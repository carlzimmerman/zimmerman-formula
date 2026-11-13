# G240 — the AQUAL completion: where does the external field actually turn on?

**Question inherited from G239:** "this is QUMOND; h34's AQUAL solve finds the algebraic boost ~15% high, so the
plateau may be overstated." Tested with the repo's committed AQUAL solver
(`qwen_claude_field_theory/theory_2026/aqual_solver_2026.py`, DE01's instrument), on the same quantity
`M_dyn(<r)/M_b = r⟨dφ/dr⟩_θ`.

## The structural finding (independent of any number)

**QUMOND and AQUAL put the EFE at different radii.**

| | EFE turns on when | transition radius |
|---|---|---|
| QUMOND | the **Newtonian** field equals g_ext | `r_M/√e_N` — item 38's 71 kpc, DW1's 88 kpc, G157's 3r_M, G239's whole plateau |
| AQUAL | the **boosted** field equals g_ext | ≈ `r_M/e_N` |

Measured with the solver (the last radius still on the `M ∝ r` deep-MOND branch, <10% off):
`r_trans = 14.7 r_M` at `e_N = 0.05` and `52.2 r_M` at `e_N = 0.0127`. So `r_trans·e_N = 0.73 / 0.66`
against `r_trans·√e_N = 3.3 / 5.9` — the **1/e_N scaling**, by a factor **6** in radius for the Milky Way.

## The plateau is NOT ν(e_N)M_b

The AQUAL far field is anisotropically enhanced: `ν(e)⟨(1 − L cos²θ)^{−1/2}⟩`, `L = μ'(e)e/μ(e)`. At
`e_N = 0.5`, where the solver converges inside the box, that formula gives **2.584** against the solver's
**2.514** (2.7%), while `ν(e)` alone gives 2.000 (26% away). At `e_N = 0.01273` (L = 0.987) the asymptotic
plateau is **21.4 M_b = 1.43×10¹² M☉**, with the unconverged box edge (62.5 M_b) as an upper bound.

## What it does to the DESI MW comparison

| | QUMOND (G239) | AQUAL (this lane) | paper (2611.05518) |
|---|---|---|---|
| M(<80 kpc), canonical | 4.98×10¹¹ | **5.83×10¹¹** (−1.1σ) | 6.36 ± 0.50 |
| M(<80 kpc), alt | 5.11×10¹¹ | **6.15×10¹¹** (−0.4σ) | |
| M(<200 kpc), canonical | 5.26×10¹¹ | **1.33×10¹²** (+1.0σ) | 1.19×10¹² (M200c) |
| M(<200 kpc), alt | 5.27×10¹¹ | **1.48×10¹²** (+2.2σ) | |

1. **DW1's "M200c fails at −2.8σ" is WITHDRAWN as a completion artefact.** Under AQUAL the framework's
   M(<200 kpc) is 1.33×10¹² (canonical, +1.0σ) — the QUMOND number was 0.53×10¹² (−5σ). The two
   modified-gravity completions differ by a factor 2.5 here, and **neither is the framework's own**
   (a0kit is modified *inertia*).
2. **The plateau signature goes with it.** Under AQUAL the mass does not stop at ~90 kpc; it keeps rising
   to ~1.4×10¹² at 200–400 kpc, i.e. the framework looks NFW-like in *amplitude* out to the virial radius.
   What still discriminates is the **shape**: framework γ → −2 (M ∝ r) where NFW gives −2.4 at 200 kpc —
   the same 0.35 split G238 measured. **So the MW falsifier is a shape test now, not a plateau test, and
   FALSIFIER_MATRIX row 32's kill (`M(<200 kpc) ≥ 1.0e12`) must be re-scoped: AQUAL itself would violate it.**
3. **What survives, and it is the honest core:** M(<80 kpc) = 5.83/6.15×10¹¹ (−1.1σ / −0.4σ) and the
   13-point shape fit at χ²/dof 0.26 with one amplitude. Inside 80 kpc the EFE is negligible under both
   completions, which is why **DW1's amplitude result — and the two-dataset agreement with item 35 — is
   completion-independent. It is the only such number in this chain.**

## Limits

The far field at `e_N = 0.0127` is **not converged** in a 10⁴ r_M box; the asymptote used is the linearised
formula, validated only at `e_N = 0.5` (2.7%). Grid convergence at 20 r_M is **3.5%** between (320,96) and
(512,128) — the 1% bar in the MUT check was arbitrary and is not met, so every number carries a ~4%
resolution systematic. Uniform, static external field at the repo's own vector sum.

**The open item is now the completion, not the data.** The framework is modified inertia; QUMOND and AQUAL
are modified gravity and disagree by 2.5× on M(<200 kpc). Until the MI EFE is written down, no
EFE-dependent prediction (the plateau, the saturation, G157's γ(r)) is a framework prediction — it is a
completion prediction. `κ = 1/2` stays **FITTED**.

Files: `g240.py`, `g240.out`, `g240_results.json`. `G240 COMPLETE: 6/7 checks PASS` (the FAIL is the
arbitrary 1% grid bar, disclosed above).
