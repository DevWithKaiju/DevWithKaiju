"""
About block ("Broadsheet" theme) - a pull-quote headline over the bio.

The "Personal Site" / "Mizuno Group" chips are a separate pair of small
images (links.py in this package) wrapped in real <a> tags in README.md -
not drawn inside this SVG. An <a> inside an SVG loaded via <img> is never
actually clickable on GitHub, but an <img> wrapped in a real Markdown/HTML
<a> works fine, so the chips live as their own tiny clickable images instead.
"""

from themes.broadsheet.theme import COLORS, FONT_DISPLAY, FONT_BODY, svg_header, svg_footer, text_element, kicker

CARD_W = 800
CARD_H = 246

PULL_QUOTE = ["Teaching machines", "to read the literature."]

BIO_LINES = [
    "I&#8217;m a master&#8217;s student at the Graduate School of Pharmaceutical Sciences,",
    "The University of Tokyo, and a member of the Mizuno Group. My research sits",
    "at the intersection of biomedical NLP, literature mining, and knowledge",
    "discovery &#8212; so researchers don&#8217;t have to read all of it themselves.",
]


def generate_about_svg(data: dict | None = None) -> str:
    lines = [svg_header(CARD_W, CARD_H)]
    lines.append(kicker(30, 30, "About"))

    lines.append(text_element(30, 72, PULL_QUOTE[0], size=30, fill=COLORS["ink"], weight="800", family=FONT_DISPLAY))
    lines.append(text_element(30, 104, PULL_QUOTE[1], size=30, fill=COLORS["ink"], weight="800", family=FONT_DISPLAY))

    line_y = 140
    for line in BIO_LINES:
        lines.append(text_element(30, line_y, line, size=15, fill=COLORS["ink"], family=FONT_BODY))
        line_y += 24

    lines.append(svg_footer())
    return "\n".join(lines)
