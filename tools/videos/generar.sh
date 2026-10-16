#!/bin/zsh
# Regenera los vídeos de presentación de los botes (assets/videos/<clave>.mp4 + <clave>.webp).
# Uso:
#   ./tools/videos/generar.sh                  -> los 8 productos
#   ./tools/videos/generar.sh azul cerezo      -> solo los indicados
# Claves: azul nenuco original medit cerezo delicias pieles orquidea
set -e

HERE="${0:A:h}"
ROOT="${HERE:h:h}"
OUT="$ROOT/assets/videos"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

FPS=30
SEGUNDOS=8
BITRATE=1800000   # ~1,3 MB por vídeo de 8 s

if (( $# )); then KEYS=("$@"); else KEYS=(azul nenuco original medit cerezo delicias pieles orquidea); fi

mkdir -p "$OUT"
echo "Compilando el codificador…"
swiftc -O "$HERE/encode.swift" -o "$TMP/encode"

for k in $KEYS; do
  echo "→ $k"
  python3 "$HERE/frames.py" "$k" "$TMP/$k" "$SEGUNDOS" "$FPS"
  "$TMP/encode" "$TMP/$k" "$OUT/$k.mp4" "$FPS" "$BITRATE"
  # Fotograma final (se muestra si el vídeo no se reproduce)
  python3 -c "from PIL import Image; Image.open('$TMP/$k/poster.jpg').save('$OUT/$k.webp', quality=80)"
done

echo "Listo: $OUT"
