"""
Pilgrim group scheduling algorithms: FCFS, Greedy, and DP.

Problem
-------
Ten pilgrim groups must transit the Mina-Jamarat bottleneck road one at a time.
Goal: find the processing order that minimises total weighted waiting time

    TW = sum( urgency_i * wait_i )   for all groups i

where wait_i = the time group i starts being processed (i.e. all previous
groups have already finished).

Key insight
-----------
Greedy (urgency-first) is the intuitive approach but is NOT optimal because
it ignores processing time.  A highly-urgent group with a very long processing
time blocks all groups behind it.  The optimal rule is to sort by
urgency / processing_time descending (Weighted Shortest Processing Time, WSPT),
which the bitmask DP rediscovers through exhaustive search.
"""


# ---------------------------------------------------------------------------
# Shared helper
# ---------------------------------------------------------------------------

def _compute_result(schedule: list) -> tuple:
    """Compute Gantt data and total weighted wait for a given schedule order.

    Args:
        schedule: List of group dicts in the desired processing order.

    Returns:
        (schedule, total_weighted_wait, gantt_data)
        gantt_data is a list of dicts with keys:
          'id', 'start', 'end', 'urgency', 'size'
    """
    gantt = []
    total_weighted_wait = 0.0
    t = 0.0
    for g in schedule:
        total_weighted_wait += g["urgency"] * t
        gantt.append({
            "id":      g["id"],
            "start":   round(t, 4),
            "end":     round(t + g["processing_time"], 4),
            "urgency": g["urgency"],
            "size":    g["size"],
        })
        t += g["processing_time"]
    return schedule, round(total_weighted_wait, 2), gantt


# ---------------------------------------------------------------------------
# FCFS
# ---------------------------------------------------------------------------

def fcfs_schedule(groups: list) -> tuple:
    """First Come First Served: process groups in their original arrival order.

    No reordering is applied.  Acts as the baseline for comparison.

    Time complexity: O(n)

    Args:
        groups: List of group dicts (in arrival order).

    Returns:
        (schedule, total_weighted_wait, gantt_data)
    """
    return _compute_result(list(groups))


# ---------------------------------------------------------------------------
# Greedy
# ---------------------------------------------------------------------------

def greedy_schedule(groups: list) -> tuple:
    """Greedy: process groups in descending urgency order.

    This is the natural heuristic — 'most critical groups go first'.
    It improves on FCFS but is NOT optimal because it ignores processing time.
    A critical group with a very long processing time blocks many groups behind
    it, accumulating unnecessary weighted wait for all of them.

    Time complexity: O(n log n)  — dominated by the sort

    Args:
        groups: List of group dicts.

    Returns:
        (schedule, total_weighted_wait, gantt_data)
    """
    schedule = sorted(groups, key=lambda g: -g["urgency"])
    return _compute_result(schedule)


# ---------------------------------------------------------------------------
# Dynamic Programming (bitmask)
# ---------------------------------------------------------------------------

def dp_schedule(groups: list) -> tuple:
    """Optimal scheduling via bitmask DP — minimises total weighted waiting time.

    Uses the Weighted Job Scheduling (bitmask) DP formulation:

        dp[S] = minimum TW achievable by scheduling exactly the groups in S,
                in some order, starting from time 0.

    Transition: to schedule group j as the LAST in S:
        dp[S] = dp[S \\ {j}]  +  urgency[j] * cum_time[S \\ {j}]

    where cum_time[S] = sum of processing times of groups in S.

    Because n = 10, there are only 2^10 = 1024 states.

    Time complexity:  O(n * 2^n)  — feasible for small n only.
    Space complexity: O(2^n)

    The optimal order discovered here equals the WSPT (Weighted Shortest
    Processing Time) rule, i.e. sort by urgency/processing_time descending.

    Args:
        groups: List of group dicts.

    Returns:
        (schedule, total_weighted_wait, gantt_data)
    """
    n    = len(groups)
    FULL = (1 << n) - 1

    # Precompute cumulative processing time for every subset mask
    cum_time = [0.0] * (1 << n)
    for mask in range(1, 1 << n):
        # Isolate the lowest set bit to find one group in the mask
        lsb = mask & (-mask)
        j   = lsb.bit_length() - 1
        cum_time[mask] = cum_time[mask ^ lsb] + groups[j]["processing_time"]

    INF  = float("inf")
    dp   = [INF] * (1 << n)
    prev = [-1]  * (1 << n)
    dp[0] = 0.0

    for mask in range(1 << n):
        if dp[mask] == INF:
            continue
        t = cum_time[mask]
        for j in range(n):
            if mask & (1 << j):
                continue                       # group j already scheduled
            new_mask = mask | (1 << j)
            cost = dp[mask] + groups[j]["urgency"] * t
            if cost < dp[new_mask]:
                dp[new_mask] = cost
                prev[new_mask] = mask

    # Reconstruct optimal order by tracing prev[] back from the full mask
    order = []
    mask  = FULL
    while mask:
        p     = prev[mask]
        added = mask ^ p                       # single bit: the group just added
        j     = added.bit_length() - 1
        order.append(j)
        mask  = p
    order.reverse()

    schedule = [groups[i] for i in order]
    return _compute_result(schedule)
