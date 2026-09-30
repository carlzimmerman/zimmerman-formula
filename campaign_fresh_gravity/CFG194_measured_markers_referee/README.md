# CFG194 — Referee re-derivation of CFG189 (the KURVS a0(z) test re-run with the MEASURED outer rotation markers, three laws, plus variant BS)

- **Criteria:** `CFG194_FROZEN_CRITERIA.md` (committed 7291bc798, sha256 d1169a50…), written before any script existed and before any marker value was read. (Numbered CFG194 on the coordinator's message; the scratch dir was called `cfg191`.) The CFG189 README numbers in it are TARGETS I read, not blind predictions; my hand estimates were made after reading that README.
- **Order of work:** phase 1 = criteria only. Phase 2 = my scripts written from the frozen text alone -> main run, MUTATE 1–6 (saved) -> attacks A/B, C/D at seeds 194 and 195 -> ONLY THEN CFG189's `.out` and `.json` and script opened (and CFG184's file layout looked at) -> `CFG194_bs_post.py` and `CFG194_diag_post.py` written after that (labelled post-comparison, not part of any frozen result). The attack scripts were finished before CFG189's outputs were opened; the frozen text was not edited.
- **Repo untouched. No network, no new data. No absolute home path in any output** (`<repo>` is printed; `run_all.sh` greps for it).
- Standing rules kept: κ = ½ is FITTED; a0(z) FLAT is the framework's distinctive law, a0 ∝ H(z) the rival, T (a0 ∝ t(z)/t0) the owner's third reading; nothing here says the data favour any law; a lean is not a detection.

## Bottom line

**Every CFG189 number REPRODUCES: all pass lines P1–P8 pass, and the per-disc inputs (R_out, V_out, its error, σ at R_out and its error) are identical to CFG189's to 0.0.** My independent marker reader gives the primary decision cell flat +0.1249 ± 0.0511 (+2.45σ), rival −0.0211 ± 0.0496 (−0.42σ), T +0.2953 ± 0.0540 (+5.47σ), class lean rival; the shifts −0.0193 / −0.0150 / −0.0274 dex (z −0.84 / −0.29 / −1.46); the headline CHANGED (T's z shift only); 1 of 5 variants (V-b) flips to lean flat; the break-evens, statuses, fit points and the C2 count (22 of 231) agree; BS agrees once CFG189's f_bs values are taken as given. Largest difference to CFG189's JSON anywhere: 1.7e-5 in Δ′, 1e-4 relative in a break-even, 0 status labels.

**What does not survive the attacks is the weight of the lean, and three CFG189 framings** (section 6). In short: (1) the lean rival is 0.45σ above its class edge and disappears for a coherent 4.5% lower V (the model-value analysis needed 11%); only 7 of 19 pre-declared marker choices keep it; (2) the V-b flip is a RADIUS effect, not two-side averaging: the farther side alone read at V-b's radius flips the same way (A5x), and the class falls monotonically as the outer radius is moved in (A6); (3) the marker choice DOES reintroduce the P0-versus-P4 pressure ambiguity: the equidistance point s_mid moves from 0.67 (model value) and 0.74 (primary) to 0.55–1.56 over the grid, above Kretschmer's s = 1 in 11 of 24 rows; (4) the ten outer markers' pulls about the digitised model curve give χ² = 2.3 for 10 dof: the markers are more consistent with the model than their errors say, so the "larger marker errors" that weaken the z are not information; under a third of flat's z drop is the marker-minus-model value, and the largest piece (about 55%) is the change of radius and σ at R_out, mostly KURVS-17. Nothing here says the data favour flat, the rival or T; a lean is not a detection.

## Answers to the four questions asked

1. **Does the V-b flip come from radius or from two-side averaging? Radius.**
   - V-b (both sides at the shorter side's radius; radii 4.96–9.41 kpc, median 7.4): flat +0.14σ, rival −3.15σ, lean flat.
   - **A5x**, the farther side ALONE read at that same radius: flat +0.37σ, rival −3.06σ, lean flat. Averaging the second side moves flat's z by 0.2 and the rival's by 0.1.
   - **A6 radius scan** (farther side at f × R_max(table)): f = 0.5, 0.6, 0.7 lean flat (flat −0.6σ, +0.1σ, +1.0σ; rival −4.3σ, −3.6σ, −2.6σ), f = 0.8 and 0.9 non-diagnostic (both within), the primary (f ≈ 1) lean rival. The nearer side alone at its own outermost radius is also lean flat (A2).
   - The two sides do differ at the shorter radius by up to 34% and 47% (KURVS-16, -21; v+/v− −1), so a centring or asymmetry offset exists, but it is not what flips the class. My estimate (P = 0.35 that A5x flips, leaning to averaging) was wrong; kept.
2. **Does flat's +2.4σ survive leave-one-out and the grid? Leave-one-out yes, the grid no.**
   - **LOO:** lean rival persists in 9 of 10 (z_flat +1.93 to +2.58; only dropping KURVS-21 gives non-diagnostic, +1.93). The frozen line (≥ 8 of 10) passes. My estimate (median 6 of 10; P(≥ 8) = 0.25) was wrong; kept.
   - **Bootstrap** of the ten discs (N = 2000, seed 194): lean rival 0.764, non-diagnostic (both within) 0.234, lean flat 0.002; P(z_flat > 2) = 0.764; z_flat 16/50/84% = 1.82 / 2.43 / 2.97.
   - **Named subsets:** dropping discs whose outermost plotted marker is clipped (KURVS-3, -16, -17): +1.85σ, non-diagnostic; keeping only discs whose farther side reaches ≥ 0.9 R_max: +1.95σ; dropping KURVS-13, -17, -21: +1.39σ. Extension to the 19 discs with V/σ0 ≥ 1 (labelled, mu = 0.67): +2.07σ, lean rival, but the model-value column on the same 19 is +1.79σ non-diagnostic.
   - **Grid A2–A5, A7 (19 rows):** lean rival in 7 (0.37); the frozen line (≥ 0.80) FAILS; no row has the rival above +2σ. Rows that leave the class: each side alone (non-diagnostic, +1.55σ and +1.06σ), the nearer side (lean flat), annulus [0.7, 1] (non-diagnostic), annulus [0.6, 1] (lean flat), outer five (non-diagnostic), V-b and A5x (lean flat), A5y (n = 2 discs only), i_SFR + 5° (non-diagnostic).
   - **Coherent V scale (A8):** the lean ends at v_s = 0.955 (a 4.5% lower V; flat = +2σ). The model-value column needs 0.891 (11%). The rival reaches −2σ at 0.842.
3. **Does marker choice reintroduce the P0-versus-P4 pressure ambiguity? Yes, by my frozen line.**
   - s_mid (Δ′_flat + Δ′_H = 0 at μ = 0.67; model value 0.669) is 0.736 for the primary, and over the 24 measured-marker rows of the grid runs 0.548–1.557 (range 1.009; line ≤ 0.20). It exceeds 1.0 in 11 rows and 1.42 in 2 (A5y 1.56, A6 f = 0.5 1.53); in 11 rows not all five placed prescriptions (s = 1.00–3.00) lie above it. Frozen line (iii): FAIL.
   - The movers are the radius rows (A2 nearer side, A3 [0.6,1], A5, A5x, A5y, A6 f ≤ 0.7) and the inclination scale (i_SFR − 5°: 0.548). The same-radius choices (V-a, V-c, V-d, A3 [0.8,1], A4 k = 2, 3) stay at 0.74–0.87.
   - At s = 0 (P0) the primary reads flat −1.94σ, rival −4.55σ, T +0.89σ, i.e. class LEAN FLAT (the model-value P0 is non-diagnostic, both outside, flat −2.28σ). CFG189's README does not mention that the measured markers move the P0 class.
4. **CFG189 sentences my numbers do not support:** section 6.

## 1. Table against CFG189 (row by row)

"CFG189" = its README (read before my runs) and, opened after my runs, its committed `.out` and `_results.json`. "Mine" = the frozen main run. Pass lines as frozen (criteria section 4).

| row | CFG189 | mine | line | verdict |
|---|---|---|---|---|
| **P1 C1** model col 3, i_star error term: flat / rival / T | +0.1441 / −0.0060 / +0.3227 | +0.1441 / −0.0060 / +0.3227 | 5e-4 | **REPRODUCES** |
| **P2** per-disc measured/model −1 (KURVS 3, 7, 8, 9, 11, 13, 15, 16, 17, 21), % | +10.5, −15.2, −6.6, +0.4, −3.3, +9.7, −6.5, −5.8, −22.3, −6.0 | +10.5, −15.2, −6.6, +0.4, −3.3, +9.7, −6.5, −5.8, −22.3, −6.0 | 1.0 pp | **REPRODUCES** (10/10; R_out 10.065 / 10.050 / 7.337 for KURVS-3 / -16 / -17) |
| **P3** primary flat | +0.125 ± 0.051 (+2.4σ) | +0.1249 ± 0.0511 (+2.45σ) | 0.008 / 8% / 0.25 | **REPRODUCES** |
| rival | −0.021 (−0.4σ) | −0.0211 ± 0.0496 (−0.42σ) | | **REPRODUCES** |
| T | +0.295 (+5.5σ) | +0.2953 ± 0.0540 (+5.47σ) | | **REPRODUCES** |
| **P4** primary class | lean rival | lean rival | exact | **REPRODUCES** |
| V-a (z flat / rival / T; class) | +2.4 / −1.0 / +5.9; lean rival | +2.44 / −1.00 / +5.93; lean rival | 0.35 | **REPRODUCES** |
| V-b | +0.1 / −3.2 / +3.4; lean flat | +0.14 / −3.15 / +3.43; lean flat | | **REPRODUCES** |
| V-c | +2.8 / +0.1 / +5.7; lean rival | +2.83 / +0.09 / +5.75; lean rival | | **REPRODUCES** |
| V-d | +2.2 / −0.7 / +5.3; lean rival | +2.20 / −0.70 / +5.26; lean rival | | **REPRODUCES** |
| BS (post-comparison, f_bs quoted from CFG189's `.out`) | +2.2 / −0.6 / +5.2; lean rival | +2.22 / −0.64 / +5.25 (esig unscaled, CFG189's convention); +2.23 / −0.65 / +5.27 (esig scaled with σ); lean rival | | **REPRODUCES**, NOT independent (f_bs is CFG184's) |
| **P5** shifts (dex; z), flat / rival / T | −0.019 (−0.84); −0.015 (−0.29); −0.027 (−1.46) | −0.0193 (−0.84); −0.0150 (−0.29); −0.0274 (−1.46) | 0.006 / 0.3 | **REPRODUCES** |
| headline | CHANGED (T's z shift 1.46 > 1); 1 of 5 variants flips | CHANGED; 1 of 4 checked here flips (V-b), BS lean rival, so 1 of 5 | exact | **REPRODUCES** |
| **P6** break-evens s = 1, measured flat / rival / T | 1.86 / 0.50 / 3.80 | 1.859 / 0.504 / 3.801 | 6% | **REPRODUCES** |
| model | 2.11 / 0.62 / 4.34 | 2.109 / 0.621 / 4.335 | 4% | **REPRODUCES** |
| T lower 1σ edge at s = 1 against 3.47 | below (gas-allowed) | 2.995 | | **REPRODUCES** |
| T centrals s = 1.42 … 3.00, excluded | 4.97 … 9.11 | 4.967, 5.508, 5.695, 9.110 (lower edges 3.98 … 7.47) | 6% | **REPRODUCES** |
| T at P0 | +0.9σ | +0.054 ± 0.060 (+0.89σ) | 0.3 | **REPRODUCES** |
| fit points s0 at μ = 0.67: flat / rival / T | 0.42 / 1.12 / < 0 | 0.424 / 1.119 / < 0 (model 0.389 / 1.033 / < 0) | 0.05 | **REPRODUCES** |
| **P7** C2 count | 22 of 231; 2 in KURVS-3, 20 in KURVS-17 at 0.065 kpc | 22 of 231; 2 in KURVS-3 (−9.41, −8.57 kpc: nearest σ marker 1.68, 0.83 kpc away); 20 in KURVS-17, of which **19 at 0.065 kpc and 1 (the clipped marker at 6.96 kpc) with no σ counterpart, 0.906 kpc away** | ±2 / ±0.01 | **REPRODUCES** (count and offset; the "whole panel" wording is not exact) |
| **P8** determinism | (its run) | main output byte-identical on a second run (and on the `run_all.sh` re-run) | exact | **REPRODUCES** |

**Overall: REPRODUCES on P1–P8.** In the main script alone P4 reads PARTIAL (9 of 10 rows) because BS could not be computed there (CFG184's functions may only be opened after the main and MUTATE runs were saved); the post-comparison BS row closes it.

**Every difference, classified.**
- **Numerical (≤ 1.7e-5 in Δ′ and σ; ≤ 1.0e-4 relative in break-evens; ≤ 3.8e-5 in fit points; 0 of 75 status labels):** CFG189 exec's CFG141's pipeline and re-implements CFG175's machinery; mine imports the CFG165 referee module. Per-disc R, V, eV, σ, σ-error: identical to 0.0 (`CFG194_diag_post.out`).
- **Definition (mine, declared):** (i) the primary uses i_SFR in the ±5° error term, as CFG189's text says, while C1 (model value) uses i_star as CFG160 did; the swap moves flat by +0.0026 dex in the model-value cell (chain step S1) and 0.0003 in the primary (V-d′), so it is not the cause of any shift. (ii) BS: the frozen rule gives σ_int = σ√(1 − f_bs); CFG189 leaves σ's error unscaled; mine (both variants printed) differ by 0.0003 dex. (iii) The break-even statistic and the status rule are the ones CFG175/183 use.
- **Definition/README wording (CFG189):** "twenty are KURVS-17's whole panel offset by a constant 0.065 kpc": 19 markers are at 0.065 kpc, the 20th (a clipped marker) has no σ counterpart. Count and offset stand.
- **README rounding/framing:** "T +5.5σ" is +5.47; "(−1.46)" exact.
- **Framing error of MINE (kept):** my frozen text defined s_mid as "Δ′_flat = Δ′_H", which has no root. The definition that reproduces CFG162/168's 0.669 exactly is Δ′_flat + Δ′_H = 0 (the data midway between the laws); the z-sum reading gives 0.665. I used the former and state it in `CFG194_lib.py`.
- **Physics:** none. No arithmetic disagreement.

## 2. Where independence stops

- **Imported read-only from `CFG165_kurvs_referee/CFG165_referee_kurvs_p4.py` as `M` (shared, NOT independent):** `load_kurvs` (non-velocity columns; the model-value column only for C1), `load_sparc_anchor`, `per_object`, `pool` (χ²/dof inflation), `anchor_pool`, `cell`, `spec`, `alpha_K` (Kretschmer's α(x) as quoted, unverified literature), `classify`, `E_of_z`, `gbar`, `gpred`, and through it `CFG4_common.nu_mono` and the a0 constants. `MUTATE` forced to "0" during the import. CFG165/167/168/180/183 showed this pipeline reproduces CFG160/161/162/170/175.
- **Mine:** the marker reader, the unclipped filter, the outer-point rules (primary, V-a…V-d, A2–A6), σ at R_out (own interpolation), t(z)/t0 and the E-patch, the break-even solver and status rule, fit points, s_mid/s_f2/s_h2, the headline label, every attack and mock.
- **Shared and not re-checked:** the data chat's digitisation itself (`kurvs_rc_points.csv`, sigma profiles, model curves) — my only checks are C4 (model curve at R_max / sin i_SFR = Table B1 col 3 within 0.6%: ratios 0.9944–1.0087) and C5 (511 markers, 18 clipped, 231 in the ten discs). CFG140's set-up (thin discs, spherical surrogate, gas bracket, mass 0.15 dex, ±5°, the ten f_DM discs, the z = 0 SPARC anchor). CFG175's gas ceiling 3.47.
- **BS is NOT independent:** CFG184's forward model is not re-derived; the f_bs per disc are quoted from CFG189's `.out` (a departure from the frozen plan, disclosed in `CFG194_bs_post.py`).
- Agreement therefore shows that the frozen text plus the data plus the shared pipeline determine the numbers. It does not test ν_mono, α(x), the pressure prescriptions, the digitisation, or any law's physics.

## 3. Controls and MUTATE (all runs saved; exit 1 = the control bites; wrong expectations kept)

My controls (main exits 0): C1 above; C3 (E := 1 makes the H rows equal flat's exactly, the original E replays the rival exactly, t/t0 = −0.3264 / −0.5099 dex at z = 0.85 / 1.5); C4 (0.9944–1.0087); C5 (511 / 18 / ten discs / 231 / every side has an unclipped marker). All PASS. C2′ (the marker-versus-σ radius agreement, kept failing in CFG189) is scored as row P7. Sign structure: v has the sign of R in 230 of 231 markers (KURVS-15: 21 of 22), so |v| is used.

| MUTATE | what | result | frozen expectation | verdict |
|---|---|---|---|---|
| M1 | V × 10^0.3 | flat +0.551 (+10.4σ), rival +0.406 (+7.9σ): non-diagnostic (both outside) | class ≠ lean rival | bites (exit 1) |
| M2 | law labels swapped in `classify` | non-diagnostic (both outside), NOT lean flat | ≠ lean rival; I expected non-diagnostic | bites (exit 1); the map is not label-symmetric (as CFG165 M3) |
| M3 | no deprojection (V = \|v\|) | flat +0.028 (+0.53σ), rival −0.118 (−2.34σ): lean flat | class ≠ lean rival | bites (exit 1) |
| M4 | T := flat (t/t0 replaced by 1) | T rows equal flat's; the T shift z equals flat's (−0.8381) | identity | bites (exit 1); C1's T check fails, as it must |
| M5 | innermost unclipped marker with \|R\| ≥ 0.25 R_max | flat −0.052 (−1.32σ), rival −0.175: lean flat; \|ΔΔ′_flat\| = 0.177 | > 0.05 dex | bites (exit 1) |
| M6 | σ permuted across discs (seed 194) | flat +0.146 (+2.83σ), rival −0.001: lean rival | informational | **does not bite (exit 0)**, as CFG165's M6: the σ pairing is not what carries the lean; kept |

## 4. The attacks (procedures as frozen; the headline stays the primary)

Seeds: bootstrap 194; sign-flip and mocks 194 and 195 (N = 10,000 per world and family); the two seeds agree in every class fraction to 0.010 (line 0.02).

### (a) The digitisation — which marker is "the outer point"
Decision cell (Δ′ (z) for flat / rival / T, class):

| row | flat | rival | T | class |
|---|---|---|---|---|
| A1 primary | +0.125 (+2.45) | −0.021 (−0.42) | +0.295 (+5.47) | lean rival |
| A2 + side alone | +0.075 (+1.55) | −0.069 (−1.46) | +0.239 (+4.66) | non-diagnostic (both within) |
| A2 − side alone | +0.060 (+1.06) | −0.080 (−1.46) | +0.221 (+3.68) | non-diagnostic (both within) |
| A2 nearer side | +0.009 (+0.17) | −0.128 (−2.53) | +0.162 (+2.88) | lean flat |
| A3 annulus [0.8,1] weighted / median | +0.097 (+2.29) / +0.102 (+2.40) | −1.10 / −0.98 | +5.75 / +5.85 | lean rival |
| A3 annulus [0.7,1] weighted / median | +1.80 / +1.93 (z) | −1.58 / −1.38 | +5.44 / +5.60 | non-diagnostic (both within) |
| A3 annulus [0.6,1] weighted / median | +1.08 / +1.31 (z) | −2.60 / −2.14 | +4.82 / +5.07 | lean flat |
| A4 outer 2 / 3 / 5 | +2.52 / +2.44 / +1.61 (z) | −0.73 / −1.00 / −1.95 | +5.87 / +5.93 / +5.18 | lean rival / lean rival / non-diagnostic |
| A5 V-b (both sides, shorter radius) | +0.006 (+0.14) | −0.132 (−3.15) | +0.162 (+3.43) | lean flat |
| **A5x farther side alone at that radius** | +0.015 (+0.37) | −0.124 (−3.06) | +0.175 (+3.98) | **lean flat** |
| A5y both sides at 0.8 R_max (n = 2 discs) | +0.002 (+0.02) | −0.143 (−1.61) | +0.155 (+1.52) | non-diagnostic (both within) |
| A6 f = 0.5 / 0.6 / 0.7 / 0.8 (n = 9) / 0.9 (n = 8) | −0.58 / +0.14 / +0.96 / +1.74 / +1.99 (z) | −4.33 / −3.56 / −2.57 / −1.44 / −1.00 | +3.01 / +3.79 / +4.50 / +4.91 / +5.08 | lean flat ×3 / non-diagnostic ×2 |
| A7 V-d (i_star deprojection and error term) | +2.20 (z) | −0.70 | +5.26 | lean rival |
| A7 V-d′ (i_star error term only) | +2.45 | −0.44 | +5.49 | lean rival |
| A7 i_SFR + 5° coherent | +0.097 (+1.90) | −0.049 (−0.98) | +4.95 | non-diagnostic (both within) |
| A7 i_SFR − 5° coherent | +0.161 (+3.14) | +0.015 (+0.29) | +6.13 | lean rival |

- **Frozen line (i) (class choice-robust iff ≥ 80% of rows A2–A7 keep lean rival and none has the rival above +2σ): 7 of 19 (0.37): FAIL.** My estimate (0.5 ± 0.2) was slightly optimistic; the direction (FAIL) was right.
- **(ii) radius versus centring:** A5x flips too and A6 is monotone in f, so the verdict is RADIUS-driven; the two-side average adds ≈ 0.2σ.
- **(iii) pressure ambiguity:** s_mid range 1.009 over 24 measured-marker rows: REINTRODUCED (question 3 above). Full table in `CFG194_attacks_a.out` (A10).
- **A8 V-scale tolerance:** class against v_s 0.90–1.10; lean rival for v_s ≥ 0.96 (z_flat +2.05 at 0.96, +1.95 at 0.95). Crossings: flat = +2σ at 0.9547, rival = −2σ at 0.8422, rival = +2σ at 1.2520; the model-value column: 0.8905 and 0.8313. This is the single number that bounds the untested beam-smearing bias of V, centring and non-circular motion: a coherent −4.5% V error ends the lean.
- **A9 decomposition, model value -> measured primary** (flat z; rival z; T z; Δ′ steps in dex):

| step | flat | rival | T |
|---|---|---|---|
| S0 model col 3 at R_max (C1) | +0.1441 (+3.28) | −0.0060 (−0.14) | +0.3227 (+6.94) |
| S1 + i_SFR in the error term | +0.1467 (+3.32) | −0.0027 (−0.06) | +0.3247 (+6.94) |
| S2 model curve read at R_out (R, σ at R_out same side, V move) | +0.1321 (+2.87) | −0.0135 (−0.30) | +0.3023 (+6.14) |
| S3 measured V, model errors (value effect) | +0.1220 (+2.63) | −0.0235 (−0.52) | +0.2922 (+5.89) |
| S4 measured V and marker errors (= primary) | +0.1249 (+2.45) | −0.0211 (−0.42) | +0.2953 (+5.47) |
| step dz: S2 / S3 / S4 | −0.46 / −0.24 / −0.18 | −0.24 / −0.22 / +0.10 | −0.79 / −0.25 / −0.42 |

  - **Most of the shift is the change of radius and σ at R_out, not the marker-minus-model value.** S2 carries −0.46 of flat's −0.84 (55%) and −0.79 of T's −1.46 (54%). It is mainly KURVS-17 (R_out 7.34 kpc against R_max 9.9; the model curve read there is 14.9% below col 3; the other nine discs move by ≤ 1%), and the side σ against the two-side σ_out (KURVS-3 73.9 against 55.3, KURVS-13 46.7 against 61.3, KURVS-11 57.7 against 65.8). Split from S1 (labelled extra, added after seeing S2): radius and model V only Δ′_flat +0.1326 (z +3.28); σ at R_out only +0.1462 (z +3.19): not additive.
  - The marker-minus-model value moves Δ′ by −0.010 dex in every law (−0.24 in z for flat).
  - The value-only versus σ-only split of flat's z drop (C-c): value-only −0.44, σ-only −0.46; rival −0.34 / +0.01; T −0.59 / −0.96. **About half of flat's z drop is the larger error, as I estimated (0.5 ± 0.15).**
  - My estimate that reading the model at R_out moves flat by < 0.01 dex was WRONG (−0.015 dex), because of KURVS-17; kept.

### (b) The disc set
- **B1 leave-one-out:** lean rival in 9 of 10 (line ≥ 8 PASS); T gas-allowed at s = 1 in 10 of 10 (lower edges 2.74–3.10).
- **B2 bootstrap (N = 2000, seed 194):** lean rival 0.764 / non-diagnostic 0.234 / lean flat 0.002; P(T gas-allowed at s = 1) = 0.928; P(z_T > 2) = 1.000.
- **B3, B4:** as in question 2.
- **Meaning:** flat's +2.45σ sits 0.45σ above the class edge; the ten-disc class survives dropping any one disc except KURVS-21, but not the clipped-marker discs together, the ≥ 0.9 R_max discs, or dropping KURVS-13, -17, -21. It is a ten-disc lean.

### (c) The error model and null worlds
- **C-a marker consistency:** χ² of (V_meas − model curve at R_out) with the marker errors = **2.27 for 10 dof, p = 0.994; rms pull 0.48; mean pull −0.23** (fractional meas/model − 1 mean −0.032). The pooled χ²/dof inside `pool` is 1.25 for the model-value run and **0.36** for the measured primary. The markers agree with the model far better than their errors allow: the model was fitted to these same markers, adjacent points are correlated (adaptive binning), and each bar is the single-pixel line-fit error. My estimate (χ² 6–16, p > 0.05) was wrong on the number; kept. So the larger marker errors weaken the z without adding information: the primary's z_flat +2.45 is not "more honest" than +3.28, it is the same data with a noisier estimator.
- **C-b sign-flip test** (value-only shift, baseline = model curve at R_out, primary errors and σ fixed): observed −0.0126 dex (the same in all three laws); sd under random signs 0.0107; two-sided p = 0.257 / 0.262 / 0.251 (random, N = 10,000, seed 194); exact enumeration of the 1024 sign vectors 0.256 / 0.260 / 0.249. **The marker-minus-model shift is not distinguishable from noise.**
- **C-d error variants:** E1 primary; E2/E3 larger/smaller bar identical to E1 (the digitised bars are symmetric); E4 errors × 1.5: flat +0.126 ± 0.057 (+2.21σ), T +4.97σ, lean rival; E5 5 km/s floor: +2.42σ, lean rival; E6 common V-scale error (ln s ~ N(0, 0.03) as covariance, added σ 0.0148): +2.35σ, lean rival. The class is stable to the error variants, but the edge margin shrinks to 0.2σ (E4).
- **C-e mock null worlds** (truth = the real baryons, measured σ_out, R_out and marker errors, the z = 0 pipeline offset +0.0967 dex the SPARC anchor carries; mock marker = law's V_obs + N(0, marker error); the analysis is the primary pipeline). N1 = CFG165's nuisance (μ_true lognormal median 1.0, 0.3 dex; α × lognormal(0, 0.4) per disc × coherent lognormal(0, 0.2)); N1x (extra scatter) is NOT run because the rms pull is below 1. Seed 194 (seed 195 within 0.010):

| template | family | truth | mean Δ′ (flat / rival / T) | P(lean rival) | P(z_flat ≥ 2.45) | T gas-allowed at s = 1 (first 1000 mocks) |
|---|---|---|---|---|---|---|
| measured | ideal | flat | +0.013 / −0.135 / +0.185 | 0.000 | 0.000 | 1.00 |
| | | rival | +0.155 / +0.007 / +0.329 | 0.989 | 0.919 | 0.45 |
| | | T | −0.108 / −0.255 / +0.063 | 0.000 | 0.000 | 1.00 |
| | N1 | flat | +0.070 / −0.077 / +0.242 | 0.259 | 0.140 | 0.95 |
| | | rival | +0.200 / +0.052 / +0.373 | 0.760 | 0.913 | 0.17 |
| | | T | −0.049 / −0.195 / +0.121 | 0.001 | 0.001 | 1.00 |
| model-value errors | ideal | flat / rival / T | | 0.000 / 1.000 / 0.000 | | |
| | N1 | flat / rival / T | | 0.331 / 0.740 / 0.001 | | |

  - **Frozen informativeness rule** (P(lean rival | flat) < 0.05 and P(lean rival | rival) > 0.3): ideal, measured markers: 0.000 and 0.989, JUSTIFIED (model-value errors: 0.000 and 1.000). **N1, measured markers: 0.259 and 0.760, NOT justified** (model-value errors: 0.331 and 0.740; seed 195: 0.263 / 0.761 and 0.320 / 0.740). The lean is strong only in the idealised world in which gas and α are known; with the nuisance a flat world produces the observed class one time in four. My ideal-world estimates (P(lean rival | flat) 0.10–0.25, | rival 0.6–0.85) were wrong: the ideal mocks are cleaner than I guessed (0.000 and 0.99); the N1 ones (0.26 / 0.76) were in range. Kept.
  - **Likelihood ratio at the observed Δ′_flat = +0.1249, rival-truth over flat-truth:** N1 measured 0.61 (Gaussian), 0.55 (KDE); N1 model-value errors 0.84 / 0.69; ideal astronomically large (the ideal sd is 0.02). **With gas and α uncertain the observed Δ′_flat carries no weight for the rival over flat.** T-truth over flat-truth: ≈ 0 in both families, because the mocks apply the correct s = 1 pressure and T under-predicts there; this is the T-at-Kretschmer statement, not a T-at-P0 one (T at P0 is not a mock world here).
  - **Measured versus model power:** swapping the model-value errors for the marker errors barely changes the N1 class fractions (0.259 / 0.760 against 0.331 / 0.740); in the ideal world it widens the flat Δ′ sd from 0.009 to 0.023.

### (d) The kept C2′ failure
- **D1:** the markers over 0.02 kpc: KURVS-3's two extra markers (−9.41, −8.57 kpc; nearest σ markers 1.68 and 0.83 kpc away) and KURVS-17's 20 (19 at the constant offset +0.0650 kpc; the clipped 6.96-kpc marker has no counterpart).
- **D2 repairs** (labelled post hoc), primary and V-a…V-d rows: (i) KURVS-17's σ profile shifted by +0.065: primary +2.44 / −0.43 / +5.46, no class change, |dz| ≤ 0.01; (ii) σ from the nearest σ marker: same to 0.01; (iv) markers with no σ counterpart dropped from the velocity lists: the primary is unchanged (the dropped markers are never its outer point); V-b moves +0.14 → +0.06, −3.15 → −3.22, +3.43 → +3.34 (|dz| ≤ 0.09; the only row where a dropped marker is an outer point is V-b for KURVS-3); (iii) KURVS-17 dropped: primary +2.09σ lean rival, V-b flat −0.54σ, V-d non-diagnostic (+1.83σ).
- **Frozen rule (no class change, |dz| ≤ 0.10 over D2 i–iv): as written it reads MATERIAL (largest |dz| 0.92)**, but only because (iii) is a sample change (it is the LOO of B1), not a repair. Without (iii): largest |dz| 0.093 over all five rows, no class change: **the mismatch is immaterial to every CFG189 number** and a passing C2 would change nothing. I report both.

### (e) Agreement with the model-value verdicts (CFG165/175)
- **Same:** the class at the decision cell (lean rival), the sign of Δ′ for every law (flat +, rival −, T +), the break-even ordering rival < flat < T at every s, T's status at s ≥ 1.42 (excluded), T fitting at P0, the placed prescriptions above s_mid for the primary (s_mid 0.669 → 0.736).
- **Different:** V-b's class (lean flat); the pooled lean's margin (flat +3.28σ → +2.45σ, edge margin 1.28σ → 0.45σ); T's status at s = 1 (excluded with a 2% margin → allowed, lower edge 2.995 against 3.47; robust in LOO, 10 of 10, and 0.93 of bootstrap resamples, so it is a real change: CFG183 had shown the old label was fragile at 52%); the P0 class (non-diagnostic, both outside → lean flat, flat −1.94σ).
- **Why:** the A9 chain: the radius/σ change at R_out (mostly KURVS-17) ≈ 55% of the z shift, the marker-minus-model value ≈ 29%, the larger errors ≈ 22%, the inclination-column swap −5%. T's status change is the −0.027 dex shift acting on T's lower edge (4.335 → 3.80 central).

## 5. Hand-estimate scorecard (criteria section 3; wrong expectations kept)

| estimate | result |
|---|---|
| primary flat / rival / T Δ′ +0.12 / −0.02 / +0.29 (± 0.015); P(each within 0.008) 0.55 | +0.1249 / −0.0211 / +0.2953: in |
| σ_flat 0.051 ± 0.004 | 0.0511 (in) |
| class lean rival (0.9) | yes |
| variant classes rival, flat, rival, rival, rival (all five 0.45) | all five (BS via the quoted f_bs) |
| shifts z −0.8 / −0.3 / −1.4 | −0.84 / −0.29 / −1.46 (in) |
| CHANGED (0.75) | yes |
| per-disc ratios within 1 pp (0.6) | 10 of 10 to 0.1 pp |
| break-evens within 6% (each 0.5) | all within 1% |
| C2′ 22 of 231, 2 + 20 (0.75) | 22 of 231; 2 + (19 + 1) |
| C1 (0.9) | yes |
| radius-only reading of the model curve moves flat < 0.01 dex (0.6) | **WRONG:** −0.015 dex (KURVS-17) |
| farther side alone at V-b's radius flips (P 0.35) | **WRONG:** it flips; the driver is radius |
| grid keeps lean rival 0.5 ± 0.2 (line 0.8: FAIL expected) | 0.37: FAIL, as expected |
| V scale that ends the lean −3% to −5% | −4.5% (in) |
| pressure ambiguity NOT reintroduced (0.6) | **WRONG:** reintroduced (s_mid range 1.0) |
| LOO lean rival in 4–8 of 10 (median 6; P(≥ 8) 0.25) | **WRONG:** 9 of 10 |
| marker χ² 6–16, p > 0.05 | **WRONG:** 2.27, p 0.994 |
| sign-flip p > 0.2 | 0.26 (in) |
| about half of flat's z drop is the σ | 0.51 (in) |
| ideal mocks: P(lean rival | flat) 0.10–0.25, | rival 0.6–0.85; T < 0.05 | **WRONG** on the ideal numbers (0.000, 0.99); T 0.000 (in) |
| N1: 0.3 / 0.55; rule FAILS N1 (0.8) | 0.26 / 0.76; FAILS (in) |
| C2 immaterial (0.85) | literal rule: MATERIAL (0.92, from the sample-change row); without it 0.093, immaterial |
| direction agrees with the model-value verdicts (0.9) | yes (class, signs, ordering); V-b and T's s = 1 label differ |

## 6. CFG189 sentences my numbers do not support (or only partly)

1. **"It weakens the lean: flat goes from +3.3σ to +2.4σ, because the markers carry larger errors and scatter about the model by −22% to +11%."** Half of the z drop is the larger error (which carries no information: χ² = 2.3 for 10 dof, p = 0.99, pooled χ²/dof 0.36), about 29% is the marker-minus-model value (−0.010 dex, sign-flip p = 0.26: noise), and the largest single piece, ≈ 55% by the chain, is the change of radius and σ at R_out, mostly KURVS-17 (whose two outer markers are clipped) plus side-specific σ. The "scatter about the model" is not the main driver.
2. **"It measures at the shorter side's outermost radius … That trades radius for cancelling any centring offset."** The centring cancellation is not what changes the class: the farther side alone at the same radius gives the same class and almost the same z (A5x). The radius is the whole effect.
3. **"Standing: the KURVS lean rests on a calibration, gas and radius choice the data cannot fix."** Supported, and stronger than the README says: 12 of 19 pre-declared marker choices leave the class, the lean ends at a coherent −4.5% in V, and the frozen mock rule is NOT met once gas and α are uncertain (P(lean rival | flat) 0.26).
4. **"1 of 5 variants flips"** is true and understates the fragility: it counts only CFG189's five; the lean rival is 0.45σ above the edge and the class is decided by which radius is "outer".
5. **Omission (not a wrong sentence):** the P0 class changes (non-diagnostic → lean flat, flat −1.94σ) under the measured markers; T's s = 1 gas status change (excluded → allowed) is robust in leave-one-out and bootstrap, unlike the fragile old label.
6. **Wording of disclosed departure 1:** "twenty are KURVS-17's whole panel" is 19 markers plus one unpaired clipped marker.

## 7. Files and re-run

Files (scratch dir; nothing in the repo): `CFG194_FROZEN_CRITERIA.md` (committed 7291bc798), `README.md`, `CFG194_lib.py`, `CFG194_referee_main.py`, `CFG194_attacks_a.py`, `CFG194_attacks_c.py`, `CFG194_bs_post.py` and `CFG194_diag_post.py` (post-comparison), `run_all.sh`, `CFG194_manifest.txt`; outputs `CFG194_main.out/_results.json`, `CFG194_MUTATE_{1..6}.out/_results.json`, `CFG194_attacks_a.out/_results.json`, `CFG194_attacks_c_seed{194,195}.out/_results_seed{194,195}.json`, `CFG194_bs_post.out/_results.json`, `CFG194_diag_post.out`, `run_all.out`.

```
export ZF_REPO=<repo>
bash run_all.sh        # main (rc 0), determinism check, MUTATE 1-6 (rc 1 = bites; M6 rc 0), attacks_a, attacks_c seeds 194 and 195, post-comparison, home-path grep; about 10 minutes (the two mock runs ~2 min each, alone)
```
Re-runs are identical apart from the timing lines (`[..s]`, `done in`) of the mock runs. Individually: `python3 CFG194_referee_main.py`; `MUTATE=k python3 CFG194_referee_main.py`; `python3 CFG194_attacks_a.py`; `python3 CFG194_attacks_c.py 194` (and 195; `CFG194_NMOCK=300` for a quick test).

κ = ½ and Ω_c h² stay fitted. a0(z) FLAT is the framework's distinctive law, a0 ∝ H(z) the rival, T the owner's third reading. Nothing here says the data favour any law, or that the theory is closed; a lean is not a detection.

## In-place re-run (orchestrator)

`bash run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`): main 0 (and byte-identical on its own second run); MUTATE 1-5 exit 1 (bite); MUTATE 6 exit 0 (informational, does not bite); the attacks (seeds 194 and 195), the BS post-comparison and the diagnostic exit 0; no absolute home path in any output. Every `.out`, `.err` and `_results*.json` is identical to the referee's apart from the per-line timings (`[13s]`) in the two mock outputs. The frozen criteria are `../CFG194_FROZEN_CRITERIA.md` (7291bc798). The referee's own sha256 manifest is not committed (the hashes of the timing-bearing mock outputs would differ). `CFG194_bs_post.py` and `CFG194_diag_post.py` are post-comparison scripts written after CFG189's outputs were opened; the BS variant is scored only there and uses CFG189's printed f_bs values, so it is not independent.
