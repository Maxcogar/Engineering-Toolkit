---
description: Research and document system understanding before design work
argument-hint: [system-name]
---

# System Understanding Workflow

You are researching and documenting understanding of: **$ARGUMENTS**

## MANDATORY PROCESS - DO NOT SKIP

### Step 1: Query RAG Knowledge Base

**First, use RAG to find relevant information across all reference PDFs:**

```bash
# Query for geometry and structure
python scripts/rag_query.py "$ARGUMENTS" "geometry, physical structure, and layout"

# Query for operating principles
python scripts/rag_query.py "$ARGUMENTS" "operating principles, how it works, and theory"

# Query for design constraints
python scripts/rag_query.py "$ARGUMENTS" "design constraints, limitations, and requirements"

# Query for design approaches
python scripts/rag_query.py "$ARGUMENTS" "design approaches, methods, and best practices"
```

The RAG system will:
- Search across ALL reference PDFs (JATO guide + Small Gas Turbines books)
- Return relevant sections with source citations
- Tell you which PDF and page to read for details

**Save RAG results** - you'll include them in the understanding document.

### Step 2: Read Cited Sources

Based on RAG query results:
1. Note which PDFs have relevant information
2. Read the specific pages cited by RAG
3. Take detailed notes on:
   - Key constraints from each source
   - Geometric details and dimensions
   - Operating principles
   - Design approaches mentioned
4. Cross-reference information across sources

### Step 3: Search Existing Documentation
1. Check docs/systems/$ARGUMENTS/ for existing notes
2. Review any existing calculations in calculations/$ARGUMENTS/
3. Check docs/decisions/ for related decisions

### Step 4: Research if Needed

If RAG + existing docs don't have enough information, use WebSearch to find:
- Academic papers about this technology
- Technical standards
- Build guides from other projects
- Manufacturer specifications

### Step 5: Create Understanding Document

Create: `docs/systems/$ARGUMENTS/current-understanding.md`

Required sections:
- **System Overview**: What this system is and does
- **RAG Query Results**: Summary of what RAG found (with citations)
- **Reference Documents Read**: List every document you actually read (from RAG citations + manual reading)
- **Key Constraints**: Physical, thermal, mechanical constraints from references
- **Geometry/Architecture**: Physical layout and structure
- **Operating Principles**: How it works
- **Incompatibilities Identified**: What approaches WON'T work and why
- **Design Approach**: Based on constraints, what approach makes sense
- **Open Questions**: What needs more research

**CRITICAL**: Include RAG citations in "Reference Documents Read" section:
```markdown
## Reference Documents Read

### From RAG Query Results
1. jato-gas-turbine-build-guide.pdf (pages 20-25) - Combustor geometry and air flow
2. Small Gas Turbines 1 operation.pdf (page 45) - Design principles
3. ...

### Additional Reading
1. ...
```

### Step 6: Verify Understanding

Before ANY design work:
- [ ] Queried RAG for all relevant aspects of this system
- [ ] Read the PDFs and pages cited by RAG
- [ ] Read at least 3 reference documents total
- [ ] Documented all key constraints
- [ ] Identified incompatible approaches (what WON'T work)
- [ ] Created current-understanding.md with all required sections
- [ ] Included RAG citations in understanding document

## DO NOT PROCEED TO DESIGN WITHOUT COMPLETING THIS PROCESS

If you skip this and design something incompatible (like TVC in a JATO can combustor), the hook system will block you.

## Why RAG First?

**The TVC Mistake**: Designed a cavity-in-wall combustor without checking JATO guide. JATO uses radial air injection through walls - cavity physically incompatible.

**With RAG**: Query would have immediately returned "JATO uses can-type with radial air injection" → no cavity design possible.

RAG prevents designing things that are fundamentally incompatible with the actual geometry.
