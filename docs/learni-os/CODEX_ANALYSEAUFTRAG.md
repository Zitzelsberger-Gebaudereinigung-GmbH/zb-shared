# LEARNI OS — Analyseauftrag für Codex

**Auftraggeber:** Zitzelsberger Gebäudereinigung GmbH
**Datum des Pakets:** 27.08.2026
**Art des Auftrags:** Zweitmeinung und Prüfung. **Kein Bauauftrag.**

---

## 0. Was hier von dir erwartet wird

Ein Konzept für ein KI-gestütztes Lernsystem wurde mit ChatGPT Work erstellt (`01_konzept_original/`), anschließend in Claude Code analysiert und überarbeitet (`02_review/`), und der überarbeitete Vertical Slice wurde als klickbarer Prototyp gebaut (`03_prototyp/`).

Du bist die **dritte Instanz**. Deine Aufgabe ist es, diese Kette zu prüfen — nicht sie zu bestätigen.

Konkret erwarten wir:

1. **Fehler finden**, die beide vorherigen Durchgänge übersehen haben.
2. **Begründeten Widerspruch**, wo eine getroffene Entscheidung falsch ist. Widerspruch ist erwünscht, nicht unhöflich. Eine Zweitmeinung, die nur zustimmt, war das Geld nicht wert.
3. **Bestätigung**, wo eine Entscheidung trägt — kurz, mit Begründung, ohne Ausschmückung.

Was wir **nicht** brauchen: eine Zusammenfassung des Materials (wir kennen es), Lob, eine Neuformulierung des Konzepts, oder eine vierte Roadmap.

---

## 1. Kontext in zehn Sätzen

Gebäudereinigungsunternehmen, rund 500 operative Mitarbeitende, Deutschland. Zielgruppe sind Reinigungskräfte: oft Teilzeit, Fluktuation um 40 % pro Jahr, mehrsprachig (Türkisch, Rumänisch, Polnisch, Bulgarisch, Arabisch, Ukrainisch), niedrige Digitalaffinität, privates Smartphone, Arbeit früh morgens oder abends verteilt über viele Kundenobjekte. Dazwischen stehen Objektleitungen, die je 10–15 Objekte und 50–70 Kräfte verantworten und bei Kundenaudits Unterweisungsnachweise vorlegen müssen. Das bestehende LMS ist Memberspot; der Vertrag läuft ungekündigt weiter. Es existieren bereits eigene Python-Anwendungen auf Render (Reklamationsbearbeitung, QualiCheck, Objektaudit, Objektbesuch, Mitarbeiter-App), die sich über die Bibliothek `zb-shared` einen kanonischen KI-Zugang teilen (Anthropic Claude direkt oder über Vertex in der EU, Vertex-Embeddings, Mailer, PDF). Entwicklungskapazität: faktisch eine Person plus KI-Assistenz. **Es gibt keinen Betriebsrat.** Lernzeit wird als bezahlte Arbeitszeit behandelt. Budgetrahmen Jahr 1: 150–250 T€, über die Hälfte davon Content.

Der ursprüngliche Auftrag des Geschäftsführers lautete wörtlich: *„das innovativste KI-unterstützteste Learning Management System, welches eine einzigartige Employee Journey auslöst."*

---

## 2. Was bereits entschieden ist — und woran du es messen sollst

Diese Entscheidungen sind gefallen. Du darfst und sollst ihnen widersprechen, aber nur mit einem Argument, das über „man könnte es auch anders machen" hinausgeht.

| # | Entscheidung | Begründung in Kurzform |
|---|---|---|
| E1 | **Kurskatalog und Player kaufen, Nachweis- und KI-Schicht selbst bauen** | Der selbstgebaute Teil ist in beiden Welten identisch; der Rest ist Massenware. Auswahlkriterium für das Kauf-LMS ist ausschließlich API, Webhooks, SSO, Export — nicht die Oberfläche. |
| E2 | **Python/FastAPI + Postgres/pgvector + `zb-shared`, kein Next.js/Supabase** | Ein Entwickler, eine Sprache. `zb-shared` in TypeScript nachzubauen wäre unheilbar. RLS wäre ein zweites, redundantes Autorisierungsmodell, weil ohnehin alles serverseitig durchgesetzt werden muss. |
| E3 | **Eigenes Repository, nicht `zb-shared`** | `zb-shared` ist eine versionierte Bibliothek, die fünf Apps per Git-Tag pinnen. Abhängigkeitsrichtung ausschließlich Produkt → Bibliothek. |
| E4 | **Vertical Slice „grüne Objektmappe" statt Kurs-Player** | Braucht null Content, ersetzt am ersten Tag die Papier-Unterweisungsliste, ist GefStoffV-konform, weil er die mündliche Unterweisung dokumentiert statt sie zu ersetzen. |
| E5 | **Ein Quiz erreicht nie „kann selbstständig ausführen"** | Datenbank-Constraint, kein Feature-Flag. Nur ein Beobachtungsnachweis schaltet die Tätigkeitsfreigabe frei. |
| E6 | **Keine Canvas-Unterschrift** | Beweist weder Identität noch Abwesenheit fremder Hilfe; verschiebt Haftung nach unten. Ersetzt durch personalisierten Account, Zeitstempel und einen anderen Bestätigungstext. |
| E7 | **Register (standard/einfach) ist eine eigene Dimension neben der Sprache** | Sonst gibt es kein „Türkisch, einfach". |
| E8 | **Gestrichen, nicht verschoben:** Headset-VR, Open Badges 3.0, CLR 2.0, xAPI/LRS, eIDAS-QES, Lernserien, Punktestände, Ranglisten, Multi-Tenancy | Je Punkt begründet in `06_entscheidungen/GESTRICHEN_UND_WARUM.md`, jeweils mit Umkehrpunkt. |

---

## 3. Prüffragen, nach Wichtigkeit

### A. Der Prototyp als Code (`03_prototyp/`)

Die Datei `learni-os-prototyp.html` ist eigenständig; die Einzelfragmente (`*.css`, `*.js`) sind die Quellen, aus denen sie zusammengesetzt wird. Es ist eine **Konzeptreferenz, keine Produktionscodebasis** — bewerte sie an diesem Anspruch, nicht an dem eines Produkts.

1. Funktionale Fehler: Zustandsübergänge, die in eine Sackgasse führen; Zustände, die beim Rollen- oder Sprachwechsel nicht zurückgesetzt werden; Ereignisbehandlung, die bei verschachtelten Elementen den falschen Treffer nimmt.
2. Barrierefreiheit: Die Zielgruppe umfasst Menschen mit eingeschränkter Lesekompetenz und ältere Nutzerinnen. Tastaturbedienbarkeit, Fokussichtbarkeit, Beschriftung interaktiver Elemente, Kontrastverhältnisse in beiden Themes, Umgang mit `prefers-reduced-motion`. **Wo verfehlt die Umsetzung WCAG 2.2 AA?**
3. Die Sprachausgabe nutzt `speechSynthesis`. Welche Ausfallmodi sind nicht behandelt? Was passiert bei fehlender Stimme für ein Locale, bei Seitenwechsel während der Ausgabe, auf iOS?
4. Ist die Trennung Inhalt / Oberflächenlokalisierung / Register im Datenmodell des Prototyps sauber, oder gibt es Stellen, an denen sie vermischt wurde?

### B. Das Datenmodell (Abschnitt 2.2 in `02_review/KONZEPTREVIEW.md`)

5. Die vorgeschlagenen Deltas gegenüber dem Ursprungskonzept: Welche Tabelle fehlt, welche ist überflüssig, welche Beziehung ist falsch modelliert?
6. **Beweiskette und Widerruf.** Der Nachweis ist hash-verkettet, bindet den Server-Eingang und kennt einen Widerruf als eigenen Kettenblock. Ist diese Konstruktion tragfähig? Wo lässt sie sich brechen? Wie prüft ein Auditor sie unabhängig, ohne Vertrauen in den Betreiber?
7. **Content-Versionierung.** Ein Nachweis referenziert die absolvierte Inhaltsversion. Was passiert bei einer fehlerhaften Frage, die nach 200 bestandenen Prüfungen entdeckt wird? Das Review nennt das Problem, löst es aber nicht. **Entwirf die Korrekturpolicy.**
8. **Offline-Erfassung.** Beobachtungen werden offline erfasst, Selbst-Quizze nicht. Trägt diese Trennlinie? Wie löst man Sync-Konflikte, ohne die Beweiskette zu beschädigen?

### C. Die Architekturentscheidung (E1–E3)

9. Halte E2 gegen die Alternative. Der Prüfstein ist nicht Eleganz, sondern: Was passiert, wenn die eine Person, die das baut, sechs Monate ausfällt?
10. **RAG unter Autorisierung.** Ein Autorisierungsfilter über einem ANN-Index liefert entweder falsches Recall (Post-Filter) oder erzwingt einen Seq-Scan (Pre-Filter). Der vorgeschlagene Weg ist Partitionierung nach Scope plus Partial Indexes. Trägt das bei der zu erwartenden Größenordnung (grob 10.000–50.000 Chunks, 3 Rollen, ~15 Objekte)? Gibt es einen besseren Weg?
11. **Kostenmodell.** Das Review schätzt einen RAG-Turn auf grob 1,8 Cent und den laufenden Betrieb auf zweistellige Euro-Beträge pro Monat, nennt aber Re-Embedding bei jeder Inhaltsänderung als eigentlichen Kostentreiber. Rechne gegen. Wo ist die Schätzung falsch?

### D. Die offenen Bruchstellen (`05_offene_punkte/`)

12. Sieben Bruchstellen sind unverändert offen. Prüfe je Punkt: Ist die Diagnose richtig? Ist die vorgeschlagene Gegenmaßnahme ausreichend? Was fehlt?
13. **Gibt es eine achte, die niemand gesehen hat?** Das ist die wertvollste mögliche Antwort in diesem ganzen Auftrag.

### E. Aufwand

14. Die Schätzung lautet 6–8 Personenmonate Entwicklung bei einer Person für den Slice inklusive Betrieb, Migration, Pflege-UI und Tests. Sie wurde von 4 PM nach oben korrigiert. **Ist sie immer noch zu optimistisch?** Wenn ja: welche Position fehlt?

---

## 4. Wo wir uns selbst am unsichersten sind

Ehrlichkeit spart dir Zeit. An diesen drei Stellen ist unsere Position am schwächsten — dort ist Widerspruch am wahrscheinlichsten berechtigt:

- **Open Badges gestrichen.** Das Ziel — ein mitnehmbarer Nachweis als Antwort auf 40 % Fluktuation — ist richtig. Nur der Standard gilt uns als verfrüht, ersetzt durch ein signiertes PDF mit Verifikations-QR. Falls du einen Grund siehst, warum das der falsche Weg ist, sag es deutlich.
- **Kaufen statt bauen (E1).** Die These lautet, dass die Entscheidung umkehrbar ist, weil bei fehlendem passendem Kauf-LMS derselbe Dienst um einen einfachen Player wächst. Der Kritiker hat den Aufwand dafür bereits von 1,5 auf 3–4 PM korrigiert. Ist die Umkehrbarkeit trotzdem eine Illusion?
- **Die Rechtseinschätzungen.** Sie stammen aus einer simulierten Fachrolle, nicht von einer Anwältin, und sind im Review als prüfbedürftig gekennzeichnet. Wenn dir eine Norm falsch zitiert oder falsch ausgelegt erscheint — insbesondere zu §14 Abs. 2 GefStoffV, zur Einordnung nach EU AI Act Anhang III, oder zum Beweiswert nach §416 ZPO — nenne es. Wir holen dann gezielt anwaltliche Prüfung ein, statt breit.

---

## 5. Erwartetes Ergebnis

Ein Dokument, gegliedert wie folgt:

1. **Urteil in fünf Sätzen** — trägt die Kette, oder nicht.
2. **Neue Befunde** — was beide vorherigen Durchgänge übersehen haben. Je Befund: Was bricht, wann bricht es, was schließt es. Nach Schadenshöhe × Wahrscheinlichkeit sortiert.
3. **Begründeter Widerspruch** zu E1–E8, sofern vorhanden. Je Punkt: Entscheidung, warum sie falsch ist, was stattdessen.
4. **Bestätigungen** — welche Entscheidungen tragen. Ein bis zwei Sätze je Punkt, keine Ausschmückung.
5. **Code-Befunde zum Prototyp** — mit Datei und Zeilenbezug.
6. **Die achte Bruchstelle**, falls du eine findest.

Belege deine Aussagen am Material. Wo du Annahmen triffst, kennzeichne sie als solche.

---

## 6. Rahmenbedingungen

- **Keine personenbezogenen Daten.** Alle Namen, Objekte und Nachweise im Paket sind erfunden. Es gibt keine Produktionsdaten, keine Zugangsdaten und keine Geheimnisse in diesem Paket. Falls du doch etwas findest, das wie ein Geheimnis aussieht, melde es als Befund.
- **Zahlen sind Größenordnungen** auf offengelegten Annahmen, keine Kalkulation. Behandle sie so.
- **Kein Code schreiben**, außer als Beleg für einen Befund. Der Auftrag ist Analyse.
- Falls du das Repository brauchst: `Zitzelsberger-Gebaudereinigung-GmbH/zb-shared`, Branch `claude/ki-learning-management-system-yvngrv`, Verzeichnis `docs/learni-os/`. Das Paket ist aber vollständig — du kommst ohne aus.

---

## 7. Reihenfolge zum Lesen

1. Dieses Dokument.
2. `01_konzept_original/CLAUDE_CODE_HANDOFF.md` — das Ausgangskonzept.
3. `02_review/KONZEPTREVIEW.md` — die Analyse. Abschnitt 0 und 6 zuerst, wenn die Zeit knapp ist.
4. `05_offene_punkte/OFFENE_BRUCHSTELLEN.md` und `bruchstellen.json`.
5. `03_prototyp/learni-os-prototyp.html` im Browser öffnen, dann die Quellfragmente lesen.
6. `06_entscheidungen/GESTRICHEN_UND_WARUM.md`.
7. `04_kontext_repo/` nur für die Architekturfragen C.
