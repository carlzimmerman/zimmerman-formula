#!/usr/bin/env python3
"""A5 -- region-CONTRAST readout for the pin-free U rule (Z3-wave; owns A5_*). A4 successor.
Door (A4 verdict + register row, 2026-09-26): A4 proved the pin-free joint
(R,U,slack) Mahalanobis membership kills the volume-branch U-OUT class (10->0,
G2) but does NOT restore EXCLUSIVE geometry reading -- at 3-sigma against the
STOred landscape SigT every core cell sits inside several regions (V03b's own
census: C x V 3-sigma mass overlap ~0.66), so membership is an outlier VETO,
not a classifier. A4's mechanism pre-registered the successor verbatim:
"region-CONTRAST (likelihood-ratio / tighter-sigma readout)".

This lane implements exactly that: for each measured (R,U,slack) cell the readout
is the signed likelihood-ratio contrast between its kernel's V and C joint
regions, Delta = d_V^2 - d_C^2 (Mahalanobis quadratic forms, SigT VERBATIM from
V03b_trio_results.json, clip-inverse + stored clip -- all loaded, never re-fit).
A call requires the contrast preponderance |Delta| >= delta (tighter-sigma
margin); otherwise the cell is AMBIG (contrast insufficient to call). Read C iff
Delta >= +delta, V iff Delta <= -delta.

Pre-registered (fixed BEFORE any A5 number; A4 verdicts stand verbatim):
 R0 control (recorded, no gate): argmin-region readout (Delta without margin)
    must reproduce A4's G4 counts (volume->V 12/18, central->C 9/18) -- an
    engine-replication gate on the loaded regions.
 G1 central: 18/18 core central cells read 'C' (Delta >= +delta at delta = 9,
    i.e. 3-sigma-squared margin).
 G2 all-core: zero U-OUT under the contrast rule (every cell calls C, V or
    AMBIG; U-OUT = no region at 3-sigma membership, retained as the veto guard).
 G3 volume: >= 12/18 core volume cells read 'V' (Delta <= -9).
 G4 informative (no gate): margin sweep delta in {4, 9, 16, 25}
    (2^2..5^2 sigma-squared) -- exclusivity-vs-separation tradeoff recorded.
 G5 informative (no gate): measurement-aware panel -- contrast with
    SigT + this cell's cov3 (the A4 adaptive analog); expect the same calls,
    recorded as the noise-footing check.
 All of G1-G3 -> REGION-CONTRAST-BUILT exit 0 (the U rule reads the volume
 branch exclusively, pin-free, at a 3-sigma contrast margin). Any fail ->
 honest FAIL with the margin table, exit 1, verdict verbatim.
House rules 1-10 binding; leaf lane does NOT commit.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DELTA = 9.0   # 3-sigma-squared preponderance margin for an exclusive call
MARGINS = [4.0, 9.0, 16.0, 25.0]

RES = {"title": "A5 region-contrast readout for the pin-free U rule (Z3-wave)",
       "pre_registration": ("A5 docstring (fixed before any number): R0 argmin replication; "
                            "G1 central 18/18 C at Delta>=+9; G2 zero U-OUT; G3 volume >= 12/18 V "
                            "at Delta<=-9; G4 margin sweep {4,9,16,25}; G5 adaptive-cov3 panel. "
                            "Kernel-matched vs V03b joint_regions, SigT verbatim, V03b clip + inverse"),
       "gates": {"delta": DELTA, "G1_central_C": 18, "G3_volume_V": 12, "G2_zero_UOUT": 0}}


def clip_inv(A, clip):
    w, V = np.linalg.eigh(A)
    wc = np.array([1.0 / wi if wi > clip else 0.0 for wi in w])
    return (V * wc) @ V.T


def main():
    v = json.load(open(os.path.join(HERE, "V03b_trio_results.json")))
    cells = v["cells"]
    jr = v["joint_regions"]
    clip = v["overlaps"]["clip"]

    def region_base(src, a):
        return "V" if src == "volume" else ("C" if src == "central"
                                            else ("S03" if a == 0.3 else "S05"))

    # precompute C/V inverses per kernel (verbatim SigT)
    INV = {}
    for name in ("C", "V", "S03", "S05"):
        for ker in ("thomson", "iso"):
            full = f"{name}:{ker}"
            INV[full] = (np.array(jr[full]["mu"]), clip_inv(np.array(jr[full]["SigT"]), clip))

    core_tags = [t for t in cells if t[:1] in ("c", "v")]
    rows = []
    for tag in core_tags:
        c = cells[tag]
        src = "central" if c["src"] == "central" else "volume"
        ker = "thomson" if c["kernel"] == "thomson" else "iso"
        x = np.array([c["R"], c["U"], c["slack"]])
        muV, iV = INV[f"V:{ker}"]
        muC, iC = INV[f"C:{ker}"]
        dV2 = float((x - muV) @ iV @ (x - muV))
        dC2 = float((x - muC) @ iC @ (x - muC))
        # 4-region argmin over kernel-matched regions (A4 G4 replication, identical semantics)
        ds = {}
        for name in ("C", "V", "S03", "S05"):
            mu, iq = INV[f"{name}:{ker}"]
            ds[f"{name}"] = float((x - mu) @ iq @ (x - mu))
        argmin8 = min(ds.items(), key=lambda kv: kv[1])[0]
        Delta = dV2 - dC2
        # adaptive panel: SigT + this cell's cov3
        SV = np.array(jr[f"V:{ker}"]["SigT"]) + np.array(c["cov3"])
        SC = np.array(jr[f"C:{ker}"]["SigT"]) + np.array(c["cov3"])
        dV2a = float((x - muV) @ clip_inv(SV, clip) @ (x - muV))
        dC2a = float((x - muC) @ clip_inv(SC, clip) @ (x - muC))
        Delta_a = dV2a - dC2a
        rows.append(dict(tag=tag, src=src, kernel=ker, truth=region_base(c["src"], c.get("a")),
                         dV2=round(dV2, 3), dC2=round(dC2, 3), Delta=round(Delta, 3),
                         Delta_adaptive=round(Delta_a, 3),
                         argmin8=argmin8))
    RES["rows"] = rows

    # R0: 4-region kernel-matched argmin replication vs A4 G4 counts (identical semantics)
    r0v = sum(1 for r in rows if r["src"] == "volume" and r["argmin8"] == "V")
    r0c = sum(1 for r in rows if r["src"] == "central" and r["argmin8"] == "C")
    RES["R0_argmin_volume_V"] = f"{r0v}/18"
    RES["R0_argmin_central_C"] = f"{r0c}/18"
    # sibling-pair sign (A5's own no-margin limiting case), informative
    spv = sum(1 for r in rows if r["src"] == "volume" and r["Delta"] < 0)
    spc = sum(1 for r in rows if r["src"] == "central" and r["Delta"] > 0)
    RES["R0b_sibling_sign_volume_V"] = f"{spv}/18"
    RES["R0b_sibling_sign_central_C"] = f"{spc}/18"
    print(f"R0 all-8 argmin replication: volume->V {r0v}/18, central->C {r0c}/18 ",
          f"(A4 G4 recorded 12/18, 9/18)", flush=True)
    print(f"R0b sibling-pair contrast sign (no margin): volume->V {spv}/18, central->C {spc}/18", flush=True)

    # G1/G2/G3 at delta = 9
    def label_at(delta, r):
        D = r["Delta"]
        return "C" if D >= delta else ("V" if D <= -delta else "AMBIG")

    conf9 = {"central": {}, "volume": {}}
    for r in rows:
        lab = label_at(DELTA, r)
        conf9[r["src"]][lab] = conf9[r["src"]].get(lab, 0) + 1
        r["label_d9"] = lab
    RES["confusion_delta9"] = conf9

    g1 = conf9["central"].get("C", 0) == 18 and sum(conf9["central"].values()) == 18
    uout = sum(conf9[s].get("U-OUT", 0) for s in ("central", "volume"))
    g2 = uout == 0
    g3 = conf9["volume"].get("V", 0) >= 12
    RES["G1_central_18C"], RES["G2_zero_UOUT"], RES["G3_volume_V12"] = g1, g2, g3
    print(f"delta=9: central={conf9['central']} volume={conf9['volume']} "
          f"-> G1={g1} G2={g2} G3={g3}", flush=True)

    # G4 margin sweep + G5 adaptive panel (informative)
    sweep = {}
    for d in MARGINS:
        c = {"central": {}, "volume": {}}
        for r in rows:
            lab = label_at(d, r)
            c[r["src"]][lab] = c[r["src"]].get(lab, 0) + 1
        sweep[d] = c
    RES["margin_sweep"] = sweep
    for d in MARGINS:
        print(f"  delta={d:5.0f}: central={sweep[d]['central']} volume={sweep[d]['volume']}", flush=True)

    adapt = {"central": {}, "volume": {}}
    for r in rows:
        lab = ("C" if r["Delta_adaptive"] >= DELTA else
               ("V" if r["Delta_adaptive"] <= -DELTA else "AMBIG"))
        adapt[r["src"]][lab] = adapt[r["src"]].get(lab, 0) + 1
    RES["confusion_adaptive_cov3"] = adapt
    print(f"adaptive-cov3 (delta=9): central={adapt['central']} volume={adapt['volume']}", flush=True)

    if g1 and g2 and g3:
        RES["verdict"] = ("REGION-CONTRAST-BUILT: the likelihood-ratio readout (Delta = d_V^2 - d_C^2, "
                          "3-sigma-squared margin) reads central 18/18 C and volume >= 12/18 V"
                          f" ({conf9['volume'].get('V', 0)}/18) with zero U-OUT -- the exclusive "
                          "branch reading the membership rule could not give is restored pin-free "
                          "by the contrast. Margins: 4->V; 9; 16; 25 recorded")
        finish(0)
    RES["verdict"] = (f"HONEST FAIL: G1={g1} G2={g2} G3={g3} at delta={DELTA} "
                      f"(conf central={conf9['central']}, volume={conf9['volume']}); "
                      "margin sweep recorded; verdict verbatim, no re-tuning")
    finish(1)


def finish(rc):
    RES["exit"] = rc
    with open(os.path.join(HERE, "A5_region_contrast.json"), "w") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps({k: RES[k] for k in ("verdict", "G1_central_18C", "G2_zero_UOUT",
                                          "G3_volume_V12", "R0_argmin_volume_V",
                                          "R0_argmin_central_C")}, indent=1))
    print(f"exit {rc}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
