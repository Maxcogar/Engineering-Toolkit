#!/usr/bin/env python3
"""
Verify engineering project setup against toolkit requirements.

Usage:
    python verify-setup.py [project-path]
    python verify-setup.py ../projects/pump-design
    python verify-setup.py --strict  # Treat warnings as errors
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Required directories
REQUIRED_DIRS = [
    ".claude",
    "calculations",
    "design",
    "docs",
    "manufacturing",
    "scripts",
    "templates",
    "testing",
    "verification",
]

# Required core files
REQUIRED_FILES = [
    "CONTEXT.md",
    "CLAUDE.md",
    "WORKFLOW.md",
    "project_params.py",
    ".gitignore",
]

# Required CONTEXT.md sections
CONTEXT_SECTIONS = [
    "Project State",
    "Critical Parameters",
    "System Status",
]

# Required hooks
REQUIRED_HOOKS = [
    "check-context-update.py",
    "enforce-documentation-before-design.py",
    "require-context-before-work.py",
    "validate-bash-safety.py",
]

# Required commands
REQUIRED_COMMANDS = [
    "decision.md",
    "prime.md",
    "research.md",
    "understand.md",
    "verify-calc.md",
]

# Required agents
REQUIRED_AGENTS = [
    "doc-specialist.md",
    "knowledge-builder.md",
    "systematic-engineer.md",
    "memory-ingest.md",
    "memory-search.md",
]

# Required skill definition files
REQUIRED_SKILLS = [
    "skills/SKILL.md",
]

# Required skill template files
REQUIRED_SKILL_TEMPLATES = [
    "SKILL.md/CONTEXT.md",
    "SKILL.md/decision-template.md",
    "SKILL.md/init-engineering-project.sh",
    "SKILL.md/reference-template.md",
    "SKILL.md/sources-template.md",
    "SKILL.md/TODO.md",
    "SKILL.md/workspace-structure.md",
]

# Required scripts
REQUIRED_SCRIPTS = [
    "setup_rag.py",
    "rag_query.py",
    "generate_dashboard.py",
]


class Verifier:
    def __init__(self, project_path: Path, strict: bool = False):
        self.project_path = project_path.resolve()
        self.strict = strict
        self.passes = 0
        self.warnings = 0
        self.errors = 0

    def check(self, condition: bool, message: str, is_warning: bool = False) -> bool:
        """Record a check result."""
        if condition:
            self.passes += 1
            return True
        elif is_warning:
            self.warnings += 1
            print(f"  [WARN] {message}")
            return False
        else:
            self.errors += 1
            print(f"  [FAIL] {message}")
            return False

    def verify_structure(self) -> int:
        """Verify required directories exist."""
        print("\n[Structure]")
        count = 0
        for dir_path in REQUIRED_DIRS:
            full_path = self.project_path / dir_path
            if self.check(full_path.is_dir(), f"Missing directory: {dir_path}"):
                count += 1
        print(f"  [PASS] {count}/{len(REQUIRED_DIRS)} directories")
        return count

    def verify_core_files(self) -> int:
        """Verify required core files exist."""
        print("\n[Core Files]")
        count = 0
        for file_path in REQUIRED_FILES:
            full_path = self.project_path / file_path
            if self.check(full_path.is_file(), f"Missing file: {file_path}"):
                count += 1
        print(f"  [PASS] {count}/{len(REQUIRED_FILES)} core files")
        return count

    def verify_context_md(self) -> int:
        """Verify CONTEXT.md has required sections."""
        print("\n[CONTEXT.md Validation]")
        context_path = self.project_path / "CONTEXT.md"

        if not context_path.is_file():
            self.errors += 1
            print("  [FAIL] CONTEXT.md not found")
            return 0

        content = context_path.read_text(encoding='utf-8')
        count = 0
        for section in CONTEXT_SECTIONS:
            if self.check(section in content, f"Missing section: {section}"):
                count += 1

        print(f"  [PASS] {count}/{len(CONTEXT_SECTIONS)} required sections")
        return count

    def verify_claude_config(self) -> tuple:
        """Verify Claude configuration."""
        print("\n[Claude Configuration]")

        claude_dir = self.project_path / ".claude"

        # Check settings.json
        settings_path = claude_dir / "settings.json"
        settings_valid = False
        if settings_path.is_file():
            try:
                json.loads(settings_path.read_text(encoding='utf-8'))
                self.passes += 1
                settings_valid = True
            except json.JSONDecodeError:
                self.check(False, "settings.json is invalid JSON")
        else:
            self.check(False, "settings.json not found")

        # Check settings.local.json (core-memory config)
        settings_local_path = claude_dir / "settings.local.json"
        settings_local_valid = False
        if settings_local_path.is_file():
            try:
                json.loads(settings_local_path.read_text(encoding='utf-8'))
                self.passes += 1
                settings_local_valid = True
            except json.JSONDecodeError:
                self.check(False, "settings.local.json is invalid JSON")
        else:
            self.check(False, "settings.local.json not found")

        # Check hooks
        hooks_dir = claude_dir / "hooks"
        hooks_count = 0
        for hook in REQUIRED_HOOKS:
            if (hooks_dir / hook).is_file():
                hooks_count += 1
                self.passes += 1
            else:
                self.check(False, f"Missing hook: {hook}")

        # Check commands
        commands_dir = claude_dir / "commands"
        commands_count = 0
        for cmd in REQUIRED_COMMANDS:
            if (commands_dir / cmd).is_file():
                commands_count += 1
                self.passes += 1
            else:
                self.check(False, f"Missing command: {cmd}")

        # Check agents
        agents_dir = claude_dir / "agents"
        agents_count = 0
        for agent in REQUIRED_AGENTS:
            if (agents_dir / agent).is_file():
                agents_count += 1
                self.passes += 1
            else:
                self.check(False, f"Missing agent: {agent}")

        # Check skills
        skills_count = 0
        for rel_path in REQUIRED_SKILLS:
            if (claude_dir / rel_path).is_file():
                skills_count += 1
                self.passes += 1
            else:
                self.check(False, f"Missing skill file: {rel_path}")

        skill_templates_count = 0
        for rel_path in REQUIRED_SKILL_TEMPLATES:
            if (claude_dir / rel_path).is_file():
                skill_templates_count += 1
                self.passes += 1
            else:
                self.check(False, f"Missing skill template: {rel_path}")

        print(f"  Settings: {'valid' if settings_valid else 'INVALID'}")
        print(f"  Settings.local: {'valid' if settings_local_valid else 'MISSING/INVALID'}")
        print(f"  Hooks: {hooks_count}/{len(REQUIRED_HOOKS)}")
        print(f"  Commands: {commands_count}/{len(REQUIRED_COMMANDS)}")
        print(f"  Agents: {agents_count}/{len(REQUIRED_AGENTS)}")
        print(f"  Skills: {skills_count}/{len(REQUIRED_SKILLS)}")
        print(f"  Skill templates: {skill_templates_count}/{len(REQUIRED_SKILL_TEMPLATES)}")

        return (hooks_count, commands_count, agents_count)

def verify_scripts(self) -> int:
        """Verify required scripts exist."""
        print("\n[Scripts]")
        scripts_dir = self.project_path / "scripts"
        count = 0
        for script in REQUIRED_SCRIPTS:
            if self.check((scripts_dir / script).is_file(), f"Missing script: {script}"):
                count += 1
        print(f"  [PASS] {count}/{len(REQUIRED_SCRIPTS)} scripts")
        return count

    def verify_templates(self) -> int:
        """Verify templates directory has content."""
        print("\n[Templates]")
        templates_dir = self.project_path / "templates"
        if not templates_dir.is_dir():
            self.check(False, "templates directory not found")
            return 0

        templates = list(templates_dir.glob("*.md")) + list(templates_dir.glob("*.ipynb"))
        count = len(templates)

        if self.check(count >= 6, f"Expected at least 6 templates, found {count}"):
            print(f"  [PASS] {count} templates found")
        return count

    def verify_git(self) -> bool:
        """Verify git repository (warning only)."""
        print("\n[Git]")
        git_dir = self.project_path / ".git"

        if not git_dir.is_dir():
            self.check(False, "Not a git repository", is_warning=True)
            return False

        self.passes += 1
        try:
            result = subprocess.run(
                ["git", "-C", str(self.project_path), "rev-parse", "--verify", "HEAD"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.passes += 1
                print("  [PASS] Git repository initialized with commits")
                return True
            self.check(False, "Git repository has no commits", is_warning=True)
            return False
        except FileNotFoundError:
            self.check(False, "Git not available to verify commits", is_warning=True)
            return False

    def verify_optional(self):
        """Check optional components."""
        print("\n[Optional Components]")

        # RAG
        chroma_db = self.project_path / "chroma_db"
        if chroma_db.is_dir():
            print("  [INFO] RAG index present")
        else:
            print("  [INFO] RAG index not initialized")

        # Venv
        venv = self.project_path / ".venv"
        if venv.is_dir():
            print("  [INFO] Virtual environment present")
        else:
            print("  [INFO] Virtual environment not created")

        # Dashboard
        dashboard = self.project_path / "dashboard.html"
        if dashboard.is_file():
            print("  [INFO] Dashboard generated")
        else:
            print("  [INFO] Dashboard not generated")

    def run(self) -> int:
        """Run all verifications."""
        print(f"Verifying: {self.project_path}")

        if not self.project_path.is_dir():
            print(f"ERROR: Path does not exist: {self.project_path}")
            return 1

        self.verify_structure()
        self.verify_core_files()
        self.verify_context_md()
        self.verify_claude_config()
        self.verify_scripts()
        self.verify_templates()
        self.verify_git()
        self.verify_optional()

        # Summary
        print()
        print("=" * 60)
        print(f"SUMMARY: {self.passes} passed, {self.warnings} warnings, {self.errors} errors")

        if self.errors > 0:
            print("STATUS: INVALID")
            return 1
        elif self.warnings > 0 and self.strict:
            print("STATUS: INVALID (strict mode)")
            return 2
        elif self.warnings > 0:
            print("STATUS: VALID (with warnings)")
            return 0
        else:
            print("STATUS: VALID")
            return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify engineering project setup",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Project path to verify (default: current directory)"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors"
    )

    args = parser.parse_args()

    verifier = Verifier(Path(args.path), strict=args.strict)
    sys.exit(verifier.run())
