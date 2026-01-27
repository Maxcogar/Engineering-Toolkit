---
description: Create engineering decision record for significant choices
argument-hint: [decision-title]
---

# Create Engineering Decision Record

Creating decision record: **$ARGUMENTS**

## Process

### Step 1: Determine Decision Number
Check docs/decisions/ to find the next DEC number.

### Step 2: Create Decision File
File: `docs/decisions/DEC-XXX-$ARGUMENTS.md`

Use this template:

```markdown
# DEC-XXX: $ARGUMENTS

**Date**: [Today's date]
**Status**: PROPOSED
**Author**: Claude Code + User

## Context

[What situation led to this decision? What problem are we solving?]

## Decision

[What did we decide to do?]

## Rationale

[WHY is this the right choice? What analysis supports it?]

## Alternatives Considered

1. **Option 1**: [What else could we do?]
   - Pros: ...
   - Cons: ...
   - Why rejected: ...

2. **Option 2**: ...

## Consequences

### Positive
- [What good comes from this?]

### Negative
- [What trade-offs or downsides?]

### Neutral
- [What changes but isn't clearly good or bad?]

## Implementation

[What needs to be done to implement this?]

## Verification

[How will we verify this was the right decision?]

## Related Decisions

- Links to other DEC-XXX records
- Links to calculations that support this
- Links to test results if relevant

## References

- [Reference documents that informed this decision]
```

### Step 3: Link Decision
- Update CONTEXT.md noting this decision was made
- Reference from relevant system docs
- Link from calculations if decision was based on analysis

### Step 4: Commit
Create git commit for the decision record.
