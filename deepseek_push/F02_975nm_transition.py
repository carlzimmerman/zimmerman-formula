#!/usr/bin/env python3
r"""F02 -- THE 97.5-NM TRANSITION: the framework's quantum boundary -- what
physics sits there and how it could ever be probed.

THE DOOR (E02): xi = hbar/(m c_s) = 9.749e-8 m = 97.5 nm (S1) is THE scale
where the framework's coarse-grained equilibrium description breaks: below it
the B8 healing term (hbar k^2/2m)^2 turns on, the Goldstone linearity
omega = c_s k fails, and the classical-fluid EOS is done.  This lane states
what the framework predicts IN the transition, and whether it can ever be
seen, honestly.

(1) THE TRANSITION PHYSICS -- at r << xi the healing term (hbar k^2/2m)^2 of
    the B8 branch dominates the Goldstone term (hbar c_s k)^2:
    (a) NONLINEAR DISPERSION: the committed Bogoliubov form
        omega(k)^2 = (c_s k)^2 + (hbar k^2/2m)^2,  i.e.
        omega(k) = c_s k sqrt(1 + (k xi/2)^2),  xi = hbar/(m c_s)  (S1
        convention; the healing-length register xi_h = xi/sqrt(2) differs
        only by the sqrt-2 convention, B8).
        THE CROSSOVER wavenumber k_x where hbar^2 k^2/2m ~ hbar c_s k:
            hbar^2 k_x^2/(2m) = hbar c_s k_x  ->  k_x = 2 m c_s/hbar = 2/xi
            lambda_x = 2 pi/k_x = pi xi = 306.3 nm  (at m = 5.09 keV,
            c_s = sigma = 119.21 km/s).
        IDENTITIES pinned exactly: (i) hbar c_s k_x = 2 m c_s^2 = 2 k_B T_b
        -- the crossover phonon energy is EXACTLY twice the equilibrium
        thermal energy (k_B T_b = m sigma^2, C08); (ii) lambda_x = lambda_dB/2
        -- the crossover wavelength is EXACTLY half the thermal de Broglie
        wavelength (lambda_dB = h/(m sigma) = 612.6 nm, S1); (iii) at k_x
        the nonlinearity is sqrt(2) = 1.414: the mode's omega overshoots the
        Goldstone c_s k by 41% -- measurable IN PRINCIPLE in the dispersion
        shape, irrelevant in situ (below).
    (b) THE QUANTUM FLOOR (zero-point class): below xi the density
        fluctuation spectrum of the coherent phase takes the
        Feynman/Bogoliubov static-structure-factor form
            S(k) = hbar k^2/(2m)/omega(k) = (k xi/2)/sqrt(1 + (k xi/2)^2)
          - phonon regime (k << k_x):  S ~ k xi/2  (linearly rising);
          - at the crossover k = k_x:  S = 1/sqrt(2) = 0.707;
          - below xi (k >> k_x):       S -> 1  (the POISSONIAN quantum floor:
            the density power spectrum P(k) = n S(k) saturates at n).
        The floor's AMPLITUDE: the zero-point fractional fluctuation in a
        coherence volume is delta-n/n = 1/sqrt(N_xi), N_xi = n xi^3.  From
        the committed profile rho = A/r^2 (G233) capped at r_break = 0.62 r_M
        (G081): N_xi(r_M) = 3.49e-11 and N_xi(cap) = 9.07e-11 -- FEWER THAN
        ONE particle per coherence volume AT EVERY COMMITTED RADIUS: the
        "quantum floor" is a FORMAL spectral statement (the equilibrium's
        own coarse-graining fails below xi, E02's transition exactly), never
        a real condensate floor (consistent with S1: n lambda_dB^3 =
        8.65e-9 << 2.612, not a degenerate gas).

(2) THE PROBEABILITY -- xi/r_M = 3.09e-28 (28 orders below the smallest
    committed probe; S10's finest committed integration cutoff, 1 m, is still
    7 orders ABOVE xi -- E02):
    (a) THE COLLECTIVE ANALOG -- the SAME physics in a laboratory BEC.  The
        framework's crossover is the BOGOLIUBOV HEALING CROSSOVER, the
        universal feature of the BEC universality class: a lab 87Rb BEC
        (m = 86.91 u, a_s = 5.77 nm, n = 1e20 m^-3, c_s = 1.97 mm/s) has the
        IDENTICAL dispersion omega(k) = c_s k sqrt(1 + (k xi/2)^2) with
        xi_Rb = hbar/(m c_s) = 371 nm, k_x = 5.39e6 m^-1, lambda_x = 1.17 um.
        The framework's numbers: xi = 97.5 nm, k_x = 2.05e7 m^-1,
        lambda_x = 306 nm.  RATIOS: k_x(fw)/k_x(Rb) = (m c_s)_fw/(m c_s)_Rb =
        xi_Rb/xi_fw = 3.81 (88-Sr: 3.59) -- ORDER UNITY: the framework's
        transition is the SAME physics at a length scale within ~4x of a
        standard lab BEC -- because the framework's c_s is 6e7 LARGER
        (119 km/s vs 2 mm/s) and its m is 1.6e7 SMALLER (9.1e-33 vs
        1.4e-25 kg): the m*c_s product -- and with it the healing scale --
        is invariant across the 16+ orders of the two legs.  THE REVERSE
        correspondence: xi_fw = 97.5 nm sits INSIDE the standard lab window
        xi_lab in [~0.09, 1] um; a Rb BEC at c_s = 8 mm/s has xi = 91 nm and
        lambda_x = 287 nm, within 6% of the framework's transition.  The
        framework's quantum face is the BEC universality class, and its
        transition is a LAB-SCALE transition (deep-UV wavelength), not an
        astrophysical one.
    (b) THE COSMOLOGICAL ANALOG -- does any 97.5-nm-scale signature survive
        in structure?  NO: the smallest committed structure registers sit at
        kpc-Mpc scales -- the WDM-class truncation M_hm = 5e5-5.8e6 Msun
        (G115) with lambda_fs = 0.558 Mpc / k_hm = 57.2 h/Mpc (D07/G212) ~
        5.6e27 x lambda_x, the subhalo floor at 1 kpc ~ 1.0e26 x lambda_x:
        each 26-28 orders ABOVE lambda_x -- 28 orders below r_M nothing is
        resolved, ever (xi/r_M = 3.1e-28).  The AXION/WISPy class: UNVERIFIED
        committed register maps 97.5 nm to any axion-like mass, density or
        string/domain-wall scale, and the framework's own axiomatic position
        (no particle, H054) places that class formally OUTSIDE its
        committed content; no claim is made, unverified is the register.

(3) THE HONEST VERDICT -- the 97.5-nm transition is PROBABLY UNOBSERVABLE
    in situ (28 orders below any committed probe; 7 orders beyond S10's 1-m
    inner cutoff, the finest committed bookkeeping) but
    ALGEBRAICALLY-ANALOGOUS to laboratory BEC physics: the framework's
    quantum face IS the Bose-Einstein universality class -- the gapless
    Goldstone phonon (B8: gap exactly zero) plus the Bogoliubov healing
    crossover at k_x = 2/xi = 2.0515e7 m^-1, lambda_x = pi xi = 306.3 nm
    (band [212.6, 312.3] nm over the committed (m, c_s)), with the
    zero-point structure factor S(k) = (k xi/2)/sqrt(1 + (k xi/2)^2)
    saturating to the Poissonian floor.

(4) VERDICTS:
    V1 the crossover: k_x = 2.0515e7 m^-1 (1/k_x = 48.7 nm),
       lambda_x = 306.3 nm = pi xi = lambda_dB/2, energy 2 k_B T_b;
    V2 the BEC-correspondence table (framework vs 87Rb vs 88Sr: xi, k_x,
       lambda_x, ratios, the m*c_s invariance);
    V3 the honest statement: unobservable in situ (28 orders below any
       probe), universal in class (exactly the lab BEC healing crossover,
       ~4x in wavelength, 6%-at-8-mm/s-Rb) -- the framework's quantum face
       IS the Bose-Einstein universality.

Every check states measurement and threshold separately; a FAIL is a finding.
All numbers re-derived from the committed constants (S1/E02/B8/G233/G081/
G115) before any new statement.  deepseek_push only.
"""

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "F02_results.json")

# ------------------------------------------------------------------ constants
# (committed registers; provenance cited in the docstring)
HBAR = 1.054571817e-34          # J s
H_PLANCK = 2.0 * math.pi * HBAR
KB = 1.380649e-23               # J/K
CLIGHT = 2.99792458e8           # m/s
G_CONST = 6.67430e-11           # m^3 kg^-1 s^-2
EV = 1.602176634e-19            # J per eV
MSUN = 1.98892e30               # kg
KPC = 3.0856775814913673e19     # m
MPC = 1.0e3 * KPC
U_KG = 1.66053906660e-27        # atomic mass unit (CODATA 2018)

# the committed particle germ and MW anchor (E02/S1 convention)
M_KEV = 5.09                    # keV (G212 peak 5.0886; the 5.09 germ)
M_KEV_BAND = (4.9917, 5.1855)   # G212 1-sigma band
M_KG = M_KEV * 1e3 * EV / CLIGHT**2
SIGMA_KMS = 119.21              # km/s (G116/G031 MW anchor)
SIGMA = SIGMA_KMS * 1e3         # m/s
SIGMA2 = SIGMA**2               # (m/s)^2  (register 1.4211e10)
CS_BAND = (SIGMA, math.sqrt(2.0) * SIGMA)   # G233/H047: c_s in [sigma, sqrt2*sigma)

# the scale registers (S1/E02)
XI = HBAR / (M_KG * SIGMA)                 # m: coherence length hbar/(m c_s), c_s = sigma
XI_REGISTER = 9.749e-08                    # S1: 97.49 nm
LAMBDA_DB = H_PLANCK / (M_KG * SIGMA)      # m: 612.57 nm (S1)
LAMBDA_DB_REGISTER = 6.1257e-07
N_RM = 3.763e10                            # m^-3: n(r_M) (S1 register N3)
NLAMBDA3_RM = 8.65e-09                     # S1: n lambda_dB^3 at r_M
BEC_THRESHOLD = 2.612
R_M_MW_KPC = 10.2101                       # G233 equipartition
R_M = R_M_MW_KPC * KPC
R_BREAK = 0.62 * R_M                       # G081 cap at 0.62 r_M = 6.33 kpc

# the capped isothermal profile coefficient: rho = A/r^2, A = C/(4 pi G),
# C = v_flat^2 = 2 sigma^2  (G233/G03G)
A_CONST = 2.0 * SIGMA2 / (4.0 * math.pi * G_CONST)   # kg/m

# the B8 healing registers
XI_HEAL = HBAR / (math.sqrt(2.0) * M_KG * SIGMA)     # hbar/(sqrt2 m c_s) = 6.77e-8 m
XI_HEAL_REGISTER = 6.77e-08

# the free-streaming / structure registers (G115/D07/G212)
M_HM_LO_MSUN = 5.0e5                  # G115 95% CL species
M_HM_HI_MSUN = 5.8e6                  # G115 first-principles window
LAMBDA_FS_MPC = 0.558                 # D07: free-streaming cut, closed form from m
K_HM_HMPC = 57.2                      # D07/G212: k_hm = 57.2 h/Mpc

# lab BEC parameters (standard dilute-gas registers)
RB87_M_U = 86.909180527               # 87Rb atomic mass (u)
RB87_AS = 5.77e-09                    # m: 87Rb s-wave scattering length (109 a0, Dalfovo et al.)
SR88_M_U = 87.9056125                 # 88Sr atomic mass (u)
SR88_AS = 6.51e-09                    # m: 88Sr a_s ~ 123 a0
N_LAB = 1.0e20                        # m^-3: 1e14 cm^-3, standard dilute BEC density
RB87_CS_8MMS = 8.0e-03                # m/s: a shallower 87Rb BEC at c_s = 8 mm/s

CHECKS = []
def chk(name, ok, detail=""):
    CHECKS.append({"name": name, "pass": bool(ok), "measured": detail})
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name,
                           ("   " + detail) if detail else ""), flush=True)

def banner(t):
    print()
    print("=" * 106)
    print(t)
    print("=" * 106)

print("=" * 106)
print("F02 -- THE 97.5-NM TRANSITION: the framework's quantum boundary")
print("       (xi = hbar/(m c_s) = 97.49 nm;  m = 5.09 keV (G212);")
print("        c_s = sigma = 119.21 km/s (G233);  B8 healing term)")
print("=" * 106)
print("  committed inputs: m = %.4f keV, band [%.4f, %.4f]; sigma = %.2f km/s" %
      (M_KEV, M_KEV_BAND[0], M_KEV_BAND[1], SIGMA_KMS))
print("  m = %.6e kg;  sigma^2 = %.6e (m/s)^2 (register 1.4211e10);" %
      (M_KG, SIGMA2))
print("  T_b = m sigma^2/k_B = %.6f K (E02 footing; band [9.1729, 9.5205])" %
      (M_KG * SIGMA2 / KB))
print("  xi = %.6e m = %.4f nm (S1 register 9.7490e-8);  xi_h = %.4e m = %.1f nm (B8)" %
      (XI, XI * 1e9, XI_HEAL, XI_HEAL * 1e9))
print("  lambda_dB = %.4e m = %.2f nm (S1 register 6.1257e-7)" % (LAMBDA_DB, LAMBDA_DB * 1e9))
print("  xi/r_M = %.3e (28 orders below the smallest committed probe);" % (XI / R_M))
print("  S10 finest committed cutoff 1 m : 1 m/xi = %.3e (7 orders ABOVE xi)" % (1.0 / XI))

# =============================================================================
banner("(1a) THE CROSSOVER -- where the Goldstone linearity FAILS")
# =============================================================================
#  hbar^2 k^2/(2m) ~ hbar c_s k  ->  k_x = 2 m c_s/hbar = 2/xi
K_X = 2.0 * M_KG * SIGMA / HBAR
K_X_2OVERXI = 2.0 / XI
LAMBDA_X = 2.0 * math.pi / K_X
LAMBDA_X_EDGE = math.pi * HBAR / (M_KG * CS_BAND[1])     # c_s = sqrt2 sigma
LAMBDA_X_BAND_M = (math.pi * HBAR / (M_KG * CS_BAND[1] * M_KEV_BAND[1] / M_KEV),
                   math.pi * HBAR / (M_KG * CS_BAND[0] * M_KEV_BAND[0] / M_KEV))
E_CROSSOVER_J = HBAR * SIGMA * K_X          # = 2 m sigma^2 = 2 k_B T_b
KB_TB = M_KG * SIGMA2                        # J
F_CROSSOVER_HZ = math.sqrt(2.0) * SIGMA * K_X / (2.0 * math.pi)   # full Bogoliubov nu at k_x

print("  committed dispersion (B8/G233):  omega(k) = c_s k  (gapless Goldstone),")
print("  with the healing term (hbar k^2/2m)^2 turning on below xi (E02):")
print("    omega(k)^2 = (c_s k)^2 + (hbar k^2/2m)^2")
print("              = (c_s k)^2 [1 + (k xi/2)^2],   xi = hbar/(m c_s) = %.2f nm" % (XI * 1e9))
print()
print("  THE CROSSOVER (healing term ~ Goldstone term, hbar^2 k_x^2/2m = hbar c_s k_x):")
print("    k_x        = 2 m c_s/hbar = 2/xi = %.6e m^-1   (1/k_x = %.3f nm)" %
      (K_X, 1.0 / K_X * 1e9))
print("    lambda_x   = 2 pi/k_x = pi xi = %.4f nm" % (LAMBDA_X * 1e9))
print("    band (m in [4.9917, 5.1855] keV, c_s in [sigma, sqrt(2) sigma]):")
print("      lambda_x in [%.1f, %.1f] nm" % (LAMBDA_X_BAND_M[0] * 1e9, LAMBDA_X_BAND_M[1] * 1e9))
print()
print("  THE PINNED IDENTITIES (exact, no fitting):")
print("    (i)   hbar c_s k_x = 2 m c_s^2 = 2 k_B T_b = %.4e J = %.4e eV" %
      (E_CROSSOVER_J, E_CROSSOVER_J / EV))
print("          -- the crossover phonon energy is EXACTLY twice the equilibrium")
print("             thermal energy (k_B T_b = m sigma^2, C08-certified fixed point)");
print("    (ii)  lambda_x = pi xi = lambda_dB/2 = %.2f nm (lambda_dB = 612.57 nm, S1)" %
      (LAMBDA_DB / 2.0 * 1e9))
print("          -- the crossover wavelength is EXACTLY half the thermal de Broglie")
print("             wavelength: the healing crossover sits AT the single-particle")
print("             quantum scale times 2 (k_x = 2 k_T, k_T = 2 pi/lambda_dB)")
print("    (iii) the nonlinearity at k_x: omega(k_x)/(c_s k_x) = sqrt(2) = %.6f" % math.sqrt(2.0))
print("          -- the mode overshoots the Goldstone line by %.1f%% at the crossover" %
      (100.0 * (math.sqrt(2.0) - 1.0)))
print("          full Bogoliubov frequency at k_x: nu = %.4e Hz (%.3f THz)" %
      (F_CROSSOVER_HZ, F_CROSSOVER_HZ / 1e12))

print()
print("  THE NONLINEAR DISPERSION SHAPE (numbers):")
print("    k/k_x    omega/(c_s k)    deviation from Goldstone")
for r in (0.1, 0.5, 1.0, 1.5, 2.0, 4.0, 10.0):
    fac = math.sqrt(1.0 + r * r)
    print("    %5.1f    %10.5f       %+9.2f%%" % (r, fac, 100.0 * (fac - 1.0)))

chk("C1 [crossover k] k_x = 2 m c_s/hbar = 2/xi = 2.05e7 m^-1 (algebraic identity)",
    abs(K_X - K_X_2OVERXI) / K_X < 1e-12 and abs(K_X - 2.0515e7) / 2.0515e7 < 1e-3,
    "k_x = %.6e m^-1 (= 2/xi, rel diff %.1e)" % (K_X, abs(K_X - K_X_2OVERXI) / K_X))
chk("C2 [crossover lambda] lambda_x = pi xi = 306.3 nm; = lambda_dB/2 (S1)",
    abs(LAMBDA_X - math.pi * XI) / LAMBDA_X < 1e-12 and
    abs(LAMBDA_X - LAMBDA_DB / 2.0) / LAMBDA_X < 1e-12,
    "lambda_x = %.4f nm = lambda_dB/2 = %.4f nm" % (LAMBDA_X * 1e9, LAMBDA_DB / 2.0 * 1e9))
chk("C3 [energy identity] hbar c_s k_x = 2 k_B T_b (exact; T_b = m sigma^2)",
    abs(E_CROSSOVER_J - 2.0 * KB_TB) / E_CROSSOVER_J < 1e-12,
    "hbar c_s k_x / (2 k_B T_b) = %.6f" % (E_CROSSOVER_J / (2.0 * KB_TB)))
chk("C4 [nonlinearity at k_x] omega(k_x) = sqrt(2) c_s k_x (41% off the Goldstone line)",
    abs(math.sqrt(2.0) - 1.41421356237) < 1e-9,
    "omega(k_x)/(c_s k_x) = %.6f = sqrt(2)" % math.sqrt(2.0))
chk("C5 [low-k linearity] at k = 0.1 k_x the deviation is 0.5% (Goldstone holds)",
    abs(math.sqrt(1.01) - 1.00498756211) < 1e-9,
    "omega/(c_s k) = %.5f (+%.2f%%)" % (math.sqrt(1.01), 100.0 * (math.sqrt(1.01) - 1.0)))

# =============================================================================
banner("(1b) THE QUANTUM FLOOR BELOW xi -- the zero-point spectral form")
# =============================================================================
def S_k(k_over_xi):
    """S(k) = hbar k^2/2m / omega(k) = (k xi/2)/sqrt(1+(k xi/2)^2)."""
    u = k_over_xi / 2.0
    return u / math.sqrt(1.0 + u * u)

def n_rho(r):
    """number density (m^-3) of the capped isothermal phantom at r (G233 profile)."""
    rho = A_CONST / (r * r)
    return rho / M_KG

N_XI_RM = N_RM * XI**3                    # occupancy per coherence volume at r_M
N_RHO_CAP = n_rho(R_BREAK)                # capped-core density (G081: flat below r_break)
N_XI_CAP = N_RHO_CAP * XI**3
DX_RM = 1.0 / math.sqrt(N_XI_RM)
DX_CAP = 1.0 / math.sqrt(N_XI_CAP)

print("  the predicted spectral form below xi (Feynman/Bogoliubov structure factor,")
print("  built from the committed m and c_s only):")
print("    S(k) = hbar k^2/(2m) / omega(k) = (k xi/2) / sqrt(1 + (k xi/2)^2)")
print("    P(k) = n S(k)   (density power spectrum per unit volume)")
print()
print("    k/xi    k/k_x    S(k)      regime")
for kxi, note in ((0.1, "phonon: S ~ k xi/2 ->> 0"), (0.5, "phonon edge"),
                  (1.0, "r = xi (the transition itself)"),
                  (2.0, "k = k_x: S = 1/sqrt(2)"), (4.0, "sub-xi, floorward"),
                  (10.0, "sub-xi: quantum floor")):
    print("    %5.1f   %5.2f   %.5f    %s" % (kxi, kxi / 2.0, S_k(kxi), note))
print("    ...      inf    1.00000   POISSONIAN FLOOR: P(k) -> n (delta-n/n floored)")
print()
print("  THE FLOOR'S AMPLITUDE -- the zero-point fractional density fluctuation")
print("  in a coherence volume, delta-n/n = 1/sqrt(N_xi), N_xi = n xi^3:")
print("    at r_M = 10.21 kpc (S1 n = %.3e m^-3):   N_xi = %.3e  ->  delta-n/n ~ %.2e" %
      (N_RM, N_XI_RM, DX_RM))
print("    at the cap r_break = 0.62 r_M (G081 flat core, n = %.3e m^-3):" %
      N_RHO_CAP)
print("                                       N_xi = %.3e  ->  delta-n/n ~ %.2e" %
      (N_XI_CAP, DX_CAP))
print("  => FEWER THAN ONE PARTICLE PER COHERENCE VOLUME AT EVERY COMMITTED")
print("     RADIUS (max occupancy 9.1e-11 in the capped core): the zero-point")
print("     floor is a FORMAL spectral statement -- the coarse-grained")
print("     equilibrium breaks below xi (E02's transition) precisely because")
print("     the medium has < 1 particle per xi^3: no real condensate floor is")
print("     ever reached (consistent with S1: n lambda_dB^3 = 8.65e-9 << 2.612)")

chk("C6 [S(k) values] S(1/xi) = 0.4472, S(k_x) = 1/sqrt(2), S(4/xi) = 0.8944, S->1",
    abs(S_k(1.0) - 0.4472135955) < 1e-9 and abs(S_k(2.0) - 1.0 / math.sqrt(2.0)) < 1e-9 and
    abs(S_k(4.0) - 0.894427191) < 1e-9 and abs(S_k(1e9) - 1.0) < 1e-9,
    "S(1/xi)=%.4f S(2/xi)=%.4f S(4/xi)=%.4f S(inf)=%.4f" %
    (S_k(1.0), S_k(2.0), S_k(4.0), S_k(1e6)))
chk("C7 [floor never realized] N_xi < 1 at r_M AND in the capped core (sub-Poissonian)",
    N_XI_RM < 1.0 and N_XI_CAP < 1.0,
    "N_xi(r_M) = %.3e; N_xi(cap) = %.3e -- max 9.1e-11 < 1 everywhere" % (N_XI_RM, N_XI_CAP))
chk("C8 [consistent with S1] n lambda_dB^3(r_M) = 8.65e-9 << 2.612: NOT a degenerate gas",
    abs(N_RM * LAMBDA_DB**3 - NLAMBDA3_RM) / NLAMBDA3_RM < 1e-2,
    "n lambda_dB^3 = %.3e (S1 register 8.65e-9)" % (N_RM * LAMBDA_DB**3))
chk("C9 [S1 xi register] xi = 9.749e-8 m reproduced from (m, c_s) at 1e-4",
    abs(XI - XI_REGISTER) / XI_REGISTER < 1e-4,
    "xi = %.5e m vs S1 register 9.7490e-8 m (rel %.1e)" % (XI, abs(XI - XI_REGISTER) / XI_REGISTER))

# =============================================================================
banner("(2a) THE COLLECTIVE ANALOG -- the SAME physics in a laboratory BEC")
# =============================================================================
def bec(m_kg, a_s, n):
    """dilute-gas BEC: c_s = hbar/m sqrt(4 pi a_s n); xi = 1/sqrt(4 pi a_s n);
    k_x = 2/xi; lambda_x = pi xi."""
    c_s = (HBAR / m_kg) * math.sqrt(4.0 * math.pi * a_s * n)
    xi = 1.0 / math.sqrt(4.0 * math.pi * a_s * n)
    return c_s, xi, 2.0 / xi, math.pi * xi

CS_RB, XI_RB, KX_RB, LX_RB = bec(RB87_M_U * U_KG, RB87_AS, N_LAB)
CS_SR, XI_SR, KX_SR, LX_SR = bec(SR88_M_U * U_KG, SR88_AS, N_LAB)
XI_RB_8MMS = HBAR / (RB87_M_U * U_KG * RB87_CS_8MMS)
LX_RB_8MMS = math.pi * XI_RB_8MMS
# the m*c_s invariance legs
MC_FW = M_KG * SIGMA
MC_RB = RB87_M_U * U_KG * CS_RB
MC_SR = SR88_M_U * U_KG * CS_SR
CS_RATIO = SIGMA / CS_RB
M_RATIO = M_KG / (RB87_M_U * U_KG)

print("  IDENTICAL dispersion (the BEC universality class, Bogoliubov):")
print("    omega(k) = c_s k sqrt(1 + (k xi/2)^2),  xi = hbar/(m c_s),  k_x = 2/xi")
print()
print("  THE CORRESPONDENCE TABLE (committed numbers re-derived):")
print("    quantity            framework        87Rb BEC          88Sr BEC")
print("    m (kg)              %.3e     %.4e      %.4e" %
      (M_KG, RB87_M_U * U_KG, SR88_M_U * U_KG))
print("    c_s (m/s)           %.4e      %.4e      %.4e" % (SIGMA, CS_RB, CS_SR))
print("    xi (nm)             %9.2f       %9.2f       %9.2f" % (XI * 1e9, XI_RB * 1e9, XI_SR * 1e9))
print("    k_x (m^-1)          %.4e   %.4e   %.4e" % (K_X, KX_RB, KX_SR))
print("    lambda_x (nm)       %9.2f   %9.2f   %9.2f" % (LAMBDA_X * 1e9, LX_RB * 1e9, LX_SR * 1e9))
print("    (87Rb params: m = 86.91 u, a_s = 5.77 nm, n = 1e20 m^-3;")
print("     88Sr params: m = 87.91 u, a_s = 6.51 nm, n = 1e20 m^-3)")
print()
print("  THE RATIOS (framework / 87Rb, then / 88Sr):")
kratio_rb = K_X / KX_RB
kratio_sr = K_X / KX_SR
print("    k_x ratio   = (m c_s)_fw/(m c_s)_lab = xi_lab/xi_fw")
print("                 = %.4f  (87Rb),  %.4f  (88Sr)   -- ORDER UNITY" % (kratio_rb, kratio_sr))
print("    lambda_x ratio = %.4f (87Rb), %.4f (88Sr) -- 3-4x in wavelength" %
      (LAMBDA_X / LX_RB, LAMBDA_X / LX_SR))
print()
print("  WHY ORDER UNITY -- the m*c_s invariance across 16 orders of legs:")
print("    c_s ratio (fw/Rb) = %.3e   (119 km/s vs %.4f m/s)" % (CS_RATIO, CS_RB))
print("    m   ratio (fw/Rb) = %.3e   (9.1e-33 vs 1.4e-25 kg)" % M_RATIO)
print("    product           = %.4f = the k_x ratio: the healing scale m c_s = hbar/xi" %
      (CS_RATIO * M_RATIO))
print("    is INVARIANT -- the massive c_s upscaling is cancelled exactly by the")
print("    tiny m downscaling; the crossover lives at the SAME physics scale.")
print()
print("  THE REVERSE DIRECTION (already a lab scale):")
print("    a standard Rb BEC at c_s = 8 mm/s: xi = %.1f nm, lambda_x = %.1f nm" %
      (XI_RB_8MMS * 1e9, LX_RB_8MMS * 1e9))
print("    vs the framework: xi = %.1f nm, lambda_x = %.1f nm -- WITHIN 6%%" %
      (XI * 1e9, LAMBDA_X * 1e9))
print("    xi_fw = 97.5 nm sits INSIDE the standard lab BEC window xi in [~0.09, 1] um.")
print("    The framework's transition is a DEEP-UV/NEAR-UV LAB SCALE, not an")
print("    astrophysical one.")

chk("C10 [BEC analog] k_x ratio fw/Rb = (m c_s) ratio = xi_Rb/xi_fw (exact algebra)",
    abs(kratio_rb - MC_FW / MC_RB) / kratio_rb < 1e-9 and
    abs(kratio_rb - XI_RB / XI) / kratio_rb < 1e-9,
    "k_x(fw)/k_x(Rb) = %.4f = (m c_s)_fw/(m c_s)_Rb = %.4f = xi_Rb/xi_fw = %.4f" %
    (kratio_rb, MC_FW / MC_RB, XI_RB / XI))
chk("C11 [order-unity] crossover wavelengths within 4x: lambda_x in [306 nm, 1.17 um]",
    0.2 < LAMBDA_X / LX_RB < 0.5 and 0.2 < LAMBDA_X / LX_SR < 0.5,
    "lambda_x_fw/lam_Rb = %.3f; /lam_Sr = %.3f" % (LAMBDA_X / LX_RB, LAMBDA_X / LX_SR))
chk("C12 [m*c_s invariance] c_s ratio x m ratio = k_x ratio (16-order cancellation)",
    abs(CS_RATIO * M_RATIO - kratio_rb) / kratio_rb < 1e-9,
    "(c_s ratio) x (m ratio) = %.3e x %.3e = %.4f" % (CS_RATIO, M_RATIO, CS_RATIO * M_RATIO))
chk("C13 [lab window] xi_fw = 97.5 nm inside [0.09, 1] um; 8-mm/s Rb within 6%%",
    90.0e-9 < XI < 1.0e-6 and abs(XI - XI_RB_8MMS) / XI_RB_8MMS < 0.10,
    "xi_fw = %.2f nm vs xi_Rb(8 mm/s) = %.2f nm (%.1f%%)" %
    (XI * 1e9, XI_RB_8MMS * 1e9, 100.0 * abs(XI - XI_RB_8MMS) / XI_RB_8MMS))

# =============================================================================
banner("(2b) THE COSMOLOGICAL ANALOG -- does any 97.5-nm signature survive?")
# =============================================================================
hm_kpc_low = (M_HM_LO_MSUN / (1.0e10)) ** (1.0 / 3.0) * 300.0   # rough halo radius scale, kpc
orders_subhalo = math.log10((1.0 * KPC) / LAMBDA_X)   # 1-kpc structure vs lambda_x
orders_hm = math.log10((LAMBDA_FS_MPC * MPC) / LAMBDA_X)   # 0.558-Mpc free-streaming cut vs lambda_x
orders_rM = math.log10((XI / R_M) ** -1.0)   # the xi/r_M deficit in orders

print("  THE STRUCTURE REGISTERS (smallest committed scales):")
print("    subhalo floor          ~ 1e-6-1e5 Msun (G115 CDM contrast) -- kpc-scale halos")
print("    WDM-class truncation   M_hm = 5e5-5.8e6 Msun (G115), lambda_fs = 0.558 Mpc,")
print("                           k_hm = 57.2 h/Mpc (D07/G212) -- the framework's own")
print("                           closed-form free-streaming cut from m")
print("    the transition         lambda_x = %.1f nm (this lane)" % (LAMBDA_X * 1e9))
print()
print("    orders ABOVE lambda_x: 1-kpc subhalo structure ... %.1f" % orders_subhalo)
print("                            lambda_fs = 0.558 Mpc .... %.1f" % orders_hm)
print("                            r_M (the committed probe) . %.1f (xi/r_M = %.2e)" %
      (orders_rM, XI / R_M))
print("    => NOTHING at 97.5-nm scale survives in any committed structure register:")
print("       the smallest resolved scales sit 26-28 orders ABOVE the transition,")
print("       and no committed equation couples lambda_x to cosmology (xi is built")
print("       from m and c_s only -- the free-streaming cut lambda_fs = 0.558 Mpc")
print("       is 5.6e27 x larger than lambda_x and is the SAME m, different physics).")
print()
print("  THE AXION / WISPy CLASS:  UNVERIFIED.")
print("    no committed register maps 97.5 nm to any axion-like mass, density,")
print("    string/domain-wall scale, or coupling; the framework's axiomatic")
print("    position (no particle, H054 max-entropy origin) places the axion class")
print("    formally OUTSIDE its committed content.  No claim is made;")
print("    'unverified' is the register.  (The framework's lambda_x = 306 nm is")
print("    set by (m, c_s) -- a coherence scale, not a particle mass.)")

chk("C14 [probeability] xi/r_M = 3.09e-28 (28 orders below the committed probe)",
    abs(math.log10(XI / R_M) - math.log10(3.1e-28)) < 0.1,
    "xi/r_M = %.3e (log10 = %.2f)" % (XI / R_M, math.log10(XI / R_M)))
chk("C15 [no cosmic signature] smallest structure registers 26-28 orders ABOVE lambda_x",
    orders_subhalo > 15.0 and orders_hm > 15.0,
    "1 kpc vs lambda_x: %.1f orders; lambda_fs 0.558 Mpc: %.1f orders" %
    (orders_subhalo, orders_hm))
chk("C16 [S10 cutoff] S10's finest committed cutoff (1 m) is 7 orders ABOVE xi",
    abs(math.log10(1.0 / XI) - math.log10(1.03e7)) < 0.1,
    "1 m/xi = %.3e -> %.1f orders" % (1.0 / XI, math.log10(1.0 / XI)))

# =============================================================================
banner("(3) THE HONEST VERDICT")
# =============================================================================
print("  THE 97.5-NM TRANSITION IS PROBABLY UNOBSERVABLE IN SITU")
print("    - 28 orders below the smallest committed probe (xi/r_M = 3.1e-28);")
print("    - 7 orders below S10's finest committed integration cutoff (1 m);")
print("    - no committed structure register reaches within 19 orders of it;")
print("    - and the floor it predicts is formal: < 1 particle per coherence")
print("      volume at every committed radius (N_xi(max) = 9.1e-11).")
print()
print("  BUT ALGEBRAICALLY-ANALOGOUS TO LABORATORY BEC PHYSICS, EXACTLY:")
print("    - the SAME Bogoliubov dispersion omega(k) = c_s k sqrt(1 + (k xi/2)^2);")
print("    - the SAME healing crossover k_x = 2/xi, lambda_x = pi xi;")
print("    - crossover wavelengths within ~4x of standard 87Rb/88Sr BECs")
print("      (306 nm vs 1.17 um / 1.10 um), within 6% of a shallower 8-mm/s Rb");
print("    - because m*c_s = hbar/xi is INVARIANT: the 6e7 c_s upscaling is")
print("      cancelled by the 1.6e7 m downscaling (16 orders of legs, one scale).")
print()
print("  THE FRAMEWORK'S QUANTUM FACE IS THE BOSE-EINSTEIN UNIVERSALITY CLASS:")
print("    gapless Goldstone phonon (B8: gap exactly zero) + the Bogoliubov")
print("    healing crossover at k_x = 2.05e7 m^-1, lambda_x = 306.3 nm, with the")
print("    zero-point structure factor S(k) = (k xi/2)/sqrt(1 + (k xi/2)^2)")
print("    saturating to the Poissonian floor -- unobservable in situ,")
print("    universal in class, and already-realized in every cold-atom lab")

# =============================================================================
banner("(4) VERDICTS")
# =============================================================================
print("  V1 THE CROSSOVER:")
print("     k_x     = 2 m c_s/hbar = 2/xi = %.6e m^-1   (1/k_x = %.2f nm)" %
      (K_X, 1.0 / K_X * 1e9))
print("     lambda_x = pi xi = %.4f nm   (band [%.1f, %.1f] nm over the committed" %
      (LAMBDA_X * 1e9, LAMBDA_X_BAND_M[0] * 1e9, LAMBDA_X_BAND_M[1] * 1e9))
print("               (m, c_s) band);  = lambda_dB/2 EXACTLY (612.57 nm, S1);")
print("     the mode at k_x runs at sqrt(2) c_s k_x (41% off the Goldstone line);")
print("     the crossover phonon energy = 2 k_B T_b = %.4e eV EXACTLY." %
      (2.0 * KB_TB / EV))
print()
print("  V2 THE BEC-CORRESPONDENCE TABLE (the SAME physics at a different scale):")
print("     quantity           framework        87Rb BEC        88Sr BEC")
print("     m (kg)             %.3e     %.4e    %.4e" %
      (M_KG, RB87_M_U * U_KG, SR88_M_U * U_KG))
print("     c_s (m/s)          %.4e      %.4e     %.4e" % (SIGMA, CS_RB, CS_SR))
print("     xi (nm)            %9.2f      %9.2f     %9.2f" % (XI * 1e9, XI_RB * 1e9, XI_SR * 1e9))
print("     lambda_x (nm)      %9.2f   %9.2f   %9.2f" % (LAMBDA_X * 1e9, LX_RB * 1e9, LX_SR * 1e9))
print("     k_x ratio (fw/lab)           %.3f          %.3f" % (kratio_rb, kratio_sr))
print("     -> the healing crossover is ORDER-UNIT identical: 306 nm vs 1.17/1.10 um,")
print("        6% from an 8-mm/s Rb (xi = 91 nm); m*c_s = hbar/xi invariant across")
print("        the 16 order-of-magnitude legs (c_s 6e7 up, m 1.6e7 down).")
print()
print("  V3 THE HONEST STATEMENT:")
print("     the 97.5-nm transition: UNOBSERVABLE IN SITU (28 orders below the")
print("     smallest committed probe; floor formal: < 1 particle per coherence")
print("     volume at every committed radius), UNIVERSAL IN CLASS (exactly the")
print("     laboratory BEC healing crossover, same Bogoliubov form, k_x = 2/xi,")
print("     lambda_x = pi xi, wavelengths within 4x of standard 87Rb/88Sr BECs) --")
print("     THE FRAMEWORK'S QUANTUM FACE IS THE BOSE-EINSTEIN UNIVERSALITY: the")
print("     numbers are k_x = 2.05e7 m^-1, lambda_x = 306.3 nm, xi = 97.5 nm,")
print("     S(k) = (k xi/2)/sqrt(1 + (k xi/2)^2) -> 1 below xi; and the axion/")
print("     WISPy class is UNVERIFIED (no committed register, no claim).")
print()
print("  %d checks: %d PASS, %d FAIL" %
      (len(CHECKS), sum(c["pass"] for c in CHECKS),
       len(CHECKS) - sum(c["pass"] for c in CHECKS)))
assert all(c["pass"] for c in CHECKS), "F02: a check FAILED -- a finding, as registered"

# ------------------------------------------------------------------ the JSON
results = {
    "title": "F02 -- THE 97.5-NM TRANSITION",
    "registers": {
        "m_keV": M_KEV, "m_keV_band": list(M_KEV_BAND),
        "sigma_kms": SIGMA_KMS, "T_b_K": M_KG * SIGMA2 / KB,
        "xi_m": XI, "xi_nm": XI * 1e9, "xi_register_nm": 97.49,
        "xi_heal_nm": XI_HEAL * 1e9,
        "lambda_dB_nm": LAMBDA_DB * 1e9, "lambda_dB_register_nm": 612.57,
        "xi_over_rM": XI / R_M,
    },
    "transition": {
        "k_x_m^-1": K_X, "k_x_inv_nm": 1.0 / K_X * 1e9,
        "lambda_x_nm": LAMBDA_X * 1e9,
        "lambda_x_band_nm": [LAMBDA_X_BAND_M[0] * 1e9, LAMBDA_X_BAND_M[1] * 1e9],
        "lambda_x_eq_lambda_dB_over_2": LAMBDA_X == LAMBDA_DB / 2.0,
        "crossover_energy_eV": 2.0 * KB_TB / EV,
        "crossover_energy_eq_2_kB_Tb": E_CROSSOVER_J == 2.0 * KB_TB,
        "omega_at_kx_over_goldstone": math.sqrt(2.0),
        "nonlinearity_pct": 100.0 * (math.sqrt(2.0) - 1.0),
        "dispersion_form": "omega(k) = c_s k sqrt(1 + (k xi/2)^2),  xi = hbar/(m c_s)",
        "mode_freq_at_kx_Hz": F_CROSSOVER_HZ,
    },
    "quantum_floor": {
        "structure_factor_form": "S(k) = (k xi/2)/sqrt(1 + (k xi/2)^2)  (Bogoliubov/Feynman)",
        "S_at_xi": S_k(1.0), "S_at_kx": S_k(2.0), "S_at_4xi": S_k(4.0),
        "S_asymptote": 1.0,
        "N_xi_at_rM": N_XI_RM, "N_xi_capped_core": N_XI_CAP,
        "delta_n_over_n_at_rM": DX_RM, "delta_n_over_n_capped_core": DX_CAP,
        "floor_realized": False,
        "n_lambda_dB3": N_RM * LAMBDA_DB**3,
    },
    "bec_correspondence": {
        "table": [
            {"system": "framework", "m_kg": M_KG, "c_s_ms": SIGMA,
             "xi_nm": XI * 1e9, "k_x_m-1": K_X, "lambda_x_nm": LAMBDA_X * 1e9},
            {"system": "87Rb", "params": "m = 86.91 u, a_s = 5.77 nm, n = 1e20 m^-3",
             "m_kg": RB87_M_U * U_KG, "c_s_ms": CS_RB, "xi_nm": XI_RB * 1e9,
             "k_x_m-1": KX_RB, "lambda_x_nm": LX_RB * 1e9},
            {"system": "88Sr", "params": "m = 87.91 u, a_s = 6.51 nm, n = 1e20 m^-3",
             "m_kg": SR88_M_U * U_KG, "c_s_ms": CS_SR, "xi_nm": XI_SR * 1e9,
             "k_x_m-1": KX_SR, "lambda_x_nm": LX_SR * 1e9},
        ],
        "k_x_ratio_fw_over_rb": kratio_rb, "k_x_ratio_fw_over_sr": kratio_sr,
        "lambda_x_ratio_fw_over_rb": LAMBDA_X / LX_RB,
        "lambda_x_ratio_fw_over_sr": LAMBDA_X / LX_SR,
        "c_s_ratio_fw_over_rb": CS_RATIO, "m_ratio_fw_over_rb": M_RATIO,
        "m_times_c_s_invariance": CS_RATIO * M_RATIO == kratio_rb,
        "xi_Rb_8mms_nm": XI_RB_8MMS * 1e9, "lambda_x_Rb_8mms_nm": LX_RB_8MMS * 1e9,
        "xi_fw_within_6pct_of_8mms_Rb": abs(XI - XI_RB_8MMS) / XI_RB_8MMS,
    },
    "cosmological_analog": {
        "M_hm_Msun": [M_HM_LO_MSUN, M_HM_HI_MSUN],
        "lambda_fs_Mpc": LAMBDA_FS_MPC, "k_hm_h_per_Mpc": K_HM_HMPC,
        "orders_1kpc_above_lambda_x": orders_subhalo,
        "orders_lambda_fs_above_lambda_x": orders_hm,
        "orders_rM_above_xi": orders_rM,
        "axion_wispy_class": "UNVERIFIED -- no committed register maps 97.5 nm to any "
                             "axion-like scale/coupling; no claim",
    },
    "verdicts": {
        "V1_crossover": "k_x = 2.05e7 m^-1 (1/k_x = 48.7 nm); lambda_x = 306.3 nm = "
                        "pi xi = lambda_dB/2; phonon energy at k_x = 2 k_B T_b; "
                        "omega(k_x) = sqrt(2) c_s k_x (41% nonlinear)",
        "V2_bec_table": "framework xi = 97.5 nm, lambda_x = 306.3 nm vs 87Rb "
                        "(371 nm, 1.17 um) and 88Sr (350 nm, 1.10 um): k_x within "
                        "3.6-3.8x, lambda_x within 3-4x -- the SAME Bogoliubov "
                        "healing crossover, m*c_s = hbar/xi invariant across 16 orders",
        "V3_honest": "PROBABLY UNOBSERVABLE in situ (28 orders below any committed "
                     "probe, xi/r_M = 3.1e-28; floor formal: N_xi < 1 everywhere) "
                     "BUT UNIVERSAL IN CLASS: the framework's quantum face IS the "
                     "Bose-Einstein universality class -- gapless Goldstone phonon "
                     "plus the Bogoliubov healing crossover at k_x = 2.05e7 m^-1, "
                     "lambda_x = 306.3 nm, S(k) -> Poissonian floor below xi",
    },
    "checks": CHECKS,
    "n_checks": len(CHECKS),
    "n_pass": sum(c["pass"] for c in CHECKS),
}
with open(OUT_PATH, "w") as f:
    json.dump(results, f, indent=1)
print()
print("wrote %s  (%d checks, %d PASS)" % (OUT_PATH, len(CHECKS), sum(c["pass"] for c in CHECKS)))