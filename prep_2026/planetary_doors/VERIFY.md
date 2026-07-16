# VERIFY — adversarial verification of the Lane-K planetary kernel calc

**Date:** 2026-07-16. **Script:** `vfy_kernel_planets.py` (this dir; **exit 0, 20/20 PASS**;
`vfy_kernel_planets.out`). It re-derives, with **no import from `laneK_kernel_planets.py`**, the two
claims the tasking singled out — the a₀/2 arithmetic and the "DC-into-GM absorption" question — plus
independent re-checks of the cut identities, the drift factor, and the constitutive-vs-operator fork.
Both footings.

---

## What was checked, and what it found

### V1 — the a₀/2 landmine arithmetic (independent)
a₀/2 = **4.681e-11** (canon) / **5.650e-11** (alt) m/s². Per-planet exclusion vs the laneR
constant-radial-δg bounds (Fienga–Minazzoli 2024 Table 10): Mercury 1018×/1228×, **Mars 33 436×/40 357×**,
Saturn 6687×/8071×. **Reproduces the laneK table exactly.** PASS.

### V2 — is the constant sunward a₀/2 absorbable into GM? (the DC-absorption test the task named)
Two independent refutations of the "it just hides in a GM rescaling" hypothesis:
1. **GM-shift spread.** Absorbing a constant A=a₀/2 into GM_eff(r)=GM+A·r² requires a *fractional* shift
   A·r²/GM that would have to be r-independent for a genuine absorption. It is **not**: it runs from
   1.18e-9 (Mercury) to 7.25e-7 (Saturn), **spread 613× = (r_Sat/r_Merc)² exactly** (both footings). No
   single GM_eff absorbs a constant sunward acceleration across the planets.
2. **Observable precession.** A constant sunward A produces a **nonzero secular perihelion precession**
   (LRL-vector ODE): rate −1.09e-3 (A=1e-3) vs +3.8e-12 (A=0) code units, scaling **linearly** in A (2× at
   2e-3, <5%). A constant radial term is exactly the observable, apsidal-precessing "Pioneer" residual
   Blanchet–Novak 2011 ruled out — not a coordinate/GM artifact.

**Finding (decisive, honest):** the a₀/2 tail on the constitutive reading is a **genuine, non-absorbable
secular residual**. The task's alternative hypothesis — "the evasion is the standard DC-into-GM absorption
shared with any ν" — is **refuted**: there is no DC-into-GM absorption of a constant sunward a₀/2. So on
the reading that carries the galactic wins, Reading A is simply dead at planets, with **neither a kernel
suppression nor a DC-absorption escape**. PASS.

### V3 — cut boundary values (pure phase), independent sympy+numeric
K(−W²+i0) over W ∈ [0.6, 6×10⁵]: max deviation from (|K|²=1, Re=√(1−1/4W²), Im=1/2W) = **2.2×10⁻¹⁶**.
Confirms the S2 identities that failed only as a sympy-assumption artifact in the first laneK run. PASS.

### V4 — the secular-drift orbital-mechanics factor, independent ODE
Direct tangential drag f_t=ε·g_N, ε=1e-6, integrator-baseline subtracted: (measured−baseline)/predicted =
**0.9979** (<1%). With Im K=1/2W=a₀/(2cω) this gives d ln r/dt = a₀/c: canon 9.86e-12/yr (×246 vs
MESSENGER), alt 1.19e-11/yr (×297). PASS.

### V5 — the constitutive-vs-operator fork, independent
- **Constitutive first-moment closure reproduces the tail:** (ν−1)·g_bar at Saturn = 4.681e-11 (canon) /
  5.650e-11 (alt) = a₀/2 to ratio **1.0000** (<0.1%). The kernel, on z=+(a/a₀)², carries the a₀/2 tail.
- **Bound-orbit operator spectrum cannot feed z>0:** circular u_μ gives □_u eigenvalue −(γω)²<0 on the
  spatial part and 0 (DC) on the time part — no positive argument. PASS.

---

## Reconciliation with the fixes applied to `laneK_kernel_planets.py`

The first laneK run exited non-zero on five checks. Each was diagnosed as a **coding/numerical artifact,
not a physics failure**, and the physics is independently PASS-verified here (V3–V5) and in
`mi_fingerprint/rb2_frequency_dependence.out`:

| laneK check that had failed | root cause | fix | evidence it was an artifact |
|---|---|---|---|
| master identity 1−K=∫dμ/(\|t\|+z) | naive t-quad lost the slow region-B tail for z≳10⁵ (returned garbage) | u=√\|t\| substitution (analytic-stable) | err now 1e-15…1e-12 at all z; identity holds (V3 measure is the same one) |
| \|K\|²=1 on the cut | sympy could not assume 4W²−1>0 from W>0 alone | prove Kcut=(√(4W²−1)+i)/(2W) first (one simplify → 0), read Re/Im off it | `sp.simplify(Kcut−Krat)=0` exact; V3 numeric 2e-16; rb2 [2] PASS |
| Re K = √(1−1/4W²) | same sympy assumption gap | same | same |
| \|Im K\| = 1/(2W) | same | same | same |
| secular-rate ODE (ratio 0.005) | toy relaxator out of linear regime (S=0.25 → predicted d ln r/dt≈ω₀, wildly non-adiabatic; orbit saturates) | direct tangential drag, ε=1e-6, baseline-subtracted | ratio → 0.998 (ε=1e-6), 0.9994 (ε=3e-7): the formula holds in the regime it applies to |

**No physics number changed.** The S3–S7 tables and every load-bearing quantity (a₀/2 exclusions, reactive
residuals, drift a₀/c, Q₂, the gated window) are byte-identical to the banked run; only the five check
verdicts flipped from FAIL to PASS once the quadrature, the sympy assumptions, and the toy-ODE regime were
corrected.

## Residual honesty caveats (named, not glossed)
- The Ġ/G exclusion of Reading B's drift is a factor-few, not orders, of formal slack: the published Ġ/G
  bounds are fits of the *signal class* a secular ṙ produces, not a dedicated refit of this kernel. The
  ~250–500× headline is robust to that slack (it is orders); the exact σ is not.
- The Saturn/Mars "rdot proxy" anchors (2.3, 0.05 m/yr) are order-of-magnitude ranging-residual proxies,
  flagged as factor-few uncertain; the load-bearing drift exclusions rest on MESSENGER/LLR Ġ/G and the
  lunar tidal budget, which are published.
- The gated-Reading-C window rests on the SPEC's Lorentzian gate *form* and a *free* corner; nothing
  published pins the corner. The window is a conditional pass, not a derived one.
- Everything here discriminates BETWEEN the framework's doors. **No result prefers the framework over
  ΛCDM**, and none is claimed to.

**VERIFY RESULT: ALL PASS (exit 0).** The a₀/2 arithmetic and the (refuted) DC-into-GM absorption
hypothesis both survive independent adversarial re-derivation.
