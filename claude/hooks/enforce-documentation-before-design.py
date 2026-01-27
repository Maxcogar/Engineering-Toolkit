#!/usr/bin/env python3
"""
Prevent modifying design files without understanding documentation.
Ensures proper research before design changes.
"""
import json
import sys
import os
import re
from pathlib import Path

def is_design_file(file_path):
    """Check if file is a design artifact"""
    design_indicators = [
        '/design/',
        '/iterations/',
        '.step',
        '.sldprt',
        '.f3d',
        '.dwg',
        '.dxf',
        'design-',
    ]
    return any(indicator in file_path.lower() for indicator in design_indicators)

def is_calculation_file(file_path):
    """Check if file is a calculation"""
    return '/calculations/' in file_path and file_path.endswith('.ipynb')

def get_system_from_path(file_path):
    """Extract system name from file path"""
    # Try to extract from path like calculations/combustor/...
    match = re.search(r'/(combustor|fuel-system|structural|thermal|performance|testing)/', file_path)
    if match:
        return match.group(1)

    # Try from design/
    match = re.search(r'/design/([^/]+)', file_path)
    if match:
        return match.group(1)

    return None

def check_understanding_exists(cwd, system_name):
    """Check if understanding document exists for this system"""
    if not system_name:
        return True  # Can't determine system, allow

    understanding_path = Path(cwd) / 'docs' / 'systems' / system_name / 'current-understanding.md'

    if not understanding_path.exists():
        return False

    # Check it's not just a template
    content = understanding_path.read_text()
    if content.count("TODO") > 3 or content.count("TBD") > 3:
        return False

    # Check it has required sections
    required_sections = ["## System Overview", "## Reference Documents", "## Key Constraints"]
    for section in required_sections:
        if section not in content:
            return False

    return True

def check_reference_docs_exist(cwd):
    """Check if reference documentation exists"""
    ref_dir = Path(cwd) / 'docs' / 'reference'
    if not ref_dir.exists():
        return False

    # Check for PDF or markdown files
    pdf_files = list(ref_dir.rglob('*.pdf'))
    md_files = list(ref_dir.rglob('*.md'))

    return len(pdf_files) + len(md_files) > 0

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get('tool_name', '')
tool_input = input_data.get('tool_input', {})
file_path = tool_input.get('file_path', '')
cwd = input_data.get('cwd', '')

# Only enforce for Write/Edit operations
if tool_name not in ['Write', 'Edit']:
    sys.exit(0)

# Check if this is a design or calculation file
is_design = is_design_file(file_path)
is_calc = is_calculation_file(file_path)

if not (is_design or is_calc):
    sys.exit(0)

# Extract system name
system_name = get_system_from_path(file_path)

# Check if understanding document exists
if system_name and not check_understanding_exists(cwd, system_name):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"""❌ BLOCKED: Before modifying {system_name} design/calculations, you MUST:

1. Read ALL reference documentation in docs/reference/ about this system
2. Create docs/systems/{system_name}/current-understanding.md documenting:
   - What this system is (geometry, architecture, operating principles)
   - What reference documents you read
   - Key constraints from those documents
   - What approaches are INCOMPATIBLE and why

This prevents mistakes like designing a TVC without understanding JATO uses can-type combustors.

Use template: templates/system-understanding-template.md"""
        }
    }
    print(json.dumps(output))
    sys.exit(0)

# Check if any reference docs exist at all
if not check_reference_docs_exist(cwd):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": """❌ BLOCKED: No reference documentation found in docs/reference/

Before ANY design or calculation work, you need reference material:
- Technical papers
- Build guides (like JATO guide)
- Manufacturer datasheets
- Academic references

Ask the user for reference material or search for it yourself first."""
        }
    }
    print(json.dumps(output))
    sys.exit(0)

# Allow the operation
sys.exit(0)
