"""
Toolkit block ("Broadsheet" theme) - a thick stacked language bar with
a square-marker legend, instead of a wall of pill badges.
"""

from themes.broadsheet.theme import COLORS, CHART_PALETTE, FONT_MONO, svg_header, svg_footer, text_element, kicker

CARD_W = 800
PADDING = 30
BAR_H = 22
MAX_SEGMENTS = 6  # top N languages get their own segment; the rest are bucketed as "Other"


def _prepare_languages(languages: list[dict]) -> list[dict]:
    if not languages:
        return [{"name": "No data", "color": COLORS["muted"], "percentage": 100.0}]

    top = [dict(lang) for lang in languages[:MAX_SEGMENTS]]  # copy - we're about to overwrite "color"
    rest = languages[MAX_SEGMENTS:]
    if rest:
        other_pct = round(sum(l["percentage"] for l in rest), 1)
        top = top + [{"name": "Other", "percentage": other_pct}]

    # Rank-based tones from the page's own palette, not each language's GitHub
    # brand color - those are a clash of unrelated hues against the rest of the page.
    for i, lang in enumerate(top):
        lang["color"] = CHART_PALETTE[min(i, len(CHART_PALETTE) - 1)]
    return top


def generate_skills_svg(data: dict) -> str:
    langs = _prepare_languages(data.get("languages", []))

    chip_gap_x, chip_gap_y = 22, 20
    max_row_w = CARD_W - PADDING * 2
    chips = []
    for lang in langs:
        label = f"{lang['name']}  {lang['percentage']}%"
        chips.append({**lang, "label": label, "w": len(label) * 6.6 + 22})

    rows: list[list[dict]] = [[]]
    row_w = 0.0
    for chip in chips:
        if row_w + chip["w"] + chip_gap_x > max_row_w and rows[-1]:
            rows.append([])
            row_w = 0.0
        rows[-1].append(chip)
        row_w += chip["w"] + chip_gap_x

    bar_y = 56
    legend_top = bar_y + BAR_H + 28
    card_h = legend_top + len(rows) * chip_gap_y + 16

    lines = [svg_header(CARD_W, card_h)]
    lines.append(kicker(PADDING, 30, "Toolkit"))

    bar_w = CARD_W - PADDING * 2
    cursor_x = PADDING
    for lang in langs:
        seg_w = bar_w * lang["percentage"] / 100
        lines.append(f'  <rect x="{cursor_x}" y="{bar_y}" width="{seg_w}" height="{BAR_H}" fill="{lang["color"]}" />')
        cursor_x += seg_w

    for row_idx, row in enumerate(rows):
        y = legend_top + row_idx * chip_gap_y
        x = PADDING
        for chip in row:
            lines.append(f'  <rect x="{x}" y="{y - 9}" width="10" height="10" fill="{chip["color"]}" />')
            lines.append(text_element(x + 18, y, chip["label"], size=11.5, fill=COLORS["ink"], family=FONT_MONO))
            x += chip["w"] + chip_gap_x

    lines.append(svg_footer())
    return "\n".join(lines)
