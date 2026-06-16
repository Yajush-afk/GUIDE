# GUIDE MVP Context

This document captures the agreed project direction for the team.

## Product Direction

GUIDE is a Windows-only desktop overlay application for teaching beginner laptop users how to perform basic computer tasks. The product should feel like navigation for using a laptop: the user sees instructions, target highlights, and progress feedback while completing the task manually.

The V1 project should prioritize a reliable guided loop over AI sophistication. AI and screen understanding matter, but the system must work consistently during demos and user testing.

The core V1 experience is:

1. User selects a predefined tutorial.
2. The JavaFX desktop overlay displays the current instruction.
3. The overlay highlights the target area or UI element.
4. The user performs the action manually.
5. The Python backend analyzes the screen and system state.
6. Validators decide whether the step is complete.
7. The app automatically advances to the next step.
8. If validation fails, the user can receive hints or manually mark the step complete.

## V1 Scope

The primary V1 demo tutorial is Chrome Search Basics.

Target demo flow:

1. User starts the Chrome tutorial.
2. GUIDE asks the user to open Chrome.
3. GUIDE highlights the Start/taskbar area approximately.
4. GUIDE detects that Chrome opened.
5. GUIDE asks the user to click the address bar.
6. GUIDE highlights the address/search bar.
7. User searches a predefined query.
8. GUIDE detects that the search/page loaded.
9. Tutorial completes automatically.

The V1 should be one polished tutorial rather than several incomplete tutorials.

## Product Priorities

Priority order:

1. The system understands the current screen state.
2. The system highlights where the user should interact.
3. The system advances automatically when the action is completed.
4. Voice guidance comes after text-guided tutorials are stable.

## Target Users

Primary users:

- first-time laptop users
- non-technical adults
- school students

Secondary users:

- internal demo audience
- evaluators
- portfolio reviewers

Assume users may get lost, click incorrect places, misunderstand instructions, or complete a step in an unexpected way. V1 can teach one recommended path, but should include recovery controls.

## Architecture

GUIDE uses a local desktop-plus-backend architecture.

### Desktop Application Layer

Technology:

- Java 21
- JavaFX
- Maven

Responsibilities:

- Windows desktop app shell
- floating instruction bubble
- click-through overlay
- highlight rendering
- course/tutorial selection
- local settings
- backend startup
- localhost API communication

Java owns all overlay rendering. It should not own computer vision or tutorial validation.

### Local Python Backend

Technology:

- Python 3.12
- FastAPI
- Pydantic
- SQLite when persistence is needed

Responsibilities:

- tutorial state machine
- lesson loading
- validation orchestration
- screen capture coordination
- OCR/CV processing
- Windows state detection
- hint/help orchestration
- local API and WebSocket server

The Java app should launch the Python backend automatically. The backend should bind only to `127.0.0.1`.

### Screen Understanding Layer

Technology under consideration:

- MSS for screen capture
- OpenCV for image processing
- Tesseract/pytesseract for OCR
- PyAutoGUI where useful
- Windows UI Automation libraries where useful

V1 should use a hybrid validation strategy.

Preferred signal order depends on the step:

1. deterministic OS/application state
2. Windows UI Automation
3. OCR/CV
4. AI-assisted reasoning or hints

AI should assist validation and explanation, not replace the source of truth in V1.

### AI Help Layer

V1 can include basic AI-assisted help if time allows. It must not be required for the core tutorial to work.

Rules:

- no required paid APIs
- no required hosted infrastructure
- BYO API keys are allowed later
- local-only mode must remain functional
- screenshots must not leave the machine by default
- Ollama/local models are future scope

## Validation Philosophy

Validation must be explainable. Developers should be able to see why a step passed or failed.

Good validation reason:

```text
Chrome window not detected.
```

Bad validation reason:

```text
AI thinks the user is not finished.
```

Validation should be moderately forgiving. The system should auto-advance when success is detected, but there must also be an `I completed this step` fallback button.

V1 should not block incorrect user clicks. GUIDE should guide, not control.

## Screenshot Ownership

Python should own screen capture because the CV/OCR stack is Python-native. Java should render overlays and receive structured screen-state results from Python.

Important issue:

The overlay may appear in screenshots. V1 should handle this by either hiding the overlay briefly during capture or telling the backend which overlay regions to ignore.

## API Direction

Use REST for setup/control and WebSocket for live state updates.

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

Example step event:

```json
{
  "type": "step_changed",
  "step_id": "open_chrome",
  "instruction": "Open Google Chrome.",
  "overlay": {
    "bubble": true,
    "highlight": {
      "type": "approximate_region",
      "region": "taskbar_or_start"
    }
  }
}
```

Example validation event:

```json
{
  "type": "validation_update",
  "step_id": "open_chrome",
  "status": "waiting",
  "reason": "Chrome window not detected",
  "signals": {
    "active_window": "File Explorer",
    "ocr_text_found": ["Documents", "Downloads"]
  }
}
```

## Lesson Schema Direction

Lessons should be manually authored as YAML files and validated by schema/Pydantic.

Lessons should declare intent, not executable code.

Example:

```yaml
id: chrome_search_basics
title: Chrome Search Basics
platform: windows
version: 1

steps:
  - id: open_chrome
    instruction: Open Google Chrome.
    target:
      type: approximate_region
      region: taskbar_or_start
    validation:
      strategy: active_window
      app: chrome
    hints:
      - Click the Chrome icon if it is on the taskbar.
      - You can also open Start and search for Chrome.

  - id: click_search_bar
    instruction: Click the address bar at the top of Chrome.
    target:
      type: ui_automation_or_fallback_region
      role: address_bar
    validation:
      strategy: focus_or_screen_state
      expected_app: chrome

  - id: search_query
    instruction: Type "Wikipedia" and press Enter.
    validation:
      strategy: browser_search_detected
      expected_text_any:
        - Wikipedia
        - Search
        - Google
```

## Four Week Execution Plan

### Week 1: Foundation

- JavaFX app shell
- floating overlay bubble
- click-through overlay proof
- FastAPI backend shell
- Java launches backend
- health check
- one hardcoded tutorial
- WebSocket or polling state updates

### Week 2: Screen Understanding

- Python screen capture
- active window/process detection
- Chrome detection
- OCR proof
- structured screen-state output
- privacy indicator design

### Week 3: Guided Chrome Tutorial

- lesson schema
- tutorial state machine
- validation loop
- auto advance
- highlight target regions
- manual fallback button
- developer-readable validation reasons

### Week 4: Polish And Demo Reliability

- retry and hint behavior
- debug/logging view
- controlled demo script
- packaging and developer scripts
- repeated testing on the demo machine

## Team Responsibilities

### Yajush

- backend architecture
- tutorial state machine
- lesson schema
- validation orchestration
- AI/help abstraction

### Adarsh

- screen capture privacy
- local API security
- Windows process/window detection
- sensitive-screen rules
- validation helpers

### Karan

- backend service lifecycle
- logging
- SQLite/progress if needed
- packaging and developer scripts
- reliability testing

### Aryaveer

- JavaFX overlay
- click-through window behavior
- highlight rendering
- tutorial selection UI
- backend communication

## Avoid In MVP

- autonomous clicking or typing
- generic open-ended computer assistant
- required paid API usage
- hosted backend
- cloud screenshot analysis
- complex custom object detection models
- multi-monitor support
- all-browser support
- real shutdown flow
- AI-generated lessons
- saving screenshots

## Privacy Rules

- Screen analysis should have a visible indicator.
- Screenshots should not be saved by default.
- Screenshots should not leave the machine by default.
- BYO API features must be explicitly enabled later.
- Avoid passwords, banking, personal documents, and sensitive workflows.

## Definition Of Done For V1

A user can:

1. Start a tutorial.
2. Receive visual guidance.
3. See highlighted targets.
4. Complete steps manually.
5. Trigger automatic validation.
6. Progress through the tutorial without manual intervention.

Reliable demo behavior is more important than broad feature coverage.
