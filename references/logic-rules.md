# Academic PPT Logic Rules

Use these rules to design or review the **report logic** of an academic talk.

## Core Principle

A strong academic PPT is not a pile of content blocks. It is a controlled answer to one visible question.

Every good deck should make the audience feel:

1. why the problem matters,
2. why current work is insufficient,
3. what exact question this talk answers,
4. how the method answers it,
5. what evidence proves the answer,
6. where the answer stops.

## Canonical Talk Arc

Default arc for empirical or methodological conference talks:

1. Title / speaker
2. Motivation
3. Background or related work
4. Research gap
5. Scientific question / hypothesis / task definition
6. Method overview
7. Method detail A
8. Method detail B
9. Data / study area / setup
10. Main result 1
11. Main result 2
12. Analysis / ablation / interpretation
13. Conclusion
14. Limitations / future work / thanks

Compress or expand, but preserve that order unless there is a strong topic-specific reason not to.

## Title-Chain Test

Read the slide titles in order. They should already tell the story.

Good title chains:

- progress from `background -> gap -> question -> method -> evidence -> conclusion`
- contain verbs or claims when possible
- allow the listener to predict why the next slide exists

Weak title chains:

- repeat generic labels like `研究背景`, `研究方法`, `实验结果` too many times without semantic advance
- jump from background directly to many method details before the question is explicit
- show multiple result slides before the audience knows what success means

## Section Rules

### Opening

- Spend as little time as needed to establish urgency.
- Prefer current tension, application need, or scientific bottleneck over broad textbook review.
- End the opening section with a narrowing move.

### Related Work

- Use related work to expose the gap, not to prove the speaker read many papers.
- Organize by limitations that matter to this talk.
- Stop once the audience understands what existing methods cannot do.

### Research Question

- State the question explicitly.
- If there are multiple questions, rank them and keep one primary question.
- Put hypotheses or task definitions in audience language, not only notation.

### Method

- Start with a full pipeline view.
- Make every method detail slide answer: `why is this component necessary?`
- Prefer `input -> transformation -> output -> benefit` over dense formula dumps.
- If a method block does not change the answer to the core question, cut it or move it to backup.

### Results

- Present results in the same order as the claims or method modules they validate.
- Label what each result proves.
- Pair comparison figures with a sentence-level takeaway.
- Use one slide for one evidentiary job whenever possible.

### Conclusion

- Answer the opening question directly.
- State the contribution in one sentence.
- Name the strongest evidence.
- State the scope boundary, limitation, or next step without diluting the main claim.

## Allocation Rules

For a standard 12-15 minute talk:

- Background + related work: 20-30%
- Method: 25-35%
- Results + interpretation: 30-40%
- Conclusion + future: 10-15%

If the deck spends half its pages before the method or half its pages on method internals with thin evidence, the logic is usually imbalanced.

## Question-Method-Result Closure

Create an explicit mapping table while drafting:

- Question Q1 -> Method M1/M2 -> Evidence R1/R2 -> Conclusion C1
- Question Q2 -> Method M3 -> Evidence R3 -> Conclusion C2

If a result cannot be mapped back to a question, it is probably decorative.
If a method cannot be mapped forward to a result, it is probably over-explained.
