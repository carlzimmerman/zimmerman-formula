# CFG263: hostile audit of the 32π / κ = ½ no-gos

**Standing.** κ = ½ stays FITTED. This audit can find errors and narrow scopes. It cannot derive the coefficient, and it did not.

**Bottom line.** No door was closed wrongly.
- Of the 8 load-bearing no-gos, none has a false load-bearing step (0 ERROR).
- One leg of X1 is a unit-dependent π-count presented as unit-free. This is the same class as the section-12 H3 correction, and it is uncorrected in X1. Its conclusion survives only because, in the other units, the condition restates the puzzle.
- Six findings are correct but narrower than their headline wording.
- Three are correct as worded. p12 is in fact more general than worded: it holds for any static-patch Killing normalisation under the null energy condition (NEC).

The criteria were frozen first: `CFG263_FROZEN_CRITERIA.md`, sha256 `ece04edd…`, 2026-10-01T21:42:56Z, unchanged (`shasum -c` passes). Every no-go was then re-derived with my own code before any original script or `.out` was opened. Totals: 148 checks in 11 scripts, all pass; `./run_all.sh` reruns everything in about 45 s.

## Findings

| no-go | class | evidence (file:line) | re-opened door |
|---|---|---|---|
| **G** symmetry | CORRECT-NARROWER-THAN-WORDED | The dichotomy, dilatation, Killing algebra (H-free, so(4,1)) and Tolman checks reproduce: `cfg263_01_G_symmetry.out:1-20`. The headline "no symmetry contains it" (`sonnet55_push/puzzle_32pi/README.md:151`) is broader than the tested set (`agents/G_symmetry_conformal/README.md:49-51`). G-iii holds for the φ field equation only; the gravity-coupled action sees the constant (`.out:12`). | no |
| **E** literature | CORRECT-NARROWER-THAN-WORDED | Every computed coefficient reproduces (2H, 1/6, 0.2023, Verlinde's d-minimum 3+2√2 > Z): `cfg263_02_E_literature.out:1-15`. The table row "horizon-first routes give rational Z" (`README.md:149`) drops E's own "(or 1/area)" (`agents/E…/README.md:65`). An area-first route is π-allowed: a₀²A_dS = 3/8 (`.out:13-14`). It is in the same class as "density", and no mechanism exists for it. | no |
| **X1-(i)** one generator | CORRECT-NARROWER-THAN-WORDED | The slots agree only at D = 4 (`cfg263_03….out:13-15`). The MacDowell-Mansouri slot 2(D−2)(D−3) is reproduced from E4(R) − E4(R − kΔ) (`.out:14`). Rejecting the labels "4 = D", etc. rests on X1's acknowledged shared-D-lift premise (`agents/X1_one_generator/README.md:117`). | no |
| **X1-(ii)** Noether / Euler origin | **PREMISE-UNVERIFIED** | Leg (a): "no r³ charge … can be a rational multiple of π^k there" (`agents/X1…/README.md:9`, `x1_05…out:17-29`, L held fixed only) is false in u-units. There G\|Q\|·u = 4π/3 (`cfg263_03….out:7-8`), because Q_IW(r) = −M_vac(r) (`.out:4`). Leg (b) rests on the assertion that "a₀ = ½√(Gρ) is an equation-of-motion statement" (`x1_05…out:39`), which is not derived. The conclusion survives because the u-unit condition GQ/r = −4π/3 is Gρ r² = 1 at r = 1/(2a₀), i.e. the puzzle restated (`.out:9`). | no |
| **K** density-linear family | CORRECT-NARROWER-THAN-WORDED | The offset c = ∫(1−μ)dy, the μₙ closed form, c(N) = 2N²/((N−1)(N−2)), N* = 2.07409, and the tail graft (p* = 2.10, about 1.0e-3 dex) all reproduce: `cfg263_04….out`. The "SUSY vacua have V ≤ 0" row (`agents/K…/README.md:13,78`) covers SUSY-preserving vacua only; a SUSY-breaking de Sitter (dS) minimum exists (`.out:23`). The accumulation-fraction difference is definitional (`cfg263_10….out:8`). | no |
| **L** SdS two-horizon | CORRECT-NARROWER-THAN-WORDED | Vieta relations, monotone bijection, T_b = T_c only at Nariai, μ* = 0.98695/0.98298, the integer elimination polynomial, and 19 functionals with no interior extremum (16 distinct) all reproduce: `cfg263_05_L_sds.out`. "No SdS-internal principle can produce Z" (`agents/L…/README.md:6`) holds for principles that are algebraic in Λ-units. The lane's own text admits u-algebraic ones (`:52,:56`). The only natural u-algebraic one, K_Σ = ρ_Λ, is unattainable (`.out:14`). | no |
| **N** Jacobson in dS | CORRECT-GENERAL | Tolman cancellation, exactly one mismatched pair (κ_obs, a), a₀ = H or 2H, the literal insertion being a threshold, R_kk = 0 in dS: `cfg263_06_N_jacobson.out:3-11`. The thermal structure knows only a and H, so its outputs are qH, which is excluded in any units. | no |
| **p12** horizon identity | CORRECT-GENERAL (stronger than worded) | The identity 1 − 2κr_h = 8πρ r_h² and (A)-(D) reproduce (`cfg263_07….out:1-5`). With a lapse N(r), κ = N_h f′(r_h)/2 (covariant, `.out:8`) and N′/N = 4πr(ρ+p_r)/f (`.out:7`). Under NEC, with any static-region normalising observer, \|κ\|r_h ≥ (8π−1)/2 = 12.07 (`.out:9-11`). So (D) does not need the f-normalisation stated at `README.md:197`. `STANDING_2026-09-29.md:335` stands. | no |
| **B3** modified horizon equations | CORRECT-NARROWER-THAN-WORDED | The SdS-form and Glavan-Lin results (a = −8π/3, 1 + 2a = −15.755) reproduce (`cfg263_07….out:14-15`). The summary "a modified horizon equation re-inserts the coefficient" (`README.md:206`) is broader than what was computed: Einstein-aether, Horava/khronon, AeST, TeVeS, BIMOND and CA5/V0 are NOT computed (`agents/B3…/README.md:23`). B3 handled only the signed, black-hole-type reading, N_h = 1/(1−8π) < 0 (`b01.out` K3). The cosmological-type \|κ\| reading is closed here under NEC. | no |
| **sol61** clock + BBN | CORRECT-GENERAL (within its stated scope) | The Friedmann constraint of the λ-action, G_cosm = 2G/(3λ−1), C = 4D(1+D)²/(3(3λ−1)), C = (2/3)R(1+D)³, C > (2/3)R/(1−R)³, R < 0.8238740919 and the ΔN diagnostics all reproduce: `cfg263_08….out`. Not re-derived here: the static law G_N = G(1+D)/D and a₀_N (`sol61_push/CANONICAL_CLOCK_RESULTS.md:55-59`). | no |

The classes are the output of the frozen classifier (`cfg263_lib.py`, written before any run) applied to the scripted flags. The table is in `cfg263_11_classify.out` and in `results.json` under `CLASSIFICATION`. The flag `headline_scope_ok` is a manual comparison of wording against tested class; the file:line evidence above is the basis for it.

## New small results (sharpenings, not doors)
1. **The RAR offset has a closed form.** For ν = 1/(1 − e^{−√y}), c = 4Γ(4)ζ(4) = 4π⁴/15, so Gρ/a₀² = π³/30 = 1.0335 (`cfg263_01….out:21-24`). This is lane G's and lane K's "1.03" made exact.
2. **Bose-shaped ν functions cannot give 4.** Every ν − 1 = g/(e^{β√y} − 1), renormalised to its own deep-MOND a₀, gives W_v = π³/(30g³), independent of β (`cfg263_04….out:25`). A thermal (Bose) origin of the RAR shape cannot yield W_v = 4 under the offset reading.
3. **The offset does not depend on the formulation.** The AQUAL and QUMOND offsets are equal whenever (x − y)² → 0 at both ends (`cfg263_04….out:18`), so K's choice of AQUAL is not load-bearing.
4. **X1's static-patch charge is the vacuum mass.** The Iyer-Wald charge is exactly −M_vac(r) (`cfg263_03….out:4`). That is why its u-unit value is (4π/3) × (ball volume factor).
5. **p12 (D) needs NEC, not the f-normalisation.** Exotic radial tension p_r = −1.395 (ρ + p_r < 0) between the observer and the horizon reaches \|κ\|r_h = ½ exactly (`cfg263_09_mutate.out:5`).
6. **The gemini radius lies outside the static patch.** R* = c/√(Gρ_Λ) satisfies R*/L = √(8π/3) = 2.894 (`cfg263_07….out:16`).

## MUTATE controls (`cfg263_09_mutate.out`; mutant copies and their outputs in `mutants/`, never the main `results.json`)
| control | planted change | caught by |
|---|---|---|
| M-ERR-1 | p12 identity: 8π → 4π | `P2_horizon_identity` FAILS (exit 1) |
| M-ERR-2 | K: c(N) = 2N²/((N−1)(N+2)) | `K2c_OR_family` and `K3b_reading_algebra` FAIL |
| M-ERR-3 | X1: Komar used as the Iyer-Wald charge | 6 checks FAIL, including the Schwarzschild normalisation and Q = −M_vac |
| M-PREM-1a | X1 π-power claim with Λ held fixed vs G ρ_Λ admitted | class shifts CORRECT-GENERAL → PREMISE-UNVERIFIED |
| M-PREM-1b | p12's strengthened (D) with NEC vs an NEC-violating layer | class shifts CORRECT-GENERAL → CORRECT-NARROWER-THAN-WORDED (\|κ\|r_h = 0.500000) |

## Hand estimates (frozen) vs outcome
| no-go | P(error) | P(narrower) | outcome |
|---|---|---|---|
| G | 0.10 | 0.70 | narrower |
| E | 0.10 | 0.80 | narrower |
| X1 | 0.25 | 0.70 | (i) narrower; (ii) premise-unverified (unit-dependent π-count; the suspicion from frozen §8 is confirmed) |
| K | 0.10 | 0.75 | narrower |
| L | 0.08 | 0.60 | narrower |
| N | 0.08 | 0.60 | general |
| p12/B3 | 0.10 | 0.60 | p12 general (stronger than worded, as guessed in §8); B3 narrower |
| sol61 | 0.10 | 0.90 | general within scope |

Overall P(a re-opened door) was frozen at about 0.25. Outcome: none.

## Comparison with the originals (`cfg263_10_compare_originals.out`, 15/15)
Every load-bearing number in the originals' committed outputs equals my independent value: lanes G, E, X1, K, L, N, p12, B3, and sol61's own `runs/` results.

One apparent discrepancy was resolved. Lane K's "fraction of c from x < X" (4%, 25%, 66%, 97%; `k01….out:89`) is the partial second moment ∫₀ˣ x² dμ. My fractions (12%, 42%, 81%, 99%) are of ∫₀ˣ (1−μ) d(x²). The two differ by X²(1 − μ(X)) and agree once that term is subtracted. This is definitional, not an error.

Method differences, all mine:
- Killing algebra in conformal coordinates with symbolic H.
- The RAR offset by a parametric route and by bisection inversion.
- X1's charges from the covariant ∇ξ.
- The L functionals with a planted-extremum control.
- The p12 lapse via the covariant κ² = −½∇ξ·∇ξ.

## Door search (the criteria require a search of the record)
I searched `sonnet55_push/puzzle_32pi`, `sol61_push` and `campaign_fresh_gravity/closure_map`:
- **Sequestering** is in the record: XR20 T4, "not tied" (`closure_map/ACTIONS_AND_NOGOS.md:37`).
- **Universal and aether horizons** appear only as "NOT computed" (B3) and as a c₂ singularity (`ACTIONS_AND_NOGOS.md:86`).
- **G_cosm** is computed only in sol61's action.
- **The RAR/Bose closed form** appears nowhere in the record.

Each narrowing was tested against door rule D-b (frozen §4). Every candidate route either inserts the target, restates the puzzle, or has no equation; the reasons are in `cfg263_11_classify.py` (`ROUTES`).

## HANDOFF
**No re-opened door, so there is no untested route to hand off as a door.** For the sibling lane CFG264 (untried routes; not run here), three near-misses were considered and rejected, with the reason each failed the door rule:
1. **Preferred-frame coupling ratio (B3's uncomputed class).** If a theory gave the forced kernel a₀² = G_N ρ_v while Λ = 8πG_cosm ρ_v, then κ² = G_N/G_cosm, and κ = ½ means G_cosm = 4G_N. It fails the rule for three reasons:
   - The ratio is a free coupling, set to 4 by hand.
   - In the λ-model, G_cosm = 2G/(3λ−1) needs λ = ½ when G_N = G, or 1/3 < λ < ½ with sol61's G_N = G(1+D)/D. Both lie inside sol61's negative-kinetic window 1/3 < λ < 1 (`cfg263_08….out:16`).
   - BBN allows G_cosm/G_N in 0.92–1.04 only.
2. **u-unit Noether condition (X1-(ii)).** It is u-algebraic but is the puzzle restated: Gρ r² = 1 at r = 1/(2a₀).
3. **Area-first horizon route (E).** a₀²A_dS = 3/8 is π-allowed, but no mechanism supplies the 3/8.

Structural guidance that survives the audit, and is unit-independent:
- A mechanism whose only scales are a and H gives outputs qH, which Lindemann excludes in any units. This covers the dS group and its representations, the thermal T(a) structure, and geometric SdS selection.
- A derivation can therefore live only in a mechanism that sees Gρ_Λ separately from H, that is, one that couples the a₀ sector's energy density to gravity with a rational coefficient. That is the record's open target (the 4 in Gρ_Λ = 4a₀²).

## Own errors, fixed openly before the final run (none changes a verdict)
- **G9 (sympy branch):** sympy cannot reduce √(H²/(1−x²)), so I compare squares plus spot values.
- **X1 tautologies:** two of my X1 checks could not fail, an `or True` and a hard-coded flag; both are now computed.
- **K1b:** the integral at y = 0 stayed unevaluated; I take the limit instead.
- **K2d integration range:** it stopped at x = 120 and missed a tail of about 0.12; it now runs to x = 3000.
- **K4 tolerance:** 1e-15 was below the quadrature accuracy.
- **K6 units:** I compared Δμ with lane K's dex number; the check now converts to dex.
- **K7 Polonyi parameter:** my first β was on the anti-de Sitter side.
- **K9 discretisation:** the cumsum started at μ(0) > 0.
- **N4b:** sympy needed an explicit factor.
- **P5c profile:** the first parameters forced m₀ < 0.
- **S1:** my extraction squared H² twice.
- **Compare regexes:** two matched the wrong lines.

## Not established
- That no door exists anywhere: only these 8 no-gos were audited, against the frozen door rule.
- The literature reading in E: I re-derived the formulas, not the papers.
- K's SPARC fits (k02): not re-run.
- sol61's static law (G_N, a₀_N) and the BBN source transfer: taken as its premises.
- Lindemann's theorem: imported; the integer-relation searches are illustrations only.
- X1's Myers-Perry side result: not audited.

## Files
- `CFG263_FROZEN_CRITERIA.md` and `.sha256` (written first)
- `cfg263_lib.py` (check registry, frozen classifier, door rule)
- `cfg263_01_G_symmetry`, `02_E_literature`, `03_X1_generator_noether`, `04_K_density_linear`, `05_L_sds`, `06_N_jacobson`, `07_P12_B3_horizon`, `08_S61_clock_bbn`: independent re-derivations (`.py` and `.out`)
- `cfg263_09_mutate` (MUTATE; mutant copies in `mutants/`)
- `cfg263_10_compare_originals` (read-only comparison)
- `cfg263_11_classify` (frozen classifier and door rule)
- `results.json`, `run_all.sh`

Nothing outside this directory was written. Nothing was committed or pushed.
