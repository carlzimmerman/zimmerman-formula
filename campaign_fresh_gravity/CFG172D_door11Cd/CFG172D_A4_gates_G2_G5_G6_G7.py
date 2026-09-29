#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG172D_A4 -- G2, G5, G6, G7 for the 11C-d arms (frozen criteria 2.2), controls C3, M4 (G7 side).

G2  (i) homogeneous background off-plateau: A1's O3b;  (ii) d1: the gate is never on (f = 0 at every radius, A2), so the web is untouched;
    (iii) d2: the contact interaction acts in the WEB on the baryons: c_s^2/c^2 = -zeta^2 eps_b/(3 c2 eps_L) at the cosmic mean baryon density,
    growth rate Gamma = k |c_s| against H at k = 0.1, 1, 10, 30 /Mpc, z = 0, 1, 3, 10 (pass iff |Gamma|/H <= 0.05: growth of the baryon
    perturbations within 5%); CMB: UNDEFINED (no Boltzmann treatment).
G5  ghost sign (A1), O1 (A3), criterion B (NOT ADDRESSED: no characteristic-cone analysis was done), Q2: the isolated Sun's anomalous
    acceleration at Saturn from V0's kernel (unfiltered), evaluated only if the gate is ON at the Sun (theta root at the solar density);
    the heat-filtered remainder (KM3) is INHERITED from the record and not re-derived here.
G6  KM3's V0 formulas alpha_1 = -4 alpha_c, alpha_2 = alpha_c (alpha_c - c2)/(2 c2), printed against |alpha_1| <= 3.4e-5, 3.5e-5, 2.1e-5 and
    |alpha_2| <= 1.6e-9 (quoted, from memory, unverified; the data chat verifies).  d2's coupling contribution is NOT derived (UNDEFINED).
G7  KM1: D = 2 w^2/(c^2 c2) with the record's control numbers; the gate-edge shift from CV4's K3 dipole (record input, not re-derived).
Run:  ZF_REPO=<repo> python3 CFG172D_A4_gates_G2_G5_G6_G7.py     (seconds)
"""
import os, sys, json, math
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG172D_common as C
import CFG172D_solver as S

MUT = os.environ.get("MUTATE")
R = C.Report("CFG172D_A4_gates_G2_G5_G6_G7", MUT)
P, banner, check = R.P, R.banner, R.check
P(__doc__.split("Run:")[0].strip()); P(f"\n  repo: {C.rel(C.REPO)}   MUTATE={MUT}")
CK = S.CKMS; G = S.G
zeta_ref = {}
p3 = os.path.join(C.HERE, "CFG172D_A3_obstruction_results.json")
if os.path.exists(p3):
    zeta_ref = json.load(open(p3))["numbers"].get("zeta_min_reference", {})
P(f"  zeta_min (reference cell) from A3: {zeta_ref}")

# ============================================================================================ G2
banner("G2  (i) background (A1 O3b), (ii) d1, (iii) d2's contact instability in the web")
p1 = os.path.join(C.HERE, "CFG172D_A1_theta_equation_results.json")
o3b = json.load(open(p1))["numbers"].get("O3b_tmax") if os.path.exists(p1) else None
P(f"  O3b (A1): max t(u_bg) over z in [-0.5, 20]: {o3b}   (<= 0 means off-plateau with all derivatives zero)")
c2 = 7.3e-3
G2 = {}
zs = (0.0, 1.0, 3.0, 10.0); ks = (0.1, 1.0, 10.0, 30.0)      # 1/Mpc
for arm in ("d2_lin_even", "d2_sat_even", "d2_lin_mono", "d2_sat_mono"):
    kind, variant = arm.split("_")[1], arm.split("_")[2]
    zt = zeta_ref.get(f"{kind}/{variant}")
    if zt is None:
        continue
    zt = abs(zt) if not (MUT == "M2") else 0.0
    rows = {}
    for z in zs:
        rho_b_mean = C.FB * C.Om * C.rho_crit0 * (1 + z)**3
        eps_ratio = rho_b_mean / C.RHO_L                              # eps_b / eps_L (same c^2)
        cs2 = -zt**2 * eps_ratio / (3 * c2)                            # c_s^2 / c^2 (lin; sat's h' = 1 at the web's tiny vartheta)
        cs = math.sqrt(abs(cs2)) * C.CLIGHT / 1e3                      # km/s
        Hkms_Mpc = C.Hz(z) * C.KPC                                      # km/s/Mpc (1 Mpc = KPC km)
        for k in ks:
            rows[f"z{z}/k{k}"] = dict(cs_kms=cs, Gamma_over_H=k * cs / Hkms_Mpc)
    G2[arm] = rows
    mx = max(v["Gamma_over_H"] for v in rows.values()); mn = min(v["Gamma_over_H"] for v in rows.values())
    P(f"  [{arm}] zeta = {zt:.3g}: |c_s| at the mean baryon density: z = 0 {rows['z0.0/k1.0']['cs_kms']:.3g} km/s, z = 3 {rows['z3.0/k1.0']['cs_kms']:.3g} km/s; "
      f"Gamma/H over k in [0.1, 30]/Mpc, z in [0, 10]: {mn:.2g} .. {mx:.2g}  (pass line 0.05)")
R.num("G2_web_instability", G2)
for arm, rows in G2.items():
    ok = max(v["Gamma_over_H"] for v in rows.values()) <= 0.05
    R.verdict(f"G2_{arm}", "PASS" if ok else "FAIL", f"web growth Gamma/H max {max(v['Gamma_over_H'] for v in rows.values()):.2g} (line 0.05); CMB UNDEFINED")
R.verdict("G2_d1", "PASS (trivially: the gate is never on, so V0's web is untouched; but MOND is never on either)", "background O3b PASS; CMB UNDEFINED")
if MUT == "M2":
    bit2 = all(max(v["Gamma_over_H"] for v in rows.values()) <= 0.05 for rows in G2.values())
    P(f"  MUTATE=M2: without the coupling the web instability vanishes: {'BITES' if bit2 else 'no'}")

# ============================================================================================ G5
banner("G5  ghost (A1), stability (A3), criterion B, Q2 at the Sun")
au = 1.495978707e11; RS = 9.5826 * au
GMsun = 1.32712440018e20
a0 = C.A0_L["canonical"]
gN_S = GMsun / RS**2
y_S = gN_S / a0
hS = float(C.h_of(y_S))
a_anom = hS * a0
Q2_iso = a_anom / RS                                     # tide = g_ph / R (>= |d g_ph/dR| since g_ph ~ const with a log tail)
bound = 5.2e-27
P(f"  Sun at Saturn: g_N = {gN_S:.3e} m/s^2, y = g_N/a0 = {y_S:.3e}, h(y) = {hS:.4f} (V0's nu_mono, L352 table): a_anom = h a0 = {a_anom:.3e} m/s^2; "
  f"Q2 = a_anom/R = {Q2_iso:.2e} s^-2 vs bound {bound:.1e}: {Q2_iso / bound:.2e} x")
check("C-Q2 the unfiltered V0 kernel leaves an acceleration ~ a0 at Saturn: Q2 = a_anom/R_Saturn (the record's 'constant ~a0 tail')", f"{Q2_iso / bound:.2e} x the bound", Q2_iso / bound > 1e3, load_bearing=False)
# is the gate ON at the solar density?  theta root at rho ~ local baryon density (0.1 Msun/pc^3)
rho_sun = 0.1 * 1e9                                       # Msun/kpc^3
gate_sun = {}
for arm in ("d2_lin_even", "d2_sat_even", "d2_lin_mono", "d2_sat_mono"):
    kind, variant = arm.split("_")[1], arm.split("_")[2]
    zt = zeta_ref.get(f"{kind}/{variant}")
    if zt is None:
        continue
    y, nro = S.theta_root(0.0, 0.25, 7.3e-3, np.zeros(1), np.array([rho_sun]), abs(zt), kind=kind, variant=variant, ND=6000)
    f, fy, fyy, t, u = S.gate_from_y(y, 0.0, 0.25, variant=variant)
    gate_sun[arm] = dict(y=float(y[0]), f=float(f[0]))
    P(f"  [{arm}] solar-neighbourhood baryon density 0.1 Msun/pc^3, z = 0: theta/thetabar = {y[0]:.3g}, gate f = {float(f[0]):.3g}"
      f"{'  => gate OFF at the Sun (band-pass artefact of the even variant)' if f[0] < 0.01 else '  => gate ON: Q2 as above'}")
R.num("gate_at_sun", gate_sun)
R.num("Q2", dict(iso_unfiltered=Q2_iso, ratio_to_bound=Q2_iso / bound, a_anom=a_anom))
R.verdict("G5_Q2_unfiltered_isolated_Sun", "FAIL where the gate is ON at the Sun (d2 mono, sat); 0 where OFF", f"{Q2_iso / bound:.2e} x the bound")
R.verdict("G5_Q2_filtered", "NOT ADDRESSED", "V0's heat-filtered remainder (KM3, eta_N <= 1.2e-8) is inherited from the record; not re-derived here")
R.verdict("G5_MW_tide", "NOT ADDRESSED", "CFG7 H1's Milky-Way tide (4.0-5.7 x for the strict law, record) needs its baryon budget; not reproduced")
R.verdict("G5_criterion_B", "NOT ADDRESSED", "no characteristic-cone analysis of the theta sector was done")
R.verdict("G5_ghost", "PASS for c2 > 0 (A1 ghost check); FAIL under M7", "the c2 part of the theta stiffness is negative for c2 > 0")

# ============================================================================================ G6
banner("G6  PREFERRED FRAME: KM3's V0 formulas against the quoted PPN limits (from memory, unverified)")
LIM1 = (3.4e-5, 3.5e-5, 2.1e-5); LIM2 = 1.6e-9
G6 = {}
for ac in (1e-13, 3.2e-9):
    for c2v in (7.3e-3, 0.067):
        a1 = -4 * ac; a2 = ac * (ac - c2v) / (2 * c2v)
        row = dict(alpha1=a1, alpha2=a2, **{f"|a1|<={l:g}": abs(a1) <= l for l in LIM1}, **{f"|a2|<={LIM2:g}": abs(a2) <= LIM2})
        G6[f"ac{ac:g}/c2{c2v:g}"] = row
        P(f"  alpha_c = {ac:g}, c2 = {c2v:g}: alpha1 = {a1:.3e} ({', '.join('PASS' if abs(a1) <= l else 'FAIL' for l in LIM1)} at 3.4e-5, 3.5e-5, 2.1e-5); "
          f"alpha2 = {a2:.4e} ({'PASS' if abs(a2) <= LIM2 else 'FAIL'} at 1.6e-9; margin {(LIM2 - abs(a2)) / LIM2:+.2e})")
R.num("G6", G6)
check("C3 (control) KM3's alpha_2 -> -alpha_c/2 for c2 >> alpha_c, and |alpha_2| <= 1.6e-9 iff alpha_c <= 3.2e-9 (the record's window)", f"alpha_c = 3.2e-9, c2 = 7.3e-3: |alpha_2| = {abs(G6['ac3.2e-09/c27.3e-03']['alpha2']):.6e}"
      if 'ac3.2e-09/c27.3e-03' in G6 else str(list(G6)), abs(G6[list(G6)[2]]["alpha2"]) <= LIM2 * (1 + 1e-6), load_bearing=False)
R.verdict("G6_d1", "PASS (inherited: V0's static block, KM3; the gate never turns on)", "alpha1, alpha2 at both c2 ends as printed; borderline: |alpha_2| = 1.5999e-9 at alpha_c = 3.2e-9, c2 = 7.3e-3")
R.verdict("G6_d2", "UNDEFINED", "the added matter-theta coupling's contribution to alpha_1, alpha_2 was not derived")

# ============================================================================================ G7
banner("G7  a0 versus the frame speed (KM1) and the gate-edge shift (CV4 K2/K3 dipole)")
def Dkm1(w, c2v): return 2 * (w * 1e3 / C.CLIGHT)**2 / c2v
ctrl = dict(D3_c2_2p5e5=Dkm1(620, 2.5e-5) / 3, D3_c2_1e5=Dkm1(620, 1e-5) / 3)
P(f"  KM1 control (record: D/3 = 0.114 at c2 = 2.5e-5, 0.285 at c2 = 1e-5, w = 620 km/s): {ctrl['D3_c2_2p5e5']:.3f}, {ctrl['D3_c2_1e5']:.3f}")
check("C3 KM1's D/3 numbers reproduced (record: 0.114, 0.285)", str(ctrl), abs(ctrl["D3_c2_2p5e5"] - 0.114) < 0.005 and abs(ctrl["D3_c2_1e5"] - 0.285) < 0.005, load_bearing=False)
w_v = 3000.0 if False else 600.0
G7 = {}
for c2v in (7.3e-3, 0.067, 7.3e-5):
    D = Dkm1(600, c2v); D3 = D / 3
    G7[f"c2={c2v:g}"] = dict(D=D, D_over_3=D3, D_pass=D <= 0.10, D3_pass=D3 <= 0.10)
    P(f"  c2 = {c2v:g}, w = 600 km/s: D = {D:.3g}, isotropic part D/3 = {D3:.3g} ({'PASS' if D3 <= 0.10 else 'FAIL'} at 10%; D itself {'PASS' if D <= 0.10 else 'FAIL'})")
edge_shift = 4.8e-3 / (1 - 0.485)                          # (|K/3H - 1| max, record CV4 K3) / (depletion at the gate's ON point, z = 0.25)
P(f"  gate edge: CV4's K3 dipole |K/3H - 1| <= 4.8e-3 shifts the gate variable by a fraction ~ {edge_shift:.3g} of the depletion the gate needs => radius shift ~ {edge_shift / 2.5:.1e}..{edge_shift:.1e} (record input, not re-derived)")
R.num("G7", G7); R.num("G7_edge_shift_frac", edge_shift)
R.verdict("G7_d1", "PASS on record inputs (a0 shift D/3 <= 1.1e-3 at c2 = 7.3e-3; no gate to shift)", "KM1's formula and CV4's numbers are inputs, not re-derived here")
R.verdict("G7_d2", "UNDEFINED for the coupling's own dipole; PASS on record inputs for a0", "the moving-matter response of theta with the d2 coupling was not derived; edge shift from CV4 K3 only")
if MUT == "M4":
    D = Dkm1(600, 7.3e-5)
    P(f"  MUTATE=M4 (c2 x 0.01): D = {D:.3g}, D/3 = {D / 3:.3g}: D itself crosses 10% ({D > 0.10}), the primary metric D/3 does not")
    bit = D > 0.10 and D / 3 <= 0.10
    P(f"  M4's G7 side {'BITES on D but NOT on the primary metric D/3 (declared control failure)' if bit else 'no'}")

nf = R.write()
sys.exit(0 if nf == 0 else 1) if not MUT else sys.exit(0)
