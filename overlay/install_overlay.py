#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys
from datetime import datetime

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
OVERLAY = Path(__file__).resolve().parent

required = [ROOT / "AGENTS.md", ROOT / ".claude", ROOT / ".agents"]
if not all(p.exists() for p in required):
    raise SystemExit(f"{ROOT} does not look like the ai-job-search repository root")

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = ROOT / f".india-newgrad-backup-{stamp}"
backup.mkdir(parents=True, exist_ok=True)

files = [
    ".claude/skills/job-scraper/search-queries.md",
    ".claude/skills/job-application-assistant/01-candidate-profile.md",
    ".claude/skills/referral-finder/SKILL.md",
    ".claude/commands/referrals.md",
    ".claude/commands/daily-batch.md",
]

for rel in files:
    src = OVERLAY / rel
    dst = ROOT / rel
    if dst.exists():
        b = backup / rel
        b.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dst, b)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

eval_path = ROOT / ".claude/skills/job-application-assistant/04-job-evaluation.md"
text = eval_path.read_text(encoding="utf-8")
start = "<!-- INDIA_NEWGRAD_GATE_START -->"
end = "<!-- INDIA_NEWGRAD_GATE_END -->"
section = (OVERLAY / "FRESHER_GATE.md").read_text(encoding="utf-8").strip()
block = f"\n{start}\n{section}\n{end}\n"

if start in text and end in text:
    before = text.split(start, 1)[0]
    after = text.split(end, 1)[1]
    new_text = before + block + after
else:
    marker = "## Scoring Dimensions"
    if marker not in text:
        raise SystemExit("Could not find Scoring Dimensions marker in 04-job-evaluation.md")
    b = backup / ".claude/skills/job-application-assistant/04-job-evaluation.md"
    b.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(eval_path, b)
    new_text = text.replace(marker, block + "\n" + marker, 1)

eval_path.write_text(new_text, encoding="utf-8")

for skill_dir in (ROOT / ".agents/skills").iterdir():
    if not skill_dir.is_dir():
        continue
    name = skill_dir.name
    if name in {"linkedin-search", "freehire-search"}:
        continue
    skill = skill_dir / "SKILL.md"
    if not skill.exists():
        continue
    raw = skill.read_text(encoding="utf-8")
    if name not in {"jobbank-search", "jobdanmark-search", "jobindex-search", "jobnet-search"}:
        continue
    b = backup / f".agents/skills/{name}/SKILL.md"
    b.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(skill, b)
    if "enabled: true" in raw:
        raw = raw.replace("enabled: true", "enabled: false", 1)
    elif "enabled: false" not in raw and raw.startswith("---"):
        raw = raw.replace("---\n", "---\nenabled: false\n", 1)
    skill.write_text(raw, encoding="utf-8")

print("India/new-grad overlay installed.")
print(f"Backup of replaced files: {backup}")
print("Next: fill exact resume details in 01-candidate-profile.md, then run /daily-batch.")
