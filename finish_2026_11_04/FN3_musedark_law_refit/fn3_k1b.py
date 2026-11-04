"""FN3 K1b (amendment A1, diagnostic, no gate): the survey's DC14 model, extracted the way the released curve looks made.

Survey conventions (each run file's kpc per arcsec, h, E(z), Delta_vir) and released parameters. Mass: DC14 + MGE disc
(q 0.15) + pi G Sigma r gas. Kinematics: sigma^2 = sigma_0^2 + (h v_c/R)^2 with h = 0.15 r_half; drift D1; the survey's
apparent handling sqrt(|v_c^2 - v_AD^2|). Extraction: at each released slit offset on the major axis, the flux-weighted
mean line-of-sight velocity through the thick disc (Gauss-Hermite in height, slit 1 pixel wide), divided by sin i.
Compared with the released |v_kms| over 0.5-2.5 R_e. Reported only; it cannot change the Stage 0 label.
kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os

import numpy as np

import fn3_common as C
import fn3_cube as F


def extract(dx_arcsec, Re_as, n, inc, kpc, R, vp, ngh=24, nslit=5):
    ci, si = math.cos(math.radians(inc)), math.sin(math.radians(inc))
    t, w = np.polynomial.hermite_e.hermegauss(ngh)
    w = w / w.sum()
    hz = 0.15 * Re_as
    ys = np.linspace(-0.1, 0.1, nslit)
    out = []
    for x in dx_arcsec:
        num = den = 0.0
        for y in ys:
            Y = y / ci + hz * t * (si / ci)
            Rr = np.sqrt(x * x + Y * Y)
            S = np.exp(-C.b_n(n) * ((Rr / Re_as) ** (1 / n) - 1)) * w
            v = np.interp(Rr * kpc, R, vp) * (x / np.maximum(Rr, 1e-9)) * si
            num += float(np.sum(S * v))
            den += float(np.sum(S))
        out.append(num / den / si if den > 0 else float("nan"))
    return np.array(out)


def main():
    s = json.load(open(os.path.join(C.HERE, "fn3_sample.json")))
    res = {}
    lines = ["K1b (diagnostic): survey DC14 model, slit-extracted through the thick disc, against released v_kms (0.5-2.5 R_e)"]
    for variant in ("abs", "clip"):
        rms_all = []
        for gid in s["primary"]:
            g = C.load_galaxy(gid)
            p, rot, kpc = g["par"], g["rot"], g["kpc"]
            Re_as = p["radius"] * g["pixscale"]
            Re = Re_as * kpc
            n = float(np.clip(p["sersic_n"], 0.5, 4.0))
            R = np.geomspace(0.01, 80.0, 400)
            mass = F.DC14Mass(g["h"], g["Ez"], g["DeltaVir"])
            vc2 = mass.vc2(R, Re, n, p["virial_velocity"], p["concentration"], p["log_X"], p["gas_density"])
            h = 0.15 * Re
            sig2 = p["velocity_dispersion"] ** 2 + h * h * vc2 / R ** 2
            vad2 = -2.0 * sig2 * C.sersic_dlnS(R, Re, n)
            d = vc2 - vad2
            vp = np.sqrt(np.abs(d)) if variant == "abs" else np.sqrt(np.maximum(d, 0.0))
            dx = np.asarray(rot["dx_arcsec"], float)
            vm = np.abs(extract(np.abs(dx), Re_as, n, p["inclination"], kpc, R, vp))
            vo = np.abs(np.asarray(rot["v_kms"], float))
            rr = np.abs(np.asarray(rot["rad_Re"], float))
            m = (rr >= 0.5) & (rr <= 2.5) & (vo > 0)
            rms = float(np.sqrt(np.mean((vm[m] / vo[m] - 1) ** 2))) if m.sum() else float("nan")
            res.setdefault(variant, {})[gid] = rms
            rms_all.append(rms)
        a = np.array(rms_all)
        lines.append(f"  {variant:4s}: N {len(a)}, median rms {np.nanmedian(a):.4f}; within 3 %: {np.mean(a <= 0.03):.3f}, "
                     f"5 %: {np.mean(a <= 0.05):.3f}, 10 %: {np.mean(a <= 0.10):.3f}")
    lines.append("For comparison, K1 as frozen (intrinsic v_perp, no extraction): best variant 1.4 % within 3 %.")
    lines.append("kappa = 1/2 FITTED; not theory closed.")
    print("\n".join(lines))
    open(os.path.join(C.HERE, "fn3_k1b.out"), "w").write("\n".join(lines) + "\n")
    json.dump(res, open(os.path.join(C.HERE, "fn3_k1b.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
