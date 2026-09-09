"""
Kaiju growth-stage data and mascot-art embedding, shared by every theme package.
Only the drawing differs between themes - the stage math and the source art are the same mascot.
"""

import os
import io
import base64

# Stage thresholds (min commits), the on-disk art file, the display name and a
# roman-numeral stage index. File stems intentionally do NOT mirror the display
# names (stage 4 displays as "Kaiju" but its art file is stage_adult.png) - keep
# this mapping explicit rather than deriving the filename from the name.
STAGES = [
    {"min": 0, "max": 50, "file": "egg", "name": "Kaiju Egg", "roman": "I"},
    {"min": 50, "max": 200, "file": "baby", "name": "Baby Kaiju", "roman": "II"},
    {"min": 200, "max": 500, "file": "junior", "name": "Junior Kaiju", "roman": "III"},
    {"min": 500, "max": 1000, "file": "adult", "name": "Kaiju", "roman": "IV"},
    {"min": 1000, "max": None, "file": "king", "name": "King Kaiju", "roman": "V"},
]


def get_stage(commits: int) -> dict:
    current = STAGES[0]
    for stage in STAGES:
        if commits >= stage["min"]:
            current = stage
    return current


def xp_progress(commits: int, stage: dict) -> float:
    if stage["max"] is None:
        return 1.0
    return min((commits - stage["min"]) / (stage["max"] - stage["min"]), 1.0)


def level(commits: int) -> int:
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

    side = max(right - left, bottom - top)
    cx, cy = (left + right) / 2, (top + bottom) / 2
    sq_left, sq_top = int(cx - side / 2), int(cy - side / 2)
    canvas = Image.new(img.mode, (side, side), (255, 255, 255))
    crop = img.crop((max(sq_left, 0), max(sq_top, 0),
                      min(sq_left + side, img.width), min(sq_top + side, img.height)))
    canvas.paste(crop, (max(-sq_left, 0), max(-sq_top, 0)))
    return canvas


def embed_stage_image(file_stem: str, size: int = 260) -> str:
    """Return a base64 data: URI of the given stage's art, autocropped to its silhouette."""
    # This file lives at scripts/common/kaiju_growth.py - repo root is two levels up.
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    img_path = os.path.join(repo_root, "images", f"stage_{file_stem}.png")

    from PIL import Image
    with Image.open(img_path) as img:
        img = _autocrop_to_square(img)
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG", optimize=True)
        encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"
