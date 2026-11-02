#!/usr/bin/env python3
"""RQ2 acceptance harness for a new framework. Criteria FROZEN_CRITERIA.md, rows REQUIREMENTS_V2.md, tolerances tolerances.json (committed before any run).
  python3 acceptance.py candidates/x.py [--no-keys] [--no-bullet]     scorecard, results/<name>[_MUTATE].{out,json}
  python3 acceptance.py --known                                        law against LW1, UX6, CRG1; mocks. Exit 1 on a failed known answer.
  RQ2_MUTATE=1 python3 acceptance.py --known                           twin: a0 x 1.5 labelled the law. Must exit 1.
A candidate is a module with NAME, g(Q), optional VERTICAL ("R", "A"), COSMO dict. Q holds baryons and local quantities in SI; never an observed dynamical quantity.
Grades nothing new, adopts no framework. kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import contextlib, csv, importlib.util, io, json, math, os, subprocess, sys, types
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True; os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
try: os.nice(19)
except OSError: pass
import numpy as np
from scipy.stats import chi2, norm
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); CRG = os.path.join(RB, "CRG1_clean_room_regrade")
TOL = json.load(open(os.path.join(HERE, "tolerances.json"))); ZL = TOL["Z_LINE"]; MUT = os.environ.get("RQ2_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); FEET = ("canonical", "alt"); LABEL_KEYS = {"sample", "r500", "name", "host"}
J = lambda *p: json.load(open(os.path.join(*p)))

class Q(dict):
    reads = set()
    def __getitem__(s, k): Q.reads.add(k); return dict.__getitem__(s, k)
def call(c, **kw):
    r = np.asarray(c.g(Q(**kw)), float)
    if not np.all(np.isfinite(r)): raise ValueError("candidate returned non-finite")
    return r
def NC(why): return dict(label="NOT COMPUTABLE", why=why)
def zrow(v, m, s, old="", note="", line=ZL):
    z = (v - m) / s
    if not np.isfinite(z): return NC("non-finite")
    return dict(label="PASS" if abs(z) <= line else "FAIL", value=float(v), measured=float(m), sigma=float(s), Z=float(z), old=old, note=note)
def lrow(ok, v, old, note=""): return dict(label="PASS" if ok else "FAIL", value=v, line_only=True, old=old, note=note)
def is_law(c, foot):
    gb = np.geomspace(1e-14, 1e-6, 200); a = A0[foot]
    try: r = call(c, gb=gb, gg=gb * 0, gs=gb, r=gb * 0 + 3e20, a0=a, sample="probe")
    except Exception: return False
    return bool(np.max(np.abs(r / (gb * (0.5 + np.sqrt(0.25 + a / gb))) - 1)) < 1e-12)

# ---------- CRG1 modules, patched to read its inputs and write nothing outside this lane
def crg():
    if "crg1_core" in sys.modules: return
    p = os.path.join(CRG, "v1", "crg1_core.py"); s = open(p).read(); a = 'INP = os.path.join(HERE, "inputs")'; assert s.count(a) == 1
    s = s.replace(a, f'INP = {os.path.join(CRG, "inputs")!r}').replace('PART = os.path.join(HERE, os.environ.get("CRG1_PARTIALS", "partials"))', f'PART = {os.path.join(HERE, "cache_crg", "p")!r}').replace('CACHE = os.path.join(HERE, os.environ.get("CRG1_CACHE", "cache"))', f'CACHE = {os.path.join(HERE, "cache_crg", "c")!r}')
    m = types.ModuleType("crg1_core"); m.__file__ = p; sys.modules["crg1_core"] = m; exec(compile(s, p, "exec"), m.__dict__); sys.path.insert(0, os.path.join(CRG, "v1"))

# ---------- A: SPARC
def rows_sparc(c, foot):
    crg(); import crg1_sparc as C; a0 = A0[foot]; R = {}
    G = C.load_gal()
    def model(g, gb):
        gg = np.sign(g["Vgas"]) * g["Vgas"] ** 2 * 1e6 / g["R"]; return call(c, gb=gb, gg=np.broadcast_to(gg, gb.shape), gs=gb - gg, r=np.broadcast_to(g["R"], gb.shape), a0=a0, sample="disc", name=g["name"])
    r = C.fit(G, model); Yb = r["Yb"]; t = C.tilt(G, Yb)
    R["A1"] = lrow(r["rms"] <= 0.110, r["rms"], "rms <= 0.110"); R["A2"] = lrow(0.50 <= r["Y_med"] <= 0.80, r["Y_med"], "0.50-0.80")
    q = np.array([g["Q"] <= 2 and g["Inc"] >= 30 for g in G]); V = np.array([g["Vflat"] for g in G]); lo = np.nan_to_num(Yb[q & (V > 0) & (V < 100)]); hi = np.nan_to_num(Yb[q & (V > 150)]); rg = np.random.default_rng(20261102)
    b = np.median(lo[rg.integers(0, len(lo), (2000, len(lo)))], 1) - np.median(hi[rg.integers(0, len(hi), (2000, len(hi)))], 1)
    R["A3"] = zrow(t["tilt"], 0.0, float(b.std()), f"|tilt| <= 0.15: {'PASS' if abs(t['tilt']) <= .15 else 'FAIL'}", "stat-only")
    R["A4"] = hs_row(G, c, a0, C)
    R.update(ul_rows(G, Yb, V, q))
    LT = C.load_lt(); E = []
    for x in LT:
        gN = np.array([C.E.G * x["Mb"] * C.E.Msun / x["R"] ** 2]); E.append(math.log10(x["V"] ** 2 / x["R"]) - math.log10(float(call(c, gb=gN, gg=gN * np.nan, gs=gN * np.nan, r=np.array([x["R"]]), a0=a0, sample="dwarf disc", name=x["name"])[0])))
    E = np.array(E); N = len(E); rg = np.random.default_rng(20261102); sd = float(np.std(np.median(E[rg.integers(0, N, (10000, N))] + TOL["IC_sE"] * rg.standard_normal((10000, N)), axis=1))); md = float(np.median(E))
    R["A9"] = zrow(md, 0.0, sd, f"|E| <= 0.10: {'PASS' if abs(md) <= .1 else 'FAIL'}", "stat-only; sE 0.075 per system")
    i = [k for k, x in enumerate(LT) if x["name"] == "IC 1613"][0]; s = math.hypot(TOL["IC_sE"], TOL["IC_V_frac"] * 2 / math.log(10)); x = LT[i]; extra = {}
    for inc in (37.9, 34.4): extra[f"E at i {inc}"] = float(E[i] + 2 * math.log10(math.sin(math.radians(48)) / math.sin(math.radians(inc))))
    R["A10"] = zrow(float(E[i]), 0.0, s, f"Z on sE alone {E[i] / TOL['IC_sE']:+.2f}: {'PASS' if abs(E[i] / TOL['IC_sE']) < 2 else 'FAIL'}", "DISPUTED inclination, HI holes. " + ", ".join(f"{k} {v:+.3f}" for k, v in extra.items()))
    return R
def hs_row(G, c, a0, C):
    Tb = {}
    for l in open(os.path.join(CRG, "inputs", "sparc", "SPARC_Lelli2016c.mrt")):
        t = l.split()
        if len(t) == 19:
            try: Tb[t[0]] = (float(t[10]), float(t[11]))
            except ValueError: pass
    X, Y = [], []
    for g in G:
        if not (g["Q"] <= 2 and g["Inc"] >= 30 and 60 <= g["Vflat"] < 120) or g["name"] not in Tb or Tb[g["name"]][0] <= 0: continue
        VB2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + .5 * g["Vdisk"] ** 2 + .7 * g["Vbul"] ** 2; gb = VB2 * 1e6 / g["R"]; ok = (gb > 0) & (g["Vobs"] > 0); Rk = g["Rk"]; R2 = 2 * Tb[g["name"]][1]
        if ok.sum() < 2 or R2 < Rk[ok].min() or R2 > Rk[ok].max(): continue
        gg = np.sign(g["Vgas"]) * g["Vgas"] ** 2 * 1e6 / g["R"]; m = call(c, gb=np.where(ok, gb, 1e-30), gg=gg, gs=gb - gg, r=g["R"], a0=a0, sample="disc", name=g["name"]); Vm = np.sqrt(np.maximum(m * g["R"], 0)) / 1e3
        Y.append(float(np.interp(math.log(R2), np.log(Rk[ok]), Vm[ok] / g["Vobs"][ok] - 1))); X.append(math.log10(Tb[g["name"]][0]))
    X, Y = np.array(X), np.array(Y); sl = lambda x, y: float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum()); rg = np.random.default_rng(1); b = np.array([sl(X[k], Y[k]) for k in rg.integers(0, len(X), (10000, len(X)))]); s = float((np.nanpercentile(b, 84) - np.nanpercentile(b, 16)) / 2); r = zrow(sl(X, Y), 0.0, s, "|b| <= 2 sigma", f"n {len(X)}, stat-only"); return r
def ul_rows(G, Yb, V, q):
    EST = J(RB, "UL1_measured_upsilon_test", "ul1_est.json")["primary"]; BI = ("60-100", "100-150", "150-200", "200-250", "250-400"); fb = np.array([g["Vbul"][-1] ** 2 / max(g["Vdisk"][-1] ** 2 + g["Vbul"][-1] ** 2, 1e-9) for g in G]); u = Yb * (1 + .4 * fb); out = {}
    def boot(a):
        r = np.random.default_rng(1); n = len(a); return float(np.std(np.log10(np.median(a[r.integers(0, n, (2000, n))], axis=1))))
    S = {b: q & (V >= float(b.split("-")[0])) & (V < float(b.split("-")[1])) for b in BI}; m = {b: float(np.median(u[S[b]])) for b in BI}
    for rid, X in (("A5", "GSWLC"), ("A6", "Taylor")):
        Zs = {}; 
        for b in BI:
            h = math.sqrt(max(boot(u[S[b]]), 1.25 * EST[b][X]["sig"] / math.sqrt(S[b].sum())) ** 2 + .04 ** 2); Zs[b] = (math.log10(m[b]) - math.log10(EST[b][X]["mu"])) / h
        w = max(Zs.values(), key=abs); out[rid] = dict(label="PASS" if max(abs(v) for v in Zs.values()) <= ZL else "FAIL", Z=float(w), bins={k: float(v) for k, v in Zs.items()}, values=m, old="level |Z| <= 2, same", note="DISPUTED estimator; worst bin shown")
        if X == "GSWLC":
            h = {b: math.sqrt(max(boot(u[S[b]]), 1.25 * EST[b][X]["sig"] / math.sqrt(S[b].sum())) ** 2 + .04 ** 2) for b in BI}; a, b_ = "100-150", "150-200"; st = (math.log10(m[b_]) - math.log10(m[a])) - (math.log10(EST[b_][X]["mu"]) - math.log10(EST[a][X]["mu"])); out["A7"] = dict(label="PASS" if abs(st / math.hypot(h[a], h[b_])) <= ZL else "FAIL", Z=float(st / math.hypot(h[a], h[b_])), old="step |Z| <= 2, same", note="23, 25 galaxies")
    return out

# ---------- A: dwarfs, LW1's rows
G5, MS5, PC5 = 6.67430e-11, 1.98847e30, 3.0856775814913673e16; GZ, MSZ, PCZ = 6.67430e-11, 1.989e30, 3.0856775814913673e16; KPCZ = 1e3 * PCZ; CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field"); GE2 = 2.0592e-10; MHOST = {"MW": 6.0e10, "M31": 1.0e11, "field": 6.0e10}; A_H = 3.0 * KPCZ
def rows_dwarfs(c, foot):
    a0 = A0[foot]; ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv")))); arrf = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}; medf = float(np.median(list(arrf.values()))); RW = []
    for r in csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv"))):
        if r["footing"] != foot or r["cls"] not in CLS: continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None; b = arrf.get(r["name"], medf if (mv is not None and mv > -7.7) else 1.0); sc = float(r["sigma"]) * b; r12 = 4 / 3 * float(r["rh_pc"]) * PC5; Mb = 10 ** float(r["logMstar"]); gobs = 3 * (sc * 1e3) ** 2 / r12; gN = G5 * (Mb / 2) * MS5 / r12 ** 2; dh = float(r["d_host_kpc"]) if r["d_host_kpc"] not in ("", None) else None; host = r["host"]
        gNh = GZ * MHOST[host if host in MHOST else "field"] * MSZ / (dh * KPCZ + A_H) ** 2 if dh else 0.0; gh = float(gNh * (0.5 + math.sqrt(0.25 + a0 / gNh))) if dh else 0.0
        RW.append(dict(cls=r["cls"], gobs=gobs, gN=gN, gNh=gNh, r12=r12, s=float(r["sdMC[Newton]"]), name=r["name"], host=host, y=GZ * Mb * MSZ / ((float(r["rh_pc"]) * PCZ) ** 2 * a0), xe=gh / a0, EN=math.log10(gobs / gN)))
    def cg(x, s): v = np.array([x]); return float(call(c, gb=v, gg=v * 0, gs=v, r=np.array([s["r12"]]), a0=a0, sample="dwarf", name=s["name"], host=s["host"])[0])
    def grade(key, E, sysv):
        rng = np.random.default_rng(20261026); o = {}
        for k in CLS:
            ii = [i for i, s in enumerate(RW) if s["cls"] == k]; e = E[ii]; se = np.array([RW[i]["s"] for i in ii]); N = len(ii); sd = float(np.std(np.median(e[rng.integers(0, N, (10000, N))] + se[rng.integers(0, N, (10000, N))] * 0, axis=1))) if False else None
            ix = rng.integers(0, N, (10000, N)); sd = float(np.std(np.median(e[ix] + se[ix] * rng.standard_normal((10000, N)), axis=1))); md = float(np.median(e)); st = math.hypot(sd, TOL["DW_sys_stack"][k] if sysv else 0.0); o[k] = dict(median=md, sd=sd, Z_sd=md / sd, sigma=st, Z=md / st)
        return dict(label="PASS" if all(abs(v["Z"]) <= ZL for v in o.values()) else "FAIL", classes=o, Z=max((v["Z"] for v in o.values()), key=abs), old=f"sd only: {'PASS' if all(abs(v['Z_sd']) < 2 for v in o.values()) else 'FAIL'}", note=key)
    R = {"A12": grade("plain", np.array([math.log10(s["gobs"] / cg(s["gN"], s)) for s in RW]), True)}
    R["A13"] = grade("algebraic field", np.array([math.log10(s["gobs"] / ((cg(s["gN"] + s["gNh"], s) - cg(s["gNh"], s)) if s["gNh"] > 0 else cg(s["gN"], s))) for s in RW]), True)
    if is_law(c, foot):
        CA = J(RB, "LW1_law_scorecard", "cache_dwarfs", "solves.json"); E = []
        for s in RW:
            k = f"{s['y']!r}|{s['xe']!r}"
            if k not in CA: R["A11"] = NC("solve not in LW1's cache"); break
            E.append(s["EN"] - CA[k])
        else: R["A11"] = grade("E1, AQUAL solver, LW1's cached solves", np.array(E), True)
    else: R["A11"] = NC("needs a field equation with this candidate's law; solver is the law's AQUAL")
    return R

# ---------- A: DiskMass, Milky Way, LW1's paths
_DM = {}
def dm_ns():
    if _DM: return _DM["n"]
    S = os.path.join(REPO, "campaign_fresh_gravity", "CFG576_diskmass_sigz", "cfg576_diskmass.py"); n = {"__file__": os.path.abspath(S), "__name__": "h"}
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(S).read().split('P("=" * 100)')[0], "h", "exec"), n)
    _DM["n"] = n; return n
def rows_dm(c, foot):
    from scipy.optimize import brentq
    n = dm_ns(); gal, terms, KV, sexp, gbar, G = n["gal"], n["galaxy_terms"], n["K_VERT"], n["sexp"], n["gbar"], n["G"]; KU = 3.0857e13; a0 = A0[foot]; T = TOL["DM"]; R = {}
    def cg(x, gas, r): v = np.array([x / KU]); return float(call(c, gb=v, gg=np.array([gas / KU]), gs=v - gas / KU, r=np.array([r * 3.0857e19]), a0=a0, sample="disc")[0]) * KU
    def one(g, r, form):
        n["gal_BD"] = g["BD"]; t = terms(g, r); go = t["vrot"] ** 2 / r; gas = gbar(t, r, 0.0)
        try: Y = brentq(lambda Y: cg(gbar(t, r, Y), gas, r) - go, .02, 5.0)
        except ValueError: return None
        gb = gbar(t, r, Y); Sig = Y * t["I0"] * math.exp(-r / t["hR"]) + sexp(r, t["Ma"], 2 * t["hR"]) + sexp(r, t["Mm"], t["hR"]); KN = 2 * math.pi * G * Sig * (1 - math.exp(-1)); B = (lambda h: cg(h, gas, r) / h)(math.hypot(gb, KN)) if form == "A" else 1 + (cg(gb, gas, r) - gb) * t["hz"] / r / KN
        return math.sqrt(math.pi * G * KV * t["hz"] * Sig * B) / t["smeas"]
    forms = [f for f in getattr(c, "VERTICAL", ()) if f in ("R", "A")]
    if not forms: return {"A18": NC("no vertical form declared")}
    o = {}
    for f in forms:
        x = [one(g, 1.5 * g["hR"], f) for g in gal.values()]; x = np.array([a for a in x if a is not None])
        if len(x) == 0: return {"A18": NC("no solution")}
        bs = np.median(np.random.default_rng(576).choice(x, size=(2000, len(x))), axis=1); w = float(np.percentile(bs, 84) - np.percentile(bs, 16)) / 2; r = float(np.median(x)); tgt = (T["c_lo"] + T["c_hi"]) / 2; s = math.sqrt(((T["c_hi"] - T["c_lo"]) / 4) ** 2 + T["line_sigma"] ** 2 + w ** 2)
        o[f] = zrow(r, tgt, s, f"r 0.90-1.10, n >= 27: {'PASS' if .9 <= r <= 1.1 and len(x) >= 27 else 'FAIL'}", f"form {f}, n {len(x)}; DISPUTED c")
    R["A18"] = dict(o[forms[0]], forms=o); R["A18"]["label"] = "PASS" if all(v["label"] == "PASS" for v in o.values()) else ("FORM-DEPENDENT" if any(v["label"] == "PASS" for v in o.values()) else "FAIL")
    return R
_MW = {}
def mw_ns():
    if _MW: return _MW
    p = os.path.join(RB, "LW1_law_scorecard", "lw1_mw.py"); s = open(p).read().split('if "--grade" in sys.argv:')[0]; n = {"__file__": p, "__name__": "m"}; a = sys.argv; sys.argv = [p]; exec(compile(s, p, "exec"), n); sys.argv = a; _MW.update(n); return _MW
def rows_mw(c, foot):
    forms = getattr(c, "VERTICAL", ())
    if "R" not in forms: return dict(A15=NC("no round-rule form declared; A and Q need a solve"), A16=NC("same"))
    n = mw_ns(); ns, L, PS = n["ns"], n["L"], n["PS"]; a0 = L.A0_SI[foot]; BR_R, R0, OR = n["BR_R"], n["R0"], n["OR"]; KZU = n["KZU"]; Mu = PS.mass_unit(a0); g = ns["mw_grid"](6.6e10 / Mu); RALL = np.r_[R0, OR, BR_R]; rows = []; nR = 1 + len(OR); kk = PS.KPC / 1e6
    for sp, rhof in n["spec"]():
        rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); Mt = 2 * float(np.sum(rho1 * g.vol)); pr = PS.Problem(g, rho1, Mt, 0.0, Lam=0.0); Ph = pr.solve_newton(); oN = ns["mw_obs"](g, Ph, a0); vb = L.vc_plane(ns, g, Ph, a0, RALL); gb = vb ** 2 / RALL
        gc = (call(c, gb=gb / kk, gg=gb * np.nan, gs=gb * np.nan, r=RALL * PS.KPC, a0=a0, sample="MW") * kk) - gb; vR = np.sqrt(vb ** 2 + RALL * gc); K = np.array(oN["K"]) + gc[nR:] * 1.1 / BR_R / KZU; K0 = oN["K_R0"] + gc[0] * 1.1 / R0 / KZU; rows.append(dict(sp, R=n["lines"](float(vR[0]), K, float(K0), vR[1:nR])))
    C = n["classify"](rows, "R"); T = TOL["MW_Kz"]; s = math.hypot(T["stat"], T["pad_frac"] * T["meas"]); bi = C["best_in_prior"]; o = {"A16": lrow(C["label"] == "PASS", dict(cls=C["cls"], n_all=C["n_all"], n_in_prior=sum(1 for r in rows if all(r["R"][l] for l in ("L1", "L2a", "L2b", "L3")) and r["tag_Rd_IN"] and r["tag_Mstar_IN"])), "FEASIBLE IN PRIORS", "form R"), "A15": zrow(bi["K_R0"], T["meas"], s, f"66.4 +- 4.4: {'PASS' if abs(bi['K_R0'] - 66.4) <= 4.4 else 'FAIL'}", "form R, best in-prior cell; DISPUTED summary")}
    if is_law(c, foot):
        ds = [json.loads(l) for l in open(os.path.join(RB, "LW1_law_scorecard", "cache_mw", f"{foot}_1.0.jsonl"))]; ra = [d for d in ds if not d.get("mcm")]; CA = n["classify"](ra, "A"); o["A16"]["form_A_read"] = CA["cls"]; o["A16"]["note"] += f"; form A READ from LW1's cells: {CA['cls']}"; o["A16"]["label"] = "FORM-DEPENDENT" if o["A16"]["label"] == "PASS" else "FAIL"
        k = CA["best_in_prior"]["K_R0"] if CA["best_in_prior"] else float("nan"); o["A15"]["form_A_K"] = k; o["A15"]["label"] = "FORM-DEPENDENT" if o["A15"]["label"] == "PASS" and abs(k - T["meas"]) / s > ZL else o["A15"]["label"]; o["A15"]["note"] += f"; form A best in-prior K {k:.1f}, Z {(k - T['meas']) / s:+.2f}, READ"
    return o

# ---------- A30 lensing, B1 groups
def rows_lens(c, foot):
    crg(); import crg1_lens as Le; L = Le.load(); st = Le.Stencil(L["Rn"] * 1e6); TH = Le.TwoHalo(L); rex = [.343, .442, .433, .429]; T0 = np.array([TH.esd2h(L["R"][b], rex[b]) * Le.FF for b in range(4)]); SIk = 1e6 / 3.0857e16; Tb = np.zeros((len(Le.LMG), 60)); a0 = A0[foot]
    for i, lm in enumerate(Le.LMG):
        MB, Mbm = Le.baryon(float(lm)); gb = Le.Gpc * MB / Le.RGRID ** 2; gg = Le.Gpc * (MB - 10 ** float(lm)) / Le.RGRID ** 2; v = call(c, gb=gb * SIk, gg=gg * SIk, gs=(gb - gg) * SIk, r=Le.RGRID * 3.0857e16, a0=a0, sample="lens"); Tb[i] = st.dsig(MB * v / (gb * SIk), "linear")
    m = Le.stack(L, Tb); ch, b = Le.fit(L, m, list(range(15)), T0); d = 56; old = J(CRG, "v1", "crg1_results.json")["C4"].get(foot, {}).get("Ln", {})
    return {"A30": zrow(ch, d, math.sqrt(2 * d), "CL2's rule, against retired halos: not applicable to a new framework", f"chi2 {ch:.1f}/56, two-halo b {np.round(b, 2).tolist()}; cov only")}
def rows_groups(c, foot):
    crg(); import crg1_groups as Gr; P = Gr.P; a0 = A0[foot]; rows = Gr.load(); XG, LX, RHO, gt0 = Gr.XG, Gr.LX, Gr.RHO_H, Gr.gN_t
    def ls(lM, Re, dl):
        a = Re * (P.pc * 1e3) / 1.8153; Mb = 10 ** (lM + dl) * P.Msun; U = P.G * Mb / a ** 2; v = gt0 * U; gt = call(c, gb=v, gg=v * np.nan, gs=v * np.nan, r=XG * a, a0=a0, sample="group") / U; s2 = np.trapz(4 * math.pi * XG ** 2 * RHO * XG * gt * XG, LX) / 3 * P.G * Mb / a; return .5 * math.log10(s2) - 3
    d = np.array([x[0] - ls(x[1], x[2], 0.0) for x in rows]); sl = np.array([(ls(x[1], x[2], .01) - ls(x[1], x[2], -.01)) / .02 for x in rows]); m = d.mean(); t = math.hypot(d.std(ddof=1) / math.sqrt(len(d)), .10 * sl.mean())
    return {"B1": zrow(-float(m), 0.0, t, "CONSISTENT, tot <= 0.045", "sign: Z here = -(data - model)/sigma")}

# ---------- B: X-COP, deficit, planets
def rows_xcop(c, foot):
    from astropy.io import fits
    Gm, MSm, PCm = 6.674e-11, 1.989e30, 3.0857e16; D = os.path.join(REPO, "real_research", "data", "xcop"); a0 = A0[foot]; XC = []; lawf = lambda gb: gb * (.5 + np.sqrt(.25 + a0 / gb)); li = lambda r, m, t: float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
    for name in sorted(os.listdir(D)):
        p = os.path.join(D, name)
        if not (os.path.isdir(p) and os.path.exists(os.path.join(p, f"{name}_mstar.fits"))): continue
        with fits.open(os.path.join(p, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
        with fits.open(os.path.join(p, f"{name}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
        with fits.open(os.path.join(p, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
        for x in (.1, .2, .3, .5, .7):
            r = x * r5; mh, mg, ms = li(hm["RADIUS"], hm["M_FORW"], r), li(ga["RADIUS"] * rg, ga["MGAS"], r), li(st["RADIUS"], st["MSTAR"], r)
            if np.all(np.isfinite([mh, mg, ms])): XC.append(dict(n=name, x=x, r=r * 1e3 * PCm, r5=r5 * 1e3 * PCm, mh=mh, mg=mg, ms=ms))
    rr = np.array([z["r"] for z in XC]); mb = np.array([z["mg"] + z["ms"] for z in XC]); gb = Gm * mb * MSm / rr ** 2; v = call(c, gb=gb, gg=Gm * np.array([z["mg"] for z in XC]) * MSm / rr ** 2, gs=Gm * np.array([z["ms"] for z in XC]) * MSm / rr ** 2, r=rr, r500=np.array([z["r5"] for z in XC]), a0=a0, sample="cluster"); Mc = v * rr ** 2 / Gm / MSm; mh = np.array([z["mh"] for z in XC]); d = np.log10(mh / Mc); ns = sorted({z["n"] for z in XC}); by = np.array([d[[z["n"] == n for z in XC]].mean() for n in ns]); m = float(d.mean()); rms = float(np.sqrt((d ** 2).mean())); s = math.hypot(by.std(ddof=1) / math.sqrt(len(ns)), TOL["XCOP"]["hse_sys"]); R = {}
    R["B23"] = zrow(m, 0.0, s, f"|mean| <= 0.05: {'PASS' if abs(m) <= .05 else 'FAIL'}", "DISPUTED hydrostatic; Z positive = model short"); R["B24"] = lrow(rms <= .10, rms, "rms <= 0.10")
    TD = TOL["DEFICIT"][foot]; Ml = lawf(gb) * rr ** 2 / Gm / MSm; Qc = (Mc - Ml) / np.array([z["mg"] for z in XC]); xs = np.array([z["x"] for z in XC]); o = {}
    for x, qh, qb in zip(TD["x"], TD["Q_hse"], TD["Q_bracket"]): o[f"{x:g}"] = dict(Q=float(np.median(Qc[np.isclose(xs, x)])), meas=qh, Z=float((np.median(Qc[np.isclose(xs, x)]) - qh) / (qh - qb)))
    R["B25"] = dict(label="PASS" if all(abs(v["Z"]) <= ZL for v in o.values()) else "FAIL", x=o, Z=max((v["Z"] for v in o.values()), key=abs), old="none, a measurement", note="DISPUTED HSE, HSC 1.7; sigma = distance to LF1's bracket")
    return R
def rows_planets(c, foot):
    a0 = A0[foot]; Rc = J(RB, "M1_trilemma", "m1_trilemma_results.json")["R2c"]["C1_planet_ratios"]; AU = 1.496e11; GMs = 6.674e-11 * 1.989e30; o = {}
    for p, d in (("Earth", 1.0), ("Mars", 1.524), ("Saturn", 9.58)):
        bound = A0["canonical"] / Rc[f"canonical|{p}"]; r = np.array([d * AU]); gN = GMs / r ** 2; o[p] = float(abs(call(c, gb=gN, gg=gN * 0, gs=gN, r=r, a0=a0, sample="planet")[0] - gN[0]) / bound)
    return {"C1": dict(label="PASS" if max(o.values()) <= 1 else "FAIL", ratios=o, value=max(o.values()), old="anomaly <= bound", note="radial anomaly / M1's bound; candidate g used at planets directly")}

# ---------- Keys, LW1's path, candidate in the source mass
def keys_tail():
    sys.path.insert(0, os.path.join(RB, "LW1_law_scorecard")); import lw1_keys as L; T = L.T; a = 'return RM ** 2 * _comb(gb, gb * (1 + _LAW["c"] * S / 3), _A0L[foot], _LAW["rd"]) / GE, S'; assert T.count(a) == 1; T = T.replace(a, 'return RM ** 2 * _rq2(gb, S, foot) / GE, S'); b = "def _msrc(Mb, foot):"; assert T.count(b) == 1
    T = T.replace(b, '''import importlib.util as _iu
_sp = _iu.spec_from_file_location("cand", os.environ["RQ2_CAND"]); _cm = _iu.module_from_spec(_sp); _sp.loader.exec_module(_cm); _UFS = 1 + float(os.environ["X73_FSTAR"])
def _rq2(gb, S, foot):
    i_, pp_ = _ST["cur"]; a0 = _A0L[foot]; gg = gb / _UFS; r5 = float(pp_["R500"]) * float(NX["MPC"]); v = _cm.g(dict(gb=gb, gg=gg, gs=gb - gg, S=S, r=RM, r500=r5, a0=a0, sample="cluster"))
    return np.asarray(v, float)
''' + b); c = 'pp = prep(i, foot, hk); m, S = _msrc(pp["Mb"], foot);'; assert T.count(c) == 1; T = T.replace(c, 'pp = prep(i, foot, hk); _ST["cur"] = (i, pp); m, S = _msrc(pp["Mb"], foot);'); return L, T
KS = ["G-IN-all", "G-MID-T1", "G-MID-T2", "G-MID-T3", "G-MID-b", "G-OUT-all", "G-OUT-T1", "G-OUT-T2", "G-OUT-T3", "G-OUT-b", "G-OUT-Mall", "G-OUT-M1", "G-OUT-M2", "G-OUT-M3", "G-IN-Mall"]; HH = ("h0672", "h0686")
def run_keys(path, name):
    L, T = keys_tail(); res = {}
    for tag, dex, fs in (("g005_f034", .005, "0.034"), ("g005_f0615", .005, "0.0615"), ("g0_f034", 0.0, "0.034")):
        W = os.path.join(HERE, f"cache_keys", f"{name}{TAG}_{tag}"); os.makedirs(W, exist_ok=True); O = os.path.join(W, "keys.json")
        if not (os.path.exists(O) and json.load(open(O)).get("done")):
            TL = os.path.join(W, "tail.py"); open(TL, "w").write(T); d = open(os.path.join(L.SL1, "sl1_harvest.py")).read()
            for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(L.GAS % dex if dex else "") + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(TL)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('X73_FSTAR="0.034"', f'X73_FSTAR="{fs}"')):
                assert d.count(a) == 1, a; d = d.replace(a, b)
            df = os.path.join(W, "driver.py"); open(df, "w").write(d); env = dict(os.environ, UR1_SL1=L.SL1, SL1_OUT=O, CN1_FORCE="1", LW1_A0X="1.0", RQ2_CAND=os.path.abspath(path), DR1_RUN=json.dumps(dict(rows=L.ROWS, k2=False)))
            subprocess.run(["nice", "-n", "19", sys.executable, df], env=env, stdout=open(os.path.join(W, "run.log"), "w"), stderr=subprocess.STDOUT)
        if not os.path.exists(O) or not json.load(open(O)).get("done"): return None
        res[tag] = json.load(open(O))
    return res
def rows_keys(K, foot):
    M3 = J(RB, "M3A1_outer_key_audit", "m3a1_results.json")["Ztot"]; R = {}; Z = {}; rk = f"R1|c0|{foot}"
    for t in ("g005_f034", "g005_f0615"):
        r = K[t][rk]
        for h in HH: Z[f"{t}|{h}"] = r["Z"][h]
    for i, k in enumerate(KS):
        vals = [Z[x][k] for x in Z]; w = max(vals, key=abs); R[f"B{i + 4}:{k}"] = dict(label="PASS" if max(abs(v) for v in vals) <= ZL else "FAIL", Z=float(w), old="|Z| <= 2, same", note="stat-only; worst of both h, both f*")
    r = K["g005_f034"][rk]; r0 = K["g0_f034"][rk]; zts = {}; js = {}
    for fs, t in (("0.034", "g005_f034"), ("0.0615", "g005_f0615")):
        r = K[t][rk]; Rr = K[t]["R"][foot]
        for h in HH:
            s = r["tmpl"][h]["G-OUT-M3"][1]; zm = r["Z"][h]["G-OUT-M3"]; q = M3[f"{fs}|{h}"]; dd = (zm - r0["Z"][h]["G-OUT-M3"]) / .005 if fs == "0.034" else 0.0; sg = abs(dd) * TOL["KEYS"]["gas_se"] * s; tot = math.sqrt(s ** 2 + sg ** 2 + q["slope"] ** 2 + q["m"] ** 2 + q["nz"] ** 2 + q["leak"] ** 2); zts[f"{fs}|{h}"] = zm * s / tot
            ks = Rr[h]["keys"]; Rb = np.array(Rr[h]["R_boot"]); z0 = np.array([r["Z"][h][k] for k in ks]); w, V = np.linalg.eigh(Rb); ok = w >= 1e-3 * w.max(); z = V[:, ok].T @ z0; c2 = float((z * z / w[ok]).sum()); js[f"{fs}|{h}"] = dict(chi2=c2, p=float(chi2.sf(c2, int(ok.sum()))))
    w = max(zts.values(), key=abs); R["B19"] = dict(label="PASS" if max(abs(v) for v in zts.values()) <= ZL else "FAIL", Z=float(w), cells=zts, old="none", note="M3A1 terms; gas term from f* 0.034's dZ/dgas only, 0.0615 omits it")
    pm = min(v["p"] for v in js.values()); R["B20"] = dict(label="PASS" if pm >= TOL["KEYS"]["p_pass"] else "FAIL", p=pm, cells=js, old="JOINT PASS p >= 0.05", note="BA1's R recomputed on this run")
    return R

# ---------- Bullet, UX6's map
_BU = {}
def bullet_ns():
    if _BU: return _BU
    p = os.path.join(RB, "UX6_gas_term_bullet", "ux6_bullet.py"); s = open(p).read().split('say("=" * 90); say("UX6')[0]; a = 'OUT = open(os.path.join(HERE, f"ux6_bullet{TAG}.out"), "w")'; assert s.count(a) == 1; s = s.replace(a, "import io as _io; OUT = _io.StringIO()"); n = {"__file__": p, "__name__": "b"}; exec(compile(s, p, "exec"), n); _BU.update(n); return _BU
def rows_bullet(c):
    n = bullet_ns(); SYS = n["SYS"]; law0 = n["SYS"].extra
    def extra(sp, C, reg=True):
        a0 = sp["a0"]; gv = tuple(sum(q[i] for q in C["gas"]) for i in range(3)); gb = [gv[i] + C["st"][i] for i in range(3)]
        if reg: gb[1] = gb[1] + a0 / 1000.0
        g = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2); gg = np.sqrt(gv[0] ** 2 + gv[1] ** 2 + gv[2] ** 2); sh = g.shape; L = call(c, gb=g.ravel(), gg=gg.ravel(), gs=(np.sqrt(C["st"][0] ** 2 + C["st"][1] ** 2 + C["st"][2] ** 2)).ravel(), r=g.ravel() * np.nan, a0=a0, sample="merger").reshape(sh); m = L / np.maximum(g, 1e-300); return tuple(gb[i] * (m - 1) for i in range(3))
    SYS.extra = extra; sp = {f: dict(form="CAND", k=0.0, a0=A0[f]) for f in FEET}; R = n["run"](sp); out = {}
    for f in FEET:
        o = n["observe"](*R[f]); T = TOL["BULLET"]; zs = [(o["M300"][i] / T["obs_M300"][i] - 1) / T["sig_frac_PROVISIONAL"] for i in (0, 1)]; ok = o["cls"] != "FAIL" and all(abs(z) <= ZL for z in zs)
        out[f] = {"B28": dict(label="PASS" if ok else "FAIL", Z=float(max(zs, key=abs)), M300=o["M300"], ZM=zs, dkappa=[o["main"]["dkappa"], o["sub"]["dkappa"]], peak=[o["main"]["peak"], o["sub"]["peak"]], old=f"UX6: {o['cls']}", note="static map, QUMOND-type; sigma PROVISIONAL")}
    SYS.extra = law0; return out

# ---------- Rows no g can reach
READ_LAW = {"A8": "not needed: no component", "A17": "form R 3.29-3.41, about +4 sigma (X5, UX5)", "A19": "not measured", "A31": "blue 0.878, red 1.313 (BL1)", "B21": "slope 0.47 against 0.90 +- 0.21 (CFG687)", "C2": "2.44-4.59 / 2.85-5.19 x line, FAILS (E2)", "D1": "no term; no-dust plik 128270/605 (UX2)", "D6": "no pass without dust (RF5)", "E1": "none (UX1)"}
N_ROWS = {"A8": "needs a live model", "A14": "needs a field equation", "A17": "scale-length fit not wired", "A19": "no data", "A20": "not wired", "A21": "not wired", "A22": "not wired", "A23": "not wired", "A24": "not wired", "A25": "not wired", "A26": "not wired", "A27": "not wired", "A28": "not wired", "A29": "not wired", "A31": "no colour input wired", "B2": "not wired", "B3": "not wired", "B21": "covered by keys; slope not wired", "B22": "open data", "B26": "projected Q not wired", "B29": "no line", "C2": "needs a field equation", "C3": "needs an action", "C4": "needs an action", "C5": "needs an action", "C6": "needs an action", "C7": "sealed data", "C8": "needs an action", "C9": "needs an action", "D1": "needs Boltzmann run", "D2": "same", "D3": "voided", "D4": "needs a live model", "D5": "needs a derivation", "D6": "needs Boltzmann run", "D7": "same", "D8": "same", "D9": "same", "D10": "same", "D11": "needs forward model", "D12": "needs a0(z)", "D13": "sealed data", "E1": "candidate must supply", "E3": "needs an action", "E4": "same", "E5": "same", "E6": "same", "E7": "same", "E8": "same", "E9": "same", "E10": "same", "E11": "same", "E14": "declared"}
BLOCKS = dict(sparc=["A3", "A4"], ups=["A5", "A6", "A7"], lt=["A9"], ic=["A10"], dw=["A11", "A12", "A13"], mw=["A15"], dm=["A18"], lens=["A30"], groups=["B1"], xcop=["B23", "B25"], bullet=["B28"])

def scorecard(path, keys=True, bullet=True):
    spec = importlib.util.spec_from_file_location("cand", path); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c); Q.reads = set(); name = os.path.basename(path)[:-3]; out = dict(name=getattr(c, "NAME", name), footings={})
    K = None
    if keys:
        try:
            gb = np.geomspace(1e-14, 1e-8, 20); call(c, gb=gb, gg=gb, gs=gb * 0, S=gb, r=gb * 0 + 1e22, r500=gb * 0 + 3e22, a0=A0["canonical"], sample="cluster"); K = run_keys(path, name)
        except Exception as e: K = None
    BU = None
    if bullet:
        try: BU = rows_bullet(c)
        except Exception as e: BU = str(e)
    for f in FEET:
        R = {}
        for fn, ids in ((rows_sparc, ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A9", "A10"]), (rows_dwarfs, ["A11", "A12", "A13"]), (rows_mw, ["A15", "A16"]), (rows_dm, ["A18"]), (rows_lens, ["A30"]), (rows_groups, ["B1"]), (rows_xcop, ["B23", "B24", "B25"]), (rows_planets, ["C1"])):
            try: R.update(fn(c, f))
            except Exception as e:
                for i in ids:
                    if i not in R: R[i] = NC(f"{type(e).__name__}: {str(e)[:80]}")
        if K: R.update(rows_keys(K, f))
        else:
            for i, k in enumerate(KS): R[f"B{i + 4}:{k}"] = NC("keys path not run or candidate non-finite")
            R["B19"] = NC("keys path"); R["B20"] = NC("keys path")
        R["B28"] = BU[f]["B28"] if isinstance(BU, dict) else NC(f"bullet path: {BU}" if BU else "not run")
        lawc = is_law(c, f)
        for i, w in N_ROWS.items(): R[i] = dict(label="READ", read=READ_LAW[i], note="from the record, not computed; never a pass") if lawc and i in READ_LAW else NC(w)
        if hasattr(c, "COSMO"): R["D1"] = dict(label="READ", read=str(c.COSMO), note="declared by candidate; never a pass")
        R["B27"] = dict(label="OPEN DATA", note="HSC against KiDS, A 0.650 +- 0.075 frozen, 0.746 +- 0.091 unbiased; not a candidate test; keys here are KiDS")
        lb = sorted(LABEL_KEYS & Q.reads)
        for r in R.values():
            if lb: r["label_tag"] = "[LABEL]"
        out["footings"][f] = dict(rows=R, summary=summary(R))
    out["reads"] = sorted(Q.reads); out["label_reads"] = sorted(LABEL_KEYS & Q.reads); out["law_numeric"] = {f: is_law(c, f) for f in FEET}
    return out
def summary(R):
    n = {}
    for r in R.values(): n[r["label"]] = n.get(r["label"], 0) + 1
    zb = {}
    for b, ids in BLOCKS.items():
        v = [abs(R[i]["Z"]) for i in ids if i in R and "Z" in R[i]]
        if v: zb[b] = max(v)
    if "p" in R.get("B20", {}): zb["keys"] = float(norm.isf(max(R["B20"]["p"], 1e-300) / 2))
    c2 = float(sum(v * v for v in zb.values())); N = len(R)
    return dict(counts=n, N=N, blocks=zb, block_chi2=c2, block_dof=len(zb), block_p=float(chi2.sf(c2, len(zb))) if zb else None, overall="REJECTED" if n.get("FAIL", 0) else ("ACCEPTED" if n.get("PASS", 0) == N else f"NOT REJECTED ON {n.get('PASS', 0)} OF {N}"), note="blocks treated as independent, worst |Z| per block, which selects upward; a summary, not a discovery p")
def write(o, tag):
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True); L = [f"RQ2 acceptance: {o['name']}{TAG}. Grades nothing new. kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.", f"keys read by g: {o['reads']}; label reads: {o['label_reads'] or 'none'}"]
    key = lambda k: (k[0], int(''.join(ch for ch in k.split(':')[0][1:] if ch.isdigit())))
    for f in FEET:
        F = o["footings"][f]; L.append(f"\n== {f}: {F['summary']['overall']}; {F['summary']['counts']}; N {F['summary']['N']}; block chi2 {F['summary']['block_chi2']:.1f}/{F['summary']['block_dof']}")
        for i in sorted(F["rows"], key=key):
            r = F["rows"][i]; v = r.get("value"); L.append(f"{i:16s} {r['label']:15s}" + (f" Z {r['Z']:+7.2f}" if "Z" in r else " " * 10) + (f" v {v:.4g}" if isinstance(v, float) else "") + (f" p {r['p']:.1e}" if "p" in r else "") + (f" {r.get('label_tag', '')}") + (f" | old: {r['old']}" if r.get("old") else "") + (f" | {r.get('note') or r.get('why') or ''}") + (f" | READ {r['read']}" if "read" in r else ""))
    open(os.path.join(HERE, "results", f"{tag}{TAG}.out"), "w").write("\n".join(L) + "\n"); json.dump(o, open(os.path.join(HERE, "results", f"{tag}{TAG}.json"), "w"), indent=1, sort_keys=True, default=float); return L

def known():
    C = []
    def chk(n, ok, m): C.append((n, bool(ok), m)); print(f"[{'PASS' if ok else 'FAIL'}] {n}: {m}", flush=True)
    o = scorecard(os.path.join(HERE, "candidates", "law.py")); write(o, "law"); LW = J(RB, "LW1_law_scorecard", "lw1_results.json"); DW = J(RB, "LW1_law_scorecard", "lw1_dwarfs.json")["footings"]; DM = J(RB, "LW1_law_scorecard", "lw1_dm.json"); XC = J(RB, "LW1_law_scorecard", "lw1_xcop.json"); MW = J(RB, "LW1_law_scorecard", "lw1_mw.json"); FH = J(RB, "FG1_final_grade", "fg1_harness_results.json")["C4"]; CR = J(CRG, "v1", "crg1_results.json")["C4"]; K0 = J(RB, "LW1_law_scorecard", "lw1_keys_g005_f034.json"); LX = {"canonical": dict(rms=.0541, U=.52, t=.02, lt=-.025, hs=-.016, hss=.061, ic=-.593), "alt": dict(rms=.0537, U=.44, t=-.02, lt=-.064, hs=-.023, hss=.063, ic=-.631)}
    for f in FEET:
        R = o["footings"][f]["rows"]; X = LX[f]
        chk(f"KA1 {f} SPARC", abs(R["A1"].get("value", 9) - X["rms"]) < 1e-3 and abs(R["A2"].get("value", 9) - X["U"]) < 1e-3 + .005, f"rms {R['A1'].get('value')}, U {R['A2'].get('value')}")
        chk(f"KA1 {f} tilt, LT", abs(R["A3"].get("value", 9) - X["t"]) < .01 and abs(R["A9"].get("value", 9) - X["lt"]) < 1e-3, f"{R['A3'].get('value')}, {R['A9'].get('value')}")
        chk(f"KA1 {f} HS1", abs(R["A4"].get("value", 9) - X["hs"]) < 2e-3 and abs(R["A4"].get("sigma", 9) - X["hss"]) < 2e-3, f"{R['A4'].get('value')} +- {R['A4'].get('sigma')}")
        chk(f"KA1 {f} IC 1613", abs(R["A10"].get("value", 9) - X["ic"]) < 1e-3, str(R["A10"].get("value")))
        ok = "classes" in R["A12"] and max(abs(R["A12"]["classes"][k]["median"] - DW[f]["rows"]["plain"][k]["median"]) for k in CLS) < 1e-6 and max(abs(R["A12"]["classes"][k]["Z_sd"] - DW[f]["rows"]["plain"][k]["Z"]) for k in CLS) < 1e-6; chk(f"KA1 {f} dwarfs plain", ok, "vs LW1 |d| < 1e-6")
        ok = "classes" in R["A13"] and max(abs(R["A13"]["classes"][k]["median"] - DW[f]["rows"]["E2"][k]["median"]) for k in CLS) < 1e-3; chk(f"KA1 {f} dwarfs E2", ok, "vs LW1 |d| < 1e-3")
        ok = "classes" in R.get("A11", {}) and max(abs(R["A11"]["classes"][k]["median"] - DW[f]["rows"]["E1"][k]["median"]) for k in CLS) < 1e-6; chk(f"KA1 {f} dwarfs E1", ok, "vs LW1 |d| < 1e-6")
        ok = "forms" in R["A18"] and abs(R["A18"]["forms"]["R"]["value"] - DM[f]["R|1.5"]["r"]) < 1e-3 and abs(R["A18"]["forms"]["A"]["value"] - DM[f]["A|1.5"]["r"]) < 1e-3; chk(f"KA1 {f} DiskMass", ok, str({k: v["value"] for k, v in R["A18"].get("forms", {}).items()}))
        lw = MW[f]["R|1.0"]; ok = R["A16"].get("value", {}).get("cls") == lw["cls"] and R["A16"]["value"]["n_all"] == lw["n_all"] and R["A16"].get("form_A_read") == MW[f]["A|1.0"]["cls"]; chk(f"KA1 {f} Milky Way", ok, f"{R['A16'].get('value')}, A {R['A16'].get('form_A_read')}")
        chk(f"KA1 {f} X-COP", abs(R["B23"].get("value", 9) - XC[f]["cached"]["mean"]) < 1e-3 and abs(R["B24"].get("value", 9) - XC[f]["cached"]["rms"]) < 1e-3, f"{R['B23'].get('value')}, {R['B24'].get('value')}")
        chk(f"KA1 {f} groups", abs(abs(R["B1"].get("Z", 99)) - abs(FH[f]["groups"]["Z"])) < .01, f"{R['B1'].get('Z')} vs {FH[f]['groups']['Z']}")
        chk(f"KA1 {f} lens chi2", abs(R["A30"].get("value", 9e9) - CR[f]["Ln"]["chi2_L2H"]) < 1e-3, f"{R['A30'].get('value')} vs CRG1 {CR[f]['Ln']['chi2_L2H']}")
        chk(f"KA1 {f} planets", abs(R["C1"].get("value", 1e99) / 1e4) < 12, str(R["C1"].get("ratios")))
        bad = [k for k in KS if R[f"B{KS.index(k) + 4}:{k}"]["label"] == "FAIL"]; ref = K0[f"R1|c0|{f}"]["bad"]; ld = LW["keys"][f"{f}|+0.005|0.034"]["cells"]; chk(f"KA1 {f} keys", sorted(bad) == sorted(ref), f"{bad} vs LW1 {ref}")
        Kr = json.load(open(os.path.join(HERE, "cache_keys", f"law{TAG}_g005_f034", "keys.json"))) if os.path.exists(os.path.join(HERE, "cache_keys", f"law{TAG}_g005_f034", "keys.json")) else None
        if Kr: d = max(abs(Kr[f"R1|c0|{f}"]["Z"][h][k] - K0[f"R1|c0|{f}"]["Z"][h][k]) for h in HH for k in KS); chk(f"KA1 {f} keys Z", d <= 1e-6, f"|d| {d:.1e}")
        else: chk(f"KA1 {f} keys Z", False, "no keys output")
        chk(f"KA1 {f} joint", abs(R["B20"].get("cells", {}).get("0.034|h0672", {}).get("chi2", 0) - ld["h0672"]["chi2"]) < 1e-6 and abs(R["B19"].get("cells", {}).get("0.034|h0672", 0) - ld["h0672"]["Ztot"]) < 1e-6, f"chi2 {R['B20'].get('cells', {}).get('0.034|h0672')}, Ztot {R['B19'].get('cells', {}).get('0.034|h0672')}")
        UX = J(RB, "UX6_gas_term_bullet", "ux6_results.json"); r = R["B28"]; ref = None
        for path in (("rows",), ("OBS",)):
            if path[0] in UX: ref = UX[path[0]].get(f"LAW|{f}")
        chk(f"KA2 {f} Bullet", "M300" in r and ref is not None and max(abs(r["M300"][i] / ref["M300"][i] - 1) for i in (0, 1)) < 1e-6, f"{r.get('M300')}, dkappa {r.get('dkappa')}")
    lab = {f: {k: v["label"] for k, v in o["footings"][f]["rows"].items()} for f in FEET}
    p = scorecard(os.path.join(HERE, "candidates", "mock_planted.py")); write(p, "mock_planted")
    for f in FEET:
        chk(f"KA3 {f} planted fails A9", p["footings"][f]["rows"]["A9"]["label"] == "FAIL" and lab[f]["A9"] == "PASS", f"mock {p['footings'][f]['rows']['A9'].get('Z')}"); fl = [k for k, v in p["footings"][f]["rows"].items() if v["label"] == "PASS" and lab[f][k] == "FAIL"]; print(f"  planted, rows FAIL for the law now PASS, {f}: {fl}", flush=True)
    q = scorecard(os.path.join(HERE, "candidates", "mock_nan.py")); write(q, "mock_nan")
    for f in FEET: chk(f"KA3 {f} NaN mock", q["footings"][f]["summary"]["counts"].get("PASS", 0) == 0 and q["footings"][f]["summary"]["counts"].get("FAIL", 0) == 0, str(q["footings"][f]["summary"]["counts"]))
    m = scorecard(os.path.join(HERE, "candidates", "mock_label.py"), keys=True, bullet=False); write(m, "mock_label"); chk("KA3 label mock", "sample" in m["label_reads"] and m["footings"]["canonical"]["rows"]["A1"].get("label_tag") == "[LABEL]", str(m["label_reads"]))
    bad = [c for c in C if not c[1]]; s = "\n".join(f"{'PASS' if c[1] else 'FAIL'} {c[0]}: {c[2]}" for c in C) + f"\n{len(C) - len(bad)} of {len(C)} known answers pass\n"; os.makedirs(os.path.join(HERE, "results"), exist_ok=True); open(os.path.join(HERE, "results", f"known{TAG}.out"), "w").write(s); print(s); sys.exit(1 if bad else 0)

if __name__ == "__main__":
    if "--known" in sys.argv: known()
    p = [a for a in sys.argv[1:] if not a.startswith("--")][0]; o = scorecard(p, "--no-keys" not in sys.argv, "--no-bullet" not in sys.argv); print("\n".join(write(o, os.path.basename(p)[:-3])))
