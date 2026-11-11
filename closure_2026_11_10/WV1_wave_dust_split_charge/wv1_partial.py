#!/usr/bin/env python3
"""AMENDMENT A2: turn a stopped law-bracket run at nu_max into runs/<tag>_partial.json (the outputs it reached and the
minimum R_s over them), read from the run's checkpoint in $WV1_CKPT/wv1_ckpt/<tag>.pkl.

    python3 wv1_partial.py <tag> [<tag> ...]
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, pickle, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CK = os.path.join(os.environ.get("WV1_CKPT", tempfile.gettempdir()), "wv1_ckpt")
for tag in sys.argv[1:]:
    ck = pickle.load(open(os.path.join(CK, tag + ".pkl"), "rb"))
    st = ck["state"]
    outs = st["res"]
    if "z2" not in outs:
        sys.exit(f"{tag}: z = 2 not reached; A2 needs at least the z = 2 output")
    h = np.array(st["hist"]) if st["hist"] else np.zeros((0, 2))
    res = {"tag": tag + "_partial", "amendment": "A2", "stopped_at_t_TU": ck["t"], "steps": ck["steps"],
           "outputs": outs, "R_s_reached_min": min(o["R_s"] for o in outs.values()),
           "outputs_reached": list(outs.keys()),
           "narrow_maxima_total_reached": sum(o["n_narrow_maxima"] for o in outs.values()),
           "central_peak_over_bar_reached": float(h[:, 1].max()) if len(h) else None}
    json.dump(res, open(os.path.join(HERE, "runs", tag + "_partial.json"), "w"), indent=1, default=float)
    print(f"{tag}: outputs {res['outputs_reached']}, R_s min {res['R_s_reached_min']}, narrow maxima {res['narrow_maxima_total_reached']}, "
          f"stopped at t = {ck['t']:.4f} TU (step {ck['steps']})")
print("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
