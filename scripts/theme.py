"""
Theme: Dusty Purple × Mint Green (Light / Cute Theme)
"""

COLORS = {
    "dusty_purple": "#b39cd0",     # Main accent (Primary)
    "deep_purple": "#8870a4",      # Dark text / strokes (Primary Dark)
    "mint_green": "#2dd4bf",       # Secondary accent (Accent)
    "soft_mint": "#e6f8f5",        # Very light mint for highlights
    "lavender": "#f5f0f9",         # Very light purple for inner backgrounds (Primary Light)
    "card_bg": "#FFFFFF",          # Card background (White)
    "dark_bg": "#FAFAFC",          # Base background (Off-white)
    "text_light": "#475569",       # Main text (Dark purple-gray)
    "text_muted": "#94a3b8",       # Muted text
    "locked_bg": "#f1f5f9",        # Locked badge background
    "locked_border": "#e2e8f0",    # Locked badge border
    "locked_text": "#94a3b8",      # Locked text
    "gold": "#F2C94C",
    "soft_pink": "#FFD6E5",
    "white": "#FFFFFF",
}

FONT_FAMILY = '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"'

# Typographic scales
TEXT_H1 = 20
TEXT_H2 = 16
TEXT_BODY = 13
TEXT_SMALL = 11

def svg_header(width: int, height: int, extra_defs: str = "", extra_style: str = "") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="purpleMintGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{COLORS['dusty_purple']}" />
      <stop offset="100%" stop-color="{COLORS['deep_purple']}" />
    </linearGradient>
    <linearGradient id="purpleMintGradH" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{COLORS['dusty_purple']}" stop-opacity="0.5" />
      <stop offset="100%" stop-color="{COLORS['deep_purple']}" stop-opacity="0.5" />
    </linearGradient>
    <linearGradient id="cardBorderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{COLORS['dusty_purple']}" stop-opacity="0.4" />
      <stop offset="100%" stop-color="{COLORS['deep_purple']}" stop-opacity="0.2" />
    </linearGradient>
    <filter id="cardShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#5A5070" flood-opacity="0.08"/>
    </filter>
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

def text_element(x: float, y: float, content: str, size: float = TEXT_BODY, fill: str | None = None, anchor: str = "start", weight: str = "normal", extra: str = "") -> str:
    fill = fill or COLORS["text_light"]
    return f'  <text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {extra}>{content}</text>'

def draw_card(width: float, height: float, title: str, icon: str = "") -> list[str]:
    """Draws a standard beautifully styled card background with a title and divider line."""
    lines = []
    # Base Card
    lines.append(rounded_rect(0, 0, width, height, rx=16, fill=COLORS["dark_bg"], extra='filter="url(#cardShadow)"'))
    lines.append(rounded_rect(0, 0, width, height, rx=16, fill="none", stroke="url(#cardBorderGrad)", stroke_width=1.5))
    
    # Title Section
    title_y = 36
    title_text = f"{icon}  {title}" if icon else title
    lines.append(text_element(width / 2, title_y, title_text, size=TEXT_H2, fill=COLORS["deep_purple"], anchor="middle", weight="700"))
    
    # Divider
    lines.append(f'  <line x1="30" y1="52" x2="{width - 30}" y2="52" stroke="url(#purpleMintGradH)" stroke-width="1.5" stroke-opacity="0.4" stroke-dasharray="4,4" />')
    
    return lines
