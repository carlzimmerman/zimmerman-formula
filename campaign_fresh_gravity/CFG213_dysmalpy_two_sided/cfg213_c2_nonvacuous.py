#!/usr/bin/env python3
"""CFG213 POST HOC (CFG234's finding, 8222db057, relayed by the orchestrator 2026-09-30; written after the frozen numbers were seen; reported only).
This lane's C2 ('a synthetic galaxy placed exactly on each law returns delta = 0 to 1e-12') sets Dexact = nu1(nu, gb / a0) and compares it with nu1(nu, gb / a0): log10(x/x) = 0 by
construction, so it cannot fail.  Replacement (non-vacuous): synthetic galaxies are placed exactly on each law THROUGH THE LANE'S OWN INPUT FIELDS (f_DM, R_e, sigma_0 and V_rot
for the z ~ 5 bin, V_c for the z ~ 1.4 bin: f_DM = 1 - 1/nu, then V solved from g_bar = (1 - f_DM) V_c,ad^2 / R_e) and passed through the lane's galaxy_rows() and deltas();
2 kernels x 2 footings x 2 laws x 2 bins x 5 z x 5 g_bar/a0; every on-law row must give |delta| < 1e-9 and the OTHER law must give |delta| > 1e-3 for >= 90% of the rows.  MUTATE=1
(the lane's D x 1.5) must make the control FAIL (max |delta| >= 0.17).
Run: python3 campaign_fresh_gravity/CFG213_dysmalpy_two_sided/cfg213_c2_nonvacuous.py
"""
import os, sys, io, math, contextlib
sys.dont_write_bytecode = True
import numpy as np

LANE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(LANE, "cfg213_two_sided.py")
src = open(path).read()
MUT = os.environ.get("MUTATE", "").strip() == "1"
ns = {"__file__": path, "__name__": "cfg213"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("BINS = {")], "cfg213", "exec"), ns)
galaxy_rows, deltas, KER, A0F, E, nu1, G2SI = (ns[k] for k in ("galaxy_rows", "deltas", "KER", "A0F", "E", "nu1", "G2SI"))
out = []


def P(s=""):
    print(s); out.append(s)


P(__doc__.split("Run:")[0].strip())
RE, S0 = 3.0, 10.0
dmax, other, n = 0.0, [], 0
for bname, zs in (("Z5", (4.4, 4.8, 5.2, 5.5, 5.7)), ("Z1.4", (1.1, 1.3, 1.4, 1.5, 1.7))):
    for kname, nu in KER.items():
        for foot in A0F:
            for law in ("flat", "rival"):
                for zz in zs:
                    for y in (0.03, 0.3, 1.0, 3.0, 30.0):
                        a0 = A0F[foot] * (E(zz) if law == "rival" else 1.0)
                        nuv = nu1(nu, y)
                        fdm = 1 - 1 / nuv
                        gbar = y * a0
                        vc2_ad_over = gbar * RE / (G2SI * (1 - fdm))              # V_c,ad^2 = g_bar R_e / (G2SI (1 - f_DM)), (km/s)^2
                        if bname == "Z5":
                            v2 = vc2_ad_over - 3.36 * S0 ** 2                      # V_c,ad^2 = V_rot^2 + 3.36 sigma_0^2
                            if v2 <= 0:
                                continue
                            g = dict(id="syn", z=zz, fdm=fdm, Re=RE, sig0=S0, Vrot=math.sqrt(v2), cls="")
                        else:
                            g = dict(id="syn", z=zz, fdm=fdm, Re=RE, sig0=S0, Vc=math.sqrt(vc2_ad_over), cls="")
                        rows = galaxy_rows(bname, [g], alpha=3.36, route=False, mutate=MUT)
                        d_own = float(deltas(rows, law, foot, nu)[0]); d_oth = float(deltas(rows, "rival" if law == "flat" else "flat", foot, nu)[0])
                        dmax = max(dmax, abs(d_own)); other.append(abs(d_oth)); n += 1
frac = float(np.mean(np.array(other) > 1e-3))
P(f"\n  {n} synthetic galaxies placed on a law through f_DM, R_e, sigma_0 and V_rot / V_c, scored by the lane's galaxy_rows() and deltas()")
ok = True
if not MUT:
    a, b = dmax < 1e-9, frac >= 0.90
    P(f"  {'PASS' if a else 'FAIL'}  C2' every on-law row returns |delta| < 1e-9: max |delta| {dmax:.2e}")
    P(f"  {'PASS' if b else 'FAIL'}  C2'-sensitivity: scored under the OTHER law, >= 90 % of the rows have |delta| > 1e-3: {100 * frac:.0f} %")
    ok = a and b
else:
    ok = dmax >= 0.17
    P(f"  {'PASS' if ok else 'FAIL'}  MUTATE: D x 1.5 makes the non-vacuous C2' FAIL (max |delta| >= 0.17): max |delta| {dmax:.3f}")
open(os.path.join(LANE, "cfg213_c2_nonvacuous" + ("_MUTATE" if MUT else "") + ".out"), "w").write("\n".join(out) + "\n")
sys.exit(0 if ok else 1)
