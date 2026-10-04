"""Single source of truth for all coupler dimensions."""

DELTA = 0.1

# Main body
lower_stem_height = 7.1
upper_body_height = 14.4
flange_height = 4.0

flange_od = 45.25
upper_body_od = 30.6
lower_stem_od = 21.50
center_hole_dia = 5.6

lip_fillet_radius = 3.0
cb_fillet_radius = 2.0

# Metallic insert (hexagon with circles on vertices)
insert_hex_flat_to_flat = 14.0
insert_circle_dia = 2.2
insert_thickness = 7.7
insert_center_hole_dia = 5.5

# Spline cavity (12 teeth)
spline_teeth_count = 12
spline_cavity_depth = 15.0
spline_cavity_dia = 24.0
spline_inner_r = 9.0
spline_outer_r = spline_cavity_dia / 2

# Lead-in chamfer at top of spline cavity
lead_in_dia = 27.0
lead_in_depth = 2.0

# Derived heights
z_stem_top = lower_stem_height
z_upper_top = lower_stem_height + upper_body_height
body_top = z_upper_top + flange_height
