"""FN3b K2'' (criteria s3): synthetic recovery and power with Sigma_HI fixed at 6.0, before any data.

Templates: FN3's 71 primary galaxies. Planted Sigma_HI = 6.0 x 10^N(0, 0.15) per galaxy (seed 50261105 + id); noise
matched-filter S/N 30 (seed 40261105 + id). Scenarios: flat (Delta 0) and rising (0.6 (z - median z)). The fit holds
Sigma_HI at 6.0. MUTATE: a0 x 2 on the flat fits. Power: FN3's grader with budget_fn3b.json on the rising scenario.
Checkpoints per fit; SIGTERM exits 75. kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import signal
import sys
import time

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
FN3 = os.path.join(HERE, "..", "FN3_musedark_law_refit")
sys.path.insert(0, FN3)
import fn3_common as C  # noqa: E402
import fn3_cube as F  # noqa: E402
from fn3_k2 import bounds, setup  # noqa: E402
from fn3_grade import grade, fmt  # noqa: E402

SIG_HI = 6.0
OUTJ = os.path.join(HERE, "fn3b_k2pp.jsonl")
STOP = False


def _term(*_):
    global STOP
    STOP = True


signal.signal(signal.SIGTERM, _term)


def one(gid, scen, zmed, N, P15, phot):
    g, z, kpc, logm_sed, mu, cm, geo = setup(gid, N, P15, phot)
    a0 = C.A_FOOT["canonical"] * float(N.band_ratio(z))
    rs = np.random.default_rng(50261105 + gid)
    sighi_true = SIG_HI * 10 ** float(rs.normal(0.0, 0.15))
    d_true = 0.0 if scen == "flat" else 0.6 * (z - zmed)
    MH2 = mu * 10 ** logm_sed
    gen = F.Fitter(cm, None, np.ones((25, 25, 25)), F.LawMass(MH2, a0), "law")
    th_true = np.array([geo[k] for k in F.GEO] + [geo["sig0"], logm_sed + d_true, sighi_true])
    m = gen.model(th_true)
    sig = math.sqrt(float(np.sum(m ** 2))) / 30.0
    data = m + np.random.default_rng(40261105 + gid).normal(0.0, sig, m.shape)
    var = np.full(m.shape, sig * sig)
    lo, hi = bounds(geo, logm_sed)
    lo, hi = lo[:11], hi[:11]
    th0 = th_true[:11].copy()
    th0[0:3] += rs.normal(0, 0.3, 3)
    th0[3] *= 1 + rs.normal(0, 0.1)
    th0[4] *= 1 + rs.normal(0, 0.1)
    th0[6] += rs.normal(0, 2.0)
    th0[7] += rs.normal(0, 5.0)
    th0[9] = geo["sig0"] * (1 + rs.normal(0, 0.2))
    th0[10] = logm_sed
    r1 = F.Fitter(cm, data, var, F.LawMass(MH2, a0), "law", sighi_fixed=SIG_HI).fit(th0, lo, hi)
    rec = dict(gid=gid, scen=scen, z=z, logm_sed=logm_sed, d_true=d_true, sighi_true=sighi_true,
               d_fit=float(r1["x"][10] - logm_sed), chi2_red=r1["chi2_red"])
    if scen == "flat":
        lo2 = lo.copy()
        lo2[10] -= 0.5
        rM = F.Fitter(cm, data, var, F.LawMass(MH2, 2 * a0), "law", sighi_fixed=SIG_HI).fit(r1["x"], lo2, hi)
        rec["d_fit_mutate"] = float(rM["x"][10] - logm_sed)
    return rec


def main():
    N, P15 = C.Native(), C.planck15()
    phot, _ = C.load_catalogue()
    s = json.load(open(os.path.join(FN3, "fn3_sample.json")))
    third = {gid: int(t) for t, gl in s["thirds"].items() for gid in gl}
    prim = s["primary"]
    zmed = float(np.median([phot[g]["z"] for g in prim]))
    done = {}
    if os.path.exists(OUTJ):
        for ln in open(OUTJ):
            d = json.loads(ln)
            done[(d["gid"], d["scen"])] = d
    t0 = time.time()
    for scen in ("flat", "rising"):
        for gid in prim:
            if (gid, scen) in done:
                continue
            if STOP:
                print("SIGTERM: stopping cleanly")
                sys.exit(75)
            rec = one(gid, scen, zmed, N, P15, phot)
            rec["third"] = third[gid]
            done[(gid, scen)] = rec
            with open(OUTJ, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
            print(f"{scen:6s} ID{gid:<5d} z {rec['z']:.3f} true {rec['d_true']:+.3f} fit {rec['d_fit']:+.3f} "
                  f"SigHI true {rec['sighi_true']:5.2f} ({time.time() - t0:.0f}s)", flush=True)
    flat = [done[(g, "flat")] for g in prim]
    rise = [done[(g, "rising")] for g in prim]
    budget = json.load(open(os.path.join(HERE, "budget_fn3b.json")))
    lines = [f"K2'' (FN3b), fresh synthetics, N {len(prim)} per scenario, S/N 30, planted Sigma_HI 6.0 x 10^N(0, 0.15), fitted at 6.0"]
    ok_a = True
    for t in range(3):
        e = [r["d_fit"] - r["d_true"] for r in flat if r["third"] == t]
        b = float(np.median(e))
        ok_a = ok_a and abs(b) <= 0.07
        lines.append(f"  (a) third {t}: N {len(e)}, median bias {b:+.4f} (line 0.07) -> {'PASS' if abs(b) <= 0.07 else 'FAIL'}")
    sf = float(stats.theilslopes([r["d_fit"] for r in flat], [r["z"] for r in flat])[0])
    sr = float(stats.theilslopes([r["d_fit"] for r in rise], [r["z"] for r in rise])[0])
    ok_b, ok_c = abs(sf) <= 0.10, abs(sr - 0.60) <= 0.10
    sh = float(np.median([r["d_fit_mutate"] - r["d_fit"] for r in flat]))
    ok_d = abs(sh + 0.30) <= 0.07
    lines.append(f"  (b) flat slope {sf:+.4f} (line 0 +- 0.10) -> {'PASS' if ok_b else 'FAIL'}")
    lines.append(f"  (c) rising slope {sr:+.4f} (line 0.60 +- 0.10) -> {'PASS' if ok_c else 'FAIL'}")
    lines.append(f"  (d) MUTATE a0 x 2 median shift {sh:+.4f} (line -0.30 +- 0.07) -> {'PASS (bites)' if ok_d else 'FAIL'}")
    ok_e = True
    for scen, recs in (("flat", flat), ("rising", rise)):
        rows = [dict(z=r["z"], third=r["third"], d=r["d_fit"], valid=True) for r in recs]
        for foot in C.A_FOOT:
            res = grade(rows, budget, foot)
            lines += ["  " + l for l in fmt(res, f"grader on {scen}, {foot} budget")]
            if scen == "rising" and res["label"] == "BAND CONSISTENT":
                ok_e = False
    lines.append(f"  (e) power: the rising scenario is {'not ' if ok_e else ''}labelled BAND CONSISTENT -> {'PASS' if ok_e else 'FAIL'}")
    e_all = np.array([r["d_fit"] - r["d_true"] for r in flat])
    lines.append(f"  per-galaxy scatter (flat): 16-84 % [{np.percentile(e_all, 16):+.3f}, {np.percentile(e_all, 84):+.3f}]")
    allok = bool(ok_a and ok_b and ok_c and ok_d and ok_e)
    lines.append(f"K2'' {'PASS: Stage 1 may run after the owner yes for the cutouts' if allok else 'FAIL: no FN3b label, no cutout requested'}")
    lines.append("kappa = 1/2 FITTED; not theory closed.")
    print("\n".join(lines))
    open(os.path.join(HERE, "fn3b_k2pp.out"), "w").write("\n".join(lines) + "\n")
    json.dump(dict(pass_=allok, a=bool(ok_a), b=bool(ok_b), c=bool(ok_c), d=bool(ok_d), e=bool(ok_e), slope_flat=sf,
                   slope_rising=sr, mutate_shift=sh, zmed=zmed), open(os.path.join(HERE, "fn3b_k2pp.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
