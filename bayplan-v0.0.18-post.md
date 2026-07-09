title: BAYPLAN speaks metric now, and the wires bend
date: 2026-07-08
tags: field-instruments, workshop, tradigital

status: draft

---

Two smaller things this release, both of them the kind of gap you do not notice until someone bumps into it. One is that the whole tool only spoke in feet and inches. The other is that the electrical wires were the only lines on the plat you could not route by hand.

## Feet and inches, or meters and centimeters

There is a toggle in the header now, in and cm, and flipping it changes the language the whole tool speaks. The rulers along the edges relabel themselves in meters. The measuring tape reads out in centimeters and meters instead of feet and inches. The width and depth boxes on a machine, the room-dimension fields, even the unit stamped on the printed title block, all of it follows the switch.

The important part is what does not change: the drawing itself. Everything inside the tool is still measured in inches, exactly as it was, and the metric display is just a translation laid over the top. So you can flip to centimeters to check a clearance against a metric spec, flip back to inches to keep laying out, and nothing drifts or rounds off in between, because the numbers underneath never moved. The choice rides along in the saved file, so a plan opens the way you left it. I left the things that have their own stubborn units alone, though. A four-inch dust port is a four-inch dust port whether you think in metric or not, and a twenty-amp breaker is twenty amps, so ports and airflow and amperage and voltage stay in the units the trade actually quotes them in.

## The wires bend too

The dust lines could bend. The air lines could bend. But the electrical runs, alone among the three, could only go straight from the panel to the thing they fed, cutting across the floor through whatever happened to be in the way. That was just an oversight, and it is fixed. Select a wire and it works exactly like a duct now: click along it to drop a bend, drag the little diamonds to steer it, straighten it back if you overdo it. A circuit can follow the wall and turn the corner the way it will actually be pulled, and it still wears its circuit letter and its voltage color and its amperage dashes while it does. It was a handful of lines to let electrical share the routing the other two already had, which is the nice thing about having built the bending once and built it general.

Five new checks: that lengths format right in both imperial and metric and that centimeters convert cleanly back to the inches underneath, and that an electrical run takes its bends when you give it waypoints and stays a clean straight shot when you do not. A hundred and twenty-five checks now, green, and the drag fix still holds through its test viewport.

Small ones, but the tool fits a few more hands today. The ones who think in millimeters, and the ones whose panel is on the far wall from everything it feeds.

Make. Hack. Learn. Share. Repeat.
