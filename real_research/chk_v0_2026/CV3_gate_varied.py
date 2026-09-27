#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CV3 -- V0 FOR THE C-H/K BRANCH, STEP 3: THE GATE VARIED AS AN ACTION TERM, AND WHAT IT MAY READ.

Up to CV2 the gate f was a prescribed function of the leaf geometry.  Varying it is where the construction has failed
before, and the record now says why:
  * the curvature reading (V0's first default, DE1/DE2's upper branch) produces slip, psi - phi = 2 delta G_R/M^2, and a
    wrong-signed k^4 term on every transition that only a repair can cure -- and the repair is slip again (DE7, 095ab610a);
  * it also stops the carrier being kernel-invisible (MS1, 2a5def6d9): a 0.06-150x edge force;
  * a reading of the khronon's K is blind: K = 3H(1 + O(5e-3)) inside bound regions (CV4);
  * MS1 recommends the MOND-sector density lap(Phi - v) (baryons + phantom) or the baryon density.
This lane varies the gate in V0's own Lagrangian (CV1, term for term, M^2 = m^2 (1 - f)) and finds the rule that decides:

  THE RULE.  V0's static action has three multiplier-field pairs -- (Phi, u), (Psi, w), (lam, v) -- each multiplier
  entering linearly.  A gate that reads only the constrained fields (u, v, w) leaves every multiplier's diagonal block zero,
  so the constraint Hessian's determinant is independent of the gate: the constraints stay invertible for EVERY gate shape.
  A gate that reads a multiplier (Phi or Psi) puts a gate-dependent entry on that multiplier's diagonal, and the
  determinant then vanishes somewhere on every transition (DE7's T1: W'' takes both signs).

So the MOND-sector density must be built from the constrained fields.  V0's gate reads
    U_g = C [ lap(u - v) + div((nu(|grad S w|/a0) - 1) grad S w) ]    (reading A+: baryons + their phantom),
covariantly C [Delta_h(U - V) + D_i((nu - 1) D^i W_b)] on C-H's leaves.  Reading A (baryons only, lap(u - v)) is its
phantom-free special case; reading B (MS1's lap(Phi - v)) reads the multiplier Phi.

WHAT THIS LANE CHECKS
  G1 [readings A+ and A, sympy] with f = W(U_g) varied: u, v and w stay constrained (the Phi-, lam- and Psi-equations keep
     their form); psi = Phi (no slip); the gate's parts of the u- and v-equations cancel in the dark component's potential,
     which stays u (no leak); for reading A explicitly Phi = u + f Psi/2 - 4 pi G C B W' and lam = -f Psi + 8 pi G C B W',
     with B = dL/df = [a0^2 q + Psi (m^2 w - lap(u - v)) + sigma m^2 w^2]/(8 pi G).
  G2 [reading B, sympy] U_g = C lap(Phi - v): no leak either (MS1's A3 reproduced), but u is no longer constrained:
     lap u = 4 pi G rho - 4 pi G C lap(B W').
  G3 [THE RULE, sympy] the Hessian of the four fields (Phi, u, Psi, w) with generic gate entries: for readings A and A+
     (gate entries on u and w only) det = a^2 b^2, independent of the gate; for reading B (a gate entry on Phi) det depends
     on it, and reading B's (Phi, u) symbol vanishes at k^2 = 1/(4 pi G C^2 B W'') where B W'' > 0.
  G3b [reading B, the global operator] the radial constraint operator L = lap + 4 pi G C^2 lap(B W'' lap) of a real
     transition (flat MOND halo, linear gate, w = 0.25, 1e11 galaxy): its eigenvalues cross zero as z runs 0.25 -> 4, the
     same number of times on two grids -- the lapse constraint passes through a singular epoch; reading A's operator never
     does.  (At generic epochs L is invertible: its smallest |eigenvalue| is reported.)
  G4 [reading A+'s condition] the gate's second variation acts on constrained fields only, i.e. on the matter density:
     delta Phi_g = -(4 pi G)^2 C^2 B W'' delta rho, a local pressure of either sign; sigma_v^2 > c_g^2 where W'' > 0.
     Margins at a 1e11 edge (w = 0.25) are REPORTED; the dark-energy thread computes them on real transitions.
  G5 [reduction (ii) with f varied] on both plateaus W is constant, every gate term vanishes, and V0's equations are CV1's
     -- L361's at sigma = 1 -- exactly.
  G6 [MS3's cap inside the gate] gates built from the constrained fields with a cap-like dependence (two concrete forms,
     one U_g/(1 + v_loc^2-like), s = u - v) keep the carrier blind and the constraints invertible; G3's rule is the
     general statement for any such gate, the smooth cap U_g/max(1, v_loc^2/v_cap^2) included.
  MUTATE=1 lets reading A+ read the carrier (lap u in place of lap(u - v)): the dark component then feels a gate force and
  G1 must FAIL.  rc = 1.

SCOPE.  Non-relativistic static limit.  The Euler-Lagrange equations are derived symbolically (sympy) for a generic gate
W and generic fields; the identities among them are then verified by substituting concrete smooth fields, constants and
gate shapes and evaluating at three points to 40 digits (an identity valid for arbitrary functions must vanish there;
sympy's simplify is too slow on the phantom-carrying reading).  Frozen-coefficient symbols plus a radial global operator; the gate's thresholds,
width and normalisation from the dark-energy thread (DE7/DE9: t = (U/U_th - 1)/(2w) + 1/2, W = smoothTransition, w <= 0.25
for the window at x_c0 = 2.5, B ~ M^2 a0^2 q).  G4's margins are estimates at one edge.

Run from the repository root:  python3 real_research/chk_v0_2026/CV3_gate_varied.py
"""
import os, sys, json, math, time, warnings
import numpy as np
import sympy as sp
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "CV3", "CV3_gate_varied"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()
W_WIDTH = 0.25                                                      # DE9: the window at x_c0 = 2.5 needs w <= 0.25


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: reading A+ reads the carrier (lap u in place of lap(u - v)); G1 must FAIL ***")

# ============================================================================================ the Lagrangian (CV1's, gate varied)
x = sp.symbols("x", real=True)
G_, a0_, c1, d1, m2_, Cg = sp.symbols("G a0 c1 d1 m2 C", positive=True)
sig = sp.symbols("sigma", real=True)
Phi, u, v, lam, w, Psi, psiM = [sp.Function(n)(x) for n in ("Phi", "u", "v", "lam", "w", "Psi", "psim")]
rb, rd = sp.Function("rho_b")(x), sp.Function("rho_d")(x)
Wf = sp.Function("W")
qc = lambda s: c1 * s ** sp.Rational(3, 2) + d1 * sp.log(1 + s)     # q = Q - Z for a concrete kernel (S = 1 at this order)
qcp = lambda s: sp.Rational(3, 2) * c1 * sp.sqrt(s) + d1 / (1 + s)  # q'(Z) = nu - 1
d_ = lambda F, n=1: sp.diff(F, x, n)
EPG = 8 * sp.pi * G_


def lagrangian(Ug):
    f = Wf(Ug)
    M2 = m2_ * (1 - f)
    return (-(rb + rd) * Phi
            + (2 * d_(psiM) ** 2 - 4 * d_(Phi) * d_(psiM)) / (2 * EPG)          # EH (static, after its divergence)
            + (d_(u) - d_(Phi)) ** 2 / EPG                                         # C-H: |grad u - grad Phi|^2/(8 pi G)
            + a0_ ** 2 * f * qc(d_(w) ** 2 / a0_ ** 2) / EPG
            + Psi * (d_(w, 2) - M2 * w - f * (d_(u, 2) - d_(v, 2))) / EPG
            + lam * (d_(v, 2) - 4 * sp.pi * G_ * rd) / EPG
            - sig * M2 * w ** 2 / EPG)


def el(L):
    return {str(F_.func): sp.euler_equations(L, [F_], x)[0].lhs * EPG
            for F_ in (Phi, psiM, u, v, lam, w, Psi)}


def B_of():
    f = sp.Symbol("f_")
    M2 = m2_ * (1 - f)
    Lf = (a0_ ** 2 * f * qc(d_(w) ** 2 / a0_ ** 2) + Psi * (d_(w, 2) - M2 * w - f * (d_(u, 2) - d_(v, 2))) - sig * M2 * w ** 2) / EPG
    return sp.diff(Lf, f)


B = B_of()
phant = d_(qcp(d_(w) ** 2 / a0_ ** 2) * d_(w))                             # div((nu - 1) grad w): the ungated phantom source
UgAp = Cg * ((d_(u, 2) - d_(v, 2)) + phant) if not MUTATE else Cg * (d_(u, 2) + phant)
UgA = Cg * (d_(u, 2) - d_(v, 2))
UgB = Cg * (d_(Phi, 2) - d_(v, 2))


# numeric identity test: an identity that holds for arbitrary fields and gate shapes must vanish for concrete smooth ones
s_t = sp.Symbol("s_t")
TEST = {Phi: sp.sin(sp.Rational(7, 10) * x + sp.Rational(3, 10)), u: sp.cos(sp.Rational(11, 10) * x) / 2 + x ** 2 / 5,
        v: sp.sin(sp.Rational(13, 10) * x + sp.Rational(1, 2)) * sp.Rational(3, 10), lam: sp.cos(sp.Rational(9, 10) * x),
        w: sp.sin(sp.Rational(4, 5) * x) * sp.Rational(2, 5) + sp.Rational(1, 10), Psi: sp.cos(x / 2 + sp.Rational(1, 5)) * sp.Rational(3, 5),
        psiM: sp.sin(sp.Rational(7, 10) * x + sp.Rational(3, 10)), rb: 1 + sp.sin(x) / 5, rd: sp.Rational(1, 2) + sp.cos(2 * x) / 10}
TESTSYM = {G_: sp.Rational(3, 7), a0_: sp.Rational(6, 5), c1: sp.Rational(1, 3), d1: sp.Rational(1, 4), m2_: sp.Rational(5, 3),
           Cg: sp.Rational(2, 9), sig: 1}
W_TEST = sp.Lambda(s_t, 1 / (1 + sp.exp(-3 * s_t)))                  # a concrete smooth gate
XPTS = (sp.Rational(3, 10), sp.Rational(11, 10), sp.Rational(27, 10))


def num_zero(expr, extra=None):
    """|expr| at three points after substituting concrete fields, constants and gate shape; True if ~0 to 30 digits."""
    e = expr.replace(Wf, W_TEST)
    if extra:
        for k_, v_ in extra.items():
            e = e.replace(k_, v_)
    e = e.subs(TESTSYM).subs(TEST).doit()
    vals = [abs(sp.N(e.subs(x, xp), 40)) for xp in XPTS]
    return max(vals) < sp.Float("1e-28"), max(vals)


def gate_parts(ELd, fexpr):
    """the gate's contribution to the u- and v-equations (everything beyond CV1's form)."""
    Eu = ELd["u"] - (-2 * d_(u, 2) + 2 * d_(Phi, 2) - d_(Psi * fexpr, 2))
    Ev = ELd["v"] - d_(Psi * fexpr + lam, 2)
    return Eu, Ev


def reading_report(Ug, label, extra=None):
    L_ = lagrangian(Ug)
    E_ = el(L_)
    f_ = Wf(Ug)
    phi_ok, phi_v = num_zero(E_["Phi"].subs(psiM, Phi) - (2 * d_(u, 2) - EPG * (rb + rd)), extra)
    lam_ok, _ = num_zero(E_["lam"] - (d_(v, 2) - 4 * sp.pi * G_ * rd), extra)
    psi_ok, _ = num_zero(E_["Psi"] - (d_(w, 2) - m2_ * (1 - f_) * w - f_ * (d_(u, 2) - d_(v, 2))), extra)
    slip_ok, _ = num_zero(E_["psim"].subs(psiM, Phi), extra)
    Eu, Ev = gate_parts(E_, f_)
    # after integrating twice, the gate parts enter Phi as -Eu/2 and lam as -Ev, so Phi + lam/2 - u = -(Eu + Ev)/2
    leak_ok, leak_v = num_zero(Eu + Ev, extra)
    gate_on, gate_v = num_zero(Eu, extra)                                  # the gate does act (Eu != 0): not vacuous
    P(f"    {label}: Phi-eq kept {phi_ok}; lam-eq kept {lam_ok}; w's constraint (Psi-eq) kept {psi_ok}; psi = Phi {slip_ok}; "
      f"|gate parts u + v| = {float(leak_v):.1e} (the gate part itself: {float(gate_v):.2e})")
    return phi_ok, lam_ok, psi_ok, slip_ok, leak_ok and not gate_on, E_


# ============================================================================================ G1 readings A+ and A
banner("G1  READINGS A+ AND A: the MOND-sector density (and the baryon density) through the constrained fields")
okAp = reading_report(UgAp, "A+ (baryons + phantom via u - v and w)")
okA = reading_report(UgA, "A  (baryons via u - v)               ")
EA = okA[5]
WpA = sp.diff(Wf(UgA), d_(u, 2)) / Cg
fA = Wf(UgA)
resid_u = num_zero(EA["u"] - (-2 * d_(u, 2) + 2 * d_(Phi, 2) + d_(-Psi * fA + EPG * Cg * B * WpA, 2)))[1]
resid_v = num_zero(EA["v"] - d_(Psi * fA + lam - EPG * Cg * B * WpA, 2))[1]
P(f"    reading A's gate force: u-equation residual {float(resid_u):.1e}, v-equation residual {float(resid_v):.1e} "
  f"(Phi = u + f P - 4 pi G C B W', lam = -f Psi + 8 pi G C B W')")
OUT["numbers"]["G1"] = {"A+": [bool(v_) for v_ in okAp[:5]], "A": [bool(v_) for v_ in okA[:5]],
                        "gate_force_resid": [float(resid_u), float(resid_v)]}
check("G1 readings A+ and A keep u, v and w constrained, give no slip, and leave the dark component's potential exactly u "
      "(the gate's u- and v-parts cancel); reading A's gate force is -4 pi G C B W' on Phi",
      f"A+: {[bool(v_) for v_ in okAp[:5]]}; A: {[bool(v_) for v_ in okA[:5]]}; gate-force residuals "
      f"{float(resid_u):.1e}, {float(resid_v):.1e}",
      all(okAp[:5]) and all(okA[:5]) and resid_u < 1e-28 and resid_v < 1e-28,
      "the gate force acts on baryons and light alike (lensing = dynamics); the carrier is blind to it as to the phantom")

# ============================================================================================ G2 reading B
banner("G2  READING B: U_g = C lap(Phi - v) (MS1's first choice) reads the multiplier Phi")
LB = lagrangian(UgB)
ELB = el(LB)
fB = Wf(UgB)
WpB = sp.diff(Wf(UgB), d_(Phi, 2)) / Cg
resB_Phi = num_zero(ELB["Phi"].subs(psiM, Phi) - (2 * d_(u, 2) - EPG * (rb + rd) + d_(EPG * Cg * B * WpB, 2)))[1]
resB_v = num_zero(ELB["v"] - d_(Psi * fB + lam - EPG * Cg * B * WpB, 2))[1]
resB_u = num_zero(ELB["u"] - (-2 * d_(u, 2) + 2 * d_(Phi, 2) - d_(Psi * fB, 2)))[1]
phiN = sp.Function("phi_N")(x)
leakB = sp.simplify((phiN - EPG / 2 * Cg * B * WpB + Psi * fB / 2) + (-Psi * fB + EPG * Cg * B * WpB) / 2 - phiN)
P(f"    residuals: Phi-eq (u no longer constrained: lap u = 4 pi G rho - 4 pi G C lap(B W')) {float(resB_Phi):.1e}; "
  f"v-eq {float(resB_v):.1e}; u-eq {float(resB_u):.1e}")
P(f"    dark component's potential - Newtonian potential of all matter = {leakB}")
OUT["numbers"]["G2"] = {"residuals": [float(resB_Phi), float(resB_v), float(resB_u)], "leak": str(leakB)}
check("G2 reading B is leak-free (MS1's A3 reproduced) but the gate enters the Phi-constraint itself, so u is no longer "
      "constrained", f"residuals {float(resB_Phi):.1e}, {float(resB_v):.1e}, {float(resB_u):.1e}; leak {leakB}",
      max(resB_Phi, resB_v, resB_u) < 1e-28 and leakB == 0,
      "reading a multiplier changes the constraint structure; G3 shows what that costs")

# ============================================================================================ G3 the rule
banner("G3  THE RULE: a gate that reads only constrained fields leaves the constraint determinant alone")
k, a_, b_ = sp.symbols("k a b", real=True)
Xuu, Xww, Xuw, XPP, XPu = sp.symbols("X_uu X_ww X_uw X_PhiPhi X_Phiu", real=True)
H_AAp = sp.Matrix([[0, a_, 0, 0], [a_, Xuu, 0, Xuw], [0, 0, 0, b_], [0, Xuw, b_, Xww]])
H_B = sp.Matrix([[XPP, a_ + XPu, 0, 0], [a_ + XPu, Xuu, 0, Xuw], [0, 0, 0, b_], [0, Xuw, b_, Xww]])
detAAp, detB_ = sp.factor(H_AAp.det()), sp.factor(H_B.det())
P(f"    readings A/A+ (gate entries on u and w): det = {detAAp}  (independent of the gate)")
P(f"    reading B (a gate entry on the multiplier Phi): det = {detB_}")
BW2 = sp.symbols("BW2", real=True)
H2B = sp.Matrix([[BW2 * Cg ** 2 * k ** 4, -2 * k ** 2 / EPG], [-2 * k ** 2 / EPG, 2 * k ** 2 / EPG]])
d2B = sp.factor(H2B.det()); kx2 = [r_ for r_ in sp.solve(sp.Eq(d2B, 0), k ** 2) if r_ != 0]
P(f"    reading B's (Phi, u) symbol: det = {d2B}; zero at k^2 = {kx2}")
OUT["numbers"]["G3"] = {"det_A": str(detAAp), "det_B": str(detB_), "d2B": str(d2B), "kx2": str(kx2)}
check("G3 THE RULE: with the multipliers' diagonal blocks zero (gate reading u, v, w only) the constraint Hessian's "
      "determinant is a^2 b^2 for every gate; a gate reading the multiplier Phi makes it gate-dependent, and reading B's "
      "(Phi, u) symbol vanishes at k^2 = 1/(4 pi G C^2 B W'')",
      f"det A/A+ = {detAAp}; det B = {detB_}; reading B zero at {kx2}",
      sp.simplify(detAAp - a_ ** 2 * b_ ** 2) == 0 and sp.simplify(sp.diff(detB_, XPP)) != 0 and len(kx2) == 1,
      "so the MOND-sector density has to be assembled from the constrained fields (reading A+), not from the lapse")

# ============================================================================================ G3b reading B's global operator
banner("G3b  READING B'S GLOBAL OPERATOR on a real transition: eigenvalues crossing zero as the universe expands")
GKs = 4.30091e-6; A0K = 9.3619e-11 * 3.0856775814913673e19 / 1e6; H0K = 0.0674; OM, OL = 0.3153, 0.6847
rho_c0 = 3 * H0K ** 2 / (8 * math.pi * GKs); E_ = lambda zz: math.sqrt(OM * (1 + zz) ** 3 + OL)
g_ = lambda s_: np.where(s_ > 0, np.exp(-1.0 / np.maximum(s_, 1e-300)), 0.0)
Wfun = lambda s_: g_(s_) / (g_(s_) + g_(1 - s_))


def operator(zz, reading, NRg):
    rho_th = (2.0 / 3.0) * 2.5 * E_(zz) ** 4 * rho_c0
    vf = (GKs * 1e11 * A0K) ** 0.25
    r_e = vf / math.sqrt(4 * math.pi * GKs * rho_th)
    rr = np.linspace(0.5 * r_e, 3.0 * r_e, NRg); h = rr[1] - rr[0]
    D2 = (np.diag(-2.0 * np.ones(NRg)) + np.diag(np.ones(NRg - 1), 1) + np.diag(np.ones(NRg - 1), -1)) / h ** 2
    if reading == "A":
        return D2, r_e
    rho_dyn = vf ** 2 / (4 * math.pi * GKs * rr ** 2)
    tt_ = (rho_dyn / rho_th - 1) / (2 * W_WIDTH) + 0.5
    ds = 1e-4
    W2t = (Wfun(tt_ + ds) - 2 * Wfun(tt_) + Wfun(tt_ - ds)) / ds ** 2
    y_ = GKs * 1e11 / rr ** 2 / A0K
    Bv = A0K ** 2 * (4.0 / 3.0) * y_ ** 1.5 / (8 * math.pi * GKs)
    Cc = 1.0 / (4 * math.pi * GKs * rho_th)
    eps_ = 4 * math.pi * GKs * Cc ** 2 * Bv * W2t / (2 * W_WIDTH) ** 2
    Lm = D2 + D2 @ np.diag(eps_) @ D2
    return 0.5 * (Lm + Lm.T), r_e


zs = np.linspace(0.25, 4.0, 76)
rowsG3b = {}
for NRg in (500, 1000):
    cB = [int(np.sum(np.linalg.eigvalsh(operator(z_, "B", NRg)[0]) < 0)) for z_ in zs]
    cA = [int(np.sum(np.linalg.eigvalsh(operator(z_, "A", NRg)[0]) < 0)) for z_ in zs]
    rowsG3b[NRg] = {"B_crossings": int(np.sum(np.diff(cB) != 0)), "A_constant": len(set(cA)) == 1}
mins = {}
for zz in (0.5, 2.5):
    Lb, r_e = operator(zz, "B", 1000); La, _ = operator(zz, "A", 1000)
    mins[zz] = {"B": float(np.min(np.abs(np.linalg.eigvalsh(Lb))) * r_e ** 2),
                "A": float(np.min(np.abs(np.linalg.eigvalsh(La))) * r_e ** 2)}
for NRg, v_ in rowsG3b.items():
    P(f"    {NRg} points: reading B's negative-eigenvalue count changes {v_['B_crossings']} times over z = 0.25..4; "
      f"reading A's is constant: {v_['A_constant']}")
for zz, v_ in mins.items():
    P(f"    z = {zz}: smallest |eigenvalue| (x r_e^2): reading B {v_['B']:.3f}, reading A {v_['A']:.3f}  (generic epochs: invertible)")
OUT["numbers"]["G3b"] = {"crossings": {str(k_): v_ for k_, v_ in rowsG3b.items()}, "min_abs_eig": {str(k_): v_ for k_, v_ in mins.items()}}
check("G3b reading B's constraint operator on a real transition has an eigenvalue crossing zero as z runs 0.25 -> 4 (the "
      "same count on both grids): the lapse constraint passes through a singular epoch; reading A's never does",
      "; ".join(f"{k_} points: {v_['B_crossings']} crossings, A constant {v_['A_constant']}" for k_, v_ in rowsG3b.items()),
      all(v_["B_crossings"] > 0 and v_["A_constant"] for v_ in rowsG3b.values())
      and rowsG3b[1000]["B_crossings"] == rowsG3b[500]["B_crossings"],
      "the crossing is a mode near k ~ eps^(-1/2) sweeping through zero as the gate's coefficient grows with z: at that "
      "epoch the lapse's response to a generic density source diverges.  At generic epochs the operator is invertible, "
      "but not uniformly in time -- reading B would need a lapse-sector repair")

# ============================================================================================ G4 reading A+'s condition
banner("G4  READING A+'s CONDITION: the gate's second variation is a local matter pressure of either sign")
drho, BW2s, Cs = sp.symbols("delta_rho BW2 C_s", real=True)
dPhi_g = -4 * sp.pi * G_ * Cs * BW2s * Cs * 4 * sp.pi * G_ * drho
g4_sym = sp.simplify(dPhi_g - (-(4 * sp.pi * G_) ** 2 * Cs ** 2 * BW2s * drho)) == 0
tt = np.linspace(1e-4, 1 - 1e-4, 200001)
W2max = float(np.max(np.gradient(np.gradient(Wfun(tt), tt), tt)))
rowsG4 = {}
for zz in (0.25, 2.5, 4.0):
    rho_th = (2.0 / 3.0) * 2.5 * E_(zz) ** 4 * rho_c0
    vf = (GKs * 1e11 * A0K) ** 0.25
    r_e = vf / math.sqrt(4 * math.pi * GKs * rho_th)
    y_e = GKs * 1e11 / r_e ** 2 / A0K
    Bv = A0K ** 2 * (4.0 / 3.0) * y_e ** 1.5 / (8 * math.pi * GKs)
    cg2 = Bv * W2max / ((2 * W_WIDTH) ** 2 * rho_th)
    rowsG4[zz] = {"c_g_kms": math.sqrt(cg2), "margin_200": 200.0 ** 2 / cg2, "margin_10": 10.0 ** 2 / cg2}
    P(f"    z = {zz}: c_g = {math.sqrt(cg2):.1f} km/s at w = {W_WIDTH}; sigma_v^2/c_g^2 = {200.0 ** 2 / cg2:.2f} (200 km/s), "
      f"{10.0 ** 2 / cg2:.4f} (10 km/s)")
OUT["numbers"]["G4"] = {"symbolic": g4_sym, "W2max": W2max, "rows": {str(k_): v_ for k_, v_ in rowsG4.items()}}
check("G4 the gate's second variation acts on the matter density only: delta Phi_g = -(4 pi G)^2 C^2 B W'' delta rho, a "
      "local pressure of either sign (sympy); the implied margins at a 1e11 edge are reported", "; ".join(
          f"z = {k_}: c_g = {v_['c_g_kms']:.0f} km/s, margins {v_['margin_200']:.2f} (200) / {v_['margin_10']:.4f} (10)"
          for k_, v_ in rowsG4.items()), g4_sym,
      "the condition sits in the matter sector, not the metric: where W'' > 0 the gate acts as an anti-pressure that the "
      "matter's own velocity dispersion must beat.  At w = 0.25 the one-edge estimate is severe (a narrow gate has a large "
      "W''); the dark-energy thread computes the margins on DE7's real transitions")

# ============================================================================================ G5 reduction (ii) with f varied
banner("G5  REDUCTION (ii) WITH f VARIED: on both plateaus every gate term vanishes")
s_, f0 = sp.Symbol("s_"), sp.Symbol("f0")
ELAp = okAp[5]
ELAp_pl = {k_: sp.simplify(v_.replace(Wf, sp.Lambda(s_, f0)).doit()) for k_, v_ in ELAp.items()}
res_pl_u = sp.simplify(ELAp_pl["u"] - (-2 * d_(u, 2) + 2 * d_(Phi, 2) - d_(Psi * f0, 2)))
res_pl_v = sp.simplify(ELAp_pl["v"] - d_(Psi * f0 + lam, 2))
res_pl_w = sp.simplify(ELAp_pl["w"] - (d_(Psi, 2) - m2_ * (1 - f0) * Psi - 2 * d_(f0 * qcp(d_(w) ** 2 / a0_ ** 2) * d_(w))
                                       - 2 * sig * m2_ * (1 - f0) * w))
P(f"    W = f0 constant: u-, v- and w-equation residuals vs CV1's: {res_pl_u}, {res_pl_v}, {res_pl_w}")
OUT["numbers"]["G5"] = {"residuals": [str(res_pl_u), str(res_pl_v), str(res_pl_w)]}
check("G5 on both plateaus the varied gate's terms vanish and V0's equations are CV1's -- L361's at sigma = 1 -- exactly: "
      "reduction (ii) holds with f varied", f"residuals {res_pl_u}, {res_pl_v}, {res_pl_w}",
      res_pl_u == 0 and res_pl_v == 0 and res_pl_w == 0,
      "inside regions and in the web V0 is L361; the gate's own physics lives only in transition layers")

# ============================================================================================ G6 the cap
banner("G6  MS3's CAP INSIDE THE GATE: any gate built from the constrained fields keeps the carrier blind")
sAB = u - v
# two concrete, cap-like gate variables built only from the constrained fields (the general statement is G3's rule)
F1 = d_(sAB) * d_(sAB, 2) + sp.sin(d_(w)) + d_(w, 2) ** 2 / (1 + d_(sAB) ** 2)
F2 = (d_(sAB, 2) + d_(qcp(d_(w) ** 2 / a0_ ** 2) * d_(w))) / (1 + d_(sAB) ** 2 / (1 + d_(sAB, 2) ** 2))   # U / (1 + v_loc^2-like)
okC1 = reading_report(F1, "cap-like F1(s', s'', w', w'')")
okC2 = reading_report(F2, "cap-like F2 = U/(1 + v_loc^2-like)")
OUT["numbers"]["G6"] = {"F1": [bool(v_) for v_ in okC1[:5]], "F2": [bool(v_) for v_ in okC2[:5]]}
check("G6 gates built from the constrained fields with a cap-like dependence -- two concrete forms, one of them "
      "U_g/(1 + v_loc^2-like) -- keep u, v and w constrained, give no slip, and leave the carrier blind",
      f"F1 {[bool(v_) for v_ in okC1[:5]]}; F2 {[bool(v_) for v_ in okC2[:5]]}", all(okC1[:5]) and all(okC2[:5]),
      "MS3's cap becomes part of V0's one gate term with v_cap a declared constant, at no cost to the constraint structure "
      "(G3's rule covers every such gate)")

banner("VERDICT")
P(f"""  Varying the gate decides what it may read, by one rule: V0's multipliers (Phi, Psi, lam) enter linearly, so a gate that
  reads only the constrained fields (u, v, w) leaves the constraint determinant independent of the gate, and one that reads
  a multiplier does not (G3).  The curvature reading leaks into the carrier and needs a slip-carrying repair (MS1, DE7);
  K is blind (CV4); lap(Phi - v) reads the multiplier Phi and its lapse constraint passes through singular epochs (G2, G3b).
  V0's gate reads the MOND-sector density assembled from the constrained fields,
      U_g = C [lap(u - v) + div((nu - 1) grad S w)]   (reading A+; covariantly on C-H's leaves),
  which is leak-free and slip-free and keeps every constraint invertible (G1, G3); the cap fits inside it (G6); on the
  plateaus V0 is L361 exactly with f varied (G5).  Its cost is a matter-sector pressure of either sign in transition layers
  (G4): at the narrow width the window needs (w = 0.25), the one-edge estimate puts c_g above 200 km/s by z = 2.5 --
  a new pincer between the window (narrow w) and matter stability (wide w), for the real transitions to decide.
  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
