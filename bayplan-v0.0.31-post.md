title: BAYPLAN can hand someone the drawing without handing them the tool
date: 2026-07-08
tags: field-instruments, workshop, tradigital

status: draft

---

There are two different things you might want to give somebody. Sometimes you want to hand them the whole workshop, editable, so they can move machines and try their own arrangement. That is the export, the plan file, and it has been there all along. But most of the time you just want to show them the drawing. The electrician who needs to see where the panel goes. The buddy helping you move the saw. The version of you six months from now who just wants to look. They do not need the editor. They need the picture. So now there is a way to give them exactly that and nothing more.

## Publish

There is a Publish button, and it bakes the whole plan into one HTML file. Open it in any browser, on any machine, and there is the plat: the machines, the clearance halos, the wiring, the ducts, the dimensions, the notes, the title block, all of it, laid out clean. A schedule of the machines underneath. A legend so the colors mean something. And if you have more than one scenario, tabs to flip between them. That is it. No editor, no buttons to break anything, no way to nudge a machine by accident. A drawing to read.

The nice part is that it is genuinely one file. It carries its own colors and its own fonts baked in, so it does not phone home for anything, does not need my stylesheet, does not need to be online. You can email it, drop it on a thumb drive, print it from the other person's laptop. It renders the same everywhere because it is the same rendering the printed sheet uses, just wrapped for a screen. There is no data hiding in it and no code that does anything but show you the plan.

## Read-only on purpose

I made it read-only deliberately, and kept it separate from the editable export. Those are two jobs and they should be two files. The plan file is for continued work, and it carries everything, including the custom machines you built. The published viewer is for handing over the drawing, full stop. It is a snapshot, so when the plan changes you publish a fresh one, the same way you would reprint a sheet after a revision. That is honest about what it is: a drawing, dated and done, not a live window into the tool.

I built the whole generator as a plain function that just returns the file's text, which meant I could test it properly without a browser in the loop, ten checks that it comes out as real self-contained HTML, embeds the drawing, resolves its own fonts, lists the machines, and carries none of the editor with it. A hundred and seventy-five now, green.

The tool has always been about keeping your data yours. This is the other half of that: being able to share the drawing freely, as a thing anyone can open, without giving up or complicating the plan itself.

Make. Hack. Learn. Share. Repeat.
