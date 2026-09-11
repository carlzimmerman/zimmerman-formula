#!/usr/bin/env python3
"""L184 -- THE CMB WITH THE KERNEL ON, CONSISTENT METRIC DERIVATIVE (answers astra's 2026-09-11 review of L183: with phi_eff = nu phi_N the
species and sources must see phi_eff' = nu phi_N' + nu' phi_N; L183 dropped nu' phi_N). Patched CLASS 3.3.4.0 (./L183_class_mond_kernel,
second patch apply_nuprime_patch.py, input mond_nuprime = 1). The nu' phi_N term is the kernel's INTRINSIC ISW: with phi_N frozen (matter
era), phi_eff'/phi_eff = (aH/2) u/(e^u - 1) in (0, aH/2] (Lean: mean_field_isw_rate_identity, mean_field_isw_rate_bounds). Runs (Newtonian):
A LCDM kernel off; F0 LCDM + kernel (nuprime 0, must reproduce L183 F); F1c/F1a LCDM + kernel consistent, both footings; F1c without the
ISW contributions; B no-CDM smooth dust; C0/C1 no-CDM + kernel canonical (nuprime 0/1). Also restates L183's low-l numbers as KERNEL-CAUSED
factors (run/baseline), which L183's V5 wording mixed with the smooth-dust baseline (astra's l = 60 point). No literal-True checks."""
import sys, os, numpy as np
sys.path.insert(0, os.path.abspath("L183_class_mond_kernel/site"))
from classy import Class
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
h = 0.6736; base = {"h": h, "omega_b": 0.02237, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046, "N_ncdm": 0, "YHe": 0.2454,
                    "output": "tCl", "l_max_scalars": 1500, "mond_As": 2.1e-9, "mond_ns": 0.9649, "mond_kpivot": 0.05, "gauge": "newtonian"}
LCDM = {"omega_cdm": 0.1200}; NOCDM = {"omega_cdm": 1e-6, "Omega_fld": 0.1200/h**2, "w0_fld": -1e-4, "wa_fld": 0.0, "cs2_fld": 1.0, "use_ppf": "no"}
LS = (2, 10, 30, 60, 100, 221, 537, 816)
def run(label, extra, a0=0.0, nuprime=0, zmin=30.0, more=None):
    c = Class(); p = dict(base); p.update(extra); p.update({"mond_a0": a0, "mond_zmin": zmin, "mond_nuprime": nuprime}); p.update(more or {})
    c.set(p); c.compute(); cl = c.raw_cl(1500); l = cl["ell"][2:]; D = l*(l + 1)*cl["tt"][2:]/(2*np.pi)
    at = lambda r: D[np.argmin(abs(l - r))]
    print(f"    {label:<46} D_l(1e10) at l={LS}: " + " ".join(f"{at(r)*1e10:.3g}" for r in LS), flush=True)
    return D, l, at
def ratio(v, ref): return [v[2](r)/ref[2](r) for r in LS]
def fmt(rs): return " ".join(f"{x:.2f}" for x in rs)
def fixed32(v): return v[2](816)/v[2](537)
print("=" * 118 + "\nL184 CMB WITH THE KERNEL ON, CONSISTENT DERIVATIVE phi_eff' = nu phi_N' + nu' phi_N (patched CLASS, mean-field, prescription A)\n" + "=" * 118)
A = run("A   LCDM, kernel off", LCDM)
F0 = run("F0  LCDM + kernel canonical, z>30, nuprime=0 (L183)", LCDM, a0=9.3619e-11)
old = np.load("L183_Dl.npz"); lo = old["ell"]; rF = [old["F"][np.argmin(abs(lo - r))]/old["A"][np.argmin(abs(lo - r))] for r in LS]
check("V1 the rebuilt binary with mond_nuprime = 0 reproduces L183's run F (kernel-caused factors at l = 2..816 within 3%)",
      all(abs(a/b - 1) < 0.03 for a, b in zip(ratio(F0, A), rF)), f"F0/A {fmt(ratio(F0, A))} vs L183 {fmt(rF)}")
F1c = run("F1c LCDM + kernel canonical, z>30, CONSISTENT", LCDM, a0=9.3619e-11, nuprime=1)
F1a = run("F1a LCDM + kernel alt, z>30, CONSISTENT", LCDM, a0=1.1279e-10, nuprime=1)
F1n = run("F1n = F1c without ISW (tsw,dop,pol only)", LCDM, a0=9.3619e-11, nuprime=1, more={"temperature contributions": "tsw,dop,pol"})
An = run("An  = A without ISW", LCDM, more={"temperature contributions": "tsw,dop,pol"})
B = run("B   no CDM, smooth dust, kernel off", NOCDM)
C0 = run("C0  no CDM + kernel canonical, z>30, nuprime=0 (L183)", NOCDM, a0=9.3619e-11)
C1 = run("C1  no CDM + kernel canonical, z>30, CONSISTENT", NOCDM, a0=9.3619e-11, nuprime=1)
print("    KERNEL-CAUSED factors D_l(run)/D_l(baseline) at l = " + str(LS))
for k, v, r in (("F0/A (L183)", F0, A), ("F1c/A", F1c, A), ("F1a/A", F1a, A), ("F1n/An (no ISW)", F1n, An), ("C0/B (L183)", C0, B), ("C1/B", C1, B)):
    print(f"      {k:<18} {fmt(ratio(v, r))}")
print(f"    peak3/peak2 at fixed l (816/537): LCDM {fixed32(A):.3f}, B {fixed32(B):.3f}, C0 {fixed32(C0):.3f}, C1 {fixed32(C1):.3f}, F1c {fixed32(F1c):.3f}")
rest = (fixed32(C1) - fixed32(B))/(fixed32(A) - fixed32(B))
check("V2 [DEFICIT verified, corrected derivative] the kernel-caused low-l excess survives the consistent nu' phi_N term: LCDM + kernel exceeds LCDM by > 5x at l = 30 on both footings",
      ratio(F1c, A)[2] > 5 and ratio(F1a, A)[2] > 5, f"F1c/A at l=30: {ratio(F1c, A)[2]:.0f}, F1a/A: {ratio(F1a, A)[2]:.0f} (L183 F0/A {ratio(F0, A)[2]:.0f})")
check("V3 [reason] the excess is ISW-borne: without the ISW contributions the l = 30 kernel-caused factor falls below 1.5",
      ratio(F1n, An)[2] < 1.5, f"F1n/An at l=30: {ratio(F1n, An)[2]:.2f} vs F1c/A {ratio(F1c, A)[2]:.0f}")
check("V4 [DEFICIT verified] with no CDM and the consistent derivative the third peak is still not restored (restoration within +/-0.05 of zero)",
      abs(rest) < 0.05, f"restoration {rest:+.2f}; C1 {fixed32(C1):.3f} vs B {fixed32(B):.3f} vs LCDM {fixed32(A):.3f}")
check("V5 [correction to L183 V5 wording] the no-CDM kernel-caused factors in L183 (C0/B) are 30x at l=30 but ~1x at l=60 (astra's point); the baseline-free line is LCDM + kernel",
      ratio(C0, B)[2] > 10 and abs(ratio(C0, B)[3] - 1) < 0.1, f"C0/B at 30,60,100: {fmt(ratio(C0, B)[2:5])}")
print("    LIMITS: mean-field kernel (no mode coupling), prescription A on the peculiar field, sub-horizon modes, nu capped at 20 (nu' = 0 on the cap),\n"
      "    envelope derivative drops the phi'' term (matters only where nu = 1); CLASS's ISW approximation phi'+psi' ~ 2 phi'; raw C_l, no lensing.")
np.savez("L184_Dl.npz", **{k: v[0] for k, v in (("A", A), ("F0", F0), ("F1c", F1c), ("F1a", F1a), ("F1n", F1n), ("An", An), ("B", B), ("C0", C0), ("C1", C1))}, ell=A[1])
print(f"\nL184 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
