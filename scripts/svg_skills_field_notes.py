"""
Toolkit card - a single stacked language-composition bar plus a dot-legend,
instead of a wall of per-language pill badges.
"""

from theme_field_notes import COLORS, FONT_MONO, svg_header, svg_footer, card_shell, text_element, kicker

CARD_W = 800
PADDING = 30
BAR_H = 14
MAX_SEGMENTS = 6  # top N languages get their own segment; the rest are bucketed as "Other"


def _prepare_languages(languages: list[dict]) -> list[dict]:
    if not languages:
        return [{"name": "No data", "color": COLORS["text_faint"], "percentage": 100.0}]

    top = languages[:MAX_SEGMENTS]
    rest = languages[MAX_SEGMENTS:]
    if rest:
        other_pct = round(sum(l["percentage"] for l in rest), 1)
        top = top + [{"name": "Other", "color": COLORS["lavender_accent"], "percentage": other_pct}]
    return top


def generate_skills_svg(data: dict) -> str:
    langs = _prepare_languages(data.get("languages", []))

    # Wrap legend chips into rows (rough width estimate per chip, mono font).
    chip_gap_x, chip_gap_y = 22, 20
    max_row_w = CARD_W - PADDING * 2
    chips = []
    for lang in langs:
        label = f"{lang['name']}  {lang['percentage']}%"
        chips.append({**lang, "label": label, "w": len(label) * 6.6 + 18})

    rows: list[list[dict]] = [[]]
    row_w = 0.0
    for chip in chips:
        if row_w + chip["w"] + chip_gap_x > max_row_w and rows[-1]:
            rows.append([])
            row_w = 0.0
        rows[-1].append(chip)
        row_w += chip["w"] + chip_gap_x

    bar_y = 58
    legend_top = bar_y + BAR_H + 26
    card_h = legend_top + len(rows) * chip_gap_y + 16

    lines = [svg_header(CARD_W, card_h)]
    lines.append(card_shell(CARD_W, card_h))
    lines.append(kicker(PADDING, 38, "Toolkit"))

    # Stacked bar
    bar_w = CARD_W - PADDING * 2
    lines.append(f'  <clipPath id="langBarClip"><rect x="{PADDING}" y="{bar_y}" width="{bar_w}" height="{BAR_H}" rx="2" /></clipPath>')
    lines.append(f'  <g clip-path="url(#langBarClip)">')
    lines.append(f'    <rect x="{PADDING}" y="{bar_y}" width="{bar_w}" height="{BAR_H}" fill="{COLORS["track_bg"]}" />')
    cursor_x = PADDING
    for lang in langs:
        seg_w = bar_w * lang["percentage"] / 100
        lines.append(f'    <rect x="{cursor_x}" y="{bar_y}" width="{seg_w}" height="{BAR_H}" fill="{lang["color"]}" />')
        cursor_x += seg_w
    lines.append('  </g>')
    lines.append(f'  <rect x="{PADDING}" y="{bar_y}" width="{bar_w}" height="{BAR_H}" rx="2" '
                  f'fill="none" stroke="{COLORS["border"]}" stroke-width="1" />')

    # Legend
    for row_idx, row in enumerate(rows):
        y = legend_top + row_idx * chip_gap_y
        x = PADDING
        for chip in row:
            lines.append(f'  <circle cx="{x + 5}" cy="{y - 4}" r="4.5" fill="{chip["color"]}" />')
            lines.append(text_element(x + 16, y, chip["label"], size=11.5, fill=COLORS["ink"], family=FONT_MONO))
            x += chip["w"] + chip_gap_x

    lines.append(svg_footer())
    return "\n".join(lines)
