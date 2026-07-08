title: BAYPLAN learns to say no
date: 2026-07-08
tags: field-instruments, workshop, tradigital
status: draft

---

The first cut of BAYPLAN could draw a shop but not change one. You could look at the demo floor, admire the halos, and do exactly nothing to it. A picture, not an instrument. This release fixes that, and in doing so it turns on the one feature the whole idea was for: the floor pushes back.

## Stow the floor

Pick a machine off the shelf in the sidebar and it lands on the floor. Grab it and drag, and it slides on a one-inch snap, or free if you hold Alt. Rotate it with R, flip it with M, lock it so a stray click cannot nudge it, delete it when you change your mind. On a touch screen the same moves live as buttons in a selection panel, because I have been bitten before by building keyboard-only controls into a thing I then wanted to use on a tablet at the bench.

None of that is remarkable on its own. Every floor planner lets you move a rectangle. The difference is what happens while you move it.

## The floor pushes back

Every time a machine moves, rotates, or lands, TRIM re-checks the whole floor. It walks every pair of machines, every clearance halo against every other, and asks a simple question with a not-simple answer: is this overlap a problem?

The answer runs on the three-value rule the model was built around. A hard zone, a blade path or a lathe swing, may never be occupied, so if a machine body or another hard zone lands in it, the footprint goes red and the conflict list names it. A soft zone, standing room, only warns, because you know your own workflow better than a checker does. And a shared zone, a feed lane or an assembly apron, is allowed to overlap other shared and soft zones, so a table saw's outfeed can run straight across the jointer's walk space without a single false alarm. That last case is the one I care about most, because it is exactly where lesser tools cry wolf until you stop believing them.

Push two machines together and watch the footprints bloom red. Slide one back and the red clears. Shove a machine through the wall and it tells you it has left the building. There is a tally in the corner that reads "clear" when the floor is honest and counts your errors and warnings when it is not.

## Tested where it matters

The severity matrix is the brain of this release, so it is the most heavily tested thing in it. Every cell of the interaction table has an assertion. Beyond the unit level, there are whole-floor tests: two machines stacked must report an error, a machine past the wall must report an error, a lone machine in open space must come back clean, and, the one that would embarrass me most to get wrong, a saw and a jointer sharing a feed lane must produce no error at all. Twenty-eight assertions, all green, runnable in the browser at the hash.

## What is still open

The checker is honest but not yet subtle. It does not read the height field yet, so a feed lane passing over a low cabinet is flagged as though the cabinet reached the ceiling. That is the next thing I will teach it. There is still only one room and one scenario, no doors to swing, no undo, and the two overlays that will make this a real planning instrument, material flow and the utilities graph, are still just schema and intent.

But it plans now. You can build a floor, and the floor will argue with you, and arguing with your floor before you pour the concrete is the entire point.

Make. Hack. Learn. Share. Repeat.
