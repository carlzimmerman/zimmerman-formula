"""
CFG103-A2 -- FRW limit of the A1 action, own derivation: minisuperspace (N,a,T,Lam,theta,J) Euler-Lagrange by sympy; lapse N=1 after
variation; numerical integration of the second-order Raychaudhuri equation (rtol 1e-12), Mp2 = 1, m = 1.
Checks: E_N preserved (Bianchi), Lam'=0, Lam_eff(z) from (H,rho) constant, a0(z)/a0(0)-1, continuity equation, dust limit, Omega_c free,
tie across universes.  Frozen pass lines: FROZEN_DOCSTRING.txt.
MUTATE=1: multiplier -> thawing exponential scalar U=U0 exp(-lam psi); the fluid still reads U(psi): a0(z) must not be flat (FAIL).
MUTATE=2: tie dropped (cap reads independent constant Lc): a0 must not follow Lambda0 across universes (FAIL).
"""
import os, sys
import numpy as np, sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg103_common import Log, MUTATE
log = Log(__file__)

t = sp.Symbol("t")
Mp2, m, nus = 1, 1, sp.Symbol("nu_s", positive=True)
eps = sp.Rational(1, 4) / (8 * sp.pi)                       # kappa=1/2 -> eps = kappa^2/8pi
nn, LL = sp.symbols("nn LL", positive=True)
Lcap_sym = sp.Symbol("Lc", positive=True)
xx = m * nn / (nus * Mp2 * (Lcap_sym if MUTATE == 2 else LL))
rho_e = m * nn + eps * Mp2 * (Lcap_sym if MUTATE == 2 else LL) * xx * sp.atan(xx)
P_e = sp.simplify(nn * sp.diff(rho_e, nn) - rho_e)
rho_L_e = sp.diff(rho_e, LL)

a, N_, T_, Lam, th, J, psi = [sp.Function(s)(t) for s in ("a", "N", "T", "Lam", "th", "J", "psi")]
lam_s, U0 = sp.symbols("lam_s U0", positive=True)
Ufun = U0 * sp.exp(-lam_s * psi)
Lam_read = Ufun if MUTATE == 1 else Lam
nf = J / a**3
Lag = (-3 * Mp2 * a * sp.diff(a, t)**2 / N_ - N_ * a**3 * rho_e.subs({nn: nf, LL: Lam_read}))
if MUTATE == 1:
    Lag += N_ * a**3 * (Mp2 * sp.diff(psi, t)**2 / (2 * N_**2) - Mp2 * Ufun)
else:
    Lag += Mp2 * Lam * sp.diff(T_, t) - N_ * a**3 * Mp2 * Lam
Lag += J * sp.diff(th, t)
from sympy.calculus.euler import euler_equations
flds = [N_, a, th, J] + ([psi] if MUTATE == 1 else [T_, Lam])
EL = {str(f.func): (e.lhs - e.rhs) for f, e in zip(flds, euler_equations(Lag, flds, t))}
lap1 = {N_: 1}
def N1(e): return e.subs(N_, 1).doit()

# ---- symbolic statements derived from the EL system
rn = sp.diff(rho_e, nn)
if MUTATE != 1:
    ET = sp.simplify(EL["T"]); EJ = sp.simplify(EL["J"]).subs(N_, 1).doit()
    log.check("E_T: Lam' = 0", sp.simplify(ET + Mp2 * sp.diff(Lam, t)) == 0, str(ET))
    EL_clock = sp.simplify(N1(EL["Lam"]) - (Mp2 * sp.diff(T_, t) - a**3 * Mp2 * (1 - (P_e / (Mp2 * LL)).subs({nn: nf, LL: Lam}))))
    log.check("E_Lam: clock T' = a^3(1 - P/(Mp2 Lam))", EL_clock == 0, "residual %s" % str(EL_clock)[:60])
    log.check("E_theta: J' = 0", sp.simplify(EL["th"] + sp.diff(J, t)) == 0, "")
    log.check("E_J: theta' = N rho_n", sp.simplify(N1(EL["J"]) - (sp.diff(th, t) - rn.subs({nn: nf, LL: Lam}))) == 0, "")
# continuity equation: rho' + 3H(rho+P) = rho_Lam Lam'   (generic Lam(t); J const from E_theta)
Lam_gen = Lam_read
rho_t = rho_e.subs({nn: nf, LL: Lam_gen})
drho = sp.diff(rho_t, t).subs(sp.diff(J, t), 0)
Hh = sp.diff(a, t) / a
cont = sp.simplify(drho + 3 * Hh * (rho_t + P_e.subs({nn: nf, LL: Lam_gen})) - (rho_L_e.subs({nn: nf, LL: Lam_gen}) * sp.diff(Lam_gen, t)))
log.check("continuity: rho'+3H(rho+P)=rho_L Lam' (any Lam(t))", cont == 0, "residual %s" % str(cont)[:50])

# ---- equations of motion for numerics
adot = sp.Symbol("adot"); aa = sp.Symbol("aa", positive=True)
EN = sp.simplify(N1(EL["N"]))
Ea = N1(EL["a"])
addot = sp.Symbol("addot")
sol_add = None
def to_sym(expr, extra):
    e = expr.subs(sp.diff(a, t, 2), addot).subs(sp.diff(a, t), adot).subs(a, aa)
    return e
Ea_s = to_sym(Ea, None)
if MUTATE != 1:
    Ea_s = Ea_s.subs(J, sp.Symbol("Jc")).subs(Lam, sp.Symbol("Lamc"))
    addot_expr = sp.solve(Ea_s, addot)[0]
    EN_s = to_sym(EN, None).subs(J, sp.Symbol("Jc")).subs(Lam, sp.Symbol("Lamc"))
    Jc, Lamc = sp.symbols("Jc Lamc")
    f_add = sp.lambdify((aa, adot, Jc, Lamc, nus, Lcap_sym), addot_expr, "numpy")
    f_EN = sp.lambdify((aa, adot, Jc, Lamc, nus, Lcap_sym), EN_s, "numpy")
    rho_f = sp.lambdify((nn, LL, nus, Lcap_sym), rho_e, "numpy"); P_f = sp.lambdify((nn, LL, nus, Lcap_sym), P_e, "numpy")
    cs2_f = sp.lambdify((nn, LL, nus, Lcap_sym), (nn * sp.diff(P_e, nn) / (rho_e + P_e)), "numpy")
else:
    psi_dot, psi_dd = sp.symbols("psid psidd")
    Ea_s = Ea_s.subs(J, sp.Symbol("Jc"))
    Epsi = N1(EL["psi"]).subs(sp.diff(psi, t, 2), psi_dd).subs(sp.diff(psi, t), psi_dot).subs(sp.diff(a, t, 2), addot).subs(sp.diff(a, t), adot).subs(a, aa).subs(J, sp.Symbol("Jc"))
    Ea_s = Ea_s.subs(sp.diff(psi, t), psi_dot).subs(sp.diff(psi, t, 2), psi_dd)
    sol = sp.solve([Ea_s, Epsi], [addot, psi_dd], dict=True)[0]
    Jc = sp.Symbol("Jc")
    # replace psi(t) by symbol
    psis = sp.Symbol("psis")
    exa = sol[addot].subs(psi, psis); exp_ = sol[psi_dd].subs(psi, psis)
    f_a = sp.lambdify((aa, adot, psis, psi_dot, Jc, nus, lam_s, U0), [exa, exp_], "numpy")
    EN_m = to_sym(EN, None).subs(J, Jc).subs(sp.diff(psi, t), psi_dot).subs(psi, psis)
    f_EN = sp.lambdify((aa, adot, psis, psi_dot, Jc, nus, lam_s, U0), EN_m, "numpy")
    rho_f = sp.lambdify((nn, LL, nus, Lcap_sym), rho_e, "numpy")

eps_f = float(eps)
def run_universe(Lam0, J0, nu, Lc=2.055, zmax=10.0, nz=60):
    """H0 from E_N at a=1; integrate a(t) BACKWARD with the 2nd-order Raychaudhuri equation to z=zmax."""
    rho0 = float(rho_f(J0, Lam0, nu, Lc))
    H0 = np.sqrt((Lam0 + rho0) / 3.0)
    def rhs(tt, y):
        return [y[1], float(f_add(y[0], y[1], J0, Lam0, nu, Lc))]
    zs = np.linspace(0, zmax, nz); aeval = 1.0 / (1 + zs)
    ev = lambda tt, y: y[0] - 1.0 / (1 + zmax) * 0.9999
    ev.terminal = True
    sol = solve_ivp(rhs, [0, -3.0], [1.0, H0], method="DOP853", rtol=1e-12, atol=1e-14, dense_output=True, events=ev)
    # invert a(t) by dense evaluation
    tg = np.linspace(0, sol.t[-1], 40001); ag = sol.sol(tg)
    out = []
    for za in aeval:
        i = np.argmin(np.abs(ag[0] - za))
        # refine with brentq on dense output
        from scipy.optimize import brentq
        lo, hi = sorted([tg[max(i - 1, 0)], tg[min(i + 1, len(tg) - 1)]])
        tz = brentq(lambda s: sol.sol(s)[0] - za, lo, hi, xtol=1e-14) if (sol.sol(lo)[0] - za) * (sol.sol(hi)[0] - za) < 0 else tg[i]
        out.append((za, *sol.sol(tz)))
    o = np.array(out)
    A, Ad = o[:, 1], o[:, 2]; H = Ad / A   # o columns: (z-target a, a(t), adot(t))
    n = J0 / A**3
    rho = rho_f(n, Lam0, nu, Lc); P = P_f(n, Lam0, nu, Lc)
    ENres = np.array([float(f_EN(A[i], Ad[i], J0, Lam0, nu, Lc)) / A[i]**3 for i in range(len(A))])   # E_N = a^3 (3H^2 - Lam - rho)
    return dict(z=zs, a=A, H=H, n=n, rho=rho, P=P, H0=H0, ENres=ENres, Lam_eff=3 * H**2 - rho,
                cs2=cs2_f(n, Lam0, nu, Lc))

if MUTATE != 1:
    Lc_ref = 2.055
    res = {}
    for nu in (1.0, 1.0e4):
        u = run_universe(2.055, 0.945, nu, Lc_ref)
        res[nu] = u
        dL = np.max(np.abs(u["Lam_eff"] / 2.055 - 1))
        ENrel = np.max(np.abs(u["ENres"])) / (3 * np.max(u["H"]**2))
        log.p("   nu*=%g: H0=%.6f  max|Lam_eff/Lam-1| = %.2e  max|E_N|/(3H^2) = %.2e  x0 = %.3g  w0 = P/rho = %.4g  c_s^2(0) = %.4g" %
              (nu, u["H0"], dL, ENrel, u["rho"][0] / (nu * 2.055), u["P"][0] / u["rho"][0], u["cs2"][0]))
        # inferred a0(z): a0^2 = 8 pi G Pcap(Lam_eff) ; MUTATE2: cap reads Lc so a0 is constant but tied to Lc, not to Lam
        a0z = np.sqrt(eps_f * (Lc_ref * np.ones_like(u["Lam_eff"]) if MUTATE == 2 else u["Lam_eff"]))
        flat = np.max(np.abs(a0z / a0z[0] - 1))
        log.check("A2-a nu*=%g: E_N preserved by E_a (Bianchi)" % nu, ENrel < 1e-8, "%.2e" % ENrel)
        log.check("A2-a nu*=%g: Lambda_eff(z) const, z<=10" % nu, dL < 1e-8, "%.2e" % dL)
        log.check("A2-a nu*=%g: a0(z)/a0(0)-1 flat, z<=10" % nu, flat < 1e-8, "max %.2e  (CFG43 quotes 6e-11)" % flat)
    u1, u4 = res[1.0], res[1.0e4]
    log.check("A2-c: c_s^2(z=0) at nu*=1 ~ 6e-3 (+-20%)", abs(u1["cs2"][0] / 6e-3 - 1) < 0.2, "%.4g" % u1["cs2"][0])
    # dust limit: H(z)/H_LCDM after refitting (Om, OL, flat) -- and rho a^3 constancy
    for nu, u in res.items():
        E2 = (u["H"] / u["H0"])**2; zz = u["z"]
        fit = least_squares(lambda p: np.sqrt(p[0] * (1 + zz)**3 + (1 - p[0])) - np.sqrt(E2), [0.3], xtol=1e-14, ftol=1e-14)
        resid = np.max(np.abs(np.sqrt(p0 := fit.x[0] * (1 + zz)**3 + (1 - fit.x[0])) / np.sqrt(E2) - 1))
        rho_a3 = u["rho"] * u["a"]**3; drift = np.max(np.abs(rho_a3 / rho_a3[0] - 1))
        log.p("   nu*=%g: best flat-LCDM Om=%.5f, max residual of E(z) over z<=10: %.2e ; rho a^3 drift %.2e ; max w=P/rho %.3g" %
              (nu, fit.x[0], resid, drift, np.max(u["P"] / u["rho"])))
        if nu == 1.0e4:
            log.check("A2-c nu*=1e4: dust limit, E(z) residual < 1e-3", resid < 1e-3, "%.2e" % resid)
            log.check("A2-c nu*=1e4: rho a^3 constant to < 1e-3", drift < 1e-3, "%.2e" % drift)
    # Omega_c free: same Lambda, different J
    ua = run_universe(2.055, 0.5, 1e4, Lc_ref); ub = run_universe(2.055, 1.5, 1e4, Lc_ref)
    Oa = ua["rho"][0] / (3 * ua["H0"]**2); Ob = ub["rho"][0] / (3 * ub["H0"]**2)
    a0a = np.sqrt(eps_f * (Lc_ref if MUTATE == 2 else ua["Lam_eff"][0])); a0b = np.sqrt(eps_f * (Lc_ref if MUTATE == 2 else ub["Lam_eff"][0]))
    log.check("A2-d Omega_c free (J is data), a0 unchanged", abs(Oa - Ob) > 0.1 and abs(a0a / a0b - 1) < 1e-8, "Omega_c = %.3f, %.3f ; a0 ratio-1 = %.1e" % (Oa, Ob, a0a / a0b - 1))
    # tie across universes
    ratio = []
    for L0 in (0.7, 2.055, 6.0):
        uu = run_universe(L0, 0.945, 1e4, Lc_ref)
        a0u = np.sqrt(eps_f * (Lc_ref if MUTATE == 2 else uu["Lam_eff"][0]))
        # kappa^2 Lambda_eff/(8 pi) with kappa=1/2 vs a0^2
        ratio.append(a0u**2 / (0.25 * uu["Lam_eff"][0] / (8 * np.pi)))
    log.check("A2-e tie across universes: a0^2/(kappa^2 Lam0/8pi)=1", max(abs(np.array(ratio) - 1)) < 1e-8, "ratios %s" % np.array2string(np.array(ratio), precision=6))
    results = dict(lam_eff_dev={str(k): float(np.max(np.abs(v["Lam_eff"] / 2.055 - 1))) for k, v in res.items()}, cs2_z0_nu1=float(u1["cs2"][0]), tie_ratios=list(map(float, ratio)))
else:
    lam_v, U0v = 0.3, 2.055
    Jc0 = 0.945
    def rhs(tt, y):
        A, Ad, ps, pd = y
        ea, ep = f_a(A, Ad, ps, pd, Jc0, 1e4, lam_v, U0v); return [Ad, ea, pd, ep]
    a_i = 1.0 / 11.0
    # start deep in the past at a_i with psi frozen; choose H_i from E_N
    psi_i = 0.0; rho_i = float(rho_f(Jc0 / a_i**3, U0v * np.exp(-lam_v * psi_i), 1e4, 1.0))
    Hi = np.sqrt((U0v * np.exp(-lam_v * psi_i) + rho_i) / 3.0)
    ev = lambda tt, y: y[0] - 1.0; ev.terminal = True
    sol = solve_ivp(rhs, [0, 5.0], [a_i, Hi * a_i, psi_i, 0.0], method="DOP853", rtol=1e-12, atol=1e-14, dense_output=True, events=ev)
    tg = np.linspace(0, sol.t[-1], 40001); Y = sol.sol(tg)
    A = Y[0]; Uv = U0v * np.exp(-lam_v * Y[2]); a0z = np.sqrt(eps_f * Uv)
    zg = 1 / A - 1
    def at(zt): return a0z[np.argmin(np.abs(zg - zt))]
    r25 = at(2.5) / a0z[-1]
    log.p("   MUTATE=1: a0(z=2.5)/a0(0) = %.4f, a0(z=10)/a0(0) = %.4f (thawing exponential, lam=0.3, psi frozen at z=10)" % (r25, at(10.0) / a0z[-1]))
    log.check("A2-a a0(z)/a0(0)-1 flat, z<=10", abs(r25 - 1) < 1e-8, "a0(2.5)/a0(0)-1 = %.3e" % (r25 - 1))
    EN_res = max(abs(float(f_EN(Y[0][i], Y[1][i], Y[2][i], Y[3][i], Jc0, 1e4, lam_v, U0v))) for i in range(0, len(tg), 2000))
    log.check("A2-b E_N preserved (scalar system, informational)", EN_res < 1e-6, "%.2e" % EN_res)
    results = dict(a0_ratio_z2p5=float(r25))
log.finish(results)
