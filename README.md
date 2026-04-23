# academic-ppt-maker

A Codex skill for distilling academic talk logic and generating strong academic slide decks.

This skill is designed for one specific problem: most academic PPTs fail because the **report logic** is weak, not because the colors are bad. The skill therefore focuses first on:

- title-chain design,
- background-to-gap narrowing,
- method-to-question alignment,
- result-to-claim closure,
- conclusion quality,
- reference distillation from strong academic decks.

It also supports a two-track reference strategy:

- `logic gold`: learn narrative structure from strong research-talk decks
- `appearance gold`: learn visual tone from preferred presenters, schools, or labs

## What It Does

Use this skill when you want Codex to:

- turn a paper, abstract, notes, or results into an academic PPT outline,
- learn from example PPT/PPTX files,
- review an existing academic deck and rewrite its logic,
- separate `good-looking slides` from `good academic storytelling`,
- combine strong logic with preferred visual style.

## Current Design Priorities

This version was distilled from a local corpus of conference slides, with special emphasis on:

- logic-first references such as the `Du Siqi` deck, the `accessible map research` deck, the `Cai Jiannan` deck, and the `Liu Baoju` deck
- appearance priors from Zhou Liang and selected decks from Peking University, Wuhan University, and Tsinghua-linked authors

The skill explicitly treats:

- `Zhou Liang` as a high-priority **visual** reference
- `Du Siqi / Cai Jiannan / Liu Baoju` style decks as stronger **logic** references

If logic and appearance conflict, logic wins.

## Repository Structure

```text
academic-ppt-maker/
|- SKILL.md
|- agents/
|  |- openai.yaml
|- references/
|  |- anti-patterns.md
|  |- chengdu-review.md
|  |- logic-rules.md
|  `- visual-priors.md
`- scripts/
   `- extract_pptx_logic.py
```

## Install

### Option 1: Clone directly into Codex skills

Clone this repository into your Codex skills directory and keep the folder name as `academic-ppt-maker`.

Typical locations:

- Windows: `C:\Users\<you>\.codex\skills\academic-ppt-maker`
- macOS/Linux: `~/.codex/skills/academic-ppt-maker`

### Option 2: Copy the skill folder

If you already cloned it elsewhere, copy the repository contents into a folder named `academic-ppt-maker` under your Codex skills directory.

## Usage

Example prompts:

```text
Use $academic-ppt-maker to turn my abstract into a 12-slide conference PPT outline.
```

```text
Use $academic-ppt-maker to learn from these 5 PPTX files, then design a new academic deck with the same visual tone but better report logic.
```

```text
Use $academic-ppt-maker to review my current PPT and rewrite the title chain, research question, method flow, and conclusion page.
```

```text
Use $academic-ppt-maker and prioritize Zhou Liang's appearance style, but keep the report logic closer to the Du Siqi deck.
```

## Workflow Summary

The skill works in three main modes:

1. `build-from-source`
2. `distill-from-references`
3. `review-existing-deck`

Core rule:

`topic -> motivation -> gap -> scientific question -> method -> evidence -> conclusion -> boundary/future`

It should produce one of these before final slide rendering:

- a slide outline,
- a rewritten logic skeleton,
- or a reference-distillation summary.

## Script

`scripts/extract_pptx_logic.py` extracts outline-level signals from `.pptx` files, including:

- slide titles,
- preview text,
- text density,
- picture density,
- logic-marker heuristics.

Example:

```bash
python scripts/extract_pptx_logic.py <root-folder> --limit 12 --json-output review.json --md-output review.md
```

## License

MIT. See [LICENSE](./LICENSE).
