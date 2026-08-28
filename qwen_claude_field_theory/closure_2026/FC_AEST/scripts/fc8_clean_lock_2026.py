"""
FC-8 CLEAN LOCK — verify Carl's rho_chi -> V(chi) trade removes the kinetic entanglement.
==========================================================================================
FC-7 lock: alpha^2 = kappa^2 G rho_chi,  rho_chi = -1/2(grad chi)^2 + V   [contains chi-dot]
FC-8 lock: alpha^2 = kappa^2 G V(chi)                                     [NO chi-dot]

Claim (Carl, 9/10): FC-8's lock C_zeta = alpha^2 - kappa^2 G V(chi) has no chi-momentum, so it does not
graft onto the AeST-chi kinetic constraint algebra; the reduced MOND term depends on chi ONLY through
V(chi) => contributes NOTHING to any kinetic entry at ALL orders (stronger than FC-7's O(Y^3/2)), and
nothing to the chi GRADIENT entry either (V has no grad chi) => chi is a fully healthy canonical scalar,
coupled to the AeST phi-gradient sector only through the algebraic factor V(chi). Price: a0^2 prop V,
exact prop rho_chi only when chi-dot^2 << V (potential-dominated).

Uses the committed leading constitutive J10(x)=x^3/3 => L_MOND = Y^{3/2}/(3 sqrt(Lambda * S)),
S = rho_chi (FC-7) or V (FC-8).  Y = aether-orthogonal (spatial) phi-gradient, carries no chi-derivative.
"""
import sympy as sp

P = print
def ok(c, s): P(f"  [{'ok' if bool(c) else 'FAIL'}] {s}"); return bool(c)
FAILS = []
P("="*94); P("FC-8 clean lock vs FC-7 — kinetic entanglement check"); P("="*94)

# fields: chi with time-deriv chid and spatial-deriv chix; Y = spatial phi-gradient invariant (no chi, no time)
chi, chid, chix, Y, Lam, G, kap = sp.symbols('chi chidot chi_x Y Lambda G kappa', real=True, positive=True)
V = sp.Function('V')(chi)
Lam = kap**2*G                      # Lambda_chi = kappa^2 G  (FC-8 uses kappa^2 G V)
rho_chi = sp.Rational(1,2)*chid**2 - sp.Rational(1,2)*chix**2 + V   # E_chi = -1/2(grad chi)^2 + V

# reduced MOND term with leading J10(x)=x^3/3:  L = Lam*S * ( (sqrt(Y)/sqrt(Lam*S))^3 /3 ) = Y^{3/2}/(3 sqrt(Lam S))
def L_MOND(S):
    return Y**sp.Rational(3,2)/(3*sp.sqrt(Lam*S))

L7 = L_MOND(rho_chi)                 # FC-7: S = rho_chi (has chidot, chix)
L8 = L_MOND(V)                       # FC-8: S = V(chi)   (no chidot, no chix)

# ---- 1. lock constraint chi-momentum dependence ----
Cz7 = sp.Symbol('alpha')**2 - Lam*rho_chi
Cz8 = sp.Symbol('alpha')**2 - Lam*V
c1a = sp.simplify(sp.diff(Cz7, chid)) != 0      # FC-7: dC_zeta/d chidot != 0  => contains pi_chi
c1b = sp.simplify(sp.diff(Cz8, chid)) == 0      # FC-8: dC_zeta/d chidot == 0  => NO pi_chi
ok(c1a, f"FC-7 lock C_zeta contains chi-dot: dC_zeta/dchidot = {sp.simplify(sp.diff(Cz7,chid))} != 0 (grafts onto chi kinetic algebra)")
if not ok(c1b, "FC-8 lock C_zeta = alpha^2 - kappa^2 G V(chi): dC_zeta/dchidot = 0 => NO pi_chi in the constraint (clean)"): FAILS.append(1)

# ---- 2. MOND contribution to the KINETIC entry K_chichi = d^2 L / d chidot^2 ----
K7 = sp.simplify(sp.diff(L7, chid, 2))
K8 = sp.simplify(sp.diff(L8, chid, 2))
c2a = K7 != 0                                   # FC-7: nonzero => modifies K_chichi
c2b = sp.simplify(K8) == 0                      # FC-8: identically zero, ALL orders
ok(c2a, f"FC-7 MOND K_chichi contribution d^2L/dchidot^2 = {K7}  != 0 (the O(Y^3/2) entanglement)")
if not ok(c2b, "FC-8 MOND K_chichi contribution d^2L/dchidot^2 = 0 IDENTICALLY (all orders) => MOND adds NOTHING to the kinetic matrix"): FAILS.append(2)

# ---- 3. MOND contribution to the chi-phi kinetic mixing and chi GRADIENT entry ----
c3a = sp.simplify(sp.diff(L8, chid)) == 0       # no chidot at all
c3b = sp.simplify(sp.diff(L8, chix)) == 0       # no spatial grad chi at all (V has none; Y is phi's)
if not ok(c3a and c3b, "FC-8 MOND term has NO chi-dot and NO grad-chi (depends on chi only via V(chi)) "
                       "=> zero contribution to K_phichi AND to the chi gradient matrix G_chichi "
                       "=> chi stays a FULLY healthy canonical scalar (kinetic AND gradient canonical)"): FAILS.append(3)

# ---- 4. auxiliary sector still clean second-class; zeta_0=0; vacuum a0 ----
al, zeta, J, Jp, V0 = sp.symbols('alpha zeta J10 J10p V0', positive=True)
C_alpha = 2*al*zeta + al*(2*J - sp.Symbol('x')*Jp)
c4a = sp.simplify(sp.diff(Cz8.subs(sp.Symbol('alpha'), al), al) - 2*al) == 0   # dC_zeta/dalpha = 2 alpha
c4b = sp.simplify(sp.diff(C_alpha, zeta) - 2*al) == 0                          # dC_alpha/dzeta = 2 alpha
zeta0 = sp.solve(C_alpha, zeta)[0].subs({J:0, Jp:0})
c4c = sp.simplify(zeta0) == 0
a0sq = sp.simplify(Lam*V0)                                                      # vacuum: alpha_0^2 = kappa^2 G V0
ok(c4a and c4b, f"auxiliary Jacobian det = 4 alpha^2 != 0 => (alpha,zeta) clean 2nd-class sector")
ok(c4c, "zeta_0 = 0 at the vacuum (J10=J10'=0)")
ok(sp.simplify(a0sq - kap**2*G*V0)==0, "vacuum: a_0,0^2 = kappa^2 G V0 (constant a0); chi=chi0, V'(chi0)=0")

# ---- 5. the honest trade: a0^2 prop V, exact prop rho_chi only when chidot^2 << V ----
frac = sp.simplify((Lam*V)/(Lam*rho_chi))       # a0^2(FC8)/[kappa^2 G rho_chi] = V/rho_chi
P(f"\n  [trade] FC-8: a0^2 = kappa^2 G V(chi).  a0^2/(kappa^2 G rho_chi) = V/rho_chi = "
  f"{sp.simplify(frac)} -> 1 iff chidot^2/2 - chix^2/2 << V (potential-dominated). So a0^2 prop rho_DE is")
P("          exact only in the slow-roll/frozen regime; a0^2 prop V is the clean lock. Still IMPORTED (V chosen).")

# ---- 6. BTFR unchanged (MOND observable law untouched) ----
g, gN, M, r, v, a0 = sp.symbols('g g_N M r v a0', positive=True)
gN_expr = g**2/(g**10+a0**10)**sp.Rational(1,10)
c6 = sp.simplify(sp.limit(gN_expr/(g**2/a0), g, 0) - 1) == 0
ok(c6, "BTFR untouched: g_N = g^2/(g^10+a0^10)^(1/10) -> g^2/a0 deep-MOND => v^4 = G a0 M_b")

P("\n"+"="*94)
if not FAILS:
    P("VERDICT: FC-8's rho_chi -> V(chi) trade VERIFIED to do exactly what Carl claims. The lock carries no")
    P("chi-momentum, and the reduced MOND term contributes IDENTICALLY ZERO to every kinetic entry AND to")
    P("the chi gradient entry (all orders) -- chi is a fully healthy canonical scalar coupled to the AeST")
    P("phi-gradient only through the algebraic V(chi). This is strictly cleaner than FC-7's O(Y^3/2) K_chichi")
    P("correction: FC-8 introduces NO new ghost/gradient risk in the chi sector at any order.")
    P("PRICE: a0^2 = kappa^2 G V (not full rho_chi); exact prop rho_DE only when potential-dominated; still IMPORTED.")
    P("STILL OPEN (unchanged, no shortcut): full nonlinear Dirac rank of the enlarged 3+1 system; PPN; nonlinear")
    P("Phi=Psi; the INHERITED AeST phi-sector stability (low-k mode) + outer oscillatory regime; FLRW growth.")
else:
    P(f"VERDICT: FAILED groups {sorted(set(FAILS))}")
import sys; sys.exit(0 if not FAILS else 1)
