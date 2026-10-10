# CFG595 FROZEN CRITERIA: the measured cold supply (replace the assumed (1 − f_b) M_ta with the cold mass that actually reaches each host in the framework's own PM)

Frozen 2026-10-10, committed alone, before any script of this lane is written or any number of this lane is computed.

Trigger: CFG594 (`HALO_ASSUMPTIONS_AUDIT.md`, item L05) ranks the SUPPLY as the #1 inherited driver of the growth excess:
every host is assumed to settle (1 − f_b) M_ta, the cold share of the ΛCDM turnaround ball (Δ_ta = 11.81 from the Planck-ΛCDM
shell ODE), PM catchments `in_cover(…, x = 1)` at `cfg527_pm.py:383, :391`, edge `x_supply` at `:313-319`.
Owner rule (10-10): framework-native only; neither ΛCDM nor standard MOND as yardstick or hidden ingredient.

Settings: κ = ½ FITTED; footings 9.3603e-11 (canonical) / 1.1312e-10 (alt) never pooled; the cold energy's MASS is still required;
no particle species is added; not "theory closed". Other lanes read only. No downloads. Compute: nice -n 10, ≤ 8 threads in total,
at most one 512³ job at a time, memory checked first.

## 0. What is and is not changed (one ingredient at a time)

Changed: ONLY the supply — (i) the cold mass M_cat that sets each host's emergent edge (CFG541 §7: the inside-out fill stops where
the catchment's cold runs out; for a point mass r_e = r_M / ln(1 + M_b / M_cat)), and (ii) the region the settled cold energy is
drawn from and conserved in (the catchment).
Unchanged (declared, inherited or posited, NOT this lane's target): ICs and background (L01/L02), the ν_mono kernel (D01), the
census f_ret painting of the phantom's baryons and M_b = f_ret f_b M_ta (L06), the global QUMOND phantom (M01), the cap
x ≤ 1, the switch width ε, the draw weight s_c, the cache cadence (every 10 calls), the step grid. The host list (resolved peaks
and r_ON) stays the engine's own; it is used only to name hosts and to report the ASSUMED supply they are given.

## 1. Definitions (frozen)

- **Bound region B** (framework-native; replaces the Δ_ta ball as the supply region): B = {cells with raw switch f_sw > 0},
  f_sw = clip(0.5 + (λ₂ − τ)/(2ε), 0, 1) computed by the engine (`cfg527_pm.py:378`) BEFORE the edge mask is applied, i.e. the
  candidate-B switch support λ₂ > τ − ε (F03). Every cell that can carry settled source e lies in B. Statement: τ = (Δ_ta − 1)/3
  still uses the shell-ODE Δ_ta; CFG594 L03 classes that ODE as the framework's own pre-turnaround collapse under candidate B
  (given L02). No turnaround-ball finder (no Δ_ta top-hat mean) enters B. Components: periodic 6-connected (engine `catch_labels`).
- **Systems** (dedupe of sub-peaks): resolved host peaks are grouped by the engine's catchment component (`in_cover(x = 1)`
  component); M_sys = the largest M_ta of the system's peaks; assumed supply A_nom = (1 − f_b) M_sys; also reported
  A_PM = (1 − f_b) × particle mass actually inside the system's catchment component (what the PM's assumed rule holds).
- **Measured supply S** (step 2a): S_sys = (1 − f_b) × particle mass of every B-component that contains at least one of the
  system's peak cells; a B-component containing peaks of several systems is split between them in proportion to A_PM.
  A peak not inside B contributes nothing (S can be 0). Cell mass = 0.315 × 2.775e11 × dx³ (1 + δ) [M_sun/h], the constant used
  by the engine's M_ta. Also reported: S_in = (1 − f_b) mass(B ∩ catchment) and the B mass attached to no host.
- **Settled source assigned** (step 2b): E_sys = the engine's per-catchment Σe after the q ≤ 1 cap, converted to mass
  as Σ e × a/(1.5 Ω_m) × ρ̄ dx³ (ρ̄ dx³ = 0.315 × 2.775e11 × dx³), on the ASSUMED-supply state.
- **Ratios** (step 2c): primary ρ = S_sys / A_nom; secondary S_sys / A_PM and E_sys / A_nom.
  Reported per run, per z ∈ {1, 0.5, 0}, in log10 M_sys bins [12, 12.5), [12.5, 13), [13, 13.5), [13.5, 14), [14, 14.5), [14.5, 16):
  median ρ and the mass-weighted ratio Σ S / Σ A_nom (bins with < 5 systems reported, flagged, not used in any criterion).
  Global: Q = Σ S / Σ A_nom over all systems.

## 2. Runs and states

- Measured states (ASSUMED supply = the CFG530 runs): L100 N128 and N256 both footings re-run with this lane's engine copy in
  mode ASSUMED, which additionally dumps the mesh δ at z = 1 and 0.5 (z = 0 positions as before). These re-runs are also MU1.
  z = 0 also from CFG530's saved states: L100 N512 and L200 N128 / N256 / N512, both footings (512³ one at a time).
- Engine: `cfg595_pm.py` = a copy of `cfg527_pm.py` (sha256 aeabd0ba…) with ONE added switch CFG595_SUPPLY ∈
  {ASSUMED, MEAS, ZERO} and the δ dumps; ASSUMED goes through the new code path with S_h = (1 − f_b) M_ta,h and catchment =
  `in_cover(x = 1)` components, draw region = catchment ∖ edge (= cfg527 exactly). MEAS: S_h = S_sys of the host's system,
  edge x_h = min(r_M / ln(1 + M_b,h / S_h) / R_h, 1), conservation per B-component, draw region = B ∖ edge (weight s_c),
  q ≤ 1 cap unchanged. ZERO: S_h = 0 and draw availability × 0 (same code path as MEAS).
- Step 3, dynamic re-run with the measured supply: MEAS at L100 N256, canonical and alt (primary); MEAS at L100 N128 both
  footings (convergence, reported). The supply is measured in-run from the evolving state (same cadence as the engine's edge cache);
  it is the framework's own measured supply rule, not a fit. The tabulated rule ρ(M, z) from step 2 is reported as its description.
- Static estimate (declared approximation, reported only): forces in MEAS mode on the saved ASSUMED z = 0 states (no
  re-evolution) at N256 (calibrated against the dynamic MEAS run) and at L100 N512.

## 3. Statistic for step 3 (CFG555 machinery, unchanged)

Gravitating density δ_grav = −k² φ̃_k / (1.5 Ω_m) captured from the engine's own acceleration transforms at z = 0 (CFG526 / CFG555
method); P(k) with the engine's `measure_pk`; ratio r(k) = P_grav / P_S0 against the same-pipeline S0 JSON at the same (L, N)
(CFG530 `runs/S0_L100_N256`, `S0_L100_N128`). Reported: max|r − 1| over k ≤ 1 h/Mpc ("k ≤ 1 excess"), mean r over 1 < k ≤ 2
("k 1–2"), r at k = 0.5 / 1 / 2, σ8 ratio. Compared with the ASSUMED-supply values of CFG555 (`cfg555_results.json` →
`cfg530.530_LR{can,alt}_L100_N256`: max|r − 1| 0.661 / 0.634) and with this lane's own ASSUMED re-run.
S0 is the same-pipeline reference only (a ΛCDM-dynamics run with no law); no verdict against data is drawn here.

## 4. Verdicts (per footing; never pooled)

- Supply (primary run L100 N256, z = 0, Q): **MEASURED SUPPLY SMALLER** if Q ≤ 0.80 (report 1 − Q); **SIMILAR** if
  0.80 < Q < 1.25; **LARGER** if Q ≥ 1.25. Also reported at z = 1 and 0.5 and per mass bin.
- Convergence (L100, z = 0): **CONVERGED** if |Q(N256) − Q(N512)| ≤ 0.10 and every mass bin with ≥ 5 systems in both has
  |Δ(Σ S / Σ A_nom)| ≤ 0.15; else **NOT CONVERGED** (the verdict above is then stated as resolution-dependent).
- Excess with the measured supply (dynamic MEAS L100 N256): **EXCESS PERSISTS** if max|r − 1|(k ≤ 1) > 0.10;
  **EXCESS REMOVED** if ≤ 0.10 and |σ8 ratio − 1| ≤ 0.05; otherwise **PARTIAL**. Reported with the fraction of the ASSUMED
  excess removed, 1 − (max|r − 1|_MEAS / max|r − 1|_ASSUMED), and the same for |mean r(1–2) − 1|.
  The 0.10 / 0.05 numbers are CFG361's same-pipeline cuts used as a label only.

## 5. Controls and MUTATE (a failure blocks the verdict it feeds)

- **MU1 (assumed supply reinserted):** ASSUMED re-runs (L100 N128 and N256, both footings) reproduce the CFG530 run JSONs'
  particle P(k) and σ8 at z = 1, 0.5, 0 to ≤ 1e-6 relative, and the z = 0 gravitating max|r − 1| reproduces CFG555's number to
  ≤ 1e-4 absolute (N256; N128 vs CFG555's cache likewise).
- **MU2 (supply zero):** ZERO at L100 N128, both footings, reproduces S0_L100_N128's particle P(k) and σ8 at every snapshot to
  ≤ 1e-6 relative, and the captured source is zero (max|δ_src| ≤ 1e-6 of max δ_p).
- **C1 (measurement = engine):** on each measured ASSUMED state, Σ_sys E_sys (in s units) and the number of catchments equal the
  engine's own diag e_sum and n_catch to ≤ 1e-5 relative / exactly.
- **C2 (bookkeeping closure):** Σ_sys S_sys + unattached B mass = total B mass × (1 − f_b) to ≤ 1e-6 relative.
- **C3 (spherical limit, sanity, reported):** for systems whose B-component and catchment are each a single component holding
  one peak, the median S_in / A_PM is reported (expected near 1 by F03 if hosts were spherical; a deviation measures asphericity
  and is not a failure).
- **MUTATE file:** `CFG595_MUTATE=1` runs the analysis with the measured S replaced by A_nom (ρ ≡ 1 → SIMILAR required) and with
  the MEAS P(k) replaced by the ASSUMED P(k) (→ EXCESS PERSISTS with 0 removed required); both teeth must bite.

## 6. Disclosures fixed in advance

- Only z = 0 particle states were saved by CFG530; z = 1 / 0.5 states come from this lane's ASSUMED re-runs (MU1 proves they are
  the CFG530 runs).
- The census f_ret, M_b, x ≤ 1 cap, ε and the global QUMOND phantom stay inherited; a supply change cannot remove them.
- Any deviation from this text after commit is reported as a dated disclosure in the README; this file is never edited.
