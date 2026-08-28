/* ===== Inhalt: Sprache × Register (standard | einfach) =====
   Register ist bewusst eine eigene Dimension neben der Sprache —
   es gibt "Türkisch, einfach", nicht nur "Einfache Sprache" auf Deutsch. */
const LANGS = {
  de:{name:"Deutsch", tag:"DE", speech:"de-DE"},
  pl:{name:"Polski",  tag:"PL", speech:"pl-PL"},
  ro:{name:"Română",  tag:"RO", speech:"ro-RO"},
  tr:{name:"Türkçe",  tag:"TR", speech:"tr-TR"}
};

const UI = {
  de:{heute:"Heute",schicht:"Objekt Nordlicht · 5:30–9:30",anhoeren:"Anhören",pause:"Pause",
      weiter:"Weiter",fertig:"Fertig",frage:"Frage",von:"von",richtig:"Richtig.",leider:"Noch nicht.",
      nochmal:"Nochmal versuchen",bestaetigen:"Bestätigen",quittung:"Quittierung",
      quittungH:"Bitte bestätige, was stimmt",pinH:"Deine PIN",pinS:"Vier Ziffern",
      karte:"Meine Karte",learni:"Learni fragen",lernzeit:"Bezahlte Lernzeit heute",
      unterweisung:"Unterweisung",gehoert:"Gehört",erledigt:"Erledigt",offen:"Offen",
      kannIch:"Das kann ich",wissen:"Wissen",beobachtet:"Beobachtet",
      nachweis:"Mein Nachweis",gueltig:"Gültig bis",fragen:"Frag mich etwas …",
      hinweis:"Deine Fragen an Learni sieht niemand aus der Führung. Sie werden nach 24 Stunden gelöscht.",
      vorlesen:"Wird vorgelesen",sprache:"Sprache",einfach:"Einfache Sprache",
      willkommen:"Willkommen bei Zitzelsberger",scanne:"Scanne den Code am Putzwagen",
      dankeH:"Danke, Anna.",dankeS:"Deine Unterweisung ist gespeichert. Der Nachweis liegt in deiner Karte.",
      bezahlt:"Wird als Arbeitszeit vergütet.",dauer:"Ungefähr 4 Minuten. Du kannst alles anhören.",
      fbOk:"Genau deshalb wechselt ein Tuch nie den Bereich.",fbNo:"Kein Problem. Du kannst es so oft versuchen, wie du willst. Es wird nichts gezählt.",
      nachgesprochen:"Deine Objektleitung hat das eben vorgesprochen. Hier kannst du es so oft anhören, wie du willst.",
      keinRanking:"Keine Serie, keine Punkte, keine Rangliste. Was zählt, ist was du sicher kannst.",
      keinStift:"Es gibt keine Unterschrift mit dem Finger. Du bist angemeldet, das genügt.",
      postH:"In vier Wochen kommt Post.",postS:"Ein gedrucktes Können-Zeugnis mit deinem Namen, zweisprachig, unterschrieben von der Geschäftsführung. Nach Hause, auf Papier.",
      legende:"Grün heißt: jemand hat dir dabei zugesehen. Türkis heißt: du weißt, wie es geht.",
      karteNote:"„Gefahrstoffe & Dosierung“ steht auf „unter Aufsicht“, weil bisher nur der Wissenscheck vorliegt. Die nächste Stufe gibt es erst nach einem Praxischeck, nicht durch ein weiteres Quiz.",
      learniHi:"Hallo Anna. Ich erkläre dir Sachen aus den freigegebenen Unterlagen — in deiner Sprache, so einfach du willst."},
  pl:{heute:"Dzisiaj",schicht:"Obiekt Nordlicht · 5:30–9:30",anhoeren:"Słuchaj",pause:"Pauza",
      weiter:"Dalej",fertig:"Gotowe",frage:"Pytanie",von:"z",richtig:"Dobrze.",leider:"Jeszcze nie.",
      nochmal:"Spróbuj jeszcze raz",bestaetigen:"Potwierdź",quittung:"Potwierdzenie",
      quittungH:"Potwierdź, co się zgadza",pinH:"Twój PIN",pinS:"Cztery cyfry",
      karte:"Moja karta",learni:"Zapytaj Learni",lernzeit:"Płatny czas nauki dzisiaj",
      unterweisung:"Instruktaż",gehoert:"Wysłuchane",erledigt:"Zrobione",offen:"Otwarte",
      kannIch:"To potrafię",wissen:"Wiedza",beobachtet:"Zaobserwowane",
      nachweis:"Moje zaświadczenie",gueltig:"Ważne do",fragen:"Zapytaj mnie o coś …",
      hinweis:"Twoich pytań do Learni nikt z kierownictwa nie widzi. Są usuwane po 24 godzinach.",
      vorlesen:"Odczytywanie",sprache:"Język",einfach:"Prosty język",
      willkommen:"Witamy w Zitzelsberger",scanne:"Zeskanuj kod na wózku",
      dankeH:"Dziękujemy, Anna.",dankeS:"Twój instruktaż został zapisany. Zaświadczenie jest w Twojej karcie.",
      bezahlt:"Płatne jako czas pracy.",dauer:"Około 4 minuty. Możesz wszystkiego wysłuchać.",
      fbOk:"Właśnie dlatego ściereczka nigdy nie zmienia obszaru.",fbNo:"Nic się nie stało. Możesz próbować tyle razy, ile chcesz. Nic nie jest liczone.",
      nachgesprochen:"Twoja kierowniczka obiektu właśnie to omówiła. Tutaj możesz posłuchać tyle razy, ile chcesz.",
      keinRanking:"Bez serii, bez punktów, bez rankingu. Liczy się to, co potrafisz bezpiecznie zrobić.",
      keinStift:"Nie ma podpisu palcem. Jesteś zalogowana, to wystarczy.",
      postH:"Za cztery tygodnie przyjdzie list.",postS:"Drukowane zaświadczenie o umiejętnościach z Twoim imieniem, dwujęzyczne, podpisane przez zarząd. Do domu, na papierze.",
      legende:"Zielony znaczy: ktoś Ci się przyglądał. Turkusowy znaczy: wiesz, jak to zrobić.",
      karteNote:"„Substancje niebezpieczne i dozowanie” są na poziomie „pod nadzorem”, bo jest tylko test wiedzy. Następny poziom dopiero po sprawdzeniu w praktyce, nie przez kolejny test.",
      learniHi:"Cześć Anna. Wyjaśniam rzeczy z zatwierdzonych dokumentów — w Twoim języku, tak prosto, jak chcesz."},
  ro:{heute:"Astăzi",schicht:"Obiectiv Nordlicht · 5:30–9:30",anhoeren:"Ascultă",pause:"Pauză",
      weiter:"Continuă",fertig:"Gata",frage:"Întrebarea",von:"din",richtig:"Corect.",leider:"Încă nu.",
      nochmal:"Mai încearcă o dată",bestaetigen:"Confirmă",quittung:"Confirmare",
      quittungH:"Confirmă ce este adevărat",pinH:"PIN-ul tău",pinS:"Patru cifre",
      karte:"Cardul meu",learni:"Întreabă Learni",lernzeit:"Timp de învățare plătit azi",
      unterweisung:"Instruire",gehoert:"Ascultat",erledigt:"Finalizat",offen:"Deschis",
      kannIch:"Asta pot",wissen:"Cunoștințe",beobachtet:"Observat",
      nachweis:"Dovada mea",gueltig:"Valabil până la",fragen:"Întreabă-mă ceva …",
      hinweis:"Întrebările tale către Learni nu sunt vizibile pentru conducere. Se șterg după 24 de ore.",
      vorlesen:"Se citește",sprache:"Limba",einfach:"Limbaj simplu",
      willkommen:"Bine ai venit la Zitzelsberger",scanne:"Scanează codul de pe cărucior",
      dankeH:"Mulțumim, Anna.",dankeS:"Instruirea ta a fost salvată. Dovada este în cardul tău.",
      bezahlt:"Plătit ca timp de lucru.",dauer:"Aproximativ 4 minute. Poți asculta tot.",
      fbOk:"Exact de aceea o lavetă nu schimbă niciodată zona.",fbNo:"Nicio problemă. Poți încerca de câte ori vrei. Nu se numără nimic.",
      nachgesprochen:"Șefa de obiectiv tocmai a explicat asta. Aici poți asculta de câte ori vrei.",
      keinRanking:"Fără serii, fără puncte, fără clasament. Contează ce poți face în siguranță.",
      keinStift:"Nu există semnătură cu degetul. Ești autentificată, este suficient.",
      postH:"În patru săptămâni vine o scrisoare.",postS:"Un certificat de competențe tipărit, cu numele tău, bilingv, semnat de conducere. Acasă, pe hârtie.",
      legende:"Verde înseamnă: cineva te-a observat. Turcoaz înseamnă: știi cum se face.",
      karteNote:"„Substanțe periculoase și dozare” este la „sub supraveghere”, pentru că există doar testul de cunoștințe. Nivelul următor vine doar după o verificare practică, nu printr-un alt test.",
      learniHi:"Bună, Anna. Îți explic lucruri din documentele aprobate — în limba ta, cât de simplu vrei."},
  tr:{heute:"Bugün",schicht:"Nordlicht binası · 5:30–9:30",anhoeren:"Dinle",pause:"Duraklat",
      weiter:"Devam",fertig:"Bitti",frage:"Soru",von:"/",richtig:"Doğru.",leider:"Henüz değil.",
      nochmal:"Tekrar dene",bestaetigen:"Onayla",quittung:"Onay",
      quittungH:"Doğru olanı onayla",pinH:"PIN kodun",pinS:"Dört rakam",
      karte:"Kartım",learni:"Learni'ye sor",lernzeit:"Bugün ücretli öğrenme süresi",
      unterweisung:"Eğitim",gehoert:"Dinlendi",erledigt:"Tamamlandı",offen:"Açık",
      kannIch:"Bunu yapabilirim",wissen:"Bilgi",beobachtet:"Gözlemlendi",
      nachweis:"Belgem",gueltig:"Geçerlilik",fragen:"Bana bir şey sor …",
      hinweis:"Learni'ye sorduklarını yönetimden kimse göremez. 24 saat sonra silinir.",
      vorlesen:"Sesli okunuyor",sprache:"Dil",einfach:"Kolay dil",
      willkommen:"Zitzelsberger'e hoş geldin",scanne:"Temizlik arabasındaki kodu okut",
      dankeH:"Teşekkürler, Anna.",dankeS:"Eğitimin kaydedildi. Belge kartında.",
      bezahlt:"Çalışma süresi olarak ödenir.",dauer:"Yaklaşık 4 dakika. Her şeyi dinleyebilirsin.",
      fbOk:"Tam da bu yüzden bir bez asla alan değiştirmez.",fbNo:"Sorun değil. İstediğin kadar deneyebilirsin. Hiçbir şey sayılmıyor.",
      nachgesprochen:"Bina sorumlun bunu az önce anlattı. Burada istediğin kadar dinleyebilirsin.",
      keinRanking:"Seri yok, puan yok, sıralama yok. Önemli olan güvenle yapabildiklerin.",
      keinStift:"Parmakla imza yok. Giriş yaptın, bu yeterli.",
      postH:"Dört hafta içinde posta gelecek.",postS:"Adının yazdığı, iki dilli, yönetim tarafından imzalanmış basılı bir yeterlilik belgesi. Eve, kâğıt olarak.",
      legende:"Yeşil: biri seni izledi. Turkuaz: nasıl yapıldığını biliyorsun.",
      karteNote:"„Tehlikeli maddeler ve dozaj“ „gözetim altında“ seviyesinde, çünkü sadece bilgi testi var. Bir sonraki seviye ancak uygulamalı kontrolle gelir, başka bir testle değil.",
      learniHi:"Merhaba Anna. Onaylı belgelerden şeyleri açıklarım — kendi dilinde, istediğin kadar basit."}
};

const C = {
  de:{title:"Die Vier-Farben-Methode",
    std:["Die Vier-Farben-Methode verhindert Kreuzkontamination. Jeder Bereich hat eine eigene Tuchfarbe.",
         "Rot ist für Sanitärbereiche mit hoher Keimbelastung: WC-Becken und Urinale.",
         "Gelb ist für die übrigen Sanitärbereiche: Waschbecken, Armaturen, Spiegel.",
         "Grün ist für Küchen und Teeküchen. Blau ist für Büro- und Möbelflächen.",
         "Ein Tuch wechselt nie den Bereich. Benutzte Tücher kommen in den Abwurfsack."],
    ez:["Jede Farbe hat einen Platz.","Rot ist für das WC.","Gelb ist für das Waschbecken.",
        "Grün ist für die Küche. Blau ist für den Schreibtisch.",
        "Ein Tuch bleibt in seinem Bereich. Benutzte Tücher kommen in den Sack."],
    q:[{std:"Welche Farbe für das WC-Becken?",ez:"Welche Farbe für das WC?"},
       {std:"Ein Tuch war im Sanitärbereich. Wohin kommt es?",ez:"Das Tuch war im WC. Wohin kommt es?"},
       {std:"Welche Farbe für die Teeküche?",ez:"Welche Farbe für die Küche?"}],
    a:{rot:"Rot",gelb:"Gelb",gruen:"Grün",blau:"Blau",sack:"In den Abwurfsack",eimer:"Zurück in den Eimer",becken:"Zum Waschbecken"},
    quit:["Ich war bei der Unterweisung dabei.","Ich habe alles verstanden.","Ich konnte Fragen stellen."]},
  pl:{title:"Metoda czterech kolorów",
    std:["Metoda czterech kolorów zapobiega przenoszeniu zarazków. Każdy obszar ma własny kolor ściereczki.",
         "Czerwony to sanitariaty o wysokim skażeniu: muszle klozetowe i pisuary.",
         "Żółty to pozostałe sanitariaty: umywalki, armatura, lustra.",
         "Zielony to kuchnie i aneksy kuchenne. Niebieski to biurka i meble.",
         "Ściereczka nigdy nie zmienia obszaru. Zużyte ściereczki trafiają do worka."],
    ez:["Każdy kolor ma swoje miejsce.","Czerwony to WC.","Żółty to umywalka.",
        "Zielony to kuchnia. Niebieski to biurko.",
        "Ściereczka zostaje w swoim obszarze. Zużyte ściereczki wrzucamy do worka."],
    q:[{std:"Jaki kolor do muszli klozetowej?",ez:"Jaki kolor do WC?"},
       {std:"Ściereczka była w sanitariacie. Gdzie trafia?",ez:"Ściereczka była w WC. Gdzie trafia?"},
       {std:"Jaki kolor do aneksu kuchennego?",ez:"Jaki kolor do kuchni?"}],
    a:{rot:"Czerwony",gelb:"Żółty",gruen:"Zielony",blau:"Niebieski",sack:"Do worka",eimer:"Z powrotem do wiadra",becken:"Do umywalki"},
    quit:["Byłam na instruktażu.","Wszystko zrozumiałam.","Mogłam zadawać pytania."]},
  ro:{title:"Metoda celor patru culori",
    std:["Metoda celor patru culori previne contaminarea încrucișată. Fiecare zonă are propria culoare de lavetă.",
         "Roșu este pentru grupurile sanitare cu contaminare ridicată: vase de toaletă și pisoare.",
         "Galben este pentru restul grupurilor sanitare: chiuvete, baterii, oglinzi.",
         "Verde este pentru bucătării. Albastru este pentru birouri și mobilier.",
         "O lavetă nu schimbă niciodată zona. Lavetele folosite merg în sac."],
    ez:["Fiecare culoare are locul ei.","Roșu este pentru WC.","Galben este pentru chiuvetă.",
        "Verde este pentru bucătărie. Albastru este pentru birou.",
        "Laveta rămâne în zona ei. Lavetele folosite merg în sac."],
    q:[{std:"Ce culoare pentru vasul de toaletă?",ez:"Ce culoare pentru WC?"},
       {std:"Laveta a fost în zona sanitară. Unde merge?",ez:"Laveta a fost la WC. Unde merge?"},
       {std:"Ce culoare pentru bucătărie?",ez:"Ce culoare pentru bucătărie?"}],
    a:{rot:"Roșu",gelb:"Galben",gruen:"Verde",blau:"Albastru",sack:"În sac",eimer:"Înapoi în găleată",becken:"La chiuvetă"},
    quit:["Am participat la instruire.","Am înțeles totul.","Am putut pune întrebări."]},
  tr:{title:"Dört renk yöntemi",
    std:["Dört renk yöntemi çapraz bulaşmayı önler. Her alanın kendi bez rengi vardır.",
         "Kırmızı, yüksek mikrop yüküne sahip saniter alanlar içindir: klozet ve pisuvarlar.",
         "Sarı, diğer saniter alanlar içindir: lavabolar, armatürler, aynalar.",
         "Yeşil, mutfaklar içindir. Mavi, ofis ve mobilya yüzeyleri içindir.",
         "Bir bez asla alan değiştirmez. Kullanılan bezler atık torbasına gider."],
    ez:["Her rengin bir yeri vardır.","Kırmızı tuvalet içindir.","Sarı lavabo içindir.",
        "Yeşil mutfak içindir. Mavi masa içindir.",
        "Bez kendi alanında kalır. Kullanılan bezler torbaya gider."],
    q:[{std:"Klozet için hangi renk?",ez:"Tuvalet için hangi renk?"},
       {std:"Bez saniter alanda kullanıldı. Nereye gider?",ez:"Bez tuvalette kullanıldı. Nereye gider?"},
       {std:"Çay ocağı için hangi renk?",ez:"Mutfak için hangi renk?"}],
    a:{rot:"Kırmızı",gelb:"Sarı",gruen:"Yeşil",blau:"Mavi",sack:"Atık torbasına",eimer:"Kovaya geri",becken:"Lavaboya"},
    quit:["Eğitime katıldım.","Her şeyi anladım.","Soru sorabildim."]}
};

const QOPTS = [
  [{k:"rot",ic:"cloth",c:"#B4341F",ok:1},{k:"gelb",ic:"cloth",c:"#D9A227"},{k:"blau",ic:"cloth",c:"#2C5FA8"}],
  [{k:"sack",ic:"sack",ok:1},{k:"eimer",ic:"bucket"},{k:"becken",ic:"sink"}],
  [{k:"gruen",ic:"cloth",c:"#2E7D52",ok:1},{k:"rot",ic:"cloth",c:"#B4341F"},{k:"blau",ic:"cloth",c:"#2C5FA8"}]
];

/* ===== Objekte: 'grau = unbekannt' ist ein echter dritter Zustand (L2) ===== */
const OBJEKTE = [
  {id:"NOR",n:"Nordlicht Bürocampus",s:"12 Kräfte · Frühschicht",st:"rot",  note:"2 Kräfte ohne gültige Gefahrstoff-Unterweisung"},
  {id:"KLI",n:"Klinikum Haus C",     s:"9 Kräfte · Zweischicht", st:"gelb", note:"3 Unterweisungen laufen in 21 Tagen ab"},
  {id:"SCH",n:"Grundschule Ost",     s:"5 Kräfte · Nachmittag",  st:"gruen",note:"Alle Nachweise gültig"},
  {id:"LOG",n:"Logistikzentrum Süd", s:"14 Kräfte · Nachtschicht",st:"grau",note:"Altbestand aus Memberspot noch nicht migriert"},
  {id:"STA",n:"Stadtwerke Verwaltung",s:"7 Kräfte · Frühschicht", st:"gruen",note:"Alle Nachweise gültig"}
];

const TEAM = [
  {n:"Anna Kowalska",   i:"AK",lang:"PL",st:"offen", r:"Gefahrstoff-Unterweisung fehlt seit 14.08."},
  {n:"Elena Popescu",   i:"EP",lang:"RO",st:"offen", r:"Erstunterweisung fehlt — Eintritt 25.08."},
  {n:"Mehmet Yılmaz",   i:"MY",lang:"TR",st:"ok",    r:"Vollständig · nächste Auffrischung 12.03.2027"},
  {n:"Katarzyna Nowak", i:"KN",lang:"PL",st:"ok",    r:"Vollständig · nächste Auffrischung 04.11.2026"},
  {n:"Ion Marinescu",   i:"IM",lang:"RO",st:"ok",    r:"Vollständig · nächste Auffrischung 22.01.2027"}
];

const KRITERIEN = [
  {t:"Trennt Tuchfarben bereichsrein — kein Tuch wechselt den Bereich.",ko:false},
  {t:"Trägt die vorgeschriebene PSA: Handschuhe und Schutzbrille beim Umgang mit dem Sanitärreiniger.",ko:true},
  {t:"Dosiert nach Betriebsanweisung, ohne Augenmaß.",ko:false},
  {t:"Mischt keine zwei Reinigungsmittel.",ko:true},
  {t:"Sperrt den Nassbereich mit dem Warnaufsteller ab.",ko:true},
  {t:"Legt benutzte Tücher in den Abwurfsack, nicht zurück in den Eimer.",ko:false}
];

const SKILLS = [
  {k:0,lvl:3,ev:"both",bis:"12.03.2027"},
  {k:1,lvl:3,ev:"both",bis:"27.08.2027"},
  {k:2,lvl:2,ev:"knowledge",bis:"14.02.2027"},
  {k:3,lvl:1,ev:"knowledge",bis:"—"},
  {k:4,lvl:0,ev:"none",bis:"—"}
];
/* Skillnamen, Kompetenzstufen und erledigte Einheiten sind Inhalt und damit uebersetzbar --
   nicht Teil der UI-Lokalisierung. Das sind im Datenmodell zwei getrennte Ebenen. */
const SKILLN = {
  de:["Sanitär-Grundreinigung","Vier-Farben-Methode","Gefahrstoffe & Dosierung","Bodenpflegemaschine","Anleiten neuer Kolleginnen"],
  pl:["Sprzątanie sanitariatów","Metoda czterech kolorów","Substancje niebezpieczne i dozowanie","Maszyna do pielęgnacji podłóg","Wprowadzanie nowych koleżanek"],
  ro:["Curățenia grupurilor sanitare","Metoda celor patru culori","Substanțe periculoase și dozare","Mașina de întreținere pardoseli","Instruirea noilor colege"],
  tr:["Saniter temel temizlik","Dört renk yöntemi","Tehlikeli maddeler ve dozaj","Zemin bakım makinesi","Yeni çalışanlara rehberlik"]
};
const DONE = {
  de:["Arbeitssicherheit im Kundenobjekt","Verhalten bei Alarm"],
  pl:["Bezpieczeństwo pracy w obiekcie klienta","Zachowanie przy alarmie"],
  ro:["Securitatea muncii la client","Comportament în caz de alarmă"],
  tr:["Müşteri binasında iş güvenliği","Alarm durumunda davranış"]
};
const LVL = {
  de:["Noch nicht begonnen","Weiß, wie es geht","Unter Aufsicht","Kann selbstständig","Kann anleiten"],
  pl:["Jeszcze nie zaczęte","Wiem, jak to zrobić","Pod nadzorem","Potrafię samodzielnie","Potrafię uczyć innych"],
  ro:["Încă neînceput","Știu cum se face","Sub supraveghere","Pot lucra singură","Pot instrui pe alții"],
  tr:["Henüz başlanmadı","Nasıl yapıldığını biliyorum","Gözetim altında","Tek başıma yapabilirim","Başkasına öğretebilirim"]
};
