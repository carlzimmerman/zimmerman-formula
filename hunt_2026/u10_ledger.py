#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""u10_ledger.py -- the COMBINED liability ledger in one machine-readable table, plus the keeper battery.

Imported by u11_kernel_modifications.py, u12_extra_variable_modifications.py and u13_mass_efe_and_domain.py.
Nothing here is a claim; it is the shared table and the shared measuring instruments.  Each row's numbers are
transcribed from the previous phase's common-currency reductions (u01_cluster_common_currency.py,
u01_pressure_supported_common_currency.py, u01_common_currency_disc_lensing.py), which in turn re-read the
h*.out files.  Spot checks against the source .out files are run as checks in u11_kernel_modifications.py.

CURRENCY.  Every row carries
    B  = log10( g_obs / g_pred )      signed, in dex of ACCELERATION, on the CANONICAL footing
    y  = g_bar^Newtonian / a_0        at the SAME radius, computed with the CANONICAL a_0
so that B = 0 means the framework lands.  A cluster row's eta_g is exactly 10**B.  Mass-currency numbers
(eta_M) are NOT used here: mixing them is the defect u01 found in the ledger.

For rows where an external field was applied by the source script, B_iso is the EFE-free value and B_efe the
published one.  Kernel modifications are tested against B_iso (a nu(y) change maps cleanly onto an isolated
system and not onto an EFE recipe); the EFE itself is the subject of u13.

TWO ROWS ARE NOT AMPLITUDE MISSES and are excluded from every amplitude fit, carried separately:
    warps  -- a LOCATION failure (the onset radius, off by x6.4 in radius)
    fp     -- a GRADIENT failure (the sigma coefficient is pinned to the virial value by a theorem)
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import *

KPC = kpc


# ---------------------------------------------------------------------------------------------- the ledger
# name                     class      B_iso   B_efe    y        r_kpc    x_ext  support   dup_group
_ROWS = [
    # ---- eight cluster/group liabilities (u01_cluster_common_currency.py; no EFE anywhere in this block)
    ("xray_ellipticals",   "cluster",  0.2279,  None,  0.80,      20.0,  0.0, "pressure", "humphrey"),
    ("xcop_cores",         "cluster",  0.4639,  None,  0.52,      50.0,  0.0, "pressure", "xcop_core"),
    ("clash_lensing",      "cluster",  0.5378,  None,  0.361,    200.0,  0.0, "lensing",  "clash"),
    ("bullet_bcg1",        "cluster",  0.5011,  None,  0.414,    300.0,  0.0, "lensing",  "bullet"),
    ("bullet_bcg3",        "cluster",  0.4983,  None,  0.382,    300.0,  0.0, "lensing",  "bullet"),
    ("lovisari_r2500",     "cluster",  0.3502,  None,  0.041,    224.0,  0.0, "pressure", "lovisari"),
    ("lovisari_r500",      "cluster",  0.1614,  None,  0.023,    526.0,  0.0, "pressure", "lovisari"),
    ("xcop_0.2r500",       "cluster",  0.4409,  None,  0.259,    246.0,  0.0, "pressure", "xcop_r500"),
    ("xcop_0.5r500",       "cluster",  0.3201,  None,  0.175,    616.0,  0.0, "pressure", "xcop_r500"),
    ("xcop_0.9r500",       "cluster",  0.1703,  None,  0.111,   1107.0,  0.0, "pressure", "xcop_r500"),
    ("erass1_groups",      "cluster",  0.4200,  None,  0.0042,   409.0,  0.0, "pressure", "erass1_M"),
    ("erass1_clusters",    "cluster",  0.3284,  None,  0.036,    758.0,  0.0, "pressure", "erass1_M"),
    ("erass1_rich",        "cluster",  0.3365,  None,  0.113,   1395.0,  0.0, "pressure", "erass1_M"),
    ("erass1_lowz",        "cluster",  0.2833,  None,  0.031,    800.0,  0.0, "pressure", "erass1_z"),
    ("erass1_hiz",         "cluster",  0.4082,  None,  0.059,    676.0,  0.0, "pressure", "erass1_z"),
    # ---- pressure-supported ledger (u01_pressure_supported_common_currency.py)
    ("mw_ufd",             "psupp",    0.709,   1.650, 0.0008,     0.071, 0.0218, "pressure", "mw_sat"),
    ("m31_satellites",     "psupp",    0.232,   0.761, 0.0035,     0.299, 0.0112, "pressure", "m31_sat"),
    ("mw_classical_dsph",  "psupp",    0.134,   0.641, 0.0071,     0.406, 0.0095, "pressure", "mw_sat"),
    ("coma_udgs",          "psupp",    0.396,   1.195, 0.0074,     1.90,  0.660,  "pressure", "udg"),
    ("pal14",              "psupp",   -0.871,  -0.658, 0.0102,     0.0276,0.0190, "pressure", "globular"),
    ("lg_field_gaspoor",   "psupp",    0.118,   0.118, 0.0120,     0.242, 0.0,    "pressure", "lg_field"),
    ("pal3",               "psupp",   -0.148,  -0.075, 0.0213,     0.0202,0.0093, "pressure", "globular"),
    ("lg_field_all",       "psupp",   -0.088,  -0.088, 0.0297,     0.320, 0.0,    "pressure", "lg_field"),
    ("ngc1052_df2",        "psupp",   -0.771,  -0.485, 0.0339,     1.65,  0.0233, "pressure", "df"),
    ("pal4",               "psupp",   -0.811,  -0.781, 0.0489,     0.0159,0.0083, "pressure", "globular"),
    ("ngc1052_df4",        "psupp",   -1.375,  -1.155, 0.0582,     1.20,  0.0233, "pressure", "df"),
    ("sluggs_massive",     "psupp",    0.331,   0.331, 0.73,      20.9,   0.0,    "pressure", "sluggs"),
    ("ngc2419",            "psupp",   -0.201,  -0.199, 0.8619,     0.0198,0.0,    "pressure", "globular"),
    ("pne_earlytypes",     "psupp",    0.066,   0.066, 1.44,       7.9,   0.0,    "pressure", "pne"),
    ("sluggs_lowmass",     "psupp",    0.058,   0.058, 1.64,       7.3,   0.0,    "pressure", "sluggs"),
    ("atlas3d_chabrier",   "psupp",    0.094,   0.094, 2.32,       2.72,  0.0,    "pressure", "atlas3d"),
    ("atlas3d_salpeter",   "psupp",   -0.095,  -0.095, 3.94,       2.72,  0.0,    "pressure", "atlas3d"),
    # ---- disc / lensing ledger (u01_common_currency_disc_lensing.py)
    ("mw_kz",              "disc",    -0.115,  -0.115, 1.39,       8.2,   0.0,    "rotation", "mw_kz"),
    ("diskmass",           "disc",     0.177,   0.177, 0.353,      8.63,  0.0,    "rotation", "diskmass"),
    ("slacs_lenses",       "disc",     0.084,   0.084,10.0,        4.07,  0.0,    "lensing",  "slacs"),
    ("tidal_dwarfs",       "disc",    -0.682,  -0.394, 0.038,      4.8,   0.0,    "rotation", "tdg"),
    ("binary_pairs",       "disc",     0.553,   0.837, 0.0119,   141.0,   0.03,   "pressure", "pairs"),
]
# the two non-amplitude rows, carried but never fitted
_SPECIAL = [
    ("warp_onset",  "disc", 1.607, 0.185,    7.2,  "LOCATION failure: predicted onset 52 kpc vs measured 7.2 kpc"),
    ("fp_tilt",     "disc", 0.109, 16.8,     3.02, "GRADIENT failure: the sigma coefficient is virial by a theorem"),
]
# rows whose sign is explicitly not robust in the source reduction
_FRAGILE = {"diskmass": "sign flips to -0.011 at the stellar-population Upsilon_K = 0.60",
            "pal3":     "crosses zero (+0.096) on the harmonised QUMOND eq.-60 EFE recipe"}


def ledger(footing="canonical", efe="iso"):
    """Return the amplitude ledger as a list of dicts.

    footing : 'canonical' or 'alt'.  The alt footing changes y (y = g_bar/a_0) and shifts B.  Both are
              recomputed from the SAME g_bar, which is the invariant: g_bar = y_canonical * a_0_canonical.
    efe     : 'iso' (EFE stripped, the value a nu(y) modification must explain) or 'published'.
    """
    a0c, a0 = A0["canonical"], A0[footing]
    out = []
    for name, cls, b_iso, b_efe, y_c, r_kpc, x_ext, support, dup in _ROWS:
        g_bar = y_c*a0c                      # invariant, SI
        B_can = b_iso if efe == "iso" or b_efe is None else b_efe
        # g_obs is fixed by the canonical prediction and B; re-express B on the new footing
        g_obs = (10.0**B_can)*nu_s(y_c)*g_bar
        y = g_bar/a0
        B = math.log10(g_obs/(nu_s(y)*g_bar))
        r = r_kpc*KPC
        M_enc = g_bar*r*r/G                  # spherical enclosed baryonic mass implied by y and r (SI)
        out.append(dict(name=name, cls=cls, B=B, y=y, g_bar=g_bar, g_obs=g_obs, r_kpc=r_kpc, r=r,
                        M_enc=M_enc, M_enc_msun=M_enc/Msun, x_ext=x_ext, support=support, dup=dup,
                        Phi=G*M_enc/r, Sigma=M_enc/(math.pi*r*r), rho_bar=M_enc/(4.0/3.0*math.pi*r**3),
                        fragile=name in _FRAGILE))
    return out


def dedup(rows):
    """One row per dup_group, the median |B| member -- the robustness sample."""
    groups = {}
    for r in rows: groups.setdefault(r["dup"], []).append(r)
    out = []
    for k, v in groups.items():
        v = sorted(v, key=lambda r: abs(r["B"]))
        out.append(v[len(v)//2])
    return sorted(out, key=lambda r: r["y"])


# ---------------------------------------------------------------------------------------------- kernels
def nu_routeA(y):   return 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-14))))

def nu_family_n(y, n):
    """the standard 'alpha family': nu_n = [1/2 + sqrt(1/4 + y^-n)]^(1/n).  n=1 'simple', n=2 'standard'."""
    y = np.maximum(np.asarray(y, float), 1e-14)
    return (0.5 + np.sqrt(0.25 + y**(-n)))**(1.0/n)

def nu_routeA_p(y, p):
    """Route A with a free exponent: nu = 1/(1 - exp(-y^p)).  p = 1/2 is Route A."""
    y = np.maximum(np.asarray(y, float), 1e-14)
    return 1.0/(1.0 - np.exp(-y**p))

def nu_twoscale(y, A, y1, w):
    """Route A times a bump centred on log10 y1 of height A and log-width w -- the most generous
    'second acceleration scale' a modification can be, with the bump placed wherever the fit wants it."""
    y = np.maximum(np.asarray(y, float), 1e-14)
    return nu_routeA(y)*(1.0 + A*np.exp(-0.5*((np.log10(y) - np.log10(y1))/w)**2))

def nu_floor(y, f):
    """an additive acceleration floor: g = nu_A(y) g_bar + f a_0, i.e. nu_eff = nu_A(y) + f/y."""
    y = np.maximum(np.asarray(y, float), 1e-14)
    return nu_routeA(y) + f/y


# ---------------------------------------------------------------------------------------------- keepers
class Keepers:
    """The galactic successes, measured the same way for any kernel.  Baseline = Route A, canonical a_0.

    K1  RAR point scatter          SPARC, rms of log10 g_obs - log10 [nu(y) g_bar]
    K2  RAR median offset          the same residual's median (must stay at zero)
    K3  deep-tail slope            log-log slope of g_obs vs g_bar for g_bar < 1e-11 (predicted 0.500)
    K4  BTFR slope / a_0           v_flat^4 vs M_b (predicted slope 1, intercept G a_0)
    K5  Renzo 1st order            regression of measured dln v/dln r on the kernel's prediction (predicted 1)
    K6  inner diversity            corr(predicted, observed) of v(2 kpc)/v_flat (baseline r = 0.79)
    K7  lensing 1/r slope          the deep limit's power: g ~ r^-1 iff nu -> y^-1/2 (KiDS Fig-3, 4 bins)
    """
    def __init__(self, footing="canonical"):
        self.footing = footing
        self.a0 = A0[footing]
        self.gals = load_sparc()
        self.gbar = np.concatenate([g["gbar"] for g in self.gals])
        self.gobs = np.concatenate([g["gobs"] for g in self.gals])
        self.gid = np.concatenate([np.full(len(g["gbar"]), i) for i, g in enumerate(self.gals)])
        # BTFR sample: quality discs with a measured V_flat
        self.btfr = [g for g in self.gals if g["Vflat"] > 0 and g["Mb"] > 0]
        # inner-diversity sample: galaxies whose curve brackets 2 kpc and have V_flat
        self.div = [g for g in self.gals if g["Vflat"] > 0 and g["r"].min() <= 2.0 <= g["r"].max()]
        # Renzo sample: galaxies with >= 8 points
        self.renzo = [g for g in self.gals if len(g["r"]) >= 8]
        # KiDS lensing rotation curves, 4 stellar-mass bins
        self.kids = []
        for i in (1, 2, 3, 4):
            R, ESD, e = load_esd(f"Fig-3_Lensing-rotation-curves_Massbin-{i}.txt")
            m = (R > 0.05) & (R < 2.6) & (ESD > 0)
            self.kids.append((R[m], 4*G_PC*ESD[m]*PC_PER_M, 4*G_PC*e[m]*PC_PER_M))

    # ---- the GENERAL interface: any modification is a predictor gpred(g_bar[SI], r[m]) -> g_pred[SI].
    #      A kernel modification is the special case gpred = nu(g_bar/a0) g_bar with no r dependence.
    @staticmethod
    def as_gpred(nuf, a0):
        def gp(gb, r):
            gb = np.asarray(gb, float)
            return np.asarray(nuf(gb/a0), float)*gb
        return gp

    # ---- the metrics
    def K1_K2(self, gp):
        rr = np.concatenate([g["r"] for g in self.gals])*kpc
        res = np.log10(self.gobs) - np.log10(gp(self.gbar, rr))
        return float(np.std(res)), float(np.median(res))

    def K3(self, gp):
        rr = np.concatenate([g["r"] for g in self.gals])*kpc
        m = self.gbar < 1e-11
        s, b, _ = fit_loglog(self.gbar[m], gp(self.gbar[m], rr[m]))
        return float(s)

    def K4(self, gp):
        """predicted v_flat at the outermost measured radius vs M_b; slope of log v^4 vs log M_b (predicted 1)."""
        Mb, v4 = [], []
        for g in self.btfr:
            i = np.argmax(g["r"]); gb = g["gbar"][i]; rr = g["r"][i]*kpc
            v = math.sqrt(float(np.asarray(gp(np.array([gb]), np.array([rr]))).ravel()[0])*rr)
            Mb.append(g["Mb"]); v4.append(v**4)
        Mb, v4 = np.asarray(Mb), np.asarray(v4)
        s, b, sc = fit_loglog(Mb, v4)
        return float(s), float((10.0**b)/(G*Msun)), float(sc)

    def K5(self, gp):
        """Renzo's rule at first order.  v^2 = g_pred r  =>  dln v/dln r = 1/2 [dln g_pred/dln r + 1].
        For a kernel that is dln g_pred/dln r = (1+n) dln g_bar/dln r with n = dln nu/dln y; computed here by
        differencing g_pred numerically so that ANY modification (including r-dependent ones) is handled.
        Regress the measured dln v_obs/dln r on that prediction; the framework predicts coefficient 1."""
        X, Y = [], []
        for g in self.renzo:
            r, vo, gb = g["r"], g["vobs"], g["gbar"]
            lr, lv = np.log(r), np.log(vo)
            dv = np.gradient(lv, lr)
            lgp = np.log(np.asarray(gp(gb, r*kpc), float))
            pred = 0.5*(np.gradient(lgp, lr) + 1.0)
            X.append(pred[1:-1]); Y.append(dv[1:-1])
        X, Y = np.concatenate(X), np.concatenate(Y)
        A = np.vstack([X, np.ones_like(X)]).T
        beta, c = np.linalg.lstsq(A, Y, rcond=None)[0]
        return float(beta), float(np.std(Y - (beta*X + c)))

    def K6(self, gp):
        po, pp = [], []
        for g in self.div:
            gb2 = float(np.interp(2.0, g["r"], g["gbar"]))
            vp = math.sqrt(float(np.asarray(gp(np.array([gb2]), np.array([2.0*kpc]))).ravel()[0])*2.0*kpc)/1e3
            po.append(float(np.interp(2.0, g["r"], g["vobs"]))/g["Vflat"]); pp.append(vp/g["Vflat"])
        po, pp = np.asarray(po), np.asarray(pp)
        return float(np.corrcoef(po, pp)[0, 1]), float(np.std(np.log10(po/pp)))

    def K7(self, gp):
        """The 1/r law.  For each KiDS mass bin, find the point mass whose modified prediction reproduces the
        innermost measured lensing acceleration, then measure the predicted log slope over 0.05-2.6 Mpc."""
        sl = []
        for R, g, e in self.kids:
            rr = R*Mpc
            M = g[0]*rr[0]**2/G
            for _ in range(200):
                pred = float(np.asarray(gp(np.array([G*M/rr[0]**2]), np.array([rr[0]]))).ravel()[0])
                M *= (g[0]/pred)**0.5
            gb = G*M/rr**2
            s, b, _ = fit_loglog(R, np.asarray(gp(gb, rr), float))
            sl.append(s)
        return float(np.mean(sl)), [float(x) for x in sl]

    def all_g(self, gp):
        k1, k2 = self.K1_K2(gp); k4s, k4a, k4sc = self.K4(gp); k5b, k5r = self.K5(gp)
        k6r, k6s = self.K6(gp); k7m, k7l = self.K7(gp)
        return dict(rar_rms=k1, rar_med=k2, tail_slope=self.K3(gp), btfr_slope=k4s, btfr_a0=k4a,
                    btfr_scatter=k4sc, renzo_beta=k5b, renzo_rms=k5r, div_r=k6r, div_rms=k6s,
                    lens_slope=k7m, lens_slopes=k7l)

    def all(self, nuf, a0=None):
        return self.all_g(self.as_gpred(nuf, a0 or self.a0))


KEEPER_TOL = dict(       # what counts as BREAKING a keeper.  Fixed before any modification was run.
    rar_rms=0.02,        # +0.02 dex on the RAR point scatter (18% of the 0.11 dex published RAR scatter)
    rar_med=0.05,        # a 0.05 dex systematic offset in the RAR
    tail_slope=0.05,     # the deep tail's 1/2 (item 25 measures 0.60 +- 0.07)
    btfr_slope=0.10,     # the BTFR's unit slope
    renzo_beta=0.20,     # Renzo's coefficient, measured 0.94 +- 0.13 against a predicted 1
    div_r=0.10,          # the inner-diversity correlation, baseline 0.79
    lens_slope=0.10,     # the lensing 1/r law, measured -1.10..-0.96
)


def keeper_verdict(base, new):
    """Which keepers a modification breaks, against the pre-fixed tolerances."""
    broken = []
    for k, tol in KEEPER_TOL.items():
        if abs(new[k] - base[k]) > tol:
            broken.append(f"{k}: {base[k]:+.3f} -> {new[k]:+.3f} (tol {tol})")
    return broken
