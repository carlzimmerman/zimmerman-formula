#!/usr/bin/env python3
"""GAL1 post-freeze extras (reported only; no label rests on them). kappa = 1/2 FITTED; not theory closed. Adopts nothing.
E1: constant-f allowances switched on earlier than the frozen brackets (z_on 4, 6).
E2: what moves the allowance from SWT1's 0.0231: 2 sigma vs 3 sigma, the switch-on epoch, growth.
Executes gal1.py's definitions (up to the SWT1-readings block) read-only; one thread."""
import os, sys, io, json, math, contextlib, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "gal1.py")
src = open(SRC).read(); cut = src.index("# ------------------------------------------------------------------ SWT1 readings")
NS = {"__file__": SRC, "__name__": "gal1_reused"}
argv0, sys.argv = sys.argv, [SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:cut], SRC, "exec"), NS)
sys.argv = argv0
assert NS["KA_OK"], "known answers failed in the reused block"
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time(); RES = dict(lane="GAL1 extras (reported only)", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", E1={}, E2={})
allowance, LINE2, LINE3 = NS["allowance"], NS["LINE2"], NS["LINE3"]
fmt = lambda d: (f"{d['f_max']:.5f}" if d.get("f_max") is not None else "> 0.5")

# E1: earlier switch-on (z 4 and 6 are steps on gal1's Limber grid; the growth solve covers z <= 6.5)
for z_on in (4.0, 6.0):
    a = {k: allowance(z_on, k, "main") for k in ("lens2", "fs8", "s8", "lens3", "shear")}
    RES["E1"][str(z_on)] = a
    P(f"E1 z_on {z_on:g}: lensing 2 sigma {fmt(a['lens2'])}, f sigma8 {fmt(a['fs8'])}, S8 {fmt(a['s8'])}; lensing 3 sigma {fmt(a['lens3'])}, shear S8 {fmt(a['shear'])}")

# E2: decomposition at z_on 3 and with the boost at every z
def fq(q): return q / (1.5 + q)
e2 = dict(all_z_potential_only_3sig=fq(math.sqrt(1 + LINE3) - 1), all_z_potential_only_2sig=fq(math.sqrt(1 + LINE2) - 1))
for key in ("lens2", "lens3"):
    e2[f"zon3_potential_only_{key}"] = allowance(3.0, key, "potonly")["f_max"]
    e2[f"zon3_with_growth_{key}"] = allowance(3.0, key, "main")["f_max"]
o_m = NS["observe"](NS["const_hist"](0.0231, 3.0), "main"); o_p = NS["observe"](NS["const_hist"](0.0231, 3.0), "potonly")
e2["r_eff_at_0231_zon3"] = dict(main=o_m["r_eff"], potential_only=o_p["r_eff"], all_z_potential_only=(1 + NS["qf"](0.0231)) ** 2)
RES["E2"] = e2
P(f"E2 boost at every z, potential only: 3 sigma {e2['all_z_potential_only_3sig']:.5f} (SWT1's 0.0231), 2 sigma {e2['all_z_potential_only_2sig']:.5f}")
P(f"E2 z_on 3, potential only: 3 sigma {e2['zon3_potential_only_lens3']:.5f}, 2 sigma {e2['zon3_potential_only_lens2']:.5f}")
P(f"E2 z_on 3, with growth (main): 3 sigma {e2['zon3_with_growth_lens3']:.5f}, 2 sigma {e2['zon3_with_growth_lens2']:.5f}")
P(f"E2 r_eff at f 0.0231, z_on 3: potential only {o_p['r_eff']:.5f}, with growth {o_m['r_eff']:.5f}; boost at every z, potential only {(1 + NS['qf'](0.0231)) ** 2:.5f}")
# E3: M-SIGN as frozen did not bite on one history; re-read its output bin by bin (boost on at the bin's z or not)
MS = json.load(open(os.path.join(HERE, "gal1_MUTATE_sign.json")))["MUTATE"]["M_SIGN"]["rows"]
ZB = {t: z for (t, z, *_ ) in NS["DESI"]}; e3 = []
for r in MS:
    nm = r["history"]; z_on = float(nm.split("zon")[1]) if nm.startswith("const") else 3.0
    on = {t: v for t, v in r["Rf"].items() if ZB[t] <= z_on}; off = {t: v for t, v in r["Rf"].items() if ZB[t] > z_on}
    e3.append(dict(history=nm, bins_on=on, bins_off=off, on_all_drop=bool(all(v < 1 for v in on.values())),
                   off_max_dev=(max(abs(v - 1) for v in off.values()) if off else None), s0_drops=bool(r["s0"] < 1), r_eff_drops=bool(r["r_eff"] < 1)))
    P(f"E3 M-SIGN {nm}: bins with the boost on " + ", ".join(f"{t} {v:.4f}" for t, v in on.items()) + f" -> all drop {e3[-1]['on_all_drop']}; "
      + (f"bins before switch-on " + ", ".join(t for t in off) + f" max |Rf - 1| {e3[-1]['off_max_dev']:.1e}; " if off else "") + f"s(0) {r['s0']:.5f}, r_eff {r['r_eff']:.5f}")
RES["E3"] = dict(rows=e3, every_on_bin_drops=bool(all(x["on_all_drop"] and x["s0_drops"] and x["r_eff_drops"] for x in e3)))
P(f"E3: every bin where the boost is on drops, and s(0), r_eff drop for all {len(e3)} histories: {RES['E3']['every_on_bin_drops']}")
P(f"runtime {time.time() - T0:.0f} s. kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
json.dump(RES, open(os.path.join(HERE, "gal1_extra.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "gal1_extra.out"), "w").write("\n".join(OUT) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
