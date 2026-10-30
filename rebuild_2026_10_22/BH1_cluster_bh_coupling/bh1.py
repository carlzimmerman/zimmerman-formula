#!/usr/bin/env python3
"""BH1_cluster_bh_coupling: gravity-only black hole gas motion on CE1's cluster and group cusps (CM1 machinery read-only).
    python3 bh1.py setup; python3 bh1.py run NAME; python3 bh1.py list; python3 bh1.py grade [--partial]"""
import json, math, os, signal, sys, textwrap
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); CM1 = os.path.join(REB, "CM1_outflow_coupling"); sys.path.insert(0, CM1)
import cm1_outflow as C
S0 = json.load(open(os.path.join(CM1, "cm1_setup.json"))); RC = S0["rep"]["canonical"]; tu = S0["tunit_Myr"]; EPS = C.EPS
ETA = {"14": 16.91, "13": 17.67}; ce = json.load(open(os.path.join(REB, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; ETA = {"14": ce["14"]["med"], "13": ce["13"]["med"]}
FG, FS, AS, AG = 0.10, 0.0615, 0.015, 0.2; MSUN, CL, ERG = 1.989e30, 2.998e8, 1e-7; TOT = 10000.0
def mdir(m): d = os.path.join(HERE, f"ics_{m}"); os.makedirs(d, exist_ok=True); return d
def phys(m):
    M = 10.0 ** int(m); R = RC["R200_kpc"] * (M / RC["M200"]) ** (1 / 3); EU = S0["Eunit_erg"] * (M / RC["M200"]) ** (5 / 3); return M, R, EU
def EBH(m): return 0.1 * 0.005 * FS * FG * 10.0 ** int(m) * MSUN * CL ** 2 / ERG
GRID = {f"{g}_N{n}": (g, n, 1.0) for g in ("G1", "G2") for n in (3, 10, 40)}; GRID.update(UNCAP=("G2", 10, None), MUTATE=("G2", 3, 0.01), STATIC=("G2", 10, 0.0))

def setup():
    src = open(os.path.join(CM1, "cm1_outflow.py")).read(); body = src.split("    # cold density")[1].split("    xc = float(np.sort(r)[499])")[0]
    old = 'Mb = S["Mb"]; a = S["a_star"]; Mt = Mc + hern_M(rg, Mb, a)'; assert body.count(old) == 1
    body = body.replace(old, 'Mt = Mc + hern_M(rg, FS * FG, AS) + hern_M(rg, FG, AG)')
    for m, e in ETA.items():
        lo, hi = 1.5, 30.0
        for _ in range(50):
            mid = 0.5 * (lo + hi); v = C.eta_a(C.a_fit_profile(C.M_nfw(mid), 1e-3)); lo, hi = (mid, hi) if v < e else (lo, mid)
        c = 0.5 * (lo + hi); assert 2 < c < 29; S = dict(c=c, eta_c=C.eta_a(C.a_fit_profile(C.M_nfw(c), 1e-3)))
        ns = dict(vars(C)); ns.update(S=S, c=c, HERE=mdir(m), SEED=1, FS=FS, FG=FG, AS=AS, AG=AG); exec(textwrap.dedent("    # cold density" + body), ns)
        r = np.linalg.norm(ns["pos"], axis=1); xc = float(np.sort(r)[499]); S.update(xc500=xc, eta_analytic=C.eta_a(C.a_fit_profile(C.M_nfw(c), xc)), eta_t0=C.eta_p(ns["pos"], xc))
        M, R, EU = phys(m); S.update(M200=M, R200_kpc=R, Eunit_erg=EU, E_BH_erg=EBH(m)); json.dump(S, open(os.path.join(mdir(m), "setup.json"), "w"), indent=1); print(m, S, flush=True)

def lift(Mf, g, S, Mst=FS * FG, Mh=FG, a_s=AS, a_g=AG):
    """energy to move Mf from its radius to 8x, in static stars + other gas + NFW + self, code units"""
    c = S["c"]; mc = math.log1p(c) - c / (1 + c); rs = 1 / c; rg = np.geomspace(1e-6, 3.0, 200001); Pc = -np.log1p(rg / rs) / (mc * rg)
    a0 = a_s if g == "G1" else a_g; st = Mst - (Mf if g == "G1" else 0.0); ho = Mh - (Mf if g == "G2" else 0.0)
    def U(ag):
        d = np.diff(C.hern_M(rg, Mf, ag)); rm = 0.5 * (rg[1:] + rg[:-1])
        return -Mf * Mf / (6 * ag) + float(np.sum(d * (C.hern_P(rm, st, a_s) + C.hern_P(rm, ho, a_g) + np.interp(rm, rg, Pc))))
    return U(8 * a0) - U(a0)

def schedule(g, N, eps, S, EU, Eb, Mst=FS * FG, Mh=FG):
    out = []
    for k in range(N):
        pool = Mst * (1 - k / N) if g == "G1" else Mh
        if eps is None: out.append((pool, pool)); continue
        lim = eps * Eb / N
        if eps == 0 or lift(pool, g, S, Mst, Mh) * EU <= lim: out.append((0.0 if eps == 0 else pool, pool)); continue
        lo, hi = 0.0, pool
        for _ in range(50):
            mid = 0.5 * (lo + hi); lo, hi = (mid, hi) if lift(mid, g, S, Mst, Mh) * EU <= lim else (lo, mid)
        out.append((lo, pool))
    return out

def integrate(pos, vel, mp, xc, g, N, sch, Mst, Mh, a_s, a_g, tot, path, meta):
    per = (tot if meta.get("K1") else TOT) / N / tu if not meta.get("K1") else 250.0 / tu
    up, dn = 5 / tu, 200 / tu; dt = 0.5 / tu; nst = int(round(tot / tu / dt)); mark = int(round(1250 / tu / dt)); a0 = a_s if g == "G1" else a_g
    def state(t):
        k = min(int(t / per + 1e-9), N - 1); ph = t - k * per
        s = (1 - math.cos(math.pi * ph / up)) / 2 if ph < up else (1 + math.cos(math.pi * (ph - up) / dn)) / 2 if ph < up + dn else 0.0
        return sch[k][0], a0 * (1 + 7 * s)
    def parts(Mf): return Mst - (Mf if g == "G1" else 0.0), Mh - (Mf if g == "G2" else 0.0)
    def Pb(r, Mf, ag): st, ho = parts(Mf); return C.hern_P(r, st, a_s) + C.hern_P(r, ho, a_g) + C.hern_P(r, Mf, ag)
    def acc(p, Mf, ag):
        r = np.sqrt(np.einsum("ij,ij->i", p, p)); o = np.argsort(r); rank = np.empty(len(r)); rank[o] = np.arange(len(r)); st, ho = parts(Mf)
        M = mp * rank + C.hern_M(r, st, a_s) + C.hern_M(r, ho, a_g) + C.hern_M(r, Mf, ag); return -p * (M / (r * r + EPS * EPS) ** 1.5)[:, None], r
    def energy(p, v, Mf, ag):
        r = np.sqrt(np.einsum("ij,ij->i", p, p)); q = np.sort(r)
        return 0.5 * mp * float(np.sum(v * v)) - mp * mp * float(np.sum(np.arange(len(q)) / np.sqrt(q * q + EPS * EPS))) + mp * float(np.sum(Pb(r, Mf, ag)))
    stop = {"x": False}; signal.signal(signal.SIGTERM, lambda *_: stop.update(x=True))
    Mf, ag = state(0.0); E0 = energy(pos, vel, Mf, ag); W = 0.0; maxerr = 0.0; A, r = acc(pos, Mf, ag); marks = [dict(t=0, eta=C.eta_p(pos, xc))]
    res = dict(meta, schedule=sch, E0=E0, marks=marks, done=False)
    for i in range(nst):
        t = i * dt; Mm, am = state(t + dt / 2); Mn, an = state(t + dt)
        if (Mm, am) != (Mf, ag): W += mp * float(np.sum(Pb(r, Mm, am) - Pb(r, Mf, ag))); A, r = acc(pos, Mm, am)
        vel += dt / 2 * A; pos += dt * vel; A, r = acc(pos, Mm, am); vel += dt / 2 * A
        if (Mn, an) != (Mm, am): W += mp * float(np.sum(Pb(r, Mn, an) - Pb(r, Mm, am))); A, r = acc(pos, Mn, an)
        Mf, ag = Mn, an; k = i + 1
        if k % mark == 0:
            err = abs(energy(pos, vel, Mf, ag) - E0 - W) / abs(E0); maxerr = max(maxerr, err); marks.append(dict(t=int(round(k * dt * tu)), eta=C.eta_p(pos, xc), err=err, W=W)); res.update(maxerr=maxerr, W=W); json.dump(res, open(path, "w"), indent=1)
        if stop["x"]: sys.exit(3)
    res.update(done=True, maxerr=maxerr, W=W); json.dump(res, open(path, "w"), indent=1)

def run(name):
    if name == "K1":
        # CM1's halo, CM2's K1 schedule (all baryons static except the moved gas, which is CM1's Mg from a_star): G2 with Mst 0 reproduces it
        S = S0; I = np.load(os.path.join(CM1, "cm1_ics.npz")); Ms, Mg, a = S["Mb"] - S["Mg"], S["Mg"], S["a_star"]; sch = [(Mg, Mg)] * 40
        return integrate(I["pos"].copy(), I["vel"].copy(), float(I["mp"]), S["xc500"], "G2", 40, sch, Ms, Mg, a, a, 1250.0, os.path.join(HERE, "bh1_run_K1.json"), dict(K1=True))
    m, cell = name.split("_", 1); g, N, eps = GRID[cell]; d = mdir(m); S = json.load(open(os.path.join(d, "setup.json"))); I = np.load(os.path.join(d, "cm1_ics.npz"))
    sch = schedule(g, N, eps, S, S["Eunit_erg"], S["E_BH_erg"]); use = sum(lift(f, g, S) * S["Eunit_erg"] for f, _ in sch if f > 0)
    integrate(I["pos"].copy(), I["vel"].copy(), float(I["mp"]), S["xc500"], g, N, sch, FS * FG, FG, AS, AG, TOT, os.path.join(HERE, f"bh1_run_{name}.json"), dict(name=name, g=g, N=N, eps=eps, E_used_erg=use, E_BH_erg=S["E_BH_erg"]))

def grade():
    out = []
    def P(s): print(s, flush=True); out.append(s)
    L = lambda n: json.load(open(os.path.join(HERE, f"bh1_run_{n}.json")))
    P("BH1 cluster black hole coupling (see FROZEN_CRITERIA.md); ceiling inputs PROVISIONAL; kappa = 1/2 FITTED; not theory closed; cold dark energy is a gravitating field, never a particle")
    k1r = L("K1"); pr = json.load(open(os.path.join(CM1, "cm1_run_PRIMARY.json")))["marks"][1]["eta"]; k1 = abs(k1r["marks"][1]["eta"] / pr - 1) < 1e-6; P(f"K1 eta at 1250 Myr {k1r['marks'][1]['eta']:.6f} vs CM1/CM2 {pr:.6f}: {'PASS' if k1 else 'FAIL'}")
    k2, k3, k4, k5, done = True, True, True, True, True; RES = {}; best = {}
    for m in ETA:
        S = json.load(open(os.path.join(mdir(m), "setup.json"))); st = L(f"{m}_STATIC"); es = st["marks"][-1]["eta"]; lim = 14.3 / ETA[m]
        d = es / st["marks"][0]["eta"]; k4 &= 0.97 <= d <= 1.03; k5 &= abs(S["eta_t0"] / S["eta_analytic"] - 1) <= 0.05; RES[m] = {}
        P(f"[1e{m}] R200 {S['R200_kpc']:.0f} kpc, c {S['c']:.3f}, x_c {S['xc500']:.4f}, eta t0 {S['eta_t0']:.2f} (analytic {S['eta_analytic']:.2f}), STATIC end {es:.2f} (drift {d:.3f}); E_BH {S['E_BH_erg']:.2e} erg; LIMIT R {lim:.3f}")
        for c, (g, N, e) in GRID.items():
            if c == "STATIC": continue
            q = L(f"{m}_{c}"); R = q["marks"][-1]["eta"] / es; f = [s[0] for s in q["schedule"]]; k2 &= q["maxerr"] < 0.01; done &= q["done"]
            if e is not None: k3 &= q["E_used_erg"] <= e * q["E_BH_erg"] * (1 + 1e-6) and all(a <= b * (1 + 1e-12) for a, b in q["schedule"])
            RES[m][c] = dict(R=R, moved_first=f[0], moved_last=f[-1], E_over_EBH=q["E_used_erg"] / q["E_BH_erg"], err=q["maxerr"])
            P(f"  {c}: R {R:.3f}; moved first/last {f[0]:.5f}/{f[-1]:.5f} M200; E/E_BH {RES[m][c]['E_over_EBH']:.3g}; err {q['maxerr']:.1e}")
        capped = {c: v["R"] for c, v in RES[m].items() if c not in ("UNCAP", "MUTATE")}; bc = min(capped, key=capped.get); best[m] = dict(cell=bc, R=capped[bc], limit=lim, uncapped=RES[m]["UNCAP"]["R"])
        P(f"  best capped {bc} R {capped[bc]:.3f}; UNCAP R {RES[m]['UNCAP']['R']:.3f}")
    mut = {}
    for m in ETA:
        a, b = RES[m]["G2_N3"]["R"], RES[m]["MUTATE"]["R"]; mut[m] = "NOT INFORMATIVE" if abs(1 - a) < 0.03 else ("PASS" if abs(1 - b) < abs(1 - a) else "FAIL"); P(f"MUTATE 1e{m}: eps 0.01 R {b:.3f} vs eps 1 R {a:.3f}: {mut[m]}")
    P(f"K2 work balance: {'PASS' if k2 else 'FAIL'}; K3 caps: {'PASS' if k3 else 'FAIL'}; K4 static drift: {'PASS' if k4 else 'FAIL'}; K5 t0 eta: {'PASS' if k5 else 'FAIL'}; all done: {done}")
    ok = k1 and k2 and k3 and k4 and k5 and done and "FAIL" not in mut.values()
    if not ok: v = "NOT DECIDED"
    elif all(best[m]["R"] <= 0.685 for m in ETA): v = "REACHES CLEAN AT CEILING"
    elif all(best[m]["R"] <= best[m]["limit"] for m in ETA): v = "REACHES LIMIT AT CEILING"
    else:
        ul = all(best[m]["uncapped"] <= best[m]["limit"] for m in ETA); v = "NOT REACHED AT CEILING (" + ("energy-limited: UNCAPPED reaches" if ul else "channel-limited: UNCAPPED does not reach") + ")"
    P(f"VERDICT: {v}")
    open(os.path.join(HERE, "bh1.out"), "w").write("\n".join(out) + "\n"); json.dump(dict(R=RES, best=best, verdict=v, K1=k1, K2=k2, K3=k3, K4=k4, K5=k5, mutate=mut), open(os.path.join(HERE, "bh1_results.json"), "w"), indent=1)

if __name__ == "__main__":
    a = sys.argv[1]
    if a == "setup": setup()
    elif a == "run": run(sys.argv[2])
    elif a == "list": print("\n".join(["K1"] + [f"{m}_{c}" for m in ETA for c in GRID]))
    else: grade()
