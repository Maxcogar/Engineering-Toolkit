#!/usr/bin/env python3
"""
Initialize a new engineering project with the AI toolkit.

Usage:
    python init-project.py <project-name> [options]

Examples:
    python init-project.py pump-design
    python init-project.py turbine --full
    python init-project.py motor-controller --venv --rag
"""

import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

TOOLKIT_ROOT = Path(__file__).parent.resolve()


def validate_project_name(name: str) -> bool:
    """Validate project name - no spaces, no special chars."""
    pattern = r'^[a-zA-Z][a-zA-Z0-9_-]*$'
    return bool(re.match(pattern, name))


def process_template(content: str, replacements: dict) -> str:
    """Replace template placeholders with values."""
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


def init_project(
    name: str,
    target_path: Path = None,
    description: str = "",
    project_type: str = "general",
    create_venv: bool = False,
    init_rag: bool = False,
    create_dashboard: bool = False,
    git_remote: str = None,
    no_git: bool = False,
    dry_run: bool = False
):
    """Initialize a new project with toolkit files."""

    # Validate project name
    if not validate_project_name(name):
        print(f"ERROR: Invalid project name '{name}'")
        print("Project name must start with a letter and contain only letters, numbers, hyphens, and underscores.")
        sys.exit(1)

    # Determine target path
    if target_path is None:
        target_path = TOOLKIT_ROOT.parent / "projects" / name
    target_path = Path(target_path).resolve()

    # Check target doesn't exist
    if target_path.exists():
        print(f"ERROR: Target path already exists: {target_path}")
        sys.exit(1)

    # Template replacements
    today = datetime.now()
    replacements = {
        "PROJECT_NAME": name,
        "PROJECT_DESCRIPTION": description or f"{name} engineering project",
        "DATE": today.strftime("%Y-%m-%d"),
        "YEAR": str(today.year),
    }

    if dry_run:
        print(f"DRY RUN - Would create project at: {target_path}")
        print(f"  Name: {name}")
        print(f"  Description: {replacements['PROJECT_DESCRIPTION']}")
        print(f"  Type: {project_type}")
        print(f"  Options: venv={create_venv}, rag={init_rag}, dashboard={create_dashboard}")
        print(f"  Git: {'no' if no_git else 'yes'}" + (f", remote={git_remote}" if git_remote else ""))
        return

    print(f"Creating project '{name}' at: {target_path}")
    print()

    # Step 1: Create target directory
    target_path.mkdir(parents=True, exist_ok=True)

    # Step 2: Copy scaffold structure and process templates
    scaffold = TOOLKIT_ROOT / "project-scaffold"
    if not scaffold.exists():
        print(f"ERROR: Scaffold not found at {scaffold}")
        sys.exit(1)

    print("[1/7] Copying project scaffold...")
    for item in scaffold.rglob("*"):
        if item.is_file():
            rel_path = item.relative_to(scaffold)
            dest = target_path / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)

            # Handle .template files
            if item.suffix == ".template":
                dest = dest.with_suffix("")  # Remove .template extension
                content = item.read_text(encoding='utf-8')
                content = process_template(content, replacements)
                dest.write_text(content, encoding='utf-8')
            else:
                shutil.copy2(item, dest)

    # Step 3: Copy .claude directory
    print("[2/7] Copying Claude configuration...")
    claude_src = TOOLKIT_ROOT / "claude"
    claude_dest = target_path / ".claude"
    if claude_src.exists():
        shutil.copytree(claude_src, claude_dest)

        # Rename settings.json.template to settings.json
        settings_template = claude_dest / "settings.json.template"
        settings_dest = claude_dest / "settings.json"
        if settings_template.exists():
            settings_template.rename(settings_dest)

    # Step 4: Copy scripts
    print("[3/7] Copying scripts...")
    scripts_src = TOOLKIT_ROOT / "scripts"
    scripts_dest = target_path / "scripts"
    if scripts_src.exists():
        shutil.copytree(scripts_src, scripts_dest)

    # Step 5: Copy templates
    print("[4/7] Copying templates...")
    templates_src = TOOLKIT_ROOT / "templates"
    templates_dest = target_path / "templates"
    if templates_src.exists():
        shutil.copytree(templates_src, templates_dest)

    # Step 6: Copy requirements
    req_src = TOOLKIT_ROOT / "requirements-engineering.txt"
    if req_src.exists():
        shutil.copy2(req_src, target_path / "requirements-engineering.txt")

    # Step 7: Write toolkit version marker
    version_file = TOOLKIT_ROOT / "VERSION"
    version = version_file.read_text().strip() if version_file.exists() else "1.0.0"
    (target_path / ".toolkit-version").write_text(f"{version}\n")

    # Optional: Create virtual environment
    if create_venv:
        print("[5/7] Creating virtual environment...")
        venv_path = target_path / ".venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)

        # Install requirements
        if sys.platform == "win32":
            pip_path = venv_path / "Scripts" / "pip.exe"
        else:
            pip_path = venv_path / "bin" / "pip"

        req_eng = target_path / "requirements-engineering.txt"
        req_rag = target_path / "scripts" / "requirements-rag.txt"

        if req_eng.exists():
            subprocess.run([str(pip_path), "install", "-r", str(req_eng)], check=True)
        if req_rag.exists():
            subprocess.run([str(pip_path), "install", "-r", str(req_rag)], check=True)
    else:
        print("[5/7] Skipping virtual environment (use --venv to enable)")

    # Optional: Initialize RAG
    if init_rag:
        print("[6/7] Initializing RAG index...")
        setup_rag = target_path / "scripts" / "setup_rag.py"
        if setup_rag.exists():
            # Just create the chroma_db directory - actual setup needs PDFs
            (target_path / "chroma_db").mkdir(exist_ok=True)
            print("      Empty RAG index created. Add PDFs to docs/reference/ then run:")
            print("      python scripts/setup_rag.py --setup")
    else:
        print("[6/7] Skipping RAG initialization (use --rag to enable)")

    # Optional: Generate dashboard
    if create_dashboard:
        print("[7/7] Generating dashboard...")
        dashboard_script = target_path / "scripts" / "generate_dashboard.py"
        if dashboard_script.exists():
            try:
                subprocess.run([sys.executable, str(dashboard_script)], cwd=str(target_path), check=True)
            except subprocess.CalledProcessError:
                print("      Dashboard generation failed (may need dependencies)")
    else:
        print("[7/7] Skipping dashboard (use --dashboard to enable)")

    # Git initialization
    if not no_git:
        print()
        print("Initializing git repository...")
        subprocess.run(["git", "init"], cwd=str(target_path), check=True, capture_output=True)
        subprocess.run(["git", "add", "-A"], cwd=str(target_path), check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"[INIT] {name} project from toolkit v{version}"],
            cwd=str(target_path),
            check=True,
            capture_output=True
        )

        if git_remote:
            subprocess.run(["git", "remote", "add", "origin", git_remote], cwd=str(target_path), check=True)
            print(f"      Remote added: {git_remote}")

    # Print success message
    print()
    print("=" * 80)
    print(f" PROJECT INITIALIZED: {name}")
    print(f" Location: {target_path}")
    print(f" Toolkit Version: {version}")
    print("=" * 80)
    print()
    print(" GETTING STARTED CHECKLIST")
    print(" -------------------------")
    print(f" [ ] 1. Open project in VS Code:")
    print(f'        code "{target_path}"')
    print()
    print(" [ ] 2. Read workflow documentation:")
    print("        - WORKFLOW.md (daily workflow)")
    print("        - .claude/README.md (hook system)")
    print()
    print(" [ ] 3. Customize project_params.py with your parameters")
    print()
    print(" [ ] 4. Add PDFs to docs/reference/, then:")
    print("        python scripts/setup_rag.py --setup")
    print()
    print(" [ ] 5. Update CONTEXT.md with project state")
    print()
    print(" [ ] 6. Run /prime in Claude Code to orient yourself")
    print()
    print(" KEY COMMANDS")
    print(" ------------")
    print(" /prime              - Read essential project context")
    print(" /understand [sys]   - Research before designing")
    print(" /research [topic]   - Web search and document")
    print(" /decision [title]   - Create decision record")
    print()
    print(" DASHBOARD")
    print(" ---------")
    print(" python scripts/generate_dashboard.py")
    print(" Open dashboard.html in browser")
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Initialize engineering project with AI toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python init-project.py pump-design
  python init-project.py turbine --full
  python init-project.py motor --description "BLDC motor controller" --venv
        """
    )

    parser.add_argument("name", help="Project name (letters, numbers, hyphens, underscores)")
    parser.add_argument("--path", help="Custom target directory (default: ../projects/<name>)")
    parser.add_argument("--description", "-d", help="Project description")
    parser.add_argument("--type", "-t", choices=["general", "mechanical", "electrical", "thermal"],
                        default="general", help="Project type (default: general)")
    parser.add_argument("--venv", action="store_true", help="Create Python virtual environment")
    parser.add_argument("--rag", action="store_true", help="Initialize empty RAG index")
    parser.add_argument("--dashboard", action="store_true", help="Generate initial dashboard")
    parser.add_argument("--full", action="store_true", help="Enable --venv --rag --dashboard")
    parser.add_argument("--git-remote", help="Add git remote origin URL")
    parser.add_argument("--no-git", action="store_true", help="Skip git initialization")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created")

    args = parser.parse_args()

    # Handle --full flag
    if args.full:
        args.venv = True
        args.rag = True
        args.dashboard = True

    target = Path(args.path) if args.path else None

    init_project(
        name=args.name,
        target_path=target,
        description=args.description or "",
        project_type=args.type,
        create_venv=args.venv,
        init_rag=args.rag,
        create_dashboard=args.dashboard,
        git_remote=args.git_remote,
        no_git=args.no_git,
        dry_run=args.dry_run
    )
