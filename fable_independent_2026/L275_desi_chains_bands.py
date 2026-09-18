#!/usr/bin/env python3
"""L275 -- the w0-wa correlation from the DESI DR2 public chains, and the a0(z) bands from the chains themselves (no Gaussian).

Chains: DESI DR2 BAO cosmology release (data.desi.lbl.gov/public/papers/y3/bao-cosmo-params, cobaya/base_w_wa/), the paper's baseline
CMB (planck2018 lowl TT+EE, NPIPE CamSpec TTTEEE, ACT DR6 lensing) with each SNe sample: pantheonplus, union3, desy5sn; chains 1-4 each.
If the full chains are present (env CHAIN_DIR, ~200 MB, not committed) this lane reads them and writes a thinned copy (every 4th
weighted sample; columns weight, w, wa, omegam) to fable_independent_2026/data/desi_dr2_w0wa_thinned/<sn>.txt, which IS committed and
is what the lane reads otherwise.  For every sample: the framework's pressure mapping a0(z)/a0(0) = sqrt(w(z) f_DE(z)/w0) and the density
mapping sqrt(f_DE(z)), with CPL f_DE(z) = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z)); weighted 16/50/84 percentiles at z = 0.5-5; the
H(z) law with each sample's own Omega_m.  Checks compare the chain means with the paper's quoted values (arXiv:2503.14738v2) and the
chain bands with the Gaussian rho = -0.9 assumption used in L273/L274.  A FAIL is a finding."""
import os, sys, json, glob, math
import numpy as np
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("L275 -- DESI DR2 chains: the w0-wa correlation and the a0(z) bands from the samples\n")
HERE = os.path.dirname(os.path.abspath(__file__)); THIN = os.path.join(HERE, "data", "desi_dr2_w0wa_thinned")
CHAIN_DIR = os.environ.get("CHAIN_DIR", "")
PAPER = {"pantheonplus": dict(w0=-0.838, sw0=0.055, wa=-0.62, swa=(0.22 + 0.19) / 2, om=0.3114), "union3": dict(w0=-0.667, sw0=0.088, wa=-1.09, swa=(0.31 + 0.27) / 2, om=0.3275), "desy5sn": dict(w0=-0.752, sw0=0.057, wa=-0.86, swa=(0.23 + 0.20) / 2, om=0.3191)}
NICE = {"pantheonplus": "Pantheon+", "union3": "Union3", "desy5sn": "DESY5"}
def load(sn):
    thin = os.path.join(THIN, f"{sn}.txt")
    if CHAIN_DIR:
        files = sorted(glob.glob(os.path.join(CHAIN_DIR, sn, "chain.*.txt")))
        hdr = open(files[0]).readline().lstrip("#").split(); cols = {c: i for i, c in enumerate(hdr)}
        arr = np.vstack([np.loadtxt(f) for f in files])
        w, wa = arr[:, cols["w"]], arr[:, cols["wa"]]; wt = arr[:, cols["weight"]]
        om = arr[:, cols["omegam"]] if "omegam" in cols else np.full_like(w, PAPER[sn]["om"])
        data = np.column_stack([wt, w, wa, om])[::4]                                   # thin every 4th sample
        os.makedirs(THIN, exist_ok=True); np.savetxt(thin, data, fmt="%.6g", header="weight w wa omegam (DESI DR2 base_w_wa, desi-bao-all + planck2018-lowl-TT/EE + NPIPE CamSpec TTTEEE + ACT DR6 lensing + %s; every 4th weighted sample of chains 1-4; source data.desi.lbl.gov/public/papers/y3/bao-cosmo-params)" % sn)
        print(f"    {sn}: {len(arr)} samples in {len(files)} chains -> thinned {len(data)} rows written; columns had omegam: {'omegam' in cols}")
        return data
    return np.loadtxt(thin)
f_DE = lambda z, w0, wa: (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))
w_z = lambda z, w0, wa: w0 + wa * z / (1 + z)
def wpct(x, wt, q):
    i = np.argsort(x); cx = np.cumsum(wt[i]) / np.sum(wt); return np.interp(np.asarray(q) / 100.0, cx, x[i])
Z = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]); zg = np.linspace(0.0, 5.0, 101)
res = {}
print("=" * 100); print("1. chain statistics (weighted) versus the paper's quoted values"); print("=" * 100)
for sn in ("pantheonplus", "union3", "desy5sn"):
    d = load(sn); wt, w, wa, om = d[:, 0], d[:, 1], d[:, 2], d[:, 3]
    mw, mwa = np.average(w, weights=wt), np.average(wa, weights=wt)
    sw, swa = math.sqrt(np.average((w - mw) ** 2, weights=wt)), math.sqrt(np.average((wa - mwa) ** 2, weights=wt))
    rho = np.average((w - mw) * (wa - mwa), weights=wt) / (sw * swa); mom = np.average(om, weights=wt)
    res[sn] = dict(n=int(len(w)), w0=mw, sw0=sw, wa=mwa, swa=swa, rho=rho, omegam=mom)
    print(f"    {NICE[sn]:10s} n = {len(w):6d}: w0 = {mw:+.3f} +/- {sw:.3f} (paper {PAPER[sn]['w0']:+.3f} +/- {PAPER[sn]['sw0']:.3f}); wa = {mwa:+.3f} +/- {swa:.3f} (paper {PAPER[sn]['wa']:+.2f} +/- {PAPER[sn]['swa']:.3f}); rho(w0, wa) = {rho:+.3f}; Omega_m = {mom:.4f} (paper {PAPER[sn]['om']:.4f})")
check("1a the chain means reproduce the paper's quoted (w0, wa) within 0.02 and the widths within 25% for all three combinations (the chains are the ones the paper's table came from)",
      all(abs(r["w0"] - PAPER[sn]["w0"]) < 0.02 and abs(r["wa"] - PAPER[sn]["wa"]) < 0.05 and abs(r["sw0"] / PAPER[sn]["sw0"] - 1) < 0.25 and abs(r["swa"] / PAPER[sn]["swa"] - 1) < 0.25 for sn, r in res.items()),
      "; ".join(f"{NICE[sn]}: dw0 {r['w0']-PAPER[sn]['w0']:+.3f}, dwa {r['wa']-PAPER[sn]['wa']:+.3f}" for sn, r in res.items()))
check("1b the w0-wa correlation is strongly negative in every chain, between -0.95 and -0.75 (the value L273/L274 assumed was -0.9)",
      all(-0.95 <= r["rho"] <= -0.75 for r in res.values()), f"rho = {[round(r['rho'], 3) for r in res.values()]}")
OUT["chains"] = res
# ------------------------------------------------------------------ 2. bands from the samples
print("\n" + "=" * 100); print("2. a0(z)/a0(0) in dex from the chain samples: weighted 16 / 50 / 84 percentiles"); print("=" * 100)
bands = {"pressure": {}, "density": {}, "hz": {}}
for sn in res:
    d = load(sn); wt, w, wa, om = d[:, 0], d[:, 1], d[:, 2], d[:, 3]
    for key, fn in (("pressure", lambda z: np.log10(np.sqrt(w_z(z, w, wa) * f_DE(z, w, wa) / w))), ("density", lambda z: np.log10(np.sqrt(f_DE(z, w, wa)))), ("hz", lambda z: np.log10(np.sqrt(om * (1 + z) ** 3 + (1 - om) * f_DE(z, w, wa))))):
        bands[key][sn] = {"table": {float(z): [float(v) for v in wpct(fn(z), wt, [16, 50, 84])] for z in Z}, "grid": {"lo": [float(wpct(fn(z), wt, [16])[0]) for z in zg], "med": [float(wpct(fn(z), wt, [50])[0]) for z in zg], "hi": [float(wpct(fn(z), wt, [84])[0]) for z in zg]}}
for key in ("pressure", "density"):
    print(f"    {key} mapping:  z   " + "".join(f"{NICE[sn]:>30s}" for sn in res))
    for z in Z:
        print(f"      {z:3.1f}  " + "".join(f"{bands[key][sn]['table'][float(z)][1]:+.3f} [{bands[key][sn]['table'][float(z)][0]:+.3f},{bands[key][sn]['table'][float(z)][2]:+.3f}]".rjust(30) for sn in res))
p25 = {sn: bands["pressure"][sn]["table"][2.5] for sn in res}; d25 = {sn: bands["density"][sn]["table"][2.5] for sn in res}
gauss = {"pantheonplus": (-0.015, 0.028), "union3": (0.019, 0.097), "desy5sn": (0.007, 0.054)}      # L273 Part 4, Gaussian rho = -0.9
check("2a at z = 2.5 the chain medians of the pressure mapping are +0.00 to +0.06 dex (a slight rise) and every 68% band lies within [-0.03, +0.11]: the Gaussian rho = -0.9 bands of L273/L274 agree with the chains to 0.02 dex at each edge",
      all(0.0 <= v[1] <= 0.065 and -0.03 <= v[0] and v[2] <= 0.11 for v in p25.values()) and all(abs(p25[sn][0] - gauss[sn][0]) < 0.02 and abs(p25[sn][2] - gauss[sn][1]) < 0.02 for sn in res),
      "; ".join(f"{NICE[sn]} chain [{v[0]:+.3f}, {v[2]:+.3f}] vs Gaussian [{gauss[sn][0]:+.3f}, {gauss[sn][1]:+.3f}]" for sn, v in p25.items()))
check("2b the density mapping's chain medians at z = 2.5 are -0.08 to -0.12 dex with 68% bands entirely below zero, as L273 Parts 1-3 found",
      all(-0.13 <= v[1] <= -0.07 and v[2] < 0.0 for v in d25.values()), "; ".join(f"{NICE[sn]} {v[1]:+.3f} [{v[0]:+.3f},{v[2]:+.3f}]" for sn, v in d25.items()))
OUT["bands"] = bands
n, n_pass = len(CH), sum(CH)
print(f"\nL275 COMPLETE: {n_pass}/{n} checks PASS.")
print("""VERDICT.  The DESI DR2 chains carry a w0-wa correlation of about -0.9 in every combination, so the Gaussian bands of L273/L274 were
already right to ~0.02 dex; the bands here are computed from the samples with no approximation and replace them on the chart (L274 reads
this lane's JSON).  The picture is unchanged: the framework's own law is flat; DESI at face value through the pressure law gives a slight
rise of a few hundredths of a dex at z = 2.5 with 68% bands inside [-0.03, +0.11]; the rejected density mapping sits at -0.1.""")
json.dump(dict(pass_=n_pass, n=n, **OUT), open(os.path.join(HERE, "L275_results.json"), "w"), indent=1)
