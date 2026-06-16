# GUIDE Agent Context

This repository contains GUIDE, a Windows-only desktop overlay application that teaches beginner laptop users how to complete basic computer tasks.

Agents working in this repository should preserve the current product direction: GUIDE is a guided learning overlay, not an autonomous computer-control agent.

## Product Rules

- The user performs actions manually.
- The app guides, observes, validates, and explains.
- Do not add autonomous clicking, typing, or task execution unless explicitly requested.
- Prioritize reliable guidance and validation over impressive but fragile AI behavior.
- Keep local-only operation functional.
- Do not require paid APIs, hosted infrastructure, or cloud services for core features.
- Screenshots must not be saved or sent off-device by default.
- Windows is the only target platform for the MVP.

## Architecture

The project uses a monorepo structure:

```text
apps/desktop-javafx/        Java 21 + JavaFX desktop overlay
services/guide-backend/     Python 3.12 + FastAPI local backend
lessons/                    Manually authored tutorial lesson files
schemas/                    Shared API and lesson schemas
docs/                       Architecture, setup, privacy, and planning docs
scripts/                    Developer scripts
packaging/windows/          Windows packaging assets
```

## Layer Ownership

JavaFX desktop app owns:

- Windows desktop UI
- floating instruction bubble
- click-through overlay
- highlight rendering
- course/tutorial selection
- local settings
- launching the backend
- localhost API/WebSocket client behavior

Python backend owns:

- FastAPI localhost server
- tutorial state machine
- lesson loading
- validation orchestration
- screen capture
- OCR/CV processing
- Windows process/window detection
- AI/help abstraction

## Validation Strategy

Use a hybrid validation strategy. Pick the most reliable signal for each step.

Preferred signals:

1. deterministic OS/application state
2. Windows UI Automation
3. OCR/CV
4. AI-assisted reasoning or help

AI should assist explanation and recovery. It should not be the only source of truth for V1 step completion.

Validation must be explainable. Return developer-readable reasons such as:

```text
Chrome window not detected.
```

Avoid vague reasons such as:

```text
AI says user is not done.
```

## MVP Tutorial Direction

The primary V1 demo is Chrome Search Basics:

1. Open Chrome.
2. Detect Chrome is active.
3. Guide the user to the address/search bar.
4. User searches a predefined query.
5. Detect the search/page result.
6. Complete the tutorial automatically.

Keep the V1 narrow and polished. One reliable tutorial is better than several unfinished tutorials.

## API Direction

Use REST for control and WebSocket for live session updates.

Candidate REST endpoints:

```text
GET  /health
GET  /tutorials
POST /sessions
POST /sessions/{id}/start
POST /sessions/{id}/pause
POST /sessions/{id}/complete-step-manually
POST /sessions/{id}/hint
POST /sessions/{id}/stop
```

Candidate WebSocket endpoint:

```text
/ws/sessions/{id}
```

## Lesson Direction

Lessons should be declarative YAML files. They should describe instructions, targets, hints, and validation strategies. They should not contain executable logic.

Validator implementations belong in the Python backend.

## Coding Guidance

- Keep changes scoped to the requested task.
- Prefer existing project structure before adding new patterns.
- Do not add cloud dependencies to core flows.
- Do not commit secrets or API keys.
- Keep generated/cache files out of the repository.
- Use clear names for tutorial steps, validators, and API events.
- Keep beginner-user safety and privacy in mind when adding features.

## Privacy And Safety

- Bind local backend APIs to `127.0.0.1`.
- Add authentication/session tokens before exposing sensitive backend controls.
- Keep screen capture local by default.
- Do not persist screenshots unless a future feature explicitly requires it and the user has opted in.
- Avoid tutorials involving passwords, banking, personal documents, or sensitive accounts.
