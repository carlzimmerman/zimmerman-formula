#!/usr/bin/env python3
"""mi_constants.py -- THE single source of truth. Import this; never retype a constant.

    import sys; sys.path.insert(0, "qwen_36_experiment/opus_orchestrator_oracle/TOOLS")
    from mi_constants import *

This module exists because the qwen experiment folder produced FOUR different values of a_0
(1.2e-10, 2.4e-10, 9.425e-11, 9.3614e-11) and a "Z" of 0.7135 colliding with Z = 5.7888.
Every number here is derived, printed with its provenance by self_check(), and cross-checked.
"""
import math

# --- measured inputs -------------------------------------------------------------
G      = 6.67430e-11          # m^3 kg^-1 s^-2
C      = 2.99792458e8         # m/s  (exact)
LAMBDA = 1.0908e-52           # m^-2, from Milgrom 1994's a_lambda = c^2 sqrt(L/3) = 5.419e-10
H0_KMS = 67.36                # km/s/Mpc, Planck 2018
OMEGA_L = 0.6889   # Planck 2018 TT,TE,EE+lowE+lensing+BAO. NB: the corpus's banked ALT/canon
                   # ratio 1.2082 corresponds to Omega_L = 0.68505 (a DIFFERENT Planck column);
                   # with 0.6889 the ratio is 1.204819. A 0.28% footing sub-choice nobody documented.
KPC    = 3.0856775814913673e19
MPC    = 1000.0 * KPC
MSUN   = 1.98892e30
GYR    = 3.1557e16            # s

# --- derived ---------------------------------------------------------------------
RHO_L  = LAMBDA * C**2 / (8 * math.pi * G)     # 5.844e-27 kg/m^3  (the DE MASS density)
CHL    = C**2 * math.sqrt(LAMBDA / 3.0)        # 5.4194e-10 m/s^2  = c H_Lambda
H_LAM  = CHL / C                               # 1.80772e-18 s^-1
T_GH   = H_LAM / (2 * math.pi)                 # Gibbons-Hawking temperature, in s^-1 units
T_DYN  = 1.0 / math.sqrt(G * RHO_L)            # 1.6011e18 s
CSQRT  = C * math.sqrt(G * RHO_L)              # 1.87228e-10 m/s^2 = c sqrt(G rho_L)

Z      = 2.0 * math.sqrt(8.0 * math.pi / 3.0)  # 5.7888100366  -- NOT the EOS lane's 0.7135
TWO_Z  = 2.0 * Z                               # 11.577620073
INV_Z  = 1.0 / Z                               # 0.1727470747

KAPPA  = 0.5                                   # *** FITTED, NOT DERIVED ***
A0 = {"canonical": 0.5 * CSQRT,                # 9.3614e-11  (rho_DE + cH_Lambda)
      "ALT":       0.5 * CSQRT / math.sqrt(OMEGA_L)}   # 1.13104e-10  (x 1.2082)
FLOOR = {k: v / 2.0 for k, v in A0.items()}    # Milgrom's balance floor; a_0 = 2*floor ALWAYS

OMEGA_C_LO, OMEGA_C_HI = 1.7824e-14, 2.2113e-14   # committed window (galactic + LLR), FREE constant
A0_EMPIRICAL = 1.20e-10                            # McGaugh / SPARC

# reference crossover values, q = a_0/cH_Lambda = 2/r
R_REF = {"Milgrom1999_eq8": 1.0, "Milgrom1999_eq10": 2.0,
         "conventional_4pi": 4.0 * math.pi, "kappa_half_2Z": TWO_Z}


def nu(y):
    """Milgrom 1999 PLA 253:273 eqs 6-9 kernel. y = g_bar/a_0."""
    return math.sqrt(1.0 + 1.0 / y)


def a0_line(g_bar, a0=None):
    """g_obs from g_obs^2 = g_bar^2 + a_0 g_bar (alpha=1; EXCLUDED at 378 sigma by ephemeris)."""
    a0 = A0["canonical"] if a0 is None else a0
    return math.sqrt(g_bar * g_bar + a0 * g_bar)


def r_of_a0(a0):
    """crossover ratio r from an acceleration scale."""
    return 2.0 * CHL / a0


def self_check(verbose=True):
    """Cross-check every derived value. Returns (n_ok, n_total)."""
    tests = [
        ("rho_L from Lambda",      RHO_L, 5.844e-27, 2e-3),
        ("cH_Lambda",              CHL, 5.4194e-10, 1e-4),
        ("Z = 2 sqrt(8pi/3)",      Z, 5.7888100366, 1e-10),
        ("2Z",                     TWO_Z, 11.577620073, 1e-10),
        ("1/Z",                    INV_Z, 0.172747074736, 1e-11),
        ("a_0 canonical",          A0["canonical"], 9.3614e-11, 3e-3),
        ("a_0 ALT",                A0["ALT"], 1.13104e-10, 3e-3),
        ("ALT/canon = 1/sqrt(OmL)", A0["ALT"]/A0["canonical"], 1.0/(0.6889**0.5), 1e-12),
        ("banked 1.2082 needs OmL", 1.0/1.2082**2, 0.68505, 1e-4),
        ("floor = a_0/2",          FLOOR["canonical"], 4.6810e-11, 3e-3),
        ("t_dyn",                  T_DYN, 1.6011e18, 1e-3),
        ("c sqrt(G rho_L)",        CSQRT, 1.87228e-10, 1e-3),
        ("a_0/cH_L = 1/Z",         A0["canonical"]/CHL, INV_Z, 3e-3),
        ("r(a_0 canon) = 2Z",      r_of_a0(A0["canonical"]), TWO_Z, 3e-3),
        ("memory time 1/(a0/c)",   C/A0["canonical"]/GYR, 101.5, 1e-2),
    ]
    ok = 0
    for name, got, want, tol in tests:
        good = abs(got/want - 1.0) < tol
        ok += good
        if verbose:
            print(f"  [{'OK' if good else 'FAIL'}] {name:<26} {got:.6e}  (expect {want:.6e})")
    if verbose:
        print(f"\n  {ok}/{len(tests)} constants cross-check.")
        print(f"  kappa = {KAPPA} is FITTED, NOT DERIVED.")
    return ok, len(tests)


if __name__ == "__main__":
    import sys
    n, m = self_check()
    sys.exit(0 if n == m else 1)
