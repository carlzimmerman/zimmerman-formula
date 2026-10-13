# CFG653: the filter length of astra's nonlocal response CANNOT be derived from the framework, and no constant length passes R7

Criteria d44fee295 (committed alone, before any script or number). Scripts: `cfg653_core.py` (spherical solver),
`cfg653_filter.py` (parts K, A, B, C; `--mutate`). Outputs: `cfg653_filter_{K,A,B,C}.out` and `_results.json`, plus
`_MUTATE_{A,B}`. kappa = 1/2 FITTED. Both footings are scored separately and never pooled. Cold energy. Not theory closed.

**Object (astra, read as data).** `sol61_push/nonlocal_response_2026_10_12`:
div{q - P_L[p(|z|) z/|z|]} = 4 pi G rho_b with z = P_L q and P_L = 1 - (Gaussian smoothing of width L). It is exactly blind to a
uniform added gradient for every L. L is the open input. Here it is reimplemented exactly for spherical sources in R^3: the
filter acts on m = r^2 g through the analytic enclosed fraction of a smoothed shell.

## Per-candidate verdicts

| candidate | L | (a) SPARC RAR rms, can / alt (local 0.1003 / 0.0991) | (b1) cluster satellites chi2/5, can / alt (p >= 0.01 needed) | (b2) wide binaries gamma_hat, z vs DR3, can / alt | (c) well-posed | verdict |
|---|---|---|---|---|---|---|
| C1 r_M = sqrt(GM_b/a0) | 0.3-32 kpc (SPARC) | **0.359 / 0.374 FAIL** (41 / 53 repulsive points) | primary (cluster, f_b 0.1/0.2; L 270-420 kpc): **59.9-75.9 / 50.3-67.3 FAIL**; own: 131 / 131 FAIL | MW (9.5 kpc): 1.240 (+2.1) / 1.324 (+3.4) TENSION; LG: 1.195 (+1.6) PASS / 1.263 (+2.5) TENSION; own: 0.924 (-2.6) / 0.903 (-2.9) | variational, convex; **c3 CONDITIONAL** (merger moves the outer RAR by 0.51 / 0.49 dex) | **FAILS (a, b1)** |
| C2a c^2/a0 | 3.11e7 / 2.57e7 kpc | 0.1003 / 0.0991 PASS | **98.7 / 94.6 FAIL** (f_res = 1.000: the local EFE) | 1.179 (+1.3) PASS / 1.244 (+2.3) TENSION | **c4 FAIL**: 3.37 L = 19.5 / 16.1 l_dS | **FAILS (b1, c4)** |
| C2b l_dS = c/H_Lambda | 5.38e6 kpc | 0.1003 / 0.0991 PASS | **98.7 / 94.6 FAIL** | 1.179 (+1.3) PASS / 1.244 (+2.3) TENSION | **c4 FAIL** (3.37 l_dS) | **FAILS (b1, c4)** |
| C3a r_ta (CFG4's) | 0.31-2.9 Mpc (SPARC); cluster 10-13 Mpc | 0.1003 / 0.0991 PASS | cluster: **98.7 / 94.6 FAIL**; own (0.9-2.3 Mpc): **97.1 / 93.1 FAIL** | MW/LG: 1.179 (+1.3) PASS / 1.244 (+2.3) TENSION; own (4 kpc): **1.50 pinned (+7.7 / +8.3) FAIL** | PASS (c3 jump 0.0000 dex) | **FAILS (b1)** |
| C3b r_zg (law + rho_DE only) | 0.5-5 Mpc (SPARC); cluster 17-21 Mpc | 0.1003 / 0.0991 PASS | cluster: **98.7 / 94.6 FAIL**; own: **98.2 / 94.2 FAIL** | MW/LG: PASS / TENSION as above; own: 1.333 (+3.1) / 1.394 (+4.1) TENSION | PASS | **FAILS (b1)** |
| C4 singled out by astra | none | - | - | - | - | **none exists** (L enters only through H(k)) |

**No candidate is DERIVED-AND-PASSES.** Every candidate fails the cluster-satellite gate on both footings. The universal ones also
fail static causality.

## The constant-L window (C4 diagnostic): EMPTY

| L (kpc) | 1 | 3 | 10 | 30 | 100 | 300 | 1e3 | 3e3 | >= 1e4 |
|---|---|---|---|---|---|---|---|---|---|
| SPARC rms can | 0.323 | 0.335 | 0.318 | 0.232 | **0.1002** | 0.1003 | 0.1003 | 0.1003 | 0.1003 |
| satellites chi2 can | 132 | 132 | 132 | 575 | 495 | **60.0** | 94.5 | 98.3 | 98.7 |
| binaries z can / alt | +7.7 / +8.3 | +7.7 / +8.3 | +2.0 / +2.9 | +1.4 / +2.3 | +1.3 / +2.3 | +1.3 / +2.3 | = | = | = |

- SPARC needs L >= ~100 kpc. Binaries need L >= ~30 kpc so the MW field is kept. Below that they become EFE-blind and are
  excluded at 7.7 / 8.3 sigma, the CFG447 value. On alt, even the full local EFE sits at +2.3 (TENSION), so every L is TENSION there.
- **No L passes the satellites.** The frozen best is chi2 60.0 / 55.3 at 300 kpc. The POST-HOC finer scan (120-250 kpc, labelled)
  bottoms out at L = 120 kpc with chi2 20.6 / 17.6 (p = 0.0009 / 0.0035), still below p = 0.01. That uses the OPTIMISTIC min()
  combination; letting the two suppressions compound can only make it worse.
- So a tuned knob cannot rescue the construction either. The window is empty for a structural reason. The host field (NFW, not
  harmonic) leaks through the high-pass as f_res ~ (L/R)^2 (0.03 at 100 kpc, 0.29 at 300 kpc, for R = 0.66-0.93 Mpc). But the
  satellite's own field must pass the filter out to r_bg = 36-149 kpc, and r_bg/R is only 0.05-0.2. Astra's scale-separation bound
  (k_g/k_e >= 8.4) is violated by the data's own geometry.

## Structural findings (these hold for every L)

1. **Direction of the limits.** In astra's convention, L -> infinity is the LOCAL response, with the full EFE from any host at
   finite distance; only an exactly uniform gradient drops out. L -> 0 is NEWTON. The brief's MUTATE wording had them reversed.
   No member of this family has a local L -> 0 limit. This was disclosed in the criteria before any number.
2. **The phantom has zero total mass.** H(0) = 0, so the effective density's monopole vanishes. For r >> L the curve returns to
   Keplerian and then OVERSHOOTS: the boost drops below 1, and repulsive points appear (C1: 41 / 53 SPARC points; the
   MW-mass boost at 3 r_M is 0.68). Flat curves exist only for r << L.
3. "Uniform-gradient blind" does not mean "EFE-free". Real host fields are not uniform. A non-harmonic host leaks as
   (L/D)^2, not exponentially.

## Controls and MUTATE

- K1: CFG4 reproduced exactly: 0.1003 @ 0.61 / 0.0991 @ 0.57, both algebraically and through the solver at L = infinity.
- K3: CFG478 Q1 reproduced: 98.68 / 94.62.
- K4: CFG447 EFE-blind reproduced: 10/10 pinned, +7.7 / +8.3. The pipeline sha256 was unchanged.
- c2: the variable-width filter 1 - exp(div(L(x)^2/2) grad) is self-adjoint, annihilates constants, and has 0 <= P <= 1. So the
  convexity bound carries over for system-dependent L.
- **K2, frozen node, FAILS at L = 4.** Spherical vs astra's own 3D solver (N64, box 128, dx 2) gives 6.6% against a 3% tolerance.
  It passes at L = 8 (2.7%) and for local (0.6%). A post-hoc refinement at L = 4 shows the gap is 3D discretisation:
  6.3% (dx 2) -> 3.6% (dx 1) -> 2.0% (dx 0.5), converging onto the spherical solver. Local: 0.74% -> 0.24% -> 0.24%.
- M3: astra's uniform-gradient invariance re-run in 3D: max change <= 1.2e-16 at every L.
- MUTATE: DETECTED on both footings. M1 (L = 1e12 kpc) gives the local law's SPARC rms to 1e-6 dex, f_res = 1.000 for the cluster and MW hosts, and the local-EFE satellite chi2 (98.7 / 94.6). M2 (L = 1e-6 kpc) gives Newton's rms exactly (0.2755) and satellite self-boosts of 1.00.

## Caveats

- Spherical-equivalent sources: SPARC enters as m_N = r^2 g_bar, the statistic's own convention, which L -> infinity reproduces exactly.
- In the satellite gate, B_EFE is CFG478's QUMOND enclosed phantom with the host field scaled by f_res. In the binary gate, the
  pipeline's EFE-saturated shape is replaced by the exact enclosed boost.
- In the frozen binary gate, z <= 2 is one-sided. C1-own's sub-Newtonian 0.92 / 0.90 (z -2.6 / -2.9) therefore "passes" as
  frozen, but it is a 2.6-2.9 sigma deficit. It does not change C1's verdict.
- r_ta uses CFG4's rho_m (Omega_m = 0.3153) and Delta_ta = 11.81, which are cosmological inputs; this is flagged. r_zg avoids them,
  and the verdict is the same.
- Context, not a gate: every candidate that keeps the MW field (L >= 30 kpc) predicts gamma ~ 1.18 / 1.24 for wide binaries.
  That differs from the sealed DR4 prediction (exactly Newtonian, Amendment 21). Adopting this field would change that prediction.
