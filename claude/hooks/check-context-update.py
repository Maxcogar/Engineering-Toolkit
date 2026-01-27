#!/usr/bin/env python3
"""
Remind to update CONTEXT.md before ending session.
"""
import json
import sys
import os
from datetime import datetime, timedelta

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

cwd = input_data.get('cwd', '')
context_path = os.path.join(cwd, 'CONTEXT.md')

try:
    if os.path.exists(context_path):
        # Check if file was modified recently (within last hour)
        mod_time = datetime.fromtimestamp(os.path.getmtime(context_path))
        age = datetime.now() - mod_time

        if age > timedelta(hours=1):
            # CONTEXT.md not updated recently
            output = {
                "continue": False,
                "stopReason": """❌ REMINDER: Update CONTEXT.md before ending session!

Document in CONTEXT.md:
1. What was worked on this session
2. What was accomplished
3. Any decisions made (create DEC-NNN.md for significant ones)
4. What to pick up next session
5. Any blocking issues

This ensures continuity between sessions and prevents information loss."""
            }
            print(json.dumps(output))
            sys.exit(0)
except:
    pass

sys.exit(0)
