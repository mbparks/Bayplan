title: BAYPLAN, or planning the floor the way the floor actually works
date: 2026-07-08
tags: field-instruments, workshop, tradigital
status: draft

---

Every shop layout tool I have ever tried treats a machine as a rectangle. Drop the rectangle, rotate the rectangle, tile the rectangles until they stop touching. And every one of them is wrong the moment you turn on a table saw, because the thing that governs where a table saw can live is not its cabinet. It is the sixteen feet of clear runway you need to rip a sheet of plywood without the offcut landing in the bandsaw.

So the newest Field Instrument, number 075, is called BAYPLAN, after the stowage diagram a ship's mate draws to pack a cargo hold. It plans the floor around the working halo of each machine, not just its footprint.

## Footprints lie

The idea the whole instrument turns on is small and, once you have lived it, obvious. A machine carries clearance zones, and those zones have opinions. A table saw's infeed and outfeed want ninety-six inches each so a full sheet can pass. A lathe wants a hard, uncrossable arc where the outboard blank swings. A welding table wants a spark standoff that no combustible may enter. A jointer wants its infeed and outfeed along the bed, not the front.

The trick that makes this layable-out rather than a wall of red warnings is a three-value rule on every zone. Hard zones may never be occupied, and the tool refuses to let anything sit in a blade path or a spinning arc. Soft zones should be clear but only warn, because two operator stations you never use at once can share space and you know that better than any checker. Shared zones may legitimately overlap the same kind of zone on a neighbor, which is how a saw's outfeed and a jointer's walk space coexist without a fight. That one distinction is the difference between a tool that helps and a tool that nags.

## What shipped

This first release is a scaffold, and I want to be honest about that word. It is not the finished instrument. It is the foundation with the hard parts already load-bearing.

The geometry core is real and tested: the math that projects a clearance strip off a named edge, the point-in-arc test for swings and door arcs, and the transform that rotates and mirrors a machine and its whole halo with it. That mirror transform is the one I made the test suite lean on hardest, because a flipped machine whose swing arc is silently wrong is exactly the kind of bug that passes a glance and fails on the bench. Twenty-one assertions, all green, runnable in the browser at the hash.

There is a built-in library of seventeen machines, from cabinet saw to CNC to welding table, each with a real footprint and its real halo, generated from a single script so the numbers stay honest and in one place. And there is a plat that draws it, night drafting-table by default, with a proper title block and a north arrow in the corner where a drafting sheet keeps them.

## What did not ship, on purpose

You cannot drag a machine yet. Conflict checking is not wired, though the geometry to do it is sitting right there and tested. Material flow and the utilities graph, the two overlays that will eventually turn this from a picture into an instrument, are specified down to the schema and scheduled but not built.

I am shipping the scaffold anyway because the shape of a thing is worth getting right before you fill it, and because a foundation you can run and test beats a pile of intentions. The station arc is written, eight stops from empty floor to issued plat, and this release lands the middle of it.

Next up is the part everyone actually wants: picking a machine off the shelf, setting it on the floor, and watching the halos light up when you put it somewhere it cannot go.

Make. Hack. Learn. Share. Repeat.
