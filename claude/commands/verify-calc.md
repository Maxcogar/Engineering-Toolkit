---
description: Verify calculation against reference material and engineering principles
argument-hint: [calculation-notebook-path]
---

# Calculation Verification Workflow

Verifying calculation: **$ARGUMENTS**

## Verification Process

### Step 1: Read the Calculation
1. Open and read: $ARGUMENTS
2. Understand what is being calculated and why
3. Note all assumptions and inputs
4. Identify the calculation method

### Step 2: Check Documentation
- [ ] Purpose clearly stated
- [ ] All inputs documented with units
- [ ] Assumptions explicitly listed
- [ ] Reference equations cited with sources
- [ ] Output units verified
- [ ] imports from project_params.py (not hard-coded values)

### Step 3: Verify Against References
Search docs/reference/ and use WebSearch to find:
1. Published equations for this type of calculation
2. Benchmark problems with known solutions
3. Worked examples in textbooks or papers

Compare:
- Are the equations correct?
- Are units consistent?
- Are assumptions reasonable?

### Step 4: Dimensional Analysis
Check all equations:
- Left side and right side have same units
- No adding apples to oranges
- Dimensionless numbers calculated correctly

### Step 5: Sanity Checks
- Do the output values make physical sense?
- Are they in the expected range?
- Do they match order-of-magnitude estimates?

### Step 6: Create Verification Report
If this calculation will be used for hardware:

Create: `verification/reviews/[calc-name]-verification.md`

Template:
```markdown
# Verification Report: [Calculation Name]

**Date**: [Today]
**Calculation**: $ARGUMENTS
**Verified by**: Claude Code + User Review

## Scope
What was verified and method used.

## Original Work Summary
Brief summary of what the calculation does.

## Verification Method
How verification was performed (literature comparison, alternative method, etc.)

## Verification Calculations
[Show verification work - different method, reference comparison, etc.]

## Dimensional Analysis
[Check units throughout]

## Sanity Checks
[Order of magnitude estimates, physical reasonableness]

## Literature Cross-Reference
[Citations to published work, comparison of methods and results]

## Issues Found
[Any problems or discrepancies]

## Recommendations
[Changes needed or approval to use]

## Conclusion
[Pass/Fail, conditions for use]
```

### Step 7: Update Calculation Status
If verified:
- Change status in notebook from "Draft" to "Verified"
- Add link to verification report
- Note any corrections made

If failed:
- Document issues
- Create DEC-XXX explaining what needs to be fixed
