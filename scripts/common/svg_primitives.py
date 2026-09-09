"""
Theme-agnostic SVG building blocks shared by every theme package.
Nothing here knows about colors or fonts - that's each theme_*.py's job.
"""


def svg_open(width: int, height: int, extra_defs: str = "", extra_style: str = "") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    {extra_defs}
  </defs>
  <style>
    {extra_style}
  </style>'''


def svg_close() -> str:
    return "</svg>"


def rect(x: float, y: float, w: float, h: float, rx: float = 0, fill: str = "none",
         stroke: str | None = None, stroke_width: float = 1, opacity: float = 1, extra: str = "") -> str:
    stroke_attr = f' stroke="{stroke}" stroke-width="{stroke_width}"' if stroke else ""
    opacity_attr = f' opacity="{opacity}"' if opacity != 1 else ""
    return f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{stroke_attr}{opacity_attr} {extra}/>'


def text_element(x: float, y: float, content: str, size: float, fill: str, family: str,
                  anchor: str = "start", weight: str = "normal", style: str = "normal",
                  letter_spacing: float | None = None, extra: str = "") -> str:
    ls_attr = f' letter-spacing="{letter_spacing}"' if letter_spacing is not None else ""
    style_attr = f' font-style="{style}"' if style != "normal" else ""
    return (f'  <text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-family="{family}"{style_attr}{ls_attr} {extra}>{content}</text>')
