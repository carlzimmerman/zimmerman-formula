# CFG937: two-floor primordial halos (H-CF2). Reading (S): PARTIAL (corner-selectable), FRAGILE. Upper bracket: PARTIAL-UPPER (corner-selectable). Reading (M): PARTIAL (corner-selectable)

**Bottom line.** H-CF2 adds a second floor to CFG934's atomic-cooling floor. Dwarfs that kept forming stars after reionization
must sit in halos that could keep accreting photo-heated gas: V_vir ≥ √2 c_s(T_IGM), the record's own CFG782 retention
condition, with T_IGM between 1 and 2 × 10⁴ K. In practice almost every dwarf is a late former, so the second floor raises the
floor mass by ×1.84 (T_IGM 1.5e4) or ×2.83 (2e4).

- **What it does.** Under the primary sum reading (S), the LVD-83 class moves from CFG934's +0.121 … +0.403 ln to −0.093 …
  +0.326 ln. It is CONSISTENT at 12 of 36 corners on each footing (CFG934: 0 of 12). The isolated LG dwarfs reach CONSISTENT at
  20 (canonical) / 30 (alt) of 36 corners. The MW classicals, the M31 dSphs and all 110 SPARC dwarfs stay CONSISTENT at every
  corner. At 6 corners all six classes are CONSISTENT on both footings.
- **What it does not do.**
  - It does not survive the declared brackets. The verdict was fixed in advance (criteria E2): at T_IGM = 1e4 K the filtering
    velocity equals the ionised cooling velocity, so those corners are CFG934's.
  - Within the upper bracket (T_IGM 1.5–2e4), the six all-CONSISTENT corners lie on a narrow diagonal in (C, T_IGM, τ). Denser or
    hotter corners over-predict the ultra-faints; less dense or cooler ones leave L CONTRADICTED.
  - **The intermediate dSphs (−10 < M_V ≤ −7.7) still carry +0.08 to +0.23 ln at every all-CONSISTENT corner** (canonical
    +0.10 … +0.23, alt +0.08 … +0.22). The LVD-83
    class mean passes there because the faint dwarfs are pushed to about zero, not because the intermediate excess is gone.
    Wherever the intermediate bin comes closest to the law (+0.08 ln, τ50 / C6000 / T 2e4), the ultra-faints are CONTRADICTED on
    the over-predicted side (−0.169 dex, z −3.4).
- **FRAGILE.** Four variants change the verdict:
  - Υ_V = 1 for the I and L classes;
  - the 13.3-Gyr onset collapse epoch (FAILS-UPPER: the ultra-faints are over-predicted at all 24 upper corners);
  - an own-evidence selector (dwarfs without their own SFH or HI take only the cooling floor; L is then CONTRADICTED at 33 of 36);
  - V_th = c_s instead of √2 c_s.

  The improvement in L rests on giving the filtering floor to dwarfs whose SFH is only a group default.

κ = ½ is FITTED. The footings 9.3603e-11 / 1.1312e-10 m/s² are scored separately and never pooled. Verdicts use raw data and
framework-native inputs only: CFG42's Moster / Dutton–Macciò inputs appear only in K1. The extra mass is cold energy, not a
particle. Not "theory closed". Nothing here says the data favour the framework.

| | |
|---|---|
| Kind | HYPOTHESIS TEST building on CFG934: one new rule (SFH-selected second floor), zero fitted constants (μ, τ, C, T_IGM are declared brackets; m = √2 and μ_f = 0.59 are record values) |
| Block | CFG930–939 (this lane = CFG937) |
| Criteria | `FROZEN_CRITERIA.md`, **73144fddb**, committed alone before any script or number. No amendments. |
| Seal | **a8792e8b4**: `cfg937_SEALED_P937.json` (sha256 `75987b4250ef246cb7ed65de8835b65fbc51fc70063aa37fe5de8719f557e89e`), committed with the script and the K/MUTATE outputs **before** the main run |
| Results | main run `cfg937.out`, `cfg937_results.json`, this README (commit in the LEDGER row). `cfg937.py` did not change after a8792e8b4. |
| Run | `CFG937_MODE=K|MUTATE_EQ|MUTATE_T10|SEAL|main OMP_NUM_THREADS=1 nice -n 10 python3 cfg937.py` (each mode 3–20 s, peak 174 MB; RSS guard 900 MB). CFG934's code is exec'd read-only (writes refused) |
| Not blind | Formed AFTER CFG934's result. Criteria §0 disclosed E1–E4, including that the full-bracket verdict could only be PARTIAL (E2). E3 was partly wrong: under (S) the class mean of L does reach CONSISTENT at the hot corners, but the intermediate dSphs stay above the law as E3 expected |

## Hypothesis and rule

**H-CF2.** Start from CFG934: cold energy is cold collisionless matter before any bound system exists (CFG649/CFG654), and every
star-forming dwarf sits in a primordial halo at least at the atomic-cooling threshold (T_vir 1e4 K at its formation epoch z_f).
In addition, a dwarf that kept forming stars after reionization needs a halo whose virial velocity at z_f reaches the
filtering threshold V_th = √2 c_s(T_IGM), μ_f = 0.59. That is CFG782's T_vir ≥ T_IGM, reused as a halo floor and not as the
removed S4 untethering selector. No cold energy is freed. A dwarf quenched at reionization needs only the cooling floor.

- **Selector.** A dwarf is a late former iff its Weisz+14 τ90 lies below the grid's first node (12.589 Gyr, z 4.96). τ90 is
  its own value, or CFG934's group default. SPARC dwarfs are late formers (star-forming now).
- **z_reion.** Its lookback (12.84 Gyr at z 6, 13.14 at z 8) lies beyond that node, so the declared z_reion bracket is inert
  (asserted in K4).
- **Membership.** Quenched dwarfs are Hercules (U, L), Andromeda VII and Andromeda XIII (M31 LVD, L). Every other dwarf is a
  late former, including 39 of 40 ultra-faints (37 of them by the faint-satellite default τ90 9.76 Gyr).
- **Floor.** For a late former, M_floor = max(M_cool, M_filt) at the same z_f. M_filt ≥ M_cool always; the two are equal at
  T_IGM 1e4, μ 0.59.

### The floor masses used (`cfg937.out`; native Δ_vir)

| z_f | 0 | 0.5 | 1 | 2 | 3 | 5 |
|---|---|---|---|---|---|---|
| M_cool μ 1.22 (quenched only) [M☉] | 7.86e8 | 5.03e8 | 3.46e8 | 1.95e8 | 1.28e8 | 6.99e7 |
| M_cool μ 0.59 = M_filt T_IGM 1e4 [M☉] | 2.34e9 | 1.50e9 | 1.03e9 | 5.79e8 | 3.80e8 | 2.08e8 |
| M_filt T_IGM 1.5e4 [M☉] | 4.30e9 | 2.75e9 | 1.89e9 | 1.06e9 | 6.97e8 | 3.82e8 |
| M_filt T_IGM 2e4 [M☉] | 6.61e9 | 4.23e9 | 2.91e9 | 1.64e9 | 1.07e9 | 5.88e8 |
| r_vir T_IGM 2e4 [kpc] | 50.8 | 32.5 | 22.3 | 12.6 | 8.3 | 4.5 |

V_th = 16.73 / 20.49 / 23.66 km/s at T_IGM 1 / 1.5 / 2e4 K. V_cool = 16.73 (μ 0.59) / 11.63 (μ 1.22) km/s. The concentration
depends only on C and z_f (c ≈ 2.3 / 3.2 / 4.4 at z ≥ 2), so a ×2.83 floor mass raises the inner mass by about ×2.83^(1/3) =
1.41 at fixed C.

## Results (`cfg937.out`, `cfg937_results.json`)

The statistics and errors are CFG934's: U, C, M in dex of σ; I in dex of g; L in ln σ; S as the fraction of 110 SPARC dwarfs
raised by < 0.03 dex. Classes: |z| < 2 CONSISTENT, 2–3 TENSION, ≥ 3 CONTRADICTED. Corners: μ {0.59, 1.22} × τ {τ50, τ90} ×
C {1500, 3000, 6000} × T_IGM {1, 1.5, 2}e4 = 36.

### Reading (S), primary: range over the 36 corners (labels C / T / X of 36)

| class | canonical: bare → H-CF2 (z range) | labels | alt: bare → H-CF2 (z range) | labels |
|---|---|---|---|---|
| **U** MW ultra-faints (31 + 9 limits) | +0.325 (+3.77) → −0.169 … +0.194 (−3.50 … +3.14) | 21 / 11 / 4 | +0.304 → −0.169 … +0.184 (−3.53 … +2.98) | 20 / 14 / 2 |
| **C** MW classicals (14) | +0.027 → −0.037 … +0.027 | 36 / 0 / 0 | +0.007 → −0.052 … +0.007 | 36 / 0 / 0 |
| **M** M31 dSphs (worse of Collins+13 / LVD) | +0.064 → −0.036 … +0.064 | 36 / 0 / 0 | +0.045 → −0.036 … +0.045 | 36 / 0 / 0 |
| **I** isolated LG dwarfs (11, gas counted) | +0.194 (+2.53) → +0.050 … +0.194 (+0.75 … +2.53) | 20 / 16 / 0 | +0.155 → +0.036 … +0.155 | 30 / 6 / 0 |
| **S** SPARC gas-rich dwarfs (110) | 1.00 → 1.00 (f_ex = 0 in all 110) | 36 / 0 / 0 | 1.00 → 1.00 | 36 / 0 / 0 |
| **L** LVD-83 | +0.518 (+8.86) → −0.093 … +0.326 (−1.75 … +6.54) | 12 / 6 / 18 | +0.472 → −0.096 … +0.297 (−1.82 … +5.93) | 12 / 8 / 16 |

Labels by T_IGM (C / T / X of 12, canonical):

| T_IGM | U | I | L |
|---|---|---|---|
| 1e4 | 8 / 2 / 2 | 0 / 12 / 0 | 0 / 2 / 10 |
| 1.5e4 | 6 / 6 / 0 | 8 / 4 / 0 | 4 / 4 / 4 |
| 2e4 | 7 / 3 / 2 | 12 / 0 / 0 | 8 / 0 / 4 |

**Verdict (S), headline: PARTIAL (corner-selectable), on both footings.** As E2 stated in advance, SURVIVES and FAILS were both
unreachable over the full bracket. **Upper bracket (T_IGM 1.5–2e4, 24 corners): PARTIAL-UPPER (corner-selectable).** No class
is CONTRADICTED at all 24 upper corners, and none is CONSISTENT at all 24 except C, M and S (and I on the alt footing).

**Corner spread.** All six classes are CONSISTENT on both footings at 6 corners (canonical 7, alt 6). μ only touches the three
quenched dwarfs, so these are three settings, each at both μ. The canonical footing's seventh corner is μ 0.59 / τ50 / C3000 /
2e4, where U sits at z −1.998 (CONSISTENT by 0.002; −2.03 on alt and −2.08 at μ 1.22, TENSION).

| setting (τ, C, T_IGM) | canonical U / I / L (z) | alt U / I / L (z) | LVD-83 by M_V, canonical (≤ −10 / −10…−7.7 / > −7.7) |
|---|---|---|---|
| τ50, C 1500, 2e4 | −0.037 (−0.7) / +0.103 (+1.6) / +0.068 (+1.4) | −0.037 / +0.081 / +0.056 (+1.1) | +0.01 / **+0.18** / +0.01 |
| τ50, C 3000, 1.5e4 | −0.063 (−1.3) / +0.133 (+2.0, just under) / +0.070 (+1.4) | −0.063 / +0.114 / +0.062 | +0.01 / **+0.23** / −0.02 |
| τ90, C 6000, 2e4 | +0.025 (+0.5) / +0.073 (+1.2) / +0.081 (+1.6) | +0.023 / +0.046 / +0.063 | −0.01 / **+0.10** / +0.11 |

The neighbouring corners fail on one side or the other:
- τ50 / C3000 / 2e4: U −0.101 (z −1.998 to −2.15: the CONSISTENT/TENSION boundary).
- τ50 / C6000 / ≥ 1.5e4: U −0.132 / −0.169 (TENSION / CONTRADICTED, over-predicted).
- Every τ90 corner with C ≤ 3000 or T_IGM ≤ 1.5e4: L +0.133 … +0.326 (TENSION / CONTRADICTED).

Choosing one of the three settings is a discrete fit, not a survival.

**The intermediate dSphs.** This is the per-luminosity diagnostic declared in criteria §7, so it is not post hoc. Bare-law
LVD-83 excess, canonical: M_V ≤ −10 +0.012, −10 < M_V ≤ −7.7 +0.360, M_V > −7.7 +0.860 ln. Under (S), the intermediate bin
ranges over:
- T_IGM 1e4: +0.271 … +0.341 (the floor acts in 6–18 of 28);
- T_IGM 1.5e4: +0.167 … +0.261 (acts in 17–28 of 28);
- T_IGM 2e4: +0.081 … +0.208 (acts in 24–28 of 28).

The faint bin over the same corners: −0.269 … +0.479. The filtering floor turns f_ex on for most intermediate dSphs, but with
small leftover fractions (canonical, μ 0.59, τ50 / τ90 at T_IGM 1e4 / 1.5e4 / 2e4):

| dwarf | edge phantom | τ50 floor and f_ex | τ90 floor and f_ex |
|---|---|---|---|
| Draco | 8.2e8 | f_ex 0 / 0 / 0.16 | f_ex 0 / 0.18 / 0.47 |
| And IX | 6.9e8 | f_ex 0 / 0.34 / 0.57 | f_ex 0.52 / 0.74 / 0.83 |
| And V | 1.1e9 | f_ex 0 / 0 / 0.11 | f_ex 0 / 0.37 / 0.59 |

At τ90 the floor halos are larger but formed late and diffuse, so they add little mass inside r½. Under (S) the intermediate
excess shrinks from about +0.3 to +0.1–0.2 ln at the hot corners. It does not reach zero anywhere that the ultra-faints stay on
the law.

(Print note: in `cfg937.out` the named-dwarf line labels its three T_IGM entries "T1e+04 / T2e+04 / T2e+04" because the format
rounds 1.5e4. The entries are 1e4, 1.5e4 and 2e4 in that order; the JSON keys `named_dwarfs` are correct. No number is affected.)

**Change vs CFG934 at the same (μ, τ, C)**, over the upper corners, canonical (S): U −0.255 … −0.027, C −0.064 … −0.001,
M −0.100 … 0, I −0.144 … −0.024, S 0, L −0.384 … −0.054.

### Reading (M), alternative: PARTIAL (corner-selectable); upper PARTIAL-UPPER (corner-selectable)

All six classes are CONSISTENT on both footings at 8 corners (four settings × both μ):
- τ50 / C1500 / 2e4;
- τ50 / C3000 / 1.5e4;
- τ50 / C3000 / 2e4;
- τ50 / C6000 / 1e4 (CFG934's (M) corner).

Labels over the 36 corners, canonical: U 18 / 6 / 12, I 12 / 24 / 0, L 11 / 3 / 22. On the canonical footing every τ90 corner
leaves U or L CONTRADICTED (alt: τ90 / C6000 / 2e4 has L TENSION, +2.9). At its all-CONSISTENT corners, (M) also leaves the intermediate bin at +0.11 … +0.22 ln. Where (M) brings that
bin to the law (τ50 / C6000 / 2e4: −0.02), U is −0.168 (z −3.1) and L −0.168 (z −3.2), both CONTRADICTED.

### Variants (reading S; criteria §4.3)

| variant | headline | upper | all-CONSISTENT corners can / alt | note |
|---|---|---|---|---|
| V1 Δ_vir = 18π² | corner-selectable | corner-selectable | 7 / 6 | |
| **V2 onset z_coll (13.3 Gyr)** | **PARTIAL** | **FAILS-UPPER** | 0 / 0 | denser halos: U CONTRADICTED 34/36 (24/24 upper) |
| **V3 Υ_V 1 (I, L)** | **PARTIAL** | PARTIAL-UPPER | 1 / 0 | I CONTRADICTED 24/36, L 24/36 |
| V3 Υ_V 4 (I, L) | corner-selectable | corner-selectable | 15 / 18 | |
| V4 CFG930 uniform recipe | corner-selectable | corner-selectable | 15 / 17 | the Υ floor dilutes L (0 CONTRADICTED) |
| V5 Υ_SFH (CFG827) | corner-selectable | corner-selectable | 3 / 4 | |
| V6 luminosity-class τ default | corner-selectable | corner-selectable | 5 / 6 | |
| V7 selector by τ50 | corner-selectable | corner-selectable | 7 / 6 | |
| **V8 own-evidence selector** | **PARTIAL** | PARTIAL-UPPER | 0 / 2 | 55 of 83 LVD dwarfs and 38 of 40 UFDs revert to the cooling floor; L CONTRADICTED 33/36 |
| **V9 m = 1 (V_th = c_s)** | **PARTIAL** | PARTIAL-UPPER | 0 / 0 | the filtering floor falls to or below the cooling floor; L CONTRADICTED 32/36 |
| V10 m = 2 (V_th = 2 c_s) | corner-selectable | corner-selectable | 14 / 12 | |
| V11 onset mapping (every dwarf late) | corner-selectable | corner-selectable | 8 / 6 | the three quenched dwarfs barely matter |

**FRAGILE: yes** (V2, V3 Υ_V 1, V8, V9). The verdict moves with:
- the stellar M/L of the I and L classes;
- the collapse epoch convention;
- how dwarfs without their own SFH are classed;
- the filtering multiple m.

## Controls

| control | result |
|---|---|
| K0 | CFG934's committed K passed; cfg934.py sha256 `746aa6c9…` |
| K1 / K1b | CFG42 reproduced through the inherited estimator with its own inputs: 60 UF/CL numbers \|d\| 0, H4 exact. CFG45 (M): 16 numbers, 1.8e-15; SPARC dwarf\|M exact |
| **K2** | **CFG934 reproduced with the second floor switched off:** 3540 numbers (corners S and M, bare law) max \|d\| 0; labels identical; verdicts PARTIAL / PARTIAL (corner-selectable) identical; all six CFG934 variants identical (verdicts and statistics, \|d\| 0) |
| K3 | V_th 16.7275 / 20.4870 / 23.6563 km/s; vs CFG782's formula 6.6e-6 relative (m_p constant); vs its printed values 0.0037 km/s; M_filt(1e4) ≡ M_cool(μ 0.59) exactly; V_vir identity 1.6e-15 |
| K4 | selector τ90 = CFG824's (36/36, exact); "τ90 at the node" ⇔ f(12.59 Gyr) ≥ 0.9 for all 40 Weisz objects; lookback z 6 / 8 = 12.844 / 13.136 Gyr > 12.589 (z_reion inert) |
| K5 | the seal's synthetic estimator equals the L estimator for the real 83 (boost and f_ex, \|d\| 0) |
| **MUTATE_EQ** (filtering floor := cooling floor) | **PASS:** all 36 corners reproduce CFG934, 10 224 numbers, \|d\| 0 |
| **MUTATE_T10** (T_IGM × 10) | **FAILED as frozen: 231 of 504 cells** (see below) |

**MUTATE_T10, by class:**
- **S, 68 cells:** SPARC stays CONSISTENT at 32/36 canonical and 36/36 alt corners. Its frac is ≥ 0.86 even with z_f = 0
  floors of 0.7–2e11 M☉.
- **C, 54 cells, and M-Collins, 48:** the statistic has the right sign, but z > −2. This is the error-budget limitation that
  CFG934's T100 also hit.
- **U 20, I 24, L 11:** all at τ90 corners with C ≤ 3000 (I also at C 6000 / 1e5), where ~31× the floor mass only brings the
  class to the law. Six cells have a statistic of about 0 (|stat| ≤ 0.007).

U, I and L bite at every τ50 corner. **Flag:** at the late, diffuse τ90 corners these classes cannot detect over-supply, and S
has little power against a floor at z_f = 0. The same diffuseness is why L stays CONTRADICTED at the τ90 low-C corners in the
main run.

## Sealed prediction P937 (commit a8792e8b4, before the main run)

- **Class.** Gas-free dSphs with a resolved CMD SFH and a stellar σ, in none of the record's samples (CFG42, CFG874,
  CFG880/LVD-83, CFG933, CFG936), e.g. future discoveries.
- **Split.** Q: f(12.59 Gyr) ≥ 0.9. Lm: τ50 < 12.589 Gyr.
- **Quantity.** ΔE = ⟨ln σ_obs/σ_law⟩_Lm − ⟨…⟩_Q at matched M_V and r_h (CFG880 estimator).
- **Templates.**
  - Q: z_f 4.955.
  - Lm: τ50 9.040 / τ90 3.374 Gyr (z_f 1.325 / 0.284), the medians of the 30 Weisz+14 objects with an LVD row and τ50 below
    the node.
- **Sealed ranges** over all 36 corners:

| bin | (S) canonical | (S) alt | (M) canonical | (M) alt |
|---|---|---|---|---|
| −10 < M_V ≤ −7.7 | **+0.059 … +0.367** | **+0.041 … +0.326** | −0.524 … −0.017 | −0.484 … −0.011 |
| M_V > −7.7 | −0.229 … +0.805 | −0.186 … +0.827 | −0.854 … −0.049 | −0.841 … −0.049 |
| M_V ≤ −10 | 0.000 … +0.057 | 0.000 … +0.042 | −0.138 … +0.014 | −0.110 … +0.016 |

- **Plain statement.**
  - Under (S), H-CF2 predicts that intermediate-luminosity dSphs that formed most of their stars after reionization show
    **more** excess than matched quenched ones, by +0.04 to +0.37 ln, at every corner on both footings.
  - Under (M) the sign is reversed at every corner (the early, dense cooling-floor halo wins).
  - So a future matched sample can test H-CF2 and also separate the two readings.
- **Kill line.** With ≥ 5 dwarfs per group, matched within 0.5 mag and 0.15 dex in r_h, H-CF2 is excluded on a footing if the
  observed ΔE lies outside [min − 2 se, max + 2 se] of the (S) prediction.
- **No current sample can score it.** LVD-83 has only three quenched dwarfs.

## Ungraded reports

- **Coma UDGs** (CFG933's 9): H-CF2 predicts **zero excess** at every z_f 0–5, either status, every μ / T_IGM / C:
  - (S): f_ex = 0 in 9/9;
  - (M): the floor is below the phantom.

  Observed ⟨E⟩ +0.760 / +0.669 ln. The UDG excess is not a floor effect.
- **NGC 1052-DF2/DF4.** No primordial halo, so E_pred = 0. Even with a floor halo of either status at any z_f 0–5, E_pred = 0
  under both readings. Observed −1.71 / −2.17 (canonical), −1.80 / −2.26 ln (alt).
- **Tidal dwarfs** (CFG936 S1). Observed −0.690 ± 0.078 (canonical) / −0.728 ± 0.079 dex (alt), below the law. H-CF2 predicts 0:
  no excess, matching the sign of "no primordial halo", but the deficit is not explained.
- **CFG880 scatter.** LVD-83 intrinsic scatter of ln(σ_obs/σ_pred):

  | model | canonical | alt |
  |---|---|---|
  | bare law | 0.462 | 0.462 |
  | H-CF2 (S) | 0.318–0.368 | 0.322–0.368 |
  | H-CF2 (M) | 0.344–0.426 | 0.344–0.426 |
  | CFG934 (S) | 0.335–0.378 | — |
  | CFG877 universal clump | 0.271 | 0.282 |

  Spearman ρ(predicted boost, observed excess) = +0.56 … +0.62 (S, canonical). The floor still puts mass in the right dwarfs,
  but one universal clump removes more scatter than the two floors.

## What is and is not established

**Established** (conditional on the declared brackets and the inherited estimators):
1. A second, SFH-selected floor at the record's own filtering threshold lowers every dwarf class's excess relative to CFG934:
   - L by 0.05–0.38 ln and I by 0.02–0.14 dex at the upper corners;
   - the classicals, M31 dSphs and SPARC are kept CONSISTENT at all 36 corners.
2. There is a narrow set of corners (three settings) where all six galaxy-scale classes are CONSISTENT on both footings under
   (S). This is corner-selection, and the verdict is FRAGILE.
3. Even there, the intermediate dSphs keep +0.08 to +0.23 ln under (S). Under neither reading do the faint and intermediate
   dSphs reach the law together with the ultra-faints.
4. H-CF2 predicts zero excess for Coma UDGs, DF2/DF4 and tidal dwarfs.
5. A sealed, sign-definite prediction separates late formers from quenched dSphs, and (S) from (M).

**Not established:**
- That H-CF2 survives. It cannot over the record's T_IGM bracket (E2), and the result is FRAGILE.
- That the late-former status of the ultra-faints is right. 37 of 40 rest on the faint-satellite default τ90 (9.76 Gyr, median
  of 6 Weisz objects). With an own-evidence selector (V8), L returns to CONTRADICTED.
- That the floor is the dwarfs' actual halo. It is a lower bound.
- That T_IGM ≥ 1.5e4 K, the corners that work, is physically preferred.
- The inherited caveats of CFG934: tides, EFE and binaries are not modelled; the CFG35 edge uses CFG7's flat-Λ turnaround
  convention; NFW with ρ_s = C ρ̄_m(z_f) is declared generic collapse physics.

**For the record.** The second floor narrows CFG934's gap, but it does not close it robustly. The residual that remains is the
same one CFG934 found: the intermediate dSphs, about +0.1–0.2 ln at the corners that keep everything else on the law.

κ = ½ FITTED; footings never pooled; cold energy, not a particle; not theory closed.
