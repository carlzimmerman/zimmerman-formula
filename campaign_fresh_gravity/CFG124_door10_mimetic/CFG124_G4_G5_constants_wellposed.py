# -*- coding: utf-8 -*-
"""CFG124 G4 (constants) and G5 (well-posedness) (frozen: CFG124_FROZEN_CRITERIA.md, e8b9fbcdf).
Reads the derived results of T0 (c_s^2, ghost/gradient signs, class-D scan), G2 (gt_max window) and re-derives the E1 hyperbolicity.
MUTATE b: the G2 upper bound is replaced by 1e-6 by hand (widening the window): the 'window is empty' claim must flip.
MUTATE a/c: not used here.
"""
import os, sys, math, json
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG124_common as C
R = C.Report("CFG124_G4_G5_constants_wellposed")
P = R.P
P(__doc__)
def load(name):
    p = os.path.join(C.HERE, name)
    if not os.path.exists(p): raise SystemExit("missing %s: run the earlier scripts first" % name)
    return json.load(open(p))
T0 = load("CFG124_T0_field_equations_results.json"); G2 = load("CFG124_G2_growth_results.json")
gt_max = float(G2["numbers"]["gt_max_z10_k30"])
if C.MU("b"): gt_max = 1e-6
c_kms = 299792.458; G = 4.30091727e-6; KPC_M = 3.0856775814913673e19
need = []
for a0si in (9.3603e-11, 1.1312e-10):
    a0 = a0si * KPC_M / 1e6
    for M in (1e9, 1e10, 1e11, 1e12):
        c2 = math.sqrt(G * a0 * M) / 2 / c_kms ** 2
        need.append(2 * c2 / (1 + 3 * c2))
gt_lo, gt_hi_need = min(need), max(need)

R.banner("G4  constants")
P("  constants beyond kappa = 1/2 (FITTED) and Omega_c h^2 = 0.12 (FITTED):")
P("    class A: Cm(x) prescribed = an unconstrained function that equals the postulated target (rule 3: the target enters as data) -> FAIL G4")
P("    class B: V(phi): a free function (a constant V is Lambda, already tied) -> each shape parameter is a new constant")
P("    class C: gamma: one dimensionless constant (gt = 8 pi G gamma), a new constant unless tied")
P("    class D: gt, s, w: three")
P("    class E: F(rho_b) [scale + strength]; per-mass Mdot, S from G1.1 (dimensionless a, b, w and the M^{3/4} scaling law)")
P("  window for a single tied gt: it must lie BELOW the growth bound gt_max = %.3e (G2, k = 30/Mpc, z = 10) and ABOVE the halo scale gt >= %.3e (smallest need, M_b = 1e9), and ideally serve all masses (needs span %.1e ... %.1e, a factor %.0f)." % (gt_max, gt_lo, gt_lo, gt_hi_need, gt_hi_need / gt_lo))
window_empty = gt_lo > gt_max
R.check("G4a", "the window for a tied gamma is EMPTY: the halo-scale need exceeds the G2 growth bound by %.1e (smallest need / bound)" % (gt_lo / gt_max), "need_min = %.3e, bound = %.3e" % (gt_lo, gt_max), window_empty)
R.check("G4b", "a single mass-independent gamma cannot match sigma^2 = V_f^2/2 across M_b = 1e9-1e12 anyway: the required gt spans a factor > 10", "need span factor = %.1f" % (gt_hi_need / gt_lo), gt_hi_need / gt_lo > 10)
a0 = 9.3603e-11; a0alt = 1.1312e-10; cH0 = 299792458.0 * 67.36e3 / 3.0856775814913673e22
kap = 0.5; OL = 0.6847
cands = {"kappa": kap, "kappa^2": kap ** 2, "kappa^2/(8 pi)": kap ** 2 / (8 * math.pi), "Omega_Lambda": OL, "Omega_c/Omega_b": 0.12 / 0.02237}
for n in (1, 2, 3):
    cands["(a0/cH0)^%d" % n] = (a0 / cH0) ** n
    cands["kappa (a0/cH0)^%d" % n] = kap * (a0 / cH0) ** n
    cands["(a0alt/cH0)^%d" % n] = (a0alt / cH0) ** n
inside = []
for nm, v in cands.items():
    ok = gt_lo <= v <= gt_max
    if ok: inside.append(nm)
    P("    tie candidate %-22s = %.3e : %s (decades from the window: %.1f)" % (nm, v, "INSIDE" if ok else "outside", math.log10(v / gt_max) if v > gt_max else math.log10(gt_lo / v)))
R.check("G4c", "NO candidate of the frozen tie list lands inside the window (frozen expectation; the smallest candidate is (a0/cH0)^3 ~ 3e-3)", "candidates inside: %s ; smallest candidate %.2e" % (inside, min(cands.values())), len(inside) == 0)
R.num("G4_window", [gt_lo, gt_max, gt_hi_need])

R.banner("G5  well-posedness")
ck = {c["name"]: c for c in T0["checks"]}
R.check("G5a", "class C (gamma): the derived scalar sector has NO healthy stable window: kinetic term negative (GHOST) for 0 < gt < 2/3, gradient-unstable (c_s^2 < 0) for gt < 0 and gt > 2/3 (T0.6b). The frozen G5 text implied a healthy window 0 < gt < 1/2; that expectation is WRONG", "T0.6b ok = %s ; %s" % (ck["T0.6b"]["ok"], ck["T0.6b"]["measured"]), ck["T0.6b"]["ok"])
tot, healthy, ex = T0["numbers"]["classD_cT1_healthy_points"]
R.check("G5b", "class D with c_T = 1 (w = s, GW170817): a scan of (gt, s) finds NO point with a healthy kinetic term and 0 < c_s^2 <= 1", "%d grid points, %d healthy" % (tot, healthy), healthy == 0)
R.check("G5c", "class A (gt = 0): the scalar is frozen by the momentum constraint (T0.6c): no ghost, no gradient instability, hyperbolic (dust): PASS", "T0.6c ok = %s" % ck["T0.6c"]["ok"], ck["T0.6c"]["ok"], load_bearing=False)
# gradient instability rate for gt < 0
Gyr_c = 0.3066014          # Mpc/Gyr
for gt in (-gt_max, -1e-7, -1e-3):
    c2 = gt / (2 - 3 * gt)
    for k in (1.0, 30.0, 1000.0):
        P("    gt = %.1e: gradient-instability rate |c_s| c k/a = %.3e /Gyr at k = %g /Mpc (a=1)" % (gt, math.sqrt(abs(c2)) * Gyr_c * k, k))
# E1 hyperbolicity
import CFG124_common
B = C.import_bcommon()
Gk = B.G
rho_b, eps_, Up, Upp = sp.symbols('rho_b eps Up Upp', positive=True)
lam = sp.symbols('lam')
Mx = sp.Matrix([[rho_b * eps_ * Upp, rho_b * Up], [eps_ * Up, 0]])
det = sp.simplify(Mx.det())
R.check("G5d", "E1 (contact coupling E_int = INT eps U(rho_b)): the stiffness matrix of (delta rho_b, delta eps) has determinant -rho_b eps U'^2 < 0 for ANY nonzero coupling U': one squared frequency omega^2 = k^2 lambda_- is negative: a gradient (Hadamard) instability at every k, whatever U''", "det = %s" % det, sp.simplify(det + rho_b * eps_ * Up ** 2) == 0)
M = 1e10; a0p = B.A0; rM = math.sqrt(Gk * M / a0p); h = 0.5 * rM
prof = B.exp_sphere(M, h)
tf = B.target_fields(prof, r0=1e-3 * rM, r1=100 * rM, n=8001)
r, rc, g = tf["r"], tf["rho"], tf["g"]
rb = prof.rho_b(r)
Uprime = g * h / rb
dU_dr = np.gradient(Uprime, r); drb_dr = np.gradient(rb, r)
U2 = dU_dr / drb_dr
tr = rb * rc * U2; detn = -rb * rc * Uprime ** 2
lam_minus = (tr - np.sqrt(tr ** 2 - 4 * detn)) / 2
x = r / rM
sel = (x >= 0.3) & (x <= 30)
rate_per_k = np.sqrt(np.abs(lam_minus)) * 1.0227          # per Gyr per (1/kpc)
P("  exponential sphere M = 1e10, h = 0.5 r_M: lambda_- (km/s)^2 at x = 0.3, 1, 3, 10, 30 = %s ; instability rate at k = 1/kpc = %s /Gyr" % (["%.2e" % np.interp(p, x, lam_minus) for p in (0.3, 1, 3, 10, 30)], ["%.2e" % np.interp(p, x, rate_per_k) for p in (0.3, 1, 3, 10, 30)]))
R.check("G5e", "E1 at the target on the exponential sphere: lambda_- < 0 at every x in [0.3, 30] (the instability is present everywhere the coupling is on)", "max lambda_- over the range = %.2e (km/s)^2 (negative = unstable)" % lam_minus[sel].max(), bool(np.all(lam_minus[sel] < 0)))
P("  E3 (enclosed-mass exchange): CFG48 G6: the baryon-mass Volterra gate is second-variation stable on 48 of 48; CFG72: the coupled fluid + mediator operator has growing modes under the declared 5/3 shell-gas operator, fragile. Cited, not re-run.")
R.banner("G5  Solar System")
P("  classes A-D: minimally coupled dust + GR metric sector: PPN = GR, Cassini safe by construction (explicit statement); the dust there is the local environmental dust (order 0.01 Msun/pc^3 = 6.8e-22 kg/m^3).")
Gsi = 6.6743e-11; Msun = 1.98847e30; AU = 1.495978707e11; a0si = 9.3603e-11
rMs = math.sqrt(Gsi * Msun / a0si); xs = AU / rMs
rho1 = a0si / (4 * math.pi * Gsi * AU * math.sqrt(1 + xs ** 2))
halo = 0.01 * Msun / (3.0856775814913673e16) ** 3
P("  E-couplings that make the dust follow C_44 at the Sun would put rho_c = a0/(4 pi G r sqrt(1+x^2)) = %.2e kg/m^3 at 1 AU (x = %.1e), which is %.1e times the local halo density %.1e kg/m^3." % (rho1, xs, rho1 / halo, halo))
txt = open(os.path.join(C.repo(), "real_research", "CASSINI_QUADRUPOLE_CONSTRAINT.md"), encoding="utf-8").read()
has_density = any(w in txt.lower() for w in ("kg/m", "g/cm", "dark matter density", "dust density", "ephemeris"))
R.check("G5f", "the frozen G5 asked to compare rho_c(1 AU) with 'the committed Cassini/ephemeris constraint read from CASSINI_QUADRUPOLE_CONSTRAINT.md'. That file holds the MOND external-field QUADRUPOLE bound (Q2), not a dust-density bound; the comparison cannot be made as written (criterion not repaired; disclosed). rho_c(1 AU) and the local-halo ratio are reported instead", "density/ephemeris terms found in the file: %s" % has_density, not has_density, load_bearing=False)
P("  ownership (a bound-only top-level switch that excludes the Sun) is Gap 1 (CFG48): unresolved; E-couplings are therefore not Solar-System-safe without it.")
if C.MU("b"):
    P("  (MUTATE b: window widened by hand to 1e-6, so G4a's claim flips.)")
nf = R.write()
sys.exit(1 if nf else 0)
