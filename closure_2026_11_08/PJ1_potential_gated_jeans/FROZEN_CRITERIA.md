# PJ1: potential-gated biharmonic Jeans scale for the K(Q) component. FROZEN CRITERIA (committed alone, before any number)

Lane class: TEST (owner decision closure_2026_11_08/OWNER_DECISION_2026-11-08_PJ1_LAUNCH.md). Adopts nothing.

## Mechanism under test (as proposed; graded as written, then at its best point)
Add to the K(Q) sector a spatial fourth-derivative term -(M_Pl^2/2) xi(Q) (h^{mu nu} grad_mu A grad_nu A) with
A = divergence of the khronon acceleration (= grad^2 Phi / c^2 in the weak field), xi set by the lapse so that the
component's local Jeans scale and source weight are gated by potential depth:
  R_J(Phi) = R_J0 / (1 + (|Phi|/Phi_*)^p)^(p/2),      S(Phi) = R_cmb * (|Phi|/Phi_*)^p / (1 + (|Phi|/Phi_*)^p),
  [1 + R_J^4 grad^4] rho_K = rho_b S(Phi),             M_K(<r) from rho_K; law applied to g_source = G (M_b + M_K)/r^2,
with the disc correction g_eff = g_source [1 - ell_theta^2 grad^2 ln(1 + g_source/a0)].
Proposed values (the AS-WRITTEN point): R_J0 = 1.4 Mpc, Phi_*/c^2 = 1.5e-6, p = 2, ell_theta = 1.5 kpc, R_cmb = the
record's F1A ratio (5.41; the proposal's 4.4 is a misreading and is graded as a reported alternative, not the primary).
NOTE: the proposal's text gives R_J(Phi) = R_J0 (1 + |Phi|/Phi_*)^(-p/2) while its code gives the form above; both are
graded, named form T (text) and form C (code). The lane also scans R_J0 in [0.3, 10] Mpc, Phi_* in [3e-7, 3e-5], p in
{1, 2, 3}, ell_theta in {0, 1.5, 3} kpc (coarse grid, declared) and reports whether ANY point passes every gate.
Both footings (a0 1.2e-10 / 1.1e-10) graded separately, never pooled. Phi is the self-consistent depth including M_K,
integrated from the law's potential to r_EFE (framework-native), not a LambdaCDM halo potential.

## Gates
- G1 SPARC (record gate, as BG1 G1): rms not above law-only + 0.010 dex, |mean| <= 0.05; G1b massive tail v_flat >= 250
  km/s alone, same bounds; G1c AGC 114905 and Malin 1 with ell_theta: report chi^2 vs the law-only value (informational).
- G2 KiDS isolated lenses (Brouwer 2021, 59 points; QX7 iter_4 FROZEN_CRITERIA.md:26): |shift| <= 0.05 dex in every
  g_bar bin, including the outermost bins (0.3-1.5 Mpc), stacked with the lenses' own depths.
- G3 X-COP (|mean| <= 0.05, rms <= 0.10 over 50 kpc-r500) with rho_K from the biharmonic solution sourced by gas + BCG;
  shape graded as in QX7 iter_7 (need more concentrated than gas).
- G4 Groups (Lovisari 20): >= 16/20 in the need band. G5 Coma UDGs (EV1 gate): within 2 sigma of the need.
- G6 Bullet: the component's centroid must sit within the lensing-peak offset band on the galaxies' side, not the gas's
  (record Bullet gate; NOT EVALUABLE if no framework-native merger model, name it).
- G7 Primary CMB (F1A machinery): the component's clustered weight at z 1100 is scale-dependent, S(Phi(k)) with Phi(k)
  the linear potential at recombination; Delta chi^2 vs the constant-weight F1A fit <= 10 on raw Planck TT/TE/EE
  bandpowers out to ell 2500. (The orchestrator's hand estimate: S falls from 0.99 at peak 1 to ~0.6 at ell 2000.)
- G8 Growth and lensing (QX3 ODE, raw PR4 lensing Delta chi^2 <= 4; raw fsigma8 within 2 sigma) with the k^4 cutoff at
  R_J0 and S(Phi) on the linear web. G9 Forest (NC2 gate). G10 Solar System / Cassini with the biharmonic term at the
  Sun's depth (KT16 Cassini gate), and c_T = 1 (spatial-only term; state it).

## Label rule
PASS on a footing iff one grid point (or the as-written point) passes G1-G10. FAIL iff none does. NO VERDICT only for a
NOT EVALUABLE gate named by its missing framework-native input.

## MUTATE (must bite; separate *_MUTATE.json)
- M1 gate inverted (S large where |Phi| is small): must FAIL G1/G2. M2 S -> 0: must FAIL G3. M3 R_J0 -> 10 R_J0 at the
  best point: must flip G2 or G8. KA replay: criteria hash in every output; x10 on Phi_* must flip a gate.

## Operational
Preemptible, RSS < 1 GB, no edits to other lanes' files, outputs under this directory, explicit-path commits, push via a
temp worktree. Message "Theory completion": "PJ1 RESULT: <label can / alt> (criteria <hash>, result <origin hash>)".
