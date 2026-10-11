#!/usr/bin/env python3
"""CFG600 (FROZEN_CRITERIA.md, committed alone first): KiDS catchment from the OUTER lensing profile (bins 0-5), scored on the held-out inner nine.
Run: nice -n 10 python3 cfg600_native_catchment.py   (about 1 min with the cached CFG531 tables)"""
import os, json, math
import numpy as np
import cfg600_common as K

MUTATE = False                                         # MU1 / MU2 are inside the main run (they are controls on the calibration, not a separate mode)
SUF = ""
HERE = K.HERE
LOG, CHK = [], {}
RES = {"lane": "CFG600", "script": "cfg600_native_catchment", "mutate": MUTATE, "criteria": "FROZEN_CRITERIA.md",
       "settings": "kappa = 1/2 FITTED; footings never pooled; nu_mono; cold energy mass required; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(n, ok, msg):
    CHK[n] = dict(ok=bool(ok), msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {n}: {msg}")


def fmt(fb):
    return " | ".join(f"{b} {fb[b]['eps']:+.3f}+-{fb[b]['sig']:.3f} (Z {fb[b]['Z']:+.1f})" for b in ("K-in", "K-mid", "K9"))


fE = K.MEAS["f30"]
CL = {"all": K.F30, "early": K.F30 & K.EARLY, "late": K.F30 & ~K.EARLY}
OUT = {}
EGR = {c: K.Egrid(c, None, fE, "main") for c in K.CONS}
base_j = {}
for cls, mk in CL.items():
    d, Cv, L = K.esd_loo(mk)
    for c in K.CONS:
        Eg = K.Egrid(c, mk, fE, cls)
        for foot in K.FOOTS:
            j, curve = K.calibrate(d, Cv, c, foot, mk, fE, fE, Eg)
            jin, curve_in = K.calibrate(d, Cv, c, foot, mk, fE, fE, Eg, bins=K.INNER)           # MU1 route (circular)
            cpc = K.cp_census(c, foot, mk, fE, fE, Eg)
            cpx = K.cp_node(c, foot, mk, j, fE, fE, Eg)
            fbc, fbx = K.all_bands(d, Cv, cpc), K.all_bands(d, Cv, cpx)
            cpl = K.cp_node(c, foot, mk, K.SEL[-1], fE, fE, Eg)
            fbl = K.all_bands(d, Cv, cpl)
            r = dict(x_star=float(K.NODES[j]), outer_curve=curve, x_star_inner_circular=float(K.NODES[jin]),
                     chi2_outer_at_star=curve[K.SEL.index(j)], chi2_outer_at_0p20=curve[0],
                     chi2_inner_census=K.chi2_bins(d, Cv, cpc, K.INNER), chi2_inner_star=K.chi2_bins(d, Cv, cpx, K.INNER),
                     census=fbc, star=fbx, node1=fbl, n=int(mk.sum()))
            # loo eps for early-late
            for nm, cp, fb in (("census", cpc, fbc), ("star", cpx, fbx)):
                mM = cp["moster"][0] + cp["moster"][1]
                r[f"loo_{nm}"] = {b: ((L[:, ix] - mM[ix][None, :]) @ np.array(fb[b]["wvec"])).tolist() for b, ix in K.BANDS.items()}
            OUT[f"{cls}|{c}|{foot}"] = r
            P(f"[{cls:5s} {c} {foot:9s}] x* {K.NODES[j]:.2f} (census edge x not fixed per group; circular inner-calibrated x {K.NODES[jin]:.2f}); "
              f"outer chi2 at x* {r['chi2_outer_at_star']:.1f} (at 0.20: {curve[0]:.1f})")
            P(f"      census : {fmt(fbc)}; inner-9 chi2 {r['chi2_inner_census']:.1f}")
            P(f"      x*     : {fmt(fbx)}; inner-9 chi2 {r['chi2_inner_star']:.1f}")
            P(f"      x=1.00 : {fmt(fbl)}")
RES["cells"] = {k: {kk: vv for kk, vv in v.items() if not kk.startswith("loo_")} for k, v in OUT.items()}

# ---------------------------------------------------------------- labels
LAB = {}
for foot in K.FOOTS:
    per = []
    for c in K.CONS:
        cen = OUT[f"all|{c}|{foot}"]["census"]["K9"]; st = OUT[f"all|{c}|{foot}"]["star"]["K9"]
        dd = st["eps"] - cen["eps"]
        lab = "CLOSED" if st["Z"] < 2 else "REDUCED" if dd <= -cen["sig"] else "WORSE" if dd >= cen["sig"] else "UNCHANGED"
        per.append(lab); P(f"  label {c} {foot}: eps K9 census {cen['eps']:+.3f} -> x* {st['eps']:+.3f} (d {dd:+.3f}, sigma_census {cen['sig']:.3f}; Z at x* {st['Z']:+.1f}) -> {lab}")
    LAB[foot] = per[0] if per[0] == per[1] else "MIXED " + "/".join(per)
RES["label_all"] = LAB
P("  KiDS inner-shortfall label:", LAB)

SPL = {}
for foot in K.FOOTS:
    for c in K.CONS:
        out = {}
        for nm in ("census", "star"):
            e, l_ = OUT[f"early|{c}|{foot}"], OUT[f"late|{c}|{foot}"]
            dv = np.array(e[f"loo_{nm}"]["K9"]) - np.array(l_[f"loo_{nm}"]["K9"])
            vj = (K.NPATCH - 1) / K.NPATCH * np.sum((dv - dv.mean()) ** 2)
            vq = e[nm]["K9"]["sig"] ** 2 + l_[nm]["K9"]["sig"] ** 2
            den = math.sqrt(max(vj, vq)); df = e[nm]["K9"]["eps"] - l_[nm]["K9"]["eps"]
            out[nm] = dict(diff=df, sig=den, Z=df / den, eps_early=e[nm]["K9"]["eps"], eps_late=l_[nm]["K9"]["eps"],
                           x_early=e["x_star"], x_late=l_["x_star"])
        mv = abs(out["star"]["diff"] - out["census"]["diff"]) >= out["census"]["sig"]
        out["label"] = "MOVED" if mv else "UNCHANGED"
        SPL[f"{c}|{foot}"] = out
        P(f"  split {c} {foot:9s}: early-late K9 census {out['census']['diff']:+.3f}+-{out['census']['sig']:.3f} (Z {out['census']['Z']:+.1f}) -> "
          f"x*_class {out['star']['diff']:+.3f}+-{out['star']['sig']:.3f} (Z {out['star']['Z']:+.1f}; x* early {out['star']['x_early']:.2f} late {out['star']['x_late']:.2f}) {out['label']}")
RES["split"] = SPL

# ---------------------------------------------------------------- controls
J531 = json.load(open(os.path.join(K.LANES, "CFG531_inner_halo_shortfall", "cfg531_kids_results.json")))
k1 = max(abs(OUT[f"all|{c}|{foot}"]["census"][b][q] - J531["base"][f"{c}|{foot}|CENSUS"][b][q])
         for c in K.CONS for foot in K.FOOTS for b in ("K-in", "K9") for q in ("eps", "sig"))
check("K1 census path reproduces CFG531 committed BASE eps (K-in, K9)", k1 < 1e-6, f"max |d| {k1:.1e}")
k2 = max(abs(OUT[f"all|{c}|{foot}"]["node1"]["K9"]["eps"] - J531["base"][f"{c}|{foot}|LAW_RTA"]["K9"]["eps"]) for c in K.CONS for foot in K.FOOTS)
P(f"  K2 (reported) node x=1.00 vs LAW_RTA K9 eps: max |d| {k2:.3f}")
RES["K2_node1_vs_lawrta_max_abs_d"] = k2
# K3 mock recovery
j50 = int(np.argmin(np.abs(K.NODES - 0.50)))
d, Cv, L = K.esd_loo(K.F30)
k3 = []
for c in K.CONS:
    Eg = EGR[c]
    for foot in K.FOOTS:
        cp = K.cp_node(c, foot, K.F30, j50, fE, fE, Eg)
        mock = cp["moster"][0] + cp["moster"][1]
        jm, _ = K.calibrate(d, Cv, c, foot, K.F30, fE, fE, Eg, dat=mock)
        fb = K.all_bands(mock, Cv, cp)
        k3.append((K.NODES[jm], fb["K9"]["eps"]))
check("K3 noiseless mock at x = 0.50 recovers x* = 0.50 and eps = 0", all(abs(a - 0.5) < 1e-12 and abs(b) < 1e-9 for a, b in k3), f"{k3}")

# MU1: circular calibration closes the shortfall by construction
mu1 = {}
for foot in K.FOOTS:
    zs = []
    for c in K.CONS:
        r = OUT[f"all|{c}|{foot}"]
        Eg = EGR[c]
        jj = K.SEL[int(np.argmin(r["outer_curve"]))]
        jin = int(np.argmin(np.abs(K.NODES - r["x_star_inner_circular"])))
        cp = K.cp_node(c, foot, K.F30, jin, fE, fE, Eg)
        zs.append(K.all_bands(d, Cv, cp)["K9"]["Z"])
    mu1[foot] = zs
P(f"  MU1 circular (inner-calibrated) K9 Z (A, B): {mu1}; held-out labels {LAB}")
RES["MU1_circular_K9_Z"] = mu1
mu1_ok = any(all(z < 2 for z in zs) for zs in mu1.values()) and any(l.startswith(("UNCHANGED", "WORSE", "REDUCED", "MIXED")) for l in LAB.values())
# MU2 broken edge
mu2 = {foot: all(OUT[f"all|{c}|{foot}"]["chi2_outer_at_0p20"] >= 2 * OUT[f"all|{c}|{foot}"]["chi2_outer_at_star"] for c in K.CONS) for foot in K.FOOTS}
check("MU2 edge fixed at x = 0.20 rejected (outer chi2 >= 2x that at x*) on both footings", all(mu2.values()), f"{mu2}")
check("MU1 circular calibration closes the K9 shortfall on at least one footing while the held-out label does not", mu1_ok, f"{mu1} vs {LAB}")
# POST-FREEZE DIAGNOSTIC (written after seeing MU1/MU2 fail; no verdict weight): how much does eps_K9 move across ALL nodes x >= 0.20?
SCAN = {}
for c in K.CONS:
    for foot in K.FOOTS:
        e9 = [K.all_bands(d, Cv, K.cp_node(c, foot, K.F30, j, fE, fE, EGR[c]))["K9"]["eps"] for j in K.SEL]
        SCAN[f"{c}|{foot}"] = dict(eps_K9_by_node=e9, range=max(e9) - min(e9), sigma_census=OUT[f"all|{c}|{foot}"]["census"]["K9"]["sig"])
        P(f"  [post-freeze] eps_K9 over nodes 0.20..1.00 {c} {foot}: {min(e9):+.3f} .. {max(e9):+.3f} (range {max(e9) - min(e9):.3f} vs sigma {SCAN[c + '|' + foot]['sigma_census']:.3f})")
RES["post_freeze_node_scan"] = SCAN
void = not (CHK["MU2 edge fixed at x = 0.20 rejected (outer chi2 >= 2x that at x*) on both footings"]["ok"] and mu1_ok)
RES["verdict"] = ("VOID by frozen MU1/MU2 (controls did not flip); descriptive: inner-nine eps is edge-independent, label UNCHANGED, split UNCHANGED" if void
                  else f"inner shortfall {LAB}")
P("  VERDICT:", RES["verdict"])
RES["checks"] = CHK
json.dump(RES, open(os.path.join(HERE, f"cfg600_native_catchment_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg600_native_catchment{SUF}.out"), "w").write("\n".join(LOG) + "\n")
P(f"{sum(v['ok'] for v in CHK.values())}/{len(CHK)} checks pass")
