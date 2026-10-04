#!/usr/bin/env python3
"""Generate side and top cross-section diagrams with dimensions for the coupler."""

import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as MplCircle

from params import *


def dim_arrow(
    ax, x1, y1, x2, y2, text, offset_x=0.0, offset_y=0.0, fontsize=9, color="blue"
):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops={"arrowstyle": "<->", "color": color, "lw": 1.2},
    )
    mx = (x1 + x2) / 2 + offset_x
    my = (y1 + y2) / 2 + offset_y
    ax.text(
        mx,
        my,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=color,
        fontweight="bold",
        bbox={
            "boxstyle": "round,pad=0.2",
            "facecolor": "white",
            "edgecolor": color,
            "alpha": 0.8,
        },
    )


def generate_side_section(path="images/cross_section_side.png"):
    fig, ax = plt.subplots(1, 1, figsize=(12, 14))
    ax.set_aspect("equal")
    ax.set_title(
        "SIDE CROSS-SECTION (all dimensions in mm)",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )

    # Right-half profile
    rx = [
        lower_stem_od / 2,
        lower_stem_od / 2,
        upper_body_od / 2,
        upper_body_od / 2,
        flange_od / 2,
        flange_od / 2,
    ]
    ry = [0, z_stem_top, z_stem_top, z_upper_top, z_upper_top, body_top]

    # Full profile (mirror)
    px = [-x for x in reversed(rx)] + rx
    py = list(reversed(ry)) + ry
    ax.plot(px, py, "k-", linewidth=2)

    # Insert cavity
    insert_od = insert_hex_flat_to_flat + insert_circle_dia
    ix = [-insert_od / 2, insert_od / 2, insert_od / 2, -insert_od / 2, -insert_od / 2]
    iy = [0, 0, insert_thickness, insert_thickness, 0]
    ax.fill(ix, iy, color="yellow", alpha=0.3)
    ax.plot(ix, iy, "r--", linewidth=1.5, label="Metallic Insert Cavity")

    # Spline cavity
    spline_r = spline_cavity_dia / 2
    sx = [-spline_r, spline_r, spline_r, -spline_r, -spline_r]
    sy = [
        body_top - spline_cavity_depth,
        body_top - spline_cavity_depth,
        body_top,
        body_top,
        body_top - spline_cavity_depth,
    ]
    ax.fill(sx, sy, color="lightgreen", alpha=0.3)
    ax.plot(sx, sy, "g--", linewidth=1.5, label="Spline Cavity")

    li_r_top = lead_in_dia / 2
    li_r_bot = spline_cavity_dia / 2
    li_x = [-li_r_top, -li_r_bot, li_r_bot, li_r_top, li_r_top]
    li_y = [
        body_top,
        body_top - lead_in_depth,
        body_top - lead_in_depth,
        body_top,
        body_top,
    ]
    ax.fill(li_x, li_y, color="deepskyblue", alpha=0.4)
    ax.plot(li_x, li_y, color="dodgerblue", linewidth=1.5, label="Lead-in Cone")

    ax.axvline(x=0, color="gray", linestyle=":", linewidth=0.5)

    dim_arrow(
        ax,
        -lower_stem_od / 2,
        -3,
        lower_stem_od / 2,
        -3,
        f"{lower_stem_od}",
        offset_y=-2,
    )
    dim_arrow(
        ax,
        flange_od / 2 + 5,
        0,
        flange_od / 2 + 5,
        z_stem_top,
        f"{lower_stem_height}",
        offset_x=5,
    )
    dim_arrow(
        ax,
        -upper_body_od / 2,
        z_stem_top - 2,
        upper_body_od / 2,
        z_stem_top - 2,
        f"{upper_body_od}",
        offset_y=-2,
    )
    dim_arrow(
        ax,
        flange_od / 2 + 5,
        z_stem_top,
        flange_od / 2 + 5,
        z_upper_top,
        f"{upper_body_height}",
        offset_x=5,
    )
    dim_arrow(
        ax,
        -flange_od / 2,
        body_top + 3,
        flange_od / 2,
        body_top + 3,
        f"{flange_od}",
        offset_y=2,
    )
    dim_arrow(
        ax,
        flange_od / 2 + 5,
        z_upper_top,
        flange_od / 2 + 5,
        body_top,
        f"{flange_height}",
        offset_x=5,
    )
    dim_arrow(
        ax,
        -flange_od / 2 - 8,
        0,
        -flange_od / 2 - 8,
        body_top,
        f"{body_top}",
        offset_x=-6,
    )

    ax.annotate(
        "",
        xy=(-insert_hex_flat_to_flat / 2, insert_thickness + 4),
        xytext=(insert_hex_flat_to_flat / 2, insert_thickness + 4),
        arrowprops={"arrowstyle": "<->", "color": "darkred", "lw": 1},
    )
    ax.text(
        0,
        insert_thickness + 5,
        f"{insert_hex_flat_to_flat} (hex f-f)",
        ha="center",
        va="center",
        fontsize=8,
        color="darkred",
        bbox={
            "boxstyle": "round,pad=0.2",
            "facecolor": "white",
            "edgecolor": "darkred",
            "alpha": 0.8,
        },
    )
    dim_arrow(
        ax,
        -insert_od / 2,
        insert_thickness + 1,
        insert_od / 2,
        insert_thickness + 1,
        f"~{insert_od:.1f}",
        offset_y=1.5,
        fontsize=7,
    )
    dim_arrow(
        ax,
        insert_od / 2 + 2,
        0,
        insert_od / 2 + 2,
        insert_thickness,
        f"{insert_thickness}",
        offset_x=4,
        fontsize=8,
    )

    dim_arrow(
        ax,
        -spline_r,
        body_top + 3,
        spline_r,
        body_top + 3,
        f"{spline_cavity_dia}",
        offset_y=5,
        fontsize=8,
    )
    dim_arrow(
        ax,
        -spline_r - 5,
        body_top - spline_cavity_depth,
        -spline_r - 5,
        body_top,
        f"{spline_cavity_depth}",
        offset_x=-6,
    )

    li_r_top = lead_in_dia / 2
    li_r_bot = spline_cavity_dia / 2
    dim_arrow(
        ax,
        -li_r_top,
        body_top + 1,
        li_r_top,
        body_top + 1,
        f"{lead_in_dia}",
        offset_y=1,
        fontsize=7,
        color="dodgerblue",
    )
    dim_arrow(
        ax,
        li_r_bot + 3,
        body_top - lead_in_depth,
        li_r_bot + 3,
        body_top,
        f"{lead_in_depth}",
        offset_x=4,
        fontsize=7,
        color="dodgerblue",
    )

    ax.set_xlim(-35, 35)
    ax.set_ylim(-8, body_top + 12)
    ax.set_xlabel("X (mm)", fontsize=12)
    ax.set_ylabel("Z / Height (mm)", fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {path}")


def generate_top_section(path="images/cross_section_top.png"):
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    ax.set_aspect("equal")
    ax.set_title(
        "TOP VIEW - Metallic Insert Cross-Section\n(hexagon with circles on vertices)",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )

    hex_corner_r = insert_hex_flat_to_flat / (2 * math.cos(math.pi / 6))
    circle_r = insert_circle_dia / 2

    hx, hy = [], []
    for i in range(6):
        angle = 2 * math.pi * i / 6 + math.pi / 6
        hx.append(hex_corner_r * math.cos(angle))
        hy.append(hex_corner_r * math.sin(angle))
    hx.append(hx[0])
    hy.append(hy[0])

    ax.plot(hx, hy, "k-", linewidth=2)
    ax.fill(hx, hy, color="lightyellow", alpha=0.5, label="Hexagon")

    for i in range(6):
        angle = 2 * math.pi * i / 6 + math.pi / 6
        cx = hex_corner_r * math.cos(angle)
        cy = hex_corner_r * math.sin(angle)
        circle = MplCircle(
            (cx, cy),
            circle_r,
            facecolor="gold",
            alpha=0.5,
            edgecolor="black",
            linewidth=1.5,
        )
        ax.add_patch(circle)

    stem_r = lower_stem_od / 2
    ax.add_patch(
        MplCircle(
            (0, 0),
            stem_r,
            facecolor="lightblue",
            alpha=0.2,
            edgecolor="blue",
            linewidth=1,
            linestyle="--",
        )
    )
    ax.plot(0, 0, "k+", markersize=10, markeredgewidth=2)

    dim_arrow(
        ax,
        -insert_hex_flat_to_flat / 2,
        -hex_corner_r - 5,
        insert_hex_flat_to_flat / 2,
        -hex_corner_r - 5,
        f"Hex flat-to-flat: {insert_hex_flat_to_flat}mm",
        fontsize=10,
    )

    angle0 = 2 * math.pi * 0 / 6 + math.pi / 6
    cx0 = hex_corner_r * math.cos(angle0)
    cy0 = hex_corner_r * math.sin(angle0)
    ax.annotate(
        "",
        xy=(cx0 + circle_r + 1, cy0),
        xytext=(cx0 - circle_r - 1, cy0),
        arrowprops={"arrowstyle": "<->", "color": "darkred", "lw": 1},
    )
    ax.text(
        cx0 + circle_r + 4,
        cy0,
        f"Circle dia: {insert_circle_dia}mm",
        ha="left",
        fontsize=9,
        color="darkred",
        bbox={
            "boxstyle": "round,pad=0.2",
            "facecolor": "white",
            "edgecolor": "darkred",
            "alpha": 0.8,
        },
    )

    total_r = hex_corner_r + circle_r
    dim_arrow(
        ax,
        -total_r,
        0,
        total_r,
        0,
        f"Total dia: {total_r * 2:.1f}mm",
        offset_y=2,
        fontsize=10,
        color="green",
    )

    spline_r = spline_cavity_dia / 2
    ax.add_patch(
        MplCircle(
            (0, 0),
            spline_r,
            facecolor="lightgreen",
            alpha=0.1,
            edgecolor="green",
            linewidth=1.5,
            linestyle="--",
        )
    )
    ax.text(
        0,
        spline_r + 2,
        f"Spline cavity dia: {spline_cavity_dia}mm",
        ha="center",
        fontsize=9,
        color="green",
        bbox={
            "boxstyle": "round,pad=0.2",
            "facecolor": "white",
            "edgecolor": "green",
            "alpha": 0.8,
        },
    )

    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_xlabel("X (mm)", fontsize=12)
    ax.set_ylabel("Y (mm)", fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {path}")


if __name__ == "__main__":
    generate_side_section()
    generate_top_section()
    print("Done")
