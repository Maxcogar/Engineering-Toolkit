# AI Engineering Toolkit

Reusable infrastructure for AI-assisted engineering R&D projects.

## Overview

This toolkit provides:
- **Claude Code hooks** - Enforce documentation-before-design workflow
- **Slash commands** - `/prime`, `/understand`, `/research`, `/decision`, `/verify-calc`
- **Agents** - Specialized agents for documentation, knowledge building, systematic engineering
- **Project scaffold** - Complete folder structure with guidance
- **Scripts** - RAG setup, dashboard generation
- **Templates** - Calculation notebooks, decision records, test reports

## Quick Start

### Create a New Project

```bash
cd toolkit
python init-project.py my-project
```

With all features:
```bash
python init-project.py my-project --full
```

### Options

```
python init-project.py <project-name> [options]

Options:
  --path PATH           Custom location (default: ../projects/<name>)
  --description DESC    Project description
  --type TYPE           Project type: general|mechanical|electrical|thermal
  --venv                Create Python virtual environment
  --rag                 Initialize empty RAG index
  --dashboard           Generate initial dashboard
  --full                Enable --venv --rag --dashboard
  --git-remote URL      Add git remote origin
  --no-git              Skip git initialization
  --dry-run             Show what would be created
```

### Verify Project Setup

```bash
python verify-setup.py ../projects/my-project
```

## Project Structure Created

```
my-project/
├── .claude/            # Claude Code configuration
│   ├── hooks/          # 4 enforcement scripts
│   ├── commands/       # 5 slash commands
│   ├── agents/         # 5 specialized agents
│   └── settings.json   # Hook configuration
├── calculations/       # Jupyter notebooks
├── design/            # CAD files, iterations
├── docs/              # Documentation
│   ├── decisions/     # Decision records
│   ├── reference/     # PDFs, datasheets
│   ├── research/      # Investigation notes
│   └── systems/       # System documentation
├── manufacturing/     # BOM, processes
├── scripts/           # RAG, dashboard
├── templates/         # Document templates
├── testing/           # Test data, results
├── verification/      # Calculation verification
├── CONTEXT.md         # AI session handoff
├── CLAUDE.md          # Claude Code instructions
├── WORKFLOW.md        # Engineering workflow
├── project_params.py  # Parameter file
└── TODO.md            # Task backlog
```

## Toolkit Contents

### Hooks (claude/hooks/)

| Hook | Purpose |
|------|---------|
| `require-context-before-work.py` | Ensures CONTEXT.md is read before work |
| `enforce-documentation-before-design.py` | Requires research before design |
| `validate-bash-safety.py` | Prevents destructive bash commands |
| `check-context-update.py` | Reminds to update CONTEXT.md |

### Commands (claude/commands/)

| Command | Purpose |
|---------|---------|
| `/prime` | Read essential project context |
| `/understand [system]` | Research before designing |
| `/research [topic]` | Web search and document |
| `/decision [title]` | Create decision record |
| `/verify-calc` | Verify calculation against reference |

### Agents (claude/agents/)

| Agent | Purpose |
|-------|---------|
| `systematic-engineer` | Enforces systematic engineering thinking |
| `doc-specialist` | Creates and organizes documentation |
| `knowledge-builder` | Builds knowledge base from references |
| `memory-ingest` | Stores conversation context |
| `memory-search` | Retrieves relevant context |

### Scripts (scripts/)

| Script | Purpose |
|--------|---------|
| `setup_rag.py` | Initialize RAG index from PDFs |
| `rag_query.py` | Query the knowledge base |
| `generate_dashboard.py` | Generate project dashboard |

## Updating Existing Projects

To update an existing project with new toolkit files:

```bash
python update-project.py ../projects/my-project
```

This will update hooks, commands, agents, scripts, and templates while preserving your project's work.

## Requirements

- Python 3.10+
- Git
- VS Code with Claude Code extension

## Version

Current version: 1.0.0

Check project version:
```bash
cat ../projects/my-project/.toolkit-version
```
