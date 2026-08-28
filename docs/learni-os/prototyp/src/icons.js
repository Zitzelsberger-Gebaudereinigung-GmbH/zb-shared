const svg=(d,extra="")=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" ${extra}>${d}</svg>`;
const IC={
  back:svg('<path d="M15 18l-6-6 6-6"/>'),
  play:svg('<path d="M8 5.5v13l11-6.5z" fill="currentColor" stroke="none"/>'),
  pause:svg('<rect x="7" y="5.5" width="3.4" height="13" rx="1" fill="currentColor" stroke="none"/><rect x="13.6" y="5.5" width="3.4" height="13" rx="1" fill="currentColor" stroke="none"/>'),
  mic:svg('<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3"/>'),
  check:svg('<path d="M5 12.5l4.5 4.5L19 7"/>'),
  home:svg('<path d="M3.5 10.5L12 3.5l8.5 7M5.5 9.5V20h13V9.5"/>'),
  card:svg('<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="M3 10h18M7 14.5h4"/>'),
  chat:svg('<path d="M20.5 12c0 4.1-3.8 7.3-8.5 7.3-1 0-2-.15-2.9-.4L4 20.5l1.7-3.7C4.3 15.5 3.5 13.8 3.5 12 3.5 7.9 7.3 4.7 12 4.7s8.5 3.2 8.5 7.3z"/>'),
  doc:svg('<path d="M6 2.8h8l4.5 4.5v13.9H6z"/><path d="M13.8 2.8v4.7h4.7M9 13h6M9 16.5h4"/>'),
  layers:svg('<path d="M12 3.2l8.5 4.6L12 12.4 3.5 7.8z"/><path d="M3.5 12l8.5 4.6 8.5-4.6M3.5 16.2l8.5 4.6 8.5-4.6"/>'),
  eye:svg('<path d="M2.5 12S6 5.8 12 5.8 21.5 12 21.5 12 18 18.2 12 18.2 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="2.9"/>'),
  cam:svg('<path d="M3.5 8h3.2l1.4-2h7.8l1.4 2h3.2v11.5H3.5z"/><circle cx="12" cy="13.2" r="3.4"/>'),
  spark:svg('<path d="M12 3.5l1.9 5.1 5.1 1.9-5.1 1.9L12 17.5l-1.9-5.1L5 10.5l5.1-1.9z"/><path d="M18.6 16.4l.7 1.9 1.9.7-1.9.7-.7 1.9-.7-1.9-1.9-.7 1.9-.7z"/>'),
  lock:svg('<rect x="4.5" y="10.2" width="15" height="10.3" rx="2.2"/><path d="M8 10.2V7.4a4 4 0 0 1 8 0v2.8"/>'),
  clock:svg('<circle cx="12" cy="12" r="8.6"/><path d="M12 7.2V12l3.1 2"/>')
};
/* Piktogramme für Antwortoptionen — Antworten ohne Lesen erkennbar */
const PIK={
  cloth:c=>`<svg viewBox="0 0 44 44" aria-hidden="true"><rect x="4" y="7" width="36" height="30" rx="5" fill="${c}"/><path d="M4 22h36" stroke="rgba(255,255,255,.55)" stroke-width="2"/><path d="M13 7v30M31 7v30" stroke="rgba(255,255,255,.3)" stroke-width="1.6"/></svg>`,
  sack:()=>`<svg viewBox="0 0 44 44" aria-hidden="true"><path d="M14 13h16l4 24H10z" fill="#3E555E"/><path d="M14 13c0-3 3.5-5 8-5s8 2 8 5" fill="none" stroke="#3E555E" stroke-width="2.6"/><path d="M16 21h12" stroke="rgba(255,255,255,.5)" stroke-width="2"/></svg>`,
  bucket:()=>`<svg viewBox="0 0 44 44" aria-hidden="true"><path d="M9 15h26l-3.5 22h-19z" fill="#2C5FA8"/><path d="M11 12c1-3 5.5-5 11-5s10 2 11 5" fill="none" stroke="#2C5FA8" stroke-width="2.4"/><path d="M12 23h20" stroke="rgba(255,255,255,.45)" stroke-width="2"/></svg>`,
  sink:()=>`<svg viewBox="0 0 44 44" aria-hidden="true"><path d="M7 21h30v5c0 5-4 9-9 9h-12c-5 0-9-4-9-9z" fill="#6E848C"/><path d="M22 21v-7c0-2.5 2-4.5 4.5-4.5H31" fill="none" stroke="#6E848C" stroke-width="2.6"/><path d="M7 21h30" stroke="rgba(255,255,255,.5)" stroke-width="2"/></svg>`
};
