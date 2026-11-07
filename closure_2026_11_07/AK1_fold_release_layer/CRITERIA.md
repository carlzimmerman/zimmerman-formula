# AK1 frozen criteria: does the certified fold machinery show the outside solver's layer and release speed?

Frozen before any AK1 script or number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No dark-matter
particle. No LCDM input. Both footings graded, never pooled.

## The claim under test (closure_2026_11_07/ARGON_RESPONSE_ASSESSMENT_2026_11_07.md, Q1)

- Critical layer: lambda_crit = (L*^2 c^2 / a0)^(1/3).
- Release: (1/2) v_k^2 = 2 a0 lambda_crit, so v_k = 2 c (a0 L* / c^2)^(1/3), which is host-independent.

The claim's own numbers are used:

| footing | a0 | L* | lambda_crit | v_k |
|---|---|---|---|---|
| canonical | 1.2e-10 | 21.7 pc | 22.53 kpc | 577.6 km/s |
| alt | 1.1e-10 | 22.9 pc | 24.04 kpc | 571.3 km/s |

**Disclosure 1: lambda_crit is ~22-24 kpc, not ~2 kpc.** The assessment and the lane brief quote "~2.1-2.25 kpc".
The formula gives 22.53 / 24.04 kpc (pc = 3.0857e16 m), and only those values reproduce 577.6 / 571.3 km/s through
4 a0 lambda_crit. The brief's figure is a factor-10 slip. AK1 grades against the formula values. With the
record's footing a0 values (9.3603e-11 / 1.1312e-10), lambda_crit is 24.47 / 23.81 kpc and v_k is 531.7 / 576.6 km/s.
These are reported, not graded.

## Disclosure 2: what the machinery is, and where D.P = 0 sits in it (read from code, no numbers run)

The certified fold machinery is AC10's planar label system with FS1/FS2 scheme S:
- `closure_2026_11_06/FS2_fold_viscosity_free/`, criteria 1a686ed9a2, result fd29a9fc84;
- 240 AC2q + 240 v3s rows.

Units, per row:
- speed: the stream's crossing speed w (68.75 or 74.8 km/s);
- time: tau_f = w / (2 g_host);
- length: ell = w tau_f. Across the grid ell runs from 0.59 kpc (11 kpc host) to 15.5 kpc (156 kpc host);
- stiffness: gamma_hat = L*^2 / (2 ell^2).

The stream occupies q in [-3, -0.05] ell.

The switch argument D.P is the cell charge Pi = Pic / J. Pic is constant along each label, and pressure acts only
where J > 0. Therefore:
- **sign(D.P) never changes along a label in these runs.**
- Clock-only and phantom AC2q rows have Pi > 0 on every pressure cell. The FS2 clock shock is on the stiff side,
  not at a D.P = 0 crossing.
- D.P = 0 interfaces exist only:
  - spatially, at the tapered edges of the soft rows (interior Pi < 0, switched off);
  - in folded cells (J <= 0), where the code switches pressure off.

The assessment's reading that "the branch is crossed in dynamical collapse" is therefore tested here as: what layer
and what speed does the collapse produce, wherever it happens. AK1 also records min Pi over pressure cells
(Disclosure 3).

The "M234 / M490 hosts" named in the brief are AC15/AC24's moving-Sun 3D runs, not collapse runs. They are outside
this machinery and not graded. The host axis graded here is the AC14 depth grid:
- 5 host radii, 11-156 kpc;
- w in {68.75, 74.8} km/s;
- the M - 1 bracket;
- L* in {21.7 or 22.9, 90} pc;
- both footings.

## Protocol adopted, tightened or rejected (ARGON_AK1_PROTOCOL_2026_11_07.md, filed before any AK1 number)

The protocol's three regimes:
- I: width ~L*, v 1-100 km/s;
- II: width (L*^2 r_M)^(1/3), v 35-180 km/s;
- III: width lambda_crit, v 578 / 571 km/s, flat.

Lines:
- **Adopted (graded):** the protocol's two observables.
  - R_delta = FWHM of the |d(D.P)/dx| pulse over lambda_crit. D.P = Pi = Pic/J on pressure cells; the Eulerian
    gradient is taken across neighbouring pressure cells; the FWHM is the Eulerian extent where the pulse exceeds
    half its peak, around the peak. It is read at t_reg (first interior J <= J_reg, FS2's viscosity-free event) and
    at both snapshots.
  - v_post = the mass-weighted rms of (v - v_bulk) over the nodes of the collapsed cells (J <= J_reg). v_bulk is
    their mass-weighted mean. Read at both snapshots.
  - The gates are the protocol's: 0.5 <= R_delta <= 2.0 and 500 <= v_post * w <= 650 km/s.
- **Adopted and tightened:** flatness. The fitted |d ln v_post / d ln v_f| across the AC14 depth grid, with v_f taken
  as the row's max infall speed before t_reg, must be <= 0.1 for CONFIRMED.
- **Tightened:** CONFIRMED needs BOTH gates on every graded row (below), both footings, both snapshots, converged. W
  (collapsed-layer thickness) and V (max |v|) are reported beside them.
- **Rejected:** the protocol's lambda_crit values 2.09 / 2.25 kpc (Disclosure 1). The formula gives 22.53 / 24.04 kpc,
  and AK1 grades R_delta against those. R_delta against 2.09 / 2.25 kpc is reported.
- **Rejected:** M234 / M490 as hosts. They are moving-Sun runs (Disclosure 2). "Both hosts" is replaced by the AC14
  depth grid.

### Code-unit mapping and what the run can see (frozen)

- **Mapping, per row:**
  - speed unit w = 68.75 / 74.8 km/s;
  - time unit tau_f = w/(2 g_host);
  - length unit ell = w tau_f (0.59-15.5 kpc);
  - gamma_hat = L*^2/(2 ell^2), so L* enters only through the stiffness;
  - s^2 = 32 pi a0^2 tau_f^2 / c^2 (K s^2 = 8 pi G rho_DE with rho_DE = a0^2/(kappa^2 c^2 G)), so a0 and c enter only
    through the clock charge;
  - phantom charge Pi_ph = K rho_ph tau_f^2.
- **The footing a0 is the record's** (9.3603e-11 / 1.1312e-10). The claim's 1.2e-10 / 1.1e-10 are used only for its
  lambda_crit and v_k.
- **Resolution at N 8000:**
  - cell dq ell = 2.95 ell / 8000 = 0.22 pc (11 kpc host) to 5.7 pc (156 kpc host), so L* (21.7-90 pc) spans >= 3.8
    cells on every row;
  - stream extent 2.95 ell = 1.7 kpc to 46 kpc. A layer of width >= lambda_crit/2 (11.3 / 12.0 kpc) fits inside the
    stream only where 2.95 ell >= lambda_crit/2, i.e. ell >= 3.8 / 4.1 kpc: the 73 / 91 / 156 kpc hosts.
  - **Both 22 pc and ~22 kpc are resolved at once only on those hosts.** The R_delta gate is graded there only. On the
    11 / 33 kpc hosts it is reported as "domain cannot contain regime III's width".
- **Relativistic content:** the reduction is non-relativistic. The clock enters through s^2 and the stiffness through
  gamma_hat, and the X > 0 check (FS1/FS2: min X/X_bg 0.999999) says Q - 1 stays O(1e-6). Regime III, as the
  protocol states it, needs Q - 1 = O(1) inside the front, so its mechanism cannot appear in this machinery. AK1 can
  see:
  - regimes I and II;
  - whether the certified reduction, without that mechanism, produces regime III's numbers anyway.
- **Consequence for the label:** a REFUTED label reads "REFUTED within the certified non-relativistic fold reduction".
  The regime-III mechanism stays untested and is named as needing relativistic collapse machinery. AK1 reports
  max (1 - X/X_bg) over the graded runs as the measure of Q - 1 reached.

## Method (FS2's, unchanged up to the fold)

- `ak1_core.c` is FS2's core (`fs2_core.c`) with three additions:
  1. A flag that does not stop at the interior J_thr event. It is recorded, and the run continues under the same
     scheme S.
  2. Snapshots at t_reg + Delta, Delta in {0.25, 0.5} (tau_f units), capped at t_max = 6. The step is clamped to
     land on each snapshot. This only happens after t_reg.
  3. A run-wide record of min Pi = K / (gamma J) over pressure cells.
- Every line up to and including the first interior J_thr event is FS2's. KA checks this.

**Observables at each snapshot:**
- **W, the collapsed-layer thickness:** the Eulerian extent max x - min x of the nodes of all cells with
  J <= J_reg = 0.05. This includes folded (J < 0) cells and edge cells. W_kpc = W * ell.
- **W_Q, the numerical shock-front width (reported):** the extent of cells with Q > 0. The inviscid width is 0, so it
  should shrink as 1/N.
- **V, the post-collapse speed:** max over all nodes of |v| (sheet frame), in km/s as V * w. The largest speed any
  clock label carries, which is the most generous reading for a release.
- **Specific kinetic energy (reported):** e = mean over nodes of v^2/2.
  - The clock-sector part is de = e_AC2q - e_v3s at the same Delta.
  - It is reported as the speed sqrt(2 |de|) * w.

**Runs:**
- All 480 physical rows at N = 4000 and 8000.
- L* x2 (gamma x4) on every row at the lower L* (21.7 / 22.9 pc), N 4000 and 8000.

## Convergence (per row, per snapshot)

A reading is converged if, between N 4000 and N 8000:
- V and v_post change by <= 1e-2 relative, or v_post * w changes by <= 5 km/s absolute;
- R_delta changes by <= 0.1 relative, or the FWHM changes by <= 0.01 ell absolute;
- W changes by <= 0.1 relative, or the absolute change is <= 0.01 ell when W < 0.1 ell.

## Graded rows and lines

Graded rows: the AC2q clock-only and phantom rows at the lower L*. These are the rows where the clock pressure acts:
40 + 40 per footing. Both snapshots are graded. The v_post gate applies on all of them. The R_delta gate applies only
on the 73 / 91 / 156 kpc hosts (see the resolution section).

- **CONFIRMED:** every graded row, at both snapshots, converged, has
  - 0.5 <= R_delta <= 2.0 (where graded), AND
  - 500 <= v_post * w <= 650 km/s, AND
  - |d ln v_post / d ln v_f| <= 0.1.
- **REFUTED:** some graded row has a converged R_delta or v_post outside its band. The label states the measured scaling:
  log-log slopes of W_kpc and V(km/s) against ell (host depth), against L* (21.7/22.9 -> 90 pc, and x2), and against
  w, per footing. It also states which of the three named forms the speed follows:
  - 2 a0 lambda_crit: flat, ~575 km/s;
  - stored stiffness: rises with L* rho_ph;
  - well depth: tracks the infall speed.
- **NO VERDICT:** otherwise. This includes every out-of-band reading being unconverged.

## The identity's own predictions (reported with the label)

- **I1, L* x2:** if the identity holds, V moves by 2^(1/3) = 1.260 and W by 2^(2/3) = 1.587.
  - Measured ratios at x2 are reported, and at 90 pc vs 21.7 / 22.9 pc (predicted 1.607 / 1.581 for V).
- **I2, Pi^4 blend:** the identity predicts c_branch 2 -> 1, i.e. V / sqrt(2). In this machinery any blend confined to
  D.P near 0 can act only where a pressure cell has Pi near 0.
  - AK1 reports min Pi / s^2 (clock-only) and min Pi / Pi0 (phantom) over every run.
  - If those minima stay far from 0, every AK1 number is blend-independent by construction, and I2 is reported as
    "not realised: no fold number depends on the branch".

## Checks (gating; any failure gives NO VERDICT)

- **KA (FS2's fold times to 0).** For every one of the 480 rows at N 4000 and 8000, AK1's t_reg, t_fold, t_fold_all
  and step count at the event equal FS2's `parts/` files exactly (difference 0).
- **MUTATE-V (planted release, power on V).** Clock-only AC2q row 1 is rerun with the stream started at
  v0 = 577.6 / w instead of 1. Its V reading must land in 500-650 km/s at both snapshots. v_post is a velocity spread, which a uniform planted
stream does not move, so MUTATE-V2 plants the spread itself. Clock-only AC2q row 1 is rerun with the initial velocity
v(q) = 1 + A sin(2 pi k q / span), k = 20, and A chosen so that rms(A sin) = 577.6/w. Its v_post must read
>= 500 km/s at both snapshots. A reading that cannot see a
  577.6 km/s stream has no power.
- **MUTATE-0 (null).** The same row at v0 = 1 must read V and v_post below 500 km/s. If it does not, the band is not separating.
- **K-visc on the graded observables.** The 20 clock-only and 20 phantom AC2q rows of FS2's sample at the lower L*
  are rerun at N 8000 with (c_Q, c_L) = (2, 1). V and v_post must move <= 1e-2, or v_post * w by <= 5 km/s. R_delta and W must move <= 0.1, or <= 0.01 ell absolute.

## Compute

nice 15, at most 4 workers, checkpoint per row and rung, SIGTERM-safe, RSS under 1 GB. Outputs stay small:
- per-row JSON (no state arrays);
- `GRADE.json`, `grade.out`, `README.md`.

The lane is read-only on every other lane. FS2's driver and files are loaded by path.

## Out of scope

- 3D and spherical collapse, and the moving Sun.
- Any derivation of the claim's layer from the action.
- Evolution beyond t_reg + 0.5 or t_max.
