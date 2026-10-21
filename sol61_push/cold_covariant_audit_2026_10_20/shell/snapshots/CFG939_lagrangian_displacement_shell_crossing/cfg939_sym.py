"""CFG939 symbolic checks (sympy): K1, K1b, K2, K8 and the linear dispersion relations.
Criteria: FROZEN_CRITERIA.md (3524438b2) + AMENDMENT_A1_pre_result.md (7dace0a16).
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg939_sym.py   -> cfg939_sym.out, cfg939_sym_results.json (exit 0 iff all PASS)
kappa = 1/2 FITTED; footings never pooled (nothing here depends on the footing); not theory closed.
"""
import os, sys, json, resource
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
LINES, RES = [], {}
def P(s=""):
    print(s, flush=True); LINES.append(s)
def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
def check(name, ok, detail=""):
    RES[name] = dict(ok=bool(ok), detail=str(detail)); P(f"  {name}: {'PASS' if ok else 'FAIL'}  {detail}"); return bool(ok)

P(__doc__.strip()); P()
OK = []

# ---------------------------------------------------------------- K1: 3-D linear limit
P("K1  3-D linear limit: x = q + eps*psi(q,t); rho = rhobar/det(I + eps dpsi/dq); P = -rhobar*eps*psi")
eps, t, rb = sp.symbols("epsilon t rhobar", positive=True)
q = sp.symbols("q1:4")
psi = [sp.Function(f"psi{i+1}")(*q, t) for i in range(3)]
M = sp.Matrix(3, 3, lambda i, j: (1 if i == j else 0) + eps * sp.diff(psi[i], q[j]))
detM = sp.expand(M.det())
rho = rb / detM
delta1 = sp.series(rho / rb - 1, eps, 0, 2).removeO()
divq_psi = sum(sp.diff(psi[i], q[i]) for i in range(3))
OK.append(check("K1a delta = -div_q Psi + O(eps^2)", sp.simplify(delta1 + eps * divq_psi) == 0))
Minv = M.inv()                                   # d/dx_j = sum_k Minv[k, j] d/dq_k
Pv = [-rb * eps * psi[i] for i in range(3)]
divx_P = sum(Minv[k, j] * sp.diff(Pv[j], q[k]) for j in range(3) for k in range(3))
lhs = sp.series(divx_P - (rho - rb), eps, 0, 2).removeO()
OK.append(check("K1b div_x P - (rho - rhobar) = O(eps^2)", sp.simplify(lhs) == 0))
v = [eps * sp.diff(psi[i], t) for i in range(3)]
# Eulerian time derivative: d_t|_x P = d_t|_q P - v . grad_x P
gradx = lambda f: [sum(Minv[k, j] * sp.diff(f, q[k]) for k in range(3)) for j in range(3)]
dtP = [sp.diff(Pv[i], t) - sum(v[j] * gradx(Pv[i])[j] for j in range(3)) for i in range(3)]
jv = [rho * v[i] for i in range(3)]
res = [sp.simplify(sp.series(dtP[i] + jv[i], eps, 0, 2).removeO()) for i in range(3)]
OK.append(check("K1c d_t P + j = O(eps^2)   (sign: P = -rhobar*Psi)", all(r == 0 for r in res)))
# wrong-sign tooth: P = +rhobar*Psi must fail
Pw = [rb * eps * psi[i] for i in range(3)]
divx_Pw = sum(Minv[k, j] * sp.diff(Pw[j], q[k]) for j in range(3) for k in range(3))
bad = sp.simplify(sp.series(divx_Pw - (rho - rb), eps, 0, 2).removeO())
OK.append(check("K1d tooth: P = +rhobar*Psi violates div P = rho - rhobar", bad != 0, f"residual {bad}"))

# ---------------------------------------------------------------- K1b: exact single-stream 1-D and spherical
P("\nK1b exact single-stream forms (inverse map Q(x,t); continuity d_t Q|_x = -v d_x Q)")
x, r = sp.symbols("x r", positive=True)
Q = sp.Function("Q")(x, t); vf = sp.Function("v")(x, t)
P1 = rb * (Q - x); rho1 = rb * sp.diff(Q, x)
gauss1 = sp.simplify(sp.diff(P1, x) - (rho1 - rb))
cont1 = sp.simplify((sp.diff(P1, t) + rho1 * vf).subs(sp.Derivative(Q, t), -vf * sp.diff(Q, x)))
OK.append(check("K1b-1D P = rhobar (q - x): d_x P = rho - rhobar EXACT", gauss1 == 0))
OK.append(check("K1b-1D d_t P = -rho v EXACT", cont1 == 0))
Qr = sp.Function("Q")(r, t); vr = sp.Function("v")(r, t)
Pr = rb * (Qr**3 - r**3) / (3 * r**2); rhor = rb * Qr**2 * sp.diff(Qr, r) / r**2
gaussr = sp.simplify(sp.diff(r**2 * Pr, r) / r**2 - (rhor - rb))
contr = sp.simplify((sp.diff(Pr, t) + rhor * vr).subs(sp.Derivative(Qr, t), -vr * sp.diff(Qr, r)))
OK.append(check("K1b-sph P_r = rhobar (q^3 - r^3)/(3 r^2): Gauss EXACT", gaussr == 0))
OK.append(check("K1b-sph continuity EXACT", contr == 0))
Ps = sp.symbols("Psi")
ser = sp.expand(rb * ((r - Ps)**3 - r**3) / (3 * r**2))
OK.append(check("K1b-sph series in Psi = r - q", sp.simplify(ser - (-rb * Ps + rb * Ps**2 / r - rb * Ps**3 / (3 * r**2))) == 0,
                f"P_r = {ser}"))
RES["exact_spherical_P_series"] = str(ser)

# ---------------------------------------------------------------- K2: 1-D Lagrangian action -> Eulerian force
P("\nK2  1-D reduced Lagrangian per unit q (Phi eliminated; cold self-gravity cancelled by the critical quadratic, CFG888):")
P("    L = rhobar*Psidot^2/2 - rhobar*Phi_b(q+Psi) - J*W(K*rhobar*Psi) - (gamma*rhobar^2/2)*(J-1)^2/J,  J = 1 + Psi'   (Psi > 0 branch)")
qq, K, gam = sp.symbols("q K gamma", positive=True)
Psi = sp.Function("Psi")(qq, t)
W = sp.Function("W"); Phib = sp.Function("Phi_b")
J = 1 + sp.diff(Psi, qq)
L = rb * sp.diff(Psi, t)**2 / 2 - rb * Phib(qq + Psi) - J * W(K * rb * Psi) - gam * rb**2 / 2 * (J - 1)**2 / J
EL = sp.euler_equations(L, [Psi], [qq, t])[0].lhs          # dL/dPsi - d_t dL/dPsidot - d_q dL/dPsi' = 0
acc = sp.solve(sp.Eq(EL, 0), sp.diff(Psi, t, 2))[0]
u = K * rb * Psi
Rfun = K * sp.Subs(sp.diff(W(sp.Symbol("s")), sp.Symbol("s")), sp.Symbol("s"), u).doit()   # R(u) = K W'(u)
expected = -sp.Subs(sp.diff(Phib(sp.Symbol("y")), sp.Symbol("y")), sp.Symbol("y"), qq + Psi).doit() - Rfun \
           + gam * rb * J**-3 * sp.diff(J, qq)
diffK2 = sp.simplify(acc - expected)
OK.append(check("K2a EL acceleration = -Phi_b' - R(K|P|) sgn(Psi) + gamma*rhobar*J^-3*J'", diffK2 == 0))
# stiffness identity: Eulerian -gamma d_x rho with rho = rhobar/J, d_x = (1/J) d_q
st_eul = -gam * (1 / J) * sp.diff(rb / J, qq)
OK.append(check("K2b stiffness: gamma*rhobar*J^-3*J' == -gamma d_x rho (per unit mass)", sp.simplify(st_eul - gam * rb * J**-3 * sp.diff(J, qq)) == 0))
# tether-off limit: W_rem -> -u^2/(2K)  => R = -u => force +K rhobar Psi = Newtonian planar self-gravity of the excess
s_ = sp.Symbol("s")
L_off = L.subs(W(K * rb * Psi), -(K * rb * Psi)**2 / (2 * K))
acc_off = sp.solve(sp.Eq(sp.euler_equations(L_off, [Psi], [qq, t])[0].lhs, 0), sp.diff(Psi, t, 2))[0]
newt = -sp.Subs(sp.diff(Phib(sp.Symbol("y")), sp.Symbol("y")), sp.Symbol("y"), qq + Psi).doit() + K * rb * Psi + gam * rb * J**-3 * sp.diff(J, qq)
OK.append(check("K2c tether off (W -> -u^2/2K): +K*rhobar*Psi = planar Newtonian self-gravity", sp.simplify(acc_off - newt) == 0))
# kinetic term in P language: rhobar Psidot^2/2 = Pdot^2/(2 rhobar) with P = -rhobar Psi  -> inertia I = 1/rhobar
Pd = sp.Symbol("Pdot")
OK.append(check("K2d kinetic term: (1/2) rhobar Psidot^2 == Pdot^2/(2 rhobar) at P = -rhobar Psi (inertia I = 1/rhobar FORCED)",
                sp.simplify(rb * (-Pd / rb)**2 / 2 - Pd**2 / (2 * rb)) == 0))
# Lagrangian stiffness energy density (per unit q) equals (gamma/2)(rho - rhobar)^2 dx
OK.append(check("K2e stiffness energy: (gamma rhobar^2/2)(1-J)^2/J dq == (gamma/2)(rho-rhobar)^2 dx",
                sp.simplify(gam * rb**2 / 2 * (1 - J)**2 / J - gam / 2 * (rb / J - rb)**2 * J) == 0))

# ---------------------------------------------------------------- linear dispersion with stiffness
P("\nLinear dispersion (1-D, static background, plane wave Psi ~ exp(i(kq - wt))):")
k, w = sp.symbols("k omega", positive=True)
Ls = sp.symbols("L_star", positive=True)
gsub = {gam: K * Ls**2 / 2}
w2_newt = (gam * rb * k**2 - K * rb).subs(gsub)
kJ = sp.solve(sp.Eq(w2_newt, 0), k)[0]
OK.append(check("D1 Newtonian+stiffness: omega^2 = gamma rhobar k^2 - K rhobar -> k_J = sqrt(2)/L*, lambda_J = sqrt(2) pi L*",
                sp.simplify(kJ - sp.sqrt(2) / Ls) == 0, f"k_J = {kJ}"))
P("  D2 canonical tether (ID): R(u) = u^2/(a0-u) is O(u^2) -> no linear restoring term; no cold self-gravity -> omega^2 = gamma rhobar k^2"
  " (stiffness sound speed c^2 = 2 pi G L*^2 rhobar; locally 2 pi G L*^2 rho_c)")
RES["lambda_J_over_Lstar"] = float(sp.sqrt(2) * sp.pi)

# ---------------------------------------------------------------- K8: closed forms
P("\nK8  closed forms (units G = 1):")
a0, m, rr, uu, sv = sp.symbols("a_0 m r u s", positive=True)
Rk = lambda z: z**2 / (a0 - z)
w_ = sp.symbols("w", positive=True)
# Pi(r; m) = int_r^inf R(m/r'^2) dr' = sqrt(m a0) [artanh(sqrt(u/a0)) - sqrt(u/a0)], u = m/r^2
Pi_closed = sp.sqrt(m * a0) * (sp.atanh(sp.sqrt(m / (rr**2 * a0))) - sp.sqrt(m / (rr**2 * a0)))
dPi = sp.simplify(sp.diff(Pi_closed, rr) + Rk(m / rr**2))
OK.append(check("K8a dPi/dr = -R(m/r^2) (closed form of the tether potential)", dPi == 0))
import mpmath as mp
mp.mp.dps = 30
for (mv, rv, av) in ((0.3, 2.0, 1.0), (5.0, 3.0, 1.0), (0.01, 0.2, 1.3)):
    num = mp.quad(lambda y: (mv / y**2)**2 / (av - mv / y**2), [rv, 10 * rv, mp.inf])
    clo = mp.sqrt(mv * av) * (mp.atanh(mp.sqrt(mv / (rv**2 * av))) - mp.sqrt(mv / (rv**2 * av)))
    OK.append(check(f"K8b Pi quadrature m={mv} r={rv} a0={av}", abs(num / clo - 1) < 1e-8, f"rel {float(abs(num/clo-1)):.1e}"))
# f_crit for sudden loss of a fraction f of point-mass baryons, shell at rest on the law (single stream, own enclosed mass):
#   E_q = -(1-f) M_b/r + Pi(r; m_law) > 0 ;  law: R(u) = M_b/r^2, m = u r^2.  x = u/a0.
xx = sp.symbols("x", positive=True)
gN = a0 * xx**2 / (1 - xx)                         # = R(u) at u = a0 x
Pi_on_law = sp.sqrt(a0 * xx * rr**2 * a0) * (sp.atanh(sp.sqrt(xx)) - sp.sqrt(xx))
fcrit = sp.simplify(1 - Pi_on_law / (gN * rr))
fcrit_claim = 1 - (1 - xx) * (sp.atanh(sp.sqrt(xx)) - sp.sqrt(xx)) / xx**sp.Rational(3, 2)
OK.append(check("K8c f_crit(x) = 1 - (1-x)(artanh sqrt x - sqrt x)/x^(3/2)", sp.simplify(fcrit - fcrit_claim) == 0))
lim0 = sp.limit(fcrit_claim, xx, 0, "+")
OK.append(check("K8d deep limit f_crit -> 2/3", sp.simplify(lim0 - sp.Rational(2, 3)) == 0, f"limit {lim0}"))
fnum = sp.lambdify(xx, fcrit_claim, "mpmath")
for xv in (1e-4, 0.1, 0.5, 0.9):
    # direct root: find f with E_q = 0 numerically using quadrature for Pi
    uv = xv; rv = 1.7; av = 1.0; mv = uv * rv**2; Mb = rv**2 * uv**2 / (1 - uv)
    piq = mp.quad(lambda y: (mv / y**2)**2 / (av - mv / y**2), [rv, 10 * rv, mp.inf])
    froot = 1 - piq * rv / Mb
    OK.append(check(f"K8e f_crit closed form vs quadrature root at x={xv}", abs(froot - fnum(xv)) < 1e-8,
                    f"f_crit {float(fnum(xv)):.6f}"))
RES["fcrit_table"] = {str(xv): float(fnum(xv)) for xv in (1e-6, 1e-3, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99)}
P("  f_crit(x): " + ", ".join(f"x={k_}: {v_:.4f}" for k_, v_ in RES["fcrit_table"].items()))
# energy antiderivative for int r^2 What(M/r^2) dr = (1/2) M^(3/2) [G(s_lo) - G(s_hi)], What(s) = -s^2/2 - s - ln(1-s) (a0 = 1)
What = -sv**2 / 2 - sv - sp.log(1 - sv)
Gs = -sp.sqrt(sv) + sp.Rational(2, 3) / sp.sqrt(sv) + sp.Rational(2, 3) * sv**sp.Rational(-3, 2) * sp.log(1 - sv) + sp.Rational(4, 3) * sp.atanh(sp.sqrt(sv))
OK.append(check("K8f dG/ds = s^(-5/2) What(s)", sp.simplify(sp.diff(Gs, sv) - sv**sp.Rational(-5, 2) * What) == 0))
serG = sp.series(Gs, sv, 0, 4).removeO()
OK.append(check("K8g G(s) series starts (2/9) s^(3/2) + (1/10) s^(5/2)", sp.simplify(serG - (sp.Rational(2, 9) * sv**sp.Rational(3, 2) + sv**sp.Rational(5, 2) / 10 + sp.Rational(2, 35) * sv**sp.Rational(7, 2))) == 0,
                f"{serG}"))
# flat effective potential of the static law (A1): with R(u_law) = g_N = Mb/r^2 the frozen push from r to the edge is Mb/r - Mb/Re;
# deep-regime exterior push = (m_e)^2/(3 a0 Re^3) = Mb/(3 Re)  => mu = -(2/3) Mb/Re
Mb_, Re_ = sp.symbols("M_b R_e", positive=True)
me = sp.sqrt(a0 * Mb_) * Re_                        # deep law at the edge: (m/Re^2)^2/a0 = Mb/Re^2
push_out = sp.integrate((me / rr**2)**2 / a0, (rr, Re_, sp.oo))
mu = sp.simplify(-Mb_ / rr + (Mb_ / rr - Mb_ / Re_) + push_out)
OK.append(check("K8h (A1) flat frozen potential of the deep law with edge Re: mu = -(2/3) M_b/R_e", sp.simplify(mu + sp.Rational(2, 3) * Mb_ / Re_) == 0,
                f"mu = {mu}"))
# co-moving (own-mass) binding in the deep law: -Mb/r + m^2/(3 a0 r^3), m = sqrt(a0 Mb) r  -> -(2/3) Mb/r
mq = sp.sqrt(a0 * Mb_) * rr
OK.append(check("K8i co-moving deep binding -M_b/r + Pi_q = -(2/3) M_b/r", sp.simplify(-Mb_ / rr + mq**2 / (3 * a0 * rr**3) + sp.Rational(2, 3) * Mb_ / rr) == 0))
# oscillation frequency of a single-stream shell about the law (point mass): omega^2 = -dF/dr at fixed m
mloc = sp.symbols("m_loc", positive=True)
Fr = -Mb_ / rr**2 + Rk(mloc / rr**2)
om2 = sp.simplify(-sp.diff(Fr, rr))
om2_deep = sp.limit((om2.subs(mloc, sp.sqrt(a0 * Mb_) * rr) * rr**3 / Mb_), a0, sp.oo)
OK.append(check("K8j deep-limit oscillation omega^2 = 2 G M_b / r^3 (point mass, single stream)", sp.simplify(om2_deep - 2) == 0, f"{om2_deep}"))

ok_all = all(OK)
RES.update(lane="CFG939", part="sym", criteria="3524438b2", amendment="7dace0a16", all_pass=ok_all, n_checks=len(OK),
           n_pass=int(sum(OK)), peak_rss_mb=round(rss_mb(), 1))
P(f"\nSYM: {sum(OK)}/{len(OK)} PASS; peak RSS {rss_mb():.0f} MB.  kappa = 1/2 FITTED; not theory closed.")
open(os.path.join(HERE, "cfg939_sym.out"), "w").write("\n".join(LINES) + "\n")
json.dump(RES, open(os.path.join(HERE, "cfg939_sym_results.json"), "w"), indent=1)
sys.exit(0 if ok_all else 1)
