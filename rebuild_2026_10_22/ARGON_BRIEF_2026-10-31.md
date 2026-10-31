# Instructions for Argon: you write the plan

The report below is the full state of route E. Your job is to work out the shortest honest path from where it stands to one rule that clears every gate in section 0a, or to show that no such path exists. You are writing the plan. Section 9 is my own list, for comparison only: write yours first, then say where you differ and why.

Read sections 0, 0a and N1–N8 first, then work through these in order.

1. **The blocker.** In under ten lines, say what you think is really stopping a full pass, and why.
2. **Audit.** Walk the chain from zoom to grader and list every bookkeeping error I've missed, in either direction, with its sign and size in S or Z. Three turned up in one day (the mass argument, redshift, a template defect), so assume there are more.
3. **Predict.** Before ZN1's snapshots exist, give numbers for everything listed in Q2. They get recorded on receipt and scored when ZN1 lands.
4. **The plan.** At most five lanes, in order. For each one, give:
   - what it computes, in one sentence;
   - every input, marked measured, native or assumed;
   - its pass and fail conditions, fixed before any result;
   - its cost on the machine in section 8 (16 cores, 64 GB, direct-summation zooms, no hydro code, no new data without the owner's OK);
   - which gates in 0a it can close, and what a pass would break elsewhere;
   - what happens next on a pass, and on a fail.
5. **Triage.** For each gate G1–G14 and each item in 0b, say which it is: reachable by bookkeeping and native computation, needs new physics, fatal, or deferrable with a stated caveat.
6. **Closure.** For each mechanism in section 6, say what would close it: a derivation, a measurement, or an honest "open".
7. **Stop conditions.** State the results that would make you drop route E, each version separately, and what you'd compare it with instead.
8. **The rest.** Answer the other questions in section 10 only where you have something new.

**Rules**
- No tuned parameter, scanned multiplier or chosen slope. No number back-solved from its target.
- Nothing from the closed list in section 11 unless you say what's new.
- No ΛCDM inputs. Published simulations can be cited for sign and size, not used as inputs.
- κ = ½ is fitted. Call the fluid cold dark energy, never dark matter. Never say "proves", "final theory" or that the data favour the framework.
- Check every closed form numerically. Scripts must read their inputs, not hard-code targets.
- Every number you give gets recomputed here, and criteria get frozen before any run, so wrong numbers cost you the argument.
- "No new idea" and "no such path exists" are acceptable answers. A plan that only looks good is not.

**Format.** Plain text with as little inline LaTeX as you can manage: a long reply of yours arrived scrambled once. If it runs long, split it into numbered parts and say how many there are.

---

# Full report for Argon: route E, what stands, and the path to a full pass (2026-10-31)

This replaces ARGON_BRIEF_2026-10-30_EVENING and stands alone. Every number comes from a lane output on the record. Lane names are given so you can ask for any file. Footing is canonical unless I say alt. Z < 0 means the model is above the data (OVER).

The owner wants a win and final closure. Your instructions are at the top. Nothing here is theory closed, and I can't accept a pass that comes from moving a line.

## 0. The short version

1. **The theory under test.** Plain Newtonian gravity. Each halo is cold dark energy, a gravitating w ≈ 0 field component with no particle. Its core strength S = ρ₀r₀ comes from native collapse zooms on the record's own P(k) and background. The a₀ law g = ν(g_N/a₀) g_N is emergent, not fundamental. κ = ½ is fitted.
2. **Two real gains on 10-31, and each clears what the other fails.**
   - **MA1 (bookkeeping):** S(M) is defined for collapsed mass. SPARC, groups and the zooms use it. Clusters had been passing the mass out to turnaround. With the same M₂₀₀ everywhere: all 15 shear keys, SPARC and groups pass at both f★, worst key −1.45 and −1.55 (they were −1.95 and −2.004). X-COP still fails.
   - **NZ1 (core radius):** taking r₀ from the zooms as well as S, X-COP's hydrostatic masses pass at both f★ (rms 0.087, 0.085; limit 0.10). It is the first zero-parameter rule to do that, and SPARC's line holds. The shear past about 1 Mpc goes under, and groups fail (Z +3.98).
3. **A defect in my own grader, found today.** Four outer keys have been compared on two different templates ever since f★ and the gas tail changed. On one template the budget rules land nearly on the data in those keys (MA1: G-OUT-Mall +0.35, G-OUT-M3 +0.83, from −1.36, −0.99). NZ1 gets worse (G-OUT-M3 +6.14). No frozen pass or fail on FC1 or MA1 changes. N5 has it.
4. **The closest thing to one rule.** X-COP's gate uses X-COP's gas and the shear keys have used eRASS1's, which runs 0.111 dex lower for the same clusters (SM1). With one gas scale and one template, NZ1 passes X-COP and **13 of 15 shear keys** at both f★. Only G-OUT-M3 (+4.18, +3.87) and G-OUT-Mall (+2.61, +2.88) miss at f★ 0.034. With S at z_obs too: 12 of 15. That isn't a pass, and groups fail if the zoom r₀ goes on every path. MA1 on the same gas scale falls to 8 of 15, OVER.
5. **Why neither is a win.**
   - **Redshift takes MA1 back.** Every lane has treated clusters as if seen at z = 0. With S at each cluster's own z_obs (median 0.22), S rises × 1.26 and G-IN-Mall fails at −2.33. That leaves 14 of 15 at f★ 0.034, and 13 at 0.0615.
   - **The current rule fails X-COP on its own** (XH1: mean −0.073, rms 0.139), too heavy from 0.2 to 0.7 R500, which agrees with the shear's MID band. So that part of the over-prediction is real. The all-cluster OUTER band is not over, once the defect is fixed.
6. **The diagnosis.** The zooms stop at z_f with M/2 collapsed, and every rule guesses where the other half goes: a single r⁻³ tail to a budget, a frozen core with a solved tail, an r⁻⁹ᐟ⁴ tail. Each passes X-COP or the shear, never both. **No zoom on the record has been run past z_f.**
7. **What's running.** ZN1 (frozen 22d690ccf2, amended b5df0a0a1c before any number, owner's go): six zooms continued to z = 0, one native profile, no fitted parameter, graded on both data sets at each cluster's own z_obs. X80 (24 zooms at 10¹⁰ and 10¹¹) decides whether a floor is needed. A4 (ng 64 at 10¹³ and 10¹⁴) is finishing today.
8. **Standing since 10-30.** The floor may not be needed on SPARC (NF1), which would take a₀ out of the cold sector: the owner's call. Contraction breaks SPARC (CN1, Υ 0.31). Photometric lensing favours the law by Δχ² +434. On clean spectroscopic lenses it's level, conditional on a red stellar-mass rung (SI2). The Milky Way passes on wide priors only. L★ is −16 km/s (law −12.5). IC 1613 and J0946 fail. Collapse makes cusps while the rule assigns cores.

## 0a. What a win means

One rule, with no fitted parameter beyond what it declares, has to clear all of these at once. Today the best rule changes from gate to gate.

| Gate | Pass line | FC1 (rule of 10-30) | MA1 | NZ1 | a₀ law |
|---|---|---|---|---|---|
| **G1 SPARC line** | rms ≤ 0.110, median Υ 0.50–0.80, both backgrounds | pass, Υ 0.51 / 0.50, rms 0.0687 | same | pass on all paths, Υ 0.52 / 0.52, rms 0.0691 | rms 0.0541, Υ 0.52; alt Υ 0.44 fails |
| **G2 Groups** | \|Z\| ≤ 2, 63 groups | +1.62 | +1.62 | **+3.98 FAIL** on all paths; +1.62 if only clusters change | not repeated |
| **G3 Shear, S at z = 0** | 15 keys, \|Z\| ≤ 2, both h, both f★, one template | f★ 0.034 only, worst −1.95; −2.004 at 0.0615 | **PASS, worst −1.45, −1.55** | **FAIL:** 10, 11 of 15; G-OUT-M3 +6.14, G-OUT-Mall +4.07, G-MID-T3 +2.40 | fails heavy cores (record) |
| **G3z same, S at own z_obs** | same | not run, worse than MA1 | **FAIL:** 14, 13 of 15; G-IN-Mall −2.33, −2.40 | **FAIL:** 11 of 15; G-OUT-M3 +5.76 | n/a |
| **G3g same, one gas scale for both data sets** | same, eRASS1's gas + 0.111 dex (SM1) | not run | **FAIL:** 8, 6 of 15; G-MID-T3 −3.26 | **closest: 13 of 15;** G-OUT-M3 +4.18, G-OUT-Mall +2.61 | n/a |
| **G3gz one gas scale, S at own z_obs** | same | not run | **FAIL:** 6, 4 of 15; G-MID-T3 −4.38 | **12 of 15;** G-OUT-M3 +3.69, G-OUT-Mall +2.30, G-IN-Mall −2.04 | n/a |
| **G4 X-COP** | 35 points, \|mean Δ\| ≤ 0.05, rms ≤ 0.10 | **FAIL** −0.073, 0.139 | **FAIL** −0.014, 0.136 | **PASS** +0.047, 0.087 | n/a |
| **G5 Milky Way** | Eilers v_c 229.1 ± 4.6, K_z, Ou+24, measured priors | wide priors only | same path | not run | misses K_z by +4.7–6.6σ (GD2) |
| **G6 High V_flat** | ΔV at Υ 0.50 near 0 | −16.2 at 200–250, −56.7 at 250–400 | same | −17.1, −53.1 | −12.5, −40.0 |
| **G7 KiDS photometric lensing** | competitive with the law | LAW by Δχ² +434 | same | not run | γ ≈ 1 fits |
| **G8 Clean spectroscopic lenses** | S1, S3 | level, conditional on R2 | same | not run | S1 beyond 1.1 Mpc 4.4σ over |
| **G9 Dwarfs** | LITTLE THINGS, Local Group | median −0.041; IC 1613 −8.6σ | same | not run | median −0.025; IC 1613 −7.9σ |
| **G10 J0946** | dark perturber under the ceiling | exceeds, R 31 | same | not run | needs a luminous solution |
| **G11 Core** | a physical origin | chosen by hand; zooms make cusps | same | same | no halo |
| **G12 Net cold response** | about 1 from L★ to clusters, derived | no calculation produces it | same | same | no halo |
| **G13 One halo-mass rule** | one statement at all masses | galaxies fitted, clusters fair share | same | same | no halo |
| **G14 κ and a₀** | derived, or removed | κ fitted | same | same | κ fitted |

G1–G4 are where ZN1 and X80 can move things this week. G11–G14 need physics, not bookkeeping.

## 0b. What closure needs beyond this table

- **Covariant parent.** v3s, the covariant attempt, has a final verdict (10-24): as a galaxy-scale law it passes; as a theory of gravity and cosmology it fails on clusters, growth and CMB, the radiation era, hosted dwarfs and the MW disc, mostly through one mechanism (α ≡ 1, one field). That investigation is closed and v3s is frozen. Route E has no covariant parent of its own on the record. In route E the Solar System is plain Newtonian, so Cassini isn't a constraint there.
- **Abundance of the cold fluid.** X1_seedfree_abundance reads UNDETERMINED by its frozen rule. Every light-spectator point computed fails the CMB isocurvature bound by 2e8–6e8 in power. In the kinetic description the X condensate is absorbed by the bath as soon as it oscillates (Γ/H 22.6), giving Ω_c h² ≈ 1.4e-8; 0.12 is reached only if it never interacts. Lattice runs are in the compute queue. The route E grades here take Ω_c/Ω_b from the native background; they don't derive it.
- **What a₀ is.** Under route E, a₀ = κc√(Gρ_Λ) is a coincidence (EM1). The law's scatter (0.054) still beats every halo rule (0.067), and no halo rule explains the RAR's tightness.
- **Telling route E from dust with a cored prescription.** With the floor gone, the honest answer may be: only the core and the zero particle content. No observation on this list separates them.
- **Dated data, already pre-registered:** ALMA windows 11-06 and 11-28, Gaia DR4 12-02.

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

**Paste problem.** Your long reply before last reached me scrambled from the end of Q2 through Q4: the words were alphabetically sorted. I could not read that part. If it mattered, resend it, ideally with less inline LaTeX. Your last reply came through clean.

## 2. Your last two replies, checked

**Your long reply, Q1–Q6:**

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

**Your reply on moving X80 ahead of A5.** The owner did that. You did not answer Q1–Q8 of the last brief, and they carry over in section 10.

| Your claim | Check | Result |
|---|---|---|
| c_f ∝ 1 + z_f gives η ratios 1.126 at 10¹¹, 1.254 at 10¹⁰ | recomputed: 1.1256, 1.2541 (1.2514 at X80's smoke z_f 1.326) | right; recorded in X80's README before any low-mass number, HIT within ±15 % |
| Those ratios are in the SPARC window | through NF1's grader, a what-if: Υ 0.62 / 0.63, rms 0.0669, the lowest so far; ρ₁₀ 1.9 fails at Υ 0.49; ρ₁₀ 1.1 passes at 0.67 / 0.68 | right |
| The frozen converged reads close the X81 loophole "completely" | η_conv still assumes the NFW continues inside the resolved radius. ε/2 only moves x_c 0.0321 → 0.0296, +3.4 % in η, and A5 can't test it | too strong |
| Below 1.1 falls short "unless Σ_a0 is put in by hand" | the line passes down to a ratio of 1, and the floor over-predicts gas-rich dwarfs. Below 1.1 only falls short of ET1's and ET2's intervals | wrong |
| S products at 10¹⁰ and 10¹² | you left out f_c: cold S is 59 not 70 at 10¹⁰, 149 not 177 at 10¹². 59 is inside ET1's [52, 85] | corrected |
| Disk pre-flight, clear old scratch | about 5 MB per run, under 300 MB for A4 + X80 + A5, 23 GB free | not needed |

## 3. The theory under test, exactly

### 3a. Rule
Gravity is plain Newtonian. The a₀ law g = ν(g_N/a₀) g_N is emergent, not fundamental. Each halo is cold dark energy with

ρ(r) = ρ₀ (1 + x²)^(−3/2), x = r/r₀; M(<r) = π S r₀² B(x); B(x) = 4[asinh x − x/√(1+x²)]; S ≡ ρ₀r₀.

Two versions now compete:

- **Version F (floor):** S_cold(M) = max(Σ_a0, f_c η(M_t) Σ_coll(M_t)), M_t = M/f_c.
- **Version N (no floor):** S_cold(M) = f_c η(M_t) Σ_coll(M_t) at every mass. N0: η flat below 10¹². N1: η × 10^(0.0927 (12 − lg M_t)) below 10¹². N2: slope 0.1668.

r₀ is solved from M(<R200) = M200 for galaxies and groups, and M(<r_ta) = M_fair for clusters. (The last brief listed groups with clusters. That was wrong: the code has groups on M200.) The halo continues to r_ta.

**Cluster variants as of 10-31:** FC1 passes M_t = M_fair + M_b,t, the whole mass to r_ta, to S. MA1 passes the model's own M₂₀₀. NZ1 also takes r₀ = r_f/a from the zooms and fills a solved tail beyond r_f. ZN1 drops S and r₀ altogether and uses the native z = 0 profile. In every graded rule so far, S assumes z_obs = 0.

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
| Cluster M_fair | baryons × (1 + R_nat) inside self-consistent r_ta | GC2, X43 |
| a = r_f/r₀ from η = (4/3) a²/B(a), 10¹² / 10¹³ / 10¹⁴ | 13.34 / 10.40 / 10.11 | NZ1, from CE1's η |
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
| Two halo-mass rules | galaxies and groups EM1, clusters fair share. Not unified |
| S's mass argument | clusters had mass to r_ta until MA1; M₂₀₀ on all paths since |
| z_obs in S | absent from every graded rule; N3 shows it matters |
| r₀ | budget-solved in FC1 and MA1; from the zooms in NZ1 |
| f★, gas slope | measured, but the slope is extrapolated past the data to r_ta |
| R2 | from the record, conditional. Lens tests only |
| Υ | free per galaxy on a grid 0.30–1.20; line tests the median |

### 3d. Grader (X74)
- **SPARC line:** rms ≤ 0.110 and median Υ in [0.50, 0.80] on backgrounds A and B.
- **Clusters:** 15 keys, |Z| ≤ 2, in h 0.672 and 0.686 cells. IN (bins near 0.15–0.46 Mpc), MID (by kT tercile and slope), OUT (1.42–3 Mpc, by kT and M_gas tercile). The values below are in the grader's own units.
- **Groups:** |Z| ≤ 2 on 63 groups.
- **X-COP:** HO1's line, 35 points at 0.1–0.7 R500, |mean Δ| ≤ 0.05, rms ≤ 0.10, M_FORW, 7 clusters with stars. Not part of X74's grader.
- Separate: MW (Eilers v_c 229.1 ± 4.6, K_z, Ou+24), KiDS bins 3–4, lens tests.
- **Apertures (SM1):** in R500, INNER 0.23–0.49, MID 0.71–1.50, OUTER 2.18–3.17, median R500 0.78 Mpc, median M500 1.8e14. X-COP's median M500 is 5.7e14, the lensing sample's 95th percentile.
- **INNER's error** is s_IN = √(s_STAT² + A_x² + A_RR²), dominated by the cross shear: at OS1, A 2.28, s_STAT 0.29, A_x −1.01, s_IN 1.05 (IC1 D2). MID and OUTER have X7's calibrated errors.

**Weakness in my own grader:** the 15 keys have no joint statistic. They share clusters and are correlated, and at FC1, 10 of 13 amplitude keys sit on the OVER side once N5's template defect is fixed (13 of 13 as the grader read it; table in 4a). "All pass" is not a joint fit.

## New on 10-31 (sections N1–N8)

### N1. XH1: the rule of 10-30 on X-COP (criteria 530debe21b)
X-COP's hydrostatic masses had never been graded on this rule. HO1's pass line was inherited unchanged. Δ = log₁₀[M_HSE/(M_b + M_h)], so Δ > 0 means the model is too light. M_FORW; 35 points; 7 clusters; baryons are X-COP's measured gas and stars.

| Rule | mean | rms | x = r/R500: 0.1 | 0.2 | 0.3 | 0.5 | 0.7 | verdict |
|---|---|---|---|---|---|---|---|---|
| FC1, f★ 0.034 | −0.073 | 0.139 | +0.115 | −0.064 | −0.119 | −0.142 | −0.157 | FAIL |
| FC1, f★ 0.0615 | −0.077 | 0.143 | +0.115 | −0.066 | −0.123 | −0.148 | −0.165 | FAIL |
| HO1's older picture (Burkert) | −0.002 | 0.126 | +0.193 | +0.029 | −0.034 | −0.082 | −0.117 | FAIL |

- The excess at 0.3–0.7 R500 (× 1.3–1.44) agrees with the shear's MID band (G-MID-T1, T2, T3: × 1.51, 1.18, 1.20). Two independent data sets say the rule is too heavy there. In OUTER, the 106 kT clusters run × 1.29, but all 326 are on the data once N5's defect is fixed (G-OUT-Mall × 0.98).
- G-IN-Mall (0.15–0.46 Mpc) has the model × 1.90 over. X-COP in the same band has it × 1.23. Frozen band label: SHEAR BAND OUTLIER. That band's error budget is dominated by its cross shear (A 2.28, s_STAT 0.29, A_x −1.01, s_IN 1.05; IC1 D2). This shows a conflict between data sets, not which is biased: X-COP is 7 massive clusters in 3D mass; eRASS1 is 326 lighter ones in projected shear.
- A hydrostatic bias can't carry the miss: XRISM's non-thermal pressure is a few percent in cores (0.013 dex for 3 %), Eckert+19's X-COP median is about 6 % at R500 (0.027 dex), and the miss is 0.12–0.16 dex.

### N2. MA1: the same collapsed mass on every path (criteria b22583d196)
**The point.** X43's Σ_coll(M) uses Lacey–Cole with M as the final collapsed mass, and X48's zooms put M/2 at z_f. SPARC and groups pass M200. Since GS1 extended the budget to r_ta, clusters have passed M_fair + M_b,t, everything out to turnaround. FC1's criteria only checked that it was total mass. Here M₂₀₀ is the model's own total mass inside R₂₀₀, as a fixed point at 200 ρ_c(z = 0). M₂₀₀/M_ta = 0.503 [0.472, 0.545]. S falls × 0.857 [0.842, 1.000]. No parameter. Post hoc, disclosed: I found it looking for help.

| Run | f★ | Υ (A/B) | groups Z | worst key | G-IN-Mall (h 0.672/0.686) | G-MID-T3 | result |
|---|---|---|---|---|---|---|---|
| **MA1 frozen** | 0.034 | 0.51 / 0.50 | +1.62 | G-IN-Mall −1.45 | −1.45 / −1.23 | −1.15 / −0.61 | **PASS** |
| **MA1 frozen** | 0.0615 | 0.51 / 0.50 | +1.62 | G-OUT-all −1.55 | −1.50 / −1.26 | −1.35 / −0.80 | **PASS** |
| p16 | 0.034 | 0.52 / 0.52 | +1.67 | G-OUT-all −1.32 | −1.22 / −1.03 | −0.88 / −0.36 | PASS |
| p16 | 0.0615 | 0.52 / 0.52 | +1.67 | G-OUT-all −1.48 | −1.26 / −1.07 | −1.07 / −0.54 | PASS |
| p84 | 0.034 | 0.49 / 0.49 | +1.55 | G-IN-Mall −1.72 | −1.72 / −1.45 | −1.45 / −0.89 | FAIL on SPARC's line only |
| p84 | 0.0615 | 0.49 / 0.49 | +1.55 | G-IN-Mall −1.77 | −1.77 / −1.50 | −1.66 / −1.09 | FAIL on SPARC's line only |
| η(10¹³, 10¹⁴) × 1.1144, A4's guide | 0.034 | 0.50 / 0.50 | +1.55 | G-IN-Mall −1.80 | −1.80 / −1.52 | −1.54 / −0.97 | PASS |
| same | 0.0615 | 0.50 / 0.50 | +1.55 | G-IN-Mall −1.85 | −1.85 / −1.56 | −1.75 / −1.18 | PASS |
| η × 1.206, its 68 % upper end | 0.034 | 0.50 / 0.50 | +1.50 | G-IN-Mall −2.07 | −2.07 / −1.75 | −1.82 / −1.23 | FAIL |
| same | 0.0615 | 0.50 / 0.50 | +1.50 | G-IN-Mall −2.13 | −2.13 / −1.80 | −2.04 / −1.45 | FAIL |
| M at 18π² ρ_m(0), not 200 ρ_c | 0.034 | 0.51 / 0.50 | +1.62 | G-IN-Mall −1.65 | −1.65 / −1.39 | −1.38 / −0.83 | PASS |
| same | 0.0615 | 0.51 / 0.50 | +1.62 | G-IN-Mall −1.70 | −1.70 / −1.44 | −1.59 / −1.02 | PASS |

Every key moved toward the data except the two slopes. All 15, h 0.672, f★ 0.034, MA1 (FC1): G-IN-all −1.17 (−1.49); G-IN-Mall −1.45 (−1.95); G-MID-T1 −1.33 (−1.48); G-MID-T2 −0.71 (−0.96); G-MID-T3 −1.15 (−1.71); G-MID-b +0.44 (+0.15); G-OUT-all −1.38 (−1.50); G-OUT-T1 −0.81 (−0.84); G-OUT-T2 −0.87 (−0.93); G-OUT-T3 −0.66 (−0.78); G-OUT-b +0.49 (+0.42); G-OUT-Mall −1.36 (−1.55); G-OUT-M1 −0.28 (−0.30); G-OUT-M2 −1.27 (−1.37); G-OUT-M3 −0.99 (−1.31). The last four are as the grader read them. On one template they are +0.35, +0.10, −0.15, +0.83 (N5).

X-COP on MA1: mean −0.014, rms 0.136, FAIL; by x +0.205, +0.013, −0.057, −0.102, −0.128. Disputed band model/data × 1.05. Model M₂₀₀ runs × 1.4–1.6 over X-COP's hydrostatic M₂₀₀ in five of seven clusters. Alt fails SPARC's line (Υ 0.44), X78's known failure.

### N3. The redshift stress test that takes MA1 back (post-result; MA1's frozen label stands as frozen)
MA1, like FC1 and every lane before, treats each cluster as seen at z = 0. Here D_f = δ_c/(δ_c/D(z_obs) + ω√ΔS), with R₂₀₀ at 200 ρ_c(z_obs). SPARC and groups stay at z = 0. z_obs median 0.223 [0.108, 0.393], max 0.499. S(z_obs)/S(0) at fixed M: median 1.26, p84 1.51, max 1.75.

| Run | f★ | result | worst keys |
|---|---|---|---|
| z_obs | 0.034 | **FAIL** | G-IN-Mall −2.33 / −2.00, G-MID-T3 −1.96, G-IN-all −1.68 |
| z_obs | 0.0615 | **FAIL** | G-IN-Mall −2.40 / −2.05, G-MID-T3 −2.19, G-OUT-Mall −1.79 |
| z_obs, η × 1.1144 | 0.034 | FAIL | G-IN-Mall −2.76 / −2.36, G-MID-T3 −2.35 |
| z_obs, η × 1.1144 | 0.0615 | FAIL | G-IN-Mall −2.83 / −2.43, G-MID-T3 −2.59 |

On one template (N5) that's 14 of 15 at f★ 0.034, G-IN-Mall only, and 13 of 15 at 0.0615. η may itself depend on z_obs through peak height. That isn't measured here. **I found two bookkeeping errors looking for help (f_c, the mass argument) and this one attacking a pass. Others may remain, in either direction.**

### N4. NZ1: r₀ from the zooms too (criteria 7b6807445e)
The smooth-core fit has M(<r_f) = M/2 at r_f, so η = (4/3) a²/B(a) with a = r_f/r₀ fixes a from η alone: a = 13.34, 10.40, 10.11 at 10¹², 10¹³, 10¹⁴. r_f² = 3(M/2)/(4π Σ_coll). The budget-solved r₀ runs about × 1.6 larger on clusters (X-COP: zoom 181–251 kpc, budget 284–400 kpc). Beyond r_f the fair share to r_ta fills a tail whose slope γ is solved per cluster. M is MA1's M₂₀₀, a hybrid: the frozen profile can't itself hold M inside R₂₀₀ at z = 0. Galaxies and groups on the collapse branch use r₀ = r_f/a at M200/f_c; the floor keeps its budget r₀.

Frozen verdict: **X-COP PASSES, KEYS BREAK.**

| Run, f★ | X-COP mean | rms | x 0.1 | 0.2 | 0.3 | 0.5 | 0.7 | keys over 2 | groups Z | Υ |
|---|---|---|---|---|---|---|---|---|---|---|
| ALL, 0.034 | +0.047 | **0.087** | +0.100 | +0.006 | +0.012 | +0.052 | +0.064 | G-MID-T2, G-MID-T3, G-OUT-Mall, G-OUT-M3 | +3.98 | 0.52 / 0.52 |
| ALL, 0.0615 | +0.042 | **0.085** | +0.100 | +0.002 | +0.007 | +0.044 | +0.056 | G-MID-T3, G-OUT-Mall, G-OUT-M3 | +3.98 | 0.52 / 0.52 |
| η × 1.1144, 0.034 | +0.017 | 0.076 | +0.047 | −0.032 | −0.015 | +0.034 | +0.051 | G-MID-T3, G-OUT-Mall, G-OUT-M3 | +3.93 | 0.52 / 0.52 |
| r₀ × 1.5, its MUTATE, 0.034 | −0.010 | 0.125 | +0.191 | +0.008 | −0.054 | −0.087 | −0.108 | none; SPARC's line fails | +1.31 | 0.49 / 0.50 |

All 15 at f★ 0.034, h 0.672 / 0.686: G-IN-all −0.71 / −0.73; G-IN-Mall −0.80 / −0.69; G-MID-T1 +0.39 / +0.61; G-MID-T2 +1.64 / +2.03; G-MID-T3 +2.40 / +2.77; G-MID-b +1.22 / +1.39; G-OUT-all +1.28 / +1.25; G-OUT-T1 −0.02 / −0.07; G-OUT-T2 +0.58 / +0.73; G-OUT-T3 +1.63 / +1.44; G-OUT-b +1.29 / +1.08; G-OUT-Mall +3.06 / +3.32; G-OUT-M1 +0.36 / +0.53; G-OUT-M2 +1.51 / +1.61; G-OUT-M3 +5.10 / +4.71. Those are as frozen. On one template G-OUT-Mall is +4.07, G-OUT-M2 +2.18, G-OUT-M3 +6.14 at h 0.672 (N5).

Solved γ: median 1.87 [1.73, 2.00]. X-COP per cluster, mean Δ: A1795 +0.068, A2029 +0.079, A2142 −0.005, A2319 +0.025, A644 +0.148, A85 +0.002, ZW1215 +0.010. SPARC by V_flat, ΔV at Υ 0.50 (FC1): +3.7 (+3.7), +2.9 (+2.9), −10.2 (−6.4), −2.3 (−3.8), −17.1 (−16.2), −53.1 (−56.7). So L★ isn't fixed. A higher η helps X-COP here, where on single-tail rules it hurts.

### N5. A defect in my grader, and one gas scale (post-result, reported; frozen labels stand as frozen)
**The defect.** Four keys (G-OUT-Mall, G-OUT-M1–M3) read X7's fixed A_CAL and s_CAL, computed on the C\* template at f★ 0.20 with no gas tail. Their predictions, and the other 11 keys' measured values, divide by the current template. At f★ 0.20 with no tail the two agree to 2e-16 in every cell. f★ and the tail each move the template. So every lane since either one changed (X71, GS1, X73, X74, CE1, FC1, MA1, NZ1) has compared these four on two templates. This is my grader's error. I found it because a what-if failed only on those keys. The fix: A from the run's `M_all|OUTER` and `M_terc|OUTER`, s_CAL scaled by the same ratio (`NZ1_zoom_core_radius/nz1_one_template.out`).

| f★, gas tail | M_all | M1 | M2 | M3 |
|---|---|---|---|---|
| 0.20, none (X7's values) | 0.929 | 0.488 | 0.762 | 1.369 |
| 0.20, to r_ta | 1.017 | 0.560 | 0.841 | 1.445 |
| 0.034, none | 1.007 | 0.529 | 0.826 | 1.488 |
| 0.034, to r_ta | 1.102 | 0.607 | 0.910 | 1.570 |
| 0.0615, to r_ta | 1.087 | 0.599 | 0.897 | 1.547 |

**What it changes** (h 0.672; on one template, then as the grader read it):

| Rule, f★ | G-OUT-Mall | G-OUT-M1 | G-OUT-M2 | G-OUT-M3 | keys passing, one template (as read) |
|---|---|---|---|---|---|
| FC1, 0.034 | +0.18 (−1.55) | +0.09 (−0.30) | −0.23 (−1.37) | +0.54 (−1.31) | 15 (15) |
| FC1, 0.0615 | −0.06 (−1.68) | +0.04 (−0.32) | −0.39 (−1.45) | +0.22 (−1.47) | 14 (14) |
| MA1, 0.034 | +0.35 (−1.36) | +0.10 (−0.28) | −0.15 (−1.27) | +0.83 (−0.99) | 15 (15) |
| MA1, 0.0615 | +0.11 (−1.48) | +0.06 (−0.30) | −0.31 (−1.36) | +0.52 (−1.13) | 15 (15) |
| NZ1, 0.034 | +4.07 (+3.06) | +0.61 (+0.36) | +2.18 (+1.51) | +6.14 (+5.10) | 10 (11) |
| NZ1, 0.0615 | +3.94 (+3.00) | +0.59 (+0.35) | +2.10 (+1.47) | +5.96 (+5.02) | 11 (12) |

No pass or fail label on FC1 or MA1 changes: G-IN-Mall decides those. But the read changes. On the budget rules all 326 clusters' OUTER band is on the data (G-OUT-Mall pred/meas 0.98 on FC1), not over it. G-OUT-all's × 1.29 is the 106 kT clusters only. At FC1, 10 of 13 amplitude keys sit OVER, not 13 of 13. NZ1 gets worse, and G-OUT-M2 joins its misses. Earlier reads that turned on these keys need rechecking, and I haven't done that yet: X71's "break", X73's FRAGILE, GX2.

**One gas scale.** SM1 matched five clusters in both catalogues: eRASS1's Mgas500 runs below X-COP's by 0.055, 0.116, 0.064, 0.111, 0.111 dex (median 0.111, about 23 %, std 0.026). None of the five is in the lensing sample, and all are massive, so applying it across the lensing sample is an extrapolation. X-COP's gate has always used X-COP's gas, and the shear keys have used eRASS1's: two gas scales for one rule. Here is every rule on both, all on one template. M is MA1's M₂₀₀. SPARC and groups stay as FC1 in these runs (Υ 0.51 / 0.50, Z +1.62). X-COP's own redshifts are 0.05–0.09, and its line is read at z = 0.

| Rule | shear's gas scale | S at z_obs | keys passing, f★ 0.034 / 0.0615 | over 2 at f★ 0.034, Z at h 0.672 / 0.686 | X-COP mean, rms |
|---|---|---|---|---|---|
| FC1 | eRASS1's | no | 15 / 14 | none | −0.073, 0.139 FAIL |
| MA1 | eRASS1's | no | 15 / 15 | none | −0.014, 0.136 FAIL |
| MA1 | eRASS1's | yes | 14 / 13 | G-IN-Mall −2.33 / −2.00 | −0.014, 0.136 FAIL |
| MA1 | X-COP's | no | 8 / 6 | G-MID-T3 −3.26 / −2.63; G-OUT-all −3.19 / −3.14; G-OUT-M3 −2.53 / −2.49; G-MID-T1 −2.40 / −2.04; 3 more | −0.014, 0.136 FAIL |
| MA1 | X-COP's | yes | 6 / 4 | G-MID-T3 −4.38 / −3.67; G-OUT-all −3.44 / −3.37; G-OUT-M3 −3.23 / −3.14; G-IN-Mall −3.01 / −2.57; 5 more | −0.014, 0.136 FAIL |
| NZ1 | eRASS1's | no | 10 / 11 | G-OUT-M3 +6.14 / +5.73; G-OUT-Mall +4.07 / +4.38; G-MID-T3 +2.40 / +2.77; G-OUT-M2 +2.18 / +2.24; 1 more | +0.047, 0.087 **PASS** |
| NZ1 | eRASS1's | yes | 11 / 11 | G-OUT-M3 +5.76 / +5.37; G-OUT-Mall +3.83 / +4.13; G-MID-T3 +1.99 / +2.39; G-OUT-M2 +2.05 / +2.12 | +0.047, 0.087 **PASS** |
| **NZ1** | **X-COP's** | **no** | 13 / 13 | G-OUT-M3 +4.18 / +3.87; G-OUT-Mall +2.61 / +2.88 | +0.047, 0.087 **PASS** |
| **NZ1** | **X-COP's** | **yes** | 12 / 12 | G-OUT-M3 +3.69 / +3.41; G-OUT-Mall +2.30 / +2.56; G-IN-Mall −2.04 / −1.77 | +0.047, 0.087 **PASS** |

**NZ1 on X-COP's gas scale, f★ 0.034, h 0.672 / 0.686, all 15:** G-IN-all −1.04 / −1.08; G-MID-T1 −0.29 / −0.04; G-MID-T2 +0.70 / +1.13; G-MID-T3 +0.91 / +1.35; G-MID-b +0.83 / +1.01; G-OUT-all +0.24 / +0.23; G-OUT-T1 −0.36 / −0.39; G-OUT-T2 +0.01 / +0.16; G-OUT-T3 +0.77 / +0.63; G-OUT-b +1.04 / +0.83; G-OUT-Mall +2.61 / +2.88; G-OUT-M1 +0.35 / +0.52; G-OUT-M2 +1.26 / +1.39; G-OUT-M3 +4.18 / +3.87; G-IN-Mall −1.30 / −1.12. G-OUT-M3: measured 1.362 ± 0.103, predicted 0.931, pred/meas 0.68. G-OUT-Mall: 0.959 ± 0.101, 0.696, 0.73.

**How this reads.** There are two self-consistent pairs. MA1 with eRASS1's gas fits the shear and not X-COP. NZ1 with X-COP's gas fits X-COP and 13 of 15 shear keys. The second uses one gas scale throughout and is the closest thing to a single rule on the record. It isn't a pass. What's left is the OUTER band, 2.18–3.17 R500, mostly in the most gas-rich tercile: beyond R₂₀₀, the region that holds the mass arriving after z_f. NZ1's tail spreads that mass out to r_ta, and ZN1 measures where it actually goes. If zoom r₀ goes on every path, groups fail at Z +3.98. GX2 raised the gas on older halos with the same template mismatch in these four keys, so its OUT-Mall and OUT-M reads need rechecking too.

### N6. What these lanes say together
1. **X-COP and the shear aren't graded at the same radii.** SM1: X-COP is at 0.1–0.7 R500. The lensing bands in R500 are INNER 0.23–0.49, MID 0.71–1.50, OUTER 2.18–3.17, on clusters 3× lighter (median R500 0.78 Mpc against 1.23 Mpc). And they've been on different gas scales. So there's no proven contradiction between the two data sets.
2. **The bracket.** r₀ × 1 gives γ 1.87: X-COP passes, the outer keys go under. r₀ × 1.5 gives γ 2.90: keys pass, X-COP fails. The real profile lies between. Picking a multiplier would be a knob. GX1 showed the same trade for the r⁻⁹ᐟ⁴ family (splashback edge passes X-COP, lensing OVER; r_ta edge fails both).
3. **What's physically missing.** R₂₀₀ ≈ 1.12 r_f at z = 0. So the M/2 arriving after z_f has to land inside a radius only 12 % beyond r_f, unless the inner profile changes too. A frozen z_f core can't do that, and a single tail can't hold it. Only a calculation past z_f can say where it goes. On one gas scale, the only keys still missing are in the band where that mass should sit.

### N7. ZN1: the zooms to z = 0 (frozen 22d690ccf2, running)
- **Runs:** seeds 1–3 at 10¹³ and 10¹⁴, ng 64, N 57,777, continued from X48's `snap_zf.npz` with X48's own direct-summation engine, softening (ε fixed at 0.01 r_f), step rule and background. Snapshots at z = 0.5, 0.25, 0. Isolated Lagrangian sphere of 1.5 q_M, about 1.69 M in all. About 740–1,090 more steps per run, 2–3 days. K1: from X48's last checkpoint, the continuation reproduces X48's own final snapshot exactly, max |d| 0 in positions and velocities (M1e14 s3).
- **Measure:** M(<r) in spheres, R₂₀₀ at 200 ρ_c(z), shape m(x) = M(<x R₂₀₀)/M₂₀₀, resolved for r ≥ 3ε, trusted to x_edge where M reaches 90 % of the run's mass. Median over seeds, tagged with the measured M₂₀₀.
- **Rule for a cluster, at its own z_obs, no fitted parameter:** M₂₀₀ from fair share inside R₂₀₀: (1 + R_nat) M_b(<R₂₀₀) = 200 ρ_c(z_obs) (4π/3) R₂₀₀³. Shape from the snapshot nearest z_obs, interpolated in log M₂₀₀, clamped outside. M_c(r) = f_c M₂₀₀ m(r/R₂₀₀). Beyond x_edge, a tail to M_fair at r_ta, slope solved. S, η, r₀ and a₀ don't enter. SPARC and groups stay as FC1.
- **Graded:** X-COP's line and the 15 shear keys at both f★, all on one template and on X-COP's gas scale (AMENDMENT A1, b5df0a0a1c, committed before any snapshot is analysed). Classes: Z0 PROFILE PASSES BOTH, F★-DEPENDENT, X-COP ONLY, KEYS ONLY, FAILS BOTH, with [NOISE-LIMITED] if seeds disagree, [MASS-DEFINITION-DEPENDENT] if MA1's budget M₂₀₀ changes the class, and [GAS-SCALE-DEPENDENT] if eRASS1's own gas does.
- **Reported:** where the late mass lands (M(<r, 0)/M(<r, z_f) at r/r_f 0.1, 0.2, 0.5, 1, 1.5), whether S and r₀ freeze, c_nfw against z, M₂₀₀(0) against nominal M, the native slope past R₂₀₀.
- **My expectation, on record before any new snapshot:** X-COP probably passes, and G-OUT-M3 is the key most at risk, because fair share inside R₂₀₀ gives less mass than MA1's budget.
- **Weak points I know of:** three seeds; 10¹⁴ shape clamped for the massive clusters; vacuum outside the sphere; SM1's gas offset comes from five massive clusters.

### N8. Other lanes that landed after the last brief
- **ET3–ET6 (low-mass S, free fits on real curves):** S rises about × 2 from V_flat 20–60 to 100–150 km/s (70.2, 107.7, 157.5, ρ +0.556). It survives beam, pressure support, inclination, distance, quality cuts (ET3; WORST ρ +0.415, p 0.0099), a Υ trend (ET4; erased only at s 1, with 36 galaxies clipped), their joint grid (ET5) and four core shapes (ET6; ρ +0.518 to +0.563, × 2.2–2.6). Systematics reach at most about × 1.4 from a flat truth. The flat floor is **not rejected:** its grade stays MIXED at the base. Canonical's floor is not reconciled in 18 cells (ET5) and is definition-dependent across shapes (ET6); alt's floor is contained at a generous corner with the rise remaining. The collapse branch rises by about the right factor: N0 47, 69, 94 (× 2.0). Not tested: real per-galaxy beams, 3D modelling, non-circular motions.
- **GH10_dr2_ksz_published_points:** published DESI DR2 × ACT DR6 kSZ at CIGALE log M★ 10.5–11: A(1.8) 0.448 ± 0.105, BELOW NEED, a 4.3σ detection of the same gas. Measured M_gas(<1.8 R_vir) about 2.1e11 M☉ against a need of 4.7e11 (limit 3.2e11, post hoc). The misfit is in the shape, so extended gas isn't retired.
- **GH10_smooth_gas_taper:** FORM-DEPENDENT. A(1.8) + 2e is 0.61 sharp, 0.76 F2, 1.31 F1 at the same total mass.
- **GH11_ksz_two_halo_miscentring:** A(1.8) 0.54 ± 0.13 at realistic miscentring (f_s 0.24, σ_off 300 kpc), still BELOW. Removed only at the extreme. My two-halo template doesn't work, so that question stays open.
- **FC1's forecast for A4:** with η at 10¹³ and 10¹⁴ × g, FC1's pass has room to g 1.016 only. At 10¹², ng 48 → 64 moved converged η × 1.114 (23.27 → 25.94; 68 % 0.84–1.21; each grid redraws the field). So I expect FC1's own label to fail on clusters. MA1 absorbs that at z = 0.

## 4. Results of 10-30

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

**All 15 keys, f★ 0.034, h 0.672 (measured ± s, prediction, Z). G-OUT-Mall and G-OUT-M1–M3 are shown as the grader read them; N5 has the correction:**
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

**Room on the high side: about +1.5 % in S on FC1.** On MA1 it's about × 1.17 at z = 0 (N2), and none once z_obs enters (N3). SPARC's line has about the same room at 10¹² (p84, +2.3 %, gives Υ 0.49); moving η at 10¹³ and 10¹⁴ alone leaves it at 0.50 or above up to × 1.114 (`fc1_a4_expect.out`).

### 4d. NF1: no floor (criteria f95621e30a)
ET1 and ET2 measured the S SPARC asks for below 150 km/s: 69, 103, 143 with M200, and 70, 108, 158 free (rise ρ +0.60, +0.556). A flat floor reads MIXED. The collapse branch runs parallel to that rise. ET3–ET6 are in N8.

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

GH10 and GH11's results are in N8.

### 4g. Softening channels, not needed unless S has to fall
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

## 5. Scoreboard, rest of the record

The cluster and SPARC gates by rule are in section 0a. Version F against N against the law, on everything else:

| Test | Version F canonical | Version N (N1) | Law |
|---|---|---|---|
| SPARC line | PASS, edge: Υ 0.51 / 0.50, rms 0.0687 | PASS: Υ 0.55 / 0.56, rms 0.0670 | rms 0.0541, Υ 0.52 canonical; alt Υ 0.44 fails |
| Footing dependence | alt fails (Υ 0.44) | none | both fit rms; alt fails Υ |
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
| Cluster net response | room +1.5 % on FC1, about × 1.17 on MA1 at z = 0, none at z_obs; hydro's sign is c +10 % | same | n/a |
| IC 1613 | fails −8.6σ | fails −7.4σ | fails −7.9σ |
| J0946 dark perturber | exceeds ceiling R 31 | worse | needs luminous solution |
| Baryon budget | half of fair share missing at L★ | same | n/a |

## 6. Mechanism closure table

| Mechanism | Status | Key number | Lane |
|---|---|---|---|
| Collapse sets S above the crossing | native, post-hoc cold share | Υ 0.51; G-IN-Mall −1.95 | FC1, CE1, X81 |
| S's mass argument | same M₂₀₀ on all paths; bookkeeping, post hoc, no parameter | worst key −1.45 from −1.95 | MA1 |
| Redshift in S | **omitted until now; raises S × 1.26** | G-IN-Mall −2.33 | MA1 stress test |
| Core radius | budget × 1.6 above the zooms' own | X-COP rms 0.087 with the zooms' | NZ1 |
| Gas scale | eRASS1 0.111 dex below X-COP for the same clusters; one scale needed | NZ1 13 of 15, MA1 8 of 15 on X-COP's | SM1, N5 |
| Template for four outer keys | **grader defect, fixed from here on** | G-OUT-M3 on MA1 +0.83, was −0.99 | N5 |
| Mass arriving after z_f | **never measured; ZN1 running** | R₂₀₀ ≈ 1.12 r_f | ZN1 |
| Floor below the crossing | by hand, disputed, maybe absent | N1 Υ 0.55; gas-rich offset −0.11 with floor | ET1–ET6, NF1, X80 |
| Floor from local physics | closed | gated AQUAL, tethers, caps | X47, X65–67, PS1/2 |
| Floor from cooling | not derived | M_f NOT DIAGNOSTIC | MF1 |
| Core shape | **not produced by collapse** | NFW cusps at a/a_NFW 0.95–1.06 | X81, EM1 |
| Galaxy contraction | **breaks SPARC; open** | Υ 0.31; ε 0.094; channel 30× short | CN1, X39 |
| SN outflows, gravity only | insufficient at measured gas | R 0.932; only coupling ≈ 1, rare bursts | CM1–3, SH1 |
| Cluster gas response | **sign open** | Blumenthal −, hydro + 10 % c | CN1b, CN1c |
| Black hole, gas cycles | not reached; not needed unless S has to fall | R 0.986, 0.917; load 8× | BH1, BH2, CL4, CL5 |
| Baryonic dynamical friction | untested, not needed | f_clump 2–3 % by your estimate | your Q3 |
| CGM extended gas | seen, below route E's need at R0; not called on under R2 | DR2 A(1.8) 0.45 ± 0.11; DR1 0.24 ± 0.19 | GH2–GH11 |
| Red stellar-mass scale | conditional | +0.123 measured difference, +0.172 IMF | CFG667, CFG926, S2, SI2 |
| Galaxy halo-mass rule | fitted, not unified | 11.18, 0.90 | EM1, X76 |
| κ | fitted | ½ | |
| Alt footing | law-level fail; moot under N | a₀ ≤ 9.95e-11 for Υ ≥ 0.50 | X78, NF1 |

## 7. Open wounds, largest first

1. **No single cluster profile passes X-COP and the shear.** The closest, NZ1 on one gas scale, misses G-OUT-M3 and G-OUT-Mall, and G-IN-Mall too at z_obs. ZN1 is the test.
2. **Net cold response must be about 1 from L★ to clusters.** Contraction breaks galaxies by a wide margin. Clusters tolerate +1.5 % on FC1 and about +17 % on MA1 at z = 0, and nothing at z_obs. No calculation in this record produces it.
3. **Cusp versus core.** Collapse makes cusps. The rule assigns the core of equal fit and calls that S. SPARC needs cores. Nothing supplies the core at any mass. Below about 10¹¹ this could be baryons; at 10¹⁴ it can't be SN.
4. **Post hoc, and one-sided.** FC1 and MA1 were found while looking for help. The redshift error was found attacking a pass. The template defect sat in my own grader from X71 and GS1 on, and turned up only because a what-if failed on exactly those keys. The chain from zoom to grader has never had a systematic audit in both directions.
5. **No joint statistic.** The 15 keys share clusters and are correlated. Under MA1, 10 of 13 amplitude keys still sit on the OVER side. "All pass" isn't a joint fit, and G-IN-Mall's band fails its own null.
6. **Two halo-mass rules, half the baryons unaccounted for at L★.**
7. **What a₀ is, if the floor is absent.** The law's scatter (0.054) still beats every halo rule (0.067), and a halo model doesn't explain why.
8. **KiDS +434 is unresolved.** It might be environment. Not shown.
9. **R2 is doing work:** S1's class moves from LAW to NEITHER only near +0.295.
10. **S1's 2.3σ shortfall at 0.4–1.1 Mpc at R2.** Neighbours fainter than r 19.8 aren't in either model's neighbour term. They count for more in route E, where mass sits in halos. Not computed.
11. **Milky Way, IC 1613, J0946, Draco.**
12. **What distinguishes version N from "dust with a cored prescription"?** See 0b.

## 8. Compute state (10-31, 09:10)

- **A4:** 18 ng 64 zooms at 10¹³ and 10¹⁴. 14 done, the last due early afternoon. Auto-grades when done: X72, X74, X77, CE1_A4, FC1_A4. Then I rerun XH1, MA1 and NZ1 on the new cluster masses (`--A4`).
- **ZN1:** six zooms to z = 0, launched 09:08. Five running, the sixth waits on A4's M1e13 s2. About 2–3 days. Its grader is specified in the criteria and isn't built yet. K2, K3 and the MUTATE run before any grade.
- **X80:** 24 zooms at 10¹⁰ and 10¹¹, starts within minutes of A4's regrades. About 3 days alongside ZN1. Frozen reading: η(10¹⁰)/η(10¹²) above 1.9 breaks N's line; 1.1–1.9 is in the window; below 1.1 falls short of ET1's and ET2's intervals, though the line still passes down to a ratio of 1. Your prediction is on record: 1.126 at 10¹¹, 1.251–1.254 at 10¹⁰.
- **A5:** nine ng 80 at 10¹², 5–6 days, after X80. X81 says it measures the same ε cut.
- **PAPER65:** draft only, predates FC1. Nothing deposited.
- **Data on disk:** SPARC, B21's full release (mass, colour, Sérsic bins), KiDS-1000 sources, KiDS-bright LePhare, GAMA DR4 G3C, DESI DR1 centrals, ACT DR6, X-COP, eRASS1 stacks, LITTLE THINGS, SLUGGS. No SDSS or BOSS spectroscopy on disk. A fetch needs the owner's OK.

## 9. My own list, for comparison only. Write your plan first

| # | Step | Status, cost | Gates it can move | What decides it |
|---|---|---|---|---|
| 1 | **ZN1:** zooms to z = 0, one native profile | running, 2–3 days | G3, G3z, G4 | Frozen classes in N7. FAILS BOTH means collapse alone doesn't make the cluster profile, and baryons have to |
| 2 | **A4 reruns** of XH1, MA1, NZ1 | today, small | G3, G4 | Whether MA1's room survives ng 64. FC1's own label is expected to fail |
| 3 | **X80** | about 3 days | G1, G9, G14 | The window above. Decides F against N and the owner's call on a₀ |
| 4 | **Bookkeeping audit**, both directions, re-reading X71, GS1, X73 and GX2 on one template, then a redshift-aware rule frozen before ZN1 lands | you and me, small jobs | G3z, G3g, wound 4 | Each item gets sign and size, no knob |
| 5 | **Joint statistic for the 15 keys** from the shear jackknife | small job, data on disk | wound 5 | Whether "worst key" has been a fair read |
| 6 | **NR1:** two-fluid non-radiative zoom on X48's seeds | needs a hydro code, not in repo | G12, f_c | R_c ≥ 1.05 at both cluster masses is the sign hydro reports |
| 7 | **GD1:** growing-disc potential in a live zoom at 10¹², gravity only | hours to days per seed at ng 48 | G12, G1 | Replaces Blumenthal with a number. Net S above about 1.2 needs a real expansion channel |
| 8 | **AM1:** native abundance match, M200(M_b) from our own P(k) and a measured baryonic mass function | under a day | G13 | A relation that can't pass SPARC's line means EM1 isn't describing the halos it names |
| 9 | **SI3:** nested photometric isolation with a hole term, route E and law, R0 and R2 | hours, data on disk | G7 | LAW at D ≥ 5 with route E p < 0.01 at strict isolation and R2 means KiDS's preference isn't environmental |
| 10 | **R2 tests, unseen neighbours** | small | G8 | S1 returns to LAW, or the shortfall closes |

## 10. Questions, in priority order. If you're short on space, answer Q1–Q4 and Q9

**Q1. Bookkeeping audit, both directions.** I found f_c and the mass argument looking for help, z_obs attacking a pass, and the four-key template defect by accident. Walk the chain from zoom to grader and list every further mismatch, with sign and size in S or Z. Candidates I haven't closed: M₂₀₀c against the zooms' 18π²ρ_m virial definition; fair share inside R₂₀₀ against at r_ta; f_c when the gas shocks and stops tracing the cold fluid; reduced shear and cluster-member dilution in the INNER band; the catalogue miscentring; eRASS1's gas scale (N5); η clamped at 10¹⁴ for clusters at 10¹⁵. Don't list anything without a number.

**Q2. ZN1: attack it and predict it.** Before the snapshots exist, give numbers for M₂₀₀(z = 0)/M, c_nfw at z_f and z = 0, M(<r, 0)/M(<r, z_f) at r/r_f 0.1, 0.2, 0.5, 1, 1.5, X-COP's mean and rms, and G-OUT-M3's Z. What's wrong with the frozen rule? Is fair share inside R₂₀₀ the right M₂₀₀? Should SM1's gas offset enter the lensing side? Are three seeds, a 1.5 q_M sphere and a vacuum boundary good enough? I can amend the grader before any number, with the amendment disclosed. I can't after.

**Q3. Redshift.** Is D_f = δ_c/(δ_c/D(z_obs) + ω√ΔS) the right formation epoch for an object of mass M seen at z_obs? Is S × 1.26 at median z_obs 0.22 real? Does η depend on M or on peak height ν? If on ν, what's the size at z_obs 0.2–0.5, from X48's own table (η 25.94, 17.67, 16.91 at ν for 10¹², 10¹³, 10¹⁴)? Does a shape taken from the nearest snapshot absorb this correctly?

**Q4. X-COP against the shear.** Are they in conflict once radius, mass and gas definition are accounted for (SM1)? G-IN-Mall has A 2.28 with A_x −1.01 at OS1's template, and FC1 reads × 1.90 there where X-COP reads × 1.23: what would you do with that band, without dropping a frozen key after the fact? How would you build a joint statistic? Which independent inner-cluster data would settle it, and is any on disk? Is SM1's +0.111 dex, from five massive clusters, right across the lensing sample's mass range, or should it depend on mass? On one gas scale G-OUT-M3 at 2.18–3.17 R500 still wants about × 1.45 NZ1's prediction: how much of that is late-accreted mass inside r_ta, given that "correlated matter beyond r_ta" is closed (section 11)?

**Q5. Net response.** What sets net S_final/S_initial for a w ≈ 0 gravitating fluid when baryons settle, at 10¹², 10¹³, 10¹⁴? Give sign and size with an energy budget. Does Rasia/Lin's +10 % apply to this fluid? Is there any route to about 1 across 2 dex in mass without tuning? Design the smallest NR1: code, gas physics, diagnostics, R_c to ±3 % on same-seed pairs at N ≈ 25k–100k, and your prediction before any run.

**Q6. Attack version N, and the floor.** What existing data kills N1 but not the floor? Give one test with numbers. Consider the RAR's tightness and scale, HSB/LSB at fixed V_flat, dSph central densities, BTFR slope. ET1–ET6's × 2 rise stands against a flat floor, and the collapse branch gives × 2.0 at about two-thirds of the amplitude: what does that imply? If N stands, what is left of a₀ = κc√(Gρ_Λ) and κ = ½? Is 2πG S(10¹¹–10¹²) ≈ cH a coincidence with a derivation?

**Q7. Cusp against core.** NZ1 shows that the zooms' (S, r₀) keeps SPARC's line and passes X-COP. The zooms make cusps, and the smooth core is a fit to them. On the collapse branch, what physical scale turns a cusp into a core while conserving ρr? If none, can route E work with cusps at some masses and cores at others, and on what variable? Don't re-propose anything in section 11.

**Q8. One halo-mass rule, and lensing.** Can M200(M_b) at galaxy scale and fair share at cluster scale be one statement? Predict AM1's answer. Where do the missing 44–63 % of fair-share baryons go, with a number and a test? Freeze SI3's classes, and give the expected signal for each model at S10, S30, S_strict with the hole term. What's the cleanest independent test of R2 (+0.295) using data on disk?

**Q9. The path, and when to stop.** Put all of this in order as a path to the gates in 0a: which are reachable by bookkeeping and native computation, which need new physics, which are fatal, which can be deferred with a stated caveat. What would final closure of each mechanism in section 6 look like: a derivation, a measurement, or an honest "open"? State the results on steps 1–5 that would make you drop route E, each version separately, and what you'd compare it with instead.

## 11. Closed: do not re-propose without something new

| Idea | Why closed |
|---|---|
| Full adiabatic contraction for MW or galaxies | X39, CN1 |
| r⁻⁹ᐟ⁴ tail for lensing or clusters | TL1, GC3, GX1 |
| A tail slope or an r₀ multiplier for clusters, chosen to fit | NZ1's bracket and GX1: a knob |
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
| Hydrostatic bias as the fix for X-COP's excess | XRISM a few percent, 0.013–0.027 dex against a 0.12–0.16 dex miss |
| More ET systematics on the low-mass rise without new data | ET1–ET6 converged; needs real per-galaxy beams or 3D |
| ε/2 zooms to test converged η | x_c only 0.0321 → 0.0296, +3.4 %; needs far more particles |

## 12. Format for your reply

For each question:
1. The answer in plain words, or "no new idea".
2. Every input, with its source: measured, native, or assumed.
3. The derivation, with a numerical check of any closed form.
4. Frozen pass and fail conditions before any result, both footings where they differ.
5. What it breaks elsewhere: SPARC, clusters, MW, KiDS, dwarfs.

The plan itself follows the instructions at the top of this report. Scripts are welcome if they read inputs rather than hard-code targets. Every number you give gets recomputed here.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
