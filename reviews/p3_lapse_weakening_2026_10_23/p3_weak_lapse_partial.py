#!/usr/bin/env python3
"""AMENDMENT A1 (post-result, reported only): partial d log eps / d log M_kk at fixed (r, k, G, omega, L*, footing)."""
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.argv = [sys.argv[0]]
ns = {"__file__": str(HERE / "p3_weak_lapse.py")}
code = (HERE / "p3_weak_lapse.py").read_text()
head = code[:code.index("# ================================================================ W1 identity")]
exec(head, ns)                                     # constants + P3's scales()/zP_of() (hash-checked) only
scales, zP_of = ns["scales"], ns["zP_of"]
c_SI, G_SI, PC, KPC, MU_K = ns["c_SI"], ns["G_SI"], ns["PC"], ns["KPC"], ns["MU_K"]
rows = {}
cases = {"G3 compact r 0.3 kpc": (1e11, 0.3, 0.3), "G1 r 5 kpc": (1e11, 2.0, 5.0), "G2 r 1.65 kpc": (1e12, 3.0, 1.65)}
for cname, (Mg, ag, rk) in cases.items():
    for foot, a0 in ns["A0"].items():
        a0m = a0 / c_SI ** 2
        L = 24 * PC
        r_ = rk * KPC
        GM = G_SI * Mg * 1.98892e30
        rr = np.array([0.999, 1.0, 1.001]) * r_
        gN = GM / (rr + ag * KPC) ** 2
        xN = gN / a0
        xx = (xN + np.sqrt(xN ** 2 + 4 * xN)) / 2
        KPs = a0m * xx / (1 + xx)
        KDP = float((np.gradient(rr ** 2 * KPs, rr) / rr ** 2)[1])
        vc = math.sqrt(a0 * xx[1] * r_)
        Qbar = 1 + 1e-6
        gh = KDP * (1 + KDP * L ** 2 / 2) + MU_K ** 2 * 1e-6 / Qbar
        for kr in (3, 30, 300):
            kk = kr / r_
            Ms = np.logspace(0, 6, 25)
            eps = {}
            regime = []
            for Mkk in Ms:
                zPh = zP_of(kk, L, Mkk, Qbar)
                s_ = scales(zPh + MU_K ** 2, zPh, gh, kk, vc / r_, a0m, a0m / math.sqrt(Mkk), Mkk, L, Qbar)
                for vn, v in s_["vertices"].items():
                    eps.setdefault(vn, []).append(v["eps"])
                regime.append(("E=c_pi k" if s_["c_pi"] * kk >= vc / r_ / c_SI else "E=omega/c",
                               "Z_P>mu^2" if zPh > MU_K ** 2 else "Z_P<mu^2"))
            sl = {vn: float(np.polyfit(np.log10(Ms), np.log10(np.array(e)), 1)[0]) for vn, e in eps.items()}
            rows[f"{cname}|{foot}|k r {kr}"] = {"x_actual": float(xx[1]), "slopes": sl,
                                                "regimes_M1_M1e6": [regime[0], regime[-1]],
                                                "eps_max_M1": max(e[0] for e in eps.values()),
                                                "eps_max_M1e6": max(e[-1] for e in eps.values())}
            print(f"{cname:22s} {foot:9s} kr {kr:4d} x {xx[1]:7.2f} regimes {regime[0]} -> {regime[-1]}  "
                  + "  ".join(f"{vn.split()[0]} {s:+.2f}" for vn, s in sl.items()))
(HERE / "p3_weak_lapse_partial.json").write_text(json.dumps(rows, indent=1))
