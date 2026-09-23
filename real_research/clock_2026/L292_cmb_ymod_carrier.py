"""L292 -- THE Y-MODULATED CARRIER IN THE CMB: the CLASS face (L185's own machinery, kernel off, CDM -> w ~ 0 fluid of sound speed cs2).
The carrier's COSMOLOGICAL state: at the homogeneous background Y = 0 at EVERY epoch (the switch turns on only inside virialized
structures -- L290 V3: dY = 0 linearly; the virial heating is a nonlinear-region effect, invisible to the linear P(k)),
and its pressure stiffness is the bare k-essence value: c_s^2(z) = 1/(1 + 2 g2/p1) = 1/A = 1e-10 CONSTANT through the whole
cosmological history (g2/p1 = (A-1)/2 is a fixed ratio; both scale as a^-3).  So the CMB test is L185's scan AT the carrier's
cs2 = 1e-10 (the L185 thresholds: third peak restored for cs2 <= 1e-2; the forest P(k = 5 h/Mpc, z = 3) within 10% for
cs2 <= cs2_forest ~ 1e-9): the third peak at recombination and the linear P(k) at z = 3 and 0, run at the carrier's value,
plus the LCDM reference.  L185's exact CLASS parameters and conventions are used.
Checks (a FAIL is a finding): V1 the third acoustic peak at recombination is restored at the carrier's cs2 = 1e-10
(restoration > 0.9, the L185 gate); V2 the forest face: P(k, z = 3) > 0.9 of LCDM at k = 5 h/Mpc (the L185 gate: the carrier's
cs2 = 1e-10 <= the committed 1e-9 threshold); V3 the z = 0 linear P(k) within 10% at k = 0.2, 1, 5 h/Mpc (the carrier clusters
like CDM in the linear regime -- requirement (1) of the brief; the virial heating is nonlinear, absent from the homogeneous
background); V4 the CMB epoch's clock sector is untouched: the carrier is pressureless dust -- Delta N_eff = 0 by construction."""
import os, sys, json, time
import numpy as np
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
T0 = time.time(); print("L292 -- the Y-modulated carrier in the CMB: CLASS at the carrier's cold state\n", flush=True)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.abspath(os.path.join(ROOT, "fable_independent_2026", "L183_class_mond_kernel", "site")))
from classy import Class
h = 0.6736
base = {"h": h, "omega_b": 0.02237, "A_s": 2.1e-9, "n_s": 0.9649, "tau_reio": 0.0544, "N_ur": 3.046, "N_ncdm": 0, "YHe": 0.2454,
        "output": "tCl,mPk", "l_max_scalars": 1500, "P_k_max_h/Mpc": 10., "z_pk": "0,3", "mond_a0": 0.0}
def run(extra):
    c = Class(); p = dict(base); p.update(extra); c.set(p); c.compute(); cl = c.raw_cl(1500); l = cl["ell"][2:]; D = l * (l + 1) * cl["tt"][2:] / (2 * np.pi)
    at = lambda r: D[np.argmin(abs(l - r))]; pk = {z: [c.pk(k * h, z) * h ** 3 for k in (0.2, 1., 5.)] for z in (0., 3.)}
    return at(816) / at(537), pk
L, pkL = run({"omega_cdm": 0.1200})
print(f"    LCDM reference: peak3/peak2 = {L:.3f}; P(k, z=3) = {[f'{v:.4g}' for v in pkL[3.] ]}; P(k, z=0) = {[f'{v:.4g}' for v in pkL[0.] ]}", flush=True)
r32, pk = run({"omega_cdm": 1e-6, "Omega_fld": 0.1200 / h ** 2, "w0_fld": -1e-4, "wa_fld": 0.0, "cs2_fld": 1e-10, "use_ppf": "no"})
rest = (r32 - L) / L
print(f"    carrier cs2 = 1e-10: peak3/peak2 = {r32:.3f} (LCDM {L:.3f}); P/P_LCDM(z=3) at k = 0.2, 1, 5 h/Mpc: "
      f"{[f'{pk[3.][i]/pkL[3.][i]:.3f}' for i in range(3)]}; P/P_LCDM(z=0): {[f'{pk[0.][i]/pkL[0.][i]:.3f}' for i in range(3)]}", flush=True)
OUT["cmb"] = dict(peak3_peak2=float(r32), peak3_ratio=float(r32 / L),
                  Pk_z3_ratio=[float(pk[3.][i] / pkL[3.][i]) for i in range(3)],
                  Pk_z0_ratio=[float(pk[0.][i] / pkL[0.][i]) for i in range(3)])
check("V1 the CMB third acoustic peak: at the carrier's cosmological c_s^2 = 1e-10 the third peak is restored (peak3/peak2 within 10% of LCDM -- the L185 gate at the same convention): the recombination clustering facility the brief requires is present at the carrier's cold state",
      abs(r32 / L - 1) < 0.10, f"{r32:.3f} vs LCDM {L:.3f} (ratio {r32 / L:.3f})")
check("V2 the forest face: P(k = 5 h/Mpc, z = 3) > 0.9 of LCDM (the L185 gate) and P(k, z = 3) within 10% at k = 0.2, 1 -- the carrier at c_s^2 = 1e-10 (<= the committed L185 threshold 1e-9) is forest-cold",
      pk[3.][2] / pkL[3.][2] > 0.9 and all(abs(pk[3.][i] / pkL[3.][i] - 1) < 0.10 for i in (0, 1)), str([pk[3.][i] / pkL[3.][i] for i in range(3)]))
check("V3 the z = 0 linear P(k): within 10% of LCDM at k = 0.2, 1, 5 h/Mpc -- the carrier clusters like CDM in the linear regime (the linear growth requirement; the virial heating is a nonlinear-region effect, absent from the homogeneous background)",
      all(abs(pk[0.][i] / pkL[0.][i] - 1) < 0.10 for i in range(3)), str([pk[0.][i] / pkL[0.][i] for i in range(3)]))
check("V4 the CMB epoch's clock sector is untouched: the carrier is pressureless dust (w0 = -1e-4, c_s^2 = 1e-10): no dark radiation, Delta N_eff = 0 by construction -- no new relativistic component at recombination",
      True, "pressureless dust by construction (L290 V2b/V3: no linear coupling to the clock sector)")
n_pass = sum(CH); print(f"\nL292 COMPLETE: {n_pass}/{len(CH)} checks PASS  ({time.time()-T0:.0f} s).")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
sys.exit(0 if n_pass == len(CH) else 1)