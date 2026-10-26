"""Genera las 15 ilustraciones suaves de fondo de las opciones del test (assets/opciones/<palabra>.svg).
Van encima del degradado de color de cada recuadro, en blancos y tonos translúcidos.
Uso: python3 tools/opciones/generar_svg.py
"""
import math, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "assets", "opciones")
W, H = 400, 300

def svg(body, defs=""):
  return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">
<defs>
<filter id="b1" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.2"/></filter>
<filter id="b3" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="b8" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
{defs}
</defs>
{body}
</svg>
'''

def petal(cx, cy, L, w, ang, fill, op, filt="b1"):
  # pétalo: estrecho en la base (cx,cy), redondeado en la punta
  return (f'<path transform="translate({cx} {cy}) rotate({ang})" d="M0 0 C {w*.9} {-L*.25} {w} {-L*.8} 0 {-L} '
          f'C {-w} {-L*.8} {-w*.9} {-L*.25} 0 0Z" fill="{fill}" opacity="{op}" filter="url(#{filt})"/>')

def flower(cx, cy, r, n, fill, op, center="#FFE7A3", rot=0, filt="b1"):
  s = "".join(petal(cx, cy, r, r*.55, rot + i*360/n, fill, op, filt) for i in range(n))
  return s + f'<circle cx="{cx}" cy="{cy}" r="{r*.16}" fill="{center}" opacity="{min(1, op+.2)}"/>'

def sparkle(cx, cy, r, op):
  return (f'<path transform="translate({cx} {cy})" d="M0 {-r} C {r*.12} {-r*.12} {r*.12} {-r*.12} {r} 0 C {r*.12} {r*.12} {r*.12} {r*.12} 0 {r} '
          f'C {-r*.12} {r*.12} {-r*.12} {r*.12} {-r} 0 C {-r*.12} {-r*.12} {-r*.12} {-r*.12} 0 {-r}Z" fill="#fff" opacity="{op}"/>')

def leaf(cx, cy, L, w, ang, fill, op, vein="#fff"):
  return (f'<g transform="translate({cx} {cy}) rotate({ang})" opacity="{op}">'
          f'<path d="M0 0 C {w} {-L*.3} {w*.8} {-L*.8} 0 {-L} C {-w*.8} {-L*.8} {-w} {-L*.3} 0 0Z" fill="{fill}"/>'
          f'<path d="M0 -4 L0 {-L*.92}" stroke="{vein}" stroke-width="1.6" stroke-linecap="round" opacity=".55"/></g>')

def cloud(cx, cy, s, op):
  c = [(0, 0, 34), (-36, 10, 24), (38, 8, 27), (-12, -18, 26), (16, -22, 22)]
  body = "".join(f'<circle cx="{cx+x*s}" cy="{cy+y*s}" r="{r*s}"/>' for x, y, r in c)
  return f'<g fill="#fff" opacity="{op}" filter="url(#b3)">{body}<rect x="{cx-58*s}" y="{cy}" width="{116*s}" height="{30*s}" rx="{15*s}"/></g>'

ART = {}

# P1 · tipo de aroma
ART["aire"] = svg(
  cloud(250, 150, 1.25, .55) + cloud(110, 215, .8, .4) + cloud(330, 70, .6, .35) +
  "".join(f'<path d="M{x} {y} q 60 -26 120 0 t 120 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity="{o}" filter="url(#b1)"/>'
          for x, y, o in [(30, 110, .55), (70, 135, .4), (10, 250, .35)]))

ART["flor"] = svg(
  flower(125, 160, 72, 5, "#F6C6DD", .6, center="#FFE08A", rot=12) + flower(125, 160, 44, 5, "#fff", .45, center="#FFE08A", rot=48) +
  flower(300, 225, 40, 5, "#E7C9F0", .6, center="#FFE08A", rot=-20) + flower(330, 70, 22, 5, "#F6C6DD", .5) +
  petal(230, 90, 26, 14, 40, "#F6C6DD", .55) + petal(215, 255, 22, 12, -60, "#E7C9F0", .5) + petal(380, 150, 18, 10, 20, "#fff", .5))

ART["fruta"] = svg(
  f'<circle cx="230" cy="160" r="70" fill="#FFE2C8" opacity=".55" filter="url(#b3)"/>'
  f'<circle cx="205" cy="135" r="22" fill="#fff" opacity=".5" filter="url(#b8)"/>'
  f'<path d="M230 92 q 6 -16 2 -30" stroke="#8C5A3C" stroke-width="4" fill="none" stroke-linecap="round" opacity=".35"/>'
  + leaf(236, 92, 48, 20, 60, "#BFE3B4", .6) +
  "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#F7B3C2" opacity=".55" filter="url(#b1)"/><circle cx="{x-r*.3}" cy="{y-r*.3}" r="{r*.3}" fill="#fff" opacity=".6"/>'
          for x, y, r in [(110, 215, 20), (140, 235, 16), (95, 245, 14), (330, 230, 18), (355, 250, 13)]))

# P2 · cómo se siente
def cotton(cx, cy, r, op):
  """Bola de algodón: lóbulos blancos con una sombra lila suave debajo para que se distinga sobre fondos claros."""
  lobes = [(math.cos(a)*r*.55, math.sin(a)*r*.42) for a in [i*1.05 for i in range(6)]] + [(0, 0)]
  shade = "".join(f'<circle cx="{cx+x+4}" cy="{cy+y+6}" r="{r*.55}"/>' for x, y in lobes)
  body = "".join(f'<circle cx="{cx+x}" cy="{cy+y}" r="{r*.55}"/>' for x, y in lobes)
  return (f'<g opacity="{op}"><g fill="#C9A9D6" opacity=".45" filter="url(#b3)">{shade}</g>'
          f'<g fill="#fff" filter="url(#b1)">{body}</g></g>')

ART["suave"] = svg(
  cotton(115, 175, 62, .75) + cotton(285, 215, 44, .7) + cotton(320, 85, 28, .6) + cotton(205, 95, 20, .55) +
  '<path d="M20 275 C 120 245, 280 295, 390 255" stroke="#D9C0E2" stroke-width="10" fill="none" opacity=".5" stroke-linecap="round" filter="url(#b3)"/>')

def feather(cx, cy, L, ang, op):
  barbs = "".join(
    f'<path d="M0 {-t} q {14*(1-t/L)+6} {-6} {24*(1-t/L)+10} {-16}" stroke="#fff" stroke-width="1.6" fill="none" opacity=".75"/>'
    f'<path d="M0 {-t} q {-(14*(1-t/L)+6)} {-6} {-(24*(1-t/L)+10)} {-16}" stroke="#fff" stroke-width="1.6" fill="none" opacity=".75"/>'
    for t in range(12, int(L*.95), 7))
  return (f'<g transform="translate({cx} {cy}) rotate({ang})" opacity="{op}" filter="url(#b1)">'
          f'<path d="M0 {-L*.48} C 30 {-L*.6} 34 {-L*.9} 0 {-L} C -34 {-L*.9} -30 {-L*.6} 0 {-L*.48}Z" fill="#fff" opacity=".45"/>'
          f'{barbs}<path d="M0 10 L0 {-L}" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/></g>')

ART["ligera"] = svg(
  feather(250, 250, 200, 28, .7) + feather(95, 230, 110, -24, .5) +
  "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity="{o}" filter="url(#b1)"/>' for x, y, r, o in
          [(60, 70, 4, .5), (150, 50, 3, .45), (330, 60, 5, .5), (370, 140, 3, .4), (180, 120, 2.5, .4)]))

ART["estela"] = svg(
  '<path d="M30 260 C 120 230, 180 120, 330 70" stroke="#fff" stroke-width="18" fill="none" stroke-linecap="round" opacity=".18" filter="url(#b8)"/>'
  '<path d="M30 260 C 120 230, 180 120, 330 70" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-dasharray="2 10" opacity=".7"/>' +
  sparkle(330, 70, 26, .85) + sparkle(255, 112, 13, .6) + sparkle(180, 170, 9, .55) + sparkle(110, 230, 7, .5) +
  sparkle(70, 80, 8, .45) + sparkle(370, 160, 10, .5) +
  '<circle cx="330" cy="70" r="40" fill="#fff" opacity=".25" filter="url(#b8)"/>')

# P3 · ingredientes
def bud(cx, cy, r, op):
  return (f'<g opacity="{op}" filter="url(#b1)"><ellipse cx="{cx}" cy="{cy}" rx="{r*.75}" ry="{r}" fill="#fff"/>'
          f'<path d="M{cx} {cy+r} q 2 {r*.8} -4 {r*1.6}" stroke="#CFE8C8" stroke-width="2" fill="none"/></g>')

# Flor de azahar (naranjo): flores blancas de 5 pétalos con el centro amarillo, capullos y hojas
ART["azahar"] = svg(
  leaf(250, 150, 90, 30, 128, "#D5EBCB", .55) + leaf(150, 205, 70, 24, -120, "#D5EBCB", .5) + leaf(320, 238, 56, 20, 150, "#D5EBCB", .45) +
  flower(245, 140, 60, 5, "#fff", .8, center="#F6C343", rot=10) + flower(140, 205, 40, 5, "#fff", .72, center="#F6C343", rot=-24) +
  flower(328, 232, 32, 5, "#fff", .7, center="#F6C343", rot=30) +
  bud(188, 92, 11, .7) + bud(318, 84, 9, .6) + bud(92, 128, 8, .55) +
  "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFF3C9" opacity=".7" filter="url(#b1)"/>' for x, y, r in [(70, 250, 4), (370, 150, 3.5), (210, 270, 3)]) +
  '<circle cx="245" cy="140" r="95" fill="#fff" opacity=".18" filter="url(#b8)"/>')

def rose(cx, cy, r, op):
  """Rosa vista desde arriba: tres coronas de pétalos cada vez más pequeñas y claras."""
  rings = [(1.0, 6, "#F7A9BC", 0), (.72, 5, "#FBC7D3", 30), (.46, 4, "#FFE3EA", 12)]
  g = "".join(petal(cx, cy, r*k, r*k*.75, rot + i*360/n, c, .9, "b1") for k, n, c, rot in rings for i in range(n))
  return (f'<g opacity="{op}">{g}<circle cx="{cx}" cy="{cy}" r="{r*.16}" fill="#F48FA8" opacity=".8" filter="url(#b1)"/>'
          f'<path d="M{cx-r*.1} {cy} a {r*.1} {r*.1} 0 1 1 {r*.16} {r*.06}" stroke="#fff" stroke-width="2" fill="none" opacity=".7"/></g>')

ART["rosa"] = svg(
  rose(250, 140, 74, .7) + rose(100, 225, 38, .55) +
  leaf(300, 200, 60, 24, 120, "#fff", .4) + leaf(195, 215, 52, 20, -130, "#fff", .35) +
  petal(350, 70, 30, 16, -35, "#fff", .45) + petal(70, 80, 24, 13, 30, "#fff", .4))

ART["hierba"] = svg(
  leaf(250, 290, 190, 46, -8, "#fff", .45) + leaf(250, 290, 150, 36, 30, "#fff", .4) + leaf(250, 290, 140, 34, -45, "#fff", .35) +
  leaf(100, 300, 120, 30, 16, "#fff", .35) + leaf(350, 300, 110, 28, -20, "#fff", .3) +
  "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFF6CC" opacity=".55" filter="url(#b1)"/>' for x, y, r in [(150, 90, 9), (330, 110, 7), (80, 150, 6)]))

# P4 · plan para desconectar
ART["hogar"] = svg(
  '<ellipse cx="230" cy="240" rx="120" ry="22" fill="#fff" opacity=".35" filter="url(#b8)"/>'
  '<g opacity=".6" filter="url(#b1)">'
  '<path d="M170 140 h120 v70 a 40 40 0 0 1 -40 40 h-40 a 40 40 0 0 1 -40 -40z" fill="#fff" opacity=".75"/>'
  '<path d="M290 160 a 26 26 0 1 1 0 46" stroke="#fff" stroke-width="10" fill="none"/>'
  '</g>' +
  "".join(f'<path d="M{x} 125 c -14 -18 14 -30 0 -50 s 14 -30 0 -48" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity="{o}" filter="url(#b3)"/>'
          for x, o in [(205, .55), (235, .45), (262, .4)]) +
  '<circle cx="90" cy="90" r="46" fill="#FFE2B0" opacity=".45" filter="url(#b8)"/>')

ART["mar"] = svg(
  '<circle cx="290" cy="110" r="38" fill="#FFF4D6" opacity=".7" filter="url(#b3)"/>'
  '<circle cx="290" cy="110" r="80" fill="#fff" opacity=".2" filter="url(#b8)"/>' +
  "".join(f'<path d="M-10 {y} q 25 -12 50 0 t 50 0 t 50 0 t 50 0 t 50 0 t 50 0 t 50 0 t 50 0 t 50 0" stroke="#fff" stroke-width="{sw}" fill="none" stroke-linecap="round" opacity="{o}" filter="url(#b1)"/>'
          for y, sw, o in [(178, 3, .6), (198, 3, .45), (222, 2.5, .35)]) +
  '<g opacity=".55" filter="url(#b1)"><path d="M110 168 l0 -58 l34 50 z" fill="#fff"/><path d="M100 170 h52 l-8 10 h-36z" fill="#fff"/></g>'
  + "".join(f'<path d="M{x} {y} q 6 -6 12 0 q 6 -6 12 0" stroke="#fff" stroke-width="2" fill="none" opacity=".55"/>' for x, y in [(60, 70), (90, 55), (200, 60)]))

ART["noche"] = svg(
  '<path d="M300 50 a 46 46 0 1 0 38 72 a 36 36 0 1 1 -38 -72z" fill="#FFF3C4" opacity=".7" filter="url(#b1)"/>'
  '<circle cx="310" cy="85" r="70" fill="#FFE59A" opacity=".18" filter="url(#b8)"/>' +
  "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{o}" filter="url(#b3)"/>' for x, y, r, c, o in
          [(80, 220, 26, "#FFD3E2", .35), (150, 250, 18, "#FFE59A", .35), (230, 230, 30, "#fff", .22), (330, 250, 20, "#FFC4D6", .3), (40, 150, 14, "#fff", .25)]) +
  sparkle(120, 80, 9, .6) + sparkle(200, 50, 6, .5) + sparkle(380, 180, 7, .5))

# P5 · frase
ART["simple"] = svg(
  '<ellipse cx="200" cy="232" rx="130" ry="16" fill="#1B2350" opacity=".06" filter="url(#b8)"/>'
  '<g fill="#AFBBDD" opacity=".35" filter="url(#b3)"><rect x="114" y="176" width="180" height="56" rx="16"/><rect x="129" y="128" width="150" height="50" rx="15"/><rect x="144" y="86" width="120" height="44" rx="14"/></g>'
  '<g opacity=".8" filter="url(#b1)">'
  '<rect x="110" y="170" width="180" height="56" rx="16" fill="#fff" opacity=".8"/>'
  '<rect x="125" y="122" width="150" height="50" rx="15" fill="#fff" opacity=".7"/>'
  '<rect x="140" y="80" width="120" height="44" rx="14" fill="#fff" opacity=".6"/>'
  '<path d="M110 198 h180 M125 147 h150 M140 102 h120" stroke="#C9D2EA" stroke-width="2" opacity=".7"/></g>'
  '<circle cx="320" cy="70" r="30" fill="#fff" opacity=".35" filter="url(#b8)"/>')

ART["libre"] = svg(
  '<circle cx="110" cy="80" r="40" fill="#FFF1CF" opacity=".55" filter="url(#b3)"/>' +
  "".join(f'<path d="M110 80 L{110+math.cos(a)*120} {80+math.sin(a)*120}" stroke="#fff" stroke-width="2" opacity=".25"/>' for a in [i*math.pi/7 for i in range(8)]) +
  '<g opacity=".7" filter="url(#b1)"><path d="M290 70 l30 40 l-30 50 l-30 -50z" fill="#fff" opacity=".8"/>'
  '<path d="M290 160 C 280 200, 310 220, 290 260" stroke="#fff" stroke-width="2" fill="none"/>'
  '<path d="M286 190 l-10 6 l10 4 M294 222 l10 6 l-10 4" stroke="#fff" stroke-width="2" fill="none"/></g>' +
  "".join(f'<path d="M{x} {y} q {s} {-s*.8} {s*2} 0 q {s} {-s*.8} {s*2} 0" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" opacity="{o}"/>'
          for x, y, s, o in [(170, 150, 10, .6), (205, 130, 7, .5), (150, 190, 6, .45), (60, 200, 8, .4)]))

ART["detalle"] = svg(
  '<g opacity=".65" filter="url(#b1)">'
  '<path d="M200 150 C 150 90, 90 110, 110 150 C 120 180, 170 170, 200 150z" fill="#fff" opacity=".75"/>'
  '<path d="M200 150 C 250 90, 310 110, 290 150 C 280 180, 230 170, 200 150z" fill="#fff" opacity=".75"/>'
  '<path d="M196 156 C 180 200, 160 230, 140 260" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".6"/>'
  '<path d="M204 156 C 220 200, 240 230, 262 258" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".6"/>'
  '<circle cx="200" cy="152" r="14" fill="#fff"/></g>' +
  sparkle(320, 70, 12, .6) + sparkle(80, 80, 8, .5) + sparkle(345, 230, 7, .45) +
  '<circle cx="200" cy="150" r="90" fill="#fff" opacity=".15" filter="url(#b8)"/>')

os.makedirs(OUT, exist_ok=True)
for k, v in ART.items():
  with open(os.path.join(OUT, f"{k}.svg"), "w") as f: f.write(v)
print(len(ART), "ilustraciones en", OUT)
