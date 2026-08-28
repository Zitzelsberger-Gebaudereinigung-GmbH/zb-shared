# LEARNI OS — Analysepaket für Codex

Zweitmeinung und Prüfung einer Konzeptkette. **Kein Bauauftrag.**

## Einstieg

**`CODEX_ANALYSEAUFTRAG.md` zuerst lesen.** Dort stehen Auftrag, Kontext, die getroffenen
Entscheidungen, die Prüffragen und das erwartete Ergebnisformat.

## Inhalt

| Verzeichnis | Was drin ist |
|---|---|
| `CODEX_ANALYSEAUFTRAG.md` | Der Auftrag. Einstiegspunkt. |
| `01_konzept_original/` | Das Ausgangskonzept, erstellt mit ChatGPT Work: Übergabedokument und klickbarer Entwurf. |
| `02_review/` | Die Analyse dazu: Walt-Disney-Methode und Plenum aus sechs Stakeholder-Rollen, mit Urteil, elf Bruchstellen und den beantworteten Entscheidungsfragen. |
| `03_prototyp/` | Der Prototyp des korrigierten Vertical Slice. `learni-os-prototyp.html` ist eigenständig und im Browser lauffähig; die `*.css` und `*.js` daneben sind die Quellfragmente, aus denen sie zusammengesetzt wird. |
| `04_kontext_repo/` | Die bestehende geteilte Bibliothek `zb-shared` im Original: kanonischer KI-Zugang, Mailer, PDF. Nur für die Architekturfragen relevant. |
| `05_offene_punkte/` | Die sieben offenen Bruchstellen als Fließtext und als `bruchstellen.json`. |
| `06_entscheidungen/` | Was gestrichen wurde, warum, und bei welchem Ereignis die Entscheidung neu zu treffen ist. |

## Rahmen

Keine personenbezogenen Daten, keine Zugangsdaten, keine Produktionsdaten. Alle Namen, Objekte und
Nachweise sind erfunden. Geldbeträge sind Größenordnungen auf offengelegten Annahmen. Rechtliche
Einschätzungen stammen aus einer simulierten Fachrolle und ersetzen keine anwaltliche Prüfung — sie
sind im Review als prüfbedürftig gekennzeichnet.

## Herkunft

Analyse, Review und Prototyp entstanden in Claude Code. Repository:
`Zitzelsberger-Gebaudereinigung-GmbH/zb-shared`, Branch `claude/ki-learning-management-system-yvngrv`,
Verzeichnis `docs/learni-os/`. Das Paket ist vollständig und kommt ohne Repo-Zugang aus.
