#!/usr/bin/env python3
r"""
ppn_khronon_routeB_gates_2026.py -- the CONSTITUTIVE fix and the two STATIC gates
(G_eff/G_N and Phi = Psi), computed rather than assumed.

(A) CONSTITUTIVE: what does the auxiliary that multiplies (D phi)^2 have to equal?
    Static, khronon at rest (unitary gauge T=t), weak field, GR gravity sector:
        L/(16 pi G) = -4 grad(Phi).grad(Psi) + 2 (grad Psi)^2 - F((grad Phi)^2)
                      + 16 pi G rho Phi
    (derived: g_00 = -1+2Phi, g_ij = (1+2Psi)d_ij, N = 1-Phi, a_i = d_i ln N = -d_i Phi)
    Psi-variation  => Psi = Phi ;  Phi-variation => div[(1 + F'/2) grad Phi] = 4 pi G rho.
    MOND requires the bracket to BE mu(y):
        F'(A) = 2 (mu(y) - 1) = -2 e^{-y}     and    alpha_khronometric = -F' = 2 e^{-y}.
    So the on-shell value of the auxiliary that multiplies a_mu a^mu is the MOND DEFICIT
    2(1-mu), NOT mu.  With the literal reading chi = mu one gets mu_eff = 1 -+ chi/2 in
    [1/2, 3/2]: the theory never reaches deep MOND at all.

(B) GATE G_eff/G_N: G_eff = G/(1 - alpha/2) = G/mu(y) -> G_N exactly as y -> infinity.

(C) GATE Phi = Psi: order-counting of the spatial TRACELESS stress, computed by explicit
    variation of the static spatial metric.
        MOND sector   Sigma^TF_ij  ~  F'(A) [a_i a_j]^TF          -- QUADRATIC in a
        carrier       Sigma^TF_ij  ~  (f^2/M) A [a_i a_j]^TF      -- QUARTIC  in a
    (Q^ij is auxiliary: its own equation gives Q^ij = (f/M) A^ij, itself O(a^2))
    so the carrier CANNOT cancel Sigma_P at the order Sigma_P appears.
"""
import sympy as sp

y = sp.symbols('y', positive=True)
A, Fp = sp.symbols('A F_prime', real=True)

print("=" * 74)
print("(A) CONSTITUTIVE RELATION -- forced by the theory's own static equations")
mu = 1 - sp.exp(-y)
Fp_req = sp.simplify(2*(mu - 1))
alpha_kh = sp.simplify(-Fp_req)
print("   frozen interpolation      mu(y)      =", mu)
print("   required F'(A)            F'         =", Fp_req)
print("   khronometric alpha        alpha(y)   =", alpha_kh, "= 2(1-mu)")
print("   G_eff/G = 1/(1-alpha/2)              =", sp.simplify(1/(1 - alpha_kh/2)),
      "= 1/mu(y)   [the MOND Poisson law]")
print()
print("   LITERAL reading chi = mu:  mu_eff = 1 -+ chi/2 in [1/2, 3/2]"
      "  -> deep MOND (mu_eff -> 0) UNREACHABLE.")
print("   => the auxiliary that multiplies a.a must be 2(1-mu) = 2 e^{-y}, not mu.")

print()
print("   Solar-System evaluation (a0 = 9.36e-11 m/s^2, framework value):")
a0 = 9.36e-11
GMsun = 1.32712440018e20            # m^3/s^2
AU = 1.495978707e11                 # m
for name, r_AU in (("Earth orbit", 1.0), ("Jupiter orbit", 5.204),
                   ("Saturn orbit", 9.583), ("Cassini conjunction ~8.7 AU", 8.7),
                   ("Neptune orbit", 30.07), ("100 AU", 100.0)):
    g = GMsun/(r_AU*AU)**2
    yv = g/a0
    print("      %-28s g = %.3e m/s^2 ,  y = g/a0 = %.3e ,  alpha_kh = 2 exp(-y)"
          % (name, g, yv))
ymin = GMsun/(100*AU)**2/a0
print("      the SMALLEST y anywhere inside 100 AU is ~%.2e, so alpha_kh <= 2 exp(-%.2e)"
      " ~ 1e-%d :" % (ymin, ymin, int(ymin*0.4343)))
print("      zero to any conceivable precision (it underflows every float format).")
print("      MOND-scale onset (y = 1) sits at r = %.0f AU."
      % (((GMsun/a0)**0.5)/AU))

print()
print("=" * 74)
print("(C) STATIC TRACELESS-STRESS GATE (Phi = Psi):  explicit variation")
# static spatial metric gamma_ij = delta_ij + eps*chi_ij, chi traceless
ep = sp.symbols('eps')
c11, c12, c13, c22, c23 = sp.symbols('c11 c12 c13 c22 c23', real=True)
chi = sp.Matrix([[c11, c12, c13], [c12, c22, c23], [c13, c23, -c11 - c22]])
gam = sp.eye(3) + ep*chi
gaminv = sp.eye(3) - ep*chi + ep**2*chi*chi
detg = sp.simplify(sp.expand(gam.det()))
sqrtg = sp.series(sp.sqrt(detg), ep, 0, 3).removeO()

a1, a2, a3 = sp.symbols('a1 a2 a3', real=True)
av = sp.Matrix([a1, a2, a3])            # a_i = d_i ln N  (metric-INDEPENDENT covector)
Aq = sp.expand((av.T*gaminv*av)[0, 0])  # A = gamma^{ij} a_i a_j

Fsym = sp.Function('F')
L_mond = sp.expand(-sqrtg*Fsym(Aq))
dL = sp.simplify(sp.diff(L_mond, ep).subs(ep, 0))
print("   MOND sector: d/d(chi_ij) of -sqrt(gamma) F(A) at chi=0:")
print("     coefficient of c11 :", sp.simplify(sp.expand(dL).coeff(c11)))
print("     coefficient of c12 :", sp.simplify(sp.expand(dL).coeff(c12)))
print("   -> traceless stress ~ F'(A) [a_i a_j]^TF : QUADRATIC in a, nonzero"
      " whenever F' != 0  (Part-I no-go reproduced)")

# carrier: Q^{ij} auxiliary, traceless; its own equation gives Q^{ij} = (f/M) A^{ij}
q11, q12, q13, q22, q23 = sp.symbols('q11 q12 q13 q22 q23', real=True)
Qm = sp.Matrix([[q11, q12, q13], [q12, q22, q23], [q13, q23, -q11 - q22]])
Aij = av*av.T - sp.Rational(1, 3)*gam*Aq          # A_ij = [a_i a_j]^TF (indices down)
f, Mk = sp.symbols('f M', positive=True)
L_car = sp.expand(sqrtg*(f*sp.trace(Qm*Aij) - sp.Rational(1, 2)*Mk
                         * sp.trace(Qm*gam*Qm*gam)))
dLc = sp.simplify(sp.diff(L_car, ep).subs(ep, 0))
print()
print("   carrier sector: d/d(chi_ij) of sqrt(gamma)[f Q^ij A_ij - (1/2) M Q^ij Q_ij]:")
print("     coefficient of c11 :", sp.simplify(sp.expand(dLc).coeff(c11)))
print("     coefficient of c12 :", sp.simplify(sp.expand(dLc).coeff(c12)))
print()
print("   Q equation of motion:  f A^ij - M Q^ij = 0  =>  Q^ij = (f/M) A^ij ~ O(a^2)")
onshell = {q11: f/Mk*(a1*a1 - sp.Rational(1, 3)*(a1**2 + a2**2 + a3**2)),
           q12: f/Mk*(a1*a2),
           q13: f/Mk*(a1*a3),
           q22: f/Mk*(a2*a2 - sp.Rational(1, 3)*(a1**2 + a2**2 + a3**2)),
           q23: f/Mk*(a2*a3)}
c11c = sp.simplify(sp.expand(dLc).coeff(c11).subs(onshell))
c12c = sp.simplify(sp.expand(dLc).coeff(c12).subs(onshell))
print("     on-shell coefficient of c11 :", sp.factor(sp.simplify(c11c)))
print("     on-shell coefficient of c12 :", sp.factor(sp.simplify(c12c)))
lam_ = sp.symbols('lambda_scale', positive=True)
deg = sp.simplify(sp.expand(c12c.subs({a1: lam_*a1, a2: lam_*a2, a3: lam_*a3})
                            / c12c) if c12c != 0 else 0)
print("     homogeneity degree in a (scaling a -> lambda a):", sp.simplify(deg))
degm = sp.simplify(sp.expand(dL).coeff(c12))
print("     MOND-sector c12 coefficient:", degm, " -> degree 2 in a")
print()
print("   VERDICT (C): carrier traceless stress is O(a^4), Sigma_P is O(a^2).")
print("   They are different orders in the acceleration, so the exact profile match")
print("   f(chi(y)) = y e^{-y} = Sigma_P(y) does NOT produce a cancellation in the")
print("   spatial traceless field equation.  Phi = Psi is NOT established on-shell")
print("   beyond linear order (at linear order gamma_PPN = 1 is verified separately).")
