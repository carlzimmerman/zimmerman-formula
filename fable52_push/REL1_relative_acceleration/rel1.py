"""REL1 step 1 (criteria e495153acf): definition and consistency of the relative-acceleration action.

TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

Items: KA1-KA3 (known answers), K1 (limits of D and D', 2+1 exact / weak-field series), K2 (Hessian of J(|A_rel|) in
the baryons' second time derivative, linearized Euler-Lagrange roots, runaway rates), K3 (stiffness: Sherman-Morrison
form), K4 (nonlinear 1D blow-up with conserved Ostrogradsky energy; KA4 linear rate), K5 (unvaried u_b), K6 (WEP).
MUTATE: REL1_MUTATE = M1 (Christoffel sign flipped in K1), M2 (u_b coupling removed: A_rel = A), M3 (J concave).
Outputs: rel1.out / rel1.json, or rel1_MUTATE_<M>.out / .json.
"""
import json
import math
import os
import sys
import time

import sympy as sp
from scipy.integrate import solve_ivp

MUT = os.environ.get("REL1_MUTATE", "")
TAG = f"_MUTATE_{MUT}" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = open(os.path.join(HERE, f"rel1{TAG}.out"), "w")
RES = {"mutate": MUT}


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.write(s + "\n")
    OUT.flush()


t0 = time.time()
say(f"REL1 step 1 (criteria e495153acf). MUTATE = {MUT or 'none'}. kappa = 1/2 FITTED; not theory closed.")

# ---------------------------------------------------------------- constants (SI)
G = 6.674e-11
K_SI = 4 * math.pi * G
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
YEAR = 3.15576e7
AGE = 13.8e9 * YEAR
MP = 1.6726e-27
RHO = {
    "water": 1000.0, "rock": 3000.0, "Earth (mean)": 5514.0, "platinum": 21450.0, "titanium": 4507.0,
    "ISM gas 1 cm^-3": 1e6 * MP, "halo gas 1e-4 cm^-3": 1e2 * MP, "mean baryon density": 4.21e-28,
}

# ---------------------------------------------------------------- KA1: Legendre (QX17 K0)
p, y, a0, K = sp.symbols("p y a0 K", positive=True)
W = (a0**2 / K) * (-K * p / a0 - sp.log(1 - K * p / a0))
pstar = sp.solve(sp.Eq(y, sp.diff(W, p)), p)[0]
Jy = sp.simplify(pstar * y - W.subs(p, pstar))
Jtarget = (a0**2 / K) * (y / a0 - sp.log(1 + y / a0))
ka1 = sp.simplify(sp.expand_log(Jy - Jtarget, force=True))
RES["KA1"] = {"residual": str(ka1), "pass": ka1 == 0}
say(f"KA1 Legendre max_P[P y - W(K P)] - (a0^2/K)[u - ln(1+u)] = {ka1}  -> {'PASS' if ka1 == 0 else 'FAIL'}")
Jfun = sp.Lambda(y, Jtarget)
if MUT == "M3":
    Jfun = sp.Lambda(y, -Jtarget)  # concave J

# ---------------------------------------------------------------- KA2: law from the static balance (coupling off)
g, gN = sp.symbols("g g_N", positive=True)
mu = (g / a0) / (1 + g / a0)
ka2 = sp.simplify(sp.solve(sp.Eq(mu * g, gN), gN)[0] * (g + a0) - g**2)
RES["KA2"] = {"residual": str(ka2), "pass": ka2 == 0}
say(f"KA2 static spherical balance mu(g/a0) g = g_N  <=>  g^2 = g_N (g + a0): residual {ka2} -> {'PASS' if ka2 == 0 else 'FAIL'}"
    "  (record certificate: Lean QX1.balance_iff_lawS)")

# ---------------------------------------------------------------- KA3: dust-only limit
Pv = sp.symbols("P1 P2")
Ar = sp.symbols("Ar1 Ar2")
new_term = sum(Pv[i] * Ar[i] for i in range(2))
ka3 = new_term.subs({Pv[0]: 0, Pv[1]: 0})
RES["KA3"] = {"pass": ka3 == 0}
say(f"KA3 dust-only (P = 0): P.A_rel = {ka3}; W(0) = {sp.simplify(W.subs(p, 0))}; F(0) = 0 -> GR + clock dust + baryons: "
    f"{'PASS' if ka3 == 0 and sp.simplify(W.subs(p, 0)) == 0 else 'FAIL'}")

# ---------------------------------------------------------------- K1: limits, 2+1
say("\nK1 limits of D: A_rel = h . n.nabla(u_b/gamma), and D': A_rel = A - h . a_b")
T, x1, x2, e = sp.symbols("T x y e")
X = (T, x1, x2)
SGN = -1 if MUT == "M1" else 1


def christoffel(gm, deriv):
    gi = gm.inv()
    n = gm.shape[0]
    return [[[sp.simplify(sum(gi[a, d] * (deriv(gm[d, b], c) + deriv(gm[d, c], b) - deriv(gm[b, c], d))
                               for d in range(n)) / 2) for c in range(n)] for b in range(n)] for a in range(n)]


def cov_along(Gam, vec, field, deriv):
    """(vec . nabla field)^a = vec^r (d_r field^a + Gam^a_{r s} field^s); Christoffel sign SGN (M1 flips)."""
    n = len(field)
    return [sum(vec[r] * (deriv(field[a], r) + SGN * sum(Gam[a][r][s] * field[s] for s in range(n))) for r in range(n))
            for a in range(n)]


def lower(gm, v):
    return [sum(gm[a, b] * v[b] for b in range(len(v))) for a in range(len(v))]


def project(gm, nvec, V):
    nl = lower(gm, nvec)
    nV = sum(nl[a] * V[a] for a in range(len(V)))
    return [V[a] + nvec[a] * nV for a in range(len(V))]


# (i)/(ii): exact static metric diag(-N^2, B^2, B^2), static clock, steady baryon flow (arbitrary U1, U2)
N = sp.Function("N")(x1, x2)
B = sp.Function("B")(x1, x2)
U1 = sp.Function("U1")(x1, x2)
U2 = sp.Function("U2")(x1, x2)
gs = sp.diag(-N**2, B**2, B**2)


def dstat(f, i):
    return 0 if i == 0 else sp.diff(f, X[i])


Gs = christoffel(gs, dstat)
nst = [1 / N, 0, 0]
U0 = sp.sqrt((1 + B**2 * (U1**2 + U2**2)) / N**2)
ub = [U0, U1, U2]
gam = -sum(lower(gs, nst)[a] * ub[a] for a in range(3))
Aclock = project(gs, nst, cov_along(Gs, nst, nst, dstat))
DD = project(gs, nst, cov_along(Gs, nst, [ub[a] / gam for a in range(3)], dstat))
res_ii = [sp.simplify(DD[a] - Aclock[a]) for a in range(3)]
res_i = [sp.simplify((DD[a] - Aclock[a]).subs({U1: 0, U2: 0}).doit()) for a in range(3)]
A_is = [sp.simplify(Aclock[a]) for a in range(3)]
say(f"  clock acceleration A (static clock, exact) = {A_is}")
say(f"  (i)  u_b = n (comoving):                   D - A = {res_i}")
say(f"  (ii) static clock, ANY steady baryon flow: D - A = {res_ii}")
k1_i = all(r == 0 for r in res_i)
k1_ii = all(r == 0 for r in res_ii)
# D' with held baryons (u_b = n): a_b = A, so D' = 0; with geodesic baryons a_b = 0 so D' = A (definition)
ab_held = project(gs, nst, cov_along(Gs, nst, nst, dstat))
Dp_held = [sp.simplify(Aclock[a] - ab_held[a]) for a in range(3)]
say(f"  D' with baryons held at rest beside a static clock: A - h.a_b = {Dp_held}  (the law is OFF in any held medium)")

# (iii): weak static metric, moving clock, baryons at rest. Phi ~ e^2, clock speed ~ e, d/dt ~ e d/dT.
phi = sp.Function("phi")(x1, x2)
V1 = sp.Function("V1")(T, x1, x2)
V2 = sp.Function("V2")(T, x1, x2)
gw = sp.diag(-(1 + 2 * e**2 * phi), 1 - 2 * e**2 * phi, 1 - 2 * e**2 * phi)


def dw(f, i):
    return e * sp.diff(f, T) if i == 0 else sp.diff(f, X[i])


Gw = christoffel(gw, dw)
nraw = [1, e * V1, e * V2]
nn = sum(lower(gw, nraw)[a] * nraw[a] for a in range(3))
ncl = [c / sp.sqrt(-nn) for c in nraw]
ubr = [1 / sp.sqrt(1 + 2 * e**2 * phi), 0, 0]
gam_w = -sum(lower(gw, ncl)[a] * ubr[a] for a in range(3))
Dw = project(gw, ncl, cov_along(Gw, ncl, [ubr[a] / gam_w for a in range(3)], dw))


def ser(expr, order=3):
    return sp.simplify(sp.series(expr, e, 0, order).removeO())


res_iii = [ser(Dw[i]) - e**2 * sp.diff(phi, X[i]) for i in (1, 2)]
res_iii = [sp.simplify(r) for r in res_iii]
say(f"  (iii) clock moving with velocity e V(T,x,y), baryons at rest, Phi = e^2 phi:")
say(f"        D^i to O(e^2) minus e^2 d_i phi = {res_iii}")
k1_iii = all(r == 0 for r in res_iii)
# D': A - h.a_b with a_b of the static observer
abw = project(gw, ncl, cov_along(Gw, ubr, ubr, dw))
res_iii_p = [sp.simplify(sp.series(abw[i], e, 0, 3).removeO() - e**2 * sp.diff(phi, X[i])) for i in (1, 2)]
say(f"        D' = A - h.a_b: (h.a_b)^i to O(e^2) minus e^2 d_i phi = {res_iii_p}  (free-falling clock, A = 0: D' = -grad Phi)")
k1_iii_p = all(r == 0 for r in res_iii_p)
# flat space, static clock, time-dependent baryon flow: D carries d_t v_b (the baryons' second time derivative)
vb = sp.Function("vb")(T, x1, x2)
flat = sp.diag(-1, 1, 1)
Gf = christoffel(flat, dw)
ubf = [1 / sp.sqrt(1 - e**2 * vb**2), e * vb / sp.sqrt(1 - e**2 * vb**2), 0]
gf = -sum(lower(flat, [1, 0, 0])[a] * ubf[a] for a in range(3))
Df = project(flat, [1, 0, 0], cov_along(Gf, [1, 0, 0], [ubf[a] / gf for a in range(3)], dw))
Df_x = sp.simplify(Df[1])
say(f"  (d) flat space, static clock, baryon flow e vb(T,x,y) along x: D^x = {Df_x}  (exact: d_t of the flow)")
k1_d = sp.simplify(Df_x - e**2 * sp.diff(vb, T)) == 0
RES["K1"] = {"i": k1_i, "ii": k1_ii, "iii_D": k1_iii, "iii_Dprime": k1_iii_p, "flat_dt": k1_d,
             "Dprime_held_static": [str(r) for r in Dp_held],
             "pass": bool(k1_i and k1_ii and k1_iii and k1_iii_p and k1_d)}
say(f"  K1: (i) {k1_i}, (ii) {k1_ii}, (iii) D {k1_iii}, (iii) D' {k1_iii_p}, flat d_t {k1_d} -> "
    f"{'PASS' if RES['K1']['pass'] else 'FAIL'}")

# ---------------------------------------------------------------- K2: Hessian in xi'' and the runaway
say("\nK2 matter kinetic structure. About a background with A_rel = y0 (u = |y0|/a0) and baryons at rest, a uniform")
say("   displacement xi(t) changes A_rel by xi'' (K1(d); D' likewise through a_b). P has no time derivative in (A),")
say("   so at gamma_L = 0 P is eliminated: L_matter = rho xi'^2/2 + J(|y0 + c xi''|) - k xi^2/2 (c = 1; M2: c = 0).")
u = sp.symbols("u", nonnegative=True)
z1, z2 = sp.symbols("z1 z2", real=True)
cpl = 0 if MUT == "M2" else 1
yv = sp.Matrix([u * a0 + cpl * z1, cpl * z2])
Jz = Jfun(sp.sqrt(yv.dot(yv)))
H = sp.Matrix(2, 2, lambda i, j: sp.diff(Jz, [z1, z2][i], [z1, z2][j])).subs({z1: 0, z2: 0})
H = sp.simplify(H)
Hpar = sp.simplify(H[0, 0])
Hperp = sp.simplify(sp.limit(H[1, 1], u, 0, "+") if False else H[1, 1])
say(f"  Hessian of J in xi'' : along A_rel {Hpar} ; across A_rel {Hperp} ; off-diagonal {sp.simplify(H[0, 1])}")
nondeg = (sp.simplify(Hpar) != 0) and (sp.simplify(Hperp) != 0)
# 1D Euler-Lagrange with sympy and its characteristic roots
tt = sp.symbols("t")
xi = sp.Function("xi")(tt)
rho, kk, s = sp.symbols("rho k s")
Hs = sp.simplify(Hpar.subs(u, 0))  # H at the background u = 0 (1/K for the physical J)
L2 = rho * sp.diff(xi, tt)**2 / 2 + Hs * sp.diff(xi, tt, 2)**2 / 2 - kk * xi**2 / 2
EL = sp.euler_equations(L2, [xi], [tt])[0].lhs
char = sp.simplify(EL.subs(xi, sp.exp(s * tt)).doit() / sp.exp(s * tt))
roots = sp.solve(sp.Eq(char, 0), s**2) if char.has(s) else []
say(f"  linearized Euler-Lagrange: {sp.simplify(EL)} = 0")
say(f"  characteristic polynomial in s (xi ~ e^(s t)): {sp.factor(char)};  s^2 roots: {roots}")
# Ostrogradsky Hamiltonian
q1, q2, p1, p2 = sp.symbols("q1 q2 p1 p2")
if Hs != 0:
    a_of_p2 = p2 / Hs
    Ham = p1 * q2 + p2 * a_of_p2 - (rho * q2**2 / 2 + Hs * a_of_p2**2 / 2 - kk * q1**2 / 2)
    Ham = sp.simplify(Ham)
else:
    Ham = sp.simplify(q2 * q2 * rho / 2 + kk * q1**2 / 2)  # ordinary second-order system: H = rho v^2/2 + k x^2/2
say(f"  Ostrogradsky Hamiltonian (q1 = xi, q2 = xi', p2 = H xi''): H_O = {Ham};  d^2 H_O/dp1^2 = {sp.diff(Ham, p1, 2)}"
    f"  -> linear in p1, unbounded below when the H xi''^2 term is present (H != 0)")
# physical rates
rates = {}
Hpar_num = sp.lambdify((u, a0, K), Hpar.subs({}), "math") if nondeg else None
Hperp_num = sp.lambdify((u, a0, K), Hperp, "math") if nondeg else None
say("\n  runaway rates s = sqrt(rho / H) (k = 0), SI, K = 4 pi G:")
for foot, a0v in A0.items():
    rates[foot] = {}
    cases = [("u = 0 (free-falling compact body under D; any body at A_rel = 0)", 0.0),
             ("lab mass at rest on Earth under D (u = 9.81/a0)", 9.81 / a0v),
             ("test mass in Earth orbit r = 7081 km under D' (u = g/a0)", 3.986004e14 / 7.081e6**2 / a0v)]
    for label, uu in cases:
        rows = {}
        for mname, rv in RHO.items():
            if not nondeg:
                rows[mname] = None
                continue
            hp, ht = Hpar_num(uu, a0v, K_SI), Hperp_num(uu, a0v, K_SI)
            sp_par = math.sqrt(rv / hp) if hp > 0 else float("nan")
            sp_perp = math.sqrt(rv / ht) if ht > 0 else float("nan")
            rows[mname] = {"s_along": sp_par, "s_across": sp_perp,
                           "efold_along_s": 1 / sp_par if sp_par == sp_par else None,
                           "efold_across_s": 1 / sp_perp if sp_perp == sp_perp else None,
                           "faster_than_age": (1 / min(sp_par, sp_perp) < AGE) if sp_par == sp_par else None}
        rates[foot][label] = rows
        say(f"  [{foot}] {label}")
        for mname, r in rows.items():
            if r is None or r["efold_along_s"] is None:
                say(f"      {mname:22s}  no real runaway root (H <= 0 or degenerate)")
            else:
                say(f"      {mname:22s}  e-fold along {r['efold_along_s']:.3e} s ; across {r['efold_across_s']:.3e} s"
                    f"  ({r['efold_across_s'] / YEAR:.3e} yr); faster than the age: {r['faster_than_age']}")
s2pos = [r for r in roots if sp.simplify(r.subs({rho: 1, kk: 0, K: 1, a0: 1})) > 0]
runaway = nondeg and len(s2pos) > 0 and (MUT != "M3")
_w = rates["canonical"]["u = 0 (free-falling compact body under D; any body at A_rel = 0)"]["water"]
S1_fail = bool(runaway and _w is not None and _w["faster_than_age"])
RES["K2"] = {"H_along": str(Hpar), "H_across": str(Hperp), "nondegenerate": bool(nondeg),
             "char": str(sp.factor(char)), "s2_roots": [str(r) for r in roots], "ostrogradsky_H": str(Ham),
             "rates": rates, "S1_fails": S1_fail}
say(f"  K2: Hessian non-degenerate {nondeg}; real runaway root {runaway}; S1 (Ostrogradsky) FAILS: {S1_fail}")

# ---------------------------------------------------------------- K3: the stiffness does not remove it
say("\nK3 gamma_L > 0. Maximizing -dP.M.dP/2 + dP.b - (gamma/2)(k.dP)^2 over dP (M = W'' > 0, b = (1+gamma Pi) dA_rel)")
say("   gives b.(M + gamma k k^T)^-1.b. Sherman-Morrison and Cauchy-Schwarz: >= 0, = 0 only for b parallel to k.")
m1, m2, gl, kx, ky, bx, by = sp.symbols("m1 m2 gamma kx ky bx by", positive=True)
Mm = sp.diag(m1, m2)
kv = sp.Matrix([kx, ky])
Heff = sp.simplify((sp.Matrix([bx, by]).T * (Mm + gl * kv * kv.T).inv() * sp.Matrix([bx, by]))[0])
Heff_t = sp.simplify(Heff.subs({bx: ky, by: -kx * m1 / m2 * 0 - kx}))  # a b not parallel to k (b = (ky, -kx) is transverse)
Heff_trans = sp.simplify(Heff.subs({bx: ky, by: -kx}).subs(m2, m1))
say(f"  b.(M + gamma k k^T)^-1.b = {sp.factor(Heff)}")
say(f"  transverse b = (ky, -kx), isotropic M = m1: {Heff_trans}  (gamma drops out: stiffness does not act)")
k3 = sp.simplify(Heff_trans - (kx**2 + ky**2) / m1) == 0
RES["K3"] = {"Heff": str(sp.factor(Heff)), "transverse_isotropic": str(Heff_trans), "gamma_free": bool(k3)}
say(f"  K3: transverse displacement patterns keep H = 1/M (gamma_L free) -> {'the runaway survives the stiffness' if k3 else 'CHECK'}")

# ---------------------------------------------------------------- K4: nonlinear 1D blow-up, Ostrogradsky energy
say("\nK4 nonlinear 1D: L = xdot^2/2 - g x + J(xddot + g) (units rho = K = a0 = 1). EL: xddot + g = d^2 J'(y)/dt^2,")
say("   so q = J'(y) = y/(1+|y|) obeys q'' = y(q) = q/(1 - |q|): q reaches 1 (y infinite) in finite time.")
sgnJ = -1.0 if MUT == "M3" else 1.0
gacc = 1.0


def y_of_q(q):
    return q / (1 - abs(q)) if sgnJ > 0 else -q / (1 - abs(q))


def rhs(t, Z):
    x, xd, q, qd = Z
    yy = y_of_q(q) if cpl else 0.0
    return [xd, yy - gacc, qd, yy if cpl else 0.0]


def Jval(yy):
    return sgnJ * (abs(yy) - math.log1p(abs(yy)))


def H_terms(Z):
    x, xd, q, qd = Z
    yy = y_of_q(q)
    return [0.5 * xd**2, -xd * qd, q * (yy - gacc), gacc * x, -Jval(yy)]


def H_O(Z):
    x, xd, q, qd = Z
    yy = y_of_q(q)
    return 0.5 * xd**2 - xd * qd + q * (yy - gacc) + gacc * x - Jval(yy)


eps = 1e-12
Z0 = [0.0, 0.0, eps, eps]


def near_one(t, Z):
    return 1 - 1e-9 - abs(Z[2])


near_one.terminal = True
sol = solve_ivp(rhs, (0, 80), Z0, rtol=1e-12, atol=1e-30, events=near_one, dense_output=True, method="DOP853")
Tb = sol.t_events[0][0] if len(sol.t_events[0]) else None
Hs_ = [H_O(sol.y[:, i]) for i in range(sol.y.shape[1])]
Hscale = max(abs(h) for h in Hs_) or 1.0
Hdrift = max(abs(H_O(sol.y[:, i]) - Hs_[0]) / max(abs(v) for v in H_terms(sol.y[:, i])) for i in range(sol.y.shape[1]))  # A1 (post hoc)
# KA4: early growth rate
t_a, t_b = 2.0, 10.0
if Tb is None or Tb > t_b:
    qa, qb = sol.sol(t_a)[2], sol.sol(t_b)[2]
    rate = math.log(abs(qb / qa)) / (t_b - t_a)
else:
    rate = float("nan")
ka4 = abs(rate - 1.0) < 1e-3
say(f"  blow-up time from eps = 1e-12: T = {Tb} (units 1/sqrt(K rho)); ln(1/eps) = {math.log(1 / eps):.3f}")
say(f"  KA4 small-amplitude growth rate {rate:.6f} (expect 1) -> {'PASS' if ka4 else 'FAIL'}")
say(f"  Ostrogradsky energy relative drift {Hdrift:.2e} (A1: per time, over the largest of its terms; line 1e-8) -> {'PASS' if Hdrift < 1e-8 else 'FAIL'}")
phys = {}
if Tb is not None:
    for mname, rv in RHO.items():
        phys[mname] = Tb / math.sqrt(K_SI * rv)
        say(f"      {mname:22s} blow-up after {phys[mname]:.3e} s = {phys[mname] / 3600:.3e} h = {phys[mname] / YEAR:.3e} yr")
RES["K4"] = {"T_blowup_scaled": Tb, "rate_scaled": rate, "KA4_pass": ka4, "H_drift": Hdrift,
             "H_pass": Hdrift < 1e-8, "T_blowup_SI_s": phys}

# ---------------------------------------------------------------- K5: unvaried u_b
say("\nK5 the other exit: u_b a prescribed background (not varied). Then the baryons stay geodesic (div T_b = 0) while")
say("   the P sector's Lagrangian J(|A_rel(t)|) depends explicitly on the prescribed flow; its energy changes at")
say("   dE/dt = -dL/dt|explicit. In the reduced system with x_b(t) prescribed:")
xb = sp.Function("x_b")(tt)
Lp = Jfun(sp.diff(xb, tt, 2) + sp.Symbol("g0"))
Eexch = sp.simplify(sp.diff(Jfun(sp.diff(xb, tt, 2) + sp.Symbol("g0")), sp.diff(xb, tt, 2)))
say(f"   the source the baryons would have felt (dL/dx_b'' = J'(y)) = {Eexch}; nonzero unless y = 0, so the non-GR stress")
say("   is not conserved and the Einstein equation's divergence (Bianchi: identically zero) cannot be matched: inconsistent.")
RES["K5"] = {"exchange": str(Eexch), "consistent": False}

# ---------------------------------------------------------------- K6: WEP
say("\nK6 WEP.")
say("   D: a compact free-falling body has A_rel = xddot + grad Phi = 0 inside it, so J'(0) = 0: no first-order force;")
say("      but the free fall itself runs away at s = sqrt(4 pi G rho), a rate set by the body's density (K2):")
for mname in ("platinum", "titanium"):
    say(f"      {mname}: e-fold {1 / math.sqrt(K_SI * RHO[mname]):.1f} s")
wep = {}
omega = math.sqrt(3.986004e14 / 7.081e6**3)
gorb = 3.986004e14 / 7.081e6**2
for foot, a0v in A0.items():
    Psat = a0v / K_SI
    da = Psat * omega**2 * abs(1 / RHO["titanium"] - 1 / RHO["platinum"])
    wep[foot] = {"P_sat": Psat, "delta_a": da, "eta": da / gorb, "over_MICROSCOPE": da / gorb / 1e-15}
    say(f"   D' [{foot}]: order-reduced force (1/rho) d^2(J' yhat)/dt^2 on a test mass in Earth orbit, unscreened")
    say(f"      P = a0/K = {Psat:.4f} kg/m^2: Ti - Pt differ by {da:.2e} m/s^2, eta = {da / gorb:.2e} "
        f"= {da / gorb / 1e-15:.1e} x MICROSCOPE's 1e-15 (argued; screening not modelled)")
RES["K6"] = {"Dprime_unscreened": wep}

# ---------------------------------------------------------------- verdict
ka_ok = RES["KA1"]["pass"] and RES["KA2"]["pass"] and RES["KA3"]["pass"] and RES["K4"]["KA4_pass"] if not MUT else None
if not MUT:
    if not ka_ok or not RES["K4"]["H_pass"]:
        label = "NO VERDICT"
    elif not RES["K1"]["pass"]:
        label = "NOT WELL-DEFINED (a required limit fails)"
    elif S1_fail:
        label = "NOT WELL-DEFINED (Ostrogradsky runaway of ordinary matter; S1)"
    else:
        label = "step 1 passes"
    RES["label_both_footings"] = label
    say(f"\nLABEL (canonical and alt, step 1): {label}")
else:
    say(f"\nMUTATE {MUT}: K1 pass {RES['K1']['pass']}; Hessian non-degenerate {RES['K2']['nondegenerate']}; "
        f"s^2 roots {RES['K2']['s2_roots']}; runaway (S1 fails) {RES['K2']['S1_fails']}; K4 T_blowup {Tb}, rate {rate}")
RES["runtime_s"] = time.time() - t0
say(f"runtime {RES['runtime_s']:.1f} s. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
json.dump(RES, open(os.path.join(HERE, f"rel1{TAG}.json"), "w"), indent=1, default=str)
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
