"""
Kaiju hero block ("Minimal Editorial" theme) - a solid color block with the
mascot and a huge level number, instead of a soft specimen card.
"""

from theme_minimal_editorial import COLORS, FONT_DISPLAY, FONT_MONO, svg_header, svg_footer, text_element, kicker
from kaiju_growth import get_stage, xp_progress, level, embed_stage_image

CARD_W = 800
CARD_H = 268


def generate_kaiju_svg(data: dict) -> str:
    commits = data.get("total_commits", 0)
    stage = get_stage(commits)
    progress = xp_progress(commits, stage)
    lvl = level(commits)
    img_url = embed_stage_image(stage["file"])

    extra_style = """
    @keyframes float {
      0% { transform: translateY(-3px); }
      50% { transform: translateY(3px); }
      100% { transform: translateY(-3px); }
    }
    .kaiju-art { animation: float 3s ease-in-out infinite; }
    """

    lines = [svg_header(CARD_W, CARD_H, extra_style=extra_style)]
    lines.append(f'  <rect x="0" y="0" width="{CARD_W}" height="{CARD_H}" rx="2" fill="{COLORS["purple_block"]}" />')

    lines.append(kicker(30, 42, f"Stage {stage['roman']} / V · Specimen 03", color=COLORS["lavender"]))

    # Mascot
    box_x, box_y, box_size = 30, 66, 176
    lines.append(f'  <rect x="{box_x}" y="{box_y}" width="{box_size}" height="{box_size}" rx="2" fill="{COLORS["white"]}" />')
    img_size = 152
    img_x = box_x + (box_size - img_size) / 2
    img_y = box_y + (box_size - img_size) / 2
    lines.append(f'  <g class="kaiju-art">')
    lines.append(f'    <image x="{img_x}" y="{img_y}" width="{img_size}" height="{img_size}" href="{img_url}" />')
    lines.append(f'  </g>')

    # Text column
    text_x = box_x + box_size + 36
    lines.append(text_element(text_x, box_y + 20, stage["name"].upper(), size=13, fill=COLORS["lavender"],
                               weight="700", family=FONT_MONO, letter_spacing=0.6))
    lines.append(text_element(text_x, box_y + 90, f"LV{lvl}", size=68, fill=COLORS["white"],
                               weight="900", family=FONT_DISPLAY))
    lines.append(text_element(text_x, box_y + 112, f"{commits} COMMITS TOTAL", size=10.5, fill=COLORS["lavender"],
                               family=FONT_MONO, letter_spacing=0.8))

    bar_x, bar_y, bar_w, bar_h = text_x, box_y + 132, CARD_W - text_x - 30, 8
    lines.append(f'  <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="1" fill="rgba(255,255,255,0.28)" />')
    fill_w = max(bar_w * progress, 6)
    lines.append(f'  <clipPath id="xpClip"><rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="1" /></clipPath>')
    lines.append(f'  <rect x="{bar_x}" y="{bar_y}" width="{fill_w}" height="{bar_h}" fill="{COLORS["teal"]}" clip-path="url(#xpClip)" />')

    if stage["max"] is not None:
        molt_note = f"{stage['max'] - commits} COMMITS TO NEXT MOLT"
    else:
        molt_note = "MAX STAGE REACHED"
    lines.append(text_element(text_x, bar_y + 22, molt_note, size=10, fill=COLORS["lavender"],
                               family=FONT_MONO, letter_spacing=0.8))

    lines.append(svg_footer())
    return "\n".join(lines)
