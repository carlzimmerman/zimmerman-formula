"""F2_outer_lensing: own axisymmetric AQUAL solver (point mass in a uniform external field) and lensing projection.

Units: G = M = a0 = 1, length r_M = sqrt(G M / a0).  mu(x) = x/(1+x) (THEORY_V3 Sec. 1; C4 K2).
Field equation (AQUAL, the action's equation): div[ mu(|grad Phi|) grad Phi ] = 4 pi rho, point mass inside r_min.
External field: Phi -> x_e z at large r, with mu(x_e) x_e = y_e (y_e = Newtonian external field / a0).
Discretisation: finite volume on (ln r, theta), axisymmetric about the field axis; Kacanov (frozen-mu) iteration,
each step one sparse direct solve.  Inner face: radial flux mu dPhi/dr = 1/r_min^2 (Newtonian regime at r_min).
Outer face: Dirichlet, the linearised anisotropic far field  Phi = x_e z - 1/(mu_e sqrt(1+L_e) r'),
r' = sqrt(x^2 + y^2 + z^2/(1+L_e)),  L_e = dln mu/dln x at x_e.
Lensing: phi = psi (C4 K1) so the lensing mass inside a sphere is M_eff(<r) = r^2 <dPhi/dr>_Omega; for random
orientations the stacked Delta Sigma is that of the spherical profile M_eff(r) (orientation-average identity).
kappa = 1/2 FITTED (enters only through the a0 footing used by the caller).
"""
import math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

mu = lambda x: x / (1.0 + x)


def nu_simple(y):
    """isolated spherical law: g = nu(g_N) g_N with mu = x/(1+x)."""
    y = np.asarray(y, float)
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / np.maximum(y, 1e-300)))


def x_of_y(y):
    """total external field from the Newtonian one: x^2/(1+x) = y."""
    return 0.5 * (y + math.sqrt(y * y + 4.0 * y)) if y > 0 else 0.0


def M_iso(s):
    """isolated AQUAL effective (lensing) mass inside s = r/r_M for a point mass (exact, spherical)."""
    s = np.asarray(s, float)
    return nu_simple(1.0 / s ** 2)


def solve_efe(y_e, nr_per_dec=60, nt=64, r_min=0.05, rmax_fac=60.0, tol=1e-9, maxit=300, omega=1.0, verbose=False):
    """Return dict(r=face radii, M=angle-averaged lensing mass, x_e, iters, resid)."""
    x_e = x_of_y(y_e)
    r_max = rmax_fac / x_e
    nr = int(round(nr_per_dec * math.log10(r_max / r_min)))
    du = math.log(r_max / r_min) / nr
    rf = r_min * np.exp(du * np.arange(nr + 1))                 # radial faces 0..nr (nr cells)
    rc = np.sqrt(rf[1:] * rf[:-1])                               # cell centres (geometric)
    dth = math.pi / nt
    th = (np.arange(nt) + 0.5) * dth
    thf = np.arange(1, nt) * dth
    sth = np.sin(th); cth = np.cos(th)
    w_ang = np.cos(th - 0.5 * dth) - np.cos(th + 0.5 * dth)      # exact solid-angle weights / 2pi (sum = 2)
    # far-field Dirichlet values at a ghost centre beyond the last face
    mu_e = mu(x_e); L_e = 1.0 / (1.0 + x_e)                       # dln mu/dln x for x/(1+x)
    def far(r, t):
        rp = r * np.sqrt(np.sin(t) ** 2 + np.cos(t) ** 2 / (1.0 + L_e))
        return x_e * r * np.cos(t) - 1.0 / (mu_e * math.sqrt(1.0 + L_e) * rp)
    r_ghost = rf[-1] * math.exp(0.5 * du)
    phi_out = far(r_ghost, th)
    # areas (2pi dropped consistently) and distances
    Ar = rf[:, None] ** 2 * w_ang[None, :]                       # radial faces (nr+1, nt)
    rlo, rhi = rf[:-1], rf[1:]
    At = np.sin(thf)[None, :] * 0.5 * (rhi ** 2 - rlo ** 2)[:, None]   # theta faces (nr, nt-1)
    rcg = np.concatenate([rc, [r_ghost]])
    drc = np.diff(rcg)                                           # centre spacing across interior faces 1..nr
    # initial guess: isolated algebraic potential + external
    rr = np.exp(np.linspace(math.log(r_min * 0.5), math.log(r_ghost), 20001))
    gi = nu_simple(1.0 / rr ** 2) / rr ** 2
    pot = np.concatenate([[0.0], np.cumsum(0.5 * (gi[1:] * rr[1:] + gi[:-1] * rr[:-1]) * np.diff(np.log(rr)))])
    pot = pot - np.interp(r_ghost, rr, pot) + np.mean(phi_out - x_e * r_ghost * cth)
    P = np.interp(rc, rr, pot)[:, None] + x_e * rc[:, None] * cth[None, :]
    N = nr * nt
    idx = np.arange(N).reshape(nr, nt)

    def face_mu(P):
        Pg = np.vstack([P, phi_out[None, :]])                    # include ghost row
        # radial faces 1..nr (interior + outer): normal from difference, tangential averaged
        dPr = (Pg[1:] - Pg[:-1]) / drc[:, None]                  # (nr, nt) at faces 1..nr
        dPt_c = np.empty_like(Pg)
        dPt_c[:, 1:-1] = (Pg[:, 2:] - Pg[:, :-2]) / (2 * dth)
        dPt_c[:, 0] = (Pg[:, 1] - Pg[:, 0]) / (2 * dth)
        dPt_c[:, -1] = (Pg[:, -1] - Pg[:, -2]) / (2 * dth)
        dPt_c /= rcg[:, None]
        tang = 0.5 * (dPt_c[1:] + dPt_c[:-1])
        mu_r = mu(np.hypot(dPr, tang))
        # theta faces
        dPr_c = np.empty_like(P)
        dPr_c[1:-1] = (P[2:] - P[:-2]) / (rc[2:] - rc[:-2])[:, None]
        dPr_c[0] = (P[1] - P[0]) / (rc[1] - rc[0])
        dPr_c[-1] = (Pg[-1] - P[-2]) / (r_ghost - rc[-2])
        dPt = (P[:, 1:] - P[:, :-1]) / (rc[:, None] * dth)
        rad = 0.5 * (dPr_c[:, 1:] + dPr_c[:, :-1])
        mu_t = mu(np.hypot(rad, dPt))
        return mu_r, mu_t

    hist = []
    for it in range(maxit):
        mu_r, mu_t = face_mu(P)
        cr = mu_r * Ar[1:] / drc[:, None]                        # conductances at faces 1..nr  (nr, nt)
        ct = mu_t * At / (rc[:, None] * dth)                     # (nr, nt-1)
        rows, cols, vals = [], [], []
        diag = np.zeros((nr, nt))
        b = np.zeros((nr, nt))
        # radial interior faces between cell i and i+1 (i = 0..nr-2) -> conductance cr[i]
        ci = cr[:-1]
        k0 = idx[:-1].ravel(); k1 = idx[1:].ravel()
        rows += [k0, k1]; cols += [k1, k0]; vals += [ci.ravel(), ci.ravel()]
        diag[:-1] -= ci; diag[1:] -= ci
        # outer face: Dirichlet ghost
        diag[-1] -= cr[-1]; b[-1] -= cr[-1] * phi_out
        # inner face: prescribed flux into cell 0 (outward flux of mu grad Phi equals enclosed mass 1)
        b[0] += Ar[0] * (1.0 / r_min ** 2)
        # theta faces
        k0 = idx[:, :-1].ravel(); k1 = idx[:, 1:].ravel()
        rows += [k0, k1]; cols += [k1, k0]; vals += [ct.ravel(), ct.ravel()]
        diag[:, :-1] -= ct; diag[:, 1:] -= ct
        rows.append(idx.ravel()); cols.append(idx.ravel()); vals.append(diag.ravel())
        A = sp.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(N, N))
        Pn = spla.spsolve(A, b.ravel()).reshape(nr, nt)
        ch = np.max(np.abs(Pn - P)) / max(1.0, np.max(np.abs(Pn)))
        P = P + omega * (Pn - P)
        hist.append(ch)
        if verbose and it % 10 == 0:
            print(it, ch, flush=True)
        if ch < tol:
            break
    Pg = np.vstack([P, phi_out[None, :]])
    dPr = (Pg[1:] - Pg[:-1]) / drc[:, None]                      # faces 1..nr
    M = rf[1:] ** 2 * np.einsum("ij,j->i", dPr, w_ang) / 2.0
    return dict(r=rf[1:], M=M, x_e=x_e, y_e=y_e, iters=it + 1, resid=hist[-1], mu_e=mu_e, L_e=L_e,
                M_far=(math.asin(math.sqrt(L_e / (1 + L_e))) / math.sqrt(L_e / (1 + L_e))) / (mu_e * math.sqrt(1 + L_e)),
                nr=nr, nt=nt)


# ---------------------------------------------------------------------------- projection
TT = np.linspace(0.0, 12.0, 2401)                                 # cosh substitution r = R cosh t


def delta_sigma(R, rgrid, Mgrid, M_beyond="const"):
    """Delta Sigma(R) of a spherical profile given M(<r) on rgrid (any units, consistent).
    M_cyl(R) = M(R) + int dM/dr(R cosh t) (1 - tanh t) R sinh t dt ;  Sigma = (1/2 pi R) int dM/dr(R cosh t)/cosh t dt.
    Outside rgrid: M_beyond='const' (dM/dr = 0) or 'linear' (dM/dr = last slope)."""
    R = np.atleast_1d(np.asarray(R, float))
    lr = np.log(rgrid)
    dMdr = np.gradient(Mgrid, lr) / rgrid
    tail = dMdr[-1] if M_beyond == "linear" else 0.0
    ch = np.cosh(TT); sh = np.sinh(TT); th_ = np.tanh(TT)
    r = R[:, None] * ch[None, :]
    lrr = np.log(r)
    f = np.interp(lrr, lr, dMdr, left=dMdr[0], right=tail)
    w = np.full(TT.size, TT[1] - TT[0]); w[0] *= 0.5; w[-1] *= 0.5
    Mcyl = np.interp(np.log(R), lr, Mgrid) + np.sum(f * (1 - th_) * R[:, None] * sh * w, axis=1)
    Sig = np.sum(f / ch * w, axis=1) / (2 * math.pi * R)
    return Mcyl / (math.pi * R ** 2) - Sig
