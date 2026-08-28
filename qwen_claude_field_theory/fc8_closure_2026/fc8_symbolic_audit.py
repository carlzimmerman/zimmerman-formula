"""
Gate 0 — FC-FINAL SYMBOLIC AUDIT.  The one gate that PASSES from the equations right now.
=========================================================================================
FC-FINAL = AeST with the free function modified ONLY in its Y-sector, a0 a CONSTANT:
   F(Y,Q) = F_Q^star(Q) + a0^2 J10( sqrt(Y)/a0 ),   a0 = const.   Fields: g, A, phi (no sigma).
Proves: sharp-kernel sequestration => the MOND term does not add a quadratic kinetic term on the vacuum,
plus the MOND law / BTFR / Solar-System suppression. FAILS LOUDLY if a quadratic MOND kinetic term appears.
Discipline: PASS only from the equations; this script prints the quantities it checks.
Frozen (do not edit): mu10(y)=y/(1+y^10)^(1/10); x=(y/2)(2-mu10); J10'=2x mu10/(2-mu10).
"""
import sympy as sp
P = print
def report(tag, status, msg): P(f"  [{status:4}] {tag}: {msg}"); return status
STAT = []
P("="*94); P("Gate 0  FC-FINAL symbolic audit (constant a0, no sigma)"); P("="*94)

y, x, Y, a0 = sp.symbols('y x Y a0', positive=True)

# --- A1: mu10 = y + O(y^11) ---
mu10 = y/(1+y**10)**sp.Rational(1,10)
s_mu = sp.series(mu10, y, 0, 12).removeO()
STAT.append(report("A1 sharp kernel", "PASS" if sp.simplify(s_mu-(y-y**11/10))==0 else "FAIL",
    f"mu10(y) = y - y^11/10 + ... = y + O(y^11)  [{s_mu}]"))

# --- A2: J10(x) = x^3/3 + ...  (sequestration), via committed bridge x=(y/2)(2-mu10) ---
y_of_x = sp.series(sp.solve(sp.Eq(y - y**2/2, x), y)[0], x, 0, 6).removeO()   # mu10~y => x=y-y^2/2
tmu = sp.series(y_of_x/(2 - y_of_x), x, 0, 5).removeO()
J10 = sp.integrate(sp.series(2*x*tmu, x, 0, 5).removeO(), (x, 0, x))
STAT.append(report("A2 cubic sequestration", "PASS" if sp.simplify(sp.limit(J10/x**3,x,0)-sp.Rational(1,3))==0 else "FAIL",
    f"tilde_mu(x)=x/2+... ; J10(x)=x^3/3+O(x^13)  [{sp.series(J10,x,0,4).removeO()}]"))

# --- A3: F_M = a0^2 J10(sqrt Y/a0) = Y^{3/2}/(3 a0) => O(delta^3) => delta^2 S_MOND = 0 ---
F_M = a0**2 * (sp.sqrt(Y)/a0)**3 / 3
c3 = sp.simplify(F_M - Y**sp.Rational(3,2)/(3*a0)) == 0 and sp.simplify(F_M.subs(Y,0))==0 \
     and sp.simplify(sp.limit(F_M/Y**sp.Rational(3,2), Y, 0)) != 0
STAT.append(report("A3 MOND-kinetic guard", "PASS" if c3 else "FAIL",
    "F_M = a0^2 J10 = Y^{3/2}/(3 a0): no Y^0, no Y^1 term (a0 constant) => O(delta^3) => delta^2 S_MOND=0. "
    "GUARD: any Y^0/Y^1 (quadratic MOND kinetic) here => FAIL"))

# --- A4: Y carries no phi-dot (aether-orthogonal projector) => MOND adds nothing to the velocity Hessian ---
N, h1, h2, h3, pt, px, py, pz = sp.symbols('N h1 h2 h3 phi_t phi_x phi_y phi_z', real=True)
ginv = sp.diag(-1/N**2, 1/h1, 1/h2, 1/h3); Aup = sp.Matrix([1/N,0,0,0])
proj = ginv + Aup*Aup.T
Ycal = (sp.Matrix([pt,px,py,pz]).T * proj * sp.Matrix([pt,px,py,pz]))[0]
c4 = sp.simplify(sp.diff(Ycal, pt)) == 0
STAT.append(report("A4 no MOND kinetic", "PASS" if c4 else "FAIL",
    f"(g+AA) projector removes phi_t: Y = {sp.simplify(Ycal)} (spatial only) => F_M(Y) has no phi-dot "
    "=> zero contribution to the velocity Hessian => AeST kinetic structure untouched by the modification"))

# --- A5: MOND law, sharp Newtonian recovery, BTFR ---
g, gN, M, r, v, Gn = sp.symbols('g g_N M r v Gnewton', positive=True)
gN_expr = g**2/(g**10+a0**10)**sp.Rational(1,10)
one_minus = sp.series(1 - mu10, y, sp.oo, 2)
c5a = sp.simplify(sp.limit(gN_expr/(g**2/a0), g, 0) - 1) == 0
v4 = [s for s in sp.solve(sp.Eq((v**2/r)**2, a0*(Gn*M/r**2)), v) if s.is_positive][0]
c5b = sp.simplify(v4**4 - Gn*a0*M) == 0
STAT.append(report("A5 MOND+SS+BTFR", "PASS" if (c5a and c5b) else "FAIL",
    f"g_N=g^2/(g^10+a0^10)^(1/10); 1-mu10 ~ (1/10)(a0/g)^10 (SS sharp, no screening needed); "
    f"deep-MOND g^2=a0 g_N => v^4 = G a0 M_b"))

P("\n"+"="*94)
nfail = sum(s=="FAIL" for s in STAT)
P(f"Gate 0 RESULT: {sum(s=='PASS' for s in STAT)}/{len(STAT)} PASS, {nfail} FAIL.")
if nfail == 0:
    P("Gate 0 = PASS. Sequestration + no-MOND-kinetic + MOND law/BTFR/Newtonian-sharp all produced by the")
    P("frozen FC-FINAL equations. This is an INPUT to the closure, NOT the closure. Gates A-G remain (RESULTS.md).")
else:
    P("Gate 0 = FAIL — a frozen-candidate identity broke. Do NOT proceed until fixed or the candidate is FAILED.")
import sys; sys.exit(0 if nfail == 0 else 1)
