"""
Standalone link-chip images ("Field Notes" theme).

These are tiny, tightly-cropped SVGs (not full 800px cards) meant to be
wrapped in a real <a href> in README.md - an <img> inside a real anchor tag
is clickable on GitHub even though an <a> drawn inside an SVG is not.
"""

from themes.field_notes.theme import COLORS, FONT_MONO, svg_header, svg_footer, text_element

CHIP_H = 20


def _link_svg(label: str) -> str:
    w = len(label) * 7.1 + 4

    lines = [svg_header(w, CHIP_H)]
    lines.append(text_element(0, CHIP_H - 5, label, size=12.5, fill=COLORS["deep_purple"],
                               weight="600", family=FONT_MONO))
    lines.append(svg_footer())
    return "\n".join(lines)


def generate_link_site_svg(data: dict | None = None) -> str:
    return _link_svg("Personal site ↗")


def generate_link_group_svg(data: dict | None = None) -> str:
    return _link_svg("Mizuno Group ↗")
