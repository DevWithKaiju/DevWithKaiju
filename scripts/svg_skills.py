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

    extra_defs = """
    <filter id="badgeShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#5A5070" flood-opacity="0.1"/>
    </filter>
    <linearGradient id="badgeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#F4F1FA" stop-opacity="0.9" />
    </linearGradient>
    """

    extra_style = """
    @keyframes slideUpFade {
      0% { opacity: 0; transform: translateY(12px); }
      100% { opacity: 1; transform: translateY(0); }
    }
    .badge {
      opacity: 0;
      animation: slideUpFade 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }
    .badge rect {
      transition: all 0.3s ease;
    }
    .badge:hover rect {
      stroke: #9B8EC4;
      stroke-width: 1.5;
      transform: translateY(-1px);
    }
    """

    lines = [svg_header(total_w, total_h, extra_defs=extra_defs, extra_style=extra_style)]

    # Background
    lines.append(rounded_rect(0, 0, total_w, total_h, rx=16, fill=COLORS["dark_bg"]))
    lines.append(rounded_rect(0, 0, total_w, total_h, rx=16, fill="none", stroke="url(#cardBorderGrad)", stroke_width=1.5))

    # Title
    lines.append(text_element(total_w / 2, 32, "🛠  Skills &amp; Languages", size=16, fill=COLORS["deep_purple"], anchor="middle", weight="700"))

    # Render badges
    base_y = 50
    badge_idx = 0
    for row_idx, row in enumerate(rows):
        # Center the row
        row_total_w = sum(b["w"] for b in row) + (len(row) - 1) * BADGE_GAP_X
        start_x = (total_w - row_total_w) / 2
        y = base_y + row_idx * (BADGE_H + BADGE_GAP_Y)

        cur_x = start_x
        for badge in row:
            delay = 0.1 + (badge_idx * 0.05)
            lines.append(_render_badge(cur_x, y, badge, delay))
            cur_x += badge["w"] + BADGE_GAP_X
            badge_idx += 1

    lines.append(svg_footer())
    return "\n".join(lines)


def _render_badge(x: float, y: float, badge: dict, delay: float) -> str:
    """Render a single pill-shaped language badge with animation."""
    w = badge["w"]
    color = badge.get("color", COLORS["dusty_purple"])
    parts: list[str] = []

    # Use a group with animation delay
    parts.append(f'  <g class="badge" style="animation-delay: {delay}s" transform-origin="{x + w/2} {y + BADGE_H/2}">')

    # Pill background with gradient and shadow
    parts.append(
        f'    <rect x="{x}" y="{y}" width="{w}" height="{BADGE_H}" '
        f'rx="{BADGE_RX}" fill="url(#badgeGrad)" '
        f'stroke="{COLORS["locked_border"]}" stroke-width="1" '
        f'filter="url(#badgeShadow)" />'
    )

    # Language color dot with slight glow
    dot_cx = x + 14
    dot_cy = y + BADGE_H / 2
    parts.append(f'    <circle cx="{dot_cx}" cy="{dot_cy}" r="6" fill="{color}" opacity="0.3" />')
    parts.append(f'    <circle cx="{dot_cx}" cy="{dot_cy}" r="4" fill="{color}" />')

    # Label text (bolded language name)
    parts.append(
        f'    <text x="{x + 26}" y="{y + BADGE_H / 2 + 4}" '
        f'font-size="11.5" fill="{COLORS["text_light"]}" font-weight="600" '
        f'font-family="{FONT_FAMILY}">{badge["name"]}</text>'
    )

    # Percentage
    parts.append(
        f'    <text x="{x + w - 10}" y="{y + BADGE_H / 2 + 3.5}" '
        f'font-size="10" fill="{COLORS["text_muted"]}" text-anchor="end" font-weight="500" '
        f'font-family="{FONT_FAMILY}">{badge["percentage"]}%</text>'
    )

    parts.append("  </g>")
    return "\n".join(parts)
