# QX19 frozen criteria: one-action scorecard (AC2q + Pi^6 blend; v3s + blend as a second column)

Frozen before any QX19 script exists. Lane rules: closure_2026_11_06/SWARM_BRIEF.md. Adopts nothing; the owner
adopts. Kappa = 1/2 FITTED; not theory closed.

## The action graded

AC2q (AC7; field equations in QX17A, read only), with the stiffness gamma F(Sigma) - gamma(2X)^2/2,
Sigma = D.P + 2X. The original [max(Sigma,0)]^2/2 is replaced by AC21 iter_6's blend:
F = b^2 f(Sigma/b), with f from action_search_2026_11_05/AC21_smooth_3d/iter_6*/form.json (exact rationals),
f = q^2/2 for q >= 1, f = 0 for q <= 0, b = X.

Column 2 is v3s with the same blend and b = rho_DE.

The blend differs from the unblended action only on the layer 0 < Sigma < b. Every carry below must be proved from
that fact or recomputed. None may be assumed.

## Carries and their tests

- **C1, tensor (sympy, AC9 T1 method, generic F).** Expand gamma N sqrt(h) F(Sigma) to O(h^2) for TT modes with F
  arbitrary, writing F(Sigma0 + d) = F0 + F1 d + F2 d^2/2 with F0, F1, F2 arbitrary functions of position.
  - C1a: no (dh)(dh) term for any F, and every h dh term is a total derivative, so c_T = c.
  - C1b: the new mass on AC9's grid, with F1 = gamma b f'(q) and F2 = gamma f''(q) taken over q in [0, 1]
    (the layer) and b = s^2/2 at s^2 = 2 rho_DE. dv/c at 100 Hz must lie in the GW170817 band, both footings.
  - MUTATE-1: a planted c P^2 (d_z h_+)^2 must make C1a fail.
- **C2, lensing slip (sympy structure + bound).** Derive S_Psi for N sqrt(h) F(Sigma) with F generic (AC9 T2
  method). Show it splits into a part proportional to {F, F'} and a total divergence d_i(C_i F'(Sigma)).
  - Bound the blend's change, dF = F_blend - F_AC2q, with Delta0 = max|f - q^2/2| and Delta1 = max|f' - q| over
    [0, 1].
  - The non-divergence part is <= c gamma b^2 (Delta0 + Delta1). The divergence part's deflection is bounded by
    Helmholtz: |grad(Phi - Psi)| <= 4 pi |C| |dF'|.
  - Both, relative to rho_tot or g, on AC9 T2b's profiles (r = 30/100/310 kpc, Lstar up to 90 pc), must be < 1e-6.
- **C3, PPN / Solar System (bound).** The blend changes the stiffness force only on the layer. AC21's statics
  bounds (Cassini relative change <= 2.0e-5, both footings, for b = rho_DE; b = X <= rho_DE for AC2q, and the bounds
  are monotone in b) times C6P's Cassini margin (>= 4.8e7) must leave the margin > 1. PPN gamma = beta = 1 at
  O(GM) carries from V3W W1, because the stiffness enters beyond O(GM) there.
- **C4, FRW health (sympy, exact).** On FRW, P = 0, so Sigma = 2X and q = 2. Show:
  - f(q) = q^2/2 and dF/db = 0 identically on q > 1;
  - every perturbation with |delta Sigma| < X (and any delta b) stays where F = gamma Sigma^2/2 exactly.
  
  Then the FRW quadratic action equals AC2q's, and AC7 Q1 (72/72) carries.
- **C5, PN sign.** AC21 T7: B >= s for any convex F with F(0) = F'(0) = 0. Check f(0) = f'(0) = 0 exactly and
  f'' >= 0 on [0, 2] (exact pieces, grid of 20001 points plus the Bernstein argument from AC21's Lean
  `layer_nonneg`).
- **C6, well-posedness.** AC21 theorem: needs a pure power near 0 with m > d + 2. Check symbolically that f is
  exactly A q^6/30 on [0, 1/2], so m = 6 > 5. AC22's 2D numerics carry.
  - MUTATE-2: a blend with f'' ~ q^2 near 0 (m = 4) must fail the 3D condition.
- **C7, slow roots.** By C4 the linear FRW operator is unchanged, so AC23 PASS (HARMLESS, scoped) carries. If C4
  fails, C7 is NO VERDICT.
- **C8, galaxy statics / SPARC.**
  - The layer is the shell -2X < D.P < -X around D.P = 0 surfaces.
  - The change in the phantom field is bounded by QX2's stiffness bound (the whole stiffness moves the phantom by
    <= 5e-5) times max(1, max f'').
  - QX8's exact-field SPARC grade (rms 0.0560 / 0.0558, line PAPER67's) carries if that bound is < 1e-3 dex.
- **C9, galaxy linear health (AC7 Q2).** In the layer, F'' = gamma f'' with 0 <= f'' <= max f''. The stiffness stays
  positive and bounded, so no Gamma ~ k branch appears. Graded by checking f'' >= 0 and max f'' finite (reported).

## Gates not changed by the blend (carried as their own labels)

Clusters, CMB lensing/growth, Malin 1, AGC 114905, X-ray ellipticals, FN6, FG1 tilt (canonical) and the running
lanes (AC14, AC18, AC24, QX15) are listed with their labels from CLOSURE_FINAL.md.

The blend cannot rescue any of them. Its effect is bounded by C3/C8-type bounds (<= 1e-4 relative), and every one
of those misses is >= 0.05 dex. This is checked against the stated numbers.

## Lines

- CARRY (PASS) for each Ck whose test above holds.
- FAIL if a test fails.
- NO VERDICT if a MUTATE does not bite.
- Lean: fable_independent_2026/lean_2026/QX19_scorecard.lean certifies the algebraic carries:
  - q >= 1 implies F = Sigma^2/2 and is independent of b;
  - the FRW point q = 2;
  - m = 6 > 5, and m = 4 is not > 5;
  - margin * (1 - 2e-5) > 1.
  
  It needs a MUTATE twin that fails on its false claims, 0 sorry and standard axioms.

Output: one SCORECARD table (gate / label for the one action / evidence).
