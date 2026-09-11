#!/usr/bin/env python3
"""L183 -- THE CMB WITH THE KERNEL ON, in a full Boltzmann code (patched CLASS 3.3.4.0, ./L183_class_mond_kernel, mean-field
Phi = Psi = nu(g_rms/a0) Phi_N, prescription A on the peculiar field, sub-horizon modes only, nu capped at 20). Runs (Newtonian gauge):
A LCDM kernel off (validation vs stock synchronous CLASS); B no-CDM smooth dust (omega_cdm -> 0, Omega_fld = Omega_c, w0 = -1e-4, cs2 = 1,
the L129/L165 setup) kernel off; C/D = B + kernel canonical/alt for z > 30; E = B + kernel canonical at all epochs; F = LCDM + kernel z > 30.
Statistic: D_l peak positions and ratios peak2/peak1, peak3/peak2. No literal-True checks."""
import sys, os, numpy as np
sys.path.insert(0, os.path.abspath("L183_class_mond_kernel/site"))
from classy import Class
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
h = 0.6736; base = {"h": h, "omega_b": 0.02237, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046, "N_ncdm": 0, "YHe": 0.2454,
                    "output": "tCl", "l_max_scalars": 1500, "mond_As": 2.1e-9, "mond_ns": 0.9649, "mond_kpivot": 0.05}
LCDM = {"omega_cdm": 0.1200}; NOCDM = {"omega_cdm": 1e-6, "Omega_fld": 0.1200/h**2, "w0_fld": -1e-4, "wa_fld": 0.0, "cs2_fld": 1.0, "use_ppf": "no"}
def peaks(l, D, w=40):
    p = []
    for j in range(w, len(D) - w):
        if D[j] >= D[j-w:j+w+1].max() and 120 < l[j] < 1300: p.append((int(l[j]), D[j]))
    return p[:3]
def run(label, extra, gauge="newtonian", a0=0.0, zmin=30.0):
    c = Class(); p = dict(base); p.update(extra); p["gauge"] = gauge; p["mond_a0"] = a0; p["mond_zmin"] = zmin
    c.set(p); c.compute(); cl = c.raw_cl(1500); l = cl["ell"][2:]; D = l*(l + 1)*cl["tt"][2:]/(2*np.pi); pk = peaks(l, D)
    r21 = pk[1][1]/pk[0][1] if len(pk) > 1 else np.nan; r32 = pk[2][1]/pk[1][1] if len(pk) > 2 else np.nan
    print(f"    {label:<40} peaks l = {[q[0] for q in pk]}  peak2/peak1 = {r21:.3f}  peak3/peak2 = {r32:.3f}", flush=True)
    return pk, r21, r32, D, l
print("=" * 112 + "\nL183 CMB WITH THE KERNEL ON (patched CLASS, mean-field, prescription A)\n" + "=" * 112)
S = run("stock CLASS, LCDM (synchronous)", LCDM, gauge="synchronous")
A = run("A  LCDM, kernel off (newtonian)", LCDM)
check("V1 the Newtonian-gauge run reproduces stock synchronous CLASS: peak positions within 1% and peak3/peak2 within 1%",
      all(abs(A[0][i][0]/S[0][i][0] - 1) < 0.01 for i in range(3)) and abs(A[2]/S[2] - 1) < 0.01, f"A {[q[0] for q in A[0]]} {A[2]:.3f} vs stock {[q[0] for q in S[0]]} {S[2]:.3f}")
B = run("B  no CDM, smooth dust, kernel off", NOCDM)
check("V2 control: smooth dust reproduces the L129/L165 third-peak deficit (peak3/peak2 = 0.55 +/- 0.10 vs 0.99)", abs(B[2] - 0.5545) < 0.10 and B[2] < 0.75, f"B peak3/peak2 = {B[2]:.3f}")
C = run("C  no CDM + kernel canonical, z > 30", NOCDM, a0=9.3619e-11)
D_ = run("D  no CDM + kernel alt, z > 30", NOCDM, a0=1.1279e-10)
E = run("E  no CDM + kernel canonical, all z", NOCDM, a0=9.3619e-11, zmin=0.0)
F = run("F  LCDM + kernel canonical, z > 30", LCDM, a0=9.3619e-11)
def fixed(v):   # peak ratios at LCDM's own peak multipoles (the kernel's low-l ramp defeats a free peak finder)
    l = v[4]; D = v[3]; i1, i2, i3 = [np.argmin(abs(l - r)) for r in (221, 537, 816)]; return D[i2]/D[i1], D[i3]/D[i2]
def lowl(v, ref=A):
    l = v[4]; return [v[3][np.argmin(abs(l - r))]/ref[3][np.argmin(abs(l - r))] for r in (30, 60, 100, 221, 537, 816)]
print("    fixed-multipole ratios (537/221, 816/537): " + ", ".join(f"{k} {fixed(v)[0]:.3f}/{fixed(v)[1]:.3f}" for k, v in (("A", A), ("B", B), ("C", C), ("D", D_), ("E", E), ("F", F))))
print("    D_l / D_l(LCDM) at l = 30, 60, 100, 221, 537, 816: " + "; ".join(f"{k} " + " ".join(f"{x:.2f}" for x in lowl(v)) for k, v in (("B", B), ("C", C), ("F", F))))
rest = {k: (fixed(v)[1] - fixed(B)[1])/(fixed(A)[1] - fixed(B)[1]) for k, v in (("C", C), ("D", D_), ("E", E))}
print("    restoration of the third peak at fixed l (0 = smooth-dust deficit, 1 = LCDM): " + ", ".join(f"{k}: {v:+.2f}" for k, v in rest.items()))
check("V3 [THE QUESTION, DEFICIT verified] with no CDM and the kernel on, peak3/peak2 at fixed l stays at the smooth-dust value (0.56 vs LCDM 0.99, restoration within +/-0.05 of zero) on both footings: the kernel does NOT replace cold dark matter at recombination",
      all(abs(rest[k]) < 0.05 for k in ("C", "D")), f"C {fixed(C)[1]:.3f}, D {fixed(D_)[1]:.3f}, B {fixed(B)[1]:.3f}, LCDM {fixed(A)[1]:.3f}")
check("V4 [reason] on the peak scales the kernel is in its Newtonian regime: with CDM present it changes the 221/537/816 amplitudes by less than 5%", all(abs(x - 1) < 0.05 for x in lowl(F)[3:]), "F at 221/537/816: " + " ".join(f"{x:.3f}" for x in lowl(F)[3:]))
check("V5 [DEFICIT verified] prescription A adds a low-multipole catastrophe: D_l at l = 30-100 is boosted 5-500x over LCDM with or without CDM (deep-MOND regime of large-scale potentials), which Planck excludes outright",
      all(min(lowl(v)[:3]) > 5 for v in (C, F)), "C/F at 30,60,100: " + " ".join(f"{x:.0f}" for x in lowl(C)[:3]) + " / " + " ".join(f"{x:.0f}" for x in lowl(F)[:3]))
print("    LIMITS: mean-field kernel (nu of the mode's rms envelope acceleration; no mode coupling), prescription A on the peculiar field for sub-horizon modes,\n"
      "    nu capped at 20; smooth-dust background as in L129 (w0 = -1e-4, cs2 = 1); Newtonian gauge; no lensing; raw C_l.")
np.savez("L183_Dl.npz", **{k: v[3] for k, v in (("S", S), ("A", A), ("B", B), ("C", C), ("D", D_), ("E", E), ("F", F))}, ell=A[4])
print(f"\nL183 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
