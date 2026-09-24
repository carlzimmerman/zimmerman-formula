#!/usr/bin/env python3
"""
bilek_data.py -- transcribed dataset from Bilek, Renaud & Samurovic 2026
(arXiv:2603.23591, A&A), "Deviations from the radial acceleration relation in
the central galaxies of clusters, subclusters, and groups".

Provenance: every constant below carries (paper-table, row) tags.
  - ENV: Table 1 (eq:env), rows 1..17: rank, galaxy, host, host virial mass
    (X = no number in the paper), r_max [kpc].
  - BESTFIT: Appendix Table A.1 (bestfittab.txt): per galaxy, three Jeans
    models (beta_iso / beta_neg / beta_lit), each (M/L, log10(M_v/Msun),
    log10(r_s/kpc)) with M_v the NFW "virial mass", r_s the scale radius.
  - Paper's own text claims transcribed as VERBATIM constants for audits.

The absorbed constants are checkable claims, per house provenance rule.
"""
import math

# ---------------------------------------------------------------- constants
G = 6.67430e-11          # N m^2 kg^-2
MSUN = 1.98847e30        # kg
KPC = 3.085677581491367e19   # m
MPC = 1000.0 * KPC

# Registered a0 footings of the framework (hermes_push/STATE.md H001) and the
# paper's own fiducial (Bilek et al. eq:rar a0 = 1.2e-10).
FOOT = {"K1": 1.1279e-10, "K2": 9.3619e-11}
A0_PAPER = 1.2e-10

# NFW truncation concentration assumed for M_v (not stated in the paper:
# REFEREE FINDING BIL-R3). c = 10 default; lane prints the sensitivity.
C_CONC = 10.0
A_C = math.log(1.0 + C_CONC) - C_CONC / (1.0 + C_CONC)   # = ln(1+c) - c/(1+c)

# ----------------------------------------------------------------- environment
# (rank, galaxy, host-string, host virial mass [Msun] or None, r_max [kpc])
ENV = [
    (1,  "NGC4486", "Central of Virgo A",                  5e14, 140),
    (2,  "NGC4472", "Central of Virgo B",                  1e14,  45),
    (3,  "NGC1399", "Central of Fornax Cluster",           9e13, 106),
    (4,  "NGC5846", "Central of its group",                8e13,  64),
    (5,  "NGC1407", "Central of its group",                6e13, 122),
    (6,  "NGC4365", "Central of Virgo W' cloud",           3e13,  69),
    (7,  "NGC4649", "Central of Virgo C",                  3e13, 105),
    (8,  "NGC5128", "Central of its group",                8e12,  52),
    (9,  "NGC4278", "Central of Coma I clump",             None,  39),
    (10, "NGC1023", "Central own group, virtually isolated", None, 26),
    (11, "NGC2768", "Isolated or group member",            None,  60),
    (12, "NGC3115", "Isolated",                             None,  22),
    (13, "NGC0821", "Isolated",                             None,  35),
    (14, "NGC4494", "Non-central of Coma II cloud",        None,  38),
    (15, "NGC3377", "Non-central of Leo I group",          None,  31),
    (16, "NGC1400", "Non-central of NGC1407 group",        None,  71),
    (17, "NGC4526", "Non-central of Virgo B",              None,  33),
]

# ------------------------------------------------------------------- best fits
# name -> (iso (M/L, logMv, logrs), neg (...), lit (...)) -- Appendix A.1
BESTFIT = {
    "NGC0821": ((-5.82, 12.2, 0.464), (-8.82, 12.1, 0.295), (-4.29, 12.2, 0.569)),
    "NGC1023": (( 3.27, 10.9, 1.43),  ( 3.05, 11.0, 1.53),  ( 3.23, 11.1, 1.59)),
    "NGC1399": ((-3.09, 13.9, 2.00),  (-3.30, 13.9, 2.10),  (-4.01, 13.9, 1.96)),
    "NGC1400": (( 1.74, 12.6, 1.54),  ( 2.92, 12.5, 1.57),  (-0.117, 12.7, 1.57)),
    "NGC1407": (( 6.98, 15.8, 6.06),  ( 1.94, 13.7, 2.23),  ( 4.95, 15.2, 4.78)),
    "NGC2768": ((-12.7, 12.4, 0.492), (-2.66, 12.1, 0.488), (-10.3, 12.4, 0.615)),
    "NGC3115": ((-8.05, 12.0, 0.357), ( 3.38, 11.7, 0.435), (-7.04, 12.1, 0.534)),
    "NGC3377": (( 6.66, 12.4, 1.95),  ( 7.22, 12.7, 2.24),  ( 5.93, 12.3, 1.81)),
    "NGC4278": ((-3.15, 12.3, 0.660), ( 7.35, 12.3, 1.10),  ( 0.165, 12.8, 1.37)),
    "NGC4365": (( 10.6, 16.5, 4.49),  ( 13.2, 16.3, 4.52),  (  4.06, 13.1, 1.05)),
    "NGC4472": (( 3.31, 12.7, -0.248),(-1.42, 13.5, 1.48),  ( 0.236, 14.2, 2.04)),
    "NGC4486": ((-4.92, 13.5, 1.41),  (-6.69, 13.4, 1.28),  (-2.84, 13.8, 1.77)),
    "NGC4494": (( 1.44, 13.5, 3.04),  ( 1.43, 13.4, 2.90),  ( 0.896, 12.3, 1.84)),
    "NGC4526": (( 4.64, 15.1, 4.57),  ( 4.62, 15.1, 4.56),  (  2.38, 13.0, 1.99)),
    "NGC4649": (( 5.72, 16.1, 4.12),  ( 7.04, 14.1, 2.54),  (  4.01, 16.4, 4.26)),
    "NGC5128": ((-0.496, 13.7, 2.22), ( 0.269, 13.7, 2.18), (-0.400, 16.6, 5.43)),
    "NGC5846": ((-0.846, 14.1, 2.35), (-1.56, 13.2, 1.65),  (  5.31, 13.6, 2.04)),
}

# -------------------------------------------------- paper's own text claims
# Verbatim-anchored numbers used by the doors:
VIRGO_TOTAL_MSUN = 6.3e14     # "the virial masses of clumps A, B, and C add to
                              #  the well-established virial mass of the whole
                              #  Virgo Cluster (6.3e14 Msun)" (Sect. env)
SEP_SUBCLUSTERS_MPC = 1.0     # "the centrals of the Virgo subclusters A, B and
                              #  C are around 1 Mpc from each other" (Sect. conc)
GAL_HOST = {  # galaxy -> (host name, host virial mass Msun or None)
    "NGC4486": ("Virgo A", 5e14), "NGC4472": ("Virgo B", 1e14),
    "NGC1399": ("Fornax", 9e13),  "NGC5846": ("grp5846", 8e13),
    "NGC1407": ("grp1407", 6e13), "NGC4365": ("Virgo W'", 3e13),
    "NGC4649": ("Virgo C", 3e13), "NGC5128": ("grp5128", 8e12),
    "NGC4278": ("Coma I clump", None),
    "NGC1023": ("own group", None),
}
RANK = {r[1]: r[0] for r in ENV}
RMAX = {r[1]: r[4] for r in ENV}

# ------------------------------------------------------------------- helpers
def nfw_F(y):
    """NFW profile shape ln(1+y) - y/(1+y)."""
    return math.log(1.0 + y) - y / (1.0 + y)

def g_halo(galaxy, model, r_kpc):
    """NFW halo acceleration [m/s^2] at r_kpc from (M_v, r_s) of a model fit.
    Convention (REFEREE FINDING BIL-R3): M_v = mass within virial radius,
    c = C_CONC; the paper does not state c, so absolute values carry ~+-20%
    sensitivity (A(7)=1.19, A(15)=1.75); RATIOS between galaxies are
    convention-independent common factors."""
    ml, lmv, lrs = BESTFIT[galaxy][model]
    Mv = 10.0 ** lmv * MSUN
    rs = 10.0 ** lrs * KPC
    r = r_kpc * KPC
    y = r / rs
    return G * Mv / (r * r) * nfw_F(y) / A_C

def g_peak(galaxy, model):
    """Peak NFW acceleration [m/s^2] (shape max at y ~ 2.16, c-independent)."""
    ml, lmv, lrs = BESTFIT[galaxy][model]
    Mv = 10.0 ** lmv * MSUN
    rs = 10.0 ** lrs * KPC
    best = (0.0, 0.0)
    y = 1e-3
    while y < 1e3:
        f = nfw_F(y) / (y * y)
        if f > best[0]:
            best = (f, y)
        y *= 1.01
    return G * Mv / (rs * rs) * best[0] / A_C, best[1]

def ambient_field_1Mpc(masses_msun):
    """Summed point-mass field [m/s^2] of sibling structures at the paper's
    fiducial 1-Mpc separation (SEP_SUBCLUSTERS_MPC)."""
    d = SEP_SUBCLUSTERS_MPC * MPC
    tot = 0.0
    for m in masses_msun:
        tot += G * m * MSUN / (d * d)
    return tot