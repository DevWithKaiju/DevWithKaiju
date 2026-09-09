"""
Theme: "Broadsheet" - bold display type, solid color blocks and thin
rules instead of cards; a newspaper/poster-infographic treatment of the same
content as the "Field Notes" theme.
"""

from common.svg_primitives import svg_open, svg_close, rect, text_element as _text_element

COLORS = {
    "purple_block": "#8870a4",   # Solid accent block (Kaiju hero)
    "lavender": "#f5f0f9",       # Light text-on-purple / secondary tint
    "teal": "#14b8a6",           # Growth bar fill / highlighted figures
    "ink": "#27222c",            # Headlines / primary text
    "muted": "#475569",          # Captions / kickers
    "hairline": "rgba(136,112,164,0.35)",  # Soft rule dividers
    "chart_other": "#84809a",    # Neutral "Other" bucket - deliberately unsaturated: a
                                  # catch-all reads as receding, not as its own identity.
    "white": "#FFFFFF",
}

# A categorical palette for charts (e.g. the Toolkit language bar), picked and
# ORDER-validated with the dataviz skill's validate_palette.js rather than
# eyeballed - GitHub's per-language brand colors read as a clash of unrelated
# hues against the rest of the page, but a palette narrowed to just this
# theme's purple/teal family fails CVD separation between adjacent segments.
# This is four genuinely distinct hues (still cool-leaning, no hot
# orange/yellow) confirmed pairwise distinguishable in this exact order -
# reordering or swapping a hue requires re-validating, not eyeballing.
CHART_PALETTE = ["#c2447e", "#5a4fb0", "#0f9e8e", "#3a6bc4"]

# Web-safe stacks only: SVGs referenced via <img> in a GitHub README render in an
# "image context" that will not fetch external @font-face/webfont resources, so
# the "big bold condensed" display face is approximated with weight, not a webfont.
FONT_DISPLAY = "'Arial Narrow', 'Helvetica Neue Condensed', Arial, sans-serif"
FONT_BODY = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
FONT_MONO = "'SF Mono', 'Cascadia Code', Consolas, 'Courier New', monospace"


def svg_header(width: int, height: int, extra_defs: str = "", extra_style: str = "") -> str:
    style = f"text {{ font-family: {FONT_BODY}; }}\n{extra_style}"
    return svg_open(width, height, extra_defs=extra_defs, extra_style=style)


def svg_footer() -> str:
    return svg_close()


def text_element(x: float, y: float, content: str, size: float, fill: str | None = None,
                  anchor: str = "start", weight: str = "normal", family: str | None = None,
                  style: str = "normal", letter_spacing: float | None = None, extra: str = "") -> str:
    return _text_element(x, y, content, size=size, fill=fill or COLORS["ink"], family=family or FONT_BODY,
                          anchor=anchor, weight=weight, style=style, letter_spacing=letter_spacing, extra=extra)


def kicker(x: float, y: float, content: str, anchor: str = "start", color: str | None = None) -> str:
    color = color or COLORS["muted"]
    return text_element(x, y, content.upper(), size=10.5, fill=color, anchor=anchor,
                         weight="600", family=FONT_MONO, letter_spacing=1.6)


def hairline(x1: float, y: float, x2: float, color: str | None = None, width: float = 1.5) -> str:
    color = color or COLORS["hairline"]
    return f'  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="{width}" />'
