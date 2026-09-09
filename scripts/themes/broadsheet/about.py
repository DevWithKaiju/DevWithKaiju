"""
About block ("Broadsheet" theme) - a pull-quote headline over the bio.

Note: the "Personal site" / "Mizuno Group" chips below are visual only. An <a>
inside an SVG referenced via <img> never becomes clickable in a rendered
GitHub README, so the actual clickable links live as plain Markdown links in
README.md, placed right under this image.
"""

from themes.broadsheet.theme import COLORS, FONT_DISPLAY, FONT_BODY, FONT_MONO, svg_header, svg_footer, text_element, kicker

CARD_W = 800
CARD_H = 286

PULL_QUOTE = ["Teaching machines", "to read the literature."]

BIO_LINES = [
    "I&#8217;m a master&#8217;s student at the Graduate School of Pharmaceutical Sciences,",
    "The University of Tokyo, and a member of the Mizuno Group. My research sits",
    "at the intersection of biomedical NLP, literature mining, and knowledge",
    "discovery &#8212; so researchers don&#8217;t have to read all of it themselves.",
]

LINKS = ["Personal Site ↗", "Mizuno Group ↗"]


def generate_about_svg(data: dict | None = None) -> str:
    lines = [svg_header(CARD_W, CARD_H)]
    lines.append(kicker(30, 30, "About"))

    lines.append(text_element(30, 72, PULL_QUOTE[0], size=30, fill=COLORS["ink"], weight="800", family=FONT_DISPLAY))
    lines.append(text_element(30, 104, PULL_QUOTE[1], size=30, fill=COLORS["ink"], weight="800", family=FONT_DISPLAY))

    line_y = 140
    for line in BIO_LINES:
        lines.append(text_element(30, line_y, line, size=15, fill=COLORS["ink"], family=FONT_BODY))
        line_y += 24

    chip_y, chip_h = 228, 34
    chip_x = 30
    for label in LINKS:
        chip_w = len(label) * 7.2 + 32
        lines.append(f'  <rect x="{chip_x}" y="{chip_y}" width="{chip_w}" height="{chip_h}" fill="none" '
                      f'stroke="{COLORS["ink"]}" stroke-width="1.5" />')
        lines.append(text_element(chip_x + chip_w / 2, chip_y + chip_h / 2 + 4, label.upper(), size=11,
                                   fill=COLORS["ink"], anchor="middle", weight="600",
                                   family=FONT_MONO, letter_spacing=0.6))
        chip_x += chip_w + 14

    lines.append(svg_footer())
    return "\n".join(lines)
