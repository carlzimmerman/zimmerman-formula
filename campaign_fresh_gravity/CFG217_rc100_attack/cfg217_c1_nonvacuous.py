#!/usr/bin/env python3
"""CFG217 POST HOC (the referee's item on CFG216's C1, applied to this lane; 2026-09-30; written after the frozen numbers were seen; reported only).
This lane's C1 ('a synthetic galaxy placed exactly on each law returns delta = 0') is written the same way as CFG216's: log10 of nu(x)/nu(x) at identical arguments, so it cannot
fail.  This script replaces it with a NON-VACUOUS control: synthetic table rows are placed exactly on each law (flat and rival, nu_mono, canonical footing: the ones this lane
uses; 5 z x 5 g_bar/a0) by solving for the table's own observables (V_c, R_e, f_DM), written to a CSV in the RC100 six-field format, read by the lane's actual loader code
(cfg217_attack.py exec'd read-only through its data block and its function definitions, with only the input path replaced), and scored by the lane's actual delta_arr().
Every on-law row must give |delta| < 1e-9; scored under the OTHER law >= 90 % of the rows must have |delta| > 1e-3 (the control can discriminate).  MUTATE=1 passes through to the
lane's injection (D x 10^(0.2 (z - z_med))): the control must then FAIL (max |delta| >= 0.15); outputs are named *_MUTATE.
Run: python3 campaign_fresh_gravity/CFG217_rc100_attack/cfg217_c1_nonvacuous.py
"""
import os, sys, io, csv, math, tempfile, contextlib
sys.dont_write_bytecode = True
import numpy as np

LANE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(LANE, "cfg217_attack.py")
src = open(path).read()
MUT = os.environ.get("MUTATE", "").strip() == "1"
out = []


def P(s=""):
    print(s); out.append(s)


P(__doc__.split("Run:")[0].strip())
ns0 = {"__file__": path, "__name__": "cfg217"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ------------------------------------------------------------------------------------------------ data")], "cfg217_pre", "exec"), ns0)
A0, E, nu1, G2SI = (ns0[k] for k in ("A0", "E", "nu1", "G2SI"))
tags, recs = [], []
RE_KPC = 5.0
for law in ("flat", "rival"):
    for zz in (0.61, 1.0, 1.53, 2.0, 2.52):
        for y in (0.03, 0.3, 1.0, 3.0, 30.0):
            a0 = A0 * (E(zz) if law == "rival" else 1.0)
            nuv = nu1(y)
            gobs = y * a0 * nuv
            fd = 1 - 1 / nuv
            vc = math.sqrt(gobs * RE_KPC / G2SI)
            tags.append(law); recs.append(dict(name=f"{law}|z={zz}|y={y}", z=zz, Re_kpc=RE_KPC, Vc_Re_kms=vc, fDM_within_Re=fd, logMbar_Msun=11.0, sigma0_kms=100.0))
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(recs[0])); w.writeheader(); w.writerows(recs)
    SYN = f.name
src_syn = src.replace('raw = list(csv.DictReader(open(RC100_PATH, newline="")))', 'raw = list(csv.DictReader(open(SYNTH_PATH, newline="")))')
assert src_syn != src, "the loader line changed; refusing"
ns1 = {"__file__": path, "__name__": "cfg217", "SYNTH_PATH": SYN}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src_syn[:src_syn.index('R.banner("CONTROLS")')], "cfg217_syn", "exec"), ns1)
os.unlink(SYN)
z, gbar0, D0, delta_arr = (ns1[k] for k in ("z", "gbar0", "D0", "delta_arr"))
assert len(z) == len(recs), f"the loader dropped synthetic rows ({len(z)} of {len(recs)})"
tg = np.array(tags)
dmax, off = 0.0, []
for law, other in (("flat", "rival"), ("flat", "rival")[::-1]):
    sel = tg == law
    d_own = delta_arr(z[sel], D0[sel], gbar0[sel], law)
    d_oth = delta_arr(z[sel], D0[sel], gbar0[sel], other)
    dmax = max(dmax, float(np.max(np.abs(d_own)))); off.extend(np.abs(d_oth).tolist())
frac = float(np.mean(np.array(off) > 1e-3))
P(f"\n  {len(z)} synthetic table rows on the two laws, read by the lane's loader, scored by the lane's delta_arr()")
allok = True
if not MUT:
    ok1, ok2 = dmax < 1e-9, frac >= 0.90
    P(f"  {'PASS' if ok1 else 'FAIL'}  C1' every on-law row returns |delta| < 1e-9: max |delta| {dmax:.2e}")
    P(f"  {'PASS' if ok2 else 'FAIL'}  C1'-sensitivity: scored under the OTHER law, >= 90 % of the rows have |delta| > 1e-3: {100 * frac:.0f} %")
    allok = ok1 and ok2
else:
    ok = dmax >= 0.15
    P(f"  {'PASS' if ok else 'FAIL'}  MUTATE: the injected 0.2 (z - z_med) drift makes the non-vacuous C1' FAIL (max |delta| >= 0.15): max |delta| {dmax:.3f}")
    allok = ok
open(os.path.join(LANE, "cfg217_c1_nonvacuous" + ("_MUTATE" if MUT else "") + ".out"), "w").write("\n".join(out) + "\n")
sys.exit(0 if allok else 1)
