"""
Kaiju Growth Card SVG generator.
A unique card where a cute dinosaur evolves based on total commits.
"""

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
    """Determine growth stage from commit count."""
    current = STAGES[0]
    for stage in STAGES:
        if commits >= stage[0]:
            current = stage
    return current


def _xp_progress(commits: int, stage: tuple) -> float:
    """Calculate XP progress within current stage (0.0 – 1.0)."""
    if stage[4] is None:  # Max stage
        return 1.0
    floor = stage[0]
    ceiling = stage[4]
    return min((commits - floor) / (ceiling - floor), 1.0)


def _level(commits: int) -> int:
    """Simple level: 1 level per 20 commits."""
    return max(1, commits // 20 + 1)


# ─── Dinosaur SVG Art ───────────────────────────────────────

def _draw_egg(cx: float, cy: float) -> str:
    """Draw a cute egg with crack lines."""
    return f"""
  <g transform="translate({cx},{cy})">
    <!-- egg body -->
    <ellipse cx="0" cy="0" rx="32" ry="42" fill="{COLORS['lavender']}" />
    <ellipse cx="0" cy="0" rx="32" ry="42" fill="none" stroke="{COLORS['dusty_purple']}" stroke-width="2" />
    <!-- crack -->
    <polyline points="-12,-5 -5,2 -14,8 -6,14" fill="none" stroke="{COLORS['deep_purple']}" stroke-width="1.5" stroke-linecap="round" />
    <!-- spots -->
    <circle cx="10" cy="-15" r="4" fill="{COLORS['soft_mint']}" opacity="0.6" />
    <circle cx="-8" cy="10" r="3" fill="{COLORS['soft_pink']}" opacity="0.5" />
    <circle cx="14" cy="8" r="2.5" fill="{COLORS['mint_green']}" opacity="0.5" />
    <!-- sparkle -->
    <text x="28" y="-30" font-size="14" text-anchor="middle">✨</text>
  </g>"""


def _draw_baby(cx: float, cy: float) -> str:
    """Draw a tiny cute dinosaur hatching."""
    return f"""
  <g transform="translate({cx},{cy})">
    <!-- egg shell bottom -->
    <path d="M-22,10 Q-25,-5 -15,-10 L15,-10 Q25,-5 22,10 Z" fill="{COLORS['lavender']}" stroke="{COLORS['dusty_purple']}" stroke-width="1.5" />
    <path d="M-22,10 Q-20,25 0,28 Q20,25 22,10 Z" fill="{COLORS['lavender']}" stroke="{COLORS['dusty_purple']}" stroke-width="1.5" />
    <!-- zigzag crack line on shell -->
    <polyline points="-22,10 -14,5 -6,12 2,4 10,11 18,6 22,10" fill="none" stroke="{COLORS['deep_purple']}" stroke-width="1.2" />
    <!-- baby dino head poking out -->
    <ellipse cx="0" cy="-22" rx="18" ry="16" fill="{COLORS['mint_green']}" />
    <ellipse cx="0" cy="-22" rx="18" ry="16" fill="none" stroke="{COLORS['deep_purple']}" stroke-width="1.5" />
    <!-- eyes -->
    <circle cx="-6" cy="-24" r="4" fill="{COLORS['dark_bg']}" />
    <circle cx="6" cy="-24" r="4" fill="{COLORS['dark_bg']}" />
    <circle cx="-5" cy="-25" r="1.5" fill="{COLORS['white']}" />
    <circle cx="7" cy="-25" r="1.5" fill="{COLORS['white']}" />
    <!-- blush -->
    <ellipse cx="-12" cy="-18" rx="4" ry="2.5" fill="{COLORS['soft_pink']}" opacity="0.5" />
    <ellipse cx="12" cy="-18" rx="4" ry="2.5" fill="{COLORS['soft_pink']}" opacity="0.5" />
    <!-- tiny horns -->
    <circle cx="-8" cy="-37" r="3" fill="{COLORS['soft_mint']}" />
    <circle cx="8" cy="-37" r="3" fill="{COLORS['soft_mint']}" />
    <!-- sparkle -->
    <text x="26" y="-36" font-size="12" text-anchor="middle">💖</text>
  </g>"""


def _draw_junior(cx: float, cy: float) -> str:
    """Draw a medium-sized cute dinosaur."""
    return f"""
  <g transform="translate({cx},{cy})">
    <!-- body -->
    <ellipse cx="0" cy="10" rx="28" ry="22" fill="{COLORS['mint_green']}" />
    <ellipse cx="0" cy="10" rx="28" ry="22" fill="none" stroke="{COLORS['deep_purple']}" stroke-width="1.5" />
    <!-- head -->
    <ellipse cx="0" cy="-20" rx="22" ry="18" fill="{COLORS['mint_green']}" />
    <ellipse cx="0" cy="-20" rx="22" ry="18" fill="none" stroke="{COLORS['deep_purple']}" stroke-width="1.5" />
    <!-- tummy -->
    <ellipse cx="0" cy="12" rx="18" ry="14" fill="{COLORS['soft_mint']}" opacity="0.6" />
    <!-- eyes -->
    <circle cx="-7" cy="-22" r="5" fill="{COLORS['dark_bg']}" />
    <circle cx="7" cy="-22" r="5" fill="{COLORS['dark_bg']}" />
    <circle cx="-5.5" cy="-23.5" r="2" fill="{COLORS['white']}" />
    <circle cx="8.5" cy="-23.5" r="2" fill="{COLORS['white']}" />
    <!-- mouth smile -->
    <path d="M-5,-12 Q0,-8 5,-12" fill="none" stroke="{COLORS['deep_purple']}" stroke-width="1.2" stroke-linecap="round" />
    <!-- blush -->
    <ellipse cx="-15" cy="-16" rx="5" ry="3" fill="{COLORS['soft_pink']}" opacity="0.5" />
    <ellipse cx="15" cy="-16" rx="5" ry="3" fill="{COLORS['soft_pink']}" opacity="0.5" />
    <!-- spikes -->
    <circle cx="-6" cy="-38" r="4" fill="{COLORS['dusty_purple']}" />
    <circle cx="6" cy="-38" r="4" fill="{COLORS['dusty_purple']}" />
    <circle cx="0" cy="-40" r="3.5" fill="{COLORS['lavender']}" />
    <!-- tiny arms -->
    <ellipse cx="-25" cy="5" rx="8" ry="5" fill="{COLORS['mint_green']}" stroke="{COLORS['deep_purple']}" stroke-width="1" transform="rotate(-20 -25 5)" />
    <ellipse cx="25" cy="5" rx="8" ry="5" fill="{COLORS['mint_green']}" stroke="{COLORS['deep_purple']}" stroke-width="1" transform="rotate(20 25 5)" />
    <!-- legs -->
    <ellipse cx="-12" cy="32" rx="8" ry="5" fill="{COLORS['mint_green']}" stroke="{COLORS['deep_purple']}" stroke-width="1" />
    <ellipse cx="12" cy="32" rx="8" ry="5" fill="{COLORS['mint_green']}" stroke="{COLORS['deep_purple']}" stroke-width="1" />
    <!-- tail -->
    <path d="M28,15 Q42,10 38,0" fill="none" stroke="{COLORS['mint_green']}" stroke-width="8" stroke-linecap="round" />
    <path d="M28,15 Q42,10 38,0" fill="none" stroke="{COLORS['deep_purple']}" stroke-width="1.5" stroke-linecap="round" />
    <!-- sparkle -->
    <text x="38" y="-30" font-size="14" text-anchor="middle">🌟</text>
  </g>"""


def _draw_kaiju(cx: float, cy: float) -> str:
    """Draw a full-size cute kaiju dinosaur."""
    return f"""
  <g transform="translate({cx},{cy})">
    <!-- body -->
    <ellipse cx="0" cy="8" rx="35" ry="28" fill="{COLORS['mint_green']}" />
    <ellipse cx="0" cy="8" rx="35" ry="28" fill="none" stroke="{COLORS['deep_purple']}" stroke-width="1.8" />
    <!-- tummy -->
    <ellipse cx="0" cy="12" rx="22" ry="18" fill="{COLORS['soft_mint']}" opacity="0.5" />
    <!-- head -->
    <ellipse cx="0" cy="-26" rx="26" ry="22" fill="{COLORS['mint_green']}" />
    <ellipse cx="0" cy="-26" rx="26" ry="22" fill="none" stroke="{COLORS['deep_purple']}" stroke-width="1.8" />
    <!-- eyes -->
    <circle cx="-8" cy="-28" r="6" fill="{COLORS['dark_bg']}" />
    <circle cx="8" cy="-28" r="6" fill="{COLORS['dark_bg']}" />
    <circle cx="-6" cy="-30" r="2.5" fill="{COLORS['white']}" />
    <circle cx="10" cy="-30" r="2.5" fill="{COLORS['white']}" />
    <!-- nostrils -->
    <circle cx="-4" cy="-16" r="1.5" fill="{COLORS['deep_purple']}" />
    <circle cx="4" cy="-16" r="1.5" fill="{COLORS['deep_purple']}" />
    <!-- mouth smile -->
    <path d="M-8,-11 Q0,-5 8,-11" fill="none" stroke="{COLORS['deep_purple']}" stroke-width="1.5" stroke-linecap="round" />
    <!-- blush -->
    <ellipse cx="-18" cy="-20" rx="6" ry="3.5" fill="{COLORS['soft_pink']}" opacity="0.5" />
    <ellipse cx="18" cy="-20" rx="6" ry="3.5" fill="{COLORS['soft_pink']}" opacity="0.5" />
    <!-- back spikes -->
    <path d="M-10,-48 L-6,-42 L-2,-50 L2,-42 L6,-48 L10,-42" fill="{COLORS['dusty_purple']}" stroke="{COLORS['deep_purple']}" stroke-width="1" />
    <!-- arms -->
    <path d="M-32,0 Q-42,-5 -40,-12" fill="none" stroke="{COLORS['mint_green']}" stroke-width="10" stroke-linecap="round" />
    <path d="M-32,0 Q-42,-5 -40,-12" fill="none" stroke="{COLORS['deep_purple']}" stroke-width="1.5" stroke-linecap="round" />
    <path d="M32,0 Q42,-5 40,-12" fill="none" stroke="{COLORS['mint_green']}" stroke-width="10" stroke-linecap="round" />
    <path d="M32,0 Q42,-5 40,-12" fill="none" stroke="{COLORS['deep_purple']}" stroke-width="1.5" stroke-linecap="round" />
    <!-- legs -->
    <ellipse cx="-14" cy="38" rx="10" ry="6" fill="{COLORS['mint_green']}" stroke="{COLORS['deep_purple']}" stroke-width="1.5" />
    <ellipse cx="14" cy="38" rx="10" ry="6" fill="{COLORS['mint_green']}" stroke="{COLORS['deep_purple']}" stroke-width="1.5" />
    <!-- tail -->
    <path d="M35,12 Q52,5 55,-8 Q58,-18 50,-22" fill="none" stroke="{COLORS['mint_green']}" stroke-width="12" stroke-linecap="round" />
    <path d="M35,12 Q52,5 55,-8 Q58,-18 50,-22" fill="none" stroke="{COLORS['deep_purple']}" stroke-width="1.8" stroke-linecap="round" />
    <!-- sparkle -->
    <text x="-42" y="-40" font-size="14" text-anchor="middle">💫</text>
    <text x="50" y="-35" font-size="12" text-anchor="middle">✨</text>
  </g>"""


def _draw_king(cx: float, cy: float) -> str:
    """Draw the king kaiju with a crown."""
    base = _draw_kaiju(cx, cy)
    crown = f"""
  <g transform="translate({cx},{cy})">
    <!-- crown -->
    <path d="M-18,-56 L-14,-46 L-6,-52 L0,-44 L6,-52 L14,-46 L18,-56 Z" fill="{COLORS['gold']}" stroke="{COLORS['deep_purple']}" stroke-width="1.2" />
    <circle cx="-10" cy="-52" r="2" fill="{COLORS['soft_pink']}" />
    <circle cx="0" cy="-49" r="2" fill="{COLORS['mint_green']}" />
    <circle cx="10" cy="-52" r="2" fill="{COLORS['dusty_purple']}" />
    <!-- royal sparkles -->
    <text x="-50" y="-50" font-size="10" text-anchor="middle">👑</text>
    <text x="55" y="-45" font-size="16" text-anchor="middle">🌈</text>
  </g>"""
    return base + crown


DRAW_FNS = {
    "Egg": _draw_egg,
    "Baby": _draw_baby,
    "Junior": _draw_junior,
    "Kaiju": _draw_kaiju,
    "King": _draw_king,
}


# ─── Main Generator ────────────────────────────────────────

def generate_kaiju_svg(data: dict) -> str:
    """Generate the kaiju growth card SVG."""

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

    extra_style = f"""
    @keyframes pulse {{
      0%, 100% {{ transform: scale(1); }}
      50% {{ transform: scale(1.02); }}
    }}
    @keyframes xpGrow {{
      from {{ width: 0; }}
      to {{ width: {progress * 300}px; }}
    }}
    @keyframes float {{
      0%, 100% {{ transform: translateY(0); }}
      50% {{ transform: translateY(-4px); }}
    }}
    .kaiju-art {{ animation: float 3s ease-in-out infinite; }}
    """

    lines = [svg_header(CARD_W, CARD_H, extra_defs=extra_defs, extra_style=extra_style)]

    # Card background
    lines.append(rounded_rect(0, 0, CARD_W, CARD_H, rx=16, fill=COLORS["dark_bg"]))
    lines.append(rounded_rect(0, 0, CARD_W, CARD_H, rx=16, fill="none", stroke="url(#cardBorderGrad)", stroke_width=1.5))

    # Title
    lines.append(text_element(CARD_W / 2, 30, f"🦖  {stage[3]}", size=17, fill=COLORS["lavender"], anchor="middle", weight="700"))

    # Level badge
    lv_x = CARD_W / 2
    lines.append(rounded_rect(lv_x - 30, 38, 60, 22, rx=11, fill=COLORS["card_bg"], stroke="url(#purpleMintGrad)", stroke_width=1.2))
    lines.append(text_element(lv_x, 54, f"Lv. {level}", size=11, fill=COLORS["mint_green"], anchor="middle", weight="700"))

    # Kaiju art (centered)
    art_cx = CARD_W / 2
    art_cy = 150
    draw_fn = DRAW_FNS.get(stage[1], _draw_egg)
    lines.append(f'  <g class="kaiju-art">')
    lines.append(draw_fn(art_cx, art_cy))
    lines.append("  </g>")

    # Decorative elements
    lines.append(f'  <circle cx="40" cy="90" r="3" fill="{COLORS["dusty_purple"]}" opacity="0.3" />')
    lines.append(f'  <circle cx="380" cy="100" r="2.5" fill="{COLORS["mint_green"]}" opacity="0.3" />')
    lines.append(f'  <circle cx="60" cy="250" r="2" fill="{COLORS["soft_pink"]}" opacity="0.3" />')
    lines.append(f'  <circle cx="360" cy="240" r="3.5" fill="{COLORS["lavender"]}" opacity="0.2" />')

    # XP Bar section
    bar_y = 250
    bar_x = 60
    bar_w = 300
    bar_h = 14

    # XP label
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

    # Bar glow
    lines.append(f'  <rect x="{bar_x}" y="{bar_y}" width="{fill_w}" height="{bar_h / 2}" rx="7" fill="{COLORS["white"]}" opacity="0.1" clip-path="url(#xpClip)" />')

    # Commit counter
    lines.append(text_element(CARD_W / 2, bar_y + bar_h + 22, f"🔥 {commits} total commits", size=12, fill=COLORS["text_light"], anchor="middle", weight="600"))

    # Bottom decorative line
    lines.append(f'  <line x1="60" y1="{CARD_H - 15}" x2="{CARD_W - 60}" y2="{CARD_H - 15}" stroke="url(#purpleMintGradH)" stroke-width="1" stroke-opacity="0.2" />')

    lines.append(svg_footer())
    return "\n".join(lines)
