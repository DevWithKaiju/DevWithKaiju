"""
Hero header ("Broadsheet" theme) - a bold two-line poster headline.
"""

from themes.broadsheet.theme import COLORS, FONT_DISPLAY, FONT_MONO, svg_header, svg_footer, text_element, kicker

CARD_W = 800
CARD_H = 172

HEADLINE_LINE_1 = "Bridging Pharma"
HEADLINE_LINE_2 = "Science &amp; NLP."
SUBTITLE = "Master&#8217;s Student, Graduate School of Pharmaceutical Sciences &#8212; The University of Tokyo"


def generate_header_svg(data: dict | None = None) -> str:
    username = (data or {}).get("username", "DevWithKaiju")

    lines = [svg_header(CARD_W, CARD_H)]
    lines.append(kicker(30, 30, f"@{username} · Github Profile"))

    lines.append(text_element(30, 76, HEADLINE_LINE_1, size=46, fill=COLORS["ink"],
                               weight="900", family=FONT_DISPLAY, letter_spacing=-0.3))
    lines.append(text_element(30, 120, HEADLINE_LINE_2, size=46, fill=COLORS["ink"],
                               weight="900", family=FONT_DISPLAY, letter_spacing=-0.3))

    lines.append(text_element(30, 144, SUBTITLE, size=13.5, fill=COLORS["muted"], family="'Segoe UI', Arial, sans-serif"))
    lines.append(f'  <rect x="30" y="156" width="64" height="3" fill="{COLORS["ink"]}" />')

    lines.append(svg_footer())
    return "\n".join(lines)
