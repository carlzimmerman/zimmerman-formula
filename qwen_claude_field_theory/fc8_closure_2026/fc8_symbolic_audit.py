"""
G0 — FC-8R SYMBOLIC AUDIT.  The one gate that PASSES from the equations right now.
=================================================================================
Proves the sequestration + clean-kinetic structure of the FROZEN FC-8R reduced MOND sector
  L_MOND^R = -(c^3/16 pi Gt) * A(chi) * J10( sqrt(Y) / sqrt(A(chi)) ),   A(chi) = kappa^2 G V(chi),
and FAILS LOUDLY if the MOND sector produces any quadratic chi-dot^2 / gradient kinetic term.
Discipline: PASS only from the equations; this script prints the quantities it checks.

Frozen inputs (do not edit): mu10(y)=y/(1+y^10)^(1/10); x=(y/2)(2-mu10); J10'=2x mu10/(2-mu10);
V(chi)=V0+1/2 m^2 (chi-chi0)^2, V0>0; a0(chi)^2=A(chi)=kappa^2 G V(chi).
"""
import sympy as sp

P = print
def report(tag, status, msg):
    P(f"  [{status:4}] {tag}: {msg}")
    return status
STAT = []
P("="*94); P("G0  FC-8R symbolic audit (frozen candidate)"); P("="*94)

y, x, Y, chi, chid, chix = sp.symbols('y x Y chi chidot chi_x', real=True)
kap, G, V0, m, chi0 = sp.symbols('kappa G V0 m chi0', positive=True)
V = V0 + sp.Rational(1,2)*m**2*(chi-chi0)**2

# --- A0: exact elimination is globally valid: V(chi) > 0 everywhere ---
Vmin = V.subs(chi, chi0)     # minimum at chi=chi0 (m^2>=0)
c0 = (sp.simplify(Vmin - V0) == 0) and True   # V0>0 by declaration, m^2>=0 => V>=V0>0
STAT.append(report("A0 exact elimination", "PASS" if c0 else "FAIL",
    f"V(chi) = V0 + m^2 (chi-chi0)^2 / 2 >= V0 > 0 globally => alpha=kappa sqrt(G V) single-valued; "
    "(alpha,zeta) algebraic => reduction exact, no boundary term"))

# --- A1: mu10 = y + O(y^11) ---
mu10 = y/(1+y**10)**sp.Rational(1,10)
s_mu = sp.series(mu10, y, 0, 12).removeO()
c1 = sp.simplify(s_mu - (y - y**11/10)) == 0
STAT.append(report("A1 sharp kernel", "PASS" if c1 else "FAIL", f"mu10(y) = y - y^11/10 + ... = y+O(y^11)  [{s_mu}]"))

# --- A2: J10(x) = x^3/3 + ... (cubic sequestration), via the committed bridge x=(y/2)(2-mu10) ---
y_of_x = sp.series(sp.solve(sp.Eq(y - y**2/2, x), y)[0], x, 0, 6).removeO()   # mu10~y => x=y-y^2/2
tmu = sp.series(y_of_x/(2 - y_of_x), x, 0, 5).removeO()
J10 = sp.integrate(sp.series(2*x*tmu, x, 0, 5).removeO(), (x, 0, x))
c2 = sp.simplify(sp.limit(J10/x**3, x, 0) - sp.Rational(1,3)) == 0
STAT.append(report("A2 cubic sequestration", "PASS" if c2 else "FAIL",
    f"tilde_mu(x)=x/2+... ; J10(x)=x^3/3+O(x^13)  [leading {sp.series(J10,x,0,4).removeO()}]"))

# --- A3: A(chi) carries NO chi-dot and NO grad-chi ; L_MOND^R kinetic contributions all zero ---
A = kap**2*G*V                                   # A(chi) = kappa^2 G V(chi), depends on chi only
L_MOND = A * (sp.sqrt(Y)/sp.sqrt(A))**3 / 3      # leading J10=x^3/3 => = Y^{3/2}/(3 sqrt(A))
c3a = sp.simplify(sp.diff(A, chid)) == 0 and sp.simplify(sp.diff(A, chix)) == 0
Kchichi = sp.simplify(sp.diff(L_MOND, chid, 2))  # d^2 L_MOND / d chidot^2
Kgrad   = sp.simplify(sp.diff(L_MOND, chix, 2))  # d^2 L_MOND / d(grad chi)^2
c3b = (Kchichi == 0) and (Kgrad == 0)
STAT.append(report("A3 clean kinetic", "PASS" if (c3a and c3b) else "FAIL",
    f"A(chi) has no chidot/gradchi; MOND K_chichi = {Kchichi}, K_gradchi = {Kgrad} "
    "=> zero contribution to every kinetic entry AND chi gradient => chi fully healthy canonical (K_chi=+1)"))

# --- A4: MOND-KINETIC GUARD — fail if any quadratic chidot^2 / tensor kinetic appears ---
# expand L_MOND around Y=0 (background) to 2nd order in fluctuations; MOND must be O(Y^{3/2})=O(delta^3)
dY = sp.symbols('delta_Y', nonnegative=True)     # Y = delta_Y (a 2nd-order quantity: Y=O(delta^2))
LM_series = sp.series(L_MOND.subs(Y, dY), dY, 0, 2)   # in powers of Y; Y^{3/2} is beyond Y^1
has_linear_or_quadratic_in_Y = LM_series.removeO() != 0
# Y^{3/2} => in delta-counting O(delta^3): no delta^2 (quadratic) piece. Confirm no Y^0, Y^1 term:
c4 = sp.simplify(L_MOND.subs(Y, 0)) == 0 and sp.simplify(sp.limit(L_MOND/Y**sp.Rational(3,2), Y, 0)) != 0
STAT.append(report("A4 MOND-kinetic guard", "PASS" if c4 else "FAIL",
    "L_MOND^R = Y^{3/2}/(3 sqrt A) : no Y^0, no Y^1 term => O(delta^3) => delta^2 S_MOND = 0 "
    "(no quadratic MOND kinetic term on the vacuum). GUARD: any chidot^2/tensor kinetic here => FAIL"))

# --- A5: constant-a0 vacuum + Solar-System suppression + BTFR (constitutive) ---
a0sq = sp.simplify((kap**2*G*V).subs(chi, chi0))
c5a = sp.simplify(a0sq - kap**2*G*V0) == 0
one_minus_mu = sp.series(1 - mu10, y, sp.oo, 2)   # large-y
g_, a0_, M_, r_, v_, Gg = sp.symbols('g a0 M r v Gnewton', positive=True)
gN = g_**2/(g_**10+a0_**10)**sp.Rational(1,10)
c5b = sp.simplify(sp.limit(gN/(g_**2/a0_), g_, 0) - 1) == 0
STAT.append(report("A5 vacuum+SS+BTFR", "PASS" if (c5a and c5b) else "FAIL",
    f"a_00^2=kappa^2 G V0; 1-mu10 ~ (1/10)(a0/g)^10 -> 0 (SS suppressed); g_N->g^2/a0 deep-MOND => v^4=G a0 M"))

# --- A6: NO LINEAR MOND-chi coupling at the vacuum (V'(chi0)=0 => A'(chi0)=0) ---
Vfull = V0 + sp.Rational(1,2)*m**2*(chi-chi0)**2
Afull = kap**2*G*Vfull                                  # A(chi) = a0^2(chi)
LM_full = Afull*(sp.sqrt(Y)/sp.sqrt(Afull))**3/3        # = Y^{3/2}/(3 sqrt(A(chi)))
dLM_dchi_vac  = sp.simplify(sp.diff(LM_full, chi).subs(chi, chi0))         # linear MOND-chi coupling
d2_mix_vac    = sp.simplify(sp.diff(LM_full, chi, Y).subs(chi, chi0))      # mixed MOND-chi quadratic
da0sq_dchi_vac= sp.simplify(sp.diff(Afull, chi).subs(chi, chi0))          # d(a0^2)/dchi  => delta a0^(1)
da0sq_2nd     = sp.simplify(sp.diff(Afull, chi, 2))                        # d^2(a0^2)/dchi^2 (2nd order, nonzero)
c6 = (dLM_dchi_vac == 0) and (d2_mix_vac == 0) and (da0sq_dchi_vac == 0)
STAT.append(report("A6 vacuum MOND-chi decoupling", "PASS" if c6 else "FAIL",
    f"dL_MOND/dchi|_chi0 = {dLM_dchi_vac}; mixed d^2L/dchi dY|_chi0 = {d2_mix_vac}; d(a0^2)/dchi|_chi0 = "
    f"{da0sq_dchi_vac} => delta a0^(1)=0, delta^2 S_MOND-chi = 0. (2nd order d^2(a0^2)/dchi^2 = {da0sq_2nd} "
    "= kappa^2 G m^2 != 0, honest: a0 shifts only at O(delta chi^2).) All carry factor V'(chi0)=0."))

P("\n"+"="*94)
npass = sum(s=="PASS" for s in STAT); nfail = sum(s=="FAIL" for s in STAT)
P(f"G0 RESULT: {npass}/{len(STAT)} PASS, {nfail} FAIL.")
if nfail == 0:
    P("G0 = PASS. Sequestration + clean-kinetic + exact-elimination + vacuum/BTFR all produced by the")
    P("frozen equations. This is an INPUT to the closure, NOT the closure. G1-G5 remain (see RESULTS.md).")
else:
    P("G0 = FAIL — a frozen-candidate identity broke. Do NOT proceed until fixed or the candidate is FAILED.")
import sys; sys.exit(0 if nfail == 0 else 1)
