"""CFG645 library (FROZEN_CRITERIA.md, 21b7b0857): energy-bounded settling H-EB.

The one framework identity used: rho_DE c^2 = a0^2 / (kappa^2 G)  (A2, a0 = kappa c sqrt(G rho_DE)).
Local capacity (EB-L): rho_set(r) <= rho_cap(r) = a0^2 / (kappa^2 G e(r)),  e = e_V = V_c^2  or  e_Phi = Phi(r_ta) - Phi(r).
Global capacity (EB-R): C = rho_DE c^2 V_ta; settle inside-out until the cumulative export int e_Phi dM_set reaches C.
Unit-agnostic: pass r, masses, G, a0 in ONE consistent system (SI, kpc-Gyr-Msun, or Mpc-km/s-Msun).
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import math
import numpy as np

KAPPA = 0.5
DTA = 11.81                     # Delta_ta, the framework PM z = 0 value (CFG504 / CFG555 / CFG556), inherited
OM = (0.02237 + 0.1200) / 0.6736 ** 2


def rho_de_c2(a0, G):
    """dark-energy energy density from the law's scale (A2)."""
    return a0 ** 2 / (KAPPA ** 2 * G)


def r_ta_of(Mta, rho_m):
    return (3.0 * Mta / (4.0 * math.pi * DTA * rho_m)) ** (1.0 / 3.0)


def e_profiles(r, Mtot, G, r_ta, outer="kepler"):
    """e_V(r) = G Mtot/r and e_Phi(r) = int_r^{r_ta} G Mtot/r'^2 dr' on the grid r (ascending).
    Beyond the grid end: outer = 'kepler' (Mtot fixed) or 'iso' (Mtot grows proportional to r, flat V)."""
    r = np.asarray(r, float); Mtot = np.asarray(Mtot, float)
    rr = np.maximum(r, 1e-300)
    g = G * Mtot / rr ** 2
    eV = G * Mtot / rr
    # cumulative integral from each r to the grid end
    seg = 0.5 * (g[1:] + g[:-1]) * np.diff(r)
    tail_grid = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    rend = r[-1]
    if r_ta > rend:
        if outer == "kepler":
            ext = G * Mtot[-1] * (1.0 / rend - 1.0 / r_ta)
        else:
            ext = G * Mtot[-1] / rend * math.log(r_ta / rend)
        ePhi = tail_grid + ext
    else:
        # integrate only to r_ta
        Phi_cum = np.concatenate([[0.0], np.cumsum(seg)])            # int_{r0}^{r} g
        Phi_ta = float(np.interp(r_ta, r, Phi_cum))
        ePhi = np.maximum(Phi_ta - Phi_cum, 0.0)
    return eV, ePhi


def cap_cum(r, Mset, e, a0, G, fac=1.0, mode="L", C=None):
    """apply a capacity to a cumulative settled-mass profile Mset(<r) on the grid r.
    mode 'L': local cap rho_set <= fac * a0^2/(kappa^2 G e) shell by shell (shell-averaged density, shell-midpoint e).
    mode 'R': global inside-out truncation where cumulative int e dM_set reaches C (fac multiplies C).
    mode 'inf': no cap.  mode 'zero': nothing settles.
    Returns (Mset_capped(<r), removed(<r), info)."""
    r = np.asarray(r, float); Mset = np.asarray(Mset, float); e = np.asarray(e, float)
    if mode == "inf":
        return Mset.copy(), np.zeros_like(Mset), dict(removed_tot=0.0, bind_lo=None, bind_hi=None)
    if mode == "zero":
        return np.zeros_like(Mset), Mset.copy(), dict(removed_tot=float(Mset[-1]), bind_lo=float(r[0]), bind_hi=float(r[-1]))
    dM = np.diff(Mset)
    em = 0.5 * (e[1:] + e[:-1])
    if mode == "L":
        dV = 4.0 / 3.0 * math.pi * (r[1:] ** 3 - r[:-1] ** 3)
        rho = dM / np.maximum(dV, 1e-300)
        rcap = fac * a0 ** 2 / (KAPPA ** 2 * G * np.maximum(em, 1e-300))
        rem = np.maximum(rho - rcap, 0.0) * dV
        rem = np.minimum(rem, np.maximum(dM, 0.0))
        bind = rem > 0
    elif mode == "R":
        Ecum = np.cumsum(np.maximum(dM, 0.0) * em)
        Cap = fac * C
        own = np.maximum(dM, 0.0) * em
        with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
            keep = np.where(own > 0, np.clip((Cap - (Ecum - own)) / np.where(own > 0, own, 1.0), 0.0, 1.0), 1.0)
        rem = np.maximum(dM, 0.0) * (1.0 - keep)
        bind = rem > 0
    else:
        raise ValueError(mode)
    removed = np.concatenate([[0.0], np.cumsum(rem)])
    Mc = Mset - removed
    rm = np.where(r[:-1] > 0, np.sqrt(r[1:] * np.maximum(r[:-1], 1e-300)), 0.5 * r[1:])
    info = dict(removed_tot=float(removed[-1]),
                bind_lo=float(rm[bind].min()) if bind.any() else None, bind_hi=float(rm[bind].max()) if bind.any() else None)
    return Mc, removed, info


# ------------------------------------------------------------------ point mass (GM = 1, a0 = 1 units unless given)
def point_mass_R(y, nu, dy=1e-4):
    """R(y) = rho_ph V_c^2 / (rho_DE c^2) for a point mass, from the profile by finite differences in r (no closed form used).
    In units GM = a0 = 1: r = y^-1/2, M_ph(<r) = nu(y) - 1, V_c^2 = nu(y) y r, rho_DE c^2 = 1/(kappa^2 G) with G = 1."""
    y = np.asarray(y, float)
    r = y ** -0.5
    h = dy * r
    yp, ym = (r + h) ** -2, (r - h) ** -2
    dMdr = (np.asarray(nu(yp), float) - np.asarray(nu(ym), float)) / (2 * h)
    rho = dMdr / (4 * math.pi * r ** 2)
    Vc2 = np.asarray(nu(y), float) * y * r
    return rho * Vc2 * KAPPA ** 2


def point_mass_removed(M, a0, G, nu, r_out, e_mode="V", r_ta=None, n=4000, fac=1.0, Mtot_outer=None):
    """EB-L removal for a point baryonic mass M inside r_out (any consistent units).
    Returns (removed mass, phantom mass M_ph(<r_out))."""
    r = np.geomspace(r_out * 1e-7, r_out, n)
    y = G * M / (r ** 2 * a0)
    Mph = (np.asarray(nu(y), float) - 1.0) * M
    Mtot = M + Mph
    if e_mode == "V":
        e = G * Mtot / r
    else:
        rgrid = np.geomspace(r_out * 1e-7, r_ta, n + 2000)
        yg = G * M / (rgrid ** 2 * a0)
        Mt_g = M * np.asarray(nu(yg), float)
        if Mtot_outer is not None:
            Mt_g = np.minimum(Mt_g, Mtot_outer)
        _, ePhi = e_profiles(rgrid, Mt_g, G, r_ta)
        e = np.interp(np.log(r), np.log(rgrid), ePhi)
    Mc, rem, _ = cap_cum(r, Mph - Mph[0], e, a0, G, fac=fac, mode="L")
    # interior of the first node: its phantom is (nu(y0)-1) M ~ 0 for the kernels used; counted as fully removed (upper bound)
    return float(rem[-1] + Mph[0]), float(Mph[-1])
