#!/usr/bin/env python3
"""CFG658 CL3 stage 1 (FROZEN_CRITERIA.md): CFG652's per-group model ESDs recomputed with the kernel swapped to the CFG695 law
nu_s(y) = 1/2 + sqrt(1/4 + 1/y)  (g_N = g^2/(g + a0)).  cfg652_model.py is imported read-only; the ONLY change is M.NU.
PRIMARY variant x1 only (declared), models (a) condensed source and (b) all baryons, both footings.
MUTATE control (always run first): 5 groups recomputed with the stored kernel must equal the stored CFG652 models (1e-9 rel).
Writes ../../../_external_data/cfg658_work/cfg658_cl3_models.npz.   Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg658_cl3_models.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, time, json
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
L652 = os.path.join(LANES, "CFG652_hot_group_discriminator"); sys.path.insert(0, L652)
WORK652 = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg652_work"))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg658_work"))
try:
    os.nice(10)
except OSError:
    pass
import cfg652_model as M                                                    # noqa: E402  (read-only)
NU_STORED = M.NU


def nu_s(y, newton=False):
    if newton:
        return np.ones_like(y)
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


RB = np.geomspace(30, 3000, 13); RC = np.sqrt(RB[1:] * RB[:-1]); NB = len(RC)        # = cfg652_test.py
I = np.load(os.path.join(WORK652, "cfg652_inputs.npz")); MD = np.load(os.path.join(WORK652, "cfg652_models.npz"))
n = len(I["z"]); T0 = time.time()
LOG = []


def P(s):
    print(s, flush=True); LOG.append(s)


def one(i, foot, model):
    o = M.system(I["Mcond"][i], I["Mhot"][i], I["Rx_kpc"][i], I["z"][i], foot, model, N=600, gas_trunc=2.0)
    return M.delta_sigma(o["rg"], o["Mbound"], RC, rmax=o["rta"])


# MUTATE control: stored kernel reproduces the stored models
M.NU = NU_STORED
ok_idx = [i for i in range(n) if I["Mcond"][i] > 0][:5]
dmax = 0.0
for foot in ("canonical", "alt"):
    for model in "ab":
        ref = MD[f"{foot}__x1__{model}"]
        for i in ok_idx:
            dmax = max(dmax, float(np.max(np.abs(one(i, foot, model) / ref[i] - 1))))
P(f"M-K control: 5 groups x 2 footings x 2 models with the stored kernel vs stored CFG652 models: max rel {dmax:.2e} -> "
  f"{'PASS' if dmax <= 1e-9 else 'FAIL'} ({time.time() - T0:.0f} s)")
# kernel swap
M.NU = nu_s
out = {}
for foot in ("canonical", "alt"):
    for model in "ab":
        arr = np.full((n, NB), np.nan)
        for i in range(n):
            if I["Mcond"][i] <= 0:
                continue
            arr[i] = one(i, foot, model)
        out[f"{foot}__x1__{model}"] = arr
        P(f"  nu_s models {foot} x1 {model} done ({time.time() - T0:.0f} s)")
np.savez(os.path.join(WORK, "cfg658_cl3_models.npz"), **out)
json.dump(dict(mutate_control_maxrel=dmax, ok=dmax <= 1e-9, groups_checked=ok_idx), open(os.path.join(HERE, "cfg658_cl3_models.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg658_cl3_models.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if dmax <= 1e-9 else 1)
