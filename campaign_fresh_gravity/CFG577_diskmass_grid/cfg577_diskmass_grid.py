"""CFG577: DiskMass sigma_z with the CFG516 grid solver. Criteria: FROZEN_CRITERIA.md (d0473b924).

Re-uses, by execution and unedited: CFG576's table parsing (data in CFG576_diskmass_sigz/data/) and CFG516's
grid models (CFG514 solver, nu_mono, PD = full QUMOND, RM-phi = round cold mass equal to PD's enclosed phantom).
MUTATE: CFG577_MUTATE=1 multiplies a0 by 10 in RM only; outputs carry the _MUTATE tag.
Optional: CFG577_ONLY=calib runs the alt-footing PD calibration and controls only.
"""
import os, sys, json, math, time
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
# ---- CFG576 parsing (head only: everything before its banner)
SRC576 = os.path.join(HERE, "..", "CFG576_diskmass_sigz", "cfg576_diskmass.py")
h576 = open(SRC576).read().split('P("=" * 100)')[0]
n576 = {"__file__": os.path.abspath(SRC576), "__name__": "cfg576_head"}
exec(compile(h576, "cfg576_head", "exec"), n576)
gal, MSUN_K = n576["gal"], n576["MSUN_K"]
# ---- CFG516 grid models (head only)
SRC516 = os.path.join(HERE, "..", "CFG516_round_cold_energy", "cfg516_mw.py")
h516 = open(SRC516).read().split("# ------------------------------------------------------------------ controls")[0]
n516 = {"__file__": os.path.abspath(SRC516)}
_so = sys.stdout; sys.stdout = open(os.devnull, "w")
exec(compile(h516, "cfg516_head", "exec"), n516)
sys.stdout = _so
GR, Base, FieldModel, build_PD = n516["GR"], n516["Base"], n516["FieldModel"], n516["build_PD"]
flux_mass, RS, G = n516["flux_mass"], n516["RS"], n516["G"]
A0_ORIG = dict(n516["A0"])

MUTATE = os.environ.get("CFG577_MUTATE", "0") == "1"
ONLY = os.environ.get("CFG577_ONLY", "")
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


AS2KPC = math.pi / 180 / 3600 * 1000.0


def galaxy(g, hz_scale=1.0, gas=True):
    kpc_as = g["D"] * AS2KPC
    hR, hz = g["hR"], g["hz"] * hz_scale
    I0 = 10 ** (0.4 * (MSUN_K + 21.572 - g["mu0"])) * 1e6
    Ld = 2 * math.pi * I0 * hR * hR
    Ma = 10 ** g["lMatom"] if gas else 0.0
    Mm = 10 ** g["lMmol"] if gas else 0.0
    Vflat = g["Varot"] / math.sin(math.radians(g["iTF"])); rs = g["rs_as"] * kpc_as
    hs = g["hsz_as"] * kpc_as
    return dict(hR=hR, hz=hz, I0=I0, Ld=Ld, Ma=Ma, Mm=Mm, BD=g["BD"],
                vrc=lambda R: Vflat * math.tanh(R / rs), smeas=lambda R: g["sz0"] * math.exp(-R / hs))


def rho_fun(t, Y):
    hR, hz = t["hR"], t["hz"]; Mb = t["BD"] * t["Ld"] * Y; a = 0.2

    def f(R, z):
        z = np.abs(z); r = np.maximum(np.sqrt(R * R + z * z), 1e-6)
        stars = Y * t["I0"] * np.exp(-R / hR) / (2 * hz) * np.exp(-z / hz)
        bul = Mb * a / (2 * math.pi * r * (r + a) ** 3) if Mb > 0 else 0.0
        hg = 2 * hR; zg = 0.10
        atom = t["Ma"] / (2 * math.pi * hg * hg) * np.exp(-R / hg) / (4 * zg) / np.cosh(np.minimum(z / (2 * zg), 300)) ** 2
        zm = 0.05
        mol = t["Mm"] / (2 * math.pi * hR * hR) * np.exp(-R / hR) / (4 * zm) / np.cosh(np.minimum(z / (2 * zm), 300)) ** 2
        return stars + bul + atom + mol
    return f


def models(t, Y, foot, which, a0mult_rm=1.0):
    base = Base("gal", rho_fun(t, Y))
    out = {}
    if "N" in which:
        out["N"] = FieldModel(base, 1.0)
    if "PD" in which:
        n516["A0"] = dict(A0_ORIG)
        out["PD"] = build_PD(base, 1.0, foot)[0]
    if "RM" in which:
        n516["A0"] = {k: v * a0mult_rm for k, v in A0_ORIG.items()}
        pd, _ = build_PD(base, 1.0, foot)
        Mphi = flux_mass(pd.gm.gRz, RS) - base.Menc
        out["RM"] = FieldModel(base, 1.0, Mcold=Mphi)
        n516["A0"] = dict(A0_ORIG)
    return out


def jeans_sigma(model, R, hz):
    z = np.linspace(0, 12 * hz, 2401); rho = np.exp(-z / hz)
    K = np.abs(model.Kz(np.full_like(z, R), z))
    return math.sqrt(np.trapz(z * rho * K, z) / np.trapz(rho, z))


def fit_and_predict(g, R_over_hR, foot, model, a0mult_rm=1.0, **kw):
    t = galaxy(g, **kw); R = R_over_hR * t["hR"]; v2 = t["vrc"](R) ** 2

    def f(Y):
        m = models(t, Y, foot, [model], a0mult_rm)[model]
        return float(m.vc(np.array([R]))[0]) ** 2 - v2
    try:
        lo, hi = f(0.02), f(5.0)
        if lo > 0 or hi < 0:
            return None
        Y = brentq(f, 0.02, 5.0, xtol=2e-3, rtol=2e-3)
    except Exception:
        return None
    m = models(t, Y, foot, [model], a0mult_rm)[model]
    return dict(Y=Y, r=jeans_sigma(m, R, t["hz"]) / t["smeas"](R))


def median_ci(x, seed=577):
    x = np.array([v for v in x if v is not None and np.isfinite(v)])
    if len(x) == 0:
        return float("nan"), float("nan"), float("nan"), 0
    bs = np.median(np.random.default_rng(seed).choice(x, size=(2000, len(x))), axis=1)
    return float(np.median(x)), float(np.percentile(bs, 16)), float(np.percentile(bs, 84)), len(x)


def summarize(per, label):
    rs = [p["r"] for p in per.values() if p]; Ys = [p["Y"] for p in per.values() if p]
    med, lo, hi, n = median_ci(rs)
    Ym = float(np.median(Ys)) if Ys else float("nan")
    gY = n >= 25 and 0.3 <= Ym <= 1.0
    cons = 0.85 <= med <= 1.15 and gY
    P(f"  {label}: median r = {med:.3f} [{lo:.3f}, {hi:.3f}]  n = {n}/30  median Y_K = {Ym:.3f}  G-Y {'pass' if gY else 'FAIL'}  -> {'CONSISTENT' if cons else 'not consistent'}")
    return dict(med=med, lo=lo, hi=hi, n=n, Ymed=Ym, gY=gY, consistent=cons)


T0 = time.time()
P("=" * 100)
P(f"CFG577  DiskMass sigma_z, grid solver  {'*** MUTATE: a0 x10 in RM ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)

P("\n--- controls")
g0 = gal[1087]; t0 = galaxy(g0, gas=False); t0["BD"] = 0.0
b0 = Base("c", rho_fun(t0, 0.5))
check(abs(b0.Mb / (0.5 * t0["Ld"]) - 1) < 0.02, f"C1 grid stellar mass {b0.Mb:.4e} vs analytic {0.5 * t0['Ld']:.4e} (2%)")
Rc = 1.5 * t0["hR"]; Sig = 0.5 * t0["I0"] * math.exp(-Rc / t0["hR"])
sJ = jeans_sigma(FieldModel(b0, 1.0), Rc, t0["hz"]); sK = math.sqrt(1.5 * math.pi * G * Sig * t0["hz"])
check(abs(sJ / sK - 1) < 0.05, f"C3 Jeans integral on a Newtonian exponential disc {sJ:.2f} vs 1.5 pi G Sigma h_z -> {sK:.2f} km/s (5%)")

res = {}
P("\n--- calibration: PD, alt footing, 1.5 h_R")
per = {u: fit_and_predict(g, 1.5, "alt", "PD") for u, g in gal.items()}
res["PD_alt_1.5"] = per
cal = summarize(per, "PD  alt  1.5 h_R")
gcal = 1.15 <= cal["med"] <= 1.45
check(gcal, f"G-cal PD alt median r {cal['med']:.3f} within [1.15, 1.45] (Angus+15 ~1.3)")
P(f"  [{time.time() - T0:.0f} s]")
if ONLY == "calib":
    open(os.path.join(HERE, f"cfg577_calib{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0)

S = {}
for foot in ("canonical", "alt"):
    for rad in (1.5, 2.2):
        for mdl in ("RM", "PD"):
            key = f"{mdl}_{foot}_{rad}"
            if key not in res:
                res[key] = {u: fit_and_predict(g, rad, foot, mdl, a0mult_rm=(10.0 if MUTATE else 1.0)) for u, g in gal.items()}
            S[key] = summarize(res[key], f"{mdl:3s} {foot:9s} {rad} h_R")
        P(f"  [{time.time() - T0:.0f} s]")
pn = {u: fit_and_predict(g, 1.5, "canonical", "N") for u, g in gal.items()}
summarize(pn, "C2 Newtonian canonical 1.5 h_R (reference)")

P("\n--- verdict (primary 1.5 h_R)")
calls = {}
for foot in ("canonical", "alt"):
    rm, pd = S[f"RM_{foot}_1.5"]["consistent"], S[f"PD_{foot}_1.5"]["consistent"]
    calls[foot] = ("INCONCLUSIVE" if not gcal else "ROUND FAVOURED" if rm and not pd else
                   "PD FAVOURED" if pd and not rm else "NOT DIAGNOSTIC")
    P(f"  [{foot}] {calls[foot]}")
overall = calls["canonical"] if calls["canonical"] == calls["alt"] else "SPLIT"
P(f"VERDICT: {overall}")
if MUTATE:
    P("MUTATE reading: RM (a0 x10) must NOT be consistent (G-Y included).")
else:
    P("\n--- variants (reported), canonical 1.5 h_R")
    for name, kw in (("h_z x 0.75", dict(hz_scale=0.75)), ("no gas", dict(gas=False))):
        for mdl in ("RM", "PD"):
            summarize({u: fit_and_predict(g, 1.5, "canonical", mdl, **kw) for u, g in gal.items()}, f"{name:11s} {mdl}")
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass   [{time.time() - T0:.0f} s]")
json.dump(dict(verdict=overall, calls=calls, summary=S, calibration=cal, per_galaxy={k: {str(u): v for u, v in d.items()} for k, d in res.items()},
               checks=CHECKS), open(os.path.join(HERE, f"cfg577_results{TAG}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg577_diskmass_grid{TAG}.out"), "w").write("\n".join(OUT) + "\n")
