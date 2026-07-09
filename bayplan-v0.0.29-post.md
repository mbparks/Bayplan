title: BAYPLAN checks whether you can actually get around the shop
date: 2026-07-08
tags: field-instruments, workshop, tradigital

status: draft

---

TRIM has been guarding the space around each machine for a long time now. The halo of working room, the operator's stance, the outfeed a saw needs, the swing of a lathe, all of it checked so nothing crowds anything else. But there was a whole dimension it never looked at. Not the room around a machine, the paths between them. Can you actually walk from the door to the saw. Can you carry a sheet of plywood there without turning it sideways and skinning your knuckles. Is the main aisle wide enough to move around while a cut is running. That is the question a shop lives or dies by, and now the tool asks it.

## The walkability map

Hit Egress and the floor lights up. Not the machines, the space between them, shaded by how wide it is. Red where it pinches down tight, amber in the middle, green where it opens up. It is the open floor made visible, and the tight spots you walk past without noticing jump right out. There is the gap behind the jointer that looked fine on paper and turns out to be eighteen inches. There is the corner you have to sidle through.

Underneath, the tool floods the floor from every door, the way you actually move through a room, and works out what it can reach. At a walking width, about three feet, and at a material width you can set, four feet by default for a sheet of goods. Then it tells you plainly. Every machine you can reach on foot, and any you cannot, outlined in red right on the map. The aisle width that serves the whole shop, the widest path that still gets to every tool. The narrowest door, because a forty-eight inch sheet does not fit through a thirty-two inch door no matter how clear the floor is.

## How it thinks about width

The honest part is how it measures a corridor. It samples the floor on a grid and, for every open spot, works out how far it is to the nearest obstacle or wall. Twice that is how wide the passage is right there. Then it floods from the doors through everything wide enough, following the middle of the aisles the way water finds the channel. A machine counts as reachable if that network of good-width paths comes up to it. Two things had to be right for this to work and took a couple of passes to get there: the doorway itself, which is narrow by nature and was choking the flood until I taught it to step just inside to the first spot wide enough, and the machine you are walking up to, whose edge is always tight, so the network reaches out to it rather than demanding full width right at the tool.

It feeds the readiness list, of course. A machine with no walking path is an error on the punch list. One you can reach on foot but not with material is a warning. A door too narrow for a sheet gets flagged. So the aisles join everything else you clear before install.

And I will say what it is: a planning estimate on a grid, working off the footprints, not a stamped egress analysis. It does not know about occupant loads or travel distances or how a door swing might block a path. It is the tool that shows you the dark tight corner while you can still slide a machine over six inches and open it up. Eight checks on the geometry, and a hundred and sixty-nine now, green.

Lay out the machines, then walk the floor before you build it. Now the drawing walks it for you.

Make. Hack. Learn. Share. Repeat.
