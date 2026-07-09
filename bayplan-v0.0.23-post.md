title: BAYPLAN hangs the lights and lets you hide your notes
date: 2026-07-08
tags: field-instruments, workshop, tradigital

status: draft

---

Two this time. One is a small mercy: the notes you can scribble on the plat can now be turned off. The other fills a real gap: the shop has lights, and until now the plan pretended it did not.

## Notes, on a switch

Notes are great right up until you want to show the drawing to someone without your margin scribbles all over it, or print a clean copy for the wall. So there is a switch now, right next to the Note button: Notes, on or off. Flip it off and every pinned note vanishes from the plat at once, and stays gone from the printed sheet and the takeoff PDF too, so the version you hand out can be the clean one. Flip it back and they are all right where you left them, because hiding is not deleting, it is just a view. And while they are hidden they are truly out of the way, you cannot accidentally grab one or nudge one, only the things you can see are the things you can touch.

## The shop has lights now

Here is the gap. The plan knew about your saw's power, your collector's circuit, your outlets, but the ceiling was dark. A shop is lit, and lighting is load, and load is circuits, and circuits are wire and breakers you have to buy. So light fixtures are a utility now. Drop a fixture on the plan, tell it its wattage, a forty-watt LED shop light by default, and it draws the little ceiling-light symbol you would expect, a circle with a cross.

And when you wire the shop, the lights wire like lights. They do not each get a home run like the big machines; they gang up on shared lighting circuits, the way a real lighting circuit carries a whole row of fixtures. The tool keeps them on their own circuits, separate from the receptacles and the machines, because that is how a panel is actually laid out, and it sizes them by the watts they actually pull, so dozens of LED fixtures ride one fifteen-amp circuit without breaking a sweat. They land in the panel total, they land on the circuit report, and if you hang a fixture with no panel to feed it, the tool says so.

Best part, and the reason this was not much code: the lights just fall into everything the electrical already did. They show up in the shopping list, counted by wattage, and their circuits and their cable are already in the breaker tally and the copper totals, because a light is just another load on the same typed graph as everything else. Teaching the takeoff to count fixtures was one more line; the wire and the breakers counted themselves.

Eleven new checks: that the notes hide and show on the plat and the printed sheet, that fixtures gang onto a single lighting circuit without overloading it, that a fixture with no panel is flagged, and that the takeoff counts the fixtures by wattage. A hundred and forty-seven checks now, green, and the drag fix still holds.

The drawing can be clean when you want it clean. And the ceiling is finally on the plan.

Make. Hack. Learn. Share. Repeat.
