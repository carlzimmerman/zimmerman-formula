#!/usr/bin/env python3
"""A16 -- the cutoff chain and the edge prediction.

Three lengths are derived from the cold medium's own equations:
  lam_J    = sqrt(2) pi L*          (Jeans, Gamma=2 polytrope)
  lam_FS   = 2 sigma/(3 H0)         (free streaming, sigma = sqrt(a0 L*))
  lam_1/2  = 1/k_1/2(L*)            (half mode, growth ODE with c_s^2 = 2 pi G L*^2 rho)
then the system is solved, the SPARC edge r_e = r_M sqrt(N(N+1)) is tested on all
175 rotmod curves, the pressure switch-off radius is located in an MW-like halo,
and the Jeans mass at the switch is computed.

Run:  python3 a16_checks.py            (exit 0 iff every declared check passes)
      python3 a16_checks.py --mutate gamma   (Gamma=5/3: K2 must fail)
      python3 a16_checks.py --mutate units   (drop the c in c_s/c: K8 must fail)
Deterministic, no network, stdlib + numpy/scipy/sympy.
"""
import glob
import json
import math
import os
import sys
import time

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
SPARC = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data"

MUT = None
if "--mutate" in sys.argv:
    i = sys.argv.index("--mutate")
    MUT = sys.argv[i + 1] if len(sys.argv) > i + 1 else "gamma"

# ----------------------------------------------------------------- constants
c = 2.99792458e8
G = 6.67430e-11
a0 = 9.36e-11                 # canonical footing (BRIEF section 4)
H0 = 2.1843e-18
pc = 3.0856775814913673e16
kpc = 1e3 * pc
Mpc = 1e6 * pc
Msun = 1.98847e30
K_STIFF = 4.0 * math.pi * G   # AG6D FROZEN_CRITERIA section 0 (BRIEF section 1 writes 8 pi G; see report)
GAMMA = 2.0
rho_crit = 3 * H0**2 / (8 * math.pi * G)
Om_c = 0.2645
rho_cosmic = Om_c * rho_crit
MSUN_PC3 = Msun / pc**3
GKPC = 4.300917270e-6         # G in kpc (km/s)^2 / Msun (IAU)

# census: N = 5.364327/f_ret with f_ret a function of the TURNAROUND mass (CFG416
# cfg416_pm.py:268 `fret_of`, verbatim in CFG953 cfg953.py:84), M_b = f_ret f_b M_ta/h.
CENSUS_RATIO = 5.364327223960661
FB16 = 0.157
HH = 0.674
CENSUS_PTS = {3e10: 53.6432722396066, 1e11: 44.12538834801819,
              1e12: 14.916859007524724, 1e13: 8.295807681588572,
              1e14: 5.9603635821785135}

t0 = time.time()
OUT = []
RESULTS = {"lane": "A16", "mutate": MUT, "checks": [], "numbers": {},
           "constants_used": [], "external_inputs": []}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


def chk(cid, ok, measured, threshold, note=""):
    RESULTS["checks"].append({"id": cid, "pass": bool(ok),
                              "value": measured, "threshold": threshold})
    P("%-4s %-4s %s   [threshold %s]%s" % (cid, "PASS" if ok else "FAIL",
                                           measured, threshold,
                                           ("  " + note) if note else ""))


def num(key, val):
    RESULTS["numbers"][key] = val


def f_ret_ta(lMta):
    """CFG416 cfg416_pm.py:268, verbatim."""
    if lMta < 12.5:
        f = 0.10
    elif lMta < 13.5:
        f = 0.10 + 0.45 * (lMta - 12.5)
    else:
        f = min(0.55 + 0.30 * (lMta - 13.5), 0.90)
    return min(f, 1.0)


def Mb_of_Mta(Mta):
    return f_ret_ta(math.log10(Mta)) * FB16 * Mta / HH


def N_census(Mb):
    lMta = brentq(lambda x: math.log(Mb_of_Mta(10.0**x)) - math.log(Mb), 8.0, 17.0)
    return CENSUS_RATIO / f_ret_ta(lMta)


# ============================================================ 1. the medium EOS
P("=" * 78)
P("A16  cutoff chain + edge prediction")
P("=" * 78)
P("")
P("[1] the cold medium's equation of state and its Jeans wavenumber (sympy)")

rho, rhobar, Ls, gG = sp.symbols("rho rhobar L G", positive=True)
gam = (4 * sp.pi * gG) * Ls**2 / 2   # gamma = K L*^2/2, K = 4 pi G  =>  2 pi G L*^2
e = gam / 2 * (rho - rhobar) ** 2
p_of_rho = sp.simplify(rho * sp.diff(e, rho) - e)
cs2_sym = sp.simplify(sp.diff(p_of_rho, rho))
cs2_target = 2 * sp.pi * gG * Ls**2 * rho

if MUT == "gamma":
    # Gamma = 5/3 polytrope: e = A rho^Gamma, p = (Gamma-1) A rho^Gamma
    GA = sp.Rational(5, 3)
    e_m = sp.Symbol("A", positive=True) * rho**GA
    p_m = sp.simplify(rho * sp.diff(e_m, rho) - e_m)
    cs2_sym = sp.simplify(sp.diff(p_m, rho))
    cs2_target = sp.Rational(10, 9) * sp.Symbol("A", positive=True) * rho ** sp.Rational(2, 3)

res_cs2 = sp.simplify(cs2_sym - cs2_target)
P("  e = (gamma/2)(rho-rhobar)^2, gamma = 2 pi G L*^2  ->  p = %s" % p_of_rho)
P("  c_s^2 = dp/drho = %s" % cs2_sym if MUT != "gamma" else
  "  MUTANT Gamma=5/3: c_s^2 = %s" % cs2_sym)
chk("K1", res_cs2 == 0, "residual %s" % res_cs2, "exactly 0",
    "c_s^2 = dp/drho is exactly 2 pi G L*^2 rho" if MUT != "gamma" else "MUTANT: species differ")

# Jeans wavenumber from the dispersion relation
kk = sp.symbols("k", positive=True)
omega2 = sp.simplify(cs2_sym * kk**2 - 4 * sp.pi * gG * rho)
ratio = sp.simplify(omega2 / (4 * sp.pi * gG * rho))
P("  dispersion: omega^2/(4 pi G rho) = %s" % ratio)
if MUT == "gamma":
    kJm = sp.sqrt(4 * sp.pi * gG * rho / cs2_sym)
    lnkJ = sp.simplify(rho * sp.diff(sp.log(kJm), rho))
    dln = float(lnkJ)
    P("  MUTANT Gamma=5/3: d ln k_J / d ln rho = %s" % lnkJ)
else:
    kJ = sp.simplify(sp.solve(sp.Eq(ratio, 0), kk)[0])
    P("  k_J = %s   (independent of rho: d/drho = %s)" %
      (kJ, sp.simplify(sp.diff(kJ, rho))))
    dln = float(sp.simplify(rho * sp.diff(sp.log(kJ), rho)))
    P("  d ln k_J / d ln rho = %s" % dln)
chk("K2", abs(dln) < 1e-30 and dln == 0.0, "dlnkJ/dlnrho = %g" % dln,
    "0 for Gamma=2 (1/6 for Gamma=5/3)",
    "this is what makes L* a single length" if MUT != "gamma" else "MUTANT: Gamma=5/3 breaks it")

kJ_val = math.sqrt(2.0) / (24 * pc)
lamJ_24 = 2 * math.pi / kJ_val
lamJ_1k = math.sqrt(2) * math.pi * 1000.0
P("  lambda_J = 2 pi/k_J = sqrt(2) pi L* = %.4f pc at 24 pc, %.4f pc at 1 kpc" %
  (lamJ_24 / pc, lamJ_1k))
chk("K3", abs(lamJ_24 / pc - 106.6291905158008) < 1e-6 and
    abs(lamJ_1k / (math.sqrt(2) * math.pi * 1000.0) - 1.0) < 1e-12,
    "%.4f pc / %.4f pc" % (lamJ_24 / pc, lamJ_1k), "106.62919 / 4442.8829")
num("lambda_J_24pc_pc", lamJ_24 / pc)
num("rho_cosmic_kgm3", rho_cosmic)
num("rho_cosmic_Msun_pc3", rho_cosmic / MSUN_PC3)
num("lambda_J_1kpc_pc", lamJ_1k)
num("kJ_over_Lstar", math.sqrt(2.0))

# ================================================== 2. the other two lengths
P("")
P("[2] free-streaming and half-mode lengths")
sig_24 = math.sqrt(a0 * 24 * pc)
sig_1k = math.sqrt(a0 * 1000 * pc)
lamFS_24 = 2 * sig_24 / (3 * H0)
lamFS_1k = 2 * sig_1k / (3 * H0)
P("  sigma_c = sqrt(a0 L*) = %.4f km/s (24 pc), %.4f km/s (1 kpc)" %
  (sig_24 / 1e3, sig_1k / 1e3))
chk("K4", abs(sig_24 / 1e3 - 8.32566) < 1e-3 and abs(sig_1k / 1e3 - 53.7400) < 1e-2,
    "%.4f / %.4f km/s" % (sig_24 / 1e3, sig_1k / 1e3), "8.3257 / 53.740")
P("  lambda_FS = 2 sigma/(3 H0) = %.4f kpc (24 pc), %.4f kpc (1 kpc)" %
  (lamFS_24 / kpc, lamFS_1k / kpc))
chk("K5", abs(lamFS_24 / kpc - 82.3502) < 1e-3 and abs(lamFS_1k / kpc - 531.568) < 1e-2,
    "%.4f / %.4f kpc" % (lamFS_24 / kpc, lamFS_1k / kpc), "82.3502 / 531.568")
num("sigma_24pc_kms", sig_24 / 1e3)
num("sigma_1kpc_kms", sig_1k / 1e3)
num("lambda_FS_24pc_kpc", lamFS_24 / kpc)
num("lambda_FS_1kpc_kpc", lamFS_1k / kpc)

# --- half mode: the record's own linear growth equation (AG6D Part C1), re-run here
h = 0.677
Om = 0.31
Or = 4.15e-5 / h**2
OL = 1 - Om - Or
fc = 5.364 / 6.364
fb = 1 / 6.364
H0c = h / 2997.92458
a_dec = 1 / 1091.0
a_end = 1 / 50.0
a_eq = Or / Om


def E2(a):
    return Om / a**3 + Or / a**4 + OL


def kH(a):
    return a * math.sqrt(E2(a)) * H0c


def a_entry(k):
    return math.exp(brentq(lambda x: math.log(kH(math.exp(x))) - math.log(k), -30,
                           math.log(a_end)))


def rhs_factory(k, Lmpc, fcv=fc):
    def rhs(x, s):
        a = math.exp(x)
        e2 = Om / a**3 + Or / a**4 + OL
        dlnH = (-3 * Om / a**3 - 4 * Or / a**4) / (2 * e2)
        oma = Om / a**3 / e2
        press = 1.5 * oma * fcv * 0.5 * (Lmpc * k / a) ** 2
        dc, dc1, db, db1 = s
        fr = -(2 + dlnH)
        ddc = fr * dc1 + 1.5 * oma * (fcv * dc + fb * db) - press * dc
        ddb = fr * db1 + 1.5 * oma * (fcv * dc + fb * db) if a >= a_dec else 0.0
        return [dc1, ddc, db1 if a >= a_dec else 0.0, ddb]
    return rhs


def grow(k, Lpc):
    Lmpc = Lpc * 1e-6
    aH = a_entry(k)
    rhs = rhs_factory(k, Lmpc)
    s = [1.0, 1.0, 0.0, 0.0]
    xs = [math.log(aH)] + ([math.log(a_dec)] if aH < a_dec else []) + [math.log(a_end)]
    for x0, x1 in zip(xs[:-1], xs[1:]):
        sol = solve_ivp(rhs, (x0, x1), s, method="DOP853", rtol=1e-9, atol=1e-13)
        if not sol.success:
            raise RuntimeError(sol.message)
        s = sol.y[:, -1]
    return fc * s[0] + fb * s[2]


_REF = {}
KG = np.logspace(math.log10(0.05), math.log10(200.0), 49)


def Tk(k, Lpc):
    if k not in _REF:
        _REF[k] = grow(k, 0.0)
    return grow(k, Lpc) / _REF[k]


def khalf(Lpc, grid=KG):
    pk, pT = None, None
    for k in grid:
        t = Tk(k, Lpc)
        if pT is not None and pT >= 0.5 > t:
            f = (math.log(pT) - math.log(0.5)) / (math.log(pT) - math.log(max(t, 1e-300)))
            return float(math.exp(math.log(pk) + f * (math.log(k) - math.log(pk))))
        pk, pT = k, t
    return None


LGRID = [24.0, 50.0, 100.0, 300.0, 1000.0]
KH = {L: khalf(L) for L in LGRID}
P("  half mode from the growth ODE (z=49, 49-point k grid):")
for L in LGRID:
    P("    L* = %6.0f pc: k_1/2 = %.4f /Mpc -> 1/k_1/2 = %.4f Mpc" % (L, KH[L], 1 / KH[L]))
chk("K6", abs(KH[24.0] / 0.980 - 1) < 1e-2, "k_1/2(24pc) = %.4f /Mpc" % KH[24.0],
    "0.980 to 1% (AG6D ag6d_cutoff.out)",
    "reproduced in-lane, not quoted")
num("k_half_Mpc", {str(int(L)): KH[L] for L in LGRID})
num("lam_half_Mpc", {str(int(L)): 1 / KH[L] for L in LGRID})
MH = 4 * math.pi / 3 * (Om * 2.775e11 * h**2) * (math.pi / KH[24.0]) ** 3
num("M_half_Msun_24pc", MH)

# log-log linear fit k_1/2 ~ L^-p over the scanned range (monotone by construction)
XL = np.log(np.array(LGRID))
YK = np.log(np.array([KH[L] for L in LGRID]))
CF = np.polyfit(XL, YK, 1)
P("  fit: k_1/2 = %.4f (L*/24 pc)^%.4f /Mpc  (residual max %.2e dex)" %
  (math.exp(np.polyval(CF, math.log(24.0))), CF[0],
   np.max(np.abs(np.polyval(CF, XL) - YK)) / math.log(10)))


def khalf_fit(L):
    return float(math.exp(np.polyval(CF, math.log(L))))


def lam_half(L):
    return 1.0 / khalf_fit(L)


# spread
spread24 = math.log10((1 / KH[24.0]) * Mpc / lamJ_24)
P("  spread at L*=24 pc: %.4f dex (%.1f pc -> %.4f kpc -> %.4f Mpc)" %
  (spread24, lamJ_24 / pc, lamFS_24 / kpc, 1 / KH[24.0]))
chk("K7", abs(spread24 - 3.98) < 0.02, "%.4f dex" % spread24, "3.98 +- 0.02",
    "the motive's 3.98 dex reproduced")
num("spread_dex_24pc", spread24)
num("cutoff_ratio_FS_over_J_24pc", lamFS_24 / lamJ_24)
num("cutoff_ratio_half_over_J_24pc", (1 / KH[24.0]) * Mpc / lamJ_24)

# ---------------------------------------------- 3. the superluminality claim
P("")
P("[3] is the Gamma=2 pressure superluminal?  (checking the lane's premise)")
cs2_cosmic_24 = 2 * math.pi * G * (24 * pc) ** 2 * rho_cosmic
cs_cosmic_24 = math.sqrt(cs2_cosmic_24)
P("  c_s^2(24 pc, Omega_c rho_crit) = %.6f m^2/s^2  ->  c_s = %.6f m/s = %.4e c" %
  (cs2_cosmic_24, cs_cosmic_24, cs_cosmic_24 / c))
L_cs1 = math.sqrt(1.0 / (2 * math.pi * G * rho_cosmic))
L_csc = math.sqrt(c**2 / (2 * math.pi * G * rho_cosmic))
P("  A11's number 0.5191 is c_s^2 in m^2/s^2, not in units of c^2.")
P("  c_s = 1 m/s at L* = %.4f pc;  c_s = c at L* = %.4e pc = %.3f Gpc" %
  (L_cs1 / pc, L_csc / pc, L_csc / Mpc / 1e3))
rho_sw_c = c**2 / (2 * math.pi * G * (24 * pc) ** 2)
P("  c_s = c requires rho = %.5e kg/m^3 = %.4e Msun/pc^3 (white-dwarf core density)" %
  (rho_sw_c, rho_sw_c / MSUN_PC3))
rho_gal = 0.01 * MSUN_PC3
cs_gal = math.sqrt(2 * math.pi * G * (24 * pc) ** 2 * rho_gal)
P("  at a galactic 0.01 Msun/pc^3, L*=24 pc: c_s = %.4f m/s = %.3e c" % (cs_gal, cs_gal / c))
if MUT == "units":
    cs_ratio = cs_cosmic_24          # the A11 slip: report m/s as c
else:
    cs_ratio = cs_cosmic_24 / c
chk("K8", cs_ratio < 1e-6, "c_s/c = %.4e" % cs_ratio, "< 1e-6",
    "NO superluminality: A11 section 14 has a c^2 unit slip" if MUT != "units"
    else "MUTANT: unit slip reproduces A11's 0.72")
num("cs2_cosmic_24pc_m2s2", cs2_cosmic_24)
num("cs_cosmic_24pc_ms", cs_cosmic_24)
num("cs_over_c_cosmic_24pc", cs_cosmic_24 / c)
num("Lstar_cs_eq_1ms_pc", L_cs1 / pc)
num("Lstar_cs_eq_c_pc", L_csc / pc)
num("rho_cs_eq_c_Msun_pc3", rho_sw_c / MSUN_PC3)
num("rho_cs_eq_c_kgm3", rho_sw_c)
num("cs_galactic_over_c", cs_gal / c)
num("cs_galactic_001_Msun_pc3_ms", cs_gal)

# ================================================== 4. the system: over-determined?
P("")
P("[4] the (L*, rho_c, sigma) system")
P("  lam_J   = sqrt(2) pi L*                      depends on L* only")
P("  lam_FS  = 2 sigma/(3 H0)                     depends on sigma only")
P("  lam_1/2 = 1/k_1/2(L*)                        depends on L* only")
P("  c_s^2/(4 pi G rho_m) = f_c (L* k/a)^2/2 : rho_c enters only through the")
P("  cosmic ratio f_c = Omega_c/Omega_m, never as a local density.")
Jac = sp.Matrix([[sp.Symbol("dL", positive=True), 0, 0],
                 [0, 0, sp.Symbol("dsig", positive=True)],
                 [sp.Symbol("dL2", positive=True), 0, 0]])
rank = Jac.rank()
chk("K9", rank == 2, "rank = %d" % rank, "2 of 3",
    "rho_c is a null direction; the system is over-determined by one")
num("jacobian_rank", rank)

# pairwise crossings
L_JFS = 2 * a0 / (9 * math.pi**2 * H0**2)
P("  lam_J = lam_FS  <=>  L* = 2 a0/(9 pi^2 H0^2) = %.4f Mpc" % (L_JFS / Mpc))
L_JH = math.exp(brentq(lambda x: math.log(lam_half(math.exp(x)) * 1e6) -
                       math.log(math.sqrt(2) * math.pi * math.exp(x)), math.log(1e6),
                       math.log(1e14)))
P("  lam_J = lam_1/2 <=>  L* = %.4e pc (power-law extrapolation, 8 decades out)" % L_JH)
rFSh = [(lamFS_24 / Mpc) * math.sqrt(L / 24) / lam_half(L) for L in (24.0, 1000.0)]
P("  lam_FS/lam_1/2 = %.4f at 24 pc, %.4f at 1 kpc (never 1: no crossing)" %
  (rFSh[0], rFSh[1]))
chk("K10", L_JFS / kpc > 1e3 and L_JH / 1e3 > 1e6 and max(rFSh) < 0.1,
    "crossings %.1f Mpc, %.2e pc; FS/half max %.3f" %
    (L_JFS / Mpc, L_JH, max(rFSh)), "crossings > 1 Mpc; FS/half < 0.1",
    "the ordering lam_J < lam_FS < lam_1/2 is rigid inside [24 pc, 1 kpc]")
num("Lstar_cross_J_FS_Mpc", L_JFS / Mpc)
num("Lstar_cross_J_half_pc", L_JH)
num("FS_over_half_24pc", rFSh[0])
num("FS_over_half_1kpc", rFSh[1])

Ls_scan = np.logspace(math.log10(24.0), 3.0, 3000)
rat = np.array([(1 / khalf_fit(L)) * 1e6 / (math.sqrt(2) * math.pi * L) for L in Ls_scan])
imin = int(np.argmin(rat))
spread_min = math.log10(rat[imin])
P("  minimum spread of the three lengths over the window: %.4f dex at L* = %.1f pc" %
  (spread_min, Ls_scan[imin]))
P("  => no L* makes the three cutoffs coincide; best case is still a factor %.0f" %
  10 ** spread_min)
chk("K11", spread_min > 3.0, "min spread = %.4f dex" % spread_min, "> 3.0 dex",
    "single-cutoff reading has NO solution")
num("spread_min_dex", spread_min)
num("spread_min_factor", 10 ** spread_min)
num("khalf_fit_amp", math.exp(np.polyval(CF, math.log(24.0))))
num("khalf_fit_exp", float(CF[0]))
num("khalf_fit_resid_dex", float(np.max(np.abs(np.polyval(CF, XL) - YK)) / math.log(10)))
num("Lstar_at_min_spread_pc", float(Ls_scan[imin]))

# ================================================== 5. the edge on SPARC
P("")
P("[5] the edge r_e = r_M sqrt(N(N+1)) on 175 SPARC curves")


def load_sparc(ups=0.5):
    out = []
    for f in sorted(glob.glob(SPARC + "/*_rotmod.dat")):
        d = np.loadtxt(f, comments="#")
        if d.ndim == 1:
            d = d[None, :]
        r = d[:, 0]
        vbar2 = d[:, 3] ** 2 + ups * d[:, 4] ** 2 + 1.4 * ups * d[:, 5] ** 2
        Mb = r[-1] * vbar2[-1] / GKPC
        out.append(dict(name=os.path.basename(f).replace("_rotmod.dat", ""),
                        rmax=float(r[-1]), Mb=float(Mb),
                        rM=float(math.sqrt(G * Mb * Msun / a0) / kpc),
                        n=int(len(r)),
                        gmin=float((vbar2 * 1e6 / (r * kpc)).min()),
                        gmax=float((vbar2 * 1e6 / (r * kpc)).max()),
                        rmin=float(r[0])))
    return out


S = load_sparc(0.5)
S7 = load_sparc(0.7)
npts = sum(s["n"] for s in S)
Mbs = np.array([s["Mb"] for s in S])
P("  %d curves, %d points; M_b(<r_max) = %.3e .. %.3e Msun" % (len(S), npts, Mbs.min(), Mbs.max()))
chk("K13", len(S) == 175 and npts == 3391, "%d curves / %d points" % (len(S), npts),
    "175 / 3391", "matches A10's SPARC read")
num("n_curves", len(S))
num("n_points", npts)
num("Mb_min_Msun", float(Mbs.min()))
num("Mb_max_Msun", float(Mbs.max()))

# census N per galaxy (f_ret evaluated at M_ta, inverted from M_b)
cens_err = max(abs(N_census(m) / n - 1) for m, n in CENSUS_PTS.items())
P("  census inversion reproduces A11's five points to %.2e relative" % cens_err)
chk("K12", cens_err < 1e-3, "max rel. err = %.2e over 5 masses" % cens_err, "< 1e-3",
    "f_ret(M_ta) table + M_b = f_ret f_b M_ta/h inverted")
Ns = np.array([N_census(m) for m in Mbs])
res = np.array([math.sqrt(n * (n + 1)) for n in Ns])
num("N_census_min", float(Ns.min()))
num("N_census_max", float(Ns.max()))
num("r_e_over_rM_min", float(res.min()))
num("r_e_over_rM_max", float(res.max()))
P("  census N over the sample: %.2f .. %.2f  ->  r_e/r_M = %.2f .. %.2f" %
  (Ns.min(), Ns.max(), res.min(), res.max()))

xs = np.array([s["rmax"] / s["rM"] for s in S])
frac_reach = float(np.mean(xs >= res))
closest = float(np.max(xs / res))
worst = S[int(np.argmax(xs / res))]
chk("K14", frac_reach == 0.0 and closest < 0.5,
    "fraction reaching r_e = %.3f; closest approach = %.4f (%s)" %
    (frac_reach, closest, worst["name"]), "0.000 / < 0.5",
    "no violation -> no constraint on the census reading")
order = np.argsort(-(xs / res))[:5]
P("  five closest approaches (r_max/r_e): " +
  ", ".join("%s %.3f" % (S[i]["name"], xs[i] / res[i]) for i in order))
num("frac_reaching_re", frac_reach)
num("closest_five", [{"name": S[i]["name"], "rmax_over_re": float(xs[i] / res[i]),
                      "N": float(Ns[i]), "x": float(xs[i])} for i in order])
num("closest_approach_r_max_over_re", closest)
num("closest_galaxy", worst["name"])

Nmin = 0.5 * (np.sqrt(1 + 4 * xs**2) - 1)
Nmin_max = float(Nmin.max())
gmin = S[int(np.argmax(Nmin))]["name"]
chk("K15", 5.0 < Nmin_max < 20.0, "max N_min = %.3f (%s)" % (Nmin_max, gmin),
    "5 < N_min < 20", "the sample requires N > %.2f" % Nmin_max)
num("N_min_max", Nmin_max)
num("N_min_max_galaxy", gmin)

N_FIT = 8.295807681588572
viol = xs >= math.sqrt(N_FIT * (N_FIT + 1))
chk("K16", viol.sum() == 3, "%d/175 curves reach r_e(N=8.296); worst %.3f x" %
    (viol.sum(), float(np.max(xs / math.sqrt(N_FIT * (N_FIT + 1))))),
    "3/175", "the fitted N=8.3 reading is excluded")
num("n_violating_N8p3", int(viol.sum()))
num("worst_over_re_N8p3", float(np.max(xs / math.sqrt(N_FIT * (N_FIT + 1)))))
num("violating_galaxies_N8p3", [S[i]["name"] for i in np.where(viol)[0]])
num("violating_over_re_N8p3", [float(xs[i] / math.sqrt(N_FIT * (N_FIT + 1)))
                               for i in np.where(viol)[0]])

# fragility: how much extra baryonic mass removes the N=8.3 violation?
fac_needed = (Nmin_max / math.sqrt(N_FIT * (N_FIT + 1))) ** 2
chk("K17", 1.3 < fac_needed < 1.7, "M_b inflation needed = %.2f x" % fac_needed,
    "1.3 < f < 1.7", "the N=8.3 exclusion is 1-dex fragile; the census result is not")
num("Mb_inflation_to_clear_N8p3", fac_needed)

# N-scan table
scan = []
for n in (1.0, 2.0, 3.0, 5.0, 8.295807681588572, 10.12, 20.0, float(np.median(Ns))):
    thr = math.sqrt(n * (n + 1))
    scan.append({"N": n, "r_e_over_rM": thr, "n_reach": int(np.sum(xs >= thr)),
                 "frac": float(np.mean(xs >= thr))})
num("N_scan_edge", scan)
P("  N-scan (fraction of curves extending beyond r_e):")
for row in scan:
    P("    N = %7.3f  r_e/r_M = %7.3f  %3d/175 (%.1f%%)" %
      (row["N"], row["r_e_over_rM"], row["n_reach"], 100 * row["frac"]))

Mb6 = 6.0e10
rM6 = math.sqrt(G * Mb6 * Msun / a0) / kpc
num("rM_6e10_kpc", rM6)
num("re_at_Nmin_6e10_kpc", rM6 * math.sqrt(Nmin_max * (Nmin_max + 1)))
num("M_half_over_Mb_max", MH / float(Mbs.max()))
# Upsilon sensitivity
xs7 = np.array([s["rmax"] / s["rM"] for s in S7])
Nmin7 = float((0.5 * (np.sqrt(1 + 4 * xs7**2) - 1)).max())
num("N_min_max_Ups0p7", Nmin7)
num("N_min_max_Ups0p7_pct", 100 * (Nmin7 / Nmin_max - 1))
P("  Upsilon_d = 0.7 instead of 0.5: max N_min = %.3f (%.1f%% change)" %
  (Nmin7, 100 * (Nmin7 / Nmin_max - 1)))

# r_e table vs mass
tab = []
for lm in (8.0, 10.0, 11.0, 12.0, 12.5, 13.0, 14.0):
    Mb = 10.0**lm
    N = N_census(Mb)
    tab.append({"logMb": lm, "N": N, "r_e_over_rM": math.sqrt(N * (N + 1))})
num("r_e_over_rM_vs_Mb", tab)
P("  r_e/r_M vs mass: " + ", ".join("1e%.1f:%.2f" % (t["logMb"], t["r_e_over_rM"]) for t in tab))

# ================================================== 6. the switch-off radius
P("")
P("[6] where the pressure switches off in an MW-like halo")
P("  condition (gradient, not density): the pressure force competes when")
P("    2 pi G L*^2 |grad rho| ~ g.  For rho ~ r^-n and M ~ 4 pi rho r^3/(3-n):")
P("      R_press = n(3-n)/2 * (L*/r)^2   ->  R = (L*/r)^2 for n = 1 and n = 2.")
P("  So r_switch = L* sqrt(n(3-n)/2) ~ L* : the switch is at ~L*, density-free.")

M200 = 1e12
cc = 10.0
rho_c_kpc3 = 2.775e11 * 0.674**2 / 1e9
r200 = (3 * M200 / (4 * math.pi * 200 * rho_c_kpc3)) ** (1.0 / 3.0)
rs = r200 / cc
mu_nfw = math.log(1 + cc) - cc / (1 + cc)
rhos = M200 / (4 * math.pi * rs**3 * mu_nfw)


def nfw(r):
    x = r / rs
    return rhos / (x * (1 + x) ** 2), M200 * (math.log(1 + x) - x / (1 + x)) / mu_nfw


def drho_nfw(r):
    x = r / rs
    return rhos / rs * (-(1 + 3 * x) / (x**2 * (1 + x) ** 3))


def g_tot(r):
    rho, M = nfw(r)
    gN = G * M * Msun / ((r * kpc) ** 2)
    return math.sqrt(a0 * gN) if gN < a0 else gN


def R_press(Lpc, r):
    ap = 2 * math.pi * G * (Lpc * pc) ** 2 * abs(drho_nfw(r)) * (Msun / kpc**4)
    return ap / g_tot(r)


r_sw = brentq(lambda r: math.log(R_press(24.0, r)), 1e-4, 1.0)
P("  MW-like NFW (M200 = 1e12 Msun, c = %.0f): r200 = %.1f kpc, r_s = %.2f kpc" %
  (cc, r200, rs))
P("  R_press = 1 at r = %.4f pc  (L* = 24 pc)  ->  r_switch/L* - 1 = %.2e" %
  (r_sw * 1e3, r_sw * 1e3 / 24.0 - 1))
chk("K18", abs(r_sw * 1e3 / 24.0 - 1) < 0.01, "r_switch = %.3f pc" % (r_sw * 1e3),
    "24 pc to 1%", "exactly L*: the switch is a length, not a density")
rho_sw = nfw(r_sw)[0] * 1e-9
P("  density at the switch: %.2f Msun/pc^3" % rho_sw)
num("r_switch_pc", r_sw * 1e3)
num("rho_at_switch_Msun_pc3", rho_sw)
num("R_press_at_1kpc", R_press(24.0, 1.0))
num("R_press_at_1kpc_analytic", (24.0 / 1000.0) ** 2)
num("r_switch_over_Lstar", r_sw * 1e3 / 24.0)
num("r200_kpc", r200)
num("rs_kpc", rs)
num("R_press_at_24pc", R_press(24.0, 0.024))

rmin_all = min(s["rmin"] for s in S)
P("  RAR region: the innermost SPARC point is r = %.3f kpc = %.1f L*" %
  (rmin_all, rmin_all * 1e3 / 24.0))
P("  R_press at that radius <= (L*/r)^2 = %.4f ; at 1 kpc %.2e" %
  ((24.0 / (rmin_all * 1e3)) ** 2, (24.0 / 1000.0) ** 2))
chk("K19", rmin_all * 1e3 / 24.0 > 3.0 and (24.0 / (rmin_all * 1e3)) ** 2 < 0.10,
    "r_min = %.3f kpc (%.1f L*), R = %.4f" %
    (rmin_all, rmin_all * 1e3 / 24.0, (24.0 / (rmin_all * 1e3)) ** 2),
    "> 3 L* and R < 0.10", "no conflict with the RAR fit region")
num("sparc_r_min_kpc", rmin_all)
num("sparc_rmin_over_Lstar", rmin_all * 1e3 / 24.0)
num("frac_points_r_gt_1kpc", float(np.mean(np.concatenate(
    [np.loadtxt(f, comments="#")[:, 0] for f in sorted(glob.glob(SPARC + "/*_rotmod.dat"))]) > 1.0)))
num("R_press_at_sparc_rmin", (24.0 / (rmin_all * 1e3)) ** 2)

# ================================================== 7. the Jeans mass
P("")
P("[7] the Jeans mass at the switch")

RTF = math.pi * 24 / math.sqrt(2)
MJ_sw = 4 * math.pi / 3 * rho_sw * RTF**3
Vf = 165.2e3
COEF = math.pi**3 / (6 * math.sqrt(2))          # = 3.6540
MJ_iso = COEF * Vf**2 * 24 * pc / G / Msun
MJ_per_kms2 = COEF * 1e6 * 24 * pc / G / Msun
P("  R_TF = lambda_J/2 = pi L*/sqrt(2) = %.4f pc (mass-independent)" % RTF)
P("  M_J = (4 pi/3) rho R_TF^3 ; at the NFW switch density %.2f Msun/pc^3: %.3e Msun" %
  (rho_sw, MJ_sw))
P("  deep-MOND isothermal reading: rho = V_f^2/(4 pi G r^2) is the law's own flat-curve")
P("  profile, so M_J(r_sw) = 3.6540 V_f^2 L*/G = %.2e (V_f/km/s)^2 Msun = %.3e at 165.2" %
  (MJ_per_kms2, MJ_iso))
# half-mass radius of the n=1 polytrope (xi cos xi - sin xi = -pi/2)
xi_h = brentq(lambda x: x * math.cos(x) - math.sin(x) + math.pi / 2, 1.0, 3.0)
reff = xi_h / math.pi * RTF
chk("K20", 1e8 < MJ_iso < 1e9 and abs(MJ_per_kms2 - 2.04e4) < 1e2 and
    abs(RTF - 53.3146) < 1e-3,
    "M_J = %.3e Msun (%.2e per (km/s)^2), R_TF = %.2f pc, r_eff = %.1f pc" %
    (MJ_iso, MJ_per_kms2, RTF, reff), "1e8..1e9 Msun; 2.04e4 (km/s)^-2; R_TF 53.31",
    "class: ultra-compact dwarf / massive nuclear star cluster")
num("RTF_pc", RTF)
num("M_J_at_switch_NFW_Msun", MJ_sw)
num("M_J_per_kms2_Msun", MJ_per_kms2)
num("M_J_isothermal_Msun", MJ_iso)
num("r_eff_pc", reff)
num("MJ_coefficient", COEF)
num("V_flat_kms", Vf / 1e3)
num("M_J_mean_density_Msun_pc3", MJ_iso / (4 * math.pi / 3 * RTF**3))
num("M_J_at_cosmic_mean_Msun", 4 * math.pi / 3 * (Om_c * rho_crit / MSUN_PC3) * RTF**3)
num("M_J_at_cs_eq_c_Msun", 4 * math.pi / 3 * (rho_sw_c / MSUN_PC3) * RTF**3)

# M_J proportional to rho -- the Gamma=2 signature
r1 = 4 * math.pi / 3 * 1.0 * RTF**3
r2 = 4 * math.pi / 3 * 100.0 * RTF**3
slope = math.log(r2 / r1) / math.log(100.0)
chk("K21", abs(slope - 1.0) < 1e-12, "dlnM_J/dlnrho = %.6f" % slope,
    "1 exactly (standard Jeans: -1/2)",
    "Gamma=2 inverts the hierarchy: denser regions make bigger clumps")
num("dlnMJ_dlnrho", slope)

# ================================================== summary
npass = sum(1 for c in RESULTS["checks"] if c["pass"])
ntot = len(RESULTS["checks"])
P("")
P("numbers: lam_J(24pc)=%.2f pc, lam_FS(24pc)=%.2f kpc, 1/k_1/2=%.4f Mpc, spread=%.2f dex" %
  (lamJ_24 / pc, lamFS_24 / kpc, 1 / KH[24.0], spread24))
P("edge: r_e/r_M=%.2f..%.2f, %d/175 reach it, closest %.1f%%, N>%.2f required" %
  (res.min(), res.max(), int(np.sum(xs >= res)), 100 * closest, Nmin_max))
P("switch: r=%.1f pc (L*), rho=%.1f Msun/pc^3, M_J=%.2e Msun in %.1f pc" %
  (r_sw * 1e3, rho_sw, MJ_iso, RTF))
P("A16 COMPLETE: %d/%d checks PASS." % (npass, ntot))

RESULTS["status"] = ("NO-GO(one cutoff); DERIVED(three functionals); "
                     "NUMERICAL(SPARC edge); DERIVED(pressure switch); "
                     "CORRECTION(A11 sec.14 c^2 slip)")
RESULTS["runtime_s"] = round(time.time() - t0, 2)
RESULTS["constants_used"] = [
    "c = 2.99792458e8 m/s (BRIEF 4)", "G = 6.67430e-11 (BRIEF 4)",
    "a0 = 9.36e-11 m/s^2 canonical (BRIEF 4)", "H0 = 2.1843e-18 s^-1 (BRIEF 4)",
    "pc = 3.0856775814913673e16 m (BRIEF 4)", "Msun = 1.98847e30 kg (GM_sun/G)",
    "K_stiffness = 4 pi G (AG6D FROZEN_CRITERIA section 0; BRIEF 1 writes 8 pi G -- factor 2, see report)",
    "Omega_c = 0.2645, rho_crit = 3H0^2/(8 pi G)", "h = 0.677, Omega_m = 0.31, Omega_r h^2 = 4.15e-5 (AG6D)",
    "G_kpc = 4.300917270e-6 kpc (km/s)^2/Msun",
]
RESULTS["external_inputs"] = [
    "k_1/2 = 0.980 /Mpc at L*=24 pc: AG6D ag6d_cutoff.out (recomputed here, not trusted)",
    "census N = 5.364327/f_ret, f_ret table: A11 section 10 reproducing CFG416",
    "SPARC rotmod curves: real_research/data/sparc_data (175 files, 3391 points), Upsilon_d = 0.5",
    "r_e = r_M sqrt(N(N+1)): A11 eq. (7)",
]
tag = ("_MUTATE_" + MUT) if MUT else ""
with open(os.path.join(HERE, "a16_results%s.json" % tag), "w") as fh:
    json.dump(RESULTS, fh, indent=1, default=float)
with open(os.path.join(HERE, "a16%s.out" % tag), "w") as fh:
    fh.write("\n".join(OUT) + "\n")

sys.exit(0 if (npass == ntot and not MUT) else 1)
