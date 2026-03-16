# Changelog

All notable changes to Dasu.print are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.0-alpha] — 2026-03

### Added
- Sheet canvas with A4–A1 paper sizes, portrait/landscape, configurable grid
- Zoom/pan, fit-to-sheet, viewport transform
- Snap engine — grid snap, sheet edges, element edges/centres, equal spacing, smart guide lines
- Ortho lock (Ctrl+drag), angle snap (Shift), arrow key nudge
- Element settings panel — position, size (mm), scale label, angle, order, align to sheet
- Mirror X/Y, crop with drag handles, element lock with padlock icon
- Import — SVG, PNG, JPG via drag-drop or file picker
- Annotation tools — line (with Alt→polyline continuation), rectangle, ellipse, polyline/polygon
- Text tool — IText and Textbox modes, font family/size/weight/style/alignment
- Text background box, border styles (solid, dashed, dotted, dash-dot, revision cloud)
- Revision cloud geometry — configurable arc angle, inward/outward toggle
- Fill — solid colour, hatch patterns (5 styles), linear gradient
- Stroke — colour, width (uniform across scale)
- Title block (NZ standard layout), north point, scale bar
- Multi-page tabs with per-sheet paper settings
- `.bprint` file format — Portable and Referenced save modes
- Save As with OS native folder picker (File System Access API)
- Auto-save to IndexedDB (debounced 3s, referenced mode)
- Recent files list (last 10, stored in IndexedDB)
- Built-in templates — blank A4/A3/A2, A4/A3/A2 with title block
- User-saved templates stored in IndexedDB
- Start dialog — New, Templates, Recent tabs with restore autosave
- Export PDF (jsPDF), Export SVG, browser Print
- Preferences — nudge, grid, snap, PDF resolution, cloud arc angle, bridge port
- About dialog with version info
- Bonsai BIM bridge — local HTTP server (`dasu_bridge.py`, stdlib only)
- Blender N-panel (`dasu_panel.py`) — Send to Dasu button, drawings folder, diagnostics
- Bridge modal in Dasu — connect/disconnect, auto-place toggle, setup instructions
- Status dot on bridge button showing connection state

### Known Issues
- Downloads blocked in sandboxed iframe environments (e.g. claude.ai preview) — works normally when opened locally
- Crop tool may not display immediately on Bonsai BIM SVGs — render timing under investigation
- Arrow leader vertex editing deferred — Fabric.js polyline coordinate system complexity
- Bonsai BIM decoration.py numpy shape mismatch error (non-fatal, Bonsai 5.0 bug)

---

## Upcoming — [0.2.0]

- Fix Sheets / Add Sheet state management bug
- Clipboard paste — Ctrl+V images and plain text
- DXF import via bridge (ezdxf conversion)
- DXF layer manager — lineweight/colour/linetype mapping, named presets
- Bonsai bridge drawings folder persistent via addon prefs
- Crop lag fix — requestAnimationFrame throttle during drag
