"""
Credentials card - certifications as a row of stamp-sealed entries.
"""

from theme import COLORS, FONT_MONO, svg_header, svg_footer, card_shell, text_element, kicker

CARD_W = 800
CARD_H = 130
PADDING = 30

CERTS = [
    {"title": "応用情報技術者", "sub": "Applied IT Engineer"},
    {"title": "データベーススペシャリスト", "sub": "Database Specialist"},
    {"title": "統計検定2級", "sub": "Statistics Grade 2"},
]


def _seal_icon(x: float, y: float) -> str:
    color = COLORS["deep_purple"]
    return (f'  <g transform="translate({x}, {y})">'
            f'<circle cx="15" cy="12" r="8" fill="none" stroke="{color}" stroke-width="1.6"/>'
            f'<path d="M11 18.5 L9 27 L15 24 L21 27 L19 18.5" fill="none" stroke="{color}" '
            f'stroke-width="1.6" stroke-linejoin="round"/>'
            f'</g>')


def generate_certs_svg(data: dict | None = None) -> str:
    lines = [svg_header(CARD_W, CARD_H)]
    lines.append(card_shell(CARD_W, CARD_H))
    lines.append(kicker(PADDING, 38, "Credentials"))

    col_w = (CARD_W - 2 * PADDING) / len(CERTS)
    icon_y = 54
    for i, cert in enumerate(CERTS):
        col_x = PADDING + col_w * i
        lines.append(_seal_icon(col_x, icon_y))
        text_x = col_x + 42
        lines.append(text_element(text_x, icon_y + 14, cert["title"], size=12.5,
                                   fill=COLORS["ink"], weight="700"))
        lines.append(text_element(text_x, icon_y + 32, cert["sub"], size=10,
                                   fill=COLORS["text_faint"], family=FONT_MONO))

    lines.append(svg_footer())
    return "\n".join(lines)
