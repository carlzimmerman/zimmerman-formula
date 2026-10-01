"""CFG263 / NG-K: independent re-derivation of lane K (the a0^2-linear-in-a-density / AQUAL-offset family).
Written without opening agents/K_density_linear_family/*.py or *.out. c = G = 1.

 K1  F(0) = int_0^inf (1 - mu) dy given F' = mu, F - y -> 0 (I2); G rho/a0^2 = c/(8 pi)
 K2  c for sharp, exponential, Milgrom mu_n (closed form vs quadrature), OR family, RAR
 K3  OR-family reading (N-1)(N-2) = 1/(4 pi), N*, kappa*
 K4  AQUAL vs QUMOND offset (is the AQUAL choice load-bearing?)
 K5  w_off = -1 + (2/3) dln a0 / dln(1+z)
 K6  tail graft: c moves 26 -> 32 pi while mu moves < 1e-3 on x in [1, 60] (SPARC fits NOT re-run here)
 K7  SUSY row: V <= 0 at DW = 0, but SUSY-breaking dS stationary points exist (scope of K's 'SUSY vacua' row)
 K8  new: every Bose-Einstein-shaped nu with the deep-MOND limit gives W_v = pi^3/(30 g^3): never 4
"""
import numpy as np
import sympy as sp
import mpmath as mp
from scipy import optimize
from cfg263_lib import Checks, run_main

mp.mp.dps = 40


def c_aqual(one_minus_mu, pts=(0, 1, 10, 100, mp.inf)):
    return mp.quad(lambda x: 2 * x * one_minus_mu(x), list(pts))


def main():
    C = Checks("NG-K")
    yv, x, N, s = sp.symbols("y x N s", positive=True)

    # K1: F(0) from F' = mu, F(y) - y -> 0
    mu_e = 1 - sp.exp(-sp.sqrt(yv))           # sample mu(y) with y = x^2, x = sqrt y
    F0 = sp.integrate(1 - mu_e, (yv, 0, sp.oo))
    Fy = yv - sp.integrate((1 - mu_e).subs(yv, s), (s, yv, sp.oo))   # F(y) = y - int_y^inf (1 - mu)... sign check below
    # F' = mu requires F(y) = y + int_y^inf (1 - mu) ds  (so that F - y -> 0 and d/dy[int_y^inf] = -(1 - mu))
    Fy = yv + sp.integrate((1 - mu_e).subs(yv, s), (s, yv, sp.oo))
    C.check("K1_F_prime_is_mu", sp.simplify(sp.diff(Fy, yv) - mu_e) == 0 and sp.limit(Fy - yv, yv, sp.oo) == 0, "F(y) = y + int_y^inf (1-mu): F' = mu, F - y -> 0")
    # own fix: the first run FAILED here because sympy left the integral unevaluated under subs(y, 0); use the limit
    C.check("K1b_F0_is_offset", sp.simplify(sp.limit(Fy, yv, 0) - F0) == 0 and F0 == 2, f"F(0) = int_0^inf (1-mu) dy = {F0} for mu = 1 - exp(-x) (lane K: 2)")

    # K2: values
    vals = {}
    vals["sharp"] = c_aqual(lambda x: 1 - x if x < 1 else 0, (0, 1, 2))
    vals["exp"] = c_aqual(lambda x: mp.exp(-x))
    C.check("K2_sharp_and_exp", abs(vals["sharp"] - mp.mpf(1) / 3) < 1e-30 and abs(vals["exp"] - 2) < 1e-30, f"sharp {mp.nstr(vals['sharp'], 8)}, exponential {mp.nstr(vals['exp'], 8)}")
    ok = True; rows = []
    for n in (3, 4, 6, 10):
        num = mp.quad(lambda t: 2 * mp.exp(2 * t) * (-mp.expm1(-mp.log1p(mp.exp(-n * t)) / n)), [-60, 0, 10, 60])  # x = e^t, 1-mu = 1 - (1+x^-n)^(-1/n)
        closed = -(mp.mpf(2) / n) * mp.gamma(mp.mpf(3) / n) * mp.gamma(-mp.mpf(2) / n) / mp.gamma(mp.mpf(1) / n)
        rows.append((n, mp.nstr(num, 6), mp.nstr(closed, 6)))
        ok &= abs(num - closed) < 1e-12 * abs(closed)
    C.check("K2b_milgrom_mu_n_closed_form", ok, f"(n, quadrature, -(2/n)G(3/n)G(-2/n)/G(1/n)): {rows} (lane K: 1, 0.599, 0.431, 0.366)")
    cN = sp.simplify(sp.integrate(2 * x * (1 + x / N)**(-N), (x, 0, sp.oo), conds="none"))
    target = 2 * N**2 / ((N - 1) * (N - 2))
    C.check("K2c_OR_family", sp.simplify(cN.subs(N, 3) - target.subs(N, 3)) == 0 and sp.simplify(cN.subs(N, 5) - target.subs(N, 5)) == 0
            and abs(float(cN.subs(N, sp.Rational(7, 2))) - float(target.subs(N, sp.Rational(7, 2)))) < 1e-12,
            f"c(N) = 2N^2/((N-1)(N-2)): N=3 -> {target.subs(N,3)}, N=5 -> {float(target.subs(N,5)):.4f}; N = 2 diverges (log)")
    # RAR by direct inversion of x = nu(y) y (different route from NG-G's parametric integral)
    def mu_rar(xv):
        if xv == 0:
            return mp.mpf(0)
        # own fix: bracketed solve. nu <= 1 + 1/sqrt(y) gives y >= ((sqrt(1+4x)-1)/2)^2, and nu >= 1 gives y <= x
        lo = ((mp.sqrt(1 + 4 * xv) - 1) / 2)**2
        hi = xv
        fn = lambda t: t / (-mp.expm1(-mp.sqrt(t))) - xv
        for _ in range(200):
            mid = (lo + hi) / 2
            if fn(mid) > 0:
                hi = mid
            else:
                lo = mid
        return ((lo + hi) / 2) / xv
    # own fix: the first run stopped at x = 120 and missed the tail (int_120^inf ~ 4 t^3 e^-t ~ 0.12); extended to x = 3000
    cr = mp.quad(lambda xv: 2 * xv * (1 - mu_rar(xv)), [0, 0.5, 2, 10, 40, 120, 400, 1200, 3000])
    c100 = mp.quad(lambda xv: 2 * xv * (1 - mu_rar(xv)), [0, 0.5, 2, 10, 40, 100])
    C.value("RAR_fraction_below_x100", c100 / cr)
    fr = {}
    for Xc in (3, 10, 30, 100):
        pts = [0, 0.5, 2, 10, 30, 100]
        pts = [p_ for p_ in pts if p_ < Xc] + [Xc]
        fr[Xc] = mp.quad(lambda xv: 2 * xv * (1 - mu_rar(xv)), pts) / cr
        C.value(f"RAR_fraction_below_x{Xc}", fr[Xc])
    # independent large-x estimate: x ~ y there, fraction above y = X is ~ Gamma(4, sqrt X)/Gamma(4) (Bose tail ~ e^-t)
    est100 = 1 - mp.gammainc(4, mp.sqrt(100), mp.inf) / mp.gamma(4)
    C.check("K2e_accumulation_fractions", fr[3] < fr[10] < fr[30] < fr[100] and abs(fr[100] - est100) < 2e-3,
            f"RAR c accumulated below x = 3, 10, 30, 100: {[mp.nstr(fr[k], 3) for k in (3, 10, 30, 100)]} (Gamma-tail estimate at 100: {mp.nstr(est100, 4)}); "
            "lane K README:50 says 4%, 25%, 66%, 97% -- DISCREPANT, see compare step")
    C.check("K2d_RAR_by_inversion", abs(cr - 4 * mp.pi**4 / 15) < 1e-10, f"c_RAR (inverted mu) = {mp.nstr(cr, 14)}; 4 pi^4/15 = {mp.nstr(4*mp.pi**4/15, 14)} (lane K: 25.976)")
    C.value("c_RAR", cr)

    # K3: OR reading
    Ns = (3 + mp.sqrt(1 + 1 / mp.pi)) / 2
    C.check("K3_Nstar", abs((Ns - 1) * (Ns - 2) - 1 / (4 * mp.pi)) < 1e-30 and abs(Ns - mp.mpf("2.0741")) < 5e-5,
            f"(N-1)(N-2) = 1/(4 pi): N* = {mp.nstr(Ns, 8)}, kappa* = 1/N* = {mp.nstr(1/Ns, 6)}, G rho/a0^2 = N*^2 = {mp.nstr(Ns**2, 5)}")
    C.value("Nstar", Ns); C.value("kappa_star", 1 / Ns)
    # the derivation of c(N) = 8 pi N^2: G rho = c a0^2/(8 pi), a0 = s/N, s^2 = G rho
    Ns_ = sp.symbols("N_s", positive=True)
    C.check("K3b_reading_algebra", sp.simplify((target * (1 / Ns_)**2 / (8 * sp.pi)).subs(N, Ns_) - 1 / (4 * sp.pi * (Ns_ - 1) * (Ns_ - 2))) == 0,
            "G rho_off/s^2 = c(N)/(8 pi N^2) = 1/(4 pi (N-1)(N-2)); setting it to 1 gives (N-1)(N-2) = 1/(4pi)")

    # K4: AQUAL vs QUMOND offsets: c_A - c_Q = [(x - y)^2] boundary term (x = g/a0, y = g_N/a0)
    # OR N = 3: x(1 - mu(x)) -> 0 at both ends => equal
    N3 = 3
    def y_of_x(xv):
        return xv * (1 - (1 + xv / N3)**(-N3))
    dydx = lambda xv: 1 - (1 + xv / N3)**(-N3) + xv * (1 + xv / N3)**(-N3 - 1)   # own fix: analytic, not mp.diff
    cQ = mp.quad(lambda xv: 2 * (xv - y_of_x(xv)) * dydx(xv), [0, 1, 10, 100, mp.inf])
    cA = mp.quad(lambda xv: 2 * (xv - y_of_x(xv)), [0, 1, 10, 100, mp.inf])
    # own fix: tolerance 1e-15 was below the quadrature accuracy (|cA - 9| = 6e-12); 1e-9 is the honest level
    C.check("K4_AQUAL_equals_QUMOND", abs(cA - 9) < 1e-9 and abs(cQ - cA) < 1e-9,
            f"OR N=3: c_AQUAL = {mp.nstr(cA, 12)}, c_QUMOND = int 2(x-y) dy = {mp.nstr(cQ, 12)}: the offset is formulation-independent (boundary term (x-y)^2 vanishes)")

    # K5: w_off
    z = sp.symbols("z", positive=True)
    a0f = sp.Function("a0")(z)
    rho_off = a0f**2
    w = -1 + sp.Rational(1, 3) * sp.diff(sp.log(rho_off), z) * (1 + z)   # rho ~ (1+z)^(3(1+w))
    C.check("K5_w_off", sp.simplify(w - (-1 + sp.Rational(2, 3) * sp.diff(sp.log(a0f), z) * (1 + z))) == 0,
            "w_off = -1 + (2/3) dln a0/dln(1+z): the offset reading forces flat a0(z) iff w = -1")

    # K6: tail graft at X_J = 10 on the RAR mu
    XJ = mp.mpf(10)
    mJ = mu_rar(XJ); dmJ = mp.diff(mu_rar, XJ)
    c_core = mp.quad(lambda xv: 2 * xv * (1 - mu_rar(xv)), [0, 0.5, 2, 10])
    def c_graft(p):
        A = (1 - mJ) * XJ**p
        return c_core + 2 * A * XJ**(2 - p) / (p - 2)
    p_star = mp.findroot(lambda p: c_graft(p) - 32 * mp.pi, 2.1)
    A = (1 - mJ) * XJ**p_star
    xs = np.linspace(1, 60, 400)
    # own fix: the first run compared Delta mu with lane K's number, which is in dex of g_obs. At fixed g_N (AQUAL
    # mu(x) x = g_N/a0) a change delta mu shifts ln x by -delta mu/(mu + x mu'), i.e. dex = delta mu/((mu + x mu') ln 10).
    def ddex(xv):
        xv = mp.mpf(xv)
        if xv <= XJ:
            return 0.0
        m_new = 1 - A * xv**(-p_star); m_old = mu_rar(xv)
        dm_old = mp.diff(mu_rar, xv)
        return abs(float((m_new - m_old) / ((m_old + xv * dm_old) * mp.log(10))))
    dmax_mu = max(abs(float((1 - A * mp.mpf(xv)**(-p_star)) - mu_rar(mp.mpf(xv)))) if xv > 10 else 0.0 for xv in xs)
    dmax = max(ddex(xv) for xv in xs)
    C.value("graft_max_delta_mu_1_60", dmax_mu)
    mono = float(A * p_star * XJ**(-p_star - 1)) > 0  # graft derivative positive (mu increasing)
    C.check("K6_tail_graft", abs(c_graft(p_star) - 32 * mp.pi) < 1e-20 and dmax < 1.5e-3 and mono,
            f"graft 1-mu = A x^-p beyond x = 10: p* = {mp.nstr(p_star, 6)} gives c = 32 pi; max shift of g_obs on x in [1,60] = {dmax:.2e} dex (|Delta mu| {dmax_mu:.2e}) (lane K: p = 2.10, <= 1.2e-3 dex on SPARC points)")
    C.value("graft_pstar_XJ10", p_star)

    # K7: SUSY. (a) DW = 0 => V = -3 e^K |W|^2 <= 0. (b) Polonyi W = m^2 (phi + beta), K = |phi|^2 has dS minima for beta > 2 - sqrt3
    # own fix: the first run used beta = 2 - sqrt3 + 0.02, which is the AdS side (V_min < 0); the dS side is beta < 2 - sqrt3.
    def V(ph, beta):
        W = ph + beta
        DW = 1 + np.conj(ph) * W
        return float(np.real(np.exp(abs(ph)**2) * (abs(DW)**2 - 3 * abs(W)**2)))
    beta = 2 - np.sqrt(3) - 0.02
    res = optimize.minimize(lambda v: V(v[0] + 1j * v[1], beta), [0.73, 0.0], method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-16, "maxiter": 20000})
    p0 = res.x[0] + 1j * res.x[1]
    h = 1e-4
    Hxx = (V(p0 + h, beta) - 2 * V(p0, beta) + V(p0 - h, beta)) / h**2
    Hyy = (V(p0 + 1j * h, beta) - 2 * V(p0, beta) + V(p0 - 1j * h, beta)) / h**2
    DW0 = abs(1 + np.conj(p0) * (p0 + beta))
    C.check("K7_susy_breaking_dS_exists", V(p0, beta) > 0 and Hxx > 0 and Hyy > 0 and DW0 > 0.1,
            f"Polonyi (N=1 sugra, W = phi + beta, K = |phi|^2), beta = 2 - sqrt3 - 0.02: local minimum at phi = {p0.real:.4f}{p0.imag:+.1e}i, V = {V(p0, beta):.3e} > 0, |DW| = {DW0:.3f}: "
            "K's 'SUSY vacua have V <= 0' (README:13, :78) covers SUSY-PRESERVING vacua only")
    C.check("K7b_susy_preserving_nonpositive", all(-3 * np.exp(p**2) * (p + b)**2 <= 0 for p in np.linspace(-2, 2, 9) for b in (0.1, 1.0)),
            "at DW = 0, V = -3 e^K |W|^2 <= 0 (K's row reproduced for its actual class)")

    # K8: Bose-Einstein nu with degeneracy g and scale beta, renormalised to its own deep-MOND a0
    okBE = True; rowsBE = []
    for gdeg in (1, 2, 3):
        for beta_ in (mp.mpf("0.5"), mp.mpf(1), mp.mpf(2)):
            c_raw = mp.quad(lambda t: 2 * t**2 * (gdeg / mp.expm1(beta_ * t)) * 2 * t, [0, 1, 10, 100, mp.inf])  # y = t^2 in units a0'
            a0eff_over = mp.mpf(gdeg)**2 / beta_**2      # deep MOND: nu ~ g/(beta sqrt y) => a0_eff = a0' g^2/beta^2
            W = c_raw / (8 * mp.pi) / a0eff_over**2      # G rho / a0_eff^2
            rowsBE.append((gdeg, float(beta_), mp.nstr(W, 8)))
            okBE &= abs(W - mp.pi**3 / (30 * gdeg**3)) < 1e-25
    C.check("K8_BoseEinstein_nu_gives_pi3_over_30g3", okBE, f"(g, beta, W_v): {rowsBE}; W_v = pi^3/(30 g^3) for every scale: a thermal (Bose) nu cannot give W_v = 4 (needs g = pi/120^(1/3))")

    # K9: c >= 1/3 when mu' <= 1 (mu <= x)
    rs = np.random.default_rng(5)
    mins = []
    for _ in range(2000):
        knots = np.sort(rs.uniform(0, 1, 6)); dens = rs.uniform(0, 1, 7)  # piecewise density of mu' in [0,1]
        xs_ = np.linspace(0, 40, 4001)
        mup = np.interp(xs_, np.concatenate([[0], knots * 40, [40]]), np.concatenate([[dens[0]], dens[1:], [0]]))
        from scipy.integrate import cumulative_trapezoid  # own fix: cumsum started at mu(0) > 0 and overshot mu <= x
        muv = np.minimum(cumulative_trapezoid(mup, xs_, initial=0.0), 1.0)
        mins.append(np.trapezoid(2 * xs_ * (1 - muv), xs_) if hasattr(np, 'trapezoid') else np.trapz(2 * xs_ * (1 - muv), xs_))
    C.check("K9_lower_bound_one_third", min(mins) >= 1 / 3 - 1e-4, f"min c over 2000 random mu with mu' <= 1: {min(mins):.4f} >= 1/3")

    core = ["K1_F_prime_is_mu", "K1b_F0_is_offset", "K2b_milgrom_mu_n_closed_form", "K2c_OR_family", "K2d_RAR_by_inversion", "K3_Nstar", "K5_w_off", "K6_tail_graft"]
    step_false = not all(rw["pass"] for rw in C.rows if rw["id"] in core)
    flags = {"step_false": step_false, "premise_unverified": False, "headline_scope_ok": False}
    return C.write({"flags": flags, "core": core})


if __name__ == "__main__":
    run_main(main)
