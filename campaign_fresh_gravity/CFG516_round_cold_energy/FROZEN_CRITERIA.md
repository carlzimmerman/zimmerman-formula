# CFG516 FROZEN CRITERIA: the round enclosed-mass rule (RM) for cold energy, stress-tested and generalised

Written and committed alone, before any script for this lane exists and before any RM model is compared with any data.
Offline only: data already on disk; local compute (nice -n 15, <= 4 threads). Nothing is downloaded; data that would be
needed is listed as "needs owner go". κ = ½ is FITTED. Both footings: a0 = 9.36e-11 (canonical) and 1.13e-10 (alt) m/s².
The cold energy's MASS is still required (no particle species is added). Not theory closed.

## 0. Where this starts

CFG514 (results 68494b0bf) found that Bovy & Rix 2013's 43 K_z,1.1(R) values reject the flattened QUMOND phantom
("phantom disc") on McMillan 2017 baryons (Δχ² vs NFW +101 / +167 zero-knob) while the same phantom made spherical
(its MUTATE) sits at +1.9 / +0.1. The reading to be stress-tested: the law fixes the ENCLOSED mass M(<r); the cold energy
(collisionless, σ ~ 145 km/s, CFG484/CFG513) is distributed roundly. CFG514's one result used one baryon model, one RM
definition, and only the Milky Way. This lane asks whether it survives other baryon models, a second definition of
"the law's enclosed mass", and SPARC.

Prior record read first and not redone: the vertical-force front (mi_aqual_mcmillan2017_2026.py, 6fb320dd: full AQUAL
α=2 kernel fits Σ_dyn(1.1) but fails v_c(R0); ν_vert/ν_rad = 1.024), hunt item 34 (algebraic K_z, FAIL +30%),
CFG513 (L172-shape baryons 6.0e10 / 7.3e10; spherical cold energy lowers the in-plane RC 0.5–1.5%), CFG514.

## 1. The rule RM and its two definitions (declared now)

RM: ρ_cold(r) is SPHERICAL, with M_cold(<r) = M_law(<r) − M_b(<r), where M_b(<r) is the baryon mass inside the
sphere of radius r (3-D, from the flattened baryon model). The total field is the flattened baryons' Newtonian field
plus the spherical field G M_cold(<r)/r² (radial). "The law's spherical-equivalent enclosed mass" is ambiguous for a
flattened baryon distribution, so BOTH definitions are run and scored separately:

- **RM-φ (flux / spherically-averaged phantom):** M_law(<r) = M_b(<r) + M_ph(<r), with M_ph(<r) the enclosed mass of
  the full QUMOND phantom ρ_ph = ∇·[(ν_mono(|g_N|/a0) − 1) g_N]/4πG; equivalently ρ_cold = the shell average of ρ_ph.
  (This is CFG514's MUTATE, re-run here on every baryon model.)
- **RM-v (in-plane circular speed):** M_law(<r) = r v_law²(r)/G, where v_law(R) = √(R ν_mono(|g_N(R,0)|/a0) |g_N(R,0)|)
  is the ALGEBRAIC law applied to the Newtonian in-plane radial field of the same 3-D baryon model. So the in-plane speed
  under RM-v is v² = v_N,disc²(R) + v_law²(R) − G M_b(<R)/R. If dM_cold/dr < 0 anywhere (negative cold density), the
  negative-mass fraction inside 30 kpc (MW) / R_last (SPARC) is reported, not hidden.

Comparators, on the same baryons: **PD** = the full QUMOND field (the "phantom disc"); **N** = baryons + spherical NFW
with (M200, c) fitted to the same rotation curve. ν_mono(y) = 1/(1 − exp(−√y)) throughout.

## 2. Part 1 — Milky Way K_z robustness

Data (on disk): Bovy & Rix 2013 Table 3, 43 MAPs, K_z,1.1(R)/(2πG) (real_research/data/mw_kz11_bovyrix2013_table3.tsv),
evaluated at R = R_tab + (8.122 − 8.0) exactly as CFG514. No other K_z data are on disk (the Σ_1.1 column of the same
table is derived from the same fits and is reported for information only, never scored). Rotation curve for every fit:
Eilers+2019 (38 points, σ = stat ⊕ 2%), as CFG514.

Statistic (CFG514's primary, unchanged): χ² over the 43 MAPs with σ_i ⊕ 5% of the measured value.

Baryon models (all declared now):
- **B1 McMillan 2017** Table 3, exactly CFG514's implementation (M_b ≈ 6.64e10).
- **B2 L172 / CFG513 shapes, 6.0e10:** Hernquist bulge 0.90e10 (a = 0.7 kpc); stellar exponential disc 4.03e10
  (R_d 2.6, exponential vertical h_z 0.3 kpc); gas exponential disc 1.08e10 (R_d 6.0, h_z 0.1 kpc).
- **B2b:** B2 with every component scaled to 7.3e10 (CFG513's RC-fitting variant).
- **B3 short disc:** B1 with the thin and thick stellar discs' scale lengths set to 2.15 kpc (Bovy & Rix 2013's
  dynamical disc scale length; RECALLED, unverified) and each disc renormalised to keep its own surface density at
  R0 = 8.122 kpc (so the local column is unchanged and the disc mass rises). Bulge and gas unchanged. This addresses
  CFG514's +4.9σ K_z scale-length issue.

Per baryon model: F0 (baryon amplitude A = 1) and FA (one amplitude A fitted to Eilers+19 by each model's OWN in-plane
v_c: PD, RM-φ and RM-v each get their own A). NFW N refitted per baryon model at A = 1. Both footings.

Rule per cell (baryon model × footing × F0/FA × RM definition): **round beats disc** if χ²(RM) − χ²(PD) ≤ −4.
Reported but not a verdict input: χ²(RM) − χ²(N) and χ²(PD) − χ²(N); exponential scale length h of each model's
K_z,1.1(R) against the data's.

**MUTATE (load-bearing):** a FLATTENED cold distribution carrying RM's enclosed mass: an oblate homeoid
ρ(m), m² = R² + z²/q², q = 0.3, with the mass inside the homeoid of semi-major axis m equal to M_cold,RM(<r = m),
solved on the grid by Poisson. It must REPRODUCE the rejection: χ²(MUT) − χ²(RM) ≥ +4 in every cell where round
beats disc. If it does not in some cell, the K_z discrimination there is not shape-based and that cell's "beats" is
NOT COUNTED (reported as such). Outputs written separately (_MUTATE).

## 3. Part 2 — SPARC: RM vs the full QUMOND field

Sample: CFG4_common-style read of the 175 rotmod files (real_research/data/sparc_data/*_rotmod.dat) and
SPARC_Lelli2016c.mrt (never SPARC_table.txt); Q ≤ 2 (CFG476's sample); all points; Υ_disk 0.5, Υ_bul 0.7.

3-D baryon model per galaxy (declared, the same for every model compared):
- stellar disc Σ_* = Υ_d × SBdisk (piecewise linear in R; constant inside the first point; exponential with the
  table's R_disk beyond the last point); exponential vertical profile with h_z = 0.196 R_disk^0.633 kpc (the SPARC
  convention, recalled).
- bulge: spherical, with M_bul(<r) = Υ_b r V_bul²/G (monotone-cleaned; constant beyond the last point).
- gas: Σ_gas recovered by a non-negative ring inversion of V_gas|V_gas| (thin rings, ring edges at the midpoints
  between data radii plus 4 rings to 1.6 R_last), exponential vertical h_g = 0.1 kpc.
- a scale-free axisymmetric finite-volume grid (CFG514's solver) in units u = R_last/25.
Models at each data radius (all from the same grid baryons): ALG (algebraic law in the plane), PD (full QUMOND in the
plane), RM-φ, RM-v.

Statistic (CFG476's): weighted rms of log g_obs − log g_model, weights (V_obs/e_V)², over all points of all galaxies.
- at a0 fixed at each footing (canonical, alt);
- with a0 FREE (one global value; grid of 31 log-spaced a0 from 5e-11 to 2e-10 + parabolic refinement); κ reported on
  both footings as κ = ½ × a0_fit / a0_footing.

**SPARC rule (record's tolerance, CFG476/477's 0.02 dex):** RM fits SPARC "within tolerance of QUMOND" if its rms is
≤ rms(PD) + 0.02 dex at the canonical fixed a0, at the alt fixed a0, AND with a0 free. κ shift (RM's fitted κ vs PD's)
is reported and NAMED if |Δ log a0_fit| > 0.05 dex (CFG493's kernel term was +0.06–0.09 dex); it is not a verdict input.

Controls (reported; a failure is disclosed and the affected part labelled, never silently dropped):
- **S1** grid baryons reproduce rotmod's V_bar: median per-galaxy rms |V_bar,grid/V_bar,rotmod − 1| ≤ 5%.
- **S2** ALG on grid baryons vs ALG on rotmod V_bar: rms difference ≤ 0.02 dex (the record's RAR reproduced).
- **S3** PD's spherical Plummer control (CFG514 K2) passes in galaxy units.
- **S4** RM-φ's enclosed mass equals PD's flux-enclosed mass to 0.5% (identity).

## 4. Part 3 — edge-on vertical structure (prediction only)

For each SPARC galaxy, PD vs RM (both definitions), at R = 2 R_disk and R = R_last: the midplane vertical frequency
ν_z² = ∂K_z/∂z|_0 and K_z at z = h_z. Predicted ratios: stellar σ_z at fixed scale height ∝ √(K_z), HI scale height at
fixed σ_HI ∝ 1/ν_z. Medians over the sample, split HSB/LSB (SBdisk at R_disk above/below 100 L☉/pc²). On-disk data
that could test it are listed; DiskMass σ_z is expected NOT on disk (CFG492) and this is checked. No verdict.

## 5. Part 4 — consistency (argued, no PM rerun unless essential)

(a) The record's vertical-force front: compare RM's K_z(R0, 1.1) with the AQUAL front's Σ_dyn values. (b) The zero-knob
growth rule (CFG424 engine) sources the phantom on a Mpc/h mesh from a filtered field and conserves M(<r) per catchment:
state whether RM changes the mesh-level source (expected: no, since RM keeps M(<r) and differs only on sub-cell scales).

## 6. Verdict (per RM definition; then overall)

For each definition D ∈ {RM-φ, RM-v}:
- **ROBUST** if round beats disc in EVERY counted cell of Part 1 (4 baryon models × 2 footings × F0/FA) AND the SPARC
  rule passes on both footings and with a0 free.
- **FRAGILE** otherwise, with every failing cell or SPARC clause named.
Overall: **ROUND RULE ROBUST** if both definitions are ROBUST; **DEFINITION-DEPENDENT** (a named form of FRAGILE) if
exactly one is; **FRAGILE** if neither.

A cell that the MUTATE does not reproduce is not counted as a win; if that leaves fewer than all cells, the definition is
FRAGILE (named "not shape-based in cell X").

The MUTATE run as a whole must DETECT: exit 1 when every counted RM cell's homeoid sits ≥ +4 above RM.
