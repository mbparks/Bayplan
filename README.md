# BAYPLAN

**Field Instrument #075.** A workshop floor planner that plans for how a shop actually works, not just where the boxes sit.

A bayplan is the stowage diagram for a ship's cargo bays. This one stows a workshop: scale-accurate, imperial, snap-to-grid, and single-file HTML in the local-first fleet posture. The whole plan is one JSON document that exports and imports cleanly, no server required.

## What makes it an instrument, not a floor planner

Three things, all in the data model rather than the UI:

1. **Clearance envelopes, not just footprints.** Every machine carries its real working halo: a table saw's infeed and outfeed, a lathe's outboard swing, a welder's spark standoff. Overlap two halos and the checker flags it, with a hard / soft / shared rule so a table saw's outfeed can legitimately share an aisle while a blade path never can.
2. **Material flow as a first-class overlay.** Draw the path stock takes from rack to assembly; the tool derives backtracking and crossing traffic.
3. **A typed utilities graph.** Electrical, dust, air, and data as a graph, so duct runs get measured and circuit loads roll up instead of being drawn as dumb lines.

## Status

v0.0.4. Four of the eight stations are live: STOWAGE, TRIM, ROUTING, and now SERVICES. Beyond placing machines, checking clearances, and tracing material flow, you can now lay the utilities graph: drop a dust collector and an electrical panel, drag them into place, and wire every machine to its nearest node in one click. SERVICES then reports dust-run effective length (straight run plus inferred elbow equivalents) against a per-diameter budget, and rolls up electrical load with a 240V-reachability check. The v0.0.1 scaffold stood up the geometry core, the built-in library, the plat render, the theme system, and the test harness.

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

## Tests

The test harness is browser-runnable at `bayplan.html#test`, seeded with the built-in library as its fixture. It covers the geometry core (bounds with offset anchors, edge projection, point-in-polygon, the bearing convention, point-in-arc, the mirror transform, the placement transform, segment intersection, and polygon overlap), the TRIM checker (the full severity-interaction matrix plus end-to-end scenarios), ROUTING (work-point snapping, travel distance, backtrack detection, and crossing detection), and SERVICES (elbow-equivalent inference, dust-run budget warnings, and the electrical rollup with voltage reachability). The release gate is green only when every assertion passes.

## Local frame convention

Origin at the machine anchor, +y back (away from the operator), +x to the operator's right. Footprint edges are named front (min y), back (max y), left (min x), right (max x). Arc angles are degrees clockwise from +y. See `bayplan-envelope-conventions.md` for the full convention and the default clearance depths per machine category.

## Known Limitations

- Only a single rectangular facility is supported in the UI. The model allows an arbitrary boundary polygon, but there is no wall-drawing tool yet, and features (doors, columns, windows) are not placeable, so door-swing conflicts are not checked.
- Only one scenario. Scenario-compare (current versus proposed side by side) is in the data model but not in the UI.
- Conflict checking is pairwise and geometric. It does not yet account for `minHeight`, so a feed lane passing over a low cabinet is still flagged as if the cabinet were full height. Honoring `minHeight` is the next refinement to TRIM.
- No undo for placement. Deleting or moving a machine is immediate; recovery is by re-adding or dragging back. (Flow routing does have an undo for the last waypoint.)
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

BAYPLAN runs an eight-station arc: SOUNDING (set the floor), MANIFEST (build the library), ENVELOPE (define the halos), STOWAGE (place), TRIM (balance conflicts), ROUTING (material flow), SERVICES (utilities graph), PLAT (compare and issue). Delivered so far: ENVELOPE's built-in defaults, the render foundation, STOWAGE, TRIM, ROUTING, and now SERVICES. What remains: SOUNDING (a real wall-drawing tool and placeable features, which also unlocks door-swing conflicts), the minHeight refinement to TRIM, and PLAT (scenario-compare and a printable sheet). See the station arc in `bayplan-data-model.md`.

## License

BAYPLAN is licensed under the GNU General Public License, version 3.0 (GPL-3.0).

This program is free software: you can redistribute it and modify it under the terms of the GPL as published by the Free Software Foundation, either version 3 of the License or any later version. It is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY, without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the LICENSE file for the full text.
