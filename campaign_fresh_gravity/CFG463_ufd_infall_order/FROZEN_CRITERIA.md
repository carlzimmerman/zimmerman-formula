# CFG463 FROZEN CRITERIA: does the ultra-faints' bare-law excess rise with LATER infall? (per-object test of CFG344)

Frozen 2026-10-08, before the script existed and before any infall time was computed. No orbit of any satellite has been
integrated in this lane. What was seen before freezing is listed in section 10.

κ = ½ is FITTED. No dark-matter particle is added: the cold fluid's MASS is still required. Nothing here says the theory is
closed or that the data favour the framework.

## 1. Question

CFG344 explains the Milky Way ultra-faints' bare-law excess (+0.32 dex, CFG28/CFG259) by post-reionisation cold accretion
onto reionisation fossils. Accretion stops at infall. With one formation epoch z_f, a later infaller has accreted longer and
carries more cold mass: on CFG344's own grid M_c = 3.7e8 / 5.75e8 / 8.8e8 Msun at z_inf = 3 / 2 / 1. So, object by object,
**the bare-law excess must be larger for later infallers**, i.e. it must ANTI-correlate with infall lookback time. CFG344
used one z_inf for every object; this is the per-object test (failure ledger 2026-10-08, top-3 item 2).

## 2. Samples (fixed)

The ultra-faints are FG001's (M_V > −7.7, LVD Milky Way table), exactly as CFG28 loads them.

- **S1 (PRIMARY, verdict sample):** FG001's 31 resolved ultra-faints that have a Fritz et al. 2018 (A&A 619, A103) Table 2
  entry. Expected N = 21: Aquarius II, Bootes I, Bootes II, Canes Venatici II, Carina II, Carina III, Coma Berenices,
  Eridanus II, Grus I, Hercules, Horologium I, Hydrus I, Leo IV, Leo V, Pisces II, Reticulum II, Segue 1, Tucana II,
  Ursa Major I, Ursa Major II, Willman 1.
- **S2 (reported):** S1 plus the five FG001 upper-limit systems that Fritz measured (Draco II, Hydra II, Segue 2,
  Triangulum II, Tucana III), each entered at its limit (an upper bound on its excess). N = 26.
- **S3 (reported):** S1 without CFG433's six LMC candidates (Carina II, Carina III, Horologium I, Hydrus I, Reticulum II,
  Tucana II). N = 15.
- **S4 (reported; data veto, section 7):** all 31 resolved ultra-faints with the LVD's own (Pace+22, Gaia EDR3) proper
  motions, distances and systemic velocities, two-piece Gaussian errors as in CFG286. N = 31 if every one has a proper motion
  (any without one is dropped and named).

## 3. The excess (fixed; the record's estimator)

x_i = log10(σ_obs,i / σ_law,i), per footing, never pooled (a0 = 9.3603e-11 canonical, 1.1312e-10 alt).
σ_law is FG001's `sigma_pred(..., efe=False)`: the isolated law of the stars (Υ_V = 2, gas 1.33 M_HI), r = (4/3) r_half,
σ² = g r / 3. FG001's loader and estimator are exec'd read-only, as in CFG28. Measurement error ELOG_i = 0.4343 esig_i/sig_i.

## 4. Phase space (fixed)

- **Fritz (S1, S2, S3):** RA/Dec from the LVD row of the same object; distance modulus from Fritz Table 1, its error ⊕ 0.1
  mag (the paper's own floor); proper motions from Table 2 with statistical ⊕ systematic errors, the quoted correlation C
  applied to the statistical part only; V_LOS ± error from Table 2.
- **Frame (all samples):** Fritz's Galactocentric frame, R0 = 8.2 kpc and solar velocity (11, 248, 7.3) km/s, with
  z_sun = 25 pc (Bland-Hawthorn & Gerhard 2016, the paper's cited source).
- **Monte Carlo:** 300 Gaussian draws per object plus the central values, seed 463.

## 5. Hosts and infall (fixed)

All hosts are spherical, so each orbit is integrated in its own plane: kick-drift-kick leapfrog, backward from today,
dt = 0.5 Myr, to t_max = the lookback time at z_f = 8 (CFG344's primary formation epoch). Cosmic time comes from
CFG7_common.LCDM (Planck 2018, Ω_m 0.3153, h 0.6736).

**Host growth.** h(z) = M(z)/M_0 is CFG344's own Correa+15 median MAH (`ab`, `M_of`; colossus planck18), exec'd read-only
from CFG344's script, at the record's MW collapse mass M_0 = 9.82e11 Msun (M_200c; CFG286's rule-S host value).

| host | field | role |
|---|---|---|
| **L6 (PRIMARY)** | g = ν_mono(g_N/a0) g_N, point-mass baryons M_b(t) = 6.0e10 h(z(t)), the footing's a0 | load-bearing |
| **L7** | the same with M_b0 = 7.3e10 (the record's census-high MW value) | load-bearing |
| L6s | the same as L6 with M_b fixed at 6.0e10 (no baryon growth) | reported; sign condition |
| N | Newtonian NFW, M_200c(t) = 9.82e11 h(z(t)), c_200c(M, z) from Dutton & Macciò 2014 (z clamped at 5; its z = 0 form equals CFG36's), untruncated, no separate baryons | reported; sign condition |

g_N is softened as G M r / (r² + ε²)^{3/2} with ε = 0.5 kpc (numerical only; < 0.4 % change beyond 10 kpc).

**Infall boundary.** R_b(t) = R_200c of the MW's collapse mass 9.82e11 h(z) at that epoch (ρ_c(z) from CFG7_common.LCDM), the
same for every host: the region where the MW's cold fluid has collapsed (the cold fluid is operationally CDM, CFG474), which
is where a fossil stops accreting. Reported variant **B300**: a fixed physical 300 kpc boundary (L6 host).

**Infall lookback t_inf (Gyr):** the largest lookback time at which r ≤ R_b, linearly interpolated at the crossing (first
entry in forward time). Never inside within t_max → t_inf = 0 (not yet fallen in). Inside at t_max → t_inf = t_max
(censored; the count is reported). Per object, t̂_inf = the median over its 301 orbits.

## 6. Statistic (fixed)

ρ = Spearman(x, t̂_inf) on S1, per host and footing (the law hosts' infall times are per footing; N's are not).
Z = atanh(ρ) √((N − 3)/1.06) (Fieller-Hartley-Pearson). A two-sided permutation p (10,000, seed 4632) is reported beside Z.
**CFG344 predicts ρ < 0.**

Error Monte Carlo sign fraction: for each draw k = 1..300, ρ_k = Spearman(x + ELOG ε_k, t_inf^(k)); f_neg (f_pos) is the
fraction with ρ_k < 0 (> 0).

## 7. Verdict (fixed)

- **SUPPORTED:** Z ≤ −2 in all four load-bearing readings (L6 and L7, canonical and alt), AND f_neg ≥ 0.84 for L6 on both
  footings, AND ρ < 0 for L6s and N on both footings (robust to the potential choice), AND no veto, AND C-NULL passes.
- **CONTRADICTED:** the mirror: Z ≥ +2 in all four, f_pos ≥ 0.84 for L6 on both footings, ρ > 0 for L6s and N on both
  footings, no veto, C-NULL passes.
- **NOT DIAGNOSTIC:** anything else. The power (section 8) and N are reported with it.
- **Veto (data):** S4 on the L6 host with |Z| ≥ 2 of the OPPOSITE sign on either footing downgrades SUPPORTED or
  CONTRADICTED to NOT DIAGNOSTIC (data-dependent).
- A failed load-bearing control (section 9) also blocks SUPPORTED and CONTRADICTED.

## 8. Power (reported, required)

CFG344's predicted shift is taken from its committed JSON (`RUNS`, rows P1, canonical, both cold-mass profiles NFW and SIS,
z_f = 8, z_inf = 3 / 2 / 1). The predicted bare-law excess of an object that fell in at z is
Δx(z) = −[off(z) − off(2)], piecewise linear in log10 M_c(z) of CFG344's z_f = 8 fossil MAH, linearly extrapolated outside
z ∈ [1, 3], z capped at 8. Mocks (2000, seed 4633, L6 canonical, S1): x_mock = a random permutation of the observed x plus
Δx(z(t_true)), with t_true one random Monte Carlo draw per object; the statistic uses the medians t̂_inf. Power = the fraction
of mocks with Z ≤ −2, for each profile; the median mock ρ is reported as the predicted ρ.

## 9. Controls (load-bearing unless marked)

- **C-DATA:** the Fritz LaTeX source's sha256 equals FETCH_LOG.md's (5e958fa5…1197); Tables 1 and 2 parse to 39 rows each.
- **C-X:** FG001's committed resolved ultra-faint median (+0.355 / +0.334 dex) is reproduced to 1e-9 (CFG28's C1).
- **C-FRITZ:** the frame conversion reproduces Fritz Table 2 for all 26 (S2) objects: |Δd_GC| ≤ 1.5 kpc, |ΔV_rad| ≤ 3 km/s;
  |ΔV_tan| ≤ max(5 km/s, 5 %) where the table's V_tan error is < 30 km/s.
- **C-MAH:** h(0) = 1 to 1e-12 and h falls monotonically over z ∈ [0, 8]; R_200c(z = 0) of 9.82e11 lies in 200–220 kpc;
  DM14 at z = 0 equals CFG36's c(M) to 1e-12.
- **C-ORB:** (a) static L6 host (h ≡ 1), central S2 orbits: relative energy drift ≤ 1e-4 over t_max; (b) dt halved: at least
  90 % of the central L6-canonical S2 orbits keep t_inf within 0.05 Gyr (the rest are reported by name).
- **C-SIGN:** x = −t̂_inf gives ρ = −1.
- **C-NULL:** 10,000 shuffles of t̂_inf (L6 canonical, S1, seed 4632): P(|Z| ≥ 2) ≤ 0.07.
- **MUTATE (separate run, `CFG463_MUTATE=1`, `_MUTATE` outputs):** each object's whole block of infall times (its median and
  its draws) is permuted across objects (seed 4631), identically in every host and footing; the frozen verdict logic must
  return NOT DIAGNOSTIC with |Z| < 2 in all four load-bearing readings.

## 10. Reported rows (none is a verdict)

S2, S3, S4; B300; L6s and N in full; partial Spearman of (x, t̂_inf) controlling for log r_GC and for M_V; the leave-one-out
range of Z; the Theil-Sen slope dx/dt̂_inf (dex/Gyr) with a bootstrap 1σ against the two predicted slopes; Spearman(x, r_GC)
on S1 (CFG28's T2 on this subset); static-NFW pericentres against Fritz Table 3 for the well-measured objects (sanity only;
different potential).

## 11. Hand estimates (frozen)

- HE1: N = 21 / 26 / 15 / 31 for S1 / S2 / S3 / S4.
- HE2: R_200c(0) ≈ 210 kpc; the MAH's z_1/2 ≈ 1.2 (CFG344's C2 for 1e12 gave 1.20).
- HE3: the 2σ line at N = 21 is |ρ| ≥ 0.45.
- HE4: median t̂_inf (L6 canonical, S1) between 6 and 10 Gyr; Eridanus II has t̂_inf = 0 (beyond R_200c now) or near it.
- HE5: **I expect NOT DIAGNOSTIC, with a weakly POSITIVE ρ (|Z| < 2).** Reason: CFG28's T2 gave Spearman(x, distance) = −0.22
  (p 0.23) on the 31, so nearer systems have slightly larger excesses, and nearer systems tend to have fallen in earlier.
- HE6: power for the SIS-profile slope 0.2–0.4; for the NFW-profile slope < 0.15.

## 12. Seen before freezing (disclosure)

CFG28's README and committed per-population numbers, including T2's ρ(x, distance) = −0.22; CFG259's README; CFG286's README
(law-host pericentres from LVD motions; it computes no infall time); CFG344's README and committed JSON (the per-z_inf
offsets). Note: CFG344's README bracket table quotes the SIS (V2) canonical ultra-faint offsets as −0.09 (z_inf 3) and −0.21
(z_inf 1); its committed JSON gives −0.048 and −0.224. Section 8 uses the JSON. CFG433's README and the Fritz Table 1, 2 and
3 layouts (read for their columns). No infall time, no orbit and no correlation with infall was computed before this file.
