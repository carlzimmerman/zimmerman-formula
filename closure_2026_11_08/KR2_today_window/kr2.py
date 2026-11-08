#!/usr/bin/env python3
"""KR2 (FROZEN_CRITERIA.md, 92c1ced823): the present-day mu_K window for the action's K(Q) dust at the CMB's amount.
    python3 kr2.py battery  -> parts/battery.json   C2 X-COP, C3 groups, C6 hosts; KA3, KA5, KA6a, KA7 (clusters, groups);
                                                    M1 (X-COP cusp, C2 at R), M2 (C2 at f 0), M3 (planted core)
    python3 kr2.py sparc    -> parts/sparc.json     C1; KA2, KA7 (SPARC); M1 (C1 at mu_B)
    python3 kr2.py kids     -> parts/kids.json      C5; KA4, KA6b/c; M1 (C5 at mu_B)
    python3 kr2.py lens     -> parts/lens.json      C7 static + C7-run; KA8
    python3 kr2_grade.py    -> kr2.json / kr2.out, kr2_MUTATE.json / kr2_MUTATE.out
Dust: QX7 iter_5's n = 1 host-hydrostatic `profile` (via KQ1's prefix, which runs NA2's, which runs iter_5's prelude), a
vectorised copy checked against it (KA7); C5 uses KX1's own sector solver (QX10 iter_2 solve_static). Reading B (label):
no extra inside r_J = 1/mu_K, solver mass beyond. Reading A (reported): uncapped. Amount R (F1A) label; f_cap R reported.
Cold dark energy, never dark matter; no particle. One thread. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, time, signal, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL6 = os.path.join(REPO, "closure_2026_11_06"); CL7 = os.path.join(REPO, "closure_2026_11_07"); CL8 = os.path.join(REPO, "closure_2026_11_08")
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
FOOTS = ("canonical", "alt")
WHICH = sys.argv[1] if len(sys.argv) > 1 else ""
GRID = [0.1 * 10 ** (k / 5) for k in range(15)] + [79.43282347242821]
FCAP = 0.76
F1A = json.load(open(os.path.join(CL7, "F1A_primary_cmb_audit", "f1a.json")))
RF = {f: float(F1A[f]["R_B2"]) for f in FOOTS}
KDJ = json.load(open(os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.json")))
UF = {f: KDJ["footings"][f]["uniform_f_diag"] for f in FOOTS}
FX = {f: UF[f]["Xcop_f_need"] for f in FOOTS}; CAPF = {f: UF[f]["capture_f"] for f in FOOTS}; SPCAP = {f: UF[f]["SPARC_f_max"] for f in FOOTS}
MU_B = {f: KDJ["footings"][f]["B1"]["mu_B"] for f in FOOTS}
AMT = {"R": RF, "fcapR": {f: FCAP * RF[f] for f in FOOTS}}       # label amount R; bracket f_cap R
NC4_HOSTFRAC, NC4_CGEN = 0.0133, {"canonical": 0.0248, "alt": 0.0222}
RES = {}
def P(s=""): print(s, flush=True)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9          # macOS: bytes -> GB
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return None
    return o
def dump(name, obj): json.dump(clean(obj), open(os.path.join(PARTS, name), "w"), indent=1)
def on_term(sig, frm):
    dump(f"{WHICH}_partial.json", RES); P("SIGTERM: partial checkpoint written"); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)
def load_prefix(path, marker, name):
    src = open(path).read(); ns = {"__file__": path, "__name__": name}; a = sys.argv; sys.argv = [path]
    try:
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:src.index(marker)], name, "exec"), ns)
    finally: sys.argv = a
    return ns
def window(mus, ok): return [m for m, o in zip(mus, ok) if o]
def bisect_edge(fun, a, b, n=12):
    """log-bisection between grid neighbours a < b whose statuses differ; returns the edge mu (reported only)."""
    s0 = fun(a); la, lb = math.log(a), math.log(b)
    for _ in range(n):
        m = 0.5 * (la + lb)
        if fun(math.exp(m)) == s0: la = m
        else: lb = m
    return math.exp(0.5 * (la + lb))


# ================================================================== KQ1 prefix -> iter_5 solver, X-COP data, lines
def load_kq1():
    p = os.path.join(CL7, "KQ1_kq_dust_cluster_core", "kq1.py")
    src = open(p).read(); cut = src.index("def cored_shape(rc)")
    ns = {"__file__": p, "__name__": "kq1_prefix"}; a = sys.argv; sys.argv = [p]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): exec(compile(src[:cut], p, "exec"), ns)
    finally: sys.argv = a
    ns["_log"] = buf.getvalue(); return ns


def make_vec(I5):
    """Vectorised copy of QX7 iter_5's `profile` (same algorithm, many hosts at one lambda_0). Returns (rs [m], r [m], M_d [Msun]
    (NSTEP x nh), err mask)."""
    G, MS, KPC, glaw, NSTEP = I5["G"], I5["MS"], I5["KPC"], I5["glaw"], I5["NSTEP"]; MPC = 1e3 * KPC
    def profile_vec(Mb_ofs, Mtots, lam0_mpc, a0):
        Mtots = np.asarray(Mtots, float); nh = len(Mtots)
        mu = 2 * math.pi / (lam0_mpc * MPC); Rc = math.pi / mu
        rmin = min(1e-4 * Rc, 0.1 * KPC); r = np.geomspace(rmin, 1.05 * Rc, NSTEP); cmu = mu ** 2 / (4 * math.pi * G)
        Mb = np.stack([np.asarray(f(r), float) * MS for f in Mb_ofs], axis=1)                    # (NSTEP, nh)
        def run(rc, idx, store=False):
            Mbx = Mb[:, idx]; rho = rc.copy(); M = np.zeros_like(rc); alive = np.ones(len(rc), bool)
            Ms = np.zeros((len(r), len(rc))) if store else None
            rs = np.full(len(rc), np.nan); Mfin = np.full(len(rc), np.nan)
            def deriv(rr, rho_, M_, mb):
                gN = G * (mb + M_) / rr ** 2; gt = glaw(gN, a0)
                return -cmu * gt, 4 * math.pi * rr ** 2 * np.maximum(rho_, 0)
            for i in range(len(r) - 1):
                h = r[i + 1] - r[i]; rm = 0.5 * (r[i] + r[i + 1]); mbm = 0.5 * (Mbx[i] + Mbx[i + 1])
                k1 = deriv(r[i], rho, M, Mbx[i]); k2 = deriv(rm, rho + h / 2 * k1[0], M + h / 2 * k1[1], mbm)
                k3 = deriv(rm, rho + h / 2 * k2[0], M + h / 2 * k2[1], mbm); k4 = deriv(r[i + 1], rho + h * k3[0], M + h * k3[1], Mbx[i + 1])
                rn = rho + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); Mn = M + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
                cross = alive & (rn <= 0)
                if cross.any():
                    t = rho[cross] / (rho[cross] - rn[cross]); rs[cross] = r[i] + t * h; Mfin[cross] = M[cross] + t * (Mn[cross] - M[cross])
                    alive &= ~cross
                rho = np.where(alive, rn, 0.0); M = np.where(alive, Mn, M)
                if store: Ms[i + 1] = M
                if not alive.any(): break
            if store: Ms[i + 1:] = M
            return rs, Mfin, Ms
        target = Mtots * MS; riso = math.pi * target / (4 * Rc ** 3)
        lo, hi = np.log(riso * 1e-8), np.log(riso * 1e4); err = np.zeros(nh, bool)
        pend = np.ones(nh, bool)
        for _ in range(40):
            idx = np.where(pend)[0]
            if not len(idx): break
            _, Mhi, _ = run(np.exp(hi[idx]), idx); ok = np.isfinite(Mhi) & (Mhi > target[idx])
            pend[idx[ok]] = False; hi[idx[~ok]] += math.log(1e3)
        err |= pend
        pend = np.ones(nh, bool)
        for _ in range(40):
            idx = np.where(pend)[0]
            if not len(idx): break
            _, Mlo, _ = run(np.exp(lo[idx]), idx); ok = np.isfinite(Mlo) & (Mlo < target[idx])
            pend[idx[ok]] = False; lo[idx[~ok]] -= math.log(1e3)
        err |= pend
        act = ~err; Mjm1 = np.full(nh, np.nan); Mj = np.full(nh, np.nan)
        for _ in range(5):
            idx = np.where(act)[0]
            if not len(idx): break
            lrc = np.linspace(lo[idx], hi[idx], 24, axis=1)                                      # (m, 24)
            hid = np.repeat(idx, 24); _, Mf, _ = run(np.exp(lrc.ravel()), hid); Mf = Mf.reshape(len(idx), 24)
            bad = np.isnan(Mf).any(axis=1)
            for k, h_ in enumerate(idx):
                if bad[k]: err[h_] = True; act[h_] = False; continue
                j = int(np.searchsorted(Mf[k], target[h_]))
                if j == 0 or j == 24: err[h_] = True; act[h_] = False; continue
                lo[h_], hi[h_] = lrc[k, j - 1], lrc[k, j]; Mjm1[h_], Mj[h_] = Mf[k, j - 1], Mf[k, j]
                if abs(Mf[k, j] / target[h_] - 1) < 1e-6: act[h_] = False
        ok = ~err; idx = np.where(ok)[0]
        rs_all = np.full(nh, np.nan); Mout = np.zeros((len(r), nh))
        if len(idx):
            t = (np.log(target[idx]) - np.log(Mjm1[idx])) / (np.log(Mj[idx]) - np.log(Mjm1[idx]))
            rs, Mf, Ms = run(np.exp(lo[idx] + t * (hi[idx] - lo[idx])), idx, store=True)
            rs_all[idx] = rs; Mout[:, idx] = Ms / MS * (target[idx] / Mf)[None, :]
        return rs_all, r, Mout, err
    return profile_vec


class DustSet:
    """Dust M_d(<r) for many hosts at one mu and footing: retention (iter_5: r_s < r_ta0(M_b,tot)) and readings A / B."""
    def __init__(self, r, M, rs, Mtot, keep, mu, KPC):
        self.r, self.M, self.rs, self.Mtot, self.keep, self.mu = r, M, rs, np.asarray(Mtot, float), keep, mu
        self.rJ = 1.0 / mu * 1e3 * KPC                                                          # r_J = 1/mu_K, m
    def at(self, h, r_m, reading="B"):
        r_m = np.asarray(r_m, float)
        if not self.keep[h]: return np.zeros_like(r_m)
        Md = np.where(r_m >= self.rs[h], self.Mtot[h], np.interp(r_m, self.r, self.M[:, h]))
        if reading == "B": Md = np.where(r_m < self.rJ, 0.0, Md)
        return Md


# ================================================================== battery: C2, C3, C6
def run_battery():
    K = load_kq1(); P(K["_log"].strip().splitlines()[-1] if K["_log"] else ""); I5 = K["I5"]
    assert K["KA_OK"], "KQ1 prefix KA failed"
    RES["KQ1_prefix_KA"] = dict(ok=bool(K["KA_OK"]), log=K["_log"].strip().splitlines())
    A0, XC, KPC, MS, G, glaw = (K[k] for k in ("A0", "XC", "KPC", "MS", "G", "glaw"))
    XINFO, XN, XPROF, r_ta0, profile, xeval_md, solve = K["XINFO"], K["XN"], K["XPROF"], K["r_ta0"], K["profile"], K["xeval_md"], K["solve"]
    r_half, max_slope_in = K["r_half"], K["max_slope_in"]; L1_LO, L1_HI, L2_MAX, L3P = K["L1_LO"], K["L1_HI"], K["L2_MAX"], K["L3P"]
    MPC = 1e3 * KPC; pvec = make_vec(I5); GB = K["GB"]
    UA1J = json.load(open(os.path.join(CL7, "UA1_fragile_rows", "ua1.json")))
    CI = {f: UA1J["footings"][f]["cells"]["groups"]["post"]["ci95"] for f in FOOTS}
    # groups: GB1 points per footing and f*, host M_sys from rrM (GB1's group total), as HY1
    GRP = {}
    for f in FOOTS:
        a0h = GB["A0"][f]; GRP[f] = {}
        for fst in (0, 1):
            gl = GB["groups_pts"](a0h, float(fst)); rows = []
            for g in gl:
                ft0 = g["pts"][0]["feat"]; Ms_ = (ft0["r"] / ft0["rrM"]) ** 2 * a0h / G / MS
                rows.append(dict(name=g["name"], Msys=Ms_, r=np.array([p["feat"]["r"] for p in g["pts"]]), x=np.array([p["feat"]["x"] for p in g["pts"]]),
                                 D=np.array([p["D"] for p in g["pts"]]), sl=np.array([p["sl"] for p in g["pts"]])))
            GRP[f][fst] = rows
    def point(M): return lambda r: np.full_like(np.asarray(r, float), M)
    R500 = {n: XINFO[n]["r500"] for n in XN}
    # ---- KA7 (clusters, groups): vectorised solver == profile
    ka7 = []
    for f in FOOTS:
        for mu in (1.0, 19.054607179632473):
            ns_ = XN[:2]; Mt = [RF[f] * XINFO[n]["Mlast"] for n in ns_]
            rsv, rv, Mv, er = pvec([XPROF[n][0] for n in ns_], Mt, 2 * math.pi / mu, A0[f])
            for k, n in enumerate(ns_):
                rs0, r0, M0 = profile(XPROF[n][0], Mt[k], 2 * math.pi / mu, A0[f])
                rr = np.array([z["r_kpc"] for z in XC if z["name"] == n]) * KPC
                a_ = np.where(rr >= rs0, Mt[k], np.interp(rr, r0, M0)); b_ = np.where(rr >= rsv[k], Mt[k], np.interp(rr, rv, Mv[:, k]))
                ka7.append(dict(f=f, mu=mu, host=n, rel=float(np.max(np.abs(b_ / a_ - 1))), rs_rel=float(abs(rsv[k] / rs0 - 1))))
            gs = GRP[f][0][:2]; Mt = [RF[f] * g["Msys"] for g in gs]
            rsv, rv, Mv, er = pvec([point(g["Msys"]) for g in gs], Mt, 2 * math.pi / mu, GB["A0"][f])
            for k, g in enumerate(gs):
                rs0, r0, M0 = profile(point(g["Msys"]), Mt[k], 2 * math.pi / mu, GB["A0"][f])
                a_ = np.where(g["r"] >= rs0, Mt[k], np.interp(g["r"], r0, M0)); b_ = np.where(g["r"] >= rsv[k], Mt[k], np.interp(g["r"], rv, Mv[:, k]))
                ka7.append(dict(f=f, mu=mu, host="group " + g["name"], rel=float(np.max(np.abs(b_ / np.maximum(a_, 1e-300) - 1))), rs_rel=float(abs(rsv[k] / rs0 - 1))))
    k7 = max(max(x["rel"], x["rs_rel"]) for x in ka7)
    RES["KA7_battery"] = dict(rows=ka7, max_rel=k7, pass_=bool(k7 <= 1e-5))
    P(f"KA7 vectorised solver vs iter_5 profile (2 X-COP + 2 groups x 2 mu x 2 footings): max rel {k7:.2e} -> {'PASS' if k7 <= 1e-5 else 'FAIL'}  [{time.time()-T0:.0f}s {rss():.2f}GB]")

    # ---- cluster dust per (f, mu, amount)
    def xdust(f, mu, amt_f):
        Mt = [amt_f * XINFO[n]["Mlast"] for n in XN]
        rs, r, M, er = pvec([XPROF[n][0] for n in XN], Mt, 2 * math.pi / mu, A0[f])
        keep = np.array([(not er[k]) and rs[k] / MPC < r_ta0(XPROF[n][1]) for k, n in enumerate(XN)])
        return DustSet(r, M, rs, Mt, keep, mu, KPC), er
    def c2c6(f, mu, amt_f, reading, D=None):
        if D is None: D, er = xdust(f, mu, amt_f)
        md = {n: (lambda r_m, k=k: D.at(k, np.atleast_1d(r_m), reading)) for k, n in enumerate(XN)} if amt_f > 0 else None
        xe = xeval_md(f, md); per = {}
        for k, n in enumerate(XN):
            r5 = R500[n] * KPC; Mq = D.at(k, np.array([0.25 * r5, 0.7 * r5]), reading) if amt_f > 0 else np.zeros(2)
            conc = float(Mq[0] / Mq[1]) if Mq[1] > 0 else float("nan")
            Mb5 = float(XPROF[n][0](np.array([r5]))[0]); q5 = float(D.at(k, np.array([r5]), reading)[0]) / Mb5 if amt_f > 0 else 0.0
            Mta = float(D.at(k, np.array([r_ta0(XPROF[n][1]) * MPC * 0.999999]), reading)[0]) if amt_f > 0 else 0.0
            o = dict(retained=bool(D.keep[k]) if amt_f > 0 else False, r_s_kpc=float(D.rs[k] / KPC) if amt_f > 0 else None, conc=conc, q500=q5,
                     need_present=bool(Mta >= FX[f] * XINFO[n]["Mlast"] * (1 - 1e-9)))
            if reading == "A" and amt_f > 0 and D.keep[k]:
                rl = D.r[2:]; dM = np.gradient(D.M[:, k], D.r); rho = (dM / (4 * math.pi * D.r ** 2))[2:]
                o["r_half_kpc"] = r_half(rl / KPC, rho); o["max_slope_20kpc"] = max_slope_in(rl / KPC, rho, 20.0)
            per[n] = o
        cc = [per[n]["conc"] for n in XN]
        L3 = all(np.isfinite(c) and L3P[0] <= c <= L3P[1] for c in cc); L4 = bool(xe["L4"]); L5 = all(per[n]["need_present"] for n in XN)
        if reading == "B": Lcore = bool(D.rJ / KPC <= L1_HI); L2 = None
        else:
            rh = [per[n].get("r_half_kpc") for n in XN]; sl = [per[n].get("max_slope_20kpc", float("inf")) for n in XN]
            Lcore = all(x is not None and L1_LO <= x <= L1_HI for x in rh); L2 = all(s <= L2_MAX for s in sl)
        c2 = bool(Lcore and L3 and L4 and L5 and (L2 is None or L2))
        q = [per[n]["q500"] for n in XN]; H = NC4_HOSTFRAC * float(np.median(q)) / RF[f]
        c6a = bool(H <= NC4_CGEN[f]); c6b = all(x <= FX[f] for x in q)
        return dict(C2=c2, lines=dict(core=Lcore, L2=L2, L3=bool(L3), L4=L4, L5=bool(L5)), mean=xe["mean"], rms=xe["rms"],
                    bins=[b["mean"] for b in xe["bins"]], max_abs_bin=xe["max_abs_bin"], NA2_gate=xe["NA2_gate"], conc_range=[float(np.nanmin(cc)) if np.isfinite(cc).any() else None, float(np.nanmax(cc)) if np.isfinite(cc).any() else None],
                    r_J_kpc=D.rJ / KPC, per_cluster=per, C6=bool(c6a and c6b), C6_H=H, C6_H_line=NC4_CGEN[f], C6a=c6a, C6b=bool(c6b), q500=q,
                    n_retained=int(sum(per[n]["retained"] for n in XN)))
    def gdust(f, fst, mu, amt_f):
        rows = GRP[f][fst]; Mt = [amt_f * g["Msys"] for g in rows]
        rs, r, M, er = pvec([point(g["Msys"]) for g in rows], Mt, 2 * math.pi / mu, GB["A0"][f])
        keep = np.array([(not er[k]) and rs[k] / MPC < r_ta0(g["Msys"]) for k, g in enumerate(rows)])
        return DustSet(r, M, rs, Mt, keep, mu, KPC), er
    def c3(f, mu, amt_f, reading, Ds=None):
        a0 = GB["A0"][f]; out = {}
        for fst in (0, 1):
            D = Ds[fst] if Ds else (gdust(f, fst, mu, amt_f)[0] if amt_f > 0 else None); dl = []; npass = 0; med = []
            for k, g in enumerate(GRP[f][fst]):
                gN = g["x"] * a0; md = D.at(k, g["r"], reading) if amt_f > 0 else np.zeros_like(g["r"])
                d = np.log10(glaw(gN + G * md * MS / g["r"] ** 2, a0) / glaw(gN, a0)); dl.extend(d.tolist())
                res = g["D"] - d; npass += bool(np.all(np.abs(res) <= 2 * g["sl"])); med.extend(res.tolist())
            out[fst] = dict(step=float(np.mean(dl)), strict_n_pass=int(npass), median_res=float(np.median(med)),
                            n_retained=int(D.keep.sum()) if D is not None else 0)
        ok = all(CI[f][0] <= out[s]["step"] <= CI[f][1] for s in (0, 1))
        return dict(C3=bool(ok), step_fst0=out[0]["step"], step_fst1=out[1]["step"], ci95=CI[f], detail=out)

    # ---- KA3, KA5 (f 0), KA6a (KQ1's closest row via my path), M2
    for f in FOOTS:
        R = RES.setdefault(f, {}); ka = {}
        x0 = c2c6(f, 1.0, 0.0, "B"); ka["KA3"] = dict(mean=x0["mean"], ref=GB["KA20"][f]["X"], d=abs(x0["mean"] - GB["KA20"][f]["X"]))
        ka["KA3"]["pass_"] = bool(ka["KA3"]["d"] <= 1e-6)
        g0 = c3(f, 1.0, 0.0, "B"); ka["KA5"] = dict(step=[g0["step_fst0"], g0["step_fst1"]], pass_=bool(g0["step_fst0"] == 0.0 and g0["step_fst1"] == 0.0))
        KQJ = json.load(open(os.path.join(CL7, "KQ1_kq_dust_cluster_core", "kq1.json")))
        rec = KQJ["footings"][f]["closest"]                                  # KQ1's recorded closest row (mu 19.05)
        D, _ = xdust(f, rec["mu"], FX[f])
        D.keep[:] = True                                                     # KQ1's L4 used the profile whether or not retained (it was, every cell)
        xa = c2c6(f, rec["mu"], FX[f], "A", D)
        recL = rec["lines"]; d6 = max(abs(xa["rms"] - recL["rms"]), abs(xa["bins"][0] - rec["xeval"]["bins"][0]["mean"]))
        ka["KA6a"] = dict(mu=rec["mu"], rms=xa["rms"], rec_rms=recL["rms"], inner=xa["bins"][0], rec_inner=rec["xeval"]["bins"][0]["mean"], d=d6, pass_=bool(d6 <= 1e-3))
        R["KA"] = ka
        for k_, v in ka.items(): P(f"[{f}] {k_}: {'PASS' if v['pass_'] else 'FAIL'}  " + ", ".join(f"{a}={b}" for a, b in v.items() if a != "pass_"))
        R["M2"] = dict(C2_at_f0=x0["C2"], mean=x0["mean"], rms=x0["rms"], L4=x0["lines"]["L4"], bites=bool(ka["KA3"]["pass_"] and not x0["C2"]))
        P(f"[{f}] M2 f 0: X-COP mean {x0['mean']:.6f} rms {x0['rms']:.4f}, C2 {'PASS' if x0['C2'] else 'FAIL'} -> {'BITES' if R['M2']['bites'] else 'NO BITE'}")
    dump("battery_partial.json", RES)
    if not all(RES[f]["KA"][k]["pass_"] for f in FOOTS for k in RES[f]["KA"]) or not RES["KA7_battery"]["pass_"]:
        RES["stopped"] = "KA FAIL"; dump("battery.json", RES); P("KA FAIL: nothing graded"); return

    # ---- M1 (mu_B): KD1 cusp at capture amount (reading A) and C2 at R; M3 planted core
    cored = lambda rc: (lambda rk: (lambda x: x - np.arctan(x))(np.asarray(rk, float) / rc))
    for f in FOOTS:
        R = RES[f]; mu = MU_B[f]
        D, _ = xdust(f, mu, CAPF[f]); xa = c2c6(f, mu, CAPF[f], "A", D)
        rec = KDJ["footings"][f]["static"]["G2 X-COP"]["num"]
        rh = [xa["per_cluster"][n].get("r_half_kpc") for n in XN]
        m1 = dict(mu=mu, mean=xa["mean"], rms=xa["rms"], kd1_mean=rec["mean"], kd1_rms=rec["rms"], max_r_half_kpc=max(x for x in rh if x is not None) if any(x is not None for x in rh) else None)
        m1["cusp_ok"] = bool(abs(xa["mean"] - rec["mean"]) <= 1e-5 and abs(xa["rms"] - rec["rms"]) <= 1e-5)
        m1["L1_fails"] = bool(m1["max_r_half_kpc"] is None or m1["max_r_half_kpc"] < 1.0)
        xr = c2c6(f, mu, RF[f], "B"); m1["C2_at_R_label"] = xr["C2"]; m1["C2_at_R_rms"] = xr["rms"]
        g1 = c3(f, mu, RF[f], "B"); m1["C3_at_R"] = g1["C3"]; m1["C6_at_R"] = xr["C6"]
        m1["bites"] = bool(m1["cusp_ok"] and m1["L1_fails"] and not xr["C2"])
        R["M1"] = m1
        P(f"[{f}] M1 mu {mu:.4e}: X-COP at KD1 capture (A) {xa['mean']:.6f}/{xa['rms']:.6f} vs KD1 {rec['mean']:.6f}/{rec['rms']:.6f}; max r_1/2 {m1['max_r_half_kpc']}; "
          f"C2 at R {'PASS' if xr['C2'] else 'FAIL'} (rms {xr['rms']:.3f}); C3 {'P' if g1['C3'] else 'F'} C6 {'P' if xr['C6'] else 'F'} -> {'BITES' if m1['bites'] else 'NO BITE'}")
        md = {}; per = {}
        for n in XN:
            m = cored(100.0); tl = XINFO[n]["tl"]; t = float(m(np.array([tl]))[0]); Ml = XINFO[n]["Mlast"]; r5 = R500[n]
            md[n] = (lambda r_m, m=m, t=t, tl=tl, Ml=Ml: FX[f] * Ml * np.where(np.asarray(r_m, float) / KPC > tl, 1.0, m(np.asarray(r_m, float) / KPC) / t))
            per[n] = float(m(np.array([0.25 * r5]))[0] / m(np.array([0.7 * r5]))[0])
        xe = xeval_md(f, md); L3 = all(L3P[0] <= c <= L3P[1] for c in per.values())
        R["M3"] = dict(rms=xe["rms"], bins=[b["mean"] for b in xe["bins"]], conc=per, L3=bool(L3), L4=bool(xe["L4"]), holds=bool(L3 and xe["L4"]))
        P(f"[{f}] M3 planted r_c 100 at need: rms {xe['rms']:.4f}, bins {[round(b['mean'],3) for b in xe['bins'] if b['mean'] is not None]}, c {min(per.values()):.4f}-{max(per.values()):.4f} -> {'HOLDS' if R['M3']['holds'] else 'FAILS'}")
    dump("battery_partial.json", RES)

    # ---- the grid
    for f in FOOTS:
        R = RES[f]; rows = []
        for mu in GRID:
            row = dict(mu=mu, r_J_kpc=1e3 / mu)
            for an, amt in AMT.items():
                D, er = xdust(f, mu, amt[f]); Dg = {s: gdust(f, s, mu, amt[f])[0] for s in (0, 1)}
                for rd in ("B", "A"):
                    xc = c2c6(f, mu, amt[f], rd, D); gc = c3(f, mu, amt[f], rd, Dg)
                    row[f"{an}_{rd}"] = dict(C2=xc, C3=gc, solver_errors=int(er.sum()))
            rows.append(row); R["grid"] = rows; dump("battery_partial.json", RES)
            L = row["R_B"]; x = L["C2"]; g = L["C3"]
            P(f"[{f}] mu {mu:8.4g} r_J {1e3/mu:8.1f} kpc | C2 {'P' if x['C2'] else 'F'} rms {x['rms']:.3f} bins {'/'.join('-' if b is None else f'{b:+.2f}' for b in x['bins'][:3])} c {x['conc_range']} "
              f"core {'P' if x['lines']['core'] else 'F'} L5 {'P' if x['lines']['L5'] else 'F'} ret {x['n_retained']}/7 | C3 {'P' if g['C3'] else 'F'} step {g['step_fst0']:+.3f}/{g['step_fst1']:+.3f} | "
              f"C6 {'P' if x['C6'] else 'F'} H {x['C6_H']:.4f} q500max {max(x['q500']):.2f} | A: C2 {'P' if row['R_A']['C2']['C2'] else 'F'} rms {row['R_A']['C2']['rms']:.3f} "
              f"C3 {'P' if row['R_A']['C3']['C3'] else 'F'} C6 {'P' if row['R_A']['C2']['C6'] else 'F'}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
        # edges (reported): C2, C3, C6 under the label reading
        def st(col):
            def fun(mu):
                if col == "C3": return c3(f, mu, RF[f], "B")["C3"]
                x = c2c6(f, mu, RF[f], "B"); return x["C2"] if col == "C2" else x["C6"]
            return fun
        ed = {}
        for col, key in (("C2", lambda r_: r_["R_B"]["C2"]["C2"]), ("C3", lambda r_: r_["R_B"]["C3"]["C3"]), ("C6", lambda r_: r_["R_B"]["C2"]["C6"])):
            s = [key(r_) for r_ in rows]; ed[col] = []
            for a, b, sa, sb in zip(GRID[:-1], GRID[1:], s[:-1], s[1:]):
                if sa != sb: ed[col].append(dict(between=[a, b], from_=sa, edge=bisect_edge(st(col), a, b)))
        R["edges"] = ed; P(f"[{f}] edges (reported): {ed}")
    RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0; dump("battery.json", RES)
    if os.path.exists(os.path.join(PARTS, "battery_partial.json")): os.remove(os.path.join(PARTS, "battery_partial.json"))
    P(f"battery done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")



# ================================================================== C1 SPARC (QX8 per-galaxy rule, as HY1 C1) + per-galaxy cap
def run_sparc():
    K = load_kq1(); I5 = K["I5"]; assert K["KA_OK"]
    pvec = make_vec(I5); profile, r_ta0 = K["profile"], K["r_ta0"]
    Gs, MSs, KPCs = I5["G"], I5["MS"], I5["KPC"]; MPC = 1e3 * KPCs
    sys.path.insert(0, os.path.join(CL6, "QX8_sparc_exact_field"))
    a = sys.argv; sys.argv = [a[0]]
    with contextlib.redirect_stdout(io.StringIO()):
        import qx8 as Q8
    sys.argv = a
    GALS = Q8.load_sparc(); Q8J = json.load(open(os.path.join(CL6, "QX8_sparc_exact_field", "qx8.json")))
    GK = 4.30091e-6; lU, lN = np.log(Q8.UPS), np.log(Q8.NODES)
    TF = {}
    for f in FOOTS:
        TF[f] = []
        for i, q in enumerate(GALS):
            z = np.load(os.path.join(Q8.PARTS, f, f"{i:03d}.npz"), allow_pickle=False); Tn = z["T"]
            TF[f].append(np.array([np.interp(lU, lN, Tn[:, j]) for j in range(Tn.shape[1])]))
    # host baryons at U 0.5 (bulge 0.7): M_b(<r), constant beyond the last point at HY1's M_tot(U 0.5)
    HOST = []
    for q in GALS:
        Rk = q["R"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
        Mr = np.maximum.accumulate(np.clip(VB2 * Rk / GK, 0, None)); m = q["meta"]
        Mtot = max(float(Mr[-1]), 0.5 * m["L36"] * 1e9 + 1.33 * m["MHI"] * 1e9)
        ok = Mr > 0; rk, mk = Rk[ok], Mr[ok]
        if len(rk) < 2: rk, mk = np.array([Rk[-1] * 0.5, Rk[-1]]), np.array([Mtot * 0.125, Mtot])
        lr, lm = np.log(rk), np.log(mk); sl = (lm[1] - lm[0]) / (lr[1] - lr[0]) if lr[1] > lr[0] else 3.0
        def fb(r_m, lr=lr, lm=lm, sl=sl, Rl=Rk[-1], Mt=Mtot):
            x = np.log(np.maximum(np.asarray(r_m, float) / KPCs, 1e-300)); y = np.interp(x, lr, lm)
            y = np.where(x < lr[0], lm[0] + sl * (x - lr[0]), y)
            return np.where(np.asarray(r_m, float) / KPCs > Rl, Mt, np.exp(y))
        HOST.append(dict(fb=fb, Mtot=Mtot, Mlast=float(fb(np.array([Rk[-1] * KPCs]))[0]), Rm=Rk * KPCs, rlast=Rk[-1] * KPCs))
    def ev(f, gd, tmode="T"):
        a0 = Q8.FOOT[f]; out = []
        for q, gdi, T in zip(GALS, gd, TF[f]):
            gN = q["GB"] + gdi[:, None]
            lg = np.log10(np.maximum(glaw_(gN, a0), 1e-300)) + (T if tmode == "T" else 0.0)
            out.append(Q8.fit_one(q, lg))
        st = Q8.pooled(out); st["line"] = Q8.line(st); return st
    def glaw_(gN, a0): return 0.5 * gN + np.sqrt(0.25 * gN * gN + a0 * gN)
    def dset(f, mu, amt):
        Mt = [amt * h["Mtot"] for h in HOST]
        rs, r, M, er = pvec([h["fb"] for h in HOST], Mt, 2 * math.pi / mu, Q8.FOOT[f])
        keep = np.array([(not er[k]) and rs[k] / MPC < r_ta0(h["Mtot"]) for k, h in enumerate(HOST)])
        return DustSet(r, M, rs, Mt, keep, mu, KPCs), er
    def c1(f, D, rd):
        gd = [Gs * D.at(k, h["Rm"], rd) * MSs / h["Rm"] ** 2 for k, h in enumerate(HOST)]
        sT = ev(f, gd, "T"); s0 = ev(f, gd, "0")
        st = ("PASS" if sT["line"] else "FAIL") if sT["line"] == s0["line"] else "NOT EVALUABLE"
        fr = np.array([float(D.at(k, np.array([h["rlast"]]), rd)[0]) / h["Mlast"] for k, h in enumerate(HOST)])
        nbad = int((fr > SPCAP[f]).sum())
        ok = bool(st == "PASS" and nbad == 0)
        return dict(C1=ok, rule=st, rms=sT["rms"], U_median=sT["U_median"], rms_T0=s0["rms"], n_over_cap=nbad, max_frac_rlast=float(fr.max()),
                    n_retained=int(D.keep.sum()), n_dust_inside_rlast=int((fr > 0).sum()))
    # KA2 (f 0) and KA7 (SPARC)
    for f in FOOTS:
        R = RES.setdefault(f, {})
        k0 = ev(f, [np.zeros(len(h["Rm"])) for h in HOST]); ref = Q8J["footings"][f]; rx = ref.get("exact", ref.get("st_ex", {}))
        d = abs(k0["rms"] - rx["rms"]); du = abs(k0["U_median"] - rx["U_median"])
        R["KA2"] = dict(rms=k0["rms"], U=k0["U_median"], ref_rms=rx["rms"], ref_U=rx["U_median"], d=d, dU=du, pass_=bool(d <= 1e-6 and du <= 1e-6))
        P(f"[{f}] KA2 SPARC law only: rms {k0['rms']:.8f} U {k0['U_median']:.2f} vs QX8 {rx['rms']:.8f} @ {rx['U_median']:.2f} -> {'PASS' if R['KA2']['pass_'] else 'FAIL'}")
        rows7 = []
        for mu in (1.0, 19.054607179632473):
            sel = [0, 40, 80, 120, 170]; Mt = [RF[f] * HOST[k]["Mtot"] for k in sel]
            rsv, rv, Mv, er = pvec([HOST[k]["fb"] for k in sel], Mt, 2 * math.pi / mu, Q8.FOOT[f])
            for j, k in enumerate(sel):
                rs0, r0, M0 = profile(HOST[k]["fb"], Mt[j], 2 * math.pi / mu, Q8.FOOT[f]); rr = HOST[k]["Rm"]
                a_ = np.where(rr >= rs0, Mt[j], np.interp(rr, r0, M0)); b_ = np.where(rr >= rsv[j], Mt[j], np.interp(rr, rv, Mv[:, j]))
                rows7.append(dict(mu=mu, gal=GALS[k]["name"], rel=float(np.max(np.abs(b_ / np.maximum(a_, 1e-300) - 1) * (a_ > 0))), rs_rel=float(abs(rsv[j] / rs0 - 1))))
        m7 = max(max(x["rel"], x["rs_rel"]) for x in rows7)
        R["KA7"] = dict(rows=rows7, max_rel=m7, pass_=bool(m7 <= 1e-5))
        P(f"[{f}] KA7 SPARC vectorised vs profile (5 galaxies x 2 mu): max rel {m7:.2e} -> {'PASS' if R['KA7']['pass_'] else 'FAIL'}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
    dump("sparc_partial.json", RES)
    if not all(RES[f][k]["pass_"] for f in FOOTS for k in ("KA2", "KA7")):
        RES["stopped"] = "KA FAIL"; dump("sparc.json", RES); P("KA FAIL"); return
    for f in FOOTS:
        D, er = dset(f, MU_B[f], RF[f]); m1 = c1(f, D, "B"); m1["solver_errors"] = int(er.sum()); m1["bites"] = bool(not m1["C1"])
        RES[f]["M1"] = m1; P(f"[{f}] M1 mu_B {MU_B[f]:.4e} at R: C1 {'PASS' if m1['C1'] else 'FAIL'} (rule {m1['rule']} rms {m1['rms']:.4f} U {m1['U_median']:.2f}; over cap {m1['n_over_cap']}) -> {'BITES' if m1['bites'] else 'NO BITE'}")
    dump("sparc_partial.json", RES)
    for f in FOOTS:
        rows = []
        for mu in GRID:
            row = dict(mu=mu, r_J_kpc=1e3 / mu)
            for an, amt in AMT.items():
                D, er = dset(f, mu, amt[f])
                for rd in ("B", "A"): row[f"{an}_{rd}"] = dict(c1(f, D, rd), solver_errors=int(er.sum()))
            rows.append(row); RES[f]["grid"] = rows; dump("sparc_partial.json", RES)
            L = row["R_B"]; A_ = row["R_A"]
            P(f"[{f}] mu {mu:8.4g} r_J {1e3/mu:8.1f} kpc | C1 {'P' if L['C1'] else 'F'} rule {L['rule']} rms {L['rms']:.4f} U {L['U_median']:.2f} over-cap {L['n_over_cap']} retained {L['n_retained']} dust<r_last {L['n_dust_inside_rlast']} err {L['solver_errors']}"
              f" | A: {'P' if A_['C1'] else 'F'} rms {A_['rms']:.4f} over-cap {A_['n_over_cap']} | fcapR B {'P' if row['fcapR_B']['C1'] else 'F'}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
    RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0; dump("sparc.json", RES)
    if os.path.exists(os.path.join(PARTS, "sparc_partial.json")): os.remove(os.path.join(PARTS, "sparc_partial.json"))
    P(f"sparc done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")


# ================================================================== C5 KiDS (KX1 machinery, its own sector solver)
def run_kids():
    KX = os.path.join(CL7, "KX1_kids_joint_budget", "kx1.py")
    src = open(KX).read(); cut = src.index("# ================================================================ run")
    NS = {"__file__": KX, "__name__": "kx1_lib"}; a = sys.argv; sys.argv = [KX]
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "kx1_lib", "exec"), NS)
    sys.argv = a
    KXJ = json.load(open(os.path.join(CL7, "KX1_kids_joint_budget", "kx1.json")))
    BIN, A0K, ACC, G_SI, MS, KPC_M, hot_ratio, glaw_SI = (NS[k] for k in ("BIN", "A0K", "ACC", "G_SI", "MS", "KPC_M", "hot_ratio", "glaw_SI"))
    solve_static, Mdust_at, pointmass, K_of, r_ta, CELLS, FCQ, RR = (NS[k] for k in ("solve_static", "Mdust_at", "pointmass", "K_of", "r_ta", "CELLS", "FCAP", "RR"))
    orig_model = NS["model"]; SOL = {}
    def sol_of(foot, lm, lam_kpc, amt):
        key = (foot, round(lm, 9), lam_kpc, amt)
        if key not in SOL:
            Mb = 10 ** lm; SOL[key] = solve_static(pointmass(Mb), amt * Mb, K_of(lam_kpc), r_ta(Mb), A0K[foot])
        return SOL[key]
    def model(B, sel, foot, cell, mult, prof, dM):
        """cell None: KX1's law. cell ('KR2', lam_kpc, amt, reading): law + K(Q) dust (amt x M*), reading B zero inside r_J."""
        if cell is None or cell[2] == 0.0: return orig_model(B, sel, foot, None, 0.0, prof, dM)
        _, lam, amt, rd = cell
        s = 10 ** dM; lm = B["lm"] + dM; r = B["r"][sel]; Mb = 10 ** lm
        gN = B["gbar"][sel] * s
        if prof is not None: gN = gN + G_SI * hot_ratio(prof, lm, r) * Mb * MS / (r * KPC_M) ** 2
        so = sol_of(foot, lm, lam, amt); md = np.array([Mdust_at(so, x) for x in r])
        if rd == "B": md = np.where(r < lam / (2 * math.pi), 0.0, md)                             # r_J = 1/mu = lam/(2 pi), kpc
        gN = gN + G_SI * md * MS / (r * KPC_M) ** 2
        return glaw_SI(gN, A0K[foot] * ACC)
    NS["model"] = model; budget = NS["budget"]
    def grade(foot, lam, amt, rd):
        rows = []
        for b, B in enumerate(BIN):
            sel = B["win"]; L = budget(B, b, sel, foot, None, 0.0); H = budget(B, b, sel, foot, ("KR2", lam, amt, rd), 1.0)
            W = L["loga"] - H["loga"]; z = (W - L["loga"]) / H["sigma_tot"]
            so = sol_of(foot, B["lm"], lam, amt) if amt > 0 else None
            rows.append(dict(bin=b + 1, lm=B["lm"], E=L["loga"], sig_law=L["sigma_tot"], W=W, sig_win=H["sigma_tot"], z=z,
                             bound=(None if so is None else so["bound"]), retained_over_Mstar=(None if so is None else so["retained"] / 10 ** B["lm"]),
                             Rs_kpc=(None if so is None else so["Rs"])))
        nk = sum(1 for x in rows if abs(x["z"]) > 2)
        return dict(rows=rows, n_out=nk, C5=bool(nk < 2))
    for f in FOOTS:
        R = RES.setdefault(f, {}); ka = {}
        g0 = grade(f, 1.0, 0.0, "B"); ref = KXJ["grade"][f]["C1"]["rows"]
        d = max(max(abs(x["E"] - r_["E"]), abs(x["sig_law"] - r_["sig_law"])) for x, r_ in zip(g0["rows"], ref)); dW = max(abs(x["W"]) for x in g0["rows"])
        ka["KA4"] = dict(maxd=d, max_W=dW, pass_=bool(d <= 1e-9 and dW == 0.0))
        lamC2 = CELLS["C2"][0] * 1e3; g6 = grade(f, lamC2, FCQ * RR, "A"); ref6 = KXJ["grade"][f]["C2"]["rows"]
        d6 = max(abs(x["W"] - r_["W"]) for x, r_ in zip(g6["rows"], ref6))
        ka["KA6b"] = dict(lam_kpc=lamC2, W=[x["W"] for x in g6["rows"]], ref=[r_["W"] for r_ in ref6], maxd=d6, pass_=bool(d6 <= 1e-9))
        R["KA"] = ka
        for k_, v in ka.items(): P(f"[{f}] {k_}: {'PASS' if v['pass_'] else 'FAIL'}  " + ", ".join(f"{a_}={b_}" for a_, b_ in v.items() if a_ != "pass_"))
    # KA6c: the two solvers, M_d(200 kpc) for a 10^10.7 point host, smallest grid mu where both bind (canonical a0 of each machinery)
    Kq = load_kq1(); prof5, r_ta05, KPC5, MPC5 = Kq["profile"], Kq["r_ta0"], Kq["KPC"], 1e3 * Kq["KPC"]
    Mb = 10 ** 10.7; k6c = None
    for mu in GRID:
        lam = 2 * math.pi / mu * 1e3; so = solve_static(pointmass(Mb), RF["canonical"] * Mb, K_of(lam), r_ta(Mb), A0K["canonical"])
        try: rs5, r5, M5 = prof5(lambda r: np.full_like(np.asarray(r, float), Mb), RF["canonical"] * Mb, 2 * math.pi / mu, Kq["A0"]["canonical"])
        except Exception as e: continue
        b5 = rs5 / MPC5 < r_ta05(Mb)
        if so["bound"] and b5:
            x = 200.0; m10 = Mdust_at(so, x); m5 = float(np.where(x * KPC5 >= rs5, RF["canonical"] * Mb, np.interp(x * KPC5, r5, M5)))
            k6c = dict(mu=mu, Md_qx10=m10, Md_iter5=m5, rel=abs(m10 / m5 - 1), pass_=bool(abs(m10 / m5 - 1) <= 0.02)); break
    if k6c is None: k6c = dict(pass_=False, note="no grid mu where both bind")
    RES["KA6c"] = k6c; P(f"KA6c solvers M_d(200 kpc), 10^10.7 host: {k6c} -> {'PASS' if k6c['pass_'] else 'FAIL'}")
    dump("kids_partial.json", RES)
    if not (all(RES[f]["KA"][k]["pass_"] for f in FOOTS for k in RES[f]["KA"]) and k6c["pass_"]):
        RES["stopped"] = "KA FAIL"; dump("kids.json", RES); P("KA FAIL"); return
    HYK = json.load(open(os.path.join(CL8, "HY1_hybrid_law_plus_component", "parts", "kids.json")))
    for f in FOOTS:
        lam = 2 * math.pi / MU_B[f] * 1e3; m = grade(f, lam, RF[f], "B"); mc = grade(f, lam, FCAP * RF[f], "B")
        hz = HYK[f]["power_KD1_dust_at_half"]["z"]; dz = max(abs(x["z"] - y) for x, y in zip(mc["rows"], hz))
        RES[f]["M1"] = dict(mu=MU_B[f], C5_at_R=m["C5"], z_R=[x["z"] for x in m["rows"]], z_fcapR=[x["z"] for x in mc["rows"]], HY1_point_z=hz, d_vs_HY1=dz, bites=bool(not m["C5"]))
        P(f"[{f}] M1 mu_B: C5 at R {'PASS' if m['C5'] else 'FAIL'} z " + ", ".join(f"{x['z']:+.2f}" for x in m["rows"]) + f"; at f_cap R vs HY1 point mass |dz| {dz:.1e} -> {'BITES' if not m['C5'] else 'NO BITE'}")
    dump("kids_partial.json", RES)
    for f in FOOTS:
        rows = []
        for mu in GRID:
            lam = 2 * math.pi / mu * 1e3; row = dict(mu=mu, r_J_kpc=1e3 / mu)
            for an, amt in AMT.items():
                for rd in ("B", "A"): row[f"{an}_{rd}"] = grade(f, lam, amt[f], rd)
            rows.append(row); RES[f]["grid"] = rows; dump("kids_partial.json", RES)
            L = row["R_B"]
            P(f"[{f}] mu {mu:8.4g} | C5 {'P' if L['C5'] else 'F'} z " + ", ".join(f"{x['z']:+.2f}" for x in L["rows"]) + " | W " + ", ".join(f"{x['W']:+.3f}" for x in L["rows"])
              + " | bound " + "".join("b" if x["bound"] else "-" for x in L["rows"]) + f" | A {'P' if row['R_A']['C5'] else 'F'} fcapR-B {'P' if row['fcapR_B']['C5'] else 'F'}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
        s = [r_["R_B"]["C5"] for r_ in rows]; ed = []
        for a_, b_, sa, sb in zip(GRID[:-1], GRID[1:], s[:-1], s[1:]):
            if sa != sb: ed.append(dict(between=[a_, b_], from_=sa, edge=bisect_edge(lambda m_: grade(f, 2 * math.pi / m_ * 1e3, RF[f], "B")["C5"], a_, b_)))
        RES[f]["edges"] = ed; P(f"[{f}] C5 edges (reported): {ed}")
    RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0; dump("kids.json", RES)
    if os.path.exists(os.path.join(PARTS, "kids_partial.json")): os.remove(os.path.join(PARTS, "kids_partial.json"))
    P(f"kids done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")


# ================================================================== C7 CMB lensing (KD1 background, QX3 growth, GL1 n = 4 Limber)
ZRUN = [0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 20.0]
def run_lens():
    Q3 = load_prefix(os.path.join(CL6, "QX3_cmb_growth", "iter2_kq_dust", "iter2.py"), 'if __name__ == "__main__":', "qx3_iter2_lib")
    GL1J = json.load(open(os.path.join(CL7, "GL1_limber_kernel_reread", "gl1.json")))
    Class, LMAX, ZPK = Q3["Class"], Q3["LMAX"], Q3["ZPK"]
    KG = np.logspace(-4, 1, 70); ZG = np.linspace(0.02, ZPK, 120)
    def limber4(M, kgrid, zgrid, Rm):
        """GL1's limber_n at n = 4 (QX3 iter2's limber_ratio with the k^-4 = (chi/(L + 1/2))^4 restored)."""
        chis = M.angular_distance(1089.0) * (1 + 1089.0); chi = np.array([M.angular_distance(z) * (1 + z) for z in zgrid]); lnk = np.log(kgrid)
        Pm = np.array([[M.pk_lin(k, z) for z in zgrid] for k in kgrid])
        w = ((chis - chi) / (chi * chis)) ** 2 * (1 + np.asarray(zgrid)) ** 2 / np.array([M.Hubble(z) for z in zgrid])
        Ls = np.arange(2, LMAX + 1); num = np.zeros(len(Ls)); den = np.zeros(len(Ls))
        for j in range(len(zgrid)):
            kk = (Ls + 0.5) / chi[j]; m = (kk >= kgrid[0]) & (kk <= kgrid[-1])
            Pj = np.interp(np.log(kk[m]), lnk, Pm[:, j]); Rj = np.interp(np.log(kk[m]), lnk, Rm[:, j]); ex = (chi[j] / (Ls[m] + 0.5)) ** 4
            num[m] += w[j] * Pj * Rj ** 2 / chi[j] ** 2 * ex; den[m] += w[j] * Pj / chi[j] ** 2 * ex
        S = np.ones(LMAX + 1); ok = den > 0; S[Ls[ok]] = num[ok] / den[ok]; return S
    def growth_run(M, ob, od, H0, specs, kgrid, zgrid):
        """QX3 iter2's growth_ratio solve() with mu(a): Jeans term (k/(a mu))^2 only for a > a_run = 1/(1 + z_run); spec (mu, z_run),
        mu None = no suppression. Returns {spec: R(k, z)}."""
        h = H0 / 100; Om_b0 = ob / h ** 2; Om_d0 = od / h ** 2
        lna_t = np.linspace(math.log(1 / 3500.0), 0.0, 4000)
        lnH_t = np.array([math.log(M.Hubble(1 / math.exp(x) - 1)) for x in lna_t]); dlnH_t = np.gradient(lnH_t, lna_t); H0c = M.Hubble(0.0)
        ai = 1 / 3401.0; adec = 1 / 1091.0
        lnz = np.log(1 / (1 + np.asarray(zgrid))); kv = np.asarray(kgrid); nk = len(kv)
        def solve(mu, zrun):
            arun = 0.0 if zrun is None else 1 / (1 + zrun)
            grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 6001), lnz]))
            y = np.zeros((nk, 4)); y[:, 0] = ai; y[:, 1] = ai; rec = {}; tset = {float(x): i for i, x in enumerate(lnz)}; I4 = np.eye(4)[None, :, :]
            def Amat(lna):
                a = math.exp(lna); E2 = math.exp(2 * np.interp(lna, lna_t, lnH_t)) / H0c ** 2; dl = float(np.interp(lna, lna_t, dlnH_t))
                Od = Om_d0 * a ** -3 / E2; Ob = Om_b0 * a ** -3 / E2; on = a > adec
                jeans = 0.0 if (mu is None or a <= arun) else (kv / (a * mu)) ** 2
                A = np.zeros((nk, 4, 4)); A[:, 0, 1] = 1; A[:, 1, 0] = 1.5 * Od * (1 - jeans); A[:, 1, 1] = -(2 + dl)
                if on: A[:, 1, 2] = 1.5 * Ob; A[:, 2, 3] = 1; A[:, 3, 0] = 1.5 * Od; A[:, 3, 2] = 1.5 * Ob; A[:, 3, 3] = -(2 + dl)
                return A
            for n in range(len(grid) - 1):
                h_ = grid[n + 1] - grid[n]; A = Amat(0.5 * (grid[n] + grid[n + 1]))
                y = np.linalg.solve(I4 - 0.5 * h_ * A, ((I4 + 0.5 * h_ * A) @ y[:, :, None]))[:, :, 0]
                t = float(grid[n + 1])
                if t in tset: rec[tset[t]] = y.copy()
            out = np.empty((nk, len(zgrid)))
            for jz in range(len(zgrid)):
                yy = rec[jz]; a = 1 / (1 + zgrid[jz]); E2 = math.exp(2 * np.interp(math.log(a), lna_t, lnH_t)) / H0c ** 2
                Od = Om_d0 * a ** -3 / E2; Ob = Om_b0 * a ** -3 / E2; out[:, jz] = (Od * yy[:, 0] + Ob * yy[:, 2]) / (Od + Ob)
            return out
        ref = solve(None, None); return {sp: solve(*sp) / ref for sp in specs}
    for f in FOOTS:
        R = RES.setdefault(f, {}); st = KDJ["footings"][f]["setting"]; M = Class()
        M.set({'output': 'tCl,lCl,mPk', 'l_max_scalars': LMAX + 100, 'h': st["h"], 'omega_b': st["omega_b"], 'omega_cdm': st["omega_d"], 'A_s': Q3["AS0"],
               'n_s': st["n_s"], 'tau_reio': st["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 12.0, 'z_max_pk': ZPK}); M.compute()
        X0 = Q3["X_of"](M); c0, _ = Q3["best_amp_chi2"](X0); H0 = 100 * st["h"]
        def dchi(Rm): S = limber4(M, KG, ZG, Rm); c, _ = Q3["best_amp_chi2"](X0 * S); return float(c - c0), float(S[100]), float(S[400])
        # KA8: constant-mu copy == Q3 growth_ratio; static Delta chi^2 at 0.1 / 79.43 == GL1 L6 converse n4
        ref_g = Q3["growth_ratio"](M, st["omega_b"], st["omega_d"], H0, [0.1, 79.43282347242821], KG, ZG)
        mine = growth_run(M, st["omega_b"], st["omega_d"], H0, [(0.1, None), (79.43282347242821, None), (0.1, 1e9)], KG, ZG)
        dg = max(float(np.max(np.abs(mine[(0.1, None)] - ref_g[0.1]))), float(np.max(np.abs(mine[(79.43282347242821, None)] - ref_g[79.43282347242821]))),
                 float(np.max(np.abs(mine[(0.1, 1e9)] - mine[(0.1, None)]))))
        conv = GL1J["labels"]["L6_KD1"]["footings"][f]["converse"]
        d1 = dchi(mine[(0.1, None)])[0]; d2 = dchi(mine[(79.43282347242821, None)])[0]
        dd = max(abs(d1 - conv["0.1"]["n4"]), abs(d2 - conv["79.4328"]["n4"]))
        R["KA8"] = dict(growth_maxd=dg, dchi2=[d1, d2], ref=[conv["0.1"]["n4"], conv["79.4328"]["n4"]], d=dd, pass_=bool(dg <= 1e-9 and dd <= 1e-3))
        P(f"[{f}] KA8 C7: growth copy vs QX3 max|d| {dg:.1e}; static dchi2 {d1:.4f} / {d2:.4f} vs GL1 {conv['0.1']['n4']:.4f} / {conv['79.4328']['n4']:.4f} -> {'PASS' if R['KA8']['pass_'] else 'FAIL'}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
        dump("lens_partial.json", RES)
        if not R["KA8"]["pass_"]: M.struct_cleanup(); continue
        mb = MU_B[f]; Rb = growth_run(M, st["omega_b"], st["omega_d"], H0, [(mb, None)], KG, ZG)[(mb, None)]
        R["M1"] = dict(mu=mb, dchi2=dchi(Rb)[0]); P(f"[{f}] M1 mu_B: C7 static dchi2 {R['M1']['dchi2']:.4f} (reported)")
        rows = []
        for mu in GRID:
            specs = [(mu, None)] + [(mu, z) for z in ZRUN]; Rs_ = growth_run(M, st["omega_b"], st["omega_d"], H0, specs, KG, ZG)
            ds, s100, s400 = dchi(Rs_[(mu, None)]); run = {z: dchi(Rs_[(mu, z)])[0] for z in ZRUN}
            zmax = None
            for z in ZRUN:
                if run[z] <= 4.0: zmax = z
                else: break
            rows.append(dict(mu=mu, C7_static=bool(ds <= 4.0), dchi2_static=ds, S_L100=s100, S_L400=s400, dchi2_run={str(z): v for z, v in run.items()}, z_run_max=zmax))
            R["grid"] = rows; dump("lens_partial.json", RES)
            P(f"[{f}] mu {mu:8.4g} | C7 static {'P' if ds <= 4 else 'F'} dchi2 {ds:9.2f} | run: " + " ".join(f"{z:g}:{run[z]:.1f}" for z in ZRUN) + f" -> z_run,max {zmax}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
        M.struct_cleanup()
    RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0; dump("lens.json", RES)
    if os.path.exists(os.path.join(PARTS, "lens_partial.json")): os.remove(os.path.join(PARTS, "lens_partial.json"))
    P(f"lens done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")

if __name__ == "__main__":
    P(f"KR2 {WHICH}. Criteria 92c1ced823. R {RF['canonical']:.6f} / {RF['alt']:.6f}; f_cap R {AMT['fcapR']['canonical']:.4f} / {AMT['fcapR']['alt']:.4f}. "
      "kappa = 1/2 FITTED; not theory closed; footings never pooled.")
    {"battery": run_battery, "sparc": run_sparc, "kids": run_kids, "lens": run_lens}[WHICH]()
    P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
