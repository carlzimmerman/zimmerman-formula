# MG-BASELINE: is "MG = 0 infall-phase spread" airtight for the CLUSTER-MEMBER EFE channel?

**Lane:** MG-baseline (the exact-zero side of the cluster-member infall-phase discriminator).
**Script:** `mg_efe_zero.py` (exit 0, numpy+sympy, both footings). **Output:** `mg_efe_zero.out`.
**Date:** 2026-07-17. **Builds on / reuses:** `prep_2026/sigma_spread/mg_zero.py` (the symbolic
MG-class theorem), `GAP_STATEMENT.md` (frozen estimator E2/E5/E6), `POWER_cluster_efe_channel.md`
(MI band + power). **Companion lanes:** MI-amplitude + power (banked); D3 sign-flip pre-registration
(`reviews/residual_doors_2026_07/`, DOI 10.5281/zenodo.21179352).

---

## The claim under test (this channel specifically)

A galaxy falling into a cluster feels the cluster's external field `g_ext`. Both MI and MG have an
EFE that suppresses the member's internal MOND boost. They differ in **time-dependence**:

- **MG (QUMOND / AeST / AQUAL / f(R)):** the EFE is **instantaneous** — internal dynamics are set by
  the **current** `g_ext` (a function of cluster-centric position only). Two members at the same
  current position have **identical** internal boost.
- **MI (this framework + any history-dependent inertia):** inertia depends on the member's
  **acceleration history** via the non-local kernel `K(Box_u)`, so the boost depends on **infall
  phase** `y = omega_ex/omega_in` (Milgrom 2022, PRD 106 064060). At fixed current `g_ext`, MI
  predicts a **spread** across infall phase; MG predicts **zero**.

Banked MI band (both footings, kernel-hostage): **6.2–11.8%** (canonical `a0=9.36e-11`),
**7.5–14.1%** (alt `1.13e-10`). This lane asks the honest converse question: **is the MG=0 baseline
really zero *for what we can observe*, or does a real cluster manufacture a false MG spread that
mimics the MI band?**

## Result 1 — At fixed TRUE 3D external field, MG=0 is airtight (theorem, re-verified)

The instantaneous-EFE vs history-EFE distinction is exact. MG's member acceleration is the sourced
field evaluated at the member's position, `a = g(x(t))`; the field carries **no** `d/dt(worldline)`
label (verified symbolically, `[A]`). So:

- **(a) time-varying potential:** going non-adiabatic replaces the fixed position by the worldline
  `x(t)` but attaches no velocity/history label to `g`. A settled member and a deep plunger that
  reach the **same current radius** by different histories have **identical** MG boost (verified
  numerically, both footings). MG is **memoryless**; the infall history drops out exactly.
- **(b) retardation / finite crossing:** the field lag is `~ v/c ~ 3.5e-3` (crossing `r/c ~ 2e14 s`
  vs dynamical `r/sigma ~ 6e16 s`). Retardation lives in the **source** past light-cone, felt
  identically by every member at `(x,t)` — it shifts the **mean** field (`~1e-3` in `d`) but adds
  **zero** infall-phase family spread. (Contrast MI: `K(Box_u)` retards along the **tracer's own**
  worldline → per-orbit.)

**So the exact-0 is a genuine theorem for the sourced-field channel at fixed true `g_ext`.** Neither
the real potential's time-variation nor retardation leaks history into MG. This reproduces and
sharpens the banked `mg_zero.py` C4/C6 result for this specific channel.

## Result 2 — But the OBSERVED spread in an MG universe is NOT zero (the two mimics, quantified)

We do not observe true 3D position — we observe **projected radius `R_proj` + LOS velocity**. Two
observational channels manufacture a false MG infall-phase spread. Quantified by Monte Carlo (240k
synthetic members, NFW cluster `M200=1e15`, `R200=2 Mpc`; radial-orbit plungers vs NFW-settled;
random isotropic projection):

### (c) Projection mimic — the main threat

At fixed **projected** radius, radial plungers sit at systematically **different true 3D radius**
than settled members (a plunger seen down the LOS has `R_proj << r_true`). Different true `r` →
different true `g_ext` → different MG boost `d_MG(r_true)`. Because the infall-phase proxy correlates
with orbit class, MG's real **radial** `g_ext` trend **aliases into the phase direction** = a false
spread.

| binning regime | canonical mimic | alt mimic |
|---|---|---|
| by TRUE 3D `r` (perfect deprojection) | **0.09%** (theorem ~0) | 0.11% |
| by `R_proj` (no deprojection, worst) | **2.25%** | 2.35% |
| by class-blind statistically-deprojected `r` | **2.19%** | 2.30% |

**Raw projection mimic ≈ 2.2–2.4%, i.e. ~17–19% of the MI band top, ~31–35% of the MI band floor.**

**Honest sting (load-bearing):** class-blind statistical deprojection barely helps (2.25% → 2.19%).
The alias is driven by a **class-dependent LOS-depth residual** (plungers and settled members have
different projection statistics), not a mean bias — so a population-mean deprojection removes the
mean and leaves the mimic almost intact. **Killing the projection mimic requires a phase-space
membership/deprojection that is orbit-class-aware (caustic + PPS), not a scalar radial correction.**

### (d) Interloper / backsplash mimic

Interlopers (foreground/background non-members) feel a **weak** field → **high** isolated MOND boost
(large `d`). If mis-tagged "infalling" they inject a class-correlated offset:

| interloper fraction (all mis-tagged infalling, uncut) | canonical false spread | alt |
|---|---|---|
| 5% | 0.25% (2% of MI top) | 0.28% |
| 15% | 1.28% (11% of MI top) | 1.42% |
| 30% | 4.43% (38% of MI top) | 4.67% |

Uncut at 30% contamination this **reaches into the MI band**. The frozen estimator's **caustic
membership + Dressler–Shectman cut** (banked: fake-3σ rate 28% → 0.08% with the cut) removes
DS-coherent infalling groups and clips caustic-outlier interlopers, leaving a residual contamination
`~1–3%`, i.e. a `~0.25–0.5%` residual false spread.

## Result 3 — Verdict (honest both ways)

- **MG=0 is a THEOREM for the sourced-field channel at fixed TRUE `g_ext`** — memoryless, survives a
  time-varying potential and retardation, any `a0`, both footings. That much is airtight.
- **MG=0 is NOT airtight in projection.** The **raw** projection mimic (~2.2%) plus **uncut**
  interlopers can reach a substantial fraction of — even into — the MI 6–13% band. So a "detection"
  that bins by projected radius and skips membership cuts would measure **projection + interlopers,
  not modified inertia.**
- **The frozen mitigations are load-bearing, not polish.** `≤0.3 dex deprojected a_ext binning + DS
  cut + caustic membership` (GAP_STATEMENT E2/E5) are what turn the airtight-at-true-`r` theorem into
  an airtight-in-observation baseline. And **statistical deprojection must be orbit-class-aware** —
  a scalar radial correction leaves the mimic nearly intact (Result 2c). The residual MG floor after
  the frozen, class-aware cuts is the real number the MI band must clear; it is **well below** the MI
  band only if the cuts are applied as specified.
- **Not footing-hostage:** the mimic and the MI band scale together; the alt footing shifts both up
  ~20%, flipping nothing.

## Scope & credit (do not overclaim)

This is an **MI-CLASS (any history-dependent inertia) vs MG** test — the spread discriminates MI-class
from MG (`MG=0` exactly at fixed true field), but **NOT this framework vs Milgrom's linear no-EFE
model** (arXiv:2503.07106, which also produces a spread). `a0`'s value and the sign `s=-1` remain
**postulates**; the 6–13% magnitude is **kernel-hostage**. `MG=0` is a theorem only where labelled
(fixed true `g_ext`); in projection it is a **mitigation-dependent baseline**.

Credit: Milgrom 1983 (MOND) / 1999 PLA 253:273 (ν-kernel wellhead) / 2022 PRD 106 064060 (MOND as
modified inertia; two-frequency EFE) / 2025 arXiv:2503.07106 (linear MI spread → MI-class-generic).
Cluster kinematics & phase-space membership: Rhee+2017 (infall-phase PPS diagram), Oman+2013, HeCS
caustic membership, SDSS/MaNGA dispersions. Framework-distinctive content = the `cH_Lambda/Z`
coefficient + the MI covariant completion (worldline `K(Box_u)`).
