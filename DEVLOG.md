# Development Log - The Torchbearer

**Student Name:** Alexus Aguirre Arias
**Student ID:** 132191303

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 - [May 13th 2026]: Initial Plan

My plan is to read the assignment.md and readme.md over, and identifuing what information needs to be stored so I can first implement that. Then build the main planner on top of that as it depends on correct shortest path values. The hardest parts will most liekly be making sure the algorthim deos not explore unncecessary routes.

---

## Entry 2 - [May 14th 2026]: Bug Fix and Search-State Design

At first I was treating the route search too loosely and had not lined the code variables up with the Part 5a state definition, which made it harder to reason about what each recursive call actually represented. I changed the implementation so each state clearly tracks `currLoc`, `relics_VistedOrder`, and `currCost`, and I used a `set` named `relics_remaining` to support fast mark/unmark steps during backtracking. I also caught that one of the explanation functions in `torchbearer.py` was not valid Python as written, so I rewrote it as a proper returned string before continuing with the route planner.

---

## Entry 3 - [Date]: [Short description]

_Your entry here._

---

## Entry 4 - [Date]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry - [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | |
| Part 2: Precomputation Design | |
| Part 3: Algorithm Correctness | |
| Part 4: Search Design | |
| Part 5: State and Search Space | |
| Part 6: Pruning | |
| Part 7: Implementation | |
| README and DEVLOG writing | |
| **Total** | |
