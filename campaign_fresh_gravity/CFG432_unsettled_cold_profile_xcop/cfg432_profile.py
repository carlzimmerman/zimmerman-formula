#!/usr/bin/env python3
"""CFG432: is the unsettled cold mass M_u = M_HSE/(1-b) - M_law in X-COP clusters shaped like the gas, or like a fixed-c NFW?
Criteria: FROZEN_CRITERIA.md (committed alone first). Run: python3 cfg432_profile.py [--mutate]"""
import os, sys, json, glob
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "xcop")
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
G, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
BIAS = (0.0, 0.3)
T = 0.15
NGRID = 16
RELAXED = ("A1795", "A2029", "A2142")
OUT = []
def P(s=""):
    print(s); OUT.append(str(s))

def nu(y):
    return 1.0 / (-np.expm1(-np.sqrt(y)))

def loginterp(x, xp, fp):
    return np.exp(np.interp(np.log(x), np.log(xp), np.log(fp), left=np.nan, right=np.nan))

R200 = json.load(open(os.path.join(DATA, "xcop_r500_ettori2019.json")))
cl = []
for d in sorted(glob.glob(os.path.join(DATA, "*", ""))):
    n = os.path.basename(os.path.dirname(d))
    with fits.open(os.path.join(d, n + "_hydro_mass.fits")) as f:
        rh = np.array(f[1].data["RADIUS"], float); mh = np.array(f[1].data["M_FORW"], float)
        mnfw_x = np.array(f[1].data["M_NFW"], float)
    with fits.open(os.path.join(d, n + "_fgas_profile.fits")) as f:
        r500 = float(f[1].header["R500"])
        rg = np.array(f[1].data["RADIUS"], float) * r500; mg = np.array(f[1].data["MGAS"], float)
    st = os.path.join(d, n + "_mstar.fits")
    rs = ms = None
    if os.path.exists(st):
        with fits.open(st) as f:
            assert f[2].columns["RADIUS"].unit == "kpc"
            rs = np.array(f[2].data["RADIUS"], float); ms = np.array(f[2].data["MSTAR"], float)
    r = np.logspace(np.log10(0.1 * r500), np.log10(r500), NGRID)
    c = dict(name=n, R500=r500, R200=R200[n]["R200"] * 1000.0, r=r,
             mh=loginterp(r, rh, mh), mg=loginterp(r, rg, mg), mnfw_xcop=loginterp(r, rh, mnfw_x),
             ms=(loginterp(r, rs, ms) if rs is not None else None))
    cl.append(c)
names = [c["name"] for c in cl]
N = len(cl)

# stellar import (median ratio over clusters with files, at the same x = r/R500 grid point)
ratio = np.nanmedian(np.array([c["ms"] / c["mg"] for c in cl if c["ms"] is not None]), axis=0)
def stars(c, conv="median"):
    if c["ms"] is not None: return c["ms"]
    return c["mg"] * (ratio if conv == "median" else 0.10)

# C2 data identity
c2 = all(np.all(np.isfinite(v) & (v > 0)) for c in cl for v in (c["mh"], c["mg"], stars(c), c["mnfw_xcop"]))
P(f"CFG432  N clusters = {N}; grid {NGRID} log radii 0.1-1.0 R500 (own R500); T = {T}")
P(f"C2 data identity (all profiles positive/finite on grid): {'PASS' if c2 else 'FAIL'}")

def m_nfw(c, conc):
    x = c["r"] / c["R200"]; cx = conc * x
    return np.log1p(cx) - cx / (1 + cx)

def slope(r, q):
    ok = np.isfinite(q) & (q > 0)
    if ok.sum() < 6: return np.nan, int(ok.sum())
    return float(np.polyfit(np.log(r[ok]), np.log(q[ok]), 1)[0]), int(ok.sum())

def boot(s, seed=432):
    s = np.asarray(s); s = s[np.isfinite(s)]; rng = np.random.default_rng(seed)
    med = float(np.median(s))
    sd = float(np.std([np.median(s[rng.integers(0, len(s), len(s))]) for _ in range(2000)]))
    return med, sd, len(s)

def zval(m, sd):
    if sd == 0: return 0.0 if abs(m) < 1e-12 else float("inf")
    return abs(m) / sd

def shape_call(s_list, need=8):
    m, sd, n = boot(s_list)
    z = zval(m, sd)
    nclose = int(np.sum(np.abs(np.asarray(s_list)[np.isfinite(s_list)]) <= 2 * T))
    if abs(m) <= T and z <= 2 and nclose >= need: call = "CONSISTENT"
    elif abs(m) > T and z > 3: call = "EXCLUDED"
    else: call = "INCONCLUSIVE"
    return dict(median=m, boot_sd=sd, z=z, n=n, n_within_2T=nclose, call=call)

def cell_verdict(g, f, underpop):
    if underpop: return "UNDERPOPULATED"
    if g == "CONSISTENT" and f == "CONSISTENT": return "BOTH / NON-DISCRIMINATING"
    if g == "CONSISTENT" and f == "EXCLUDED": return "GAS-SHAPED"
    if f == "CONSISTENT" and g == "EXCLUDED": return "NFW-SHAPED"
    if g == "EXCLUDED" and f == "EXCLUDED": return "NEITHER"
    return "INCONCLUSIVE"

def mlaw_of(c, a0, conv="median"):
    mb = c["mg"] + stars(c, conv)
    gb = G * mb * MSUN / (c["r"] * KPC) ** 2
    return mb, nu(gb / a0) * mb, gb

# C1 discrimination
disc = np.median([abs(slope(c["r"], m_nfw(c, 4.0) / c["mg"])[0]) for c in cl])
c1 = disc >= 2 * T
P(f"C1 discrimination: median |dln(m_NFW,c=4 / M_gas)/dln r| = {disc:.3f} (need >= {2*T:.2f}) -> {'PASS' if c1 else 'FAIL'}")
# C3 law identity
c3 = True
for c in cl:
    for a0 in A0.values():
        mb, ml, gb = mlaw_of(c, a0)
        c3 &= bool(np.all(np.abs(ml / mb - nu(gb / a0)) < 1e-12) and np.all(nu(gb / a0) >= 1))
P(f"C3 law identity: {'PASS' if c3 else 'FAIL'}")

def run_cell(a0, b, conc=4.0, conv="median", idx=None, mh_override=None):
    idx = list(range(N)) if idx is None else list(idx)
    sg, sn, sx, rows, npos, ntot = [], [], [], [], 0, 0
    dropped = 0
    for i in idx:
        c = cl[i]
        mb, ml, _ = mlaw_of(c, a0, conv)
        mh = c["mh"] if mh_override is None else mh_override[i]
        mu = mh / (1 - b) - ml
        npos += int(np.sum(mu > 0)); ntot += len(mu)
        s_g, nv = slope(c["r"], mu / c["mg"])
        s_n, _ = slope(c["r"], mu / m_nfw(c, conc))
        s_x, _ = slope(c["r"], mu / np.clip(c["mnfw_xcop"] - mb, 1e-30, None) * (c["mnfw_xcop"] > mb))
        if not np.isfinite(s_g): dropped += 1
        sg.append(s_g); sn.append(s_n); sx.append(s_x)
        q = mu / c["mg"]
        rows.append(dict(name=c["name"], s_gas=s_g, s_nfw=s_n, n_valid=nv,
                         Q_01=float(q[0]), Q_05=float(np.interp(np.log(0.5), np.log(c["r"] / c["R500"]), q)), Q_10=float(q[-1]),
                         Mu_over_Mph_R500=float(mu[-1] / (ml[-1] - mb[-1]))))
    nidx = len(list(idx)); need = 8 if nidx == N else int(np.ceil(2 * nidx / 3))  # subsets (reported only): 2/3 of n
    g = shape_call(sg, need); f = shape_call(sn, need)
    underpop = dropped > (3 if nidx == N else nidx // 4)
    return dict(gas=g, nfw=f, xcop_nfw_minus_baryons=boot(sx), dropped=dropped, frac_mu_pos=npos / ntot,
                verdict=cell_verdict(g["call"], f["call"], underpop), rows=rows)

def line(tag, res):
    g, f = res["gas"], res["nfw"]
    return (f"{tag}: gas S {g['median']:+.3f} +- {g['boot_sd']:.3f} (z {g['z']:.1f}, {g['n_within_2T']}/{g['n']} |s|<=0.30) {g['call']:12s} | "
            f"NFW S {f['median']:+.3f} +- {f['boot_sd']:.3f} (z {f['z']:.1f}, {f['n_within_2T']}/{f['n']}) {f['call']:12s} | M_u>0 {res['frac_mu_pos']:.2f}, dropped {res['dropped']} -> {res['verdict']}")

results = {"criteria": "FROZEN_CRITERIA.md", "T": T, "controls": dict(C1=bool(c1), C1_value=float(disc), C2=bool(c2), C3=bool(c3))}
rc = 0
if not MUT:
    P(); P("PRIMARY CELLS (stars: median-ratio import for 5; c200 = 4)")
    verdicts, gascalls = {}, {}
    for foot, a0 in A0.items():
        for b in BIAS:
            res = run_cell(a0, b)
            key = f"{foot}|b{b}"
            results[key] = res; verdicts[key] = res["verdict"] if c1 else "NON-DISCRIMINATING (C1 fail)"; gascalls[key] = res["gas"]["call"]
            P(line(f"{foot:9s} b={b}", res))
    vs = set(verdicts.values())
    headline = vs.pop() if len(vs) == 1 else "DEPENDS ON b / FOOTING"
    gc = set(gascalls.values())
    hyp = ("SUPPORTED" if set(verdicts.values()) == {"GAS-SHAPED"} else
           "CONTRADICTED" if gc == {"EXCLUDED"} else "NOT SETTLED")
    results["headline"] = headline; results["hypothesis_gas_tracking"] = hyp
    P(); P(f"HEADLINE: {headline}")
    P(f"Hypothesis 'unsettled cold mass tracks the gas': {hyp}")

    P(); P("PER CLUSTER (canonical): name | s_gas b=0 | s_nfw b=0 | s_gas b=0.3 | s_nfw b=0.3 | Q_gas at 0.1/0.5/1.0 R500 (b=0) | M_u/M_ph at R500 (b=0)")
    r0, r3 = results["canonical|b0.0"]["rows"], results["canonical|b0.3"]["rows"]
    for a, bb in zip(r0, r3):
        P(f"  {a['name']:8s} {a['s_gas']:+.3f} {a['s_nfw']:+.3f}   {bb['s_gas']:+.3f} {bb['s_nfw']:+.3f}   {a['Q_01']:6.2f} {a['Q_05']:6.2f} {a['Q_10']:6.2f}   {a['Mu_over_Mph_R500']:.2f}")

    P(); P("REPORTED, NOT DECISIVE")
    sens = {}
    for foot, a0 in A0.items():
        for b in BIAS:
            for lab, kw in (("stars=0.10Mgas", dict(conv="fixed")), ("c200=3", dict(conc=3.0)), ("c200=5", dict(conc=5.0)),
                            ("relaxed3", dict(idx=[names.index(n) for n in RELAXED]))):
                res = run_cell(a0, b, **kw)
                sens[f"{foot}|b{b}|{lab}"] = {k: res[k] for k in ("gas", "nfw", "verdict", "dropped")}
                P(line(f"{foot:9s} b={b} {lab:15s}", res))
    results["sensitivity"] = sens
    P("X-COP's own NFW-minus-baryons (fitted to the same data, not independent): median slope of ln(M_u/(M_NFW,xcop - M_b))")
    for foot in A0:
        for b in BIAS:
            m, sd, n = results[f"{foot}|b{b}"]["xcop_nfw_minus_baryons"]
            P(f"  {foot:9s} b={b}: {m:+.3f} +- {sd:.3f} (N {n})")
    # reference: logarithmic slopes of the profiles themselves
    def dln(arrs): return float(np.median([slope(c["r"], a)[0] for c, a in zip(cl, arrs)]))
    mu0 = [c["mh"] - mlaw_of(c, A0["canonical"])[1] for c in cl]
    P(f"Reference d ln M/d ln r over 0.1-1 R500 (canonical, b=0, medians): M_u {dln(mu0):.2f}; M_gas {dln([c['mg'] for c in cl]):.2f}; "
      f"m_NFW(c=4) {dln([m_nfw(c,4.0) for c in cl]):.2f}; M_HSE {dln([c['mh'] for c in cl]):.2f}; "
      f"M_ph {dln([mlaw_of(c,A0['canonical'])[1]-mlaw_of(c,A0['canonical'])[0] for c in cl]):.2f}")
    if not (c1 and c2 and c3): rc = 1
else:
    a0 = A0["canonical"]
    # M-A planted gas shape
    mhA = []
    for c in cl:
        mb, ml, _ = mlaw_of(c, a0)
        mu = c["mh"] - ml
        q = float(np.interp(np.log(0.5), np.log(c["r"] / c["R500"]), mu / c["mg"]))
        q = q if q > 0 else 0.5
        mhA.append(ml + q * c["mg"])
    resA = run_cell(a0, 0.0, mh_override=mhA)
    # M-B shuffled radii
    rng = np.random.default_rng(432)
    mhB = [c["mh"][rng.permutation(NGRID)] for c in cl]
    resB = run_cell(a0, 0.0, mh_override=mhB)
    P(line("M-A planted gas  canonical b=0", resA))
    P(line("M-B shuffled r   canonical b=0", resB))
    okA = resA["verdict"] == "GAS-SHAPED"
    okB = resB["verdict"] not in ("GAS-SHAPED", "NFW-SHAPED")
    P(f"M-A must be GAS-SHAPED: {'OK' if okA else 'NOT MET'}; M-B must not be GAS-/NFW-SHAPED: {'OK' if okB else 'NOT MET'}")
    rc = 1 if (okA and okB) else 0
    P(f"MUTATE: {'detected (both controls behave)' if rc else 'NOT detected -> main verdict rests on an unvalidated test'} (rc {rc})")
    results["M_A"] = resA; results["M_B"] = resB; results["mutate_detected"] = bool(rc)

json.dump(results, open(os.path.join(HERE, f"cfg432_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg432{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(rc)
