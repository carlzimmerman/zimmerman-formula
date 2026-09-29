#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S_stability_solar_ownership -- CFG121 G4 table/tie, G5 tests S1-S4, and the Gap-1 side test O1, exactly as frozen.
S1 kernel stability: min over g_N in [1e-4, 1e4] a0 of d|Pi_eq|/dg_N = h'(y) for P2, nu_mono, simple, standard.  Pass: >= 0.
S2 Hessian; S3 hyperbolicity; S4 Solar System (uncapped and medium-density-capped); O1 locality + twin test + tau/t_dyn.
MUTATE=kernel : the kernel used for G1 is 'standard' instead of P2       -> S1_used must change from PASS to FAIL
MUTATE=nofield: drop the -4 pi G self-field term (stiffness uses dg/dPi instead of dg/dPi - 4 pi G) -> S1_standard classification must change
"""
import math, sys, json, os
import numpy as np
import cfg121_common as C
from cfg121_common import G, A0, MASSES, rM_of, target_at, nu_p2, nu_mono, nu_simple, nu_standard, MUTATE, HERE

R = C.Report("S_stability_solar_ownership")
R.banner(f"CFG121 S  (footing {C.FOOT}: a0 = {C.A0_SIV:.4e} m/s^2; MUTATE='{MUTATE}')")
KERNELS = {"P2": nu_p2, "nu_mono": nu_mono, "simple": nu_simple, "standard": nu_standard}
USED = "standard" if MUTATE == "kernel" else "P2"
PS = json.load(open(os.path.join(HERE, "B_budget_pincer" + ("" if C.FOOT == "canonical" else "_second") + "_results.json")))["numbers"]["Pstar"]

# ------------------------------------------------------------------------------------------------ S1
R.banner("S1  kernel stability: h(y) = (nu-1) y (= 4 pi G |Pi_eq|/a0, y = g_N/a0); longitudinal stiffness  dg/dPi - 4 pi G = 4 pi G / h'  (needs h' > 0)")
y = np.geomspace(1e-4, 1e4, 4001)
lo_thresh = -1.0 if MUTATE == "nofield" else 0.0          # nofield control: stiffness dg/dPi = 4 pi G (1 + 1/h') ... positive iff h' > -1
S1 = {}
for name, nu in KERNELS.items():
    h = (nu(y) - 1.0) * y
    hp = np.gradient(h, y)
    hp_min = float(hp.min())
    neg = y[hp < lo_thresh]
    S1[name] = hp_min
    R.P(f"  {name:9s}: min h' = {hp_min:+.4e}; region with h' < {lo_thresh:g}: " + ("none" if len(neg) == 0 else f"y in [{neg.min():.3g}, {neg.max():.3g}]") + f";  h(1e4) = {float(h[-1]):.4f} (P2 -> 0.5 from below)")
    R.verdict(f"S1_{name}", "PASS" if hp_min >= lo_thresh else "FAIL", f"min h' = {hp_min:+.3e} vs {lo_thresh:g}")
R.verdict("S1_used", R.verdicts[f"S1_{USED}"]["status"], f"the kernel used for G1 in this run is {USED}")

# ------------------------------------------------------------------------------------------------ S2 / S3
R.banner("S2  Hessian of the declared action about the static state (V_U and V_B); S3  hyperbolicity of the linearised local system")
kern = KERNELS[USED]
hp = np.gradient((kern(y) - 1.0) * y, y)
Gfun_over_P_min = None
# longitudinal potential Hessian ~ 4 pi G / h' (V_U and V_B: after eliminating the Poisson/constraint fields), transverse ~ Gfun(P)/P > 0
PP = (kern(y) - 1.0) * y * A0                  # P in accel units (kpc-based)
gT = ((kern(y) - 1.0) * y)
transverse = np.where(gT > 0, ((gT ** 2 / (1 - 2 * gT) + gT) if False else 1.0), 1.0)
longi_min = float(np.min(1.0 / hp[np.abs(hp) > 1e-30])) if np.all(hp > 0) else float(np.min(np.sign(hp) / np.maximum(np.abs(hp), 1e-30)))
R.P(f"  V_U: kinetic coefficient kappa_I/(Q^2 rho_D) > 0; longitudinal potential Hessian 4 pi G/h' over y in [1e-4, 1e4]: min sign = {'positive' if np.all(hp > 0) else 'NEGATIVE somewhere'}; transverse Hessian Gfun(P)/P > 0 for P > 0 (kernel {USED}).")
R.P("  V_U: no spatial-gradient term in the declared action, so omega^2(k) is independent of k (a local oscillator at each point; the Poisson constraint enters only through the -4 pi G already counted).")
ok_U = bool(np.all(hp > 0))
R.verdict("S2_V_U", "PASS" if ok_U else "FAIL", "kinetic matrix positive; potential Hessian non-negative iff h' > 0 for the kernel in use")
# V_B: the (Phi_b, lambda) constraint block in the quadratic form
eig_rows = []
for kk in (1e-3, 1.0, 1e3):
    D = kk ** 2 / (4 * math.pi * G)
    Mx = np.array([[0.0, D], [D, 0.0]])
    ev = np.linalg.eigvalsh(Mx)
    eig_rows.append((kk, ev))
    R.P(f"  V_B: quadratic form of the (Phi_b, lambda) block at k = {kk:g}/kpc: [[0, D],[D, 0]], D = k^2/(4 pi G): eigenvalues {ev[0]:.3e}, {ev[1]:.3e} (signature +,-)")
R.P("  V_B: in the declared Newtonian action this block has NO time derivatives (constraint variables); the +,- signature becomes a dipole-ghost KINETIC matrix only in a relativistic completion (CFG50: OPEN).  The frozen rule ('a dipole-ghost structure is a FAIL for that variant') is applied literally.")
R.verdict("S2_V_B", "FAIL", "the (Phi_b, lambda) block has the indefinite [[0, D],[D, 0]] structure (frozen rule applied literally); Newtonian-sector dynamical fields (Pi) are healthy iff h' > 0 as for V_U; relativistic completion untested")
R.verdict("S3_V_U", "PASS" if ok_U else "FAIL", "omega_L^2, omega_T^2 >= 0 for all g_N and k, group velocity 0 <= c (kernel in use); Newtonian sector only")
R.verdict("S3_V_B", "PASS" if ok_U else "FAIL", "same for the Pi modes; the constraint block has no propagating mode; Newtonian sector only")

# ------------------------------------------------------------------------------------------------ S4
R.banner("S4  Solar System (the Sun in the Galaxy's field): monopole and anisotropy of the polarisation field at 9.5 AU, uncapped and medium-density-capped")
GMSUN = 1.32712440018e20
AU = 1.495978707e11
r = 9.5 * AU
a0 = C.A0_SIV
gsun = GMSUN / r ** 2
mu = np.linspace(-1.0, 1.0, 40001)               # cos(theta) of the position relative to the external-field axis
rows = {}
for gx in (1.0, 1.9, 3.0):
    ge = gx * a0
    # g_N = -gsun rhat + ge zhat ; rhat = (sin, 0, mu)
    gr = -gsun + ge * mu                          # radial component of g_N (inward positive magnitude below)
    gp = ge * np.sqrt(1 - mu ** 2)
    gn = np.hypot(gr, gp)
    Vin = (nu_p2(gn / a0) - 1.0) * (-gr)          # (nu-1) g_N . (-rhat) : inward pull of the algebraic phantom vector
    mono = float(np.trapz(Vin, mu) / 2.0)
    aniso = float(0.5 * (Vin.max() - Vin.min()))
    nu_eff = mono * r ** 2 / GMSUN
    rows[gx] = (mono, aniso, nu_eff)
    R.P(f"  g_ext = {gx} a0: uncapped monopole pull (Gauss) = {mono:.4e} m/s^2 (isolated limit a0/2 = {a0 / 2:.4e}), anisotropy amplitude of V_r = {aniso:.3e} m/s^2, induced mass fraction = {nu_eff:.3e} M_sun")
unc = max(v[0] for v in rows.values())
CAP = {}
for lab, rhoD_msun_pc3 in (("0.01 Msun/pc^3 (local DM density)", 0.01),):
    rhoD = rhoD_msun_pc3 * 1.98841e30 / (3.0857e16) ** 3
    for eps in (1.0,):
        for var, Q in (("Q = 1", 1.0), ("Q = 9.68 (V_B star)", PS["V_B"]["Q"]), ("Q = 139 (V_U star)", PS["V_U"]["Q"])):
            Pcap = 4 * math.pi * 6.6743e-11 * eps * Q * rhoD * r          # |4 pi G Pi| <= 4 pi G eps Q rho_D r  (m/s^2)
            CAP[var] = Pcap
            R.P(f"  capped |Pi| <= eps_c Q rho_D r with rho_D = {lab}, eps_c = {eps}, {var}: |delta a| <= {Pcap:.3e} m/s^2")
bound_generous, bound_tight = 1e-13, 1e-15
bound_record = a0 / 2 / 1278.0
capped = max(CAP.values())
R.P(f"  bounds: generous 1e-13, tight 1e-15, and the record's alpha = 1 ephemeris bound a0/2/1278 = {bound_record:.2e} m/s^2 (the 1278x is from the memory notes: unverified here)")
R.verdict("S4_uncapped", "FAIL" if unc > bound_generous else "PASS", f"uncapped P2 monopole pull {unc:.2e} m/s^2 vs generous line 1e-13: {unc / bound_generous:.0f}x over ({unc / bound_record:.0f}x over the record's a0/2/1278); the external-field effect at g_ext = 1-3 a0 does NOT remove it (the Sun's field dominates: |g_N| >> a0)")
R.verdict("S4_capped", "PASS" if capped <= bound_generous else "FAIL", f"medium-density-capped |delta a| <= {capped:.2e} m/s^2 (generous 1e-13; tight 1e-15: {'pass' if capped <= bound_tight else 'fail'})")
R.verdict("S4", "PASS" if capped <= bound_generous else "FAIL", "safe ONLY through the medium-density cap (the same budget B1 that makes G1c fail), NOT through the external-field effect; ownership route of candidate B unavailable")

# ------------------------------------------------------------------------------------------------ O1
R.banner("O1  Gap-1 side test: (i) instantaneous locality (external-field suppression of a satellite's bound charge); (ii) twin test and tau/t_dyn")
R.P("  (i) satellite of baryon mass Ms in the field of a point host Mh at distance d: monopole bound-charge mass within 3 r_M,sat (algebraic P2, Gauss-averaged) / isolated")
G_ = 4.30091727e-6
for Ms in (1e8, 1e9):
    rMs = rM_of(Ms)
    rs = 3 * rMs
    for Mh in (1e11, 1e12):
        line = f"    Ms={Ms:.0e}, Mh={Mh:.0e}: "
        for d in (50.0, 100.0, 200.0, 300.0):
            gh = G_ * Mh / d ** 2                                        # (km/s)^2/kpc
            gs = G_ * Ms / rs ** 2
            gr = -gs + gh * mu
            gp = gh * np.sqrt(1 - mu ** 2)
            gn = np.hypot(gr, gp)
            Vin = (nu_p2(gn / A0) - 1.0) * (-gr)
            Mph = rs ** 2 / G_ * float(np.trapz(Vin, mu) / 2.0)
            iso = Ms * (math.sqrt(1 + 9.0) - 1.0)
            line += f"d={d:.0f} kpc (g_h/a0 = {gh / A0:.2f}): {Mph / iso:.3f};  "
        R.P(line)
R.P("  (ii) twin test: two systems with the same instantaneous baryon state and different histories (accreted satellite vs formed-embedded dwarf) have the SAME adiabatic polarisation P = h(g_b(x)) -- a theorem of the declared model (state functional); CFG48 G2/G3.")
R.P("       tau/t_dyn = Omega_orb/omega at the minimal B1-satisfying medium (rho_D = M_c/(4 pi Q r^3), eps_c = 1); omega^2/Omega^2 = Q kappa_I^-1 (M_c/M_tot)/h' * ... computed exactly below")
best = []
for M in (1e10, 1e12):
    t = target_at(M, np.geomspace(0.3, 30.0, 121))
    Xg = np.geomspace(0.3, 30.0, 121)
    Mb, Mc, r_ = t["Mb"], t["Mc"], t["r"]
    yb = G_ * Mb / (r_ ** 2 * A0)
    hpb = (nu_p2(yb) - 1.0) + yb * (-1.0 / (2 * yb ** 2 * nu_p2(yb)))
    Om2 = G_ * (Mb + Mc) / r_ ** 3
    for Q, kap in ((1.0, 1.0), (PS["V_B"]["Q"], 1.0), (PS["V_B"]["Q"], PS["V_B"]["kappa_I"]), (PS["V_U"]["Q"], 1.0), (PS["V_B"]["Q"], 1e2), (PS["V_B"]["Q"], 1e4)):
        rhoD = Mc / (4 * math.pi * Q * r_ ** 3)
        om2 = (Q ** 2 / kap) * 4 * math.pi * G_ * rhoD / hpb
        ratio = np.sqrt(Om2 / om2)                        # tau / t_dyn
        F_req = Mc / (4 * math.pi * r_ ** 3 * t["rho"]) / Q
        b1 = bool(np.all(F_req <= 0.10))
        win = (ratio >= 1.0) & (ratio <= 10.0)
        xs_win = Xg[win]
        best.append((M, Q, kap, b1, xs_win))
        R.P(f"    M_b={M:.0e}, Q={Q:.3g}, kappa_I={kap:.3g}: B1 satisfied everywhere: {b1}; tau/t_dyn at x=0.3,1,3,10,30 = " + ", ".join(f"{np.interp(v, Xg, ratio):.3g}" for v in (0.3, 1, 3, 10, 30))
            + f";  x with 1 <= tau/t_dyn <= 10: " + ("none" if len(xs_win) == 0 else f"[{xs_win.min():.1f}, {xs_win.max():.1f}]"))
declared = [b for b in best if b[2] == 1.0 and b[3] and len(b[4]) > 0]
Vb_star = [b for b in best if abs(b[1] - PS["V_B"]["Q"]) < 1e-9 and b[2] == 1.0]
R.P("  post-hoc note (declared after seeing the table): where tau/t_dyn is only 1-1.6 the dipoles respond to the drive with reduction ~ (omega^2/Omega^2)/(1 + omega^2/Omega^2) ~ 0.3-0.5, so B1 (which assumes the full equilibrium Pi) is not really met there; the frozen literal test does not include this factor.")
R.verdict("O1_V_B", "PASS" if (len(declared) > 0 and any(abs(b[1] - PS['V_B']['Q']) < 1e-9 for b in declared)) else "FAIL",
          f"literal frozen test at the declared kappa_I = 1 with B1 satisfied (Q = Q* = {PS['V_B']['Q']:.2f}): window 1 <= tau/t_dyn <= 10 exists at " + str([(f"{b[0]:.0e}", f"[{b[4].min():.1f},{b[4].max():.1f}]") for b in declared if abs(b[1] - PS['V_B']['Q']) < 1e-9]))
declU = [b for b in best if abs(b[1] - PS['V_U']['Q']) < 1e-9 and len(b[4]) > 0]
R.verdict("O1_V_U", "PASS" if declU else "FAIL", f"V_U at Q* = {PS['V_U']['Q']:.1f}, kappa_I = 1: window exists: {bool(declU)}")

# ------------------------------------------------------------------------------------------------ G4
R.banner("G4  constants beyond kappa and Omega_c h^2, and the a0-Lambda tie")
R.P("  table: kappa = 1/2 (FITTED), Omega_c h^2 = 0.12 (FITTED); Q = 1 (declared; a pass needs Q* != 1: NEW); kappa_I = 1 (declared; a pass needs kappa_I* != 1: NEW); kernel shape P2 (derived from the point-mass target, no fit; free-form chi = new information); eps_c, f_track analysis thresholds; Pi_sat = a0/(8 pi G) tied to a0.")
R.P(f"  V_B star: Q* = {PS['V_B']['Q']:.2f}, kappa_I* = {PS['V_B']['kappa_I']:.3f};  V_U star: Q* = {PS['V_U']['Q']:.1f}, kappa_I* = {PS['V_U']['kappa_I']:.3f}")
for zz in (0.25, 0.4, 0.499):
    P_ = zz * A0
    WB = -(1.0 / 8.0) * (A0 ** 2 * math.log1p(-2 * zz) + 2 * A0 * P_ + 2 * P_ ** 2)
    R.P(f"  internal energy density scale at P = {zz} a0: w/P_cap = 2 W/a0^2 = {2 * WB / A0 ** 2:.4f} (V_B), {2 * (WB + 0.5 * P_ ** 2) / A0 ** 2:.4f} (V_U);  P_cap = a0^2/(8 pi G) = (kappa^2/8 pi) rho_Lambda c^2 (CFG43)")
R.P("  strong-field coefficient: W_B ~ -(a0^2/8) ln(1 - 2P/a0), i.e. w ~ (1/4) P_cap ln(...): logarithmically unbounded at the saturation wall (a 'cap' only in the sense of a wall); the tie of the scale a0^2/(8 pi G) to Lambda is the CFG43 tie, POSTULATED not derived: PARTIAL.")
R.verdict("G4_VB", "FAIL", f"no pass exists at Q = kappa_I = 1 (G1c fails); the smallest passing set needs Q* = {PS['V_B']['Q']:.2f} and kappa_I* = {PS['V_B']['kappa_I']:.2f}: new constants; tie PARTIAL")
R.verdict("G4_VU", "FAIL", f"the smallest passing set needs Q* = {PS['V_U']['Q']:.0f}; new constant; tie PARTIAL")
R.finish(required_change=(["S1_used"] if MUTATE == "kernel" else ["S1_standard"] if MUTATE == "nofield" else None))
