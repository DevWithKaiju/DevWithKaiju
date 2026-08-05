"""
Custom SVG Header for GitHub Profile.
"""

from theme import COLORS, FONT_FAMILY, svg_header, svg_footer, rounded_rect, text_element

CARD_W = 800
CARD_H = 120

def generate_header_svg(data: dict = None) -> str:
    extra_defs = f"""
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{COLORS['lavender']}" />
      <stop offset="100%" stop-color="{COLORS['soft_mint']}" />
    </linearGradient>
    """
    
    extra_style = """
    @keyframes float1 {
      0% { transform: translateY(0px) rotate(0deg); }
      50% { transform: translateY(-5px) rotate(5deg); }
      100% { transform: translateY(0px) rotate(0deg); }
    }
    @keyframes float2 {
      0% { transform: translateY(0px) rotate(0deg); }
      50% { transform: translateY(5px) rotate(-5deg); }
      100% { transform: translateY(0px) rotate(0deg); }
    }
    .star1 { animation: float1 4s ease-in-out infinite; }
    .star2 { animation: float2 5s ease-in-out infinite; }
    """

    lines = [svg_header(CARD_W, CARD_H, extra_defs=extra_defs, extra_style=extra_style)]

    # Background
    lines.append(rounded_rect(0, 0, CARD_W, CARD_H, rx=16, fill="url(#headerGrad)"))
    lines.append(rounded_rect(0, 0, CARD_W, CARD_H, rx=16, fill="none", stroke="url(#cardBorderGrad)", stroke_width=2))

    # Decorational SVG paths (Sparkles / Stars)
    star_path = "M0,-10 L2,-3 L10,0 L2,3 L0,10 L-2,3 L-10,0 L-2,-3 Z"
    
    # Left decorations
    lines.append(f'<g class="star1" transform="translate(60, 40)"><path d="{star_path}" fill="{COLORS["mint_green"]}" opacity="0.6"/></g>')
    lines.append(f'<g class="star2" transform="translate(40, 80)"><circle cx="0" cy="0" r="4" fill="{COLORS["dusty_purple"]}" opacity="0.4"/></g>')
    lines.append(f'<g class="star1" transform="translate(100, 90) scale(0.6)"><path d="{star_path}" fill="{COLORS["soft_pink"]}" opacity="0.8"/></g>')

    # Right decorations
    lines.append(f'<g class="star2" transform="translate({CARD_W - 60}, 50)"><path d="{star_path}" fill="{COLORS["dusty_purple"]}" opacity="0.5"/></g>')
    lines.append(f'<g class="star1" transform="translate({CARD_W - 40}, 90)"><circle cx="0" cy="0" r="3" fill="{COLORS["mint_green"]}" opacity="0.5"/></g>')
    lines.append(f'<g class="star2" transform="translate({CARD_W - 100}, 30) scale(0.7)"><path d="{star_path}" fill="{COLORS["soft_pink"]}" opacity="0.7"/></g>')

    # Main text
    lines.append(text_element(CARD_W / 2, CARD_H / 2 + 8, "Bridging Pharmaceutical Sciences & NLP", size=24, fill=COLORS["deep_purple"], anchor="middle", weight="800"))

    # Sub text / decorative line
    lines.append(f'<line x1="{CARD_W/2 - 100}" y1="{CARD_H - 30}" x2="{CARD_W/2 + 100}" y2="{CARD_H - 30}" stroke="{COLORS["dusty_purple"]}" stroke-width="2" stroke-opacity="0.4" stroke-linecap="round" />')
    lines.append(text_element(CARD_W / 2, CARD_H - 12, "Graduate School of Pharmaceutical Sciences", size=12, fill=COLORS["text_muted"], anchor="middle", weight="600"))

    lines.append(svg_footer())
    return "\n".join(lines)
