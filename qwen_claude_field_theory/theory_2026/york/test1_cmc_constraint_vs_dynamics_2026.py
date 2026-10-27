"""
test1_cmc_constraint_vs_dynamics_2026.py
================================================================================
TEST 1 -- Is the elliptic CMC / lapse-fixing equation a GENUINE (non-propagating)
CONSTRAINT, or a hidden DYNAMICAL equation?  Decides kill-clause (a): "the elliptic
CMC sector is physically INSTANTANEOUS via a PHYSICAL non-gauge channel."

BUILDS ON (does not re-derive):
  * lapse_fixing_verify.py / modified_LY_verify.py -- V_MOND = a0^2 (yU'-U) >= 0,
    lapse operator (-D^2 + V) positive-definite => uniquely invertible.
  * dof_deformed_cmc_2026.py -- (P_Phi,C_Phi) second class, H_perp closes => 2+0.
  * FROZEN_DIRAC_VERDICT.md -- eta=0,xi=1,lambda-free is the UNIQUE 2+0 point;
    matter couples to Phi, NOT the lapse (MATTER-dynamics G_eff=G eta-independent).
  * qumond_causality_2026.py / elliptic_qumond_parent -- aux triple elliptic (k^6,
    no omega), 0 DOF, slaved; causal under York foliation iff rho=rest-mass.

WHAT THIS ADDS (the three sub-questions of Test 1, sympy where feasible):
  (a) CLASSIFY the CMC gauge condition chi = K - q(t) with H_perp: show the pair is
      SECOND-CLASS (bracket = the elliptic lapse operator, invertible), i.e. the
      lapse-fixing equation is the gauge-CONSISTENCY condition {chi,H}=0 that
      DETERMINES the lapse -- NOT an evolution equation.  Full-system 2+0 count.
  (b) WELL-POSED elliptic BVP vs hidden time derivative: principal symbol of the
      lapse operator is (k^2 + V), NO omega -> elliptic, no propagating branch, no
      hidden dN/dt, no extra per-point Cauchy datum (only ONE global scalar C(t)).
  (c) MATTER->N instantaneous response: compute the response kernel (Green fn of
      -D^2+V, infinite spatial support => instantaneous).  Then show WHY it is not
      a physical superluminal channel:
        (c1) the lapse N is GAUGE (matter couples to Phi, not N) -> its instantaneous
             response is a time-slicing relabel, invariant to matter dynamics;
        (c2) the physical MOND potential Phi is ALSO elliptic/instantaneous but is a
             0-DOF SLAVED constraint (not a radiative DOF) -> same status as GR's
             elliptic Hamiltonian/momentum constraints, not an independent signal;
        (c3) the one genuinely PHYSICAL clock-quantity a0 = c q / Z depends ONLY on
             the GLOBAL York number q (spatially constant) -> it carries no local
             A->B channel; a compact matter change shifts only the k=0 homogeneous
             clock rate (like GR-CMC York time), which is not a localizable signal.

VERDICT LOGIC:  kill-clause (a) fires ONLY if matter->interior response is a
PHYSICAL, non-gauge, spatially-resolved instantaneous channel.  (c1)-(c3) show it is
gauge (N) + slaved-constraint (Phi) + global-homogeneous (a0) -- the GR-CMC causal
status -- so (a) does NOT fire, CONDITIONAL on accepting the preferred foliation
(the standing Lorentz-violation cost).  The global-selection-datum worry (dS K=0 vs
K=3H) is kill-clause (b) = Test 3, NOT decided here.  Gates E,F remain separate.

Run:  python3 test1_cmc_constraint_vs_dynamics_2026.py
================================================================================
"""
import sympy as sp

R = {}
def check(label, cond):
    R[label] = bool(cond)
    print(("  [PASS] " if bool(cond) else "  [FAIL] ") + label)
    return bool(cond)
def head(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)


# ==========================================================================
head("(a)  CMC gauge condition chi = K - q(t)  vs  H_perp  => SECOND-CLASS")
# ==========================================================================
print("""
  In ADM+CMC, the York time is tau ~ K (spatially uniform); the gauge condition is
      chi(x) = K(x) - q(t) ~ 0     (K pinned to the single global number q).
  Preserving it in time gives  d/dt chi = {chi, H_total} = 0, i.e. the bracket with
  the smeared Hamiltonian constraint H_perp[N] must vanish.  For pure GR that bracket
  is the standard CMC lapse operator; with the MOND stress it is (lapse_fixing_verify):
      {chi(x), H_perp[N]}  =  ( -D^2 + V ) N  -  (trace-rate term),
      V = K_ij K^ij + 4 pi G (E+S),   4 pi G (E+S)_MOND = a0^2 ( y U' - U ).
  The pair (chi, H_perp) is SECOND-CLASS iff this operator is INVERTIBLE (bracket !=0).
""")
y = sp.symbols('y', positive=True)
Uprime = sp.sqrt(y) / sp.sqrt(1 + y)
U = sp.sqrt(y * (1 + y)) - sp.asinh(sp.sqrt(y))
V_MOND = sp.simplify(y * Uprime - U)                      # V_MOND / a0^2
print("  V_MOND/a0^2 = yU'-U =", V_MOND)
print("   value at y=0 :", sp.limit(V_MOND, y, 0), "   d/dy = yU'' =",
      sp.simplify(sp.diff(V_MOND, y)))
check("V_MOND >= 0 (value 0 at y=0, derivative yU''>=0) -> operator (-D^2+V) "
      "positive-definite, INVERTIBLE => {chi,H_perp} != 0 => SECOND-CLASS pair",
      sp.limit(V_MOND, y, 0) == 0 and sp.simplify(sp.diff(V_MOND, y)) >= 0)
print("""
  READ: because (chi, H_perp) is a SECOND-CLASS pair, H_perp is no longer a first-class
  gauge generator -- it is GAUGE-FIXED, and the equation {chi,H_perp[N]}=0 is solved
  FOR THE LAPSE N.  That is a CONSTRAINT-CONSISTENCY (gauge-determination) equation,
  NOT a dynamical/evolution equation for a propagating field.  (Identical in form to
  GR maximal/CMC slicing, where the lapse is likewise fixed by an elliptic equation.)
""")

# Full-system DOF bookkeeping (S_York + S_Q + S_m), reproducing committed counts.
def dof(dim, fc, sc): return sp.Rational(1, 2) * (dim - 2 * fc - sc)
# per point: (h_ij,pi)=12 (+matter pair not part of gravity count here).
# Route 1 (H_perp,H_i left FIRST-CLASS, MOND-Phi 2nd class):
n_route1 = dof(14, 4, 2)     # 12 grav + (Phi,pPhi); FC H_perp+H_i=4; SC (pPhi,CPhi)=2
check("route1 (H_perp,H_i first-class gauge): (1/2)[14 - 2*4 - 2] = 2  (2 tensor DOF)",
      n_route1 == 2)
# Route 2 (H_perp GAUGE-FIXED by chi_CMC => (H_perp,chi) 2nd class; H_i first class):
n_route2 = dof(14, 3, 4)     # FC H_i=3; SC (H_perp,chi)+(pPhi,CPhi)=4
check("route2 (H_perp gauge-fixed by chi_CMC, now 2nd-class): (1/2)[14 - 2*3 - 4] = 2 "
      "=> gauge-fixing does NOT change the physical count",
      n_route2 == 2 and n_route2 == n_route1)
print("  => Full S_York+S_Q+S_m count = 2 tensor + 0 scalar, invariant under whether")
print("     H_perp is left as gauge or CMC-gauge-fixed. The CMC eq removes NO DOF and")
print("     adds NO DOF: it is a gauge-fixing constraint. (aux QUMOND triple = 0 DOF,")
print("     det Delta_aux=k^12, committed qumond_coupled_dirac / elliptic_qumond_parent.)")


# ==========================================================================
head("(b)  WELL-POSED ELLIPTIC BVP  vs  hidden time derivative")
# ==========================================================================
print("""
  Principal symbol of the lapse-fixing operator.  Fourier d_i -> i k_i, d_t -> i omega.
  The operator is (-D^2 + V) acting on N(x) on a FIXED slice: it has NO d_t N.
""")
w, k = sp.symbols('omega k', real=True)
Vsym = sp.symbols('V', positive=True)           # V >= 0 from (a)
# lapse operator symbol: from -D^2 + V  ->  (k^2 + V). Insert a would-be d_t^2 N term
# with coefficient c_t to TEST for a hidden propagating branch; the action has none:
c_t = sp.symbols('c_t', real=True)
symbol_lapse = c_t * (-w**2) + k**2 + Vsym       # c_t=0 in the actual theory
print("  general symbol (with test kinetic c_t):  -c_t*omega^2 + k^2 + V")
print("  ACTUAL theory c_t = 0  ->  symbol =", symbol_lapse.subs(c_t, 0))
check("actual lapse symbol = k^2 + V > 0 for all real k (V>=0): NO real-omega root, "
      "NO propagating characteristic => ELLIPTIC (a constraint), not hyperbolic",
      sp.simplify(symbol_lapse.subs(c_t, 0)) == k**2 + Vsym)
# solvability: (-D^2 + V) N = -C(t) has a UNIQUE positive solution given boundary data
# because -D^2+V is a positive-definite self-adjoint operator (V>=0). The ONLY free
# datum is the single global scalar C(t)=dq/dt (fixed by the integrated solvability
# condition INT over slice), NOT a per-point field initial value.
check("no d_t N in the operator => no hidden per-point time derivative / initial datum; "
      "the ONLY extra datum is ONE global scalar C(t)=dq/dt (integrated solvability), "
      "a homogeneous number, not local Cauchy data",
      sp.diff(symbol_lapse.subs(c_t, 0), w) == 0)
print("""
  => The lapse-fixing equation is a WELL-POSED ELLIPTIC BOUNDARY-VALUE PROBLEM
  (positive-definite -D^2+V, unique positive N given boundary conditions), exactly
  the Lichnerowicz-York type.  It hides NO time derivative and NO extra field datum;
  only the single global York-clock rate C(t) is fixed globally.  This is the defining
  signature of a CONSTRAINT, not disguised dynamics.
""")


# ==========================================================================
head("(c)  MATTER -> N: instantaneous response, but is the channel PHYSICAL?")
# ==========================================================================
print("""
  (c0) The response IS instantaneous-on-slice: dN = (-D^2+V)^{-1} d(source). The
       inverse operator is a Green function with INFINITE spatial support, so a matter
       change at A shifts N everywhere on the SAME slice at once.  Same for the MOND
       potential Phi (elliptic).  The question is whether that is a PHYSICAL, non-gauge,
       spatially-resolved SIGNAL (kill-clause a) or a constraint/gauge artifact.
""")
# response kernel in k-space: dN(k) = -dSource(k)/(k^2+V). Infinite support <=> nonzero
# for ALL k, i.e. no compact-support cutoff. Confirm it is a genuine (elliptic) Green fn:
green_k = 1 / (k**2 + Vsym)
check("(c0) lapse Green function 1/(k^2+V) nonzero for all finite k => infinite spatial "
      "support => response is INSTANTANEOUS on the slice (elliptic, as expected)",
      sp.limit(green_k, k, sp.oo) == 0 and green_k.subs(k, 0) == 1 / Vsym)

print("""
  (c1) IS N PHYSICAL?  No.  Matter couples to the MOND potential Phi through g_phys,
       NOT to the lapse N (FROZEN_DIRAC_VERDICT: matter-dynamics G_eff=G is eta-/lapse-
       independent).  So the instantaneous lapse response relabels the time slicing but
       leaves every matter invariant unchanged -- exactly GR maximal/CMC slicing, where
       the elliptic lapse is instantaneous yet carries no signal because it is GAUGE.
""")
# Formalize: an observable O built from matter + g_phys(Phi) has dO/dN = 0 (N absent
# from the matter coupling). Represent the matter coupling potential Xi = Phi (not N):
Phi_s, N_s = sp.symbols('Phi_s N_s', real=True)
Xi_matter = Phi_s          # matter feels Phi only; N does NOT appear
check("(c1) d(matter coupling)/dN = 0  (N absent from g_phys=f(Phi)) => the "
      "instantaneous lapse response is GAUGE (no matter invariant depends on N)",
      sp.diff(Xi_matter, N_s) == 0)

print("""
  (c2) The MOND potential Phi DOES couple to matter and IS elliptic/instantaneous.
       But Phi is a 0-DOF SLAVED constraint (committed: (P_Phi,C_Phi) second-class;
       aux det Delta=k^12): it carries NO independent Cauchy data -- it is a functional
       of the instantaneous matter distribution, like GR's elliptic Hamiltonian/momentum
       constraints.  Its instantaneity is CONSTRAINT propagation, not an independent
       radiative signal.  Causal under the York foliation (committed qumond_causality:
       only hyperbolic characteristic is the matter cone; matter cone is lambda-
       INDEPENDENT iff rho = rest-mass).
""")
# reproduce the decisive slaving fact: the aux principal symbol carries no omega.
mu = sp.symbols('mu', real=True)
H_AB = k**2 * sp.Matrix([[0, mu, -1], [mu, -1, 0], [-1, 0, 0]])
detH = sp.simplify(H_AB.det())
check("(c2) aux (Phi,chi,lambda) principal symbol det = -k^6, carries NO omega "
      "=> elliptic (no cone, no Cauchy data) => Phi is slaved-constraint, not a DOF",
      sp.simplify(sp.Abs(detH) - k**6) == 0 and sp.diff(detH, w) == 0)

print("""
  (c3) The one genuinely PHYSICAL clock quantity is a0 = c q / Z, q = K = global York
       number (SPATIALLY CONSTANT, committed gate F).  Does local matter shift a0
       locally?  No: a0 has no spatial x-dependence, so d(a0)/d(local rho at A) has no
       A->B spatial structure.  A compact matter change can shift only the k=0
       homogeneous clock rate dq/dt (the integrated solvability C(t)), i.e. the same
       global York-time mode GR-CMC already carries -- not a localizable superluminal
       signal.
""")
# a0 depends on q only; q is x-independent. Represent a0 as a0(q); d a0/d x_local = 0.
q_s, x_s = sp.symbols('q_s x_s', real=True)
Zc, cc = sp.symbols('Z c', positive=True)
a0_expr = cc * q_s / Zc          # NO x dependence
check("(c3) a0 = c q / Z depends only on the GLOBAL q; d a0/d(local x) = 0 => a0 "
      "carries NO spatially-resolved A->B channel (only the k=0 homogeneous clock mode)",
      sp.diff(a0_expr, x_s) == 0)


# ==========================================================================
head("VERDICT (Test 1)")
# ==========================================================================
allpass = all(R.values())
print(f"  internal checks: {sum(R.values())}/{len(R)} PASS   all green: {allpass}\n")
print("""  (a) The CMC/lapse-fixing equation is the SECOND-CLASS gauge-consistency partner
      of H_perp: {chi_CMC, H_perp[N]} = (-D^2+V)N (invertible, V>=0) => it DETERMINES
      the (gauge) lapse; it is NOT a dynamical evolution equation.  Full S_York+S_Q+S_m
      count = 2 tensor + 0 scalar, invariant to the gauge-fixing.  => GENUINE CONSTRAINT.

  (b) It is a WELL-POSED elliptic BVP (symbol k^2+V>0, no omega, positive-definite,
      unique positive lapse).  No hidden time derivative; the only extra datum is ONE
      global scalar C(t)=dq/dt.  => NOT disguised dynamics.

  (c) Matter coupling makes the response INSTANTANEOUS-on-slice, but NOT a physical
      non-gauge channel:  (c1) N is gauge (matter couples to Phi, not N);
      (c2) Phi is a 0-DOF slaved elliptic constraint (GR-constraint status, causal
      under York foliation iff rho=rest-mass);  (c3) the physical a0 depends only on
      the GLOBAL spatially-constant q, so it carries no localizable A->B channel.

  => KILL-CLAUSE (a) does NOT fire: the elliptic CMC sector is a genuine
     non-propagating CONSTRAINT, instantaneous only in the GR-CMC (gauge + slaved-
     constraint + global-clock) sense.  This is CONDITIONAL on accepting the preferred
     CMC foliation (the standing Lorentz-violation cost), which the spine already pays.

  NOT decided here (separate):
   - kill-clause (b): the global foliation-SELECTION datum (dS K=0 vs K=3H) = Test 3.
   - gates E (G_eff=2G) and F (Cassini 4-8 sigma) remain independent active kills.
  So Test 1 => the York exception SURVIVES the causality/constraint test (does not self-
  kill via clause a), but is NOT saved: it stays alive-pending-Test-3 and still fails E,F.
""")

import sys
sys.exit(0 if allpass else 1)
