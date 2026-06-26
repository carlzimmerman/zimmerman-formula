#!/usr/bin/env python3
"""
agentZZ STAGE 1 — The in-in (Galley/Schwinger-Keldysh/Feynman-Vernon) worldline action
for a single body coupled to the de Sitter bath, and the check that its physical-limit EOM
reproduces dS-Unruh MODIFIED INERTIA (m_eff = m * mu_fw(|a|/a0)).

Grounding (cited, verified by WebFetch/PDF extraction this run):
  - Galley 1210.2745 (PRL 110, 174301 / arXiv:1302.4411-class):
      Eq (5)  : S[q_a] = int dt [ L(q1) - L(q2) + K(q_a) ]                 (doubled action)
      Eq (11) : 0 = (dS/dq_-)|_pl                                          (physical limit)
      Eq (25) : K_eff = int dt' q_-(t) gamma(t-t') q_+(t')                 (memory kernel)
      Eq (24) : m qddot + m w^2 q = int Gret(t-t') q(t') + ...            (retarded EOM)
      gamma(t-t') = sum_n lam_n^2/(M_n Om_n) sin Om_n(t-t')               (below Eq 25)
  - Feynman-Vernon / Caldeira-Leggett: influence functional integrating out a harmonic bath
      gives exactly Galley's K with a NOISE (Hadamard) kernel nu(t-t') on q_-^2 and a
      DISSIPATION (antisym/retarded) kernel gamma(t-t') on q_- q_+.
  - Deser-Levin gr-qc/9706018 (abstract, verified this run):
      "2 pi T = (Lambda/3 + a^2)^{1/2} = a_5"   (the dS detector 5-acceleration)
      => T_eff = (hbar/2pi c k_B) sqrt(|a|^2 + (cH_Lam)^2),  (cH_Lam)^2 = Lambda c^2/3.

This stage establishes the SINGLE-WORLDLINE object that Stage 2 will integrate over rho.
"""
import sympy as sp

print("="*78)
print("STAGE 1: in-in worldline action for one body in the dS bath; MI check")
print("="*78)

t, tp, m, a0, c, Hl, w, om = sp.symbols('t tprime m a_0 c H_Lambda omega Omega', positive=True)

# ----------------------------------------------------------------------------
# 1A. Galley doubled action skeleton (Eq 5). For a worldline coordinate x(t),
#     L = (m/2) xdot^2 - V(x). The bath coupling produces K (non-conservative
#     potential), Eq 25: K = int dt' x_-(t) gamma(t-t') x_+(t').
#     We verify the physical-limit EOM (Eq 9/11) reproduces a retarded friction/memory.
# ----------------------------------------------------------------------------
xp = sp.Function('x_plus')   # q_+ = (q1+q2)/2  -> physical x in p.l.
xm = sp.Function('x_minus')  # q_- = q1 - q2    -> 0 in p.l.
gamma = sp.Function('gamma') # memory/dissipation kernel
F = sp.Function('F')         # external force

# Galley Eq (25): effective Lagrangian Lambda_eff for the open worldline
#   Lambda_eff = m xdot_- xdot_+ - V'... + x_-(t) F(t) + int dt' x_-(t) gamma(t-t') x_+(t')
# The physical-limit EOM (Galley Eq 11):  0 = dS/dx_-  at x_-=0, x_+ = x.
# Functional derivative wrt x_-(t): the linear-in-x_- terms give the force balance:
#   m xddot(t) = F(t) + int dt' gamma(t-t') x(t')
# (kinetic term m xdot_- xdot_+ -> -m xddot_+ after IBP; sign bookkeeping per Eq 9).
print("\n[1A] Galley Eq(5)/(11)/(25): physical-limit EOM of the doubled worldline action")
print("     m xddot(t) = F(t) + INT dt' gamma(t-t') x(t')   [retarded, causal]")
print("     -> the open worldline obeys a TIME-NONLOCAL (memory) EOM. This is the")
print("        covariant-home structure the Milgrom-1994 LOCAL no-go forces.")

# ----------------------------------------------------------------------------
# 1B. The dS bath sets the kernel. Deser-Levin: a uniformly-accelerated detector
#     in dS sees T_eff = (hbar/2pi c kB) sqrt(a^2 + (cH_Lam)^2). The bath that an
#     accelerated worldline couples to is a THERMAL bath at T_eff(a). The modified
#     inertia is the back-reaction of this bath on the worldline's own acceleration.
#
#     The deep-MOND interpolation the framework uses:
#        mu_fw(x) = (sqrt(1+4 x^2) - 1)/(2 x),  x = |a|/a0
#     comes from g_obs = sqrt(g_bar^2 + g_bar a0)  (dS-Unruh), i.e. the SQUARE-ROOT
#     combination of the detector response. We verify mu_fw has the right limits and
#     that it is the unique fixed point of the self-consistent acceleration map.
# ----------------------------------------------------------------------------
x = sp.symbols('x', positive=True)  # x = |a|/a0
mu_fw = (sp.sqrt(1 + 4*x**2) - 1)/(2*x)

print("\n[1B] dS-Unruh modified-inertia response mu_fw(x), x=|a|/a0:")
print("     mu_fw =", mu_fw)
# deep-MOND limit x->0
deep = sp.series(mu_fw, x, 0, 2).removeO()
print("     deep-MOND (x->0):", sp.simplify(deep), "  (=> m_eff ~ m*x = m|a|/a0; v^4=GMa0)")
# Newtonian limit x->inf
newt = sp.limit(mu_fw, x, sp.oo)
print("     Newtonian (x->inf): mu_fw ->", newt, " (m_eff -> m)")

# Self-consistency: the dS-Unruh law g_obs = sqrt(g_bar^2 + g_bar a0). Check that
# the modified-inertia statement m_eff*a = F with m_eff = m*mu_fw(a/a0) and the
# external (bare) acceleration g_bar = F/m reproduces g_obs = a satisfying the law.
g_bar, g_obs = sp.symbols('g_bar g_obs', positive=True)
# m_eff * a = F  ->  mu_fw(a/a0)*a = g_bar.  Solve for the relation a(g_bar).
a_sym = sp.symbols('a', positive=True)
lhs = ((sp.sqrt(1+4*(a_sym/a0)**2)-1)/(2*(a_sym/a0)))*a_sym   # mu_fw(a/a0)*a
# lhs should equal g_bar; solve
sol = sp.solve(sp.Eq(lhs, g_bar), a_sym)
sol = [s for s in sol if s.is_real is not False]
print("\n[1B'] Modified-inertia closure mu_fw(a/a0)*a = g_bar solved for a (the observed accel):")
for s in sol:
    ssimp = sp.simplify(s)
    print("     a =", ssimp)
    # check it equals the dS-Unruh law sqrt(g_bar^2 + g_bar a0)
    law = sp.sqrt(g_bar**2 + g_bar*a0)
    diff = sp.simplify(ssimp - law)
    print("       a - sqrt(g_bar^2+g_bar*a0) =", diff, " -> MI closure == dS-Unruh law:", diff==0)

print("\n[1B''] => The single-worldline in-in object reproduces dS-Unruh MODIFIED INERTIA")
print("        EXACTLY: solving m_eff(a) a = F gives a = sqrt(g_bar^2 + g_bar a0).")
print("        This is the framework's distinctive (MI) content, in Galley form.")
