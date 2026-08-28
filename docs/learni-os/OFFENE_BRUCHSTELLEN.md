# Offene Bruchstellen

Elf Bruchstellen wurden im Kritiker-Durchgang benannt. Vier sind durch die Antworten des
Auftraggebers geschlossen oder entfallen. **Sieben sind offen** und Gegenstand der Analyse.

Format je Punkt: Was bricht · Wann · Bisher vorgeschlagene Gegenmaßnahme · Was daran ungeprüft ist.

---

## L2 — Die Ampel ist am Tag 1 zu 100 % rot
**Was bricht.** Die Objekt-Ampel zeigt ohne migrierte Nachweishistorie keine Realität, sondern eine leere
Datenbank. Alarmmüdigkeit in Woche eins, danach glaubt niemand mehr der Farbe.
**Wann.** Woche 3–4, sobald die Ampel erstmals mit echten Objekten läuft.
**Gegenmaßnahme.** Migration der laufenden Nachweise als Vorbedingung der Ampel. Dritter Zustand
„grau = unbekannt" mit Einführungsfrist je Objekt.
**Ungeprüft.** Ob Memberspot Teilnahme- und Nachweisdaten überhaupt exportierbar hält, und in welcher
Form. Ob importierte Altnachweise rechtlich als Nachweis weitergelten oder nur als Indiz. Ob die
Einführungsfrist je Objekt oder je Unterweisungstyp laufen muss.

## L4 — Anmeldung funktioniert dort nicht, wo gereinigt wird
**Was bricht.** Ein SMS-Einmalcode setzt Netz voraus; im Tiefgeschoss gibt es keins. Eine Mobilfunknummer
beweist Gerätebesitz, nicht Identität — bei Prepaid, geteilten Familiengeräten und rund 200
Nummernwechseln pro Jahr trägt sie keinen Rechtsnachweis. Angeordnete Privatgerätenutzung ist nicht
durchsetzbar.
**Wann.** Ab dem ersten echten Enrollment.
**Gegenmaßnahme.** Identität einmalig durch die Objektleitung im Beisein feststellen und protokollieren;
danach langlebiger Gerätetoken plus persönliche PIN. Kein Selfservice-Reset. Geteiltes Gerät als
expliziter Modus mit kurzer Sitzung. Pflicht-Fallback: Tablet der Objektleitung im Kiosk-Modus.
**Ungeprüft.** Wie der Gerätetoken bei Geräteverlust, Werksreset oder Weitergabe des Geräts behandelt
wird. Ob das Kiosk-Tablet nicht selbst zum Identitätsloch wird. Ob eine PIN, die die Objektleitung
zurücksetzen kann, den Beweiswert des Nachweises beschädigt.

## L6 — Offline-Erfassung und Zeitstempel widersprechen sich
**Was bricht.** Ein qualifizierter Zeitstempel bezeugt den Server-Eingang. Die Erfassungszeit auf dem
Gerät ist eine Client-Behauptung mit manipulierbarer Uhr. Stehen beide gleichrangig im Nachweis, ist er
angreifbarer als Papier.
**Wann.** Im ersten Streitfall — also möglicherweise Jahre später.
**Gegenmaßnahme.** Kette und Zeitstempel binden ausschließlich den Server-Eingang. Die Gerätezeit wird
als „vom Gerät angegeben" gekennzeichnet, die Drift beim Sync gemessen und mitgeloggt. Maximale
Offline-Latenz 72 Stunden. Beobachtung durch Dritte offline ja, Selbst-Quiz offline nein.
**Ungeprüft.** Ob die Trennlinie in der Praxis hält, wenn die Objektleitung im Funkloch auch die
Quittierungen der Teilnehmenden entgegennimmt. Wie Sync-Konflikte aufgelöst werden, ohne die Kette zu
beschädigen. Ob 72 Stunden zu lang oder zu kurz sind.

## L7 — Der Praxischeck ist eine Beurteilung ohne Gegenzeichnung
**Was bricht.** Fünf bis acht Verhaltensanker mit K.-o.-Kriterien, erfasst über den Kopf der beurteilten
Person hinweg. Die betriebsverfassungsrechtliche Seite entfällt mangels Gremium — das Fairnessproblem
nicht.
**Wann.** Beim ersten Widerspruch.
**Gegenmaßnahme.** Quittierung „zur Kenntnis genommen" plus Freitext-Widerspruchsvermerk als
Pflichtschritt der Sitzung.
**Ungeprüft.** Ob ein Widerspruchsvermerk ohne unabhängige Stelle, an die er geht, mehr ist als eine
Geste. Wer ihn liest. Was passiert, wenn die beurteilende Objektleitung zugleich die einzige
Eskalationsinstanz ist.

## L8 — „Ein eigener Player ist schnell gebaut" ist eine Beruhigungspille
**Was bricht.** Die Umkehrbarkeit der Kaufentscheidung steht und fällt damit, dass ein einfacher Player
schnell nachrüstbar ist. Ursprünglich mit 1,5 PM veranschlagt, im Kritiker-Durchgang auf 3–4 PM ohne
Video korrigiert. Nicht gedeckt sind Autorenwerkzeug, Versionierung mit Korrekturpolicy,
Register × Sprache über alles, Piktogramm-Antworten, Medienauslieferung, Barrierefreiheit.
**Wann.** Wenn der Marktabgleich kein LMS mit brauchbarer Schnittstelle findet — der wahrscheinliche Fall.
**Gegenmaßnahme.** Umkehrbarkeit erzwingen statt behaupten: ein Content-Adapter mit genau vier
Operationen (Kurse listen, Version auflösen, Completion-Ereignis, Deep-Link) ab Tag 1, alles andere
hinter dieser Kante.
**Ungeprüft.** Ob vier Operationen ausreichen. Ob die Kante bei Versionierung und Register hält, oder ob
das Kauf-LMS diese Konzepte gar nicht kennt und die Kante damit leckt.

## L9 — Die Aufwandsschätzung ist Feature-Zeit, nicht Projektzeit
**Was bricht.** In den ursprünglichen 4 Personenmonaten fehlten Personalstamm-Sync und Matching,
Enrollment und Gerätehandling, Nachweis-Migration, Admin- und Pflege-UI, Offline-Sync-Konfliktauflösung,
Betrieb, Monitoring, Backup-Restore-Test, Tests, Betriebsdokumentation und die Zuarbeit zur
Datenschutz-Folgenabschätzung. Korrigiert auf 6–8 PM.
**Wann.** Ab Woche 6, schleichend.
**Gegenmaßnahme.** Entweder Scope halbieren oder die Zeitachse verdoppeln und das offen sagen.
**Ungeprüft.** Ob 6–8 PM immer noch zu optimistisch sind. Welche Position weiterhin fehlt.

## L11 — Der KI-Autoren-Copilot ist haftungsseitig ungesichert
**Was bricht.** Ein KI-erzeugter Sprechzettel mit falscher Angabe zur Schutzausrüstung wird zum
Rechtsnachweis. Einziger vorgesehener Schutz ist die Freigabe durch die Objektleitung, die
Gefahrstofffachtexte nicht validieren kann.
**Wann.** Beim ersten Gefahrstoff-Baustein.
**Gegenmaßnahme.** Entwürfe nur aus freigegebenen Quellen mit Quellenangabe je Aussage. Zwei-Augen-
Freigabe für Gefahrstoff- und Schutzausrüstungsinhalte durch die Fachkraft für Arbeitssicherheit.
Herkunfts- und Freigabemerkmal an jedem Block, im Audit sichtbar. Widerruf als eigener Kettenblock.
**Ungeprüft.** Ob „Quellenangabe je Aussage" bei einem generativen Modell überhaupt verlässlich
herstellbar ist oder nur plausibel aussieht. Wie ein Widerruf praktisch abläuft, wenn der fehlerhafte
Nachweis bereits an einen Kunden ausgeliefert wurde.

---

## Geschlossen oder entfallen — nur zur Vollständigkeit

- **L1** Objektleitung als Erfüllungsgehilfin — geschlossen: Zeit ist im Objektbudget hinterlegt,
  Pilotteilnahme ist freiwillig.
- **L3** „Darf hier arbeiten?" als Einsatzsteuerung — entschärft: kein Betriebsrat, damit kein
  §95-Konflikt. Die inhaltliche Auflage bleibt: deterministisch, Ausgabe als Tatsachenfeststellung mit
  Datum, keine Kopplung an den Dienstplan.
- **L5** Personalstamm als Quelle der Wahrheit — halb geschlossen: Personalnummer, Name und
  Austrittssignal kommen aus der Lohnbuchhaltung. Sprache und Objektzuordnung kommen nicht und müssen im
  neuen Dienst gepflegt werden.
- **L10** Kollision der Betriebsvereinbarung mit dem Zeitplan — entfällt: kein Betriebsrat. An ihre
  Stelle tritt eine Nutzungsrichtlinie als freiwillige Selbstbindung plus Datenschutz-Folgenabschätzung.
