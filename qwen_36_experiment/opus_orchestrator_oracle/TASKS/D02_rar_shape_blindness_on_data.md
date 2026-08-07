# D02 — Confirm on real data that the RAR shape is blind to a₀
COST: M | script: `mi_rar_blindness_data_2026.py` | PREREQ: D01

> ENGINEERING / DATA task. Import `TOOLS/mi_constants.py` — never retype a constant.
> `../02_HOUSE_RULES.md` and `../03_NUMERIC_HAZARDS.md` apply.

## The claim to test
Theorem 3's corollary (`mi_r_one_parameter_nogo_paper_2026.py`, 41/41) proved *analytically* that two members
of the class whose a₀ differ by **67×** have kernels agreeing to **1.9e-16 dex**. If true, real SPARC data
should be unable to distinguish them. Show it — or find where the analytic claim breaks on real data.

## Do
1. Take two class members with a₀ differing by 67× (Theorem 3 gives them in closed form).
2. Fit each to SPARC with Υ free per galaxy. Report Δχ² between them, and the best-fit a₀ each prefers.
3. **The prediction: Δχ² ≈ 0 and the fits are indistinguishable.** If instead one is clearly preferred, the
   analytic corollary has a loophole on real data — that would be a significant finding, so check your fit
   before believing it.
4. Then the useful by-product: how large a **shape** difference would SPARC detect at 3σ? That number sets
   what M02's escape kernel has to hide inside.

## Settles if / refuted if
CONFIRMS: Δχ² ≈ 0 ⇒ the corpus's "RAR is non-diagnostic of 9.36e-11" now has a data-side proof, not just an
analytic one. REFUTES: a real preference ⇒ investigate immediately.
