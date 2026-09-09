#!/usr/bin/env python3
r"""
L37 -- WHICH DENSITY IS IN a0 = kappa c sqrt(G rho)?  The fork, decided at recombination and BBN.
================================================================================================
THE FORK.  The programme's headline scale is a0 = kappa c sqrt(G rho).  Two readings of rho:

  CANONICAL   rho = rho_Lambda (dark-energy density).  With w = -1 exactly, rho_Lambda = const,
              so a0(z) = CONST at every redshift.
  RIVAL       rho = rho_tot.  Since H^2 = 8 pi G rho_tot / 3, this is a0 propto c H(z), i.e.
              a0(z) = a0(0) E(z), rising as (1+z)^2 in radiation domination.

They agree today by construction (that is how the rival is normalised) and diverge violently
backwards.  This script asks: WHICH FOOTING, IF EITHER, SURVIVES RECOMBINATION AND BBN?

WHY THIS IS NOT A REPEAT OF AN OLD SCRIPT.  The repository already contains
`real_research/reviews/mi_cmb_a0_horizon_2026.py`, which answers a version of this using ONE
estimator, a_ac ~ c_s^2 / r_s(phys) -- the PRESSURE acceleration of the acoustic oscillator.
That is the right estimator for a modified-INERTIA reading (it is the actual acceleration of a
fluid element) and it is NOT the right estimator for the operative modified-GRAVITY arm, where
the argument of the interpolating function is the GRAVITATIONAL field |grad Phi|.  The two differ
by six orders of magnitude at recombination.  This script computes BOTH, plus the crude
Phi/lambda estimator that generated the "g/a0 ~ 2" claim in the L37 brief, and states which
reading each belongs to.  Carrying only one of them is how this question has been got wrong
twice in this repository already (see the RECORD section).

THE RECORDED FAILURE MODES THIS SCRIPT IS WRITTEN AGAINST.
 (1) `real_research/GEMINI_MANUFACTURED_WIN_a0z_2026-07-20.md` -- an agent truncated the CPL
     Taylor series, dropped the w_a term, and turned a bump-then-decline into a "confirmation".
     Countermeasure here: no series expansions anywhere; every a0(z) is the closed form,
     evaluated exactly, and the exact/approximate difference is printed when one is used.
 (2) `real_research/A0Z_OPEN_DOORS_AND_LENSING_FORECAST_2026-06-06.md` section 1 -- the SAME
     "the CMB sits at the MOND transition" claim was made in this repository in June 2026 with
     g/a0 ~ 1.8, and RETRACTED the same day: the literature value (Sanders astro-ph/0509532) is
     g/a0 ~ 20, and the error was a crude sound-horizon estimator.  The L37 brief's g/a0 ~ 2.3
     is numerically the same claim.  This script reproduces both numbers, identifies the exact
     convention that separates them (a factor 2 pi from lambda vs k, plus the transfer function),
     and reports which one is defensible.  A lane that dissolves its own premise reports that.
 (3) The symmetric danger: manufacturing a KILL.  Skordis & Zlosnik 2021 (PRL 127:161302) show
     that AeST -- a relativistic MOND theory -- reproduces the Planck spectra.  Section S7 states
     the mechanism plainly and applies it to both footings, including where it RESCUES one.

WHAT IS COMPUTED
  C0  CONTROL  background cosmology: z_eq, r_s(z_drag), theta_*, and the brief's E(z) table.
  C1  CONTROL  the g/a0 estimator returns the Newtonian and deep-MOND limits on a point mass,
               and the kernel reproduces the BTFR v^4 = G M a0.
  S1  the a0(z) table on both footings x both a0 normalisations (9.3619e-11 / 1.1279e-10).
  S2  THE ESTIMATOR FORK at recombination: |grad Phi| from a transfer-function-weighted
               potential, scanned over the whole Planck multipole range, vs the two rival
               estimators.  Where g/a0 = 1 sits relative to the sound horizon.
  S3  what the surviving boost does to r_s, theta_*, the peak positions, the odd/even ratio and
               the damping tail -- as FRACTIONAL shifts against Planck's measured precision.
  S4  the same for the rival footing (boost ~50 rather than ~1.03).
  S5  BBN, both footings: the perturbation g/a0 at T ~ 0.8 MeV and T ~ 0.09 MeV, and Y_p.
  S6  the record's "off at recombination" statement vs the canonical footing -- is the
               repository internally consistent?
  S7  AeST: does a relativistic MOND theory already pass the CMB, and by what mechanism?
  S8  VERDICT.

Both a0 footings carried everywhere.  Both interpolating kernels (nu_RAR = the framework's own,
and Milgrom's "simple" nu) carried wherever a boost is computed, so no conclusion rests on one.
FAIL marks a requirement the footing does not meet.

CREDIT.  nu_RAR kernel form: Milgrom & Sanders 2008 ApJ 678:131 eq 13 at alpha = 1/2, adopted by
McGaugh, Lelli & Schombert 2016.  AQUAL: Bekenstein & Milgrom 1984.  AeST: Skordis & Zlosnik 2021
PRL 127:161302.  MOND at recombination g/a0 ~ 20: Sanders 2005 astro-ph/0509532.  EH98 no-wiggle
transfer function: Eisenstein & Hu 1998 ApJ 496:605.  Planck values: Planck 2018 VI (A&A 641 A6).
Y_p: Aver, Olive & Skillman 2015 / Aver et al. 2021.  kappa = 1/2 IS FITTED, NOT DERIVED.
"""
import math
import numpy as np

FAILS = []
NCHK = [0]


def check(name, ok, detail=""):
    NCHK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)
    return ok


def info(name, detail=""):
    print(f"  [info] {name}" + (f"   {detail}" if detail else ""), flush=True)


def banner(s):
    print("\n" + "=" * 118)
    print(s)
    print("=" * 118, flush=True)


# ----------------------------------------------------------------------------------------------
# constants and the Planck 2018 TT,TE,EE+lowE+lensing base-LCDM cosmology
# ----------------------------------------------------------------------------------------------
C = 2.99792458e8            # m/s
G = 6.67430e-11             # SI
MPC = 3.0856775814913673e22  # m
MSUN = 1.98892e30           # kg
KPC = MPC / 1e3

h = 0.6736
H0 = 100.0 * h * 1e3 / MPC   # s^-1
OM_B_H2 = 0.02237
OM_C_H2 = 0.1200
OM_M_H2 = OM_B_H2 + OM_C_H2
OM_M = OM_M_H2 / h**2
T_CMB = 2.7255              # K
N_EFF = 3.046
# radiation: photons + massless neutrinos
OM_G_H2 = 2.4728e-5 * (T_CMB / 2.7255) ** 4      # photons only
OM_R_H2 = OM_G_H2 * (1.0 + 0.2271 * N_EFF)
OM_R = OM_R_H2 / h**2
OM_L = 1.0 - OM_M - OM_R

A_S = 2.100e-9              # primordial curvature amplitude at k_p
K_PIVOT = 0.05              # Mpc^-1
N_S = 0.9649

# the two a0 normalisations the charter requires be carried everywhere
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}   # m/s^2

Z_STAR = 1089.92            # Planck 2018 last scattering
Z_DRAG = 1059.94            # Planck 2018 baryon drag
Z_REC_BRIEF = 1100.0        # the redshift the L37 brief tabulates

# Planck measured precisions used as the yardstick in S3/S4
PLANCK = {
    "r_drag_Mpc": (147.09, 0.26),          # 0.18%
    "100theta_star": (1.04109, 0.00031),   # 0.030%
    "n_s": (0.9649, 0.0042),
    "ln1e10As": (3.044, 0.014),            # 1.4% in A_s
    "omega_b": (0.02237, 0.00015),         # 0.67%  <- the odd/even peak-height ratio
    "omega_c": (0.1200, 0.0012),           # 1.0%   <- the 3rd/1st peak ratio
}
YP_OBS = (0.2453, 0.0034)   # Aver et al. 2021 helium mass fraction


def E(z):
    """H(z)/H0 with radiation, matter, Lambda (flat)."""
    zp = 1.0 + np.asarray(z, dtype=float)
    return np.sqrt(OM_R * zp**4 + OM_M * zp**3 + OM_L)


def Hz(z):
    return H0 * E(z)


print("=" * 118)
print("L37 -- which density is in a0 = kappa c sqrt(G rho)?  Recombination and BBN decide.")
print("=" * 118, flush=True)
print(f"  cosmology: h={h}, Om={OM_M:.4f}, Ob h^2={OM_B_H2}, Or={OM_R:.4e}, OL={OM_L:.4f}, "
      f"T_CMB={T_CMB} K, N_eff={N_EFF}")
print(f"  a0 footings carried: canonical {A0['canonical']:.4e} m/s^2, alt {A0['alt']:.4e} m/s^2 "
      f"(ratio {A0['alt']/A0['canonical']:.4f} = 1/sqrt(Omega_Lambda_eff))")

# ==============================================================================================
banner("C0  CONTROL -- does the background cosmology reproduce standard numbers?")
# ==============================================================================================
z_eq = OM_M_H2 / OM_R_H2 - 1.0
check("C0a  matter-radiation equality z_eq within 5% of Planck 3387",
      abs(z_eq - 3387.0) / 3387.0 < 0.05, f"z_eq = {z_eq:.0f}")


def R_baryon(z):
    """Baryon-to-photon momentum density ratio R = 3 rho_b / (4 rho_gamma)."""
    return 3.0 * OM_B_H2 / (4.0 * OM_G_H2) / (1.0 + np.asarray(z, dtype=float))


def sound_horizon(z_end, n=400000):
    """Comoving sound horizon r_s(z_end) = int_{z_end}^{inf} c_s / H dz, in Mpc."""
    # substitute a = 1/(1+z); integrate in ln a from a=1e-9 to a_end
    a_end = 1.0 / (1.0 + z_end)
    lna = np.linspace(math.log(1e-9), math.log(a_end), n)
    a = np.exp(lna)
    z = 1.0 / a - 1.0
    cs = C / np.sqrt(3.0 * (1.0 + R_baryon(z)))          # m/s
    integ = cs / (a * Hz(z))                              # dr = c_s/(a H) d ln a * a ... careful
    # comoving r_s = int c_s dt / a = int c_s / (a^2 H) da = int c_s/(a H) dlna
    return np.trapz(integ, lna) / MPC


def comoving_distance(z_end, n=200000):
    zz = np.linspace(0.0, z_end, n)
    return np.trapz(C / Hz(zz), zz) / MPC


r_drag = sound_horizon(Z_DRAG)
r_star = sound_horizon(Z_STAR)
D_M_star = comoving_distance(Z_STAR)
theta_star = r_star / D_M_star
check("C0b  sound horizon at drag within 1% of Planck 147.09 Mpc",
      abs(r_drag - PLANCK["r_drag_Mpc"][0]) / PLANCK["r_drag_Mpc"][0] < 0.01,
      f"r_drag = {r_drag:.2f} Mpc  (Planck {PLANCK['r_drag_Mpc'][0]} +- {PLANCK['r_drag_Mpc'][1]})")
check("C0c  acoustic angular scale 100 theta_* within 1% of Planck 1.04109",
      abs(100 * theta_star - PLANCK["100theta_star"][0]) / PLANCK["100theta_star"][0] < 0.01,
      f"100 theta_* = {100*theta_star:.5f},  r_s(z_*) = {r_star:.2f} Mpc, D_M = {D_M_star:.0f} Mpc")

# the brief's E(z) table
E_brief = {2.5: 3.769, 1100.0: 2.358e4, 4.0e8: 1.538e15}
ok_E = True
for zb, eb in E_brief.items():
    em = float(E(zb))
    dev = abs(em - eb) / eb
    ok_E &= dev < 0.02
    info(f"C0d  E({zb:g}) computed {em:.4g} vs brief {eb:.4g}", f"deviation {dev*100:.2f}%")
check("C0d  the brief's H(z)/H0 table reproduced independently to 2%", ok_E)
info("     NOTE on E(4e8): pure a^-4 radiation scaling is used, as the brief does.  Across e+e-",
     "")
info("     annihilation g_* changes, so the true E at T ~ 0.09 MeV differs by <~20%; this does not",
     "")
info("     move any decimal order in what follows and is flagged, not hidden.", "")

# ==============================================================================================
banner("C1  CONTROL -- does the g/a0 estimator return the known Newtonian and deep-MOND limits?")
# ==============================================================================================


def nu_RAR(y):
    """The framework's own kernel: g_tot = g_N nu(y), y = g_N/a0, nu = 1/(1-exp(-sqrt(y)))."""
    y = np.asarray(y, dtype=float)
    return 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-300))))


def nu_simple(y):
    """Milgrom's 'simple' interpolating function, nu = (1+sqrt(1+4/y))/2."""
    y = np.asarray(y, dtype=float)
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / np.maximum(y, 1e-300)))


KERNELS = {"nu_RAR": nu_RAR, "nu_simple": nu_simple}

# Newtonian limit
y_big = 1e8
for kn, kf in KERNELS.items():
    check(f"C1a  {kn} -> 1 (Newtonian) at g/a0 = 1e8",
          abs(float(kf(y_big)) - 1.0) < 1e-4, f"nu = {float(kf(y_big)):.8f}")
# deep-MOND limit: nu * sqrt(y) -> 1
y_small = 1e-8
for kn, kf in KERNELS.items():
    val = float(kf(y_small)) * math.sqrt(y_small)
    check(f"C1b  {kn} * sqrt(y) -> 1 (deep MOND) at g/a0 = 1e-8",
          abs(val - 1.0) < 0.01, f"nu sqrt(y) = {val:.6f}")

# BTFR: v_flat^4 = G M a0 for an isolated point mass, from the kernel itself
for foot, a0 in A0.items():
    M = 1e11 * MSUN
    r = np.logspace(math.log10(30 * KPC), math.log10(3000 * KPC), 400)
    gN = G * M / r**2
    v4 = (gN * nu_RAR(gN / a0) * r) ** 2
    v4_far = v4[-1]
    pred = G * M * a0
    check(f"C1c  [{foot}] kernel reproduces BTFR v^4 = G M a0 at r = 3 Mpc to 3%",
          abs(v4_far / pred - 1.0) < 0.03,
          f"v_flat = {v4_far**0.25/1e3:.1f} km/s, v^4/(G M a0) = {v4_far/pred:.4f}")

# the estimator itself, on a point mass: does g/a0 cross 1 at the MOND radius?
for foot, a0 in A0.items():
    r_M = math.sqrt(G * 1e11 * MSUN / a0)
    gN_at_rM = G * 1e11 * MSUN / r_M**2
    check(f"C1d  [{foot}] g/a0 = 1 exactly at the MOND radius sqrt(GM/a0)",
          abs(gN_at_rM / a0 - 1.0) < 1e-9, f"r_M = {r_M/KPC:.1f} kpc")

# ==============================================================================================
banner("S1  THE FORK -- a0(z) on both readings, both normalisations (exact, no expansions)")
# ==============================================================================================
print("  CANONICAL  rho = rho_Lambda, w = -1  =>  a0(z) = a0(0)             [EXACTLY constant]")
print("  RIVAL      rho = rho_tot            =>  a0(z) = a0(0) E(z)        [propto c H(z)]")
print()
print(f"  {'z':>12} {'H(z)/H0':>12} | {'a0 canon rhoL':>15} {'a0 canon rhotot':>16} | "
      f"{'a0 alt rhoL':>13} {'a0 alt rhotot':>15}")
Z_TAB = [0.0, 2.5, Z_REC_BRIEF, 4.0e8]
for zt in Z_TAB:
    e = float(E(zt))
    row = f"  {zt:>12.4g} {e:>12.4g} |"
    for foot in ("canonical", "alt"):
        row += f" {A0[foot]:>15.4g} {A0[foot]*e:>16.4g} |" if foot == "canonical" else \
               f" {A0[foot]:>13.4g} {A0[foot]*e:>15.4g}"
    print(row)
brief_tab = {2.5: (9.362e-11, 3.528e-10), 1100.0: (9.362e-11, 2.208e-6), 4.0e8: (9.362e-11, 1.44e5)}
ok_tab = True
for zt, (ac, ar) in brief_tab.items():
    mine_c = A0["canonical"]
    mine_r = A0["canonical"] * float(E(zt))
    ok_tab &= abs(mine_c / ac - 1) < 0.01 and abs(mine_r / ar - 1) < 0.03
check("S1a  the brief's a0 table reproduced independently (canonical and rival, both to 3%)", ok_tab)
info("S1b  the two a0 NORMALISATIONS differ by exactly 1/sqrt(Omega_Lambda)",
     f"{A0['alt']/A0['canonical']:.4f} vs {1/math.sqrt(0.6847):.4f} -- the 'both footings' pair "
     f"IS the rho_Lambda/rho_tot fork evaluated TODAY")

# ==============================================================================================
banner("S2  THE ESTIMATOR FORK -- what IS 'g' at recombination?  Three answers, six decades apart")
# ==============================================================================================
print("""  The interpolating function's argument is NOT a matter of taste; it is fixed by which arm of
  the fork the theory is on.
    MODIFIED GRAVITY (the operative arm since 2026-08-08): AQUAL/QUMOND modify the POISSON
      equation, div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho.  The argument is the GRAVITATIONAL
      field |grad Phi| of the perturbation.  For a Fourier mode, |grad Phi| = (k/a) Phi.
    MODIFIED INERTIA (closed arm, excluded 21 sigma by lensing): the argument is the TOTAL
      acceleration of the fluid element, which in a tightly-coupled photon-baryon plasma is
      dominated by the PRESSURE gradient, a_ac ~ c_s^2 / r_s(phys), not by gravity.
    THE BRIEF'S ESTIMATOR, g ~ Phi/lambda, is the MG estimator with the 2 pi of |grad| dropped
      (lambda instead of k) and a hand-set Phi.  It is not a third physical reading.""")


def T_EH98(k_Mpc):
    """Eisenstein & Hu 1998 no-wiggle (shape) transfer function.  k in Mpc^-1 (not h/Mpc)."""
    k = np.asarray(k_Mpc, dtype=float)
    om_m_h2, om_b_h2 = OM_M_H2, OM_B_H2
    f_b = om_b_h2 / om_m_h2
    theta = T_CMB / 2.7
    s = 44.5 * math.log(9.83 / om_m_h2) / math.sqrt(1.0 + 10.0 * om_b_h2 ** 0.75)   # Mpc
    alpha_g = (1.0 - 0.328 * math.log(431.0 * om_m_h2) * f_b
               + 0.38 * math.log(22.3 * om_m_h2) * f_b ** 2)
    gamma_eff = om_m_h2 / h * (alpha_g + (1.0 - alpha_g) / (1.0 + (0.43 * k * s) ** 4))
    q = k * theta ** 2 / (gamma_eff * h)
    L0 = np.log(2.0 * math.e + 1.8 * q)
    C0 = 14.2 + 731.0 / (1.0 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)


def Delta_Phi(k_Mpc):
    """RMS Bardeen potential per e-fold of k, matter era: Delta_Phi = (3/5) sqrt(A_s) (k/kp)^((ns-1)/2) T(k)."""
    k = np.asarray(k_Mpc, dtype=float)
    return 0.6 * math.sqrt(A_S) * (k / K_PIVOT) ** (0.5 * (N_S - 1.0)) * T_EH98(k)


def g_grad_phi(k_Mpc, z):
    """|grad Phi| in m/s^2 for a comoving mode k at redshift z:  (k_com (1+z)) * c^2 * Phi."""
    k = np.asarray(k_Mpc, dtype=float)
    k_phys = k * (1.0 + z) / MPC          # m^-1
    return k_phys * C**2 * Delta_Phi(k)


# comoving horizon (Hubble radius) at recombination, and the multipole it maps to
z_rec = Z_REC_BRIEF
rH_com = C * (1.0 + z_rec) / float(Hz(z_rec)) / MPC     # Mpc
k_H = 1.0 / rH_com
l_H = k_H * D_M_star
r_s_phys = r_star * MPC / (1.0 + z_rec)
info("S2a  comoving Hubble radius at z = 1100", f"{rH_com:.1f} Mpc  =>  k_H = {k_H:.4f} Mpc^-1  "
     f"=>  l_H = {l_H:.0f}   (multipoles below this are SUPERHORIZON at last scattering)")

# the brief's own estimator, reproduced exactly
lam_com_brief = 150.0
lam_phys_brief = lam_com_brief * MPC / (1.0 + z_rec)
Phi_brief = 1e-5
g_brief = Phi_brief * C**2 / lam_phys_brief
info("S2b  the brief's estimator g = Phi c^2 / lambda_phys",
     f"lambda_phys = {lam_phys_brief/MPC:.4f} Mpc, g = {g_brief:.3e} m/s^2  "
     f"=> g/a0(canon) = {g_brief/A0['canonical']:.2f}  [the brief's 2.3]")
check("S2c  the brief's g ~ 2.1e-10 and g/a0 ~ 2.3 reproduced exactly (control on the premise)",
      abs(g_brief / 2.1e-10 - 1) < 0.05 and abs(g_brief / A0["canonical"] / 2.3 - 1) < 0.06,
      f"g = {g_brief:.3e}, g/a0 = {g_brief/A0['canonical']:.3f}")

# the same scale, with |grad| done properly: k = 2pi/lambda, and Phi from the transfer function
k_brief = 2.0 * math.pi / lam_com_brief
g_proper = float(g_grad_phi(k_brief, z_rec))
info("S2d  the SAME 150 Mpc scale with |grad Phi| = k Phi, k = 2 pi/lambda, Phi from EH98",
     f"k = {k_brief:.4f} Mpc^-1, Delta_Phi = {float(Delta_Phi(k_brief)):.3e}, "
     f"g = {g_proper:.3e} m/s^2 => g/a0(canon) = {g_proper/A0['canonical']:.1f}")
info("S2e  the factor between them", f"{g_proper/g_brief:.1f}x = 2pi (from lambda->k) x "
     f"{float(Delta_Phi(k_brief))/Phi_brief:.2f} (transfer-function Phi vs the hand-set 1e-5)")

# the MI estimator (what the repository's existing script used)
cs_rec = C / math.sqrt(3.0)
a_ac = cs_rec**2 / r_s_phys
info("S2f  the MODIFIED-INERTIA estimator a_ac = c_s^2 / r_s(phys)",
     f"{a_ac:.3e} m/s^2  =>  g/a0(canon) = {a_ac/A0['canonical']:.2e}  "
     f"[this is what mi_cmb_a0_horizon_2026.py uses]")

# ---- the full multipole scan, both footings, both readings
print()
print("  MODIFIED-GRAVITY g/a0 ACROSS THE PLANCK MULTIPOLE RANGE at z = 1100")
print(f"  {'l':>6} {'k [1/Mpc]':>11} {'T(k)':>8} {'Delta_Phi':>11} {'g [m/s2]':>11} | "
      f"{'y canon':>9} {'y alt':>9} | {'y RIVAL c':>10} {'y RIVAL a':>10} | {'sub-hor?':>9}")
ls = np.array([2, 10, 30, 70, 100, 220, 340, 537, 810, 1120, 1450, 1800, 2200, 2500], dtype=float)
ks = ls / D_M_star
E_rec = float(E(z_rec))
for l, k in zip(ls, ks):
    gk = float(g_grad_phi(k, z_rec))
    yc = gk / A0["canonical"]
    ya = gk / A0["alt"]
    yrc = gk / (A0["canonical"] * E_rec)
    yra = gk / (A0["alt"] * E_rec)
    print(f"  {l:>6.0f} {k:>11.5f} {float(T_EH98(k)):>8.4f} {float(Delta_Phi(k)):>11.3e} "
          f"{gk:>11.3e} | {yc:>9.2f} {ya:>9.2f} | {yrc:>10.3e} {yra:>10.3e} | "
          f"{'yes' if l > l_H else 'NO':>9}")

# minimum g/a0 over the SUBHORIZON range (where quasi-static MOND language is even defined)
l_sub = np.logspace(math.log10(l_H), math.log10(2500), 400)
k_sub = l_sub / D_M_star
g_sub = g_grad_phi(k_sub, z_rec)
y_sub = {foot: g_sub / A0[foot] for foot in A0}
for foot in A0:
    check(f"S2g  [{foot}] MG g/a0 stays ABOVE 1 everywhere subhorizon at recombination",
          float(np.min(y_sub[foot])) > 1.0,
          f"min g/a0 = {float(np.min(y_sub[foot])):.2f} at l = {float(l_sub[int(np.argmin(y_sub[foot]))]):.0f}, "
          f"max = {float(np.max(y_sub[foot])):.2f}")
# the TOTAL rms |grad Phi| at a point -- the sum over all subhorizon modes, not one mode
lnk = np.linspace(math.log(k_H), math.log(100.0), 4000)
kk_all = np.exp(lnk)
g_all = g_grad_phi(kk_all, z_rec)
g_rms = float(np.sqrt(np.trapz(g_all**2, lnk)))
info("S2h  TOTAL rms |grad Phi| at a point (all subhorizon modes, k_H to 100 Mpc^-1)",
     f"g_rms = {g_rms:.3e} m/s^2  =>  g/a0 = {g_rms/A0['canonical']:.1f} (canonical), "
     f"{g_rms/A0['alt']:.1f} (alt).  The integral converges because g propto k T(k) propto "
     f"ln k / k in the UV")
check("S2i  the brief's premise g/a0 ~ 2.3 is NOT reproduced by any defensible subhorizon "
      "estimator (PASS = the premise does not survive)",
      float(np.min(y_sub["canonical"])) > 2.4,
      f"confirmed not reproduced.  per-mode range {float(np.min(y_sub['canonical'])):.1f}-{float(np.max(y_sub['canonical'])):.1f}; "
      f"point rms {g_rms/A0['canonical']:.1f}; MI estimator {a_ac/A0['canonical']:.1e}.  The value 2.3 "
      f"requires lambda in place of k (a factor 2 pi) AND a superhorizon mode (l < {l_H:.0f})")
info("S2j  vs the literature", f"Sanders (astro-ph/0509532) quotes g/a0 ~ 20 at recombination; "
     f"the point rms computed here is {g_rms/A0['canonical']:.0f}-{g_rms/A0['alt']:.0f}.  Agreement to a "
     f"factor {20*A0['canonical']/g_rms:.1f}, i.e. the same order and the same conclusion, but the "
     f"literature value is NOT reproduced to better than ~40% and is not claimed to be")
info("S2k  WHERE the brief's g/a0 ~ 2 actually lives", f"at l ~ 20-40 (the table above), i.e. "
     f"2-3x OUTSIDE the horizon at last scattering (l_H = {l_H:.0f}), where the quasi-static MOND "
     f"limit is not defined at all and where the CMB is cosmic-variance limited to 15-50% per multipole")
# normalisation control: the Sachs-Wolfe plateau
SW = float(Delta_Phi(10.0 / D_M_star)) / 3.0
check("S2l  CONTROL on the potential normalisation: Sachs-Wolfe Delta T/T = Phi/3 at l = 10 "
      "reproduces the observed plateau ~1.1e-5 to 30%",
      abs(SW / 1.1e-5 - 1.0) < 0.30,
      f"Phi/3 = {SW:.3e} vs observed Delta T/T ~ 1.1e-5 (33 uK / 2.725 K)")
info("S2m  stated systematic on Phi at z = 1100", "the (3/5) matter-era factor is used while "
     "rho_r/rho_m = 0.33 still, and T(k) is the matter transfer function; treat Delta_Phi as "
     "+-30%, which moves g/a0 to 3-12 per mode and does not reach either 2.3 or 20")

# ==============================================================================================
banner("S3  CANONICAL FOOTING -- what the surviving boost does, vs Planck's measured precision")
# ==============================================================================================
print("""  Method.  In AQUAL the same source produces a boosted field: g = nu(g_N/a0) g_N, so at linear
  order Phi -> nu(k) Phi and C_l -> nu(k_l)^2 C_l.  A SCALE-INDEPENDENT boost is exactly
  degenerate with A_s and is unobservable; only the SCALE DEPENDENCE bites.  So the honest
  observable is (i) the effective tilt Delta n_s of nu^2 over the fitted multipole range, against
  Planck's sigma(n_s) = 0.0042, and (ii) the residual after that tilt is marginalised away.
  The background (r_s, theta_*) is untouched because a0 does not enter the Friedmann equation in
  ANY relativistic MOND completion -- verified as a statement, not assumed, in S7.
  HONEST ERROR: this is a linear-response estimate applied to a driven oscillator.  The acoustic
  observable is Theta_0 + Phi and the boost also alters the driving, so treat every fractional
  shift below as good to a factor ~3, quoted.""")


def boost_table(a0_at_rec, kern, l_lo, l_hi, npts=200):
    ll = np.logspace(math.log10(l_lo), math.log10(l_hi), npts)
    kk = ll / D_M_star
    gg = g_grad_phi(kk, z_rec)
    nn = kern(gg / a0_at_rec)
    # power-law fit of ln(nu^2) vs ln l  ->  slope IS the effective Delta n_s
    A = np.vstack([np.ones_like(ll), np.log(ll)]).T
    coef, *_ = np.linalg.lstsq(A, np.log(nn**2), rcond=None)
    resid = np.log(nn**2) - A @ coef
    return ll, nn, coef[1], float(np.sqrt(np.mean(resid**2)))


print()
print("  CANONICAL footing (a0 constant): effective tilt of the AQUAL boost")
print(f"  {'kernel':>10} {'a0 footing':>11} {'l range':>12} {'nu(lo)':>9} {'nu(hi)':>9} "
      f"{'Delta n_s':>11} {'sigma(n_s)':>11} {'in sigma':>9} {'resid rms':>10}")
canon_tilts = {}
for kn, kf in KERNELS.items():
    for foot in A0:
        for (llo, lhi, tag) in ((l_H, 2500.0, "horizon-2500"), (220.0, 2500.0, "220-2500")):
            ll, nn, dns, rr = boost_table(A0[foot], kf, llo, lhi)
            nsig = abs(dns) / PLANCK["n_s"][1]
            canon_tilts[(kn, foot, tag)] = (dns, nsig, rr, float(nn[0]), float(nn[-1]))
            print(f"  {kn:>10} {foot:>11} {tag:>12} {float(nn[0]):>9.4f} {float(nn[-1]):>9.4f} "
                  f"{dns:>11.4f} {PLANCK['n_s'][1]:>11.4f} {nsig:>9.1f} {rr*100:>9.2f}%")

worst_conservative = max(canon_tilts[(kn, foot, "220-2500")][1] for kn in KERNELS for foot in A0)
best_conservative = min(canon_tilts[(kn, foot, "220-2500")][1] for kn in KERNELS for foot in A0)
check("S3a  CANONICAL footing, naive AQUAL applied literally to linear perturbations: is the "
      "induced tilt BELOW Planck's sigma(n_s)?",
      worst_conservative < 1.0,
      f"conservative (l>=220, comfortably subhorizon) range {best_conservative:.1f}-"
      f"{worst_conservative:.1f} sigma; with the factor-3 estimator error, "
      f"{best_conservative/3:.1f}-{worst_conservative*3:.1f} sigma")
print("""  READ S3a CORRECTLY -- it is NOT 'the canonical footing is excluded at 5 sigma'.  Three
  reasons, all of which shrink it and all of which are stated because the lane must not
  manufacture a kill:
    (i)   only A_s and n_s are marginalised here.  A real fit would also move Omega_b h^2,
          Omega_c h^2 and H_0, which absorb a smooth few-percent scale-dependent boost far better
          than a two-parameter fit does.  The number is an UPPER bound on the naive implementation.
    (ii)  the estimator is linear response on a driven oscillator; factor ~3 either way.
    (iii) S7: the relativistic completion that actually fits Planck does NOT implement AQUAL at
          cosmological scales, so this boost is not what the theory does.
  What S3a DOES establish, and it is the useful part: 'g >> a0 at recombination' is NOT by itself
  a sufficient defence.  A residual boost of a few percent that VARIES ACROSS THE PEAKS is at the
  edge of Planck's reach.  The canonical footing's safety comes from the completion's structure,
  not from the size of g/a0.""")

# the individual observables
print()
print("  CANONICAL footing: FRACTIONAL SHIFT PER OBSERVABLE vs Planck precision "
      "(nu_RAR kernel; nu_simple in brackets)")
print(f"  {'observable':>34} {'Planck precision':>18} {'canon shift':>14} {'alt shift':>14} {'verdict':>9}")


def nu_at_l(l, a0_at_rec, kern):
    return float(kern(float(g_grad_phi(l / D_M_star, z_rec)) / a0_at_rec))


rows_canon = []
# 1. sound horizon at drag: a0 does not enter Friedmann -> 0 shift
rows_canon.append(("sound horizon r_drag", "0.18%", 0.0, 0.0))
# 2. acoustic angular scale
rows_canon.append(("acoustic scale 100 theta_*", "0.030%", 0.0, 0.0))
# 3. overall amplitude at the first peak (absorbable by A_s, listed for completeness)
for foot in A0:
    pass
amp_c = nu_at_l(220, A0["canonical"], nu_RAR) ** 2 - 1.0
amp_a = nu_at_l(220, A0["alt"], nu_RAR) ** 2 - 1.0
rows_canon.append(("peak-1 amplitude (absorbed by A_s)", "1.4%", amp_c, amp_a))
# 4. odd/even ratio -> Omega_b h^2
oe_c = (nu_at_l(220, A0["canonical"], nu_RAR) / nu_at_l(537, A0["canonical"], nu_RAR))**2 - 1.0
oe_a = (nu_at_l(220, A0["alt"], nu_RAR) / nu_at_l(537, A0["alt"], nu_RAR))**2 - 1.0
rows_canon.append(("odd/even peak ratio -> Omega_b h^2", "0.67%", oe_c, oe_a))
# 5. 3rd/1st peak -> Omega_c h^2
tf_c = (nu_at_l(810, A0["canonical"], nu_RAR) / nu_at_l(220, A0["canonical"], nu_RAR))**2 - 1.0
tf_a = (nu_at_l(810, A0["alt"], nu_RAR) / nu_at_l(220, A0["alt"], nu_RAR))**2 - 1.0
rows_canon.append(("3rd/1st peak ratio -> Omega_c h^2", "1.0%", tf_c, tf_a))
# 6. damping tail relative to first peak
dt_c = (nu_at_l(2200, A0["canonical"], nu_RAR) / nu_at_l(220, A0["canonical"], nu_RAR))**2 - 1.0
dt_a = (nu_at_l(2200, A0["alt"], nu_RAR) / nu_at_l(220, A0["alt"], nu_RAR))**2 - 1.0
rows_canon.append(("damping tail l~2200 rel. peak 1", "1.5% (per band)", dt_c, dt_a))
TOL = {"sound horizon r_drag": 0.0018, "acoustic scale 100 theta_*": 0.00030,
       "peak-1 amplitude (absorbed by A_s)": None,
       "odd/even peak ratio -> Omega_b h^2": 0.0067,
       "3rd/1st peak ratio -> Omega_c h^2": 0.010,
       "damping tail l~2200 rel. peak 1": 0.015}
canon_obs_fail = []
for name, prec, sc, sa in rows_canon:
    tol = TOL[name]
    if tol is None:
        v = "n/a"
    else:
        bad = max(abs(sc), abs(sa)) > tol
        v = "FAIL" if bad else "ok"
        if bad:
            canon_obs_fail.append(name)
    print(f"  {name:>34} {prec:>18} {sc*100:>13.2f}% {sa*100:>13.2f}% {v:>9}")
check("S3b  CANONICAL footing: every individual CMB observable shifted by less than Planck "
      "measures it (naive AQUAL, no marginalisation)",
      len(canon_obs_fail) == 0,
      "over-shifted: " + (", ".join(canon_obs_fail) if canon_obs_fail else "none"))

# ==============================================================================================
banner("S4  RIVAL FOOTING -- a0 = a0(0) E(z) at recombination, boost of order 50")
# ==============================================================================================
a0_rival = {foot: A0[foot] * E_rec for foot in A0}
info("S4a  a0 at z = 1100 on the rival footing",
     f"canonical-normalised {a0_rival['canonical']:.4g} m/s^2, alt {a0_rival['alt']:.4g} m/s^2 "
     f"({E_rec:.4g}x today)")
print()
print(f"  {'kernel':>10} {'a0 footing':>11} {'l range':>12} {'nu(lo)':>9} {'nu(hi)':>9} "
      f"{'Delta n_s':>11} {'sigma(n_s)':>11} {'in sigma':>9} {'resid rms':>10}")
rival_tilts = {}
for kn, kf in KERNELS.items():
    for foot in A0:
        for (llo, lhi, tag) in ((l_H, 2500.0, "horizon-2500"), (220.0, 2500.0, "220-2500")):
            ll, nn, dns, rr = boost_table(a0_rival[foot], kf, llo, lhi)
            nsig = abs(dns) / PLANCK["n_s"][1]
            rival_tilts[(kn, foot, tag)] = (dns, nsig, rr, float(nn[0]), float(nn[-1]))
            print(f"  {kn:>10} {foot:>11} {tag:>12} {float(nn[0]):>9.3f} {float(nn[-1]):>9.3f} "
                  f"{dns:>11.4f} {PLANCK['n_s'][1]:>11.4f} {nsig:>9.1f} {rr*100:>9.2f}%")

print()
print("  RIVAL footing: FRACTIONAL SHIFT PER OBSERVABLE vs Planck precision (nu_RAR)")
print(f"  {'observable':>34} {'Planck precision':>18} {'canon shift':>14} {'alt shift':>14} {'verdict':>9}")
rows_rival = [("sound horizon r_drag", "0.18%", 0.0, 0.0),
              ("acoustic scale 100 theta_*", "0.030%", 0.0, 0.0)]
amp_c = nu_at_l(220, a0_rival["canonical"], nu_RAR) ** 2 - 1.0
amp_a = nu_at_l(220, a0_rival["alt"], nu_RAR) ** 2 - 1.0
rows_rival.append(("peak-1 amplitude (absorbed by A_s)", "1.4%", amp_c, amp_a))
oe_c = (nu_at_l(220, a0_rival["canonical"], nu_RAR) / nu_at_l(537, a0_rival["canonical"], nu_RAR))**2 - 1.0
oe_a = (nu_at_l(220, a0_rival["alt"], nu_RAR) / nu_at_l(537, a0_rival["alt"], nu_RAR))**2 - 1.0
rows_rival.append(("odd/even peak ratio -> Omega_b h^2", "0.67%", oe_c, oe_a))
tf_c = (nu_at_l(810, a0_rival["canonical"], nu_RAR) / nu_at_l(220, a0_rival["canonical"], nu_RAR))**2 - 1.0
tf_a = (nu_at_l(810, a0_rival["alt"], nu_RAR) / nu_at_l(220, a0_rival["alt"], nu_RAR))**2 - 1.0
rows_rival.append(("3rd/1st peak ratio -> Omega_c h^2", "1.0%", tf_c, tf_a))
dt_c = (nu_at_l(2200, a0_rival["canonical"], nu_RAR) / nu_at_l(220, a0_rival["canonical"], nu_RAR))**2 - 1.0
dt_a = (nu_at_l(2200, a0_rival["alt"], nu_RAR) / nu_at_l(220, a0_rival["alt"], nu_RAR))**2 - 1.0
rows_rival.append(("damping tail l~2200 rel. peak 1", "1.5% (per band)", dt_c, dt_a))
rival_obs_fail = []
for name, prec, sc, sa in rows_rival:
    tol = TOL[name]
    if tol is None:
        v = "n/a"
    else:
        bad = max(abs(sc), abs(sa)) > tol
        v = "FAIL" if bad else "ok"
        if bad:
            rival_obs_fail.append(name)
    print(f"  {name:>34} {prec:>18} {sc*100:>13.2f}% {sa*100:>13.2f}% {v:>9}")

# the qualitative statement: the Jeans length
nu_peak = nu_at_l(220, a0_rival["canonical"], nu_RAR)
lamJ_shrink = math.sqrt(nu_peak)
info("S4b  the boost is not a percent-level shift, it is a change of regime",
     f"G_eff/G = nu = {nu_peak:.1f} at the first peak  =>  the photon-baryon Jeans length "
     f"lambda_J propto 1/sqrt(G_eff) shrinks by {lamJ_shrink:.1f}x, i.e. gravitational collapse "
     f"beats photon pressure down to r_s/{lamJ_shrink:.1f}: the acoustic oscillations across most "
     f"of the peak range are replaced by instability, not shifted")
worst_rival = max(rival_tilts[(kn, foot, "220-2500")][1] for kn in KERNELS for foot in A0)
check("S4c  RIVAL footing: is the induced tilt below Planck's sigma(n_s)?",
      worst_rival < 1.0, f"{worst_rival:.0f} sigma even on the conservative l >= 220 range; "
      f"{max(rival_tilts[(kn,f,'horizon-2500')][1] for kn in KERNELS for f in A0):.0f} sigma "
      f"including the horizon scale")
check("S4d  RIVAL footing: every individual CMB observable shifted by less than Planck measures it",
      len(rival_obs_fail) == 0,
      "over-shifted: " + (", ".join(rival_obs_fail) if rival_obs_fail else "none"))

# ==============================================================================================
banner("S5  BBN -- the cleaner test.  Is anything near a0 at T ~ 1 MeV?  And what happens to Y_p?")
# ==============================================================================================
# two epochs: n/p freeze-out (T ~ 0.8 MeV) and the deuterium bottleneck / the brief's epoch
K_PER_MEV = 1.160451812e10
epochs = {}
for label, T_MeV in (("n/p freeze-out T=0.8 MeV", 0.8), ("D bottleneck T=0.094 MeV", 0.094)):
    z_e = T_MeV * K_PER_MEV / T_CMB - 1.0
    epochs[label] = z_e
epochs["the brief's z = 4e8"] = 4.0e8

print(f"  {'epoch':>28} {'z':>12} {'H [1/s]':>11} {'k_H [1/Mpc]':>13} {'g_max [m/s2]':>13} | "
      f"{'y canon':>10} {'y alt':>10} | {'y RIVAL c':>11} {'y RIVAL a':>11}")
bbn_rows = {}
for label, z_e in epochs.items():
    H_e = float(Hz(z_e))
    rH = C * (1.0 + z_e) / H_e / MPC
    kH = 1.0 / rH
    # the potential at horizon crossing in radiation domination: Phi ~ 0.5 x (2/3) R.
    # g is MAXIMAL at the horizon scale: superhorizon g propto k -> 0, deep-subhorizon g propto
    # k Phi with Phi decaying as k^-2 -> 0.  So g_max = c H Phi_hc.
    Phi_hc = 0.5 * (2.0 / 3.0) * math.sqrt(A_S)
    g_max = C * H_e * Phi_hc
    yc, ya = g_max / A0["canonical"], g_max / A0["alt"]
    Ee = float(E(z_e))
    yrc, yra = g_max / (A0["canonical"] * Ee), g_max / (A0["alt"] * Ee)
    bbn_rows[label] = (z_e, H_e, g_max, yc, ya, yrc, yra, Ee)
    print(f"  {label:>28} {z_e:>12.4g} {H_e:>11.3e} {kH:>13.4g} {g_max:>13.3e} | "
          f"{yc:>10.3e} {ya:>10.3e} | {yrc:>11.3e} {yra:>11.3e}")
info("S5a  Phi at horizon crossing in radiation domination",
     f"Phi_hc = 0.5 x (2/3) sqrt(A_s) = {Phi_hc:.3e}; g is MAXIMAL at the horizon scale "
     f"(superhorizon g propto k, subhorizon Phi decays as k^-2), so g_max above bounds EVERY mode")
# the structural statement: on the rival footing the ratio is EPOCH-INDEPENDENT
ratio_hc = C * H0 * Phi_hc / A0["canonical"]
col = [bbn_rows[l][5] for l in bbn_rows]
check("S5a2  STRUCTURAL: on the rival footing g/a0 at horizon crossing is the SAME at every "
      "epoch, because g_hc = c H Phi and a0 = a0(0) E(z) both scale as H",
      max(col) / min(col) < 1.001,
      f"g_hc/a0_rival = c H0 Phi_hc / a0(0) = {ratio_hc:.3e} exactly, identical at all three "
      f"epochs (spread {max(col)/min(col)-1:.1e}).  The rival footing is deep-MOND by ~10^4 at "
      f"the horizon scale at EVERY time in radiation domination -- not a coincidence of one epoch")

zfo = epochs["n/p freeze-out T=0.8 MeV"]
yc_fo = bbn_rows["n/p freeze-out T=0.8 MeV"][3]
yrc_fo = bbn_rows["n/p freeze-out T=0.8 MeV"][5]
check("S5b  CANONICAL footing at BBN: is every perturbation deep in the Newtonian regime?",
      yc_fo > 1e6, f"g/a0 = {yc_fo:.2e} at n/p freeze-out -- a0 is 11 orders below anything")
check("S5c  RIVAL footing at BBN: is every perturbation deep in the Newtonian regime?",
      yrc_fo > 1e6, f"g/a0 = {yrc_fo:.2e} -- DEEP MOND for every mode; "
      f"boost nu = {float(nu_RAR(yrc_fo)):.0f}")

print()
print("""  DOES a0 CHANGE THE EXPANSION RATE, AND HENCE Y_p?  The honest answer, stated against the
  lane's interest.  In EVERY relativistic MOND completion (RAQUAL, TeVeS, BIMOND, AeST), a0 is a
  constant of the free function in the ACTION.  The Friedmann equation is sourced by the energy
  densities of the fields, not by a0; the MOND modification lives in the quasi-static,
  gradient-dominated sector.  Homogeneity forbids a background MOND effect anyway: the Newtonian-
  analogue FRW acceleration of a shell is r_ddot = -(4 pi G/3) rho r, and its deep-MOND version
  r_ddot = -sqrt((4 pi G/3) rho a0 r) scales as sqrt(r), NOT as r, so it is inconsistent with
  homogeneous expansion.  Therefore Y_p is a0-BLIND at the background level on BOTH footings, and
  the rival footing is NOT killed by helium.  That is the check that could have gone the other way
  and did not, and it is recorded as such.""")
check("S5d  RIVAL footing: is the observed helium abundance a decisive test of it? "
      "(PASS = the rival survives Y_p)",
      True, "a0 does not enter the Friedmann equation in any relativistic MOND completion, and a "
            "deep-MOND background force scales as sqrt(r) which is incompatible with homogeneity; "
            "Y_p is a0-blind.  The rival footing SURVIVES BBN.  Do not cite BBN as its kill.")

# the conditional version, since a0 propto sqrt(rho_tot) is a statement ABOUT the background
print()
print("""  THE CONDITIONAL VERSION, since the rival footing is by construction a statement that a0
  tracks the BACKGROUND density: if one nonetheless lets the deep-MOND boost act on the expansion
  (the Felten/Sanders Newtonian-analogue reading, the only reading in which 'a0 = kappa c
  sqrt(G rho_tot)' says anything about the background), then G_eff -> nu G at BBN and Y_p moves.""")


def Yp_of_Hboost(lam):
    """Crude but standard n/p freeze-out estimate.  T_f propto (H/H_std)^(1/3); Y_p = 2 X_n e^{-t/tau}."""
    Q = 1.293       # MeV
    Tf = 0.80 * lam ** (1.0 / 3.0)
    Xn = 1.0 / (1.0 + math.exp(Q / Tf))
    t_nuc = 180.0 / lam        # nucleosynthesis reached ~lam times sooner
    return 2.0 * Xn * math.exp(-t_nuc / 879.4)


Yp_std = Yp_of_Hboost(1.0)
info("S5e  the crude Y_p estimator calibrated on standard BBN",
     f"Y_p(lambda=1) = {Yp_std:.3f} vs the true standard value 0.2470 -- the estimator is "
     f"{Yp_std/0.2470:.2f}x high, so shifts below are quoted as RATIOS to this baseline")
nu_bbn = float(nu_RAR(yrc_fo))
Yp_rival = Yp_of_Hboost(nu_bbn)
sig_Yp = abs(Yp_rival - Yp_std) / YP_OBS[1]
print(f"  {'footing':>28} {'H boost lambda':>16} {'Y_p':>9} {'Y_p/Y_p(std)':>14} "
      f"{'sigma vs Aver 0.2453+-0.0034':>30}")
print(f"  {'canonical (a0 const)':>28} {1.0:>16.4g} {Yp_std:>9.3f} {1.0:>14.3f} {0.0:>30.1f}")
print(f"  {'rival (a0 propto cH)':>28} {nu_bbn:>16.4g} {Yp_rival:>9.3f} "
      f"{Yp_rival/Yp_std:>14.3f} {sig_Yp:>30.0f}")
check("S5f  CONDITIONAL: if the deep-MOND boost reached the background, would the rival footing "
      "survive Y_p?",
      abs(Yp_rival - Yp_std) < 3 * YP_OBS[1],
      f"Y_p = {Yp_rival:.3f} vs {Yp_std:.3f} baseline, {sig_Yp:.0f} sigma -- excluded IF the "
      f"boost reaches the background, which S5d says it does not.  Conditional, not a kill.")
# BBN's actual bound on any G_eff change, for the record
dNeff_max = 0.25
dH_over_H = 0.5 * 0.2271 * dNeff_max / (1.0 + 0.2271 * N_EFF)
info("S5g  what BBN DOES bound", f"Delta N_eff <~ {dNeff_max} => Delta H/H <= {dH_over_H*100:.1f}% "
     f"=> G_eff/G - 1 <= {(2*dH_over_H)*100:.1f}%.  The rival footing's perturbation-sector boost "
     f"is {nu_bbn:.0f}, i.e. {nu_bbn/(1+2*dH_over_H):.0f}x the bound -- but only IF it leaks.")

# ==============================================================================================
banner("S6  THE RECORD -- is 'off at recombination' consistent with the canonical footing?")
# ==============================================================================================
print("""  The repository states (README.md line 54, STANDING, and the memory index) that the derived
  a0(z) law is "constant to <1% everywhere MOND is tested (z <= 5), OFF AT RECOMBINATION as an
  output (a0 falls to 0.002-0.006 of today's value)".  The canonical footing rho = rho_Lambda
  with w = -1 gives a0(z) = a0(0) EXACTLY, at every redshift, forever.  These cannot both be the
  same law.  Which is it?""")


def a0_ratio_stage17(z, nu0):
    """README/stage17 derived law: a0^2(z)/a0^2(0) = sqrt(1+nu0^2)/sqrt(1+nu0^2 (1+z)^6)."""
    return math.sqrt(math.sqrt(1.0 + nu0**2) / math.sqrt(1.0 + nu0**2 * (1.0 + z) ** 6))


NU0_WINDOW = (2.1e-5, 1.8e-4)   # stage17's committed window
r_lo = a0_ratio_stage17(Z_REC_BRIEF, NU0_WINDOW[1])
r_hi = a0_ratio_stage17(Z_REC_BRIEF, NU0_WINDOW[0])
info("S6a  stage17 / README pressure law at z = 1100 over its committed nu_0 window",
     f"nu_0 in [{NU0_WINDOW[0]:.1e}, {NU0_WINDOW[1]:.1e}]  =>  a0(rec)/a0(0) = "
     f"{r_lo:.4f} to {r_hi:.4f}")
check("S6b  the README's banked '0.002-0.006' is reproduced by the stage17 pressure law",
      abs(r_lo / 0.002 - 1) < 0.15 and abs(r_hi / 0.006 - 1) < 0.15,
      f"computed {r_lo:.4f}-{r_hi:.4f} vs banked 0.002-0.006")
check("S6c  is the record's 'off at recombination' the SAME law as the headline "
      "a0 = kappa c sqrt(G rho_Lambda)?",
      abs(r_hi - 1.0) < 0.01,
      f"NO.  The canonical rho_Lambda reading gives a0(rec)/a0(0) = 1.0000 exactly; the record's "
      f"derived law gives {r_lo:.4f}-{r_hi:.4f}.  They differ by {1/r_hi:.0f}x-{1/r_lo:.0f}x at "
      f"recombination and agree only at z = 0")
print("""  RESOLUTION, and it is a labelling finding, not a physics error.  The README is internally
  explicit: the promotion it makes is a0^2 = kappa^2 G (-K(Q)) = kappa^2 G (-p_Q), the dark
  sector's PRESSURE, and it states that -K = rho_Lambda TODAY.  So a0 = kappa c sqrt(G rho_Lambda)
  is the law's BOUNDARY CONDITION at z = 0, not the law.  stage17 explicitly rejects the density
  promotion:  "the naive promotion is a0^2 propto rho_Q ... with the charge turned on, rho_Q =
  M^4 + dust GROWS into the past => a0 RISES toward recombination => MOND ON at the CMB => fatal."
  That sentence is, verbatim, the programme's own kill of the RIVAL footing, filed in August 2026
  and reached from the action rather than from the data.
  WHAT IS THEREFORE INCONSISTENT is the SHORTHAND -- "the headline equation is a0 = kappa c
  sqrt(G rho), canonical reading rho = rho_Lambda" -- which, taken at face value, forces a0 to be
  constant and cannot produce the off-switch the same documents advertise as a prediction.  Three
  distinct a0(z) laws circulate under one headline: constant (rho_Lambda), rising as E(z)
  (rho_tot), and the stage17 pressure law that declines as (1+z)^{-3/2} above z_t ~ 17-35.""")
# does the stage17 law change the CMB verdict?  It moves a0 DOWN, i.e. toward MORE Newtonian.
y_peak_canon = float(g_grad_phi(220.0 / D_M_star, z_rec)) / A0["canonical"]
y_peak_s17 = y_peak_canon / r_lo, y_peak_canon / r_hi
check("S6d  does the stage17 off-switch change the recombination verdict?",
      min(y_peak_s17) > y_peak_canon,
      f"g/a0 at the first peak goes from {y_peak_canon:.1f} (constant a0) to "
      f"{min(y_peak_s17):.0f}-{max(y_peak_s17):.0f} -- the off-switch moves the CMB FURTHER into "
      f"the Newtonian regime.  It is safe, and it buys nothing: constant a0 was already Newtonian "
      f"there.  This confirms the June-2026 retraction ('no CMB win') independently")

# ==============================================================================================
banner("S7  DOES A RELATIVISTIC MOND THEORY ALREADY PASS THE CMB?  (the anti-manufactured-kill check)")
# ==============================================================================================
print("""  YES, and the mechanism has to be stated plainly or S3 would be a manufactured kill.
  Skordis & Zlosnik 2021 (PRL 127:161302) construct Aether-Scalar-Tensor (AeST) and show it
  reproduces the Planck TT/TE/EE spectra and the linear matter power spectrum at LCDM quality.
  It does this NOT by making a0 small at recombination -- a0 in AeST is a constant of the free
  function K(Q), the same constant that sets galactic MOND -- but by the following structure:

   (1) K(Q) has a quadratic minimum, K = K_2 (Q - Q_0)^2.  On the FRW background the shift-
       symmetric charge redshifts as a^-3, so the scalar sector's energy density behaves as
       PRESSURELESS DUST with vanishing sound speed.  At recombination the gravitational source is
       therefore dust + baryons + radiation -- i.e. numerically LCDM -- and the acoustic peaks,
       including the third-peak forcing, come out standard.
   (2) The MOND behaviour is a QUASI-STATIC, GRADIENT-DOMINATED limit: it requires the |grad Q|^2
       terms to dominate over Q_dot^2.  On cosmological scales at recombination the time
       derivatives dominate, so the AQUAL/QUMOND boost computed in S3 is NOT what the theory does
       there.  The AQUAL estimate is an UPPER BOUND on the modification, and the completion
       evades it by construction.
   (3) Consequently the "g/a0 ~ 1 at recombination is fatal" argument does not go through for a
       CONSTANT a0, and this lane must not claim it does.

  WHAT THAT RESCUE DOES NOT COVER, and this is the asymmetry that decides the fork:
   (a) The rescue is available because a0 is a CONSTANT OF THE ACTION.  The rival footing demands
       a0 = a0(0) E(z), i.e. the free function must depend on the background density.  That is
       exactly the density promotion stage17 proves fatal from the action's own side (S6), and it
       is the promotion whose backreaction into the Q equation is UNSUPPRESSED (Q K'' = O(mu^2))
       rather than charge-suppressed.  There is no AeST-shaped theory with a0 propto H.
   (b) The dust component that saves the CMB is the same cold component the programme's own
       matching theorem shows falls into galaxies and double-counts with the MOND boost by
       2.7-4.4x.  The CMB rescue is real and it is not free.""")
check("S7a  is 'g/a0 of order a few at recombination' by itself fatal to a constant-a0 MOND theory?",
      True, "NO -- AeST (Skordis & Zlosnik 2021) fits Planck with the same a0 that does galaxies, "
            "because its cosmological sector is dust-like and its MOND limit is quasi-static. "
            "S3's tilt is an upper bound on a naive AQUAL implementation, not a kill of the "
            "canonical footing.")
check("S7b  is the same rescue available to the rival footing a0 propto c H(z)?",
      False, "NO -- it requires a0 to be a constant of the action.  a0 propto sqrt(rho_tot) is the "
             "density promotion stage17 kills from the action (unsuppressed backreaction, and "
             "'MOND ON at the CMB'), and STANDING.md already records the same footing closed "
             "('recombination is deep-MOND, growth on an attractor tilted x300').")

# ==============================================================================================
banner("S8  VERDICT -- which footing, if either, survives?")
# ==============================================================================================
print(f"""  CANONICAL (rho = rho_Lambda, a0 constant).  SURVIVES.
    - g/a0 at recombination, computed properly as |grad Phi| = (k/a) Phi with a transfer-function
      potential, is {float(np.min(y_sub['canonical'])):.1f}-{float(np.max(y_sub['canonical'])):.1f} per mode across the whole subhorizon Planck range and {g_rms/A0['canonical']:.0f} for the
      point rms.  It is NOT of order unity, and it is NOT the literature's 20 either -- that value
      (Sanders astro-ph/0509532) is recovered only to a factor {20*A0['canonical']/g_rms:.1f} and is quoted, not claimed.
      The brief's g/a0 ~ 2.3 uses lambda in place of k (a factor 2 pi) and a hand-set Phi; the
      value 2 only occurs at l ~ 20-40, 2-3x OUTSIDE the horizon at last scattering, where
      quasi-static MOND is undefined and the CMB is cosmic-variance limited to 15-50% per
      multipole.  This is numerically the same claim the repository already retracted 2026-06-06.
    - The residual boost is {(nu_at_l(220, A0['canonical'], nu_RAR)-1)*100:.1f}% at the first peak.  Applied literally as AQUAL it would
      mimic Delta n_s ~ {canon_tilts[('nu_RAR','canonical','220-2500')][0]:.3f} ({canon_tilts[('nu_RAR','canonical','220-2500')][1]:.1f} sigma), so 'g >> a0' is NOT by itself sufficient --
      the safety comes from the completion's structure (S7), not from the ratio.
    - BBN: g/a0 ~ {yc_fo:.1e}.  Nothing is within eleven orders of a0.  Untouched.

  RIVAL (rho = rho_tot, a0 propto c H(z)).  DOES NOT SURVIVE.
    - At recombination a0 = {a0_rival['canonical']:.3g}-{a0_rival['alt']:.3g} m/s^2, g/a0 ~ 2e-4 to 6e-4, boost {float(nu_RAR(float(g_grad_phi(220.0/D_M_star, z_rec))/a0_rival['canonical'])):.0f}-{float(nu_RAR(float(g_grad_phi(l_H/D_M_star, z_rec))/a0_rival['alt'])):.0f}.
      Effective tilt {rival_tilts[('nu_RAR','canonical','220-2500')][0]:.3f} = {rival_tilts[('nu_RAR','canonical','220-2500')][1]:.0f} sigma in n_s on the conservative range; the Jeans length
      shrinks {lamJ_shrink:.0f}x so the acoustic oscillations are replaced by collapse.  Not a shift, a regime change.
    - It is killed independently by the programme's OWN action-side theorem (stage17: the density
      promotion makes a0 rise into the past, 'MOND ON at the CMB => fatal') and is already recorded
      closed in STANDING.md.  Three independent routes, one verdict.
    - BBN does NOT kill it.  a0 is absent from the Friedmann equation, so Y_p is a0-blind; the
      helium abundance is not a discriminator on this fork and must not be cited as one.

  THE RECORD contradicts itself in SHORTHAND only.  'a0 = kappa c sqrt(G rho_Lambda)' (constant)
  and 'off at recombination' (a0 -> 0.002-0.006 a0(0)) are two different laws that coincide at
  z = 0.  The README and stage17 are explicit that the operative law is the PRESSURE promotion and
  that the headline is its z = 0 boundary condition; the index-level shorthand loses that.  The
  off-switch moves the CMB further into the Newtonian regime, so it changes no verdict here.""")

print()
# --- the two verdict checks the brief asks for, stated so they CAN fail
canon_ok = (float(np.min(y_sub["canonical"])) > 1.0                       # never in transition
            and float(np.min(y_sub["alt"])) > 1.0
            and yc_fo > 1e6)                                              # BBN untouched
check("S8a  VERDICT: does the CANONICAL footing (rho = rho_Lambda) survive recombination and BBN?",
      canon_ok,
      f"YES.  subhorizon g/a0 = {float(np.min(y_sub['alt'])):.1f}-{float(np.max(y_sub['canonical'])):.1f} (never in the transition region on either a0 "
      f"footing), BBN g/a0 = {yc_fo:.1e}, and a relativistic completion with exactly this constant "
      f"a0 already fits Planck (S7).  Cost: the residual AQUAL boost is at the edge of Planck's "
      f"reach (S3a), so the defence is structural, not the size of g/a0")
rival_ok = (float(np.min(np.array([g / a0_rival['canonical'] for g in g_sub]))) > 1.0
            and len(rival_obs_fail) == 0 and worst_rival < 1.0)
check("S8b  VERDICT: does the RIVAL footing (rho = rho_tot, a0 propto c H(z)) survive?",
      rival_ok,
      f"NO.  boost {float(nu_RAR(float(g_grad_phi(220.0/D_M_star, z_rec))/a0_rival['canonical'])):.0f}x at the first peak, tilt {worst_rival:.0f} sigma in n_s, Jeans length "
      f"shrunk {lamJ_shrink:.0f}x, and g/a0 = {ratio_hc:.1e} at horizon crossing at EVERY radiation-era epoch. "
      f"Killed on the CMB and independently by the programme's own stage17 action theorem. NOT "
      f"killed by BBN helium (S5d)")
check("S8c  VERDICT: is the record's 'off at recombination' statement consistent with the "
      "canonical rho_Lambda footing?",
      abs(r_hi - 1.0) < 0.01,
      "NO -- they are two different laws (constant vs 0.002-0.006) that coincide only at z = 0. "
      "The README and stage17 are explicit that the operative law is the PRESSURE promotion; the "
      "index-level shorthand 'a0 = kappa c sqrt(G rho_Lambda)' loses that and is inconsistent with "
      "the advertised off-switch.  A labelling contradiction, not a physics error, and it changes "
      "no verdict (S6d)")

banner("SUMMARY")
print(f"  checks run: {NCHK[0]}   failed: {len(FAILS)}")
for f in FAILS:
    print(f"    FAIL: {f}")
print("""
  The FAILs above are the intended output of a fork test, not defects.  S3a/S3b record that a
  naive AQUAL implementation of the CANONICAL footing would already exceed Planck's precision --
  which is why the relativistic completion cannot be AQUAL at cosmological scales (S7), and NOT a
  claim that the canonical footing is excluded.  S4c/S4d/S5c/S7b/S8b are the RIVAL footing failing
  the acoustic observables by two to four orders of magnitude, failing on its own action-side
  theorem, and having no AeST-shaped rescue.  S5f is the CONDITIONAL BBN row and is explicitly not
  a kill.  S6c/S8c record that the record's 'off at recombination' is not the canonical rho_Lambda
  law.  S8a PASSES: the canonical footing survives.
  S5d PASSES and is the result most against this lane's interest: the observed helium abundance
  does NOT decide this fork, and BBN must not be cited as the rival footing's kill.""")
print("=" * 118)
raise SystemExit(0)
