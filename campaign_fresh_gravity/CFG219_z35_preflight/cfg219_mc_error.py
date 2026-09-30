#!/usr/bin/env python3
"""CFG219 POST HOC (written after the first forecast numbers were seen; reported only): the Monte Carlo error of the forecast.
Re-runs the primary pairs (FLAT vs H(z), FLAT vs HORIZON), nu_mono, canonical footing, S6 inputs, at R_e and at R_out, N = 6 / 13 / 20 and tau = 0 / 0.25, ten times with different
random streams (the forecast function of cfg219_preflight.py exec'd read-only through its definitions, 500 mocks each); reports the mean and the standard deviation over the ten
reseeds of the frozen n_sigma (median over mocks of |median delta| / bootstrap sd, min over the two directions) and of the post hoc n_tot = |mu| / sd over mocks.
Run: python3 campaign_fresh_gravity/CFG219_z35_preflight/cfg219_mc_error.py   (about 3 minutes)
"""
import os, sys, io, contextlib, json
sys.dont_write_bytecode = True
import numpy as np

LANE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(LANE, "cfg219_preflight.py")
src = open(path).read()
ns = {"__file__": path, "__name__": "cfg219"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ------------------------------------------------------------------------------------------------ the per-disc table")], "cfg219", "exec"), ns)
forecast, S6, K, A0S = ns["forecast"], ns["S6"], ns["K"], ns["A0S"]
S6o = ns["make_base"](ns["cristal_rows"](), radius="Rout")
out, lines = {}, [__doc__.split("Run:")[0].strip(), ""]
for lab, base in (("R_e", S6), ("R_out", S6o)):
    for (a, b) in (("FLAT", "H(z)"), ("FLAT", "HORIZON")):
        for N in (6, 13, 20):
            for tau in (0.0, 0.25):
                ns_, nt = [], []
                for seed in range(10):
                    rng = np.random.default_rng(9000 + seed)
                    f1 = forecast(base, N, tau, a, b, K.nu_mono, A0S["canonical"], rng)
                    f2 = forecast(base, N, tau, b, a, K.nu_mono, A0S["canonical"], rng)
                    ns_.append(min(f1["zmed"], f2["zmed"]))
                    nt.append(min(abs(f1["mu"]) / f1["sd_mock"], abs(f2["mu"]) / f2["sd_mock"]))
                out[f"{lab} {a}-{b} N={N} tau={tau}"] = (float(np.mean(ns_)), float(np.std(ns_)), float(np.mean(nt)), float(np.std(nt)))
                lines.append(f"{lab} {a}-{b} N={N} tau={tau}".ljust(36) + f" n_sigma {np.mean(ns_):5.2f} +- {np.std(ns_):.2f}   n_tot {np.mean(nt):5.2f} +- {np.std(nt):.2f}   (mean +- sd over 10 reseeds)")
mx = max(v[1] for v in out.values()), max(v[3] for v in out.values())
lines.append(f"\nlargest sd over the reseeds: n_sigma {mx[0]:.2f}, n_tot {mx[1]:.2f}")
print("\n".join(lines))
open(os.path.join(LANE, "cfg219_mc_error.out"), "w").write("\n".join(lines) + "\n")
json.dump(out, open(os.path.join(LANE, "cfg219_mc_error.json"), "w"), indent=1)
