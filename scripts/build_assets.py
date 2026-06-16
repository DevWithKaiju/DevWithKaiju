import base64
import json

files = {
    'Egg': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_egg_1781601645385.png',
    'Baby': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_baby_1781601655443.png',
    'Junior': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_junior_1781601665560.png',
    'Kaiju': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_adult_1781601676347.png',
    'King': r'C:\Users\liong\.gemini\antigravity-ide\brain\bd9c0859-b0b0-4574-a135-69020797d543\kaiju_king_1781601687044.png'
}

out = 'ASSETS = {\n'
for k, v in files.items():
    with open(v, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    out += f'    "{k}": "data:image/png;base64,{b64}",\n'
out += '}\n'

with open(r'c:\Users\liong\OneDrive\ドキュメント\DevWithKaiju\scripts\kaiju_assets.py', 'w') as f:
    f.write(out)
