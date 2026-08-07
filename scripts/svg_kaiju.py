import os
import base64
import io
from theme import COLORS, FONT_FAMILY, svg_header, svg_footer, draw_card, rounded_rect, text_element, TEXT_BODY

CARD_W = 390
CARD_H = 260

def _get_stage(commits: int):
    # Same logic
    STAGES = [
        (0, "Egg", "", "Kaiju Egg", 50),
        (50, "Baby", "", "Baby Kaiju", 200),
        (200, "Junior", "", "Junior Kaiju", 500),
        (500, "Kaiju", "", "Kaiju", 1000),
        (1000, "King", "", "King Kaiju", None),
    ]
    current = STAGES[0]
    for stage in STAGES:
        if commits >= stage[0]:
            current = stage
    return current

def _xp_progress(commits: int, stage: tuple) -> float:
    if stage[4] is None: return 1.0
    return min((commits - stage[0]) / (stage[4] - stage[0]), 1.0)

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
    
    # 1. Copy the current stage image to current_kaiju.png (fallback)
    import shutil
    try:
        shutil.copyfile(img_path, out_path)
    except Exception as e:
        pass

    # Convert to base64 for embedding in the card
    try:
        from PIL import Image
        with Image.open(img_path) as img:
            img = img.resize((120, 120), Image.Resampling.LANCZOS)
            buffered = io.BytesIO()
            img.save(buffered, format="PNG", optimize=True)
            encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
        img_url = f"data:image/png;base64,{encoded_img}"
    except Exception as e:
        img_url = ""

    extra_defs = f"""
    <linearGradient id="xpBarGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{COLORS['mint_green']}" />
      <stop offset="100%" stop-color="#0d9488" />
    </linearGradient>
    """
    
    extra_style = """
    @keyframes float {
      0% { transform: translateY(-3px); }
      50% { transform: translateY(3px); }
      100% { transform: translateY(-3px); }
    }
    .kaiju-art {
      animation: float 3s ease-in-out infinite;
    }
    """
    
    lines = [svg_header(CARD_W, CARD_H, extra_defs=extra_defs, extra_style=extra_style)]
    
    # Draw standard card background & title
    lines.extend(draw_card(CARD_W, CARD_H, "My Kaiju", "🦖"))
    
    # Left side: Kaiju Image
    if img_url:
        lines.append(f'  <g class="kaiju-art" transform="translate(45, 80)">')
        lines.append(f'    <image x="0" y="0" width="120" height="120" href="{img_url}" />')
        lines.append(f'  </g>')
        
    # Right side: Stats
    text_x = 180
    
    # Title & Level Badge
    lines.append(text_element(text_x, 100, f"{stage[3]}", size=18, fill=COLORS["deep_purple"], anchor="start", weight="800"))
    
    lines.append(rounded_rect(text_x, 112, 54, 20, rx=10, fill=COLORS["lavender"]))
    lines.append(text_element(text_x + 27, 126, f"Lv. {level}", size=11, fill=COLORS["deep_purple"], anchor="middle", weight="800"))
    
    # Total Commits
    lines.append(text_element(text_x + 64, 126, f"{commits} total commits", size=11, fill=COLORS["text_muted"], anchor="start", weight="600"))

    # XP Bar section
    bar_y = 150
    bar_w = 170
    bar_h = 12

    lines.append(text_element(text_x, bar_y - 6, "EXP", size=10, fill=COLORS["text_muted"], weight="700"))

    if stage[4] is not None:
        remaining = stage[4] - commits
        lines.append(text_element(text_x + bar_w, bar_y - 6, f"{remaining} commits to next stage", size=9, fill=COLORS["text_light"], anchor="end"))
    else:
        lines.append(text_element(text_x + bar_w, bar_y - 6, "MAX STAGE", size=9, fill=COLORS["gold"], anchor="end"))

    # Bar background
    lines.append(rounded_rect(text_x, bar_y, bar_w, bar_h, rx=6, fill=COLORS["locked_bg"]))

    # Bar fill
    fill_w = max(bar_w * progress, 8)
    lines.append(f'  <clipPath id="xpClip"><rect x="{text_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="6" /></clipPath>')
    lines.append(f'  <rect x="{text_x}" y="{bar_y}" width="{fill_w}" height="{bar_h}" rx="6" fill="url(#xpBarGrad)" clip-path="url(#xpClip)" />')

    lines.append(svg_footer())
    return "\n".join(lines)
