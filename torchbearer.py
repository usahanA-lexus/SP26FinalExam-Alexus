"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Alexus Aguirre Arias
Student ID:   132191303

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

from asyncio import graph
import heapq

from torch import dist


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    return (
        "- **Why a single shortest-path run from S is not enough:**\n"
        "  To calculate the single shortest path run from S isnt enough as it does not decide which relic chamber to visit first.\n\n"
        "- **What decision remains after all inter-location costs are known:**\n"
        "  The visit order of the relic chambers before exiting still must be done.\n\n"
        "- **Why this requires a search over orders (one sentence):**\n"
        "  The total cost hinges on the order of visting relics, so you must compare multiple possible orders rather than do one shortest path computation."
    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.
    """
    sources = [spawn] + relics + [exit_node]
    unique=[]
    for node in sources:
        if node not in unique:
            unique.append(node)
    return unique

def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').
    """
    dist = {}
    for node in graph:
        dist[node] = float('inf')

    dist[source] = 0
    pq = [(0, source)]

    while pq:
        current_dist, u = heapq.heappop(pq)

        if current_dist != dist[u]:
            continue

        for v, cost in graph[u]:
            new_dist = current_dist + cost
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))
    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.
    """
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {}

    for u in sources:
        dist_table[u] = run_dijkstra(graph, u)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    return (
        "- **For nodes already finalized (in S):**\n"
        "  - The nodes already finalized already have their shortest distance from the source, thus once placed in S then it can't find a cheaper path to it.\n\n"
        "- **For nodes not yet finalized (not in S):**\n"
        "  -Their current value is the best path found so far using only finalized nodes in the middle of the path, then the estimat emight still decrease later if  a better route is discovered.\n\n"
        "### Part 3b: Why Each Phase Holds\n"
        "- **Initialization : why the invariant holds before iteration 1:**\n"
        "  - At the start S is empty, dist[x]=0 and every other node has distance infinty as no nodes are finalized. This matches the invariant because the source already has the correct distance and no other paths have eebn discovered yet.\n\n"
        "- **Maintenance : why finalizing the min-dist node is always correct:**\n"
        "  - The choosen node has the smallest estimate along all non-finalized nodes. Since edge weights are nonnegative, any other path that reaches that node later cannot become cheaper by going through another non-finalized node first so its current distance must already be correct.\n\n"
        "- **Termination : what the invariant guarantees when the algorithm ends:**\n"
        "  - When the algorithm finishes  then every reachable node has been fianlzide with tis true shrotest path distance from the source and any ndoe at infity is unreachbale.\n\n"
        "### Part 3c: Why This Matters for the Route Planner\n"
        "  - Correct shortest path distances let the Torchbearer's planner compare route options using true travel costs, so it can make the right routing decisions."
    )


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    TODO
    """
    return (
        "- **The failure mode:** A greedy rule that always picks the cheapest next relic can make a locally cheap move that leads to a worse total route later.\n"
        "- **Counter-example setup:** Using the example distances from 'S' we have \"S->B=1', 'S->C=2','S->D=2', and later some moves like 'B->C=100' and 'D->T=100' are very expensive.\n"
        "- **What greedy picks:**Greedy [icks 'B' first becaise 'B' is the cheapest relic to reach from 'S'.\n"
        "- **What optimal picks:** The best full order is 'S->B->D->C->T' with total cost '4'. while another possible order like 'S->C->B->D->T' costs '5'.\n"
        "- **Why greedy loses:**Choosing only by the next cheapest step does not account for the remaining relic order and exit cost, so a choice that looks best now may increase the total later.\n\n"
        "- The algorithm must explore each possible order fo visitng the relic chambers, ebcause the toal fuel cost depends on the full order and not jksut the next step."
    )


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    currLoc = spawn
    relics_VistedOrder = []
    currCost = 0.0
    relics_remaining = set(relics)
    best = [float('inf'), []]

    _explore(
        dist_table,
        currLoc,
        relics_remaining,
        relics_VistedOrder,
        currCost,
        exit_node,
        best
    )
    return best[0], best[1]


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    currLoc = current_loc
    relics_VistedOrder = relics_visited_order
    currCost = cost_so_far

    if not relics_remaining:
        final_cost = currCost + dist_table[currLoc][exit_node]
        if final_cost < best[0]:
            best[0] = final_cost
            best[1] = list(relics_VistedOrder)
        return

    # This pruning is safe because every remaining edge cost is nonnegative, so
    # any completed route from this state must cost at least currCost overall.
    if currCost >= best[0]:
        return

    for next_relic in list(relics_remaining):
        step_cost = dist_table[currLoc][next_relic]
        if step_cost == float('inf'):
            continue

        relics_remaining.remove(next_relic)
        relics_VistedOrder.append(next_relic)

        _explore(
            dist_table,
            next_relic,
            relics_remaining,
            relics_VistedOrder,
            currCost + step_cost,
            exit_node,
            best
        )

        relics_VistedOrder.pop()
        relics_remaining.add(next_relic)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
