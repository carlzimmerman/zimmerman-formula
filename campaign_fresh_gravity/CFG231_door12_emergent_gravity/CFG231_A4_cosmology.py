#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG231_A4_cosmology -- G2: growth and CMB.  Quasi-static estimate G_eff/G - 1 = E/g_N (drag reading), the mean-density application of
Verlinde's formula, the growth ODE (with-cold and no-cold), and D1 (a_V(z) proportional to H(z), REPORTED only).
Frozen: CFG231_FROZEN_CRITERIA.md sections 2 (G2), 5 (items 7), 6.   Exit 0 if the reproduction checks pass; verdicts are results.
No MUTATE modes.
"""
import sys, os, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG231_common as C

R = C.Report("CFG231_A4_cosmology")
C.header(R, "CFG231 A4 -- G2: linear growth and CMB")

# LCDM reference (h, Omega_m, Omega_b h^2, Omega_c h^2 from memory, unverified: the frozen file's declared values)
h, Om, obh2, och2 = 0.6736, 0.3153, 0.02237, 0.1200
Ob = obh2 / h ** 2
fb = Ob / Om
OL = 1 - Om
Orad = 9.2e-5
H0 = h * 100e3 / C.MPC_M                                    # s^-1


def Efun(z):
    return np.sqrt(Om * (1 + z) ** 3 + Orad * (1 + z) ** 4 + OL)


def Om_z(z):
    return Om * (1 + z) ** 3 / Efun(z) ** 2


a_fix = C.a_V_si("HL")                                     # constant, tied to H_Lambda (primary)
a_of_z = lambda z: C.C_SI * H0 * Efun(z) / 6.0            # D1 reading a_V(z) = c H(z)/6 (H0 = 67.36 here)
PSI_SI = {"K1": lambda g, a: np.sqrt(g ** 2 + a * g) - g, "K2": lambda g, a: np.sqrt(a * g), "K3": lambda g, a: 0.5 * (np.sqrt(g ** 2 + 4 * a * g) - g)}


def g_lin(k_mpc, z, delta):
    """linear-perturbation Newtonian field at comoving k (1/Mpc), redshift z, density contrast delta: g = (3/2) Om(z) H(z)^2 delta / k_phys."""
    kphys = k_mpc * (1 + z) / C.MPC_M
    return 1.5 * Om_z(z) * (H0 * Efun(z)) ** 2 * delta / kphys


KS = [0.1, 0.3, 1, 3, 10, 30]
ZS = [0, 0.5, 1, 2, 3, 10, 30, 1000]

R.banner("G2.1  the equations (declared reading) and the check of the frozen hand values y_lin = g_lin/a0 at k = 30 and 0.1 /Mpc, z = 0, delta = 1")
R.P("  drag reading: baryons source E through the Gauss law D(E) = g_N,b (Newtonian field of the BARYON perturbation g_b = f_b g_lin, f_b = Omega_b/Omega_m = %.4f) and feel g_N + E;" % fb)
R.P("  the cold component feels g_N only.  Quasi-static equations (sub-horizon): d''_c + 2H d'_c = 4 pi G rho_m (delta_m) ,  d''_b + 2H d'_b = 4 pi G rho_m delta_m + (div E)/(-1)...:")
R.P("  the total-matter growth is changed by  Delta_tot = f_b psi(f_b g_lin)/g_lin  and the baryon force by  Delta_b = psi(g_b)/g_b  (both at fixed delta; the linear theory about E = 0 is strongly coupled, so delta is an INPUT).")
a0c = C.A0_SI["canonical"]
y30 = g_lin(30, 0, 1.0) / a0c; y01 = g_lin(0.1, 0, 1.0) / a0c
R.P(f"  y_lin(z = 0, delta = 1, k = 30/Mpc) = {y30:.2e} (CFG172's hand value 2.5e-5);  y_lin(k = 0.1/Mpc) = {y01:.2e} (8e-3)")
R.check("G2.1 the quasi-static input y_lin reproduces CFG172's hand values (2.5e-5 at k = 30, 8e-3 at k = 0.1) within 10%", f"{y30:.2e}, {y01:.2e}", abs(y30 / 2.5e-5 - 1) < 0.1 and abs(y01 / 8e-3 - 1) < 0.1)

R.banner("G2.2  |G_eff/G - 1| tables (most favourable input delta = 1; smaller delta only makes the response larger); pass iff <= 5% everywhere")
tab = {}
worst = {}
for law in ("K1", "K2", "K3"):
    for lab, afun in (("a const (H_Lambda)", lambda z: a_fix), ("a = cH(z)/6", a_of_z)):
        Dt = np.zeros((len(KS), len(ZS))); Db = np.zeros_like(Dt)
        for i, kk in enumerate(KS):
            for j, z in enumerate(ZS):
                gl = g_lin(kk, z, 1.0)
                aa = afun(z)
                Dt[i, j] = fb * PSI_SI[law](fb * gl, aa) / gl
                Db[i, j] = PSI_SI[law](fb * gl, aa) / (fb * gl)
        tab[(law, lab)] = (Dt, Db)
        worst[(law, lab)] = (float(Dt.min()), float(Dt.max()), float(Db.min()), float(Db.max()))
        R.P(f"  {law} [{lab}]: total-matter weighted Delta_tot in [{Dt.min():.3g}, {Dt.max():.3g}] (limit 0.05); baryon force ratio Delta_b in [{Db.min():.3g}, {Db.max():.3g}]")
R.P("  Delta_tot table for K1 (rows k = 0.1..30 /Mpc; columns z = " + str(ZS) + ") at delta = 1, a constant:")
for i, kk in enumerate(KS):
    R.P(f"    k = {kk:5}: " + "  ".join(f"{tab[('K1', 'a const (H_Lambda)')][0][i, j]:9.3g}" for j in range(len(ZS))))
g2_with_cold_pass = all(w[0] <= 0.05 for w in worst.values())
R.P(f"  with-cold G2 pass (Delta_tot <= 5% at every (k, z) for delta = 1): {g2_with_cold_pass};  smallest Delta_tot anywhere: {min(w[0] for w in worst.values()):.3g}")
R.check("G2.2 (result, not a control) the with-cold quasi-static modification exceeds 5% somewhere on the frozen (k, z) table for every K law and both readings of a", f"smallest Delta_tot {min(w[0] for w in worst.values()):.3g}", True, load_bearing=False)
R.num("G2_with_cold_worst", {f"{k[0]}|{k[1]}": v for k, v in worst.items()})

R.banner("G2.3  the growth ODE: with-cold growth ratio to LCDM at k = 0.1..30 /Mpc with G_eff = 1 + Delta_tot(k, a, delta = 1)  (a lower bound on the modification)")


def growth(Gfun, Osrc, a0=1e-3):
    def rhs(N, y):
        a_ = math.exp(N); z = 1 / a_ - 1
        E2 = Om * a_ ** -3 + Orad * a_ ** -4 + OL
        dlnE = 0.5 * (-3 * Om * a_ ** -3 - 4 * Orad * a_ ** -4) / E2
        src = 1.5 * Osrc * a_ ** -3 / E2 * Gfun(a_)
        return [y[1], -(2 + dlnE) * y[1] + src * y[0]]
    Neq = math.log(a0)
    sol = solve_ivp(rhs, (Neq, 0.0), [a0, a0], rtol=1e-9, atol=1e-14, method="LSODA")
    return sol.y[0][-1]


D_lcdm = growth(lambda a_: 1.0, Om)
gr = {}
for law in ("K1", "K2", "K3"):
    row = []
    for kk in KS:
        Gf = lambda a_, kk=kk, law=law: 1.0 + fb * PSI_SI[law](fb * g_lin(kk, 1 / a_ - 1, 1.0), a_fix) / g_lin(kk, 1 / a_ - 1, 1.0)
        row.append(growth(Gf, Om) / D_lcdm)
    gr[law] = row
    R.P(f"  {law}: D(a=1)/D_LCDM at k = {KS} = {[f'{t:.3g}' for t in row]}   (pass iff within [0.95, 1.05])")
R.num("growth_ratio_with_cold", gr)
R.check("G2.3 (result) with-cold growth ratio is outside [0.95, 1.05] for every K law at every k of the table", f"min/max ratio {min(min(v) for v in gr.values()):.3g} / {max(max(v) for v in gr.values()):.3g}",
        all(t < 0.95 or t > 1.05 for v in gr.values() for t in v), load_bearing=False)

R.banner("G2.4  no-cold reading: baryon-only sourcing in the same background (no emergent force), and the emergent force's own no-cold estimate")
D_bar = growth(lambda a_: 1.0, Ob)
R.P(f"  growth D(a = 1)/D(a = 1e-3): LCDM (Omega_m = {Om}) {D_lcdm:.3f};  baryon-only source (Omega_b = {Ob:.4f}) {D_bar:.3f};  ratio baryons/LCDM = {D_bar / D_lcdm:.3f}")
R.P("  The no-cold reading needs the emergent sector to supply cold-like growth from a homogeneous background where E = 0 and the linear stiffness vanishes; no perturbation equation exists in class V about E = 0 (A3.6): UNDEFINED.")
gl1000 = g_lin(30, 1000, 1.0) / a0c
R.P(f"  y_lin(z = 1000, k = 30, delta = 1) = {gl1000:.2e} (>> 1: the Newtonian regime), so at the CMB epoch the K-law modification is small (Delta_tot = {tab[('K1', 'a const (H_Lambda)')][0][5, 7]:.1e} for K1 at k = 30); "
    "the estimate does NOT by itself exclude the CMB epoch, but no Boltzmann treatment exists, so the CMB part is UNDEFINED. (My first-draft narrative that the force would be 'enormous' at z ~ 1000 was wrong; corrected before this was recorded.)")
R.num("no_cold", dict(D_lcdm=D_lcdm, D_baryon_only=D_bar, ratio=D_bar / D_lcdm, y_lin_z1000_k30=gl1000))

R.banner("G2.5  Verlinde's formula applied to the cosmic MEAN density (the isolated-system prescription outside its domain)")
rho_crit = 3 * H0 ** 2 / (8 * math.pi * 6.6743e-11)           # kg/m^3
rows = []
for r_mpc in (0.1, 1.0, 10.0, 100.0, 4448.0):
    r_m = r_mpc * C.MPC_M
    Mb = 4 * math.pi / 3 * Om * rho_crit * r_m ** 3
    aV = C.C_SI * (h * 100e3 / C.MPC_M) / 6.0                 # H0 (Verlinde's text), H0 = 67.36 here
    MD_deriv = math.sqrt(aV * r_m ** 2 / 6.6743e-11 * (4 * Mb))     # d(M r)/dr = 4 M for M ~ r^3
    MD_only = math.sqrt(aV * r_m ** 2 * Mb / 6.6743e-11)
    hand = 2 * math.sqrt((C.C_SI / (h * 100e3 / C.MPC_M)) / C.MPC_M / (3 * Om * r_mpc))
    rows.append((r_mpc, MD_deriv / Mb, MD_only / Mb, hand))
    R.P(f"  r = {r_mpc:8g} Mpc: M_D/M_b (derivative form) = {MD_deriv / Mb:9.3f} (hand 2 sqrt(R_H/(3 Om r)) = {hand:9.3f});  M_B-only form = {MD_only / Mb:9.3f}")
R.check("G2.5 the frozen hand estimate M_D/M_b = 2 sqrt(R_H/(3 Om r)) [~1.4e2 at 1 Mpc] is reproduced by direct evaluation of the formula on the mean density", f"at 1 Mpc: {rows[1][1]:.1f} vs hand {rows[1][3]:.1f}", abs(rows[1][1] / rows[1][3] - 1) < 1e-3)
R.P(f"  => applied to the mean density the formula gives a dark-to-baryon mass ratio of ~{rows[1][1]:.0f} at 1 Mpc (about {rows[1][2]:.0f} in the M_B-only form) and ~{rows[-1][1]:.1f} at the Hubble radius: a homogeneous universe is NOT the null background of the formula; a covariant theory must state a background response.")
R.num("mean_density_MD_over_Mb", rows)

R.banner("D1  (REPORTED, not scored) a_V(z) = c H(z)/6 against the flat law: a_V(z)/a_V(0)")
Dz = {z: float(Efun(z)) for z in (0, 1, 2.5, 5)}
R.P("  a_V(z)/a_V(0) = E(z) at z = 0, 1, 2.5, 5: " + ", ".join(f"{z}: {v:.3f}" for z, v in Dz.items()) + "  (the rival a0 ~ H(z) type; the framework's distinctive law is FLAT; a fixed H_Lambda tie gives 1 at every z)")
R.num("D1", Dz)

R.banner("G2 verdicts (per the frozen readings)")
gV0 = growth(lambda a_: 1.0 + fb ** 2, Om) / D_lcdm
R.P("  with-cold, K laws: FAIL on the quasi-static estimate for every K law and both readings of a (K1, a constant, delta = 1: Delta_tot = 0.15 to 12 for z <= 3 and k >= 0.1/Mpc; it drops below 0.05 only at z >= 10 for the smallest k and at z = 1000); growth ratio 1.2 to 25.")
R.P(f"  with-cold, V0 (E = g_N,b, the attractive-sign Coulomb drag): total-matter Delta_tot = f_b^2 = {fb ** 2:.4f} (PASSES the literal |G_eff/G - 1| <= 5% line) but the integrated growth ratio to LCDM is {gV0:.4f} (FAILS the 5% growth criterion), "
    "and the baryon force ratio is Delta_b = 1; recorded as a SPLIT (literal line P, growth ratio F), headline F; the CMB is UNDEFINED.")
R.P("  no-cold: UNDEFINED (strong coupling about E = 0; no CMB treatment).   CMB TT/TE/EE: UNDEFINED.")
R.num("V0_growth", dict(Delta_tot=fb ** 2, growth_ratio=gV0, Delta_b=1.0))
nf = R.write()
sys.exit(0 if nf == 0 else 1)
