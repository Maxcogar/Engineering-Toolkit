---
description: Research topic using web search and document findings
argument-hint: [topic]
---

# Web Research Workflow

You are researching: **$ARGUMENTS**

## MANDATORY PROCESS

### Step 1: Check RAG First

Query existing knowledge base to see what's already known:

```bash
python scripts/rag_query.py "$ARGUMENTS" "all available information"
```

Document what RAG already has so you don't duplicate effort.

### Step 2: Web Search for Gaps

Perform comprehensive web searches to fill knowledge gaps:

**Search Strategy:**
1. Academic/technical papers
2. Industry standards and specifications
3. Manufacturer documentation
4. Build guides and practical implementations
5. Recent developments (last 2-3 years)

**Required Searches:**
- Technical overview and fundamentals
- Design methods and best practices
- Real-world implementations and case studies
- Common problems and solutions
- Recent advances or improvements

Use WebSearch tool for each aspect. Gather URLs and key findings.

### Step 3: Document Findings

Create: `docs/reference/$ARGUMENTS-research.md`

**Required sections:**

```markdown
# [Topic] Research

**Research Date:** [Current date]
**Researcher:** Claude Code

## Research Question

What specific question or gap was this research addressing?

## RAG Knowledge Base Results

What did the existing knowledge base already contain?
- Summary of RAG findings
- Which PDFs had relevant info
- What gaps were identified

## Web Search Results

### Search 1: [Description]
**Query:** [Exact search query used]
**Key Findings:**
- Finding 1
- Finding 2
**Sources:**
- [Title 1](URL)
- [Title 2](URL)

### Search 2: [Description]
[Repeat format]

## Key Insights

What are the most important findings from this research?
1. Insight 1
2. Insight 2
3. Insight 3

## Implications for Project

How does this research affect the gas turbine project?
- Design implications
- Constraint changes
- New possibilities
- Things to avoid

## Open Questions

What still needs more research?

## References

Complete list of all sources with URLs.
```

### Step 4: Update RAG (Optional)

If the research findings are substantial and will be referenced frequently:

```bash
python scripts/setup_rag.py --setup
```

This rebuilds the knowledge base to include the new research document.

### Step 5: Update Related Understanding Docs

If this research affects an existing system understanding document:
1. Update `docs/systems/[system]/current-understanding.md`
2. Add research citations to relevant sections
3. Update constraints or design approach if changed

## When to Use This Command

Use `/research [topic]` when:
- RAG doesn't have enough information on a topic
- Need current/recent information (last few years)
- Researching new approaches or technologies
- Need manufacturer specs or standards
- Building understanding before design work

## Example Usage

```
User: "/research transpiration cooling for turbine blades"

1. Query RAG for existing blade cooling info
2. WebSearch: "transpiration cooling turbine blades design"
3. WebSearch: "porous material transpiration cooling gas turbine"
4. WebSearch: "transpiration cooling implementation challenges"
5. WebSearch: "ceramic matrix composite transpiration cooling"
6. Document all findings in docs/reference/transpiration-cooling-research.md
7. Optionally rebuild RAG
8. Update docs/systems/turbine-section/current-understanding.md
```

## DO NOT

- Don't just do one quick search and call it done
- Don't skip documenting sources with URLs
- Don't forget to check RAG first to avoid duplicating existing knowledge
- Don't research without a clear question or gap to address

## Integration with Design Workflow

Research → Understanding → Design

1. `/research [topic]` - Gather web information, document findings
2. `/understand [system]` - Query RAG (now includes research) + read PDFs
3. Design work - Based on complete knowledge (RAG + research + PDFs)

Research FEEDS the understanding process by expanding the knowledge base.
