#!/usr/bin/env python3
"""Generate deterministic large inputs for scripts/bench-python.py.

The files exercise different interpreter bottlenecks: big-integer arithmetic,
nested loops, binary search, heap operations, sorting, matrix rotation, custom
integer parsing and string scanning.

Examples:
  python3 scripts/gen-bench-inputs.py /tmp/bench-inputs
  python3 scripts/gen-bench-inputs.py /tmp/bench-inputs P1080 P3799
  python3 scripts/bench-python.py luogu/P1080.py -i /tmp/bench-inputs/P1080.in
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path


def gen_p1080(out: Path, rng: random.Random) -> None:
    """Big-integer multiplication/division loop (king game)."""
    n = 1000
    with open(out / "P1080.in", "w") as f:
        f.write(f"{n}\n")
        f.write(f"{rng.randint(1, 10000)} {rng.randint(1, 10000)}\n")
        for _ in range(n):
            f.write(f"{rng.randint(1, 9999)} {rng.randint(1, 10000)}\n")


def gen_p2367(out: Path, rng: random.Random) -> None:
    """Custom byte-level integer parser plus difference-array loops."""
    n = p = 200_000
    with open(out / "P2367.in", "w") as f:
        f.write(f"{n} {p}\n")
        f.write(" ".join(str(rng.randint(0, 1000)) for _ in range(n)) + "\n")
        for _ in range(p):
            x = rng.randint(1, n)
            y = rng.randint(x, n)
            f.write(f"{x} {y} {rng.randint(0, 1000)}\n")


def gen_p3799(out: Path, rng: random.Random) -> None:
    """Nested counting loops (~6M iterations for values <= 5000)."""
    n = 1_000_000
    with open(out / "P3799.in", "w") as f:
        f.write(f"{n}\n")
        f.write(" ".join(str(rng.randint(1, 5000)) for _ in range(n)))
        f.write("\n")


def gen_p2249(out: Path, rng: random.Random) -> None:
    """A million binary searches, half of them hits."""
    n = m = 1_000_000
    values = sorted(rng.randint(0, 10**9) for _ in range(n))
    queries = [
        rng.choice(values) if i % 2 == 0 else rng.randint(0, 10**9)
        for i in range(m)
    ]
    with open(out / "P2249.in", "w") as f:
        f.write(f"{n} {m}\n")
        f.write(" ".join(map(str, values)) + "\n")
        f.write(" ".join(map(str, queries)) + "\n")


def gen_p1090(out: Path, rng: random.Random) -> None:
    """500k heap pops/pushes (fruit merging)."""
    n = 500_000
    with open(out / "P1090.in", "w") as f:
        f.write(f"{n}\n")
        f.write(" ".join(str(rng.randint(1, 10000)) for _ in range(n)) + "\n")


def gen_p1271(out: Path, rng: random.Random) -> None:
    """Sort and join one million integers."""
    n, m = 1000, 1_000_000
    with open(out / "P1271.in", "w") as f:
        f.write(f"{n} {m}\n")
        f.write(" ".join(str(rng.randint(1, n)) for _ in range(m)) + "\n")


def gen_p4924(out: Path, rng: random.Random) -> None:
    """Sub-matrix rotation: nested list indexing/comprehension loops."""
    n, m = 400, 200
    with open(out / "P4924.in", "w") as f:
        f.write(f"{n} {m}\n")
        for _ in range(m):
            r = rng.randint(1, 100)
            x = rng.randint(r + 1, n - r)
            y = rng.randint(r + 1, n - r)
            f.write(f"{x} {y} {r} {rng.randint(0, 1)}\n")


def gen_p1042(out: Path, rng: random.Random) -> None:
    """Scan a two-million-character W/L stream."""
    n = 2_000_000
    with open(out / "P1042.in", "w") as f:
        f.write("".join(rng.choice("WL") for _ in range(n)))
        f.write("E\n")


CASES = {
    "P1080": ("big-integer arithmetic", gen_p1080),
    "P2367": ("byte-level integer parsing + difference array", gen_p2367),
    "P3799": ("nested counting loops", gen_p3799),
    "P2249": ("binary search x1e6", gen_p2249),
    "P1090": ("heap x500k", gen_p1090),
    "P1271": ("sort x1e6", gen_p1271),
    "P4924": ("matrix rotation loops", gen_p4924),
    "P1042": ("string scan", gen_p1042),
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate deterministic large inputs for bench-python.py.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Examples:", 1)[1].strip(),
    )
    parser.add_argument("out", type=Path, help="output directory")
    parser.add_argument(
        "cases",
        nargs="*",
        choices=sorted(CASES),
        help="cases to generate (default: all)",
    )
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    for name in args.cases or sorted(CASES):
        description, generator = CASES[name]
        rng = random.Random(int(name[1:]))
        generator(args.out, rng)
        path = args.out / f"{name}.in"
        print(f"{name:<6} {path.stat().st_size / 1e6:>6.1f} MB  {description}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
