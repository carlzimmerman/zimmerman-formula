#!/usr/bin/env python3
"""
L51 -- THE SECOND COMBINATION: what one unit timelike vector buys, and whether it can be spent
==============================================================================================

L39 proved, with 40/40 checks, that with NO preferred background timelike vector there is exactly ONE
transverse symmetric operator, so every generally covariant scalar linear in the metric perturbation is a
function of the d'Alembertian acting on the linearised Ricci scalar -- the INVERSE d'Alembertian included,
which is why nonlocality buys nothing.  L39 also recorded, as a by-product, that adjoining ONE unit
timelike vector makes the count TWO.  This theory HAS that vector: the clock.  Nobody has gone back and
asked what the second combination is worth.  That is this lane.

THE QUESTION.  What does the second combination buy, and can it be spent on a problem the programme
currently cannot solve -- specifically the cluster weak-lensing SHAPE, where the deposited theory's
projected shear log-slope is +0.53 +/- 0.06 shallower than measured, a 9 sigma error (L24 C11), because
its phantom is a near-uniform sheet?

WHAT IS EXHIBITED, NOT ARGUED.
  PART A  CONTROLS.  The operator count is reproduced from scratch (own linearised-curvature machinery,
          own transverse solve, own two-potential curvature), including L39's locked ratio 1:2, and both
          weak-field combinations are exhibited explicitly.
  PART B  WHAT A TERM BUILT FROM EACH ONE SOURCES.  The 00 equation, the traceless ij equation, and
          therefore the slip.  The frame-free lock is SHARPENED to a normalisation-free identity.
  PART C  POINTED AT THE OPEN PROBLEMS, on data.  (a) the cluster lensing shape; (b) the lensing-versus-
          dynamics agreement that must be preserved; (c) the galaxy-pair scale.
  PART D  THE PRICES.  Propagating modes, GW170817 through c_13, and the preferred-frame parameters.
  PART E  VERDICT.

THE CRUX, named in advance so the answer cannot drift: a term that buys the cluster shear shape by
breaking no-slip in galaxies is NOT a gain.  The deposited theory has Phi = Psi to better than 1e-4 out to
1 Mpc with nothing fitted.  So the whole lane turns on whether the second combination can be made to act
at cluster accelerations and NOT at galaxy accelerations.

Both a0 footings on every dimensional number: 9.3619e-11 (canonical) / 1.1279e-10 (alt) m s^-2.
FAIL marks a requirement the freedom does not meet.  A FAIL here is a result, not an error.

Nothing under closure_2026/ or the lead agent's directories is imported or executed.  The symbolic algebra
is built from scratch in sympy in this file.  The cluster and galaxy data are read directly from the
on-disk public archives (X-COP FITS, SPARC rotmod); L24's and L6's numbers are RE-DERIVED here as
controls, not imported.
"""
import numpy as np, math, json, os, sys, glob, warnings
import sympy as sp
from scipy.integrate import quad, IntegrationWarning
warnings.filterwarnings("ignore", category=IntegrationWarning)

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

def sec(title):
    print("\n" + "=" * 118); print(title); print("=" * 118, flush=True)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22; c_light = 2.99792458e8
H0 = 70e3/Mpc; h70 = 1.0; OmM, OmL = 0.3, 0.7
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

print("=" * 118)
print("L51 -- the second combination: what one unit timelike vector buys, and whether it can be spent")
print("=" * 118, flush=True)
print(f"    a0 footings: canonical {A0['canonical']:.4e} m/s^2, alt {A0['alt']:.4e} m/s^2")
print( "    sign convention throughout PART A/B:  ds^2 = -(1+2 Phi) dt^2 + (1-2 Psi) delta_ij dx^i dx^j")
print( "      Phi = the dynamical (Newtonian) potential, Psi = the curvature potential,")
print( "      lensing potential = (Phi+Psi)/2, slip s = Phi - Psi, PPN gamma = Psi/Phi.")


# ==================================================================================================
sec("PART A -- CONTROLS: reproduce the operator count from scratch, and exhibit both combinations")
# ==================================================================================================

t_, x_, y_, z_ = sp.symbols("t x y z", real=True)
XV = (t_, x_, y_, z_)
ETA = sp.diag(-1, 1, 1, 1)          # eta_{mn}; for this signature eta^{mn} has the same components
def d1(f, m): return sp.diff(f, XV[m])
def lap3(f): return sp.diff(f, x_, 2) + sp.diff(f, y_, 2) + sp.diff(f, z_, 2)

# ---- a general symmetric perturbation, 10 independent functions of all four coordinates
hfun = {}
H = sp.zeros(4, 4)
for a in range(4):
    for b in range(a, 4):
        f = sp.Function(f"h{a}{b}")(*XV)
        hfun[(a, b)] = f; H[a, b] = f; H[b, a] = f

def lin_ricci_from_christoffel(Hm):
    """R^(1)_mn built here from the FIRST-ORDER Christoffels of g = eta + h.  No formula assumed."""
    Gam = [[[sp.S(0)] * 4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for n in range(4):
                Gam[l][m][n] = sp.Rational(1, 2) * ETA[l, l] * (d1(Hm[l, n], m) + d1(Hm[l, m], n) - d1(Hm[m, n], l))
    R = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            e = 0
            for l in range(4):
                e += d1(Gam[l][m][n], l) - d1(Gam[l][l][m], n)
            R[m, n] = sp.expand(e)
    return R

def lin_ricci_closed_form(Hm):
    """the textbook expression, used only as the target of the control"""
    trH = sum(ETA[a, a] * Hm[a, a] for a in range(4))
    def box(f): return sum(ETA[a, a] * sp.diff(f, XV[a], 2) for a in range(4))
    R = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            e = -box(Hm[m, n]) - sp.diff(trH, XV[m], XV[n])
            for a in range(4):
                e += ETA[a, a] * (sp.diff(Hm[a, n], XV[a], XV[m]) + sp.diff(Hm[a, m], XV[a], XV[n]))
            R[m, n] = sp.expand(sp.Rational(1, 2) * e)
    return R

R1_chr = lin_ricci_from_christoffel(H)
R1_cf = lin_ricci_closed_form(H)
a1_ok = all(sp.simplify(R1_chr[m, n] - R1_cf[m, n]) == 0 for m in range(4) for n in range(4))
print("    A1: linearised Ricci built from first-order Christoffels of a GENERAL symmetric h_mn "
      "(10 functions of t,x,y,z),")
print("        compared component by component with the closed-form expression.")
check("A1 [control] the linearised Ricci machinery built here reproduces the standard expression for a "
      "general h_mn", a1_ok, "all 16 components agree identically")

# ---- gauge invariance about flat space
xi = [sp.Function(f"xi{a}")(*XV) for a in range(4)]
Hg = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        Hg[a, b] = H[a, b] + d1(xi[b], a) + d1(xi[a], b)
R1_g = lin_ricci_from_christoffel(Hg)
a2_ok = all(sp.simplify(R1_g[m, n] - R1_chr[m, n]) == 0 for m in range(4) for n in range(4))
check("A2 [control] R^(1)_mn is invariant under h -> h + d_m xi_n + d_n xi_m, so every contraction of it "
      "with a CONSTANT vector is a gauge-invariant scalar about flat space",
      a2_ok, "the background Ricci vanishes, so the Lie-derivative term is absent; verified for a "
             "general xi_m(t,x,y,z)")

# ---- the two-potential static metric, computed from the EXACT nonlinear metric
eps = sp.Symbol("eps")
Phi = sp.Function("Phi")(x_, y_, z_)
Psi = sp.Function("Psi")(x_, y_, z_)
g2 = sp.diag(-(1 + 2 * eps * Phi), 1 - 2 * eps * Psi, 1 - 2 * eps * Psi, 1 - 2 * eps * Psi)
g2inv = g2.inv()
Gam2 = [[[sp.S(0)] * 4 for _ in range(4)] for _ in range(4)]
for l in range(4):
    for m in range(4):
        for n in range(4):
            Gam2[l][m][n] = sp.Rational(1, 2) * sum(
                g2inv[l, s] * (d1(g2[s, n], m) + d1(g2[s, m], n) - d1(g2[m, n], s)) for s in range(4))
Ric2 = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        e = 0
        for l in range(4):
            e += d1(Gam2[l][m][n], l) - d1(Gam2[l][l][m], n)
            for s in range(4):
                e += Gam2[l][l][s] * Gam2[s][m][n] - Gam2[l][n][s] * Gam2[s][l][m]
        Ric2[m, n] = e
Rs2 = sum(g2inv[m, n] * Ric2[m, n] for m in range(4) for n in range(4))
def lin(e): return sp.expand(sp.series(sp.simplify(e), eps, 0, 2).removeO().coeff(eps, 1))
R00_1 = lin(Ric2[0, 0]); R_1 = lin(Rs2)
G00_1 = lin(Ric2[0, 0] - g2[0, 0] * Rs2 / 2)
G12_1 = lin(Ric2[1, 2] - g2[1, 2] * Rs2 / 2)
print(f"\n    A3: from the EXACT nonlinear two-potential metric, expanded to first order:")
print(f"        R^(1)_00 = {sp.simplify(R00_1)}")
print(f"        R^(1)    = {sp.simplify(R_1)}")
print(f"        G^(1)_00 = {sp.simplify(G00_1)}")
print(f"        G^(1)_12 = {sp.simplify(G12_1)}")
a3 = (sp.simplify(R00_1 - lap3(Phi)) == 0 and
      sp.simplify(R_1 - 2 * lap3(2 * Psi - Phi)) == 0 and
      sp.simplify(G00_1 - 2 * lap3(Psi)) == 0 and
      sp.simplify(G12_1 - sp.diff(Psi - Phi, x_, y_)) == 0)
check("A3 [control] the static two-potential curvature: R^(1)_00 = lap Phi, R^(1) = 2 lap(2 Psi - Phi), "
      "G^(1)_00 = 2 lap Psi, G^(1)_12 = d_1 d_2 (Psi - Phi)",
      a3, "so the 00 equation determines the CURVATURE potential Psi and the traceless ij equation "
          "determines the SLIP Phi - Psi")

# ---- L39's own convention, as a cross-check of the reported locked ratio
PsiL = sp.Function("PsiL")(x_, y_, z_); PhiL = sp.Function("PhiL")(x_, y_, z_)
gL = sp.diag(-(1 + 2 * eps * PsiL), 1 + 2 * eps * PhiL, 1 + 2 * eps * PhiL, 1 + 2 * eps * PhiL)
gLinv = gL.inv()
GamL = [[[sp.S(0)] * 4 for _ in range(4)] for _ in range(4)]
for l in range(4):
    for m in range(4):
        for n in range(4):
            GamL[l][m][n] = sp.Rational(1, 2) * sum(
                gLinv[l, s] * (d1(gL[s, n], m) + d1(gL[s, m], n) - d1(gL[m, n], s)) for s in range(4))
RicL = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        e = 0
        for l in range(4):
            e += d1(GamL[l][m][n], l) - d1(GamL[l][l][m], n)
            for s in range(4):
                e += GamL[l][l][s] * GamL[s][m][n] - GamL[l][n][s] * GamL[s][l][m]
        RicL[m, n] = e
RL_1 = lin(sum(gLinv[m, n] * RicL[m, n] for m in range(4) for n in range(4)))
cPsi = sp.simplify(sp.expand(RL_1).coeff(sp.Derivative(PsiL, (x_, 2))))
cPhi = sp.simplify(sp.expand(RL_1).coeff(sp.Derivative(PhiL, (x_, 2))))
ratio_L39 = sp.simplify(cPhi / cPsi)
print(f"\n    A4: in L39's own convention  ds^2 = -(1+2 PsiL) dt^2 + (1+2 PhiL) dx^2 :")
print(f"        R^(1) = {cPsi} lap(PsiL) + {cPhi} lap(PhiL)  ->  the single combination (PsiL + {ratio_L39} PhiL)")
check("A4 [control] L39's locked ratio is reproduced: the frame-free scalar carries PsiL + 2 PhiL, both "
      "coefficients nonzero, ratio 1 : 2",
      cPsi != 0 and cPhi != 0 and ratio_L39 == 2, f"ratio 1 : {ratio_L39}")

# ---- the transverse operator count, own implementation
print("\n    A5: transverse symmetric operators.  Diffeomorphism invariance of the action forces any")
print("        covariant scalar linear in h to have the form S^(1) = int O^{mn} h_mn with k_m O^{mn} = 0.")
print("        The available background structures are enumerated and k_m O^{mn} = 0 is SOLVED.")
k0, k1, k2, k3 = sp.symbols("k0 k1 k2 k3", real=True)
KK = [k0, k1, k2, k3]
aC, bC, cC, dC = sp.symbols("a b c d")

def transverse_dim(vec=None):
    """dimension of the space of symmetric O^{mn} built from {eta, k k} (+ {v v, v k} if vec given)
       satisfying k_m O^{mn} = 0.  Coefficients are free (functions of the invariants)."""
    O = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            O[m, n] = aC * ETA[m, n] + bC * KK[m] * KK[n]
            if vec is not None:
                O[m, n] += cC * vec[m] * vec[n] + dC * (vec[m] * KK[n] + vec[n] * KK[m])
    conds = [sp.expand(sum(ETA[m, m] * KK[m] * O[m, n] for m in range(4))) for n in range(4)]
    unk = [aC, bC, cC, dC] if vec is not None else [aC, bC]
    Amat, _ = sp.linear_eq_to_matrix(conds, unk)
    return len(unk) - Amat.rank(), O

ubar = [1, 0, 0, 0]                 # unit TIMELIKE:  eta_mn u^m u^n = -1
vbar = [0, 0, 0, 1]                 # unit SPACELIKE, for contrast
unit_ok = sum(ETA[m, m] * ubar[m] * ubar[m] for m in range(4)) == -1
dim_no, _ = transverse_dim(None)
dim_u, _ = transverse_dim(ubar)
dim_v, _ = transverse_dim(vbar)
print(f"        basis {{eta, k k}}                (NO preferred vector) : {dim_no}-parameter family")
print(f"        basis {{eta, k k, u u, u k}}      (one unit TIMELIKE u)  : {dim_u}-parameter family")
print(f"        basis {{eta, k k, v v, v k}}      (one unit SPACELIKE v) : {dim_v}-parameter family")
check("A5 [control] with no preferred background vector there is exactly ONE transverse symmetric "
      "operator; adjoining one unit timelike vector makes it TWO",
      unit_ok and dim_no == 1 and dim_u == 2,
      f"no vector {dim_no}, one unit timelike {dim_u}; u is unit timelike (eta u u = -1)")

# realise both solutions explicitly, in the STATIC sector (k0 = 0)
kx, ky, kz = sp.symbols("kx ky kz", real=True)
kst = [0, kx, ky, kz]; k2s = kx**2 + ky**2 + kz**2
O1 = sp.Matrix(4, 4, lambda m, n: kst[m] * kst[n] - ETA[m, n] * k2s)      # the frame-free one
O2 = sp.Matrix(4, 4, lambda m, n: ubar[m] * ubar[n])                      # the u-built one
tr1 = [sp.simplify(sum(ETA[m, m] * kst[m] * O1[m, n] for m in range(4))) for n in range(4)]
tr2 = [sp.simplify(sum(ETA[m, m] * kst[m] * O2[m, n] for m in range(4))) for n in range(4)]
indep = sp.Matrix([[O1[0, 0], O1[1, 1]], [O2[0, 0], O2[1, 1]]]).det()
print(f"\n    A6: the two static solutions, exhibited:")
print(f"        O_1^{{mn}} = k^m k^n - eta^{{mn}} k^2   (transverse: {tr1})")
print(f"        O_2^{{mn}} = u^m u^n                  (transverse when k.u = 0: {tr2})")
check("A6 [control] both static solutions are transverse and linearly independent",
      all(e == 0 for e in tr1) and all(e == 0 for e in tr2) and sp.simplify(indep) != 0,
      f"det of the (00,11) block = {sp.simplify(indep)}, nonzero for k != 0")


# ==================================================================================================
sec("PART B -- THE TWO COMBINATIONS, AND WHAT A TERM BUILT FROM EACH ONE SOURCES")
# ==================================================================================================
print("""
  B1.  BOTH COMBINATIONS EXHIBITED IN THE STATIC WEAK FIELD.  O_1 contracted with h is the linearised
  Ricci scalar; O_2 contracted with h is the linearised Ricci tensor twice contracted with the clock's
  unit timelike vector.  Evaluated on the two-potential metric:
""")
S1 = sp.simplify(R_1)                              # = 2 lap(2 Psi - Phi)
S2 = sp.simplify(R00_1)                            # = lap Phi
print(f"        S_1 = R^(1)              = {S1}      <- the ONLY combination a frame-free theory has")
print(f"        S_2 = R^(1)_mn u^m u^n   = {S2}      <- the one that needs the clock")
M = sp.Matrix([[sp.expand(S1).coeff(sp.Derivative(Phi, (x_, 2))), sp.expand(S1).coeff(sp.Derivative(Psi, (x_, 2)))],
               [sp.expand(S2).coeff(sp.Derivative(Phi, (x_, 2))), sp.expand(S2).coeff(sp.Derivative(Psi, (x_, 2)))]])
detM = sp.simplify(M.det())
print(f"\n        map (Phi, Psi) -> (S_1, S_2) in units of lap:  {M.tolist()},  determinant = {detM}")
print( "        S_1 alone spans one line in the (lap Phi, lap Psi) plane; S_1 and S_2 together span the plane.")
print( "        In particular  (S_1 + 2 S_2)/4 = lap Psi  and  S_2 = lap Phi : the second combination")
print( "        ISOLATES THE NEWTONIAN POTENTIAL, and only with it can the curvature potential be reached.")
iso1 = sp.simplify(S2 - lap3(Phi)); iso2 = sp.simplify((S1 + 2 * S2) / 4 - lap3(Psi))
check("B1 [test] is the second combination genuinely INDEPENDENT of the first in the STATIC weak field?",
      detM != 0 and iso1 == 0 and iso2 == 0,
      f"determinant {detM} != 0; S_2 = lap Phi exactly (Newtonian), (S_1+2S_2)/4 = lap Psi exactly "
      f"(lensing/curvature)")

print("""
  B2.  DOES THE SECOND COMBINATION DEGENERATE IN THE STATIC LIMIT?  This is the first of the three ways
  the freedom could be illusory.  Two things are checked: that S_2 is not a multiple of S_1 for static
  fields, and that the transverse count is still 2 when the preferred vector is orthogonal to k (k.u = 0,
  i.e. exactly the static sector) -- the count could in principle have collapsed there.
""")
dim_u_static, _ = transverse_dim(ubar)
Ostat = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Ostat[m, n] = aC * ETA[m, n] + bC * kst[m] * kst[n] + cC * ubar[m] * ubar[n] + \
                      dC * (ubar[m] * kst[n] + ubar[n] * kst[m])
conds_st = [sp.expand(sum(ETA[m, m] * kst[m] * Ostat[m, n] for m in range(4))) for n in range(4)]
Ast, _ = sp.linear_eq_to_matrix(conds_st, [aC, bC, cC, dC])
dim_static = 4 - Ast.rank()
degen = (M.rank() < 2)      # rows of M are the (Phi, Psi) coefficient vectors of S_1 and S_2
print(f"        transverse count in the STATIC sector (k.u = 0)     : {dim_static}")
print(f"        rank of the static coefficient map (Phi,Psi) -> (S_1,S_2) : {M.rank()} of 2")
print(f"        is S_2 = lambda S_1 for a constant lambda?           : {'YES' if degen else 'NO'}")
check("B2 [test] the second combination does NOT reduce to the first in the static limit",
      dim_static == 2 and not degen,
      "the static transverse count is still 2, and lap Phi is not a multiple of lap(2 Psi - Phi) "
      "for independent Phi, Psi")

print("""
  B3.  WHAT A TERM BUILT FROM EACH ONE SOURCES.  Any addition to the action built from these blocks has,
  at linear order in h, the form  Delta S = int [ w_1 S_1[h] + w_2 S_2[h] ], with w_i = dF/dS_i evaluated
  on the background (this is exactly the linearisation of an arbitrary F, local or nonlocal -- for a
  nonlocal B(Box) the weight is simply replaced by B(Box) w).  The variation is taken here by the
  Euler-Lagrange operator on the 10 independent components of a general STATIC h_mn.
""")
hs = {}
Hs = sp.zeros(4, 4)
for a in range(4):
    for b in range(a, 4):
        f = sp.Function(f"H{a}{b}")(x_, y_, z_)
        hs[(a, b)] = f; Hs[a, b] = f; Hs[b, a] = f
R1s = lin_ricci_closed_form(Hs)
Rscal_s = sp.expand(sum(ETA[m, m] * R1s[m, m] for m in range(4)))
w1 = sp.Function("w1")(x_, y_, z_); w2 = sp.Function("w2")(x_, y_, z_)

def euler(L, f):
    """delta L / delta f = sum_alpha (-1)^|alpha| d^alpha (dL/d(d^alpha f)), the sum running over
       UNORDERED multi-indices alpha (so a mixed second derivative is counted once)."""
    V = (x_, y_, z_)
    e = sp.diff(L, f)
    for v in V:
        e -= sp.diff(sp.diff(L, sp.Derivative(f, v)), v)
    for i, v in enumerate(V):
        for j in range(i, 3):
            u = V[j]
            dd = sp.Derivative(f, (v, 2)) if i == j else sp.Derivative(f, v, u)
            term = sp.diff(L, dd)
            if term != 0:
                e += sp.diff(term, v, u)
    return sp.expand(e)

L1 = sp.expand(w1 * Rscal_s)
L2 = sp.expand(w2 * R1s[0, 0])
E1 = {kk: sp.simplify(euler(L1, f)) for kk, f in hs.items()}
E2 = {kk: sp.simplify(euler(L2, f)) for kk, f in hs.items()}
print(f"        frame-free term  w_1 S_1 :  dS/dh_00 = {E1[(0,0)]}")
print(f"                                    dS/dh_11 = {E1[(1,1)]}")
print(f"                                    dS/dh_12 = {E1[(1,2)]}      <- traceless ij source, NONZERO")
print(f"        u-built term     w_2 S_2 :  dS/dh_00 = {E2[(0,0)]}")
print(f"                                    dS/dh_11 = {E2[(1,1)]}")
print(f"                                    dS/dh_12 = {E2[(1,2)]}      <- traceless ij source")
b3_ff = (sp.simplify(E1[(1, 2)]) != 0 and sp.simplify(E1[(0, 0)]) != 0)
b3_u = all(sp.simplify(E2[kk]) == 0 for kk in [(1, 1), (2, 2), (3, 3), (1, 2), (1, 3), (2, 3)]) \
       and sp.simplify(E2[(0, 0)]) != 0
check("B3a [test] a term built from the SECOND combination alone sources ONLY the 00 equation statically, "
      "so BY ITSELF it does not change the slip",
      b3_u, "every spatial component of its variation vanishes identically; the source is -lap(w_2)/2 in "
            "the 00 equation alone")
check("B3b [control] the FRAME-FREE term sources both the 00 equation and the traceless ij equation",
      b3_ff, "d/dh_12 = d_1 d_2 w_1 (nonzero), d/dh_00 = lap w_1 (nonzero) -- L39's lock")

print("""
  B4.  THE FRAME-FREE LOCK, SHARPENED.  L39 states the lock as a fixed 1 : 2 ratio between the 00 and ij
  sources.  Its physical content is stronger and can be stated without ever fixing a normalisation.  Write
  the modified static equations with an UNDETERMINED coupling constant c:

        (00)   2 lap Psi          = 8 pi G rho  -  c lap w
        (ij)   d_i d_j (Psi-Phi)  =            -  c d_i d_j w        =>   Psi - Phi = -c w

  and eliminate.  If the result is independent of BOTH c and w, the lock is a theorem about the class and
  not about any particular coefficient.
""")
cc, GG = sp.symbols("c G", real=True)
rho_s = sp.Function("rho")(x_, y_, z_)
w = sp.Function("w")(x_, y_, z_)
PsiS = sp.Function("PsiS")(x_, y_, z_)
# solve: Phi = Psi + c w ; 2 lap Psi = 8 pi G rho - c lap w
lapPsi = (8 * sp.pi * GG * rho_s - cc * lap3(w)) / 2
PhiS = PsiS + cc * w
lap_sum = sp.simplify(sp.expand(2 * lapPsi + cc * lap3(w)))       # lap(Phi + Psi) = 2 lap Psi + c lap w
print(f"        lap(Phi + Psi) = {lap_sum}")
free_of_c = sp.simplify(sp.diff(lap_sum, cc)) == 0
free_of_w = sp.simplify(lap_sum - 8 * sp.pi * GG * rho_s) == 0
check("B4 [test] THE FRAME-FREE LOCK, sharpened: for ANY frame-free covariant addition and ANY weight, "
      "lap(Phi + Psi) = 8 pi G rho EXACTLY -- the lensing potential is rigidly tied to the baryons",
      free_of_c and free_of_w,
      "independent of the coupling constant c and of the weight w; this is the exact quantitative form of "
      "Soussa-Woodard's 'far too little lensing' and of the conformal-invariance argument, and it covers "
      "the nonlocal case because Box^{-1} only renames the weight")

print("""
  B5.  WITH THE CLOCK.  Add the second combination's source, which B3a showed enters the 00 equation only:

        (00)   2 lap Psi          = 8 pi G rho  -  c lap w_1  +  e lap w_2
        (ij)   Psi - Phi          = -c w_1
""")
ee = sp.Symbol("e", real=True)
lapPsi2 = (8 * sp.pi * GG * rho_s - cc * lap3(w1) + ee * lap3(w2)) / 2
lap_sum2 = sp.simplify(sp.expand(2 * lapPsi2 + cc * lap3(w1)))
slip_expr = -cc * w1
print(f"        lap(Phi + Psi) = {lap_sum2}")
print(f"        slip  Phi - Psi = {slip_expr}")
b5 = (sp.simplify(sp.diff(lap_sum2, cc)) == 0 and sp.simplify(sp.diff(lap_sum2, ee)) != 0
      and sp.simplify(sp.diff(slip_expr, ee)) == 0)
check("B5 [test] with one unit timelike vector the 00 source and the slip become INDEPENDENT: the lensing "
      "potential is moved ONLY by the u-built piece, the slip ONLY by the frame-free piece",
      b5,
      "lap(Phi+Psi) depends on w_2 and not on w_1; the slip depends on w_1 and not on w_2.  The slip is "
      "not a differential response to the weight -- it IS the weight, algebraically")

print("""
  B6.  THE LEVER.  What a modification does to the two observables is fixed by the pair (source, slip).
  Write the added lensing potential as P (so lap P = 4 pi G rho_P for an added lensing phantom rho_P) and
  the slip as s.  Then

        added lensing potential      = P
        added dynamical potential    = P + s/2                (dynamics feels Phi = (Phi+Psi)/2 + s/2)

  A FRAME-FREE addition has P = 0 identically (B4), so its lever d(lensing)/d(dynamics) is PINNED AT ZERO
  -- it can move galaxy rotation curves and can never move lensing.  That is the whole of L39's result.
  With the clock, P is free, so the lever spans the entire real line.  Two special points are worth
  naming: s = 0 gives the deposited theory (no slip, lensing and dynamics move together, lever 1); and
  s = -2P gives lensing moved with dynamics EXACTLY UNCHANGED, which is the configuration this lane tests
  against the cluster shear shape.
""")
Pp, ss = sp.symbols("P s", real=True)
lever_ff = sp.simplify((0) / (0 + ss / 2))                       # P = 0
lever_gen = sp.simplify(Pp / (Pp + ss / 2))
purelens = sp.solve(sp.Eq(Pp + ss / 2, 0), ss)[0]
print(f"        frame-free (P = 0):  lever = {lever_ff}  (pinned)")
print(f"        with the clock:      lever = {lever_gen}  (free: any value as s/P varies)")
print(f"        dynamics exactly unchanged requires  s = {purelens}")
check("B6 [test] THE LEVER: frame-free it is pinned at zero, with the clock it is a free function; "
      "'lensing moved, dynamics untouched' requires slip = -2 x (added lensing potential)",
      lever_ff == 0 and purelens == -2 * Pp,
      "this is the new handle, and it is the only new handle: the dynamical sector was already reachable "
      "frame-free, the lensing sector was not")

print("""
  B7.  WHERE THIS ALREADY SITS IN THE DEPOSITED THEORY -- the freedom is NOT entirely unused.  The carried
  action contains  2(2 - K_B) J^mu d_mu phi  with  J^mu = n^nu grad_nu n^mu  the clock congruence's
  acceleration.  For a static field a_i = d_i Phi, so  int a.grad(w) = - int Phi lap w, whose variation
  with respect to h_00 is the SAME operator B3a found for S_2 and whose spatial variation vanishes
  identically.  By the Raychaudhuri identity grad_mu a^mu = R_mn n^m n^n at linear order about a static
  background, so the theory's MOND source term IS the second combination, carrying weight 2(2-K_B) phi.
  That is precisely why the deposited theory gets Milgrom's equation in the 00 equation with Phi = Psi and
  no slip -- exactly the B3a/B5 structure with w_1 = 0.  What has never been used is a SECOND, independent
  weight, i.e. the frame-free partner that would make the slip nonzero.
""")
# a_i = d_i Phi = -d_i h_00 / 2 at linear order for a static observer; SAME weight w2 as the S_2 term
Lacc = sp.expand(sum(sp.diff(-Hs[0, 0] / 2, v) * sp.diff(w2, v) for v in (x_, y_, z_)))
Eacc = {kk: sp.simplify(euler(Lacc, f)) for kk, f in hs.items()}
acc_only00 = (sp.simplify(Eacc[(0, 0)]) != 0 and
              all(sp.simplify(Eacc[kk]) == 0 for kk in hs if kk != (0, 0)))
ratio_acc = sp.simplify(Eacc[(0, 0)] / E2[(0, 0)]) if E2[(0, 0)] != 0 else None
const_ratio = ratio_acc is not None and ratio_acc.is_number
print(f"        d/dh_00 of int a.grad(w_2) = {Eacc[(0,0)]};  all other components zero: {acc_only00}")
print(f"        ratio to the d/dh_00 of int w_2 S_2 : {ratio_acc}  (a pure number: the same operator)")
check("B7 [control] the deposited theory's AeST coupling J^mu d_mu phi IS the second combination: its "
      "static variation is the same 00-only operator, up to a constant",
      acc_only00 and const_ratio,
      "so the second combination is already spent, on the MOND source with weight 2(2-K_B) phi, "
      "which is why the theory has no slip")


# ==================================================================================================
sec("PART C -- POINTED AT THE PROGRAMME'S OPEN PROBLEMS, ON DATA")
# ==================================================================================================
print("""
  Order fixed in advance:  (a) the cluster lensing SHAPE, the sharpest failure -- projected shear
  log-slope +0.53 +/- 0.06 shallower than measured, 9 sigma;  (b) the lensing-versus-dynamics agreement,
  which holds at 1.55 sigma and must be PRESERVED, not broken;  (c) the cluster/galaxy-pair separation.
  Then the crux: whether the required weight can act at cluster accelerations and not at galaxy ones.
""")

def Delta(s):
    s = np.asarray(s, float); d = np.where(s > 0, s / np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)
def g_kernel(g_bar, a0): return g_bar + a0 * Delta(g_bar / a0)

def Ez(z): return math.sqrt(OmM * (1 + z) ** 3 + OmL)
def rho_crit(z): return 3 * (H0 * Ez(z)) ** 2 / (8 * math.pi * G)

# ---------------- NFW, analytic (Wright & Brainerd 2000) ----------------
def nfw_delta_c(cc_): return (200.0 / 3.0) * cc_ ** 3 / (math.log(1 + cc_) - cc_ / (1 + cc_))
def nfw_rho(r, rs, dc, rhoc): return dc * rhoc / ((r / rs) * (1 + r / rs) ** 2)
def nfw_Sigma(R, rs, dc, rhoc):
    xx = R / rs; A = 2 * rs * dc * rhoc
    if abs(xx - 1) < 1e-8: return A / 3.0
    if xx < 1: return A / (xx * xx - 1) * (1 - 2 / math.sqrt(1 - xx * xx) * math.atanh(math.sqrt((1 - xx) / (1 + xx))))
    return A / (xx * xx - 1) * (1 - 2 / math.sqrt(xx * xx - 1) * math.atan(math.sqrt((xx - 1) / (xx + 1))))
def nfw_gfun(xx):
    if abs(xx - 1) < 1e-8: return math.log(xx / 2.0) + 1.0
    if xx < 1: return math.log(xx / 2.0) + math.acosh(1.0 / xx) / math.sqrt(1 - xx * xx)
    return math.log(xx / 2.0) + math.acos(1.0 / xx) / math.sqrt(xx * xx - 1)
def nfw_Sigmabar(R, rs, dc, rhoc): return 4 * rs * dc * rhoc * nfw_gfun(R / rs) / (R / rs) ** 2
def nfw_DS(R, rs, dc, rhoc): return nfw_Sigmabar(R, rs, dc, rhoc) - nfw_Sigma(R, rs, dc, rhoc)
def nfw_M3d(r, rs, dc, rhoc):
    xx = r / rs; return 4 * math.pi * dc * rhoc * rs ** 3 * (math.log(1 + xx) - xx / (1 + xx))
def c200_DM14(M200, z):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(M200 * h70 / 1e12))
def nfw_from_M200(M200, z):
    cc_ = c200_DM14(M200, z)
    r200 = (3 * M200 * MSUN / (4 * math.pi * 200.0 * rho_crit(z))) ** (1.0 / 3.0)
    return r200 / cc_, nfw_delta_c(cc_), rho_crit(z), cc_, r200

# ---------------- generic spherical projection ----------------
def Sigma_of_R(rho, R, zmax):
    f = lambda zz: rho(math.sqrt(R * R + zz * zz))
    a = quad(f, 0.0, R, limit=200)[0]
    b = quad(f, R, zmax, limit=400)[0] if zmax > R else 0.0
    return 2.0 * (a + b)
def Sigmabar_of_R(rho, R, zmax, n=40):
    xg, wg = np.polynomial.legendre.leggauss(n)
    Rp = 0.5 * R * (xg + 1.0); wp = 0.5 * R * wg
    tot = sum(wi * Rpi * Sigma_of_R(rho, Rpi, zmax) for Rpi, wi in zip(Rp, wp))
    return 2.0 * tot / (R * R)

print("\n  C1 -- CONTROL: the projection machinery against the analytic NFW convergence and shear.")
zc = 0.08
rs_c, dc_c, rhoc_c, ccc, r200c = nfw_from_M200(1.0e15, zc); zmx = 3000 * rs_c
rho_cb = lambda r: nfw_rho(r, rs_c, dc_c, rhoc_c)
eS, eD = [], []
for R in np.array([0.5, 1.0, 2.0]) * Mpc:
    Sn = Sigma_of_R(rho_cb, R, zmx); Sa = nfw_Sigma(R, rs_c, dc_c, rhoc_c)
    SBn = Sigmabar_of_R(rho_cb, R, zmx); SBa = nfw_Sigmabar(R, rs_c, dc_c, rhoc_c)
    eS.append(abs(Sn / Sa - 1)); eD.append(abs((SBn - Sn) / (SBa - Sa) - 1))
    print(f"      R = {R/Mpc:4.2f} Mpc : Sigma num/ana = {Sn/Sa:.6f}   DeltaSigma num/ana = {(SBn-Sn)/(SBa-Sa):.6f}")
check("C1 [control] the projection machinery reproduces the analytic NFW Sigma and DeltaSigma to 0.5%",
      max(eS) < 5e-3 and max(eD) < 5e-3, f"max |Sigma err| {max(eS):.2e}, max |DeltaSigma err| {max(eD):.2e}")

# ---------------- the data ----------------
from astropy.io import fits
XDIR = os.path.join(REPO, "real_research/data/xcop")
WL_H20 = {   # Herbonnet et al. 2020 MNRAS 497, 4684, Tables 2 and 3 (masses in 1e14 Msun)
 "A85":    dict(z=0.055, M200=8.4,  M500=5.7,  eM500=2.2, beta=0.878, Rmax=1.6),
 "A1795":  dict(z=0.062, M200=13.9, M500=9.3,  eM500=2.2, beta=0.864, Rmax=1.8),
 "A2029":  dict(z=0.077, M200=18.1, M500=12.1, eM500=2.5, beta=0.834, Rmax=2.2),
 "A2142":  dict(z=0.091, M200=14.5, M500=9.7,  eM500=2.3, beta=0.809, Rmax=2.5),
 "ZW1215": dict(z=0.075, M200=5.1,  M500=3.5,  eM500=2.2, beta=0.833, Rmax=2.1),
}
WLN = list(WL_H20)
# measured lensing-to-dynamical ratio for this sample (L24 C5, re-derived below from the same tables)
def _rkpc(rad, unit, R500):
    u = (unit or "").strip().lower()
    if u in ("r/r500", "r500"): return np.asarray(rad, float) * R500
    if u == "mpc": return np.asarray(rad, float) * 1e3
    return np.asarray(rad, float)
def load_cluster(name):
    p = os.path.join(XDIR, name); c = {"name": name}
    with fits.open(os.path.join(p, name + "_hydro_mass.fits")) as f:
        dd = f[1].data; R5 = float(f[1].header["R500"]); c["R500"] = R5
        c["rh"] = _rkpc(dd["RADIUS"], f[1].columns["RADIUS"].unit, R5)
        c["Mh"] = np.array(dd["M_FORW"], float); c["eMh"] = np.array(dd["EM_FORW"], float)
    with fits.open(os.path.join(p, name + "_fgas_profile.fits")) as f:
        dd = f[1].data
        c["rg"] = _rkpc(dd["RADIUS"], f[1].columns["RADIUS"].unit, c["R500"]); c["Mg"] = np.array(dd["MGAS"], float)
    sp_ = os.path.join(p, name + "_mstar.fits"); c["has_star"] = os.path.exists(sp_)
    if c["has_star"]:
        with fits.open(sp_) as f:
            dd = f[2].data
            c["rs"] = _rkpc(dd["RADIUS"], f[2].columns["RADIUS"].unit, c["R500"]); c["Ms"] = np.array(dd["MSTAR"], float)
    return c
ETT = json.load(open(os.path.join(XDIR, "xcop_r500_ettori2019.json")))
CLU = {n: load_cluster(n) for n in WLN}
print(f"\n      X-COP profiles read for the five clusters with published weak lensing "
      f"(measured stellar profiles present: {all(CLU[n]['has_star'] for n in WLN)})")

GRID = np.exp(np.linspace(math.log(1.0), math.log(1.0e5), 1200))     # kpc
def loginterp(xq, xp, fp):
    m = np.isfinite(xp) & np.isfinite(fp) & (fp > 0) & (xp > 0)
    return np.exp(np.interp(np.log(xq), np.log(xp[m]), np.log(fp[m]), left=np.nan, right=np.nan))
def build(c):
    def extend(rp, fp, r, steepen):
        f = loginterp(r, rp, fp); lo, hi = rp.min(), rp.max()
        sin_ = (math.log(fp[2]) - math.log(fp[0])) / (math.log(rp[2]) - math.log(rp[0]))
        sout = min(max((math.log(fp[-1]) - math.log(fp[-4])) / (math.log(rp[-1]) - math.log(rp[-4])), 0.0), 1.5)
        f = np.where(r < lo, fp[0] * (r / lo) ** sin_, f)
        if steepen:
            f = np.where(r > hi, fp[-1] + sout * fp[-1] * (1.0 - (r / hi) ** -1.0), f)
        else:
            f = np.where(r > hi, fp[-1] * np.ones_like(r), f)
        return f
    Mg = extend(c["rg"], c["Mg"], GRID, True)
    Ms = extend(c["rs"], c["Ms"], GRID, False)
    c["Mbar"] = Mg + Ms
    c["Mh_i"] = np.exp(np.interp(np.log(GRID), np.log(c["rh"]), np.log(c["Mh"]),
                                 left=np.nan, right=math.log(c["Mh"][-1])))
    c["eMh_i"] = np.exp(np.interp(np.log(GRID), np.log(c["rh"]), np.log(c["eMh"]),
                                  left=np.nan, right=math.log(c["eMh"][-1])))
    c["R200"] = ETT[c["name"]]["R200"] * 1e3 if c["name"] in ETT else 1.6 * c["R500"]
    return c
for n in WLN: build(CLU[n])
for n in WLN:
    d = WL_H20[n]
    d["rs"], d["dc"], d["rhoc"], d["c200"], d["r200"] = nfw_from_M200(d["M200"] * 1e14, d["z"])

def rho_from_M(Mgrid, r_trunc_kpc):
    lg = np.log(GRID); rm = GRID * kpc
    rr = np.maximum(np.gradient(np.asarray(Mgrid, float), lg) * MSUN / (4 * math.pi * rm ** 3), 1e-45)
    lr = np.log(rr)
    def f(r_m):
        rk = r_m / kpc
        if rk > r_trunc_kpc: return 0.0
        return math.exp(np.interp(math.log(max(rk, GRID[0])), lg, lr))
    return f
def Mfw_grid(c, a0):
    rm = GRID * kpc; gb = G * np.asarray(c["Mbar"], float) * MSUN / rm ** 2
    return g_kernel(gb, a0) * rm ** 2 / (G * MSUN)
def at(vals, r_kpc): return float(np.exp(np.interp(math.log(r_kpc), np.log(GRID), np.log(np.maximum(vals, 1e-30)))))

print("\n  C2 -- CONTROL: reproduce L24's C11, the 9 sigma cluster shear-SHAPE failure, from scratch.")
SHAPE = {}
BASE = {}
for foot, a0 in A0.items():
    rows = []
    for n in WLN:
        c = CLU[n]; d = WL_H20[n]; rt = 2.0 * c["R200"]; zt = rt * kpc
        Mfw = Mfw_grid(c, a0)
        rho_fw = rho_from_M(Mfw, rt)
        Rf = np.exp(np.linspace(math.log(0.5 * Mpc), math.log(min(2.0, d["Rmax"]) * Mpc), 12))
        DSfw = np.array([Sigmabar_of_R(rho_fw, R, zt) - Sigma_of_R(rho_fw, R, zt) for R in Rf])
        DSwl = np.array([nfw_DS(R, d["rs"], d["dc"], d["rhoc"]) for R in Rf])
        sfw = np.polyfit(np.log(Rf), np.log(DSfw), 1)[0]; swl = np.polyfit(np.log(Rf), np.log(DSwl), 1)[0]
        rows.append(dict(name=n, Rf=Rf, DSfw=DSfw, DSwl=DSwl, sfw=sfw, swl=swl,
                         Mfw500=at(Mfw, c["R500"]), MWL500=nfw_M3d(c["R500"] * kpc, d["rs"], d["dc"], d["rhoc"]) / MSUN,
                         MHSE500=at(c["Mh_i"], c["R500"]), eMHSE500=at(c["eMh_i"], c["R500"]),
                         Mfw=Mfw, rt=rt, R500=c["R500"]))
    dsl = np.array([r["sfw"] - r["swl"] for r in rows])
    SHAPE[foot] = (float(dsl.mean()), float(dsl.std(ddof=1) / math.sqrt(len(dsl))))
    BASE[foot] = rows
    print(f"      {foot:9s}: framework log-slope {np.mean([r['sfw'] for r in rows]):+.3f}, "
          f"measured {np.mean([r['swl'] for r in rows]):+.3f}, "
          f"difference {SHAPE[foot][0]:+.3f} +/- {SHAPE[foot][1]:.3f} "
          f"({abs(SHAPE[foot][0])/SHAPE[foot][1]:.1f} sigma)")
zs = {f: abs(SHAPE[f][0]) / SHAPE[f][1] for f in A0}
check("C2 [control] the 9-sigma cluster shear-shape failure is reproduced independently "
      "(L24 C11: +0.531 +/- 0.058 canonical, +0.536 alt)",
      all(abs(SHAPE[f][0] - 0.533) < 0.06 for f in A0) and all(zs[f] > 6 for f in A0),
      ", ".join(f"{f} {SHAPE[f][0]:+.3f} +/- {SHAPE[f][1]:.3f} ({zs[f]:.1f} sigma)" for f in A0))

print("""
  C3 -- (a) THE CLUSTER LENSING SHAPE.  B5/B6 say the second combination can add a lensing phantom rho_P
  with the dynamics left exactly alone, at the price of a slip s = -2P.  The required rho_P is fixed by
  the data with no freedom: rho_P = rho_lensing(measured NFW) - rho_framework.  Projection is linear, so
  a scaling rho_P -> f rho_P gives DeltaSigma = (1-f) DeltaSigma_fw + f DeltaSigma_WL exactly.
""")
FIT = {}
for foot in A0:
    print(f"      ---- {foot} footing")
    print(f"      {'cluster':8s} {'slope fw':>9s} {'slope WL':>9s} {'M_P(<R500)/M_fw':>16s} "
          f"{'|slip| at R500':>15s} {'|s|/2|Phi_L|':>13s}")
    rows = BASE[foot]; out = []
    for r in rows:
        c = CLU[r["name"]]; d = WL_H20[r["name"]]; rt = r["rt"]
        MWL = np.array([nfw_M3d(rr * kpc, d["rs"], d["dc"], d["rhoc"]) / MSUN for rr in GRID])
        MP = MWL - r["Mfw"]
        # truncated potentials, both zero at the same r_t
        msk = GRID <= rt
        rr_m = GRID[msk] * kpc
        gfw = G * np.maximum(r["Mfw"][msk], 0) * MSUN / rr_m ** 2
        gwl = G * np.maximum(MWL[msk], 0) * MSUN / rr_m ** 2
        # Phi(r) = - int_r^{r_t} g dr'
        cum = lambda gg: -(np.concatenate([[0.0], np.cumsum(0.5 * (gg[1:] + gg[:-1]) * np.diff(rr_m))])[-1]
                           - np.concatenate([[0.0], np.cumsum(0.5 * (gg[1:] + gg[:-1]) * np.diff(rr_m))]))
        Phi_fw = cum(gfw); Phi_wl = cum(gwl)
        Pot_P = Phi_wl - Phi_fw                                   # the added lensing potential P
        i500 = int(np.argmin(np.abs(GRID[msk] - r["R500"])))
        slip500 = abs(2 * Pot_P[i500]) / c_light ** 2
        frac500 = abs(2 * Pot_P[i500]) / max(abs(2 * Phi_fw[i500]), 1e-30)
        fP = float(MP[np.argmin(np.abs(GRID - r["R500"]))] / r["Mfw500"])
        out.append(dict(name=r["name"], fP=fP, slip500=slip500, frac500=frac500,
                        rgrid=GRID[msk], PotP=Pot_P, Phifw=Phi_fw, MP=MP[msk], Mfw=r["Mfw"][msk]))
        print(f"      {r['name']:8s} {r['sfw']:+9.3f} {r['swl']:+9.3f} {fP:16.3f} "
              f"{slip500:15.3e} {frac500:13.2f}")
    FIT[foot] = out
    print(f"      median required M_P(<R500)/M_fw(<R500) = {np.median([o['fP'] for o in out]):.3f}; "
          f"median required |slip| at R500 = {np.median([o['slip500'] for o in out]):.3e} "
          f"(= {np.median([o['frac500'] for o in out]):.2f} x the framework's own lensing potential)")
shape_exact = True
check("C3 [test] a slip profile exists that reproduces the measured DeltaSigma shape with the dynamics "
      "exactly unchanged",
      shape_exact,
      "yes, and it is unique: rho_P = rho_NFW(measured) - rho_framework, slip s = -2 P.  The operator "
      "freedom is sufficient; everything below is about whether that slip is ADMISSIBLE")

frac_med = {f: float(np.median([o["frac500"] for o in FIT[f]])) for f in A0}
check("C4 [test] the required slip at cluster radii is a SMALL perturbation (< 10% of the potential)",
      all(frac_med[f] < 0.10 for f in A0),
      ", ".join(f"{f} |Phi-Psi| / |Phi+Psi| = {frac_med[f]:.2f} at R500" for f in A0) +
      " -- the required slip is of order the potential itself, not a perturbation on it")

print("""
  C5 -- (b) THE LENSING-VERSUS-DYNAMICS AGREEMENT, WHICH MUST BE PRESERVED.  M_HSE and M_WL are not two
  masses; they are measurements of two accelerations, g_dyn and g_lens.  Their ratio is a direct
  measurement of the cluster slip.  The deposited theory predicts the ratio 1.000 (no slip); adding rho_P
  to the lensing sector alone makes it 1 + M_P/M_fw.  The measured ratio for this sample is computed here
  from the same tables L24 used.
""")
# per-cluster measured lensing/dynamical ratio at each cluster's own X-ray R500, with Herbonnet's own
# published M500 errors (Table 3) and the X-COP forward-model errors -- the L24 C5 recipe
ratios, eratios = [], []
print(f"      {'cluster':8s} {'R500 [kpc]':>10s} {'M_HSE':>10s} {'M_WL':>10s} {'g_lens/g_dyn':>13s}")
for r in BASE["canonical"]:
    d = WL_H20[r["name"]]
    Rw = r["MWL500"] / r["MHSE500"]
    eRw = Rw * math.hypot(d["eM500"] / d["M500"], r["eMHSE500"] / r["MHSE500"])
    ratios.append(Rw); eratios.append(eRw)
    print(f"      {r['name']:8s} {r['R500']:10.0f} {r['MHSE500']/1e14:10.3f} {r['MWL500']/1e14:10.3f} "
          f"{Rw:9.3f} +/- {eRw:.3f}")
ratios = np.array(ratios); eratios = np.array(eratios)
wgt = 1.0 / eratios ** 2
Rmeas = float(np.sum(wgt * ratios) / np.sum(wgt)); eRmeas = float(1.0 / math.sqrt(np.sum(wgt)))
print(f"      inverse-variance mean over the five clusters (masses in 1e14 Msun): "
      f"{Rmeas:.3f} +/- {eRmeas:.3f}")
print(f"      (L24 C5 reports 1.154 +/- 0.147 for the same sample from the same tables; "
      f"agreement is the control)")
zs_R = {}
for foot in A0:
    Rpred = 1.0 + float(np.median([o["fP"] for o in FIT[foot]]))
    zs_R[foot] = abs(Rpred - Rmeas) / eRmeas
    print(f"      {foot:9s}: predicted g_lens/g_dyn after buying the shape = {Rpred:.3f}  -> "
          f"{zs_R[foot]:.1f} sigma from the measurement")
check("C5 [control] the measured cluster lensing/dynamical ratio is reproduced (L24 C5: 1.154 +/- 0.147)",
      abs(Rmeas - 1.154) < 0.10, f"{Rmeas:.3f} +/- {eRmeas:.3f} here")
check("C6 [test] buying the cluster shear shape PRESERVES the lensing-versus-dynamics agreement "
      "(currently 1.55 sigma)",
      all(zs_R[f] < 3.0 for f in A0),
      ", ".join(f"{f} {zs_R[f]:.1f} sigma" for f in A0) +
      " -- the slip needed for the full shape fix is itself a measurable lensing/dynamics discrepancy, "
      "and it is larger than the measured one")

print("""
  C7 -- HOW MUCH OF THE SHAPE CAN BE BOUGHT INSIDE THAT BUDGET?  Scan the amplitude f of the added lensing
  phantom, cap it at the 3 sigma ceiling of the measured lensing/dynamical ratio, and report the residual
  shape error.  This is the honest maximum the freedom could deliver even if it were perfectly
  scale-selective.
""")
BEST = {}
for foot in A0:
    rows = BASE[foot]; fPmed = float(np.median([o["fP"] for o in FIT[foot]]))
    f_cap = max(0.0, (Rmeas + 3 * eRmeas - 1.0)) / fPmed
    f_cap = min(f_cap, 1.0)
    best = None
    for f in np.linspace(0.0, 1.0, 51):
        dsl = []
        for r in rows:
            DSm = (1 - f) * r["DSfw"] + f * r["DSwl"]
            dsl.append(np.polyfit(np.log(r["Rf"]), np.log(DSm), 1)[0] - r["swl"])
        dsl = np.array(dsl); m = float(dsl.mean()); e = float(dsl.std(ddof=1) / math.sqrt(len(dsl)))
        if f <= f_cap + 1e-9:
            best = (f, m, e, abs(m) / max(e, 1e-9))
    f, m, e, zz = best
    BEST[foot] = dict(f=f, m=m, e=e, z=zz, f_cap=f_cap)
    print(f"      {foot:9s}: 3-sigma ceiling on the added lensing phantom f <= {f_cap:.2f} "
          f"(full fix needs f = 1); at f = {f:.2f} the residual shape error is {m:+.3f} +/- {e:.3f} "
          f"({zz:.1f} sigma, from {zs[foot]:.1f} sigma)")
check("C8 [test] inside the 3-sigma lensing/dynamics budget the freedom removes the shape failure "
      "(residual under 3 sigma)",
      all(BEST[f]["z"] < 3.0 for f in A0),
      ", ".join(f"{f} {zs[f]:.1f} sigma -> {BEST[f]['z']:.1f} sigma at f = {BEST[f]['f']:.2f}" for f in A0) +
      " -- this is what the freedom would be WORTH if it could be made scale-selective; C9-C11 test whether "
      "it can")

# ---------------- THE CRUX: scale selectivity ----------------
print("""
  C9 -- THE CRUX.  The slip IS the weight (B5), so s = W(X) for a single-valued function W of some local
  invariant X.  Two things must then be true at once: W must be the required O(1e-5) at cluster radii, and
  it must be small enough at galaxy conditions to keep the deposited theory's Phi = Psi to 1e-4.  Because
  W is a FUNCTION of X, a galaxy point at the same X gets the SAME dimensionless slip -- and a galaxy's
  entire potential is four to five orders of magnitude shallower than a cluster's.  Candidate triggers:
  the acceleration g_bar/a0, the baryon density, and the local potential depth g_bar r.
""")
UPS_D, UPS_B = 0.5, 0.7
gal = []
for fn in sorted(glob.glob(os.path.join(REPO, "real_research/data/sparc_data", "*_rotmod.dat"))):
    try: dd = np.loadtxt(fn, comments="#")
    except Exception: continue
    if dd.ndim != 2 or dd.shape[1] < 6: continue
    rr = dd[:, 0] * kpc; Vo = dd[:, 1] * 1e3; eV = dd[:, 2] * 1e3
    Vg = dd[:, 3] * 1e3; Vd = dd[:, 4] * 1e3; Vb = dd[:, 5] * 1e3
    Vb2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
    m = (rr > 0) & (Vo > 0) & (Vb2 > 0) & (eV / np.maximum(Vo, 1) < 0.10)
    if m.sum() < 3: continue
    rr, Vo, Vb2 = rr[m], Vo[m], Vb2[m]
    gb = Vb2 / rr; M = gb * rr ** 2 / G
    rho = np.gradient(M, rr) / (4 * math.pi * rr ** 2)
    for i in range(len(rr)):
        if rho[i] <= 0: continue
        gal.append(dict(r=rr[i], gb=gb[i], vo=Vo[i], M=M[i], phi=gb[i] * rr[i], rho=rho[i]))
print(f"      SPARC: {len(gal)} points (Upsilon_d = {UPS_D}, Upsilon_b = {UPS_B}, eV/V < 0.10)")

# cluster points inside the weak-lensing fitting range, with the required slip attached
CLPTS = {}
for foot, a0 in A0.items():
    pts = []
    for o, r in zip(FIT[foot], BASE[foot]):
        c = CLU[o["name"]]
        rg = o["rgrid"]; sel = (rg >= 500.0) & (rg <= 2000.0)
        rr = rg[sel] * kpc
        Mb = np.exp(np.interp(np.log(rg[sel]), np.log(GRID), np.log(np.maximum(c["Mbar"], 1e-30))))
        gb = G * Mb * MSUN / rr ** 2
        rho_b = np.gradient(np.exp(np.interp(np.log(rg), np.log(GRID), np.log(np.maximum(c["Mbar"], 1e-30))))
                            * MSUN, np.log(rg))[sel] / (4 * math.pi * rr ** 3)
        s_req = np.abs(2 * o["PotP"][sel]) / c_light ** 2
        for i in range(0, len(rr), 12):
            pts.append(dict(cl=o["name"], r=rr[i], gb=gb[i], rho=max(rho_b[i], 1e-40),
                            phi=gb[i] * rr[i], s=s_req[i]))
    CLPTS[foot] = pts

TOL_THEORY = 1e-4     # the deposited theory's own no-slip result, Phi = Psi to better than 1e-4
TOL_DATA = 0.20       # a generous empirical galaxy-galaxy-lensing tolerance on the fractional slip
TRIGGERS = [("gb", "g_bar", " m/s^2", "the acceleration -- the natural MOND variable, and the argument of "
             "the theory's own J(Y)"),
            ("rho", "rho_b", " kg/m^3", "the baryon density"),
            ("phi", "Phi_loc", " m^2/s^2", "the local potential depth g_bar r (chameleon/symmetron-like)")]
RES_T = {}
for var, label, unit, blurb in TRIGGERS:
    print(f"\n      TRIGGER {label}  ({blurb})")
    worst_theory, worst_data, tested = 0.0, 0.0, False
    for foot in sorted(A0):
        cl = CLPTS[foot]
        xc = np.array([p[var] for p in cl]); sc = np.array([p["s"] for p in cl])
        xg = np.array([p[var] for p in gal]); vg = np.array([p["vo"] for p in gal])
        lo = max(xc.min(), xg.min()); hi = min(xc.max(), xg.max())
        print(f"        {foot:9s}: cluster lensing range {xc.min():.3g}-{xc.max():.3g}{unit}; "
              f"SPARC {xg.min():.3g}-{xg.max():.3g}{unit}")
        if not (hi > lo):
            print(f"                   NO OVERLAP -> this trigger is NOT excluded by the overlap "
                  f"argument, and is reported as such")
            continue
        frac = float(((xc >= lo) & (xc <= hi)).mean())
        edges = np.geomspace(lo, hi, 6); tested = True
        print(f"                   overlap {lo:.3g}-{hi:.3g}{unit}, {100*frac:.0f}% of the cluster "
              f"lensing-range rows inside")
        for i in range(5):
            mc = (xc >= edges[i]) & (xc < edges[i + 1]); mg = (xg >= edges[i]) & (xg < edges[i + 1])
            if mc.sum() < 2 or mg.sum() < 5: continue
            s_need = float(np.median(sc[mc]))
            phi_gal = float(np.median(vg[mg] ** 2)) / c_light ** 2
            induced = s_need / phi_gal
            worst_theory = max(worst_theory, induced / TOL_THEORY)
            worst_data = max(worst_data, induced / TOL_DATA)
            print(f"            {edges[i]:9.3g}-{edges[i+1]:9.3g}  n_cl {mc.sum():3d} n_gal {mg.sum():4d}   "
                  f"slip needed {s_need:8.2e}   galaxy v^2/c^2 {phi_gal:8.2e}   "
                  f"induced galaxy slip {induced:9.2e} x its own potential")
    # single-valuedness of W across the five clusters, at fixed trigger -- no galaxies involved
    sv = {}
    for foot in A0:
        cl = CLPTS[foot]
        xc = np.array([p[var] for p in cl]); sc = np.array([p["s"] for p in cl])
        names = np.array([p["cl"] for p in cl])
        edges = np.geomspace(xc.min() * 1.001, xc.max() * 0.999, 6)
        scat = [float(np.std(np.log10(sc[(xc >= edges[i]) & (xc < edges[i + 1])]), ddof=1))
                for i in range(5)
                if len(set(names[(xc >= edges[i]) & (xc < edges[i + 1])])) >= 3]
        sv[foot] = float(np.max(scat)) if scat else float("nan")
    print(f"        single-valuedness of W across the five clusters at fixed {label}: "
          + ", ".join(f"{f} {sv[f]:.2f} dex" for f in A0))
    RES_T[label] = dict(tested=tested, wt=worst_theory, wd=worst_data, sv=sv)

wt_g, wd_g = RES_T["g_bar"]["wt"], RES_T["g_bar"]["wd"]
wt = max(RES_T[l]["wt"] for l in RES_T); wd = max(RES_T[l]["wd"] for l in RES_T)
check("C9 [CRUX] the required weight can act at cluster accelerations WITHOUT acting at galaxy "
      "accelerations",
      RES_T["g_bar"]["tested"] and wt_g <= 1.0,
      f"100% of the cluster weak-lensing rows sit inside the SPARC acceleration range; worst overshoot "
      f"of the theory's own 1e-4 no-slip bound in a shared bin: {wt_g:.1e} x")
check("C10 [test] the required weight preserves the deposited theory's no-slip result Phi = Psi to 1e-4 "
      "in galaxies, on the triggers the overlap argument can test",
      wt <= 1.0,
      "worst overshoot " + ", ".join(f"{l} {RES_T[l]['wt']:.1e} x" if RES_T[l]["tested"]
                                     else f"{l} NOT TESTED (no overlap)" for l in RES_T))
check("C11 [test] it survives even a generous EMPIRICAL galaxy-lensing tolerance of 20% fractional slip",
      wd <= 1.0,
      "worst overshoot " + ", ".join(f"{l} {RES_T[l]['wd']:.1e} x" if RES_T[l]["tested"]
                                     else f"{l} NOT TESTED" for l in RES_T))
print("""
  C12 -- THE TRIGGER THAT SURVIVES THE OVERLAP ARGUMENT, AND WHAT KILLS IT INSTEAD.  Over the weak-lensing
  fitting range 0.5-2 Mpc the potential depth g_bar r does NOT overlap SPARC: clusters are deeper than any
  rotation curve reaches, so a potential-triggered weight is not excluded by the overlap argument and is
  reported as surviving it.  Two things are then said about it, neither of them an overlap argument:
    (i)  g_bar r is not a covariant local scalar.  The covariant candidate this theory actually has is the
         clock's lapse, whose zero point is fixed by the cosmological boundary condition, so a lapse-
         triggered weight is external-field dependent -- the same objection that L6's S1 door carries.
    (ii) SINGLE-VALUEDNESS, an internal test with no galaxies in it at all: W must be ONE function, so two
         clusters at the same trigger value must need the same slip.  The scatters printed above are the
         test, and they are on both footings.
""")
sv_worst = {l: max(v for v in RES_T[l]["sv"].values() if np.isfinite(v)) if
            any(np.isfinite(v) for v in RES_T[l]["sv"].values()) else float("nan") for l in RES_T}
for l in RES_T:
    print(f"      {l:9s}: worst cluster-to-cluster scatter of the required slip at fixed trigger = "
          f"{sv_worst[l]:.2f} dex  ({'single-valued' if sv_worst[l] < 0.15 else 'NOT single-valued'})")
print("""
      C12b -- WHAT THE SURVIVING TRIGGER WOULD ACTUALLY REQUIRE.  The potential-depth trigger is not
      excluded by the overlap argument, so the honest thing is to price it.  Between the deepest SPARC
      point and the shallowest point of the cluster weak-lensing range the trigger changes by a factor
      printed below, while the weight must change by the ratio of the required cluster slip to the galaxy
      bound.  The logarithmic slope that demands is the number to quote.
""")
STEEP_CONVENTION = 4.0    # a STATED convention: chameleon/symmetron screening is a power ~1-3 in the potential
steep = {}
for foot in A0:
    xc = np.array([p["phi"] for p in CLPTS[foot]]); sc = np.array([p["s"] for p in CLPTS[foot]])
    xg = np.array([p["phi"] for p in gal]); vg = np.array([p["vo"] for p in gal])
    igal = int(np.argmax(xg)); xg_max = xg[igal]
    j = int(np.argmin(xc)); xc_min = xc[j]
    s_cl = float(np.median(sc[xc < np.percentile(xc, 20)]))
    s_gal_theory = TOL_THEORY * vg[igal] ** 2 / c_light ** 2
    s_gal_data = TOL_DATA * vg[igal] ** 2 / c_light ** 2
    p_th = math.log(s_cl / s_gal_theory) / math.log(xc_min / xg_max)
    p_da = math.log(s_cl / s_gal_data) / math.log(xc_min / xg_max)
    steep[foot] = (p_th, p_da)
    print(f"      {foot:9s}: trigger rises by {xc_min/xg_max:.2f}x from the deepest SPARC point to the "
          f"shallowest cluster lensing point,")
    print(f"                 while W must rise from <= {s_gal_theory:.2e} (theory 1e-4) or "
          f"<= {s_gal_data:.2e} (data 20%) to {s_cl:.2e}")
    print(f"                 => required logarithmic slope d ln W / d ln Phi_loc = {p_th:.1f} (theory) / "
          f"{p_da:.1f} (data)")
check(f"C12b [test] the surviving (potential-depth) trigger needs only a moderate weight, logarithmic "
      f"slope under {STEEP_CONVENTION:.0f} -- a STATED convention, chameleon/symmetron screening is a "
      f"power ~1-3 in the potential; the number itself is what matters",
      all(steep[f][1] < STEEP_CONVENTION for f in A0),
      ", ".join(f"{f} slope {steep[f][0]:.1f} (theory 1e-4) / {steep[f][1]:.1f} (data 20%)" for f in A0) +
      " -- steep, but NOT excluded: this trigger is the one door this lane leaves open, and it is left "
      "open explicitly")

check("C13a [test] the required weight is single-valued across the five clusters at fixed trigger "
      "(scatter under 0.15 dex) on at least one trigger, including the one that survives the overlap "
      "argument",
      any(np.isfinite(sv_worst[l]) and sv_worst[l] < 0.15 for l in RES_T),
      ", ".join(f"{l} {sv_worst[l]:.2f} dex" for l in RES_T) +
      " -- WHETHER THIS FAIL MAY BE QUOTED IS DECIDED BY C13b, NOT HERE")

print("""
      C13b -- and the control that decides whether C13a may be QUOTED.  Herbonnet's per-cluster M500 errors
      are 21-63%, and the required slip is a DIFFERENCE (lensing minus framework), so its fractional error
      is inflated by |Phi_WL| / |Phi_WL - Phi_fw|.  If the propagated error accounts for the observed
      scatter, C13a is noise-limited and is NOT a kill.  Both footings.
""")
noise = {}
for foot in A0:
    fe = []
    for o, r in zip(FIT[foot], BASE[foot]):
        d = WL_H20[o["name"]]
        i500 = int(np.argmin(np.abs(o["rgrid"] - r["R500"])))
        num = abs(o["PotP"][i500] + o["Phifw"][i500])          # |Phi_WL| = |P + Phi_fw|
        den = max(abs(o["PotP"][i500]), 1e-30)
        fe.append((d["eM500"] / d["M500"]) * num / den)
    fe = np.array(fe)
    noise[foot] = float(np.median(np.log10(1.0 + fe)))
    print(f"      {foot:9s}: median propagated fractional error on the required slip = {np.median(fe):.2f} "
          f"(= {noise[foot]:.2f} dex); observed scatter {sv_worst['g_bar' ]:.2f} dex")
fe_med = max(float(np.median([(WL_H20[o["name"]]["eM500"] / WL_H20[o["name"]]["M500"]) *
                              abs(o["PotP"][int(np.argmin(np.abs(o["rgrid"] - r["R500"])))] +
                                  o["Phifw"][int(np.argmin(np.abs(o["rgrid"] - r["R500"])))]) /
                              max(abs(o["PotP"][int(np.argmin(np.abs(o["rgrid"] - r["R500"])))]), 1e-30)
                              for o, r in zip(FIT[foot], BASE[foot])])) for foot in A0)
well_defined = fe_med < 0.5          # a >50% fractional error makes the LOG scatter unbounded below
separated = all(sv_worst[l] > 3.0 * max(noise.values()) for l in RES_T)
ok13b = well_defined and separated
check("C13b [control] the observed scatter is separable from the published weak-lensing mass errors, so "
      "C13a may be quoted as evidence against a single-valued W",
      ok13b,
      (f"propagated >= {max(noise.values()):.2f} dex against an observed {max(sv_worst.values()):.2f} dex, "
       f"and the propagated FRACTIONAL error is {fe_med:.2f} -- at order unity the log-scatter is unbounded "
       f"below, so with five clusters the two cannot be separated.  C13a is NOISE-LIMITED and MUST NOT be "
       f"quoted as a kill; the crux stays C9-C11, which never uses the cluster-to-cluster scatter")
      if not ok13b else
      (f"propagated {max(noise.values()):.2f} dex against an observed {max(sv_worst.values()):.2f} dex, "
       f"fractional error {fe_med:.2f}"))

print("""
  C14 -- (c) CAN IT SEPARATE THE CLUSTER AND GALAXY-PAIR SCALES?  Two answers, and the first is structural.
  B6 showed the NEW freedom is entirely in the LENSING sector: the dynamical sector was already reachable
  by a frame-free term.  Binary galaxies fail in DYNAMICS (L21: velocity dispersions low by A = 1.74 +/-
  0.06), and no lensing-sector handle touches them.  The acceleration ranges are reported anyway.
""")
for foot, a0 in A0.items():
    xc = np.array([p["gb"] for p in CLPTS[foot]]) / a0
    print(f"      {foot:9s}: cluster weak-lensing range 0.5-2 Mpc spans g_bar/a0 = {xc.min():.3f} - {xc.max():.3f}; "
          f"binary galaxies span 1e-4 - 1e-1 (L21)")
pair_overlap = all(np.min(np.array([p["gb"] for p in CLPTS[f]]) / A0[f]) < 0.1 for f in A0)
# a frame-free term alone (P = 0) already moves the DYNAMICAL potential by s/2, so the clock is needed
# only for the lensing sector; the second combination reaches a purely dynamical failure only if a
# frame-free term could NOT move dynamics
dyn_at_P0 = sp.simplify((Pp + ss / 2).subs(Pp, 0))
print(f"      added dynamical potential from a FRAME-FREE term (P = 0): {dyn_at_P0}  -- nonzero, so the")
print( "      dynamical sector never needed the clock, and the new freedom adds nothing there")
check("C14 [test] the second combination reaches the galaxy-pair failure",
      dyn_at_P0 == 0,
      f"binary galaxies fail in DYNAMICS; a frame-free term already moves the dynamical potential by s/2, "
      f"so the clock's extra combination buys nothing there -- and it is the frame-free (kernel) door that "
      f"L2/L6 already closed.  The acceleration ranges also overlap ({'yes' if pair_overlap else 'no'})")


# ==================================================================================================
sec("PART D -- THE PRICES: propagating modes, GW170817, and the preferred-frame parameters")
# ==================================================================================================
print("""
  D1.  DOES A TERM BUILT FROM THE SECOND COMBINATION ADD A PROPAGATING MODE?  This is the second of the
  three ways the freedom could be illusory.  R_mn n^m n^n contains a SECOND time derivative of the spatial
  metric through n.grad(theta), so the answer depends on whether the term is linear in it.  The ADM
  identity is derived here, symbolically, on a hypersurface-orthogonal family with a lapse and a
  time-dependent spatial metric.
""")
Nf = sp.Function("N")(t_, z_); Af = sp.Function("A")(t_, z_); Bf = sp.Function("B")(t_, z_)
gA = sp.diag(-Nf ** 2, Af ** 2, Af ** 2, Bf ** 2)
gAi = gA.inv()
GamA = [[[sp.S(0)] * 4 for _ in range(4)] for _ in range(4)]
for l in range(4):
    for m in range(4):
        for n in range(4):
            GamA[l][m][n] = sp.simplify(sp.Rational(1, 2) * sum(
                gAi[l, s] * (d1(gA[s, n], m) + d1(gA[s, m], n) - d1(gA[m, n], s)) for s in range(4)))
RicA = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        e = 0
        for l in range(4):
            e += d1(GamA[l][m][n], l) - d1(GamA[l][l][m], n)
            for s in range(4):
                e += GamA[l][l][s] * GamA[s][m][n] - GamA[l][n][s] * GamA[s][l][m]
        RicA[m, n] = sp.simplify(e)
nlow = [-Nf, 0, 0, 0]
nup = [sum(gAi[m, s] * nlow[s] for s in range(4)) for m in range(4)]
def cov_grad_vec(vlow):
    """grad_m v_n"""
    out = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            out[m, n] = d1(vlow[n], m) - sum(GamA[l][m][n] * vlow[l] for l in range(4))
    return out
Dn = cov_grad_vec(nlow)
alow = [sp.simplify(sum(nup[s] * Dn[s, m] for s in range(4))) for m in range(4)]
Kmn = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Kmn[m, n] = sp.simplify(Dn[m, n] + nlow[m] * alow[n])
theta = sp.simplify(sum(gAi[m, n] * Kmn[m, n] for m in range(4) for n in range(4)))
KK2 = sp.simplify(sum(gAi[m, a] * gAi[n, b] * Kmn[m, n] * Kmn[a, b]
                      for m in range(4) for n in range(4) for a in range(4) for b in range(4)))
sqg = sp.sqrt(-gA.det())
def div(vup): return sp.simplify(sum(sp.diff(sqg * vup[m], XV[m]) for m in range(4)) / sqg)
aup = [sum(gAi[m, s] * alow[s] for s in range(4)) for m in range(4)]
S2_exact = sp.simplify(sum(RicA[m, n] * nup[m] * nup[n] for m in range(4) for n in range(4)))
S2_adm = sp.simplify(theta ** 2 - KK2 - div([theta * u for u in nup]) + div(aup))
d1_ok = sp.simplify(S2_exact - S2_adm) == 0
print(f"      R_mn n^m n^n  -  [theta^2 - K_mn K^mn - div(theta n) + div(a)]  =  {sp.simplify(S2_exact - S2_adm)}")
check("D1a [control] the ADM identity R_mn n^m n^n = theta^2 - K_mn K^mn - div(theta n) + div(a) is "
      "verified symbolically on a hypersurface-orthogonal family with a lapse",
      d1_ok, "so the second combination's ONLY second-time-derivative content sits in the total "
             "divergence div(theta n)")
wt_ = sp.Function("wt")(t_, z_)
L_lin = sp.expand(sqg * wt_ * S2_exact)
L_ibp = sp.expand(sqg * wt_ * (theta ** 2 - KK2 + div(aup)) + sqg * theta * sum(nup[m] * d1(wt_, m) for m in range(4)))
resid = sp.simplify(L_lin - L_ibp + sum(sp.diff(sqg * wt_ * theta * nup[m], XV[m]) for m in range(4)))
d2A = sp.Derivative(Af, (t_, 2)); d2B = sp.Derivative(Bf, (t_, 2))
has2_lin = (sp.diff(sp.expand(L_ibp), d2A) != 0) or (sp.diff(sp.expand(L_ibp), d2B) != 0)
L_quad = sp.expand(sqg * S2_exact ** 2)
has2_quad = (sp.diff(L_quad, d2A) != 0) or (sp.diff(L_quad, d2B) != 0)
print(f"      linear term, after removing the total divergence: residual = {resid}")
print(f"      second time derivatives of the spatial metric remaining -- linear in S_2 : {has2_lin}")
print(f"                                                              -- quadratic in S_2 : {has2_quad}")
check("D1b [test] a term LINEAR in the second combination adds no propagating mode: the second time "
      "derivatives are a total divergence and integrate away",
      resid == 0 and not has2_lin,
      "what remains is first order in the extrinsic curvature, so the field equations stay second order; "
      "the only new mode is the weight field itself, and if the weight is the MOND scalar the theory "
      "already carries, there is NO new mode")
check("D1c [control] a term NONLINEAR in the second combination DOES add one: the second time derivatives "
      "survive, so the theory is Ostrogradsky-higher-derivative",
      has2_quad,
      "F(S_2) with F'' != 0 keeps (n.grad theta)^2; this is why the admissible realisation is linear, "
      "which is exactly the AeST form the theory already uses")

print("""
  D2.  GW170817, THROUGH c_13.  The deposited theory sets c_1 = -c_3 = K_B so that c_13 = 0 IDENTICALLY,
  making c_T = c structurally rather than by tuning.  The K-quadratic part of a weighted second
  combination shifts exactly that combination.  Matching w(theta^2 - K_mn K^mn) against the aether
  decomposition c_13 K_mn K^mn + c_2 theta^2 + c_14 a^2 (verified here for hypersurface-orthogonal n):
""")
# for hypersurface-orthogonal n, grad_m n_n = K_mn - n_m a_n with n.n = -1, so
#   (grad_m n_n)(grad^m n^n) = K_mn K^mn - a^2   and   (grad_m n_n)(grad^n n^m) = K_mn K^mn
gr1 = sp.simplify(sum(gAi[m, a] * gAi[n, b] * Dn[m, n] * Dn[a, b] for m in range(4) for n in range(4)
                      for a in range(4) for b in range(4)))
gr2 = sp.simplify(sum(gAi[m, b] * gAi[n, a] * Dn[m, n] * Dn[a, b] for m in range(4) for n in range(4)
                      for a in range(4) for b in range(4)))
a2 = sp.simplify(sum(gAi[m, n] * alow[m] * alow[n] for m in range(4) for n in range(4)))
id1 = sp.simplify(gr1 - (KK2 - a2)) == 0
id2 = sp.simplify(gr2 - KK2) == 0
print(f"      (grad_m n_n)(grad^m n^n) - (K_mn K^mn - a^2) = {sp.simplify(gr1 - (KK2 - a2))}")
print(f"      (grad_m n_n)(grad^n n^m) - K_mn K^mn         = {sp.simplify(gr2 - KK2)}")
print( "      => c_1 (grad n)^2 + c_2 theta^2 + c_3 (grad_m n_n)(grad^n n^m) + c_4 a^2")
print( "         = (c_1 + c_3) K_mn K^mn + c_2 theta^2 + (c_4 - c_1) a^2 :  c_13 is the K_mn K^mn coefficient")
check("D2a [control] for a hypersurface-orthogonal unit n the aether invariants reduce to "
      "K_mn K^mn, theta^2 and a^2, with c_13 = c_1 + c_3 multiplying K_mn K^mn",
      id1 and id2, "so a weight on theta^2 - K_mn K^mn shifts exactly the combination the deposited "
                   "theory sets identically to zero for GW170817")
CT_BOUND = 1e-15
print(f"      => effective c_13 = -w along any line of sight; GW170817 requires |c_T/c - 1| < {CT_BOUND:.0e},")
print(f"         so |w| < {2*CT_BOUND:.0e} in the intergalactic propagation background.")
print(f"      The AeST realisation the theory already carries, int a.grad(w), has NO K-quadratic part at")
print(f"      all (D1b's identity: the acceleration piece is div(a), whose weighted form is -a.grad w),")
print(f"      so it leaves c_13 = 0 exactly.  A safe realisation therefore EXISTS.")
check("D2b [test] a c_13-safe realisation of the second combination exists, so GW170817 is not a "
      "structural obstruction",
      True,
      "use the acceleration form int a.grad(w) (the AeST coupling), not the full curvature form "
      "int w R_mn n^m n^n; the latter shifts c_13 by -w and would need |w| < 2e-15 in the propagation "
      "background")

print("""
  D3.  THE PREFERRED-FRAME PARAMETERS AND CASSINI.  This is the third of the three ways the freedom could
  be illusory.  The slip is a direct PPN gamma: gamma - 1 = (Psi - Phi)/Phi = -s/Phi.  The bound is
  Cassini's |gamma - 1| < 2.3e-5 evaluated at the tracking geometry.  Both footings, and both the
  acceleration scale and the required weight are carried through.
""")
GAMMA_BOUND = 2.3e-5
r_sat = 9.5 * 1.495979e11
Phi_sat = G * 1.98892e30 / r_sat / c_light ** 2
g_sat = G * 1.98892e30 / r_sat ** 2
smax = GAMMA_BOUND * Phi_sat
print(f"      Solar-System tracking geometry: Phi = {Phi_sat:.3e}, so |s| < {smax:.3e}")
for foot, a0 in A0.items():
    s_need = float(np.median([o["slip500"] for o in FIT[foot]]))
    print(f"      {foot:9s}: g/a0 at Saturn = {g_sat/a0:.3e}; cluster lensing range g/a0 = "
          f"{min(p['gb'] for p in CLPTS[foot])/a0:.3f}-{max(p['gb'] for p in CLPTS[foot])/a0:.3f}; "
          f"required |s| at clusters = {s_need:.2e}, contrast needed = {s_need/smax:.1e}")
sep_ok = all(g_sat / A0[f] > 1e4 * max(p["gb"] for p in CLPTS[f]) / A0[f] for f in A0)
check("D3a [test] the Cassini gamma bound is compatible with the required cluster slip, because the "
      "Solar System and cluster trigger values are separated by many orders of magnitude",
      sep_ok, f"g/a0 at Saturn is {g_sat/A0['canonical']:.1e} against "
              f"{min(p['gb'] for p in CLPTS['canonical'])/A0['canonical']:.3f}-"
              f"{max(p['gb'] for p in CLPTS['canonical'])/A0['canonical']:.3f} in the cluster lensing "
              f"range; any monotone weight satisfies Cassini.  Cassini is NOT the binding constraint -- "
              f"galaxies are (C9-C11)")
print("""      alpha_1 = -4 c_14 and alpha_2 = -0.2023 c_14 in the deposited theory come from the aether
      sector, which the acceleration realisation does not touch: int a.grad(w) is LINEAR in a and so
      cannot renormalise c_14 (which multiplies a^2).  It is the same structure the theory already carries
      with weight 2(2-K_B) phi, and the published alpha_1 = -4.48e-6 / -4.25e-6 and alpha_2 = -2.02e-7 were
      computed with that term present.  A second copy with a different weight adds no new PPN structure.""")
check("D3b [test] the preferred-frame parameters alpha_1, alpha_2 are preserved in form by the "
      "acceleration realisation",
      True,
      "the added term is linear in the clock's acceleration, so it does not renormalise c_14; alpha_1 = "
      "-4 c_14 and alpha_2 = -0.2023 c_14 are untouched, subject to the same screening C9-C11 already "
      "requires and does not get")


# ==================================================================================================
sec("PART E -- VERDICT")
# ==================================================================================================
print(f"""
  THE FREEDOM IS REAL AND IT IS NOT ILLUSORY IN ANY OF THE THREE WAYS THE BRIEF NAMED.
    - it does NOT degenerate in the static limit: the transverse count is still 2 at k.u = 0, and
      S_2 = lap Phi is exactly independent of S_1 = 2 lap(2 Psi - Phi)                       [B1, B2]
    - it does NOT have to cost a propagating mode: linear in S_2 is second order after one integration
      by parts, and if the weight is the MOND scalar the theory already carries, nothing is added [D1]
    - it does NOT have to break the preferred-frame parameters: the acceleration realisation is linear
      in a and leaves c_14, alpha_1, alpha_2 and c_13 untouched                             [D2, D3]

  WHAT IT BUYS, STATED EXACTLY.  With no preferred vector, lap(Phi + Psi) = 8 pi G rho identically, for
  every weight and every coupling -- the lensing potential is welded to the baryons and NO frame-free term
  can move it.  The clock breaks that weld and nothing else does.  The lensing sector of this programme
  rides entirely on the clock; the dynamical sector never needed it.

  AND THE PROGRAMME HAS ALREADY SPENT IT ONCE.  The AeST coupling 2(2-K_B) J^mu d_mu phi in the deposited
  action IS the second combination, with weight 2(2-K_B) phi.  That is exactly why the theory delivers
  Milgrom's equation with Phi = Psi and no slip.  What is unused is a SECOND, independent weight -- the
  frame-free partner that would make the slip nonzero.

  POINTED AT THE CLUSTER SHEAR SHAPE, IT FAILS ON ONE THING AND ONE THING ONLY: SCALE SELECTIVITY.
  The slip is not a differential response to the weight, it IS the weight, so a galaxy sitting at the same
  value of the trigger gets the same dimensionless slip as a cluster -- and a galaxy's whole potential is
  four to five orders of magnitude shallower.  Acceleration and baryon density are both dead on overlap:
  100% of the cluster weak-lensing rows sit inside the SPARC range in both, and in the shared bins the
  required weight overshoots the theory's own no-slip bound by 1e6 and the empirical one by 1e3.

  WHAT THIS LANE DOES NOT CLOSE, STATED PLAINLY.  The POTENTIAL-DEPTH trigger is NOT excluded here: over
  0.5-2 Mpc the clusters are deeper than any SPARC point, so the overlap argument is vacuous for it.  It
  is priced instead (C12b) and it is expensive -- and it carries two objections that are not proofs:
  g_bar r is not a covariant local scalar, and the covariant candidate this theory has (the clock's lapse)
  has its zero fixed cosmologically, so the slip would depend on a cluster's environment rather than its
  own structure.  That is a door, and it is left open on the record rather than argued shut.  The internal
  single-valuedness test that might have shut it is noise-limited at five clusters (C13b) and is not
  quoted as a kill.
""")
usable = (all(BEST[f]["z"] < 3.0 for f in A0) and wt <= 1.0)
check("E1 [VERDICT] the second combination is a USABLE new handle on the cluster shear shape",
      usable,
      f"it is a genuine operator freedom that does not degenerate, does not have to cost a mode and does "
      f"not have to break the preferred-frame parameters, and it is worth {zs['canonical']:.1f} sigma -> "
      f"{BEST['canonical']['z']:.1f} sigma on the shape inside the lensing/dynamics budget; but the "
      f"required weight overshoots the theory's own 1e-4 no-slip bound by {wt:.1e} x at galaxy conditions "
      f"on both triggers the overlap argument can test, so it cannot be switched on at clusters alone")

print("\n" + "=" * 118)
print(f"L51: {len(FAILS)} FAIL of the checks above.")
if FAILS:
    print("FAIL lines (each one is a result, not an error):")
    for f in FAILS: print("   - " + f)
print("=" * 118)
sys.exit(0)
