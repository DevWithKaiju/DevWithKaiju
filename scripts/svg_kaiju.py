"""
Kaiju specimen card - the centerpiece of the profile.
Renders the mascot's current growth stage as a labelled specimen card,
with a level, a growth (XP) gauge, and a field-note caption.
"""

import os
import io
import base64

from theme import COLORS, FONT_MONO, svg_header, svg_footer, card_shell, text_element, kicker

CARD_W = 800
CARD_H = 246

# Stage thresholds (min commits), the on-disk art file, the display name and
# a roman-numeral stage index. File stems intentionally do NOT mirror the
# display names (stage 4 displays as "Kaiju" but its art file is stage_adult.png) -
# keep this mapping explicit rather than deriving the filename from the name.
STAGES = [
    {"min": 0, "max": 50, "file": "egg", "name": "Kaiju Egg", "roman": "I"},
    {"min": 50, "max": 200, "file": "baby", "name": "Baby Kaiju", "roman": "II"},
    {"min": 200, "max": 500, "file": "junior", "name": "Junior Kaiju", "roman": "III"},
    {"min": 500, "max": 1000, "file": "adult", "name": "Kaiju", "roman": "IV"},
    {"min": 1000, "max": None, "file": "king", "name": "King Kaiju", "roman": "V"},
]


def _get_stage(commits: int) -> dict:
    current = STAGES[0]
    for stage in STAGES:
        if commits >= stage["min"]:
            current = stage
    return current


def _xp_progress(commits: int, stage: dict) -> float:
    if stage["max"] is None:
        return 1.0
    return min((commits - stage["min"]) / (stage["max"] - stage["min"]), 1.0)


def _level(commits: int) -> int:
    return max(1, commits // 20 + 1)


def _autocrop_to_square(img, padding_ratio: float = 0.25):
    """The source art sits on a near-white canvas with a large margin around the
    character; crop to its silhouette's bounding box (plus a little breathing
    room) so it actually fills the specimen frame instead of floating in a sea
    of white. A plain white-vs-image diff won't find this box: resizing/pasting
    during asset prep leaves faint sub-255 noise across the whole canvas, so the
    box must come from a real brightness threshold instead."""
    from PIL import Image

    mask = img.convert("L").point(lambda p: 255 if p < 245 else 0)
    bbox = mask.getbbox()
    if bbox is None:
        return img

    left, top, right, bottom = bbox
    pad = int(max(right - left, bottom - top) * padding_ratio)
    left, top = max(left - pad, 0), max(top - pad, 0)
    right, bottom = min(right + pad, img.width), min(bottom + pad, img.height)

    # Pad out to a centered square so the mascot doesn't get stretched.
    side = max(right - left, bottom - top)
    cx, cy = (left + right) / 2, (top + bottom) / 2
    sq_left, sq_top = int(cx - side / 2), int(cy - side / 2)
    canvas = Image.new(img.mode, (side, side), (255, 255, 255))
    crop = img.crop((max(sq_left, 0), max(sq_top, 0),
                      min(sq_left + side, img.width), min(sq_top + side, img.height)))
    canvas.paste(crop, (max(-sq_left, 0), max(-sq_top, 0)))
    return canvas


def _embed_stage_image(file_stem: str) -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(os.path.dirname(script_dir), "images", f"stage_{file_stem}.png")

    from PIL import Image
    with Image.open(img_path) as img:
        img = _autocrop_to_square(img)
        img = img.resize((260, 260), Image.Resampling.LANCZOS)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG", optimize=True)
        encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def generate_kaiju_svg(data: dict) -> str:
    commits = data.get("total_commits", 0)
    stage = _get_stage(commits)
    progress = _xp_progress(commits, stage)
    level = _level(commits)
    img_url = _embed_stage_image(stage["file"])

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
    lines.append(text_element(text_x, 114, f"LV. {level}  ·  {commits} total commits",
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
