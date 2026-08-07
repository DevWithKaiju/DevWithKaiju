"""
Custom SVG Certifications for GitHub Profile.
"""

from theme import COLORS, FONT_FAMILY, svg_header, svg_footer, draw_card, rounded_rect, text_element

CARD_W = 390
CARD_H = 240

def generate_certs_svg(data: dict = None) -> str:
    extra_defs = f"""
    <linearGradient id="certGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{COLORS['white']}" />
      <stop offset="100%" stop-color="{COLORS['lavender']}" />
    </linearGradient>
    """
    
    extra_style = """
    .cert-card { transition: transform 0.3s ease; }
    .cert-card:hover { transform: translateX(3px); }
    """

    lines = [svg_header(CARD_W, CARD_H, extra_defs=extra_defs, extra_style=extra_style)]

    # Draw standard card background & title
    lines.extend(draw_card(CARD_W, CARD_H, "Certifications", "📜"))

    # Vertical list of cards
    cert_w = CARD_W - 60
    cert_h = 44
    gap = 12
    start_x = 30
    start_y = 66

    certs = [
        {"title": "応用情報技術者", "sub": "Applied IT Engineer", "icon": "shield"},
        {"title": "データベーススペシャリスト", "sub": "Database Specialist", "icon": "db"},
        {"title": "統計検定2級", "sub": "Statistics Grade 2", "icon": "chart"}
    ]

    for i, cert in enumerate(certs):
        y = start_y + (cert_h + gap) * i
        
        lines.append(f'<g class="cert-card" transform="translate({start_x}, {y})">')
        
        # Icon Background
        lines.append(rounded_rect(0, 0, 44, 44, rx=10, fill=COLORS["soft_mint"], opacity=0.7))
        
        # Draw elegant SVG icons
        icon_color = COLORS["deep_purple"]
        if cert["icon"] == "shield":
            path = f'<path d="M 12 10 L 32 10 L 32 24 Q 22 36 12 24 Z" fill="none" stroke="{icon_color}" stroke-width="2" stroke-linejoin="round" />'
            lines.append(path)
        elif cert["icon"] == "db":
            path1 = f'<ellipse cx="22" cy="14" rx="10" ry="4" fill="none" stroke="{icon_color}" stroke-width="2" />'
            path2 = f'<path d="M 12 14 L 12 30 A 10 4 0 0 0 32 30 L 32 14" fill="none" stroke="{icon_color}" stroke-width="2" />'
            path3 = f'<path d="M 12 22 A 10 4 0 0 0 32 22" fill="none" stroke="{icon_color}" stroke-width="2" />'
            lines.append(path1)
            lines.append(path2)
            lines.append(path3)
        elif cert["icon"] == "chart":
            path1 = f'<rect x="12" y="24" width="6" height="10" rx="1" fill="{COLORS["dusty_purple"]}" />'
            path2 = f'<rect x="20" y="16" width="6" height="18" rx="1" fill="{COLORS["mint_green"]}" />'
            path3 = f'<rect x="28" y="8" width="6" height="26" rx="1" fill="{icon_color}" />'
            lines.append(path1)
            lines.append(path2)
            lines.append(path3)
            
        # Text
        lines.append(text_element(56, 18, cert["title"], size=13, fill=COLORS["deep_purple"], weight="700"))
        lines.append(text_element(56, 34, cert["sub"], size=11, fill=COLORS["text_muted"], weight="500"))
        
        lines.append('</g>')

    lines.append(svg_footer())
    return "\n".join(lines)
