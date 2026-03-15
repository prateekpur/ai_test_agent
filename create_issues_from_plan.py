"""
create_issues_from_plan.py

Usage:
    python create_issues_from_plan.py

Requirements:
- GitHub CLI installed and authenticated: https://cli.github.com/
- PLAN.md in the same directory
"""

import re
import subprocess

# Mapping phases to milestones (adjust if needed)
phase_milestones = {
    "Phase 0": "Project Bootstrap",
    "Phase 1": "Core Infrastructure",
    "Phase 2": "Fake Agents",
    "Phase 3": "Real LLM (API)",
    "Phase 4": "Web UI Tests",
    "Phase 5": "Mobile / Device Tests",
    "Phase 6": "Workflow Hardening",
    "Phase 7": "Stretch Goals"
}

def get_phase(line):
    """Return phase key if line starts with a phase"""
    match = re.match(r'## (Phase \d+)', line)
    return match.group(1) if match else None

def get_tasks_from_plan(plan_path="PLAN.md"):
    tasks = []
    current_phase = None

    with open(plan_path, "r") as f:
        for line in f:
            line = line.strip()
            # Detect phase
            phase = get_phase(line)
            if phase:
                current_phase = phase
                continue
            print("Current phase : " + str(current_phase))
            # Detect task: "- [ ] Task description"
            task_match = re.match(r'-\s*\[\s*\]\s*(.+)', line)
            if task_match and current_phase:
                task_desc = task_match.group(1)
                tasks.append({
                    "phase": current_phase,
                    "title": task_desc[:50],  # truncate for title if too long
                    "body": task_desc
                })
    print("Taks length : " + str(len(tasks)))
    return tasks

def create_github_issue(task):
    milestone = phase_milestones.get(task["phase"], None)
    print("Milestone : " + str(milestone))
    cmd = [
        "gh", "issue", "create",
        "--title", task["title"],
        "--body", task["body"],
        "--repo", "prateekpur/ai_test_agent" 
    ]
    if milestone:
        cmd.extend(["--milestone", milestone])
    print(f"Creating issue: {task['title']} (Milestone: {milestone})")
    subprocess.run(cmd)

if __name__ == "__main__":
    tasks = get_tasks_from_plan()

    for task in tasks:
        create_github_issue(task)