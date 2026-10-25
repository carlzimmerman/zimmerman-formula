"""NU1_cluster_gap_sources (criteria ee69137b45): can independently bounded ordinary mass (massive neutrinos, hidden baryons)
close the eRASS1 x KiDS cluster-core gap of F1 / X2 / X7 without a new fitted constant?
Inputs (read-only): X2's source (F1's functions, statistics, gas, EFE, model exec'd from its text, as X7 does), X2's replay npz
(= F1's measurement), X7's analysis JSON (CAL systematic terms), X2's JSON (K1).  Usage: nu1_cluster_gap_sources.py [--mutate]
--mutate: Tremaine-Gunn density uses v_esc^-3 (K4 must FAIL) and the CAL rescaling uses a mis-scaled denominator (K6 must FAIL).
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle adopted; not theory closed."""
import os, sys
if os.environ.get("MallocMediumZone") != "0":
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "MallocMediumZone": "0"})
import json, math, time, hashlib, resource
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"nu1_cluster_gap_sources{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
# ============================================================== X2's functions (exec'd read-only, same cuts as X7)
X2DIR = os.path.join(REB, "X2_cluster_outskirts"); X2SRC = os.path.join(X2DIR, "x2_cluster_outskirts.py"); TX = open(X2SRC).read()
X7DIR = os.path.join(REB, "X7_cluster_core_significance"); X7J = json.load(open(os.path.join(X7DIR, "x7_analysis_results.json")))
RES["x2_source_sha256"] = sha(X2SRC); RES["x7_json_sha256"] = sha(os.path.join(X7DIR, "x7_analysis_results.json"))
def cutx(a, b): i = TX.index(a); j = TX.index(b, i); return TX[i:j]
NS2 = {"np": np, "os": os, "sys": sys, "math": math, "json": json, "time": time, "REB": REB, "REPO": REPO, "HERE": X2DIR,
       "LANES": os.path.join(REPO, "campaign_fresh_gravity"), "MUT": False, "RES": {}, "say": (lambda *a: None), "check": (lambda *a: None),
       "sha": sha, "rss": rss, "guard": (lambda tag: None)}
exec(cutx("# ============================================================== F1's own functions", "# ============================================================== data: the replay"), NS2)
exec(cutx("# ============================================================== data: the replay", "# ============================================================== statistics"), NS2)
exec(cutx("# ============================================================== statistics", "# ============================================================== EFE"), NS2)
exec(cutx('sys.path.insert(0, os.path.join(REB, "F2_outer_lensing"))', 'for f in FEET:\n    for k in ("noclu", "maxclu", "p2cat"):'), NS2)
exec(cutx("# ============================================================== the model", "# ============================================================== K2, K3, K7"), NS2)
G, MSUN, MPC, KG_PC2, A0 = NS2["G"], NS2["MSUN"], NS2["MPC"], NS2["KG_PC2"], NS2["A0"]
RG, RC, RM, BANDS = NS2["RG"], NS2["RC"], NS2["RM"], NS2["BANDS"]
DM, DA_lcdm, g_aqual_sph = NS2["DM"], NS2["DA_lcdm"], NS2["g_aqual_sph"]
project_floor, offset_floor, sig_bins, dsig_from_sig, at_bins, gas = (NS2[k] for k in ("project_floor", "offset_floor", "sig_bins", "dsig_from_sig", "at_bins", "gas"))
CTAB, Cof, redfac, HV = NS2["CTAB"], NS2["Cof"], NS2["redfac"], NS2["HV"]
FEET, HK = ("canonical", "alt"), ("h0672", "h0686"); CELLS = [(f, h) for f in FEET for h in HK]; BN = ("INNER", "MID", "OUTER")
for f in FEET:
    t1 = time.time(); CTAB[(f, "noclu")] = NS2["ctable"](NS2["AQ"].solve_efe(NS2["YE"][f]["noclu"], maxit=3000))
    say(f"EFE solve (X2's) {f} noclu: iters {CTAB[(f, 'noclu')]['iters']} [{time.time()-t1:.0f} s]")
CL, DAT, PATCH, N = NS2["CL"], NS2["DAT"], NS2["PATCH"], NS2["N"]
Mg_cat = np.array([c["Mgas500"] for c in CL])
q3 = np.array(X7J["mass"]["q3"]); TID = np.digitize(Mg_cat, q3); TERC = {f"T{t+1}": TID == t for t in range(3)}; ALL = np.ones(N, bool)
CSTAR = dict(gasshape="P", efe="noclu", red=True)
say(f"clusters {N}; tercile edges {q3/1e12} e12 Msun (X7); n per tercile {[int(v.sum()) for v in TERC.values()]}")
# ============================================================== physical constants for the neutrino sector
EV = 1.602176634e-19; C_L = 2.99792458e8; H_P = 6.62607015e-34; EV_KG = EV/C_L**2
OBH2 = 0.0222                                    # BBN deuterium (PROVISIONAL external fact)
NU_SETS = {"N0 osc-min NO": 0.0588, "N0i osc-min IO": 0.0995, "Nrec record 0.0613": 0.0613, "NK KATRIN 3x0.45": 1.35}
def masses(label, S):
    if label.startswith("NK"): return [0.45, 0.45, 0.45]
    if "IO" in label: m3 = 0.0; m1 = math.sqrt(2.5e-3 - 7.4e-5); return [m1, math.sqrt(m1**2 + 7.4e-5), m3]
    if "record" in label: m1 = 2.24e-3
    else: m1 = 0.0
    return [m1, math.sqrt(m1**2 + 7.4e-5), math.sqrt(m1**2 + 2.5e-3)]
def tg_rho(m_ev, v):
    """fine-grained Tremaine-Gunn cap per flavour (nu + nubar, f <= 1/2 per helicity state): rho = m (4 pi/3) (m v / h)^3, kg/m^3."""
    m = m_ev*EV_KG; p = m*np.asarray(v, float)
    if MUT: p = m*np.maximum(np.asarray(v, float), 1.0)**-3*1e18                 # MUTATE: wrong power of v
    return m*(4*np.pi/3)*(p/H_P)**3
def vesc2(g, Rta):
    """v_esc^2(r) = 2 int_r^Rta g dr on RG (zero beyond Rta)."""
    gi = np.where(RG <= Rta, g, 0.0); seg = 0.5*(gi[1:] + gi[:-1])*np.diff(RM)
    return 2*np.r_[np.cumsum(seg[::-1])[::-1], 0.0]
def cummass(rho):
    dm = 4*np.pi*RM**2*rho; return np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(RM))]
# ============================================================== the model: X2's non-DEB branch + added sources in M_src
def model_add(cl, foot, hk, gasshape="G0", efe=None, red=False, gfac=1.0, fstar=0.20, Mcold=0.0, nu=None, lamgas=0.0, info=None):
    h = HV[hk]; a0 = A0[foot]; q = (float(DM(cl["z"], h))/(1 + cl["z"]))/DA_lcdm(cl["z"])
    Mg500 = cl["Mgas500"]*q**2.5; R500 = cl["R500"]*q
    Mg, rho_g = gas(Mg500, R500, gasshape); Mb = Mg*(gfac + fstar); Msrc = Mb.copy()
    if lamgas: Msrc = Msrc + lamgas*Mg
    Mpt = Mcold*MSUN; Msrc = Msrc + Mpt
    Mnu = np.zeros_like(RG)
    if nu is not None:
        ms, mode, Rta = nu; ratio = sum(ms)/93.14/OBH2; i3 = np.searchsorted(RG, 3.0); cap = ratio*Mb[min(i3, len(RG) - 1)]
        rho_b = np.gradient(Mb, RM)/(4*np.pi*RM**2)
        for _ in range(8):
            gg = g_aqual_sph(G*np.maximum(Msrc + Mnu, 1e-30)/RM**2, a0); v = np.sqrt(np.maximum(vesc2(gg, Rta), 0.0))
            rtg = sum(tg_rho(m, v) for m in ms)
            if mode == "max": Mn = np.minimum(cummass(rtg), cap)
            else: Mn = np.minimum(cummass(np.minimum(rtg, ratio*rho_b)), cap)
            if np.max(np.abs(Mn - Mnu)) <= 1e-6*max(cap, 1.0): Mnu = Mn; break
            Mnu = Mn
        if info is not None:
            info.update(cap=cap/MSUN, M05=float(np.interp(0.5, RG, Mnu))/MSUN, M1=float(np.interp(1.0, RG, Mnu))/MSUN, M3=float(Mnu[-1])/MSUN,
                        Mb1=float(np.interp(1.0, RG, Mb))/MSUN, vesc05=float(np.interp(0.5, RG, v))/1e3,
                        tgM1=float(np.interp(1.0, RG, cummass(rtg)))/MSUN, rtg_over_cap=float(np.all(rtg >= 0)), rho_ok=float(np.all(np.diff(Mnu) <= np.diff(cummass(rtg))*(1 + 1e-9) + 1e-30*MSUN)))
        Msrc = Msrc + Mnu
    gN = G*Msrc/RM**2; g = g_aqual_sph(gN, a0)
    if efe is not None:
        tab = CTAB[(foot, efe)]; s = RG/(math.sqrt(G*float(np.interp(3.0, RG, Msrc))/a0)/MPC); g = g*Cof(tab, s)
    ML = g*RM**2/G - Mpt
    rho = np.gradient(ML, RM)/(4*np.pi*RM**2)
    Sig = project_floor(rho); d = np.radians(cl["off_deg"])*float(DM(cl["z"], h))/(1 + cl["z"])
    So = offset_floor(Sig, d); P = at_bins(dsig_from_sig(So))/KG_PC2; Sb = sig_bins(So)
    if Mpt > 0: P = P + np.where(RC > d, Mpt/(np.pi*(RC*MPC)**2), 0.0)/KG_PC2
    return P, Sb
def stack_add(foot, hk, model="C*", infos=None, **kw):
    base = CSTAR if model == "C*" else {}; P = np.empty((N, 8))
    for i, cl in enumerate(CL):
        inf = {} if infos is not None else None
        p, sb = model_add(cl, foot, hk, info=inf, **base, **kw)
        if base.get("red"): p = p*redfac(hk, i, sb)[0]
        P[i] = p
        if infos is not None: infos.append(inf)
    if rss() > 0.95: say("RSS GUARD"); sys.exit(3)
    return P
# ============================================================== statistics: X7's ratio estimators, bootstrap seeds, CAL rescaling
RNGBASE = 20261024; BOOTIDX = {}
def bsum(X, Wb, b): j = BANDS[b]; return (X[:, j]*Wb[:, j]).sum(-1)
def ratio(num, den, sel): return float(num[sel].sum()/den[sel].sum())
def jk(num, den, sel):
    reps = [ratio(num, den, sel & (PATCH != p)) for p in range(30) if (sel & (PATCH != p)).sum() < sel.sum()]
    n = len(reps); return float(np.sqrt((n - 1)/n*np.sum((np.array(reps) - np.mean(reps))**2)))
def boot(num, den, sel, key):
    if key not in BOOTIDX:
        rng = np.random.default_rng([RNGBASE, key]); BOOTIDX[key] = rng.integers(0, int(sel.sum()), size=(2000, int(sel.sum())))
    nn, dd = num[sel][BOOTIDX[key]], den[sel][BOOTIDX[key]]; return float(np.std(nn.sum(1)/dd.sum(1), ddof=1))
def x7ref(f, hk, sel_name, band):
    """X7's reference quantities for a selection: A, A_CAL, s_STAT, s_CAL (all-cluster: summ; tercile: summ + graded trend sig)."""
    if sel_name == "ALL":
        q = X7J["all"][f"C*|boost|{f}|{hk}"][band]; return dict(A=q["A"], A_CAL=q["A_CAL"], s_STAT=q["s_STAT"], s_CAL=q["s_CAL"])
    k = int(sel_name[1]) - 1; q = X7J["bins"][f"terciles|{f}|{hk}"][k][band]; tr = X7J["trend"][f"terciles|{f}|{hk}|{band}|CAL"]
    return dict(A=q["A"], A_CAL=tr["A"][k], s_STAT=q["s_STAT"], s_CAL=tr["sig"][k])
SELS = {"ALL": (ALL, 0), "T1": (TERC["T1"], 200), "T2": (TERC["T2"], 201), "T3": (TERC["T3"], 202)}
PBASE = {}
def score(f, hk, P, model="C*"):
    d = DAT[hk]; WB = d["W"]*d["B"][None, :]; out = {}
    Pold = PBASE[(model, f, hk)]
    for sn, (sel, key) in SELS.items():
        out[sn] = {}
        for b in ("MID", "OUTER"):
            num = bsum(d["D"], WB, b); den = bsum(P, d["W"], b); den0 = bsum(Pold, d["W"], b)
            r = float(den0[sel].sum()/den[sel].sum())
            if MUT: r *= 1.1                                                          # MUTATE: mis-scaled denominator
            A = ratio(num, den, sel); sst = max(jk(num, den, sel), boot(num, den, sel, key))
            o = dict(A=A, s_STAT=sst, r=r)
            if model == "C*":
                ref = x7ref(f, hk, sn, b); ssys2 = max(ref["s_CAL"]**2 - ref["s_STAT"]**2, 0.0)
                o["A_CAL"] = ref["A_CAL"]*r; o["s_CAL"] = math.sqrt(sst**2 + r**2*ssys2); o["Z_CAL"] = (o["A_CAL"] - 1)/o["s_CAL"]
            o["Z_STAT"] = (A - 1)/sst
            out[sn][b] = o
    return out
# ============================================================== K4: Tremaine-Gunn unit tests
m_t, v_t = 2.0, 2.0e6
pp = np.linspace(0, m_t*EV_KG*v_t, 200001); n_num = 2*np.trapz(0.5*4*np.pi*pp**2, pp)/H_P**3; n_cf = (4*np.pi/3)*(m_t*EV_KG*v_t/H_P)**3
hc = 1.23984198e-6; pc = m_t*v_t/C_L; rho_hand = m_t*EV_KG*(4*np.pi/3)*(pc/hc)**3
k4a = abs(n_num/n_cf - 1); k4b = abs(float(tg_rho(m_t, v_t))/rho_hand - 1)
check("K4", k4a <= 1e-6 and k4b <= 1e-6, f"Fermi sphere numeric/closed {k4a:.1e}; tg_rho(2 eV, 2000 km/s) vs hand {k4b:.1e} (rho {rho_hand:.3e} kg/m3)", "<= 1e-6; <= 1e-6")
RES["TG_example"] = dict(m_eV=2.0, v_kms=2000, rho_kg_m3=rho_hand)
# ============================================================== baselines and K1 / K2 / K3 / K6
for f, hk in CELLS:
    PBASE[("C*", f, hk)] = stack_add(f, hk, "C*"); PBASE[("C0", f, hk)] = stack_add(f, hk, "C0")
say(f"baselines built [{time.time()-T0:.0f} s]")
dev1, dev1s, dev2 = [], [], []
X2J = json.load(open(os.path.join(X2DIR, "x2_cluster_outskirts_results.json")))
BASE = {}
for f, hk in CELLS:
    sc = score(f, hk, PBASE[("C*", f, hk)]); BASE[(f, hk)] = sc
    for sn in SELS:
        for b in ("MID", "OUTER"):
            ref = x7ref(f, hk, sn, b); o = sc[sn][b]
            dev1 += [abs(o["A"] - ref["A"])]; dev1s += [abs(o["s_STAT"] - ref["s_STAT"])]
            dev2 += [abs(o["A_CAL"] - ref["A_CAL"]), abs(o["s_CAL"] - ref["s_CAL"]), abs(o["Z_CAL"] - (ref["A_CAL"] - 1)/ref["s_CAL"])]
    s0 = score(f, hk, PBASE[("C0", f, hk)], "C0")
    for t in ("T1", "T2", "T3"):
        dev1 += [abs(s0[t]["MID"]["A"] - X2J["terciles"]["C0"][t]["boost"][f"{f}|{hk}"]["MID"]["A"])]
check("K1", max(dev1) <= 1e-6 and max(dev1s) <= 1e-6, f"A vs X7 (C*, all + terciles) and X2 C0 terciles: max {max(dev1):.1e}; s_STAT vs X7 {max(dev1s):.1e}", "<= 1e-6")
check("K2", max(dev2) <= 1e-6, f"rescaled CAL with no added mass vs X7 A_CAL / s_CAL / Z_CAL: max {max(dev2):.1e}", "<= 1e-6")
lam3 = 0.7; Pm = stack_add("canonical", "h0672", "C*", lamgas=lam3); Px = NS2["stack_model"]("canonical", "h0672", comp="GS", lam=lam3, **CSTAR)[0]
k3 = float(np.max(np.abs(Pm/Px - 1)))
check("K3", k3 <= 1e-10, f"lam x gas (lam {lam3}) vs X2 comp GS: max rel {k3:.1e}", "<= 1e-10")
P6 = stack_add("canonical", "h0672", "C*", gfac=1.5); s6 = score("canonical", "h0672", P6); d6 = DAT["h0672"]
k6 = max(abs(s6[sn][b]["A"]/BASE[("canonical", "h0672")][sn][b]["A"] - s6[sn][b]["r"]) for sn in SELS for b in ("MID", "OUTER"))
check("K6", k6 <= 1e-12, f"planted gas x 1.5: A_new/A_old vs rescale factor max |diff| {k6:.1e}", "<= 1e-12")
# ============================================================== rows
ROWS = {}
def row(label, model="C*", **kw):
    out = {}; infos = {}
    for f, hk in CELLS:
        inf = [] if "nu" in kw else None
        P = stack_add(f, hk, model, infos=inf, **kw); out[f"{f}|{hk}"] = score(f, hk, P, model)
        if inf is not None: infos[f"{f}|{hk}"] = inf
    ROWS[(label, model)] = out
    say(f"{model} {label}")
    for f, hk in CELLS:
        o = out[f"{f}|{hk}"]; z = "Z_CAL" if model == "C*" else "Z_STAT"; a = "A_CAL" if model == "C*" else "A"; s = "s_CAL" if model == "C*" else "s_STAT"
        say(f"   {f[:3]} {hk}: " + "  ".join(f"{sn} MID {o[sn]['MID'][a]:.3f}+-{o[sn]['MID'][s]:.3f} ({o[sn]['MID'][z]:+.2f}) OUT {o[sn]['OUTER'][a]:.3f} ({o[sn]['OUTER'][z]:+.2f})" for sn in SELS))
    if infos:
        inf = infos["canonical|h0672"]
        say("   nu (can h0672) medians: cap {:.2e}  M(<0.5) {:.2e}  M(<1) {:.2e}  M(<3) {:.2e} Msun; M_nu(<1)/M_b(<1) {:.3f}; TG mass (<1) {:.2e}; v_esc(0.5) {:.0f} km/s".format(
            *[float(np.median([e[k] for e in inf])) for k in ("cap", "M05", "M1", "M3")], float(np.median([e["M1"]/e["Mb1"] for e in inf])),
            float(np.median([e["tgM1"] for e in inf])), float(np.median([e["vesc05"] for e in inf]))))
        for tn, sel in TERC.items():
            say(f"      {tn}: median M_nu(<1)/M_b(<1) {np.median([inf[i]['M1']/inf[i]['Mb1'] for i in np.where(sel)[0]]):.3f}, TG/cap at 1 Mpc {np.median([inf[i]['tgM1']/inf[i]['cap'] for i in np.where(sel)[0]]):.3f}")
        ROWS[(label, model)]["nu_info"] = {c: {k: float(np.median([e[k] for e in v])) for k in ("cap", "M05", "M1", "M3", "Mb1", "tgM1", "vesc05")} for c, v in infos.items()}
        ROWS[(label, model)]["nu_rho_ok"] = bool(all(e["rho_ok"] == 1.0 and e["M3"] <= e["cap"]*(1 + 1e-9) for v in infos.values() for e in v))
    return out
say("\n=== rows (C* graded with X7 CAL errors; A_CAL +- s_CAL (Z_CAL) per selection) ===")
row("R0 baseline")
for lab, S in NU_SETS.items():
    row(f"{lab} maximal (TG-filled to the fair-share cap, R_ta 5 Mpc)", nu=(masses(lab, S), "max", 5.0))
NKm = masses("NK", 1.35)
row("NK tracing baryons (fair share, TG-capped)", nu=(NKm, "trace", 5.0))
row("NK maximal, R_ta 3 Mpc", nu=(NKm, "max", 3.0)); row("NK maximal, R_ta 10 Mpc", nu=(NKm, "max", 10.0))
row("B1 gas x 1.236 (X-COP)", gfac=1.236)
row("B1-extreme gas x 1.50 (CFG922 rho_84; bracket)", gfac=1.50)
row("B2 f* 0.30 (incl. ICL)", fstar=0.30)
row("B3 cold gas 2e11 Msun central", Mcold=2e11)
row("B1+B2+B3 hidden baryons at allowed max", gfac=1.236, fstar=0.30, Mcold=2e11)
COMB = row("ALLOWED-MAX COMBINATION (NK maximal + B1 + B2 + B3)", gfac=1.236, fstar=0.30, Mcold=2e11, nu=(NKm, "max", 5.0))
row("EXTREME (NK maximal + gas x1.50 + B2 + B3; bracket)", gfac=1.50, fstar=0.30, Mcold=2e11, nu=(NKm, "max", 5.0))
say("\n=== C0 (F1 PRIMARY model, STAT errors; reported) ===")
row("R0 baseline", "C0"); row("ALLOWED-MAX COMBINATION", "C0", gfac=1.236, fstar=0.30, Mcold=2e11, nu=(NKm, "max", 5.0))
nuok = all(ROWS[k]["nu_rho_ok"] for k in ROWS if "nu_rho_ok" in ROWS[k])
check("K5", nuok, f"every nu row: M_nu(<3 Mpc) <= cap and rho_nu <= rho_TG at every radius, all clusters and cells: {nuok}", "True")
# ============================================================== sterile-neutrino requirement (reported, a NEW constant, never adopted)
say("\n=== sterile neutrino the gap would need (NEW constant; reported only) ===")
STER = {}
for f, hk in CELLS:
    STER[f"{f}|{hk}"] = {}
    for sn in ("ALL", "T2", "T3"):
        def resid(lam):
            P = stack_add(f, hk, "C*", lamgas=lam) if lam > 0 else PBASE[("C*", f, hk)]
            return score(f, hk, P)[sn]["MID"]["A_CAL"] - 1
        lam = brentq(resid, 0.0, 6.0, xtol=1e-3) if resid(0.0) > 0 else 0.0
        P = stack_add(f, hk, "C*", lamgas=lam); so = score(f, hk, P)[sn]
        # TG minimum single-species mass (g f = 1) for the needed density lam*rho_gas inside 1 Mpc, per cluster in the selection
        sel = SELS[sn][0]; mreq = []; m05 = []
        for i in np.where(sel)[0]:
            cl = CL[i]; h = HV[hk]; q = (float(DM(cl["z"], h))/(1 + cl["z"]))/DA_lcdm(cl["z"])
            Mg, rho_g = gas(cl["Mgas500"]*q**2.5, cl["R500"]*q, "P"); Ms = Mg*(1.2 + lam)
            v = np.sqrt(vesc2(g_aqual_sph(G*Ms/RM**2, A0[f]), 5.0)); ins = (RG >= 0.05) & (RG <= 1.0)
            need = lam*rho_g[ins]; m4 = need*H_P**3/((4*np.pi/3)*v[ins]**3*EV_KG**4)
            mreq.append(float(np.max(m4))**0.25); m05.append(float(np.interp(0.5, RG, Mg))/MSUN*lam)
        Mn05 = float(np.median(m05))
        STER[f"{f}|{hk}"][sn] = dict(lam_gas=lam, Omega_s_over_Omega_b=lam/1.2, Omega_s_h2=lam/1.2*OBH2, m_thermal_eV=93.14*lam/1.2*OBH2,
                                     m_TG_min_eV_median=float(np.median(mreq)), OUTER_A_CAL=so["OUTER"]["A_CAL"], OUTER_Z_CAL=so["OUTER"]["Z_CAL"], M05_median=Mn05)
        s = STER[f"{f}|{hk}"][sn]
        say(f"   {f[:3]} {hk} {sn}: needed lam x gas {lam:.3f} -> Omega_s/Omega_b >= {s['Omega_s_over_Omega_b']:.2f} (Omega_s h2 {s['Omega_s_h2']:.4f}; thermal-relic mass {s['m_thermal_eV']:.2f} eV);"
            f" TG minimum mass (g f = 1, median cluster) {s['m_TG_min_eV_median']:.2f} eV; OUTER then {so['OUTER']['A_CAL']:.3f} (Z {so['OUTER']['Z_CAL']:+.2f})")
RES["sterile"] = STER
# ============================================================== verdict
say("\n=== verdict (frozen rule; C*, X7 CAL errors) ===")
V = {}
for f, hk in CELLS:
    c = f"{f}|{hk}"; b0 = ROWS[("R0 baseline", "C*")][c]; cm = COMB[c]
    zall = cm["ALL"]["MID"]["Z_CAL"]; zt = [cm[t]["MID"]["Z_CAL"] for t in ("T1", "T2", "T3")]
    broke = cm["ALL"]["OUTER"]["Z_CAL"] <= -2 or any(b0[t]["OUTER"]["Z_CAL"] > -2 and cm[t]["OUTER"]["Z_CAL"] <= -2 for t in ("T1", "T2", "T3"))
    red = 1 - (cm["ALL"]["MID"]["A_CAL"] - 1)/(b0["ALL"]["MID"]["A_CAL"] - 1)
    closed = zall < 1 and max(zt) < 2 and not broke
    cls = "CLOSED BY ALLOWED MASS" if closed else ("PARTLY" if (red >= 0.25 or (zall < 1 and max(zt) < 2)) else "NOT CLOSED")
    V[c] = dict(cls=cls, Z_all=zall, Z_terc=zt, outer_broken=broke, residual_removed=red,
                resid_terc={t: cm[t]["MID"]["A_CAL"] - 1 for t in ("T1", "T2", "T3")}, resid_terc_R0={t: b0[t]["MID"]["A_CAL"] - 1 for t in ("T1", "T2", "T3")},
                OUT_terc={t: cm[t]["OUTER"]["Z_CAL"] for t in ("T1", "T2", "T3")}, OUT_all=cm["ALL"]["OUTER"]["Z_CAL"])
    say(f"   {c}: {cls}  all-cluster Z_MID {zall:+.2f}; terciles Z_MID " + " / ".join(f"{z:+.2f}" for z in zt)
        + f"; residual removed {100*red:.0f}%; residual A_MID-1 per tercile " + " / ".join(f"{V[c]['resid_terc'][t]:+.3f} (R0 {V[c]['resid_terc_R0'][t]:+.3f})" for t in ("T1", "T2", "T3"))
        + f"; OUTER Z all {V[c]['OUT_all']:+.2f}, terciles " + " / ".join(f"{V[c]['OUT_terc'][t]:+.2f}" for t in ("T1", "T2", "T3")) + f"; OUTER broken {broke}")
order = ["NOT CLOSED", "PARTLY", "CLOSED BY ALLOWED MASS"]
VERD = order[min(order.index(v["cls"]) for v in V.values())]
RES["verdict_cells"] = V; RES["VERDICT"] = VERD
RES["rows"] = {f"{m}|{l}": v for (l, m), v in ROWS.items()}
say(f"\nVERDICT (frozen rule, weaker of the footings): {VERD}")
npass = sum(ok for _, ok in CHECKS)
RES["runtime_s"] = time.time() - T0; RES["peak_rss_GB"] = rss()
json.dump(RES, open(os.path.join(HERE, f"nu1_cluster_gap_sources_results{TAG}.json"), "w"), indent=1, default=float)
say(f"NU1 COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s, peak RSS {rss():.2f} GB]")
sys.exit(0 if npass == len(CHECKS) else 1)
