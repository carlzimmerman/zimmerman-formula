#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gen2_constraint_reduced_quadratic_2026.py
=========================================
THE EXACT CONSTRAINT-REDUCED QUADRATIC ACTION FOR THE FROZEN GEN-2 ACTION.

Carl's ruling: "The right next calculation is the exact constraint-reduced quadratic
action for Gen-2.  That determines whether the promising k^2, rather than k^4, tensor
behavior survives the full ADM constraints and whether the scalar sector is actually
healthy."

The previous calculation (ya_tensor_exact_2026.py) SET delta N = delta N^i = 0 BY HAND.
Nothing is set by hand here: all ten metric perturbations are carried, the three spatial
diffeomorphisms are gauge-fixed exactly (H_ij = 0 for i along k), and the four
non-dynamical fields (delta N, delta N^i) are eliminated by an EXACT Schur complement --
which IS "solving the lapse and shift constraints at quadratic order".

TWO ANSWERS, POINTING OPPOSITE WAYS:
  TENSOR  the k^2 behaviour SURVIVES exactly.  c_T^2/c^2 = 1 + 2 eps A(X0) X0,
          k-independent; the constraints change it only at O((eps A X0)^2) ~ 1e-50,
          as a + / x birefringence for k perpendicular to a^(0).
  SCALAR  NOT healthy.  For ANY eps != 0, of either sign, the khronon's short-wavelength
          speed is c_s^2(k->oo) = (1 - lam_K)/(3 lam_K - 1), NEGATIVE for every lam_K > 1
          -- and lam_K > 1 is exactly what no-ghost requires.

Labels: DERIVED = computed here and sympy-verified.  IMPORTED = cited external input.
ASSUMED = an input of the frozen programme, not derived here.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
import numpy as np
import gen2_adm_core_2026 as C

k, w, lam, eta, X0, ell, epsY = C.k, C.w, C.lam, C.eta, C.X0, C.ell, C.epsY
FX, FXX, FY, F0 = C.FX, C.FXX, C.FY, C.F0
W, cc, uu = sp.Symbol('W'), sp.Symbol('c2'), sp.Symbol('u')
FAIL = []
LBL = ['phi', 'B1', 'B2', 'B3', 'h_+', 'h_x', 'tr']
CON = [0, 1, 2, 3]                                    # phi, B1, B2, B3 : non-dynamical


def head(s):
    print("\n" + "=" * 100 + "\n" + s + "\n" + "=" * 100)


def ck(name, cond, note=""):
    print(("  [ok]   " if cond else "  [FAIL] ") + name + (("\n         " + note) if note else ""))
    if not cond:
        FAIL.append(name)
    return cond


def sector(kvec, gauge, pair, cross):
    L2, A, Ab, used, L1 = C.build_L2(kvec, gauge_zero=gauge)
    M, res = C.hermitian_matrix(L2, A, Ab)
    assert sp.simplify(res) == 0
    idx = {n: i for i, n in enumerate(used)}
    n = len(used)
    P = sp.zeros(n, n)
    for j, nm in enumerate(['phi', 'B1', 'B2', 'B3']):
        P[idx[nm], j] = 1
    P[idx[pair[0]], 4] = 1
    P[idx[pair[1]], 4] = -1                            # h_+   (traceless)
    P[idx[cross], 5] = 1                               # h_x
    P[idx[pair[0]], 6] = 1
    P[idx[pair[1]], 6] = 1                             # trace (the khronon)
    return sp.expand(P.T * M * P), used, L1


def uv_polynomial(Mb, rows):
    """Schur out (phi,B_i); then the UV (leading-k) dispersion polynomial in c^2 = W/k^2."""
    inv = Mb[CON, CON].inv()
    Pr = Mb[rows, rows] - Mb[rows, CON] * inv * Mb[CON, rows]
    m = len(rows)
    Pr = sp.Matrix(m, m, lambda a, b: sp.cancel(sp.together(sp.expand(Pr[a, b]).subs(w**2, W))))
    det = (Pr[0, 0] * Pr[1, 1] - Pr[0, 1] * Pr[1, 0]) if m == 2 else Pr[0, 0]
    D = sp.numer(sp.cancel(sp.together(det)))
    D = sp.expand(D.subs(W, cc * k**2))
    top = sp.Poly(D, k).coeffs()[0]
    return sp.Poly(sp.expand(top), cc), Pr


CFG = {
    'par': dict(lab="k PARALLEL to a^(0)   (both along z)", kvec=(0, 0, k),
                gauge=[(2, 2), (0, 2), (1, 2)], pair=('H11', 'H22'), cross='H12'),
    'perp': dict(lab="k PERPENDICULAR to a^(0)   (k along x, a^(0) along z)", kvec=(k, 0, 0),
                 gauge=[(0, 0), (0, 1), (0, 2)], pair=('H22', 'H33'), cross='H23'),
}

head("0.  BUILD -- exact O(eps^2) Lagrangian, all 10 metric perturbations, 3 diffeos fixed")
print("""  Background: h_ij = delta_ij, N = exp(abar z), N_i = 0.  Chosen so that
  T^(0)_ij = D_<i a_j> = 0 EXACTLY (a^(0)_i uniform); hence Y^(0) = 0 and the entire
  quadratic Y-content is (delta T)^2 -- no cross terms.  X0 = (ell abar)^2 = x^2,
  x = g/a0, ell = c^2/a0, kept exact.  Background gradients kept (dNb/dz = abar Nb);
  Nb -> 1 imposed only at the end (local WKB frame).""")
D = {}
for key, cfg in CFG.items():
    Mb, used, L1 = sector(cfg['kvec'], cfg['gauge'], cfg['pair'], cfg['cross'])
    D[key] = dict(Mb=Mb, used=used, L1=L1)
    print("     %-5s fields carried: %s   ->  basis %s" % (key, used, LBL))
ck("quadratic form reproduces the Lagrangian exactly (zero residue), both configurations",
   True, "asserted inside sector()")

head("T0.  THE TADPOLE DOES NOT ENTER THE DISPERSION  [DERIVED]")
print("""  The background is not an exact solution (a true static solution carries
  h_ij = (1-2Psi) delta_ij with curvature ~ abar^2), so a linear term survives:
      S = S_0 + J.f + (1/2) f.M.f    =>    linear field equation   J + M f = 0.
  J is an INHOMOGENEOUS term; det M = 0 -- the dispersion relation -- cannot see it.
  What IS neglected is the shift of M by the true background: relative O(abar^2/k^2),
  with NO factor of ell.  Every ell-ENHANCED term (everything carrying X0 = ell^2 abar^2,
  which is O(1) in a galaxy) is kept EXACTLY.  At LIGO k, abar/k ~ 1e-21, so the
  neglected piece is ~1e-42 relative -- 17 orders below the effect being computed.""")
ck("linear (tadpole) term is nonzero, as expected, and is not part of M",
   sp.simplify(D['par']['L1']) != 0)

head("1.  TRANSVERSALITY THEOREM: the Y operator cannot mix TT with the lapse  [DERIVED]")
print("""  delta T_ij = TF[ d_i d_j phi - dGamma^k_ij abar_k ].  For a plane wave the lapse
  piece is TF[-k_i k_j] phi -- purely LONGITUDINAL.  A TT polarisation obeys
  k^i gamma_ij = 0 and gamma^i_i = 0, so TF[k_i k_j] : TF[dGamma.abar] = 0 for ANY
  orientation of abar relative to k.  Verified below for generic k and generic abar.""")
kx, ky, kz = sp.symbols('k_x k_y k_z', real=True)
ax, ay, az = sp.symbols('a_x a_y a_z', real=True)
kv, av = [kx, ky, kz], [ax, ay, az]
kM = sp.Matrix(kv)
e1 = kM.cross(sp.Matrix([1, 0, 0]))
e2 = kM.cross(e1)
e1 = e1 / sp.sqrt(sum(e1[i]**2 for i in range(3)))
e2 = e2 / sp.sqrt(sum(e2[i]**2 for i in range(3)))
c1, c2s = sp.symbols('c_1 c_2', real=True)
gTT = sp.expand(c1 * (e1 * e1.T - e2 * e2.T) + c2s * (e1 * e2.T + e2 * e1.T))
ck("the TT basis used is genuinely transverse and traceless",
   all(sp.simplify(sum(kv[i] * gTT[i, j] for i in range(3))) == 0 for j in range(3))
   and sp.simplify(sp.trace(gTT)) == 0)
k2 = kx**2 + ky**2 + kz**2
dG = lambda m, i, j: sp.Rational(1, 2) * (sp.I * kv[i] * gTT[j, m] + sp.I * kv[j] * gTT[i, m]
                                          - sp.I * kv[m] * gTT[i, j])
dTg = sp.Matrix(3, 3, lambda i, j: -sum(dG(m, i, j) * av[m] for m in range(3)))
dTp = sp.Matrix(3, 3, lambda i, j: -(kv[i] * kv[j] - sp.Rational(1, 3) * (1 if i == j else 0) * k2))
cross0 = sp.simplify(sp.expand(sum(dTp[i, j] * dTg[i, j] for i in range(3) for j in range(3))))
ck("TF[d_i d_j phi] : TF[dGamma.abar] = 0 identically -- generic k, generic abar", cross0 == 0,
   "this, not any smallness, is why the lapse constraint cannot feed back into c_T")

head("2.  WHAT EACH TENSOR POLARISATION ACTUALLY MIXES WITH  [DERIVED]")
mixes = {}
for key in ('par', 'perp'):
    Mb = D[key]['Mb']
    print("\n  --- %s ---" % CFG[key]['lab'])
    for i, pol in ((4, 'h_+'), (5, 'h_x')):
        nz = [(LBL[j], sp.cancel(sp.expand(Mb[i, j]))) for j in range(7)
              if j != i and sp.cancel(sp.expand(Mb[i, j])) != 0]
        mixes[(key, pol)] = dict(nz)
        print("      %s mixes with: %s" % (pol, [a for a, _ in nz] or "NOTHING"))
        for a, v in nz:
            print("          <%s|M|%s> = %s" % (pol, a, sp.factor(v)))
ck("[par] BOTH tensor polarisations decouple EXACTLY from (delta N, delta N^i, trace)",
   mixes[('par', 'h_+')] == {} and mixes[('par', 'h_x')] == {},
   "k || a^(0) leaves an unbroken SO(2) about the common axis: helicity 2 cannot mix "
   "with helicity 0 or 1.  Constraint elimination provably cannot touch c_T here.")
ck("[perp] h_x (odd under y -> -y) decouples EXACTLY", mixes[('perp', 'h_x')] == {})
mp = mixes[('perp', 'h_+')]
ck("[perp] h_+ mixes ONLY with phi and the trace",
   set(mp) == {'phi', 'tr'})
ck("[perp] the h_+ / lapse mixing carries NO k at all -- it is a pure abar^2 mass mixing, "
   "with ZERO contribution from the Y-sector",
   sp.diff(mp['phi'], k) == 0 and sp.diff(mp['phi'], FY) == 0,
   "<h_+|M|phi> = %s = abar^2 (eta_K - 2 F_X).  Exactly the transversality theorem."
   % sp.factor(mp['phi']))
ck("[perp] the only k-dependent Y-mixing of h_+ is with the TRACE, at order eps A X0 k^2",
   sp.simplify(sp.expand(mp['tr']).coeff(FY) - 2 * X0 * k**2) == 0)

head("3.  THE CONSTRAINT-REDUCED TENSOR ACTION  S_T = K_T omega^2 - G_T k^2  [DERIVED]")
FRZ = C.frozen_subs(with_Y=True)
Aof = X0**2 / (1 + X0)**4
for key in ('par', 'perp'):
    Mb = D[key]['Mb']
    print("\n  --- %s ---" % CFG[key]['lab'])
    for i, pol in ((4, 'h_+'), (5, 'h_x')):
        if mixes[(key, pol)]:
            continue
        Pii = sp.cancel(sp.expand(Mb[i, i]).subs(w**2, W))
        KT = sp.cancel(sp.diff(Pii, W))
        GT = sp.cancel(-sp.diff(sp.cancel(Pii - KT * W), k, 2) / 2)
        mass = sp.cancel(Pii - KT * W + GT * k**2)
        print("      %s :  K_T = %s ,  G_T = %s" % (pol, KT, sp.factor(GT)))
        print("             residual 0-derivative part = %s" % sp.factor(mass))
        print("               (= O(abar^2) and O(a0^2/c^4): relative (abar/k)^2 ~ 1e-42)")
        print("             c_T^2 = G_T/K_T = %s" % sp.factor(sp.cancel(GT / KT).subs(FRZ)))
        ck("[%s/%s] c_T^2 = 1 + 2 eps A(X0) X0 EXACTLY and k-INDEPENDENT" % (key, pol),
           sp.simplify(sp.cancel(GT / KT).subs(FRZ) - (1 + 2 * epsY * Aof * X0)) == 0)
        ck("[%s/%s] K_T = 1 > 0: the tensor is never a ghost; lam_K and eta_K drop out"
           % (key, pol), sp.simplify(KT - 1) == 0)
        ck("[%s/%s] NO k^4 dispersion survives: G_T is k-independent" % (key, pol),
           sp.simplify(sp.diff(GT, k)) == 0)

head("4.  h_+ AT k PERPENDICULAR TO a^(0): the ONE thing the constraints DO change [DERIVED]")
q, _ = uv_polynomial(D['perp']['Mb'], [4, 6])
print("  Exact UV dispersion polynomial for the coupled (h_+, trace) pair, after the")
print("  lapse and shift constraints are solved:")
print("      %s = 0" % sp.factor(sp.expand(q.as_expr())))
m2 = 2 * lam - 1
cT_exact = (2 * uu * m2 + lam + sp.sqrt(m2**2 * (1 + 4 * uu**2) + 4 * uu * lam * m2)) / (3 * lam - 1)
cS_exact = (2 * uu * m2 + lam - sp.sqrt(m2**2 * (1 + 4 * uu**2) + 4 * uu * lam * m2)) / (3 * lam - 1)
qu = sp.Poly(sp.expand(q.as_expr().subs(FY, uu / X0) / (8 * (uu / X0) * ell**8)), cc)
a2c, a1c, a0c = [sp.expand(t) for t in qu.all_coeffs()]
ck("the reduced (h_+, trace) UV dispersion is exactly "
   "(3L-1)c^4rt - 2[L + 2u(2L-1)]c^2 - (L-1) = 0,  u := eps A(X0) X0,  L := lam_K",
   sp.expand(a2c - (3 * lam - 1)) == 0
   and sp.expand(a1c + 2 * (lam + 2 * uu * m2)) == 0
   and sp.expand(a0c + (lam - 1)) == 0)
ck("Vieta: sum of the two roots = 2[L + 2u(2L-1)]/(3L-1), matching the closed forms",
   sp.expand(sp.together(cT_exact + cS_exact) - 2 * (lam + 2 * uu * m2) / (3 * lam - 1)) == 0)
ck("Vieta: product of the two roots = (1-L)/(3L-1), matching the closed forms",
   sp.simplify(sp.expand(sp.together(cT_exact * cS_exact)) - (1 - lam) / (3 * lam - 1)) == 0)
_bir = True
for _lv in (1.05, 1.5, 3.0, 10.0):
    for _uv in (1e-2, 1e-3, 1e-4):
        _ex = float(cT_exact.subs({lam: _lv, uu: _uv}))
        _pr = 1 + 2 * _uv + 2 * _uv**2 * (_lv - 1) / (2 * _lv - 1)
        if abs(_ex - _pr) > 50 * _uv**3 + 1e-14:
            _bir = False
ck("c_T^2(h_+, k perp a) = 1 + 2u + 2u^2 (lam_K-1)/(2 lam_K-1) + O(u^3)   "
   "[verified to O(u^3) at 12 (lam_K,u) points]", _bir,
   "=> solving the constraints induces a + / x BIREFRINGENCE of size "
   "2u^2 (lam_K-1)/(2 lam_K-1) for k perpendicular to a^(0), and changes NOTHING else "
   "in the tensor sector.  At u ~ 1e-25 that is ~1e-50.")
ck("the SCALAR root of the same pair reduces at u = 0 to (1-lam_K)/(3 lam_K-1)",
   all(abs(float(cS_exact.subs({lam: _lv, uu: 0})) - (1 - _lv) / (3 * _lv - 1)) < 1e-13
       for _lv in (1.05, 1.5, 3.0, 10.0)),
   "the UV limit; section 6 shows why it is negative and what it means")

head("5.  THE NUMBER  [DERIVED + IMPORTED bound]")
c_l, a0 = 2.99792458e8, 9.3619e-11
ellv = c_l**2 / a0
eps_need = 1.1e-24
print("  ell = c^2/a0 = %.4e m" % ellv)
print("  eps required by the Solar-System suppression window = %.2e   [ASSUMED, imported "
      "from the Gen-1 programme]" % eps_need)
Xs = np.logspace(-4, 8, 60001)
f = 2 * Xs**2 / (1 + Xs)**4 * Xs
print("  max over X0 of  2 A(X0) X0  = %.6f   at X0 = %.4f  (x = g/a0 = %.4f)"
      % (f.max(), Xs[f.argmax()], np.sqrt(Xs[f.argmax()])))
worst = eps_need * f.max()
print("  => |c_T/c - 1| = |dc_T^2/c^2|/2 <= %.3e for EVERY background" % (worst / 2))
print("  GW170817: |c_T/c - 1| < 1e-15   [IMPORTED: Abbott et al. 2017, ApJL 848, L13]")
ck("GW170817 PASSED by the constraint-reduced result", worst / 2 < 1e-15,
   "margin %.1e x.  Gen-1's Y_R failed the same test by ~29 orders, because its TT content "
   "carried k^4 -- an extra (k c^2/a0)^2 = 4e42 at LIGO frequencies." % (1e-15 / (worst / 2)))

head("6.  THE SCALAR SECTOR -- and it is NOT healthy  [DERIVED]")
Mb = D['par']['Mb']
Q = sp.Matrix([[1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 0, 0], [0, 0, 1]])
Ms = sp.expand(Q.T * Mb * Q)                    # exact (phi, B3, trace) scalar sector
Pr = sp.cancel(sp.together((Ms[[2], [2]] - Ms[[2], [0, 1]] * Ms[[0, 1], [0, 1]].inv()
                            * Ms[[0, 1], [2]])[0, 0]))
Pr = sp.cancel(sp.expand(Pr).subs(w**2, W))
U = sp.cancel(sp.diff(Pr, W))
print("  Constraint-reduced khronon inverse propagator:  P = U omega^2 - V(k) k^2")
print("      U = %s" % sp.simplify(U))
ck("U = (3 lam_K - 1)/(lam_K - 1): INDEPENDENT of eta_K, of F, and of eps",
   sp.simplify(U - (3 * lam - 1) / (lam - 1)) == 0)
ck("no-ghost  <=>  U > 0  <=>  lam_K > 1  or  lam_K < 1/3", True,
   "the FLRW branch (sign of the energy density) additionally requires lam_K > 1/3, so "
   "the physical no-ghost window is lam_K > 1")
Dnum = sp.expand(sp.numer(sp.cancel(Pr)).subs(W, cc * k**2))
qs = sp.Poly(Dnum, k)
top = sp.factor(qs.coeffs()[0])
cs_uv = sp.solve(sp.Eq(sp.expand(top), 0), cc)[0]
eta_par = eta - 2 * FX - 4 * X0 * FXX
top0 = sp.factor(sp.Poly(sp.expand(sp.numer(sp.cancel(Pr.subs(FY, 0))).subs(W, cc * k**2)),
                         k).coeffs()[0])
cs_ir = sp.solve(sp.Eq(sp.expand(top0), 0), cc)[0]
print("\n  eps = 0 (Y off), leading k:   c_s^2 = %s" % sp.factor(cs_ir))
ck("eps = 0 reproduces the khronometric form with eta -> eta_par := eta_K - 2F_X - 4X0 F_XX",
   sp.simplify(cs_ir - (lam - 1) * (2 - eta_par) / (eta_par * (3 * lam - 1))) == 0)
print("  eps != 0, leading k:          c_s^2 = %s" % sp.factor(cs_uv))
ck("for ANY eps != 0 -- either sign, any magnitude -- the UV scalar speed is "
   "(1 - lam_K)/(3 lam_K - 1)", sp.simplify(cs_uv - (1 - lam) / (3 * lam - 1)) == 0,
   "F_Y cancels out of the ratio ENTIRELY.  This is structural, not a smallness.")
for lv in (sp.Rational(11, 10), sp.Rational(3, 2), sp.Integer(3)):
    print("      lam_K = %-6s :  U = %+.4f   c_s^2(UV) = %+.4f"
          % (lv, float((3 * lv - 1) / (lv - 1)), float((1 - lv) / (3 * lv - 1))))
ck("U > 0 and c_s^2 < 0 together for every lam_K > 1: a genuine GRADIENT INSTABILITY "
   "(not a ghost)", all(float((3 * lv - 1) / (lv - 1)) > 0 and float((1 - lv) / (3 * lv - 1)) < 0
                        for lv in (1.1, 1.5, 3.0, 10.0)))
Mpp = sp.expand(Mb[0, 0])
print("\n  Mechanism.  The lapse-sector operator is")
print("      M_phiphi = %s" % sp.factor(Mpp))
kstar2 = sp.solve(sp.Eq(sp.cancel(Mpp / k**2), 0), k**2)[0]
ck("M_phiphi changes sign at  k*^2 = 3 eta_par / (4 eps A(X0) ell^2)",
   sp.simplify(kstar2 - 3 * eta_par / (4 * FY * ell**2)) == 0,
   "Y_a is the trace-free HESSIAN of ln N, so it puts -(8/3) eps A ell^2 k^4 into the "
   "LAPSE equation, with the sign OPPOSITE to eta_par.  Below k* the lapse sector is "
   "eta_par-dominated (healthy); above k* it is Y-dominated and the khronon goes "
   "gradient-unstable.")

head("7.  HOW BAD IS IT?  [DERIVED]")


def kstar(x, epsv, etaK=0.0):
    X = x * x
    Aa = X**2 / (1 + X)**4
    etp = etaK + 2.0 / (1 + x)**2                  # eta_par at background x, frozen F
    return np.sqrt(3 * etp / (4 * epsv * Aa * ellv**2))


csuv = np.sqrt(0.0996 / 2.2989)     # |c_s| at the BBN-edge lam_K (companion script), for a rate
print("  eta_K = 0 (the value both the deep-MOND limit and the stability window force).")
print("  Every mode with k > k* grows;  growth rate |omega| = |c_s| c k.")
print("\n  %-26s %-11s %-12s %-13s %s" % ("environment", "x = g/a0", "k* [1/m]",
                                          "lambda* [m]", "growth time at k*"))
for lab, xv in (("deep MOND, galaxy edge", 0.1), ("MOND transition", 1.0),
                ("inner galaxy", 10.0), ("1 AU from the Sun", 0.0059 / a0),
                ("Earth's surface", 9.81 / a0)):
    ks = kstar(xv, eps_need)
    print("  %-26s %-11.3g %-12.3e %-13.3e %.3e s   (%.2e yr)"
          % (lab, xv, ks, 2 * np.pi / ks, 1 / (csuv * c_l * ks),
             1 / (csuv * c_l * ks) / 3.156e7))
print("""
  Every one of those wavelengths is MACROSCOPIC, and every one sits far inside any
  reasonable EFT cutoff, so this is not an artefact of the derivative truncation:
  at k*, the Y-term is comparable to eta_par (both ~1e-15 at 1 AU) but both are utterly
  negligible against the "1" of (3)R and K_ij K^ij.  The derivative expansion is fine.
  What is anomalous is that eta_par = 2/(1+x)^2 is TINY in the Solar System, so the
  4-derivative lapse term overtakes it absurdly early.""")
print("\n  How small must eps be to push k* above a UV cutoff 1/L_c?")
for Lc, nm in ((1.24e-4, "0.13 mm  (the deep-MOND cubic scale already in the repo)"),
               (1e-2, "1 cm"), (1.0, "1 m")):
    for xv, en in ((0.0059 / a0, "1 AU"), (1.0, "X0 = 1")):
        X = xv * xv
        Aa = X**2 / (1 + X)**4
        etp = 2.0 / (1 + xv)**2
        epsmax = 3 * etp / (4 * Aa * ellv**2 * (1.0 / Lc)**2)
        print("     cutoff %-48s at %-6s :  eps < %.2e   (short by %.1e x)"
              % (nm, en, epsmax, eps_need / epsmax))
print("""
  That table depends on a choice of UV cutoff, which is arguable.  Here is the same
  question with NO cutoff assumption at all -- just "the unstable wavelength must be
  shorter than a length on which we already trust GR":""")
print("     %-34s %-14s %s" % ("require lambda* shorter than", "at X0 = 1", "at 1 AU (x=6.3e7)"))
for S, sn in ((1.496e11, "1 AU  = 1.5e11 m"), (6.96e8, "the solar radius"),
              (6.4e6, "the Earth's radius"), (1.0, "1 metre")):
    row = []
    for xv in (1.0, 0.0059 / a0):
        X = xv * xv
        Aa = X**2 / (1 + X)**4
        etp = 2.0 / (1 + xv)**2
        row.append(3 * etp / (4 * Aa * ellv**2 * (2 * np.pi / S)**2))
    print("     %-34s eps < %-8.1e eps < %.1e" % (sn, row[0], row[1]))
print("""
  Can eta_K rescue it?  k*^2 scales as eta_par = eta_K + 2/(1+x)^{2}, and khronon
  stability needs eta_eff = eta_K + 2/(1+x) < 2, i.e. eta_K < 2 (and section (1b) of the
  companion script forces eta_K = 0 outright).  Even at the absolute ceiling eta_K = 2:""")
for xv, en in ((0.0059 / a0, "1 AU"), (1.0, "X0 = 1")):
    X = xv * xv
    Aa = X**2 / (1 + X)**4
    for ek, ekn in ((0.0, "eta_K = 0"), (2.0, "eta_K = 2 (excluded, shown as a ceiling)")):
        etp = ek + 2.0 / (1 + xv)**2
        ks = np.sqrt(3 * etp / (4 * eps_need * Aa * ellv**2))
        print("     %-8s %-42s k* = %.3e 1/m   lambda* = %.3e m"
              % (en, ekn, ks, 2 * np.pi / ks))
print("""     At 1 AU, eta_K = 2 buys 7.8 orders in k* (because eta_par there is only 5e-16)
     and brings lambda* from 8e7 m down to 1.3 m -- still macroscopic, and it costs the
     deep-MOND limit.  At X0 = 1, where eta_par is already 0.5, it buys a factor 2.2 and
     nothing else.  The galaxy environment is the binding one and eta_K cannot move it.

  CAVEATS, stated because they are the only ways out I can see:
     * this is the QUADRATIC spectrum.  A nonlinear analysis could in principle saturate
       the growth; that is not computed here.
     * matter perturbations were set to zero.  The unstable modes are vacuum khronon
       modes, so matter cannot remove them, but it can change the growth rate.
     * the instability is removed if the frozen F is replaced by one with F_X -> 0 more
       slowly, i.e. if eta_par does not collapse as 2/(1+x)^2 in the Newtonian regime.
       That is a change to the MOND kernel, not a tuning of eps.""")

head("8.  CORRECTION TO THE REPO'S OWN TEXT  [DERIVED]")
print("""  ya_tensor_exact_2026.py section F asserts the TT content is "IDENTICALLY ZERO for
  a wave parallel to a^(0)".  That contradicts checks B1/B3 in the SAME file, which verify
  <dT.dT> = (1/4) a^2 k^2 (h+^2 + hx^2) for BOTH directions.  The present exact
  calculation confirms B1/B3: both directions give the same c_T^2.  Section F is a stale
  sentence, not a second result; the physical conclusion of that script is unchanged.""")

head("9.  INDEPENDENT CROSS-VALIDATION  [DERIVED elsewhere, agreeing here]")
print("""  A second agent worked the same ruling concurrently in this directory with entirely
  separate code (gen2_constraint_reduced_tensor_2026.py, 41/41; and
  constraint_reduced_scalar_2026.py).  Its results and mine agree item by item:

    quantity                       this script            the companion scripts
    ------------------------------ ---------------------- ------------------------------
    K_T                            1                      1
    G_T                            1 + 2 eps X0^3/(1+X0)^4  same, "EXACT, isotropic"
    k^4 in the tensor sector       none                   none
    lapse symbol                   2 eta_par k^2
                                   - (8/3) eps A ell^2 k^4  Sigma = 2 alpha k^2 - (8/3) eps A k^4
    sign-flip wavenumber           k*^2 = 3 eta_par/(4 eps A ell^2)   k_deg^2 = 3 alpha/(4 eps A)
    reduced scalar kinetic coeff   (3L-1)/(L-1)           4(3L-1)/(L-1)  [field normalisation]
    eta_par, eta_perp              eta_K + 2/(1+x)^2 , eta_K + 2/(1+x)    identical
    eta_K = 0 forced               yes                    yes
    scalar sector verdict          gradient-unstable      gradient-unstable, both eps signs
    ya_tensor section F            stale, corrected       stale, corrected

  Two INDEPENDENT derivations, one shared conclusion.  Two items they raise that this
  script does NOT close, and that I therefore inherit:
    * the factor-2 point: 2 eps A X0 is delta(c_T^2)/c^2, and the GW170817 bound is on
      |c_T/c - 1| = half of it.  Handled here (section 5 divides by 2).
    * NOT ESTABLISHED, by either of us: the background acceleration was taken UNIFORM, so
      T^(0)_ij = 0 exactly.  A real galaxy has T^(0)_ij =/= 0, which switches on a LINEAR
      delta-Y source and a T^(0).delta^2 T cross term.  Power counting suppresses them by
      1/(kL) ~ 1e-21 at LIGO, but that is an estimate, not a derivation.  It is the next
      tensor-sector item, and it does not touch the scalar-sector kill, which is driven
      by the lapse piece TF[d_i d_j phi] and needs no background gradient at all.""")

head("VERDICT")
print("""  TENSOR  [DERIVED; constraints solved, nothing set to zero by hand]

      K_T = 1                       (never a ghost; lam_K- and eta_K-blind)
      G_T = 1 + 2 eps A(X0) X0      (k-INDEPENDENT: no k^4 anywhere)
      c_T^2/c^2 = 1 + 2 eps A(X0) X0  for h_x and for both polarisations at k || a^(0);
                = 1 + 2u + 2u^2 (lam_K-1)/(2 lam_K-1) + O(u^3)  for h_+ at k perp a^(0)
      max over all backgrounds: |c_T/c - 1| <= 0.105 eps = 1.2e-25  vs the 1e-15 bound.

    The promising k^2 behaviour SURVIVES the full ADM constraints.  Elimination of the
    lapse and shift changes the tensor sector by exactly one thing: an O((eps A X0)^2)
    +/x birefringence at k perpendicular to a^(0), ~1e-50.  Four theorems, not
    assumptions, are why: helicity decoupling at k || a; the transversality theorem for
    the Y operator; delta R^(1)[gamma_TT] = 0; and K^(0)_ij = 0.  Gen-1's GW no-go does
    NOT transfer.  Carl's first question gets a clean YES.

  SCALAR  [DERIVED]   NO -- the frozen Gen-2 action is not healthy.

      U = (3 lam_K - 1)/(lam_K - 1)                       (eps-, eta_K-, F-blind)
      c_s^2(k << k*) = (lam_K-1)(2-eta_par)/(eta_par(3 lam_K-1))   > 0   healthy
      c_s^2(k >> k*) = (1 - lam_K)/(3 lam_K - 1)                   < 0   for lam_K > 1
      k*^2 = 3 eta_par / (4 eps A(X0) ell^2)

    At eps = 1.1e-24 the instability sets in at 8.2e7 m in the Solar System and 2.6e15 m
    (0.084 pc) at the MOND transition, with growth times of 0.2 s and 0.2 yr respectively.
    Pushing it below scales on which GR is already tested needs eps <~ 1e-33 (1 AU at
    X0 = 1) and eps <~ 1e-58 for a millimetre cutoff -- 9 to 34 orders below the
    phenomenological window, depending on how conservative one is.

  THE STRUCTURAL POINT.  Gen-1's Y_R is built from the SPATIAL METRIC, so its
  4-derivative, 1/a0^4-carrying operator lands on the TENSORS (k^4 -> GW170817, ~29
  orders).  Gen-2's Y_a is built from the LAPSE, so it misses the tensors -- and lands
  on the SCALAR instead (9 to 34 orders, depending on the cutoff assumed).  The two generations fail in mirror-image sectors
  for the same reason.  Any repair must find an invariant whose 4-derivative content is
  suppressed in BOTH sectors, not moved from one to the other.""")
print("\nFAILURES: %s" % (FAIL if FAIL else "none"))
sys.exit(1 if FAIL else 0)
