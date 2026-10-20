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

No se guarda nombre, email ni ningún dato personal: el test no los pide (la participación en el sorteo va por Tally, que tiene su propia integración con Google Sheets).

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

Si más adelante cambias `Code.gs`, hay que volver a publicar: **Implementar → Gestionar implementaciones → editar → Nueva versión**. La URL se mantiene.

## Notas

- Mientras `SHEETS_URL` esté vacío, la landing no envía nada.
- La landing envía los datos con `mode: "no-cors"`: es lo que permite Apps Script desde otra web, pero el navegador no puede leer la respuesta, así que un fallo del servidor no se muestra al usuario (el test sigue funcionando igual).
- Cualquiera con la URL `/exec` podría enviar filas falsas. Para una promoción con premio, la participación válida es la de Tally (con ticket); esta hoja sirve para estadísticas del test.
