"""
Custom SVG Certifications for GitHub Profile.
"""

from theme import COLORS, FONT_FAMILY, svg_header, svg_footer, rounded_rect, text_element

CARD_W = 800
CARD_H = 160

def generate_certs_svg(data: dict = None) -> str:
    extra_defs = f"""
    <linearGradient id="certGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{COLORS['white']}" />
      <stop offset="100%" stop-color="{COLORS['lavender']}" />
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.04" />
    </filter>
    """
    
    extra_style = """
    .cert-card { transition: transform 0.3s ease; }
    .cert-card:hover { transform: translateY(-3px); }
    """

    lines = [svg_header(CARD_W, CARD_H, extra_defs=extra_defs, extra_style=extra_style)]

    # Background (transparent)
    lines.append(rounded_rect(0, 0, CARD_W, CARD_H, rx=16, fill="none"))

    # Title
    lines.append(text_element(30, 30, "Certifications", size=18, fill=COLORS["deep_purple"], weight="800"))
    lines.append(f'<line x1="30" y1="42" x2="{CARD_W - 30}" y2="42" stroke="url(#purpleMintGradH)" stroke-width="1.5" stroke-opacity="0.4" stroke-linecap="round" />')

    # Draw 3 cards
    cert_w = 230
    cert_h = 80
    gap = 25
    start_x = 30
    start_y = 60

    certs = [
        {"title": "応用情報技術者", "sub": "Applied IT Engineer", "icon": "shield"},
        {"title": "データベーススペシャリスト", "sub": "Database Specialist", "icon": "db"},
        {"title": "統計検定2級", "sub": "Statistics Grade 2", "icon": "chart"}
    ]

    for i, cert in enumerate(certs):
        x = start_x + (cert_w + gap) * i
        y = start_y
        
        lines.append(f'<g class="cert-card" transform="translate({x}, {y})">')
        # Card Background
        lines.append(rounded_rect(0, 0, cert_w, cert_h, rx=12, fill="url(#certGrad)", stroke="url(#cardBorderGrad)", stroke_width=1.5, extra='filter="url(#shadow)"'))
        
        # Icon Background
        lines.append(rounded_rect(15, 20, 40, 40, rx=10, fill=COLORS["soft_mint"], opacity=0.7))
        
        # Draw elegant SVG icons
        icon_color = COLORS["deep_purple"]
        if cert["icon"] == "shield":
            path = f'<path d="M 35 28 L 45 28 L 45 42 Q 35 50 25 42 L 25 28 Z" fill="none" stroke="{icon_color}" stroke-width="2" stroke-linejoin="round" />'
            lines.append(path)
        elif cert["icon"] == "db":
            path1 = f'<ellipse cx="35" cy="30" rx="10" ry="4" fill="none" stroke="{icon_color}" stroke-width="2" />'
            path2 = f'<path d="M 25 30 L 25 46 A 10 4 0 0 0 45 46 L 45 30" fill="none" stroke="{icon_color}" stroke-width="2" />'
            path3 = f'<path d="M 25 38 A 10 4 0 0 0 45 38" fill="none" stroke="{icon_color}" stroke-width="2" />'
            lines.append(path1)
            lines.append(path2)
            lines.append(path3)
        elif cert["icon"] == "chart":
            path1 = f'<rect x="25" y="40" width="6" height="10" rx="1" fill="{COLORS["dusty_purple"]}" />'
            path2 = f'<rect x="33" y="32" width="6" height="18" rx="1" fill="{COLORS["mint_green"]}" />'
            path3 = f'<rect x="41" y="24" width="6" height="26" rx="1" fill="{icon_color}" />'
            lines.append(path1)
            lines.append(path2)
            lines.append(path3)
            
        # Text
        lines.append(text_element(70, 36, cert["title"], size=13, fill=COLORS["deep_purple"], weight="700"))
        lines.append(text_element(70, 54, cert["sub"], size=10, fill=COLORS["text_muted"], weight="500"))
        
        lines.append('</g>')

    lines.append(svg_footer())
    return "\n".join(lines)
