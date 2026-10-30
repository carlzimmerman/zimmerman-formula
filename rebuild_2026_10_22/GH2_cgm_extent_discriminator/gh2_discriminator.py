#!/usr/bin/env python3
"""GH2_cgm_extent_discriminator: lensing chi2(route E fair share) - chi2(isolated law), both with identical baryons, vs
the hot-CGM cut k (Zhang+24 MW-mass profile to k R_vir; k=0 = F2's 0.5 M* hot gas), on KiDS isolated lenses (X53 harness,
via X78's code) and GAMA G09 centrals (GH1's committed stacks), bins 3-4. Frozen criteria: FROZEN_CRITERIA.md (48468b5bd8).
kappa = 1/2 FITTED; c_f EXTERNAL; footings never pooled; not theory closed; nothing here says the data favour the framework.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gh2_discriminator.py
"""
import os, sys, io, json, math, time, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
OUT, CHK = [], {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(k, ok, v): CHK[k] = bool(ok); P(f"  {k}: {'PASS' if ok else 'FAIL'} ({v})")

# ------------------------------------------------------------ X78 machinery (definitions + its own identities), read-only
S78 = os.path.join(REB, "X78_cgm_closure_regrade", "x78_regrade.py"); s78 = open(S78).read()
s78 = s78[:s78.index("# ------------------------------------------------------------ satellites")]
G = {"__file__": S78, "__name__": "x78_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s78, S78, "exec"), G)
lens_models, lens_grade, mass_route_e, mass_law, AQ, RG_ALL = (G[k] for k in ("lens_models", "lens_grade", "mass_route_e", "mass_law", "AQ", "RG_ALL"))
P(f"GH2  criteria 48468b5bd8; X78 machinery loaded (its K1/K2/K3: {G['CHK']}) [{time.time() - T0:.0f} s]")
KG = [0, 1, 1.5, 2, 3, 5]
def hot_of(k): return None if k == 0 else (1.84, 0.43, k)

# ------------------------------------------------------------ G09 centrals: GH1's committed stacks
E = np.load(os.path.join(os.path.dirname(REPO), "_external_data", "gh1_work", "gh1_esd.npz"))
GH1 = json.load(open(os.path.join(REB, "GH1_matched_lensing_satellites", "gh1_results.json")))
RB = np.geomspace(30, 3000, 13); RC = np.sqrt(RB[1:] * RB[:-1]); NB = len(RC); NPATCH = 30
hbin, lmH, pg, pr = E["hbin"], E["lm"], E["pg"], E["pr"]
def esd(sl, sr):
    return np.array([E["WG"][sl & (hbin == b)].sum(0) / E["WW"][sl & (hbin == b)].sum(0) - E["rWG"][sr].sum(0) / E["rWW"][sr].sum(0) for b in range(4)])
DS = esd(np.ones(len(hbin), bool), np.ones(len(pr), bool))
JK = np.array([esd(pg != p, pr != p) for p in range(NPATCH)])
GR = (RC >= 50) & (RC <= 300); B34 = [2, 3]
v = JK[:, B34][:, :, GR].reshape(NPATCH, -1); C = (NPATCH - 1) / NPATCH * (v - v.mean(0)).T @ (v - v.mean(0))
npts = v.shape[1]; Ci = np.linalg.inv(C) * (NPATCH - npts - 2) / (NPATCH - 1)
d34 = np.concatenate([DS[b, GR] for b in B34])
check("K3_G09_data_equals_GH1", float(np.max(np.abs(d34 - np.concatenate([np.array(GH1["DS"])[b][GR] for b in B34])))) == 0.0, "bins 3-4, 50-300 kpc")
LGRID = np.round(np.arange(8.5, 11.31, 0.05), 2); Rpc = RC * 1e3


def g09_chi2(foot, k):
    hot = hot_of(k); tH = np.empty((len(LGRID), NB)); tL = np.empty((len(LGRID), NB))
    for a, l in enumerate(LGRID):
        tH[a] = AQ.delta_sigma(Rpc, RG_ALL, mass_route_e(foot, l, 0.1797, hot)[0], "const")
        tL[a] = AQ.delta_sigma(Rpc, RG_ALL, mass_law(foot, l, hot), "const")
    def stk(t, b):
        m = hbin == b; W = E["WW"][m]; vv = np.array([np.interp(lmH[m], LGRID, t[:, j]) for j in range(NB)])   # (NB, hosts)
        return (vv * W.T).sum(1) / W.sum(0)
    out = {}
    for lab, t in (("H", tH), ("L", tL)):
        r = d34 - np.concatenate([stk(t, b)[GR] for b in B34]); out[lab] = float(r @ Ci @ r)
    return out


# ------------------------------------------------------------ K1 / K2 (KiDS identities) and MUTATE
X76L = json.load(open(os.path.join(REB, "X76_galaxy_fair_share_halos", "x76_lensing_results_fair.json")))
X53L = json.load(open(os.path.join(REB, "X53_outer_lensing_law_vs_halos", "x53_outer_lensing_results.json")))
X78R = json.load(open(os.path.join(REB, "X78_cgm_closure_regrade", "x78_regrade_results.json")))
RES = {"criteria": "48468b5bd8", "k_grid": KG, "footings": {}, "checks": CHK}
for foot in ("canonical", "alt"):
    rows = {}
    for k in KG:
        mH, mL = lens_models(foot, hot_of(k)); lg = lens_grade(mH, mL)
        kid = dict(H=lg["H2H_b34"], L=lg["L2H_b34"], d=lg["d_b34"], H_all4=sum(lg["per_bin_H"]), L_all4=sum(lg["per_bin_L"]))
        g9 = g09_chi2(foot, k); g9["d"] = g9["H"] - g9["L"]
        cls = lambda d: "LAW" if d >= 9 else ("HALOS" if d <= -9 else "NOT DIAGNOSTIC")
        rows[k] = dict(kids=kid, g09=g9, cls_kids=cls(kid["d"]), cls_g09=cls(g9["d"]))
        P(f"  [{foot} k={k:<3}] KiDS b3-4: H {kid['H']:.1f} L {kid['L']:.1f} d {kid['d']:+.1f} ({rows[k]['cls_kids']}) | G09 b3-4 (10 pts): H {g9['H']:.1f} L {g9['L']:.1f} d {g9['d']:+.1f} ({rows[k]['cls_g09']})  [{time.time() - T0:.0f} s]")
        if foot == "canonical" and k == 0:
            h76 = sum(X76L["footings"][foot]["all"]["H2H"]["per_bin"][2:]); l53 = sum(X53L["footings"][foot]["all"]["L2H"]["per_bin"][2:])
            check("K1_k0_reproduces_X76_X53", abs(kid["H"] / h76 - 1) < 1e-6 and abs(kid["L"] / l53 - 1) < 1e-6, f"H {kid['H']:.3f} vs X76 {h76:.3f}; L {kid['L']:.3f} vs X53 {l53:.3f}")
        if k == 3:
            x = X78R["footings"][foot]["central_k3"]["lens"]
            check(f"K2_k3_reproduces_X78_{foot}", abs(kid["H"] / x["H2H_b34"] - 1) < 1e-6 and abs(kid["L"] / x["L2H_b34"] - 1) < 1e-6, f"H {kid['H']:.2f}/{x['H2H_b34']:.2f}, L {kid['L']:.2f}/{x['L2H_b34']:.2f}")
    def kstar(key):
        ds = [rows[k][key]["d"] for k in KG]
        for i in range(len(KG) - 1):
            if ds[i] == 0: return float(KG[i])
            if ds[i] * ds[i + 1] < 0: return float(KG[i] + (KG[i + 1] - KG[i]) * ds[i] / (ds[i] - ds[i + 1]))
        return None
    ks = {"kids": kstar("kids"), "g09": kstar("g09")}
    flip = {s: rows[3][f"cls_{s}"] != rows[0][f"cls_{s}"] or rows[3][f"cls_{s}"] != rows[1][f"cls_{s}"] for s in ("kids", "g09")}
    step = lambda x: (None if x is None else int(np.searchsorted(KG, x)))
    agree = ks["kids"] is not None and ks["g09"] is not None and abs(step(ks["kids"]) - step(ks["g09"])) <= 1
    disc = "CGM EXTENT DECIDES" if (all(flip.values()) and agree) else "NOT A CLEAN DISCRIMINATOR: " + ", ".join(
        ([f"no class flip on {s}" for s, f in flip.items() if not f]) + ([] if agree else [f"k* disagree {ks}"]))
    RES["footings"][foot] = dict(rows={str(k): v for k, v in rows.items()}, primary_k1={"kids": rows[1]["cls_kids"], "g09": rows[1]["cls_g09"]},
                                 kstar=ks, flip=flip, discriminator=disc)
    P(f"=== [{foot}] PRIMARY k=1 (measured gas only): KiDS {rows[1]['cls_kids']}, G09 {rows[1]['cls_g09']}; k* KiDS {ks['kids']}, G09 {ks['g09']} -> {disc}")
# MUTATE: zeroing all hot gas lowers both models' DS at 100 kpc (test lens 10.8, canonical)
R1 = np.array([1e5])
def ds_at(fn): return float(AQ.delta_sigma(R1, RG_ALL, fn, "const")[0])
h0, h_ = ds_at(mass_route_e("canonical", 10.8, 0.1797, None)[0]), ds_at(mass_route_e("canonical", 10.8, 0.1797, (0.0, 0.43, 1))[0])
l0, l_ = ds_at(mass_law("canonical", 10.8, None)), ds_at(mass_law("canonical", 10.8, (0.0, 0.43, 1)))
check("MUTATE_no_hot_gas_lowers_both", h_ < h0 and l_ < l0, f"H {h0:.2f} -> {h_:.2f}; L {l0:.2f} -> {l_:.2f}")
n = sum(CHK.values()); P(f"\nchecks {n}/{len(CHK)}; runtime {time.time() - T0:.0f} s")
json.dump(RES, open(os.path.join(HERE, "gh2_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "gh2.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n == len(CHK) else 1)
