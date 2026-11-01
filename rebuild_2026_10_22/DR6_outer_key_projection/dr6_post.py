#!/usr/bin/env python3
"""DR6 post-result, reported: M3's model Delta Sigma in the band in absolute units from ZN4's shape at the median cluster, for scale; and how many M3 cells have the zoom's edge inside r_ta. Not a grade. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); S = json.load(open(os.path.join(H, "..", "ZN4_cluster_resolution", "zn4_shapes.json"))); A = json.load(open(os.path.join(H, "dr6_amp.json")))["M3"]
x = np.array(S["x"]); k = "0.25"; a, b = S["1e14"][k], S["1e15"][k]; w = (A["lgM200"] - a["lgM"]) / (b["lgM"] - a["lgM"]); ln = (1 - w) * np.array(a["lnm"]) + w * np.array(b["lnm"]); xe = min(a["x_edge"], b["x_edge"])
M2 = 10 ** A["lgM200"]; R2 = A["R200"]; rta = A["rta"]; r = x * R2; m = x <= min(xe, rta / R2); r = r[m]; M = M2 * np.exp(ln[m]); rho = np.gradient(M, r) / (4 * np.pi * r ** 2)
def S_(R):
    l = np.geomspace(1e-3, np.sqrt(max(r[-1] ** 2 - R ** 2, 1e-6)), 3000); return 2 * np.trapz(np.interp(np.sqrt(R ** 2 + l ** 2), r, rho, right=0) * l, np.log(l))
RR = np.geomspace(0.01, 3.0, 300); SS = np.array([S_(x_) for x_ in RR]); out = {}
for R in (1.42, 2.0, 3.0):
    i = np.searchsorted(RR, R); gr = RR[:i + 1]; ds = 2 / R ** 2 * np.trapz(SS[:i + 1] * gr ** 2, np.log(gr)) + 2 / R ** 2 * M2 * np.exp(ln[0]) / (2 * np.pi) * 0 - np.interp(R, RR, SS); out[str(R)] = ds / 1e12
rows = {q["i"]: q for q in json.load(open(os.path.join(H, "cache_jobs", "C3_0.034_+1_rows.json")))}; t3 = [q for q in rows.values() if q["t"] == 2]; n = sum(xe * q["R200"] < q["rta"] for q in t3)
print("M3 median, ZN4 shape (total mass at M200, to min(x_edge, r_ta)), Delta Sigma Msun/pc^2 at R 1.42, 2, 3 Mpc:", {k_: round(v, 2) for k_, v in out.items()}); print("direct two-halo, no exclusion:", {k_: round(v, 2) for k_, v in A["dsig"].items()}); print(f"x_edge {xe:.2f}, r_ta/R200 median {rta / R2:.2f}; M3 clusters with x_edge R200 < r_ta (tail in use, at this x_edge): {n} of {len(t3)}")
