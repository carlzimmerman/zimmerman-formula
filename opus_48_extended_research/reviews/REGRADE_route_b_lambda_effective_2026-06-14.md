# HOSTILE REGRADE — Route B (lambda_effective). VERDICT: CONFIRMED NULL (closed falsifier holds) (2026-06-14)

**Regrade grade: CONFIRMED CLOSED FALSIFIER.** Independent re-derivation reproduces every load-bearing step; no tuned
input smuggled; the sign analysis is correct; the closed-falsifier conclusion is airtight (no missed route). One
non-fatal arithmetic slip found in the *prose* (the SdS magnitude is overstated by ~1000x — and correcting it makes the
null STRONGER, not weaker). Code: `/tmp/regrade_routeB2.py` (independent sympy Christoffel + perturbative cubic).

## What I re-derived from scratch (not trusting route_b code)
- **(a) SdS cosmological-horizon shift — REAL, zero knobs.** Perturbative solve of `(Λ/3)r³ − r + μ = 0` about
  `r_c0 = √(3/Λ)` gives `δr_c = −μ/2` (leading order) and `Λ_eff/Λ = 1 + μ√(Λ/3)`, μ=2GM/c². Positive (RIGHT SIGN).
  Reproduced exactly.
- **(b) SdS Ricci scalar — REAL, M-independent.** My own from-scratch Christoffel→Ricci computation gives **R = 4Λ**
  with M entirely absent from R. The category claim (Λ is the w=−1 vacuum trace; matter adds only a Ricci-flat
  Weyl/tidal piece) is confirmed symbolically, not asserted.
- **(c) Magnitudes.** Trace backreaction `Λ_eff/Λ = 1+ρ/(4ρ_DE)`: disk boost **530x** ≫ cluster-core **19x** — wrong
  sign (disk is ~10³× denser) and SPARC-fatal. CKN `a0 ∝ 1/L`: cluster window needs `L_local ≈ 210–4100 Mpc`, Gpc-scale.
  All reproduced.

## The one error I found (non-fatal; strengthens the null)
The verdict prose says the 1e15 M⊙ SdS boost is **1.00001x** (`2GM/c² ≈ 0.096 Mpc`, `Λ_eff/Λ−1 ≈ 2.2×10⁻⁵`). The
correct numbers: `2GM/c² = 9.57×10⁻⁵ Mpc` (the prose's 0.096 Mpc is ~1000x too big — a units slip) and
`Λ_eff/Λ−1 = r_g/r_c0 = 1.8×10⁻⁸` (boost 1.00000002x). The route's own *code* prints `1.000000e+00`, so the slip is
prose-only. **Direction of the error: the true SdS effect is ~1000x SMALLER than the verdict claimed** → the route is
even more inert than stated. The null is unaffected and reinforced.

## (e) The skeptic's job — did the route miss a route? NO.
I stress-tested the one place a larger effect could hide: alternative SdS *local-temperature* readings that the
dS-Unruh foundation could plausibly select instead of the cosmological-horizon Λ_eff:
- **Gibbons-Hawking surface gravity of the cosmological horizon** `T_c ∝ |f′(r_c)|`: numerically `T_c/T_vac − 1 ~ 10⁻⁸`
  for a 1e15 cluster — same cosmological-horizon scaling, dead.
- **Tolman blueshift of the local floor** `T_loc = T_∞/√(f(r))` at a cluster core: `a0_loc/a0 = 1.00012` (boost−1
  ~1.2×10⁻⁴) — the LARGEST of all readings, and it is exactly the banked **Route A** (`DSUNRUH_TOLMAN_FLOOR`) null.
- **CKN IR cutoff**: web-confirmed `ρ_Λ ∝ M_Pl²/L²` ⇒ `a0 ∝ 1/L`. The two principled cutoffs (local Hubble horizon →
  banked ELL_DESITTER; system size → wrong sign + 10⁴–10⁵x absurd) both fail. No principled cutoff lands in-window.

Every reading is governed by (gravitational scale)/(cosmological or c² scale) = 10⁻⁸ to 10⁻⁴. There is no leak to a
large in-window boost. The closed falsifier is airtight.

## Regrade verdict (both ways, held to the 10x bar for any "works" claim)
**CONFIRMED NULL — Route B is a closed falsifier, exactly as banked.** The derivation is genuine (not tuned), the
sign analysis is correct, the arithmetic conclusion is right (one prose slip that makes the SdS route MORE dead), and
the steelman is complete (the three additional SdS/CKN readings I tested as a hostile check all collapse to ≤10⁻⁴, the
largest being the already-banked Route A Tolman effect). The foundation's a0↔Λ is a **vacuum** identity (R=4Λ in the
vacuum around any mass); a local matter overdensity does not move the vacuum Λ that a0 reads. The one real,
right-signed effect (SdS cosmological-horizon back-reaction) is `r_g/r_c0 ~ 10⁻⁸` — cosmologically inert.

No manufactured cure (the SdS right-sign near-miss is, if anything, reported ~1000x too GENEROUSLY in the prose; the
true effect is smaller). No high-priest dismissal (the SdS shift and the CKN literature are engaged on the merits and
credited where real). Quarantine held: a0/Z never asserted derived; every candidate flagged derived-vs-tuned.

*Sources: independent sympy re-derivation `/tmp/regrade_routeB2.py`; CKN/HDE `ρ_Λ∝M_Pl²/L²` (arXiv:2501.18144);
banked companion nulls ELL_DESITTER_UNRUH_HORIZON_VERDICT, DSUNRUH_TOLMAN_FLOOR_A0LOCAL_VERDICT (Route A),
DENSITY_A0_RDE_CROSSOVER, DENSITY_A0_ELL_1MPC; SPARC environment anchor d log a0/d log(1+δ)=+0.052±0.043 (10.5σ from
the +0.5 the trace route predicts); spine THE_A0_LAMBDA_BRIDGE.md.*
