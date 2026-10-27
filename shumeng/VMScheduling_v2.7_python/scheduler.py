from typing import Tuple

class Scheduler:
    def __init__(self):
        self.c = 0
        self.m = 0
        self.pm_vcpu = []
        self.pm_mem = []
        self.vm_map = {}
        # 记录有负载但未满的主机索引集合，大幅缩小子集遍历规模
        self.partial_pms = set()
        # 全空物理机池（避免重复遍历多个全空机器）
        self.empty_pms = []

    def init(self, n: int, c: int, m: int):
        self.c = c
        self.m = m
        self.pm_vcpu = [c] * n
        self.pm_mem = [m] * n
        self.vm_map.clear()
        self.partial_pms.clear()
        # 初始时所有主机均为空闲
        self.empty_pms = list(range(n))

    def create(self, id: int, vcpu: int, mem: int) -> Tuple[int, int]:
        c_inv = 1.0 / self.c
        m_inv = 1.0 / self.m

        best_id = -1
        best_score = -float('inf')

        # 1. 仅在已有负载的机器中寻找最佳拟合（集合规模通常远小于总机数）
        for i in self.partial_pms:
            rem_v = self.pm_vcpu[i] - vcpu
            rem_m = self.pm_mem[i] - mem

            if rem_v >= 0 and rem_m >= 0:
                # 紧凑度与平衡度打分
                ratio_v = rem_v * c_inv
                ratio_m = rem_m * m_inv
                compactness = (1.0 - ratio_v) + (1.0 - ratio_m)
                balance_diff = abs(ratio_v - ratio_m)

                score = compactness * 2.0 - balance_diff * 0.8

                if score > best_score:
                    best_score = score
                    best_id = i
                    # 强剪枝：如果剩余空间已经非常小（利用率极高），直接采纳
                    if rem_v <= 2 and rem_m <= 8:
                        break

        # 2. 如果部分占用的机器放得下，直接放置
        if best_id != -1:
            self.pm_vcpu[best_id] -= vcpu
            self.pm_mem[best_id] -= mem
            self.vm_map[id] = (best_id, vcpu, mem)
            # 如果这台机器已经被彻底填满，从 partial_pms 移除避免后续无效遍历
            if self.pm_vcpu[best_id] == 0 or self.pm_mem[best_id] == 0:
                self.partial_pms.discard(best_id)
            return best_id, 0

        # 3. 如果已有负载的机器都放不下，看是否存量里有全空机器
        if self.empty_pms:
            pm_id = self.empty_pms.pop()
            self.pm_vcpu[pm_id] -= vcpu
            self.pm_mem[pm_id] -= mem
            self.vm_map[id] = (pm_id, vcpu, mem)
            if self.pm_vcpu[pm_id] > 0 and self.pm_mem[pm_id] > 0:
                self.partial_pms.add(pm_id)
            return pm_id, 0

        # 4. 彻底没有空闲主机，扩容 1 台
        new_id = len(self.pm_vcpu)
        self.pm_vcpu.append(self.c - vcpu)
        self.pm_mem.append(self.m - mem)
        self.vm_map[id] = (new_id, vcpu, mem)
        if self.pm_vcpu[new_id] > 0 and self.pm_mem[new_id] > 0:
            self.partial_pms.add(new_id)
        return new_id, 1

    def remove(self, id: int):
        if id in self.vm_map:
            machine_id, vcpu, mem = self.vm_map.pop(id)
            self.pm_vcpu[machine_id] += vcpu
            self.pm_mem[machine_id] += mem

            curr_v = self.pm_vcpu[machine_id]
            curr_m = self.pm_mem[machine_id]

            if curr_v == self.c and curr_m == self.m:
                # 恢复全空，移出 partial_pms，加入 empty_pms
                self.partial_pms.discard(machine_id)
                self.empty_pms.append(machine_id)
            else:
                # 重新拥有部分可用资源
                self.partial_pms.add(machine_id)