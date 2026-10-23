# X1_hosted_recount: FROZEN CRITERIA (written and committed before any script or number of this lane)

Lane X1 of `rebuild_2026_10_22/X0_explanation_map/MAP.md` (§1.D items 1–2, §3 "Board tile 26").

**Questions.**
- **Q1.** Is v3's dwarf-satellite failure (S1: +1.33 / +1.30 dex at the L★ floor) a property of dwarf satellites, or of E3's sample?
  E3's cut M★ < a₀L★²/G (≈ 3.9e5 M☉) removed every classical MW dSph and the bright M31 dSphs, and left 31 MW ultra-faints in 45.
- **Q2.** Does U1's theorem-T3 premise survive? The premise: a system held in a static host carries no dust, so it is Newtonian.
  This is tested against hosted systems that are measured to be non-Newtonian. It tests the premise, not the law.

Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md`. κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11 and alt
1.1312e-10 m/s², never pooled. No dark-matter particle; the cold sector is BS dust ("cold energy"). Never "theory closed". Never "the
data favour the framework". No downloads; the literature inputs are PROVISIONAL web look-ups (`LITERATURE_LOOKUP.md`). Every run is
`OMP_NUM_THREADS=1 nice -n 15`, one thread, < 1 GB RSS, ≤ 30 min per process. No new knob, no M/L refit beyond the record's declared
prior (Υ_V = 2, bracket 1–4), no scan.

**Seen before freezing (disclosed).**
- S1's README, JSON and `s1_per_system.csv`; MAP's audit medians from that CSV (MW +1.47, M31 +0.89, M31 log M★ ≥ 5 +0.47,
  Crater II +0.36 dex).
- U1's README and JSON numbers (B0 satellites +2.00 / +1.99; Coma B0 z_sys 5.41; TDG B0 +0.055 ± 0.114; DF B0 +0.028 ± 0.539 ln;
  UMa per galaxy z 12.6–14.4).
- CFG948's Newton exclusion (z 5.45). T1's README. E3's README.
- h43's (`hunt_2026/h43_h44_ufd_m31_sigma.out`) QUMOND 1-D EFE medians: MW classical +0.32, Collins M31 +0.48 dex in σ.
- The literature values in `LITERATURE_LOOKUP.md`. Two hand checks of that reading: And I's σ_iso from Eq. (2) is 9.19 km/s
  (printed 9.2), and its σ_efe from Eq. (3) with μ = x/(1+x) at LVD's 44.39 kpc is 8.0 (printed 8.0).
- The list of LVD systems with a measured σ (names, M_V, log M★, R_e, host distance).
- **No Δ, χ², z or class of this lane has been computed.**

**Pre-result analytic expectation (stated so it cannot be tuned afterwards).** The published Eq. (3) uses the full mass M.
The record's Wolf convention, on both the data side and the prediction side (E-W), uses M(<r_{1/2}) = M/2 (Plummer: 0.512 M).
In the external-field-dominated regime this alone puts an exact solve **≈ −0.15 dex in σ** below the published σ_efe. AQUAL's
anisotropic external-field response is also expected to give a monopole G_eff at or below the naive G/μ_e. The C2 control
(§2) may therefore fail for a known reason. The stop rule (§3) says in advance how that case is read.

## 1. The theory, solver and estimator (FRAMEWORK-NATIVE; S1's, read-only)

v3's static equation, solved exactly as S1 solves it:

    ∇²ψ = ∇·p(∇χ),   χ = Φ_N + ψ + (L★²/2)∇·p(∇χ),   p(v) = v/(1 + |v|/a₀).

- L★ = 0 is AQUAL with μ = x/(1+x).
- The host enters as a uniform **total** background field x_e = g_e/a₀, and the response is solved (no recipe).
- Solver: `doors_push_2026_10_22/D10_native_Lstar/d10_solver.py`, imported read-only, D10/S1 grid (nper 24, N_θ 16, r ∈ [1e-3, 1e4] a).
  Cross-checks: F2's AQUAL point-mass solver (`rebuild_2026_10_22/F2_outer_lensing/f2_aqual.py`, read-only) and Route F (C6 kernel,
  in `d10_solver`).
- S1's code paths (data loader, Monte Carlo, 3 × 3 MC grids in log y and log Λ, bootstrap, host fields, E3's CFG691 recipe) are
  **copied** into this lane's script with provenance (S1 commit 2b6bb658a1). S1's script cannot be imported: it runs on import.
- Each system is a Plummer sphere, a = R_e (circularised `rhalf_sph_physical`), M = M★ (LVD `mass_stellar`, Υ_V = 2).
- **E-W (primary):** σ² = r₁₂ g(r₁₂)/3, r₁₂ = (4/3) a. The data side is g_obs = 3σ²/r₁₂.
- **E-V (reported):** the exact global virial.
- Statistic, as S1: Δ = log₁₀(g_obs/g_pred) (dex in **g**, = 2 Δ log σ). Per system: NMC = 2000 Monte Carlo draws of σ, R_e and
  distance modulus (M★ ∝ D², R_e ∝ D). Classes use the bootstrap median over systems (NBOOT = 4000) ± bootstrap sd.

## 2. Steps, in order

### Step 0: read the same data (K0)
Rebuild E3's sample (45 canonical / 46 alt) and S1's data choices with S1's code path and S1's seed (20261023), in S1's RNG order.
Tabulate v3 at the L★ floor (21.68 / 22.85 pc) in the E_mid host field.
- **K0 PASS** iff N = 45 / 46 and the clean-primary E-W Δ and its bootstrap sd equal S1's JSON
  (`satellites["<foot>|primary|S4 v3: AQUAL + EFE + screening L*floor E-W"]`: +1.33072 ± 0.14735 / +1.29900 ± 0.14742) within 0.005 dex.

### Step 1: controls against published MOND (S1's solver at L★ = 0, AQUAL + EFE, no screening)
All controls use **the papers' own a₀ and inputs** (LITERATURE-INPUT, PROVISIONAL), not the footings. The controls test the solver
and the inputs, not the framework's a₀.

**MM13 rows.** The 30 unique M31 dwarfs of `LITERATURE_LOOKUP.md`; And XVIII is dropped (no host distance in its LVD row's
`distance_host`, and no printed σ_efe), leaving **29**.
- M = 2 L_V, Plummer a = (3/4) r_{1/2}, a₀ = 1.21e-10.
- **Field:** where σ_efe is printed, x_e is backed out of it with Eq. (3) and μ = x/(1+x). This makes the input exactly the paper's
  own G_eff. Otherwise x_e = (230 km/s)²/(D a₀), with D = LVD `distance_host`.
- **Published adopted prediction** σ_pub = min(σ_iso, σ_efe) as printed (σ_iso where no σ_efe is printed).

**Crater II.** M = 3.3e5 M☉, a = 1066 pc, a₀ = 1.2e-10, x_e = 0.076; σ_pub = 2.1 km/s (EFE).

**Checks and control lines:**
- **C0 (transcription, check):** Eq. (2) with the transcribed L_V reproduces every printed σ_iso to |Δ log σ| ≤ 0.02 dex. Crater II's
  Eq. (1) and Eq. (2) values reproduce 4 and 2.1 km/s to ≤ 0.02 dex.
- **C1 (on-disk inputs, reported; flag line 0.05 dex):** Eq. (3) with μ = x/(1+x), V = 230 km/s and LVD `distance_host`, against the
  printed σ_efe. Reported: the median |Δ log σ| over rows with a printed σ_efe. Above 0.05 dex the README flags the method reading
  as uncertain. C2 does not use C1's fields.
- **C2 (the control):** the solver's E-W σ (L★ = 0, the control field above) against σ_pub.
  - **C2 PASS** iff median_i |log σ_solver − log σ_pub| ≤ **0.10 dex** over the 29 MM13 rows **and** Crater II's |Δ log σ| ≤ 0.10.
  - Reported beside it: E-V; the signed median; per-row values.
- **Decomposition (reported, pre-declared), per row:**
  - D0 = σ_pub.
  - D1 = the published method re-evaluated on the control inputs: min(Eq. 2, Eq. 3).
  - D2 = D1 with the Wolf mass convention. Eq. (3) uses M/2; the isolated form uses Wolf's deep-MOND σ⁴ = G M a₀/18. Then the min.
  - D3 = the solver (E-W).
  - m_tot, m_mass and m_rem are the signed medians over the 29 rows of D3−D0, D2−D1 and D3−D2, each in dex of σ.
- **C3 (solver physics, checks):**
  - (a) Isolated deep MOND: solver E-V at y = 1e-5 and 1e-4 against Eq. (2) (an exact theorem for the global dispersion),
    |Δ log σ| ≤ 0.005 dex.
  - (b) Linear EFE: solver monopole field at r = a against Route F, at x_e ∈ {0.05, 0.076, 0.3, 0.5}, y = 1e-4 x_e, Λ ∈ {0, 0.5, 2}
    (Λ = 0 only at 0.076 and 0.3); relative error < 2e-2.
  - (c) Embedded AQUAL: the solver against F2's point-mass solver (S1's K3 cells); < 2e-2.
  - (d) Convergence at Crater II's control cell and at And I's: grid doubling and r_out × 10 change σ (E-W, E-V) by < 5e-3.

### Step 2: v3 on all Local Group satellites with a measured σ on disk, no mass cut (if §3 allows)
**Sample.** Every row of `real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv` with a measured `vlos_sigma` (upper limits
have no `vlos_sigma` and are not used), S1's loader.

**Classes (fixed here, by name or rule).**
- **MW classical dSphs (verdict class, 8):** Carina, Draco, Fornax, Leo I, Leo II, Sculptor, Sextans, Ursa Minor.
- **MW ultra-faints (verdict class):** MW-table systems with M_V > −7.7 (Simon 2019's boundary, as h43).
- **Bright M31 dSphs (verdict class):** M31-table systems with log M★ ≥ 5, except M32, NGC 147, NGC 185 and NGC 205.
- **M31 others (verdict class):** M31-table systems with log M★ < 5.
- **Reported individually, no verdict weight:** Crater II, Antlia II, Canes Venatici I, Sagittarius (tidally disrupting).
- **Reported as classes, no verdict weight:** M31 dEs (NGC 147, NGC 185, NGC 205); LG field dwarfs (the 13 local-field rows).
- **Excluded, with reason:**
  - LMC and SMC: rotation-supported discs; the Wolf estimator does not apply.
  - M32: a compact elliptical 6.5 kpc from M31; the uniform-field model does not apply.

**Host fields.** S1's: v3's law field of a Hernquist host (a_H = 3 kpc) at LVD `distance_host`.
- MW 6e10 M☉ (E_mid); bracket E_lo 4e10 and E_hi Mb_hi(a₀). M31 1e11 M☉ with the same fractional bracket.
- Two rules differ from S1's code, and only for systems outside E3's sample:
  - M31 systems with no `distance_host` (And XVIII) use LVD `distance_m31`. S1's code would use the heliocentric distance.
  - Field dwarfs use the MW field at the heliocentric `distance`, ignoring any `distance_host`. For Antlia B, that column is its
    distance from NGC 3109.

**Data choices.**
- **Primary:** LVD σ. The binary correction is S1's Arroyo-Polonio free-f ratio where matched; S1's median ratio for other systems
  with M_V > −7.7; none (b = 1) for M_V ≤ −7.7. The UFD-calibrated median ratio is not applied to bright, many-star systems.
  Υ_V = 2.
- **W (worst-clean, reported):** S1's W (Υ_V 4, f = 0.7 ratios, lower of LVD/Geha σ), with the same M_V rule for the median ratio.
- Own seed 20261031; NMC, NBOOT and the MC grids as S1.

**Predictions per system, per footing.**
- Newton (E-W Plummer).
- Isolated AQUAL (L★ = 0).
- AQUAL + EFE (L★ = 0; "exact MOND + EFE").
- **v3 = AQUAL + EFE + screening at L★ = floor (21.68 / 22.85), 24 and 90 pc.**
- Host bracket E_lo / E_hi at the floor.
- E-V at every L★.
- Reported side row, STANDARD-MOND-MACHINERY with no verdict weight: the published MM13 recipe (Eq. 2/3, μ = x/(1+x),
  min rule, full M, r_{1/2} = (4/3) R_e) at each footing's a₀, in the same E_mid host field.

**Per-system central values and χ².**
- Δ_i = the median of the system's MC draws. s_i² = sd_MC,i² + (0.15 k_i)².
- 0.15 dex is the Υ_V prior: the record's 1–4 bracket read as ±2σ about 2.
- k_i = |1 + ∂ log₁₀(g_pred/g_bar)/∂ log₁₀ y|, taken from the system's own floor table at its central Λ.
- χ²_C = Σ_i (Δ_i/s_i)² over class C. It is acceptable iff χ²_C/N_C ≤ 1 + 3√(2/N_C).

**Class status (per footing, clean primary, E-W, L★ floor).**
- **PASS-LIKE:** |median Δ| ≤ 0.15 dex **and** χ² acceptable.
- **FAIL:** |median Δ| > 0.15 dex **and** |median Δ| ≥ 3 × bootstrap sd.
- **UNRESOLVED:** otherwise, naming the reason (χ² only, or < 3 sd).

### Step 3: T3 bookkeeping (no new solve)
T3's prediction for a hosted system that falls with its host: dust-free, so **Newtonian on its baryons** (U1 B0). Each row is
Δ_N = log₁₀(g_obs/g_N) (E-W Plummer Newton) with its significance:
- Crater II and Antlia II (individual): z = (Δ_N − 0.301)/sd_MC. This is Υ_V = 4, the conservative edge.
- MW classical, bright M31, M31 others, MW ultra-faints (classes): z = (median Δ_N − 0.301)/bootstrap sd; plus the count of
  members with individual z_i ≥ 3.
- Coma UDGs: CFG948 `byfoot.<foot>.primary.H_newton.z` and U1 `numbers.N5.coma.<foot>.B0.z_sys` (read, not recomputed).
- UMa members: U1 A4 `numbers.F5.footings.<foot>.A4.{any_radius,beyond_rf}.per_galaxy.z_from_Newton` (read).
- Booked in the same table, as T3-consistent hosted systems: P4's TDGs (U1 `numbers.N5.tdg.<foot>.TDG_B0`) and DF2/DF4
  (U1 `DF_B0`; CFG948's z).

## 3. Verdict classes and the stop rule (frozen)

**Step-1 outcome.**
- **CONTROLS PASS:** K0, C0, C3a–d and C2 all pass. Go to step 2.
- **CONTROL FAIL, PUBLISHED APPROXIMATION.** All of the following:
  - K0, C0 and C3a–d pass, and C2 fails.
  - Over the 29 MM13 rows, m_mass has the sign of m_tot, |m_mass| ≥ ½|m_tot|, and m_rem ∈ [−0.10, +0.02] dex.
  - The same three conditions hold for Crater II's own steps.

  The solver then reproduces published MOND's physics, and the published numbers carry their estimator's normalisation. Step 2 runs.
  Every step-2 number is labelled as computed with the exact estimator, which sits below published MOND's numbers by the stated m_tot.
- **CONTROL FAIL, UNEXPLAINED** (any other failure): **STOP.** Step 2 is not run. The README reports the controls. Step 3 needs no
  solver and is still reported.

  *This refines the brief's literal "if the controls fail, stop". It is frozen here, before any number, because of the analytic
  expectation above. It is a deviation from the brief and is flagged as one.*

**Step-2 verdict (Q1).** Status as in §2, on both footings at the floor.
- **(i) SAMPLE-DRIVEN:** MW classical and bright M31 are both PASS-LIKE on both footings, **and** MW ultra-faints FAIL on both.
- **(ii) GENERIC:** MW classical, bright M31, M31 others and MW ultra-faints all FAIL on both footings.
- **(iii) CLASS-GRADED:** anything else. The status and median Δ of each class are named.
  - Label **FOOTING-SPLIT** if a class's status differs between footings.
  - Label **W-SENSITIVE** if W changes a verdict class's status.
- Reported with every verdict:
  - the L★ 24 / 90, E-V and host-bracket rows;
  - the exact MOND + EFE row (L★ = 0), which says whether a failure is v3-specific (screening) or shared by AQUAL;
  - the published-recipe side row.

**Step-3 verdict (Q2).**
- **T3 PREMISE CONTRADICTED:** at least two hosted rows from independent data sets conflict with Newton at ≥ 5σ, on both footings,
  after the conservative Υ_V = 4 (or the row's own committed systematics).
  - The independent data sets are: Crater II, Antlia II, each class, the Coma UDGs, and the UMa members.
- **T3 PREMISE SUPPORTED:** no hosted row conflicts with Newton at ≥ 3σ.
- **MIXED:** otherwise.
- **Booking rule:** if CONTRADICTED, the TDG and DF2/DF4 "native pass" is reported as T3-consistent in those systems while T3 fails
  in the contradicting sets. It is not credited as an independent success.
- What the bookkeeping cannot separate is stated in the README: a wrong premise, a v3 that fails for hosted systems, or systems out
  of equilibrium (tidal heating).

## 4. Checks (script prints `Kn/Cn PASS|FAIL value threshold`; exit 0 iff every check passes)

| check | line |
|---|---|
| K0 | step-0 reproduction (above) |
| C0 | transcription |
| C3a–d | solver physics (above) |
| KT | determinism: the step-2 floor tables reproduce the step-0 floor tables for every system in both, to 1e-9 dex; exempt: none expected, since E3's systems use the same host rule |
| KS | every production solve converged (scaled residual < 1e-8) |
| KR | peak RSS < 1 GB in every process |

C1 and C2 are outcome lines (§3), not checks.

**`--mutate`:** S1's host-field bug, the solver background set to the Newtonian y_e = x_e²/(1 + x_e) instead of the total x_e.
**K0 and C3b must FAIL.** The mutate run computes steps 0–1 only and writes `*_MUTATE.*`.

## 5. What each outcome means
- **SAMPLE-DRIVEN:** tile 26's FAIL is a property of E3's ultra-faint sample. The board's "dwarf satellites" wording must be
  narrowed to ultra-faints.
- **GENERIC:** v3 fails hosted dwarfs of every luminosity. E3's cut did not create the failure.
- **CLASS-GRADED:** the gap depends on the class; the README gives each class's size.
- **T3 CONTRADICTED:** U1's "satellites dust-free" consequence is excluded by hosted systems that the record itself measures. The
  TDG/DF2 native pass rests on the same premise and is booked with them.

κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework.
