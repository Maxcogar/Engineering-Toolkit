#!/usr/bin/env python3
"""
Project Dashboard Generator - Aerospace Engineering Aesthetic

Generates an HTML dashboard showing project status, parameters, and navigation.
Run: python scripts/generate_dashboard.py
Output: dashboard.html (open in browser)
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import re

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def read_context_md():
    """Extract key info from CONTEXT.md"""
    context_path = Path("CONTEXT.md")
    if not context_path.exists():
        return {}

    content = context_path.read_text(encoding='utf-8')

    # Extract current phase
    phase_match = re.search(r'\*\*Current Phase:\*\* (.+)', content)
    phase = phase_match.group(1) if phase_match else "Unknown"

    # Extract blocking issues
    blocking_section = re.search(r'\*\*Blocking Issues:\*\*\n\n(.+?)(?=\n\n\*\*)', content, re.DOTALL)
    blocking = blocking_section.group(1).strip() if blocking_section else "None"

    # Extract next actions
    next_actions = []
    next_section = re.search(r'\*\*Next Actions:\*\*\n\n(.+?)(?=\n\n##)', content, re.DOTALL)
    if next_section:
        actions_text = next_section.group(1)
        next_actions = [line.strip('- [ ] ') for line in actions_text.split('\n') if line.strip().startswith('- [ ]')]

    return {
        'phase': phase,
        'blocking': blocking,
        'next_actions': next_actions
    }


def read_critical_parameters():
    """Extract critical parameters from CONTEXT.md"""
    context_path = Path("CONTEXT.md")
    if not context_path.exists():
        return []

    content = context_path.read_text(encoding='utf-8')

    # Find parameters table
    params_section = re.search(r'## Critical Parameters\n\n(.+?)(?=\n\n##)', content, re.DOTALL)
    if not params_section:
        return []

    table_text = params_section.group(1)
    lines = table_text.strip().split('\n')[2:]  # Skip header and separator

    parameters = []
    for line in lines:
        if '|' in line:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 3:
                parameters.append({
                    'name': parts[0],
                    'value': parts[1],
                    'source': parts[2]
                })

    return parameters


def read_system_status():
    """Extract system status from CONTEXT.md"""
    context_path = Path("CONTEXT.md")
    if not context_path.exists():
        return []

    content = context_path.read_text(encoding='utf-8')

    # Find system status table
    status_section = re.search(r'## System Status\n\n(.+?)(?=\n\n##)', content, re.DOTALL)
    if not status_section:
        return []

    table_text = status_section.group(1)
    lines = table_text.strip().split('\n')[2:]  # Skip header and separator

    systems = []
    for line in lines:
        if '|' in line:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 3:
                systems.append({
                    'name': parts[0],
                    'status': parts[1],
                    'documentation': parts[2]
                })

    return systems


def read_recent_decisions():
    """Read recent decision files"""
    decisions_dir = Path("docs/decisions")
    if not decisions_dir.exists():
        return []

    decision_files = sorted(decisions_dir.glob("DEC-*.md"), reverse=True)[:5]

    decisions = []
    for df in decision_files:
        content = df.read_text(encoding='utf-8')
        title_match = re.search(r'^# (.+)', content, re.MULTILINE)
        title = title_match.group(1) if title_match else df.stem

        decisions.append({
            'number': df.stem,
            'title': title,
            'file': str(df)
        })

    return decisions


def generate_html(context_info, parameters, systems, decisions):
    """Generate the HTML dashboard with aerospace engineering aesthetic"""

    # Calculate completion metrics
    total_systems = len(systems)
    completed = sum(1 for s in systems if 'concept' in s['status'].lower() or 'complete' in s['status'].lower())
    in_progress = sum(1 for s in systems if 'requirements' in s['status'].lower() or 'research' in s['status'].lower())
    completion_pct = int((completed / total_systems * 100)) if total_systems > 0 else 0

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JET TURBINE // PROJECT TELEMETRY</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary: #00ff9d;
            --secondary: #00d4ff;
            --accent: #ff006e;
            --warning: #ffb800;
            --bg-dark: #0a0e1a;
            --bg-panel: #0f1420;
            --bg-elevated: #151b2b;
            --grid-color: rgba(0, 255, 157, 0.1);
            --text: #e8f4f8;
            --text-dim: #7a8a99;
            --border: rgba(0, 255, 157, 0.3);
        }}

        @keyframes scanline {{
            0% {{ transform: translateY(-100%); }}
            100% {{ transform: translateY(100vh); }}
        }}

        @keyframes flicker {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.97; }}
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}

        @keyframes slideInRight {{
            from {{
                transform: translateX(50px);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        body {{
            font-family: 'JetBrains Mono', monospace;
            background: var(--bg-dark);
            color: var(--text);
            overflow-x: hidden;
            position: relative;
            line-height: 1.6;
        }}

        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
                repeating-linear-gradient(0deg, transparent, transparent 2px, var(--grid-color) 2px, var(--grid-color) 3px),
                repeating-linear-gradient(90deg, transparent, transparent 2px, var(--grid-color) 2px, var(--grid-color) 3px);
            background-size: 50px 50px;
            pointer-events: none;
            z-index: 1;
            opacity: 0.3;
        }}

        body::after {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--primary), transparent);
            animation: scanline 8s linear infinite;
            pointer-events: none;
            z-index: 9999;
            opacity: 0.5;
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 2;
            animation: fadeIn 0.5s ease-out;
        }}

        header {{
            margin-bottom: 3rem;
            border-left: 4px solid var(--primary);
            padding-left: 2rem;
            position: relative;
            animation: slideInRight 0.6s ease-out;
        }}

        header::before {{
            content: '// SYSTEM STATUS';
            position: absolute;
            top: -1.5rem;
            left: 2rem;
            font-size: 0.75rem;
            color: var(--text-dim);
            letter-spacing: 2px;
        }}

        h1 {{
            font-family: 'Orbitron', sans-serif;
            font-size: 3rem;
            font-weight: 900;
            color: var(--primary);
            letter-spacing: -1px;
            text-transform: uppercase;
            line-height: 1;
            margin-bottom: 0.5rem;
            text-shadow: 0 0 20px rgba(0, 255, 157, 0.5);
        }}

        .subtitle {{
            font-size: 0.9rem;
            color: var(--text-dim);
            letter-spacing: 1px;
            text-transform: uppercase;
        }}

        .status-bar {{
            background: linear-gradient(135deg, var(--bg-elevated), var(--bg-panel));
            border: 1px solid var(--border);
            padding: 1.5rem 2rem;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            overflow: hidden;
            animation: slideInRight 0.7s ease-out 0.1s backwards;
        }}

        .status-bar::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 157, 0.1), transparent);
            animation: shimmer 3s infinite;
        }}

        @keyframes shimmer {{
            0% {{ left: -100%; }}
            100% {{ left: 100%; }}
        }}

        .phase {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.1rem;
            color: var(--primary);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .completion {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .completion-bar {{
            width: 200px;
            height: 8px;
            background: var(--bg-dark);
            border: 1px solid var(--border);
            position: relative;
            overflow: hidden;
        }}

        .completion-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            width: {completion_pct}%;
            transition: width 1s ease-out;
            box-shadow: 0 0 10px var(--primary);
        }}

        .completion-text {{
            font-size: 0.9rem;
            color: var(--text-dim);
            font-family: 'Orbitron', sans-serif;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .panel {{
            background: var(--bg-panel);
            border: 1px solid var(--border);
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            animation: slideInRight 0.8s ease-out backwards;
        }}

        .panel:nth-child(1) {{ animation-delay: 0.1s; }}
        .panel:nth-child(2) {{ animation-delay: 0.2s; }}
        .panel:nth-child(3) {{ animation-delay: 0.3s; }}
        .panel:nth-child(4) {{ animation-delay: 0.4s; }}

        .panel::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, var(--primary), transparent);
        }}

        .panel:hover {{
            border-color: var(--primary);
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.2);
            transform: translateY(-2px);
        }}

        .panel h2 {{
            font-family: 'Orbitron', sans-serif;
            font-size: 0.9rem;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 1.5rem;
            font-weight: 700;
        }}

        .metric {{
            display: flex;
            justify-content: space-between;
            padding: 0.75rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 0.85rem;
        }}

        .metric:last-child {{
            border-bottom: none;
        }}

        .metric-label {{
            color: var(--text-dim);
        }}

        .metric-value {{
            font-family: 'Orbitron', sans-serif;
            color: var(--secondary);
            font-weight: 700;
            font-size: 1.1rem;
        }}

        .alert {{
            background: linear-gradient(135deg, rgba(255, 0, 110, 0.1), rgba(255, 0, 110, 0.05));
            border: 1px solid var(--accent);
            border-left: 4px solid var(--accent);
            padding: 1rem 1.5rem;
            margin-bottom: 2rem;
            animation: pulse 2s ease-in-out infinite;
        }}

        .alert strong {{
            color: var(--accent);
            font-family: 'Orbitron', sans-serif;
        }}

        .success {{
            background: linear-gradient(135deg, rgba(0, 255, 157, 0.1), rgba(0, 255, 157, 0.05));
            border: 1px solid var(--primary);
            border-left: 4px solid var(--primary);
            padding: 1rem 1.5rem;
            margin-bottom: 2rem;
        }}

        .success strong {{
            color: var(--primary);
            font-family: 'Orbitron', sans-serif;
        }}

        .actions-list {{
            list-style: none;
        }}

        .actions-list li {{
            padding: 0.75rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            position: relative;
            padding-left: 1.5rem;
            font-size: 0.85rem;
        }}

        .actions-list li::before {{
            content: '▸';
            position: absolute;
            left: 0;
            color: var(--primary);
            font-weight: bold;
        }}

        .actions-list li:last-child {{
            border-bottom: none;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }}

        thead {{
            background: var(--bg-elevated);
        }}

        th {{
            text-align: left;
            padding: 1rem;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.75rem;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 2px solid var(--border);
            font-weight: 700;
        }}

        td {{
            padding: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}

        tbody tr {{
            transition: background 0.2s ease;
        }}

        tbody tr:hover {{
            background: rgba(0, 255, 157, 0.05);
        }}

        .status-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            font-size: 0.7rem;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            border: 1px solid;
        }}

        .status-complete {{
            color: var(--primary);
            border-color: var(--primary);
            background: rgba(0, 255, 157, 0.1);
        }}
        .status-progress {{
            color: var(--secondary);
            border-color: var(--secondary);
            background: rgba(0, 212, 255, 0.1);
        }}
        .status-pending {{
            color: var(--warning);
            border-color: var(--warning);
            background: rgba(255, 184, 0, 0.1);
        }}
        .status-blocked {{
            color: var(--accent);
            border-color: var(--accent);
            background: rgba(255, 0, 110, 0.1);
        }}

        .quick-links {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }}

        .quick-link {{
            display: block;
            background: var(--bg-elevated);
            padding: 1rem;
            text-align: center;
            text-decoration: none;
            color: var(--text);
            border: 1px solid var(--border);
            transition: all 0.3s ease;
            font-size: 0.85rem;
            position: relative;
            overflow: hidden;
        }}

        .quick-link::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 157, 0.2), transparent);
            transition: left 0.4s ease;
        }}

        .quick-link:hover::before {{
            left: 100%;
        }}

        .quick-link:hover {{
            border-color: var(--primary);
            color: var(--primary);
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.3);
        }}

        .wide {{
            grid-column: 1 / -1;
        }}

        .timestamp {{
            text-align: right;
            color: var(--text-dim);
            font-size: 0.75rem;
            margin-top: 3rem;
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 1px;
        }}

        .glow {{
            animation: flicker 3s ease-in-out infinite;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1 class="glow">JET TURBINE</h1>
            <p class="subtitle">GT3582R Turbocharger Platform // Experimental Gas Turbine Engine</p>
        </header>

        <div class="status-bar">
            <div class="phase">Phase: {context_info.get('phase', 'Unknown')}</div>
            <div class="completion">
                <div class="completion-bar">
                    <div class="completion-fill"></div>
                </div>
                <span class="completion-text">{completion_pct}% COMPLETE</span>
            </div>
        </div>

        {'<div class="alert"><strong>⚠ BLOCKING:</strong> ' + context_info.get('blocking', 'None') + '</div>' if context_info.get('blocking') != 'None' else '<div class="success"><strong>✓ STATUS:</strong> All systems operational - no blocking issues</div>'}

        <div class="grid">
            <div class="panel">
                <h2>// Telemetry</h2>
                <div class="metric">
                    <span class="metric-label">Total Systems</span>
                    <span class="metric-value">{len(systems)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Completed</span>
                    <span class="metric-value">{completed}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">In Progress</span>
                    <span class="metric-value">{in_progress}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Parameters Locked</span>
                    <span class="metric-value">{len(parameters)}</span>
                </div>
            </div>

            <div class="panel">
                <h2>// Priority Queue</h2>
                <ul class="actions-list">
                    {' '.join(f'<li>{action}</li>' for action in context_info.get('next_actions', [])[:4]) or '<li>No actions queued</li>'}
                </ul>
            </div>

            <div class="panel">
                <h2>// Navigation</h2>
                <div class="quick-links">
                    <a href="CONTEXT.md" class="quick-link">CONTEXT.md</a>
                    <a href="WORKFLOW.md" class="quick-link">WORKFLOW</a>
                    <a href="README-RAG.md" class="quick-link">RAG SYSTEM</a>
                    <a href=".claude/README.md" class="quick-link">HOOKS</a>
                    <a href="docs/systems/" class="quick-link">SYSTEMS</a>
                    <a href="calculations/" class="quick-link">CALCS</a>
                </div>
            </div>
        </div>

        <div class="panel wide">
            <h2>// System Matrix</h2>
            <table>
                <thead>
                    <tr>
                        <th>System</th>
                        <th>Status</th>
                        <th>Documentation</th>
                    </tr>
                </thead>
                <tbody>
                    {' '.join(f'''<tr>
                        <td><strong>{s['name']}</strong></td>
                        <td>{get_status_badge(s['status'])}</td>
                        <td>{s['documentation']}</td>
                    </tr>''' for s in systems)}
                </tbody>
            </table>
        </div>

        <div class="panel wide">
            <h2>// Critical Parameters</h2>
            <table>
                <thead>
                    <tr>
                        <th>Parameter</th>
                        <th>Value</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>
                    {' '.join(f'''<tr>
                        <td><strong>{p['name']}</strong></td>
                        <td style="color: var(--secondary); font-weight: 700;">{p['value']}</td>
                        <td style="color: var(--text-dim);">{p['source']}</td>
                    </tr>''' for p in parameters)}
                </tbody>
            </table>
        </div>

        <div class="timestamp">
            TELEMETRY TIMESTAMP // {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        </div>
    </div>
</body>
</html>"""

    return html


def get_status_badge(status):
    """Generate HTML for status badge"""
    status_lower = status.lower()

    if 'concept' in status_lower or 'complete' in status_lower:
        css_class = 'status-complete'
    elif 'requirements' in status_lower or 'research' in status_lower or 'defined' in status_lower:
        css_class = 'status-progress'
    elif 'basic' in status_lower or 'placeholder' in status_lower:
        css_class = 'status-pending'
    else:
        css_class = 'status-blocked'

    return f'<span class="status-badge {css_class}">{status}</span>'


def main():
    """Generate dashboard"""
    print("Generating project dashboard...")

    # Read all data
    context_info = read_context_md()
    parameters = read_critical_parameters()
    systems = read_system_status()
    decisions = read_recent_decisions()

    # Generate HTML
    html = generate_html(context_info, parameters, systems, decisions)

    # Write to file
    output_path = Path("dashboard.html")
    output_path.write_text(html, encoding='utf-8')

    print(f"Dashboard generated: {output_path.absolute()}")
    print(f"   Systems: {len(systems)}")
    print(f"   Parameters: {len(parameters)}")
    print(f"   Completion: {int((sum(1 for s in systems if 'concept' in s['status'].lower() or 'complete' in s['status'].lower()) / len(systems) * 100)) if systems else 0}%")


if __name__ == "__main__":
    main()
