"""CFG966 -- stars vs HI inside the same dwarfs (WLM, IC 1613, DDO 210 = Aquarius, DDO 216 = Pegasus dIrr).
Criteria: FROZEN_CRITERIA.md (5ec3dc16a, committed alone before this script).  N = 4: a pointer, not a verdict.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg966.py      (CFG966_MUTATE=hi|plant_system|plant_tracer -> separate outputs).
Estimator: the record's (CFG874) Wolf r12 = (4/3) rhalf_sph, Ups_V 2, gas inside r12 (Wang+16 disc, extended root), for BOTH
tracers; HI = the authors' asymmetric-drift-corrected V_c at r12 (Oh+2015 primary; Iorio+2017, SPARC UGCA 444 brackets).
Kernel: primary nu_A = inverse of the record's AQUAL statement mu = x/(1+x); co-reading nu_e (record's stored excess).
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import csv, json, math, time, zipfile, hashlib, resource, builtins
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG966_MUTATE", ""); assert MUT in ("", "hi", "plant_system", "plant_tracer")
SUF = f"_MUTATE_{MUT}" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def rss_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
def rel(p): return os.path.relpath(p, REPO)
def sha(p): return hashlib.sha256(builtins.open(p, "rb").read()).hexdigest()

G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16; KPC = 3.0857e19; LN10 = math.log(10.0)
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOTS = ("canonical", "alt")
EFFECT = {"canonical": 0.372, "alt": 0.332}                  # CFG919 dwarf-class excess (dex, nu_e)
PLANT = 0.37; FLOOR = 0.05; CURVE_KILL = 0.15; REACH = 1.10
nu_e = lambda y: 1.0 / (-math.expm1(-math.sqrt(max(y, 1e-15))))         # CFG874, copied unchanged
nu_A = lambda y: 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / max(y, 1e-15)))     # AQUAL mu = x/(1+x), exact spherical inverse
KERNELS = (("nu_A (AQUAL, primary)", "A", nu_A), ("nu_e (record co-reading)", "e", nu_e))

F_LVD = [os.path.join(REPO, "real_research", "data", "dsph", f) for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv")]
D442 = os.path.join(LANES, "CFG442_a0_rung_expansion", "data")
F_OHROT, F_OHT2, F_OHT1 = (os.path.join(D442, f) for f in ("oh15_rotdmbar.dat", "oh15_table2.dat", "oh15_table1.dat"))
F_IO = os.path.join(LANES, "CFG449_a0_rung_iorio_edd", "data", "iorio17_finalrot.zip")
F_SP = os.path.join(REPO, "real_research", "data", "sparc_data", "UGCA444_rotmod.dat")
F_MRT = os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")
F_874 = os.path.join(LANES, "CFG874_isolated_dwarfs_pooled", "cfg874_results.json")
F_860 = os.path.join(LANES, "CFG860_stripping_vs_isolated_dwarfs", "cfg860_results.json")
F_931 = os.path.join(LANES, "CFG931_faint_rotator_discriminator", "cfg931_results.json")
INPUTS = F_LVD + [F_OHROT, F_OHT2, F_OHT1, F_IO, F_SP, F_MRT, F_874, F_860, F_931]

RES = dict(lane="CFG966", criteria="5ec3dc16a", mode=MUT or "main", inputs={rel(p): sha(p) for p in INPUTS}, checks={})
def check(name, ok, measured):
    RES["checks"][name] = dict(ok=bool(ok), measured=str(measured))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)

P("CFG966  stars vs HI inside the same dwarfs (WLM, IC 1613, DDO 210, DDO 216)" + (f"   [MUTATE {MUT}]" if MUT else ""))
P("  record estimator for both tracers; kernel primary nu_A (AQUAL mu = x/(1+x)), co-reading nu_e; kappa = 1/2 FITTED; N = 4: a pointer")
P("  inputs (sha256):")
for k, v in RES["inputs"].items(): P(f"    {v}  {k}")

# =========================================================================================================== record estimator (CFG874)
def fnum(x):
    try: return float(x)
    except (TypeError, ValueError): return None
LVD = {}
for f in F_LVD:
    for r in csv.DictReader(builtins.open(f)): LVD[r["name"]] = r

def gas_in(lHI, r12_pc, mode):                                    # CFG874, copied unchanged
    if lHI is None or mode == "zero": return 0.0
    Mg = 1.33 * 10 ** lHI
    if mode == "full": return Mg
    if mode == "half": return Mg / 2                                                   # CFG860 convention
    MHI = 10 ** lHI; RHI = 0.5 * 10 ** (0.506 * lHI - 3.293) * 1e3                     # pc
    f = lambda Rs: MHI / (2 * math.pi * Rs * Rs) * math.exp(-RHI / Rs) - 1.0
    grid = np.geomspace(1e-3 * RHI, 10 * RHI, 4000); v = [f(x) for x in grid]
    roots = [grid[i] for i in range(len(grid) - 1) if v[i] * v[i + 1] < 0]
    Rs = (max(roots) if mode == "disc" else min(roots)) if roots else RHI / 2          # disc = extended (primary); compact = bracket
    x = r12_pc / Rs
    return Mg * (1 - (1 + x) * math.exp(-x))

def record_delta(name, foot, gas="disc"):                         # CFG874 build() for one dwarf, Ups 2, nu_e (same arithmetic order)
    r = LVD[name]; a0 = A0[foot]; s = fnum(r["vlos_sigma"])
    rh = fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical")); MV = fnum(r["M_V"])
    r12_pc = (4 / 3) * rh; r12 = r12_pc * PC
    Ms = 2.0 * 10 ** (0.4 * (4.83 - MV)); Mg = gas_in(fnum(r.get("mass_HI")), r12_pc, gas)
    gb = G * (Ms / 2 + Mg) * Msun / r12 ** 2
    return math.log10(3 * (s * 1e3) ** 2 / r12 / (gb * nu_e(gb / a0)))

# =========================================================================================================== HI curve sets
OHD = {}
for l in builtins.open(F_OHT1):
    v = l.split("|"); OHD[v[0].strip()] = float(v[2])
OHT2 = {}
for l in builtins.open(F_OHT2):
    v = l.split("|"); OHT2[v[0].strip()] = dict(Rmax=float(v[1]), Vmax=float(v[3]))
OHROT = {}
for l in builtins.open(F_OHROT):
    v = l.split()
    if len(v) == 7 and v[1] == "Data":
        OHROT.setdefault(v[0], []).append([float(x) for x in v[2:]])
def oh_curve(oname):                                              # (R kpc at Oh distance, V, eV), truncated at table-2 R_max
    a = np.array(OHROT[oname]); R03, V03 = a[0, 0], a[0, 1]
    R = a[:, 2] * R03; V = a[:, 3] * V03; eV = a[:, 4] * V03
    m = R <= OHT2[oname]["Rmax"] * 1.001
    return R[m], V[m], eV[m]

ZIO = zipfile.ZipFile(F_IO)
def io_curve(fname):
    txt = ZIO.read(f"finalrot/{fname}_onlinetab.txt").decode()
    D = None; rows = []
    for l in txt.splitlines():
        if l.startswith("# Distance:"): D = float(l.split(":")[1].split()[0])
        elif l.strip() and not l.startswith("#"): rows.append([float(x) for x in l.split()])
    a = np.array(rows)
    return D, dict(R=a[:, 1], Vr=a[:, 2], eVr=a[:, 3], Va=a[:, 4], eVa=a[:, 5], Vc=a[:, 6], eVc=a[:, 7])

def sp_curve():
    D = None; rows = []
    for l in builtins.open(F_SP):
        if l.startswith("# Distance"): D = float(l.split("=")[1].split()[0])
        elif l.strip() and not l.startswith("#"): rows.append([float(x) for x in l.split()[:6]])
    return D, np.array(rows)

def at(R, Y, r):                                                  # reach rule: inside -> interp; <= 1.10 R_last -> outermost; else None
    if r < R[0] or r > REACH * R[-1]: return None
    if r <= R[-1]: return float(np.interp(r, R, Y))
    return float(Y[-1])

DW = [dict(name="WLM", oh="WLM", io="wlm", sp=True), dict(name="IC 1613", oh="IC_1613", io=None, sp=False),
      dict(name="Aquarius", oh="DDO_210", io="ddo210", sp=False), dict(name="Pegasus dIrr", oh="DDO_216", io="ddo216", sp=False)]
LABEL = {"WLM": "WLM", "IC 1613": "IC 1613", "Aquarius": "DDO 210 (Aquarius)", "Pegasus dIrr": "DDO 216 (Pegasus dIrr)"}

# =========================================================================================================== K stage
P("\n=== K stage")
KOK = []
R874 = json.load(builtins.open(F_874)); R860 = json.load(builtins.open(F_860)); R931 = json.load(builtins.open(F_931))
k1 = []
for foot in FOOTS:
    ref = [x for x in R874[foot]["primary"]["iso"] if x["name"] == "Aquarius"][0]["D"]
    k1.append(abs(record_delta("Aquarius", foot, "disc") - ref))
for foot, key in (("canonical", "d"), ("alt", "d_alt")):
    ref = [m for g in R860["members"].values() for m in g if m["name"] == "Aquarius"][0][key]
    k1.append(abs(record_delta("Aquarius", foot, "zero") - ref))
KOK.append(check("K1 record excess for Aquarius (CFG874 primary gas -0.04408/-0.08229; CFG860 zero gas +0.13177/+0.09265; nu_e)",
                 max(k1) <= 1e-9, f"max |diff| {max(k1):.1e}; canonical/alt with gas {record_delta('Aquarius','canonical'):+.5f} / "
                 f"{record_delta('Aquarius','alt'):+.5f}, zero gas {record_delta('Aquarius','canonical','zero'):+.5f} / {record_delta('Aquarius','alt','zero'):+.5f}"))
stored = {x["name"] for f in FOOTS for t in R874[f] if isinstance(R874[f][t], dict) and "iso" in R874[f][t] for x in R874[f][t]["iso"]}
stored |= {m["name"] for g in R860["members"].values() for m in g}
absent = [n for n in ("WLM", "IC 1613", "Pegasus dIrr") if n not in stored]
KOK.append(check("K2 WLM, IC 1613, Pegasus dIrr carry no stored stellar excess in the record (absent from CFG874/CFG860 stored members)",
                 len(absent) == 3, f"absent: {', '.join(absent)} (record excluded them as the rotating / gas-rich set); nothing to reproduce"))
# K3: CFG931 A1-3 UGCA 444 cells (no point cut), CFG931's loader convention
QG = {}
for l in builtins.open(F_MRT):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: QG[v[0]] = dict(inc=float(v[5]), q=int(v[17]))
        except ValueError: pass
DSP, ASP = sp_curve()
GRID = np.arange(-20.0, 10.0001, 0.5)
nu_e15 = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
gb_sp, go_sp = [], []
if QG["UGCA444"]["q"] <= 2 and QG["UGCA444"]["inc"] >= 30:
    for R, V, eV, Vg, Vd, Vb in ASP:
        if V <= 0 or R <= 0: continue
        g_b = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPC)
        if g_b <= 0: continue
        gb_sp.append(g_b); go_sp.append(V * V * 1e6 / (R * KPC))
gb_sp, go_sp = np.array(gb_sp), np.array(go_sp); kc = np.digitize(np.log10(gb_sp), GRID) - 1
k3 = []; k3s = []
for foot in FOOTS:
    d = np.log10(go_sp / (gb_sp * nu_e15(gb_sp / A0[foot])))
    for c in ("15", "16"):
        ref = R931["info"][f"UGCA444|{foot}"][c]; m = kc == int(c)
        k3.append(abs(float(np.mean(d[m])) - ref["ugca444"])); k3.append(abs(int(m.sum()) - ref["n444"]))
        k3s.append(f"{foot} [{GRID[int(c)]:.1f},{GRID[int(c)] + 0.5:.1f}) {float(np.mean(d[m])):+.5f} ({int(m.sum())} pts)")
KOK.append(check("K3 SPARC residual for UGCA 444 = CFG931 A1-3 cell means (no point cut, Ups_disk 0.5, nu_e)", max(k3) <= 1e-9,
                 f"max |diff| {max(k3):.1e}; " + "; ".join(k3s)))
k4 = []; k4s = []
for d in DW:
    R, V, eV = oh_curve(d["oh"]); v = float(np.interp(OHT2[d["oh"]]["Rmax"], R, V))
    k4.append(abs(v - OHT2[d["oh"]]["Vmax"])); k4s.append(f"{d['oh']} {v:.2f} vs {OHT2[d['oh']]['Vmax']:.1f}")
io_dev = 0.0
for fn in ("wlm", "ddo210", "ddo216", "ddo216b"):
    _, c = io_curve(fn); io_dev = max(io_dev, float(np.max(np.abs(c["Vc"] - np.sqrt(c["Vr"] ** 2 + c["Va"] ** 2)))))
KOK.append(check("K4 parse: Oh V(R_max) = table 2 within 0.6 km/s; Iorio |V_c - sqrt(V_r^2+V_a^2)| <= 0.02 km/s",
                 max(k4) <= 0.6 and io_dev <= 0.02, "; ".join(k4s) + f"; Iorio max dev {io_dev:.3f} km/s"))

# =========================================================================================================== per-dwarf computation
def dwarf_rows(foot, nu, radius="sph", primary="oh", d216="ddo216", gas="disc", v6=False, mut=""):
    a0 = A0[foot]; rows = []
    for d in DW:
        r = LVD[d["name"]]; Dl = fnum(r["distance"]) / 1e3                 # Mpc
        rh = fnum(r["rhalf_sph_physical"]) if radius == "sph" else fnum(r["rhalf_physical"])
        r12_pc = (4 / 3) * rh; r12 = r12_pc * PC; rk = r12_pc / 1e3
        s = fnum(r["vlos_sigma"]); es = 0.5 * (fnum(r["vlos_sigma_em"]) + fnum(r["vlos_sigma_ep"]))
        MV = fnum(r["M_V"]); Ms = 2.0 * 10 ** (0.4 * (4.83 - MV)); Mg = gas_in(fnum(r.get("mass_HI")), r12_pc, gas)
        gb = G * (Ms / 2 + Mg) * Msun / r12 ** 2; law = gb * nu(gb / a0)
        gs = 3 * (s * 1e3) ** 2 / r12; kin_s = 2 / LN10 * es / s
        sets = {}
        Ro, Vo, eVo = oh_curve(d["oh"]); Ro = Ro * Dl / OHD[d["oh"]]
        v, e = at(Ro, Vo, rk), at(Ro, eVo, rk)
        if v is not None: sets["Oh15"] = (v, e)
        cad = None; vr_ = None
        if d["io"]:
            fn = d216 if d["io"] == "ddo216" else d["io"]
            Di, c = io_curve(fn); Ri = c["R"] * Dl / Di
            v, e = at(Ri, c["Vc"], rk), at(Ri, c["eVc"], rk); vr_ = at(Ri, c["Vr"], rk)
            if v is not None:
                sets["Iorio17"] = (v, e); cad = 2 * math.log10(v / vr_) if vr_ and vr_ > 0 else float("inf")
        if d["sp"]:
            Rs = ASP[:, 0] * Dl / DSP; v, e = at(Rs, ASP[:, 1], rk), at(Rs, ASP[:, 2], rk)
            if v is not None: sets["SPARC"] = (v, e)
        gh = {k: (vv * 1e3) ** 2 / r12 for k, (vv, ee) in sets.items()}
        kin = {k: 2 / LN10 * ee / vv for k, (vv, ee) in sets.items()}
        if mut == "hi": gh = {k: g * 10 ** PLANT for k, g in gh.items()}
        EH = {k: math.log10(g / law) for k, g in gh.items()}
        spread = max([abs(EH[a] - EH[b]) for a in EH for b in EH] or [0.0])
        scur = max(0.5 * spread, FLOOR)
        order = ("Oh15", "Iorio17") if primary == "oh" else ("Iorio17", "Oh15")
        pset = next((k for k in order if k in sets), None)
        Es = math.log10(gs / law)
        row = dict(name=d["name"], label=LABEL[d["name"]], r12_pc=r12_pc, lg_gbar=math.log10(gb), law=law, g_star=gs,
                   E_star=Es, kin_star=kin_s, sE_star=math.hypot(kin_s, FLOOR), sets={k: dict(V=sets[k][0], eV=sets[k][1], E=EH[k]) for k in sets},
                   spread=spread, s_curve=scur, primary=pset, c_AD=cad, Vr_io=vr_, Mg=Mg, Ms2=Ms / 2)
        if pset:
            Eh = EH[pset]; kh = kin[pset]
            if mut in ("plant_system", "plant_tracer"):
                Es = PLANT; Eh = PLANT if mut == "plant_system" else 0.0
                row["E_star"] = Es
            row.update(E_HI=Eh, kin_HI=kh, sE_HI=math.sqrt(kh ** 2 + scur ** 2 + FLOOR ** 2), Delta=Es - Eh,
                       sDelta=math.sqrt(kin_s ** 2 + kh ** 2 + scur ** 2),
                       Delta_direct=math.log10(gs / gh[pset]) if not mut else None)
        else:
            row.update(E_HI=None, kin_HI=None, sE_HI=None, Delta=None, sDelta=None, Delta_direct=None)
        if v6 and "SPARC" in sets:                                    # CFG931-V3 pressure bracket on SPARC (switch 1 only)
            vv = math.sqrt(sets["SPARC"][0] ** 2 + 2 * 8.0 ** 2); row["E_SPARC_V6"] = math.log10((vv * 1e3) ** 2 / r12 / law)
        rows.append(row)
    return rows

def core(rows, drop=()):
    use = [r for r in rows if r["primary"] and r["name"] not in drop and r["E_star"] > 0 and r["E_star"] / r["sE_star"] > 2]
    nsys = sum(r["E_HI"] >= 0.5 * r["E_star"] for r in use)
    ntr = sum(r["E_HI"] < 0.5 * r["E_star"] and abs(r["E_HI"]) < 2 * r["sE_HI"] for r in use)
    if len(use) < 3: c = "NOT DIAGNOSTIC (NO LEVER)"
    elif nsys >= 3: c = "SYSTEM PROPERTY"
    elif ntr >= 3: c = "TRACER PROPERTY"
    else: c = "MIXED"
    return c, dict(n_usable=len(use), usable=[r["name"] for r in use], n_system=nsys, n_tracer=ntr)

def classify(rows, foot, v6=False):
    w = [r for r in rows if r["name"] == "WLM"][0]
    s1v = None
    if "Oh15" in w["sets"] and "SPARC" in w["sets"]:
        s1v = abs(w["sets"]["Oh15"]["E"] - (w["E_SPARC_V6"] if v6 else w["sets"]["SPARC"]["E"]))
    s1 = s1v is not None and s1v > CURVE_KILL
    ad = {r["name"]: r["c_AD"] for r in rows if r["name"] in ("Aquarius", "Pegasus dIrr")}
    s2_names = [n for n, c in ad.items() if c is not None and c > EFFECT[foot]]
    c_core, info = core(rows)
    if s1: c = "NOT DIAGNOSTIC (CURVES)"
    elif s2_names: c = "NOT DIAGNOSTIC (AD)"
    else: c = c_core
    shadow, sinfo = core(rows, drop=tuple(s2_names))
    return dict(cls=c, core=c_core, core_info=info, switch1_WLM_Oh_vs_SPARC=s1v, switch1=s1, c_AD=ad, switch2=s2_names,
                shadow=shadow, shadow_info=sinfo)

def dbar(rows):
    q = [r for r in rows if r["Delta"] is not None]
    w = np.array([1 / r["sDelta"] ** 2 for r in q]); x = np.array([r["Delta"] for r in q])
    m = float(np.sum(w * x) / np.sum(w)); s = float(1 / math.sqrt(np.sum(w)))
    rd = "tracers agree" if abs(m) < 0.10 else ("stellar estimator high" if (m > 0.20 and m / s >= 2) else "unresolved")
    return dict(N=len(q), Dbar=m, sDbar=s, unweighted=float(np.mean(x)), reading=rd, full_excess_disfavoured=bool(m + 2 * s < 0.372))

def fmt(x, f="+.3f"): return ("%" + f) % x if x is not None else "  -  "

# =========================================================================================================== main readings
P("\n=== Per-dwarf table (V0: circularised r12, Oh+2015 primary, CFG874 gas)" + (f"  [MUTATE {MUT}]" if MUT else ""))
V0 = {}
k5 = []
for foot in FOOTS:
    for kname, kk, nu in KERNELS:
        rows = dwarf_rows(foot, nu, mut=MUT); cl = classify(rows, foot); V0[f"{foot}|{kk}"] = dict(rows=rows, cls=cl)
        if not MUT: k5 += [abs(r["Delta"] - r["Delta_direct"]) for r in rows if r["Delta"] is not None]
        P(f"\n  [{foot} a0 {A0[foot]:.4e} | {kname}]")
        P(f"    {'dwarf':23s} {'r12 pc':>6s} {'lg g_bar':>8s} {'E_star':>15s} {'E_HI (set)':>24s} {'Oh15':>7s} {'Iorio17':>7s} {'SPARC':>7s} {'Delta':>15s} {'c_AD':>6s} usable")
        for r in rows:
            use = r["name"] in cl["core_info"]["usable"]
            P(f"    {r['label']:23s} {r['r12_pc']:6.0f} {r['lg_gbar']:8.2f} {r['E_star']:+7.3f} +- {r['sE_star']:.3f} "
              f"{fmt(r['E_HI']):>7s} +- {fmt(r['sE_HI'], '.3f'):>5s} ({r['primary'] or 'none':7s}) "
              f"{fmt(r['sets'].get('Oh15', {}).get('E')):>7s} {fmt(r['sets'].get('Iorio17', {}).get('E')):>7s} {fmt(r['sets'].get('SPARC', {}).get('E')):>7s} "
              f"{fmt(r['Delta']):>7s} +- {fmt(r['sDelta'], '.3f'):>5s} {fmt(r['c_AD'], '.3f'):>6s} {'yes' if use else 'no'}")
        P(f"    switch 1 (WLM Oh15 vs SPARC at r12): {fmt(cl['switch1_WLM_Oh_vs_SPARC'], '.3f')} dex (kill > {CURVE_KILL}) -> {'FIRES' if cl['switch1'] else 'no'}")
        P(f"    switch 2 (Iorio c_AD at r12 vs effect {EFFECT[foot]}): DDO 210 {fmt(cl['c_AD']['Aquarius'], '.3f')}, DDO 216 {fmt(cl['c_AD']['Pegasus dIrr'], '.3f')} dex"
          f" -> {'FIRES (' + ', '.join(LABEL[n] for n in cl['switch2']) + ')' if cl['switch2'] else 'no'}")
        ci = cl["core_info"]
        P(f"    core: usable {ci['n_usable']} ({', '.join(ci['usable']) or 'none'}), SYSTEM count {ci['n_system']}, TRACER count {ci['n_tracer']} -> {cl['core']}")
        P(f"    CLASS: {cl['cls']}     shadow (switches ignored, AD-dominated dropped; no class weight): {cl['shadow']}")

if not MUT:
    KOK.append(check("K5 identity (by construction): E_star - E_HI = log10(3 sigma^2 / V_c^2)", max(k5) <= 1e-12, f"max |diff| {max(k5):.1e} over {len(k5)} rows"))

def lane(V, kk):
    c, a = V[f"canonical|{kk}"]["cls"]["cls"], V[f"alt|{kk}"]["cls"]["cls"]
    return c if c == a else "UNDECIDED (FOOTING-SPLIT)"
LANE_A, LANE_E = lane(V0, "A"), lane(V0, "e")
flag = "KERNEL-SENSITIVE" if LANE_A != LANE_E else None
P(f"\n=== LANE CLASS (primary kernel nu_A): {LANE_A}" + (f"   [{flag}: nu_e reads {LANE_E}]" if flag else f"   (nu_e co-reading: {LANE_E})"))
DB = dbar(V0["canonical|A"]["rows"])
P(f"=== Secondary (scout NA-4 (iv); no class weight; footing- and kernel-free): D-bar = {DB['Dbar']:+.3f} +- {DB['sDbar']:.3f} dex "
  f"(N {DB['N']}; unweighted {DB['unweighted']:+.3f}) -> {DB['reading']}; full-excess estimator inflation (0.372) disfavoured: {DB['full_excess_disfavoured']}")

# =========================================================================================================== variants
VARS = [("V1 major-axis r12", dict(radius="maj")), ("V2 Iorio primary", dict(primary="io")), ("V3 DDO 216 scenario 2", dict(d216="ddo216b")),
        ("V4 gas compact root", dict(gas="compact")), ("V5 no gas", dict(gas="zero")), ("V6 SPARC + CFG931-V3 pressure term", dict(v6=True))]
RES_V = {}
if not MUT:
    P("\n=== Variants (lane class per kernel; a change from V0 marks FRAGILE)")
    for tag, kw in VARS:
        VV = {}
        for foot in FOOTS:
            for kname, kk, nu in KERNELS:
                rows = dwarf_rows(foot, nu, **kw); VV[f"{foot}|{kk}"] = dict(rows=rows, cls=classify(rows, foot, v6=kw.get("v6", False)))
        la, le = lane(VV, "A"), lane(VV, "e")
        RES_V[tag] = dict(lane_A=la, lane_e=le, per={k: v["cls"] for k, v in VV.items()},
                          rows={k: [{q: r[q] for q in ("name", "r12_pc", "E_star", "E_HI", "primary", "Delta", "sDelta", "c_AD")} for r in v["rows"]] for k, v in VV.items()})
        cA = VV["canonical|A"]
        P(f"  {tag:36s} nu_A {la:28s} nu_e {le:28s}  canonical nu_A: switch1 {fmt(cA['cls']['switch1_WLM_Oh_vs_SPARC'], '.3f')}, "
          f"c_AD 210/216 {fmt(cA['cls']['c_AD']['Aquarius'], '.2f')}/{fmt(cA['cls']['c_AD']['Pegasus dIrr'], '.2f')}, core {cA['cls']['core']}; "
          f"E_star/E_HI " + ", ".join(f"{r['name'].split()[0]} {fmt(r['E_star'], '+.2f')}/{fmt(r['E_HI'], '+.2f')}" for r in cA["rows"]))
    main_cls = lambda c: c.split(" (")[0]                       # class without its sub-label (record convention, CFG931)
    fragile = any(main_cls(v["lane_A"]) != main_cls(LANE_A) for v in RES_V.values())
    sub = [t for t, v in RES_V.items() if v["lane_A"] != LANE_A and main_cls(v["lane_A"]) == main_cls(LANE_A)]
    P(f"  -> {'FRAGILE' if fragile else 'no variant changes the primary-kernel lane class'}"
      + (f"; sub-label changes only (not FRAGILE, CFG931 convention): {', '.join(sub)}" if sub else ""))
    RES["fragile"] = fragile; RES["sublabel_changes"] = sub
    # INFO (not in criteria; no class weight): SPARC's own disc baryon model for WLM at r12
    P("\n=== INFO (not in criteria; no class weight): WLM residual at r12 with SPARC's own disc baryons (UGCA 444, Ups_disk 0.5)")
    w = LVD["WLM"]; Dl = fnum(w["distance"]) / 1e3; rk = (4 / 3) * fnum(w["rhalf_sph_physical"]) / 1e3; Rs = ASP[:, 0] * Dl / DSP
    Vg, Vd, Vo = at(Rs, ASP[:, 3], rk), at(Rs, ASP[:, 4], rk), at(Rs, ASP[:, 1], rk)
    gbS = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd)) * 1e6 / (rk * KPC); goS = Vo ** 2 * 1e6 / (rk * KPC)
    gbR = [r for r in V0["canonical|A"]["rows"] if r["name"] == "WLM"][0]["lg_gbar"]
    for foot in FOOTS:
        P(f"  {foot}: log g_bar SPARC-disc {math.log10(gbS):+.3f} vs record spherical {gbR:+.3f}; E_HI(SPARC baryons) nu_A {math.log10(goS / (gbS * nu_A(gbS / A0[foot]))):+.3f}, "
          f"nu_e {math.log10(goS / (gbS * nu_e(gbS / A0[foot]))):+.3f}")

# =========================================================================================================== MUTATE grading
exit_code = 0 if all(KOK) else 1
if MUT:
    need = {"hi": None, "plant_system": "SYSTEM PROPERTY", "plant_tracer": "TRACER PROPERTY"}[MUT]
    grades = {}
    for key, v in V0.items():
        foot, kk = key.split("|"); nu = dict((k_, n_) for _, k_, n_ in KERNELS)[kk]
        if MUT == "hi":
            base = core(dwarf_rows(foot, nu))[0]
            if base == "TRACER PROPERTY": grades[key] = dict(base=base, mut=v["cls"]["core"], ok=v["cls"]["core"] == "SYSTEM PROPERTY")
            else: grades[key] = dict(base=base, mut=v["cls"]["core"], ok=None)
        else:
            grades[key] = dict(mut=v["cls"]["core"], ok=v["cls"]["core"] == need)
    P("\n=== MUTATE grading (decision core; switches reported above, not applied)")
    for key, g in grades.items():
        st = "n/a (main core not TRACER: no stellar lever to flip)" if g["ok"] is None else ("BITES" if g["ok"] else "TOOTHLESS")
        P(f"  {key:12s} " + (f"main core {g['base']:28s} " if "base" in g else "") + f"mutated core {g['mut']:28s} -> {st}")
    graded = [g["ok"] for g in grades.values() if g["ok"] is not None]
    ok = all(graded) if graded else None
    RES["mutate_grades"] = grades; RES["mutate_ok"] = ok
    if MUT == "hi" and ok is None:
        P("  MUTATE hi: not applicable on this data (no stellar lever); the plant_system / plant_tracer modes carry the control")
    else:
        P(f"  MUTATE {MUT}: {'PASS' if ok else 'FAIL'}")
        if not ok: exit_code = 1

RES.update(lane_class=LANE_A, lane_class_nu_e=LANE_E, flag=flag, secondary=DB,
           V0={k: dict(cls=v["cls"], rows=v["rows"]) for k, v in V0.items()}, variants=RES_V,
           K_all_pass=all(KOK), runtime_s=round(time.time() - T0, 1), peak_rss_mb=round(rss_mb(), 1), exit=exit_code)
P(f"\n  done [{time.time() - T0:.1f} s, peak RSS {rss_mb():.0f} MB], exit {exit_code}.  kappa = 1/2 FITTED; footings never pooled; N = 4 is a pointer, not a verdict; not theory closed.")
def jdef(o):
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)
json.dump(RES, builtins.open(os.path.join(HERE, f"cfg966_results{SUF}.json"), "w"), indent=1, default=jdef)
builtins.open(os.path.join(HERE, f"cfg966{SUF}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(exit_code)
