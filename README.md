# BAYPLAN

**Field Instrument #075.** A workshop floor planner that plans for how a shop actually works, not just where the boxes sit.

A bayplan is the stowage diagram for a ship's cargo bays. This one stows a workshop: scale-accurate, imperial, snap-to-grid, and single-file HTML in the local-first fleet posture. The whole plan is one JSON document that exports and imports cleanly, no server required.

## What makes it an instrument, not a floor planner

Three things, all in the data model rather than the UI:

1. **Clearance envelopes, not just footprints.** Every machine carries its real working halo: a table saw's infeed and outfeed, a lathe's outboard swing, a welder's spark standoff. Overlap two halos and the checker flags it, with a hard / soft / shared rule so a table saw's outfeed can legitimately share an aisle while a blade path never can.
2. **Material flow as a first-class overlay.** Draw the path stock takes from rack to assembly; the tool derives backtracking and crossing traffic.
3. **A typed utilities graph.** Electrical, dust, air, and data as a graph, so duct runs get measured and circuit loads roll up instead of being drawn as dumb lines.

## Status

v0.0.7. The full eight-station arc is now functional end to end, and SOUNDING is the capstone. You can reshape the room: edit its dimensions, drag boundary corners, and add or remove corners for L-shaped floors and bump-outs. You can place features: columns (solid obstacles), doors (with swing arcs), and windows. Door swings and columns check against your machines through the same TRIM engine, so a machine blocking a door or landing on a post is flagged, using the same arc primitive the lathe swing uses. Everything from the earlier releases stands: placement (STOWAGE), clearance checking with vertical `minHeight` bands (TRIM), material flow (ROUTING), the utilities graph (SERVICES), and scenario-compare with a printable plat (PLAT). All three original data-model open items are closed.

## Repository layout

```
bayplan.html                     the instrument (open it, no build step)
bayplan-seed-library.json        built-in machine library (17 machines)
build_seed.py                    generator; source of truth for the seed
bayplan-data-model.md            full data-model spec and station arc
bayplan-envelope-conventions.md  local frame + default clearance depths
README.md
LICENSE
```

The seed embedded in `bayplan.html` is spliced in from `bayplan-seed-library.json` at scaffold-build time, so `build_seed.py` remains the single source. To regenerate: run `python3 build_seed.py`, then re-splice.

## Running it

Open `bayplan.html` in a browser. It runs from `file://` with no server, no network, and no build step. On first load it shows a small demo shop so the plat is not blank.

Editing: click a machine to select it, drag to move (snaps to one inch, hold Alt for free movement). With something selected, R rotates ninety degrees (Shift+R the other way), M mirrors, L locks, Delete removes, and arrow keys nudge by the grid. All of the same actions are available as buttons in the Selection panel for touch. Add machines from the shelf in the sidebar.

Routing: in the Material flow panel, click New flow, then click machines in the order stock moves through them. Each click snaps to the nearest work point on that machine (its infeed or outfeed). The panel shows travel distance and backtrack count per flow, and a crossing count across flows. Undo point removes the last waypoint, Done finishes. Backspace undoes and Escape finishes from the keyboard.

Utilities: in the Utilities panel, click Open utilities, then add a dust collector and an electrical panel. Drag each node where it belongs, then click Wire all to connect every machine to its nearest collector (dust) and panel (electrical). The panel reports dust-run effective lengths, connected electrical load, and any warnings; drag a node and the numbers update live. Select a node to remove it. Escape finishes.

Scenarios and plat: the scenario switcher in the header lets you keep more than one layout. + Scenario duplicates the active one (as Proposed), so you can rearrange a copy without losing the original. Compare shows the two side by side with a delta summary (added, removed, and moved machines, plus TRIM, utilities, and flow figures for each). Print issues the active scenario as a plat with a full title block, scale bar, north arrow, and legend, on a clean white sheet.

Room: click Room to edit the facility. Set the room's dimensions in inches, drag the corner handles to reshape it, or use Add corner and Remove corner for L-shapes and bump-outs. Add columns, doors, and windows, then drag them into place; doors and windows rotate with R (or the panel buttons). Door swings and columns are checked against your machines by TRIM. Escape finishes.

## Tests

The test harness is browser-runnable at `bayplan.html#test`, seeded with the built-in library as its fixture. It covers the geometry core (bounds with offset anchors, edge projection, point-in-polygon, the bearing convention, point-in-arc, the mirror transform, the placement transform, segment intersection, and polygon overlap), the TRIM checker (the full severity-interaction matrix, the vertical-band `minHeight` logic that lets a short machine sit under a high feed lane while a tall one is caught, plus end-to-end scenarios), ROUTING (work-point snapping, travel distance, backtrack detection, and crossing detection), SERVICES (elbow-equivalent inference, dust-run budget warnings, and the electrical rollup with voltage reachability), PLAT (scenario independence after duplication, delta detection, and the printable sheet), and SOUNDING (boundary resize and add/remove corner, plus column-obstacle, door-swing, and window conflict behavior). The release gate is green only when every assertion passes.

## Local frame convention

Origin at the machine anchor, +y back (away from the operator), +x to the operator's right. Footprint edges are named front (min y), back (max y), left (min x), right (max x). Arc angles are degrees clockwise from +y. See `bayplan-envelope-conventions.md` for the full convention and the default clearance depths per machine category.

## Known Limitations

- Boundary editing is by corner handles and dimension entry. There is no free-form click-to-draw wall tool, and corners snap to one inch. Angled or curved walls are approximated by adding straight-edged corners.
- Features are placed by button and dragged into position; they do not snap to the nearest wall automatically, so a door or window can be dragged into open floor. Its swing and conflict logic still work wherever it sits.
- Door swing is modeled as a quarter-circle arc from the hinge, treated as a full-height hard zone. It does not model leaf thickness or a partial-height opening.
- Scenario compare pairs the active scenario against the first other scenario. With three or more scenarios there is no picker yet for which two to compare.
- Printing relies on the browser's print dialog and its page-size and margin handling. The plat scales to fit the sheet; there is no fixed paper-size or multi-page tiling.
- No undo for placement. Deleting or moving a machine is immediate; recovery is by re-adding or dragging back. (Flow routing has an undo for the last waypoint.)
- Flow waypoints snap to a machine's work points, or to its anchor when the machine has no work points defined. Only the flow-relevant machines in the seed (saw, jointer, planer, bandsaw, miter saw, CNC) carry work points; everything else routes through its anchor.
- Backtrack detection uses the net start-to-end direction of a flow. A flow that returns exactly to its start (zero net travel) cannot report backtracks by this measure; genuine process flows have a net direction, so this is a corner case rather than a real limit.
- The utilities graph auto-routes runs: dust as a single orthogonal L (one elbow), electrical as a straight line. There is no manual duct routing with multiple bends yet, so a real run with several elbows is under-counted. Effective-length and elbow math is in place for when manual routing lands.
- The dust budget is a per-diameter rule-of-thumb ceiling, not a static-pressure calculation against the collector's fan curve. It is deliberately conservative and tunable; a true SP model is a future refinement.
- Electrical rollup buckets load by voltage and checks 240V reachability and total load against the panel main. It does not yet assign individual circuits or check per-breaker load.
- QUARTERMASTER seed import is designed (provenance fields are in the schema) but not implemented.
- Annular arcs (with an inner radius) are supported in the model and sampled correctly, but no seed machine exercises one yet.
- The plat export produces the JSON document, not a printable sheet. A full printable plat with legend and revision block is a PLAT-station item, still open.
- Import validation is shallow. It checks for a facility and a scenarios array; it does not yet validate the full schema or migrate older schema versions.

## Roadmap

BAYPLAN runs an eight-station arc: SOUNDING (set the floor), MANIFEST (build the library), ENVELOPE (define the halos), STOWAGE (place), TRIM (balance conflicts), ROUTING (material flow), SERVICES (utilities graph), PLAT (compare and issue). As of this release all eight are functional end to end: you can shape a room and place features, build the library and its halos, stow machines, trim their conflicts in three dimensions, route the flow, run the services, and compare and issue the plat. The three data-model open items are closed. Future work is depth rather than breadth: a free-form wall tool, wall-snapping for features, manual multi-bend duct routing, per-circuit electrical assignment, a compare picker for three-plus scenarios, and undo. See the station arc in `bayplan-data-model.md`.

## License

BAYPLAN is licensed under the GNU General Public License, version 3.0 (GPL-3.0).

This program is free software: you can redistribute it and modify it under the terms of the GPL as published by the Free Software Foundation, either version 3 of the License or any later version. It is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY, without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the LICENSE file for the full text.
