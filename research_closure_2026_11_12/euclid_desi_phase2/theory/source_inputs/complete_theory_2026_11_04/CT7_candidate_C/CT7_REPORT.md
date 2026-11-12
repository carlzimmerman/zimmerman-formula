# CT7: candidate C graded (CFG911 N6 potential portal inside v3s). Stops at G3

This lane grades candidate C under owner decision D1 ("Yes, grade it"). Grading is not adoption: nothing here is adopted, the cold sector retired on 2026-11-01 stays retired, and no particle is added. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s^2 are never pooled.

**Files:**
- `FROZEN_CRITERIA.md` was written before any number.
- `ct7_candidate_c.py` uses sympy, numpy and scipy on one thread. It ran in 1.1 s with a 0.28 GB peak RSS.
- The outputs are `ct7_candidate_c.out` and `ct7_results.json`.
- Nothing was downloaded. Nothing outside this folder was edited.

## The action graded

    S = (c^3/16 pi G) ∫ sqrt(-g) [R - 2 J(Y; a0(phi)) + 2 K(Q)] - (gamma_L/2) ∫ sqrt(-g) [max(D.P, 0)]^2
        + ∫ sqrt(-g) [-(1/2)(d phi)^2 - V(phi)] + S_m[g, matter],      a0(phi)^2 = xi G V(phi)

- J is v3s's J_x with its bare Lambda set to 0, so all of the dark energy is phi.
- phi is minimally coupled and does not enter S_m.
- The portal is CFG911's N6 as frozen (`campaign_fresh_gravity/CFG911_kappa_constructive_coupling/FROZEN_CRITERIA.md:124`).

## Gates

| gate | label | numbers (`ct7_candidate_c.out` line) |
|---|---|---|
| G0 health | **PASS, conditional on W4b (UNDECIDED, inherited from CT2_REPORT.md:7)** | 4 DOF, and no derivative of phi enters J (l.18). On FRW, J'(0) = -1 does not depend on a0, so phi decouples at quadratic order (l.16-17). The static-background mass induced by J gives \|m\|R ≤ 4.1e-5 at lambda = 10 (l.27-36). |
| G1 weak field | **PASS** | The v3s J term gives AQUAL with mu = x/(1+x) (law S) whatever sets a0 (l.6-7). Shifting a0 by the G2 maximum moves the law by 1.1e-9 dex (l.61-63). |
| G2 local constancy | **PASS** | delta ln a0 is recomputed from v3s's own J. The a0-charge equals CFG911's h(x) (l.9), and the CFG911 numbers are reproduced (l.43-55). Cluster: 3.6e-11 / 4.1e-11 lambda^2. The worst environment spread is 2.2e-9 dex at lambda = 10, a margin of 6.7e6 (l.52-53). The cosmological perturbation channel is about 1e-9 (l.51). |
| G3 tie | **FAIL (first failed gate)** | GT passes in every realisable background (≤ 0.029 dex, l.75-86). The slope fails: least-squares s is 0.586 (B2 thawing), 0.405 (B3 freezing) and 0.661 (F1, exponential V with lambda = 1 solved from the field equations), against 0.5 ± 0.01 (l.87-88). |
| G4 local gravity | REPORT ONLY (PASS, inherited) | At the Sun, delta ln a0 ≤ 8.7e-22 at lambda = 10. There is no tree-level fifth force, and c_T is unchanged. C6P's Q2 margin of at least 2.80e7 / 3.30e7 inside Park, Mars at 0.173 of its bound, and W4a's 5.1e-32 carry over (l.95-98). |

## Why G3 fails: CT1's claims checked against the field equations

**CT1's running law is not the law of N6.**
- From the Klein-Gordon equation (check S8, l.20), the potential portal gives d ln a0/d ln a = -(3/2)(1+w) - w'/(2(1-w)).
- The form -(3/2)(1+w) is CFG911's energy-portal law (N1). It holds for N6 only when w is constant.
- The local exponent of a0 on rho_DE is s = 1/2 + w'/(6(1-w)(1+w)). Two examples:
  - Thawing fields, where w' ≈ 3(1+w), give s ≈ 3/4 (F1 local s is 0.61 to 0.74, l.82).
  - B3 gives s = -0.10 today (l.78).

**"Locally silent" is confirmed.** The value is 3.6e-11 lambda^2 at a cluster.

**The way out fails health.** The energy portal (C', a0^2 = xi G T_nn in the khronon frame) would track rho_DE with s = 1/2 exactly. But it reverses the sign of phi's gradient term wherever h(g/a0) > 8 pi/kappa^2. That happens at x > 109, i.e. g > 1.0e-8 / 1.2e-8 m/s^2 (l.37), which covers every star and the Solar System.

So the healthy portal does not tie a0 to rho_DE, and the portal that ties it is unhealthy. This was not tuned around.

**Realisability.**
- A canonical phi cannot cross w = -1.
- The DESI DR2 CPL backgrounds B1, B1p and B1u, and also B4, are NOT REALISABLE by this candidate (l.69-80).
- If DESI DR3 or Euclid confirm the crossing, candidate C is excluded as a dark-energy model.

## Hand-set constants

| constant | role | status |
|---|---|---|
| xi | kappa^2 = xi | TRADE; any xi > 0 is consistent; kappa = 1/2 is not derived (l.89) |
| V0 | replaces Lambda | hand-set |
| lambda (V's shape) | new | hand-set |
| phi's initial condition | new | hand-set |
| L* | from v3s | hand-set |
| mu_K | from v3s | free |
| dust abundance | from v3s | hand-set |
| J_x's form | from v3s | postulated |

- Against v3s this adds two (lambda and phi's initial condition).
- At lambda = 0 the candidate is v3s exactly, with a0 renamed as xi.
- **Nothing derives kappa = 1/2.**

## Testable prediction

- **Prediction.** For a healthy canonical phi, N6 predicts a0(z)/a0(0) = sqrt(V(z)/V0).
- **Example.** In F1 that is +0.053, +0.060 and +0.064 dex at z = 1, 1.5 and 2.33, with a running of -0.28 today. a0 is larger in the past (l.82-83).
- **Size.** It differs from sqrt(rho_DE) tracking by ≤ 0.03 dex at z ≤ 2.33.
- **What tests it:**
  - DESI DR3 or Euclid w(z), where a confirmed phantom crossing kills the candidate.
  - a0(z) at z ≈ 1 to 2.5 to about 0.04 dex. CFG911 README:111-113 gives σ ≤ 0.043 dex at z = 2. The routes are high-z rotation curves (ALMA, JWST/KMOS, GS4) and a lens-redshift split of the lensing RAR (KiDS-Legacy, Euclid).
  - The local drift is a few 1e-11 per year, which cannot be measured.

**Caveats.**
- Point masses only.
- The q bound uses h(x) ≤ x, which holds under v3s screening (check S3).
- B2 to B4 are A29's stand-ins, used for their background definitions only; that folder is quarantined and is not evidence.
- S6 is a structural reading.
- The hand expectations in FROZEN_CRITERIA were confirmed.

kappa = 1/2 FITTED; not theory closed.
