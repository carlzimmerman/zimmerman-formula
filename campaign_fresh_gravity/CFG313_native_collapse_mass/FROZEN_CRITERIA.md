# CFG313 — FROZEN CRITERIA: a framework-native collapse mass for candidate B's cold-mass rule

Written and committed before any score is computed. The hand pre-flight (section 7) was computed before this file was frozen, from the committed functions only (no population statistic was evaluated).

## 1. Why

Candidate B's derived cold-mass rule is reading (S) of CFG45: g = ν(g_N/a₀) g_N + f_ex (1 − f_b) G M_cold(<r; M_c)/r², with f_ex = max(0, 1 − M_ph,edge / [(1 − f_b) M_c]), the edge at x_e = 0.40 of the law's own turnaround radius (CFG7 `r_ta_law`, a = 1, ν_mono, each footing's own a₀). CFG303's inventory tags the rule's collapse masses M_c as LCDM-MODEL inputs: the Moster+13 stellar-to-halo relation (clamped at 1e9 M☉) for the satellites, the SPARC dwarfs and the LV field dwarfs; Mandelbaum+16's red/blue halo masses for SLUGGS, the X-ray ellipticals, SPARC log M★ ≥ 10, UGC 2487, the Di Teodoro discs and the Ogle super spirals; and a Dutton–Macciò NFW for the shape everywhere. This lane replaces M_c with a framework-native, parameter-free one and re-scores every rule row. The law-only rows use raw inputs and are not re-scored here; they are reproduced as controls.

## 2. The native collapse mass (primary, declared)

- **M_c = M_b / f_b.** The cold component and the baryons collapse together at the cosmic ratio. No feedback correction, no abundance matching, no halo model.
- **f_b = Ω_b/Ω_m = 0.02237 / (0.02237 + 0.1200) = 0.157126**, the committed `FB` of `campaign_fresh_gravity/CFG35_cold_mass_conservation.py` (Planck 2018 ω_b h² = 0.02237, ω_c h² = 0.1200), the same value every rule lane uses. Equivalently (1 − f_b) M_c = (Ω_c/Ω_b) M_b = 5.3643 M_b, the cosmic share of `CFG4_clusters.py` (`COSMIC` = 5.364).
- **M_b is each lane's own baryon mass, the same M_b the lane feeds to its edge phantom**, so the rule and its switch see one inventory:
  - satellites (MW ultra-faints, MW classical, M31 Collins+13, M31 LVD) and LV field dwarfs: M_b = Υ_V L_V + 1.33 M_HI, plus CFG18's infall gas for the classical samples (as CFG42/CFG45 compute M_b), at the Υ_V of the evaluation (so the Υ_V-floor variants move M_c with the baryons);
  - SPARC (dwarfs and log M★ ≥ 10), UGC 2487: M_b = 0.61 L_3.6 + 1.33 M_HI;
  - Di Teodoro+23 (CFG41) and Ogle+19 (CFG40): M_b = M★ + M_gas of the lane (with the lane's M★/M_gas perturbation variants);
  - SLUGGS (CFG38/h50 masses, CFG55 JAM-calibrated masses, CFG111 literature slopes): M_b = the lane's stellar mass (no hot gas, as the lanes); in the calibrated lanes the calibration solves for M★ with M_c = M★/f_b moving with it;
  - X-ray ellipticals (CFG36/CFG45 P6): M_b = the lane's stellar mass at the IMF of the evaluation (the committed rule fed the SHMR the Kroupa mass in every variant; the native rule has no SHMR, so it takes the baryons as they are).
- Nothing else changes: f_ex, x_e = 0.40, ν (each lane's kernel), the estimators, the data, the error models.
- No fitting. κ = ½ remains FITTED (it sets a₀ on both footings: 9.3603e-11 / 1.1312e-10 m s⁻²). The cold mass is still required; no dark-matter particle is added.

## 3. The profile (declared before running; no knob)

- **V1 (as committed):** the record's profile rule as-is, h48's `nfw_enclosed` — NFW, M_200c = M_c, Dutton & Macciò 2014 c(M). That c(M) is fitted to ΛCDM N-body haloes, so it is a ΛCDM input.
- **V2 (parameter-free):** a singular isothermal cold component truncated at the law's own turnaround radius: M_cold(<r) = M_c · min(r / r_ta, 1), r_ta = CFG7's `r_ta_law(M_b, a₀, ν_mono, a = 1)` at each footing's own a₀ (equivalently r_e / 0.40). It has no free parameter. The rule's added acceleration becomes f_ex (1 − f_b) G M_c min(r/r_ta, 1) / r².
- Both variants are run with the native mass. V1 is primary; V2 is reported in full. (If f_ex = 0 for an object the profile does not enter.)

## 4. Populations, statistics and scoring rules (copied, not changed)

Each lane's committed machinery is exec'd read-only (the lane's own MUTATE forced off). Where a call site must take the native M_c, the lane's source is exec'd with that call site replaced by a hook whose committed mode returns the lane's own function's value; control C1 proves the hooked harness reproduces the committed numbers.

| ID | population | lane | statistic and error (as committed) | gate (copied) |
|---|---|---|---|---|
| P1 | MW ultra-faints (31 + 9 limits) | CFG45 P1 / CFG42 H1 | Kaplan–Meier median of log σ_obs/σ_pred; bootstrap (1000, seed 42) ⊕ Υ_V floor ⊕ collapse-mass floor | A1: \|z\| < 2, both footings |
| P2a | MW classical dSph (14) | CFG45 P2 | sample median; 1.2533 std/√n ⊕ Υ_V floor ⊕ collapse floor | A2: z > −2, both footings |
| P2b | M31 Collins+13 (14) | CFG45 P2 | same | A2 |
| P2c | M31 LVD (34) | CFG45 P2 | same | A2 |
| P2d | LV field dwarfs (13) | CFG58 (d2) | same estimator without infall gas; same error recipe | \|z\| < 2, both footings |
| P3 | SPARC dwarfs (log M★ < 10) and log M★ ≥ 10 | CFG45 P3 | d log v at R_HI, canonical | A3: < 0.03 dex in ≥ 90% of each |
| P4a | UGC 2487 | CFG45 P4a | log V_flat/v_pred(R_HI), declared σ | A6: \|z\| < 2, both footings |
| P4b | Di Teodoro+23, 15 massive discs; the four S0/S0a | CFG45 P4b / CFG41 | corrected mean offset, CFG41 error | A7: S0 mean > −2σ_S0 (canonical); H2a \|mean₁₅\| < 2σ reported |
| P5 | SLUGGS, 19, h50 masses | CFG45 P5 / CFG38 | mean outer-bin offset, std/√19 | A4: \|z\| < 2, both footings |
| P5J | SLUGGS, 16, JAM-calibrated masses (γ = 3) | CFG55 | same, calibration on M_JAM/2 inside r_½ | CFG55 H2: \|z\| < 2, both footings; law H1 reproduced |
| P5S | SLUGGS, same 16, SLUGGS masses | CFG55 R1 | same | reported, \|z\| < 2 |
| P5L | SLUGGS, 16, JAM masses, Alabi+17 literature γ | CFG111 | same | CFG111 H2: \|z\| < 2, both footings |
| P6 | X-ray ellipticals (7) | CFG45 P6 | per-galaxy median over 5–70 kpc, mean ⊕ IMF ⊕ radial floor | A5: \|z\| < 2, both footings |
| P7 | Ogle+19 super spirals (23) | CFG45 P7 | mean offset | reported (CFG40 H2, 'no change from L') |
| P8 | SPARC rms (CFG4's weighted statistic, Υ 0.61, canonical) | CFG39 | rms change with the rule | < 0.005 dex (CFG39's clause); committed +0.0009 |

- **Collapse-mass floor term (satellites; CFG42/45/58 recipe).** The committed term is half the range of the statistic when the collapse mass of every satellite with M★ < 1e5 is set to 1e8, 3e8, 1e9, 3e9, 1e10 M☉, a span of ×0.1 to ×10 around the 1e9 clamp. Native primary: the same five values become factors ×0.1, ×0.3, ×1, ×3, ×10 on the native M_c (no clamp exists in the native mass). Reported beside it: the committed floor values substituted verbatim (not native).
- The two readings compared per population: (L) the bare law, (S) the rule. Columns reported: law alone (L), committed rule (S, Moster/Mandelbaum + NFW), native rule V1, native rule V2, both footings (canonical | alt), with offsets in dex and z.
- **Moves (declared classification):** for each gated row, FAIL→PASS and PASS→FAIL between the committed rule and the native rule V1 (and V2).

## 5. Controls (each can fail)

- **C1 (committed masses).** With the hook returning the committed Moster/Mandelbaum masses and NFW, the harness reproduces the committed rule and law values: CFG45's UF / CL / SPARC / UGC 2487 / DT23 / SLUGGS / X-ray / Ogle numbers (z, offsets, totals) to 1e-6; CFG58's field-dwarf medians and totals to 1e-6; CFG55's law and rule means (JAM and SLUGGS masses) to 1e-9; CFG111's law and rule means to 1e-9; CFG39's SPARC rms0 and rms1 to 1e-9.
- **C2 (M_c → 0).** With the hook returning 1e-30 M☉, every rule row equals the law row (reading L) of the same harness to 1e-9, both footings.
- **C3 (the native hook is the declared one).** Over every rule evaluation of the native run, M_c f_b / M_b = 1 to 1e-12, and the V2 profile satisfies M_cold(<r_ta) = M_c and M_cold(<r_ta/2) = M_c/2 to 1e-12.
- **MUTATE (separate output, `_MUTATE`).** f_b × 0.5 everywhere f_b enters the rule (M_c = M_b/(0.5 f_b) and the (1 − f_b) factor), native V1. Check as specified: every gated population's rule statistic shifts in the predicted direction (more cold mass: data/prediction offsets fall) by more than 1e-6 dex. The pre-flight (section 7) predicts this check FAILS, because the cold share rises only to 11.7 M_b, below the edge phantom of every object, so f_ex stays 0; a FAIL is kept and reported as such.
- Reported (no gate): the inertness margin k* = min over every scored object of M_ph,edge / [(1 − f_b) M_b / f_b], the factor by which the native cold mass would have to grow before the rule touches any object.

## 6. Declared checks of the main run

- **H1 [prediction from the pre-flight; can fail]:** under the native mass (V1 and V2) f_ex = 0 for every scored object, so every native rule row equals the law row to 1e-9.
- **H2 (reported):** the per-population table and the FAIL→PASS / PASS→FAIL moves against the committed rule, V1 and V2.
- **H3 (reported):** which gates the native rule passes (A1–A7, P2d, CFG55 H2, CFG111 H2, the SPARC rms clause), V1 and V2.

Outputs: `cfg313_native_rescore.py` → `.out`, `_results.json`; MUTATE → `_MUTATE.out`, `_MUTATE_results.json`; a final "N/M checks pass" line in each.

## 7. Hand pre-flight (computed before freezing, from the committed functions only)

M_c(native) = M_b/f_b = 6.364 M_b. Ratios below take M_b = M★ (the satellites add gas, which raises the native mass slightly and changes no conclusion). Moster from h48's `halo_mass`; Mandelbaum from CFG36's `collapse` (M_200c).

| object | M★ [M☉] | M_c(Moster) | M_c(native) | native / Moster | native / Mandelbaum |
|---|---|---|---|---|---|
| ultra-faint | 1e3 – 1e4 | 1.0e9 (clamp) | 6.4e3 – 6.4e4 | 6.4e-6 – 6.4e-5 | — |
| classical dwarf | 1e6 – 1e7 | 5.3e9 – 1.4e10 | 6.4e6 – 6.4e7 | 1.2e-3 – 4.6e-3 | — |
| M31 dwarf | 1e6 – 1e8 | 5.3e9 – 3.7e10 | 6.4e6 – 6.4e8 | 1.2e-3 – 1.7e-2 | — |
| L* galaxy | 5e10 | 2.0e12 | 3.2e11 | 0.16 | blue 0.32, red 0.14 |
| massive elliptical | 10^11.5 | 2.0e14 | 2.0e12 | 0.010 | red 0.039 |

The native mass is smaller than the ΛCDM collapse mass at every scale, by 5 dex for the ultra-faints and 1–2 dex for the massive ellipticals.

**The switch.** The law's own phantom inside the edge is M_ph,edge / M_b ≈ 6700 (1e3), 3800 (1e4), 1200 (1e6), 670 (1e7), 380 (1e8), 120 (1e10), 79 (5e10), 50 (10^11.5) on the canonical footing (alt about 15% higher). The native leftover needs M_ph,edge < (Ω_c/Ω_b) M_b = 5.36 M_b. That fails by a factor ≥ 9 at every mass, so **f_ex = 0 for every object and the native rule reduces to the bare law in every population, under either profile.** (This is CFG35's own remark: the cosmic share of today's baryons is only a floor.)

**Predicted direction of each population's shift (committed rule → native rule = law):**

| population | committed rule (z, canonical \| alt) | law (z) | predicted move |
|---|---|---|---|
| MW ultra-faints | −0.41 \| −0.41 | +3.77 \| +3.55 | up; PASS → FAIL |
| MW classical | −1.78 \| −1.90 | +0.32 \| +0.09 | up; stays pass |
| M31 Collins+13 | −0.22 \| −0.15 | +0.78 \| +0.55 | up; stays pass |
| M31 LVD | −2.67 \| −2.66 | +0.60 \| +0.42 | up; FAIL → PASS |
| LV field dwarfs | −3.47 \| −2.70 | −0.60 \| −0.85 | up; FAIL → PASS |
| SPARC (both classes) | 100% / 98% | 100% / 100% | the rule's UGC 2487 touch vanishes; pass |
| UGC 2487 | −1.05 \| −1.02 | +0.90 \| +0.68 | up; stays pass |
| Di Teodoro S0 / all 15 | −0.80 / −0.71 | +0.05 / −0.43 | up; stay pass |
| SLUGGS h50 masses | +0.39 \| +0.10 | +3.28 \| +2.67 | up; PASS → FAIL |
| SLUGGS JAM (γ = 3) | +2.58 \| +2.60 | +3.99 \| +3.65 | up; FAIL stays FAIL |
| SLUGGS SLUGGS masses (16) | +0.36 \| +0.12 | +2.75 \| +2.23 | up; PASS → FAIL |
| SLUGGS JAM, literature γ | +1.55 \| +1.64 | +3.60 \| +3.22 | up; PASS → FAIL |
| X-ray ellipticals | +1.04 \| +1.03 | +1.70 \| +1.58 | up; stays pass |
| SPARC rms | +0.0009 | 0 | to 0; pass |

MUTATE (f_b × 0.5): the cold share becomes 11.7 M_b, still below every edge phantom (≥ 50 M_b), so the predicted shift is zero everywhere and the MUTATE check is predicted to FAIL.

## 8. Rules

No fitting and no knob scans; nothing here is tuned to the data. No downloads. Other lanes' files are read, never edited. No personal names or absolute home paths in files. A failure is a valid result. Nothing here says the theory is closed.
