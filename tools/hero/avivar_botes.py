"""Aviva el color de los 8 botes del header (assets/hero.jpg) para acercarlo al de los renders sueltos.
Solo toca los botes: una máscara limita el retoque a las zonas con color de la franja de botes,
así el fondo de seda, el cielo y el titular no cambian.

Uso:  python3 tools/hero/avivar_botes.py
      Parte siempre de tools/hero/hero_original.jpg (sin retocar) y escribe assets/hero.jpg.
      No lo pases sobre assets/hero.jpg: el retoque se aplicaría dos veces.
"""
import os, sys
from PIL import Image, ImageEnhance, ImageFilter, ImageChops, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "hero_original.jpg")
dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "assets", "hero.jpg")

img = Image.open(src).convert("RGB")
W, H = img.size
k = W / 2400  # coordenadas pensadas para el header de 2400 px

# Centro de cada bote (de izquierda a derecha) y cuánto avivarlo: (saturación, contraste).
# Medido frente a los renders sueltos de assets/productos: Original, Nenuco y Pieles eran los más apagados.
BOTES = [
  (309,  "cerezo",   1.35, 1.12), (559,  "orquidea", 1.40, 1.12), (810,  "original", 1.90, 1.14),
  (1062, "azul",     1.52, 1.12), (1310, "medit",    1.25, 1.10), (1563, "nenuco",   1.90, 1.14),
  (1813, "delicias", 1.32, 1.12), (2060, "pieles",   1.75, 1.10),
]
Y0, Y1 = 500, 1260  # franja vertical de los botes y su reflejo

# Máscara 1: silueta de cada bote (cuerpo + hombros), para incluir también las zonas pálidas
# (Original, Pieles) que tienen la misma saturación que el fondo. El tapón blanco queda fuera.
def silueta(cx):
  m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
  d.rounded_rectangle(((cx-101)*k, 640*k, (cx+101)*k, 1102*k), radius=34*k, fill=255)  # cuerpo
  d.rounded_rectangle(((cx-86)*k, 606*k, (cx+86)*k, 680*k), radius=30*k, fill=255)     # hombros
  return m.filter(ImageFilter.GaussianBlur(3*k))

# Máscara 2: zonas con color de la franja (flores a los pies y reflejos); el fondo, poco saturado, queda fuera.
sat = img.convert("HSV").getchannel("S").point(lambda s: 0 if s < 26 else min(255, int((s - 26) * 255 / 34)))

out = img.copy()
for i, (cx, nombre, ks, kc) in enumerate(BOTES):
  # columna del bote: desde el punto medio con el vecino izquierdo hasta el del derecho
  left = (BOTES[i-1][0] + cx) / 2 if i else cx - 150
  right = (BOTES[i+1][0] + cx) / 2 if i < len(BOTES) - 1 else cx + 150
  band = Image.new("L", (W, H), 0)
  ImageDraw.Draw(band).rectangle((left*k, Y0*k, right*k, Y1*k), fill=255)
  band = band.filter(ImageFilter.GaussianBlur(18*k))  # bordes suaves entre columnas y arriba/abajo
  mask = ImageChops.lighter(silueta(cx), ImageChops.multiply(band, sat).filter(ImageFilter.GaussianBlur(2.5*k)))
  viva = ImageEnhance.Contrast(ImageEnhance.Color(img).enhance(ks)).enhance(kc)
  out = Image.composite(viva, out, mask)

if os.environ.get("MASCARA"):  # depuración: guarda la silueta de los botes
  full = Image.new("L", (W, H), 0)
  for cx, *_ in BOTES: full = ImageChops.lighter(full, silueta(cx))
  full.save(os.environ["MASCARA"])

out.save(dst, quality=84, optimize=True, progressive=True)
print("OK", dst, out.size)
