"""
About Me SVG Card generator.
Converts the Markdown bio into a beautiful dashboard card.
"""

from theme import COLORS, svg_header, svg_footer, draw_card, text_element, TEXT_BODY

CARD_W = 390
CARD_H = 260

def generate_about_svg(data: dict = None) -> str:
    lines = [svg_header(CARD_W, CARD_H)]
    
    # Draw standard card background & title
    lines.extend(draw_card(CARD_W, CARD_H, "About Me", "🧬"))
    
    # Content rows
    start_y = 86
    
    # 🎓 Master's student
    lines.append(text_element(30, start_y, "🎓", size=14))
    lines.append(text_element(55, start_y - 1, "Master's student", size=TEXT_BODY, fill=COLORS["text_light"], weight="700"))
    lines.append(text_element(55, start_y + 16, "at the Graduate School of Pharmaceutical", size=TEXT_BODY, fill=COLORS["text_muted"]))
    lines.append(text_element(55, start_y + 32, "Sciences, The University of Tokyo.", size=TEXT_BODY, fill=COLORS["text_muted"]))
    
    # 🔬 Member
    y2 = start_y + 60
    lines.append(text_element(30, y2, "🔬", size=14))
    lines.append(text_element(55, y2 - 1, "Member", size=TEXT_BODY, fill=COLORS["text_light"], weight="700"))
    lines.append(text_element(115, y2 - 1, "of the Mizuno Group.", size=TEXT_BODY, fill=COLORS["text_muted"]))
    
    # 📚 Research Interests
    y3 = y2 + 36
    lines.append(text_element(30, y3, "📚", size=14))
    lines.append(text_element(55, y3 - 1, "Research Interests:", size=TEXT_BODY, fill=COLORS["text_light"], weight="700"))
    lines.append(text_element(55, y3 + 16, "Biomedical NLP, Literature Mining,", size=TEXT_BODY, fill=COLORS["text_muted"]))
    lines.append(text_element(55, y3 + 32, "and Knowledge Discovery from", size=TEXT_BODY, fill=COLORS["text_muted"]))
    lines.append(text_element(55, y3 + 48, "Scientific Literature.", size=TEXT_BODY, fill=COLORS["text_muted"]))

    # Links
    y4 = CARD_H - 22
    lines.append(f'  <a href="https://devwithkaiju.github.io" target="_blank">')
    lines.append(text_element(CARD_W / 2 - 10, y4, "🌐 Personal HP", size=12, fill=COLORS["mint_green"], anchor="end", weight="600"))
    lines.append(f'  </a>')
    
    lines.append(text_element(CARD_W / 2, y4, "|", size=12, fill=COLORS["text_muted"], anchor="middle"))
    
    lines.append(f'  <a href="https://www.mizuno-group.com" target="_blank">')
    lines.append(text_element(CARD_W / 2 + 10, y4, "🏢 Mizuno Group HP", size=12, fill=COLORS["mint_green"], anchor="start", weight="600"))
    lines.append(f'  </a>')

    lines.append(svg_footer())
    return "\n".join(lines)
