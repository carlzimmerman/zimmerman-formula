# M02 — Theorem 4's escape: what kernel has μ ≤ 1 saturated to 6.75e-05?
COST: S | KILLS FAST: YES | script: `mi_theorem4_escape_2026.py`

## The task
Theorem 4 (`mi_r_one_parameter_nogo_paper_2026.py`, 41/41) proved every member of the class carries a
**constant residual Δ**, that μ ≤ 1 **is** Δ ≥ 0, and that on the balance member Δ = a₀/2 exactly — so the
ephemeris bounds the whole class and **no r does both jobs** (a₀ = 2Δ identically). The one escape it
named: μ ≤ 1 must be **saturated to 6.75e-05**, which forces a kernel that is NOT √(1+1/y).

Find that kernel and see whether it survives.

## Do
1. Solve for the ψ that saturates μ ≤ 1 to 6.75e-05 while reaching r = 2Z. Exhibit it in closed form if
   possible, numerically otherwise.
2. Extract its ν(y) and compute max |dex| distance from √(1+1/y) and from McGaugh 2008 eq 11a, over
   y ∈ [1e-4, 1e4].
3. **The decider:** is that distance inside SPARC's 0.034 dex RAR scatter? If yes, the escape is alive and
   invisible to rotation curves. If no, SPARC already excludes it — and the class is closed for real.
4. Also check the corpus's own result that in the exactly-solved family ψ = (1+x/δ)^(-2), Δ = 0 forces
   δ ≥ 1/2 hence **r ≤ 3** against 2Z = 11.578. Does the saturating kernel evade that or confirm it?

## Settles if / refuted if
SETTLED (alive): the saturating kernel's shape sits inside 0.034 dex ⇒ the class survives the ephemeris via
a kernel SPARC cannot see. Then M01's α-ledger becomes the test.
CLOSED: it sits outside ⇒ SPARC excludes the escape and Theorem 4's bound applies to the class with no exit.

## Known walls
The RAR shape is **exactly blind to the coefficient** (Theorem 3 corollary: 67× in a₀ ⇒ 1.9e-16 dex). So
shape and coefficient are independent axes — a shape measurement tests the ESCAPE, never the coefficient.
