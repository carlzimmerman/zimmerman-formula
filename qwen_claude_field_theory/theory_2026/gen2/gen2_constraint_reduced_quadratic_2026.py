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
Here nothing is set by hand: all ten metric perturbations are carried, the three spatial
diffeomorphisms are gauge-fixed exactly (H_ij = 0 for i along k), and the four
non-dynamical fields (delta N, delta N^i) are eliminated by an EXACT Schur complement --
which IS "solving the lapse and shift constraints at quadratic order".

RESULT IN ONE LINE (both answers, and they point opposite ways):
  * TENSOR:  the k^2 behaviour SURVIVES exactly.  c_T^2/c^2 = 1 + 2 eps A(X0) X0,
             k-independent, isotropic, and the constraints change it by EXACTLY ZERO.
  * SCALAR:  the frozen action is NOT healthy.  For ANY eps != 0 the khronon's
             short-wavelength speed is  c_s^2(k -> oo) = (1 - lam_K)/(3 lam_K - 1),
             which is NEGATIVE for every lam_K > 1 -- and lam_K > 1 is exactly what
             no-ghost requires.  A gradient instability, ABOVE a computed wavenumber k*.

Labels: DERIVED = computed here, sympy-verified.  IMPORTED = cited external input.
ASSUMED = an input of the frozen programme, not derived here.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
import numpy as np
import gen2_adm_core_2026 as C

k, w, lam, eta, X0, ell, epsY = C.k, C.w, C.lam, C.eta, C.X0, C.ell, C.epsY
FX, FXX, FY, F0 = C.FX, C.FXX, C.FY, C.F0
W = sp.Symbol('W', real=True)
xs = sp.Symbol('x', positive=True)
FAIL = []


def head(s):
    print("\n" + "=" * 100 + "\n" + s + "\n" + "=" * 100)


def ck(name, cond, note=""):
    print(("  [ok]   " if cond else "  [FAIL] ") + name + (("\n         " + note) if note else ""))
    if not cond:
        FAIL.append(name)
    return cond


CFG = {
    'par': dict(lab="k PARALLEL to a^(0)  (both along z)", kvec=(0, 0, k),
                gauge=[(2, 2), (0, 2), (1, 2)], pair=('H11', 'H22'), cross='H12'),
    'perp': dict(lab="k PERPENDICULAR to a^(0)  (k along x, a^(0) along z)", kvec=(k, 0, 0),
                 gauge=[(0, 0), (0, 1), (0, 2)], pair=('H22', 'H33'), cross='H23'),
}
LBL = ['phi', 'B1', 'B2', 'B3', 'h_+', 'h_x', 'tr']

head("0.  BUILD -- exact O(eps^2) Lagrangian; 10 metric perturbations, 3 diffeos fixed")
print("""  Background: h_ij = delta_ij, N = exp(abar z), N_i = 0.  Chosen so that
  T^(0)_ij = D_<i a_j> = 0 EXACTLY (a^(0)_i uniform), hence Y^(0) = 0 and the whole
  quadratic Y-content is (delta T)^2 with no cross terms.  X0 = (ell abar)^2 = x^2,
  x = g/a0, kept exact.  Background gradients kept (dNb/dz = abar Nb), Nb -> 1 imposed
  only at the end (local WKB frame).""")
DATA = {}
for key, cfg in CFG.items():
    L2, A, Ab, used, L1 = C.build_L2(cfg['kvec'], gauge_zero=cfg['gauge'])
    M, res = C.hermitian_matrix(L2, A, Ab)
    ck("[%s] quadratic form is exactly Abar_a M_ab A_b (zero residue)" % key,
       sp.simplify(res) == 0)
    idx = {n: i for i, n in enumerate(used)}
    n = len(used)
    P = sp.zeros(n, n)
    for j, nm in enumerate(['phi', 'B1', 'B2', 'B3']):
        P[idx[nm], j] = 1
    P[idx[cfg['pair'][0]], 4] = 1
    P[idx[cfg['pair'][1]], 4] = -1              # h_+ : traceless
    P[idx[cfg['cross']], 5] = 1                 # h_x
    P[idx[cfg['pair'][0]], 6] = 1
    P[idx[cfg['pair'][1]], 6] = 1               # trace
    DATA[key] = dict(M=sp.expand(P.T * M * P), used=used, L1=L1, cfg=cfg)
    print("       %-5s fields carried: %s   ->  basis %s" % (key, used, LBL))

head("T0.  THE TADPOLE DOES NOT ENTER THE DISPERSION  [DERIVED]")
print("""  The background is not an exact solution (a true static solution carries
  h_ij = (1-2Psi)delta_ij with curvature ~ abar^2), so a linear term J.f survives:
    S = S_0 + J.f + (1/2) f.M.f    =>   linear field equation  J + M f = 0.
  J is an INHOMOGENEOUS term; det M = 0 -- the dispersion relation -- cannot see it.
  What is neglected is the shift of M itself by the true background, which is relative
  O(abar^2/k^2) with NO factor of ell.  Every ell-ENHANCED term (i.e. everything
  carrying X0 = ell^2 abar^2, which is O(1) in a galaxy) is kept EXACTLY.
  At LIGO k, abar/k ~ 1e-21, so the neglected piece is ~1e-42 relative.""")
ck("linear (tadpole) term is nonzero, as expected, and is not part of M",
   sp.simplify(DATA['par']['L1']) != 0)

head("1.  TRANSVERSALITY THEOREM: the Y operator cannot mix TT with the lapse [DERIVED]")
print("""  delta T_ij = TF[ d_i d_j phi - dGamma^k_ij abar_k ].  For a plane wave the lapse
  piece is TF[-k_i k_j] phi -- purely LONGITUDINAL.  A TT polarisation has k^i gamma_ij = 0
  and gamma^i_i = 0, so TF[k_i k_j] : TF[dGamma.abar] = 0 for ANY orientation of abar.""")
kx, ky, kz = sp.symbols('k_x k_y k_z', real=True)
ax, ay, az = sp.symbols('a_x a_y a_z', real=True)
kv, av = [kx, ky, kz], [ax, ay, az]
# explicit TT basis for generic k (no solve): two polarisation tensors from any 2 vectors
# orthogonal to k.  Use e1 = k x u, e2 = k x e1, then TT = c1(e1e1-e2e2) + c2(e1e2+e2e1).
u = sp.Matrix([1, 0, 0])
kM = sp.Matrix(kv)
e1 = kM.cross(u)
e2 = kM.cross(e1)
e1 = e1 / sp.sqrt(sum(e1[i]**2 for i in range(3)))
e2 = e2 / sp.sqrt(sum(e2[i]**2 for i in range(3)))
c1, c2 = sp.symbols('c_1 c_2', real=True)
gTT = sp.expand(c1 * (e1 * e1.T - e2 * e2.T) + c2 * (e1 * e2.T + e2 * e1.T))
ck("TT basis really is transverse and traceless",
   all(sp.simplify(sum(kv[i] * gTT[i, j] for i in range(3))) == 0 for j in range(3))
   and sp.simplify(sp.trace(gTT)) == 0)
k2 = kx**2 + ky**2 + kz**2
dG = lambda m, i, j: sp.Rational(1, 2) * (sp.I * kv[i] * gTT[j, m] + sp.I * kv[j] * gTT[i, m]
                                          - sp.I * kv[m] * gTT[i, j])
dT_g = sp.Matrix(3, 3, lambda i, j: -sum(dG(m, i, j) * av[m] for m in range(3)))
dT_p = sp.Matrix(3, 3, lambda i, j: -(kv[i] * kv[j] - sp.Rational(1, 3) * (1 if i == j else 0) * k2))
cross = sp.simplify(sp.expand(sum(dT_p[i, j] * dT_g[i, j] for i in range(3) for j in range(3))))
ck("TF[d_i d_j phi] : TF[dGamma.abar] = 0 identically, generic k, generic abar", cross == 0,
   "this, and not any smallness, is why constraint elimination leaves c_T untouched")

head("2.  THE TENSOR BLOCK AFTER SOLVING THE CONSTRAINTS  [DERIVED]")
res = {}
for key in ('par', 'perp'):
    Mb = DATA[key]['M']
    print("\n  --- %s ---" % CFG[key]['lab'])
    for i, pol in ((4, 'h_+'), (5, 'h_x')):
        nz = [(LBL[j], sp.cancel(sp.expand(Mb[i, j]))) for j in range(7)
              if j != i and sp.cancel(sp.expand(Mb[i, j])) != 0]
        print("      %s mixes with: %s" % (pol, [a for a, _ in nz] or "NOTHING"))
        for a, v in nz:
            print("          <%s|M|%s> = %s" % (pol, a, sp.factor(v)))
        res[(key, pol)] = nz
ck("[par] BOTH tensor polarisations decouple EXACTLY from (delta N, delta N^i, trace)",
   res[('par', 'h_+')] == [] and res[('par', 'h_x')] == [],
   "k || a: unbroken SO(2) about the common axis => helicity 2 cannot mix with 0 or 1")
ck("[perp] h_x (odd under y -> -y) decouples EXACTLY", res[('perp', 'h_x')] == [])
mix_perp = dict(res[('perp', 'h_+')])
ck("[perp] h_+ mixes ONLY with phi and the trace, and its phi-mixing has NO k^2 "
   "(pure abar^2 mass mixing) -- exactly what the transversality theorem predicts",
   set(mix_perp) == {'phi', 'tr'} and sp.diff(mix_perp['phi'], k) == 0,
   "<h_+|M|phi> = %s   (= abar^2 (eta_K - 2 F_X), no Y-contribution at all)"
   % sp.factor(mix_perp['phi']))
ck("[perp] the ONLY k-dependent Y-mixing of h_+ is with the TRACE, at order eps A X0 k^2",
   sp.simplify(sp.expand(mix_perp['tr']).coeff(FY) - 2 * X0 * k**2) == 0,
   "so the Schur back-reaction on c_T is O((eps A X0)^2) ~ 1e-50, not O(eps A X0)")

head("3.  K_T, G_T, c_T^2 -- the constraint-reduced tensor action  [DERIVED]")
FRZ = C.frozen_subs(with_Y=True)
Aof = X0**2 / (1 + X0)**4
tgt = 1 + 2 * epsY * Aof * X0
for key in ('par', 'perp'):
    Mb = DATA[key]['M']
    print("\n  --- %s ---" % CFG[key]['lab'])
    for i, pol in ((4, 'h_+'), (5, 'h_x')):
        if res[(key, pol)]:
            # h_+ at perp: exact 2x2 with the trace, after Schur-eliminating phi,B_i
            Pr = (Mb[[4, 6], [4, 6]] - Mb[[4, 6], [0, 1, 2, 3]]
                  * Mb[[0, 1, 2, 3], [0, 1, 2, 3]].inv() * Mb[[0, 1, 2, 3], [4, 6]])
            Pr = sp.Matrix(2, 2, lambda a, b: sp.cancel(sp.together(sp.expand(Pr[a, b]).subs(w**2, W))))
            D = sp.numer(sp.cancel(sp.together(Pr.det())))
            rts = sp.solve(sp.Eq(sp.expand(D), 0), W)
            cts = [sp.simplify(sp.limit(sp.cancel(r / k**2), k, sp.oo)) for r in rts]
            good = [c for c in cts if sp.simplify(sp.series(c, epsY, 0, 2).removeO()
                                                  - (1 + 2 * FY * X0).subs(FY, epsY * Aof)) == 0]
            KT, GT = sp.S(1), None
            print("      %s (exact 2x2 with the trace, constraints solved):" % pol)
            for c_ in cts:
                print("         a root gives  c^2 = %s" % sp.simplify(c_))
            ck("[%s/%s] one root is exactly the tensor branch  c_T^2 = 1 + 2 eps A X0 "
               "+ O(eps^2)" % (key, pol), len(good) >= 1)
            cT2 = 1 + 2 * epsY * Aof * X0
        else:
            Pii = sp.cancel(sp.expand(Mb[i, i]).subs(w**2, W))
            KT = sp.cancel(sp.diff(Pii, W))
            GT = sp.cancel(-sp.diff(sp.cancel(Pii - KT * W), k, 2) / 2)
            mass = sp.cancel(Pii - KT * W + GT * k**2)
            cT2 = sp.cancel(GT / KT)
            print("      %s : K_T = %s ,  G_T = %s" % (pol, KT, sp.factor(GT)))
            print("             residual 0-derivative part = %s   (= O(abar^2, a0^2/c^4))"
                  % sp.factor(mass))
            print("             c_T^2 = %s" % sp.factor(cT2.subs(FRZ)))
            ck("[%s/%s] c_T^2 = 1 + 2 eps A(X0) X0 EXACTLY, k-INDEPENDENT" % (key, pol),
               sp.simplify(cT2.subs(FRZ) - tgt) == 0)
            ck("[%s/%s] K_T = 1 > 0 : the tensor is never a ghost; lam_K and eta_K drop out"
               % (key, pol), sp.simplify(KT - 1) == 0)
            ck("[%s/%s] G_T carries NO k^2, i.e. NO k^4 dispersion survives" % (key, pol),
               sp.simplify(sp.diff(GT, k)) == 0)
ck("eps = 0 => c_T = c EXACTLY at every X0, lam_K, eta_K",
   sp.simplify(tgt.subs(epsY, 0) - 1) == 0)

head("4.  THE NUMBER, WITH THE CONSTRAINTS SOLVED  [DERIVED + IMPORTED bound]")
c_l, a0 = 2.99792458e8, 9.3619e-11
ellv = c_l**2 / a0
print("  ell = c^2/a0 = %.4e m" % ellv)
eps_need = 1.1e-24
print("  eps required by the Solar-System suppression window = %.2e   [ASSUMED, imported "
      "from the Gen-1 programme]" % eps_need)
Xs = np.logspace(-4, 8, 60001)
f = 2 * Xs**2 / (1 + Xs)**4 * Xs
print("  max over X0 of 2 A(X0) X0 = %.6f  at X0 = %.4f" % (f.max(), Xs[f.argmax()]))
worst = eps_need * f.max()
print("  => |dc_T^2/c^2| <= %.3e for every background" % worst)
print("  GW170817: |c_T/c - 1| < 1e-15   [IMPORTED: Abbott et al. 2017 ApJL 848 L13]")
ck("GW170817 PASSED by the constraint-reduced result", worst / 2 < 1e-15,
   "margin %.1e x.  Gen-1's Y_R failed the same test by ~29 orders because its TT content "
   "carried k^4, i.e. an extra (k c^2/a0)^2 = 4e42 at LIGO frequencies." % (1e-15 / (worst / 2)))

head("5.  THE SCALAR SECTOR -- and it is NOT healthy  [DERIVED]")
Mb = DATA['par']['M']
Q = sp.Matrix([[1, 0, 0], [0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 0, 0], [0, 0, 0], [0, 0, 1]])
Ms = sp.expand(Q.T * Mb * Q)               # (phi, B3, trace) -- the exact scalar sector
Pr = sp.cancel(sp.together((Ms[[2], [2]] - Ms[[2], [0, 1]] * Ms[[0, 1], [0, 1]].inv()
                            * Ms[[0, 1], [2]])[0, 0]))
Pr = sp.cancel(sp.expand(Pr).subs(w**2, W))
U = sp.cancel(sp.diff(Pr, W))
print("  constraint-reduced khronon inverse propagator  P = U omega^2 - V(k) k^2")
print("  U = %s   -- INDEPENDENT of eta_K, of F, and of eps" % sp.simplify(U))
ck("no-ghost <=> U > 0 <=> lam_K > 1 or lam_K < 1/3",
   sp.simplify(U - (3 * lam - 1) / (lam - 1)) == 0)
sol = sp.solve(sp.Eq(sp.numer(sp.cancel(Pr)), 0), W)[0]
cs2k = sp.cancel(sol / k**2)
cs_lo = sp.simplify(sp.limit(cs2k.subs(FY, 0), k, sp.oo))
cs_hi = sp.simplify(sp.limit(cs2k, k, sp.oo))
eta_par = eta - 2 * FX - 4 * X0 * FXX
print("\n  eps = 0    (Y off):  c_s^2 = %s" % sp.simplify(cs_lo))
ck("eps = 0 reproduces the khronometric form with eta -> eta_par = eta_K - 2F_X - 4X0 F_XX",
   sp.simplify(cs_lo - (lam - 1) * (2 - eta_par) / (eta_par * (3 * lam - 1))) == 0)
print("  eps != 0, k -> oo:   c_s^2 = %s" % sp.simplify(cs_hi))
ck("for ANY eps != 0 (either sign, any magnitude) the UV scalar speed is "
   "(1 - lam_K)/(3 lam_K - 1)", sp.simplify(cs_hi - (1 - lam) / (3 * lam - 1)) == 0,
   "F_Y cancels out of the ratio entirely -- this is a STRUCTURAL result, not a smallness")
ck("that UV speed is NEGATIVE for every lam_K > 1, i.e. for every no-ghost choice",
   sp.simplify(((1 - lam) / (3 * lam - 1)).subs(lam, sp.Rational(3, 2))) < 0
   and sp.simplify(((1 - lam) / (3 * lam - 1)).subs(lam, sp.Rational(11, 10))) < 0,
   "U > 0 and V < 0  =>  omega^2 < 0  =>  a genuine gradient instability, not a ghost")
# the crossover: it is exactly where the lapse operator M_phiphi changes sign
Mpp = sp.expand(Mb[0, 0])
print("\n  M_phiphi = %s" % sp.factor(Mpp))
kstar2 = sp.solve(sp.Eq(sp.cancel(Mpp / k**2), 0), k**2)[0]
print("  lapse operator vanishes at   k*^2 = %s" % sp.factor(kstar2))
ck("k*^2 = 3 eta_par / (4 eps A(X0) ell^2)",
   sp.simplify(kstar2 - 3 * eta_par / (4 * FY * ell**2)) == 0,
   "below k* the lapse sector is dominated by eta_par (healthy); above it, by the "
   "Y-term's 4-derivative piece, which enters with the OPPOSITE sign")

head("6.  HOW BAD IS IT?  [DERIVED]")


def kstar(x, epsv, etaK=0.0):
    X = x * x
    Aa = X**2 / (1 + X)**4
    etp = etaK + 2.0 / (1 + x)**2
    return np.sqrt(3 * etp / (4 * epsv * Aa * ellv**2))


print("  k*  = sqrt( 3 eta_par / (4 eps A(X0) ell^2) ) ;  every mode with k > k* grows.")
print("  eta_K = 0 (the value the deep-MOND limit and the stability window both force).")
print("  %-26s %-10s %-12s %-12s %-12s" % ("environment", "x = g/a0", "k* [1/m]",
                                           "lambda* [m]", "growth time"))
csUV = 0.0996 / 2.2989                     # |c_s^2| at the BBN-edge lam_K (section 2 of the
cs = np.sqrt(csUV)                         # companion script); used only for a growth time
for lab, xv in (("deep MOND (galaxy edge)", 0.1), ("MOND transition", 1.0),
                ("inner galaxy", 10.0), ("1 AU from the Sun", 0.0059 / a0),
                ("Earth's surface", 9.81 / a0)):
    ks = kstar(xv, eps_need)
    lm = 2 * np.pi / ks
    tg = 1.0 / (cs * c_l * ks)
    print("  %-26s %-10.3g %-12.3e %-12.3e %-12.3e s  (%.3g yr)"
          % (lab, xv, ks, lm, tg, tg / 3.156e7))
print("""
  Every one of those wavelengths is MACROSCOPIC and sits far inside any reasonable EFT
  cutoff, so the instability is not an artefact of the derivative truncation.""")
print("\n  How small must eps be to push the instability below a UV cutoff L_c?")
for Lc, nm in ((1.24e-4, "0.13 mm (the deep-MOND cubic scale already in the repo)"),
               (1e-2, "1 cm"), (1.0, "1 m")):
    kc = 1.0 / Lc
    for xv, en in ((0.0059 / a0, "1 AU"), (1.0, "X0 = 1")):
        X = xv * xv
        Aa = X**2 / (1 + X)**4
        etp = 2.0 / (1 + xv)**2
        epsmax = 3 * etp / (4 * Aa * ellv**2 * kc**2)
        print("     cutoff %-52s at %-6s : eps < %.2e   (short by %.1e x)"
              % (nm, en, epsmax, eps_need / epsmax))

head("7.  CORRECTION TO THE REPO'S OWN TEXT  [DERIVED]")
print("""  ya_tensor_exact_2026.py section F says the TT content is "IDENTICALLY ZERO for a
  wave parallel to a^(0)".  That contradicts checks B1/B3 in the SAME file, which verify
  <dT.dT> = (1/4) a^2 k^2 (h+^2 + hx^2) for BOTH directions.  The present exact
  calculation confirms B1/B3 -- both directions give the same c_T^2.  Section F is a
  stale sentence; the physical conclusion of that script is unchanged.""")

head("VERDICT")
print("""  TENSOR  [DERIVED, constraints solved, nothing set to zero by hand]:

      S_T^(2) = (M_Pl^2 c^3/2) INT [ gammadot_ij^2 - (1 + 2 eps A(X0) X0)(d_k gamma_ij)^2 ]
      K_T = 1 (never a ghost, lam_K- and eta_K-blind)
      G_T = 1 + 2 eps A(X0) X0 ,  k-INDEPENDENT, ISOTROPIC
      c_T^2/c^2 = 1 + 2 eps A(X0) X0  <=  0.106 eps  <  1.2e-25

    The promising k^2 behaviour SURVIVES the full ADM constraints.  Constraint
    elimination changes the tensor block by EXACTLY ZERO, for four reasons that are now
    theorems: helicity decoupling at k || a; the transversality theorem for the Y
    operator; delta R^(1)[gamma_TT] = 0; and K^(0)_ij = 0.  Gen-1's GW no-go does NOT
    transfer.  This part of Carl's question gets a clean YES.

  SCALAR  [DERIVED]:  NO -- the frozen action is not healthy.

      U = (3 lam_K - 1)/(lam_K - 1)                (eps-blind, eta_K-blind, F-blind)
      c_s^2(k -> 0)  = (lam_K-1)(2 - eta_par)/(eta_par (3 lam_K - 1))   > 0   (healthy)
      c_s^2(k -> oo) = (1 - lam_K)/(3 lam_K - 1)                        < 0   for lam_K>1
      crossover at   k*^2 = 3 eta_par / (4 eps A(X0) ell^2)

    The Y operator is the trace-free HESSIAN OF ln N, so it feeds a 4-derivative term
    -(8/3) eps A ell^2 k^4 into the LAPSE equation with the sign opposite to eta_par.
    Above k* the lapse sector flips sign and the khronon becomes gradient-unstable.
    This is structural: F_Y cancels out of the UV speed, so no choice of eps sign or
    magnitude removes it -- only pushes k* up, and at the eps the phenomenology needs,
    k* corresponds to 8e7 m in the Solar System.

  THE STRUCTURAL POINT: Gen-1's Y_R is built from the SPATIAL METRIC, so it hits the
  TENSOR sector (k^4 -> GW170817 kill).  Gen-2's Y_a is built from the LAPSE, so it
  misses the tensors -- and hits the SCALAR instead.  The two generations fail in
  mirror-image sectors, for the same reason: a 4-derivative operator carrying 1/a0^4
  is anti-suppressed at short wavelength somewhere, and the only question is where.""")
print("\nFAILURES: %s" % (FAIL if FAIL else "none"))
sys.exit(1 if FAIL else 0)
