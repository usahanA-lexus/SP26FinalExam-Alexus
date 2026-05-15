# The Torchbearer

**Student Name:** Alexus Aguirre Arias
**Student ID:** 132191303
**Course:** CS 460 – Algorithms | Spring 2026
---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  To calculate the single shortest path run from S isnt enough as it does not decide which relic chamber to visit first.

- **What decision remains after all inter-location costs are known:**
  The visit order of the relic chambers before exiting still must be done.

- **Why this requires a search over orders (one sentence):**
  The total cost hinges on the order of visting relics, so you must compare multiple possible orders rather than do one shortest path computation.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| spawn (S) | We need to find shortest costs from the starting point to each possible first relic. |
| relic chambers (R in M) | We need to know shortest costs between relics and from the last visited relic to the exit. |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Nested dictionary (dist_table)|
| What the keys represent | Ouer Key is the source node u, while inner key is desination node v. |
| What the values represent | dist_table[u][v] represents the minimum fuel cost from u to v. |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Python dict hash table lookup is  O(1) average for both key levels. |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** k+1 
- **Cost per run:** O(m log n)
- **Total complexity:** O((k+1)*mlogn)
- **Justification (one line):** We run Dijkstra once per selected source and store each run's full distance map.

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
  - The nodes already finalized already have their shortest distance from the source, thus once placed in S then it can't find a cheaper path to it.

- **For nodes not yet finalized (not in S):**
    -Their current value is the best path found so far using only finalized nodes in the middle of the path, then the estimat emight still decrease later if  a better route is discovered.

### Part 3b: Why Each Phase Holds
 
- **Initialization : why the invariant holds before iteration 1:**
    - At the start S is empty, dist[x]=0 and every other node has distance infinty as no nodes are finalized. This matches the invariant because the source already has the correct distance and no other paths have eebn discovered yet.

- **Maintenance : why finalizing the min-dist node is always correct:**
    - The choosen node has the smallest estimate along all non-finalized nodes. Since edge weights are nonnegative, any other path that reaches that node later cannot become cheaper by going through another non-finalized node first so its current distance must already be correct.

- **Termination : what the invariant guarantees when the algorithm ends:**
  - When the algorithm finishes  then every reachable node has been fianlzide with tis true shrotest path distance from the source and any ndoe at infity is unreachbale.

### Part 3c: Why This Matters for the Route Planner
  - Correct shortest path distances let the Torchbearer's planner compare route options using true travel costs, so it can make the right routing decisions.

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** A greedy rule that always picks the cheapest next relic can make a locally cheap move that leads to a worse total route later.
- **Counter-example setup:** Using the example distances from 'S' we have "S->B=1', 'S->C=2','S->D=2', and later some moves like 'B->C=100' and 'D->T=100' are very expensive.
- **What greedy picks:**Greedy [icks 'B' first becaise 'B' is the cheapest relic to reach from 'S'.
- **What optimal picks:** The best full order is 'S->B->D->C->T' with total cost '4'. while another possible order like 'S->C->B->D->T' costs '5'.
- **Why greedy loses:**Choosing only by the next cheapest step does not account for the remaining relic order and exit cost, so a choice that looks best now may increase the total later.

### What the Algorithm Must Explore

- The algorithm must explore each possible order fo visitng the relic chambers, ebcause the toal fuel cost depends on the full order and not jksut the next step.

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | currLoc | node | THe node wher the Torchbearer is currently standing. |
| Relics already collected | relics_VistedOrder | list[node] | The relics collected so far, in the order they were visited. |
| Fuel cost so far |currCost | float | The total fuel cost spent so far along the current partial route.|

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | 'set' stored in 'relics_remaining'|
| Operation: check if relic already collected | Time complexity: '0(1)' average, by removing it from the set. |
| Operation: mark a relic as collected | Time complexity: 'O(1)' average, by removing it from the set.|
| Operation: unmark a relic (backtrack) | Time complexity:'O(1)' average, by adding it back to the set. |
| Why this structure fits | It supports fast membership updates during recursion and backtracking, which is exactly what the search needs.|

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** 'k!'
- **Why:** The algorithm may need to try every possible order of visitng the 'k' relics.

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
