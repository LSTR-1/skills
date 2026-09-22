# Compliance Reference (DSGVO / EU AI Act / Deutsche Datenhaltung)

> Single source of truth for compliance constraints across all ported orchestrator skills.
> Referenced by skills that transmit content to MCP endpoints or handle personal data.

## DSGVO Art. 28 — Auftragsverarbeitung

Inhalte, die an MCP-Endpunkte gesendet werden, MÜSSEN von Secrets und personenbezogenen Daten
befreit sein, sofern keine Auftragsverarbeitungsvereinbarung (AVV) für diesen Endpunkt vorliegt.
Reasoning-Aufrufe übertragen Inhalte an einen entfernten Endpunkt; `thought`-, `content`- und
`claim`-Felder MÜSSEN bereinigt werden.

**Regel:** Vor jedem MCP-Aufruf MÜSSEN Credentials, Tokens, Klarnamen, E-Mail-Adressen und
Kundendaten aus den Argumenten entfernt oder pseudonymisiert werden.

## EU AI Act Art. 5 — Verbotene Praktiken

Keine Systeme, die natürliche Personen manipulieren, ausbeuten oder sozial bewerten. Keine
Inferenz sensibler Attribute (Herkunft, Gesundheit, politische Meinung) ohne Rechtsgrundlage.

**Regel:** Persona-Panels, Discovery-Probes und Review-Agenten MÜSSEN auf technische Artefakte
beschränkt bleiben. Keine Bewertung natürlicher Personen.

## Deutsche Datenhaltung (Daten-Souveränität)

Lokale Skills und Projektregeln haben Vorrang vor entfernten Diensten bei gleichwertiger Funktion.
Grenzüberschreitender Datenabfluss MÜSSEN explizit ausgewiesen werden.

**Regel:** Standard ist lokale Verarbeitung. Jeder entfernte Aufruf MUSS im Session Overview
als grenzüberschreitender Datenabfluss gekennzeichnet werden.

## Human Oversight — irreversible Aktionen

Irreversible oder hochgradig wirkungsvolle Aktionen MÜSSEN vor Ausführung eine explizite
Nutzerbestätigung erhalten:

| Aktion | Blast Radius | Freigabe |
|--------|--------------|----------|
| `git push --force` / `--force-with-lease` | Hoch | **Zwingend** |
| `git reset --hard` | Hoch | **Zwingend** |
| `git checkout -- .` / `git restore .` | Hoch | **Zwingend** |
| Auto-Merge von MRs/PRs | Hoch | **Zwingend** |
| `rm -rf` außerhalb des Repos | Hoch | **Zwingend** |
| Deploy / Release | Hoch | **Zwingend** |
| Finanzielle Mutation | Hoch | **Zwingend** |
| Commit / Push (Standard-`/close`) | Mittel | Nein — Standardverhalten |

**Regel:** Diese Aktionen MÜSSEN als `blockedCommands` in `wave-scope.json` geführt werden.
Der PreToolUse-Guard blockiert sie deterministisch; eine Freigabe erfolgt ausschließlich über
eine explizite Nutzerbestätigung im Dialog.

## Secrets-Hygiene

Secrets MÜSSEN NICHT in Hooks, Memory-Dateien, Evolution-Ledger oder Reasoning-Records
erscheinen. Verwendung von Umgebungsvariablen oder einem Secrets-Store ist zwingend.