import sys
import os
import time
from typing import List, Tuple
from scheduler import Scheduler

NUM_OF_EXPAND = [0, 100]
MAX_OF_PHY_MAC = 100000
MAX_SCORE = 200.0
SCORE_OF_BASLINE = 200.0 * 0.6

class InteractiveSystem:
    def __init__(self):
        self.n = 0
        self.total_vcpu = 0
        self.total_mem = 0
        self.num_of_ins = 0
        self.used_vcpu: List[int] = []
        self.used_mem: List[int] = []
        self.id_to_pos: List[int] = []
        self.id_to_vcpu: List[int] = []
        self.id_to_mem: List[int] = []
        self.scheduler = Scheduler()

    def addVM(self, id: int, vcpu: int, mem: int):
        assert id == len(self.id_to_pos)
        self.id_to_pos.append(-1)
        self.id_to_vcpu.append(vcpu)
        self.id_to_mem.append(mem)

    def create(self, id: int, pos: int, vcpu: int, mem: int) -> bool:
        if pos < 0 or pos >= len(self.used_vcpu):
            return False
        if (self.used_vcpu[pos] + vcpu > self.total_vcpu) or (self.used_mem[pos] + mem > self.total_mem):
            return False
        self.id_to_pos[id] = pos
        self.used_vcpu[pos] += vcpu
        self.used_mem[pos] += mem
        return True

    def remove(self, id: int):
        pos = self.id_to_pos[id]
        vcpu = self.id_to_vcpu[id]
        mem = self.id_to_mem[id]
        self.used_vcpu[pos] -= vcpu
        self.used_mem[pos] -= mem

    def init(self, file_name: str):
        self.file = open(file_name, 'r')
        self.n, self.total_vcpu, self.total_mem = map(int, self.file.readline().split())
        self.num_of_ins = int(self.file.readline())
        self.used_vcpu = [0] * self.n
        self.used_mem = [0] * self.n
        self.scheduler.init(self.n, self.total_vcpu, self.total_mem)

    def runOnce(self) -> bool:
        this_line = self.file.readline().split()
        ins = this_line[0]
        id = int(this_line[1])
        is_success = True
        if ins[0] == 'C':
            vcpu, mem = int(this_line[2]), int(this_line[3])
            res = self.scheduler.create(id, vcpu, mem)
            if res[1] < NUM_OF_EXPAND[0] or res[1] > NUM_OF_EXPAND[1]:
                return False
            pos = res[0]
            for _ in range(res[1]):
                self.n += 1
                if self.n > MAX_OF_PHY_MAC:
                    return False
                self.used_vcpu.append(0)
                self.used_mem.append(0)
            self.id_to_pos.append(0)
            self.id_to_vcpu.append(vcpu)
            self.id_to_mem.append(mem)
            is_success = self.create(id, pos, vcpu, mem)
        else:
            self.scheduler.remove(id)
            self.remove(id)
        return is_success

    def getNumOfMachines(self) -> int:
        is_success = True
        for _ in range(self.num_of_ins):
            if not self.runOnce():
                is_success = False
                break
        return len(self.used_vcpu) if is_success else -1

def main():
    mode = "GEN_SCH_SCORE"
    if "GEN_SCH_SCORE" in mode:
        score_path = "./final_score.txt"
        with open(score_path, 'w') as f:
            sys.stdout = f
            n_tests = 20
            total_score = 0
            score_list = [0.0] * n_tests
            time_list = [0.0] * n_tests

            for i in range(1, n_tests + 1):
                print(f"test case #{i}: ", file=sys.stderr, end='', flush=True)
                
                # 记录单测试点开始时间
                start_time = time.perf_counter()
                
                inter_sys = InteractiveSystem()
                file_name = f"./data/{i}.in"
                inter_sys.init(file_name)
                res = inter_sys.getNumOfMachines()
                
                # 计算单测试点执行时长
                elapsed = time.perf_counter() - start_time
                time_list[i - 1] = elapsed

                file_name = f"./data/baseline_{i}.out"
                with open(file_name, 'r') as baseline_file:
                    baseline = int(baseline_file.readline())
                    score = 0.0
                    if res != -1:
                        score = min(MAX_SCORE, 1.0 * baseline / res * SCORE_OF_BASLINE)
                    total_score += score
                    print(f"{score:.2f} (took {elapsed:.3f}s)", file=sys.stderr)
                
                score_list[i - 1] = score

            total_elapsed = sum(time_list)
            print(f"Final Score: {total_score / n_tests:.2f} (Total time: {total_elapsed:.3f}s)", file=sys.stderr)
            print(f"Final Score: {total_score / n_tests:.2f} (Total time: {total_elapsed:.3f}s)")
            
            for i in range(n_tests):
                print(f"Score of Test Case #{i + 1}: {score_list[i]:.2f} (Time: {time_list[i]:.3f}s)")

if __name__ == "__main__":
    main()