# Design Iterations

Versioned snapshots of design states.

## When to Create an Iteration

- Before major design changes
- At design review milestones
- When calculations drive redesign
- Before testing a design

## Folder Structure

```
iterations/
├── v1.0/
│   ├── README.md      # What changed, why
│   ├── exports/       # STEP, STL files
│   └── screenshots/   # Visual reference
├── v1.1/
└── v2.0/
```

## Version Numbering

- Major (vX.0): Significant redesign
- Minor (v1.X): Incremental improvements

## Each Iteration Should Include

1. README.md explaining changes
2. Exported geometry (STEP preferred)
3. Screenshot or render
4. Link to driving calculation/decision
