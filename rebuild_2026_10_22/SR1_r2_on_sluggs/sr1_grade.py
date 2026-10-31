#!/usr/bin/env python3
"""SR1_r2_on_sluggs (criteria 1d0fea100e, committed alone): R2's stellar-mass rungs against the record's dynamical masses on SLUGGS.

Machinery, all read-only: CFG55's head (h50 -> CFG38 -> CFG55) for the 16 galaxies, M_JAM, r_1/2, GC bins and the Jeans solver; SI1's text for
FC1's rule (`halo_of`); KN1's shape rule on ZN1's z = 0 shapes; CFG528b's head for the four centrals' measured tracers (reported row).
kappa = 1/2 FITTED; footings never pooled; cold dark energy is a gravitating field component, never a particle.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 15 python3 -B sr1_grade.py [--mutate]
Outputs sr1.out, sr1_results.json (twin: sr1_MUTATE.out, sr1_results_MUTATE.json). Exit 0 only if every K passes; the twin exits 1 if its tooth bites.
"""
import builtins, contextlib, io, json, math, os, re, resource, sys, time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
for _v in ("MUTATE", "CFG528_MUTATE", "CFG528_POSTFREEZE", "CFG528B_MUTATE", "CFG331_MUTATE"):
    os.environ.pop(_v, None)
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq, minimize_scalar

T0 = time.time()
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REB = os.path.dirname(HERE)
REPO = os.path.dirname(REB)
CFG = os.path.join(REPO, "campaign_fresh_gravity")
EXT = os.path.join(os.path.dirname(REPO), "_external_data")
OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


def ro_open(path, mode="r", *a, **k):
    """Machinery runs through this: anything but a read is refused, so no other lane's file can change."""
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"write refused: {path}")
    return builtins.open(path, mode, *a, **k)


RUNGS = {"R0": 0.0, "I": 0.172, "L": 0.295}          # criteria sec. 2; T and Isig are reported
RUNG_T = 0.295 - (0.304 - 0.10)                      # CFG505 M1b early median; Bell+03 about +0.10 above Chabrier (recalled, PROVISIONAL)
SIG_S_R12 = 0.10
SIG_S_GC = math.sqrt(0.10 ** 2 + 0.052 ** 2)
NBOOT, SEED = 20000, 20261031
FOOTS = ("canonical", "alt")
CENTRALS = ("NGC4486", "NGC4365", "NGC4374", "NGC5846")
checks = {}
P(f"SR1_r2_on_sluggs (criteria 1d0fea100e){'  [MUTATE: M_JAM x 0.5, sigma_obs x 0.8, halos x 0.5]' if MUT else ''}")
P("kappa = 1/2 FITTED; footings never pooled; cold dark energy, never a particle. d lg M = lg(M_dyn / M_model): negative = model above M_dyn.")

# ------------------------------------------------------------------ CFG55's head (machinery, sample, estimators), read-only
sys.path.insert(0, CFG)
P55 = os.path.join(CFG, "CFG55_sluggs_dynamical_masses.py")
SRC55 = builtins.open(P55).read()
CUT55 = "RES = {}\nfor f in FOOTS:"
assert SRC55.count(CUT55) == 1
NS = {"__file__": P55, "__name__": "cfg55_ro", "open": ro_open}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(SRC55[:SRC55.index(CUT55)], P55, "exec"), NS)
G16, RES50 = NS["G16"], NS["RES50"]
sigma_r2, sigma_los, GAMMA, G_, KPC, MSUN, nu_h, A0SI = (NS[k] for k in ("sigma_r2", "sigma_los", "GAMMA", "G_", "KPC", "MSUN", "nu_h", "A0SI"))
JF, SF, HF = (0.5, 0.8, 0.5) if MUT else (1.0, 1.0, 1.0)
if MUT:                                               # in place, so K1 must fail on the same objects it reads
    for g in G16:
        g["Mjam"] *= JF
        g["r"]["Sb"] = g["r"]["Sb"] * SF
J55 = json.load(builtins.open(os.path.join(CFG, "CFG55_sluggs_dynamical_masses_results.json")))["numbers"]["RES"]
P(f"[{time.time() - T0:.0f} s] CFG55 head loaded: {len(G16)} galaxies, {len(RES50)} in h50's list")

# ------------------------------------------------------------------ SI1's text: FC1's rule, smooth core, EM1's relation, r_ta
SI1F = os.path.join(REB, "SI1_spec_isolated_route_e", "si1_grade.py")
T1 = builtins.open(SI1F).read()
P2T = builtins.open(os.path.join(REB, "P2_spec_isolated_lensing", "p2_spec_isolated_lensing.py")).read()
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
NSH = {"os": os, "json": json, "math": math, "np": np, "brentq": brentq, "minimize_scalar": minimize_scalar, "REB": REB, "A0": A0, "FOOTS": FOOTS,
       "Gpc": 4.30091e-3, "ZT": 0.0, "open": ro_open}
exec(compile(T1[T1.index("EM1J = json.load"):T1.index('_w = MEAS["WW"]')], "si1_slice_a", "exec"), NSH)
exec(compile(T1[T1.index("def halo_of"):T1.index("HF = 0.5 if MUTS else 1.0")], "si1_slice_b", "exec"), NSH)
halo_of, SAT, FC, RHOC, BA, BB = (NSH[k] for k in ("halo_of", "SAT", "FC", "RHOC", "BA", "BB"))
ETAV0 = list(NSH["ETAV"])
ETA_A4 = json.load(builtins.open(os.path.join(REB, "CE1_converged_eta_grade", "ce1_a4_results.json")))["eta"]
ETAV_A4 = [ETA_A4[e]["med"] for e in ("12", "13", "14")]

# ------------------------------------------------------------------ KN1's shape rule on ZN1's z = 0 shapes (native line)
_ZN = json.load(builtins.open(os.path.join(REB, "ZN1_zooms_to_z0", "zn1_shapes.json")))
XL = np.log(np.array(_ZN["x"]))
TAGS = sorted(((_ZN[m]["0.00"]["lgM"], np.array(_ZN[m]["0.00"]["lnm"]), _ZN[m]["0.00"]["x_edge"]) for m in ("1e12", "1e13", "1e14")), key=lambda t: t[0])
KN = {"below": 0, "n": 0}


def kn1_shape(lg):
    KN["n"] += 1
    if lg <= TAGS[0][0]:
        KN["below"] += 1
        return TAGS[0][1], TAGS[0][2]
    if lg >= TAGS[-1][0]:
        return TAGS[-1][1], TAGS[-1][2]
    k = next(i for i in range(len(TAGS) - 1) if TAGS[i][0] <= lg <= TAGS[i + 1][0])
    w = (lg - TAGS[k][0]) / (TAGS[k + 1][0] - TAGS[k][0])
    return (1 - w) * TAGS[k][1] + w * TAGS[k + 1][1], min(TAGS[k][2], TAGS[k + 1][2])


def native_M(r_pc, Ma):
    """KN1 (EM1's masses, z = 0): M_c(r) = f_c M_t m(r/R_t) for r <= x_edge R_t, constant beyond; inner M ~ r^2 below the first node."""
    M200 = 10 ** (BA + BB * (math.log10(Ma) - 10))
    Mt = M200 / FC
    R = (3 * Mt / (4 * math.pi * 200 * RHOC)) ** (1 / 3)
    ln_, xe = kn1_shape(math.log10(Mt))
    x = np.minimum(np.asarray(r_pc, float) / R, xe)
    lx = np.log(np.maximum(x, 1e-300))
    return FC * Mt * np.exp(np.where(lx >= XL[0], np.interp(lx, XL, ln_), ln_[0] + 2 * (lx - XL[0])))


# ------------------------------------------------------------------ fields and estimators
def nu1(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def rec(g):
    r = g["r"]
    return dict(name=g["name"], Ms0=r["Mstar"], Re=r["Re"], ah=r["Re"] / 1.8153, Rb=r["Rb"], Sb=r["Sb"], Eb=r["Eb"], out=r["out"], Mjam=g["Mjam"], r12=g["r12"],
                Msalp=g["Msalp"], lsig=g["lsig"], x=r["Rb"] / r["Re"])


GAL = [rec(g) for g in G16]
for S in GAL:
    S["w15"] = (S["x"] >= 1.0) & (S["x"] <= 5.0)
    S["w13"] = (S["x"] >= 1.0) & (S["x"] <= 3.0)
    S["fH"] = S["r12"] ** 2 / (S["r12"] + S["ah"]) ** 2
    S["gam111"] = float(np.clip(-0.63 * math.log10(S["Ms0"]) + 9.81, 2.0, 4.0))


def g_field(S, Ms, model, foot=None, arg=None):
    """g(r) in SI on h50's grid; model in stars / law / routeE / native. arg: M200's argument if not the rung's stars."""
    a = S["ah"]
    Ma = Ms if arg is None else arg
    if model == "stars":
        return lambda r: G_ * (Ms * MSUN * r ** 2 / (r + a) ** 2) / (r * KPC) ** 2
    if model == "law":
        def gl(r):
            gN = G_ * (Ms * MSUN * r ** 2 / (r + a) ** 2) / (r * KPC) ** 2
            return gN * nu1(gN / A0[foot])
        return gl
    if model == "routeE":
        def gr(r):
            Mh, _ = halo_of(foot, r * 1e3, Ma, 0.0, Ma, 0.0, "E")
            return G_ * (Ms * r ** 2 / (r + a) ** 2 + HF * Mh) * MSUN / (r * KPC) ** 2
        return gr
    if model == "native":
        return lambda r: G_ * (Ms * r ** 2 / (r + a) ** 2 + HF * native_M(r * 1e3, Ma)) * MSUN / (r * KPC) ** 2
    raise ValueError(model)


def dl_gc(S, gf, mask, gam=None, beta=0.0):
    gm = GAMMA if gam is None else gam
    s = sigma_los(S["Rb"], sigma_r2(gf, gm, beta), gm, beta)
    return 2.0 * float(np.mean(np.log10(S["Sb"][mask] / s[mask])))


def M12(S, Ms, model, foot=None, f=None, arg=None):
    r = S["r12"]
    Mst = (S["fH"] if f is None else f) * Ms
    Ma = Ms if arg is None else arg
    if model == "stars":
        return Mst
    if model == "law":
        return Mst * float(nu1(G_ * Mst * MSUN / (r * KPC) ** 2 / A0[foot]))
    if model == "routeE":
        return Mst + HF * float(halo_of(foot, np.array([r * 1e3]), Ma, 0.0, Ma, 0.0, "E")[0][0])
    if model == "native":
        return Mst + HF * float(native_M(np.array([r * 1e3]), Ma)[0])
    raise ValueError(model)


def dl_r12(S, Ms, model, foot=None, f=None, arg=None):
    return math.log10(0.5 * S["Mjam"]) - math.log10(M12(S, Ms, model, foot, f, arg))


# ------------------------------------------------------------------ sample statistics and classes (criteria sec. 3-6)
_IDX = {}


def idx(n):
    if n not in _IDX:
        _IDX[n] = np.random.default_rng(SEED).integers(0, n, (NBOOT, n))
    return _IDX[n]


def summ(v, sig_s):
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    n = len(v)
    med = float(np.median(v))
    sb = float(np.median(v[idx(n)], axis=1).std(ddof=1))
    return dict(n=n, median=med, sig_b=sb, Z_stat=med / sb if sb > 0 else float("nan"), Z_sys=med / math.sqrt(sb ** 2 + sig_s ** 2),
                mean=float(v.mean()), sem=float(v.std(ddof=1) / math.sqrt(n)) if n > 1 else float("nan"), median_abs=float(np.median(np.abs(v))),
                n_neg=int((v < 0).sum()))


ORDER = ["BELOW THE CEILING", "AT THE CEILING", "OVER THE CEILING", "EXCLUDED"]


def ceil_cls(s):
    if s["Z_sys"] < -2:
        return "EXCLUDED"
    if s["Z_stat"] < -2:
        return "OVER THE CEILING"
    return "AT THE CEILING" if abs(s["Z_stat"]) <= 2 else "BELOW THE CEILING"


def worse(*c):
    return max(c, key=ORDER.index)


def state(s):
    if abs(s["median"]) <= 0.07:
        return "LEVEL"
    if s["median"] < 0 and s["Z_stat"] < -2:
        return "OVER"
    if s["median"] > 0 and s["Z_stat"] > 2:
        return "SHORT"
    return "WITHIN 2 SIGMA"


def fmt(s):
    return f"{s['median']:+.3f} +- {s['sig_b']:.3f} (Z {s['Z_stat']:+.1f}, sys {s['Z_sys']:+.1f}; mean {s['mean']:+.3f} +- {s['sem']:.3f}; {s['n_neg']}/{s['n']} neg)"


def rows_for(galaxies, shifts, models=None, window_keys=("r12", "w15", "w13", "out"), gam=None, beta=0.0, f=None, arg_cat=False):
    """{model label: {rung: {radius: [per galaxy d lg M]}}}. shifts: {rung: float or per-galaxy list}."""
    models = models or [("stars", None), ("law", "canonical"), ("law", "alt"), ("routeE", "canonical"), ("routeE", "alt"), ("native", None)]
    out = {}
    for model, foot in models:
        lab = model if foot is None else f"{model}|{foot}"
        out[lab] = {}
        for rung, sh in shifts.items():
            out[lab][rung] = {k: [] for k in window_keys}
            for i, S in enumerate(galaxies):
                d = sh[i] if isinstance(sh, (list, np.ndarray)) else sh
                Ms = S["Ms0"] * 10 ** d
                arg = S["Ms0"] if arg_cat else None
                need_gc = any(k != "r12" for k in window_keys)
                gf = g_field(S, Ms, model, foot, arg) if need_gc else None
                s = None
                if need_gc:
                    gm = (S["gam111"] if gam == "cfg111" else GAMMA)
                    s = sigma_los(S["Rb"], sigma_r2(gf, gm, beta), gm, beta)
                for k in window_keys:
                    if k == "r12":
                        out[lab][rung][k].append(dl_r12(S, Ms, model, foot, f, arg) if "Mjam" in S else float("nan"))
                    else:
                        m = S[k]
                        out[lab][rung][k].append(2.0 * float(np.mean(np.log10(S["Sb"][m] / s[m]))) if m.any() else float("nan"))
    return out


def sums(tab):
    out = {}
    for lab, by in tab.items():
        out[lab] = {}
        for rung, rad in by.items():
            out[lab][rung] = {k: summ(v, SIG_S_R12 if k == "r12" else SIG_S_GC) for k, v in rad.items()}
    return out


# ------------------------------------------------------------------ main table
TAB = rows_for(GAL, RUNGS)
SUM = sums(TAB)
STARS = {r: SUM["stars"][r] for r in RUNGS}
P(f"[{time.time() - T0:.0f} s] main table done; saturated halos counted {SAT['n']}; native evaluations below the 1e12 tag {KN['below']} of {KN['n']}")

# per-galaxy errors for the first table (criteria sec. 4)
for S in GAL:
    S["sig_r12"] = math.sqrt(0.05 ** 2 + 0.10 ** 2 + (2 * S["ah"] / (S["r12"] + S["ah"]) * 0.15) ** 2)
    so = lambda m: math.sqrt(float(np.sum((S["Eb"][m] / S["Sb"][m] / math.log(10)) ** 2))) / m.sum()
    S["sig_w15"] = math.sqrt((2 * so(S["w15"])) ** 2 + 0.10 ** 2)
    S["sig_w13"] = math.sqrt((2 * so(S["w13"])) ** 2 + 0.10 ** 2)

P("\n" + "=" * 150)
P("TABLE 1. Stars alone, no halo, no law, no footing. M*(R0), M*(+0.172), M*(+0.295) against M_dyn inside the same radius.")
P("=" * 150)
P("r_1/2: M_dyn(<r12) = M_JAM/2; M*(<r12) = f_H M* (Hernquist at SLUGGS's R_e). GC window 1-5 R_e: 2 <log10 sigma_obs/sigma_pred>, gamma 3, isotropic, no gas. o = over M_dyn, O = over by 2 sigma_i.")
P(f"{'galaxy':8s} {'lgM*':>6s} {'r12':>5s} {'r12/Re':>6s} {'f_H':>5s} {'lgMdyn12':>8s} {'lgM*12':>6s} | {'R0':>7s} {'+0.172':>8s} {'+0.295':>8s} {'s_i':>5s} | {'n':>1s} {'R/Re':>10s} {'R0':>7s} {'+0.172':>8s} {'+0.295':>8s} {'s_i':>5s}")
FLAG = lambda d, s: "O" if d < -2 * s else ("o" if d < 0 else " ")
for i, S in enumerate(GAL):
    d12 = [TAB["stars"][r]["r12"][i] for r in RUNGS]
    d15 = [TAB["stars"][r]["w15"][i] for r in RUNGS]
    x = S["x"][S["w15"]]
    P(f"{S['name']:8s} {math.log10(S['Ms0']):6.2f} {S['r12']:5.2f} {S['r12'] / S['Re']:6.2f} {S['fH']:5.2f} {math.log10(0.5 * S['Mjam']):8.2f} {math.log10(S['fH'] * S['Ms0']):6.2f} | "
      + " ".join(f"{d:+7.3f}{FLAG(d, S['sig_r12'])}" for d in d12) + f" {S['sig_r12']:5.3f} | {int(S['w15'].sum()):1d} {x.min():4.2f}-{x.max():4.2f}  "
      + " ".join(f"{d:+7.3f}{FLAG(d, S['sig_w15'])}" for d in d15) + f" {S['sig_w15']:5.3f}")
N_OVER = {}
for r in RUNGS:
    N_OVER[r] = dict(r12_over=int(sum(TAB["stars"][r]["r12"][i] < 0 for i in range(len(GAL)))),
                     r12_over_2sig=int(sum(TAB["stars"][r]["r12"][i] < -2 * GAL[i]["sig_r12"] for i in range(len(GAL)))),
                     w15_over=int(sum(TAB["stars"][r]["w15"][i] < 0 for i in range(len(GAL)))),
                     w15_over_2sig=int(sum(TAB["stars"][r]["w15"][i] < -2 * GAL[i]["sig_w15"] for i in range(len(GAL)))))
    P(f"  {r:2s} (+{RUNGS[r]:.3f}): r_1/2 {fmt(STARS[r]['r12'])} -> {ceil_cls(STARS[r]['r12'])}; over {N_OVER[r]['r12_over']}, by 2 sigma_i {N_OVER[r]['r12_over_2sig']}")
    P(f"              1-5 R_e {fmt(STARS[r]['w15'])} -> {ceil_cls(STARS[r]['w15'])}; over {N_OVER[r]['w15_over']}, by 2 sigma_i {N_OVER[r]['w15_over_2sig']}")
CEIL = {r: dict(r12=ceil_cls(STARS[r]["r12"]), w15=ceil_cls(STARS[r]["w15"])) for r in RUNGS}
for r in RUNGS:
    CEIL[r]["rung"] = worse(CEIL[r]["r12"], CEIL[r]["w15"])

# ------------------------------------------------------------------ models on top
P("\n" + "=" * 150)
P("TABLE 2. The law and route E on top, each footing separately (median d lg M; state: LEVEL |m| <= 0.07, OVER / SHORT beyond it at 2 sigma). Native z = 0 line reported, no footing.")
P("=" * 150)
STATES = {}
for lab in ("law|canonical", "routeE|canonical", "law|alt", "routeE|alt", "native"):
    STATES[lab] = {}
    for r in RUNGS:
        s12, s15, s13 = SUM[lab][r]["r12"], SUM[lab][r]["w15"], SUM[lab][r]["w13"]
        STATES[lab][r] = dict(r12=state(s12), w15=state(s15), both=state(s12) == "LEVEL" and state(s15) == "LEVEL")
        P(f"  {lab:18s} {r:2s}: r_1/2 {fmt(s12)} {state(s12)}")
        P(f"  {'':18s}     1-5 R_e {fmt(s15)} {state(s15)}")
        P(f"  {'':18s}     1-3 R_e {fmt(s13)}")

P("  CFG55's full outer bins (median d lg M, R0 / I / L):")
for lab in ("stars", "law|canonical", "law|alt", "routeE|canonical", "routeE|alt", "native"):
    P(f"    {lab:18s} " + " / ".join(f"{SUM[lab][r]['out']['median']:+.3f}" for r in RUNGS))
P("  Per galaxy, canonical, d lg M at r_1/2 and 1-5 R_e (R0, I, L):")
for i, S in enumerate(GAL):
    P(f"    {S['name']:8s} law " + " ".join(f"{TAB['law|canonical'][r]['r12'][i]:+.3f}" for r in RUNGS) + " | " + " ".join(f"{TAB['law|canonical'][r]['w15'][i]:+.3f}" for r in RUNGS)
      + "   route E " + " ".join(f"{TAB['routeE|canonical'][r]['r12'][i]:+.3f}" for r in RUNGS) + " | " + " ".join(f"{TAB['routeE|canonical'][r]['w15'][i]:+.3f}" for r in RUNGS))

# ceiling rung and null rung per model and galaxy
def root(fn, lo=-2.0, hi=2.5):
    try:
        return brentq(fn, lo, hi, xtol=1e-6)
    except ValueError:
        return float("nan")


ROOTS = {}
for model, foot in (("stars", None), ("law", "canonical"), ("law", "alt"), ("routeE", "canonical"), ("routeE", "alt"), ("native", None)):
    lab = model if foot is None else f"{model}|{foot}"
    dc, dn = [], []
    for S in GAL:
        dc.append(root(lambda d: dl_r12(S, S["Ms0"] * 10 ** d, model, foot)))
        dn.append(root(lambda d: dl_gc(S, g_field(S, S["Ms0"] * 10 ** d, model, foot), S["w15"])))
    gap = [b - a for a, b in zip(dc, dn)]
    ROOTS[lab] = dict(ceil=dc, null=dn, gap=gap, s_ceil=summ(dc, SIG_S_R12), s_null=summ(dn, SIG_S_GC), s_gap=summ(gap, 0.0))
    P(f"  {lab:18s}: rung at the r_1/2 ceiling {fmt(ROOTS[lab]['s_ceil'])}")
    P(f"  {'':18s}  rung that zeroes 1-5 R_e {fmt(ROOTS[lab]['s_null'])}; gap null - ceil median {ROOTS[lab]['s_gap']['median']:+.3f} +- {ROOTS[lab]['s_gap']['sig_b']:.3f}")
P(f"[{time.time() - T0:.0f} s] roots done")

# ------------------------------------------------------------------ reported rows (criteria sec. 8)
REP = {}
models3 = [("stars", None), ("law", "canonical"), ("law", "alt"), ("routeE", "canonical"), ("routeE", "alt")]
# 1. half convention
REP["half"] = sums(rows_for(GAL, RUNGS, models3, ("r12",), f=0.5))
# 2. ATLAS3D's own population scale, half the same light
REP["a3d_pop"] = {r: summ([math.log10(S["Mjam"]) - (math.log10(S["Msalp"]) - 0.25 + d) for S in GAL], SIG_S_R12) for r, d in RUNGS.items()}
# 3. tracer and anisotropy
REP["gam111"] = sums(rows_for(GAL, RUNGS, models3, ("w15", "w13"), gam="cfg111"))
REP["beta+0.5"] = sums(rows_for(GAL, RUNGS, models3, ("w15", "w13"), beta=0.5))
REP["beta-0.5"] = sums(rows_for(GAL, RUNGS, models3, ("w15", "w13"), beta=-0.5))
# 4. centrals split
mask_c = np.array([S["name"] in CENTRALS for S in GAL])
split = {}
for nm, sel in (("no_centrals", ~mask_c), ("centrals", mask_c)):
    split[nm] = {}
    for lab, by in TAB.items():
        split[nm][lab] = {r: {k: summ(np.array(v)[sel], SIG_S_R12 if k == "r12" else SIG_S_GC) for k, v in rad.items()} for r, rad in by.items()}
REP["split"] = split
# 5. rungs T and Isig
R926 = json.load(builtins.open(os.path.join(CFG, "CFG926_small_reframings_B", "cfg926_results.json")))["R5"]["relation"]
ISIG = [R926["a"] + math.log10(R926["SC"]) + R926["b"] * (S["lsig"] - math.log10(200.0)) for S in GAL]
REP["rung_T_Isig"] = sums(rows_for(GAL, {"T": RUNG_T, "Isig": ISIG}, models3, ("r12", "w15", "w13")))
REP["Isig_values"] = dict(zip([S["name"] for S in GAL], ISIG))
# 6. M200's argument at the catalogue
REP["halo_at_catalogue"] = sums(rows_for(GAL, {"I": 0.172, "L": 0.295}, [("routeE", "canonical"), ("routeE", "alt")], ("r12", "w15"), arg_cat=True))
# 7. A4 eta table
NSH["ETAV"] = ETAV_A4
REP["eta_A4"] = sums(rows_for(GAL, RUNGS, [("routeE", "canonical"), ("routeE", "alt")], ("r12", "w15")))
NSH["ETAV"] = ETAV0
REP["eta_tables"] = dict(si1=ETAV0, a4=ETAV_A4)
P(f"[{time.time() - T0:.0f} s] reported rows 1-7 done")
# 8a. h50's 19, GC windows only
G19 = []
for r in RES50:
    S = dict(name=r["name"], Ms0=r["Mstar"], Re=r["Re"], ah=r["Re"] / 1.8153, Rb=r["Rb"], Sb=r["Sb"], Eb=r["Eb"], out=r["out"], x=r["Rb"] / r["Re"])
    if MUT:
        S["Sb"] = r["Sb"] * (1.0 if r["name"] in [g["name"] for g in GAL] else SF)
    S["w15"] = (S["x"] >= 1.0) & (S["x"] <= 5.0)
    S["w13"] = (S["x"] >= 1.0) & (S["x"] <= 3.0)
    G19.append(S)
REP["h50_19"] = sums(rows_for(G19, RUNGS, models3, ("w15", "w13")))
# 8b. NGC 821 restored: CFG55's key fix, in memory (no file changes)
if not MUT:
    PKF = os.path.join(CFG, "CFG55_h50_keyfix.py")
    KF = builtins.open(PKF).read()
    NSK = {"__file__": PKF, "__name__": "cfg55_keyfix_ro", "open": ro_open}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(KF[:KF.index("path55 = os.path.join")], PKF, "exec"), NSK)
        s55k = builtins.open(P55).read()
        for (old, new), what in ((NSK["P3"], "P3"), (NSK["P4"], "P4"), (NSK["P5"], "P5")):
            s55k = NSK["sub_once"](s55k, old, new, what)
        NS17 = {"__file__": P55, "__name__": "cfg55_kf_ro", "open": ro_open, "_PATCH38": lambda s: NSK["sub_once"](s, *NSK["P2"], "P2")}
        exec(compile(s55k[:s55k.index(CUT55)], P55, "exec"), NS17)
    NSK["C4"].exec_slices = NSK["_orig_exec_slices"]
    G17 = [rec(g) for g in NS17["G16"]]
    for S in G17:
        S["w15"] = (S["x"] >= 1.0) & (S["x"] <= 5.0)
        S["w13"] = (S["x"] >= 1.0) & (S["x"] <= 3.0)
        S["fH"] = S["r12"] ** 2 / (S["r12"] + S["ah"]) ** 2
    REP["n17_ngc821"] = dict(names=[S["name"] for S in G17], rows=sums(rows_for(G17, RUNGS, models3, ("r12", "w15", "w13"))))
P(f"[{time.time() - T0:.0f} s] reported row 8 done")
# 9. the four centrals on CFG528b's measured tracers and anisotropy (row M), with and without measured gas truncated at the X-ray edge
P528 = os.path.join(CFG, "CFG528_sluggs_centrals_mechanism", "cfg528b_measured_tracers.py")
SB = builtins.open(P528).read()
NB = {"__file__": P528, "__name__": "cfg528b_ro", "open": ro_open}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(SB[:SB.index('P("=" * 124)')], "cfg528b_measured_tracers", "exec"), NB)
BIN, CEN4, A0L, RG4, Gs, KPC4, field, measured_pops, sig_multi, off_pops = (NB[k] for k in ("B", "CEN", "A0", "RG", "G", "KPC", "field", "measured_pops", "sig_multi", "off_pops"))
NS528 = NB["NS"]
MS4, gas_profile, GAL4 = NS528["MSUN"], NS528["gas_profile"], NB["GAL"]
J528 = json.load(builtins.open(os.path.join(CFG, "CFG528_sluggs_centrals_mechanism", "cfg528b_measured_tracers_results.json")))
k1d = 0.0
for ft, a0 in A0L.items():
    for n in CEN4:
        k1d = max(k1d, abs(off_pops(n, field(n, a0, "K0"), measured_pops(n)) - J528["rows"]["M K0"][ft]["per"][f"NGC{n}"]))
POPS4 = {n: measured_pops(n) for n in CEN4}


def row4(n, Ms, model, foot, gas):
    b = BIN[n]
    Mg = None if not gas else gas_profile(n, "trunc")
    Mx = 0.0 if Mg is None else Mg
    gN = Gs * (Ms * RG4 ** 2 / (RG4 + b["ah"]) ** 2 + Mx) * MS4 / (RG4 * KPC4) ** 2
    if model == "stars":
        g = gN
    elif model == "law":
        g = gN * nu1(gN / A0[foot])
    else:
        g = gN + HF * Gs * halo_of(foot, RG4 * 1e3, Ms, 0.0, Ms, 0.0, "E")[0] * MS4 / (RG4 * KPC4) ** 2
    s = sig_multi(b["Rb"], g, POPS4[n])
    x = b["Rb"] / b["Re"]
    m = (x >= 1.0) & (x <= 5.0)
    return 2.0 * float(np.mean(np.log10(b["Sb"][m] / s[m])))


R9 = {}
for gas in (False, True):
    gk = "trunc_gas" if gas else "no_gas"
    R9[gk] = {}
    for model, foot in models3:
        lab = model if foot is None else f"{model}|{foot}"
        R9[gk][lab] = {}
        for r, d in RUNGS.items():
            per = {f"NGC{n}": row4(n, 10 ** GAL4[n]["lMs"] * 10 ** d, model, foot, gas) for n in CEN4}
            R9[gk][lab][r] = dict(per=per, median=float(np.median(list(per.values()))), mean=float(np.mean(list(per.values()))))
REP["four_centrals_measured_tracers"] = R9
P(f"[{time.time() - T0:.0f} s] reported row 9 done")
# 10. Alabi+17's published masses at 5 R_e (read as CFG431 reads them; its column name)
tex = builtins.open(os.path.join(EXT, "alabi2017", "src", "halov3.tex")).read()
num = lambda s: re.sub(r"[^0-9.\-]", "", s.split("^")[0].split("_")[0])
T2 = {}
for line in (tex.split("\\begin{table*}")[2] + tex.split("\\begin{table*}")[3]).split("\n"):
    c = [x.strip() for x in line.split("&")]
    if len(c) >= 6 and re.match(r"^\$\s*\d{3,4}\s*\$", c[0]) and re.match(r"^\$\s*0\s*\$", c[1]):
        mt, emt = [float(v) for v in c[4].strip("$").split("\\pm")]
        fd, efd = [float(v) for v in c[5].strip("$").split("\\pm")]
        T2[num(c[0])] = (mt * 1e11, fd, emt * 1e11, efd)
R10 = {}
for r, d in RUNGS.items():
    per, over2 = {}, 0
    for S in GAL:
        k = S["name"].replace("NGC", "").lstrip("0")
        if k in T2:
            mt, fd, emt, efd = T2[k]
            v = -math.log10(max(1.0 - fd, 1e-3)) - d
            per[S["name"]] = v
            over2 += int(v < -2 * efd / (max(1.0 - fd, 1e-3) * math.log(10)))
    R10[r] = dict(per=per, s=summ(list(per.values()), SIG_S_GC), over_2sig=over2)
REP["alabi17_5Re"] = R10
# 11. GC estimator against JAM, stars at R0: innermost bin of the 1-5 R_e window against r_1/2
xc = []
for i, S in enumerate(GAL):
    j = np.where(S["w15"])[0][0]
    m = np.zeros(len(S["Rb"]), bool)
    m[j] = True
    xc.append(dl_gc(S, g_field(S, S["Ms0"], "stars"), m) - TAB["stars"]["R0"]["r12"][i])
REP["gc_minus_jam_innermost_bin"] = dict(per=xc, median=float(np.median(xc)), sd=float(np.std(xc, ddof=1)))
# 12. M*/M_JAM at the rungs, four centrals
REP["Mstar_over_MJAM_centrals"] = {S["name"]: {r: S["Ms0"] * 10 ** d / S["Mjam"] for r, d in RUNGS.items()} for S in GAL if S["name"] in CENTRALS}

# ------------------------------------------------------------------ checks
P("\n" + "=" * 150)
P("CHECKS")
P("=" * 150)
# K1 (a) CFG55's committed law offsets; (b) stars path = h50's off_newt; (c) law path with CFG55's kernel = committed SLUGGS-mass law mean; (d) CFG528b row M K0
ka = kam = 0.0
for f in FOOTS:
    ML = [NS["law_mass_g"](g, f) for g in G16]
    per = [NS["offset"](g, f, m, "law")[0] for g, m in zip(G16, ML)]
    ka = max(ka, max(abs(a - b) for a, b in zip(per, J55[f]["law"]["per"])))
    kam = max(kam, max(abs(math.log10(a) - b) for a, b in zip(ML, J55[f]["logM_law"])))
kb = 0.0
for S, g in zip(GAL, G16):
    o = 0.5 * dl_gc(S, g_field(S, S["Ms0"], "stars"), S["out"])
    kb = max(kb, abs(o - g["r"]["off_newt"]))
kc = 0.0
for f in FOOTS:
    vals = []
    for S in GAL:
        def gh(r):
            gN = G_ * (S["Ms0"] * MSUN * r ** 2 / (r + S["ah"]) ** 2) / (r * KPC) ** 2
            return gN * nu_h(gN / A0SI[f])
        vals.append(0.5 * dl_gc(S, gh, S["out"]))
    kc = max(kc, abs(float(np.mean(vals)) - J55[f]["law_sluggs"]["mean"]))
checks["K1"] = ka <= 1e-10 and kam <= 1e-10 and kb <= 1e-12 and kc <= 1e-10 and k1d <= 1e-6
P(f"K1 record reproduced: (a) CFG55 law offsets |d| {ka:.1e}, log M*_law |d| {kam:.1e}; (b) stars = h50 off_newt |d| {kb:.1e}; (c) CFG55's kernel = law_sluggs mean |d| {kc:.1e}; (d) CFG528b row M K0 |d| {k1d:.1e}: {'PASS' if checks['K1'] else 'FAIL'}")
# K2 radius matching
A3 = NS["A3"]; SL = NS["SL"]; fnum = NS["fnum"]; ARCSEC = NS["ARCSEC"]
k2a = 0.0
for S, g in zip(GAL, G16):
    a = A3[S["name"]]; s = SL[S["name"]]; DS, DA = float(s["Dist"]), float(a["Dist_Mpc"])
    r12 = 10 ** fnum(a["logr12"]) * ARCSEC * DS * 1e3
    Mj = JF * 10 ** (fnum(a["logML_JAM"]) + fnum(a["logL"])) * DS / DA
    k2a = max(k2a, abs(r12 / S["r12"] - 1), abs(Mj / S["Mjam"] - 1))
dlr = np.array([fnum(a["logr12"]) - fnum(a["logRe"]) for a in A3.values()])
med_lr = float(np.median(dlr[np.isfinite(dlr)]))
k2b = abs(med_lr - math.log10(1.33)) <= 0.03
fh_133 = 1.33 ** 2 / (1.33 + 1 / 1.8153) ** 2
k2c = abs(fh_133 - 0.5) <= 1e-3
fhs = [S["fH"] for S in GAL]
k2d = round(min(fhs), 2) == 0.28 and round(max(fhs), 2) == 0.57 and max(abs(S["fH"] - NS["hernq_frac"](g)) for S, g in zip(GAL, G16)) <= 1e-12
k2e = all(S["w15"].any() and S["w13"].any() and bool(np.all(S["out"][S["w15"]])) for S in GAL)
checks["K2"] = k2a <= 1e-9 and k2b and k2c and k2d and k2e
P(f"K2 radius matching: (a) r12, M_JAM from raw TSV max rel |d| {k2a:.1e}; (b) median lg(r12/R_e) {med_lr:.3f} vs lg 1.33 {math.log10(1.33):.3f}; (c) f_H(1.33 R_e) {fh_133:.4f}; "
  f"(d) f_H range {min(fhs):.2f}-{max(fhs):.2f} (CFG55 0.28-0.57); (e) all 16 have window bins, inside h50's outer bins: {k2e}: {'PASS' if checks['K2'] else 'FAIL'}")
# K3 route E and native
F1 = json.load(builtins.open(os.path.join(REB, "FC1_cold_share_native_eta", "fc1_results.json")))["fc1"]["S_over_Scoll"]
k3a = max(abs(FC * NSH["eta_conv"](10.0 ** e) - F1[str(e)]) for e in (12, 13, 14))
k3b, nsat = 0.0, 0
for f in FOOTS:
    for S in GAL:
        for d in RUNGS.values():
            Ms = S["Ms0"] * 10 ** d
            n0 = SAT["n"]
            _, inf = halo_of(f, np.array([1.0]), Ms, 0.0, Ms, 0.0, "E")
            Mh2, _ = halo_of(f, np.array([inf["R200"]]), Ms, 0.0, Ms, 0.0, "E")
            if SAT["n"] > n0:
                nsat += 1
            else:
                k3b = max(k3b, abs(float(Mh2[0]) / inf["M200"] - 1))
k3c = max(abs(math.exp(float(np.interp(0.0, XL, t[1]))) - 1.0) for t in TAGS)
k3d = 'A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}' in P2T
checks["K3"] = k3a <= 1e-3 and k3b <= 1e-8 and k3c <= 1e-3 and k3d
P(f"K3 route E and native: (a) S/Sigma_coll nodes |d| {k3a:.1e} vs FC1 {[round(F1[str(e)], 3) for e in (12, 13, 14)]}; (b) M_h(R200) = M200 max rel |d| {k3b:.1e}, saturated {nsat}; (c) native m(x=1) - 1 max {k3c:.1e}; (d) a0 = P2's text {k3d}: {'PASS' if checks['K3'] else 'FAIL'}")
# K4 linearity of the stars path
k4 = 0.0
for r, d in RUNGS.items():
    for k in ("r12", "w15"):
        k4 = max(k4, max(abs(a - (b - d)) for a, b in zip(TAB["stars"][r][k], TAB["stars"]["R0"][k])))
checks["K4"] = k4 <= 1e-9
P(f"K4 stars' d lg M(+D) = d lg M(R0) - D: max |d| {k4:.1e}: {'PASS' if checks['K4'] else 'FAIL'}")

# ------------------------------------------------------------------ qualifiers and verdict
QUAL = []
half = {r: ceil_cls(REP["half"]["stars"][r]["r12"]) for r in RUNGS}
a3d = {r: ceil_cls(REP["a3d_pop"][r]) for r in RUNGS}
tr = {nm: {r: ceil_cls(REP[nm]["stars"][r]["w15"]) for r in RUNGS} for nm in ("gam111", "beta+0.5", "beta-0.5")}
nc = {r: worse(ceil_cls(split["no_centrals"]["stars"][r]["r12"]), ceil_cls(split["no_centrals"]["stars"][r]["w15"])) for r in RUNGS}
if any(half[r] != CEIL[r]["r12"] for r in ("I", "L")):
    QUAL.append("RADIUS-CONVENTION-DEPENDENT")
if any(a3d[r] != CEIL[r]["r12"] for r in ("I", "L")):
    QUAL.append("SCALE-DEPENDENT")
if any(tr[nm][r] != CEIL[r]["w15"] for nm in tr for r in ("I", "L")):
    QUAL.append("TRACER-DEPENDENT")
if any(nc[r] != CEIL[r]["rung"] for r in ("I", "L")):
    QUAL.append("CENTRALS-DEPENDENT")
P("\n" + "=" * 150)
P("CLASSES AND VERDICT")
P("=" * 150)
for r in RUNGS:
    P(f"  stars {r:2s}: r_1/2 {CEIL[r]['r12']} | 1-5 R_e {CEIL[r]['w15']} | rung {CEIL[r]['rung']}.  half convention: {half[r]}; ATLAS3D population: {a3d[r]} ({fmt(REP['a3d_pop'][r])}); "
      f"gamma CFG111 {tr['gam111'][r]}; beta +0.5 {tr['beta+0.5'][r]}; beta -0.5 {tr['beta-0.5'][r]}; 12 non-centrals {nc[r]}")
VERD = {}
for f in FOOTS:
    lv = [m for m in ("law", "routeE") if STATES[f"{m}|{f}"]["I"]["both"]]
    c = [CEIL["I"]["r12"], CEIL["I"]["w15"]]
    if "EXCLUDED" in c:
        v = "SR1 FAIL"
    elif "OVER THE CEILING" in c:
        v = "SR1 OVER"
    elif lv:
        v = "SR1 PASS (" + ", ".join(lv) + " LEVEL AT BOTH)"
    else:
        v = "SR1 ALLOWED, NOT LEVEL"
    VERD[f] = v
    P(f"  [{f}] law at I: r_1/2 {STATES[f'law|{f}']['I']['r12']}, 1-5 R_e {STATES[f'law|{f}']['I']['w15']}; route E at I: r_1/2 {STATES[f'routeE|{f}']['I']['r12']}, 1-5 R_e {STATES[f'routeE|{f}']['I']['w15']} -> {v}")
ALLK = all(checks.values())
vtxt = VERD["canonical"] + "; LITERAL R2: " + CEIL["L"]["rung"] + "".join(f" [{q}]" for q in QUAL)
if VERD["canonical"] != VERD["alt"]:
    vtxt += f"  (alt: {VERD['alt']})"
if not ALLK:
    vtxt = "NO VERDICT, a K check failed (" + vtxt + " before the failed check)"
P(f"\nVERDICT: {vtxt}")

# ------------------------------------------------------------------ Argon's lines (criteria sec. 7)
P("\n" + "=" * 150)
P("ARGON'S LINES (scored on three rows; each HIT named). R2 = +0.295. These scores change no class.")
P("=" * 150)
ARG = {}
for rung_lab, rg, rg0 in (("at R2 (+0.295), as stated", "L", "R0"), ("reported, at the carried +0.172", "I", "R0")):
    ARG[rg] = {}
    P(f"  {rung_lab}:")
    for lab in ("stars", "law|canonical", "law|alt", "routeE|canonical", "routeE|alt"):
        s15, s13, s12, s0 = SUM[lab][rg]["w15"], SUM[lab][rg]["w13"], SUM[lab][rg]["r12"], SUM[lab][rg0]["w13"]
        a = dict(A1=abs(s15["median"]) <= 0.07, A1_jam=abs(s12["median"]) <= 0.07, A2=abs(s13["median"]) <= 0.05, A2_abs=s13["median_abs"] <= 0.05, A3=0.18 <= s0["median"] <= 0.25,
                 A4_r12=s12["Z_stat"] < -2, A4_w15=(s15["Z_stat"] < -2 if lab == "stars" else abs(s15["Z_stat"]) > 2), Zsys_r12=s12["Z_sys"], Zsys_w15=s15["Z_sys"],
                 m15=s15["median"], m13=s13["median"], m12=s12["median"], m13_abs=s13["median_abs"], m0_13=s0["median"])
        ARG[rg][lab] = a
        P(f"    {lab:18s} A1 |med 1-5| {a['m15']:+.3f} {'HIT' if a['A1'] else 'MISS'}; JAM column {a['m12']:+.3f} {'HIT' if a['A1_jam'] else 'MISS'}; A2 |med 1-3| {a['m13']:+.3f} {'HIT' if a['A2'] else 'MISS'}; "
          f"median|.| {a['m13_abs']:.3f} {'HIT' if a['A2_abs'] else 'MISS'}; A3 R0 1-3 {a['m0_13']:+.3f} {'HIT' if a['A3'] else 'MISS'}; "
          f"A4 r_1/2 {'FIRES' if a['A4_r12'] else 'no'} (Z {s12['Z_stat']:+.1f}, sys {a['Zsys_r12']:+.1f}); 1-5 {'FIRES' if a['A4_w15'] else 'no'} (Z {s15['Z_stat']:+.1f}, sys {a['Zsys_w15']:+.1f})")

# ------------------------------------------------------------------ reported rows printed
P("\n" + "=" * 150)
P("REPORTED (no class weight except the qualifiers)")
P("=" * 150)
P(f"Native z = 0 line: below the 1e12 tag in {KN['below']} of {KN['n']} shape evaluations (clamped). Tags lg M_t {[round(t[0], 2) for t in TAGS]}.")
P("Half convention at r_1/2 (median d lg M):")
for lab in REP["half"]:
    P(f"  {lab:18s} " + "; ".join(f"{r} {fmt(REP['half'][lab][r]['r12'])}" for r in RUNGS))
P("ATLAS3D population Chabrier, half the same light: " + "; ".join(f"{r} {fmt(REP['a3d_pop'][r])}" for r in RUNGS))
for nm in ("gam111", "beta+0.5", "beta-0.5"):
    P(f"{nm} (1-5 R_e median; 1-3 R_e median):")
    for lab in REP[nm]:
        P(f"  {lab:18s} " + "; ".join(f"{r} {REP[nm][lab][r]['w15']['median']:+.3f} (Z {REP[nm][lab][r]['w15']['Z_stat']:+.1f}) / {REP[nm][lab][r]['w13']['median']:+.3f}" for r in RUNGS))
P("Non-centrals (12) and centrals (4), median d lg M at r_1/2 / 1-5 R_e:")
for nm in ("no_centrals", "centrals"):
    for lab in ("stars", "law|canonical", "routeE|canonical", "law|alt", "routeE|alt", "native"):
        P(f"  {nm:12s} {lab:18s} " + "; ".join(f"{r} {split[nm][lab][r]['r12']['median']:+.3f} / {split[nm][lab][r]['w15']['median']:+.3f}" for r in RUNGS))
P(f"Rung T = +{RUNG_T:.3f} and Isig (own sigma_e, values {min(ISIG):.3f}-{max(ISIG):.3f}), median d lg M at r_1/2 / 1-5 R_e / 1-3 R_e:")
for lab in REP["rung_T_Isig"]:
    P(f"  {lab:18s} " + "; ".join(f"{r} {REP['rung_T_Isig'][lab][r]['r12']['median']:+.3f} / {REP['rung_T_Isig'][lab][r]['w15']['median']:+.3f} / {REP['rung_T_Isig'][lab][r]['w13']['median']:+.3f}" for r in ("T", "Isig")))
P("Stars at T: r_1/2 " + fmt(REP["rung_T_Isig"]["stars"]["T"]["r12"]) + " -> " + ceil_cls(REP["rung_T_Isig"]["stars"]["T"]["r12"]))
P("Route E with M200's argument at the catalogue, median at r_1/2 / 1-5 R_e: " + "; ".join(f"{lab} {r} {REP['halo_at_catalogue'][lab][r]['r12']['median']:+.3f} / {REP['halo_at_catalogue'][lab][r]['w15']['median']:+.3f}" for lab in REP["halo_at_catalogue"] for r in ("I", "L")))
P(f"Route E on CE1's A4 eta {[round(x, 2) for x in ETAV_A4]} (SI1's {[round(x, 2) for x in ETAV0]}), median at r_1/2 / 1-5 R_e: " + "; ".join(f"{lab} {r} {REP['eta_A4'][lab][r]['r12']['median']:+.3f} / {REP['eta_A4'][lab][r]['w15']['median']:+.3f}" for lab in REP["eta_A4"] for r in RUNGS))
P("h50's 19, GC only, median 1-5 R_e / 1-3 R_e:")
for lab in REP["h50_19"]:
    P(f"  {lab:18s} " + "; ".join(f"{r} {REP['h50_19'][lab][r]['w15']['median']:+.3f} / {REP['h50_19'][lab][r]['w13']['median']:+.3f}" for r in RUNGS))
if "n17_ngc821" in REP:
    P(f"N = 17 with NGC 821 restored ({len(REP['n17_ngc821']['names'])} galaxies), median at r_1/2 / 1-5 R_e:")
    for lab in REP["n17_ngc821"]["rows"]:
        P(f"  {lab:18s} " + "; ".join(f"{r} {REP['n17_ngc821']['rows'][lab][r]['r12']['median']:+.3f} / {REP['n17_ngc821']['rows'][lab][r]['w15']['median']:+.3f}" for r in RUNGS))
P("Four centrals on CFG528b's measured tracers and anisotropy, catalogue masses, 1-5 R_e, per galaxy (NGC 4486, 4365, 4374, 5846):")
for gk in R9:
    for lab in R9[gk]:
        P(f"  {gk:9s} {lab:18s} " + "; ".join(f"{r} " + " ".join(f"{R9[gk][lab][r]['per'][f'NGC{n}']:+.3f}" for n in CEN4) for r in RUNGS))
P("Alabi+17 M_tot(<5 R_e), f_DM column, beta = 0: d lg M = -lg(1 - f_DM) - D: " + "; ".join(f"{r} {fmt(R10[r]['s'])}, over by 2 sigma {R10[r]['over_2sig']}" for r in RUNGS))
P("  per galaxy at R0: " + ", ".join(f"{k} {v:+.2f}" for k, v in R10["R0"]["per"].items()))
P(f"GC estimator against JAM, stars at R0, innermost window bin minus r_1/2: median {REP['gc_minus_jam_innermost_bin']['median']:+.3f}, SD {REP['gc_minus_jam_innermost_bin']['sd']:.3f}")
P("M*/M_JAM at the rungs, four centrals (SG1's JAM analogue 0.87-0.95): " + "; ".join(f"{k} " + "/".join(f"{v[r]:.2f}" for r in RUNGS) for k, v in REP["Mstar_over_MJAM_centrals"].items()))

# ------------------------------------------------------------------ the twin's teeth
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
checks["K5"] = rss < 1.0
P(f"\nK5 peak RSS {rss:.2f} GB: {'PASS' if checks['K5'] else 'FAIL'}")
ALLK = all(checks.values())
tooth = None
if MUT:
    B0 = json.load(builtins.open(os.path.join(HERE, "sr1_results.json")))
    t1 = STARS["R0"]["r12"]["median"] - B0["stars"]["R0"]["r12"]["median"]
    t2 = STARS["R0"]["w15"]["median"] - B0["stars"]["R0"]["w15"]["median"]
    g0 = np.abs(np.array(B0["per_galaxy"]["routeE|canonical"]["R0"]["w15"]) - np.array(B0["per_galaxy"]["stars"]["R0"]["w15"]))
    g1 = np.abs(np.array(TAB["routeE|canonical"]["R0"]["w15"]) - np.array(TAB["stars"]["R0"]["w15"]))
    tooth = dict(shift_r12=t1, shift_w15=t2, gap_shrinks=bool(np.all(g1 < g0)), K1_fails=not checks["K1"])
    bites = abs(t1 - math.log10(0.5)) <= 1e-6 and abs(t2 - 2 * math.log10(0.8)) <= 1e-6 and tooth["gap_shrinks"] and tooth["K1_fails"]
    P(f"MUTATE: stars' median shift at r_1/2 {t1:+.5f} (-0.30103), GC window {t2:+.5f} (-0.19382); route E gap shrinks in every galaxy {tooth['gap_shrinks']}; K1 fails {tooth['K1_fails']}: tooth {'BITES' if bites else 'DOES NOT BITE'}")
P(f"\nchecks {sum(checks.values())}/{len(checks)}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks.items()) + f"; {time.time() - T0:.0f} s")

# ------------------------------------------------------------------ outputs (no timing in the JSON, no local paths in either)
gal_info = [dict(name=S["name"], lgMs=math.log10(S["Ms0"]), Re=S["Re"], r12=S["r12"], fH=S["fH"], lgMdyn12=math.log10(0.5 * S["Mjam"]), lgMs12=math.log10(S["fH"] * S["Ms0"]),
                 sig_r12=S["sig_r12"], sig_w15=S["sig_w15"], sig_w13=S["sig_w13"], n_w15=int(S["w15"].sum()), n_w13=int(S["w13"].sum()), gam111=S["gam111"]) for S in GAL]
RES = dict(criteria="1d0fea100e", mutate=MUT, rungs=RUNGS, rung_T=RUNG_T, sig_s=dict(r12=SIG_S_R12, gc=SIG_S_GC), bootstrap=dict(n=NBOOT, seed=SEED), galaxies=gal_info, per_galaxy=TAB, summaries=SUM,
           stars=STARS, n_over=N_OVER, ceiling=CEIL, states=STATES, roots=ROOTS, reported=REP, classes_variants=dict(half=half, a3d=a3d, tracer=tr, no_centrals=nc), qualifiers=QUAL, verdict=dict(footings=VERD, text=vtxt), argon=ARG,
           checks={k: bool(v) for k, v in checks.items()}, k_values=dict(k1a=ka, k1am=kam, k1b=kb, k1c=kc, k1d=k1d, k2a=k2a, med_lr=med_lr, k3a=k3a, k3b=k3b, k3c=k3c, k4=k4, n_sat=nsat), saturated_counted=SAT["n"], native=dict(below=KN["below"], n=KN["n"]), tooth=tooth)


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    return o


json.dump(clean(RES), builtins.open(os.path.join(HERE, f"sr1_results{TAG}.json"), "w"), indent=1, sort_keys=False)
builtins.open(os.path.join(HERE, f"sr1{TAG}.out"), "w").write("\n".join(OUT).replace(os.path.dirname(REPO), "<root>") + "\n")
if MUT:
    sys.exit(1 if bites else 0)
sys.exit(0 if ALLK else 1)
