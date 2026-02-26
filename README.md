# 🤖 AI Development Team

Multi-agent system for automated software development powered by Claude Agent SDK.

## Architecture

Three specialized AI agents collaborate through GitHub Issues + Projects:

| Agent | Role | Responsibility |
|-------|------|---------------|
| **Architect** | Team Leader | Decomposes tasks into specs, creates subtasks, makes releases |
| **Developer** | Teammate | Writes code based on specs, creates PRs |
| **Tester** | Teammate | Validates code against specs, approves or returns |

## Workflow

```
User creates Issue → Architect writes spec → Developer codes → Tester validates
                                                    ↑                    ↓
                                                    └── fix if rejected ←┘
                                              Architect merges & releases
                                              Tester verifies release ✅
```

## Project Structure

```
├── .github/
│   ├── workflows/          ← GitHub Actions (tests, deploy, Telegram notifications)
│   └── ISSUE_TEMPLATE/     ← Templates for creating tasks
├── agents/
│   ├── architect.py        ← Architect agent configuration
│   ├── developer.py        ← Developer agent configuration
│   ├── tester.py           ← Tester agent configuration
│   ├── orchestrator.py     ← Main orchestrator (polls GitHub, runs agents)
│   └── tools/
│       ├── github_tools.py ← Custom tools for GitHub API
│       └── telegram_tools.py ← Custom tools for Telegram
├── specs/                  ← Specs from Architect (markdown)
├── src/                    ← Application code
├── tests/                  ← Tests
├── CLAUDE.md               ← Instructions for all agents
├── .env.example            ← Environment variables template
└── requirements.txt        ← Python dependencies
```

## Quick Start

```bash
# 1. Clone repo
git clone https://github.com/oleglgt/Ollgt_Develop_team.git
cd Ollgt_Develop_team

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run orchestrator
python agents/orchestrator.py
```

## GitHub Project Setup

Create a GitHub Project with these columns:
- 📥 Inbox
- 📋 Spec
- 🛠 Development
- 🧪 Testing
- 🚀 Release
- ✅ Done

## Labels

| Label | Purpose |
|-------|---------|
| `role:architect` | Tasks for architect agent |
| `role:developer` | Tasks for developer agent |
| `role:tester` | Tasks for tester agent |
| `role:human` | Requires user attention |
| `type:feature` | New feature |
| `type:bug` | Bug fix |
| `type:release` | Release task |
| `priority:high/medium/low` | Priority levels |

## Telegram Notifications

The system sends notifications to Telegram on:
- Spec ready
- PR created
- Test results (approve/return)
- Release published
- Release verified
