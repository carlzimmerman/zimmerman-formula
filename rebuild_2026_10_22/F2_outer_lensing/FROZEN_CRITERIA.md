# F2_outer_lensing: FROZEN CRITERIA (committed alone, before any script or number of this lane)

Brief: `rebuild_2026_10_22/BRIEF.md` (failure 2) plus `doors_push_2026_10_22/BRIEF.md` and `BRIEF_E_AUDIT.md`.
κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11, alt 1.1312e-10 m/s², scored separately, never pooled.
No dark-matter particle. Never "theory closed". Never "the data favour the framework".
Assumption ledger: `ASSUMPTION_LEDGER.md` (committed with this file).

## 0. The failure being rebuilt

Record: CFG804 → CFG902 (declared Msun/h convention). On Brouwer et al. 2021 (B21) Fig. 3 KiDS-1000 isolated lenses,
4 stellar-mass bins × 15 radii (0.035–2.6 Mpc), released covariance: the derived catchment model D_der falls short of
the no-edge law B at all radii, Δχ²(D_der − B) = **+100.10 canonical / +123.12 alt** (χ²_B = 163.1 / 155.3).
CFG903's catalogue two-halo term (catchment-supplied neighbours) brings it to +40.7 / +52.8 (PARTIAL).

## 1. Cross-check (must pass before anything else is read)

K0: my own re-implementation (not an exec of the record script) of CFG804's model with CFG902's R1 convention
reproduces χ²_B(all) 163.1 / 155.3 and Δχ²(D_der − B) all radii +100.10 / +123.12 to |Δ| ≤ 0.05, and primary
(R ≤ 0.31 Mpc) +0.84 / −0.27 to |Δ| ≤ 0.05. If K0 fails, the lane stops and reports why.

## 2. The rebuild model T (the screened covariant theory, THEORY_V3_DRAFT §1)

- Field equation: AQUAL, ∇·[μ(|∇Φ|/a₀)∇Φ] = 4πGρ_b, μ = x/(1+x) (C4 K1/K2; E2). Lensing sees Φ (C4: ϕ = ψ).
  Screening (L★ ≥ 21.7 pc) is irrelevant at R ≥ 35 kpc (stated, not computed).
- Baryons per lens (each a stated input with an error bracket, ledger rows B1–B3):
  stars M★ (record lens catalogue `lr_lenses.npz`, LePhare + 0.15 dex); cold gas f_cold M★ with
  log f_cold = −0.69 log M★ + 6.63 (B21's relation as used by the record); hot CGM f_hot M★ as a uniform sphere of
  radius 100 kpc, central f_hot = 0.5, bracket [0, 1.0] (derived from CFG580's recorded emissivities and the recorded
  eRASS:4 stacked L_X; ledger B3). Stars + cold gas are a point mass (R ≥ 35 kpc).
- External field: uniform Newtonian y_e (units of the footing's a₀); total external field x_e from μ(x_e)x_e = y_e.
  Three values, all reported: y_e = 0 (maximum outer signal); **primary** y_e = Chae+21 "noclu" median
  10^−3.215 × (1.2e-10/a₀) (the weakest on-disk empirical estimate, `real_research/reviews/directional_efe_2026/laneB_data/chae21_env.csv`);
  upper y_e = Chae+21 "maxclu" median 10^−2.30 × (1.2e-10/a₀). The EFE is solved with my own axisymmetric AQUAL
  solver for a point mass in a uniform field; lensing uses the orientation-averaged effective mass
  M_eff(<r) = r²⟨∂_rΦ⟩_Ω/G (exact for random orientations). Extended baryons: isolated AQUAL (exact in spherical
  symmetry) × the point-mass EFE ratio C(r; y_e) (exact at R ≥ 100 kpc where all baryons are enclosed).
- Native background: h = 0.679 (mid of 67.2–68.6, C2 K5), ends 0.672 / 0.686 reported; Ω_m = 0.3085 (CFG682 via CFG885).
  Data: ΔΣ × (h/0.70) × T_Ωm, R × (0.70/h) × D_A ratio; masses × (0.70/h)² × D_A ratio²; T_Ωm = 1.0128 (B21 fid
  Ω_m 0.2793) / 1.0037 (record re-measurement, fid 0.3), from CFG885's committed JSON (survey calibration).
- Cold-energy (BS dust) term: the covariant theory fixes the dust abundance as a cosmological initial condition only
  (C2, C4); it predicts no galaxy-bound dust profile (OPEN). T therefore contains **no dust term** (adding one would be a
  new knob). The dust the data would need is reported as an output (inner amplitude A_in, R ≤ 0.31 Mpc).
- Stacking: per B21 mass bin, the model is the lens-weighted mean of ΔΣ_T(R; M_b,i) over the record's lenses in that bin
  (weights = each lens's total Σ_crit⁻²-weighted source weight from `cfg110_perlens.npz`).

## 3. Statistics

- Track A (B21 Fig. 3, released covariance, bias-corrected): χ²_all (60 points), χ²_out (R > 0.4 Mpc, 28 points),
  Δχ² ≡ χ²(model) − χ²(B refit on the same data version; B = record's law, no EFE, M_b profiled per bin as in CFG804).
  GLS amplitudes of data relative to the model: A_O1 (0.4 < R < 1.1 Mpc, 16 points), A_O2 (R > 1.1 Mpc, 12 points),
  A_out (both), A_in (R ≤ 0.31 Mpc).
- Track B (record's per-lens re-measurement `cfg110_perlens.npz`, g_bar bins, delete-one jackknife over the 50 record
  patches): per isolation sample S, the same amplitudes A_O1, A_O2 (bins whose lens-median R lies in the range), with
  inverse-variance weights from the jackknife diagonal and the jackknife error of A itself. Samples (nested):
  S10 = record base (|Δχ| < 10 Mpc, 181,477), S20, S30 (`cfg96_isoflags.npz`), and **S_strict** = S30 ∩ no neighbour with
  log M★ ≥ log M★_lens within projected 1 Mpc (h70, physical, at the lens z) and |Δχ| < 100 Mpc (pool = the record's
  neighbour pool: r < 20, 0.1 < z < 0.5, unmasked, log M★ > 7). Shear calibration 1/(1+K), K = −0.0147 (B21 column).
- "Falls short" in a range ≡ A − 1 > 3σ_A. "Overshoots" ≡ 1 − A > 3σ_A. "Consistent" ≡ |A − 1| ≤ 2σ_A.

## 4. Ladder (Track A; each step reported with χ²_all, Δχ², χ²_out, A_O1, A_O2, A_in; both footings)

L0 record D_der (K0). L1 remove the catchment edge (covariant theory: phantom is a field response, not supply-limited) =
B with profiled masses. L2 native h, Ω_m (masses still profiled). L3 inventory masses M★ + cold gas, nothing profiled.
L4 + hot CGM (central). L5 + EFE (primary y_e) = **T_central**. Then one at a time from T_central: EFE y_e = 0 / maxclu;
f_hot 0 / 1.0; f_cold ± 0.2 dex; M★ −0.2 dex (E1) and +0.2 dex; h 0.672 / 0.686; source photo-z / Σ_crit ± 3 % (KiDS
SOM δz, survey calibration); boost: none applied (no correction exists in B21's released ESD; stated). Two-halo terms:
CFG903 (catchment-supplied neighbours), CFG805 (T1x, free bias), CFG502 (ΛCDM halo model) are audited and reported only;
none enters the verdict.

## 5. Verdict rule (per footing; evaluated separately at each y_e)

Let T_y be T_central with the given y_e.
1. **EXPLAINED (no catchment edge)** if on Track A both A_O1 and A_O2 are "consistent" for T_y.
2. Else **EXPLAINED (contamination of the isolated sample)** if on Track B A_out(S10) − A_out(S_strict) > 3σ (paired
   jackknife of the difference) **and** S_strict is "consistent" with T_y in both O1 and O2.
3. Else **REAL FAILURE** if S_strict "falls short" (> 3σ) in O1 or O2 for T_y — or "overshoots" (> 3σ).
4. Else **UNDECIDABLE** (S_strict too noisy, or neither line met).
Overall: the y_e = 0 / primary / maxclu verdicts are all reported; the lane verdict is the primary-y_e verdict if all
three agree, else **UNDECIDABLE (g_ext-limited)** with the split stated. Footings are reported separately; if they
disagree, the lane verdict is UNDECIDABLE (footing split).
A cure must be a named ingredient from the brief (AQUAL, screening, BS dust, native H₀, E1/E4 inputs) or a measured
sample property; no fitted amplitude, bias or profile enters any verdict.

## 6. Checks (script `f2_outer_lensing.py`, one line per check, exit 0 iff all pass; `--mutate` separate files)

K0 record reproduction (above). K1 AQUAL solver: y_e → 1e-6 reproduces the isolated law M_eff(<r) to ≤ 1e-3 at
r ≤ 10 r_M; far field (r ≥ 10 r_e) matches the linearised anisotropic solution's angle-averaged mass to ≤ 2 %.
K2 cross-check of my AQUAL solver against the record's independent E2 solver (`doors_push_2026_10_22/E2_field_equation/aqual_axi.py`)
at one y_e: M_eff(<r) agree to ≤ 2 % for 1 ≤ r/r_M ≤ 100 (if E2's API cannot be called read-only, reported N/A, not PASS).
K3 projection: ΔΣ of a point mass and of the isolated law against analytic forms (≤ 1e-3).
K4 Track B base sample reproduces the record's per-patch sums (cfg96 W10 stack, all lenses) to 1e-10; and its stack
vs B21 Fig. 9 median ratio over S/N > 3 points lies in [0.8, 1.25] (information on calibration, recorded either way).
K5 isolation samples nested (S_strict ⊂ S30 ⊂ S20 ⊂ S10).
MUTATE (`--mutate`): B21 data × 1.10 before K0 → K0 must FAIL (exit 1), outputs `*_MUTATE.*`.
Compute: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, minutes; no downloads; no PM simulation.
