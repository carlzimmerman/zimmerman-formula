# ROUTE A — what does cosmology fix the cluster Helmholtz constant chi_out to? (2026-06-14)

*Opus 4.8. The question the cluster closing-calc left open: the AeST cluster scalar obeys an
inhomogeneous **Helmholtz** equation whose +mu^2 sign makes Phi(inf)->0 NON-selective, leaving a
free constant chi_out (Verwayen-Skordis-Zlosnik 2024's chi_hat_out). eta=2.15 is reachable by
sliding chi_out per cluster — a tune. ROUTE A asks: does the **cosmological AeST background**, matched
at the cluster edge, FIX chi_out universally? Companion code:
`cluster_chi_out_cosmological_matching.py`, `cluster_chi_out_rta_robustness.py`. Quarantine:
a0/Z never asserted derived; mu the free CMB-pinned constant (1/mu=1 Mpc).*

## VERDICT: **DEFICIT-BY-MAGNITUDE, TUNE-BY-PHASE** — cosmology fixes the chi_out *magnitude* small (it does NOT force 2.15), but the matching-radius *phase* is a hidden lever

The cosmological matching DOES fix chi_out to a single universal prescription (one formula, all
clusters): **chi_out = Phi_cosmo(r_ta) ~ -(1/6)Lambda c^2 r_ta^2**, magnitude **~ -(3 to 6)x10^10
(m/s)^2 = -0.03 to -0.06 v_c^2** at z~0.3. That magnitude is **3-10x too small** to FORCE the
eRASS1 boost (which needs chi_out ~ -2 to -3x10^11 = -0.2 to -0.3 v_c^2). So **by amplitude the
cosmological BC gives a deficit-to-mild eta, not 2.15** — the closing-calc deficit survives.

BUT the honest catch, found in the robustness sweep: because the operator is **oscillatory**
(Helmholtz), eta(R500) is a strongly **non-monotone** function of the *matching radius* r_ta/R500
(which sets the phase (mu r_ta)): eta = {0.38, 0.60, **2.05**, 1.50} at r_ta/R500 = {2, 3, **4**,
5.64}. A turnaround multiple r_ta/R500≈4 hits 2.05≈2.15 — but that multiple is a **convention**, not
forced by cosmology. So 2.15 is **accessible** at a defensible-looking matching radius, yet it rides
the phase, not the cosmologically-fixed amplitude. **That is the smuggle to flag: not a per-cluster
knob (the prescription is universal), but a per-CONVENTION knob (which r_ta you match at).**

## The derivation chain (all numbers from real python; z=0.3)

**STEP 1 — cosmological AeST background.** The shift-symmetric scalar has a Noether shift current
J^mu; its background charge Q0 ≡ J^0 sets BOTH the DE mimicry (rho_phi,bg ~ rho_DE = OL rho_crit,0 =
5.85e-27 kg/m^3, verified OL=0.685) AND the mass term mu^2 = 2 K2 Q0^2/(2-K_B) (Durakovic-Skordis
2.18). AeST fixes the combination via the CMB to 1/mu~1 Mpc (the only banked constraint). The
load-bearing background OUTPUT is the **cosmological scalar potential amplitude** = the depth of the
DE/de Sitter potential well the cluster perturbation must match. Cross-check: Lambda(a0)=1.090e-52
m^-2 from a0=c^2 sqrt(Lambda/32pi) AGREES with Lambda(OL)=1.091e-52 m^-2 from 3 OL H0^2/c^2 to 0.1%.

**STEP 2-3 — the matching condition.** The weak-field cluster Phi is measured RELATIVE to the
cosmological mean. At the cluster edge the perturbation must join the background scalar continuously,
so the surviving Helmholtz constant equals the background cosmological potential at the matching
radius: **chi_out = Phi_cosmo(r_ta)**. Two physically-equivalent estimators (both run, they bracket):
  (A) de Sitter/DE well   Phi_Lambda(r) = -(1/6) Lambda c^2 r^2  (the potential the scalar mimics);
  (B) cosmic-mean well    Phi_mean(r)   = -(1/2)(4pi/3) G rho_m(z) r^2.
They agree to a factor ~2 (DE is ~2x the mean at z=0.3), so the answer is bracketed, not arbitrary.

**STEP 4 — the matching radius r_ta.** The cluster edge = turnaround radius, fixed by spherical
collapse: M500 = (4/3)pi r_ta^3 Delta_ta rho_crit(z) with Delta_ta/rho_crit(z) ~ 2.8 (Lambda-modified
collapse, Om(z=0.3)=0.503), giving **r_ta/R500 = (500/Delta_ta)^(1/3) = 5.64 — the SAME multiple for
ALL clusters** (a structural number, not per-object). r_ta = {3.67, 5.29, 6.27, 7.90} Mpc for M500 =
{1,3,5,10}e14. Note (mu r_ta) = {3.7, 5.3, 6.3, 7.9}: the matching radius is several oscillation
wavelengths outside 1/mu — deep in the Helmholtz oscillatory tail. This is exactly the regime where
the cosmological background field IS the physical boundary the cluster sits in.

**STEP 5 — chi_out and eta(R500), all clusters, fed back into the full nonlinear solver.** With the
BC imposed as Phi(r_ta)=chi_out (replacing the degenerate Phi(inf)->0):

| M500 [Msun] | r_ta [Mpc] | chi_out(DE) [(m/s)^2] | eta(R500) DE | chi_out(mean) | eta(R500) mean |
|---|---|---|---|---|---|
| 1e14 | 3.67 | -2.09e10 | 0.94 | -1.06e10 | 0.99 |
| 3e14 | 5.29 | -4.35e10 | 1.07 | -2.20e10 | 1.01 |
| 5e14 | 6.27 | -6.12e10 | 1.50 | -3.09e10 | 1.45 |
| 1e15 | 7.90 | -9.71e10 | 0.95 | -4.91e10 | 1.05 |

**eta = 0.94-1.50, never 2.15.** d eta/d log10(M500) = +0.16-0.18 (eRASS1: flat at 2.15, slope ~-0.03)
— the cosmological BC gives roughly MOND-to-mildly-boosted, NOT the 2x excess, and a non-monotone
mass trend (the oscillatory signature), not the flat 2.15.

## IS IT UNIVERSAL? (the honesty pivot, both ways)

- **YES, it is ONE prescription, not a per-cluster free parameter.** chi_out(M500) =
  -(1/6)Lambda c^2 r_ta(M500)^2 is a fixed function: d log chi_out/d log M500 = +0.667 = 2/3 exactly
  (since r_ta ~ M500^{1/3}). Every cluster gets chi_out from the same cosmology + the same turnaround
  multiple. There is **no per-object dial.** This is the genuine content of Route A: the matching IS
  universal, and it does NOT secretly hide a per-cluster knob.

- **BUT the magnitude is too small to force 2.15, AND the result rides the matching-radius phase.**
  The robustness sweep (5e14 fiducial, both estimators) over the matching radius:

  | r_ta/R500 | (mu r_ta) | chi_out(DE) | eta(DE) | eta(mean) |
  |---|---|---|---|---|
  | 2.0  | 2.22 | -7.7e9  | 0.38 | 0.40 |
  | 3.0  | 3.34 | -1.7e10 | 0.60 | 0.56 |
  | **4.0**  | **4.45** | **-3.1e10** | **2.05** | **2.03** |
  | 5.64 | 6.27 | -6.1e10 | 1.50 | 1.45 |

  eta swings 0.38 -> 0.60 -> **2.05** -> 1.50 as the matching radius walks 2->5.64 R500, because
  (mu r_ta) sweeps through the Helmholtz oscillation. **2.15 IS hit at r_ta/R500≈4** — a perfectly
  defensible turnaround multiple — but the spherical-collapse value computed honestly here is 5.64,
  giving 1.50. So 2.15 is reachable, but it is NOT forced by the cosmologically-fixed amplitude; it
  requires landing the matching radius on the right oscillation phase (≈4 R500). **The chi_out NEEDED
  for 2.15 (~ -2 to -3e11 = 0.2-0.3 v_c^2) is 3-10x LARGER than any cosmological estimator (~ -3 to
  -6e10).** By magnitude, cosmology under-delivers; the only route to 2.15 is the phase.

## Both ways, honestly

- **Does cosmology FORCE 2.15?** NO. The cosmological chi_out magnitude is ~0.03-0.06 v_c^2, 3-10x
  too small; at the honestly-computed turnaround radius (5.64 R500) it gives eta~1.5, and across
  clusters 0.94-1.50 with the wrong (rising, non-monotone) mass trend. **The closing-calc DEFICIT
  verdict survives the cosmological-BC test by magnitude.**
- **Is it a per-cluster TUNE?** NO — the prescription is genuinely universal (one formula, scaling as
  M^{2/3}, no per-object dial). This part of the prompt's hope is VINDICATED: matching to cosmology is
  NOT a disguised per-cluster knob.
- **The residual lever is per-CONVENTION, not per-cluster.** Because the operator oscillates, eta is
  phase-sensitive to the matching radius; 2.15 lives at r_ta/R500≈4, not the collapse value 5.64. That
  is a single global convention choice (~30% in r_ta), not 9830 individual tunes — much weaker than a
  per-cluster tune, but still NOT a forced first-principles output. Honest grade: cosmology pins the
  amplitude (small -> deficit/mild) and universalizes the prescription, but the 2.15 target sits on an
  oscillation phase that the matching radius is not forced to hit.

## What Carl CAN / MUST NOT say

- **CAN:** "The Helmholtz boundary constant chi_out is NOT a per-cluster free parameter — matching the
  cluster scalar to the evolving cosmological AeST background fixes it universally to
  chi_out=-(1/6)Lambda c^2 r_ta^2 ~ -0.03-0.06 v_c^2 at z~0.3, scaling as M500^{2/3}. Done this way it
  gives eta(R500)~0.9-1.5 (a mild, near-MOND result), NOT a per-object tune."
- **MUST NOT:** "cosmology forces eta=2.15." It does not — the cosmological amplitude is 3-10x too
  small, and 2.15 appears only at a matching radius (~4 R500) the spherical-collapse calculation does
  not select (it gives 5.64 -> 1.50). Reaching 2.15 still rides the oscillation phase, a global
  convention, not a forced output.

## Where this leaves clusters (consistent with the banked closing-calc verdict)

Route A CONVERTS the closing-calc's "free per-cluster chi_out" into a "universal cosmological chi_out"
— a real conceptual gain (the BC is no longer a per-object knob) — but it does NOT convert the deficit
into the 2.15 cure: the universal cosmological amplitude is too small, and the boost that exists rides
an unforced matching-radius phase. **Clusters remain MOND's shared liability; the AeST mass term with
a cosmologically-matched BC predicts a mild, near-MOND eta, not the eRASS1 2x.** The flatness of the
real eRASS1 eta(M500) is NOT reproduced (Route A gives a rising, non-monotone trend), which further
disfavors a pure cosmological-BC origin for the observed 2.15.

Sources: Verwayen, Skordis & Zlosnik 2024 MNRAS 531 272 (arXiv:2304.05134, chi_hat_out / cosmological
AeST background); Durakovic & Skordis 2024 JCAP 04 040 (arXiv:2312.00889, Eq 2.18/2.40, "depends on
the boundary value of the gravitational potential"); Skordis & Zlosnik 2021 PRL 127 161302. Banked
closing-calc: `CLUSTER_CLOSING_CALC_VERDICT_2026-06-14.md`, `cluster_aest_shooting_solver.py`.
