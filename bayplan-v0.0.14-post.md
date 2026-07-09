title: BAYPLAN still could not drag, and the real reason was hiding one level up
date: 2026-07-08
tags: field-instruments, workshop, tradigital

status: draft

---

Last time I wrote up a drag bug, explained it with some confidence, fixed it, wrote a test, and shipped it. And it still did not work. The person testing it told me, again, that they could not move a machine or a corner, and they were right, and I was wrong to have been so sure. So this is the second entry on the same bug, which is embarrassing in exactly the way that is worth being honest about.

## The first fix was real but incomplete

Last time I moved the mouse listeners off the drawing, which gets rebuilt constantly, and onto the stage that holds it, which does not. That was a genuine bug and a genuine fix, and my test proved it. But my test proved it with a pretend mouse and a pretend coordinate system, an identity, one-to-one mapping from screen to drawing. It confirmed the part I had reasoned about and quietly assumed the rest.

The rest is where the actual bug lived. When you click, the tool has to turn that screen position into a spot on the shop floor, and it was doing that by asking the browser for the drawing's coordinate transform through a function called getScreenCTM. That function is correct almost always. It is not correct when something above the drawing in the page uses a particular layout mode called display:contents, which the app's root does, because it makes an element vanish as a box while keeping its children. In that situation the transform comes back subtly wrong, and every click lands somewhere other than where you clicked. So the machine you pressed on was never the machine the tool thought you pressed on, the hit-test found nothing under your finger, and no drag ever began. Machines and corners failed identically because they both start from that same wrong answer to the question "where did they click."

## The second fix does not ask that question

So the tool no longer uses getScreenCTM at all. It asks the drawing for its plain rectangle on the screen, which every element will tell you correctly regardless of what layout tricks sit above it, and it does the small bit of arithmetic to undo the centering-and-scaling itself. It is a few more lines and one fewer thing that can lie to me. And this time the test drives the whole thing through a fake viewport that is offset and scaled and letterboxed, not a tidy one-to-one, so it actually exercises the arithmetic that was broken. A click at a known spot round-trips back to the exact floor coordinate it should, and then a full press-drag-release lands the machine where it was dragged. For good measure the stage now also tells the browser not to treat a drag as text selection, which is the other thing that quietly eats a drag.

## While I was in there

I also pulled the title block off the working view. It was drawn in the corner of the plat on screen, the project name and scale and sheet, which is exactly right on a printed sheet and just clutter while you are pushing machines around. It is gone from the screen now, replaced by a small north arrow so you still know which way is up, and it still prints in full on the actual plat where it belongs.

The lesson I am taking, again and more firmly: a test that mocks the thing that is broken cannot catch the break. The first test mocked the coordinate system and so it could never have failed. The new one refuses to, and fails against the old code the way a good test should. My thanks, again, to the person who kept telling me it did not work, because a real hand on a real machine found in one try what all my green checks were built to miss.

Make. Hack. Learn. Share. Repeat.
