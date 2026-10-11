# CFG630: settling energy feeds dark energy. Prediction: a phantom-side trickle of ~1e-6 in rho_DE since z = 1. BELOW SENSITIVITY by 4-5 orders of magnitude.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (45dd454a6). Date: 2026-10-11.
- **Script:** `cfg630.py`. It takes about 2 min with `OMP_NUM_THREADS=1 nice -n 10 python3 cfg630.py`, one process, well under 1 GB. It writes `cfg630.out`, `cfg630_results.json` and `cfg630_prediction.png`. `CFG630_MUTATE=1` writes `cfg630_MUTATE.out` and `cfg630_results_MUTATE.json`. Both runs exit 0 and every frozen check passes.
- **Settings:**
  - κ = ½ is FITTED. It cancels in the a₀ ratio.
  - The two footings, 9.3603e-11 and 1.1312e-10, are never pooled.
  - Candidate B; class-A overdamped sink (CFG542 Pb); w_b = −1 background.
  - The cold energy's MASS is required. No particle species is added.
  - This is not "theory closed", and nothing here says the data favour the framework.
- **Numbers:** every number below comes from the two JSON files. Ranges cover the declared α bracket [0.5, 1.186].

## What this lane adds to CFG541/542/549/557
CFG549 R1 used CFG541's E_sink with instantaneous settling. This lane uses three later pieces of the record:
- CFG542's derived sink. In the overdamped runs it takes the WHOLE potential drop: Q/ΔW = 1.0004–1.0009, and c_W = ΔW/(M_cat V_f²) is 0.77 (MW) to 0.99–1.01 (cluster).
- CFG557's rate-limited catchment s_c(M, t; α), with capture time r_e/(αV_f).
- Census f_ret baryons.

These give the cosmic settling power

U(t) = ρ_c0 ∫ dlnM f_ta(M,t) s_c(M,t;α) c_W V_f², with Q = a⁻³ dU/dt.

Q is fed into d(ρ_DE c²)/dt + 3H(1 + w_b)ρ_DE c² = +Q, with w_b = −1 and ρ_DE(t0) fixed at the measured input. The matter sector loses the same energy as binding energy. The first law closes to 4e-12 of U(0) (K3).

**Sign convention.** Q > 0 means energy flows from the settling cold energy into dark energy.

## The prediction (primary: PS turnaround barrier, M_min 1e8 M☉/h; HMF context)

| | canonical | alt |
|---|---|---|
| Q today | 7.4–7.9e-34 W/m³ (6.5–6.9e-7 H0 ρ_DE0 c²) | 8.5–8.9e-34 W/m³ (7.4–7.7e-7) |
| settled fraction of all cold energy today | 0.505–0.547 | 0.512–0.549 |
| Δρ_DE/ρ_DE0 since z = 0.5 | 4.4–4.8e-7 | 5.1–5.5e-7 |
| since z = 1 | 0.98–1.10e-6 | 1.12–1.25e-6 |
| since z = 2 | 1.81–2.12e-6 | 2.10–2.41e-6 |
| since z = 3 | 2.24–2.70e-6 | 2.60–3.07e-6 |
| total since z = 8 (≈ all of it) | 2.7–3.4e-6 | 3.1–3.8e-6 |
| 1 + w_DE(0) | −2.2 to −2.3e-7 | −2.5 to −2.6e-7 |
| CPL, DE-own ρ_DE(z): (w0+1, wa) | (−2.2..−2.3e-7, −0.8..−1.1e-6) | (−2.5..−2.6e-7, −1.0..−1.2e-6) |
| CPL, observer's effective DE | (−2.3..−2.6e-6, +1.3..+1.4e-5) | (−2.7..−3.0e-6, +1.5..+1.6e-5) |
| CPL, H(z)-fit | (−4.4..−4.9e-7, −0.7..−0.9e-6) | (−5.0..−5.5e-7, −0.8..−1.05e-6) |
| a₀(z)/a₀(0) − 1 at z = 1 / 2 / 3 | −4.9..−5.5e-7 / −0.91..−1.06e-6 / −1.12..−1.35e-6 | −5.6..−6.2e-7 / −1.05..−1.20e-6 / −1.30..−1.54e-6 |
| in dex at z = 1 / 2 / 3 | −2.1..−2.4e-7 / −3.9..−4.6e-7 / −4.9..−5.9e-7 | −2.4..−2.7e-7 / −4.6..−5.2e-7 / −5.7..−6.7e-7 |

The "observer" CPL is larger than the DE-own one. That is bookkeeping: matter loses U/c², which shows up as a⁻³-diluted energy.

Every quantity rises monotonically with α across the bracket. α only delays settling: the time-integrated energy depends on α only weakly, and α → ∞ (the free-fall ceiling) adds about 10%. Q peaks near z ≈ 2 in physical units, at about 8e-33 W/m³.

**Brackets** (Δρ/ρ0 since z = 1, over PS/ST × M_min {1e6, 1e8, 1e10} × α):
- canonical 0.80–1.10e-6;
- alt 0.92–1.25e-6.

Outside the bracket, α = 2 gives 1.14 / 1.28e-6 and the α = ∞ ceiling gives 1.19 / 1.34e-6.

**Native-anchored variant (context).** The framework PM's own switch-on mass fraction (CFG424 TA boxes) is 0.35–0.73 of route H's catchment above the PM resolution (K6). The two counts are different objects: switch-on cells versus turnaround balls. Rescaling to the PM gives about 4e-7 since z = 1. So the native count sits at the low end, a factor of about 2.5 lower.

## Verdicts (frozen rules)

**1. TESTABILITY: BELOW SENSITIVITY.** The largest predicted effects anywhere in the bracket, on either footing, are:
- max |1 + w0| = 3.0e-6, which is 5.4e-5 of σ(w0) = 0.055;
- max |wa| = 1.6e-5, which is 7.7e-5 of σ(wa) = 0.21;
- max |Δlog a₀| at z ≤ 3 = 6.7e-7 dex. That is 9.5e-5 of the 0.007 dex per-bin precision CFG549 R2 asks for, 3.3e-5 of the 0.02 dex the record calls unseparable (CFG571), and 4.4e-6 of the 0.15 dex per-disc floor.

The DESI σ values are DR2 context only; they are not a yardstick for the model. Seeing the z = 2 drift statistically at 0.1 dex per disc would take about 4e10 discs, before any systematic floor. The sealed CFG570/571 ALMA predictions are unaffected: settling moves a₀ by about 1e-7 of the F-DESI vs F-flat difference they already cannot separate.

**2. SIGN: PHANTOM-SIDE.**
- Q ≥ 0 at every z. Class A is one-sided, and the ratchet never had to bind.
- So ρ_DE grows toward today, a₀ was slightly smaller in the past, and 1 + w_DE = −q ≤ 0, where q = Q/(3Hρ_DE c²) ≤ 9.9e-7.
- There is no crossing of −1.

**3. Canonical partner.**
- CFG542's φ obeys φ̈ + 3Hφ̇ + V′ = Q/φ̇. This is singular at φ̇ = 0, which is w = −1.
- The source is a small perturbation only where the field's own 1 + w_φ ≫ q ~ 1e-6. There the observed w_eff = w_φ − q.
- So a canonical partner can show w_eff < −1 only inside a band |1 + w| ≲ 1e-6 around −1. With w_φ exactly −1 it is singular.
- Two conclusions follow:
  - the settling sink cannot produce, or rescue, an O(0.1) crossing of −1 like the one in the DESI chains;
  - the phantom-side trickle needs either a non-canonical receiver or a canonical partner that already sits at 1 + w_φ ≫ 1e-6, in which case the trickle is a negligible correction to w_φ.

**4. CFG511 fork.** Whether a₀ tracks −p_DE or ρ_DE changes the prediction by ≤ 1.6e-7 dex. The fork stays undecidable on settling alone.

## Scope note: the local hand-off is not validated here (orchestrator note, 2026-10-11)
astra's `sol61_push/local_sink_reaction_2026_10_11/REPORT.md` (b626126ed) shows the following. Depositing a spatially varying settling power into PURE vacuum (T_v = −V g) forces a matter force density +∇V. That reaction is order-one relative to halo gravity, even when the deposited energy is only ~1e-7 of rest energy.

This lane's cosmic ledger Q(z) is a volume average. It neither bounds nor validates that local hand-off. The homogeneous w(z) and a₀(z) results above ASSUME a receiver whose local reaction is supplied by a dynamical partner: CFG542's scalar φ, with its w = −1 singularity (verdict 3). They are **not** evidence that a passive-vacuum sink is consistent. A homogeneous Q is the explicitly allowed control in that report, and it is the only thing computed here.

## Controls and MUTATE
- **K0:** the analytic age equals cfg557_lib's to 2e-16.
- **K1:** PS normalisation 1.000000. ST is 1.0001, reported only.
- **K2:** ODE versus quadrature agree to 9.8e-11 (PASS ≤ 1e-9).
- **K3:** first law 4e-12 of U(0).
- **K4:** the maximum over all variants, 5.87e-6, is below the ceiling 6.52e-6 (all cold energy at the cluster ε_W).
- **K5:** the CPL projection of exact Λ returns (−1, 0).
- **K6:** native comparison, reported above.
- **MU1, α = 0:** max |Δρ_DE| = 0, max |a₀ ratio − 1| = 0 and max Q = 0, all exactly. PASS.
- **MU2, settled mass × 2:** Q and Δρ scale by exactly 2 (deviation 0). PASS.

## Inherited ingredients (flagged; none used as a yardstick)
- The excursion-set mass fraction on the turnaround barrier (PS primary, ST bracket), with Gaussian ICs.
- The PM's Eisenstein–Hu input spectrum (σ8 0.811) and flat matter+Λ linear growth.
- cfg557_lib's spherical-collapse t_reach (with a Λ term) and its EPS main-progenitor history (PROVISIONAL).
- DESI DR2 Gaussian σ values, read from CFG549's committed JSON; context only.

So the prediction carries the label **HMF context**.

## Disclosures
1. **s_c deviates from CFG557 in one place.** s_c re-uses CFG557's iteration. Only a converged "nothing captured" state reads as 0; CFG557 reports its 0.02 grid floor there.
2. **Post-first-run fixes.** No criterion was changed.
   - The first version made s_c = 0 absorbing at an intermediate iterate. That killed real fixed points: α 0.5, z 2, log M_ta 12 gave 0 instead of 0.210. It is fixed to CFG557's restart.
   - K2 first read 1.21e-9, above its 1e-9 limit, because the integrator stepped across the interpolation knots. The ODE is now integrated knot to knot.
3. **ε_W at partial settling.** ε_W uses CFG542's full-settling ΔW per catchment mass at every settled fraction. c_W spans ±13%.
4. **U(t) is a state function** of the halo population. Re-settling after mergers is not tracked separately.
5. **Background feedback is neglected.** The background H is the input matter+Λ one, and the feedback of a ~1e-6 change is neglected.
6. **Comparison with CFG549.** The total since z = 8 (2.7–3.8e-6) exceeds CFG549 R3f's scaled ≤ 2.6e-6. CFG549 used a collapsed-mass ST fraction with instantaneous settling; this lane uses turnaround catchments, CFG557's s_c and c_W V_f². Both sit about 4–5 orders below any sensitivity.
