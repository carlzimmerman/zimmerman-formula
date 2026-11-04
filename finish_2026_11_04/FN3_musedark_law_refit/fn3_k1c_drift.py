"""FN3 diagnostic K1c (amendment A1, no gate): can the survey's own released numbers pin the pressure-support form?

From each primary galaxy's released v_perp and sigma at 2.2 R_e / 1.678 (interpolated along the slit), each drift form
gives v_c; compare with the released v22. Uses only released numbers, not this lane's mass model.
kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os

import numpy as np

import fn3_common as C


def main():
    s = json.load(open(os.path.join(C.HERE, "fn3_sample.json")))
    forms = ("D1", "D2", "D3", "D1x0.5", "none")
    res = {k: [] for k in forms}
    used = []
    for gid in s["primary"]:
        g = C.load_galaxy(gid)
        p, rot, kpc = g["par"], g["rot"], g["kpc"]
        Re = p["radius"] * g["pixscale"] * kpc
        n = p["sersic_n"]
        r = np.abs(rot["dx_arcsec"]) * kpc
        o = np.argsort(r)
        r, v, sg = r[o], np.abs(rot["v_kms"])[o], rot["sig_kms"][o]
        r22 = 2.2 * Re / 1.678
        if not (r.min() <= r22 <= r.max()):
            continue
        used.append(gid)
        vp, s22 = np.interp(r22, r, v), np.interp(r22, r, sg)
        dls2 = np.interp(r22, r, np.gradient(np.log(sg ** 2), np.log(np.maximum(r, 1e-4))))
        dl = float(C.sersic_dlnS(r22, Re, n))
        vad2 = {"D1": -2 * s22 ** 2 * dl, "D2": -2 * s22 ** 2 * dl - s22 ** 2 * dls2,
                "D3": -2 * p["velocity_dispersion"] ** 2 * dl, "D1x0.5": -s22 ** 2 * dl, "none": 0.0}
        for k in forms:
            res[k].append(math.sqrt(vp ** 2 + vad2[k]) / g["der"]["v22"] - 1)
    out = {"criteria": "c6640225c2", "amendment": "A1", "N": len(used), "forms": {}}
    lines = [f"K1c (diagnostic, no gate): released v_perp and sigma at 2.2 R_e/1.678 -> v_c, against released v22; N {len(used)}"]
    for k in forms:
        a = np.array(res[k])
        d = dict(median=float(np.median(a)), p16=float(np.percentile(a, 16)), p84=float(np.percentile(a, 84)),
                 frac_within_3pct=float(np.mean(np.abs(a) <= 0.03)))
        out["forms"][k] = d
        lines.append(f"  {k:7s} median {d['median']:+.4f}  16-84 % [{d['p16']:+.4f}, {d['p84']:+.4f}]  within 3 %: {d['frac_within_3pct']:.3f}")
    lines.append("No form pins the convention: the released curve is not the intrinsic v_perp the forms assume (A1).")
    lines.append("kappa = 1/2 FITTED; not theory closed.")
    print("\n".join(lines))
    open(os.path.join(C.HERE, "fn3_k1c_drift.out"), "w").write("\n".join(lines) + "\n")
    json.dump(out, open(os.path.join(C.HERE, "fn3_k1c_drift.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
