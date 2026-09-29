#!/usr/bin/env python3
"""Cut 13 (resolved-triple search): the frozen text read literally, and the
existing orbit-aware bound, as two functions with IDENTICAL signatures so they
can be run side by side as primary / variant (Amendment 16 draft, item (b)).

NOTHING HERE CHANGES A FROZEN CUT.  Frozen text (PREREGISTRATION_DR4.md
section 1.2 row 13, line 558): "no co-moving third Gaia source (parallax within
3 sigma, PM within 5 sigma of the pair) with G < 20 within projected 30 kAU of
either component".

Both functions take the searched catalogue as a dict of equal-length arrays
`cat` and pair index arrays `a`, `b` (rows of `cat`), and return a
ThirdResult:
    flags                 bool per pair: True = a third star was found
                          (the pair would be REJECTED by cut 13)
    n_neigh               candidate neighbours inside the search radius
                          (unique per pair, either component, pair members
                          excluded)
    n_no_g                of those, how many have NO G value (NaN)
    n_no_g_kin            of those, how many pass the kinematic test of the
                          criterion in force, i.e. third stars that the
                          G < 20 lookup would silently drop
    n_hit                 number of flagged pairs (= flags.sum())
The no-G counts are reported separately, never folded into `flags`
(Amendment 16 draft (b): "the count of such sources is recorded in the
manifest").

Required keys of `cat`: ra, dec (deg), parallax, parallax_error (mas), pmra,
pmdec, pmra_error, pmdec_error (mas/yr), phot_g_mean_mag.

Provenance of the maths (read-only, copied not imported so this module has no
dependency on the frozen builder; test_cut13.py cross-checks the copies
against the builder on random data):
  * _ang_sep_arcsec       == catalog_builder/build_catalog.py ang_sep_arcsec,
                             lines 79-82.
  * _delta_mu_and_sigma   == build_catalog.py delta_mu_and_sigma, lines 58-67
                             (El-Badry eq. 3-4).
  * orbit-aware bound     == build_catalog.py third_star_flags, lines 364-387:
        search radius  th = 30000 AU / d(primary) [arcsec], d = 1000/parallax[a]
                             (lines 371-372: the PRIMARY's parallax sets the
                             radius for both components);
        reference star k = a (line 377): parallax and PM differences are taken
                             against the PRIMARY, also for a third found near b;
        dpar = |plx_k - plx_j| / hypot(e_k, e_j)                (line 379)
        orb  = 0.44428 * plx_k**1.5 * theta**-0.5, theta = sep(k, j) in arcsec
                             (line 384; theta from the PRIMARY even when the
                             third was found within 30 kAU of b);
        hit  = dpar < 3 and dmu < orb + 2*sdmu and G_j < 20    (line 385).
    Reproduced exactly, including those two quirks.

Interpretive choices in the LITERAL criterion (the frozen text is silent):
  * "the pair" as reference: default reference="primary" (the same reference
    star the existing code uses, so the two functions differ ONLY in the PM
    bound).  reference="mean" uses the pair mean (parallax, PM) with errors
    hypot(e_a, e_b)/2, and is offered so the difference can be measured, not
    to choose after the data exist.
  * "PM within 5 sigma": dmu < 5*sdmu with sdmu the El-Badry projected sigma of
    the relative PM (the same sdmu as the orbit-aware bound).  No orbital
    allowance.
  * strict inequalities everywhere (parallax 3, PM 5, G < 20), as written.
"""
from __future__ import annotations

from typing import NamedTuple

import numpy as np
from scipy.spatial import cKDTree

# ---- constants of the two criteria (documented, not tunable at run time) ----
N_SIGMA_PLX = 3.0          # frozen row 13
N_SIGMA_PM = 5.0           # frozen row 13 (literal)
ORB_COEFF = 0.44428        # build_catalog.py line 384
SDMU_MULT = 2.0            # build_catalog.py line 385
G_MAX = 20.0               # frozen row 13
RADIUS_KAU = 30.0          # frozen row 13

# Test hook ONLY: test_cut13.py sets this to True for its MUTATE control, which
# inverts the PM inequality.  Never set outside a control.
_MUTATE = False

REQUIRED = ("ra", "dec", "parallax", "parallax_error", "pmra", "pmdec",
            "pmra_error", "pmdec_error", "phot_g_mean_mag")


class ThirdResult(NamedTuple):
    flags: np.ndarray
    n_neigh: int
    n_no_g: int
    n_no_g_kin: int
    n_hit: int


# ------------------------------------------------------------------ maths
def _ang_sep_arcsec(ra1, dec1, ra2, dec2):
    """Copy of build_catalog.py ang_sep_arcsec (lines 79-82)."""
    r1, d1, r2, d2 = map(np.radians, (ra1, dec1, ra2, dec2))
    h = np.sin((d2 - d1) / 2) ** 2 + np.cos(d1) * np.cos(d2) * np.sin((r2 - r1) / 2) ** 2
    return np.degrees(2 * np.arcsin(np.sqrt(h))) * 3600


def _delta_mu_and_sigma(pmra1, pmdec1, pmra2, pmdec2, e_ra1, e_de1, e_ra2, e_de2):
    """Copy of build_catalog.py delta_mu_and_sigma (lines 58-67)."""
    dra, dde = pmra1 - pmra2, pmdec1 - pmdec2
    dmu = np.sqrt(dra ** 2 + dde ** 2)
    with np.errstate(invalid="ignore", divide="ignore"):
        sig = np.sqrt((e_ra1 ** 2 + e_ra2 ** 2) * dra ** 2
                      + (e_de1 ** 2 + e_de2 ** 2) * dde ** 2) / dmu
    zero = np.sqrt(e_ra1 ** 2 + e_ra2 ** 2 + e_de1 ** 2 + e_de2 ** 2)
    sig = np.where(dmu > 0, sig, zero)
    return dmu, sig


def orbit_allowance(parallax_mas, theta_arcsec):
    """orb = 0.44428 * plx^1.5 * theta^-0.5  [mas/yr] (build_catalog.py l.384)."""
    with np.errstate(divide="ignore"):
        return np.where(np.asarray(theta_arcsec) > 0,
                        ORB_COEFF * np.asarray(parallax_mas) ** 1.5
                        * np.asarray(theta_arcsec, float) ** -0.5, 1e9)


# ------------------------------------------------------------ shared search
def _check(cat, a, b):
    miss = [k for k in REQUIRED if k not in cat]
    if miss:
        raise KeyError(f"catalogue lacks required columns: {miss}")
    n = len(cat["ra"])
    for k in REQUIRED:
        if len(cat[k]) != n:
            raise ValueError(f"column {k} has length {len(cat[k])} != {n}")
    a, b = np.asarray(a, int), np.asarray(b, int)
    if a.shape != b.shape:
        raise ValueError("a and b must have the same shape")
    return a, b


def _unit(ra, dec):
    r, d = np.radians(ra), np.radians(dec)
    return np.column_stack([np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)])


def _search(cat, a, b, radius_kau):
    """Yield (i, js): rows of `cat` within radius_kau of either component of
    pair i, pair members excluded.  Radius = radius_kau*1000 AU / d(primary)
    in arcsec, d = 1000/parallax[a] (build_catalog.py l.371-372)."""
    xyz = _unit(np.asarray(cat["ra"], float), np.asarray(cat["dec"], float))
    tree = cKDTree(xyz)
    th_arcsec = radius_kau * 1000.0 * np.asarray(cat["parallax"], float)[a] / 1000.0
    th_rad = th_arcsec * np.pi / 180 / 3600
    chord = 2 * np.sin(th_rad / 2)
    out = []
    for i in range(len(a)):
        sel = set()
        for comp in (a[i], b[i]):
            sel.update(tree.query_ball_point(xyz[comp], r=chord[i]))
        sel.discard(int(a[i]))
        sel.discard(int(b[i]))
        out.append((i, np.array(sorted(sel), dtype=int)))
    return out


def _run(cat, a, b, radius_kau, g_max, n_sigma_par, kind, reference):
    a, b = _check(cat, a, b)
    if kind == "orbit" and reference != "primary":
        raise ValueError("the orbit-aware reproduction uses the primary as reference only")
    if reference not in ("primary", "mean"):
        raise ValueError("reference must be 'primary' or 'mean'")
    f = {k: np.asarray(cat[k], float) for k in REQUIRED}
    flags = np.zeros(len(a), bool)
    n_neigh = n_no_g = n_no_g_kin = 0
    for i, js in _search(cat, a, b, radius_kau):
        if len(js) == 0:
            continue
        k = a[i]
        n_neigh += len(js)
        if reference == "mean":
            plx_r = 0.5 * (f["parallax"][a[i]] + f["parallax"][b[i]])
            e_plx_r = 0.5 * np.hypot(f["parallax_error"][a[i]], f["parallax_error"][b[i]])
            pmra_r = 0.5 * (f["pmra"][a[i]] + f["pmra"][b[i]])
            pmde_r = 0.5 * (f["pmdec"][a[i]] + f["pmdec"][b[i]])
            e_ra_r = 0.5 * np.hypot(f["pmra_error"][a[i]], f["pmra_error"][b[i]])
            e_de_r = 0.5 * np.hypot(f["pmdec_error"][a[i]], f["pmdec_error"][b[i]])
        else:
            plx_r, e_plx_r = f["parallax"][k], f["parallax_error"][k]
            pmra_r, pmde_r = f["pmra"][k], f["pmdec"][k]
            e_ra_r, e_de_r = f["pmra_error"][k], f["pmdec_error"][k]
        dpar = np.abs(plx_r - f["parallax"][js]) / np.hypot(e_plx_r, f["parallax_error"][js])
        dmu, sdmu = _delta_mu_and_sigma(pmra_r, pmde_r, f["pmra"][js], f["pmdec"][js],
                                        e_ra_r, e_de_r, f["pmra_error"][js], f["pmdec_error"][js])
        if kind == "literal":
            bound = N_SIGMA_PM * sdmu
        else:  # orbit-aware, theta from the PRIMARY (build_catalog.py l.377-385)
            thk = _ang_sep_arcsec(f["ra"][k], f["dec"][k], f["ra"][js], f["dec"][js])
            bound = orbit_allowance(f["parallax"][k], thk) + SDMU_MULT * sdmu
        with np.errstate(invalid="ignore"):
            pm_ok = (dmu > bound) if _MUTATE else (dmu < bound)   # _MUTATE inverts
            kin = (dpar < n_sigma_par) & pm_ok
            g = f["phot_g_mean_mag"][js]
            nog = ~np.isfinite(g)
            hit = kin & (g < g_max)
        n_no_g += int(nog.sum())
        n_no_g_kin += int((kin & nog).sum())
        flags[i] = bool(hit.any())
    return ThirdResult(flags, n_neigh, n_no_g, n_no_g_kin, int(flags.sum()))


# --------------------------------------------------------------- public API
def third_star_literal(cat, a, b, radius_kau=RADIUS_KAU, g_max=G_MAX,
                       n_sigma_par=N_SIGMA_PLX, reference="primary") -> ThirdResult:
    """Frozen row 13 read literally: dpar < 3 and dmu < 5*sdmu and G < 20 within
    30 kAU (projected) of either component.  Proposed PRIMARY (Amendment 16
    draft (b))."""
    return _run(cat, a, b, radius_kau, g_max, n_sigma_par, "literal", reference)


def third_star_orbit_aware(cat, a, b, radius_kau=RADIUS_KAU, g_max=G_MAX,
                           n_sigma_par=N_SIGMA_PLX, reference="primary") -> ThirdResult:
    """The existing code's bound (build_catalog.py third_star_flags):
    dpar < 3 and dmu < orb + 2*sdmu and G < 20, orb = 0.44428*plx^1.5*theta^-0.5.
    Proposed reported VARIANT.  `reference` must be 'primary' (kept in the
    signature so both functions are call-compatible)."""
    return _run(cat, a, b, radius_kau, g_max, n_sigma_par, "orbit", reference)


if __name__ == "__main__":
    print(__doc__)
