"""
Kaiju Growth Card SVG generator.
A unique card where a cute dinosaur evolves based on total commits.
"""

import os
from theme import COLORS, FONT_FAMILY, svg_header, svg_footer, rounded_rect, text_element

# ─── Growth Stages ──────────────────────────────────────────

STAGES = [
    # (min_commits, label, emoji, title, next_threshold)
    (0, "Egg", "🥚", "Kaiju Egg", 50),
    (50, "Baby", "🐣", "Baby Kaiju", 200),
    (200, "Junior", "🦎", "Junior Kaiju", 500),
    (500, "Kaiju", "🦖", "Kaiju", 1000),
    (1000, "King", "👑", "King Kaiju", None),
]

CARD_W = 420
CARD_H = 320

def _get_stage(commits: int):
    current = STAGES[0]
    for stage in STAGES:
        if commits >= stage[0]:
            current = stage
    return current

def _xp_progress(commits: int, stage: tuple) -> float:
    if stage[4] is None:
        return 1.0
    floor = stage[0]
    ceiling = stage[4]
    return min((commits - floor) / (ceiling - floor), 1.0)

def _level(commits: int) -> int:
    return max(1, commits // 20 + 1)

def generate_kaiju_svg(data: dict) -> str:
    commits = data.get("total_commits", 0)
    stage = _get_stage(commits)
    progress = _xp_progress(commits, stage)
    level = _level(commits)

    extra_defs = f"""
    <linearGradient id="xpBarGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{COLORS['dusty_purple']}" />
      <stop offset="100%" stop-color="{COLORS['mint_green']}" />
    </linearGradient>
    """

    extra_style = ""

    lines = [svg_header(CARD_W, CARD_H, extra_defs=extra_defs, extra_style=extra_style)]

    # Use pure white background to blend perfectly with the generated image background
    lines.append(rounded_rect(0, 0, CARD_W, CARD_H, rx=16, fill=COLORS["white"]))
    lines.append(rounded_rect(0, 0, CARD_W, CARD_H, rx=16, fill="none", stroke="url(#cardBorderGrad)", stroke_width=1.5))

    # Title
    lines.append(text_element(CARD_W / 2, 30, f"🦖  {stage[3]}", size=17, fill=COLORS["deep_purple"], anchor="middle", weight="700"))

    # Level badge
    lv_x = CARD_W / 2
    lines.append(rounded_rect(lv_x - 30, 38, 60, 22, rx=11, fill=COLORS["white"], stroke="url(#purpleMintGrad)", stroke_width=1.2))
    lines.append(text_element(lv_x, 54, f"Lv. {level}", size=11, fill=COLORS["deep_purple"], anchor="middle", weight="700"))

    # Kaiju art (centered)
    art_cx = CARD_W / 2
    art_cy = 150
    lines.append(f'  <g class="kaiju-art" transform="translate({art_cx},{art_cy})">')
    # Use raw github URL to bypass GitHub SVG raster stripping
    img_size = 140
    stage_name = stage[1].lower()
    repo_env = os.environ.get('GITHUB_REPOSITORY', 'DevWithKaiju/DevWithKaiju')
    img_url = f"https://raw.githubusercontent.com/{repo_env}/main/images/stage_{stage_name}.png"
    lines.append(f'    <image x="{-img_size/2}" y="{-img_size/2}" width="{img_size}" height="{img_size}" href="{img_url}" xlink:href="{img_url}" />')
    lines.append("  </g>")

    # Decorative elements
    lines.append(f'  <circle cx="40" cy="90" r="3" fill="{COLORS["dusty_purple"]}" opacity="0.4" />')
    lines.append(f'  <circle cx="380" cy="100" r="2.5" fill="{COLORS["mint_green"]}" opacity="0.5" />')
    lines.append(f'  <circle cx="60" cy="250" r="2" fill="{COLORS["soft_pink"]}" opacity="0.6" />')
    lines.append(f'  <circle cx="360" cy="240" r="3.5" fill="{COLORS["dusty_purple"]}" opacity="0.3" />')

    # XP Bar section
    bar_y = 250
    bar_x = 60
    bar_w = 300
    bar_h = 14

    lines.append(text_element(bar_x, bar_y - 6, "EXP", size=10, fill=COLORS["text_muted"], weight="600"))

    if stage[4] is not None:
        remaining = stage[4] - commits
        lines.append(text_element(bar_x + bar_w, bar_y - 6, f"{remaining} commits to next stage", size=9, fill=COLORS["text_muted"], anchor="end"))
    else:
        lines.append(text_element(bar_x + bar_w, bar_y - 6, "MAX STAGE ✨", size=9, fill=COLORS["gold"], anchor="end"))

    # Bar background
    lines.append(rounded_rect(bar_x, bar_y, bar_w, bar_h, rx=7, fill=COLORS["locked_bg"]))

    # Bar fill
    fill_w = max(bar_w * progress, 8)
    lines.append(f'  <clipPath id="xpClip"><rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="7" /></clipPath>')
    lines.append(f'  <rect x="{bar_x}" y="{bar_y}" width="{fill_w}" height="{bar_h}" rx="7" fill="url(#xpBarGrad)" clip-path="url(#xpClip)" />')

    # Commit counter
    lines.append(text_element(CARD_W / 2, bar_y + bar_h + 22, f"🔥 {commits} total commits", size=12, fill=COLORS["deep_purple"], anchor="middle", weight="700"))

    # Bottom decorative line
    lines.append(f'  <line x1="60" y1="{CARD_H - 15}" x2="{CARD_W - 60}" y2="{CARD_H - 15}" stroke="url(#purpleMintGradH)" stroke-width="1.5" stroke-opacity="0.3" />')

    lines.append(svg_footer())
    return "\n".join(lines)
