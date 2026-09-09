"""
Theme: "Broadsheet" - bold display type, solid color blocks and thin
rules instead of cards; a newspaper/poster-infographic treatment of the same
content as the "Field Notes" theme.
"""

from common.svg_primitives import svg_open, svg_close, rect, text_element as _text_element

COLORS = {
    "purple_block": "#8870a4",   # Solid accent block (Kaiju hero)
    "dusty_purple": "#b39cd0",   # Lighter purple accent
    "lavender": "#f5f0f9",       # Light text-on-purple / secondary tint
    "lavender_accent": "#c9b6e4",  # Light purple tint (chart filler)
    "teal": "#14b8a6",           # Growth bar fill / highlighted figures
    "mint": "#2dd4bf",           # Lighter teal accent
    "ink": "#27222c",            # Headlines / primary text
    "ink_soft": "#6b6178",       # Muted purple-gray (chart filler)
    "muted": "#475569",          # Captions / kickers
    "hairline": "rgba(136,112,164,0.35)",  # Soft rule dividers
    "white": "#FFFFFF",
}

# A ranked, in-family palette for categorical charts (e.g. the Toolkit language
# bar) - alternating purple/teal tones instead of GitHub's per-language brand
# colors, which read as a clash of unrelated hues against the rest of the page.
CHART_PALETTE = [
    COLORS["purple_block"],
    COLORS["teal"],
    COLORS["dusty_purple"],
    COLORS["mint"],
    COLORS["ink_soft"],
    COLORS["lavender_accent"],
]

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
