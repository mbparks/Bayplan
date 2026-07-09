title: BAYPLAN watches the wood walk
date: 2026-07-08
tags: field-instruments, workshop, tradigital
status: draft

---

There is a rule of thumb in shop layout that nobody writes down but everybody who has stood at a table saw at the wrong end of a long day knows in their spine: the machines should be arranged in the order the wood moves through them. Rough stock comes off the rack, gets flattened on the jointer, thicknessed on the planer, cut to length, joined, assembled. If your floor makes the wood walk backward, you walk backward with it, all day, carrying boards.

The last two releases of BAYPLAN taught it to place machines and to check their clearances. This one teaches it to watch the wood walk.

## Trace the path

There is a new mode. Click New flow, then click your machines in the order stock passes through them. Each click snaps to the nearest work point on the machine you clicked, its infeed or its outfeed, so the path connects where the board actually enters and leaves, not at some abstract center. A colored line grows across the floor with little arrows showing which way the material travels. When you are done, you are done.

You can lay more than one flow. Hardwood takes one route, sheet goods another, and each gets its own color. Undo the last point if you misclick. The whole thing snaps to the work points I built into the machine library back at the start, which is a quiet payoff for having defined those points months before there was anything to snap them to.

## The numbers that matter

A path is not just a picture, it is a measurement. For every flow, BAYPLAN now reports three things.

Travel distance, in feet, because a layout that looks tidy can still march your stock a country mile. Backtracks, the count of legs where the material doubles back against the overall direction of the line, which is the single most useful number here, because a backtrack is a place where two people carrying two boards are about to meet in a doorway. And crossings, the count of places where one flow's path cuts across another's, because where paths cross, traffic collides.

None of these are stored. They recompute every time you nudge a machine, which means you can drag the planer three feet to the left and watch the backtrack count drop to zero in real time. That is the whole promise of the thing: change the floor, and the floor tells you immediately whether you made it better.

## Tested at the seams

The metrics are the substance of this release, so they carry the tests. There is an assertion that a straight run reports no backtrack, one that a deliberate reverse leg reports exactly one, one that two crossing paths are detected and two parallel ones are not, and one that a click near the outfeed snaps to the outfeed and not the infeed. Sixteen assertions across the routing work, folded into the harness that already guards the geometry and the clearance checker, all green, at the usual hash.

## Still to come

The backtrack measure uses a flow's net direction, so a path that loops back exactly to where it started cannot report a backtrack, an honest corner case I have written down rather than papered over. Machines without defined work points route through their center for now. And the big one still ahead is SERVICES, the utilities layer, where the dust collector and the electrical panel stop being furniture and start being a graph that knows whether your longest duct run will actually pull chips.

But the floor plans, checks itself, and now traces its own traffic. Three of the eight stations are lit. The wood is being watched.

Make. Hack. Learn. Share. Repeat.
