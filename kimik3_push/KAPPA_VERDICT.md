# The κ = ½ verdict — what is derived, what is certified, what is honestly open

**kimik3_push, 2026-09-13.** The status of the one fitted number, stated with no theatre.

## The hard floor (the framework's own theorem)

κ = ½ is a **proven zero mode of the candidate action** (`kappa_closure/k01`): the MOND primitive
enters the field equations only through `J′`, so **no action of this class derives it.** κ = ½ is an
**empirical boundary condition**, measured (0.551 ± 0.043 distance-free / 0.465 ± 0.076 BTFR), not a
derivable quantity. Any claim to "derive κ = ½" must either (a) go outside this action class, or
(b) show the zero mode is lifted by a mechanism the k01 theorem did not cover. Neither is done.

## The candidate that is NOT a derivation (K010 + TransverseCount.lean)

The photocount reading (L237) says the interpolating function `μ_n(Y) = 1-(1+Y)^{-n}` is a mode count,
and the data select `n = 2`. My contribution:

- **Certified (Lean, `TransverseCount.lean`, 8 theorems, exit 0, 0 sorry, clean axioms):** the spatial
  projector `q = 1 − n nᵀ` is idempotent with kernel `span{n}`; the orthogonal complement of a line in
  a d-dimensional space has dimension **d − 1**; specialised to d = 3 the transverse-mode count is
  **exactly 2**. This is the linear algebra of the count.
- **NOT certified, and NOT shown:** that the vacuum actually **occupies** those 2 transverse modes with
  the **linear (equipartition) occupancy** the photocount reading requires. L238 proved the occupancy
  is linear (not Boltzmann), that the reading is pinned to d = 3, and that **four candidate counts all
  give 2 in d = 3** (transverse directions, graviton polarisations, screen dimensions, the two gradient
  branches) — so the count "2" is over-determined and **nothing selects which "2" it is**, and nothing
  shows any of them is *occupied*.

**Verdict: the dimension count "2" is real and certified; the leap from "2 transverse modes exist" to
"the vacuum occupies 2 modes linearly, hence κ = 1/slope = ½" is a PHYSICAL assumption, not a theorem.
κ = ½ is therefore NOT derived. It is a certified-consistent candidate whose load-bearing occupation
step is an open physics problem, on top of the k01 zero-mode theorem that already forbids a derivation
within this action class.**

## What would actually close it (the honest remaining problem)

Show, **from the action's own perturbation dynamics** (not the photocount analogy), that:
1. the two transverse perturbation modes of the MOND scalar (the `W_Y` pair, L192/L193) are the
   *only* gapless/horizon-coupled response channels (the longitudinal `W_Y + 2YW_{YY}` is lifted), AND
2. they are populated with **mean occupancy exactly linear in `Y = g/s`** (equipartition), not
   exponentially (Boltzmann/Unruh — which L238 ruled out by 41 orders of magnitude).

If both hold, `n = 2` and the linear occupancy give `μ = 1-(1+Y)^{-2}`, slope 2, and κ = 1/slope = ½
**follows** — and the theory would have zero fitted numbers. If either fails, κ = ½ stays empirical.
**This is a concrete, attackable calculation and it is the single most valuable open problem in the
programme.** It is not done, and this document does not pretend it is.
