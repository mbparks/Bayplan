title: BAYPLAN stops being just my shop
date: 2026-07-08
tags: field-instruments, workshop, tradigital

status: draft

---

Here is the thing I have been quietly embarrassed about. For all the checking and routing and drawing this tool does, if you wanted to add a machine it did not already know, you had to open a Python file and edit a seed generator. Which is fine if you are me. It is a wall if you are anybody else. A shop-planning tool that only knows the machines I happened to type in is a tool for exactly one shop. So this release is the one that fixes that, and it is the one I think matters most.

## Define a tool, once

There is a + Machine button now. It opens a little workbench where you describe a machine the way you would describe it to a friend. Its name. What kind of thing it is. How big it is, width and depth. How much room it needs around it, and off which edges, the operator side, the infeed, wherever. Whether it draws power, and how much. Whether it has a dust port or an air fitting. How tall, how heavy. Fill that in, hit save, and it drops onto the shelf right next to the table saw and the jointer and everything else.

And from that moment it is a real machine. Not a second-class sketch, not a placeholder. It places, it drags, its clearance halo checks itself against the neighbors, it wires onto a circuit, material flow routes through it, it shows up in the takeoff and the panel schedule and the punch list, it prints. Everything the built-in tools do, your machine does, because under the hood it is built in exactly the same shape. I made sure of that. The builder writes the same kind of definition my generator writes, down to the geometry of the clearance zones and the work points the flow snaps to.

## It travels with the plan

Your machines are yours, and they stay with the drawing. They save when you save, they come back when you open, they ride along when you export the plan and when it autosaves in the background. Delete one you are not using and it is gone; try to delete one that is placed in a scenario and the tool stops you, because pulling a definition out from under a placement is the kind of quiet damage I built the whole archive-over-delete posture to avoid. And each custom tool is stamped as yours, kept distinct from the built-in roster, so there is never any confusion about what came from where.

I kept the first version honest about its edges. It makes rectangles, a width-by-depth footprint with square clearances, a centered dust or air port, work points front and back. That covers the great majority of shop machines. It does not yet do the odd-shaped footprints or a lathe's swept swing arc or multiple named work points, and you edit a machine by deleting and remaking it. Those are the seed generator's job for now, and they are on the list. But the wall is down. You no longer need me, or a text editor, to describe your own shop.

Fifteen checks on this one, the most of any single release, because getting a user-authored machine to behave exactly like a built-in through placing and checking and saving and loading is where the bugs hide. A hundred and seventy-three now, green.

BAYPLAN was always a tool for planning a shop. Now it is a tool for planning yours.

Make. Hack. Learn. Share. Repeat.
