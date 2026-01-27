# Design Directory

CAD files, drawings, and design documentation.

## Structure

```
design/
├── iterations/     # Versioned design snapshots
├── drawings/       # 2D drawings and prints
├── cad/           # Source CAD files
└── exports/       # STL, STEP, DXF exports
```

## Design Iterations

Save snapshots in `iterations/vX.X/` when:
- Major design change is made
- Before significant modifications
- At review milestones

## File Naming

- CAD: `part-name_vX.X.ext`
- Drawings: `part-name_drawing.pdf`
- Exports: `part-name.step`, `part-name.stl`

## Version Control

- Large binary files: Consider Git LFS
- Always commit with descriptive message
- Reference related calculations/decisions
