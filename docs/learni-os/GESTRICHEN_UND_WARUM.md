# Gestrichen — und warum

Acht Bausteine aus dem Ursprungskonzept sind nicht im Slice enthalten. Sie sind **gestrichen, nicht
verschoben**: Es gibt keinen Platz in einer späteren Phase, in der sie automatisch wieder auftauchen.
Jeder Punkt nennt einen **Umkehrpunkt** — das Ereignis, bei dem die Entscheidung neu zu treffen ist.

Das gemeinsame Muster: Nichts davon ist gestrichen, weil es unmodern wäre. Es ist gestrichen, weil es
entweder Geld ohne Gegenwert kostet, ein Rechtsrisiko einführt, oder die Menschen bestraft, die es
benutzen sollen.

---

## Headset-VR / „Immersive Learning Lab"

**Präzisierung vorab:** AR ist nicht gestrichen. Der QR-Code am Putzwagen, der 60–120 Sekunden
gesprochene Anleitung genau für dieses Objekt liefert, ist im Slice enthalten und gilt als stärkster
Hebel des ganzen Konzepts. Gestrichen ist ausschließlich das Headset.

**Warum.** Die Gerätedurchdringung bei Reinigungskräften liegt praktisch bei null. Aus dem Plenum,
Perspektive Reinigungskraft: „Ein Headset habe ich nicht und will keins um 5:30 Uhr." Dazu 10–50 T€
Contentkosten je Szenario bei 80–150 T€ Gesamtnutzen pro Jahr. Und WebXR bringt ein Risiko mit, das
leicht übersehen wird: Eye-Tracking und Aufmerksamkeitsmetriken sind im Headset technisch trivial und
am Arbeitsplatz nach Art. 5 Abs. 1 lit. f AI Act verboten. Ein Gerät zu betreiben, dessen Standard-
Telemetrie man aktiv unterdrücken muss, ist kein guter Ausgangspunkt.

**Umkehrpunkt.** Ein Kunde — realistisch ein Klinikum — verlangt in einer Ausschreibung dokumentiertes
Simulationstraining.

## Open Badges 3.0 / CLR 2.0 / Verifiable Credentials

**Warum.** Das Ziel ist richtig: Bei rund 40 % Fluktuation ist ein mitnehmbarer Nachweis eine
Rückkehrer-Strategie, kein Techniknice-to-have. Der Standard ist verfrüht. Er setzt ein
Wallet-Ökosystem voraus, das diese Zielgruppe nicht hat, und kostet Konformitätsarbeit, Hosting und
eine eigene Widerrufsinfrastruktur. Denselben Zweck erfüllen ein signiertes PDF mit Verifikations-QR
und der gedruckte, zweisprachige Stolzbrief — beides ist im Slice enthalten.

**Umkehrpunkt.** Ein Kunde oder eine öffentliche Ausschreibung fragt Open Badges schriftlich ab.

**Selbsteinschätzung.** Das ist die schwächste der acht Begründungen. Sie steht bewusst in Abschnitt 4
des Analyseauftrags als Stelle, an der Widerspruch wahrscheinlich berechtigt ist.

## xAPI / Learning Record Store

**Warum.** Ein LRS ist ein feingranularer Verhaltensspeicher. Die Auswertungen, die zulässig und
gewollt sind — aggregiert, mit Mindestschwelle, ohne Verhaltensprofile — brauchen ihn nicht. Man würde
Infrastruktur bauen, deren einziger Mehrwert genau die Daten wären, die man nicht erheben will.

**Umkehrpunkt.** Keiner, der derzeit plausibel erscheint.

## eIDAS-QES (qualifizierte elektronische Signatur)

**Warum.** Das ArbSchG verlangt für eine Unterweisungsbestätigung keine qualifizierte Signatur.
Gebraucht werden Identität, Integrität und Inhalt. Das leisten ein personalisierter Account, ein
hash-verkettetes Protokoll und ein qualifizierter Zeitstempel (Art. 41 eIDAS, Vermutungswirkung für
Zeit und Integrität) zu einem Bruchteil der Kosten. QES bräuchte ein Identifizierungsverfahren für jede
einzelne Person; bei 500 Beschäftigten und rund 200 Wechseln pro Jahr steht das in keinem Verhältnis.

**Wichtig:** Die Abstraktion bleibt erhalten. Die Signaturmethode ist im Datenmodell austauschbar
modelliert; QES lässt sich ergänzen, ohne etwas umzubauen.

**Umkehrpunkt.** Ein Rechtsgutachten stellt für einen bestimmten Nachweistyp echte Schriftform nach
§126a BGB fest.

## Lernserien / Streaks

**Warum.** Eine Serie bestraft freie Tage, Krankheit, Urlaub und Teilzeit — also genau die Struktur
dieses Jobs. Das Ursprungskonzept hatte das öffentliche Ranking richtigerweise gestrichen und dann
privaten Druck eingebaut. Ersetzt durch das, was bei dieser Zielgruppe wirkt: sichtbar quittierte
bezahlte Lernzeit, Ein-Klick-Anerkennung durch die direkte Führungskraft, physische Artefakte.

**Umkehrpunkt.** Keiner.

## Punktestände

**Warum.** Sobald eine Zahl existiert, wird jemand eine Entscheidung darauf stützen. Damit rutscht das
System in Anhang III Nr. 4 AI Act — Skill-Daten steuern Einsatz oder Bewertung —, und zwar für eine
Zahl, die nichts aussagt. Ersetzt durch Kompetenzstufen mit Verhaltensankern: „kann selbstständig
ausführen" ist überprüfbar, „Skill-Level 12" ist es nicht.

**Umkehrpunkt.** Keiner.

## Ranglisten

**Warum.** Das Ursprungskonzept verbot öffentliche Ranglisten bereits selbst. Das Verbot wurde auf die
privaten Varianten ausgedehnt: Personenscharfe Vergleichsdaten sind Leistungskontrolle, unabhängig von
der Bezeichnung. Da es keinen Betriebsrat gibt, der das einfordert, muss diese Selbstbeschränkung im
Datenmodell stehen und nicht in einer Richtlinie.

**Umkehrpunkt.** Keiner.

## Canvas-Unterschrift

**Warum.** Das Ursprungskonzept sagt es selbst: Sie beweist weder Identität noch die Abwesenheit
fremder Hilfe. Damit ist der Nutzen null, das Risiko nicht. Rechtlich ist sie eine einfache
elektronische Signatur — kein Anscheinsbeweis, kein Urkundenbeweis nach §416 ZPO. Praktisch
unterschreibt jemand mit dem Finger auf einem Sprung im Display einen deutschen Satz, den sie nicht
ganz versteht. Aus dem Plenum, Perspektive Reinigungskraft: „Das ist keine Qualitätssicherung, das ist
Haftungsverschiebung nach unten."

Ersetzt durch personalisierten Account plus Zeitstempel — und, wichtiger, durch einen **anderen
Bestätigungstext**: nicht „ich hatte keine Hilfe", sondern „ich war dabei, ich habe verstanden, ich
konnte fragen". Das ist es, was §14 Abs. 2 GefStoffV dokumentiert sehen will, und es ist etwas, das die
Person tatsächlich beurteilen kann.

**Umkehrpunkt.** Keiner.

## Multi-Tenancy

**Warum.** Es gibt ein Unternehmen. Multi-Tenant-Tests würden Fiktion testen, und 35 Tabellen × 6
Rollen ergäben eine Berechtigungsmatrix, die niemand verifiziert. Reduziert auf drei Rollen: Lernende,
Objektleitung, Administration inklusive Auditor mit Nur-Lese-Sicht.

**Umkehrpunkt.** Eine Übernahme oder ein Tochterunternehmen mit eigener Belegschaft, das getrennt
verwaltet werden muss.
