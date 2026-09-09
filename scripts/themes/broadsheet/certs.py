"""
Credentials block ("Broadsheet" theme) - bordered stamp boxes in a row.
"""

from themes.broadsheet.theme import COLORS, FONT_DISPLAY, FONT_MONO, svg_header, svg_footer, text_element, kicker

CARD_W = 800
CARD_H = 164
PADDING = 30

CERTS = [
    {"title": "応用情報技術者", "sub": "Applied IT Engineer"},
    {"title": "データベーススペシャリスト", "sub": "Database Specialist"},
    {"title": "統計検定2級", "sub": "Statistics Grade 2"},
]


def generate_certs_svg(data: dict | None = None) -> str:
    lines = [svg_header(CARD_W, CARD_H)]
    lines.append(kicker(PADDING, 30, "Credentials"))

    # Box height matches one row of the Field Data stat grid, so the two
    # sections keep the same visual rhythm stacked back to back.
    col_w = (CARD_W - 2 * PADDING) / len(CERTS)
    box_y, box_h = 44, 96
    for i, cert in enumerate(CERTS):
        x = PADDING + col_w * i
        w = col_w - (10 if i < len(CERTS) - 1 else 0)
        lines.append(f'  <rect x="{x}" y="{box_y}" width="{w}" height="{box_h}" fill="none" '
                      f'stroke="{COLORS["ink"]}" stroke-width="1.5" />')
        lines.append(text_element(x + 16, box_y + 44, cert["title"], size=14, fill=COLORS["ink"],
                                   weight="700", family=FONT_DISPLAY))
        lines.append(text_element(x + 16, box_y + 66, cert["sub"].upper(), size=9.5, fill=COLORS["muted"],
                                   family=FONT_MONO, letter_spacing=0.6))

    lines.append(svg_footer())
    return "\n".join(lines)
