# CFG597 FROZEN CRITERIA: cluster mergers as a stopwatch for cold-energy settling

Date: 2026-10-10. Written and committed ALONE, before any merger simulation, any offset number, or any code of this lane has run.
Nothing below may be edited after this commit; later changes go in dated disclosures in the README.

κ = ½ is fitted. The cold energy's mass is still required (its amount is an input). No dark-matter particle is added. The
theory is not closed. Yardsticks are raw data only: neither ΛCDM nor standard MOND enters as a yardstick or as a hidden
ingredient (no ΛCDM halo, no "excess over ΛCDM" baseline, no MOND force law). The gas physics is ordinary hydrodynamics.

## 0. The idea and what is measured

In candidate B the settled cold energy is the law's phantom of the retained baryons, and in clusters those are mostly hot gas.
In a collision the gas is ram-pressure slowed and lags while galaxies pass through. If cold energy re-settled instantly onto the
phantom of the CURRENT baryons, lensing would follow the gas. If settling takes a finite time (CFG541 class-A drift at rate
Γ = α (ρ_c/ρ_m) √(4πG ρ_m), plus CFG544's FIX-2 velocity relaxation at rate α/τ), cold energy first moves collisionlessly with
the galaxies and re-settles toward the gas later. Merger offsets versus time since pericentre therefore constrain α.

α is O(1) FREE in the theory (CFG541 §4; THEORY_v1 §5a). This lane MEASURES the range of α allowed by merger data. It is
declared here as the measured quantity; no other constant is adjusted.

## 1. Data (published numbers; no downloads)

D1 Bullet Cluster 1E 0657−56 (z = 0.296), from the record's verbatim transcription of Clowe et al. 2006 (ApJ 648, L109) Table 2
   in `opus_48_extended_research/reviews/bullet/bullet_data_table.py` (exec'd read-only):
   - galaxy (BCG) – plasma offsets 209 kpc (main) and 194 kpc (sub), recomputed from the Table 2 coordinates;
   - BCG–BCG separation (recomputed) ≈ 720 kpc, which matches the 0.72 Mpc on the sky quoted there;
   - "κ peaks lie ~2″ from their BCGs, within 1σ of the galaxies" and "each κ peak offset from its own plasma ~8σ" (as quoted in
     that script). 2″ = 8.8 kpc at 4.413 kpc/″.
   - Observed fraction f_obs = (lens − galaxy)/(gas − galaxy) along the axis: sub 8.8/194 = 0.045, main 8.8/209 = 0.042
     (the 2″ is taken toward the gas, the conservative sign). σ_f from the 8σ statement: σ_offset = offset/8, so
     σ_f = 1/8 = 0.125. This error derivation is PROVISIONAL (it reads a significance as a positional error).
   - Kinematics: bulk speed ≈ 2700 km/s (Springel & Farrar 2007, MNRAS 380, 911, as quoted in the record script); time since
     core passage ~100 Myr (Clowe et al. 2006 as quoted); 0.1–0.2 Gyr is the PROVISIONAL band.
   - Masses for the model: M200 main ≈ 1.5e15, sub ≈ 1.5e14 M☉ (the record script's "[Springel & Farrar / sims]" line), with a
     4:1 sensitivity run (sub 3.75e14). Paraficz et al. 2016 (A&A 594, A121) strong-lensing M(<250 kpc) 2.5e14 / 2.0e14 is
     quoted as context (it suggests a heavier sub, hence the 4:1 run).
D2 Harvey et al. 2015 (Science 347, 1462): 72 substructures in 30 systems, β = δ_SI/δ_SG = −0.04 ± 0.07 (the record's value,
   L370/L371). Wittman, Golovich & Dawson 2018 (ApJ 869, 104) contest the bound (record CFG1 A09d); reported, not used.
D3 Other systems (sign-level context only, NOT load-bearing; all values recalled and PROVISIONAL):
   MACS J0025.4−1222 (Bradač et al. 2008, ApJ 687, 959; lensing on the galaxies, gas between; TSP ~0.1–0.2 Gyr);
   El Gordo (Jee et al. 2014, ApJ 785, 20; Ng et al. 2015, MNRAS 453, 1531; TSP ~0.5–0.9 Gyr; lensing near the galaxies);
   Musket Ball DLSCL J0916.2+2951 (Dawson et al. 2012, ApJL 747, L42; Dawson 2013, ApJ 772, 131; TSP ~0.7 Gyr; lensing near the
   galaxies, a low-significance galaxy–lensing offset);
   Abell 520 (Mahdavi et al. 2007; Jee et al. 2012, ApJ 747, 96; Clowe et al. 2012, ApJ 758, 128; a disputed "dark core" on the
   gas). If any of these became load-bearing, its table would be listed with size for the owner's go; none is fetched here.

## 2. The framework-native merger model (declared in full)

Units kpc, Gyr, M☉; G = 4.4985e-6 kpc³ Gyr⁻² M☉⁻¹. Footings a₀ = 9.3603e-11 and 1.1312e-10 m s⁻², never pooled. Kernel ν_mono.
Candidate B, G9 (only real mass gravitates: ∇²Φ = 4πG(ρ_gas + ρ_stars + ρ_c)), no EFE.

M-1 Grid and gravity. 3-D box 6.4 × 3.2 × 3.2 Mpc, 50 kpc cells (128 × 64 × 64). Φ and ψ from zero-padded FFT Poisson solves
    (isolated boundary). Collisionless particles: CIC deposit and interpolation, kick-drift-kick leapfrog.
M-2 Gas. Adiabatic Euler equations (γ = 5/3) with gravity, finite volume, piecewise-linear (minmod) reconstruction, Rusanov
    flux, second-order Runge–Kutta, CFL 0.3. No cooling, no viscosity beyond numerical, no magnetic fields. A passive tracer
    marks each progenitor's gas. A density floor of 1e-4 of the main cluster's central gas density.
M-3 Progenitors (each declared from D1). M_b = M200/6.73 (the X-COP Newtonian dark/baryon ratio 5.73 of CFG4, raw data);
    gas 0.87 M_b, stars 0.13 M_b (stars/gas 0.15, PROVISIONAL from the record script's "gas ~10–15%, stars ~1–2% of total").
    Gas: β-model, β = 2/3, r_c = 0.1 r200, hydrostatic in the progenitor's own total potential. Stars: NFW shape, c = 4.
    Every component truncated at r_t = min(r200, 1.2 Mpc) (box limit; declared). r200 uses 200 ρ_crit(z = 0.296) with the
    record's h = 0.7, Ω_m = 0.3 plate-scale convention (a size convention only, no dynamics).
M-4 Cold energy, two initial cases.
    L (PRIMARY; "law profile filled to the supply"): cold energy = the round-rule phantom (CFG541 E7) of the progenitor's own
      baryons, truncated at r_t (the supply edge, ≥ 3 Mpc for these masses, lies outside the box).
    U (SECONDARY; the record's cluster census, CFG4 identity reading / CFG515 unsettled fraction): settled = the same phantom,
      plus an UNSETTLED part with NFW c = 4 shape (CFG432) holding M200 − M_b − M_ph(<r200). The unsettled fraction
      u = M_u/(M_u + M_ph) is reported against CFG515's 0.37–0.63.
    Collisionless components start with isotropic Jeans velocities in the progenitor's total potential (Maxwellian sampling).
M-5 Settling dynamics of the SETTLED cold energy (CFG541 E3–E6 with CFG544 FIX-2).
    - Phantom target: per progenitor (bound region = progenitor, membership tagged at t = 0), ρ_ph,i(r) from M_b,i(<r) about the
      progenitor's baryon centre x_i (mass-weighted centroid of its own baryons within r_t, iterated), round rule, no EFE.
      ρ_ph = Σ_i ρ_ph,i. Mobility region B∩C = the whole box (both progenitors lie inside one turnaround region; overlapping
      catchments share one ψ, R8).
    - Deficit, rule 2S (PRIMARY, FIX-2's two-sided form, CFG544): d = ρ_ph − ρ_c,settled. Rule 1S (SECONDARY, CFG541 E5):
      d = max(ρ_ph − ρ_c,settled, 0). ∇²ψ = 4πG d (isolated).
    - Drift v_s = −α τ ∇ψ, τ = (4πG ρ_m)^(−1/2) from the local total density (grid, floored at the density floor scaled by
      ρ_m/ρ_gas of the IC centre). Displacement capped at 0.5 cell per step (CFG544 practice; the capped fraction is reported).
    - FIX-2 velocity part: Ornstein–Uhlenbeck relaxation at rate α/τ toward the LOCAL MEAN cold-energy velocity (the Galilean-
      invariant reading; relaxing toward zero velocity would brake a moving cluster in an arbitrary frame) with target dispersion
      the isotropic spherical Jeans dispersion of the progenitor's current settled cold density in its current total enclosed
      mass (CFG544's posited FIX-2 target, per bound region, about the progenitor's cold-energy centre).
    - The unsettled part (case U) is ordinary cold matter: no drift, no OU.
    - α ∈ {0, 0.1, 0.3, 1, 3, 10, ∞}. α = 0: pure collisionless (no drift, no OU). α = ∞: instant re-settling, the settled cold
      energy IS ρ_ph of the current baryons at every step (a grid field; rule 2S only).
M-6 Collision. Head-on in the plane of the sky (projection along z). Initial separation 2.3 Mpc. The initial relative speed v0 is
    set once per (mass ratio, case) by an α = 0 calibration run so that the galaxy-centroid relative speed at pericentre is
    2700 ± 200 km/s (D1 kinematics). The same v0 is then used for every α and both footings. Runs end 0.8 Gyr after pericentre.
M-7 Runs. 10:1: {L-2S, U-2S} × 7 α × 2 footings; L-1S × α ∈ {0.1, 0.3, 1, 3, 10} × 2 footings. 4:1: {L-2S, U-2S} × 7 α,
    canonical footing only (sensitivity).

## 3. Observables

O-1 Projected maps (along z): Σ_tot = gas + stars + all cold energy (the lensing map), and the sub's gas (tracer-weighted).
O-2 Centroids of the SUB (the "bullet") and of the main: galaxy = iterative centroid of the progenitor's projected stars (150 kpc
    aperture); gas = iterative centroid of the progenitor's projected tracer gas (150 kpc aperture, started at its projected peak);
    lensing = iterative centroid of Σ_tot in an aperture R ∈ {100, 150} kpc started at the galaxy centroid (maps deposited on a
    12.5 kpc projected grid).
O-3 β(t) = (x_lens − x_gal)·ê_SG / |x_gas − x_gal|, ê_SG the unit vector from galaxies to gas. Pericentre = minimum galaxy-centroid
    separation.
O-4 Bullet statistic: f = β of the sub at t_obs, the first post-pericentre time at which the galaxy-centroid separation reaches
    720 kpc (geometry match, D1). Primary aperture 150 kpc; σ_num = |f(100) − f(150)|. Main reported.
O-5 Harvey statistic: β̄ = time average of the sub's β over 0.05–0.6 Gyr after pericentre (uniform in time; PROVISIONAL window,
    Harvey's ages are not known), using only epochs with |δ_SG| ≥ 25 kpc, from the 10:1 runs (4:1 reported).

## 4. Scores and verdict rules (frozen)

S-1 Z_B = (f − 0.045)/√(0.125² + σ_num²). Z_H = (β̄ − (−0.04))/√(0.07² + σ_num,H²), σ_num,H the 100/150 kpc difference of β̄.
S-2 α is ALLOWED in a (case, rule, footing) cell iff |Z_B| < 2 and |Z_H| < 2. The allowed range is the set of grid α that pass;
    α_max (where Z_B or Z_H crosses 2) is interpolated linearly in log α between grid points and reported.
V-1 INSTANT RE-SETTLING (α = ∞) is EXCLUDED iff Z_B ≥ 3 in L-2S on both footings. Otherwise NOT EXCLUDED.
V-2 PURE COLLISIONLESS (α = 0) is ALLOWED iff it passes S-2 in L-2S on both footings.
V-3 Galaxy-settling compatibility (L-2S, both footings): COMPATIBLE iff α_max ≥ 1 (CFG558: the MW settles and keeps its edge at
    α ≳ 1); TENSION iff 0.5 ≤ α_max < 1 (CFG557/558: settles by 13.8 Gyr at α ≈ 0.5 but the edge spills); INCOMPATIBLE iff
    α_max < 0.5. The causality bound α ≲ 1 (THEORY_v1 §5a) is reported alongside.
V-4 Robustness: the allowed range is ROBUST if L-1S and U-2S give the same verdicts V-1 to V-3 as L-2S; otherwise
    VARIANT-DEPENDENT, with the differing cells listed.
V-5 What cold energy must be: if α = 0 is allowed and α = ∞ excluded, cold energy in mergers is a collisionless fluid that
    re-settles slowly, with the allowed Γ t_obs at the sub's core reported; if α = ∞ is allowed, the data do not distinguish
    "locked to baryons" from "collisionless"; if α = 0 is excluded too, NO α works (a real failure, stated as such).
D3's systems are reported at sign level: the predicted f at TSP 0.5 and 0.7 Gyr against "lensing nearer the galaxies than the gas"
(El Gordo, Musket Ball) and "lensing on the gas" (Abell 520, disputed). Not scored.

## 5. Controls (must pass, else the dependent verdict is VOID)

C1 Poisson solver: the force of a Hernquist sphere on the padded grid matches the analytic force to ≤ 3% at r ≥ 3 cells.
C2 Hydro: Sod shock tube (1-D slice through the same solver), L1 density error ≤ 3% of the exact solution at 200 cells.
C3 Round phantom: the routine reproduces CFG541 E7's analytic Hernquist phantom mass (ν_mono) to ≤ 1% at 0.1–2 a.
C4 Isolated progenitor (main, L-2S, α = 1, canonical) for 0.6 Gyr: galaxy, gas and lensing centroids coincide within 15 kpc;
   total projected mass within 300 kpc drifts ≤ 10%.
C5 Conservation: the drift and the OU step change the settled cold mass by 0 (exactly) and the OU step conserves the cold
   component's total momentum to ≤ 1e-3 of |p| scale.

## 6. MUTATE (separate outputs, `_MUTATE` suffix)

M1 α = ∞ must put lensing on the gas: f ≥ 0.5 in L-2S (canonical). If not, the machinery cannot see settling and the lane's
   verdicts are VOID.
M2 α = 0 with no baryon coupling (no drift, no OU): the collisionless expectation, |f| ≤ 0.25 and β̄ ≤ 0.10 (canonical, L).
M3 Gas and galaxy roles swapped (the hydro fluid carries 0.13 M_b, the collisionless "galaxies" 0.87 M_b), α = ∞, L-2S canonical:
   lensing must now sit on the collisionless baryons, f ≤ 0.25 (the offsets flip relative to M1).

## 7. Compute and housekeeping

nice -n 10, ≤ 4 processes of 1 thread, memory well under 8 GB. Scripts, `.out`, `_MUTATE.out`, results JSON and README in this
folder only; numbers quoted in the README come from the JSON. Commit specific paths only; no push; never rewrite history.
Deviations forced by run time or numerics are disclosed in the README with a date and do not change the rules above.
