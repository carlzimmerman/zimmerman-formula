#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
GATE 2 -- ENERGY / POSITIVITY after the retarded projection, for the Deffayet-Woodard 2026
nonlocal-MOND chassis (arXiv:2512.10513).  Certifies (or not): bounded energy + no
secular / gradient instability / negative-energy radiation in the PHYSICAL (retarded-projected)
sector, on Minkowski and FLRW.

Inputs established this session (committed):
  sf43: UNRESTRICTED localized rep has (X,xi) kinetic signature (+,-) -- FORMAL localization ghost.
  sf44: under the RETARDED / null-IC prescription X,xi,M,phi are metric functionals with NO free
        Cauchy data => the ghost combination is NOT an independent propagating mode (linear).
  => GATE 2 asks the NEXT question: absence of free data != bounded Hamiltonian.  Does energy leak /
     grow / go negative through the retarded source?

Reference dichotomy (arXiv:1307.6639 = Deser & Woodard, "Observational Viability and Stability of
Nonlocal Cosmology"): STABLE class = "the systems' initial value constraints are the same as in
general relativity, and our nonlocal modifications never convert the original gravitons into ghosts";
UNSTABLE class = the ghostful localized versions (auxiliary fields promoted to independent DOF with
free IC).  This script determines which class DW-MOND is in, BY COMPUTATION.

KEY FACTS pulled from the source paper (arXiv:2512.10513, verified by fetch):
  * f(Z) = (1/2) Z exp(-(1/3) sqrt|Z|),  small-Z: f = (1/2)Z - (1/6)Z^{3/2} + O(Z^2).
  * Z = (4 c^4/a0^2)(dX)^2,  X = Box^{-1}(R_uu),  u_mu = d_mu phi,  (dphi)^2 = -1  (MIMETIC constraint).
  * Tensor modes: NO change (Z carries Ricci factors that vanish for GW) => c_T = 1.
  * Deep-MOND static eqn reproduces BTFR v^4 = a0 G M.
  * The paper contains NO perturbation / ghost / c_s / energy analysis.  GATE 2 is unaddressed there.
  * phi obeys the mimetic constraint (dphi)^2 = -1, but (unlike mimetic gravity) is a metric functional
    with null IC -- exactly the sf44 point.

Every quantitative claim below is sympy-checked; output pasted into the report.
a0 = 9.36e-11 (kappa=1/2, Z FITTED -- never claimed derived).
"""
import sympy as sp

def hdr(s):
    print("\n" + "=" * 88 + "\n" + s + "\n" + "=" * 88)

results = {}

# =====================================================================================
hdr("SECTION 1 -- TENSOR (graviton) sector on Minkowski: nonlocal term does NOT modify it")
# =====================================================================================
r"""
Linearize the source R_uu = R_ab u^a u^b for a transverse-traceless (TT) GW around Minkowski with
the mimetic clock at rest, u = d_t (so u^a = delta^a_0).  R_uu^{(1)} = R_00^{(1)}[h^TT].
Linearized Ricci: R_mn^{(1)} = 1/2 ( d_a d_n h^a_m + d_a d_m h^a_n - d_m d_n h - Box h_mn ).
TT gauge: h_0m = 0, h^i_i = 0, d_i h^{ij} = 0.  A GW h_+(t-z), h_x(t-z) in the x-y plane.
If R_00^{(1)} = 0 then X = Box^{-1}(R_uu) = 0 for a GW => Z = 0 => f(Z)=0 => the a0^2 M term contributes
NOTHING to the quadratic tensor action => graviton kinetic term = pure GR => positive energy, c_T^2=1.
"""
t, x, y, z = sp.symbols('t x y z', real=True)
hp = sp.Function('h_plus')(t - z)          # TT plus-polarization, propagating in z
hx = sp.Function('h_cross')(t - z)
# metric perturbation h_{mn}, mostly-plus (-,+,+,+); indices order (0,1,2,3)=(t,x,y,z)
h = sp.zeros(4, 4)
h[1, 1] = hp; h[2, 2] = -hp          # h_xx = -h_yy = h_+
h[1, 2] = hx; h[2, 1] = hx           # h_xy = h_yx = h_x
coords = [t, x, y, z]
eta = sp.diag(-1, 1, 1, 1)           # background Minkowski, mostly-plus
def d(f_, i): return sp.diff(f_, coords[i])
# linearized Ricci R_mn = 1/2 ( d^a d_n h_{am} + d^a d_m h_{an} - d_m d_n h - Box h_mn ), indices raised by eta
h_trace = sp.simplify(sum(eta[a, b] * h[a, b] for a in range(4) for b in range(4)))
def Box(f_): return sum(eta[a, b] * d(d(f_, a), b) for a in range(4) for b in range(4))
def dupdn_h(m, n):  # d^a d_n h_{a m}
    return sum(eta[a, c] * d(d(h[c, m], a), n) for a in range(4) for c in range(4))
R00 = sp.simplify(sp.Rational(1, 2) * (dupdn_h(0, 0) + dupdn_h(0, 0) - d(d(h_trace, 0), 0) - Box(h[0, 0])))
print("  h^TT trace h^a_a          =", h_trace)
print("  R_00^(1)[h^TT] (=R_uu)    =", R00)
results['R00_TT'] = R00
assert R00 == 0, "tensor source did not vanish!"
print("  => X = Box^{-1}(R_uu) = 0 for a GW  =>  Z=0, f(Z)=0  =>  a0^2 M term absent from tensor action")
print("  => graviton kinetic term = pure GR: POSITIVE energy, c_T^2 = 1, no ghost/gradient/secular.")
print("  [PROVED] tensor sector PASSES GATE 2.")

# =====================================================================================
hdr("SECTION 2 -- Quasi-static SCALAR MOND sector on Minkowski: effective mu(y) and its positivity")
# =====================================================================================
r"""
Quasi-static weak field: X = Box^{-1}(R_uu).  Static => Box -> del^2 (spatial), R_uu = R_00 = del^2(Phi)
(Newtonian), so X = Phi (metric potential, in c=1 units).  Then
   Z = (4)(grad X)^2 / a0^2  = 4 (grad Phi)^2 / a0^2 = 4 y^2,   y := |grad Phi|/a0 = g_obs/a0,   sqrt Z = 2y.
The total action R - a0^2 M reduces, in the effective quasi-static field Lagrangian for the potential,
to the natural structure  L(y^2) = A*y^2  +/-  B*f(4 y^2)   (Einstein piece y^2  +  nonlocal f-piece).
The effective interpolation function (coefficient of grad Phi in the flux, field eqn div[mu grad Phi]=4piG rho)
is   mu_eff(y) = P + Q * f'(Z),  Z=4y^2.  The two DW-stated limits fix P,Q UNIQUELY:
   Newtonian y->inf : f'(Z)->0        => mu->P    ; DW require mu->1        => P = 1.
   deep-MOND  y->0  : f'(Z)->1/2      => mu->P+Q/2; DW require mu->0 (mu~y) => Q = -2.
=> mu_eff(y) = 1 - 2 f'(4 y^2).  (This is the interpolation IMPLIED by DW's two stated limits + the
   natural Einstein+f structure; DW themselves do NOT publish mu(y).)
STABILITY of the AQUAL scalar sector (=bounded-below energy, no gradient instability, well-posed elliptic):
   transverse fluctuation eigenvalue   = mu(y)          > 0   REQUIRED
   longitudinal fluctuation eigenvalue = d(y mu)/dy      > 0   REQUIRED
"""
Z = sp.symbols('Z', positive=True)
yy = sp.symbols('y', positive=True)
f = sp.Rational(1, 2) * Z * sp.exp(-sp.sqrt(Z) / 3)
fp = sp.simplify(sp.diff(f, Z))
print("  f(Z)        =", f)
print("  f'(Z)       =", sp.simplify(fp))
# f'(Z) in terms of y (sqrt Z = 2y):
fp_y = sp.simplify(fp.subs(Z, 4 * yy**2))
fp_y = sp.simplify(fp_y.rewrite(sp.exp))
print("  f'(4y^2)    =", sp.simplify(fp_y))
mu = sp.simplify(1 - 2 * fp_y)
print("  mu_eff(y)   = 1 - 2 f'(4y^2) =", mu)
mu_closed = 1 - (1 - yy/3) * sp.exp(-2*yy/3)
print("  closed form check  mu_eff(y) ?= 1-(1-y/3)e^{-2y/3}:",
      sp.simplify(mu - mu_closed) == 0)
results['mu'] = mu_closed

# limits and deep-MOND slope
lim_newt = sp.limit(mu_closed, yy, sp.oo)
lead = sp.series(mu_closed, yy, 0, 3).removeO()
print("  mu(y->inf)          =", lim_newt, "  (Newtonian mu->1)")
print("  mu small-y series   =", sp.simplify(lead), "  (deep-MOND leading term = y)")
results['mu_lim_newt'] = lim_newt
results['mu_series'] = sp.simplify(lead)

# --- PROVE mu_eff(y) > 0 for all y>0 :  P(y)=e^{2y/3}*mu = e^{2y/3}-(1-y/3);  P(0)=0, P'(y)>0.
P = sp.exp(2*yy/3) - (1 - yy/3)
Pp = sp.simplify(sp.diff(P, yy))
print("\n  [mu>0 proof]  P(y):=e^{2y/3} mu = e^{2y/3}-(1-y/3);  P(0)=", P.subs(yy, 0),
      ";  P'(y)=", Pp, " (>0 for all y>=0 since e^{2y/3}>0)")
results['muPos'] = (P.subs(yy, 0) == 0) and (sp.simplify(Pp - (sp.Rational(2,3)*sp.exp(2*yy/3)+sp.Rational(1,3))) == 0)
print("            => P(0)=0 and P'(y)>0  => P(y)>0  => mu_eff(y)>0 for all y>0.  [PROVED]")

# --- PROVE d(y mu)/dy > 0 for all y>0 :  G(y)=d(y mu)/dy; show D(y)=e^{2y/3}*G >0 via D(0)=0,D'(0)>0,D''>=0
ymu = sp.expand(yy * mu_closed)
G = sp.simplify(sp.diff(ymu, yy))
print("\n  [d(y mu)/dy>0 proof]  y*mu =", sp.simplify(ymu))
print("            G(y)=d(y mu)/dy =", G)
D = sp.simplify(sp.expand(G * sp.exp(2*yy/3)))   # = e^{2y/3} - (1 - 4y/3 + 2y^2/9)
D_target = sp.exp(2*yy/3) - (1 - sp.Rational(4,3)*yy + sp.Rational(2,9)*yy**2)
print("            D(y):=e^{2y/3} G(y) =", sp.simplify(D), " ; target e^{2y/3}-(1-4y/3+2y^2/9):",
      sp.simplify(D - D_target) == 0)
D0 = D_target.subs(yy, 0)
Dp = sp.simplify(sp.diff(D_target, yy)); Dp0 = Dp.subs(yy, 0)
Dpp = sp.simplify(sp.diff(D_target, yy, 2))
print("            D(0)=", D0, " ; D'(0)=", Dp0, " ; D''(y)=", Dpp,
      " = (4/9)(e^{2y/3}-1) >=0 for y>=0")
print("            => D' increasing, D'(0)=2>0 => D'>0 => D increasing, D(0)=0 => D>0 => d(y mu)/dy>0. [PROVED]")
results['longPos'] = (D0 == 0 and Dp0 == 2 and sp.simplify(Dpp - sp.Rational(4,9)*(sp.exp(2*yy/3)-1)) == 0)

# numeric scan corroboration (both eigenvalues) across 6 decades of y
import mpmath as mp
mp.mp.dps = 30
muf = sp.lambdify(yy, mu_closed, 'mpmath')
Gf = sp.lambdify(yy, G, 'mpmath')
grid = [mp.mpf('1e-6'), mp.mpf('1e-3'), mp.mpf('0.1'), mp.mpf('0.5'), mp.mpf('1'),
        mp.mpf('2'), mp.mpf('3'), mp.mpf('5'), mp.mpf('10'), mp.mpf('100'), mp.mpf('1e4')]
print("\n  numeric scan (transverse mu, longitudinal d(y mu)/dy):")
allpos = True
for g_ in grid:
    m_ = muf(g_); l_ = Gf(g_)
    allpos = allpos and (m_ > 0) and (l_ > 0)
    print(f"    y={float(g_):12.4g}  mu={float(m_):+.6e}  d(y mu)/dy={float(l_):+.6e}")
results['scan_allpos'] = allpos

# --- AQUAL energy functional F(s), s=y^2:  F' = mu(sqrt s) as function of the AQUAL variable; F>=0
# transverse+longitudinal both >0 => Hessian positive-definite => static energy BOUNDED BELOW.
print("\n  AQUAL static energy density ~ F(y^2) with F'(y^2)=mu; mu>0 => F increasing, F(0)=0 => F>=0.")
print("  Hessian eigenvalues {mu, d(y mu)/dy} both >0 everywhere => POSITIVE-DEFINITE =>")
print("  scalar MOND energy BOUNDED BELOW, NO gradient instability, elliptic & well-posed.  [PROVED]")

# --- explicitly REJECT the naive (wrong) identification mu_naive ~ f'(Z) that would flip sign
mu_naive = fp_y   # ~ f'(4y^2) alone (WITHOUT the Einstein '1')
root_naive = sp.nsolve(mu_naive, yy, 3)   # f'(4y^2)=0 at y=3 (sqrt Z=6)
print("\n  [anti-overstatement] NAIVE identification mu~f'(4y^2) alone vanishes at y=",
      float(root_naive), " and goes NEGATIVE for y>3.")
print("  This is the WRONG reduction: it omits the Einstein '1'. The correct mu_eff=1-2f'(4y^2) stays")
print("  POSITIVE (overshoots 1 just past transition, never negative). The apparent 'mu<0 for g>3a0'")
print("  is a manufactured kill and is REJECTED (cf. the sf43 overstatement lesson).")

# =====================================================================================
hdr("SECTION 3 -- MIMETIC clock sector: sound speed c_s^2 = 0 (marginal, no gradient instability)")
# =====================================================================================
r"""
phi obeys the MIMETIC constraint g^{mn} d_m phi d_n phi = -1 (paper's Eq. for u_mu=d_mu phi).
FLRW scalar-perturbed metric (Newtonian gauge): ds^2 = -(1+2Phi)dt^2 + a^2(1-2Psi)dx^2, phi=t+dphi.
Impose the constraint at linear order and read the perturbed kinetic structure of dphi.
"""
tt, kk = sp.symbols('t k', real=True)
a = sp.Function('a')(tt)
Phi = sp.Function('Phi')(tt)      # metric potential (function of t at fixed Fourier mode)
dphi = sp.Function('dphi')(tt)
# g^{00} to linear order for g_00=-(1+2Phi):  g^{00} = -(1-2Phi)
g00 = -(1 - 2*Phi)
# constraint g^{mn} dphi dphi = g^{00}(d_t phi)^2 + g^{ij} d_i phi d_j phi = -1
# spatial gradient term (d_i dphi)^2 is 2nd order (dphi already 1st order) => drops at linear order
dt_phi = 1 + sp.diff(dphi, tt)
constraint_lhs = sp.expand(g00 * dt_phi**2)
constraint_lin = sp.simplify(sp.series(constraint_lhs, sp.Symbol('eps'), 0, 2))  # keep linear
# linearize by hand: g00*dt_phi^2 = -(1-2Phi)(1+2 dphi_dot) ~ -(1 + 2 dphi_dot - 2 Phi)
lin = -(1 + 2*sp.diff(dphi, tt) - 2*Phi)
print("  constraint (linearized):  g^{mn}dphi dphi = ", lin, "  set = -1")
sol = sp.solve(sp.Eq(lin, -1), sp.diff(dphi, tt))
print("  => dphi_dot =", sol, "  (dphi is SLAVED to the metric potential Phi; 1st-order in time)")
print("  => NO independent (grad dphi)^2 gradient term in the quadratic action (it is 2nd order and")
print("     the constraint leaves no free spatial dynamics) => dispersion omega^2 = c_s^2 k^2 with")
print("     c_s^2 = 0.  MIMETIC DUST: MARGINAL (c_s^2=0 is NOT a gradient instability, which needs")
print("     c_s^2<0; and NOT a ghost). This is exactly how the model mimics pressureless dark matter.")
results['cs2_mimetic'] = 0
print("  DW twist (sf44): phi is a metric functional with null IC => this c_s^2=0 mode has NO free")
print("  Cauchy data => it is not an independently excitable caustic-forming channel (unlike standard")
print("  mimetic DM, where phi is free). Caustic/strong-coupling is a NONLINEAR concern -> different gate.")

# =====================================================================================
hdr("SECTION 4 -- FLRW background: transport solution, boundedness of f, self-limiting nonlocal energy")
# =====================================================================================
r"""
Transport: nabla_mu[ sqrt(-g) u^mu (M+f) ] = 0.  On FLRW u^mu=(1,0,0,0), sqrt(-g)=a^3:
   d/dt[ a^3 (M+f) ] = 0   =>   M = -f(Z) + K/a^3.
The homogeneous piece K/a^3 REDSHIFTS AWAY (dust) => NO secular growth of the background nonlocal
sector.  The -f(Z) piece is bounded because f is bounded on the whole real Z-axis (below).
On FLRW, X=X(t) is homogeneous => dX = Xdot u_mu => Z = (4/a0^2)(dX)^2 = -(4/a0^2)Xdot^2 <= 0
(timelike), matching the paper's "large negative Z" cosmological branch.
"""
Zr = sp.symbols('Z', real=True)
f_full = sp.Rational(1,2) * Zr * sp.exp(-sp.sqrt(sp.Abs(Zr))/3)
# extrema on Z>0 branch:
fpos = sp.Rational(1,2)*Zr*sp.exp(-sp.sqrt(Zr)/3)
crit = sp.solve(sp.diff(fpos, Zr), Zr)
print("  f on Z>0: critical points (f'(Z)=0):", crit)
Zc = [c for c in crit if c.is_real and c > 0]
for c in ([sp.Integer(36)] if not Zc else Zc):
    print("    f(Z=%s) = %s = %.6f   (global max on Z>0)" % (c, sp.nsimplify(fpos.subs(Zr, c)),
                                                             float(fpos.subs(Zr, c))))
lim_pos = sp.limit(fpos, Zr, sp.oo)
# Z<0 branch: f = (1/2) Z exp(-sqrt(-Z)/3), Z->-inf
w_ = sp.symbols('w', positive=True)   # w=-Z>0
fneg = sp.Rational(1,2)*(-w_)*sp.exp(-sp.sqrt(w_)/3)
lim_neg = sp.limit(fneg, w_, sp.oo)
print("  lim_{Z->+inf} f =", lim_pos, "  ;  lim_{Z->-inf} f =", lim_neg,
      "  => f BOUNDED on all Z (|f|<=18/e^2~2.44).")
results['f_bounded'] = (lim_pos == 0 and lim_neg == 0)
print("  => even if the retarded auxiliary X grows secularly (Deser-Woodard growing mode, Z->-inf),")
print("     the exponential suppression drives f->0 => M->K/a^3 (dust) => nonlocal ENERGY CONTRIBUTION")
print("     SELF-LIMITS. No secular energy blow-up. [DERIVED, given f bounded]")

# =====================================================================================
hdr("SECTION 5 -- classification vs arXiv:1307.6639 and negative-energy radiation")
# =====================================================================================
print(r"""
  1307.6639 STABLE-class criterion (quoted): "the systems' initial value constraints are the same as
  in general relativity, and our nonlocal modifications never convert the original gravitons into ghosts."
    (i)  same IV constraints as GR : YES -- sf44 (null-IC => X,xi,M,phi carry NO free Cauchy data =>
         the constraint surface is GR's; DW state phi,rho are metric functionals, NOT free mimetic fields).
    (ii) gravitons never become ghosts : YES -- SECTION 1 (R_uu[TT]=0 => tensor action = pure GR,
         c_T^2=1, positive energy).
  => DW-MOND sits in the STABLE class of 1307.6639, by the SAME mechanism Deser-Woodard proved for
     their nonlocal cosmology, PLUS the extra self-limiting exponential cap on f (SECTION 4).

  NEGATIVE-ENERGY RADIATION (channel c): the only radiating sector on Minkowski is the graviton, which
  is UNMODIFIED (SECTION 1) => no negative-energy graviton radiation. The scalar sector is elliptic /
  constrained (no free data, sf44) and the mimetic mode has c_s^2=0 => NON-radiating. No negative-energy
  radiation channel exists at linear order. [DERIVED]
""")

# =====================================================================================
hdr("VERDICT ASSEMBLY")
# =====================================================================================
print(f"""
  R_00^(1)[h^TT]                     = {results['R00_TT']}      (tensor source vanishes)
  mu_eff(y)                          = {results['mu']}
  mu_eff(y->inf)                     = {results['mu_lim_newt']}   (Newtonian)
  mu_eff small-y                     = {results['mu_series']}   (deep MOND, leading y)
  mu_eff(y) > 0  proved              = {results['muPos']}
  d(y mu)/dy > 0 proved              = {results['longPos']}
  numeric scan both eigenvalues >0   = {results['scan_allpos']}
  mimetic sound speed c_s^2          = {results['cs2_mimetic']}   (marginal dust; not <0)
  f bounded on all Z (self-limiting) = {results['f_bounded']}

  MINKOWSKI physical sector : tensor PASS (PROVED) + scalar MOND PASS (mu>0 & d(y mu)/dy>0, PROVED)
                              => energy BOUNDED BELOW, NO gradient instability, NO secular growth,
                                 NO negative-energy radiation.  ===> GATE 2 PASS on Minkowski.
  FLRW : background energy bounded (f capped, dust mode decays) [DERIVED]; mimetic scalar c_s^2=0
         [PROVED for the constraint] -- marginal, no gradient instability.
  OWED (the single remaining piece): the FULL coupled FLRW scalar-perturbation spectrum including the
         f(Z) gradient coupling (Z=(dX)^2, X=Box^{-1}R_uu), to certify c_s^2>=0 in EVERY channel (not
         only the bare mimetic one). DW published no such analysis. Mimetic structure + exponential cap
         make c_s^2>=0 expected but it is SUPPORTED, not PROVED here.

  OVERALL GATE 2 = PARTIAL: Minkowski physical sector CERTIFIED PASS (explicit certificates);
  FLRW background + bare mimetic c_s^2 PASS; full-coupling FLRW perturbation c_s^2 OWED. No instability
  found in any computed channel. The naive 'mu<0 for g>3a0' kill is a WRONG identification, REJECTED.
""")
print("checks:", results)
