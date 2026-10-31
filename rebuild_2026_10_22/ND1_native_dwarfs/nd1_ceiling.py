#!/usr/bin/env python3
"""ND1_native_dwarfs part C (FROZEN_CRITERIA.md section 5): PC1's Local Group dwarfs and J0946 under (i) the smooth core at native N's S, (ii) the zooms' measured cusp; Argon's cusp claim rechecked; K4, K5c, K6, K7; noise from X80's seeds. Needs nd1_shapes.json.
    python3 nd1_ceiling.py            # writes nd1_ceiling.out, nd1_ceiling_results.json; exit 1 on any K failure
    python3 nd1_ceiling.py --mutate   # S x 0.5, shape r x 1.5; writes nd1_ceiling_MUTATE.out, nd1_ceiling_results_MUTATE.json; exit 1 if it does not bite
kappa = 1/2 FITTED; footings never pooled; cold dark energy, never a particle; not theory closed."""
import contextlib, csv, io, json, math, os, re, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
FHERE = os.path.dirname(os.path.abspath(__file__)); FRB = os.path.dirname(FHERE); REPO = os.path.dirname(FRB)
MUTATE = "--mutate" in sys.argv; NODRAWS = "--nodraws" in sys.argv; _av = sys.argv; sys.argv = [sys.argv[0]]; TAGOUT = "_MUTATE" if MUTATE else ""
LSD = os.path.join(FRB, "LS1_lstar_analogs"); _S = open(os.path.join(LSD, "ls1_analogs.py")).read(); __file__ = os.path.join(FHERE, "ls1_analogs_loader.py")
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_S[:_S.index('P("LS1 SPARC')], "ls1_head", "exec"))
HERE = FHERE; sys.argv = _av
from scipy.optimize import brentq, minimize_scalar
zform, EPS_, DELTA_ = NS["zform"], NS["EPS"], NS["DELTA"]
X81P = os.path.join(FRB, "X81_core_convergence", "x80_core_convergence.py"); _src = open(X81P).read(); _src = _src[:_src.index("# K1: exact smooth core")]; NX81 = dict(__file__=X81P, __name__="x81_prefix"); _a = sys.argv; sys.argv = [X81P]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src, X81P, "exec"), NX81)
sys.argv = _a; a_fit, M_nfw, eta_ofa = NX81["a_fit_profile"], NX81["M_nfw"], NX81["eta_of"]
def cleanup():
    for n in ("x74_fs0.034_c4_s2.7774.out", "x74_results_fs0.034_c4_s2.7774.json", "x74_x30_machinery.log", "x74_x30_machinery_MUTATE.log"):
        try: os.remove(os.path.join(FHERE, n))
        except OSError: pass
OUTL = []
def Pn(s): print(s, flush=True); OUTL.append(s)
# PC1's constants, so K4 is exact
G, MSUN, PC, MPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e16, 3.0856775814913673e22
A0_ = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FEET = ("canonical", "alt"); SIGF = {f: A0_[f] / (2 * math.pi * G) for f in FEET}; SIGFPC = {f: SIGF[f] * PC ** 2 / MSUN for f in FEET}
CLS = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field"); REP = ("indiv:Crater II", "indiv:Antlia II", "indiv:Sagittarius")
TA, TB_ = "A_c2b_refit", "B_cfg886_bg"; FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2)
BB = lambda x: np.log1p(np.asarray(x, float) ** 2) + 2 * np.log1p(np.asarray(x, float)) - 2 * np.arctan(np.asarray(x, float))
BS = lambda x: 4 * (np.arcsinh(np.asarray(x, float)) - np.asarray(x, float) / np.sqrt(1 + np.asarray(x, float) ** 2))
assert abs(float(B(1.0)) - float(BS(1.0))) < 1e-12, "the loader's B is not the smooth core"
def peak(Bf):
    p = minimize_scalar(lambda lx: -math.pi * float(Bf(math.exp(lx))) / math.exp(2 * lx), bounds=(-3, 4), method="bounded", options={"xatol": 1e-8}); return -p.fun, math.exp(p.x)
C3B, X3B = peak(BB); C3S, X3S = peak(BS)
_CE0 = json.load(open(os.path.join(FRB, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; ETA_PRE = [_CE0[str(e)]["med"] for e in (12, 13, 14)]
_CE4 = json.load(open(os.path.join(FRB, "CE1_converged_eta_grade", "ce1_a4_results.json")))["eta"]; ETA_A4 = [_CE4[str(e)]["med"] for e in (12, 13, 14)]
X80 = json.load(open(os.path.join(FRB, "X80_low_mass_floor_emergence", "x80_converged.json"))); R10, R11 = X80["r10"], X80["r11"]; assert (R10, R11) == (1.1280903506658675, 0.9383778261143368), "X80's ratios changed since the criteria"
S1 = 1.25 * 0.5 * math.log10(8.05 / 5.72); LM_CLAMP = 7.0 + math.log10(2.0)
def make_rule(etav, slope=None, tab=None, mut=1.0):
    """S in Msun/pc^2 as a function of M200 (Msun), background tag; sigma_coll held below lg M_t 7.301, as the criteria state."""
    def Srule(M, tag):
        Mt = M / FC; lg = math.log10(Mt); trend = 10 ** float(np.interp(lg, [10.0, 11.0, 12.0], tab)) if tab is not None else 10 ** (slope * max(0.0, 12 - lg))
        return mut * FC * float(np.interp(lg, [12, 13, 14], etav)) * trend * sigma_coll(tag, max(Mt, 10 ** LM_CLAMP))[0]
    return Srule
TAB_NAT = [math.log10(R10), math.log10(R11), 0.0]; MS = 0.5 if MUTATE else 1.0; RX = 1.5 if MUTATE else 1.0
RULE_NAT = make_rule(ETA_A4, tab=TAB_NAT, mut=MS); RULE_N1 = make_rule(ETA_PRE, slope=S1); RULE_N0 = make_rule(ETA_PRE, slope=0.0)
# ---------------------------------------------------------------- objects, PC1's rows
ARR = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv")))); arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}; med_free = float(np.median(list(arr_free.values())))
X1 = list(csv.DictReader(open(os.path.join(FRB, "X1_hosted_recount", "x1_per_system.csv"))))
def rows(f, tag=TA):
    bg = BGS[tag]; out = []
    for r in X1:
        if r["footing"] != f or r["cls"] not in CLS + REP: continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        b = arr_free.get(r["name"], med_free if (mv is not None and mv > -7.7) else 1.0)
        sc = float(r["sigma"]) * b; r12 = 4 / 3 * float(r["rh_pc"]) * PC; Mb = 10 ** float(r["logMstar"])
        out.append(dict(name=r["name"], cls=r["cls"], r12=r12, r12_pc=r12 / PC, gobs=3 * (sc * 1e3) ** 2 / r12, gN=G * (Mb / 2) * MSUN / r12 ** 2, s=float(r["sdMC[Newton]"]), M200_own=10 ** (bg["a"] + bg["b"] * (math.log10(Mb) - 10))))
    return out
ROWS = {f: rows(f) for f in FEET}; RR = {f: np.array([x["r12"] for x in ROWS[f]]) for f in FEET}; RPC = RR["canonical"] / PC; GOBS = {f: np.array([x["gobs"] for x in ROWS[f]]) for f in FEET}; GN = {f: np.array([x["gN"] for x in ROWS[f]]) for f in FEET}; SD = {f: np.array([x["s"] for x in ROWS[f]]) for f in FEET}; CLSV = np.array([x["cls"] for x in ROWS["canonical"]]); NAMESV = [x["name"] for x in ROWS["canonical"]]; IDR = NAMESV.index("Draco")
assert all((RR["canonical"] == RR["alt"]).tolist()) and all((GOBS["canonical"] == GOBS["alt"]).tolist()), "X1's footing rows differ in their data"
PERT = [("J0946 dark <0.3 kpc", 300.0, 5.8e8, 0.3e8, 8 * 5.0e6), ("J0946 dark <0.6 kpc", 600.0, 1.1e9, 0.05e9, 8 * 5.0e6)]; RP = np.array([p[1] for p in PERT])
def boot(E, s, rng, n=10000):
    N = len(E); ix = rng.integers(0, N, (n, N)); return float(np.median(E)), float(np.std(np.median(E[ix] + s[ix] * rng.standard_normal((n, N)), axis=1)))
def grade(Crow, Cpert, f="canonical"):
    """Crow: mass in kg at each r12; Cpert: mass in Msun at J0946's radii. PC1's E_C, bootstrap order and R."""
    E = np.log10(GOBS[f] / (GN[f] + G * Crow / RR[f] ** 2)); rng = np.random.default_rng(20261026); o = dict(cls={}, E=E)
    for c in CLS:
        m_ = CLSV == c; med, sd = boot(E[m_], SD[f][m_], rng); o["cls"][c] = dict(N=int(m_.sum()), median=med, sd=sd, Z=med / sd, n_above_2s=int((E[m_] > 2 * SD[f][m_]).sum()))
    o["draco"] = dict(E=float(E[IDR]), s=float(SD[f][IDR]), above_2s=bool(E[IDR] > 2 * SD[f][IDR])); o["R"] = [float((p[2] - 2 * p[3] - p[4]) / Cpert[i]) for i, p in enumerate(PERT)]; o["rep"] = {n: float(E[NAMESV.index(n)]) for n in ("Crater II", "Antlia II", "Sagittarius")}; return o
def clsR(R): return "ALLOWED" if R <= 1 else ("MARGINAL" if R <= 2 else "EXCEEDS")
def ufd_label(z): return "NO M200 RESCUES" if z > 2 else ("CEILING ADMITS" if abs(z) < 2 else "BELOW CEILING")
def strip(o): return {k: ([None if x != x else x for x in v] if k == "R" else v) for k, v in o.items() if k != "E"}
def line(tag_, o, extra=""):
    c = o["cls"]; Pn(f"  {tag_:44s} UFD {c['MW ultra-faint']['median']:+.3f} ({c['MW ultra-faint']['Z']:+.2f}); bright M31 {c['bright M31']['median']:+.3f} ({c['bright M31']['Z']:+.2f}); M31 others {c['M31 others']['median']:+.3f} ({c['M31 others']['Z']:+.2f}); classical {c['MW classical']['median']:+.3f} ({c['MW classical']['Z']:+.2f}); LG field {c['LG field']['median']:+.3f} ({c['LG field']['Z']:+.2f}); Draco {o['draco']['E']:+.3f}; J0946 R {o['R'][0]:.1f} / {o['R'][1]:.1f}{extra}")
def solve_r0_B(Mtot, Rout, Sig, Bf):
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(Bf(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10}); lpk = float(pk.x)
    if lm(lpk) < math.log(Mtot): return math.exp(lpk)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), lpk, xtol=1e-14))
LMG = np.arange(4.0, 14.0 + 1e-9, 0.02)
def rho_c(tag): return 3 * (100 * BGS[tag]["h"] * 1e3 / MPC) ** 2 / (8 * math.pi * G)
def table(rule_pc, tag, Bf=BS, lmg=LMG):
    """On the M200 grid: S (kg/m^2), R200 (m), compact r0 (m)."""
    rc = rho_c(tag); Sg, Rg, r0g = [], [], []
    for lm in lmg:
        M = 10.0 ** lm; R2 = (3 * M * MSUN / (4 * math.pi * 200 * rc)) ** (1 / 3); s = rule_pc(M, tag) * MSUN / PC ** 2; Sg.append(s); Rg.append(R2); r0g.append(solve_r0_B(M * MSUN, R2, s, Bf))
    return np.array(Sg), np.array(Rg), np.array(r0g)
def mass_on(r_m, Sg, Rg, r0g, Bf=BS):
    """M(<r) in kg, r_m an array of radii; result shape (len(grid), len(r_m))."""
    r_ = np.asarray(r_m, float)[None, :]; return math.pi * Sg[:, None] * r0g[:, None] ** 2 * Bf(np.minimum(r_, Rg[:, None]) / r0g[:, None])
def sup_core(rule_pc, tag):
    Sg, Rg, r0g = table(rule_pc, tag); Mo = mass_on(RR["canonical"], Sg, Rg, r0g); Mp = mass_on(RP * PC, Sg, Rg, r0g); return Mo.max(0), Mp.max(0) / MSUN, LMG[Mo.argmax(0)], LMG[Mp.argmax(0)], (Sg, Rg, r0g, Mo, Mp)
def at_mass(rule_pc, M200, tag=TA):
    rc = rho_c(tag); R2 = (3 * M200 * MSUN / (4 * math.pi * 200 * rc)) ** (1 / 3); s = rule_pc(M200, tag) * MSUN / PC ** 2; r0 = solve_r0_B(M200 * MSUN, R2, s, BS); return s, R2, r0
def rf_pc(Mt):
    zf = zform(TA, max(Mt, 10 ** LM_CLAMP))[0]; rho = DELTA_ * EPS_[TA]["rhom0"] * (1 + zf) ** 3; return (3 * (Mt / 2) / (4 * math.pi * rho)) ** (1 / 3) * 1e6
# ---------------------------------------------------------------- the zooms' measured shape
SH = json.load(open(os.path.join(HERE, "nd1_shapes.json"))); XG = np.array(SH["x"]); LXG = np.log(XG); RG = np.geomspace(0.1, 1e7, 4001); LRG = np.log(RG); mu = lambda y: np.log1p(y) - y / (1 + y); TAGSM = {10: "1e10", 11: "1e11", 12: "1e12", 13: "1e13", 14: "1e14"}
def seed_ln(d, mode):
    r = RG / RX; lx = np.log(r / d["R200_pc"]); ln = np.array(d["lnm"]); prim = np.where(lx >= LXG[0], np.interp(lx, LXG, ln), ln[0] + 2 * (lx - LXG[0])) + math.log(d["M200"])
    if mode == "r2": return prim
    c = d["c_nfw"]; y = c * r / d["rvir_pc"]
    if mode == "nfw": return np.where(r >= d["r3e_pc"], prim, np.log(d["Mvir"] * mu(y) / mu(c)))
    return math.log(2 * math.pi * d["rhos_rs_pc"]) + 2 * np.log(r)      # the limit, M/r^2 -> 2 pi rho_s r_s
SEED = {snap: {l: {m: np.array([seed_ln(d, m) for d in SH[snap][t]]) for m in ("r2", "nfw", "lim")} for l, t in TAGSM.items() if len(SH[snap][t]) >= 6} for snap in ("zf", "z0")}
def meds(snap, mode, idx=None):
    return {l: (np.median(v[mode], axis=0) if not (idx is not None and l == 10) else np.median(v[mode][idx], axis=0)) for l, v in SEED[snap].items()}
RF10 = rf_pc(1e10)
def lnM_at(r_pc, Mt, md):
    """ln M(<r) (total matter, Msun) at M_t: self-similar from the 1e10 tag below it, linear in lg M_t between tags, physical r at a tag. NaN above 1e14."""
    r_pc = np.asarray(r_pc, float); lg = math.log10(Mt)
    if lg <= 10.0: return math.log(Mt / 1e10) + np.interp(np.log(r_pc * RF10 / rf_pc(Mt)), LRG, md[10])
    if lg > 14.0: return np.full(r_pc.shape, np.nan)
    lo = min(int(math.floor(lg)), 13); w = lg - lo; return (1 - w) * np.interp(np.log(r_pc), LRG, md[lo]) + w * np.interp(np.log(r_pc), LRG, md[lo + 1])
def cusp_mass(r_pc, Mt, md): return FC * np.exp(lnM_at(r_pc, Mt, md))         # cold mass, Msun
def r3e_pc(Mt): return 0.03 * rf_pc(Mt)
def grade_cusp(Mt, md): return grade(cusp_mass(RPC, Mt, md) * MSUN, cusp_mass(RP, Mt, md))
def inside(Mt):
    r3 = r3e_pc(Mt); return dict(r3e_pc=r3, classes={c: int((RPC[CLSV == c] < r3).sum()) for c in CLS}, N={c: int((CLSV == c).sum()) for c in CLS}, draco=bool(RPC[IDR] < r3), J0946=[bool(x < r3) for x in RP], reported={n: bool(RPC[NAMESV.index(n)] < r3) for n in ("Crater II", "Antlia II", "Sagittarius")}, total=int((RPC[np.isin(CLSV, CLS)] < r3).sum()), n_total=int(np.isin(CLSV, CLS).sum()))
def flag_inside(Mt):
    q = inside(Mt); return f"; inside 3 eps ({q['r3e_pc']:.0f} pc): " + ", ".join(f"{c} {q['classes'][c]}/{q['N'][c]}" for c in CLS) + f", Draco {'yes' if q['draco'] else 'no'}, J0946 {'yes' if q['J0946'][0] else 'no'}/{'yes' if q['J0946'][1] else 'no'}"
# ---------------------------------------------------------------- checks
Pn(f"ND1 part C{' [MUTATE S x 0.5, shape r x 1.5]' if MUTATE else ''}: bounds M3D(<r) <= C S r^2: smooth core C {C3S:.4f} at r/r0 {X3S:.3f}, Burkert C {C3B:.4f} at {X3B:.3f}; kappa = 1/2 FITTED; footings never pooled; not theory closed")
K = {}; PC1 = json.load(open(os.path.join(FRB, "PC1_perturber_ceiling_route_e", "pc1_results.json"))); okK = True
if not MUTATE:
    dk = abs(C3B - PC1["C3"]); F_B = {}
    for f in FEET:
        F_B[f] = grade(C3B * SIGF[f] * RR[f] ** 2, C3B * SIGFPC[f] * RP ** 2, f); pc = PC1["footings"][f]
        for c in CLS: dk = max(dk, abs(F_B[f]["cls"][c]["median"] - pc["dwarfs"][c]["median_EC"]), abs(F_B[f]["cls"][c]["sd"] - pc["dwarfs"][c]["sd"]), abs(F_B[f]["cls"][c]["Z"] - pc["dwarfs"][c]["Z_C"]))
        for i, p in enumerate(PERT): dk = max(dk, abs(F_B[f]["R"][i] - pc["perturbers"][p[0]]["R"]))
    dD = max(abs(F_B["canonical"]["draco"]["E"] - 0.148), abs(F_B["alt"]["draco"]["E"] - 0.068)); ok4 = dk <= 1e-9 and dD <= 0.001; K["K4"] = dict(pc1=dk, draco=dD); Pn(f"K4 the floor's S with Burkert reproduces PC1: max |d| {dk:.1e} (1e-9), Draco {dD:.4f} (0.001): {'PASS' if ok4 else 'FAIL'}"); okK = okK and ok4
    # K5c r_f
    d5 = max(abs(rf_pc(float(SH["zf"][t][0]["M_nominal"])) / SH["zf"][t][0]["rf_pc"] - 1) for t in TAGSM.values()); ok5 = d5 <= 1e-3 and SH["K5a"] <= 1e-9 and SH["K5b"]; K["K5"] = dict(rf=d5, K5a=SH["K5a"], K5b=SH["K5b"]); Pn(f"K5 zoom path (nd1_shapes): c_nfw, eta_conv {SH['K5a']:.1e} (1e-9), ZN1's K2 {'PASS' if SH['K5b'] else 'FAIL'}; rf_phys vs zform {d5:.1e} (1e-3): {'PASS' if ok5 else 'FAIL'}"); okK = okK and ok5
    # K6 free-M200 path, floor's S, Burkert
    s0 = SIGFPC["canonical"]; Sg, Rg, r0g = table(lambda M, tag: s0, TA, BB); rr_ = np.array([RP[0] * PC, RP[1] * PC, RR["canonical"][IDR]]); Mx = mass_on(rr_, Sg, Rg, r0g, BB).max(0); d6 = float(np.max(np.abs(Mx / (C3B * s0 * MSUN / PC ** 2 * rr_ ** 2) - 1))); ok6 = d6 <= 1e-3; K["K6"] = d6; Pn(f"K6 free-M200 path with the floor's S and Burkert returns {C3B:.3f} S r^2: max |d| {d6:.1e} (1e-3): {'PASS' if ok6 else 'FAIL'}"); okK = okK and ok6
    # K7 exact NFW against argon_check.out
    AC = open(os.path.join(FRB, "ARGON_REPLY_2026-10-31", "argon_check.out")).read(); ROWQ = re.findall(r"c ([\d.]+): eta ([\d.]+), c\^2/\(3 m\(c\)\) ([\d.]+), ratio ([\d.]+), ceiling gain x([\d.]+) \(\+([\d.]+) dex\)", AC); d7 = 0.0; EXN = {}
    for row in ROWQ:
        c = float(row[0]); e = float(eta_ofa(a_fit(M_nfw(c), 0.001))); rs = c * c / (3 * float(mu(c))); g = 2 * math.pi * rs / e / C3B; d7 = max(d7, abs(e - float(row[1])), abs(rs - float(row[2])), abs(rs / e - float(row[3])), abs(g - float(row[4])), abs(math.log10(g) - float(row[5]))); EXN[f"{c:g}"] = dict(eta=e, rhos_rs=rs, ratio=rs / e, gain_burkert=g, gain_burkert_dex=math.log10(g), gain_smooth=2 * math.pi * rs / e / C3S, gain_smooth_dex=math.log10(2 * math.pi * rs / e / C3S))
    ok7 = len(ROWQ) == 5 and d7 <= 5.1e-3; K["K7"] = d7; Pn(f"K7 exact NFW reproduces argon_check.out at {len(ROWQ)} c values: max |d| {d7:.1e} (5e-3): {'PASS' if ok7 else 'FAIL'}"); okK = okK and ok7
    _NB = json.load(open(os.path.join(FRB, "NF1_no_floor_rule", "nf1_bins.json"))); d4b = max(abs(RULE_N1(1e9, TA) - _NB["N1"]["S_at"]["9"]), abs(RULE_N0(1e9, TA) - _NB["N0"]["S_at"]["9"])); ok4b = d4b <= 1e-9; K["K4b"] = d4b; Pn(f"K4b this path's S at lg M200 9 reproduces NF1's N1 and N0: max |d| {d4b:.1e} (1e-9): {'PASS' if ok4b else 'FAIL'}"); okK = okK and ok4b
    for c, v in EXN.items(): Pn(f"  exact NFW c {c}: eta {v['eta']:.2f}, rho_s r_s / S {v['ratio']:.3f}; 2 pi rho_s r_s over Burkert's bound +{v['gain_burkert_dex']:.3f} dex (the earlier check), over the smooth core's own bound +{v['gain_smooth_dex']:.3f} dex")
RES = dict(frozen="9230f53a67", mutate=MUTATE, C3_smooth=C3S, C3_burkert=C3B, K=K, status=SH["status"], exact_nfw=EXN if not MUTATE else None)
# ---------------------------------------------------------------- the zoom table
Pn("Measured zooms (cold share f_c applied to Gamma = M/r^2; S_N the rule's S at that M_t):"); TABZ = {}
def med(rows, k): return float(np.median([q[k] for q in rows if k in q]))
for snap in ("zf", "z0"):
    TABZ[snap] = {}
    for l, t in TAGSM.items():
        rows_ = SH[snap][t]
        if len(rows_) < 6: Pn(f"  {snap} {t}: {len(rows_)} finished seeds, not read"); continue
        Mt = 10.0 ** l; Sn = RULE_NAT(FC * Mt, TA); g3 = FC * float(np.median([q["M_3e"] / q["r3e_pc"] ** 2 for q in rows_])); gl = FC * 2 * math.pi * med(rows_, "rhos_rs_pc"); o = dict(n=len(rows_), r3e=med(rows_, "r3e_pc"), n3e=med(rows_, "n_in_3e"), r200th=med(rows_, "r200th_pc"), R200=med(rows_, "R200_pc"), M200_over=med(rows_, "M200") / Mt, c_nfw=med(rows_, "c_nfw"), eta=med(rows_, "eta_conv"), ratio=med(rows_, "ratio"), G3=g3, Glim=gl, S_rule=Sn, slope=med(rows_, "slope_3e6e"), slope_nfw=med(rows_, "slope_nfw_3e6e"), y3=med(rows_, "y_3e"))
        o["M3e_over_nfw"] = float(np.median([q["M_3e"] / (q["Mvir"] * float(mu(q["y_3e"])) / float(mu(q["c_nfw"]))) for q in rows_])); o["S_conv_cold"] = FC * med(rows_, "S_conv_pc"); o["S_conv_over_rule"] = o["S_conv_cold"] / Sn; o["G3_over_core"] = g3 / (C3S * Sn); o["Glim_over_core"] = gl / (C3S * Sn); o["Glim_over_burkert"] = gl / (C3B * Sn); TABZ[snap][t] = o
        Pn(f"  {snap} {t}: n {o['n']}, 3 eps {o['r3e']:.0f} pc (n inside {o['n3e']:.0f}; 200th particle {o['r200th']:.0f} pc), R200 {o['R200'] / 1e3:.1f} kpc, M200/M_t {o['M200_over']:.3f}, c_nfw {o['c_nfw']:.2f}, eta_conv {o['eta']:.2f}, rho_s r_s / S_conv {o['ratio']:.3f}; Gamma(3 eps) {g3:.0f}, limit 2 pi rho_s r_s {gl:.0f} Msun/pc^2; rule S {Sn:.1f}, the zoom's own eta_conv 3 M_vir / (4 pi r_vir^2) f_c {o['S_conv_cold']:.1f} ({o['S_conv_over_rule']:.3f} of it); over the smooth bound C S: {o['G3_over_core']:.2f} at 3 eps, {o['Glim_over_core']:.2f} limit; slope 3-6 eps {o['slope']:.2f} vs NFW {o['slope_nfw']:.2f} (y {o['y3']:.2f}); M(<3 eps) over the seed's own NFW fit {o['M3e_over_nfw']:.3f}")
RES["zooms"] = TABZ
# ---------------------------------------------------------------- core ceilings
Pn("E_C (Z_C) by class, Draco's E_C, J0946 R at 0.3 / 0.6 kpc:"); GR = {}
Mt9 = 1e9 / FC; S9_nat, S9_n1, S9_n0 = RULE_NAT(1e9, TA), RULE_N1(1e9, TA), RULE_N0(1e9, TA)
Pn(f"  S at lg M200 9 (lg M_t {math.log10(Mt9):.3f}): native N {S9_nat:.2f}, N1 {S9_n1:.2f}, N0 {S9_n0:.2f}; floor {SIGFPC['canonical']:.1f} / {SIGFPC['alt']:.1f} Msun/pc^2; r_f {rf_pc(Mt9) / 1e3:.2f} kpc, z_f {zform(TA, Mt9)[0]:.3f}; 3 eps scaled {r3e_pc(Mt9):.0f} pc")
def bound_grade(S_pc, Cc, f="canonical"): return grade(Cc * S_pc * MSUN / PC ** 2 * RR[f] ** 2, Cc * S_pc * RP ** 2, f)
if not MUTATE:
    for f in FEET: GR[f"floor Burkert (PC1) {f}"] = F_B[f]; line(f"floor Burkert (PC1) {f}", F_B[f])
    for f in FEET: GR[f"floor smooth bound {f}"] = bound_grade(SIGFPC[f], C3S, f); line(f"floor smooth bound {f}", GR[f"floor smooth bound {f}"])
    GR["N1 lg 9 Burkert bound (brief)"] = bound_grade(S9_n1, C3B); line("N1 lg 9 Burkert bound (brief)", GR["N1 lg 9 Burkert bound (brief)"]); GR["N1 lg 9 smooth bound"] = bound_grade(S9_n1, C3S); line("N1 lg 9 smooth bound", GR["N1 lg 9 smooth bound"])
GR["native lg 9 Burkert bound"] = bound_grade(S9_nat, C3B); line("native lg 9 Burkert bound", GR["native lg 9 Burkert bound"]); GR["native lg 9 smooth bound"] = bound_grade(S9_nat, C3S); line("native lg 9 smooth bound", GR["native lg 9 smooth bound"])
s9, R29, r09 = at_mass(RULE_NAT, 1e9); GR["native lg 9 own r0"] = grade(math.pi * s9 * r09 ** 2 * BS(np.minimum(RR["canonical"], R29) / r09), math.pi * s9 * r09 ** 2 * BS(np.minimum(RP * PC, R29) / r09) / MSUN); line("native lg 9, the halo's own r0", GR["native lg 9 own r0"], f"; r0 {r09 / PC:.0f} pc")
Crow, Cpert, lmr, lmp, TBL = sup_core(RULE_NAT, TA); GR["native free M200 (PRIMARY)"] = grade(Crow, Cpert); line("native free M200 (PRIMARY core)", GR["native free M200 (PRIMARY)"], f"; peak lg M200: Draco {lmr[IDR]:.2f}, J0946 {lmp[0]:.2f}/{lmp[1]:.2f}; systems whose peak is under the Sigma_coll clamp {int((lmr < LM_CLAMP + math.log10(FC)).sum())}")
Crow_alt = grade(Crow, Cpert, "alt"); GR["native free M200, alt's s"] = Crow_alt; line("native free M200, alt's MC s (same E)", Crow_alt)
CrowB, CpertB, _, _, _ = sup_core(RULE_NAT, TB_); GR["native free M200, background B"] = grade(CrowB, CpertB); line("native free M200, background B", GR["native free M200, background B"])
# own EM1 M200, the halo itself, not a ceiling (reported)
own = []
for x in ROWS["canonical"]:
    s_, R2_, r_ = at_mass(RULE_NAT, x["M200_own"]); own.append(math.pi * s_ * r_ ** 2 * float(BS(min(x["r12"], R2_) / r_)))
GR["native own EM1 M200, core (a prediction)"] = grade(np.array(own), Cpert * np.nan); line("native own EM1 M200, core (a prediction)", GR["native own EM1 M200, core (a prediction)"], f"; own lg M200 of Draco {math.log10(ROWS['canonical'][IDR]['M200_own']):.2f}; n below the clamp {int(sum(math.log10(x['M200_own'] / FC) < LM_CLAMP for x in ROWS['canonical']))}")
# ---------------------------------------------------------------- the cusp
def do_snap(snap):
    Rs = {}; md = {m: meds(snap, m) for m in ("r2", "nfw", "lim")}
    Pn(f"Native cusp, snapshot {snap}; M_t 1.19e9 is lg M200 9, from the 1e10 tag by self-similar scaling:")
    for nm, m in (("cusp lg 9, M prop r^2 (PRIMARY)", "r2"), ("cusp lg 9, NFW fit at r", "nfw"), ("cusp lg 9, limit 2 pi rho_s r_s", "lim")):
        Rs[nm] = grade_cusp(Mt9, md[m]); line(nm, Rs[nm], flag_inside(Mt9) if m == "r2" else "")
    for l in (10, 11, 12, 13, 14):
        if l not in md["r2"]: continue
        Rs[f"cusp tag 1e{l}, M prop r^2"] = grade_cusp(10.0 ** l, md["r2"]); line(f"cusp tag 1e{l}, M prop r^2", Rs[f"cusp tag 1e{l}, M prop r^2"], flag_inside(10.0 ** l)); Rs[f"cusp tag 1e{l}, NFW fit"] = grade_cusp(10.0 ** l, md["nfw"]); line(f"cusp tag 1e{l}, NFW fit", Rs[f"cusp tag 1e{l}, NFW fit"]); Rs[f"cusp tag 1e{l}, limit"] = grade_cusp(10.0 ** l, md["lim"]); line(f"cusp tag 1e{l}, limit", Rs[f"cusp tag 1e{l}, limit"])
    Co = np.array([cusp_mass(np.array([x["r12_pc"]]), x["M200_own"] / FC, md["r2"])[0] for x in ROWS["canonical"]]) * MSUN; Rs["cusp own EM1 M200 (a prediction)"] = grade(Co, Cpert * np.nan); line("cusp own EM1 M200 (a prediction)", Rs["cusp own EM1 M200 (a prediction)"], f"; inside 3 eps at own mass: {int(sum(x['r12_pc'] < r3e_pc(x['M200_own'] / FC) for x in ROWS['canonical']))} of {len(ROWS['canonical'])}")
    # the premise: does M/r^2 rise with mass at fixed r?
    lgs = (8, 9, 10, 11, 12, 13, 14); PRM = {}
    for r_ in (100.0, 300.0, 600.0, 1000.0):
        v = [float(cusp_mass(np.array([r_]), 10.0 ** l, md["r2"])[0] / r_ ** 2) for l in lgs]; w = [float(cusp_mass(np.array([r_]), 10.0 ** l, md["lim"])[0] / r_ ** 2) for l in lgs]; mono = all(b > a for a, b in zip(v, v[1:])); PRM[f"{r_:g}"] = dict(gamma=v, limit=w, monotonic=mono); Pn(f"  M/r^2 at r {r_:.0f} pc, lg M_t 8..14, M prop r^2: " + ", ".join(f"{g:.0f}" for g in v) + f"; limit: " + ", ".join(f"{g:.0f}" for g in w) + f"; rises at every step: {mono}")
    # M200 needed
    LMT = np.arange(5.0, 14.0 + 1e-9, 0.02); need = np.maximum(GOBS["canonical"] - GN["canonical"], 0.0) * RR["canonical"] ** 2 / G / MSUN; rall = np.concatenate([RPC, RP]); nall = np.concatenate([need, np.array([p[2] - 2 * p[3] - p[4] for p in PERT])]); GRD = {}
    for m in ("r2", "nfw", "lim"): GRD[m] = np.array([cusp_mass(rall, 10.0 ** l, md[m]) for l in LMT])
    def first(arr, nn):
        ok_ = arr >= nn; return float(LMT[int(np.argmax(ok_))]) if ok_.any() else None
    NEED = {}
    for m in GRD:
        lg = [first(GRD[m][:, j], nall[j]) for j in range(len(rall))]; NEED[m] = lg
    def need_row(m, title):
        out = {}; lg = NEED[m]
        for c in CLS:
            ii = np.where(CLSV == c)[0]; own_ = np.array([ROWS["canonical"][i]["M200_own"] for i in ii]); got = [(lg[i] + math.log10(FC), own_[k]) for k, i in enumerate(ii) if lg[i] is not None]; ins = [rall[i] < r3e_pc(10.0 ** lg[i]) for i in ii if lg[i] is not None]
            out[c] = dict(reached=len(got), N=len(ii), med_lgM200=float(np.median([g[0] for g in got])) if got else None, med_over_own=float(np.median([10 ** g[0] / g[1] for g in got])) if got else None, inside=int(sum(ins)))
        dr = lg[IDR]; out["Draco"] = dict(lgM200=None if dr is None else dr + math.log10(FC), over_own=None if dr is None else 10 ** (dr + math.log10(FC)) / ROWS["canonical"][IDR]["M200_own"], inside=None if dr is None else bool(rall[IDR] < r3e_pc(10.0 ** dr))); nP = len(RPC)
        out["J0946"] = [None if lg[nP + i] is None else lg[nP + i] + math.log10(FC) for i in range(2)]
        Pn(f"  M200 needed, {title}: " + "; ".join(f"{c}: reached {out[c]['reached']}/{out[c]['N']}, median lg {out[c]['med_lgM200'] if out[c]['med_lgM200'] is None else round(out[c]['med_lgM200'], 2)}, x{out[c]['med_over_own'] if out[c]['med_over_own'] is None else round(out[c]['med_over_own'])} over EM1's, inside 3 eps {out[c]['inside']}" for c in CLS) + f"; Draco lg {None if out['Draco']['lgM200'] is None else round(out['Draco']['lgM200'], 2)}, x{None if out['Draco']['over_own'] is None else round(out['Draco']['over_own'])}, inside {out['Draco']['inside']}; J0946 lg {[None if v is None else round(v, 2) for v in out['J0946']]} (None = not reached at 1e14)")
        return out
    Rs_need = {m: need_row(m, t) for m, t in (("r2", "M prop r^2"), ("nfw", "NFW fit"), ("lim", "limit"))}
    return Rs, PRM, Rs_need, md
CU = {}; PRMS = {}; NEEDS = {}; MDS = {}
CU["zf"], PRMS["zf"], NEEDS["zf"], MDS["zf"] = do_snap("zf")
z0ok = all(l in SEED["z0"] for l in (10, 11)); RES["z0_graded"] = bool(z0ok); st = SH["status"]
if z0ok: CU["z0"], PRMS["z0"], NEEDS["z0"], MDS["z0"] = do_snap("z0")
else: Pn(f"z = 0 NOT GRADED: ZN2's low-mass runs had {st['z0_1e10']} of 9 (1e10) and {st['z0_1e11']} of 9 (1e11) finished seeds when nd1_shapes.py ran; z_f stands alone")
# core: M200 needed on the rule
need_c = np.maximum(GOBS["canonical"] - GN["canonical"], 0.0) * RR["canonical"] ** 2 / G; Mo = TBL[3]; lgc = [float(LMG[int(np.argmax(Mo[:, j] >= need_c[j]))]) if (Mo[:, j] >= need_c[j]).any() else None for j in range(len(RPC))]; NCORE = {}
for c in CLS:
    ii = np.where(CLSV == c)[0]; got = [(lgc[i], ROWS["canonical"][i]["M200_own"]) for i in ii if lgc[i] is not None]; NCORE[c] = dict(reachable=len(got), N=len(ii), med_lgM200=float(np.median([g[0] for g in got])) if got else None, med_over_own=float(np.median([10 ** g[0] / g[1] for g in got])) if got else None)
Pn("  Core on the rule, M200 needed (lowest): " + "; ".join(f"{c}: reachable {NCORE[c]['reachable']}/{NCORE[c]['N']}, median lg {None if NCORE[c]['med_lgM200'] is None else round(NCORE[c]['med_lgM200'], 2)}, x{None if NCORE[c]['med_over_own'] is None else round(NCORE[c]['med_over_own'])} over EM1's" for c in CLS) + f"; Draco {'reachable at lg ' + str(round(lgc[IDR], 2)) if lgc[IDR] is not None else 'NOT reachable'}")
# ---------------------------------------------------------------- Argon's cusp claim
if not MUTATE:
    z10 = SH["zf"]["1e10"]; ratio_m = float(np.median([q["ratio"] for q in z10])); c_m = float(np.median([q["c_nfw"] for q in z10])); eta_n1 = ETA_PRE[0] * 10 ** (S1 * (12 - math.log10(Mt9))); cg = np.arange(3.0, 30.01, 0.25); eg = np.array([float(eta_ofa(a_fit(M_nfw(float(c_)), 0.001))) for c_ in cg]); c_eq = float(np.interp(eta_n1, eg, cg)); rat_eq = float(c_eq ** 2 / (3 * mu(c_eq)) / float(eta_ofa(a_fit(M_nfw(c_eq), 0.001))))
    g_d, gn_d = GOBS["canonical"][IDR], GN["canonical"][IDR]; S1si = S9_n1 * MSUN / PC ** 2; rD = RR["canonical"][IDR]
    Eof = lambda rat, S_si: math.log10(g_d / (gn_d + G * 2 * math.pi * rat * S_si)); rs_eq = rf_pc(Mt9) / c_eq; yD = (rD / PC) / rs_eq; fin = float(mu(yD)) / yD ** 2 / 0.5
    A = dict(ratio_measured=ratio_m, c_measured=c_m, eta_N1_at_9=eta_n1, c_eq=c_eq, ratio_c_eq=rat_eq, ratio_c15=EXN["15"]["ratio"], draco_hand_burkert=GR["N1 lg 9 Burkert bound (brief)"]["draco"]["E"], draco_smooth=GR["N1 lg 9 smooth bound"]["draco"]["E"], draco_measured_ratio=Eof(ratio_m, S1si), draco_c15=Eof(EXN["15"]["ratio"], S1si), draco_c_eq=Eof(rat_eq, S1si), draco_c_eq_finite_r=math.log10(g_d / (gn_d + G * 2 * math.pi * rat_eq * S1si * fin)), y_finite=yD, finite_factor=fin)
    Rof = lambda rat, S_pc, i=0: (PERT[i][2] - 2 * PERT[i][3] - PERT[i][4]) / (2 * math.pi * rat * S_pc * PERT[i][1] ** 2)
    A.update(J0946_floor_measured=Rof(ratio_m, SIGFPC["canonical"]), J0946_floor_c15=Rof(EXN["15"]["ratio"], SIGFPC["canonical"]), J0946_N1_measured=Rof(ratio_m, S9_n1), J0946_N1_c15=Rof(EXN["15"]["ratio"], S9_n1), J0946_native_measured=Rof(ratio_m, S9_nat), J0946_argon_form_floor=(PERT[0][2] - 2 * PERT[0][3] - PERT[0][4]) / (2 * math.pi * SIGFPC["canonical"] * PERT[0][1] ** 2), draco_argon_form=Eof(1.0, S1si))
    A["score_draco"] = "HIT" if abs(A["draco_measured_ratio"] + 0.104) <= 0.05 else "MISS"; A["score_J0946"] = "HIT" if abs(A["J0946_floor_measured"] / 7.9 - 1) <= 0.15 else "MISS"; RES["argon"] = A
    Pn("Argon's cusp claim rechecked:")
    Pn(f"  Measured at 1e10, z_f: c_nfw {c_m:.2f}, rho_s r_s / S {ratio_m:.3f} (claim: 1). N1's eta at lg M200 9 is {eta_n1:.1f}, c equivalent {c_eq:.1f}, ratio {rat_eq:.3f}; c 15 ratio {EXN['15']['ratio']:.3f}")
    Pn(f"  Draco on N1, S {S9_n1:.1f}: Burkert bound {A['draco_hand_burkert']:+.3f} (brief, by hand, +0.49); smooth bound {A['draco_smooth']:+.3f}; claim's form 2 pi S r^2 {A['draco_argon_form']:+.3f} (claim -0.104); cusp, measured ratio {A['draco_measured_ratio']:+.3f}; c 15 {A['draco_c15']:+.3f} (earlier check +0.076); c equivalent {A['draco_c_eq']:+.3f}; and at Draco's finite r (y {yD:.3f}, x{fin:.3f}) {A['draco_c_eq_finite_r']:+.3f}")
    Pn(f"  J0946 <0.3 kpc: claim's form at the floor's S {A['J0946_argon_form_floor']:.1f} (claim 7.9); cusp at the floor's S, measured ratio {A['J0946_floor_measured']:.1f}; c 15 {A['J0946_floor_c15']:.1f} (earlier check 12.0); at N1's S {A['J0946_N1_measured']:.1f}; at native N's S {A['J0946_native_measured']:.1f}")
    Pn(f"  Scores: Draco {A['score_draco']} (within 0.05 dex of -0.104), J0946 {A['score_J0946']} (within 15 % of 7.9)")
# ---------------------------------------------------------------- labels
PC_ = GR["native free M200 (PRIMARY)"]; core = dict(ufd=ufd_label(PC_["cls"]["MW ultra-faint"]["Z"]), J0946=[clsR(r) for r in PC_["R"]], draco_above=PC_["draco"]["above_2s"])
CP = CU["zf"]["cusp lg 9, M prop r^2 (PRIMARY)"]; CN = CU["zf"]["cusp lg 9, NFW fit at r"]; CL = CU["zf"]["cusp lg 9, limit 2 pi rho_s r_s"]
def clear(o): return dict(Draco=o["draco"]["E"] <= 2 * o["draco"]["s"], J0946=max(o["R"]) <= 2, ultra_faints=ufd_label(o["cls"]["MW ultra-faint"]["Z"]) != "NO M200 RESCUES")
cl_p, cl_n, cl_l = clear(CP), clear(CN), clear(CL); names = [k for k, v in cl_p.items() if v]; lab_c = "ALL THREE CLEAR" if len(names) == 3 else ("NONE CLEAR" if not names else "SOME CLEAR: " + ", ".join(n.replace("_", " ") for n in names))
first_tag = next((f"1e{l}" for l in (10, 11, 12, 13, 14) if f"cusp tag 1e{l}, M prop r^2" in CU["zf"] and max(CU["zf"][f"cusp tag 1e{l}, M prop r^2"]["R"]) <= 2), None); first_lim = next((f"1e{l}" for l in (10, 11, 12, 13, 14) if f"cusp tag 1e{l}, limit" in CU["zf"] and max(CU["zf"][f"cusp tag 1e{l}, limit"]["R"]) <= 2), None); IN9 = inside(Mt9)
lab_c += " [INSIDE 3 EPS]" if (IN9["total"] or IN9["draco"] or any(IN9["J0946"])) else ""; lab_c += " [CONTINUATION-DEPENDENT]" if cl_p != cl_n else ""
# ---------------------------------------------------------------- noise, X80's seeds, the same draws as nd1_ab
if not MUTATE and not NODRAWS:
    SUM = X80["summary"]; PR = [np.array(SUM[k]["per_run"]) for k in ("1e+10_ng64", "1e+11_ng64", "1e+12_ng64")]; IDX = np.random.default_rng(20261031).integers(0, 9, (200, 3, 9)); ND = []; sdU = PC_["cls"]["MW ultra-faint"]["sd"]; sdUc = CP["cls"]["MW ultra-faint"]["sd"]; mU = CLSV == "MW ultra-faint"
    for d in range(200):
        e10, e11, e12 = [float(np.median(PR[j][IDX[d, j]])) for j in range(3)]; rule = make_rule([e12, ETA_A4[1], ETA_A4[2]], tab=[math.log10(e10 / e12), math.log10(e11 / e12), 0.0]); Co, Cp, _, _, _ = sup_core(rule, TA); Ecore = np.log10(GOBS["canonical"] / (GN["canonical"] + G * Co / RR["canonical"] ** 2))
        mdd = meds("zf", "r2", IDX[d, 0]); Cc = cusp_mass(RPC, Mt9, mdd) * MSUN; Cj = cusp_mass(RP, Mt9, mdd); Ecusp = np.log10(GOBS["canonical"] / (GN["canonical"] + G * Cc / RR["canonical"] ** 2)); Rc = [(p[2] - 2 * p[3] - p[4]) / Cp[i] for i, p in enumerate(PERT)]; Ru = [(p[2] - 2 * p[3] - p[4]) / Cj[i] for i, p in enumerate(PERT)]
        ND.append(dict(core_ufd=float(np.median(Ecore[mU])), core_draco=float(Ecore[IDR]), core_R=Rc, core_cls={c: float(np.median(Ecore[CLSV == c])) for c in CLS}, cusp_ufd=float(np.median(Ecusp[mU])), cusp_draco=float(Ecusp[IDR]), cusp_R=Ru, cusp_cls={c: float(np.median(Ecusp[CLSV == c])) for c in CLS}))
        if (d + 1) % 25 == 0: print(f"  noise draw {d + 1}/200", flush=True)
    q = lambda v: [float(x) for x in np.percentile(v, [16, 50, 84])]
    NC = dict(core_ufd=q([x["core_ufd"] for x in ND]), core_draco=q([x["core_draco"] for x in ND]), core_R0=q([x["core_R"][0] for x in ND]), core_R1=q([x["core_R"][1] for x in ND]), cusp_ufd=q([x["cusp_ufd"] for x in ND]), cusp_draco=q([x["cusp_draco"] for x in ND]), cusp_R0=q([x["cusp_R"][0] for x in ND]), cusp_R1=q([x["cusp_R"][1] for x in ND]), core_cls={c: q([x["core_cls"][c] for x in ND]) for c in CLS}, cusp_cls={c: q([x["cusp_cls"][c] for x in ND]) for c in CLS})
    H = dict(core_ufd=float(np.mean([ufd_label(x["core_ufd"] / sdU) == core["ufd"] for x in ND])), core_J=float(np.mean([[clsR(r) for r in x["core_R"]] == core["J0946"] for x in ND])), core_draco=float(np.mean([(x["core_draco"] > 2 * PC_["draco"]["s"]) == core["draco_above"] for x in ND])), cusp_ufd=float(np.mean([(ufd_label(x["cusp_ufd"] / sdUc) != "NO M200 RESCUES") == cl_p["ultra_faints"] for x in ND])), cusp_J=float(np.mean([(max(x["cusp_R"]) <= 2) == cl_p["J0946"] for x in ND])), cusp_draco=float(np.mean([(x["cusp_draco"] <= 2 * CP["draco"]["s"]) == cl_p["Draco"] for x in ND])))
    RES["noise"] = dict(ranges=NC, held=H, draws=ND); Pn(f"  noise, 200 draws, 68 %: core UFD median {NC['core_ufd'][0]:+.3f}..{NC['core_ufd'][2]:+.3f}, Draco {NC['core_draco'][0]:+.3f}..{NC['core_draco'][2]:+.3f}, J0946 R {NC['core_R0'][0]:.1f}..{NC['core_R0'][2]:.1f}; cusp lg 9: UFD {NC['cusp_ufd'][0]:+.3f}..{NC['cusp_ufd'][2]:+.3f}, Draco {NC['cusp_draco'][0]:+.3f}..{NC['cusp_draco'][2]:+.3f}, J0946 R {NC['cusp_R0'][0]:.1f}..{NC['cusp_R0'][2]:.1f}; classes held: " + ", ".join(f"{k} {v:.2f}" for k, v in H.items()))
    if min(H[k] for k in ("cusp_ufd", "cusp_J", "cusp_draco")) < 0.68: lab_c += " [NOISE-LIMITED]"
    core["noise_limited"] = bool(min(H[k] for k in ("core_ufd", "core_J", "core_draco")) < 0.68)
RES.update(core=core, cusp=dict(label=lab_c, clear=cl_p, clear_nfw=cl_n, clear_limit=cl_l, J0946_first_tag=first_tag, J0946_first_tag_limit=first_lim, inside_lg9=IN9))
RES["grades"] = {k: strip(v) for k, v in GR.items()}; RES["cusp_grades"] = {s: {k: strip(v) for k, v in d.items()} for s, d in CU.items()}; RES["premise"] = PRMS; RES["M200_needed"] = NEEDS; RES["M200_needed_core"] = NCORE
premise_ok = all(v["monotonic"] for v in PRMS["zf"].values()); RES["premise_holds"] = premise_ok
Pn(f"CORE (free M200, background A): ultra-faints {core['ufd']} (Z_C {PC_['cls']['MW ultra-faint']['Z']:+.2f}), J0946 {core['J0946'][0]}/{core['J0946'][1]} (R {PC_['R'][0]:.1f} / {PC_['R'][1]:.1f}), Draco E_C {PC_['draco']['E']:+.3f} ({'above' if core['draco_above'] else 'not above'} by 2 s){' [NOISE-LIMITED]' if core.get('noise_limited') else ''}")
Pn(f"CUSP (lg M200 9, M prop r^2): {lab_c}; Draco {CP['draco']['E']:+.3f}, J0946 R {CP['R'][0]:.1f} / {CP['R'][1]:.1f}, ultra-faints {ufd_label(CP['cls']['MW ultra-faint']['Z'])} (Z {CP['cls']['MW ultra-faint']['Z']:+.2f}); J0946 first reaches R <= 2 at tag {first_tag or 'none to 1e14'} (limit reading: {first_lim or 'none to 1e14'}); M/r^2 rises with mass at every step at fixed r: {premise_ok}")
RES["okK"] = bool(okK)
if not MUTATE:
    _nd = NEEDS["zf"]; _lg = {}; _md = MDS["zf"]; LMT_ = np.arange(5.0, 14.0 + 1e-9, 0.02); need_ = np.maximum(GOBS["canonical"] - GN["canonical"], 0.0) * RR["canonical"] ** 2 / G / MSUN; _grd = np.array([cusp_mass(RPC, 10.0 ** l, _md["r2"]) for l in LMT_])
    with open(os.path.join(HERE, "nd1_systems.csv"), "w", newline="") as _f:
        _w = csv.writer(_f); _w.writerow(["name", "class", "r12_pc", "s", "own_lgM200", "E_floor_burkert_canonical", "E_floor_smooth_canonical", "E_native_core_freeM200", "E_cusp_lg9_r2", "E_cusp_lg9_nfwfit", "E_cusp_lg9_limit", "r12_inside_3eps_at_lg9", "r12_inside_3eps_at_tag_1e10", "lgM200_needed_cusp_r2", "inside_3eps_at_needed_mass"])
        _r3_9, _r3_10 = r3e_pc(Mt9), r3e_pc(1e10)
        for j, n_ in enumerate(NAMESV):
            ok_ = _grd[:, j] >= need_[j]; lt_ = float(LMT_[int(np.argmax(ok_))]) if ok_.any() else None
            _w.writerow([n_, CLSV[j], f"{RPC[j]:.1f}", f"{SD['canonical'][j]:.3f}", f"{math.log10(ROWS['canonical'][j]['M200_own']):.2f}", f"{F_B['canonical']['E'][j]:.3f}", f"{GR['floor smooth bound canonical']['E'][j]:.3f}", f"{PC_['E'][j]:.3f}", f"{CP['E'][j]:.3f}", f"{CN['E'][j]:.3f}", f"{CL['E'][j]:.3f}", int(RPC[j] < _r3_9), int(RPC[j] < _r3_10), "" if lt_ is None else f"{lt_ + math.log10(FC):.2f}", "" if lt_ is None else int(RPC[j] < r3e_pc(10.0 ** lt_))])
if MUTATE:
    base = json.load(open(os.path.join(HERE, "nd1_ceiling_results.json"))); b_ = base["grades"]; r1 = b_["native lg 9 smooth bound"]["R"][0] / GR["native lg 9 smooth bound"]["R"][0]; bite1 = abs(r1 - 0.5) < 1e-9; bite2 = PC_["cls"]["MW ultra-faint"]["Z"] > b_["native free M200 (PRIMARY)"]["cls"]["MW ultra-faint"]["Z"]; bcu = base["cusp_grades"]["zf"]["cusp lg 9, M prop r^2 (PRIMARY)"]; dcu = float(np.median([CP["cls"][c]["median"] - bcu["cls"][c]["median"] for c in CLS])); bite3 = dcu >= 0.02; bite = bite1 and bite2 and bite3
    Pn(f"MUTATE: reference-mass bound ratio {r1:.6f} (0.5 exact, R halves in the denominator): {bite1}; ultra-faint Z_C on C_N {b_['native free M200 (PRIMARY)']['cls']['MW ultra-faint']['Z']:+.2f} -> {PC_['cls']['MW ultra-faint']['Z']:+.2f}: {bite2}; cusp median E +{dcu:.3f} (>= 0.02): {bite3}: {'BITES' if bite else 'FAIL'}"); RES["mutate_bite"] = bool(bite)
if NODRAWS: Pn("NODRAWS: no JSON written")
else: json.dump(RES, open(os.path.join(HERE, f"nd1_ceiling_results{TAGOUT}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"nd1_ceiling{TAGOUT}{'_nodraws' if NODRAWS else ''}.out"), "w").write("\n".join(OUTL) + "\n"); cleanup()
if MUTATE: sys.exit(0 if RES["mutate_bite"] else 1)
sys.exit(0 if okK else 1)
