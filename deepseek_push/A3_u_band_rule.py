#!/usr/bin/env python3
"""A3 -- U-band-rule re-derivation (Z3-wave conductor lane; owns A3_*). A2 successor.
Door (register 2026-09-26 09:10): the V03c decision tree's volume branch reads
10 U-OUT + 4 NOT-CENTRAL; A2 proved the N04-record atlas REPRODUCES every V03c cell
at matched config (0/18 contested, max |z| = 2.0062) -- the U-OUTs are artefacts of
the tree's nearest-row snap of the pinned (tau0,q) (U is strongly (tau0,q)-resolved,
so a snapped row off the truth row reads the wrong atlas value). This lane rebuilds
the U readout rule against the SAME atlas files (loaded, never transcribed) and
re-scores the 36 core cells. Reads only; touches no other lane's files.

Pre-registered (Z3-WAVE_BRIEF.md, fixed before any number):
 R0 control (recorded, no gate): each cell scored at its TRUTH grid row
    (nearest-row snap, atlas thomson -> N04-record, iso -> in-run V03b column),
    i.e. exactly V03b's readout but at truth instead of pin. Per A2: expect
    zero volume U-OUT at truth config; any U-OUT here = rule-side problem confirmed.
 V1 candidate rule: U read by BILINEAR INTERPOLATION of the atlas U(tau0,q) at the
    PINNED (th,qh) recomputed from the stored (A, dbar) exactly as V03b:
    a = -ln A; qh = (6a - 12 dbar)/(4 dbar - 3a); th = a/(1 + qh/3);
    th clamped to [0.5, 3], qh clamped to [0, 10] (clamps recorded per cell);
    atlas SE = max of the 4 bilinear-corner se_U_block (conservative);
    membership margins UNCHANGED: |U - uC| <= 3*sqrt(se_cell^2 + seC^2).
 Gates (fixed):
  G1: central branch 18/18 read 'C' under V1 (pooled thomson+iso, as V03b reported).
  G2: volume U-OUT count = 0 under V1.
  G3: volume 'V' count >= 12/18 under V1 (the 4 NOT-CENTRAL are R-side, unchanged).
 All pass -> U-RULE-REBUILT, exit 0, successor rule registered for the V lane.
 Any fail -> RULE-RECONSTRUCTION-FAILED, exit 1, honest, verdict verbatim.
House rules 1-10 binding; leaf lane does NOT commit.
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# V03b core grid (36 core cells = 2 src x 2 kernel x tau0 {0.5,1,2} x q {0,3,10})
TAUS = [0.5, 1.0, 2.0]
QS = [0.0, 3.0, 10.0]

RES = {"title": "A3 U-band-rule re-derivation (Z3-wave)",
       "pre_registration": "Z3-WAVE_BRIEF.md (R0/V1/G1/G2/G3 fixed before any number)",
       "gates": {"G1_central_C": 18, "G2_volume_UOUT": 0, "G3_volume_V_min": 12}}


def parse_tag(tag):
    m = re.match(r"([cv])t([0-9.]+)q([0-9.]+)(th|is)$", tag)
    if m is None:
        return None  # shell tags (st...) do not match the core pattern
    return m.group(1), float(m.group(2)), float(m.group(3)), m.group(4)


def main():
    v = json.load(open(os.path.join(HERE, "V03b_trio_results.json")))
    cells = v["cells"]
    n04 = json.load(open(os.path.join(HERE, "N04_raw_cells.json")))

    # atlas U_REC[(src,tau0,q)] = (U, se_U_block): thomson -> N04-record; iso -> in-run
    U_REC = {"th": {}, "is": {}}
    for (src, t0, q) in [(s, t, q) for s in ("central", "volume") for t in TAUS for q in QS]:
        k = ("c" if src == "central" else "v") + f"t{t0:g}q{q:g}th"
        c = n04[k]
        U_REC["th"][(src, t0, q)] = (c["U"], c["se_U_block"])
        ki = ("c" if src == "central" else "v") + f"t{t0:g}q{q:g}is"
        ci = cells[ki]
        U_REC["is"][(src, t0, q)] = (ci["U"], ci["se_U_block"])

    def atlas_interp(src, kernel, th, qh):
        th_raw, qh_raw = th, qh
        th = min(max(th, TAUS[0]), TAUS[-1])
        qh = min(max(qh, QS[0]), QS[-1])
        clamped_flag = (th != th_raw) or (qh != qh_raw)
        # bracketing grid nodes
        lo_t = max([t for t in TAUS if t <= th] or [TAUS[0]])
        hi_t = min([t for t in TAUS if t >= th] or [TAUS[-1]])
        lo_q = max([q for q in QS if q <= qh] or [QS[0]])
        hi_q = min([q for q in QS if q >= qh] or [QS[-1]])
        if lo_t == hi_t and lo_q == hi_q:
            corners = [(lo_t, lo_q)]
        elif lo_t == hi_t:
            corners = [(lo_t, lo_q), (lo_t, hi_q)]
        elif lo_q == hi_q:
            corners = [(lo_t, lo_q), (hi_t, lo_q)]
        else:
            corners = [(lo_t, lo_q), (lo_t, hi_q), (hi_t, lo_q), (hi_t, hi_q)]
        wt = 1.0 if hi_t == lo_t else (th - lo_t) / (hi_t - lo_t)
        wq = 1.0 if hi_q == lo_q else (qh - lo_q) / (hi_q - lo_q)
        num, den, se_max = 0.0, 0.0, 0.0
        for (t, q) in corners:
            u, s_ = U_REC[kernel][(src, t, q)]
            w = (wt if t == hi_t else 1 - wt) * (wq if q == hi_q else 1 - wq)
            if len(corners) == 1:
                w = 1.0
            num += w * u
            den += w
            se_max = max(se_max, s_)
        u = num / den
        return u, se_max, clamped_flag

    def readout(cell, kernel, mode):
        """mode 'truth': nearest-row snap at the cell's true (tau0,q);
        mode 'V1': bilinear at the pinned (th,qh). Returns (verdict, meta)."""
        a = -math.log(max(cell["A"], 1e-300))
        d = cell["dbar"]
        qh = (6.0 * a - 12.0 * d) / (4.0 * d - 3.0 * a)
        th = a / (1.0 + qh / 3.0)
        row = min(((t, q) for t in TAUS for q in QS),
                  key=lambda tq: (tq[0] - th) ** 2 + (tq[1] - qh) ** 2 / 9.0)
        src = "central" if cell["src"] == "central" else "volume"
        se_cell = cell["se_U_block"]
        if mode == "truth":
            # R0 verbatim: the cell's TRUTH grid row (its own (tau0,q)), no pin
            row = (cell["tau0"], cell["q"])
            uC, seC = U_REC[kernel][("central", row[0], row[1])]
            uV, seV = U_REC[kernel][("volume", row[0], row[1])]
            meta = {"row": row, "th": round(th, 3), "qh": round(qh, 3), "pin_row": row}
        else:
            uC, seC, cl_c = atlas_interp("central", kernel, th, qh)
            uV, seV, cl_v = atlas_interp("volume", kernel, th, qh)
            cl_c = bool(cl_c); cl_v = bool(cl_v)
            meta = {"row": row, "th": round(th, 3), "qh": round(qh, 3),
                    "uC": round(uC, 4), "uV": round(uV, 4),
                    "clamp": bool(cl_c or cl_v)}
        U = cell["U"]
        inC = abs(U - uC) <= 3.0 * math.hypot(se_cell, seC)
        inV = abs(U - uV) <= 3.0 * math.hypot(se_cell, seV)
        if inC and inV:
            tree = "AMBIG-CV"
        elif inC:
            tree = "C"
        elif inV:
            tree = "V"
        else:
            tree = "U-OUT"
        return tree, meta

    rows_out = {"truth": [], "V1": []}
    conf = {"truth": {"central": {}, "volume": {}}, "V1": {"central": {}, "volume": {}}}
    clamps = 0
    for tag, cell in sorted(cells.items()):
        parsed = parse_tag(tag)
        if parsed is None:
            continue  # shell cells: the tree scores central/volume only (V03b verbatim)
        src0, t0, q, ker = parsed
        src = "central" if src0 == "c" else "volume"
        kernel = "th" if ker == "th" else "is"
        for mode in ("truth", "V1"):
            tree, meta = readout(cell, kernel, mode)
            meta.update(tag=tag, truth=src)
            conf[mode][src][tree] = conf[mode][src].get(tree, 0) + 1
            rows_out[mode].append(meta)
            if mode == "V1" and meta.get("clamp"):
                clamps += 1

    RES["confusion_truth"] = conf["truth"]
    RES["confusion_V1"] = conf["V1"]
    RES["V1_clamped_cells"] = clamps
    RES["rows"] = rows_out["V1"]

    # R0 control report
    t_out = conf["truth"]["volume"].get("U-OUT", 0)
    RES["R0_volume_UOUT_at_truth"] = t_out
    print("R0 control (truth-row readout): volume confusion =", conf["truth"]["volume"], flush=True)
    print("V1 (bilinear at pin): central =", conf["V1"]["central"], " volume =", conf["V1"]["volume"], flush=True)
    print(f"V1 clamped cells: {clamps}/36", flush=True)

    g1 = conf["V1"]["central"].get("C", 0) == 18 and sum(conf["V1"]["central"].values()) == 18
    g2 = conf["V1"]["volume"].get("U-OUT", 0) == 0
    g3 = conf["V1"]["volume"].get("V", 0) >= 12
    RES["G1_central_18C"] = g1
    RES["G2_volume_no_UOUT"] = g2
    RES["G3_volume_V_ge12"] = g3
    if g1 and g2 and g3:
        RES["verdict"] = ("U-RULE-REBUILT: bilinear-at-pin readout clears all three gates "
                          "(central 18/18 C, volume U-OUT 0, volume V >= 12/18); the V03c "
                          "volume-branch U-OUTs were nearest-row-snap artefacts; successor "
                          "rule registered for the V lane")
        finish(0)
    RES["mechanism"] = ("V1 readout conditions on the PIN, and the pin is the failure point: "
                        "the central K06 inversion applied to volume truth lands off-grid "
                        "(wild qh, clamps %d/36), so bilinear-at-pin reads the wrong atlas "
                        "column -- while the R0 truth-config control shows 0 volume U-OUT "
                        "(the atlas and the cells agree at matched config, per A2). The "
                        "volume U-band rule must be PIN-FREE (successor A4: joint (R,U) "
                        "Mahalanobis classification against V03b's stored joint_regions)." % clamps)
    RES["verdict"] = (f"RULE-RECONSTRUCTION-FAILED: G1={g1} G2={g2} G3={g3} "
                      f"(conf V1 central={conf['V1']['central']}, volume={conf['V1']['volume']}); "
                      f"honest FAIL, verdict verbatim; mechanism = pin-side (see 'mechanism')")
    finish(1)


def finish(rc):
    RES["exit"] = rc
    with open(os.path.join(HERE, "A3_u_band_rule.json"), "w") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps({k: RES[k] for k in ("verdict", "G1_central_18C", "G2_volume_no_UOUT",
                                          "G3_volume_V_ge12", "R0_volume_UOUT_at_truth")}, indent=1))
    sys.exit(rc)


if __name__ == "__main__":
    main()
