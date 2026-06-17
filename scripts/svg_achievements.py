"""
Achievement badges SVG generator.
Creates cute milestone badges based on GitHub stats.
"""

from theme import COLORS, FONT_FAMILY, svg_header, svg_footer, rounded_rect, text_element


# ─── Achievement Definitions ────────────────────────────────

ACHIEVEMENTS = [
    # (id, icon, title, description, stat_key, thresholds)
    ("commits_100", "💻", "100+ Commits", "Contributed 100+ times", "total_commits", 100),
    ("commits_500", "🔥", "500+ Commits", "Contributed 500+ times", "total_commits", 500),
    ("stars_10", "⭐", "10+ Stars", "Earned 10+ stars", "total_stars", 10),
    ("stars_50", "🌟", "50+ Stars", "Earned 50+ stars", "total_stars", 50),
    ("repos_10", "📦", "10+ Repos", "Created 10+ repositories", "total_repos", 10),
    ("prs_10", "🔀", "10+ PRs", "Opened 10+ Pull Requests", "total_prs", 10),
    ("issues_10", "📝", "10+ Issues", "Opened 10+ Issues", "total_issues", 10),
    ("years_3", "🗓️", "3+ Years", "GitHub member for 3+ years", "account_age_years", 3),
]

# ─── Card dimensions ────────────────────────────────────────

CARD_W = 185
CARD_H = 95
GAP = 10
COLS = 4
PADDING = 20


def generate_achievements_svg(data: dict) -> str:
    """Generate the achievements badge grid SVG."""

    rows = (len(ACHIEVEMENTS) + COLS - 1) // COLS
    total_w = COLS * CARD_W + (COLS - 1) * GAP + PADDING * 2
    total_h = rows * CARD_H + (rows - 1) * GAP + PADDING * 2 + 40  # +40 for title

    # Build extra style for animations
    extra_style = """
    @keyframes sparkle {
      0%, 100% { opacity: 0.4; }
      50% { opacity: 1; }
    }
    .sparkle { animation: sparkle 2s ease-in-out infinite; }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(5px); }
      to { opacity: 1; transform: translateY(0); }
    }
    """

    lines = [svg_header(total_w, total_h, extra_style=extra_style)]

    # Background
    lines.append(rounded_rect(0, 0, total_w, total_h, rx=16, fill=COLORS["dark_bg"]))
    lines.append(rounded_rect(0, 0, total_w, total_h, rx=16, fill="none", stroke="url(#cardBorderGrad)", stroke_width=1.5))

    # Title
    lines.append(text_element(total_w / 2, 32, "🎯 GitHub Milestones", size=16, fill=COLORS["deep_purple"], anchor="middle", weight="700"))

    # Render each badge
    for idx, ach in enumerate(ACHIEVEMENTS):
        _id, icon, title, desc, stat_key, threshold = ach
        col = idx % COLS
        row = idx // COLS

        x = PADDING + col * (CARD_W + GAP)
        y = 48 + row * (CARD_H + GAP)

        value = data.get(stat_key, 0)
        unlocked = value >= threshold

        lines.append(_render_badge(x, y, icon, title, desc, unlocked, idx))

    lines.append(svg_footer())
    return "\n".join(lines)


def _render_badge(x: float, y: float, icon: str, title: str, desc: str, unlocked: bool, idx: int) -> str:
    """Render a single achievement badge card."""
    parts: list[str] = []

    # ── Card group ──
    delay = idx * 0.08
    parts.append(f'  <g>')

    if unlocked:
        # Unlocked card — gradient border, full color
        parts.append(rounded_rect(x, y, CARD_W, CARD_H, rx=10, fill=COLORS["card_bg"]))
        parts.append(rounded_rect(x, y, CARD_W, CARD_H, rx=10, fill="none", stroke="url(#cardBorderGrad)", stroke_width=1.2))

        # Icon circle
        cx = x + 32
        cy = y + CARD_H / 2
        parts.append(f'  <circle cx="{cx}" cy="{cy}" r="22" fill="{COLORS["dark_bg"]}" stroke="url(#purpleMintGrad)" stroke-width="1.5" />')
        parts.append(text_element(cx, cy + 6, icon, size=20, anchor="middle"))

        # Sparkle dots
        parts.append(f'  <circle cx="{x + CARD_W - 15}" cy="{y + 12}" r="2" fill="{COLORS["mint_green"]}" class="sparkle" style="animation-delay: {delay}s" />')
        parts.append(f'  <circle cx="{x + CARD_W - 8}" cy="{y + 18}" r="1.5" fill="{COLORS["dusty_purple"]}" class="sparkle" style="animation-delay: {delay + 0.4}s" />')

        # Text
        parts.append(text_element(x + 62, y + 38, title, size=12, fill=COLORS["text_light"], weight="600"))
        parts.append(text_element(x + 62, y + 56, desc, size=10, fill=COLORS["text_muted"]))

        # Check mark
        parts.append(text_element(x + 62, y + 76, "✅ Unlocked", size=9, fill=COLORS["mint_green"]))
    else:
        # Locked card — muted, grayscale
        parts.append(rounded_rect(x, y, CARD_W, CARD_H, rx=10, fill=COLORS["locked_bg"]))
        parts.append(rounded_rect(x, y, CARD_W, CARD_H, rx=10, fill="none", stroke=COLORS["locked_border"], stroke_width=1))

        # Icon circle (locked)
        cx = x + 32
        cy = y + CARD_H / 2
        parts.append(f'  <circle cx="{cx}" cy="{cy}" r="22" fill="{COLORS["dark_bg"]}" stroke="{COLORS["locked_border"]}" stroke-width="1.5" />')
        parts.append(text_element(cx, cy + 6, "🔒", size=18, anchor="middle", fill=COLORS["locked_text"]))

        # Text
        parts.append(text_element(x + 62, y + 38, title, size=12, fill=COLORS["locked_text"], weight="600"))
        parts.append(text_element(x + 62, y + 56, desc, size=10, fill=COLORS["locked_text"]))

        # Locked label
        parts.append(text_element(x + 62, y + 76, "🔒 Locked", size=9, fill=COLORS["locked_text"]))

    parts.append("  </g>")
    return "\n".join(parts)
