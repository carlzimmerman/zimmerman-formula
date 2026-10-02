# CFG286 — derived tidal stripping of the satellites' collapse-cold cores at their measured pericentres: FAIL, the stripping is inert at the radius where dispersions are measured

> **κ = ½ FITTED.** No dark-matter particle: the cold component is a conserved, collisionless fluid, and **its mass is still required** (a declared stellar-to-halo relation supplies it). Nothing here says the theory is closed or that the data favour the framework.

- **Criteria:** `FROZEN_CRITERIA.md`, written before the script existed and before any satellite offset, pericentre or tidal radius was computed. Its sha256 (f091e2eb…eb97) is printed at the top of every run's output. It is not committed: this lane does not commit, so the orchestrator should commit the criteria first.
- **Scripts:**
  - `cfg286_tidal_stripping.py` (about 50 s per mode). Modes: MUTATE=0 main; 1 = every pericentre ×2; 2 = no stripping; 3 = full stripping.
  - `cfg286_posthoc_retained_mass.py` (labelled POST-HOC; no verdict depends on it).
- **Outputs:**
  - `cfg286_tidal_stripping.out` / `_results.json`, and the same for `_MUTATE1`, `_MUTATE2`, `_MUTATE3`;
  - `cfg286_pericentres.csv`: per satellite and footing, r_p (median and 16–84 %), time since pericentre, v_p, D_t, r_t, r_ev, f_ex, M_c, the stripped minus unstripped log σ, and the offset;
  - `cfg286_orbit_draws.npz`: the 2 × 54,054 orbits (phase space, r_p, v_p, time since pericentre, exact-root r_p);
  - `cfg286_posthoc_retained_mass_POSTHOC.out` / `_results.json`.
- **Exit codes:**
  - The main run exits 1 because H2 fails, and because of the frozen C-HOST tolerance (see disclosures).
  - MUTATE=1 exits 0: its UNCHANGED check passes, which means the mutation does not bite.
  - MUTATE=2 and 3 exit 0 (their reproductions hold).
- **Nothing downloaded.** Only on-disk data (the LVD tables, Collins+13) and the record's committed scripts were used, exec'd read-only. No file outside this directory was written.

## Bottom line

**FAIL on both footings; the binding population is the M31 LVD (z −2.67 canonical / −2.66 alt, −0.107 / −0.109 dex), exactly as for the unstripped rule.**
- The derived stripping moves no population median at all (shift 0.0000 dex in every population, on both footings).
- Pericentre ×2 also moves nothing (MUTATE=1 does not bite).
- **Why:** at the measured or transferred pericentres, every satellite's tidal radius is about 10–35 times its estimator radius (4/3) r_half (median r_t / r_ev: 34 for the ultra-faints, 11 for the MW classicals, 15 for the M31 LVD). The truncation does remove most of each satellite's collapse mass: 66–87 % of the debris, by population median (post hoc). But only 0.03–1 % of that mass sat inside r_ev, where the dispersion is measured, and the NFW cusp there is untouched.
- **The only classical with r_t < r_ev is Sagittarius** (r_t 0.59 kpc vs r_ev 2.09 kpc at r_p = 15.7 kpc). Under the rule its f_ex = 0 (its phantom already exceeds its collapse mass), so it has no debris to strip.
- **The closest M31 cases** are NGC 205 (r_t/r_ev 1.68, also f_ex = 0), And XIX (2.29) and And I (2.62).

So **a sharp tidal truncation at the satellites' pericentres cannot be what separates the ultra-faints from the classicals.** Lowering the classicals' predicted dispersions needs a lower inner cold density at r ≈ r_half: a core, or tidal heating that reshapes the inner profile. The tidal-track models that do that are N-body-calibrated: their constants would be imported, so under the no-knob rule they are not run here. This is consistent with PAPER37's note that a Burkert core removes both the closure and the over-prediction.

## The frozen pass lines

| line | criterion |
|---|---|
| H1 (ultra-faints) | \|z\| < 2 on both footings; Kaplan–Meier median of the 31 + 9 offsets; error = bootstrap (1000, seed 42) ⊕ Υ_V floor ⊕ collapse-mass floor (CFG45 / CFG42 recipe) |
| H2 (classicals) | \|z\| < 2 for the MW classical (14), M31 LVD (34) and M31 Collins+13 (14) on both footings; median; error = 1.2533 std/√n ⊕ Υ_V floor ⊕ collapse-mass floor; two-sided ("consistent"); the record's one-sided A2 is reported |
| JOINT PASS | H1 and H2 on both footings, with the M31 part also holding under the alternate (3D-distance) route |
| PARTIAL | the M31 part depends on the route; or the joint holds on one footing only; or one of H1/H2 holds on both footings and the other on one |
| FAIL | anything else; the binding population is the largest \|z\| ≥ 2 |

The tidal radius is re-solved in every error-model variant (Υ_V 1 / 4, the collapse-mass floors).

## Results

| population | canonical: stripped | canonical: no stripping (S) | alt: stripped | alt: S |
|---|---|---|---|---|
| P1 MW ultra-faints (31 + 9 limits) | −0.0586 ± 0.1423, z −0.41 | identical | −0.0591 ± 0.1448, z −0.41 | identical |
| P2 MW classical (14) | −0.1183 ± 0.0666, z −1.78 | identical | −0.1233 ± 0.0647, z −1.90 | identical |
| P3 M31 LVD (34) | **−0.1069 ± 0.0401, z −2.67** | identical | **−0.1086 ± 0.0409, z −2.66** | identical |
| P4 M31 Collins+13 (14) | −0.0240 ± 0.1082, z −0.22 | identical | −0.0161 ± 0.1054, z −0.15 | identical |
| P3 / P4, 3D route | −2.67 / −0.22 | | −2.66 / −0.15 | |

- **H1 PASS** on both footings.
- **H2 FAIL** on both footings, through the M31 LVD.
- **Verdict: FAIL.**
- Not all four populations are within 1σ; the one-sided A2 also fails.

**The rule's two ends, through this lane's own pipeline:**
- r_t = ∞ (MUTATE=2) is reading S: FAIL through the M31 LVD.
- r_t = 0 (MUTATE=3) is reading L, i.e. CFG244's (a1) "own nothing", B's frozen isolated law: FAIL through the ultra-faints (+0.325 / +0.304 dex, z +3.77 / +3.55), while H2 passes.

The derived stripping at measured pericentres lands exactly on the S end.

**Caveat carried from CFG244 / CFG259:** the ultra-faints' preference for a retained core is carried by a few systems, with margins that are fractions of a χ². The ultra-faint "closure" by the rule is itself a weak test: any collapse mass from 2e8 to 1e12 passes (CFG42's referee). The M31 LVD significance also depends on the error recipe: −2.67 / −1.74 / −1.97 / −1.49σ across four recipes (CFG91). This lane uses the record's frozen recipe, so the H2 failure inherits that dependence; the stripping does not change it.

## Pericentres (law host: MW baryons 6.0e10 M☉ point mass, ν_mono; median of 1000 Monte Carlo draws)

**MW classical, canonical:**

| system | r_p [16–84 %] (kpc) | last pericentre (Myr ago) | r_t / r_ev | f_ex |
|---|---|---|---|---|
| Sagittarius | 15.7 [13.6, 17.5] | 37 | **0.28** | 0 |
| Crater II | 44.1 [38.7, 49.9] | 1749 | 2.06 | 0.56 |
| UMi | 46.9 | 1419 | 11.95 | 0.67 |
| LMC | 47.5 [46.9, 48.1] | 44 | 3.22 | 0 |
| Antlia II | 51.8 [46.1, 58.5] | 853 | 1.40 | 0.63 |
| Draco | 53.4 [51.8, 55.0] | 1878 | 17.3 | 0.66 |
| Leo I | 55.9 | 1051 | 11.3 | 0.08 |
| SMC | 60.2 | 2856 | 9.05 | 0 |
| Sculptor | 63.5 | 401 | 21.2 | 0.46 |
| CVn I | 70.9 | 1229 | 12.3 | 0.68 |
| Sextans | 78.1 | 243 | 9.9 | 0.68 |
| Fornax | 82.0 | 1992 | 9.8 | 0 |
| Leo II | 85.1 | 1711 | 38.2 | 0.66 |
| Carina | 106.6 | 3090 | 32.9 | 0.66 |

- **MW classical:** median r_p 58.0 kpc (alt 56.9).
- **Ultra-faints:** median r_p 39.3 kpc (31 resolved) and 29.7 kpc (9 limits). The smallest are Tucana III 2.5 kpc (inside R0, where a point-mass host is not the Galaxy; flagged), Boötes III 10.9, Triangulum II 13.6 and Centaurus I 19.8. **Two are stripped at r_ev:** Boötes III (r_t/r_ev 0.41, Δlog σ_pred −0.28) and Tucana III (0.19, −0.47). Neither moves the Kaplan–Meier median.
- **No pericentre within t_H = 13.8 Gyr** for most draws of Pisces II (96 %), Pegasus III (86 %) and Eridanus II (63 %); these are unstripped by the frozen rule.
- **M31 (projected radius × the MW-derived pool):** median r_p 101 kpc (LVD) and 99 kpc (Collins). No system has r_t < r_ev on any M31 route.
- **The MW pool** has median q' = r_p/R_proj = 0.88, median q = r_p/r_now = 0.70, and median η = v_p/v_c(r_p) = 1.60.

## Controls and MUTATE outcomes

| control | result |
|---|---|
| M2 (r_t = ∞ reproduces CFG45 reading S, 30 numbers) | PASS, max \|d\| 0.0 |
| M3 (r_t = 0 reproduces CFG45 reading L = CFG244 (a1), and CFG28's committed KM median) | PASS, max \|d\| 0.0 |
| **M1 (MUTATE=1, pericentre ×2 at fixed pericentre speed): "UNCHANGED" must FAIL for the stripping to bite** | **PASSES (max shift 0.0000 dex), so the mutation does NOT bite: the stripping is inert on the classicals at the estimator radius** |
| C-ORB (leapfrog vs exact (E, L) root, central orbits) | PASS, max 5.3e-4 / 5.8e-4; 0.02 % of all draws off by > 1 % |
| C-JAC (Jacobi residual; Kepler limit) | PASS, 7.5e-14; 1.9e-15 |
| C-COORD (Galactocentric distances vs the LVD's distance_gc) | PASS, max 0.01 kpc |
| C-HOST (table vs formula; deep limit to 1e-3 at y = 1e-4) | **FAIL as frozen**: the table is exact to 5.3e-8, but the deep-limit deviation is 5.0e-3, the kernel's known +½ next-order term. My tolerance was wrong; it was kept. A diagnostic against 1 + √y/2 agrees to 8e-6 |

## Reported rows (none is a verdict; none changes it)

- Pericentre floor (16th vs 84th percentile tides): 0.0000 in every population.
- Point-mass baryons in m(<r): identical medians.
- **Phantom truncated too:** MW classical −0.1094 (z −1.53) canonical, −0.1088 (z −1.59) alt, all through Sagittarius. The M31 LVD is unchanged (−2.67 / −2.66).
- M31 literal row (projected radius as pericentre, circular orbit) and the minimal-tide bound (circular orbit at the 3D distance): identical to the primary.
- MW host at 7.3e10 M☉, and the MW host with the exponential RAR kernel: shift 0.0000 in P1 and P2.
- The hosts' own rule f_ex: 0 for the MW (M_c 9.8e11 against an edge phantom of 4.6e12 / 5.3e12) and for M31, so the host-debris row is not needed.

## Hand estimates (frozen), scored

- **All met:**
  - HE1: MW classical median 58.0 kpc, Sgr 15.7, LMC 47.5.
  - HE2: P1 median 39.0, Tuc III 2.5.
  - HE3: stripped systems: P2 1, P1 2, P3 0, P4 0.
  - HE4, HE5: shifts 0.
  - HE6: FAIL with the M31 LVD binding.
  - HE7: I expected M1 not to bite; it did not.
  - HE8: median r_t/r_ev 10.6.
  - HE9, HE10.
- **Missed:** none.

## Free choices: none affects the verdict

Every input is either the record's, measured, or derived:
- **The record's:** the samples; the estimator; the error recipe; Υ_V = 2; the Moster collapse mass and clamp; the Dutton–Macciò NFW; f_b; the host baryons 6.0e10 / 1.2e11.
- **Measured:** the LVD positions, distances, proper motions and velocities; the solar parameters (astropy 'v4.0').
- **Derived:** t_H.
- **The rule's own pieces:** f_ex and the edge.

**The declared pieces that are not derived:**
- **The King (1962) Jacobi form at pericentre.** Among the standard Jacobi-type forms at a given radius it gives the strongest tide, since Ω_p² ≥ g/r, so the inertness is not an artefact of a weak form.
- **The Plummer stellar profile.** The point-mass row is identical.
- **Uncorrelated two-piece-normal errors.** The pericentre floor is 0.
- **The M31 orbit-distribution transfer from the MW (an explicit assumption).** Every M31 route gives 0 stripped systems, including the strongest-tide primary route, and the median M31 LVD system sits at r_t/r_ev ≈ 15.

**The one reading choice is not truncating the satellite's own phantom.** The frozen rule keeps it, as M3 requires. Truncating it moves only the MW classicals, by +0.009 dex through Sagittarius, and leaves the binding M31 LVD unchanged.

So the lane is a derivation in the sense the brief asked for: zero declared constants beyond κ = ½, and no choice was free in a way that matters.

## Disclosures

- **Seen before freezing:** the record's aggregate satellite numbers and the code and data listed in `FROZEN_CRITERIA.md` §0 (no per-satellite offset, pericentre or tidal radius). My pre-freeze hand arithmetic already expected the truncation to be mostly inert.
- **First execution crashed** in the Jacobi solve (scipy's brentq refuses rtol = 4e-16, below its 4·eps floor), before any satellite number was computed. Only the host, coordinate and orbit controls had been printed. rtol was set to 1e-15; nothing else changed.
- **C-HOST's frozen tolerance** cannot hold: I left out ν_mono's +½ term. Before the first run I saw it would fail, kept it unchanged, and added a labelled diagnostic.
- **Load-bearing scope:** the frozen text makes only the mode's own check load-bearing in MUTATE runs, but the first script version left H1, H2 and C-HOST load-bearing in every mode. I scoped the flags to the main mode before any MUTATE run and re-ran the main mode. Its `.out` (apart from the run-time lines), its JSON numbers and checks, the CSV and the npz are all byte-identical.
- **The host variants** (rows 1 and 2) find pericentres by the exact (E, L) root on the same draws (validated by C-ORB) and keep the main run's no-pericentre-within-t_H flags.
- **Physics limits, stated:**
  - static spherical point-mass hosts;
  - no dynamical friction and no host growth;
  - the LMC's own field is ignored (its 7 ultra-faints and the SMC are integrated in the MW field);
  - sharp truncation only (no tidal heating or tidal tracks);
  - M31 satellites by the transfer assumption.
  None of these can move a satellite whose tidal radius is 10–35 times its estimator radius.
- `cfg286_posthoc_retained_mass.py` was written after the runs and is labelled POST-HOC.

Nothing here says the theory is closed. κ = ½ FITTED. The cold fluid's mass is still required.
