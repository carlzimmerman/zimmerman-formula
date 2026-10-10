# CFG548 FROZEN CRITERIA: weighing the Local Group from its fringe (zero-velocity surface R0, local Hubble flow)

Frozen 2026-10-09, committed alone before any CFG548 script exists.
κ = ½ is FITTED. Footings 9.36e-11 / 1.13e-10 m/s² are never pooled; every number is reported per footing. Kernel
ν_mono(y) = 1/(1 − exp(−√y)). Candidate B: the law acts inside bound systems; settled cold energy (Ω_c/Ω_b = 5.364) is the law's
phantom, supply-capped, out to the census edge; no EFE. Shared-catchment rule (CFG522 M1): MW and M31 share one supply,
f_LG = 0.1704. The cold energy's mass is still required. Nothing here closes the theory.

## 0. The question
The Local Group's (LG) edge sits where its pull balances dark energy's push. The galaxies just outside the LG are on the local
Hubble flow; the radius R0 where their radial velocity relative to the LG barycentre is zero today weighs the LG
(Lynden-Bell 1981 / Sandage 1986; with Λ: Chernin+09, Peñarrubia+14). Test: does the framework's LG mass (CFG522) put R0 where
it is measured?

## 1. Data (no downloads)
- **Primary, on disk:** the Updated Nearby Galaxy Catalog (Karachentsev, Makarov & Kaisina 2013, AJ 145, 101; VizieR J/AJ/145/101),
  committed as `real_research/data/ungc_karachentsev2013.tsv` (fetched 2026-09-03). Columns used: Name, RA, Dec, Dist, f_Dist, Vlg
  (velocity in the LG frame of the catalogue), MD (main disturber), Ti1 (tidal index).
- **Frame:** barycentre on the MW→M31 line at fraction f31 of the M31 distance (UNGC MESSIER031 row); barycentric distance R and
  the Karachentsev–Makarov projection V_r = Vlg (D − D_c cos θ)/R (as FP11's `ungc_hubble`, with the barycentre at rest in Vlg).
  Primary f31 = 2/3 (the M1 shared-catchment split, M31 3.90e12 of 5.85e12; CFG522 JSON). Variants f31 = 0.5, 0.6.
- **Selection (frozen):** accurate distances only (f_Dist ∈ TRGB, Cep, RR, HB, SBF, BS, CMD, geom; FP11's list); fit window
  0.6 ≤ R ≤ 2.5 Mpc; keep a galaxy iff its MD is Milky Way, MESSIER031 or MESSIER033, OR Ti1 ≤ 0 (field), OR its MD itself lies at
  R < 1.5 Mpc from the barycentre (LG-fringe associations such as NGC 3109 / Antlia); drop all others (members of Sculptor,
  IC 342/Maffei, M81, NGC 2403, Cen A, ... groups). Rows without Vlg or Dist are dropped. Window variants: [0.5, 2.0], [0.7, 3.0].
- **Distance error:** 5% per galaxy (typical TRGB/Cepheid; PROVISIONAL), propagated as σ_i² = σ_int² + (dv/dR|_{R_i} · 0.05 R_i)²
  with the model slope; σ_int (the flow's intrinsic scatter) is a free fit parameter.
- **Published values (recalled, PROVISIONAL, not re-verified in this lane):**
  - Karachentsev+09 (MNRAS 393, 1265): R0 = 0.96 ± 0.03 Mpc; M_LG ≈ 1.9 ± 0.2e12 Msun (their mass relation; used only as a quoted
    number, never as an input to a mass here — this lane converts R0 to mass with its own model).
  - Peñarrubia+14 (MNRAS 443, 2204): M_LG = 2.3 ± 0.7e12 (point mass + Λ, local flow).
  - Peñarrubia+16 (MNRAS 456, L54): with the LMC, M_MW + M_M31 + M_LMC ≈ 2.64 (+0.42 / −0.38)e12.
  - Others named by the owner (Teyssier/Johnston, Benisty, Hartl/del Pino, Wempe, Anand/Tully local-flow fits, Cosmicflows-4) are
    NOT used: no on-disk table and no precise recall. Listed in the README as not used.

## 2. The model (derived, no knob)
Radial motion of a test galaxy about the LG barycentre, starting on the Hubble flow at the Big Bang (r → 0 as t → 0, the
Lynden-Bell–Sandage family, first-infall/outflow branch only), integrated to t0 = 13.80 Gyr (CFG513/515 constants:
h = 0.674, Ω_m = 0.3153, Ω_Λ = 1 − Ω_m, G = 4.30091727e-6 kpc (km/s)² / Msun):

  r'' = − G M(r, t) / r² − ½ (1 + 3 w(a)) Ω_DE H0² [ρ_DE(a)/ρ_DE,0] r

- w = −1 (primary): the push is + Ω_Λ H0² r (as CFG513/515/522's integrators). a(t) from the background Friedmann equation with the
  same Ω_m, h (needed only for w ≠ −1).
- **(i) Gravitating mass.** Under candidate B the law is OFF outside bound systems; the LG's settled region (cold-energy edges
  302/427 kpc canonical, 275/389 alt; CFG522 JSON) lies far inside the fringe, so a fringe galaxy feels Newtonian gravity of the
  enclosed total M = baryons + settled cold energy. Primary: point mass M, settled at all times (as CFG522). Footings then give the
  same R0; this is stated, not hidden. Declared profile variant (per footing): the rigid CFG513 `Prof` profiles of MW and M31
  (CFG522 M1 settings) both centred on the barycentre, M(r) = Mb_enc + Mdark (so early, small-radius phases feel less mass).
  Reported growth bracket (not judged): cold mass ∝ t (CFG522 M4 bracket).
- **(ii) Dark-energy push.** w = −1 primary; DESI w0wa variant w0 = −0.838, wa = −0.62 (DR2 + CMB + Pantheon+, PROVISIONAL; the
  value the repo uses); reported second variant w0 = −0.752, wa = −0.86. Same h, Ω_m; t0 = that background's own age.
- **(iii) Initial conditions.** Shells labelled by their energy; started at t_i = 1e-4 t0 at r_i = (9 G M t_i²/2)^(1/3) with v from
  the energy; v(R) at t0 tabulated on the first branch; R0 = the radius where v(t0) = 0.
- **Masses under test (from JSON, not retyped where a JSON exists):**
  - F-M1 shared catchment (CFG522 `M1.<foot>.full.M_tot`, 5.845e12) — the framework's PRIMARY LG mass;
  - F-CI census-individual (CFG522 `census_individual.<foot>.M_tot`, 8.142e12);
  - F variants (reported): M_b,MW 7.3e10 and +M33/LMC baryons (masses M_b (1 + 5.364/f_LG) from CFG522's f_LG values).
  - Reference, NOT candidate B (reported only): plain law on outside the LG, baryons 1.8e11 with ν_mono(g_N/a0) g_N, per footing.
- **ΛCDM comparator.** M_LG from the timing argument with the same constants: point-mass two-body, Λ, first approach at t0,
  D = 770 ± 40 kpc, v_r = −109.3 km/s, (a) radial and (b) v_tan = 82.4 km/s (Salomon+21; 2-D orbit). That M feeds the same R0
  prediction. (Simulation-calibrated timing corrections exist in the literature; not used — no precise recall.)
- **Fit (the weighing).** On the frozen sample, maximise the Gaussian likelihood of V_r,i against v(R_i; M) over (M, σ_int); M on
  a log grid 3e11–3e13 (interpolated). R0_meas = R0(M_fit). σ_boot = the std of R0_meas over 400 bootstrap resamples of galaxies
  (seed 548). σ_sys = half the full range of R0_meas over the declared frame/window variants (f31 ∈ {0.5, 0.6, 2/3} × the three
  windows). σ_tot = √(σ_boot² + σ_sys²). The same M_fit is the LG's flow mass.

## 3. Statistics and verdict (frozen)
- For each model mass M_X and footing: R0_pred(M_X); **Z = (R0_pred − R0_meas)/σ_tot** (primary: w = −1, point mass, f31 = 2/3,
  window [0.6, 2.5]).
- **NOT DIAGNOSTIC** if σ_tot / R0_meas > 0.116 (i.e. the flow cannot tell a factor-2 mass at 1σ_lnM ≈ 3 σ_R0/R0 > ln2/2).
- Otherwise for F-M1 on BOTH footings: **CONSISTENT** iff |Z| < 2; **TOO MASSIVE** iff Z ≥ 2 (labelled marginal if Z < 3);
  **TOO LIGHT** iff Z ≤ −2 (marginal if > −3). Mixed footings → report both, verdict = the weaker.
- Robustness (reported with the verdict, does not change it): Z under the profile variant, DESI w0wa, and against the published
  R0 0.96 ± 0.03 with σ = √(0.03² + σ_sys²); the flow mass against the published masses (K09, P14, P16 including the LMC — the
  declared LMC systematic) as ratios.
- **Timing agreement:** the LG weighing via R0 AGREES with the CFG522 timing mass iff |ln(M_fit / M_F-M1)| ≤ 2 σ_lnM,
  σ_lnM = 3 σ_tot / R0_meas (from R0 ∝ M^(1/3)); otherwise DISAGREES, with the sign. The same is reported for the ΛCDM timing mass
  (the timing-vs-flow mass tension is known in ΛCDM too; it is scored, not assumed).
- Reported (not judged): the Hubble-flow slope just outside, a straight-line fit of V_r on R over [R0_meas, 2.5] Mpc in data vs the
  model's mean slope over the same range for F-M1 and ΛCDM; the post-hoc common f_ret the flow mass implies,
  f = 5.364 M_b / (M_fit − M_b) with M_b = 1.8e11.

## 4. Controls (must pass before the verdict is read)
- K1: with Λ = 0 the integrator reproduces the Lynden-Bell closed form R0³ = 8 G M t0² / π² to 0.5%.
- K2: the solved ΛCDM timing mass, re-integrated forward, returns v_r = −109.3 km/s to 0.1 km/s (radial) at D = 770 kpc. Reported
  beside it: the radial v_r of the CFG522 M1 total as a point mass at 780 kpc vs CFG522's extended-profile `M1.canonical.full.v_radial`
  (the difference is the extended-profile effect; not judged).
- K3: injection–recovery: a mock sample at the observed R_i with v = v(R_true; M_inj) + N(0, 35 km/s), R_obs = R_true (1 + 0.05 N),
  M_inj = the F-M1 mass, 50 mocks: median recovered R0 within 3% of the injected R0, and the mean Z of the injected mass against
  the mock measurement |Z| < 1 (the test can pass).
- K4: the projection reproduces FP11's selection-independent check: f31 = 0.63 linear fit of V_r on R over 0.7–3 Mpc for all
  UNGC galaxies passing the distance cut is reported beside FP11's committed 1.050 / 1.048 Mpc (reported; different selection).

## 5. MUTATE (CFG548_MUTATE=1, writes *_MUTATE.* files; each must behave as stated)
- T1: Λ = 0 shifts R0_pred at fixed M by the amount the closed form gives relative to the Λ run (the Λ-run/closed-form ratio is
  printed; T1 passes iff the Λ = 0 run equals the closed form to 0.5% AND R0(Λ) < R0(Λ = 0) at fixed M).
- T2: M_LG × 0.3 (F-M1 × 0.3) must FAIL: Z ≤ −2 (TOO LIGHT).
- T3: shuffled distances (R permuted among galaxies, 200 permutations, seed 548): the V_r–R Pearson correlation must collapse
  (median |r| < 0.2 vs the real one) and the likelihood at M_fit must drop by Δ ln L ≥ 10 in at least 95% of permutations.

## 6. Pre-freeze disclosure (dated 2026-10-09)
Before freezing I read FP11's committed UNGC linear fits (R0 ≈ 0.98–1.05 Mpc, f31 0.5–0.67), XR4/k02's record (plain law on
the baryons gives R0 ≈ 1.9–2.2 Mpc; a Newtonian point mass 3.18e12 gives 1.176 Mpc in k02's pipeline), and made a hand estimate
that 5.85e12 would give R0 ≈ 1.4 Mpc (scaling k02's number by M^(1/3)). So I expected F-M1 to come out heavy. The thresholds
(|Z| = 2 / 3, the 0.116 diagnostic line, the windows and selection) were written knowing that and were not tuned to it;
the windows follow FP11's 0.7–3 Mpc range trimmed to avoid other groups.
