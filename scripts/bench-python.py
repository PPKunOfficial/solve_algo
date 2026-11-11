#!/usr/bin/env python3
"""Benchmark project Python scripts across CPython, PyPy and GraalPy.

Interpreters are resolved with `uv python find`, so anything installed via
`uv python install` works out of the box.  Two measurement modes:

  process  A fresh interpreter process per run (judge-style).  Timings include
           interpreter startup; the "net" column subtracts the measured
           `-c pass` startup so compute time is comparable.
  inproc   A single interpreter process executes the script repeatedly, with a
           fresh namespace and stdin each iteration.  Use this for steady-state
           numbers, especially when comparing JITs (PyPy / GraalPy).

Solutions that read stdin are fed --input.  Without it, the largest *.in in a
sibling testcases/<stem>/ directory is used (the luogu/ layout), otherwise they
run with an empty stdin and usually fail -- which is reported, not hidden.
Large deterministic inputs for several luogu solutions can be generated with
scripts/gen-bench-inputs.py.

Examples:
  python3 scripts/bench-python.py luogu/P2367.py --input big.in
  python3 scripts/bench-python.py luogu/P2367.py --mode inproc --warmup 3 --runs 10
  python3 scripts/bench-python.py 'leetcode/python/49.字母异位词分组.py'
  python3 scripts/bench-python.py luogu/P2367.py --input big.in --json > timing.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_INTERPRETERS = (
    "cpython=cpython3",
    "pypy=pypy3",
    "graalpy=graalpy",
)

VERSION_PROBE = (
    "import platform; "
    "print(platform.python_implementation() + ' ' + platform.python_version())"
)

# Runs inside the target interpreter for --mode inproc.  The solution is
# compiled once, then executed in a fresh module namespace on every iteration
# (a real module __dict__, not a plain dict: PyPy's JIT only optimizes the
# former).  stdin is refilled from the input file and stdout/stderr are
# replaced by a sink that only counts bytes and hashes them, so output volume
# does not distort timings and can still be compared between interpreters.
INPROC_DRIVER = r"""
import hashlib, io, json, sys, time, types

path, inp, warmup, runs = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])

data = b""
if inp:
    with open(inp, "rb") as fh:
        data = fh.read()

real_stdin, real_stdout, real_stderr = sys.stdin, sys.stdout, sys.stderr


class Sink:
    encoding = "utf-8"
    errors = "strict"

    def __init__(self):
        self.count = 0
        self.chunks = []
        self.buffer = self

    def write(self, chunk):
        if isinstance(chunk, str):
            chunk = chunk.encode("utf-8", "surrogatepass")
        else:
            chunk = bytes(chunk)
        self.count += len(chunk)
        self.chunks.append(chunk)
        return len(chunk)

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def flush(self):
        pass

    def isatty(self):
        return False

    def fileno(self):
        raise io.UnsupportedOperation("fileno")

    def digest(self):
        hasher = hashlib.sha1()
        for chunk in self.chunks:
            hasher.update(chunk)
        return hasher.hexdigest()


result = {"times": [], "outputs": [], "error": None}

try:
    with open(path, "rb") as fh:
        code = compile(fh.read(), path, "exec")
except BaseException as exc:
    result["error"] = "%s: %s" % (type(exc).__name__, exc)
    print(json.dumps(result), file=real_stdout)
    raise SystemExit(0)

for i in range(warmup + runs):
    sink = Sink()
    sys.stdin = io.TextIOWrapper(io.BytesIO(data), encoding="utf-8")
    sys.stdout = sink
    sys.stderr = sink
    sys.argv = [path]

    error = None
    namespace = types.ModuleType("__main__").__dict__
    namespace["__file__"] = path
    t0 = time.perf_counter()
    try:
        exec(code, namespace)
    except SystemExit as exc:
        if exc.code not in (None, 0):
            error = "SystemExit: %s" % (exc.code,)
    except BaseException as exc:
        error = "%s: %s" % (type(exc).__name__, exc)
    finally:
        t1 = time.perf_counter()
        sys.stdin, sys.stdout, sys.stderr = real_stdin, real_stdout, real_stderr

    if error:
        result["error"] = error
        break
    if i >= warmup:
        result["times"].append(t1 - t0)
        # Hashing happens after t1 so output volume does not inflate the time.
        result["outputs"].append([sink.count, sink.digest()])

print(json.dumps(result), file=real_stdout)
"""


@dataclass
class Interpreter:
    label: str
    path: str


@dataclass
class Result:
    interpreter: Interpreter
    status: str = "ok"
    times: list[float] = field(default_factory=list)
    startup: float | None = None
    output_sha1: str | None = None
    output_bytes: int = 0
    error: str | None = None


def log(message: str) -> None:
    print(message, file=sys.stderr)


def resolve_interpreter(spec: str) -> Interpreter | None:
    """Resolve NAME=REQUEST (or just REQUEST) to an interpreter path."""
    name, sep, request = spec.partition("=")
    if not sep:
        request, name = name, name

    candidate = Path(request).expanduser()
    if candidate.is_file():
        if os.access(candidate, os.X_OK):
            return Interpreter(label=name, path=str(candidate.resolve()))
        log(f"warning: {candidate} is not executable; skipping")
        return None

    path = None
    uv = shutil.which("uv")
    if uv:
        cp = subprocess.run(
            [uv, "python", "find", "--no-project", request],
            capture_output=True,
            text=True,
        )
        if cp.returncode == 0 and cp.stdout.strip():
            path = cp.stdout.strip().splitlines()[-1]
    if not path:
        path = shutil.which(request)
    if not path:
        log(f"warning: could not resolve interpreter {request!r}; skipping")
        return None
    return Interpreter(label=name, path=str(Path(path).resolve()))


def probe_version(interp: Interpreter) -> str | None:
    try:
        cp = subprocess.run(
            [interp.path, "-c", VERSION_PROBE],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if cp.returncode == 0 and cp.stdout.strip():
        return cp.stdout.strip()
    return None


def measure_startup(interp: Interpreter, reps: int = 5) -> float | None:
    times = []
    for _ in range(reps):
        started = time.perf_counter()
        try:
            subprocess.run(
                [interp.path, "-c", "pass"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired):
            return None
        times.append(time.perf_counter() - started)
    return min(times)


def find_input(file: Path) -> Path | None:
    """Find the largest .in next to the solution, following the luogu layout."""
    stem = file.stem
    candidates = [
        file.parent / "testcases" / stem,
        file.parent.parent / "testcases" / stem,
        file.parent / f"{stem}.in",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
        if candidate.is_dir():
            inputs = [p for p in candidate.glob("*.in") if p.is_file()]
            if inputs:
                return max(inputs, key=lambda p: p.stat().st_size)
    return None


def resolve_input(path: Path | None) -> Path | None:
    if path is None:
        return None
    path = path.expanduser().resolve()
    if path.is_dir():
        inputs = [p for p in path.glob("*.in") if p.is_file()]
        if not inputs:
            raise SystemExit(f"error: no .in files found in {path}")
        path = max(inputs, key=lambda p: p.stat().st_size)
    if not path.is_file():
        raise SystemExit(f"error: input file not found: {path}")
    return path


def short_error(data: bytes | str) -> str:
    text = data.decode("utf-8", "replace") if isinstance(data, bytes) else data
    text = " ".join(text.split())
    return text[-300:] or "(no stderr output)"


def bench_process(
    interp: Interpreter,
    file: Path,
    input_path: Path | None,
    warmup: int,
    runs: int,
    timeout: float,
) -> Result:
    times = []
    output_sha1 = None
    output_bytes = 0
    for index in range(warmup + runs):
        stdin_path = input_path if input_path is not None else Path(os.devnull)
        started = time.perf_counter()
        try:
            with open(stdin_path, "rb") as stdin:
                cp = subprocess.run(
                    [interp.path, str(file)],
                    stdin=stdin,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=timeout,
                    cwd=str(file.parent),
                )
        except subprocess.TimeoutExpired:
            return Result(interp, status="failed", error=f"timed out after {timeout:g}s")
        except OSError as exc:
            return Result(interp, status="failed", error=f"failed to start: {exc}")
        elapsed = time.perf_counter() - started

        if cp.returncode != 0:
            detail = short_error(cp.stderr)
            return Result(
                interp,
                status="failed",
                error=f"exit code {cp.returncode}: {detail}",
            )
        if index >= warmup:
            times.append(elapsed)
            if output_sha1 is None:
                output_sha1 = hashlib.sha1(cp.stdout).hexdigest()
                output_bytes = len(cp.stdout)
    return Result(interp, times=times, output_sha1=output_sha1, output_bytes=output_bytes)


def bench_inproc(
    interp: Interpreter,
    file: Path,
    input_path: Path | None,
    warmup: int,
    runs: int,
    timeout: float,
) -> Result:
    command = [
        interp.path,
        "-c",
        INPROC_DRIVER,
        str(file),
        str(input_path) if input_path is not None else "",
        str(warmup),
        str(runs),
    ]
    budget = timeout * (warmup + runs) + 30
    try:
        cp = subprocess.run(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=budget,
            cwd=str(file.parent),
        )
    except subprocess.TimeoutExpired:
        return Result(interp, status="failed", error=f"timed out after {budget:g}s")
    except OSError as exc:
        return Result(interp, status="failed", error=f"failed to start: {exc}")

    if cp.returncode != 0:
        return Result(
            interp,
            status="failed",
            error=f"exit code {cp.returncode}: {short_error(cp.stderr)}",
        )

    lines = cp.stdout.decode("utf-8", "replace").strip().splitlines()
    try:
        payload = json.loads(lines[-1])
    except (IndexError, json.JSONDecodeError):
        return Result(
            interp,
            status="failed",
            error=f"driver produced no result: {short_error(cp.stderr)}",
        )

    if payload.get("error"):
        return Result(interp, status="failed", error=payload["error"])

    times = payload.get("times") or []
    if not times:
        return Result(interp, status="failed", error="no successful iterations")

    outputs = payload.get("outputs") or []
    output_bytes, output_sha1 = outputs[-1] if outputs else (0, None)
    return Result(
        interp,
        times=times,
        output_sha1=output_sha1,
        output_bytes=output_bytes,
    )


def fmt_time(seconds: float | None) -> str:
    if seconds is None:
        return "-"
    millis = seconds * 1000
    if millis < 1:
        return f"{millis:.2f}ms"
    if millis < 1000:
        return f"{millis:.1f}ms"
    return f"{millis / 1000:.2f}s"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def describe_input(input_path: Path | None) -> str:
    if input_path is None:
        return "none (empty stdin)"
    return f"{display_path(input_path)} ({input_path.stat().st_size} B)"


def print_table(results: list[Result], mode: str) -> None:
    ok = [r for r in results if r.status == "ok"]
    failed = [r for r in results if r.status != "ok"]

    if ok:
        medians = [statistics.median(r.times) for r in ok]
        fastest = min(medians)

        headers = ["interpreter", "startup", "best", "median", "mean"]
        if mode == "process":
            headers.append("net")
        headers.append("vs best")

        rows = []
        for result, median in zip(ok, medians):
            row = [
                result.interpreter.label,
                fmt_time(result.startup),
                fmt_time(min(result.times)),
                fmt_time(median),
                fmt_time(statistics.mean(result.times)),
            ]
            if mode == "process":
                net = None
                if result.startup is not None:
                    net = max(0.0, median - result.startup)
                row.append(fmt_time(net))
            row.append(f"{median / fastest:.2f}x")
            rows.append(row)

        widths = [
            max(len(row[i]) for row in [headers, *rows])
            for i in range(len(headers))
        ]
        formatted = []
        for row in [headers, *rows]:
            cells = [
                cell.ljust(widths[i]) if i == 0 else cell.rjust(widths[i])
                for i, cell in enumerate(row)
            ]
            formatted.append("  " + "  ".join(cells).rstrip())
        print("\n".join(formatted))

        hashes = {r.output_sha1 for r in ok if r.output_sha1 is not None}
        if len(hashes) == 1:
            sample = ok[0]
            scope = "across interpreters" if len(ok) > 1 else "across runs"
            print(
                f"  output: identical {scope} "
                f"({sample.output_bytes} B, sha1 {sample.output_sha1[:12]})"
            )
        elif len(hashes) > 1:
            detail = ", ".join(
                f"{r.interpreter.label}={r.output_sha1[:8]}" for r in ok
            )
            print(f"  WARNING: output differs: {detail}")

    for result in failed:
        print(f"  FAILED {result.interpreter.label}: {result.error}")


def result_to_dict(result: Result, mode: str) -> dict:
    payload = {
        "interpreter": result.interpreter.label,
        "path": result.interpreter.path,
        "status": result.status,
        "startup_s": result.startup,
        "times_s": result.times,
        "output_sha1": result.output_sha1,
        "output_bytes": result.output_bytes,
        "error": result.error,
    }
    if result.times:
        best = min(result.times)
        median = statistics.median(result.times)
        payload["best_s"] = best
        payload["median_s"] = median
        payload["mean_s"] = statistics.mean(result.times)
        if mode == "process" and result.startup is not None:
            payload["net_median_s"] = max(0.0, median - result.startup)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Benchmark project scripts across Python interpreters.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Examples:", 1)[1].strip(),
    )
    parser.add_argument("files", nargs="*", type=Path, help="solution .py files")
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        help="stdin file (or a directory, whose largest .in is used) for all files",
    )
    parser.add_argument(
        "-r", "--runs", type=int, default=5, help="measured runs (default: 5)"
    )
    parser.add_argument(
        "-w",
        "--warmup",
        type=int,
        default=1,
        help="unmeasured warmup runs (default: 1; use 10+ with --mode inproc for "
        "JIT interpreters)",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=30.0,
        help="per-run timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--mode",
        choices=("process", "inproc"),
        default="process",
        help="process = fresh interpreter per run; inproc = repeated exec in one "
        "interpreter (default: process)",
    )
    parser.add_argument(
        "--interpreter",
        action="append",
        metavar="NAME=REQUEST",
        help="interpreter to benchmark, repeatable (default: cpython=cpython3, "
        "pypy=pypy3, graalpy=graalpy)",
    )
    parser.add_argument(
        "--list-interpreters",
        action="store_true",
        help="resolve and print interpreters, then exit",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = parser.parse_args(argv)

    if not args.list_interpreters and not args.files:
        parser.error("the following arguments are required: files")
    if args.runs < 1:
        parser.error("--runs must be at least 1")
    if args.warmup < 0:
        parser.error("--warmup must not be negative")

    specs = args.interpreter or list(DEFAULT_INTERPRETERS)
    interpreters: list[Interpreter] = []
    seen_paths = set()
    for spec in specs:
        interp = resolve_interpreter(spec)
        if interp is None or interp.path in seen_paths:
            continue
        seen_paths.add(interp.path)
        version = probe_version(interp)
        if version:
            interp.label = version
        interpreters.append(interp)

    if not interpreters:
        log("error: no usable interpreters found")
        return 2

    if args.list_interpreters:
        if args.json:
            print(
                json.dumps(
                    [{"label": i.label, "path": i.path} for i in interpreters],
                    ensure_ascii=False,
                    indent=2,
                )
            )
        else:
            for interp in interpreters:
                print(f"{interp.label:<20} {interp.path}")
        return 0

    files = [path.expanduser().resolve() for path in args.files]
    for path in files:
        if not path.is_file():
            log(f"error: solution not found: {path}")
            return 2

    explicit_input = resolve_input(args.input)
    startup_cache: dict[str, float | None] = {}

    if not args.json:
        print(
            f"mode={args.mode}  runs={args.runs}  warmup={args.warmup}  "
            f"timeout={args.timeout:g}s"
        )
        print("interpreters: " + ", ".join(i.label for i in interpreters))

    report = {
        "mode": args.mode,
        "runs": args.runs,
        "warmup": args.warmup,
        "timeout_s": args.timeout,
        "interpreters": [
            {"label": interp.label, "path": interp.path} for interp in interpreters
        ],
        "files": [],
    }

    for file in files:
        input_path = explicit_input
        if input_path is None:
            input_path = find_input(file)

        if not args.json:
            label = display_path(file)
            print(f"\n== {label}  (stdin: {describe_input(input_path)})")
        else:
            log(f"benchmarking {display_path(file)}")

        results = []
        for interp in interpreters:
            if interp.path not in startup_cache:
                startup_cache[interp.path] = measure_startup(interp)

            if args.mode == "process":
                result = bench_process(
                    interp, file, input_path, args.warmup, args.runs, args.timeout
                )
            else:
                result = bench_inproc(
                    interp, file, input_path, args.warmup, args.runs, args.timeout
                )
            result.startup = startup_cache[interp.path]
            results.append(result)

        if args.json:
            report["files"].append(
                {
                    "file": display_path(file),
                    "input": str(input_path) if input_path else None,
                    "input_bytes": input_path.stat().st_size if input_path else 0,
                    "results": [result_to_dict(r, args.mode) for r in results],
                }
            )
        else:
            print_table(results, args.mode)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
