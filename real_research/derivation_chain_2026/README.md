# The first-principles derivation chain (FP lanes)

One covariant action at the root, every observable varied out of it, nothing posited by hand below the postulates.
Each lane `FPn_*.py` is a runnable script with named checks, a verdict line
`N/M checks pass; load-bearing failures: K`, a results JSON carrying its `ledger`, and a `MUTATE=1` control that must
fail (rc = 1). `run_chain.py` assembles every lane's ledger into `CHAIN_STATUS.md` and enforces that contract.

```bash
python3 real_research/derivation_chain_2026/run_chain.py
```

Status words: DERIVED (varied out of the chain above, with a script), TIED (an input implemented as an exact
action-level relation, coupling chosen), POSTULATED (an input), FITTED (a constant set by data), CONSTRAINT (a derived
requirement on a lower link), OPEN (owed), FAILS (derived and contradicted by data).

## The inputs

- a0 = kappa c sqrt(G rho_DE), with the form forced by (G, c, rho) and kappa = 1/2 FITTED (FP0). On a true Lambda, a0 is
  flat in z. The link to Lambda is TIED inside the action by the Henneaux-Teitelboim unimodular multiplier (the hub's
  XR20, a075ad7f7). Under evolving dark energy, an action-level field tie reads sqrt(V), not sqrt(rho_DE) (FP0 L2a').
  In the khronon's own terms, a0 = (kappa/sqrt(24 pi)) c^2 K_inf with K_inf = sqrt(3 Lambda) the asymptotic expansion
  (XR30, 2a2d81f61). The khronon's CMC clock and the unimodular clock stay two structures (unimodular shape dynamics):
  the local count is unchanged and the global count gains one pair.
- The galaxy law P2, g_obs = sqrt(g_bar^2 + g_bar a0): an infrared law (FP0 R2).

## The action as it stands (per 1/16 pi G, c = 1)

The gravity core (FP7's AQUAL-type repair of the C-H/K root, with FP14's eliminations):

    R - 2 Lambda + alpha_c a^2 - 2 mu (K - <K>_h) + (2 - alpha_c) h^mn (2 a_m - D_m chi) D_n chi
      - 2 alpha^2 J_Y(h^mn D_m phi D_n phi/alpha^2) + [2 lambda (n.d phi)^2] + heat pair (chi = S_h phi) + S_m[g]

The cosmology separator is H_K1 (FP19), the well-posed repair of H_S (FP13, ill-posed as written; see errata). It reads the
state only through the leaf-averaged expansion <K>_h:

    chi = (S_xi - S_B) phi,   B = L^2/2,   L = L_Lambda 3 Lambda/<K>_h^2
    J_Y = J_P2(Y) + 2 y_th sqrt(Y),   y_th = max(0, 1 + Omega_r - 9 Lambda/<K>_h^2) (<K>_h^2/3 - Lambda) L/alpha   (c_y = 2)

with lambda > 0 required as a regulator (the yield vanishes below z = 0.635). The hub's re-audit XR18b (3c0cf3c37) finds it
linearly well posed and causal under criterion B, with FRW well posed across the q = 0 kink (the Newtonian psi-symbol is
>= +0.999982 at every sub-horizon k for z = 0-2.5); the particle-mesh run (XR21 stage 2a) proceeds on it. H_Y (FP9; four
declared constants) is the fallback. The dark sector is FK1's internal splitting (FP10), a
light complex scalar whose own rest energy powers the kick.

**Who feels MOND (FP22, adopted).** On the matter metric g, FK1 would source and feel chi like any matter (reciprocity),
and late-time web MOND would then be excluded by CMB lensing. The dark lanes (FP4, FP8, FP10, FP15, FP16) assumed instead
that the dark component feels Newtonian gravity only, via the L353 pair; that pair subtracts from C-H's field u, which FP7
removed, so it had no action on this root. The chain therefore puts FK1 on the root's own Einstein-frame metric

    S_Psi[g~],   g~ = g + (1 - e^(-2 chi)) n n

so that baryons source and feel the phantom and the dark component feels Newtonian gravity only. This is a POSTULATED
coupling with no new field and no new constant. Its price: dark-baryon free-fall universality is broken wherever chi != 0
(the L353 estimate: a median of 0.47 across X-COP's clusters). The Solar System and GW170817 are unaffected. The
merger/offset gates (Harvey, the Bullet cluster) must score it (OPEN).

## What is derived, and what is not (knob ledger; kappa = 1/2 accepted)

| sector | constant | status | lane |
|---|---|---|---|
| core | lambda (inertia) | REGULATOR in a DECLARED range 0 < lambda <= 0.03 (XR18b, 3c0cf3c37): only there are the MOND-regime observables lambda-independent (sigma_8 spread 3.6e-7; the tracking speed moves 1% at 0.061, galaxy alpha_2 v^2 at 0.030). Outside it lambda is a knob no datum picks (x9.6 and x93 across (0, 274.4], XR25). Required > 0 under H_S and H_K1 (below z = 0.635); eliminated under H_Y | FP14, FP13, FP19, XR25, XR18b |
| core | c_2 | ELIMINATED on Minkowski and FRW (c_2 -> infinity: a multiplier). At black holes the limit is not uniform: at c_2 = infinity with alpha_c > 0 the multiplier diverges logarithmically at the universal horizon (r = 3M/2), a curvature singularity at O(alpha_c); finite c_2 is regular. OPEN (XR25) | FP14, XR25 |
| core | alpha_c | REGULATOR (every observable moves <= 1.6e-9) | FP14 |
| core | xi (heat filter) | KNOB: irreducible by a threshold-mass theorem. MEASURABLE by Gaia DR4 wide binaries with a separation-resolved statistic: sigma(ln xi) ~ 0.20/0.15 at the floor, 91% of the information at 5-30 kAU. The frozen pre-registered statistic can only kill the chain from above (gamma_hat >~ 1.157/1.174); a Newtonian result only bounds xi > 0.036/0.047 pc (the hub's XR22, 661ea3cff, re-run pending) | FP17, XR22 |
| separator | L_Lambda | DECLARED in H_K1: 2.9 Mpc, inside the window 2.8-4.6 with the exact KiDS projector (FP20b; 2.65-4.6 before) (sigma_8 <= 1.02 needs <= 3.0); zero modes alone cannot give it (FP19) | FP19, FP20b |
| separator | n = 2, the q = 0 ramp, c_y = 2 | natural choices in H_K1 (c_y chosen after scoring: the only one of four natural normalizations passing both yardsticks); H_Y's y_Lambda and p' are gone | FP13, FP19 |
| dark | eps | IRREDUCIBLE (the only Z4-odd term; a khronon-frame coupling only relabels it) and FITTED (the flagship sets the window's lower end, Harvey its upper) | FP10, FP15 |
| dark | zeta (lambda_0), q, m | FITTED BY DATA: zeta's band is x1.16 wide at the mass floor; sharing q with the separator FAILS the web; m is pinned on the canonical footing, bounded on alt. The yield-onset trigger removes q but keeps zeta and adds a postulated gate form | FP15 |
| dark | cross quartic | POSTULATED (radiatively stable) | FP15 |
| dark | amount, misalignment | initial data (the amount has the status of LCDM's omega_c) | FP10, FP15 |

## Where the theory passes (beyond the galaxy law it embeds)

- The early universe (the hub's XR26, 68135cb7a, re-run pending): at z >~ 10 the linear equations derived from the full
  action reduce to GR + CDM up to alpha_c (G_cos = G_N (1 - alpha_c/2), no slip, the unimodular multiplier cancels from
  the comoving Poisson equation, the band-pass is closed at recombination); TT/TE/EE equal LCDM's to 7.8e-8; BBN is
  standard BBN. Load-bearing: the phi-dot = 0 initial condition (with lambda > 0, BBN needs Omega_phi,0 < 1.7e-25).
- The Solar System, c_T = 1, PPN gamma = 1 and alpha_3 = 0 (FP2); binary pulsars and GW170817 (XR25; alpha_2 sits on
  the isolated-MSP bound by construction, not by prediction); MW-M31 timing with baryons only (FP11).

## Where the theory fails or is undecided

- CMB lensing (XR26, re-run pending): below z ~ 0.64 the separator's yield vanishes and MOND switches on in the linear
  web; on FP13's per-mode yardstick C_L^phiphi rises x1.08/1.74/4.85 at L = 100/400/1000, and Planck's 8-400 amplitude
  (1.011 +- 0.028) becomes 1.149 on the linear base (+4.9 sigma) and 2.13 on halofit (+40 sigma); every variant scored
  fails. Passing needs the web's phantom cut to 0.62x (linear) / 0.18x (halofit). FP22 (bfe9a2fe5): with all matter
  feeling MOND it is EXCLUDED on every separator, yardstick and footing (real-space cut 0.52-1.35); with the adopted
  Einstein-frame coupling (baryons only) the real-space cut is 0.13-0.26 (H_K1 0.13-0.19): it passes Planck and ACT DR6
  on the linear base and fails ACT on the halofit base (>= 3.8 sigma). UNDECIDED until the nonlinear phantom is computed
  (the hub's XR21 stage 2a, reading "chain"). FK1's late conversion offsets only ~1.5% at L = 1000 (XR19).
- KiDS and the web's external field (FP22, a risk, not a result): in the baryons-only reading the web's band-passed field
  enters the kernel of an isolated lens at an estimated Delta chi^2 +205-232 with H_Y or H_K1 (all matter: +575-714), 6-8x
  over the field KiDS tolerates. No committed KiDS model includes that field; FP23 computes it.
- FK1's conversion alone, without the phantom (the hub's XR32, fa341733d, re-run pending): the survey-inferred S8 is
  0.752-0.766 (on KiDS-1000, DES Y3 and HSC Y3, ~2 sigma below KiDS-Legacy), but with a poor fit shape; its costs are
  cluster counts 0.64-0.81 of LCDM (5-9 sigma below eRASS1), DESI RSD -2.2 sigma, CMB lensing 0.976 (-1.6 sigma vs ACT
  DR6), and a lensing suppression equivalent to +0.098 eV of neutrino mass. These favour less late conversion or more
  cluster recapture, while X-COP (FP16) needs less recapture inside R500: a pincer for the dark sector (FP25).
- The Milky Way's outer curve (the hub's XR29, 633c161b5, re-run pending): the Gaia DR3 decline needs M_* = 7.3-8.2e10
  (4-5 sigma above the McMillan/Cautun censuses) and the 8-19 kpc slope misfits (-2.2 to -2.9 vs -1.7 km/s/kpc); LCDM's
  control needs a concentration 1.9-3.8 sigma above the c-M relation.

- The group-scale outer profile: R0 overshoots by +0.20 dex for the Local Group, M81 and IC 342 (Cen A matches); fixing
  it costs KiDS (FP11, FP12). FP18 finds the tension is in the data itself: at face value no profile fits both KiDS and
  the Hubble-flow R0 (9.8 sigma, LCDM included); six comparability systematics bring it to 2.3 sigma (UNDECIDED). FP21
  measured the lensing of 52 spectroscopically isolated late-type centrals (2M++ in KiDS-1000) at 0.26-1.62 Mpc: A =
  2.19 +- 1.46 of the mixed-type level, S/N 1.5; the reconciliation level (A ~ 0.3) is disfavoured at 0.8-1.8 sigma, a
  lean, not a result (UNDECIDED). Deciding it needs ~2,100 such centrals at z ~ 0.03: all-sky shear around 2M++.
- Re-accretion of the kicked dark component: FP16 (semi-analytic) finds the window EMPTY. Clusters recapture the escaped
  daughters, so X-COP fails at every kick from 575 to 650 km/s; the flagship, galaxies, KiDS and S8 pass. Only the hub's
  particle-mesh run (XR21 stage 3) could overturn it.
- The small-scale (sub-L) power boost and its cosmic-shear cost need the particle-mesh run (the hub's XR21). Under H_K1 the
  per-mode boost at z = 0 is +0.03/+0.14/+1.34 at k = 0.3/0.5/1 h/Mpc (FP19).
- H_K1's prices (FP19): KiDS for lenses at z = 0.7 comes out at +500/+524 with the exact projector (FP20b; +467/+496 before), a sharp prediction the data can test; the Local
  Group R0 still fails (1.41/1.46 Mpc). All of FP19's numbers are in the all-matter reading and use FP6's projection, so
  they are provisional until FP20 and FP22.
- Nonlinear well-posedness (XR18b, OPEN): cold-matter growth is resolution-dependent at H_K1's yield surfaces (190-374 H
  at xi) and, below z = 0.635, at every zero of the band-passed field (halo centres, web saddles); the nonlinear
  free-boundary problem is open. Far from an isolated host (13.6 Mpc at z = 0.25, band-passed field ~1e-24 a0, no yield)
  DE12's convention gives up to 1.4e5 H; embedded in the web's own field it is 0.
- Strong lensing (the hub's XR33, 92fe59705): SLACS ellipticals from baryons plus the phantom need a stellar IMF
  0.118 +- 0.013 dex above the spectroscopic relation (CvD12's heaviest); the phantom supplies only 9.5-11% of the
  Einstein mass (g_N ~ 9-11 a0). LCDM's own IMF for the same lenses is off by +0.021 dex.
- No-go results that constrain any repair: local gates (FP3 lemma), the MOND-sector kick (FP4, FP8 reciprocity), and
  xi from (a0, Lambda, G, c) (FP17 theorem).

## Errata

- **FP13 A1 is WRONG at the action level** (corrected by the hub's XR18 N3, 53854a459). The leaf-averaged state term
  does add a local term. Through the O(V) leaf integral, dS/d delta is an O(1) local force with coefficient R_B ~ 7-8 at
  z <= 0.635, so the psi-constraint symbol k^2(1 - R_B) changes sign on k = 0.12-1.62 h/Mpc. H_S as written is linearly
  ill-posed. FP19 carries the correction in its ledger and tests the repairs (stationary B, a <K>_h-only readout).
- **FP9's H_Y fails KiDS at z = 0.4** (+20.6; found by FP13). Its z = 0.25 KiDS pass stands.
- **FP6's KiDS projection `esd_of_M` under-projects** (found by FP18; fixed and re-scored by FP20, 7a8c25321). It
  treated the inner projected mass as a flat disc and skipped the Abel integral's 1/sqrt end interval: -59% at 35 kpc and
  -4 to -14% outside on a singular isothermal sphere. The record's other projector (L352's `project_M2`, DE8's
  `esd_from_mlens`) shares the end-interval defect and is badly off on cored/hollow carrier templates (+187% / -123% at
  35 kpc). With the exact projector (< 0.04%) none of the chain's deciding KiDS verdicts flips: FP6, FP9 (z = 0.25),
  FP11, FP12 K7 and FP13 (z = 0.25, 0.4) still pass; FP9 at z = 0.4 still fails; the KiDS-LG pincer stands. What flips:
  L360's passing pairs (70 -> 35 of 96), FP13's A3 window edges, FP11 P1's band edge (now passes). FP15/FP16 (L352's
  projector) and FP19 (the old one) were committed before the fix; FP20b (3924bb8c2) re-scored them: no headline verdict
  flips (FP16's KiDS passes hold at every kick; H_K1 passes at z = 0.25 and 0.4; its L_Lambda window narrows to 2.8-4.6).
- **The dark lanes' "Newtonian-only" dark component had no action on this root** (found by FP22): FP4, FP8, FP10, FP15
  and FP16 used the L353 kernel-invisible pair, which subtracts from C-H's field u, removed by FP7. Their dynamics are
  realised by the Einstein-frame coupling FP22 identified, now adopted (see "Who feels MOND"). FP7's sigma_8 failure used
  the all-matter reading; in the adopted reading the no-separator sigma_8 still fails (real-space 1.45/1.51), so a
  separator stays needed.
- **The record's forest particle-mesh codes** (L346, L347, L362, DE11, DE11b) pass (1+z) times the physical field to the
  MOND kernel, so MOND is evaluated about sqrt(1+z) too weak in the deep limit at z = 2-3 (the hub's XR21 flag, confirmed by
  FP22; the hub's XR34 re-scores DE11b). The chain's own forest proxies (FP9, FP13) use the physical field.
- **FP19's "the <K>_h read acts at k = 0 only" is wrong** (XR18b): its second variation is a local operator at every k.
  It is harmless: the constraint determinant is identical with and without it (|eps_C| <= 9.1e-6, rho_extra/rho_bar <=
  2.6e-5). FP19's "lambda any value <~ 100" is also wrong at c_2 = infinity: lambda must be declared <= 0.03.
- **FP14's "sigma_8 unchanged for lambda = 0-100"** was measured at the c_2 floor, where lambda_eff = lambda + 277 (the
  hub's XR25, 43cfa1692). At that floor the lambda window is empty, so a required lambda > 0 (FP13, FP19) needs
  c_2 > 7.289e-3; FP14's "c_2 -> infinity is regular" holds on Minkowski and FRW but not uniformly at black holes.
- **FP16's MUTATE banner** names R1, G3 and G9 as the flips; the observed flips are R1, G7 and G9 (without recapture
  X-COP fails on the other side, which G3 does not distinguish). Wording only; no number changes.
- **Numerology is flagged, never claimed:** eps/m^2 = kappa^19 (FP10); (c^2/a0)(32 pi)^-6 = 0.030 pc and
  ((hbar/m)^2/a0)^(1/3) (FP14, FP17); (hbar c/G)^(3/2)/m_p^2 (FP17).
