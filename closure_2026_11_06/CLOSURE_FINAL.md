# Closure, 2026-11-06: one table, every gate

Consolidates the 11-06 swarm (rules: SWARM_BRIEF.md). It changes no lane's label and adopts nothing; the owner
adopts. Kappa = 1/2 FITTED; not theory closed. Each label is the lane's frozen label. A post-data reading is shown
only where the lane itself gives one, and is marked as such.

**Action on the table.** v3s, adopted and scoped (closure_2026_11_05/CLOSURE.md section 1). AC2q is the candidate
successor; AC7 introduced it.

**Repair on the table, NOT adopted.** Replace the stiffness kink max(D.P, 0)^2 with AC21's iter_6 blend: a pure
Pi^6 near zero, C4-blended to (gamma/2) Pi^2 above b, with b = rho_DE (v3s) or b = X (AC2q). It adds no new
constant.

**Equation chain.** EQUATIONS_IN_ORDER.md (QX1). Every step is tagged LEAN / SYMPY / NUM / POSTULATED. QX1 has 28
Lean theorems, 0 sorry, standard axioms only. The lanes add more Lean files (QX2-QX7, AC20, AC21), each with a
MUTATE twin.

## Gates

| Gate | Label | Lane / commit |
|---|---|---|
| SPARC / RAR on the action's exact AQUAL field | PASS, both footings (rms 0.0560 at U 0.58 canonical, 0.0558 at U 0.52 alt; alt previously failed U on the law) | QX8 3ba7c78ce6 |
| FG1 Upsilon-tilt row on the exact field | FAIL canonical (+0.170 vs 0.15; bootstrap sd 0.127), PASS alt (+0.090) | QX11 1883bb4d2e |
| QX8's per-galaxy Vflat slope | NO VERDICT (the planted control recovered half). Post-data: an artefact of grid-edge Upsilon; not PAPER67's statistic, so no erratum | QX9 cd94913d33 |
| Solar System, PPN, c_T, galaxy lensing (v3s) | PASS (carried) | C6P, V3W W1/W3/W4a |
| AC2q tensor speed and lensing slip | PASS | AC9 29eb0c2bf9 |
| PN sign, all directions, high-frequency limit | PASS, scoped (v3s and AC2q) | AC17 61b2a2fde9 |
| Well-posedness, raw max switch | FAIL across the switch: no C1 solution for generic data. Each branch is well-posed on its own | AC16 6d5faba9bd |
| Well-posedness, Pi^6-blend repair | 3D condition m > d+2 proved analytically (AC21); curved 2D C1 and C2 PASS, converged (AC22). Not adopted | AC21 63242d3e1e, AC22 23b4be92bf |
| AC2q slow frozen roots, dark-energy-like backgrounds | PASS (HARMLESS, scoped): 16 fresh powered witnesses, R <= 2.70, det K > 0. eps_phi = 2 stays NO VERDICT | AC23 43009b6e76 (AC5, AC13 NO VERDICT) |
| Clusters, every static term of v3s / AC2q | FAIL, no-go: no universal nu; clock, stiffness and K(Q) all short | QX2 34a3050f18 |
| Clusters, new keyed terms | FAIL: p/rho, khronon velocity, enclosed density and gas-g are dead; the depth key works only if clusters set it | QX5 00f9e19c9b |
| Clusters, depth key derived from the action | FAIL: not derivable; groups overlap galaxies on that key | QX6 cefca47d52 |
| Clusters, virial-shock-heated sector with entropy floor | FAIL (under): X-COP +0.463/+0.430 at the galaxy-set floor; the post-result Lean class_bound covers every shock radius and upstream density in the isentropic class; the floor violates adiabatic J0 by 6000x | QX13 10eb35b351 |
| CMB lensing + growth inside the current action | FAIL, no-go (clock Jeans; K(Q) 500x gap; barotropic class) | QX3 0240c8e31d, 602db4263d |
| Switched cold-dark-energy sector, window | KILLED: host galaxies retain the sector, and KiDS lensing is over-predicted by 0.15-0.27 dex. The primary TT/TE/EE as a cold component fit (chi2 6718 vs 6497) is NO VERDICT (J1) | QX7 9a8f2e4778, QX10 f8d51400c8 |
| Constraint triangle (cold early / not retained by galaxies / clusters + groups) | RUNNING: iter_1's universal-density no-go does not fire (statics only) | QX12 8ea6100c3f |
| AGC 114905 | FAIL: NOT RESCUED by EFE, both footings. The owner-approved census finds no spectroscopic neighbour within 1 Mpc / +-500 km/s, and the record's field is ~1e-3 a0 against the 0.076 a0 needed (QX4 iters 1, 3 already NOT RESCUED) | QX4 beabff85b5, QX14 1e5ab2c2d9 |
| Malin 1 | FAIL: no mechanism in the action | QX4 beabff85b5 |
| FN6 window source | FAIL for v3s / AC2q, on a post-result control; NO VERDICT as frozen | AC19 f747d27e9e |
| Nonlinear fold (full grid) | RUNNING | AC14 |
| Moving Sun, nonlinear halo | RUNNING | AC15 |
| Constraint causality | RUNNING | AC18 |
| kappa | FITTED; Lean proves it is not derivable from the premises | KAPPA_LOGIC_2026_10_20 |
| a0(z), wide binaries | Wait on data (ALMA proposal-class sample, Gaia DR4 around 12-02) | AT2, prep_2026 |

## Waiting on the owner

- Downloads: the AGC 114905 census was approved 11-06 and is done (QX14). Planck PR4 / ACT primary spectra
  (QX10_window_hardening/iter_1_primary_cmb/NEEDS_OWNER.md).
- Adoption: the Pi^6-blend stiffness repair.

Kappa = 1/2 FITTED; not theory closed.
