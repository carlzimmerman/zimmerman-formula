#!/usr/bin/env python3
r"""
W-4  NATURALNESS AUDIT OF THE GATE CORNER omega_c
==================================================================================================
Framework: Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA program, judged on ITS OWN terms
(own kernel nu = sqrt(1+1/y), K(z) = (sqrt(1+4z)-1)/(2 sqrt z); horizon-derived a0 = c H_Lambda / Z,
Z = sqrt(32 pi/3) = 5.78881).  Source of every quoted band and scale:
    real_research/papers/MI_FIELD_THEORY_RESULTS_2026.md  Secs. 2.1, 5.1-5.4, E10, E12
    real_research/reviews/mi_cassini_q2_omegac_2026.py    (the committed <2% window rebuild)
    prep_2026/mi_planetary_falsification/{window_joint,loweredge_fullsparc,origin_window_scales}.py

QUESTION (W-4 only -- W-1/W-2/W-3 are other lanes):  the solar system forces the gate corner to
omega_c ~ 2e-14 rad/s.  Does the WRITTEN THEORY supply ANY intrinsic frequency near that value?

WHAT THIS SCRIPT DOES
  0. REGRESSION: rebuild both window edges and assert agreement with the committed pass (<0.5%).
  1. DIMENSIONAL CENSUS: prove (by counting the action's dimensionful content) that every frequency
     the classical action can build is either  (pure number) x H_Lambda  or the ENVIRONMENTAL
     sqrt(G rho).  There is no third branch.
  2. ENUMERATE every intrinsic frequency explicitly -- a0/2pi c, a0/2c, a0/c, 4a0/c (disformal B),
     T_dS = H_Lambda/2pi, H_Lambda, H_0, Z H_Lambda, Z^n H_Lambda, 1/t_universe, Herglotz measure
     support, Planck -- both footings, with the dex gap to omega_c.
  3. (a) PERIOD of the corner in years, and an honest search for ANY physical process at that period.
  4. (b) FINE-TUNING, quantified: log-prior fraction of the surviving window under three explicit
     priors, plus the scale-free (no-UV-cutoff) statement.
  5. THRESHOLD SENSITIVITY of the (non-negotiable, theory-internal) LOWER edge.

CALIBRATION HELD:  no manufactured exclusion, no manufactured comfort.  The alt footing is NOT
declared excluded.  The window is NOT declared comfortable.  Both footings on every number.
No TOE language, no "theory closed".  numpy only.  Exits 0.
"""
import numpy as np

# ==================================================================================================
# 0.  CONSTANTS, FOOTINGS, AND THE COMMITTED WINDOW (regression anchor)
# ==================================================================================================
C     = 2.99792458e8          # m/s
G     = 6.674e-11             # m^3 kg^-1 s^-2
HBAR  = 1.054571817e-34       # J s
YR    = 365.25 * 86400.0      # s   (same Julian year as the committed pass)
MYR, GYR = 1e6 * YR, 1e9 * YR
MSUN  = 1.98892e30            # kg
PC    = 3.0856776e16          # m
KPC   = 1e3 * PC
MPC   = 1e6 * PC

Z_FRAME = np.sqrt(32 * np.pi / 3)          # 5.78881, postulated (kappa=1/2 provably unforceable)
A0 = {"canon": 9.355e-11, "alt": 1.1305e-10}   # paper Sec. 1: rho_DE/cH_Lambda vs rho_total/cH0
FOOT = ("canon", "alt")

# --- window inputs, verbatim from the committed pass -----------------------------------------------
OMEGA_GAL_MAX = 5.94e-15      # rad/s, UGC05721 innermost deep-MOND orbit (151 gal / 2188 points)
GATE_KEEP     = 0.90          # theory-internal: Re G >= 0.90 at EVERY confirmed deep-MOND orbit
GDOT_LLR_2SIG = 2.42e-14      # /yr, Biskupek & Mueller 2021, |central| + 2 sigma
GM_EARTH, R_MOON = 3.986004418e14, 3.844e8
COMMITTED = {"canon": (1.782e-14, 2.211e-14), "alt": (1.782e-14, 1.831e-14)}

RULE = "=" * 102
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)

def ReG(omega, wc): return 1.0 / (1.0 + (omega / wc) ** 2)

head("0.  REGRESSION -- rebuild both window edges, assert vs mi_cassini_q2_omegac_2026.py")
k_lo    = 1.0 / np.sqrt(1.0 / GATE_KEEP - 1.0)          # = 3 exactly for Re G >= 0.9
gN_moon = GM_EARTH / R_MOON ** 2
WIN = {}
print(f"\n  lower edge = k * omega_gal,max,  k = 1/sqrt(1/{GATE_KEEP}-1) = {k_lo:.6f}  (THEORY-INTERNAL)")
print(f"  upper edge = (Gdot/G)_2sig * g_N(Moon)/a0 ,  g_N(Moon) = {gN_moon:.4e} m/s^2  (OBSERVATIONAL)\n")
print(f"  {'footing':<8}{'a0 [m/s^2]':>13}{'lower':>13}{'upper':>13}{'width':>9}"
      f"{'committed':>26}{'dev':>10}")
print("  " + "-" * 92)
for f in FOOT:
    lo = OMEGA_GAL_MAX * k_lo
    hi = (GDOT_LLR_2SIG / YR) * gN_moon / A0[f]
    WIN[f] = (lo, hi)
    clo, chi = COMMITTED[f]
    dev = max(abs(lo / clo - 1), abs(hi / chi - 1))
    print(f"  {f:<8}{A0[f]:>13.4e}{lo:>13.4e}{hi:>13.4e}{hi/lo:>8.3f}x"
          f"{f'[{clo:.3e},{chi:.3e}]':>26}{dev:>9.2%}")
    assert dev < 5e-3, f"regression against the committed window failed for {f}"
print("\n  Both edges reproduced to <0.5%.  Regression anchor SET.  The lower edge is footing-")
print("  INDEPENDENT (galaxy orbits); the upper edge scales as 1/a0 (footing-DEPENDENT).")

# ==================================================================================================
# 1.  DIMENSIONAL CENSUS -- how many frequency branches can the classical action even build?
# ==================================================================================================
head("1.  DIMENSIONAL CENSUS -- the action's dimensionful content, and the branches it permits")
print(f"""
  S = S_EH[g] + S_u[g,u,lambda] + S_matter[g,u,psi;K(Box_u/a0^2)] + S_photon[g + B uu]

  DIMENSIONFUL constants appearing anywhere in S:   c ,  G ,  Lambda   (a0 = c H_Lambda/Z is DERIVED
      from Lambda and the DIMENSIONLESS Z; s = -1, eta, and the Herglotz branch point t = -1/4 are
      all dimensionless and supply NO scale).
  DIMENSIONFUL FIELD:   rho_m  (in S_matter).   No hbar: the action is classical.

  Dimensional analysis over {{c, G, Lambda}} for a quantity of dimension 1/s:
      [c] = m/s ,  [G] = m^3 kg^-1 s^-2 ,  [Lambda] = m^-2.
      G carries an inverse MASS, so no monomial c^a G^b Lambda^d with b != 0 can be mass-free.
      => b = 0 forced, and then c^a Lambda^d has dimension m^(a+... ) s^-a  =>  a = 1, d = 1/2.
      THE ONLY constant frequency the classical action can build is  c sqrt(Lambda)  x (pure number),
      i.e. the H_Lambda family.  Introducing rho_m re-opens G, giving the SECOND branch sqrt(G rho) --
      but rho is a FIELD VALUE (environmental), not a constant of the theory.

  ROBUSTNESS OF THE COUNT:  the paper treats a0's VALUE as an independent postulate rather than as a
  consequence of Lambda.  Take that reading instead -- dimensionful constants {{c, G, a0}} -- and the
  same elimination applies (G still carries an inverse mass, so b = 0 forced), leaving
  (pure number) x a0/c.  Since a0/c = H_Lambda/Z, it is the SAME single family either way.  The count
  does not depend on which of {{Lambda, a0}} is taken as primitive.

  ==> EXACTLY TWO BRANCHES.  Branch I: (pure number) x H_Lambda  [constant, theory-supplied].
      Branch II: sqrt(4 pi G rho)                                 [environmental, not a constant].
  This is not a survey that might have missed a candidate -- it is a closed count.  Section 2 walks
  Branch I explicitly; Section 2b handles Branch II (and shows its apparent near-miss is a virial
  tautology).  Planck frequency is listed only because hbar is NOT in S (it would be an import).
""")

# --- footing-consistent H and internal cross-checks ------------------------------------------------
H_OF = {f: Z_FRAME * A0[f] / C for f in FOOT}       # a0 = c H / Z  =>  H = Z a0 / c
LAMBDA_PLANCK = 1.1056e-52                          # m^-2, Planck 2018 TT,TE,EE+lowE+lensing
H_LAMBDA_COSMO = C * np.sqrt(LAMBDA_PLANCK / 3.0)
H0_PLANCK = 67.4e3 / MPC
OMEGA_L = 0.6847
print(f"  internal checks on the footing-consistent horizon rate H = Z a0/c:")
print(f"    canon: H = {H_OF['canon']:.4e} rad/s  vs  c sqrt(Lambda/3) = {H_LAMBDA_COSMO:.4e}"
      f"   ratio {H_OF['canon']/H_LAMBDA_COSMO:.5f}   (must be ~1: canon IS H_Lambda)")
print(f"    alt  : H = {H_OF['alt']:.4e} rad/s  vs  H_0 (Planck) = {H0_PLANCK:.4e}"
      f"   ratio {H_OF['alt']/H0_PLANCK:.5f}   (must be ~1: alt IS H_0)")
print(f"    and H_Lambda/H_0 = {H_OF['canon']/H_OF['alt']:.5f}  vs  sqrt(Omega_Lambda) ="
      f" {np.sqrt(OMEGA_L):.5f}   ratio {(H_OF['canon']/H_OF['alt'])/np.sqrt(OMEGA_L):.5f}")
assert abs(H_OF["canon"] / H_LAMBDA_COSMO - 1) < 0.01
assert abs(H_OF["alt"] / H0_PLANCK - 1) < 0.01
assert abs((H_OF["canon"] / H_OF["alt"]) / np.sqrt(OMEGA_L) - 1) < 0.01
print("    -> the two footings ARE the (H_Lambda, H_0) pair; the 21% a0 split is the 1/sqrt(Omega_L) split.")
print(f"\n  the memory time and the E10 weld (tau_mem H = 2Z, footing-free pure Z):")
for f in FOOT:
    tau_mem = 2 * C / A0[f]
    print(f"    [{f}] tau_mem = 2c/a0 = {tau_mem/GYR:.1f} Gyr = 1/(a0/2c) ;"
          f"  tau_mem * H = {tau_mem*H_OF[f]:.5f}  vs  2Z = {2*Z_FRAME:.5f}")
    assert abs(tau_mem * H_OF[f] / (2 * Z_FRAME) - 1) < 1e-9, "E10 weld failed"
print("    -> E10 verified exactly on both footings (203 / 168 Gyr), so the theory's ONE forced")
print("       memory frequency is a0/2c and nothing else in the kernel supplies a second one.")

# ==================================================================================================
# 2.  BRANCH I -- ENUMERATE EVERY INTRINSIC (CONSTANT) FREQUENCY THE THEORY SUPPLIES
# ==================================================================================================
head("2.  BRANCH I -- every intrinsic constant frequency in the written theory, vs omega_c")

def scales(f):
    a0, H = A0[f], H_OF[f]
    return [
        ("a0/(2 pi c)          dS-Unruh temp. of a0 (T_a0 in freq. units)", a0 / (2 * np.pi * C), "yes"),
        ("a0/(2c)   = 1/tau_mem   MEMORY-KERNEL EDGE, Gamma(0) (E12) -- FORCED", a0 / (2 * C), "yes"),
        ("a0/c                 kernel retardation / Compton c/a0", a0 / C, "yes"),
        ("4 a0/c               disformal B scale (grad B = 4(nu-1)g_bar/c^2 at g_bar=a0)",
         4 * a0 / C, "yes"),
        ("H_Lambda/(2 pi)      dS bath temperature T_dS", H / (2 * np.pi), "yes"),
        ("H_Lambda (canon) / H_0 (alt) = Z a0/c   dS Matsubara pole", H, "yes"),
        ("sqrt(H^2+(a0/c)^2)   off-circular pullback pole at |a| = a0 (floored at H)",
         np.hypot(H, a0 / C), "yes"),
        ("Z H                  = Z^2 a0/c   (one unmotivated factor of Z)", Z_FRAME * H, "no*"),
        ("Z^2 H                = Z^3 a0/c   (two unmotivated factors)", Z_FRAME ** 2 * H, "no*"),
        ("Z^5 H                (nearest integer power of Z below omega_c)", Z_FRAME ** 5 * H, "no*"),
        ("Z^6 H                (nearest integer power of Z above omega_c)", Z_FRAME ** 6 * H, "no*"),
        ("1/t_universe         (13.80 Gyr) -- H-family, not an action constant", 1.0 / (13.80 * GYR), "no"),
        ("Herglotz measure     branch point t=-1/4 is DIMENSIONLESS -> only builds a0/2c",
         a0 / (2 * C), "yes"),
        ("c/l_Planck           requires hbar, which is NOT in the classical action",
         C / np.sqrt(HBAR * G / C ** 3), "no"),
    ]

for f in FOOT:
    lo, hi = WIN[f]
    print(f"\n  [{f}]  a0 = {A0[f]:.4e} m/s^2 ,  H = Z a0/c = {H_OF[f]:.4e} rad/s ,"
          f"  window [{lo:.3e}, {hi:.3e}] rad/s")
    print(f"    {'intrinsic frequency':<66}{'omega [rad/s]':>14}{'dex to lo':>11}{'in S?':>7}")
    print("    " + "-" * 96)
    for name, om, ins in scales(f):
        d = np.log10(om / lo)
        tag = f"{d:+.2f}"
        print(f"    {name:<66}{om:>14.4e}{tag:>11}{ins:>7}")
    print("    * a bare factor of Z multiplying a FREQUENCY appears nowhere in S: Z enters only in "
          "a0 = cH/Z.\n      Listed to show that even the numerology route fails (below).")

# --- the two headline gaps -------------------------------------------------------------------------
print()
for f in FOOT:
    lo, hi = WIN[f]
    forced = A0[f] / (2 * C)
    nearest_named = Z_FRAME * H_OF[f]     # nearest scale even loosely nameable in the theory
    print(f"  [{f}] gap from the action's OWN FORCED corner a0/2c = {forced:.4e} to the window bottom:"
          f"  {lo/forced:.3e}x  = {np.log10(lo/forced):.2f} dex")
    print(f"        gap from the nearest UNAMBIGUOUS theory constant  H = {H_OF[f]:.4e}:"
          f"           {lo/H_OF[f]:.3e}x  = {np.log10(lo/H_OF[f]):.2f} dex")
    print(f"        gap from the nearest LOOSELY-nameable scale Z H = {nearest_named:.4e}:"
          f"        {lo/nearest_named:.3e}x  = {np.log10(lo/nearest_named):.2f} dex")
    print(f"        retained galactic boost AT the forced corner a0/2c:"
          f" Re G = {ReG(OMEGA_GAL_MAX, forced):.3e}   (RAR-DEAD)")

# --- the Z-numerology door, closed quantitatively --------------------------------------------------
print(f"\n  Z-NUMEROLOGY DOOR (checked, not waved away):  omega_c / H  requires Z^p with")
for f in FOOT:
    lo, hi = WIN[f]
    p_lo = np.log(lo / H_OF[f]) / np.log(Z_FRAME)
    p_hi = np.log(hi / H_OF[f]) / np.log(Z_FRAME)
    z5, z6 = Z_FRAME ** 5 * H_OF[f], Z_FRAME ** 6 * H_OF[f]
    print(f"    [{f}] p in [{p_lo:.3f}, {p_hi:.3f}] -- NON-INTEGER.  Z^5 H = {z5:.3e} is"
          f" {lo/z5:.3f}x BELOW the bottom; Z^6 H = {z6:.3e} is {z6/hi:.3f}x ABOVE the top.")
print("    => no integer power of Z times the horizon rate lands inside the window, on either")
print("       footing.  The cheapest numerology escape is closed too, quantitatively.")

# ==================================================================================================
# 2b.  BRANCH II -- the environmental sqrt(4 pi G rho) branch, and why its near-miss is a tautology
# ==================================================================================================
head("2b.  BRANCH II -- the environmental density frequency sqrt(4 pi G rho) (NOT a theory constant)")
def w_rho(rho): return np.sqrt(4 * np.pi * G * rho)
rho_local  = 0.10 * MSUN / PC ** 3                 # solar-neighborhood Oort dynamical density
rho_cosmic = 0.315 * 3 * H0_PLANCK ** 2 / (8 * np.pi * G)
# binding galaxy's OWN mean density inside the binding orbit (UGC05721, r=0.09 kpc, V=16.5 km/s)
r_b, v_b = 0.09 * KPC, 16.5e3
M_b   = v_b ** 2 * r_b / G
rho_b = M_b / (4.0 / 3.0 * np.pi * r_b ** 3)
lo_c = WIN["canon"][0]
print(f"""
  rho_cosmic  = {rho_cosmic:.3e} kg/m^3            -> sqrt(4 pi G rho) = {w_rho(rho_cosmic):.3e} rad/s"""
      f"  ({np.log10(lo_c/w_rho(rho_cosmic)):.2f} dex below)")
print(f"  rho_local   = {rho_local:.3e} kg/m^3 (0.1 Msun/pc^3) -> {w_rho(rho_local):.3e} rad/s"
      f"  ({np.log10(lo_c/w_rho(rho_local)):.2f} dex below, factor {lo_c/w_rho(rho_local):.1f})")
print(f"  rho_bind    = {rho_b:.3e} kg/m^3 = {rho_b/(MSUN/PC**3):.2f} Msun/pc^3 (inside the BINDING"
      f" deep-MOND orbit)\n              -> {w_rho(rho_b):.3e} rad/s"
      f"  (only factor {lo_c/w_rho(rho_b):.2f} below the window bottom)")
rho_needed = lo_c ** 2 / (4 * np.pi * G)
print(f"  density that WOULD give omega = {lo_c:.3e}: rho = {rho_needed:.3e} kg/m^3"
      f" = {rho_needed/(MSUN/PC**3):.1f} Msun/pc^3")
print(f"""
  THE NEAR-MISS IS A TAUTOLOGY, NOT A CANDIDATE.  For any virialized system omega_orb ~ sqrt(G rho)
  identically, so "sqrt(4 pi G rho_bind) sits just below 3 x omega_gal,max" is the SAME statement as
  "omega_gal,max ~ sqrt(G rho_bind)".  It supplies no independent anchor.  Concretely, a corner set
  environmentally at sqrt(4 pi G rho_bind) = {w_rho(rho_b):.3e} retains only
  Re G = {ReG(OMEGA_GAL_MAX, w_rho(rho_b)):.3f} at the binding orbit -- BELOW the theory's own {GATE_KEEP:.2f}
  requirement, i.e. the density branch fails the very condition that defines the lower edge.
  Two further disqualifications, both from the paper's own record: (i) rho is a FIELD, spanning
  {np.log10(w_rho(rho_b)/w_rho(rho_cosmic)):.1f} dex across the environments involved, so it is not a constant of the theory;
  (ii) an environment-dependent corner IS a frequency-split RAR at fixed g_bar, which the paper lists
  as falsifier (i) -- it would be a NEW prediction to be killed, not an explanation of omega_c.
""")

# ==================================================================================================
# 3.  (a) WHAT PERIOD IS omega_c, AND IS THERE ANY PROCESS THERE?
# ==================================================================================================
head("3.  (a) THE CORNER'S PERIOD, AND AN HONEST SEARCH FOR A PROCESS AT THAT TIMESCALE")
print(f"\n  {'footing/edge':<16}{'omega_c [rad/s]':>16}{'tau = 1/omega_c':>18}{'T = 2pi/omega_c':>18}")
print("  " + "-" * 70)
for f in FOOT:
    for lab, wcv in zip(("lower", "upper"), WIN[f]):
        print(f"  {f+'/'+lab:<16}{wcv:>16.4e}{1/wcv/MYR:>15.3f} Myr{2*np.pi/wcv/MYR:>15.3f} Myr")
print(f"""
  So the corner is a RELAXATION TIME tau = 1.43-1.78 Myr, i.e. an oscillation PERIOD
  T = 2 pi/omega_c = 9.0-11.2 Myr (canon) / 10.9-11.2 Myr (alt).

  CANDIDATE PROCESSES AT THAT PERIOD -- searched, each with its frequency and ratio to the bottom
  edge {WIN['canon'][0]:.3e} rad/s.  ("in S?" = is it a constant of the written theory?)""")
cands = [
    ("fastest SPARC deep-MOND orbit (UGC05721, r=0.09 kpc)", OMEGA_GAL_MAX, "no -- DEFINES the edge"),
    ("Sun's galactic orbit  Omega = V/R (233 km/s, 8.2 kpc)", 233e3 / (8.2 * KPC), "no"),
    ("Sun's epicyclic frequency  kappa ~ 1.4 Omega", 1.4 * 233e3 / (8.2 * KPC), "no"),
    ("Sun's vertical oscillation (period ~70 Myr)", 2 * np.pi / (70 * MYR), "no"),
    ("local disk dynamical  sqrt(4 pi G rho_local)", w_rho(rho_local), "no (environmental)"),
    ("spiral-arm crossing (period ~150 Myr)", 2 * np.pi / (150 * MYR), "no"),
    ("Saturn's orbit (the Cassini/ephemeris frequency)", 2 * np.pi / (29.4571 * YR), "no"),
    ("Moon's orbit (the LLR frequency)", 2 * np.pi / (27.3217 * 86400), "no"),
    ("1/age of universe (13.8 Gyr)", 1.0 / (13.80 * GYR), "no"),
    ("H_Lambda (the theory's ONLY constant frequency family)", H_OF["canon"], "YES"),
]
print(f"\n    {'process':<56}{'omega [rad/s]':>14}{'dex to lo':>11}   in S?")
print("    " + "-" * 98)
for nm, om, ins in cands:
    print(f"    {nm:<56}{om:>14.4e}{np.log10(om/WIN['canon'][0]):>+11.2f}   {ins}")
# cosmological epoch whose age equals the corner period (matter-dominated estimate)
t_corner = 2 * np.pi / WIN["canon"][0]
Om = 0.315
zp1 = (2.0 / (3.0 * H0_PLANCK * np.sqrt(Om) * t_corner)) ** (2.0 / 3.0)
print(f"""
    cosmological epoch whose AGE equals the corner period ({t_corner/MYR:.1f} Myr): z ~ {zp1-1:.0f}
    -- between recombination (z=1090) and reionization (z~8), an epoch with no role in the theory
    and no feature in it.  Nothing selects it.

  HONEST RESULT (a):  NOTHING matches.  The only entries within one order of magnitude of omega_c are
  galactic / dwarf orbital-dynamical frequencies -- and those are precisely the quantity the LOWER
  EDGE WAS DEFINED FROM (omega_c >= 3 omega_gal,max).  "omega_c ~ 3 x the fastest galaxy orbit" is the
  constraint restated, not an explanation: it contains the arbitrary retention threshold {GATE_KEEP}
  (Section 5) and would move with any new dwarf.  The nearest thing in the solar system, Saturn's
  orbit, is {np.log10(2*np.pi/(29.4571*YR)/WIN['canon'][0]):.1f} dex ABOVE; the theory's own H_Lambda is 4.0 dex BELOW.  There is a clean,
  empty ~3-dex desert on both sides of omega_c, and the theory has nothing in it.
""")

# ==================================================================================================
# 4.  (b) FINE-TUNING, QUANTIFIED
# ==================================================================================================
head("4.  (b) FINE-TUNING -- log-prior fraction of the surviving window")
w_planck = C / np.sqrt(HBAR * G / C ** 3)
print(f"\n  window width in dex:", end="")
for f in FOOT:
    lo, hi = WIN[f]
    print(f"   {f} = {np.log10(hi/lo):.4f} dex (x{hi/lo:.3f})", end="")
print()
for f in FOOT:
    lo, hi = WIN[f]
    gm, hw = np.sqrt(lo * hi), np.sqrt(hi / lo) - 1
    print(f"    {f}: omega_c must be specified as ({gm:.4e}) x (1 +/- {hw:.1%})")

priors = [
    ("P1  theory->observation: [a0/2c (the action's forced corner), the LLR ceiling]",
     lambda f: (A0[f] / (2 * C), WIN[f][1])),
    ("P2  IR->UV: [a0/2c, c/l_Planck]  (needs hbar, which is NOT in the classical action)",
     lambda f: (A0[f] / (2 * C), w_planck)),
    ("P3  dynamically probed: [omega_gal,max (slowest probe), omega_Mercury (fastest probe)]",
     lambda f: (OMEGA_GAL_MAX, 2 * np.pi / (87.969 * 86400))),
]
print(f"\n  {'log-uniform (Jeffreys) prior on omega_c':<74}{'span':>9}{'canon':>9}{'alt':>9}")
print("  " + "-" * 101)
for nm, rng in priors:
    fr = {}
    for f in FOOT:
        a, b = rng(f)
        span = np.log10(b / a)
        fr[f] = (np.log10(WIN[f][1] / WIN[f][0]) / span, span)
    print(f"  {nm:<74}{fr['canon'][1]:>7.2f}dx{fr['canon'][0]:>8.3%}{fr['alt'][0]:>9.3%}")
print(f"""
  THE SCALE-FREE STATEMENT (the sharpest honest form):  the classical action supplies NO ultraviolet
  frequency at all (Section 1: no hbar, and G cannot make a frequency without a density).  On a
  genuinely scale-free log-uniform prior over omega_c in (0, infinity) the surviving window therefore
  has measure ZERO -- every finite fraction quoted above requires a cutoff IMPORTED BY HAND (P2
  imports hbar; P1 and P3 import the observations themselves).  P1 is the most favourable framing
  available to the theory, and even it gives {np.log10(WIN['canon'][1]/WIN['canon'][0])/np.log10(WIN['canon'][1]/(A0['canon']/(2*C))):.2%} (canon) / """
      f"""{np.log10(WIN['alt'][1]/WIN['alt'][0])/np.log10(WIN['alt'][1]/(A0['alt']/(2*C))):.2%} (alt).

  THE SANDWICH, stated plainly:
      from BELOW   omega_c >= 3 omega_gal,max = {WIN['canon'][0]:.3e}   -- a PHENOMENOLOGICAL requirement
                   (the gate must not switch off the rotation curves the framework exists to explain);
                   THEORY-INTERNAL and NON-NEGOTIABLE: it cannot be relaxed without breaking the
                   framework's core success.  It is also footing-independent.
      from ABOVE   omega_c <= {WIN['canon'][1]:.3e} (canon) / {WIN['alt'][1]:.3e} (alt) -- an OBSERVATIONAL
                   bound (LLR Gdot/G), the only edge that moves with better data, and it moves DOWN.
      in BETWEEN   NOTHING.  No constant of the theory lies within {np.log10(WIN['canon'][0]/(Z_FRAME*H_OF['canon'])):.1f} dex (and no unambiguous
                   one within {np.log10(WIN['canon'][0]/H_OF['canon']):.1f} dex) of the window; the action's own forced corner is
                   {np.log10(WIN['canon'][0]/(A0['canon']/(2*C))):.2f} dex below it and RAR-dead.
  ASYMMETRY:  all improvement pressure therefore closes the window from ABOVE.  A free constant
  squeezed between a non-negotiable theory-internal floor and a monotonically improving observational
  ceiling is a genuinely precarious configuration -- it is also, and equally honestly, TWO-SIDEDLY
  FALSIFIABLE, which is a virtue.  Both halves of that are the record.
""")

# ==================================================================================================
# 5.  THRESHOLD SENSITIVITY OF THE NON-NEGOTIABLE LOWER EDGE
# ==================================================================================================
head("5.  HOW MUCH OF THE WINDOW IS THE ARBITRARY RETENTION THRESHOLD?  (lower-edge sensitivity)")
print(f"\n  The lower edge is  omega_c >= omega_gal,max / sqrt(1/S_keep - 1)  with S_keep chosen = {GATE_KEEP}.")
print(f"  S_keep is a MODELLING CHOICE, not a measurement.  Its effect on the window:\n")
print(f"    {'S_keep':>8}{'k':>8}{'lower edge':>14}{'width canon':>14}{'width alt':>12}"
      f"{'dex cost in g_obs':>19}")
print("    " + "-" * 78)
for S in (0.80, 0.85, 0.90, 0.95, 0.99):
    k = 1.0 / np.sqrt(1.0 / S - 1.0)
    lo = OMEGA_GAL_MAX * k
    wc_, wa_ = WIN["canon"][1] / lo, WIN["alt"][1] / lo
    dex = -0.5 * np.log10(S)                       # deep-MOND: g_obs ~ sqrt(a0 g_bar S)
    print(f"    {S:>8.2f}{k:>8.3f}{lo:>14.4e}"
          f"{('x%.3f' % wc_) if wc_>1 else 'CLOSED':>14}{('x%.3f' % wa_) if wa_>1 else 'CLOSED':>12}"
          f"{dex:>18.4f}")
print(f"""
  Read carefully, both ways:
    * Requiring only 80% retention widens the window to x{WIN['canon'][1]/(OMEGA_GAL_MAX*2.0):.2f} (canon) /"""
      f""" x{WIN['alt'][1]/(OMEGA_GAL_MAX*2.0):.2f} (alt).
    * Requiring 95% retention CLOSES the window on BOTH footings.  The window's existence is therefore
      contingent on tolerating a 10% suppression of the MOND term at the binding innermost orbit.
    * The price of that 10% is small but not zero: in deep MOND g_obs ~ sqrt(a0 g_bar S), so
      S = 0.90 costs {-0.5*np.log10(0.90):.4f} dex at that point, ~{(-0.5*np.log10(0.90))/0.108:.0%} of the framework's own 0.108-dex RAR
      scatter -- at ONE point of ONE galaxy.  Across the canonical window the retention at that orbit
      runs {ReG(OMEGA_GAL_MAX, WIN['canon'][0]):.3f}-{ReG(OMEGA_GAL_MAX, WIN['canon'][1]):.3f}.
    * This is NOT an exclusion and is NOT presented as one: no observation fixes S_keep.  It is the
      honest statement that a stricter reading of the framework's OWN core requirement closes its own
      solar-system window, and a looser one opens it -- so part of the quoted 24% is threshold choice.
""")

# ==================================================================================================
# 6.  VERDICT (W-4 lane only)
# ==================================================================================================
head("6.  VERDICT -- W-4 NATURALNESS")
lo_c, hi_c = WIN["canon"]; lo_a, hi_a = WIN["alt"]
print(f"""
  1. CLOSED CENSUS, not a survey: the classical MI action's dimensionful content is {{c, G, Lambda}}
     plus the FIELD rho_m.  Every constant frequency it can build is (pure number) x H_Lambda; the
     only other branch is the environmental sqrt(G rho).  There is no third place for omega_c to hide.

  2. NEAREST INTRINSIC SCALE, both footings:
       action's OWN FORCED corner  a0/2c = {A0['canon']/(2*C):.3e} (canon) / {A0['alt']/(2*C):.3e} (alt)
           -> {np.log10(lo_c/(A0['canon']/(2*C))):.2f} / {np.log10(lo_a/(A0['alt']/(2*C))):.2f} dex BELOW the window (factor {lo_c/(A0['canon']/(2*C)):.2e} / {lo_a/(A0['alt']/(2*C)):.2e}), and RAR-DEAD
           (retained boost {ReG(OMEGA_GAL_MAX, A0['canon']/(2*C)):.2e}).
       nearest UNAMBIGUOUS constant  H = {H_OF['canon']:.3e} / {H_OF['alt']:.3e}
           -> {np.log10(lo_c/H_OF['canon']):.2f} / {np.log10(lo_a/H_OF['alt']):.2f} dex below.
       nearest LOOSELY-nameable  Z H = {Z_FRAME*H_OF['canon']:.3e} / {Z_FRAME*H_OF['alt']:.3e}
           -> {np.log10(lo_c/(Z_FRAME*H_OF['canon'])):.2f} / {np.log10(lo_a/(Z_FRAME*H_OF['alt'])):.2f} dex below (and a bare Z on a frequency is in no term of S).
     ==> the nearest intrinsic scale is 3.2 dex below on the most generous reading, 3.9-4.0 dex on the
         defensible one, and 5.06/4.99 dex for the corner the action actually FORCES.  Plainly: NO
         intrinsic scale sits near 1e-14 rad/s.

  3. NO integer power of Z times H lands in the window (p = 5.24 required; Z^5 is 1.52x low, Z^6 is
     3.07x high, canon).  The numerology escape is closed quantitatively, not by assertion.

  4. PERIOD: tau = 1/omega_c = 1.43-1.78 Myr, T = 2 pi/omega_c = 9.0-11.2 Myr.  No process in the
     theory and none in the solar system sits there.  The only nearby frequencies are galactic /
     dwarf orbital ones -- i.e. the lower edge's own definition.  Nothing anchors it.

  5. FINE-TUNING: window = {np.log10(hi_c/lo_c):.4f} dex canon (+/-{np.sqrt(hi_c/lo_c)-1:.1%}) / {np.log10(hi_a/lo_a):.4f} dex alt (+/-{np.sqrt(hi_a/lo_a)-1:.1%}).
     Log-prior fraction: {np.log10(hi_c/lo_c)/np.log10(hi_c/(A0['canon']/(2*C))):.2%} (canon) / {np.log10(hi_a/lo_a)/np.log10(hi_a/(A0['alt']/(2*C))):.2%} (alt) of the 5-dex span between the theory's own
     corner and the LLR ceiling; {np.log10(hi_c/lo_c)/np.log10(w_planck/(A0['canon']/(2*C))):.3%} / {np.log10(hi_a/lo_a)/np.log10(w_planck/(A0['alt']/(2*C))):.3%} of the a0-to-Planck span; and formally ZERO on
     a scale-free prior, because the classical action has no UV frequency to normalise against.

  6. HONEST SUMMARY: omega_c is anchored by NOTHING in the theory.  It is sandwiched purely by
     observation -- just above the fastest confirmed deep-MOND galaxy orbit (a non-negotiable
     theory-internal requirement) and just below LLR (an observational bound that only improves).
     This is a PREDICTIVITY deficit, stated as the paper itself states it: five constants, none
     derived.  It is not an anthropic coincidence and it is not a falsification; it is the honest
     cost of the solar-system save, and it is two-sidedly falsifiable, which is a virtue.
     NOT claimed: that the alt footing is excluded, that the window is comfortable, or that any door
     is closed.  Lane: W-4 only.
""")
print(RULE)
print("mi_omegac_naturalness_2026.py: window regression <0.5% vs mi_cassini_q2_omegac_2026.py; all asserts passed.")
print(RULE)
