"""Genera los fotogramas de la animación de presentación de un bote Flor.
Uso: python3 frames.py <clave> <carpeta_salida> [segundos] [fps]
Normalmente se lanza desde generar.sh, que además codifica el MP4.
"""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # carpeta de la landing
W, H = 720, 900

# Color de cada fragancia (igual que en la landing) y elementos que la acompañan
PROD = {
  "azul":     ("#2F55C9", "petal", ["#5B8DEF", "#3E6FD9", "#9EC0FF", "#FFFFFF"]),
  "nenuco":   ("#3FA9A0", "petal", ["#7FD3C9", "#B9EBE4", "#FFFFFF", "#5FBFB4"]),
  "original": ("#3D86D6", "fluff", ["#FFFFFF", "#EAF3FF", "#FFFFFF"]),
  "medit":    ("#1F9AB2", "petal", ["#B455C9", "#D07BDF", "#9A3FB5", "#F5D33A"]),
  "cerezo":   ("#D63F72", "petal", ["#F7B7C9", "#F59AB5", "#FFFFFF", "#E5578A"]),
  "delicias": ("#E8734A", "petal", ["#F7A26B", "#FFD2A8", "#FFFFFF", "#F28C5B"]),
  "pieles":   ("#D9958F", "petal", ["#F6CFCB", "#FBE3E0", "#FFFFFF", "#EBB3AE"]),
  "orquidea": ("#C9A13B", "petal", ["#FFFFFF", "#FFF6D8", "#F3E3A6", "#FFFFFF"]),
}

def hex2rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def mix(c, w, f): return tuple(round(c[i]*f + w[i]*(1-f)) for i in range(3))

def comp(dst, src, x, y):
  """alpha_composite que admite posiciones negativas o fuera del lienzo."""
  x, y = int(x), int(y)
  l, t = max(0, -x), max(0, -y)
  r, b = min(src.width, dst.width - x), min(src.height, dst.height - y)
  if r <= l or b <= t: return
  dst.alpha_composite(src.crop((l, t, r, b)) if (l or t or r < src.width or b < src.height) else src, (x + l, y + t))

def background(color):
  """Degradado vertical del color de la fragancia + halo blanco detrás del bote."""
  c = hex2rgb(color); white = (255, 255, 255)
  top, bot = mix(c, white, .12), mix(c, white, .30)
  bg = Image.new("RGB", (1, H))
  for y in range(H):
    f = y/(H-1); bg.putpixel((0, y), tuple(round(top[i]*(1-f)+bot[i]*f) for i in range(3)))
  bg = bg.resize((W, H)).convert("RGBA")
  glow = Image.new("RGBA", (W, H), (255, 255, 255, 0))
  d = ImageDraw.Draw(glow)
  for r in range(380, 0, -6):  # círculos concéntricos -> radial suave
    a = int(255 * (1 - r/380) ** 1.3)
    d.ellipse((W/2-r, 330-r, W/2+r, 330+r), fill=(255, 255, 255, a))
  glow = glow.filter(ImageFilter.GaussianBlur(28))
  return bg, Image.alpha_composite(bg, glow)

def petal_mask(L, Wd):
  """Silueta de pétalo: estrecho en la base, redondeado y ancho hacia la punta."""
  m = Image.new("L", (Wd, L), 0)
  pts_r, pts_l = [], []
  for i in range(41):
    u = i/40
    hw = (Wd/2) * (math.sin(math.pi*min(1, u*1.08))**0.75) * (0.55 + 0.45*u)
    pts_r.append((Wd/2 + hw, L*(1-u))); pts_l.append((Wd/2 - hw, L*(1-u)))
  ImageDraw.Draw(m).polygon(pts_r + pts_l[::-1], fill=255)
  return m

def petal_img(color, L):
  Wd = int(L*.62)
  c = hex2rgb(color); light = mix(c, (255, 255, 255), .45); dark = mix(c, (20, 25, 60), .82)
  g = Image.new("RGBA", (1, L))
  for y in range(L):  # punta clara -> base más intensa
    f = y/(L-1); g.putpixel((0, y), tuple(round(light[i]*(1-f) + dark[i]*f) for i in range(3)) + (255,))
  g = g.resize((Wd, L))
  vein = ImageDraw.Draw(g); vein.line((Wd/2, L*.25, Wd/2, L*.95), fill=light + (110,), width=max(1, L//40))
  g.putalpha(petal_mask(L, Wd))
  return g

def petal_sprite(color, size, kind, blur):
  s = size*3
  im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
  c = hex2rgb(color)
  if kind == "fluff":  # semillas de diente de león
    for i in range(14):
      a = i/14*2*math.pi
      d.line((s/2, s/2, s/2+math.cos(a)*s*.42, s/2+math.sin(a)*s*.42), fill=c+(210,), width=max(2, s//45))
      d.ellipse((s/2+math.cos(a)*s*.42-s*.02, s/2+math.sin(a)*s*.42-s*.02, s/2+math.cos(a)*s*.42+s*.02, s/2+math.sin(a)*s*.42+s*.02), fill=c+(230,))
    d.ellipse((s*.45, s*.45, s*.55, s*.55), fill=(235, 225, 190, 255))
  elif kind == "flower":  # flor de 5 pétalos
    p = petal_img(color, int(s*.46))
    for k in range(5):
      # cada pétalo nace en el centro y se gira 72° alrededor de él
      tmp = Image.new("RGBA", (s, s), (0, 0, 0, 0)); tmp.alpha_composite(p, (int(s/2 - p.width/2), int(s/2 - p.height)))
      im.alpha_composite(tmp.rotate(k*72, resample=Image.BICUBIC, center=(s/2, s/2)))
    d.ellipse((s*.43, s*.43, s*.57, s*.57), fill=(245, 205, 80, 255))
  else:  # pétalo suelto
    p = petal_img(color, int(s*.8))
    im.alpha_composite(p, (int(s/2 - p.width/2), int(s/2 - p.height/2)))
  im = im.resize((size, size), Image.LANCZOS)
  return im.filter(ImageFilter.GaussianBlur(blur)) if blur else im

def make_petals(kind, palette, rnd, n, front, T):
  """Cada pétalo vive un ciclo de T segundos (nace, cae y se desvanece) con un desfase propio.
  Todos los movimientos dan vueltas completas en T, así el vídeo enlaza sin cortes."""
  ps = []
  for _ in range(n):
    size = rnd.randint(95, 140) if front else rnd.randint(40, 74)
    color = rnd.choice(palette)
    k = kind
    if kind == "petal" and rnd.random() < .3: k = "flower"; size = int(size*1.35)
    ps.append(dict(
      spr=petal_sprite(color, size, k, 3.2 if front else 0.8),
      off=rnd.uniform(0, T),
      x0=rnd.uniform(-20, W+20),
      y0=rnd.uniform(-160, H*.3) if front else rnd.uniform(-90, H*.45),
      v=rnd.uniform(70, 110) if front else rnd.uniform(40, 75),
      amp=rnd.uniform(18, 46), kx=rnd.choice([1, 2]), ph=rnd.uniform(0, 6.28),
      rot=rnd.uniform(0, 360), kr=rnd.choice([-1, 1]),
      flip=rnd.uniform(0, 6.28), kf=rnd.choice([2, 3, 4]),
      alpha=rnd.uniform(.75, .95) if front else rnd.uniform(.55, .85)))
  return ps

def smooth(x): x = max(0, min(1, x)); return x*x*(3 - 2*x)

def draw_petals(frame, ps, t, T):
  for p in ps:
    age = (t + p["off"]) % T
    u = age/T
    env = smooth(u/.18) * smooth((1-u)/.22)  # aparece y se desvanece dentro del ciclo
    if env <= .01: continue
    y = p["y0"] + p["v"]*age
    x = p["x0"] + p["amp"]*math.sin(2*math.pi*p["kx"]*t/T + p["ph"])
    spr = p["spr"]
    sx = max(.25, abs(math.cos(p["flip"] + 2*math.pi*p["kf"]*t/T)))  # giro 3D simulado
    w = max(2, int(spr.width*sx))
    s2 = spr.resize((w, spr.height), Image.BILINEAR).rotate(p["rot"] + 360*p["kr"]*t/T, expand=True, resample=Image.BICUBIC)
    a = p["alpha"]*env
    s2.putalpha(s2.getchannel("A").point(lambda v, a=a: int(v*a)))
    comp(frame, s2, x - s2.width/2, y - s2.height/2)

def main():
  key, outdir = sys.argv[1], sys.argv[2]
  secs = float(sys.argv[3]) if len(sys.argv) > 3 else 8
  fps = int(sys.argv[4]) if len(sys.argv) > 4 else 30
  color, kind, palette = PROD[key]
  os.makedirs(outdir, exist_ok=True)
  rnd = random.Random(key)

  bg0, bg1 = background(color)
  bottle = Image.open(f"{ROOT}/assets/productos/{key}.webp").convert("RGBA")
  BH = 600
  bottle = bottle.resize((round(bottle.width*BH/bottle.height), BH), Image.LANCZOS)
  bw = bottle.width
  base_top = 112  # posición final del bote

  # sombra difuminada bajo el bote
  sh = Image.new("RGBA", (int(bw*1.5), 90), (0, 0, 0, 0))
  ImageDraw.Draw(sh).ellipse((sh.width*.12, 30, sh.width*.88, 62), fill=(27, 35, 80, 120))
  sh = sh.filter(ImageFilter.GaussianBlur(14))

  # banda de brillo para el destello sobre el bote
  band = Image.new("RGBA", (180, BH*2), (255, 255, 255, 0))
  for x in range(180):
    a = int(120 * math.exp(-((x-90)/38)**2))
    ImageDraw.Draw(band).line((x, 0, x, BH*2), fill=(255, 255, 255, a))
  band = band.rotate(-22, expand=True, resample=Image.BICUBIC)
  bottle_alpha = bottle.getchannel("A")

  T = secs
  back = make_petals(kind, palette, rnd, 20, False, T)
  front = make_petals(kind, palette, rnd, 6, True, T)

  N = int(round(T*fps))
  for i in range(N + 1):  # N+1 fotogramas: el último es idéntico al primero
    t = (i % N)/fps
    cyc = (1 - math.cos(2*math.pi*t/T))/2
    frame = Image.blend(bg0, bg1, .85 + .15*cyc)  # el halo "respira"
    draw_petals(frame, back, t, T)

    # flotación suave: dos subidas y bajadas por ciclo
    float_y = -10*(1 - math.cos(2*math.pi*2*t/T))/2
    y = base_top + float_y

    shs = sh.resize((max(1, int(sh.width*(1 + float_y/300))), sh.height))
    comp(frame, shs, W/2 - shs.width/2, base_top + BH - 38)

    b = bottle
    # destello diagonal una vez por ciclo (de 1,0 s a 2,1 s)
    st = (t-1.0)/1.1
    if 0 <= st <= 1:
      layer = Image.new("RGBA", b.size, (0, 0, 0, 0))
      bx = int(-band.width + st*(bw + band.width*1.2))
      comp(layer, band, bx, -BH//2)
      layer.putalpha(ImageChops.multiply(layer.getchannel("A"), bottle_alpha))
      b = Image.alpha_composite(b, layer)
    comp(frame, b, W/2 - bw/2, y)

    draw_petals(frame, front, t, T)
    out = frame.convert("RGB")
    out.save(f"{outdir}/f{i:04d}.png", compress_level=1)
    if i == 0: out.save(f"{outdir}/poster.jpg", quality=86)
  print(key, N + 1, "frames")

main()
