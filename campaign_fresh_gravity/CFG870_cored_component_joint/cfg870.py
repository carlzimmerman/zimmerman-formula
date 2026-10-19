"""CFG870 -- joint consistency of the cored extra cold component.  Criteria: FROZEN_CRITERIA.md (976af111d).
Run: python3 cfg870.py (CFG870_MUTATE=1: r_c = 1 kpc).  kappa = 1/2 FITTED; not theory closed."""
import os, glob, csv, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG870_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, KPC, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
RC = 1000.0 if MUT else 104.0
nu = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
def fnum(x):
    try: return float(x)
    except: return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
R27 = json.load(open(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")))["rows"]
R24 = json.load(open(os.path.join(LANES, "CFG824_dwarf_age_fossil", "cfg824_results.json")))["rows"]
R28 = json.load(open(os.path.join(LANES, "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))
R59 = json.load(open(os.path.join(LANES, "CFG859_extra_speed_vs_ufds", "cfg859_results.json")))
Q = {}
for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: Q[v[0]] = dict(inc=float(v[5]), q=int(v[17]), Mb=(0.5 * float(v[7]) + 1.33 * float(v[13])) * 1e9)
        except ValueError: pass
def dwarf(nm, a0, ups):
    L = LVD[nm]; rh = (4 / 3) * (fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical"))) * PC
    M = ups * 10 ** (0.4 * (4.83 - fnum(L["M_V"]))); gN = G * (M / 2) * Msun / rh ** 2
    return math.sqrt(float(gN * nu(gN / a0)) * rh / 3) / 1e3, rh / PC
fcore = lambda rpc: rpc ** 2 / (rpc ** 2 + RC ** 2)
def mean_E(items, a0, Vx):
    E = []
    for nm, so, ups in items:
        sl, rpc = dwarf(nm, a0, ups); E.append(math.log(so / math.sqrt(sl ** 2 + fcore(rpc) * Vx ** 2 / 3)))
    E = np.array(E); return float(E.mean()), float(E.std(ddof=1) / math.sqrt(len(E))), E
def sparc(a0, Vx):
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
            gl = float(gbar * nu(gbar / a0)); go = V * V * 1e6 / (R * KPC); rpc = R * 1000
            gx = (Vx * 1e3) ** 2 * (R * KPC) / ((R * KPC) ** 2 + (RC * PC) ** 2)
            d_.append(math.log10(go / gl) - math.log10((gl + gx) / gl))
        if d_: gal.append(float(np.median(d_)))
    D = np.array(gal); rng = np.random.default_rng(870); bs = [rng.choice(D, len(D)).mean() for _ in range(2000)]
    return float(D.mean()), float(np.std(bs)), len(D)
P("CFG870  cored extra cold component: joint consistency" + (f"  [MUTATE r_c = {RC:.0f} pc]" if MUT else f"  (r_c = {RC:.0f} pc)"))
RES = dict(lane="CFG870", mutate=MUT, rc=RC)
for foot in ("canonical", "alt"):
    a0 = A0[foot]; rows = R28[f"{foot}|nu_e"]["rows"]
    host = lambda nm: LVD[nm].get("host") or "field"
    mw = [(r["name"], R24[r["name"]]["so"], R27[r["name"]]["ups"]) for r in rows if host(r["name"]) == "mw" and r["delta"] > 0.05]
    lv = []
    for nm, so, ups in mw:
        sl, rpc = dwarf(nm, a0, ups)
        if so > sl: lv.append(0.5 * math.log10(3 * (so ** 2 - sl ** 2) / fcore(rpc)))
    Vx = 10 ** float(np.mean(lv))
    D, sD, NG = sparc(a0, Vx); t1 = abs(D) < 0.05 and abs(D) <= 2 * sD
    oth = [(r["name"], R24[r["name"]]["so"], R27[r["name"]]["ups"]) for r in rows if host(r["name"]) in ("m_031", "field")]
    e2, s2, _ = mean_E(oth, a0, Vx); t2 = abs(e2) < 2 * s2
    ufd = []
    for nm in R59[f"{foot}|secondary (literature sigma)"]["names"]:
        so = fnum(LVD[nm]["vlos_sigma"]); ufd.append((nm, so, 2.20))
    e3, s3, _ = mean_E(ufd, a0, Vx); t3 = abs(e3) < 2 * s3
    cl = [(nm, so, ups) for nm, so, ups in mw]; ec, _, Ec = mean_E(cl, a0, Vx); el, _, El = mean_E(cl, a0, 0.0)
    cls = "JOINT FIT HOLDS" if (t1 and t2 and t3) else ("SPARC + UFD ONLY" if (t1 and t3) else ("BREAKS" if not t1 else "OTHER"))
    RES[foot] = dict(Vx=Vx, N_cal=len(lv), sparc_D=D, sparc_sD=sD, T1=t1, m31_field_E=e2, m31_field_se=s2, T2=t2, ufd_E=e3, ufd_se=s3, T3=t3,
                     classical_rms_cored=float(np.sqrt(np.mean(Ec ** 2))), classical_rms_law=float(np.sqrt(np.mean(El ** 2))), cls=cls)
    P(f"\n  [{foot}] V_x refit with core on MW classical dSphs (N {len(lv)}): {Vx:.2f} km/s")
    P(f"     T1 SPARC (N {NG}): D = {D:+.3f} +- {sD:.3f} -> {'pass' if t1 else 'FAIL'}")
    P(f"     T2 M31 + field (N {len(oth)}): E = {e2:+.3f} +- {s2:.3f} -> {'pass' if t2 else 'FAIL'}")
    P(f"     T3 literature-sigma UFDs (N {len(ufd)}): E = {e3:+.3f} +- {s3:.3f} -> {'pass' if t3 else 'FAIL'}")
    P(f"     T4 MW classical rms ln-residual: cored {RES[foot]['classical_rms_cored']:.3f} vs law alone {RES[foot]['classical_rms_law']:.3f}")
    P(f"     CLASS: {cls}")
RES["cls"] = RES["canonical"]["cls"]; P(f"\n  CLASS (canonical): {RES['cls']}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg870_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg870{sfx}.out"), "w").write("\n".join(OUT) + "\n")
