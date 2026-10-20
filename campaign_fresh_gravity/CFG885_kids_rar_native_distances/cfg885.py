"""CFG885 -- the KiDS lensing RAR results (CFG829/840/849/850/851) without B21's LCDM distances.
Criteria: FROZEN_CRITERIA.md (10838b3c7, committed alone before this script).
B21 (Brouwer+21) converted shear to ESD with Sigma_crit from flat LCDM (Om 0.2793, H0 70).  g_bar is distance-free at fixed
angle; g_obs -> T g_obs with T = (h/0.70)/<r>, r = Sigma_crit,nat^-1 / Sigma_crit,fid^-1 over lens-source pairs (per g_bar point).
The lanes' loaders / amplitude / calibration code is exec'd from their files unchanged; `load` is wrapped (g_obs*T, C*T T^T).
Run: OMP_NUM_THREADS=1 python3 cfg885.py   (CFG885_MUTATE=1: T = 1.3 on every dataset; outputs *_MUTATE).
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, json, math, glob, itertools, numpy as np
from scipy.optimize import minimize_scalar
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
EXT = os.path.join(os.path.dirname(REPO), "_external_data")
MUT = os.environ.get("CFG885_MUTATE") == "1"
for v in ("CFG829_MUTATE", "CFG840_MUTATE", "CFG849_MUTATE", "CFG850_MUTATE", "CFG851_MUTATE"):
    os.environ.pop(v, None)                                   # the exec'd definitions must never run in their own MUTATE mode
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

# ------------------------------------------------------------------ the lanes' code, exec'd unchanged (definitions only)
def defs(lane, fname, marker):
    path = os.path.join(LANES, lane, fname); src = open(path).read()
    assert marker in src, (fname, marker)
    ns = {"__file__": path, "__name__": "cfg885_" + fname[:-3]}; exec(compile(src.split(marker)[0], fname, "exec"), ns); return ns
N829 = defs("CFG829_lensing_low_g_vs_dwarf_excess", "cfg829.py", 'P("CFG829  KiDS')
N840 = defs("CFG840_cfg829_robustness", "cfg840.py", 'P("CFG840  robustness')
N849 = defs("CFG849_structure_vs_colour_lensing", "cfg849.py", 'P("CFG849  structure')
N850 = defs("CFG850_red_split_mstar_systematic", "cfg850.py", 'P("CFG850  red/spheroidal')
N851 = defs("CFG851_spheroidal_excess_law", "cfg851.py", 'P("CFG851  one')
assert not (N829["MUT"] or N840["MUT"] or N849["MUT"] or N850["MUT"] or N851["MUT"])
BASE_LOAD, amp, nu_e, nu_s, A0, A_DW = N829["load"], N829["amp"], N829["nu_e"], N829["nu_s"], N829["A0"], N829["A_DW"]
SETS, W, WC = N829["SETS"], N829["W"], N829["WC"]
_cache = {}
def base_load(esd, cov, binmin=None):                         # memoised call of cfg829.load (values identical; copies returned)
    k = (esd, cov, binmin)
    if k not in _cache: _cache[k] = BASE_LOAD(esd, cov, binmin)
    gb, go, C = _cache[k]; return gb.copy(), go.copy(), C.copy()
def make_load(tmap):
    """tmap(esd_filename, gbar_array) -> T per point (None = exactly B21's numbers)."""
    def load(esd, cov, binmin=None):
        gb, go, C = base_load(esd, cov, binmin)
        if tmap is None: return gb, go, C
        T = np.asarray(tmap(esd, gb), float); return gb, go * T, C * np.outer(T, T)
    return load

# ------------------------------------------------------------------ the lanes' main statistics (classification lines verbatim)
def run829(load):
    R = dict(window=W, calib=WC, A_dwarf=A_DW)
    for foot in ("canonical", "alt"):
        for kn, nu in (("nu_e", nu_e), ("nu_simple", nu_s)):
            if foot == "alt" and kn == "nu_simple": continue
            for name, (f, c, bm) in SETS.items():
                gb, go, C = load(f, c, bm); gl = gb * nu(gb / A0[foot])
                a, ac = amp(gb, go, C, gl, W), amp(gb, go, C, gl, WC)
                if a is None: continue
                if name.startswith("blue") and kn == "nu_e":
                    holds = abs(a["A"] - 1) < 2 * a["sA"] and (A_DW - a["A"]) >= 3 * a["sA"]
                    shape = a["A"] >= 2.0 and (a["A"] - 1) >= 3 * a["sA"]
                    R["cls" if foot == "canonical" else "cls_alt"] = "LAW HOLDS AT LOW g" if holds else ("LAW-SHAPE" if shape else "INTERMEDIATE")
                    if foot == "canonical": R["k1"] = ac
                R[f"{foot}|{kn}|{name}"] = dict(window=a, calib=ac)
    k1 = R["k1"]; R["k1_pass"] = abs(math.log10(max(k1["A"], 1e-3)) - 0.04) <= 3 * k1["sA"] / (k1["A"] * math.log(10))
    return R
def run840(load):
    N840["load"] = load; run = N840["run"]; res = dict(variants={}); fails = []
    for name, ds, win, foot, gs in N840["V"]:
        a = run(ds, win, foot, gs)
        if a is None: fails.append(name + " (no data)"); continue
        ok = abs(a["A"] - 1) < 2 * a["sA"] and (A_DW - a["A"]) >= 3 * a["sA"]
        if not ok: fails.append(name)
        res["variants"][name] = dict(A=a["A"], sA=a["sA"], n=a["n"], ok=ok)
    g, k = run(N840["GAMA"], N840["W0"]), run(N840["ALLK"], N840["W0"])
    z = (g["A"] - k["A"]) / math.hypot(g["sA"], k["sA"]) if g and k else float("nan")
    res["V4"] = dict(gama=g and dict(A=g["A"], sA=g["sA"], n=g["n"]), kids_all=dict(A=k["A"], sA=k["sA"]), z=z)
    res["cls"] = "ROBUST" if not fails else "FRAGILE"; res["fails"] = fails
    res["min_excl"] = min((A_DW - v["A"]) / v["sA"] for v in res["variants"].values())
    return res
def run849(load):
    res = {}
    for foot in ("canonical", "alt"):
        A = {}
        for k, (f, c, bm) in N849["B"].items():
            gb, go, C = load(f, c, bm); gl = gb * nu_e(gb / A0[foot]); a = amp(gb, go, C, gl, N849["W"]); A[k] = (a["A"], a["sA"])
        dc, sc = A["red"][0] - A["blue"][0], math.hypot(A["red"][1], A["blue"][1]); ds, ss = A["sph n>2"][0] - A["disc n<2"][0], math.hypot(A["sph n>2"][1], A["disc n<2"][1])
        s1 = math.hypot(sc, ss)
        if ds >= 3 * ss and dc >= 3 * sc and abs(ds - dc) < s1: cls = "BOTH / DEGENERATE"
        elif ds >= 3 * ss and ds >= dc: cls = "STRUCTURE CARRIES IT"
        elif dc >= 3 * sc and dc > ds + s1: cls = "COLOUR CARRIES IT"
        else: cls = "NO SPLIT"
        res[foot] = dict(A={k: list(v) for k, v in A.items()}, d_colour=[dc, sc], d_sersic=[ds, ss], cls=cls)
    res["cls"] = res["canonical"]["cls"]; return res
def run850(load):
    N850["load"] = load; Af = N850["A"]; rows = {}
    for foot in ("canonical", "alt"):
        for sr, sb in N850["VAR"]:
            r, b, s, d = Af("red", foot, sr), Af("blue", foot, sb), Af("sph", foot, sr), Af("disc", foot, sb)
            z1 = (r["A"] - b["A"]) / math.hypot(r["sA"], b["sA"]); z2 = (s["A"] - d["A"]) / math.hypot(s["sA"], d["sA"])
            rows[f"{foot}|{sr}|{sb}"] = dict(A_red=r["A"], A_blue=b["A"], z_colour=z1, A_sph=s["A"], A_disc=d["A"], z_sersic=z2)
    res = dict(rows=rows)
    for foot in ("canonical", "alt"):
        z123, z20 = rows[f"{foot}|0.123|0.0"]["z_colour"], rows[f"{foot}|0.2|0.0"]["z_colour"]
        res["cls" if foot == "canonical" else "cls_alt"] = "SPLIT SURVIVES" if (z123 >= 3 and z20 >= 2) else ("SPLIT IS M*" if z123 < 2 else "WEAKENED")
    return res
def run851(load):
    N851["load"] = load; calibrate, predict, R28 = N851["calibrate"], N851["predict"], N851["R28"]; res = {}
    for foot in ("canonical", "alt"):
        key = "canonical|nu_e" if foot == "canonical" else "alt|nu_e"
        dw = [r for r in R28[key]["rows"] if r["lgbar"] < -11.9]; dobs = np.array([r["delta"] for r in dw])
        for shift in (0.123, 0.0):
            cal = calibrate(N851["RED"], shift, foot)
            pr = np.array([predict(cal, r["lgbar"]) for r in dw])
            prl = np.mean([cal["b_lo"] * max(0, cal["lgd"] - r["lgbar"]) for r in dw]); prh = np.mean([cal["b_hi"] * max(0, cal["lgd"] - r["lgbar"]) for r in dw])
            sp = 0.5 * abs(prh - prl); so = float(np.std(dobs, ddof=1) / math.sqrt(len(dobs))); diff = float(dobs.mean() - pr.mean()); z = diff / math.hypot(so, sp)
            und = cal["b_lo"] <= 0 and cal["b_hi"] > 1
            cls = "NOT DIAGNOSTIC" if und else ("UNIFIED" if abs(z) < 2 else ("DSPHS ABOVE" if z >= 2 else "DSPHS BELOW"))
            res[f"{foot}|shift{shift}"] = dict(cal=cal, N_dw=len(dw), d_obs=float(dobs.mean()), d_pred=float(pr.mean()), se_obs=so, se_pred=sp, z=z, cls=cls)
    res["blue_b"] = calibrate(N851["BLUE"], 0.0, "canonical"); res["cls"] = res["canonical|shift0.123"]["cls"]
    return res
def run_all(load):
    return {"829": run829(load), "840": run840(load), "849": run849(load), "850": run850(load), "851": run851(load)}

# ------------------------------------------------------------------ K1: T = 1 reproduces every committed number
def cmp(ref, mine, path, bad, worst):
    if isinstance(ref, dict):
        for k, v in ref.items():
            if k in ("lane", "mutate"): continue
            if k not in mine: bad.append(path + "/" + k + " (missing)"); continue
            cmp(v, mine[k], path + "/" + k, bad, worst)
    elif isinstance(ref, (list, tuple)):
        if len(ref) != len(mine): bad.append(path + " (length)"); return
        for i, (a, b) in enumerate(zip(ref, mine)): cmp(a, b, f"{path}[{i}]", bad, worst)
    elif isinstance(ref, str) or isinstance(ref, bool) or ref is None:
        if ref != mine: bad.append(f"{path}: {ref!r} != {mine!r}")
    else:
        d = abs(float(ref) - float(mine)); worst[0] = max(worst[0], d)
        if not d < 1e-9: bad.append(f"{path}: {ref} vs {mine} (diff {d:.2e})")
COMMITTED = {"829": ("CFG829_lensing_low_g_vs_dwarf_excess", "cfg829_results.json"), "840": ("CFG840_cfg829_robustness", "cfg840_results.json"),
             "849": ("CFG849_structure_vs_colour_lensing", "cfg849_results.json"), "850": ("CFG850_red_split_mstar_systematic", "cfg850_results.json"),
             "851": ("CFG851_spheroidal_excess_law", "cfg851_results.json")}
P("CFG885  KiDS lensing RAR results with framework-native distances" + ("  [MUTATE: T = 1.3 on every dataset]" if MUT else ""))
P("  criteria 10838b3c7; lanes' code exec'd unchanged; both footings (canonical 9.3603e-11, alt 1.1312e-10), never pooled")
REF = run_all(make_load(None))
K1 = {}
for lane, (d, f) in COMMITTED.items():
    ref = json.load(open(os.path.join(LANES, d, f))); bad, worst = [], [0.0]
    cmp(ref, REF[lane], "CFG" + lane, bad, worst); K1[lane] = dict(ok=not bad, max_abs_diff=worst[0], problems=bad[:5])
K1_ok = all(v["ok"] for v in K1.values())
P("\n  K1 (T = 1 vs committed JSON): " + "  ".join(f"CFG{k} {'PASS' if v['ok'] else 'FAIL'} (max |d| {v['max_abs_diff']:.1e})" for k, v in K1.items()))
for k, v in K1.items():
    for b in v["problems"]: P(f"     CFG{k} problem: {b}")

# ------------------------------------------------------------------ distances (h-free, units of c/H0) and Sigma_crit^-1
ZG = np.linspace(0.0, 6.0, 30001)
def chi_fn(om, orad=0.0):
    f = 1.0 / np.sqrt(om * (1 + ZG) ** 3 + orad * (1 + ZG) ** 4 + (1.0 - om - orad))
    c = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(ZG))]); return lambda z: np.interp(z, ZG, c)
def omr(h): return 2.469e-5 / h ** 2 * (1 + 0.2271 * 3.046)          # CFG681's radiation density, at the bracket's h
def sinv(chi, zl, zs):                                             # proportional to Sigma_crit^-1 (physical, D_l D_ls / D_s)
    cl, cs = chi(zl), chi(zs); return np.where(zs > zl, cl * (cs - cl) / np.maximum(cs, 1e-30) / (1 + zl), 0.0)
# K2: distances vs analytic forms, and against astropy (independent code)
k2 = {}
for z in (0.3, 1.0, 3.0):
    k2[f"EdS z{z}"] = abs(chi_fn(1.0)(z) / (2 * (1 - 1 / math.sqrt(1 + z))) - 1); k2[f"Lambda z{z}"] = abs(chi_fn(0.0)(z) / z - 1)
try:
    from astropy.cosmology import FlatLambdaCDM
    cf, cn = FlatLambdaCDM(H0=70, Om0=0.2793, Tcmb0=0), FlatLambdaCDM(H0=70, Om0=0.3085, Tcmb0=0)
    ch_f, ch_n = chi_fn(0.2793), chi_fn(0.3085); dev = 0.0
    for zl, zs in ((0.15, 0.6), (0.3, 0.9), (0.45, 1.1)):
        ra = (cn.angular_diameter_distance(zl).value * cn.angular_diameter_distance_z1z2(zl, zs).value / cn.angular_diameter_distance(zs).value) / \
             (cf.angular_diameter_distance(zl).value * cf.angular_diameter_distance_z1z2(zl, zs).value / cf.angular_diameter_distance(zs).value)
        dev = max(dev, abs(float(sinv(ch_n, zl, zs) / sinv(ch_f, zl, zs)) / ra - 1))
    k2["astropy r(zl,zs)"] = dev
except Exception as e:
    k2["astropy r(zl,zs)"] = float("nan"); P(f"  (astropy check unavailable: {e})")
zz = np.linspace(0.05, 1.0, 20); DA = chi_fn(0.3085)(zz) / (1 + zz); DL = chi_fn(0.3085)(zz) * (1 + zz)
k2["g_bar identity (by construction)"] = float(np.max(np.abs((DL / DA) ** 2 / (1 + zz) ** 4 - 1)))
K2_ok = all((v < 1e-6) for k, v in k2.items() if not k.startswith("g_bar")) and k2["g_bar identity (by construction)"] < 1e-12

# ------------------------------------------------------------------ inputs: KiDS-1000 SOM n(z) and the lens reconstruction
fn = glob.glob(os.path.join(EXT, "cfg592_work", "kids", "*", "data_fits", "xipm_KIDS1000_*.fits"))[0]
from astropy.io import fits
with fits.open(fn) as F:
    nzt = F["NZ_SOURCE"].data; hdr = F["NZ_SOURCE"].header
    ZLO, ZHI = np.array(nzt["Z_LOW"], float), np.array(nzt["Z_HIGH"], float); NZ = [np.array(nzt[f"BIN{i+1}"], float) for i in range(5)]
    NGAL = np.array([float(hdr[f"NGAL_{i+1}"]) for i in range(5)])
ZB_EDGES = [(0.1, 0.3), (0.3, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.2)]
LZ = np.load(os.path.join(REPO, "real_research", "data", "lensing_rar", "lr_lenses.npz"))
LZz, LZM, LZlogM, LZtyp = LZ["z"], LZ["Mgal"], LZ["logM"], LZ["typ"]
K3 = dict(nz_bins=len(NZ), nz_nonneg=all(bool(np.all(n >= 0)) and n.sum() > 0 for n in NZ), ngal=NGAL.tolist(), n_lens=int(len(LZz)),
          n_typ0=int((LZtyp == 0).sum()), n_typ1=int((LZtyp == 1).sum()), n_dwarf_proxy=int((LZlogM < 10.0).sum()),
          z_lens=[float(LZz.min()), float(np.median(LZz)), float(LZz.max())])
K3_ok = K3["nz_bins"] == 5 and K3["nz_nonneg"] and K3["n_lens"] == 181477 and K3["n_typ0"] == 93398 and K3["n_typ1"] == 88079
P(f"  K2 distances: " + ", ".join(f"{k} {v:.1e}" for k, v in k2.items()) + f" -> {'PASS' if K2_ok else 'FAIL'}")
P(f"  K3 inputs: 5 SOM n(z) bins (NGAL {', '.join(f'{x:.3f}' for x in NGAL)}), {K3['n_lens']} lenses ({K3['n_typ0']} typ0 / {K3['n_typ1']} typ1; "
  f"dwarf proxy logM<10: {K3['n_dwarf_proxy']}), lens z {K3['z_lens'][0]:.2f}/{K3['z_lens'][1]:.2f}/{K3['z_lens'][2]:.2f} -> {'PASS' if K3_ok else 'FAIL'}")

# source models: lists of (zs array, weight array, cut function(zl) -> per-point multiplier)
def src_S1():
    out = []
    for b, (lo, hi) in enumerate(ZB_EDGES):
        sub = (np.arange(10) + 0.5) / 10
        zs = (ZLO[:, None] + (ZHI - ZLO)[:, None] * sub[None, :]).ravel(); w = np.repeat(NZ[b] / NZ[b].sum() / 10, 10)
        frac = lambda zl, lo=lo, hi=hi: float(np.clip((hi - max(lo, zl + 0.2)) / (hi - lo), 0.0, 1.0))
        out.append((zs, w * NGAL[b], lambda zl, zs=zs, frac=frac: frac(zl)))
    return out
def src_S2():
    out = []
    for b, (lo, hi) in enumerate(ZB_EDGES):
        zs = lo + (hi - lo) * (np.arange(200) + 0.5) / 200; w = np.full(200, NGAL[b] / 200)
        out.append((zs, w, lambda zl, zs=zs: (zs > zl + 0.2).astype(float)))
    return out
SRC = {"S1": src_S1(), "S2": src_S2()}
ZLG = np.linspace(0.05, 0.6, 221)
def s2_tables(om_fid, om_nat, orad_nat, smodel, orad_fid=0.0):
    cf, cn = chi_fn(om_fid, orad_fid), chi_fn(om_nat, orad_nat); S2, S2r = np.zeros(len(ZLG)), np.zeros(len(ZLG))
    for i, zl in enumerate(ZLG):
        for zs, w, cut in SRC[smodel]:
            m = w * cut(zl); a, b = sinv(cf, zl, zs), sinv(cn, zl, zs); S2[i] += np.sum(m * a * a); S2r[i] += np.sum(m * a * b)
    return S2, S2r
GM_MPC2 = 6.67430e-11 * 1.98841e30 / 3.085677581e22 ** 2             # G Msun / Mpc^2 in m s^-2 -> R^2 [Mpc^2] = GM_MPC2 * M / g
SUBSET = {"Fig-8_RAR-KiDS-isolated_Colorbin_1.txt": LZtyp == 0, "Fig-8_RAR-KiDS-isolated_Colorbin_2.txt": LZtyp == 1,
          "Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt": LZtyp == 0, "Fig-8_RAR-KiDS-isolated_Sersicbin_2.txt": LZtyp == 1,
          "Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt": np.ones(len(LZz), bool), "Fig-10_RAR-KiDS-isolated-dwarfs_Nobins.txt": LZlogM < 10.0,
          "Fig-4-C1_RAR-GAMA-isolated_Nobins.txt": np.ones(len(LZz), bool)}
FALLBACK = set()
def r_L1(esd, gb, S2, S2r, om_fid):
    m = SUBSET[esd]; zl, M = LZz[m], LZM[m]; da2 = (chi_fn(om_fid)(zl) / (1 + zl)) ** 2
    s2, s2r = np.interp(zl, ZLG, S2), np.interp(zl, ZLG, S2r); q = math.exp(float(np.median(np.diff(np.log(gb))))); out = []
    for g in gb:
        lo, hi = GM_MPC2 * M / (g * math.sqrt(q)), GM_MPC2 * M / (g / math.sqrt(q))   # R^2 at the bin's upper / lower g_bar edge
        area = np.maximum(0.0, np.minimum(hi, 3.0 ** 2) - np.maximum(lo, 0.03 ** 2))
        if area.sum() <= 0: area = M.copy(); FALLBACK.add((esd, float(g)))
        a = area / da2; out.append(float(np.sum(a * s2r) / np.sum(a * s2)))
    return np.array(out)
DATASETS = sorted(SUBSET)
LAB = {"Fig-8_RAR-KiDS-isolated_Colorbin_1.txt": "blue", "Fig-8_RAR-KiDS-isolated_Colorbin_2.txt": "red", "Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt": "disc",
       "Fig-8_RAR-KiDS-isolated_Sersicbin_2.txt": "sph", "Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt": "all", "Fig-10_RAR-KiDS-isolated-dwarfs_Nobins.txt": "dwarfs",
       "Fig-4-C1_RAR-GAMA-isolated_Nobins.txt": "GAMA"}
GB = {e: base_load(e, *{"Fig-8_RAR-KiDS-isolated_Colorbin_1.txt": ("Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0),
                        "Fig-8_RAR-KiDS-isolated_Colorbin_2.txt": ("Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5),
                        "Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt": ("Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 0.0),
                        "Fig-8_RAR-KiDS-isolated_Sersicbin_2.txt": ("Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 2.0),
                        "Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt": ("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", None),
                        "Fig-10_RAR-KiDS-isolated-dwarfs_Nobins.txt": ("Fig-10_RAR-KiDS-isolated-dwarfs_covmatrix.txt", None),
                        "Fig-4-C1_RAR-GAMA-isolated_Nobins.txt": ("Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt", None)}[e])[0] for e in DATASETS}
def tmaps(h, om_nat, lens, smodel, om_fid=0.2793, orad_fid=0.0, rad=True):
    S2, S2r = s2_tables(om_fid, om_nat, omr(h) if rad else 0.0, smodel, orad_fid)
    if lens == "L1": rr = {e: r_L1(e, GB[e], S2, S2r, om_fid) for e in DATASETS}
    else:
        zl = {"L2": 0.15, "L3": 0.25, "L4": 0.35}[lens]; r0 = float(np.interp(zl, ZLG, S2r) / np.interp(zl, ZLG, S2)); rr = {e: np.full(len(GB[e]), r0) for e in DATASETS}
    return {e: (h / 0.70) / rr[e] for e in DATASETS}
def tfun(maps):
    def tm(esd, gb):
        assert len(gb) == len(GB[esd]) and np.allclose(gb, GB[esd], rtol=0, atol=0); return maps[esd]
    return tm
def wmean(maps, e): m = (GB[e] >= W[0]) & (GB[e] < W[1]); return float(np.mean(maps[e][m])) if m.any() else float("nan")
# K2 continued: T = 1 when native = fiducial, and the radiation term's size
t_id = tmaps(0.70, 0.2793, "L1", "S1", rad=False); k2["T(native=fid) - 1"] = max(float(np.max(np.abs(v - 1))) for v in t_id.values())
t_r1, t_r0 = tmaps(0.70, 0.3085, "L1", "S1", rad=True), tmaps(0.70, 0.3085, "L1", "S1", rad=False)
rad_eff = max(float(np.max(np.abs(t_r1[e] / t_r0[e] - 1))) for e in DATASETS)
t_rf = tmaps(0.70, 0.3085, "L1", "S1", orad_fid=omr(0.70)); rad_fid = max(float(np.max(np.abs(t_rf[e] / t_r1[e] - 1))) for e in DATASETS)
K2_ok = K2_ok and k2["T(native=fid) - 1"] < 1e-12
P(f"  K2 T(native = fiducial) - 1 = {k2['T(native=fid) - 1']:.1e}; radiation in native changes T by {rad_eff:.1e}, in fiducial by {rad_fid:.1e} "
  f"(< 1e-4 required: {'yes' if max(rad_eff, rad_fid) < 1e-4 else 'NO'}) -> K2 {'PASS' if K2_ok else 'FAIL'}")

# ------------------------------------------------------------------ extraction of tracked quantities
AKEYS = [("blue", "blue (u-r<2.5)"), ("red", "red (u-r>2.5)"), ("all", "all isolated"), ("dwarf", "isolated dwarfs")]
def summary(R):
    s = {}
    for foot in ("canonical", "alt"):
        for short, name in AKEYS:
            a = R["829"][f"{foot}|nu_e|{name}"]["window"]; s[f"A_{short}|{foot}"] = (a["A"], a["sA"])
        s[f"excl_blue|{foot}"] = (A_DW - s[f"A_blue|{foot}"][0]) / s[f"A_blue|{foot}"][1]
        for sh in ("0.123", "0.0"):
            c = R["851"][f"{foot}|shift{sh}"]; s[f"b|{foot}|{sh}"] = c["cal"]["b"]; s[f"lgd|{foot}|{sh}"] = c["cal"]["lgd"]; s[f"z851|{foot}|{sh}"] = c["z"]
        s[f"zsplit850|{foot}"] = R["850"]["rows"][f"{foot}|0.123|0.0"]["z_colour"]
        s[f"zcol849|{foot}"] = R["849"][foot]["d_colour"][0] / R["849"][foot]["d_colour"][1]
    s["min_excl840"] = R["840"]["min_excl"]
    s["classes"] = {"829 canonical": R["829"]["cls"], "829 alt": R["829"]["cls_alt"], "840": R["840"]["cls"], "849 canonical": R["849"]["canonical"]["cls"],
                    "849 alt": R["849"]["alt"]["cls"], "850 canonical": R["850"]["cls"], "850 alt": R["850"]["cls_alt"],
                    **{f"851 {f}|{sh}": R["851"][f"{f}|shift{sh}"]["cls"] for f in ("canonical", "alt") for sh in ("0.123", "0.0")}}
    s["k1_829_calib_pass"] = R["829"]["k1_pass"]
    return s
S0 = summary(REF)
# sigma(log g_dagger) at T = 1: profile Delta chi2 = 1 over b (same chi2 as cfg851.calibrate; computed here, declared)
def lgd_interval(shift, foot):
    gb, go, C = make_load(None)(*N851["RED"]); gbs = gb * 10 ** shift; gl = gbs * nu_e(gbs / A0[foot]); Ci = np.linalg.inv(C)
    def chi2(b, lgd):
        d = b * np.maximum(0.0, lgd - np.log10(gbs)); r = go - gl * 10 ** d; return float(r @ Ci @ r)
    grid = np.arange(-13.0, -4.0 + 1e-9, 0.01); prof = np.array([minimize_scalar(lambda b: chi2(b, l), bounds=(0.0, 1.5), method="bounded", options=dict(xatol=1e-7)).fun for l in grid])
    c0 = min(REF["851"][f"{foot}|shift{shift}"]["cal"]["chi2"], float(prof.min())); ok = grid[prof <= c0 + 1.0]
    return dict(lo=float(ok.min()), hi=float(ok.max()), prof_min=float(prof.min()), hits_edge=bool(ok.max() >= grid[-1] - 1e-9 or ok.min() <= grid[0] + 1e-9))
LGDI = {f"{f}|{sh}": lgd_interval(float(sh), f) for f in ("canonical", "alt") for sh in ("0.123", "0.0")}
BI = {f"{f}|{sh}": (REF["851"][f"{f}|shift{sh}"]["cal"]["b_lo"], REF["851"][f"{f}|shift{sh}"]["cal"]["b_hi"]) for f in ("canonical", "alt") for sh in ("0.123", "0.0")}
P("\n  T = 1 reference (= the lanes' committed numbers):")
for foot in ("canonical", "alt"):
    P(f"    [{foot}] " + "  ".join(f"A_{k} {S0[f'A_{k}|{foot}'][0]:.3f}+-{S0[f'A_{k}|{foot}'][1]:.3f}" for k, _ in AKEYS) +
      f"  excl {S0[f'excl_blue|{foot}']:.1f}  split850 {S0[f'zsplit850|{foot}']:.2f}  b {S0[f'b|{foot}|0.123']:.4f} lgd {S0[f'lgd|{foot}|0.123']:.3f} "
      f"(1sig {LGDI[f'{foot}|0.123']['lo']:.2f}..{LGDI[f'{foot}|0.123']['hi']:.2f}{' EDGE' if LGDI[f'{foot}|0.123']['hits_edge'] else ''})")
P("    classes: " + "; ".join(f"{k}: {v}" for k, v in S0["classes"].items()))

def moves(s):
    """tracked amplitudes: list of (name, delta/sigma, moved>=1sigma)"""
    out = []
    for foot in ("canonical", "alt"):
        for k, _ in AKEYS:
            a0, s0 = S0[f"A_{k}|{foot}"]; out.append((f"A_{k} {foot}", (s[f"A_{k}|{foot}"][0] - a0) / s0, abs(s[f"A_{k}|{foot}"][0] - a0) >= s0))
        key = f"{foot}|0.123"; b0 = S0[f"b|{key}"]; bl, bh = BI[key]; b = s[f"b|{key}"]
        out.append((f"b {foot}", (b - b0) / (0.5 * (bh - bl)), not (bl <= b <= bh)))
        l0 = S0[f"lgd|{key}"]; li = LGDI[key]; l = s[f"lgd|{key}"]; half = (li["hi"] - l0) if l >= l0 else (l0 - li["lo"])
        out.append((f"log g_dagger {foot}", (l - l0) / half if half > 0 else float("inf"), not (li["lo"] <= l <= li["hi"])))
    return out
def flips(s): return [k for k, v in s["classes"].items() if v != S0["classes"][k]]

LOG_A0 = {f: math.log10(A0[f]) for f in A0}
sfx = "_MUTATE" if MUT else ""
RES = dict(lane="CFG885", criteria="10838b3c7", mutate=MUT, K1=K1, K1_ok=K1_ok, K2=k2, K2_ok=K2_ok, radiation_effect=dict(native=rad_eff, fiducial=rad_fid),
           K3=K3, K3_ok=K3_ok, reference=S0, lgd_1sigma_T1=LGDI, b_1sigma_T1={k: list(v) for k, v in BI.items()})
if MUT:
    # ---------------------------------------------------------------- MUTATE: T = 1.3 everywhere
    Rm = run_all(make_load(lambda esd, gb: np.full(len(gb), 1.3))); Sm = summary(Rm)
    chk = {}
    rat = [Sm[f"A_{k}|{f}"][0] / S0[f"A_{k}|{f}"][0] for k, _ in AKEYS for f in ("canonical", "alt")]
    chk["every A x1.3"] = max(abs(x / 1.3 - 1) for x in rat) < 1e-9
    chk["CFG829 blue canonical -> INTERMEDIATE"] = Sm["classes"]["829 canonical"] == "INTERMEDIATE"
    chk["CFG849/850 splits unchanged"] = all(abs(Sm[f"zsplit850|{f}"] - S0[f"zsplit850|{f}"]) < 1e-9 and abs(Sm[f"zcol849|{f}"] - S0[f"zcol849|{f}"]) < 1e-9 for f in ("canonical", "alt")) \
        and all(Sm["classes"][k] == S0["classes"][k] for k in ("849 canonical", "849 alt", "850 canonical", "850 alt"))
    chk["CFG851 b unchanged (0.005)"] = all(abs(Sm[f"b|{f}|0.123"] - S0[f"b|{f}|0.123"]) <= 0.005 for f in ("canonical", "alt"))
    chk["CFG851 lgd shift = log10(1.3)/b (0.05 dex)"] = all(abs((Sm[f"lgd|{f}|0.123"] - S0[f"lgd|{f}|0.123"]) - math.log10(1.3) / S0[f"b|{f}|0.123"]) <= 0.05 for f in ("canonical", "alt"))
    fl = flips(Sm); cls = "CHANGED" if fl else ("SHIFTED, SAME CLASS" if any(m[2] for m in moves(Sm)) else "ROBUST")
    chk["CFG885 class CHANGED"] = cls == "CHANGED"
    P("\n  MUTATE T = 1.3:")
    for foot in ("canonical", "alt"):
        P(f"    [{foot}] " + "  ".join(f"A_{k} {Sm[f'A_{k}|{foot}'][0]:.3f}+-{Sm[f'A_{k}|{foot}'][1]:.3f}" for k, _ in AKEYS) +
          f"  split850 {Sm[f'zsplit850|{foot}']:.2f}  b {Sm[f'b|{foot}|0.123']:.4f} lgd {Sm[f'lgd|{foot}|0.123']:.3f}  z851 {Sm[f'z851|{foot}|0.123']:+.2f}")
    P("    classes: " + "; ".join(f"{k}: {v}" for k, v in Sm["classes"].items()))
    P("    flips: " + (", ".join(f"{k} {S0['classes'][k]} -> {Sm['classes'][k]}" for k in fl) or "none"))
    for k, v in chk.items(): P(f"    {'PASS' if v else 'FAIL'}  {k}")
    P(f"\n  CLASS (MUTATE): {cls}  -> MUTATE {'BITES as required' if all(chk.values()) else 'FAILS (see above)'}")
    RES.update(mutate_summary=Sm, mutate_checks=chk, cls=cls, flips=fl, mutate_ok=all(chk.values()))
else:
    # ---------------------------------------------------------------- the 72-point native bracket
    H, OMN, LENS, SM = (0.674, 0.70, 0.73), (0.3010, 0.3085, 0.3160), ("L1", "L2", "L3", "L4"), ("S1", "S2")
    PTS = []; worst = {}
    P("\n  native bracket (fiducial Om 0.2793): window-mean T per dataset, then the tracked numbers")
    P("    h      Om_nat  lens src | T blue  T red  T all  T dw  T GAMA | A_blue  A_red  A_all  A_dw (canonical) | excl  split850  lgd(can)  z851 | flips")
    for h, om, L, S in itertools.product(H, OMN, LENS, SM):
        maps = tmaps(h, om, L, S); R = run_all(make_load(tfun(maps))); s = summary(R); mv = moves(s); fl = flips(s)
        tw = {e: wmean(maps, e) for e in DATASETS}; tr = (min(float(v.min()) for v in maps.values()), max(float(v.max()) for v in maps.values()))
        PTS.append(dict(h=h, om_nat=om, lens=L, src=S, T_window=tw, T_range=tr, summary=s, moves=mv, flips=fl))
        for name, d, moved in mv:
            if name not in worst or abs(d) > abs(worst[name][0]): worst[name] = (d, moved, f"h {h} Om {om} {L} {S}")
        if L == "L1":
            P(f"    {h:.3f}  {om:.4f}  {L}  {S}  | {tw['Fig-8_RAR-KiDS-isolated_Colorbin_1.txt']:.4f} {tw['Fig-8_RAR-KiDS-isolated_Colorbin_2.txt']:.4f} "
              f"{tw['Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt']:.4f} {tw['Fig-10_RAR-KiDS-isolated-dwarfs_Nobins.txt']:.4f} {tw['Fig-4-C1_RAR-GAMA-isolated_Nobins.txt']:.4f} | "
              f"{s['A_blue|canonical'][0]:.3f}  {s['A_red|canonical'][0]:.3f}  {s['A_all|canonical'][0]:.3f}  {s['A_dwarf|canonical'][0]:.3f} | "
              f"{s['excl_blue|canonical']:.1f}  {s['zsplit850|canonical']:.2f}  {s['lgd|canonical|0.123']:.2f}  {s['z851|canonical|0.123']:+.2f} | {','.join(fl) or '-'}")
    allflips = sorted({(k, p["summary"]["classes"][k], f"h {p['h']} Om {p['om_nat']} {p['lens']} {p['src']}") for p in PTS for k in p["flips"]})
    moved = sorted({n for p in PTS for n, d, m in p["moves"] if m})
    cls = "CHANGED" if allflips else ("SHIFTED, SAME CLASS" if moved else "ROBUST")
    def rng(key, foot=None):
        v = [p["summary"][key] if not isinstance(p["summary"][key], (list, tuple)) else p["summary"][key][0] for p in PTS]; return (min(v), max(v))
    P("\n  ranges over all 72 points (canonical | alt):")
    for k, _ in AKEYS:
        P(f"    A_{k:6s} {rng(f'A_{k}|canonical')[0]:.3f}..{rng(f'A_{k}|canonical')[1]:.3f} (T=1 {S0[f'A_{k}|canonical'][0]:.3f}+-{S0[f'A_{k}|canonical'][1]:.3f})"
          f"  |  {rng(f'A_{k}|alt')[0]:.3f}..{rng(f'A_{k}|alt')[1]:.3f} (T=1 {S0[f'A_{k}|alt'][0]:.3f}+-{S0[f'A_{k}|alt'][1]:.3f})")
    for key, lab in (("excl_blue", "blue dwarf-x2.75 exclusion (sigma)"), ("zsplit850", "CFG850 red/blue split @+0.123 (sigma)"), ("zcol849", "CFG849 colour split (sigma)")):
        P(f"    {lab:40s} {rng(key + '|canonical')[0]:.2f}..{rng(key + '|canonical')[1]:.2f} (T=1 {S0[key + '|canonical']:.2f})  |  "
          f"{rng(key + '|alt')[0]:.2f}..{rng(key + '|alt')[1]:.2f} (T=1 {S0[key + '|alt']:.2f})")
    for f in ("canonical", "alt"):
        P(f"    CFG851 [{f}, +0.123] b {rng(f'b|{f}|0.123')[0]:.4f}..{rng(f'b|{f}|0.123')[1]:.4f} (T=1 {S0[f'b|{f}|0.123']:.4f}, 1sig {BI[f'{f}|0.123'][0]}-{BI[f'{f}|0.123'][1]});"
          f"  log g_dagger {rng(f'lgd|{f}|0.123')[0]:.2f}..{rng(f'lgd|{f}|0.123')[1]:.2f} (T=1 {S0[f'lgd|{f}|0.123']:.2f}, 1sig {LGDI[f'{f}|0.123']['lo']:.2f}..{LGDI[f'{f}|0.123']['hi']:.2f});"
          f"  dSph z {rng(f'z851|{f}|0.123')[0]:+.2f}..{rng(f'z851|{f}|0.123')[1]:+.2f} (T=1 {S0[f'z851|{f}|0.123']:+.2f})")
    P(f"    CFG840 min exclusion over variants {rng('min_excl840')[0]:.1f}..{rng('min_excl840')[1]:.1f} (T=1 {S0['min_excl840']:.1f})")
    tw_all = {e: (min(p["T_window"][e] for p in PTS), max(p["T_window"][e] for p in PTS)) for e in DATASETS}
    P("    window-mean T: " + "; ".join(f"{LAB[e]} {v[0]:.4f}..{v[1]:.4f}" for e, v in tw_all.items()))
    P(f"    per-point T over all files/points: {min(p['T_range'][0] for p in PTS):.4f}..{max(p['T_range'][1] for p in PTS):.4f}; fallback points (no lens inside 0.03-3 Mpc): {len(FALLBACK)}")
    P("\n  largest move of each tracked amplitude (in its own T=1 sigma):")
    for n, (d, m, where) in worst.items(): P(f"    {n:24s} {d:+.2f} sigma at {where}{'   >= 1 sigma' if m else ''}")
    # g_dagger ~ a0 flag (secondary)
    gd = [p["summary"]["lgd|canonical|0.123"] - LOG_A0["canonical"] for p in PTS]; flag = "STABLE" if max(abs(x) for x in gd) <= 0.1 else "DISTANCE-DEPENDENT"
    P(f"\n  g_dagger ~ a0 flag (canonical, M*-corrected): log g_dagger - log a0 in {min(gd):+.2f}..{max(gd):+.2f} (T=1 {S0['lgd|canonical|0.123'] - LOG_A0['canonical']:+.2f}) -> {flag}")
    # reported only: fiducial Om envelope
    P("\n  reported only -- fiducial Om envelope (h 0.70, Om_nat 0.3085, L1/S1):")
    FENV = {}
    for omf in (0.25, 0.27, 0.2793, 0.30, 0.32):
        maps = tmaps(0.70, 0.3085, "L1", "S1", om_fid=omf); s = summary(run_all(make_load(tfun(maps)))); fl = flips(s)
        FENV[str(omf)] = dict(T_window={e: wmean(maps, e) for e in DATASETS}, A_blue=s["A_blue|canonical"], A_red=s["A_red|canonical"], A_all=s["A_all|canonical"],
                             lgd=s["lgd|canonical|0.123"], flips=fl)
        P(f"    Om_fid {omf:.4f}: T(all) {wmean(maps, 'Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt'):.4f}  A_blue {s['A_blue|canonical'][0]:.3f}  A_red {s['A_red|canonical'][0]:.3f}  "
          f"A_all {s['A_all|canonical'][0]:.3f}  lgd {s['lgd|canonical|0.123']:.2f}  flips {','.join(fl) or 'none'}")
    P("\n  classification flips: " + ("; ".join(f"{k} -> {c} at {w}" for k, c, w in allflips) if allflips else "none at any of the 72 points"))
    P("  amplitudes moving >= 1 sigma somewhere: " + (", ".join(moved) if moved else "none"))
    P(f"\n  CLASS: {cls}" + (f"  (moved >= 1 sigma: {', '.join(moved)})" if cls.startswith("SHIFTED") else ""))
    P(f"  controls: K1 {'PASS' if K1_ok else 'FAIL'}, K2 {'PASS' if K2_ok else 'FAIL'}, K3 {'PASS' if K3_ok else 'FAIL'}")
    RES.update(points=PTS, worst={k: list(v) for k, v in worst.items()}, flips=[list(x) for x in allflips], moved=moved, cls=cls, gdagger_flag=flag,
               gdagger_minus_a0=[min(gd), max(gd)], T_window_range=tw_all, fallback_points=sorted(FALLBACK), fiducial_envelope=FENV)
P("\n  kappa = 1/2 fitted; cold energy mass required; not theory closed; cannot favour the framework over LCDM.")
json.dump(RES, open(os.path.join(HERE, f"cfg885_results{sfx}.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (bool(o) if isinstance(o, np.bool_) else str(o)))
open(os.path.join(HERE, f"cfg885{sfx}.out"), "w").write("\n".join(OUT) + "\n")
