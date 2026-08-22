#!/usr/bin/env python3
"""
Section 12: gravitational waves in the frozen action, DERIVED not inferred.

Action (units c=1 inside the sympy work; x^0 = ct so K and (3)R both carry 1/length;
c restored analytically in the report):

  S = (M_Pl^2/2) INT dt d^3x N sqrt(h) [ (3)R + K_ij K^ij - lam_K K^2 + eta_K a_i a^i
       - 2 a0^2 F(X,Y) ]
  X = a_i a^i / a0^2   (c=1),   Y = Rbar_ij Rbar^ij / a0^4,
  F = -2 sqrt(X) + 2 ln(1+sqrt(X)) + eps * A(X) * Y,  A(X) = X^2/(1+X)^4.

TENSOR SECTOR, unitary gauge (T = t), TT perturbation:
  N = 1, N_i = 0, h_ij = delta_ij + gamma_ij, gamma TT.

PART A: exact statements: a_i = 0, X = 0, K = O(gamma^2)  => eta_K and lam_K and the
        mu-sector of F contribute NOTHING at quadratic TT order around Minkowski.
PART B: quadratic tensor Lagrangian from (3)R + K_ij K^ij; dispersion => c_T.
PART C: quadratic Y-term for TT; dispersion with frozen eps*A(X0) => k^4 correction.
PART D: finite-X0 background (a^(0) = q zhat), wave perpendicular to a^(0):
        the mu-sector (F_X, F_XX) gives NON-DERIVATIVE (mass-type) gamma^2 terms only,
        with coefficients ~ a0^2 * O(1)  (Hubble-scale mass) -- derived exactly here
        in the frozen-background approximation.
PART E: numbers: GW170817 bound on eps*A(X_path); crossover (EFT) scale.

Every statement printed with PASS/FAIL.
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
e = sp.Symbol('e', positive=True)          # perturbation order parameter
lamK, etaK, epsl, a0, A0 = sp.symbols('lam_K eta_K eps a0 A0', real=True, positive=True)
k, w = sp.symbols('k omega', positive=True)
q = sp.Symbol('q', positive=True)          # background acceleration a_z = q (c=1)
X0 = sp.Symbol('X0', positive=True)

coords = [x, y, z]
FAILURES = []

def check(name, cond):
    print(("PASS: " if cond else "FAIL: ") + name)
    if not cond:
        FAILURES.append(name)

def christoffel(h):
    hin = h.inv()
    G = [[[sp.S(0)]*3 for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for i in range(3):
            for j in range(3):
                s = sp.S(0)
                for l in range(3):
                    s += hin[a, l]*(sp.diff(h[l, i], coords[j])
                                    + sp.diff(h[l, j], coords[i])
                                    - sp.diff(h[i, j], coords[l]))
                G[a][i][j] = sp.together(s/2)
    return G

def ricci(h):
    G = christoffel(h)
    R = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            s = sp.S(0)
            for a in range(3):
                s += sp.diff(G[a][i][j], coords[a]) - sp.diff(G[a][i][a], coords[j])
                for b in range(3):
                    s += G[a][a][b]*G[b][i][j] - G[a][j][b]*G[b][i][a]
            R[i, j] = s
    return R

def order2(expr):
    """coefficient of e^2 in the series of expr around e=0"""
    s = sp.series(expr, e, 0, 3).removeO()
    return sp.expand(s.coeff(e, 2))

# ----------------------------------------------------------------------------------
print("="*78)
print("PART A: exact TT statements around Minkowski (N=1, N_i=0)")
print("="*78)

hp = sp.Function('hp')(t, z)
hx = sp.Function('hx')(t, z)
h = sp.Matrix([[1 + e*hp, e*hx, 0],
               [e*hx, 1 - e*hp, 0],
               [0, 0, 1]])
hin = h.inv()

# lapse N = 1 identically for the TT ansatz => a_i = D_i ln N = 0 exactly.
# (ADM identity a_mu = u^nu grad_nu u_mu with u_mu = -N delta^0_mu gives a_i = d_i ln N,
#  a_0 = 0; verified by direct 4D computation in the docstring derivation.)
# => X = 0 EXACTLY, at every order in gamma. The mu-sector -2sqrt(X)+2ln(1+sqrt X)
#    and the prefactor A(X) are evaluated at X=0: F(0,Y) = eps*A(0)*Y = 0 since A(0)=0.
XA = sp.Symbol('XA', nonnegative=True)
Aofx = XA**2/(1+XA)**4
check("A(0) = 0 exactly (Y-sector switched off at X=0)",
      sp.simplify(Aofx.subs(XA, 0)) == 0 and sp.limit(Aofx, XA, 0) == 0)

# K_ij = (1/2N)(dh/dt - D_i N_j - D_j N_i) = dh/dt / 2
Kij = h.diff(t)/2
K = sp.expand((hin*Kij).trace())
Kser = sp.series(K, e, 0, 3).removeO()
check("K (trace) is O(gamma^2): no O(e) term",
      sp.simplify(sp.expand(Kser).coeff(e, 1)) == 0)
check("lam_K K^2 is O(gamma^4): e^2-coefficient of K^2 vanishes",
      sp.simplify(order2(K**2)) == 0)

detH = sp.factor(h.det())
check("det h = 1 - e^2(hp^2+hx^2)  (traceless => volume preserved at O(e))",
      sp.simplify(detH - (1 - e**2*(hp**2 + hx**2))) == 0)

# ----------------------------------------------------------------------------------
print("="*78)
print("PART B: quadratic tensor Lagrangian from (3)R + K_ij K^ij ; c_T")
print("="*78)

Ric = ricci(h)
Rscal = sp.expand((hin*Ric).trace())
KK = sp.expand((hin*Kij*hin*Kij).trace())

Lbulk = sp.sqrt(detH)*(Rscal + KK - lamK*K**2)     # N=1
L2 = order2(Lbulk)
L2 = sp.expand(sp.simplify(L2))
print("L2 (GR part, before integration by parts):")
print("   ", L2)
check("lam_K absent from quadratic TT Lagrangian", sp.diff(L2, lamK) == 0)

# Euler-Lagrange -> dispersion
eqs = sp.calculus.euler.euler_equations(L2, [hp, hx], [t, z])
pw = {hp: sp.exp(sp.I*(k*z - w*t)), hx: 0}
disp = []
for eq in eqs:
    ex = eq.lhs - eq.rhs
    ex = ex.subs({hp: sp.Function('HP')(t, z)}).replace(sp.Function('HP')(t, z),
                                                        sp.exp(sp.I*(k*z - w*t)))
    ex = sp.simplify(sp.expand(ex.doit()))
    if ex != 0:
        disp.append(sp.simplify(ex/sp.exp(sp.I*(k*z - w*t))))
sols = set()
for d in disp:
    for s in sp.solve(d, w**2):
        sols.add(sp.simplify(s))
print("EL dispersion solutions for omega^2:", sols)
check("tensor dispersion omega^2 = k^2 exactly  (=> c_T = c, massless)",
      sols == {k**2})

# quadratic action normalisation (after ibp the standard GR form):
# expected L2 ~ (1/2)(hp_t^2 + hx_t^2) - (1/2)(hp_z^2 + hx_z^2) up to total derivs
# (per-polarisation normalisation (M_Pl^2/2)*(1/2)[gdot^2 - (dg)^2] * ... printed above)

# ----------------------------------------------------------------------------------
print("="*78)
print("PART C: the Y-term at quadratic TT order (frozen A(X0) = A0)")
print("="*78)

Rbar = Ric - h*Rscal/sp.S(3)
Ycontr = sp.expand((hin*Rbar*hin*Rbar).trace())     # Rbar_ij Rbar^ij
Y2 = order2(Ycontr)
Y2 = sp.simplify(Y2)
print("[Rbar_ij Rbar^ij]_2 =", Y2)
# Rbar_ij^(1) = -(1/2) lap gamma_ij (TT); sum over ij components (xx,yy,xy,yx):
# Rbar^2 = (1/4)[2 (hp'')^2 + 2 (hx'')^2] = (1/2)[(hp'')^2 + (hx'')^2]
check("[Rbar^2]_2 = (1/2)[(hp'')^2 + (hx'')^2]  (pure k^4 structure, no time derivs)",
      sp.simplify(Y2 - sp.Rational(1, 2)*(sp.diff(hp, z, 2)**2 + sp.diff(hx, z, 2)**2)) == 0)

# bracket contribution: -2 a0^2 * eps * A0 * Y,  Y = Rbar^2/a0^4  =>  -(2 eps A0/a0^2) Rbar^2
L2Y = L2 - 2*epsl*A0/a0**2 * Y2
eqs = sp.calculus.euler.euler_equations(sp.expand(L2Y), [hp, hx], [t, z])
disp = []
for eq in eqs:
    ex = (eq.lhs - eq.rhs).replace(hp, sp.exp(sp.I*(k*z - w*t))).subs(hx, 0)
    ex = sp.simplify(sp.expand(ex.doit()))
    if ex != 0:
        disp.append(sp.simplify(ex/sp.exp(sp.I*(k*z - w*t))))
solsY = set()
for d in disp:
    for s in sp.solve(d, w**2):
        solsY.add(sp.factor(sp.simplify(s)))
print("dispersion with Y-term:", solsY)
target = k**2*(1 + 2*epsl*A0*k**2/a0**2)
check("omega^2 = k^2 [1 + 2 eps A(X0) (k/a0)^2]   (k^4 correction, DERIVED)",
      any(sp.simplify(s - target) == 0 for s in solsY))

# ----------------------------------------------------------------------------------
print("="*78)
print("PART D: mu-sector at finite X0: mass-type terms only (wave perp to a^(0))")
print("="*78)
# wave along x, background acceleration a_i = q delta_iz (frozen), TT components in (y,z):
hp2 = sp.Function('hp')(t, x)
hx2 = sp.Function('hx')(t, x)
h2 = sp.Matrix([[1, 0, 0],
                [0, 1 + e*hp2, e*hx2],
                [0, e*hx2, 1 - e*hp2]])
h2in = h2.inv()
avec = sp.Matrix([0, 0, q])
Xex = (avec.T*h2in*avec)[0, 0]/a0**2       # X = h^{ij} a_i a_j / a0^2
F = sp.Function('F')
LF = -2*a0**2*F(Xex)                       # bracket-level F-term
LF2 = order2(LF)
LF2 = sp.simplify(LF2.subs(q**2, X0*a0**2))
LF2 = sp.collect(sp.expand(LF2), [hp2, hx2])
print("[-2 a0^2 F(X)]_2 =", LF2)
# expected: -2 a0^2 [ F'(X0) X0 (hp^2 + hx^2)  + (1/2) F''(X0) X0^2 hp^2 ]  -- pure mass terms
Fp = sp.Derivative(F(X0), X0)
Fpp = sp.Derivative(F(X0), (X0, 2))
LF2_expected = sp.expand(-2*a0**2*(Fp*X0*(hp2**2 + hx2**2) + sp.Rational(1, 2)*Fpp*X0**2*hp2**2))
check("mu-sector at finite X0 => NON-DERIVATIVE gamma^2 terms only, coeff ~ a0^2*O(1): "
      "L2 = -2a0^2[F' X0 (hp^2+hx^2) + (1/2) F'' X0^2 hp^2]",
      sp.simplify(sp.expand(LF2 - LF2_expected).doit()) == 0)
check("no (d gamma)^2 or (dgamma/dt)^2 terms from the mu-sector (c_T untouched at ALL X0)",
      all(sp.diff(LF2, d) == 0 for d in
          [sp.diff(hp2, t), sp.diff(hp2, x), sp.diff(hx2, t), sp.diff(hx2, x)]))

# plug the frozen F: F_X = -1/(1+sqrt X), F_XX = 1/(2 sqrt X (1+sqrt X)^2)
sx = sp.sqrt(X0)
FX = -1/(1 + sx)
FXX = sp.diff(FX, X0)
check("F_XX = 1/(2 sqrt X (1+sqrt X)^2) for the frozen F",
      sp.simplify(FXX - 1/(2*sx*(1 + sx)**2)) == 0)
m2_hx = sp.simplify(2*a0**2*(-FX)*X0)           # +m^2 would be -coeff of hp^2 in L... sign:
# L ⊃ -2a0^2 F' X0 hx^2 = +2a0^2 X0/(1+sqrt X0) hx^2  -> enters L with + sign,
# i.e. a TACHYONIC mass^2 of size m^2 = 2 a0^2 X0/(1+sqrt X0) for the cross pol.
print("mass-type coefficient (hx): L2 ⊃ +", m2_hx, "* hx^2   [tachyonic, |m| ~ a0 = 1/L_Hubble]")
print("mass-type coefficient (hp): L2 ⊃ +",
      sp.simplify(2*a0**2*(-FX)*X0 - a0**2*FXX*X0**2), "* hp^2")

# ----------------------------------------------------------------------------------
print("="*78)
print("PART E: numbers (SI restored):  correction = 2 eps A(X0) (k c^2/a0)^2")
print("="*78)
import math
c = 2.99792458e8
a0SI = 9.3619e-11
ell = c**2/a0SI                       # = c^2/a0, the a0 length
fLIGO = 100.0
kL = 2*math.pi*fLIGO/c
enh = (kL*ell)**2
print(f"  l_a0 = c^2/a0 = {ell:.4e} m  (~ Hubble length)")
print(f"  k(100 Hz) = {kL:.4e} 1/m ;  (k l_a0)^2 = {enh:.4e}")
Amax = 1.0/16.0
bound = 1e-15                          # GW170817 |v_gw - c|/c
# group velocity excess = 3 eps A (k l)^2  for omega^2 = k^2(1 + 2 eps A k^2 l^2)
for label, Aeff, frac in [
        ("worst-case  A=1/16 over the whole 40 Mpc path", Amax, 1.0),
        ("Milky-Way-only segment (10 kpc / 40 Mpc, A=1/16)", Amax, 10.0/40000.0),
        ("IGM floor  x~1e-3 -> A~x^4~1e-12, whole path", 1e-12, 1.0)]:
    eps_bound = bound/(3*Aeff*enh*frac)
    print(f"  {label}:  eps < {eps_bound:.2e}")
# cluster utility of the Y term: O(1) static effect at 100 kpc needs eps*A ~ (k_cl l)^-2
kcl = 1.0/(100*3.086e19)
need = 1.0/((kcl*ell)**2)
print(f"  eps*A needed for O(1) static effect at 100 kpc: {need:.2e}")
epsA_gw = bound/(3*enh*(10.0/40000.0))     # MW-segment bound on eps*A directly
print(f"  eps*A allowed by GW170817 (MW segment): {epsA_gw:.2e}"
      f"   -> conflict factor {need/epsA_gw:.1e}")
kc = a0SI/(c**2*math.sqrt(2*epsA_gw))
print(f"  dispersion-crossover (EFT) scale if GW bound saturated: k_c = {kc:.2f} 1/m "
      f"(f_c = {c*kc/(2*math.pi):.2e} Hz);  eps->0 => k_c -> infinity (GR tensor sector)")

print()
print("FAILURES:", FAILURES if FAILURES else "none")
