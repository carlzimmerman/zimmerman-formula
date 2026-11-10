"""R541A GA1 (background) and GA5 (constraint preservation, signs).

Minisuperspace of action (A) with P = 0 (F = W = 0), dust baryons, and the clock-matter couplings
  (i)  -alpha rho_b f(Q),  f in {Q-1, (Q-1)^2, ln Q}
  (ii) beta (Q-1) T, T = -rho_b for dust (radiation traceless) -> identical to (i) with f = Q-1, alpha = beta.
Units c = 1, K = 4 pi G, M0 = mu_K^2/K. Lagrangian L = L_grav + N a^3 G(Q, a),
  G(Q, a) = M0 (Q-1)^2/2 - rho_b(a) (1 + alpha f(Q)),  rho_b = rho_b0 / a^3,  Q = taudot / N.
Output: ga1_background.out (same folder).
"""
import os, sys
import sympy as sp
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
out = open(os.path.join(HERE, "ga1_background.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.write(s + "\n")

t = sp.symbols('t')
K, mu, Lam, C, rb0, al, q = sp.symbols('K mu_K Lambda C rho_b0 alpha q', positive=True)
N = sp.Function('N')(t); a = sp.Function('a')(t); tau = sp.Function('tau')(t)
Q = sp.diff(tau, t) / N
M0 = mu**2 / K
fs = {"(i-a) f=Q-1": lambda Q: Q - 1, "(i-b) f=(Q-1)^2": lambda Q: (Q - 1)**2, "(i-c) f=ln Q": lambda Q: sp.log(Q)}

def lag(f, alpha):
    Lg = (-6*a*sp.diff(a, t)**2/N - 2*Lam*N*a**3) / (4*K)
    G = M0*(Q - 1)**2/2 - (rb0/a**3)*(1 + alpha*f(Q))
    return Lg + N*a**3*G

P("# R541A GA1 background + GA5 constraint check")
P("## KA (alpha = 0): record first integral and density")
L0 = lag(fs["(i-a) f=Q-1"], 0)
p0 = sp.simplify(sp.diff(L0, sp.diff(tau, t)).subs(N, 1))
P("  tau cyclic:", sp.diff(L0, tau) == 0, "; p_tau =", p0)
x = sp.symbols('x')
G0 = M0*(q - 1)**2/2
rho0 = sp.simplify(q*sp.diff(G0, q) - G0)
Qs = 1 + C*K/(mu**2*a**3)
P("  rho_K(alpha=0) on shell =", sp.expand(rho0.subs(q, Qs)), "  (record: C/a^3 + K C^2/(2 mu_K^2 a^6))  ->",
  sp.simplify(rho0.subs(q, Qs) - (C/a**3 + K*C**2/(2*mu**2*a**6))) == 0)

P("\n## First integrals with the couplings (shift symmetry tau -> tau + c survives: L depends on taudot only)")
qa = sp.symbols('qa', positive=True)
for name, f in fs.items():
    L = lag(f, al)
    cyc = sp.diff(L, tau) == 0
    pt = sp.simplify(sp.diff(L, sp.diff(tau, t)).subs(N, 1).subs(sp.diff(tau, t), q))
    P(f"  {name}: tau cyclic {cyc}; a^3 G'(Q) = p_tau = {sp.simplify(pt)} = C (C an integration constant)")

P("\n## Energy density (Hamiltonian constraint): rho_tot = Q dG/dQ - G (checked against -dL/dN / a^3)")
for name, f in fs.items():
    L = lag(f, al)
    rho_from_N = sp.simplify((-sp.diff(L - (-6*a*sp.diff(a, t)**2/N - 2*Lam*N*a**3)/(4*K), N)/a**3)
                             .subs(N, 1).subs(sp.diff(tau, t), q))
    rb = sp.symbols('rho_b', positive=True)
    G = M0*(q - 1)**2/2 - rb*(1 + al*f(q))
    rho_formula = sp.simplify(q*sp.diff(G, q) - G)
    chk = sp.simplify(rho_from_N.subs(rb0, rb*a**3) - rho_formula)
    P(f"  {name}: rho_tot = {sp.simplify(rho_formula)}   (residual vs dL/dN: {chk})")

P("\n## GA5: Friedmann constraint preserved by the equations (N = 1 gauge), alpha generic, f = Q-1 and ln Q")
for name in ["(i-a) f=Q-1", "(i-c) f=ln Q"]:
    f = fs[name]
    L = lag(f, al)
    # Euler-Lagrange for a and tau, constraint dL/dN
    EL = lambda y: sp.diff(sp.diff(L, sp.diff(y, t)), t) - sp.diff(L, y)
    Ea = EL(a).subs(N, 1).doit(); Et = EL(tau).subs(N, 1).doit(); Hc = sp.diff(L, N).subs(N, 1).doit()
    dH = sp.diff(Hc, t)
    s_a, s_ad, s_add, s_td, s_tdd = sp.symbols('s_a s_ad s_add s_td s_tdd')
    def S(e):
        e = e.subs({sp.diff(a, t, 2): s_add, sp.diff(tau, t, 2): s_tdd})
        e = e.subs({sp.diff(a, t): s_ad, sp.diff(tau, t): s_td})
        return e.subs(a, s_a)
    sol = sp.solve([S(Ea), S(Et)], [s_add, s_tdd], dict=True)[0]
    syms = {K: 0.7, mu: 1.3, Lam: 0.2, rb0: 0.4, al: 0.6}
    av, tdv = 1.1, 1.25
    Hn = S(Hc).subs(syms).subs({s_td: tdv, s_a: av})
    adv_s = sp.nsolve(Hn, s_ad, 0.8)
    val = S(dH).subs(sol).subs(syms).subs({s_td: tdv, s_ad: adv_s, s_a: av})
    P(f"  {name}: H constraint at the point = {sp.N(Hn.subs(s_ad, adv_s), 3)}; d/dt(constraint) on shell = {sp.N(val, 6)}")
    syms0 = dict(syms); syms0[al] = 0
    Hn0 = S(Hc).subs(syms0).subs({s_td: tdv, s_a: av}); ad0 = sp.nsolve(Hn0, s_ad, 0.8)
    val0 = S(dH).subs(sol).subs(syms0).subs({s_td: tdv, s_ad: ad0, s_a: av})
    P(f"    KA alpha = 0 (GR + dust + khronon): d/dt(constraint) = {sp.N(val0, 6)}")

# ---------- numbers ----------
P("\n## Numbers. I0 = 4.037e-8 Mpc^-2 = 2 K rho_d0 (MK1 row 1); K rho_b0 = I0 / (2 R)")
I0 = 4.037e-8
for foot, R in [("canonical", 5.410), ("alt", 5.412)]:
    Krb0 = I0/(2*R)
    P(f"\n### footing {foot}: R target {R}, K rho_b0 = {Krb0:.4e} Mpc^-2")
    # naive background split for f = Q-1 under Z_can: baryon (1-alpha) rho, clock-own alpha rho -> R_naive = alpha/(1-alpha)
    al_need = R/(1 + R)
    P(f"  f=Q-1 / (ii), Z_can, NAIVE background split clock-own/baryon = alpha/(1-alpha) -> alpha = {al_need:.5f}")
    for muK in [198.0, 2.51e4, 8.9e6]:
        P(f"  mu_K = {muK:g} /Mpc:")
        for name in ["(i-a) f=Q-1", "(i-b) f=(Q-1)^2", "(i-c) f=ln Q"]:
            rows = []
            for aa in [1e-9, 1e-6, 1e-3, 1.0]:
                y = Krb0/(muK**2*aa**3)   # rho_b / M0
                A = al_need
                # Z_can: G'(Q) = 0 -> (Q-1) = A y f'(Q)
                if name.startswith("(i-a)"):
                    xz = A*y; Qz = 1 + xz; fp = 1.0; fQ = xz
                elif name.startswith("(i-b)"):
                    xz = 0.0; Qz = 1.0; fp = 0.0; fQ = 0.0   # Q=1 is the stationary point (unique while 1 - 2 A y > 0)
                else:
                    xz = 2*A*y/(1 + np.sqrt(1 + 4*A*y)); Qz = 1 + xz; fp = 1/Qz; fQ = np.log1p(xz)
                clock_own = xz*(2 + xz)/2/y            # M0 (Q^2-1)/2 in units of rho_b
                inter = -A*(Qz*fp - fQ)                # Q dG_c/dQ - G_c for G_c = -rho alpha f : -alpha (Q f' - f)
                bary = 1.0                              # rho_b (1) from the -rho_b term
                tot_extra = clock_own + inter - A*fQ*0  # extra over bare rho_b
                locked = A*fp                           # E / rho_b: induced charge locked to baryons (GA2)
                sigma = 0.0                             # free charge = C_can = 0 under Z_can
                rows.append((aa, xz, clock_own, inter, clock_own + inter, locked, sigma))
            P(f"    {name}: a | Q-1 | clock-own/rho_b | interaction/rho_b | extra total/rho_b | locked E/rho_b | R_cold")
            for r in rows:
                P("      " + " | ".join(f"{v:.4g}" for v in r))
        # (i-b) sign flip of the clock kinetic coefficient M0 - 2 alpha rho_b
        aflip = (2*al_need*Krb0/muK**2)**(1/3)
        P(f"    (i-b) M0 - 2 alpha rho_b changes sign at a = {aflip:.3e} (alpha {al_need:.3f}): clock kinetic coefficient negative earlier")
    P("  Z_K reading (clock-own charge a^3 M0 (Q-1) = 0 -> Q = 1): f=Q-1 and ln Q: canonical charge C = -alpha rho_b0 f'(1);"
      " free charge sigma = C = -alpha rho_b0 -> R_cold = -alpha < 0; (Q-1)^2: sigma = 0 -> R_cold = 0")
    P(f"  MU (free reading C = {R} rho_b0, alpha = 0 and alpha = {al_need:.3f}): late R = C/rho_b0 = {R} for both alpha"
      " (alpha enters only at O(alpha rho_b/M0) and through the locked part)")
out.close()
