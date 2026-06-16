import base64
import os
from PIL import Image

files = {
    'Egg': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_egg_v2_1781606467928.png',
    'Baby': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_baby_v2_1781606478959.png',
    'Junior': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_junior_v3_1781620216888.png',
    'Kaiju': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_adult_v2_1781606499980.png',
    'King': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_king_v2_1781606509690.png'
}

out = 'ASSETS = {\n'
for k, v in files.items():
    img = Image.open(v).convert('RGBA')
    bg = Image.new('RGBA', img.size, (255, 255, 255, 255))
    bg.paste(img, mask=img)
    
    w, h = bg.size
    new_w, new_h = int(w * 0.75), int(h * 0.75)
    shrunk = bg.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    final_img = Image.new('RGB', (w, h), (255, 255, 255))
    final_img.paste(shrunk, ((w - new_w)//2, (h - new_h)//2), shrunk if shrunk.mode == 'RGBA' else None)
    
    import io
    buf = io.BytesIO()
    final_img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    out += f'    "{k}": "data:image/png;base64,{b64}",\n'
out += '}\n'

with open(r'c:\Users\liong\OneDrive\ドキュメント\DevWithKaiju\scripts\kaiju_assets.py', 'w', encoding='utf-8') as f:
    f.write(out)
