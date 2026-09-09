"""
About card - researcher bio, as plain readable prose rather than icon-per-line rows.
"""

from theme import COLORS, FONT_MONO, svg_header, svg_footer, card_shell, text_element, kicker

CARD_W = 800
CARD_H = 208

BIO_LINES = [
    "I&#8217;m a master&#8217;s student at the Graduate School of Pharmaceutical Sciences,",
    "The University of Tokyo, and a member of the Mizuno Group. My research sits",
    "at the intersection of biomedical NLP, literature mining, and knowledge",
    "discovery &#8212; teaching machines to read the scientific literature so",
    "researchers don&#8217;t have to read all of it themselves.",
]


def generate_about_svg(data: dict | None = None) -> str:
    lines = [svg_header(CARD_W, CARD_H)]
    lines.append(card_shell(CARD_W, CARD_H))

    lines.append(kicker(30, 38, "About"))

    line_y = 66
    for line in BIO_LINES:
        lines.append(text_element(30, line_y, line, size=14.5, fill=COLORS["ink"]))
        line_y += 22

    link_y = CARD_H - 26
    lines.append(f'  <a href="https://devwithkaiju.github.io" target="_blank">')
    lines.append(text_element(30, link_y, "Personal site &#8599;", size=12.5, fill=COLORS["deep_purple"],
                               weight="600", family=FONT_MONO))
    lines.append(f'  </a>')

    lines.append(f'  <a href="https://www.mizuno-group.com" target="_blank">')
    lines.append(text_element(160, link_y, "Mizuno Group &#8599;", size=12.5, fill=COLORS["deep_purple"],
                               weight="600", family=FONT_MONO))
    lines.append(f'  </a>')

    lines.append(svg_footer())
    return "\n".join(lines)
