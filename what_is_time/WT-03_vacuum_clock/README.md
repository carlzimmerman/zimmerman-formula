# WT-03 — the vacuum clock: which way and how fast does a0 run in cosmic time?

**Criteria:** `FROZEN_CRITERIA.md`, committed alone first in **c9ea722b6**. Amendment A1 (`AMENDMENT_A1.md`, after the run): Branch
A, rival viability, the stage-17 scope note, and a post-hoc script.
**Input:** CFG689 primary band, `cfg689.json` @ 6c064b83a (read only).
**Standing:** κ = ½ FITTED. Z = 5.7888. Footings 9.3603e-11 / 1.1312e-10, never pooled. Cold energy is real mass, with no
particle. Not theory closed. **Nothing here says the data favour the framework.** The NEC demand below is a property of the
measured ρ_DE(z): any model with this background inherits it, ΛCDM with free dark energy included.

## Two branches on record, never pooled
- **Branch A (unimodular; CFG6, "keep A as the framework's prediction").** a0 reads the HT integration constant, so it is exactly
  flat for any dark-energy history: d ln a0/dt ≡ 0. **The vacuum clock has no direction and no rate.** This is an IDENTITY, with
  no verdict weight.
- **Tracking reading** (owner rule 10-06; THEORY_CANONICAL §3.8). a0(z)/a0(0) = √(X(z)/X(0)), with X = ε, −p or V (CFG911).
  Everything below is about this branch.

## (a) The band: exact keys
- `BAO+SN.P1.<z>.sqrtX_q` (z 1.0/1.2/1.5/2.33; percentiles 2.5/16/50/84/97.5): 0.913 [0.762, 1.027], 0.925 [0.762, 1.048],
  0.942 [0.706, 1.115], 0.909 [0.325, 1.212] (median [68%]).
- `BAO+SN.P3.a0_node_q`, `BAO+SN.posterior.node_mean/node_std` for the six nodes (0, 0.4, 0.7, 1.0, 1.5, 2.33), plus
  `P3.H0_q`, `P1.E_q` and `P3.P_w_le0`.
- No samples or node covariance are stored. Node draws therefore use the declared **APPROX-G**: a Gaussian per node, with
  adjacent correlation ρ_adj ∈ {−0.5, 0, +0.5}.

## (b) What a rising a0 demands (sympy, K4 PASS)

| reading | d ln a0/dt > 0 requires | d ln a0/dt < 0 requires |
|---|---|---|
| ε | w < −1: **NEC violation, always** (= −(3/2)H(1+w); CFG911 K17 reproduced) | w > −1 |
| −p | c_a²(1+w) > 0. With NEC this means c_a² > 0, i.e. ρ″ > 2ρ′/(1+z). For a canonical scalar, d(−p)/dt = 2V′φ̇ + 3Hφ̇² > 0 (field faster than slow roll, or climbing). **Healthy is possible.** | c_a² < 0 with NEC (e.g. slow-roll thawing) |
| V (canonical scalar, Klein–Gordon) | V′φ̇ > 0: the field **climbs**. φ̇² must then fall (transient). Needs ρ′ ≥ 0 and ρ″ > 5ρ′/(1+z). **Healthy is possible, but only transiently.** ρ′ < 0 needs a ghost (K = (1+z)ρ′/6 < 0) | field rolls down (V′φ̇ < 0) |

**S4 (true by construction):** inside a CFG689 segment ρ″ = 0, so all three readings drift with sign(−ρ′). The node band does
**not** measure the ρ″ that separates −p and V from ε.

## (c)/(d) VERDICT (frozen rules; literal = CFG689's own linear w(z); class at ρ_adj = 0, bracket ±0.5 gives the same class)

| reading | 68% | 95% |
|---|---|---|
| ε | **PHANTOM-REQUIRED** | **NOT DIAGNOSTIC** |
| −p | PHANTOM-REQUIRED (inherited from ε by S4; RECONSTRUCTION-DEPENDENT: spline gives FALLING) | NOT DIAGNOSTIC |
| V | PHANTOM-REQUIRED (inherited by S4; ghost for a canonical scalar; spline gives HEALTHY) | NOT DIAGNOSTIC |

- **Where the demand comes from:** the single segment z 0.7 → 1.0 (6.4–7.8 Gyr ago).
  - f_NEC = P(ρ_DE falls with z) = 0.888 (0.842 / 0.952 across the bracket).
  - w_eff = −1.84 [−2.66, −1.14].
  - a0 rose there at +0.145 [+0.024, +0.300] per Gyr.
  - The other four segments are FLAT at 68%. Every net interval [0, z] (stored quantiles, z 1.0–2.33) is FLAT at 68% and at 95%:
    P(net rise from z to today) is only 0.62–0.78. **"a0 smaller in the past, rising toward today" is NOT established.**
- **Knife-edge.** At ρ_adj = −0.5, p_rise = 0.84149 against 0.8413, which is 0.3 Monte-Carlo σ from the line. The 68% class is
  lost below ρ_adj ≈ −0.50 (PH1, post hoc).
- **Arrow.**
  - 68%: RISING-ONLY at ρ_adj 0 and −0.5 (DIRECTION SEEN, MONOTONICITY NOT ESTABLISHED). At +0.5 it is a TURNAROUND, a PEAK at
    z = 0.7 (6.4 Gyr ago), with NO GLOBAL VACUUM ARROW. This is CORRELATION-SENSITIVE.
  - 95%: FLAT, so NO VACUUM CLOCK MEASURED.
  - P(the a0 maximum sits at node 0.7) = 0.47.
  - By construction, a0 runs only through ρ_DE(a(t)). Any direction it has is the expansion's direction read through dark
    energy, not an arrow of its own. Under ε its direction flips exactly where w crosses −1.
- **Does any reading allow a rising a0 with healthy minimal dark energy?** In theory: −p yes (convex ρ), V yes (transient
  climb), ε never. On this band it cannot be tested, because ρ″ is unmeasured. The literal reconstruction makes all three equal
  (S4). The spline rows (sensitivity only) give −p FALLING and V HEALTHY at 68%: different reconstructions give different answers.

## (e) Rate today (mean background H0 = 67.70 → 0.06924 Gyr⁻¹)

| | d ln a0/dt median | 68% | in H0 |
|---|---|---|---|
| ε (literal) | −3.2e-12 /yr | [−1.66e-11, +9.1e-12] /yr | −0.047 |
| −p (literal) | −2.2e-12 /yr | [−1.32e-11, +5.6e-12] /yr | −0.032 |
| V (literal) | −2.7e-12 /yr | [−1.51e-11, +7.3e-12] /yr | −0.039 |
| ε (spline, sensitivity) | +8.1e-11 /yr | [−3.9e-12, +1.64e-10] /yr | +1.16 |
| rival a0 ∝ H (Ḣ/H) | **−3.53e-11 /yr** | [−4.39e-11, −2.67e-11] /yr | −0.51 |
| Branch A | 0 (identity) | — | 0 |

- **Today's sign is not determined.** The 68% interval straddles zero in every literal reading. The literal value is a
  [0, 0.4] segment average (a plant shows a secant/instantaneous ratio of 0.76–0.93). The smooth spline even flips the sign.
- The a0 e-folding time is ≥ 60 Gyr (68% envelope; median 310 Gyr), against the rival's 28 Gyr.
- **The rival is not viable:** L37/A34 put it at 27σ in n_s at recombination. It is used here only as MUTATE and as a
  comparison.
- **Observables** (deep-MOND flat curve, M_b = 6e10 M☉, orbit at 3 r_M; canonical / alt). v_flat is 165.2 / 173.2 km/s, r_M is
  9.45 / 8.60 kpc, and P is 1054 / 915 Myr. Over 100 yr at the framework's 68% envelope (ε):

  | | framework (ε, 68% envelope) | rival |
  |---|---|---|
  | Δv_flat | 6.9e-5 / 7.2e-5 m/s | 1.8e-4 / 1.9e-4 m/s |
  | Δr_M | 1.6 / 1.5 AU | 4.3 / 3.9 AU |
  | ΔP (fixed r) | 1.4e7 / 1.2e7 s | 3.7e7 / 3.2e7 s |
  | ȧ0 | 1.6e-21 / 1.9e-21 m s⁻² yr⁻¹ | — |

- **Reachability: framework NOT REACHABLE, rival NOT REACHABLE.**
  - The precision is δ_rec = 3.73%, the 68% half-width of `P3.a0_node_q["0.0"]` (a committed file).
  - Reaching it needs T_req = 2.2e9 yr for the framework and 8.5e8 yr for the rival.
  - A hypothetical 1e-6 precision (a stress value, not a quote) would still need 6e4 / 2.3e4 yr.
  - The drift is reached only through lookback (the a0(z) band), not by any local clock.

## (f) IDENTITY (no verdict weight)
S_dS = 3k_B c⁷/(32Għa0²) at κ = ½. This is 3.31e122 k_B (canonical) and 2.27e122 k_B (alt). Also d ln S/dt = −2 d ln a0/dt:
a rising a0 is a shrinking horizon entropy of the dark-energy patch.

## Controls
- **Pass:** K1(a–c) (H0 67.701 vs 67.696; a0(0) 9.3523e-11; E(z) to 0.03%). K2 (constant DE gives a flat a0, TRUE BY
  CONSTRUCTION). K3 (phantom/quintessence plants recovered). K4 (sympy). K5 (age integrator, inside its 1e-6 tolerance).
- **K1b, the approximation diagnostic: FLAGGED.** APPROX-G misses the stored √X quantiles by 0.036 / 0.032 / 0.038 at
  z 1.0 / 1.5 / 2.33, against a tolerance of 0.03.
  - The cause is the non-adjacent correlations APPROX-G omits (PH3).
  - These correlations do not enter the frozen per-segment classes, which use adjacent pairs only.
- **MUTATE (X → H²): PASS and BITES.** All five segments are FALL_95; the ε class flips PHANTOM-REQUIRED → FALLING, and the arrow
  is FALLING-ONLY. It reproduces CFG689's rival column (1.761 / 2.353 / 3.491).
- Peak RSS is 0.71 / 0.78 GB; runtime is about 3 s.

## POST HOC (`wt03_posthoc.py`; reported only, no verdict weight)
- **PH3: the stored joint quantiles call for strong positive correlations** (corr(w0, w_z) ≈ +0.85 / +0.75 / +0.85).
  - One all-node equicorrelation of +0.80 reproduces all four stored √X rows to 0.008. This looks like the curvature mode.
  - Under it, segment 0.7→1.0 rises with p = 0.9925 (**PHANTOM-REQUIRED at 95%**), and 0.4→0.7 falls at 68%. That gives a
    **TURNAROUND, PEAK at z ≈ 0.7, at 68%**, and P(maximum at 0.7) = 0.68.
  - Today stays undetermined: −0.047 H0, 68% [−0.010, +0.004] Gyr⁻¹.
- **PH2:** a0(0.7)/a0(0) = 1.122 [1.021, 1.220], above today's value at 68% for all three correlations, but not at 95%.
- **PH4, CFG689 bracket modes** (ρ_adj 0):
  - PHANTOM-REQUIRED at 68% in every mode except D5 (DES-SN5YR, NOT DIAGNOSTIC) and B6 (coarse nodes).
  - Flat F and the θ* modes (not in canon) give PHANTOM-REQUIRED plus a PEAK at z 0.7 **at 95%**.
  - B12/B12c show a trough at z 1.0 (DR1 zigzag).
- **What settles it:** CFG689's primary run with its node samples or 6×6 node covariance written out. That is a small job in
  CFG689's own lane.

## Strongest caveat
CFG689 stores no posterior samples. The 68% class sits on a knife-edge for the unknown adjacent-node correlation; the post-hoc
calibration points the other way, toward 95%. The 68% demand also vanishes with DES-SN5YR. −p and V cannot be separated from ε
with this band (ρ″ unmeasured).

**In this framework, the vacuum clock runs** only through dark energy. Under Branch A it does not run at all. Under the tracking
reading it ran up during a phantom episode 6.4–7.8 Gyr ago (68%), probably peaked near z ≈ 0.7, and today it moves too slowly to
show a sign (|d ln a0/dt| ≲ 1.7e-11 per yr, e-fold ≥ 60 Gyr). It has no arrow of its own beyond the expansion's.

## Files and rerun
`FROZEN_CRITERIA.md` (c9ea722b6) and `AMENDMENT_A1.md`.
- `wt03.py` writes `wt03.out` and `wt03_results.json`.
- `WT03_MUTATE=1` writes `wt03_MUTATE.out` and `wt03_results_MUTATE.json`.
- `wt03_posthoc.py` writes `wt03_posthoc.out` and `wt03_posthoc.json`. Run it after `wt03.py`.

```
OMP_NUM_THREADS=1 nice -n 10 python3 what_is_time/WT-03_vacuum_clock/wt03.py
WT03_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 what_is_time/WT-03_vacuum_clock/wt03.py
OMP_NUM_THREADS=1 nice -n 10 python3 what_is_time/WT-03_vacuum_clock/wt03_posthoc.py
```
