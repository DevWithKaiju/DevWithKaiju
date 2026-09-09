"""
Field Data card - a compact specimen-log data sheet of GitHub activity.
"""

from theme_field_notes import COLORS, FONT_MONO, svg_header, svg_footer, card_shell, text_element, kicker

CARD_W = 800
CARD_H = 236

# (label, data key) - laid out as a 3-column x 2-row grid, in this order.
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
    lines.append(card_shell(CARD_W, CARD_H))

    lines.append(kicker(30, 38, "Field Data"))
    lines.append(text_element(770, 38, "Updated daily · 09:00 JST", size=10, fill=COLORS["text_faint"],
                               anchor="end", family=FONT_MONO))

    col_w = (CARD_W - 2 * 30) / 3
    for i, (label, key) in enumerate(STAT_CELLS):
        col, row = i % 3, i // 3
        cx = 30 + col_w * col + col_w / 2
        num_y = 100 + row * 62
        label_y = num_y + 20
        value = data.get(key, 0)
        lines.append(text_element(cx, num_y, str(value), size=28, fill=COLORS["ink"],
                                   anchor="middle", weight="700"))
        lines.append(text_element(cx, label_y, label.upper(), size=10, fill=COLORS["text"],
                                   anchor="middle", family=FONT_MONO, letter_spacing=1.0))

    divider_y = CARD_H - 38
    lines.append(f'  <line x1="30" y1="{divider_y}" x2="770" y2="{divider_y}" '
                  f'stroke="{COLORS["border"]}" stroke-width="1" stroke-dasharray="3,3" />')
    contrib_y = CARD_H - 16
    lines.append(text_element(CARD_W / 2, contrib_y,
                               f"{data.get('contributions_this_year', 0)} contributions logged this year",
                               size=14, fill=COLORS["deep_purple"], anchor="middle", style="italic"))

    lines.append(svg_footer())
    return "\n".join(lines)
