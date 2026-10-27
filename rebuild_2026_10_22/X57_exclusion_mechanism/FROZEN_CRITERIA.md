# X57_exclusion_mechanism: FROZEN CRITERIA (committed alone, before any script or number)

κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11, alt 1.1312e-10 m/s², never pooled. **Cold dark energy** is the
gravitating w ≈ 0 clumping field component paired with dark energy; it is not matter and not a particle. ΛCDM is the
external rival. No dark-matter particle. Framework-native inputs only (no ΛCDM-derived inputs). Not "theory closed".
Nothing here may say the data favour the framework; results are phrased "this test …".

Lane id: X50–X56 are taken and X58 is the peer's `X58_object_keyed_switch` (frozen 9964127dfd), so this lane is X57.
Two coordinator instructions arrived before this file was written and are folded in here (no amendment needed):
(i) the R4b line (law on cluster baryons vs X30's OUTER band) is graded explicitly for every class that leaves the law
acting on cluster baryons; (ii) M5 is **reported only** (the operational switch is the peer's X58; X58 is cited for its
numbers, M5 is not graded on data here; only its action form is examined).

## Question (the owner's)

What keeps full-strength cold dark energy out of galaxies, and mostly out of cluster outskirts, without heating it and
without converting it?

## 1. Requirements (record results; every number re-read from committed JSON / .out in Step 0)

| # | requirement | number(s) graded against | source (committed file) |
|---|---|---|---|
| R1 | Dust-like by z ≈ 5×10⁴; clusters linearly like dust; passes the Lyman-α forest down to λ_hm ≈ 0.42 Mpc/h at z = 2–3 | X34 z_on allowed 5e4 (R1 turn-on, EXCLUDED at 2e4); X22 α_NF 0.02991 Mpc/h, λ_hm 0.4167 Mpc/h, M_hm 4.89e9 M☉; X22 `forest_class` rule (FAIL if T²(k5) < 0.9 or any L346 bin outside [0.5, 2.0]) | `X34_recombination_release/x34_recombination_release_results.json` (Q1_summary.R1); `X22_cosmic_dust_window/x22_cosmic_dust_window_results.json` (step1), `.py` L154–161 |
| R2 | Full amount today; no exchange with dark energy | ξ ∈ [−0.0035, +0.0011] (95 %, DES-SN5YR; PP / U3 same class); Ω_m BAO 0.2970, BAO+PP 0.3039 | `X54_cold_de_exchange/x54_cold_de_exchange_results.json` (analysis.C_DES5.int95, S0.CFG681) |
| R3 | Galaxies hold almost none inside R_last | f_max 0.196 (canonical) / 0.0269 (alt) of the fair share; tolerated M_c(<R_last)/M_b median 0.0354 / 0.0049; SPARC R_last median 11.27 kpc, V_last median 99.7 km/s | X22 step2 (from X6's d2 line) |
| R3b | Lens environments to ~1 Mpc: the law beats route-E halos; one halo mass cannot fit both | X53 Δχ²(H2H − L2H, all radii) = 583.91 − 154.34 (canonical), 580.63 − 125.08 (alt); X55 n_sep 4.55 / 4.26σ | `X55_one_halo_mass_for_both/x55_one_halo_results.json` (step0_X53, footings.*.n_sep) |
| R4 | Cluster cores hold a concentrated cold component, about 0.6–0.7 × the gas | X43 G-MID-T3 Z +0.30 (canonical, h 0.672); X43 groups Z +2.05; law-alone MID T3 under-predicted (Z +4.46 / +4.11, X56's law copy of X43) | `X43_collapse_core_floor/x43_collapse_core_results.json`; `X56_law_floor_structure/x56_x43copy_law_x48_results.json` |
| R4b | Cluster outskirts at 1.4–3 Mpc below the law | X30 OUTER all-KT 0.716 ± 0.141 (canonical h 0.672) / 0.656 ± 0.129 (alt); **law alone on cluster baryons: G-OUT-all pred 0.999, Z −2.01 / −2.14 (canonical, h 0.672 / 0.686), −2.66 / −2.80 (alt)**; X43 line |Z| ≤ 2.0 | `X56_law_floor_structure/x56_x43copy_law_x48_results.json`; `X30_sheet_cluster_profile/README.md` |
| R5 | No heating, no conversion | X23 ×2, X24b, X26, X30 (thermal routes closed); X37, X54 (conversion) | V3S_FINAL_VERDICT §8 |
| R6 | Object-keyed, not local | X47: as a local rule the tether FAILS at growth / data, as an object rule it is CONSISTENT but nonlocal (verdict, verdict_VT_O); X19: no catalogue selector; CFG944 Theorem G; X22 step 3C: x and ρ_b do not separate the cosmic medium from SPARC | `X47_vacuum_tethered_core_floor/x47_vt_floor_results.json`; X22 step3C |
| R7 | Bullet: the cluster's cold component travels with the galaxies | X32: a dust-like tracer keeps f_ret 0.80–1.02 and lands on the galaxies | `X32_bullet_cold_sector/x32_bullet_cold_sector_results.json` (passages_reported.CDMlike) |

Source text: `covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md` §8 (X22, X23, X24b, X26, X30, X32, X34,
X47, X53, X54, X55, X56 entries) and `rebuild_2026_10_22/COLD_SECTOR_SPEC_2026-10-24.md` §1, §6.

## 2. Step 0 (stop rule)

Reproduce from committed JSON / .out, exactly (|dev| ≤ 1e-9 relative on JSON floats; printed values to their printed
digits): X22 α_NF, λ_hm, f_max (both), tolerated M_c/M_b medians, R_last / V_last quantiles, capture median 0.7603,
content 0.5405, grms at z = 2, 3; X34 z_on allowed / excluded; X54 ξ int95 (three SN sets), CFG681 Ω_m; X53 Δχ² via X55's
step0 (both footings, all radii); X55 n_sep; X30 OUTER all-KT measured ± σ (both footings, via X56's law copy); X56 law
copy G-OUT-all pred and Z (4 cells); X43 G-MID-T3 Z and groups Z; X40b g_b(r₀)/a₀ for T1–T3 (both footings); X32
dust-like tracer f_ret. Also: my two-fluid ODE at β = 0 (X22's equations, X22's IC a_i = 1e-3, δ_b = δ_c) must give X22's
C2 value δ_m(z = 0) = 0.787089 within 1e-5. **If any Step-0 item fails, stop: no class is graded.**

## 3. Mechanism classes and how each is graded

Common premise (all graded classes): the fundamental law acts on baryons (the reading X53 / X55 prefer for galaxies),
and cold dark energy is a separate gravitating component whose gravitating (lensing) mass density is ≥ 0. Each class
must keep cold dark energy out of galaxies (R3) without heat or conversion (R5).

Grade per requirement: PASS / FAIL / NOT DECIDABLE (ND) / by construction (BC). Per footing.

### M1 Sector-dependent coupling (cold dark energy feels GR only; baryons feel the law)
- R1: cold dark energy's own linear growth is GR dust → BC PASS (X22 C2 machinery).
- **R3 (decisive):** with no non-gravitational term the cold component collapses on its own Lagrangian scales (X22
  A3: M_L/M_hm median 9.5). Graded number: the generous lower bound on its content inside R_last is X22's
  virial-heated hydrostatic content 0.5405 of the fair share (any less-heated state holds more; X22's frozen-cut capture
  is 0.7603). FAIL if 0.5405 > f_max.
- R4: BC PASS (cores retained). R4b: graded by the common line (§4). R7: BC PASS (collisionless dust).

### M2 Repulsive baryon–cold dark energy Yukawa force (source = baryon mass density; strength β × gravity; range λ, physical)
Force between a baryon element and a cold element: −G m m′/r² × [1 − s β (1 + r/λ) e^{−r/λ}], s = +1 (repulsive).
Baryon–baryon and cold–cold gravity are unchanged.
- **R1:** X22's two-fluid ODE with the cross-coupling (1 − s β_eff) in both equations, β_eff(k, a) = β / (1 + (a/(k h λ))²)
  (k in h/Mpc, λ in physical Mpc, h = 0.674 as X22). Grade on the **gas** transfer T_b(k, z) = δ_b/δ_b,ref (the forest is
  gas), with X22's `forest_class` on t² = sign(T_b) T_b² over the L346 bins and k5 at z = 3 and 2. Allowed = not FAIL
  (X22's verdict-bearing α_NF convention). The δ_m grade is reported. For each λ on a log grid 1e-4 … 10 Mpc (41 points)
  find β_max^R1(λ) (bisection in log β over 1e-4 … 1e4, after confirming monotonic FAIL-onset on a coarse grid).
- **R3 (necessary, generous to M2):** static force balance at the median SPARC R_last with the tolerated cold content:
  β ≥ β_min^R3(λ) = (1 + μ) e^{x}/(1 + x), x = 11.27 kpc/λ, μ = 0.0354 / 0.0049. (Assembly against the fair-share self-gravity,
  β (1 + x)e^{−x} ≥ 1 + 5.364, is reported.)
- **R3b:** the same with μ = 0 at R = 1 Mpc (the lens environment, X55).
- **Interval statement:** the class is EXCLUDED BY R1∩R3 if β_max^R1(λ) < β_min^R3(λ) at every λ on the grid; the
  reported number is max_λ [β_max^R1/β_min^R3]. Same for R1∩R3b.
- R4 (only if R1∩R3 is non-empty): smooth-gas Yukawa potential 4πG β λ² ρ_gas vs σ² in a cluster core (ρ_gas = 3.4e-4
  M☉/pc³ ≈ 1e-2 cm⁻³, σ = 1000 km/s, stated as an illustrative core, not a fit); PASS if ≤ 0.1.
- Equivalence principle: derived statement only (no external number used; see ledger A9).
- R4b common line. R7 ND.

### M3 Repulsion from the law's own field (cold dark energy pushed out where x < 1)
Cold dark energy feels an outward acceleration s g_ph with g_ph = (ν(y) − 1) g_N,b, y = g_N,b/a₀, ν = X22's `nu1`
(the law's phantom), s = +1 (out). Two readings of where the law acts:
- (L) the law acts on any baryon field with x < 1, including linear perturbations. **R1 (decisive):** ratio
  Q(z) = s (ν(f_b x_lin) − 1) f_b/f_c of phantom repulsion to cold self-gravity in the linear regime at z = 2 and 3, with
  x_lin = X22's record-method rms linear peculiar gravity / a₀ (grms 3.83e-12 / 5.15e-12 m/s²), f_b = 1/6.364. FAIL if
  Q ≥ 1 (cold dark energy is net repelled by linear baryon perturbations and does not grow).
- (V) the law is off on linear perturbations (v3s with no khronon charge, X35). Then x < 1 holds in both the linear
  medium and in galaxies (X22 step 3C: x does not separate), so the activation key is not x: M3 becomes an object key and
  falls under R6 (Theorem G). Graded: R6 FAIL as a local class (reported: it moves to M5).
- **R4 (decisive under either reading):** cluster cores have x_b(r₀) = 0.048–0.073 (X40b T1–T3), inside SPARC's R_last
  range x = 0.025–0.24 (X22). FAIL if the cluster range lies inside the SPARC range on that footing: any x-keyed repulsion
  that empties galaxies empties cluster cores.
- Sign and object scale are reported: the radius beyond which the phantom repulsion beats the fair-share cold
  self-gravity, r* = 5.364 √(G M_b/a₀), for the median SPARC M_b.
- R4b common line.

### M4 Wave / coherence scale of the field (field-energy parameter ν_w in m²/s; never a particle mass)
Linear term −(ν_w²/4) k_phys⁴ δ_c in the cold equation of X22's ODE.
- **R1:** ν_w,max = the largest ν_w whose δ_m transfer is not FAIL under X22's `forest_class` (as X22 grades its cuts).
- **R3 (generous):** exclusion radius r_w = full de Broglie length 2π ν_w/V_last per SPARC galaxy. PASS only if
  r_w(ν_w,max) ≥ R_last for at least half of SPARC. Reported: median r_w/R_last; ν_w,need = R_last V_last/2π (median);
  interval statement ν_w,need vs ν_w,max.
- R4: r_w in a σ = 1000 km/s cluster vs X38's core size 0.27–0.44 Mpc: PASS if r_w ≤ 0.27 Mpc (cores keep cold dark
  energy). The sign of the mass scaling (r_w ∝ 1/V) is reported.
- R4b common line. R7 BC PASS.

### M5 Halo-scale (nonlocal) exclusion keyed to the bound object — REPORTED ONLY (coordinator, pre-freeze)
No data grade. Examined: which action forms could implement an object-level switch, and whether CFG944 Theorem G and the
μ-pincer allow them. X58_object_keyed_switch (peer, frozen 9964127dfd) is cited for operational numbers, if committed by
the time of this lane's README; otherwise "pending".

### M6 Displacement (anticorrelated, compensated initial conditions)
Compensated patches: ρ_b δ_b + ρ_c δ_c = 0, with δ_c,in = −(1 − f_max) in the galaxies' Lagrangian patches.
- **R2 / positivity (decisive algebra):** with baryon density ≥ 0 outside, the depleted Lagrangian volume fraction is
  bounded: f_V ≤ 1/(1 + r(1 − f_max)), r = 5.364; at the bound every baryon sits in the depleted patches. Reported.
- **R1 forest:** frozen (non-growing) isocurvature gas variance ≥ F_b δ_in²/(1 + δ_in), δ_in = r(1 − f_max), F_b = the
  fraction of all baryons in depleted patches. The forest band allows gas power within ±20 % of the adiabatic gas power,
  so F_b ≤ F_b,max = 0.2 σ²_ad(R_L, z)/[δ_in²/(1 + δ_in)], with σ_ad from the record's BBKS shape (X22 `Tk`), σ₈ = 0.82742
  (EM1 own, X43 K2 line), growth D(z) from X22's D_lcdm, top-hat R_L = 0.442 Mpc/h (X22 median), z = 3 and 2 (the tighter
  is graded). R1 FAIL if F_b,max < 0.01 on that footing; otherwise ND (the record has no measured F_b).
- **CMB through X34's machinery:** X34's vanilla CLASS binary (C7 parameters as X34 / X54), TT C_ℓ with ad only vs ad +
  compensated (cdi, bi, f_bi = (ω_c/ω_b) f_cdi, c_cdi_bi = −1, f_cdi = 1) vs ad + uncompensated cdi (f_cdi = 1, control).
  Reported: max |ΔC_ℓ/C_ℓ| over ℓ 2–2500 for each. CMB line ND if the compensated change is < 1e-3 (linear CMB blind).
- R4b common line. R7 BC PASS.

## 4. The common R4b line (coordinator)

Every graded class (M1, M2, M3, M4, M6) leaves the law acting on cluster baryons and adds a cold component of
non-negative gravitating density. Its OUTER prediction is then ≥ the law's own, A ≥ 0.999 (X56's law copy of X43).
**R4b FAIL** for the class if the law's own G-OUT-all is outside |Z| ≤ 2.0 in both h cells on that footing (X43's line).
The one way out is a cold-dark-energy deficit below the cosmic mean around clusters (an evacuated region). Its largest
possible effect is bounded by D = (4π/3)(3 Mpc)³ ρ̄_c / M_gas500,med (ρ̄_c = 5.364 Ω_b ρ_crit with X22's constants;
M_gas500 median from X7's committed npz). The law's lensing mass at ≥ 1.4 Mpc exceeds the gas mass, so D bounds the
fractional drop in A from above. R4b FAIL stands if D < 1 − 0.716 = 0.284 (canonical) / 1 − 0.656 = 0.344 (alt).

## 5. Verdict classes

Per class and footing:
- **CLASS k EXCLUDED BY Rn (number)**: any graded line FAILS. All failing lines are listed; the binding one is the
  first in the order R1, R3, R3b, R4, R4b, R6.
- **CLASS k VIABLE (open requirement)**: no FAIL, and R1, R3, R4, R4b are PASS or BC.
- **NOT DECIDABLE WITH RECORD DATA**: no FAIL, but one of R1, R3, R4, R4b is ND.
A class is quoted with one verdict only if the footings agree; otherwise both are given.

**Overall:**
- **NO GRADED CLASS VIABLE** if M1, M2, M3, M4 and M6 are each EXCLUDED on both footings.
- **CLASS(ES) k VIABLE** if any graded class is VIABLE on both footings.
- **UNDECIDED** otherwise.
The overall line also states whether each exclusion survives with R4b removed (i.e. whether it rests on R4b alone).

Reported, not graded: a ranked shortlist of whatever survives (graded classes not EXCLUDED, plus M5 as reported), and
the one observation that would decide between them.

## 6. Checks (all must PASS in the normal run)

- K0 Step 0 (all items in §2).
- K1 β = 0 two-fluid ODE reproduces X22 C2: δ_m(z = 0) 0.787089 within 1e-5, and T_b ≡ 1.
- K2 M2 sign: β = 1, λ = 10 Mpc, k = k5, z = 3: T_b < 1 (repulsion lowers baryon clustering).
- K3 M4: T²(k5, z = 3) non-increasing over ν_w ∈ {0, ν₁, 2ν₁, 4ν₁}, ν₁ = 0.1 kpc·km/s.
- K4 sympy (PYTHONHASHSEED=0): the Yukawa kernel β 4πG/(k² + λ⁻²) expanded for kλ ≪ 1 gives the local potential
  +4πG β λ² ρ_b (repulsive sign for s = +1), and for kλ ≫ 1 tends to β × the Newtonian kernel.
- K5 M6 positivity: closed-form f_V bound equals a brute-force scan (1e-6 grid) to 1e-5.
- K6 peak RSS < 1 GB, one thread.

## 7. MUTATE twin (`X57_MUTATE=1`; outputs suffixed `_MUTATE`)

- m1: M2 force sign flipped (s = −1, attractive).
- m2: M4 wave term sign flipped (anti-pressure).
- m3: Step 0 compares X53's Δχ² to the committed value + 1.
- m4: M6 positivity uses r = 1/5.364.
**Required:** K0, K2, K3, K5 FAIL; K1, K4, K6 PASS; exit code 1. Any other pattern means the twin is broken.

## 8. Rules

Small jobs only (< 1 GB, OMP_NUM_THREADS=1, nice -n 15); CLASS outputs go to the scratch/temp area, not the repository;
no downloads; nothing outside this lane is edited. Every README number comes from the committed `.out` / `_results.json`.
Commit by pathspec only; no push.
