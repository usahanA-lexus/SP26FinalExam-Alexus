# Development Log - The Torchbearer

**Student Name:** Alexus Aguirre Arias
**Student ID:** 132191303
---

## Entry 1 - [May 13th 2026]: Initial Plan

My plan is to read the assignment.md and readme.md over, and identifuing what information needs to be stored so I can first implement that. Then build the main planner on top of that as it depends on correct shortest path values. The hardest parts will most liekly be making sure the algorthim deos not explore unncecessary routes.

---

## Entry 2 - [May 14th 2026]: Bug Fix and Search-State Design

At first I was treating the route search too loosely and had not lined the code variables up with the Part 5a state definition, which made it harder to reason about what each recursive call actually represented. I changed the implementation so each state clearly tracks `currLoc`, `relics_VistedOrder`, and `currCost`, and I used a `set` named `relics_remaining` to support fast mark/unmark steps during backtracking. I also caught that one of the explanation functions in `torchbearer.py` was not valid Python as written, so I rewrote it as a proper returned string before continuing with the route planner.

---

## Entry 3 - [May 14th 2026]: ReadMe part 6 answered and test

After finishing the main route planner, I went back through README.md and torchbearer.py to make sure the written answers still matched the actual variable names and search design used in code. I checked the Part 4, Part 5, and Part 6 wording against the implementation and then ran the provided tests to confirm the full pipeline worked correctly. The tests all passed!
---

## Entry 4 - [May 14th 2026]: Post-Implementation Reflection

If I had more time then I would improve the pruning so the search could cut off mroe branches earlier isntead of only comapring currCost to the current best route. Currently, its a safe approach but suppose I could try out estimating the minimum remaining cost from the current location through the unvisited relics to the exit. That would let the search stop ealreir on rbanches that are already guaranteed to end worse than the current best route. 

---

## Final Entry - [May 14th 2026]: Time Estimate

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis |0.5 |
| Part 2: Precomputation Design |1|
| Part 3: Algorithm Correctness |0.5|
| Part 4: Search Design | 1 |
| Part 5: State and Search Space | 1 |
| Part 6: Pruning | 0.5 |
| Part 7: Implementation |2|
| README and DEVLOG writing |1 |
| **Total** | 7.5 |
