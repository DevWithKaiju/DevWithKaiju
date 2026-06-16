"""
Theme: Dusty Purple × Mint Green — Cute dark theme
Shared color palette, fonts, and SVG helper functions.
"""

# ─── Color Palette ──────────────────────────────────────────
COLORS = {
    "dusty_purple": "#9B8EC4",
    "deep_purple": "#7B6FA0",
    "mint_green": "#A8D8C8",
    "soft_mint": "#C5E8D9",
    "lavender": "#D4CCE6",
    "card_bg": "#2D2640",
    "dark_bg": "#1E1833",
    "text_light": "#E8E0F0",
    "text_muted": "#A89EC0",
    "locked_bg": "#252038",
    "locked_border": "#3A3350",
    "locked_text": "#5A5070",
    "gold": "#F0D080",
    "soft_pink": "#E8B4C8",
    "white": "#FFFFFF",
}

FONT_FAMILY = "'Segoe UI', 'Helvetica Neue', Ubuntu, Arial, sans-serif"


# ─── SVG Helpers ────────────────────────────────────────────

def svg_header(width: int, height: int, extra_defs: str = "", extra_style: str = "") -> str:
    """Return the opening <svg> tag with common defs (gradients, filters)."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="purpleMintGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{COLORS['dusty_purple']}" />
      <stop offset="100%" stop-color="{COLORS['mint_green']}" />
    </linearGradient>
    <linearGradient id="purpleMintGradH" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{COLORS['dusty_purple']}" />
      <stop offset="100%" stop-color="{COLORS['mint_green']}" />
    </linearGradient>
    <linearGradient id="cardBorderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{COLORS['dusty_purple']}" stop-opacity="0.5" />
      <stop offset="100%" stop-color="{COLORS['mint_green']}" stop-opacity="0.5" />
    </linearGradient>
    <filter id="softGlow">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="subtleShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="{COLORS['dark_bg']}" flood-opacity="0.5" />
    </filter>
    {extra_defs}
  </defs>
  <style>
    text {{ font-family: {FONT_FAMILY}; }}
    {extra_style}
  </style>'''


def svg_footer() -> str:
    return "</svg>"


def rounded_rect(
    x: float, y: float, w: float, h: float,
    rx: float = 12,
    fill: str | None = None,
    stroke: str | None = None,
    stroke_width: float = 1,
    opacity: float = 1,
    extra: str = "",
) -> str:
    """Render a rounded rectangle."""
    fill = fill or COLORS["card_bg"]
    stroke_attr = f' stroke="{stroke}" stroke-width="{stroke_width}"' if stroke else ""
    opacity_attr = f' opacity="{opacity}"' if opacity != 1 else ""
    return (
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" '
        f'rx="{rx}" fill="{fill}"{stroke_attr}{opacity_attr} {extra}/>'
    )


def text_element(
    x: float, y: float, content: str,
    size: float = 14,
    fill: str | None = None,
    anchor: str = "start",
    weight: str = "normal",
    extra: str = "",
) -> str:
    """Render a <text> element."""
    fill = fill or COLORS["text_light"]
    return (
        f'  <text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" font-weight="{weight}" {extra}>'
        f"{content}</text>"
    )


def circle(
    cx: float, cy: float, r: float,
    fill: str | None = None,
    stroke: str | None = None,
    stroke_width: float = 1,
    opacity: float = 1,
) -> str:
    fill = fill or COLORS["dusty_purple"]
    stroke_attr = f' stroke="{stroke}" stroke-width="{stroke_width}"' if stroke else ""
    opacity_attr = f' opacity="{opacity}"' if opacity != 1 else ""
    return f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{stroke_attr}{opacity_attr} />'
