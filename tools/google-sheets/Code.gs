/**
 * Receptor de respuestas del test «Descubre tu fragancia Flor».
 * Se pega en la hoja de cálculo: Extensiones → Apps Script, y se publica como aplicación web
 * (ver README.md en esta carpeta). Cada test completado añade una fila en la pestaña «Respuestas».
 *
 * El dashboard (dashboard.html) lee los datos con { accion: "leer", clave: "…" }. La clave se guarda en
 * Configuración del proyecto → Propiedades del script → CLAVE_DASHBOARD (nunca en el código).
 */

const HOJA = 'Respuestas';
const FRAGANCIAS = ['Azul', 'Nenuco', 'Original', 'Mediterráneo', 'Cerezo y Frambuesa',
                    'Delicias de Verano', 'Pieles Sensibles', 'Orquídea Blanca'];
const COLUMNAS = [
  'Fecha', 'ID participación', 'Fragancia resultado',
  'P1 · Tipo de aroma', 'P2 · Cómo se siente', 'P3 · Ingredientes', 'P4 · Plan para desconectar', 'P5 · Frase',
  ...FRAGANCIAS.map(f => 'Puntos ' + f),
  'Dispositivo', 'Idioma', 'Origen', 'utm_source', 'utm_medium', 'utm_campaign', 'Página',
];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000); // evita que dos envíos simultáneos se pisen
  try {
    const d = JSON.parse(e.postData.contents);
    if (d.accion === 'leer') return leer_(d.clave);
    const hoja = obtenerHoja_();
    const puntos = d.puntos || {};
    hoja.appendRow([
      new Date(),
      limpiar_(d.id),
      limpiar_(d.resultado),
      ...(d.respuestas || []).slice(0, 5).map(limpiar_),
      ...FRAGANCIAS.map(f => Number(puntos[f]) || 0),
      limpiar_(d.dispositivo), limpiar_(d.idioma), limpiar_(d.origen),
      limpiar_(d.utm_source), limpiar_(d.utm_medium), limpiar_(d.utm_campaign), limpiar_(d.pagina),
    ]);
    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

// Devuelve todas las filas para el dashboard, solo con la clave correcta.
function leer_(clave) {
  const buena = PropertiesService.getScriptProperties().getProperty('CLAVE_DASHBOARD');
  if (!buena || String(clave || '') !== buena) return json_({ ok: false, error: 'Clave incorrecta' });
  const valores = obtenerHoja_().getDataRange().getValues();
  const columnas = valores.shift() || COLUMNAS;
  const filas = valores.map(r => r.map(v => v instanceof Date ? v.toISOString() : v));
  return json_({ ok: true, columnas, filas, actualizado: new Date().toISOString() });
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

// Al abrir la URL en el navegador: comprobación rápida de que está publicado.
function doGet() {
  return ContentService.createTextOutput('Receptor del test Flor activo.');
}

function obtenerHoja_() {
  const libro = SpreadsheetApp.getActiveSpreadsheet();
  let hoja = libro.getSheetByName(HOJA);
  if (!hoja) hoja = libro.insertSheet(HOJA);
  if (hoja.getLastRow() === 0) {
    hoja.appendRow(COLUMNAS);
    hoja.getRange(1, 1, 1, COLUMNAS.length).setFontWeight('bold').setBackground('#232850').setFontColor('#ffffff');
    hoja.setFrozenRows(1);
    hoja.getRange('A:A').setNumberFormat('dd/mm/yyyy hh:mm:ss');
  }
  return hoja;
}

// Texto corto y sin fórmulas (un valor que empieza por = + - @ se guarda como texto).
function limpiar_(v) {
  const s = String(v == null ? '' : v).slice(0, 300);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}
