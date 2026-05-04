# Simulated pilgrim group data for scheduling demonstration — not real-world measurements.
#
# The FCFS order is deliberately mixed so that naive ordering (process groups as they
# arrive) is clearly suboptimal.  The Greedy algorithm (urgency-first) improves on FCFS
# but is still not optimal because it ignores processing time.  The DP solution (bitmask
# exhaustive search) finds the true optimum: the Weighted Shortest Processing Time order.
#
# Teaching point: sorting by urgency alone is a natural heuristic but fails because a
# highly-urgent group with a very long processing time blocks many other groups behind it.
# The correct trade-off is urgency / processing_time (WSPT rule), which DP discovers.

PILGRIM_GROUPS = [
    # id     size      urgency  processing_time (hours)
    {"id": "G1",  "size": 120_000, "urgency": 1, "processing_time": 2.0},
    {"id": "G2",  "size":  80_000, "urgency": 5, "processing_time": 0.5},
    {"id": "G3",  "size":  90_000, "urgency": 1, "processing_time": 1.5},
    {"id": "G4",  "size":  70_000, "urgency": 4, "processing_time": 0.7},
    {"id": "G5",  "size":  60_000, "urgency": 2, "processing_time": 1.0},
    {"id": "G6",  "size":  85_000, "urgency": 5, "processing_time": 2.0},
    {"id": "G7",  "size":  75_000, "urgency": 3, "processing_time": 0.8},
    {"id": "G8",  "size":  50_000, "urgency": 2, "processing_time": 0.5},
    {"id": "G9",  "size":  65_000, "urgency": 4, "processing_time": 1.5},
    {"id": "G10", "size":  95_000, "urgency": 3, "processing_time": 1.2},
]
