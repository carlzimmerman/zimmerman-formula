# S2_v3_lowg_lensing: FROZEN CRITERIA (committed with the ledger, before any script or number of this lane)

Batch R2 of `rebuild_2026_10_22/N0_board_audit/AUDIT.md` (tiles 17 "Isolated-galaxy lensing, inner" and 30 "Red (early-type)
lenses"; feeds tile 31). Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`, `BRIEF_E_AUDIT.md`.
κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11, alt 1.1312e-10 m/s², scored separately, never pooled. No dark-matter
particle. Never "theory closed". Never "the data favour the framework". Ledger: `ASSUMPTION_LEDGER.md` (same commit).

**Not blind.** Before freezing I read CFG829, CFG840, CFG885, CFG926 (R5/R6) and F2 (README, JSON). Known numbers:
CFG829 window A (data / algebraic law, ν_e) blue 1.016 ± 0.086, red 1.587 ± 0.076, all 1.439 ± 0.050 (canonical);
CFG926 window A_red 1.451 (+0.123 dex) → 1.208 (+0.123 + IMF); F2 ESD-space A_in (all lenses, R ≤ 0.31 Mpc) 1.13 at
y_e = 0 / 1.14 at the primary y_e. Expectation formed: the hot CGM lowers A, the external field (EFE) raises it, and the
EFE matters inside CFG829's window because r_e = r_M/x_e ≈ 35 r_M at the primary field while the window spans 9–43 r_M.

## 0. The tiles being recomputed

- **Tile 17 (PASS today):** "supply suffices ≤ 0.31 Mpc; blue lenses A 1.016" (CFG804/829/840/902). The supply rule is not in
  v3; CFG829's A used the isolated, EFE-free algebraic law.
- **Tile 30 (COND today):** "an IMF α–σ relation removes it, if discs stay near Chabrier" (CFG926 R5 on top of CFG667's
  +0.123 dex). It used the EFE-free law.

## 1. The v3 model (THEORY_V3_DRAFT §1–3; F2's T, reused read-only)

- Field equation: AQUAL ∇·[μ(|∇Φ|/a₀)∇Φ] = 4πGρ_b, μ = x/(1+x); lensing sees Φ (C4). External field: uniform Newtonian
  y_e, solved with F2's own axisymmetric AQUAL solver (`../F2_outer_lensing/f2_aqual.py`, imported read-only); lensing mass
  M_eff(<r) orientation-averaged; extended baryons = isolated AQUAL (exact, spherical) × the point-mass EFE ratio C(r; y_e),
  exactly as F2 §2.
- y_e (units of the footing's a₀): 0; **primary** = Chae+21 "noclu" median 10^−3.215 × 1.2e-10/a₀; upper = "maxclu" median
  10^−2.30 × 1.2e-10/a₀ (F2's values; must equal F2's committed JSON).
- Baryons per lens (F2's inventory, ledger B1–B3): stars M★ (record lens catalogue `lr_lenses.npz`, LePhare MASS_MED + 0.15,
  h70 → native), cold gas log f_cold = −0.69 log M★ + 6.63, hot CGM f_hot M★ as a uniform sphere of 100 kpc, central
  f_hot = 0.5.
- Screening: L★ = 24 and 90 pc. Galaxies are unscreened at lensing radii (l_g = L★²/(2 r_M), M2's definition, is sub-pc);
  the script computes max l_g / R_min over the stack and the v3 rows are identical with and without screening (stated, by
  construction; reported).
- μ_K²ψ term (BS24 Eq. 35): **not included** here. N0 assigns it to batch R6 (it acts beyond ~0.1 Mpc for μ_K ≤ 14.8
  h/Mpc). Every verdict below carries the caveat "before R6".
- No supply, settling, catchment, ownership or round rule. No dust (cold-energy) profile: v3 predicts none for a galaxy (F2).
- Native background: h = 0.679 (ends 0.672 / 0.686), Ω_m = 0.3085. Data g_obs × (h/0.70) × T_Ωm per file, T_Ωm from
  CFG885's committed JSON (fiducial 0.2793 entry); covariance × the square. g_bar labels are distance-independent (CFG885).

## 2. Data and statistic (CFG829's, forward-modelled)

- B21 RAR files (`real_research/data/lensing_rar/brouwer2021_rar/`): **blue** Fig-8 Colorbin_1, **red** Colorbin_2 (colour
  covmatrix, per-bin diagonal block as CFG829), **all** Fig-4-5-C1 isolated. g_obs = 4G·ESD_t/bias (B21 Eq. 7, CFG829's
  constants), covariance / bias as the README says.
- **Window W = [10^−13.3, 10^−11.9) m/s² on B21's g_bar labels** (CFG829): a fixed set of data points for every ladder step.
- **Model (forward):** for each record lens i of the class and each B21 bin k, R_ik = √(G Mgal_i / g_bar,k) (h70, Mgal = the
  record's B21-style M★(1 + f_cold)), converted to native with (0.70/h) and the Ω_m D_A ratio (F2's convention). The model
  ESD of lens i at R_ik is v3's ΔΣ of that lens's inventory; the class model is the mean over lenses weighted by each lens's
  Σ_crit⁻²-weighted source weight in bin k (`cfg110_perlens.npz` WW, as F2), and g_model = 4G·ΔΣ_model (same constants as
  the data, so the estimator's 4GΔΣ conversion is applied identically to data and model).
- **Lens classes** (record lenses): primary = the record's `typ` (u−r > 2.0 in LePhare MAG_ABS, the record's colour valley,
  `lr_esd_remeasure.py` L87); variant (reported) = u−r 2.5 reconstructed from the LePhare file. "All" = every lens.
- **A** = GLS amplitude of data over model in W with the full window covariance: A = (mᵀC⁻¹d)/(mᵀC⁻¹m), σ_A = (mᵀC⁻¹m)^−½
  (CFG829's estimator). Also reported: A in CFG829's calibration window [10^−11.9, 10^−10.9), χ² over all 15 points, the
  lens-weighted median R of each window point (native kpc), and the red − blue split z = (A_red − A_blue)/√(σ_r² + σ_b²).
- Amplitude classes (F2 §3): **consistent** |A − 1| ≤ 2σ_A; **short** A − 1 > 3σ_A (v3 under-predicts); **over**
  1 − A > 3σ_A; otherwise **between**.

## 3. Ladder (one ingredient at a time; A for blue, red, all; both footings)

L0 CFG829 as recorded (algebraic ν_e, B21 distances) — must reproduce (K0). L1 kernel ν_e → ν₁ = v3's μ = x/(1+x) (algebraic).
L2 native h, Ω_m on the data. L3 forward 4GΔΣ model of the isolated AQUAL profile (spherical AQUAL = algebraic law), B21's
own baryons (stars + cold gas). L4 + hot CGM (f_hot 0.5) = **v3 at y_e = 0**. L5 + EFE at the primary y_e = **T_central**.
L6 screening L★ 24 / 90 pc (identical by construction; reported). Then one at a time from T_central: y_e 0 / maxclu;
f_hot 0 / 1.0; f_cold ± 0.2 dex; M★ ± 0.2 dex (E1); h 0.672 / 0.686; Σ_crit ± 3 % (source photo-z); window −0.3 / +0.3 dex
(CFG840 V1); colour split 2.5 (variant). Reported only: y_e scan 1e-6, 1e-5, 3e-5, 1e-4, 3e-4 (largest y_e keeping blue
"consistent"); F2's ESD-space A_in (all lenses, R ≤ 0.31 Mpc, read from F2's committed JSON, not recomputed).

**Red-lens readings (tile 30).** R0 inventory (Chabrier LePhare + 0.15). R1 = R0 + 0.123 dex on red-lens stars (CFG667
Taylor − LePhare). R2 = R1 + Δ_IMF on red-lens stars, Δ_IMF = CFG926 R5's committed D_red = 0.17216 (read from
`cfg926_results.json`; zero free constants, fitted on ATLAS3D, never on lensing). Blue lenses stay at R0 (CFG926's declared
asymmetry). Shifts act on stars only (cold and hot gas fixed). Reported only: R2 with CFG850's convention (window applied to
labels × 10^shift); R5-blue (Δ_IMF = D_blue 0.15886 on blue stars).

## 4. Verdict rules (per footing; T_central inputs; y_e ∈ {0, primary, maxclu})

Let S be the set of (reading, y_e) cells whose A is **consistent**.

**Tile 17 (blue lenses; reading R0 only):**
1. **PASS** if (R0, 0) and (R0, primary) are both in S.
2. **FAIL** if A is **short** at y_e = 0 (then, by K6, at every y_e ≥ 0), or **over** at y_e = maxclu (then at every y_e
   ≤ maxclu).
3. **CONDITIONAL** if neither, and S is not empty; the condition (the y_e cells that pass) is stated.
4. **NOT DECIDABLE** otherwise.

**Tile 30 (red lenses; readings R0, R1, R2):**
1. **PASS** if (R0, 0) and (R0, primary) are both in S.
2. **CONDITIONAL** if not PASS and S is not empty; the condition names the reading(s) and y_e cells that pass. "The old COND
   survives" iff (R2, 0) and (R2, primary) are both in S.
3. **FAIL** if S is empty and, for every reading, A is **short** at y_e = 0 or **over** at y_e = maxclu.
4. **NOT DECIDABLE** otherwise.

**Robustness tag** (does not change the verdict): ROBUST if the cells that decide the verdict keep their class under every
one-at-a-time bracket (f_hot 0/1, f_cold ±0.2, M★ ±0.2, h ends, Σ_crit ±3 %, window ±0.3 dex); else FRAGILE, naming the
brackets.

**Footings.** Each footing gets its own verdict. The board verdict is the less favourable of the two in the order
PASS > CONDITIONAL > NOT DECIDABLE > FAIL, with the split stated. "All" lenses are reported with their classes (feeds tile 31),
not graded. Every verdict is "before R6 (μ_K² term)".

A cure must be a named ingredient (AQUAL, EFE, screening, native H₀, E1 masses, the declared CFG667/CFG926 posits for red
lenses) — no fitted amplitude, bias, profile or y_e enters any verdict line.

## 5. Checks (script `s2_v3_lowg_lensing.py`; one line per check; exit 0 iff all pass)

- **K0a** own re-implementation of CFG829 (load, window, GLS A, ν_e) reproduces `cfg829_results.json` window A and σ_A for
  blue / red / all on both footings to ≤ 5e-4. If K0a fails the lane stops.
- **K0b** CFG850/926 algebraic shifted-g_bar path reproduces CFG926 `window850` A_red (before / after / IMF_alone) on both
  footings to ≤ 1e-6.
- **K1** F2 solver: y_e = 1e-6 reproduces the isolated M_eff to ≤ 1e-3 at r ≤ 10 r_M; far field (r ≥ 10 r_e) within 2 % of
  the linearised angle-averaged mass; the y_e values equal F2's committed JSON to 1e-12.
- **K2** forward model, point mass, isolated: 4GΔΣ at fixed g_bar is mass-independent across the M★ table (max spread ≤ 1e-3),
  and it equals an independent line-of-sight quadrature of the isolated AQUAL point-mass profile (point mass + CFG804's
  ρ_law(s) = 1/(2πs√(1+4s²))) at the window g_bar to ≤ 2e-3.
- **K3** projection: ΔΣ of a point mass and of an SIS against analytic forms (≤ 1e-3).
- **K4** the record's per-lens weights summed per (patch, typ) reproduce `cfg96_stack.npz` W_10 to 1e-10.
- **K5** colour sanity (information on calibration): the record's per-lens re-measured stack split by class vs B21 Fig-8
  colour bins, median ratio over S/N > 3 points within [0.8, 1.25] for both classes; the u−r 2.5 reconstruction matches the
  record's lenses exactly (self-match ≤ 1e-9 rad, log M★ equal, (u−r > 2.0) ≡ `typ`).
- **K6** EFE monotonicity: A(y_e = 0) ≤ A(primary) ≤ A(maxclu) for every class, reading and footing.
- **K7** T_Ωm for the all-isolated file equals F2's 1.0128 to 5e-4.
- **MUTATE** (`--mutate`): every B21 g_obs × 1.10 before K0a → K0a FAILS, exit 1, outputs `*_MUTATE.*`.

Compute: `OMP_NUM_THREADS=1 nice -n 15`, one thread, < 1 GB RSS, minutes. No downloads. No PM simulation. Do not redo P2's
spectroscopic outer test (read its outputs if committed).
