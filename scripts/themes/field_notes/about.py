"""
About card ("Field Notes" theme) - researcher bio, as plain readable prose
rather than icon-per-line rows.

Note: the actual "Personal site" / "Mizuno Group" links live as plain Markdown
links in README.md, not inside this SVG - an <a> inside an SVG referenced via
<img> never becomes clickable in a rendered GitHub README.
"""

from themes.field_notes.theme import COLORS, svg_header, svg_footer, card_shell, text_element, kicker

CARD_W = 800
CARD_H = 180

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

    lines.append(svg_footer())
    return "\n".join(lines)
