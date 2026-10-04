import math

import cadquery as cq

from params import *

# ============================================================
# 1. MAIN BODY
# ============================================================

stem = cq.Workplane("XY").circle(lower_stem_od / 2.0).extrude(lower_stem_height)
upper_body = (
    cq.Workplane("XY")
    .workplane(offset=z_stem_top)
    .circle(upper_body_od / 2.0)
    .extrude(upper_body_height)
)
flange = (
    cq.Workplane("XY")
    .workplane(offset=z_upper_top)
    .circle(flange_od / 2.0)
    .extrude(flange_height)
)

main_body = stem.union(upper_body).union(flange)

try:
    main_body = main_body.edges(">Z").fillet(lip_fillet_radius)
except Exception:  # noqa: BLE001, S110 - CadQuery fillet may fail on some geometries
    pass

try:
    main_body = main_body.edges(
        cq.selectors.BoxSelector(
            (-15, -15, z_stem_top - DELTA), (15, 15, z_stem_top + DELTA)
        )
    ).fillet(cb_fillet_radius)
except Exception:  # noqa: BLE001, S110 - CadQuery fillet may fail on some geometries
    pass

# ============================================================
# 2. METALLIC INSERT - Hexagon with circles on vertices
# ============================================================

hex_corner_r = insert_hex_flat_to_flat / (2 * math.cos(math.pi / 6))
circle_r = insert_circle_dia / 2.0

hex_pts = []
for i in range(6):
    angle = 2 * math.pi * i / 6 + math.pi / 6
    hex_pts.append((hex_corner_r * math.cos(angle), hex_corner_r * math.sin(angle)))
hex_pts.append(hex_pts[0])

hex_solid = cq.Workplane("XY").polyline(hex_pts).close().extrude(insert_thickness)

insert_shape = hex_solid
for i in range(6):
    angle = 2 * math.pi * i / 6 + math.pi / 6
    cx = hex_corner_r * math.cos(angle)
    cy = hex_corner_r * math.sin(angle)
    circle_solid = (
        cq.Workplane("XY").center(cx, cy).circle(circle_r).extrude(insert_thickness)
    )
    insert_shape = insert_shape.union(circle_solid)

insert_shape = insert_shape.translate((0, 0, -insert_thickness / 2))

# ============================================================
# 3. SPLINE CAVITY
# ============================================================

r_avg = (spline_inner_r + spline_outer_r) / 2.0
r_amp = (spline_outer_r - spline_inner_r) / 2.0

tooth_pts = []
steps_per_tooth = 20
for t in range(spline_teeth_count):
    base_angle = 2 * math.pi * t / spline_teeth_count
    tooth_width = 2 * math.pi / spline_teeth_count
    for s in range(steps_per_tooth):
        frac = s / steps_per_tooth
        angle = base_angle + frac * tooth_width
        r = r_avg + r_amp * math.sin(spline_teeth_count * angle)
        tooth_pts.append((r * math.cos(angle), r * math.sin(angle)))

spline_cut = (
    cq.Workplane("XY")
    .workplane(offset=body_top + DELTA)
    .polyline(tooth_pts)
    .close()
    .extrude(-(spline_cavity_depth + 2 * DELTA))
)

lead_in_cut = cq.Solid.makeCone(
    spline_cavity_dia / 2.0,
    lead_in_dia / 2.0,
    lead_in_depth,
    pnt=cq.Vector(0, 0, body_top - lead_in_depth),
)

# ============================================================
# 4. FINAL COUPLER
# ============================================================

result = (
    main_body.cut(insert_shape).cut(spline_cut).cut(cq.Workplane("XY").add(lead_in_cut))
)

print(f"Body top: {body_top} mm")
print(f"Spline cavity max dia: {spline_cavity_dia} mm")
print(f"Volume: {result.val().Volume():.1f} mm3")  # type: ignore[reportAttributeAccessIssue]

cq.exporters.export(result, "coupler.step")
cq.exporters.export(result, "coupler.stl")
print("Exported coupler.step and coupler.stl")
