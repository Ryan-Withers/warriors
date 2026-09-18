from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Rebuilds every icon and the share card from apple-touch-icon.png.
# Run after replacing that file:  python3 tools/make-images.py
ROOT = Path(__file__).resolve().parent.parent

MAROON_DEEP = (94, 24, 36)
MAROON      = (139, 41, 55)
GOLD        = (238, 181, 66)
CHALK       = (255, 248, 236)
CHALK_SOFT  = (242, 210, 201)

F = "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf"
def font(style, size): return ImageFont.truetype(F % style, size)

logo = Image.open(ROOT / "apple-touch-icon.png").convert("RGB")

def stripes(img, period=80, width=40, alpha=0.08):
    """The same 135deg gold hatch the page uses on its end zones."""
    w, h = img.size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    a = int(255 * alpha)
    for off in range(-h, w + h, period):
        d.line([(off, 0), (off + h, h)], fill=GOLD + (a,), width=width)
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

def centred(d, y, text, f, fill):
    l, t, r, b = d.textbbox((0, 0), text, font=f)
    d.text(((1200 - (r - l)) / 2 - l, y), text, font=f, fill=fill)
    return b - t

# ---------- share card (og:image), 1200x630 ----------
card = Image.new("RGB", (1200, 630), MAROON_DEEP)
card = stripes(card)
d = ImageDraw.Draw(card)

# The logo tile's own maroon reads as a box against the deeper card, so cut the
# round badge out of it. Radius measured at 78/90 of the 180px tile; supersample
# the mask so the edge stays smooth after scaling.
S, R = 8, 190
m = Image.new("L", (180 * S, 180 * S), 0)
ImageDraw.Draw(m).ellipse([(90 - 78.5) * S, (90 - 78.5) * S,
                           (90 + 78.5) * S, (90 + 78.5) * S], fill=255)
badge = logo.resize((R, R), Image.LANCZOS)
badge.putalpha(m.resize((R, R), Image.LANCZOS))
card.paste(badge, ((1200 - R) // 2, 74), badge)

centred(d, 300, "WARRIORS", font("Bold", 132), CHALK)
centred(d, 452, "AFV 2026 Men's draw", font("Bold", 46), GOLD)
centred(d, 516, "Division 1  ·  Arrival times, grounds and calendar", font("Regular", 30), CHALK_SOFT)

d.rectangle([0, 630 - 14, 1200, 630], fill=GOLD)   # goal line, as on the page
card.save(ROOT / "share-card.png", optimize=True)

# ---------- manifest icons ----------
logo.resize((192, 192), Image.LANCZOS).save(ROOT / "icon-192.png", optimize=True)
logo.resize((512, 512), Image.LANCZOS).save(ROOT / "icon-512.png", optimize=True)

# Maskable: Android crops to a circle, so the badge sits at 60% on a solid tile.
mask = Image.new("RGB", (512, 512), MAROON)
inner = logo.resize((307, 307), Image.LANCZOS)
mask.paste(inner, ((512 - 307) // 2, (512 - 307) // 2))
mask.save(ROOT / "icon-maskable-512.png", optimize=True)
