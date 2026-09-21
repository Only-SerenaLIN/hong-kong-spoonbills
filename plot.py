# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""
Read the file in data/, make one picture, save it to out/.

    uv run plot.py

Three parts, and you will replace all three: rows() reads the file the way *your*
file needs reading, the loop in main() picks the numbers out of it, and the plot at
the bottom is the transformation you chose. Print before you plot.
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

FILE = "0001661-260916113435855.csv"
PICTURE = "plot.png"                           # what goes into out/, and into the README

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"


def rows(path):
    """Read the tab-separated GBIF occurrence table."""
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main():
    table = rows(DATA)
    print(f"{DATA.name}: {len(table)} rows. The first one: {table[0]}")

    records = []
    for row in table:
        year = int(row["year"])
        if 2020 <= year <= 2025:
            records.append({
                "month": int(row["month"]),
                "latitude": float(row["decimalLatitude"]),
                "longitude": float(row["decimalLongitude"]),
            })

    print(f"{len(records)} records from 2020 to 2025")

    month_names = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ]

    fig, axes = plt.subplots(
        3, 4, figsize=(12, 9), sharex=True, sharey=True
    )

    for month_number, ax in enumerate(axes.flat, start=1):
        points = [
            record for record in records
            if record["month"] == month_number
        ]

        ax.scatter(
            [point["longitude"] for point in points],
            [point["latitude"] for point in points],
            s=7,
            alpha=0.25,
            color="#136f8a",
            edgecolors="none",
        )
        ax.set_title(
        f"{month_names[month_number - 1]} · {len(points):,} records"
        )
        ax.set_xlim(113.80, 114.35)
        ax.set_ylim(22.18, 22.65)
        ax.grid(color="#dddddd", linewidth=0.5)

    fig.suptitle(
        "Black-faced Spoonbill observations in Hong Kong by month, 2020–2025"
    )
    fig.supxlabel("longitude")
    fig.supylabel("latitude")
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150)
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()
