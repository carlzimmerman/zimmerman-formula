#!/usr/bin/env python3
"""CFG632 POST-FREEZE diagnostic (no verdict weight): the frozen fit puts the host log-normal width at the upper edge of the
authors' BCEmu prior (sigma_host = 1.0).  Re-fit the census PRIMARY and the two MUTATE controls with the authors' wider HMcode
host prior sigma_host in [0.2, 2.0] (mu_host in [4, 6] unchanged), both footings.  Also the census PRIMARY with the MW halo
marginalised over a flat [30, 80] prior.
  nice -n 10 python3 -I cfg632_diag_hostprior.py -> cfg632_diag_hostprior.out / .json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import json, math, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cfg632_fit as F  # noqa: E402
OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
say("CFG632 post-freeze diagnostic (no verdict weight). kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
dm, z, _ = F.load_sample()
res = {}
# (1) wide host-width prior
F.SH = np.linspace(0.2, 2.0, 61)
MUg, SHg = np.meshgrid(F.MU, F.SH, indexing="ij"); F.MUf, F.SHf = MUg.ravel(), SHg.ravel()
hm = F.host_matrices(dm, z)
for foot in F.FOOTS:
    for mode in ("census", "one", "dep"):
        f = F.fit(dm, z, f"{foot}|{mode}|lo|H|DIFF", hm)
        say(f"wide host prior s<=2  {foot:9s} {mode:6s} lnA {f['m']:+.3f} ({f['p16']:+.3f}, {f['p84']:+.3f})  Z {f['Z']:+.2f}  host best {f['host_best']}")
        res[f"wide|{foot}|{mode}"] = f
# (2) MW halo marginalised over flat [30, 80] (frozen host prior restored)
F.SH = np.linspace(0.2, 1.0, 33)
MUg, SHg = np.meshgrid(F.MU, F.SH, indexing="ij"); F.MUf, F.SHf = MUg.ravel(), SHg.ravel()
for foot in F.FOOTS:
    key = f"{foot}|census|lo|H|DIFF"; LLs = []
    for mwh in np.arange(30.0, 80.01, 5.0):
        hmw = F.host_matrices(dm, z, mwh)
        LLs.append(F.loglike_grid(dm, z, F.mean_dm(z), F.sig_interp(key, z), hmw, mwh))
    LL = np.stack(LLs)                     # (mwh, lnA, host)
    mx = LL.max(); P = np.exp(LL - mx).sum(axis=(0, 2)); P /= P.sum(); c = np.cumsum(P)
    q = lambda p: float(np.interp(p, c, F.LNA))
    m, lo, hi = q(0.5), q(0.16), q(0.84)
    Pm = np.exp(LL - mx).sum(axis=(1, 2)); Pm /= Pm.sum()
    say(f"MW halo marginalised [30, 80]  {foot:9s} census lnA {m:+.3f} ({lo:+.3f}, {hi:+.3f})  Z {F.zscore(m, lo, hi):+.2f}; "
        f"MW-halo posterior mean {float(np.sum(Pm * np.arange(30.0, 80.01, 5.0))):.1f}")
    res[f"mwmarg|{foot}"] = dict(m=m, p16=lo, p84=hi, Z=F.zscore(m, lo, hi))
json.dump(res, open(HERE / "cfg632_diag_hostprior.json", "w"), indent=1, default=float)
open(HERE / "cfg632_diag_hostprior.out", "w").write("\n".join(OUT) + "\n")
