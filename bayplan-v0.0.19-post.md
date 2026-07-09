title: BAYPLAN writes your shopping list
date: 2026-07-08
tags: field-instruments, workshop, tradigital

status: draft

---

Here is the thing about a good plan: at some point you have to go buy the stuff. And the tool already knew everything you needed to know to write that list. It knew how many outlets and what kind, because you placed them. It knew how long every wire run was and what breaker it hung on, so it knew the gauge. It knew every foot of duct and every elbow, every foot of air line. It was all sitting right there in the drawing, and you were going to count it by hand anyway. So now it counts it for you.

## The takeoff

There is a Takeoff button, and it does exactly what the word means to anyone who has estimated a job: it takes the quantities off the drawing. Press it and you get a list.

Outlets, by type, so many 120-volt twenty-amp, so many 240-volt fifties. Breakers, by size and by pole, because a 240 eats two slots and a 120 eats one and the panel only has so many. Copper cable, grouped by gauge, and this is the part I am proudest of, because the tool sizes the wire itself. A twenty-amp circuit wants twelve-gauge, a fifty wants six, and it knows that from the breaker it already assigned, so it just walks every run, reads the breaker, picks the gauge, and adds up the feet. Then it pads each number by fifteen percent for the slack you leave at every box and the tails you strip and waste, and rounds up to the nearest five, so the number on the list is the number you actually buy, not the number that leaves you eight inches short on the last pull.

Then the duct, by diameter, with a foot count and a tally of elbows, because elbows you buy one at a time, and a blast gate for every branch. The air line, its footage and its elbows. And the equipment, the panel and the collector and the compressor, counted. Lengths come out in whatever units you have the tool set to, feet or meters, same as everything else.

There is a Copy button that drops the whole thing to your clipboard as plain text, so it goes straight into an email to the supply house or a note in your pocket. I was careful about what it does not claim, though. It counts what the drawing shows: outlets, breakers, wire, duct, gates, air line, boxes of equipment. It does not pretend to know your couplings and your connectors and your straps and your staples, because those depend on how you run it, and a list that guesses at those is worse than a list that leaves them to you.

## Built on what was already there

None of this needed new information. The wire gauge came from the breaker sizing that was already in the electrical, the one that groups outlets per the code. The run lengths came from the same geometry the plat draws. The elbows are just the corners in a run, counted. That is the quiet payoff of having built the utilities as a real typed graph instead of freehand lines, all the way back: when you finally want a bill of materials, the materials are already described, and the list is a matter of adding them up.

Five new checks: that the gauge follows the breaker, that outlets and equipment tally correctly, that cable groups by gauge with its slack, and that duct comes out with its blast gates. A hundred and thirty checks now, green, and the drag fix still holds.

The plan tells you what to build, where to put it, whether it clears, how the air and the dust and the power get to it. And now, when you are ready, it tells you what to go buy.

Make. Hack. Learn. Share. Repeat.
