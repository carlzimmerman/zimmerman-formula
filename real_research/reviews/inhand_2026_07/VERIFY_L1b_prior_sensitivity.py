#!/usr/bin/env python3
"""ADVERSARIAL VERIFY for lane_L1b: is the U_bul prior doing hidden work?
Reuses the L1b script's own data/likelihood machinery (exec of its definition block),
then runs: sigUb in {0.05, 0.10, 0.15, 0.30(~free)} and prior-center shifts
LUB0 -> log10(0.5), log10(0.9) at 0.10 dex. Plus a 300-resample bootstrap at 0.30 dex.
If a0_hat or Dchi2(9.36e-11) is prior-DRIVEN, widening/moving the prior should move it a lot."""
import numpy as np, os, sys, time

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lane_L1b_bulge_sigma_knobs.py")
src = open(SRC).read()
cut = src.index("# ================================================================= GATE V1")
ns = {}
exec(compile(src[:cut], SRC, "exec"), ns)
np = ns["np"]
build, combine, analyze, bootstrap = ns["build"], ns["combine"], ns["analyze"], ns["bootstrap"]
gals, nu_fw, NG = ns["gals"], ns["nu_fw"], ns["NG"]
A0FW, A0FORK, LUB0 = ns["A0FW"], ns["A0FORK"], ns["LUB0"]

# build caches once (locked for no-bulge, unlocked for bulge gals) -- same as main script
T_lock = build(gals, nu_fw, unlock=False, tag="v-locked")
ib = [i for i, g in enumerate(gals) if np.any(g["Vb"] != 0)]
T_blg = build([gals[i] for i in ib], nu_fw, unlock=True, tag="v-unlock-bulge")
T_unl = list(T_lock)
for j, i in enumerate(ib): T_unl[i] = T_blg[j]

print("\n=== PRIOR-WIDTH SENSITIVITY (full N=%d, corrected likelihood) ===" % NG)
rows = {}
for s in (0.05, 0.10, 0.15, 0.30):
    G = combine(T_unl, sigUb=s)
    rows[s] = analyze(f"sigUb={s:.2f} dex" + ("  (~FREE)" if s == 0.30 else ""), G)
G_lock = combine(T_lock)
r_lock = analyze("locked baseline (repro)", G_lock)

print("\n=== PRIOR-CENTER SENSITIVITY (sigUb=0.10) ===")
for c in (0.5, 0.7, 0.9):
    G = combine(T_unl, sigUb=0.10, lu0b=np.log10(c))
    analyze(f"U_bul prior center {c:.1f}", G)

print("\n=== BOOTSTRAP at sigUb=0.30 (near-free), 500 resamples ===")
G30 = combine(T_unl, sigUb=0.30)
h30, z30 = bootstrap("near-free U_bul 0.30", G30)

d05, d10, d30 = rows[0.05]["dfw"], rows[0.10]["dfw"], rows[0.30]["dfw"]
prior_driven = (d30 < 9) or (abs(np.log(rows[0.30]["a0hat"]/rows[0.10]["a0hat"])) > 0.10)
print("\nVERDICT: Dchi2(9.36e-11) at 0.05/0.10/0.15/0.30 dex = "
      f"{d05:.1f}/{d10:.1f}/{rows[0.15]['dfw']:.1f}/{d30:.1f}; near-free boot z~{z30:.1f}")
print("  U_bul prior HIDDEN WORK: " + ("YES -- exclusion is prior-driven" if prior_driven
      else "NO -- exclusion stable as the prior widens to near-free"))
print(f"total {time.time()-ns['t_start']:.0f}s"); print("EXIT 0")
