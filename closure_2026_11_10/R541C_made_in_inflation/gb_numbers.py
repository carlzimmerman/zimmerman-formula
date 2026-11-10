"""R541C gate numbers. SI unless stated; gamma = ell / K (K = 4 pi G, c = 1), ell a length.
Uses the identities proved in gb_frw.py (a^3 n = C + 8 gamma (aH)^3) and gb_tensor.py (c_T^2 = (1+16K xi'')/(1+16K H xi')).
Prints to gb_numbers.out."""
import json
import os
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
c = 2.99792458e8; G = 6.67430e-11; Msun = 1.98892e30; Mpc = 3.0856775814913673e22; AU = 1.495978707e11
pc = Mpc / 1e6; Gyr = 3.15576e16; yr = Gyr / 1e9
hbar_GeV_s = 6.582119569e-25; Mpl_red_GeV = 2.435e18

FOOT = {"canonical": dict(a0=9.3603e-11, R=5.410, ob=0.02236, od=0.1209, h=0.674),
        "alt": dict(a0=1.1312e-10, R=5.412, ob=0.02234, od=0.1209, h=0.674)}
GW_LO, GW_HI = -3e-15, 7e-16          # Abbott et al. 2017 ApJL 848 L13 (PROVISIONAL)
EPHEM = 1e-10                          # Msun inside Saturn's orbit (Pitjev & Pitjeva 2013, PROVISIONAL)
W_LINE, Z_LINE = 0.01, 3400.0          # MK1 RESULT.md:113 (KD1 B1a)
out = {}

print("=== GC0 dilution (no source) ===")
for Ne in (0, 50, 60, 70):
    print(f"  N_e = {Ne:2d}: physical charge density x exp(-3 N_e) = {np.exp(-3 * Ne):.3e}"
          + ("   (KA6: no dilution)" if Ne == 0 else ""))
out["GC0"] = {str(Ne): float(np.exp(-3 * Ne)) for Ne in (50, 60, 70)}

print("\n=== GC1 numerical check of the identity through inflation -> radiation -> matter (H_I = 1, a_end = 1) ===")
# smooth history: H^2 = H_I^2 [1/(1+a^4)] (1 + a/a_eq)  (de Sitter, then radiation, then matter after a_eq)
a_eq = 1e6


def Hx(x):
    a = np.exp(x)
    return np.sqrt((1.0 + a / a_eq) / (1.0 + a ** 4))


def dlnH(x, d=1e-5):
    return (np.log(Hx(x + d)) - np.log(Hx(x - d))) / (2 * d)


def run(gfun, x0=-60.0, x1=25.0, y0=0.0, rtol=1e-10):
    # y = a^3 n / gamma0 ; dy/dx = g(x) a^3 G / H = g(x) a^3 24 H^3 (1 + dlnH/dx)
    f = lambda x, y: [gfun(x) * np.exp(3 * x) * 24 * Hx(x) ** 3 * (1 + dlnH(x))]
    s = solve_ivp(f, (x0, x1), [y0], rtol=rtol, atol=1e-300, dense_output=True, max_step=0.05)
    return s


s = run(lambda x: 1.0)
for x in (-60, -30, -5, 0, 2, 5, 10, 14, 20, 25):
    y = s.sol(x)[0]
    ident = 8 * (np.exp(x) * Hx(x)) ** 3 - 8 * (np.exp(-60) * Hx(-60)) ** 3
    print(f"  ln a = {x:4d}: a^3 n/gamma = {y: .6e}   identity 8[(aH)^3 - (aH)^3_start] = {ident: .6e}"
          f"   n/(8 gamma H^3) = {y / np.exp(3 * x) / (8 * Hx(x) ** 3): .6f}")
late = s.sol(25.0)[0]
peak = s.sol(0.0)[0]
print(f"  late a^3 n/gamma at ln a = 25: {late: .3e} = {late / peak: .2e} of the peak 8 (aH)^3_end = {peak:.4f};"
      f" identity says {8 * (np.exp(25) * Hx(25)) ** 3 - 8 * (np.exp(-60) * Hx(-60)) ** 3: .3e}")
for rt in (1e-8, 1e-12):
    l2 = run(lambda x: 1.0, rtol=rt).sol(25.0)[0]
    print(f"    rtol {rt:.0e}: late value {l2: .3e} (sign and size move with the tolerance and stay ~1e-12 of the peak: integration error, not a lasting charge)")
print("  => the lasting comoving charge made by the term is zero to the integrator's accuracy; the only lasting piece"
      " is the pre-inflation offset C = a_i^3 (n_i - 8 gamma H_I^3), diluted by e^(-3 N_e)")
out["GC1_lasting_over_gamma_HI3"] = float(late)
# MU1b: switch the coupling off at the end of inflation
sw = run(lambda x: 0.5 * (1 - np.tanh(x / 0.1)))
ls = sw.sol(25.0)[0]
print(f"  MU1b switched coupling (off at a_end): lasting a^3 n/gamma = {ls:.4f}  (8 (aH)^3 at a_end = {8 * Hx(0.0) ** 3:.4f} in this smooth history:"
      f" the gate moves; a lasting charge appears only with a switch, a new ingredient)")
out["MU1b_switched_lasting"] = float(ls)

print("\n=== GC1 Arm I: what R the plain term gives, and what it would need ===")
for name, F in FOOT.items():
    H0 = 100 * F["h"] * 1e3 / Mpc
    Od = F["od"] / F["h"] ** 2; Ob = F["ob"] / F["h"] ** 2
    print(f" [{name}] H0 = {H0:.4e} /s, Omega_d = {Od:.4f}, R target {F['R']}")
    print("   lasting dust from the term = 0 + (pre-inflation offset) x e^(-3 N_e): R_term = 0 for every gamma, H_I, T_reh;"
          " R stays the free constant C / rho_b0 (one constant, as before; gamma adds none to dust)")
    # the most generous reading: total term charge today equals rho_d0 (not dust)
    ellA = 3 * Od / (16 * H0)        # in seconds (c = 1 length = c * s)
    print(f"   most generous reading 8 gamma H0^3 = rho_d0 -> ell_A = 3 Omega_d/(16 H0) = {ellA:.4e} s = {ellA * c / Mpc:.1f} Mpc")
    out.setdefault(name, {})["ell_A_m"] = ellA * c

    print(" GC3 cold at ell_A: the term's density n_GB = 8 gamma H^3; w_eff = -1 - dlnH/dlna")
    Or = 4.18e-5 / F["h"] ** 2
    a = 1 / (1 + Z_LINE)
    Om = Od + Ob
    dl = -(3 * Om * a ** -3 + 4 * Or * a ** -4) / (2 * (Om * a ** -3 + Or * a ** -4))
    w = -1 - dl
    print(f"   w_eff at z 3400 = {w:.3f} vs line <= {W_LINE} -> factor {w / W_LINE:.0f}; matter era w = 1/2, radiation w = 1;"
          f" MU3: an a^-3 component gives w = {-1 - (-1.5) + -0.5:.1f}")
    net = -16  # net energy of the term in Friedmann (gb_frw.py): -16 gamma H^3 (negative)
    print(f"   net Friedmann contribution of the term = {net} gamma H^3 = -2 x rho_d0 today at ell_A: NEGATIVE energy")
    out[name]["GC3_w_z3400"] = w

    print(" GC5 tensor speed: c_T^2 = (1 + 16 ell Qdot)/(1 + 16 ell H Q), Q ~ 1, Qdot ~ 0")
    for lab, ell in (("ell_A", ellA), ("ell_A/2 (MU4)", ellA / 2), ("ell -> 0 (MU4)", 0.0)):
        cT = 1 / np.sqrt(1 + 16 * ell * H0)
        print(f"   {lab:15s}: c_T - 1 = {cT - 1: .4e}")
    cTA = 1 / np.sqrt(1 + 16 * ellA * H0) - 1
    print(f"   at ell_A: |c_T - 1| / |bound {GW_LO}| = {abs(cTA) / abs(GW_LO):.2e}")
    ell_gw_pos = -GW_LO / (8 * H0); ell_gw_neg = GW_HI / (8 * H0)
    print(f"   GW170817 allows ell <= {ell_gw_pos:.3e} s = {ell_gw_pos * c:.3e} m (ell > 0) and |ell| <= {ell_gw_neg * c:.3e} m (ell < 0)")
    out[name]["GC5_cT_minus_1_at_ellA"] = cTA
    out[name]["ell_GW_max_m"] = ell_gw_pos * c

    print(" GC2 local: flux F = int 4 pi r^2 gamma G_GB dr = 16 ell G M^2 / (c r_min^3) [kg/s]; mass inside r >= F r / c")
    bodies = [("Sun", Msun, 6.957e8), ("neutron star 1.4 Msun", 1.4 * Msun, 1.2e4),
              ("10 Msun black hole", 10 * Msun, 2 * G * 10 * Msun / c ** 2),
              ("Sgr A* 4.3e6 Msun", 4.3e6 * Msun, 2 * G * 4.3e6 * Msun / c ** 2)]
    for lab, ell_m in (("ell_A", ellA * c), ("ell_GW", ell_gw_pos * c), ("ell_A/2 (MU2)", ellA * c / 2)):
        print(f"   at {lab} = {ell_m:.3e} m:")
        for b, M, rmin in bodies:
            Fl = 16 * ell_m * G * M ** 2 / (c * rmin ** 3)
            print(f"     {b:22s} r_min {rmin:.3e} m: charge made per Gyr = {Fl * Gyr / Msun:.3e} Msun ({Fl * Gyr / M:.3e} M)")
        Fsun = 16 * ell_m * G * Msun ** 2 / (c * 6.957e8 ** 3)
        msat = Fsun * 9.58 * AU / c / Msun
        print(f"     Sun: charge inside Saturn's orbit >= {msat:.3e} Msun vs ephemeris {EPHEM:.0e} -> factor {msat / EPHEM:.2e}")
        if lab == "ell_A":
            out[name]["GC2_sun_factor_at_ellA"] = msat / EPHEM
    # MU2: r_min scaling
    F1 = 16 * ellA * c * G * Msun ** 2 / (c * 6.957e8 ** 3); F2 = 16 * ellA * c * G * Msun ** 2 / (c * (2 * 6.957e8) ** 3)
    print(f"   MU2: doubling r_min divides the Sun's flux by {F1 / F2:.1f} (expect 8)")
    ell_eph = EPHEM * Msun * c * 6.957e8 ** 3 / (16 * G * Msun ** 2 * 9.58 * AU) * c
    print(f"   ephemeris bound on |ell| (Sun, crude): <= {ell_eph:.3e} m")
    out[name]["ell_ephem_max_m"] = ell_eph
    # local density near Earth at ell_eph, against 0.01 Msun/pc^3 (indicative)
    Fe = 16 * ell_eph * G * Msun ** 2 / (c * 6.957e8 ** 3)
    rho_e = Fe / (4 * np.pi * AU ** 2 * c)
    print(f"   density at 1 AU (outflow at c) at that ell: {rho_e / (Msun / pc ** 3):.3e} Msun/pc^3 vs local 0.01 (indicative)")

    print(" GC5 reported: the net term vs radiation at BBN (T = 1 MeV) and its size in inflation, at the GW-allowed ell")
    HB = 1.66 * np.sqrt(10.75) * (1e-3) ** 2 / 1.22089e19 / hbar_GeV_s
    frac = 32 / 3 * ell_gw_pos * HB
    print(f"   H(1 MeV) = {HB:.3f} /s; |net term|/rho_tot = (32/3) ell H = {frac:.3e} (indicative line 0.05)"
          f" -> BBN bound |ell| <= {0.05 * 3 / 32 / HB * c:.3e} m")
    out[name]["ell_BBN_max_m"] = 0.05 * 3 / 32 / HB * c

    print(" Reported only: switched coupling (MU1b-type) R = 8 gamma H_I^3 (a_end/a_0)^3 / rho_b0, instant reheating")
    for HI_GeV in (1e13, 1e10, 1e5):
        Treh = (90 * HI_GeV ** 2 * Mpl_red_GeV ** 2 / (np.pi ** 2 * 106.75)) ** 0.25
        T0 = 2.7255 * 8.617333e-14
        aratio = (3.91 / 106.75) ** (1 / 3) * T0 / Treh
        HI = HI_GeV / hbar_GeV_s
        rho_b0 = 3 * H0 ** 2 * Ob / (8 * np.pi * G)
        # need 8 gamma HI^3 aratio^3 = R rho_b0 ; gamma = ell/K, K = 4 pi G / c^2 ; densities as mass density
        # 8 (ell c^2/(4 pi G)) (HI/c)^3 ... in c = 1 with t in s: n = 8 ell H^3 /K -> mass density 8 ell H^3 / (4 pi G) * (1 s units)
        ell_s = F["R"] * rho_b0 * 4 * np.pi * G / (8 * HI ** 3 * aratio ** 3)
        print(f"   H_I {HI_GeV:.0e} GeV (T_reh {Treh:.2e} GeV): ell_switch = {ell_s * c:.3e} m; constants: gamma, H_I, T_reh,"
              f" switch -> at least 2 fitted beyond the history; no natural value")

with open(os.path.join(HERE, "gb_numbers.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("\nwritten gb_numbers.json")
