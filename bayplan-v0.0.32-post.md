title: BAYPLAN comes out to the shop with you
date: 2026-07-08
tags: field-instruments, workshop, tradigital

status: draft

---

A shop-planning tool has a funny relationship with where you actually are. You do the real thinking at a desk, laying things out on a big screen. But the moment of truth comes standing in the empty bay with a tape measure, phone in your other hand, trying to see whether the drawing matches the concrete. And up to now, on that phone, in that bay, the tool was awkward. You could see the whole plat but never get close enough to a corner to work with it, and every time you tried, the browser fought you, zooming the page instead of the plan. This release is about that moment. It brings the tool out to the shop.

## Pinch, and it is where you need it

Now you pinch to zoom, the way everything else on a phone works. Spread two fingers and the plat comes toward you, right at the spot between your fingers, so you can drive into the corner by the door and see the eighteen inches you were worried about. Drag those two fingers and you pan around. Pull them together and it falls back. On a desktop the mouse wheel does the same, zooming toward wherever the cursor is pointing, and there is a little zoom control in the toolbar, minus and plus and a Fit button that snaps back to the whole drawing when you are done poking around.

I kept the gestures from stepping on each other. One finger, or the mouse, still does what it always did, picks up a machine and moves it, selects a thing, drags a handle. Two fingers is the pan-and-zoom. So there is no mode to switch, no button to arm. You just use it the way your hands already expect to.

## Under the hood, carefully

Here is the part I am quietly proud of, because it could have gone badly. The way this tool maps a tap on glass to a spot on the floor was hard-won. It broke twice, early on, in ways that took real digging to fix, and I have guarded that math ever since. Adding zoom meant touching exactly that machinery, which is the last place you want to be careless. So I did it the safe way: the drawing is still drawn once, in full, and zooming just changes which window of it you are looking through. The mapping from floor to screen never changes. Only the inverse, screen back to floor, learns about the window. Which means the drag that was so hard to get right did not have to change at all. It just works, zoomed or not, and I have the checks to prove the tap-to-floor round trip still lands true at any zoom.

The buttons got bigger on touch, too, with room for a thumb, and the plat stopped letting the browser hijack your gestures. Eight checks on the zoom math, a couple more on the clamps, and a hundred and seventy-seven now, green, with the old drag test still passing untouched.

That closes out this run of work: the drawing you can read on the wall, the checks that clear before you build, and now a tool that fits in your hand in the bay where the real questions get asked. Make the plan at the desk. Check it on your phone, standing in the space. That is the whole loop, and it finally closes.

Make. Hack. Learn. Share. Repeat.
