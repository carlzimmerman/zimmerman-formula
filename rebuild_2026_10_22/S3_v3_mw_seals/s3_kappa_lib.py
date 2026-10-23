"""S3_v3_mw_seals Part B library: per-galaxy AQUAL corrections C(R; a0) for CFG493's P1 (SPARC, ladder) and P3 (WALLABY)
gas points.  Criteria FROZEN_CRITERIA.md §3 (8f6c6587e1) + A1, A2.  Each job runs in a child process (s3_aqual.run_batch).

Mass models (declared in §3): SPARC stars Sigma = Ups SBdisk (rotmod), constant inside the first point, exponential (R_disk)
beyond the last; bulge spherical from V_bul; gas from a non-negative least-squares inversion of rotmod V_gas^2 on hat
functions (nodes 0, the rotmod radii, 1.5 and 2 R_last; zero beyond).  WALLABY gas Sigma = CFG493's profile with its tail;
stars CFG493's exponential.  Thickness: primary stars exponential z_d = 0.1 R_d, gas sech^2 z0 = 0.1 kpc; variant razor-thin.
C = g_AQUAL / [nu1(g_N/a0) g_N] in the plane, g_N from the same grid.  Optional uniform external field along the disc axis
(gamma = 0) for the EFE step.  kappa = 1/2 FITTED; not theory closed.
"""
import os
import sys
import math
import numpy as np
from scipy.optimize import nnls
from scipy.sparse.linalg import splu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s3_aqual as S

G = S.G
KPC_M = S.KPC_M


def grid_for(Rlast):
    return S.Grid(0.01, 1.06, 3000.0, 0.005, 1.08, 3000.0)


def vertical(g, kind, zscale):
    """normalised vertical profile per column: 'exp' exp(-|z|/h)/(2h), 'sech2' sech^2(z/z0)/(2 z0), 'thin' central layer."""
    if kind == "thin":
        p = np.zeros(g.nz); p[g.jc] = 1.0 / g.dz[g.jc]
        return p
    if kind == "exp":
        p = np.exp(-np.abs(g.zc) / zscale) / (2 * zscale)
    else:
        p = 1.0 / np.cosh(g.zc / zscale) ** 2 / (2 * zscale)
    return p / np.sum(p * g.dz)


def sigma_cells(g, fun, nsub=8):
    """cell-averaged surface density (area-weighted sub-sampling)."""
    out = np.zeros(g.nR)
    for i in range(g.nR):
        r = np.linspace(g.Re[i], g.Re[i + 1], nsub + 1)
        rm = 0.5 * (r[1:] + r[:-1]); w = rm * np.diff(r)
        out[i] = float(np.sum(fun(rm) * w) / np.sum(w))
    return out


def laplace_lu(g):
    c = g.coeffs(np.zeros((g.nR, g.nz)), {k: np.zeros_like(v[0]) for k, v in g.bpoints().items()}, 1.0, None)
    return splu(g.matrix(*c)), c


def newton_with(g, lu, c, rho):
    M = S.total_mass(g, rho)
    PB = S.bc_newton(g, M)
    S_ = 4 * math.pi * G * rho * g.V
    return lu.solve(g.rhs(S_, PB, c).ravel()).reshape(g.nR, g.nz), PB


def C_profiles(g, rho, a0_list, R_eval, eN_list=None):
    """AQUAL / nu1-algebraic in-plane correction at R_eval for each a0 (isolated) or each (a0, eN) pair (EFE along z)."""
    M = S.total_mass(g, rho)
    PBN = S.bc_newton(g, M); PhiN = g.newton(rho, PBN)
    gN = g.gR_plane(PhiN, R_eval)
    out = []
    pairs = [(a, 0.0) for a in a0_list] if eN_list is None else list(zip(a0_list, eN_list))
    for a0_si, eN in pairs:
        a0 = S.a0u(a0_si)
        if eN and eN > 0:
            PB, ge = S.bc_aqual_efe_z(g, M, a0, eN)
            Phi, info = g.aqual(rho, a0, PB, Phi_init_N=PhiN, PB_N=PBN, ge=ge, ye_a0=eN * a0)
        else:
            Phi, info = g.aqual(rho, a0, S.bc_aqual_iso(g, M, a0), Phi_init_N=PhiN, PB_N=PBN)
        gA = g.gR_plane(Phi, R_eval)
        out.append(dict(C=(gA / (S.nu1(gN / a0) * gN)).tolist(), residual=info["residual"], floor=info["floor"]))
    return out, gN


def job_sparc(name, R, Vgas, SBdisk, Vbul, Rdisk, a0_list, thin=False, eN_list=None, ups_d=0.5, ups_b=0.7, tail=1.5, Mgas_target=None):
    """SPARC galaxy (already rescaled to its ladder distance): returns C at the rotmod radii and inversion diagnostics."""
    R = np.asarray(R, float); Vgas = np.asarray(Vgas, float); SB = np.asarray(SBdisk, float); Vb = np.asarray(Vbul, float)
    g = grid_for(R[-1])
    lu, c = laplace_lu(g)
    # stars
    Sig_nodes = ups_d * SB * 1e6

    def sig_star(r):
        r = np.asarray(r, float)
        inner = np.interp(r, R, Sig_nodes)
        tail = Sig_nodes[-1] * np.exp(-(r - R[-1]) / Rdisk)
        return np.where(r <= R[-1], inner, tail)
    vs = vertical(g, "thin" if thin else "exp", 0.1 * Rdisk)
    rho_s = sigma_cells(g, sig_star)[:, None] * vs[None, :]
    # bulge (spherical, M(<r) = ups_b Vbul^2 r / G, constant beyond the last point)
    rho_b = np.zeros_like(rho_s)
    if np.any(Vb > 0):
        Mb = ups_b * Vb ** 2 * R / G
        rr = np.concatenate([[0.0], R]); mm = np.concatenate([[0.0], np.maximum.accumulate(Mb)])
        rc = np.hypot(g.RR, g.ZZ)
        Mi = np.interp(rc, rr, mm)
        # cell density from the enclosed-mass derivative
        dr = 1e-3 * np.maximum(rc, 1e-3)
        dM = (np.interp(rc + dr, rr, mm) - np.interp(np.maximum(rc - dr, 0), rr, mm)) / (2 * dr)
        rho_b = np.where(rc < R[-1], dM / (4 * math.pi * np.maximum(rc, 1e-4) ** 2), 0.0)
    # gas inversion (NNLS on hats)
    # AMENDMENT A4: one hat per rotmod radius; flat inside R_1; the last hat declines linearly to zero at tail x R_last
    nodes = np.concatenate([[0.0], R, [tail * R[-1]]])
    vg = vertical(g, "thin" if thin else "sech2", 0.1)
    B = []

    def ext(e):
        return np.concatenate([[e[0]], e, [0.0]])
    for k in range(len(R)):
        e = np.zeros(len(R)); e[k] = 1.0
        hat = lambda r, e=e: np.interp(r, nodes, ext(e), right=0.0)
        rho_k = sigma_cells(g, hat)[:, None] * vg[None, :] * 1e6
        Phi_k, _ = newton_with(g, lu, c, rho_k)
        B.append(g.vc2(Phi_k, R))
    B = np.array(B).T                                           # (npts, nnodes): V^2 per 1e6 Msun/kpc^2 node value
    target = np.sign(Vgas) * Vgas ** 2
    # AMENDMENT A7: bounded-variable least squares on V_gas^2 (rows scaled by max|V_gas^2|) plus one row holding the total gas
    # mass to SPARC's own 1.33 M_HI (weight 1: a 10 % mass error costs as much as a 10 % misfit of the peak V^2), and a 1e-6
    # relative ridge for uniqueness.  Without the mass row the outer hats are degenerate (DDO161 took 1e11 Msun).
    from scipy.optimize import lsq_linear
    cn = np.maximum(np.linalg.norm(B, axis=0), 1e-300)
    sc = max(float(np.max(np.abs(target))), 1e-30)
    Bn = B / cn[None, :] / sc
    Mk = np.array([2 * math.pi * float(np.sum(sigma_cells(g, lambda r, e=e: np.interp(r, nodes, ext(e), right=0.0)) * g.Rc * g.dR)) * 1e6
                   for e in np.eye(len(R))])
    rows = [Bn, (Mk / cn / Mgas_target)[None, :]] if Mgas_target else [Bn]
    rhs_ = [target / sc, [1.0]] if Mgas_target else [target / sc]
    lam = 1e-6 * np.linalg.norm(Bn, 2)
    Aug = np.vstack(rows + [lam * np.eye(Bn.shape[1])]); tAug = np.concatenate([np.concatenate([np.atleast_1d(x) for x in rhs_]), np.zeros(Bn.shape[1])])
    coef = lsq_linear(Aug, tAug, bounds=(0, np.inf), method="bvls", tol=1e-12).x / cn
    fit = B @ coef
    rho_g = sigma_cells(g, lambda r: np.interp(r, nodes, ext(coef), right=0.0))[:, None] * vg[None, :] * 1e6
    rho = rho_s + rho_b + rho_g
    # Newtonian diagnostics
    Phi_t, _ = newton_with(g, lu, c, rho)
    vbar2_me = g.vc2(Phi_t, R)
    Cs, gN = C_profiles(g, rho, a0_list, R, eN_list)
    return dict(name=name, R=R.tolist(), gas_fit=fit.tolist(), gas_target=target.tolist(), vbar2_me=vbar2_me.tolist(), C=Cs,
                Mgas=S.total_mass(g, rho_g), Mstar=S.total_mass(g, rho_s), Mbul=S.total_mass(g, rho_b))


def job_wallaby(name, R, rS, Sig, Mstar, Rd, a0_list, thin=False, eN_list=None, tail=1.5):
    """WALLABY galaxy (CFG493 build at H0 67.4): C at the rotation-curve radii; my grid's V_gas^2 for check B3."""
    R = np.asarray(R, float); rS = np.asarray(rS, float); Sig = np.asarray(Sig, float)
    g = grid_for(R[-1])
    lu, c = laplace_lu(g)
    rlast = rS[-1]
    h = None
    if len(rS) >= 3 and Sig[-1] > 0 and Sig[-2] > Sig[-1]:
        h = (rS[-1] - rS[-2]) / math.log(Sig[-2] / Sig[-1])

    def sig_gas(r):
        r = np.asarray(r, float)
        inner = np.interp(r, rS, Sig)
        if h is None:
            return np.where(r <= rlast, inner, 0.0)
        tl = np.where(r <= tail * rlast, Sig[-1] * np.exp(-(r - rlast) / h), 0.0)
        return np.where(r <= rlast, inner, tl)
    vg = vertical(g, "thin" if thin else "sech2", 0.1)
    rho_g = sigma_cells(g, sig_gas)[:, None] * vg[None, :]
    Phi_g, _ = newton_with(g, lu, c, rho_g)
    vg2_me = g.vc2(Phi_g, R)
    Menc = Mstar * (1 - (1 + g.Re / Rd) * np.exp(-g.Re / Rd))
    Sig_s = np.diff(Menc) / (math.pi * (g.Re[1:] ** 2 - g.Re[:-1] ** 2))
    vs = vertical(g, "thin" if thin else "exp", 0.1 * Rd)
    rho = rho_g + Sig_s[:, None] * vs[None, :]
    Cs, gN = C_profiles(g, rho, a0_list, R, eN_list)
    return dict(name=name, R=R.tolist(), vg2_me=vg2_me.tolist(), C=Cs)


def job_refdisc(a0_si, thin=False):
    """P2's declared reference deep disc: stars exponential (R_d = 1 kpc), gas exponential R_g = 2 R_d with M_gas = 3 M*,
    M* set so that the algebraic total g_N(3 R_d)/a0 = 0.05 (razor-thin Freeman sums).  C at 3, 4, 5 R_d."""
    from scipy.optimize import brentq
    a0 = S.a0u(a0_si)
    Rd = 1.0
    fv2 = lambda M, Rs, R: S.freeman_v2(M, Rs, R)
    yfun = lambda Ms: (fv2(Ms, Rd, 3.0) + fv2(3 * Ms, 2 * Rd, 3.0)) / 3.0 / a0 - 0.05
    Ms = brentq(yfun, 1e4, 1e12)
    g = grid_for(5.0)
    vs = vertical(g, "thin" if thin else "exp", 0.1 * Rd)
    vgp = vertical(g, "thin" if thin else "sech2", 0.1)

    def disc(M, Rs, prof):
        Menc = M * (1 - (1 + g.Re / Rs) * np.exp(-g.Re / Rs))
        return (np.diff(Menc) / (math.pi * (g.Re[1:] ** 2 - g.Re[:-1] ** 2)))[:, None] * prof[None, :]
    rho = disc(Ms, Rd, vs) + disc(3 * Ms, 2 * Rd, vgp)
    Rv = np.array([3.0, 4.0, 5.0])
    Cs, gN = C_profiles(g, rho, [a0_si], Rv)
    return dict(Mstar=Ms, C=Cs[0]["C"], y=(gN / a0).tolist())


def job_wallaby_vg2(name, R, rS, Sig, tail=1.5):
    """Newtonian V_gas^2 (primary thickness and razor-thin) of a WALLABY gas profile on this lane's grid (AMENDMENT A6)."""
    R = np.asarray(R, float); rS = np.asarray(rS, float); Sig = np.asarray(Sig, float)
    g = grid_for(R[-1])
    lu, c = laplace_lu(g)
    rlast = rS[-1]
    h = None
    if len(rS) >= 3 and Sig[-1] > 0 and Sig[-2] > Sig[-1]:
        h = (rS[-1] - rS[-2]) / math.log(Sig[-2] / Sig[-1])

    def sig_gas(r):
        r = np.asarray(r, float)
        inner = np.interp(r, rS, Sig)
        if h is None:
            return np.where(r <= rlast, inner, 0.0)
        tl = np.where(r <= tail * rlast, Sig[-1] * np.exp(-(r - rlast) / h), 0.0)
        return np.where(r <= rlast, inner, tl)
    sc = sigma_cells(g, sig_gas)
    out = {}
    for kind in ("sech2", "thin"):
        rho = sc[:, None] * vertical(g, kind, 0.1)[None, :]
        Phi, _ = newton_with(g, lu, c, rho)
        out[kind] = g.vc2(Phi, R).tolist()
    return dict(name=name, vg2=out["sech2"], vg2_thin=out["thin"])
