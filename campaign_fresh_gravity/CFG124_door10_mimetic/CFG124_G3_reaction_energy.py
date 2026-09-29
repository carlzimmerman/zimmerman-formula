# -*- coding: utf-8 -*-
"""CFG124 G3 -- reciprocity and energy of a coupling that would hold the dust at the target (frozen: CFG124_FROZEN_CRITERIA.md, e8b9fbcdf).
Uncoupled classes A-D: no interaction with the baryons other than through g (already in g_tot): reaction = 0 by construction.
Contact coupling (E1 / local E4): E_int = INT eps U(rho_b) dV with U' fixed by the requirement that the dust feel f_ext = g_tot outward
(-U'(rho_b) grad rho_b = g_tot).  The EXACT reaction on the baryons (generalised force of E_int under a baryon displacement) is
a_b = -grad( rho_c U'(rho_b) ) per unit baryon mass.  (The frozen text wrote the cruder third-law estimate a_b ~ -(rho_c/rho_b) f_ext; both are reported.)
Energy: E_sup = INT_0^{r_ta} 4 pi r^2 rho_c(r) [Phi_tot(r_ta) - Phi_tot(r)] dr, compared with (1/2) M_b V_f^2, V_f^4 = G a0 M_b,
in CFG48's r_ta and B's committed r_ta (CFG7_common.r_ta_law, nu_mono), both footings.  Profiles: point mass and the exponential sphere h = 0.5 r_M.
MUTATE a: hand-supplied internal pressure (reaction 0, no supply) -- the claims of the main run must flip.
"""
import os, sys, math, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG124_common as C
R = C.Report("CFG124_G3_reaction_energy")
P = R.P
P(__doc__)
B = C.import_bcommon()
G = B.G; KPC_M = B.KPC_M

R.check("G3.0", "classes A-D contain no term coupling (phi, lambda) to the baryon fields other than through g: reaction = 0 exactly (a definitional statement, verified by inspection of the action, not a numerical test)", "reaction = 0 by construction", True, load_bearing=False)

R.banner("G3.1  exact reaction on the baryons of a contact coupling that holds the target: a_b = -grad(rho_c U'), U' = g_tot h/rho_b   (exponential sphere)")
def contact(M, a0=B.A0):
    rM = math.sqrt(G * M / a0); h = 0.5 * rM
    prof = B.exp_sphere(M, h)
    tf = B.target_fields(prof, r0=1e-3 * rM, r1=100 * rM, n=8001, a0=a0)
    r, rho_c, g = tf["r"], tf["rho"], tf["g"]
    rho_b = prof.rho_b(r); gN = prof.gN(r)
    Q = rho_c * g * h / rho_b                            # rho_c U'
    a_b = -np.gradient(Q, r)                             # per unit baryon mass, radial component (negative = inward)
    g_law = B.nu_p2(gN / a0) * gN
    crude = (rho_c / rho_b) * g / g_law
    return r / rM, np.abs(a_b) / g_law, crude, rM, h
res = {}
for M in (1e9, 1e10, 1e12):
    x, rat, crude, rM, h = contact(M)
    sel = (x >= 0.3) & (x <= 30)
    res[M] = (x, rat, crude, sel)
    pts = [0.3, 1, 3, 10, 30]
    P("  M_b = %.0e (h = %.2f kpc): |a_b|/g_law at x = 0.3, 1, 3, 10, 30: %s ; crude (rho_c/rho_b) g_tot/g_law: %s" % (M, h, ["%.2e" % np.interp(p, x, rat) for p in pts], ["%.2e" % np.interp(p, x, crude) for p in pts]))
    within = (x >= 0.3) & (x <= 2.5)
    P("      max over x in [0.3, 30]: %.2e ; over x in [0.3, 2.5] (r <= 5h, where baryons still are): %.2e ; fraction of the x-grid (log) with |a_b|/g_law <= 0.10: %.3f" % (rat[sel].max(), rat[within].max(), np.mean(rat[sel] <= 0.10)))
mx = {M: v[1][v[3]].max() for M, v in res.items()}
frac = {M: float(np.mean(v[1][v[3]] <= 0.10)) for M, v in res.items()}
R.num("G3.1_max_reaction_over_glaw", mx)
if C.MU("a"):
    R.check("G3.1 (MUTATE a)", "[main-run claim] the reaction exceeds 0.10 g_law somewhere in x in [0.3, 30]; with a hand-supplied internal pressure the dust needs no coupling and the reaction is 0", "reaction = 0 (no coupling)", False)
else:
    R.check("G3.1", "the contact coupling's reaction on the baryons FAILS the 0.10 g_law line (exceeds it at x in [0.3, 30]) for every mass", "max |a_b|/g_law = %s ; fraction of the x-range within 0.10: %s" % ({"%.0e" % M: "%.2e" % v for M, v in mx.items()}, {"%.0e" % M: "%.3f" % v for M, v in frac.items()}), all(v > 0.10 for v in mx.values()))
    r10 = res[1e10]; xx = r10[0]; sel = r10[3]
    ratio_exact_crude = np.median(r10[1][sel] / r10[2][sel])
    R.check("G3.1b", "[reported] the frozen text's crude third-law estimate a_b ~ (rho_c/rho_b) g_tot is not the exact contact reaction; the exact/crude ratio (median over x in [0.3,30]) is reported", "median exact/crude = %.3g" % ratio_exact_crude, True, load_bearing=False)

R.banner("G3.2  energy: E_sup = INT rho_c [Phi_tot(r_ta) - Phi_tot(r)] dV  vs  (1/2) M_b V_f^2   (two r_ta conventions, both footings)")
try:
    sys.path.insert(0, C.repo() + "/campaign_fresh_gravity")
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        import CFG7_common as C7
    have7 = True
except Exception as e:
    have7 = False; P("  CFG7_common import failed: %r (B's committed r_ta unavailable)" % (e,))
OM, HH, DELTA_TA48 = 0.3153, 0.6736, 11.81
RHOC0_MPC = 2.775e11 * HH ** 2
def r_ta48(Mb):
    Mcol = Mb * (1.0 + B.OMEGA_C_OVER_B)
    return 1e3 * (3.0 * Mcol / (4.0 * math.pi * OM * RHOC0_MPC * DELTA_TA48)) ** (1.0 / 3.0)
def esup(prof, M, a0, r_ta, rM):
    tf = B.target_fields(prof, r0=1e-3 * rM, r1=max(2 * r_ta, 200 * rM), n=8001, a0=a0)
    r, rho, g = tf["r"], tf["rho"], tf["g"]
    keep = r <= r_ta
    r, rho, g = r[keep], rho[keep], g[keep]
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(r))])
    dphi = cum[-1] - cum                                                                          # Phi(r_ta) - Phi(r) = int_r^{r_ta} g dr'
    integrand = 4 * math.pi * r ** 2 * rho * dphi
    E = float(np.trapz(integrand, r))
    Vf2 = math.sqrt(G * a0 * M)
    return E / (0.5 * M * Vf2)
rows = {}
for foot, a0si in {"canonical": 9.3603e-11, "alt": 1.1312e-10}.items():
    a0 = a0si * KPC_M / 1e6
    for M in (1e9, 1e10, 1e11, 1e12):
        rM = math.sqrt(G * M / a0)
        rt48 = r_ta48(M)
        rtB = 1e3 * float(C7.r_ta_law(M, C7.A0[foot], C7.nu_mono, 1.0)) if have7 else float("nan")
        for pn, prof in (("point", B.point_mass(M)), ("expsphere", B.exp_sphere(M, 0.5 * rM))):
            e48 = esup(prof, M, a0, rt48, rM)
            eB = esup(prof, M, a0, rtB, rM) if have7 else float("nan")
            rows[(foot, M, pn)] = (e48, eB, rt48, rtB)
for k, v in rows.items():
    P("  %-9s M=%.0e %-9s: E_sup/(M V_f^2/2) = %.1f (CFG48 r_ta = %.0f kpc) ; %.1f (B's committed r_ta = %.0f kpc)" % (k[0], k[1], k[2], v[0], v[2], v[1], v[3]))
R.num("G3.2_energy_ratio", {"%s_%.0e_%s" % k: [v[0], v[1]] for k, v in rows.items()})
allv = [x for v in rows.values() for x in v[:2] if x == x]
if C.MU("a"):
    R.check("G3.2 (MUTATE a)", "[main-run claim] E_sup exceeds the baryons' orbital energy; with a hand-supplied internal pressure no external supply is needed (E_sup = 0)", "E_sup = 0", False)
else:
    R.check("G3.2", "E_sup > (1/2) M_b V_f^2 in BOTH r_ta conventions for every mass, both profiles and both footings (pre-declared expectation: ratio of order M_c/M_b >= 1)", "ratio ranges %.1f ... %.1f over %d cases" % (min(allv), max(allv), len(allv)), min(allv) > 1.0)
    # how it compares with CFG70's committed 23 ... 318 range (cited, not a criterion)
    P("  (CFG70's exchange energy, a different definition, is 23-73x in CFG48's convention and 57-318x in B's committed r_ta; the ratios above use the door's own declared E_sup)")
R.banner("G3.3  non-contact couplings: cited, not re-run")
P("  E2 -> CFG50 (reaction 0.03 to 7 g_law by mass at the ghost-limited strength; ghost-free force ceiling 0.5 g_tot); E3 -> CFG48 G4 (0.06-22 g_law, 23-50x baryon energy), CFG70 (23-318x), CFG72 (light cone does not change the verdict).")
nf = R.write()
sys.exit(1 if nf else 0)
