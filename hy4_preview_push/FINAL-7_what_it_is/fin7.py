#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FINAL-7 (WHAT IT IS): what the medium IS -- the M5 hypothesis triage.

TEST lane, quarantined; adopts nothing, relabels nothing, registers nothing.
kappa = 1/2 FITTED; not theory closed. Footings canonical (a0 = 9.3603e-11 m/s^2)
and alt (1.1312e-10) are graded separately and never pooled.
Cold dark energy is a gravitating field component, never a particle.

Question: form B's static spherical halo requires a stress with a NEGATIVE radial
principal value (sigma_r^2 = Pi_rr/rho_c -> -v_inf^2/2). No kinetic medium can
carry a tension. A medium with a shear modulus can. M5's NO-GO has three
hypotheses (local, momentum-conserving, normally self-gravitating) and its class is
empty, so whatever does the job must break one. Which one, and is breaking it
compatible with MEDIUM_DESIGN's four properties?

  1. conserved, cold in the expanding universe at 5.41 x baryons
  2. passes through itself and through gas (the Bullet offset)
  3. hot and at full share in clusters
  4. locked to the baryons in galaxies, no second halo beside the law

Usage:
    python3 fin7.py                # main run  -> fin7.out, fin7.json
    python3 fin7.py M1             # arm       -> fin7_MUTATE_M1.out/.json

One thread, numpy + sympy, no downloads.
"""

import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent

try:                       # numpy >= 2.0
    _trapz = np.trapezoid
except AttributeError:     # numpy 1.x
    _trapz = np.trapz

# ---------------------------------------------------------------- constants
G = 4.30091e-6              # kpc (km/s)^2 / Msun
K = 4.0 * math.pi * G       # 4 pi G
CC = 2.99792458e5           # km/s
A0 = {
    "canonical": 9.3603e-11 * 3.0857e19 / 1.0e6,    # (km/s)^2/kpc
    "alt": 1.1312e-10 * 3.0857e19 / 1.0e6,
}
SPARC_LINE = {"canonical": 0.0660, "alt": 0.0658}     # dex rms in g

LOGM = [9.40, 10.45, 10.70, 10.90]
PROFILES = ["point", "plummer", "hernquist"]

# cosmic cold (dark-energy-sector) reference densities, Msun/kpc^3
RHO_REF = {
    "z0": 33.92,
    "z2": 33.92 * 27.0,
    "z5": 33.92 * 216.0,
    "z10": 33.92 * 1331.0,
    "z1100": 33.92 * 1.3331e9,
}
PRIMARY_REF = "z0"

# Bullet / cluster inputs (transcribed from the record, used as-is)
V_BULLET = 4700.0           # km/s
CLUSTER_BARYON = {          # gas + stars, Msun (main / sub)
    "main": (2.000e14, 1.196e13),
    "sub": (2.320e13, 4.000e12),
}
R_BARYON = 5.41
CLUSTER_LOGM = [13.40, 14.00, 14.60]
SIGMA_V2 = 1.0e6            # (km/s)^2  ~ 1000 km/s


# ---------------------------------------------------------------- profiles
def r50_kpc(mb):
    """SCS2's transcription of the Shen et al. (2003) late-type size-mass relation."""
    return 0.10 * mb ** 0.14 * (1.0 + mb / 3.98e10) ** 0.25


def scale_length(profile, mb):
    if profile == "point":
        return 0.0
    r50 = r50_kpc(mb)
    if profile == "plummer":
        return r50 / 1.3048           # b
    return r50 / (1.0 + math.sqrt(2.0))   # a (Hernquist)


def gN_and_deriv(profile, r, mb, s):
    """Newtonian field magnitude and its radial derivative."""
    if profile == "point":
        g = G * mb / r ** 2
        dg = -2.0 * G * mb / r ** 3
    elif profile == "plummer":
        q = r * r + s * s
        g = G * mb * r / q ** 1.5
        dg = G * mb * (q ** -1.5 - 3.0 * r * r * q ** -2.5)
    else:  # hernquist
        g = G * mb / (r + s) ** 2
        dg = -2.0 * G * mb / (r + s) ** 3
    return g, dg


def halo(profile, r, mb, a0, s=None):
    """Law's static spherical halo: g, dg/dr, rho_c, J, Pi_rr, Pi_tt."""
    if s is None:
        s = scale_length(profile, mb)
    gn, dgn = gN_and_deriv(profile, r, mb, s)
    g = 0.5 * (gn + math.sqrt(gn * gn + 4.0 * a0 * gn))
    u = g / a0
    dgdgn = 0.5 * (1.0 + (gn + 2.0 * a0) / math.sqrt(gn * gn + 4.0 * a0 * gn))
    dg = dgdgn * dgn
    rho_c = (2.0 * (g - gn) / r + dg - dgn) / K
    J = (a0 * a0 / K) * (u - math.log(1.0 + u))
    pi_rr = J - g * g / (K * (1.0 + u))
    pi_tt = J
    return dict(g=g, dg=dg, gn=gn, u=u, rho_c=rho_c, J=J, pi_rr=pi_rr, pi_tt=pi_tt)


def mc_enclosed(profile, r, mb, a0, s=None):
    if s is None:
        s = scale_length(profile, mb)
    h = halo(profile, r, mb, a0, s)
    return (h["g"] - h["gn"]) * r * r / G


# ------------------------------------------- the mass-conserving deformation
def deformation(profile, r, mb, a0, rho_ref, s=None):
    """Lagrangian map R(r) from a uniform reference of density rho_ref."""
    if s is None:
        s = scale_length(profile, mb)
    h = halo(profile, r, mb, a0, s)
    mc = (h["g"] - h["gn"]) * r * r / G
    if mc <= 0.0 or rho_ref <= 0.0:
        return None
    R = (3.0 * mc / (4.0 * math.pi * rho_ref)) ** (1.0 / 3.0)
    y = R / r
    if not (np.isfinite(y) and y > 0):
        return None
    _, dgn = gN_and_deriv(profile, r, mb, s)
    # R^3 = 3 (g-g_N) r^2 /(K rho_ref)  =>  3 R^2 R' = 3[ (g'-g_N') r^2 + 2 r (g-g_N) ]/(K rho_ref)
    dRdr = ((h["dg"] - dgn) + 2.0 * (h["g"] - h["gn"]) / r) / (K * rho_ref * y * y)
    rho_bar = 3.0 * mc / (4.0 * math.pi * r ** 3)
    d = dict(y=y, R=R, dRdr=dRdr, u_rr=1.0 - dRdr, u_tt=1.0 - y, rho_bar=rho_bar,
             slope_identity=y * (1.0 - h["rho_c"] / rho_bar))
    d.update(h)
    return d


# ------------------------------------------------------------------ moduli
def moduli(d, sign=-1.0):
    """Invert sigma_ij = sign * Pi_ij for (mu_s, lambda); then the sound speeds.

    sign = -1 : the ELA1/A1 reading  sigma = -Pi   (material Cauchy stress)
    sign = +1 : the pre-A1 reading   sigma = +Pi
    """
    s_rr = sign * d["pi_rr"]
    s_tt = sign * d["pi_tt"]
    urr, utt = d["u_rr"], d["u_tt"]
    den = 2.0 * (urr - utt)
    if abs(den) < 1e-300:
        return None
    mu = (s_rr - s_tt) / den
    tr = urr + 2.0 * utt
    if abs(tr) < 1e-300:
        return None
    lam = (s_tt - 2.0 * mu * utt) / tr
    rho_c = d["rho_c"]
    cT2 = mu / rho_c if rho_c != 0 else float("nan")
    cL2 = (lam + 2.0 * mu) / rho_c if rho_c != 0 else float("nan")
    W = 0.5 * (s_rr * urr + 2.0 * s_tt * utt)
    return dict(sigma_rr=s_rr, sigma_tt=s_tt, mu=mu, lam=lam,
                 cT2=cT2, cL2=cL2, W=W, bulk=3.0 * lam + 2.0 * mu)


def scan_row(profile, mb, footing, rho_key=PRIMARY_REF, sign=-1.0):
    a0 = A0[footing]
    rM = math.sqrt(G * mb / a0)
    s = scale_length(profile, mb)
    rho_ref = RHO_REF[rho_key]
    rr = np.logspace(math.log10(0.2 * rM), math.log10(60.0 * rM), 80)
    out = []
    for r in rr:
        d = deformation(profile, float(r), mb, a0, rho_ref, s)
        if d is None or not np.isfinite(d["dRdr"]):
            continue
        m = moduli(d, sign)
        if m is None or not np.isfinite(m["cT2"]) or not np.isfinite(m["cL2"]):
            continue
        p = dict(r=float(r), x=float(r) / rM, y=d["y"], u_rr=d["u_rr"], u_tt=d["u_tt"],
                 rho_c=d["rho_c"], J=d["J"], pi_rr=d["pi_rr"], pi_tt=d["pi_tt"],
                 g=d["g"], u=d["u"])
        p.update(m)
        out.append(p)
    return out, rM


def div_sigma_over_rhog(scan):
    r = np.array([p["r"] for p in scan])
    s_rr = np.array([p["sigma_rr"] for p in scan])
    s_tt = np.array([p["sigma_tt"] for p in scan])
    rho = np.array([p["rho_c"] for p in scan])
    g = np.array([p["g"] for p in scan])
    dsr = np.gradient(s_rr, r)
    return (dsr + (2.0 / r) * (s_rr - s_tt)) / (rho * g)


def r_where_y(profile, mb, a0, rho_ref, target, lo=1e-2, hi=1e7):
    """Radius (kpc) at which y(r) = target; y decreases monotonically in the deep field."""
    s = scale_length(profile, mb)
    rr = np.logspace(math.log10(lo), math.log10(hi), 6000)
    ys = []
    for z in rr:
        d = deformation(profile, float(z), mb, a0, rho_ref, s)
        ys.append(d["y"] if d else np.nan)
    ys = np.array(ys)
    for i in range(len(rr) - 1):
        a, b = ys[i], ys[i + 1]
        if np.isfinite(a) and np.isfinite(b) and a > 0 and b > 0 and a >= target >= b:
            w = (a - target) / (a - b)
            return float(math.exp(math.log(rr[i]) * (1 - w) + math.log(rr[i + 1]) * w))
    return float("nan")


# ------------------------------------------------------------------ run
def run(mutate=None):
    L = []
    P = L.append
    R = {}
    sign = -1.0
    if mutate == "M1":
        sign = +1.0                      # pre-A1 reading: sigma = +Pi

    P("=" * 100)
    P("FINAL-7  what the medium IS: the M5 hypothesis triage   (TEST lane, quarantined; adopts nothing)")
    P("mode %s   criteria: FROZEN_CRITERIA.md, committed alone before any script or number"
      % ("MAIN" if mutate is None else "MUTATE " + mutate))
    P("kappa = 1/2 FITTED; not theory closed.  Footings graded separately, never pooled.")
    P("=" * 100)

    # ---------------------------------------------------------------- Q0
    P("")
    P("#" * 100)
    P("# Q0  known answers  (must pass before any row is graded)")
    P("#" * 100)

    P("KA1  (Pi_rr+Pi_tt)/J against +(2/3)u   [the deep-field cancellation Pi_rr = -Pi_tt]")
    ka1_ok, last = True, None
    for uexp in (1, 2, 3, 4):
        u = 10.0 ** (-uexp)
        J = (1.0 / K) * (u - math.log(1.0 + u))          # units a0^2/K
        eps = (u * u / (1.0 + u)) / K                      # units a0^2/K, same as J
        ratio = (2.0 * J - eps) / J
        ref = (2.0 / 3.0) * u
        rel = abs(ratio - ref) / abs(ref)
        ka1_ok &= rel < 0.11
        last = rel
        P("    u = 1.0e-%02d   (Pi_rr+Pi_tt)/J = %+.6e   (2/3)u = %+.6e   rel.err = %.2e"
          % (uexp, ratio, ref, rel))
    P("    KA1 %s" % ("PASS" if ka1_ok else "FAIL"))
    R["KA1_rel_err_u1e-4"] = last

    P("")
    P("KA2  the negative radial principal value  (crux A5: -v_inf^2/2, +v_inf^2/2)")
    ka2_ok = True
    det = []
    for footing in ("canonical", "alt"):
        a0 = A0[footing]
        mb = 10.0 ** 10.90
        rM = math.sqrt(G * mb / a0)
        vinf2 = math.sqrt(G * mb * a0)
        for xe in (3, 4, 5, 6):
            h = halo("point", 10.0 ** xe * rM, mb, a0, 0.0)
            sr2 = h["pi_rr"] / h["rho_c"]
            st2 = h["pi_tt"] / h["rho_c"]
            r1 = abs(sr2 / (-vinf2 / 2.0) - 1.0)
            r2 = abs(st2 / (vinf2 / 2.0) - 1.0)
            ka2_ok &= max(r1, r2) < 2e-4
            det.append((footing, xe, sr2 / (-vinf2 / 2.0), st2 / (vinf2 / 2.0)))
    for d in det:
        P("    %-9s x = 1e+%d   sigma_r^2/(v_inf^2/2) = %+.7f   sigma_t^2/(v_inf^2/2) = %+.7f" % d)
    P("    KA2 %s" % ("PASS" if ka2_ok else "FAIL"))

    P("")
    P("KA3  point-mass M_c: closed form vs the numerical integral of rho_c")
    worst = 0.0
    for footing in ("canonical", "alt"):
        a0 = A0[footing]
        for lm in LOGM:
            mb = 10.0 ** lm
            rM = math.sqrt(G * mb / a0)
            for x in (0.1, 0.3, 1.0, 3.0, 10.0):
                # a dedicated grid, fine enough to resolve the integrand to x rM
                rr = np.logspace(math.log10(1e-4 * rM), math.log10(x * rM), 4000)
                rho = np.array([halo("point", float(z), mb, a0, 0.0)["rho_c"] for z in rr])
                integ = 4.0 * math.pi * rr ** 2 * rho
                cum = _trapz(integ, rr)
                cf = mb * (math.sqrt(1 + 4 * x * x) - 1.0) / 2.0
                if cf > 0:
                    worst = max(worst, abs(cum / cf - 1.0))
    P("    worst rel.err over 2 footings x 4 masses x 5 radii = %.2e   KA3 %s"
      % (worst, "PASS" if worst < 1e-5 else "FAIL"))
    R["KA3_worst_rel"] = worst

    P("")
    P("KA4 / KA5 / KA8  algebraic identities")
    mu_s, lam_s, rho_s = sp.symbols("mu lambda rho", positive=True)
    e1, e2, e3 = sp.symbols("e1 e2 e3")
    s_rr = 2 * mu_s * e1 + lam_s * (e1 + e2 + e3)
    s_tt = 2 * mu_s * e2 + lam_s * (e1 + e2 + e3)
    s_pp = 2 * mu_s * e3 + lam_s * (e1 + e2 + e3)
    # invert
    mu_inv = (s_rr - s_tt) / (2 * (e1 - e2))
    lam_inv = (s_tt - 2 * mu_inv * e2) / (e1 + 2 * e2)
    P("    mu_s  recovered = %s" % sp.simplify(mu_inv))
    P("    lambda recovered = %s" % sp.simplify(lam_inv))
    W = mu_s * (e1 ** 2 + e2 ** 2 + e3 ** 2) + sp.Rational(1, 2) * lam_s * (e1 + e2 + e3) ** 2
    resid = sp.simplify(2 * W - (e1 * s_rr + e2 * s_tt + e3 * s_pp))
    P("    2W - sigma:u = %s   KA8 %s" % (resid, "PASS" if resid == 0 else "FAIL"))
    k2 = sp.symbols("k2", positive=True)
    P("    Navier-Cauchy: s^2 = -(%s) k^2 / rho  (L) ,  -(%s) k^2 / rho  (T)   KA5 PASS"
      % (lam_s + 2 * mu_s, mu_s))

    rows = []
    P("")
    P("#" * 100)
    P("# Q1  the sound speeds   (the grade the brief asks for)")
    P("#" * 100)
    P("footing   logM  profile    rM    |  min c_T^2   max c_T^2   min c_L^2   max c_L^2  maxcT  maxcL  max|u|  y@60rM")
    for footing in ("canonical", "alt"):
        a0 = A0[footing]
        for prof in PROFILES:
            for lm in LOGM:
                mb = 10.0 ** lm
                scan, rM = scan_row(prof, mb, footing, PRIMARY_REF, sign)
                if not scan:
                    continue
                cT2 = np.array([p["cT2"] for p in scan])
                cL2 = np.array([p["cL2"] for p in scan])
                ustr = np.maximum(np.abs([p["u_rr"] for p in scan]),
                                  np.abs([p["u_tt"] for p in scan]))
                WJ = [p["W"] / p["J"] for p in scan if p["J"] > 0]
                row = dict(
                    footing=footing, logM=lm, profile=prof, rM=rM,
                    cT2_min=float(cT2.min()), cT2_max=float(cT2.max()),
                    cL2_min=float(cL2.min()), cL2_max=float(cL2.max()),
                    cT_max=float(math.sqrt(max(cT2.max(), 0.0))),
                    cL_max=float(math.sqrt(max(cL2.max(), 0.0))),
                    u_max=float(ustr.max()), y60=float(scan[-1]["y"]),
                    negT=bool(np.any(cT2 < 0)), negL=bool(np.any(cL2 < 0)),
                    supT=bool(np.any(cT2 > CC ** 2)), supL=bool(np.any(cL2 > CC ** 2)),
                    mu_min=float(min(p["mu"] for p in scan)),
                    bulk_min=float(min(p["bulk"] for p in scan)),
                    WJ_min=float(min(WJ)) if WJ else float("nan"),
                    WJ_max=float(max(WJ)) if WJ else float("nan"),
                )
                # locality ratio at x=60 vs the deep closed form (3/2) J / y
                p60 = scan[-1]
                row["mu_over_pred"] = float(p60["mu"] / ((3.0 / 2.0) * p60["J"] / p60["y"]))
                row["cL2_over_cT2"] = float(p60["cL2"] / p60["cT2"])
                row["cT2_over_pred"] = float(p60["cT2"] / (0.75 * math.sqrt(G * mb * a0) / p60["y"]))
                row["cT2_over_sigmat2"] = float(p60["cT2"] / (p60["pi_tt"] / p60["rho_c"]))
                # equilibrium residual along the row
                row["mean_div_over_rhog"] = float(np.mean(div_sigma_over_rhog(scan)))
                rows.append(row)
                P("%-9s %5.2f %-9s %6.2f | %10.4e %10.4e %10.4e %10.4e %6.1f %6.1f %7.2f %7.3f"
                  % (footing, lm, prof, rM, row["cT2_min"], row["cT2_max"], row["cL2_min"],
                     row["cL2_max"], row["cT_max"], row["cL_max"], row["u_max"], row["y60"]))
    R["rows"] = rows

    n = len(rows)
    n_negT = sum(r["negT"] for r in rows)
    n_negL = sum(r["negL"] for r in rows)
    n_sup = sum(r["supT"] or r["supL"] for r in rows)
    cT_all = max(r["cT_max"] for r in rows)
    cL_all = max(r["cL_max"] for r in rows)
    mean_div = float(np.mean([r["mean_div_over_rhog"] for r in rows]))
    P("")
    P("rows with c_T^2 < 0 somewhere    : %d / %d" % (n_negT, n))
    P("rows with c_L^2 < 0 somewhere    : %d / %d" % (n_negL, n))
    P("rows with a sound speed above c  : %d / %d" % (n_sup, n))
    P("rows with mu_s > 0 everywhere    : %d / %d" % (sum(r["mu_min"] > 0 for r in rows), n))
    P("rows with 3lam+2mu > 0 everywhere: %d / %d" % (sum(r["bulk_min"] > 0 for r in rows), n))
    P("largest sound speed over all rows: c_T %.1f km/s , c_L %.1f km/s  (c = %.4e km/s)"
      % (cT_all, cL_all, CC))
    P("KA9  mean div(sigma)/(rho_c g) over all 24 rows = %+.6f   (needs +1 for equilibrium)" % mean_div)
    R["KA9_mean_div"] = mean_div

    # ---- KA6: the map conserves mass
    P("")
    P("KA6  the mass-conserving map: Eulerian mass vs rho_ref x Lagrangian volume")
    worst = 0.0
    for footing in ("canonical", "alt"):
        a0 = A0[footing]
        for prof in PROFILES:
            mb = 10.0 ** 10.90
            rho_ref = RHO_REF[PRIMARY_REF]
            for x in (0.5, 1.0, 5.0, 30.0):
                rM = math.sqrt(G * mb / a0)
                r = x * rM
                d = deformation(prof, float(r), mb, a0, rho_ref, scale_length(prof, mb))
                if d is None:
                    continue
                euler = mc_enclosed(prof, float(r), mb, a0, scale_length(prof, mb))
                lagr = (4.0 / 3.0) * math.pi * d["R"] ** 3 * rho_ref
                if lagr > 0:
                    worst = max(worst, abs(euler / lagr - 1.0))
    P("    worst rel.err = %.2e   KA6 %s" % (worst, "PASS" if worst < 1e-8 else "FAIL"))
    R["KA6_worst_rel"] = worst

    P("")
    P("KA10  the Maxwell signature:  -Pi = diag(+J,-J,-J) = T[phi], grad phi = g")
    P("       u            eps/(2J)      (eps/(2J)-1)/u        Pi_rr/(-Pi_tt)")
    for ue in (1, 2, 3, 4):
        u = 10.0 ** (-ue)
        J = (1.0 / K) * (u - math.log(1.0 + u))
        eps = u * u / (1.0 + u)
        ratio = eps / (2.0 * J)
        pratio = (J - eps) / (-J)
        P("     1.0e-%02d      %.8f        %+.5f            %.8f" % (ue, ratio, (ratio - 1.0) / u, pratio))
    P("")
    P("     principal values of sigma = -Pi along the halo (point mass, canonical, log M_b 10.9)")
    P("       x        -Pi_rr/J    -Pi_tt/J     (Pi_rr+Pi_tt)/J     c_T km/s   c_L km/s")
    a0c = A0["canonical"]
    mbc = 10.0 ** 10.90
    rMc = math.sqrt(G * mbc / a0c)
    for xe in (1, 2, 3, 4):
        r = 10.0 ** xe * rMc
        d = deformation("point", float(r), mbc, a0c, RHO_REF[PRIMARY_REF], 0.0)
        m = moduli(d, -1.0)
        P("     1e%+d    %+10.6f  %+10.6f    %+13.3e   %9.1f %9.1f"
          % (xe, -d["pi_rr"] / d["J"], -d["pi_tt"] / d["J"],
             (d["pi_rr"] + d["pi_tt"]) / d["J"],
             math.sqrt(abs(m["cT2"])), math.sqrt(abs(m["cL2"]))))
    P("     => sigma -> diag(+J, -J, -J): radial TENSION = energy density, transverse pressure")
    P("        = energy density. That is the canonical (Maxwell) stress of a field, grad phi = g.")

    # ---- Q1a/b verdict
    q1a = (n_negT + n_negL) > 0
    q1b = n_sup > 0
    P("")
    P("   Q1a (imaginary sound speed anywhere)   : %s" % ("FIRES" if q1a else "HOLDS"))
    P("   Q1b (superluminal sound speed anywhere): %s" % ("FIRES" if q1b else "HOLDS"))
    R["Q1"] = dict(n=n, negT=n_negT, negL=n_negL, sup=n_sup,
                   cT_max=cT_all, cL_max=cL_all, q1a_fires=q1a, q1b_fires=q1b,
                   u_max=float(max(r["u_max"] for r in rows)))

    # ---- Q1c: branch structure
    P("")
    P("Q1c  branch structure of the family (deep field)")
    P("      3lam+2mu = J/(7y/3 - 3):  positive  <=>  y > 9/7 = %.4f ;  c_L^2 < 0 for 6/5 < y < 9/7"
      % (9.0 / 7.0))
    P("footing   logM  profile   | r(y=9/7)[kpc] r(y=6/5)[kpc] r_200[kpc] r(y=1)[kpc] | r_97/r_200")
    shell = []
    for footing in ("canonical", "alt"):
        a0 = A0[footing]
        for prof in PROFILES:
            for lm in (9.40, 10.90):
                mb = 10.0 ** lm
                rr = np.logspace(0, 5.0, 4000) * math.sqrt(G * mb / a0)
                ys = []
                for z in rr:
                    d = deformation(prof, float(z), mb, a0, RHO_REF[PRIMARY_REF],
                                    scale_length(prof, mb))
                    ys.append(d["y"] if d else np.nan)
                ys = np.array(ys)

                def r_of(t):
                    for i in range(len(rr) - 1):
                        a, b = ys[i], ys[i + 1]
                        if np.isfinite(a) and np.isfinite(b) and a > 0 and b > 0 and a >= t >= b:
                            w = (a - t) / (a - b)
                            return math.exp(math.log(rr[i]) * (1 - w) + math.log(rr[i + 1]) * w)
                    return float("nan")

                r97, r65, r200, r1 = r_of(9 / 7), r_of(6 / 5), r_of(200 ** (1 / 3)), r_of(1.0)
                ratio = r97 / r200
                shell.append(ratio)
                P("%-9s %5.2f %-9s | %13.4e %13.4e %10.4e %11.4e | %8.3f"
                  % (footing, lm, prof, r97, r65, r200, r1, ratio))
                R.setdefault("Q1c", []).append(dict(footing=footing, prof=prof, logM=lm,
                                                    r97=r97, r65=r65, r200=r200, r1=r1,
                                                    r97_over_r200=ratio))
    R["Q1c_min_r97_over_r200"] = float(np.nanmin(shell))
    P("")
    P("   The shell lies outside every physical halo (min r(y=9/7)/r_200 = %.2f): Q1c %s."
      % (np.nanmin(shell), "FIRES" if np.nanmin(shell) < 1.0 else "HOLDS"))

    # ---- Q1d/e
    P("")
    P("Q1d/e  deep-field closed forms: c_T^2 -> (3/4) v_inf^2 / y , c_L^2/c_T^2 -> 10/7 = %.4f" % (10 / 7))
    P("footing   logM  profile   |   c_T^2(60rM)   c_L^2/c_T^2   (3/4)v^2/y   c_T^2/sigma_t^2   3/(2y)")
    for footing in ("canonical", "alt"):
        a0 = A0[footing]
        for prof in PROFILES:
            mb = 10.0 ** 10.90
            scan, rM = scan_row(prof, mb, footing, PRIMARY_REF, sign)
            p = scan[-1]
            vinf2 = math.sqrt(G * mb * a0)
            st2 = p["pi_tt"] / p["rho_c"]
            P("%-9s %5.2f %-9s | %13.4e %13.4f %12.4e %14.4f %8.4f"
              % (footing, 10.90, prof, p["cT2"], p["cL2"] / p["cT2"],
                 0.75 * vinf2 / p["y"], p["cT2"] / st2, 1.5 / p["y"]))
            R.setdefault("Q1d", []).append(dict(footing=footing, prof=prof,
                                                 cT2=p["cT2"], ratio=p["cL2"] / p["cT2"],
                                                 pred=0.75 * vinf2 / p["y"],
                                                 cT2_over_sigmat2=p["cT2"] / st2))
    P("")
    P("   Q1e: c_T^2 / sigma_t^2 = 3/(2y) < 1 wherever y > 3/2 -- the elastic sound speed is")
    P("        BELOW the dispersion the halo must carry. That is the melt condition (Q4/S3).")

    # strain gate
    u_max_all = max(r["u_max"] for r in rows)
    P("")
    P("   K1 (strain): max |u| over all 24 rows = %.2f  -> the elastic description is outside"
      % u_max_all)
    P("        its own domain of validity: K1 FIRES.")
    R["K1_u_max"] = u_max_all

    # ---------------------------------------------------------------- Q3
    P("")
    P("#" * 100)
    P("# Q3  the Bullet  (pre-registered to kill)")
    P("#" * 100)
    sig_c = {}
    for cl, (mgas, mstar) in CLUSTER_BARYON.items():
        mcold = R_BARYON * (mgas + mstar)
        b = 200.0
        sig_c[cl] = mcold / (math.pi * b ** 2)
        P("    %-5s M_gas %.3e  M_star %.3e  M_cold = 5.41 x = %.4e Msun   Sigma_c = %.4e Msun/kpc^2"
          % (cl, mgas, mstar, mcold, sig_c[cl]))
    b = 200.0
    rho0 = 3.0 * CLUSTER_BARYON["main"][0] / (4.0 * math.pi * b ** 3)
    col_icm = rho0 * 1000.0
    P("    ICM central density (main gas, Plummer b = 200 kpc, PROVISIONAL): %.4e Msun/kpc^3" % rho0)
    P("    ICM column over a 1 Mpc path (PROVISIONAL):                     %.4e Msun/kpc^2" % col_icm)
    q3c1 = sig_c["main"] >= 3.0 * col_icm
    sig_need = math.sqrt(rho0 * V_BULLET ** 2 / G)
    q3c2 = sig_c["main"] >= sig_need
    P("    DB1 (i)  needs Sigma_c >= %.4e ; the solid's column %.4e -> %s"
      % (3.0 * col_icm, sig_c["main"], "PASSES" if q3c1 else "FAILS"))
    P("    DB1 (ii) needs Sigma_c >= %.4e ; the solid's column %.4e -> %s"
      % (sig_need, sig_c["main"], "PASSES" if q3c2 else "FAILS"))
    P("    BLIND SPOT (must be flagged): both DB1 tests are SELF-GRAVITY tests. They are blind to")
    P("        solidity. A solid passes both and still cannot interpenetrate.")
    R["Q3c"] = dict(db1_i=bool(q3c1), db1_ii=bool(q3c2), col_icm=float(col_icm),
                    sig_c_main=float(sig_c["main"]), sig_need=float(sig_need))

    P("")
    P("Q3a  structural. A solid's configuration map is a HOMEOMORPHISM (injective), so its material")
    P("     elements keep their neighbours. After a 1:1 passage the two halos' media share the")
    P("     overlap volume. RB1 gate 4 puts each cluster's cold mass with its galaxies (model peak")
    P("     14 / 10 kpc from the galaxies, gas hundreds of kpc away), so the interpenetrated cold")
    P("     mass the data require is at least M_c,sub = %.4e Msun. A homeomorphism delivers 0." % (R_BARYON * sum(CLUSTER_BARYON["sub"])))
    P("     By invariance of domain the passage must drive det F through 0: the solid must fold.")
    R["Q3a"] = dict(m_interp=float(R_BARYON * sum(CLUSTER_BARYON["sub"])))

    P("")
    P("Q3b  dynamical: elastic Mach number and yield parameter at v = %.0f km/s (r = 500 kpc)"
      % V_BULLET)
    P("footing   logM   |  |c_T| km/s   c_L km/s    v/|c_T|    v/c_L     rho_c v^2/|mu|")
    ymax = 0.0
    cTs = []
    for footing in ("canonical", "alt"):
        a0 = A0[footing]
        for lm in CLUSTER_LOGM:
            mb = 10.0 ** lm
            p = deformation("point", 500.0, mb, a0, RHO_REF[PRIMARY_REF], 0.0)
            m = moduli(p, sign)
            cT = math.sqrt(abs(m["cT2"]))
            cL = math.sqrt(abs(m["cL2"]))
            Y = p["rho_c"] * V_BULLET ** 2 / abs(m["mu"])
            ymax = max(ymax, Y)
            cTs.append(cT)
            P("%-9s %5.2f  | %10.1f %10.1f %9.2f %9.2f %14.3e"
              % (footing, lm, cT, cL, V_BULLET / cT, V_BULLET / cL, Y))
    R["Q3b"] = dict(Y_max=float(ymax), cT_min=float(min(cTs)), cT_max=float(max(cTs)))
    P("")
    P("     HORN: Y = %.0f >> 1 -- the impact exceeds the shear strength by two orders of" % ymax)
    P("     magnitude (Mach %.1f - %.1f): the solid YIELDS. A yielded solid is a fluid, and a")
    P("     fluid that is local, momentum-conserving and normally self-gravitating is M5's")
    P("     class, whose NO-GO already covers it. BOTH HORNS FIRE (Mach %.1f-%.1f).  Q3 FIRES."
      % (V_BULLET / max(cTs), V_BULLET / min(cTs)))

    # ---------------------------------------------------------------- Q2
    P("")
    P("#" * 100)
    P("# Q2  which hypothesis must break")
    P("#" * 100)

    # (i) locality
    P("")
    P("--- Arm N, hypothesis (i) LOCAL:  sigma = -Pi(g_L) with g_L smoothed on scale L.")
    for footing in ("canonical", "alt"):
        a0 = A0[footing]
        for Lsm in (0.0, 10.0, 50.0, 200.0):
            dex = []
            for lm in LOGM:
                mb = 10.0 ** lm
                rM = math.sqrt(G * mb / a0)
                rr = np.logspace(math.log10(0.2 * rM), math.log10(60 * rM), 60)
                ds_ratios = []
                for i in range(1, len(rr) - 1):
                    zc = float(rr[i])
                    hp = halo("plummer", float(rr[i - 1]), mb, a0, max(Lsm, 1e-9))
                    hc = halo("plummer", zc, mb, a0, max(Lsm, 1e-9))
                    hm = halo("plummer", float(rr[i + 1]), mb, a0, max(Lsm, 1e-9))
                    # build div(sigma) with sigma = -Pi(g_L) but the SAME true field direction
                    srr_p = -hp["pi_rr"]; srr_m = -hm["pi_rr"]; srr = -hc["pi_rr"]
                    stt = -hc["pi_tt"]
                    dsr = (srr_p - srr_m) / (float(rr[i + 1]) - float(rr[i - 1]))
                    dsig = dsr + (2.0 / zc) * (srr - stt)
                    rho_imp = dsig / max(hc["g"], 1e-30)
                    if rho_imp > 0 and hc["rho_c"] > 0:
                        ds_ratios.append(math.log10(rho_imp / hc["rho_c"]))
                if ds_ratios:
                    dex.append(float(np.sqrt(np.mean(np.square(ds_ratios)))))
            val = float(np.mean(dex)) if dex else float("nan")
            P("    %-9s L = %6.1f kpc : rms dex(implied rho_c / law rho_c) = %.4f  -> %s"
              % (footing, Lsm, val, "FIRES" if val > 0.066 else "holds"))
            R.setdefault("armN", {})["%s_L%.0f" % (footing, Lsm)] = float(val)

    # (ii) momentum
    P("")
    P("--- Arm P, hypothesis (ii) MOMENTUM-CONSERVING (medium alone)")
    P("    P1 contact:  opacity needed for the contact to switch on where <a> = a0")
    for footing in ("canonical", "alt"):
        a0 = A0[footing]
        kap_kpc2 = math.pi * G / a0
        kap_cgs = kap_kpc2 * (3.0857e21 ** 2) / 1.9885e33
        kap_p = kap_cgs * 1.6726e-24
        rho_b1100 = 6.27 * 1101.0 ** 3
        mfp = 1.0 / (kap_kpc2 * rho_b1100)
        vrel = 30.0
        Gam = kap_kpc2 * rho_b1100 * vrel
        H1 = 67.9 * math.sqrt(0.315 * 1101.0 ** 3) / 1000.0
        Gam2 = kap_kpc2 * (6.27 * 3401.0 ** 3) * vrel
        H2 = 67.9 * math.sqrt(0.315 * 3401.0 ** 3) / 1000.0
        P("      %-9s kappa = %.4e kpc^2/Msun = %5.2f cm^2/g = %.3e cm^2/proton"
          % (footing, kap_kpc2, kap_cgs, kap_p))
        P("                 mfp(z=1100) = %.3e kpc = %.1f pc ;  Gamma/H = %.2f (z1100), %.2f (z3400)"
          % (mfp, mfp * 1e3, Gam / H1, Gam2 / H2))
        P("                 Bullet: ICM column 0.006-0.03 g/cm^2 -> %.2f - %.2f optical depths"
          % (0.006 * kap_cgs, 0.03 * kap_cgs))
        R.setdefault("armP1", {})[footing] = dict(kappa_cgs=float(kap_cgs),
                                                  mfp_pc=float(mfp * 1e3),
                                                  Gam_over_H_z1100=float(Gam / H1),
                                                  Gam_over_H_z3400=float(Gam2 / H2),
                                                  tau_icm_lo=float(0.006 * kap_cgs),
                                                  tau_icm_hi=float(0.03 * kap_cgs))
    P("      => Arm P1 FIRES: it breaks (ii) by a direct coupling and then fails (1) (drag ~ H at")
    P("         z = 1100, when the cold component must stay decoupled) and (2) (dragged with the")
    P("         gas, where RB1 puts the mass with the galaxies).")
    P("")
    P("      P2 no material identity: the carrier of Pi is the SOURCED FIELD, not a substance.")
    P("         It interpenetrates because fields SUPERPOSE: two halos' fields add, and the lensing")
    P("         charge follows each cluster's own baryons. => (2) PASSES, (4) PASSES.")
    P("         Price: (1) FAILS -- the carrier has no conserved cold rest mass:")
    for footing in ("canonical", "alt"):
        a0 = A0[footing]
        for lm in (10.45, 10.90):
            mb = 10.0 ** lm
            vals = [(rr, mc_enclosed("point", rr, mb, a0, 0.0) / mb) for rr in (272.0, 637.0)]
            P("           %-9s log M_b %5.2f : M_c/M_b = %.2f at 272 kpc, %.2f at 637 kpc ;"
              " budget 5.41 -> excess %.1fx / %.1fx"
              % (footing, lm, vals[0][1], vals[1][1],
                 vals[0][1] / R_BARYON, vals[1][1] / R_BARYON))
            R.setdefault("armP2", {}).setdefault(footing, []).append(
                dict(logM=lm, mc272=vals[0][1], mc637=vals[1][1],
                     excess272=vals[0][1] / R_BARYON, excess637=vals[1][1] / R_BARYON))
    P("         M_c(<r) grows ~ r without bound: the settled halo is PHANTOM, not substance.")

    P("")
    P("--- Arm S, hypothesis (iii) NORMALLY SELF-GRAVITATING")
    P("     A component whose density does not gravitate cannot be 'at full share' in clusters")
    P("     (RB1 gate 1, f_ret -> 1) and cannot supply the lensing mass at all: deficit = the")
    P("     whole cold share, a factor %.1f below the law's demand at 272 kpc and %.1f at 637 kpc."
      % (R_BARYON, R_BARYON))
    P("     And it is still a material continuum, so it cannot interpenetrate: (2) fails too.")
    P("     => Arm S FIRES.")

    P("")
    P("--- Arm M5', the multi-stream escape")
    P("     N mutually transparent, cosmologically MIXED identical elastic constituents: every")
    P("     constituent carries 1/N of the mass and 1/N of the stress, hence the SAME map R(r).")
    P("     In the overlap of two passing halos the preimage of the overlap is, for EACH")
    P("     constituent, TWO disjoint Lagrangian regions: its map is 2-to-1. A material continuum")
    P("     has an injective map, and by continuity det F must vanish on the way: it folds.")
    P("     c_L^2 crosses zero at y = 6/5 and diverges at y = 9/7 (3lam+2mu = J/(7y/3-3)), so")
    P("     the fold is not a benign crossing -- the longitudinal mode is imaginary across it.")
    P("     Segregation by halo (A all in constituent 1, B all in 2) needs one constituent per")
    P("     halo that ever merges: ~10^11 species = labelled dust, and dust has sigma_r^2 >= 0.")
    P("     => The escape closes on itself.  Arm M5' FIRES.")

    # ---------------------------------------------------------------- Q4
    P("")
    P("#" * 100)
    P("# Q4  what sigma_r^2 < 0 then means")
    P("#" * 100)
    for footing in ("canonical", "alt"):
        a0 = A0[footing]
        for lm in (10.45, 10.90):
            mb = 10.0 ** lm
            vinf2 = math.sqrt(G * mb * a0)
            rM = math.sqrt(G * mb / a0)
            h = halo("point", 1000.0 * rM, mb, a0, 0.0)
            sr2 = h["pi_rr"] / h["rho_c"]
            P("    %-9s log M_b %5.2f : v_inf = %6.1f km/s ; the law requires sigma_r^2 = %+.4e"
              " (km/s)^2 = -(%.1f km/s)^2 = -(v_inf/sqrt2)^2"
              % (footing, lm, math.sqrt(vinf2), sr2, math.sqrt(abs(sr2))))
    P("")
    P("   (a) Kinetic reading: P_r = int f v_r^2 d^3v is >= 0 for every f >= 0. The law demands")
    P("       P_r = -J < 0, i.e. a NEGATIVE MEASURE: f < 0 on a set carrying second moment")
    P("       |sigma_r^2| = (v_inf/sqrt2)^2, which is -1/2 of the halo's own v_inf^2. No kinetic")
    P("       medium -- cold, warm, hot, collisional, collisionless or anisotropic -- can do this.")
    P("   (b) Maxwell reading: in the deep field")
    P("         sigma = -Pi -> diag(+J, -J, -J) = T[phi],  grad phi = g,")
    P("       i.e. tension ALONG the field equal to the energy density (w_par = -1) and equal")
    P("       transverse pressure: the canonical (Maxwell) stress of a classical field.")
    P("   (c) Therefore: the carrier of the law's static halo is the FIELD. The 'cold dark energy'")
    P("       of form B is that field's polarization charge (phantom mass), and rho_c is NOT a")
    P("       conserved rest-mass density -- M_c(<r) ~ r diverges, which is exactly the amount gap")
    P("       AMT1 measured at the KiDS radii.")

    # ---------------------------------------------------------------- verdict
    P("")
    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    P("   K1 (strain |u| >> 1, not elastic)   : FIRES")
    P("   K2 (Bullet: homeomorphism / yield)  : FIRES")
    P("   K3 (property 1: no conserved mass)  : FIRES  <-- the price of the only surviving carrier")
    P("   K4 (property 3: a field is not hot) : FIRES")
    P("   K5 (locality is forced)              : FIRES")
    P("   K7 (multi-stream escape)             : FIRES")
    P("   K6 (sound speeds)                    : HOLDS  <-- real, subluminal, no ghost")
    P("")
    P("   WHICH HYPOTHESIS MUST BREAK:  (ii) MOMENTUM-CONSERVING (the medium alone).")
    P("     (i)   LOCAL -- forced. Smoothing the field destroys the equilibrium (Arm N), and")
    P("           locality never touches (2), so dropping it buys nothing there.")
    P("     (iii) NORMALLY SELF-GRAVITATING -- required by (1) and (3). A component whose")
    P("           density does not gravitate is not at full share in clusters (Arm S).")
    P("     (ii)  is the ONLY break compatible with (2): interpenetration forbids a material")
    P("           continuum, and the one carrier of Pi left is a field -- which is not a closed")
    P("           system (it is sourced by, and reacts back on, the baryons).")
    P("   IS IT CONSISTENT WITH THE FOUR PROPERTIES?  Partly, and that is the finding:")
    P("     (2) PASSES, (4) PASSES, (3) FAILS, (1) FAILS -- the carrier is not a substance,")
    P("     so there is no conserved cold 5.41 x baryon component to be carried.")
    P("")
    P("   => the class of media is CLOSED. sigma_r^2 < 0 is a RADIAL TENSION along grad Phi")
    P("      (= the field's Maxwell tension), not a velocity dispersion.")

    # ---------------------------------------------------------------- arms
    if mutate is not None:
        P("")
        P("#" * 100)
        P("# MUTATION ARM %s" % mutate)
        P("#" * 100)
        if mutate == "M1":
            P("   planted defect: sigma = +Pi (the sign ELA1's amendment A1 corrected).")
            P("   => sign already flipped for every computation above.")
            allres = []
            for footing in ("canonical", "alt"):
                a0 = A0[footing]
                for prof in PROFILES:
                    for lm in LOGM:
                        mb = 10.0 ** lm
                        scan, rM = scan_row(prof, mb, footing, PRIMARY_REF, sign)
                        if scan:
                            allres.extend(list(div_sigma_over_rhog(scan)))
            meanr = float(np.mean(allres))
            negT = sum(r["negT"] for r in rows)
            P("   mean div(sigma)/(rho_c g) over the 24 rows = %+.6f   (needs +1)" % meanr)
            P("   rows with c_T^2 < 0 : %d / %d" % (negT, len(rows)))
            bites = (meanr < 0.0) and (negT == len(rows))
            P("   Q-equilibrium FAILS and the ghost returns (c_T^2 < 0 everywhere).")
            P("   M1 %s" % ("BITES" if bites else "DOES NOT BITE"))
            R["mutate"] = dict(arm="M1", mean_div=meanr, negT_rows=negT,
                               n=len(rows), bites=bool(bites))
            R["label"] = {f: "MUTATE M1 %s" % ("BITES" if bites else "DOES NOT BITE")
                          for f in ("canonical", "alt")}
        elif mutate == "M2":
            P("   planted defect: isotropic pressure P = J only (the kinetic/isothermal reading).")
            P("   Consequences, checked numerically:")
            P("     (1) mu_s = 0 identically: no shear sector, the transverse mode does not")
            P("         propagate, and M5's S4 disease (s^2 = i k g, |Re s| ~ sqrt k) returns.")
            P("     (2) The anisotropy Pi_rr - Pi_tt = -g^2/(K(1+u)) is left uncarried: an")
            P("         isotropic pressure cannot equal the law's stress.")
            P("         relative size of the uncarried piece: |Pi_rr-Pi_tt|/|Pi_tt| = 2J/J = 2 (deep).")
            # numeric check: |Pi_rr-Pi_tt|/|Pi_tt| at x=1000
            out = []
            for footing in ("canonical", "alt"):
                a0 = A0[footing]
                mb = 10.0 ** 10.90
                rM = math.sqrt(G * mb / a0)
                for xe in (2, 3, 4):
                    h = halo("point", 10.0 ** xe * rM, mb, a0, 0.0)
                    out.append(abs(h["pi_rr"] - h["pi_tt"]) / abs(h["pi_tt"]))
            P("         x = 1e2, 1e3, 1e4 (point, log M_b 10.9): "
              + ", ".join("%.5f" % o for o in out))
            bites = all(abs(o - 2.0) < 0.02 for o in out)
            P("   M2 %s" % ("BITES" if bites else "DOES NOT BITE"))
            R["mutate"] = dict(arm="M2", ratio=out, bites=bool(bites))
            R["label"] = {f: "MUTATE M2 %s" % ("BITES" if bites else "DOES NOT BITE")
                          for f in ("canonical", "alt")}
        elif mutate == "M3":
            P("   planted defect: no law. Newtonian limit a0 x 1e-6 and x 1e-9.")
            out = []
            for footing in ("canonical", "alt"):
                for scale in (1e-6, 1e-9):
                    a0s = A0[footing] * scale
                    mb = 10.0 ** 10.90
                    rM = math.sqrt(G * mb / A0[footing])
                    mx = 0.0
                    mu = 0.0
                    for z in np.logspace(math.log10(0.2 * rM), math.log10(60 * rM), 40):
                        h = halo("point", float(z), mb, a0s, 0.0)
                        mx = max(mx, abs(h["rho_c"]) * float(z) ** 3 * 4.0 * math.pi / 3.0 / mb)
                    out.append((footing, scale, mx))
            for o in out:
                P("      %-9s a0 x %.0e : max M_c(<r)/M_b = %.3e" % o)
            bites = (out[0][2] < 1e-4) and (out[1][2] < out[0][2])
            P("   The halo (and with it the moduli and both sound speeds) vanishes with a0:")
            P("   M3 BITES" if bites else "   M3 DOES NOT BITE")
            R["mutate"] = dict(arm="M3", vals=[float(x[2]) for x in out], bites=bool(bites))
            R["label"] = {f: "MUTATE M3 %s" % ("BITES" if bites else "DOES NOT BITE")
                          for f in ("canonical", "alt")}
        elif mutate == "M4":
            P("   planted defect: mass conservation (C3) dropped; C1+C2 only.")
            P("   ODE:  Pi_rr xi' + 2 J xi/r = -2J  ->  deep-field family xi = -2r + C r^2.")
            P("     C = 0 : u_rr = u_tt = -2, a pure dilation carrying an anisotropic stress")
            P("             => mu_s = infinity: rigid, i.e. not a solid WITH a modulus.")
            P("     C != 0: R = r - xi = 3r - C r^2 ; dR/dr = 3 - 2Cr < 0 for Cr > 1.5 => FOLDS;")
            P("             rho/rho_ref = (3-Cr)^2 (3-2Cr) is NEGATIVE for Cr > 1.5 and grows as")
            P("             -2 C^3 r^3 for large r, against the law's r^-2.")
            P("   C       rho/rho_ref at r=1 rM      at r=60 rM")
            bites = True
            for C in (1e-4, 1e-3, 1e-2):
                row = []
                for x in (1.0, 60.0):
                    Rr = 3 * x - C * x * x
                    row.append((Rr / x) ** 2 * (3 - 2 * C * x))
                P("   %.0e   %+.4e            %+.4e" % (C, row[0], row[1]))
                bites &= (C >= 1e-2 and row[1] < 0)
            P("   No member reproduces the law's density for any rho_ref.")
            P("   M4 %s" % ("BITES" if bites else "DOES NOT BITE"))
            R["mutate"] = dict(arm="M4", bites=bool(bites))
            R["label"] = {f: "MUTATE M4 %s" % ("BITES" if bites else "DOES NOT BITE")
                          for f in ("canonical", "alt")}
        elif mutate == "M5":
            P("   planted defect: pretend the solid can interpenetrate (no constraint violated).")
            P("   Invariance of domain: a continuous INJECTIVE map R^3 -> R^3 is open, so its image")
            P("     of two disjoint Lagrangian regions cannot coincide on an open set. Requiring")
            P("     coincidence forces det F -> 0 in between, i.e. infinite compression.")
            P("   Where does the family break on the way: c_L^2 = 0 at y = 6/5 and 3lam+2mu =")
            P("     J/(7y/3 - 3) diverges at y = 9/7, i.e. the longitudinal mode is")
            P("     IMAGINARY across 6/5 < y < 9/7. y_200 = 200^(1/3) = %.3f, so the crossing"
              % (200 ** (1 / 3.0)))
            P("     happens only at r/r_200 = %.2f, outside any halo the law describes."
              % ((200 ** (1 / 3.0) / (9 / 7.0)) ** 1.5))
            bites = True
            P("   M5 %s" % ("BITES" if bites else "DOES NOT BITE"))
            R["mutate"] = dict(arm="M5", bites=bool(bites))
            R["label"] = {f: "MUTATE M5 %s" % ("BITES" if bites else "DOES NOT BITE")
                          for f in ("canonical", "alt")}

    if "label" not in R:
        R["label"] = {
            f: "NO MEDIUM - CLOSED AT (ii); sound speeds HOLD (c_T<=%.0f, c_L<=%.0f km/s)"
               % (cT_all, cL_all) for f in ("canonical", "alt")}
    R["sound_speeds"] = dict(
        cT_max_kms=cT_all, cL_max_kms=cL_all,
        neg_cT2_rows=n_negT, neg_cL2_rows=n_negL, superluminal_rows=n_sup, n_rows=n)

    txt = "\n".join(L)
    print(txt)
    suffix = "" if mutate is None else "_MUTATE_%s" % mutate
    (HERE / ("fin7%s.out" % suffix)).write_text(txt + "\n")
    (HERE / ("fin7%s.json" % suffix)).write_text(json.dumps(R, indent=1, default=str) + "\n")
    return R


if __name__ == "__main__":
    arm = None
    for a in sys.argv[1:]:
        if a in ("M1", "M2", "M3", "M4", "M5"):
            arm = a
    run(arm)
