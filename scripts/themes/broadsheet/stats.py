"""
Field Data block ("Broadsheet" theme) - a newspaper-style stat grid:
uniform big numbers over a soft hairline rule, instead of a card.
"""

from themes.broadsheet.theme import COLORS, FONT_DISPLAY, FONT_MONO, svg_header, svg_footer, text_element, kicker, hairline

CARD_W = 800
CARD_H = 290
PADDING = 30

STAT_CELLS = [
    ("Commits", "total_commits"),
    ("Pull Requests", "total_prs"),
    ("Repositories", "total_repos"),
    ("Issues", "total_issues"),
    ("Stars", "total_stars"),
    ("Followers", "followers"),
]


def generate_stats_svg(data: dict) -> str:
    lines = [svg_header(CARD_W, CARD_H)]
    lines.append(kicker(PADDING, 30, "Field Data"))
    lines.append(text_element(770, 30, "Updated daily · 09:00 JST", size=10, fill=COLORS["muted"],
                               anchor="end", family=FONT_MONO))

    col_w = (CARD_W - 2 * PADDING) / 3
    for i, (label, key) in enumerate(STAT_CELLS):
        col, row = i % 3, i // 3
        x = PADDING + col_w * col
        rule_y = 64 + row * 96
        num_y = rule_y + 56
        label_y = num_y + 18
        value = data.get(key, 0)
        lines.append(hairline(x, rule_y, x + col_w - 20))
        lines.append(text_element(x, num_y, str(value), size=40, fill=COLORS["ink"], weight="800", family=FONT_DISPLAY))
        lines.append(text_element(x, label_y, label.upper(), size=10, fill=COLORS["muted"],
                                   family=FONT_MONO, letter_spacing=1.2))

    lines.append(text_element(CARD_W / 2, CARD_H - 16,
                               f"{data.get('contributions_this_year', 0)} contributions logged this year",
                               size=12.5, fill=COLORS["teal"], anchor="middle", family=FONT_MONO))

    lines.append(svg_footer())
    return "\n".join(lines)
