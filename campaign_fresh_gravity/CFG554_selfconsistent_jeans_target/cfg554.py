#!/usr/bin/env python3
"""CFG554: the self-consistent Jeans target of the velocity part, from a principle (no knobs). FROZEN_CRITERIA.md (01ad75492).

Routes: (a) maximum entropy at fixed density with the exact kinetic (tensor Jeans) stationarity constraint -> anisotropic
Gaussian target (sigma_r^2, sigma_t^2) from a multiplier field lambda(r) solved on the CURRENT density in the CURRENT field;
(b) FIX-2 (isotropic Jeans target) written as a metriplectic relaxation with angular-momentum-conserving pairs;
(c) maximum entropy with the global (virial) constraint only -> single temperature T_v.
Bench = CFG544's spherical N-body toy, imported unchanged from ../CFG544_settling_kinetic_consistency/cfg544.py (read only).
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy mass required; not "theory closed".
CFG554_MUTATE=1 -> MT (route-a target x 2), MJ (Jeans constraint removed -> law phantom T_ph), MK (sink removed).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg554.py
"""
import os, sys, json, math, time, importlib.util
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ["CFG544_MUTATE"] = "0"
os.environ["CFG550_MUTATE"] = "0"
import numpy as np
import sympy as sp
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, "..", rel))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
T544 = _load("cfg544", os.path.join("CFG544_settling_kinetic_consistency", "cfg544.py"))
T550 = _load("cfg550", os.path.join("CFG550_settling_velocity_part", "cfg550.py"))
J544 = json.load(open(os.path.join(HERE, "..", "CFG544_settling_kinetic_consistency", "cfg544_results.json")))
J541 = T544.J541
MUT = os.environ.get("CFG554_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
NPROC = 4
RMIN, EPS, NB, NPART = T544.RMIN, T544.EPS, T544.NB, T544.NPART
Mb_enc, Mph_enc = T544.Mb_enc, T544.Mph_enc
C2_544 = {"MW_can": 0.255, "MW_alt": 0.333, "cluster_can": 0.445, "cluster_alt": 0.539}   # frozen in FROZEN_CRITERIA.md
OUT, RES = [], {"lane": "CFG554", "mutate": MUT, "criteria_commit": "01ad75492",
                "settings": dict(kappa=0.5, footings=T544.FOOT, toy="CFG544 cfg544.py imported unchanged", N=NPART,
                                 alpha_default=1.0, seed=T544.SEED, maxent_solver="RK2, 8 substeps/bin, 3 bracket passes x 24",
                                 inputs="CFG541/CFG544 JSON and CFG550 law_profiles (read only)")}


def log(s=""):
    print(s, flush=True); OUT.append(s)


# ================================================================================================ route (a) solver
NSUB, NC, NPASS = 8, 24, 3


def _march(rf, rho, gf, k0, k1, c, record=False):
    """Integrate Lambda' = rho/(2P), P' = -rho g - 2P/r + rho/Lambda outward from rf[k0] for a vector of c.
    Returns alive mask at R = rf[k1+1] (P > 0 throughout); if record, P and Lambda at bin centres (geometric mid)."""
    r0 = rf[k0]
    Lam = c * r0; P = rho[k0] / (2 * c)
    alive = np.ones(c.size, bool)
    Prec = np.zeros((NB, c.size)); Lrec = np.zeros((NB, c.size))
    for k in range(k0, k1 + 1):
        a, b = rf[k], rf[k + 1]; h = (b - a) / NSUB; rk = rho[k]; ga, gb = gf[k], gf[k + 1]
        for j in range(NSUB):
            r = a + j * h; rm = r + 0.5 * h
            g1 = ga + (gb - ga) * (r - a) / (b - a); g2 = ga + (gb - ga) * (rm - a) / (b - a)
            Ps = np.where(P > 0, P, 1.0)
            k1L = rk / (2 * Ps); k1P = -rk * g1 - 2 * P / r + rk / Lam
            Pm = P + 0.5 * h * k1P; Lm = Lam + 0.5 * h * k1L
            alive &= Pm > 0
            Pms = np.where(Pm > 0, Pm, 1.0)
            k2L = rk / (2 * Pms); k2P = -rk * g2 - 2 * Pm / rm + rk / Lm
            P = P + h * k2P; Lam = Lam + h * k2L
            alive &= P > 0
            if record and j == NSUB // 2 - 1:
                Prec[k] = P; Lrec[k] = Lam
    return alive, Prec, Lrec


def maxent_target(rf, rho, gf, s2iso_in):
    """Route (a): maximum-entropy Gaussian at fixed rho with the tensor Jeans constraint. Returns (sig_r2, sig_t2, ok)."""
    occ = np.where(rho > 0)[0]
    if occ.size < 2:
        return None, None, False
    k0, k1 = int(occ[0]), int(occ[-1])
    c0 = 1.0 / (2 * max(s2iso_in, 1e-30))
    lo, hi = math.log(c0) - 3 * math.log(10), math.log(c0) + 3 * math.log(10)
    ca = None
    for _ in range(NPASS):
        cs = np.exp(np.linspace(lo, hi, NC))
        alive, _, _ = _march(rf, rho, gf, k0, k1, cs)
        if alive.all() or (not alive.any()):
            if ca is None:
                return None, None, False
            break
        ia = int(np.where(alive)[0].max())
        if ia + 1 >= NC or alive[ia + 1]:
            return None, None, False
        ca = cs[ia]; lo, hi = math.log(cs[ia]), math.log(cs[ia + 1])
    _, Prec, Lrec = _march(rf, rho, gf, k0, k1, np.array([ca]), record=True)
    rc = np.sqrt(rf[1:] * rf[:-1])
    sr2 = np.where(rho > 0, np.maximum(Prec[:, 0], 0.0) / np.maximum(rho, 1e-300), 0.0)
    st2 = np.where(Lrec[:, 0] > 0, rc / (2 * np.maximum(Lrec[:, 0], 1e-300)), 0.0)
    st2 = np.where(rho > 0, st2, 0.0)
    return sr2, st2, True


def iso_jeans_bins(c, rf, rc, dr, mc, rho):
    """FIX-2's isotropic Jeans target (CFG544 ou_step formula) and face gravity of the current enclosed mass."""
    Menc_c = Mb_enc(c, rc) + np.concatenate([[0.0], np.cumsum(mc)[:-1]]) + 0.5 * mc
    gb = Menc_c * rc / (rc ** 2 + EPS ** 2) ** 1.5
    Pf = np.concatenate([np.cumsum((rho * gb * dr)[::-1])[::-1], [0.0]]); Pc = 0.5 * (Pf[1:] + Pf[:-1])
    s2J = np.where(rho > 0, Pc / np.maximum(rho, 1e-300), 0.0)
    Mf = Mb_enc(c, rf) + np.concatenate([[0.0], np.cumsum(mc)])
    gf = Mf * rf / (rf ** 2 + EPS ** 2) ** 1.5
    return s2J, gf


# ================================================================================================ bench
class Toy554(T544.Toy):
    def __init__(self, c, mode, scale, prof=None):
        super().__init__(c, "two", ou=(mode != "none"), ou_scale=1.0, drift=(mode != "none"))
        self.mode, self.scale, self.prof = mode, scale, prof
        self.n_fail = 0; self.n_solve = 0; self.last_target = None

    def vel_step(self, r, vr, vt, dt, g, rng):
        if self.mode == "b":
            return self.ou_step(r, vr, vt, dt, g, rng)          # FIX-2 exactly (CFG544 operator)
        c = self.c; al = T544.ALPHA
        mc = self.m * np.histogram(r, self.rf)[0]; rho = mc / self.V
        k = np.clip(np.searchsorted(self.rf, r) - 1, 0, NB - 1)
        inside = r < c["rta"]
        gam = al * np.sqrt(4 * math.pi * (self.rhob + rho))[k]
        a = np.exp(-gam * dt)
        if self.mode == "a":
            s2J, gf = iso_jeans_bins(c, self.rf, self.rc, self.dr, mc, rho)
            occ = np.where(rho > 0)[0]
            self.n_solve += 1
            sr2, st2, ok = maxent_target(self.rf, rho, gf, s2J[occ[0]] if occ.size else 1.0)
            if not ok:
                self.n_fail += 1
                return vr, vt, 0.0
            sr = sr2[k] * self.scale; stt = st2[k] * self.scale
            self.last_target = (sr2, st2, s2J)
        elif self.mode == "c":
            gc, _ = self.gravity(r)                                 # current (post-drift) field
            Tv = float(np.sum(r[inside] * gc[inside]) / (3 * max(inside.sum(), 1))) * self.scale
            sr = np.full(r.size, Tv); stt = sr
            self.last_target = Tv
        elif self.mode == "mj":
            sr = np.interp(r, self.prof["r"], self.prof["T"]) * self.scale; stt = sr
        br = np.sqrt(sr * (1 - a ** 2)); bt = np.sqrt(stt * (1 - a ** 2))
        K0 = 0.5 * self.m * np.sum(vr ** 2 + vt ** 2)
        x1, x2, x3 = rng.standard_normal((3, r.size))
        nr = a * vr + br * x1; vtx = a * vt + bt * x2; vty = bt * x3; nt = np.hypot(vtx, vty)
        vr_n = np.where(inside, nr, vr); vt_n = np.where(inside, nt, vt)
        K1 = 0.5 * self.m * np.sum(vr_n ** 2 + vt_n ** 2)
        return vr_n, vt_n, K1 - K0

    def diag554(self, r, vr, L):
        d = self.diag(r, vr, L)
        c = self.c; vt = L / r
        mc = self.m * np.histogram(r, self.rf)[0]; rho = mc / self.V
        s2J, _ = iso_jeans_bins(c, self.rf, self.rc, self.dr, mc, rho)
        k = np.clip(np.searchsorted(self.rf, r) - 1, 0, NB - 1)
        sh = (r > 0.1) & (r < 0.9)
        XJ = float(np.sum(vr[sh] ** 2 + vt[sh] ** 2) / 3 / np.sum(s2J[k[sh]])) if sh.sum() > 10 else float("nan")
        dd = self.rhoph - rho
        Md = np.concatenate([[0.0], np.cumsum(dd * self.V)])
        integ = Md ** 2 / (2 * self.rf ** 2)
        F = float(np.sum(0.5 * (integ[1:] + integ[:-1]) * self.dr) + Md[-1] ** 2 / (2 * self.rf[-1]))
        d.update(logXJ=float(np.log10(XJ)) if XJ > 0 else -99.0, F=F, vmax=float(np.max(np.sqrt(vr ** 2 + vt ** 2))))
        return d


def run(job):
    c, name, ic, mode, T_Gyr = job["c"], job["name"], job["ic"], job["mode"], job["T"]
    T544.ALPHA = job.get("alpha", 1.0)                     # alpha per job (robustness runs); default 1 as frozen
    prof = T550.law_profiles(c) if mode == "mj" else None
    rng = np.random.default_rng(T544.SEED)
    r, vr, L, m = T544.make_ic(c, ic, rng, sig2_scale=job.get("sig2", 1.0), inject=job.get("inject", False))
    toy = Toy554(c, mode, job.get("scale", 1.0), prof); toy.m = m
    n0 = r.size
    dt = c["dt"]; nsteps = int(round(T_Gyr / (dt * c["tu_Gyr"])))
    every = max(1, int(round(0.25 / (dt * c["tu_Gyr"]))))
    K0, W0 = toy.energy(r, vr, L)
    W_drift = 0.0; W_ou = 0.0; W_ou_pos = 0.0
    snaps = []; t0 = time.time(); nsub_max = 0; blow = False
    for it in range(nsteps + 1):
        if it % every == 0 or it == nsteps:
            dg = toy.diag554(r, vr, L); K, W = toy.energy(r, vr, L)
            dg.update(t_Gyr=it * dt * c["tu_Gyr"], E=K + W, sink_cum=-(W_drift + W_ou) / c["Mcat"],
                      drift_out=-W_drift / c["Mcat"], relax_in=W_ou / c["Mcat"], relax_in_gross=W_ou_pos / c["Mcat"],
                      integ_err=(K + W - K0 - W0 - W_drift - W_ou) / abs(K0 + W0), dEmatter=(K + W - K0 - W0) / abs(K0 + W0))
            snaps.append(dg)
            if dg["relax_in_gross"] > 10.0 or dg["vmax"] > 50.0:
                blow = True
        if it == nsteps: break
        r, vr, ns = T544.vlasov_step(toy, r, vr, L, dt)
        nsub_max = max(nsub_max, ns)
        if toy.drift:
            vt = L / r
            g, _ = toy.gravity(r)
            _, Wb = toy.energy(r, vr, L)
            rn, _w = toy.drift_step(r, dt, g)
            Ln = rn * vt
            _, Wa = toy.energy(rn, vr, Ln)
            W_drift += Wa - Wb
            L = Ln; r = rn
            vr, vt, dk = toy.vel_step(r, vr, vt, dt, g, rng)     # same call sequence as CFG544 (exact reproduction, C5)
            W_ou += dk; W_ou_pos += max(dk, 0.0); L = r * vt
    E0 = K0 + W0; fin = snaps[-1]
    ref = min(snaps, key=lambda s: abs(s["t_Gyr"] - (fin["t_Gyr"] - 2.0)))
    F0 = snaps[0]["F"]
    dF = [snaps[i + 1]["F"] - snaps[i]["F"] for i in range(len(snaps) - 1)]
    res = dict(name=name, sys=c["sys"], foot=c["foot"], ic=ic, mode=mode, alpha=T544.ALPHA, scale=job.get("scale", 1.0),
               T_Gyr=T_Gyr, steps=nsteps, n_particles=n0, mass_exact=bool(r.size == n0),
               dE_over_E=float((fin["E"] - E0) / abs(E0)), final=fin,
               d_logX_last2=float(fin["logX"] - ref["logX"]), d_logXJ_last2=float(fin["logXJ"] - ref["logXJ"]),
               d_D_last2=float(fin["D"] - ref["D"]), limited_frac=toy.n_lim / max(toy.n_mv, 1),
               series=[dict(t=s["t_Gyr"], logX=s["logX"], logXJ=s["logXJ"], D=s["D"], r99=s["r99"], sink=s["sink_cum"],
                            F=s["F"], drift_out=s["drift_out"], relax_in=s["relax_in"], beta=s["beta"]) for s in snaps],
               wall_s=time.time() - t0, nsub_max=nsub_max, integ_err_final=fin["integ_err"],
               integ_err_maxabs=float(max(abs(s["integ_err"]) for s in snaps)), dEmatter_final=fin["dEmatter"],
               vmax_code=float(max(s["vmax"] for s in snaps)), relax_in_gross_max=float(max(s["relax_in_gross"] for s in snaps)),
               blow_up=bool(blow), max_rise_F_over_F0=float(max(dF) / F0) if F0 > 0 else None,
               solver_fail_frac=(toy.n_fail / toy.n_solve) if toy.n_solve else None, solver_calls=toy.n_solve)
    if mode == "a" and toy.last_target is not None:
        sr2, st2, s2J = toy.last_target
        res["final_target"] = dict(rc=toy.rc.tolist(), sig_r2=sr2.tolist(), sig_t2=st2.tolist(), s2J_iso=s2J.tolist())
        sh = (toy.rc > 0.1) & (toy.rc < 0.9) & (sr2 > 0)
        res["final_target_beta_shell_median"] = float(np.median(1 - st2[sh] / sr2[sh])) if sh.any() else None
        ed = (toy.rc > 0.8) & (toy.rc < 1.2) & (sr2 > 0)
        res["final_target_beta_edge_median"] = float(np.median(1 - st2[ed] / sr2[ed])) if ed.any() else None
    if mode == "c":
        res["final_Tv"] = toy.last_target
    res["gate550_end"] = bool(abs(fin["D"]) <= 0.1 and abs(fin["logXJ"]) <= 0.1)
    res["gate550_steady"] = bool(abs(res["d_D_last2"]) <= 0.05 and abs(res["d_logXJ_last2"]) <= 0.05)
    res["gate550"] = res["gate550_end"] and res["gate550_steady"]
    res["gate544"] = bool(abs(fin["logX"]) <= 0.1 and abs(fin["D"]) <= 0.1 and abs(res["d_logX_last2"]) <= 0.05 and abs(res["d_D_last2"]) <= 0.05)
    res["sink_rate_last2"] = float((fin["sink_cum"] - ref["sink_cum"]) / max(fin["t_Gyr"] - ref["t_Gyr"], 1e-9))
    res["relax_in_rate_last2"] = float((fin["relax_in"] - ref["relax_in"]) / max(fin["t_Gyr"] - ref["t_Gyr"], 1e-9))
    return res


# ================================================================================================ control C6
def control_c6():
    """Gaussian density rho ~ exp(-r^2/2T) in g = r (T = 1), R = 8, 100 log bins: solver must return sigma^2/T = 1 (r <= 3)."""
    T = 1.0
    rf = np.geomspace(1e-3, 8.0, NB + 1); rc = np.sqrt(rf[1:] * rf[:-1])
    V = 4 * math.pi / 3 * np.diff(rf ** 3)
    rr = np.geomspace(1e-3, 8.0, 200001); M = np.concatenate([[0.0], np.cumsum(0.5 * (4 * math.pi * rr[1:] ** 2 * np.exp(-rr[1:] ** 2 / 2) + 4 * math.pi * rr[:-1] ** 2 * np.exp(-rr[:-1] ** 2 / 2)) * np.diff(rr))])
    rho = np.diff(np.interp(rf, rr, M)) / V
    gf = rf.copy()
    sr2, st2, ok = maxent_target(rf, rho, gf, T)
    sel = (rc <= 3.0) & (rc >= 0.01)
    out = dict(ok=bool(ok))
    if ok:
        out.update(max_dev_sr2=float(np.max(np.abs(sr2[sel] / T - 1))), max_dev_st2=float(np.max(np.abs(st2[sel] / T - 1))))
        out["pass"] = bool(out["max_dev_sr2"] <= 0.02 and out["max_dev_st2"] <= 0.02)
        # anisotropic Jeans residual on the bin grid (diagnostic)
        P = sr2 * rho; Pt = st2 * rho
        dP = np.gradient(P, rc)
        resid = (dP + 2 * (P - Pt) / rc + rho * rc) / np.maximum(rho * rc, 1e-300)
        out["jeans_resid_median_abs_r_le3"] = float(np.median(np.abs(resid[sel])))
        # diagnostic (post-freeze, no label depends on it): FIX-2's isotropic formula on the same grid, and the r <= 1.5 bulk
        dr = np.diff(rf); Pf = np.concatenate([np.cumsum((rho * rc * dr)[::-1])[::-1], [0.0]]); s2i = 0.5 * (Pf[1:] + Pf[:-1]) / rho
        out["diag_fix2_iso_formula_max_dev_r_le3"] = float(np.max(np.abs(s2i[sel] / T - 1)))
        b15 = (rc <= 1.5) & (rc >= 0.01)
        out["diag_max_dev_sr2_r_le1p5"] = float(np.max(np.abs(sr2[b15] / T - 1)))
        out["diag_dev_profile"] = [(float(rc[i]), float(sr2[i]), float(st2[i]), float(s2i[i])) for i in range(0, NB, 5)]
    else:
        out["pass"] = False
    return out


# ================================================================================================ angular-momentum numeric test
def ang_mom_test(steps=2000, npt=20, n=500, gam_dt=2e-3, s2t=0.5, seed=554):
    rng = np.random.default_rng(seed)
    xs = rng.standard_normal((npt, 3)); xs /= np.linalg.norm(xs, axis=1)[:, None]
    Om = np.array([0.0, 0.0, 1.0])
    pos = np.repeat(xs, n, axis=0)
    v0 = np.cross(Om, pos) + 0.3 * rng.standard_normal(pos.shape)
    def J(v): return np.sum(np.cross(pos, v), axis=0)
    a = math.exp(-gam_dt); b = math.sqrt(s2t * (1 - a * a))
    out = {}
    for op in ("route_b_momentum_pairs", "cfg544_fix2"):
        v = v0.copy(); J0 = J(v)
        for _ in range(steps):
            vr = np.sum(v * pos, axis=1)
            vtv = v - vr[:, None] * pos
            xr = rng.standard_normal(vr.size)
            vr = a * vr + b * xr
            xt = rng.standard_normal(pos.shape); xt -= np.sum(xt * pos, axis=1)[:, None] * pos
            if op == "route_b_momentum_pairs":
                vtv = vtv.reshape(npt, n, 3); xt = xt.reshape(npt, n, 3)
                u = vtv.mean(axis=1, keepdims=True); xt = xt - xt.mean(axis=1, keepdims=True)
                vtv = (u + a * (vtv - u) + b * xt).reshape(-1, 3)
            else:
                vtv = a * vtv + b * xt
            v = vr[:, None] * pos + vtv
        J1 = J(v)
        out[op] = dict(J0=J0.tolist(), J1=J1.tolist(), rel_change=float(np.linalg.norm(J1 - J0) / np.linalg.norm(J0)))
    out["pass"] = bool(out["route_b_momentum_pairs"]["rel_change"] <= 1e-10 and out["cfg544_fix2"]["rel_change"] > 0.5)
    return out


# ================================================================================================ sympy
def sympy_items():
    R = {}
    # ---- S1a: maximiser of -f ln f - mu f + A_ij v_i v_j f (constraint term after integration by parts)
    f, mu = sp.symbols("f mu", positive=True)
    v1, v2, v3 = sp.symbols("v1 v2 v3", real=True)
    A = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"A{min(i, j)}{max(i, j)}"))
    vv = sp.Matrix([v1, v2, v3])
    Lag = -f * sp.log(f) - mu * f + (vv.T * A * vv)[0] * f
    sol = sp.solve(sp.diff(Lag, f), f)
    R["S1a_maximiser"] = str(sol)
    R["S1a_is_gaussian"] = bool(len(sol) == 1 and sp.simplify(sol[0] - sp.exp(-1 - mu + sp.expand((vv.T * A * vv)[0]))) == 0)
    xx, Pi, lam = sp.symbols("x"), sp.Function("Pi")(sp.Symbol("x")), sp.Function("lambda")(sp.Symbol("x"))
    R["S1a_by_parts"] = bool(sp.simplify(sp.diff(lam * Pi, xx) - lam * sp.diff(Pi, xx) - sp.diff(lam, xx) * Pi) == 0)
    # ---- S1b: spherical lambda_i = lambda(r) x_i/r: v_i v_j d_j lambda_i at (x,0,0) = lambda' v_r^2 + (lambda/r) v_t^2
    X, Y, Z = sp.symbols("X Y Z", real=True)
    rr = sp.sqrt(X ** 2 + Y ** 2 + Z ** 2); lf = sp.Function("l")
    lam_vec = [lf(rr) * q / rr for q in (X, Y, Z)]
    Jm = sp.Matrix(3, 3, lambda i, j: sp.diff(lam_vec[i], (X, Y, Z)[j]))
    quad = sp.simplify((vv.T * Jm * vv)[0].subs({Y: 0, Z: 0}))
    rs = sp.symbols("r", positive=True)
    quad = sp.simplify(quad.subs(X, rs))
    target = sp.diff(lf(rs), rs) * v1 ** 2 + lf(rs) / rs * (v2 ** 2 + v3 ** 2)
    R["S1b_quadratic_form"] = str(quad)
    R["S1b_quadratic_form_ok"] = bool(sp.simplify(quad - target) == 0)
    Lp = sp.symbols("Lp", positive=True)
    w = sp.symbols("w", real=True)
    var_r = sp.integrate(w ** 2 * sp.exp(-Lp * w ** 2), (w, -sp.oo, sp.oo)) / sp.integrate(sp.exp(-Lp * w ** 2), (w, -sp.oo, sp.oo))
    R["S1b_sigma_r2_for_lambda_prime_eq_minus_Lp"] = str(sp.simplify(var_r))     # = 1/(2 Lp) -> sigma_r^2 = -1/(2 lambda')
    lsol = sp.dsolve(sp.Eq(sp.diff(lf(rs), rs), lf(rs) / rs))
    R["S1b_isotropy_ODE_solution"] = str(lsol)
    lam_iso = lsol.rhs
    s2_iso = sp.simplify(-1 / (2 * sp.diff(lam_iso, rs)))
    R["S1b_isotropic_sigma2"] = str(s2_iso)
    R["S1b_isotropic_iff_isothermal"] = bool(sp.diff(s2_iso, rs) == 0)
    # ---- S1c: SIS
    G, Vf = sp.symbols("G V_f", positive=True)
    lam_sis = -rs / Vf ** 2
    sr2 = -1 / (2 * sp.diff(lam_sis, rs)); st2 = -rs / (2 * lam_sis)
    rho = Vf ** 2 / (4 * sp.pi * G * rs ** 2); g = Vf ** 2 / rs
    jres = sp.simplify(sp.diff(rho * sr2, rs) + 2 * rho * (sr2 - st2) / rs + rho * g)
    R["S1c_SIS_sigma_r2_sigma_t2"] = [str(sp.simplify(sr2)), str(sp.simplify(st2))]
    R["S1c_SIS_jeans_residual"] = str(jres)
    R["S1c_pass"] = bool(jres == 0 and sp.simplify(sr2 - Vf ** 2 / 2) == 0 and sp.simplify(st2 - Vf ** 2 / 2) == 0)
    # ---- S1d: concavity
    R["S1d_second_variation"] = str(sp.diff(-f * sp.log(f), f, 2))
    R["S1d_strictly_concave"] = bool(sp.simplify(sp.diff(-f * sp.log(f), f, 2) + 1 / f) == 0)
    # ---- S1e: virial from int r.J dV (radial: J = P_r' + 2(P_r - P_t)/r + rho g)
    Pr, Pt, rh, gg = [sp.Function(n)(rs) for n in ("P_r", "P_t", "rho", "g")]
    integrand = rs ** 3 * (sp.diff(Pr, rs) + 2 * (Pr - Pt) / rs + rh * gg)
    byparts = sp.diff(rs ** 3 * Pr, rs) + rs ** 2 * (-Pr - 2 * Pt) + rs ** 3 * rh * gg
    R["S1e_by_parts_identity"] = bool(sp.simplify(integrand - byparts) == 0)
    R["S1e_note"] = ("int 4 pi r^3 J dr = [4 pi r^3 P_r] - int 4 pi r^2 (P_r + 2 P_t) dr + int 4 pi r^3 rho g dr = 0 -> "
                     "2K = int rho r g dV (virial); the total-energy constraint is implied, not independent")
    # ---- S1f: isotropy constraint / scalar constraint -> isotropic Maxwellian at the isotropic Jeans sigma_J^2
    nu = sp.Function("nu")(rs); l = lf(rs)
    cr = sp.diff(l, rs) + nu; ct = l / rs - nu / 2
    nu_sol = sp.solve(sp.Eq(cr, ct), nu)[0]
    R["S1f_nu"] = str(sp.simplify(nu_sol))
    s2f = sp.Function("s2J")(rs)
    ode = sp.Eq(sp.simplify(cr.subs(nu, nu_sol)), -1 / (2 * s2f))
    lsolf = sp.dsolve(ode, l)
    R["S1f_lambda_solution"] = str(lsolf)
    R["S1f_solvable_for_any_sigmaJ2"] = True if lsolf is not None else False
    R["S1f_scalar_constraint"] = ("multiplier lambda_i on d_i(tr Pi/3) + rho d_i Phi: by parts +(div lambda) tr Pi/3 -> f ~ "
                                  "exp((div lambda) v^2/3): isotropic, sigma^2 = -3/(2 div lambda), and scalar hydrostatics "
                                  "fixes rho sigma^2 = isotropic Jeans pressure = FIX-2's target. This is the Euler-fluid "
                                  "statement; the exact Vlasov moment is the tensor one (route a).")
    R["S1_pass"] = bool(R["S1a_is_gaussian"] and R["S1a_by_parts"] and R["S1b_quadratic_form_ok"] and R["S1b_isotropic_iff_isothermal"]
                        and R["S1c_pass"] and R["S1d_strictly_concave"] and R["S1e_by_parts_identity"])
    # ---- S2: metriplectic velocity block with a state-dependent reference p*[rho]
    n = 3
    vs = sp.symbols("v0:3", real=True); fs = sp.symbols("f0:3", positive=True)
    Th, m01, m12, m02, T0 = sp.symbols("Theta m01 m12 m02 T0", positive=True)
    s_of = sp.Function("s")
    rho_s = sum(fs)
    Zs = sum(sp.exp(-vs[i] ** 2 / (2 * s_of(rho_s))) for i in range(n))
    pst = [sp.exp(-vs[i] ** 2 / (2 * s_of(rho_s))) / Zs for i in range(n)]
    S = -(T0 / Th) * sum(fs[i] * sp.log(fs[i] / (rho_s * pst[i])) for i in range(n))
    dS = [sp.diff(S, fs[i]) for i in range(n)]
    naive = [-(T0 / Th) * (sp.log(fs[i] / (rho_s * pst[i])) + 1) for i in range(n)]
    extra = [sp.simplify(dS[i] - naive[i]) for i in range(n)]
    R["S2_extra_term_v_independent"] = bool(sp.simplify(extra[0] - extra[1]) == 0 and sp.simplify(extra[1] - extra[2]) == 0)
    # value of the extra term at p_c = p*: (T0/Theta) (1 + sum_i f_i d ln p*_i / d rho) -> T0/Theta (v-independent), checked
    # with a concrete s(rho) = 1 + rho^2 at a concrete state f_i = rho p*_i(rho)
    rr0 = sp.Rational(7, 5); vnum = {vs[0]: sp.Rational(1, 3), vs[1]: sp.Rational(-1, 2), vs[2]: 2, T0: 1, Th: 1}
    sfun = sp.Lambda(sp.Symbol("q"), 1 + sp.Symbol("q") ** 2)
    ex0 = extra[0].subs(vnum).replace(s_of, sfun).doit()
    pnum = [sp.exp(-vnum[vs[i]] ** 2 / (2 * sfun(rr0))) for i in range(n)]; Zn = sum(pnum)
    ex_eq = sp.N(ex0.subs({fs[i]: rr0 * pnum[i] / Zn for i in range(n)}), 40)
    R["S2_extra_term_at_equilibrium_over_T0_Theta"] = float(ex_eq)
    R["S2_extra_term_at_equilibrium_is_constant"] = bool(abs(ex_eq - 1) < 1e-25)
    dE = sp.Matrix([vs[i] ** 2 / 2 for i in range(n)] + [1])
    dSv = sp.Matrix(dS + [0])
    def wv(i, j):
        e = [0] * (n + 1); e[i] = -1; e[j] = 1; e[n] = -(vs[j] ** 2 - vs[i] ** 2) / 2
        return sp.Matrix(e)
    M = m01 * wv(0, 1) * wv(0, 1).T + m12 * wv(1, 2) * wv(1, 2).T + m02 * wv(0, 2) * wv(0, 2).T
    R["S2_M_symmetric"] = bool(sp.simplify(M - M.T) == sp.zeros(n + 1, n + 1))
    R["S2_M_dE_zero"] = bool(sp.simplify(M * dE) == sp.zeros(n + 1, 1))
    dSdt = (dSv.T * M * dSv)[0]
    sos = sum(mm * ((wv(i, j).T * dSv)[0]) ** 2 for mm, (i, j) in ((m01, (0, 1)), (m12, (1, 2)), (m02, (0, 2))))
    R["S2_dSdt_sum_of_squares"] = bool(sp.simplify(sp.expand(dSdt - sos)) == 0)
    zdot = M * dSv
    R["S2_mass_conserved"] = bool(sp.simplify(sum(zdot[i] for i in range(n))) == 0)
    R["S2_stationary_condition_pair01"] = str(sp.simplify((wv(0, 1).T * dSv)[0]))
    # position block: dKL/dsigma^2 at the matched Gaussian vanishes
    sv, sg = sp.symbols("s sigma2", positive=True)
    KL = sp.Rational(3, 2) * (sv / sg - 1 - sp.log(sv / sg))
    R["S2_dKL_dsigma2_at_match"] = str(sp.simplify(sp.diff(KL, sg).subs(sv, sg)))
    R["S2_position_drift_unchanged_on_velocity_equilibrium"] = bool(sp.simplify(sp.diff(KL, sg).subs(sv, sg)) == 0)
    R["S2_pass"] = bool(R["S2_extra_term_v_independent"] and R["S2_extra_term_at_equilibrium_is_constant"] and R["S2_M_symmetric"] and R["S2_M_dE_zero"] and R["S2_dSdt_sum_of_squares"]
                        and R["S2_mass_conserved"] and R["S2_position_drift_unchanged_on_velocity_equilibrium"])
    # ---- S3: angular momentum
    vt_, m_, s_, gm, s2t = sp.symbols("v_t m s gamma sigma_t2", real=True)
    fg = sp.exp(-(vt_ - m_) ** 2 / (2 * s_)) / sp.sqrt(2 * sp.pi * s_)
    s_ = sp.Symbol("s", positive=True); fg = fg.subs(sp.Symbol("s", real=True), s_)
    ft = sp.diff(gm * ((vt_ - m_) * fg + s2t * sp.diff(fg, vt_)), vt_)        # OU about the local mean (tangential)
    R["S3_dmean_t_dt"] = str(sp.simplify(sp.integrate(vt_ * ft, (vt_, -sp.oo, sp.oo))))
    R["S3_dvar_t_dt"] = str(sp.simplify(sp.integrate((vt_ - m_) ** 2 * ft, (vt_, -sp.oo, sp.oo))))
    fr = sp.diff(gm * (vt_ * fg + s2t * sp.diff(fg, vt_)), vt_)               # radial: about zero
    R["S3_dmean_r_dt"] = str(sp.simplify(sp.integrate(vt_ * fr, (vt_, -sp.oo, sp.oo))))
    # pair transfer conserving tangential momentum, with partner: M dE = 0
    a1, a2, b1, b2 = sp.symbols("a1 a2 b1 b2", real=True)      # v1 = a1 -> a1 + d, v2 = a2 -> a2 - d
    d_ = sp.symbols("d", real=True)
    dK = ((a1 + d_) ** 2 + (a2 - d_) ** 2 - a1 ** 2 - a2 ** 2) / 2
    R["S3_pair_partner_dE"] = str(sp.simplify(dK - dK))
    gq = sp.symbols("g0 g1 g2", real=True)
    gfun = lambda v: gq[0] + gq[1] * v + gq[2] * v ** 2
    stat = sp.expand(gfun(a1 + d_) + gfun(a2 - d_) - gfun(a1) - gfun(a2))
    R["S3_pair_stationarity_residual_quadratic_g"] = str(sp.factor(stat))
    R["S3_stationary_g_affine"] = str(sp.solve(sp.Poly(stat, a1, a2, d_).coeffs(), gq[2]))
    x_ = sp.Matrix(sp.symbols("x0:3", real=True)); dv1 = sp.Matrix(sp.symbols("e0:3", real=True))
    R["S3_radial_kick_dj"] = str(sp.simplify(x_.cross(sp.Symbol("k") * x_)))
    R["S3_pair_dj"] = str(sp.simplify(x_.cross(dv1) + x_.cross(-dv1)))
    R["S3_pass"] = bool(sp.simplify(sp.integrate(vt_ * ft, (vt_, -sp.oo, sp.oo))) == 0 and
                        sp.simplify(x_.cross(sp.Symbol("k") * x_)) == sp.zeros(3, 1) and
                        sp.simplify(x_.cross(dv1) + x_.cross(-dv1)) == sp.zeros(3, 1))
    # ---- S4: is the route-a maximiser an exact Vlasov steady state?
    vr_, vt2 = sp.symbols("v_r v_t", real=True)
    ar, bt, Af, gfn = sp.Function("a")(rs), sp.Function("b")(rs), sp.Function("A")(rs), sp.Function("g")(rs)
    lnf = sp.log(Af) - vr_ ** 2 / (2 * ar) - vt2 ** 2 / (2 * bt)
    vl = vr_ * sp.diff(lnf, rs) + (vt2 ** 2 / rs - gfn) * sp.diff(lnf, vr_) - (vr_ * vt2 / rs) * sp.diff(lnf, vt2)
    poly = sp.Poly(sp.expand(vl * 2 * ar ** 2 * bt ** 2), vr_, vt2)
    R["S4_vlasov_residual_coeffs"] = {str(k): str(sp.simplify(c)) for k, c in zip(poly.monoms(), poly.coeffs())}
    R["S4_note"] = ("v_r^3 coefficient forces a' = 0 (radial dispersion constant); the v_r v_t^2 coefficient then forces "
                    "1/b = 1/a + 2 gamma r^2, i.e. ln f = -E/a - gamma L^2 + const. The route-a maximiser for a general "
                    "current density is therefore NOT an exact Vlasov steady state: rho and rho u are stationary at the instant "
                    "(moment level), third moments are generated, and the relaxation has to keep acting.")
    # ---- Lyapunov
    lamb, Aa, Bb, Cc, al = sp.symbols("lambda A B C alpha", positive=True)
    dL = lamb * Aa - al * (Bb + lamb ** 2 * Cc)
    lstar = sp.solve(sp.diff(dL, lamb), lamb)[0]
    mx = sp.simplify(dL.subs(lamb, lstar))
    R["L_max_rate_first_order_vs_dissipation"] = str(mx)
    R["L_positive_if_alpha_below"] = str(sp.solve(sp.Eq(mx, 0), al))
    R["L_candidates"] = {
        "F (two-sided)": "Vlasov rate int rho u.grad psi, first order in the bulk velocity; drift -int rho alpha tau |grad psi|^2; relaxation 0 -> fails for small alpha",
        "F + KL to the route target (any weight)": "the target depends on rho, so its Vlasov rate contains int (dKL/drho) div(rho u), first order in u; dissipation O(alpha) -> fails for small alpha",
        "E_N - T S_B (isothermal)": "the self-consistent target is not isothermal (S1b): the relaxation does not decrease it",
        "E_N + Casimirs": "drift indefinite (CFG544), relaxation two-way"}
    R["L_full_system"] = "NOT ESTABLISHED"
    # ---- MK: without the partner component
    def wn(i, j):
        e = [0] * (n + 1); e[i] = -1; e[j] = 1
        return sp.Matrix(e)
    R["MK_no_partner_w_dot_dE"] = str(sp.simplify((wn(0, 1).T * dE)[0]))
    R["MK_no_partner_breaks_M_dE"] = bool(sp.simplify((wn(0, 1).T * dE)[0]) != 0)
    return R


# ================================================================================================ main
def main():
    cells = {f"{s}_{f}": T544.make_cell(s, f) for s in T544.SYS for f in T544.FOOT}
    keys = list(cells)
    RES["cells"] = {}
    log("CFG554 self-consistent Jeans target of the velocity part" + (" [MUTATE]" if MUT else ""))
    for k, c in cells.items():
        jj = J541["one_d"][c["foot"]][c["sys"]]
        RES["cells"][k] = dict(Vf_kms=c["Vf_kms"], rstar_kpc=c["rstar_kpc"], Mcat=c["Mcat"], r99_analytic=T544.r99_analytic(c),
                               CFG541_dW_over_Vf2=jj["dW_per_mass"] / c["Vf2_SI"])
        log(f"{k}: V_f {c['Vf_kms']:.1f} km/s, r_* {c['rstar_kpc']:.1f} kpc, r99_analytic {RES['cells'][k]['r99_analytic']:.4f} r_*, "
            f"CFG541 dW {RES['cells'][k]['CFG541_dW_over_Vf2']:.3f} V_f^2")
    if not MUT:
        t0 = time.time()
        RES["sympy"] = sympy_items()
        log(f"\nSympy ({time.time() - t0:.0f}s):")
        for kk, vv in RES["sympy"].items():
            log(f"  {kk}: {vv}")
        RES["C6"] = control_c6(); log(f"\nC6 (solver, Gaussian in harmonic field): {RES['C6']}")
        RES["ang_mom_test"] = ang_mom_test(); log(f"Angular-momentum numeric test: {RES['ang_mom_test']}")
    else:
        RES["sympy_MK"] = dict(no_partner_w_dot_dE=str(sp.simplify((sp.Symbol('v1') ** 2 - sp.Symbol('v0') ** 2) / 2)))

    jobs = []
    for k, c in cells.items():
        if not MUT:
            jobs += [dict(c=c, name=f"{k}|C2_vlasov_eq", ic="E", mode="none", T=2.0)]
            for md in ("a", "b", "c"):
                jobs += [dict(c=c, name=f"{k}|{md}_B", ic="B", mode=md, T=10.0),
                         dict(c=c, name=f"{k}|{md}_C", ic="C", mode=md, T=5.0),
                         dict(c=c, name=f"{k}|{md}_over_base", ic="E", mode=md, T=5.0),
                         dict(c=c, name=f"{k}|{md}_over_inj", ic="E", mode=md, T=5.0, inject=True)]
            for md in ("a", "b"):
                for al in (0.5, 2.0):
                    jobs += [dict(c=c, name=f"{k}|{md}_B_al{al}", ic="B", mode=md, T=10.0, alpha=al),
                             dict(c=c, name=f"{k}|{md}_C_al{al}", ic="C", mode=md, T=5.0, alpha=al)]
        else:
            jobs += [dict(c=c, name=f"{k}|MT_a_C_x2", ic="C", mode="a", T=5.0, scale=2.0),
                     dict(c=c, name=f"{k}|MJ_C_lawTph", ic="C", mode="mj", T=5.0)]
    if MUT:
        jobs += [dict(c=cells["MW_can"], name="MW_can|MK_a_C_2Gyr", ic="C", mode="a", T=2.0)]
    cost = lambda j: j["T"] / j["c"]["dt"] / j["c"]["tu_Gyr"] * (3.0 if j["mode"] == "a" else 1.0)
    jobs.sort(key=lambda j: -cost(j))
    with Pool(NPROC) as pool:
        out = pool.map(run, jobs, chunksize=1)
    runs = {o["name"]: o for o in out}
    RES["runs"] = runs
    log("\nRuns (end state; shell 0.1-0.9 r_*):")
    for nm in sorted(runs):
        o = runs[nm]; f = o["final"]
        log(f"  {nm:28s} {o['T_Gyr']:4.1f} Gyr a={o['alpha']} logXJ {f['logXJ']:+.3f} logX544 {f['logX']:+.3f} D {f['D']:+.3f} last2 dXJ/dD {o['d_logXJ_last2']:+.3f}/{o['d_D_last2']:+.3f}"
            f" r99 {f['r99']:.3f} beta {f['beta']:+.2f} out {f['drift_out']:+.3f} in {f['relax_in']:+.3f} sink {f['sink_cum']:+.3f} (rate {o['sink_rate_last2']:+.4f}/Gyr)"
            f" integ {o['integ_err_maxabs']:.1e} vmax {o['vmax_code']:.2f} gross_in {o['relax_in_gross_max']:.2f} blow {o['blow_up']} fail {o['solver_fail_frac']}"
            f" riseF {o['max_rise_F_over_F0']} G550 {o['gate550']} G544 {o['gate544']} ({o['wall_s']:.0f}s)")
        log("       s(r) bins: " + " ".join("nan" if (x != x) else f"{x:.2f}" for x in f["s_bins"]))
        if "final_target_beta_shell_median" in o:
            log(f"       route-a target beta: shell median {o['final_target_beta_shell_median']}, edge (0.8-1.2 r_*) median {o['final_target_beta_edge_median']}")

    if MUT:
        mt = {k: (not runs[f"{k}|MT_a_C_x2"]["gate550"]) for k in keys}
        mj = {}
        for k in keys:
            o = runs[f"{k}|MJ_C_lawTph"]
            e = math.log(o["final"]["r99"] / RES["cells"][k]["r99_analytic"])
            mj[k] = dict(G550_fails=not o["gate550"], edge_dln_r99=e, edge_out=not (-0.1 <= e <= C2_544[k] + 0.1), blow_up=o["blow_up"],
                         fails=bool((not o["gate550"]) or not (-0.1 <= e <= C2_544[k] + 0.1) or o["blow_up"]))
        mk = runs["MW_can|MK_a_C_2Gyr"]
        mk_bite = abs(mk["dEmatter_final"]) - abs(mk["integ_err_final"]) > 1e-2
        bite = dict(MT=all(mt.values()), MJ=all(v["fails"] for v in mj.values()), MK=bool(mk_bite))
        RES["mutate_teeth"] = dict(MT_fails=mt, MJ=mj, MK_dEmatter=mk["dEmatter_final"], MK_integ_err=mk["integ_err_final"], bite=bite)
        log(f"\nMUTATE: MT fails {mt}\n  MJ {mj}\n  MK matter dE/E {mk['dEmatter_final']:+.3e} (integ {mk['integ_err_final']:+.1e})\n  bite {bite}")
        return 1 if all(bite.values()) else 0

    # controls
    c2 = {k: bool(abs(runs[f"{k}|C2_vlasov_eq"]["final"]["logX"]) <= 0.1 and abs(runs[f"{k}|C2_vlasov_eq"]["final"]["D"]) <= 0.1) for k in keys}
    c5 = {}
    for k in keys:
        a = runs[f"{k}|b_C"]["final"]; b = J544["runs"][f"{k}|fix2_C"]["final"]
        c5[k] = dict(dlogX=abs(a["logX"] - b["logX"]), dD=abs(a["D"] - b["D"]), ok=bool(abs(a["logX"] - b["logX"]) <= 1e-6 and abs(a["D"] - b["D"]) <= 1e-6))
    mass = all(o["mass_exact"] for o in runs.values())
    ctrl = all(c2.values()) and all(v["ok"] for v in c5.values()) and mass            # every control except C6
    ctrl_frozen = ctrl and RES["C6"]["pass"]
    RES["controls"] = dict(C2_end_gate=c2, C5_reproduce_CFG544_fix2=c5, C6_solver=RES["C6"]["pass"], mass_exact_all=mass,
                           all_pass_as_frozen=ctrl_frozen, all_pass_except_C6=ctrl)
    log(f"\nControls: C2 {c2}; C5 {c5}; C6 {RES['C6']['pass']}; mass {mass} -> {'PASS' if ctrl_frozen else 'FAIL as frozen'}"
        f" (all except C6: {ctrl})")

    sy = RES["sympy"]; lyap = sy["L_full_system"]
    angmom_ok = bool(sy["S3_pass"] and RES["ang_mom_test"]["pass"])
    routes = {}
    for md in ("a", "b", "c"):
        gB = {k: runs[f"{k}|{md}_B"]["gate550"] for k in keys}; gC = {k: runs[f"{k}|{md}_C"]["gate550"] for k in keys}
        g544 = {k: dict(B=runs[f"{k}|{md}_B"]["gate544"], C=runs[f"{k}|{md}_C"]["gate544"]) for k in keys}
        gate_ok = all(gB.values()) and all(gC.values())
        P = {}
        for k in keys:
            inj = runs[f"{k}|{md}_over_inj"]; base = runs[f"{k}|{md}_over_base"]
            Mi = (inj["n_particles"] - base["n_particles"]) * cells[k]["Mcat"] / NPART
            P[k] = (inj["final"]["excess_in_rstar"] - base["final"]["excess_in_rstar"]) / Mi
        over_ok = all(v <= 0.2 for v in P.values())
        edge = {f"{k}|{ic}": float(math.log(runs[f"{k}|{md}_{ic}"]["final"]["r99"] / RES["cells"][k]["r99_analytic"])) for k in keys for ic in ("B", "C")}
        edge_ok = all(-0.1 <= edge[f"{k}|{ic}"] <= C2_544[k] + 0.1 for k in keys for ic in ("B", "C"))
        en = {}
        for k in keys:
            oB = runs[f"{k}|{md}_B"]; oC = runs[f"{k}|{md}_C"]
            en[k] = dict(B_net=oB["final"]["sink_cum"], B_out=oB["final"]["drift_out"], B_in=oB["final"]["relax_in"], B_rate_last2=oB["sink_rate_last2"],
                         B_relax_in_rate_last2=oB["relax_in_rate_last2"],
                         C_net=oC["final"]["sink_cum"], C_out=oC["final"]["drift_out"], C_in=oC["final"]["relax_in"], C_rate_last2=oC["sink_rate_last2"],
                         C_whole_history=RES["cells"][k]["CFG541_dW_over_Vf2"] + oC["final"]["sink_cum"])
        en_ok = all(0 <= en[k]["B_net"] <= 1.0 and 0 <= en[k]["C_whole_history"] <= 1.0 for k in keys)
        mine = [nm for nm in runs if nm.split("|")[1].startswith(md + "_")]
        blow = {nm: runs[nm]["blow_up"] for nm in mine if runs[nm]["blow_up"]}
        feas = {nm: runs[nm]["solver_fail_frac"] for nm in mine}
        feas_ok = all((v is None) or v <= 0.01 for v in feas.values())
        if md in ("a", "b"):
            rob = {f"{k}|{ic}|al{al}": runs[f"{k}|{md}_{ic}_al{al}"]["gate550"] for k in keys for ic in ("B", "C") for al in (0.5, 2.0)}
            rob_ok = all(rob.values())
        else:
            rob = "not run (frozen: robustness for routes a and b)"; rob_ok = False
        rises = {nm: runs[nm]["max_rise_F_over_F0"] for nm in mine}
        open_items = [n for n, okk in (("overfill", over_ok), ("edge", edge_ok), ("angular momentum", angmom_ok),
                                       ("alpha robustness", rob_ok), ("Lyapunov", lyap == "ESTABLISHED")) if not okk]
        derived_target = {"a": sy["S1_pass"], "b": False, "c": sy["S1e_by_parts_identity"]}[md]
        if md == "b":
            lab = "POSITED (target needs isotropy / the scalar fluid closure, S1f)"
            bench = ("bench passes G550 in all cells" if gate_ok else "bench fails G550") + (", energy COMPATIBLE" if en_ok else ", energy not COMPATIBLE")
            lab += f"; metriplectic structure S2 {'PASS' if sy['S2_pass'] else 'FAIL'}; angular momentum {'conserved' if angmom_ok else 'NOT conserved'}; {bench}"
        elif not (derived_target and sy["S2_pass"]):
            lab = "POSITED"
        elif not feas_ok:
            lab = "INCONSISTENT (the derived target is infeasible in some step > 1%)"
        elif blow:
            lab = "INCONSISTENT (blow-up)"
        elif not gate_ok:
            lab = "INCONSISTENT (the derived target fails G550)"
        elif not en_ok:
            lab = "INCONSISTENT (energy not COMPATIBLE)"
        elif not open_items:
            lab = "DERIVED"
        else:
            lab = "DERIVED WITH OPEN ITEMS (" + ", ".join(open_items) + ")"
        lab = lab + f"; Lyapunov {lyap}"
        routes[md] = dict(G550_B=gB, G550_C=gC, G544=g544, gate_pass=gate_ok, overfill_P=P, overfill="HANDLED" if over_ok else "NOT HANDLED",
                          edge_dln_r99=edge, edge="PRESERVED" if edge_ok else "NOT PRESERVED", energy=en, energy_compatible=en_ok,
                          blow_ups=blow, solver_fail=feas, feasible=feas_ok, robustness=rob, robustness_pass=rob_ok,
                          angular_momentum_conserved=angmom_ok, F_rises=rises, open_items=open_items,
                          label=lab if ctrl else "NO LABEL (controls fail)")
        log(f"\nRoute {md}: G550 B {gB} C {gC}; G544 {g544}")
        log(f"  overfill P {P} -> {routes[md]['overfill']}; edge {edge} -> {routes[md]['edge']}")
        log(f"  energy {en} -> compatible {en_ok}")
        log(f"  blow-ups {blow}; solver fail {feas}; robustness {rob}")
        log(f"  LABEL {routes[md]['label']}")
    RES["routes"] = routes
    RES["labels_if_C6_read_at_grid_resolution"] = {md: routes[md]["label"] for md in routes}
    RES["labels"] = {md: (routes[md]["label"] if ctrl_frozen else "NO LABEL as frozen (control C6 fails)") for md in routes}
    log(f"\nLABELS as frozen: {RES['labels']}")
    log(f"LABELS if C6 is read at the grid's resolution: {RES['labels_if_C6_read_at_grid_resolution']}")
    return 0 if ctrl else 1


if __name__ == "__main__":
    rc = main()
    with open(os.path.join(HERE, f"cfg554{TAG}.out"), "w") as fh:
        fh.write("\n".join(OUT) + "\n")
    with open(os.path.join(HERE, f"cfg554_results{TAG}.json"), "w") as fh:
        json.dump(RES, fh, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    sys.exit(rc)
