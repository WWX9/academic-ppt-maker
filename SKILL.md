---
name: academic-ppt-maker
description: Create, review, and distill academic slide decks with strong conference-talk logic. Use when Codex needs to turn a paper, abstract, manuscript, notes, or research results into a polished academic PPT; learn reusable structure from example PPT/PPTX decks; or critique an academic deck's narrative flow, title chain, method-result closure, and conclusion quality.
---

# Academic PPT Maker

Use this skill to control the **report logic** of an academic deck. Let the `PowerPoint` skill own final PPTX construction, rendering, and export; this skill owns narrative structure, reference distillation, and logic checks.

## Workflow

### 1. Pick the working mode

Choose one of three modes before drafting slides:

- `build-from-source`: Turn a paper, abstract, notes, or results into a new academic deck.
- `distill-from-references`: Learn reusable structure from strong reference PPT/PPTX files.
- `review-existing-deck`: Critique an existing deck and rewrite its logic before redesigning slides.

If the user provides both source material and reference decks, start with `distill-from-references`, then adapt the learned structure to the source material.

### 2. Distill reference decks when they exist

If the user gives example PPT/PPTX files, extract their outline before copying any style choices.

Use `scripts/extract_pptx_logic.py` to pull slide titles, preview text, picture counts, and deck-level signals from `.pptx` references:

```bash
python scripts/extract_pptx_logic.py <root-folder> --limit 12 --json-output review.json --md-output review.md
```

Then read:

- `references/logic-rules.md`
- `references/anti-patterns.md`
- `references/chengdu-review.md` when it exists
- `references/visual-priors.md` when the user gives preferred schools, labs, or named presenters

While distilling references:

- Learn the **title chain**, not just colors and layout.
- Prefer 3-5 high-quality reference decks over a large mixed corpus.
- Copy stable structural patterns, not topic-specific wording.
- Reject decks with repeated agenda jumps, overlong background sections, or conclusions that do not answer the opening question.
- Separate `logic references` from `appearance references`. Do not inherit the outline of a deck just because its visual treatment is strong.

### 3. Build the narrative backbone before designing slides

Force every deck into a visible reasoning chain:

`topic -> motivation -> gap -> scientific question -> method -> evidence -> conclusion -> boundary/future`

Require the user-facing slide titles to carry that chain. If someone reads only the slide titles, they should still recover the talk's logic.

Use these defaults unless the user specifies otherwise:

- Conference research talk: 10-18 slides.
- Background + related work: usually 2-4 slides total.
- Methods: 25-35% of the deck.
- Results + analysis: at least as much space as methods.
- Conclusion: 1 slide, occasionally 2 if limitations/future work matter.

Do not start layout work until the outline passes the logic checks in `references/logic-rules.md`.

### 4. Write slide sections with explicit jobs

Use this section-level contract:

- `Title slide`: State the topic cleanly; keep author/unit/date secondary.
- `Opening`: Explain why the problem matters now, not the full field history.
- `Gap slide`: End background by naming what existing work cannot do.
- `Question or hypothesis slide`: Convert the gap into a crisp scientific target.
- `Method overview slide`: Show the full pipeline before module details.
- `Method detail slides`: For each module, state input, operation, output, and why it is needed.
- `Data / study area slide`: Include only what the audience needs to trust the experiment.
- `Result slides`: Tie each result to one question, claim, or method component.
- `Interpretation / ablation slide`: Explain why the result happened, not only that it happened.
- `Conclusion slide`: Restate the question, contribution, strongest evidence, and scope boundary.

### 5. Enforce logic checks

Before calling the `PowerPoint` skill, check all of the following:

- Can the title chain stand alone as a mini-abstract?
- Does the background end with a specific unresolved problem?
- Does each method block answer a visible sub-problem?
- Does each major result map back to a method or research question?
- Does the conclusion cite evidence instead of repeating slogans?
- Is the deck free of repeated full-agenda slides unless the talk is very long?
- Is there enough room for results, instead of spending most pages on background or method setup?

If any answer is "no", fix the outline first.

### 6. Hand off for PPT production

Once the narrative backbone is stable, use the `PowerPoint` skill to generate or edit the final deck.

When handing off:

- Keep all slide text editable.
- Keep charts native and data-backed.
- Preserve logic-first ordering even if a reference deck looks more decorative.
- Prefer one idea per slide unless the user explicitly wants dense review slides.

## Reference Map

- Read `references/logic-rules.md` for the canonical academic talk structure.
- Read `references/anti-patterns.md` for patterns to block during drafting and review.
- Read `references/chengdu-review.md` when you need concrete examples from the Chengdu 2025 corpus.
- Read `references/visual-priors.md` when the user names presenters or schools whose visual style should influence the deck.

## Output Expectations

When this skill is used, produce one of these artifacts before final deck rendering:

- a slide outline with one-line purpose per slide,
- a rewritten logic skeleton for an existing deck, or
- a reference-distillation summary with "learn / avoid" findings.

Do not jump straight from raw source material to slide styling without first producing one of those logic artifacts.
