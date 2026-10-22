# Guardar los tests en Google Sheets

Cada persona que completa el test añade una fila en la pestaña **Respuestas** de esta hoja:
https://docs.google.com/spreadsheets/d/1bnfjKt4doYfU2H7WqSaUHA95zjXQiNGrcyjZKhd7ek0/edit

La fila se envía al llegar a la pantalla de resultado (una vez por test; si repite el test, es una fila nueva).

## Qué se guarda

| Columna | Ejemplo |
|---|---|
| Fecha | 20/10/2026 12:41:05 |
| ID participación | identificador anónimo aleatorio |
| Fragancia resultado | Flor Orquídea Blanca |
| P1 … P5 | `B · Floral y envolvente` (letra + texto de la opción elegida) |
| Puntos de cada fragancia (8 columnas) | 8, 3, 2… |
| Dispositivo | Móvil / Tablet / Escritorio |
| Idioma | es |
| Origen | web desde la que llega, o «Directo» |
| utm_source · utm_medium · utm_campaign | parámetros de campaña de la URL, si los hay |
| Página | URL de la landing |

No se guarda nombre, email ni ningún dato personal: el test no los pide (la participación en el sorteo va por el formulario de https://participa.samplia.com/cualestuflor).

## Instalación (una sola vez, ~5 minutos)

1. Abre la hoja de cálculo y ve a **Extensiones → Apps Script**.
2. Borra el contenido de `Código.gs` y pega el de [`Code.gs`](Code.gs). Guarda (icono del disquete).
3. Pulsa **Implementar → Nueva implementación**.
   - Tipo: **Aplicación web**.
   - Ejecutar como: **Yo** (tu cuenta).
   - Quién tiene acceso: **Cualquier usuario** (necesario para que la landing pueda enviar datos sin iniciar sesión).
4. Pulsa **Implementar** y autoriza los permisos que pide Google (acceso a esta hoja de cálculo).
5. Copia la **URL de la aplicación web** (termina en `/exec`).
6. En `index.html`, busca `const SHEETS_URL = "";` y pega la URL entre las comillas:
   ```js
   const SHEETS_URL = "https://script.google.com/macros/s/XXXXXXXX/exec";
   ```

Para comprobarlo: abre la URL `/exec` en el navegador (debe decir «Receptor del test Flor activo.»), haz el test en la landing y mira que aparece la fila en la pestaña **Respuestas** (se crea sola la primera vez, con la cabecera).

7. **Clave del dashboard:** en Apps Script, ve a **Configuración del proyecto** (icono del engranaje) → **Propiedades del script** → **Añadir propiedad**:
   - Propiedad: `CLAVE_DASHBOARD`
   - Valor: una clave larga que solo conozca el equipo (por ejemplo, 4-5 palabras sin relación entre sí).
8. En `dashboard.html`, busca `const DATA_URL = "";` y pega la **misma** URL `/exec`.

Si más adelante cambias `Code.gs`, hay que volver a publicar: **Implementar → Gestionar implementaciones → editar → Nueva versión**. La URL se mantiene.

## Dashboard de resultados

`dashboard.html` es el informe de participación. Se sube junto a la landing y se abre en:

- GitHub Pages: `https://<usuario>.github.io/<repositorio>/dashboard.html`
- Dominio definitivo: `https://<dominio>/dashboard.html`

Funciona igual en los dos sin cambiar nada: usa rutas relativas y lee los datos directamente de Google.

Al entrar pide la clave (`CLAVE_DASHBOARD`). El navegador la recuerda hasta pulsar **Salir**. Muestra:

- Tests completados, tests de hoy, de los últimos 7 días y la fragancia más frecuente.
- Resultado del test por fragancia, tests por día, respuestas de cada pregunta, dispositivo, origen y campaña (UTM).
- Tabla con cada participación (fecha, ID, resultado, respuestas P1–P5, dispositivo, origen y campaña), con buscador y paginación.
- Filtros por periodo (hoy, 7 días, 30 días, todo), dispositivo y origen. **Descargar CSV** exporta lo filtrado, listo para Excel.

**Modo demostración:** mientras `DATA_URL` esté vacío, o añadiendo `?demo` a la dirección, se ven datos de ejemplo.

**Seguridad:** los datos no se publican en la web; el dashboard los pide a Google con la clave en cada carga y Google los entrega solo si coincide. La clave no está en el código (el repositorio puede ser público). La página tiene `noindex` para que no aparezca en buscadores. Para cambiar la clave, edita la propiedad `CLAVE_DASHBOARD`: no hace falta volver a publicar.

## Notas

- Mientras `SHEETS_URL` esté vacío, la landing no envía nada.
- La landing envía los datos con `mode: "no-cors"`: es lo que permite Apps Script desde otra web, pero el navegador no puede leer la respuesta, así que un fallo del servidor no se muestra al usuario (el test sigue funcionando igual).
- Cualquiera con la URL `/exec` podría enviar filas falsas. Para una promoción con premio, la participación válida es la del formulario de participación (con ticket); esta hoja sirve para estadísticas del test.
- Leer los datos sí exige la clave: sin ella, el script responde «Clave incorrecta».
