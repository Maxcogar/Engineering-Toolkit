---
description: Prime a fresh session with essential context and workflows
argument-hint:
---

# Session Priming - READ THIS FIRST

You are starting a fresh session on the **Jet Gas Turbine Project** (GT3582R turbocharger-based experimental engine).

## STEP 1: Read Project Context

**MANDATORY - Read these files in order:**

1. **CONTEXT.md** - Current project state, blocking issues, next actions
2. **CLAUDE.md** - How to work in this repository
3. **.claude/README.md** - Workflow enforcement system (hooks, commands, agents)
4. **README-RAG.md** - Knowledge base system

## STEP 2: Understand Project Organization

```
Jet/
├── CONTEXT.md                  # Session handoff - read first, update last
├── CLAUDE.md                   # Repository instructions
├── dashboard.html              # Auto-generated status (run: python scripts/generate_dashboard.py)
│
├── .claude/                    # Workflow enforcement
│   ├── hooks/                  # Python scripts that block inappropriate work
│   ├── commands/               # Slash commands (/research, /understand, etc.)
│   └── agents/                 # Specialized AI assistants
│
├── docs/
│   ├── decisions/              # Engineering decisions (DEC-NNN.md)
│   ├── reference/              # PDFs, research docs (indexed by RAG)
│   └── systems/                # System documentation
│       └── [system]/
│           └── current-understanding.md  # Required before design work
│
├── calculations/               # Jupyter notebooks for engineering calcs
│   └── [system]/
│
├── scripts/
│   ├── setup_rag.py           # Build knowledge base
│   ├── rag_query.py           # Query knowledge base
│   └── generate_dashboard.py  # Generate status dashboard
│
├── templates/                  # Document templates
└── chroma_db/                  # RAG vector database (auto-generated)
```

## STEP 3: Key Workflows

### Research → Understanding → Design

**Never design without understanding.**

1. **Web Research**: `/research [topic]`
   - WebSearch for new information
   - Document in `docs/reference/[topic]-research.md`
   - Rebuild RAG to include findings

2. **System Understanding**: `/understand [system]`
   - Query RAG for existing knowledge
   - Read cited PDFs
   - Create `docs/systems/[system]/current-understanding.md`
   - Document constraints and incompatible approaches

3. **Design Work**: Only after understanding doc exists
   - Hooks will block design file modifications without understanding doc

### Other Commands

- `/decision [title]` - Create engineering decision record
- `/verify-calc [notebook]` - Verify calculation against references
- `python scripts/generate_dashboard.py` - Update status dashboard

## STEP 4: When You Add/Change Things

### Adding a New System

When you create a new system (combustor, fuel-system, oil-system, etc.):

**Update these files:**

1. **CONTEXT.md** - Add to System Status table:
   ```markdown
   | System Name | Status | Documentation |
   ```

2. **Create folder**: `docs/systems/[system-name]/`

3. **Before design work**: Create `docs/systems/[system-name]/current-understanding.md`

### Adding a Decision

1. **Find next number**: Check `docs/decisions/` for highest DEC-NNN
2. **Create file**: `docs/decisions/DEC-XXX-title.md`
3. **Update CONTEXT.md**: Add to Key Decisions Made table

### Adding a Parameter

**Update CONTEXT.md** - Add to Critical Parameters table:
```markdown
| Parameter | Value | Source |
```

### Adding Reference Material

1. **Add PDF/markdown** to `docs/reference/`
2. **Rebuild RAG**: `python scripts/setup_rag.py --setup`
3. **Query available**: `python scripts/rag_query.py [system] "[topic]"`

### Completing Work

**Update CONTEXT.md** before ending session:
- What was worked on
- What was accomplished
- Decisions made
- Next steps

**Regenerate dashboard**: `python scripts/generate_dashboard.py`

## STEP 5: Critical Rules

### DO NOT

- ❌ Design without understanding docs
- ❌ Skip reading CONTEXT.md
- ❌ Ignore reference materials (use RAG to find them)
- ❌ Create generic solutions without checking existing work
- ❌ Leave CONTEXT.md outdated at session end

### ALWAYS

- ✅ Read CONTEXT.md at session start
- ✅ Use RAG to find existing knowledge before web research
- ✅ Create understanding docs before design
- ✅ Document decisions in docs/decisions/
- ✅ Update CONTEXT.md before session end
- ✅ Cite sources (PDF page numbers, URLs)

## STEP 6: Hook System (Enforcement)

The workflow is **enforced by hooks** that block inappropriate actions:

- **SessionStart**: Reminds to read CONTEXT.md
- **UserPromptSubmit**: Blocks design prompts without context
- **PreToolUse**: Blocks file modifications without understanding docs
- **Stop**: Reminds to update CONTEXT.md

**Hooks are in `.claude/hooks/`** - they prevent the TVC failure mode (designing something incompatible because you didn't read the docs first).

## STEP 7: RAG Knowledge Base

**What is RAG?**
- Vector database of all PDFs and docs in `docs/reference/`
- Semantic search across all sources
- Returns relevant chunks with citations (PDF + page number)

**How to use:**
```bash
# Query for information
python scripts/rag_query.py combustor "geometry and air flow"

# Returns:
# - Relevant text excerpts
# - Source citations (which PDF, which page)
# - Tells you exactly what to read
```

**Information flow:**
```
WebSearch → Research Docs → RAG → Understanding → Design
```

## STEP 8: Current Project Status

**Check CONTEXT.md for:**
- Current phase
- Blocking issues
- Next actions
- System status
- Critical parameters

**Or open dashboard:**
```bash
python scripts/generate_dashboard.py
start dashboard.html  # (or open in browser)
```

## YOU ARE NOW PRIMED

You have the essential knowledge to work effectively in this project:

1. ✅ Know where key files are
2. ✅ Understand the workflow (research → understand → design)
3. ✅ Know what to update when things change
4. ✅ Understand hook enforcement system
5. ✅ Know how to use RAG for knowledge discovery

**Next step:** Read CONTEXT.md to see current project state and blocking issues.

---

**Remember:** This is serious R&D work. The workflow exists because I previously designed a Trapped Vortex Combustor without checking the JATO guide - it was physically incompatible with the actual geometry. The hooks and RAG system prevent this from happening again.
