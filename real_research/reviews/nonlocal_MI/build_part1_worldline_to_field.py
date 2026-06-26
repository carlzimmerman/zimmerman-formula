#!/usr/bin/env python3
"""
THE IN-IN WORLDLINE MI ACTION  ->  COARSE-GRAIN  ->  AeST ?
===========================================================
PART 1 of 3: build the Galley/in-in worldline MI action, take its physical-limit
EOM, and perform the worldline->field coarse-graining. Then PART 2 matches against
the AeST action term-by-term; PART 3 does the active<->passive truncation + Cassini.

VERIFIED PRIMARIES (text cached in this dir):
  GALLEY (1210.2745, PRL 110 174301):
    eq (5):  S[q_a] = int dt [ L(q1,qd1) - L(q2,qd2) + K(q_a,qd_a,t) ]   (doubled action)
    eq (6):  Lambda = L(q1)-L(q2)+K                                       (new Lagrangian)
    eq (11): EOM <=> delta S/delta q_-  |_{p.l.} = 0  ; q_- = q1-q2, q_+ = (q1+q2)/2,
             q_- -> 0, q_+ -> q in the physical limit; only terms LINEAR in q_- give forces.
    eq (19): dh/dt = -(dL/dt) - qd.( d/dt dK/dqd_- - dK/dq_- )|_p.l.  (energy NON-conservation set by K)
    eq (20): example  Lambda = m xd_-.xd_+ - alpha x_-.xd_+ |xd_+|^{n-1}  (K = the drag/dissipation term)
  AeST (2007.00082, PRL 127 161302):
    eq (5):  S = int d4x sqrt(-g)/(16pi Gt) [ R - (K_B/2)F^2 + 2(2-K_B) J.grad phi
                                              - (2-K_B) Y - F(Y,Q) - lambda(A^2+1) ] + S_m
             F_{mu nu}=2 grad_[mu A_nu], J^mu = A^a grad_a A^mu, Q = A^mu grad_mu phi,
             Y = q^{mu nu} grad_mu phi grad_nu phi, q^{mu nu}=g^{mu nu}+A^mu A^nu (A-orthogonal).
    deep-MOND:  J(Y) -> (2 lambda_s /(3(1+lambda_s) a0)) Y^{3/2}  as grad phi -> 0.  a0 appears HERE.
    eq (6):  weak-field quasistatic reduction -> AQUAL + a mu^2 Phi^2 mass term.

Everything below is CONSTRUCTED here (sympy) or CITED (marked). Both ways: the test
is whether the coarse-grained worldline EFT IS AeST; if it is not, say so.
"""
import sympy as sp

print("="*80)
print(" STAGE A.  The dS-Unruh MODIFIED-INERTIA worldline action (the framework's pillar 1)")
print("="*80)
print("""
The framework's MI premise (CITED, framework corpus + Deser-Levin gr-qc/9706018):
  A worldline with u-frame proper acceleration a in de Sitter reads an effective temperature
     T_eff = (hbar/2 pi c k_B) sqrt(|a|^2 + (c H_Lambda)^2)              [Deser-Levin, dS detector]
  and its inertia is MODIFIED:  m -> m * mu_fw(|a|/a0),
     mu_fw(x) = (sqrt(1+4x^2) - 1)/(2x),   a0 = c^2 sqrt(Lambda/32pi).
  Deep-MOND (x<<1):  mu_fw -> x = |a|/a0   =>  m a^2/a0  force law  =>  v^4 = G M a0.
This response is MODIFIED INERTIA (the kinetic term, not the potential) and Milgrom-1994
(astro-ph/9303012) proved NO LOCAL Galilei-invariant action reproduces both limits =>
the covariant home must be NONLOCAL-in-time. Galley (1210.2745) is the variational engine
for exactly such an action: a worldline functional that is (a) initial-value/causal,
(b) able to host non-potential ("active") generalized forces through K.
""")

# Symbols
t, tp, s = sp.symbols('t t_prime s', real=True)
m, a0, c, HL = sp.symbols('m a_0 c H_Lambda', positive=True)
om = sp.symbols('omega', real=True)

print("-"*80)
print(" A.1  The doubled (in-in) worldline action for MI.  CONSTRUCTED.")
print("-"*80)
print("""
Write the worldline position x^i(t) (u-frame spatial, weak field). The free piece is the
ordinary kinetic Lagrangian L = (m/2)|xd|^2. The MI content is a NON-POTENTIAL generalized
force => it lives ENTIRELY in Galley's K (eq 5), the doubled non-conservative potential:

  S[x_1,x_2] = int dt [ (m/2)|xd_1|^2 - (m/2)|xd_2|^2 + K(x_a, xd_a; t) ]          (Galley eq 5)

The MI kernel K is the time-nonlocal object. The minimal causal form (a retarded memory
kernel acting on the u-frame acceleration history), in Galley's +/- variables, is

  K = - x_-^i(t) * int_{-inf}^{t} dt' gamma(t-t') xdd_+^i(t')                       (*)

This is the worldline analog of Galley eq (20)'s K = -alpha x_-.xd_+|xd_+|^{n-1}: linear in
x_- (so it produces a physical force, eq 11), retarded (causal), and history-dependent
(nonlocal). gamma(t-t') is the response/memory kernel = the dS-Unruh inertia-dressing kernel.
""")

# Physical-limit EOM from (*). In freq space, with x_- linear (Galley eq 11):
#   delta S / delta x_-(t) |p.l.  ->  m xdd(t) + int dt' gamma(t-t') xdd(t') = F(t)
# i.e. the inertia is dressed:  m_eff(omega) = m + gamma_hat(omega).
gh = sp.Function('gamma_hat')(om)
print("Physical-limit EOM (Galley eq 11 applied to L+K, freq space):")
print("   [ m + gamma_hat(omega) ] * (-omega^2) x_hat(omega) = F_hat(omega)")
print("   => m_eff(omega) = m + gamma_hat(omega)   (the DRESSED, frequency-dependent inertia)")
print("""
   For deep-MOND, the MI law needs m_eff to DROP at low |a| (low characteristic omega):
   m_eff -> m * mu_fw(|a|/a0) with mu_fw -> |a|/a0 << 1. The kernel gamma_hat must therefore
   carry the a0 scale and the sqrt-acceleration nonlinearity (mu_fw is NONLINEAR in a) =>
   gamma is a NONLINEAR, history-dependent, retarded kernel. CONSTRUCTED (form), with the
   nonlinearity inherited from mu_fw (framework corpus, Deser-Levin-anchored).
""")

print("-"*80)
print(" A.2  Energy non-conservation (Galley eq 19): the action is ACTIVE.  CONSTRUCTED.")
print("-"*80)
# Galley eq 19: dh/dt = -(dK/dt-piece). For the retarded kernel (*), compute the secular drain.
print("""
Galley eq (19): dh/dt = - qd . ( d/dt dK/dqd_- - dK/dq_- )|_p.l.   (energy flux SET BY K).
For a strictly RETARDED kernel (causal), the time-symmetric part vanishes and the
time-ANTISYMMETRIC part gives a NON-ZERO secular dh/dt: the worldline EXCHANGES energy with
the (dS) bath. Sign: for deep-MOND the inertia is REDUCED at low a => the kernel must inject
'negative dissipation' (the worldline gains effective response) = an ACTIVE kernel.
This is the framework's banked Theorem X2 (passivity no-go): causality + vacuum passivity
force m_eff(0) >= m_eff(inf) (anti-MOND); the MOND inversion m_eff(0) < m_eff(inf) requires
an ACTIVE (pumped, dS-bath) kernel. So the in-in worldline MI action is ACTIVE + NONLOCAL,
by construction. (banked: agentZZ_galley_active_bath.py, Theorem X2.)
""")

print("="*80)
print(" STAGE B.  WORLDLINE -> FIELD coarse-graining (the actual new calculation)")
print("="*80)
print("""
The conjecture: coarse-graining the in-in worldline MI dynamics over a continuum of
worldlines (a fluid of test bodies) gives a FIELD theory, and that field theory is AeST.
The standard worldline->field map (Mathisson-Papapetrou / kinetic-theory / hydrodynamic
coarse-graining): a congruence of worldlines with 4-velocity field u^mu(x) and a collective
phase phi(x) whose gradient encodes the coarse-grained MI response.

DICTIONARY TO TEST (the charge):
  (D1) u^mu(x) = coarse-grained worldline 4-velocity = the dS-bath preferred frame
       <->  AeST unit-timelike aether A^mu  (A^mu A_mu = -1).
  (D2) phi(x)  = collective coarse-grained MI field (the 'potential' whose gradient is the
       MI response)  <->  AeST shift-symmetric scalar phi.
  (D3) the deep-MOND limit of the worldline kernel  <->  AeST's Y^{3/2} term (a0 enters here).
  (D4) the active/nonlocal kernel  <->  AeST's passive/local action as the leading truncation.

Build the coarse-grained Lagrangian and test each.
""")
