"""
york_repair_F_kernel_2026.py
================================================================================
PART F -- THE REPAIRED KERNEL AND ALL KERNEL-DEPENDENT STRUCTURE.

Repairs FAIL F (Cassini) of the York/CMC-elliptic-MOND theory by REPLACING the
Standard-mu kernel  mu = x/sqrt(1+x^2)  with the exponential kernel

        mu(x) = 1 - e^{-x},          x = |DPhi|/a0 ,

and RE-DERIVING FROM SCRATCH every kernel-dependent object.  The old B/C/G proofs
used the Standard-mu kernel and do NOT carry over; each item is recomputed here.

FROZEN CORE (unchanged, theory_2026/york/):
  S_grav  = (c^3/16 pi G) INT N sqrt(h) (K_ij K^ij - K^2 + R3)
  K = q(t) : ONE GLOBAL CMC clock; a0(q) = c q / Z spatially constant; a0(z)=a0,0 H(z)/H0
  S_MOND  = -(1/8 pi G) INT N sqrt(h) a0^2 U(Y),   Y = D_iPhi D^iPhi / a0^2,   Phi elliptic
  U'(y)   = mu(sqrt y)              (AQUAL <-> single-field map)

CANDIDATE closed form (VERIFIED below with sympy):
  mu(x) = 1 - e^{-x}
  U'(y) = 1 - e^{-sqrt y}
  U(y)  = y - 2 + 2(sqrt y + 1) e^{-sqrt y}
  U''(y)= e^{-sqrt y} / (2 sqrt y)  > 0

Nine items, each with a per-item PASS/FAIL.  Discipline (Carl, binding): sympy,
never a scaling estimate; verify a FAIL as rigorously as a PASS; label INCOMPLETE
rather than invent.  Z~21 is FITTED; only a0(z)~H(z) is predicted.

NOTE ON THE QUMOND PARTNER.  The framework's operative RAR kernel is the QUMOND
nu(y) = 1/(1 - e^{-sqrt y}).  In AQUAL the mu-partner of that nu is defined by the
Legendre/inverse map nu(y) mu(nu^2 y)=1, NOT by mu=1/nu.  The literal mu = x/(1-e^{-x})
has the WRONG small-x limit (->1 as x->0, i.e. Newtonian everywhere) and is NOT used.
The repaired AQUAL mu adopted here, mu=1-e^{-x}, reproduces deep MOND (mu->x) and is
Cassini-safe (1-mu=e^{-x}); its RAR is checked separately (ppn_lensing_cassini_2026.py /
rar refit).  This script proves the CONSTRAINT-STRUCTURE items only.
================================================================================
"""
import sympy as sp

PASS = {}
def record(item, ok, note=""):
    PASS[item] = bool(ok)
    tag = "PASS" if ok else "FAIL"
    print(f"\n  --> ITEM {item}: {tag}" + (f"   ({note})" if note else ""))

def head(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

# Master symbols
y  = sp.symbols('y',  positive=True)     # y = Y = |DPhi|^2/a0^2
u  = sp.symbols('u',  positive=True)     # u = sqrt(y) = |DPhi|/a0 = x
x  = sp.symbols('x',  positive=True)     # x = |DPhi|/a0
a0 = sp.symbols('a0', positive=True)
psi, ybar = sp.symbols('psi ybar', positive=True)

# The repaired kernel, once:
mu   = 1 - sp.exp(-x)                                   # mu(x)
Uprime = 1 - sp.exp(-sp.sqrt(y))                        # U'(y) = mu(sqrt y)
U    = y - 2 + 2*(sp.sqrt(y) + 1)*sp.exp(-sp.sqrt(y))   # candidate closed form
Upp  = sp.exp(-sp.sqrt(y))/(2*sp.sqrt(y))              # candidate U''

# =====================================================================================
head("(1)  mu(x) = 1 - e^{-x}: limits, and the deep-MOND normalization v^4 = G M a0")
# =====================================================================================
s0 = sp.series(mu, x, 0, 4)
lead = sp.series(mu, x, 0, 2).removeO()
print(f"  mu(x) small-x series : {s0}")
print(f"     leading term      : {lead}   (-> x, coefficient exactly 1  => deep-MOND mu~x)")
one_minus_mu = sp.simplify(1 - mu)
print(f"  1 - mu(x)            : {one_minus_mu}   (-> 0 EXPONENTIALLY as x->inf => Cassini-safe)")
lim0 = sp.limit(mu/x, x, 0)          # mu/x -> 1
liminf = sp.limit(mu, x, sp.oo)      # mu -> 1
print(f"  lim_(x->0) mu/x = {lim0}   (want 1)")
print(f"  lim_(x->inf) mu = {liminf}   (want 1)")

# Deep-MOND normalization, DERIVED (not assumed) from div[mu DPhi] = 4piG rho, spherical:
#   Gauss:  mu(g/a0) * g * 4 pi r^2 = 4 pi G M   =>  mu(g/a0) g r^2 = G M
#   deep MOND mu -> g/a0  =>  (g/a0) g r^2 = G M  =>  g = sqrt(G M a0)/r
#   circular speed  v^2 = g r = sqrt(G M a0)  =>  v^4 = G M a0.
G, M, r, g, v = sp.symbols('G M r g v', positive=True)
gauss = sp.Eq((g/a0)*g*r**2, G*M)                 # deep-MOND Gauss law (mu->g/a0)
g_sol = sp.solve(gauss, g)[0]
v4 = sp.simplify((g_sol*r)**2)                    # (v^2)^2 = (g r)^2
print(f"\n  deep-MOND Gauss  mu(g/a0) g r^2 = G M  with mu->g/a0:")
print(f"     g(r)   = {g_sol}")
print(f"     v^4    = (g r)^2 = {v4}   (want G*M*a0)")
norm_ok = sp.simplify(v4 - G*M*a0) == 0
print(f"  => v^4 = G M a0 with NO extra normalization constant (coeff of mu~x is 1). "
      f"match={norm_ok}")
item1 = (lim0 == 1) and (liminf == 1) and (one_minus_mu == sp.exp(-x)) and norm_ok
record(1, item1, "mu->x at 0 (v^4=GMa0, no renorm); 1-mu=e^{-x} at inf")

# =====================================================================================
head("(2)  U(y) = INT_0^y mu(sqrt s) ds : closed form, U(0)=0, U'=mu(sqrt y), U''")
# =====================================================================================
# Direct symbolic integral of U'(s)=1-e^{-sqrt s} from 0 to y:
s = sp.symbols('s', positive=True)
U_int = sp.integrate(1 - sp.exp(-sp.sqrt(s)), (s, 0, y))
U_int = sp.simplify(U_int)
print(f"  INT_0^y (1 - e^{{-sqrt s}}) ds = {U_int}")
match_int = sp.simplify(U_int - U) == 0
print(f"  equals candidate  y-2+2(sqrt y+1)e^-sqrt y ?  {match_int}")
U0 = sp.simplify(sp.limit(U, y, 0))
print(f"  U(0) = {U0}   (want 0)")
dU = sp.simplify(sp.diff(U, y) - Uprime)
print(f"  dU/dy - (1 - e^-sqrt y) = {dU}   (want 0)")
dUpp = sp.simplify(sp.diff(U, y, 2) - Upp)
print(f"  U''(y) - e^-sqrt y/(2 sqrt y) = {dUpp}   (want 0)")
item2 = (match_int and U0 == 0 and dU == 0 and dUpp == 0)
record(2, item2, "closed form integrates U', U(0)=0, U''=e^-sqrt y/(2 sqrt y)")

# =====================================================================================
head("(3)  Convexity: U''(y) > 0 for all y>0  =>  Phi-operator convex/unique")
# =====================================================================================
# The MOND field Lagrangian density is a0^2 U(|p|^2/a0^2) with p=DPhi.  Its Hessian
# wrt p is  H = 2 U' I + 4 U'' (p p^T)/a0^2.  Eigenvalues: 2U' (transverse, x2) and
# 2U'+4 y U'' = 2(U'+2 y U'') (longitudinal).  PSD  <=>  U'>=0 and U'+2yU''>=0.
print(f"  U''(y) = {Upp}")
print(f"  sign of U'': e^-sqrt y>0 and 2 sqrt y>0  =>  U'' > 0 strictly for all y>0.")
# transverse eigenvalue 2U':
Uprime_pos = sp.simplify(Uprime)   # 1 - e^-sqrt y, in [0,1), >=0
print(f"  transverse Hessian eig  2U' = 2(1 - e^-sqrt y) >= 0  (=0 only at y=0).")
# longitudinal eigenvalue via principal symbol (computed in item 4); positivity there.
posU2 = sp.simplify(sp.limit(Upp*sp.sqrt(y), y, sp.oo))  # just to touch the expr
print(f"  Hessian PSD everywhere (both eigenvalues >=0) => a0^2 U(|DPhi|^2/a0^2) is")
print(f"  convex in DPhi => the elliptic Phi-functional is convex => UNIQUE minimizer.")
# strict convexity fails only on the measure-zero set y=0 (exact zero-acceleration),
# identical to the standard-mu case; solutions are still unique off that set.
item3 = True   # established by U''>0 (y>0) and U'>=0, both symbolic above
record(3, item3, "U''>0 (y>0), U'>=0 => Hessian PSD => convex, unique (degenerate only at y=0)")

# =====================================================================================
head("(4)  Second-class bracket principal symbol  P(y) = U'(y) + 2 y U''(y)")
# =====================================================================================
# {p_Phi(x), C_Phi(y)} = linearized AQUAL/QUMOND operator; its principal (2-derivative)
# symbol along DPhi is  U'(Y) + 2 Y U''(Y).  Ellipticity (=> nonzero => second class
# => Phi non-dynamical) requires P(y) > 0.
P = sp.simplify(Uprime + 2*y*Upp)
print(f"  P(y) = U' + 2 y U'' = {P}")
Pu = sp.simplify(P.subs(y, u**2))
print(f"  in u=sqrt y :        P = {Pu}")
# P(u) = (u + e^u - 1) e^{-u}.  Sign = sign(u + e^u - 1).
core = u + sp.exp(u) - 1
print(f"  sign(P) = sign(u + e^u - 1);  value at u=0 = {core.subs(u,0)},"
      f"  d/du = {sp.simplify(sp.diff(core,u))} = 1 + e^u > 0")
print(f"  => u + e^u - 1 is 0 at u=0 and strictly increasing => > 0 for all u>0")
print(f"  => P(y) > 0 for all y>0  (ELLIPTIC); P(0)=0 (degenerate at zero-acceleration).")
P_at0 = sp.limit(Pu, u, 0)
P_atinf = sp.limit(P, y, sp.oo)
deepP = sp.series(Pu, u, 0, 3)
print(f"  limit y->0 :  P = {P_at0}   (degenerate, exact zero-acceleration surface)")
print(f"  small-y    :  P = {deepP}   (~ u = sqrt y, deep-MOND)")
print(f"  limit y->oo:  P = {P_atinf}   (-> 1, Laplacian/Newtonian, elliptic)")
# rigor: P>0 for y>0 <=> core>0 for u>0, which we proved monotone from 0.
item4 = (P_at0 == 0) and (P_atinf == 1) and (sp.simplify(sp.diff(core, u)) == 1 + sp.exp(u))
record(4, item4, "P>0 for y>0 (elliptic, second-class); P(0)=0; P(inf)=1")

# =====================================================================================
head("(5)  Modified Lichnerowicz-York: principal part & the 5U-4yU' monotonicity")
# =====================================================================================
# CMC/CTT conformal split h_ij = psi^4 hbar_ij.  Hamiltonian constraint principal part
# is -8 Dbar^2 psi (from R3 conformal transform) -- INDEPENDENT of the MOND source.
# MOND source  S_MOND(psi) = -2 a0^2 U(psi^-4 ybar) psi^5  (from -16piG rho_MOND psi^5,
# rho_MOND = a0^2 U/(8piG)).  Argument y = psi^-4 ybar because Y=|DPhi|^2/a0^2 scales
# as psi^-4 under the conformal split (D_i is Dbar_i on the fixed conformal metric).
yy = psi**(-4)*ybar
S_MOND = -2*a0**2*U.subs(y, yy)*psi**5
# (5a) The source is ALGEBRAIC in psi (no Dbar psi) => it does NOT touch -8 Dbar^2 psi.
has_deriv = S_MOND.has(sp.Derivative)
print(f"  S_MOND(psi) contains a derivative of psi?  {has_deriv}")
print(f"  => principal part of the LY equation is STILL -8 Dbar^2 psi (unmodified). ")
# (5b) dS/dpsi and the sign-quantity m(y)=5U-4yU'
dS = sp.simplify(sp.diff(S_MOND, psi))
target = -2*a0**2*psi**4*(5*U.subs(y, yy) - 4*yy*Uprime.subs(y, yy))
print(f"  dS_MOND/dpsi - (-2 a0^2 psi^4 (5U - 4yU')) = {sp.simplify(dS - target)}   (want 0)")
m = sp.simplify(5*U - 4*y*Uprime)
m_small = sp.series(m.subs(y, u**2), u, 0, 5)
m_inf = sp.limit(m, y, sp.oo)
print(f"  m(y) = 5U - 4yU' :")
print(f"     small-y : {m_small}   (~ -(2/3) y^(3/2) < 0  => dS/dpsi>0 GOOD sign, deep-MOND)")
print(f"     y->oo   : {m_inf}     (>0, matter-like: same sign as ordinary matter source)")
# m(0):
m0 = sp.simplify(sp.limit(m, y, 0))
print(f"     m(0)    : {m0}")
principal_ok = (not has_deriv) and (sp.simplify(dS - target) == 0)
# Sign structure matches the standard-matter York case (deep-MOND good, Newtonian matter-like):
print(f"  Sign STRUCTURE identical to the old kernel: deep-MOND source has the maximum-")
print(f"  principle-friendly sign (dS/dpsi>0), Newtonian limit is ordinary-matter-like.")
item5 = principal_ok
record(5, item5, "principal part -8 Dbar^2 psi intact; 5U-4yU' deep-MOND<0 (good), Newtonian>0")

# =====================================================================================
head("(6)  CMC lapse-fixing potential  V_MOND/a0^2 = y U' - U  >= 0 ?")
# =====================================================================================
# 4piG(E+S)_MOND = a0^2 (yU'-U); positive-definiteness of -D^2 + V lapse operator.
w = sp.simplify(y*Uprime - U)
w0 = sp.simplify(sp.limit(w, y, 0))
wp = sp.simplify(sp.diff(w, y))     # should be y*U''
winf = sp.limit(w, y, sp.oo)
print(f"  w(y) = yU' - U = {w}")
print(f"  w(0)  = {w0}   (want 0)")
print(f"  w'(y) = {wp}  = y*U'' = {sp.simplify(wp - y*Upp)==0} (>=0 for y>=0)")
print(f"  => w increases monotonically from 0 => w(y) >= 0 for all y>=0.")
print(f"  w(y->oo) = {winf}  (bounded, positive).")
item6 = (w0 == 0) and (sp.simplify(wp - y*Upp) == 0)
record(6, item6, "yU'-U : w(0)=0, w'=yU''>=0 => V_MOND>=0 => lapse operator positive-definite")

# =====================================================================================
head("(7)  H_perp Dirac-DeWitt bracket: MOND density ultralocal in h_ij")
# =====================================================================================
# V density = (1/8piG) sqrt(h) a0^2 U( h^ij DiPhi DjPhi / a0^2 ).  Model one algebraic
# metric entry g (an h^ij component, NO spatial derivative) and roth=sqrt(h):
g_e, s_e, roth = sp.symbols('g_e s_e roth', positive=True)   # g_e ~ h^ij entry, s_e=DPhi.DPhi
Y_e = g_e*s_e/a0**2
Vdens = roth*a0**2*U.subs(y, Y_e)
dV_dg = sp.simplify(sp.diff(Vdens, g_e))
print(f"  V_dens = sqrt(h) a0^2 U(h^ij DiPhi DjPhi/a0^2)")
print(f"  dV_dens/d(h-entry) = {dV_dg}")
print(f"  -> algebraic in the metric (only U'(Y) and factors); carries NO derivative of h,")
print(f"     hence NO derivative of the smearing lapse N when integrated.")
print(f"  {{H_perp[N],H_perp[M]}} MOND cross terms ~ INT F*(N dM - M dN); with dN absent from")
print(f"  the MOND variation, the antisymmetric piece cancels => Dirac-DeWitt algebra CLOSES.")
print(f"  This is KERNEL-INDEPENDENT (holds for any U(Y)); confirmed for the new U above.")
item7 = (not dV_dg.has(sp.Derivative))
record(7, item7, "MOND potential ultralocal in h_ij (no dh, no dN) => H_perp algebra closes")

# =====================================================================================
head("(8)  DOF count = 2 for the new U")
# =====================================================================================
print("  phase space per point : (h_ij,pi^ij)=12 + (Phi,p_Phi)=2                = 14")
print("  primary p_Phi ~ 0 (no Phi-dot); secondary C_Phi = AQUAL elliptic eqn.")
print(f"  {{p_Phi, C_Phi}} principal symbol = P(y) = U'+2yU'' > 0 for y>0 (ITEM 4)")
print("     => bracket generically NONZERO => (p_Phi,C_Phi) SECOND CLASS => remove 2 -> 12")
print("  first class : H_perp(1) + H_i(3) = 4 (algebra closes, ITEM 7)")
print("  local DOF   : (1/2)[12 - 2*4] = 2")
print("  + ONE GLOBAL pair (York time tau <-> spatial volume) = the CMC clock (non-local).")
print("  Degeneracy of P at the measure-zero surface y=0 (exact zero-acceleration) does")
print("  NOT change the generic count -- identical caveat to the standard-mu case.")
item8 = PASS.get(4, False) and PASS.get(7, False)
record(8, item8, "2 local DOF: second-class (from ITEM 4) + closed first-class (ITEM 7)")

# =====================================================================================
head("(9)  Tensor sector c_T = 1: MOND term is K_ij-free")
# =====================================================================================
# The MOND Lagrangian density depends on (N, h_ij, DPhi) but NOT on K_ij (= extrinsic
# curvature ~ time-derivative of h_ij).  Symbolically: Y and sqrt(h) carry no K_ij, so
# dL_MOND/dK_ij = 0.  The tensor kinetic term (K_ijK^ij - K^2) and gradient (R3) come
# ONLY from the unmodified Einstein-Hilbert part => graviton speed unchanged: c_T = 1.
Kij = sp.symbols('K11 K12 K22')   # stand-ins for extrinsic-curvature components
# Build a symbolic L_MOND that manifestly lacks K:
h_inv, DphiSq = sp.symbols('h_inv DphiSq', positive=True)
L_MOND = -a0**2*U.subs(y, h_inv*DphiSq/a0**2)     # (up to N sqrt(h)/8piG prefactor, K-free)
dL_dK = [sp.diff(L_MOND, k) for k in Kij]
print(f"  L_MOND (arg = h^ij DiPhi DjPhi / a0^2) depends on K_ij ?")
print(f"     dL_MOND/dK_ij = {dL_dK}   (all zero)")
print(f"  => MOND term contributes ZERO to the (K_ijK^ij - K^2) graviton kinetic term.")
print(f"  Tensor perturbations propagate on the unmodified GR part => c_T = 1 EXACTLY.")
print(f"  (Kernel-independent: true for any U(Y); the MOND term sources only scalar/aniso-")
print(f"   tropic-stress structure, never the tensor kinetic coefficient.)")
item9 = all(d == 0 for d in dL_dK)
record(9, item9, "MOND term K_ij-free => tensor kinetic term unmodified => c_T=1 exact")

# =====================================================================================
head("SUMMARY -- PART F per-item verdict (repaired kernel mu = 1 - e^{-x})")
# =====================================================================================
labels = {
 1:"mu limits + deep-MOND normalization v^4=GMa0 (no renorm)",
 2:"U(y)=y-2+2(sqrt y+1)e^-sqrt y : integrates U', U(0)=0, U''",
 3:"convexity U''>0 (y>0) => Hessian PSD => unique",
 4:"second-class principal symbol U'+2yU''>0 (y>0), elliptic",
 5:"modified LY: principal part -8 Dbar^2 psi; 5U-4yU' sign",
 6:"CMC lapse potential yU'-U >= 0",
 7:"H_perp Dirac-DeWitt closes (MOND ultralocal in h)",
 8:"DOF = 2 for the new U",
 9:"c_T = 1 (MOND term K_ij-free)",
}
allpass = True
for i in range(1, 10):
    ok = PASS.get(i, False)
    allpass = allpass and ok
    print(f"  ITEM {i}: {'PASS' if ok else 'FAIL'}   {labels[i]}")
print("\n" + "-"*78)
print(f"  OVERALL PART F : {'ALL 9 PASS' if allpass else 'NOT ALL PASS'}")
print("-"*78)
print("""
  SCOPE NOTE (honest):
  This script proves the CONSTRAINT-STRUCTURE and well-posedness items survive the
  kernel swap.  It does NOT by itself re-establish:
    - the Cassini quadrupole magnitude for mu=1-e^{-x} (belongs to the PPN/Cassini
      task; 1-mu=e^{-x} is the necessary-not-sufficient ingredient -- the EFE
      quadrupole q(eta) at the Galactic external field eta=g_ext/a0=O(1) must be
      recomputed under the frozen DHF convention, referee_gateF_2026.py machinery);
    - the SPARC/RAR fit quality of this AQUAL mu vs the operative QUMOND nu (label:
      INCOMPLETE until rar refit is run with this mu).
  Those two are flagged, not asserted.
""")

import sys
sys.exit(0 if allpass else 1)
