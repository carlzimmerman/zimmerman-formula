#!/usr/bin/env python3
"""CFG122 S0 controls (frozen criteria S0.1-S0.5) + S0.6 (reported): the harness must pass these or every gate result is void.
S0.1 sympy: flux law, N_a, deep-MOND limit  | S0.2 EOS: K, c_s^2, index | S0.3 alpha->0 recovers Newton | S0.4 Lane-Emden n=1/2 M-R exponent 1/5
S0.5 target identities (point mass) and the CFG44 B1 cross-check (repo read-only)  | S0.6 (reported) DM mass inside the solver's inner radius.
Run: ZF_REPO=<repo root> python3 cfg122_s0_controls.py"""
import os, sys, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg122_common import *
from cfg122_targets import target_on_grid

R = Report("cfg122_s0_controls")
P, check = R.P, R.check
R.banner("S0.1  sympy: static spherical reduction of L = P(X) - alpha (Lam/M_Pl) phi rho_b; flux law; N_a; deep-MOND limit")
r, m, al, Lam, Mpl, Gs, Mb, Y = sp.symbols("r m alpha Lambda M_Pl G M_b Y", positive=True)
p = sp.symbols("p", real=True)
phi = sp.Function("phi")(r)
Xs = Y - sp.diff(phi, r) ** 2 / (2 * m)
# P(X) = (2 Lam (2m)^(3/2)/3) X sqrt|X| ; use the branch X<0 (deep) with |X| = -X:  P = -(2 Lam (2m)^(3/2)/3) (-X)^(3/2)
Pfun = lambda X, sgn: sgn * (2 * Lam * (2 * m) ** sp.Rational(3, 2) / 3) * (sgn * X) ** sp.Rational(3, 2)
# flux law: d/dr[ 4 pi r^2 * dL/dphi' ] = 4 pi r^2 dL/dphi  with dL/dphi = -alpha Lam rho_b / M_Pl and  rho_b 4 pi r^2 dr = dM_b
Xp = sp.symbols("X_", real=True)
n_of_X_neg = sp.diff(Pfun(Xp, -1), Xp)                    # n = P'(X) for X<0
n_of_X_pos = sp.diff(Pfun(Xp, +1), Xp)
Xneg = sp.symbols("Xneg", negative=True)
Xpos = sp.symbols("Xpos", positive=True)
chk_n_pos = sp.simplify(n_of_X_pos.subs(Xp, Xpos) - Lam * (2 * m) ** sp.Rational(3, 2) * sp.sqrt(Xpos))
chk_n_neg = sp.simplify(n_of_X_neg.subs(Xp, Xneg) - Lam * (2 * m) ** sp.Rational(3, 2) * sp.sqrt(-Xneg))
P(f"  n = P'(X):  X>0 residual {chk_n_pos},  X<0 residual {chk_n_neg}")
# dL/dphi' = P_X * (-phi'/m) = -n p/m ;  EL: d/dr(4 pi r^2 (-n p/m)) = -4 pi r^2 alpha Lam rho_b/M_Pl  =>  4 pi r^2 n p/m = alpha Lam M_b(<r)/M_Pl
n_sym = Lam * (2 * m) ** sp.Rational(3, 2) * sp.sqrt(-Xneg)
flux = sp.Eq(4 * sp.pi * r ** 2 * n_sym * p / m, al * Lam * Mb / Mpl)
# deep (gradient-dominated) regime X = -p^2/(2m):
psol = sp.solve(sp.Eq(flux.lhs.subs(Xneg, -p ** 2 / (2 * m)), flux.rhs), p)
psol = [s for s in psol if s.is_positive is not False][0] if psol else None
P(f"  gradient-dominated p = {sp.simplify(psol)}")
a_phi = al * Lam / Mpl * psol
gN = Gs * Mb / r ** 2
Gsub = 1 / (8 * sp.pi * Mpl ** 2)
ratio = sp.simplify((a_phi ** 2 / (gN * (al ** 3 * Lam ** 2 / Mpl))).subs(Gs, Gsub))
P(f"  a_phi^2 / [g_N * (alpha^3 Lam^2 / M_Pl)] = {ratio}     => N_a = {ratio}   (a0 = N_a alpha^3 Lam^2/M_Pl)")
check("S0.1a  n = P'(X) = Lam (2m)^(3/2) sqrt|X| in both signs of X (sympy)", f"residuals {chk_n_pos}, {chk_n_neg}", chk_n_pos == 0 and chk_n_neg == 0)
check("S0.1b  the gradient-dominated phonon force is a_phi = sqrt(a0 g_N) with a0 = N_a alpha^3 Lam^2/M_Pl and N_a = 1 (derived)", f"N_a = {ratio}", sp.simplify(ratio - 1) == 0)
R.num("N_a", str(ratio))
# numeric deep-MOND limit through the algebraic solver (Y = 0: X = -sqrt(D)):
worst = 0.0
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    for (mm, aa) in ((1.0, 1.0), (0.01, 30.0), (100.0, 0.05)):
        L = float(lam_tie(mm, aa, a0n))
        Mm = 1e10 * MSUN_EV
        for x in (0.3, 3.0, 30.0):
            rr = x * float(rM(Mm, a0n))
            C = mm * aa * Mm / (4 * math.pi * rr ** 2 * MPL)
            D = C * C / (16 * mm ** 4)
            X = float(solveX(np.array(0.0), np.array(D), "B-"))
            pp = C / ((2 * mm) ** 1.5 * math.sqrt(abs(X)))
            aphi = aa * L / MPL * pp
            expect = math.sqrt(a0n * G_N * Mm) / rr
            worst = max(worst, abs(aphi / expect - 1))
check("S0.1c  numeric deep-MOND limit through the algebraic solver: a_phi = sqrt(a0 G M)/r, v^4 = G M a0 (both footings, 3 (m, alpha), 3 radii)", f"worst relative deviation {worst:.2e}", worst < 1e-6)

R.banner("S0.2  EOS of the condensed phase (X>0): P = K rho^3, K = 1/(12 m^6 Lam^2); c_s^2 = dP/drho = 2X/m; polytropic index n = 1/2")
X_, rho_ = sp.symbols("X rho", positive=True)
Pp = 2 * Lam * (2 * m) ** sp.Rational(3, 2) / 3 * X_ ** sp.Rational(3, 2)
nn = sp.diff(Pp, X_)
rho_expr = m * nn
Xof = sp.solve(sp.Eq(rho_expr, rho_), X_)[0]
Prho = sp.simplify(Pp.subs(X_, Xof))
K_sym = sp.simplify(Prho / rho_ ** 3)
cs2_sym = sp.simplify(sp.diff(Prho, rho_))
cs2_X = sp.simplify(nn / (m * sp.diff(nn, X_)))
P(f"  P(rho) = {Prho};  K = {K_sym};  c_s^2 = {cs2_sym} = {cs2_X} (in X)")
check("S0.2a  K = 1/(12 m^6 Lam^2) (the frozen file's hand value)", f"sympy K = {K_sym}", sp.simplify(K_sym - 1 / (12 * m ** 6 * Lam ** 2)) == 0)
check("S0.2b  c_s^2 = 2X/m and c_s^2 = 3 K rho^2 = 3P/rho", f"c_s^2(X) = {cs2_X}", sp.simplify(cs2_X - 2 * X_ / m) == 0 and sp.simplify(cs2_sym - 3 * K_sym * rho_ ** 2) == 0)
gam = sp.simplify(sp.diff(sp.log(Prho), rho_) * rho_)
check("S0.2c  polytropic exponent dlnP/dlnrho = 3, i.e. n = 1/2", f"dlnP/dlnrho = {gam}", gam == 3)

R.banner("S0.3  alpha -> 0 recovers Newton: p -> 0, a_phi/g_N -> 0, the condensate is the Newtonian polytrope")
a0n = a0_nat("canonical")
mm, aa = 1.0, 3.0
Lv = float(lam_tie(mm, aa, a0n))
pr = Prof("point", 1e10)
sol = integrate(mm, aa, Lv, pr, 0.1 * float(rM(pr.M, a0n)), 30 * float(rM(pr.M, a0n)), 60, np.array([1e-3 * mm * G_N * pr.M / float(rM(pr.M, a0n))]), "B+hi", a0n, alpha_c=1e-14)
ratio_a = np.nanmax(sol["a_phi"] / (G_N * sol["Mb"][:, None] / sol["r"][:, None] ** 2))
Xrel = np.nanmax(np.abs(sol["X"] / sol["Y"] - 1))
check("S0.3  alpha_c = 1e-14 alpha: max a_phi/g_N and |X/Y - 1| (X = mu - m Phi, the Newtonian condensate)", f"a_phi/g_N max {ratio_a:.2e}; max |X/Y - 1| {Xrel:.2e}", ratio_a < 1e-12 and Xrel < 1e-12)

R.banner("S0.4  Lane-Emden n = 1/2 (P = K rho^3 self-gravitating): M-R exponent 1/5 (internal consistency, no external table)")
def le_RM(rhoc):
    # G = K = 1 units, w = rho^2:  P = rho^3 => 3 rho drho/dr = -M/r^2 => dw/dr = -(2/3) M/r^2 ;  dM/dr = 4 pi r^2 sqrt(w)
    def f(rr, y):
        w, M = y
        return [-(2.0 / 3.0) * M / rr ** 2, 4 * math.pi * rr ** 2 * math.sqrt(max(w, 0.0))]
    ev = lambda rr, y: y[0]
    ev.terminal = True
    r0 = 1e-6
    s = solve_ivp(f, (r0, 1e3), [rhoc ** 2, 4 * math.pi / 3 * r0 ** 3 * rhoc], events=ev, rtol=1e-12, atol=1e-30, method="DOP853")
    return s.t_events[0][0], s.y_events[0][0][1]
R1, M1 = le_RM(1.0)
R2, M2 = le_RM(2.0)
expo = math.log(R2 / R1) / math.log(M2 / M1)      # R ~ M^((1-n)/(3-n)) = M^(1/5)  (my first draft computed dlnM/dlnR = 5: an inverted definition, fixed before any gate ran)
xi1 = R1 * 1.0 ** -0.5 / math.sqrt(3 / (4 * math.pi) * 1.0 * (1 + 0.5) * 1.0) if False else None
check("S0.4  d ln R / d ln M = (1-n)/(3-n) = 1/5 for the n = 1/2 polytrope (numerical hydrostatic integration, rho_c = 1 and 2)", f"exponent {expo:.5f}; R(1) = {R1:.5f}, M(1) = {M1:.5f}", abs(expo - 0.2) < 1e-3)

R.banner("S0.5  the target's point-mass identities; CFG44 B1 cross-check (repo read-only)")
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    pr = Prof("point", 1e10)
    r0_, r1_ = 0.1 * float(rM(pr.M, a0n)), 300 * float(rM(pr.M, a0n))
    T = target_on_grid(pr, a0n, r0_, r1_, 200)
    x = T["r"] / float(rM(pr.M, a0n))
    rho_an = a0n / (4 * math.pi * G_N * T["r"] * np.sqrt(1 + x ** 2))
    dev = np.max(np.abs(T["rho_t"] / rho_an - 1))
    Mc_an = pr.M * (np.sqrt(1 + x ** 2) - 1)
    dev2 = np.max(np.abs(T["Mc"][1:] / Mc_an[1:] - 1))
    ident = np.max(np.abs(T["rho_t"] * T["r"] ** 3 * T["gtot"] / (a0n * pr.M / (4 * math.pi)) - 1))
    check(f"S0.5 [{foot}] ODE target = rho_c = a0/(4 pi G r sqrt(1+x^2)), M_c = M(sqrt(1+x^2) - 1), C(r) = a0 M/4pi", f"max dev rho {dev:.2e}, M_c {dev2:.2e}, C(r) {ident:.2e}", max(dev, dev2, ident) < 1e-5)
if REPO is None:
    check("S0.5x CFG44 Bcommon cross-check", "repo not found (set ZF_REPO): NOT run", False, load_bearing=False)
else:
    try:
        sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG44_fluid_target"))
        import Bcommon as BC
        prof = BC.point_mass(1e10)
        tf = BC.target_fields(prof, n=2001)
        a0n = a0_nat("canonical")
        pr = Prof("point", 1e10)
        # compare rho_c at r = r_M in physical units: Bcommon: Msun/kpc^3
        rMk = math.sqrt(BC.G * 1e10 / BC.A0)
        i = int(np.argmin(np.abs(tf["r"] - rMk)))
        rho_b = tf["rho"][i]                                      # Msun/kpc^3 at r = tf['r'][i]
        rr = tf["r"][i] * KPC_EV
        rho_mine = float(a0n / (4 * math.pi * G_N * rr * math.sqrt(1 + (tf["r"][i] / rMk) ** 2)))  # eV^4
        conv = MSUN_EV / KPC_EV ** 3
        dev = abs(rho_b * conv / rho_mine - 1)
        check("S0.5x  CFG44 Bcommon.target_fields (point mass 1e10, r near r_M) agrees with this lane's natural-unit target", f"relative deviation {dev:.2e} (units Msun/kpc^3 -> eV^4; A0 canonical)", dev < 1e-3)
    except Exception as e:                                       # noqa
        check("S0.5x CFG44 Bcommon cross-check", f"import failed: {e}", False, load_bearing=False)

R.banner("S0.6 (reported)  DM mass accumulated inside the solver's inner radius 0.1 r_M (the solver starts at M_DM = 0 there)")
worst = {}
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    mg, ag, Mm_, Aa_ = plane(20)
    for br in BRANCHES:
        wmax = 0.0
        fr_ok = fr_all = 0
        for Mmsun in (1e9, 1e12):
            pr = Prof("point", Mmsun)
            base = Mm_ * G_N * pr.M / float(rM(pr.M, a0n))
            for k in (-2, 0, 2):
                Y0 = base * 10.0 ** k
                Lm = lam_tie(Mm_, Aa_, a0n)
                so = integrate(Mm_, Aa_, Lm, pr, 1e-3 * float(rM(pr.M, a0n)), 0.1 * float(rM(pr.M, a0n)), 60, Y0 * 1.0, br, a0n)
                with np.errstate(invalid="ignore"):
                    f = so["MD"][-1] / pr.M
                f = f[np.isfinite(f)]
                fr_ok += int(np.sum(f <= 1e-2)); fr_all += int(f.size)
                if f.size:
                    wmax = max(wmax, float(np.max(f)))
        worst[(foot, br)] = wmax
        worst[(foot, br, "frac_cells_le_1e-2")] = fr_ok / max(fr_all, 1)
P("  max over the coarse (m, alpha) plane and Y(r_lo) in {1e-2, 1, 1e2} x m G M/r_M, masses 1e9 and 1e12, starting from 1e-3 r_M, of M_DM(<0.1 r_M)/M_b:")
for k, v in worst.items():
    P(f"    {k}: {v:.3g}")
R.num("S0.6_MDM_inner_over_Mb_max", {str(k): v for k, v in worst.items()})
R.check("S0.6 (reported) neglected inner DM mass M_DM(<0.1 r_M)/M_b", "see the table above; values >> 1e-2 mean the solver's M_DM(r_lo) = 0 start is not negligible for those (m, alpha, Y) cells (disclosed; each gate row states whether it uses such cells)", True, load_bearing=False)

R.banner("S0.7  RK4 resolution control: N = 160 (used by the gates) against N = 640 on the same solutions (density and a_phi at common nodes), stratified")
stat = {br: dict(n=0, ok=0, worst=0.0) for br in BRANCHES}
dm_dom = dict(n=0, bad=0)
for foot in FOOTINGS:
    a0n = a0_nat(foot)
    mg_, ag_, Mm_, Aa_ = plane(8)
    for Mmsun in (1e9, 1e12):
        pr = Prof("point", Mmsun)
        rMv = float(rM(pr.M, a0n))
        base = Mm_ * G_N * pr.M / rMv
        Lm = lam_tie(Mm_, Aa_, a0n)
        for br in BRANCHES:
            for k in (-4, -2, 0, 2, 4):
                Y0 = base * 10.0 ** k
                lo = integrate(Mm_, Aa_, Lm, pr, 0.1 * rMv, 30 * rMv, 160, Y0, br, a0n)
                hi = integrate(Mm_, Aa_, Lm, pr, 0.1 * rMv, 30 * rMv, 640, Y0, br, a0n)
                fin = np.cumprod(np.isfinite(lo["rho"]) & np.isfinite(hi["rho"][::4]), axis=0) > 0
                mdmax = np.where(fin, hi["MD"][::4] / pr.M, 0).max(axis=0)
                for q in ("rho", "a_phi"):
                    with np.errstate(all="ignore"):
                        d = np.where(fin, np.abs(lo[q] / hi[q][::4] - 1), 0).max(axis=0)
                    sub = (mdmax <= 30) & fin.any(axis=0)
                    stat[br]["n"] += int(sub.sum()); stat[br]["ok"] += int((sub & (d <= 1e-3)).sum())
                    if sub.any():
                        stat[br]["worst"] = max(stat[br]["worst"], float(d[sub].max()))
                    dd = ~sub & fin.any(axis=0)
                    dm_dom["n"] += int(dd.sum()); dm_dom["bad"] += int((dd & (d > 1e-3)).sum())
for br in BRANCHES:
    P(f"  {br:5s}: DM-subdominant solutions (M_DM <= 30 M_b everywhere): {stat[br]['n']} sets; agree to 1e-3: {stat[br]['ok']}; worst relative deviation {stat[br]['worst']:.2e}")
P(f"  DM-dominated solutions (M_DM > 30 M_b somewhere; the target has M_c <= 29 M_b at x = 30, so these cannot match it): {dm_dom['n']} sets, of which {dm_dom['bad']} disagree by > 1e-3 (stiff: not resolved; irrelevant to every pass line)")
R.num("S0.7", dict(stat=stat, dm_dominated=dm_dom))
check("S0.7a  branch B- (the MOND-carrying branch), DM-subdominant solutions: N = 160 agrees with N = 640 to 1e-3 in rho and a_phi", f"worst deviation {stat['B-']['worst']:.2e} over {stat['B-']['n']} sets", stat["B-"]["worst"] < 1e-3 and stat["B-"]["n"] > 0)
check("S0.7b (reported)  branches B+hi / B+lo, DM-subdominant: fraction agreeing to 1e-3 (the disagreements sit next to the fold Y^2 = 4D where the root is singular)",
      f"B+hi {stat['B+hi']['ok']}/{stat['B+hi']['n']} (worst {stat['B+hi']['worst']:.2e}); B+lo {stat['B+lo']['ok']}/{stat['B+lo']['n']} (worst {stat['B+lo']['worst']:.2e})", True, load_bearing=False)
nf, gf = R.write()
sys.exit(1 if nf else 0)
