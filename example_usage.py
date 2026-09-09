"""Example usage for Vector Clock Causality Skill."""
from client import VectorClock

def main():
    print("Executing Vector Clock Causality Tracker...")
    nodes = ["Agent_A", "Agent_B", "Agent_C"]
    va = VectorClock("Agent_A", nodes)
    vb = VectorClock("Agent_B", nodes)

    msg_from_a = va.send_message()
    vb.receive_message(msg_from_a)
    rel = VectorClock.compare(msg_from_a, vb.clock)
    print("Relation (msg_from_a vs vb):", rel)
    assert rel == "BEFORE"

    vc = VectorClock("Agent_C", nodes)
    vc.local_event()
    conc_rel = VectorClock.compare(va.clock, vc.clock)
    print("Relation (va vs vc):", conc_rel)
    assert conc_rel == "CONCURRENT"
    print("Vector Clock Causality verified successfully!")

if __name__ == "__main__":
    main()
