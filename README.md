# BuildGuild: Broken Help Center

Welcome to BuildGuild, a repo-based learning game where you build AI products by working through messy product requests, engineering tradeoffs, and validation gates.

You are the engineer on Quest 1.

The fictional company has a help-center bot. It answers questions, sort of. Nobody knows if it retrieves the right articles, whether the answers are useful, or where it fails.

Quest 1 uses the WixQA benchmark from Hugging Face as the task dataset. The company is fictional, but the knowledge base and evaluation data are WixQA-derived because they provide a realistic website-builder support corpus without exposing proprietary production data.

Your mission:

```text
Create the first measurable baseline.
```

No agents. No fancy reranking. No dashboard. First, prove what the bot can and cannot do today.

## Install

This project uses Python and Invoke tasks.

From the repo root:

```text
uv run --extra dev invoke data
uv run --extra dev buildguild status
```

This is the recommended path for a fresh checkout. `uv` creates and manages the project environment, includes the development dependencies, and runs the command without requiring a separate install step.

Optional: install the local CLI into the project environment if you want shorter commands while working repeatedly:

```text
uv run --extra dev invoke install
uv run buildguild status
```

The bare command `buildguild ...` only works if the project environment is installed and its `bin` directory is on your shell `PATH`, for example after activating `.venv`. When in doubt, use `uv run buildguild ...`.

## Start Quest 1

Open Codex, Claude Code, or OpenCode in this repo and ask it:

```text
Use skills/maya-product-lead.md to role-play Maya and run Quest 1 product discovery with me.
```

No terminal command is needed to start the Maya conversation. The agent should read the markdown skill file and role-play Maya directly. This avoids environment setup, `uv`, and cache permissions during product discovery.

You will meet Maya, the product lead, in the SiteForge product room. Ask questions until you understand what she actually needs.

She will welcome you to SiteForge, ask your name because she is bad at names, and explain that you have been assigned the most important task on her board. She knows the customer pain, but she is bad at data, so you need to lead by asking the right questions.

Maya will not write the ticket for you.

Maya tracks discovery with four hidden checkboxes:

```text
Discovery checklist:
- [ ] ???
- [ ] ???
- [ ] ???
- [ ] ???
```

Ask the right product questions to uncover each area. When you ask a useful question, Maya reveals and checks the matching box.

You can ask Maya for a tip. Tips should nudge you without revealing the answer.

Once all four are checked, the agent should create:

```text
requirements/quest_01_product_requirements.md
```

Then the agent should update `.buildguild/state.json` and set `quest_01.product_onboarding_completed` to `true`.

## Tour The Data

Before implementing retrieval or evaluation, ask your coding agent to become Ari, the EDA guide:

```text
Use skills/ari-data-guide.md to tour the data with me.
```

Ari is the coding agent in EDA mode. Ari should inspect the dataset, explain the scripts and checks behind the findings, and help you understand what the baseline can rely on.

If you want the visual companion app during the tour, run:

```text
uv run --extra dev invoke tour
```

The Streamlit app shows:

- Help-center articles.
- Evaluation questions.
- Expected answer terms.
- Expected help article sources and content.
- A few guided question-to-document examples.

Ari should create:

```text
notes/quest_01_data_tour.md
```

Then Ari should update `.buildguild/state.json`:

```json
{
  "quest_01": {
    "data_tour_completed": true
  }
}
```

## Write The Technical Spec

After product requirements and Ari's data tour, ask your coding agent:

```text
Use skills/write-technical-spec.md to help me write the Quest 1 technical spec.
```

Create:

```text
specs/quest_01_implementation_spec.md
```

This technical spec is the implementation ticket. There is no separate ticket-review step.

## Your Quest Loop

Use status whenever you are unsure what to do next:

```text
uv run buildguild status
```

If you are using an agent, you can also use the repo-local slash command:

```text
/quest-status
```

The shared status skill is:

```text
skills/quest-status.md
```

Claude Code and Codex slash-command wrappers point to that same skill:

```text
.claude/commands/quest-status.md
.codex/commands/quest-status.md
```

Claude Code can also show the current quest stage in its status line. This repo includes:

```text
.claude/settings.json
tools/quest_statusline.py
```

If Claude Code does not pick it up automatically, run `/statusline` inside Claude Code and set the command to:

```text
python3 tools/quest_statusline.py
```

The status line is intentionally read-only and does not run `uv`; it reads `.buildguild/state.json` and checks the expected quest files directly.

The flow is:

```text
check status
talk to Maya
generate product requirements
tour the data with Ari
write the technical spec
build the baseline RAG
run the evaluation
ask Maya to review the report
validate the quest
```

## What You Will Build

The backend team already wrote a simple lexical retriever in:

```text
app/retrieval.py
```

Nobody knows how well it performs. Quest 1 evaluates that existing baseline over the WixQA-derived benchmark:

- Existing lexical retrieval baseline.
- Baseline answer generation.
- `python -m app.ask "How do I connect a domain?"`
- `python -m evals.run_baseline`
- `reports/baseline_report.md`

The most important score is retrieval quality: did the backend retriever include the expected WixQA source article in the top 5 results? The generated-answer checks are intentionally simple for Quest 1: compare the answer against reference-answer terms, measure answer length, and report concrete positive and negative examples.

The report should include metric definitions, baseline scores, positive examples, and negative failed examples.

After the report exists, ask your coding agent:

```text
Use skills/maya-tests-outputs.md so Maya can review reports/baseline_report.md.
```

If Maya accepts the report, Quest 1 is complete.

## Development

Run tests:

```text
uv run --extra dev invoke test
```

Prepare the WixQA-derived benchmark from Hugging Face:

```text
uv run --extra dev invoke data
```

## Current State

This repo currently contains the early playable skeleton:

- Quest status.
- WixQA dataset preparation through Hugging Face `datasets`.
- Maya persona skill for agent-mediated conversation.
- Maya report-review skill.
- CLI routing.
- Tests for the implemented pieces.

Ticket review and final RAG validation are intentionally stubbed for upcoming phases.
