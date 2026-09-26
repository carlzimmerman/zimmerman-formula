#!/usr/bin/env python3
"""M04b -- J10-I(z) cosmography at the OB1 JWST recipe (Z3-wave; owns M04b_*).
Door: M04 (register row 42) LANDED 14/14 but closed only under an ASSUMED per-object
S/N = 30 (L05 was in flight then). OB1/Z2 registered the minimal feasible config:
N = 3 objects, per-object S/N = 10, f = 20, rate 0.9998. This lane re-runs M04's own
code (loaded source, exec'd, never transcribed) at S/N = 10 and re-asks whether the
cosmography claims survive the cheap block.

Pre-registered (Z3-WAVE_BRIEF.md, fixed before any number):
 R0 control: exec M04_j10z.py UNPATCHED except the output filename -> must reproduce
    M04_results.json key scalars bit-equal (dev_days, sigma_d_days, zstat_window_z1,
    chain_zstats, zc_3sigma_window, zc_3sigma_chain). Mismatch -> exit 1 (loaded break).
 R1 patch: SN 30.0 -> 10.0 only; all SEs in M04 scale exactly as 1/SN (seA = se_d = 1/SN,
    SE_r = sqrt(2)/SN) -> sigma x3, z-stats /3.
 Gates on the S/N = 10 run (fixed):
  GA (single-object lag): dev_days/sigma_d_days >= 3 at z = 1.
  GB (window incl. atom noise): single z-stat >= 3 OR N = 3 stacked (OB1 recipe,
     same-z stack, independence assumed and stated) z-stat >= 3.
  GC (ratio chain): zc_3sigma_chain(S/N=10) <= 2.0 (inside the G237 law's z <= 3 range).
 All -> PASS-CHEAP (exit 0): the OB1 block runs cosmography. GA and GB both fail ->
 OB1-CANNOT-COSMOGRAPH (exit 1): program must book S/N = 30 blocks (L05 budget x5).
 Partial -> verdict states exactly which gates failed; exit 1 honest.
House rules 1-10 binding; leaf lane does NOT commit.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "M04_j10z.py")
KEYS = ["dev_days", "sigma_d_days", "zstat_window_z1", "chain_zstats_mrise",
        "zc_3sigma_window", "zc_3sigma_chain", "sigma_J10I_rel", "d_fw1_days", "d_mr1_days"]

RES = {"title": "M04b J10-I(z) at the OB1 recipe (S/N = 10, N = 3)",
       "pre_registration": "Z3-WAVE_BRIEF.md (R0/R1/GA/GB/GC fixed before any number)",
       "gates": {"GA_lag3sigma": 3.0, "GB_window3sigma": 3.0, "GC_chain_zc_max": 2.0}}


def run_variant(sn_value, out_name):
    src = open(SRC).read()
    if sn_value is not None:
        old = "SN   = 30.0"
        assert src.count(old) == 1, f"SN anchor not found ({src.count(old)})"
        src = src.replace(old, f"SN   = {sn_value}")
    old_out = '"M04_results.json"'
    assert src.count(old_out) >= 1
    src = src.replace(old_out, f'"{out_name}"')
    g = {"__name__": "m04b_exec", "__file__": SRC}
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            exec(compile(src, SRC, "exec"), g)
        except SystemExit:
            pass  # M04 ends with sys.exit(n_pass==n_tot); results already on disk
    out = json.load(open(os.path.join(HERE, out_name)))
    return out, buf.getvalue()


def main():
    # R0 control
    out30, _ = run_variant(None, "M04b_results_sn30_control.json")
    ref = json.load(open(os.path.join(HERE, "M04_results.json")))["measurements"]
    diffs = {k: (out30["measurements"][k], ref[k]) for k in KEYS
             if out30["measurements"][k] != ref[k]}
    RES["R0_control_bit_equal"] = (len(diffs) == 0)
    if diffs:
        RES["R0_diffs"] = {k: list(v) for k, v in diffs.items()}
        RES["verdict"] = "FAIL R0: patched-output control does not reproduce M04_results.json"
        finish(1)
    print("R0 control: S/N=30 exec reproduces M04_results.json bit-equal on", KEYS, flush=True)

    # OB1 registered config (loaded)
    ob1 = json.load(open(os.path.join(HERE, "OB1_results.json")))
    RES["ob1_config"] = {k: ob1.get(k) for k in list(ob1)[:8]}

    # R1: S/N = 10
    out10, _ = run_variant(10.0, "M04b_results_sn10.json")
    m10 = out10["measurements"]
    RES["sn10_key_values"] = {k: m10[k] for k in KEYS}
    lag_z = m10["dev_days"] / m10["sigma_d_days"]
    win_z = m10["zstat_window_z1"]
    win_z_stack3 = win_z * math.sqrt(3.0)
    zc_chain = m10["zc_3sigma_chain"]
    RES.update(lag_z_sn10=lag_z, window_z_sn10=win_z, window_z_stack3=win_z_stack3,
               zc_3sigma_chain_sn10=zc_chain)
    GA = lag_z >= 3.0
    GB = (win_z >= 3.0) or (win_z_stack3 >= 3.0)
    GC = zc_chain <= 2.0
    RES.update(GA_pass=GA, GB_pass=GB, GC_pass=GC,
               GB_mode=("single" if win_z >= 3.0 else ("stack3" if win_z_stack3 >= 3.0 else "none")))
    print(f"S/N=10: lag z = {lag_z:.2f}; window z = {win_z:.2f} (stack3 {win_z_stack3:.2f}); "
          f"3-sigma chain exclusion from z2 = {zc_chain:.3f}", flush=True)
    if GA and GB and GC:
        RES["verdict"] = ("PASS-CHEAP: the OB1 block (N=3, S/N=10, f=20) carries the cosmography "
                          "-- single-object lag 3-sigma at z=1, window 3-sigma (mode %s), "
                          "ratio-chain 3-sigma exclusion from z2 = %.3f (<= 2.0)"
                          % (RES["GB_mode"], zc_chain))
        finish(0)
    if not GA and not GB:
        RES["verdict"] = ("OB1-CANNOT-COSMOGRAPH: at S/N=10 neither the lag (z=%.2f) nor the "
                          "window (z=%.2f single / %.2f stacked) reaches 3 sigma; the program "
                          "must book S/N=30 blocks (L05 budget: x5 exposure)" % (lag_z, win_z, win_z_stack3))
        finish(1)
    RES["verdict"] = ("PARTIAL: GA=%s GB=%s GC=%s -- which gates failed is recorded verbatim "
                      "in the results file; honest exit 1" % (GA, GB, GC))
    finish(1)


def finish(rc):
    RES["exit"] = rc
    with open(os.path.join(HERE, "M04b_results.json"), "w") as f:
        json.dump(RES, f, indent=1, default=str)
    print(json.dumps({k: RES[k] for k in ("verdict", "GA_pass", "GB_pass", "GC_pass",
                                          "lag_z_sn10", "window_z_sn10", "window_z_stack3",
                                          "zc_3sigma_chain_sn10")}, indent=1))
    sys.exit(rc)


if __name__ == "__main__":
    main()
