# Feedback zur AGI-/Agentic-AI-Strategie Zitzelsberger

**Stand:** 29.08.2026 · **Auftrag:** `02_PRUEFAUFTRAG_AN_CLAUDE_CODE.md` · **Format:** `03_FEEDBACK_TEMPLATE.md`
**Methode:** Walt-Disney-Team (Träumer · Realist · Kritiker), anschließend Plenum-Entscheid.

## Prüfgrundlage

Gelesen wurde nicht nur das Feedbackpaket, sondern der **tatsächliche Code-Bestand**:

| Quelle | Was daraus stammt |
|---|---|
| `claude_code_agi_feedback/*` (6 Dateien) | die zu prüfende Strategie |
| `zb-shared` (v0.2.3) | `ki_client`, `mailer`, `pdf`; Konsolidierung `[d-303]` |
| `zitzelsberger-mitarbeiter-app` (HEAD `8002c11`) | 117 Backend-Module, `main.py` 17.296 Zeilen / 366 Routen, `ki_register.json`, `docs/rechtlich/`, `konsolidierung/PHASE-2-3-PLAYBOOK.md`, `konzepte/` (48 Konzepte) |
| `list_repos` | 17 Repositories der Organisation |

Nicht gelesen (kein Zugriff angefordert): `wissensmanagement_2.0`, `supabase-schema`, `reklamationsmanagement`, `qualicheck`, `objektbesuch-agent`, `zitzelsberger-website`, `zitzelsberger-dashboard` und die LP-Repos. Aussagen dazu stützen sich auf das Konsolidierungs-Playbook der MA-App und sind als solche gekennzeichnet.

---

## 0. Der eine Befund, der alles verschiebt

> **Die Strategie ist ein Greenfield-Plan für ein Haus, das schon steht.**

`01_STRATEGIE_UND_ANALYSE.md` beschreibt zehn Agenten, die in 0–36 Monaten aufzubauen seien, und eine fünfschichtige Zielarchitektur, die zu schaffen sei. Der Code-Bestand zeigt: **alle zehn existieren bereits in produktiver oder halbproduktiver Form.**

| Strategie sagt „aufzubauen" | Existiert bereits als |
|---|---|
| 3.1 Knowledge Brain | `wissenspflege/` (OCR→Chunk→Embedding→Storage), `betriebswissen_service.py`, `rag_rerank.py`, `/api/wissen/ask` — Vertex 768, Hybridsuche + Re-Ranking |
| 3.2 Reklamations-/Qualitätsagent | `reklamation_dashboard_service.py`, `reklamation_regelkreis_service.py`, `reklamation_mail_service.py`, `qualicheck_*` (4 Module) |
| 3.3 Kalkulations-/Angebotsagent | `angebotskalkulator_service.py`, `leistungsverzeichnis_service.py`, `lv_aenderung_service.py`, `grundriss_service.py`, `raumanker_service.py` |
| 3.4 Objektmanager-Agent | `objekt_tagebuch_service.py`, `objekt_uebergabe_service.py`, `objekt_vertrag_service.py`, `aufgaben_bridge.py`, `prozessboard_service.py` |
| 3.5 Learni | `unterweisung_agent_service.py`, `_quiz_`, `_i18n_` (19 Sprachen), `_zertifikat`, `_objektmodul_`, `vr_training_service.py`, VR-Panoramen |
| 3.6 Kunden-/Vertriebsagent | `zitzelsberger-service-bot`, `zitzelsberger-bewerber-chat`, `nachweis_quoten.py` + Konzept Nachweisportal |
| 3.7 Nachhaltigkeitsagent | `umweltaspekte.py`, `fuhrpark_kosten.py` (CO₂-Bilanz, Eco-Score) |
| 3.8 Einsatzplanungsagent | `einsatzplanung_service.py` (regelbasiert, bewusst ohne KI) |
| 3.9 Multimodaler Praxisassistent | `vor_ort_service.py`, `lager.py` (CLP-Einstufung per Vision), `gbu_bilder_service.py`, `beleg_scanner_service.py` |
| 3.10 Robotik / Physical AI | `rayban_service.py`, `arvr_akzeptanz_service.py` (Akzeptanz-Gate vor Hardware-Entscheidung) |

Ebenso ist **Phase 0 der Roadmap weitgehend erledigt**, was die Strategie als offen führt:

- *KI-Systeminventar* → `backend/ki_register.json`, 39 Module, je mit Zweck, AI-Act-Einstufung, Begründung — plus eine Wache (`scripts/ki_kennzeichnung_wache.py`), die im pre-push-Hook Abweichungen meldet.
- *Prozess-/Datenlandkarte* → `wissen/kartografie.md` (K6) + `konsolidierung/PHASE-2-3-PLAYBOOK.md`.
- *Rollen-/Berechtigungskonzept* → `objekt_rollen` als self-refreshing Single-Source via `pg_cron */30`.
- *Datenschutz-Risikoklassifizierung* → `docs/rechtlich/` mit VVT-Eintrag, DSFA-Entwurf, KI-Literacy-Schulung, Datenschutzhinweis; DSB benannt (PROXI GmbH), Aufsicht LfDI BW.
- *Offene Annahme „Gibt es einen Betriebsrat?"* → in `docs/rechtlich/README.md` bereits beantwortet: **kein Betriebsrat**, § 87 BetrVG entfällt, Information individuell per Info-Brief.

**Konsequenz:** Die Strategie stellt die richtigen Fragen, aber an einen Zustand von vor etwa zwölf Monaten. Würde man ihre Roadmap befolgen, verbrächte man Phase 0 bis 2 (0–12 Monate) damit, Vorhandenes ein zweites Mal zu bauen — während die realen Risiken des gebauten Systems unbearbeitet weiterlaufen.

Das ist kein Vorwurf an das Papier: Es ist als externe Analyse sauber, gut strukturiert und in den Leitprinzipien richtig. Es ist nur **nicht auf dem Stand des eigenen Hauses**. Genau das zu korrigieren ist der Zweck dieses Feedbacks.

---

# Teil I — Walt-Disney-Team

## 1. Der Träumer

*Regel: keine Einwände, nur Möglichkeiten.*

**Das Zielbild ist zu klein geträumt.** Die Strategie beschreibt einen „digitalen Begleiter je Rolle". Was hier tatsächlich entsteht, ist etwas Selteneres: ein **mittelständisches Unternehmen, dessen Betriebswissen maschinenlesbar ist**. 19 Sprachen, VR-Unterweisungen, Objektmappen, Gefährdungsbeurteilungen mit Ortsbefund-Fotos, ein Gefahrstoffkataster, ein Nachweisportal — das hat in dieser Branche kaum jemand.

Drei Träume, die im Papier fehlen:

**1.1 Das Objekt erzählt seine eigene Geschichte.**
Alle Bausteine liegen vor: `objekt_tagebuch`, `raumanker_service`, `raum_qr`, QualiCheck-Verläufe, Reklamationsmuster, Verbrauch, Fuhrpark-Kilometer, Unterweisungsstände. Zusammengezogen entsteht eine **Objektakte, die man befragen kann**: „Warum ist Objekt 4711 im dritten Quartal gekippt?" Heute beantwortet das niemand, weil die Antwort in sechs Tabellen verteilt liegt. Das ist keine neue KI — das ist eine Verbindung.

**1.2 Das Angebot, das aus dem Objektbesuch entsteht.**
`objekt_uebergabe_service` (Erstgespräch) → `grundriss_service`/`raumanker_service` (Flächen) → `leistungsverzeichnis_service` (LV) → `angebotskalkulator_service` (Zeitwerte) → `crosssell_service`. Die Kette ist **modulweise vollständig vorhanden und nirgends durchverbunden**. Wer sie schließt, verkürzt Angebotsdurchlaufzeit von Tagen auf Stunden — und zwar ohne ein einziges neues Modell.

**1.3 Der Nachweis als Produkt.**
`nachweis_quoten.py` + Nachweisportal-Konzept: Kunden bekommen nicht „einen Bericht", sondern **belegte Qualität in Echtzeit** — Kontrollen, Maßnahmen, Umweltkennzahlen, Unterweisungsstände des eingesetzten Personals. In einer Branche, die im Preiskampf steht, ist prüfbare Qualität das einzige tragfähige Differenzierungsmerkmal. Das ist kein IT-Projekt, das ist ein Vertriebsargument.

**Was der Träumer außerdem sieht:** Die Sprachfähigkeit (19 Sprachen, TTS, Voice-Eingabe) ist strategisch unterschätzt. In Reinigungsberufen ist der Anteil Beschäftigter mit Einwanderungsgeschichte hoch (Destatis, in `04_QUELLEN.md` zitiert, aber im Papier nie in einen Anwendungsfall überführt). Ein Betrieb, in dem jede Unterweisung, jede Objektmappe und jede Rückfrage in der Muttersprache funktioniert, hat einen **Rekrutierungs- und Bindungsvorteil**, der schwerer zu kopieren ist als jede Software.

## 2. Der Realist

*Regel: Wie ginge es konkret, mit den Mitteln, die da sind?*

**2.1 Die entscheidende Ressourcenfrage stellt das Papier nicht.**
Die Strategie plant zehn Agenten über 36 Monate, nennt aber **keine Kapazität**. Der Bestand deutet auf eine sehr kleine Entwicklungsmannschaft hin — Konzeptdateien, Log-IDs und Entscheidungsvermerke laufen erkennbar über wenige Personen. Bei dieser Aufstellung ist die realistische Jahresleistung nicht „vier neue Agenten", sondern **zwei bis drei tiefe Konsolidierungszüge plus laufender Betrieb**. Jede Planung, die das ignoriert, produziert Halbfertiges.

**2.2 Der Engpass ist nicht Fähigkeit, sondern Struktur.**
`main.py` mit 17.296 Zeilen und 366 Routen ist der zentrale Realitätsfaktor. Er ist kein Fehler — so entsteht Tempo — aber er ist jetzt der Punkt, an dem Tempo kippt: Jede neue Funktion vergrößert die Fläche, die niemand mehr vollständig überblickt. Der Registereintrag sagt das selbst: `main.py` → *„PRUEFEN — 17.000 Zeilen, Einzelstellen nicht abschliessend geprueft."*

**2.3 Was in den nächsten 6 Monaten tatsächlich geht.**
Nicht zehn Agenten. Sondern:

- **Ein Datenschutz-/EU-Zug** (2–3 Wochen): US-Default schließen, PII-Buckets privatisieren, Bewerber-KI absichern. Kein neues Feature, hoher Risikoabbau.
- **Ein Struktur-Zug** (6–10 Wochen): `main.py` entlang der bestehenden Modulgrenzen in Router zerlegen, beginnend bei den KI-Aufrufstellen — das räumt zugleich den Register-Sammelposten ab.
- **Ein Wertschöpfungs-Zug** (6–8 Wochen): die Angebotskette 1.2 durchverbinden.

Das sind drei Vorhaben, nicht zwölf. Sie sind machbar. Alles darüber hinaus ist Wunsch.

**2.4 Build-vs-Buy ist faktisch bereits entschieden.**
Das Papier führt vier Optionen als offen. Sie sind es nicht: Es läuft Supabase EU + Render Frankfurt + Vertex EU (`europe-west3` Embeddings, `europe-west1` Claude) + Microsoft Graph für das Bewerbungspostfach + Resend für Mail. Ein Wechsel auf eine Copilot-/Power-Platform-zentrierte Welt hieße, 117 Module und 39 KI-Funktionen wegzuwerfen. Der Realist sagt: **Die Frage lautet nicht „build or buy", sondern „was davon kaufe ich künftig zu".** Antwort in Plenum §5.

**2.5 Realistisch ist auch: die Website-Punkte sind billig und wirken.**
Die zehn Website-Empfehlungen (`01_…` §6) sind fachlich richtig und kosten wenig. Die Inkonsistenz „24 h / 24–48 h / 48 h" ist ein Ein-Tages-Fix mit unmittelbarer Wirkung auf Vertrauen und auf die Frage, was man vertraglich zusagt. Strukturierte Daten sind ein Zwei-Wochen-Thema. Beides braucht keinen Agenten und keine Architekturentscheidung.

## 3. Der Kritiker

*Regel: was bricht, was ist falsch, was ist ungedeckt.*

**3.1 Der EU-Default ist dokumentiert, aber nicht durchgesetzt. — schwerwiegend**

`zb_shared/ki_client.py` trägt im Kopf: *„EU-Default (DSGVO, [d-211])"*. Der Code sagt etwas anderes:

```
zb_shared/ki_client.py:28          ANTHROPIC_BACKEND = os.getenv("ANTHROPIC_BACKEND", "direct")
backend/main.py:641                ANTHROPIC_BACKEND = os.getenv("ANTHROPIC_BACKEND", "direct")
backend/wissenspflege_service.py:44  _ANTHROPIC_BACKEND = os.getenv("ANTHROPIC_BACKEND", "direct")
```

`"direct"` = US-API. Und `render.yaml` **deklariert `ANTHROPIC_BACKEND` überhaupt nicht** — gesetzt wird dort nur `ANTHROPIC_API_KEY` (der Direct-Key). Das heißt: Solange die Variable nicht von Hand in der Render-UI steht, laufen alle Claude-Textaufrufe der MA-App in die USA, während Hosting (Frankfurt) und Embeddings (`europe-west3`) EU sind und die Dokumentation EU behauptet.

Das Konsolidierungs-Playbook kennt das Muster bereits an anderer Stelle: *„Foto-KI uneinheitlich: Objektaudit `claude-sonnet-4-6` **direct US** … QM/Reklamation/service-bot Vertex EU"* (P2.2). Es ist also kein Einzelfall, sondern ein **strukturelles Default-Problem**. Ein Default, der in die riskantere Richtung fällt, ist ein Bug — unabhängig davon, was in Render gerade eingestellt ist.

**3.2 Zwei Annex-III-Kandidaten laufen bereits, einer davon mit Bestand. — schwerwiegend**

Das eigene Register ist hier bemerkenswert ehrlich:

- `bewerbung_mail_service.py` → *„Annex III Nr. 4a … DSGVO Art. 22 gilt SCHON HEUTE … **139 Bewerbungen tragen eine Passungsbewertung**."* Kennzeichnung: *„PRUEFEN — Bewerberpool zeigt KI-Passung, Kennzeichnung nicht verifiziert."*
- `video_doku_service.py` → *„Video von ARBEITENDEN Menschen … Würde daraus eine Bewertung der gezeigten Person abgeleitet, wäre es Annex III Nr. 4b UND näherte sich Art. 5."* Kennzeichnung: *„PRUEFEN — hier besonders wichtig."*

Die Strategie behandelt Recruiting-KI unter §9 als abstraktes künftiges Risiko („besonders kritisch"). Tatsächlich ist es ein **bestehender Datenbestand mit KI-erzeugten Personenbewertungen ohne verifizierte Kennzeichnung**. Art. 22 DSGVO und die Informationspflichten gelten unabhängig von jeder AI-Act-Frist. Das ist der Punkt mit dem kürzesten Weg zu einem echten Schaden.

**3.3 20 von 39 KI-Modulen tragen „PRUEFEN". — mittel bis schwer**

Die Wache läuft und meldet sauber: 39/39 registriert, **20 offene Prüfpunkte**, darunter `main.py` als Sammelposten mit ausdrücklich nicht abschließend geprüften Einzelstellen. Der Gesprächsprotokoll-Assistent (`main.py:13442 ff.`, Voice → Claude → Vektor → PDF/Mail) ist ein Beispiel: Er verarbeitet **Personalgespräche**, sein KI-Aufruf liegt in `main.py` und fällt damit unter den ungeprüften Sammeleintrag. Ein Register, dessen größter Eintrag „nicht abschließend geprüft" lautet, deckt genau dort nicht, wo am meisten passiert.

Fairerweise: Dass dieser Zustand überhaupt sichtbar ist, ist eine Stärke. Die meisten Betriebe wüssten es nicht.

**3.4 Die Strategie widerspricht sich bei der Autonomie. — mittel**

Leitprinzip: *„Keine autonome Aktion allein auf Basis ungesicherter Modellantworten."* Stufe A4: *„innerhalb enger Regeln autonom"*. Beides zusammen ist nur haltbar, wenn A4 präzisiert wird zu: **A4 ist deterministischer Code, den eine Regel auslöst; das Modell darf lesen und aufbereiten, aber nie auslösen.** So formuliert ist A4 tragfähig — sonst ist es eine Hintertür.

**3.5 Die Strategie zitiert Gartner gegen sich selbst und merkt es nicht. — mittel**

`04_QUELLEN.md` führt die Reuters/Gartner-Meldung, dass über 40 % der Agentic-AI-Projekte bis 2027 eingestellt werden. Der häufigste Grund ist Überbreite. Das Papier antwortet darauf mit **zehn Agenten in fünf Phasen**. Wer diese Quelle zitiert, muss die eigene Breite begründen — oder reduzieren.

**3.6 Ereignisbus, API-Gateway und Knowledge Graph sind an dieser Stelle Ballast. — mittel**

Ebene B fordert „API-Gateway bzw. kontrollierte Connectoren" und „Ereignisbus oder Workflow-Orchestrierung". Bei einem Betrieb mit einer führenden Datenbank (Supabase), ~113 aktiven Konten und einem dominanten Backend ist ein Ereignisbus **zusätzliche Betriebslast ohne Nutzen**. Postgres + `pg_cron` (schon im Einsatz für `objekt_rollen`) + eine Job-Tabelle decken alles ab, was in 24 Monaten anfällt. Ein Knowledge Graph ist bei diesem Schema schlicht nicht nötig — das relationale Modell *ist* der Graph. Empfehlung: Beides streichen, bis es mindestens drei echte Konsumenten desselben Ereignisses gibt.

**3.7 Die Kalkulations-Priorisierung ist zu hoch angesetzt. — mittel**

Platz 3 der Prioritätenliste hat die **niedrigste Datenreife** im ganzen Portfolio. Das Playbook P2.4 sagt es deutlich: Der Leistungskatalog (`qm_checkliste_vorlagen`, `lk_*`) wird **dreifach bewirtschaftet und ist Owner-los**; einzige Sicherung ist ein `manuell_bearbeitet`-Flag. Ein Kalkulationsagent auf einer Datenbasis ohne Schreib-Owner erzeugt plausible, falsche Preise — der teuerste denkbare Fehlertyp. **Erst Owner, dann Agent.** Und: Grundriss-Vermessung per Vision ist der harte Teil; die LV-Assemblierung aus einer strukturierten Raumliste ist der leichte. Das Papier behandelt beides als ein Vorhaben.

**3.8 Der Einsatzplanungsagent ist regulatorisch unterschätzt. — mittel**

Das Papier schreibt: *„Personalentscheidungen bleiben menschlich."* Das genügt für Annex III Nr. 4 **nicht**. Erfasst sind auch Systeme zur **Aufgabenzuweisung** und zur **Überwachung/Bewertung von Leistung und Verhalten** — unabhängig davon, wer am Ende unterschreibt. Der Bestand ist hier klüger als die Strategie: `einsatzplanung_service.py`, `fluktuation_service.py` und `predictive_wartung_service.py` enthalten **nachweislich keinen KI-Aufruf** (geprüft; `fluktuation_service` ausdrücklich „STRENG nach den DSB-Leitplanken", `predictive_wartung` „rein statistisch … kein Personenbezug/-ranking"). Diese Entscheidung ist richtig und sollte als **Architekturregel festgeschrieben** werden, nicht als Zufall bestehen bleiben.

**3.9 Was in der Strategie fehlt — und im Code auch. — mittel**

Drei Lücken, die keine der zehn Agentenbeschreibungen abdeckt:

1. **Objektbezogene Wirtschaftlichkeit.** Die Kennzahl „Deckungsbeitrag nach Objektstart" steht in §8 — es gibt kein Modul, das sie berechnet. Soll/Ist je Objekt existiert nur segmentweise (`hotel_dienstplan_service`). Damit ist die wichtigste betriebswirtschaftliche Kennzahl der Branche nicht messbar, und die Kalkulationsqualität bleibt unbelegbar.
2. **Kostentransparenz der KI selbst.** 39 KI-Module, kein Modul, das Modellkosten je Funktion erfasst. „Modellrouting nach Risiko, Kosten und Aufgabe" (Ebene C) ist ohne Kostendaten nicht steuerbar.
3. **Ausfallpfad bei Modell-/Regionsausfall.** Der Bestand kennt das Problem bereits — `[L-356]`: `sonnet-4-6` existiert in `europe-west1` nicht, deshalb dort `claude-sonnet-4-5@20250929`. Das Playbook nennt Modell-ID-Hardcodes als Risiko (`claude-opus-4-6` objektbesuch, `claude-sonnet-4-6` leistungskalkulation). Es gibt keinen dokumentierten Herabstufungspfad.

**3.10 Ein Zeitzünder im Deployment. — gering, aber terminiert**

`render.yaml`: *„Das Secret läuft nach 24 Monaten ab — danach steht der Abruf still."* (`GRAPH_CLIENT_SECRET`). Notiert, aber nirgends terminüberwacht. Gehört in die Fristenlogik, die für Fahrzeuge und Unterweisungen längst existiert.

**3.11 Wo der Kritiker der Strategie ausdrücklich recht gibt**

- Die Autonomiestufen A0–A5 sind ein gutes, benutzbares Instrument. A5 dauerhaft zu sperren ist richtig.
- Die Aussage zur digitalen Eigenerklärung („dokumentierte Selbsterklärung, aber allein kein sicherer Identitätsnachweis") ist präzise und wichtiger, als sie im Papier wirkt.
- Der Robotik-Vorbehalt (Vollkosten, Rüstzeiten, Akzeptanz messen) ist richtig und wird durch `arvr_akzeptanz_service.py` bereits methodisch gestützt.
- Die Website-Punkte 3, 8 und 10 (Konsistenz, AEO-Fähigkeit, keine unbelegten Referenzen) sind fachlich einwandfrei.

---

# Teil II — Plenum

## 1. Managementurteil

1. Die Strategie ist inhaltlich solide und in ihren Leitprinzipien richtig, beschreibt aber einen Ausgangszustand, den das Unternehmen vor rund einem Jahr verlassen hat.
2. Alle zehn vorgeschlagenen Agenten existieren bereits ganz oder teilweise; Phase 0 der Roadmap ist im Wesentlichen abgearbeitet (KI-Register, Kartografie, Rollenmodell, DSFA/VVT, Betriebsratsfrage geklärt).
3. Das Unternehmen hat damit keinen Rückstand, sondern einen **Vorsprung** — und das dazugehörige Problem: 117 Module, 366 Routen in einer 17.296-Zeilen-Datei, 39 KI-Funktionen, davon 20 mit offenem Prüfpunkt.
4. **Größte Chance:** die vorhandene Angebotskette (Objektaufnahme → Grundriss → LV → Kalkulation → Cross-Selling) durchzuverbinden. Alle Bausteine liegen, keiner ist verbunden; die Wirkung auf Angebotsdurchlaufzeit und Deckungsbeitrag ist unmittelbar.
5. **Größtes Risiko:** nicht Technik, sondern zwei ungedeckte Rechtsflanken — 139 Bewerbungen mit KI-Passungsbewertung ohne verifizierte Kennzeichnung (Art. 22 DSGVO gilt heute) und ein US-Default für Claude-Textaufrufe, der der eigenen EU-Dokumentation widerspricht.
6. Hinzu kommt ein strukturelles Risiko: Die Wissenskonzentration auf sehr wenige Personen ist bei dieser Systemgröße das eigentliche Ausfallrisiko.
7. Die Roadmap der Strategie ist in der Reihenfolge nicht falsch, aber in der Breite unrealistisch: zehn Agenten in fünf Phasen widersprechen der im eigenen Quellenverzeichnis zitierten Gartner-Warnung.
8. Empfohlen wird deshalb ein **Wechsel des Modus: von Bauen auf Härten, Verbinden und Belegen.**
9. Keine neue Plattform, kein Ereignisbus, kein Knowledge Graph, keine neue Agentengeneration in den nächsten 12 Monaten.
10. **Empfehlung:** drei Züge in dieser Reihenfolge — Rechtsflanken schließen, `main.py` entflechten, Angebotskette schließen. Alles andere wartet.

## 2. Bewertungsmatrix

Skala 1–5. Bei **Risiko** bedeutet 5 = hohes Risiko, bei allen anderen Spalten 5 = am besten.

| Ansatz | Nutzen | Machbarkeit | Datenreife | Risiko | Kosten | Empfehlung |
|---|---:|---:|---:|---:|---:|---|
| Knowledge Brain (`wissenspflege`, `betriebswissen`, `rag_rerank`) | 5 | 5 | 4 | 2 | niedrig | **Behalten** — härten + Goldset messen |
| Reklamations-/Qualitätsagent | 5 | 5 | 4 | 2 | niedrig | **Behalten** — Regelkreis schließen |
| Angebotskette (Aufnahme→Grundriss→LV→Kalkulation) | 5 | 3 | 2 | 3 | mittel | **Teilen** — LV-Owner zuerst, Vision später |
| Learni / Unterweisung (19 Sprachen, VR) | 4 | 5 | 4 | 3 | niedrig | **Behalten** — Nachweiswert rechtlich klären |
| Objektmanager als Cockpit | 5 | 4 | 3 | 3 | mittel | **Verändern** — Sachbezug, keine Personenbewertung |
| Nachweisportal Kunde | 4 | 4 | 3 | 2 | mittel | **Vorziehen** — vor dem Website-Chat |
| Website-Bedarfsberater (Chat) | 3 | 3 | 3 | 4 | mittel | **Verschieben** — nach Nachweisportal |
| Nachhaltigkeitsagent (`umweltaspekte`, CO₂) | 3 | 4 | 3 | 3 | niedrig | **Behalten** — Werbeaussagen belegpflichtig |
| Einsatzplanung | 4 | 3 | 2 | 5 | mittel | **Regelbasiert einfrieren** — kein KI-Ranking von Personen |
| Multimodaler Praxisassistent (`vor_ort`, `lager` CLP) | 4 | 4 | 3 | 4 | niedrig | **Behalten** — Stopp-Regel bei Gefahrstoff härten |
| Bewerber-KI (`bewerbung_mail_service`) | 4 | 4 | 3 | **5** | niedrig | **Sofort absichern oder stilllegen** |
| Video-Doku (`video_doku_service`) | 2 | 3 | 2 | **5** | niedrig | **Einfrieren** bis Neubewertung |
| Robotik / Physical AI | 2 | 2 | 1 | 3 | hoch | **Kein Projekt** — Bewertungskriterium bei Großobjekten |
| Ereignisbus / API-Gateway / Knowledge Graph | 1 | 3 | – | 2 | mittel | **Streichen** für 24 Monate |

**Begründung der Ausreißer.** *Bewerber-KI* und *Video-Doku* stehen auf Risiko 5, weil beide Personenbezug im Beschäftigtenkontext haben, beide vom eigenen Register als Annex-III-Kandidaten geführt werden und beide die Kennzeichnung „PRUEFEN" tragen — bei der Bewerber-KI zusätzlich mit 139 bestehenden Bewertungen. *Einsatzplanung* steht auf 5, obwohl sie heute regelbasiert und damit unkritisch ist: Das Risiko liegt darin, dass eine spätere „kleine Verbesserung" per KI-Vorschlag sie unbemerkt in Annex III Nr. 4 schiebt. *Angebotskette* hat Datenreife 2 wegen des Owner-losen Leistungskatalogs (Playbook P2.4) — der Nutzen ist hoch, die Grundlage trägt aber noch nicht.

## 3. Kritik und Korrekturen

**Falsche oder schwache Annahmen**

| Annahme im Papier | Befund |
|---|---|
| „Vor weiteren Agenten braucht es eine gemeinsame Daten-, Identitäts- und Governance-Schicht." | Richtig — existiert aber bereits teilweise (`objekt_rollen` via `pg_cron`, RLS, KI-Register). Die Aufgabe heißt *vervollständigen*, nicht *schaffen*. |
| „Phase 0: KI-Systeminventar, Datenlandkarte, Rollenkonzept, Risikoklassifizierung (0–3 Monate)" | Weitgehend erledigt. Drei Monate hierfür wären verlorene Zeit. |
| „Gibt es einen Betriebsrat?" (offene Annahme, `05_…`) | Beantwortet: nein. § 87 BetrVG entfällt, Information individuell. |
| „Personalentscheidungen bleiben menschlich" genügt für Einsatzplanung | Genügt nicht für Annex III Nr. 4 (Aufgabenzuweisung, Leistungsüberwachung). |
| Kalkulationsagent als Priorität 3 | Niedrigste Datenreife im Portfolio; Leistungskatalog ohne Schreib-Owner. |
| Robotik als Phase-4-Projekt | Rechnet sich in diesem Objektportfolio absehbar nicht. Als *Bewertungskriterium bei Großobjekt-Ausschreibungen* kostenlos, als Projekt teuer. |
| Implizit: EU-Verarbeitung ist gesetzt | Code-Default ist US; im Blueprint nicht gepinnt. |

**Fehlende Bausteine**

1. Objektbezogene Deckungsbeitragsrechnung — die eigene Leitkennzahl ist nicht berechenbar.
2. Kostentelemetrie je KI-Modul — ohne sie ist „Modellrouting nach Kosten" nicht steuerbar.
3. Dokumentierter Herabstufungspfad bei Modell-/Regionsausfall (`[L-356]` ist der Präzedenzfall).
4. Fristenüberwachung für technische Zugänge (`GRAPH_CLIENT_SECRET`, 24 Monate).
5. Ein Nachfolge-/Vertretungskonzept für die Systemkenntnis. Bei 117 Modulen ist das kein Personalthema, sondern ein Architekturrisiko.
6. Ausschreibungs-/Vergabemonitoring — die einzige echte Lücke in der Vertriebskette; günstig, unkritisch.

**Unnötige Komplexität**

Ereignisbus, API-Gateway als eigene Infrastruktur, Knowledge Graph, Modellrouting über mehrere Anbieter, fünf Architekturebenen als Zielbild. Streichen. Was tatsächlich gebraucht wird: eine Datenbank, ein Backend in Routern, eine geteilte Bibliothek (`zb-shared` — existiert), ein Register (existiert), eine Wache (existiert).

**Widersprüche**

1. „Keine autonome Aktion auf Basis ungesicherter Modellantworten" vs. A4 „innerhalb enger Regeln autonom" → auflösen wie in §4.
2. Gartner-Warnung vor Überbreite zitiert, zehn Agenten geplant.
3. „EU-Default (DSGVO)" dokumentiert, `"direct"` im Code.
4. Website nennt 24 h, 24–48 h und 48 h Reaktionszeit (im Papier korrekt erkannt) — das ist zugleich eine vertragliche Zusage, nicht nur ein Textfehler.

## 4. Empfohlene Zielarchitektur

**Architekturentscheidung: modularer Monolith. Keine Microservices, kein Ereignisbus — für mindestens 24 Monate.**

Begründung: Ein Ereignisbus zahlt sich ab etwa drei unabhängigen Konsumenten desselben Ereignisses und mehreren Teams aus. Beides liegt nicht vor. Microservices würden die Wissenskonzentration verschärfen statt lösen. Der bestehende Monolith ist nicht das Problem — seine **fehlende innere Gliederung** ist es.

**Komponenten (Zielbild 24 Monate)**

```
Kanäle      MA-App (PWA, 19 Sprachen) · Teams · Website · Nachweisportal · Telefon/Service-Bot
              │
Anwendung   EIN FastAPI-Backend, gegliedert in Router je Fachdomäne
            (wissen · qualitaet · objekt · personal · fuhrpark · angebot · nachweis)
            main.py = nur noch Bootstrap + Router-Registrierung
              │
Geteilt     zb-shared: ki_client · mailer · pdf · (neu) ocr · stt · vision · kosten
              │  ── EINZIGE Modellgrenze. Kein direkter Anbieter-Aufruf in Fachmodulen.
Daten       Supabase/Postgres EU · RLS auf objekt_id · pgvector 768 · pg_cron
            Storage: alle PII-Buckets privat + Signed URLs
              │
Modelle     Vertex EU: Claude (europe-west1) · Embeddings (europe-west3) · Gemini
            Direct/US: nur nach ausdrücklicher, dokumentierter Einzelentscheidung
```

**Minimale gemeinsame Datenstruktur** (Prüfauftrag B4). Leitregel: **`objekt_id` ist der Mandanten- und Berechtigungsschlüssel.** Jede Zeile trägt entweder `objekt_id` oder ist ausdrücklich global.

| Entität | Schlüsselfelder |
|---|---|
| `kunde` | kunde_id, name, status |
| `objekt` | **objekt_id**, kunde_id, bezeichnung, adresse, objektart, flaeche_qm, vertrag_von/bis, objektleiter_id, status |
| `raum` | raum_id, objekt_id, bezeichnung, etage, raumart, bodenbelag, flaeche_qm, intervall, → lv_pos_id |
| `lv_position` | lv_pos_id, objekt_id, taetigkeit, frequenz, menge, zeitwert_min, preis, **quelle**, **manuell_bearbeitet** |
| `person` | person_id, typ, sprachen, aktiv_von/bis |
| `objekt_rolle` | person_id, objekt_id, rolle, gueltig_von/bis ← Rückgrat der Berechtigung (existiert) |
| `dokument` | dok_id, quelle, titel, typ, objekt_id?, version, gueltig_von, **gueltig_bis**, freigabe_status, freigeber_id, vertraulichkeit |
| `reklamation` | rek_id, objekt_id, raum_id?, kanal, eingang_ts, kategorie, prioritaet, verantwortlich_id, frist_ts, status, ursache_code, abschluss_evidenz |
| `kontrolle` | kontroll_id, objekt_id, typ, datum, pruefer_id, score, maengel[], fotos[] |
| `schulung` | schulung_id, person_id, thema, typ, datum, ergebnis, nachweis_art, **gueltig_bis** |
| `aufgabe` | aufgabe_id, objekt_id?, quelle_typ+quelle_id, verantwortlich_id, faellig_ts, status, freigabe_erforderlich, freigeber_id |
| `agent_aktion` | aktion_id, modul, ausloeser, werkzeug, ziel_entitaet, vorschlag, freigabe_status, freigeber_id, ts, modell, **kosten**, quellen[] |

`agent_aktion` ist der Baustein, der heute fehlt: **ein Protokoll für alle KI-Aktionen mit Quellen, Freigabe und Kosten.** Es beantwortet in einer Tabelle vier offene Punkte gleichzeitig — Auditpflicht, Kostentransparenz, Halluzinationsmessung und Art.-50-Nachweis.

**RAG, Knowledge Graph, relationale DB, Vektorsuche** (Prüfauftrag B5)

| Technik | Wo | Urteil |
|---|---|---|
| Relationale DB (Postgres) | alle Entitäten oben | **Das Rückgrat.** ~90 % des Werts. |
| Vektorsuche (pgvector, 768) | nur unstrukturierte Dokumente | **Vorhanden und richtig.** Nicht ausweiten. |
| Hybridsuche + Re-Ranking | `rag_rerank.py` — bereits im Einsatz | **Notwendig.** Reine Vektorsuche versagt bei Artikelnummern, Objektnamen, Normbezeichnungen. |
| Knowledge Graph | – | **Nicht nötig.** Das relationale Schema ist der Graph. Frühestens neu bewerten, wenn objektübergreifende Ursachenanalyse ein Produkt wird. |

**Ein harter Zusatz zur Retrieval-Logik:** `gueltig_bis` muss ein **Vorfilter** sein, kein Ranking-Signal. Ein abgelaufenes Sicherheitsdatenblatt als Antwort ist kein Qualitätsmangel, sondern ein Arbeitsschutzvorfall.

**Synchron, asynchron, freigabepflichtig** (Prüfauftrag B7)

| Modus | Was |
|---|---|
| Synchron | Suchen, Anzeigen, Entwurf im geöffneten Dialog (A0–A2) |
| Asynchron | OCR, Embedding, Fotoauswertung, Stapelklassifikation, Nachtberichte, Monitoring |
| Freigabepflichtig | alles, was **das Haus verlässt** (Kundenmail, Angebot, Preis), alles, was **eine Verpflichtung erzeugt** (zugesagte Frist), alles, was **eine Personenakte berührt** (Schulungsstatus, Einsatzzuordnung, Gesprächsprotokoll), und **jedes Schließen einer Reklamation** |

**Autonomie A4, präzisiert:** A4 ist ein deterministischer Codepfad, den eine Regel auslöst. Das Modell darf Eingaben lesen und aufbereiten; es darf nie der auslösende Faktor sein. Damit ist der Widerspruch zum Leitprinzip aufgelöst.

**Schutzmaßnahmen** (Prüfauftrag B8)

| Bedrohung | Maßnahme |
|---|---|
| Prompt Injection | Jedes Dokument, jede Reklamation, jede Kunden-E-Mail, jeder Foto-OCR-Text ist **nicht vertrauenswürdig**. Zweistufig: ein Leseschritt ohne Werkzeuge erzeugt strukturierte Daten; nur strukturierte Daten erreichen den Handlungspfad. Abgerufener Inhalt darf niemals ein Werkzeug auswählen. |
| Tool-Missbrauch | Jedes schreibende Werkzeug prüft `objekt_id` **serverseitig** gegen `objekt_rolle` neu. Keine vom Modell erzeugte ID wird ungeprüft übernommen. Werkzeug-Allowlist je Modul. |
| Datenabfluss | Retrieval-Vorfilter auf `objekt_id` + Rolle; getrennter Index für kundenseitige Agenten; ausgehende Verbindungen des Agentenlaufzeit auf Allowlist; Links/Bilder in kundenseitiger Ausgabe neutralisieren (Exfiltration über Markdown-Bild-URLs). |
| Halluzination | Antwort nur mit Beleg (`dok_id` + Version + `gueltig_bis`); Verweigerung, wenn kein gültiges Dokument über Schwelle; „Weiß ich nicht" ist ein **erwünschtes** Ergebnis und wird im Goldset positiv bewertet; Eskalation an Objektleitung. |
| Veraltete Dokumente | `gueltig_bis` als Vorfilter; Nachtlauf entfernt Abgelaufenes **aus dem Index** und erzeugt eine Prüfaufgabe für den Dokumenteigner. |

## 5. Build-versus-Buy-Entscheidung

| Kriterium | M365/Copilot-zentriert | Eigenbau + API-Modelle (heutiger Stand) | Hybrid (Empfehlung) | On-Prem/Hetzner |
|---|---|---|---|---|
| Kosten | hoch: Lizenz je Kopf über eine überwiegend gewerbliche Belegschaft | niedrig laufend, hoch an Personenkenntnis | niedrig–mittel | mittel Infrastruktur, hoch Betrieb |
| Flexibilität | gering | sehr hoch | hoch | hoch |
| Datenschutz | gut, aber Verarbeitung schwer objektgenau steuerbar | gut, wenn EU-Pfad erzwungen | gut | am besten |
| Vendor-Lock-in | hoch | gering (`ki_client` als Grenze) | gering | keiner |
| Wartung | gering | **hoch — der reale Engpass** | mittel | sehr hoch |
| Time-to-Market | schnell für Generisches, langsam für Fachliches | bereits erreicht | erhalten | langsam |
| Kompetenzbedarf | gering | hoch, heute auf wenige Köpfe konzentriert | hoch, aber teilbar | sehr hoch |

**Empfehlung: Hybrid — und zwar durch Zukauf an genau drei Stellen, sonst unverändert.**

Ein Plattformwechsel würde 117 Module und 39 KI-Funktionen entwerten; das ist ausgeschlossen. Copilot bleibt sinnvoll für die Büro-Belegschaft (Office-Arbeit), ist aber **kein Träger** für objektbezogene Fachlogik: Die Rechte-Trimmung über SharePoint-ACLs bildet das Rollenmodell `person × objekt × rolle` nicht ab. Der bestehende Weg — eigenes Backend, `objekt_rollen` in Postgres, RLS — ist der einzige, der die Fachlogik korrekt trifft.

Zugekauft werden sollte dort, wo Eigenbau nur Wartungslast erzeugt:

1. **Identität** → Microsoft Entra ID als führende Identität für Büro und Leitungsebene (Graph ist bereits angebunden); Supabase Auth bleibt für gewerbliche Beschäftigte ohne M365-Lizenz.
2. **Dokumenten-Ablage** → SharePoint bleibt Quelle der Wahrheit für freigegebene Dokumente; indexiert wird **nur eine kuratierte, ausdrücklich freigegebene Bibliothek** — die vollständigen SharePoint-ACLs zu spiegeln ist der klassische Weg, an dem solche Projekte scheitern.
3. **Betriebliche Absicherung** → externe Bereitschaft/Vertretung für den Systembetrieb. Das ist der wirksamste Einzelkauf gegen das größte Risiko.

**Nicht zukaufen:** Agenten-Frameworks, Vektordatenbanken, Orchestrierungsplattformen. Alles davon existiert bereits im Bestand und funktioniert.

## 6. Review der einzelnen Agenten

| Agent | Urteil | Autonomie | Wichtigste Daten | Größte Risiken |
|---|---|---|---|---|
| **3.1 Knowledge Brain** | **behalten**, härten | A0–A1 | `dokument` mit `gueltig_bis`, `objekt_rolle` | Veraltete Quelle als verbindliche Auskunft; Prompt Injection über hochgeladene Dokumente. **Fehlt: Goldset.** |
| **3.2 Reklamation/Qualität** | **behalten**, Regelkreis schließen | A2 (Entwurf), A4 nur für interne Fristerinnerung | `reklamation`, `kontrolle`, `lv_position` | Schließen ohne Evidenz; Kundenmail ohne Freigabe |
| **3.3 Kalkulation/Angebot** | **teilen und verschieben** | A2 | `lv_position` (**Owner fehlt**), `raum`, Zeitwerte | Plausible Falschpreise auf Owner-loser Katalogbasis (P2.4); Vision-Flächenfehler |
| **3.4 Objektmanager** | **verändern** → Cockpit | A1 | `aufgabe`, `kontrolle`, `reklamation`, `schulung` | Kippt in Leistungsüberwachung, sobald personenbezogen aggregiert wird |
| **3.5 Learni** | **behalten**, Rechtsfrage klären | A1–A2 | `schulung`, Objektmodule, Sprachstände | Nachweiswert der Pflichtunterweisung; Identität bei geteilten Geräten |
| **3.6 Kunden-/Vertriebsagent** | **umsortieren**: Nachweisportal vor Website-Chat | A0–A2 | `nachweis_quoten`, `kontrolle` | Öffentlicher Chat = größte Injection-/Reputationsfläche; Upload fremder Ausschreibungsunterlagen |
| **3.7 Nachhaltigkeit** | **behalten** | A1 | `umweltaspekte`, `fuhrpark_kosten` | **Werbeaussagen**: jede Umweltkennzahl braucht belegte Berechnungsgrundlage und Zeitraum |
| **3.8 Einsatzplanung** | **einfrieren** (regelbasiert) | A0–A1, **kein KI-Ranking von Personen** | Qualifikation, Verfügbarkeit, Entfernung | **Annex III Nr. 4** bei jeder KI-Erweiterung; besondere Kategorien (Krankheit) |
| **3.9 Praxisassistent** | **behalten**, Stopp-Regel härten | A1 | Gefahrstoffkataster, SDB, GBU | Falschauskunft bei Gefahrstoff; SDB-Version veraltet |
| **3.10 Robotik** | **kein Projekt** | – | – | Vollkosten; rechnet sich unterhalb großer zusammenhängender Hartbodenflächen nicht |
| **(neu) Bewerber-KI** | **sofort absichern oder stilllegen** | A1, Entscheidung ausschließlich Mensch | `karriere_bewerbungen` | **Art. 22 DSGVO heute**; 139 bestehende Bewertungen; Kennzeichnung unverifiziert |
| **(neu) Video-Doku** | **einfrieren** | – | – | Video arbeitender Menschen; Annex III Nr. 4b bei jeder Bewertungsfunktion |

## 7. Pilotpläne

Bewusst **keine neuen Agenten** — drei Züge, die Vorhandenes absichern, entflechten und verbinden.

### Pilot 1 · „EU-Pfad und Rechtsflanken schließen"

- **Ziel:** Dokumentierter Anspruch und tatsächliches Verhalten decken sich wieder.
- **Nicht-Ziel:** kein neues Feature, keine Modelländerung, keine UI-Änderung.
- **Nutzergruppen:** GF, DSB (PROXI), Entwicklung.
- **Eingaben:** `ki_register.json`, Render-Konfiguration, `storage.buckets`, Bewerberpool-Bestand.
- **Ausgaben:** (a) `ANTHROPIC_BACKEND=vertex` als Code-Default in `zb_shared/ki_client.py`, `backend/main.py`, `backend/wissenspflege_service.py`, zusätzlich im `render.yaml` gepinnt und beim Start protokolliert; (b) Objektaudit-Vision auf Vertex EU (Playbook P2.2); (c) PII-Buckets privat + Signed URLs (P3.1); (d) Kennzeichnung der Bewerber-KI verifiziert oder Passungsbewertung abgeschaltet und die 139 Bestandsbewertungen bewertet; (e) `video_doku_service` eingefroren; (f) Frist auf `GRAPH_CLIENT_SECRET`.
- **Integrationen:** keine neuen.
- **Autonomiestufe:** entfällt.
- **Freigabepunkte:** DSB-Gegenzeichnung zu (d); GF-Entscheidung zu (e).
- **Akzeptanzkriterien:** kein Produktivpfad ruft ohne dokumentierte Einzelentscheidung ein Modell außerhalb der EU; kein PII-Bucket öffentlich; die Wache meldet 0 Annex-III-Kandidaten ohne verifizierte Kennzeichnung.
- **Evaluationsdatensatz:** Wachen-Lauf vorher/nachher; Bucket-Liste vorher/nachher.
- **Komplexität:** gering–mittel. **Kostenklasse:** niedrig.
- **Abbruchkriterien:** keine — dieser Zug ist nicht verhandelbar. Falls (d) nicht binnen 4 Wochen gutachterlich geklärt ist, gilt die Abschaltung als Vorgabe, nicht als Option.

### Pilot 2 · „`main.py` entflechten — beginnend bei den KI-Aufrufstellen"

- **Ziel:** Aus 17.296 Zeilen mit 366 Routen werden Fachrouter; jede KI-Aufrufstelle erhält einen eigenen Registereintrag.
- **Nicht-Ziel:** kein Umbau der Fachlogik, keine Datenbankmigration, kein Verhaltensunterschied nach außen.
- **Nutzergruppen:** Entwicklung; mittelbar alle.
- **Eingaben:** `main.py`, `ki_register.json`.
- **Ausgaben:** 7 Fachrouter; `main.py` reduziert auf Bootstrap + Registrierung; die 8 KI-Aufrufstellen aus dem Sammelposten einzeln registriert und gekennzeichnet; `agent_aktion`-Tabelle eingeführt und von den herausgelösten Stellen beschrieben.
- **Autonomiestufe:** unverändert je Funktion.
- **Freigabepunkte:** Rauchtest und Deploy-Frage zwischen den Teilzügen (Hausverfahren aus `plenum-restpunkte-plan`).
- **Akzeptanzkriterien:** alle 366 Routen antworten unverändert; Wache meldet 0 „PRUEFEN" im Sammelposten; `agent_aktion` protokolliert jede herausgelöste KI-Aktion mit Quelle, Freigabe und Kosten.
- **Evaluationsdatensatz:** Routen-Inventar vorher/nachher (Pfad, Methode, Statuscode) als automatischer Vergleich.
- **Komplexität:** mittel–hoch. **Kostenklasse:** mittel.
- **Abbruchkriterien:** wenn nach zwei Teilzügen die Routen-Parität nicht automatisch nachweisbar ist → anhalten, Prüfwerkzeug zuerst.

### Pilot 3 · „Angebotskette schließen"

- **Ziel:** Vom Objektbesuch zum belastbaren Angebotsentwurf in einem durchgehenden Vorgang.
- **Nicht-Ziel:** **keine** Grundriss-Vermessung per Vision in diesem Pilot; kein Preis ohne menschliche Freigabe; keine Angebotsversendung durch das System.
- **Nutzergruppen:** Kalkulation, Vertrieb, Objektleitung.
- **Eingaben:** Erstgesprächsaufnahme (`objekt_uebergabe_service`), strukturierte Raumliste, Leistungskatalog, Zeitwerte.
- **Ausgaben:** LV-Entwurf, Personal-/Material-/Maschinenansatz, Plausibilitätsprüfung, Deckungsbeitragsrechnung, Angebotsentwurf als PDF.
- **Datenquellen:** `objekt`, `raum`, `lv_position`, Zeitwerte, `crosssell_service`.
- **Integrationen:** keine externen.
- **Autonomiestufe:** **A2.** Preis und Leistungsversprechen ausschließlich menschlich.
- **Freigabepunkte:** LV-Entwurf durch Kalkulation; Preis durch GF/Vertrieb.
- **Vorbedingung (harte Sperre):** **P2.4 zuerst** — ein Schreib-Owner für den Leistungskatalog (`leistungsverzeichnis_service`), alle anderen Pfade nur lesend. Ohne diesen Schritt startet Pilot 3 nicht.
- **Akzeptanzkriterien:** 20 reale Altangebote nachgerechnet; Abweichung des KI-Entwurfs zum tatsächlich kalkulierten Ansatz **≤ 10 %** im Median; Durchlaufzeit von Besichtigung bis Angebotsentwurf halbiert; jede Position auf eine Katalogquelle rückführbar.
- **Evaluationsdatensatz:** eben diese 20 Altangebote mit bekanntem Ergebnis — und, wo vorhanden, dem tatsächlichen Deckungsbeitrag nach Objektstart.
- **Sicherheit/Datenschutz:** Ausschreibungsunterlagen Dritter sind Fremdgeheimnisse — eigener Bucket, Löschfrist, kein Eingang in den allgemeinen Wissensindex.
- **Komplexität:** mittel. **Kostenklasse:** mittel.
- **Abbruchkriterien:** Medianabweichung > 20 % nach zwei Nachschärfungen → Kette bleibt Werkzeugkasten, kein durchgehender Vorgang.

## 8. Roadmap 0 bis 24 Monate

Geordnet **nach Risiko der Änderung**, nach dem Hausverfahren aus `plenum-restpunkte-plan-2026-08-15.md`.

| Zeitraum | Zug | Ergebnis | Entscheidungstor |
|---|---|---|---|
| **M0–M1** | Pilot 1 · Rechtsflanken | EU-Pfad erzwungen; Buckets privat; Bewerber-KI geklärt; Video-Doku eingefroren | **T1:** DSB zeichnet gegen. Ohne T1 kein weiterer Ausbau. |
| **M1–M2** | Knowledge-Brain-Goldset | 150–300 reale Fragen mit belegter Antwort; Basiswert für Genauigkeit und Quellenabdeckung | **T2:** Quellenabdeckung ≥ 90 %, sonst zuerst Dokumentenpflege |
| **M2–M4** | Pilot 2 · Entflechtung | 7 Fachrouter; `agent_aktion` live; Register ohne Sammelposten | **T3:** Routen-Parität automatisch nachgewiesen |
| **M4–M5** | P2.4 · LV-Schreib-Owner | Ein Owner, alle anderen lesend | **T4 (harte Sperre):** ohne Owner kein Pilot 3 |
| **M5–M8** | Pilot 3 · Angebotskette | Angebotsentwurf aus Objektaufnahme; DB-Rechnung je Objekt | **T5:** Medianabweichung ≤ 10 % gegen 20 Altangebote |
| **M8–M10** | Objekt-Cockpit | Sachbezogene Objektsicht ohne Personenbewertung | **T6:** Datenschutz-Kurzprüfung „kein Personenranking" |
| **M10–M13** | Nachweisportal Kunde | Belegte Qualität als Vertriebsargument | **T7:** 3 Pilotkunden nutzen es aktiv |
| **M13–M16** | P2.1–P2.2 Restkonsolidierung | Ein Dokumenten-Backbone; OCR/STT/Vision als geteilte Libs | **T8:** keine doppelte Pipeline mehr |
| **M16–M20** | Website-Bedarfsberater | Qualifizierter Lead statt Formular | **T9:** Injection-/Missbrauchstest bestanden |
| **M20–M24** | Kostentelemetrie + Modellstrategie | Kosten je KI-Modul; dokumentierter Herabstufungspfad | **T10:** Modellwechsel in ≤ 1 Tag möglich |

**Abhängigkeiten:** T1 → alles. T4 → Pilot 3. Pilot 2 → sinnvolle Kostentelemetrie (ohne Entflechtung ist Zurechnung nicht möglich). Goldset → jede Aussage über Knowledge-Brain-Qualität.

**Was in diesen 24 Monaten bewusst nicht vorkommt:** Ereignisbus, API-Gateway, Knowledge Graph, Robotikpilot, Einsatzplanungs-KI, autonome Stufen oberhalb A4.

## 9. Offene Fragen an Zitzelsberger

Nur Fragen, deren Antwort eine Architektur- oder Investitionsentscheidung verändert.

1. **Steht `ANTHROPIC_BACKEND=vertex` heute in der Render-UI der MA-App — und in jedem anderen Dienst?** Von außen nicht einsehbar. Die Antwort entscheidet, ob Pilot 1 (a) eine Absicherung oder eine Korrektur ist.
2. **Wurden die 139 KI-Passungsbewertungen im Bewerberpool jemals einer Person angezeigt oder in eine Auswahlentscheidung einbezogen?** Entscheidet über Informationspflichten und ggf. Löschung.
3. **Wer wird Schreib-Owner des Leistungskatalogs, und wer darf ihn fachlich ändern?** Ohne benannte Person startet Pilot 3 nicht.
4. **Gibt es objektbezogene Soll-/Ist-Kosten (Stunden, Material) außerhalb des Hotel-Dienstplans — und in welchem System?** Entscheidet, ob die Deckungsbeitragsrechnung eine Anbindung oder eine Neuerfassung ist.
5. **Wie viel Entwicklungskapazität steht 2027 verlässlich zur Verfügung, und wer ist die Vertretung?** Bei 117 Modulen ist das die wichtigste Zahl der ganzen Planung — wichtiger als jedes Budget.
6. **Haben gewerbliche Beschäftigte eine persönliche digitale Identität, oder werden Geräte geteilt?** Entscheidet über den Nachweiswert jeder Unterweisung und über die Durchsetzbarkeit rollenbezogener Rechte.
7. **Besteht eine AVV mit Supabase?** In `docs/rechtlich/README.md` als offen geführt. Betrifft die gesamte Datenhaltung.
8. **Jahresbudget für KI-Betrieb (Modelle, Hosting, externe Bereitschaft)?** Entscheidet über den Zukauf der Betriebsvertretung aus §5.

## 10. Schlussvotum

**Jetzt starten**

1. **Pilot 1 — Rechtsflanken und EU-Pfad.** Höchstes Risiko, geringster Aufwand, keine fachliche Abhängigkeit.
2. **Knowledge-Brain-Goldset.** Ohne Messgrundlage ist jede Aussage über den wichtigsten Agenten unbelegt — auch die positive.
3. **Pilot 2 — `main.py` entflechten.** Der Engpass, hinter dem alles andere klemmt: Register-Vollständigkeit, Kostentransparenz, Vertretbarkeit der Systemkenntnis.

**Später prüfen**

1. **Angebotskette (Pilot 3)** — erst nach dem LV-Schreib-Owner. Hoher Nutzen auf noch nicht tragfähiger Grundlage.
2. **Website-Bedarfsberater** — nach dem Nachweisportal. Ein öffentlicher Chat ist die größte Angriffs- und Reputationsfläche und sollte nicht das erste kundenseitige KI-Erlebnis sein.
3. **Kundenportal als eigenes Produkt** — beginnt als monatlicher belegter Bericht aus vorhandenen Daten. Ein Portal ist ein Produkt, kein Feature.

**Nicht umsetzen bzw. neu denken**

1. **Ereignisbus, API-Gateway als eigene Infrastruktur, Knowledge Graph** — für diese Größe reine Betriebslast. Streichen.
2. **Robotikpilot als Projekt** — stattdessen kostenloses Bewertungskriterium bei Großobjekt-Ausschreibungen.
3. **KI in der Einsatzplanung** — bleibt regelbasiert. Als Architekturregel festschreiben, nicht als Zufall belassen.
4. **`video_doku_service`** — einfrieren bis zur Neubewertung.
5. **Phase 0 der vorgelegten Roadmap** — ist erledigt. Drei Monate dafür wären verlorene Zeit.
6. **Die Zählweise „zehn Agenten"** — sie treibt genau die Zersplitterung, die die Strategie selbst als Hauptrisiko benennt. Besser drei Produkte: **Wissen · Qualität · Steuerung.**

**Nächster konkreter Auftrag an Claude Code**

> **Pilot 1 (a): den EU-Pfad erzwingen statt dokumentieren.**
> `ANTHROPIC_BACKEND` von `"direct"` auf `"vertex"` als Default in `zb_shared/ki_client.py:28`, `backend/main.py:641` und `backend/wissenspflege_service.py:44`; im `render.yaml` ausdrücklich pinnen; beim Start das gewählte Backend und die Region protokollieren; einen Wächter nach dem Muster von `ki_kennzeichnung_wache.py` ergänzen, der jeden Nicht-EU-Pfad meldet. Ein kleiner, prüfbarer, in sich abgeschlossener Zug — und der einzige, der eine dokumentierte Zusage wieder zu einer wahren Aussage macht.

---

### Anhang: Belegstellen

| Aussage | Fundstelle |
|---|---|
| 117 Backend-Module, `main.py` 17.296 Zeilen, 366 Routen | `zitzelsberger-mitarbeiter-app/backend/` |
| 39 KI-Module, 20 offene Prüfpunkte, 2 Annex-III-Kandidaten | `backend/ki_register.json`; Lauf von `scripts/ki_kennzeichnung_wache.py` |
| 139 Bewerbungen mit Passungsbewertung | `ki_register.json` → `bewerbung_mail_service.py`, Feld `begruendung` |
| US-Default für Claude | `zb_shared/ki_client.py:28`, `backend/main.py:641`, `backend/wissenspflege_service.py:44`; `render.yaml` (ohne `ANTHROPIC_BACKEND`) |
| Objektaudit-Vision direct US | `konsolidierung/PHASE-2-3-PLAYBOOK.md` § P2.2 |
| Öffentliche PII-Buckets | ebenda § P3.1 |
| Leistungskatalog ohne Schreib-Owner | ebenda § P2.4 |
| Kein Betriebsrat; DSB PROXI; LfDI BW | `docs/rechtlich/README.md` |
| `objekt_rollen` self-refreshing via `pg_cron */30` | `konsolidierung/PHASE-2-3-PLAYBOOK.md`, Statuszeile Phase 1 |
| Modellverfügbarkeit EU (`[L-356]`) | `zb_shared/ki_client.py`, Kommentar zu `CLAUDE_MODEL_VERTEX` |
| `GRAPH_CLIENT_SECRET` läuft nach 24 Monaten ab | `render.yaml` |
| 113 aktive Konten | `konzepte/plenum-restpunkte-plan-2026-08-15.md` § A2 |

**Vorbehalt.** Regulatorische Aussagen (AI-Act-Fristen, Annex-III-Einstufungen, Art.-50-Pflichten) sind hier auf Basis der im Repository dokumentierten Rechtsstände wiedergegeben und stellen **keine Rechtsberatung** dar. Vor Produktivbetrieb sind sie mit dem Datenschutzbeauftragten und, für die Beschäftigtenthemen, arbeitsrechtlich zu prüfen — insbesondere Punkt 2 der offenen Fragen.
