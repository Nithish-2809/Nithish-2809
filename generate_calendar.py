"""
Generates a custom-styled GitHub contribution calendar SVG:
rounded cells, black background, green palette — built from
your real public contribution data (no auth token needed).
"""
import re
import datetime
import urllib.request

USERNAME = "Nithish-2809"
OUTPUT_PATH = "assets/contribution-calendar.svg"

url = f"https://github.com/users/{USERNAME}/contributions"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("utf-8")

cells = re.findall(r'data-date="([^"]+)"[^>]*data-level="(\d)"', html)
dates = sorted((datetime.date.fromisoformat(d), int(l)) for d, l in cells)

first = dates[0][0]
first_sunday = first - datetime.timedelta(days=(first.weekday() + 1) % 7)

grid = {}
max_col = 0
for d, lvl in dates:
    col = (d - first_sunday).days // 7
    row = (d.weekday() + 1) % 7  # Sunday = 0
    grid[(row, col)] = lvl
    max_col = max(max_col, col)

# Black background, green intensity scale (darkest -> brightest)
palette = ["#0d1117", "#0e4429", "#006d32", "#26a641", "#39d353"]
bg = "#000000"

cell, gap = 11, 3
step = cell + gap
pad = 6
width = pad * 2 + (max_col + 1) * step
height = pad * 2 + 7 * step

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
svg.append(f'<rect width="100%" height="100%" fill="{bg}" rx="12"/>')
for (row, col), lvl in grid.items():
    x = pad + col * step
    y = pad + row * step
    color = palette[lvl] if lvl < len(palette) else palette[-1]
    svg.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" ry="3" fill="{color}"/>')
svg.append("</svg>")

import os
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    f.write("\n".join(svg))

print(f"Wrote {OUTPUT_PATH} ({width}x{height}, {len(grid)} cells)")
