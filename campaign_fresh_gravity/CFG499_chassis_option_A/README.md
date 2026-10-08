# CFG499: option A of CFG469 as a full track (lenient black holes on the C-H/K khronon chassis)

Criteria frozen first: [FROZEN_CRITERIA.md](FROZEN_CRITERIA.md), commit 3b820a1ec, committed alone before any script.
A dated correction section was appended after the runs (post-hoc; nothing frozen was edited). Theory plus offline
numerics; no downloads; every other lane is read-only. The owner (10-08): "try both A and C". This lane is A; a parallel
lane does C.

| run | output files | checks | exit code |
|---|---|---|---|
| main | `cfg499_option_a.out`, `cfg499_results.json` | 13/13 checks pass | 0 |
| MUTATE (`CFG499_MUTATE=1`) | `cfg499_option_a_MUTATE.out`, `cfg499_results_MUTATE.json` | all three flips happen | 1, as required |

    python3 campaign_fresh_gravity/CFG499_chassis_option_A/cfg499_option_a.py
    CFG499_MUTATE=1 python3 campaign_fresh_gravity/CFG499_chassis_option_A/cfg499_option_a.py

About 6 minutes (main, including the collapse) and 3 minutes (MUTATE). `cfg499_lib.py` holds the second-order Lagrangian
engine and the series tools; `cfg499_collapse.py` holds test (2). The symbolic cache goes to the system temp directory.

## Verdict

| test | result | the deciding numbers |
|---|---|---|
| (1) metric-coupled moving black hole | **PASSES** (at the order computed) | the UH defect stays hidden and gets *milder*: metric response x^1.618 (C^{1,0.618}), curvature x^+0.618 (bounded); no exponent shift, no logs; count unchanged |
| (2) collapse | **FAILS by the frozen rule**, on two clauses that encoded a wrong expectation; **PARTIAL** under the dated correction | the UH forms: lapse decays at kappa = 0.5443310540 vs kappa_U = 2 sqrt6/9 (dev 2e-12); the weak branch is selected; alpha > 0 C-vs-C' selection is an argument only |
| (3) window with every gate | **PASSES** | no-constant sliver open for c_2 >= 0.0347: alpha_c in [9.624e-14, 9.93e-14 / 1.08e-13 / 1.18e-13] at c_2 = 0.0383 / 0.0506 / 0.0667, all 12 gates pass; with the hierarchy [9.624e-14, 3.2e-9] at every chosen c_2 |

- **Frozen-rule verdict: A WEAKENED, named item (2), clauses 2a(ii) and 2a(iii).**
- **Under the dated correction (post-hoc, the owner's call): A NOT DECIDED, open item 2c** (the alpha > 0 selection of
  option C over C' inside the boundary layer is not computed).
- Nothing computed here shows collapse forming something worse than the weak-defect UH. The frozen fail is a criterion
  error, stated as such; it is still reported as the frozen outcome.
- Option A's standing conditions are unchanged: the owner must adopt reading W (under the RB2019/FHB2021 strict criterion
  G12 is still a KILL), and the full window needs the Pospelov-Shang hierarchy (+1 UV scale M_* <= 9.87e8 GeV).

## Test (1): the metric-coupled moving black hole

**What was computed.** The full quadratic action sqrt(-g)[R - lambda K^2 + alpha a.a] for the O(v), l = 1 sector: six
metric functions plus the khronon F, angle-integrated (sympy), on Schwarzschild plus CFG319's test-khronon background
(rebuilt as a series from CFG319's r_UH and y1 at each of the five window points). Then the first round trip of the
back-reaction, local at the UH:
- F0 = the test-khronon UH modes (s+, -1, 0);
- h1 = the Einstein response to F0's O(v) stress (all six Einstein equations solved, gauge C = E = Kf = 0);
- F1 = the khronon equation's response to h1.

**Controls (all pass).**

| control | result |
|---|---|
| K1 | the same engine on flat space gives omega^2 = lambda (2 - alpha) k^2 / (alpha (2 + 3 lambda)) exactly, tensor speed 1 (fixes the sign and normalisation of R against the khronon terms) |
| K2 | at h = 0: S22, dK and d(a.a) equal CFG319's committed expressions exactly |
| K3 | a pure-gauge l = 1 metric annihilates all six Einstein-Hilbert equations exactly |
| K4 | the khronon equation annihilates the joint pure-gauge (h, F) on an on-shell background (3e-57); off shell it does not (3e-3) |
| K5 | h1 solves all six Einstein equations (including the gauged-away ones) to <= 6e-48 relative; F0 solves its equation to <= 2e-37 |

**Results (identical in structure at all five window points).**

| UH mode | stress (Einstein sources) | metric response h1 | curvature dR, dKretschmann, every Riemann component (EF basis) | feedback into the khronon equation |
|---|---|---|---|---|
| s+ = 0.6180-0.6182 (option C) | x^s+ (bounded, vanishing) | B ~ x^(1+s+) = x^1.618, A, D ~ x^2.618 | x^0.618 (bounded) | x^(s+ + 1): one order above the mode, no resonance, no exponent shift |
| -1 (UH displacement) | analytic | analytic (x^0), no log | analytic | x^1, misses the resonant powers -1, 0: no log |
| 0 | analytic | analytic, no log | analytic | x^1, no log |

- **1a weak: pass.** The metric stays C^{1,0.618}; the curvature perturbation is bounded at O(v).
  - This is milder than CFG319/CFG469's estimate ("Ricci ~ x^-0.382"). That estimate was an argument from the gradient of
    d(a.a). The computed O(v) stress is bounded in every component: the cross-coupling coefficients vanish at the UH
    fast enough to cancel the gradient.
  - Still a defect: the khronon's own scalars keep grad d(a.a) ~ x^-0.382 (CFG319), and tau is C^{1,0.618}, not C^2.
- **1b hidden: pass.** h1 is continuous and vanishes at the UH, so tau = -exp(-kappa_U T) stays C^1 with a timelike normal
  in the perturbed metric, and T -> infinity on the UH in every direction.
- **1c count: pass, Delta_len = 0.**
  - (i) every homogeneous solution of the gauge-fixed Einstein l = 1 block is pure gauge (dimension 2 = residual gauge 2;
    the one candidate non-gauge mode, A ~ r, is killed by the constraint). The metric adds no constant and no condition.
  - (ii) every cross coefficient has only r and the lapse in its denominator, so it is analytic at r_S (where the lapse is
    not zero); r_S keeps one no-log condition. The source of the boosted khronon decays (stress ~ r^-3, l = 1 response ~
    r^-1).
  - (iii) reading: metric mixing moves the spin-0 horizon out by sqrt((2 + 3 lambda)/(2 - alpha)) = 1.005-1.049 (K1's c_S);
    it stays a single regular singular point.
  - So option C stays determined (4 vs 4) and the strict count stays over-determined by one (as RB2019).

**What limits this.** Local at the UH; one round trip (F0 -> h1 -> F1); the khronon's own h-h terms (relative O(lambda)
corrections to the Einstein operator) and CFG318's O(alpha) static metric correction are left out; O(v), l = 1. No global
coupled boundary-value problem is solved. The O(v^2) stress (quadratic in d a, which could go as x^-0.76, integrable) is
not computed.

## Test (2): collapse

**2a formation (alpha -> 0, where the khronon is the maximal slicing for any lambda).** Marginally bound
Oppenheimer-Snyder collapse, interior K = 0 leaves from a regular centre (Taylor series, 40 digits), matched C^1 to the
exterior W = C/r^2 leaves. Controls K6/K6b: interior K residual 4e-25; the normal is continuous at the surface to 5e-40;
the exterior l = 1 Jacobi operator equals CFG319's dK operator (sympy).
- The leaves exist to T = 114 M. C(T) -> 3 sqrt3/4 (C - Clim = 2.3e-25 at the last leaf).
- The central lapse decays as exp(-kappa T) with **kappa = 0.5443310540, kappa_U = 2 sqrt6/9 = 0.5443310540**
  (relative difference 2e-12). This is the UH's own rate: the T = infinity leaf forms.
- **Frozen clause 2a(ii) FAILS:** C approaches the limit from ABOVE, monotonically decreasing (frozen text said
  "increases").
- **Frozen clause 2a(iii) FAILS:** the late leaves meet the star at R_s* = 1.4582 < 3/2.
  - Those points are on finite-T leaves that reach infinity, so they are outside the UH. The UH coincides with r = 3/2 only
    asymptotically, as the throat of the limiting leaf. The clause tested a fixed radius, not the UH.
  - This is why the dated correction exists. The correction is post-hoc and reported separately.

**2b weak branch selected (alpha -> 0): pass.** The O(v) l = 1 perturbation of the late leaves (the Jacobi operator on the
whole leaf, through the star, regular centre).
- At the throat, the exterior solution is decomposed into the two UH branches of the alpha = 0 operator: weak
  x^(sqrt2 - 1) and strong x^(-1 - sqrt2).
- The strong admixture falls with the throat width: |c_strong/c_weak| = 1.2e-11, 1.2e-13, 1.2e-15 at throat widths 7.8e-5,
  7.8e-6, 7.8e-7 (slope 2.00 in log-log).
- It is the same for every Robin datum tested at the star surface (-100 ... +inf). The true interior datum is F'/F = +62.4;
  the fine-tuned datum that would give the strong branch is -9.66.

**2c (alpha > 0, C versus C' inside the O(M/c_S) layer): ARGUMENT only.** A mode whose leaf displacement kappa x v F ~
x^(1+s) diverges cannot be the limit of leaves that are regular at finite T. At alpha = 0 this rule removes exactly the
branch that 2b's computation removes (1 + s = -1.41). At alpha > 0 it removes s- (1 + s = -0.62, option C') and keeps s+
(option C). A dynamical alpha > 0 evolution inside a layer of width ~1e-3 to 1e-6 M at c_S = 444 to 8e5 was not attempted.

## Test (3): the window, every gate

- The no-constant sliver (alpha_rs(c_2) from Lambda_sc = Lambda_HL_max) opens at **c_2 >= 0.0347**. It is
  [9.624e-14, 9.93e-14 / 1.08e-13 / 1.18e-13] at c_2 = 0.0383 / 0.0506 / 0.0667.
- G1-G12 were re-evaluated on a 7-point alpha grid inside each sliver: **all pass at every grid point** (G12 under
  reading W, with test (1) not failed). Controls K7 (alpha_rs = 1.1783e-13 at 0.0667) and K8 (G4 edge, G6 island, G11
  edge vs CFG467's committed sets) pass.
- With the hierarchy, all gates pass on [9.624e-14, 3.2e-9] at every chosen c_2.
- The alpha-independent rows pass: tracking floor, GW170817 (beta = 0), Cassini.
- **Condition:** the cosmological-G gate passes only on the leaf-average branch of the lambda term (L350 G5). On the plain
  branch, every c_2 >= 7.3e-3 is excluded by Planck-era cosmology (c_2 <= 2.9e-3). The chassis window of L340/CFG467 is
  already that branch.
- The sliver's lower edge rests on L340's alpha_min estimate (9.624e-14). G5's bisected threshold (2.75e-14) would widen
  it, but G8 and G12 are untested below 9.6e-14.

## MUTATE

- **M1:** alpha_c = 1e-11 at c_2 = 0.0667 without the hierarchy fails G11. alpha_c = 1e-6 with the hierarchy fails G6, G8
  and G11. The all-gate set is empty at both points.
- **M2:** the strong branch s- (option C') put through the same pipeline gives h ~ x^-0.618 (unbounded metric) and
  curvature ~ x^-1.618 (not integrable). Test (1) FAILS, as required.
- The injection s = 0.3 fails the O(v^2) integrability clause. rc = 1.

## Disclosures

- **Not blind.** All source lanes were read before freezing. The two 2a clauses that fail encoded my pre-registered
  picture (leaves approaching r = 3/2 from outside). The correction is appended and dated; the frozen outcome is kept as
  the headline.
- **Bugs fixed before the final runs (no kept output):**
  - a series-scaling problem: the background's Taylor radius equals the boundary-layer width, so the series variable is
    rescaled by CFG319's dS;
  - a least-squares solver that lost accuracy, replaced by an exact Frobenius recursion for F0 and QR with equilibration
    for h1;
  - an equation window that left the lowest metric coefficients unconstrained (spurious x^(s-3) leads);
  - coefficients above the validated window are now zeroed before the leads are read;
  - a float rounding at the star surface;
  - a slow symbolic infinity expansion, replaced by a numeric one;
  - the 1c(ii) in-code decay threshold (r^-2), corrected to the frozen "decays" (see the dated section). With the old
    threshold, (1) and, through G12, (3) read FAIL.
- Literature (RB2019, FHB2021, Beig-O Murchadha lapse rate, Kovachik-Sibiryakov, Pospelov-Shang) is recalled, PROVISIONAL,
  not fetched, and not scored. kappa = 0.5443 is computed here, not taken from the literature.

## What this implies for candidate B

B has no action, so nothing here tests B. If B is ever written on this chassis, it inherits:
- a moving-black-hole defect that, with the metric coupled at first order, is hidden and has bounded O(v) curvature;
- a UH that forms in collapse in the alpha -> 0 limit;
- a no-constant window only at c_2 >= 0.035 on the leaf-average branch.

It also inherits the open item: the alpha > 0 selection of option C in collapse.

## What this lane cannot say

- It does not solve a global coupled boundary-value problem, or do a nonlinear or dynamical alpha > 0 collapse.
- It does not reach O(v^2), rotation, or l > 1.
- It does not decide reading W; that stays the owner's call.
- It is one axis of one chassis. It is not "the theory works", and not "theory closed". kappa = 1/2 is FITTED. No
  dark-matter particle is added, and the cold fluid's mass is still required.
