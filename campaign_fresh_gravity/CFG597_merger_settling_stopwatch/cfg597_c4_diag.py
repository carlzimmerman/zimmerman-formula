#!/usr/bin/env python3
"""CFG597 C4 diagnosis (post-run, 2026-10-10; README D-5).  Why did the isolated-progenitor control fail (16.96 kpc vs 15)?
(a) the committed isolated run's offsets by component and time; (b) the gas-centroid estimator on the exactly symmetric t = 0
initial state (true gas centre = (0, 0)), with the frozen start (argmax pixel of the block-upsampled 50-kpc gas map) and, for
diagnosis only, a start at the mass-weighted centroid.  No verdict is changed by this script.
Run: nice -n 10 python3 cfg597_c4_diag.py  -> cfg597_c4_diag.out, cfg597_c4_diag_results.json"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg597_lib as L
import cfg597_sim as S

OUT = []; RES = {}
P = lambda s="": (print(s, flush=True), OUT.append(str(s)))

r = json.load(open(os.path.join(HERE, "runs", "r10_L_2S_a1_can_isolated.json")))
gas_off, lens_off, gal_r = [], [], []
for d in r["diag"]:
    m = d["main"]; g = np.array(m["gal"])
    gas_off.append(float(np.linalg.norm(np.array(m["gas"]) - g))); lens_off.append(float(np.linalg.norm(np.array(m["lens150"]) - g)))
    gal_r.append(float(np.linalg.norm(g)))
RES["a"] = dict(gas_minus_gal_max=max(gas_off), gas_minus_gal_median=float(np.median(gas_off)), lens_minus_gal_max=max(lens_off),
                gal_from_origin_max=max(gal_r), n_epochs=len(gas_off), n_gas_over_15=int(sum(x > 15 for x in gas_off)))
P("(a) committed isolated run (L-2S, alpha 1, canonical, 0.6 Gyr): " + json.dumps({k: round(v, 2) if isinstance(v, float) else v for k, v in RES["a"].items()}))

sim = S.Sim(dict(foot="can", case="L", alpha=1.0, mode="isolated"))
(XX, YY), gas_k, st_k, tot, cold = sim.project()
sg = gas_k[0]
ip = np.unravel_index(np.argmax(sg), sg.shape)
frozen = L.iter_centroid_2d(XX, YY, sg, (XX[ip], YY[ip]), 150.0)
mw0 = np.array([(sg * XX).sum() / sg.sum(), (sg * YY).sum() / sg.sum()])
alt = L.iter_centroid_2d(XX, YY, sg, mw0, 150.0)
gal = L.iter_centroid_2d(XX, YY, st_k[0], np.median(sim.x[sim.is_s, :2], axis=0), 150.0)
RES["b"] = dict(argmax_pixel=[float(XX[ip]), float(YY[ip])], gas_centroid_frozen_start=frozen.tolist(),
                gas_centroid_massweighted_start=alt.tolist(), galaxy_centroid_t0=gal.tolist())
P(f"(b) t = 0, symmetric IC, true gas centre (0, 0): argmax pixel ({XX[ip]:.2f}, {YY[ip]:.2f}); frozen-start gas centroid "
  f"({frozen[0]:.2f}, {frozen[1]:.2f}) = {np.hypot(*frozen):.1f} kpc off; mass-weighted start ({alt[0]:.2f}, {alt[1]:.2f}) = "
  f"{np.hypot(*alt):.1f} kpc off; galaxy centroid ({gal[0]:.2f}, {gal[1]:.2f}) from {sim.is_s.sum()} star particles")
P("READING: the gas centroid sits ~13 kpc off a perfectly centred gas sphere at t = 0, before any dynamics. The frozen estimator "
  "(start at the argmax pixel of a map made by block-repeating 50-kpc gas cells, tol 0.25 kpc) stalls at a block-edge fixed point. "
  "Galaxy-centroid shot noise (+-4-9 kpc) adds to it. The lensing centroid stays within 10.6 kpc and M(<300 kpc) drifts -0.13%, so this "
  "is a gas-ESTIMATOR offset, not a dynamical drift. It still fails the frozen C4, so the dependent verdicts stay VOID.")
open(os.path.join(HERE, "cfg597_c4_diag.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "cfg597_c4_diag_results.json"), "w"), indent=1)
