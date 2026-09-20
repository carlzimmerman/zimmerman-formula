"""L289 -- the dark-matter CARRIER of the candidate: what a separately coupled carrier does to the clock sector (machine), and what any
carrier must satisfy to keep pure-MOND galaxies, MOND-plus-dark clusters and a cold forest (numbers from the record's constraints).
Part A (machine, Minkowski build of L285 + a second scalar chi minimally coupled through the metric only, L_chi = -Fchi(Xchi),
   Xchi = -g^{mu nu} d_mu chi d_nu chi, rolling background chi = C t with slope F1chi (dust: 16 pi G rho = -2 C^2 F1chi ...) and curvature F2chi):
   the MOND scalar's own well has NO roll (Q0 = 0, F1 = 0: the L288 killer is switched off); the dust lives in chi.
   V1 control: with chi's dust switched off the dispersion is L282's (two branches).
   V2 at the dust densities that killed the roll-dust (the a = 0.01 and 0.001 parameters of L288, k = 0.1/Mpc), the chi-carrier system has NO
      growing root faster than 10 H(a): a carrier that does not enter through the clock's Q does not load the clock sector.
   V3 chi's branch is the standard dust: high-k sound speed = the k-essence value F1chi/(2 C^2 F2chi ...) (printed), i.e. it clusters like CDM.
Part B (numbers): the isothermal retention of a homogeneous fluid carrier of sound speed c_s in deep-MOND potentials (galaxy M_b = 6e10 Msun,
   group 1e13, cluster 2e14; rho propto (R_out/r)^{v_f^2/c_s^2}, v_f^4 = G M a0), against the record's KiDS <= 14% (galaxy halo), clusters 32-46%
   (record), and the forest c_s^2 <= 1e-9 at z ~ 3 (L185):
   V4 no constant sound speed satisfies all three; the carrier must have c_s(z = 0) >~ 400 km/s and c_s^2(z = 3) <= 1e-9: a rise by >~ 1e3
      in c_s^2 since z = 3 (c_s^2 propto a^p with p >~ 5), or a field-dependent pressure (the MOND scalar's own, L282), whose only known
      inertia is the clock-coupled K2 term that L288 killed.  A FAIL is a finding."""
import os, sys, json, time, math
import sympy as sp, mpmath as mp, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
T0 = time.time(); print("L289 -- the carrier requirements\n", flush=True)
# ---------------- Part A: Minkowski build with a metric-coupled carrier chi
t, x, y, z = sp.symbols('t x y z', real=True); X = [t, x, y, z]
eps = sp.symbols('epsilon', positive=True)
KB, c1, c2, c3, c4, Q0, beta, xi, F1, F2, Cc, G1, G2 = sp.symbols('K_B c_1 c_2 c_3 c_4 Q_0 beta xi F_1 F_2 C G_1 G_2', real=True)
Psi, Phi, Tf, P, Xc = [sp.Function(n)(t, x) for n in ("Psi", "Phi", "T", "P", "chi")]
N = 1 + eps * Psi; a = 1 - eps * Phi
g = sp.diag(-N ** 2, a ** 2, a ** 2, a ** 2); ginv = g.inv(); sqrtg = N * a ** 3
Gam = [[[sp.simplify(sum(ginv[l, s] * (sp.diff(g[s, m], X[n]) + sp.diff(g[s, n], X[m]) - sp.diff(g[m, n], X[s])) for s in range(4)) / 2) for n in range(4)] for m in range(4)] for l in range(4)]
Ric = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        Ric[m, n] = sum(sp.diff(Gam[l][m][n], X[l]) - sp.diff(Gam[l][m][l], X[n]) + sum(Gam[l][l][s] * Gam[s][m][n] - Gam[l][n][s] * Gam[s][m][l] for s in range(4)) for l in range(4))
R = sum(ginv[m, n] * Ric[m, n] for m in range(4) for n in range(4))
tau = t + eps * Tf; dtau = [sp.diff(tau, v) for v in X]
Xinv = -sum(ginv[m, n] * dtau[m] * dtau[n] for m in range(4) for n in range(4))
n_dn = [-dtau[m] / sp.sqrt(Xinv) for m in range(4)]; n_up = [sum(ginv[m, n] * n_dn[n] for n in range(4)) for m in range(4)]
Dn = [[sp.diff(n_dn[n], X[m]) - sum(Gam[l][m][n] * n_dn[l] for l in range(4)) for n in range(4)] for m in range(4)]
Dn_up = [[sum(ginv[m, a_] * ginv[n, b_] * Dn[a_][b_] for a_ in range(4) for b_ in range(4)) for n in range(4)] for m in range(4)]
T1 = sum(Dn[m][n] * Dn_up[m][n] for m in range(4) for n in range(4)); divn = sum(ginv[m, n] * Dn[m][n] for m in range(4) for n in range(4)); T2 = divn ** 2
T3 = sum(Dn[m][n] * Dn_up[n][m] for m in range(4) for n in range(4))
J_dn = [sum(n_up[nu] * Dn[nu][m] for nu in range(4)) for m in range(4)]; J_up = [sum(ginv[m, n] * J_dn[n] for n in range(4)) for m in range(4)]
T4 = sum(J_dn[m] * J_up[m] for m in range(4))
phi = Q0 * t + eps * P; dphi = [sp.diff(phi, v) for v in X]
Jdphi = sum(J_up[m] * dphi[m] for m in range(4)); Q = sum(n_up[m] * dphi[m] for m in range(4))
Y = sum((ginv[m, n] + n_up[m] * n_up[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4))
dQ = Q - Q0
chi = Cc * t + eps * Xc; dchi = [sp.diff(chi, v) for v in X]
Xchi = -sum(ginv[m, n] * dchi[m] * dchi[n] for m in range(4) for n in range(4)); dX = Xchi - Cc ** 2
Lbr = R - c1 * T1 - c2 * T2 - c3 * T3 + c4 * T4 + 2 * (2 - KB) * Jdphi - (2 - KB) * beta * Y - (F1 * dQ + F2 * dQ ** 2 / 2) - (G1 * dX + G2 * dX ** 2 / 2)
L = sqrtg * Lbr
L2 = sp.expand(sp.diff(L, eps, 2).subs(eps, 0) / 2) - (2 - KB) * xi ** 2 * sp.diff(P, x, 2) ** 2
fields = [Psi, Phi, Tf, P, Xc]
def EL(Lag, f):
    e = sp.diff(Lag, f)
    for d_ in Lag.atoms(sp.Derivative):
        if d_.expr == f:
            vars_ = []
            for v_, cnt in d_.variable_count: vars_ += [v_] * cnt
            e += (-1) ** len(vars_) * sp.diff(sp.diff(Lag, d_), *vars_)
    return sp.expand(e)
E = [EL(L2, f) for f in fields]
w, k = sp.symbols('omega k', positive=True)
amps = sp.symbols('A_Psi A_Phi A_T A_P A_chi'); ex = sp.exp(sp.I * (k * x - w * t))
sub = {f: A * ex for f, A in zip(fields, amps)}
M = sp.zeros(5, 5)
for i, e in enumerate(E):
    ee = sp.expand(sp.simplify(e.subs(sub).doit() / ex))
    for j, A in enumerate(amps): M[i, j] = sp.simplify(ee.coeff(A))
c14 = sp.Symbol('c14'); M = M.subs({c1: KB, c3: -KB, c4: c14 - KB})
print(f"    5-field Minkowski matrix (with the carrier chi) built ({time.time()-T0:.0f} s)", flush=True)
R_ = sp.Rational; c14n = R_(25, 10 ** 6); NUM = {KB: R_(1, 5), c14: c14n, c2: c14n / (1 - 2 * c14n), beta: (2 - R_(1, 5)) / (2 - c14n), xi: 0, Q0: 0, F1: 0, F2: -648000}
W = sp.Symbol('W', positive=True); mp.mp.dps = 60
def roots_at(Mx, kQ):
    dn = sp.expand(Mx.subs(k, kQ).subs(w, sp.sqrt(W)).det(method="berkowitz")); pW = sp.Poly(dn, W)
    cf = [mp.mpf(R_(c_).p) / mp.mpf(R_(c_).q) for c_ in pW.all_coeffs()]
    while cf and cf[0] == 0: cf = cf[1:]
    return [mp.mpc(r_) for r_ in mp.polyroots(cf, maxsteps=2000, extraprec=800)] if cf else []
# V1 control: chi off (G1 = G2 = 0 -> chi decouples; its row/col trivial) vs L282's 4x4
from clock_action_build import build_fourier_matrix
M4, S4 = build_fourier_matrix()
M4 = M4.subs({S4['w']: w, S4['k']: k, S4['KB']: KB, S4['c2']: c2, S4['c14']: c14, S4['Q0']: Q0, S4['beta']: beta, S4['xi']: xi, S4['K2']: F2 / 2})
diff4 = [sp.simplify(d_) for d_ in (M.extract([0, 1, 2, 3], [0, 1, 2, 3]).subs({G1: 0, G2: 0, Cc: 0, F1: 0}) - M4)]
check("V1 control: with the carrier switched off the (Psi, Phi, T, P) block equals L282's matrix entry by entry", all(d_ == 0 for d_ in diff4), f"{[d_ for d_ in diff4 if d_ != 0][:2]}")
# carrier dust: 16 pi G rho_chi = (Fchi - Xchi ... ) : for L = -Fchi(X), rho = 2 X Fchi_X - Fchi -> with Fchi = G1 dX + G2 dX^2/2 about X = C^2: rho ~ 2 C^2 G1 (dust) ; set 2 C^2 G1 = 6 Om_m a^-3 (H0 = 1)
MPC = 3.0856775814913673e22; H0 = 67.4e3 / MPC; C_ = 2.99792458e8; Om_m = 0.31
Hfun = lambda a_: math.sqrt(9.1e-5 * a_ ** -4 + Om_m * a_ ** -3 + 0.69)
res = {}
for a_ in (1.0, 0.01, 1e-3):
    rho16 = 6 * Om_m * a_ ** -3; Cn = 1; G1n = R_(str(rho16 / 2)); G2n = G1n / R_(1, 10 ** 9)        # c_s,chi^2 ~ 1e-9-type stiffness
    Mn = M.subs(NUM).subs({Cc: Cn, G1: G1n, G2: G2n})
    kQ = R_(str(0.1 * (C_ / H0) / MPC / a_))
    rr = roots_at(Mn, kQ)
    grow = sorted([float(mp.sqrt(-r_)) for r_ in rr if mp.re(r_) < 0 and abs(mp.im(r_)) < 1e-20 * abs(r_)], reverse=True)
    res[a_] = dict(growth_H0=grow, H_H0=Hfun(a_), roots=[mp.nstr(r_, 5) for r_ in rr])
    print(f"    carrier chi at the a = {a_:g} parameters (16 pi G rho = {rho16:.3g} H0^2, k/a = {float(kQ):.3g} H0/c): omega^2 roots = {res[a_]['roots']}; growth rates = {[f'{g_:.3g}' for g_ in grow]} H0 (H(a) = {Hfun(a_):.3g} H0)  [roll-dust L288: 1.9e5 H0 at a = 0.01, 6.1e6 at 0.001]", flush=True)
OUT["carrier_dispersion"] = {str(a_): v_ for a_, v_ in res.items()}
check("V2 a carrier coupled through the metric only does NOT load the clock: at the a = 0.01 and 0.001 parameters that killed the roll-dust (1.9e5 and 6.1e6 H0), the chi-carrier system's fastest growth is below 10 H(a) (the ordinary Jeans/structure growth), and none at a = 1 beyond the dust's own",
      all(max(res[a_]['growth_H0'] + [0.0]) < 10 * res[a_]['H_H0'] for a_ in (0.01, 1e-3)), str({a_: res[a_]['growth_H0'][:2] for a_ in res}))
# V3: chi's high-k sound speed
Mn = M.subs(NUM).subs({Cc: 1, G1: R_(93, 100), G2: R_(93, 100) * 10 ** 9})
dWK = sp.expand(Mn.subs({w: sp.sqrt(W), k: sp.sqrt(sp.Symbol('K', positive=True))}).det(method="berkowitz")); Kk = sp.Symbol('K', positive=True)
pWK = sp.Poly(dWK, W, Kk); deg = max(sum(m_) for m_ in pWK.monoms())
lead = sum(c_ * W ** m_[0] * Kk ** m_[1] for m_, c_ in zip(pWK.monoms(), pWK.coeffs()) if sum(m_) == deg)
v = sp.Symbol('v', positive=True); pv = sp.Poly(sp.expand(lead.subs(W, v * Kk) / Kk ** deg), v)
vr = sorted([float(mp.re(r_)) for r_ in roots_at(sp.Matrix([[pv.as_expr().subs(v, W)]]), 1)] if False else [float(sp.re(r_)) for r_ in sp.Poly(pv.as_expr(), v).nroots(n=30)])
cs2_k = float(R_(93, 100) / (R_(93, 100) + 2 * 1 * R_(93, 100) * 10 ** 9))                                      # k-essence: P_X/(P_X + 2 X P_XX), X = C^2 = 1, P_X = G1, P_XX = G2
print(f"    carrier's high-k branch speeds: {vr}; k-essence c_s^2 = P_X/(P_X + 2 X P_XX) = {cs2_k:.3e}", flush=True)
check("V3 the carrier's branch is an ordinary k-essence dust: one high-k speed equals P_X/(P_X + 2 X P_XX) to 1% (it clusters like CDM with a tiny sound speed -- and therefore forms galaxy halos)",
      any(abs(x_ / cs2_k - 1) < 0.01 for x_ in vr if x_ > 0), f"{vr} vs {cs2_k:.3e}")
# ---------------- Part B: retention numbers
Gn, MSUN, KPC, a0 = 6.67430e-11, 1.98847e30, 3.0856775814913673e19, 1.2e-10
systems = {"galaxy (M_b = 6e10 Msun, r_in = 30 kpc, R_out = 1 Mpc)": (6e10, 30, 1000), "group (1e13, 300 kpc, 3 Mpc)": (1e13, 300, 3000), "cluster (2e14, 1.4 Mpc, 5 Mpc)": (2e14, 1400, 5000)}
def retention(cs_kms, M, r_in, R_out):
    vf = (Gn * M * MSUN * a0) ** 0.25; p_ = (vf / (cs_kms * 1e3)) ** 2                      # rho propto (R_out/r)^p (deep MOND, isothermal)
    if p_ >= 3: return float('inf')                                                          # mass diverges at the centre: full collapse
    frac_in = (r_in / R_out) ** (3 - p_)                                                   # fraction of the fluid mass inside r_in, relative to a uniform fill of R_out
    Mfluid_uniform = 0.26 * 1.36e11 * (4 / 3) * math.pi * (R_out / 1000) ** 3               # Msun: cosmic-mean dark density x volume (Om_dm rho_crit = 3.5e10 Msun/Mpc^3)
    return Mfluid_uniform * frac_in * 3 / (3 - p_) / M                                       # retained-fluid mass inside r_in over the baryonic mass
table = {}
for cs in (10, 100, 200, 300, 400, 600, 800, 1000, 1500):
    table[cs] = {nm: retention(cs, *pars) for nm, pars in systems.items()}
    print(f"    c_s = {cs:5d} km/s: retained/baryonic = " + " | ".join(f"{nm.split(' ')[0]} {v_:.3g}" for nm, v_ in table[cs].items()), flush=True)
OUT["retention"] = {str(cs): {nm.split(' ')[0]: v_ for nm, v_ in row.items()} for cs, row in table.items()}
gal_ok = [cs for cs in table if table[cs]["galaxy (M_b = 6e10 Msun, r_in = 30 kpc, R_out = 1 Mpc)"] <= 0.14]
clu_ok = [cs for cs in table if table[cs]["cluster (2e14, 1.4 Mpc, 5 Mpc)"] >= 0.32]
window = sorted(set(gal_ok) & set(clu_ok))
cs_forest = math.sqrt(1e-9) * C_ / 1e3
print(f"    galaxy halo <= 14% needs c_s >= {min(gal_ok) if gal_ok else None} km/s; cluster >= 32% needs c_s <= {max(clu_ok) if clu_ok else None} km/s; window today: {window} km/s; the forest (L185) needs c_s(z = 3) <= {cs_forest:.1f} km/s", flush=True)
rise = (min(window) / cs_forest) ** 2 if window else float('inf'); p_needed = math.log(rise) / math.log(4) if window else float('inf')
print(f"    => c_s^2 must rise by >= {rise:.0f}x between z = 3 and z = 0: c_s^2 propto a^p with p >= {p_needed:.1f}", flush=True)
OUT["window_kms"] = window; OUT["rise_needed"] = rise; OUT["p_needed"] = p_needed
check("V4 [FINDING] no constant sound speed satisfies KiDS (galaxy halo <= 14%), the clusters (>= 32%) and the forest (c_s <= 9.5 km/s at z = 3) together: the galaxy/cluster dichotomy alone needs c_s(z = 0) in the printed window (hundreds of km/s), 1e3-1e4 times the forest value in c_s^2 -- a homogeneous carrier must HEAT by that factor since z = 3 (p >~ 5), or carry a field-dependent pressure like the MOND scalar's (L282), whose only known inertia is the clock-coupled K2 term (dead, L288)",
      bool(window) and rise > 100, f"window {window}, rise {rise:.0f}, p {p_needed:.1f}")
n_pass = sum(CH); print(f"\nL289 COMPLETE: {n_pass}/{len(CH)} checks PASS  ({time.time()-T0:.0f} s).")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
sys.exit(0 if n_pass == len(CH) else 1)
