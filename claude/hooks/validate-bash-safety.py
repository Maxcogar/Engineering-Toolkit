#!/usr/bin/env python3
"""
Validate bash commands for safety and engineering best practices.
"""
import json
import sys
import re

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = input_data.get('tool_name', '')
tool_input = input_data.get('tool_input', {})
command = tool_input.get('command', '')

if tool_name != 'Bash':
    sys.exit(0)

# Dangerous patterns
dangerous_patterns = [
    (r'\brm\s+-rf\s+/', 'Destructive rm -rf on root paths'),
    (r'\brm\s+-rf\s+\*', 'Dangerous rm -rf with wildcards'),
    (r'\brm\s+-rf\s+\$', 'Dangerous rm -rf with variables'),
]

blocking_patterns = [
    (r'>\s*/dev/null\s+2>&1.*git\s+commit', 'Silencing git commit output - breaks pre-commit hooks'),
]

# Check blocking patterns first
for pattern, message in blocking_patterns:
    if re.search(pattern, command):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"❌ BLOCKED: {message}"
            }
        }
        print(json.dumps(output))
        sys.exit(0)

# Check warning patterns
warnings = []
for pattern, message in dangerous_patterns:
    if re.search(pattern, command):
        warnings.append(f"⚠️  Warning: {message}")

if warnings:
    errors_text = "\n".join(warnings)
    print(errors_text, file=sys.stderr)
    sys.exit(1)  # Non-blocking warning

sys.exit(0)
