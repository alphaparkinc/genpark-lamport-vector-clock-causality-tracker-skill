"""
Autonomous Agent Vector Clock Causality Tracker Skill
Pure Python Standard Library implementation.
"""
from typing import List, Dict, Any

class VectorClock:
    """
    Lamport Vector Clock for causal partial ordering and concurrency detection.
    """
    def __init__(self, node_id: str, all_nodes: List[str]):
        self.node_id = node_id
        self.clock = {n: 0 for n in all_nodes}

    def local_event(self) -> Dict[str, int]:
        self.clock[self.node_id] += 1
        return dict(self.clock)

    def send_message(self) -> Dict[str, int]:
        self.clock[self.node_id] += 1
        return dict(self.clock)

    def receive_message(self, remote_clock: Dict[str, int]) -> Dict[str, int]:
        for n, val in remote_clock.items():
            self.clock[n] = max(self.clock.get(n, 0), val)
        self.clock[self.node_id] += 1
        return dict(self.clock)

    @staticmethod
    def compare(vc1: Dict[str, int], vc2: Dict[str, int]) -> str:
        keys = set(vc1) | set(vc2)
        le = all(vc1.get(k, 0) <= vc2.get(k, 0) for k in keys)
        ge = all(vc1.get(k, 0) >= vc2.get(k, 0) for k in keys)
        if le and ge:
            return "EQUAL"
        if le and not ge:
            return "BEFORE"
        if ge and not le:
            return "AFTER"
        return "CONCURRENT"
