# X22_cosmic_dust_window — FROZEN CRITERIA (committed with ASSUMPTION_LEDGER.md, alone, before any script or number)

**Question.** Is there any window, in scale, time or environment, where a cold component clusters enough for the
Lyman-α forest (z ≈ 2–3) and σ₈, yet is absent from isolated galaxies today?

Settings. κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt a₀ = 1.1312e-10 m/s², reported separately, never
pooled. a₀ is absent at linear order on FRW (Q6 D0, X4), so the forest and σ₈ side is footing-independent; the galaxy
side is computed per footing. The cold component is gravitating field mass ("cold energy"), never a particle. No knob
is fitted: every family index (cut strength α, time power p, key threshold) is graded over a frozen grid or bounded by
a line, never adopted. Not "theory closed". Nothing here says the data favour the framework.

Constants (record, CFG946 via X6): H₀ = 67.4 km/s/Mpc (h = 0.674), Ω_b = 0.0493, Ω_c/Ω_b = 5.364, Ω_m = 6.364 Ω_b,
δ_ta = 5.55, r_ta(M_b) = [3(Ω_m/Ω_b) M_b / (4π δ_ta ρ̄_m)]^{1/3}. ρ̄_m (comoving) = Ω_m ρ_crit,0.

## 0. Step 0 — stop rule (all must PASS, or the lane stops with UNDECIDED and no Step 1–3 numbers are graded)

| id | reproduction | line |
|---|---|---|
| S0-1 | L346 bins (6, 1.10–3.56 h/Mpc) and the sw5_canon / sw5_alt / never_on bands at z = 3 and 2, read from `real_research/g03_audit_2026/L346_switch_forest_gate_results.json` with X4's code, equal X4's `F0a` (`x4_dbi_door_results.json`) | ≤ 1e-9 |
| S0-2 | L319's line T²_5.3keV(k5) with L319's formula and cosmology (h 0.6736, ω_b 0.02237, ω_c 0.1200; k5 = L319 grid point nearest 5 = 4.6199 h/Mpc) equals X4 `F0b.T2_5.3keV` | ≤ 1e-12, and within 5e-4 of 0.995 |
| S0-3 | X6's SPARC machinery (copied verbatim: 175 `*_rotmod.dat`, Υ grid 0.30–1.20 step 0.01, CFG4 weights, algebraic ν₁) gives the law's rms and median Υ per footing equal to X6 `d.law_sparc` | rms ≤ 1e-9, same U median |
| S0-4 | X6's f_d,max(d2) (both footings, 20-step bisection) and NGC 3198's deviation at X6's f_c (`growth.f_c.cap_10.ai1e3`), both footings, equal X6 `d.f_d_max_d2` and `d.per_footing.<f>.f_c.ngc3198_dex` | ≤ 1e-9 |
| S0-5 | X19 `x19_classes.csv`: the cosmic-background ρ_b band ends equal Ω_b ρ_crit(1+z)³ (h 0.672, Ω_b 0.049) at z = 0 and 1100; SPARC small/large rows present on both footings | ≤ 1e-6 relative |

## 1. Step 1 — λ_forest (footing-independent)

**Cut family** (transcribed from L319, the record's WDM-calibrated line): T²(k) = [1 + (αk)^{2ν}]^{−10/ν}, ν = 1.12,
i.e. T(k) = [1 + (k/k_c)^n]^{−m} with n = 2ν = 2.24, m = 5/ν, k_c = 1/α. The cut is applied to the total matter
transfer at z = 3 and z = 2 (a frozen comoving cut is z-independent in this family).

**Forest class of a cut** (X4's F_p rule, verbatim lines):
- PASS iff T² ∈ [0.8, 1.2] at all six L346 bins (z = 3 and 2) **and** T²(k5) ≥ T²_5.3keV (S0-2).
- FAIL iff T²(k5) < 0.9 (L319 loose) **or** the worst L346 bin < 0.5.
- UNDECIDED otherwise.

**Outputs.** α_PASS = largest α with class PASS; α_NF = largest α not FAIL (window-favourable). For each: k_c⁻¹ = α
(Mpc/h), the half-mode k_hm (T = ½, i.e. T² = ¼), λ_hm = 2π/k_hm, Lagrangian radius R_hm = λ_hm/2 and mass
M_hm = (4π/3) ρ̄_m R_hm³. λ_line = 2π/k5 is the smallest comoving scale at which the line demands dust-like power.
**λ_forest** (verdict-bearing) = λ_hm at α_NF (the largest cut the forest does not exclude). Reported only: the
pincer's loose yardstick T²(10 h/Mpc) ≥ 0.5.

Check C1 (control): α → 0 gives PASS; L319's α at 1 keV gives FAIL; L319's α at 5.3 keV gives T²(k5) = S0-2's value.

## 2. Step 2 — the galaxy side (per footing, never pooled)

- **R_gal.** SPARC R_last (last measured radius) distribution: min / 16 / 50 / 84 / max, kpc.
- **f_max(footing).** The largest fraction f of the CFG946 D-F fair share (cold mass f × 5.364 M_b with M(<r) ∝ r to
  r_ta; X6's profile) such that X6's adapted d2 line passes **on that footing**: rms ≤ 0.110 dex and median Υ ∈
  [min(0.50, Υ_law), 0.80]. 20-step bisection on [0, 1]. Reported: the rms-only bound (rms ≤ 0.110 alone).
- **Tolerated cold mass.** M_c,max(<R_last)/M_b = f_max × 5.364 × min(R_last/r_ta, 1) per galaxy at the law's
  per-galaxy best Υ (distribution reported).
- **Lagrangian scale per galaxy.** M_L = (Ω_m/Ω_b) M_b(Υ_law), R_L = [3 M_L/(4π ρ̄_m)]^{1/3} (comoving), k_L = π/R_L
  (the same convention as M_hm, so M_L ≤ M_hm ⟺ k_L ≥ k_hm).
- **Hydrostatic content (for time-dependent and keyed pressure).** A cold component with sound speed c_s in a galaxy's
  flat well (V_i = V_obs at R_last), isothermal and normalised to the cosmic mean ρ̄_c at r_ta (window-favourable: the
  real r_ta region is overdense): M_c(<r) = (5.364 M_b/δ_ta) · 3/(3 − β_i) · (r/r_ta)^{3−β_i} for r ≤ r_ta, with
  β_i = V_i²/c_s², β capped at 2.9 (count reported). **c_s,need(footing)** = the smallest c_s (bisection in log c_s on
  [1, 3000] km/s, 30 steps) for which X6's d2 line passes on that footing with this profile in place of X6's.
  Reported: the content at β = 2 (c_s = V/√2, gravitational virial heating), as a fraction of the fair share inside
  R_last.

Check C4: the closed-form M_c(<r) equals a numerical quadrature of 4πr²ρ to ≤ 1e-8 (three β values).
Check C5: the per-galaxy-vector form of X6's d2 statistic with fd_i ≡ f equals X6's scalar form at f = f_max and 1
(exact).

## 3. Step 3 — compare

**3A. Frozen comoving cut, gravity only.** At α_NF (and α_PASS, reported), the captured fraction per galaxy is taken
as c_i = T²(k_L,i) (window-favourable: the linear amplitude T is larger, and nonlinear refill of halos above M_hm only
adds). X6's d2 line is evaluated with per-galaxy fd_i = c_i on each footing. Reported: k_excl and M_excl where
T² = f_max at α_NF; the gap M_L(SPARC p16, p50)/M_excl; the fraction of SPARC galaxies with M_L < M_excl; the infall
content of a suppressed galaxy from the smallest unsuppressed scale (reported only).
**Window-A** iff the d2 line passes on both footings at α_NF.

**3B. Time-dependent Jeans cut, λ_J,com ∝ a^p ⟺ c_s(a) = c_s,need · a^{p − 1/2}.** Frozen grid
p ∈ {−0.5, 0, 0.5, 1, 1.5, 2, 3, 4, 6, 8}. Linear two-fluid ODE in ln a on flat ΛCDM (Ω_m above, no radiation),
a_i = 1e-3, growing-mode start (δ = δ′ = a_i for both fluids), baryons pressureless, cold term
−(c_s k/(aH))² δ_c; T²(k, z) = (δ_m/δ_m,c_s=0)², δ_m = (5.364 δ_c + δ_b)/6.364.
- Forest class from T² at z = 3 and 2 (rule §1).
- σ₈ ratio R = [∫Δ²(k) W₈² T²(k, 0) dlnk / ∫Δ² W₈² dlnk]^{1/2} with the record's BBKS + Sugiyama shape
  (`prep_2026/mi_linear_cosmology/mi_growth.py`, its constants verbatim), k ∈ [1e-3, 30] h/Mpc. Line R ≥ 0.95.
- **Window-B(p)** iff forest not FAIL and R ≥ 0.95 on both footings (the galaxy line holds at c_s,need by construction).
- Classification: p ≤ 0.5 (c_s non-increasing in time; an equation of state alone) is gravitational/EOS; p > 0.5
  needs c_s to rise after the forest epoch, i.e. energy injected into the cold component (non-gravitational heating).

Check C2: with c_s ≡ 0, T² ≡ 1 to 1e-10 and δ_m(a=1)/a_i equals the ΛCDM growth integral D ∝ H∫da/(aH)³ (normalised
in the matter era at a_i) to ≤ 2e-3. Check C3: at every graded k, T²(z = 0) is non-increasing in c_s over
{0, 10, 100, 300} km/s (p = 0.5).
Reported only: the pincer's constant-c_s control (4 km/s) at k = 10, z = 3.

**3C. Environment keys.** Keys = X19's variables placeable on FRW (ρ_b, x, ρ_env, e, kT, N_orb, H) plus one derived key,
the baryon overdensity δ_b = ρ_b/ρ̄_b(z) (same numbers, divided by the epoch's mean).
- Cosmic set C (where the cold component must cluster like dust): X19's background band over z ∈ [0, 1100] ∪ forest
  absorbers at z ∈ [2, 3] with δ_b ∈ [0.1, 10] (PROVISIONAL; loose bound δ_b ≤ 100). For δ_b the background is δ_b = 0
  (linear |δ_b| ≪ 1).
- Galaxy set S: SPARC small ∪ large, X19 16–84 % intervals (lo = min p16, hi = max p84), each footing; strict min–max
  over SPARC galaxies reported where computable.
- A key **separates** iff C and S are disjoint (in log₁₀ V; binary as 0/1) on both footings. If the background band
  overlaps S, report z_match where the background enters S (ρ_b: (ρ_S,lo/ρ̄_b,0)^{1/3} − 1) and grade the consequence
  for ρ_b: the ODE of 3B with c_s = c_s,need switched on for z ≥ z_match (sharp key) → forest class and R.
- Keys whose separation exists only by catalogue convention (a value set to 0 for "none", not measured: kT, and e or
  N_orb for the background) are flagged CONVENTION; a CONVENTION separation carries no window weight unless a physical
  value of the key for the cosmic medium is computed. Reported only: the record-method rms linear peculiar gravity
  g_rms(z) (mi_growth's `grms` construction, BBKS σ₈ = 0.811) at z = 0, 2, 3, against SPARC's e·a₀.
- For a separating key: the side effects on X19's other classes (which EXTRA classes it would also empty, which NONE
  classes it leaves) are reported only, and the record is searched for an action (X6 class, X19 step 2, CFG944
  Theorem G).

## 4. Verdict rule (frozen)

1. Any S0 FAIL, or any required check (C1–C5) FAIL → **UNDECIDED**.
2. Window-A, or Window-B(p) at some p ≤ 0.5 → **WINDOW EXISTS** (state the scale and the strength).
3. Else, Window-B(p) at some p > 0.5, or a physical (non-CONVENTION) key separating C from S on both footings →
   **WINDOW ONLY WITH A NON-GRAVITATIONAL EXCLUSION** (state the kind, the strength c_s,need, and whether the record has
   an action for it).
4. Else → **NO WINDOW: the forest scale is smaller than the galaxy exclusion scale, so any cold component that passes
   the forest falls into galaxies.**

The NO-WINDOW statement for gravity alone (3A and 3B at p ≤ 0.5) is reported as its own line whatever the overall class.

## 5. MUTATE twin (`X22_MUTATE=1`; outputs `*_MUTATE.*`; the run must exit 1)

Mutations: (m1) L346 read from sw5_alt in place of sw5_canon in S0-1's comparison; (m2) L319 exponent −10/ν → −5/ν;
(m3) SPARC Υ grid × 1.1; (m4) X6 f_max bisection on the rms-only line; (m5) X19 h = 0.70; (m6) ODE source
1.5 Ω_m(a) → 1.4 Ω_m(a); (m7) hydrostatic exponent 3 − β → 2 − β.
**Named checks that must FAIL:** S0-1, S0-2, S0-3, S0-4, S0-5, C2, C4. C1, C3 and C5 may pass. The MUTATE verdict line
is the control's output, not physics.

## 6. Compute

One thread, `nice -n 15`, `PYTHONHASHSEED=0`, < 1 GB RSS, minutes. No CLASS run, no N-body, no download, no
`compute_queue/`. Every README number comes from the committed `.out` / `_results.json`.
