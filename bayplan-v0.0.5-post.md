title: BAYPLAN issues the plat
date: 2026-07-08
tags: field-instruments, workshop, tradigital
status: draft

---

A drawing you cannot compare against and cannot print is a sketch, not a plan. For four releases BAYPLAN has been a very good sketch: it placed machines, checked their clearances, traced the flow of stock, ran the ducts. All of it lived on one screen, in one arrangement, and the moment you left it, it was gone. This release gives it the two things that turn a sketch into a plan you can actually hand to someone. It can hold two ideas at once, and it can put one on paper.

## Two floors, side by side

There is a scenario switcher in the top bar now. Hit plus and BAYPLAN clones your current floor into a proposed one, and you can shove machines around the copy while the original sits untouched, waiting. When you want to know whether the new arrangement is actually better or just different, hit Compare.

You get both floors drawn next to each other, conflicts and all, and underneath them a table that does the arithmetic you would otherwise do in your head and get wrong. How many machines moved. How many were added or pulled out. TRIM errors in each. Utility warnings in each. Total material travel, in feet, for each. The whole point of a proposed layout is the word "versus," and now the tool says it out loud: this many conflicts here, that many there, this far to walk here, that far there. You stop guessing which floor is better and start reading it.

## On paper, properly

And then there is Print. Not a screenshot of the dark interface, but a real plat: white ground, black linework, the whole floor drawn true to size, with the things a drawing needs to be a drawing. A title block in the corner with the project, the facility, the scale, the revision, the date, and the name of whoever drew it. A north arrow. A scale bar showing a known two feet, so the sheet still means something after a copier resizes it. A legend, so the person holding it knows what the red halo and the tan duct and the dashed electrical line are saying.

That title block is the last thing on a list I wrote months ago, back when BAYPLAN was nothing but a data model and a set of intentions. Scale, north arrow, legend, revision. Every one of those was a promissory note to myself, and this release pays the last of them.

## The arc is lit

There were eight stations in the plan from the start. Sound the floor, manifest the machines, define their envelopes, stow them, trim the conflicts, route the flow, run the services, issue the plat. As of this release, all eight are on the board. The instrument does the whole job now, empty room to printed sheet.

I want to be honest that lit is not the same as finished. The floor is still a plain rectangle, because a proper wall-drawing tool is still ahead, and until it lands there are no doors to swing and no columns to work around. The clearance checker still reads the world flat and ignores the height field, so it frets about a duct passing over a low cabinet as though the cabinet reached the ceiling. Those are real, and they are written down. But they are refinements to a thing that works, not holes in a thing that does not.

Every assertion in the harness still passes, now including the ones that prove a duplicated scenario is truly independent, that the compare table counts moved and added and removed machines correctly, and that the printed sheet carries its title block and its legend. Green, at the usual hash.

The floor plans, argues, traces, wires, and now issues. It has been a long walk from a JSON schema to a sheet you can tack to the shop wall, and here we are, at the sheet.

Make. Hack. Learn. Share. Repeat.
