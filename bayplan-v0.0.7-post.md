title: BAYPLAN gets its walls
date: 2026-07-08
tags: field-instruments, workshop, tradigital
status: draft

---

For six releases BAYPLAN worked in a perfect rectangle. Every shop it ever drew was a clean box, because the box was all it knew how to draw. Real shops are not boxes. They have a bump-out where the old chimney was, a structural post planted right where you wanted the assembly table, a door that swings inward across the exact patch of floor you were about to fill with a jointer. The first station in the whole arc is called SOUNDING, sounding the floor, taking the measure of the room before you put anything in it, and it was the last one I built. This release builds it, and with it the arc is whole.

## Shape the room

Click Room and the walls come alive. The corners become handles you can drag. Type a width and a depth and the room snaps to those dimensions. Add a corner and the longest wall gets a new joint you can pull out into an L, or a T, or whatever your actual building does. Remove a corner you do not need. It is not a full drafting program and I did not try to make it one; it is enough to describe the real footprint of a real shop, which is almost always straight walls meeting at corners, and that it does cleanly.

## Put the obstacles where they really are

Then there are the things in the room that are not machines. A column, drawn as a solid post, that your machines simply cannot occupy. A door, drawn with its swing, the quarter-circle the leaf sweeps as it opens. A window, marked on the wall. Drop them, drag them where they live, turn the doors and windows to face the right way.

And here is the part that makes them more than decoration: the door swings and the columns talk to the clearance checker. Park a bandsaw where the shop door opens and the floor lights up, because a door you cannot open is not a door. Set a machine on top of the lally column holding up the second floor and it flags, because you are not moving that column and the checker knows it. The door swing is drawn with the very same arc math that draws a lathe's outboard swing, which is a quiet satisfaction: I built that arc primitive four releases ago for spinning bowl blanks, wrote it carefully, tested it hard, and it turns out a door is just a slower lathe.

## The arc is whole

Eight stations were on the plan from the first sketch. Sound the floor. Manifest the machines. Envelope their clearances. Stow them. Trim the conflicts. Route the flow. Run the services. Issue the plat. As of this release every one of them does its job, and they do it together: you can draw a room with a post and a door in it, fill it with machines that know their own working halos, watch the checker catch a saw blocking the door in three dimensions, trace the wood through the floor, run the ducts and the circuits, hold a second layout beside the first, and print the whole thing on a clean sheet with a title block.

It has been a long build, and I want to mark that it did not wander. The data model I wrote at the very beginning described a door as carrying a swing arc that enters conflict checking exactly like a machine's clearance zone. That sentence sat in the spec for the entire build, a promise made before there was a single line of code, and this release is where the code finally grew up to meet it. When the spec and the thing agree at the end, you did the thinking in the right order.

Ten new assertions guard the room work, folded into a harness that now runs seventy checks over the whole instrument. All green.

The floor sounds, plans, argues, traces, wires, compares, and issues. The rectangle is gone. BAYPLAN can draw your actual shop now, posts and doors and all, and tell you where it will fight you before you move a single machine.

Make. Hack. Learn. Share. Repeat.
