# LEARNI OS – Übergabepaket für Claude Code

## Auftrag
Baue **LEARNI OS** als production-grade, AI-native Learning Experience Platform für operative Mitarbeiter. Ziel ist perspektivisch die Ablösung von Memberspot. Die Plattform ist mobile-first, mehrsprachig, skill-native, XR-ready, accessibility-first sowie Privacy/Security/Compliance-by-Design.

Leitidee: Nicht „Welche Kurse wurden abgeschlossen?“, sondern „Welche Tätigkeit kann ein Mitarbeiter nachweisbar sicher ausführen?“

## Kernrollen
- Learner/Mitarbeiter
- Trainer/Content Author
- Manager/Objektleitung
- L&D/QM/Arbeitsschutz
- Admin
- Auditor (read-only)

RBAC serverseitig erzwingen; Tenant-Trennung und Supabase RLS sind Pflicht.

## Kernfunktionen
### Learning
Video, Text, Audio, PDF, interaktive Aufgaben, Flashcards, Quiz, Szenarien, AI Practice, AR, VR/3D und Praxisnachweise. Struktur: Course → Module → Learning Unit → Blocks → Assessment → Skill/Credential. Veröffentlichte Fassungen erhalten unveränderliche `content_version`.

### Learni – KI-Lerncoach
Learni ist ein Orchestrator, kein fest verdrahtetes Modell:
- RAG aus freigegebenem Unternehmenswissen mit Quellen
- erklären, vereinfachen, übersetzen, zusammenfassen
- Übungen und Lernkarten
- Socratic Tutoring
- später Voice-to-Voice
- transparente Lernempfehlungen
- AI Gateway zur austauschbaren Modellwahl

**Harte Regel:** Während eines als eigenständig markierten Wissenschecks darf Learni keine prüfungsrelevante Hilfe geben. Serverseitig über Assessment-Session-Policy erzwingen, nicht nur in der UI.

### Skills
Skill-Taxonomie, Rollenanforderungen, Skill-Level, Evidenz, Ablauf, Rezertifizierung, Skill Wallet. Architektur für Open Badges 3.0 und CLR 2.0 vorbereiten.

### Assessments
Single/Multiple Choice, True/False, Reihenfolge, Zuordnung, Bild-Hotspot, Freitext, Szenario und Praxischeck. Fragenpool, Randomisierung, Bestehensgrenze, Versuche, optionale Zeitlimits und versionsgebundene Ergebnisberechnung.

### Selbsterklärung & Signatur
Vor Abschluss:
„Ich bestätige, dass ich diese Lerneinheit selbst absolviert und den Wissenscheck ohne Hilfe Dritter durchgeführt habe.“

Speichern: user_id, assessment_session_id, course/content_version, declaration_version, declaration_text/hash, accepted_at, result, signature_method/reference, evidence_document_hash, audit_event.

Eine Canvas-Unterschrift ist nicht automatisch ein starker Identitätsnachweis. Signaturmethoden austauschbar modellieren: Login+Attestation, MFA/Step-up und bei erforderlichem Beweisniveau externer eIDAS-Vertrauensdienst. Rechtliche Eignung je Nachweistyp separat prüfen.

### XR
Abstrakte `immersive_activity`-Schnittstelle für WebXR, Smartphone-AR, Desktop-3D-Fallback, QR/NFC Deep Links und optional spätere Unity/WebGL-Integration. Keine Emotionserkennung oder verdecktes biometrisches/Verhaltens-Profiling.

## Tech-Stack
Empfehlung:
- Next.js + TypeScript + React
- Tailwind / zugängliches Component System
- PWA
- Supabase PostgreSQL + Auth + Storage + RLS
- pgvector
- serverseitiger AI Gateway
- Background Jobs/Queue für Übersetzung, Embeddings, Medien und Nachweise
- Object Storage
- OpenTelemetry/Sentry-kompatible Observability
- WebXR

Keine Provider-API-Keys im Browser.

## Zielarchitektur
```text
Web/PWA
  |
Next.js UI
  |
BFF/API
  +-- Auth/RBAC/RLS
  +-- Learning Service
  +-- Assessment Service
  +-- Skill/Credential Service
  +-- Evidence/Signature Service
  +-- Learni AI Gateway
  +-- Translation Service
  +-- XR Event Service
  +-- Audit Service
  |
PostgreSQL / Storage / Vector Index
  |
External adapters: LLM | Speech | Translation | Notifications | Trust/Signature
```

## Datenmodell Minimum
`organizations`, `profiles`, `organization_memberships`, `roles`, `permissions`, `teams`, `locations`, `courses`, `course_versions`, `modules`, `learning_units`, `content_blocks`, `translations`, `enrollments`, `learning_progress`, `learning_events`, `assessment_definitions`, `assessment_versions`, `questions`, `question_versions`, `assessment_sessions`, `assessment_answers`, `assessment_results`, `declarations`, `signature_evidence`, `skills`, `role_skill_requirements`, `learner_skills`, `credentials`, `credential_evidence`, `knowledge_sources`, `knowledge_chunks`, `ai_conversations`, `ai_messages`, `ai_usage_events`, `audit_events`, `retention_policies`, `deletion_requests`.

UUIDs; UTC; Tenant-Isolation via RLS.

## Mehrsprachigkeit
Drei Ebenen strikt trennen:
1. UI-i18n
2. redaktionell freigegebene Kursübersetzungen
3. AI-On-Demand-Übersetzung

Master-Inhalt besitzt stabile semantische ID. Übersetzung hängt an Content-Version + Locale. Initial DE, EN, FR, PL. Sicherheitskritische KI-Übersetzungen benötigen Review/Freigabe und dürfen nie still als freigegeben gelten. Zusätzlich „Einfache Sprache“.

## AI Gateway
```ts
interface AIProvider {
  chat(input: ChatInput): Promise<ChatResult>
  embed(input: EmbedInput): Promise<EmbedResult>
}
```
Policy Layer vor Provider: Tenant Policy, Use-Case-Freigabe, Assessment Lock, PII-Minimierung, Retrieval Scope, Model Routing, Prompt-Version, Safety, Rate/Cost Limits.

RAG: Query → Authorization Filter → Hybrid Retrieval → Rerank → Context → Answer → Citations.

## DSGVO-Leitplanken
Datenminimierung, Zweckbindung, Privacy by Default, Rollen/Rechte, Verschlüsselung, Retention/Löschung, Betroffenenrechte, Audit Logs, Subprocessor-Inventar, bevorzugte EU-Datenresidenz und keine Freigabe von Mitarbeiter-/Unternehmensdaten zum Modelltraining. AI-Chat-Retention standardmäßig kurz und konfigurierbar. DPIA-Trigger dokumentieren. Finale Rechtsgrundlagen, Aufbewahrung, Mitbestimmung und Signaturbeweiswert juristisch prüfen.

## EU AI Act
- AI Literacy als eigener Lernpfad
- KI-Interaktion transparent kennzeichnen
- Quellen/Unsicherheit bei relevanten Antworten
- Human Oversight
- AI Inventory / Model Registry
- Modell-/Prompt-/Policy-Versionierung
- Risikoklassifizierung je AI Use Case
- keine Emotionserkennung am Arbeitsplatz
- keine verdeckte Persönlichkeits-/Leistungsbewertung
- keine alleinige folgenreiche Personalentscheidung durch Learni

## Security
OWASP-ASVS-orientiert, serverseitige Autorisierung, RLS, MFA/Step-up für sensible Aktionen, CSP, sichere Cookies, Upload-Validierung, Malware-Scanning-Pipeline, Rate Limits, Secrets serverseitig, append-orientierter Audit Trail, Dependency/Secret Scanning, Backup/Restore-Tests.

## Employee Experience
Navigation maximal: **Mein Lernen · Entdecken · Learni · Skills · Profil**.
Dashboard-Reihenfolge: notwendige Handlung → fortsetzen → Empfehlung → Entwicklung.
Kein öffentliches Mitarbeiterranking. WCAG 2.2 AA als Ziel, Untertitel, Transkripte, Tastatur/Screenreader, ausreichender Kontrast und Reduced Motion.

## Analytics
Erlaubt: Completion, Wissenscheck, Pflichtstatus, aggregierte Content-Qualität, Drop-off, Skill Coverage, Rezertifizierung.
Nicht Default: Produktivitätsscore, Emotion/Aufmerksamkeit, verdeckte Verhaltensprofile oder unnötig granulare Überwachung.

## Interoperabilität
Vorbereiten für xAPI/LRS, Open Badges 3.0, CLR 2.0, Verifiable Credentials, WebXR und Import aus dem bestehenden LMS.

## MVP – Definition of Done
- Auth
- Learner/Admin
- responsive PWA
- DE/EN/FR/PL Grundgerüst
- Course/Module/Unit CRUD
- Video + Text
- Progress
- Single/Multiple Choice Assessment
- eigenständige Assessment Session
- Selbsterklärung
- Signature-Evidence-Abstraktion
- versionsgebundener Abschlussnachweis
- Skill-Zuordnung
- Learni RAG + Quellen
- serverseitiger Assessment Lock
- Publishing/Versioning
- Audit Log
- RLS Tests
- Seed Demo
- E2E Happy Path

## Roadmap
**Phase 0 Foundation:** Repo, ADRs, CI, DB-Migrations, Auth, RLS, i18n, Design System.  
**Phase 1 Core:** Authoring, Player, Progress, Assessments, Nachweise, Admin.  
**Phase 2 Learni:** Knowledge Ingestion, RAG, Citations, AI Gateway, Translation, AI Literacy.  
**Phase 3 Skills:** Taxonomie, Rollen, Ablauf/Rezertifizierung, Dashboards.  
**Phase 4 Immersive:** WebXR/AR Pilot, QR/NFC, 3D Fallback, XR Events.  
**Phase 5 Interop:** Open Badges 3.0, CLR 2.0, xAPI/LRS.

## Erster Vertical Slice
Implementiere vollständig:
**Login → Dashboard → Kurs → Video/Text → Learni-Frage mit Quelle → Assessment starten → Learni serverseitig sperren → Quiz → Selbsterklärung → Signatur/Evidence → Ergebnis → Skill/Nachweis → Audit Event.**

Tests:
- Tenant A kann niemals Daten von Tenant B lesen
- Learni beantwortet im eigenständigen Assessment keine prüfungsrelevanten Fragen
- Abschluss referenziert exakt die absolvierte Content-Version
- ungeprüfte sicherheitskritische Übersetzung ist sichtbar als ungeprüft markiert
- neuer Versuch erzeugt neue Session und überschreibt keine Historie

## Repo-Struktur
```text
/apps/web
/packages/ui
/packages/domain
/packages/ai
/packages/i18n
/packages/xr
/packages/testing
/supabase/migrations
/supabase/functions
/docs/adr
/docs/privacy
/docs/ai-governance
/docs/product
```

## ADRs zuerst
ADR-001 Multi-Tenancy  
ADR-002 Auth/RBAC/RLS  
ADR-003 Course Versioning  
ADR-004 Assessment Integrity  
ADR-005 Signature Evidence  
ADR-006 AI Gateway/RAG  
ADR-007 Translation Workflow  
ADR-008 Learning Event Model  
ADR-009 XR Strategy  
ADR-010 Retention/Audit

## Nicht im MVP
Gesichtserkennung, Emotionserkennung, automatisierte HR-Rankings, Webcam-Proctoring, QES-Eigenbau, vollständiges VR-Authoring-Studio, öffentliche Social Leaderboards und automatisierte Kündigungs-/Beförderungsentscheidungen.

## UX/Brand
`prototype.html` ist eine klickbare Konzeptreferenz, **keine Produktions-Codebasis**.
Primärfarbe: `#00A7B7`. Modern, freundlich, klar, mobile-first. Learni ist ein sympathischer KI-Lerncoach.

## Startprompt für Claude Code
1. Lies dieses Dokument vollständig.
2. Analysiere zuerst das vorhandene Repository; überschreibe nichts blind.
3. Erstelle `/docs/product/PRODUCT_SPEC.md`.
4. Erstelle ADR-001 bis ADR-010 als Entwürfe.
5. Erstelle priorisiertes Backlog Phase 0/1.
6. Prüfe den Stack und dokumentiere begründete Abweichungen.
7. Entwirf DB-Schema + RLS-Strategie.
8. Erstelle Threat Model und Privacy/Data-Flow-Übersicht.
9. Implementiere danach den Vertical Slice.
10. Schreibe Unit-, Integration-, RLS- und E2E-Tests.
11. Bei erheblichen Datenschutz-, Security- oder Architekturentscheidungen: Optionen dokumentieren und nicht still riskante Annahmen treffen.
12. Qualitätsziel: production-grade, keine reine Demo.

## Definition für Claude
Wenn eine Anforderung unklar ist, bevorzuge:
**Datenschutz > Nachweisbarkeit > Sicherheit > Einfachheit für Mitarbeiter > Interoperabilität > Feature-Menge.**
