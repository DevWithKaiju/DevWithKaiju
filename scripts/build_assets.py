import os
from PIL import Image

files = {
    'egg': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_egg_v2_1781606467928.png',
    'baby': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_baby_v2_1781606478959.png',
    'junior': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_junior_v4_1781620547955.png',
    'adult': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_adult_v2_1781606499980.png',
    'king': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_king_v2_1781606509690.png'
}

out_dir = r'c:\Users\liong\OneDrive\ドキュメント\DevWithKaiju\images'
os.makedirs(out_dir, exist_ok=True)

for stage_name, filepath in files.items():
    img = Image.open(filepath).convert('RGBA')
    bg = Image.new('RGBA', img.size, (255, 255, 255, 255))
    bg.paste(img, mask=img)
    
    w, h = bg.size
    new_w, new_h = int(w * 0.75), int(h * 0.75)
    shrunk = bg.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    final_img = Image.new('RGB', (w, h), (255, 255, 255))
    final_img.paste(shrunk, ((w - new_w)//2, (h - new_h)//2), shrunk if shrunk.mode == 'RGBA' else None)
    
    out_path = os.path.join(out_dir, f'stage_{stage_name}.png')
    final_img.save(out_path, format='PNG')
    print(f"Saved {out_path}")

