# XF1 frozen criteria: the action's own hosted state (a body moving through its host's khronon)

Frozen before any script producing a graded number exists. Kappa = 1/2 FITTED; not theory closed. Adopts
nothing; the owner adopts. No dark-matter particle. TEST lane, quarantined as HY1/BG1/PJ1 were: a result here
re-grades hosted rows of the record; it does not change the adopted action (v3s + Pi^6 blend, PAPER70 v1.8,
DOI 10.5281/zenodo.24058756). Both footings graded separately (canonical a0 1.2e-10, alt 1.1e-10), never pooled.

## Why this lane

Every hosted row in the record (Coma UDGs, the two dwarf-spheroidal samples, the KiDS satellites, the group
members, X-COP's members) was graded with a STATIC external-field state: the host's law field g_ext enters
the satellite's law as a fixed background (X1 hosted recount, "AQUAL + EFE + screening L*floor E-W"; SE2's
Coma cell with g_host = x_e a0 from the Coma beta model at the satellites' mean distance). The adopted
action's own moving-body solve (AC15, b089f97024/aa2612a47c; MS3 FINAL PASS scoped) found that a body moving
hypersonically through its host's khronon sweeps the static hedgehog away: the charge around the body is set
by global Bernoulli, gamma q = c_gal^2 + Phi_N + (V^2 - w^2)/2, and the static anomaly is not present at the
planets. AC15 lists "galaxies moving through their own khronon, where the same sweeping would act on the
phantom charge" as NOT GRADED. A Coma UDG moves at V ~ 1000 km/s through Coma's khronon while its own
internal potential is ~ (25 km/s)^2: the V^2 term dominates Phi_N by ~1e3, the same ordering that swept the
Sun's hedgehog. The question is therefore whether the static EFE state the record graded is the action's
hosted state at all. The record's Coma UDG shortfall under the static host field is +1.121 dex in sigma
(SE2 widths_half_post_freeze median, canonical, n 9); the orchestrator's synthesis quoted the isolated
plain-law shortfall of the same cell as +0.325 dex (to be RECOMPUTED here from the SE2/X1 data path, not
taken from the synthesis).

This lane adds no parameter. Everything graded is computed from the adopted action at the frozen footings.

## Stage A: the equations (sympy, exact; must PASS before Stage B runs)

Starting point: the v3s action as certified in PAPER70 (J(Y) with the Pi^6 blend, K(Q) sector at its
adopted smooth state, screening at L* canonical 21.68 / alt 22.85 pc at the floor). Not the PN mu_K = 0
reduction of AC15: at galaxy scales 2 M_theta (r/L*)^2 is ~1e5 at 10 kpc, so the screening term AC15 dropped
is the dominant one and the deep-law nonlinearity of J is live.

- A1. Derive the stationary-pattern equations for a point mass M moving at constant V through a uniform host
  khronon of background charge rho_h and host law field g_ext (constant over the body, direction free; both
  the aligned and the perpendicular cases are written). Report whether a first integral of Bernoulli type
  survives the screening and J terms; if it does, state it; if it does not, state the coupled PDE system that
  replaces it. Either outcome is allowed; "no closed equation" ends the lane NOT EVALUABLE at Stage A and
  the Stage B/C grades are not run.
- A2 (known answer). At V = 0 the A1 system must reduce to the static screened law with external field as
  used by X1/SE2 (AQUAL + EFE + screening at the floor): same equation, checked symbolically.
- A3 (known answer). With gravity off (M = 0, g_ext = 0) the A1 system must admit the uniform wind
  q = rho_h, w = -V as an exact solution.
- A4 (known answer). In the PN limit (screening term dropped, J linear) A1 must reduce to AC15's S1b Bernoulli
  relation term by term.

## Stage B: the solve

Axisymmetric 2D, time-dependent to steady, the same architecture as AC15/MS3 (hydro.py / hydro_ms3.py lineage,
checkpointed, preemptible on SIGTERM, RSS < 1 GB, one thread per run, nice 10). The axis is V; g_ext is
graded in the aligned configuration as primary and in the perpendicular one as a reported bracket if the
2D code cannot hold it (then it is declared NOT RUN, not silently skipped).

Cells (every one on both footings):

| Cell | M_b | V (km/s) | g_ext / a0 (x_e) | readout radii |
|---|---|---|---|---|
| B1 Coma UDG (SE2 cell) | SE2's per-galaxy M_* , n 9 | SE2's sigma_Coma 1000 (1D dispersion x sqrt 3 for the 3D speed) | SE2's x_e_dmean (Coma beta model) | R_e per galaxy |
| B2 MW classical dSph (X1 cell) | X1's per-row M | X1 row's host distance and the MW circular speed at it | X1's x_e per row | X1's a (half-light) |
| B3 group member (Lovisari cell proxy) | 1e10.5 Msun stellar + gas as in CE2's group path | group sigma_1D 300 x sqrt 3 | group field at 300 kpc from CE2's path | 10 kpc |
| B4 X-COP member (cluster member proxy) | 1e11 Msun | 1000 x sqrt 3 | X-COP core field at 500 kpc from CE2's path | 10 kpc |
| B5 control: the Sun | 1 Msun | 220 | MW field at 8.2 kpc | 1 AU, Saturn |

Two starts per cell (UNIFORM, HEDGEHOG = the static EFE solution), M_inf bracketed by the two V readings of
the cell as in AC15 (the two must give the same label), coarse and medium grids (convergence line 30 % on the
graded ratio as in AC15). Readout: the effective radial acceleration on a test particle at the readout radius
in the body frame, azimuthally averaged over the readout sphere (upstream, side and downstream reported
separately, the sphere average graded).

Known answers for Stage B:
- KB1. B5 must reproduce AC15's worst-bracket Earth and Saturn ratios to within 30 % (0.036 and 0.11 at the
  AC15 lines) when run with AC15's reduced equations; and when run with the full A1 system its numbers at
  1 AU must differ from AC15's by less than the AC15 convergence spread (27 %), since the screening term is
  1.2e-10 there.
- KB2. HEDGEHOG start at V = 0 must hold the static EFE solution to 1e-2 over the run (the A2 solution is a
  fixed point of the code).
- KB3. UNIFORM start with gravity off must hold the uniform wind to 1e-2 on the medium grid (AC15 KA3 line).

## Stage C: the grades

For each cell and footing, three readings of the body's effective acceleration at the readout radius:
g_static = the static EFE reading (the record's), g_iso = the isolated plain-law reading (no host field), and
g_dyn = the Stage B steady state (worst over starts, brackets and grids). Define the hosted-state ratio
D = log10(g_dyn / g_static) and the isolation fraction F = (log g_dyn - log g_static) / (log g_iso - log g_static).

- C1 (the question). F for B1, both footings, with its coarse/medium spread. F <= 0.3 everywhere: the static
  EFE is the action's hosted state to within the grading width, label FAIL (the hosted rows stand as graded).
  F >= 0.7 everywhere: the moving body is effectively isolated, label PASS at Stage C1. In between, or
  footing-dependent, or start-dependent beyond the convergence line: NO VERDICT.
- C2 (does a C1 PASS buy anything). Re-grade the Coma UDG shortfall with g_dyn in place of g_static on SE2's
  data path: the record's +1.121 dex (widths_half_post_freeze median) becomes +X dex. Line: the re-graded
  median's 95 % interval must include 0 for the cell to turn EXPLAINED; otherwise NOT EXPLAINED with the new
  number. The same for X1's MW classical and M31 rows (record: +0.32 / +0.48 dex QUMOND EFE medians).
- C3 (the sign check that kills the easy story). If the body sweeps its own phantom away (D < 0), the hosted
  rows get WORSE, not better: report D's sign per cell first, before F. A negative D on B1 is a FAIL of the
  reading "hosted rows are mis-graded in the theory's favour" even if |F| is large.
- C4 (hot rows). B3 and B4 are proxies: report D only, no re-grade of groups or X-COP (those rows are host
  rows, not member rows; the member sweep cannot by itself change the host's own hydrostatic/lensing need of
  x4.2/3.8). State this limit in RESULT.md in those words.
- C5 (Solar System guard). B5 under the full A1 system must stay under every AC15/MS3 line (Earth, Mars,
  Saturn, Cassini 5.2e-27) on both footings; a breach is a FAIL of the whole lane regardless of C1.

## MUTATE (must bite) and KA replay

- MUTATE-1: V -> 0 in every cell. F must read 0 (static EFE recovered); if the grader still prints F > 0.3
  the pipeline is broken and nothing is graded.
- MUTATE-2: g_ext -> 0 (isolated host). F must read 1 by construction; same use.
- MUTATE-3: a planted anomaly of known size (AC15's "MUTATE that bites" fix): add 0.5 dex to g_dyn in B1 and
  check C2 flips from NOT EXPLAINED toward EXPLAINED at the stated interval; if it cannot flip, C2 has no power
  and is reported NO POWER.
- KA replay: KB1-KB3 and A2-A4, all printed with their numbers in the .out.

## Label rule

- FAIL: C1 F <= 0.3 on both footings (hosted rows stand), or C3 D < 0 on B1, or C5 breach.
- PASS (scoped, hosted state): C1 F >= 0.7 both footings AND C2 turns the Coma UDG cell EXPLAINED on both
  footings AND C5 holds. Scope words required in the label: "member rows only; host rows (X-COP, groups)
  unchanged".
- NO VERDICT: anything else, with the bracket printed.
- NOT EVALUABLE: Stage A yields no closed system (A1), stated with the obstruction.

Hand estimates (frozen, to be marked HIT/MISS): HE-a: Stage A keeps a Bernoulli-type integral only in the
unscreened limit; the screened system is a coupled PDE (no first integral). HE-b: B1's F lands between 0.3
and 0.7 (NO VERDICT) because the screening length 22 pc is far inside R_e, so the sweep acts on the
unscreened far field only. HE-c: B5 passes C5 with margin > 10x. HE-d: D on B1 is positive (the host field's
suppression weakens) but C2 stays NOT EXPLAINED (shortfall > 0.3 dex remains).

Budget: Stage A < 1 h; Stage B 10 runs x 2 grids, ~8 h on 4 cores at RSS < 1 GB; Stage C minutes. Outputs:
xf1_stageA.py / .out, xf1_hydro.py (diff from hydro_ms3.py committed), xf1_grade.py, xf1.json, xf1.out,
xf1_MUTATE.out, RESULT.md. Commit with explicit paths; push via a temp detached worktree of origin/main.
