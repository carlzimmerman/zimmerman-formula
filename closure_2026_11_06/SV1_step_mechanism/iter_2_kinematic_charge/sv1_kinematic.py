#!/usr/bin/env python3
"""SV1 iter_2 (criteria 74a07762ff): keys carried by scalars the action already has. K_Pi (stiffness charge
Pi = D.P + 2X = s^2/N^2 in a stationary source, monotone in the depth |Phi|/c^2) and K_v (the khronon's response to the
matter flow, entering at v^2/c^2). QX20's build() (QX5 loaders) read-only.
  OMP_NUM_THREADS=1 nice -n 15 python3 sv1_kinematic.py   -> sv1_kinematic.out / .json (MUTATE M1, M2 inside)
kappa = 1/2 FITTED; not theory closed."""
import os, sys, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
src = open(os.path.join(REPO, "closure_2026_11_06", "QX20_failure_ladder", "qx20.py")).read()
NS = {"__file__": os.path.join(REPO, "closure_2026_11_06", "QX20_failure_ladder", "qx20.py"), "__name__": "qx20_lib"}
_a = sys.argv; sys.argv = [sys.argv[0]]; exec(compile(src[:src.index("BGRID = ")], "qx20_lib", "exec"), NS); sys.argv = _a
A0, build, C = NS["A0"], NS["build"], NS["C"]
CKMS = C / 1e3
KA1 = {"canonical": dict(V2_vobs=48, V6_depth=522), "alt": dict(V2_vobs=48, V6_depth=535)}
DELTA = {"canonical": dict(E=0.209888 - 0.027383, X=0.467499 - 0.027383, G=0.263752 - 0.027383),
         "alt": dict(E=0.188763 + 0.000603, X=0.434523 + 0.000603, G=0.225997 + 0.000603)}
ZLINE = 0.057


def overlap(v, vs, Dh, Ds):
    lo, hi = np.percentile(v, 5), np.percentile(v, 95); ov = (vs >= lo) & (vs <= hi); hv = (v >= lo) & (v <= hi)
    n = int(ov.sum())
    if n < 20: return dict(n=n, step=None, se=None)
    step = float(np.median(Dh[hv]) - np.median(Ds[ov]))
    se = float(math.hypot(np.std(Dh[hv], ddof=1) / math.sqrt(hv.sum()), np.std(Ds[ov], ddof=1) / math.sqrt(n)) * 1.2533)  # median SE
    return dict(n=n, n_hot=int(hv.sum()), step=step, se=se, range=[float(lo), float(hi)])


R = dict(tag="sv1_kinematic", criteria="74a07762ff", note="kappa = 1/2 FITTED; not theory closed")
for f, a0 in A0.items():
    H, S = build(a0); Hn, Sn = build(a0, newton=True)
    Dh = np.array([h["D"] for h in H]); Ds = np.array([s["D"] for s in S]); cls = np.array([h["cls"] for h in H])
    RF = {}
    keys = {"K_Pi (depth |Phi|/c^2)": "V6_depth", "K_v (v^2/c^2)": "V2_vobs"}
    for kn, vn in keys.items():
        v = np.array([h[vn] for h in H], float); vs = np.array([s[vn] for s in S], float)
        if vn == "V2_vobs": v, vs = (v / CKMS) ** 2, (vs / CKMS) ** 2       # monotone map: overlap counts unchanged
        o = overlap(v, vs, Dh, Ds)
        ka = o["n"] == KA1[f][vn]
        dead = bool(o["step"] is not None and o["step"] > ZLINE + 2 * o["se"])
        m1 = overlap(v * 1e10, vs, Dh, Ds); m1_dead = bool(m1["step"] is not None and m1["step"] > ZLINE + 2 * m1["se"])
        e = dict(overlap=o, KA1=bool(ka), DEAD=dead, M1_overlap=m1["n"], M1_bites=bool(not m1_dead))
        # per-class steps inside the overlap (reported)
        lo, hi = o["range"]; ov = (vs >= lo) & (vs <= hi)
        e["class_step"] = {c: (float(np.median(Dh[(cls == c) & (v >= lo) & (v <= hi)]) - np.median(Ds[ov]))
                               if ((cls == c) & (v >= lo) & (v <= hi)).sum() else None) for c in "EXG"}
        if vn == "V2_vobs":
            kmed = {c: float(np.median(v[cls == c])) for c in "EXG"}; ks = float(np.median(vs))
            cneed = {c: (10 ** DELTA[f][c] - 1) / kmed[c] for c in "EXG"}
            sp_shift = {c: float(np.mean(np.log10(1 + cneed[c] * vs)) ) for c in "EXG"}
            e.update(k_median=kmed, k_sparc_median=ks, C_need=cneed, sparc_shift_at_C=sp_shift,
                     CLUSTER_SET=bool(min(cneed.values()) > 100), BREAKS_SPARC=bool(min(sp_shift.values()) > ZLINE))
        RF[kn] = e
        P(f"[{f}] {kn}: overlap {o['n']} SPARC pts (KA1 {KA1[f][vn]}: {'PASS' if ka else 'FAIL'}), hot in range {o.get('n_hot')}; "
          f"step hot-SPARC {o['step']:+.3f} +- {o['se']:.3f} vs line {ZLINE} + 2se = {ZLINE + 2 * o['se']:.3f} -> {'DEAD (mono_dead)' if dead else 'not dead'}; "
          f"class steps " + " ".join(f"{c} {s_:+.3f}" if s_ is not None else f"{c} n/a" for c, s_ in e["class_step"].items())
          + f"; M1 (hot key x1e10): overlap {m1['n']} -> {'BITES' if e['M1_bites'] else 'NO BITE'}")
        if vn == "V2_vobs":
            P(f"[{f}]    median k_v: E {kmed['E']:.2e} X {kmed['X']:.2e} G {kmed['G']:.2e} SPARC {ks:.2e}; C_need E {cneed['E']:.2e} X {cneed['X']:.2e} G {cneed['G']:.2e} "
              f"-> {'CLUSTER-SET (C >> 1)' if e['CLUSTER_SET'] else 'O(1) possible'}; SPARC mean shift at that C: E {sp_shift['E']:+.3f} X {sp_shift['X']:+.3f} G {sp_shift['G']:+.3f} dex "
              f"-> {'BREAKS SPARC' if e['BREAKS_SPARC'] else 'SPARC kept'}")
    m2 = float(np.mean([s["D"] for s in Sn]) - Ds.mean()); RF["M2_sparc_move"] = -m2; RF["M2_bites"] = bool(abs(m2) > 0.3)
    P(f"[{f}] MUTATE M2 Newton: SPARC mean moves {m2:+.3f} dex (line 0.3) -> {'BITES' if RF['M2_bites'] else 'NO BITE'}")
    kp = RF["K_Pi (depth |Phi|/c^2)"]; kv = RF["K_v (v^2/c^2)"]
    RF["label_K_Pi"] = "DEAD" if kp["DEAD"] else "ALIVE"
    RF["label_K_v"] = "DEAD" if kv["DEAD"] else ("CLUSTER-SET" if kv["CLUSTER_SET"] else "ALIVE")
    RF["label"] = ("NO-GO IN CLASS" if RF["label_K_Pi"] != "ALIVE" and RF["label_K_v"] != "ALIVE" else "OPEN")
    P(f"[{f}] K_Pi {RF['label_K_Pi']}; K_v {RF['label_K_v']}{' and BREAKS SPARC' if kv['BREAKS_SPARC'] else ''}; T3 (QX22 support split +0.002 +- 0.045 ln) carried; LABEL: {RF['label']}")
    R[f] = RF
json.dump(R, open(os.path.join(HERE, "sv1_kinematic.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "sv1_kinematic.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed.\n")
