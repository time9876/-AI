# Starx MVS-1 Engineering Rules

- Implement only the task explicitly requested; do not implement future system behavior early.
- Do not add external dependencies except `pytest`.
- Do not call external APIs.
- Do not build UI.
- Do not add agents.
- Do not make architectural changes beyond the current task scope.
- Keep code deterministic and easy to test.
