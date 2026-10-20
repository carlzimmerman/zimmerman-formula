"""CFG877 -- finite cold clump (no new parameter) on all six dwarf/SPARC samples.  Criteria: FROZEN_CRITERIA.md (37fd77c59).
Run: python3 cfg877.py  (CFG877_MUTATE=inf|tenth).  kappa = 1/2 FITTED; not theory closed."""
import os, glob, csv, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG877_MUTATE", ""); assert MUT in ("", "inf", "tenth"); SUF = f"_MUTATE_{MUT}" if MUT else ""; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, KPC, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; RC = 104.0
nu = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
def fnum(x):
    try:
        v = float(x); return None if math.isnan(v) else v
    except (TypeError, ValueError): return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
J = lambda *p: json.load(open(os.path.join(LANES, *p)))
R870 = J("CFG870_cored_component_joint", "cfg870_results.json"); R876 = J("CFG876_cold_floor_universality", "cfg876_results.json")
R28 = J("CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json"); R59 = J("CFG859_extra_speed_vs_ufds", "cfg859_results.json")
R24 = J("CFG824_dwarf_age_fossil", "cfg824_results.json")["rows"]; R27 = J("CFG827_dwarf_age_sfh_ml", "cfg827_results.json")["rows"]
Q = {}
for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: Q[v[0]] = dict(inc=float(v[5]), q=int(v[17]), Mb=(0.5 * float(v[7]) + 1.33 * float(v[13])) * 1e9)
        except ValueError: pass

def Mx(r_pc, Vx, Mcl):                                   # kg
    r = r_pc * PC; return min((Vx * 1e3) ** 2 * r ** 3 / (G * (r ** 2 + (RC * PC) ** 2)), Mcl)
def sx2(r_pc, Vx, Mcl): return G * Mx(r_pc, Vx, Mcl) / (3 * r_pc * PC) / 1e6          # (km/s)^2
def law_cfg870(nm, a0, ups):                             # CFG870's dwarf(): sigma_law (km/s), r12 (pc); no gas
    L = LVD[nm]; rh = (4 / 3) * (fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical"))) * PC
    M = ups * 10 ** (0.4 * (4.83 - fnum(L["M_V"]))); gN = G * (M / 2) * Msun / rh ** 2
    return math.sqrt(float(gN * nu(gN / a0)) * rh / 3) / 1e3, rh / PC
def gas_in(lHI, r12_pc):                                 # CFG874/876
    if lHI is None: return 0.0
    Mg = 1.33 * 10 ** lHI; MHI = 10 ** lHI; RHI = 0.5 * 10 ** (0.506 * lHI - 3.293) * 1e3
    f = lambda Rs: MHI / (2 * math.pi * Rs * Rs) * math.exp(-RHI / Rs) - 1.0
    grid = np.geomspace(1e-3 * RHI, 10 * RHI, 4000); v = [f(x) for x in grid]
    roots = [grid[i] for i in range(len(grid) - 1) if v[i] * v[i + 1] < 0]
    Rs = max(roots) if roots else RHI / 2; x = r12_pc / Rs
    return Mg * (1 - (1 + x) * math.exp(-x))
def law_cfg876(nm, a0, ups):
    L = LVD[nm]; rh_pc = fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical")); r12_pc = (4 / 3) * rh_pc; r12 = r12_pc * PC
    Ms = ups * 10 ** (0.4 * (4.83 - fnum(L["M_V"]))); gN = G * (Ms / 2 + gas_in(fnum(L.get("mass_HI")), r12_pc)) * Msun / r12 ** 2
    return math.sqrt(float(gN * nu(gN / a0)) * r12 / 3 / 1e6), r12_pc

def group_E(items, a0, Vx, Mcl, lawf, nb=4000, fails=False):
    eps, nf, rows = [], 0, []
    for it in items:
        nm, so = it["name"], it["s"]; sl, r12 = lawf(nm, a0, it["ups"]); sp = math.sqrt(sl ** 2 + sx2(r12, Vx, Mcl))
        eps.append(math.log(so / sp)); row = dict(name=nm, r12=r12, sigma=so, pred=sp, law=sl)
        if fails:
            sl1, _ = lawf(nm, a0, 1.0); sp1 = math.sqrt(sl1 ** 2 + sx2(r12, Vx, Mcl)); e = it["ep"] if so < sp1 else it["em"]
            row["z1"] = (so - sp1) / e; nf += row["z1"] <= -3
        rows.append(row)
    eps = np.array(eps); rng = np.random.default_rng(877); bs = [rng.choice(eps, len(eps)).mean() for _ in range(nb)]
    return dict(N=len(eps), E=float(eps.mean()), se=float(np.std(bs)), N_fail=int(nf), rows=rows)
def sparc(a0, Vx, Mcl):
    gal = []
    for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
        nm = os.path.basename(fn).replace("_rotmod.dat", ""); g = Q.get(nm)
        if not g or g["q"] > 2 or g["inc"] < 30 or g["Mb"] > 3e9: continue
        d_ = []
        for l in open(fn):
            if l.startswith("#") or not l.strip(): continue
            R, V, eV, Vg, Vd, Vb = [float(t) for t in l.split()[:6]]
            if V <= 0 or R <= 0 or eV / V >= 0.10: continue
            gbar = (Vg * abs(Vg) + 0.5 * Vd * abs(Vd) + 0.7 * Vb * abs(Vb)) * 1e6 / (R * KPC)
            if gbar <= 0: continue
            gl = float(gbar * nu(gbar / a0)); go = V * V * 1e6 / (R * KPC); gx = G * Mx(R * 1000, Vx, Mcl) / (R * KPC) ** 2
            d_.append(math.log10(go / gl) - math.log10((gl + gx) / gl))
        if d_: gal.append(float(np.median(d_)))
    D = np.array(gal); rng = np.random.default_rng(870); bs = [rng.choice(D, len(D)).mean() for _ in range(2000)]
    return float(D.mean()), float(np.std(bs)), len(D)

P("CFG877  finite cold clump, no new parameter, on all samples" + (f"  [MUTATE {MUT}]" if MUT else ""))
RES = dict(lane="CFG877", mutate=MUT or None)
for foot in ("canonical", "alt"):
    a0 = A0[foot]; Vx = R870[foot]["Vx"]; sig = Vx / math.sqrt(2); Mcl = 81 * (sig * 1e3) ** 4 / (4 * G * a0)
    if MUT == "inf": Mcl = float("inf")
    if MUT == "tenth": Mcl *= 0.1
    rt = G * Mcl / (Vx * 1e3) ** 2 / PC if math.isfinite(Mcl) else float("inf")
    rows = R28[f"{foot}|nu_e"]["rows"]; host = lambda nm: LVD[nm].get("host") or "field"
    mwc = [dict(name=r["name"], s=R24[r["name"]]["so"], ups=R27[r["name"]]["ups"]) for r in rows if host(r["name"]) == "mw" and r["delta"] > 0.05]
    oth = [dict(name=r["name"], s=R24[r["name"]]["so"], ups=R27[r["name"]]["ups"]) for r in rows if host(r["name"]) in ("m_031", "field")]
    ufd = [dict(name=nm, s=fnum(LVD[nm]["vlos_sigma"]), ups=2.20) for nm in R59[f"{foot}|secondary (literature sigma)"]["names"]]
    def oos(big):
        out = []
        for x in R876[foot]["primary B" if big else "small (r12<312)"]["rows"]:
            L = LVD[x["name"]]; s = fnum(L["vlos_sigma"])
            out.append(dict(name=x["name"], s=s, ups=2.0, em=fnum(L.get("vlos_sigma_em")) or 0.2 * s, ep=fnum(L.get("vlos_sigma_ep")) or 0.2 * s))
        return out
    if foot == "canonical" and not MUT:          # K1 with M_cl -> inf
        k_t2 = group_E(oth, a0, Vx, float("inf"), law_cfg870, nb=10)["E"]; k_b = group_E(oos(True), a0, Vx, float("inf"), law_cfg876, nb=10)["E"]
        d1, d2 = abs(k_t2 - R870[foot]["m31_field_E"]), abs(k_b - R876[foot]["primary B"]["E"]); RES["K1"] = [d1, d2]
        P(f"  K1 (M_cl -> inf): CFG870 T2 |diff| {d1:.1e}, CFG876 primary |diff| {d2:.1e} -> {'PASS' if max(d1, d2) < 1e-9 else 'FAIL'}")
    P(f"\n  [{foot}] V_x {Vx:.3f} km/s, sigma {sig:.2f} km/s, M_cl = {Mcl / Msun:.3e} Msun, cap radius r_t = G M_cl/V_x^2 = {rt:.0f} pc")
    grp = {"MW classical (calib)": group_E(mwc, a0, Vx, Mcl, law_cfg870), "M31 + field (T2)": group_E(oth, a0, Vx, Mcl, law_cfg870),
           "UFDs (T3)": group_E(ufd, a0, Vx, Mcl, law_cfg870), "large out-of-sample": group_E(oos(True), a0, Vx, Mcl, law_cfg876, fails=True),
           "small out-of-sample": group_E(oos(False), a0, Vx, Mcl, law_cfg876)}
    D, sD, NG = sparc(a0, Vx, Mcl)
    for k, g in grp.items():
        P(f"    {k:22s} N {g['N']:2d}  E = {g['E']:+.3f} +- {g['se']:.3f} ({g['E']/g['se']:+.1f} se)" + (f"  N_fail {g['N_fail']}" if k.startswith("large") else ""))
    P(f"    SPARC small rotators   N {NG}  D = {D:+.3f} +- {sD:.3f}")
    for x in sorted(grp["large out-of-sample"]["rows"], key=lambda q: q["z1"])[:5]:
        P(f"      worst large: {x['name']:16s} r12 {x['r12']:5.0f}  sigma {x['sigma']:5.2f}  pred {x['pred']:5.2f}  law {x['law']:5.2f}  z@Ups1 {x['z1']:+.1f}")
    ok_d = abs(D) < 0.05 and abs(D) <= 2 * sD; zs = {k: g["E"] / g["se"] for k, g in grp.items()}; nf = grp["large out-of-sample"]["N_fail"]
    if any(z >= 3 for z in zs.values()): cls = "FAILS-UNDER"
    elif any(z <= -3 for z in zs.values()) or nf >= 2 or D <= -0.05: cls = "FAILS-OVER"
    elif all(abs(z) < 2 for z in zs.values()) and nf < 2 and ok_d: cls = "FINITE CLUMP HOLDS"
    else: cls = "PARTIAL (" + ", ".join(k for k, z in zs.items() if abs(z) >= 2) + ")"
    RES[foot] = dict(Vx=Vx, sigma=sig, Mcl_Msun=Mcl / Msun, rt_pc=rt, groups={k: {kk: vv for kk, vv in g.items()} for k, g in grp.items()},
                     sparc=dict(D=D, se=sD, N=NG, ok=ok_d), cls=cls)
    P(f"    -> {cls}")
cc, ca = RES["canonical"]["cls"], RES["alt"]["cls"]; overall = cc if cc == ca else f"{cc} (alt {ca})"
P(f"\n  CLASS: {overall}")
if MUT:
    ok = (cc == "FAILS-OVER") if MUT == "inf" else (cc != "FINITE CLUMP HOLDS"); RES["mutate_ok"] = ok
    P(f"  MUTATE-{MUT}: {'control behaves as required' if ok else 'CONTROL FAILED'}")
RES["cls"] = overall
json.dump(RES, open(os.path.join(HERE, f"cfg877_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg877{SUF}.out"), "w").write("\n".join(OUT) + "\n")
