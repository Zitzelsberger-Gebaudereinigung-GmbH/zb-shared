# Quellfragmente des Prototyps

`../learni-os-prototyp.html` ist die ausgelieferte, eigenständige Datei. Sie wird aus diesen
Fragmenten zusammengesetzt:

- **CSS** in dieser Reihenfolge: `base.css` (Tokens, beide Themes) → `shell.css` (Markenleiste, Kopf,
  Telefonrahmen) → `ui.css` (Bausteine im Telefon) → `rail.css` (Erläuterungsspalte)
- **JS** in dieser Reihenfolge: `data.js` (Inhalte je Sprache × Register, Objekte, Kriterien, Skills) →
  `icons.js` (Symbole und Piktogramme) → `app.js` (Bildschirme und Erläuterungstexte) →
  `render.js` (Rollen, Tabs, Rendering, Interaktion)

Die Reihenfolge ist bindend: `render.js` ruft beim Laden `render()` auf und setzt alles davor voraus.

Zusammensetzen: CSS in den `<style>`-Block, JS in den `<script>`-Block der HTML-Datei einsetzen.
Das Logo ist als Data-URI eingebettet und bleibt beim Neubau erhalten, wenn nur die beiden Blöcke
ersetzt werden.

Syntaxprüfung ohne Browser:

    cat data.js icons.js app.js render.js > /tmp/chk.js && node --check /tmp/chk.js
