#!/usr/bin/env python3
"""UX4_dwarf_failures: what fraction of the law's Local Group and IC 1613 misses can each known systematic carry?
Criteria FROZEN_CRITERIA.md (3ae0afdee2, committed alone). Baseline: LW1's E1, by LW1's own path. Solves cached and resumable.
--mutate: M_star x 10 before E; K1, K2, K6 must fail, exit 1, separate outputs.
kappa = 1/2 FITTED; footings never pooled; cold sector stays retired; not theory closed.
Run: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I ux4.py"""
import csv, json, math, os, sys, importlib.util, signal
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"; sys.dont_write_bytecode = True
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from scipy.special import i0, i1, k0, k1
from scipy.stats import norm
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
sys.path.insert(0, os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar")); import d10_solver as S
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; MFAC = 10.0 if MUT else 1.0; OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
G5, MS5, PC5 = 6.67430e-11, 1.98847e30, 3.0856775814913673e16; GZ, MSZ, PCZ = 6.67430e-11, 1.989e30, 3.0856775814913673e16; KPC = 1e3 * PCZ
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); FEET = ("canonical", "alt"); CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field"); FAIL3 = CLS[:3]
A_H = 3.0 * KPC; GE2 = 2.0592e-10; MHOST = {"MW": 6.0e10, "M31": 1.0e11, "field": 6.0e10}; R12 = 4.0 / 3.0; GYR = 3.15576e16; RSUN = 6.957e8; DAY = 86400.0
FLOOR = 0.01
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-300))
def g_host(R, Mb, a0): gN = GZ * Mb * MSZ / (R + A_H) ** 2; return 0.5 * gN * (1 + np.sqrt(1 + 4 * a0 / gN))
GR = S.Grid2D(nper=24, Nt=16); CF = os.path.join(HERE, f"cache_solves{TAG}.json"); CACHE = json.load(open(CF)) if os.path.exists(CF) else {}; FIELDS = {}; NS = [0]
def save_cache(*_):
    json.dump(CACHE, open(CF + ".tmp", "w")); os.replace(CF + ".tmp", CF)
    if _: sys.exit(143)
signal.signal(signal.SIGTERM, save_cache)
def solve(y, xe):
    iso = xe <= 0; sv = S.Solver2D(GR, y, 0.0 if iso else xe, 0.0, isolated=iso); sv.solve(tol=1e-10); return sv.field_monopole()
def W(y, xe):
    """Wolf sigma^2 in units a0 * r_h (a = 1): LW1's wo."""
    k = f"{y!r}|{xe!r}"
    if k not in CACHE:
        rf, gr = solve(y, xe); CACHE[k] = S.jeans(rf, gr, [])[2]; NS[0] += 1
        if NS[0] % 50 == 0: save_cache()
    return CACHE[k]
def proj_W(rf, gr, beta, Rap):
    """luminosity-weighted projected sigma^2 inside Rap, constant beta, Plummer tracer, a = 1. Rap None = all."""
    lr = np.log(rf); r = np.geomspace(rf[0], rf[-1], 5000); g = np.interp(np.log(r), lr, gr); rho = (3 / (4 * np.pi)) * (1 + r * r) ** -2.5
    f = rho * g * r ** (2 * beta); seg = 0.5 * (f[1:] + f[:-1]) * np.diff(r); I = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]); Pr = I * r ** (-2 * beta)
    Rs = np.geomspace(1e-3, 300.0 if Rap is None else Rap, 220); t = np.concatenate([[0.0], np.geomspace(1e-4, r[-1], 1500)]); num = []
    for R in Rs:
        rr = np.sqrt(R * R + t * t); Pv = np.interp(rr, r, Pr, right=0.0); num.append(np.trapezoid((1 - beta * R * R / (rr * rr)) * Pv, t) * 2.0 if hasattr(np, "trapezoid") else np.trapz((1 - beta * R * R / (rr * rr)) * Pv, t) * 2.0)
    num = np.array(num); Sig = (1 / np.pi) * (1 + Rs * Rs) ** -2; tz = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
    return float(tz(num * Rs * Rs, np.log(Rs)) / tz(Sig * Rs * Rs, np.log(Rs)))
def estimators(y, xe):
    rf, gr = solve(y, xe); _, vir, wo = S.jeans(rf, gr, []); gi = lambda x: float(np.interp(np.log(x), np.log(rf), gr)); o = dict(wo=wo, R1_virial=vir, R3_Walker=gi(1.0) / 2.5, R3_Errani=gi(1.8) * 1.8 / 3.5, K5_b0=proj_W(rf, gr, 0.0, None))
    for b, nm in ((0.5, "bp"), (-0.5, "bm"), (0.0, "b0")):
        for ap, an in ((1.0, "Rh"), (2.0, "2Rh")): o[f"R2_{nm}_{an}"] = proj_W(rf, gr, b, ap)
    return o
# data
def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception: return None
ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arrf = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}; arr7 = {r["lvd_name"]: float(r["sig_f07"]) / float(r["sig_f0"]) for r in ARR}; medf, med7 = float(np.median(list(arrf.values()))), float(np.median(list(arr7.values())))
def bfac(name, mv, seven=False):
    t, m = (arr7, med7) if seven else (arrf, medf); return t.get(name, m if (mv is not None and mv > -7.7) else 1.0)
X1 = list(csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv"))))
LVD = {}
for fn in ("mw", "m31", "local_field"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f"lvd_dwarf_{fn}.csv"))): r["_h"] = {"mw": "MW", "m31": "M31", "local_field": "field"}[fn]; LVD[r["name"]] = r
GEHM = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "geha_vs_lvd_match.csv"))))
NCOL = [c for c in GEHM[0] if c.startswith("geha") and c.lower().endswith(("n_stars", "n", "nstar"))]; GEHN = {}; GEHS = {}
for r in GEHM:
    if NCOL and fl(r.get(NCOL[0])): GEHN[r["lvd_name"]] = fl(r[NCOL[0]])
    if r.get("geha_sigma_resolved") == "1" and fl(r.get("geha_sigma")): GEHS[r["lvd_name"]] = fl(r["geha_sigma"])
Z2 = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(RB, "Z2_satellite_systematics", "z2_per_system.csv")))}
LW = json.load(open(os.path.join(RB, "LW1_law_scorecard", "lw1_dwarfs.json")))
def row(f, name, host, cls, logms, mv, rh_pc, sig, s, dh, ul=False):
    a0 = A0[f]; b = bfac(name, mv); sc = sig * b; Mb = 10 ** logms * MFAC; r12 = 4 / 3 * rh_pc * PC5; gobs = 3 * (sc * 1e3) ** 2 / r12; gN = G5 * (Mb / 2) * MS5 / r12 ** 2
    y = GZ * Mb * MSZ / ((rh_pc * PCZ) ** 2 * a0); xe = float(g_host(dh * KPC, MHOST[host if host in MHOST else "field"], a0) / a0) if dh else 0.0
    return dict(name=name, host=host, cls=cls, mv=mv, rh=rh_pc, sig=sig, b=b, s=s, y=y, xe=xe, dh=dh, EN=math.log10(gobs / gN), plain=math.log10(gobs / (float(nu(gN / a0)) * gN)), ul=ul)
def rows(f):
    o = []
    for r in X1:
        if r["footing"] != f or r["cls"] not in CLS: continue
        o.append(row(f, r["name"], r["host"], r["cls"], float(r["logMstar"]), fl(r["M_V"]), float(r["rh_pc"]), float(r["sigma"]), float(r["sdMC[Newton]"]), fl(r["d_host_kpc"])))
    for x in o:
        x["W0"] = W(x["y"], x["xe"]); x["E1"] = x["EN"] - math.log10(6 * x["W0"] * R12 / x["y"]); x["E0"] = x["EN"] - math.log10(6 * W(x["y"], 0.0) * R12 / x["y"])
        l = LVD[x["name"]]; em, ep = fl(l.get("vlos_sigma_em")) or 0.1 * x["sig"], fl(l.get("vlos_sigma_ep")) or 0.1 * x["sig"]; x["N"] = max(4.0, min(4000.0, GEHN.get(x["name"], 0.5 * (x["sig"] / (0.5 * (em + ep))) ** 2)))
        x["N_src"] = "Geha" if x["name"] in GEHN else "proxy"; x["ell"] = fl(l.get("ellipticity")); x["sph"] = fl(l.get("rhalf_sph_physical")) is not None
        z = Z2.get((f, x["name"])); x["z"] = z
        x["s2b"] = (x["sig"] * x["b"]) ** 2
    return o
def boot(E, s, rng, n=10000):
    N = len(E); ix = rng.integers(0, N, (n, N)); return float(np.median(E)), float(np.std(np.median(E[ix] + s[ix] * rng.standard_normal((n, N)), axis=1)))
def grade(R, E, classes=CLS):
    rng = np.random.default_rng(20261026); o = {}
    for c in classes:
        i = [k for k, x in enumerate(R) if x["cls"] == c]
        if len(i) < 2: o[c] = dict(N=len(i), median=float(E[i[0]]) if i else None, sd=None, Z=None); continue
        m, sd = boot(np.array([E[k] for k in i]), np.array([R[k]["s"] for k in i]), rng); o[c] = dict(N=len(i), median=m, sd=sd, Z=m / sd if sd else None)
    return o
def label(base, var):
    if var["median"] is None or base["median"] is None: return dict(share=None, label="NOT COMPUTABLE")
    sh = (base["median"] - var["median"]) / base["median"]
    if sh >= 1 or (var["Z"] is not None and abs(var["Z"]) < 2): l = "CARRIES"
    elif sh >= 0.25: l = "PARTIAL"
    elif sh <= -0.25: l = "WORSENS"
    else: l = "MINOR"
    return dict(share=float(sh), label=l)
def line(name, G, B, classes=CLS):
    P(f"  {name:42s}: " + "; ".join((f"{c} {G[c]['median']:+.3f} (Z {G[c]['Z']:+.2f}, N {G[c]['N']}) share {label(B[c], G[c])['share']:+.2f} {label(B[c], G[c])['label']}" if G[c]["Z"] is not None else f"{c} N {G[c]['N']} too few") for c in classes))
def Evar(R, s2=None, W_=None, rhf=None):
    """E1 + log(sigma^2/sigma0^2) - log(W/W0) - log(rh/rh0); sigma^2 floored at FLOOR of the raw value."""
    E = np.array([x["E1"] for x in R])
    if s2 is not None: E = E + np.log10(np.maximum(s2, FLOOR * np.array([x["sig"] ** 2 for x in R])) / np.array([x["s2b"] for x in R]))
    if W_ is not None: E = E - np.log10(np.array(W_) / np.array([x["W0"] for x in R]))
    if rhf is not None: E = E - np.log10(rhf)
    return E
# binary population
def kepler_E(M, e):
    E = M + e * np.sin(M)
    for _ in range(40): E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E
def pool(rstar, n, seed, fixed=None):
    rng = np.random.default_rng(seed); m1 = 0.8; Ps, qs, es = [], [], []; tot = 0
    while tot < n:
        P_ = 10 ** rng.normal(5.03, 2.28, 2 * n); q = rng.uniform(0.1, 1, 2 * n); e = rng.uniform(0, 0.9, 2 * n)
        a = (GZ * m1 * (1 + q) * MSZ * (P_ * DAY / (2 * np.pi)) ** 2) ** (1 / 3); ok = a * (1 - e) > 2 * rstar * RSUN
        Ps.append(P_[ok]); qs.append(q[ok]); es.append(e[ok]); tot += int(ok.sum())
    P_, q, e = np.concatenate(Ps)[:n], np.concatenate(qs)[:n], np.concatenate(es)[:n]; return vbin(P_, q, e, rng)
def vbin(P_, q, e, rng, si=None):
    m1 = 0.8; n = len(P_); sini = np.sqrt(1 - rng.uniform(0, 1, n) ** 2) if si is None else si; om = rng.uniform(0, 2 * np.pi, n); M = rng.uniform(0, 2 * np.pi, n); Ee = kepler_E(M, e); f_ = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(Ee / 2), np.sqrt(1 - e) * np.cos(Ee / 2))
    K = (2 * np.pi * GZ * MSZ / (P_ * DAY)) ** (1 / 3) * q * m1 * sini / (m1 * (1 + q)) ** (2 / 3) / np.sqrt(1 - e * e) / 1e3
    return K * (np.cos(om + f_) + e * np.cos(om))
def mock(R, E_law_sq, f, vp, seed, nm=400, err=2.2):
    """returns per-system array of mock sigma^2 (nm x systems); ML with one error = max(var - err^2, 0); no clipping."""
    rng = np.random.default_rng(seed); out = np.zeros((nm, len(R)))
    for j, x in enumerate(R):
        N = int(x["N"]); v = math.sqrt(E_law_sq[j]) * rng.standard_normal((nm, N)) + err * rng.standard_normal((nm, N))
        if f > 0: v = v + (rng.uniform(0, 1, (nm, N)) < f) * vp[rng.integers(0, len(vp), (nm, N))]
        out[:, j] = np.maximum(np.var(v, axis=1, ddof=1) - err * err, 0.0)
    return out
def trunc_ratio(p):
    z = norm.ppf(1 - p / 2); return 1 - 2 * z * norm.pdf(z) / (1 - p)
def km_median(E, cens):
    """left-censored median by flipping to right-censored Kaplan-Meier."""
    t = -np.array(E); o = np.argsort(t, kind="mergesort"); t, c = t[o], np.array(cens)[o]; Sv = 1.0; n = len(t)
    for i in range(n):
        if not c[i]:
            Sv *= 1 - 1 / (n - i)
            if Sv <= 0.5: return float(-t[i])
    return float(-t[-1])
def ols(y, X, n=5000, seed=20261102):
    y = np.array(y); X = np.column_stack([np.ones(len(y))] + list(X)); b = np.linalg.lstsq(X, y, rcond=None)[0]; rng = np.random.default_rng(seed); B = []
    for _ in range(n):
        ix = rng.integers(0, len(y), len(y))
        try: B.append(np.linalg.lstsq(X[ix], y[ix], rcond=None)[0])
        except Exception: pass
    return b.tolist(), np.std(np.array(B), axis=0).tolist()
# Walker per-star
def walker():
    wf = os.path.join(HERE, "cache_walker.json")
    if os.path.exists(wf): return json.load(open(wf))
    sp = importlib.util.spec_from_file_location("rw", os.path.join(REPO, "campaign_fresh_gravity", "CFG51_walker_multiepoch", "reduce_walker.py")); rw = importlib.util.module_from_spec(sp); sp.loader.exec_module(rw)
    lv = rw.load_lvd(); rw_rows = []
    for fn in ("hectocat.dat.gz", "m2fshi.dat.gz", "m2fsmed.dat.gz"): rw_rows += rw.parse(rw.IN + fn)
    st = rw.build_stars(rw_rows); out = {}
    for n in sorted(set(s["target"] for s in st.values())):
        x = lv.get(n.lower())
        if x is None or not (rw.fnum(x["M_V"]) > -7.7): continue
        mem, nvr, vc, _ = rw.membership({k: s for k, s in st.items() if s["target"] == n}, x)
        if len(mem) < 8: continue
        v = np.array([s["vm"] for s in mem]); e = np.array([s["em"] for s in mem]); rec = dict(name=x["name"], n=len(mem), n_vreject=nvr); ord_ = np.argsort(-np.abs(v - np.median(v)), kind="mergesort")
        for k in (0, 1, 2):
            keep = np.sort(ord_[k:]); r = rw.mle_sigma(v[keep], e[keep]); rec[f"sig{k}"] = r["sig"]; rec[f"ul{k}"] = r["ul95"]
        out[n] = rec
    json.dump(out, open(wf, "w"), indent=0); return out
WK = walker()
WT = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG51_walker_multiepoch", "walker_reduced_dispersions.tsv")), delimiter="\t")}
RES = dict(mutate=MUT, footings={}); CHK = {}
P(f"UX4_dwarf_failures{' MUTATE M_star x 10' if MUT else ''}; criteria 3ae0afdee2; kappa = 1/2 FITTED; not theory closed")
vc = pool(10.0, 2000000, 1); vC = pool(1.0, 2000000, 2)
P(f"binary pool, rms km/s, central {np.std(vc):.2f}, ceiling {np.std(vC):.2f}; |v| median {np.median(np.abs(vc)):.3f}, {np.median(np.abs(vC)):.3f}; 99th {np.percentile(np.abs(vc), 99):.1f}, {np.percentile(np.abs(vC), 99):.1f}")
# K3, K4
_rng = np.random.default_rng(5); _t = mock([dict(N=1000)], [9.0], 0.0, vc, 6, nm=200); CHK["K3"] = abs(math.sqrt(float(np.mean(_t))) / 3 - 1) < 0.03
_P = np.full(1000000, 365.25); _v = vbin(_P, np.full(1000000, 1.0), np.zeros(1000000), _rng, si=np.ones(1000000)); _Ka = (2 * np.pi * GZ * MSZ / (365.25 * DAY)) ** (1 / 3) * 0.8 / 1.6 ** (2 / 3) / 1e3; CHK["K4"] = abs(np.std(_v) / (_Ka / math.sqrt(2)) - 1) < 0.03
P(f"K3 mock f=0 returns input: {CHK['K3']}; K4 Kepler rms {np.std(_v):.3f} vs analytic {_Ka / math.sqrt(2):.3f}: {CHK['K4']}")
K1d, K2d, K5d = [], [], []
for f in FEET:
    a0 = A0[f]; R = rows(f); P(f"\n===== {f} a0 {a0} N {len(R)}; N source Geha {sum(x['N_src'] == 'Geha' for x in R)}, proxy {sum(x['N_src'] == 'proxy' for x in R)}; rhalf not circularised: {[x['name'] for x in R if not x['sph']]}")
    F = RES["footings"][f] = dict(); V = F["variants"] = {}
    E1 = np.array([x["E1"] for x in R]); B = grade(R, E1); G0 = grade(R, np.array([x["E0"] for x in R])); Pl = grade(R, np.array([x["plain"] for x in R])); F["base_E1"] = B; F["E0"] = G0
    lw = LW["footings"][f]["per_system"]; K1d += [abs(x["E1"] - lw[x["name"]]["E1"]) for x in R] + [abs(x["plain"] - lw[x["name"]]["plain"]) for x in R] + [abs(B[c]["Z"] - LW["footings"][f]["rows"]["E1"][c]["Z"]) for c in CLS]
    line("BASE E1", B, B); line("E0 isolated", G0, B); line("plain", Pl, B); P("  share of E1 from the EFE term: " + ", ".join(f"{c} {(B[c]['median'] - G0[c]['median']) / B[c]['median']:+.2f}" for c in FAIL3))
    def add(key, E, base=None, rr=None, name=None):
        rr = R if rr is None else rr; g = grade(rr, np.asarray(E)); bb = base or B; V[key] = {c: {**g[c], **label(bb[c], g[c])} for c in CLS}; line(name or key, g, bb)
    def paired(key, sel, E):
        """class medians over a subset, against E1 on the same subset."""
        idx = [i for i, x in enumerate(R) if sel(x)]
        if not idx: P(f"  {key}: no systems"); V[key] = None; return
        rr = [R[i] for i in idx]; add(key, np.asarray(E)[idx], grade(rr, E1[idx]), rr, name=key + " (against E1 on same systems)")
    # B
    s2raw = np.array([x["sig"] ** 2 for x in R])
    add("B0_no_correction", Evar(R, s2raw)); Eb1 = Evar(R, s2raw); Bb1 = grade(R, Eb1)
    add("B1_f07", Evar(R, np.array([(x["sig"] * bfac(x["name"], x["mv"], True)) ** 2 for x in R])))
    slaw2 = np.array([x["s2b"] * 10 ** (-x["E1"]) for x in R]); dbin = {}
    for tag, ff, vp, sd in (("central", 0.5, vc, 11), ("ceiling", 1.0, vC, 12)):
        M = mock(R, slaw2, ff, vp, sd); Em = np.log10(np.maximum(M, 0.01 * slaw2) / slaw2); ms = {}; dbin[tag] = np.maximum(np.median(M, axis=0) - slaw2, 0.0)
        for c in CLS:
            i = [k for k, x in enumerate(R) if x["cls"] == c]; mm = np.median(Em[:, i], axis=1); d = Bb1[c]["median"]; ms[c] = dict(mock_median=float(np.median(mm)), mock_p84=float(np.percentile(mm, 84)), mock_p99=float(np.percentile(mm, 99)), data_b1=d, P_ge=float(np.mean(mm >= d)), share_of_b1=float(np.median(mm) / d) if d else None, sigma_law_med=float(np.median(np.sqrt(slaw2[i]))), sigma_mock_med=float(np.median(np.sqrt(np.median(M, axis=0)[i]))), sigma_raw_med=float(np.median(np.sqrt(s2raw[i]))), Nmed=float(np.median([R[k]["N"] for k in i])))
        F[f"B2_mock_{tag}"] = ms; P(f"  B2 mock {tag} f {ff}: " + "; ".join(f"{c}: law sigma {ms[c]['sigma_law_med']:.2f}, mock {ms[c]['sigma_mock_med']:.2f}, data raw {ms[c]['sigma_raw_med']:.2f}; E mock {ms[c]['mock_median']:+.3f} [p99 {ms[c]['mock_p99']:+.3f}] vs data {ms[c]['data_b1']:+.3f}, P(mock>=data) {ms[c]['P_ge']:.3f}" for c in CLS))
        add(f"B2_{tag}_subtracted", Evar(R, s2raw - dbin[tag]), name=f"B2 {tag}: excess subtracted from raw sigma^2")
    Ew = E1.copy(); sw = np.zeros(len(R), bool)
    for i, x in enumerate(R):
        t = WT.get(x["name"].replace(" ", "_").replace(" II", "_2").replace(" I", "_1"));
        for k, w in WT.items():
            pass
    WNAME = {r["name"]: k for k, r in WK.items()}
    for i, x in enumerate(R):
        k = WNAME.get(x["name"])
        if k and k in WT and fl(WT[k]["sigma_clean"]) is not None:
            sc = fl(WT[k]["sigma_clean"]); sc = sc if sc > 0 else fl(WT[k]["ul95_clean"]); Ew[i] = Eb1[i] + 2 * math.log10(sc / x["sig"]); sw[i] = True
    paired("B3_Walker_clean", lambda x: x["name"] in WNAME and WNAME[x["name"]] in WT and fl(WT[WNAME[x["name"]]]["sigma_clean"]) is not None, Ew)
    add_geha = np.array([min(x["sig"], GEHS.get(x["name"], x["sig"])) for x in R]); paired("B4_Geha_lower", lambda x: x["name"] in GEHS, Evar(R, np.array([(s * x["b"]) ** 2 for s, x in zip(add_geha, R)])))
    F["B3_systems"] = {x["name"]: dict(raw=x["sig"], clean=fl(WT[WNAME[x["name"]]]["sigma_clean"]), single=fl(WT[WNAME[x["name"]]]["sigma_single"]), allmean=fl(WT[WNAME[x["name"]]]["sigma_allmean"])) for x in R if x["name"] in WNAME and WNAME[x["name"]] in WT}
    # T
    q = lambda x: fl(x["z"]["q_MOND"]) if x["z"] else None; hasq = lambda x: q(x) is not None
    def subset(key, sel):
        idx = [i for i, x in enumerate(R) if sel(x)]; rr = [R[i] for i in idx]; add(key, E1[idx], B, rr, name=key + " (subset against the full class)")
    subset("T1_q<0.5", lambda x: hasq(x) and q(x) < 0.5); subset("T1_ell<0.5", lambda x: x["ell"] is not None and x["ell"] < 0.5); subset("T1_all_clean", lambda x: hasq(x) and q(x) < 0.5 and x["ell"] is not None and x["ell"] < 0.5 and x["N"] >= 10 and x["z"]["grad_flag"] != "True")
    idx = [i for i, x in enumerate(R) if hasq(x) and q(x) >= 1]; id2 = [i for i, x in enumerate(R) if hasq(x) and q(x) < 0.5]; F["T2"] = dict(exposed_N=len(idx), exposed=float(np.median(E1[idx])) if idx else None, safe_N=len(id2), safe=float(np.median(E1[id2])) if id2 else None)
    ii = [i for i, x in enumerate(R) if x["z"] and fl(x["z"]["logT_peri"]) is not None and x["mv"] is not None]; b_, sd_ = ols(E1[ii], [np.array([fl(R[i]["z"]["logT_peri"]) for i in ii]), np.array([R[i]["mv"] for i in ii])]); F["T2"].update(slope_logT=b_[1], sd=sd_[1], N=len(ii)); P(f"  T2 exposed q>=1 median {F['T2']['exposed']} (N {len(idx)}), safe {F['T2']['safe']} (N {len(id2)}); E1 on logT_peri at fixed M_V {b_[1]:+.3f} +- {sd_[1]:.3f} (N {len(ii)})")
    dT = {}
    for tag, fp, vf in (("central", 3.0, math.sqrt(2)), ("ceiling", 5.0, 1.0)):
        d = np.zeros(len(R))
        for i, x in enumerate(R):
            if x["host"] not in ("MW", "M31") or not x["dh"]: continue
            MH = MHOST[x["host"]]; z = x["z"]; rp = fl(z["r_peri_kpc"]) if z and z.get("pm") == "True" else None; ra = fl(z["r_apo_kpc"]) if rp else None
            p = (rp if rp else x["dh"] / fp) * KPC; rm = (0.5 * (rp + ra) if rp and ra else x["dh"]) * KPC; Vc = math.sqrt(float(g_host(p, MH, a0)) * p); Tor = 2 * np.pi * rm / math.sqrt(float(g_host(rm, MH, a0)) * rm); Gam = abs(float(g_host(p * 1.001, MH, a0)) - float(g_host(p * 0.999, MH, a0))) / (0.002 * p); tau = p / (vf * Vc); Np = 10 * GYR / Tor
            d[i] = (Gam * (4 / 3 * x["rh"] * PCZ) * tau) ** 2 / 3 * Np / 1e6
        dT[tag] = d; s2 = np.array([x["s2b"] for x in R]) - d; fl_n = int(np.sum(s2 < FLOOR * s2raw)); F[f"T3_{tag}_floored"] = fl_n; F[f"T3_{tag}_dsig2_med"] = {c: float(np.median([d[i] for i, x in enumerate(R) if x["cls"] == c])) for c in CLS}
        add(f"T3_{tag}", Evar(R, s2), name=f"T3 heating {tag} (floored {fl_n}; med dsig2 " + ",".join(f"{F[f'T3_{tag}_dsig2_med'][c]:.3g}" for c in FAIL3) + ")")
    # M
    for k in (1, 2):
        Em_ = E1.copy()
        for i, x in enumerate(R):
            w = next((r for r in WK.values() if r["name"] == x["name"]), None)
            if w and w["sig0"] > 0: s = w[f"sig{k}"] if w[f"sig{k}"] > 0 else w[f"ul{k}"]; Em_[i] = E1[i] + 2 * math.log10(s / w["sig0"])
        paired(f"M1_drop{k}", lambda x: any(r["name"] == x["name"] and r["sig0"] > 0 for r in WK.values()), Em_)
    for tag, p_ in (("5pc", 0.05), ("20pc", 0.20)):
        add(f"M2_{tag}", E1 + math.log10(trunc_ratio(p_)), name=f"M2 remove extreme {tag} (sigma ratio {math.sqrt(trunc_ratio(p_)):.3f})")
    req = {}
    for c in FAIL3:
        m = B[c]["median"]; t = 10 ** (-m)
        try: req[c] = float(brentq(lambda p_: trunc_ratio(p_) - t, 1e-6, 0.999))
        except Exception: req[c] = None
    F["M2_required_fraction"] = req; P(f"  M2 fraction of stars to remove as extreme to close the median: {req}")
    Eul, Rul = [], []
    for nm, l in LVD.items():
        ulv = fl(l.get("vlos_sigma_ul"))
        if ulv is None or fl(l.get("vlos_sigma")) or l.get("confirmed_galaxy") != "1": continue
        rh = fl(l.get("rhalf_sph_physical")) or fl(l.get("rhalf_physical")); ms = fl(l.get("mass_stellar")); mv = fl(l.get("M_V"))
        if not rh: continue
        ms = ms if ms is not None else 0.4 * (4.83 - mv) + 0.301; h = l["_h"]; cl = ("MW ultra-faint" if (mv is not None and mv > -7.7) else None) if h == "MW" else (("bright M31" if ms >= 5 else "M31 others") if h == "M31" else "LG field")
        if cl is None: continue
        dh = fl(l.get("distance_host")); y_ = row(f, nm, h, cl, ms, mv, rh, ulv, 0.0, dh, ul=True); y_["W0"] = W(y_["y"], y_["xe"]); y_["E1"] = y_["EN"] - math.log10(6 * y_["W0"] * R12 / y_["y"]); Rul.append(y_)
    F["M3"] = {}
    for c in CLS:
        i = [k for k, x in enumerate(R) if x["cls"] == c]; ux = [x for x in Rul if x["cls"] == c]; E_ = [E1[k] for k in i] + [x["E1"] for x in ux]; ce = [False] * len(i) + [True] * len(ux); m = km_median(E_, ce); rng = np.random.default_rng(77); ss = np.array([R[k]["s"] for k in i] + [0.0] * len(ux)); Ea = np.array(E_); bs = []
        for _ in range(2000):
            ix = rng.integers(0, len(Ea), len(Ea)); bs.append(km_median(Ea[ix] + ss[ix] * rng.standard_normal(len(ix)), np.array(ce)[ix]))
        sd = float(np.std(bs)); g = dict(N=len(E_), median=m, sd=sd, Z=m / sd if sd else None); F["M3"][c] = {**g, "n_ul": len(ux), "ul_E": {x["name"]: x["E1"] for x in ux}, **label(B[c], g)}
    P("  M3 with upper limits, KM: " + "; ".join(f"{c} {F['M3'][c]['median']:+.3f} (Z {F['M3'][c]['Z']:+.2f}, +{F['M3'][c]['n_ul']} UL) {F['M3'][c]['label']}" for c in CLS))
    subset("M4_N>=10", lambda x: x["N"] >= 10)
    # L
    grid = (0.5, 1.0, 1.5, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0); LG = {}
    for fa in grid:
        Wf = [W(x["y"] * fa, x["xe"]) for x in R]; LG[fa] = Evar(R, None, Wf)
        if fa == 1.0: K2d.append(float(np.max(np.abs(LG[fa] - E1))) if not MUT else float(np.max(np.abs(LG[fa] - np.array([lw[x['name']]['E1'] for x in R])))))
        add(f"L_ups{2 * fa:g}", LG[fa], name=f"L Upsilon_V {2 * fa:g}")
    F["L_required_Upsilon"] = {}
    for c in FAIL3:
        ms = [grade(R, LG[fa], (c,))[c]["median"] for fa in grid]; F["L_required_Upsilon"][c] = None
        for a, b, ma, mb in zip(grid, grid[1:], ms, ms[1:]):
            if ma > 0 >= mb: F["L_required_Upsilon"][c] = 2 * float(10 ** (math.log10(a) + (0 - ma) / (mb - ma) * math.log10(b / a))); break
    P(f"  L Upsilon_V required for median 0: {F['L_required_Upsilon']}")
    # R
    ef = os.path.join(HERE, f"cache_est_{f}{TAG}.json"); EST = json.load(open(ef)) if os.path.exists(ef) else {}
    for x in R:
        if x["name"] not in EST: EST[x["name"]] = estimators(x["y"], x["xe"]); json.dump(EST, open(ef, "w"))
    K5d += [abs(EST[x["name"]]["K5_b0"] / EST[x["name"]]["R1_virial"] - 1) for x in R]
    RK = [k for k in EST[R[0]["name"]] if k.startswith("R")]; Ek = {}
    for k in RK:
        Ek[k] = Evar(R, None, [EST[x["name"]][k] for x in R]); add(k, Ek[k])
    best = {c: min(RK, key=lambda k: grade(R, Ek[k], (c,))[c]["median"]) for c in CLS}; F["R_best"] = best; P(f"  R most favourable by class: {best}")
    nsph = [x["name"] for x in R if not x["sph"] and x["ell"]]; rhf = np.array([math.sqrt(1 - x["ell"]) if (not x["sph"] and x["ell"]) else 1.0 for x in R]); W4 = [W(x["y"] / r_ ** 2, x["xe"]) for x, r_ in zip(R, rhf)]; E4 = Evar(R, None, W4, rhf); F["R4_systems"] = nsph; add("R4_circularised", E4, name=f"R4 circularise {len(nsph)} systems")
    # stacks
    def stack(db, dt, p_, fa, usebest):
        s2 = (s2raw - db - dt) * trunc_ratio(p_); nf = int(np.sum(s2 < FLOOR * s2raw)); Ws = np.array([W(x["y"] * fa / r_ ** 2, x["xe"]) for x, r_ in zip(R, rhf)]); E = Evar(R, s2, Ws, rhf)
        if usebest:
            for i, x in enumerate(R):
                k = best[x["cls"]]; E[i] = E[i] - math.log10(EST[x["name"]][k] / EST[x["name"]]["wo"]) * 1.0
        return E, nf
    Ec, nc = stack(dbin["central"], dT["central"], 0.05, 1.0, False); EC, nC = stack(dbin["ceiling"], dT["ceiling"], 0.20, 2.0, True); F["floored"] = dict(central=nc, ceiling=nC)
    add("STACK_central", Ec, name=f"STACK central (floored {nc})"); add("STACK_ceiling", EC, name=f"STACK ceiling (floored {nC})")
    Gc, GC = grade(R, Ec), grade(R, EC); clo = all(abs(Gc[c]["Z"]) < 2 for c in FAIL3); cei = all(abs(GC[c]["Z"]) < 2 for c in FAIL3); oneC = {}
    for k, E_ in (("B2", Evar(R, s2raw - dbin["central"])), ("T3", Evar(R, np.array([x["s2b"] for x in R]) - dT["central"])), ("M2", E1 + math.log10(trunc_ratio(0.05))), ("R4", E4)):
        g = grade(R, E_); oneC[k] = all(abs(g[c]["Z"]) < 2 for c in FAIL3)
    F["verdict"] = "CLOSED BY COMPUTED EFFECT" if (clo or any(oneC.values())) else ("CEILING ONLY" if cei else "FAILURES STAND"); F["verdict_class"] = {c: "CLOSED BY COMPUTED EFFECT" if abs(Gc[c]["Z"]) < 2 else ("CEILING ONLY" if abs(GC[c]["Z"]) < 2 else "STANDS") for c in FAIL3}
    # ceiling without the floor's help: how many of each class are floored
    F["floored_by_class_ceiling"] = {c: int(sum(((s2raw - dbin['ceiling'] - dT['ceiling']) * trunc_ratio(0.2))[i] < FLOOR * s2raw[i] for i, x in enumerate(R) if x["cls"] == c)) for c in CLS}; F["floored_by_class_central"] = {c: int(sum(((s2raw - dbin['central'] - dT['central']) * trunc_ratio(0.05))[i] < FLOOR * s2raw[i] for i, x in enumerate(R) if x["cls"] == c)) for c in CLS}
    P(f"  >>> SATELLITE VERDICT [{f}]: {F['verdict']}; per class {F['verdict_class']}; floored ceiling {F['floored_by_class_ceiling']}, central {F['floored_by_class_central']}")
    # environment
    env = {}; sat = np.array([x["cls"] != "LG field" for x in R], float); mv = np.array([x["mv"] if x["mv"] is not None else np.nan for x in R]); ly = np.log10([x["y"] for x in R]); ok = np.isfinite(mv)
    for nm, Y in (("E0", np.array([x["E0"] for x in R])), ("E1", E1)):
        a = ols(Y, [sat]); b = ols(Y[ok], [sat[ok], mv[ok]]); c = ols(Y, [sat, ly]); fm = [i for i, x in enumerate(R) if x["cls"] == "LG field" and x["mv"] is not None]; sm = [i for i, x in enumerate(R) if x["cls"] != "LG field" and x["mv"] is not None]; lo, hi = max(min(mv[fm]), min(mv[sm])), min(max(mv[fm]), max(mv[sm])); pairs = []
        for i in fm:
            if lo <= mv[i] <= hi: j = min(sm, key=lambda j_: (abs(mv[j_] - mv[i]), j_)); pairs.append((Y[j] - Y[i], mv[i], R[j]["name"], R[i]["name"]))
        dd = np.array([p_[0] for p_ in pairs]); rng = np.random.default_rng(3); bsd = float(np.std([np.median(dd[rng.integers(0, len(dd), len(dd))]) for _ in range(5000)])) if len(dd) else None
        env[nm] = dict(A_raw=[a[0][1], a[1][1]], B_MV=[b[0][1], b[1][1]], B_MV_slope=[b[0][2], b[1][2]], C_y=[c[0][1], c[1][1]], C_y_slope=[c[0][2], c[1][2]], D_matched=dict(n=len(dd), median=float(np.median(dd)) if len(dd) else None, sd=bsd, pairs=[(p_[3], p_[2], float(p_[0])) for p_ in pairs]), overlap=[float(lo), float(hi)])
        P(f"  ENV {nm}: sat-field raw {a[0][1]:+.3f}+-{a[1][1]:.3f}; +M_V {b[0][1]:+.3f}+-{b[1][1]:.3f} (M_V slope {b[0][2]:+.3f}+-{b[1][2]:.3f}); +log y {c[0][1]:+.3f}+-{c[1][1]:.3f} (slope {c[0][2]:+.3f}+-{c[1][2]:.3f}); matched n {len(dd)} median {env[nm]['D_matched']['median']:+.3f}+-{bsd:.3f}; overlap M_V {lo:.2f} to {hi:.2f}")
    e = env["E0"]; zA, zB, zC = e["A_raw"][0] / e["A_raw"][1], e["B_MV"][0] / e["B_MV"][1], e["C_y"][0] / e["C_y"][1]
    env["label"] = "NOT SEPARATED" if (e["B_MV"][1] > 0.3 or e["C_y"][1] > 0.3 or e["D_matched"]["n"] < 5) else ("ENVIRONMENT" if zB > 2 and zC > 2 else ("LUMINOSITY OR ACCELERATION" if abs(zA) >= 2 and (abs(zB) < 2 or abs(zC) < 2) else "NO RAW DIFFERENCE")); P(f"  ENV label (E0): {env['label']} (Z raw {zA:+.2f}, M_V {zB:+.2f}, y {zC:+.2f})"); F["env"] = env
    # F slope, Z2's 45
    zz = [r for (ff, n), r in Z2.items() if ff == f]; xr = {r["name"]: r for r in X1 if r["footing"] == f}; lx = np.log10([fl(r["x_e"]) for r in zz]); mvz = np.array([fl(r["M_V"]) for r in zz]); yN = np.array([float(xr[r["name"]]["Delta[Newton]"]) for r in zz]); yA = np.array([float(xr[r["name"]]["Delta[AQUAL + EFE L*0 (exact MOND + EFE)]"]) for r in zz]); bN = ols(yN, [lx, mvz]); bA = ols(yA, [lx, mvz]); F["slope"] = dict(newton=[bN[0][1], bN[1][1]], residual_AQUAL=[bA[0][1], bA[1][1]], predicted=bN[0][1] - bA[0][1])
    y1 = {x["name"]: x["E1"] for x in R}; hs = {}
    for h in ("MW", "M31"):
        i = [k for k, x in enumerate(R) if x["host"] == h and x["xe"] > 0 and x["mv"] is not None]; yy = np.array([x["EN"] for x in (R[k] for k in i)]); lxx = np.log10([R[k]["xe"] for k in i]); mm = np.array([R[k]["mv"] for k in i]); pr = np.array([R[k]["EN"] - R[k]["E1"] for k in i]); bh = ols(yy, [lxx, mm]); pb = np.linalg.lstsq(np.column_stack([np.ones(len(i)), lxx, mm]), pr, rcond=None)[0]; hs[h] = dict(data=[bh[0][1], bh[1][1]], pred_E1=float(pb[1]), N=len(i))
    F["slope"]["by_host_law_sample"] = hs; P(f"  F slope on log x_e at fixed M_V, Z2's 45: data {bN[0][1]:+.3f}+-{bN[1][1]:.3f}, predicted {F['slope']['predicted']:+.3f}; by host, data vs E1's prediction: {hs}")
    if f == "canonical": CHK["K7"] = abs(bN[0][1] - (-0.05)) < 0.02 and abs(F["slope"]["predicted"] - (-0.76)) < 0.02
    # G: gas on field dwarfs
    Rf = [x for x in R if x["cls"] == "LG field"]; gt = {}
    for x in Rf:
        l = LVD[x["name"]]; mhi = fl(l.get("mass_HI"));
        if mhi is not None and not l.get("mass_HI_ul"):
            ms = next(float(r["logMstar"]) for r in X1 if r["name"] == x["name"]); fa = 1 + 1.33 * 10 ** (mhi - ms) / MFAC; gt[x["name"]] = dict(fgas=fa, E1=x["E1"], E1gas=x["E1"] - math.log10(W(x["y"] * fa, x["xe"]) / x["W0"]))
    Eg = [gt[x["name"]]["E1gas"] if x["name"] in gt else x["E1"] for x in Rf]; ss = np.array([x["s"] for x in Rf]); m_, sd_ = boot(np.array(Eg), ss, np.random.default_rng(9)); F["G_field_gas"] = dict(per=gt, median=m_, sd=sd_, Z=m_ / sd_, N_gas=len(gt), N=len(Rf)); P(f"  G field + 1.33 HI as stars: {m_:+.3f} (Z {m_ / sd_:+.2f}), {len(gt)} of {len(Rf)} with HI; rotation: LVD has no v_rot column, NOT COMPUTABLE from LVD")
    # IC 1613
    a0_ = a0; MS0, MG0, V0, RM, I0 = 2.88e7 * MFAC, 5.93e7, 16.9, 2.71, 48.0; xr1 = xr["IC 1613"]; xm = fl(xr1["x_e_mid"]) or 0.0; l = LVD["IC 1613"]; xs = float(g_host(fl(l["distance_m31"]) * KPC, MHOST["M31"], a0) + g_host(fl(l["distance_gc"]) * KPC, MHOST["MW"], a0)) / a0; Rds = float(xr1["rh_pc"]) / 1678.0
    def gdisc(M, Rd, Rk):
        """Freeman exponential disc: V^2 = 4 pi G Sigma0 Rd y^2 [I0K0 - I1K1], y = R/2Rd, Sigma0 = M/(2 pi Rd^2); returns V^2/R in m/s^2."""
        y_ = Rk / (2 * Rd); V2 = 2 * G5 * M * MS5 / (Rd * KPC) * y_ * y_ * (i0(y_) * k0(y_) - i1(y_) * k1(y_)); return V2 / (Rk * KPC)
    def Eic(i=I0, Rdg=None, ms=MS0, dx=0.0, dfac=1.0, extra2=0.0):
        V = V0 * math.sin(math.radians(I0)) / math.sin(math.radians(i)); R_ = RM * dfac; mst, mg = ms * dfac ** 2, MG0 * dfac ** 2; go = (V * V + extra2) * 1e6 / (R_ * KPC)
        gN = (G5 * (mst + mg) * MS5 / (R_ * KPC) ** 2) if Rdg is None else float(gdisc(mst, Rds * dfac, R_) + gdisc(mg, Rdg * dfac, R_))
        return math.log10(go) - math.log10(float(nu(gN / a0_)) * gN) - dx
    def efe_d(xe_):
        a_ = RM * KPC * 0.75; y_ = GZ * (MS0 + MG0) * MSZ / (a_ ** 2 * a0_); return math.log10(W(y_, xe_) / W(y_, 0.0))
    ir = {}; ib = Eic(); ir["base"] = ib; dxm, dxs = efe_d(xm) if xm > 0 else 0.0, efe_d(xs)
    terms = dict(I1_i37_9=Eic(37.9), I1_i34_4=Eic(34.4), I1_i24_5=Eic(24.5), I2_included_oh=ib, I2_if_missed_s5=Eic(extra2=25 * RM / (RM / 3)), I2_if_missed_s9=Eic(extra2=81 * RM / (RM / 3)), I2_if_missed_s12=Eic(extra2=144 * RM / (RM / 3)), I3_central=Eic(Rdg=RM / 3), I3_ceiling=Eic(Rdg=RM), I4_mid=Eic(dx=dxm), I4_sum=Eic(dx=dxs), I5_Mstar0=Eic(ms=0.0), I6_d0_9=Eic(dfac=0.9), I6_d1_1=Eic(dfac=1.1))
    dbest = max((0.9, 1.1), key=lambda d_: Eic(dfac=d_)); stc = Eic(37.9, RM / 3, dx=dxm); stC = Eic(24.5, RM, 0.0, dxs, dbest); terms["I8_central"] = stc; terms["I8_ceiling"] = stC
    SE = 0.075; SE7 = math.sqrt(0.075 ** 2 + (2 * 0.15 / math.log(10)) ** 2); ir["terms"] = {k: dict(E=v, Z=v / SE, Z15=v / SE7, share=(ib - v) / ib, label=("CARRIES" if ((ib - v) / ib >= 1 or abs(v / SE) < 2) else "PARTIAL" if (ib - v) / ib >= 0.25 else "WORSENS" if (ib - v) / ib <= -0.25 else "MINOR")) for k, v in terms.items()}
    try: ir["i_required"] = brentq(lambda i: Eic(i), 5, 48)
    except Exception: ir["i_required"] = None
    try: ir["i_range_Z2"] = [brentq(lambda i: Eic(i) - 2 * SE, 5, 48), brentq(lambda i: Eic(i) + 2 * SE, 5, 60)]
    except Exception: ir["i_range_Z2"] = None
    try: ir["i_required_I3central"] = brentq(lambda i: Eic(i, RM / 3, dx=dxm), 5, 48)
    except Exception: ir["i_required_I3central"] = None
    ir.update(xe_mid=xm, xe_sum=xs, dx_mid=dxm, dx_sum=dxs, Z_base=ib / SE, Z15_base=ib / SE7, Rd_star=Rds, verdict="CLOSED BY COMPUTED EFFECT" if abs(stc / SE) < 2 or any(abs(terms[k] / SE) < 2 for k in ("I1_i37_9", "I3_central", "I4_mid")) else "CEILING ONLY" if abs(stC / SE) < 2 else "FAILURES STAND")
    sig, rhi = 10.8, float(xr1["rh_pc"]); r12i = 4 / 3 * rhi * PC5
    def Es(i_, q_=0.6, vrot=13.0):
        c2, s2 = math.cos(math.radians(i_)) ** 2, math.sin(math.radians(i_)) ** 2; v2 = sig ** 2 / (q_ * q_ * c2 + s2) * (2 + q_ * q_) + vrot ** 2; go = v2 * 1e6 / r12i; gN = G5 * 0.5 * (MS0 + MG0) * MS5 / r12i ** 2; return math.log10(go) - math.log10(float(nu(gN / a0_)) * gN)
    ir["E_sigma"] = {f"i{i_}": Es(i_) for i_ in (48, 37.9, 34.4, 24.5)}; ir["field_row_E1"] = lw["IC 1613"]["E1"]; F["IC1613"] = ir
    P(f"  IC 1613 base {ib:+.4f} (Z {ib / SE:+.2f}, with 15 % V {ib / SE7:+.2f}); x_e mid {xm:.4f}, sum {xs:.4f}; i for E=0 {ir['i_required']}; |Z|<2 range {ir['i_range_Z2']}; i for E=0 with I3 central + I4 {ir['i_required_I3central']}; verdict {ir['verdict']}"); P("    " + "; ".join(f"{k} {v['E']:+.3f} (Z {v['Z']:+.2f}) sh {v['share']:+.2f} {v['label']}" for k, v in ir["terms"].items())); P(f"    E_sigma {ir['E_sigma']}; X1 field row E1 {ir['field_row_E1']:+.3f}")
    if f == "canonical": CHK["K6"] = abs(ib - (-0.5928)) < 0.001
    # ---- POST-RESULT, reported only, no label changes (see README)
    PR = F["post"] = {}
    def sc(E_): g = grade(R, E_); return {c: dict(median=g[c]["median"], Z=g[c]["Z"]) for c in CLS}
    def mock_clip(ff, vp, sd, nm=200, err=2.2):
        rng = np.random.default_rng(sd); o = np.zeros((nm, len(R)))
        for j, x in enumerate(R):
            N = int(x["N"]); V = math.sqrt(slaw2[j]) * rng.standard_normal((nm, N)) + err * rng.standard_normal((nm, N)) + (rng.uniform(0, 1, (nm, N)) < ff) * vp[rng.integers(0, len(vp), (nm, N))]
            for m in range(nm):
                v = V[m]
                for _ in range(5):
                    c0 = np.median(v); s0 = max(1.4826 * np.median(np.abs(v - c0)), err); k_ = np.abs(v - c0) < 3 * s0
                    if k_.all() or k_.sum() < 3: break
                    v = v[k_]
                o[m, j] = max(np.var(v, ddof=1) - err * err, 0.0) if len(v) > 1 else 0.0
        return o
    PR["mock_clipped"] = {}
    for tag, ff, vp, sd in (("central", 0.5, vc, 21), ("ceiling", 1.0, vC, 22)):
        Mc = mock_clip(ff, vp, sd); Emc = np.log10(np.maximum(Mc, 0.01 * slaw2) / slaw2); PR["mock_clipped"][tag] = {c: dict(mock=float(np.median(np.median(Emc[:, [k for k, x in enumerate(R) if x["cls"] == c]], axis=1))), P_ge=float(np.mean(np.median(Emc[:, [k for k, x in enumerate(R) if x["cls"] == c]], axis=1) >= Bb1[c]["median"])), data=Bb1[c]["median"]) for c in CLS}
    # T3 with adiabatic damping (first-order form), and at d/2
    dA = {}; pcomp = {}
    for tag, fp, vf in (("damped_central", 3.0, math.sqrt(2)), ("undamped_d2", 2.0, math.sqrt(2)), ("damped_d2", 2.0, math.sqrt(2))):
        d = np.zeros(len(R))
        for i, x in enumerate(R):
            if x["host"] not in ("MW", "M31") or not x["dh"]: continue
            MH = MHOST[x["host"]]; z = x["z"]; rp = fl(z["r_peri_kpc"]) if z and z.get("pm") == "True" else None; ra = fl(z["r_apo_kpc"]) if rp else None; p = (rp if rp else x["dh"] / fp) * KPC; rm = (0.5 * (rp + ra) if rp and ra else x["dh"]) * KPC; Vc = math.sqrt(float(g_host(p, MH, a0)) * p); Tor = 2 * np.pi * rm / math.sqrt(float(g_host(rm, MH, a0)) * rm); Gam = abs(float(g_host(p * 1.001, MH, a0)) - float(g_host(p * 0.999, MH, a0))) / (0.002 * p); tau = p / (vf * Vc); r12_ = 4 / 3 * x["rh"] * PCZ; om = x["sig"] * 1e3 * math.sqrt(3) / r12_; Af = (1 + (om * tau) ** 2) ** -2.5 if tag.startswith("damped") else 1.0
            d[i] = (Gam * r12_ * tau) ** 2 / 3 * (10 * GYR / Tor) / 1e6 * Af
        dA[tag] = d; PR[f"T3_{tag}"] = sc(Evar(R, np.array([x["s2b"] for x in R]) - d))
    Ens, _ = stack(dbin["central"], np.zeros(len(R)), 0.05, 1.0, False); PR["STACK_central_no_T3"] = sc(Ens); Eda, _ = stack(dbin["central"], dA["damped_central"], 0.05, 1.0, False); PR["STACK_central_damped_T3"] = sc(Eda); Enb, nb = stack(dbin["central"], np.zeros(len(R)), 0.20, 2.0, True); PR["STACK_ceiling_no_mock_ceiling_no_T3"] = {**sc(Enb), "floored": nb}
    from scipy.stats import spearmanr
    im = [i for i, x in enumerate(R) if x["cls"] == "bright M31"]; rho = spearmanr(np.log10(np.maximum(dT["central"][im], 1e-9) / s2raw[im]), np.array([R[i]["E0"] for i in im])); PR["bright_M31_E0_vs_heating"] = dict(rho=float(rho[0]), p=float(rho[1]), N=len(im))
    i0_ = [i for i, x in enumerate(R)]; Eiso = np.array([x["E0"] for x in R]); dE0 = Eiso - E1; PR["STACK_on_E0_central"] = sc(Ec + dE0); WC = np.array([W(x["y"] * 2.0, 0.0) for x in R]); Wiso = np.array([W(x["y"], 0.0) for x in R]); WC1 = np.array([W(x["y"] * 2.0, x["xe"]) for x in R]); PR["STACK_on_E0_ceiling"] = sc(EC + dE0 - np.log10(WC / Wiso) + np.log10(WC1 / np.array([x["W0"] for x in R]))); PR["L_E0_Ups4"] = sc(Eiso - np.log10(WC / Wiso))
    PR["field_rows"] = {x["name"]: dict(E1=x["E1"], E0=x["E0"], mv=x["mv"], s=x["s"]) for x in R if x["cls"] == "LG field"}; fi = [i for i, x in enumerate(R) if x["cls"] == "LG field"]; bf = ols(E1[fi], [mv[fi]]); PR["field_slope_MV"] = [bf[0][1], bf[1][1]]; PR["faintest_field_MV"] = float(np.nanmax(mv[fi])); PR["n_sat_fainter_than_field"] = int(sum(1 for x in R if x["cls"] != "LG field" and x["mv"] is not None and x["mv"] > np.nanmax(mv[fi])))
    bz = ols(np.array([fl(r["lb0"]) for r in zz]), [lx, mvz]); PR["K7_on_Z2_central_column_lb0"] = [bz[0][1], bz[1][1]]
    PR["B3_measured_cleaning_dE"] = {x["name"]: 2 * math.log10(fl(WT[WNAME[x["name"]]]["sigma_single"]) / fl(WT[WNAME[x["name"]]]["sigma_clean"])) for x in R if x["name"] in WNAME and WNAME[x["name"]] in WT and (fl(WT[WNAME[x["name"]]]["sigma_clean"]) or 0) > 0}
    SE15 = math.sqrt(0.075 ** 2 + (2 * 0.15 / math.log(10)) ** 2)
    try: ir["i_upper_Z2_15pcV"] = brentq(lambda i: Eic(i) + 2 * SE15, 5, 60)
    except Exception: ir["i_upper_Z2_15pcV"] = None
    P("  POST " + json.dumps({k: v for k, v in PR.items() if k not in ("field_rows",)}, sort_keys=True, default=float))
    save_cache()
CHK["K1"] = max(K1d) <= 1e-6; CHK["K2"] = max(K2d) <= 1e-6; CHK["K5"] = max(K5d) <= 0.01
kb = next((r for r in WK.values() if r["name"] == "Bootes I"), None); CHK["K8"] = bool(kb and abs(kb["sig0"] - fl(WT["Bootes_1"]["sigma_allmean"])) < 0.02)
P(f"\nK1 E1, plain, Z vs LW1 max |d| {max(K1d):.1e}: {CHK['K1']}; K2 factor-1 re-solve {max(K2d):.1e}: {CHK['K2']}; K3 {CHK['K3']}; K4 {CHK['K4']}; K5 beta 0 vs virial max {max(K5d):.2e}: {CHK['K5']}; K6 {CHK.get('K6')}; K7 {CHK.get('K7')}; K8 Bootes I {kb['sig0'] if kb else None} vs {WT['Bootes_1']['sigma_allmean']}: {CHK['K8']}")
RES["checks"] = {k: bool(v) for k, v in CHK.items()}
def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items() if k != "z"}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer, np.bool_)): return o.item()
    return o
json.dump(clean(RES), open(os.path.join(HERE, f"ux4_results{TAG}.json"), "w"), indent=1, sort_keys=True); open(os.path.join(HERE, f"ux4{TAG}.out"), "w").write("\n".join(OUT) + "\n"); save_cache()
sys.exit(0 if all(RES["checks"].values()) else 1)
