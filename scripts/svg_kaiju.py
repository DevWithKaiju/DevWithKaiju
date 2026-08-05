"""
Kaiju Growth Card SVG generator.
A unique card where a cute dinosaur evolves based on total commits.
"""

import os
import base64
import io
from theme import COLORS, FONT_FAMILY, svg_header, svg_footer, rounded_rect, text_element

# ─── Growth Stages ──────────────────────────────────────────

STAGES = [
    # (min_commits, label, icon, title, next_threshold)
    (0, "Egg", "", "Kaiju Egg", 50),
    (50, "Baby", "", "Baby Kaiju", 200),
    (200, "Junior", "", "Junior Kaiju", 500),
    (500, "Kaiju", "", "Kaiju", 1000),
    (1000, "King", "", "King Kaiju", None),
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
    stage_name = stage[1].lower()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    img_path = os.path.join(project_root, "images", f"stage_{stage_name}.png")
    out_path = os.path.join(project_root, "images", "current_kaiju.png")
    
    # 1. Copy the current stage image to current_kaiju.png for direct HTML rendering
    import shutil
    try:
        shutil.copyfile(img_path, out_path)
    except Exception as e:
        pass

    # 2. Generate minimalist SVG for status (NO CARD BACKGROUND, NO RASTER IMAGE)
    # Dimension is compact to sit nicely next to the PNG
    svg_w = 260
    svg_h = 120
    
    extra_defs = f"""
    <linearGradient id="xpBarGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{COLORS['mint_green']}" />
      <stop offset="100%" stop-color="#0d9488" />
    </linearGradient>
    """
    
    lines = [svg_header(svg_w, svg_h, extra_defs=extra_defs)]
    
    # We DO NOT add a white background rect or a border rect. It's completely transparent!
    
    # Title & Level Badge
    lines.append(text_element(0, 30, f"{stage[3]}", size=18, fill=COLORS["deep_purple"], anchor="start", weight="800"))
    
    lines.append(rounded_rect(0, 42, 54, 20, rx=10, fill=COLORS["lavender"]))
    lines.append(text_element(27, 56, f"Lv. {level}", size=11, fill=COLORS["deep_purple"], anchor="middle", weight="800"))
    
    # Total Commits
    lines.append(text_element(64, 56, f"{commits} total commits", size=11, fill=COLORS["text_muted"], anchor="start", weight="600"))

    # XP Bar section
    bar_y = 80
    bar_x = 0
    bar_w = 260
    bar_h = 12

    lines.append(text_element(bar_x, bar_y - 6, "EXP", size=10, fill=COLORS["text_muted"], weight="700"))

    if stage[4] is not None:
        remaining = stage[4] - commits
        lines.append(text_element(bar_x + bar_w, bar_y - 6, f"{remaining} commits to next stage", size=9, fill=COLORS["text_light"], anchor="end"))
    else:
        lines.append(text_element(bar_x + bar_w, bar_y - 6, "MAX STAGE", size=9, fill=COLORS["gold"], anchor="end"))

    # Bar background
    lines.append(rounded_rect(bar_x, bar_y, bar_w, bar_h, rx=6, fill=COLORS["locked_bg"]))

    # Bar fill
    fill_w = max(bar_w * progress, 8)
    lines.append(f'  <clipPath id="xpClip"><rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="6" /></clipPath>')
    lines.append(f'  <rect x="{bar_x}" y="{bar_y}" width="{fill_w}" height="{bar_h}" rx="6" fill="url(#xpBarGrad)" clip-path="url(#xpClip)" />')

    lines.append(svg_footer())
    return "\n".join(lines)
