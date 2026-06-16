import base64
import json

files = {
    'Egg': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_egg_v2_1781606467928.png',
    'Baby': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_baby_v2_1781606478959.png',
    'Junior': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_junior_v2_1781606489879.png',
    'Kaiju': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_adult_v2_1781606499980.png',
    'King': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_king_v2_1781606509690.png'
}

out = 'ASSETS = {\n'
for k, v in files.items():
    with open(v, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    out += f'    "{k}": "data:image/png;base64,{b64}",\n'
out += '}\n'

with open(r'c:\Users\liong\OneDrive\ドキュメント\DevWithKaiju\scripts\kaiju_assets.py', 'w') as f:
    f.write(out)
