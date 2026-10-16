"""Diagnostic (POST-HOC, not a verdict): framework-native catchment retention for the 76 CFG813 clusters.
Gas = the harness's beta-model (rho ~ r^-2 at large r) EXTENDED beyond its 3 Mpc truncation out to the framework's own
turnaround radius r_ta (CFG654 native Delta_ta(z)); catchment bc = gas(<r_ta) + M_cond (lambda masses); fixed point
M_ta = bc/f_b.  'Retained' = what the harness models as the system (gas < 3 Mpc + condensed).  f_eff = retained / bc."""
import os, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
EXT = os.path.abspath(os.path.join(LANES, "..", "..", "_external_data"))
d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
lam = np.array(json.load(open(os.path.join(EXT, "cfg726_work", "lambda.json")))["lam"], float); SEL = np.where(lam > 0)[0]
DT = json.load(open(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_delta_ta.json")))
dta = lambda z: float(np.interp(z, DT["z"], DT["D"]))
h = 0.6736; FB = 0.02237 / (0.02237 + 0.1200); OM = (0.02237 + 0.1200) / h ** 2
RHOM0 = OM * 2.775e11 * h ** 2                                     # Msun / Mpc^3 (physical at z=0)
MPC = 3.0857e22
out = []
for i in SEL:
    R5, mgas, z = float(d["R500"][i]), float(d["mg"][i]), float(d["z"][i])
    r = np.logspace(-3, np.log10(60), 6000); rc = 0.15 * R5; sh = (1 + (r / rc) ** 2) ** -1.0          # NOT truncated
    dm = 4 * np.pi * r ** 2 * sh; Mm = np.r_[0, np.cumsum(0.5 * (dm[1:] + dm[:-1]) * np.diff(r))]
    Mm *= mgas / np.interp(R5, r, Mm)
    M3 = float(np.interp(3.0, r, Mm)); Mc = lam[i] * 10 ** 10.7
    rta = 5.0
    for _ in range(100):
        bc = float(np.interp(rta, r, Mm)) + Mc; Mta = bc / FB
        rn = (3 * Mta / (4 * math.pi * dta(z) * RHOM0 * (1 + z) ** 3)) ** (1 / 3)
        if abs(rn - rta) < 1e-6: break
        rta = 0.5 * (rta + rn)
    feff = (M3 + Mc) / bc
    out.append((math.log10(mgas), rta, rta / (R5 / 1.0), feff))
o = np.array(out)
print(f"76 clusters: r_ta {np.median(o[:,1]):.1f} Mpc (median; {o[:,1].min():.1f}-{o[:,1].max():.1f}), r_ta/R500 {np.median(o[:,2]):.1f}")
print(f"  f_eff = retained(<3 Mpc + stars) / catchment(<r_ta): median {np.median(o[:,3]):.3f}  (range {o[:,3].min():.2f}-{o[:,3].max():.2f})")
for q in (0.25, 0.5, 0.75):
    print(f"  quantile {q}: {np.quantile(o[:,3], q):.3f}")
print("  data-implied effective retention (CFG813 reading): ~0.65-0.75; census at these masses: 0.90; accidental pin: 0.60")
