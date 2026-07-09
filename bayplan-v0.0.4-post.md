title: BAYPLAN runs the ducts
date: 2026-07-08
tags: field-instruments, workshop, tradigital
status: draft

---

Ask anyone who has plumbed a shop for dust collection and they will tell you the same thing: the machine is the easy part. It is the four-inch pipe snaking back to the collector, gaining an elbow here and a wye there, each one quietly stealing airflow, that decides whether your bandsaw actually clears its own chips or just pushes them around. You cannot see static pressure. You feel it, weeks later, as a pile of dust under a machine that the collector was supposed to reach.

This release gives BAYPLAN a nose for that problem, and for its electrical cousin. The utilities layer is live.

## Drop, drag, wire

Open the utilities panel and you get two things to place: a dust collector and an electrical panel. Drop them, drag them where they really live in your shop, against the wall, in the corner, wherever the real one sits. Then click Wire all, and every machine on the floor connects itself to the nearest collector and the nearest panel in a single stroke. Dust runs snake out as thick tan lines, turning one honest orthogonal corner the way real duct does, because duct does not run diagonally across a room. Electrical runs trace out as thin dashed lines, because wire bends however it likes.

Drag the collector to the far corner and watch the runs stretch and the numbers climb. That is the whole instrument in one gesture.

## The numbers it now knows

For dust, BAYPLAN computes effective length, which is the straight run plus a charge for every bend. That charge is the part I care about, because it is the part people forget. A ninety-degree elbow in four-inch pipe is not a corner, it is another six feet of pipe as far as your collector is concerned, and the tool now says so. Run a line too far for its diameter and it turns red and tells you it has exceeded the budget. The elbow-equivalent table and the length budgets are written down, tunable, and finally out of my head and into the code where they belong.

For electrical, it rolls up connected load into a 120-volt bucket and a 240-volt bucket, and it does the one check that has bitten every shop owner at least once: if a machine needs 240 volts and there is no panel that can give it 240 volts, that is an error, in red, before you buy the machine. It watches the total load against the panel's main, too, so you know when you are asking one service to do more than it can.

## Tested where the physics lives

The elbow math is the technical heart of this release, so it carries the tests. There is an assertion that a straight run charges no elbow, that an L-shaped run charges exactly one ninety, that a bigger diameter costs more equivalent feet than a smaller one. There is a long four-inch run that must trip the budget warning, a 240-volt machine on a 120-volt panel that must error, and a clean 240-volt hookup that must not. All of it folds into the harness alongside the geometry, the clearance checker, and the flow tracer. Every assertion green, at the usual hash.

## Honest about the edges

The dust budget is a rule of thumb, a diameter-based ceiling, not a full static-pressure calculation against a fan curve. It is conservative on purpose, and I have said so in the notes rather than dressing it up as more than it is. Runs auto-route with a single elbow for now; hand-routing a duct with three bends around a beam is a later feature, though the math to score it already exists. And the electrical side buckets load rather than assigning individual circuits, which is the next place to sharpen it.

Four stations lit of eight. The floor plans, checks its own clearances, traces its own traffic, and now runs its own ducts. What is left is mostly the bookends: drawing real walls at one end, and printing a proper plat at the other.

Make. Hack. Learn. Share. Repeat.
