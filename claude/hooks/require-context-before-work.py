#!/usr/bin/env python3
"""
Enforce that Claude reads CONTEXT.md before starting design/calculation work.
Blocks work without proper context awareness.
"""
import json
import sys
import os
import re

def read_file_if_exists(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

def get_context_md(cwd):
    context_path = os.path.join(cwd, "CONTEXT.md")
    return read_file_if_exists(context_path)

def prompt_indicates_design_work(prompt):
    """Check if prompt is asking for design/calc work"""
    design_patterns = [
        r'\b(design|iterate|optimize|calculate|model|simulate)\b',
        r'\b(create|implement|build|develop|write)\s+(calculation|design|model)',
        r'\b(review|analyze|check)\s+(design|implementation|calculation)',
        r'\bcombustor\b',
        r'\bturbine\b',
        r'\bcompressor\b',
    ]

    for pattern in design_patterns:
        if re.search(pattern, prompt, re.IGNORECASE):
            return True
    return False

def context_md_has_recent_read(context_md):
    """Check if CONTEXT.md shows recent awareness"""
    # If empty or template-like, not recently read
    if len(context_md.strip()) < 100:
        return False

    # If has "TODO" or similar placeholders, likely not engaged with
    placeholder_count = context_md.count("TODO") + context_md.count("TBD") + context_md.count("[TODO]")
    if placeholder_count > 5:
        return False

    return True

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

prompt = input_data.get('prompt', '')
cwd = input_data.get('cwd', '')

# Check if this is design/calculation work
if not prompt_indicates_design_work(prompt):
    sys.exit(0)

# Check if CONTEXT.md exists and has meaningful content
context_md = get_context_md(cwd)
if not context_md_has_recent_read(context_md):
    output = {
        "decision": "block",
        "reason": """❌ BLOCKED: Before ANY design/calculation work, you MUST:

1. Read CONTEXT.md completely
2. State what you learned: current project status, blocking issues, what was previously tried
3. Explain how your approach addresses known issues
4. Confirm you understand the constraints

This prevents repeating past mistakes (like the TVC design that ignored JATO geometry constraints).

If CONTEXT.md doesn't exist or is empty, ask the user for current project status first."""
    }
    print(json.dumps(output))
    sys.exit(0)

# Allow the prompt
sys.exit(0)
