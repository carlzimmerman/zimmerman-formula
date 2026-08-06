# 07 — WRITING RULES (ledger entries and commit messages)

The corpus is a **record**, not an argument. Someone reading it in a year must be able to tell what was
established, what was assumed, and what was withdrawn. Write for that reader.

## Banned words and phrases

| never write | write instead |
|---|---|
| derived (of a₀ or κ) | fitted; or "reachable at r = …, with r free" |
| emerges from | is set equal to; is imposed as |
| zero / no free parameters | "N free parameters: …" (list them) |
| proves | establishes, for \<class\>; is consistent with |
| theorem (from N examples) | "of the N tested" |
| cannot be made to / no X can | "not within \<class\>"; "excluded for \<the cases checked\>" |
| definitively, conclusively | (delete) |
| the theory is closed / no open doors | (banned outright — R7) |
| remarkable, striking, beautiful | (delete — describe the number) |
| perfect agreement, near-perfect | "agrees to X%" — and say whether that is a fit or a prediction |

## A fit is not a prediction

If the coefficient was chosen to match data, then matching that data to 0.04% is **the quality of the fit**, not
evidence for the theory. Always write which it is. This is the single most common way this project has
overstated itself.

## Ledger entry format

Append to `LEDGER.md`. Keep it under 25 lines. Exactly this shape:

```
## <date> — DOOR <n>: <title>            STATUS: CLOSED | CONFIRMED | PARKED | SPLIT | NEEDS_CARL
SETTLED IF: <what you wrote at step 3>
REFUTED IF: <what you wrote at step 3>
SCRIPT: real_research/reviews/<name>_2026.py  (<n>/<m> checks, exit <code>)
RESULT: <2-4 lines. The number first, then what it means.>
FREE PARAMETERS: before <n>, after <m>. <If not lower: "REPARAMETRISATION, not derivation.">
VERIFY: opposite-position argument = <1 line>. Second route = <1 line, and the number it gave>.
        moved-the-number = <what moved, by how much, vs predicted>.
        refinement = <shift under 4x>.
AGAINST INTEREST: <what this found that cuts against the framework. "searched, none found" only if you did.>
SCOPE: within <class>, <result>. Outside it, <named open thing> remains open.
NEXT: <the single sharpest follow-up, or "none — this door is done">
```

## Commit message format

First line: the verdict, ≤ 100 chars, with the check count. Then a blank line, then the body.

Good first lines from this corpus:
```
I REFUTE MY OWN RIGIDITY THEOREM (14/14): q = 2/r with r FREE, and an explicit f delivers q = 1/Z EXACTLY
THE RESPONSE LANE IS COMPUTED (8/8): it VALIDATES Deser-Levin exactly and is a NULL for the coefficient
11.577620 IS RIGHT, and my "2Z carries sqrt(pi) with no mechanism" objection is WITHDRAWN (8/8)
```
Note what those have in common: **the verdict, the check count, and — where applicable — the withdrawal, in the
first line.** Not "update script" or "add analysis".

Body must contain:
1. what was asked and what the number is,
2. **AGAINST INTEREST:** section — always,
3. **WITHDRAWN:** section if anything previously claimed is now retracted, naming it explicitly,
4. **SCOPE:** the class,
5. the last line: `kappa = 1/2 remains FITTED, NOT DERIVED.`

End with:
```
Co-Authored-By: <your model name> <noreply@anthropic.com>
```

## Withdrawals are first-class

If you contradict something you or the corpus said earlier, **lead with it**. Do not bury it, do not soften it,
do not write "clarification" when you mean "this was wrong". Say which claim, why it was wrong, and what
replaces it. Six claims have been withdrawn in this project in two days and the corpus is stronger for each one
being explicit. A withdrawal is a result.

## Tone

Plain. No plating. Do not describe your own work as rigorous, careful, or thorough — demonstrate it and let the
numbers say so. No exclamation marks. No emoji in scripts or commits.
