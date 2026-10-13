#!/usr/bin/env python3
"""CFG654 POST-FREEZE diagnostic for gate V-N1 (which failed as frozen: max dev 0.041 at k ~ 0.1).
The frozen check compared the binned measured ratio with the predicted ratio at the bin's mean k. The native spectrum (CAMB) has
baryon wiggles; the inherited one (EH no-wiggle) has none, so the ratio oscillates inside a bin.  Here the prediction is averaged
over the grid modes of each bin with the SAME seed's white-noise amplitudes |w_k|^2 (exact for the 1LPT field up to CIC/shot noise).
Reported only; the V-N1 label stays as frozen.  python3 cfg654_vn1_diag.py [_cmb] -> cfg654_vn1_diag[_cmb].out/.json
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, glob, math, importlib.util
SFX = sys.argv[1] if len(sys.argv) > 1 else ""; assert SFX in ("", "_cmb")
JOB, PRE = ("VNcs", "cfg654cmb_") if SFX else ("VNs", "cfg654nat_")
import numpy as np
from scipy import fft as sfft
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
sp = importlib.util.spec_from_file_location("ics", os.path.join(HERE, "cfg654_ics.py")); ics = importlib.util.module_from_spec(sp); sp.loader.exec_module(ics)
T = np.load(os.path.join(HERE, f"cfg654_ics_tables{SFX}.npz")); inh = ics.inherited()
VNs = json.load(open(glob.glob(os.path.join(EXT, "cfg654_work", JOB, PRE + "*_S0_*.json"))[0]))
VLs = json.load(open(glob.glob(os.path.join(EXT, "cfg596_work", "VLs", "cfg596_S0_*.json"))[0]))
L, N, NSEED = 100.0, 256, 512
rng = np.random.default_rng(359)
wk = sfft.rfftn(rng.standard_normal((NSEED,) * 3), workers=2) / NSEED ** 1.5
ix = np.concatenate([np.arange(0, N // 2), np.arange(NSEED - N // 2, NSEED)])
w2 = np.abs(wk[ix][:, ix][:, :, :N // 2 + 1]) ** 2; del wk
k1 = 2 * np.pi * np.fft.fftfreq(N, d=L / N); kz = 2 * np.pi * np.fft.rfftfreq(N, d=L / N)
kk = np.sqrt(k1[:, None, None] ** 2 + k1[None, :, None] ** 2 + kz[None, None, :] ** 2)
wt = np.full(kk.shape, 2.0); wt[..., 0] = 1.0; wt[..., -1] = 1.0; wt[0, 0, 0] = 0
Pn = np.exp(np.interp(np.log(np.maximum(kk, 1e-4)), np.log(T["kh"]), np.log(T["P_zi"]))); Pi = inh["P0"](kk) * inh["Dg"](1 / 50.0) ** 2
kf = 2 * np.pi / L; edges = np.arange(0.5, N // 2 + 1, 1.0) * kf; ib = np.digitize(kk.ravel(), edges)
num = np.bincount(ib, weights=(wt * w2 * Pn).ravel(), minlength=len(edges) + 1)[1:len(edges)]
den = np.bincount(ib, weights=(wt * w2 * Pi).ravel(), minlength=len(edges) + 1)[1:len(edges)]
k = np.array(VNs["snap"]["zi"]["k"]); meas = np.array(VNs["snap"]["zi"]["P"]) / np.array(VLs["snap"]["zi"]["P"])
pred = (num / den)[:len(k)]; m = k <= 1.0
dev = float(np.max(np.abs(meas[m] / pred[m] - 1)))
out = dict(max_dev_mode_averaged=dev, k=k[m].tolist(), meas=meas[m].tolist(), pred_mode_avg=pred[m].tolist(), label="POST-FREEZE diagnostic; V-N1 stays FAIL-as-frozen")
s = f"[{JOB}] V-N1 POST-FREEZE diagnostic: prediction averaged over each bin's modes with the seed's |w|^2: max |meas/pred - 1| (k <= 1) = {dev:.4f}; first bins " + \
    "; ".join(f"k {a:.3f}: meas {b:.4f} pred {c:.4f}" for a, b, c in list(zip(k[m], meas[m], pred[m]))[:6])
print(s); open(os.path.join(HERE, f"cfg654_vn1_diag{SFX}.out"), "w").write(s + "\n"); json.dump(out, open(os.path.join(HERE, f"cfg654_vn1_diag{SFX}.json"), "w"), indent=1)
