# Genesis research protocol

## Purpose
Genesis is an experimental artificial-life model. It is a simplified simulation, not a claim that digital agents are biological organisms or conscious.

## Research roles
- **ChatGPT:** proposes model changes, experiments, test cases, and interpretation.
- **Claude:** provides an independent review, challenges assumptions, identifies confounders, and proposes alternative experiments.
- **Evidence:** simulation outputs and reproducible tests take priority over either researcher's confidence.

## Disagreement procedure
1. State the claim precisely.
2. Record each researcher's reasoning separately.
3. Identify what observation would distinguish the competing explanations.
4. Run a controlled experiment, changing one major factor at a time.
5. Record configuration, seed, code revision, and results.
6. Update the conclusion. Do not silently erase a failed hypothesis.

## Guardrails
- Never describe model output as proof of consciousness.
- Never invent results or imply a run occurred when it did not.
- Keep API keys in GitHub Actions secrets, never in source files or logs.
- Claude's review is advisory. It does not automatically modify code or merge changes.
- Changes to core model rules should have tests and a documented reason.

## Claude API integration
The optional `claude_researcher.py` script reads recent experiment records and requests an independent review through Anthropic's Messages API. It runs only when the GitHub Actions secret `ANTHROPIC_API_KEY` is configured.
