"""X76_galaxy_fair_share_halos: shared source patches (criteria 5775b7d6b3).
SMOOTH: X70/X73 smooth core (as X74_smooth_core_lensing).  FAIR: the clusters' native fair-share rule for galaxy halos,
M_fair = R_nat * M_b,tot inside the self-consistent r_ta (X30's r_ta_com, native), truncated at r_ta; budget multiplier
10**dlM on M_b,tot when cfg_h carries dlM. Switched by the namespace globals FAIR_ON / FAIR_Z.
kappa = 1/2 FITTED; c_f EXTERNAL; not theory closed.
"""
import math
NAT_OM, NAT_h, NAT_wb = 0.2976016, 0.6856427, 0.0223081
NAT_OB = NAT_wb / NAT_h ** 2; RNAT = (NAT_OM - NAT_OB) / NAT_OB; DTA = 5.55
_G, _MSUN, _MPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e22    # X30's SI constants
_H0 = NAT_h * 100e3 / _MPC
RHOM0_PC = NAT_OM * 3 * _H0 ** 2 / (8 * math.pi * _G) / _MSUN * (_MPC / 1e6) ** 3   # native mean matter density today, Msun/pc^3 (comoving)


def rta_pc(Mb, z):
    """X30's r_ta_com at native parameters, physical (pc): [3 (Om/Ob) Mb / (4 pi DTA rho_m0)]^(1/3) / (1+z)."""
    return (3 * (NAT_OM / NAT_OB) * Mb / (4 * math.pi * DTA * RHOM0_PC)) ** (1 / 3) / (1 + z)


SMOOTH = (("def B(x):\n    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)\n",
           "def B(x):\n    x = np.asarray(x, float)\n    return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))\n"),
          ("    return 4.0 / (3.0 * B1) * cf ** 1.25\n", "    return 4.0 / (3.0 * B1) * cf ** 1.25 * B1 / float(B(1.0))\n"),
          ("(St / r0t) * r0t ** 3 / ((r + r0t) * (r * r + r0t * r0t))", "(St / r0t) * r0t ** 3 / (r * r + r0t * r0t) ** 1.5"))
FAIR_CODE = '''
def FAIR_SETUP(foot, Ms, Mc, Mhot, cfg_h):
    """X76 fair-share galaxy halo: (M_fair, r_ta, r0, Sigma_core, above-floor)."""
    Mbt = (Ms + Mc + Mhot) * 10 ** cfg_h.get("dlM", 0.0)
    Mf = X76_RNAT * Mbt; rta = X76_RTA(Mbt, FAIR_Z)
    sc = eta_of(Mf + Mbt, cfg_h["cf"]) * sigma_coll(Mf + Mbt); Sig = max(SIGA0[foot], sc)
    return Mf, rta, solve_r0(Mf, rta, Sig), Sig, sc > SIGA0[foot]


def mass_H('''
FAIR = (("\ndef mass_H(", FAIR_CODE),
        ("    M200, R200, r0, Sig, above = halo_setup(foot, math.log10(Ms + Mc), cfg_h)\n",
         "    M200, R200, r0, Sig, above = (FAIR_SETUP(foot, Ms, Mc, Mhot, cfg_h) if FAIR_ON else halo_setup(foot, math.log10(Ms + Mc), cfg_h))\n"))


def patch(src, smooth=True, fair=True):
    for a, b in (SMOOTH if smooth else ()) + (FAIR if fair else ()):
        assert src.count(a) == 1, (a[:60], src.count(a)); src = src.replace(a, b)
    return src


def ns_globals(on, z):
    return {"FAIR_ON": on, "FAIR_Z": z, "X76_RNAT": RNAT, "X76_RTA": rta_pc}
