"""QX17C: finite-difference Newton solver for the static spherical v3s equations (same problem as QX17B sph_solve.py).
Criteria FROZEN_CRITERIA.md (77dc5bfff9). kappa = 1/2 FITTED; not theory closed. Geometrized units G = c = 1.

Scaled (as sph_solve.py): s = r/Lstar, Y = K p/a0, Z = K Pi Lstar/a0, Mh = m/M, Pm = K p_m/a0^2, eps = a0 Lstar,
ystar = M/(Lstar^2 a0).  Unknown Y_i on a grid from s_0 = 0 (Y_0 = 0, regular centre).
  node equation: (Z_{i+1/2} - Z_{i-1/2})/H_i = 2 ( B fW(Y/B) - (1 + eps Z_i/2) G_i )
  Z_{i+1/2} = [s^2 Y/B]_{i}^{i+1} / (h s_m^2 B_m),  s_m^2 = (s_i^2 + s_i s_{i+1} + s_{i+1}^2)/3
  mass: Mh = Mb + sum s_m^2 h (Z + eps (W + Z^2/4))/ystar  (weak: telescopes, G = gN + Y exactly)
Outer node: delta = Y - Y_S obeys delta'/delta = k dln k_1(ks)/d(ks), k^2 = 2 (1/(1-Y_S)^2 - 1).
Usage: python3 qx17c.py [MUTATE]
"""
import json, os, sys, time
import numpy as np
from scipy.linalg import solve_banded

HERE = os.path.dirname(os.path.abspath(__file__))
Gs, cs, Msun, pc, AU = 6.674e-11, 2.998e8, 1.989e30, 3.0857e16, 1.496e11
FOOT = {"canonical": (9.3603e-11, 21.7), "alt": (1.1312e-10, 22.9)}
MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
M_sun = Gs * Msun / cs**2; R_sun = 6.957e8
M_gal = Gs * 1e10 * Msun / cs**2; R_gal = 0.5e3 * pc

def fW(q): return q / (1 - q)
def fWp(q): return 1 / (1 - q)**2
def wW(q): return -q - np.log1p(-q)
def lawS_y(gN): return (-gN + np.sqrt(gN**2 + 4 * gN)) / 2       # a0 units

def grid(Sh, s_out, npd):
    s1 = min(1e-3 * Sh, 1e-3)
    g = np.geomspace(s1, s_out, int(npd * np.log10(s_out / s1)) + 1)
    w = 2e-3 * Sh
    lo, hi = Sh - 15 * w, Sh + 15 * w
    cl = np.linspace(lo, hi, int(npd * 1.2))           # cluster spacing ~ w/(npd/25)
    g = g[(g < lo - (cl[1] - cl[0])) | (g > hi + (cl[1] - cl[0]))]
    return np.concatenate([[0.0], np.sort(np.concatenate([g, cl]))])

class Problem:
    def __init__(self, M, R, a0_si, Lstar_pc, s_out_pc, npd, full, mutate=False):
        self.a0 = a0_si / cs**2; self.L = Lstar_pc * pc; self.M = M
        self.eps = self.a0 * self.L; self.ystar = M / (self.L**2 * self.a0); self.Sh = R / self.L
        self.full, self.mut = full, mutate
        s = grid(self.Sh, s_out_pc / Lstar_pc, npd); self.s = s
        self.h = np.diff(s); self.sm2 = (s[:-1]**2 + s[:-1] * s[1:] + s[1:]**2) / 3
        self.smid = (s[:-1] + s[1:]) / 2
        self.Hn = (s[2:] - s[:-2]) / 2                     # nodes 1..N-1
        kb = 3.0 / self.Sh**3
        self.rhob_n = kb * self.Hfun(s)                    # K Lstar^3 rho_b / M at nodes
        dMb = self.sm2 * self.h * kb * self.Hfun(self.smid)
        self.Mb = np.concatenate([[0.0], np.cumsum(dMb)])
        self.Mb /= self.Mb[-1]                             # unit bare mass (edge smoothing renormalised)
        sp = np.where(s > 0, s, 1.0)
        self.gN = np.where(s > 0, self.ystar * self.Mb / sp**2, 0.0)
        self.gN_bare = self.ystar / sp**2                   # exterior Newtonian field of the bare mass
        gNo = self.gN[-1]; self.YS_out = lawS_y(gNo)

    def Hfun(self, s):
        return 0.5 * (1 - np.tanh((s - self.Sh) / (2e-3 * self.Sh)))

    def fields(self, Y):
        """B, G, Z_mid, Z_node, Pm from the current Y (full: fixed-point on B and Pm)."""
        s, h, sm2 = self.s, self.h, self.sm2
        N1 = s.size
        B = np.ones(N1); Pm = np.zeros(N1)
        sp = np.where(s > 0, s, 1.0)
        for it in range(8 if self.full else 1):
            Bm = (B[:-1] + B[1:]) / 2
            Zm = np.diff(s**2 * Y / B) / (h * sm2 * Bm)
            Zn = np.concatenate([[Zm[0]], (Zm[:-1] + Zm[1:]) / 2, [Zm[-1]]])
            if not self.full:
                G = self.gN + (0 if self.mut else Y)
                return B, G, Zm, Zn, Pm
            q = Y / B; qm = (q[:-1] + q[1:]) / 2
            ph = sm2 * h * (Zm + self.eps * (wW(qm) + Zm**2 / 4)) / self.ystar
            Mh = self.Mb + (0 if self.mut else np.concatenate([[0.0], np.cumsum(ph)]))
            twoU = np.where(s > 0, 2 * self.M * Mh / (self.L * sp), 0.0)
            Bn = 1 / np.sqrt(1 - twoU)
            G = np.where(s > 0, (twoU / (1 - twoU)) / (2 * self.eps * sp), 0.0) \
                + self.eps * s * Bn**2 * (Zn**2 / 4 - wW(Y / Bn) + Pm)
            # TOV, backward trapezoid from Pm(s_out) = 0 (p_m' = -(rho + p_m) Phi')
            src = -(self.rhob_n * self.ystar) * G
            Pn = np.zeros(N1)
            for i in range(N1 - 2, -1, -1):
                a = self.eps * G[i] * h[i] / 2; b = self.eps * G[i + 1] * h[i] / 2
                Pn[i] = (Pn[i + 1] * (1 + b) - h[i] / 2 * (src[i] + src[i + 1])) / (1 - a)
            B, Pm = Bn, Pn
        return B, G, Zm, Zn, Pm

    def residual(self, Y):
        B, G, Zm, Zn, Pm = self.fields(Y)
        q = Y / B
        lhs = (Zm[1:] - Zm[:-1]) / self.Hn
        rhs = 2 * (B[1:-1] * fW(q[1:-1]) - (1 + self.eps * Zn[1:-1] / 2) * G[1:-1])
        R = lhs - rhs
        scale = (np.abs(Zm[1:]) + np.abs(Zm[:-1])) / self.Hn + 2 * np.abs(B[1:-1] * fW(q[1:-1])) + 2 * np.abs(G[1:-1]) + 1e-300
        # outer Robin row
        s = self.s; hN = self.h[-1]; smN = self.smid[-1]
        YS1 = lawS_y(self.gN[-2]); YSN = self.YS_out
        k = np.sqrt(2 * (1 / (1 - (YS1 + YSN) / 2)**2 - 1)); x = k * smN
        kap = k * (-1 - (x + 2) / (x * (x + 1)))
        dN, d1 = Y[-1] - YSN, Y[-2] - YS1
        Rb = (dN - d1) / hN - kap * (dN + d1) / 2
        ab_ = abs(Y[-1]) + abs(YSN) + abs(Y[-2]) + abs(YS1)       # round-off-aware: sizes of the terms entering the row
        sb = ab_ / hN + abs(kap) * ab_ / 2 + 1e-300
        return np.concatenate([R, [Rb]]), np.concatenate([scale, [sb]]), (kap, hN)

    def jac(self, Y, kap, hN):
        s, h, sm2, Hn = self.s, self.h, self.sm2, self.Hn
        n = s.size - 1                                     # unknowns Y_1..Y_N
        up = np.zeros(n); dg = np.zeros(n); lo = np.zeros(n)
        i = np.arange(1, s.size - 1)
        cp = s[i]**2 / (h[i] * sm2[i]) / Hn                 # from Z_{i+1/2}
        cm = s[i]**2 / (h[i - 1] * sm2[i - 1]) / Hn         # from Z_{i-1/2}
        a_up = s[i + 1]**2 / (h[i] * sm2[i]) / Hn
        a_lo = s[i - 1]**2 / (h[i - 1] * sm2[i - 1]) / Hn
        dfd = fWp(Y[i]) - (0 if self.mut else 1)
        dg[:-1] = -cp - cm - 2 * dfd
        up[:-1] = a_up; lo[:-1] = a_lo
        dg[-1] = 1 / hN - kap / 2; lo[-1] = -1 / hN - kap / 2
        ab = np.zeros((3, n)); ab[0, 1:] = up[:-1]; ab[1] = dg
        # lo[k] multiplies Y_{k-1} in row k  -> ab[2, k-1]
        ab[2, :-1] = lo[1:]
        return ab

    def guess(self):
        s = self.s
        YS = lawS_y(np.maximum(self.gN, 1e-300))
        Yh = self.ystar * np.minimum(s / self.Sh, 1.0)
        Y = 1 / (1 / np.maximum(YS, 1e-300) + 1 / np.maximum(Yh, 1e-300)); Y[0] = 0.0
        return np.minimum(Y, 0.999)

    def solve(self, Y=None, maxit=200):
        Y = self.guess() if Y is None else Y.copy()
        for it in range(maxit):
            R, sc, (kap, hN) = self.residual(Y)
            err = float(np.max(np.abs(R) / sc))
            if err <= 1e-10: break
            d = solve_banded((1, 1), self.jac(Y, kap, hN), -R)
            lam = 1.0
            for _ in range(40):
                Yn = Y.copy(); Yn[1:] += lam * d
                ok = np.all(Yn[1:] / 1.0 < 1) and np.all(np.isfinite(Yn))
                if ok:
                    Rn, scn, _ = self.residual(Yn)
                    en = float(np.max(np.abs(Rn) / scn))
                    if np.isfinite(en) and (en < err or lam < 1e-3): break
                lam /= 2
            Y = Yn
        R, sc, _ = self.residual(Y)
        self.err = float(np.max(np.abs(R) / sc)); self.iters = it
        self.Y = Y
        return Y

    def Yat(self, s_q):
        return np.exp(np.interp(np.log(s_q), np.log(self.s[1:]), np.log(np.maximum(self.Y[1:], 1e-300))))

def lawS_dev(P, r_m):
    sq = r_m / P.L
    gN = P.ystar / sq**2
    return np.abs((gN + P.Yat(sq)) / (gN + lawS_y(gN)) - 1)

def run_set(a0si, Ls, npd, sfac):
    """all graded numbers at one (grid density, outer edge) setting"""
    o = {}; t0 = time.time()
    sun = {f: Problem(M_sun, R_sun, a0si, Ls, 1e5 * sfac, npd, f, MUT) for f in (False, True)}
    for f in (False, True): sun[f].solve(sun[False].Y if f else None)
    gal = {f: Problem(M_gal, R_gal, a0si, Ls, 3e6 * sfac, npd, f, MUT) for f in (False, True)}
    for f in (False, True): gal[f].solve(gal[False].Y if f else None)
    kn = Problem(M_gal, R_gal, a0si, 1e-3, 3e6 * sfac, npd, False, MUT); kn.solve()
    o["newton_err"] = {"sun_weak": sun[False].err, "sun_full": sun[True].err, "gal_weak": gal[False].err,
                       "gal_full": gal[True].err, "known": kn.err}
    o["n_nodes"] = {"sun": int(sun[True].s.size), "gal": int(gal[True].s.size), "known": int(kn.s.size)}
    rk = np.geomspace(1e3, 3e4, 60) * pc
    o["G1_known_lawS_maxdev"] = float(np.max(lawS_dev(kn, rk)))
    P = sun[True]; gstar = P.ystar
    sq = np.geomspace(10 * AU, 1e-3 * P.L, 200) / P.L
    o["G2_sun_hedgehog_maxdev"] = float(np.max(np.abs(P.Yat(sq) / gstar - 1)))
    o["sun_y_over_gstar_1_10_100AU"] = (P.Yat(np.array([1, 10, 100]) * AU / P.L) / gstar).tolist()
    ext = np.geomspace(2 * R_sun, 1e3 * P.L, 400) / P.L
    yf, yw = sun[True].Yat(ext), sun[False].Yat(ext)
    o["G3_sun_GR_remainder"] = float(np.max(np.abs(yf - yw) / np.abs(yw))); o["sun_Umax"] = M_sun / R_sun
    o["G4_gal_lawS_maxdev"] = float(np.max(lawS_dev(gal[True], rk)))
    ext = np.geomspace(2 * R_gal, 1e5 * pc, 400) / gal[True].L
    yf, yw = gal[True].Yat(ext), gal[False].Yat(ext)
    o["G5_gal_GR_remainder"] = float(np.max(np.abs(yf - yw) / np.abs(yw))); o["gal_Umax"] = M_gal / R_gal
    far = np.array([1, 3, 10, 30, 100, 1000.0])
    gN = P.ystar / far**2
    o["sun_g_over_gS_1_3_10_30_100_1000_Lstar"] = ((gN + P.Yat(far)) / (gN + lawS_y(gN))).tolist()
    o["sun_min_Y_over_ystar_inside_1e3L"] = float(np.min(P.Y[1:][P.s[1:] < 1e3] / P.ystar))
    o["seconds"] = round(time.time() - t0, 1)
    return o, sun, gal

def x1_crosscheck(a0si, Ls, sun_w, gal_w):
    """X1: weak exterior vs QX17B solve_bvp (its weak runs converged)."""
    src = open(os.path.join(HERE, "..", "QX17B_adm_lean_solutions", "sph_solve.py")).read().split("\nmode = sys.argv")[0]
    ns = {"__file__": os.path.join(HERE, "..", "QX17B_adm_lean_solutions", "sph_solve.py")}
    exec(src, ns)
    out = {}
    for name, M, R, so, P in (("sun", M_sun, R_sun, 1e5, sun_w), ("gal", M_gal, R_gal, 3e6, gal_w)):
        sol, par = ns["solve"](M, R, a0si, Ls, False, s_out_pc=so)
        hi = 1e3 * par["L"] if name == "sun" else 1e5 * pc
        ext = np.geomspace(2 * R, hi, 400) / par["L"]
        yb = sol.sol(np.log(ext))[0] * par["Yref"]
        out[name] = {"bvp_status": int(sol.status), "max_rel": float(np.max(np.abs(P.Yat(ext) / yb - 1)))}
    return out

TOL = {"G1_known_lawS_maxdev": 1e-3, "G2_sun_hedgehog_maxdev": 1e-2, "G3_sun_GR_remainder": None,
       "G4_gal_lawS_maxdev": 1e-2, "G5_gal_GR_remainder": None}

res = {"mode": "MUTATE" if MUT else "main"}
for foot, (a0si, Ls) in FOOT.items():
    base, sun, gal = run_set(a0si, Ls, 500, 1)
    dbl, _, _ = run_set(a0si, Ls, 1000, 1)
    far, _, _ = run_set(a0si, Ls, 500, 10)
    tol = dict(TOL); tol["G3_sun_GR_remainder"] = 10 * base["sun_Umax"]; tol["G5_gal_GR_remainder"] = 10 * base["gal_Umax"]
    row = {"base": base, "grid_x2": dbl, "s_out_x10": far, "gates": {}}
    C1 = max(max(d["newton_err"].values()) for d in (base, dbl, far)) <= 1e-9
    for g, t in tol.items():
        c2 = abs(dbl[g] - base[g]); c3 = abs(far[g] - base[g])
        conv = C1 and c2 <= 0.1 * t and c3 <= 0.1 * t
        row["gates"][g] = {"value": base[g], "tol": t, "grid_change": c2, "edge_change": c3, "converged": conv,
                           "verdict": ("PASS" if base[g] <= t else "FAIL") if conv else "NO VERDICT"}
    if not MUT:
        x1 = x1_crosscheck(a0si, Ls, sun[False], gal[False])
        row["gates"]["X1"] = {**x1, "verdict": "PASS" if all(v["bvp_status"] == 0 and v["max_rel"] <= 1e-3
                                                            for v in x1.values()) else "FAIL"}
    row["C1_newton"] = C1
    res[foot] = row
    print(foot, json.dumps(row["gates"]), "C1", C1, flush=True)
json.dump(res, open(os.path.join(HERE, "qx17c_MUTATE.json" if MUT else "qx17c.json"), "w"), indent=1)
print("EXIT 0")
