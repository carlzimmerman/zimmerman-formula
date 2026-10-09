"""CFG576: DiskMass sigma_z, round rule (RM) vs phantom disc (PD). Criteria: FROZEN_CRITERIA.md (e1c6d8abe).

Inputs: DMS VI (arXiv:1307.8130) tables 1, 5, 6 and DMS VII (arXiv:1308.0336) h_R/h_z and mass tables, copied
verbatim into data/. MUTATE: CFG576_MUTATE=1 multiplies a0 by 10 in RM only; outputs carry the _MUTATE tag.
"""
import os, re, json, math
import numpy as np
from scipy.special import i0, i1, k0, k1
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
MUTATE = os.environ.get("CFG576_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


G = 4.30091e-6                         # kpc (km/s)^2 / Msun
A0 = {"canonical": 9.36e-11 * 3.0857e13, "alt": 1.13e-10 * 3.0857e13}   # (km/s)^2 / kpc
K_VERT, MSUN_K = 1.5, 3.28
AS2KPC = math.pi / 180 / 3600 * 1000.0   # kpc per arcsec per Mpc


def nu(y):
    y = np.maximum(y, 1e-30); return 1.0 / (-np.expm1(-np.sqrt(y)))


def rows(fn):
    out = []
    for line in open(os.path.join(D, fn)):
        line = line.split("%")[0]
        if re.match(r"^\s*\d+\s*&", line):
            out.append(line)
    return out


def nums(s):
    s = s.replace("$-$", "-").replace("\\phantom{1}", "")
    return [float(x) for x in re.findall(r"-?\d+\.?\d*", s)]


gal = {}
for r in rows("DMS_VI_tab1.tex"):
    c = r.split("&"); u = int(c[0])
    gal[u] = dict(D=nums(c[3])[0], hR_as=nums(c[10])[0], mu0=nums(c[12])[0], BD=nums(c[14])[0])
for r in rows("DMS_VI_tab5.tex"):
    c = r.split("&"); u = int(c[0])
    gal[u].update(iTF=nums(c[7])[0], Varot=nums(c[8])[0], rs_as=nums(c[9])[0])
for r in rows("DMS_VI_tab6.tex"):
    c = r.split("&"); u = int(c[0])
    gal[u].update(sz0=nums(c[3])[0], hsz_as=nums(c[4])[0])
for r in rows("DMS_VII_tab_hRhz.tex"):
    v = nums(r)                                   # u hR ehR hz ehz u hR ehR hz ehz
    for k in (0, 5):
        gal[int(v[k])].update(hR=v[k + 1], hz=v[k + 3])
for r in rows("DMS_VII_tabMasses.tex"):
    c = r.split("&"); u = int(c[0])
    gal[u].update(lMatom=nums(c[3])[0], lMmol=nums(c[4])[0])


def vexp2(R, M, h):
    """thin exponential disc circular speed^2 (Freeman 1970)."""
    if M <= 0: return 0.0
    S0 = M / (2 * math.pi * h * h); y = R / (2 * h)
    return 4 * math.pi * G * S0 * h * y * y * (i0(y) * k0(y) - i1(y) * k1(y))


def sexp(R, M, h):
    return M / (2 * math.pi * h * h) * math.exp(-R / h)


def galaxy_terms(g, R, hz_scale=1.0, gas=True):
    kpc_as = g["D"] * AS2KPC
    hR = g["hR"]
    I0 = 10 ** (0.4 * (MSUN_K + 21.572 - g["mu0"])) * 1e6        # Lsun/kpc^2
    Ld = 2 * math.pi * I0 * hR * hR
    Ma = 10 ** g["lMatom"] if gas else 0.0
    Mm = 10 ** g["lMmol"] if gas else 0.0
    vrot = g["Varot"] / math.sin(math.radians(g["iTF"])) * math.tanh(R / (g["rs_as"] * kpc_as))
    smeas = g["sz0"] * math.exp(-R / (g["hsz_as"] * kpc_as))
    return dict(hR=hR, hz=g["hz"] * hz_scale, I0=I0, Ld=Ld, Ma=Ma, Mm=Mm, vrot=vrot, smeas=smeas)


def gbar(t, R, Y):
    v2 = vexp2(R, Y * t["Ld"], t["hR"]) + vexp2(R, t["Ma"], 2 * t["hR"]) + vexp2(R, t["Mm"], t["hR"]) \
        + G * Y * t["Ld"] * gal_BD / R
    return v2 / R


def predict(g, R, foot, k=K_VERT, hz_scale=1.0, gas=True, a0mult_rm=1.0, newton=False):
    global gal_BD
    gal_BD = g["BD"]
    t = galaxy_terms(g, R, hz_scale, gas)
    gobs = t["vrot"] ** 2 / R
    out = {}
    for model in (["N"] if newton else ["RM", "PD"]):
        a0 = A0[foot] * (a0mult_rm if model == "RM" else 1.0)
        f = (lambda Y: gbar(t, R, Y) - gobs) if newton else (lambda Y: nu(gbar(t, R, Y) / a0) * gbar(t, R, Y) - gobs)
        try:
            Y = brentq(f, 0.02, 5.0)
        except ValueError:
            out[model] = None; continue
        gb = gbar(t, R, Y)
        Sig = Y * t["I0"] * math.exp(-R / t["hR"]) + sexp(R, t["Ma"], 2 * t["hR"]) + sexp(R, t["Mm"], t["hR"])
        KN = 2 * math.pi * G * Sig * (1 - math.exp(-1))
        if model == "PD":
            B = float(nu(math.hypot(gb, KN) / a0))
        elif model == "RM":
            gmod = float(nu(gb / a0)) * gb
            B = 1 + (gmod - gb) * t["hz"] / R / KN
        else:
            B = 1.0
        sp = math.sqrt(math.pi * G * k * t["hz"] * Sig * B)
        out[model] = dict(Y=Y, B=B, r=sp / t["smeas"])
    return out


def median_ci(x, seed=576):
    x = np.array([v for v in x if v is not None and np.isfinite(v)])
    rng = np.random.default_rng(seed)
    bs = np.median(rng.choice(x, size=(2000, len(x))), axis=1)
    return float(np.median(x)), float(np.percentile(bs, 16)), float(np.percentile(bs, 84)), len(x)


P("=" * 100)
P(f"CFG576  DiskMass sigma_z: RM vs PD  {'*** MUTATE: a0 x10 in RM ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)
P(f"galaxies parsed: {len(gal)}; complete: {sum(1 for g in gal.values() if len(g) >= 13)}")
check(len(gal) == 30 and all(len(g) >= 13 for g in gal.values()), "C0 all 30 galaxies have every input")

res = {}
for foot in ("canonical", "alt"):
    res[foot] = {}
    for rad in (1.5, 2.2):
        per = {u: predict(g, rad * g["hR"], foot, a0mult_rm=(10.0 if MUTATE else 1.0)) for u, g in gal.items()}
        res[foot][rad] = per
        for m in ("RM", "PD"):
            rv = [p[m]["r"] for p in per.values() if p[m]]
            med, lo, hi, n = median_ci(rv)
            Ym = np.median([p[m]["Y"] for p in per.values() if p[m]]); Bm = np.median([p[m]["B"] for p in per.values() if p[m]])
            P(f"  [{foot:9s}] R = {rad} h_R  {m}: median r = {med:.3f} [{lo:.3f}, {hi:.3f}]  n = {n}  median Y_K = {Ym:.3f}  median B = {Bm:.3f}")
        if rad == 1.5:
            nY = min(sum(1 for p in per.values() if p[m]) for m in ("RM", "PD"))
            check(nY >= 20, f"C1 [{foot}] valid Y_K for >= 20 galaxies (min over models {nY})")

# C2 Newtonian reference
for foot in ("canonical",):
    pn = [predict(g, 1.5 * g["hR"], foot, newton=True)["N"] for g in gal.values()]
    med, lo, hi, n = median_ci([p["r"] for p in pn if p])
    P(f"  C2 Newtonian reference (Y_K from the RC, B = 1): median r = {med:.3f} [{lo:.3f}, {hi:.3f}] n = {n}; median Y_K = {np.median([p['Y'] for p in pn if p]):.3f}")

P("\n--- verdict (primary R = 1.5 h_R)")
calls = {}
pdalt = median_ci([p["PD"]["r"] for p in res["alt"][1.5].values() if p["PD"]])[0]
gcal = 1.15 <= pdalt <= 1.45
check(gcal, f"G-cal PD median r on the alt footing {pdalt:.3f} reproduces Angus+15 (~1.3) within [1.15, 1.45]")
for foot in ("canonical", "alt"):
    med = {m: median_ci([p[m]["r"] for p in res[foot][1.5].values() if p[m]])[0] for m in ("RM", "PD")}
    cons = {m: 0.85 <= med[m] <= 1.15 for m in med}
    call = ("INCONCLUSIVE" if not gcal else "ROUND FAVOURED" if cons["RM"] and not cons["PD"] else
            "PD FAVOURED" if cons["PD"] and not cons["RM"] else "NOT DIAGNOSTIC")
    calls[foot] = call
    P(f"  [{foot}] RM {med['RM']:.3f} ({'consistent' if cons['RM'] else 'not'}), PD {med['PD']:.3f} ({'consistent' if cons['PD'] else 'not'}) -> {call}")
overall = calls["canonical"] if calls["canonical"] == calls["alt"] else "SPLIT"
P(f"VERDICT: {overall}")
if MUTATE:
    P("MUTATE reading: RM (a0 x10) must NOT be consistent.")

P("\n--- variants (reported, not gates), R = 1.5 h_R, canonical")
for name, kw in (("k = 2 (sech^2)", dict(k=2.0)), ("h_z x 0.75", dict(hz_scale=0.75)), ("no gas", dict(gas=False))):
    per = {u: predict(g, 1.5 * g["hR"], "canonical", **kw) for u, g in gal.items()}
    s = "  ".join(f"{m} {median_ci([p[m]['r'] for p in per.values() if p[m]])[0]:.3f}" for m in ("RM", "PD"))
    P(f"  {name:16s} {s}")

P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(verdict=overall, calls=calls,
               per_galaxy={f: {str(r): {str(u): v for u, v in res[f][r].items()} for r in res[f]} for f in res},
               checks=CHECKS), open(os.path.join(HERE, f"cfg576_results{TAG}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg576_diskmass{TAG}.out"), "w").write("\n".join(OUT) + "\n")
