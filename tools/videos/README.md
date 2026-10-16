# Vídeos de presentación de los botes

Generan los vídeos que aparecen en el resultado del test (`assets/videos/<clave>.mp4`) y una imagen fija (`<clave>.webp`, primer fotograma del bucle, que se ve si el vídeo no se reproduce o si el usuario tiene activado "reducir movimiento").

## Regenerar

Desde la carpeta de la landing:

```bash
./tools/videos/generar.sh
```

Para regenerar solo algunos: `./tools/videos/generar.sh azul cerezo`

Claves: `azul`, `nenuco`, `original`, `medit`, `cerezo`, `delicias`, `pieles`, `orquidea`.

## Requisitos

- macOS con Swift (viene con las Command Line Tools de Xcode). Se usa para codificar en MP4 H.264, compatible con todos los navegadores, también iPhone.
- Python 3 con Pillow (`pip3 install Pillow`).

## Qué se puede ajustar

- **Bucle:** el vídeo es un ciclo cerrado; el último fotograma es idéntico al primero y la landing lo reproduce en bucle. Si cambias la duración, todo el movimiento se ajusta solo a ese ciclo.
- **Duración, fps y peso:** variables `SEGUNDOS`, `FPS` y `BITRATE` en `generar.sh`.
- **Color de fondo y elementos que caen (pétalos, flores, semillas):** diccionario `PROD` al principio de `frames.py`.
- **Animación** (destello, flotación del bote, halo, cantidad y tamaño de pétalos): función `main()` y `make_petals()` en `frames.py`.
- **Imagen del bote:** se toma de `assets/productos/<clave>.webp`.

## Archivos

- `generar.sh` — script principal.
- `frames.py` — dibuja los fotogramas (720×900, formato 4:5).
- `encode.swift` — une los fotogramas en el MP4.
