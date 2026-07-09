title: BAYPLAN learns that clearance has a height
date: 2026-07-08
tags: field-instruments, workshop, tradigital
status: draft

---

Here is a thing that is true in a real shop and was false in BAYPLAN until this week: a table saw's outfeed can run right over the top of a low tool cabinet, and that is fine. The board slides out at table height, thirty-four inches off the floor. The cabinet is thirty inches tall. The board passes over it. Nobody who has ever worked wood would call that a conflict.

BAYPLAN called it a conflict. Every version until this one read the floor as if it were a single flat plane, so any two things whose outlines touched on the plan lit up as a problem, whether one was a spinning blade path at eye level or a storage bin you could rest your coffee on. The clearance checker was working in two dimensions when the shop lives in three.

## Clearance has a floor and a ceiling

So clearance zones now have height, or more precisely, they have a band. A clearance zone is protected from some height up to the ceiling. A feed lane's band starts at deck height, because that is where the wood travels; below that, the space is free to hold something short. An operator's standing zone has no floor to its band at all, it runs from the ground to the ceiling, because a person occupies the whole of it and you cannot tuck a cabinet under someone's feet.

A machine, meanwhile, occupies the space from the floor up to its own height. And now the check is simple and honest: a machine only conflicts with a zone if the two bands actually overlap in the vertical. Put a sixteen-inch benchtop unit under a forty-inch feed lane and the bands miss each other, so there is no flag. Put a sixty-six-inch floor drill press in that same spot and its band punches straight up into the lane, and the tool flags it, correctly, because a drill press in your outfeed is a board in the face.

## What did not change, on purpose

Two machines still cannot occupy the same patch of floor, no matter how short either one is, because both bodies start at the ground and their bands always meet. A blade path, a lathe's swing, a welder's spark standoff, all the zones that protect a person rather than a board, still run floor to ceiling and still catch anything that enters them at any height. Height forgiveness applies exactly where it should, to the space above a low obstruction, and nowhere it should not. The tests say so out loud: overlapping bodies still error, and a short machine shoved into a full-height hard zone still errors, even as a short machine under a feed lane now passes clean.

## Small change, honest change

This was a small edit to the code and a real correction to the model. It also forced me to fix a sentence I had written months ago in the conventions document that quietly described the height field backward, saying a zone was clear "up to" a height when what I meant, and what the examples all assumed, was that the zone was protected from that height on up. The code is now right and the words now match the code, which is the only state worth shipping in.

Five assertions guard the new behavior, folded into a harness that now runs sixty-one checks across the whole instrument, from the geometry math to the printed plat. All green.

The floor plans, argues, traces, wires, issues, and now it argues in three dimensions instead of two. What is left is to let you draw the walls yourself.

Make. Hack. Learn. Share. Repeat.
