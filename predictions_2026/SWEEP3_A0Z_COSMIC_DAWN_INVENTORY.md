# Predictions audit — inventory sweep 3/4: a₀(z) and cosmic dawn

**Scope.** Every prediction, registered number and falsification statement in: `nbody_2026/stage17`
(derived a₀(z) law), `stage19` (CLASS re-run), `stage21` (MUSE / MSA-3D re-exam), `stage23` (S8 null),
`stage24` (cosmic-dawn linear-growth theorem), `stage25` (early-rotator BTFR, Σ†), `stage26` (collapse
timing), the Lyman-α forest (`nbody_2026/stage14-16`, `real_research/reviews/mi_forest_*`), DESI w(z)
dissolution-to-constant, and the SN-Ia host step at a₀ (`real_research/snia_*`, `reviews/mi_snia_power_curve_2026.py`).

**This is an inventory, not a verdict pass.** Correctness labels (CORRECT / STALE / WRONG / SUPERSEDED /
DEAD) are applied only where the corpus itself has already retired the item; everything else is
listed with the status the source file gives it. Evaluation is the next workflow step.

**Re-derivation.** All seven stage scripts were re-run for this sweep (exit 0, checks 17/17, 8/8, 7/7,
5/5, 8/8, 4/4 for stages 17/19/21/23/25/26; stage 24 not re-run — its E-part number was superseded by
stage 25 and its D2 number by stage 26). `mi_snia_power_curve_2026.py` re-run (exit 0). The closed-form
numbers are re-derived on BOTH footings by `predictions_2026/sweep3_a0z_cosmic_dawn_numbers_2026.py`
(21/21 checks; output `sweep3_numbers.json`).

**Footings.** Canonical a₀ = ½c√(Gρ_Λ) = 9.362e-11 m/s² (ρ_DE / cH_Λ); alt = 1.128e-10 (ρ_total / cH₀);
alt/canonical = Ω_Λ^(−1/2) = 1.2083. The derived a₀(z)/a₀(0) ratio is footing-INDEPENDENT (the anchor
cancels); only dimensionful numbers (Σ†, Σ_M, the absolute BTFR zero point, collapse speedup via
y = g_N/a₀) move, and both values are given.

---

## A. The derived a₀(z) law (stage 17) — the object every other item hangs on

| id | statement | equation | registered number | footing | data / date | status |
|---|---|---|---|---|---|---|
| S3-01 | a₀ tracks the dark sector's PRESSURE: a₀²(Q) = κ²c²G·(−K(Q)); today −K = M⁴ = ρ_Λ | closed form a₀²(z)/a₀²(0) = [1−β(1−(1+ν²)^−½)]/[1−β(1−(1+ν₀²)^−½)], ν = ν₀(1+z)³ | at β=1: a₀(z)/a₀(0) = [√(1+ν₀²)/√(1+ν₀²(1+z)⁶)]^½ | ratio footing-independent; anchor 9.362e-11 / 1.128e-10 | none directly; it is the law | LIVE — but a **PROMOTION / target relation, not derived from the action** (HANDOFF §1; memory 2026-08-28). Never quote as "derived from the action" unqualified |
| S3-02 | β = 1 ("the Lagrangian vanishes at the DBI wall", μ²Λ_D² = M⁴) | off-switch needs 1−β ≤ (0.006)² = 3.6e-5 | β = 1 to 3.6e-5 | — | CMB (Planck) | SELECTED, NOT DERIVED (stage 17 C2, stated in-file) |
| S3-03 | ν₀ window | floor from a₀(1090)/a₀(0) ≤ 0.006; ceiling from RAR via drain bound (ν_loc ≤ 0.141) | ν₀ ∈ [2.14e-5, 1.77e-4], factor 8.26 | — | CMB + SPARC RAR | LIVE; ceiling rests on stage-2/3 drain arithmetic (t_ff/t_H at 15 kpc × overdensity 1.5e5) |
| S3-04 | transition redshift | z_t = ν₀^(−1/3) − 1 | z_t ∈ [16.8, 35.0] | — | 21-cm / cosmic-dawn window in principle; stage 24 E4: **no linear 21-cm signature** | LIVE (registered); no 21-cm prediction attaches |
| S3-05 | a₀ constant at low z | same law | a₀(z)/a₀(0) − 1 < 1e-4 at z=3, < 1e-3 at z=5 (ceiling); z=0.5,1,2 → 1.0000 | — | every z<5 a₀ probe | LIVE — **the sharp null** (see S3-20) |
| S3-06 | MOND off at recombination | same law at z_* = 1089.9 | a₀(z_*)/a₀(0) = 0.0060 (floor) – 0.00209 (ceiling) | — | CMB (stage 19) | LIVE; the retired CPL law also gave 0.0060 (Gemini-verified 0.00603) |
| S3-07 | footing fork decided at action level: pressure scalar DECLINES into the past = canonical; alt (cH·E(z), rising) "corresponds to no scalar" | stage 17 F1 | — | canonical selected | — | INFO-level claim, inherits S3-01's promotion caveat |
| S3-08 | health: c_T = 1 survives; no-ghost theorem does NOT automatically survive F_YQ ≠ 0 mixing | stage 17 F2 | — | — | — | OWED (perturbation matrix redo; stage 18 later addressed on FRW only) |
| S3-09 | drain result load-bearing: without the drain ν_loc = 3.21 at g = a₀ radius ⇒ local a₀ = 0.545 nominal, RAR-fatal | stage 17 D3 | 0.545 | — | RAR 0.108 dex | LIVE (internal consistency) |
| S3-10 | cluster R500 local shift negligible | ν_loc ≤ 0.0102 ⇒ Δa₀ ≤ 0.0026 % | — | — | X-COP | INFO |

### Retired predecessor law (DEAD — carry only as a label)

| id | statement | equation | number | status |
|---|---|---|---|---|
| S3-R1 | CPL-dressed law a₀(z)/a₀(0) = (1+z)^{1.5(1+w₀+wₐ)} exp(−1.5wₐz/(1+z)), DESI DR2 (w₀,wₐ)=(−0.75,−0.86) | ρ_DE(z) footing | bump +6.1 % at z=0.5 (+6.26 % at z=0.405); 1.011 at z=1; 0.865 at z=2; **0.740 at z=3**; 0.36 at z=10; 0.006 at z=1090 | **DEAD** (stage 17 E1: "never self-consistent with the sector's own w=−1"; REPLACED not refined). Do NOT cite "a₀(3)=0.74 ELT target" (stage 21 D2) |
| S3-R2 | fit-specific spread of R1: bump +2.4 % (Pantheon+) … +17.8 % (DESI+CMB-only); a₀(3)/a₀(0) 0.706–0.775 | memory 2026-06-21/07-07 | — | DEAD with R1 |
| S3-R3 | "z≳3 BTFR-offset −0.033 dex at z=3 (Branch A declining)" | v ∝ a₀^{1/4} on R1 | −0.033 dex | DEAD with R1 (replaced by S3-30) |
| S3-R4 | "DESI DR3 is the gate for a₀(z)" / "w→−1 dissolves the framework" as a RISK | memory 2026-06-21 | — | **SUPERSEDED** — stage 21 E2: dissolution to constant is now the PREDICTION; DR3 gates only the separate w=−1-exact-vs-evolving-DE tension |
| S3-R5 | "3.1–4.2σ DESI cosmology-leg tailwind" | — | — | **FORFEITED** (stage 21 E2), not citable as support |
| S3-R6 | "declining a₀ is favourable/neutral for JWST" (Nusser-2002 read) | — | — | WITHDRAWN for the derived law (stage 21 E3); then re-scoped by stages 24/26 |

---

## B. CMB / background (stage 19)

| id | statement | equation | number | footing | data | status |
|---|---|---|---|---|---|---|
| S3-11 | exact background of the non-dust piece | ρ_nd = M⁴√(1+ν²), p_nd = −M⁴/√(1+ν²), w_nd = −1/(1+ν²) | ρ_nd·p_nd = −M⁸ invariant | footing-independent (ν₀ only dial) | — | LIVE (sympy) |
| S3-12 | DE indistinguishable from Λ where measured | \|1+w\| = 2.3e-5 at z=2 (ceiling) vs survey ~0.03 | 2.3e-5 | — | DESI/SN w(z) | LIVE |
| S3-13 | expansion-history deviation | max \|δH/H\| = 1.87e-4 (ceiling), asymptote Ω_Λν₀/(2Ω_m) = 1.94e-4; 8.3× smaller at floor | — | — | BAO | LIVE |
| S3-14 | acoustic geometry untouched | δθ_*/θ_* = 5.3e-5 exact / 5.63e-5 CLASS (ceiling); 8.2e-6 floor; Planck precision 2.9e-4 | 0.18× / 0.028× Planck | — | Planck | LIVE |
| S3-15 | real CLASS bracket (trace as cold matter, δω_cdm = 5.51e-5 = 0.046 %) | per-multipole and χ² vs cosmic variance | max \|ΔC_ℓ/C_ℓ\| 0.114 % TT / 0.171 % EE; **Δχ² = 1.343 over 4998 TT+EE multipoles** vs √(2N) ≈ 100 | — | Planck (ideal CV yardstick) | LIVE; SAME rigour as committed CMB pass, not full Einstein-Boltzmann AeST (stage 19 E1) |
| S3-16 | GDM degeneracy in action: the trace is a 0.046σ shift of ω_cdm | δω/0.0012 | 0.046σ | — | Planck | LIVE |

---

## C. Direct a₀(z) data (stage 21) — re-graded on the derived law

| id | statement | equation | number | footing | data | status |
|---|---|---|---|---|---|---|
| S3-17 | derived law = the flat branch on the MUSE window (0.5<z<1.44): predicted slope a₁ = −1.7e-6 (×1e-10/z) | slope of S3-01 | raw tension vs Ciocan a₁ = 1.59±0.105: **15.1σ** (was 16.3σ wrong-sign on R1) | ratio footing-indep. | Ciocan MUSE-DARK III, A&A 709 L16 (2026), arXiv:2604.22613 — published | LIVE tension, now SHARED with all constant-a₀ MOND, no longer framework-distinctive |
| S3-18 | drift-folded residual after Magneticum ΛCDM-assembly drift (Mayer+2023, +0.80/z) | (1.59−0.80)/√(0.105²+(f·0.80)²) | 1.91σ (f=0.5) – 3.02σ (f=0.3); banked stricter folding ~3–5σ | — | same | LIVE — do NOT quote raw 15σ without drift, do NOT quote ~0σ |
| S3-19 | joint fork likelihood relabels: framework branch M-DEC → M-FLAT; M-FLAT needs drift p = 1.22 (= MSA-3D's own measured apparent component) vs M-DEC 1.22–1.43; M-FLAT beat M-DEC 59.5:1 at that prior | `prep_2026/a0z_crossscale/a0z_fork_likelihood_2026.py` | 59.5:1 | — | 11 constraints | RE-ATTRIBUTED (committed numbers unchanged) |
| S3-20 | **THE SHARP NULL**: zero a₀ evolution below z~5 at <1 %; any robust nonzero evolution, EITHER SIGN, falsifies the derived law | S3-05 | a₀(3)/a₀(0) = 0.99997, a₀(5)/a₀(0) = 0.99963 (ceiling) | — | homogeneous-IFS drift-modelled a₀(z) pipeline (KROSS+KMOS3D+KGES+MUSE, ≤2 % velocity); z-binned weak-lensing RAR (KiDS/DES/HSC → LSST/Euclid) | LIVE; **falsification threshold: any a₀(z)/a₀(0) ≠ 1 at >1 % for z ≤ 5, once ΛCDM-assembly drift is forward-modelled** |
| S3-21 | MSA-3D genuine trend +0.91 [+0.05, +1.63] (raw +2.13 was selection-confounded) vs flat | 0.91/0.79 | **1.15σ** from flat ⇒ CONSISTENT (was WEAK-TENSION/WATCH) | — | MSA-3D (published) | RE-GRADED |
| S3-22 | Jeanneau+26 deep refit (N=61 lensed dwarfs, g_bar < 0.5a₀): Δb = +0.140 ± 0.276 dex vs derived 0.000 / ALT-rising −0.243 | BTFR zero point | 0.51σ from derived; ALT-side lean 1.0–1.4σ | canonical 0.000 vs alt −0.243 | VizieR J/A+A/709/A120 (in hand) | LIVE, underpowered (band 0.276 > separation 0.243; coherent gas-scaling systematic binds) |
| S3-23 | M-RISE (alt-footing rising law) fits the single Ciocan point best (p=0.197) but excluded by Milgrom 2017 (1+z)^1.5, 17× cluster offset with no z-trend (Tian+2024, eRASS1), disk BTFR null; since stage 17 corresponds to NO scalar in the action | — | — | alt | — | EXTERNAL hypothesis only |
| S3-24 | FORFEIT 1: bump defense gone (old +6.26 % at z=0.405; derived flat to 1e-5) — any robust low-z rise counts fully against | — | — | — | z~0.4 lensing-RAR bump surveys (needed ≲2 % at 0.3<z<0.6, ~2028+) | PRICED against interest |

---

## D. S8 (stage 23) and the linear-growth theorem (stage 24)

| id | statement | equation | number | footing | data | status |
|---|---|---|---|---|---|---|
| S3-25 | S8-relief idea via χ-sector Jeans cutoff λ_J = 2.2 Mpc comoving: **DEAD on scale** | k_J = 2π/λ_J = 4.24 h/Mpc; σ₈ top-hat W²(k_J R₈) = 4.46e-6 | computed σ₈ response 0.232 % (soft) / 0.001 % (step) vs 8.2 % needed ⇒ short **35×**; relief would need λ_J ≈ 15.4 Mpc (soft) / 32.4 Mpc (step), 7×/15× the pinned value | footing-indep. | KiDS-1000/DES-Y3 S8 0.766±0.020 vs Planck 0.834±0.016 | **DEAD** (reported as a dud in-file) |
| S3-26 | redshift trend adverse: comoving λ_J ∝ a² ⇒ 0.98 Mpc at z=0.5 (k_J = 9.5 h/Mpc) | — | — | — | — | INFO |
| S3-27 | S8 INHERITED UNCHANGED at linear order (δY⁽¹⁾ = 0 on FRW, stages 18/22); nonlinear sign ADVERSE (MOND collapse ⇒ higher effective S8), UNPRICED | theorem | — | — | S8 surveys | LIVE statement: **no S8 prediction either way**; nonlinear channel unpriced |
| S3-28 | linear-growth theorem: MOND sector contributes exactly zero to linear cosmological growth at every z, for any a₀(z); halo mass function is ΛCDM's | Y = 0 on FRW; δY⁽¹⁾ = 0; promoted term starts at third order | if it DID act: y = g_N/a₀ at the σ₈ scale today ~ deep MOND, ν ≈ 29 boost ⇒ "dark matter at full Ω_dm is STRUCTURALLY REQUIRED" | — | — | LIVE theorem (stages 18/22/24) — also the reason the JWST-abundance claim is NOT made (S3-R7) |
| S3-R7 | THE_COMPLETION §5 row "accelerated structure formation / earlier massive objects / JWST" read as an ABUNDANCE (linear-growth) claim | — | — | — | — | **WITHDRAWN as abundance** (stages 24/25); **RESTORED as collapse-TIMING** (stage 26, S3-33). Do NOT cite "JWST tailwind" as abundance |
| S3-R8 | stage 24 D2 "surviving nonlinear channel ≤ 1.5× (ratio derived/CPL boost at δ≈200)" | ν(y) at virial overdensity | ≤ 1.5× | — | — | **WRONG** (stage 26: evaluated the rate-limiting boost at its minimum; at turnaround ν = 2.3–5.1×, per-row 1.57–1.80× bigger than virial) |
| S3-R9 | stage 24 E2 "JWST compact objects sit 11× above Σ_M = a₀/(2πG) = 107 M⊙/pc²" | borrowed threshold | 11× | — | — | **WRONG number, right conclusion** (stage 25 C2: framework's own Σ† = a₀/(πG) = 213.7 ⇒ 5.5× above; still Newtonian) |
| S3-29 | 21-cm: z_t ∈ [17,35] sits in the EDGES window but there is NO linear signature | stage 24 E4 | — | — | 21-cm | NON-PREDICTION (must not be sold as one) |

---

## E. Cosmic dawn on the framework's own terms (stages 25, 26)

| id | statement | equation | number | footing | data / date | falsification / power | status |
|---|---|---|---|---|---|---|---|
| S3-30 | BTFR is a THEOREM of the a₀-line; early rotators at fixed M_b: v(z)/v(0) = [a₀(z)/a₀(0)]^{1/4} | g_obs² = g_bar² + a₀g_bar low-g limit ⇒ v⁴ = GM_b a₀; d ln v/d ln a₀ = ¼ | deficit (ceiling ν₀): 0.009 % z=5; **0.337 % z=10; 2.61 % z=15; 4.43 % z=17; 7.83 % z=20; 13.8 % z=25; 18.9 % z=30**; floor ν₀ flatter (0.24 % z=20, 2.1 % z=30) | ratio footing-indep.; absolute zero point alt/can = 1.0477 in v | ALMA [CII] / JWST z~4–7 now; z>12 kinematics do not exist (2030s ELT/HARMONI) | committed floor 0.06 dex ⇒ 3.51 % in v; **first detectable at z≈17 (ceiling)**; below z=5 any offset >0.1 % in v kills the law | LIVE pre-registered forecast. ⚠ the a₀-line is the α=1 identity (RETIRED as "exact"); the deep-MOND limit v⁴ = GM_b a₀ is kernel-independent so the ratio survives, but the "exact" framing in stage 25 A1/A2 is on the retired kernel |
| S3-31 | framework's own surface-density threshold Σ† = a₀/(πG) (2× the usual a₀/(2πG)) | g_bar = a₀ at Σ = M/(πr²) | **213.8 M⊙/pc² canonical / 258.3 alt**; Σ_M = a₀/(2πG) = 106.9 / 129.1 | both given | — | — | LIVE (derived from the α=1 a₀-line; under μ = 1−e^{−y} the g_bar = a₀ crossing is the same, so Σ† is kernel-robust as a threshold definition) |
| S3-32 | Σ†(z) = Σ†(0)·a₀(z)/a₀(0) ⇒ MOND regime SHRINKS toward high z | — | 154.2 at z=20, 92.3 at z=30 (canonical, ceiling) | ×1.208 alt | — | — | LIVE |
| S3-33 | **collapse-timing prediction (RESTORES §5 row)**: spherical shell r̈ = −√(g_N² + a₀(z)g_N) from turnaround (r_ta = 2r_200) collapses faster than Newtonian | energy integral, stage 26 B | speedup 1.34–1.96× (M=1e9–1e11, z=8–15); M=1e10: **2.03× z=6, 1.81× z=8, 1.66× z=10, 1.41× z=15, 1.24× z=20, 1.14× z=25**; formation (1+z) × speedup^{2/3}: z=10 → 14.4–16.2 | canonical; alt (larger a₀, smaller y): 2.12× z=6, 1.73× z=10, 1.46× z=15, 1.17× z=25 (+3–5 %) | JWST/ALMA high-z assembly (earlier, more mature galaxies at FIXED halo abundance) | signed shape: speedup DECLINES with z above z_t — no constant-a₀ MOND has this; falsified by no early-assembly excess OR by an excess that GROWS toward z>20 | LIVE, with the double-counting fork named: honest range ~1× (dust dominates, MOND screened) to 1.2–2.4× (stage 26 C3); boost at turnaround ν = 2.3–5.1× vs 1.5–2.8× virial |
| S3-34 | NOT predicted: ABUNDANCE of early objects (halo mass function ΛCDM-like by S3-28) | — | — | — | — | — | NON-CLAIM |
| S3-35 | observed JWST compact objects cannot test the cosmic-dawn a₀ (Newtonian, 5.5× above Σ†); test needs Σ < Σ† (LSB/diffuse) rotators at z>5 with resolved kinematics | — | — | — | none published | — | OBSERVATIONALLY INACCESSIBLE now ("weaker than safe") |

---

## F. Lyman-α forest

| id | statement | equation | number | footing | data | status |
|---|---|---|---|---|---|---|
| S3-36 | diffuse-baryon velocity amplification vs low-b cutoff (Hiss+2018 Table 4, 8 bins z=2.0–3.4) | kernel at OBSERVED x = √(y²+y): deep 1/h → 1/(2√y); conservative amplification 1.65× at x_rms = 0.0372 | best treatment (x_rms/CAMB): **1.1–9.0σ statistical / 0.4–0.9σ calibration** (3.36 km/s systematic); +conditioning 1.0–8.5 / 0.4–0.9; single-absorber 4.1–26 / 1.7–3.0 | canonical 4.1–24 stat / 1.7–3.0 cal; alt 4.5–26 / 1.9–3.0 (single-absorber) | Hiss+2018 (published); convention-owned ~32× | LIVE weak tension; **SIGN robust across every fork, EXCLUSION not**. DO-NOT-CITE "6–8σ" |
| S3-R10 | "6–8σ strongly disfavoured" forest exclusion; b_cut 15/17/22/24 km/s ±2.0 | — | — | — | — | **WRONG** (three defects: unsourceable data, invented error bar, kernel at Newtonian y not observed x — inflation 1.9–5.6×). Old "7–43σ", "8.7/6.6/3.2/1.7σ" also withdrawn |
| S3-37 | γ=0 χ-sector comoving cutoff evolves: L_J ∝ a³a₀(z)^{1/3} (MOND Jeans, NOT Newtonian); Murgia+18 shape-marginalised α < 0.03 h⁻¹Mpc passes at every z | stage 15 | worst bin z=2: α = 0.0200 (CPL law) → **0.0190 h⁻¹Mpc under the derived law**, margin 1.5× → 1.58× | footing-indep. | MIKE/HIRES 2018 (k_max 0.08 s/km); Iršič+24 to 0.2 s/km not re-derived | LIVE BOUNDARY; three named risks unretired |
| S3-38 | derived-law simplification: a₀(z)^{−1/3} Jeans factor → unity over the forest range (13–43 % CPL decline removed) | stage 17 E2 | — | — | — | LIVE |
| S3-39 | lognormal mock: predicted P_1D suppression below single-bin precision everywhere, worst-case sub-σ per bin, ~30-bin naive combination "nuisance-dominated rather than absent" | stage 16 | half-mode k ~ 35 h/Mpc, 3–9× beyond deepest data | — | XQ-100 / MIKE-HIRES / eBOSS | LIVE; stage 15's "released Hooper+22 likelihood" claim WITHDRAWN (no public release) |
| S3-40 | evolving comoving cutoff (shrinks with z) is qualitatively distinguishable from WDM's fixed cutoff using the forest's own z-bins | stage 14 pt 5 | factor cuts(z=2)/cuts(z=5) across the range | — | — | LIVE prediction in principle; no likelihood run |

---

## G. DESI w(z)

| id | statement | equation | number | data / date | status |
|---|---|---|---|---|---|
| S3-41 | **PREDICTION: dark energy dissolves to w = −1**; the sector's non-dust remainder has w_nd = −1/(1+ν²) ≥ −1 ALWAYS, so DESI's phantom past (w₀+wₐ = −1.61 < −1) is UNREACHABLE | stage 17 E4 / stage 19 A2 | w_nd runs −1.0 → −1e-4 across the transition (z_t 17–35); \|1+w\| ≤ 2.4e-5 for z ≤ 2 | DESI DR2 (2503.14738): 2.8σ (Pantheon+) / 3.1σ SN-free / 3.8σ (Union3) / 4.2σ (DESY5) evolving-DE; **DESI DR3 BAO ~2027**; DEBASS/LS4 SN recalibration | LIVE; **a confirmed DESI phantom-past detection is evidence AGAINST w = −1 exact** (against interest, stated in-file). w = −1 + O(ν₀²) — never say "w = −1 exact" unqualified |
| S3-42 | a₀(z) no longer inherits w(z) at all; DESI DR3 ceases to be the a₀(z) gate | stage 21 E2 | — | — | LIVE (supersedes S3-R4/R5) |
| S3-43 | Route B (dust → DE) sign test: can only produce the phantom side, w_eff(0) = −2.9…−1.8, 18–37σ from DESI w₀ | `nbody_2026/routeB_dust_to_dark_energy_2026.py` | — | DESI DR2 | DEAD route (already) |

---

## H. SN-Ia host step at a₀

| id | statement | equation | number | footing | data / date | power | status |
|---|---|---|---|---|---|---|---|
| S3-44 | the Pantheon+ host-mass step location coincides with hosts crossing g_bar = a₀ | Σ_a0 = a₀/(2πG); g_bar(M*) = GM*/R_e² with disk mass-size relation | Σ_a0 = **106.9 (canonical) / 129.1 (alt) M⊙/pc²**; crossing at log M* ≈ 9.6–10.2 vs empirical step at 10 | both | Pantheon+ (in hand) | — | LIVE coincidence (location only) |
| S3-45 | reproduced mass step (self-standardised, raw SALT2) | γ = −0.050 ± 0.007 mag | **6.9σ** | — | Pantheon+ | — | CORRECT data reproduction (not a framework result) |
| S3-46 | decisive separability: HR tracks acceleration at fixed mass? | partial corr(HR, log g/a₀ \| log M) vs partial(HR, log M \| g) | +0.0296 (accel, wrong sign, 0.63 SE from 0) vs −0.1704 (mass); local-SB version −0.036 vs −0.203; local-a₀ step −0.032±0.015 (2.1σ) vs mass 4.3σ | **statistic exactly footing-blind** (affine invariance) | SDSS DR17 × Pantheon+ N=449/450 | **18 % power** at the observed 0.06 mag; 80 % needs D = 0.142 mag (2.4×) or **N ≈ 2505** sized hosts (5.6× in hand); verdict gate with collinearity clause needs D = 0.217 mag | **UNDERPOWERED, NOT NULL** — "lever CLOSED" WITHDRAWN; DISFAVOURED not excluded; a₀ component ≤ 0.05/0.061 not excluded |
| S3-47 | a₀(z) under the SN progenitor-age-bias fight (Chung/Son vs Wiseman/Murakami): bump-then-decline "survives every (w₀,wₐ) fork" | `real_research/a0z_snia_systematics_forks.py` | — | — | — | **STALE** — computed on the RETIRED CPL law (S3-R1); under the derived law a₀(z) does not depend on (w₀,wₐ) at all |

---

## I. Cross-cutting falsification statements registered in this group

| id | statement | threshold | data release / date | status |
|---|---|---|---|---|
| S3-F1 | any robust a₀ evolution at z < 5, either sign, kills the derived law | \|a₀(z)/a₀(0) − 1\| > 1 % after drift forward-modelling | homogeneous IFS re-derivation (in-hand data); LSST/Euclid z-binned lensing RAR (late 2020s) | LIVE |
| S3-F2 | any BTFR zero-point offset below z = 5 larger than ~0.1 % in v (≈0.002 dex) | 0.1 % in v | requires systematics ≪ the current 0.06-dex floor; not testable at that level today | LIVE (registered; power ≈ 0 today) |
| S3-F3 | predicted BTFR velocity deficit above z ≈ 17 (ceiling) must appear as a specific declining curve | 3.51 % in v at z≈17 rising to 7.8 % at z=20 | 2030s ELT/HARMONI + JWST/ALMA; no z>12 kinematics exist | LIVE forecast |
| S3-F4 | earlier assembly at fixed halo abundance with a speedup that DECLINES toward z>20 | 1.1–2.0× collapse-time speedup, ~1× if dust screens | JWST/ALMA high-z maturity statistics | LIVE; fork (dust screening) unresolved |
| S3-F5 | DESI phantom past confirmed ⇒ evidence against w = −1 exact | \|1+w\| > 2.4e-5 at z ≤ 2 | DESI DR3 (~2027) | LIVE, against interest |
| S3-F6 | forest: evolving comoving cutoff vs WDM fixed cutoff | — | needs an unreleased generic likelihood | LIVE, unrun |
| S3-F7 | SN-Ia: N ≈ 2505 sized hosts at 80 % power | D = 0.142 mag | future SN samples (LSST/ZTF hosts with sizes) | LIVE, underpowered |

**Items in this group that later sweeps must not re-flag as live:** S3-R1…R10 (retired), S3-25 (S8 dead), S3-43 (Route B dead).
