# BAYPLAN

**Field Instrument #075.** A workshop floor planner that plans for how a shop actually works, not just where the boxes sit.

A bayplan is the stowage diagram for a ship's cargo bays. This one stows a workshop: scale-accurate, imperial, snap-to-grid, and single-file HTML in the local-first fleet posture. The whole plan is one JSON document that exports and imports cleanly, no server required.

## What makes it an instrument, not a floor planner

Three things, all in the data model rather than the UI:

1. **Clearance envelopes, not just footprints.** Every machine carries its real working halo: a table saw's infeed and outfeed, a lathe's outboard swing, a welder's spark standoff. Overlap two halos and the checker flags it, with a hard / soft / shared rule so a table saw's outfeed can legitimately share an aisle while a blade path never can.
2. **Material flow as a first-class overlay.** Draw the path stock takes from rack to assembly; the tool derives backtracking and crossing traffic.
3. **A typed utilities graph.** Electrical, dust, air, and data as a graph, so duct runs get measured and circuit loads roll up instead of being drawn as dumb lines.

## Status

v0.0.14. A fix-and-tidy release. Two things: dragging still did not work in the browser after the v0.0.11 fix, and the on-screen plat carried a title block that belongs on the printed sheet, not the working view. The drag problem was the click-to-world coordinate mapping: it relied on `getScreenCTM()`, which returns a wrong transform when an ancestor uses `display:contents` (as the app root does), so clicks resolved to the wrong spot and the hit-test found nothing to grab. The mapping now inverts the SVG's bounding rectangle and its `xMidYMid meet` letterboxing directly, which is immune to that quirk; the stage also suppresses native text-selection and drag so a press-and-move stays a drag. A regression test drives a full pointer sequence through an offset, scaled, letterboxed viewport. The title block was removed from the interactive view (a small north arrow remains); the printed plat still carries the full block, scale bar, and legend.

The eight-station arc is complete and every depth item from the original roadmap has shipped: undo/redo (v0.0.8), the free-form wall tool and feature wall-snapping (v0.0.9), manual multi-bend flow paths and loop-aware backtracks (v0.0.10), manual duct routing with per-circuit electrical and the static-pressure model (v0.0.12), and the compare picker with fixed-scale multi-page printing (v0.0.13).

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

Utilities: in the Utilities panel, click Open utilities, then add a dust collector and an electrical panel. Drag each node where it belongs, then click Wire all to connect every machine to its nearest collector (dust) and panel (electrical) and to assign each electrical run to a breaker. Click a run to select it: a dust run shows its delivered airflow against the capture target and lets you click along it to add bends and drag them to route the duct by hand (Straighten reverts to auto-routing); an electrical run shows its circuit and lets you reassign it to another breaker or a new one. The panel lists each circuit's load against its breaker and flags overloads, voltage mismatches, dust branches that fall short, and connected load over the panel main. Escape finishes.

Scenarios and plat: the scenario switcher in the header lets you keep more than one layout. + Scenario duplicates the active one (as Proposed), so you can rearrange a copy without losing the original. Compare shows two side by side with a delta summary (added, removed, and moved machines, plus TRIM, utilities, and flow figures for each); with three or more scenarios, dropdowns pick which pair to compare. Print opens a setup screen: choose paper size, orientation, and scale. Fit-to-page issues one titled sheet with scale bar, north arrow, and legend; a fixed scale (down to 1/8 inch to the foot) tiles the plat across multiple pages, each captioned with project, scale, and sheet number.

Room: click Room to edit the facility. Set the room's dimensions in inches, drag the corner handles to reshape it, or use Add corner and Remove corner for L-shapes and bump-outs. For an arbitrary outline, click Draw walls from scratch and click corners in order around the room (angled walls included); click the first corner or press Enter to close. Add columns, doors, and windows, then drag them into place; doors and windows snap to the nearest wall and align to it, and rotate with R. Door swings and columns are checked against your machines by TRIM. Escape finishes.

Undo and redo: the Undo and Redo buttons in the header (or Ctrl/Cmd+Z and Ctrl/Cmd+Shift+Z, and Ctrl+Y for redo) walk the whole edit history. A drag counts as one step, a no-op click adds nothing, and undo works the same in every mode.

Flows: New flow starts route mode. Click machines in order to trace how stock moves; click empty floor to drop a free bend point and route the path by hand. The panel reports travel distance, backtracks, and path crossings, and marks a flow that circles back to its start as a loop. Select a flow to drag its diamond bend points, or remove it. Escape finishes.

## Tests

The test harness is browser-runnable at `bayplan.html#test`, seeded with the built-in library as its fixture. It covers the geometry core, the TRIM checker (severity matrix, vertical-band `minHeight`, end-to-end scenarios), ROUTING (work-point snapping, travel distance, open-flow backtracks, free bend points, and the loop-aware backtrack measure), SERVICES (elbow-equivalent inference, the effective-length budget, manual dust bends raising effective length, the static-pressure model delivering a sane in-envelope airflow and flagging a long branch that falls short, per-circuit auto-assignment with a dedicated breaker sized above load and shared breakers held under eighty percent, an overloaded-circuit flag, and a voltage-mismatch flag), PLAT (scenario independence, delta detection, the printable sheet, a three-scenario compare picking an arbitrary pair, printable-area margins, fixed-scale multi-page tiling that covers the whole plat, and auto orientation choosing the fewer-page layout), SOUNDING (boundary resize and add/remove corner, free-form angled boundaries, wall-snapping of windows and doors, and feature conflict behavior), history (undo, redo, redo-tail truncation, dedupe, mid-drag suspension, library-strip), and an interaction test that drives a full pointer-down, move, and up sequence to confirm a drag survives the redraw that selection triggers. The release gate is green only when every assertion passes.

## Local frame convention

Origin at the machine anchor, +y back (away from the operator), +x to the operator's right. Footprint edges are named front (min y), back (max y), left (min x), right (max x). Arc angles are degrees clockwise from +y. See `bayplan-envelope-conventions.md` for the full convention and the default clearance depths per machine category.

## Known Limitations

- Boundary editing offers corner handles, dimension entry, and a free-form click-to-draw wall tool. Corners snap to one inch, and true curves are approximated by placing several straight corners; there is no arc-wall primitive.
- Doors and windows snap to the nearest wall within about thirty inches while dragging; hold Alt to place one off the wall. Columns are free obstacles and do not snap.
- Door swing is modeled as a quarter-circle arc from the hinge, treated as a full-height hard zone. It does not model leaf thickness or a partial-height opening.
- Scenario compare pairs two layouts at a time; with three or more you pick the pair from the dropdowns. There is no all-at-once matrix across every scenario.
- Fixed-scale printing tiles the plat across pages and captions each with its sheet number, but the pages abut rather than overlap, so there is no trim-and-tape margin. Set the browser print dialog to the same paper size at 100% (no shrink-to-fit) for the scale to come out true.
- Undo history is per session and lives in memory; it is not written into the exported document, so reopening a saved plan starts with a clean history.
- Flow waypoints snap to a machine's work points, or to its anchor when the machine has no work points defined, and free bend points can be dropped anywhere to route by hand. Only the flow-relevant machines in the seed (saw, jointer, planer, bandsaw, miter saw, CNC) carry work points; everything else routes through its anchor.
- Backtrack detection uses net start-to-end direction for open flows, and switches to counting reversals (turns past ninety degrees) for a flow whose net travel is small, which covers loops that return to their start. A gentle zigzag that drifts backward without any single sharp reversal is the remaining measurement corner.
- The utilities graph auto-routes runs (dust as a single orthogonal L, electrical straight), and dust runs can then be routed by hand with any number of bends. Electrical runs are still drawn straight.
- The dust static-pressure model uses a linear fan curve and a smooth-metal friction fit, and omits hood entry losses and blast-gate settings. It is a design aid, not a certified duct calculation; the effective-length budget remains as a secondary quick screen.
- Per-circuit assignment covers breaker sizing, the eighty-percent continuous-load margin, and voltage matching. It does not model conductor gauge, voltage drop over distance, or panel space limits beyond the breaker count you create.
- Electrical rollup buckets load by voltage and checks 240V reachability and total load against the panel main. It does not yet assign individual circuits or check per-breaker load.
- QUARTERMASTER seed import is designed (provenance fields are in the schema) but not implemented.
- Annular arcs (with an inner radius) are supported in the model and sampled correctly, but no seed machine exercises one yet.
- The plat export produces the JSON document, not a printable sheet. A full printable plat with legend and revision block is a PLAT-station item, still open.
- Import validation is shallow. It checks for a facility and a scenarios array; it does not yet validate the full schema or migrate older schema versions.

## Roadmap

BAYPLAN runs an eight-station arc: SOUNDING (set the floor), MANIFEST (build the library), ENVELOPE (define the halos), STOWAGE (place), TRIM (balance conflicts), ROUTING (material flow), SERVICES (utilities graph), PLAT (compare and issue). As of this release all eight are functional end to end: you can shape a room and place features, build the library and its halos, stow machines, trim their conflicts in three dimensions, route the flow, run the services, and compare and issue the plat. The three data-model open items are closed. The eight-station arc is complete and every depth item from the original roadmap has shipped: undo/redo (v0.0.8), the free-form wall tool and feature wall-snapping (v0.0.9), manual multi-bend flow paths and loop-aware backtracks (v0.0.10), the drag fix (v0.0.11), manual duct routing with per-circuit electrical and the static-pressure model (v0.0.12), and the compare picker with fixed-scale multi-page printing (v0.0.13). What remains is optional breadth, not depth: a daylight overlay driven by window facing, and the QUARTERMASTER seed import that would connect BAYPLAN to the workshop inventory. See the station arc in `bayplan-data-model.md`.

## License

BAYPLAN is licensed under the GNU General Public License, version 3.0 (GPL-3.0).

This program is free software: you can redistribute it and modify it under the terms of the GPL as published by the Free Software Foundation, either version 3 of the License or any later version. It is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY, without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the LICENSE file for the full text.
