const ROLES=[
  {k:"ol", n:"Objektleitung", d:"14 Objekte · 60 Kräfte", first:"ol-objekte"},
  {k:"ma", n:"Anna Kowalska", d:"Reinigungskraft · PL · 20 h", first:"ma-qr"},
  {k:"aud",n:"Auditor",       d:"Read-only · Kundenaudit",  first:"aud-liste"}
];
const TABS={
  ol:[["ol-objekte","layers","Objekte"],["ol-briefing","doc","Unterweisen"],["ol-nachweis","card","Nachweise"],["ol-autor","spark","Learni"]],
  ma:[["ma-heute","home",()=>t().heute],["ma-karte","card",()=>t().karte],["ma-learni","chat","Learni"]]
};
const FLOW={
  ol:[["ol-objekte","Objekte"],["ol-objekt","Wer darf heute"],["ol-briefing","Unterweisung"],["ol-praxis","Praxischeck"],["ol-nachweis","Nachweis"],["ol-autor","Baustein bauen"]],
  ma:[["ma-qr","QR"],["ma-pin","PIN"],["ma-heute","Heute"],["ma-hoeren","Anhören"],["ma-frage","Fragen"],["ma-quittung","Quittierung"],["ma-fertig","Fertig"],["ma-karte","Kann-Ich-Karte"],["ma-learni","Learni"]],
  aud:[["aud-liste","Nachweisliste"]]
};
const val=v=>typeof v==="function"?v():v;

function render(){
  const sc=SCR[S.scr], bar=sc.bar;
  document.getElementById("roles").innerHTML=ROLES.map(r=>
    `<button class="role" data-role="${r.k}" aria-pressed="${S.role===r.k}">
       <span class="rn">${r.n}</span><span class="rd">${r.d}</span></button>`).join("");

  document.getElementById("screen").innerHTML=`
    <div class="statusbar"><span>6:0${S.joined} · Objekt Nordlicht</span><span>◧ 4G · 61 %</span></div>
    ${bar?`<div class="appbar">
        ${bar.back?`<button class="back" data-go="${bar.back}" aria-label="Zurück">${IC.back}</button>`:""}
        <span class="t">${esc(val(bar.t))}<span class="s">${esc(val(bar.s))}</span></span></div>`:""}
    <div class="view">${sc.view()}</div>
    ${sc.chat?`<div class="chatin"><input placeholder="${esc(t().fragen)}" aria-label="Frage an Learni">
        <button class="mic" aria-label="Sprechen">${IC.mic}</button></div>`:""}
    ${sc.tabs?`<div class="tabbar">${TABS[sc.tabs].map(([s,i,l])=>
        `<button data-go="${s}" aria-current="${S.scr===s}">${IC[i]}<span>${esc(val(l))}</span></button>`).join("")}</div>`:""}`;

  const n=sc.note;
  document.getElementById("rail").innerHTML=`
    <div class="ctrl">
      <div class="grp"><span class="gl">Sprache der Mitarbeiterin</span>
        <div class="seg">${Object.entries(LANGS).map(([k,l])=>
          `<button data-lang="${k}" aria-pressed="${S.lang===k}">${l.name}</button>`).join("")}</div></div>
      <div class="grp"><span class="gl">Register</span>
        <div class="seg">
          <button data-ez="0" aria-pressed="${!S.ez}">Standard</button>
          <button data-ez="1" aria-pressed="${S.ez}">Einfache Sprache</button></div></div>
    </div>
    <div class="grp" style="display:flex;flex-direction:column;gap:7px">
      <span class="gl" style="font-family:var(--mono);font-size:.62rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)">Bildschirme dieser Rolle</span>
      <div class="flow">${FLOW[S.role].map(([s,l])=>
        `<button data-go="${s}" aria-current="${S.scr===s}">${esc(l)}</button>`).join("")}</div>
    </div>
    ${n?`<div class="note">
      <div class="nh"><h3>${n.h}</h3>${(n.chips||[]).map(([c,k])=>
        `<span class="pill p-${k}">${esc(c)}</span>`).join("")}</div>
      <div class="nb">${n.b.map(p=>`<p>${p}</p>`).join("")}
        ${n.fix?`<div class="fixline"><span class="fl">Merksatz</span><span>${n.fix}</span></div>`:""}</div>
    </div>`:""}
    <div class="scope">
      <h3>Was dieser Prototyp ist — und was nicht</h3>
      <ul>
        <li>Klickbare Konzeptreferenz für den korrigierten Vertical Slice „grüne Objektmappe“. <b>Keine Produktionscodebasis.</b></li>
        <li>Es werden keine personenbezogenen Daten verarbeitet oder gespeichert. Alle Namen, Objekte und Nachweise sind erfunden.</li>
        <li>Die Vorlesefunktion nutzt die Sprachausgabe des Geräts. Ob eine Stimme für Polnisch, Rumänisch oder Türkisch vorhanden ist, entscheidet das Betriebssystem des Nutzers.</li>
        <li>Nicht enthalten, weil bewusst gestrichen: VR/AR-Lab, Open Badges, xAPI, eIDAS-Signatur, Lernserien, Punktestände, Ranglisten.</li>
      </ul>
    </div>`;
}

/* =================== Interaktion =================== */
document.addEventListener("click",e=>{
  const el=t2=>e.target.closest(t2);
  let x;
  if(x=el("[data-role]")){const r=ROLES.find(r=>r.k===x.dataset.role);S.role=r.k;go(r.first);return}
  if(x=el("[data-go]")){if(!x.disabled)go(x.dataset.go);return}
  if(x=el("[data-obj]")){S.obj=OBJEKTE[+x.dataset.obj];go("ol-objekt");return}
  if(x=el("[data-lang]")){S.lang=x.dataset.lang;stopSpeak();render();return}
  if(x=el("[data-ez]")){S.ez=x.dataset.ez==="1";stopSpeak();render();return}
  if(el("[data-join]")){S.joined=Math.min(5,S.joined+1);render();return}
  if(el("[data-speak]")){S.speaking?stopSpeak():speak(c()[reg()].join(" "));return}
  if(el("[data-speakq]")){speak(c().q[S.qi][reg()]+". "+QOPTS[S.qi].map(o=>c().a[o.k]).join(", "));return}
  if(x=el("[data-ans]")){S.qAns[S.qi]=+x.dataset.ans;render();return}
  if(el("[data-retry]")){S.qAns[S.qi]=null;render();return}
  if(el("[data-next]")){if(S.qi<2){S.qi++;render()}else go("ma-quittung");return}
  if(x=el("[data-quit]")){const i=+x.dataset.quit;S.quit[i]=!S.quit[i];render();return}
  if(el("[data-wid]")){S.widerspruch=!S.widerspruch;render();return}
  if(x=el("[data-r]")){S.ratings[+x.closest("[data-crit]").dataset.crit]=x.dataset.r;render();return}
  if(x=el("[data-pin]")){
    const k=x.dataset.pin;
    if(k==="del")S.pin=S.pin.slice(0,-1);
    else if(k==="ok"){if(S.pin.length===4){S.pin="";go("ma-heute")}return}
    else if(S.pin.length<4)S.pin+=k;
    if(S.pin.length===4){setTimeout(()=>{S.pin="";go("ma-heute")},260)}
    render();return}
  if(x=el("[data-ask]")){
    if(x.dataset.ask==="foto"){
      S.chat.push({u:"Was ist in dieser Flasche? 📷"});
      S.chat.push({l:"Das ist der Sanitärreiniger S2. Er ist nur für WC und Urinale. Zieh Handschuhe und Schutzbrille an. Misch ihn mit nichts anderem.",
                   src:"Betriebsanweisung BA-014 · Sicherheitsdatenblatt S2 · freigegeben 11.08.2026"});
    }else{
      S.chat.push({u:"Mir brennt die Haut"});
      S.chat.push({l:"Spül die Stelle sofort 10 Minuten mit fließendem Wasser. Zieh verschmutzte Kleidung aus. Melde es noch heute. Ich beantworte solche Fragen nicht selbst — sprich bitte mit deiner Objektleitung.",
                   src:"Hinterlegter Notfalltext · keine generierte Antwort"});
    }
    render();
    setTimeout(()=>{const v=document.querySelector(".view");if(v)v.scrollTop=v.scrollHeight},20);
    return}
});
document.addEventListener("keydown",e=>{if(e.key==="Escape")stopSpeak()});
window.addEventListener("beforeunload",()=>{if("speechSynthesis" in window)speechSynthesis.cancel()});
render();
