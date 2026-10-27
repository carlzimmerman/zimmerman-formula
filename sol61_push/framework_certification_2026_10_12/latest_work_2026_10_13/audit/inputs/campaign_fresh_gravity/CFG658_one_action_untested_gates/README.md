# CFG658: the one-action construction on the gates it had not faced

**Label: C\* FAILS C3 (early types, Z 3.7) and the X-COP cluster gate as built (η 1.81 / 1.67 at 1000 kpc; inner band 3.1 / 2.9).
It PASSES the EFE gates: wide binaries are consistent with DR3 because stiffness screens them, satellites match because of the
basin rule, and star halos are 3.5% of the star's mass. It passes CFG686's cluster shear (LAW SUFFICES), the same as ν_mono. The
CFG652 groups exclude both sources. D2 (context only): the kernel moves the halo-model excess by +0.003. The kernel change alone
changes no verdict of the record anywhere.**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (12c5ab6b3), 2026-10-13, before any CFG658 number.
- **C\*** is CFG694's action, plus CFG695's saturating vacuum (static law g_N = g²/(g + a₀), i.e. ν_s = ½ + √(¼ + 1/y)), plus
  CFG691's stiffness at L\* = 5.75 pc, plus CFG693's free-fall basins.
- **Rule:** every harness is executed read-only, and only its kernel is swapped. The Lean chat's lanes (CFG690–699) are read only.
- **Settings:** κ = ½ is FITTED. Footings are never pooled. "Cold energy" throughout, and its mass is still required. No ΛCDM or
  standard-MOND yardstick enters a verdict. Not "theory closed". Nothing here says the data favour the framework.
- **Machine:** one process at a time, nice 10, peak RSS ≤ 1.51 GB. No PM was run, nothing was downloaded, and `cfg650_pm.py` was
  not touched.

## Scripts (all exit 0; MUTATE reproductions run in the same pass)
| script | gate | time |
|---|---|---|
| `cfg658_cl3_models.py` | CFG652 model ESDs with ν_s (x1), stored-kernel control | 30 min |
| `cfg658_clusters.py` | CL1 CFG686, CL2 X-COP (CFG4 + CFG634 T3), CL3 CFG652 | 2 min |
| `cfg658_c3.py` | C3-R (verdict), C3-A (context) | 13 min |
| `cfg658_efe.py` | E1 wide binaries, E2 satellites, E3 star nodes | 15 s |
| `cfg658_d2_sparc.py` | S0 SPARC control, D2 halo-model context | 40 s |

Each script writes `<name>.out` and `<name>_results.json`. The CFG652 per-group models are cached in
`_external_data/cfg658_work/`, which is not committed.

## Results (canonical / alt)

| gate | C\* (ν_s) | harness kernel (reproduced) | label |
|---|---|---|---|
| **S0** raw SPARC | 0.1009 @ Υ 0.60 / 0.0994 @ 0.55 | ν_mono 0.1003 / 0.0991 | control PASS (= CFG695) |
| **C3-R** CFG669 T2, Ks masses: early/late at matched M_b | A_obs **+0.280 ± 0.083**; A_law **−0.027 / −0.027**; D = +0.307, **Z +3.69 / +3.69** | ν_mono A_law −0.027 (identical) | **FAIL** |
| C3-A CFG531 ε, all f30, K-in / K9 (CONTEXT) | +0.340 / +0.384 ; +0.229 / +0.265 | +0.342 / +0.385 ; +0.231 / +0.265 | Δε −0.002 (a hair *more* mass) |
| C3-A early types, K-in / K9 (CONTEXT) | +0.536 / +0.831 ; +0.409 / +0.675 | +0.538 / +0.832 ; +0.411 / +0.676 | shortfall unchanged |
| **CL1** CFG686 shear, A INNER / MID / OUTER | 2.68 / 1.69 / **1.02 ± 0.24** ; 2.49 / 1.56 / **0.94 ± 0.24** | 2.70 / 1.70 / 1.02 ; 2.51 / 1.57 / 0.94 | **LAW SUFFICES** both (14/18 brackets; 4 CORE EXCESS) |
| **CL2** X-COP B\|R0 (all baryons, no reservoir = C\* as built) | η **1.813 ± 0.066 / 1.673 ± 0.062**; inner **3.146 / 2.914** | 1.820 / 1.679 ; 3.163 / 2.927 | **FAIL** (headline and inner) |
| X-COP HCB\|R0 (condensed only, A5) | 3.972 / 3.805 ; inner 5.200 / 4.982 | identical to 3 decimals | FAIL |
| X-COP RI (identity, either source) | 1.057 / 1.057 ; inner 1.535 | same | headline PASS, inner FAIL |
| X-COP RNc4: B / HCB | B 1.082 / 1.115 (inner 1.462 / 1.583); HCB 0.895 / 0.898 (inner 0.890 / 0.897) | same | B: headline PASS, inner FAIL; **HCB+RN passes both** |
| **CL3** CFG652 eFEDS: (a) condensed χ²/8, (b) all baryons χ²/8 | (a) 22.5 / 23.5; (b) 28.7 / 25.1; Δχ² +6.2 / +1.6 | (a) 22.9 / 22.3; (b) 28.7 / 25.2 | **BOTH EXCLUDED** |
| **E1** wide binaries, basin only (EFE-blind ν_s) | γ̂ ≥ 1.50 (pinned); **+7.73σ / +8.25σ** | = CFG447 ν_P2 row exactly | EXCLUDED BY DR3 |
| **E1** wide binaries, C\* (basin + stiffness) | γ̂ **1.016 / 1.020** (spread 0.046); **−0.82σ / −0.83σ** | — | **CONSISTENT** |
| **E2** satellites, basin rule | χ² **0.7 / 0.6** of 5 (p 0.98 / 0.99); r_J/r_bg 0.96–1.34 / 1.01–1.40 | basin off (EFE on) ν_s: 97.1 / 93.2 | **PASS** |
| **E3** star node: M_ph/M inside min(r_J, 1.08 pc) | **0.0352** (1 and 0.3 M☉); saturation changes it by ≤ 2e-8 relative (ε = r_M/ℓ_γ ≤ 9e-5) | cubic 0.0352 (= CFG694 G3) | **PASS** (≤ 0.155) |
| D2 CFG556 halo model (CONTEXT ONLY) | E **+0.718 / +0.886**; R(1) 1.719 / 1.888; σ8 ratio 1.0403 / 1.0464 | recorded kernel +0.715 / +0.883; ν_mono identical to 1e-8 | ΔE **+0.003**; edge radii unchanged |

**MUTATE: every reproduction is exact.**
- **CFG686:** the predictions and the A table, including the bootstrap σ, match with |d| = 0.
- **X-COP:** CFG4 η and all six CFG634 T3 cells (headline and inner) match with |d| = 0.
- **CFG652:** the stored models give the recorded χ² exactly. Five groups recomputed with the stored kernel equal the stored ESDs (0.0).
- **C3:** CFG531's ε for all, early and late, in both constructions and both footings, matches with |d| = 0, and A_obs = CFG669.
- **EFE:** CFG478 Q1 (basin off) matches with |d| = 0; CFG447's ν_P2 rows (no stiffness) match exactly; E3 at ε = 0 gives 0.0352.
- **D2 and SPARC:** CFG556 E matches with |dE| = 0, and SPARC ν_mono gives 0.1003 / 0.0991.
- **The M-T tooth bites:** early model mass × 10^0.3 moves A_law by +0.156, so C3-R can see a type-dependent mass.

## Reading
1. **The kernel swap is inert everywhere except SPARC's Υ.**
   - At matched baryons, ν_s and ν_mono differ by less than 1% in every cluster, group and early-type statistic here.
   - So **C3 fails exactly as before.** The early/late excess at matched Ks baryonic mass is a ratio. Any morphology-blind law
     predicts it to be about 0 (A_law −0.027, the same for both kernels). The data give +0.280.
   - ν_s does not add mass at 50–100 kpc. Relative to ν_mono it adds a hair (Δε −0.002), which is far below the +0.3–0.5 shortfall.
   - The one-action construction gives no route to C3 unless the action itself reads morphology.
2. **The EFE gates are where C\* earns something, and every piece is load-bearing:**
   - **Basins without stiffness:** wide binaries feel the full EFE-blind law, which is excluded at 7.7σ / 8.3σ (the CFG447
     result, reproduced).
   - **Basins with stiffness:** wide binaries are Newtonian (anomaly/Newton ≤ 8e-3 across the pipeline's pairs) and consistent
     with DR3 at −0.8σ.
   - **Satellites:** their basin edge sits at r_J/r_bg ≈ 1 (host slope 1.87–2.0, as CFG693 T2 predicted), so they keep their
     isolated boost (χ² 0.6–0.7). With the EFE on they fail at χ² 93–97.
   - **Stars:** star halos are capped at 3.5% by stiffness.
   - So C\* is the first construction on the record that passes all three EFE-type gates at once. It does so with two rules that
     are definitions, not results of varying the action (B1 is still open). It predicts no wide-binary boost, unlike the law.
     Gaia DR4 decides, and the frozen DR4 pre-registration is not edited.
3. **Clusters: as built, C\* fails.**
   - C\* is a pure field with no cold-energy reservoir. Its prediction is the law on all baryons. That fails X-COP's hydrostatic
     masses at 1000 kpc (η 1.81 / 1.67) and much worse inside (2.9–3.1 at 200–420 kpc).
   - Shear at 1.2–3 Mpc around 8 clusters is matched by the same all-baryon law (A_outer 1.02 / 0.94). Raw lensing far out and
     X-ray hydrostatics inside therefore disagree about how much mass the law needs. Part of this is CFG686's extrapolated gas, and
     part is that its inner band is unusable.
   - The only cell passing both the X-COP headline and the inner band is HCB + RN: condensed source plus an NFW-shaped reservoir.
     That needs (i) a phase label and (ii) a cold-energy reservoir. C\* has neither.

## A5 tension (frozen reading applied)
- **C\* is sourced by all baryons.** P responds to ∇Φ, and Φ is sourced by all of ρ_b. Hot gas therefore polarizes the vacuum
  exactly as stars do. The action has no phase label, so it cannot express Theory v2's A5 (phantom sourced by condensed baryons
  only) without an added term.
- **The data do not settle which source is right:**
  - CFG686 shear supports the all-baryon source far out.
  - X-COP prefers condensed + reservoir inside (HCB+RNc4 is the only cell passing both bands; all-baryon + reservoir fails the
    inner band at 1.46 / 1.58).
  - The CFG652 groups exclude both.
- **Either way, C\* and v2 disagree.** If A5 is kept, the action needs a phase-dependent coupling, which is a new structure that R0
  would judge. If C\* is kept, v2's cluster and growth wins that came from A5 are lost: CFG636's census-capped condensed source,
  the Bullet's gas-tied share of 0, and the X-COP inner band.

## D2 context and the PM spec
- **The halo-model excess is set by the supply and the census edge, not by the kernel.**
  - Edge radii r_e/r_ta are identical for all three kernels.
  - ν_s raises E by +0.003, to +0.718 / +0.886.
  - The kernel swap therefore leaves CFG596's D2 failure where it was. Any change must come from the source and supply rules,
    which are T12's modules.
- **A native test is specified, not run.** See `PM_SPEC_1024.md`:
  - K12 = T12 + ν_s, as a same-seed pair against T12;
  - K0 = the all-baryon source with ν_s, against S0;
  - start condition, abort rule and scoring as in CFG650.

## Disclosures (2026-10-13)
1. **E2 bug, caught on the first run, before any verdict text.** The basin edge was computed as log r instead of r: the `exp` was
   missing, so r_J came out as 0 and χ² as 131.6, a FAIL. The fix is one token. The criteria are unchanged and both runs used
   the same rule. The fixed run is the one committed.
2. **CL1 first run** stopped on a missing bin-centre variable (`RC`) before printing any number. The fix execs CFG686's
   `EDGES … RC …` line read-only.
3. **Seen before the freeze:** CFG531's committed ν_simple rows at a₀ rescaled by CFG468 (+0.389 / +0.269). This lane recomputes
   them at the footings.
4. **CL3 scope:** only the x1 variant was run, as declared. CFG652's M_cond ±0.2 dex and gas-extent variants were not re-run with
   ν_s.
5. **E1 approximation:** g_an uses CFG691's cubic profile. E3 shows the saturating correction is at most 2e-8 relative.
6. **C3-R model:** own profile only (point mass plus phantom to r_ta), with no environment term. That is the framework-native
   choice declared in the criteria. A ratio test is insensitive to an environment term that does not depend on type.
