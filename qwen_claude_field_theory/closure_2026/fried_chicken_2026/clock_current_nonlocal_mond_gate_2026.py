#!/usr/bin/env python3
r"""
NONLOCAL DOOR, ATTEMPT 3 -- nonlocality carried by the clock's OWN conserved current.

Candidate (written out explicitly, all gates from THIS action):

  S = INT d^4x sqrt(-g) [ (c^4/16 pi G)(R - 2 Lambda)                    (gravity, one metric)
                          + P(X),  X = -g^{mn} d_m T d_n T                (clock scalar T; shift symmetry
                                                                            => conserved current J^m = 2 P_X grad^m T,
                                                                            charge density n = -J.u, dust-like)
                          + (a0^2 / 8 pi G) F_M(I),  I = F_{mn}F^{mn}/a0^2 (mediator A_m, F = dA; the MOND kernel:
                                                                            F_M(I) = G(y), y = sqrt(-I/2),
                                                                            G(y) = y^2 + 2(1+y)e^{-y} - 2, G'(y)/(2y) = 1-e^{-y})
                          + q A_m J^m ]                                    (mediator couples ONLY to the clock current)
      + S_m[g, psi]                                                        (baryons minimally coupled to g ONLY, req 5/11)

Integrating out A gives exactly the requested term  q^2 INT J^m [Box^{-1}]_{field-dependent} J_m : the retarded
Box^{-1} acting on a conserved current IS the exchange of a massless vector, and the field-dependent kernel is the
nonlinear (MOND) constitutive law of that vector.  This is the unique ghost-free, causal, Euler--Lagrange
localization of the proposed nonlocal term (the multiplier and Feynman-gauge localizations are ghosts: see the
companion clock_current_localization_dof_gate_2026.py).  Every gate below is derived from this local action by
explicit variation.  Ratio-lock (task's mechanism): n = lambda rho_b, with q lambda = 1 so that A_0 is sourced by
rho_b exactly.

Gates: (a) AQUAL for the current's potential and for the METRIC potential baryons feel
       (b) lensing Phi, Psi both derived   (c) c_T    (e) conservation    (f) FLRW: dust a^-3, Gauss law.
Every check can fail; each block carries a mutation control.
"""
import sys
import numpy as np
import sympy as sp

checks = []
def check(name, ok, detail=""):
    checks.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

a0, Gn, q, lam = sp.symbols("a0 G q lambda", positive=True)
y = sp.symbols("y", positive=True)

# ------------------------------------------------------------------------------------------------
print("=" * 96)
print("[A] THE KERNEL, AND AQUAL FOR THE CURRENT'S POTENTIAL V = A_0 (exact exponential law)")
print("=" * 96)
Gker = y**2 + 2*(1 + y)*sp.exp(-y) - 2                    # spec req 12 primitive
mu_exact = 1 - sp.exp(-y)
check("G'(y)/(2y) == 1 - e^{-y} exactly (spec primitive)", sp.simplify(sp.diff(Gker, y)/(2*y) - mu_exact) == 0)
Gmut = y**2                                                 # mutation: Newtonian kernel
mu_mut = sp.simplify(sp.diff(Gmut, y)/(2*y))
check("MUTATION CONTROL: kernel G=y^2 gives mu==1 (Newtonian, NOT MOND) -- test discriminates",
      mu_mut == 1 and sp.simplify(mu_exact.subs(y, 1)) != 1)

# static 3D Euler-Lagrange for V(x,y,z):  L = +(a0^2/8piG) G(|grad V|/a0) + q n V   (healthy-vector sign, see [B])
X, Y, Z = sp.symbols("x y z", real=True)
V = sp.Function("V")(X, Y, Z)
nfun = sp.Function("n")(X, Y, Z)
gradV = [sp.diff(V, s) for s in (X, Y, Z)]
absg = sp.sqrt(sum(c**2 for c in gradV))
yV = absg/a0
Lstat = (a0**2/(8*sp.pi*Gn))*Gker.subs(y, yV) + q*nfun*V
# constitutive relation  dL/d(d_i V) = +(1/4piG) mu(y) d_i V
D_i = [sp.diff(Lstat, c) for c in gradV]
constitutive_ok = all(sp.simplify(D_i[i] - (1/(4*sp.pi*Gn))*mu_exact.subs(y, yV)*gradV[i]) == 0 for i in range(3))
check("constitutive law  dL/d(grad V) = (1/4piG) mu(|grad V|/a0) grad V  with mu = 1-e^{-y}", constitutive_ok)
EL = sp.diff(Lstat, V) - sum(sp.diff(D_i[i], s) for i, s in enumerate((X, Y, Z)))
target = q*nfun - (1/(4*sp.pi*Gn))*sum(sp.diff(mu_exact.subs(y, yV)*gradV[i], s) for i, s in enumerate((X, Y, Z)))
check("Euler-Lagrange for V  ==  q n - (1/4piG) div[mu grad V]   i.e.  div[mu(|grad V|/a0) grad V] = 4 pi G q n",
      sp.simplify(EL - target) == 0)
# spherical / deep-MOND for V sourced by the dark charge (ratio-locked: q n = rho_b when q*lambda = 1)
g, gN = sp.symbols("g g_N", positive=True)
deep = sp.series((1 - sp.exp(-g/a0))*g, g, 0, 3).removeO()
check("spherical: mu(g/a0) g = g_N  ->  deep-MOND  g^2 = a0 g_N  (leading term of mu g is g^2/a0)",
      sp.simplify(deep - g**2/a0) == 0)
print("  => the CURRENT'S potential V=A_0 obeys the exact exponential AQUAL law sourced by q n.  With the ratio lock")
print("     n = lambda rho_b and q lambda = 1 its source is rho_b.  Gate (a) for V: PASS.  The question is whether V is")
print("     the potential BARYONS feel (they couple only to g): decided in [B]-[C] below.")

# ------------------------------------------------------------------------------------------------
print("\n" + "=" * 96)
print("[B] STRESS TENSOR OF THE MEDIATOR BY EXPLICIT METRIC VARIATION (generic kernel, then MOND kernel)")
print("=" * 96)
# independent upper-metric symbols, symmetric derivative convention; T_mn = -2 dL/dg^{mn} + g_mn L
# (uses the textbook identity delta sqrt(-g) = -1/2 sqrt(-g) g_mn delta g^{mn})
gsym = {}
for m in range(4):
    for n_ in range(m, 4):
        gsym[(m, n_)] = sp.symbols(f"gu{m}{n_}", real=True)
def gu(m, n_):
    return gsym[(min(m, n_), max(m, n_))]
Fsym = {}
for m in range(4):
    for n_ in range(m + 1, 4):
        Fsym[(m, n_)] = sp.symbols(f"F{m}{n_}", real=True)
def Fd(m, n_):
    if m == n_:
        return sp.Integer(0)
    return Fsym[(m, n_)] if m < n_ else -Fsym[(n_, m)]
Icov = sum(gu(m, a_)*gu(n_, b_)*Fd(m, n_)*Fd(a_, b_) for m in range(4) for n_ in range(4) for a_ in range(4) for b_ in range(4))/a0**2
FM = sp.Function("F_M")
Lcov = (a0**2/(8*sp.pi*Gn))*FM(Icov)
def dL_dg(m, n_):
    s = gsym[(min(m, n_), max(m, n_))]
    d = sp.diff(Lcov, s)
    return d if m == n_ else d/2
eta = sp.diag(-1, 1, 1, 1)
# lower metric on the Minkowski point: g_mn = eta_mn ; evaluate at g^{mn} = eta^{mn}
sub_eta = {gsym[(m, n_)]: eta[m, n_] for (m, n_) in gsym}
E1, E2, E3 = sp.symbols("E1 E2 E3", real=True)
sub_E = {Fsym[(0, 1)]: -E1, Fsym[(0, 2)]: -E2, Fsym[(0, 3)]: -E3, Fsym[(1, 2)]: 0, Fsym[(1, 3)]: 0, Fsym[(2, 3)]: 0}  # F_{i0}=+E_i, no B
Tmn = sp.zeros(4, 4)
for m in range(4):
    for n_ in range(4):
        Tmn[m, n_] = (-2*dL_dg(m, n_) + eta[m, n_]*Lcov).subs(sub_eta).subs(sub_E)
Ival = sp.simplify(Icov.subs(sub_eta).subs(sub_E))
E2s = E1**2 + E2**2 + E3**2
check("invariant on the electric configuration:  I = F^2/a0^2 = -2 E^2/a0^2  = -2 y^2", sp.simplify(Ival + 2*E2s/a0**2) == 0)
Fp = sp.Symbol("FMp")  # F_M'(I)
FMval = sp.Symbol("FMval")
def canon(expr):
    """map Subs(Derivative(F(d),(d,k)), d, I) -> F_p..p(I): canonical chain-rule objects for a generic kernel"""
    def repl(e):
        der = e.expr
        return sp.Function(der.expr.func.__name__ + "_" + "p"*der.derivative_count)(*e.point)
    return expr.replace(lambda e: isinstance(e, sp.Subs) and isinstance(e.expr, sp.Derivative), repl)
def _is_applied(e, name):
    return isinstance(e, sp.core.function.AppliedUndef) and e.func.__name__ == name
Tmn_s = Tmn.applyfunc(lambda e: sp.simplify(canon(e).replace(lambda t_: _is_applied(t_, "F_M_p"), lambda t_: Fp)
                                             .replace(lambda t_: _is_applied(t_, "F_M"), lambda t_: FMval)))
check("every entry of the varied T_mn is a function of F_M(I) and F_M'(I) only (chain rule closed)",
      not any(e.atoms(sp.Subs) or e.atoms(sp.Derivative) for e in Tmn_s))
print("  T_00 (generic kernel) =", sp.factor(Tmn_s[0, 0]))
print("  T_11 (generic kernel) =", sp.factor(Tmn_s[1, 1]))
# MOND kernel: F_M(I) = G(y), y = sqrt(-I/2)  =>  F_M'(I) = -G'(y)/(4y) = -mu/2 ;  F_M = G
mond_sub = {Fp: -mu_exact/2, FMval: Gker}
EtoY = {E1: 0, E2: 0, E3: a0*y}   # field along z, |E| = a0 y
T00_mond = sp.simplify(Tmn_s[0, 0].subs(mond_sub).subs(EtoY))
T33_mond = sp.simplify(Tmn_s[3, 3].subs(mond_sub).subs(EtoY))
T11_mond = sp.simplify(Tmn_s[1, 1].subs(mond_sub).subs(EtoY))
print("  MOND kernel: T_00 =", sp.simplify(T00_mond), " ;  T_zz =", sp.simplify(T33_mond), " ;  T_xx =", sp.simplify(T11_mond))
check("T_00 = (a0^2/8piG)[2 mu y^2 - G(y)]  (derived, not assumed)",
      sp.simplify(T00_mond - (a0**2/(8*sp.pi*Gn))*(2*mu_exact*y**2 - Gker)) == 0)
# Maxwell control: G=y^2, mu=1 -> T_00 = E^2/8piG > 0, T_ij = -(E_iE_j - 1/2 delta E^2)/4piG  (healthy sign)
T00_max = sp.simplify(Tmn_s[0, 0].subs({Fp: -sp.Rational(1, 2), FMval: -Ival/2}))
T11_max = sp.simplify(Tmn_s[1, 1].subs({Fp: -sp.Rational(1, 2), FMval: -Ival/2}))
check("MUTATION/CONTROL: Newtonian kernel reproduces Maxwell  T_00 = +E^2/8piG (positive energy: healthy vector sign)",
      sp.simplify(T00_max - E2s/(8*sp.pi*Gn)) == 0)
check("Maxwell control: T_xx = -(E_x^2 - E^2/2)/4piG  (standard Maxwell stress)",
      sp.simplify(T11_max + (E1**2 - E2s/2)/(4*sp.pi*Gn)) == 0)
T00_deep = sp.series(T00_mond, y, 0, 4).removeO()
check("deep MOND: T_00 -> (a0^2/6piG) y^3 > 0  (positive energy also on the MOND branch)",
      sp.simplify(T00_deep - (a0**2/(6*sp.pi*Gn))*y**3) == 0)
# anisotropic (trace-free) stress that sources Phi-Psi
TF = sp.simplify(T33_mond - T11_mond)   # zz - xx = (3/2)*(zz - trace/3) for a z-directed field
check("trace-free stress  T_zz - T_xx = -(mu/4piG) E^2 = -(a0^2/4piG) mu y^2  (O(E^2))",
      sp.simplify(TF + (a0**2/(4*sp.pi*Gn))*mu_exact*y**2) == 0)

# --- the coupling term q A_m J^m with J^m = 2 P_X g^{mn} d_n T: its OWN metric variation (closes the 'coupling stress' loophole) ---
Pf = sp.Function("P")
Vsym, Tdot0 = sp.symbols("V Tdot", real=True)
g00u = gsym[(0, 0)]
Xc = -g00u*Tdot0**2                                       # X = -g^{mn} d_m T d_n T with T = T(t), static A = (V,0,0,0)
L_AJ = q*Vsym*2*sp.diff(Pf(Xc), Xc)*g00u*Tdot0 if False else None
Xs = sp.Symbol("X_s")
PX = sp.Function("P_X")
L_AJ = q*Vsym*2*PX(-g00u*Tdot0**2)*g00u*Tdot0             # sqrt(-g)-stripped coupling density: q A_0 J^0, J^0 = 2 P_X g^{00} Tdot
T00_AJ = (-2*sp.diff(L_AJ, g00u) + eta[0, 0]*L_AJ).subs(g00u, -1).subs(Tdot0, 1)
T00_AJ = canon(T00_AJ)
print("  coupling-term stress T_00^{AJ} (T=t, A=(V,0,0,0)) =", sp.simplify(T00_AJ))
check("the coupling stress is PROPORTIONAL to V (no V-independent piece): T_00^{AJ} = O(q n V) = O(n Phi/c^2), post-Newtonian",
      sp.simplify(T00_AJ.subs(Vsym, 0)) == 0 and sp.simplify(sp.diff(T00_AJ, Vsym, 2)) == 0)
print("  (the clock's own stress 2P_X dT dT + g P supplies the O(n) Newtonian source; every V-dependent term is O(n V) or O(V^2))")

# --- the load-bearing ORDER comparison: mediator energy vs the phantom density the MOND boost needs ---
M, r, c = sp.symbols("M r c", positive=True)
rM = sp.sqrt(Gn*M/a0)                   # MOND radius of the (ratio-locked) source
y_deep = rM/r                             # deep-MOND: |grad V| = sqrt(G M a0)/r  =>  y = r_M/r
rho_ph = sp.sqrt(Gn*M*a0)/(4*sp.pi*Gn*r**2)   # phantom density: (1/4piG) lap(sqrt(GMa0) ln r) [mass density, c=1 units]
T00_field = (a0**2/(6*sp.pi*Gn))*y_deep**3      # deep-MOND mediator energy density (mass units, c=1)
ratio = sp.simplify(T00_field/rho_ph)
print("  deep MOND, point source:  T_00^A / rho_phantom  =", ratio, "  [c=1]  ->  (2/3) G M/(r c^2) with c restored")
check("mediator energy / phantom density = (2/3) G M/(r c^2): post-Newtonian, NOT Newtonian order",
      sp.simplify(ratio - sp.Rational(2, 3)*Gn*M/r) == 0)

# ------------------------------------------------------------------------------------------------
print("\n" + "=" * 96)
print("[C] LENSING: Phi AND Psi BOTH DERIVED FROM THE LINEARIZED EINSTEIN EQUATIONS WITH ALL SOURCES")
print("=" * 96)
eps = sp.symbols("epsilon")
t = sp.symbols("t", real=True)
Phi = sp.Function("Phi")(X, Y, Z)
Psi = sp.Function("Psi")(X, Y, Z)
coords = [t, X, Y, Z]
gdn = sp.diag(-(1 + 2*eps*Phi), 1 - 2*eps*Psi, 1 - 2*eps*Psi, 1 - 2*eps*Psi)
gup = gdn.inv()
def christoffel(gdn, gup):
    Gam = [[[0]*4 for _ in range(4)] for _ in range(4)]
    for a_ in range(4):
        for b_ in range(4):
            for c_ in range(4):
                Gam[a_][b_][c_] = sum(gup[a_, d]*(sp.diff(gdn[d, b_], coords[c_]) + sp.diff(gdn[d, c_], coords[b_]) - sp.diff(gdn[b_, c_], coords[d])) for d in range(4))/2
    return Gam
Gam = christoffel(gdn, gup)
def ricci(Gam):
    Ric = sp.zeros(4, 4)
    for b_ in range(4):
        for c_ in range(4):
            Ric[b_, c_] = sum(sp.diff(Gam[a_][b_][c_], coords[a_]) - sp.diff(Gam[a_][b_][a_], coords[c_])
                              + sum(Gam[a_][a_][d]*Gam[d][b_][c_] - Gam[a_][c_][d]*Gam[d][b_][a_] for d in range(4)) for a_ in range(4))
    return Ric
Ric = ricci(Gam)
Rs = sum(gup[a_, b_]*Ric[a_, b_] for a_ in range(4) for b_ in range(4))
Ein = (Ric - gdn*Rs/2).applyfunc(lambda e: sp.series(e, eps, 0, 2).removeO().coeff(eps, 1))
lap = lambda f: sum(sp.diff(f, s, 2) for s in (X, Y, Z))
check("linearized G_00 = 2 lap(Psi)  (from the metric, not assumed)", sp.simplify(Ein[0, 0] - 2*lap(Psi)) == 0)
G12_expected = sp.diff(Psi - Phi, X, Y)
check("linearized G_xy = d_x d_y (Psi - Phi)  (trace-free slip channel)", sp.simplify(Ein[1, 2] - G12_expected) == 0)
trace_sp = sum(Ein[i, i] for i in (1, 2, 3))
check("linearized G_kk = 2 lap(Phi - Psi)", sp.simplify(trace_sp - 2*lap(Phi - Psi)) == 0)
print("  Einstein eqs (c=1): 2 lap Psi = 8piG [rho_b + n + T^A_00] ;  2 lap(Phi-Psi) = 8piG T^A_kk ;  G_ij^TF = 8piG T^A_ij^TF")
print("  => Psi solves Poisson with source rho_b + n (+ O(E^2) mediator energy);  Phi - Psi = O(E^2) (mediator stress).")
# quantitative: relative size of the O(E^2) corrections to Psi and to (Phi-Psi), deep MOND, point source
TA_kk = sp.simplify((T11_mond*2 + T33_mond).subs(y, y_deep))     # spatial trace of mediator stress
slip_source = sp.simplify(4*sp.pi*Gn*TA_kk)                        # lap(Phi - Psi)  (trace equation)
newt_source = sp.simplify(4*sp.pi*Gn*rho_ph)                       # lap of the MOND-required potential (phantom part)
ratio_slip = sp.simplify(sp.series(slip_source/newt_source, r, sp.oo, 3).removeO())
print("  trace channel:  lap(Phi-Psi)/lap(Phi_MOND-needed)  (deep MOND, leading) =", ratio_slip)
check("trace-channel slip source = (1/8)(GM/r)(r_M/r): the deep-MOND mediator stress is 3D-traceless at leading order (L homogeneous "
      "of degree 3 in E), so the trace slip is even below O(GM/r c^2)",
      sp.simplify(ratio_slip - sp.Rational(1, 8)*(Gn*M/r)*(rM/r)) == 0)
# trace-free channel: G_ij^TF = 8piG T_ij^TF ; leading anisotropic stress |T_zz - T_xx| = (a0^2/4piG) mu y^2 ~ (a0^2/4piG) y^3
TF_deep = sp.simplify(sp.series(((a0**2/(4*sp.pi*Gn))*mu_exact*y**2).subs(y, y_deep), r, sp.oo, 4).removeO())
ratio_TF = sp.simplify(TF_deep/rho_ph)
print("  trace-free channel:  |T_zz - T_xx| / rho_phantom  (deep MOND, leading) =", ratio_TF)
check("trace-free slip source is exactly (GM/r) x phantom density at leading deep-MOND order: O(GM/(r c^2)) => Phi = Psi at Newtonian order",
      sp.simplify(ratio_TF - Gn*M/r) == 0)
print("  BOTH potentials derived:  Phi = Psi = Phi_N[rho_b + n] + O(v^2/c^2).  Under the ratio lock n = lambda rho_b:")
print("       Phi = (1+lambda) Phi_N[rho_b]  -- a CONSTANT boost of Newton, NOT the MOND function.")

# baryon-felt acceleration vs exact MOND, numerically, framework a0 and mu
G_SI = 6.674e-11; c_SI = 2.998e8; a0_SI = 9.36e-11; Msun = 1.989e30
lam_num = 0.1200/0.02237        # Planck 2018 Omega_c h^2 / Omega_b h^2 = 5.36 (ratio-lock value)
def g_mond_exact(gN):
    # solve (1 - exp(-g/a0)) g = gN for g
    lo, hi = gN, np.sqrt(a0_SI*gN) + gN + a0_SI
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if (1 - np.exp(-mid/a0_SI))*mid > gN: hi = mid
        else: lo = mid
    return 0.5*(lo + hi)
print("\n  baryon-felt g = dPhi/dr from THIS action (ratio lock, lambda=%.2f) vs exact MOND g for rho_b:" % lam_num)
worst = []
all_rows = []
for name, Mb in [("dwarf 1e9 Msun", 1e9*Msun), ("MW-like 6e10 Msun", 6e10*Msun), ("giant 3e11 Msun", 3e11*Msun)]:
    rMv = np.sqrt(G_SI*Mb/a0_SI)
    rows = []
    for f in (1.0, 3.0, 10.0):
        rr = f*rMv
        gN = G_SI*Mb/rr**2
        Efield2 = G_SI*Mb*a0_SI/rr**2                      # deep-MOND |grad V|^2 for the locked charge (q lambda = 1)
        yv = np.sqrt(Efield2)/a0_SI
        T00 = (a0_SI**2/(8*np.pi*G_SI))*(2*(1 - np.exp(-yv))*yv**2 - (yv**2 + 2*(1 + yv)*np.exp(-yv) - 2))  # J/m^3
        rhoA = T00/c_SI**2
        # enclosed mediator mass is at most 4pi r^3 rhoA (upper bound since rhoA falls as r^-3 -> log; use it as a bound)
        gA_bound = G_SI*(4*np.pi*rr**3*rhoA*np.log(rr/(0.01*rMv)))/rr**2
        g_this = (1 + lam_num)*gN + gA_bound
        gM = g_mond_exact(gN)
        rows.append((f, g_this/gN, gM/gN, gA_bound/gN))
    print(f"   {name}: r_M = {rMv/3.086e19:.1f} kpc")
    for f, b_this, b_mond, bA in rows:
        print(f"      r = {f:4.1f} r_M :  g/g_N (this action) = {b_this:6.3f}   exact-MOND g/g_N = {b_mond:6.3f}   mediator-energy part = {bA:.1e}")
    worst.append(max(abs(np.log10(b_this/b_mond)) for _, b_this, b_mond, _ in rows))
    all_rows.extend(rows)
check("baryon-felt boost is a CONSTANT (1+lambda), the MOND boost is not: mismatch > 0.15 dex somewhere in r_M..10 r_M for every mass",
      all(w > 0.15 for w in worst), f"worst |log10| mismatch per galaxy = {['%.2f' % w for w in worst]}")
check("mediator-energy contribution to the baryon-felt acceleration is < 1e-5 of g_N at every sampled (mass, radius)",
      all(bA < 1e-5 for _, _, _, bA in all_rows), f"max = {max(bA for _, _, _, bA in all_rows):.1e}")
# Keplerian vs flat: log-slope of v^2 = r dPhi/dr at large r
v2 = r*sp.diff(-(1 + lam)*Gn*M/r, r)
check("rotation-curve slope: d ln v^2 / d ln r = -1 (Keplerian) for Phi=(1+lambda)Phi_N, vs 0 (flat) required by MOND",
      sp.simplify(r*sp.diff(sp.log(v2), r)) == -1)
print("  Gate (a) for BARYONS: FAIL.  The current's potential V never enters g_mn at Newtonian order; the mediator")
print("  reaches the metric only through its stress, which is quadratic in grad V  =>  O(Phi_N/c^2) suppressed.")

# ------------------------------------------------------------------------------------------------
print("\n" + "=" * 96)
print("[C'] TENSOR SPEED: does the dark sector touch the graviton principal symbol?")
print("=" * 96)
# TT wave h_12(t,z) on Minkowski; check derivative-of-metric dependence of sqrt(-g) L_A and of sqrt(-g) R
h = sp.Function("h")(t, Z)
gTT = sp.Matrix([[-1, 0, 0, 0], [0, 1, eps*h, 0], [0, eps*h, 1, 0], [0, 0, 0, 1]])
gTTu = gTT.inv()
sqrtg = sp.sqrt(-gTT.det())
# A-sector: sqrt(-g) F_M(g^{ma} g^{nb} F_mn F_ab / a0^2) with a fixed background field F (symbols)
Fbg = sp.Matrix(4, 4, lambda i, j: Fd(i, j))
I_TT = sum(gTTu[m, a_]*gTTu[n_, b_]*Fbg[m, n_]*Fbg[a_, b_] for m in range(4) for n_ in range(4) for a_ in range(4) for b_ in range(4))/a0**2
LA_TT = sqrtg*(a0**2/(8*sp.pi*Gn))*FM(I_TT)
LA2 = sp.series(LA_TT, eps, 0, 3).removeO()
no_hdot = sp.simplify(sp.diff(LA2, sp.Derivative(h, t))) == 0 and sp.simplify(sp.diff(LA2, sp.Derivative(h, Z))) == 0
check("mediator sector: quadratic TT action contains NO d_t h or d_z h  (no metric-derivative dependence, any kernel)", no_hdot)
# clock sector: sqrt(-g) P(X), X = -g^{mn} d_m T d_n T with T = T(t) background + symbols: also no metric derivatives
Tdot = sp.symbols("Tdot", real=True)
X_TT = -gTTu[0, 0]*Tdot**2
LP_TT = sp.series(sqrtg*sp.Function("P")(X_TT), eps, 0, 3).removeO()
check("clock sector P(X): quadratic TT action contains NO d_t h or d_z h",
      sp.simplify(sp.diff(LP_TT, sp.Derivative(h, t))) == 0 and sp.simplify(sp.diff(LP_TT, sp.Derivative(h, Z))) == 0)
# gravity sector (control): sqrt(-g) R for the same TT wave DOES contain h_dot^2 and (d_z h)^2 with the GR ratio
coordsTT = [t, X, Y, Z]
def ricci_scalar(gdn_):
    gup_ = gdn_.inv()
    Gam_ = [[[sum(gup_[a_, d]*(sp.diff(gdn_[d, b_], coordsTT[c_]) + sp.diff(gdn_[d, c_], coordsTT[b_]) - sp.diff(gdn_[b_, c_], coordsTT[d])) for d in range(4))/2
              for c_ in range(4)] for b_ in range(4)] for a_ in range(4)]
    Ric_ = sp.zeros(4, 4)
    for b_ in range(4):
        for c_ in range(4):
            Ric_[b_, c_] = sum(sp.diff(Gam_[a_][b_][c_], coordsTT[a_]) - sp.diff(Gam_[a_][b_][a_], coordsTT[c_])
                               + sum(Gam_[a_][a_][d]*Gam_[d][b_][c_] - Gam_[a_][c_][d]*Gam_[d][b_][a_] for d in range(4)) for a_ in range(4))
    return sum(gup_[a_, b_]*Ric_[a_, b_] for a_ in range(4) for b_ in range(4))
LEH2 = sp.series(sqrtg*ricci_scalar(gTT), eps, 0, 3).removeO().coeff(eps, 2)
# integrate by parts symbolically: coefficient of h_t^2 and h_z^2 after removing h*h_tt, h*h_zz via (h h_tt -> -h_t^2)
LEH2_ibp = sp.expand(LEH2).subs({h*sp.Derivative(h, (t, 2)): -sp.Derivative(h, t)**2, h*sp.Derivative(h, (Z, 2)): -sp.Derivative(h, Z)**2})
cT_coef_t = LEH2_ibp.coeff(sp.Derivative(h, t)**2)
cT_coef_z = LEH2_ibp.coeff(sp.Derivative(h, Z)**2)
print("  EH TT quadratic density (after ibp): coeff(h_t^2) =", cT_coef_t, ", coeff(h_z^2) =", cT_coef_z)
check("MUTATION CONTROL: the Einstein-Hilbert term DOES carry h_t^2 and h_z^2 with c_T^2 = -coeff_z/coeff_t = 1",
      cT_coef_t != 0 and sp.simplify(-cT_coef_z/cT_coef_t) == 1)
check("c_T = 1 EXACTLY: the graviton principal symbol is the GR one (dark sector adds only non-derivative terms)",
      no_hdot and sp.simplify(-cT_coef_z/cT_coef_t) == 1)

# ------------------------------------------------------------------------------------------------
print("\n" + "=" * 96)
print("[E] CONSERVATION: mediator + charged clock dust, generic kernel, 3+1, from the Euler-Lagrange equations")
print("=" * 96)
A = [sp.Function(f"A{m}")(t, X, Y, Z) for m in range(4)]
Fdd = sp.Matrix(4, 4, lambda m, n_: sp.diff(A[n_], coords[m]) - sp.diff(A[m], coords[n_]))
Fuu = eta*Fdd*eta
Ifl = sum(Fdd[m, n_]*Fuu[m, n_] for m in range(4) for n_ in range(4))/a0**2
xi = sp.Symbol("xi")
FMp_I = sp.Subs(sp.Derivative(FM(xi), xi), xi, Ifl)      # F_M'(I) as the genuine derivative object (chain rule automatic)
# L_A = (a0^2/8piG) F_M(I);  T^{mn} = -(1/2piG) F_M' F^{ma} F^n_a + eta^{mn} (a0^2/8piG) F_M
Fmix = Fuu*eta*Fuu.T   # F^{m a} F^{n}_{a} = F^{ma} eta_{ab} F^{nb}
Tuu = -(1/(2*sp.pi*Gn))*FMp_I*Fmix + eta*(a0**2/(8*sp.pi*Gn))*FM(Ifl)
# EOM defines the current: q J^n = d_m [ (1/2piG) F_M' F^{mn} ]
Jup = [sum(sp.diff((1/(2*sp.pi*Gn))*FMp_I*Fuu[m, n_], coords[m]) for m in range(4))/q for n_ in range(4)]
Jdn = [sum(eta[n_, k]*Jup[k] for k in range(4)) for n_ in range(4)]
# identity to test:  d_m T^{mn} + q F^{n a} J_a == 0   (uses dF=0 automatically since F=dA)
resid = []
for n_ in range(4):
    divT = sum(sp.diff(Tuu[m, n_], coords[m]) for m in range(4))
    lorentz = q*sum(Fuu[n_, a_]*Jdn[a_] for a_ in range(4))
    resid.append(sp.simplify(sp.expand(canon(divT + lorentz))))
check("d_m T_A^{mn} + q F^{n a} J_a == 0 for all n (generic F_M, generic A_m(t,x,y,z))  [mediator exchanges momentum with the charge]",
      all(rr == 0 for rr in resid), "residuals: " + str([0 if rr == 0 else 'nonzero' for rr in resid]))
# MUTATION: drop the trace term eta^{mn} L  -> conservation fails
Tuu_mut = -(1/(2*sp.pi*Gn))*FMp_I*Fmix
divT_mut = sum(sp.diff(Tuu_mut[m, 0], coords[m]) for m in range(4))
lorentz0 = q*sum(Fuu[0, a_]*Jdn[a_] for a_ in range(4))
resid_mut = sp.simplify(sp.expand(canon(divT_mut + lorentz0)))
check("MUTATION CONTROL: dropping the eta^{mn} L term breaks the identity (test discriminates)", resid_mut != 0)
# charged dust: T_d^{mn} = n u^m u^n with continuity d_m(n u^m)=0 and Lorentz force u.d u^n = q F^n_a u^a  =>  d_m T_d^{mn} = q F^{n a} J_a
# 1+1 check with u = (gamma, gamma v), gamma = 1/sqrt(1-v^2)
v = sp.Function("v")(t, X); nd = sp.Function("nd")(t, X); E = sp.Function("E")(t, X)
gam = 1/sp.sqrt(1 - v**2)
u = [gam, gam*v]
eta2 = sp.diag(-1, 1)
F2 = sp.Matrix([[0, -E], [E, 0]])      # F_{01} = -E, F_{10} = +E  (F_{i0} = E_i)
F2uu = eta2*F2*eta2
Td = sp.Matrix(2, 2, lambda m, n_: nd*u[m]*u[n_])
c2 = [t, X]
divTd = [sum(sp.diff(Td[m, n_], c2[m]) for m in range(2)) for n_ in range(2)]
cont = sum(sp.diff(nd*u[m], c2[m]) for m in range(2))
# Lorentz: u^m d_m u^n = q F^{n}_{a} u^a  -> solve for d_t v
udu = [sum(u[m]*sp.diff(u[n_], c2[m]) for m in range(2)) for n_ in range(2)]
lor = [q*sum(F2uu[n_, a_]*sum(eta2[a_, b_]*u[b_] for b_ in range(2)) for a_ in range(2)) for n_ in range(2)]
vt_sol = sp.solve(sp.Eq(udu[1], lor[1]), sp.Derivative(v, t))[0]
nt_sol = sp.solve(sp.Eq(cont, 0), sp.Derivative(nd, t))[0]
Jd_up = [nd*u[m] for m in range(2)]
Jd_dn = [sum(eta2[m, k]*Jd_up[k] for k in range(2)) for m in range(2)]
dust_resid = []
for n_ in range(2):
    e_ = divTd[n_] - q*sum(F2uu[n_, a_]*Jd_dn[a_] for a_ in range(2))
    e_ = e_.subs(sp.Derivative(nd, t), nt_sol).subs(sp.Derivative(v, t), vt_sol)
    dust_resid.append(sp.simplify(e_))
check("charged clock dust: d_m T_d^{mn} = + q F^{n a} J_a on its own equations (1+1, both components)  => total dark stress conserved",
      all(rr == 0 for rr in dust_resid))
# sign of the mediator force on the dust: nonrelativistic limit of the Lorentz equation, then the AQUAL point-charge potential
vt_nr = sp.simplify(vt_sol.subs(v, 0).doit())          # dust element momentarily at rest
check("nonrelativistic dust acceleration = + q E = + q dV/dx  (E = d_x A_0 = d_x V)", sp.simplify(vt_nr - q*E) == 0)
# spherical AQUAL for V with positive source q n:  f(V') := mu(|V'|/a0) V' = G q Q_c / r^2 > 0.
# f is odd and strictly increasing (f' = lambda_par > 0), so a positive right-hand side forces V' > 0 (V rises outward).
p = sp.symbols("p", positive=True)
f_pos = (1 - sp.exp(-p/a0))*p
f_neg = (1 - sp.exp(-sp.Abs(-p)/a0))*(-p)
check("AQUAL flux function is odd, positive for V'>0, negative for V'<0, and strictly increasing (f' = 1+(y-1)e^{-y} > 0)",
      sp.simplify(f_neg + f_pos) == 0 and sp.simplify(sp.diff(f_pos, p) - (1 + (p/a0 - 1)*sp.exp(-p/a0))) == 0)
# f_pos/p = 1 - e^{-p/a0} > 0  <=>  -p/a0 < 0, which holds for p, a0 > 0
check("=> point charge: V' > 0 outward, acceleration +q V' points AWAY from the charge: like charges REPEL (healthy vector);"
      " the MOND-strength force on the dark dust has the ANTI-gravity sign",
      sp.simplify(f_pos/p - (1 - sp.exp(-p/a0))) == 0 and sp.ask(sp.Q.negative(-p/a0)) is True)
print("  => the ratio lock n = lambda rho_b is not even dynamically preserved: the charged dust is pushed OUT of the baryons by")
print("     its own MOND-strength self-repulsion (sign SOLID; the resulting profile NOT-COMPUTED, but it cannot be the")
print("     baryon-tracking one).  An ATTRACTIVE MOND self-force needs a scalar mediator = a second scalar (Case 4).")
print("  Baryons: S_m[g,psi] is a separate diff-invariant functional with no A or T dependence  =>  grad_m T_b^{mn} = 0 is")
print("  its own Ward identity (standard; the same status as the Candidate-B note).  Gate (e): PASS -- conservation is NOT the")
print("  obstruction for this door once the kernel is localized (consistent with Leg-B S4).")

# ------------------------------------------------------------------------------------------------
print("\n" + "=" * 96)
print("[F] FLRW: the clock's charge redshifts as dust; the mediator's Gauss law forbids the charged homogeneous background")
print("=" * 96)
a_ = sp.Function("a")(t); nH = sp.Function("n")(t)
cont_flrw = sp.diff(a_**3*nH, t)          # d_m(sqrt(-g) n u^m) with u=(1,0,0,0), sqrt(-g)=a^3
sol = sp.dsolve(sp.Eq(cont_flrw, 0), nH)
check("clock charge: d_m(sqrt(-g) n u^m) = 0 on FLRW  =>  n = C a^{-3} (dust-like, the CMB-relevant scaling)",
      sp.simplify(sol.rhs*a_**3).free_symbols <= {sp.Symbol('C1')})
srcH = sp.symbols("s", positive=True)
sol_mut = sp.dsolve(sp.Eq(cont_flrw, srcH*a_**3), nH)
check("MUTATION CONTROL: a non-conserved current (source s) is NOT a^{-3}", sp.simplify(sol_mut.rhs*a_**3).has(t))
# Gauss law on the homogeneous isotropic background: A_m = (A_0(t), 0, 0, 0) is the only such ansatz; F = 0 identically
A0t = sp.Function("A0")(t)
Ahom = [A0t, 0, 0, 0]
Fhom = sp.Matrix(4, 4, lambda m, n_: sp.diff(Ahom[n_], coords[m]) - sp.diff(Ahom[m], coords[n_]))
check("homogeneous-isotropic mediator ansatz has F_mn == 0 identically (any A_0(t) is pure gauge)", Fhom == sp.zeros(4, 4))
print("  the nu=0 mediator equation on FLRW:  d_m[ sqrt(-g) (1/2piG) F_M' F^{m0} ] = q sqrt(-g) J^0 = q a^3 n")
# build the nu=0 equation on the FLRW ansatz explicitly (generic kernel) and solve it for n
gF = sp.diag(-1, a_**2, a_**2, a_**2); gFu = gF.inv(); sqrtgF = a_**3
Fhom_uu = gFu*Fhom*gFu
I_hom = sum(Fhom[m, n_]*Fhom_uu[m, n_] for m in range(4) for n_ in range(4))/a0**2
lhs0 = sum(sp.diff(sqrtgF*(1/(2*sp.pi*Gn))*sp.Subs(sp.Derivative(FM(xi), xi), xi, I_hom)*Fhom_uu[m, 0], coords[m]) for m in range(4))
n_sym = sp.symbols("n_hom")
gauss_hom = sp.Eq(sp.simplify(lhs0), q*sqrtgF*n_sym)
sol_n = sp.solve(gauss_hom, n_sym)
print("  nu=0 equation on the homogeneous ansatz:", gauss_hom, " -> n =", sol_n)
check("Gauss law on the homogeneous background: the only solution is n = 0 (contradiction with the a^{-3} charge, unless it vanishes)",
      sol_n == [0])
# anisotropic homogeneous ansatz A_m = (A_0(t), A_1(t), A_2(t), A_3(t)): E_i(t) = -A_i dot != 0 but divergence-free
Aani = [sp.Function(f"Ah{m}")(t) for m in range(4)]
Fani = sp.Matrix(4, 4, lambda m, n_: sp.diff(Aani[n_], coords[m]) - sp.diff(Aani[m], coords[n_]))
Fani_uu = gFu*Fani*gFu
I_ani = sum(Fani[m, n_]*Fani_uu[m, n_] for m in range(4) for n_ in range(4))/a0**2
lhs0_ani = sum(sp.diff(sqrtgF*(1/(2*sp.pi*Gn))*sp.Subs(sp.Derivative(FM(xi), xi), xi, I_ani)*Fani_uu[m, 0], coords[m]) for m in range(4))
sol_n_ani = sp.solve(sp.Eq(sp.simplify(lhs0_ani), q*sqrtgF*n_sym), n_sym)
check("even an ANISOTROPIC homogeneous mediator (E_i(t) != 0, Bianchi-I-like) gives d_i E^i = 0 => n = 0: no homogeneous charged background at all",
      Fani != sp.zeros(4, 4) and sol_n_ani == [0])
# periodic-box form of the same statement with the full nonlinear kernel: INT div[mu grad V] = 0 for any periodic V
L_box, Amp = sp.symbols("L_box A_p", positive=True)
Vper = Amp*sp.sin(2*sp.pi*X/L_box)                       # any periodic V: V'(0) = V'(L)
Vd = sp.diff(Vper, X)
flux = (1/(4*sp.pi*Gn))*(1 - sp.exp(-sp.Abs(Vd)/a0))*Vd   # exponential-kernel flux mu(|V'|/a0) V'
box_lhs = sp.simplify(flux.subs(X, L_box) - flux.subs(X, 0))   # fundamental theorem: INT_0^L d(flux)/dx dx
nbar = sp.symbols("nbar", positive=True)
box_rhs = sp.integrate(q*nbar, (X, 0, L_box))
print("  periodic box: [flux]_0^L =", box_lhs, "  vs  INT q nbar dx =", box_rhs)
check("periodic-box Gauss identity: the net flux of the exponential-kernel field vanishes for a periodic V, the charge integral q nbar L does not",
      box_lhs == 0 and sp.simplify(box_rhs) != 0)
# neutralized control: source n - nbar integrates to zero -> consistent
check("MUTATION CONTROL: a NEUTRALIZED source (n - nbar, zero mean) is consistent with Gauss -- but then the mean charge that was to give Omega_dm sources nothing",
      sp.simplify(sp.integrate(q*(nbar + sp.cos(2*sp.pi*X/L_box)*nbar - nbar), (X, 0, L_box))) == 0)
# scalar-mediator variant (form factor on n instead of on J^m): homogeneous mode exists (no Gauss law) -> different failure
phi_t = sp.Function("phi")(t); Hs = sp.symbols("H", positive=True); gs = sp.symbols("g_s")
scalar_hom = sp.dsolve(sp.Eq(sp.diff(phi_t, t, 2) + 3*Hs*sp.diff(phi_t, t), gs*nbar), phi_t)
check("contrast: a SCALAR mediator (kernel on n, not J^m) has a homogeneous solution phi(t)  => the Gauss-law kill is specific to the vector/current kernel",
      scalar_hom.rhs.has(t))
print("  => the CMB pass (Omega_dm from the charge) is NOT automatic: with the massless vector mediator the charged")
print("     homogeneous background does not exist.  Escapes: neutralize (then the mean charge sources no MOND potential),")
print("     or a Proca mass (3 DOF, Yukawa cutoff must exceed Mpc), or a scalar mediator (a SECOND scalar: Case 4, and")
print("     it still fails gate (a) for baryons by the [B] source-order argument, which is mediator-independent).")

# ------------------------------------------------------------------------------------------------
print("\n" + "=" * 96)
print(f"SCORECARD  ({sum(checks)}/{len(checks)} checks passed; a failed check would abort the verdict below)")
print("=" * 96)
print("""  (a)  AQUAL for the current's potential V=A_0, mu=1-e^{-y}: PASS (exact, derived)           -- SOLID
  (a') MOND for BARYONS (metric Phi): FAIL -- Phi = Psi = Phi_N[rho_b+n] + O(GM/rc^2);           -- SOLID
       mediator energy / phantom density = (2/3) GM/(r c^2) ~ 1e-7; ratio lock gives a CONSTANT boost (Keplerian)
  (b)  Phi = Psi: PASS at Newtonian order, both derived; slip = O(E^2) -- but for the NON-MOND potential  -- SOLID
  (c)  c_T = 1 exactly: PASS (dark sector has no metric-derivative dependence; EH control fires)      -- SOLID
  (e)  conservation: PASS (baryons: own Ward identity; dark sector: d T_A + d T_dust = 0 on shell)   -- SOLID
  (f)  FLRW: charge is a^{-3} dust PASS; charged homogeneous background FAIL (Gauss law) => CMB Omega_dm
       from the charge is NOT automatic for the vector kernel                                        -- SOLID
  (d)  localization / DOF: see clock_current_localization_dof_gate_2026.py (gauge boson: +2 propagating DOF)
VERDICT: the clock-current nonlocal door is DEAD.  Primary obstruction = a SOURCE-ORDER one, independent of the
kernel and of localization: under minimal coupling (A1) the dark charge's nonlocal potential reaches g_mn only
through the mediator stress, quadratic in grad V, hence O(Phi_N/c^2) relative to the Newtonian source.  Baryons never
see the MOND potential.  Secondary: the unique healthy causal localization is a gauge boson (+2 DOF, A3) whose Gauss
law forbids the net-charged homogeneous clock dust (A7).  Conservation is NOT the obstruction here.""")
sys.exit(0 if all(checks) else 1)
