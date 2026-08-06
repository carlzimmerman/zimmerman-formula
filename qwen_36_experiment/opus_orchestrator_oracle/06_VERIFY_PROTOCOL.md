# 06 — VERIFY PROTOCOL (run after the script passes, before writing anything down)

Your script exiting 0 is **not** evidence. It means the checks you thought to write happened to pass. This
protocol is where the errors get caught. Every published claim this project has had to withdraw would have been
caught by step 2 or step 4.

Do all six. Write the answers into the ledger entry.

## Step 1 — Adopt the opposite position

Write one paragraph arguing that your conclusion is **wrong**. Not a caveat — an actual argument. If you cannot
construct one, you do not understand the result well enough to report it. Then answer your own argument, or
concede it.

## Step 2 — Hunt your own tautologies

Go through every `check(...)` and ask: **name an input that makes this print FAIL.** If you cannot, the check is
worthless — delete it and either write a real one or drop the claim it supported.

Specific patterns to look for, all of which have shipped here:
- squaring something you defined as a square root, then verifying it equals the original,
- differentiating an expression with respect to a variable it does not contain,
- asserting `x != 0` for an `x` you just wrote as a sum of positive symbols,
- verifying an algebraic identity that follows from your own definitions rather than from the physics,
- a check whose condition is `A and (B or True)`.

## Step 3 — Re-derive one load-bearing number by a different route

Pick the single number the conclusion rests on. Get it again a different way — symbolically if you did it
numerically, by hand-substitution if you did it symbolically, with a different library if neither. **If the two
routes agree only because they share a subroutine, that is not a second route.** (This project once claimed a
cross-validation between two "independent" routes that were both the same kinematic factor (c/v)² with different
O(1) dressing.)

## Step 4 — Prove by moving the number

Already required in the script (S2), but confirm the two directions are *genuinely* one of each:
- an input that **should** change the answer, and it moves by the **predicted** factor — not merely "it moved",
- an input that should **not** change the answer, and it does not.

## Step 5 — Check against `04_FRAMEWORK_FACTS.md`

Does your result contradict anything listed there? If yes:
1. re-run that fact's script and paste its actual output,
2. if it still contradicts, **stop** and write `NEEDS_CARL` in the ledger. Do not silently pick a side.
   A genuine contradiction between two script-backed results is the most valuable thing you can find — it means
   one of them is wrong and the corpus is carrying an error.

## Step 6 — Scope the claim

Write the conclusion in this exact shape:

> Within **\<the class you actually covered\>**, \<the result\>, established by \<the number\>.
> Outside that class, \<at least one specific thing you did not cover\> remains open.

If you cannot name the class, you have not established a result — you have an observation about the cases you
ran. Say "of the N tested".

---

## The four failure modes, named

Learn to recognise these in your own output:

| mode | what it looks like | catch |
|---|---|---|
| **over-closing** | "no kernel can…", "cannot be made to…", "forced" | step 1, step 6 |
| **five-examples-as-theorem** | N candidates all agree ⇒ stated as general | step 6, R8 |
| **relocated fit** | a new construction with a new free number that reproduces κ | S5 count, step 1 |
| **rounding as physics** | a check reading a difference of nearly-equal large numbers | step 3, H2 |

Over-closing is this project's dominant error: **six withdrawals in two days, every one in the direction of
claiming a door was shut.** Weight your suspicion accordingly. If your result closes something, spend twice as
long on step 1.
