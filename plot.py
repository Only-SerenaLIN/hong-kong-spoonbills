# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Read the GBIF occurrence table and draw a circular migration calendar.

    uv run plot.py

The angle represents the month. The distance from the centre represents the
number of occurrence records, using a square-root scale so that quiet summer
months remain visible beside the winter peak.
"""

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.path import Path as MarkerPath

FILE = "0001661-260916113435855.csv"
PICTURE = "plot.png"

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"

PAPER = "#f4efe6"
INK = "#24312f"
MUTED = "#8b918b"
WATER = "#176b72"
WATER_LIGHT = "#77aeb0"
REED = "#c78645"
GRID = "#d7d1c7"


def rows(path):
    """Read the tab-separated GBIF occurrence table."""
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def bird_marker():
    """A simple flying-bird outline, drawn as two curved wings."""
    vertices = [
        (-1.00, 0.00),
        (-0.66, 0.62),
        (-0.24, 0.52),
        (0.00, 0.04),
        (0.24, 0.52),
        (0.66, 0.62),
        (1.00, 0.00),
    ]
    codes = [MarkerPath.MOVETO] + [MarkerPath.CURVE4] * 6
    return MarkerPath(vertices, codes)


def main():
    table = rows(DATA)

    records = []
    for row in table:
        if not row["year"] or not row["month"]:
            continue
        year = int(row["year"])
        if 2020 <= year <= 2025:
            records.append({
                "month": int(row["month"]),
                "latitude": float(row["decimalLatitude"]),
                "longitude": float(row["decimalLongitude"]),
            })

    counts = [
        sum(record["month"] == month for record in records)
        for month in range(1, 13)
    ]
    print(f"{DATA.name}: {len(table)} rows")
    print(f"{len(records)} records from 2020 to 2025")
    print("monthly counts:", counts)

    month_names = [
        "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
        "JUL", "AUG", "SEP", "OCT", "NOV", "DEC",
    ]
    angles = np.linspace(0, 2 * math.pi, 12, endpoint=False)

    # Keep the quiet months visible while preserving the order of the counts.
    inner_radius = 0.25
    radii = np.array([
        inner_radius + 0.64 * math.sqrt(count / max(counts))
        for count in counts
    ])

    # A data-driven colour gradient: quiet months are pale; busy months are deep teal.
    colour_scale = LinearSegmentedColormap.from_list(
        "spoonbill_season",
        ["#c9cec5", "#78aaa5", "#176b72", "#0b4f59"],
    )
    colour_norm = Normalize(
        vmin=math.sqrt(min(counts)),
        vmax=math.sqrt(max(counts)),
    )
    colours = [colour_scale(colour_norm(math.sqrt(count))) for count in counts]

    figure = plt.figure(figsize=(9, 9), facecolor=PAPER)
    axes = figure.add_subplot(111, projection="polar", facecolor=PAPER)
    figure.subplots_adjust(left=0.08, right=0.92, top=0.86, bottom=0.08)

    axes.set_theta_zero_location("N")
    axes.set_theta_direction(-1)
    axes.set_ylim(0, 1.20)
    axes.spines["polar"].set_visible(False)
    axes.set_xticks([])
    axes.set_yticks([])
    axes.grid(False)

    # Faint calendar structure.
    circle = np.linspace(0, 2 * math.pi, 361)
    for radius in (inner_radius, 0.57, 0.89):
        axes.plot(circle, np.full_like(circle, radius), color=GRID, linewidth=0.8, zorder=0)
    for angle in angles:
        axes.plot([angle, angle], [inner_radius, 0.91], color=GRID, linewidth=0.7, zorder=0)

    # The closed annual trace: October arrives, winter swells, summer falls quiet.
    closed_angles = np.append(angles, angles[0] + 2 * math.pi)
    closed_radii = np.append(radii, radii[0])
    axes.fill(closed_angles, closed_radii, color=WATER_LIGHT, alpha=0.16, zorder=1)

    # Draw short pieces so the annual trace changes colour smoothly between months.
    for index in range(12):
        next_index = (index + 1) % 12
        start_angle = angles[index]
        end_angle = angles[next_index] if next_index else 2 * math.pi
        steps = 24
        segment_angles = np.linspace(start_angle, end_angle, steps + 1)
        segment_radii = np.linspace(radii[index], radii[next_index], steps + 1)
        segment_counts = np.linspace(counts[index], counts[next_index], steps + 1)
        for step in range(steps):
            colour_value = math.sqrt((segment_counts[step] + segment_counts[step + 1]) / 2)
            axes.plot(
                segment_angles[step:step + 2],
                segment_radii[step:step + 2],
                color=colour_scale(colour_norm(colour_value)),
                linewidth=2.6,
                solid_capstyle="round",
                zorder=2,
            )

    # Bird silhouettes mark each month. Their position, not their size, carries the value.
    axes.scatter(
        angles,
        radii,
        marker=bird_marker(),
        s=520,
        facecolors="none",
        edgecolors=colours,
        linewidths=2.2,
        zorder=4,
    )

    # The outer band repeats the same count gradient at a glance.
    for angle, colour in zip(angles, colours):
        axes.bar(
            angle,
            0.025,
            width=(2 * math.pi / 12) * 0.82,
            bottom=1.035,
            color=colour,
            alpha=0.92,
            linewidth=0,
            zorder=1,
        )

    for angle, month_name, count in zip(angles, month_names, counts):
        axes.text(
            angle,
            1.13,
            f"{month_name}\n{count:,}",
            ha="center",
            va="center",
            color=INK,
            fontsize=9.5,
            linespacing=1.35,
        )

    axes.text(
        0,
        0,
        "WINTER\nVISITORS",
        ha="center",
        va="center",
        color=INK,
        fontsize=15,
        fontweight="bold",
        linespacing=1.15,
    )
    axes.text(
        math.pi,
        0.14,
        "Hong Kong",
        ha="center",
        va="center",
        color=MUTED,
        fontsize=9,
    )

    figure.suptitle(
        "A YEAR WITH THE BLACK-FACED SPOONBILL",
        y=0.965,
        color=INK,
        fontsize=17,
        fontweight="bold",
    )
    figure.text(
        0.5,
        0.915,
        "GBIF occurrence records by month · Hong Kong · 2020–2025",
        ha="center",
        color=MUTED,
        fontsize=10.5,
    )
    figure.text(
        0.5,
        0.035,
        "Farther and darker means more monthly records · square-root scale",
        ha="center",
        color=MUTED,
        fontsize=8.5,
    )

    # Seasonal cues sit in the footer so they never cover the data or month labels.
    figure.text(
        0.36,
        0.066,
        "RETURN · OCTOBER",
        ha="center",
        color=REED,
        fontsize=8.5,
        fontweight="bold",
    )
    figure.text(
        0.64,
        0.066,
        "DEPART · MAY",
        ha="center",
        color=REED,
        fontsize=8.5,
        fontweight="bold",
    )

    OUT.mkdir(exist_ok=True)
    figure.savefig(OUT / PICTURE, dpi=180, facecolor=figure.get_facecolor())
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()
