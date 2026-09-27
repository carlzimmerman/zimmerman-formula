#!/usr/bin/env python3
"""VE1 -- LOS-frame window correction (Z4-wave; owns VE1_*).
Door: V02's registered next step, verbatim (V02_INCLINATION_PLANE.md section 6):
"An LOS-frame re-derivation of the window correction (measured LOS inflation ~=
eps^-0.10 central / eps^-0.13 volume vs the frozen-frame eps^-0.35 / eps^-0.38) is
the registered next step." Context (stored): the K10 frozen correction over-corrects
the LOS window (F6: inflation 1.131 vs 1.522 at eps=0.3 central) and its application
inverts the corrected ordering (R_corr(0.3) 0.530/0.507 below the sphere LOS anchor
0.685, V02 section 6). This lane re-measures R_lo at i=90 fresh, fits the LOS
inflation exponent, and tests the registered decision + portability gates.
Pre-registered gates in Z4-WAVE_BRIEF.md (K0, K1, K2, K3), fixed BEFORE any number;
house rules 1-10 binding; leaf lane does NOT commit.
"""
import json, math, os, sys, time
from multiprocessing import Pool
from V02_inclination import one_cell, seed_for

HERE = os.path.dirname(os.path.abspath(__file__))
N = 600000
EPSES = (0.3, 0.5, 0.7, 1.0)
REF_LOS = {"central": -0.10, "volume": -0.13}
REF_FROZEN = {"central": -0.35, "volume": -0.38}
RES = {"title": "VE1 LOS-frame window correction (V02 registered next)",
       "pre_registration": "Z4-WAVE_BRIEF.md VE1 gates (fixed before any number)"}
_T0 = time.time()

def finish(rc):
    RES["elapsed_s"] = round(time.time() - _T0, 1)
    RES["exit"] = rc
    with open(os.path.join(HERE, "VE1_results.json"), "w") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps({k: RES.get(k) for k in
                      ("verdict", "K0_parity", "K1_exponents", "K2_powerlaw",
                       "K3_portability")}, indent=1))
    print("elapsed %ss; exit %s" % (RES["elapsed_s"], rc))
    sys.exit(rc)

def main():
    v02 = json.load(open(os.path.join(HERE, "V02_results.json")))
    tabs = v02["measurements"]["U_los_tables_q0"]

    # ---- fresh re-measure at i=90, q=0
    specs = []
    for src in ("central", "volume"):
        for eps in EPSES:
            specs.append(dict(tag="VE1_%s_%s" % (src, eps), n=N, q=0.0, src=src,
                              eps=eps, i=90.0, seed=seed_for(eps, 90.0, 0.0, src) + 555000))
    with Pool(4) as ex:
        rows = ex.map(one_cell, specs)
    fresh = {(r["src"], r["eps"]): r for r in rows}

    # ---- K0 parity at eps=0.5 vs stored
    pmax = 0.0
    for src in ("central", "volume"):
        st = tabs[src]["0.5"]["90"]
        fr = fresh[(src, 0.5)]
        z = abs(fr["R_lo"] - st["R"]) / math.sqrt(fr["seR_lo"] ** 2 + st["se_R"] ** 2)
        pmax = max(pmax, z)
        print("K0 %s eps=0.5: fresh %.5f vs stored %.5f  z=%.2f" %
              (src, fr["R_lo"], st["R"], z), flush=True)
    RES["K0_parity"] = {"max_z": pmax, "pass": bool(pmax < 3.0)}
    if pmax >= 3.0:
        RES["verdict"] = "FAIL K0 machinery parity (z=%.2f >= 3)" % pmax
        finish(1)

    # ---- K1 exponent decision (eps=0.3 deepest lever) + K2 adequacy at all eps
    K1, K2 = {}, {}
    ok2 = True
    for src in ("central", "volume"):
        r1 = fresh[(src, 1.0)]
        p_ref = REF_LOS[src]; p_frz = REF_FROZEN[src]
        exps = {}
        for eps in (0.3, 0.5, 0.7):
            re = fresh[(src, eps)]
            infl = re["R_lo"] / r1["R_lo"]
            sig = math.sqrt((re["seR_lo"] / re["R_lo"]) ** 2 +
                            (r1["seR_lo"] / r1["R_lo"]) ** 2)
            p = math.log(infl) / math.log(eps)
            pse = sig / abs(math.log(eps))
            resid = abs(math.log(infl) - p_ref * math.log(eps))
            exps[str(eps)] = dict(infl=infl, sig_ln=sig, p=p, p_se=pse,
                                  resid_vs_ref=resid, resid_se_mult=resid / sig)
            if resid > 3.0 * sig:
                ok2 = False
        p3 = exps["0.3"]
        d_los = abs(p3["p"] - p_ref); d_frz = abs(p3["p"] - p_frz)
        band = max(2.0 * p3["p_se"], 0.03)
        if d_los <= band and d_frz <= band:
            call = "MEASURED-OTHER (within band of BOTH registered exponents)"
        elif d_los <= band:
            call = "LOS-FLAT (matches registered eps^%.2f)" % p_ref
        elif d_frz <= band:
            call = "FROZEN-LIKE (matches frozen eps^%.2f)" % p_frz
        else:
            call = "MEASURED-OTHER (matches neither; p=%.3f+-%.3f)" % (p3["p"], p3["p_se"])
        K1[src] = dict(call=call, p_eps03=p3["p"], p_se=p3["p_se"],
                       d_los=d_los, d_frozen=d_frz, band=band)
        K2[src] = dict(ok=ok2, rows=exps)
        print("K1 %s: %s" % (src, call), flush=True)
    RES["K1_exponents"], RES["K2_powerlaw"] = K1, K2

    # ---- K3 portability: parametric corr_los on V02 STORED tables; frozen contrast
    K3 = {"ok": True, "srcs": {}}
    for src in ("central", "volume"):
        p_ref = REF_LOS[src] if "LOS-FLAT" in K1[src]["call"] else K1[src]["p_eps03"]
        anch = tabs[src]["1.0"]["90"]["R"]
        worst = None
        rowsk = {}
        for eps in ("0.3", "0.5", "0.7"):
            st = tabs[src][eps]["90"]
            rc_los = st["R"] / (float(eps) ** p_ref)
            se = st["se_R"]
            gap = anch - rc_los
            sig = math.sqrt(se ** 2 + tabs[src]["1.0"]["90"]["se_R"] ** 2)
            rowsk[eps] = dict(R_lo=st["R"], corr_los=rc_los, gap=gap, sig=sig,
                              z_below=gap / sig)
            if gap > 3.0 * sig:
                K3["ok"] = False
            worst = max(worst or 0.0, gap / sig)
        # frozen contrast from stored tables + K10_corr p (V02 section-6 inversion
        # reproduced from stored R_lo / K10 p, recorded as the comparison row)
        k10p = v02["measurements"]["K10_corr"]["0.3"][src]["p"]
        st3 = tabs[src]["0.3"]["90"]
        rc_frz = st3["R"] / (0.3 ** k10p)
        K3["srcs"][src] = dict(p_used=p_ref, anchor=anch, worst_z=worst, rows=rowsk,
                               frozen_contrast=dict(p_k10=k10p, R_corr_03=rc_frz,
                                                    below_anchor_by_sig=(anch - rc_frz) /
                                                    math.sqrt(st3["se_R"] ** 2 +
                                                              tabs[src]["1.0"]["90"]["se_R"] ** 2)))
    RES["K3_portability"] = K3
    ok = RES["K0_parity"]["pass"] and ok2 and K3["ok"]
    if ok:
        RES["verdict"] = ("LOS-WINDOW-MEASURED+PORTABLE: parity pass; exponents %s; "
                          "single-exponent corr_los adequate (K2) and repairs the "
                          "frozen-correction ordering inversion (K3)"
                          % ({s: K1[s]["call"] for s in K1},))
    else:
        RES["verdict"] = ("HONEST FAIL (recorded): K0=%s K2=%s K3=%s -- see rows"
                          % (RES["K0_parity"]["pass"], ok2, K3["ok"]))
    finish(0 if ok else 1)

if __name__ == "__main__":
    main()
