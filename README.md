# AI Job Search — India New-Grad Backend Edition

A personalized layer on top of [MadsLorentzen/ai-job-search](https://github.com/MadsLorentzen/ai-job-search) for **2026 software-engineering graduates in India**, with a backend-first search strategy, strict fresher eligibility filtering, and referral outreach.

This repository does **not** commit your resume, contact details, application history, or generated job-search workspace. Instead, it pins the upstream framework as a submodule and applies the custom overlay into a local `workspace/` directory.

## What this version changes

The upstream project already provides a strong agentic job-search workflow:

```
/setup -> /scrape -> /rank -> /apply -> /outcome
```

This edition adds:

- **India-first discovery** across Bengaluru, Hyderabad, Pune, Mumbai, Gurugram/Noida/Delhi NCR, Chennai, Kolkata, Ahmedabad and Remote India.
- **Backend-first ranking** for Java/Spring Boot, REST APIs, microservices, AWS/SQS/RDS, PostgreSQL, event-driven systems, Docker, Jenkins/CI-CD, Temporal, Go and distributed-systems work.
- A strict **fresher/new-grad gate** applied before normal fit scoring.
- **`/daily-batch`** for a complete daily search → rank → referral queue.
- **`/referrals`** for finding relevant public LinkedIn referral targets and generating concise outreach.
- Priority for **IIIT Allahabad alumni**, relevant engineers/managers, then technical/early-career recruiters.
- Clear separation of **Primary**, **Stretch**, and **Ineligible** roles.
- No padding: if only 6 genuinely good fresher roles exist, the workflow returns 6 instead of inventing quality.

## Candidate profile this overlay is optimized for

The supplied template assumes:

- B.Tech IT, IIIT Allahabad, graduating 2026
- SDE internship at ACKO
- Java / Spring Boot
- REST APIs / microservices
- AWS / RDS / SQS
- PostgreSQL / Elasticsearch
- event-driven workflows
- idempotency / retries / state transitions
- Temporal
- Docker / Jenkins / CI-CD
- Go / C++ / Python / JavaScript / TypeScript
- strong DSA background
- CodeChef 3-star
- Flipkart Grid finalist

The profile intentionally leaves **name, email, phone, LinkedIn, GitHub, exact resume bullets and metrics** as placeholders. Fill those only in your local workspace.

---

# Repository layout

```
AI-Job-Search/
├── _upstream/                # pinned MadsLorentzen/ai-job-search submodule
├── overlay/
│   ├── .claude/
│   │   ├── commands/
│   │   │   ├── daily-batch.md
│   │   │   └── referrals.md
│   │   └── skills/
│   │       ├── job-application-assistant/
│   │       │   └── 01-candidate-profile.md
│   │       ├── job-scraper/
│   │       │   └── search-queries.md
│   │       └── referral-finder/
│   │           └── SKILL.md
│   ├── FRESHER_GATE.md
│   └── install_overlay.py
├── bootstrap.sh
├── UPSTREAM_COMMIT
└── README.md
```

`workspace/` is generated locally by the bootstrap script and is ignored by Git.

---

# Quick start

## 1. Clone with the upstream submodule

```bash
git clone --recurse-submodules https://github.com/Menma420/AI-Job-Search.git
cd AI-Job-Search
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

## 2. Build the customized workspace

```bash
chmod +x bootstrap.sh
./bootstrap.sh
```

This:

1. initializes the pinned upstream checkout,
2. creates a clean `workspace/` copy,
3. applies the India/new-grad overlay,
4. preserves upstream files,
5. inserts the fresher gate into the evaluation framework,
6. adds `/daily-batch` and `/referrals`.

Re-running `./bootstrap.sh` recreates the workspace from the pinned upstream version. Existing `workspace/` is moved to a timestamped backup first.

## 3. Enter the workspace

```bash
cd workspace
```

## 4. Install prerequisites

The upstream project currently expects:

- Python 3.10+
- Bun
- Claude Code for the full command workflow, **or** another compatible agent runtime using `AGENTS.md`
- LaTeX (`lualatex` + `xelatex`) if you want generated PDF CVs/cover letters
- optional `pypdf` for ATS PDF verification

Install the globally useful job-search CLIs:

```bash
for tool in linkedin-search freehire-search; do
  (cd ".agents/skills/$tool/cli" && bun install)
done
```

The original upstream repo includes Denmark-specific search skills too. This overlay marks those as disabled for the India workflow; the global LinkedIn and Freehire search tools remain useful.

---

# Configure your profile

You have two options.

## Option A — use upstream `/setup`

From inside `workspace/`:

```bash
claude
```

Then:

```
/setup
```

Let the framework ingest your resume/documents, then reconcile the generated profile with:

```
.claude/skills/job-application-assistant/01-candidate-profile.md
```

Keep exact facts from your resume authoritative.

## Option B — edit the profile manually

Open:

```
.claude/skills/job-application-assistant/01-candidate-profile.md
```

Fill:

- name
- email
- phone
- LinkedIn
- GitHub
- exact ACKO dates/bullets
- exact project names
- exact metrics
- exact ML/research internship details

Do **not** add claims that are not on your resume or otherwise verifiable.

---

# Core daily workflow

## Recommended: `/daily-batch`

Run:

```
/daily-batch
```

It orchestrates the full search:

```
discover
   ↓
verify live posting
   ↓
fresher eligibility gate
   ↓
fit scoring
   ↓
deduplicate
   ↓
primary + stretch shortlist
   ↓
referral discovery
   ↓
send-ready outreach queue
```

The default target is **up to 10 new jobs per batch**.

It deliberately returns fewer than 10 if the remaining jobs are weak, stale, duplicated or clearly ineligible.

### Expected output

For each batch:

- counts: primary / stretch / expired / experience-rejected
- ranked primary jobs
- location
- exact/faithful experience requirement
- freshness/posting date
- direct official apply link where possible
- strongest overlap
- one honest gap
- stretch roles separately
- 1–3 referral targets per primary company
- a concise message for the best target
- top-5 `APPLY FIRST` order

---

# Fresher eligibility rules

The experience gate runs **before fit scoring**.

| Job wording | Classification |
|---|---|
| Freshers / New Grad / Graduate / 2026 graduates | **Primary** |
| 0–1 years | **Primary** |
| 0–2 years | **Primary** |
| Bachelor's + no minimum experience | **Primary**, absent conflicting wording |
| 1+ year / 1–2 years | **Stretch** |
| 1–3 years | **Stretch** |
| 2 years preferred | **Stretch** |
| 2+ years required | **Not primary** |
| 2–4 / 3+ years required | **Not primary** |
| SDE II / Senior / Staff / Lead / Manager | **Reject**, unless requirements unexpectedly say otherwise |

Important:

> **Required years override the job title.**

A role named “Software Engineer I” that says “2–4 years required” does not become a fresher role because of the title.

The ACKO internship is treated as meaningful production engineering evidence for fit, but is **never converted into fabricated full-time YOE**.

---

# Search strategy

The customized query set prioritizes:

## Backend

- Backend Engineer
- Software Engineer — Backend
- Java Backend Engineer
- Spring Boot Engineer
- SDE I / SDE 1
- Software Engineer I / 1
- distributed systems entry-level
- platform engineering entry-level
- Go backend roles

## General SWE

- Associate Software Engineer
- Graduate Software Engineer
- New Grad Software Engineer
- Early Career Software Engineer
- 2026 graduate engineering programs

## Adjacent roles

Only when genuinely fresher-friendly:

- Platform
- Infrastructure
- Cloud engineering
- SRE
- DevOps
- Full-stack roles with meaningful backend ownership

## Sources

Prefer:

1. official company careers page
2. Lever
3. Greenhouse
4. Ashby
5. Workday
6. SmartRecruiters
7. Jobvite
8. LinkedIn/public job boards for discovery
9. Wellfound / YC / startup boards
10. Indian job boards where useful

When a board result exists but an official posting can be found, the official posting wins.

---

# Referral workflow

Run:

```
/referrals
```

or:

```
/referrals --top 10
```

or:

```
/referrals <company>
```

or:

```
/referrals <job URL>
```

Target priority:

1. **IIIT Allahabad alumni** at the company
2. relevant backend/software/platform engineers
3. engineering manager / tech lead when publicly identifiable
4. technical / university / early-career recruiters
5. recent hires into similar roles

The workflow should not spam a company. Two strong targets are better than eight random employees.

## LinkedIn connection notes

Keep first-contact notes short. A useful target is **≤300 characters** when LinkedIn's connection-note UI is the constraint.

Good pattern:

```
Hi <Name>, I’m a 2026 IIIT Allahabad student and SDE Intern at ACKO,
working on <1-2 relevant areas>. I saw <Company>'s <Role> opening and
it aligns closely. Would you be comfortable referring me? Happy to share my resume.
```

For recruiters, replace “refer me” with:

```
Would you be open to reviewing my profile or connecting me with the relevant hiring team?
```

For stretch roles, acknowledge the mismatch rather than hiding it.

---

# Manual workflow

You can still use the upstream commands individually.

## Discover

```
/scrape broad
```

## Rank

```
/rank --limit 30 --top 10
```

## Find referrals

```
/referrals --top 10
```

## Apply

```
/apply <job-url>
```

The upstream `/apply` workflow evaluates the job more deeply and can generate a tailored CV and cover letter.

## Track outcomes

```
/outcome
```

Useful variants include follow-up/stale-pipeline handling according to the upstream command.

## Gmail status sync

If using the supported Gmail integration:

```
/gmail-sync
```

This proposes status changes from real application emails and asks for approval before mutating the tracker.

---

# Using Codex / Gemini CLI / other agents

The upstream framework contains `AGENTS.md` and portable skills under `.agents/skills/`.

For non-Claude agents:

1. open the generated `workspace/`,
2. instruct the agent to read `AGENTS.md`,
3. use the canonical workflow specs under `.claude/`,
4. invoke/search with the portal CLIs under `.agents/skills/`.

The slash-command UX may differ by agent. The Markdown command files remain the workflow specification.

---

# Data and privacy

This matters.

Your generated workspace may eventually contain:

- phone/email
- resume history
- salary expectations
- job applications
- recruiter/contact notes
- generated CVs/cover letters
- application outcomes

Therefore:

- `workspace/` is gitignored in this repo.
- Do not commit your populated personal profile to this public repository.
- Do not commit `job_search_tracker.csv`, application archives or generated resumes here.
- Keep the repository code public if you want; keep the actual search workspace local/private.

If you want the whole populated workspace under version control, create a **separate private repository**.

---

# Updating upstream

The upstream project is pinned as a Git submodule.

See the currently pinned commit:

```bash
cat UPSTREAM_COMMIT
git -C _upstream rev-parse HEAD
```

To test a newer upstream version:

```bash
cd _upstream
git fetch origin
git checkout origin/master
cd ..
./bootstrap.sh
```

Run your normal workflow/tests against the rebuilt workspace.

If it works, update the submodule pointer in this repository and update `UPSTREAM_COMMIT`.

The overlay installer intentionally edits only a small surface area so upstream updates are easier to absorb.

---

# Rebuild / reset

To get a clean generated workspace:

```bash
./bootstrap.sh
```

The script backs up an existing `workspace/` directory before rebuilding.

To inspect what the overlay changed, compare:

```bash
diff -ru _upstream/.claude workspace/.claude
```

---

# Troubleshooting

## `_upstream` is empty

Run:

```bash
git submodule update --init --recursive
```

## `bootstrap.sh` says upstream is missing

You cloned without submodules. Initialize it using the command above.

## `/daily-batch` does not appear

Confirm:

```bash
ls workspace/.claude/commands/daily-batch.md
```

If missing, rebuild:

```bash
./bootstrap.sh
```

## Personal placeholders are still present

Edit:

```
workspace/.claude/skills/job-application-assistant/01-candidate-profile.md
```

or run `/setup` and merge the exact resume facts.

## Denmark-specific portals are still being searched

The India workflow should prioritize `linkedin-search`, `freehire-search`, ATS/company-career searches and the custom India queries. If an agent ignores the disabled metadata, explicitly instruct it to follow:

```
workspace/.claude/skills/job-scraper/search-queries.md
```

## A job titled “Software Engineer I” requires 3 years

That is not a primary fresher job. The experience gate is authoritative.

---

# Upstream attribution

This project customizes the MIT-licensed:

**Mads Lorentzen — AI Job Search**  
https://github.com/MadsLorentzen/ai-job-search

The upstream MIT license and copyright notice are preserved in `LICENSE`.

This repository is an independent customization and is not affiliated with Anthropic, LinkedIn, ACKO, IIIT Allahabad, or any employer searched by the workflow.

---

# Practical recommended routine

A productive daily loop:

```
6 PM
│
├─ /daily-batch
│   ├─ inspect top 10
│   ├─ apply to top 3-5
│   └─ send referral messages
│
├─ update tracker
│
└─ every few days
    ├─ /gmail-sync
    └─ /outcome followup
```

Quality > application count. The workflow is intentionally conservative about eligibility and factual claims.
