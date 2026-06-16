# GUIDE Project Phases

Use this file as the team checklist for tracking project progress. Mark items complete by changing `[ ]` to `[x]`.

## Phase 0: Repository And Planning

- [x] Create initial repository structure.
- [x] Add product-only `README.md`.
- [x] Add MVP/team context in `USER.md`.
- [x] Add agent context in `AGENTS.md`.
- [x] Add Claude Code context in `CLAUDE.md`.
- [x] Add `.gitignore`.
- [x] Add Python environment files.
- [x] Add JavaFX Maven setup.
- [x] Add initial API and lesson schema placeholders.

## Phase 1: Desktop And Backend Foundation

- [ ] Create minimal JavaFX app entry point.
- [ ] Create basic JavaFX window.
- [ ] Create floating instruction bubble UI.
- [ ] Prove transparent overlay rendering.
- [ ] Prove click-through overlay behavior on Windows.
- [ ] Create FastAPI backend entry point.
- [ ] Add `/health` endpoint.
- [ ] Add backend startup script.
- [ ] Make Java app launch the local Python backend.
- [ ] Confirm backend binds only to `127.0.0.1`.
- [ ] Add basic frontend-backend health check from Java.

## Phase 2: Tutorial Session System

- [ ] Define tutorial session model.
- [ ] Define step state model.
- [ ] Add tutorial listing endpoint.
- [ ] Add session creation endpoint.
- [ ] Add session start endpoint.
- [ ] Add pause/resume support.
- [ ] Add manual `I completed this step` fallback.
- [ ] Add hint endpoint.
- [ ] Add WebSocket or polling-based live updates.
- [ ] Add developer-readable validation reason format.

## Phase 3: Lesson System

- [ ] Finalize first version of lesson YAML format.
- [ ] Validate lessons against schema.
- [ ] Add `chrome_search_basics.yaml`.
- [ ] Add lesson loader in backend.
- [ ] Map lesson validation strategies to backend validators.
- [ ] Keep lesson files declarative with no executable logic.

## Phase 4: Screen Understanding

- [ ] Add Python screen capture using MSS.
- [ ] Ensure screenshots are not saved by default.
- [ ] Add visible screen-analysis indicator in desktop app.
- [ ] Handle overlay appearing in screenshots.
- [ ] Add active window detection.
- [ ] Add process detection.
- [ ] Add Chrome detection.
- [ ] Add OCR proof using Tesseract/pytesseract.
- [ ] Return structured screen-state data from backend.
- [ ] Add debug logging for detected signals.

## Phase 5: Chrome Search Tutorial MVP

- [ ] Step 1: guide user to open Chrome.
- [ ] Validate Chrome process/window is active.
- [ ] Auto-advance after Chrome is detected.
- [ ] Step 2: guide user to address/search bar.
- [ ] Highlight address/search bar using best available signal.
- [ ] Add fallback approximate highlight region.
- [ ] Step 3: guide user to type a predefined search query.
- [ ] Validate search/page state using window title, OCR, or browser state.
- [ ] Auto-complete tutorial.
- [ ] Confirm manual fallback works for each step.

## Phase 6: Reliability And Recovery

- [ ] Add retry behavior when validation fails.
- [ ] Add basic hints per step.
- [ ] Add stuck-state detection based on timeout.
- [ ] Add clear error messages for failed validators.
- [ ] Add debug panel or log output for developers.
- [ ] Test on controlled Windows demo machine.
- [ ] Record known environment assumptions.
- [ ] Cut or simplify unstable steps.

## Phase 7: Privacy And Safety

- [ ] Document screen capture behavior.
- [ ] Confirm screenshots are not persisted.
- [ ] Confirm screenshots never leave device in local mode.
- [ ] Add local-only mode notes.
- [ ] Add warning/rules for sensitive workflows.
- [ ] Avoid password, banking, and private document tutorials.
- [ ] Add local API security notes.
- [ ] Add per-session token plan before sensitive controls are exposed.

## Phase 8: Voice Guidance

- [ ] Add offline TTS proof.
- [ ] Add step instruction playback.
- [ ] Add user setting to enable/disable voice.
- [ ] Avoid blocking tutorial flow if voice fails.
- [ ] Add voice text field support in lessons.

## Phase 9: Packaging And Demo Prep

- [ ] Add Windows developer run scripts.
- [ ] Add backend packaging plan.
- [ ] Add Java desktop packaging plan.
- [ ] Decide how Python runtime is bundled.
- [ ] Decide how Tesseract is bundled or installed.
- [ ] Create controlled demo script.
- [ ] Run repeated end-to-end demo tests.
- [ ] Prepare V1 release checklist.

## Future Phases

- [ ] File Explorer basics tutorial.
- [ ] Windows Start Menu tutorial.
- [ ] More Chrome workflows.
- [ ] Multiple valid workflow support.
- [ ] Better Windows UI Automation integration.
- [ ] Local model/Ollama exploration.
- [ ] BYO API key AI help.
- [ ] AI-assisted lesson authoring.
- [ ] Open-ended help assistant.
- [ ] Multi-monitor support.

