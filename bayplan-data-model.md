# BAYPLAN (FI-075): Data Model Specification

**Field Instrument #075**
Workshop floorplan layout planner with clearance-aware machine placement, material-flow analysis, and a typed utilities graph.

Document revision: 1.0.0
Schema version: 1.0.0
Status: design captured, pre-build

---

## 1. Purpose and posture

BAYPLAN plans a workshop floor the way the shop actually works, not just where boxes sit. It is scale-accurate, imperial, snap-to-grid, and single-file HTML in the local-first fleet posture: the entire plan is one JSON document that exports and imports cleanly with no server dependency.

What separates BAYPLAN from a generic floor planner is three things, all of which live in the data model rather than the UI:

1. Machines carry real, directional **clearance envelopes**, not just footprints.
2. **Material flow** is a first-class overlay that snaps to named work points on each machine.
3. **Utilities** (electrical, dust, air, data) are modeled as a typed graph so runs can be measured and loads rolled up, not just drawn.

---

## 2. Top-level document

```
BayplanDocument
  schemaVersion     "1.0.0"
  meta              { title, created, modified, author, units:"imperial", gridSpacing }
  facility          Facility        // the bounded space, shared across scenarios
  library           MachineDef[]    // definitions (types), not placements
  scenarios         Scenario[]      // current, proposed, etc.
  activeScenarioId
```

### The definition/placement split

The single most important structural decision: **definitions live once in `library`, placements live in scenarios.** A "SawStop PCS 3HP" is defined one time with its footprint and clearance geometry. Each scenario references it by `defId` and adds only position, rotation, and sparse overrides.

This split does three jobs:

- Scenario-compare stays honest. You are comparing arrangements of the same machines, not divergent copies that have drifted apart.
- A QUARTERMASTER seed can populate `library` without touching any layout.
- A definition edit propagates to every placement unless a specific instance deliberately overrides it.

---

## 3. Coordinate and unit conventions

Store everything in a single canonical internal unit. Display formatting is always a render concern, never a storage concern (the same separation PITOT keeps between imperial display and calculation).

| Property | Convention |
|----------|-----------|
| Unit | Inches, floating point |
| Origin | One facility corner |
| Axes | +x east, +y north |
| Angles | Degrees, clockwise from north |

Angles clockwise from north keep the model aligned with a surveyor's plat and its north arrow. Feet-and-inches display, fractional rounding, and scale bars are all computed at render time from the canonical inch values.

---

## 4. Facility (the floor)

```
Facility
  id, name
  boundary        Polygon          // outer wall outline, ordered vertices (in)
  ceilingHeight   number
  northOffset     number           // deg, lets plan north differ from screen up
  features        Feature[]
  scaleRef        { pixelsPerInch } // for imported/traced background images
```

The boundary is a real polygon, not a width/height rectangle, because shops have bump-outs, angled walls, and the corner where the water heater lives.

### Feature

Everything fixed you must design around:

```
Feature
  id
  kind       "column" | "door" | "window" | "post" | "drain" |
             "panel" | "hoseBib" | "stairs" | "immovable"
  geometry   Polygon | Segment | Point
  swing      { hinge, direction, angle }   // doors only
  facing     number                        // windows: direction daylight enters
  height     number                        // low header, mezzanine, etc.
```

Two features participate in checks beyond simply existing:

- **Doors** carry a swing arc that enters conflict checking exactly like a machine clearance zone. Under the hood a door swing is the same `Arc` primitive a lathe end-clearance uses (see section 6).
- **Windows** carry `facing` so the daylight overlay has a direction to compute against.

---

## 5. MachineDef (the heart of the model)

A definition is a footprint plus a set of typed, directional clearance zones. This is where BAYPLAN stops being a generic floor planner.

```
MachineDef
  id, name, category   // "table_saw","lathe","welding","assembly","storage"...
  provenance           Provenance          // see section 7
  footprint    Polygon                     // local coords, origin at anchor
  anchor       Point                       // rotation/placement reference
  height       number
  weight       number                      // for later floor-loading notes
  power        PowerReq                     // see section 8
  dustPort     { position, diameter } | null
  clearances   ClearanceZone[]
  ports        WorkPoint[]                  // named material entry/exit points
```

- `footprint` is defined in the machine's own local coordinate frame, origin at `anchor`.
- `anchor` is the meaningful reference (blade, spindle) that placement rotates around, not the geometric centroid.
- `ports` are the named points material-flow paths snap to (see section 9).

Fields that a QUARTERMASTER seed may populate: `name`, `footprint`, `weight`, `power`, `dustPort`. Fields that are always BAYPLAN-native and never seeded: `clearances`, `anchor`, `ports`.

---

## 6. ClearanceZone (the differentiator)

Each machine carries its real working halo as a list of typed zones, defined in the machine's local frame so they rotate and mirror with the placement.

```
ClearanceZone
  id
  label       "infeed" | "outfeed" | "operator" | "blade_access" |
              "end_clearance" | "swing" | "loading" | "service"
  shape       "rect" | "polygon" | "arc"
  geometry    RectOffEdge | Polygon | Arc
  severity    "hard" | "soft" | "shared"
  minHeight   number      // zone only needs to be clear up to this height
  note
```

### Geometry primitives

Three first-class shapes, tagged by the `shape` discriminator so the renderer and the conflict checker both know what they are dealing with:

```
RectOffEdge   { edge, depth }         // rectangle projected off a named footprint edge
Polygon       { vertices: Point[] }   // arbitrary, local frame
Arc           { center, radius, startAngle, sweep, innerRadius? }
```

`RectOffEdge` is the common case: infeed, outfeed, operator, and service zones are usually a rectangle standing off one edge of the footprint.

`Arc` is a first-class citizen, not a polygon approximation. It carries an optional `innerRadius` so it can express either:

- a full pie wedge (lathe swing over the ways, door swing from the hinge), or
- an annular sweep (the reachable band around a rotary table, where the center is the machine itself and needs no clearing).

`center` is in the machine's local frame, so an arc rotates and mirrors with its placement like any other geometry.

Two payoffs from arc being first-class:

1. **Exact conflict math.** Point-in-arc is a cheap radius-plus-angle test, so overlap detection is precise rather than faceted. This avoids the "almost overlaps but the polygon facets missed it" class of bug.
2. **One primitive for two problems.** A door `Feature` swing and a lathe `end_clearance` are the same `Arc` under the hood. One piece of geometry code covers both, and the checker treats a door arc and a machine arc identically.

**Mirroring rule:** mirroring an arc negates `startAngle` and `sweep` about the mirror axis. This transform is written once and tested hard, because a flipped-machine arc that is silently wrong passes a glance and fails on the bench.

### Severity (the rule that makes a shop layable-out)

The `severity` field is what lets real shops share space without false conflicts:

| Severity | Meaning | Overlap behavior |
|----------|---------|------------------|
| **hard** | Must never be occupied (blade infeed path, lathe end clearance) | Overlap with any footprint or hard zone is an **error** |
| **soft** | Should be clear (an operator station not always in use) | Overlap with another soft zone is a **warning** |
| **shared** | May legitimately overlap the same label elsewhere | Two `shared` zones overlapping is **fine**; a `shared` zone hitting a `hard` zone is still an **error** |

The `shared` value is what models an outfeed/infeed pair or a common assembly apron correctly. A table saw's outfeed genuinely wants to overlap the jointer's operator walk space, and the tool needs to know that is allowed rather than lighting up red.

### WorkPoint

```
WorkPoint
  id
  label      "stock_in" | "stock_out" | ...
  position   Point       // local frame
```

Named spots the material-flow layer snaps to, so a flow path connects at the planer's actual infeed rather than at its centroid.

---

## 7. Placement (a machine in a scenario)

```
Placement
  id
  defId                 // -> MachineDef
  position   Point      // facility coords of the anchor
  rotation   number     // deg
  mirrored   bool
  overrides  { footprint?, clearances?, power? }   // sparse
  locked     bool
  label                 // instance name, e.g. "Table Saw (main)"
```

Overrides are sparse and optional. A definition change propagates to every placement unless that instance deliberately diverges. `locked` protects a placement from accidental drag once it is committed.

---

## 8. Utilities layer

Utilities are modeled as a **typed graph**, not freehand lines. The graph is what lets BAYPLAN compute duct-run length, elbow count, and per-circuit load instead of merely drawing pipes.

```
UtilityNode
  id
  kind      "panel" | "subpanel" | "dust_collector" | "compressor" |
            "drop" | "junction" | "receptacle" | "light"
  position
  spec      // panel: {voltage, spaces}; collector: {cfm, staticPressure}
```

```
UtilityRun
  id
  system            "electrical" | "dust" | "air" | "data"
  fromNode, toNode
  polyline          Point[]     // routed path, for length + elbow inference
  spec              // electrical:{voltage,amps,circuit}; dust:{diameter}
  servesPlacementId
```

```
PowerReq   (on MachineDef)
  voltage    120 | 240
  amps
  phase      1 | 3
  dedicated  bool
```

Runs-as-graph give the checks that make this layer worth having:

- A dust run whose summed length plus elbow-equivalent exceeds the threshold for the collector's CFM throws a warning. Elbow count is inferred from `polyline` vertex angles, so it is never hand-entered.
- A 240V machine placed in a scenario with no reachable 240V drop flags.
- Total connected load per circuit rolls up against the panel spec.

---

## 9. Material flow

```
FlowPath
  id, name, stockType
  waypoints   [ { placementId, portId } ... ]   // snaps to WorkPoints
  color
```

Derived, never stored: total travel distance, backtrack segments, crossing count against other flow paths.

Flow paths reference placement plus port ids rather than raw coordinates, so moving a machine drags its flow connections with it. Backtracking and crossings recompute on the fly, the way SEQUENCE DESK derives its metrics.

---

## 10. Scenario

```
Scenario
  id, name              // "Current", "Proposed A"
  placements    Placement[]
  utilityNodes  UtilityNode[]
  utilityRuns   UtilityRun[]
  flows         FlowPath[]
  notes
```

Scenario-compare is a clean diff: same `library`, same `facility`, different placement/utility/flow sets. Side-by-side render plus a small delta summary (machines moved, conflicts resolved or introduced, total flow distance change) falls straight out of this structure.

---

## 11. Provenance and the QUARTERMASTER seed

BAYPLAN seeds its library from QUARTERMASTER once, then owns it. The import is a snapshot with a paper trail, not a live binding. This protects BAYPLAN-native clearance work from any future roster sync.

```
Provenance   (on MachineDef)
  source       "quartermaster" | "manual" | "builtin"
  qmAssetId                    // stable QM id, null if manual
  seededFields  string[]       // which fields QM populated at seed time
  seededAt                     // timestamp of the seed
  localEdits    string[]       // fields the user has touched since seeding
```

### The ownership rule

**QUARTERMASTER owns the fields it seeded until you edit them; BAYPLAN owns clearances always.**

- Seedable from the roster: `footprint`, `name`, `weight`, `power`, `dustPort`.
- Always BAYPLAN-native, never seeded: `clearances`, `anchor`, `ports`.

### Re-sync as three-bucket reconciliation

A later "check against QUARTERMASTER" pass is a review screen, not an automatic overwrite:

1. Asset in QM, not in library: offer to seed it (a machine you acquired).
2. Asset in both, a seeded field changed in QM, field **not** in `localEdits`: offer to update it (you corrected a dimension in the roster).
3. Asset in both, field **is** in `localEdits`: leave it alone, show the divergence for information only.

Bucket three protects the tuning. If you measured your planer's real footprint and nudged it in BAYPLAN, re-sync surfaces the difference but never silently reverts you.

### Deletion asymmetry

A machine deleted from QUARTERMASTER does **not** vanish from a BAYPLAN scenario, because a layout is a historical document. Re-sync flags it as "in library, no longer in roster" and lets you decide, rather than removing a placement out from under a saved scenario. This matches the archive-over-delete posture.

---

## 12. Standing design decisions

**Facility is shared across scenarios, not copied into each.** Correct when the building is fixed and you are only rearranging contents. If a future version needs to compare "knock out this wall" against "leave it," `facility` gets promoted into the scenario. Kept shared for v1.

**Derived data is never stored.** Conflict lists, flow distances, load rollups, and duct-length warnings all recompute from the model. Cleaner exports, no stale cache, consistent with files-as-source-of-truth.

**Display is never storage.** All geometry is canonical inches; feet-and-inches, fractions, and scale bars are render-time only.

---

## 13. Open items for the build phase

Each open item now has a home station in the arc (section 14), so this list doubles as the close-out schedule for the build.

- Default clearance depths per machine category for the built-in library seed. Home station: **ENVELOPE**.
- Elbow-equivalent length table per duct diameter used in the dust-run warning. Home station: **SERVICES**.
- Printable plat title-block fields (scale, north arrow, legend, revision). Home station: **PLAT**.

---

## 14. Station arc

BAYPLAN runs an eight-station arc from empty floor to issued plat, in the same shape STEELYARD and the SHAKEDOWN submodules use. Station names sit in the ship-stowage register the instrument already lives in. Each station lists what it touches in the data model and its gate: the condition that says you are done and may move on.

The arc is nominally linear but genuinely a loop. TRIM sends you back to STOWAGE, SERVICES can send you back to STOWAGE, and PLAT sends you back to SOUNDING with a fresh scenario. Back-edges are noted where they matter.

### 1. SOUNDING: set the floor

Establish the bounded space before anything goes in it. Trace or draw the boundary polygon, drop fixed features, place doors with swing arcs and windows with facing, lock the scale reference against a traced background if you have one.

- Touches: `Facility`, `Feature`, `scaleRef`.
- Gate: a closed boundary polygon and a locked scale. Nothing places until the floor knows how big it is.

### 2. MANIFEST: build the library

Assemble the definitions of what must be stowed. Seed from QUARTERMASTER (populating `name`, `footprint`, `weight`, `power`, `dustPort` with provenance stamped) or add manual definitions. Footprints and anchors are set here; clearances are not.

- Touches: `library[]`, `MachineDef`, `Provenance`.
- Gate: every machine you intend to place exists as a definition with a footprint and an anchor.

### 3. ENVELOPE: define the working halos

The station that makes BAYPLAN a Field Instrument, and the one QUARTERMASTER never touches. Attach clearance zones to each definition (rect-off-edge for infeed/outfeed/service, arc for end-clearance and swings, polygon for odd cases), set each zone's severity, and drop the work points flow will later snap to.

- Touches: `ClearanceZone`, `WorkPoint`.
- Gate: each definition you will place carries its real halo and its stock-in / stock-out points.
- Closes open item: default clearance depths per category, pinned here as built-in starting values.

### 4. STOWAGE: place

The core canvas act. Drop definitions into the active scenario as placements, rotate around the anchor, mirror, snap to grid, lock the committed ones. Clearance zones and arcs rotate and mirror with each placement.

- Touches: `Placement`, `activeScenarioId`.
- Gate: every machine placed. Conflicts are expected here and are TRIM's job, not a blocker.

### 5. TRIM: balance the conflicts

Run clearance overlap detection with the hard/soft/shared rule, door-swing arcs checked against placements. Hard overlaps are errors, soft are warnings, shared-against-shared passes. Resolve by nudging placements, which loops back into STOWAGE.

- Touches: derived conflict list (never stored); reads all `Placement` and `ClearanceZone` geometry.
- Gate: zero hard conflicts, or every remaining one explicitly acknowledged.
- Back-edge: STOWAGE, the normal path for resolving a flagged overlap.

### 6. ROUTING: material flow

Draw flow paths that snap waypoint-to-waypoint across machine work points, then read the derived backtrack and crossing metrics the way SEQUENCE DESK reports flow. Moving a machine in STOWAGE drags its flow connections, so a late nudge does not orphan a path.

- Touches: `FlowPath`; reads `WorkPoint`s.
- Gate: primary stock flows drawn and their backtrack/crossing counts reviewed.

### 7. SERVICES: utilities graph

Lay the typed graph: panels and drops, dust collector, compressor, runs between them as polylines. Read the rollups that justify the graph: connected load per circuit against panel spec, and duct-run warnings from length plus inferred elbow count.

- Touches: `UtilityNode`, `UtilityRun`; reads `PowerReq`.
- Gate: every machine reachable by its required power and, where it has a `dustPort`, by a duct run within the collector's budget.
- Closes open item: the elbow-equivalent table per diameter lives here.
- Back-edge: STOWAGE (move the 240V machine nearer a drop).

### 8. PLAT: compare and issue

Two moves in one station because they are one decision. First, scenario-compare: current against proposed side by side, with the delta summary (machines moved, conflicts resolved or introduced, total flow distance change) falling straight out of the shared library and facility. Then issue the chosen scenario as a printable plat with title block, scale bar, north arrow, and legend.

- Touches: reads across `Scenario`s; emits the plat.
- Gate: a scenario chosen and a clean plat exported.
- Closes open item: the plat title-block fields are defined here.
- Back-edge: SOUNDING, when spinning up a fresh proposed variant.

### Note on the MANIFEST/ENVELOPE split

MANIFEST (what machines exist) and ENVELOPE (their halos) are deliberately separate stations so the seed-then-own boundary is a boundary between two stations rather than a subtlety inside one. QUARTERMASTER's reach stops at the MANIFEST/ENVELOPE line. A seven-station arc that folds them together is defensible, but the differentiator earns its own station.

---

## License

GPL-3.0
