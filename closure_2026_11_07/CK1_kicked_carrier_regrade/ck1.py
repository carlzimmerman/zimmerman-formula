#!/usr/bin/env python3
"""CK1: the L388 kicked collisionless "cold dark energy" carrier re-graded at today's needs (criteria f6f15f9e05).

Adopts nothing. kappa = 1/2 FITTED; not theory closed. Both footings, never pooled. One thread, < 1 GB, SIGTERM
writes a partial JSON. Read-only reuse: L388 JSONs, XR13's X-COP mass assignment, GB1's battery and gates (through
NA2's prefix, as NA2 loads them), NA2's X-COP shapes and per-bin grader, KD1 / PB3 numbers, X5's MW best cells.

  python3 closure_2026_11_07/CK1_kicked_carrier_regrade/ck1.py            -> ck1.json / ck1.out
  python3 closure_2026_11_07/CK1_kicked_carrier_regrade/ck1.py --mutate   -> ck1_MUTATE.json / ck1_MUTATE.out
"""
import os, sys, io, json, math, signal, resource, time
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "ck1_MUTATE" if MUT else "ck1"; OUT = []; T0 = time.time()
RES = dict(tag=TAG, criteria="f6f15f9e05 + A1 ecde71eaff + A2 17dbf6d9e8 + A3", reference="X-COP/groups/galaxies: CK1 RM (framework-native: the law at today's footings, KD1 own-terms capture, on-disk baryons); L388 (LCDM-referenced) reading only", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
def P(s=""): print(s, flush=True); OUT.append(str(s))
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
def J(o):
    if isinstance(o, dict): return {str(k): J(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [J(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return J(o.tolist())
    return o
def dump():
    RES["peak_rss_MB"] = rss(); RES["runtime_s"] = time.time() - T0
    json.dump(J(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, sort_keys=True)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
def _term(sig, frm):
    RES["partial"] = "SIGTERM"; P("SIGTERM: partial JSON written"); dump(); sys.exit(3)
signal.signal(signal.SIGTERM, _term)

# ------------------------------------------------------------------ NA2 prefix (QX7 iter_5 prelude, GB1 battery)
p_na2 = os.path.join(REPO, "closure_2026_11_07", "NA2_compact_baryon_remnant", "na2.py")
s_na2 = open(p_na2).read(); s_na2 = s_na2[:s_na2.index("# ------------------------------------------------------------------ section-2 amounts")]
NS = {"__file__": p_na2, "__name__": "na2_lib"}; _a = sys.argv; sys.argv = [p_na2]; _so = sys.stdout; sys.stdout = io.StringIO()
try: exec(compile(s_na2, p_na2, "exec"), NS)
finally: sys.argv = _a; sys.stdout = _so
GB, XC, XINFO, SH, XPROF, A0, BINE = NS["GB"], NS["XC"], NS["XINFO"], NS["SH"], NS["XPROF"], NS["A0"], NS["BIN_EDGES"]
KPC, MS, GSI, glaw_si = NS["KPC"], NS["MS"], NS["G"], NS["glaw"]
FOOTS = ("canonical", "alt")
CL6 = os.path.join(REPO, "closure_2026_11_06")
KDJ = json.load(open(os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.json")))
PB3J = json.load(open(os.path.join(REPO, "pbh_2026_11_06", "PB3_cluster_class_budget", "pb3.json")))
CF = {f: KDJ["footings"][f]["uniform_f_diag"]["capture_f"] for f in FOOTS}
NEED = {f: KDJ["footings"][f]["uniform_f_diag"] for f in FOOTS}
SET = {f: KDJ["footings"][f]["setting"] for f in FOOTS}
CAP = {f: NEED[f]["SPARC_f_max"] for f in FOOTS}
UA1 = {"canonical": (0.052, 0.459), "alt": (0.009, 0.415)}
P(f"CK1 {'MUTATE' if MUT else 'MAIN'}. C_f {CF['canonical']:.4f} / {CF['alt']:.4f}. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")

# battery as GB1 builds it (rms_L0, sigU, KiDS)
BATT = {}
for f in FOOTS:
    a0 = A0[f]; S, E, X = GB["build"](f, a0)
    st = GB["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
    B = dict(f=f, S=S, E=E, X=X, GR={0: GB["groups_pts"](a0, 0.0), 1: GB["groups_pts"](a0, 1.0)}, U=GB["udgs"](f, a0),
             D=GB["dsphs"](f, a0), K=GB["kids"](a0), sigU=sigU)
    B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S]))); BATT[f] = B
GL0 = json.load(open(os.path.join(CL6, "GB1_all_gates_battery", "gb1.json")))
P(f"battery loaded; rss {rss():.0f} MB")

# ------------------------------------------------------------------ units (kpc, km/s, Msun)
G = 4.30091727e-6
def a0k(f): return A0[f] * 3.0856775814913673e19 / 1e6
def glaw(gN, a0): gN = np.asarray(gN, float); return 0.5 * gN + np.sqrt(0.25 * gN * gN + a0 * gN)
HH = 0.6736                      # XR13's h for the 1 Mpc/h sphere and the Msun -> Msun/h conversion
R1H = 1000.0 / HH                # kpc

# ================================================================== L388 retention (section 3)
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
L388 = json.load(open(os.path.join(DS, "L388_linear_gate_pooled_results.json")))["numbers"]
L388M = json.load(open(os.path.join(DS, "L388_linear_gate_pooled_results_MUTATE.json")))["numbers"]
BINS = ((6e13, 1e14), (1e14, 1.5e14), (1.5e14, 2.5e14), (2.5e14, 1e17)); BK = [f"{a:.1e}-{b:.1e}" for a, b in BINS]
RUN = (575.0, 600.0, 625.0, 650.0); VK = (500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0)
def pool(js, t):
    mh = np.concatenate([np.array(js["halos"][s]["M_lt_1Mpc_h"]) for s in ("7", "17", "29")])
    ee = np.concatenate([np.array(js["halos"][s]["eps"][t]) for s in ("7", "17", "29")])
    return mh, ee
EPS = {}; ka1 = 0.0
for v in RUN:
    t = f"v{int(v)}"; mh, ee = pool(L388, t); EPS[v] = {}
    for k, (b0, b1) in zip(BK, BINS):
        m = (mh >= b0) & (mh < b1); EPS[v][k] = float(np.median(ee[m])); ka1 = max(ka1, abs(EPS[v][k] - L388["retention_by_mass"][t][k][0]))
mh0, ee0 = pool(L388M, "v575"); EPS0 = {k: float(np.median(ee0[(mh0 >= b0) & (mh0 < b1)])) for k, (b0, b1) in zip(BK, BINS)}
LINE = {k: np.polyfit(RUN, [EPS[v][k] for v in RUN], 1) for k in BK}
def eps_at(v, k, mode="central"):
    if v in EPS: return EPS[v][k]
    if v == 0.0: return EPS0[k]
    lo, hi = EPS[575.0][k], EPS0[k]
    if v < 575.0:
        if mode == "lo": return lo
        if mode == "hi": return hi
        return float(min(max(np.polyval(LINE[k], v), lo), hi))
    return float(min(max(np.polyval(LINE[k], v), 0.0), hi))   # beyond 650 (MUTATE M2): the line, clipped
KA = {}
KA["KA1"] = dict(maxdiff=ka1, ok=bool(ka1 == 0.0), note="A3: code check only (L388 machinery on its own inputs); L388 is LCDM-referenced and not evidence")
top, low = BK[3], BK[0]
tr = [EPS[v][top] for v in (575.0, 650.0)]; lr = [EPS[v][low] for v in (575.0, 650.0)]
KA["KA2"] = dict(note="A3: code check only", top_575_650=tr, low_575_650=lr, ok=bool(round(max(tr), 2) == 0.85 and round(min(tr), 2) == 0.79 and round(max(lr), 2) == 0.34 and round(min(lr), 2) == 0.17))
P(f"KA1 L388 bin medians recomputed: max|d| {ka1:.1e} -> {'PASS' if KA['KA1']['ok'] else 'FAIL'}; KA2 top {tr}, low {lr} -> {'PASS' if KA['KA2']['ok'] else 'FAIL'}")
P("eps by bin (central): " + "; ".join(f"v{int(v)}: " + ", ".join(f"{eps_at(v, k):.3f}" for k in BK) for v in (0.0,) + VK))
P("eps(0) from L388's v_k = 0 runs: " + ", ".join(f"{EPS0[k]:.4f}" for k in BK))
RES["eps"] = {f"v{int(v)}": {k: dict(central=eps_at(v, k), lo=eps_at(v, k, "lo"), hi=eps_at(v, k, "hi")) for k in BK} for v in (0.0,) + VK}
RES["eps_line"] = {k: list(LINE[k]) for k in BK}
# per-halo log-linear eps(log M) fit (reading)
def eps_fit(v, M_h):
    mh = np.concatenate([np.array(L388["halos"][s]["M_lt_1Mpc_h"]) for s in ("7", "17", "29")]); sel = mh >= 1e14
    if v in EPS: ee = pool(L388, f"v{int(v)}")[1]
    else: ee = np.array([eps_at(v, top)] * len(mh))
    c = np.polyfit(np.log10(mh[sel]), ee[sel], 1); return float(min(max(np.polyval(c, math.log10(M_h)), 0.0), EPS0[top]))
mh_all = np.concatenate([np.array(L388["halos"][s]["M_lt_1Mpc_h"]) for s in ("7", "17", "29")])
MHMAX = float(mh_all.max())
# retention curve vs the bins' Newtonian proxy v_esc (for CK3)
RES["L388_bin_vesc_proxy_kms"] = {k: float(math.sqrt(2 * G * np.median(mh_all[(mh_all >= b0) & (mh_all < b1)]) / 1000.0)) for k, (b0, b1) in zip(BK, BINS)}

# ================================================================== X-COP placement (XR13 (g), unit-consistent)
R500J = json.load(open(os.path.join(REPO, "real_research", "data", "xcop", "xcop_r500_ettori2019.json")))
RHO_C0X = 2.775e11 * HH ** 2 / 1e9
PLACE = {}
for name, meta in R500J.items():
    d_ = os.path.join(REPO, "real_research", "data", "xcop", name)
    if not os.path.isdir(d_): continue
    with fits.open(os.path.join(d_, f"{name}_hydro_mass.fits")) as hm:
        par = {row["MODEL"].strip(): (float(row["RS"]), float(row["C200"])) for row in hm[2].data}
    rs, c = par["NFW"]; rhoc_z = RHO_C0X * (0.315 * (1 + meta["z"]) ** 3 + 0.685)
    M200 = 200 * rhoc_z * 4 / 3 * math.pi * (c * rs) ** 3
    m = lambda x: math.log(1 + x) - x / (1 + x)
    M1 = M200 * m(R1H / rs) / m(c); Mh = M1 * HH
    ib = max(i for i, (b0, b1) in enumerate(BINS) if Mh >= b0) if Mh >= BINS[0][0] else -1
    near = any(abs(Mh / b0 - 1) <= 0.10 for b0, _ in BINS[1:]) or Mh > 1.10 * MHMAX
    PLACE[name] = dict(M1_Msun=M1, M1_Msun_h=Mh, bin=BK[ib] if ib >= 0 else "below", bracket=[BK[max(ib - 1, 0)], BK[ib]] if near else [BK[ib]], near_edge_or_above=near)
m1 = [p["M1_Msun"] for p in PLACE.values()]
KA["KA6"] = dict(range_Msun=[min(m1), max(m1)], ok=bool(abs(min(m1) / 5.0e14 - 1) <= 0.02 and abs(max(m1) / 8.7e14 - 1) <= 0.02))
P(f"KA6 X-COP M(<1 Mpc/h) {min(m1):.3e}-{max(m1):.3e} Msun -> {'PASS' if KA['KA6']['ok'] else 'FAIL'}; most massive L388 halo {MHMAX:.3e} Msun/h")
for n, p in sorted(PLACE.items()): P(f"  placement {n:8s} M(<1 Mpc/h) {p['M1_Msun']:.3e} Msun = {p['M1_Msun_h']:.3e} Msun/h -> bin {p['bin']}{'  BRACKET ' + str(p['bracket']) if p['near_edge_or_above'] else ''}")
RES["xcop_placement"] = PLACE

# ================================================================== RM, the resolved release model (section 4)
def rho_mean_m(f, z):
    s = SET[f]; Om = (s["omega_b"] + s["omega_d"]) / s["h"] ** 2
    return Om * (1 + z) ** 3 * 277.536627 * s["h"] ** 2
def rho_crit(f, z):
    s = SET[f]; Om = (s["omega_b"] + s["omega_d"]) / s["h"] ** 2
    return 277.536627 * s["h"] ** 2 * (Om * (1 + z) ** 3 + 1 - Om)
CELLS = [("release", 0.0), ("release", 2.0), ("baryon", 0.0), ("baryon", 2.0)]
NRM = 20000

def rm(Mb_fun, rb_lo, rb_hi, f, vk, pot, zF, r_eval, newton=False, seed=11, N=NRM):
    """Mb_fun(r_kpc) -> Msun (vectorised). Parents C_f M_b(<r) in [rb_lo, rb_hi]; one isotropic kick at z_F.
    Returns f_ret, v_esc(r_F), sigma(r_F), r_F, R_out, M_c(<r_eval)."""
    a0 = a0k(f); cf = CF[f]
    rg = np.geomspace(rb_lo, max(rb_hi * 50, 1e5), 3000)
    Mb = np.maximum.accumulate(np.maximum(Mb_fun(rg), 0.0)); Mb_tot = Mb[-1]
    Msrc = (1 + cf) * Mb if pot == "release" else Mb
    gN = G * Msrc / rg ** 2; g = gN if newton else glaw(gN, a0)
    rmean = 3 * g / (4 * math.pi * G * rg)
    ok = rmean <= rho_mean_m(f, zF); Rout = float(rg[np.argmax(ok)]) if ok.any() else float(rg[-1])
    keep = rg <= Rout; rg, Mb, g = rg[keep], Mb[keep], g[keep]
    phi = -np.concatenate([np.cumsum((0.5 * (g[1:] + g[:-1]) * np.diff(rg))[::-1])[::-1], [0.0]])
    if vk == 0.0:                                     # no kick: the decayed carrier stays (L388 MUTATE), = KD1's state
        Mc = cf * np.maximum(np.asarray(Mb_fun(np.asarray(r_eval, float)), float), 0.0)
        rF = float(np.interp(0.5 * Mb_tot, Mb, rg)); return dict(f_ret=1.0, vesc_rF=float(math.sqrt(-2 * np.interp(rF, rg, phi))),
                                                                sigma_rF=None, r_F=rF, R_out=Rout, Mc=Mc)
    rng = np.random.default_rng(seed)
    u = rng.random(N) * Mb_tot; r = np.interp(u, Mb, rg)
    dM = np.gradient(Mb, rg); integ = dM * g / (4 * math.pi * rg ** 2)
    Pr = np.concatenate([np.cumsum((0.5 * (integ[1:] + integ[:-1]) * np.diff(rg))[::-1])[::-1], [0.0]])
    rho = dM / (4 * math.pi * rg ** 2); s2 = np.where(rho > 0, Pr / np.maximum(rho, 1e-300), 0.0)
    s1 = np.sqrt(np.maximum(np.interp(r, rg, s2), 0.0))
    v = rng.normal(size=(N, 3)) * s1[:, None]
    n = rng.normal(size=(N, 3)); n /= np.linalg.norm(n, axis=1)[:, None]; v = v + vk * n
    E = 0.5 * (v ** 2).sum(1) + np.interp(r, rg, phi); L = r * np.hypot(v[:, 1], v[:, 2])
    ret = E < 0.0; fr = float(ret.mean()); m = cf * Mb_tot / N
    rF = float(np.median(r)); vesc = float(math.sqrt(-2 * np.interp(rF, rg, phi))); sF = float(np.sqrt(np.interp(rF, rg, s2) / 1.0))
    # orbit average of the retained daughters on a log grid
    ro = np.geomspace(max(rb_lo, 1e-3), Rout, 300); dro = np.gradient(ro); po = np.interp(ro, rg, phi)
    Mshell = np.zeros(len(ro)); Er, Lr, rr = E[ret], L[ret], r[ret]
    for i0 in range(0, len(Er), 2000):
        e_, l_ = Er[i0:i0 + 2000, None], Lr[i0:i0 + 2000, None]
        vr2 = 2 * (e_ - po[None, :]) - l_ ** 2 / ro[None, :] ** 2
        w = np.where(vr2 > 0, dro[None, :] / np.sqrt(np.maximum(vr2, 1e-12)), 0.0); ws = w.sum(1)
        bad = ws <= 0
        if bad.any():
            jj = np.clip(np.searchsorted(ro, rr[i0:i0 + 2000][bad]), 0, len(ro) - 1); w[bad] = 0.0; w[np.where(bad)[0], jj] = 1.0; ws = w.sum(1)
        Mshell += (w / ws[:, None]).sum(0) * m
    Mcum = np.cumsum(Mshell)
    Mc = np.interp(r_eval, ro, Mcum, left=0.0)
    return dict(f_ret=fr, vesc_rF=vesc, sigma_rF=sF, r_F=rF, R_out=Rout, Mc=Mc)

def rm_cells(Mb_fun, lo, hi, f, vk, r_eval, **kw):
    return {f"{p}|z{int(z)}": rm(Mb_fun, lo, hi, f, vk, p, z, r_eval, **kw) for p, z in CELLS}

# baryon profiles (kpc -> Msun)
def sparc_Mb(g):
    r = np.asarray(g["R"]) / KPC; Mb = np.maximum.accumulate(np.maximum(np.asarray(g["vb2"]) * np.asarray(g["R"]) / GSI / MS, 0.0))
    rr = np.concatenate([[0.0], r]); MM = np.concatenate([[0.0], Mb])
    return (lambda x: np.interp(x, rr, MM)), r, Mb
def hern(Mb, a): return lambda x: Mb * np.asarray(x, float) ** 2 / (np.asarray(x, float) + a) ** 2
def plum(Mb, a): return lambda x: Mb * np.asarray(x, float) ** 3 / (np.asarray(x, float) ** 2 + a ** 2) ** 1.5
def xcop_Mb(name):
    fx = XPROF[name][0]; tl = XINFO[name]["tl"]; Ml = XINFO[name]["Mlast"]
    return lambda x: np.where(np.asarray(x, float) > tl, Ml, np.asarray(fx(np.minimum(np.asarray(x, float), tl) * KPC), float))

# ------------------------------------------------------------------ KA5 (RM at v_k = 0 is KD1's state) and KA3 / KA4
gtest = GB["SP"][0]; mbf, rpt, mbp = sparc_Mb(gtest); o0 = rm(mbf, rpt[0] * 0.1, rpt[-1], "canonical", 0.0, "release", 0.0, rpt)
d5 = float(np.max(np.abs(o0["Mc"] / np.interp(rpt, np.concatenate([[0.0], rpt]), np.concatenate([[0.0], mbp])) - CF["canonical"])))
KA["KA5"] = dict(maxdiff=d5, f_ret=o0["f_ret"], ok=bool(d5 <= 1e-6 and o0["f_ret"] == 1.0))
BMAP = {}
def CAND(ft): return dict(b=BMAP.get(id(ft), 1.0), F=1.0, T=0.0)
def grade_gate(gname, f):
    fn = dict((n, fn) for n, fn, _ in GB["GATES"])[gname]
    ok, num = fn(CAND, BATT[f], A0[f]); return bool(ok), num
ka3 = 0.0
for f in FOOTS:
    BMAP.clear()
    for gname, _, _ in GB["GATES"]:
        ok, num = grade_gate(gname, f); ref = GL0["cands"]["L0"][f][gname]["num"]
        for k_ in ("Z", "rms", "mean", "R", "worst_planet_use", "cassini_use"):
            if k_ in num and k_ in ref: ka3 = max(ka3, abs(num[k_] - ref[k_]))
        if "fst0" in num: ka3 = max(ka3, *[abs(num[x]["n_pass"] - ref[x]["n_pass"]) + abs(num[x]["median_res"] - ref[x]["median_res"]) for x in ("fst0", "fst1")])
        if gname.startswith("G6"): ka3 = max(ka3, max(abs(num[c]["median_minus_anchor"] - ref[c]["median_minus_anchor"]) for c in num))
        ka3 = max(ka3, 0.0 if ok == (GL0["cands"]["L0"][f][gname]["status"] == "PASS") else 1.0)
KA["KA3"] = dict(maxdiff=ka3, ok=bool(ka3 <= 1e-9))
ka4 = {}
for f in FOOTS:
    e = NS["x_eval"](f, "baryon", NEED[f]["Xcop_f_need"]); ka4[f] = (e["mean"], e["rms"])
ref4 = {"canonical": (0.0, 0.0818), "alt": (0.0, 0.0835)}   # amendment A2: KD1's need zeroes the mean by construction
KA["KA4"] = dict(mine=ka4, ok=bool(all(abs(ka4[f][0] - ref4[f][0]) <= 1e-3 and abs(ka4[f][1] - ref4[f][1]) <= 1e-3 for f in FOOTS)))
for k in ("KA3", "KA4", "KA5"): P(f"{k}: {'PASS' if KA[k]['ok'] else 'FAIL'}  {json.dumps(J({kk: vv for kk, vv in KA[k].items() if kk != 'ok'}))[:220]}")
RES["KA"] = KA
if not all(v["ok"] for v in KA.values()):
    RES["label"] = "NO VERDICT (known answer failed)"; P("KNOWN ANSWER FAILED: stop, nothing graded."); dump(); sys.exit(2)

# ------------------------------------------------------------------ single-shell retention curve for CK3
from scipy.stats import ncx2
CURVE = {}
for vk in VK + (2000.0,):
    rows = []
    for ve in np.arange(100.0, 3001.0, 100.0):
        for lab, sg in (("sqrt6", ve / math.sqrt(6)), ("sqrt3", ve / math.sqrt(3))):
            rows.append(dict(v_esc=ve, sigma=lab, P=float(ncx2.cdf((ve / sg) ** 2, 3, (vk / sg) ** 2))))
    CURVE[f"v{int(vk)}"] = rows
RES["single_shell_curve"] = CURVE

# ================================================================== MUTATE
def xcop_F(f, v, mode):
    """per-cluster amount F_i = C_f eps(bin_i); mode central / lo / hi (v bracket); placement bracket -> lo uses the lower bin."""
    out = {}
    for name in sorted({z["name"] for z in XC}):
        pl = PLACE[name]; ks = pl["bracket"]
        vals = [eps_at(v, k, "lo" if mode == "lo" else ("hi" if mode == "hi" else "central")) for k in ks]
        e = min(vals) if mode == "lo" else (max(vals) if mode == "hi" else eps_at(v, pl["bin"]))
        out[name] = CF[f] * e
    return out
if MUT:
    M = {}
    def xcop_rm_G2(f, vk):
        BMAP.clear(); rd = {}
        for name in sorted({z["name"] for z in XC}):
            tl = XINFO[name]["tl"]; rr = np.array(sorted({zz["r_kpc"] for zz in XC if zz["name"] == name} | {tl}))
            rd[name] = dict(r=rr, **rm(xcop_Mb(name), 1.0, tl, f, vk, "release", 0.0, rr))
        for i, z in enumerate(XC):
            o = rd[z["name"]]; BMAP[id(BATT[f]["X"][i]["feat"])] = 1.0 + float(np.interp(z["r_kpc"], o["r"], o["Mc"])) / z["M_b"]
        ok, num = grade_gate("G2 X-COP", f); return ok, num, rd
    for f in FOOTS:
        # M1 (A3): v_k = 0 in CK1's own RM gives KD1's capture C_f at every X-COP point; L388's v_k = 0 runs reported only
        ok0, n0, r0 = xcop_rm_G2(f, 0.0); F0 = {n: float(o["Mc"][-1] / XINFO[n]["Mlast"]) for n, o in r0.items()}
        ok1 = all(abs(x / 4.111 - 1) <= 0.05 for x in F0.values())
        L388v0 = CF[f] * EPS0[top]
        # M2 (A3): v_k = 2000 reported; the bite is a kick above every cluster's central escape speed (20000 km/s)
        ok2k, n2k, r2k = xcop_rm_G2(f, 2000.0)
        okb, nb, rb = xcop_rm_G2(f, 20000.0)
        ok2 = all(o["f_ret"] <= 0.1 for o in rb.values()) and not okb
        ok3 = CF[f] > CAP[f]
        M[f] = dict(M1=dict(F_xcop_RM=F0, G2=dict(ok=ok0, num=n0), L388_v0_reading=L388v0, holds=bool(ok1)),
                    M2=dict(v2000=dict(G2=dict(ok=ok2k, num=n2k), f_ret={n: o["f_ret"] for n, o in r2k.items()}, vesc_rF={n: o["vesc_rF"] for n, o in r2k.items()}),
                            v20000=dict(G2=dict(ok=okb, num=nb), f_ret={n: o["f_ret"] for n, o in rb.items()}), bites=bool(ok2)),
                    M3=dict(f=CF[f], cap=CAP[f], bites=bool(ok3)))
        P(f"[{f}] M1 v_k 0 (RM): X-COP F {min(F0.values()):.4f}-{max(F0.values()):.4f} vs 4.111, G2 {n0['mean']:+.3f}/{n0['rms']:.3f} -> {'HOLDS' if ok1 else 'FAILS'}; L388 v_k 0 reading {L388v0:.4f}")
        P(f"[{f}] M2 v_k 2000 (RM, reported): f_ret " + ", ".join(f"{n} {o['f_ret']:.2f} (v_esc(r_F) {o['vesc_rF']:.0f})" for n, o in r2k.items()) + f"; G2 {'PASS' if ok2k else 'FAIL'} {n2k['mean']:+.3f}/{n2k['rms']:.3f}")
        P(f"[{f}] M2 bite v_k 20000 (RM): f_ret max {max(o['f_ret'] for o in rb.values()):.3f}; G2 {'PASS' if okb else 'FAIL'} {nb['mean']:+.3f}/{nb['rms']:.3f} -> {'BITES' if ok2 else 'NO BITE'}")
        P(f"[{f}] M3 RM kick off: f = C_f {CF[f]:.3f} > cap {CAP[f]:.3f} -> {'BITES' if ok3 else 'NO BITE'}")
    RES["MUTATE"] = M; RES["MUTATE_all"] = bool(all(M[f]["M1"]["holds"] and M[f]["M2"]["bites"] and M[f]["M3"]["bites"] for f in FOOTS))
    P(f"MUTATE: {'all hold / bite' if RES['MUTATE_all'] else 'SOMETHING FAILED -> NO VERDICT'}"); P(f"peak RSS {rss():.0f} MB"); dump(); sys.exit(0)

# ================================================================== RM runs for galaxies (cached per footing, cell, kick)
GAL = {}            # GAL[f][v][cell][key] = dict(...)
def sparc_list():
    out = []
    for g in GB["SP"]:
        mbf, r, mb = sparc_Mb(g); V = np.asarray(g["V"]) / 1e3; vf = float(np.mean(V[-3:]))
        out.append(dict(name=g["name"], fun=mbf, r=r, mb=mb, vflat=vf))
    return out
SPL = sparc_list(); TAIL = [s["name"] for s in SPL if s["vflat"] >= 250.0]
P(f"SPARC galaxies {len(SPL)}; tail (v_flat >= 250 km/s): {len(TAIL)}: {', '.join(TAIL)}")
MWB = {"canonical": 6.02e10, "alt": 5.36e10}; R0 = 8.122; VC_SLACK = {"canonical": 229.053 + 9.290 - 229.71, "alt": 229.053 + 9.290 - 222.32}
RMW = np.unique(np.concatenate([np.linspace(1.0, 30.0, 59), [R0 * 0.95, R0 * 1.05, 150.0 * 0.95, 150.0 * 1.05, 50.0 * 0.95, 50.0 * 1.05, 9.58 * 4.848e-9]]))   # A3: sorted (first run interpolated an unsorted grid)
RIN = RMW[(RMW >= 1.0) & (RMW <= 30.0)]
ELL = GB["EL"]
def kids_hosts(f):
    E_, L_ = BATT[f]["K"]; out = []
    for ft in list(E_) + list(L_):
        R = ft["r"] / KPC; Mb = ft["x"] * a0k(f) * R ** 2 / G; out.append((ft, Mb, R))
    return out

def run_galaxies(f, v):
    o = {}
    for p, z in CELLS:
        c = f"{p}|z{int(z)}"; d = {}
        for s in SPL:
            d["S|" + s["name"]] = rm(s["fun"], s["r"][0] * 0.1, s["r"][-1], f, v, p, z, s["r"])
        Mmw = MWB[f]; amw = 3.0 * (Mmw / 1e11) ** 0.3
        d["MW"] = rm(hern(Mmw, amw), 0.01, 200.0, f, v, p, z, RMW)
        for e in ELL:
            re_ = np.array([2, 4, 8]) * e["Re"]; d["E|" + e["name"]] = rm(np.vectorize(e["Mbar"]), 0.05 * e["Re"], 8 * e["Re"], f, v, p, z, re_)
        for i, (ft, Mb, R) in enumerate(kids_hosts(f)):
            a = 3.0 * (Mb / 1e11) ** 0.3; d[f"K|{i}"] = rm(hern(Mb, a), 0.01, max(10 * a, 50.0), f, v, p, z, np.array([R]))
        for cls, pts in BATT[f]["D"].items():
            for q in pts:
                ft = q["feat"]
                if ft["Mb"] is None or ft["r"] is None: continue
                rh = ft["r"] / KPC; d[f"D|{cls}|{q['name']}"] = rm(plum(ft["Mb"], rh), 0.01 * rh, 10 * rh, f, v, p, z, np.array([rh]))
        for i, q in enumerate(BATT[f]["U"]):
            ft = q["feat"]; rh = ft["r"] / KPC; d[f"U|{i}"] = rm(plum(ft["Mb"], rh), 0.01 * rh, 10 * rh, f, v, p, z, np.array([rh]))
        for name in sorted({zz["name"] for zz in XC}):
            tl = XINFO[name]["tl"]; r5 = XINFO[name]["r500"]; rr = np.array(sorted({zz["r_kpc"] for zz in XC if zz["name"] == name} | {tl, R1H, 0.25 * r5, 0.7 * r5}))
            d["X|" + name] = dict(r=rr, **rm(xcop_Mb(name), 1.0, tl, f, v, p, z, rr))
        for fst in (0, 1):
            for gp in GB["GR"]:
                p0, p1 = gp["pts"][0], gp["pts"][1]; r0_, r1_ = p0["r_kpc"], p1["r_kpc"]; M0, M1 = p0["M_gas"] * (1 + fst), p1["M_gas"] * (1 + fst)
                sl = math.log(M1 / M0) / math.log(r1_ / r0_)
                mbf = (lambda x, r0_=r0_, r1_=r1_, M0=M0, M1=M1, sl=sl: np.where(np.asarray(x, float) <= r1_, M0 * (np.asarray(x, float) / r0_) ** sl, M1))
                d[f"G|{fst}|{gp['name']}"] = dict(Mb=np.array([M0, M1]), **rm(mbf, 0.02 * r0_, r1_, f, v, p, z, np.array([r0_, r1_])))
        o[c] = d
    return o

ckpt = os.path.join(HERE, "_ck1_rm_cache.npz")
for f in FOOTS:
    GAL[f] = {}
    for v in VK:
        GAL[f][v] = run_galaxies(f, v)
        P(f"  RM {f} v{int(v)} done  [{time.time() - T0:.0f}s, rss {rss():.0f} MB]")
# L353 reading (Newtonian-only carrier, release potential, z_F 0) for the tail and MW
L353 = {}
for f in FOOTS:
    L353[f] = {}
    for v in VK:
        r_ = {}
        for s in SPL:
            if s["name"] in TAIL:
                o = rm(s["fun"], s["r"][0] * 0.1, s["r"][-1], f, v, "release", 0.0, s["r"], newton=True); r_[s["name"]] = float(np.max(o["Mc"] / s["mb"]))
        Mmw = MWB[f]; o = rm(hern(Mmw, 3.0 * (Mmw / 1e11) ** 0.3), 0.01, 200.0, f, v, "release", 0.0, RMW, newton=True)
        r_["MW_f_ret"] = o["f_ret"]; L353[f][f"v{int(v)}"] = r_
RES["reading_L353_newton_only"] = L353

# ================================================================== grading
def cellrule(oks):
    oks = list(oks)
    if all(o is True for o in oks): return "PASS"
    if all(o is False for o in oks): return "FAIL"
    return "NO VERDICT"
def fpts(o, mb): return np.asarray(o["Mc"]) / np.maximum(np.asarray(mb), 1e-30)

def sparc_set_b(f, d):
    BMAP.clear(); i = 0
    for s in SPL:
        fs = fpts(d["S|" + s["name"]], s["mb"])
        for j in range(len(s["r"])):
            BMAP[id(BATT[f]["S"][i]["feat"])] = 1.0 + fs[j]; i += 1
    assert i == len(BATT[f]["S"])

def host_rho(o, r_eval, D):
    """density of a host RM profile at D (kpc) from the +-5 % evaluation points."""
    m1 = np.interp(0.95 * D, r_eval, o["Mc"]); m2 = np.interp(1.05 * D, r_eval, o["Mc"])
    return max(m2 - m1, 0.0) / (4 / 3 * math.pi * ((1.05 * D) ** 3 - (0.95 * D) ** 3))

def xcop_grade(f, v, d, mode, shape="rm"):
    """G2 with per-cluster F_i = C_f eps (graded amount) and the cluster's RM retained shape normalised at Mb_last's radius."""
    Fi = xcop_F(f, v, mode); BMAP.clear(); rows = {}; dd = []
    for i, z in enumerate(XC):
        name = z["name"]; tl = XINFO[name]["tl"]; Ml = XINFO[name]["Mlast"]
        if shape == "rm":
            o = d["X|" + name]; rr = o["r"]; mc = np.asarray(o["Mc"])
            norm = np.interp(tl, rr, mc); sh = float(np.interp(z["r_kpc"], rr, mc) / norm) if norm > 0 else 0.0
        else:
            sh = float(SH[name][shape](np.array([z["r_kpc"] * KPC]))[0])
        md = Fi[name] * Ml * sh; BMAP[id(BATT[f]["X"][i]["feat"])] = 1.0 + md / z["M_b"]
        Mp = float(glaw(G * (z["M_b"] + md) / z["r_kpc"] ** 2, a0k(f))) * z["r_kpc"] ** 2 / G
        res = math.log10(z["M_obs"] / Mp); dd.append((z["r_kpc"] / XINFO[name]["r500"], res)); rows.setdefault(name, []).append(res)
    ok, num = grade_gate("G2 X-COP", f)
    xr = np.array([a for a, _ in dd]); rr_ = np.array([b for _, b in dd]); bins = []
    for lo, hi in zip(BINE[:-1], BINE[1:]):
        m = (xr >= lo) & (xr < hi); bins.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(rr_[m].mean()) if m.sum() else None))
    binok = all(abs(b["mean"]) <= 0.10 for b in bins if b["n"] >= 3)
    per = {n: dict(F=Fi[n], mean=float(np.mean(r)), n=len(r)) for n, r in rows.items()}
    return ok, dict(mean=num["mean"], rms=num["rms"], bins=bins, bins_ok=bool(binok), per_cluster=per)

def xcop_grade_rm(f, d):
    """A3: X-COP from CK1's own framework-native RM run: b = 1 + M_c(<r)/M_b at each X-COP point (no L388 input)."""
    BMAP.clear(); dd = []; rows = {}; per = {}
    for i, z in enumerate(XC):
        o = d["X|" + z["name"]]; mc = float(np.interp(z["r_kpc"], o["r"], o["Mc"]))
        BMAP[id(BATT[f]["X"][i]["feat"])] = 1.0 + mc / z["M_b"]
        Mp = float(glaw(G * (z["M_b"] + mc) / z["r_kpc"] ** 2, a0k(f))) * z["r_kpc"] ** 2 / G
        res = math.log10(z["M_obs"] / Mp); dd.append((z["r_kpc"] / XINFO[z["name"]]["r500"], res)); rows.setdefault(z["name"], []).append(res)
    ok, num = grade_gate("G2 X-COP", f)
    xr = np.array([a for a, _ in dd]); rr_ = np.array([b for _, b in dd]); bins = []
    for lo, hi in zip(BINE[:-1], BINE[1:]):
        m = (xr >= lo) & (xr < hi); bins.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(rr_[m].mean()) if m.sum() else None))
    for n_, r_ in rows.items():
        o = d["X|" + n_]; tl = XINFO[n_]["tl"]; r5 = XINFO[n_]["r500"]; I = XINFO[n_]
        conc = lambda fun: float(fun(np.array([0.25 * r5]))[0] / fun(np.array([0.7 * r5]))[0])
        c_rm = float(np.interp(0.25 * r5, o["r"], o["Mc"]) / np.interp(0.7 * r5, o["r"], o["Mc"]))
        per[n_] = dict(F_at_Mblast=float(np.interp(tl, o["r"], o["Mc"]) / I["Mlast"]), f_ret=o["f_ret"], vesc_rF=o["vesc_rF"], r_F=o["r_F"],
                       mean_res=float(np.mean(r_)), n=len(r_), conc_rm=c_rm, conc_gas=conc(I["fg"]), conc_hse=conc(I["fh"]), conc_stars=conc(I["fs"]))
    return ok, dict(mean=num["mean"], rms=num["rms"], bins=bins, bins_ok=bool(all(abs(b["mean"]) <= 0.10 for b in bins if b["n"] >= 3)), per_cluster=per)

def groups_grade_rm(f, d):
    BMAP.clear(); fl = {0: [], 1: []}
    for fst in (0, 1):
        for gp, gr in zip(BATT[f]["GR"][fst], GB["GR"]):
            o = d[f"G|{fst}|{gr['name']}"]
            for j, p in enumerate(gp["pts"]):
                fj = float(o["Mc"][j] / o["Mb"][j]); BMAP[id(p["feat"])] = 1.0 + fj; fl[fst].append(fj)
    ok, num = grade_gate("G3 groups", f); a0 = A0[f]; meds = {}
    for fst in (0, 1):
        dl = [math.log10(float(glaw(BMAP[id(p["feat"])] * p["feat"]["x"] * a0, a0)) / float(glaw(p["feat"]["x"] * a0, a0))) for gp in BATT[f]["GR"][fst] for p in gp["pts"]]
        meds[fst] = float(np.median(dl))
    return ok, dict(F_median={k: float(np.median(v)) for k, v in fl.items()}, **num, carrier_offset_median=meds,
                    UA1_ok=bool(all(UA1[f][0] <= m <= UA1[f][1] for m in meds.values())))

def groups_grade(f, v, mode):
    Fg = CF[f] * eps_at(v, low, mode); BMAP.clear()
    for fst in (0, 1):
        for gp in BATT[f]["GR"][fst]:
            for p in gp["pts"]: BMAP[id(p["feat"])] = 1.0 + Fg
    ok, num = grade_gate("G3 groups", f)
    # residue: the groups' median carrier offset (both f*) inside UA1's 95 % step interval
    a0 = A0[f]; meds = {}
    for fst in (0, 1):
        dl = [math.log10(float(glaw((1 + Fg) * p["feat"]["x"] * a0, a0)) / float(glaw(p["feat"]["x"] * a0, a0))) for gp in BATT[f]["GR"][fst] for p in gp["pts"]]
        meds[fst] = float(np.median(dl))
    return ok, dict(F=Fg, **num, carrier_offset_median=meds, UA1_ok=bool(all(UA1[f][0] <= m <= UA1[f][1] for m in meds.values())))

def tiny(x): return float(x)
TAB = {}; GALSUM = {}
for f in FOOTS:
    TAB[f] = {}; GALSUM[f] = {}
    for v in VK:
        R = {}; gs = {}
        # ---- G1, T, G4, G6, G5, G7, G8, MW per RM cell
        per = {k: [] for k in ("G1", "T", "G4", "G5", "G6", "G7", "G8", "MW")}; detail = {}
        for c, d in GAL[f][v].items():
            sparc_set_b(f, d); ok1, n1 = grade_gate("G1 SPARC", f); per["G1"].append(ok1)
            tail = {s["name"]: dict(fmax=float(np.max(fpts(d["S|" + s["name"]], s["mb"]))), f_ret=d["S|" + s["name"]]["f_ret"],
                                    vesc_rF=d["S|" + s["name"]]["vesc_rF"], r_F=d["S|" + s["name"]]["r_F"], vflat=s["vflat"]) for s in SPL if s["name"] in TAIL}
            okT = all(t["fmax"] <= CAP[f] for t in tail.values()); per["T"].append(okT)
            sp_med = float(np.median(np.concatenate([fpts(d["S|" + s["name"]], s["mb"]) for s in SPL])))
            # ellipticals
            BMAP.clear(); k = 0
            for e in ELL:
                fe = fpts(d["E|" + e["name"]], [e["Mbar"](m * e["Re"]) for m in (2, 4, 8)])
                for j in range(3): BMAP[id(BATT[f]["E"][k]["feat"])] = 1.0 + fe[j]; k += 1
            ok4, n4 = grade_gate("G4 ellipticals", f); per["G4"].append(ok4)
            ell_med = float(np.median([b - 1 for b in BMAP.values()]))
            # MW
            mw = d["MW"]; Mmw = MWB[f]; amw = 3.0 * (Mmw / 1e11) ** 0.3; a0 = a0k(f)
            rhoR0 = host_rho(mw, RMW, R0); dKz = 2 * 1100.0 * rhoR0 / 1e9
            McR0 = float(np.interp(R0, RMW, mw["Mc"])); MbR0 = float(hern(Mmw, amw)(R0))
            vc0 = math.sqrt(R0 * float(glaw(G * MbR0 / R0 ** 2, a0))); vc1 = math.sqrt(R0 * float(glaw(G * (MbR0 + McR0) / R0 ** 2, a0)))
            rin = RIN; Mbin = hern(Mmw, amw)(rin); Mcin = np.interp(rin, RMW, mw["Mc"])
            dlg = float(np.max(np.log10(glaw(G * (Mbin + Mcin) / rin ** 2, a0) / glaw(G * Mbin / rin ** 2, a0))))
            nuR0 = float(glaw(G * MbR0 / R0 ** 2, a0)) / (G * MbR0 / R0 ** 2)
            okMW = dKz <= 4.4 and (vc1 - vc0) <= VC_SLACK[f] and dlg <= 0.057; per["MW"].append(okMW)
            # G8: carrier inside 9.58 AU at the solar circle density
            rcas = 9.58 * 4.848e-9; fss = rhoR0 * 4 / 3 * math.pi * rcas ** 3 / 1.0
            per["G8"].append(None)
            # dSphs: own + host term (MW host for MW classical and bright M31) at D 50 and 150 kpc
            okd = []
            for D in (50.0, 150.0):
                rho_h = host_rho(mw, RMW, D); BMAP.clear(); sp_ok = sparc_set_b(f, d)
                for cls, pts in BATT[f]["D"].items():
                    for q in pts:
                        ft = q["feat"]
                        if ft["Mb"] is None or ft["r"] is None: continue
                        rh = ft["r"] / KPC; own = float(d[f"D|{cls}|{q['name']}"]["Mc"][0])
                        hostm = rho_h * 4 / 3 * math.pi * rh ** 3 if cls in ("MW classical", "bright M31", "MW ultra-faint", "M31 others") else 0.0
                        BMAP[id(ft)] = 1.0 + (own + hostm) / (ft["Mb"] / 2)
                ok6, n6 = grade_gate("G6 dSph classes", f); okd.append(ok6)
                detail[f"G6_{c}_D{int(D)}"] = {k_: dict(median_minus_anchor=w["median_minus_anchor"], ci=w["ci"]) for k_, w in n6.items()}
                if D == 150.0: m31_f = float(np.median([BMAP[id(q["feat"])] - 1 for q in BATT[f]["D"]["bright M31"] if id(q["feat"]) in BMAP]))
            per["G6"].append(True if all(okd) else (False if not any(okd) else None))
            # KiDS
            BMAP.clear()
            for i, (ft, Mb, Rk) in enumerate(kids_hosts(f)):
                BMAP[id(ft)] = 1.0 + float(d[f"K|{i}"]["Mc"][0]) / Mb
            ok7, n7 = grade_gate("G7 KiDS split", f); per["G7"].append(ok7)
            gs[c] = dict(G1=n1, tail=tail, sparc_median_f=sp_med, ell=n4, ell_median_f=ell_med, G7=n7, m31_median_f_D150=m31_f,
                         MW=dict(rho_R0_Msun_kpc3=rhoR0, dKz_over_2piG=dKz, dKz_nu_reading=dKz * nuR0, dvc_R0=vc1 - vc0, vc_slack=VC_SLACK[f],
                                 dlogg_inner_max=dlg, f_ret=mw["f_ret"], vesc_rF=mw["vesc_rF"], r_F=mw["r_F"], R_out=mw["R_out"],
                                 vesc_R0=None, f_sun_9p58AU=fss))
        # vesc at R0 (law, release cell z0) reported
        # ---- G5 UDGs: own RM + Coma-proxy host (densest X-COP-like host at 300 kpc, uniform-baryon reading, disclosed)
        okU = []
        for c, d in GAL[f][v].items():
            nm = "A2319"; fx = xcop_Mb(nm); r3 = 300.0
            rho_b = (float(fx(np.array([r3 * 1.05]))) - float(fx(np.array([r3 * 0.95])))) / (4 / 3 * math.pi * ((1.05 * r3) ** 3 - (0.95 * r3) ** 3))
            rho_c = CF[f] * eps_at(v, top, "hi") * rho_b
            BMAP.clear()
            for i, q in enumerate(BATT[f]["U"]):
                ft = q["feat"]; rh = ft["r"] / KPC; own = float(d[f"U|{i}"]["Mc"][0])
                BMAP[id(ft)] = 1.0 + (own + rho_c * 4 / 3 * math.pi * rh ** 3) / (ft["Mb"] / 2)
            ok5, n5 = grade_gate("G5 Coma UDGs", f); okU.append(ok5); gs[c]["G5"] = dict(**n5, f_median=float(np.median([b - 1 for b in BMAP.values()])))
        per["G5"] = okU
        # ---- G8 (record value; carrier inside 9.58 AU negligible)
        BMAP.clear(); ok8, n8 = grade_gate("G8 Solar System", f)
        for k_ in ("G1", "T", "G4", "G5", "G7", "MW"): R[k_] = cellrule(per[k_])
        R["G6"] = cellrule([x for x in per["G6"]]) if None not in per["G6"] else "NO VERDICT"
        R["G8"] = "PASS" if ok8 else "FAIL"
        # ---- G2 X-COP and G3 groups on the amount path (central / lo / hi), RM shape at each RM cell
        g2 = {}; g2ok = []
        for c, d in GAL[f][v].items():
            ok, num = xcop_grade_rm(f, d); g2[c] = dict(ok=ok, **num); g2ok.append(ok)
        R["G2"] = cellrule(g2ok)
        g2_L388 = {}                       # A3: L388 path, LCDM-referenced, reading only (not evidence)
        for mode in ("central", "lo", "hi"):
            ok, num = xcop_grade(f, v, GAL[f][v]["release|z0"], mode); g2_L388[mode] = dict(ok=ok, mean=num["mean"], rms=num["rms"])
        prof = {}
        for shp in ("hse", "baryon", "gas", "stars"):
            ok, num = xcop_grade(f, v, GAL[f][v]["release|z0"], "central", shape=shp); prof[shp] = dict(ok=ok, mean=num["mean"], rms=num["rms"], bins=num["bins"])
        g3 = {}; g3ok = []; ua = []
        for c, d in GAL[f][v].items():
            ok, num = groups_grade_rm(f, d); g3[c] = dict(ok=ok, **num); g3ok.append(ok); ua.append(num["UA1_ok"])
        R["G3"] = cellrule(g3ok)
        g3_L388 = {m: groups_grade(f, v, m) for m in ("central", "lo", "hi")}   # reading only
        R["Bullet"] = "OPEN (DB1 machinery > 1 GB, NA2 disclosure; L370's 0.000 was its kernel-off MUTATE)"
        R["G9"] = "PENDING GL1/GL3 (not graded; CK4 / HOLD_KERNEL_REREAD)"
        # ---- residue rows (SE2 95 % / UA1)
        IV = PB3J["footings"][f]["U"]["intervals"]; c0 = GAL[f][v]
        res_rows = {}
        res_rows["SPARC"] = cellrule([IV["SPARC"][0] <= gs[c]["sparc_median_f"] <= IV["SPARC"][1] for c in c0])
        res_rows["ellipticals"] = cellrule([IV["ellipticals"][0] <= gs[c]["ell_median_f"] <= IV["ellipticals"][1] for c in c0])
        res_rows["bright M31"] = cellrule([IV["bright M31"][0] <= gs[c]["m31_median_f_D150"] <= IV["bright M31"][1] for c in c0])
        res_rows["X-COP"] = cellrule([IV["X-COP"][0] <= np.median([q["F_at_Mblast"] for q in g2[c]["per_cluster"].values()]) <= IV["X-COP"][1] for c in g2])
        res_rows["groups"] = cellrule([IV["groups_fst0"][0] <= g3[c]["F_median"][0] <= IV["groups_fst0"][1] and IV["groups_fst1"][0] <= g3[c]["F_median"][1] <= IV["groups_fst1"][1] for c in g3])
        res_rows["groups_UA1_step"] = cellrule(ua)
        res_rows["T"] = R["T"]; res_rows["MW"] = R["MW"]
        # ---- reported row (amendment A1 (c)): trigger mass M_min on the system's own mass (1 + C_f) M_b; below it nothing is shed
        mmin = {}
        for Mmin in (1e11, 1e12):
            kept = [s_["name"] for s_ in SPL if (1 + CF[f]) * s_["mb"][-1] < Mmin]
            d = GAL[f][v]["release|z0"]; BMAP.clear(); i = 0
            for s_ in SPL:
                fs = CF[f] * np.ones(len(s_["r"])) if s_["name"] in kept else fpts(d["S|" + s_["name"]], s_["mb"])
                for j in range(len(s_["r"])): BMAP[id(BATT[f]["S"][i]["feat"])] = 1.0 + fs[j]; i += 1
            okm, nm = grade_gate("G1 SPARC", f); mmin[f"{Mmin:.0e}"] = dict(n_unshed=len(kept), G1_ok=okm, G1=nm, MW_sheds=bool((1 + CF[f]) * MWB[f] >= Mmin))
        TAB[f][f"v{int(v)}"] = dict(rows=R, Mmin_reading_release_z0=mmin, reading_L388_LCDM_referenced=dict(G2=g2_L388, G3={m: dict(ok=x[0], F=x[1]['F'], fst0=x[1]['fst0'], fst1=x[1]['fst1']) for m, x in g3_L388.items()}), residue=res_rows, G2=g2, profile_shapes_release_z0=prof, G3=g3, G8=n8, galaxies=gs)
        P(f"[{f}] v{int(v)}: " + " | ".join(f"{k} {R[k]}" for k in ("G1", "T", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "MW")) + "  || residue: " + ", ".join(f"{k} {x}" for k, x in res_rows.items()))
        cz = gs["release|z0"]
        P(f"      X-COP G2 (RM) by cell: " + "; ".join(f"{c} {g2[c]['mean']:+.3f}/{g2[c]['rms']:.3f}" for c in g2) + " | per cluster (release z0) F, f_ret, conc rm/gas/hse/stars: "
          + ", ".join(f"{n} {q['F_at_Mblast']:.2f} {q['f_ret']:.2f} {q['conc_rm']:.2f}/{q['conc_gas']:.2f}/{q['conc_hse']:.2f}/{q['conc_stars']:.2f}" for n, q in g2["release|z0"]["per_cluster"].items()))
        P(f"      G3 (RM) by cell n_pass f*0/f*1: " + "; ".join(f"{c} {g3[c]['fst0']['n_pass']}/{g3[c]['fst1']['n_pass']} (F med {g3[c]['F_median'][0]:.2f}/{g3[c]['F_median'][1]:.2f})" for c in g3)
          + f" | L388 reading G2 central {g2_L388['central']['mean']:+.3f}/{g2_L388['central']['rms']:.3f}")
        P(f"      MW (release z0): f_ret {cz['MW']['f_ret']:.3f}, v_esc(r_F {cz['MW']['r_F']:.1f} kpc) {cz['MW']['vesc_rF']:.0f}, dKz {cz['MW']['dKz_over_2piG']:.2f}, dvc {cz['MW']['dvc_R0']:.1f}, dlogg {cz['MW']['dlogg_inner_max']:.3f}; "
          f"tail fmax " + ", ".join(f"{n} {t['fmax']:.2f}" for n, t in cz["tail"].items()))
        dump()

# ------------------------------------------------------------------ labels
LAB = {}
ROWS = ("G1", "T", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "MW")
cand = []
for v in VK:
    t = f"v{int(v)}"; allp = all(TAB[f][t]["rows"][k] == "PASS" for f in FOOTS for k in ROWS)
    fails = sorted({k for f in FOOTS for k in ROWS if TAB[f][t]["rows"][k] == "FAIL"})
    nv = sorted({k for f in FOOTS for k in ROWS if TAB[f][t]["rows"][k] == "NO VERDICT"})
    win_closed = any(TAB[f][t]["rows"]["G2"] == "PASS" and (TAB[f][t]["rows"]["T"] == "FAIL" or TAB[f][t]["rows"]["MW"] == "FAIL") for f in FOOTS)
    rlab = "PASSES RESIDUE" if all(x == "PASS" for f in FOOTS for x in TAB[f][t]["residue"].values()) else "FAILS RESIDUE (" + ", ".join(sorted({k for f in FOOTS for k, x in TAB[f][t]["residue"].items() if x != "PASS"})) + ")"
    LAB[t] = dict(candidate=allp, fails=fails, no_verdict=nv, coordinator_window_closed=win_closed, residue=rlab)
    if allp: cand.append(t)
cnt = {k: sum(1 for v in VK if all(TAB[f][f"v{int(v)}"]["rows"][k] == "FAIL" for f in FOOTS)) for k in ROWS}
binding = max(ROWS, key=lambda k: (cnt[k], k in ("T", "MW")))
if cand: label = f"CANDIDATE ON G1-G8 WITH A POSTULATED KICK (G9 pending GL1/GL3) at {cand}"
elif any(LAB[t]["fails"] for t in LAB): label = f"FAILS (rows) at every v_k; binding gate {binding} (fails both footings at {cnt[binding]} of {len(VK)} kicks)"
else: label = "NO VERDICT"
RES.update(table=TAB, labels=LAB, fail_counts_both_footings=cnt, binding=binding, label=label)
P(""); P("LABEL: " + label)
for t, l in LAB.items(): P(f"  {t}: FAIL rows {l['fails']}; NO VERDICT {l['no_verdict']}; window closed by coordinator rule: {l['coordinator_window_closed']}; {l['residue']}")
P(f"peak RSS {rss():.0f} MB; runtime {time.time() - T0:.0f}s. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
dump()
