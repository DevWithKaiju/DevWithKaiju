"""
Theme: "Field Notes" - a lab-notebook / specimen-card aesthetic built on the
site's real brand palette (https://devwithkaiju.github.io).
"""

from common.svg_primitives import svg_open, svg_close, rect, text_element as _text_element

COLORS = {
    "dusty_purple": "#b39cd0",     # Primary accent (borders, small highlights)
    "deep_purple": "#8870a4",      # Ink accent - kickers, labels, links
    "mint": "#2dd4bf",             # Secondary accent
    "teal": "#14b8a6",             # Growth bar fill / link hover
    "lavender": "#f5f0f9",         # Hero (Kaiju) card background
    "lavender_accent": "#c9b6e4",  # Misc / "other" language bucket
    "card_bg": "#FAFAFC",          # Standard card background
    "track_bg": "#f1f5f9",         # Progress-bar track background
    "border": "#e2e8f0",           # Hairline card borders / dividers
    "ink": "#27222c",              # Headings / primary values
    "text": "#475569",             # Body / secondary text
    "text_faint": "#94a3b8",       # Tertiary / meta text
    "white": "#FFFFFF",
}

# Web-safe stacks only: SVGs referenced via <img> in a GitHub README render in an
# "image context" that will not fetch external @font-face/webfont resources.
FONT_SERIF = "Georgia, 'Iowan Old Style', 'Palatino Linotype', Palatino, serif"
FONT_MONO = "'SF Mono', 'Cascadia Code', Consolas, 'Courier New', monospace"

TEXT_BODY = 14.5


def svg_header(width: int, height: int, extra_defs: str = "", extra_style: str = "") -> str:
    defs = f'''<filter id="cardShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="3" dy="3" stdDeviation="0" flood-color="{COLORS['deep_purple']}" flood-opacity="0.08"/>
    </filter>
    {extra_defs}'''
    style = f"text {{ font-family: {FONT_SERIF}; }}\n{extra_style}"
    return svg_open(width, height, extra_defs=defs, extra_style=style)


def svg_footer() -> str:
    return svg_close()


def rounded_rect(x: float, y: float, w: float, h: float, rx: float = 3, fill: str | None = None,
                  stroke: str | None = None, stroke_width: float = 1, opacity: float = 1, extra: str = "") -> str:
    return rect(x, y, w, h, rx=rx, fill=fill or COLORS["card_bg"], stroke=stroke,
                stroke_width=stroke_width, opacity=opacity, extra=extra)


def text_element(x: float, y: float, content: str, size: float = TEXT_BODY, fill: str | None = None,
                  anchor: str = "start", weight: str = "normal", family: str | None = None,
                  style: str = "normal", letter_spacing: float | None = None, extra: str = "") -> str:
    return _text_element(x, y, content, size=size, fill=fill or COLORS["text"], family=family or FONT_SERIF,
                          anchor=anchor, weight=weight, style=style, letter_spacing=letter_spacing, extra=extra)


def card_shell(width: float, height: float, x: float = 0, y: float = 0,
               bg: str | None = None, rx: float = 3) -> str:
    """A flat paper card: subtle border + soft directional shadow. No inner title/divider -
    each generator draws its own kicker row so section headers stay lightweight."""
    bg = bg or COLORS["card_bg"]
    return rounded_rect(x + 0.75, y + 0.75, width - 1.5, height - 1.5, rx=rx, fill=bg,
                         stroke=COLORS["border"], stroke_width=1.5, extra='filter="url(#cardShadow)"')


def kicker(x: float, y: float, content: str, anchor: str = "start", color: str | None = None) -> str:
    """Small letter-spaced mono label used as a section header ('ABOUT', 'FIELD DATA', ...)."""
    color = color or COLORS["deep_purple"]
    return text_element(x, y, content.upper(), size=10.5, fill=color, anchor=anchor,
                         weight="600", family=FONT_MONO, letter_spacing=1.4)
