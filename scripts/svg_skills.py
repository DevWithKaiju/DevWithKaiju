"""
Skills / language badge SVG generator.
Creates pill-shaped badges showing top languages from GitHub repos.
"""

from theme import COLORS, FONT_FAMILY, svg_header, svg_footer, rounded_rect, text_element


BADGE_H = 28
BADGE_RX = 14
BADGE_GAP_X = 10
BADGE_GAP_Y = 10
PADDING = 20
MAX_WIDTH = 800


def generate_skills_svg(data: dict) -> str:
    """Generate skills/language badges SVG."""

    languages = data.get("languages", [])
    if not languages:
        languages = [{"name": "No data", "color": "#666", "percentage": 0}]

    # ── Lay out badges ──
    # Pre-calculate badge widths (approximate: 8px per char + padding)
    badges_info = []
    for lang in languages:
        label = f"{lang['name']}  {lang['percentage']}%"
        est_w = max(len(label) * 7.5 + 36, 80)
        badges_info.append({**lang, "label": label, "w": est_w})

    # Flow-wrap badges into rows
    rows: list[list[dict]] = [[]]
    row_w = 0
    for badge in badges_info:
        if row_w + badge["w"] + BADGE_GAP_X > MAX_WIDTH - PADDING * 2 and rows[-1]:
            rows.append([])
            row_w = 0
        rows[-1].append(badge)
        row_w += badge["w"] + BADGE_GAP_X

    total_h = PADDING * 2 + 40 + len(rows) * (BADGE_H + BADGE_GAP_Y)
    total_w = MAX_WIDTH

    extra_style = """
    @keyframes slideIn {
      from { opacity: 0; transform: translateX(-8px); }
      to { opacity: 1; transform: translateX(0); }
    }
    """

    lines = [svg_header(total_w, total_h, extra_style=extra_style)]

    # Background
    lines.append(rounded_rect(0, 0, total_w, total_h, rx=16, fill=COLORS["dark_bg"]))
    lines.append(rounded_rect(0, 0, total_w, total_h, rx=16, fill="none", stroke="url(#cardBorderGrad)", stroke_width=1.5))

    # Title
    lines.append(text_element(total_w / 2, 32, "🛠  Skills & Languages", size=16, fill=COLORS["lavender"], anchor="middle", weight="600"))

    # Render badges
    base_y = 50
    for row_idx, row in enumerate(rows):
        # Center the row
        row_total_w = sum(b["w"] for b in row) + (len(row) - 1) * BADGE_GAP_X
        start_x = (total_w - row_total_w) / 2
        y = base_y + row_idx * (BADGE_H + BADGE_GAP_Y)

        cur_x = start_x
        for badge in row:
            lines.append(_render_badge(cur_x, y, badge))
            cur_x += badge["w"] + BADGE_GAP_X

    lines.append(svg_footer())
    return "\n".join(lines)


def _render_badge(x: float, y: float, badge: dict) -> str:
    """Render a single pill-shaped language badge."""
    w = badge["w"]
    color = badge.get("color", COLORS["dusty_purple"])
    parts: list[str] = []

    parts.append(f"  <g>")

    # Pill background
    parts.append(
        f'    <rect x="{x}" y="{y}" width="{w}" height="{BADGE_H}" '
        f'rx="{BADGE_RX}" fill="{COLORS["card_bg"]}" '
        f'stroke="{COLORS["locked_border"]}" stroke-width="1" />'
    )

    # Language color dot
    dot_cx = x + 14
    dot_cy = y + BADGE_H / 2
    parts.append(f'    <circle cx="{dot_cx}" cy="{dot_cy}" r="5" fill="{color}" />')
    parts.append(f'    <circle cx="{dot_cx}" cy="{dot_cy}" r="5" fill="none" stroke="{COLORS["dark_bg"]}" stroke-width="1" />')

    # Label text
    parts.append(
        f'    <text x="{x + 26}" y="{y + BADGE_H / 2 + 4.5}" '
        f'font-size="11.5" fill="{COLORS["text_light"]}" '
        f'font-family="{FONT_FAMILY}">{badge["name"]}</text>'
    )

    # Percentage (muted, right side)
    parts.append(
        f'    <text x="{x + w - 10}" y="{y + BADGE_H / 2 + 4.5}" '
        f'font-size="10" fill="{COLORS["text_muted"]}" text-anchor="end" '
        f'font-family="{FONT_FAMILY}">{badge["percentage"]}%</text>'
    )

    parts.append("  </g>")
    return "\n".join(parts)
