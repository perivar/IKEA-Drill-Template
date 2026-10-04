"""Generate spline test pieces with sinusoidal profile and wider gaps.

Usage:
    source .venv/bin/activate
    python generate_spline_test_pieces.py

Each piece is a cylinder with the sinusoidal spline cavity cut into the top face.
The inner radius is progressively increased to make the teeth shorter, which
creates wider effective gaps for thicker blender teeth.

The inner radius value is engraved on the outer side wall for identification.
Also generates an SVG comparison of all profiles.
"""

import math
import os

import cadquery as cq

from params import DELTA, spline_inner_r, spline_outer_r, spline_teeth_count

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTER_R = spline_outer_r  # 12.0 mm (fixed — matches original)
PIECE_HEIGHT = 3.0
PIECE_OD = 28.0

# Current inner_r = 9.0mm. Increasing it makes teeth shorter and gaps wider.
INNER_RADII = [9.0 + i * 0.2 for i in range(6)]

OUTPUT_DIR = "test_pieces"


# ---------------------------------------------------------------------------
# Sinusoidal profile (matches the original coupler design)
# ---------------------------------------------------------------------------


def _sinusoidal_profile(teeth_count, inner_r, outer_r, steps_per_tooth=60):
    """Generate the same sinusoidal spline profile as the original coupler."""
    r_avg = (inner_r + outer_r) / 2.0
    r_amp = (outer_r - inner_r) / 2.0

    points = []
    for t in range(teeth_count):
        base_angle = 2 * math.pi * t / teeth_count
        tooth_width = 2 * math.pi / teeth_count
        for s in range(steps_per_tooth):
            frac = s / steps_per_tooth
            angle = base_angle + frac * tooth_width
            r = r_avg + r_amp * math.sin(teeth_count * angle)
            points.append((r * math.cos(angle), r * math.sin(angle)))

    return points


# ---------------------------------------------------------------------------
# Test piece builder
# ---------------------------------------------------------------------------


def _make_test_piece(inner_r, outer_r, piece_height, piece_od, label_text):
    """Create a test piece: cylinder with sinusoidal spline cavity on top.

    The label is engraved on the outer side wall for easy identification.
    """
    cylinder = cq.Workplane("XY").circle(piece_od / 2).extrude(piece_height)

    tooth_pts = _sinusoidal_profile(
        teeth_count=spline_teeth_count,
        inner_r=inner_r,
        outer_r=outer_r,
        steps_per_tooth=60,
    )

    spline_cut = (
        cq.Workplane("XY")
        .workplane(offset=piece_height + DELTA)
        .polyline(tooth_pts)
        .close()
        .extrude(-(piece_height + 2 * DELTA))
    )

    result = cylinder.cut(spline_cut)

    try:
        font_size = 2.5
        label = (
            cq.Workplane("YZ")
            .workplane(offset=piece_od / 2 - 0.3)
            .center(0, piece_height / 2)
            .text(label_text, fontsize=font_size, distance=1.0)
        )
        result = result.cut(label)
    except Exception:  # noqa: BLE001, S110
        pass

    return result


# ---------------------------------------------------------------------------
# SVG comparison
# ---------------------------------------------------------------------------

_SVG_WIDTH = 1000
_SVG_HEIGHT = 700
_SVG_CX = _SVG_WIDTH / 2
_SVG_CY = 350
_SVG_SCALE = 22


def _svg_header():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{_SVG_WIDTH}" height="{_SVG_HEIGHT}"
     viewBox="0 0 {_SVG_WIDTH} {_SVG_HEIGHT}" style="background: white;">
  <style>
    text {{ font-family: monospace; font-size: 11px; }}
    title {{ font-size: 16px; font-weight: bold; }}
  </style>
"""


def _profile_to_path(points, color, stroke_w=1.5, fill="none", opacity=1.0):
    if not points:
        return ""
    parts = [
        f"M {_SVG_CX + points[0][0] * _SVG_SCALE:.2f} {_SVG_CY - points[0][1] * _SVG_SCALE:.2f}"
    ]
    for x, y in points[1:]:
        parts.append(f"L {_SVG_CX + x * _SVG_SCALE:.2f} {_SVG_CY - y * _SVG_SCALE:.2f}")
    parts.append("Z")
    return (
        f'  <path d="{" ".join(parts)}" fill="{fill}" stroke="{color}" '
        f'stroke-width="{stroke_w}" opacity="{opacity}"/>\n'
    )


def _generate_svg(inner_radii, output_path):
    """Generate an SVG comparing all sinusoidal profiles."""
    colors = ["#2196F3", "#e91e63", "#ff9800", "#4caf50", "#f44336", "#9c27b0"]

    svg = _svg_header()
    svg += f'  <text x="{_SVG_CX}" y="30" text-anchor="middle" class="title">Sinusoidal Spline — Varying Inner Radius</text>\n'
    svg += f'  <text x="{_SVG_CX}" y="48" text-anchor="middle" font-size="12" fill="#666">{spline_teeth_count} teeth, outer_r={OUTER_R}mm (fixed)</text>\n'

    svg += f'  <circle cx="{_SVG_CX}" cy="{_SVG_CY}" r="{OUTER_R * _SVG_SCALE}" fill="none" stroke="#ccc" stroke-width="0.5" stroke-dasharray="4 4"/>\n'
    svg += f'  <circle cx="{_SVG_CX}" cy="{_SVG_CY}" r="{spline_inner_r * _SVG_SCALE}" fill="none" stroke="#ccc" stroke-width="0.5" stroke-dasharray="4 4"/>\n'

    svg += f'  <line x1="{_SVG_CX - OUTER_R * _SVG_SCALE - 15}" y1="{_SVG_CY}" x2="{_SVG_CX + OUTER_R * _SVG_SCALE + 15}" y2="{_SVG_CY}" stroke="#eee" stroke-width="0.5"/>\n'
    svg += f'  <line x1="{_SVG_CX}" y1="{_SVG_CY - OUTER_R * _SVG_SCALE - 15}" x2="{_SVG_CX}" y2="{_SVG_CY + OUTER_R * _SVG_SCALE + 15}" stroke="#eee" stroke-width="0.5"/>\n'

    for ir, color in zip(inner_radii, colors):
        pts = _sinusoidal_profile(spline_teeth_count, ir, OUTER_R)
        sw = 2.5 if ir == 9.0 else 1.5
        svg += _profile_to_path(pts, color, sw, opacity=0.8)

    svg += f'  <text x="{_SVG_CX}" y="{_SVG_CY - OUTER_R * _SVG_SCALE - 8}" text-anchor="middle" font-size="10" fill="#999">r={OUTER_R}mm</text>\n'
    svg += f'  <text x="{_SVG_CX}" y="{_SVG_CY - spline_inner_r * _SVG_SCALE + 20}" text-anchor="middle" font-size="10" fill="#999">r={spline_inner_r}mm (original)</text>\n'

    lx, ly = 20, 70
    svg += f'  <text x="{lx}" y="{ly}" font-weight="bold" font-size="13">Inner radius (tooth tip):</text>\n'
    for ir, color in zip(inner_radii, colors):
        ly += 20
        marker = " (current)" if ir == 9.0 else ""
        svg += f'  <line x1="{lx}" y1="{ly - 4}" x2="{lx + 25}" y2="{ly - 4}" stroke="{color}" stroke-width="2.5"/>\n'
        svg += f'  <text x="{lx + 30}" y="{ly}" font-size="11" fill="{color}">{ir:.1f}mm — tooth_h={OUTER_R - ir:.1f}mm{marker}</text>\n'

    svg += "</svg>"

    with open(output_path, "w") as f:
        f.write(svg)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Spline: {spline_teeth_count} teeth, outer_r={OUTER_R} mm (fixed)")
    print(f"Piece: {PIECE_OD} mm OD x {PIECE_HEIGHT} mm\n")

    for ir in INNER_RADII:
        label = f"IR{ir:.1f}"
        piece = _make_test_piece(
            inner_r=ir,
            outer_r=OUTER_R,
            piece_height=PIECE_HEIGHT,
            piece_od=PIECE_OD,
            label_text=label,
        )
        filename = f"{OUTPUT_DIR}/spline_inner_{ir:.1f}mm.stl"
        cq.exporters.export(piece, filename)
        tooth_height = OUTER_R - ir
        print(
            f"  {filename}  inner_r={ir:.1f} mm  tooth_h={tooth_height:.1f} mm  label='{label}'"
        )

    svg_path = f"{OUTPUT_DIR}/spline_profile_comparison.svg"
    _generate_svg(INNER_RADII, svg_path)
    print(f"  {svg_path}  (profile comparison)")

    print(f"\nDone — {len(INNER_RADII)} test pieces + SVG in '{OUTPUT_DIR}/'")
    print(
        "Each piece has the sinusoidal profile with progressively shorter teeth (= wider gaps)."
    )
    print("Label on outer side wall: 'IR<value>' = inner radius in mm.")


if __name__ == "__main__":
    main()
