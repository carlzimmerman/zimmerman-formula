# NPJ1 RESULT: a non-perturbative origin for the law's function J? (2026-11-10)

**Label: SHAPE ONLY.** Four of the nine sectors reproduce the law's shape, but none has a natural size and a
renormalizable UV action at once. So T3(i) stays FAIL, and HZ1's open door finds no origin among the condensate,
strongly coupled leaf, and thermal or horizon sectors computed here.

Criteria: `FROZEN_CRITERIA.md` (local 249f297cd0, committed alone before any script). Script `npj1.py`; output `npj1.out` /
`npj1.json`; twins `NPJ1_MUTATE=1` -> `npj1_MUTATE.out` / `npj1_MUTATE.json`; Lean `NPJ1.lean` (`compile.txt`), false twin
`NPJ1_MUTATE.lean` (`compile_MUTATE.txt`). Runtime 15 s, 0.12 GB. TEST lane, quarantined: adopts nothing, relabels
nothing, registers nothing. Footings never pooled. No amendment. Origin ids are at the end.

## The deciding number

**10^5.42** (canonical; alt 10^5.37). That is the factor by which locality misses for every sector in which the clock's
acceleration sets the gap of the law-carrying modes. This covers HZ1's leaf pair, its interacting large-N version, and
the large-N Gross-Neveu sector. For the law to be a local function of A, those modes must be heavier than the inverse
length over which A changes. On QG1's 6e10 Msun point mass that needs a coupling c_g >= c^2/v_f^2 = 3.3e6 (canonical;
alt 3.0e6), against 4 pi. **No counting rule changes this.** The holographic count rescues the amplitude (the lead's
observation 3, true for the count). It does not touch a coupling.

The one sector that clears size and locality is the Berezhiani-Khoury superfluid (a1). It fails U: its stated
microphysics is a three-body contact of dimension -4.

## The candidates

S: max |mu - x/(1+x)| <= 0.1 on 0.01-100 and deep slope within 0.1 of 0.990. C = C-amp and C-loc, under rule H (HZ1's
ceiling) and rule W (holographic count plus species cutoff >= hbar c/kpc; an ASSUMPTION). U: power counting, plus HZ1's
J1/J2 detector on anything inserted by hand. The fits are footing-independent: the same function of x, rerun on alt with
the same seeds gives identical numbers. C numbers are canonical / alt.

| candidate | S: max dmu, slope | C-amp log10 R (H; W) | C-loc log10 R | U | label |
|---|---|---|---|---|---|
| a1 BK superfluid (NEW hidden boson) | **PASS** 0.0946, 0.956 | -32.0; -32.0 (Lambda 0.12-5.2 meV) | -57 (local) | **FAIL**: \|psi\|^6 dim -4 at z = 2; \|grad theta\|^3 inserted | SHAPE ONLY |
| a2 exact-Legendre condensate ((A)'s P restated) | PASS 0.0000, 0.990 | -21.0; -21.0 | -57 | **FAIL**: W odd orders 3, 5, ..., orders >= 7; k-body tower g_k = 1/k | SHAPE ONLY |
| a3 GP + Lee-Huang-Yang | FAIL 0.501, 0.489 | n/a | -57 | FAIL (\|A\| coupling inserted) | NONE |
| b1 large-N GNY, dynamical mass | FAIL 0.531, 0.000 | 53.0 / 52.9; 1.73 / 1.65 | 5.42 / 5.37 | PASS | NONE |
| b2 interacting leaf pair (large-N O(N) + Cl(6)) | PASS 0.0260, 0.964 | 55.36 / 55.28; 4.08 / 4.00 | **5.42 / 5.37** | PASS | SHAPE ONLY |
| c1 Bose mode, thermodynamic pairing | FAIL 0.440, 1.43 | n/a | n/a | FAIL (\|A\| as chemical potential) | NONE |
| c2 bath at dS-Unruh T(A) | FAIL 0.893, 0.000 | 114.4 / 114.3; 4.44 / 4.35 | 7.31 / 7.27 | PASS (state assumed) | NONE |
| c3 holographic leaf pair (G3's fields) | PASS 0.0260, 0.964 | 55.36 / 55.28; 4.08 / 4.00 | **5.42 / 5.37** | PASS | SHAPE ONLY |
| c4 horizon dof (one per 4 Planck areas) | FAIL 0.972, 0.000 | 0; 0 | 6.52 / 6.47 | FAIL (no local action) | NONE |

Lane label = best = SHAPE ONLY (a1, a2, b2, c3), on both footings.

## What carries it

**1. The shape is easy; size and action are not.** Four routes give the shape:
- the law restated (a2);
- HZ1's boson-fermion pair (c3; b2, whose fit drives the O(N) coupling to lambda_hat = 10^-3.65, i.e. back to the free
  pair: strong coupling does not improve the shape);
- BK's additive force law a = a_N + sqrt(a0' a_N) (a1).

BK's pass is narrow: 0.0946 at x = 9.8, dense grid the same, with a0'/a0 = 0.42. Its deep-MOND scale is 0.42 of the
crossover scale of x/(1+x), which the absolute 0.1 band admits. CFG117 tested the same additive form (Verlinde's
point-mass formula) with the scale fixed at cH/6 and a relative 10 % band on 1/mu, and it failed. The two tests differ;
both results stand.

**2. Locality (new).** In a sector where A sets the gap, the law-carrying modes have mass c_g |A|. At A = a0 their Compton
length is c^2/(c_g a0) = 31 Gpc/c_g (alt 26 Gpc/c_g): Hubble-sized for any natural coupling.
- The derivative expansion that turns such a sector into a local J(|A|) needs m r >= 1. On the reference mass,
  m(x a0) r(x) = c_g (v_f^2/c^2) sqrt(1 + x) (Lean `npj1_cloc`), so c_g >= c^2/v_f^2/sqrt(1.01) = 3.28e6 / 2.98e6.
  For a 1e8 Msun dwarf it is 8.0e7 / 7.3e7.
- Reported consequence (R2, one loop, KA7's bubble), with g_B = 4 pi: the leaf fermion's momentum-dependent stiffness
  (g_F^2/4)|p| per 8-component fermion exceeds GR's by 3.2e5 at the MOND radius (9.45 kpc) and by 6.2e14 at 1 AU (alt
  2.9e5, 5.1e14).
- So outside the constant-A limit HZ1 computed in, c3 does not give the law. It gives a non-local screening of the
  Newtonian potential on every scale.

**3. The lead's observation 3: right for the count, wrong as the rescue.** The leaf pair needs nu N g_B^3 = 5.6e89 eV
(alt 4.6e89 eV). At g_B = 4 pi that is nu N = 2.8e86 eV.
- Under H (nu N <= 1000 M_Pl) it misses by 10^55.36 / 10^55.28, HZ1's number.
- The bare holographic count (nu N <= pi M_Pl^2/H = 3.9e89 eV; N_dof = 2.4e119 against S_dS = 3.3e122) passes it with
  10^3.14 to spare.
- But the species cutoff M_Pl^2/(N nu) is then 5.3e-31 eV, against hbar c/kpc = 6.4e-27 eV, which misses by 10^4.08 /
  10^4.00. Gravity would be strongly coupled on every scale below hbar c/Lambda_sp = 12 Mpc (alt 10 Mpc), galaxies included.
- Locality fails by 10^5.4 under either reading.
- The 10^55.4 is not "exactly M_Pl/H": it is M_Pl/E_a0 (10^61.77) times Bc/(1000 (4 pi)^3), against
  log10 M_Pl/H = 61.01.

**4. Strong coupling.**
- **b1, large-N Gross-Neveu-Yukawa** (Cl(7) mass sigma Gamma^0 + g A.Gamma, exact large-N minimum, Lean `npj1_gn_min`).
  The dynamical mass M reverses the needed structure: V is analytic (-M^3/(3 pi) + (M/pi) g^2 A^2) for gA < M and
  (2/(3 pi)) g^3 |A|^3 above. So mu is constant, then grows linearly without bound (slope 0, max dmu 0.53).
- **b2, large-N O(N) boson** (exact gap equation, nu = 1 at strong coupling, KA5). It changes neither the |A|^3
  coefficient nor the amplitude: the fermions carry both. At leading large N the free energy scales with N, so the
  coefficient problem is the same.

**5. Condensates.**
- **a1, BK superfluid.** a0' = alpha^3 Lambda^2/(8 pi M_Pl), derived by Euler-Lagrange (KA6; Lean `npj1_bk`).
  - Natural inputs give it: Lambda = 0.12 meV at alpha = 4 pi, 5.2 meV at alpha = 1 (alt 0.13, 5.7 meV), next to
    rho_DE^(1/4) = 2.24 / 2.46 meV. That is the record's W3 coincidence again, not derived.
  - The size is natural because the law lives in a separate field with gravitational-strength coupling to baryons, so
    the M_Pl^2/a0 cubic coefficient comes out of M_Pl/Lambda field factors.
  - U fails: BK's P proportional to X|X|^(1/2) comes from a three-body contact (coupling dimension 5 - 9 = -4 at z = 2).
  - It is also not J inside (A): it is a second field. QX28 already fails the class on G3-G6 and G8.
- **a2, the P(X) that Legendre-maps to J.** It is eps(n) = eps0[-n_hat - ln(1 - n_hat)], P(mu) = eps0[mu_hat -
  ln(1 + mu_hat)], with eps0 = a0^2/K = (0.84 meV)^4 (alt 0.92 meV) and n_max = a0/K = (13.5 MeV)^3.
  - Its microphysics is an infinite tower of k-body contacts with g_k = 1/k (k = 2 ... 8 printed) and a hard cap at
    n_max.
  - It is the record's QX29 W, "worked backwards from the law", and it fails U for the same reason HZ1's J1/J2 did.
- **a3, the textbook condensate (GP + LHY).** It gives |A|^(5/2), deep slope 0.49.

**6. Thermal and horizon sectors are analytic in A^2.**
- **c2, bath at the dS-Unruh temperature.** T(A)^2 = (A^2 + H^2)/(4 pi^2) is a polynomial in A^2 and >= H^2/(4 pi^2) > 0,
  so any bath P(T) has no odd power of A. The detector confirms it for T^4 and for a 3-d T^3; twin M5 (H = 0) shows
  |A|^3. For massless bosons mu = 1 - alpha_t/2 - B(1 + A^2/H^2): decreasing, anti-MOND.
- **c4, the acceleration-dependent horizon's own degrees of freedom.** S = pi M_Pl^2 r_h^2, T = 1/(2 pi r_h),
  dE = T dS, so E = M_Pl^2 r_h, F = M_Pl^2 r_h/2, and f = (3/(8 pi)) M_Pl^2 (A^2 + H^2). That adds exactly 3 to mu,
  independent of A: three times GR's gradient term, no MOND.
- These are free-energy versions. The inertia version (T_eff -> m_eff) is the record's GAP and was not re-run.

## The Bose-Einstein identity: true, and no physics

Lead's observation 1, computed:
- **(i)** W(p) = ln Z_BE(p) - p, W'(p) = nbar_BE(p) = p/(1-p), and x = p/(1-p) inverts x/(1+x) = p (sympy; Lean
  `npj1_be_moebius`).
- **(ii)** The same map is the Fermi-Dirac / Langmuir occupation at fugacity x: x/(1+x) = 1/(1/x + 1) (Lean
  `npj1_fd_reading`). So it selects no statistics.
- **(iii)** Under thermodynamics' own pairing (ln z with N), the Legendre partner of ln Z_BE is -S_BE(n) =
  -[(1+n) ln(1+n) - n ln n], not W.
- A real Bose mode with |A| as its chemical potential (c1) gives nbar/y: mu -> -infinity at small x, max dmu 0.44.
- Twin M7: putting the field linearly in the fugacity, i.e. (A)'s pairing, gives back the law to 1.2e-8. The pairing
  carries the law, not the statistics.

The record already holds this as an identity: route A ("It is an identity. It does not say why a gravitational energy
should be an excess pressure") and A2 (W "is conjugate to the activity, not to a chemical potential"). The lead's form,
one bosonic mode minus its fugacity, is the same function as the lattice-gas excess pressure.

## The lead's other observations

- **(2) J's scale.** a0^2/(4 pi G) = c^2 rho_DE/(16 pi) exactly (0.019894 rho_DE c^2), = 1.04e-11 J/m^3 canonical,
  1.53e-11 J/m^3 alt. Right.
- **(3) The scales.** a0 = T^2/M_Pl holds at T = 1.58 meV (alt 1.74 meV), HZ1's thermal number. The holographic leaf
  density absorbs the 10^55.4 (item 3 above). Right for the count; the rescue fails on species and locality.

## Reported

- **R1 kappa and the 5.41: not fixed by any candidate.** BK's a0' carries a free Lambda, not tied to rho_DE (QX28,
  bridge scout: "a non-Lambda a0"). In the leaf pairs, a0 = c m_b0/g_B with m_b0 independent of Lambda_cc. a2 restates
  (A). The ROOT note's hope that kappa is a universal amplitude ratio of a fixed point does not happen in any sector
  computed: each needs one free dimensionful input to place a0. The 5.41 is untouched.
- **R4 walls.**
  - W3: BK's Lambda sits at the meV end; the leaf pairs need masses about a0, i.e. about H.
  - W4 (kappa free): stands.
  - W1, W2: no matter-content claim made.
  - sqrt(pi): not reached, since no kappa comes out.
- **Aside (HZ1, reported only).** HZ1's R1 line writes a0 = m0/(c g_B), but its fit convention (s = g_B A/m0 = c x)
  gives a0 = c m0/g_B. Its R1 conclusion (kappa not fixed) and every graded number are unaffected.

## Known answers (all PASS, read before any graded line)

| check | result |
|---|---|
| KA1 3-d determinant | non-analytic part -m^3/(12 pi), relative 2.4e-19 |
| KA2 Bose-Einstein | sum p^n = 1/(1-p), nbar = p/(1-p), g_1 series; critical density zeta(3/2)(mT/2 pi)^(3/2) exact |
| KA3 Lee-Huang-Yang | I = 8 sqrt2/15 (5.5e-30), coefficient 128/(15 sqrt pi) |
| KA4 Legendre | max_p[pu - W] = u - ln(1+u); GR + (a0^2/K)J -> mu = x/(1+x) |
| KA5 large N | O(N) gap equation and envelope dV/dr = -m/(8 pi) (sympy); exponents 0.500000 / 1.000000; Cl(7) anticommutators 0, det 1.6e-15; GN closed form vs minimizer 1.1e-16 |
| KA6 BK | Euler-Lagrange residual 0; a_theta^2/a_N = alpha^3 Lambda^2/(8 pi M_Pl) |
| KA7 3-d bubble | 1/(8\|p\|), relative 6.4e-18 |

Each candidate's mu was derived in sympy from its stated free energy and checked against the reduced form fitted: b1, b2,
c1, c2 and c3 all True.

## MUTATE (all bite)

| twin | result |
|---|---|
| M1 mu = x^2/(1+x^2) / the law | S FAIL (0.149, slope 2.0) / PASS |
| M2 c3 with a0 -> M_Pl | C-amp H log10 R = -6.41: passes (the fail is the hierarchy) |
| M3 v_f = c/3 | c_g needed 8.96 < 4 pi: C-loc passes |
| M4 even degree-6 EOS | admissible |
| M5 T = \|A\|/(2 pi), 3-d bath | odd order 3 reported |
| M6 N nu = 1000 M_Pl | Lambda_sp 1.2e25 eV >= hbar c/kpc |
| M7 field linear in the fugacity | law back to 1.2e-8 |

Lean: `NPJ1.lean` compiles (exit 0, 6 theorems: be_moebius, fd_reading, cloc, gn_min, bk, leaf_amp). The false twin
`NPJ1_MUTATE.lean` gives 4 errors (wrong inverse map, C-loc without (1+x), GN sign, BK with 4 pi).

## What this means for T3(i)

T3(i) stays FAIL (HZ1); this lane does not regrade it. HZ1's scope line left a non-perturbative origin open. Computed
here, it moves the fail rather than removing it:
- Inside (A), any sector in which the clock's acceleration sets the gap needs a coupling 10^5.4 above 4 pi to be local.
  That is true of the ROOT note's "3-d conformal sector on the clock's slices", since a CFT's gap is c_g |A| by
  dimensional analysis. It also needs either 10^55 copies (H) or a species count that makes gravity strongly coupled
  below about 12 Mpc (W).
- Outside (A), a separate superfluid with its own scale gets the size naturally and the shape marginally. It loses the
  renormalizable UV, the a0-rho_DE tie and kappa.

## Limits

- Large N at leading order only. BK only in its zero-temperature gradient regime. One reference galaxy for C-loc (the
  dwarf's tighter number is reported).
- R2's stiffness is a one-loop estimate.
- Rule W is an assumption (labelled). The W-count-alone reading is reported for b2 and c3 (amplitude PASS, locality
  FAIL) and is never a label.
- Every literature input is PROVISIONAL: BK's microphysics, Deser-Levin's T(A), Dvali's species bound, the holographic
  bounds. The labels do not depend on a factor of 1000 in any of them; locality's 10^5.4 uses none.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## Commit ids (local / origin)

(filled in by the next commit)
