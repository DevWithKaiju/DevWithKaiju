"""
Kaiju specimen card ("Field Notes" theme) - the centerpiece of the profile.
Renders the mascot's current growth stage as a labelled specimen card,
with a level, a growth (XP) gauge, and a field-note caption.
"""

from theme_field_notes import COLORS, FONT_MONO, svg_header, svg_footer, card_shell, text_element, kicker
from kaiju_growth import get_stage, xp_progress, level, embed_stage_image

CARD_W = 800
CARD_H = 246


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
    lines.append(card_shell(CARD_W, CARD_H, bg=COLORS["lavender"]))

    lines.append(kicker(30, 38, "Specimen Card"))
    lines.append(kicker(770, 38, f"Stage {stage['roman']} of V", anchor="end"))

    # Image box
    box_x, box_y, box_size = 30, 54, 170
    lines.append(card_shell(box_size, box_size, x=box_x, y=box_y, bg=COLORS["card_bg"]))
    img_size = 148
    img_x = box_x + (box_size - img_size) / 2
    img_y = box_y + (box_size - img_size) / 2
    lines.append(f'  <g class="kaiju-art">')
    lines.append(f'    <image x="{img_x}" y="{img_y}" width="{img_size}" height="{img_size}" href="{img_url}" />')
    lines.append(f'  </g>')

    # Text column
    text_x = 230
    lines.append(text_element(text_x, 92, stage["name"], size=24, fill=COLORS["ink"], weight="700"))
    lines.append(text_element(text_x, 114, f"LV. {lvl}  ·  {commits} total commits",
                               size=12, fill=COLORS["deep_purple"], family=FONT_MONO))

    bar_x, bar_y, bar_w, bar_h = text_x, 148, 540, 10
    lines.append(text_element(bar_x, bar_y - 8, "GROWTH", size=10, fill=COLORS["text_faint"],
                               weight="600", family=FONT_MONO, letter_spacing=1.2))
    if stage["max"] is not None:
        remaining = stage["max"] - commits
        gauge_note = f"{remaining} commits to next molt"
        note_color = COLORS["text"]
    else:
        gauge_note = "max stage reached"
        note_color = COLORS["teal"]
    lines.append(text_element(bar_x + bar_w, bar_y - 8, gauge_note, size=10, fill=note_color,
                               anchor="end", family=FONT_MONO))

    lines.append(f'  <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="2" '
                  f'fill="{COLORS["track_bg"]}" stroke="{COLORS["border"]}" stroke-width="1" />')
    fill_w = max(bar_w * progress, 8)
    lines.append(f'  <clipPath id="xpClip"><rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="2" /></clipPath>')
    lines.append(f'  <rect x="{bar_x}" y="{bar_y}" width="{fill_w}" height="{bar_h}" fill="{COLORS["teal"]}" clip-path="url(#xpClip)" />')
    # Tick marks every 10%
    for i in range(1, 10):
        tick_x = bar_x + bar_w * i / 10
        lines.append(f'  <line x1="{tick_x}" y1="{bar_y}" x2="{tick_x}" y2="{bar_y + bar_h}" '
                      f'stroke="{COLORS["ink"]}" stroke-opacity="0.1" stroke-width="1" />')

    # Field note caption
    caption_y = 176
    lines.append(f'  <line x1="{text_x}" y1="{caption_y}" x2="770" y2="{caption_y}" '
                  f'stroke="{COLORS["border"]}" stroke-width="1" stroke-dasharray="3,3" />')
    if stage["max"] is not None:
        caption = f"Field note &#8212; growth tracks commit activity. Next molt at {stage['max']} commits."
    else:
        caption = "Field note &#8212; fully grown. No further molts observed."
    lines.append(text_element(text_x, caption_y + 22, caption, size=12.5, fill=COLORS["text"], style="italic"))

    lines.append(svg_footer())
    return "\n".join(lines)
