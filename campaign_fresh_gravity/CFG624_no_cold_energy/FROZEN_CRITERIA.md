# CFG624 FROZEN CRITERIA: "NO COLD ENERGY" (NCE)

Committed alone, before any CFG624 script exists or any gate number is computed. Owner request (chat, 2026-10-11): run the
framework with cold energy removed completely, IN ADDITION to the candidate-B (cold-energy settling) programme. No existing
lane is modified. κ = ½ is FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) m/s², never pooled. The cold
energy's mass is still required by candidate B; this lane asks what happens without it. No dark-matter particle of any kind
is added. Not "theory closed".

ID check: `ls campaign_fresh_gravity | grep CFG624` empty; `git log --oneline -20` has no CFG624 (latest lanes CFG623, CFG700).

## 0. The model under test (NCE)

- **Matter:** baryons only (Ω_c = 0). Neutrinos as in the engines (none). Photons only where a Boltzmann code is used.
- **Gravity:** the law g = ν(g_N/a₀) g_N with the REPAIRED ν_mono (the PM-engine kernel, cfg527_pm.py lineage = CFG4_common),
  a₀ = κ c √(G ρ_DE), flat in z (w = −1). With no cold energy the law's phantom is NOT a substance; it is gravity (QUMOND form,
  sourced by the baryons). No supply edge, no catchment, no cap, no compensation: those exist only to budget cold energy.
- **No EFE** (R7, unchanged).
- **The switch (A5).** Two branches, scored separately, never pooled:
  - **NCE-S (primary):** A5 kept: the law acts only where the engine's own bound-region switch is on (CFG359 T1 tidal switch,
    ε = 0.077, turnaround threshold Δ_ta(z) recomputed in the NCE background with the engine's own shell ODE).
  - **NCE-E (second branch):** A5 dropped: the law acts everywhere (engine switch "S1").
  For static, bound objects (G1–G4) the two branches coincide.
- **Background.** H0 = 67.36, ρ_DE held at the engines' value (Ω_Λ = 0.68623) because a₀'s footings are tied to ρ_DE (A2);
  Ω_b = 0.02237/h² = 0.04930; curvature fills the rest (Ω_k = +0.2645, open). A flat no-cold-energy universe would need
  Ω_Λ = 0.951, i.e. a₀ × 1.18, which would break both fitted footings; it is NOT run. This background choice is declared, not tuned.
- **What NCE leaves unchanged by construction (declared identity, no gate):** inside galaxies candidate B's settled cold energy
  IS the law's phantom inside the census edge, and for f_ret ≈ 0.1 the edge lies at ≳ 50 r_M (beyond all SPARC R_HI, CFG515:
  "no R_HI lies beyond the edge"; beyond the MW 15–27.5 kpc slope and SLUGGS radii). So central ellipticals (CFG528b), the MW
  outer slope (CFG532b) and isolated-lens inner mass (CFG529/531) are IDENTICAL under NCE and B. Removing cold energy can only
  change: clusters, mergers, pair dynamics (LG), and cosmology (growth, shear, CMB). G1 below confirms the identity numerically.

## 1. Gates (raw data vs the NCE prediction; candidate B from the record shown alongside, same pipeline)

### G1 galaxies: SPARC RAR
- Pipeline: CFG346/CFG487 SPARC harness executed read-only exactly as `CFG515/cfg515_sparc.py` does (SPARC_Lelli2016c + rotmod,
  Υ = 0.61, ok-point weights). NCE = the law with no edge (harness row "C3_one_noedge"); B = the census-edge row.
- Statistic: weighted RAR rms (dex) of log g_obs − log g_pred, both footings; CFG346 S-A3 at R_HI.
- **PASS** iff rms ≤ 0.12 dex AND |rms_NCE − rms_B| ≤ 0.005 on both footings. **FAIL** iff rms > 0.15 on either. Else TENSION.

### G2 clusters: X-COP
- Pipeline: `CFG4_clusters.py` cluster table executed read-only (the record's corrected X-COP audit rows, 12 clusters,
  outermost audited radius ≈ 0.8 R500, ν_mono primary, P2 reported). NCE = M_law = ν(g_bar/a₀) M_b (CFG4's MUTATE reading);
  B = the identity reading max(phantom, cosmic share) (CFG4 H2, 0.946).
- Statistic: η = M_HSE / M_NCE (median ± sd over clusters), the residual (M_HSE − M_NCE)/M_b with its σ on the median, and the
  missing-mass ratio η. Hydrostatic bias b = 0, 0.06, 0.1, 0.2 reported (b > 0 raises M_true).
- **PASS** iff |median η − 1| ≤ 0.20 on both footings (CFG4's own 20% tolerance). **FAIL** iff median η ≥ 1.30 (or ≤ 0.77) AND
  the residual is ≥ 3σ from zero on the median, on both footings. Else TENSION.

### G3 Bullet Cluster
- Pipeline: CFG621's merger machinery (cfg621_sim.py → CFG599/597, imported read-only) in its α = ∞ mode (no cold-energy
  particles; the lensing/gravitating dark field = the round law-phantom of the CURRENT baryons, per progenitor, no EFE), with the
  ONE NCE change: the phantom is NOT truncated at the progenitor's r_t (no supply edge). Config = CFG621's calibrated merger cell
  (v0 2666.7 km/s, η_drag 1.132, seed 599), both footings. Scored with CFG621's frozen `score_run` (f, Z_B = (f − 0.045)/0.125,
  stability T_L; Harvey β̄, Z_H).
- **EXCLUDED** iff the cell is Bullet-scorable and Z_B ≥ 3, on both footings. **PASS** iff scorable with |Z_B| < 2 and |Z_H| < 2.
  Else UNDETERMINED. B alongside: CFG621/622 record (α = ∞ EXCLUDED Z_B +7.86/+8.06; α = 0 UNDETERMINED; v4 VOID).
- Context (no verdict): CFG4 H5 aperture numbers (collisionless projected mass required at the galaxies 4.6× / 4.9× the aperture
  baryons; plasma apertures hold more baryons). NCE's only collisionless matter is stars.
- Disclosed limitation: progenitor gas is set up in CFG599's hydrostatic state, which includes the cold mass; under NCE that gas is
  over-pressured (a consequence of G2, not something to fix).

### G4 Local Group timing + groups
- LG pipeline: `CFG522/cfg522_lg_timing.py` machinery (CFG515/513 constants: M_b,MW 6.0e10, M31 1.2e11, d 780 kpc,
  v_r −109.3 ± 4.4 km/s, v_tan 82.4 ± 31.2, d ± 40) executed read-only; its M3 accelerations (baryons only, law between the pair,
  no EFE): deep-MOND two-body (PRIMARY, momentum-conserving) and test-mass ν_mono (reported). The record's "−109 km/s with
  baryons only" (F68) was computed with FP9's H_Y separator law, not the current law; this gate re-confirms with the current law.
- Background age: NCE age t0 from the NCE background above (primary); the record's 13.80 Gyr (control, must reproduce CFG522 M3).
- Statistic: z_meas (strict radial) and z_full (v_tan 82.4 with σ_D, σ_vt propagated, CFG522 definition).
- **PASS** iff |z_full| < 3 and |z_meas| < 3; **FAIL** iff |z_full| ≥ 3 (or no timing solution); else TENSION; both footings.
- Groups: Tian+26 baryonic Faber–Jackson groups (N 63), the committed CFG543 "C0_noedge" row = the law on baryons with no edge,
  which is exactly NCE; re-read from `cfg543_results.json`. **PASS** iff |Z| < 2 both footings; FAIL iff |Z| ≥ 3; else TENSION.
  B alongside: CFG543 P2 (consistent supply).

### G5 cosmic shear (framework-native, raw KiDS-1000 + DES Y3 ξ±)
- PM engine: a copy of `CFG527/cfg527_pm.py` (`cfg624_pm.py`) with ONLY: Ω_c = 0 (f_b = 1, Om = Ω_b), the NCE background
  E(a) = √(Ω_b a⁻³ + Ω_k a⁻² + Ω_Λ) (also in Δ_ta's shell ODE and the growth factor), ICs from a Boltzmann transfer with Ω_c = 0,
  and a gravitating-field P(k) measurement at each snapshot (diagnostic; no effect on dynamics). Switch T1 (NCE-S) or S1 (NCE-E),
  MIX NOFILT (the law reads unsmoothed baryons, R5), no RES machinery.
- ICs: CAMB (FLAGGED: inherited GR-linear Boltzmann machinery; with Ω_c = 0 it is physics, but GR-linear) at H0 67.36,
  ω_b 0.02237, ω_c 0, Ω_k as above, A_s 2.1e-9, n_s 0.965, no massive ν; baryon P(k, z = 49) imposed directly (amplitude from A_s,
  NOT renormalised to any σ8); growing-mode velocities from the NCE GR-linear growth rate (decaying modes ignored, flagged).
  Seed 359, NSEED 512 (the same white noise as CFG530's L100 runs).
- Boxes: L = 100 Mpc/h, N = 256 (all branches and footings), then N = 512 for NCE-S (canonical, then alt) only if the memory gate
  passes. Memory gate: no 1024³ CFG596 job running and free+inactive memory ≥ 25 GB at launch; ≤ 4 threads, nice 10; a 512³ job
  is stopped if swap grows by > 2 GB. Work files in ../_external_data/cfg624_work.
- Projection: CFG592's native machinery (surveys, published scale cuts, covariance, Hankel transforms, nuisances, NLA IA, fit),
  executed read-only, with the NCE lensing prefactor 1.5 Ω_b (H0/c)² f_K(χ)/a applied to the GRAVITATING overdensity relative to
  the mean baryon density (baryons + phantom; lensing sees the law's phantom), open-universe f_K(χ) in the kernel and in
  k = (ℓ + ½)/f_K(χ), the NCE background distances, NLA IA with Ω_b and the NCE growth. Node spectra: measured P_grav at z = 0,
  0.5, 1 (no held boost needed); z > 1 scaled by the NCE GR-linear growth²; below k_lo the NCE linear shape; above k_hi CFG592's
  own power-law continuation.
- Support cut: CFG592's rule (f ≥ 0.9 of each point's integrand inside [k_lo, k_hi], computed on the NCE spectrum; N_kept ≥ 10).
- Statistic per survey × footing × branch: χ²_min (nuisances profiled, IA marginalised), p = sf(χ²_data, N_kept). B alongside:
  CFG530 LR L100 N512 'F' (held boost, CFG592) and Δχ²(NCE − B) on the NCE kept set when B's support covers it.
- **FAIL** iff p < 0.001 in any scorable survey; **PASS** iff p ≥ 0.01 in every scorable survey; else TENSION; **NOT DIAGNOSTIC**
  iff no survey has N_kept ≥ 10. Verdict per footing and branch; 256³ boxes that keep no points are NOT DIAGNOSTIC by this rule.
- Reported only (no verdict): σ8 of the particle and gravitating fields, P_grav/P_lin, and an all-published-points χ² with the
  power-law continuation (labelled EXTRAPOLATED).
- No ΛCDM yardstick: no HMcode, BAHAMAS, mass function or S0 ratio enters the verdict.

### G6 CMB acoustic peaks
- The framework has no derived law for linear perturbations in the pre-recombination plasma: A5 (the switch) is an input without
  an action, and whether the law acts on unbound linear modes at z ≈ 1100 is not derived. **G6 framework-native verdict:
  UNTESTABLE** (declared now).
- Context only (no verdict): if A5 is read literally (law off where nothing is bound), z ≈ 1100 physics is GR + baryons +
  photons + ν; CAMB (inherited GR-linear) then gives the TT 3rd/1st peak height ratio for Ω_c = 0 in the NCE background. Raw
  Planck TT band powers are NOT on disk (downloading needs owner approval); the comparison values are the published Planck 2018
  peak heights, RECALLED and PROVISIONAL. A CAMB Ω_c = 0.120 run checks only the peak finder (machinery control).

## 2. MUTATE controls (must behave as stated)
- **M-G1:** a₀ → 0 (Newtonian baryons) must FAIL G1 (rms > 0.15 both footings); the census-edge row must reproduce CFG515 (Δrms 0).
- **M-G2:** restoring cold energy (identity reading) must reproduce CFG4's 0.946 / alt value within 1e-9; a₀ → 0 must give
  η = M_HSE/M_b = 1 + 5.73-type Newtonian deficit.
- **M-G3:** the NCE code path with the r_t truncation KEPT must reproduce CFG621's α = ∞ cell (f, Z_B) on the canonical footing
  within 1e-9 (code-path control).
- **M-G4:** with t0 = 13.80 Gyr the M3 numbers must reproduce CFG522 (v −222.6/−241.5 test-mass, −178.0/−194.4 two-body) within
  0.05 km/s; a₀ → 0 (Newtonian baryons) must FAIL (no timing solution or |z| ≥ 3).
- **M-G5:** (a) feeding CFG530 LRcan/LRalt L100 N512 through this lane's projection code with the ΛCDM-engine background must
  reproduce CFG592's χ²_F (40.02 / 45.52 can; 46.21 / 46.87 alt) within 0.01; (b) an a₀ → 0 NCE PM run (256³, canonical,
  Newtonian baryons) is reported; a 512³ a₀ → 0 run only if the 512³ NCE-S run is diagnostic and memory/time allow.
- **M-G6:** the peak finder on CAMB Ω_c = 0.120 must find three peaks at ℓ ≈ 200–230, 520–560, 790–840.

## 3. Rules
- Verify a fail as hard as a win. No new component, constant or tuned parameter to rescue any gate. If a gate fails, the missing
  mass is reported plainly. Externally calibrated ingredients appear only as labelled context.
- Commits with explicit paths; no push; no home paths or personal names in committed files; console logs deleted.

## 4. Pre-flight disclosure (before this file)
- Read the record (THEORY_v1, ASSESSMENT, CFG1, F68, STANDING, CFG4, CFG515, CFG522, CFG543, CFG592, CFG596, CFG599/621).
- One CAMB feasibility call (Ω_c = 0 accepted; it returned Ω_DE 0.68621 and an NCE background age of 17.73 Gyr). No gate
  statistic was computed. Memory at freeze: ~34 GB free, swap 12.3 of 13.3 GB used; CFG596's P1 1024³ job is NOT running (its own
  watchdog aborted it at 10:56 on 2026-10-11 for swap growth, before this lane began).
