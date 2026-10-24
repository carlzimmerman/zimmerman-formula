#!/usr/bin/env python3
"""M5_equilibrium_law: can the galaxy law be the equilibrium (attractor) of a normally self-gravitating medium?

Frozen criteria: FROZEN_CRITERIA.md (a364a6df13). kappa = 1/2 FITTED. Footings never pooled. Cold energy = medium of
real rest mass, no particle. Not "theory closed". Nothing here says the data favour the framework.
Run: OMP_NUM_THREADS=1 nice -n 15 python3 m5_equilibrium_law.py [--mutate]
"""
import os, sys, json, math, time, resource, csv
import numpy as np
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data")
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LSTAR_PC = {"canonical": 21.7, "alt": 22.9}            # D10 floors
FOOTS = ("canonical", "alt")
G_SI = 6.674e-11; KPC_S = 3.0857e19; PC = 3.0857e16; MSUN = 1.989e30
H0 = 67.9; T_H = 1.0 / (H0 * 1e3 / 3.0857e22)        # 1/H0 in s
LN10 = math.log(10.0)
OUT = []; RES = {"lane": "M5_equilibrium_law", "mutate": MUT, "checks": {}, "rows": {}, "theorems": {}}
CHECKS = []


def P(*a):
    s = " ".join(str(x) for x in a); OUT.append(s); print(s, flush=True)


def check(k, ok, val, thr, det=""):
    ok = bool(ok); CHECKS.append((k, ok))
    RES["checks"][k] = dict(ok=ok, value=val, threshold=thr, detail=det)
    P(f"{k} {'PASS' if ok else 'FAIL'}  value={val}  line={thr}" + (f"  [{det}]" if det else ""))


P(__doc__.strip()); P(f"mutate={MUT}")

# ============================================================================ S-checks (sympy)
P("\n=== S1  3D existence: the law's stress (AQUAL minus Newton) balances the phantom on any Phi")
x, y, z = sp.symbols("x y z", real=True)
Gs, a0s = sp.symbols("G a0", positive=True)
rng = np.random.default_rng(5)
coef = [sp.Rational(int(c), 7) for c in rng.integers(-9, 10, 35)]
mons = [x**i * y**j * z**k for i in range(5) for j in range(5) for k in range(5) if 1 <= i + j + k <= 4][:35]
Phi = sum(c * m for c, m in zip(coef, mons)) + (x**2 + y**2 + z**2) * 3
X = (x, y, z)
grad = [sp.diff(Phi, v) for v in X]
s = sum(gi**2 for gi in grad)
xa = sp.sqrt(s) / a0s
mu_law = xa / (1 + xa)
mu_stress = (xa / sp.sqrt(1 + xa**2)) if MUT else mu_law          # M1 plant
chi_l, chi_s = 1 - mu_law, 1 - mu_stress
# K(s) with K'(s) = chi/2 : for mu = x/(1+x): K = a0^2 (x - ln(1+x)); for the standard mu: a0^2 (sqrt(1+x^2) - x ... ) built by quadrature-free form
if not MUT:
    K = a0s**2 * (xa - sp.log(1 + xa))
else:
    K = a0s**2 * (xa**2 / 2 - (sp.sqrt(1 + xa**2) - 1))              # K' = (1 - x/sqrt(1+x^2))/2 * ... (M1 stress)
Pi = [[(chi_s * grad[i] * grad[j] - (K if i == j else 0)) / (4 * sp.pi * Gs) for j in range(3)] for i in range(3)]
rho_ph = sum(sp.diff(chi_l * grad[j], X[j]) for j in range(3)) / (4 * sp.pi * Gs)
resid = [sum(sp.diff(Pi[i][j], X[j]) for j in range(3)) - rho_ph * grad[i] for i in range(3)]
fres = sp.lambdify((x, y, z, Gs, a0s), resid, "mpmath")
fscale = sp.lambdify((x, y, z, Gs, a0s), [rho_ph * gi for gi in grad], "mpmath")
import mpmath as mpm
mpm.mp.dps = 40
worst = 0.0
for _ in range(20):
    pt = [mpm.mpf(float(v)) for v in rng.uniform(-1.5, 1.5, 3)]
    a0v = mpm.mpf(float(10 ** rng.uniform(-1, 1)))
    r_ = fres(*pt, mpm.mpf(1), a0v); sc = fscale(*pt, mpm.mpf(1), a0v)
    n = max(abs(v) for v in r_); d = max(abs(v) for v in sc) + mpm.mpf("1e-30")
    worst = max(worst, float(n / d))
check("S1", worst <= 1e-12, f"{worst:.2e}", "<=1e-12", "relative residual of div(Pi) - rho_ph grad Phi at 20 random points, quartic Phi, random a0")
RES["theorems"]["S1"] = "Pi_ij = [chi dPhi_i dPhi_j - K(s) delta_ij]/4piG, K'=chi/2, chi=1-mu: div Pi = rho_ph grad Phi exactly in 3D (AQUAL)"

P("\n=== S2  uniqueness (spherical jets, then 3D jets): the stress cannot respond to rho_c")
r, g, g1, g2, rho = sp.symbols("r g g1 g2 rho", positive=True)
Mfun = sp.Function("M")          # generic mu(g)
h = (1 - Mfun(g)) * g
hg = sp.diff(h, g)
rho_ph_sph = (2 * h / r + hg * g1) / (4 * sp.pi * Gs)
# step 1: A(rho, g): dA/dr = A_rho * drho/dr + A_g g1 ; drho/dr contains g2 with coefficient d rho/d g1
Arho, Ag, Bv = sp.symbols("A_rho A_g B")
drho_dr = sp.diff(rho_ph_sph, r) + sp.diff(rho_ph_sph, g) * g1 + sp.diff(rho_ph_sph, g1) * g2
Av = sp.Symbol("A")
res_sph = Arho * drho_dr + Ag * g1 + 2 * (Av - Bv) / r - rho_ph_sph * g
c_g2 = sp.simplify(sp.diff(res_sph, g2))
step1 = sp.solve(sp.Eq(c_g2, 0), Arho)
ok1 = step1 == [0]
# step 2: with A_rho = 0, solve for B, express g1 through (rho, r) at fixed g, demand dB/dr|_{rho,g} = 0
res2 = res_sph.subs(Arho, 0)
Bsol = sp.solve(sp.Eq(res2, 0), Bv)[0]
g1_of = sp.solve(sp.Eq(rho_ph_sph, rho), g1)[0]
B_rho_r = sp.simplify(Bsol.subs(g1, g1_of))
dBdr = sp.simplify(sp.diff(B_rho_r, r))
Ag_sol = sp.solve(sp.Eq(dBdr, 0), Ag)
ok2 = len(Ag_sol) == 1 and sp.simplify(Ag_sol[0] - g * hg / (4 * sp.pi * Gs)) == 0
Bfin = sp.simplify(B_rho_r.subs(Ag, Ag_sol[0]))
ok3 = sp.simplify(sp.diff(Bfin, rho)) == 0 and sp.simplify(Bfin - (Av - g * h / (4 * sp.pi * Gs))) == 0
P(f"  spherical: coefficient of g'' = A_rho * {sp.simplify(c_g2 / Arho)}  ->  A_rho = {step1}")
P(f"  dP_par/dg forced = {Ag_sol}  ;  P_perp = A - g h/4piG, d/drho = 0: {ok3}")
# 3D jets
p1 = sp.symbols("p1:4");
H = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"p{min(i,j)+1}{max(i,j)+1}"))
T3 = {}
for i in range(3):
    for j in range(3):
        for k in range(3):
            key = tuple(sorted((i, j, k))); T3[(i, j, k)] = sp.Symbol("q" + "".join(str(v + 1) for v in key))
Ar, Br, As, Bs, A3, B3, ch, chs = sp.symbols("A_r B_r A_s B_s A3 B3 chi chi_s")
sv = sum(p1[i]**2 for i in range(3))
ds = [2 * sum(p1[k] * H[k, j] for k in range(3)) for j in range(3)]                 # d_j s
d2s = [[2 * sum(H[k, j] * H[k, l] + p1[k] * T3[(k, j, l)] for k in range(3)) for l in range(3)] for j in range(3)]
# rho = div(chi grad Phi)/4piG with chi = chi(s): value and gradient (chi_ss enters only via d_j s * d_l s)
chss = sp.Symbol("chi_ss")
rho3 = (chs * sum(ds[j] * p1[j] for j in range(3)) + ch * sum(H[j, j] for j in range(3))) / (4 * sp.pi * Gs)
drho3 = [(chss * ds[l] * sum(ds[j] * p1[j] for j in range(3)) + chs * sum(d2s[j][l] * p1[j] + ds[j] * H[j, l] for j in range(3))
          + chs * ds[l] * sum(H[j, j] for j in range(3)) + ch * sum(T3[(j, j, l)] for j in range(3))) / (4 * sp.pi * Gs) for l in range(3)]
res3 = []
for i in range(3):
    dA = Ar * drho3[i] + As * ds[i]
    divB = sum((Br * drho3[j] + Bs * ds[j]) * p1[i] * p1[j] + B3 * (H[i, j] * p1[j] + p1[i] * H[j, j]) for j in range(3))
    res3.append(sp.expand(dA + divB - rho3 * p1[i]))
qsyms = sorted({v for v in T3.values()}, key=str)
eqs = []
for e in res3:
    for q in qsyms:
        eqs.append(sp.expand(sp.diff(e, q)))
# numeric random jets to make the linear system in (A_r, B_r) concrete
subsJ = {v: sp.Rational(int(rng.integers(-9, 10)), int(rng.integers(1, 7))) for v in list(p1) + list(H.free_symbols)}
subsJ.update({ch: sp.Rational(3, 7), chs: sp.Rational(-2, 5), chss: sp.Rational(1, 3)})
lin = [sp.simplify(e.subs(subsJ)) for e in eqs]
solr = sp.solve([l for l in lin if l != 0], [Ar, Br], dict=True)
ok4 = solr == [{Ar: 0, Br: 0}]
res3b = [sp.expand(e.subs({Ar: 0, Br: 0})) for e in res3]
eqs2 = []
for e in res3b:
    poly = sp.Poly(e, *(list(p1) + sorted(H.free_symbols, key=str)))
    eqs2 += list(poly.coeffs())
sol2 = sp.solve(eqs2, [As, Bs, B3], dict=True)
ok5 = len(sol2) == 1 and sp.simplify(sol2[0][B3] - ch / (4 * sp.pi * Gs)) == 0 and sp.simplify(sol2[0][As] + ch / (8 * sp.pi * Gs)) == 0 and sp.simplify(sol2[0][Bs] - chs / (4 * sp.pi * Gs)) == 0
P(f"  3D: third-derivative coefficients force (A_rho, B_rho) = {solr}; then {sol2}")
check("S2", ok1 and ok2 and ok3 and ok4 and ok5, f"sph {ok1},{ok2},{ok3}; 3D {ok4},{ok5}", "all True",
      "exact-law equilibrium for every baryon profile forces a stress that does not depend on rho_c; unique up to a constant pressure")
RES["theorems"]["S2"] = ("Any local stress Pi(rho_c, grad Phi) whose static balance reproduces the law for every baryon distribution "
                         "is the S1 stress up to a constant pressure; dPi/drho_c = 0 (density-blind).")

P("\n=== S3  the spherical balance integrates to mu(g/a0) g = G M_b/r^2 (unique by regularity)")
rr = sp.Symbol("r", positive=True)
gf = sp.Function("g")(rr); rhob = sp.Function("rho_b")(rr)
mu_f = sp.Function("mu")
xg = gf / a0s
chig = 1 - mu_f(xg)
Kg = sp.Function("Kg")(rr)                      # K(s(r)), dK/dr = K'(s) ds/dr = (chi/2) * 2 g g'
Prr = (chig * gf**2 - Kg) / (4 * sp.pi * Gs)
Ptt = (-Kg) / (4 * sp.pi * Gs)
if MUT:
    Ptt = Prr                                                               # M2 plant: isotropic
rhoc = sp.diff(rr**2 * gf, rr) / (4 * sp.pi * Gs * rr**2) - rhob
bal = sp.diff(Prr, rr) + 2 * (Prr - Ptt) / rr - rhoc * gf
bal = bal.subs(sp.Derivative(Kg, rr), chig * gf * sp.diff(gf, rr))
target = -(gf / rr**2) * (sp.diff(rr**2 * mu_f(xg) * gf, rr) - 4 * sp.pi * Gs * rr**2 * rhob) / (4 * sp.pi * Gs)
d3 = sp.simplify(sp.expand(bal - target))
check("S3", d3 == 0, str(d3)[:80], "0", "balance == -(g/4piG r^2) [ (r^2 mu g)' - 4piG r^2 rho_b ]  =>  mu g = G M_b/r^2 + C/r^2, C=0")

P("\n=== S4  dynamics of a medium held up by a density-blind stress (Cowling, 1D along the field)")
xx, t, k, sS, gg, c2 = sp.symbols("x t k s g c2")
eps = sp.Symbol("epsilon")
rho0 = sp.Function("rho0")(xx); xi = sp.Function("xi")(xx)
Tb1 = sp.Function("Tb1")(xx)                    # T_b'(x): gradient of the density-blind stress (force density)
acc = (1 + eps * sp.diff(xi, xx)) / rho0 * (Tb1 + eps * sp.diff(Tb1, xx) * xi) \
      - sp.diff(c2 * rho0 / (1 + eps * sp.diff(xi, xx)), xx) / rho0 - gg
lin = sp.expand(sp.series(acc, eps, 0, 2).removeO().coeff(eps))
bg = sp.simplify(acc.subs(eps, 0))
lin_b = sp.expand(lin.subs(c2, 0).subs(Tb1, rho0 * gg).doit())
lin_p = sp.expand(lin.subs(Tb1, rho0 * gg + c2 * sp.diff(rho0, xx)).doit())
P(f"  background (c2=0, T_b' = rho0 g): {sp.simplify(bg.subs(c2, 0).subs(Tb1, rho0*gg))}")
P(f"  rho-blind: xi_tt = {sp.simplify(lin_b)}")
P(f"  + c2:      xi_tt = {sp.simplify(lin_p)}")
prin_b = sp.simplify(lin_b.coeff(sp.Derivative(xi, xx)))
prin_p2 = sp.simplify(lin_p.coeff(sp.Derivative(xi, (xx, 2))))
ok4 = sp.simplify(prin_b - gg) == 0 and sp.simplify(prin_p2 - c2) == 0
check("S4", ok4, f"coef xi'={prin_b}, coef xi''(c2 case)={prin_p2}", "g and c2",
      "principal symbol s^2 = i k g (|Re s| ~ sqrt(kg/2), Hadamard ill-posed); with c2: s^2 = -c2 k^2 + i k g")

P("\n=== S5/S6  force on the medium; deep-regime cancellation; linear FRW growth")
rb, rc, rbar, drc, drb, mterm = sp.symbols("rho_b rho_c rhobar drho_c drho_b mterm")
# identity: div Pi - rho_c gradPhi = (rho_ph - rho_c) gradPhi ; with Poisson 4piG(rho_b+rho_c) = lap Phi: rho_ph = rho_b + rho_c - div(mu gradPhi)/4piG
fpm = ((drb + drc - mterm) - (rbar + drc)) / (rbar + drc)              # per-mass force / (-grad dPhi) with sign: F = fpm * grad dPhi
fpm_s = sp.simplify(fpm)
ok5 = sp.simplify(fpm_s - (-(rbar - drb + mterm) / (rbar + drc))) == 0
lin6 = sp.series(fpm_s.subs({drc: eps * drc, drb: eps * drb, mterm: eps**2 * mterm}), eps, 0, 1).removeO()
ok6 = sp.simplify(lin6 + 1) == 0
check("S5", ok5, str(fpm_s), "-(rhobar - drho_b + mterm)/(rhobar + drho_c)",
      "per-mass force on the medium = -[(rhobar - drho_b + div(mu grad dPhi)/4piG)/(rhobar + drho_c)] grad dPhi; mu-term O(g/a0)")
check("S6", ok6, str(lin6), "-1", "linear order: force per mass = -grad dPhi, so delta'' + 2H delta' = 4piG rhobar delta (dust)")

# ============================================================================ N1 top-hat, N2 operators
P("\n=== N1  spherical top-hat in EdS: dust vs the deep-regime held medium (S5)")


def tophat(deep, d_i=1e-3, mutate_bg=False):
    # units: t_i = 1, a = t^(2/3), (4pi/3) G rhobar = 2/(9 t^2); R_i = 1; growing mode
    def rhs(tt, Y):
        R, V = Y
        a = tt ** (2.0 / 3.0)
        d = (1 + d_i) * (a / R) ** 3 - 1
        bg = 2.0 / (9 * tt**2) * R
        pec = bg * d
        fac = 1.0 / (1.0 + d) if deep else 1.0
        if mutate_bg:
            return [V, -(bg + pec) / (1.0 + d) if not deep else -(bg + pec) / (1.0 + d) ** 2]
        return [V, -bg - pec * fac]
    ev = lambda tt, Y: Y[0] - 1e-4
    ev.terminal = True
    sol = solve_ivp(rhs, [1.0, 1e12], [1.0, (2.0 / 3.0) * (1 - d_i / 3.0)], events=ev, rtol=1e-10, atol=1e-14, method="LSODA")
    if sol.t_events[0].size == 0:
        return None, sol
    tc = sol.t_events[0][0]
    return d_i * (3.0 / 5.0) * 5.0 / 3.0 * tc ** (2.0 / 3.0), sol


# growing-mode IC (delta_i with velocity -delta_i/3 H R) -> linear delta = d_i * a exactly
dc_dust, sd = tophat(False, mutate_bg=MUT)
dc_deep, sdeep = tophat(True)
P(f"  dust: linear delta at collapse = {dc_dust}")
P(f"  held-in-deep-regime medium: linear delta at collapse = {dc_deep}")
check("N1", dc_dust is not None and abs(dc_dust - 1.686) <= 0.01, f"{dc_dust}", "1.686 +- 0.01", "EdS dust control")
# turnaround of the deep arm and its delay
RES["rows"]["R4_nonlinear"] = dict(delta_c_dust=dc_dust, delta_c_deep=dc_deep,
                                   ratio=(dc_deep / dc_dust) if (dc_deep and dc_dust) else None)
if dc_deep and dc_dust:
    # Press-Schechter collapsed fraction at sigma = 1 and 0.5 (reported)
    from math import erfc
    for sg in (1.0, 0.5):
        P(f"  PS collapsed fraction at sigma={sg}: dust {erfc(dc_dust/(math.sqrt(2)*sg)):.3e}  held {erfc(dc_deep/(math.sqrt(2)*sg)):.3e}")
        RES["rows"]["R4_nonlinear"][f"PS_frac_sigma{sg}"] = [erfc(dc_dust / (math.sqrt(2) * sg)), erfc(dc_deep / (math.sqrt(2) * sg))]

P("\n=== N1b (reported, added after freezing; not a check)  physical top-hats with the mu-term kept (EdS, H0 67.9)")
# per-mass force at the shell: -(g_p) (1 + m/rhobar)/(1 + delta), m/rhobar = (delta/3) g_p (4 a0 + 3 g_p)/(a0 + g_p)^2
# (exact for the stress S1 evaluated at the edge of a uniform sphere; baryons smooth, which is the optimistic case per S5)
t0 = 2.0 / (3.0 * H0 * 1e3 / 3.0857e22)
N1b = {}
for f in FOOTS:
    a0 = A0[f]; N1b[f] = {}
    for lM in (11, 12, 13, 14, 15):
        Msh = 10**lM * MSUN; ai = 1e-3; ti = t0 * ai**1.5; di = 1.686 * ai
        rb_i = 1.0 / (6 * np.pi * G_SI * ti**2); Ri = (3 * Msh / (4 * np.pi * rb_i * (1 + di)))**(1 / 3)
        def rhs(tt, Y, a0=a0, Ri=Ri, ti=ti, di=di):
            R_, V_ = Y
            rb = 1.0 / (6 * np.pi * G_SI * tt**2); a = (tt / t0)**(2 / 3)
            d = (1 + di) * (a * Ri / (ai * R_))**3 - 1
            bgf = (4 * np.pi / 3) * G_SI * rb * R_
            gp = bgf * d
            if d <= 0:
                return [V_, -bgf - gp]
            m = (d / 3) * gp * (4 * a0 + 3 * gp) / (a0 + gp)**2
            return [V_, -bgf - gp * (1 + m) / (1 + d)]
        ev = lambda tt, Y: Y[0] - 1e-3 * Ri
        ev.terminal = True
        sol = solve_ivp(rhs, [ti, t0 * 1000.0], [Ri, (2 / (3 * ti)) * Ri * (1 - di / 3)], events=ev, rtol=1e-9, atol=1e-6 * Ri, method="LSODA")
        ac = (sol.t_events[0][0] / t0)**(2 / 3) if sol.t_events[0].size else None
        N1b[f][f"1e{lM}"] = ac
    P(f"  {f}: collapse scale factor (dust = 1.00) by log M: " + ", ".join(f"{k_}: {('%.2f' % v) if v else '>100'}" for k_, v in N1b[f].items()))
RES["rows"]["R4_nonlinear"]["N1b_collapse_a_dust_at_1"] = N1b

P("\n=== N2  1D operators on a Dirichlet interval (controls for S4)")


def maxres(Nn, c2v, gv=1.0, D=0.0):
    hh = 1.0 / (Nn + 1)
    I = np.eye(Nn)
    D1 = (np.eye(Nn, k=1) - np.eye(Nn, k=-1)) / (2 * hh)
    D2 = (np.eye(Nn, k=1) - 2 * I + np.eye(Nn, k=-1)) / hh**2
    L = c2v * D2 + gv * D1
    if D > 0:
        L = L - D**2 * (D2 @ D2)
    lam = np.linalg.eigvals(L)
    return float(np.max(np.sqrt(lam.astype(complex)).real))


N2 = {}
for Nn in (200, 400, 800):
    N2[Nn] = dict(blind=maxres(Nn, 0.0), stiff=maxres(Nn, 0.05), bohm=maxres(Nn, 0.0, D=0.01))
    P(f"  N={Nn}: max Re s  rho-blind {N2[Nn]['blind']:.3f}   +c2=0.05 {N2[Nn]['stiff']:.2e}   Bohm D=0.01 {N2[Nn]['bohm']:.3f}")
okN2 = N2[800]["blind"] > 1.3 * N2[200]["blind"] and max(abs(N2[n]["stiff"]) for n in N2) <= 1e-6 * 1.0
check("N2", okN2, f"blind {N2[200]['blind']:.2f}->{N2[800]['blind']:.2f}; stiff {N2[800]['stiff']:.1e}", "blind grows with N; stiff <= 1e-6",
      "ill-posed without compressional stiffness; c2 > 0 removes the modal growth on a bounded interval (non-normal: convective growth g/2c remains)")
RES["rows"]["N2"] = {str(k_): v for k_, v in N2.items()}

# ============================================================================ SPARC (own loader)
P("\n=== SPARC: own loader; P4a reproduction; P4c ODE; R2 attractor row; (c) BTFR line")


def load_sparc():
    d_ = os.path.join(DATA, "sparc_data"); gal = []
    for f in sorted(os.listdir(d_)):
        if not f.endswith("_rotmod.dat"):
            continue
        try:
            d = np.genfromtxt(os.path.join(d_, f), comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        gal.append(dict(name=f[:-11], R=d[:, 0], Vobs=d[:, 1], eV=d[:, 2], Vgas=d[:, 3], Vdisk=d[:, 4], Vbul=d[:, 5]))
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
    tab = {}
    for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        tok = line.split()
        if len(tok) != 19:
            continue
        try:
            tab[tok[0]] = dict(zip(keys, [float(v) for v in tok[1:18]]))
        except ValueError:
            continue
    for q in gal:
        q["meta"] = tab.get(q["name"])
    return gal


def nu_simple(yv):
    if MUT:      # M4: standard mu = x/sqrt(1+x^2) -> nu = sqrt(1/2 + sqrt(1/4 + 1/y^2))
        return np.sqrt(0.5 + np.sqrt(0.25 + 1.0 / yv**2))
    return 0.5 * (1 + np.sqrt(1 + 4.0 / yv))


UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
GALS = load_sparc()
P(f"  galaxies loaded: {len(GALS)}")


def vbar2(q, u):
    return np.sign(q["Vgas"]) * q["Vgas"]**2 + u * q["Vdisk"]**2 + 1.4 * u * q["Vbul"]**2


FIT = {}
for f in FOOTS:
    a0 = A0[f]; num = den = 0.0; Us = []; FIT[f] = {}
    for q in GALS:
        R = q["R"] * KPC_S
        VB2 = (np.sign(q["Vgas"])[:, None] * q["Vgas"][:, None]**2 + UPS[None, :] * q["Vdisk"][:, None]**2 + 1.4 * UPS[None, :] * q["Vbul"][:, None]**2)
        GB = VB2 * 1e6 / R[:, None]; GO = ((q["Vobs"] * 1e3)**2 / R)[:, None] * np.ones_like(GB)
        OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & (q["Vobs"] > 0)[:, None]
        W = 1.0 / (np.clip(q["eV"], 1, None) / np.clip(q["Vobs"], 1, None))**2
        lgp = np.log10(np.where(OK, nu_simple(np.where(OK, GB, 1.0) / a0) * np.where(OK, GB, 1.0), 1.0))
        rres = np.where(OK, np.log10(np.where(OK, GO, 1.0)) - lgp, 0.0)
        Wm = np.where(OK, W[:, None], 0.0)
        mse = (Wm * rres**2).sum(0) / np.maximum(Wm.sum(0), 1e-300)
        i = int(np.argmin(mse))
        num += (Wm[:, i] * rres[:, i]**2).sum(); den += Wm[:, i].sum(); Us.append(UPS[i])
        FIT[f][q["name"]] = float(UPS[i])
    rms = math.sqrt(num / den)
    RES["rows"].setdefault("R1_SPARC", {})[f] = dict(rms=rms, U_median=float(np.median(Us)), N=len(Us))
    P(f"  {f}: rms {rms:.5f} dex, median Upsilon {np.median(Us):.2f}")
p4 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "P4_v3_galaxy_tiles", "p4_v3_galaxy_tiles_results.json")))["tiles"]["T1"]["footings"]
dP4 = max(abs(RES["rows"]["R1_SPARC"][f]["rms"] - p4[f]["iso_perUps"]["rms"]) for f in FOOTS)
dU = max(abs(RES["rows"]["R1_SPARC"][f]["U_median"] - p4[f]["iso_perUps"]["U_median"]) for f in FOOTS)
check("P4a", dP4 <= 2e-4 and dU < 1e-9, f"max|drms|={dP4:.1e}, max|dU|={dU:.2f}", "<=2e-4, equal",
      f"P4 iso_perUps {p4['canonical']['iso_perUps']['rms']:.5f}/{p4['alt']['iso_perUps']['rms']:.5f}")


def mu_of(xv):
    return xv / (1 + xv)


def profile(q, u, a0):
    """spherical: M_b(r) PCHIP from V_bar^2 r/G at SPARC radii (inner r^3), law g, phantom M_c, rho_c."""
    R = q["R"] * KPC_S
    Mb = vbar2(q, u) * 1e6 * R / G_SI
    gN = G_SI * Mb / R**2
    ok = gN > 0
    gl = np.where(ok, nu_simple(np.where(ok, gN, 1) / a0) * np.where(ok, gN, 1), np.nan)
    Mtot = gl * R**2 / G_SI
    Mc = Mtot - Mb
    rhoc = np.gradient(Mc, R) / (4 * np.pi * R**2)
    return R, Mb, gN, gl, Mc, rhoc, ok


# P4c: integrate the stress-balance ODE g'(mu + x mu_x) = 4piG rho_b - 2 g mu / r on PCHIP baryons
worstc = 0.0
for q in GALS[::5]:
    for f in FOOTS:
        a0 = A0[f]; u = FIT[f][q["name"]]
        R, Mb, gN, gl, Mc, rhoc, ok = profile(q, u, a0)
        if ok.sum() < 4 or not np.all(np.diff(R) > 0):
            continue
        r0 = R[0] * 0.5
        rg = np.concatenate([[r0], R]); Mg = np.concatenate([[Mb[0] * (r0 / R[0])**3], Mb])
        Mi = PchipInterpolator(rg, Mg); dMi = Mi.derivative()
        def rhs(rv, Y):
            gv = Y[0]; xv = gv / a0
            muv = xv / (1 + xv); dmu = 1 / (1 + xv)**2
            return [(G_SI * dMi(rv) / rv**2 - 2 * gv * muv / rv) / (muv + xv * dmu)]
        gN0 = G_SI * Mi(r0) / r0**2
        if gN0 <= 0:
            continue
        g0 = nu_simple(gN0 / a0) * gN0
        sol = solve_ivp(rhs, [r0, R[-1]], [g0], t_eval=R, rtol=1e-11, atol=1e-30, method="DOP853")
        sel = ok & (G_SI * Mi(R) / R**2 > 0)
        gN_i = G_SI * Mi(R[sel]) / R[sel]**2
        galg = nu_simple(gN_i / a0) * gN_i
        if sol.y.shape[1] == len(R):
            worstc = max(worstc, float(np.max(np.abs(np.log10(sol.y[0][sel] / galg)))))
check("P4c", worstc <= 1e-5, f"{worstc:.1e} dex", "<=1e-5", "35 galaxies x 2 footings: ODE from the stress balance == algebraic law")

# R2 attractor row
EPS = {"primary": 0.02, "reported": 0.054}
R2 = {}; ROWS_ALL = {}
for f in FOOTS:
    a0 = A0[f]; D = (LSTAR_PC[f] * PC)**1.5 * math.sqrt(a0)
    rows = []
    for q in GALS:
        u = FIT[f][q["name"]]
        R, Mb, gN, gl, Mc, rhoc, ok = profile(q, u, a0)
        sel = ok & np.isfinite(gl)
        if sel.sum() < 4:
            continue
        W = 1.0 / (np.clip(q["eV"], 1, None) / np.clip(q["Vobs"], 1, None))**2
        neg_frac = float(np.mean(rhoc[sel] <= 0))
        pos = sel & (rhoc > 0)
        lr = np.log(rhoc[pos]); TV = float(np.sum(np.abs(np.diff(lr)))) if pos.sum() > 1 else 0.0
        out = dict(name=q["name"], Q=int(q["meta"]["Q"]) if q["meta"] else -1, neg_frac=neg_frac, TV_lnrho=TV,
                   supply=float(Mc[sel][-1] / Mb[sel][-1]))
        for lab, e in EPS.items():
            def shift(dl):
                Mb2 = np.maximum(Mb + dl * np.maximum(Mc, 0), 1e-30)
                gN2 = G_SI * Mb2 / R**2
                g2_ = nu_simple(gN2 / a0) * gN2
                dlg = np.log10(g2_[sel] / gl[sel])
                return math.sqrt(np.sum(W[sel] * dlg**2) / np.sum(W[sel]))
            lo, hi = 0.0, 50.0
            if shift(hi) <= e:
                dstar = hi
            else:
                for _ in range(60):
                    mid = 0.5 * (lo + hi)
                    lo, hi = (mid, hi) if shift(mid) <= e else (lo, mid)
                dstar = lo
            lnA = TV / (2 * dstar) if dstar > 0 else float("inf")
            # relaxation (sound-crossing) time with c^2 = dstar g / |dln rho/dr|
            dl = np.abs(np.gradient(np.log(np.where(pos, rhoc, np.nan)), R))
            c2v = dstar * gl / dl
            cc = np.sqrt(c2v[pos & np.isfinite(c2v) & (c2v > 0)])
            Rp = R[pos & np.isfinite(c2v) & (c2v > 0)]
            trel = float(TRAPZ(1 / cc, Rp)) if Rp.size > 1 else float("nan")
            tdyn = float(R[sel][-1] / (q["Vobs"][sel][-1] * 1e3))
            out[lab] = dict(dstar=dstar, lnA=lnA, trel_over_tdyn=trel / tdyn, trel_over_tH=trel / T_H)
        gl_last = gl[sel][-1]
        out["bohm_growth_x_tdyn"] = float((gl_last**2 / D)**(1 / 3) * R[sel][-1] / (q["Vobs"][sel][-1] * 1e3))
        rows.append(out)
    ROWS_ALL[f] = rows
    lnA = np.array([x_["primary"]["lnA"] for x_ in rows]); trd = np.array([x_["primary"]["trel_over_tdyn"] for x_ in rows])
    trH = np.array([x_["primary"]["trel_over_tH"] for x_ in rows])
    lnA_r = np.array([x_["reported"]["lnA"] for x_ in rows])
    att = np.mean((lnA <= 3) & (trd <= 10) & (trH <= 1))
    fail_frac = float(np.mean(lnA > 10))
    cls = "PASS" if att >= 0.9 else ("FAIL" if fail_frac >= 0.5 else "MARGINAL")
    sup = np.array([x_["supply"] for x_ in rows]); neg = np.array([x_["neg_frac"] for x_ in rows])
    bohm = np.array([x_["bohm_growth_x_tdyn"] for x_ in rows])
    R2[f] = dict(N=len(rows), class_=cls, frac_attractor=float(att), frac_lnA_gt10=fail_frac,
                 lnA_median=float(np.median(lnA)), lnA_q16_84=[float(v) for v in np.percentile(lnA, [16, 84])],
                 lnA_median_eps054=float(np.median(lnA_r)), dstar_median=float(np.median([x_["primary"]["dstar"] for x_ in rows])),
                 trel_over_tdyn_median=float(np.nanmedian(trd)), trel_over_tH_median=float(np.nanmedian(trH)),
                 frac_gal_with_negative_phantom_pts=float(np.mean(neg > 0)), neg_pts_frac_mean=float(np.mean(neg)),
                 supply_median=float(np.median(sup)), frac_supply_gt_5p36=float(np.mean(sup > 5.36)),
                 bohm_growth_x_tdyn_median=float(np.median(bohm)), bohm_frac_gt1=float(np.mean(bohm > 1)))
    P(f"  R2 {f}: {cls}  N={len(rows)}  ln A median {R2[f]['lnA_median']:.1f} [16-84: {R2[f]['lnA_q16_84'][0]:.1f}, {R2[f]['lnA_q16_84'][1]:.1f}]"
      f" (eps 0.054: {R2[f]['lnA_median_eps054']:.1f}); delta* median {R2[f]['dstar_median']:.3f}; frac ln A>10 {fail_frac:.2f}; "
      f"t_rel/t_dyn median {R2[f]['trel_over_tdyn_median']:.1f}, t_rel/t_H {R2[f]['trel_over_tH_median']:.2f}")
    P(f"       negative-phantom points in {R2[f]['frac_gal_with_negative_phantom_pts']:.2f} of galaxies; supply M_c/M_b median {R2[f]['supply_median']:.1f}, "
      f"> 5.36 in {R2[f]['frac_supply_gt_5p36']:.2f}; L*-Bohm growth x t_dyn median {R2[f]['bohm_growth_x_tdyn_median']:.0f}")
    RES["rows"].setdefault("R2_attractor", {})[f] = R2[f]
with open(os.path.join(HERE, f"m5_r2_per_galaxy{TAG}.csv"), "w", newline="") as fh:
    w_ = csv.writer(fh); w_.writerow(["footing", "name", "Q", "Upsilon", "dstar_eps0.02", "lnA_eps0.02", "trel_over_tdyn", "trel_over_tH", "lnA_eps0.054", "neg_frac", "supply_Mc_over_Mb", "bohm_growth_x_tdyn"])
    for f in FOOTS:
        for x_ in ROWS_ALL[f]:
            w_.writerow([f, x_["name"], x_["Q"], FIT[f][x_["name"]], x_["primary"]["dstar"], x_["primary"]["lnA"], x_["primary"]["trel_over_tdyn"],
                         x_["primary"]["trel_over_tH"], x_["reported"]["lnA"], x_["neg_frac"], x_["supply"], x_["bohm_growth_x_tdyn"]])

# (c) BTFR line
for f in FOOTS:
    a0 = A0[f]; lv = []; res_ = []
    for q in GALS:
        m = q["meta"]
        if not m or m["Vflat"] <= 0:
            continue
        Mb = (FIT[f][q["name"]] * m["L36"] + 1.33 * m["MHI"]) * 1e9 * MSUN
        V = m["Vflat"] * 1e3
        lv.append(math.log10(V)); res_.append(math.log10(V**4 / (G_SI * Mb * a0)) / 4)
    lv = np.array(lv); res_ = np.array(res_)
    rU = float(np.std(lv)); rB = float(math.sqrt(np.mean(res_**2)))
    RES["rows"].setdefault("C_btfr", {})[f] = dict(N=len(lv), rms_logVflat_universal=rU, rms_btfr=rB, ratio=rU / rB,
                                                   cls="FAIL" if rU > 3 * rB else "not excluded")
    P(f"  (c) {f}: universal-bath rms(log Vflat) {rU:.3f} vs BTFR residual rms {rB:.3f} (N={len(lv)}): {'FAIL' if rU > 3*rB else 'not excluded'}")

# ============================================================================ Z2 satellites (read-only CSV)
P("\n=== R3 satellites from Z2's per-system CSV (read-only)")
rowsZ = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "Z2_satellite_systematics", "z2_per_system.csv"))))


def fl(v):
    try:
        return float(v)
    except Exception:
        return float("nan")


def clean(rw, flav):
    q_ = fl(rw[f"q_{flav}"])
    return (q_ < 0.5) and (fl(rw["ell"]) < 0.5) and (rw["grad_flag"] != "True") and (fl(rw["N_q"]) >= 10)


Z2ref = {"ISO": {"canonical": 0.465, "alt": 0.424}, "MOND": {"canonical": 0.693, "alt": 0.711}}
okz = True; R3 = {}
for f in FOOTS:
    rf = [rw for rw in rowsZ if rw["footing"] == f]
    for fl_ in ("ISO", "MOND"):
        vals = np.array([fl(rw[f"Delta_{fl_}"]) for rw in rf if clean(rw, fl_)])
        if MUT and fl_ == "ISO":
            vals = vals + 0.10
        bs = np.random.default_rng(1).choice(vals, (4000, vals.size)) if vals.size else None
        med = float(np.median(vals)); sd = float(np.std(np.median(bs, axis=1))) if bs is not None else float("nan")
        okz &= abs(med - Z2ref[fl_][f]) <= 0.05
        R3[f"{fl_}_{f}"] = dict(N=int(vals.size), median=med, boot_sd=sd, z=med / sd)
        P(f"  {f} {fl_}: clean N={vals.size}, median {med:+.3f} +- {sd:.3f} (Z2: {Z2ref[fl_][f]:+.3f})")
check("Z2a", okz, "see above", "within 0.05 of Z2")
rc_ = [rw for rw in rowsZ if rw["footing"] == "canonical"]
Xd = np.array([[1.0, math.log10(fl(rw["x_e"])), fl(rw["M_V"])] for rw in rc_])


def ols_slope(yv):
    b, *_ = np.linalg.lstsq(Xd, yv, rcond=None)
    rres = yv - Xd @ b; s2 = rres @ rres / (len(yv) - 3)
    cov = s2 * np.linalg.inv(Xd.T @ Xd)
    return float(b[1]), float(math.sqrt(cov[1, 1]))


v3d = np.array([fl(rw["Delta_V3D"]) for rw in rc_])
sl = {"data": ols_slope(v3d)}
for fl_ in ("MOND", "V3S", "ISO"):
    sl[fl_] = ols_slope(v3d - np.array([fl(rw[f"Delta_{fl_}"]) for rw in rc_]))
for kk, (b, e) in sl.items():
    P(f"  slope on log x_e at fixed M_V ({kk}): {b:+.2f} +- {e:.2f}")
check("Z2b", abs(sl["MOND"][0] + 0.76) <= 0.05 and abs(sl["V3S"][0] + 0.55) <= 0.05 and abs(sl["data"][0] + 0.05) <= 0.05,
      f"MOND {sl['MOND'][0]:+.2f}, V3S {sl['V3S'][0]:+.2f}, data {sl['data'][0]:+.2f}", "-0.76/-0.55/-0.05 +-0.05")
R3["slopes"] = {k_: dict(b=v[0], se=v[1]) for k_, v in sl.items()}
RES["rows"]["R3_satellites"] = R3

# ============================================================================ summary
RES["runtime_s"] = time.time() - T0
RES["peak_rss_gb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
npass = sum(ok for _, ok in CHECKS)
P(f"\nchecks {npass}/{len(CHECKS)}; runtime {RES['runtime_s']:.0f} s; peak RSS {RES['peak_rss_gb']:.2f} GB")
json.dump(RES, open(os.path.join(HERE, f"m5_equilibrium_law_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"m5_equilibrium_law{TAG}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
sys.exit(0 if npass == len(CHECKS) else 1)
