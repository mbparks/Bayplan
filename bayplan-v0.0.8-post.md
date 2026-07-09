title: BAYPLAN learns to take it back
date: 2026-07-08
tags: field-instruments, workshop, tradigital

status: draft

---

Every tool that lets you make a change should let you unmake it. For eight releases BAYPLAN did not. You dragged a machine, and it was dragged. You deleted a flow, and it was gone. You could put it back by hand, but the tool had no memory of where things had been a moment ago, and that is a small quiet anxiety that sits under every edit: do not slip, because there is no net. This release strings the net.

## One choke point, not twenty

The tempting way to build undo is to teach every single action how to reverse itself. The drag remembers where it started, the delete remembers what it deleted, the rotate remembers the old angle, and on and on, twenty little bespoke reversals that each have to be right. That is twenty places to introduce a bug, and the bug you get is the worst kind: an undo that half-works, that puts most of the state back but forgets one thing, so you can no longer trust the button at all.

BAYPLAN keeps the whole plan as one plain document, so I took the other road. The tool snapshots the entire document after every change and keeps a stack of those snapshots. Undo is just stepping back down the stack; redo is stepping back up. There is no per-action reversal logic to get wrong, because there is no per-action logic at all. The state you had is the state you get back, exactly, because it is literally the same state, saved.

The snapshots record at a single point, the moment the drawing redraws, so I did not have to thread a save call through every one of the twenty ways you can change a plan. Three details make it feel right rather than mechanical. A drag is one step, not one step per pixel, because the recorder holds its breath while you are dragging and takes the picture when you let go. A click that changes nothing adds nothing, because an identical snapshot is recognized and dropped. And walking back and then striking off in a new direction throws away the branch you abandoned, the way every editor you have ever used behaves, so redo never offers you a future you already chose against.

## What it costs and what it does not

Holding a full copy of the plan for every step could get heavy, so each snapshot quietly drops the built-in machine library, which never changes, and reattaches it on the way back. The history caps at eighty steps and lives only for the session; save the plan and reopen it and you start clean, because the undo stack is a working convenience, not part of the document. That felt like the honest line to draw. The file on disk is the plan; the history is just the scaffolding around this afternoon's work on it.

The button sits in the header, greys out when there is nothing to undo, and answers to the keystroke your hands already know. It works the same whether you are stowing machines, running ducts, shaping walls, or laying out doors, because it does not care what you changed, only that the document is different than it was.

Nine new assertions guard it: that an edit becomes undoable and a fresh plan does not, that undo and redo land on the exact states they should, that a no-op is deduped, that nothing is recorded mid-drag, that a new edit after an undo clears the redo tail, and that the library is stripped from a snapshot and restored from it. The harness now runs seventy-nine checks. Green.

BAYPLAN could already draw your shop, halo its machines, argue about clearances in three dimensions, trace the wood, run the services, hold two layouts side by side, and print the sheet. Now it can also let you be wrong for a second and take it back. That is not a feature so much as a permission, and every good drawing table grants it.

Make. Hack. Learn. Share. Repeat.
