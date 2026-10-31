# Brief for Argon: route E after the final-mile push (2026-10-30, evening)

This replaces this morning's ARGON_BRIEF_2026-10-30. Every number comes from a lane output on the record. Lane names are given so you can ask for any file. Footing is canonical unless I say alt. Z < 0 means the model is above the data (OVER).

**Update, 10-31 morning. Sections below are as of 10-30; three new cluster lanes are listed here.**
- **XH1:** FC1's rule on X-COP's hydrostatic masses: FAIL at both f★, mean −0.073, rms 0.139 (pass line 0.05, 0.10). Too heavy at 0.2–0.7 R500, which agrees with the shear's MID and OUTER excess. In 0.15–0.46 Mpc X-COP has the model × 1.23 over where G-IN-Mall has × 1.90.
- **MA1:** Σ_coll(M) is defined for collapsed mass. SPARC and groups pass M200, but clusters were passing the mass out to r_ta. With M₂₀₀ on all paths, solved self-consistently, S falls × 0.857 and the frozen label is MASS ARGUMENT PASS at both f★: worst key −1.45, −1.55. It holds at η × 1.1144 (−1.85) and fails at × 1.206. **But it isn't robust:** with S at each cluster's own z_obs (median 0.22), S rises × 1.26 and G-IN-Mall fails at −2.33, G-MID-T3 −1.96 (post-result). That omission is in every earlier lane.
- **NZ1:** r₀ from the zooms as well, r₀ = r_f/a with η = (4/3) a²/B(a); budget r₀ is × 1.6 larger. Frozen label X-COP PASSES, KEYS BREAK: X-COP mean +0.047, rms 0.087, with no fitted parameter, and SPARC's line holds. G-OUT-M3 +5.10, G-OUT-Mall +3.06, G-MID-T3 +2.40, groups Z +3.98. r₀ × 1.5 flips it: keys pass, X-COP rms 0.125. GX1 found the same trade for the r⁻⁹ᐟ⁴ family.
- **Open question for you:** no zoom has been run past z_f. The mass arriving after z_f has to land inside R₂₀₀ ≈ 1.12 r_f. Is continuing seeds 1–3 at 10¹³ and 10¹⁴ to z = 0, then reading M(<r) against X-COP and the shear, the right test?
- **A4:** 8 of 18 zooms done at 07:10, the last expected mid-afternoon. X80 follows, then A5.
- **What A4 can do to FC1 (`FC1_cold_share_native_eta/fc1_a4_expect.out`, reported, not a grade):** with η at 10¹³ and 10¹⁴ × g, G-IN-Mall reaches −2 at g ≈ 1.016. The SPARC line stays at Υ 0.50 or above up to g 1.114, so A4 threatens clusters and not the line. At 10¹², ng 48 → 64 moved converged η × 1.114 (68 % 0.84–1.21, two samples of different fields). At that g the rule fails at both f★: G-IN-Mall −2.32, G-MID-T3 −2.08 at f★ 0.034. Below about g 0.999 it would pass at both.
- **ET3–ET6, landed after this brief was written:** the ×2 rise in S from V_flat 20–60 to 100–150 km/s survives beam, pressure, inclination, distance, quality cuts, a Υ trend, their joint grid and four core shapes. Systematics reach at most about ×1.4 from a flat truth. The flat floor is still not rejected: its grade stays MIXED at the base, and generous corners contain alt's floor. No mechanism is identified. Real per-galaxy beams and 3D modelling are untested.

## 0. Where it stands

1. **Route E now reaches the grader's edge with no external c_f.** The zooms' surface density is for total matter, and the grader had been applying it to the cold share alone. Converting it (factor f_c = 0.84055, no knob) takes the converged native rule from FAIL to Υ 0.51 / 0.50, all 15 cluster keys, groups (FC1). At f★ 0.0615 it fails by 0.004 in Z. It was found post hoc, after I had seen the required softening.
2. **That edge requires the cold fluid not to respond to baryons at all.** Contraction breaks SPARC (Υ 0.31) and no softening on the grid repairs it (CN1). Undoing it costs 9 % of SN energy; the gravity-only channel delivers about 0.3 %.
3. **Clusters have room for about +1.5 % in S.** Blumenthal expands the cold fluid there, which looked comfortable. But non-radiative hydro runs report the opposite sign, concentration +10 %, and that fails G-IN-Mall and G-MID-T3 (CN1c). I told the owner clusters were "comfortable". That claim does not stand.
4. **The floor may not be needed.** The collapse branch alone, with no a₀ anywhere in the cold sector, passes the SPARC line: Υ 0.71 / 0.73 with η flat, Υ 0.55 / 0.56 with η continuing its native trend (NF1). Footings then coincide. Clusters and groups don't change. The floor is what over-predicts the most gas-rich dwarfs. This is SPARC only, it extrapolates below any zoom, and it would take a₀ out of the cold sector. That is the owner's call.
5. **Lensing on photometric isolation: the law wins, and your slope test agrees.** B21's isolated bins give γ 0.955, 0.860, 1.014 (AS1). Route E loses by Δχ² +434 (X53 harness).
6. **Lensing on spectroscopic isolation (samples S1, S3, defined in 4e): not powered, and it leans the other way.** S1 γ 1.40 ± 0.33, raw 1.57 ± 0.27; models: law 0.96, route E 1.57 (AS1). χ²: S3 route E 12.6, law 17.8, D 2.51; S1 route E 24.4, law 15.8, D 4.26 (SI1).
7. **Mass offset:** at catalogue M★, route E's M200 needs +0.22 on S1, +0.26 on KiDS, +0.17 on G09, +0.43 on S3, and +0.03 on blue KiDS lenses. S2's red stellar-mass ladder (R2, +0.295 dex for red) applied to both models puts S1 level (Δχ² −0.3, D 4.63) and S3 NOT POWERED. Conditional on R2 (SI2).
8. **Not fixed:** Milky Way (wide priors only), L★ −16 km/s (law −12.5), 250–400 km/s −57 (law −40), IC 1613, J0946, law's scatter is still lower (0.054 vs 0.067). κ is fitted. Core shape is chosen: zooms make cusps.

## 1. Rules for your answer

**Standing rules**
- κ = ½ is FITTED. Never say "theory closed" or that the data favour the framework.
- Footings are never pooled: canonical a₀ = 9.3603e-11 m/s² (Σ_a0 = a₀/2πG = 106.85 M☉/pc²); alt a₀ = 1.1312e-10 (129.13).
- The name is "cold dark energy": a gravitating w ≈ 0 field component, never "cold dark matter" and never a particle.
- No ΛCDM inputs: no Planck 5.364, no f_b = 0.157, no borrowed c(M), no ΛCDM background. Published simulation results may be cited as physics context for sign and size. They can't be inputs to a grade.
- Criteria are frozen and committed alone before any script or number. A fail gets checked as hard as a win.

**What I can't use**
- A number back-solved from its target, or inputs chosen to reach a result. State where each input comes from.
- A closed form with no numerical check.
- Hard-coded targets described as "zero hard-coded targets". Your last script did this.
- "Final theory", "Nobel", "proves".
- Anything in the closed list (section 11) unless you say what is new.

"No new idea" is a useful answer.

**Paste problem.** Your last reply reached me scrambled from the end of Q2 through Q4: the words were alphabetically sorted. I could not read that part. If it mattered, resend it, ideally with less inline LaTeX.

## 2. Your last reply, checked

| Your claim | Check | Result |
|---|---|---|
| 8/3 correction; TL1 and X39 claims dropped | recomputed | fine |
| Q1: the law column "proves" a baryon M★/L effect at L★ | law ΔV at 200–250 is −12.5 canonical but −5.0 alt, so it tracks a₀, and it isn't a pure baryon property. EM1 already carries bulges at 1.4Υ | **not supported** |
| Q1: the η 25.94 knee lifts 150–200 km/s off the floor | η 21.2 at 10¹² gives 145 > 107 as well, so it doesn't single out 25.94 | not specific |
| Rank 3 / LS2: bulge split on LS1 | this is ET1: SAMPLE-LEVEL, NO BULGE SIGNAL, NO TREND above 150 km/s | already done |
| Q2: COS cool-gas census numbers | not verified here | do not rely on them |
| Q2: the deficit means isolated halos aren't the answer at 10¹² | true on photometric lenses. On clean lenses not shown, see Rank 1 | **premature** |
| Q3: f_clump 2.66 %, 2.11 % | arithmetic right. Zooms already contain collisionless sinking; only baryonic clumps are new | not needed unless S must fall |
| Rank 1: γ over 150–800 kpc, 1.00 vs 1.675 | run as AS1, your cuts plus σ_γ ≤ 0.225. Full models give 0.96 and 1.57, so your bare numbers were good | **you are right on B21; not powered on clean lenses** |
| Rank 2: kSZ with positive control | done as GH7 → GH8 → GH9. A(1.8) 0.24 ± 0.19 meets your falsify cut (< 0.35, σ ≤ 0.20). Control S/N 4.27 misses your gate of 5 | meets the cut, control short. See 4f for why this no longer decides route E |
| Script: "zero hard-coded targets" | hard-coded tables and printed takeaways | false |

## 3. The theory under test, exactly

### 3a. Rule
Gravity is plain Newtonian. The a₀ law g = ν(g_N/a₀) g_N is emergent, not fundamental. Each halo is cold dark energy with

ρ(r) = ρ₀ (1 + x²)^(−3/2), x = r/r₀; M(<r) = π S r₀² B(x); B(x) = 4[asinh x − x/√(1+x²)]; S ≡ ρ₀r₀.

Two versions now compete:

- **Version F (floor):** S_cold(M) = max(Σ_a0, f_c η(M_t) Σ_coll(M_t)), M_t = M/f_c.
- **Version N (no floor):** S_cold(M) = f_c η(M_t) Σ_coll(M_t) at every mass. N0: η flat below 10¹². N1: η × 10^(0.0927 (12 − lg M_t)) below 10¹². N2: slope 0.1668.

r₀ is solved from M(<R200) = M200 for galaxies, and M(<r_ta) = M_fair for clusters and groups. The halo continues to r_ta.

### 3b. Numbers in the rule
| Quantity | Value | Source |
|---|---|---|
| f_c = (Ω_m − Ω_b)/Ω_m | 0.84055 (R_nat = 5.27) | native background: Ω_m 0.2976016, h 0.6856427, ω_b 0.0223081 |
| η, converged, 10¹² / 10¹³ / 10¹⁴ | 25.94 [23.89, 26.53] / 17.67 [16.73, 19.86] / 16.91 [15.68, 18.39] | X81, CE1; ng 64 / ng 48 / ng 48 |
| f_c η | 21.80 / 14.85 / 14.22 | FC1 |
| c-equivalent | 8.05 / 5.92 / 5.72 | CE1 |
| Σ_coll at 10¹¹…10¹⁵, M☉/pc² | 3.83, 6.84, 11.95, 20.48, 34.71 | X43, own P(k) |
| z_f at same masses | 1.137, 0.944, 0.751, 0.562, 0.385 | X43 |
| Galaxy M200 | lg M200 = 11.18 + 0.90 (lg M_b − 10) | EM1, **fitted** on SPARC with NFW halos |
| Cluster and group M_fair | baryons × (1 + R_nat) inside self-consistent r_ta | GC2, X43 |
| Cluster gas | X-COP slope 2.7774 [2.6756, 3.0711] extrapolated to r_ta; f★ 0.034 (A1) or 0.0615 (X-COP) | GS1, X73 |

Definition of η: η = ρ₀r₀/(18π² ρ̄_m(z_f) r_vir) = (4/3) a²/B_S(a), a = r_vir/r₀, from the smooth core fitted to a halo's mass profile. "Converged" means the fit to that halo's NFW with the inner cut removed (x_c = 0.001).

Crossing in version F, canonical: lg M_t = 11.43, lg M_cold = 11.35. Alt: 11.75, 11.68. Active on SPARC: 59 of 175 canonical, 48 alt.

**Example, lg M★ 10.78 lens:** lg M200 11.94, R200 201 kpc, r_ta 851 kpc, S 150, r₀ 14 kpc.

### 3c. What is derived and what isn't
| Item | Status |
|---|---|
| κ = ½, so Σ_a0 | fitted, by hand in the rule. Absent from version N |
| η(M) | native zooms, collisionless. Cluster masses ng 48 until A4 |
| f_c | native, no knob, post hoc in origin |
| Core shape | **chosen.** Zooms make NFW cusps (a/a_NFW 0.95–1.06, X81). Cusped halos fail SPARC's Υ leg (EM1 NFW 0.36) |
| EM1 a, b | **fitted.** X76_galaxy_fair_share_halos: fair share on observed baryons is 0.2–0.3 dex lighter and needs ×10^0.85–0.90 in baryons |
| Two halo-mass rules | galaxies EM1, clusters fair share. Not unified |
| f★, gas slope | measured, but the slope is extrapolated past the data to r_ta |
| R2 | from the record, conditional. Lens tests only |
| Υ | free per galaxy on a grid 0.30–1.20; line tests the median |

### 3d. Grader (X74)
- **SPARC line:** rms ≤ 0.110 and median Υ in [0.50, 0.80] on backgrounds A and B.
- **Clusters:** 15 keys, |Z| ≤ 2, in h 0.672 and 0.686 cells. IN (bins near 0.15–0.46 Mpc), MID (by kT tercile and slope), OUT (1.42–3 Mpc, by kT and M_gas tercile). The values below are in the grader's own units.
- **Groups:** |Z| ≤ 2 on 63 groups.
- Separate: MW (Eilers v_c 229.1 ± 4.6, K_z, Ou+24), KiDS bins 3–4, lens tests.

**Weakness in my own grader:** the 15 keys have no joint statistic. They share clusters and are correlated, and at FC1 all 13 amplitude keys sit on the OVER side (table in 4a). "All pass" is not a joint fit.

## 4. Results since this morning

### 4a. FC1: the cold share (criteria 061b2e2a1a)
X48 evolves all of Ω_m as dust and X43's Σ_coll uses total density, so η Σ_coll is a total-matter S. The grader used it for the cold halo and then added baryons on top. Applying f_c keeps the zoom's r₀ exactly.

| f★, η point | Υ (A/B) | groups Z | G-IN-Mall (h 0.672/0.686) | G-MID-T3 | result |
|---|---|---|---|---|---|
| 0.034, median | 0.51 / 0.50 | +1.62 | −1.95 / −1.64 | −1.71 / −1.13 | **PASS** |
| 0.034, p16 | 0.52 / 0.52 | +1.67 | −1.70 / −1.44 | −1.45 / −0.89 | PASS |
| 0.034, p84 | 0.49 / 0.49 | +1.55 | −2.23 / −1.88 | −2.00 / −1.40 | FAIL |
| 0.0615, median | 0.51 / 0.50 | +1.62 | **−2.004** / −1.69 | −1.93 / −1.34 | **FAIL by 0.004** |
| 0.0615, p16 | 0.52 / 0.52 | +1.67 | −1.75 / −1.48 | −1.66 / −1.09 | PASS |
| 0.0615, p84 | 0.49 / 0.49 | +1.55 | −2.29 / −1.93 | −2.23 / −1.62 | FAIL |

Frozen label: **F★-DEPENDENT.** Without the factor (CE1): Υ 0.48, G-MID-T3 −2.30, G-IN-Mall −2.55. Rms 0.0687 / 0.0700. Alt: COLD-SHARE FAIL, Υ 0.44, X78's law-level failure.

**All 15 keys, f★ 0.034, h 0.672 (measured ± s, prediction, Z):**
| key | meas ± s | pred | Z | key | meas ± s | pred | Z |
|---|---|---|---|---|---|---|---|
| G-IN-all | 2.11 ± 1.82 | 4.81 | −1.49 | G-OUT-T1 | 0.48 ± 0.38 | 0.80 | −0.84 |
| G-IN-Mall | 2.49 ± 1.15 | 4.72 | **−1.95** | G-OUT-T2 | 0.74 ± 0.27 | 0.99 | −0.93 |
| G-MID-T1 | 1.17 ± 0.40 | 1.76 | −1.48 | G-OUT-T3 | 1.18 ± 0.25 | 1.38 | −0.78 |
| G-MID-T2 | 1.76 ± 0.34 | 2.08 | −0.96 | G-OUT-b | 1.67 ± 0.76 | 1.35 | +0.42 |
| G-MID-T3 | 2.28 ± 0.27 | 2.75 | **−1.71** | G-OUT-Mall | 0.93 ± 0.10 | 1.08 | −1.55 |
| G-MID-b | 2.43 ± 0.80 | 2.31 | +0.15 | G-OUT-M1 | 0.49 ± 0.30 | 0.58 | −0.30 |
| G-OUT-all | 0.85 ± 0.17 | 1.09 | −1.50 | G-OUT-M2 | 0.76 ± 0.14 | 0.95 | −1.37 |
| | | | | G-OUT-M3 | 1.37 ± 0.10 | 1.51 | −1.31 |

**Which way the known biases push.** FP2: measured c is a lower bound, since softening and relaxation flatten profiles. X81: true η is if anything higher than 25.94. The p84 line (+2.3 % in η) already fails. So the known biases point toward failing.

### 4b. CN1: contraction on FC1's rule (criteria 38a6fb863e)
Frozen label, both footings: **CONTRACTION BREAKS (SPARC line); R_SPARC NONE ON GRID; R_CL 1.0.** Collapse-branch systems only. R is a softening of S before contraction.

| R | Υ can. | Υ alt | G-IN-Mall | G-MID-T3 | cluster fails |
|---|---|---|---|---|---|
| 1.00 | 0.31 / 0.31 | 0.30 | −1.30 | −1.00 | none |
| 0.80 | 0.33 / 0.33 | 0.30 | −0.76 | −0.31 | none |
| 0.60 | 0.36 / 0.36 | 0.33 | −0.17 | +0.58 | none |
| 0.50 | 0.39 / 0.39 | 0.36 | +0.14 | +1.13 | none |
| 0.40 | 0.44 / 0.44 | 0.37 | +0.47 | +1.79 | G-MID-T3 UNDER |
| 0.30 | 0.48 / 0.47 | 0.40 | +0.81 | +2.59 | G-MID-T3, G-MID-b UNDER |

Gnedin at R 1: Υ 0.34 / 0.35.

**Υ / ΔV at Υ 0.50 by V_flat (km/s, 2–4 R_d):**
| R | 150–200 | 200–250 | 250–400 |
|---|---|---|---|
| 1.0 | 0.30 / +39.2 | 0.34 / +33.2 | 0.46 / +11.0 |
| 0.8 | 0.30 / +32.7 | 0.39 / +24.8 | 0.49 / +2.7 |
| 0.6 | 0.34 / +24.3 | 0.42 / +13.8 | 0.54 / −6.8 |
| 0.4 | 0.41 / +11.6 | 0.48 / −1.2 | 0.59 / −18.7 |
| 0.3 | 0.47 / +4.3 | 0.56 / −10.9 | 0.65 / −26.0 |

Softening needed falls with mass: R ≈ 0.3, 0.4, 0.8, none in clusters.

**Energy to undo contraction** at Υ 0.50 (post-result): median **0.094 of E_SN** [0.055, 0.122], max 0.157, by bin 0.043 / 0.070 / 0.100 / 0.125. Inside the budget. But CM1's gravity-only channel at measured gas puts about 0.3 % of E_SN into the cold fluid, **about 30× short**.

**Context, from search excerpts, provisional, not an input:** NIHAO IX finds the response ranges from strong contraction to expansion and tracks star-formation efficiency and stellar compactness. Later NIHAO work adds a dependence on the star-formation threshold and puts contraction above M★/M_halo ≈ 0.03. Some stronger-feedback runs report weak contraction or none at MW mass. So net response ≈ 0 at L★ is reported in some hydro runs, through baryon-driven feedback this record cannot reproduce with gravity-only cycles.

### 4c. Clusters: the sign of the net response
**CN1b (post-result, selective: Blumenthal + BCG on clusters, none on SPARC):** in clusters the hot gas is less concentrated than the cold fluid, so Blumenthal expands the cold fluid.

| f★, η | Υ | G-IN-Mall | G-MID-T3 | G-OUT-M3 | G-OUT-all | failing |
|---|---|---|---|---|---|---|
| 0.034 med | 0.51 / 0.50 | −1.30 | −1.00 | −0.98 | −1.37 | none |
| 0.034 p16 | 0.52 / 0.52 | −1.11 | −0.77 | −0.84 | −1.32 | none |
| 0.034 p84 | 0.49 / 0.49 | −1.52 | −1.26 | −1.14 | −1.43 | SPARC line |
| 0.0615 med | 0.51 / 0.50 | −1.35 | −1.21 | −1.13 | −1.54 | none |
| 0.0615 p84 | 0.49 / 0.49 | −1.57 | −1.48 | −1.29 | −1.60 | SPARC line |

**Why I no longer lean on this.** It is selective. And Blumenthal has no energy exchange. Non-radiative hydro runs starting from dust plus gas report dark matter concentration **up by about 10 %** ([Rasia+04](https://arxiv.org/abs/astro-ph/0309405), [Lin+06](https://arxiv.org/abs/astro-ph/0607555); from search excerpts, ΛCDM backgrounds, not inputs). Lin+06 attribute it to the collisionless component losing energy to the gas.

**CN1c: what the clusters can take (S × R_c, no contraction):**
| R_c | f★ | G-IN-Mall | G-MID-T3 | keys over 2 |
|---|---|---|---|---|
| 0.90 | 0.034 | −1.61 | −1.35 | none |
| 0.95 | 0.034 | −1.78 | −1.54 | none |
| 1.00 | 0.034 | −1.95 | −1.71 | none |
| 1.05 | 0.034 | −2.11 | −1.88 | G-IN-Mall |
| **1.126 (c +10 %, η ∝ c^(5/4))** | **0.034** | **−2.35** | **−2.12** | **G-IN-Mall, G-MID-T3** |
| 1.00 | 0.0615 | −2.00 | −1.93 | G-IN-Mall |
| 1.126 | 0.0615 | −2.42 | −2.35 | G-IN-Mall, G-MID-T3 |

**Room on the high side: about +1.5 % in S.** SPARC's line has about the same room at 10¹² (p84, +2.3 %, gives Υ 0.49); moving η at 10¹³ and 10¹⁴ alone leaves it at 0.50 or above up to × 1.114 (`fc1_a4_expect.out`).

### 4d. NF1: no floor (criteria f95621e30a)
ET1 and ET2 measured the S SPARC asks for below 150 km/s: 69, 103, 143 with M200, and 70, 108, 158 free (rise ρ +0.60, +0.556). A flat floor reads MIXED. The collapse branch runs parallel to that rise.

| Variant | Υ (A/B) | rms (A/B) | line |
|---|---|---|---|
| F canonical | 0.51 / 0.50 | 0.0687 / 0.0700 | pass |
| F alt | 0.44 / 0.44 | 0.0719 | fail |
| **N0** | **0.71 / 0.73** | **0.0678 / 0.0688** | **pass** |
| **N1** | **0.55 / 0.56** | **0.0670 / 0.0681** | **pass** |
| N2 | 0.47 / 0.48 | 0.0695 / 0.0706 | fail |

Frozen label, SPARC only: **FLOOR NOT NEEDED.** Canonical = alt exactly. Clusters and groups: ΔZ = 0. Line holds to s ≈ 0.14 by interpolation.

**By V_flat (S; Υ; ΔV at Υ 0.50):**
| V_flat | n | lg M200 | need, ET1 [95 %] | ET2 | F canonical | N0 | N1 | N2 |
|---|---|---|---|---|---|---|---|---|
| 20–60 | 13 | 9.97 | 69 [52, 85] | 70 | 107; 0.30; +3.7 | 47; 1.20; −5.2 | **72**; 0.30; −1.0 | 100; 0.30; +2.3 |
| 60–100 | 35 | 10.59 | 103 [81, 124] | 108 | 107; 0.48; +2.9 | 69; 1.10; −6.1 | **91**; 0.59; +0.5 | 115; 0.33; +5.5 |
| 100–150 | 23 | 11.13 | 143 [118, 200] | 158 | 107; 0.73; −6.4 | 94; 0.84; −10.5 | 112; 0.71; −5.5 | **128**; 0.56; −1.6 |
| 150–200 | 25 | 11.76 | 150 [98, 190] | | 136; 0.54; −3.8 | same | 141; 0.53; −2.4 | 145; 0.52; −1.3 |
| 200–250 | 18 | 12.11 | 215 [137, 272] | | 156; 0.60; −16.2 | same | same | same |
| 250–400 | 10 | 12.27 | 412 [182, 596] | | 161; 0.76; −56.7 | same | same | same |

S at lg M200 8/9/10/11: N0 13.8 / 26.0 / 48.1 / 87.4; N1 32.0 / 48.6 / 72.6 / 106.4; N2 62.5 / 80.1 / 100.8 / 124.6.

**Checked hard, post-result, because N0's Υ of 1.1–1.2 at low mass is a warning:**

| Sample | F canonical | N0 | N1 | N2 | law can. | law alt |
|---|---|---|---|---|---|---|
| rms free Υ, all 175 | 0.0687 | 0.0678 | **0.0670** | 0.0695 | 0.0541 | 0.0537 |
| rms Υ = 0.50, all 175 | 0.1261 | 0.1294 | 0.1247 | 0.1237 | 0.1124 | 0.1029 |
| rms free Υ, V 20–60 | 0.187 | 0.119 | 0.129 | 0.179 | 0.122 | 0.138 |
| rms free Υ, V 60–100 | 0.156 | 0.139 | 0.147 | 0.165 | 0.107 | 0.122 |
| rms free Υ, V 100–150 | 0.056 | 0.066 | 0.059 | 0.058 | 0.059 | 0.056 |
| offset at Υ 0.50, gas ≥ 0.5 (81) | −0.039 | +0.036 | −0.017 | −0.056 | +0.014 | −0.023 |
| offset at Υ 0.50, gas ≥ 0.7 (41) | **−0.110** | +0.016 | −0.060 | −0.114 | −0.038 | −0.075 |

Alt with floor: offset −0.146 on gas ≥ 0.7. So the floor over-predicts the galaxies where Υ can't compensate.

**LITTLE THINGS, independent of SPARC (RT1's single-point recipe, 20 galaxies), median E (negative = over-predicted), rms:** law −0.025, 0.345; F canonical −0.041, 0.353; F alt −0.055, 0.354; N0 +0.158, 0.408; N1 +0.078, 0.365; N2 −0.026, 0.354. N0 falls short here. Together with the SPARC line, a rough window is s ≈ 0.09–0.14.

| Local Group, E (Z) | law | F canonical | N0 | N1 | N2 |
|---|---|---|---|---|---|
| IC 1613 | −0.59 (−7.9) | −0.64 (−8.6) | −0.45 (−6.0) | −0.55 (−7.4) | −0.62 (−8.2) |
| WLM | +0.08 (+1.0) | +0.04 (+0.5) | +0.21 (+2.9) | +0.12 (+1.6) | +0.06 (+0.8) |
| DDO 210 | −0.08 (−1.0) | −0.18 (−2.4) | +0.36 (+4.8) | +0.11 (+1.4) | −0.07 (−0.9) |
| DDO 216 | −0.18 (−2.4) | −0.26 (−3.4) | +0.07 (+0.9) | −0.10 (−1.3) | −0.20 (−2.7) |

**What version N costs.**
- a₀ leaves the cold sector. a₀/2πG is then just the collapse S of a roughly 10¹¹ M☉ halo (N1: 106.4 at lg M200 11). Nothing here explains the RAR's tightness or why its scale lies near cH.
- Dwarf ceilings fall. PC1's cored bound M₃D(<r) ≤ 1.599 S r² at lg M200 9 under N1 drops 0.34 dex: MW ultra-faints mean −0.275 → +0.07, Draco +0.148 → +0.49 (by hand). A cusp's bound is 2π S r², 0.59 dex higher. That's the shape question again.
- With no floor every galaxy is on the collapse branch, so CN1's contraction question applies to all of them.

**Prediction on record before X80 lands:** the SPARC line allows η_conv(10¹⁰)/η_conv(10¹²) up to about 1.9. ET1 and ET2's medians at the two lowest bins want about 1.5 over N0; their lower bounds, 1.1–1.2. N1 gives 1.53 at 10¹⁰ and 1.24 at 10¹¹.

### 4e. Lensing ladder
**Photometric isolation (B21, KiDS).**

BL1, route E at EM1's M200, FC1's rule; A = data/model in CFG829's window:
| class | A | Δ lg M200 for A = 1 | law A | χ²(15) route E / law |
|---|---|---|---|---|
| blue | 1.053 ± 0.095 | **+0.03** (−0.10, +0.14) | 0.878 | **109 / 27.5** |
| red | 1.649 ± 0.083 | +0.32 (+0.25, +0.38) | 1.313 | 562 / 137 |
| all | 1.494 ± 0.054 | +0.26 (+0.21, +0.30) | 1.207 | 693 / 79 |
| red at R2 | 1.080 ± 0.054 | | 1.023 | |
| all at R2 | 1.104 ± 0.040 | | 1.012 | 569 / 39 |

Blue data/route E rises 0.63, 0.71, 1.16, 1.53, 2.04, 1.59 across the window, and 3–6 beyond it. So BLUE CONSISTENT is amplitude only.

X53 harness at FC1: Δχ²(H − L) +434 canonical, +464 alt. GH2: route E needs gas to k* = 1.82 R_vir to beat the law (χ² law 66.2 at k = 1; route E 437.9 at k = 1, 140.6 at k = 3).

F2 Track B, law's A_O1 / A_O2 by nested isolation: S10 (181,477) 1.59 / 1.40; S30 1.46 / 0.64; S_strict (40,576) 1.31 / 0.06; S_x300 0.82 / −0.74. The outer signal falls with isolation, and the last is the isolation hole. So KiDS's outer signal is environment-exposed. **Route E has never been run on these nested samples.**

**Spectroscopic isolation (P2's GAMA G3C × KiDS-1000).** S1 and S3 are lens samples; S alone is ρ₀r₀. Δ = L − I (iso-random hole subtracted), 15 bins, 36-patch jackknife, Hartlap. S3 = R_iso 3 Mpc, N 2,251. S1 = R_iso 1 Mpc, N 10,620. Statistic Δχ² = χ²(route E) − χ²(law); D = √((m_H−m_L)ᵀC⁻¹(m_H−m_L)). Classes: D < 3 NOT POWERED; otherwise LAW, ROUTE E, or NEITHER by distance from ±D².

| Line (canonical) | χ² law (p) | χ² route E (p) | Δχ² | D | class |
|---|---|---|---|---|---|
| S3, R0 | 17.8 (0.276) | 12.6 (0.631) | −5.1 | 2.51 | NOT POWERED |
| S1, R0 | 15.8 (0.398) | 24.4 (0.058) | +8.7 | 4.26 | LAW PREFERRED |
| S3, R2 | 19.3 (0.199) | 8.7 (0.893) | −10.6 | 2.77 | NOT POWERED |
| S1, R2 | 22.7 (0.091) | 22.3 (0.099) | −0.3 | 4.63 | NEITHER |
| S1, blue R0 | 16.7 (0.335) | 20.8 (0.143) | +4.1 | 2.09 | NOT POWERED |
| S1, red R0 | 32.5 (0.006) | 48.6 (0.000) | +16.1 | 4.79 | LAW |
| S1, red R2 | 34.2 (0.003) | 32.2 (0.006) | −2.0 | 5.27 | NEITHER, both poor |
| S1, R2, raw L − R | 51.1 (0.000) | 33.7 (0.004) | −17.4 | 4.19 | ROUTE E, poor |
| alt S3, R2 | 21.3 (0.128) | 8.7 (0.893) | −12.6 | 3.16 | ROUTE E |
| alt S1, R2 | 29.0 (0.016) | 22.4 (0.097) | −6.6 | 5.26 | NEITHER |

Frozen combined reading: **LENSING TENSION GONE ON CLEAN LENSES (conditional on R2).** Would be MIXED at R0 and R1.

**Per-bin, S1, ΔΣ in M☉/pc²:**
| R, Mpc | 0.035 | 0.048 | 0.065 | 0.088 | 0.119 | 0.162 | 0.221 | 0.300 | 0.408 | 0.554 | 0.754 | 1.024 | 1.392 | 1.893 | 2.573 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| data | 25.4 | 13.6 | 42.0 | 27.9 | 22.1 | 22.5 | 11.7 | 5.42 | 5.45 | 3.22 | 2.02 | 0.73 | −0.29 | 0.57 | 0.25 |
| σ | 27.7 | 18.2 | 10.7 | 8.81 | 6.04 | 5.32 | 3.31 | 2.14 | 1.84 | 1.26 | 1.09 | 0.90 | 0.60 | 0.45 | 0.37 |
| law R0 | 46.7 | 33.5 | 24.3 | 18.7 | 15.2 | 11.1 | 8.22 | 6.12 | 4.58 | 3.43 | 2.55 | 1.80 | 1.34 | 1.18 | 1.21 |
| route E R0 | 55.8 | 40.5 | 28.0 | 18.8 | 12.4 | 7.79 | 4.86 | 2.99 | 1.84 | 1.12 | 0.67 | 0.34 | 0.17 | 0.10 | 0.08 |
| law R2 | 64.3 | 45.5 | 32.5 | 24.2 | 18.8 | 13.7 | 10.1 | 7.48 | 5.59 | 4.17 | 3.10 | 2.19 | 1.63 | 1.42 | 1.43 |
| route E R2 | 74.5 | 55.5 | 39.5 | 27.1 | 18.0 | 11.5 | 7.27 | 4.52 | 2.79 | 1.70 | 1.03 | 0.56 | 0.29 | 0.17 | 0.12 |

**Per-bin, S3:**
| R, Mpc | 0.035 | 0.048 | 0.065 | 0.088 | 0.119 | 0.162 | 0.221 | 0.300 | 0.408 | 0.554 | 0.754 | 1.024 | 1.392 | 1.893 | 2.573 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| data | 73.4 | 28.2 | 57.4 | 65.9 | 32.4 | 33.6 | 14.6 | 3.94 | 8.01 | 0.35 | 1.95 | 0.40 | 0.44 | −0.77 | 0.14 |
| σ | 46.8 | 45.3 | 24.7 | 18.9 | 13.9 | 10.4 | 7.91 | 6.61 | 4.45 | 2.88 | 2.32 | 1.94 | 1.18 | 0.76 | 0.87 |
| law R2 | 75.3 | 52.2 | 37.5 | 28.1 | 21.8 | 15.9 | 11.6 | 8.66 | 6.51 | 4.86 | 3.67 | 2.77 | 2.11 | 1.64 | 1.24 |
| route E R2 | 86.6 | 64.0 | 46.4 | 32.3 | 21.8 | 14.0 | 8.79 | 5.49 | 3.42 | 2.08 | 1.27 | 0.76 | 0.43 | 0.24 | 0.13 |

**Amplitudes, A = data/model:**
| | S1 R0 route E | S1 R2 route E | S1 R0 law | S1 R2 law | S3 R2 route E | S3 R2 law |
|---|---|---|---|---|---|---|
| A_in (≤ 0.31 Mpc) | 1.39 ± 0.19 | **0.99 ± 0.14** | 1.29 ± 0.15 | **1.00 ± 0.12** | 1.37 ± 0.23 | 1.41 ± 0.23 |
| A_O1 (0.4–1.1 Mpc) | 2.89 ± 0.60 | **1.89 ± 0.39** | 0.88 ± 0.19 | **0.72 ± 0.16** | 1.29 ± 0.77 | 0.47 ± 0.31 |
| A_O2 (1.1–3 Mpc) | | 0.96 ± 1.58 | 0.20 ± 0.23 | **0.16 ± 0.19** | −0.63 ± 2.10 | −0.13 ± 0.35 |

So on S1 at R2: inside 0.31 Mpc both models fit. At 0.4–1.1 Mpc the data lie between them: route E 2.3σ short, law 1.8σ over. Beyond 1.1 Mpc the law is 4.4σ over, and route E is not constrained at this level.

**Common M200 shift, R0 (SI1):** S3 +0.43 [+0.30, +0.57], χ² 7.0 from 12.6. S1 +0.22 [+0.15, +0.32], χ² 18.6 from 24.4. GH1, G09 centrals at 50–300 kpc: +0.17 [+0.05, +0.28], χ²(20) 24.8 best, 26.5 at 0, law 28.3.

**Sensitivity to the red shift, S1, canonical:** +0: Δχ² +8.7, LAW; +0.123: +4.9, LAW, p(H) 0.111; +0.2: +2.5, LAW; +0.295: −0.3, NEITHER; +0.4: −3.1, NEITHER, p(H) 0.029. χ²(H) is lowest around +0.2 (21.3). A_in = 1 at about +0.3 for both models.

**Does the halo have to follow the stars?** Stars +0.295 in both, route E's M200 argument moved only by h. h 0.123: S3 −8.8, D 3.07, ROUTE E, p(H) 0.784; S1 +0.6, D 5.15, NEITHER, p(H) 0.077, A_O1 2.39 ± 0.49. h 0: S3 −7.4, D 3.27, ROUTE E; S1 +2.7, D 5.59, NEITHER, p(H) 0.045, A_O1 2.78 ± 0.57. So the reading survives at h 0.123 and just misses at h 0. The IMF rung dragging the halo isn't what holds it up.

**AS1, your slope test, 150–800 kpc (six bins, GLS):**
| Sample | γ | σ_γ | A(300 kpc) | S/N | class |
|---|---|---|---|---|---|
| B21, lg M★ 8.5–10.3 | 0.583 | 0.266 | 2.88 | 9.2 | NOT POWERED |
| B21, 10.3–10.6 | **0.955** | 0.120 | 7.39 | 15.4 | FAVOURS LAW |
| B21, 10.6–10.8 | **0.860** | 0.117 | 8.26 | 16.4 | FAVOURS LAW |
| B21, 10.8–11.0 | **1.014** | 0.092 | 10.75 | 20.5 | FAVOURS LAW |
| S3, L − I | 2.016 | 0.855 | 8.01 | 3.6 | NOT POWERED |
| S1, L − I | 1.398 | 0.331 | 7.55 | 7.5 | NOT POWERED |
| S3, raw L − R | 1.769 | 0.563 | 8.78 | 4.8 | NOT POWERED |
| S1, raw L − R | 1.570 | 0.268 | 7.73 | 7.8 | NOT POWERED |

Models on S1, same estimator: law R0 0.953, R2 0.961; route E R0 1.588, R2 1.568. Data pulls on S1: from law R2 +1.32σ (raw +2.20σ); from route E R2 −0.51σ (raw −0.04σ). Amplitude at 300 kpc on S1: data 7.55; law R2 7.51; route E R2 4.48. So S1 has route E's slope at about the law's amplitude. S1 minus B21's top bin: +0.38 ± 0.34, raw +0.56 ± 0.28. N needed for σ_γ 0.225 at this completeness: about 23,000 (L − I), 15,000 (raw).

Frozen verdict is NOT DECIDED, on my error: my MUTATE kept the covariance unscaled and failed. Scaled, it passes to 7e-16. K1–K3 pass.

### 4f. Gas: why kSZ no longer decides route E
GH8/GH9, ACT DR6 × 326k DESI centrals: A(1.8) 0.24 ± 0.19 (D1 masses, CIGALE about 0.19 dex below the Chen-method scale), A(1) 0.39 ± 0.27. No detection (null p 0.21). Control S/N 4.27 after fixes. Break-even +0.27 dex.

That class was "below route E's need" under the reading that lensing needs gas to 1.8 R_vir at R0. Under EM1's M200 plus the red ladder, that gas isn't called on by lensing. **But a budget question stays open.** At EM1's relation M_b/M200 is 0.079 at lg M_b 10.78, against fair 0.159. The galaxy holds about half of fair share, with 44–63 % not in the galaxy over lg M_b 9.5–11.3. At L★ that's about 6e10 M☉ to R200, more to r_ta. Zhang's M_hot(<196 kpc) about 1e11 covers it; at GH9's A(1) it would be about 4e10 ± 3e10, marginal. Clusters are held at fair share, galaxies aren't.

Peer lanes running: GH10_dr2_ksz_published_points (Hadzhiyska+26, S/N 7–9, inherits Planck; flagged) and GH10_smooth_gas_taper.

### 4g. Softening channels, now mostly unneeded if FC1 stands
| Lane | Result |
|---|---|
| BE1 | SPARC softening needs 1.7 % of E_SN if coupled |
| CM1 | measured gas R 0.932 (need was 0.817); lift 76 % of E_SN; 0.4 % of lift reaches cold fluid |
| CM2, CM3 | coupling 1, rare bursts: 10 bursts R 0.573, 20 → 0.685, 40 → 0.898. Coupling 0.3 misses (0.894, 0.956) |
| SH1 | SN-only softening fails clusters; R 0.685 everywhere passes but assumes cluster softening |
| CL4 | clusters: SN excluded (ε 6.71), infall excluded (10.5), BH sufficient if coupled (0.075) |
| CL5 | BH-capped gas cycles: NOT REACHED; control R 0.91–0.95, need 0.81–0.85 |
| BH1 | BH, gravity only: best capped R 0.986 (10¹⁴), 0.917 (10¹³): NOT REACHED; gas limited |
| BH2 | central load: REACHES LIMIT at 0.05 M200, R 0.814 / 0.620; load is 8× closed box, 4–11× in-place. CLEAN not reached at 10¹⁴. Existence untested |

### 4h. Milky Way, L★
Milky Way at F's rule: FEASIBLE (WIDE PRIORS ONLY), 8 cells at R_d 1.93–2.27 kpc; best in-prior v_c 211.4 (R_d 2.60, D 2.61); McMillan 202.9; K_z 67.9. Eilers 229.1 ± 4.6. Same for version N (above crossing).

L★ by V_flat at Υ 0.50, ΔV: c_f 4 −34.7; converged −7.8; F/N −16.2; law −12.5 (alt law −5.0). 250–400: −65.5, −51.0, −56.7, −40.0. S at those bins sits inside ET1's interval at 200–250 (156 vs [137, 272]) and outside at 250–400 (161 vs [182, 596]).

## 5. Scoreboard

| Test | Version F canonical | Version N (N1) | Law |
|---|---|---|---|
| SPARC line | PASS, edge: Υ 0.51 / 0.50, rms 0.0687 | PASS: Υ 0.55 / 0.56, rms 0.0670 | rms 0.0541, Υ 0.52 canonical; alt Υ 0.44 fails |
| Footing dependence | alt fails (Υ 0.44) | none | both fit rms; alt fails Υ |
| Clusters, 15 keys | pass at f★ 0.034; edge at 0.0615 | same | fails heavy cores (record) |
| Groups | Z +1.62 | same | not repeated here |
| Gas ≥ 0.7, offset | −0.110 | −0.060 | −0.038 |
| LITTLE THINGS median | −0.041 | +0.078 | −0.025 |
| L★ 200–250 ΔV | −16.2 | −16.2 | −12.5 |
| 250–400 ΔV | −56.7 | −56.7 | −40.0 |
| Milky Way | wide priors only | same | misses K_z by +4.7–6.6σ on same box (GD2) |
| KiDS photometric | LAW by +434 | same | γ ≈ 1 fits |
| Blue lens amplitude | consistent | same | 0.878 |
| S1 at R0 / R2 | LAW +8.7 / NEITHER −0.3 | same | |
| S3 at R0 / R2 | NOT POWERED −5.1 / −10.6 | same | |
| Beyond 1.1 Mpc, clean | consistent | same | 4.4σ over on S1 |
| G09 50–300 kpc | Δ +0.17, χ² 24.8–26.5 | same | 28.3 |
| Contraction | **breaks SPARC** | **breaks SPARC** | no halo |
| Cluster net response | room +1.5 %; hydro sign says fail | same | n/a |
| IC 1613 | fails −8.6σ | fails −7.4σ | fails −7.9σ |
| J0946 dark perturber | exceeds ceiling R 31 | worse | needs luminous solution |
| Baryon budget | half of fair share missing at L★ | same | n/a |

## 6. Mechanism closure table

| Mechanism | Status | Key number | Lane |
|---|---|---|---|
| Collapse sets S above the crossing | native, post-hoc cold share | Υ 0.51; G-IN-Mall −1.95 | FC1, CE1, X81 |
| Floor below the crossing | by hand, disputed, maybe absent | N1 Υ 0.55; gas-rich offset −0.11 with floor | ET1, ET2, NF1 |
| Floor from local physics | closed | gated AQUAL, tethers, caps | X47, X65–67, PS1/2 |
| Floor from cooling | not derived | M_f NOT DIAGNOSTIC | MF1 |
| Core shape | **not produced by collapse** | NFW cusps at a/a_NFW 0.95–1.06 | X81, EM1 |
| Galaxy contraction | **breaks SPARC; open** | Υ 0.31; ε 0.094; channel 30× short | CN1, X39 |
| SN outflows, gravity only | insufficient at measured gas | R 0.932; only coupling ≈ 1, rare bursts | CM1–3, SH1 |
| Cluster gas response | **sign open** | Blumenthal −, hydro + 10 % c | CN1b, CN1c |
| Black hole, gas cycles | not reached; no longer needed if FC1 stands | R 0.986, 0.917; load 8× | BH1, BH2, CL4, CL5 |
| Baryonic dynamical friction | untested, not needed | f_clump 2–3 % by your estimate | your Q3 |
| CGM extended gas | not detected, not needed under R2 | A(1.8) 0.24 ± 0.19 | GH2–GH9 |
| Red stellar-mass scale | conditional | +0.123 measured difference, +0.172 IMF | CFG667, CFG926, S2, SI2 |
| Galaxy halo-mass rule | fitted, not unified | 11.18, 0.90 | EM1, X76 |
| κ | fitted | ½ | |
| Alt footing | law-level fail; moot under N | a₀ ≤ 9.95e-11 for Υ ≥ 0.50 | X78, NF1 |

## 7. Open wounds, largest first

1. **Net cold response must be about 1 from L★ to clusters.** Contraction breaks galaxies by a wide margin. Clusters tolerate +1.5 %. No calculation in this record produces it.
2. **Cusp versus core.** Collapse makes cusps. The rule assigns the core of equal fit and calls that S. SPARC needs cores. Nothing supplies the core at any mass. Below about 10¹¹ this could be baryons; at 10¹⁴ it can't be SN.
3. **FC1 is post hoc, on the edge, and the biases push against it.** A4 can break it.
4. **Two halo-mass rules, half the baryons unaccounted for at L★.**
5. **What a₀ is, if the floor is absent.** The law's scatter (0.054) still beats every halo rule (0.067), and a halo model doesn't explain why.
6. **KiDS +434 is unresolved.** It might be environment. Not shown.
7. **R2 is doing work:** S1's class moves from LAW to NEITHER only near +0.295.
8. **S1's 2.3σ shortfall at 0.4–1.1 Mpc at R2.** Neighbours fainter than r 19.8 aren't in either model's neighbour term. They count for more in route E, where mass sits in halos. Not computed.
9. **Milky Way, IC 1613, J0946, Draco.**
10. **What distinguishes version N from "dust with a cored prescription"?** With the floor gone, the honest answer may be: only the core and the zero particle content, and no observation in this list tells those apart.

## 8. Compute state
- **A4:** 18 ng 64 zooms at 10¹³ and 10¹⁴. About 38 h in. t 4.5 / 7.0 Gyr at 10¹³, 5.5 / 8.15 at 10¹⁴. Auto-grades when done: CE1_A4, FC1_A4 (uncommitted), X72, X74. CN1b --A4 is manual.
- **X80:** 24 zooms at 10¹⁰ and 10¹¹, next after A4 and its regrades. **The owner moved it ahead of A5 on 10-30** (X80 AMENDMENT_A1). These are the zooms that decide the floor. The amendment freezes the reading in 4d before any low-mass number exists, and grades the no-floor rule on the measured η.
- **A5:** nine ng 80 at 10¹², 5–6 days, ε fixed. X81 says this measures the same cut. Now after X80.
- **PAPER65:** draft only, predates FC1. Nothing deposited.
- **Data on disk:** SPARC, B21's full release (mass, colour, Sérsic bins), KiDS-1000 sources, KiDS-bright LePhare, GAMA DR4 G3C, DESI DR1 centrals, ACT DR6, X-COP, eRASS1 stacks, LITTLE THINGS, SLUGGS. No SDSS or BOSS spectroscopy on disk. A fetch needs the owner's OK.

## 9. Steps I would take, ranked. Attack this list
| # | Step | Cost | Kill or pass |
|---|---|---|---|
| 1 | **X80 before A5.** Approved and set up. Reports X81's converged η beside the frozen R(M) | 24 zooms after A4 | ratio η(10¹⁰)/η(10¹²) above 1.9 breaks N's line; below about 1.1 N is short and something else, maybe a floor, is needed |
| 2 | **NR1: two-fluid non-radiative zoom** on X48's seeds, 10¹²–10¹⁴: measure S_cold directly. This tests f_c and the sign at once | needs a hydro code; not in repo | R_c ≥ 1.05 at both cluster masses kills FC1's clusters, native |
| 3 | **SI3: nested photometric isolation with a hole term**, route E and law, R0 and R2, χ² and slope | hours; small job; data on disk | LAW at D ≥ 5 with route E p < 0.01 at strict isolation and R2 means KiDS's preference isn't environmental |
| 4 | **GD1: growing-disc potential in a live zoom** at 10¹², gravity only | hours to days per seed at ng 48 | replaces Blumenthal with a number. Net S above about 1.2 needs a real expansion channel |
| 5 | **AM1: native abundance match.** M200(M_b) from our own P(k) and a measured baryonic mass function, no fit, against EM1 and the +0.2–0.3 dex | under a day | a relation that can't pass SPARC's line means EM1 isn't describing the halos it names |
| 6 | **R2 tests:** IMF rung only on Sérsic-selected early types; dynamical bound on M★ from σ | small | S1 returns to LAW |
| 7 | **Unseen neighbours** in S1's 0.4–1.1 Mpc shortfall | small | does the shortfall close |

## 10. Questions, in priority order

**Q1. Net response.** What sets net S_final/S_initial for a w ≈ 0 gravitating fluid when baryons settle, at 10¹², 10¹³, 10¹⁴? Give sign and size with an energy budget. Does Rasia/Lin's +10 % apply to this fluid? Is there any route to about 1 across 2 dex in mass without tuning? If hydro's sign holds in clusters, what's left?

**Q2. Design NR1.** Smallest two-fluid run that can measure R_c to ±3 % on same-seed pairs at N ≈ 25k–100k. Which code, what gas physics, which diagnostics. What's your prediction, before any run? Is f_c itself right when gas shocks and no longer traces the cold fluid?

**Q3. Attack version N.** What existing data kills N1 but not the floor? Give one test with numbers. Consider the RAR's tightness and scale, HSB/LSB at fixed V_flat, dSph central densities, BTFR slope. Predict η_conv at 10¹⁰ and 10¹¹ before X80 lands; your smooth-max formula is already frozen in X80's criteria at R 1.07 and 1.16 (ε-cut fit, no f_c). If N stands, what is left of a₀ = κc√(Gρ_Λ) and κ = ½? Is 2πG S(10¹¹–10¹²) ≈ cH a coincidence with a derivation?

**Q4. Cusp versus core.** On the collapse branch, what physical scale turns a cusp into a core while conserving the ρr product? If none, can route E work with cusps at some masses and cores at others, and on what variable? Don't re-propose anything in section 11.

**Q5. One halo-mass rule.** Can M200(M_b) at galaxy scale and fair share at cluster scale be one statement? Predict AM1's answer. Where do the missing 44–63 % of fair-share baryons go, with a number and a test?

**Q6. Lensing.** Freeze SI3's classes. Give expected signal for each model at S10, S30, S_strict with the hole term. Would SDSS main-sample lenses × KiDS or DES reach N ≈ 15–23k with a complete veto? How large is the unseen-neighbour term at 0.4–1.1 Mpc?

**Q7. R2.** Cleanest independent test of +0.295 on these lenses using data on disk.

**Q8. Drop conditions.** State what result on steps 1–5 makes you drop route E, each version separately. What would you compare it with instead?

## 11. Closed: do not re-propose without something new
| Idea | Why closed |
|---|---|
| Full adiabatic contraction for MW or galaxies | X39, CN1 |
| r⁻⁹ᐟ⁴ tail for lensing | TL1, GC3, GX1 |
| Reshaping at fixed mass | X68: zero-sum |
| Correlated matter beyond r_ta | under 1 M☉/pc² at 2 Mpc; wrong sign outside R |
| Gated AQUAL, tethers, phase-space and pressure floors, phantom tracking | X65–67, X47, PS1/2 |
| Soft floor, split Burkert, cored NFW | X69, X70_soft_floor_x0 |
| Cluster gas cycles at the BH cap | CL5 |
| SN or infall for cluster cores | CL4 |
| Potential, σ, acceleration keys for a switch | J1, X19 |
| "κ derived" from 32π, DSF-21, SIS ratio | restatements |
| c_f from (Δ_vir/Δ_ta)^(1/3) × 2 | gives 8.3 |
| Bulge split for L★ | ET1 |
| Per-galaxy c_f scatter on SPARC | X76_cf_scatter_sparc: P_line 0.001 |
| Softening as the fix for clusters' η | FC1 dissolves it unless R_c > 1 |

## 12. Format for your reply
For each question:
1. The answer in plain words, or "no new idea".
2. Every input, with its source: measured, native, or assumed.
3. The derivation, with a numerical check of any closed form.
4. Frozen pass and fail conditions before any result, both footings where they differ.
5. What it breaks elsewhere: SPARC, clusters, MW, KiDS, dwarfs.

At most three new lanes, ranked. Scripts are welcome if they read inputs rather than hard-code targets. Every number you give gets recomputed here.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
