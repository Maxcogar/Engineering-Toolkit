# Claude Code Workflow Enforcement System

This directory contains the workflow enforcement system that prevents engineering mistakes.

## What This System Does

**Prevents the TVC failure mode**: The system blocks design/calculation work until proper understanding is documented. It enforces systematic engineering thinking instead of guessing.

## System Components

### 1. Hooks (`hooks/`)

Hooks intercept Claude's actions and enforce workflow rules:

- **require-context-before-work.py** - Blocks design/calc prompts until CONTEXT.md is read
- **enforce-documentation-before-design.py** - Requires understanding docs before modifying design/calc files
- **validate-bash-safety.py** - Prevents dangerous bash commands
- **check-context-update.py** - Reminds to update CONTEXT.md before exiting

### 2. Slash Commands (`commands/`)

Reusable workflows invoked with `/command-name`:

- `/prime` - **START HERE** - Prime fresh session with essential context and workflows
- `/research [topic]` - Web search for new information and document findings
- `/understand [system]` - Research and document system understanding (uses RAG + PDFs)
- `/decision [title]` - Create engineering decision record
- `/verify-calc [notebook]` - Verify calculation against references

### 3. Specialized Agents (`agents/`)

AI agents automatically invoked for specific work types:

- **systematic-engineer** - Enforces systematic thinking for all engineering work
- **doc-specialist** - Maintains project documentation and knowledge base

### 4. Settings (`settings.json`)

Configuration for:
- Hook activation (when each hook runs)
- Permissions (what Claude can/cannot do)
- Agent invocation rules

## How It Works

### Session Start
1. User starts Claude Code in this project
2. SessionStart hook reminds: "Read CONTEXT.md first"

### User Asks for Design Work
1. User: "Design the combustor flametube"
2. UserPromptSubmit hook checks if CONTEXT.md was read
3. If not read: BLOCKS with message to read CONTEXT.md first
4. If read: Allows, invokes systematic-engineer agent

### Claude Tries to Modify Design File
1. systematic-engineer agent tries to write to design/combustor/flametube.step
2. PreToolUse hook intercepts Write operation
3. Hook checks: Does docs/systems/combustor/current-understanding.md exist?
4. If no: BLOCKS with message to create understanding doc first
5. If yes: Allows modification

### Session End
1. User tries to exit
2. Stop hook checks if CONTEXT.md was updated recently
3. If not: Reminds to update CONTEXT.md before exiting

## Workflow Enforcement

The system creates multiple enforcement layers:

**Layer 1 - Session Level**: Must read CONTEXT.md before work
**Layer 2 - Prompt Level**: Blocks design prompts without context
**Layer 3 - File Level**: Blocks file modifications without understanding docs
**Layer 4 - Agent Level**: Systematic-engineer enforces thinking process
**Layer 5 - Exit Level**: Ensures CONTEXT.md is updated

## Using the System

### Researching New Information

```bash
# Use slash command to web search for new information
/research transpiration cooling for turbine blades

# This will:
# 1. Check RAG for existing knowledge
# 2. Perform multiple web searches to fill gaps
# 3. Create docs/reference/transpiration-cooling-research.md
# 4. Document findings with URLs and sources
# 5. Optionally rebuild RAG to include new research
```

### Starting Work on a System

```bash
# Use slash command to research system
/understand combustor

# This will:
# 1. Query RAG for existing knowledge (includes web research docs)
# 2. Read JATO guide and other references
# 3. Create docs/systems/combustor/current-understanding.md
# 4. Document constraints, geometry, incompatible approaches
```

### Making a Design Decision

```bash
/decision Reduce combustor length from 150mm to 120mm

# This will:
# 1. Find next DEC number
# 2. Create decision record with template
# 3. Prompt for: context, rationale, alternatives, consequences
```

### Verifying a Calculation

```bash
/verify-calc calculations/combustor/pressure-drop.ipynb

# This will:
# 1. Read the calculation
# 2. Check documentation completeness
# 3. Search for reference material
# 4. Verify against literature
# 5. Create verification report if needed
```

## What Gets Blocked

### Blocked: Design Without Understanding
```
User: "Design a trapped vortex combustor"
Hook: ❌ BLOCKED - Create current-understanding.md first
```

### Blocked: Calculation Without Context
```
User: "Calculate swirl number"
Hook: ❌ BLOCKED - Read CONTEXT.md first
```

### Blocked: File Modification Without Documentation
```
Claude tries: Write to design/combustor/flametube.step
Hook: ❌ BLOCKED - No understanding doc exists for combustor
```

## What's Allowed

### Allowed: Proper Workflow
```
User: "Read CONTEXT.md"
User: "/understand combustor"
Claude: Creates docs/systems/combustor/current-understanding.md
User: "Now design the flametube"
Claude: ✅ Allowed - understanding doc exists, can proceed
```

## File Locations

All workflow files are in `.claude/`:
```
.claude/
├── README.md                           (this file)
├── settings.json                       (hook/agent configuration)
├── hooks/                              (enforcement scripts)
│   ├── require-context-before-work.py
│   ├── enforce-documentation-before-design.py
│   ├── validate-bash-safety.py
│   └── check-context-update.py
├── commands/                           (slash commands)
│   ├── prime.md
│   ├── research.md
│   ├── understand.md
│   ├── decision.md
│   └── verify-calc.md
└── agents/                             (specialized AI agents)
    ├── systematic-engineer.md
    └── doc-specialist.md
```

## Debugging

### Check if hooks are active
```bash
# Hooks run automatically - check settings.json to see configuration
cat .claude/settings.json
```

### Test hook manually
```bash
# Run hook script directly
echo '{"prompt": "design the combustor", "cwd": "."}' | python .claude/hooks/require-context-before-work.py
```

### Disable hooks temporarily
Create `.claude/settings.local.json`:
```json
{
  "hooks": {}
}
```

## Customization

### Add new hook
1. Create Python script in `hooks/`
2. Add to `settings.json` under appropriate event (SessionStart, UserPromptSubmit, PreToolUse, Stop)
3. Test with sample input

### Add new slash command
1. Create markdown file in `commands/`
2. Add frontmatter with description and argument-hint
3. Write workflow steps

### Add new agent
1. Create markdown file in `agents/`
2. Define name, description, tools, model in frontmatter
3. Write agent instructions and workflow

## Git

This directory is committed to git and shared with the team. Everyone using Claude Code on this project gets the same workflow enforcement.

## Version

Created: 2025-12-16
Version: 1.0

## Core Memory System

This project uses Core Memory (persistent memory across all sessions) with a dedicated label for organization.

### Project Label

**Label**: `Jet`
**ID**: `cmjc6dcve04azo51ml887ombg`
**Description**: Claude Code mechanical engineering for gas turbines

### What Gets Stored

All project-related memories should be tagged with the "Jet" label:
- Project overview and specifications
- Key technical decisions and corrections
- Session summaries and lessons learned
- Important research findings
- Critical workflows and patterns

### How to Use

**At session start:**
```
Search core-memory for Jet project context using the label filter
```

**At session end:**
```
Store session summary with labelIds: ["cmjc6dcve04azo51ml887ombg"]
```

**Searching Jet memories:**
```
Use memory-search with labelIds filter to find Jet-specific context
```

This keeps Jet project memories separate from other projects and makes retrieval more efficient.

## Related Documentation

- Project workflow: [WORKFLOW.md](../WORKFLOW.md)
- Project instructions: [CLAUDE.md](../CLAUDE.md)
- Session handoff: [CONTEXT.md](../CONTEXT.md)
- RAG knowledge base: [README-RAG.md](../README-RAG.md)
