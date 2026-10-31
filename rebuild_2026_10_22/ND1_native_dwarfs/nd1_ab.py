#!/usr/bin/env python3
"""ND1_native_dwarfs parts A and B (FROZEN_CRITERIA.md): native N on the gas-rich SPARC offsets, by V_flat, the HS1 slope and LITTLE THINGS, both backgrounds; Argon's lines; K1, K2, K3; noise from X80's seeds.
    python3 nd1_ab.py            # normal run, writes nd1_ab.out, nd1_ab_results.json; exit 1 on any K failure
    python3 nd1_ab.py --mutate   # S x 0.5, writes nd1_ab_MUTATE.out, nd1_ab_results_MUTATE.json; exit 1 if it does not bite
    python3 nd1_ab.py --nodraws  # checks and central grade only, for a first look at the K lines; writes nothing but the .out
kappa = 1/2 FITTED; footings never pooled; cold dark energy, never a particle; not theory closed."""
import contextlib, io, json, math, os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
FHERE = os.path.dirname(os.path.abspath(__file__)); FRB = os.path.dirname(FHERE)
MUTATE = "--mutate" in sys.argv; NODRAWS = "--nodraws" in sys.argv; _av = sys.argv; sys.argv = [sys.argv[0]]
TAGOUT = "_MUTATE" if MUTATE else ""
# The loader runs X74's script once. __file__ is pointed here so its by-products land in this lane, not in LS1's directory; removed at the end.
LSD = os.path.join(FRB, "LS1_lstar_analogs"); _S = open(os.path.join(LSD, "ls1_analogs.py")).read(); __file__ = os.path.join(FHERE, "ls1_analogs_loader.py")
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_S[:_S.index('P("LS1 SPARC')], "ls1_head", "exec"))
HERE = FHERE; sys.argv = _av
from scipy.stats import spearmanr
def cleanup():
    for n in ("x74_fs0.034_c4_s2.7774.out", "x74_results_fs0.034_c4_s2.7774.json", "x74_x30_machinery.log", "x74_x30_machinery_MUTATE.log"):
        try: os.remove(os.path.join(FHERE, n))
        except OSError: pass
OUTL = []
def Pn(s): print(s, flush=True); OUTL.append(s)
TA, TB_ = "A_c2b_refit", "B_cfg886_bg"; TAGS = (TA, TB_)
FC = (lambda om, ob: (om - ob) / om)(0.2976016, 0.0223081 / 0.6856427 ** 2); A0 = dict(canonical=9.3603e-11, alt=1.1312e-10)
_CE0 = json.load(open(os.path.join(FRB, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; ETA_PRE = [_CE0[str(e)]["med"] for e in (12, 13, 14)]
_CE4 = json.load(open(os.path.join(FRB, "CE1_converged_eta_grade", "ce1_a4_results.json")))["eta"]; ETA_A4 = [_CE4[str(e)]["med"] for e in (12, 13, 14)]
X80 = json.load(open(os.path.join(FRB, "X80_low_mass_floor_emergence", "x80_converged.json")))
R10, R11 = X80["r10"], X80["r11"]; assert (R10, R11) == (1.1280903506658675, 0.9383778261143368), "X80's ratios changed since the criteria"
S1 = 1.25 * 0.5 * math.log10(8.05 / 5.72); S2 = 1.25 * math.log10(8.05 / 5.92); LM_CLAMP = 7.0 + math.log10(2.0); CLAMPS = {"n": 0}
def make_rule(etav, slope=None, tab=None, mut=1.0, count=False):
    """S in kg/m^2 as a function of M200 (Msun), background tag. Slope path: nf1_verify's. Table path: nf1_native_read's."""
    def Srule(M, tag):
        Mt = M / FC; lg = math.log10(Mt); trend = 10 ** float(np.interp(lg, [10.0, 11.0, 12.0], tab)) if tab is not None else 10 ** (slope * max(0.0, 12 - lg))
        if count and lg < LM_CLAMP: CLAMPS["n"] += 1
        Ms = max(Mt, 10 ** LM_CLAMP)      # sigma_coll's sigma(M) table starts at 1e7; held below, stated in the criteria
        return mut * FC * float(np.interp(lg, [12, 13, 14], etav)) * trend * sigma_coll(tag, Ms)[0] * MSUNE / PC2
    return Srule
TAB_NAT = [math.log10(R10), math.log10(R11), 0.0]
RULE_N0, RULE_N1, RULE_N2 = make_rule(ETA_PRE, slope=0.0), make_rule(ETA_PRE, slope=S1), make_rule(ETA_PRE, slope=S2)
RULE_NAT = make_rule(ETA_A4, tab=TAB_NAT, mut=0.5 if MUTATE else 1.0, count=True)
def gh(q, rule, tag, floor=None):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); M = 10 ** (bg["a"] + bg["b"] * (q["lMb"] - 10)); R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); c = rule(M, tag); c = c if floor is None else max(floor, c); r0 = solve_r0(M * MSUNE, R200, c)
    return GE * math.pi * c * r0 ** 2 * B(q["Rm"] / r0) / q["Rm"] ** 2
def pred_route(rule, tag, floor=None): return lambda q: np.log10(np.maximum(q["GB"] + gh(q, rule, tag, floor)[:, None], 1e-300))
def pred_law(f):
    def p(q): g = np.maximum(q["GB"], 1e-300); y = g / A0[f]; return np.log10(g * (0.5 + np.sqrt(0.25 + 1.0 / y)))
    return p
ALL = [q for q in GALS]; vf = {q["name"]: TAB.get(q["name"], {}).get("vf", float("nan")) for q in ALL}
fg = {q["name"]: 1.33 * q["meta"]["MHI"] / max(0.5 * q["meta"]["L36"] + 1.33 * q["meta"]["MHI"], 1e-30) for q in ALL}
GROUPS = {"all 175": ALL, "V 20-60": [q for q in ALL if 20 <= vf[q["name"]] < 60], "V 60-100": [q for q in ALL if 60 <= vf[q["name"]] < 100], "V 100-150": [q for q in ALL if 100 <= vf[q["name"]] < 150], "V 150-200": [q for q in ALL if 150 <= vf[q["name"]] < 200], "V 200-250": [q for q in ALL if 200 <= vf[q["name"]] < 250], "V 250-400": [q for q in ALL if 250 <= vf[q["name"]] < 400], "gas-dominated": [q for q in ALL if fg[q["name"]] >= 0.5], "gas >= 0.7": [q for q in ALL if fg[q["name"]] >= 0.7]}
def stats(qs, pred):
    """nf1_verify's statistic, unchanged."""
    A, Bb, C, Dd, U = 0.0, 0.0, 0.0, 0.0, []
    for q in qs:
        lgp = pred(q); wr2, ws, iu = fit_one(q, lgp); A += float(wr2); Bb += float(ws); U.append(UPS[int(iu)])
        ok, w = q["OK"][:, I05], q["W"]; r = (np.log10(q["GO"]) - lgp[:, I05])[ok]; ww = w[ok]; C += float((ww * r * r).sum()); Dd += float((ww * r).sum())
    return dict(rms_free=math.sqrt(A / Bb), rms_05=math.sqrt(C / Bb), off_05=Dd / Bb, U=float(np.median(U)), f_top=float(np.mean(np.array(U) >= 1.19)), f_bot=float(np.mean(np.array(U) <= 0.31)))
BINS = ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)); ET = json.load(open(os.path.join(FRB, "ET1_core_strength_needed", "et1_results.json")))["ups"]["0.50"]["bins"]
def bins(rule, tag):
    """nf1_bins' table; S_rule on the given background, ET1's lgM as recorded."""
    R = {}
    for lo, hi in BINS:
        qs = sel(lo, hi); U, D = [], []
        for q in qs:
            g = gh(q, rule, tag); _, _, iu = fit_one(q, np.log10(np.maximum(q["GB"] + g[:, None], 1e-300))); U.append(UPS[iu]); d = dv(q, g)
            if d is not None: D.append(d)
        k = f"{lo}-{hi}"; e = ET[k]; Sr = rule(10 ** e["lgM"], tag) / (MSUNE / PC2); R[k] = dict(n=len(qs), U=float(np.median(U)), dV=float(np.median(D)), S_rule=Sr, ET1=e["med"], ET1_ci=e["ci"], inside=bool(e["ci"][0] <= Sr <= e["ci"][1]), lgM=e["lgM"])
    return R
def S_at(rule, tag): return {f"{l}": rule(10.0 ** l, tag) / (MSUNE / PC2) for l in (8, 9, 10, 11)}
# HS1's statistic, unchanged
SBX = {}
for l in open(MRT):
    p = l.split()
    if len(p) < 18: continue
    try: SBX[p[0]] = float(p[10])
    except ValueError: pass
def iu_of(U): i = int(np.argmin(abs(UPS - U))); assert abs(UPS[i] - U) < 1e-9; return i
def delta(q, gfun, iu, fac):
    t = TAB[q["name"]]; Rk = q["Rm"] / KPC; R2 = fac * t["rd"]; ok = q["OK"][:, iu]
    if ok.sum() < 2 or R2 < Rk[ok].min() or R2 > Rk[ok].max(): return None
    Vm = np.sqrt(np.maximum(gfun(q, iu) * q["Rm"], 0.0)) / 1e3; return float(np.interp(math.log(R2), np.log(Rk[ok]), Vm[ok] / q["Vobs"][ok] - 1))
def m_route(rule, tag):
    C = {}
    def f(q, iu):
        if q["name"] not in C: C[q["name"]] = gh(q, rule, tag)
        return q["GB"][:, iu] + C[q["name"]]
    return f
def m_law(ft):
    def f(q, iu): g = q["GB"][:, iu]; return g * (0.5 + np.sqrt(0.25 + A0[ft] / np.maximum(g, 1e-300)))
    return f
def slope(x, y): x_ = x - x.mean(); return float((x_ * (y - y.mean())).sum() / (x_ * x_).sum())
def boot_s(x, y, n=10000, seed=1):
    r = np.random.default_rng(seed); b = np.empty(n)
    for i in range(n):
        k = r.integers(0, len(x), len(x)); b[i] = slope(x[k], y[k]) if np.ptp(x[k]) > 0 else np.nan
    return float((np.nanpercentile(b, 84) - np.nanpercentile(b, 16)) / 2)
def hs1(gf, want_boot=True):
    iu = iu_of(0.50); X, Y, drop = [], [], 0
    for q in sel(60, 120):
        d = delta(q, gf, iu, 2.0)
        if d is None or q["name"] not in SBX or SBX[q["name"]] <= 0: drop += 1; continue
        X.append(math.log10(SBX[q["name"]])); Y.append(d)
    X, Y = np.array(X), np.array(Y); b = slope(X, Y)
    if not want_boot: return b
    s = boot_s(X, Y); return dict(n=len(X), dropped=drop, b=b, s=s, Z=b / s, cls="FLAT" if abs(b) <= 2 * s else ("TILTED +" if b > 0 else "TILTED -"), rho=float(spearmanr(X, Y)[0]), rms=float(np.sqrt(np.mean(Y ** 2))), mean=float(Y.mean()))
# LITTLE THINGS, nf1_lt's recipe, unchanged
J_RT = json.load(open(os.path.join(FRB, "RT1_lt_rotation_regrade", "rt1_lt_rotation_regrade_results.json"))); LG = J_RT["lg"]["canonical"]
RTF = os.path.join(FRB, "RT1_lt_rotation_regrade", "rt1_lt_rotation_regrade.py"); RTT = open(RTF).read(); cutrt = 'RES = dict(criteria="ac267e8bf1"'; assert RTT.count(cutrt) == 1; RTN = {"__file__": RTF, "__name__": "rt1_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(RTT[:RTT.index(cutrt)], RTF, "exec"), RTN)
LT_ROWS = []
for nm in RTN["NAMES"]:
    d = RTN["E_rot"](RTN["rec"](nm)[0], RTN["A0"]["canonical"], "MSED")
    if d: LT_ROWS.append((nm, d))
def Ei(lMb, R_kpc, V, rule, tag):
    bg = BGS[tag]; rc = 3 * (100 * bg["h"] * 1e3 / MPCE) ** 2 / (8 * math.pi * GE); M = 10 ** (bg["a"] + bg["b"] * (lMb - 10)); R200 = (3 * M * MSUNE / (4 * math.pi * 200 * rc)) ** (1 / 3); c = rule(M, tag); r0 = solve_r0(M * MSUNE, R200, c)
    R = R_kpc * KPC; gN = GE * 10 ** lMb * MSUNE / R ** 2; gh_ = GE * math.pi * c * r0 ** 2 * B(R / r0) / R ** 2; gobs = (V * 1e3) ** 2 / R; return math.log10(gobs) - math.log10(gN + gh_), c / (MSUNE / PC2), r0 / KPC, math.log10(M)
def lt(rule, tag):
    lg = {}
    for nm, g in LG.items():
        m = g["MSED"]; e, c, r0, lM = Ei(m["logMb"], m["R"], m["V"], rule, tag); lg[nm] = dict(E=e, Z=e / m["sE"], S=c, r0=r0, lgM200=lM)
    es = np.array([Ei(d["logMb"], d["R"], d["V"], rule, tag)[0] for _, d in LT_ROWS])
    return dict(lg=lg, all=dict(n=len(es), median=float(np.median(es)), p16=float(np.percentile(es, 16)), p84=float(np.percentile(es, 84)), rms=float(np.sqrt(np.mean(es ** 2)))))
def lt_median(rule, tag): return float(np.median([Ei(d["logMb"], d["R"], d["V"], rule, tag)[0] for _, d in LT_ROWS]))
# ---------------------------------------------------------------- checks
Pn(f"ND1 parts A, B{' [MUTATE S x 0.5]' if MUTATE else ''}: native N, rho10 {R10:.4f}, rho11 {R11:.4f}, eta A4 {ETA_A4[0]:.3f}/{ETA_A4[1]:.3f}/{ETA_A4[2]:.3f}, f_c {FC:.5f}; kappa = 1/2 FITTED; footings never pooled; not theory closed")
assert abs(float(B(1.0)) - 4 * (math.asinh(1.0) - 1 / math.sqrt(2))) < 1e-12, "the loader's B is not the smooth core"
Pn(f"  loader's halo shape is the smooth core: B(1) {float(B(1.0)):.5f}; SPARC galaxies 175: {len(ALL)}, gas >= 0.7: {len(GROUPS['gas >= 0.7'])}, gas >= 0.5: {len(GROUPS['gas-dominated'])}; LITTLE THINGS with SED mass: {len(LT_ROWS)}")
V_REC = json.load(open(os.path.join(FRB, "NF1_no_floor_rule", "nf1_verify.json"))); B_REC = json.load(open(os.path.join(FRB, "NF1_no_floor_rule", "nf1_bins.json"))); L_REC = json.load(open(os.path.join(FRB, "NF1_no_floor_rule", "nf1_lt.json"))); H_REC = json.load(open(os.path.join(FRB, "HS1_hsb_lsb_residual_slope", "hs1_results.json")))["by_background"]; NR = json.load(open(os.path.join(FRB, "NF1_no_floor_rule", "nf1_native_read.json")))
def k_record(name, rule):
    """Max |d| against the record in nf1_verify, nf1_bins, nf1_lt, hs1, for rule `name`, on the pre-A4 table."""
    d = {}
    d["verify"] = max(abs(stats(qs, pred_route(rule, TA))[k] - V_REC[g][name][k]) for g, qs in GROUPS.items() for k in ("rms_free", "rms_05", "off_05", "U", "f_top", "f_bot"))
    b = bins(rule, TA); d["bins"] = max(max(abs(b[k][q] - B_REC[name][k][q]) for q in ("n", "U", "dV", "S_rule")) for k in b); sa = S_at(rule, TA); d["S_at"] = max(abs(sa[k] - B_REC[name]["S_at"][k]) for k in sa)
    t = lt(rule, TA); d["lt_lg"] = max(abs(t["lg"][nm][q] - L_REC["lg"][nm][name][q]) for nm in t["lg"] for q in ("E", "Z", "S", "r0", "lgM200")); d["lt_all"] = max(abs(t["all"][q] - L_REC["all"][name][q]) for q in ("n", "median", "p16", "p84", "rms"))
    d["hs1"] = 0.0
    for tg in TAGS:
        o = hs1(m_route(rule, tg)); d["hs1"] = max(d["hs1"], max(abs(o[q] - H_REC[tg][name][q]) for q in ("n", "b", "s", "Z", "rho", "rms", "mean")))
    return d
K = {}
if not MUTATE:
    K["K1"] = k_record("N0", RULE_N0); ok1 = max(K["K1"].values()) <= 1e-9; Pn(f"K1 rho = 1 on the pre-A4 table reproduces N0's record: " + ", ".join(f"{k} {v:.1e}" for k, v in K["K1"].items()) + f": {'PASS' if ok1 else 'FAIL'}")
    K["K2"] = k_record("N1", RULE_N1); ok2 = max(K["K2"].values()) <= 1e-9; Pn(f"K2 N1's slope {S1:.4f} on the pre-A4 table reproduces N1's record: " + ", ".join(f"{k} {v:.1e}" for k, v in K["K2"].items()) + f": {'PASS' if ok2 else 'FAIL'}")
else: ok1 = ok2 = True
# ---------------------------------------------------------------- native N, central grade
RES = dict(frozen="9230f53a67", mutate=MUTATE, rho10=R10, rho11=R11, eta_A4=ETA_A4, f_c=FC, K=K, native={}, comparators={})
for tg in TAGS:
    CLAMPS["n"] = 0
    g_ = {g: stats(qs, pred_route(RULE_NAT, tg)) for g, qs in GROUPS.items()}; b_ = bins(RULE_NAT, tg); t_ = lt(RULE_NAT, tg); h_ = hs1(m_route(RULE_NAT, tg)); sa_ = S_at(RULE_NAT, tg)
    RES["native"][tg] = dict(groups=g_, bins=b_, lt=t_, hs1=h_, S_at=sa_, n_clamped=CLAMPS["n"])
    _lgt = lambda lMb: BGS[tg]["a"] + BGS[tg]["b"] * (lMb - 10) - math.log10(FC); RES["native"][tg]["below_1e10"] = dict(gas7=int(sum(_lgt(q["lMb"]) < 10 for q in GROUPS["gas >= 0.7"])), gas5=int(sum(_lgt(q["lMb"]) < 10 for q in GROUPS["gas-dominated"])), sparc=int(sum(_lgt(q["lMb"]) < 10 for q in ALL)), lt=int(sum(_lgt(d["logMb"]) < 10 for _, d in LT_ROWS)))
    Pn(f"native N on {tg}: below X80's lowest zoom (lg M_t < 10, rho held at rho10): gas >= 0.7 {RES['native'][tg]['below_1e10']['gas7']}/41, gas >= 0.5 {RES['native'][tg]['below_1e10']['gas5']}/81, SPARC {RES['native'][tg]['below_1e10']['sparc']}/175, LITTLE THINGS {RES['native'][tg]['below_1e10']['lt']}/20")
    Pn(f"native N on {tg}: SPARC U {g_['all 175']['U']:.2f}, rms {g_['all 175']['rms_free']:.4f} free, {g_['all 175']['rms_05']:.4f} at 0.50; S at lg M200 8/9/10/11: " + " / ".join(f"{v:.1f}" for v in sa_.values()) + f"; evaluations below the Sigma_coll clamp {CLAMPS['n']}")
    for g, s in g_.items(): Pn(f"    {g:14s} n {len(GROUPS[g]):3d} rms {s['rms_free']:.4f} / {s['rms_05']:.4f}; offset at 0.50 {s['off_05']:+.3f}; U {s['U']:.2f}; at top {s['f_top']:.2f}, at bottom {s['f_bot']:.2f}")
    for k, s in b_.items(): Pn(f"    sel {k:8s} n {s['n']:2d} lg M200 {s['lgM']:.2f} U {s['U']:.2f} dV {s['dV']:+.1f}; S_rule {s['S_rule']:.0f} vs ET1 {s['ET1']:.0f} [{s['ET1_ci'][0]:.0f},{s['ET1_ci'][1]:.0f}] {'inside' if s['inside'] else 'outside'}")
    Pn(f"    HS1 slope: n {h_['n']} (dropped {h_['dropped']}), b {h_['b']:+.4f} +- {h_['s']:.4f} per dex ({h_['Z']:+.2f} sigma) {h_['cls']}; Spearman {h_['rho']:+.3f}; mean delta {h_['mean']:+.3f}, rms {h_['rms']:.3f}")
    Pn(f"    LITTLE THINGS n {t_['all']['n']}: median E {t_['all']['median']:+.3f} [{t_['all']['p16']:+.3f}, {t_['all']['p84']:+.3f}], rms {t_['all']['rms']:.3f}; " + "; ".join(f"{nm} {w['E']:+.3f} ({w['Z']:+.1f}, S {w['S']:.0f}, lg M200 {w['lgM200']:.2f})" for nm, w in t_["lg"].items()))
if not MUTATE:
    dk = max(abs(RES["native"][TA]["bins"][k][q] - NR["bins"][k][q]) for k in NR["bins"] for q in ("n", "U", "dV", "S_rule")); drms = max(abs(RES["native"][tg]["groups"]["all 175"]["rms_free"] - NR["sparc"][tg]["rms"]) for tg in TAGS); dU = max(abs(RES["native"][tg]["groups"]["all 175"]["U"] - NR["sparc"][tg]["U"]) for tg in TAGS); ok3 = dk <= 1e-9 and drms <= 1e-4 and dU <= 0.01
    K["K3"] = dict(bins=dk, grader_rms=drms, grader_U=dU); Pn(f"K3 native N reproduces nf1_native_read's bins {dk:.1e} (1e-9), its grader-path SPARC rms {drms:.1e} (1e-4), Upsilon {dU:.3f} (0.01): {'PASS' if ok3 else 'FAIL'}")
else: ok3 = True
# ---------------------------------------------------------------- comparators on background B, reported (the record has A); pre-A4 table as the record
if not MUTATE and not NODRAWS:
    SIGF = {f: SIG[f] for f in ("canonical", "alt")}; CMP = {"F canonical": pred_route(RULE_N0, TB_, SIGF["canonical"]), "F alt": pred_route(RULE_N0, TB_, SIGF["alt"]), "N0": pred_route(RULE_N0, TB_), "N1": pred_route(RULE_N1, TB_), "N2": pred_route(RULE_N2, TB_), "law canonical": pred_law("canonical"), "law alt": pred_law("alt")}
    for k, pr in CMP.items():
        RES["comparators"][k] = {g: stats(GROUPS[g], pr) for g in ("all 175", "gas-dominated", "gas >= 0.7")}; c_ = RES["comparators"][k]; Pn(f"  comparator on B, {k:14s}: U {c_['all 175']['U']:.2f}, rms {c_['all 175']['rms_free']:.4f}; offset gas >= 0.5 {c_['gas-dominated']['off_05']:+.3f}, gas >= 0.7 {c_['gas >= 0.7']['off_05']:+.3f}")
    for nm, rr in (("N0", RULE_N0), ("N1", RULE_N1), ("N2", RULE_N2)):
        t = lt(rr, TB_); RES["comparators"][nm]["lt"] = t["all"]; Pn(f"  comparator on B, {nm} LITTLE THINGS median E {t['all']['median']:+.3f}, rms {t['all']['rms']:.3f}")
# ---------------------------------------------------------------- Argon's lines
def lines_of(n):
    L = {}
    for tg in TAGS:
        a = n[tg]["groups"]["all 175"]; L[tg] = dict(sparc=(a["rms_free"] <= 0.110 and 0.50 <= a["U"] <= 0.80), offset=(abs(n[tg]["groups"]["gas >= 0.7"]["off_05"]) <= 0.07), lt=(abs(n[tg]["lt"]["all"]["median"]) <= 0.10))
    return L
LINES = lines_of(RES["native"]); RES["lines"] = LINES
NAMES_L = dict(sparc="SPARC line", offset="gas >= 0.7 offset", lt="LITTLE THINGS median E")
fails = [k for k in NAMES_L if not all(LINES[tg][k] for tg in TAGS)]; bgdep = [k for k in NAMES_L if LINES[TA][k] != LINES[TB_][k]]
lab = "ARGON'S LINES PASS" if not fails else "ARGON'S LINES FAIL: " + ", ".join(NAMES_L[k] for k in fails); lab += " [BACKGROUND-DEPENDENT]" if bgdep else ""
# ---------------------------------------------------------------- noise, X80's seeds
if not MUTATE and not NODRAWS:
    SUM = X80["summary"]; PR = [np.array(SUM[k]["per_run"]) for k in ("1e+10_ng64", "1e+11_ng64", "1e+12_ng64")]; assert all(len(p) == 9 for p in PR); IDX = np.random.default_rng(20261031).integers(0, 9, (200, 3, 9)); ND = []; TGAS7, TGAS5 = GROUPS["gas >= 0.7"], GROUPS["gas-dominated"]
    for d in range(200):
        e10, e11, e12 = [float(np.median(PR[j][IDX[d, j]])) for j in range(3)]; rule = make_rule([e12, ETA_A4[1], ETA_A4[2]], tab=[math.log10(e10 / e12), math.log10(e11 / e12), 0.0]); row = dict(r10=e10 / e12, r11=e11 / e12)
        for tg in TAGS:
            _c = {}; _p = pred_route(rule, tg)
            def pr(q, _c=_c, _p=_p):
                if q["name"] not in _c: _c[q["name"]] = _p(q)
                return _c[q["name"]]
            a = stats(ALL, pr); row[tg] = dict(U=a["U"], rms=a["rms_free"], off7=stats(TGAS7, pr)["off_05"], off5=stats(TGAS5, pr)["off_05"], lt=lt_median(rule, tg))
        row["hs1"] = hs1(m_route(rule, TA), want_boot=False); ND.append(row)
        if (d + 1) % 25 == 0: print(f"  noise draw {d + 1}/200", flush=True)
    NS_ = {}
    for tg in TAGS:
        same = dict(sparc=np.mean([(x[tg]["rms"] <= 0.110 and 0.50 <= x[tg]["U"] <= 0.80) == LINES[tg]["sparc"] for x in ND]), offset=np.mean([(abs(x[tg]["off7"]) <= 0.07) == LINES[tg]["offset"] for x in ND]), lt=np.mean([(abs(x[tg]["lt"]) <= 0.10) == LINES[tg]["lt"] for x in ND]))
        q = lambda k: [float(v) for v in np.percentile([x[tg][k] for x in ND], [16, 50, 84])]
        NS_[tg] = dict(same={k: float(v) for k, v in same.items()}, U=q("U"), off7=q("off7"), off5=q("off5"), lt=q("lt"))
        Pn(f"  noise on {tg}, 200 draws of X80's seeds, 68 %: U [{NS_[tg]['U'][0]:.2f}, {NS_[tg]['U'][2]:.2f}]; offset gas >= 0.7 [{NS_[tg]['off7'][0]:+.3f}, {NS_[tg]['off7'][2]:+.3f}], gas >= 0.5 [{NS_[tg]['off5'][0]:+.3f}, {NS_[tg]['off5'][2]:+.3f}]; LITTLE THINGS median E [{NS_[tg]['lt'][0]:+.3f}, {NS_[tg]['lt'][2]:+.3f}]; outcome held in: SPARC line {same['sparc']:.2f}, offset {same['offset']:.2f}, LITTLE THINGS {same['lt']:.2f}")
    hsn = [float(v) for v in np.percentile([x["hs1"] for x in ND], [16, 50, 84])]; Pn(f"  noise, HS1 slope on A, 68 %: [{hsn[0]:+.4f}, {hsn[2]:+.4f}], every draw's class at the central sigma: TILTED in {np.mean([abs(x['hs1']) > 2 * RES['native'][TA]['hs1']['s'] for x in ND]):.2f} of draws")
    RES["noise"] = dict(tags=NS_, hs1=hsn, tilted=float(np.mean([abs(x["hs1"]) > 2 * RES["native"][TA]["hs1"]["s"] for x in ND])), r10=[float(v) for v in np.percentile([x["r10"] for x in ND], [16, 50, 84])], r11=[float(v) for v in np.percentile([x["r11"] for x in ND], [16, 50, 84])], draws=ND)
    if min(v for tg in TAGS for v in NS_[tg]["same"].values()) < 0.68: lab += " [NOISE-LIMITED]"
okc = ok1 and ok2 and ok3
RES["label"] = lab if okc else f"NOT DECIDED ({lab})"; RES["hs1_class"] = RES["native"][TA]["hs1"]["cls"]
Pn(f"Argon's window on rho10 (pass 1.15-1.85, fail below 1.10 or above 1.90): rho10 {R10:.3f} is {'in the pass window' if 1.15 <= R10 <= 1.85 else 'in neither' if 1.10 <= R10 < 1.15 else 'in the fail range'}")
for tg in TAGS: Pn(f"  lines on {tg}: " + ", ".join(f"{NAMES_L[k]} {'pass' if LINES[tg][k] else 'FAIL'}" for k in NAMES_L))
Pn(f"LABEL: {RES['label']}; HS1 slope on A: {RES['hs1_class']}")
if MUTATE:
    base = json.load(open(os.path.join(HERE, "nd1_ab_results.json")))["native"]; m_ = RES["native"]
    b1 = all(m_[tg]["groups"]["all 175"]["U"] > base[tg]["groups"]["all 175"]["U"] for tg in TAGS); b2 = m_[TA]["groups"]["gas >= 0.7"]["off_05"] - base[TA]["groups"]["gas >= 0.7"]["off_05"]; b3 = m_[TA]["lt"]["all"]["median"] - base[TA]["lt"]["all"]["median"]; bite = b1 and b2 >= 0.02 and b3 >= 0.02
    Pn(f"MUTATE S x 0.5: U {[round(base[tg]['groups']['all 175']['U'], 2) for tg in TAGS]} -> {[round(m_[tg]['groups']['all 175']['U'], 2) for tg in TAGS]}; gas >= 0.7 offset +{b2:.3f}; LITTLE THINGS median E +{b3:.3f}: {'BITES' if bite else 'FAIL'}"); RES["mutate_bite"] = bool(bite)
if not NODRAWS or MUTATE:
    json.dump(RES, open(os.path.join(HERE, f"nd1_ab_results{TAGOUT}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"nd1_ab{TAGOUT}{'_nodraws' if NODRAWS else ''}.out"), "w").write("\n".join(OUTL) + "\n"); cleanup()
if MUTATE: sys.exit(0 if RES["mutate_bite"] else 1)
sys.exit(0 if okc else 1)
