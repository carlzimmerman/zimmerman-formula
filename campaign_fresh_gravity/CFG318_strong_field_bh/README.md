# CFG318: gate G11 (strong field: black holes, neutron-star structure) for the filtered C-H/K chassis

Criteria frozen first: `FROZEN_CRITERIA.md` (commit 1d3908e07). Script: `cfg318_strong_field_bh.py`.

| run | output files | checks | exit code |
|---|---|---|---|
| main | `.out`, `_results.json` | 13/13 pass | 0 |
| MUTATE (`CFG318_MUTATE=1`, alpha = 0.1) | `_MUTATE.out`, `_results_MUTATE.json` | 11/13 (the window gate fails; the NS reading row fails); verdict reads KILL (dipole) | 1, as required |

Run from anywhere; about 9 minutes (the WKB and neutron-star sections dominate).

## Verdict: CONDITIONAL (recipe section 6), by the frozen rule

Every scored observable passes at every window point, by 7 to 15 orders of magnitude. The static black hole's O(alpha)
exterior is derived and regular. What is not established is that **slowly moving (or rotating) black holes are
regular** when alpha_c != 0. The chassis needs alpha_c > 0 (L340 H4, XC1, XC2, CFG291), so this is the named
condition.

**The condition, and the owner flag.** Ramos & Barausse 2019 (PRD 99 024034) find that slowly moving khronometric BHs
carry curvature singularities at the spin-0 horizon for generic (alpha, beta, lambda). They are regular only on the line
alpha = beta = 0. Franchini, Herrero-Valea & Barausse 2021 restate this as: regular moving BHs "require alpha and beta to
vanish exactly". The evidence is:
- a numerical solution at a single point, (alpha, beta, lambda) = (0.02, 0.01, 0.1), seven orders above the window;
- a boundary-condition count: once the matter horizon is regular and the solution is asymptotically flat, no free
  constant is left to make the spin-0 horizon regular.

The authors say they did not explore small non-zero alpha and beta. Under the frozen rule this is not a failure
demonstrated inside the window, so the verdict is CONDITIONAL, not KILL. But the count does not depend on the size of
alpha. **If the owner reads that count as a proof for every alpha > 0, G11 reads KILL for this chassis.** This lane
does not make that call. In the window, the spin-0 horizon sits inside the Killing horizon, about 0.6 M/c_S outside
the universal horizon, with c_S >= 444.

## Results

### 1. Static black holes

**Map.** CFG291's map: alpha = c14 = alpha_c, beta = c13 = 0, lambda = c2 = c_2.

**Derivation.**
- Start from the reduced action in khronon-adapted ADM variables (N, N^r, gamma_rr), derived in sympy.
- At alpha = beta = 0, Schwarzschild with any maximal slicing (K = 0) solves it, for symbolic lambda and C (control C1).
- Regularity at the universal horizon fixes C = 3 sqrt(3) M^2/4 and r_UH = 3M/2.
- At O(alpha), lambda K acts as a multiplier mu, and the khronon equation forces K = O(alpha/lambda). The exterior
  metric is therefore lambda-independent; the neglected relative correction is alpha/lambda <= 4.4e-7.
- Eliminating the multiplier gives a closed system.

**Result (derived in-lane; no published closed form adopted):**

    e(r) = -g_tt = 1 - 2M/r + alpha q(r),   (r^2 q')' = Sigma(r),   q -> 0 with no constant and no 1/r term
    Sigma(r) = -(64 r^6 - 360 r^5 - 108 r^4 + 540 r^3 + 1944 r^2 + 1458 r + 729) / (2 r^4 (2r - 3) (4r^2 + 4r + 3)^2)   (M = 1)
    g^rr = e / (e + r e' + (alpha/2) r^2 U'^2),   U'^2 = a.a of the alpha = 0 foliation

- q is evaluated by quadrature. The inner integral is in closed form; three independent evaluations agree to 1e-13.
- Values: q(2) = -1.05e-3, q(3) = -8.02e-4, q(6) = -3.96e-4.
- Large r: q = -1/(6 r^3) + 49/(96 r^4) + ...
- The khronon-charge shift c1 drops out of e and g^rr at this order (checked).

**Regularity.**
- **Exterior, r >= 2M:** q is smooth (its only pole is at r = 3/2, the universal horizon). The Killing horizon moves
  by delta r_H/r_H = +1.05e-3 alpha.
- **Interior:** Sigma has a simple pole at r_UH with residue -1, so in the K = 0 form q ~ x ln x there. At finite
  lambda, the perturbative khronon correction grows like (alpha/lambda)/x^2. Both signal a non-perturbative boundary
  layer of width ~ M/c_S inside the Killing horizon, which is where the spin-0 horizon sits.
- **Existence through that layer** rests on Barausse, Jacobson & Sotiriou 2011's numerics (regular at the spin-0
  horizon across the explored viable ranges). Those numerics did not reach alpha ~ 1e-9. This is the static half of
  the scope limit.

### 2. Observables

All deviations are fractional per unit alpha, lambda-independent at this order, and scale-free (the same for M87*
and Sgr A*).

| quantity | d ln X / d alpha | max over window (alpha = 3.2e-9) | bound | margin |
|---|---|---|---|---|
| shadow b_c | +1.2031e-3 | 3.85e-12 | 0.10 (EHT Sgr A* VI, "~10%") | 2.6e10 |
| photon sphere r_ph | +2.366e-4 | 7.6e-13 | — | — |
| QNM frequency (eikonal, Omega_c) | -1.2031e-3 | 3.85e-12 | 0.01 (strict floor under GW250114's "few percent") | 2.6e9 |
| QNM damping (eikonal, lambda_L) | -6.370e-2 | 2.04e-10 | 0.01 | 4.9e7 |
| ISCO radius | +2.787e-3 | 8.9e-12 | none used (reading vs 1%) | 1.1e9 |
| ISCO frequency | -2.921e-3 | 9.35e-12 | none used (reading vs 1%) | 1.1e9 |
| l = 2 test scalar, WKB3: Re omega / Im omega (reading) | -1.79e-3 / -6.46e-2 | 2.07e-10 | — | — |

- The WKB l = 2 shifts track the eikonal ones: -1.79e-3 vs -1.20e-3 for the frequency, -6.46e-2 vs -6.37e-2 for the
  damping.
- The damping-time shift is the largest coefficient. It comes from the khronon's acceleration term (alpha/2) r^2 a^2
  in g^rr.

**BH dipole radiation.**
- **BBH:** Delta s = 0 for non-spinning holes. A vacuum BH's sensitivity is a pure number, independent of mass.
- **NS-BH:** Delta s = s_NS, taken from CFG311 (at most 0.470 alpha_c), with s_BH = 0 (its alpha = beta = 0 value).
  Then B_dip <= 2.2e-20 against <= 1e-4 (Owen et al. 2025), a margin of 4.6e15. The khronon's GW-band wavelength is
  << xi, so the wave-zone factor is 1 there.
- **What s_BH would have to be.** The dipole would bite only if |s_NS - s_BH| >= s_crit:
  - s_crit = 0.10 at the top-alpha / bottom-c_2 corner;
  - min s_crit/alpha_c = 3.2e7.
  - So the bound bites only for an O(0.1) BH sensitivity, as in theories where BHs have s ~ 1.
  - Ramos & Barausse's sigma ~ 1e-3 at alpha = 0.02, scaled linearly, suggests s_BH ~ 0.05 alpha, about 1.6e-10.
- s_BH is not computed here; it belongs to the moving-BH condition.

**MOND / heat filter near a BH.** The brief's "y >> 1, so the filter suppresses it" holds, with one refinement:
- The filtered field near a galactic nucleus need not be high-y. It can vanish at a symmetric centre.
- The bound used is therefore the kernel's own: for any filtered y, |MOND force| <= max h_mono a0.
- **Worst case:** epsilon_MOND = h_max a0 / g(r_ph) <= 9.9e-14 (M87*, alt footing); Sgr A* gives 7e-17 and a
  10 Msun hole 2e-22.
- **Filter suppression at k = 1/r_ph:** exp(-552) for M87*, exp(-1.5e9) for Sgr A*, exp(-2.3e20) for 10 Msun.

### 3. Neutron stars

- **Equations.** The static star with an aligned khronon (K = 0, a = D ln N), derived from the same reduced action
  plus a perfect fluid. At alpha = 0 the equations reduce to TOV exactly.
- **EOS.** SLy (Read et al. 2009, parameters recalled as in CFG311).
- **alpha = 0:** M_max = 2.0485 Msun (recalled 2.049).
- **Regularity.** Centre: y = N'/N proportional to r (N'(0) = 0). The surface is smooth. CFG311's moving-star khronon
  coefficient e^(2Phi - Lambda) stays positive, so that equation has no singular point on any star; contrast the BH,
  where the same operator has an irregular singular point at the universal horizon.
- **Max-mass shift.** d ln M_max/d alpha = -0.910 (from alpha = +-1e-3), so |delta M_max/M_max| <= 2.9e-9 on the
  window. M is the exterior Keplerian mass in G_N units.

## Controls

| control | result |
|---|---|
| C1 alpha -> 0 | the alpha = beta = 0 maximal-slicing family solves the reduced equations for symbolic lambda, C, M; at alpha = 0, e = g^rr = 1 - 2M/r exactly; every deviation carries alpha |
| C2 published BH (Berglund et al. 2012) | the c14 = 0 family solves the lane's equations exactly at beta = c13 != 0; regularity gives r_UH = 3 r0/4 and r_ae^4 = 27 r0^4/(256 (1 - c13)) (c13 = 0, 0.3) |
| C3 published asymptotics (BJS 2011 eqs. 24-25) | the e series gives -c14 r0^3/48 x^3; the EF B series gives +c14 r0^2/16 x^2 and +c14 r0^3/12 x^3; all exact |
| C4 Schwarzschild numbers | r_ph = 3M, b_c = 3 sqrt 3 M, r_ISCO = 6M, M Omega_c = M lambda_L = 1/(3 sqrt 3), r_H = 2M; the shadow and Omega_c slopes equal -/+ 3 q(3)/2 |
| C4b WKB3 | l = 2 scalar n = 0: 0.48321 - 0.09680i (recalled 0.4836 - 0.0968i) |
| C5 numerics | nested vs closed-form quadrature 1e-28; series to O(x^10) at r = 50: 8e-14; an inward ODE integration to r = 3: 1e-13 |
| C6 injection | a 20% shadow and a 5% QNM deviation are flagged |
| C7 kernel | nu_mono reproduces L340's y_p, h_p |
| C7b dipole speed | reproduces XC1's committed c_S (443.85 to 7.9356e5) |
| C8 TOV | alpha = 0 reproduces TOV and SLy M_max |
| D2 | the linear equation reduces exactly to (r^2 Q')' = alpha Sigma + 24 C c1/r^4; c1 drops out; the g^rr identity holds |
| WINDOW | every scored alpha is inside L340 P1. The top corner sits exactly on the pulsar bound alpha-hat2 = 1.6e-9, by construction (as in CFG291) |
| MUTATE alpha = 0.1 | the window gate flags it (|alpha2| = 0.05 >> 1.6e-9), rc = 1 |

**MUTATE.** As pre-registered, EHT and ringdown do not flag alpha = 0.1. At O(alpha):
- shadow 1.2e-4 (margin 830);
- eikonal damping 6.4e-3, under even the strict 1% floor (margin 1.6).

Two other things do flag it:
- **The window gate** (load-bearing, so rc = 1).
- **The NS-BH dipole.** With s_NS = 0.47 x 0.1, B_dip = 0.135 against 1e-4, so the MUTATE verdict reads KILL. Two
  caveats:
  - This uses CFG311's leading-order s, extrapolated far outside its alpha/lambda << 1 validity.
  - The frozen text named only the window gate as the expected flag. The dipole flag is reported as found.

The NS max-mass reading also moves by 9% at alpha = 0.1. Black-hole imaging and ringdown are weak discriminators of
alpha: PPN and the pulsars already bound it 7 to 9 orders more tightly.

## Disclosures

- **Literature is PROVISIONAL.** Values were read through a summarising fetch tool (arXiv abstracts, ar5iv, the arXiv
  export API), and the summariser is not the table.
  - One fetch of an arXiv PDF URL was saved automatically outside the repository by the tool. It was not read, and
    nothing rests on it.
  - The ringdown bound is the abstract's "a few percent", scored as a strict 1%.
  - The dipole bound's definition (Owen et al. 2025) was not read.
  - The M87* abstracts give no percentage. The shadow shift is scale-free, so the Sgr A* number covers both.
- **Not blind.** The exploratory sympy work (Sigma, the e_3 = -alpha/6 match, delta b/b ~ 1.2e-3 alpha) preceded the
  freeze. It is listed in FROZEN_CRITERIA section 0.
- **Four coding errors were fixed during development.** No run with them was kept; scratch runs only.
  1. The large-r series for q used the wrong power (x^(k-2)/((k-1)(k-2)) instead of x^k/(k(k-1))), so C3 failed in
     that scratch run. C3 is exact after the fix.
  2. C1 compared mp values against float arithmetic at 1e-25 (dev 1e-16). The comparison is now at mp precision.
  3. The NS lapse root was coded with a 1/alpha form that divides by zero at alpha = 0. It was rewritten as the same
     root without 1/alpha.
  4. The window check used a strict < at the top corner, which equals the bound by construction. It now uses <=.
- **WKB derivatives.** A first, fully symbolic attempt at the WKB derivatives was too slow. It was replaced by Taylor
  series in r with d/dr* applied as series algebra.
- **A K = 0-model nonlinear shooting** for static existence at finite alpha was tried in scratch and abandoned: the
  integration broke down near r ~ 1.9M for untuned C. Nothing from it is used or claimed.
- **NS parameters** are CFG311's recalled Read et al. values; only SLy was used for the max-mass slope.

## What this lane cannot say

- It works at leading order in alpha_c, with beta = 0 and alpha/lambda << 1, and gives the exterior metric only. The
  near-UH interior is a non-perturbative boundary layer. Static existence through it is adopted from BJS 2011, whose
  numerics did not reach the window.
- It contains no moving-BH or rotating-BH computation at alpha != 0, and no BH sensitivity. This is the open
  condition.
- QNMs are covered at eikonal order for the tensor modes, and at l = 2 only for a test scalar. The khronon's direct
  coupling to finite-l gravitational perturbations is not derived; by order counting it is O(alpha) and
  lambda-independent.
- It is one gate on one chassis. It is not "the theory works". kappa = 1/2 remains FITTED, and the dark sector still
  requires the cold mass.
