"""
Standalone link-chip images ("Broadsheet" theme).

These are tiny, tightly-cropped SVGs (not full 800px cards) meant to be
wrapped in a real <a href> in README.md - an <img> inside a real anchor tag
is clickable on GitHub even though an <a> drawn inside an SVG is not.
"""

from themes.broadsheet.theme import COLORS, FONT_MONO, svg_header, svg_footer, text_element

CHIP_H = 34


def _chip_svg(label: str) -> str:
    text = label.upper()
    w = len(text) * 7.2 + 32

    lines = [svg_header(w, CHIP_H)]
    lines.append(f'  <rect x="0.75" y="0.75" width="{w - 1.5}" height="{CHIP_H - 1.5}" fill="none" '
                  f'stroke="{COLORS["ink"]}" stroke-width="1.5" />')
    lines.append(text_element(w / 2, CHIP_H / 2 + 4, text, size=11, fill=COLORS["ink"], anchor="middle",
                               weight="600", family=FONT_MONO, letter_spacing=0.6))
    lines.append(svg_footer())
    return "\n".join(lines)


def generate_link_site_svg(data: dict | None = None) -> str:
    return _chip_svg("Personal Site ↗")


def generate_link_group_svg(data: dict | None = None) -> str:
    return _chip_svg("Mizuno Group ↗")
