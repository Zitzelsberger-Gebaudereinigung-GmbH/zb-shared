const S={role:"ol",scr:"ol-objekte",lang:"de",ez:false,obj:OBJEKTE[0],qi:0,qAns:[],
         quit:[false,false,false],pin:"",ratings:{},widerspruch:false,chat:[],speaking:false,joined:1};
const t=()=>UI[S.lang], c=()=>C[S.lang], reg=()=>S.ez?"ez":"std";
const esc=s=>String(s).replace(/[&<>"]/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]));

/* ---- Sprachausgabe: nutzt die Browser-Stimme, keine externe Anfrage ---- */
function speak(text){
  if(!("speechSynthesis" in window)){S.speaking=false;render();return;}
  speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text);
  u.lang=LANGS[S.lang].speech; u.rate=.92;
  u.onend=()=>{S.speaking=false;render()};
  u.onerror=()=>{S.speaking=false;render()};
  S.speaking=true; speechSynthesis.speak(u); render();
}
function stopSpeak(){if("speechSynthesis" in window)speechSynthesis.cancel();S.speaking=false;render()}
function go(scr){stopSpeak();S.scr=scr;render();const v=document.querySelector(".view");if(v)v.scrollTop=0}

/* =================== Bildschirme =================== */
const SCR={

/* ---------- Objektleitung ---------- */
"ol-objekte":{bar:{t:"Meine Objekte",s:"Dienstag, 27.08. · 6:02 Uhr"},tabs:"ol",view:()=>`
  <div class="card sunk">
    <div class="eb">Heute zu tun</div>
    <div class="h">2 Kräfte brauchen eine Unterweisung, bevor sie anfangen.</div>
    <div class="tiny">Beides im Objekt Nordlicht — deine erste Station.</div>
  </div>
  <div class="eb">5 Objekte</div>
  ${OBJEKTE.map((o,i)=>`<button class="obj" data-obj="${i}">
      <span class="dot d-${o.st}"></span>
      <span class="ob"><span class="on">${esc(o.n)}</span><span class="os">${esc(o.note)}</span></span>
      <span class="oc">${o.id}</span></button>`).join("")}
  <div class="card sunk">
    <div class="tiny"><b>Grau</b> heißt <b>unbekannt</b>, nicht rot: Für das Logistikzentrum ist der Altbestand
    aus Memberspot noch nicht migriert. Eine Ampel, die am ersten Tag überall rot steht, glaubt nach einer
    Woche niemand mehr.</div>
  </div>`,
  note:{h:"Die Objektleitung sieht zuerst ihre Objekte — nicht einen Kurskatalog",
    chips:[["L1","gruen"],["L2","gruen"]],
    b:["Im ursprünglichen Konzept hat die Rolle <b>Objektleitung</b> im gesamten MVP keine einzige Funktion. Hier ist sie die erste Nutzerin: Der Einstiegsbildschirm ist die Ampel über ihre Objekte, nicht „Mein Lernen“.",
       "Der dritte Zustand <b>grau = unbekannt</b> ist kein Designdetail. Ohne migrierte Nachweishistorie wäre die Ampel am Tag 1 zu 100 % rot — und damit wertlos."],
    fix:"Migration der laufenden Nachweise ist Vorbedingung der Ampel, nicht Nachlauf."}},

"ol-objekt":{bar:{t:()=>S.obj.n,s:"Wer darf heute hier arbeiten?",back:"ol-objekte"},tabs:"ol",view:()=>`
  <div class="card">
    <div class="eb">Einsatz heute · Frühschicht</div>
    ${TEAM.map(p=>`<div class="person">
      <span class="av">${p.i}</span>
      <span class="pb"><span class="pn">${esc(p.n)}</span><span class="pr">${esc(p.r)}</span></span>
      <span class="pill ${p.st==="ok"?"p-gruen":"p-gelb"}">${p.st==="ok"?"vollständig":"offen"}</span>
    </div>`).join("")}
  </div>
  <div class="card sunk">
    <div class="tiny">Das System sagt <b>nicht</b> „darf nicht arbeiten“. Es nennt die fehlende Unterweisung
    mit Datum. Die Entscheidung trifft die Objektleitung — nicht der Algorithmus.</div>
  </div>
  <button class="btn" data-go="ol-briefing">Unterweisung durchführen</button>
  <button class="btn ghost" data-go="ol-nachweis">Nachweise für dieses Objekt</button>`,
  note:{h:"Erinnern statt sperren",
    chips:[["L3","gruen"],["EU AI Act","brand"]],
    b:["„Darf diese Person heute hier arbeiten?“ ist die Frage, die kein LMS am Markt beantwortet — und zugleich die heikelste: Als automatische Einsatzsteuerung wäre sie ein Hochrisiko-Anwendungsfall nach Anhang III des EU AI Act.",
       "Deshalb ist die Ausgabe bewusst eine <b>Tatsachenfeststellung mit Datum</b>, kein Urteil und keine Rangfolge. Kein Modell, kein Score, keine Kopplung an den Dienstplan."],
    fix:"Der Mensch entscheidet, das System erinnert."}},

"ol-briefing":{bar:{t:"Unterweisung",s:"Vier-Farben-Methode · mündlich",back:"ol-objekt"},tabs:"ol",view:()=>`
  <div class="card" style="border-color:var(--brand)">
    <div class="pill p-brand">Du sprichst — das System dokumentiert</div>
    <div class="sub">Gefahrstoff- und Biostoffunterweisungen müssen <b>mündlich</b> und arbeitsplatzbezogen
    erfolgen. Der Sprechzettel unterstützt dich; er ersetzt dich nicht.</div>
  </div>
  <div class="eb">Sprechzettel · Objekt Nordlicht</div>
  <div class="script">
    ${C.de.ez.map((l,i)=>`<div class="l"><span class="n">${i+1}</span><span>${esc(l)}</span></div>`).join("")}
    <div class="l"><span class="n">!</span><span><b>Objektspezifisch:</b> Im 2. OG steht der Sanitärreiniger
    im abschließbaren Schrank neben dem Aufzug. Schlüssel hat nur die Frühschicht.</span></div>
  </div>
  <div class="card">
    <div class="eb">Teilnehmende</div>
    <div class="h" style="font-size:.94rem">${S.joined} von 5 beigetreten</div>
    <div class="qr"><div class="qrbox">${qrSvg()}</div>
      <div class="tiny" style="text-align:center">Code am Putzwagen scannen —<br>kein Passwort, keine E-Mail-Adresse</div></div>
    <button class="btn quiet" data-join="1">Beitritt simulieren</button>
  </div>
  <button class="btn" data-go="ol-praxis">Weiter zum Praxischeck</button>`,
  note:{h:"Blended ist Pflicht, nicht Komfort",
    chips:[["§14 GefStoffV","rot"],["§14 BioStoffV","rot"]],
    b:["Der schwerste sachliche Fehler des Ursprungskonzepts: Es wollte die Unterweisung <b>ersetzen</b>. §14 Abs. 2 GefStoffV und BioStoffV verlangen eine mündliche, tätigkeitsbezogene Unterweisung vor Aufnahme der Tätigkeit. Reines E-Learning erfüllt das nicht.",
       "Dieser Bildschirm dreht die Rollen um: Die Objektleitung spricht, die Plattform liefert den Sprechzettel in Einfacher Sprache, protokolliert Teilnahme und Sprache — und macht daraus den Nachweis."],
    fix:"Der objektspezifische Baustein ist der eigentliche Kern. Eine Tabelle „locations“ allein reicht nicht."}},

"ol-praxis":{bar:{t:"Praxischeck",s:"Anna Kowalska · Objekt Nordlicht",back:"ol-briefing"},tabs:"ol",view:()=>`
  <div class="card sunk">
    <div class="tiny">Sechs beobachtbare Verhaltensanker. <b>Drei sind K.-o.-Kriterien</b> — ein Verstoß
    bedeutet nicht bestanden, unabhängig vom Rest.</div>
  </div>
  ${KRITERIEN.map((k,i)=>`<div class="crit">
    <div class="ct">${k.ko?'<span class="pill p-rot">K.o.</span>':'<span class="pill p-grau">Anker</span>'}<span>${esc(k.t)}</span></div>
    <div class="rate" data-crit="${i}">
      <button class="y" data-r="y" aria-pressed="${S.ratings[i]==="y"}">Erfüllt</button>
      <button class="m" data-r="m" aria-pressed="${S.ratings[i]==="m"}">Mit Hinweis</button>
      <button class="n" data-r="n" aria-pressed="${S.ratings[i]==="n"}">Nicht erfüllt</button>
    </div></div>`).join("")}
  <button class="confirm" data-wid aria-pressed="${S.widerspruch}">
    <span class="bx">${S.widerspruch?IC.check:""}</span>
    <span><b style="font-family:var(--ui)">Anna hat die Bewertung gesehen</b><br>
    <span class="tiny">Sie kann einen Widerspruchsvermerk hinterlassen. Pflichtschritt der Sitzung.</span></span>
  </button>
  <button class="btn" data-go="ol-nachweis" ${Object.keys(S.ratings).length<6||!S.widerspruch?"disabled":""}>
    Beobachtung speichern</button>
  <div class="tiny">Offline erfassbar. Die Beweiskette bindet den Server-Eingang, nicht die Gerätezeit.</div>`,
  note:{h:"Die einzige Tür zu „kann selbstständig“",
    chips:[["L7","gelb"],["Kernconstraint","brand"]],
    b:["Der Anspruch des Konzepts lautet: nicht „welcher Kurs wurde abgeschlossen“, sondern „welche Tätigkeit kann jemand nachweisbar sicher ausführen“. Ein Multiple-Choice-Quiz löst das nicht ein.",
       "Deshalb gilt hier eine Regel als <b>Datenbank-Constraint, nicht als Feature-Flag</b>: Ein Quiz setzt ein Skill maximal auf „weiß, wie es geht“. Die Stufe „kann selbstständig ausführen“ ist ausschließlich über einen Beobachtungsnachweis erreichbar.",
       "Die Gegenzeichnung ist kein Formalismus. Eine Beurteilung, die über den Kopf der beurteilten Person hinweg entsteht, ist unfair — mit oder ohne Betriebsrat."],
    fix:"Kippt dieser Constraint unter Auslieferungsdruck, ist das Ergebnis Memberspot mit besserem PDF."}},

"ol-nachweis":{bar:{t:"Nachweise",s:"Objekt Nordlicht · August 2026",back:"ol-objekt"},tabs:"ol",view:()=>`
  <div class="doc">
    <div class="dh"><span class="h" style="font-size:.9rem">Unterweisungsnachweis</span><span class="pill p-gruen">gültig</span></div>
    <div class="dr"><span>Person</span><span>Anna Kowalska</span></div>
    <div class="dr"><span>Unterweisung</span><span>Vier-Farben-Methode</span></div>
    <div class="dr"><span>Inhaltsversion</span><span>v4 · 2026-08-11</span></div>
    <div class="dr"><span>Form</span><span>mündlich + Verständniskontrolle</span></div>
    <div class="dr"><span>Unterweisende</span><span>M. Zitzelsberger</span></div>
    <div class="dr"><span>Sprache</span><span>Polnisch, einfach</span></div>
    <div class="dr"><span>Praxischeck</span><span>bestanden · 27.08.2026</span></div>
    <div class="dr"><span>Kettenblock</span><span>#4187 · prev 3f9a…c2</span></div>
    <div class="dr"><span>Server-Eingang</span><span>2026-08-27T06:41:19Z</span></div>
  </div>
  <div class="row">
    <button class="btn ghost">PDF erzeugen</button>
    <button class="btn ghost" data-go="aud-liste">Auditor-Link</button>
  </div>
  <div class="card sunk">
    <div class="eb">Lernzeit August</div>
    <div class="h" style="font-size:.94rem">47 Stunden · 12 Personen</div>
    <div class="tiny">Als Lohnexport für die Buchhaltung. Lernzeit ist Arbeitszeit — hier als saubere
    Abrechnung, nicht als Leistungsüberwachung.</div>
    <button class="btn quiet">Export für Lohnbuchhaltung</button>
  </div>
  <div class="card sunk">
    <div class="tiny"><b>Widerruf ist vorgesehen.</b> Stellt sich ein Inhalt als fehlerhaft heraus, wird der
    Nachweis über einen eigenen Kettenblock zurückgerufen — ein hash-verkettetes PDF, das man nicht
    zurückholen kann, wäre ein Haftungsrisiko.</div>
  </div>`,
  note:{h:"Der Nachweis, der die Papierliste im Kofferraum ersetzt",
    chips:[["L6","gelb"],["L11","gelb"]],
    b:["Das ist der Punkt, an dem die Objektleitung zuerst etwas <b>gewinnt</b> statt Mehrarbeit zu bekommen: Nachweis auf Knopfdruck, mit Inhaltsversion, Unterweisungsform und ausgewiesener Sprache — genau das fragt der Auditor.",
       "Zwei Details, die das Ursprungskonzept offen ließ: Die Beweiskette bindet ausschließlich den <b>Server-Eingang</b> (eine Gerätezeit ist manipulierbar), und es gibt einen <b>Widerruf</b> als eigenen Kettenblock."],
    fix:"Keine Canvas-Unterschrift. Sie beweist weder Identität noch Abwesenheit fremder Hilfe."}},

"ol-autor":{bar:{t:"Learni",s:"Baustein erstellen · Objekt Nordlicht"},tabs:"ol",view:()=>`
  <div class="card sunk">
    <div class="eb">Foto + Sprachnotiz</div>
    <div class="row">
      <button class="btn quiet" style="flex-direction:column;gap:5px;padding:16px 8px">
        <span style="width:22px;height:22px;display:block">${IC.cam}</span><span style="font-size:.76rem">Foto</span></button>
      <button class="btn quiet" style="flex-direction:column;gap:5px;padding:16px 8px">
        <span style="width:22px;height:22px;display:block">${IC.mic}</span><span style="font-size:.76rem">Einsprechen</span></button>
    </div>
    <div class="tiny">„Der Sanitärreiniger steht im 2. OG im abschließbaren Schrank neben dem Aufzug.“ · 0:14</div>
  </div>
  <div class="card">
    <div class="pill p-brand">Entwurf · noch nicht freigegeben</div>
    <div class="h" style="font-size:.94rem">Gefahrstoffe im Objekt Nordlicht</div>
    <div class="sub">Learni hat aus deiner Sprachnotiz einen Baustein gebaut: Text in Einfacher Sprache,
    Übersetzung nach PL, RO und TR, dazu drei Verständnisfragen mit Piktogrammen.</div>
    <div class="src">${IC.doc}<span>Quelle je Aussage: Betriebsanweisung BA-014, Sicherheitsdatenblatt Sanitärreiniger S2</span></div>
  </div>
  <div class="guard"><b>Zwei-Augen-Freigabe erforderlich.</b> Gefahrstoff- und PSA-Inhalte gibt die Fachkraft
  für Arbeitssicherheit frei, nicht die Objektleitung allein. Bis dahin bleibt der Baustein Entwurf.</div>
  <div class="row"><button class="btn ghost">Bearbeiten</button><button class="btn" disabled>Zur Freigabe</button></div>`,
  note:{h:"Learni verdient sein Geld beim Autor, nicht im Chat",
    chips:[["L11","gelb"],["Content-Engpass","brand"]],
    b:["Es gibt im Unternehmen keinen Content Author in Vollzeit und wird keinen geben. Genau hier liegt der größte KI-Hebel: Foto plus Sprachnotiz werden zu Text, Einfacher Sprache, Übersetzung und Prüffragen — in fünf Minuten, am Handy, im Objekt.",
       "Und genau hier entsteht das Haftungsrisiko. Ein KI-erzeugter Sprechzettel mit falscher PSA-Angabe würde zum Rechtsnachweis. Deshalb: Entwürfe nur aus freigegebenen Quellen, Quellenangabe je Aussage, Zwei-Augen-Freigabe."],
    fix:"generated_by_ai und approved_by hängen an jedem Block und sind im Audit sichtbar."}},

/* ---------- Mitarbeiterin ---------- */
"ma-qr":{bar:null,tabs:null,view:()=>`
  <div style="display:flex;flex-direction:column;gap:16px;padding-top:14px">
    <div style="text-align:center;display:flex;flex-direction:column;gap:6px">
      <div class="h">${esc(t().willkommen)}</div>
      <div class="sub">${esc(t().scanne)}</div>
    </div>
    <div class="qr"><div class="qrbox">${qrSvg()}</div></div>
    <button class="btn" data-go="ma-pin">${esc(t().weiter)}</button>
    <div class="card sunk"><div class="tiny">Kein Passwort, keine E-Mail-Adresse. Die Identität hat die
    Objektleitung beim Eintritt persönlich festgestellt und protokolliert — das ist der Anker,
    nicht eine Mobilfunknummer.</div></div>
  </div>`,
  note:{h:"Anmelden im Tiefgeschoss, ohne Netz und ohne Passwort",
    chips:[["L4","gelb"]],
    b:["Ein SMS-Einmalcode funktioniert genau dort nicht, wo gereinigt wird — und eine Mobilfunknummer beweist Gerätebesitz, nicht Identität. Bei Prepaid-Karten, geteilten Familiengeräten und rund 200 Nummernwechseln pro Jahr trägt sie keinen Rechtsnachweis.",
       "Deshalb: Die Identität wird <b>einmalig durch die Objektleitung</b> festgestellt, danach gilt ein langlebiger Gerätetoken mit persönlicher PIN. Wer kein eigenes Smartphone hat, quittiert am Tablet der Objektleitung."],
    fix:"Enrollment im Beisein, protokolliert — das ist der Identitätsanker."}},

"ma-pin":{bar:{t:()=>t().pinH,s:()=>t().pinS,back:"ma-qr"},tabs:null,view:()=>`
  <div style="display:flex;flex-direction:column;gap:20px;padding-top:20px">
    <div class="pin">${[0,1,2,3].map(i=>`<i class="${S.pin.length>i?"f":""}"></i>`).join("")}</div>
    <div class="keys">
      ${[1,2,3,4,5,6,7,8,9].map(n=>`<button data-pin="${n}">${n}</button>`).join("")}
      <button data-pin="del" style="font-size:.8rem">←</button>
      <button data-pin="0">0</button>
      <button data-pin="ok" style="background:var(--brand);color:#fff">${IC.check}</button>
    </div>
  </div>`,
  note:{h:"Vier Ziffern statt E-Mail und Passwort",chips:[["L4","gelb"]],
    b:["Die PIN ist persönlich und wird nie im Selfservice zurückgesetzt — ein Reset läuft über die Objektleitung, die die Identität ohnehin schon einmal festgestellt hat.",
       "Ein geteiltes Gerät ist ein eigener Modus mit kurzer Sitzung, kein Sonderfall, den man übersieht."]}},

"ma-heute":{bar:{t:()=>t().heute,s:()=>t().schicht},tabs:"ma",view:()=>`
  <div class="card sunk">
    <div class="eb">${esc(t().lernzeit)}</div>
    <div class="h">12 min</div>
    <div class="tiny">${esc(t().bezahlt)}</div>
  </div>
  <div class="card" style="border-color:var(--brand)">
    <div class="pill p-brand">${esc(t().unterweisung)}</div>
    <div class="h">${esc(c().title)}</div>
    <div class="sub">${esc(t().dauer)}</div>
    <button class="btn" data-go="ma-hoeren">${esc(t().anhoeren)}</button>
  </div>
  <div class="card">
    <div class="eb">${esc(t().erledigt)}</div>
    <div class="skill"><span class="dot d-gruen"></span><span class="sn">
      <span class="snn">${esc(DONE[S.lang][0])}</span>
      <span class="sl">${esc(t().gueltig)} 04.11.2026</span></span></div>
    <div class="skill"><span class="dot d-gruen"></span><span class="sn">
      <span class="snn">${esc(DONE[S.lang][1])}</span>
      <span class="sl">${esc(t().gueltig)} 19.06.2027</span></span></div>
  </div>
  <div class="card sunk">
    <div class="tiny">${esc(t().keinRanking)}</div>
  </div>`,
  note:{h:"Kein Streak, kein Punktestand, keine Rangliste",
    chips:[["Motivation","brand"]],
    b:["Das Ursprungskonzept hatte das öffentliche Ranking richtigerweise gestrichen — und dann eine <b>Lernserie</b> eingebaut. Eine Serie bestraft freie Tage, Krankheit und Teilzeit; sie bestraft also genau die Struktur dieses Jobs.",
       "Was bei dieser Zielgruppe tatsächlich wirkt: <b>bezahlte Lernzeit, sichtbar quittiert</b>, Statusgewinn im Team, physische Artefakte und Anerkennung durch die direkte Führungskraft."],
    fix:"Die 12 Minuten oben sind das stärkste Motiv auf diesem Bildschirm."}},

"ma-hoeren":{bar:{t:()=>c().title,s:()=>LANGS[S.lang].name+(S.ez?" · "+t().einfach:""),back:"ma-heute"},tabs:null,view:()=>{
  const lines=c()[reg()];
  return `
  <div class="audio">
    <button data-speak>${S.speaking?IC.pause:IC.play}</button>
    <div class="ab"><div class="at">${esc(S.speaking?t().vorlesen:t().anhoeren)}</div>
      <div class="wave ${S.speaking?"on":""}">${"<i></i>".repeat(7)}</div></div>
    <span class="lang">${LANGS[S.lang].tag}${S.ez?" · EZ":""}</span>
  </div>
  <div class="script">${lines.map((l,i)=>`<div class="l"><span class="n">${i+1}</span><span>${esc(l)}</span></div>`).join("")}</div>
  <div class="card sunk"><div class="tiny">${esc(t().nachgesprochen)}</div></div>
  <button class="btn" data-go="ma-frage">${esc(t().weiter)}</button>`},
  note:{h:"Audio-First ist Pflicht, nicht Komfortfunktion",
    chips:[["Register ≠ Sprache","brand"],["§12 ArbSchG","rot"]],
    b:["Funktionaler Analphabetismus liegt im Reinigungsgewerbe deutlich über dem Durchschnitt — häufig auch in der Erstsprache. Übersetzung allein löst das nicht: Wer nicht flüssig liest, für den ist jede Schriftoberfläche eine Hürde.",
       "Probieren Sie rechts die Umschalter. <b>Einfache Sprache ist eine eigene Dimension neben der Sprache</b>, keine vierte Übersetzung — sonst gäbe es kein „Türkisch, einfach“. Die Vorlesefunktion nutzt die Stimme des Geräts und funktioniert offline."],
    fix:"§12 ArbSchG verlangt eine Unterweisung in verständlicher Sprache. Das ist hier Rechtsvoraussetzung, nicht Komfort."}},

"ma-frage":{bar:{t:()=>t().frage+" "+(S.qi+1)+" "+t().von+" 3",s:()=>LANGS[S.lang].name,back:"ma-hoeren"},tabs:null,view:()=>{
  const q=c().q[S.qi], opts=QOPTS[S.qi], given=S.qAns[S.qi];
  return `
  <div class="audio" style="padding:9px 12px">
    <button data-speakq>${IC.play}</button>
    <div class="ab"><div class="at" style="font-size:.78rem">${esc(t().vorlesen)}</div></div>
  </div>
  <div class="h">${esc(q[reg()])}</div>
  <div class="picks">
    ${opts.map((o,i)=>{
      const cls=given==null?"":(o.ok?"ok":(given===i?"no":""));
      return `<button class="pick ${cls}" data-ans="${i}" ${given!=null?"disabled":""}>
        <span class="pi">${o.ic==="cloth"?PIK.cloth(o.c):PIK[o.ic]()}</span>
        <span class="pl">${esc(c().a[o.k])}</span>
        ${cls==="ok"?'<span class="mk">✓</span>':cls==="no"?'<span class="mk">✕</span>':""}</button>`}).join("")}
  </div>
  ${given!=null?`<div class="card ${opts[given].ok?"sunk":""}">
     <div class="h" style="font-size:.94rem">${esc(opts[given].ok?t().richtig:t().leider)}</div>
     <div class="tiny">${esc(opts[given].ok?t().fbOk:t().fbNo)}</div>
     </div>
     <button class="btn" data-next>${S.qi<2?esc(t().weiter):esc(t().quittung)}</button>
     ${!opts[given].ok?`<button class="btn ghost" data-retry>${esc(t().nochmal)}</button>`:""}`:""}`},
  note:{h:"Antworten, die man ohne Lesen erkennt",
    chips:[["Piktogramme","brand"],["Fairness","brand"]],
    b:["Die Frage wird vorgelesen, die Antworten sind <b>Piktogramme</b> — ein rotes Tuch, ein gelbes Tuch, ein Abwurfsack. Kein Freitext ist Bestehensvoraussetzung.",
       "Unbegrenzte Versuche, kein Zeitlimit, und die Objektleitung sieht nur <b>bestanden oder nicht bestanden</b> mit Datum — nie die einzelnen Antworten. Sonst prüft das System Deutschkenntnisse statt Hygienewissen, und die Einzelantworten wären Leistungsdaten."],
    fix:"Ein Quiz belegt Wissen. Handlungskompetenz belegt nur der Praxischeck."}},

"ma-quittung":{bar:{t:()=>t().quittung,s:()=>LANGS[S.lang].name,back:"ma-frage"},tabs:null,view:()=>`
  <div class="h">${esc(t().quittungH)}</div>
  ${c().quit.map((q,i)=>`<button class="confirm" data-quit="${i}" aria-pressed="${S.quit[i]}">
    <span class="bx">${S.quit[i]?IC.check:""}</span><span>${esc(q)}</span></button>`).join("")}
  <div class="card sunk"><div class="tiny">${esc(t().keinStift)}</div></div>
  <button class="btn" data-go="ma-fertig" ${S.quit.every(Boolean)?"":"disabled"}>${esc(t().bestaetigen)}</button>`,
  note:{h:"Was die Quittierung wirklich bestätigt",
    chips:[["Canvas gestrichen","rot"],["§14 GefStoffV","rot"]],
    b:["Das Ursprungskonzept ließ bestätigen: „Ich habe den Wissenscheck ohne Hilfe Dritter durchgeführt.“ Das beweist dem Betrieb nichts — es verschiebt Haftung nach unten, auf Menschen, die einen deutschen Satz unterschreiben, den sie nicht ganz verstehen.",
       "Hier wird das bestätigt, was rechtlich zählt und was die Person tatsächlich beurteilen kann: <b>Ich war dabei, ich habe verstanden, ich konnte fragen.</b> Das dokumentiert die mündliche Unterweisung — in ihrer Sprache."],
    fix:"Personalisierter Account plus Zeitstempel schlagen jede Fingerunterschrift."}},

"ma-fertig":{bar:null,tabs:"ma",view:()=>`
  <div style="text-align:center;padding-top:22px;display:flex;flex-direction:column;gap:9px;align-items:center">
    <div style="width:56px;height:56px;border-radius:50%;background:var(--gruen-w);color:var(--gruen);display:grid;place-items:center">
      <span style="width:28px;height:28px;display:block">${IC.check}</span></div>
    <div class="h">${esc(t().dankeH)}</div>
    <div class="sub">${esc(t().dankeS)}</div>
  </div>
  <div class="doc">
    <div class="dh"><span class="h" style="font-size:.86rem">${esc(t().nachweis)}</span><span class="pill p-gruen">${esc(t().gueltig)} 27.08.2027</span></div>
    <div class="dr"><span>${esc(t().unterweisung)}</span><span>${esc(c().title)} · v4</span></div>
    <div class="dr"><span>${esc(t().sprache)}</span><span>${LANGS[S.lang].name}${S.ez?" · "+t().einfach:""}</span></div>
  </div>
  <div class="card" style="border-color:var(--brand)">
    <div class="pill p-brand">Stolzbrief</div>
    <div class="h" style="font-size:.94rem">${esc(t().postH)}</div>
    <div class="sub">${esc(t().postS)}</div>
  </div>
  <button class="btn ghost" data-go="ma-karte">${esc(t().karte)}</button>`,
  note:{h:"Der Stolzbrief ist kein Nice-to-have",
    chips:[["Halten","gruen"]],
    b:["Er kostet fast nichts — die PDF- und Mailer-Bausteine liegen bereits in <span class='mono'>zb-shared</span>, Druck ist eine Dienstleistung. Und er ist das einzige Element, das dieses System auf der Gefühlsseite von einem Kontrollinstrument unterscheidet.",
       "Bei rund 400 T€ jährlichen Fluktuationskosten ist ein gedrucktes Zeugnis, das jemand seiner Familie zeigt, die billigste Gegenmaßnahme im ganzen Projekt. Er wird als „später“ markiert werden. Das darf er nicht."],
    fix:"Ein Badge im Browser existiert für diese Zielgruppe nicht. Papier existiert."}},

"ma-karte":{bar:{t:()=>t().karte,s:"Anna Kowalska"},tabs:"ma",view:()=>`
  <div class="card sunk">
    <div class="eb">${esc(t().kannIch)}</div>
    <div class="tiny">${esc(t().legende)}</div>
  </div>
  ${SKILLS.map(s=>`<div class="skill">
    <span class="sn"><span class="snn">${esc(SKILLN[S.lang][s.k])}</span>
      <span class="sl">${esc(LVL[S.lang][s.lvl])}${s.bis!=="—"?" · "+t().gueltig+" "+s.bis:""}</span>
      <span class="steps">${[1,2,3,4].map(i=>`<i class="${i<=s.lvl?(s.ev==="both"&&i>=3?"obs":"on"):""}"></i>`).join("")}</span></span>
    <span class="pill ${s.ev==="both"?"p-gruen":s.ev==="knowledge"?"p-brand":"p-grau"}">
      ${s.ev==="both"?esc(t().beobachtet):s.ev==="knowledge"?esc(t().wissen):"·"}</span>
  </div>`).join("")}
  <div class="card sunk"><div class="tiny">${esc(t().karteNote)}</div></div>`,
  note:{h:"Die Kann-Ich-Karte zeigt Stufen, keine Prozente",
    chips:[["Kompetenzmodell","brand"],["evidence_type","brand"]],
    b:["Der Prototyp des Ursprungskonzepts zeigte „Arbeitssicherheit 72 %“ und „Skill-Level 12“. Beides ist bedeutungsleer: Es fehlt die Niveaudimension mit Verhaltensankern — <b>angeleitet → unter Aufsicht → selbstständig → kann anleiten</b>.",
       "Die Farbe der Stufenbalken macht die Beweisart sichtbar: Türkis steht für Wissen, Grün für Beobachtung. Erst beides zusammen schaltet die Tätigkeitsfreigabe frei."],
    fix:"Skill-Daten dürfen keine Einsatz- oder Vergütungsentscheidung automatisch steuern."}},

"ma-learni":{bar:{t:"Learni",s:()=>LANGS[S.lang].name},tabs:"ma",chat:true,view:()=>`
  <div class="guard">${IC.lock}<b> ${esc(t().hinweis)}</b></div>
  <div class="bub l">${esc(t().learniHi)}</div>
  ${S.chat.map(m=>m.u
    ?`<div class="bub u">${esc(m.u)}</div>`
    :`<div class="bub l">${esc(m.l)}${m.src?`<div class="src">${IC.doc}<span>${esc(m.src)}</span></div>`:""}</div>`).join("")}
  ${S.chat.length===0?`<div style="display:flex;flex-wrap:wrap;gap:6px">
     <button class="btn quiet" style="width:auto;font-size:.78rem;padding:8px 12px" data-ask="foto">Was ist in dieser Flasche?</button>
     <button class="btn quiet" style="width:auto;font-size:.78rem;padding:8px 12px" data-ask="haut">Mir brennt die Haut</button>
   </div>`:""}`,
  note:{h:"Ein Wächter, kein Gesprächspartner",
    chips:[["Guardrail","gelb"],["Art. 9 DSGVO","rot"]],
    b:["Sokratisches Tutoring bei Deutsch A2 um 5:30 Uhr mit dem Wischmopp in der anderen Hand erzeugt Scham und Abbruch. Der echte Nutzen ist banal und groß: <b>Foto der Flasche → was ist das, wo darf ich es benutzen, welche Schutzausrüstung.</b>",
       "Probieren Sie „Mir brennt die Haut“. Bei Gefahrstoff-, Verletzungs- und Arbeitszeitfragen generiert Learni <b>nichts</b> — es kommt hinterlegter Text plus ein Anruf-Button zur Objektleitung.",
       "Und der Chat ist für Vorgesetzte technisch unlesbar, nicht per Berechtigung: Freitext kann Gesundheitsdaten enthalten. Ohne Betriebsrat gibt diese Zusage niemand außer der Geschäftsführung — also muss sie im Datenmodell stehen, nicht in einer Richtlinie."],
    fix:"Wenn jemand die Fragen mitlesen kann, fragt niemand mehr etwas."}},

/* ---------- Auditor ---------- */
"aud-liste":{bar:{t:"Nachweise",s:"Read-only · Link läuft am 26.09.2026 ab"},tabs:null,view:()=>`
  <div class="card sunk">
    <div class="eb">Freigegeben für</div>
    <div class="h" style="font-size:.94rem">Kundenaudit Nordlicht Bürocampus</div>
    <div class="tiny">Zeitraum 01.01.–27.08.2026 · nur Unterweisungsnachweise · keine Lernverläufe,
    keine Einzelantworten, keine Chatinhalte.</div>
  </div>
  <div class="card">
    ${TEAM.map(p=>`<div class="person">
      <span class="av">${p.i}</span>
      <span class="pb"><span class="pn">${esc(p.n)}</span>
      <span class="pr">Vier-Farben-Methode v4 · mündlich + Verständniskontrolle</span></span>
      <span class="lang">${p.lang}</span>
      <span class="pill ${p.st==="ok"?"p-gruen":"p-gelb"}">${p.st==="ok"?"gültig":"offen"}</span>
    </div>`).join("")}
  </div>
  <div class="card sunk">
    <div class="eb">Prüfbar</div>
    <div class="tiny">Jeder Nachweis trägt einen Verifikations-QR. Die Hash-Kette lässt sich unabhängig
    nachrechnen — auch für widerrufene Nachweise, die als widerrufen sichtbar bleiben.</div>
  </div>`,
  note:{h:"Der Auditor bekommt einen Link, keine PDF-Mail",
    chips:[["Datenminimierung","brand"]],
    b:["Read-only, mit Ablaufdatum, auf einen Zeitraum und ein Objekt begrenzt — und ausschließlich auf Nachweise. Lernverläufe, Einzelantworten und Chatinhalte sind gar nicht Teil dieser Sicht.",
       "Das ist gleichzeitig Datenschutz und Vertrieb: Genau diese Nachweisfähigkeit wird in Ausschreibungen abgefragt, und sie ist der Teil, den kein Standard-LMS liefert, weil keines Objekt, Rolle, Sprache und Beobachtung zugleich kennt."],
    fix:"Ein append-only Log in derselben Datenbank, in der der Admin schreibt, ist ohne Hash-Kette nicht manipulationssicher."}}
};

function qrSvg(){
  const cells=[[0,0,1,1,1,1,1,0,1,0,1,1,1,1,1],[0,0,1,0,0,0,1,0,0,1,1,0,0,0,1],
  [0,0,1,0,1,0,1,0,1,1,1,0,1,0,1],[0,0,1,0,1,0,1,1,0,0,1,0,1,0,1],[0,0,1,0,0,0,1,0,1,1,1,0,0,0,1],
  [0,0,1,1,1,1,1,0,1,0,1,1,1,1,1],[0,0,0,0,0,0,0,0,1,1,0,0,0,0,0],[1,0,1,1,0,1,1,1,0,1,1,0,1,1,0],
  [0,1,1,0,1,0,0,1,1,0,0,1,0,1,1],[1,1,0,1,0,1,1,0,1,1,0,1,1,0,0],[0,0,0,0,0,0,0,0,1,0,1,1,0,1,1],
  [0,0,1,1,1,1,1,0,1,1,0,0,1,0,1],[0,0,1,0,0,0,1,0,0,1,1,0,1,1,0],[0,0,1,0,1,0,1,0,1,0,1,1,0,1,1],
  [0,0,1,1,1,1,1,0,1,1,0,1,1,0,1]];
  let r="";
  cells.forEach((row,y)=>row.forEach((v,x)=>{if(v)r+=`<rect x="${x*8}" y="${y*8}" width="8" height="8"/>`}));
  return `<svg viewBox="0 0 120 120" width="100%" height="100%" fill="#10242C" aria-label="QR-Code am Putzwagen">${r}</svg>`;
}
