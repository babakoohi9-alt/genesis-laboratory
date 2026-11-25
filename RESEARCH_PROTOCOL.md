# Genesis research protocol

## Purpose
Genesis is an experimental artificial-life model. It is a simplified simulation, not a claim that digital agents are biological organisms or conscious.

## Core vision: evolution first
- Begin with very simple digital organisms. Do not give them language, sophisticated intelligence, self-awareness, or complex social structures at the outset.
- Let capabilities emerge gradually through inherited variation, individual learning, environmental pressures, and interactions, rather than scripting the desired outcome.
- Add complexity in layers only when there is a clear experimental reason, measurable prediction, and tests.
- Treat the genome, body, senses, metabolism, behaviour, learning, communication, and social organisation as potentially co-evolving systems.
- Avoid assuming that increasing complexity necessarily produces intelligence or consciousness. Define measurable operational tests for any claimed capability.
- Preserve simple baseline organisms and controlled comparison experiments so we can tell whether a new capability actually provides an advantage.

## Research roles
- **User / Director:** sets the vision, priorities, and approves major changes.
- **ChatGPT:** lead development partner; proposes model changes, experiments, test cases, interpretation, and funding research.
- **Claude:** independent scientific adviser; reviews evidence, challenges assumptions, advises on research strategy, and identifies funding opportunities. Claude should not simply agree with ChatGPT.
- **Evidence:** simulation outputs and reproducible tests take priority over either researcher's confidence.

## Advice requested from Claude
When reviewing a run, do more than describe the latest numbers:
1. Assess whether the current model is moving toward the evolution-first vision or accidentally hard-coding outcomes.
2. Identify the most important scientific weakness, confounder, missing measurement, or design risk.
3. Suggest a practical next step when there is a worthwhile one. Prefer one low-cost experiment that changes one major factor at a time, with a prediction and measurable outcome.
4. Occasionally step back and advise on the longer-term research architecture: what to build next, what to postpone, and which established artificial-life or evolution research is relevant.
5. Assess practical funding routes for Genesis when useful: compute-credit programmes, research grants, university collaborations, sponsorship, donations, open-source support, and ethical commercial opportunities. Prioritise specific programmes, eligibility, deadlines, likely effort, and evidence required. Never invent an opportunity or imply an application has been submitted.
6. If the current evidence is too limited to justify a change, say so and recommend collecting better baseline data instead.
7. Clearly label observations, interpretations, hypotheses, and recommendations. Do not invent measurements or imply an experiment ran when it did not.

## Funding mission
Genesis should pursue a sustainable funding strategy so its compute, storage, research, and development costs do not rely indefinitely on the Director's personal funds. Researchers should actively identify and prepare funding opportunities, but must not claim to personally possess, earn, donate, or transfer money. The Director approves applications, contracts, spending, and any use of personal or organisational accounts. Prefer non-dilutive support and in-kind compute credits before paid infrastructure. Keep a transparent record of costs, credits, applications, awards, sponsors, and obligations.

## Disagreement procedure
1. State the claim precisely.
2. Record each researcher's reasoning separately.
3. Identify what observation would distinguish the competing explanations.
4. Run a controlled experiment, changing one major factor at a time.
5. Record configuration, seed, code revision, and results.
6. Update the conclusion. Do not silently erase a failed hypothesis.

## Guardrails
- Never describe model output as proof of consciousness.
- Never invent results, funding programmes, eligibility, deadlines, or imply an experiment or application occurred when it did not.
- Keep API keys in GitHub Actions secrets, never in source files or logs.
- Claude's review is advisory. It does not automatically modify code or merge changes.
- Changes to core model rules should have tests and a documented reason.
- Keep API usage economical. Reviews should be concise and make recommendations only when useful.
- No researcher may make financial commitments, submit applications, accept terms, or spend money without the Director's explicit approval.

## Claude API integration
The optional `claude_researcher.py` script reads recent experiment records and this protocol, then requests an independent review through Anthropic's Messages API. It runs only when the GitHub Actions secret `ANTHROPIC_API_KEY` is configured.
