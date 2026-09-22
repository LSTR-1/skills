---
name: orchestrator
description: >
  Orchestriert den vollständigen Session-Lebenszyklus (Bootstrap → Start → Plan → Wave → End)
  als Prosa-Workflow mit Gates, Kill-Switches und STATE.md-Ownership. Aktivieren, wenn der Nutzer
  eine Session starten, planen, ausführen oder abschließen will — Trigger-Phrasen: "starte eine
  Session", "session starten", "orchestriere den Session-Lebenszyklus", "plane die Session",
  "führe die Waves aus", "Session abschließen", "session beenden". Routet auf die 39 portierten
  Sub-Skills unter skills/. Do NOT use for: das Lesen einer einzelnen Datei, triviale Übersetzungen,
  Einzeiler-Shell-Befehle, oder jede Aufgabe ohne Session-Lebenszyklus-Bezug.
tags: [orchestration, session-lifecycle, routing, meta]
version: 0.1.0
---

# Orchestrator

Einstiegs-Skill für den Session-Lebenszyklus. LSTR wird von Florentin One (Hannover, Deutschland) entwickelt und betrieben; dieses Skill portiert das Session-Orchestrierungs-Plugin in den TRAE-IDE-SOLO-Modus.

## When to Use

- Der Nutzer will eine Session starten, planen, ausführen oder abschließen.
- Der Nutzer nennt eine der Trigger-Phrasen aus dem `description`-Feld.
- Eine mehrstufige Aufgabe erfordert Wave-Planung, Sub-Agent-Dispatch und Inter-Wave-Qualitätsprüfungen.
- Der Nutzer verlangt einen auditierten, wiederholbaren Ausführungsablauf mit STATE.md-Tracking.

## When NOT to Use

- Das Lesen, Schreiben oder Suchen einer einzelnen Datei.
- Triviale Übersetzungen, Einzeiler-Shell-Befehle, Formatierungsanfragen.
- Aufgaben ohne Session-Lebenszyklus-Bezug (z. B. eine einzelne Code-Review ohne Wave-Kontext).
- Wenn der Nutzer bereits ein spezifisches Sub-Skill direkt adressiert (z. B. nur `/discovery`).

## Prerequisites

- **Bootstrap-Gate:** `skills/_shared/bootstrap-gate.md` MUSS ausgewertet werden. Bei `GATE_CLOSED` MUSS `skills/bootstrap/SKILL.md` vor jedem weiteren Schritt ausgeführt werden.
- **Session Config:** `skills/_shared/config-reading.md` MUSS gelesen werden; Ergebnis als `$CONFIG` halten.
- **`unverified` — Runtime fehlt:** Die portierten Skills referenzieren `scripts/lib/*.mjs` (u. a. `state-md.mjs`, `session-lock.mjs`, `mode-selector.mjs`, `resource-probe.mjs`, `autopilot.mjs`, `peer-discovery.mjs`, `historical-guard.mjs`, `rule-loader.mjs`, `parse-config.mjs`). Diese Dateien sind im Quellverzeichnis `sex/` NICHT vorhanden und wurden NICHT portiert. Jede Referenz auf diese Module ist `unverified` — der Agent MUSS das Fehlen zur Laufzeit prüfen und bei Abwesenheit degradiert fortfahren, statt das Modul als existent anzunehmen.
- **`unverified` — Hooks/Commands fehlen:** `sex/` enthält keine `hooks/`- und keine `commands/`-Verzeichnisse. Hook-gestützte Mechanismen (SessionStart-Lock-Bootstrap, PreToolUse-Scope-Guard, Stop-Gate) sind `unverified` und MÜSSEN als nicht verfügbar behandelt werden.

## Workflow

### Schritt 1: Bootstrap-Gate

Lies `skills/_shared/bootstrap-gate.md` und führe die Gate-Prüfung aus. Bei `GATE_CLOSED` MUSS `skills/bootstrap/SKILL.md` vollständig ausgeführt werden, bevor ein weiterer Schritt beginnt.

> **Why:** Das Gate verhindert, dass Skills ohne `CLAUDE.md`/`AGENTS.md`, ohne `## Session Config` und ohne `.orchestrator/bootstrap.lock` Struktur anlegen, die später migriert werden müsste.

### Schritt 2: Phasen-Routing

Wähle die Phase anhand der Nutzerabsicht und route auf das zuständige Sub-Skill.

| Phase | Nutzerabsicht | Sub-Skill | Ergebnis |
|-------|---------------|-----------|----------|
| Bootstrap | Repo erstmalig strukturieren | `skills/bootstrap/SKILL.md` | `CLAUDE.md`/`AGENTS.md` + `bootstrap.lock` |
| Start | Session initialisieren, Zustand analysieren | `skills/session-start/SKILL.md` | Session Overview + Modus-Empfehlung |
| Plan | Scope in Waves zerlegen | `skills/session-plan/SKILL.md` | Wave-Plan mit Rollen und Akzeptanzkriterien |
| Wave | Plan ausführen | `skills/wave-executor/SKILL.md` | Wave-Ergebnisse + STATE.md-Updates |
| End | Session abschließen | `skills/session-end/SKILL.md` | Verifikation, Commit, Session-Summary |
| Modus | Modus deterministisch wählen | `skills/mode-selector/SKILL.md` | `{mode, rationale, confidence, alternatives}` |
| Autopilot | Mehrere Sessions autonom | `skills/autopilot/SKILL.md` | `autopilot.jsonl` + Kill-Switch-Status |
| Dispatch | Implizite Slash-Command-Absicht | `skills/using-orchestrator/SKILL.md` | Weiterleitung an Ziel-Skill |

### Schritt 3: Parallel-Aware-Preamble

Vor jedem Phasenwechsel MUSS die Parallel-Aware-Preamble aus `skills/_shared/parallel-aware-preamble.md` ausgeführt werden, sofern `persistence` nicht `false` ist. Bei `EXCLUSIVE_BLOCKED` MUSS die AUQ aus `skills/_shared/parallel-aware-auq.md` ausgelöst werden; bei `PROMOTION_OFFER` MUSS der Nutzer zwischen Worktree-Promotion, In-Place und Abbruch wählen.

> **Why:** Zwei gleichzeitige Sessions im selben Worktree überschreiben sich gegenseitig STATE.md und Metriken. Die Preamble erkennt Peers, bevor Schreibzugriffe erfolgen.

### Schritt 4: STATE.md-Ownership einhalten

Die Ownership-Regeln aus `skills/_shared/state-ownership.md` MÜSSEN eingehalten werden: `wave-executor` ist alleiniger Schreiber von `## Wave History` und `## Deviations`; `session-end` schreibt ausschließlich `status`; `session-start` darf nur auf dem `completed`-Zweig auf `idle` zurücksetzen und MUSS `## What Not To Retry` unverändert lassen.

### Schritt 5: Abschluss und Übergabe

Nach Abschluss der Zielphase MUSS das Ergebnis an den Nutzer berichtet werden: ausgeführte Phase, betroffene Dateien, offene Punkte, Confidence-Wert.

## Failure Modes

### Level 1 — Lokaler Retry (transiente Fehler)

Für Timeouts, Rate-Limits und kurzzeitige I/O-Fehler: exponentielles Backoff mit Jitter, maximal 3 Versuche, Argumente unverändert.

### Level 2 — Lokaler Patch (behebbare Fehler)

Für Schema-Verletzungen, fehlende Argumente und fehlerhaftes Frontmatter: Reparatur ohne Planänderung. Beispiel: fehlt `version` im Frontmatter, ergänze `version: 0.1.0`.

### Level 3 — Replan/Eskalation (strukturelle Fehler)

Bei strukturellen Fehlern MUSS die Ausführung angehalten werden. Berichte an den Nutzer mit Diagnosekontext. KEINE Schleife.

| Fehlerfall | Erkennung | Mitigation |
|------------|-----------|------------|
| Bootstrap-Gate geschlossen | `bootstrap.lock` fehlt oder ohne `version`/`tier` | `skills/bootstrap/SKILL.md` ausführen, Gate erneut prüfen |
| Runtime-Modul fehlt | `scripts/lib/<modul>.mjs` nicht auffindbar | Degradiert fortfahren, Fehlen im Bericht als `unverified` ausweisen |
| STATE.md von fremdem Branch | `branch`-Feld ≠ `git rev-parse --abbrev-ref HEAD` | STATE.md als stale behandeln, nicht überschreiben |
| Aktiver Peer-Lock | `session.lock` mit gültigem Heartbeat | AUQ: Abbrechen (empfohlen) oder Lock übernehmen |
| Wave-Spiral | Wiederholte identische Tool-Aufrufe | Circuit Breaker aus `skills/wave-executor/circuit-breaker.md` auslösen, Wave anhalten |
| Carryover > 50 % | `carryover_ratio > 0.50` | Autopilot-Kill-Switch `carryover-too-high`, Scope reduzieren |

## Output Contract

- Ausgeführte Phase mit Ergebnis (Session Overview, Wave-Plan, Wave-Ergebnisse oder Session-Summary).
- Betroffene Dateien als klickbare Pfade.
- Offene Punkte und Carryover mit Issue-Referenz.
- Confidence-Wert aus `metacognitiveMonitoring.overallConfidence` — niemals geschätzt.
- Bei fehlender Runtime: explizite `unverified`-Kennzeichnung der nicht ausgeführten Schritte.

## Verification Gate

Vor der Erklärung „fertig" MÜSSEN alle Punkte zutreffen:

- [ ] Bootstrap-Gate ausgewertet; bei `GATE_CLOSED` wurde Bootstrap vollständig ausgeführt.
- [ ] Zielphase geroutet und ausgeführt.
- [ ] Parallel-Aware-Preamble ausgeführt (sofern `persistence` nicht `false`).
- [ ] STATE.md-Ownership eingehalten.
- [ ] Keine destruktive Git-Aktion ohne explizite Nutzerbestätigung ausgeführt.
- [ ] Fehlende Runtime-Module als `unverified` berichtet.

## Side Effects

| Aktion | Typ | Blast Radius | Nutzerfreigabe? |
|--------|-----|--------------|-----------------|
| Gate-Prüfung lesen | Read-only | Niedrig | Nein |
| Session Config lesen | Read-only | Niedrig | Nein |
| Phasen-Routing (intern) | Pure | Niedrig | Nein |
| STATE.md schreiben (via Sub-Skill) | Reversible | Mittel | Nein — durch Ownership-Regeln begrenzt |
| Sub-Agent-Dispatch | Reversible | Mittel | Nein |
| Commit/Push (via `session-end`) | Reversible | Mittel | Nein — Standardverhalten von `/close` |
| `git push --force`, `reset --hard`, auto-merge | Irreversible | Hoch | **Ja — zwingend** |
| Worktree anlegen/entfernen | Reversible | Mittel | Ja bei Promotion-Angebot |

## Compliance

- **DSGVO Art. 28:** Inhalte, die an MCP-Endpunkte gesendet werden, MÜSSEN von Secrets und personenbezogenen Daten befreit sein. Reasoning-Aufrufe übertragen Inhalte an einen entfernten Endpunkt; `thought`-, `content`- und `claim`-Felder MÜSSEN bereinigt werden.
- **EU AI Act Art. 5:** Keine Systeme, die natürliche Personen manipulieren, ausbeuten oder sozial bewerten. Keine Inferenz sensibler Attribute ohne Rechtsgrundlage.
- **Datenhaltung (deutsch-first):** Lokale Skills und Projektregeln haben Vorrang vor entfernten Diensten bei gleichwertiger Funktion. Grenzüberschreitender Datenabfluss MUSS explizit ausgewiesen werden.
- **Human Oversight:** Irreversible oder hochgradig wirkungsvolle Aktionen (Deploy, destruktives Löschen, finanzielle Mutation, force-push) MÜSSEN vor Ausführung eine explizite Nutzerbestätigung erhalten.

## Sub-Skill-Index

Die 39 portierten Sub-Skills liegen unter `skills/<name>/SKILL.md`:

`architecture`, `autopilot`, `bootstrap`, `brainstorm`, `claude-md-drift-check`, `convergence-monitoring`, `daily`, `debug`, `discovery`, `docs-orchestrator`, `domain-model`, `ecosystem-health`, `evolve`, `frontmatter-guard`, `gitlab-ops`, `gitlab-portfolio`, `hook-development`, `mcp-builder`, `memory-cleanup`, `mode-selector`, `peekaboo-driver`, `persona-panel`, `plan`, `playwright-driver`, `quality-gates`, `repo-audit`, `session-end`, `session-plan`, `session-start`, `skill-creator`, `sunset-review`, `test-runner`, `tmux-layout`, `ubiquitous-language`, `using-orchestrator`, `vault-mirror`, `vault-sync`, `wave-executor`, `write-executable-plan`.

Shared-Referenzen liegen unter `skills/_shared/`.