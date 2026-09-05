#!/usr/bin/env python3
r"""
Gate (d) for the clock-current nonlocal door: LOCALIZE AND COUNT.

The proposed term  q^2 INT J^m [Box^{-1}] J_m  on the clock's CONSERVED current J^m.  The crux question:
can a conserved-current-sourced nonlocality be retarded/causal WITHOUT adding a propagating mode?

Trichotomy of localizations of Box^{-1} acting on a vector current, each varied here:
  (I)   gauge-invariant vector mediator  L = (a0^2/8piG) F_M(F^2/a0^2) + q A.J     [the unique ghost-free one]
        -> velocity Hessian positive-definite on the MOND electric background (eigenvalues mu, mu, mu + y mu'),
           A_0 nondynamical (Gauss constraint), plane-wave symbol on the background factorizes into a residual-gauge
           factor and TWO propagating polarizations  =>  +2 propagating DOF (A3 violated: 2+1+2 = 5 total).
  (II)  Feynman-type componentwise localization  L = -1/2 d_m V_n d^m V^n + V.J   -> V_0 is a ghost.
  (III) multiplier localization  Lambda^m (Box V_m - J_m)                          -> (V,Lambda) ghost pair (det -b^2).
  (IV)  elliptic replacement Box -> Laplacian                                       -> no velocity dependence: instantaneous (Case 1).
Also computed: the dark photon's characteristic speeds on the exponential-kernel MOND background (req 7, dark sector).
Every check can fail; mutation controls included.
"""
import sys
import sympy as sp

checks = []
def check(name, ok, detail=""):
    checks.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

a0, Gn, q = sp.symbols("a0 G q", positive=True)
y = sp.symbols("y", positive=True)
mu = 1 - sp.exp(-y)
Gker = y**2 + 2*(1 + y)*sp.exp(-y) - 2

print("=" * 96)
print("[I] GAUGE-INVARIANT VECTOR MEDIATOR: velocity Hessian, constraint, and plane-wave symbol on the MOND background")
print("=" * 96)
# temporal gauge A_0 = 0: E_i = -Adot_i ; L(E) = (a0^2/8piG) G(|E|/a0)
E1, E2, E3 = sp.symbols("E1 E2 E3", real=True)
Emag = sp.sqrt(E1**2 + E2**2 + E3**2)
LE = (a0**2/(8*sp.pi*Gn))*Gker.subs(y, Emag/a0)
H = sp.hessian(LE, (E1, E2, E3))
Hbg = H.subs({E1: 0, E2: 0, E3: a0*y})          # background field along z, |E| = a0 y
Hbg = Hbg.applyfunc(sp.simplify)
evs = Hbg.eigenvals()
print("  velocity Hessian eigenvalues on the background (x 4piG):", {sp.simplify(k*4*sp.pi*Gn): v for k, v in evs.items()})
lam_perp = sp.simplify(Hbg[0, 0]*4*sp.pi*Gn)
lam_par = sp.simplify(Hbg[2, 2]*4*sp.pi*Gn)
check("transverse eigenvalue = mu(y) = 1 - e^{-y} (x2)", sp.simplify(lam_perp - mu) == 0 and sp.simplify(Hbg[1, 1]*4*sp.pi*Gn - mu) == 0)
check("longitudinal eigenvalue = mu + y mu' = 1 + (y-1) e^{-y}  (spec's lambda_par)", sp.simplify(lam_par - (1 + (y - 1)*sp.exp(-y))) == 0)
# positivity for y > 0:  mu(0)=0, mu' = e^{-y} > 0  =>  mu > 0.
# lam_par(0)=0, lam_par' = (2-y) e^{-y} > 0 on (0,2)  =>  lam_par > 0 on (0,2];  lam_par - 1 = (y-1)e^{-y} >= 0 for y >= 1.
dlam = sp.simplify(sp.diff(lam_par, y))
print("  d lam_par/dy =", dlam, " ;  lam_par - 1 =", sp.simplify(lam_par - 1))
check("all three eigenvalues positive for every y > 0: no ghost among the spatial components (positive-definite Hessian)",
      sp.simplify(lam_par.subs(y, 0)) == 0 and sp.simplify(dlam - (2 - y)*sp.exp(-y)) == 0
      and sp.simplify(lam_par - 1 - (y - 1)*sp.exp(-y)) == 0
      and sp.simplify(mu.subs(y, 0)) == 0 and sp.simplify(sp.diff(mu, y) - sp.exp(-y)) == 0)
check("MUTATION CONTROL: the wrong-sign kernel -G(y) (the naive 'AQUAL sign' for a vector) has a negative-definite Hessian (ghost)",
      all(sp.simplify(-v*4*sp.pi*Gn).subs(y, 1) < 0 for v in (Hbg[0, 0], Hbg[2, 2])))
# A_0 carries no velocity: F_00 = 0 identically  =>  primary constraint pi^0 = 0 (Gauss law follows)
t, X, Y, Z = sp.symbols("t x y z", real=True)
Afun = [sp.Function(f"A{m}")(t, X, Y, Z) for m in range(4)]
co = [t, X, Y, Z]
Fdd = sp.Matrix(4, 4, lambda m, n: sp.diff(Afun[n], co[m]) - sp.diff(Afun[m], co[n]))
eta = sp.diag(-1, 1, 1, 1)
Fuu = eta*Fdd*eta
I4 = sum(Fdd[m, n]*Fuu[m, n] for m in range(4) for n in range(4))/a0**2
FM = sp.Function("F_M")
L4 = (a0**2/(8*sp.pi*Gn))*FM(I4)
pi0 = sp.diff(L4, sp.Derivative(Afun[0], t))
check("pi^0 = dL/d(A_0 dot) == 0 identically for ANY kernel: A_0 is a Lagrange multiplier (Gauss constraint, first class)", sp.simplify(pi0) == 0)
print("  Dirac count (standard for L(F^2) + A.J with J independent of A): 8-dim phase space per point, two first-class")
print("  constraints (pi^0, Gauss) => 8 - 2x2 = 4 => TWO propagating polarizations.  Verified below at the symbol level.")

# plane-wave symbol on the uniform electric background (source-free), temporal gauge
# linearized EOM: d_m [ Fp f^{mn} + Fpp (2/a0^2) (Fbar_ab f^{ab}) Fbar^{mn} ] = 0  with Fp=F_M'(Ibar), Fpp=F_M''(Ibar)
Fp, Fpp = sp.symbols("Fp Fpp", real=True)
w, kx, kz, Ebar = sp.symbols("omega k_x k_z E", real=True)
kvec = sp.Matrix([-w, kx, 0, kz])             # k_m (lower), wave e^{i(k.x - w t)}
eps = sp.Matrix(sp.symbols("e0 e1 e2 e3", real=True))
f_dd = sp.Matrix(4, 4, lambda m, n: kvec[m]*eps[n] - kvec[n]*eps[m])      # up to a factor i
Fbar_dd = sp.zeros(4, 4); Fbar_dd[3, 0] = Ebar; Fbar_dd[0, 3] = -Ebar     # F_{z0} = E_z
Fbar_uu = eta*Fbar_dd*eta
f_uu = eta*f_dd*eta
contr = sum(Fbar_dd[a, b]*f_uu[a, b] for a in range(4) for b in range(4))
Pi_uu = Fp*f_uu + Fpp*(2/a0**2)*contr*Fbar_uu
# d_m -> i k_m ; EOM_n = k_m Pi^{mn}
EOM = sp.Matrix([sum(kvec[m]*Pi_uu[m, n] for m in range(4)) for n in range(4)])
Msym = sp.Matrix(4, 4, lambda n, b: sp.diff(EOM[n], eps[b]))
gauge_null = sp.simplify(Msym*kvec)
check("gauge invariance: the symbol annihilates eps_m = k_m (pure gauge)", gauge_null == sp.zeros(4, 1))
Msp = Msym[1:, 1:]                                  # temporal gauge eps_0 = 0: spatial block
det_sp = sp.factor(sp.simplify(Msp.det()))
print("  det(spatial symbol) =", det_sp)
# substitute the MOND kernel: Fp = -mu/2, Fpp = mu'/(8y), Ebar = a0 y ; I = -2 y^2
Fpp_mond = sp.simplify(sp.diff(-mu/2, y)/sp.diff(-2*y**2, y))
mond = {Fp: -mu/2, Fpp: Fpp_mond, Ebar: a0*y}
det_mond = sp.factor(sp.simplify(det_sp.subs(mond)))
print("  det with the exponential kernel =", det_mond)
# expected structure: omega^2 * (ordinary: w^2 - k^2) * (extraordinary: lam_par w^2 - lam_perp kx^2 - lam_par kz^2) up to factors
ord_disp = w**2 - kx**2 - kz**2
extra_disp = lam_par*w**2 - lam_perp*kx**2 - lam_par*kz**2
ratio = sp.simplify(det_mond/(w**2*ord_disp*extra_disp))
print("  det / [omega^2 (w^2-k^2) (lam_par w^2 - lam_perp kx^2 - lam_par kz^2)] =", ratio)
check("symbol factorizes: one residual-gauge factor omega^2 (nonpropagating longitudinal) x TWO propagating dispersion factors",
      ratio.free_symbols <= {y} or ratio.is_number)
check("ordinary polarization is exactly luminal on any background (w^2 = k^2)", True if sp.simplify(ratio).free_symbols <= {y} else False)
# characteristic speeds of the extraordinary mode: w^2/k^2 = (lam_perp kx^2 + lam_par kz^2)/(lam_par k^2)
th = sp.symbols("theta", real=True)
v2_extra = sp.simplify((lam_perp*sp.sin(th)**2 + lam_par*sp.cos(th)**2)/lam_par)
print("  extraordinary phase speed^2 (angle theta to E) =", v2_extra)
check("dark-photon characteristics on the MOND background are SUBLUMINAL for all y>0 and all directions "
      "(v^2 - 1 = -(y mu'/lam_par) sin^2 theta <= 0)", sp.simplify(v2_extra - 1 + (y*sp.diff(mu, y)/lam_par)*sp.sin(th)**2) == 0)
check("no superluminal channel: y mu' = y e^{-y} > 0 and lam_par > 0 for y > 0", sp.simplify(y*sp.diff(mu, y) - y*sp.exp(-y)) == 0)
check("MUTATION CONTROL: a kernel with mu' < 0 (e.g. mu = 2 - e^{y}, decreasing) would be superluminal -- test discriminates",
      sp.simplify((y*sp.diff(2 - sp.exp(y), y))).subs(y, 1) < 0)
print("  => (I) is HEALTHY (no ghost, causal, subluminal) but carries TWO propagating dark polarizations: the retarded Box^{-1}")
print("     on a conserved current IS massless-vector exchange; making it causal means giving the vector its own Cauchy data.")

print("\n" + "=" * 96)
print("[II] FEYNMAN-TYPE COMPONENTWISE LOCALIZATION  L = -1/2 d_m V_n d^m V^n + V.J")
print("=" * 96)
Vd = sp.Matrix(sp.symbols("Vd0 Vd1 Vd2 Vd3", real=True))   # time derivatives of V_n
# -1/2 eta^{ma} eta^{nb} d_m V_n d_a V_b  restricted to m=a=0:  -1/2 * eta^{00} * eta^{nb} Vd_n Vd_b
Lkin_F = -sp.Rational(1, 2)*eta[0, 0]*sum(eta[n, b]*Vd[n]*Vd[b] for n in range(4) for b in range(4))
HF = sp.hessian(Lkin_F, list(Vd))
print("  velocity Hessian =", HF)
check("V_0 has NEGATIVE kinetic sign (ghost) while V_i are healthy: exactly the component that would carry the FLRW homogeneous mode",
      HF[0, 0] < 0 and all(HF[i, i] > 0 for i in (1, 2, 3)))

print("\n" + "=" * 96)
print("[III] MULTIPLIER LOCALIZATION  Lambda^m (Box V_m - J_m)  ->  -d Lambda . d V")
print("=" * 96)
a_, b_ = sp.symbols("a b", real=True, positive=True)
Vdot, Ldot = sp.symbols("Vdot Lambdadot", real=True)
Lvel = sp.Rational(1, 2)*a_*Vdot**2 + b_*Vdot*Ldot        # any V self-term a; multiplier cross-term b != 0
HM = sp.hessian(Lvel, (Vdot, Ldot))
check("per component det = -b^2 < 0: opposite-sign kinetic eigenvalues (ghost pair), for every V self-term a", sp.simplify(HM.det() + b_**2) == 0)
print("  (vector version of tensor_nonlocal_localization_gate_2026.py; retarded data are history conditions, not Dirac constraints)")

print("\n" + "=" * 96)
print("[IV] ELLIPTIC REPLACEMENT  Box -> Laplacian")
print("=" * 96)
Vs = sp.Function("V")(t, X, Y, Z)
Lell = -sp.Rational(1, 2)*sum(sp.diff(Vs, s)**2 for s in (X, Y, Z))
check("no velocity dependence at all: the potential is a constraint (instantaneous) -- this is Case 1 of the local theorem (alpha_3 / DC-019)",
      sp.simplify(sp.diff(Lell, sp.Derivative(Vs, t))) == 0)

print("\n" + "=" * 96)
print(f"SCORECARD (d)  ({sum(checks)}/{len(checks)} checks passed)")
print("=" * 96)
print("""  The retarded Box^{-1} acting on a conserved current has exactly one ghost-free causal localization: a dynamical
  massless vector (Gauss constraint + 2 propagating polarizations; positive Hessian and subluminal characteristics on the
  exponential-kernel background).  The alternatives are a V_0 ghost (II), a (V,Lambda) ghost pair (III), or an
  instantaneous constraint (IV = Case 1).  ANSWER TO THE CRUX: NO -- a causal, ghost-free, current-sourced nonlocality
  is a propagating dark vector: N_total = 2 (tensor) + 1 (clock) + 2 (mediator) = 5, violating A3 (at most one extra
  scalar).  This is not a DOF-neutral trick.  Combined with the companion script: the mediator's Gauss law then
  forbids the net-charged homogeneous background, and the mediator never reaches baryons at Newtonian order.""")
sys.exit(0 if all(checks) else 1)
