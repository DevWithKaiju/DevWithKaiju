"""
Theme: Dusty Purple × Mint Green (Light / Cute Theme)
"""

COLORS = {
    "dusty_purple": "#9B8EC4",     # Main accent
    "deep_purple": "#5A5070",      # Dark text / strokes
    "mint_green": "#A8D8C8",       # Secondary accent
    "soft_mint": "#E2F4EE",        # Very light mint for highlights
    "lavender": "#F4F1FA",         # Very light purple for inner backgrounds
    "card_bg": "#FFFFFF",          # Card background (White)
    "dark_bg": "#FAFAFC",          # Base background (Off-white)
    "text_light": "#4A4359",       # Main text (Dark purple-gray)
    "text_muted": "#8A80A0",       # Muted text
    "locked_bg": "#F5F5F5",        # Locked badge background
    "locked_border": "#E0E0E0",    # Locked badge border
    "locked_text": "#B0B0B0",      # Locked text
    "gold": "#F2C94C",
    "soft_pink": "#FFD6E5",
    "white": "#FFFFFF",
}

FONT_FAMILY = "'Segoe UI', 'Helvetica Neue', Ubuntu, sans-serif"


def svg_header(width: int, height: int, extra_defs: str = "", extra_style: str = "") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 {width} {height}">
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
      <stop offset="0%" stop-color="{COLORS['dusty_purple']}" stop-opacity="0.6" />
      <stop offset="100%" stop-color="{COLORS['mint_green']}" stop-opacity="0.6" />
    </linearGradient>
    {extra_defs}
  </defs>
  <style>
    text {{ font-family: {FONT_FAMILY}; }}
    {extra_style}
  </style>'''

def svg_footer() -> str:
    return "</svg>"

def rounded_rect(x: float, y: float, w: float, h: float, rx: float = 16, fill: str | None = None, stroke: str | None = None, stroke_width: float = 1, opacity: float = 1, extra: str = "") -> str:
    fill = fill or COLORS["card_bg"]
    stroke_attr = f' stroke="{stroke}" stroke-width="{stroke_width}"' if stroke else ""
    opacity_attr = f' opacity="{opacity}"' if opacity != 1 else ""
    return f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{stroke_attr}{opacity_attr} {extra}/>'

def text_element(x: float, y: float, content: str, size: float = 14, fill: str | None = None, anchor: str = "start", weight: str = "normal", extra: str = "") -> str:
    fill = fill or COLORS["text_light"]
    return f'  <text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {extra}>{content}</text>'
