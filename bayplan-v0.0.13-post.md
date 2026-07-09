title: BAYPLAN picks its comparisons and prints to scale
date: 2026-07-08
tags: field-instruments, workshop, tradigital

status: draft

---

Two small things stood between PLAT and being finished, and they were the two things I kept bumping into every time I used it. Compare only ever showed you the current layout against the first other one, which is fine until you have three ideas going and want to hold the second against the third. And printing only ever fit the whole plat onto one page, which is fine until the shop is big enough that one page means the machines are the size of grains of rice. This release fixes both, and with it every item on the depth roadmap I wrote a dozen releases ago is crossed off.

## Pick your two

When you have three or more scenarios, Compare now gives you two dropdowns, left and right, and you choose which pair to hold side by side. Change either one and the plats swap, the delta table re-tallies, the added and removed and moved counts update. If you pick the same scenario on both sides it quietly bumps one of them to something else, because comparing a thing to itself is a very short conversation. With only two scenarios it does what it always did and skips the picker, because there is nothing to pick.

## Print like a drawing, not a thumbnail

The real work is in printing. There is a setup screen now. You pick a paper size, Letter on up through A3. You pick an orientation, or leave it on auto and let it work out which way round gives you fewer pages. And you pick a scale.

Fit to page is the old behavior, the whole plat on one sheet with its title block and scale bar and legend, good for tacking a quick overview to the wall. But now there are real architect's scales too: a half inch to the foot, a quarter, an eighth. Choose one and the tool stops trying to cram the shop onto one page and instead tiles it across as many pages as the shop actually needs at that scale. A big shop at a quarter inch to the foot might come out three pages wide and three deep, nine sheets, each one a true-scale window onto its patch of floor. Every sheet gets a caption along the top: the project, the scale, and which sheet it is, sheet five of nine, row two column two, so when they come out of the printer you can lay them edge to edge in the right order and read the whole floor at a size where you can actually see it. Set your print dialog to the same paper and turn off shrink-to-fit, and a foot on the floor is a quarter inch on the paper, measurably, the way a plan is supposed to be.

The trick under the hood is simpler than it sounds. The plat is already drawn once, in shop inches. Each page is just a window onto part of it, and a window onto part of an SVG is a one-line thing: you tell it which rectangle to show and how big to draw it. So every page is the same drawing, cropped to its tile and sized so that the scale comes out true. No re-rendering, no slicing geometry, just nine views of one picture.

Eight new assertions guard it: that a third scenario can be compared as an arbitrary pair, that the printable area subtracts its margins, that a big plat tiles into multiple pages and a small one stays on a single page, that auto orientation never picks the layout with more pages, and that the tiles together cover the whole plat with nothing falling off the edge. The harness now runs a hundred and six checks. Green.

That closes the list. Sound the floor, manifest the machines, envelope their halos, stow them, trim the conflicts in three dimensions, route the flow around the obstacles and know a loop when it sees one, run the ducts by hand and the circuits by breaker and check the airflow against the fan, hold any two layouts against each other, and print the whole thing to scale across as many sheets as the shop deserves. The instrument does the whole job now, empty room to a set of drawings you could hand to someone and build from.

Make. Hack. Learn. Share. Repeat.
