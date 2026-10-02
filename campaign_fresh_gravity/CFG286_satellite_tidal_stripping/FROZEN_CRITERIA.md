# CFG286 -- derived tidal stripping of the satellites' collapse-cold cores at their measured pericentres: frozen criteria

Written before any CFG286 script existed and before any satellite offset, pericentre or tidal radius was computed. Paths are relative to the repository root.

Standing statements, binding on every sentence of the lane: kappa = 1/2 is FITTED, not derived. There is no dark-matter particle and no new species: the cold component is a conserved, collisionless fluid, and **the mass is still required** (the collapse mass comes from a declared stellar-to-halo relation, which the framework does not supply). Nothing here says the data favour the framework, or that the theory is closed. A FAIL is a valid outcome.

---

## 0. What was read before freezing (not-blind statement)

**Read:**
- `campaign_fresh_gravity/STANDING_2026-09-29.md`: the bottom line, sections 1-5, and the satellite entries (CFG244 Gate H, CFG257, CFG259, the corrigendum line).
- READMEs of CFG28, CFG29, CFG42, CFG45, CFG59, CFG75, and CFG259's README (bottom line, tables, disclosures).
- `CFG244_FROZEN_CRITERIA.md`, the Gate H section (readings (a0), (a1), (a2), (b), the statistic, the decision lines).
- PAPER37's abstract.
- Code: `CFG28_ufd_referee.py` (whole); `CFG42_satellites_rule.py` up to its C1/C2 banner; `CFG45_rule_readings.py` up to its P3 banner; `CFG7_hierarchy_fg001.py` up to `REF43`; the helpers `halo_mass` and `nfw_enclosed` (h48), `edge_phantom` (CFG35), `CFG7_common.Report`, `M_law`, `r_ta_law`, the kernels in `CFG4_common.py`; the McMillan-2017 parameter block in `hunt_2026/g02_vertical_vs_planar_frequency_split.py`; the census line `CENSUS = (6.0e10, 7.3e10)` in `hunt_2026/k_cross-scale_mwmass.py`.
- Data: the column list of `real_research/data/dsph/lvd_dwarf_mw.csv` and `lvd_dwarf_m31.csv`, and a listing of every sample member's name, host, M_V, r_half, distance and proper-motion error size. The Collins+13 table header and first rows. `PROVENANCE.md`.
- The key names (not the values) of `CFG45_rule_readings_results.json`.

**So I am not blind to:** the record's aggregate satellite numbers. Rule (S): ultra-faints -0.059 dex (-0.41 sigma), MW classical -0.118 (-1.78 / -1.90 sigma), M31 Collins+13 -0.024 (-0.22 sigma), M31 LVD -0.107 (-2.67 / -2.66 sigma). Law (L): +0.325 / +0.304 (3.77 / 3.55 sigma) on the ultra-faints. CFG91's error-recipe dependence of the M31 LVD significance (-2.67 / -1.74 / -1.97 / -1.49 sigma). CFG69's LambdaCDM-comparator aggregates as quoted in CFG244. **I have NOT seen any per-satellite offset, pericentre or tidal radius.** I know from the literature, from memory and not used as an input, that Gaia-era LambdaCDM pericentres of the MW classical dSphs are typically 30-100 kpc, Sagittarius about 15 kpc and Tucana III about 3 kpc.

**Pre-freeze hand arithmetic** (generic systems only, written into section 12). A Draco-like, an Sgr-like, an And XIX-like and a Tucana III-like system in the law's host field give tidal radii of about 2.5-3 kpc, about 2 kpc, about 6 kpc and about 0.03-0.04 kpc. Against the estimator radii (4/3) r_half these are 0.26, 2.1, 2.9 and 0.04 kpc. **So I expect the sharp truncation to reach the estimator's radius in only a handful of systems, and the population medians to move little.** This expectation is stated before the run; the run decides.

---

## 1. The question and the hypothesis (as directed, frozen)

The derived cold-mass rule (PAPER36; CFG35-CFG45 reading S) closes the ultra-faint offset but over-predicts the classical satellites (M31 LVD -2.67 sigma). The hypothesis tested here is the owner-directed one: **each satellite keeps its collapse-cold mass only inside its tidal radius at its measured pericentre.** The tidal radius comes from the host's field under the programme's own law: the host is the owner, and the satellite sits in the host's field. Does this, with no free parameter, reconcile the ultra-faints and the classicals?

---

## 2. Inputs and the constants ledger

**Samples (the record's own, unchanged; loaded by exec'ing CFG45's committed prefix read-only, which loads FG001/CFG42's samples):**
- P1, MW ultra-faints: 31 resolved and 9 upper limits (Kaplan-Meier), M_V > -7.7.
- P2, MW classical satellites: 14 (FG001's `cls`, M_V <= -7.7, including the LMC, the SMC and Sagittarius as the record has them). Infall gas as CFG18's expectation (CFG42's `gas=True`).
- P3, M31 LVD: 34.
- P4, M31 Collins+13: 14 (13 shared with P3). It is in the record's A2 gate, so it is scored here too.

**Data for the orbits (on disk, nothing downloaded):** `lvd_dwarf_mw.csv` gives ra, dec, the heliocentric `distance` with `distance_em` / `distance_ep`, `pmra` (mu_alpha cos delta) and `pmdec` with their em / ep, and `vlos_systemic` with its em / ep. All 54 MW systems in P1+P2 have all six. For M31, `lvd_dwarf_m31.csv` gives proper motions for 8 of its 43 rows. **M31's own systemic proper motion is not on disk as numbers** (only a citation record, plus a tangential-speed magnitude in FP11), so no M31 satellite's M31-centric velocity can be formed. The M31 satellites are therefore treated by radius with an explicit assumption (section 8).

**Constants ledger.** kappa = 1/2 is FITTED and gives the two footings: the satellite estimator uses FG001's a0 = 9.36e-11 / 1.13e-10 m/s^2, and the edge phantom uses CFG7's 9.3603e-11 / 1.1312e-10, as committed. Everything else is measured, derived, or a declared function shape inherited unchanged from the record:

| item | value | status |
|---|---|---|
| Upsilon_V | 2 (floor variants 1, 4) | the record's (FG001/CFG42/CFG45) |
| collapse mass | Moster+2013 as coded in h48, clamped at 1e9 Msun below M_* about 1.6e4; floor scan 1e8-1e10 for M_* < 1e5 | the record's declared function shape (it is "LambdaCDM with a declared SHMR", CFG244) |
| NFW + concentration | Dutton-Maccio, h48's `nfw_enclosed` | the record's |
| f_b | 0.02237 / (0.02237 + 0.1200) | Planck 2018 (shared with LambdaCDM) |
| f_ex | max(0, 1 - M_phantom,edge / [(1 - f_b) M_c]) at x_e = 0.40 | the committed rule, unchanged |
| host baryons | MW 6.0e10 Msun, M31 1.2e11 Msun, point masses | the record's (h43 / FG001 / CFG42 / CFG244 (a2)) |
| MW host-mass variant | 7.3e10 Msun (the census upper value) | the record's census line, reported only |
| host kernel | nu_mono (FP1's committed table) | the 09-26 decision; the exponential RAR kernel is a reported row |
| satellite internal law | FG001's `a_int` (exponential RAR kernel) | the committed estimator (CFG64: it equals nu_mono to 3e-9 at y <= 0.1) |
| solar position and motion | astropy's Galactocentric 'v4.0' set: R0 = 8.122 kpc, z_sun = 20.8 pc, v_sun = (12.9, 245.6, 7.78) km/s, Sgr A* at Reid & Brunthaler 2004 | measured (GRAVITY 2018, Bennett & Bovy 2019, Drimmel & Poggio 2018); R0 = 8.122 is also the record's registered value |
| integration window | t_H = 13.80 Gyr | derived from the record's Planck cosmology (CFG7_common.LCDM) |
| stellar profile for m(<r) | Plummer, scale a set so that M_b(<(4/3) r_half) = M_b/2 exactly (a = 1.0219 r_half) | a declared shape; it reproduces FG001's half-mass convention; the point-mass alternative is a reported row |
| M31 distance (for projected radii) | 785 kpc, centre 00 42 44.3 +41 16 09 | FG001's |
| Monte Carlo | 1000 draws per MW satellite, seed 286; leapfrog dt = 0.5 Myr | numerical settings, not physics |

**No constant is fitted, scanned or chosen by outcome.** Every reported row in section 11 is a robustness check, never used to pick anything.

---

## 3. The host potential

Spherical, static. The host field at Galactocentric radius r is

  g_h(r) = nu_mono(y) G M_host / r^2, y = G M_host / (r^2 a0),

with M_host = 6.0e10 Msun (MW) or 1.2e11 Msun (M31), at each footing's a0. For a spherical source the algebraic form is exact (the QUMOND curl term vanishes). The potential is Phi(r) = integral of g_h dr, and it is tabulated on a log grid from 0.01 to 1e5 kpc (20001 points). Interpolation is in ln r and ln g. Below about 8 kpc a point mass is not the Galaxy; systems whose median pericentre falls inside R0 are flagged.

## 4. The orbit integration (MW systems)

- For each of the 54 MW systems (P1 and P2), draw 1000 realisations of (distance, pmra, pmdec, vlos), each from a two-piece normal with sigma_- = em and sigma_+ = ep about the table value, independent and uncorrelated (the LVD gives no correlations; an assumption). If one side is missing, the other is used for both. The central realisation (the table values) is kept separately.
- Transform ICRS to Galactocentric with astropy ('v4.0' parameters).
- Integrate backward in time with a kick-drift-kick leapfrog in the static host field (dt = 0.5 Myr), up to t_H. **The pericentre is the most recent local minimum of r(t) in the backward integration**, refined by a parabola through the three steps around it. Recorded with it: the pericentre speed v_p = L / r_p and the time since pericentre.
- A draw with no pericentre within t_H is "no pericentric tide in the age of the universe": D_t = 0 (unstripped).
- **Control C-ORB:** for every central orbit, the leapfrog pericentre agrees with the exact root of 2[E - Phi(r)] - L^2/r^2 = 0 to 1% (a static spherical potential conserves E and L).

## 5. The tidal radius (formula frozen)

The King (1962) Jacobi-type radius at pericentre, in the host's actual field:

  r_t^3 = G m(<r_t) / D_t,   D_t = Omega_p^2 - d^2 Phi_h / dr^2 |_{r_p} = (v_p / r_p)^2 - dg_h/dr |_{r_p}.

For a Keplerian host on a circular orbit this reduces to r_t = r_p [m / 3M]^(1/3). For a flat rotation curve it reduces to r_t^3 = G m r_p^2 / (2 v_c^2). D_t > 0 always, because dg_h/dr < 0.

**m(<r) is the satellite's own retained mass**, in its own owned dynamics (class A: Newtonian with its cold matter, no external-field effect, as FG001):

  m(<r) = r^2 a_int(G M_b(<r) / r^2, 0, a0) / G + f_ex (1 - f_b) M_NFW(<r; M_c),

with M_b(<r) the Plummer profile of section 2 and the baryons as in the estimator (stars at the variant's Upsilon_V, plus current gas, plus CFG18's infall gas for P2-P4). It is solved self-consistently by Brent's method in ln r on [1e-4, 1e4] kpc. Per satellite the point prediction uses the **median of D_t over its Monte Carlo draws**. Since r_t is monotone in D_t at fixed m(r), this equals the median r_t.

## 6. The stripping rule (frozen)

At the estimator radius r_ev = (4/3) r_half (FG001's), the total acceleration is

  g = a_int(g_N, 0, a0) + f_ex (1 - f_b) G M_NFW(< min(r_ev, r_t); M_c) / r_ev^2,

so the collapse debris beyond r_t is removed and the debris inside r_t is retained unchanged. f_ex is the committed rule's value, set at collapse: the phantom/debris split is not re-done by stripping, which removes matter but does not re-split it. **The law's own term a_int(g_N) is not truncated:** it is B's committed class-A reading (the satellite keeps its phantom), and it is what makes full stripping return the "own nothing" reading (a1) (control M3). Truncating the phantom as well is a different reading; it is a reported row only. sigma^2 = g r_ev / 3; offset = log10(sigma_obs / sigma_pred).

**Limits that define the rule's ends (controls M2, M3):**
- r_t -> infinity (no stripping) is exactly reading S (CFG45).
- r_t = 0 (full stripping: no debris) is exactly reading L, which is CFG244's (a1) "satellites own nothing" = B's frozen isolated law.

## 7. The observable and the error model (exactly the record's, CFG42/CFG45 = CFG59/CFG75's rows)

- **P1:** the Kaplan-Meier median of the offsets with the 9 limits. error = sqrt(boot^2 + f_ups^2 + f_mh^2), with:
  - boot: 1000 resamples, seed 42, CFG45's `boot`;
  - f_ups: half the shift between Upsilon_V = 1 and 4;
  - f_mh: half the range over the collapse-mass floors 1e8, 3e8, 1e9, 3e9, 1e10 for every satellite with M_* < 1e5.
- **P2-P4:** the sample median. error = sqrt((1.2533 std / sqrt n)^2 + f_ups^2 + f_mh^2), as CFG42/CFG45.
- In every variant (Upsilon, floor) **the tidal radius is re-solved** with that variant's satellite mass. The orbit (D_t) is a property of the satellite's centre of mass and does not change.
- z = median / error. Both footings.
- CFG45's own functions (`km_median`, `boot`, `edge_info`, `a_int`, `infall_gas`, `halo_mass`, `nfw_enclosed`) are exec'd read-only and called unchanged.

## 8. The M31 satellites (no M31-centric velocities on disk): explicit assumption

- **Primary route, by projected radius (as directed):** R_proj = 785 kpc x the angular separation from M31's centre (measured to about 1%, no line-of-sight error). **Explicit assumption:** M31's satellites have the same joint distribution of (q', eta) as the MW's 54 satellites in the law's MW host. Here q' = r_p / R_proj is seen from an isotropic random direction (cos theta ~ U(-1, 1), R_proj,MW = r_now sin theta, one direction per draw), and eta = v_p / v_c,host(r_p).
  - The pool is all 54 x 1000 MW draws (draws with no pericentre enter with D_t = 0).
  - For each M31 satellite and pool entry: r_p = q' R_proj, v_p = eta v_c,M31(r_p), D_t from section 5 in the M31 host field. The point prediction uses the median D_t over the pool.
  - A log potential is scale-free, so the transfer of a dimensionless orbit distribution between hosts is the natural one. It is still an assumption, stated as such.
- **Alternate route, by 3D distance (decides PARTIAL, section 9):** r_now = the record's D (`distance_host` for the LVD; FG001's computed 3D distance for Collins+13). r_p = q r_now, with q = r_p / r_now and eta from the same MW pool.
- **Reported only:** the literal "projected radius as pericentre on a circular orbit" (r_p = R_proj, v_p = v_c); and the minimal-tide bound, a circular orbit at r_p = the record's 3D D. Since r_p <= r_now and v_p >= v_c(r_p) for any bound orbit, this is the weakest possible tide given D.

## 9. Pass lines and verdict (frozen)

- **H1 (ultra-faints consistent):** |z_P1| < 2 on both footings.
- **H2 (classicals consistent, MW and M31):** |z| < 2 for P2, P3 and P4 on both footings (primary M31 route). This is two-sided, because "consistent" is required. The record's A2 is one-sided (not below -2 sigma) and is reported beside it.
- **JOINT PASS:** H1 and H2 on both footings, and H2's M31 part also holds under the alternate (3D) route.
- **PARTIAL:** H1 and H2 hold on both footings with the primary route but the M31 part fails with the alternate route; or H1 and H2 hold together on exactly one footing; or one of H1 / H2 holds on both footings and the other on exactly one.
- **FAIL:** anything else. **The binding population** is named: the population with the largest |z| among those with |z| >= 2, per footing.
- **Reported beside the verdict:**
  - the 1-sigma level (CFG59's strict criterion: all four populations within 1 sigma);
  - the shift of every population's median and z relative to S (no stripping);
  - the number of systems with r_t < r_ev in each population;
  - the CFG244/CFG259 caveat: the ultra-faint preference for a retained core is carried by a few systems, with small margins.
- **Free-choice statement (frozen):** the verdict names every input that is neither measured nor derived nor the record's (section 2). If any choice was free and the verdict depends on it, the lane is not a derivation.

## 10. Controls and MUTATE (all load-bearing unless marked)

- **C-HOST:** the tabulated host field equals the direct formula to 1e-6 relative on 1000 random radii in [0.5, 3000] kpc; nu_mono(y -> 0) gives the deep limit g -> sqrt(G M a0) / r to 1e-3 at y = 1e-4.
- **C-COORD:** the central Galactocentric distances equal the LVD's `distance_gc` to 1.5 kpc (or 2%) for every MW system. **Reported:** the radial velocities against the LVD's `velocity_gsr`, which uses its own solar motion, so only a sanity check.
- **C-ORB:** section 4.
- **C-JAC:** the Jacobi solver satisfies r_t^3 D_t = G m(<r_t) to 1e-8 relative for every satellite. For a point-mass satellite in a point-mass Kepler host on a circular orbit it returns r_p (m / 3M)^(1/3) to 1e-6.
- **M2 (no stripping):** with r_t = infinity, this lane's pipeline reproduces CFG45's committed reading-S numbers (UF and CL: median or KM median, err, tot, z; both footings; all four populations) to 1e-9.
- **M3 (full stripping):** with r_t = 0, it reproduces CFG45's committed reading-L numbers to 1e-9, which equal B's "own nothing" (a1) offsets; P1's KM median also equals CFG28's committed RES to 1e-9.
- **M1 (MUTATE=1, pericentre x2):** every pericentre doubled with the pericentre speed held fixed (Omega_p = v_p / (2 r_p), d^2 Phi evaluated at 2 r_p); for M31 likewise on every pool entry. The load-bearing check in that run is "UNCHANGED: every classical population's median offset (P2, P3, P4) is within 0.01 dex of the main run's, on both footings". It **must FAIL (rc = 1) for the stripping to have measurable bite on the classicals.** If it passes, the lane reports that the stripping is inert on the classicals at the estimator radius.
- **MUTATE=2 / MUTATE=3:** separate runs with r_t = infinity / 0 throughout, writing their own outputs and verdict tables in the two limits; their load-bearing checks are the M2 / M3 reproductions (rc 0 when reproduced).
- Mutation runs write separate outputs, named by mode.

## 11. Reported rows (never verdicts)

1. The MW host at 7.3e10 Msun (pericentres re-found by the exact (E, L) root, validated by C-ORB).
2. The host with the exponential RAR kernel in place of nu_mono (same method).
3. Point-mass baryons in m(<r) in place of Plummer.
4. The phantom truncated too, for systems with r_t < r_ev (the law term evaluated with M_b(<r_t) at r_t and carried to r_ev as mass).
5. M31: the literal projected-radius circular row and the minimal-tide bound (section 8).
6. A pericentre floor: each population's median recomputed with every satellite at its 16th and at its 84th percentile D_t; floor = half the difference; z with it added in quadrature.
7. The rule's own f_ex for the hosts: MW at M_* = 5.0e10, M31 at M_* = 1.0e11, blue relation, the hosts' record baryons. If either is > 0, a row with the host's own debris added to its field is run.
8. Per-satellite table: r_p (median, 16th-84th percentiles), time since pericentre, v_p, D_t, r_t, r_ev, r_t / r_ev, Delta log sigma_pred (stripped - S); CSV.

## 12. Frozen hand estimates (my arithmetic, before any run)

- **HE1:** MW classical pericentres in the law host (canonical): the median of the 14 per-system medians is in [35, 80] kpc; Sagittarius in [10, 20] kpc; the LMC in [40, 52] kpc.
- **HE2:** P1 pericentres: the median of the 40 per-system medians is in [25, 70] kpc; Tucana III < 8 kpc.
- **HE3:** systems with r_t < r_ev (canonical, main): P2 0-3 of 14; P1 0-3 of 40; P3 0-4 of 34; P4 0-2 of 14.
- **HE4:** the P1 KM median moves by |Delta| <= 0.01 dex from S; H1 passes on both footings (P = 0.9).
- **HE5:** each classical population's median moves by |Delta| <= 0.02 dex (P = 0.8); P3 stays at z <= -2 on the canonical footing (P = 0.75).
- **HE6:** verdict FAIL with P3 (M31 LVD) binding, P = 0.70; PARTIAL, P = 0.10; JOINT PASS, P = 0.20.
- **HE7:** M1 bites (some classical population's median moves >= 0.01 dex on both footings): P = 0.3. I expect it not to bite.
- **HE8:** the median over the 14 MW classicals of r_t / r_ev is >= 3.
- **HE9:** C-ORB passes (P = 0.9).
- **HE10:** the 7.3e10 host row moves no population median by more than 0.01 dex.

## 13. Files

- `cfg286_tidal_stripping.py`: one script with modes MUTATE=0 (main), 1 (pericentre x2), 2 (no stripping), 3 (full stripping).
- Outputs: `cfg286_tidal_stripping[_MUTATE{1,2,3}].out` / `_results.json`, `cfg286_pericentres.csv` (main), `cfg286_orbit_draws.npz` (main; the per-draw r_p, v_p, D_t).
- `README.md` after the runs.

Nothing here says the theory is closed. kappa = 1/2 FITTED.
