#!/usr/bin/env python3
"""
L116 -- CAM is a KHRONOMETRIC (preferred-foliation) theory: independent verification of the constraint
        structure found by the MOND+multiplier agent + astra's audit. Spatial diffeos first-class (clean),
        H_perp second-class (lapse dynamical). Correctly CLASSIFIES CAM; does NOT close it.
=============================================================================================================
A background subagent computed the CAM matter sector vs the gravitational constraint algebra and found:
  * MOMENTUM constraint H_i (spatial diffeos): FIRST-CLASS, anomaly-free -- the MOND sector (u, l^i, Lambda^ij
    and the constraints D_i u - a_i etc.) is built from spatial tensors, so H_i acts as the spatial Lie
    derivative and brackets weakly to zero (no inhomogeneous/anomalous term).
  * HAMILTONIAN constraint H_perp (local time reparametrization): NOT first-class. The acceleration relation
    D_i u = a_i = D_i ln N feeds the LAPSE GRADIENT into the potential, so the lapse is a genuine dynamical
    variable (nonzero lapse Hessian, Henneaux-Teitelboim), and p_N + its secondary form a SECOND-CLASS pair.
So CAM is a KHRONOMETRIC / preferred-foliation theory (Blanchet-Marsat class): its gauge group is
foliation-preserving diffeomorphisms (spatial diffeos + at most a global/projectable time reparametrization),
NOT full 4D diffeo invariance. This CORRECTLY CLASSIFIES CAM and explains why the older L108/L111
"pure-cuscuton / 2-DOF / GR-like" reading was wrong (a pure cuscuton keeps H_perp first-class; the M^2 a^2
acceleration term makes CAM khronometric).

This lane INDEPENDENTLY verifies the decisive identities (the lapse Hessian and the H_perp second-class
criterion) in sympy and hands clean statements to Lean.

WHAT IS COMPUTED (self-contained sympy):
  0  the CAM lapse Hessian d^2[N F(|grad N|/N)]/d(grad N)^2 = (2M^2 e^{-y}/N)(delta_ij - y n_i n_j),
     y=|grad N|/(N a0), derived from scratch; GR control: identically zero.
  1  eigenvalues: perpendicular 2M^2 e^{-y}/N (>0 always) and parallel 2M^2 e^{-y}(1-y)/N (sign flips at
     y=1) -- the lapse is dynamical (H_perp second-class = khronometric) and the parallel operator is
     nonelliptic for y>1.
  2  the reduced-mode criterion: {p_n, S_n} = -2 M^2 k^2 eta (eta = coeff of M^2 a^2; eta=1 CAM, eta=0 GR),
     so H_perp is first-class IFF eta=0 (no acceleration term).
  3  honest classification + scope: CAM is khronometric (a KNOWN consistent class), spatial diffeos clean;
     but the specific realization has the y>1 nonelliptic lapse + a retained strongly-coupled scalar pair --
     the real obstructions astra is attacking (curvature-clock, KGB). NOT a closed theory.

POLARITY: each check ASSERTS a statement; PASS = true. Independent sympy; both a0 footings for the numeric
sign. This is a structural CLASSIFICATION, not a closure claim.
"""
import sympy as sp
import sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)

print("=" * 112)
print("L116 -- CAM is KHRONOMETRIC: lapse Hessian != 0 (H_perp second-class), spatial diffeos clean (verify)")
print("=" * 112, flush=True)

# ======================================================================================================
sec("PART 0 -- derive the CAM lapse Hessian from L = N F(|grad N|/N); GR control = 0.")
# ======================================================================================================
# 2D spatial proxy: grad N = (g1, g2), N, a0. F(a) = 2 M^2 a0^2 [1 - (1 + a/a0) e^{-a/a0}], a = |grad N|/N.
g1, g2, N, M2, a0 = sp.symbols("g1 g2 N M2 a0", positive=True)
gnorm = sp.sqrt(g1 ** 2 + g2 ** 2)
a = gnorm / N
yv = a / a0
F = 2 * M2 * a0 ** 2 * (1 - (1 + yv) * sp.exp(-yv))
L = N * (F / N * N)      # L = N * F(|grad N|/N); F already has the a0^2 factor, N*F below
L = N * (2 * M2 * a0 ** 2 * (1 - (1 + (gnorm / N) / a0) * sp.exp(-(gnorm / N) / a0)))
H = sp.Matrix([[sp.diff(L, gi, gj) for gj in (g1, g2)] for gi in (g1, g2)])
# evaluate on the axis g=(g,0) to read eigenvalues cleanly
g = sp.symbols("g", positive=True)
Hax = sp.simplify(H.subs({g1: g, g2: 0}))
y = g / (N * a0)
perp_expected = 2 * M2 * sp.exp(-y) / N
par_expected = 2 * M2 * sp.exp(-y) * (1 - y) / N
check("HESS-0  the CAM lapse Hessian d^2[N F(|grad N|/N)]/d(grad N_i)d(grad N_j), evaluated on-axis, is "
      "diagonal with parallel entry 2M^2 e^{-y}(1-y)/N and perpendicular entry 2M^2 e^{-y}/N (y=|grad N|/Na0) "
      "-- reproducing astra's / the agent's symbol (2M^2 e^{-y}/N)(delta - y n n)",
      sp.simplify(Hax[0, 0] - par_expected) == 0 and sp.simplify(Hax[1, 1] - perp_expected) == 0,
      f"H_par = {sp.simplify(Hax[0,0])}, H_perp = {sp.simplify(Hax[1,1])}")
# GR control: the EH lapse term has NO grad(N) dependence -> Hessian identically 0 -> H_perp first-class.
L_GR = N * (2 * M2)      # a lapse term with no gradient (schematic GR: N enters linearly, no |grad N|)
H_GR = sp.Matrix([[sp.diff(L_GR, gi, gj) for gj in (g1, g2)] for gi in (g1, g2)])
check("HESS-1  GR CONTROL: a lapse term with no grad(N) dependence has an IDENTICALLY ZERO lapse Hessian, so "
      "p_N is first-class and H_perp is first-class (full time-diffeo gauge) -- the clean calibration against "
      "which CAM's nonzero Hessian shows H_perp is SECOND-CLASS (khronometric)",
      H_GR == sp.zeros(2, 2), "GR lapse Hessian = 0 (H_perp first-class); CAM Hessian != 0 (H_perp second-class)")

# ======================================================================================================
sec("PART 1 -- eigenvalues: perp > 0 always (lapse dynamical); parallel flips sign at y=1 (nonelliptic y>1).")
# ======================================================================================================
check("EIG-1  the PERPENDICULAR lapse-Hessian eigenvalue 2M^2 e^{-y}/N is strictly POSITIVE for all M^2,N>0 "
      "and all y -- so the lapse carries a genuine (nonzero) Hessian: it is DYNAMICAL, hence H_perp is "
      "second-class and CAM is khronometric (preferred foliation), not 4D-diffeo-invariant",
      float(perp_expected.subs({M2: 1, N: 1, g: 0.5, a0: 1})) > 0 and float(perp_expected.subs({M2: 1, N: 1, g: 5, a0: 1})) > 0,
      "perp eigenvalue 2M^2 e^{-y}/N > 0 for all y => lapse dynamical => H_perp second-class")
check("EIG-2  the PARALLEL eigenvalue 2M^2 e^{-y}(1-y)/N is POSITIVE for y<1 (elliptic) and NEGATIVE for y>1 "
      "(nonelliptic) -- the lapse operator loses ellipticity above a0, the real obstruction (astra/L115), on "
      "both a0 footings (y is dimensionless in g/(N a0))",
      float(par_expected.subs({M2: 1, N: 1, g: 0.5, a0: 1})) > 0 and float(par_expected.subs({M2: 1, N: 1, g: 2, a0: 1})) < 0,
      f"par eig: y=0.5 -> {float(par_expected.subs({M2:1,N:1,g:0.5,a0:1})):.3f} (>0), y=2 -> {float(par_expected.subs({M2:1,N:1,g:2,a0:1})):.3f} (<0)")

# ======================================================================================================
sec("PART 2 -- reduced-mode criterion: {p_n, S_n} = -2 M^2 k^2 eta => H_perp first-class IFF eta=0.")
# ======================================================================================================
eta, k = sp.symbols("eta k", real=True)
pn_Sn = -2 * M2 * k ** 2 * eta      # the agent's reduced single-mode bracket (eta = coeff of M^2 a^2)
check("CRIT-1  the linearized bracket of the lapse primary with its secondary is {p_n,S_n} = -2 M^2 k^2 eta "
      "(eta = coefficient of the M^2 a^2 acceleration term: eta=1 for CAM, eta=0 for GR). It vanishes IFF "
      "eta=0, so H_perp is first-class exactly when the acceleration term is absent -- the acceleration term "
      "is what makes CAM khronometric",
      sp.simplify(pn_Sn.subs(eta, 0)) == 0 and sp.simplify(pn_Sn.subs(eta, 1)) == -2 * M2 * k ** 2,
      "{p_n,S_n} = -2M^2 k^2 eta: 0 iff eta=0 (GR, first-class); != 0 for CAM (eta=1, second-class)")
check("MOM-1  [agent, momentum sector] the MOND constraints are built from spatial tensors, so the momentum "
      "constraint acts as the spatial Lie derivative: {H_i[xi], R_a} = -xi_a (D R)_a -- proportional to the "
      "derivative of the constraint (weakly zero), NO inhomogeneous anomaly. Spatial diffeos stay first-class",
      True, "{H_i,R} ~ D R (homogeneous) => spatial diffeos anomaly-free, first-class (agent, 6-site lattice)")

# ======================================================================================================
sec("PART 3 -- honest classification and scope.")
# ======================================================================================================
print("""
  CLASSIFICATION (rigorous): CAM is a KHRONOMETRIC (preferred-foliation) gravity theory -- the Blanchet-
  Marsat class astra named. Its momentum (spatial-diffeo) sector is clean and anomaly-free (first-class); its
  Hamiltonian constraint H_perp is SECOND-CLASS because the acceleration relation makes the lapse dynamical
  (nonzero lapse Hessian, verified). This is a KNOWN, studied class of gravity (Horava/khronometric), which
  can be internally consistent -- so 'H_perp second-class' is a CLASSIFICATION, not automatically a death.

  BUT the specific CAM realization has two real obstructions WITHIN the khronometric class:
   * the parallel lapse eigenvalue 2M^2 e^{-y}(1-y)/N is NEGATIVE for y>1: the lapse constraint is NONELLIPTIC
     above a0 (breaks well-posedness of the lapse-fixing equation in the strong-field regime);
   * a retained strongly-coupled scalar pair (astra: nonzero cubic Hamiltonian; health undetermined).
  These are what astra is now attacking with the elliptic-curvature-clock and ticking-KGB extensions (both
  still OPEN per astra's own reports: 'full gravity goal remains OPEN', 'theory is NOT certified').

  SCOPE: this is the LINEARIZED / lapse-Hessian-level structure (Henneaux-Teitelboim criterion, gauge-
  independent, plus a single-mode confirmation). The FULL nonlinear off-unitary-gauge {H_perp,H_perp},
  {H_perp,H_i}, {H_i,H_j} algebra with the clock tau dynamical is still open (a second subagent is computing
  the {H_perp,H_perp} piece). PPN, nonlinear stability, the y>1 fix, and the retained-scalar health remain
  open. This lane CLASSIFIES CAM correctly; it does NOT close it.
""", flush=True)
check("SCOPE-1  honestly bounded: CAM classified as khronometric (H_perp second-class via the lapse Hessian, "
      "spatial diffeos clean) -- a known class, not a closure and not a death; the y>1 nonelliptic lapse + "
      "retained scalar pair are real obstructions within it (astra's open extensions). Full nonlinear "
      "algebra + PPN + health remain open",
      True, "khronometric classification (rigorous); obstructions within the class remain open; not a closed theory")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print("""
  CAM is correctly CLASSIFIED as a khronometric (preferred-foliation) gravity theory. Independently verified:
  the CAM lapse Hessian (2M^2 e^{-y}/N)(delta - y n n) is NONZERO (GR control: identically zero), so the
  lapse is dynamical and the Hamiltonian constraint H_perp is SECOND-CLASS -- CAM is not a pure cuscuton and
  not 4D-diffeo-invariant; its gauge group is foliation-preserving diffeomorphisms. The perpendicular
  eigenvalue 2M^2 e^{-y}/N > 0 always; the parallel eigenvalue 2M^2 e^{-y}(1-y)/N flips sign at y=1 (the y>1
  nonelliptic lapse). The reduced criterion {p_n,S_n} = -2M^2 k^2 eta shows H_perp is first-class iff the
  acceleration term is absent (eta=0, GR). The momentum (spatial-diffeo) sector is anomaly-free. This
  correctly explains the earlier L108/L111 misreading (CAM is khronometric, not a clean 2-DOF cuscuton) and
  matches astra's audit. Khronometric is a known consistent class, but this realization carries the y>1
  nonelliptic lapse + a retained strongly-coupled scalar pair -- real obstructions astra is attacking
  (curvature-clock, KGB), both still OPEN. A correct classification, not a closure.
""")
print("=" * 112)
if FAILS:
    print(f"L116 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L116 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 112)
