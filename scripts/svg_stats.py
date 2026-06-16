"""
Stats card SVG generator.
Replaces github-readme-stats with a custom card in the cute theme.
"""

from theme import COLORS, FONT_FAMILY, svg_header, svg_footer, rounded_rect, text_element


# ─── Stat row definitions ───────────────────────────────────

STAT_ROWS = [
    ("⭐", "Total Stars", "total_stars"),
    ("🔥", "Total Commits", "total_commits"),
    ("🔀", "Total PRs", "total_prs"),
    ("📝", "Total Issues", "total_issues"),
    ("📦", "Total Repos", "total_repos"),
    ("👥", "Followers", "followers"),
]

CARD_W = 420
CARD_H = 260
ROW_H = 30
PADDING = 24


def generate_stats_svg(data: dict) -> str:
    """Generate the GitHub stats card SVG."""

    extra_style = """
    @keyframes countUp {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    """

    lines = [svg_header(CARD_W, CARD_H, extra_style=extra_style)]

    # Card background
    lines.append(rounded_rect(0, 0, CARD_W, CARD_H, rx=16, fill=COLORS["dark_bg"]))
    lines.append(rounded_rect(0, 0, CARD_W, CARD_H, rx=16, fill="none", stroke="url(#cardBorderGrad)", stroke_width=1.5))

    # Title bar
    lines.append(text_element(CARD_W / 2, 36, f"📊  {data['username']}'s GitHub Stats", size=15, anchor="middle", fill=COLORS["lavender"], weight="600"))

    # Divider line
    lines.append(f'  <line x1="{PADDING}" y1="50" x2="{CARD_W - PADDING}" y2="50" stroke="url(#purpleMintGradH)" stroke-width="1" stroke-opacity="0.3" />')

    # Stats rows
    start_y = 72
    for i, (icon, label, key) in enumerate(STAT_ROWS):
        y = start_y + i * ROW_H
        value = data.get(key, 0)

        # Icon
        lines.append(text_element(PADDING + 6, y + 4, icon, size=15, anchor="start"))

        # Label
        lines.append(text_element(PADDING + 34, y + 3, label, size=13, fill=COLORS["text_muted"]))

        # Value
        lines.append(text_element(CARD_W - PADDING - 10, y + 3, str(value), size=14, fill=COLORS["mint_green"], anchor="end", weight="700"))

        # Subtle row separator (except last)
        if i < len(STAT_ROWS) - 1:
            sep_y = y + 16
            lines.append(f'  <line x1="{PADDING + 30}" y1="{sep_y}" x2="{CARD_W - PADDING}" y2="{sep_y}" stroke="{COLORS["locked_border"]}" stroke-width="0.5" />')

    # Bottom accent bar
    bar_y = CARD_H - 28
    lines.append(f'  <line x1="{PADDING}" y1="{bar_y}" x2="{CARD_W - PADDING}" y2="{bar_y}" stroke="url(#purpleMintGradH)" stroke-width="1" stroke-opacity="0.3" />')

    # Year contributions
    lines.append(text_element(CARD_W / 2, CARD_H - 10, f"🌸 {data.get('contributions_this_year', 0)} contributions this year", size=11, anchor="middle", fill=COLORS["text_muted"]))

    lines.append(svg_footer())
    return "\n".join(lines)
