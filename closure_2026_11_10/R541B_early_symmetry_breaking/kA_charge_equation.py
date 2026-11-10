"""R541B KA1: charge equation of action (A) + (-V(tau)) in the expanding background (sympy).
Template: closure_2026_11_10/R541_why_the_cold_share/part_B_action/frw_charge.py. c = 1, 2K = 8 pi G."""
import sympy as sp

t = sp.symbols('t')
K, mu, Lam, rb0 = sp.symbols('K mu_K Lambda rho_b0', positive=True)
N = sp.Function('N')(t); a = sp.Function('a')(t); tau = sp.Function('tau')(t)
V = sp.Function('V')
Q = sp.diff(tau, t) / N
L_grav = (-6 * a * sp.diff(a, t)**2 / N - 2 * Lam * N * a**3) / (4 * K)
L_K = N * a**3 * mu**2 * (Q - 1)**2 / (2 * K)
L_V = -N * a**3 * V(tau)
L_m = -N * rb0
L = L_grav + L_K + L_V + L_m

p_tau = sp.simplify(sp.diff(L, sp.diff(tau, t)))
EL_tau = sp.simplify(sp.diff(p_tau, t) - sp.diff(L, tau))
print("p_tau =", p_tau)
print("dL/dtau =", sp.simplify(sp.diff(L, tau)))
C = sp.Function('C')(t)
# Euler-Lagrange: d p_tau/dt = dL/dtau
rhs = sp.simplify(sp.diff(L, tau))
target = -N * a**3 * sp.Subs(sp.diff(V(sp.Symbol('s')), sp.Symbol('s')), sp.Symbol('s'), tau).doit()
print("KA1a dC/dt - (-N a^3 V'(tau)) =", sp.simplify(rhs - target))
print("KA1b V = 0: dL/dtau =", sp.simplify(sp.diff(L.subs(V(tau), 0), tau)), "-> C conserved")

# Energy density and pressure seen by the foliation (N = 1)
qs = sp.symbols('q')
rho = sp.simplify(-sp.diff(L_K + L_V, N).subs(N, 1) / a**3)
rho_q = sp.factor(rho.subs(sp.diff(tau, t), qs))
print("rho_K + V (N=1, Q=q) =", rho_q, " (frw_charge.out: mu^2 (q-1)(q+1)/2K, plus V)")
# pressure from d L / d(a^3) at fixed N=1: p = dL_field/d(a^3)
A3 = sp.symbols('A3', positive=True)
Lf = (mu**2 * (qs - 1)**2 / (2 * K) - V(tau)) * A3
print("p_K + p_V =", sp.diff(Lf, A3), " (p_K = mu^2 (q-1)^2/2K, p_V = -V)")

# KA5 symbolic: with C = a^3 mu^2 (q-1)/K and dC/dt = -a^3 V'(tau) tau-dot? No: dC/dt = -a^3 V'(tau) (N=1).
# energy: d(a^3 rho)/dt + p d(a^3)/dt with tau-dot = q
q = sp.Function('q')(t)
rhoK = mu**2 * (q**2 - 1) / (2 * K); pK = mu**2 * (q - 1)**2 / (2 * K)
Vt = V(tau)
expr = sp.diff(a**3 * (rhoK + Vt), t) + (pK - Vt) * sp.diff(a**3, t)
# impose the charge equation: d/dt[a^3 mu^2 (q-1)/K] = -a^3 V'(tau), and tau-dot = q
qdot = sp.solve(sp.Eq(sp.diff(a**3 * mu**2 * (q - 1) / K, t), -a**3 * sp.diff(V(tau), t) / sp.diff(tau, t)), sp.diff(q, t))[0]
expr2 = expr.subs(sp.diff(q, t), qdot).subs(sp.diff(tau, t), q)
print("KA1c d(a^3 rho)/dt + p d(a^3)/dt on shell =", sp.simplify(expr2))
print("Integration by parts (Q ~ 1, tau = t + tau_i): C_final - C_i = -int a^3 V' dt = int V d(a^3) - [a^3 V]")
