# CFG599 FROZEN CRITERIA: merger stopwatch v2 for cold-energy settling (the valid rerun of CFG597)

Date: 2026-10-10. Written and committed ALONE, before any code of this lane has run, before any merger simulation and before
any offset number of this lane exists. Nothing below may be edited after this commit; later changes go in dated disclosures
in the README.

κ = ½ is fitted. The cold energy's mass is still required (its amount is an input). No dark-matter particle is added. The
theory is not closed. Yardsticks are raw data only: no ΛCDM halo or baseline, no MOND force law, no "excess over ΛCDM". The
gas physics is ordinary hydrodynamics plus one declared sub-grid gas model (§2 M-3b). Nothing here will be phrased as "the
data favour the framework".

## 0. Question and what is measured

CFG597 (e26ea4f48, assessment 83c4952c3) is VOID as frozen: C4 failed (gas-centroid estimator), its α_max was a first-crossing
artefact, M2 failed (collisionless β̄ 0.125 > 0.10), the v0 calibration missed, and its grid gas model stripped the sub's
gas wholesale (d_SG 770–950 kpc against the Bullet's 194 kpc). This lane fixes those six points and asks the same question:
do the lensing/galaxy/gas offsets of the Bullet Cluster and the Harvey+15 ensemble constrain the settling rate α of cold
energy (CFG541 class-A drift toward the round phantom of the CURRENT baryons + CFG544 FIX-2 velocity relaxation, no EFE)?
Is instant re-settling (α = ∞) excluded? Is pure collisionless behaviour (α = 0) allowed?

α is O(1) FREE in the theory (CFG541 §4; THEORY_v1 §5a). This lane MEASURES which grid values of α the data allow. That is
declared here as the measured quantity. The only other constants set from data are the two calibration numbers of §2 M-6
(v0 and the drag efficiency η), both fixed ONCE at α = 0 on the canonical footing and then held for every α and both
footings. Nothing else is adjusted.

## 1. Data (published numbers via the record; no downloads)

D1 Bullet Cluster 1E 0657−56 (z = 0.296), from the record's transcription of Clowe et al. 2006 (ApJ 648, L109) Table 2 in
   `opus_48_extended_research/reviews/bullet/bullet_data_table.py` (exec'd read-only, as in CFG597):
   galaxy (BCG) – plasma offsets recomputed from the Table 2 coordinates (sub ≈ 194 kpc, main ≈ 209 kpc); BCG–BCG ≈ 720 kpc;
   κ peaks ~2″ (8.8 kpc) from their BCGs. f_obs = 8.8/d_SG,sub = 0.045 (sub; taken toward the gas, the conservative sign),
   σ_f = 1/8 = 0.125 from the quoted 8σ lensing–plasma offset (PROVISIONAL: reads a significance as a positional error).
   Bulk speed ≈ 2700 km/s at the observed epoch (Springel & Farrar 2007 as quoted in the record script).
   Masses: M200 main 1.5e15, sub 1.5e14 M☉ (the record script's line), as CFG597.
D2 Harvey et al. 2015 (Science 347, 1462): β = −0.04 ± 0.07 (record L370/L371). Wittman+18's critique is noted, not used.
D3 Other systems at sign level only, PROVISIONAL, recalled, not scored (as CFG597 §1 D3): MACS J0025 (lensing on galaxies),
   El Gordo and the Musket Ball (lensing nearer the galaxies, TSP ~0.5–0.9 Gyr), Abell 520 (disputed dark core on the gas).

## 2. The model (CFG597 §2 unless changed here; every change is listed)

Units kpc, Gyr, M☉; G = 4.4985e-6. Footings a₀ = 9.3603e-11 and 1.1312e-10 m s⁻², never pooled. Kernel: the same
ν(y) = 1/(1 − e^(−√y)) CFG597 used (THEORY_v1 A1 exponential form). Candidate B, G9 (only real mass gravitates), no EFE.

M-1 Grid and gravity: unchanged (6.4 × 3.2 × 3.2 Mpc, 50 kpc cells, isolated FFT Poisson, CIC, KDK leapfrog).
M-2 Grid gas: unchanged (adiabatic Euler, MUSCL-minmod, Rusanov, RK2, CFL 0.3, tracer per progenitor, floor 1e-4).
M-3 Progenitors: unchanged (M_b = M200/6.73; gas 0.87 M_b, stars 0.13 M_b; gas β-model β = 2/3, r_c = 0.1 r200; stars NFW
    c = 4; truncation r_t = min(r200, 1.2 Mpc)), except M-3b.
M-3b FIX (6), the sub's cool core (declared sub-grid gas model). The Bullet's sub carries a dense, low-entropy cool core (the
    X-ray "bullet") that a 50-kpc grid cannot resolve, which is why CFG597's grid stripped it wholesale. Here a fraction
    f_cc = 0.15 of the SUB's gas mass is a cool core represented by Lagrangian gas parcels ("cloud" particles, N = 40,000):
    Plummer profile, a_cc = 50 kpc, truncated at 300 kpc, sampled with the isotropic Jeans dispersion in the progenitor's total
    potential (its pressure support). The other 0.85 of the sub's gas stays on the grid as the β-model above, hydrostatic in the
    total potential including the core. The main cluster has no cloud (grid only, as CFG597).
    The cloud parcels feel gravity and ram-pressure drag from the grid gas:
        dv/dt = −η ρ_gas |Δu| Δu / Σ_cc,   Σ_cc = M_cc / (π a_cc²),   Δu = u_cloud,local − u_gas,local,
    where u_cloud,local is the CIC-smoothed mean cloud velocity at the parcel (so the parcels' dispersion does not cause drag),
    ρ_gas and u_gas are the grid gas at the parcel (CIC). η = ½ C_d × (effective area / π a_cc²) is the drag efficiency. The
    update is the exact solution of the quadratic drag over a step, applied as the same Δv to every parcel's velocity in its
    local bulk; the momentum lost is deposited on the grid gas momentum and the kinetic energy lost on the grid gas total
    energy (CIC), so momentum and energy are conserved. Buoyancy, ablation and mixing of the cloud are neglected (declared).
    The cloud is sub baryons everywhere: in Σ_tot, in the sub's gas map, in the phantom target of the sub, in the OU Jeans mass.
    Plausible range of η: [0.1, 2.5] (blunt-body C_d 0.5–1.2, area factor 0.5–4 for ram-pressure flattening).
M-4 Cold energy: case L only (the round-rule phantom of the progenitor's own baryons, now including the cool core, truncated at
    r_t). Cases U, rule 1S and the 4:1 ratio are OUT OF SCOPE for this lane (compute); this is a limitation, stated.
M-5 Settling dynamics: unchanged from CFG597 (per-progenitor phantom of the CURRENT baryons about the progenitor's iterated
    baryon centre, round rule, no EFE; mobility region = whole box; rule 2S deficit d = ρ_ph − ρ_c; drift v_s = −α τ ∇ψ with
    τ = (4πGρ_m)^(−1/2); displacement cap 0.5 cell per step, capped fraction reported; FIX-2 OU at rate α/τ toward the local mean
    cold velocity with the isotropic Jeans target per bound region; α = 0: no drift, no OU; α = ∞: the settled cold energy IS the
    phantom of the current baryons at every step).
    FIX (2): α nodes {0, 0.03, 0.1, 0.3, 1, 3, 10, ∞}, every node run on both footings (16 production runs).
M-5b Particle numbers (FIX 1, more star particles): stars 160,000 (main) / 100,000 (sub); settled cold 200,000 / 100,000;
    cloud 40,000. Seed 599 for every run (the calibration runs reproduce the α = 0 run's start exactly).
M-6 FIX (5) Calibration by bracketed bisection, α = 0, canonical footing, 10:1 L, initial separation 2.3 Mpc (as CFG597):
    K1 speed: the galaxy-centroid relative speed at the observed epoch (first post-pericentre time at which the sub–main galaxy
       separation reaches 720 kpc; speed = central difference of that separation over the diagnostics bracketing it) must lie in
       2700 ± 200 km/s. Bisection in v0 on [0, 4000] km/s (stop inside ±100 km/s, or at the best iterate after 8 steps), at the
       current η (first stage η = 1). If v0 = 0 already exceeds 2900 km/s, K1 FAILS (infeasible start).
    G1 gas geometry: the sub gas–galaxy separation d_SG at the same epoch must lie in 194 ± 50 kpc. Bisection in log η on
       [0.03, 10] with v0 fixed (stop inside ±25 kpc, or at the best iterate after 8 steps; d_SG assumed to increase with η).
    Then K1 is re-checked at the final η; if it fails, the v0 bisection is redone at the final η and G1 re-checked (at most two
    rounds). The calibration PASSES iff, at the final (v0, η), K1 is inside ±200 km/s AND G1 inside ±50 kpc AND η lies in the
    plausible range [0.1, 2.5]. Otherwise every verdict is VOID.
    The alt footing uses the same (v0, η); its α = 0 run must also give d_SG in 194 ± 50 kpc and speed in 2700 ± 200 km/s,
    else the alt-footing cells are VOID (reported, not scored).
    Runs end 0.8 Gyr after pericentre.

## 3. Observables

O-1 Projected maps along z on a 12.5-kpc pixel grid. FIX (1): grid gas is projected by summing columns on the 50-kpc grid and
    bilinearly interpolating the column density onto the pixel grid, then renormalising to the exact column mass (a
    mass-conserving, CIC-equivalent projection; no block-repeat). Particles (stars, cold energy, cloud) are CIC-deposited.
    Σ_tot = gas + cloud + stars + all cold energy (the lensing map). The sub's gas map = its tracer-weighted grid gas + its cloud.
O-2 One peak estimator for all three positions, FIX (1)+(3): the shrinking circle. From a start point, iterate: centre ←
    mass-weighted centroid of the map within radius R about the centre; R ← max(0.85 R, R_min); once R = R_min, iterate to
    |Δcentre| < 0.1 kpc (max 200 iterations). Primary R0 = 300 kpc, R_min = 50 kpc.
    - galaxy: the progenitor's star map, started at the median of its star particles;
    - gas: the progenitor's gas map, started at the MASS-WEIGHTED centroid of that map within 600 kpc of the galaxy position;
    - lensing: Σ_tot, started at the galaxy position.
    Convergence check (lensing): the peak is recomputed with (R0, R_min) = (300, 35), (300, 75), (200, 50), (400, 50); the spread
    is the largest distance from the primary peak. The lensing peak is STABLE at an epoch iff spread ≤ max(20 kpc, 0.1 d_SG).
    No aperture-difference error enters any score (CFG597's σ_num is dropped).
O-3 β(t) = (x_lens − x_gal)·ê_SG / |x_gas − x_gal| for the sub, ê_SG the unit vector from galaxies to gas. Pericentre = sign
    change of the sub–main galaxy separation.
O-4 Bullet statistic f = β of the sub at t_obs (the epoch of M-6 K1), linearly interpolated between the bracketing diagnostics
    (every 0.01 Gyr). The node is SCORABLE for the Bullet iff the lensing peak is stable at both bracketing diagnostics.
O-5 FIX (4) Harvey statistic: β̄ = mean of the sub's β over diagnostics with t − t_peri ∈ [0.1, 0.6] Gyr (the ±0.1 Gyr around
    pericentre is excluded), using only epochs with d_SG ≥ 50 kpc and a stable lensing peak. SCORABLE iff at least 10 such epochs
    and at least half of the window's epochs qualify. The window is PROVISIONAL (Harvey's merger ages are unknown).

## 4. Scores and verdicts (frozen)

S-1 Z_B = (f − 0.045)/0.125. Z_H = (β̄ − (−0.04))/0.07. No numerical error inflation.
S-2 FIX (2): every node is reported with Z_B and Z_H on both footings. A node is ALLOWED on a footing iff it is scorable and
    |Z_B| < 2 and |Z_H| < 2; EXCLUDED iff scorable and not allowed; UNSCORABLE otherwise (neither). The allowed set is the list
    of allowed nodes. No α_max, no interpolation between nodes, no endpoint substitution.
V-1 INSTANT RE-SETTLING (α = ∞) is EXCLUDED iff Z_B ≥ 3 on both footings; otherwise NOT EXCLUDED. Z_H at α = ∞ is reported
    alongside.
V-2 PURE COLLISIONLESS (α = 0) is ALLOWED iff the α = 0 node is ALLOWED on both footings; otherwise NOT ALLOWED.
V-3 Galaxy-side compatibility (CFG558: the MW settles within its age for α ≳ 0.5 and keeps its edge at α ≳ 1; the causality
    bound α ≲ 1 of THEORY_v1 §5a): COMPATIBLE iff the node α = 1 is ALLOWED on both footings; PARTIAL iff α = 1 is not, but
    some node in {3, 10, ∞} is allowed on both footings (outside the causality bound); INCOMPATIBLE iff no node α ≥ 1 is
    allowed on both footings. (No grid node lies in [0.5, 1).)
V-4 Summary of what cold energy must be in mergers: α = 0 allowed and α = ∞ excluded → a collisionless component that
    re-settles slowly, with the allowed nodes listed; α = ∞ not excluded → the merger data do not separate "locked to baryons"
    from "collisionless"; α = 0 not allowed and no node allowed → NO α works (a real failure, said so).
D3 sign level: predicted sub β at TSP 0.5 and 0.7 Gyr per node (canonical), reported, not scored.

## 5. Controls (all must pass, else every verdict is VOID; the merger grid is not run until C1–C6 pass)

C1 Poisson: Hernquist force on the padded grid ≤ 3% at r ≥ 3 cells (as CFG597).
C2 Hydro: Sod tube L1 density error ≤ 3% at 200 cells (as CFG597).
C3 Round phantom vs CFG541 E7 analytic Hernquist phantom ≤ 1% at 0.1–2 a (as CFG597).
C4 Isolated halos, FIX (1): (a) estimator at t = 0: on the exactly centred isolated main and sub, the gas, galaxy and lensing
   peaks lie within 3 kpc of the true centre; (b) isolated main and isolated sub (with its cloud), each L-2S, α = 1, canonical,
   evolved 0.6 Gyr: at every diagnostic the gas–galaxy and lensing–galaxy distances are ≤ 15 kpc, and M(<300 kpc) drifts ≤ 10%.
C5 Conservation: drift and OU leave the settled cold mass unchanged exactly; OU conserves cold momentum to ≤ 1e-3 of |p| scale.
C6 Drag unit test (new): a cloud moving through uniform grid gas at rest decelerates as v(t) = v0/(1 + k v0 t) to ≤ 2% over
   one drag time, and the cloud + gas momentum and total energy are conserved to ≤ 1e-6 relative.
K1, G1 (§2 M-6) are controls too.

## 6. MUTATE (separate outputs, `_MUTATE` suffix; M1–M3 must pass, else every verdict is VOID)

M1 α = ∞ (canonical) must put lensing toward the gas: f ≥ 0.5.
M2 FIX (4) α = 0 (canonical), the collisionless baseline: |f| ≤ 0.25 AND β̄ ≤ 0.10.
M3 Gas and galaxy roles swapped (hydro + cloud carry 0.13 M_b, collisionless "galaxies" 0.87 M_b), α = ∞, canonical, same
   (v0, η): lensing must sit on the collisionless baryons, f ≤ 0.25.
M4 (reported only) seed noise: α = 0 canonical with seed 600; the changes in f and β̄ are reported.

## 7. Compute and housekeeping

nice -n 10, ≤ 4 processes of 1 thread, < 8 GB in total. Scripts, `.out`, `_MUTATE.out`, results JSON and README in this
folder only; README numbers come from the JSON. CFG597 is used read-only. Commit specific paths only; no push; never rewrite
history. Any deviation forced by run time or numerics is a dated disclosure in the README and does not change the rules above.
