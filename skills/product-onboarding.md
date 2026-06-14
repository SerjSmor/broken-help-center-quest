# Product Onboarding

Product onboarding is agent-mediated.

Use Codex, Claude Code, or OpenCode to talk to Maya, the product lead, and uncover the Quest 1 task.

Maya should reveal that the learner is working with SiteForge, a website-builder company for small businesses.

She should also reveal that the help-center bot exists, nobody has a quality baseline, the first goal is measurement, and agentic RAG is out of scope.

The learner must write the engineering ticket manually after onboarding.

Use `skills/maya-product-lead.md` as Maya's persona and knowledge scaffold.

During product discovery, the agent should always show three hidden checkboxes:

```text
Discovery checklist:
- [ ] ???
- [ ] ???
- [ ] ???
```

The agent reveals each checkbox label only after the learner asks a qualifying product-discovery question. The learner may ask for tips, but tips should not reveal exact checkbox labels or exact right questions.

When all three are checked, the agent should create:

```text
requirements/quest_01_product_requirements.md
```

Then update `.buildguild/state.json`:

```json
{
  "quest_01": {
    "product_onboarding_completed": true,
    "data_tour_completed": false
  }
}
```

After the learner runs `uv run --extra dev invoke tour` and confirms they reviewed the data, update:

```json
{
  "quest_01": {
    "data_tour_completed": true
  }
}
```
