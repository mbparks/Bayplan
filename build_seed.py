#!/usr/bin/env python3
"""
BAYPLAN (FI-075) built-in machine library seed generator.

Emits a JSON document of MachineDef entries conforming to the section-5 schema
in bayplan-data-model.md. Source-of-truth for the built-in ENVELOPE defaults.

Local frame convention (see bayplan-envelope-conventions.md):
  origin (0,0) = anchor
  +y = back (away from operator), -y = front (operator side)
  +x = operator's right, -x = operator's left
  footprint edges are named: front(min y), back(max y), left(min x), right(max x)
  arc angles: degrees clockwise from +y (back); 0=back, 90=right, 180=front, 270=left

All dimensions in inches. These are defaults meant to be tuned per real shop.
"""

import json

# --- helpers ----------------------------------------------------------------

def footprint(W, D, x0=None, y0=None):
    """Rectangle as 4 CCW vertices in local frame. x0,y0 = min corner vs anchor.
    Defaults to anchor at geometric center."""
    if x0 is None:
        x0 = -W / 2
    if y0 is None:
        y0 = -D / 2
    return {"vertices": [
        [round(x0, 2), round(y0, 2)],
        [round(x0 + W, 2), round(y0, 2)],
        [round(x0 + W, 2), round(y0 + D, 2)],
        [round(x0, 2), round(y0 + D, 2)],
    ]}

def rect(edge, depth):
    return {"shape": "rect", "geometry": {"edge": edge, "depth": depth}}

def arc(cx, cy, radius, start, sweep, inner=None):
    g = {"center": [cx, cy], "radius": radius, "startAngle": start, "sweep": sweep}
    if inner is not None:
        g["innerRadius"] = inner
    return {"shape": "arc", "geometry": g}

def zone(base, label, severity, minHeight, note):
    z = dict(base)
    z.update({"label": label, "severity": severity,
              "minHeight": minHeight, "note": note})
    return z

def power(v, amps, phase=1, dedicated=False):
    return {"voltage": v, "amps": amps, "phase": phase, "dedicated": dedicated}

def dust(pos, dia):
    return {"position": pos, "diameter": dia}

def wp(pid, label, x, y):
    return {"id": pid, "label": label, "position": [x, y]}

def prov():
    return {"source": "builtin", "qmAssetId": None,
            "seededFields": [], "seededAt": None, "localEdits": []}

def machine(mid, name, category, fp, anchor_note, height, weight,
            pw, dp, clearances, ports):
    return {
        "id": mid, "name": name, "category": category,
        "provenance": prov(),
        "footprint": fp, "anchor": [0, 0], "anchorNote": anchor_note,
        "height": height, "weight": weight,
        "power": pw, "dustPort": dp,
        "clearances": clearances, "ports": ports,
    }

# --- library ----------------------------------------------------------------
# Feed-clearance defaults:
#   sheet-goods capable: 96 ideal (fits a 8ft rip), minHeight = deck + stock
#   long-stock:          72-96, matched to typical board length
#   operator standing:   30 (36 comfortable), soft, full height (minHeight null)
#   service access:      18-24, soft
#   fire/spark:          hard, projecting
#   swing:               arc, hard

M = []

# 1. Cabinet table saw --------------------------------------------------------
M.append(machine(
    "builtin-table-saw-cabinet", "Table saw (3HP cabinet, 36in fence)", "table_saw",
    footprint(44, 27, x0=-14, y0=-13),          # blade 14in from left, 13in from front
    "blade, at kerf line", 34, 500,
    power(240, 15, 1, True), dust([0, -6], 4),
    [
        zone(rect("front", 96), "infeed", "shared", 40,
             "8ft infeed to rip full sheets; clear only to table height"),
        zone(rect("back", 96), "outfeed", "shared", 40,
             "8ft outfeed for ripped stock; overlaps aisles by design"),
        zone(rect("front", 36), "operator", "soft", None,
             "operator stance at the front, full height"),
        zone(rect("right", 40), "blade_access", "soft", 40,
             "36in rip capacity to the right of the blade"),
    ],
    [wp("in", "stock_in", 0, -13), wp("out", "stock_out", 0, 14)],
))

# 2. 8-inch jointer -----------------------------------------------------------
M.append(machine(
    "builtin-jointer-8in", "Jointer (8in, long bed)", "jointer",
    footprint(72, 22),                           # long axis x, stock passes L->R
    "cutterhead, bed center", 34, 450,
    power(240, 12, 1, False), dust([0, 8], 4),
    [
        zone(rect("left", 72), "infeed", "shared", 38,
             "long-board infeed along the bed axis"),
        zone(rect("right", 72), "outfeed", "shared", 38,
             "long-board outfeed along the bed axis"),
        zone(rect("front", 30), "operator", "soft", None,
             "operator works along the front of the bed"),
    ],
    [wp("in", "stock_in", -36, 0), wp("out", "stock_out", 36, 0)],
))

# 3. Thickness planer (benchtop) ---------------------------------------------
M.append(machine(
    "builtin-planer-13in", "Thickness planer (13in benchtop on stand)", "planer",
    footprint(24, 22),
    "cutterhead center", 38, 90,
    power(120, 15, 1, False), dust([0, 10], 4),
    [
        zone(rect("front", 96), "infeed", "shared", 42,
             "long-board infeed; feeds front to back"),
        zone(rect("back", 96), "outfeed", "shared", 42,
             "long-board outfeed"),
        zone(rect("front", 30), "operator", "soft", None,
             "operator at infeed"),
    ],
    [wp("in", "stock_in", 0, -11), wp("out", "stock_out", 0, 11)],
))

# 4. 14-inch bandsaw ----------------------------------------------------------
M.append(machine(
    "builtin-bandsaw-14in", "Bandsaw (14in)", "bandsaw",
    footprint(26, 30),
    "blade at table slot", 43, 250,
    power(120, 15, 1, False), dust([0, 6], 4),
    [
        zone(rect("front", 72), "infeed", "shared", 46,
             "resaw infeed for long stock"),
        zone(rect("back", 72), "outfeed", "shared", 46,
             "resaw outfeed"),
        zone(rect("front", 30), "operator", "soft", None,
             "operator at the front of the table"),
        zone(rect("front", 8), "blade_access", "hard", None,
             "immediate blade danger zone, keep clear"),
    ],
    [wp("in", "stock_in", 0, -15), wp("out", "stock_out", 0, 15)],
))

# 5. Compound miter saw station ----------------------------------------------
M.append(machine(
    "builtin-miter-saw", "Miter saw (compound, station)", "miter_saw",
    footprint(24, 20),
    "blade at fence intersection", 36, 55,
    power(120, 15, 1, False), dust([0, 8], 2.5),
    [
        zone(rect("left", 96), "infeed", "shared", 40,
             "long-trim support to the left; 8ft ideal"),
        zone(rect("right", 96), "outfeed", "shared", 40,
             "long-trim support to the right"),
        zone(rect("front", 30), "operator", "soft", None,
             "operator at the front"),
    ],
    [wp("in", "stock_in", -12, 0), wp("out", "stock_out", 12, 0)],
))

# 6. Floor drill press --------------------------------------------------------
M.append(machine(
    "builtin-drill-press", "Drill press (floor standing)", "drill_press",
    footprint(20, 24),
    "spindle / chuck axis", 66, 200,
    power(120, 12, 1, False), None,
    [
        zone(rect("front", 30), "operator", "soft", None,
             "operator at the front"),
        zone(rect("left", 36), "loading", "soft", None,
             "long-work overhang support, left"),
        zone(rect("right", 36), "loading", "soft", None,
             "long-work overhang support, right"),
    ],
    [],
))

# 7. Wood lathe (arc showcase) ------------------------------------------------
M.append(machine(
    "builtin-wood-lathe", "Wood lathe (with outboard turning)", "lathe",
    footprint(48, 18, x0=-6, y0=-9),             # spindle 6in from left end
    "headstock spindle", 44, 220,
    power(120, 15, 1, False), None,
    [
        zone(rect("front", 30), "operator", "soft", None,
             "turner stands along the front of the bed"),
        zone(rect("right", 24), "end_clearance", "soft", 44,
             "tailstock end, room for long spindle stock"),
        zone(arc(0, 0, 20, 180, 90), "swing", "hard", None,
             "outboard bowl swing off the headstock, front-left arc"),
    ],
    [],
))

# 8. Benchtop metal lathe -----------------------------------------------------
M.append(machine(
    "builtin-metal-lathe", "Metal lathe (benchtop)", "metal_lathe",
    footprint(30, 14, x0=-3, y0=-7),             # chuck near left end
    "spindle / chuck", 16, 300,
    power(120, 15, 1, False), None,
    [
        zone(rect("left", 24), "end_clearance", "hard", None,
             "bar stock protruding through the spindle bore"),
        zone(rect("right", 18), "end_clearance", "soft", None,
             "tailstock end for long work"),
        zone(rect("front", 24), "operator", "soft", None,
             "operator at the carriage"),
    ],
    [],
))

# 9. Benchtop mill ------------------------------------------------------------
M.append(machine(
    "builtin-mill-benchtop", "Milling machine (benchtop)", "mill",
    footprint(24, 20),
    "spindle axis", 32, 350,
    power(120, 15, 1, False), None,
    [
        zone(rect("left", 16), "service", "soft", None,
             "X-table travel overhang, left"),
        zone(rect("right", 16), "service", "soft", None,
             "X-table travel overhang, right"),
        zone(rect("front", 24), "operator", "soft", None,
             "operator at the handwheels"),
    ],
    [],
))

# 10. CNC router 4x4 ----------------------------------------------------------
M.append(machine(
    "builtin-cnc-router-4x4", "CNC router (4x4 bed)", "cnc_router",
    footprint(60, 60),
    "spoilboard center", 48, 400,
    power(120, 15, 1, False), dust([0, 0], 2.5),
    [
        zone(rect("front", 48), "loading", "shared", None,
             "material load and unload from the front"),
        zone(rect("front", 30), "operator", "soft", None,
             "operator and pendant at the front"),
        zone(rect("back", 18), "service", "soft", None,
             "rear access for wiring and gantry service"),
        zone(rect("left", 18), "service", "soft", None,
             "side access for bit changes"),
        zone(rect("right", 18), "service", "soft", None,
             "side access for bit changes"),
    ],
    [wp("in", "stock_in", 0, -30)],
))

# 11. Welding table (fire standoff) -------------------------------------------
M.append(machine(
    "builtin-welding-table", "Welding table (with MIG)", "welding",
    footprint(30, 60),
    "table center", 34, 350,
    power(240, 50, 1, True), None,
    [
        zone(rect("front", 48), "service", "hard", None,
             "spark and slag spray zone, keep combustibles clear"),
        zone(rect("left", 24), "service", "hard", None,
             "spark standoff, left"),
        zone(rect("right", 24), "service", "hard", None,
             "spark standoff, right"),
        zone(rect("front", 36), "operator", "soft", None,
             "welder position, overlaps the spark zone"),
    ],
    [],
))

# 12. Bench grinder (pedestal) ------------------------------------------------
M.append(machine(
    "builtin-bench-grinder", "Bench grinder (pedestal)", "grinder",
    footprint(16, 14),
    "between the wheels", 44, 60,
    power(120, 12, 1, False), None,
    [
        zone(rect("front", 36), "service", "hard", None,
             "spark cone projecting forward from the wheels"),
        zone(rect("front", 30), "operator", "soft", None,
             "operator at the tool rests"),
    ],
    [],
))

# 13. Assembly table (shared-zone showcase) -----------------------------------
M.append(machine(
    "builtin-assembly-table", "Assembly table (4x8)", "assembly",
    footprint(48, 96),
    "table center", 34, 300,
    power(120, 15, 1, False), None,
    [
        zone(rect("front", 30), "operator", "shared", None,
             "work apron; shares space with aisles and neighbor outfeed"),
        zone(rect("back", 30), "operator", "shared", None,
             "work apron, far side"),
        zone(rect("left", 30), "operator", "shared", None,
             "work apron, left"),
        zone(rect("right", 30), "operator", "shared", None,
             "work apron, right"),
    ],
    [],
))

# 14. Woodworking bench -------------------------------------------------------
M.append(machine(
    "builtin-workbench", "Workbench (with front and end vise)", "bench",
    footprint(24, 72),
    "bench center", 34, 250,
    power(120, 15, 1, False), None,
    [
        zone(rect("front", 36), "operator", "soft", None,
             "primary working side at the front vise"),
        zone(rect("right", 24), "operator", "soft", None,
             "end-vise work clearance"),
    ],
    [],
))

# 15. Dust collector (utility source) -----------------------------------------
M.append(machine(
    "builtin-dust-collector", "Dust collector (2HP cyclone)", "dust_collector",
    footprint(30, 40),
    "inlet center", 78, 200,
    power(240, 12, 1, True), None,
    [
        zone(rect("front", 30), "service", "soft", None,
             "bin and filter service access"),
    ],
    [],
))

# 16. Air compressor ----------------------------------------------------------
M.append(machine(
    "builtin-air-compressor", "Air compressor (vertical 60gal)", "compressor",
    footprint(24, 26),
    "tank center", 68, 250,
    power(240, 15, 1, True), None,
    [
        zone(rect("front", 24), "service", "soft", None,
             "drain, regulator, and pump access"),
        zone(rect("back", 12), "service", "soft", None,
             "cooling and heat clearance behind the pump"),
    ],
    [],
))

# 17. Electronics bench -------------------------------------------------------
M.append(machine(
    "builtin-electronics-bench", "Electronics bench (ESD)", "electronics",
    footprint(30, 60),
    "bench center", 34, 200,
    power(120, 20, 1, False), None,
    [
        zone(rect("front", 30), "operator", "soft", None,
             "seated operator, chair plus reach"),
    ],
    [],
))

# --- document ----------------------------------------------------------------
doc = {
    "schemaVersion": "1.0.0",
    "kind": "bayplan-seed-library",
    "generated": "2026-07-08",
    "frame": {
        "units": "inches",
        "origin": "anchor",
        "axes": "+x operator-right, +y back (away from operator)",
        "edges": "front=min y, back=max y, left=min x, right=max x",
        "arcAngles": "degrees clockwise from +y (back): 0=back,90=right,180=front,270=left",
        "note": "Defaults for tuning. minHeight null means full height (floor to head).",
    },
    "library": M,
}

with open("bayplan-seed-library.json", "w") as f:
    json.dump(doc, f, indent=2)

# quick self-report
cats = sorted({m["category"] for m in M})
n_zones = sum(len(m["clearances"]) for m in M)
n_arcs = sum(1 for m in M for z in m["clearances"] if z["shape"] == "arc")
n_shared = sum(1 for m in M for z in m["clearances"] if z["severity"] == "shared")
n_hard = sum(1 for m in M for z in m["clearances"] if z["severity"] == "hard")
print(f"machines: {len(M)}")
print(f"categories ({len(cats)}): {', '.join(cats)}")
print(f"clearance zones: {n_zones}  (arc: {n_arcs}, shared: {n_shared}, hard: {n_hard})")
print("wrote bayplan-seed-library.json")
