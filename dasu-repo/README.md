# Dasu.print — Sheet Layout Tool

**出す** *(dasu)* — Japanese: *to output / to print*

A free, open-source browser-based sheet layout tool built for the [Bonsai BIM](https://bonsaibim.org) / [IfcOpenShell](https://ifcopenshell.org) ecosystem.

> Developed independently for the benefit of the OSArch and Bonsai communities.  
> Not affiliated with, endorsed by, or a product of either community.

---

## What is it?

Dasu is a single HTML file that runs entirely in your browser — no install, no server, no subscription. Open it in Chrome or Edge and it works.

The goal is to bridge the gap between IFC-based BIM authoring in Blender/Bonsai BIM and the production of print-ready drawing sheets. Drawings produced by Bonsai's `bim.create_drawing` operator are composed on sheets, annotated, and exported as PDF or SVG — entirely within the browser.

![Dasu screenshot placeholder](docs/screenshot.png)

---

## Features

- **Sheet canvas** — A4–A1, portrait/landscape, configurable grid, zoom/pan
- **Snap engine** — grid, sheet edges, element edges/centres, equal spacing, smart guides, ortho lock
- **Element panel** — position, size, scale, angle, order, align, mirror, crop, lock
- **Import** — SVG, PNG, JPG via drag-drop or file open; Bonsai BIM bridge (live)
- **Annotation tools** — line, polyline, rectangle, ellipse, text with full formatting
- **Fill & stroke** — solid colour, hatch patterns, gradients
- **Text** — font, size (mm), bold/italic/underline, alignment, background box, revision cloud border
- **File format** — `.bprint` JSON, Portable or Referenced mode, auto-save to IndexedDB
- **Templates** — built-in paper sizes, user-saved templates, recent files
- **Export** — PDF, SVG, browser Print
- **Bonsai BIM bridge** — local HTTP server, send drawings directly from Blender N-panel

---

## Quick Start

1. Download `dasu.html`
2. Open it in Chrome or Edge
3. Choose a template from the Start dialog
4. Drag SVG, PNG or JPG files onto the sheet — or use the Bonsai BIM bridge

---

## Bonsai BIM Bridge

The bridge lets Bonsai BIM send drawings directly to Dasu without any manual file steps.

### Requirements
- Python 3.6+ (stdlib only — no pip installs needed for the bridge)
- Blender 4.x / 5.x with Bonsai BIM installed

### Setup

```bash
# 1. Start the bridge server
python bridge/dasu_bridge.py

# 2. In Blender Text Editor, open and run:
blender/dasu_panel.py

# 3. In Blender: N-panel → Dasu tab → set drawings folder → Send to Dasu ↗
```

The bridge listens on `localhost:7821`. Open `http://localhost:7821` in your browser for a status page.

---

## DXF Import (coming soon)

DXF files from any source (Bonsai BIM, AutoCAD, FreeCAD) will be converted to SVG via `ezdxf` through the bridge server, with a layer manager for lineweight, colour, and linetype mapping.

---

## Tech Stack

| Library | Licence | Purpose |
|---------|---------|---------|
| [Fabric.js 5.3.1](https://fabricjs.com) | MIT | Canvas manipulation |
| [jsPDF 2.5.1](https://parall.ax/products/jspdf) | MIT | PDF generation |
| [ezdxf](https://ezdxf.readthedocs.io) *(bridge)* | MIT | DXF→SVG conversion |
| [IfcOpenShell](https://ifcopenshell.org) *(bridge)* | LGPL | IFC metadata |

Zero proprietary dependencies. Runs fully local. No cloud. No licence fees.

---

## File Format — `.bprint`

Dasu saves projects as `.bprint` files — plain JSON with two modes:

- **Portable** — all assets embedded as base64 (self-contained, larger file)
- **Referenced** — asset paths only (smaller file, assets must stay in place)

Auto-save runs every 3 seconds to IndexedDB in referenced mode.

---

## Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| 1 | ✅ Done | Canvas, snap, element panel, text, file system, templates |
| 2 | 🔵 Active | Bonsai BIM bridge, DXF import, layer manager |
| 3 | 🟡 Planned | Dimension tool, leader arrows, annotation tool refinement |
| 4 | 🟡 Planned | Editable title block fields, rulers |
| 5 | ⚪ Future | Undo/redo, TAKT planning integration |

---

## Contributing

Dasu is developed independently as a contribution to the OSArch and Bonsai communities. Issues, pull requests, and feedback are welcome.

- [OSArch Community](https://community.osarch.org)
- [Bonsai BIM](https://bonsaibim.org)
- [IfcOpenShell GitHub](https://github.com/IfcOpenShell/IfcOpenShell)

---

## Licence

MIT — see [LICENSE](LICENSE)

---

*Dasu.print v0.1.0-alpha — Built for the OSArch / Bonsai BIM community*
