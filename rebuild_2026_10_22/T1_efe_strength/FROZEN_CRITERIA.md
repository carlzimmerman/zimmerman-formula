# T1_efe_strength — FROZEN CRITERIA (written and committed before any script or number of this lane)

**Question.** Three rebuilds (S1, F2, S2) suggest the data want a weaker external-field effect (EFE) than v3's AQUAL EFE.
Measure the EFE strength empirically with one diagnostic multiplier ε_EFE, per dataset and per footing, and ask whether
one ε fits every dataset. This is a diagnostic of the data, not a new theory.

Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`. κ = ½ FITTED. Footings
canonical a₀ = 9.3603e-11, alt 1.1312e-10 m/s², never pooled. No dark-matter particle (cold energy = BS K(Q) dust).
Never "theory closed"; never "the data favour the framework". No downloads. Every run `OMP_NUM_THREADS=1 nice -n 15`,
one thread, < 1 GB RSS per process. CFG960 not touched. Ledger: `ASSUMPTION_LEDGER.md`.

**Seen before freezing (disclosed; this lane is not blind).** S1's README/JSON (satellites Δ +1.331/+1.299 at ε = 1,
+0.914/+0.892 isolated native screening at the floor; Coma ⟨E⟩, z_sys at ε = 1, at "field/2" = ε 0.5 (z_sys 3.60/3.38)
and isolated (1.65/1.45)); F2's README/JSON including its post-hoc x_e scan (Track A χ²_all 161/157/156/202/302 at
x_e 0.001–0.0175 canonical, 428 at noclu) and Track B / S_x300 amplitudes; S2's A at y_e 0 / noclu / maxclu; D10's
README and its central χ² curve (L★_95 21.68 / 22.85; Δχ² AQUAL 19.3); C6's Q₂ table; D2/E2 γ_v; CFG8/CFG179 Chae
amplitudes; the n = 16 and WALLABY directional Â. F2's x_e constraint is therefore essentially known in advance; the new
content is the common-ε test, the satellites' and globulars' ε curves, and the tracking statistic.

## 0. Definition

ε_EFE multiplies the magnitude of the total host field that enters v3's static solve: x_e → ε·x_e, direction unchanged.
ε = 1 reproduces each lane's v3 result; ε = 0 is the isolated solve (isolated boundary condition). The kernel
μ = x/(1+x), L★, baryons, estimators and data are unchanged. Range ε ∈ [0, 1.5]. Between grid nodes every curve is
interpolated linearly in ε (Δ, sd, ⟨E⟩, z_sys, χ²); F2's curve is computed in x_e and mapped.

## 1. Datasets (each lane's own solver and inputs, read-only)

**SAT — dwarf satellites (S1 tile 26).** E3's 45 / 46 systems, clean primary data (Arroyo free-f, Υ_V 2), E-W estimator,
host field E_mid. Reuse: S1's script executed read-only up to its "SATELLITES: per-system native tables" marker (its data
build, seeds, MC draws and bootstrap indices; D10's solver), so the MC and bootstrap are S1's exactly. Per system and ε:
the 3 × 3 table in (log y ± 0.6 dex, log Λ ± 0.3 dex) at L★ = floor, as S1. ε grid {0, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75,
1.0, 1.5}.
- Statistic (as S1): Δ(ε) = bootstrap median over systems of log₁₀(g_obs/g_pred), sd(ε) its bootstrap sd;
  χ²_SAT(ε) = (Δ/sd)², ν = 1.
- Reported: E-V; worst-clean data W; L★ 90 pc (central-value shift, as S1's bracket rows); host bracket E_lo/E_hi as an
  ε-scale factor (median over systems of x_e(E_mid)/x_e(E_lo or E_hi)).
- **Tracking statistic SAT-TRK (robust to an unknown extra-mass offset).** Per system, central data (S1's per-system
  convention): r_i(ε) = log₁₀(g_obs/g_bar)_i − log₁₀(g_pred/g_bar)_i at (y₀, Λ_floor). OLS slope b(ε) of r_i on
  log₁₀ x_e,i(E_mid); sd from 4000 bootstrap resamples of systems (seed 20261024). ε_trk = the ε where b = 0; its 95 %
  band = {ε : |b|/sd ≤ 1.96}. If b does not change sign on [0, 1.5], the endpoint values are reported. Reported per
  footing; enters only the secondary combination C5 (§3).

**COMA — ultra-diffuse galaxies (S1 tile 29).** CFG933's 9 admitted, field at dmean (primary; dproj reported), L★ floor,
E-W. ⟨E⟩, se (CFG933 convention) and σ_sys (CFG948 recipe) recomputed at each ε; χ²_COMA = z_sys², ν = 1.
ε grid {0, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.75, 1.0, 1.25, 1.5}. Reported: per-galaxy E_i vs log x_e,i slope.

**LENS — isolated-galaxy lensing (F2 Track A).** F2's script sections 0, 1 and 4 executed read-only (B21 Fig. 3 data and
covariance, inventory, native background, `stack_model`), F2's `solve_efe` for the field. T_central (h 0.679, f_hot 0.5,
M★ and cold gas at the inventory, no profiling) with x_e = ε·x_e(noclu); χ²_LENS = χ²_all over 60 points, ν = 59.
x_e grid {0, 0.001, 0.002, 0.003, 0.0045, 0.006, 0.008, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.025, 0.03, 0.035, 0.0425,
0.05, 0.07, 0.085, 0.1, 0.125}, each solved per footing with `solve_efe` at y_e = x_e²/(1+x_e).
- Reported: x_e,95 as an absolute bound; ε relative to noclu (primary) and maxclu; χ²_in (R ≤ 0.31 Mpc, the S2-window
  cross-reference) and A_O1, A_O2 per x_e; the most generous envelope (f_hot 1, M★ +0.2, cold +0.2) x_e,95.
- Track B is not recomputed; F2's committed S_strict / S_x300 amplitudes are quoted as the isolation caveat.
- **S2 is not a separate dataset** (same lenses, same shear). Its committed A at y_e 0 / noclu / maxclu is quoted.

**GC — outer globulars (D10).** NGC 2419, Pal 4, Pal 14 (Pal 3 reported), P1 SPS prior, E_mid, f_b 0.3, E-P estimator,
D10's `lik_tables` read from its JSON. Field x_e(E_mid) → ε·x_e. ε grid {0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5}; Υ nodes =
D10's `UPSG` from 0.479 to 8.0 (10 nodes; the Υ integration range is these nodes); L★ nodes = D10's `LG` from 8.43 to
118 pc (12 nodes) + AQUAL + Newton.
- χ²_GC(ε) = −2 ln L at L★ = D10 floor (v3 reading; log-linear interpolation between L nodes), no ν (not a χ² variable;
  fit quality from D10: Δχ²_Newton ≤ 2.5).
- Reported: −2 ln L at 24, 50, 90 pc; **L★_95(ε)**, the floor recomputed at each ε with D10's 3.84 rule.
- At the floor the globulars penalise ε < 1 **by construction** (the floor was set at ε = 1). This is printed next to the
  number.

**SS — Cassini and planets (C6).** Not recomputed. Screened v3: Q₂/bound at E0–E3 read from C6's JSON; Q₂ = 0 at ε = 0
(isotropy); the bound at ε = 1.5 is extrapolated with the power law d ln Q₂/d ln x_e fitted to C6's four fields; the
planets' hedgehog GM/L★² does not depend on the field. If every Q₂/bound ≤ 1e-3 on [0, 1.5]: χ²_SS ≡ 0 (no ε
information). Unscreened (L★ = 0): fails at every ε (the μ = x/(1+x) monopole tail ~ a₀ at Saturn, CFG691's Saturn gate)
⇒ no ε information.

**WB — wide binaries.** Screened v3: γ_v − 1 = 8.1e-6 at 24 pc (C6 R3), set by L★, not by the field ⇒ χ²_WB ≡ 0.
Unscreened law-first contrast (reported only, never in a v3 combination): γ_pm(ε) = √(M_eff(<r)/M) at r = 20 kAU for
2 M☉, x_e = ε·1.778e-10/a₀, from F2's point-mass AQUAL solver; compared with CFG825's R = 0.973 ± 0.178 read as γ_v
(stated approximation). E2's binary values (1.167 / 1.199) are the ε = 1 anchor (check K7).

## 2. Per-dataset numbers (per footing)

For each curve: ε̂ = argmin on [0, 1.5]; the 95 % interval {ε : χ²(ε) − χ²_min ≤ 3.84}; Δχ²(1) and Δχ²(0); χ²_min and
p = P(χ²_ν > χ²_min) where ν is defined.
**FAILED-AT-EVERY-ε flag:** p < 0.01. A flagged curve enters the primary combination scaled, Δχ²/S² with
S² = χ²_min/ν (PDG); the unscaled curve is reported.

## 3. Combination and consistency (per footing)

Primary set **V = {SAT, COMA, LENS, GC@floor}** (SS and WB are identically flat in v3 and add nothing).
χ²_V(ε) = Σ_d Δχ²_d(ε). ε̂_V, its 95 % interval, Δχ²_V(1) = χ²_V(1) − min. Consistency (parameter goodness of fit):
χ²_PG = min_ε χ²_V(ε), dof = |V| − 1, p_PG.
Secondary combinations (each with its class, §4): C1 = V unscaled; C2 = V − GC (globulars carry no ε information once
L★ is re-floored); C3 = V − SAT (satellites fail at every ε: extra-mass reading); C4 = V − LENS (F2's UNDECIDABLE
amendment; lens fields not measured); C5 = V with SAT replaced by SAT-TRK (χ²_TRK = (b/sd)²); C6 = V + REC-Chae
(CFG179's frozen A read as ε, standard-MOND machinery, σ as recorded).

## 4. Verdict rule (per footing; lane verdict = both; a footing split is stated)

Applied to the primary set V:
- **EFE CONSISTENT WITH v3**: ε = 1 inside every dataset's 95 % interval and p_PG ≥ 0.05.
- **DATA PREFER WEAK EFE (ε̂_V, interval)**: p_PG ≥ 0.01, ε̂_V < 1 and Δχ²_V(1) ≥ 9.
- **INCONSISTENT**: p_PG < 0.01. Named: every pair of datasets whose 95 % intervals do not overlap, and the dataset whose
  removal lowers χ²_PG most.
- Otherwise **NOT DECIDED** (numbers given).
The class of each secondary combination is reported. If any secondary class differs from the primary, the verdict is
labelled **FRAGILE** and the datasets that move it are named.

## 5. What each outcome means for theory (frozen wording, applied as written)

- **ε ≈ 1 consistent everywhere:** v3's AQUAL EFE is fine; the hosted excess (satellites, UDGs) is real extra bound mass
  (cold energy) or a non-equilibrium effect, not a wrong EFE.
- **ε ≈ 0 preferred by the hosted systems and tolerated elsewhere:** the AQUAL EFE is wrong in strength. Constraints:
  E2 showed the action gives AQUAL, so a weaker EFE needs a different action. QUMOND is not the cure: E2 measured
  AQUAL vs QUMOND differences of only 1.23–1.49× in Q₂ and 0.007–0.011 in γ_v. CFG946's lemma L-G and CFG179's merge
  theorem say any local second-order field that supplies the deep law has an EFE, so ε → 0 re-opens the status board's
  no-go (tile 51, "law + a¹ growth + no EFE, local"): it needs non-local physics or a screening of the EFE itself.
- **Inconsistent:** the datasets that conflict are named; the EFE strength is not a single number in the data under v3's
  other assumptions (equilibrium, no extra mass, measured fields).

## 6. Record EFE claims (checked; class assigned)

Classes: DETECTION / CONSISTENT, NOT A DETECTION / NOT DIAGNOSTIC / CONTRADICTED BY THIS LANE / OTHER READING (unscreened
or QUMOND; no bearing on v3's ε).
- (a) Chae SPARC (CFG8, CFG179 M5): A = 0.76 ± 0.16 / 0.88 ± 0.15 (frozen zero-intercept), tracking slope 0.71 ± 0.80,
  robust variants. Compared with ε̂_V and the per-dataset intervals.
- (b) Directional EFE: n = 16 Â = +2.95 (analytic sd 3.13); WALLABY n = 25 Â = −1.70 ± 2.12 boot (2.98 analytic);
  Â ≈ k·ε with k ∈ [1, 5]. Inverse-variance combination reported.
- (c) Wide binaries: CFG447 (law with no EFE excluded by the non-scoring DR3 dry run), CFG825 R, E2/D2 γ_v.
- (d) CFG478 (QUMOND force-with-EFE vs satellite lensing).
- (e) The rebuild lanes' own EFE statements (S1, F2, S2) as quoted in this lane's brief.

## 7. Checks (`K# PASS/FAIL value threshold`; exit 0 iff all pass)

- **K1** SAT reproduces S1 at ε = 1 (Δ +1.3307 / +1.2990, sd 0.1474 / 0.1474) and ε = 0 (S1 "side: isolated native
  screening L*floor E-W" +0.9142 / +0.8918): |ΔΔ| ≤ 0.005 dex, |Δsd| ≤ 0.005.
- **K2** COMA reproduces S1 at ε = 1 (⟨E⟩ 2.5806 / 2.4812, z_sys 4.2775 / 4.1109), ε = 0.5 (field/2: 2.1736 / 2.0428,
  3.5985 / 3.3812) and ε = 0 (isolated bound: 0.7485 / 0.6579, 1.6454 / 1.4475): |Δ⟨E⟩| ≤ 2e-3, |Δz_sys| ≤ 0.01.
- **K3** LENS reproduces F2: χ²_all at noclu (427.99 / alt as committed) and at y_e = 0 (160.70 / 127.6), and the scan
  points y_e 1e-5 and 1e-4: |Δχ²| ≤ 1.0.
- **K4** GC: at ε = 1 this lane's σ tables equal D10's committed `sigma_tables` at the shared (Υ, L) nodes to ≤ 1e-5
  relative, and L★_95(ε = 1) is within 0.3 pc of 21.68 / 22.85.
- **K5** ε → 0 continuity: the embedded D10 solve at x_e = 1e-8 equals the isolated solve to ≤ 2e-3 in σ for
  (y 3e-3, Λ 0.3) and (y 0.03, Λ 0.02).
- **K6** SS: every C6 Q₂/bound ≤ 1e-3 at E0–E3 and at the ε = 1.5 extrapolation (the flatness premise of SS).
- **K7** WB contrast: γ_pm(ε = 1) within 0.06 of E2's 1.167 / 1.199 (anchors the unscreened curve).
- **K8** every production solve converged (D10 solver scaled residual < 1e-8; F2 solver last change < 1e-6).
- **K9** peak RSS < 1 GB in every process.
- **`--mutate`**: the field passed to every solver is ε·y_e (the Newtonian field) instead of ε·x_e (the total field).
  It runs only the check cells, writes `*_MUTATE.*`, and must break K1–K4.

Outputs: `t1_efe_strength.py`, `.out`, `_results.json`, per-stage `t1_stage_*.json`, `*_MUTATE.*`, README (verdict first).
Any later change is an append-only AMENDMENT, marked pre- or post-result.
