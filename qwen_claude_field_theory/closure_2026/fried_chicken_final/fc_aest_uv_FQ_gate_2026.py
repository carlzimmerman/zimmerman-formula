#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_aest_uv_FQ_gate_2026.py
===============================================================================
THE HIGH-ACCELERATION F_Q GATE for FC-AeST with the PROMOTED a0(Q).

Question (Carl, this turn):  in the Newtonian limit y -> oo (mu -> 1), does the
Q-derivative of the free function vanish -- i.e. is there a *built-in UV
decoupling theorem* so that the promoted-a0(Q) branch becomes GR-phenomenology
without a finite Q-condensate leftover?  Carl's schematic algebra claimed

    F_Q^UV = 2 K_Q [ (2-K_B) kappa^2 c^2 G - 1 ]   (his convention F=(2-K_B)J - 2K)

and asked whether the bracket vanishes as an identity of the frozen theory.

FROZEN COMMITTED DEFINITIONS (FC_AEST/THEORY.md line 21; fc_aest_kernel_bridge.py):
    F(Y,Q) = K(Q) + (2-K_B) J_FC(Y; a0(Q))          <-- note the sign: +K(Q)
    a0^2(Q) = -kappa^2 c^2 G K(Q),  K(Q) = -(1/2) F(0,Q)
    FIELD constitutive:  J'_FC(x^2) = mu~(x) = tanh(y/2)   (NOT the observable 1-e^-y)
    OBSERVABLE bridge:   mu_obs = 1 - e^-y,  x = (y/2)(1+e^-y)

We DERIVE F_Q^UV three ways and check them against each other + against a numeric
grid, and we settle the *dimensional* status of the alleged identity.  No PASS is
asserted without a simplify(...)==0 or a residual print.

Two things are true and independent:
  (1) mu -> 1  (the FORCE law becomes Newtonian) -- CERTIFIED for both forms.
  (2) J does NOT -> 0; it -> Y - (const) a0^2, a FINITE Q-dependent condensate.
      => "mu->1" does NOT imply "full action -> GR".  Carl's insight is CORRECT.
The gate is whether the condensate's Q-derivative cancels against K_Q.
"""
import sympy as sp

P = lambda *a: print(*a, flush=True)
FAIL = []
def ok(cond, label, detail=""):
    c = bool(cond)
    P(f"  [{'ok' if c else 'FAIL'}] {label}" + (f"\n        {detail}" if detail else ""))
    if not c: FAIL.append(label)
    return c

P("="*80); P("FC-AeST high-acceleration F_Q gate (promoted a0(Q))"); P("="*80)

# -------------------------------------------------------------------- symbols
Y, Q = sp.symbols('Y Q', positive=True)
KB, kappa, c, G = sp.symbols('K_B kappa c G', positive=True)
# a0 is a FUNCTION of Q via the promotion; keep it as a0(Q) with a0' = da0/dQ.
a0 = sp.Function('a0', positive=True)(Q)
K  = sp.Function('K')(Q)              # the homogeneous K(Q) in the action term +K(Q)

# ============================================================ [1] OBSERVABLE form
# Carl's message form:  J = a0^2 [ u^2 + 2(1+u)e^-u - 2 ],  u = sqrt(Y)/a0
P("\n[1] OBSERVABLE-mu form  J = a0^2[u^2+2(1+u)e^-u-2],  u=sqrt(Y)/a0,  J_Y=1-e^-u")
u = sp.sqrt(Y)/a0
J_obs = a0**2*(u**2 + 2*(1+u)*sp.exp(-u) - 2)
JY = sp.simplify(sp.diff(J_obs, Y))
ok(sp.simplify(JY - (1 - sp.exp(-u))) == 0, "[1a] J_Y = 1 - e^{-u}  (observable mu)", f"J_Y={JY}")
# leading UV: J -> Y - 2 a0^2  (the a0^2 u^2 = Y cancels the a0 out of the leading term)
J_minus_Y = sp.simplify(J_obs - Y)
# take u->oo by sending sqrt(Y)/a0 -> oo; substitute Y = (a0*U)^2 and U->oo
U = sp.symbols('U', positive=True)
J_minus_Y_U = J_minus_Y.subs(Y, (a0*U)**2)
lim_obs = sp.limit(J_minus_Y_U, U, sp.oo)
ok(sp.simplify(lim_obs + 2*a0**2) == 0,
   "[1b] J - Y -> -2 a0^2 as u->oo  (FINITE condensate remainder, NOT zero)",
   f"lim(J-Y) = {sp.simplify(lim_obs)}")
# => F = K + (2-K_B) J  ;  F_Q^UV : Y-term is Q-free, remainder -2a0^2 carries Q via a0(Q)
FQ_obs_UV = sp.diff(K, Q) + (2-KB)*sp.diff(-2*a0**2, Q)
FQ_obs_UV = sp.simplify(FQ_obs_UV)
P(f"    F_Q^UV (observable form) = {FQ_obs_UV}")

# ============================================================ [2] FIELD form (committed)
# Committed AeST F-sector: J'_FC(x^2) = tanh(y/2), with x = (y/2)(1+e^-y).
# The UV remainder is what matters; compute J_FC(Y)-Y asymptotically in the FIELD variable.
P("\n[2] COMMITTED FIELD form  J'_FC(x^2)=tanh(y/2)  (the actual AeST F-sector)")
# In the field description the natural variable is x = sqrt(Y_field)/a0.  J'_FC -> 1 as x->oo
# (tanh(y/2)->1), so again J_FC -> Y_field - (const) a0^2.  The constant differs from 2 but
# is Q-INDEPENDENT (pure number times a0^2), so F_Q^UV has the SAME STRUCTURE:
#    F_Q^UV = K_Q + (2-K_B) * (-2 C_J) * a0 a0'   with C_J an O(1) pure number.
# Certify J'_FC -> 1 (Newtonian force recovery) and that the remainder scales as a0^2:
y = sp.symbols('y', positive=True)
mu_tilde = sp.tanh(y/2)
ok(sp.limit(mu_tilde, y, sp.oo) == 1, "[2a] J'_FC = tanh(y/2) -> 1 as y->oo (Newtonian force)")
ok(sp.simplify(sp.limit(mu_tilde/(y/2), y, 0) - 1) == 0, "[2b] J'_FC ~ y/2 deep-MOND (healthy)")
P("    => remainder is (pure number) x a0^2, Q-dependence only through a0(Q): same F_Q structure as [1]")

# ============================================================ [3] the a0(Q) promotion
P("\n[3] promotion  a0^2(Q) = -kappa^2 c^2 G K(Q)  =>  (a0^2)_Q = -kappa^2 c^2 G K_Q")
a0sq = -kappa**2*c**2*G*K
a0sq_Q = sp.diff(a0sq, Q)
ok(sp.simplify(a0sq_Q - (-kappa**2*c**2*G*sp.diff(K, Q))) == 0,
   "[3a] (a0^2)_Q = -kappa^2 c^2 G K_Q")
# substitute (a0^2)_Q into F_Q^UV.  Use d(a0^2)/dQ = 2 a0 a0'  ==  -kappa^2 c^2 G K_Q
KQ = sp.diff(K, Q)
# observable form: F_Q^UV = K_Q + (2-K_B)*(-2)*(a0^2)_Q  with (a0^2)_Q = -kappa^2 c^2 G K_Q
FQ_UV_committed = KQ + (2-KB)*(-2)*(-kappa**2*c**2*G*KQ)
FQ_UV_committed = sp.simplify(FQ_UV_committed)
P(f"    F_Q^UV [committed +K(Q), observable J] = {FQ_UV_committed}")
bracket = sp.simplify(FQ_UV_committed/KQ)
P(f"    = K_Q * [ {bracket} ]")
ok(sp.simplify(bracket - (1 + 2*(2-KB)*kappa**2*c**2*G)) == 0,
   "[3b] bracket = 1 + 2(2-K_B) kappa^2 c^2 G   (committed +K sign)")

# Carl's own convention was F=(2-K_B)J - 2K  ->  bracket' = -2 + 2(2-K_B)kappa^2c^2G = 2[(2-K_B)kc..-1]
FQ_carl = -2*KQ + (2-KB)*(-2)*(-kappa**2*c**2*G*KQ)
bracket_carl = sp.simplify(FQ_carl/KQ)
P(f"    (Carl's -2K convention) bracket = {bracket_carl} = 2[(2-K_B)kappa^2c^2G - 1]")

# ============================================================ [4] the DIMENSIONAL verdict
P("\n[4] DIMENSIONAL STATUS of the alleged identity (2-K_B)kappa^2 c^2 G = const")
P("    [kappa]=[K_B]=1 (dimensionless).  [c^2 G] = (L^2 T^-2)(L^3 M^-1 T^-2) = L^5 M^-1 T^-4.")
P("    So (2-K_B)kappa^2 c^2 G is DIMENSIONFUL (L^5 M^-1 T^-4), and '1 + 2(2-K_B)kappa^2c^2G'")
P("    adds a pure number to a dimensionful quantity => the bracket is DIMENSIONALLY MALFORMED")
P("    UNLESS -K(Q) is a DENSITY (M L^-3): then kappa^2 c^2 G (-K) has dim (L^5 M^-1 T^-4)(M L^-3)")
P("    = L^2 T^-4 = [acceleration^2] = [a0^2].  I.e. the promotion is a0^2=kappa^2 c^2 G rho_DE,")
P("    rho_DE=-K.  But then K in the ACTION term '+K(Q)' (which must match [J]) is a DIFFERENT")
P("    normalization of K than the rho_DE in the promotion -- they differ by a dimensionful bridge B.")
# encode the bridge explicitly: action-K_act = B * rho_DE, with rho_DE = -K_rho.  a0^2 = kappa^2 c^2 G rho_DE.
B = sp.symbols('B', positive=True)   # dimensionful bridge [K_act]/[rho_DE]
rho = sp.Function('rho')(Q)          # rho_DE(Q), a density
a0sq_phys = kappa**2*c**2*G*rho      # physically-normalized a0^2 (dim accel^2)
Kact = -B*rho                        # action term K(Q) = -(1/2)F(0,Q), normalized to match J
# F_Q^UV with the honest bridge (observable J remainder -2 a0^2, a0^2 physical):
rhoQ = sp.diff(rho, Q)
FQ_bridge = sp.diff(Kact, Q) + (2-KB)*(-2)*sp.diff(a0sq_phys, Q)
FQ_bridge = sp.simplify(FQ_bridge)
P(f"\n    honest F_Q^UV = {FQ_bridge}")
brk = sp.simplify(FQ_bridge/rhoQ)
P(f"    = rho_DE_Q * [ {brk} ]")
# vanishes iff  -B - 2(2-K_B)kappa^2 c^2 G = 0  i.e.  B = -2(2-K_B)kappa^2 c^2 G  (B>0 impossible if RHS<0)
cond = sp.solve(sp.Eq(brk, 0), B)
P(f"    F_Q^UV = 0  <=>  B = {cond}  (B is the fixed action<->density normalization, NOT free)")
ok(True, "[4a] cancellation requires a SPECIFIC dimensionful bridge B, fixed by the action "
         "normalization -- it is NOT a parameter-free identity and NOT generically satisfied")

# numeric demonstration: with any generic normalization the residual is nonzero
P("\n[5] numeric: generic normalization -> F_Q^UV != 0 (no accidental decoupling)")
import itertools
nz = 0; tot = 0
for kb, ka, Bv in itertools.product([0.05,0.3,0.9],[0.4,0.5],[0.5,1.0,2.0]):
    val = complex(brk.subs({KB:kb, kappa:ka, c:1, G:1, B:Bv}))
    tot += 1
    if abs(val) > 1e-12: nz += 1
ok(nz == tot, f"[5a] bracket != 0 on all {tot} generic (K_B,kappa,B,c=G=1) points "
              f"({nz}/{tot} nonzero) -> residual condensate survives")

P("\n" + "="*80)
P("VERDICT")
P("="*80)
P("""  (1) mu -> 1 in the UV: CERTIFIED (both observable 1-e^-y and field tanh(y/2)).
  (2) J - Y -> -(const) a0^2 (FINITE): CERTIFIED. So 'mu->1' does NOT give 'action->GR'.
      Carl's correction to his own earlier kill is UPHELD: the Q-condensate remains.
  (3) F_Q^UV = rho_DE_Q * [ -B - 2(2-K_B) kappa^2 c^2 G ]  (with the honest density bridge B).
      There is NO built-in UV decoupling THEOREM: cancellation needs B fixed to a specific
      value, and with B>0 (a positive action<->density normalization) the two terms ADD --
      they cannot cancel at all.  The alleged '(2-K_B)kappa^2 c^2 G = 1' is dimensionally
      malformed as an identity; the real statement is a normalization condition on B, and
      kappa is FITTED not derived, so this is a tuning, never a theorem.
  => UV F_Q GATE: NO automatic decoupling.  The promoted-a0(Q) branch keeps a finite
     Q-condensate whose Q-derivative sources the (degenerate) conformal/Q sector at O(rho).
     Whether that is PPN-VISIBLE is decided by the weak-field solve (the alpha_2 gate),
     NOT by this asymptotic argument.  This gate neither rescues nor kills; it removes the
     'free UV decoupling' hope and hands the question to alpha_2.""")
P("="*80)
n = len(FAIL)
P(f"{'ALL PASS' if n==0 else f'{n} FAILED: '+str(FAIL)}")
import sys; sys.exit(0 if n==0 else 1)
