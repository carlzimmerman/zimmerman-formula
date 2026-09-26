#!/usr/bin/env python3
"""A4 -- PIN-FREE joint (R,U) Mahalanobis U-band rule (Z3-wave; owns A4_*). A3 successor.
Door (A3 mechanism, register 2026-09-26): A3 showed the V03c tree's 10 volume
U-OUTs are a PIN-SIDE artefact -- the central K06 inversion applied to volume
truth lands off-grid (wild qh, 17/36 clamps), so any pinned atlas readout fails,
while the R0 truth-config control gives 0 volume U-OUT. The volume U-band rule
must therefore be PIN-FREE. Pre-registered successor (A3 mechanism verbatim):
"joint (R,U) Mahalanobis classification against V03b's stored joint_regions".

This lane implements exactly that: each measured cell is classified against
V03b's STORED (R,U,slack) Gaussian regions (mu, Sig landscape, SigT = Sig +
sampling at the op cell tau0=1,q=0; all loaded from V03b_trio_results.json,
never re-fit) by Mahalanobis distance with V03b's own clip-inverse and stored
clip. NO inversion, NO atlas table, NO nearest-row snap: the measured triple
(R, U, slack) is classified directly. Kernel-matched (thomson cell vs thomson
regions, iso vs iso), exactly as V03b's joint-region overlap census did.

Pre-registered (fixed BEFORE any A4 number; A3's FAIL stands verbatim):
 R0 control (recorded, no gate): self-membership rate over the 36 core cells,
    d_own <= 3 vs the cell's OWN truth region (central->C*, volume->V*);
    the region means are fit from these very cells so ~100% expected; a low
    rate means the stored region fit is broken (region-side problem).
 G1 central: 18/18 core central cells have nonempty 3-sigma membership in the
    C region of their kernel (d_C <= 3).
 G2 all-core: ZERO U-OUT over all 36 core cells (every cell inside >= 1 of its
    kernel's 4 regions at 3 sigma).
 G3 volume: >= 12/18 core volume cells have nonempty 3-sigma membership in
    their kernel's V region.
 G4 sharp discriminator (informative, recorded; NOT a gate): argmin-region
    label (nearest Mahalanobis) of the 18 volume cells -- the pin-free
    nearest-region assignment; 18/18 == V would be the full restoration.
 All of G1-G3 -> PIN-FREE-JOINT-RULE-REBUILT exit 0. Any fail -> honest FAIL
 with the confusion matrix, exit 1, verdict verbatim.
Secondary panel (informative): per-cell covariance-adaptive classification
(d uses Sig + THIS cell's cov3 instead of the op-cell SigT) -- records the
measurement-noise-adaptive readout without changing the gated result.
House rules 1-10 binding; leaf lane does NOT commit.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SIGMA = 3.0

RES = {"title": "A4 pin-free joint (R,U,slack) Mahalanobis U-band rule (Z3-wave)",
       "pre_registration": ("A4 docstring (fixed before any number): R0 control; G1 central "
                            "C-membership 18/18; G2 zero U-OUT over 36 core cells; G3 volume "
                            "V-membership >= 12/18; G4 nearest-region informative. Kernel-matched "
                            "vs V03b joint_regions, SigT verbatim, V03b clip-inverse + stored clip"),
       "gates": {"G1_central_C_membership": 18, "G2_allcore_UOUT": 0,
                 "G3_volume_V_membership": 12, "sigma": SIGMA}}


def clip_inv(A, clip):
    w, V = np.linalg.eigh(A)
    wc = np.array([1.0 / wi if wi > clip else 0.0 for wi in w])
    return (V * wc) @ V.T


def main():
    v = json.load(open(os.path.join(HERE, "V03b_trio_results.json")))
    cells = v["cells"]
    jr = v["joint_regions"]
    clip = v["overlaps"]["clip"]

    # truth map: (src, a, kernel) -> region base
    def region_base(src, a):
        return "V" if src == "volume" else ("C" if src == "central"
                                            else ("S03" if a == 0.3 else "S05"))

    # precompute per-region inverse (stored SigT verbatim, clip-inverse as V03b)
    INV = {}
    for name, reg in jr.items():
        INV[name] = (np.array(reg["mu"]), clip_inv(np.array(reg["SigT"]), clip))

    def classify(x, kernel, Sig_add=None):
        """Return {region_name: d} for the 4 kernel-matched regions, d = Mahalanobis
        with stored SigT (or SigT + Sig_add when given)."""
        out = {}
        for name in ("C", "V", "S03", "S05"):
            full = f"{name}:{kernel}"
            mu, inv = INV[full]
            S = np.array(jr[full]["SigT"])
            if Sig_add is not None:
                S = S + Sig_add
                inv = clip_inv(S, clip)
            d = float(np.sqrt(max((x - mu) @ inv @ (x - mu), 0.0)))
            out[full] = d
        return out

    core_tags = [t for t in cells if t[:1] in ("c", "v")]
    rows = []
    conf_verb = {"central": {}, "volume": {}}     # verbatim SigT classification
    conf_adapt = {"central": {}, "volume": {}}    # covariance-adaptive panel
    self_ok = 0
    for tag in core_tags:
        c = cells[tag]
        src = "central" if c["src"] == "central" else "volume"
        ker = "thomson" if c["kernel"] == "thomson" else "iso"
        x = np.array([c["R"], c["U"], c["slack"]])
        truth = region_base(c["src"], c.get("a"))

        ds = classify(x, ker)
        d0 = ds[f"{truth}:{ker}"]
        if d0 <= SIGMA:
            self_ok += 1
        members = sorted(k for k, d in ds.items() if d <= SIGMA)
        argmin = min(ds.items(), key=lambda kv: kv[1])[0]
        label = members[0].split(":")[0] if len(members) == 1 else (
            "AMBIG-" + "/".join(m.split(":")[0] for m in members) if members else "U-OUT")
        conf_verb[src][label] = conf_verb[src].get(label, 0) + 1

        # adaptive panel: Sig + this cell's cov3
        ds_a = classify(x, ker, Sig_add=np.array(c["cov3"]))
        memb_a = sorted(k for k, d in ds_a.items() if d <= SIGMA)
        lab_a = memb_a[0].split(":")[0] if len(memb_a) == 1 else (
            "AMBIG-" + "/".join(m.split(":")[0] for m in memb_a) if memb_a else "U-OUT")
        conf_adapt[src][lab_a] = conf_adapt[src].get(lab_a, 0) + 1

        rows.append(dict(tag=tag, src=src, kernel=ker, truth=truth,
                         R=round(c["R"], 5), U=round(c["U"], 5), slack=round(c["slack"], 5),
                         d_C=round(ds[f"C:{ker}"], 3), d_V=round(ds[f"V:{ker}"], 3),
                         d_S03=round(ds[f"S03:{ker}"], 3), d_S05=round(ds[f"S05:{ker}"], 3),
                         d_own=round(d0, 3), members=members, argmin=argmin,
                         label_verbatim=label, label_adaptive=lab_a))

    RES["rows"] = rows
    RES["confusion_verbatim_SigT"] = conf_verb
    RES["confusion_adaptive_cov3"] = conf_adapt
    RES["R0_self_membership_rate"] = f"{self_ok}/36"

    # Gates AS PRE-REGISTERED (docstring): G1 = d_C <= 3 for all 18 central;
    # G3 = d_V <= 3 for >= 12/18 volume; G2 = zero U-OUT over all 36.
    # Exclusive-label counts are reported as the honest landscape-overlap panel
    # (same overlap V03b's own census recorded), not as gates.
    g1 = sum(1 for r in rows if r["src"] == "central" and r["label_verbatim"].startswith("AMBIG") and "C" in r["label_verbatim"]) == 18 or \
         all(r["d_C"] <= SIGMA for r in rows if r["src"] == "central")
    g1 = all(r["d_C"] <= SIGMA for r in rows if r["src"] == "central")
    uout = sum(conf_verb[s].get("U-OUT", 0) for s in ("central", "volume"))
    g2 = uout == 0
    g3 = sum(1 for r in rows if r["src"] == "volume" and r["d_V"] <= SIGMA) >= 12
    RES["G3_volume_V_membership_count"] = sum(1 for r in rows if r["src"] == "volume" and r["d_V"] <= SIGMA)
    # G4 informative: nearest-region assignment per branch + R-side cross-check
    vol_argmin_V = sum(1 for r in rows if r["src"] == "volume" and r["argmin"] == f"V:{r['kernel']}")
    ctr_argmin_C = sum(1 for r in rows if r["src"] == "central" and r["argmin"] == f"C:{r['kernel']}")
    RES["G4_volume_argmin_V"] = f"{vol_argmin_V}/18"
    RES["G4_central_argmin_C"] = f"{ctr_argmin_C}/18"
    RES["G1_central_18C"], RES["G2_allcore_zero_UOUT"], RES["G3_volume_V12"] = g1, g2, g3

    print("R0 control: self-membership = %d/36 (d_own <= 3 vs own truth region)" % self_ok, flush=True)
    print("verbatim SigT confusion: central =", conf_verb["central"],
          " volume =", conf_verb["volume"], flush=True)
    print("adaptive cov3 confusion:  central =", conf_adapt["central"],
          " volume =", conf_adapt["volume"], flush=True)
    print(f"G4 nearest-region: volume->V {vol_argmin_V}/18, central->C {ctr_argmin_C}/18", flush=True)

    if g1 and g2 and g3:
        RES["verdict"] = ("PIN-FREE-JOINT-RULE-REBUILT: stored joint regions classify all 36 core "
                          "cells with zero U-OUT (G2), central 18/18 inside C (G1), volume "
                          f"{conf_verb['volume'].get('V', 0)}/18 inside V (G3); the volume-branch "
                          "U-OUTs are gone WITHOUT a pin -- Mahalanobis vs the (R,U,slack) regions "
                          "replaces the pinned atlas readout")
        finish(0)
    RES["mechanism"] = ("pin-free joint classification vs stored joint_regions; the gates as "
                        "pre-registered determine the verdict -- see confusion matrices")
    RES["verdict"] = (f"HONEST FAIL: G1={g1} G2={g2} G3={g3} "
                      f"(verbatim-SigT central={conf_verb['central']}, volume={conf_verb['volume']}); "
                      "verdict verbatim, no re-tuning")
    finish(1)


def finish(rc):
    RES["exit"] = rc
    with open(os.path.join(HERE, "A4_joint_ru_rule.json"), "w") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps({k: RES[k] for k in ("verdict", "G1_central_18C", "G2_allcore_zero_UOUT",
                                          "G3_volume_V12", "G4_volume_argmin_V", "R0_self_membership_rate")}, indent=1))
    print(f"exit {rc}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
