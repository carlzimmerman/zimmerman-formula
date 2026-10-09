#!/usr/bin/env python3
"""CFG526 post-hoc (NOT gating; written after the frozen verdicts): the lensing-tracer side of B.
Cosmic shear sees the gravitating field, not the particles. At z = 0 (the only epoch with saved positions) compute A_eff (k = 1, 2, 4) from
r_grav = P(delta_grav)/P_S0 and from r_part, per box and footing, F = 1 and the fiducial-high feedback band. Also a crude z = 0.5 estimate,
r_grav(0.5) ~ r_part(0.5) x [r_grav/r_part](0). Literature A_mod values recalled, PROVISIONAL."""
import os, json, importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg526_work"))
spec = importlib.util.spec_from_file_location("d", os.path.join(HERE, "cfg526_data.py")); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
dat = json.load(open(os.path.join(HERE, "cfg526_data.json")))
L_ = []
def P(s=""): print(s); L_.append(s)
P("CFG526 post-hoc (not gating): lensing-tracer A_eff. A_eq(k) = (r F P_NL - P_L)/(P_NL - P_L), mean over k = 1, 2, 4. PROVISIONAL literature.")
OUT = {}
for foot, boxes in D.BOX.items():
    P(f"\n== {foot}")
    for L, (nm, run, s0) in boxes.items():
        d, d0 = np.load(os.path.join(WORK, f"cfg526_{nm}.npz")), np.load(os.path.join(WORK, f"cfg526_S0_L{L}.npz"))
        kk = d["kgrav"]; row = {}
        for lab, F in (("F=1", [1, 1, 1]), ("fid-hi", D.F_FID_HI), ("fid-lo", D.F_FID_LO)):
            a = {"part_z0": [], "grav_z0": [], "grav_z05_est": []}
            for j, k in enumerate(D.KS):
                i = int(np.argmin(np.abs(np.log(kk / k))))
                rg, rp = float(d["pgrav"][i] / d0["ppart"][i]), float(d["ppart"][i] / d0["ppart"][i])
                r0, kb, Pnl0 = D.ratio_at(run, s0, "z0", k); r5, kb5, Pnl5 = D.ratio_at(run, s0, "z0.5", k)
                Pl0 = float(D.eng.P_lin0(np.array([kb]))[0]); Pl5 = Pl0 * D.eng.Dgrow(2 / 3) ** 2
                a["part_z0"].append(D.A_eq(rp, F[j], Pnl0, Pl0)); a["grav_z0"].append(D.A_eq(rg, F[j], Pnl0, Pl0))
                a["grav_z05_est"].append(D.A_eq(r5 * rg / rp, F[j], Pnl5, Pl5))
            row[lab] = {k_: float(np.mean(v)) for k_, v in a.items()}
            pulls = {k_: [(v - m) / s for (m, s) in D.DATA.values()] for k_, v in row[lab].items()}
            row[lab + "_pulls"] = pulls
            P(f"  L{L:<3d} {lab:6s} A_eff part z0 {row[lab]['part_z0']:.3f}  grav z0 {row[lab]['grav_z0']:.3f}  grav z0.5 (est) {row[lab]['grav_z05_est']:.3f}"
              f"   pulls grav z0.5 est: KiDS {pulls['grav_z05_est'][0]:+.1f}  DES {pulls['grav_z05_est'][1]:+.1f}")
        OUT[f"{foot}_L{L}"] = row
P("\nGravitating vs particle P ratio to S0 at z = 0, k = 1 / 2 / 4 (r_grav / r_part):")
for L in (50, 25):
    d0 = np.load(os.path.join(WORK, f"cfg526_S0_L{L}.npz"))
    for n in ("NOCOMP", "DCcan", "K1"):
        d = np.load(os.path.join(WORK, f"cfg526_{n}_L{L}.npz")); kk = d["kgrav"]; s_ = []
        for k in D.KS:
            i = int(np.argmin(np.abs(np.log(kk / k)))); s_.append([float(d["pgrav"][i] / d0["ppart"][i]), float(d["ppart"][i] / d0["ppart"][i])])
        OUT[f"grav_vs_part_{n}_L{L}"] = s_
        P(f"  L{L:<3d} {n:7s} " + "   ".join(f"{a:.3f} / {b:.3f}" for a, b in s_))
P("\nReading: the gravitating field is suppressed far more than the particles at k 2-4 (the compensation removes core mass directly).")
P("If shear traced the engine's gravitating field, F = 1 alone would sit about 3 sigma below both A_mod values in L100 and L50")
P("(-3.0 to -3.4) and 1-2 sigma below in L25 (whose k = 1 bin is only 4 fundamental modes); adding any feedback band moves it to -2 .. -6 sigma;")
P("this is post-hoc, z = 0.5 is scaled from z = 0, the boxes are not converged, and it is not a frozen verdict.")
open(os.path.join(HERE, "cfg526_posthoc.out"), "w").write("\n".join(L_) + "\n")
json.dump(OUT, open(os.path.join(HERE, "cfg526_posthoc.json"), "w"), indent=1)
