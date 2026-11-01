"""Known answers of section 8 (math, no real result) + K1 SPARC mock + MUTATE helpers. Exit 1 on failure."""
from crg1_core import *
import sys
from scipy.integrate import quad
import crg1_sparc as SP, crg1_zoom as Z

def run():
    R = {}; ok = True
    def chk(name, val, tol):
        nonlocal ok
        p = bool(abs(val) <= tol); R[name] = dict(value=float(val), tol=tol, passed=p); ok &= p
    # core masses vs quadrature: M = pi S r0^2 B(r/r0), S = rho0 r0, r0=1, rho0=1
    for x in (0.1, 1.0, 7.0):
        q1 = quad(lambda r: 4 * math.pi * r * r / ((r + 1) * (r * r + 1)), 0, x, epsabs=1e-11, epsrel=1e-11)[0]
        q2 = quad(lambda r: 4 * math.pi * r * r / (r * r + 1) ** 1.5, 0, x, epsabs=1e-11, epsrel=1e-11)[0]
        chk("B_B_x%g" % x, q1 / (math.pi * B_B(x)) - 1, 1e-6); chk("B_S_x%g" % x, q2 / (math.pi * B_S(x)) - 1, 1e-6)
    S0, Rr = 1.0, 3.0
    for B in (B_B, B_S):
        M = math.pi * S0 * 0.5 ** 2 * float(B(Rr / 0.5))
        r0 = solve_r0(M, Rr, S0, B)
        chk("solve_r0_%s" % B.__name__, math.pi * S0 * r0 ** 2 * float(B(Rr / r0)) / M - 1, 1e-8)
    for t in BGS:
        chk("K_S_sigma8_" + t, bg(t).sigma8() - bg(t).sigma8_given, 1e-3)
    # contract
    r = np.geomspace(0.01, 100, 400); M0 = 3 * r ** 2 / (1 + r)
    out = contract(r, np.zeros_like(r), M0, 0.0)
    chk("contract_null", np.max(np.abs(out[5:-5] / M0[5:-5] - 1)), 1e-6)
    k, Mp, Fv = 1.0, 2.0, 0.1
    M0 = k * r; Mf = contract(r, np.full_like(r, Mp), M0, Fv)
    # r_f(M_p+M_f(r_f)) = r_i k r_i (1+F): M_f(r_f) = k r_i. Direct check on a mid range
    ri = np.geomspace(0.5, 50, 30); rfs = []
    for q in ri:
        # solve rf (Mp + k q) = q k q (1+F)
        rfs.append(q * k * q * (1 + Fv) / (Mp + k * q))
    rfs = np.array(rfs); Mfi = np.interp(np.log(rfs), np.log(r), Mf)
    s = (rfs > r[3]) & (rfs < r[-3])
    chk("contract_point_mass", np.max(np.abs(rfs[s] * (Mp + Mfi[s]) / (ri[s] * k * ri[s] * (1 + Fv)) - 1)), 1e-3)
    # wls
    n, d, X = np.array([1., 2, 3]), np.array([2., 1, 5]), np.array([[1, .3], [1, -.2], [1, .7]])
    A = np.zeros((2, 2)); y = np.zeros(2)
    for i in range(3):
        A += d[i] * np.outer(X[i], X[i]); y += n[i] * X[i]
    chk("wls", np.max(np.abs(wls(n, d, X) - np.linalg.solve(A, y))), 1e-12)
    # zoom shape: sampled NFW c=4
    rng = np.random.default_rng(20261101)
    def mu(y): return np.log1p(y) - y / (1 + y)
    mr, r2r = [], []
    Gz = Z.G_Z; zz = 0.0
    thr = 200 * 3 * (100 * h_nat) ** 2 * (Om_nat + 1 - Om_nat) / (8 * math.pi * Gz)
    MM = 1e14; Rt = (3 * MM / (4 * math.pi * thr)) ** (1.0 / 3); cc = 4.0; rs = Rt / cc
    Xt = np.geomspace(1e-4, 40, 40000); cdf = mu(cc * Xt)
    N = 57777; mp = MM * mu(cc * 40) / mu(cc) / N
    for k_ in range(20):
        u = rng.random(N) * cdf[-1]; rr = np.interp(u, cdf, Xt) * Rt
        v = rng.normal(size=(N, 3)); v /= np.sqrt((v ** 2).sum(1))[:, None]; x = v * rr[:, None]
        lnmg, lg2, _xe, R2 = Z.shape_measure(x, mp, 1e-5, thr)
        xs = np.linspace(0.05, 1, 20)
        lnm = np.interp(np.log(xs), np.log(Z.XG), lnmg)
        mr.append(np.exp(lnm) / (mu(cc * xs) / mu(cc))); r2r.append(R2 / Rt)
    chk("zoom_shape_m_ratio", np.mean(mr, axis=0).max() - 1 if abs(np.mean(mr, axis=0).max() - 1) > abs(np.mean(mr, axis=0).min() - 1) else np.mean(mr, axis=0).min() - 1, 0.01)
    chk("zoom_shape_R200", np.mean(r2r) - 1, 0.01)
    # groups estimator vs second quadrature (law nu=1 -> Newton)
    XG = np.logspace(-5, 5, 3000); rho = 1 / (2 * math.pi * XG * (1 + XG) ** 3); MH = XG ** 2 / (1 + XG) ** 2
    val = np.trapz(4 * math.pi * XG ** 2 * rho * XG * (MH / XG ** 2) * XG, np.log(XG)) / 3
    q = quad(lambda x: 4 * math.pi * x * x / (2 * math.pi * x * (1 + x) ** 3) * x * (1 / (1 + x) ** 2) / 3, 0, np.inf, epsabs=1e-12, epsrel=1e-12)[0]
    chk("groups_newton_dex", 0.5 * math.log10(val / q), 1e-4)
    # SPARC mock
    G = SP.load_gal()
    for g in G:
        vb2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + 0.60 * g["Vdisk"] ** 2 + 1.4 * 0.60 * g["Vbul"] ** 2
        gm = law(vb2 * 1e6 / g["R"], A0["canonical"])
        v2 = g["R"] * gm / 1e6
        g["Vobs"] = np.sqrt(np.maximum(v2, 0))
    rr = SP.fit(G, SP.m_law(A0["canonical"]))
    chk("K1_sparc_mock_Ymed_minus_0.60", rr["Y_med"] - 0.60, 0.01)
    R["K1_sparc_mock_rms"] = rr["rms"]
    return ok, R

if __name__ == "__main__":
    ok, R = run()
    R["all_passed"] = ok
    save_part("k1_math", R)
    for k, v in R.items(): log("%s %s" % (k, v))
    sys.exit(0 if ok else 1)
