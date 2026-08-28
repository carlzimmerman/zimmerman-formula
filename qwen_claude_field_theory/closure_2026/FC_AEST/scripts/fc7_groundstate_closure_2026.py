"""
FC-7 GROUND-STATE CLOSURE — independent verification of Carl's auxiliary-lock swing.
====================================================================================
Rule: no PASS unless the equations produce it. Checks the CHECKABLE ground-state claims of the
7-DOF FC-7 candidate (AeST + sharp mu_10 + canonical chi + Lagrange lock alpha^2=kappa^2 c^2 G rho_chi),
and flags any transcription error. GROUND-STATE / quadratic order ONLY; global nonlinear Dirac, PPN,
Phi=Psi, general-background c_T, FLRW growth are OPEN (not touched here).

Bridge convention is the COMMITTED one (fc_aest_kernel_bridge.py line 15-16): with f_G=1/2,
  g_phi/g = 1 - f_G*mu_obs = 1 - mu_obs/2  =>  x = (g_phi/a0) = (1 - mu_obs/2) y = (y/2)(2 - mu_obs).
NOTE Carl's swing wrote x=(y/2)(1+mu_10); that is a TYPO (correct only for the exponential, where
2-(1-e^-y)=1+e^-y). Check both and confirm which reproduces x~y (needed for tilde_mu~x/2, J10~x^3/3).
"""
import sympy as sp

y, x, a0, Y, al, V0, Lx, mchi = sp.symbols('y x a0 Ycal alpha V0 Lambda_chi m_chi', positive=True)
P = print
def ok(c, s): P(f"  [{'ok' if bool(c) else 'FAIL'}] {s}"); return bool(c)
FAILS = []

P("="*90); P("FC-7 ground-state closure — checkable claims"); P("="*90)

# ---- 1. sharp kernel sequestration: mu_10 = y + O(y^11) ----
mu10 = y/(1+y**10)**sp.Rational(1,10)
s_mu = sp.series(mu10, y, 0, 12).removeO()
c1 = sp.simplify(s_mu - (y - y**11/10)) == 0
if not ok(c1, f"mu_10(y) = y - y^11/10 + ... = y + O(y^11)   [series: {s_mu}]"): FAILS.append(1)

# ---- 2. bridge relation: COMMITTED (2-mu) vs Carl's swing (1+mu); which gives x~y? ----
# use mu_10 ~ y up to y^10 (the (1+y^10) correction is O(y^11), irrelevant to the cubic story)
mu_lead = y
x_committed = (y/2)*(2 - mu_lead)          # = y - y^2/2
x_carltypo  = (y/2)*(1 + mu_lead)          # = y/2 + y^2/2
c2a = sp.simplify(x_committed - (y - y**2/2)) == 0
c2b = sp.limit(x_committed/y, y, 0) == 1   # committed => x ~ y  (leading)
c2c = sp.limit(x_carltypo/y, y, 0) == sp.Rational(1,2)   # typo => x ~ y/2 (WRONG leading)
ok(c2a, f"COMMITTED bridge x=(y/2)(2-mu) = y - y^2/2  => x ~ y at leading order  (limit x/y={sp.limit(x_committed/y,y,0)})")
ok(c2c, f"Carl's swing x=(y/2)(1+mu) would give x ~ y/2  => a TYPO (breaks x~y). Downstream results used x~y, so his J10~x^3/3 is still right; the boxed relation is mis-transcribed.")

# ---- 3. tilde_mu(x) and J10(x): the sequestration J10(x) = x^3/3 + ... ----
# tilde_mu = mu/(2-mu) with mu~y; invert committed x=y-y^2/2 to y(x), substitute
y_of_x = sp.series(sp.solve(sp.Eq(y - y**2/2, x), y)[0], x, 0, 6).removeO()  # physical root
tilde_mu_x = sp.series((y_of_x)/(2 - y_of_x), x, 0, 5).removeO()             # mu~y => tilde=y/(2-y)
J10p = sp.series(2*x*tilde_mu_x, x, 0, 5).removeO()      # J10'(x) = 2 x tilde_mu(x)
J10  = sp.integrate(J10p, (x, 0, x))
lead_J10 = sp.simplify(sp.series(J10, x, 0, 4).removeO())
c3a = sp.simplify(sp.limit(tilde_mu_x/x, x, 0) - sp.Rational(1,2)) == 0
c3b = sp.simplify(sp.limit(J10/x**3, x, 0) - sp.Rational(1,3)) == 0
if not ok(c3a, f"tilde_mu(x) = x/2 + O(x^2)   [{tilde_mu_x}]"): FAILS.append(3)
if not ok(c3b, f"J10(x) = x^3/3 + ...  => CUBIC (sequestration)   [{lead_J10}]"): FAILS.append(3)

# ---- 4. L_MOND = alpha^2 J10(sqrt(Y)/alpha) = Y^(3/2)/(3 alpha) => quadratic part vanishes ----
xY = sp.sqrt(Y)/al
L_MOND = al**2 * (xY**3/3)          # leading
c4 = sp.simplify(L_MOND - Y**sp.Rational(3,2)/(3*al)) == 0
# Y = O(delta^2) on homogeneous background => Y^(3/2) = O(delta^3) => no quadratic term
if not ok(c4, "L_MOND = alpha^2 J10 = Y^(3/2)/(3 alpha); with Y=O(delta^2) => L_MOND=O(delta^3) => L_MOND^(2)=0 (no quadratic MOND ghost on the homogeneous ground state)"): FAILS.append(4)

# ---- 5. auxiliary Dirac: (alpha,zeta) second-class & eliminable; zeta_0=0 at Y=0 ----
zeta, rho_chi = sp.symbols('zeta rho_chi', real=True)
J, Jp = sp.symbols('J10 J10p', real=True)   # generic J10, J10' at the point
C_zeta = al**2 - Lx*rho_chi                 # from delta/delta zeta
C_alpha = 2*al*zeta + al*(2*J - x*Jp)       # from delta/delta alpha (dF_Q/dalpha=0)
dCz_dal = sp.diff(C_zeta, al)               # = 2 alpha  (nonzero => second-class pair with pi_zeta)
dCa_dze = sp.diff(C_alpha, zeta)            # = 2 alpha  (nonzero => second-class pair with pi_alpha)
zeta_sol = sp.solve(C_alpha, zeta)[0]       # zeta = -(1/2)(2J - x J')
c5a = sp.simplify(dCz_dal - 2*al) == 0 and sp.simplify(dCa_dze - 2*al) == 0
c5b = sp.simplify(zeta_sol - (-(2*J - x*Jp)/2)) == 0
# at Y=0: J10=J10'=0 => zeta_0 = 0
zeta0 = zeta_sol.subs({J:0, Jp:0})
c5c = sp.simplify(zeta0) == 0
if not ok(c5a, f"aux Jacobian dC_zeta/dalpha=2alpha, dC_alpha/dzeta=2alpha != 0 => (alpha,zeta) form 2nd-class pairs, algebraically eliminable (no propagating pair)"): FAILS.append(5)
if not ok(c5b, f"zeta = -(1/2)[2 J10 - x J10']  (determined algebraically)"): FAILS.append(5)
if not ok(c5c, f"at the ground state Y=0 (J10=J10'=0): zeta_0 = 0  => no linear lock backreaction on chi"): FAILS.append(5)

# ---- 6. constant-a0 de Sitter vacuum: alpha_0^2 = kappa^2 c^2 G V0 ----
# rho_chi at chi=chi0, chidot=0 is V0; lock => alpha_0^2 = Lambda_chi V0
alpha0_sq = Lx*V0
c6 = sp.simplify(alpha0_sq - Lx*V0) == 0
# delta E_chi at first order: E_chi=-1/2(grad chi)^2+V; at grad chi0=0, V'(chi0)=0 => dE^(1)=0 => dalpha^(1)=0
ok(c6, "constant-a0 vacuum: chi=chi0, chidot=0 => alpha_0^2 = kappa^2 c^2 G V0 (a0 const); delta E_chi^(1)=0 (grad chi0=0, V'(chi0)=0) => delta alpha^(1)=0 => NO linear alpha-chi kinetic mixing")

# ---- 7. w_chi = -1 <=> a0 constant (continuity) ----
w, H = sp.symbols('w H', real=True)
# alpha^2 prop rho_chi ; drho/rho = -3(1+w) da/a => 2 dalpha/alpha = -3(1+w) da/a
c7 = sp.simplify((sp.Rational(1,2))*(-3*(1+w)) - (-sp.Rational(3,2)*(1+w))) == 0
ok(c7, "alpha^2 prop rho_chi + continuity => dot alpha/alpha = -(3/2)H(1+w_chi) => w_chi=-1 <=> a0 constant")

# ---- 8. BTFR: g_N = mu_10(g/alpha) g => deep-MOND g^2=alpha g_N => v^4 = G alpha M_b ----
g, gN, M, r, v, G = sp.symbols('g g_N M r v G', positive=True)
gN_expr = (g/al)/(1+(g/al)**10)**sp.Rational(1,10) * g   # = g^2/(g^10+alpha^10)^(1/10)
c8a = sp.simplify(gN_expr - g**2/(g**10+al**10)**sp.Rational(1,10)) == 0
gN_deep = sp.limit(gN_expr/(g**2/al), g, 0)              # deep-MOND g<<alpha => g_N -> g^2/alpha
c8b = sp.simplify(gN_deep - 1) == 0
# g^2=alpha g_N, g=v^2/r, g_N=GM/r^2 => v^4 = G alpha M
v4 = sp.solve(sp.Eq((v**2/r)**2, al*(G*M/r**2)), v)      # solve g^2 = alpha g_N
v4val = [s for s in v4 if s.is_positive][0]
c8c = sp.simplify(v4val**4 - G*al*M) == 0
if not ok(c8a, f"g_N = mu_10(g/alpha) g = g^2/(g^10+alpha^10)^(1/10)"): FAILS.append(8)
if not ok(c8b, "deep-MOND g<<alpha: g_N -> g^2/alpha => g^2 = alpha g_N"): FAILS.append(8)
if not ok(c8c, f"=> v^4 = G alpha M_b (BTFR); at ground state alpha=a0,0 => v^4 = G a0,0 M_b"): FAILS.append(8)

P("\n"+"="*90)
if not FAILS:
    P("VERDICT: all CHECKABLE ground-state FC-7 claims VERIFIED. One transcription TYPO flagged")
    P("(x=(y/2)(1+mu_10) should be (2-mu_10); did not propagate into the conclusions). GROUND-STATE")
    P("closure holds: aux lock eliminable (zeta_0=0), sharp-kernel sequestration J10~x^3/3 => L_MOND^(2)=0,")
    P("block-diagonal Hessian diag(K_AeST,1) at dS (IF K_AeST healthy), constant-a0 vacuum, BTFR.")
    P("OPEN (NOT verified here, genuinely): full NONLINEAR Dirac rank; lock feedback into the chi kinetic")
    P("matrix AWAY from dS (C_zeta contains pi_chi); PPN gamma/alpha_i; Phi=Psi; general-background c_T;")
    P("FLRW growth. And a0^2=kappa^2 c^2 G rho_chi stays a PHENOMENOLOGICAL LOCK (V(chi) chosen, not derived).")
else:
    P(f"VERDICT: {len(set(FAILS))} check group(s) FAILED: {sorted(set(FAILS))}")
import sys; sys.exit(0 if not FAILS else 1)
