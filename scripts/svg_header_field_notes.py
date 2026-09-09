"""
Masthead card - the top of the profile "field log".
"""

from theme_field_notes import COLORS, FONT_MONO, svg_header, svg_footer, card_shell, text_element, kicker

CARD_W = 800
CARD_H = 128

HEADLINE = "Bridging Pharmaceutical Sciences &amp; NLP"
SUBTITLE = "Master&#8217;s Student, Graduate School of Pharmaceutical Sciences &#8212; The University of Tokyo"


def generate_header_svg(data: dict | None = None) -> str:
    username = (data or {}).get("username", "DevWithKaiju")

    lines = [svg_header(CARD_W, CARD_H)]
    lines.append(card_shell(CARD_W, CARD_H))

    lines.append(kicker(30, 38, "Github Field Log"))
    lines.append(text_element(770, 38, f"@{username}", size=11, fill=COLORS["text_faint"],
                               anchor="end", family=FONT_MONO))

    lines.append(text_element(30, 74, HEADLINE, size=25, fill=COLORS["ink"], weight="700"))
    lines.append(text_element(30, 98, SUBTITLE, size=13.5, fill=COLORS["text"], style="italic"))

    lines.append(svg_footer())
    return "\n".join(lines)
