#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG171 S3 -- door 11A, gates G2 (cosmology/background), G3 (reaction and energy), G5 (Solar System, well-posedness) and G7 (frame
dependence of a0) for the candidate flow laws of FROZEN_QUESTION.md.  G1 is S2; the symbolic facts used here are S1.

  G2  the L4 flow (the only one that carries the law) with the minimal normalisation: v = 0 at the zero-gravity radius r* where
      g_law(r*) = H^2 r*, inflow inside, Hubble outflow outside; pass |v/(H r) - 1| <= 0.05 at r = 10 r*.  Growth/CMB: UNDEFINED.
  G3  L4 read as a LITERAL medium of inertial density rho_Lambda/c^2 (the potential reading has no medium: reaction 0, energy 0, p*):
      (i) fraction of the medium's required creation/destruction |s| = |r^-2 (r^2 rho_m v)'| lying where rho_b < 1e-3 rho_b(0)
      (exp sphere; pass <= 0.10, the 'boost localised on the baryons' claim); (ii) reaction |s v|/(rho_b g_law), x in [0.3, 30]
      (pass <= 0.10); (iii) the flow's kinetic-energy flux 4 pi r_e^2 rho_m |v|^3/2 over t = 1/H against (1/2) M_b V_f^2, r_e = 0.4 r_ta
      in both conventions (A: CFG48 Gcommon collapse mass; B: the P2 point-mass M_dyn), pass <= 1.
  G5  monopole anomaly at Earth and Mars vs the record's Sereno-Jetzer 2-sigma inversion (control: 3.66e-14, 3.72e-14; a0/2 is 1278x);
      the Milky Way's phantom tide at the Sun (control: CFG7 H1's committed numbers); Q2 for a Sun that owns its inflow is CITED from
      GATES 4.01 (4.0-5.7x the 5.2e-27 ceiling), not recomputed.
  G7  L1 read literally in the Hubble-flow (CMB) frame: the -grad(v_N rhat.w) term against g_target at x = 1, 10 for w = 100-600 km/s
      (pass <= 0.10); L0 (GR covariant) and L4 (S1 identity 1g) give 0 exactly.

MUTATE --mutate a : the target kernel for L4's Solar-System row is the alpha = 2 kernel -> the monopole row must flip to PASS (exit 1).
Runs in seconds.
"""
import sys
sys.dont_write_bytecode = True
import os, math, json  # noqa: E401,E402
import numpy as np  # noqa: E402
from scipy.optimize import brentq  # noqa: E402
import cfg171_common as C  # noqa: E402

MODE = C.parse_mode(sys.argv, ["a"])
R = C.Report("cfg171_s3_gates", MODE)
P, check = R.P, R.check
P(f"CFG171 S3 -- G2, G3, G5, G7 for the door-11A flow laws (mode: {'MAIN' if MODE is None else 'MUTATE_' + MODE})")
FOOTS = ("canonical", "alt")
sys.path.insert(0, os.path.join(C.REPO, "campaign_fresh_gravity", "CFG48_gap1_switch"))
import Gcommon as GC  # noqa: E402  (read-only import, for the r_ta control)


def g_law(prof, r, foot, kernel="P2"):
    gN = prof.u(r) / r ** 2
    return C.KERNELS[kernel](gN / C.a0_kpc(foot)) * gN


def flow_L4(prof, foot, kernel="P2", n=40001):
    """the L4 flow with the minimal normalisation: returns r grid, v(r) (negative = inflow), Psi, r*."""
    H2 = C.H_kpc(foot) ** 2
    rM = math.sqrt(C.G * prof.Mtot / C.a0_kpc(foot))
    fz = lambda lr: float(g_law(prof, np.array([math.exp(lr)]), foot, kernel)[0] - H2 * math.exp(lr))
    rstar = math.exp(brentq(fz, math.log(rM), math.log(1e8), xtol=1e-12))
    rr = np.geomspace(1e-3 * rM, 100.0 * rstar, n)
    f = g_law(prof, rr, foot, kernel) - H2 * rr                      # dPsi/dr = -f
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(rr))])   # int_{r0}^{r} f
    cstar = np.interp(math.log(rstar), np.log(rr), cum)
    # Psi(r) = int_r^{r*} f for r < r*, and int_{r*}^r (-f) for r > r*: both equal cstar - cum(r), >= 0 because cum peaks at r*
    Psi = np.maximum(cstar - cum, 0.0)
    v = np.where(rr < rstar, -1.0, 1.0) * np.sqrt(2.0 * Psi)
    return rr, v, Psi, rstar


def r_ta_A(Mb):
    Mcol = Mb * (1.0 + B_OCB)
    return 1e3 * (3.0 * Mcol / (4.0 * math.pi * RHO_M_MPC * DELTA_TA)) ** (1.0 / 3.0)


def r_ta_B(Mb, foot):
    """CFG4-style: the radius where the P2 point-mass law's enclosed dynamical mass M_b sqrt(1 + x^2) has mean density Delta_ta rho_m."""
    rM = C.r_M(Mb, foot)
    rho_m_kpc = RHO_M_MPC / 1e9
    f = lambda lr: math.log(3 * Mb * math.sqrt(1 + (math.exp(lr) / rM) ** 2) / (4 * math.pi * math.exp(3 * lr))) - math.log(DELTA_TA * rho_m_kpc)
    return math.exp(brentq(f, math.log(1.0), math.log(1e6)))


OM, HH, DELTA_TA = 0.3153, 0.6736, 11.81                               # CFG48 Gcommon's cosmology (read-only values)
RHO_M_MPC = OM * 2.775e11 * HH ** 2
B_OCB = C.B.OMEGA_C_OVER_B

# ================================================================================================================== G2
R.banner("G2  background: the L4 flow reduces to the Hubble (de Sitter) outflow beyond the zero-gravity radius r*")
G2 = {}
for foot in FOOTS:
    for kernel in ("P2", "nu_mono"):
        for Mb in C.MASSES:
            for fam in ("point", "exp_hCFG118"):
                prof = C.profiles(Mb, foot)[fam]
                rr, v, Psi, rstar = flow_L4(prof, foot, kernel)
                H = C.H_kpc(foot)
                dev = float(abs(np.interp(math.log(10 * rstar), np.log(rr), v) / (H * 10 * rstar) - 1))
                r_gr = (C.G * Mb / H ** 2) ** (1.0 / 3.0)
                Vf = (C.G * Mb * C.a0_kpc(foot)) ** 0.25
                G2[f"{foot}|{kernel}|{Mb:.0e}|{fam}"] = dict(r_star_kpc=rstar, r_star_over_Vf_over_H=rstar / (Vf / H), r_star_GR_kpc=r_gr,
                                                            r_star_over_rta_A=rstar / r_ta_A(Mb), dev_at_10rstar=dev, v_at_rM=float(np.interp(math.log(C.r_M(Mb, foot)), np.log(rr), v)))
                if fam == "point" and kernel == "P2":
                    P(f"    {foot:9s} {kernel:7s} M_b = {Mb:.0e}: r* = {rstar:8.0f} kpc (= {rstar / (Vf / H):.3f} V_f/H; GR's zero-gravity radius {r_gr:6.0f} kpc; "
                      f"r*/r_ta(A) = {rstar / r_ta_A(Mb):.2f}); |v/(Hr) - 1| at 10 r* = {dev:.3f}; inflow speed at r_M {abs(G2[f'{foot}|{kernel}|{Mb:.0e}|{fam}']['v_at_rM']):.0f} km/s")
g2_ok = all(d["dev_at_10rstar"] <= 0.05 for d in G2.values())
R.num("G2", G2)
if MODE is None:
    check("G2 background: with the minimal normalisation the L4 flow is an inflow inside r* ~ V_f/H and the Hubble outflow outside, |v/(Hr) - 1| <= 0.05 "
          "at 10 r* on every mass, kernel, profile and footing (kinematic only; growth and CMB UNDEFINED: 11A is defined per bound system)",
          f"max deviation {max(d['dev_at_10rstar'] for d in G2.values()):.3f}", g2_ok)

# ================================================================================================================== G3
R.banner("G3  L4 as a LITERAL medium: where it must be created/destroyed, the reaction if the baryons absorb it, the energy it carries in")
P("    frozen reading: inertia rho_Lambda/c^2 (a dust-like medium of Lambda's density).  Addendum 2 (the owner: no rest mass, not a particle) "
  "adds the massless readings: w = -1 has NO velocity (S1 1d); w = 1/3 (radiation-like) has inertia (4/3) rho_Lambda/c^2 and also advects "
  "its enthalpy (1+w) rho_Lambda c^2 v, which is (c/v)^2 larger than the kinetic flux.  All rows reported.")
if MODE is None:
    rA = {Mb: r_ta_A(Mb) for Mb in C.MASSES}
    ctl = max(abs(rA[Mb] / GC.r_ta_kpc(Mb) - 1) for Mb in C.MASSES)
    ratio_BA = {Mb: r_ta_B(Mb, "canonical") / rA[Mb] for Mb in C.MASSES}
    R.num("C3_ratio_B_over_A", {f"{Mb:.0e}": q for Mb, q in ratio_BA.items()})
    check("C3a CONTROL: r_ta(A) reproduces CFG48 Gcommon.r_ta_kpc to 1e-12", f"max |A/Gcommon - 1| = {ctl:.1e}", ctl < 1e-12)
    check("C3 CONTROL (as frozen): the CFG4-style r_ta(B) is 1.7-3.6x r_ta(A) at every mass 1e9-1e12 (the CFG48 referee's range)",
          f"B/A = {[round(q, 3) for q in ratio_BA.values()]}", all(1.7 <= q <= 3.6 for q in ratio_BA.values()))
    edges = {Mb: 0.4 / ratio_BA[Mb] for Mb in (1e10, 1e11, 1e12)}
    check("C3b (reported, added after C3 fell): the referee's range was quoted for M_b = 1e10-1e14 (edges 0.11, 0.13, 0.16 r_ta at 1e10-1e12); "
          "B reproduces those edges to their rounding, so C3's failure is the 1e9 point outside the quoted range",
          f"0.4 A/B at 1e10, 1e11, 1e12 = {[round(q, 3) for q in edges.values()]}",
          all(abs(round(edges[Mb], 2) - t) < 1e-9 for Mb, t in zip((1e10, 1e11, 1e12), (0.11, 0.13, 0.16))), load_bearing=False)
G3 = {}
for foot in FOOTS:
    rho_m = C.rho_lambda_kpc(foot)
    H = C.H_kpc(foot)
    for Mb in C.MASSES:
        for fam in ("point", "exp_hCFG118"):
            prof = C.profiles(Mb, foot)[fam]
            rr, v, Psi, rstar = flow_L4(prof, foot, "P2")
            flux = rr ** 2 * rho_m * v
            s = np.gradient(flux, rr) / rr ** 2                                  # Msun/kpc^3 per (kpc/(km/s))
            inside = rr < rstar
            dV = 4 * math.pi * rr ** 2
            tot = np.trapz(np.abs(s[inside]) * dV[inside], rr[inside])
            rec = dict(r_star=rstar)
            if fam == "exp_hCFG118":
                rho_b = prof.rho_b(rr)
                off = inside & (rho_b < 1e-3 * prof.rho_b(np.array([1e-6]))[0])
                rec["frac_off_baryons"] = float(np.trapz(np.abs(s[off]) * dV[off], rr[off]) / tot)
                x = rr / C.r_M(Mb, foot)
                with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
                    reac = np.abs(s * v) / (rho_b * g_law(prof, rr, foot))
                for xx in (0.3, 1.0, 3.0):
                    rec[f"reaction_at_x{xx:g}"] = float(np.interp(math.log(xx), np.log(x), reac))
                win = (x >= 0.3) & (x <= 30)
                bad = win & ~(reac <= 0.10)
                rec["x_first_over_0.10"] = float(x[bad][0]) if bad.any() else None
                rec["reaction_passes_x0.3_30"] = not bad.any()
            else:
                rec["frac_off_baryons"] = 1.0                                     # a point mass has no volume: all of it is off the baryons
            Vf2 = math.sqrt(C.G * Mb * C.a0_kpc(foot))
            Eb = 0.5 * Mb * Vf2
            for conv, rt in (("A", r_ta_A(Mb)), ("B", r_ta_B(Mb, foot))):
                re = 0.4 * rt
                ve = abs(float(np.interp(math.log(re), np.log(rr), v)))
                t_ = 1.0 / H
                E_kin = 4 * math.pi * re ** 2 * rho_m * ve ** 3 / 2.0 * t_                       # frozen: inertia rho_Lambda
                E_kin_rad = (4.0 / 3.0) * E_kin                                                   # Addendum 2: w = 1/3, inertia (4/3) rho_Lambda
                E_enth_rad = 4 * math.pi * re ** 2 * (4.0 / 3.0) * rho_m * C.C_KMS ** 2 * ve * t_  # Addendum 2: enthalpy flux (1+w) rho c^2 v
                rec[f"E_over_Eb_{conv}"] = E_kin / Eb
                rec[f"E_over_Eb_{conv}_w1/3_kin"] = E_kin_rad / Eb
                rec[f"E_over_Eb_{conv}_w1/3_enthalpy"] = E_enth_rad / Eb
                rec[f"v_at_re_{conv}"] = ve
            G3[f"{foot}|{Mb:.0e}|{fam}"] = rec
            line = f"    {foot:9s} M_b = {Mb:.0e} {fam:12s}: off-baryon fraction {rec['frac_off_baryons']:.3f}"
            if fam != "point":
                xf = rec["x_first_over_0.10"]
                line += (f"; reaction at x = 0.3/1/3: {rec['reaction_at_x0.3']:.1e}/{rec['reaction_at_x1']:.1e}/{rec['reaction_at_x3']:.1e} g_law, "
                         f"> 0.10 from x = {xf:.2f}" if xf else "")
            line += (f"; energy in over 1/H: {rec['E_over_Eb_A']:.1f} (A), {rec['E_over_Eb_B']:.1f} (B); massless w=1/3 enthalpy "
                     f"{rec['E_over_Eb_A_w1/3_enthalpy']:.1e} (A) x (1/2) M_b V_f^2")
            P(line)
R.num("G3_literal_medium", G3)
frac_ok = all(d["frac_off_baryons"] <= 0.10 for d in G3.values())
reac_ok = all(d.get("reaction_passes_x0.3_30", True) for d in G3.values())
en_ok = all(d["E_over_Eb_A"] <= 1 and d["E_over_Eb_B"] <= 1 for d in G3.values())
if MODE is None:
    check("G3(i) the literal medium CANNOT be destroyed only on the baryons: the fraction of its required creation/destruction that lies off the baryons "
          "exceeds 0.10 on every case (point mass: all of it) -- 'the boost is localised on the baryons' is false for the flow that carries the law",
          f"min fraction {min(d['frac_off_baryons'] for d in G3.values()):.3f}", not frac_ok)
    xs_first = [d["x_first_over_0.10"] for d in G3.values() if d.get("x_first_over_0.10")]
    check("G3(ii) reaction if the baryons absorb the destroyed momentum: small inside the baryons (x ~ 1) but it exceeds 0.10 g_law inside x in [0.3, 30] "
          "on every exp-sphere case, where the baryon density runs out and the medium must still be destroyed (FAIL of the pass line)",
          f"first x over 0.10: {[round(q, 2) for q in xs_first]}", not reac_ok)
    check("G3(iii) energy the literal medium carries into r_e over 1/H exceeds the baryons' (1/2) M_b V_f^2 in both r_ta conventions (frozen dust-like reading); "
          "the massless w = 1/3 reading adds an enthalpy flux ~(c/v)^2 larger (FAIL of the pass line)",
          f"frozen: min {min(min(d['E_over_Eb_A'], d['E_over_Eb_B']) for d in G3.values()):.1f}, max {max(max(d['E_over_Eb_A'], d['E_over_Eb_B']) for d in G3.values()):.1f}; "
          f"w=1/3 enthalpy min {min(d['E_over_Eb_A_w1/3_enthalpy'] for d in G3.values()):.1e}", not en_ok)

# ================================================================================================================== G5
R.banner("G5  Solar System: monopole anomaly at Earth and Mars; the host tide; Q2 (cited)")
GM_SUN, AU = 1.32712440018e20, 1.495978707e11                 # the record's mi_alpha1_solar_system_2026.py values
SJ = {"Earth": (1.0, 1.0, 0.0167, 0.4e-5), "Mars": (1.5237, 1.8808, 0.0934, 0.5e-5)}   # a (AU), P (yr), e, 1-sigma (arcsec/yr): S&J 2006 Table 1
BOUND = {}
for nm, (a_au, Pyr, ecc, sig) in SJ.items():
    dw = 2 * sig * (math.pi / 180 / 3600) / 3.155693e7
    n_ = 2 * math.pi / (Pyr * 3.155693e7)
    BOUND[nm] = dw * n_ * (a_au * AU) / math.sqrt(1 - ecc ** 2)
if MODE is None:
    rec1278 = (C.A0_SI["canonical"] / 2) / BOUND["Earth"]
    check("C5 CONTROL: the Sereno-Jetzer 2-sigma inversion reproduces the record's Earth 3.66e-14 and Mars 3.72e-14 m/s^2 (1%) and a0/2 = 1278x the Earth bound",
          f"Earth {BOUND['Earth']:.3e}, Mars {BOUND['Mars']:.3e}; a0/2 / Earth = {rec1278:.0f}",
          abs(BOUND["Earth"] / 3.66e-14 - 1) < 0.01 and abs(BOUND["Mars"] / 3.72e-14 - 1) < 0.01 and abs(rec1278 / 1278 - 1) < 0.005)
G5 = {}
k_L4 = "alpha2" if MODE == "a" else "P2"


def nu_minus_1(kernel, y):
    """nu(y) - 1 in cancellation-free form (P2: (1/y)/(sqrt(1+1/y)+1); alpha2: (q/2)/(nu+1), q = (4/y^2)/(sqrt(1+4/y^2)+1))."""
    if kernel == "P2":
        return (1.0 / y) / (math.sqrt(1.0 + 1.0 / y) + 1.0)
    if kernel == "alpha2":
        q = (4.0 / y ** 2) / (math.sqrt(1.0 + 4.0 / y ** 2) + 1.0)
        return (q / 2.0) / (math.sqrt(1.0 + q / 2.0) + 1.0)
    return float(C.KERNELS[kernel](y)) - 1.0
for foot in FOOTS:
    a0 = C.A0_SI[foot]
    H = C.H_si(foot)
    for nm, (a_au, Pyr, ecc, sig) in SJ.items():
        r = a_au * AU
        gN = GM_SUN / r ** 2
        y = gN / a0
        an = {"L0 (GR, outward)": H * H * r,
              "L1 (own frame)": H * math.sqrt(GM_SUN / (2 * r)),
              f"L4 {k_L4}": nu_minus_1(k_L4, y) * gN,
              "L4 nu_mono (reported)": (float(C.nu_mono(y)) - 1) * gN,
              "L4 simple (reported)": (float(C.nu_simple(y)) - 1) * gN}
        G5[f"{foot}|{nm}"] = {k: dict(anomaly=v, over_bound=v / BOUND[nm]) for k, v in an.items()}
        P(f"    {foot:9s} {nm:5s} (bound {BOUND[nm]:.2e}): " + ";  ".join(f"{k}: {v:.2e} m/s^2 = {v / BOUND[nm]:.3g}x" for k, v in an.items()))
R.num("G5_monopole", G5)
R.num("G5_bounds", BOUND)
l4_mono_ok = all(G5[k][f"L4 {k_L4}"]["over_bound"] <= 1 for k in G5)
l1_mono = max(G5[k]["L1 (own frame)"]["over_bound"] for k in G5)
# host tide (CFG7 H1 replicated with its own constants) -- the only non-Newtonian tide if the Sun owns NO inflow
Gh, kpc_h, Msun_h = 6.674e-11, 3.0857e19, 1.989e30
R0 = 8.2 * kpc_h
MD, RD, MBUL, ABUL, MGAS, RGAS = 4.5e10, 2.6, 0.9e10, 0.5, 1.2e10, 5.0
M_exp = lambda Md, Rd, Rm: Md * (1 - (1 + Rm / (Rd * kpc_h)) * math.exp(-Rm / (Rd * kpc_h)))
gN_MW = lambda Rm: Gh * (M_exp(MD, RD, Rm) + M_exp(MGAS, RGAS, Rm) + MBUL * (Rm / kpc_h) ** 2 / (Rm / kpc_h + ABUL) ** 2) * Msun_h / Rm ** 2
TIDE = {}
for foot in FOOTS:
    for kn in ("P2", "nu_mono"):
        a0 = C.A0_SI[foot]
        gph = lambda Rm: (float(C.KERNELS[kn](gN_MW(Rm) / a0)) - 1.0) * gN_MW(Rm)
        dR = 0.01 * R0
        tide = max(abs((gph(R0 + dR) - gph(R0 - dR)) / (2 * dR)), gph(R0) / R0)
        TIDE[f"{foot}|{kn}"] = tide
committed = json.load(open(os.path.join(C.REPO, "campaign_fresh_gravity", "CFG7_hierarchy_fg001_results.json")))["numbers"]["H1"]
tide_dev = max(abs(TIDE[k] / committed[k]["tide"] - 1) for k in TIDE)
R.num("G5_host_tide", TIDE)
P(f"    host (Milky Way) phantom tide at the Sun: " + ", ".join(f"{k} {v:.2e} s^-2 (margin {5.2e-27 / v:.1e})" for k, v in TIDE.items()))
P("    Q2 for a Sun that owns its own inflow (11A read literally: 'each bound system'): CITED from closure_map/GATES.md row 4.01, "
  "'Strict law would be 4.0-5.7x the ceiling' (5.2e-27 s^-2); not recomputed here")
if MODE is None:
    check("C6 CONTROL: the Milky Way phantom tide at the Sun reproduces CFG7 H1's committed values (1e-3) on both footings and kernels",
          f"max relative deviation {tide_dev:.1e}", tide_dev < 1e-3)
    check("G5-L4 (P2) FAILS the planets: the law's alpha = 1 tail gives a constant sunward ~a0/2, 1.2-1.5e3x the Earth/Mars bounds on both footings -- "
          "a property of the TARGET, which the flow neither causes nor cures",
          f"min over cases {min(G5[k]['L4 P2']['over_bound'] for k in G5):.0f}x", not l4_mono_ok)
    check("G5-L1 (own frame) monopole anomaly H sqrt(GM/2r) at Earth/Mars (reported as computed; ~1x the bound)",
          f"max {l1_mono:.2f}x the bound", True, load_bearing=False)
    mono_nm = max(G5[k]["L4 nu_mono (reported)"]["over_bound"] for k in G5)
    hE = float((C.nu_mono(GM_SUN / AU ** 2 / C.A0_SI["canonical"]) - 1) * GM_SUN / AU ** 2 / C.A0_SI["canonical"])
    check("G5-L4 nu_mono monopole at Earth/Mars (reported): the record's monotone repair keeps h(y) = (nu - 1) y NON-DECREASING (floor 0.05 H_P/(y + Y_P) "
          "on h'), so the phantom h(y) a0 never falls below H_P a0 = 0.648 a0 at high g and grows logarithmically -- an alpha = 1-like tail, WORSE than P2's a0/2 "
          "(not the exponential tail of nu_RAR); relevant only if the Sun owns its inflow",
          f"h(y_Earth) = {hE:.3f} (a0 units); max {mono_nm:.3g}x the bound", hE > 0.648, load_bearing=False)

# ================================================================================================================== G7
R.banner("G7  frame dependence: a system moving at w through the flow's frame")
G7 = {}
for foot in FOOTS:
    H = C.H_kpc(foot)
    for Mb in C.MASSES:
        for x in (1.0, 10.0):
            r = x * C.r_M(Mb, foot)
            gN = C.G * Mb / r ** 2
            gt = float(C.nu_p2(gN / C.a0_kpc(foot))) * gN
            for w in (100.0, 300.0, 600.0):
                extra = w * math.sqrt(2 * C.G * Mb) * r ** -1.5 + H * w          # max over angle of |grad(v_N rhat.w)| + the uniform H w
                G7[f"{foot}|{Mb:.0e}|x{x:g}|w{w:g}"] = extra / gt
    P(f"    {foot:9s} L1 literal (Hubble-flow frame): extra force / g_target at x = 1, w = 600 km/s: "
      + ", ".join(f"{Mb:.0e}: {G7[f'{foot}|{Mb:.0e}|x1|w600']:.2f}" for Mb in C.MASSES)
      + ";  at w = 100: " + ", ".join(f"{G7[f'{foot}|{Mb:.0e}|x1|w100']:.2f}" for Mb in C.MASSES))
sun = 370e3 * math.sqrt(2 * GM_SUN) * AU ** -1.5 / (GM_SUN / AU ** 2)
P(f"    the Sun at 1 AU moving at 370 km/s through the Hubble-flow frame under L1: extra force = {sun:.1f} x the Sun's Newtonian pull")
R.num("G7_L1_literal", G7)
R.num("G7_sun_L1", sun)
if MODE is None:
    check("G7-L1 a literal linear superposition in the Hubble-flow frame FAILS: the frame term is >= 10% of the law already at w = 100 km/s on every mass "
          "(and ~17x the Sun's Newtonian pull at 1 AU for the CMB-dipole speed); L0 (GR) and L4 (the Hamilton-Jacobi congruence, S1 1g) are exactly frame-free",
          f"min over cases {min(G7.values()):.2f}; Sun {sun:.1f}", min(G7.values()) > 0.10 and sun > 1)

nf = R.write()
if MODE == "a":
    P(f"  MUTATE a: with the alpha = 2 kernel L4's monopole {'PASSES' if l4_mono_ok else 'still fails'} the planets -> "
      f"{'exit 1 (control bites)' if l4_mono_ok else 'control broken'}")
    sys.exit(1 if l4_mono_ok else 0)
sys.exit(1 if nf else 0)
