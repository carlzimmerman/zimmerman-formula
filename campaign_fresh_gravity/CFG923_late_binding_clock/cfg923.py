"""CFG923 -- does the framework's own formation clock put cold-energy binding late enough for the dwarfs?
Criteria: FROZEN_CRITERIA.md (d60088d9c), committed alone before this script.

CONDITION TEST of CFG920's late-binding escape for route D-i (CFG915/916).  The clock (CFG763 universal, f = 1 - exp(-s/tau),
tau in [tau_min95, 8/ln10]; CFG764 orbital, tau = k t_orb, k in [k_min95, k_max]) runs from the SF onset (13.3 Gyr lookback).
Primary binding epoch s_bind = tau.  F_bind = Weisz+14 cumulative SFH fraction at t_bind (CFG920's t_of_F mapping, forward form).
A dwarf is rescued at tau iff F_bind >= CFG920's central F_need (yield -0.5 primary).  Classes per dwarf: LATE ENOUGH / TOO EARLY /
BRACKET-DEPENDENT; sample: SUPPORTED / CONTRADICTED / UNDERDETERMINED (criteria sections 6-7).
Run (from this directory):
    CFG923_MODE=K       OMP_NUM_THREADS=1 nice -n 10 python3 cfg923.py   -> cfg923_K.out, cfg923_results_K.json (exit 0 = all K pass)
    CFG923_MODE=MUTATE  OMP_NUM_THREADS=1 nice -n 10 python3 cfg923.py   -> cfg923_MUTATE.out, cfg923_results_MUTATE.json (exit 1 = bites)
    CFG923_MODE=MAIN    OMP_NUM_THREADS=1 nice -n 10 python3 cfg923.py   -> cfg923.out, cfg923_results.json (exit 0 = all K pass)
Read-only inputs: CFG763/764/920/824/838/839/873/874/875 result JSONs, cfg920.py text (exec'd read-only), Weisz+14 tables, LVD CSVs,
CFG763's own inputs (K1b).  kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, csv, json, math, hashlib
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402  (read only; exec_slices refuses writes)

MODE = os.environ.get("CFG923_MODE", "MAIN").upper()
assert MODE in ("K", "MUTATE", "MAIN"), MODE
TAG = {"K": "_K", "MUTATE": "_MUTATE", "MAIN": ""}[MODE]
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rd(rel):
    return json.load(open(os.path.join(LANES, rel)))


FOOTS = ("canonical", "alt")
T_ONSET = 13.3                         # Gyr lookback: CFG827/CFG920 SF onset = the clock's origin (criteria 5)
TAU_MAX = 8.0 / math.log(10.0)         # CFG763 F2 / CFG767 C5
YIELDS = ("-0.5", "-0.2")              # primary, V-Y02
PRIMARY_Y = "-0.5"
GYR_S = 3.15576e16
PC_KM = 3.0857e13                      # CFG920's PC (3.0857e16 m) in km
CLS = ("LATE ENOUGH", "TOO EARLY", "BRACKET-DEPENDENT")
SUP, CON, UND = "LATE BINDING SUPPORTED BY THE CLOCK", "CONTRADICTED", "UNDERDETERMINED"

P(__doc__.strip()); P(f"\nMODE = {MODE}")
CFG920_PY = os.path.join(LANES, "CFG920_dwarf_baryon_loss_chemistry", "cfg920.py")
P(f"sha256(cfg920.py) = {hashlib.sha256(open(CFG920_PY, 'rb').read()).hexdigest()}")

# ============================================================================ record inputs
R763 = rd("CFG763_formation_clock/cfg763_results.json")
R764 = rd("CFG764_orbital_clock/cfg764_results.json")
R920 = rd("CFG920_dwarf_baryon_loss_chemistry/cfg920_results.json")
R824 = rd("CFG824_dwarf_age_fossil/cfg824_results.json")["rows"]
ROWS = R920["rows"]; NAMES = list(R920["tested"])
TAU_LO = {f: float(R763["numbers"][f]["lower_1sigma_ages"]["tau_min95_Gyr"]) for f in FOOTS}
K_LO = {f: float(R764["numbers"][f]["k_min95"]) for f in FOOTS}
K_HI = float(R764["numbers"]["SPARC"]["k_max"])
B_U = {f: (TAU_LO[f], TAU_MAX) for f in FOOTS}
B_O = {f: (K_LO[f], K_HI) for f in FOOTS}

# ---------------------------------------------------------------- Weisz+14 reader (copied from CFG920, unchanged)
DS = os.path.join(REPO, "real_research", "data", "dsph"); WZ = os.path.join(DS, "weisz2014_dl")


def fnum(x):
    try: return float(x)
    except: return None  # noqa: E722  (as CFG920)


def read_tsv(fn):
    L = [l.rstrip("\n") for l in open(fn) if not l.startswith("#") and l.strip()]
    hdr = L[0].split("\t"); return [dict(zip(hdr, [x.strip() for x in l.split("\t")])) for l in L[3:] if len(l.split("\t")) == len(hdr)]


def fgrid(r):
    fk = {float(k[1:]): fnum(v) for k, v in r.items() if k.startswith("f") and k[1:].replace(".", "").isdigit() and fnum(v) is not None}
    g = sorted(fk, reverse=True); return np.array(g), np.array([fk[x] for x in g])


NAMEMAP = {"Canes Venetici I": "Canes Venatici I", "Canes Venetici II": "Canes Venatici II", "DDO 210": "Aquarius",
           "Pegasus": "Pegasus dIrr", "Sag DIG": "Sagittarius dIrr", "M32": "M 32"}
T6 = {r["ID"]: r for r in read_tsv(os.path.join(WZ, "table6.tsv"))}
WROW = {}
for r in read_tsv(os.path.join(WZ, "table5.tsv")):
    nm = NAMEMAP.get(r["ID"], r["ID"])
    if nm in WROW: continue
    WROW[nm] = T6.get(r["ID"], r)


def t_of_F(nm, F):
    """CFG920's mapping, copied unchanged: lookback (Gyr) at which the cumulative SFH reaches F."""
    g, f = fgrid(WROW[nm])
    la = np.concatenate([[math.log10(T_ONSET * 1e9)], g]); Fc = np.maximum.accumulate(np.concatenate([[0.0], f]))
    if F <= 0:
        return T_ONSET
    for i in range(1, len(la)):
        if Fc[i] >= F:
            if Fc[i] == Fc[i - 1]:
                return 10 ** la[i] / 1e9
            w = (F - Fc[i - 1]) / (Fc[i] - Fc[i - 1])
            return 10 ** (la[i - 1] + w * (la[i] - la[i - 1])) / 1e9
    return 10 ** la[-1] / 1e9


NODES = {}
for nm in NAMES:
    g, f = fgrid(WROW[nm])
    NODES[nm] = (np.concatenate([[math.log10(T_ONSET * 1e9)], g]), np.maximum.accumulate(np.concatenate([[0.0], f])))


def F_of_t(nm, t, step=False):
    """Forward form of t_of_F: cumulative SFH fraction at lookback t (Gyr).  step=True: V-STEP (first-bin stars at the onset)."""
    la, Fc = NODES[nm]
    if t >= T_ONSET:
        return 0.0
    if t <= 0:
        return float(Fc[-1])
    lt = math.log10(t * 1e9)
    if step and lt > la[1]:
        return float(Fc[1])
    for i in range(1, len(la)):
        if lt >= la[i]:
            w = (la[i - 1] - lt) / (la[i - 1] - la[i])
            return float(Fc[i - 1] + w * (Fc[i] - Fc[i - 1]))
    return float(Fc[-1])


# ---------------------------------------------------------------- LVD + CFG824 (as CFG920 reads them)
LVD = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(DS, fn))):
        LVD[r["name"]] = dict(MV=fnum(r.get("M_V")), rhl=fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical")),
                              src=fn.replace("lvd_dwarf_", "").replace(".csv", ""))
G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16
A0_920 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}


def wolf(M, rhl): return math.sqrt(G * M * Msun / (6.0 * (4.0 / 3.0) * rhl * PC)) / 1e3


def nu(y): y = max(y, 1e-12); return 1.0 / (-math.expm1(-math.sqrt(y)))


def law_M(M, rhl, a0):
    y = G * (M / 2) * Msun / ((4 / 3) * rhl * PC) ** 2 / a0
    return wolf(M, rhl) * math.sqrt(nu(y))


def t_orb(nm):
    """2 pi r_1/2 / V_c, r_1/2 = (4/3) R_e, V_c = sqrt(3) sigma_obs (present-day; criteria 5), Gyr."""
    r12 = (4.0 / 3.0) * LVD[nm]["rhl"] * PC_KM
    return 2 * math.pi * r12 / (math.sqrt(3.0) * R824[nm]["so"]) / GYR_S


TORB = {nm: t_orb(nm) for nm in NAMES}

# ---------------------------------------------------------------- CFG920 chemistry functions, exec'd read-only from its committed text
NS920, _ = C4.exec_slices(CFG920_PY, [(None, "def rd("),
                                      ("def elnx", "# ---------------------------------------------------------------- classes")])
LPOST = NS920["Lpost_min"]


def fneed_920(feh, Ms, Mg, Lreq, logy):
    """CFG920's timing() logic (F_need, reading) with its own Lpost_min."""
    if LPOST(0.0, feh, Ms, Mg, logy) <= Lreq:
        return 0.0, "AT FORMATION"
    if LPOST(1.0, feh, Ms, Mg, logy) > Lreq:
        return None, "NONE"
    F = brentq(lambda x: LPOST(x, feh, Ms, Mg, logy) - Lreq, 0.0, 1.0, xtol=1e-6)
    return float(F), ("EARLY" if F <= 0.5 else "LATE")


# ============================================================================ controls
K = {}


def k1():
    ok, msg = True, []
    for f in FOOTS:
        n = R763["numbers"][f]; lo = n["lower_1sigma_ages"]
        ok &= n["F2_window"] == "OPEN"
        for t, v in lo["f_at"].items():
            d = abs(v - (1 - math.exp(-float(t) / lo["tau_min95_Gyr"])))
            ok &= d <= 1e-12
        msg.append(f"{f}: tau_min95 {lo['tau_min95_Gyr']:.6f} Gyr, F2 {n['F2_window']}")
    ok &= abs(TAU_MAX - 3.47) < 0.005
    msg.append(f"8/ln10 = {TAU_MAX:.6f} (record 3.47)")
    return bool(ok), "; ".join(msg)


def k1b():
    """CFG763's chi^2 code (copied) on its own inputs: tau_min,95 must be reproduced exactly."""
    G_KPC, KPC_M = 4.30091727e-6, 3.0856775814913673e19
    ACC = 1e6 / KPC_M; NU = C4.nu_mono

    def v_newton(M, R): return math.sqrt(G_KPC * M / R)

    def v_law(M, R, a0, Mhost=None, Dp=None):
        gNi = G_KPC * M / R ** 2 * ACC
        if Mhost is None:
            ai = gNi * float(NU(gNi / a0))
        else:
            gNe = G_KPC * Mhost / Dp ** 2 * ACC
            ai = gNi * float(NU((gNi + gNe) / a0)) + gNe * (float(NU((gNi + gNe) / a0)) - float(NU(gNe / a0)))
        return math.sqrt(ai / ACC * R)

    def pred_err(fn, M, eM, R, eR):
        v0 = fn(M, R)
        dm = (fn(M * 1.01, R) - v0) / (0.01 * M) * eM
        dr = (fn(M, R * 1.01) - v0) / (0.01 * R) * eR
        return v0, math.hypot(dm, dr)

    OBJ = []
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv"))):
        g = lambda k: float(r[k])  # noqa: E731
        OBJ.append(dict(V=g("V_circ_kms"), eV=g("e_V_circ_kms"), M=g("M_bar_1e8") * 1e8, eM=g("e_M_bar_1e8") * 1e8,
                        R=g("R_out_kpc"), eR=g("e_R_out_kpc"), Mhost=0.6 * g("host_LK_1e10Lsun") * 1e10, Dp=g("D_p_kpc"),
                        t=g("tmerg_over_torb") * g("t_orb_Gyr"), et=g("tmerg_over_torb") * g("e_t_orb_Gyr")))
    for r in csv.DictReader(open(os.path.join(LANES, "CFG441_old_tdgs_tidal_origin", "data", "tierB_arp72c.csv"))):
        g = lambda k: float(r[k])  # noqa: E731
        OBJ.append(dict(V=g("V_circ_kms"), eV=0.5 * (g("e_V_circ_up") + g("e_V_circ_lo")), M=g("M_bar_1e8") * 1e8,
                        eM=g("e_M_bar_1e8") * 1e8, R=g("R_out_kpc"), eR=g("e_R_out_kpc"), Mhost=None, Dp=None,
                        t=g("age_Myr") / 1e3, et=g("e_age_Myr") / 1e3))
    TAUS = 10 ** np.round(np.arange(-2, 2.0001, 0.01), 2)
    c441 = rd("CFG441_old_tdgs_tidal_origin/cfg441_old_tdgs_results.json")["numbers"]["tierB"]["out"]
    ok, msg = True, []
    for fo in C4.FOOTS:
        a0 = C4.A0[fo]; pre = []
        for o in OBJ:
            vn, en = pred_err(lambda M, R: v_newton(M, R), o["M"], o["eM"], o["R"], o["eR"])
            if o["Mhost"] is None:
                vl, el = pred_err(lambda M, R: v_law(M, R, a0), o["M"], o["eM"], o["R"], o["eR"])
            else:
                vl, el = pred_err(lambda M, R, o=o: v_law(M, R, a0, o["Mhost"], o["Dp"]), o["M"], o["eM"], o["R"], o["eR"])
            pre.append((vn, en, vl, el))

        def chi2(tau, ages):
            tot = 0.0
            for o, (vn, en, vl, el), t in zip(OBJ, pre, ages):
                fr = 1.0 if tau == 0 else (0.0 if math.isinf(tau) else 1 - math.exp(-t / tau))
                vm = math.sqrt(vn ** 2 + fr * (vl ** 2 - vn ** 2)); em = en + fr * (el - en)
                tot += (o["V"] - vm) ** 2 / (o["eV"] ** 2 + em ** 2)
            return tot
        lo_age = [max(o["t"] - o["et"], 0.05) for o in OBJ]
        cl, cn = chi2(0.0, lo_age), chi2(math.inf, lo_age)
        ch = np.array([chi2(t, lo_age) for t in TAUS]); cmin = min(ch.min(), cn)
        tmin = float(TAUS[np.where(ch <= cmin + 3.84)[0][0]])
        stored = R763["numbers"][fo]["lower_1sigma_ages"]["tau_min95_Gyr"]
        ok &= (tmin == stored) and abs(cl - c441[fo]["chi2_law"]) <= 0.01 and abs(cn - c441[fo]["chi2_N"]) <= 0.01
        msg.append(f"{fo}: recomputed tau_min95 {tmin:.6f} (stored {stored:.6f}); chi2 tau->0 {cl:.3f} (CFG441 {c441[fo]['chi2_law']:.3f}),"
                   f" tau->inf {cn:.3f} (CFG441 {c441[fo]['chi2_N']:.3f})")
    return bool(ok), "; ".join(msg)


def k2():
    ok, n_a, n_b, dt_max, dF_max, msg = True, 0, 0, 0.0, 0.0, []
    counts = {f: {y: {r_: 0 for r_ in ("AT FORMATION", "EARLY", "LATE", "NONE")} for y in YIELDS} for f in FOOTS}
    for nm in NAMES:
        x = ROWS[nm]
        for f in FOOTS:
            for y in YIELDS:
                tm = x["timing"][f][y]
                counts[f][y][tm["reading"]] += 1
                if tm["F_need"] is not None:
                    d = abs(t_of_F(nm, tm["F_need"]) - tm["t_need"]); dt_max = max(dt_max, d); n_a += 1
                    ok &= d <= 1e-9
                Fn, rdg = fneed_920(x["feh"], x["Ms"], x["Mg"], x["L_req"][f], float(y))
                n_b += 1; ok &= rdg == tm["reading"]
                if Fn is not None and tm["F_need"] is not None:
                    dF_max = max(dF_max, abs(Fn - tm["F_need"])); ok &= abs(Fn - tm["F_need"]) <= 1e-5
                elif (Fn is None) != (tm["F_need"] is None):
                    ok = False
    ok &= counts == R920["timing_summary"]
    msg.append(f"(a) t_need from F_need: {n_a} entries, max |dt| {dt_max:.2e} Gyr; (b) F_need recomputed with CFG920's functions: "
               f"{n_b} entries, readings identical, max |dF| {dF_max:.2e}; (c) reading counts = timing_summary: {counts == R920['timing_summary']}")
    return bool(ok), "; ".join(msg)


def k3():
    ok, dmax = True, 0.0
    for nm in NAMES:
        x = ROWS[nm]; Ms = x["ups"] * 10 ** (0.4 * (4.83 - LVD[nm]["MV"]))
        for f in FOOTS:
            E = math.log(R824[nm]["so"] / law_M(Ms, LVD[nm]["rhl"], A0_920[f]))
            dmax = max(dmax, abs(E - x["E"][f])); ok &= abs(E - x["E"][f]) <= 1e-9
    kmx = 8.0 / (math.log(10.0) * R764["numbers"]["SPARC"]["torb_max"])
    ok &= abs(kmx - K_HI) <= 1e-9
    return bool(ok), f"E from CFG824 sigma_obs + LVD M_V, R_e + CFG920 Upsilon: max |dE| {dmax:.2e} (40 values); k_max 8/(ln10 torb_max) {kmx:.9f} = stored {K_HI:.9f}"


def k4():
    ok, nchk, dmax, nmono = True, 0, 0.0, 0
    for nm in NAMES:
        for F in np.arange(0.05, 0.951, 0.05):
            d = abs(F_of_t(nm, t_of_F(nm, float(F))) - F); dmax = max(dmax, d); nchk += 1; ok &= d <= 1e-9
    for f in FOOTS:
        for nm in NAMES:
            for lo, hi in (B_U[f], (B_O[f][0] * TORB[nm], B_O[f][1] * TORB[nm])):
                taus = np.linspace(lo, hi, 200)
                Fb = [Fbind(nm, t, "PRIMARY") for t in taus]
                nmono += 1; ok &= all(b >= a - 1e-15 for a, b in zip(Fb, Fb[1:]))
    return bool(ok), f"F(t_of_F(F)) = F on {nchk} points, max |dF| {dmax:.2e}; F_bind non-decreasing in tau on {nmono} brackets"


# ============================================================================ clock -> binding epoch -> class
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
RULE_FAC = {"PRIMARY": 1.0, "V-MED": math.log(2.0), "V-90": math.log(10.0), "V-STEP": 1.0}


def Fbind(nm, tau, rule):
    """F_bind for a clock time constant tau (Gyr) under a declared binding rule."""
    if rule == "V-DIST":
        umax = min(T_ONSET / tau, 60.0); u = np.linspace(0.0, umax, 6001); w = np.exp(-u)
        Fu = np.array([F_of_t(nm, T_ONSET - tau * uu) for uu in u])
        return float(TRAPZ(Fu * w, u) / TRAPZ(w, u))
    s = RULE_FAC[rule] * tau
    if s >= T_ONSET:
        return 1.0                                           # NOT BOUND BY TODAY (criteria 5; favourable)
    return F_of_t(nm, T_ONSET - s, step=(rule == "V-STEP"))


def tau_ends(clock, f, nm, scale=1.0):
    if clock == "C-U":
        return B_U[f][0] * scale, B_U[f][1] * scale
    return B_O[f][0] * scale * TORB[nm], B_O[f][1] * scale * TORB[nm]


def grade(F_lo_bind, F_hi_bind, Fn_fast, Fn_slow):
    """Fn_fast: F_need tested at the fast end (LATE ENOUGH needs it rescued); Fn_slow: at the slow end (TOO EARLY if not)."""
    r_lo = Fn_fast is not None and F_lo_bind >= Fn_fast
    r_hi = Fn_slow is not None and F_hi_bind >= Fn_slow
    if r_lo and r_hi:
        return "LATE ENOUGH"
    if not r_hi:
        return "TOO EARLY"
    return "BRACKET-DEPENDENT"


def sample_class(cl, half=False):
    N = len(cl)
    if N == 0:
        return "NO TEST SET"
    nTE = sum(c == "TOO EARLY" for c in cl); nLE = sum(c == "LATE ENOUGH" for c in cl)
    if nTE == 0 and nLE >= N / 2:
        return SUP
    if (nTE >= N / 2) if half else (nTE > N / 2):
        return CON
    return UND


def test_set(f, y):
    return [nm for nm in NAMES if ROWS[nm]["timing"][f][y]["reading"] in ("EARLY", "LATE")]


def run_grid(clock, f, y, rule="PRIMARY", scale=1.0, fneed=None):
    """Per-dwarf classes for one clock/footing/yield/rule/scale.  fneed: optional {nm: (F_fast, F_slow)} (V-1sigma)."""
    out = {}
    for nm in test_set(f, y):
        tm = ROWS[nm]["timing"][f][y]; lo, hi = tau_ends(clock, f, nm, scale)
        Fl, Fh = Fbind(nm, lo, rule), Fbind(nm, hi, rule)
        Ff, Fs = fneed[nm] if fneed else (tm["F_need"], tm["F_need"])
        row = dict(tau_fast=lo, tau_slow=hi, F_bind_fast=Fl, F_bind_slow=Fh, F_need=tm["F_need"], t_need=tm["t_need"],
                   cls=grade(Fl, Fh, Ff, Fs))
        if rule in ("PRIMARY", "V-MED", "V-90", "V-STEP"):
            fac = RULE_FAC[rule]
            row.update(t_bind_fast=max(T_ONSET - fac * lo, 0.0), t_bind_slow=max(T_ONSET - fac * hi, 0.0),
                       unbound_today=bool(fac * hi >= T_ONSET))
        if fneed:
            row.update(F_need_fav=Ff, F_need_unf=Fs)
        out[nm] = row
    cl = [r["cls"] for r in out.values()]
    return dict(rows=out, n={c: sum(x == c for x in cl) for c in CLS}, N=len(cl), sample=sample_class(cl),
                sample_half=sample_class(cl, half=True))


# ============================================================================ run
P("\nINPUTS")
for f in FOOTS:
    P(f"  {f:9s}: C-U tau in [{B_U[f][0]:.4f}, {B_U[f][1]:.4f}] Gyr -> binding lookback [{T_ONSET - B_U[f][1]:.3f}, {T_ONSET - B_U[f][0]:.3f}] Gyr;"
      f"  C-O k in [{B_O[f][0]:.4f}, {B_O[f][1]:.4f}]")
P(f"  F_need / t_need: CFG920's stored central values (criteria a229bb78c); yield {PRIMARY_Y} primary")

P("\nCONTROLS")
for nm_, fn_ in (("K1", k1), ("K1b", k1b), ("K2", k2), ("K3", k3), ("K4", k4)):
    ok_, msg_ = fn_(); K[nm_] = dict(ok=ok_, msg=msg_)
    P(f"  {nm_}: {'PASS' if ok_ else 'FAIL'} -- {msg_}")
KALL = all(v["ok"] for v in K.values())
P(f"  all K: {'PASS' if KALL else 'FAIL'}")
RES = dict(lane="CFG923", criteria="d60088d9c", mode=MODE, K=K,
           settings=dict(T_ONSET=T_ONSET, TAU_MAX=TAU_MAX, B_U=B_U, B_O=B_O, primary_yield=PRIMARY_Y, rule_primary="s_bind = tau",
                         sha256_cfg920_py=hashlib.sha256(open(CFG920_PY, "rb").read()).hexdigest()))

if MODE == "K":
    json.dump(C4.jclean(RES), open(os.path.join(HERE, f"cfg923_results{TAG}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg923{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if KALL else 2)

CLOCKS = ("C-U", "C-O")
if MODE == "MUTATE":
    P("\nMUTATE: every bracket end x0.1 and x10 (tau for C-U, k for C-O); compared with the unscaled primary grading")
    MU = {}
    for f in FOOTS:
        MU[f] = {}
        for c in CLOCKS:
            MU[f][c] = {str(s): run_grid(c, f, PRIMARY_Y, scale=s) for s in (1.0, 0.1, 10.0)}
            base = MU[f][c]["1.0"]
            for s in ("0.1", "10.0"):
                g_ = MU[f][c][s]
                nch = sum(g_["rows"][nm]["cls"] != base["rows"][nm]["cls"] for nm in base["rows"])
                g_["n_changed"] = nch; g_["sample_changed"] = g_["sample"] != base["sample"]
                P(f"  {f:9s} {c} x{s:4s}: {g_['n']}  sample {g_['sample']}  (unscaled {base['sample']}; {nch} per-dwarf classes changed)")
                for nm in base["rows"]:
                    P(f"      {nm:18s} {base['rows'][nm]['cls']:18s} -> {g_['rows'][nm]['cls']:18s}  F_bind {g_['rows'][nm]['F_bind_fast']:.3f}-"
                      f"{g_['rows'][nm]['F_bind_slow']:.3f} vs F_need {g_['rows'][nm]['F_need']:.3f}")
    bite = all(MU[f]["C-U"]["0.1"]["n_changed"] >= 1 and MU[f]["C-U"]["10.0"]["n_changed"] >= 1
               and (MU[f]["C-U"]["0.1"]["sample_changed"] or MU[f]["C-U"]["10.0"]["sample_changed"]) for f in FOOTS)
    P(f"\nMUTATE bites (C-U, both footings: x0.1 and x10 each change >= 1 class; >= 1 changes the sample class): {bite}")
    RES.update(mutate=MU, bites=bool(bite))
    json.dump(C4.jclean(RES), open(os.path.join(HERE, f"cfg923_results{TAG}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg923{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1 if bite else 0)

# ---------------------------------------------------------------- MAIN
MAIN = {}
P("\nPER-DWARF TABLE (yield -0.5; t in Gyr lookback; binding lookback at the fast / slow bracket end)")
for f in FOOTS:
    MAIN[f] = {}
    for c in CLOCKS:
        MAIN[f][c] = run_grid(c, f, PRIMARY_Y)
    P(f"\n  [{f}]  S = {test_set(f, PRIMARY_Y)}")
    P(f"  {'dwarf':18s} {'tau50':>6s} {'tau90':>6s} {'F_need':>7s} {'t_need':>7s} | C-U t_bind   F_bind      class             "
      f"| t_orb  C-O t_bind     F_bind      class")
    for nm in test_set(f, PRIMARY_Y):
        u, o = MAIN[f]["C-U"]["rows"][nm], MAIN[f]["C-O"]["rows"][nm]; x = ROWS[nm]
        P(f"  {nm:18s} {x['tau50']:6.2f} {x['tau90']:6.2f} {u['F_need']:7.3f} {u['t_need']:7.2f} | {u['t_bind_fast']:5.2f}-{u['t_bind_slow']:5.2f}"
          f" {u['F_bind_fast']:.3f}-{u['F_bind_slow']:.3f} {u['cls']:17s} | {TORB[nm]:5.3f} {o['t_bind_fast']:6.3f}-{o['t_bind_slow']:6.3f}"
          f" {o['F_bind_fast']:.3f}-{o['F_bind_slow']:.3f} {o['cls']}")
    for c in CLOCKS:
        g_ = MAIN[f][c]
        P(f"  {c}: N {g_['N']}  {g_['n']}  -> SAMPLE: {g_['sample']}   [V-HALF: {g_['sample_half']}]")

# f_pre: fraction of the cold energy already formed before t_need (both ends)
FPRE = {}
for f in FOOTS:
    FPRE[f] = {}
    for nm in test_set(f, PRIMARY_Y):
        tn = ROWS[nm]["timing"][f][PRIMARY_Y]["t_need"]; FPRE[f][nm] = {}
        for c in CLOCKS:
            lo, hi = tau_ends(c, f, nm)
            FPRE[f][nm][c] = [1 - math.exp(-(T_ONSET - tn) / lo), 1 - math.exp(-(T_ONSET - tn) / hi)]
P("\nf_pre = cold-energy fraction the clock has formed before t_need (fastest / slowest clock)")
for f in FOOTS:
    P(f"  [{f}] " + "; ".join(f"{nm}: C-U {v['C-U'][0]:.3f}/{v['C-U'][1]:.3f}, C-O {v['C-O'][0]:.3f}/{v['C-O'][1]:.3f}" for nm, v in FPRE[f].items()))

# outside S
OUTS = {f: {nm: ROWS[nm]["timing"][f][PRIMARY_Y]["reading"] for nm in NAMES if nm not in test_set(f, PRIMARY_Y)} for f in FOOTS}
for f in FOOTS:
    nt = [nm for nm, r in OUTS[f].items() if r == "AT FORMATION"]; nr = [nm for nm, r in OUTS[f].items() if r == "NONE"]
    P(f"  [{f}] NO TIMING REQUIREMENT (AT FORMATION) {len(nt)}: {nt}")
    P(f"  [{f}] NO TIMING RESCUE (NONE) {len(nr)}: {nr}")

# ---------------------------------------------------------------- headline, record level, overall
HEAD = {f: MAIN[f]["C-U"]["sample"] for f in FOOTS}
REC = {f: (MAIN[f]["C-U"]["sample"] if MAIN[f]["C-U"]["sample"] == MAIN[f]["C-O"]["sample"] else UND) for f in FOOTS}
OVERALL = REC["canonical"] if REC["canonical"] == REC["alt"] else UND
P("\nCLASSES")
for f in FOOTS:
    P(f"  {f:9s}: C-U (headline) {MAIN[f]['C-U']['sample']};  C-O {MAIN[f]['C-O']['sample']};  record level {REC[f]}")
P(f"  OVERALL: {OVERALL}")

# ---------------------------------------------------------------- variants
P("\nVARIANTS (reported; no class weight)")
VAR = {}
for f in FOOTS:
    VAR[f] = {}
    for c in CLOCKS:
        VAR[f][c] = {r_: run_grid(c, f, PRIMARY_Y, rule=r_) for r_ in ("V-MED", "V-90", "V-STEP", "V-DIST")}
        flips = [r_ for r_, g_ in VAR[f][c].items() if g_["sample"] != MAIN[f][c]["sample"]]
        VAR[f][c]["label"] = "RULE-ROBUST" if not flips else "RULE-FRAGILE (" + ", ".join(flips) + ")"
        for r_ in ("V-MED", "V-90", "V-STEP", "V-DIST"):
            g_ = VAR[f][c][r_]
            P(f"  {f:9s} {c} {r_:7s}: {g_['n']}  sample {g_['sample']}  | " + ", ".join(f"{nm} {v['cls'][:2]}" for nm, v in g_['rows'].items()))
        P(f"  {f:9s} {c} -> {VAR[f][c]['label']}")

# V-1sigma: F_need at the favourable / unfavourable ends with CFG920's own functions
P("\nV-1sigma (F_need from CFG920's functions at L_req = e^{4(E +- sE)}, [Fe/H] +- s; yield -0.5)")
V1 = {}
for f in FOOTS:
    fn = {}
    for nm in test_set(f, PRIMARY_Y):
        x = ROWS[nm]
        Ffav, rfav = fneed_920(x["feh"] + x["s"], x["Ms"], x["Mg"], math.exp(4 * (x["E"][f] + x["sE"])), float(PRIMARY_Y))
        Funf, runf = fneed_920(x["feh"] - x["s"], x["Ms"], x["Mg"], math.exp(4 * (x["E"][f] - x["sE"])), float(PRIMARY_Y))
        fn[nm] = (Funf, Ffav)                          # fast end tests the unfavourable F_need, slow end the favourable one
        P(f"  [{f}] {nm:18s} F_need fav {('%.3f' % Ffav) if Ffav is not None else 'NONE'} ({rfav}), central {x['timing'][f][PRIMARY_Y]['F_need']:.3f},"
          f" unf {('%.3f' % Funf) if Funf is not None else 'NONE'} ({runf})")
    V1[f] = {c: run_grid(c, f, PRIMARY_Y, fneed=fn) for c in CLOCKS}
    for c in CLOCKS:
        g_ = V1[f][c]
        P(f"  {f:9s} {c} V-1sigma: {g_['n']}  sample {g_['sample']}  | " + ", ".join(f"{nm} {v['cls'][:2]}" for nm, v in g_['rows'].items()))

# V-Y02
P("\nV-Y02 (yield -0.2; its own test set)")
VY = {}
for f in FOOTS:
    VY[f] = {c: run_grid(c, f, "-0.2") for c in CLOCKS}
    for c in CLOCKS:
        g_ = VY[f][c]
        P(f"  {f:9s} {c}: N {g_['N']} {g_['n']}  sample {g_['sample']} [V-HALF {g_['sample_half']}] | "
          + ", ".join(f"{nm} {v['cls'][:2]}" for nm, v in g_['rows'].items()))

# ---------------------------------------------------------------- ungraded reports R1 (tides) and R2 (field dwarfs)
R838 = rd("CFG838_satellite_tides/cfg838_results.json"); R839 = rd("CFG839_pericentre_tides/cfg839_results.json")
P("\nR1 (ungraded): tides vs late binding, for the S dwarfs (union of footings)")
R1 = {}
SALL = [nm for nm in NAMES if any(nm in test_set(f, PRIMARY_Y) for f in FOOTS)]
for nm in SALL:
    host = R838["rows"].get(nm, {}).get("host") or ("field" if nm in R838["field"] else LVD[nm]["src"])
    logT = R838["rows"].get(nm, {}).get("logT"); logTp = R839["rows"].get(nm, {}).get("logTp")
    u = MAIN["canonical"]["C-U"]["rows"].get(nm)
    pre90 = None if u is None else [bool(u["t_bind_fast"] > ROWS[nm]["tau90"]), bool(u["t_bind_slow"] > ROWS[nm]["tau90"])]
    R1[nm] = dict(host=host, logT_838=logT, logTp_839=logTp, tau90=ROWS[nm]["tau90"], CU_binding_before_tau90_can=pre90)
    P(f"  {nm:18s} host {host:9s} logT(838) {('%.2f' % logT) if logT is not None else '  - '}  logT_p(839) "
      f"{('%.2f' % logTp) if logTp is not None else '  - '}  tau90 {ROWS[nm]['tau90']:.2f}  C-U binds before tau90 (fast/slow, can): {pre90}")

P("\nR2 (ungraded): field dwarfs")
R873 = rd("CFG873_field_dwarf_environment/cfg873_results.json"); R874 = rd("CFG874_isolated_dwarfs_pooled/cfg874_results.json")
R875 = rd("CFG875_host_distance_trend/cfg875_results.json")
R2 = {"CFG873": {f: {k: R873[f]["primary"][k] for k in ("E", "se_E", "D", "se_D", "cls")} for f in FOOTS},
      "CFG874": {f: {k: R874[f]["primary"][k] for k in ("c", "se_c", "E", "se_E", "cls")} for f in FOOTS},
      "CFG875": {f: {k: R875[f]["primary"][k] for k in ("k", "se_k", "cls")} for f in FOOTS}, "dwarfs": {}}
for nm in ("Cetus", "Tucana", "Aquarius", "Phoenix", "Leo T"):
    d_ = {}
    for f in FOOTS:
        rdg = ROWS[nm]["timing"][f][PRIMARY_Y]["reading"]
        d_[f] = dict(reading=rdg, **{c: (MAIN[f][c]["rows"][nm]["cls"] if nm in MAIN[f][c]["rows"] else "NO TIMING REQUIREMENT"
                                         if rdg == "AT FORMATION" else "NO TIMING RESCUE") for c in CLOCKS})
    R2["dwarfs"][nm] = d_
    P(f"  {nm:9s} gas {ROWS[nm]['gas']!s:5s} tau90 {ROWS[nm]['tau90']:.2f} | " + " | ".join(
        f"{f}: {d_[f]['reading']}, C-U {d_[f]['C-U']}, C-O {d_[f]['C-O']}" for f in FOOTS))
for f in FOOTS:
    P(f"  {f}: CFG873 E_F {R2['CFG873'][f]['E']:+.3f}+-{R2['CFG873'][f]['se_E']:.3f}, D {R2['CFG873'][f]['D']:+.3f}+-{R2['CFG873'][f]['se_D']:.3f}"
      f" ({R2['CFG873'][f]['cls']}); CFG874 c {R2['CFG874'][f]['c']:+.3f}+-{R2['CFG874'][f]['se_c']:.3f}, E {R2['CFG874'][f]['E']:+.3f}"
      f" ({R2['CFG874'][f]['cls']}); CFG875 k {R2['CFG875'][f]['k']:+.3f}+-{R2['CFG875'][f]['se_k']:.3f} ({R2['CFG875'][f]['cls']})")

RES.update(torb_Gyr=TORB, main=MAIN, f_pre=FPRE, outside_S=OUTS, headline_CU=HEAD, record_level=REC, overall=OVERALL,
           variants=VAR, v1sigma=V1, v_y02=VY, R1=R1, R2=R2)
P(f"\nVERDICT: C-U (headline) canonical {HEAD['canonical']}, alt {HEAD['alt']}; C-O canonical {MAIN['canonical']['C-O']['sample']},"
  f" alt {MAIN['alt']['C-O']['sample']}; OVERALL {OVERALL}.  K {'PASS' if KALL else 'FAIL'}.")
P("kappa = 1/2 FITTED; footings never pooled; not theory closed.")
json.dump(C4.jclean(RES), open(os.path.join(HERE, f"cfg923_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg923{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if KALL else 2)
