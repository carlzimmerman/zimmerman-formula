#!/usr/bin/env python3
"""G111 follow-up: the Newtonian-arm temperature ladder at mu = 1.0 (spec section 2.5, Arm N), so the Arm-S
temperature-branch PASS can be attributed to the mediator or to the dust's self-gravity.  Same engine, same ICs."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import G111_relaxation_nbody as G
from multiprocessing import Pool
cells = [dict(tag=f"N ladder s={s} R0=1.0", arm="N", ic=dict(kind="uniform", R0=1.0, sig=s), mu=1.0, dt=G.DT, seed=20 + i) for i, s in enumerate((0.3, 0.5, 0.7, 1.0, 1.5))]
if __name__ == "__main__":
    with Pool(5) as p: R = p.map(G.run_cell, cells)
    print(f"    {'cell':28s} {'dE/E':>9s} {'sig2/st2':>9s} {'r50':>6s} {'f_esc':>6s} {'M(<rM)':>7s} {'gamma':>6s}")
    for r in R: print(f"    {r['tag']:28s} {r['dE']:+9.1e} {r['sig2_all']:9.3f} {r['r50']:6.2f} {r['f_esc']:6.2f} {r['M_in_rM']:7.2f} {r['gamma']:6.2f}")
    n_ok = sum(0.8 <= r["sig2_all"] <= 1.25 for r in R)
    print(f"\n  [{'PASS' if n_ok >= 3 else 'FAIL'}] N-ARM TEMPERATURE BRANCH: sigma_inf^2/sigma_t^2 in [0.8, 1.25] for >= 3 of 5 (the Arm-S branch passed 4/5)")
    print("  reading: if the Newtonian arm ALSO passes, the temperature attainment is the dust's self-gravity at mu = 1.0, not the mediator;")
    print("           if it fails, the mediator is doing the work and the branch is a genuine Arm-S result.")
    json.dump(R, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "G111_nladder.json"), "w"), indent=1, default=str)
    print("G111-NLADDER COMPLETE")
