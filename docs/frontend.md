# Frontend

The current frontend is implemented in `apps/desktop-javafx` as a Java 21 + JavaFX desktop shell.

## Implemented

- Custom undecorated JavaFX window shell.
- Transparent stage/scene so the app frame owns the visible window shape.
- Rounded app frame without an outer padded rectangle or corner shadow artifact.
- In-app title bar with:
  - GUIDE brand label.
  - Learning overlay subtitle.
  - Dark mode toggle.
  - Minimize control.
  - Maximize/restore control.
  - Close control.
- Draggable title bar.
- Double-click title bar maximize/restore behavior.
- Left tutorial sidebar with collapsible width animation.
- Right settings sidebar with collapsible width animation.
- Sidebar text fades out before collapse and fades back in after expand.
- Center content area for selected tutorial details and start action.
- Material-inspired light theme colors.
- Dark mode styling for shell, title bar, sidebars, content area, text, buttons, and separators.
- Sharper JavaFX text rendering through stylesheet font smoothing.

## Source Files

- `apps/desktop-javafx/src/main/java/com/guide/desktop/GuideApp.java`
- `apps/desktop-javafx/src/main/resources/guide-app.css`

## Current Scope

This frontend is still a local desktop prototype. It focuses on the GUIDE app shell, tutorial selection surface, visual polish, and smooth sidebar interactions. It does not yet implement the full overlay workflow, backend session connection, live validation, or Chrome Search Basics tutorial flow.
