"""FN3 diagnostic after K2 (amendment A2, no gate on its own): is the ENCLOSED baryonic mass recovered when the
stellar mass is not? Uses only K2's synthetic records (no real data).

M_bar(<R) = (M* + M_H2) x f_enc(R) + pi R^2 Sigma_HI, with f_enc the projected enclosed fraction of the Sersic MGE.
Reported at R = 1.5, 2.0 and 2.5 R_e: log10 M_bar,fit(<R) - log10 M_bar,true(<R), and the same for the a0 x 2 refit.
kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os

import numpy as np

import fn3_common as C


def f_enc(x, n):
    sig, frac, _ = C.sersic_mge(n)
    return float(np.sum(frac * (1 - np.exp(-x * x / (2 * sig * sig)))))


def main():
    N = C.Native()
    k2 = json.load(open(os.path.join(C.HERE, "fn3_k2.json")))
    recs = k2["records"]
    rows = []
    lines = ["K2 enclosed-baryon diagnostic (synthetic only): log M_bar,fit(<R) - log M_bar,true(<R)"]
    for r in recs:
        g = C.load_galaxy(r["gid"])
        Re = g["par"]["radius"] * 0.2 * N.kpc_per_arcsec(r["z"])
        n = float(np.clip(g["par"]["sersic_n"], 0.5, 4.0))
        Msed = 10 ** r["logm_sed"]
        MH2 = r["mu"] * Msed
        out = dict(gid=r["gid"], d_true=r["d_true"])
        for xr in (1.5, 2.0, 2.5):
            fe = f_enc(xr, n)
            R = xr * Re
            mt = (10 ** (r["logm_sed"] + r["d_true"]) + MH2) * fe + math.pi * R * R * 5.0e6
            mf = (10 ** (r["logm_sed"] + r["d_fit"]) + MH2) * fe + math.pi * R * R * r["sighi_fit"] * 1e6
            out[f"dbar_{xr}"] = math.log10(mf / mt)
        rows.append(out)
    for xr in (1.5, 2.0, 2.5):
        a = np.array([o[f"dbar_{xr}"] for o in rows])
        lines.append(f"  R = {xr} R_e: median {np.median(a):+.4f}, median |.| {np.median(np.abs(a)):.4f}, "
                     f"16-84 % [{np.percentile(a, 16):+.4f}, {np.percentile(a, 84):+.4f}]")
    a = np.array([r["d_fit"] - r["d_true"] for r in recs])
    lines.append(f"  stellar Delta for comparison: median |.| {np.median(np.abs(a)):.4f}, 16-84 % [{np.percentile(a, 16):+.4f}, {np.percentile(a, 84):+.4f}]")
    lines.append("kappa = 1/2 FITTED; not theory closed.")
    print("\n".join(lines))
    open(os.path.join(C.HERE, "fn3_k2_enclosed.out"), "w").write("\n".join(lines) + "\n")
    json.dump(dict(rows=rows), open(os.path.join(C.HERE, "fn3_k2_enclosed.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
