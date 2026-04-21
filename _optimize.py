from PIL import Image
import os

SRC = "/Users/yoshihashiryou/meguriwa_test/MEGURIWA_OS/002_Clients/13_Nomura/Assets"
DST = "/Users/yoshihashiryou/meguriwa_test/nomunomono-mock/images"

def optimize_image(src_path, dst_path, max_width=1000, quality=82):
    img = Image.open(src_path)
    if img.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")
    w, h = img.size
    if w > max_width:
        ratio = max_width / w
        img = img.resize((max_width, int(h * ratio)), Image.LANCZOS)
    img.save(dst_path, "JPEG", quality=quality, optimize=True)
    return os.path.getsize(dst_path) / 1024

targets = [
    ("Kiraさん/だるまコインケース/ダルマ_赤.png", "darma_red.jpg"),
    ("Kiraさん/だるまコインケース/ダルマ_白.png", "darma_white.jpg"),
    ("Kiraさん/だるまコインケース/ダルマ_金.png", "darma_gold.jpg"),
    ("Kiraさん/だるまコインケース/ダルマ_ラベンダー2025年限定カラー.png", "darma_lavender.jpg"),
    ("Kiraさん/富士山コインケース/富士山.png", "fuji_blue.jpg"),
    ("Kiraさん/富士山コインケース/赤富士.jpg", "fuji_red.jpg"),
    ("Kiraさん/まねきねこポーチ/まねきねこ.png", "manekineko.jpg"),
    ("Kiraさん/おにぎりポーチ/おにぎり.png", "onigiri.jpg"),
    ("Kiraさん/くじらペンケース/くじらペンケース (3).webp", "whale_pen.jpg"),
    ("Kiraさん/午_干支シリーズ/IMG_1923.jpg", "eto_uma.jpg"),
    ("photo/1.jpg", "factory_01.jpg"),
    ("photo/2.jpg", "factory_02.jpg"),
    ("photo/nomura_web_20241225_5.jpg", "factory_03.jpg"),
]

for src_rel, out_name in targets:
    src = os.path.join(SRC, src_rel)
    dst = os.path.join(DST, out_name)
    try:
        size_kb = optimize_image(src, dst)
        print(f"  {out_name}: {size_kb:.0f} KB")
    except Exception as e:
        print(f"  ERROR {out_name}: {e}")

print("\n=== DONE ===")
print(os.listdir(DST))
