#!/usr/bin/env python3
"""
Update existing project with latest toolkit files.

This updates:
- .claude/ (hooks, commands, agents, skills, SKILL.md, settings)
- scripts/
- templates/

It preserves:
- All project work (calculations, docs, design, etc.)
- project_params.py
- CONTEXT.md, CLAUDE.md, WORKFLOW.md (unless forced)

Usage:
    python update-project.py <project-path>
    python update-project.py ../projects/my-project --force
"""

import argparse
import shutil
import sys
from pathlib import Path

TOOLKIT_ROOT = Path(__file__).parent.resolve()


def update_project(project_path: Path, force: bool = False, dry_run: bool = False):
    """Update existing project with latest toolkit files."""

    project_path = project_path.resolve()

    if not project_path.is_dir():
        print(f"ERROR: Project not found: {project_path}")
        sys.exit(1)

    # Check it's a valid project
    if not (project_path / "CONTEXT.md").is_file():
        print(f"ERROR: Not a valid toolkit project (no CONTEXT.md): {project_path}")
        sys.exit(1)

    # Read current and new versions
    old_version = "unknown"
    version_file = project_path / ".toolkit-version"
    if version_file.is_file():
        old_version = version_file.read_text().strip()

    new_version_file = TOOLKIT_ROOT / "VERSION"
    new_version = new_version_file.read_text().strip() if new_version_file.is_file() else "1.0.0"

    print(f"Updating project: {project_path}")
    print(f"  Current version: {old_version}")
    print(f"  New version: {new_version}")
    print()

    if dry_run:
        print("DRY RUN - Would update:")
        print("  - .claude/ (hooks, commands, agents, skills, SKILL.md, settings)")
        print("  - scripts/")
        print("  - templates/")
        return

    # Update .claude directory
    print("[1/4] Updating Claude configuration...")
    claude_src = TOOLKIT_ROOT / "claude"
    claude_dest = project_path / ".claude"

    if claude_src.is_dir():
        # Remove old hooks, commands, agents, skills (but preserve settings.local.json if exists)
        settings_local = None
        settings_local_path = claude_dest / "settings.local.json"
        if settings_local_path.is_file():
            settings_local = settings_local_path.read_text()

        # Remove and replace subdirectories
        for subdir in ["hooks", "commands", "agents", "skills", "SKILL.md"]:
            dest_subdir = claude_dest / subdir
            if dest_subdir.is_dir():
                shutil.rmtree(dest_subdir)
            src_subdir = claude_src / subdir
            if src_subdir.is_dir():
                shutil.copytree(src_subdir, dest_subdir)

        # Update settings.json
        settings_template = claude_src / "settings.json.template"
        if settings_template.is_file():
            shutil.copy2(settings_template, claude_dest / "settings.json")

        # Update README
        readme_src = claude_src / "README.md"
        if readme_src.is_file():
            shutil.copy2(readme_src, claude_dest / "README.md")

        # Restore settings.local.json (or add default from toolkit)
        if settings_local is not None:
            settings_local_path.write_text(settings_local)
        else:
            settings_local_src = claude_src / "settings.local.json"
            if settings_local_src.is_file() and not settings_local_path.is_file():
                shutil.copy2(settings_local_src, settings_local_path)

    # Update scripts
    print("[2/4] Updating scripts...")
    scripts_src = TOOLKIT_ROOT / "scripts"
    scripts_dest = project_path / "scripts"

    if scripts_src.is_dir():
        # Backup any custom scripts
        custom_scripts = []
        if scripts_dest.is_dir():
            toolkit_scripts = {f.name for f in scripts_src.iterdir() if f.is_file()}
            for script in scripts_dest.iterdir():
                if script.is_file() and script.name not in toolkit_scripts:
                    custom_scripts.append((script.name, script.read_text()))

        # Remove and replace
        if scripts_dest.is_dir():
            shutil.rmtree(scripts_dest)
        shutil.copytree(scripts_src, scripts_dest)

        # Restore custom scripts
        for name, content in custom_scripts:
            (scripts_dest / name).write_text(content)
            print(f"       Preserved custom script: {name}")

    # Update templates
    print("[3/4] Updating templates...")
    templates_src = TOOLKIT_ROOT / "templates"
    templates_dest = project_path / "templates"

    if templates_src.is_dir():
        if templates_dest.is_dir():
            shutil.rmtree(templates_dest)
        shutil.copytree(templates_src, templates_dest)

    # Update version marker
    print("[4/4] Updating version marker...")
    (project_path / ".toolkit-version").write_text(f"{new_version}\n")

    # Update requirements if they exist
    req_src = TOOLKIT_ROOT / "requirements-engineering.txt"
    if req_src.is_file():
        shutil.copy2(req_src, project_path / "requirements-engineering.txt")

    print()
    print("=" * 60)
    print(f"UPDATE COMPLETE: {old_version} -> {new_version}")
    print("=" * 60)
    print()
    print("Updated:")
    print("  - .claude/hooks/")
    print("  - .claude/commands/")
    print("  - .claude/agents/")
    print("  - .claude/skills/")
    print("  - .claude/SKILL.md/")
    print("  - .claude/settings.json")
    print("  - scripts/")
    print("  - templates/")
    print("  - requirements-engineering.txt")
    print()
    print("Preserved:")
    print("  - All project content (calculations, docs, design, etc.)")
    print("  - project_params.py")
    print("  - CONTEXT.md, CLAUDE.md, WORKFLOW.md")
    print("  - .claude/settings.local.json")
    print()
    print("Next: Run 'python verify-setup.py' to verify the update")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update existing project with latest toolkit"
    )

    parser.add_argument("path", help="Project path to update")
    parser.add_argument("--force", action="store_true",
                        help="Force update even if versions match")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be updated")

    args = parser.parse_args()

    update_project(Path(args.path), force=args.force, dry_run=args.dry_run)
