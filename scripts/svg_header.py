"""
Custom SVG Header for GitHub Profile.
"""

from theme import COLORS, FONT_FAMILY, svg_header, svg_footer, rounded_rect, text_element

CARD_W = 800
CARD_H = 120

def generate_header_svg(data: dict = None) -> str:
    extra_defs = f"""
    <filter id="blur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="15" />
    </filter>
    <clipPath id="headerClip">
      <rect x="0" y="0" width="{CARD_W}" height="{CARD_H}" rx="16" />
    </clipPath>
    """
    
    extra_style = """
    @keyframes float1 {
      0% { transform: translateY(0px) scale(1); }
      50% { transform: translateY(-10px) scale(1.05); }
      100% { transform: translateY(0px) scale(1); }
    }
    @keyframes float2 {
      0% { transform: translate(0px, 0px) scale(1); }
      50% { transform: translate(15px, 5px) scale(0.95); }
      100% { transform: translate(0px, 0px) scale(1); }
    }
    .blob1 { animation: float1 6s ease-in-out infinite; }
    .blob2 { animation: float2 8s ease-in-out infinite; }
    .star { animation: float1 4s ease-in-out infinite; }
    """

    lines = [svg_header(CARD_W, CARD_H, extra_defs=extra_defs, extra_style=extra_style)]

    # Background
    lines.append(f'<g clip-path="url(#headerClip)">')
    lines.append(rounded_rect(0, 0, CARD_W, CARD_H, rx=0, fill=COLORS["lavender"]))
    
    # Soft blobs
    lines.append(f'<circle class="blob1" cx="100" cy="20" r="60" fill="{COLORS["soft_pink"]}" opacity="0.6" filter="url(#blur)" />')
    lines.append(f'<circle class="blob2" cx="700" cy="100" r="80" fill="{COLORS["mint_green"]}" opacity="0.5" filter="url(#blur)" />')
    lines.append(f'<circle class="blob1" cx="400" cy="-30" r="90" fill="{COLORS["dusty_purple"]}" opacity="0.4" filter="url(#blur)" />')

    # Decorational SVG paths (Sparkles / Stars) - Kawaii elements
    star_path = "M0,-8 L1.5,-2.5 L8,0 L1.5,2.5 L0,8 L-1.5,2.5 L-8,0 L-1.5,-2.5 Z"
    
    lines.append(f'<g class="star" transform="translate(60, 40)"><path d="{star_path}" fill="{COLORS["deep_purple"]}" opacity="0.4"/></g>')
    lines.append(f'<g class="star" transform="translate(100, 90) scale(0.6)"><path d="{star_path}" fill="{COLORS["deep_purple"]}" opacity="0.5"/></g>')
    lines.append(f'<g class="star" transform="translate(740, 50)"><path d="{star_path}" fill="{COLORS["deep_purple"]}" opacity="0.3"/></g>')
    lines.append(f'<g class="star" transform="translate(700, 30) scale(0.7)"><path d="{star_path}" fill="{COLORS["deep_purple"]}" opacity="0.4"/></g>')

    # Main text
    lines.append(text_element(CARD_W / 2, CARD_H / 2 + 8, "Bridging Pharmaceutical Sciences &amp; NLP", size=24, fill=COLORS["deep_purple"], anchor="middle", weight="800"))

    # Sub text / decorative line
    lines.append(f'<line x1="{CARD_W/2 - 80}" y1="{CARD_H - 30}" x2="{CARD_W/2 + 80}" y2="{CARD_H - 30}" stroke="{COLORS["dusty_purple"]}" stroke-width="2" stroke-opacity="0.6" stroke-linecap="round" />')
    lines.append(text_element(CARD_W / 2, CARD_H - 12, "Graduate School of Pharmaceutical Sciences", size=12, fill=COLORS["text_light"], anchor="middle", weight="600"))

    lines.append('</g>')
    
    # Border
    lines.append(rounded_rect(0, 0, CARD_W, CARD_H, rx=16, fill="none", stroke="url(#cardBorderGrad)", stroke_width=2))

    lines.append(svg_footer())
    return "\n".join(lines)
