# CQB1_cq2_under_blend: FROZEN CRITERIA (2026-11-15)

kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

Committed alone, before any script or number of this lane. Lane id checked free (`ls closure_2026_11_15/`,
`git log --all --grep=CQB1`: empty). Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) m/s^2, graded separately,
never pooled.

## Commission

Item Q6 of `prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-15b_DR4_OPEN_GAPS.md`: CQ2's screening margin recomputed
with the Pi^6 blend adopted on 2026-11-07, criteria committed alone first, reported beside the seal; the seal is never
edited; if the margin does not hold, that is recorded before the data and comes back to the owner. The gap is named in
`closure_2026_11_12/DR4MAP_gaia_dr4_registry_map/DR4_MAP.md` section 6.

## Question

With the adopted Pi^6 blend as the stiffness, does CQ2's sealed wide-binary prediction
(`cq_lanes_2026_11_04/CQ2_v3s_dr4_seal/SEALED_PREDICTION.md`: screened, Newtonian; gamma_r - 1 = 4.450e-05 canonical /
4.013e-05 alt at 30 kAU, primary field 1.9e-10 m/s^2, L* floor 21.682 / 22.849 pc) still hold, on each footing?

## What is being compared (fixed from the record, read only)

- **Raw stiffness (what CQ2 solved):** -(gamma_L/2) [max(Sigma, 0)]^2, Sigma = D.P for v3s.
- **Adopted stiffness:** F = gamma_L b^2 f(Sigma/b), b = rho_DE
  (`closure_2026_11_07/OWNER_DECISION_2026-11-07_ADOPT_PI6_BLEND.md`). f is AC21 iter_6's form: f'' as the exact
  rational pieces in `action_search_2026_11_05/AC21_smooth_3d/iter_6_fast_decay/form.json` (sha256 77a58d28fb...,
  commit 63242d3e1e) on (0, 1], f'' = 1 above 1, f(0) = f'(0) = 0, f = 0 for q <= 0.
- **Field equations:** QX17D's certified reading R2 (QX17's equations with Sigma_+ read as F'(Sigma), and the stress
  term Sigma F'(Sigma) h_mn in place of 2F h_mn). In CQ2's static weak-field limit the stiffness enters only as
  gamma_L grad F'(Sigma) (C6's (L)/(P_L) form, which for the raw form is (L*^2/2) grad(div p)).

## The frozen region ("everywhere the seal's solution lives")

As CQ2's own criteria (step 2 and check K4) define it, on each footing:

- **R1, Galactic environment over the DR4 sample volume.** The six X3 D2 rows of that footing
  (`rebuild_2026_10_22/X3_switched_stiffness/x3_switched_stiffness_results.json`, key D2; x_e 1.15 and 2.6;
  L* floor, 24, 90 pc): the Galactic phantom's minimum over R 7.2-9.2 kpc, |z| <= 1 kpc (a box that contains every DR4
  pair: the frozen pipeline cuts d < 250 pc and s 2-30 kAU), minus 2.5 times the row's deepest negative lobe of a
  1 Msun point mass (M_tot <= 2.5 Msun, as CQ2). Sigma_R1 = rho_gal,min - 2.5 x lobe.
- **R2, the near zone.** The Galactic phantom at the Sun (X3's H4 C3 minimum and X3's own at-Sun value for the
  footing, the smaller of the two), with the binary's own response added. Within 24 pc of a point mass that response is
  the hedgehog's positive divergence (X3's negative lobes start beyond 24.8 pc), so it can only raise Sigma; this is
  checked (check S3).
- **R3, the model's domain.** CQ2 solves a linear response on an infinite uniform background, so inside its model
  Sigma >= Sigma_R1 everywhere. R1's minimum therefore bounds the whole model domain; no separate number.

Sigma/b is evaluated at every R1 row and at R2; its minimum over R1 and R2 on a footing is that footing's margin.

## Steps and checks (each line frozen; PASS / FAIL printed)

**K0, inputs pinned.** sha256 of CQ2's `cq2.py` and `cq2.json` equal the values printed in SEALED_PREDICTION.md
(6fbf2abfe5... and a73f754ced...); form.json and X3's json equal the hashes above (X3: 8d63aac13d...).

**Step 1, known answer (before anything new).**
- **KA1** A byte-identical copy of CQ2's `cq2.py` (sha256 6fbf2abfe5...) placed in this lane folder (same depth below
  the repo root, so its repo-relative reads are unchanged; it writes its outputs into this folder, never into CQ2's)
  is run once, unchanged, main mode only. PASS if, on both footings, the binary switch margin (CQ2 json
  `switch.min_binary_margin`), the near-zone minimum, every gamma_r - 1 entry on the sealed grid at the primary field,
  the DR3 Q_pred values and every pipeline gamma_inf reproduce CQ2's committed `cq2.json` to max relative 1e-9, and its
  checks K1-K7 print PASS.
- **KA2** This lane's own copy of Route F (copied from cq2.py, not imported) gives gamma_r - 1 at s = 1, 10, 30 kAU,
  1 Msun, primary field, L* floor, equal to CQ2's json to max relative 1e-9, both footings.

**Step 2, Sigma against b, same quantity, same units.**
- **U1** rho_DE from the a0 law in SI, this lane's own constants (G 6.67430e-11, c exact, IAU nominal GM_sun /
  G, pc = 648000/pi au): rho_DE = a0^2 / (kappa^2 c^2 G), kappa = 1/2, in kg/m^3 and Msun/pc^3, each footing.
- **U2** The b used by the blend's own lanes (QX19 `qx19.py`: G = c = 1, K = 4 pi, b = s^2/2 = 4 (a0/c^2)^2, in m^-2)
  equals G rho_DE / c^2 from U1: relative difference <= 1e-12 on both footings.
- **U3** Sigma's normalisation. From the action's static limit (p = K P, Sigma = D.P = div P, (L): lap Phi = K rho +
  div p, K = 4 pi with G = c = 1): Sigma = G rho_ph / c^2 with rho_ph = div p_SI / (4 pi G). X3's reported D.P
  (Msun/pc^3) is computed as div p_SI / (4 pi G) / (Msun/pc^3) (read from `x3_switched_stiffness.py` task_D2). PASS if
  that unit chain is the stated one and X3's Msun/pc^3 constant agrees with this lane's to <= 1e-3 relative; then
  Sigma/b = rho_ph / rho_DE with both in the same units. A cross-reference (not a gate): TC1 N2's "Sigma/X = 2 +
  rho_ph/rho_DE" for AC2q.
- **U4** Independent SI estimate of the Galactic phantom (this lane's own code, not X3's solver): simple-nu QUMOND
  about a spherical Hernquist Milky Way (M_b 6e10 Msun, a_H 3 kpc; also M_b 4e10 and 8e10, a_H 2 and 4 kpc as a
  range) at R0 = 8.178 kpc: (a) off the plane, the spherical phantom at |z| = 1 kpc; (b) in the plane, that term plus
  (nu - 1) rho_b,0 with a local baryon density 0.08 Msun/pc^3 (an assumed round value). Reported against X3's box
  minimum and at-Sun value as a factor. The label gate uses the margin divided by the worst disagreement factor
  (>= 1) over the range, so a unit or solver slip smaller than the margin cannot change the label.
- **S1** (exact, sympy, from form.json) f(1) = 1/2, f'(1) = 1, f''(1-) = 1, so f = q^2/2, f' = q, f'' = 1 for
  q >= 1; F = Sigma^2/2, F' = Sigma, F'' = 1, dF/db = 0 and Sigma F' = 2F for Sigma >= b; f = f' = 0 for q <= 0.
  Also reported: min and max of f'' on [0, 1] and the q where f'' = 1 below 1/2.
- **S2** min Sigma/b over R1 and R2, each footing, and the margin after U4's factor.
- **S3** Near-zone sign: every X3 D2 row's negative region starts beyond 24 pc (> 30 kAU = 0.145 pc by a factor
  >= 100), and the analytic hedgehog divergence M/(2 pi L*^2 r) is positive; so the binary's response only raises Sigma
  where the binary lives.
- **S4** Galactic inputs: x_e = g_obs/a0 is an observed input to CQ2 (1.778, 1.9, 2.32 e-10 m/s^2) and does not
  depend on the action, so the blend cannot move it. rho_gal enters CQ2 only through the switch margin. Its
  dependence on the stiffness is X3's recorded far-region estimate (L*/R)^2 (json D2 `far_effect_estimate`); the
  blend changes the stiffness in a layer region by at most the factor max(1, max f'' on [0, 1]). PASS if that
  estimate times that factor is < 1e-3 (the margin moves by under 0.1 %).

**Step 3, branch.**
- If, on a footing, min Sigma/b >= 1 after U4's factor and S1-S4 pass: the static equations CQ2 solved are the same
  equations under the blend on an open set containing the whole frozen region (F, F', F'' and the stress term equal
  there), so CQ2's solution is a solution of the blended action with the same numbers. The sealed numbers stand.
- If some part of the frozen region has 0 < Sigma < b: recompute with the **screened local inversion** (frozen now,
  used only in this branch). Near a source in the screened state the raw equation balances gamma_L grad F'(Sigma)
  against the Newtonian field, so F'(Sigma(r)) = F'(Sigma_bg) + b h(r), h(r) = rho_hh(r)/b with rho_hh =
  M/(2 pi L*^2 r) (the raw hedgehog's divergence, in the same density units as b). Then Sigma(r) =
  b (f')^-1(f'(q_bg) + h(r)) and, in density units rho = Sigma c^2/G, the relative anomalous acceleration at s is
  4 pi G / s^2 times the integral of (rho(r) - rho_bg) r^2 dr from 0 to s. The correction factor is that acceleration
  over the raw one (GM/L*^2, recovered exactly when f' = q); the recomputed
  gamma_r - 1 = sealed value x factor, at every s of the sealed grid, source mass 0.1, 0.25, 0.5, 1.0, 1.5, 2.5 Msun,
  q_bg = the region's minimum Sigma/b; the worst (largest) value is graded. Scope: spherical, monopole, the MOND term
  enters only through the sealed F (<= 1.3 % from 1 per CQ2's K6).

## Labels (per footing)

- **MARGIN HOLDS, UNCHANGED**: KA1, KA2, U1-U3, S1, S3, S4 pass and min Sigma/b >= 1 after U4's factor over R1 and R2.
  The sealed numbers stand as they are; both CQ2 readings (V3S-REST and V3S-MOVE) carry.
- **MARGIN HOLDS, CHANGED**: part of the region has 0 < Sigma < b, and the recomputed worst gamma_r - 1 is <= the
  sealed value at every s of the sealed grid.
- **MARGIN FAILS**: the recomputed worst gamma_r - 1 exceeds the sealed value at some s. The result also says whether
  CQ2's NEWTONIAN line (max gamma_r - 1 <= 1e-3) still holds and gives the ratio to the DR4 error scale
  (sigma >= 0.02). The lane stops there, changes nothing else, and the result comes back to the owner before the data.
- **NOT EVALUABLE**: KA1 or KA2 fails (known answer not reproduced), or U2 / U3 fails (Sigma and b not shown to be the
  same quantity in the same units), or S1 fails, or q_bg <= 0 inside the region (CQ2's own K4 broken). The result says
  exactly which input is missing. S4 failing also gives NOT EVALUABLE (the margin's Galactic input is not bounded).

## Mutation twins (separate outputs `cqb1_MUTATE_<id>.json/.out`; each must fail as stated)

- **M1** (margin shrunk): b multiplied, per footing, by 4 x that footing's measured min Sigma/b, so the region's
  minimum sits at q = 1/4 inside the layer. The label must not be MARGIN HOLDS, UNCHANGED on either footing.
- **M1b** (margin shrunk, other side of the layer): the same with 4/3 in place of 4 (minimum at q = 3/4). The label
  must not be MARGIN HOLDS, UNCHANGED on either footing.
- **M2** (known answer broken): KA2 run with the two footings' L* floors swapped. KA2 must FAIL.
- **M3** (unit chain broken): b computed without the 1/kappa^2 (b = a0^2 / (c^2 G)). U2 must FAIL.
The main run exits 0 only if every gate it needs passes; each MUTATE run exits 1 when it bites.

## Hand estimate to grade

The lead's estimate, unverified: D.P about 0.0055 to 0.045 Msun/pc^3 near the Sun, rho_DE of order 1e-7 Msun/pc^3,
Sigma/b of order 1e4 to 1e5, blend equal to the raw form exactly. Graded RIGHT or WRONG against S2 and U1-U3, with
the numbers.

## Compute and house rules

One thread, `nice -n 10`, `python3 -I -B`. KA1 is CQ2's own run (about 32 s, 1.6 GB ru_maxrss); `ps -axo rss,command`
is checked for other python jobs above 2 GB before it. Everything else is light. Nothing in CQ2's folder, in any
`OWNER_DECISION_*.md`, in `PREREGISTRATION_DR4.md` or in `prep_2026/gaia_dr4_prep/` is edited; CQ2's folder must show
no change (`git status --short cq_lanes_2026_11_04/CQ2_v3s_dr4_seal/` prints nothing). No network. Commit with
explicit paths; nothing pushed by this lane.

## Outputs

`cqb1.py`, `cqb1.out` / `cqb1.json`, `cqb1_MUTATE_{M1,M1b,M2,M3}.out` / `.json`, the copy `cq2.py` with its own
`cq2.out` / `cq2.json` / `cq2.time` (KA1), `RESULT.md` with the label per footing in its first lines.

## What this lane does not do

It does not edit or re-seal CQ2, re-grade v3s, run the DR4 pipeline beyond CQ2's own reproduction, or solve the
nonlinear blended field equations in 3D. A label here is a pre-data statement about the seal, not a result about data.

kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.
