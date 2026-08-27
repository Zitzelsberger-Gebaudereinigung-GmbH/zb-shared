# LEARNI OS — Konzeptreview

**Gegenstand:** `LEARNI_OS_Claude_Code_Uebergabepaket.zip` (CLAUDE_CODE_HANDOFF.md + prototype.html), erstellt mit ChatGPT Work.
**Verfahren:** Analyse → Walt-Disney-Methode (Träumer → Realisierer → Kritiker) → Plenum mit sechs Stakeholder-Rollen.
**Zielvorgabe des Auftraggebers:** „das innovativste KI-unterstützteste Learning Management System, welches eine einzigartige Employee Journey auslöst."
**Stand:** 2026-08-27

---

## 0. Kurzfassung

Das Konzept ist **handwerklich das beste ChatGPT-Ergebnis, das man zu diesem Thema erwarten kann** — und trotzdem als Bauauftrag nicht tragfähig. Es ist ein *Systemarchitektur-Dokument*, kein Produkt- und kein Lernkonzept.

Was es richtig macht:

- Die Leitidee ist exakt richtig: nicht „welche Kurse wurden abgeschlossen", sondern „welche Tätigkeit kann jemand nachweisbar sicher ausführen".
- Es benennt selbst die schwächste Stelle (Canvas-Unterschrift ≠ Identitätsnachweis) statt sie zu verschweigen.
- Der serverseitige Assessment-Lock, die Content-Versionierung und die Trennung der drei Übersetzungsebenen (UI-i18n / redaktionelle Freigabe / KI-on-demand) sind ernsthafte, richtige Entscheidungen.
- Die Negativliste („nicht im MVP": Gesichtserkennung, Emotionserkennung, Webcam-Proctoring, HR-Rankings) ist gut und sollte unverändert bleiben.

Was fehlt — und zwar vollständig, nicht ansatzweise:

| Lücke | Konsequenz |
|---|---|
| **Kein Business Case.** 236 Zeilen Architektur, kein Euro. | Kein Gate, kein Abbruchkriterium, keine Nutzenmessung. |
| **Kein Betriebsrat, keine Mitbestimmung.** §87 BetrVG kommt einmal vor — als „juristisch prüfen". §94, §95, §98 gar nicht. | Das mitbestimmungspflichtigste Element des Konzepts ist eine Fußnote. Stilllegungsrisiko nach Launch. |
| **Keine Rolle für die Objektleitung im MVP.** Sie ist in der Rollenliste, hat aber in der Definition of Done keine einzige Funktion. | Das MVP ist für die Person unbenutzbar, die es einführen muss. |
| **Kein Lernkonzept.** „Praxischeck", „Szenarien", „Praxisnachweise" sind Aufzählungswörter ohne Entsprechung im Datenmodell. | Der Vertical Slice endet bei Quiz → Signatur → Skill und produziert damit exakt das, was das Konzept ablehnt: eine Completion mit besserem Audit-Trail. |
| **Kein Content-Plan.** „Trainer/Content Author" wird als vorhandene Rolle vorausgesetzt. | Es gibt diese Rolle im Unternehmen nicht und wird sie nicht geben. Content ist der eigentliche Engpass — und der größte Kostenblock. |
| **Keine Migration.** „Import aus dem bestehenden LMS" ist ein Satz. | Laufende Zertifikate, Nachweishistorie und Videobestand aus Memberspot sind ungeklärt. |
| **Der Prototyp ist nicht mobile-first.** `<850px` blendet die Sidebar per `display:none` aus, ohne mobilen Ersatz. | Auf dem Handy — dem einzigen realen Endgerät der Zielgruppe — ist keine Navigation erreichbar. |

Und der zentrale sachliche Fehler:

> **§14 Abs. 2 GefStoffV und §14 Abs. 2 BioStoffV verlangen eine mündliche, arbeitsplatzbezogene Unterweisung vor Aufnahme der Tätigkeit und danach mindestens jährlich. Reines E-Learning erfüllt das nicht.**

Für ein Gebäudereinigungsunternehmen — Gefahrstoffe, Infektionsschutz — ist das kein Detail, sondern die Geschäftsgrundlage. Ein System, das die Unterweisung *ersetzen* will, ist rechtswidrig. Ein System, das die mündliche Unterweisung *dokumentiert, vorbereitet und mehrsprachig unterstützt*, ist wertvoll. Das Konzept baut das erste.

---

## 1. Die Sprachauswahl ist falsch

Das Konzept nennt **DE / EN / FR / PL**. Das ist die Sprachliste einer Software-Roadmap, nicht die einer deutschen Gebäudereinigung. Realistisch relevant sind je nach Region Türkisch, Rumänisch, Polnisch, Bulgarisch, Arabisch, Ukrainisch/Russisch, Bosnisch-Kroatisch-Serbisch, Kurmandschi, Albanisch, Vietnamesisch. Französisch ist praktisch irrelevant.

Zwei Konsequenzen:

1. **Die Sprachliste ist eine Datenfrage an die Personalabteilung, keine Designentscheidung.** Das System muss beliebige Locales aufnehmen können statt vier fest zu verdrahten.
2. **„Einfache Sprache" ist keine vierte Übersetzung, sondern ein eigenes Register.** Im Datenmodell braucht es `register (standard|einfach)` als eigene Dimension **neben** `locale` — sonst gibt es kein „Türkisch, einfach". Und Einfache Sprache ist das *Ausgangsregister des Masters*; nachträgliches Vereinfachen erzeugt schlechtes Deutsch.

Dazu kommt funktionaler Analphabetismus, im Reinigungsgewerbe deutlich über dem Durchschnitt und häufig auch in der Erstsprache. Übersetzung allein löst das nicht. Nötig ist **Audio-First als Pflicht**: jede sicherheitskritische Einheit vertont je Locale, Fragen werden vorgelesen, Antwortoptionen als Bild oder Piktogramm, kein Freitext als Bestehensvoraussetzung.

---

## 2. Walt-Disney-Runde

### 2.1 Träumer — was dem Konzept zur Einzigartigkeit fehlt

Das Konzept beschreibt perfekt, **wie Wissen verwaltet wird**. Es beschreibt nicht, **wie sich ein Mensch dabei fühlt**, der um 5:20 Uhr allein im Treppenhaus steht, dessen Deutsch für Formulare nicht reicht und der noch nie ein Zertifikat mit seinem Namen darauf besessen hat.

Fünf fehlende Dimensionen: **Würde statt Compliance · Stimme statt Text · das Objekt als Klassenzimmer · Stolz, der nach Hause geht · ein sichtbarer Weg nach oben.**

Die Journey, die daraus folgt:

| Zeitpunkt | Was passiert | Was der Mensch fühlt |
|---|---|---|
| **Tag −1** | Zwei Stunden nach Vertragsunterschrift eine Nachricht in der Muttersprache: Foto des Objekts, Foto und Name der Objektleitung, Uhrzeit, wo der Schlüssel liegt. Kein Passwort. | *Ich werde erwartet. Man hat an mich gedacht.* |
| **Tag 1** | QR am Putzwagen → 90 Sekunden gesprochen: „Das ist dein Wagen. Das ist Chemie — nie mit dem grünen Tuch mischen." Sprachnachricht der Patin in derselben Sprache. | *Ich bin nicht allein. Ich blamiere mich nicht.* |
| **Tag 30** | Elf Mikro-Einheiten, alle im Objekt, alle unter drei Minuten, alle per Sprache. QualiCheck grün: „Du hast das sicher gezeigt — nicht im Test, in echt." | *Ich bin gut in dem, was ich tue.* |
| **Tag 90** | Gedrucktes, zweisprachiges Können-Zeugnis per Post, unterschrieben von der Geschäftsführung. | *Ich zeige das meiner Mutter.* |
| **Jahr 1** | Sichtbarer Karrierepfad, drei fehlende Fähigkeiten benannt, begleitete Schattenwoche als Praxisnachweis. | *Hier ist mehr für mich drin als Putzen.* |
| **Abgang** | Nachweise bleiben gültig und sind mitnehmbar. „Die Tür bleibt offen." | Rückkehrer statt Neueinstellung. |

Zwölf benannte Ideen: **Learni Ruft An · Objektfunk · Zeig's mir · Der Stolzbrief · Sanfte Schleife · Kann-Ich-Karte · Danke-Wand · Sprachbrücke · Schichtbegleiter · Vom Wagen zum Schlüssel · Schattenwoche · Erste-Woche-Pate.**

Der Wow-Moment ist nicht VR. Er ist der Satz am Küchentisch: **„Die haben mich angerufen. In meiner Sprache. Bevor ich überhaupt angefangen habe."**

### 2.2 Realisierer — der eine Weg

**Entscheidung: Kauf-LMS als Content-/Player-Layer + Eigenbau der Nachweis- und KI-Schicht als eigener Dienst `zb-lernen` (Python/FastAPI + Postgres/pgvector + `zb-shared`). Kein Next.js, kein Supabase.**

Begründung in der Reihenfolge der Wichtigkeit:

1. **Der selbstgebaute Teil ist in beiden Welten identisch.** Nachweis, Objektbezug, Praxischeck, Learni — das baut man so oder so selbst. Also baut man es zuerst und kauft den austauschbaren Rest. Findet der Marktabgleich kein LMS mit brauchbarer API, wächst derselbe Dienst um einen einfachen Player (Audio/Text/Quiz). Die Entscheidung ist damit **umkehrbar ohne Wegwerfarbeit**.
2. **Ein Entwickler, eine Sprache.** `zb-shared` in TypeScript nachzubauen — EU-Vertex-Default, Modell-Registry inklusive der `sonnet-4-5@20250929`-Falle in `europe-west1`, Creds-Bootstrap, `mailer`, `pdf` — wäre exakt das Copy-Paste-Problem, das `[d-303]` gerade beseitigt hat, nur diesmal sprachübergreifend und damit unheilbar. Bus-Faktor 0,5 ist bei einem System, das Rechtsnachweise erzeugt, inakzeptabel.
3. **RLS entfällt als zweites Autorisierungsmodell.** Supabases Hauptargument trägt hier nicht: Das Konzept fordert selbst serverseitige Durchsetzung für Assessment-Lock, RAG-Autorisierung, Signatur und Audit — also läuft ohnehin alles durch ein BFF. Dann ist RLS eine zweite, redundante Regelbasis, die man synchron halten muss. Ein Mandant, drei Rollen (Learner / Objektleitung / Admin+Auditor read-only) statt 35 Tabellen × 6 Rollen.
4. **Größenordnung.** 80–150 T€ Nutzen pro Jahr tragen keine Plattform für 700 T€–1,2 Mio €. Sie tragen 2–4 Personenmonate.

```
Handy (PWA, offline-fähig, audio-first)      QR/NFC am Objekt
        |                                            |
   zb-lernen (FastAPI) — Nachweis · Objekt · Skill · Praxischeck · Learni-Gateway
        |          \__ Webhook/Poll ──> Kauf-LMS (Player, Video, Completion)
        |          \__ Events <──────── Reklamation · QualiCheck · Objektaudit · MA-App
        |
 Postgres + pgvector  (Nachweisdaten und Verhaltensdaten strikt getrennt) · Object Storage
        |
   zb-shared (Vertex EU Claude · Embeddings · mailer · pdf)   — Richtung nur: LMS → zb-shared
```

Eigenes Repository, `zb-shared` per Git-Tag gepinnt. Medien werden nie selbst transcodiert (Cloudflare Stream / Mux). Der Personalstamm ist die Quelle der Wahrheit für Person, Sprache und Objektzuordnung.

#### Der korrigierte Vertical Slice: „Die grüne Objektmappe"

Der Slice aus dem Konzept (Login → Kurs → Learni-Frage → Assessment → Lock → Quiz → Selbsterklärung → Signatur → Skill) braucht erst Content, erzeugt am Ende eine Completion und enthält die Objektleitung überhaupt nicht. Der korrigierte Slice **braucht null Content, ersetzt am ersten Tag die Papier-Unterweisungsliste und ist GefStoffV-konform, weil er die mündliche Unterweisung dokumentiert statt sie zu ersetzen**:

1. Objektleitung öffnet die App → **Ampel über ihre Objekte** (rot = jemand ohne gültigen Nachweis ist eingeplant).
2. Objekt antippen → **„Wer darf heute hier arbeiten?"** — Ja/Nein je Person, Grund im Klartext.
3. **„Unterweisung durchführen"** → objektspezifischer Baustein (Schlüsselordnung, Alarm, Gefahrstoffe *dieses* Objekts) → Sprechzettel in Einfacher Sprache; die Objektleitung spricht mündlich vor der Gruppe.
4. Teilnehmer **scannen den QR am Putzwagen** → Login per Handynummer + OTP, kein Passwort; neue Person legt sich per QR selbst an, Abgleich gegen den Personalstamm.
5. **Drei Verständnisfragen, vorgelesen in der Stammsprache**, Antworten als Bild/Piktogramm, unbegrenzte Versuche, Ergebnis nur bestanden/nicht bestanden.
6. **Quittierung**: Selbsterklärung in der eigenen Sprache, personalisierter Account + Zeitstempel. **Keine Canvas-Unterschrift.**
7. **Praxischeck**: Beobachtung an einem Kriterienbogen (5–8 Verhaltensanker, K.-o.-Kriterien für PSA und Gefahrstoffe), offline, unter drei Minuten.
8. **`learner_skills` wird gesetzt** — ein Quiz allein erreicht maximal `weiß`; `kann selbstständig ausführen` ist **nur** über den Beobachtungsnachweis erreichbar. Datenbank-Constraint, kein Feature.
9. **Nachweis-PDF**, versionsgebunden, hash-verkettet, mit ausgewiesener Unterweisungssprache — auf Knopfdruck je Objekt.
10. **Auditor-Link**, read-only, mit Ablaufdatum.
11. **Lernzeit-Export** für die Lohnbuchhaltung (Lernzeit ist Arbeitszeit).

Learni kommt in diesem Slice **noch gar nicht vor**. Er kommt danach — zuerst als **Autoren-Copilot** für Schritt 3, weil sein ROI dort am größten ist.

#### Datenmodell-Deltas gegenüber dem Konzept

**Neu:** `observation_definitions`, `observation_criteria` (`critical bool`), `observation_sessions`, `observation_ratings`, `observer_qualifications`; `location_briefing_blocks` (objektspezifische Bausteine — `locations` allein reicht nicht, das ist der eigentliche Kern); `briefing_sessions` + `briefing_attendance` (mündliche Unterweisung, `delivery_mode = oral|blended`); `learning_time_entries`; `evidence_chain` (`prev_hash`, `payload_hash`, qualifizierter Zeitstempel); `person_languages` (Stammsprache **und nachgewiesene Unterweisungssprache**, Pflichtfeld); `assignments` (n:m Person↔Objekt für Springer) mit Funktion `may_work_at(person, location, date)`; `imported_credentials` (Altnachweise mit ursprünglichem Ablaufdatum); `assessment_invalidations` (fehlerhafte Frage nach 200 bestandenen Prüfungen — ohne Korrekturpolicy ist der Nachweis wertlos).

**Geändert:** `translations` bekommt `register (standard|einfach)` neben `locale`. `learner_skills` bekommt `evidence_type (knowledge|observation|both)`, `valid_until` und `level (angeleitet|selbstständig|kann_anleiten)`. `learning_events` ohne Sekundengranularität, Rohdaten ≤ 90 Tage. `ai_messages` Default 30 Tage, kein Klartextzugriff für Manager oder Admin. Locale-Liste offen statt Enum. `signature_evidence` → Methode `account+otp`, Canvas raus.

**Gestrichen:** `organizations` und alle Tenant-Spalten (es gibt ein Unternehmen — Multi-Tenant-RLS-Tests testen Fiktion), `credentials` nach Open Badges/CLR, `immersive_activity` und XR-Events, `roles`/`permissions` als Tabellen.

#### Was von den zwölf Träumer-Ideen übrig bleibt

| Idee | Realisierbarer Kern | Aufwand | Gestrichen |
|---|---|---|---|
| Learni Ruft An | Kein Anruf — **Nachricht am Tag −1** mit Objektfoto, Foto und Name der Objektleitung, Treffpunkt, Uhrzeit, in der Stammsprache mit Vorlese-Button | S | Telefonie-Stack, Voice-in, Dialog |
| Objektfunk | QR am Putzwagen → 60–120 s Audio + Bild, objektgenau. **Stärkster Hebel überhaupt** | M | NFC vorerst |
| Zeig's mir | Nur als **Autorenwerkzeug der Objektleitung**: Foto + Sprachnotiz → KI baut Text, Einfache Sprache, Übersetzung, drei Prüffragen → Freigabe durch die Objektleitung | M | Mitarbeiter-Upload, Schnitt-Pipeline, Auto-Publish |
| Der Stolzbrief | Unverändert bauen — aus `zb_shared.pdf` + `mailer` + Druckdienstleister. Billigste Wirkung im ganzen Projekt | S | NFC-Karte |
| Sanfte Schleife | Auditbefund/Reklamationsgrund → Skill-Mapping → 90-s-Lektion mit Frist; geschlossen erst beim nächsten grünen Check | M | Automatik ohne Bestätigung; **Bewertung und Sanktion ausgeschlossen** |
| Kann-Ich-Karte | Piktogramm-Wallet mit drei Stufen und Verhaltensankern statt „Skill Level 12" | S | Prozentbalken |
| Danke-Wand | Ein-Klick-Glückwunsch der Objektleitung per Push — das wirkt, die Wand nicht | S | Wand, Feed |
| Sprachbrücke | 40 Alltagssätze als Audio-Deck, freiwillig, ohne Messung | S | Aussprachebewertung (Art. 9 DSGVO) |
| Schichtbegleiter | 60-Sekunden-Retrieval vor Schichtbeginn | M | **Streaks**, Push in die Freizeit |
| Vom Wagen zum Schlüssel | Statische Landkarte mit vier Stationen + „Ich interessiere mich"-Button an HR | S | Matching-Algorithmus (AI Act Anhang III) |
| Schattenwoche | Als Beobachtungsnachweis-Typ; organisatorisch durch HR getragen | S | Eigene Software |
| Erste-Woche-Pate | Buddy-Feld + Skill „Anleiten" + Beobachterrolle | M | Matching-Algorithmus |

#### 90 Tage

| Block | Wochen | Wer | Inhalt |
|---|---|---|---|
| **A — Bestandssicherung** ⚠️ kritischer Pfad | 1–4 | GF / Recht | Memberspot-Kündigung stoppen oder überbrücken · **Vollexport** Inhalte + Nachweisdaten · **Nullmessung** (gezahlte Lernstunden, Nachweislücke an 50-MA-Stichprobe) · Repo, Cloud, Domains, Secrets auf Firmen-Accounts · BR-Erstgespräch · DSFA-Start · AI-Act-Rollenklärung |
| **B — Slice bauen** | 3–8 | Entwicklung | W3–4 Objekt-Ampel + `may_work_at` · W5–6 Briefing-Erfassung, QR-Selfservice, vorgelesene Fragen · W7–8 Praxischeck offline, Hashkette, Nachweis-PDF, Auditor-Link, Lernzeit-Export |
| **B′ — Betriebsvereinbarung** ⚠️ kritischer Pfad | 3–8+ | Recht / BR | Zweckkatalog mit ausdrücklichem Verbot der Leistungskontrolle · Datenkatalog je Tabelle · Reportliste mit Mindestaggregation n ≥ 5 · §94 Abs. 2 für die Skill-Matrix. **Kein Pilot mit echten Daten vor Abschluss.** |
| **B″ — Content** | 3–10 | L&D | 10 objektspezifische Bausteine für zwei Pilotobjekte; DE-Master + **eine** geprüfte Zweitsprache + Einfache Sprache |
| **C — Marktabgleich** (nicht kritisch) | 6–10 | GF / L&D | Kauf-LMS-Shortlist. Einziges Kriterium: **API, Webhooks, SSO, Export** — nicht die UI. Abbruchregel: erfüllt ein Standardprodukt ≥ 85 % der Muss-Liste zu ≤ 50 T€/Jahr, wird nur `zb-lernen` gebaut |
| **D — Pilot** | 9–13 | alle | Zwei Objekte, 60–80 Mitarbeitende, **Parallelbetrieb Papier**. Abbruch bei Nachweisquote < 90 %. Erst hier Learni als Autoren-Copilot |

Nicht auf dem kritischen Pfad: LMS-Auswahl, Learni/RAG, Stolzbrief, Sprachbrücke, Karrierepfad, Migration der Altzertifikate.

#### Die drei Dinge, die den Unterschied machen

1. **Der objektgenaue Nachweis** — „Darf diese Person heute in diesem Objekt arbeiten?", hash-verkettet, mit Sprachnachweis, Auditor-Link auf Knopfdruck. Das kauft man nirgends, weil es Schulung mit Objekt, Rolle und QM verknüpft — und genau das steht in Ausschreibungen. *~1,5 PM Entwicklung, ~15 T€ Recht.*
2. **Der Praxischeck als einzige Tür zu „kann selbstständig"** — mit dem Constraint, dass ein Quiz das nie erreicht. Das ist der Unterschied zwischen einer Completion und einer Kompetenzaussage, und er kostet fast nichts. *~1 PM + Beobachterschulung ~5 T€.*
3. **Audio-first in der eigenen Sprache, Einfache Sprache als eigenes Register** — vorgelesene Fragen, Piktogramm-Antworten, QR am Wagen, Nachricht am Tag −1. Das erreicht die Menschen, die heute niemand erreicht. *~1,5 PM Entwicklung, Übersetzung und Redaktion 25–40 T€ pro Jahr — der eigentliche Dauerposten.*

**Jahr 1 gesamt: ~4 Personenmonate Entwicklung, 30–50 T€ Recht/BR, 80–150 T€ Content.**

### 2.3 Kritiker — elf Bruchstellen und was sie schließt

| # | Was bricht | Wann | Was es schließt |
|---|---|---|---|
| **L1** | **Die Objektleitung ist Erfüllungsgehilfin, nicht Kundin.** Sie bekommt Ampel, Sprechzettel, Praxischeck, Freigaben — lauter Mehrarbeit — und ihren Gegenwert erst am Ende derselben Kette. Die einzige sichtbare Wirkung des Systems ist, dass es ihr Versagen dokumentiert. | Pilot, W9–13 | Reihenfolge umdrehen: zuerst ausliefern, was am Tag 1 Zeit spart (Papierliste weg, Nachweis-PDF und Auditor-Link auf Knopfdruck), erst danach etwas verlangen. Pilot nur mit **freiwilligen** Objektleitungen. Erfassungsminuten im Objektbudget hinterlegen. Abbruchkriterium ist nicht die Abschlussquote der Mitarbeiter, sondern **Beobachtungen je Objektleitung je Woche**. |
| **L2** | **Die Ampel ist am Tag 1 zu 100 % rot.** Die Migration steht unter „nicht kritischer Pfad" — ohne Nachweishistorie zeigt die Ampel keine Realität, sondern eine leere Datenbank. Alarmmüdigkeit in Woche eins. | W3–4 | Migration der laufenden Nachweise ist **Vorbedingung** der Ampel, nicht Nachlauf. Dritter Zustand **„grau = unbekannt"** mit Einführungsfrist je Objekt. Rot erst, wenn Rot etwas bedeutet. |
| **L3** | **`may_work_at` ist genau die Funktion, bei der der Betriebsrat stoppt.** „Darf diese Person heute hier arbeiten?" ist Einsatzsteuerung: §95 BetrVG, §94 Abs. 2, AI Act Anhang III Nr. 4. | BV-Verhandlung | Rein deterministisch — kein Modell, kein Score, keine Rangfolge, keine Empfehlung. Ausgabe ausschließlich **„Unterweisung X fehlt seit TT.MM."** statt „darf nicht". Regelliste als BV-Anlage. Keine Kopplung an den Dienstplan, kein Blocking. **Der Mensch entscheidet, das System erinnert.** |
| **L4** | **SMS-OTP funktioniert genau dort nicht, wo gereinigt wird.** Kein Netz im Tiefgeschoss. Die Nummer beweist Gerätebesitz, nicht Identität — bei Prepaid, geteilten Familiengeräten und ~200 Nummernwechseln p. a. trägt sie keinen Rechtsnachweis. Angeordnete Privatgerätenutzung ist mitbestimmungspflichtig und nicht durchsetzbar. | ab W5 | Identität **einmalig durch die Objektleitung feststellen** (Enrollment im Beisein, protokolliert — *das* ist der Identitätsanker, nicht die SMS), danach langlebiger Gerätetoken + PIN; OTP nur bei Gerätewechsel, Reset nie im Selfservice. Geteiltes Gerät als expliziter Modus mit kurzer Session. Pflicht-Fallback: **Tablet der Objektleitung im Kiosk-Modus**, Quittierung per persönlicher PIN. SMS-Kosten (~500–700 €/Jahr) sind irrelevant; Netzabdeckung und Identitätsbindung sind es nicht. |
| **L5** | **„Personalstamm ist Quelle der Wahrheit" ist eine unbelegte Annahme.** Selbst wenn ein Lohnsystem exportiert: **Stammsprache steht dort mit ziemlicher Sicherheit nicht drin, Objektzuordnung meistens auch nicht** — die lebt im Dienstplan oder im Kopf der Objektleitung. Das sind genau die zwei Felder, die der Slice am dringendsten braucht. | W1–2, kritischer Pfad | In Woche 1 verbindlich feststellen: welches System, welches Exportformat, welche Felder real vorhanden. Realistisch: Personalnummer, Name, Ein-/Austritt aus dem Stamm (Nightly-Export, Matching-Report, **nie** Auto-Löschung); `person_languages` und `assignments` werden in `zb-lernen` gepflegt — mit Pflege-UI, Verantwortlichem, budgetiertem Aufwand. Wichtigstes Feld überhaupt: **das Austrittssignal**, sonst gibt es kein Löschkonzept. |
| **L6** | **Offline-Erfassung und qualifizierter Zeitstempel widersprechen sich.** Der Zeitstempel bezeugt den Server-Eingang. `offline_captured_at` ist eine Client-Behauptung mit manipulierbarer Gerätezeit. Stehen beide gleichrangig im PDF, ist der Nachweis angreifbarer als Papier. | erster Streitfall | Kette und Zeitstempel binden **ausschließlich** `server_received_at`. `offline_captured_at` im PDF als „vom Gerät angegeben" kennzeichnen. Gerätezeit-Drift beim Sync messen und mitloggen. Maximale Offline-Latenz 72 h, danach Upload nur mit Begründung und Kennzeichnung „verspätet". Trennlinie halten: **Beobachtung durch Dritte offline ja, Selbst-Quiz offline nein.** |
| **L7** | **Der Praxischeck ist eine Beurteilung ohne Gegenzeichnung.** Fünf bis acht Verhaltensanker mit K.-o.-Kriterien, erfasst über den Kopf des Beschäftigten hinweg (§§82/83 BetrVG, §94 Abs. 2). | erster Widerspruch | Learner-Quittierung „zur Kenntnis genommen" **plus Freitext-Widerspruchsvermerk** als Pflichtschritt der Session. Kostet 20 Minuten Entwicklung und rettet die Konstruktion. |
| **L8** | **„~1,5 PM für einen eigenen Player" ist eine Beruhigungspille.** 1,5 PM decken Text, Audio und MC-Fragen. Nicht gedeckt: das Autorenwerkzeug (und es gibt keinen Vollzeit-Autor), Versionierung mit Korrekturpolicy, Register × Locale über alles, Piktogramm-Antworten, Medienauslieferung, WCAG. Realistisch **3–4 PM ohne Video**. | wenn Gate 1 kein passendes LMS findet — der wahrscheinliche Fall | Umkehrbarkeit nicht behaupten, sondern erzwingen: **`ContentSource`-Adapter mit genau vier Operationen** (Kurse listen, Version auflösen, Completion-Event, Deep-Link) ab Tag 1, alles andere hinter dieser Kante. Ehrliche Formulierung an die Geschäftsführung: „Kein passendes LMS kostet uns ein Quartal, nicht das Projekt." Die tragende Hälfte der These stimmt — die Nachweisschicht ist in beiden Welten identisch. |
| **L9** | **4 PM sind Feature-Zeit, nicht Projektzeit.** Nicht enthalten: Personalstamm-Sync und Matching, Enrollment/Auth/Gerätehandling, Nachweis-Migration, Admin- und Pflege-UI, Offline-Sync-Konfliktauflösung, Betrieb/Monitoring/Backup-Restore-Test, Tests und Betriebsdoku, Zuarbeit zu DSFA und BV. Realistisch **7–9 PM** — bei einem Entwickler 7–9 Kalendermonate. | ab W6, schleichend | Entweder Scope halbieren (Phase 1 = Ampel, Briefing, Quittierung, Nachweis-PDF; Praxischeck und Lernzeit-Export in Phase 2) oder die Zeitachse verdoppeln und das offen sagen. Der Plan heißt dann **„90 Tage bis Pilotreife der grünen Objektmappe"**, nicht „90 Tage bis fertig". |
| **L10** | **Die BV kollidiert frontal mit Woche 9.** Eine Voll-BV über §87 I Nr. 6, §94 II, §95 und §98 plus DSFA plus ggf. Sachverständiger nach §80 III braucht erfahrungsgemäß 4–9 Monate. Der Plan erzeugt in Woche 9 exakt den Druck, „nur mal kurz mit echten Daten" zu testen — der dokumentierte Sofort-Stopp-Trigger des Betriebsrats. | W9 | Zwei Stufen: eine **befristete Erprobungsvereinbarung** (zwei Objekte, benannte Zwecke, Löschzusage nach Pilotende, keine personenbezogene Auswertung, Beweisverwertungsverbot) ist in 4–6 Wochen verhandelbar; die Voll-BV läuft parallel weiter. BR-Erstgespräch in **Woche 1**, mit dem Angebot der gemeinsamen Zweckdefinition. Bis zur Unterschrift: Testdaten. |
| **L11** | **Learni ab Woche 9 ist inhaltlich richtig und haftungsseitig ungesichert.** Ein KI-erzeugter Sprechzettel mit falscher PSA-Angabe wird zum Nachweis. Einziger vorgesehener Schutz ist die Freigabe durch die Objektleitung — die Gefahrstofffachtexte nicht validieren kann. | erster Gefahrstoff-Sprechzettel | Entwürfe nur aus freigegebenen Quellen (Betriebsanweisung, Sicherheitsdatenblatt) **mit Quellenangabe je Aussage**. Zwei-Augen-Freigabe für Gefahrstoff- und PSA-Inhalte durch die Fachkraft für Arbeitssicherheit. `generated_by_ai` und `approved_by` an jedem Block, im Audit sichtbar. Und der fehlende **Widerruf**: ein hash-verkettetes PDF, das man nicht zurückrufen kann, ist bei fehlerhaftem Inhalt ein Haftungsrisiko — Revocation als eigener Kettenblock, Verifikations-QR auf jedem Nachweis. |

**Nebenbefund:** `learning_time_entries` plus Lohnexport erzeugen im ersten Lohnlauf eine sichtbare, potenziell rückwirkende Lernzeitforderung. Das ist eine Entscheidung der Geschäftsführung **vor** Rollout, keine Überraschung danach.

#### Der ehrliche Widerspruch

Der Auftrag lautet „innovativstes KI-unterstütztes LMS". Geliefert wird im Kern ein digitales Unterweisungs-Nachweissystem. Ist das Verrat am Ziel?

**Nein — aber der Plan trägt den falschen Namen.** „Digitales Unterweisungs-Nachweissystem" beschreibt das Artefakt, nicht die Innovation. Die Innovation ist die **Frage**, die das System als erstes beantwortet:

> *Darf diese Person heute in diesem Objekt arbeiten — und kann sie es nachweislich?*

Kein LMS am Markt beantwortet das, weil kein LMS Objekt, Rolle, Sprache und Beobachtung zugleich kennt. Eine Kursbibliothek ist Massenware und wird zugekauft. Der Rest ist einzigartig. Und eine Employee Journey, die mit einem Kurskatalog beginnt, ist keine — die hier beschriebene beginnt damit, dass jemand in seiner Sprache angesprochen wird, **bevor** er den ersten Tag arbeitet. Das ist die Vision des Träumers, unverändert, nur ohne Telefonanlage.

Die Formulierung für den Auftraggeber:

> „Wir bauen nicht das innovativste LMS — das wäre ein Rennen um Features, die kein Auditor und kein Ausschreibungskunde je bewertet. Wir bauen das erste System, das weiß, ob ein Mensch die Arbeit vor sich sicher tun kann, und das ihm das in seiner Sprache sagt. Wir bauen es in der Reihenfolge, in der es ihn erreicht: erst seine Sprache, dann sein Können, dann sein Stolz. Den Kurskatalog kaufen wir dazu."

Was der Plan dabei schuldet: **mindestens ein Wow-Element muss im Pilot sichtbar sein.** Ein reines Nachweisprojekt gewinnt keine Verbündeten und stirbt an Langeweile, lange bevor es an Technik stirbt.

#### Die drei Elemente, die nicht gestrichen werden dürfen

1. **Audio-first in der Muttersprache + Einfache Sprache als eigenes Register.** Erster Streichkandidat unter Zeitdruck — und der einzige, der zugleich Rechtsvoraussetzung ist (§14 Abs. 2 GefStoffV verlangt verständliche Sprache). Ohne ihn ist der Nachweis rechtlich hohl *und* das Produkt austauschbar. Als **Akzeptanzkriterium** festschreiben, nicht als Backlog-Feature.
2. **Der Stolzbrief.** Physisch, zweisprachig, nach Hause. Kostet fast nichts (`pdf` und `mailer` existieren, Druck ist eine Dienstleistung), ist das einzige Element, das das System auf der Gefühlsseite von einem Kontrollinstrument unterscheidet, und die billigste Maßnahme gegen ~400 T€ jährliche Fluktuationskosten. Er wird als „später" markiert werden. Das darf er nicht.
3. **Der Constraint „Quiz erreicht nie ‚kann selbstständig'".** Die einzige Stelle, an der das Konzept ein Completion-System überschreitet. Unter Auslieferungsdruck wird daraus ein Feature-Flag („erstmal nur Quiz, Beobachtung kommt"). Dann ist das Ergebnis Memberspot mit besserem PDF — und das gesamte Argument gegen den Zukauf fällt in sich zusammen. **DB-Constraint, kein Konfigurationswert.**

#### Urteil: **Go mit Auflagen**

Die Grundentscheidung ist richtig — Nachweis- und KI-Schicht selbst, Player kaufen. Der Zeitplan unterschätzt die drei langsamsten Dinge im Projekt: Mitbestimmung, Personalstammdaten und die Bereitschaft der Objektleitung.

**Vier Auflagen:** realistische 7–9 PM statt 4 · befristete Erprobungs-BV vor jedem echten Datensatz · Nachweismigration vor der Ampel · Enrollment, das die Identität über die Objektleitung bindet statt über eine Mobilfunknummer.

Fällt eine der fünf Auftraggeberfragen (Abschnitt 4) negativ aus — insbesondere unbezahlte Lernzeit oder ein nicht gestoppter Memberspot-Vertrag —, ist es **kein Go, sondern ein Stop bis zur Klärung**: Das Projekt scheitert dann an einer Bedingung, die keine Zeile Code beheben kann. Und wenn im Pilot Audio in der Muttersprache, der Stolzbrief oder der Beobachtungs-Constraint gestrichen werden, ist das Ergebnis technisch korrekt und strategisch wertlos — dann hätte man Memberspot behalten sollen.

---

## 3. Plenum

Sechs Rollen haben das Konzept unabhängig voneinander bewertet. Die Übereinstimmung ist bemerkenswert: **fünf von sechs nennen unabhängig denselben Kernfehler** — das Konzept ist aus der Perspektive der Plattform geschrieben, nicht aus der Perspektive der Menschen, die es benutzen sollen.

### 3.1 Reinigungskraft (Anna, 47, PL, Deutsch B1, 20 h, zwei Jobs)

> „Der Prototyp behauptet mobile-first und ist es nicht. `@media(max-width:850px){.side{display:none}}` — auf meinem Handy verschwindet die Navigation ersatzlos. Es gibt keine mobile Menüleiste. Ich komme auf dem Telefon nirgendwo hin."

- **„7 Minuten. Eine neue Fähigkeit."** In vier Stunden gibt es keine sieben freien Minuten, das Leistungsverzeichnis ist getaktet. Also wird zwischen Job 1 und Job 2 gelernt — unbezahlt. Im gesamten Handoff steht kein Wort zu Arbeitszeit oder Vergütung; Mitbestimmung taucht einmal auf, als „juristisch prüfen".
- **Privatgerät und Datenvolumen** werden durchgehend vorausgesetzt, ohne je erwähnt zu werden. MVP-Inhaltstyp ist „Video + Text". Offline steht nicht in der Definition of Done — und eine PWA allein ist kein Offline.
- **Sprache:** Sicherheitskritische Übersetzungen brauchen redaktionelle Freigabe. Praktisch heißt das: genau die Chemie- und Sicherheitsinhalte kommen zuerst auf Deutsch. B1 reicht für „Kreuzkontamination" nicht. „Einfache Sprache" steht **nicht** im MVP. *„Damit prüft ihr mein Deutsch, nicht meine Hygiene."*
- **Selbsterklärung und Signatur:** *„Euer eigenes Dokument sagt, dass eine gezeichnete Signatur weder Identität noch fremde Hilfe beweist. Sie beweist dem Betrieb also nichts — aber sie gibt ihm etwas gegen mich. Das ist keine Qualitätssicherung, das ist Haftungsverschiebung nach unten."*
- **Streak:** *„Ihr habt das öffentliche Ranking richtigerweise gestrichen und dann privaten Druck eingebaut."* Eine Serie bestraft freie Tage, Krankheit, Teilzeit.
- **Learni:** genau das könnte helfen — und genau das zerstört das Konzept selbst, indem es `ai_conversations` und `ai_messages` mit arbeitgeberkonfigurierter Retention speichert. *„Wenn irgendjemand meine dummen Fragen lesen kann, frage ich nie etwas. Dann klicke ich nur."*
- **Bedingungen für freiwillige Nutzung:** bezahlte Lernzeit im Dienstplan · Chat technisch für Vorgesetzte unlesbar, 24-h-Löschung schriftlich · Audio statt Video, herunterladbar · unbegrenzte Versuche ohne Zeitlimit · Ergebnis nur bestanden/nicht bestanden · und wenn ein Skill nachgewiesen ist: mehr Geld oder weniger Fläche.

### 3.2 Objektleitung (14 Objekte, 60 Kräfte)

> „Ich bin nicht der Lernende und nicht der Autor — ich bin der, der haftet. Die Rolle ‚Objektleitung' hat im gesamten MVP keine einzige Funktion. Das MVP ist für mich unbenutzbar."

- **Löst wirklich etwas:** Die Papierliste im Kofferraum ist das größte Risiko. Versionsgebundener Nachweis, Audit-Log, Wiedervorlage zur Rezertifizierung — echter Wert. Ebenso Mehrsprachigkeit: heute wird faktisch auf Deutsch unterwiesen, wer zu 60 % versteht — arbeitsschutzrechtlich angreifbar.
- **Montag 6:00 Uhr, neue Kraft** — wo es bricht: kein Firmengerät, kein Firmen-Account, kein WLAN (→ Login per Handynummer, QR-Onboarding statt E-Mail/Passwort); Videos in der Tiefgarage ohne Empfang (→ Offline); 25-Minuten-Basisunterweisung frisst Arbeitszeit (→ Erstunterweisung Kurzform unter 10 Minuten plus Vertiefung in 14 Tagen); **objektspezifische Bausteine fehlen** — Schlüsselordnung, Aufzug, Alarmanlage, Gefahrstoffe *dieses* Objekts. `locations` kennt das Konzept, objektspezifische Unterweisung nicht. *„Das ist der eigentliche Kern."*
- **Fünf Forderungen:** Ampel je Objekt als Startbildschirm · Nachweis-PDF auf Knopfdruck plus Read-only-Auditor-Link mit Ablaufdatum · Sprachzuordnung je Person als Pflichtfeld inklusive Nachweis der Unterweisungssprache · Mehrfachzuordnung für Springer plus Prüfung „darf heute in Objekt X eingesetzt werden" · Lernzeit-Export für die Lohnbuchhaltung.
- **Content, der ehrliche Punkt:** *„Wir haben keinen Content Author in Vollzeit. Wir werden auch keinen bekommen."* Nötig ist eine fertige Basisbibliothek zum Start (zukaufen oder konvertieren) plus Objektspezifik per Handy in fünf Minuten: Foto vom Sicherungskasten, Sprachnotiz einsprechen, KI macht Text, Übersetzung und drei Prüffragen, Freigabe durch die Objektleitung.
- **Migration:** *„Laufende Zertifikate müssen weitergelten."* Alt-Abschlüsse als „historischer Nachweis (importiert)" mit ursprünglichem Ablaufdatum. Sonst wiederholen 60 Leute alles.
- **Kopplung mit den bestehenden Apps — der eigentliche Hebel:** Reklamationsgrund → Skill-Mapping → Kurzmodul mit Frist, Ergebnis zurück in die Reklamationsakte · Auditbefund über Schwelle → Team-Schulungsvorschlag (nicht personenbezogen) · **bestandener QualiCheck vor Ort ist der beste Praxisnachweis, den es gibt** und sollte direkt als `credential_evidence` zählen. Wichtig: *„kein Automatismus in Richtung Sanktion. Zuweisung ja, Bewertung nein — sonst melden die Kräfte nichts mehr."*

### 3.3 Datenschutz und Betriebsrat

> „Mitbestimmungspflichtig ist das System als Ganzes. Die Diskussion ‚wir wollen doch gar nicht überwachen' ist rechtlich irrelevant — es genügt die objektive Eignung zur Überwachung."

**Im Konzept komplett übersehen:** §94 Abs. 2 BetrVG (die Skill-Matrix ist ein Beurteilungsgrundsatz — zustimmungspflichtig) · §95 (Auswahlrichtlinie, sobald Skill-Level Einsatzplanung steuert) · §98 (betriebliche Bildungsmaßnahmen) · §87 Abs. 1 Nr. 2/3 (Lernzeit ist Arbeitszeit) · §87 Abs. 1 Nr. 1 (Nutzungsregeln, Selbsterklärung) · §80 Abs. 3 S. 2 (Sachverständiger bei KI gilt als erforderlich) · Art. 26 Abs. 7 AI Act (eigenständige Informationspflicht **vor** Inbetriebnahme).

**Wo der Betriebsrat sofort stoppt:** personenscharfes Lernverhalten im Objektleitungs-Dashboard · `ai_messages`-Volltext ohne Zugriffsschutz (*„das ist ein Gedankenprotokoll"*) · Streak/Gamification ohne BV-Regelung · Skill-Level als Grundlage für Einsatz-, Vergütungs- oder Trennungsentscheidungen · **Pilot mit echten Mitarbeiterdaten vor Abschluss der BV** (ein „technischer Test mit echten Daten" ist bereits Einführung).

**Rechtsgrundlagen, differenziert statt pauschal:** Pflichtunterweisungen laufen über Art. 6 Abs. 1 lit. c DSGVO (echte rechtliche Verpflichtung inklusive Nachweisführung). Freiwilliges Lernen, Empfehlungen, Learni-Chat und Skill-Wallet **nicht** über Art. 6 Abs. 1 lit. f als Bequemlichkeitslösung, sondern über die **Kollektivvereinbarung als Erlaubnisnorm (Art. 88 DSGVO i. V. m. §26 Abs. 4 BDSG)** — die Betriebsvereinbarung wird damit selbst Rechtsgrundlage. Das ist der stärkste verfügbare Hebel. Einwilligung scheidet im Beschäftigungsverhältnis weitgehend aus. §26 Abs. 1 S. 1 BDSG ist seit EuGH C-34/21 unionsrechtlich angeschlagen — nicht darauf allein aufbauen. *(Anwaltliche Prüfung nötig.)*

**Art. 9 DSGVO:** Freitextantworten und Chatverläufe können Gesundheitsdaten enthalten; Sprachwahl und ein „Einfache Sprache"-Profil lassen auf Herkunft oder Behinderung schließen. Das braucht technische Absicherung, nicht nur eine Policy.

**DSFA nach Art. 35 ist zwingend** — KI-Einsatz auf Beschäftigtendaten, Bewertung/Scoring, systematische Erfassung, vulnerable Betroffenengruppe, innovative Technologie. Sie muss **vor** der Verarbeitung stehen, nicht als Phase-2-Ticket.

| Tabelle | Problem | Mindestmaßnahme |
|---|---|---|
| `learning_events` | faktisches Verhaltens- und Arbeitszeitprotokoll | keine Sekundengranularität, Rohdaten ≤ 90 Tage, danach Aggregat |
| `ai_conversations` / `ai_messages` | Selbstoffenbarung, Art.-9-Risiko | Default 30 Tage, kein Klartextzugriff für Manager oder Admin, kein Training, „Verlauf löschen"-Button |
| `ai_usage_events` | „wer viel fragt, kann wenig" | nur aggregiert, ohne Personenbezug auswertbar |
| `assessment_answers` | Einzelantworten sind Leistungsdaten | Manager sieht nur bestanden/nicht bestanden + Datum; Antwortdetails ≤ 12 Monate |
| `audit_events` | append-only kollidiert mit Art. 17 | strikte Trennung Nachweis- vs. Verhaltensdaten, Audit-Log minimiert und pseudonymisiert |

**EU AI Act — die Einschätzung, die das Konzept nicht trifft:** Hochrisiko, sobald KI bewertet. Anhang III Nr. 3 lit. b greift bei KI-gestützter Bewertung von Lernergebnissen (rein deterministische MC-Auswertung ist keine KI-Bewertung — sobald Learni Freitext oder Szenarien bewertet oder Skill-Level ableitet, kippt es). Anhang III Nr. 4 lit. b greift, sobald Skill-Daten Aufgabenzuweisung, Einsatzplanung oder Leistungsbewertung beeinflussen — **und genau das ist der Business Case.** Der Ausnahmefilter des Art. 6 Abs. 3 hilft nicht: Er ist bei Profiling ausdrücklich gesperrt, und ein Skill-Profil ist Profiling.

Konsequenz: Bei Eigenentwicklung unter eigenem Namen wäre Zitzelsberger **Anbieter** (Art. 25 Abs. 1), nicht nur Betreiber — mit Risikomanagement (Art. 9), Data Governance (Art. 10), technischer Dokumentation nach Anhang IV, Logging, Gebrauchsanweisung, menschlicher Aufsicht mit realer Eingriffsbefugnis, QMS, Konformitätsbewertung, EU-Konformitätserklärung, CE, Registrierung in der EU-Datenbank, Post-Market-Monitoring und Vorfallmeldung. **Das ist ein eigenes Projekt, keine Zeile im Handoff.** Art. 4 (AI Literacy) gilt bereits seit 02.02.2025 risikoklassenunabhängig und verlangt rollenspezifische Schulung mit Nachweis, nicht einen Lernpfad. Bei WebXR zusätzlich Eye-Tracking und Aufmerksamkeitsmetriken ausschließen, nicht nur Emotionserkennung.

**Der wichtigste Punkt des ganzen Abends:** §14 Abs. 2 GefStoffV und §14 Abs. 2 BioStoffV verlangen eine **mündliche**, arbeitsplatz- und tätigkeitsbezogene Unterweisung vor Aufnahme der Tätigkeit und danach mindestens jährlich. Reines E-Learning erfüllt das nicht. **Blended ist Pflicht, nicht Komfort.**

Zum Beweiswert: Eine Canvas-Unterschrift ist eine einfache elektronische Signatur — wirksam, aber ohne Anscheinsbeweis und ohne Urkundenbeweis nach §416 ZPO. Realistisch nötig: personalisierter Account mit MFA-Step-up beim Abschluss · hash-verkettetes, append-only Protokoll **plus qualifizierter Zeitstempel** (Vermutungswirkung für Zeit und Integrität — bestes Preis-Leistungs-Verhältnis) · vollständiger Inhalt inklusive Unterweisendem, Sprache und Rückfragemöglichkeit · QES nur dort, wo echte Schriftform gefordert ist. *(Anwaltliche Prüfung nötig, je Unterweisungstyp getrennt.)*

**Fünf Show-Stopper:** Gefahrstoff-/Biostoff-Unterweisung digital-only · Hochrisiko-Einstufung mit voller Anbieterrolle nicht eingeplant · kein BV-Entwurf, §§94/95/98 fehlen vollständig · `ai_messages`-Volltext ohne Zugriffs- und Verwertungsschutz · Rechtsgrundlagen ungeklärt.

### 3.4 L&D / Didaktik

> „Das Papier ist ein Systemarchitektur-Dokument, kein Lernkonzept. Alles, was didaktisch entscheidet, steht als Aufzählungswort da und ist nirgends im Datenmodell abgebildet."

- **Skill-Taxonomie ist kein Kompetenzmodell.** Es fehlt die Niveaudimension mit Verhaltensankern: *angeleitet → unter Aufsicht → selbstständig → kann andere anleiten*. Ohne sie ist „Skill Level 12" bedeutungsleer.
- **Weiter fehlen:** Transferkonstrukt (Einheiten nach **Tätigkeiten am Objekt** schneiden, nicht nach Themen) · Spacing und Retrieval (`review_schedule` je Learner × Skill, 60-Sekunden-Retrieval vor Schichtbeginn — jährliche Wiederholung ist juristisch das Minimum und lernpsychologisch wertlos) · Fehlerkultur (Distraktor → Fehlvorstellung mappen; ohne Misconception-Mapping ist jeder Versuch ein Ratedurchgang) · Modelllernen (Paten-/Einweiser-Relation, „Kollege zeigt"-Videos aus dem eigenen Objekt: bekanntes Gesicht, bekannter Ort, echte Maschine).
- **Der zentrale Anspruch ist nicht eingelöst.** Der Vertical Slice endet bei Quiz → Selbsterklärung → Signatur → Skill. *„Damit produziert das System exakt das, was es ablehnt: eine Completion, nur mit besserem Audit-Trail. Die Selbsterklärung beweist Ehrlichkeit, nicht Können."*
- **Learni:** Socratic Tutoring ist Deko — bei Deutsch A2 um 5:30 Uhr mit dem Wischmopp in der anderen Hand erzeugt Rückfrage-Dialektik Scham und Abbruch; freie Chat-Eingabe setzt Schreibkompetenz voraus, die hier oft fehlt. Echter Nutzen: **Voice-in/Voice-out in der Muttersprache** (Kern, nicht spätere Ausbaustufe — sprechen können alle, lesen nicht) · **Just-in-time am Objekt** (Foto der Flasche → was ist das, wo darf ich es benutzen, was ziehe ich an) · **Guardrail statt Kreativität** bei Gefahrstoff-, Verletzungs- und Arbeitszeitfragen: hinterlegter Text plus „Sprich mit deiner Objektleitung" plus Anruf-Button · **Autoren-Copilot als größter ROI** · L&D-Analytik.
- **Motivation:** Streaks sind für Schichtarbeit schädlich — Urlaub, Krankheit und Teilzeit brechen die Serie, die Mechanik bestraft genau die Struktur des Jobs. Wirksam: bezahlte Lernzeit, sichtbar quittiert (stärkster Motivator und Vertrauenssignal) · Statusgewinn im Team („Einweiser für Sanitärreinigung" — Titel, ggf. Zulage: aus Lernen wird Rolle) · physische Artefakte (laminierte Skill-Karte, Aufnäher, Symbol am Namensschild — *„ein Badge im Browser existiert für diese Zielgruppe nicht"*) · Anerkennung durch die direkte Führungskraft · Portabilität als Fluktuationsantwort · Team-Ziele statt Einzelvergleich · sofortiges, konkretes Feedback statt Punktzahl.
- **Größter ungenutzter Hebel: die Objektleitung.** Heute Kontrollinstanz, muss Lernarchitektin werden — Beobachterin, Freigeberin, Anerkennungsgeberin. Ein eigener Führungskräfte-Lernpfad („Wie weise ich ein, wie beobachte ich, wie gebe ich Feedback ohne Beschämung") verändert die Wirkung stärker als jedes VR-Modul. Zweiter Hebel: **Rückkehrer** — bei hoher Fluktuation kommen viele wieder; erhaltene Nachweise verkürzen das Re-Onboarding von Wochen auf Tage.

### 3.5 Architektur / CTO

Vollständig in Abschnitt 2.2 eingearbeitet. Ergänzend die neun unterschätzten Architekturentscheidungen:

1. **Assessment-Lock** garantiert ehrlich nur „keine Hilfe **über unseren Kanal**" — zweites Gerät, ChatGPT, Kollege bleiben offen. Ungeklärt und blockierend: Was passiert bei Browser-Absturz mitten im Test — Auto-Fail, Resume oder neuer Versuch?
2. **Publish, während 40 Leute mitten im Kurs sind.** Enrollment und Session müssen `content_version` pinnen; Fragen dürfen nie in-place editiert werden. Ungelöst: fehlerhafte Frage nach 200 bestandenen Prüfungen — nachbewerten oder nicht? **Ohne explizite Korrekturpolicy ist der Nachweis wertlos.**
3. **35 Tabellen × 6 Rollen RLS ist eine untestbare Matrix.** „Objektleitung sieht nur Mitarbeiter ihrer Objekte" braucht rekursive Membership-Joins in *jeder* Policy — Performance und Rekursionsfallen.
4. **Der RAG-Autorisierungsfilter bricht den ANN-Index.** HNSW plus `WHERE role_scope = …` liefert entweder falsches Recall (Post-Filter frisst Top-k) oder Seq-Scan (Pre-Filter). Lösung: Vektorbestand nach Scope partitionieren, Partial Indexes. Zugriffsschutz **nie** über Prompt-Instruktionen. Offen: eine bereits gegebene Antwort, die eine inzwischen zurückgezogene Sicherheitsanweisung zitiert.
5. **Offline ist kein PWA-Häkchen.** Lernen offline ja; **Assessment offline nein**, sonst ist die Integritäts- und Zeitstempelaussage gelogen. Video nicht cachen, sondern niedrige Bitrate plus Audio-Fallback plus Transkript.
6. **KI-Kosten sind nicht das Problem — die Kostenstruktur schon.** Ein RAG-Turn kostet auf Sonnet-5-Niveau grob 1,8 Cent; 500 Mitarbeitende × 5 Turns/Monat ≈ 45 $/Monat, mit Prompt-Caching deutlich darunter. Teuer wird: **Re-Embedding bei jeder Contentänderung**, Voice-to-Voice (10–50×), unbegrenzter Chat. Also Token-Budget pro Nutzer und Caching ab Tag 1.
7. **Übersetzungskosten sind Redaktionskosten, nicht MT-Kosten.** Die verpflichtende Fachfreigabe jeder Änderung × 4 Sprachen ist eine dauerhafte L&D-Last. Eine falsch übersetzte Gefahrstoffanweisung ist ein Arbeitsschutzrisiko.
8. **Medien/Video ist ein eigenes Produkt.** Ingest → Transcode → HLS → CDN → Untertitel. **Kaufen** (Cloudflare Stream, Mux, Vimeo), nie selbst bauen.
9. **„Append-orientierter Audit-Trail" in derselben Datenbank, in der der Admin schreibt, ist ohne Hash-Verkettung nicht manipulationssicher** — der Auditor-Nutzen ist dann behauptet, nicht real.

**Top-Risiken:** Scope-Kollaps (Projekt strandet bei 60 %, Memberspot läuft weiter, Doppelkosten) · Beweiswert des Nachweises hält nicht · Mitbestimmung erst nach Launch verhandelt → Stilllegung möglich · Stack-Fork und Bus-Faktor · **Content ist der Engpass, nicht Software** — im Konzept nicht budgetiert.

### 3.6 Geschäftsführung / CFO

> „Im Konzept: nirgends. 236 Zeilen Architektur, kein Euro."

*Annahmen als Größenordnungen: ~500 MA · AG-Vollkostensatz gewerblich ~18 €/h · Umsatz ~18 Mio € · EBIT ~4 % ≈ 700 T€ · ~200 Aus-/Eintritte p. a.*

| Hebel | Ist-Kostenblock p. a. | Realistisch hebbar p. a. |
|---|---|---|
| **Lernzeit als Arbeitszeit** (größter Block) | Pflichtunterweisung ~45 T€ + Onboarding ~29 T€, mit Präsenz-Overhead Faktor 1,5–2 → **110–150 T€** | Verlagerung auf mobil/Micro: **20–40 T€** |
| Einarbeitung (~40 h Minderleistung je Eintritt) | ~145 T€ | 15 % kürzer → **20 T€** |
| Fluktuation (200 × ~2.000 €) | ~400 T€ | Frühfluktuation −10 % → **20–40 T€** |
| Reklamation/Nacharbeit (0,5–1,5 % Umsatz) | 90–270 T€ | −10 % → **10–25 T€** |
| Nachweisfähigkeit in Ausschreibungen | – | ein Objekt: EBIT-Beitrag **10–20 T€** (höchstes Upside, geringste Prognostizierbarkeit) |
| Haftung/Bußgeld | Tail-Risk | Erwartungswert **5–15 T€** — Versicherung, kein Business Case |

**Summe attribuierbarer Nutzen: ~80–150 T€ pro Jahr. Davon entstehen rund 80 % durch *mobil + mehrsprachig + lückenloser Nachweis* — nicht durch RAG, XR, Open Badges oder eIDAS.**

**Die ehrliche Gegenrechnung:** Lernzeit ist vergütungspflichtige Arbeitszeit. Wird heute faktisch unbezahlt oder gar nicht gelernt und das System macht es sichtbar, **steigen die Kosten zunächst.** Das gehört in die Rechnung.

| TCO 3 Jahre | Eigenbau | Memberspot behalten | Standard-Frontline-LMS |
|---|---|---|---|
| Plattform (Entwicklung, Wartung, Lizenz, Recht) | 505–1.285 T€ | 20–60 T€ | 65–170 T€ |
| **Content + Übersetzung (fällt in jeder Variante an)** | 160–350 T€ | 160–350 T€ | 160–350 T€ |
| **Gesamt** | **~700 T€ – 1,2 Mio €** | **~200–400 T€** | **~250–500 T€** |

Der Eigenbau kostet auf Plattformebene das **15- bis 40-fache** und bindet in Jahr 1 ein halbes bis ganzes Jahres-EBIT — für 80–150 T€ Nutzen. Und: *„Die relevante Vergleichsgröße ist nicht Memberspot, sondern ein Standard-LMS für Deskless Worker. Gegen das muss sich der Eigenbau rechtfertigen."*

**Zum Anspruch „innovativstes KI-LMS":** *„Eitelkeit. Kein Kunde schreibt ‚innovativstes KI-LMS' in eine Wertungsmatrix. Er will Sauberkeit, geschultes Personal und einen Nachweis, den sein Auditor akzeptiert."*
Innovation, die zahlt: Mehrsprachigkeit, Einfache Sprache, Vorlesen — und KI-gestützte Erstellung von Quiz- und Übersetzungsentwürfen, weil sie direkt den größten Kostenblock senkt. Innovation, die Geld verbrennt: VR/AR-Lab (Gerätedurchdringung bei Reinigungskräften ≈ 0, 10–50 T€ Content je Szenario), Open Badges 3.0/CLR 2.0/Verifiable Credentials (kein Kunde fragt danach), eIDAS-QES, Voice-to-Voice, Socratic Tutoring.
*„Wir sind kein Softwarehaus. Wird das Ding gut, haben wir ein Produkt ohne Vertrieb. Wird es mittelmäßig, haben wir ein Altsystem, das genau ein Mensch versteht."*

**Risiko:** Ausfall bei 60 % → Restwert nahe null, ein zu 60 % revisionssicheres Nachweissystem ist juristisch wertlos; Übernahme durch Dritte kostet 3–6 Monate Einarbeitung und +30–50 %. Existenziell, wenn Repo, Cloud, Domains und Secrets auf privaten Accounts liegen. **Memberspot bereits gekündigt = Notfall:** Kündigung zurücknehmen oder überbrücken, notfalls zu schlechteren Konditionen, und **heute** Vollexport aller Inhalte und Nachweisdaten — Unterweisungsnachweise sind aufbewahrungspflichtig, der Verlust der Historie ist im Streitfall nicht heilbar.

**Gate-Modell:**

| Gate | Budget | Dauer | Abbruchkriterium |
|---|---|---|---|
| **0 Bestandssicherung** | 0–5 T€ | 4 Wo. | Pflicht: Vertrag stabilisieren, Vollexport, **Nullmessung** (gezahlte Lernstunden, Nachweislücke an 50-MA-Stichprobe) |
| **1 Marktabgleich & Recht** | 15–30 T€ | 6–8 Wo. | Standardprodukt erfüllt ≥ 85 % der Muss-Liste zu ≤ 50 T€/Jahr → **Eigenbau des Lernteils beendet** |
| **2 Pilot mit Content** | 30–60 T€ | 3 Mon. | 10 Einheiten, 3 Sprachen, 60–80 MA. Abschlussquote < 60 % oder Nachweisquote < 90 % → das Problem ist nicht die Software |
| **3 Rollout + Nachweis-Reporting** | 80–150 T€ Content, 20–40 T€ Reporting | 18 Mon. | Nutzenmessung gegen Gate-0-Baseline; < 50 % Zielerreichung → Stopp |
| **4 EIN KI-Feature** | ≤ 25 T€ | – | nur Übersetzung / Einfache Sprache / Vorlesen, messbar |

**Freigabe Jahr 1: 150–250 T€** — über die Hälfte davon Content, und Content ist das einzige Asset, das plattformunabhängig dem Unternehmen gehört.

**Fünf Bedingungen für ein Go:** (1) Baseline vor Budget, kein Euro ohne Nullmessung · (2) Content gehört uns — Skripte, Master-Videos, Übersetzungsspeicher, Fragenpools vertraglich exportierbar in Standardformaten · (3) kein Abschalten des Altsystems vor dokumentierter Abnahme inklusive migrierter Nachweishistorie, Doppelbetriebskosten eingeplant · (4) Eigentum und Bus-Faktor: Repo, Cloud, Domains, Secrets auf Firmen-Accounts, Betriebs- und Wiederanlaufdoku als Zahlungsmeilenstein, ein zweiter extern beauftragbarer Mensch muss nachweislich deployen können — getestet vor Rollout · (5) Rechtsrahmen **abgeschlossen**, nicht „parallel".

---

## 4. Die fünf Fragen, die nur der Auftraggeber beantworten kann

Diese Fragen blockieren Entscheidungen, nicht Arbeit. Sie sind bewusst so formuliert, dass jede in einem Satz beantwortbar ist.

1. **Memberspot:** Ist die Kündigung gestoppt oder überbrückt, bis welches Datum läuft der Vertrag, und liegt der Vollexport aller Inhalte *und* Nachweisdaten inklusive ursprünglicher Ablaufdaten vor? *(Datum + ja/nein)*
2. **Lernzeit:** Wird Lernzeit ab Pilotstart bezahlt — mit welchem Stundenbudget je Mitarbeiter und Jahr, und wer gibt sie frei? *(Stundenzahl + Name)*
3. **Objektleitung:** Wie viele Minuten je Unterweisung und je Praxischeck sind im Objektbudget hinterlegt, und ist die Pilotteilnahme der beiden Objektleitungen freiwillig oder angeordnet? *(Minutenzahl + freiwillig/angeordnet)*
4. **Personalstamm:** Welches System führt heute Personalnummer, Ein- und Austrittsdatum, Objektzuordnung und Sprache — und wer darf einen automatisierten Export daraus freigeben? *(Systemname + Name)*
5. **Geld und Recht:** Sind 150–250 T€ für Jahr 1 freigegeben (über die Hälfte davon Content), gilt die Gate-1-Abbruchregel verbindlich, und wann ist der Termin mit dem Betriebsrat? *(ja/nein + Datum)*

---

## 5. Empfehlung

**Go mit Auflagen — aber mit einem anderen Produkt als beauftragt.**

Das Konzept beschreibt ein LMS. Gebraucht wird ein System, das eine Frage beantwortet, die kein LMS am Markt beantwortet:

> **Darf diese Person heute in diesem Objekt arbeiten — und kann sie es nachweislich?**

Der Weg dahin:

1. **Kurskatalog und Player kaufen.** Kursbibliothek, Video-Hosting, Fortschrittsbalken, i18n-Grundgerüst sind Massenware; dort steckt der größte Teil des Aufwands und der kleinste Teil des Werts. Einziges Auswahlkriterium: **API, Webhooks, SSO, Export** — nicht die Oberfläche.
2. **Nachweis- und KI-Schicht selbst bauen**, als eigener Python-Dienst in einem eigenen Repository, der `zb-shared` per Tag pinnt und an Reklamation, QualiCheck und Objektaudit andockt. Das ist der differenzierende Teil, und er existiert zur Hälfte schon.
3. **Erst die Sprache, dann das Können, dann der Stolz.** Audio-first in der Muttersprache mit Einfache Sprache als eigenem Register · der Praxischeck als einzige Tür zu „kann selbstständig ausführen" · der gedruckte Stolzbrief. Diese drei sind das, was die Journey einzigartig macht, und sie kosten zusammen weniger als das VR-Lab.
4. **Recht und Mitbestimmung sind kritischer Pfad, nicht Nachlauf.** Betriebsrat in Woche 1, befristete Erprobungsvereinbarung vor dem ersten echten Datensatz, DSFA parallel zum Design. Bis zur Unterschrift: Testdaten.
5. **Gestrichen, nicht verschoben:** WebXR und VR-Lab, Open Badges 3.0 / CLR 2.0 / xAPI, eIDAS-QES, Voice-to-Voice, Socratic Tutoring, Multi-Tenancy, Streaks, die Canvas-Unterschrift und die Sprachauswahl DE/EN/FR/PL.

**Realistischer Rahmen Jahr 1:** 7–9 Personenmonate Entwicklung bei einem Entwickler (nicht 4), 30–50 T€ Recht und Betriebsrat, 80–150 T€ Content. Der 90-Tage-Plan heißt korrekt **„90 Tage bis Pilotreife der grünen Objektmappe"**, nicht „90 Tage bis fertig".

**Und die Stop-Bedingung:** Fällt eine der fünf Fragen aus Abschnitt 4 negativ aus — insbesondere unbezahlte Lernzeit oder ein nicht gestoppter Memberspot-Vertrag —, ist es kein Go, sondern ein Stop bis zur Klärung. Das Projekt scheitert dann an einer Bedingung, die keine Zeile Code beheben kann.

---

## Anhang: Hinweis zum Ablageort

Dieses Review liegt im Repository `zb-shared`, weil dort der Auftrag gestartet wurde. **Das Produkt selbst gehört nicht hierher.** `zb-shared` ist eine versionierte Bibliothek, die mehrere Apps per Git-Tag pinnen; ein Produkt mit eigenem Datenmodell, Migrationen und Frontend würde die Release-Semantik zerstören und jede App mit LMS-Abhängigkeiten belasten. LEARNI OS bzw. `zb-lernen` bekommt ein eigenes Repository. Abhängigkeitsrichtung ausschließlich **LMS → `zb-shared`**, niemals umgekehrt.
