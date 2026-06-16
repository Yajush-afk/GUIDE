# API Contract

The desktop app communicates with the local backend over `127.0.0.1`.

## REST

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

## WebSocket

```text
/ws/sessions/{id}
```

## Event: Step Changed

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

## Event: Validation Update

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
