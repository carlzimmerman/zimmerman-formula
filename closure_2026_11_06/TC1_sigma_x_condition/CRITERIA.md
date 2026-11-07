# TC1 FROZEN CRITERIA: does TC03's clock-gradient catastrophe reach the QX19 one action, and does it fire on physical data?

Committed alone, before any TC1 script or number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing; the owner
adopts. No LCDM input, no dark-matter particle. Footings canonical a0 = 9.3603e-11 and alt a0 = 1.1312e-10 m/s^2,
graded separately, never pooled.

Lane id: `ls closure_2026_11_06` and `git log` show no TC1 lane. The TC01..TC07 checkpoints of
`theory_closure_2026_11_06/` are a different namespace (the other agent's packet); "TC03" below always means that packet.

## Disclosure (what was read before freezing)

Read before writing this file: CLOSURE_FINAL.md erratum; FRW_RECONCILIATION_CHAIN/CHAIN.md (J1-J4);
EQUATIONS_IN_ORDER.md erratum; QX19 README and qx19.py blend block; AC21 FROZEN_CRITERIA T4 (f = 0 for q <= 0);
TC03 `einstein_transfer/evolution/FORMATION.md`, `auxiliary/DERIVATION.md`, `regular_frame/local_existence/ASYMMETRIC_PULSE.md`
and `FORMATION.md`; AC10 README and ac10.py; AC14 README; SV3 criteria; the stored AC10 `parts/` JSON for the 12 AC2q
subset rows (labels, t_fold_all, J_min, v_max, tau_f_s, Pi0/s2). Those stored numbers are known: every AC2q row folds
at t_fold_all = 1.068-1.078 tau_f, tau_f = 2.6e14-5.9e15 s; Pi0/s2 = 1 (clock-only), 91-2.2e4 (phantom),
-89 to -2.2e4 (soft). No TC1 run has been made.

## The question, made exact

QX19's action (A2) is AC2q (A1) with the stiffness density [max(Sigma,0)]^2/2 replaced by F = b^2 f(Sigma/b), b = X,
Sigma = D.P + 2X. AC21 T4 fixes f = 0 for q <= 0 and f = q^2/2 for q >= 1. So the two densities are equal on the open
set O = {Sigma > X} union {Sigma < 0}, and differ only in the layer L = {0 < Sigma < X}. CHAIN J1 records the Sigma > X
half. On any solution whose state stays in O (on an open neighbourhood of the event), A2's solution is A1's.

Two decisions:
- **(J3, mathematical transfer).** Can TC03's constructed formation family be kept inside Sigma > X through its
  bootstrap? If yes, N4-N5 hold for A2, and QX19's well-posedness PASS is local only.
- **(Physical firing).** Does any physically reached configuration sit in O and undergo a clock-gradient catastrophe
  (first proper-spatial derivative of the clock norm/rapidity unbounded at bounded amplitude; in the planar label code,
  a fold J -> 0 with v finite) within the age of the universe, 13.8 Gyr = 4.35e17 s?

TC03's own variables: r = sqrt(2X), D = (A r - 1 - gamma r^2)/gamma on the on-branch, so Sigma = D + r^2 and
Sigma/X = 2 + 2D/r^2. AC10's planar variables: Pi = D.P + s^2 with s^2 = 2X, so Sigma/X = 2 Pi/s^2 (= 2 Pi_c/(J s^2)).

## Checks (script `tc1.py`, outputs `tc1.json` / `tc1.out`; heavy part `tc1_runs.py`, checkpointed per row)

**S1, densities equal on O (sympy, exact).** With f built from AC21 iter_6 `form.json` exactly as qx19.py does:
F(Sigma, X) - max(Sigma,0)^2/2 and its partial derivatives in Sigma and X vanish identically for Sigma >= X and for
Sigma <= 0; F differs from it at some point of (0, X). PASS iff all three hold.

**S2, TC03 background and margin (sympy, exact).** At D(r0, A0) = 0: Sigma/X = 2 exactly. Exact
Sigma/X - 2 = 2D/r^2 on r = r0(1+u), A = A0(1+a). Margin eps1(z0) = the largest |u| (with |a| <= |u|) keeping
|Sigma/X - 2| <= 1/2, z0 = gamma r0^2, reported on z0 in {1e-17, 1e-6, 1e-2, 0.1, 0.25, 0.45}. Also at D = 0:
c^2 = z/(z + (1-z)^2) (must equal CHAIN E4) and G = 3(1 - c^2) - h H_rrr/R^2 > 0 on (0, 1/2].

**J3 rule.** J3 HOLDS iff S2 gives eps1(z0) > 0 for every z0 in (0, 1/2) (analytic, from the exact expression). Reason
frozen here: FORMATION.md section 4 gives a positive T0 for any fixed compact admissible box containing the initial
range in its interior, and section 5 gives T_k <= C_eps/k < T0 for large k. The box B' = B intersect
{|Sigma/X - 2| <= 1/2} is such a box once eps < eps1(z0). Every state before T_k lies in B', hence in Sigma > X, where
A2 = A1 (S1). If S2 fails, J3 is NOT SHOWN.

**KA, TC03's catastrophe time on its own fixture.**
- KA1: the asymmetric pulse of ASYMMETRIC_PULSE.md: max(-psi')/max psi' = 8 to 1e-6 (numerical, fine grid).
- KA2: the comparison system Q' = kappa Q^2 - C(Q+P+1), P' = -kappa P^2 + C(Q+P+1), with Rcmp = 1.01 max(1, 6C/kappa)
  and Q0 = P0 + Rcmp (+ larger Q0), on a grid of (kappa, C, P0): integrated blow-up time t_b <= 2/(kappa Q0) on every
  row, and Q - P non-decreasing. PASS iff all rows.
- KA3: the AC10 rerun below reproduces AC10's stored AC2q t_fold_all at N = 2000 and 4000 to 1e-6 relative.

**N1, physical planar rows with the QX19 action (numerical).** AC10's declared 12-row AC2q subset (11 and 156 kpc,
w 68.75 km/s, low M-1 end, Lstar minimum, phantom / clock-only / soft, both footings), physics imported unchanged from
`action_search_2026_11_05/AC10_nonlinear_clock/ac10.py` (read-only). Two models per row: AC2q (stiffness
max(Pi,0)) and QX19 (stiffness F'(Pi) = b f'(Pi/b), b = s^2/2). Ladder N = 2000, 4000. Recorded on saved samples up to
the first fold: min and max of Sigma/X = 2 Pi/s^2 over interior (graded) cells, and the fraction of interior
cell-samples in L. X itself is not evolved by the PN code; its shift is bounded by (v_max w/c)^2, reported.
Per row:
- region IN (Sigma > X) iff min interior Sigma/X > 1 + 1e-6 throughout; OFF-SIDE (Sigma < 0) iff max interior
  Sigma/X < -1e-6 throughout; else LAYER;
- QX19 fold = AC2q fold iff |t_QX19/t_AC2q - 1| <= 1e-3 at N = 4000;
- fold converged iff |t(4000)/t(2000) - 1| <= 1e-3 (AC10's ladder tolerance);
- within age iff t_fold_all x tau_f_s < 4.35e17 s.

**N2, static region census (reported; no catastrophe can fire on a time-independent regular solution).** Spherical
QUMOND phantom density rho_ph = (4 pi G r^2)^-1 d/dr[r^2 (nu(y) - 1) g_N], y = g_N/a0, nu = 1/2 + sqrt(1/4 + 1/y)
(QX8's nu), and Sigma/X = 2 + rho_ph/rho_DE with rho_DE = a0^2/(kappa^2 c^2 G) (AC10's mapping, kappa = 1/2).
SPARC rotmod (all galaxies on disk, Upsilon_disk 0.5, Upsilon_bulge 0.7) and the 12 X-COP clusters (M_gas + M_star from
the on-disk FITS), both footings. Reported: fractions of radii in Sigma > X, in L, in Sigma < 0, and min Sigma/X.
If the X-COP files do not load, the X-COP census is NO VERDICT; the lane label does not depend on N2.

**Other configurations (analytic statements, frozen here):**
- FRW: homogeneous, Sigma/X = 2, e w+- = 0, so Q = 0 for all time: NO FIRE.
- Linear growth: the linear operator is A1's (J2), and a linear system with bounded coefficients has no finite-time
  gradient blow-up: NO FIRE at linear order; dips d >= -X stay in Sigma > X (Lean `frw_pert`). The nonlinear stage
  is the N1 question.
- Moving Sun: no frozen nonlinear verdict on record (AC15 NO VERDICT; another lane is running it): NO VERDICT,
  reported with bracket, not graded here.

**P (planted controls, always run).** P1: a homogeneous Sigma/X = 2 state carrying KA2's cone data must be classified
IN and FIRES (t_b <= 2/(kappa Q0)). P0: the same state with Q0 = P0 = 0 must be classified IN and NO FIRE.

**MUTATE (`TC1_MUTATE=1`, separate outputs `*_MUTATE.*`).** The blend scale is planted at b = 4X. Then clock-only rows
sit at Sigma/b = 0.5, inside the planted layer. The region classifier (with the planted layer 0 < Sigma < 4X) must
flag the clock-only rows LAYER, and the S1 equality must fail at Sigma/X = 2. The run must exit 1. If it does not, the
classifier has no power and the lane label is NO VERDICT.

## Lane label (frozen)

- **FIRES** iff J3 HOLDS and at least one N1 row with region IN (Sigma > X) is a converged fold within the age, with
  QX19 fold = AC2q fold, on both footings. The region is named as the N1 configuration.
- **UNCONDITIONAL** iff no N1 row in O folds within the age and J3 is decided either way.
- **NO VERDICT** otherwise, with the bracket stated (which rows, which check failed).

**QX19 rows lost (frozen reading of QX19's recorded row text).** A PASS row is LOST iff its own statement asserts
global-in-time classical regularity, or a property of a nonlinear time-dependent evolution past the fold time. Read
now from QX19's README: SPARC/RAR, Cassini/PPN, static limit (static field statements); GW speed/tensor mass, lensing =
dynamics (static or linear wave statements); PN sign (HF limit); FRW health, galaxy linear health, slow frozen roots
(linear); well-posedness across the switch (local Hadamard / AC21 3D symbol / AC22 converged curved 2D). None of these
asserts global regularity, so under FIRES no PASS row is lost; the well-posedness row is re-scoped to local-in-time and
the "Nonlinear fold" row (RUNNING in QX19) takes the N1 result. Reachability of the static states through a folding
collapse is postbreak physics (CHAIN N8, OPEN) and is stated as a scope limit, not graded here.
Under UNCONDITIONAL, all rows stand and the CONDITIONAL is removed.
