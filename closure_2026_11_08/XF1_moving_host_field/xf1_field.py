#!/usr/bin/env python3
"""XF1 field module (shared by xf1_hydro.py and xf1_grade.py): the forces of the Stage A system that AC15 did not carry.

Axisymmetric (ln r, theta) finite-volume grid, code units L0, V, rho_h (G = 1 inside the multipole sums; the physical
coupling kappa_q = 4 pi G rho_h L0^2/V^2 multiplies the result). Anomalous charge dq = q - rho_h per cell.

  gravity of the charge      a_grav = -grad Phi_q,   lap Phi_q = kappa_q dq                       (Legendre expansion, l <= LMAX)
  Legendre (W) force         a_chi  = +grad chi,     div[D grad chi] = kappa_q dq,  D = diag(1/(1+x_e), 1/(1+x_e), 1/(1+x_e)^2)
                             solved by the stretch zeta = s z, s = sqrt(1+x_e): chi(x) = s^3 Phi_N[m at stretched positions](X),
                             d_perp chi = s^3 d_perp Phi', d_z chi = s^4 d_zeta Phi'  (Stage A, A1g)
  static linear EFE start    dq_static solving  kappa_q dq = div_FV[ D grad(phi_body + Phi_q[dq]) ]  (Stage A, A1h), GMRES
kappa = 1/2 FITTED; not theory closed.
"""
import math
import numpy as np
from scipy.special import eval_legendre
from scipy.sparse.linalg import LinearOperator, gmres

LMAX = 24


def legendre_table(x, lmax=LMAX):
    """P_l(x) and dP_l/dtheta (= -sin(theta) P_l'(x)) for x = cos(theta), shapes (lmax+1, N)."""
    x = np.asarray(x, float); Pl = np.array([eval_legendre(l, x) for l in range(lmax + 1)])
    sint = np.sqrt(np.maximum(1 - x * x, 0.0)); dPl = np.zeros_like(Pl)
    den = np.where(np.abs(x * x - 1) > 1e-14, x * x - 1, 1e-14)
    for l in range(1, lmax + 1):
        dPl[l] = l * (x * Pl[l] - Pl[l - 1]) / den * (-sint)
    return Pl, dPl


class Grid:
    def __init__(self, re, te):
        self.re, self.te = np.asarray(re, float), np.asarray(te, float)
        self.NR, self.NT = len(re) - 1, len(te) - 1
        self.rc = 0.75 * (re[1:] ** 4 - re[:-1] ** 4) / (re[1:] ** 3 - re[:-1] ** 3)          # volume centroid radius
        self.tc = 0.5 * (te[1:] + te[:-1])
        cm, cp = np.cos(te[:-1]), np.cos(te[1:])
        self.dV = 2 * np.pi * ((re[1:] ** 3 - re[:-1] ** 3) / 3)[:, None] * (cm - cp)[None, :]
        self.AR = (re ** 2)[:, None] * (cm - cp)[None, :]                                        # radial face areas (NR+1, NT)
        self.AT = np.sin(te)[None, :] * ((re[1:] ** 2 - re[:-1] ** 2) / 2)[:, None]            # theta face areas (NR, NT+1)
        self.w_sphere = (cm - cp) / 2                                                           # sphere-average weights (sum 1)


class Multipole:
    """Legendre-expansion acceleration (G = 1, attractive toward positive charge) of an axisymmetric cell charge m[NR, NT]."""

    def __init__(self, grid, lmax=LMAX):
        self.g, self.L = grid, lmax
        self.Pl_c, _ = legendre_table(np.cos(grid.tc), lmax)                                     # at cell-centre angles
        self.ls = np.arange(lmax + 1)[:, None]

    def moments(self, m, rc=None, Pl=None):
        """shell moments mom[l, NR] = sum_j m[i, j] P_l(cos tc_j)."""
        Pl = self.Pl_c if Pl is None else Pl
        return np.einsum("it,lt->li", m, Pl)

    _LT = {}

    def _table(self, theta):
        key = (theta.shape, float(theta[0]), float(theta[-1]), len(theta))
        if key not in Multipole._LT:
            Multipole._LT[key] = legendre_table(np.cos(theta), self.L)
        return Multipole._LT[key]

    def accel(self, mom, r_sh, r_eval, theta_eval, extra_point=None):
        """a_r, a_theta at r_eval[Nr] x theta_eval[Nt] from shell moments at radii r_sh (sorted ascending).
        extra_point: (mass, radius) of a centred point charge added to the l = 0 interior sum (AC15's core cap)."""
        L = self.L; ls = self.ls
        Pl, dPl = self._table(np.asarray(theta_eval, float))                                     # (L+1, Nt), cached
        rs = np.asarray(r_sh, float); re_ = np.asarray(r_eval, float)
        # cumulative interior / exterior sums at each evaluation radius: shells with r_sh < r are interior
        inner_terms = mom * rs[None, :] ** ls                                                    # (L+1, NR)
        outer_terms = mom * rs[None, :] ** (-ls - 1.0)
        cin = np.concatenate([np.zeros((L + 1, 1)), np.cumsum(inner_terms, axis=1)], axis=1)     # (L+1, NR+1)
        cout = np.concatenate([np.cumsum(outer_terms[:, ::-1], axis=1)[:, ::-1], np.zeros((L + 1, 1))], axis=1)
        k = np.searchsorted(rs, re_, side="left")                                                # number of shells strictly inside r
        Il = cin[:, k]; El = cout[:, k]                                                          # (L+1, Nr)
        if extra_point is not None:
            Il[0] = Il[0] + extra_point
        rp = re_[None, :]
        Ar = (-(ls + 1) * rp ** (-ls - 2.0) * Il + ls * rp ** (ls - 1.0) * El)                  # (L+1, Nr) radial coefficient
        At = (rp ** (-ls - 1.0) * Il + rp ** ls * El) / rp                                       # (L+1, Nr) theta coefficient
        a_r = np.einsum("lr,lt->rt", Ar, Pl); a_t = np.einsum("lr,lt->rt", At, dPl)
        return a_r, a_t


class Forces:
    """the two charge forces on the khronon frame and the readout gravity, on a given grid."""

    def __init__(self, grid, xe, kq, lmax=LMAX, nshell_extra=None):
        self.g, self.xe, self.kq = grid, xe, kq
        self.mp = Multipole(grid, lmax); self.s = math.sqrt(1 + xe)
        g = grid
        # stretched geometry of the cell charges: (R, s z) -> (r', theta')
        R = g.rc[:, None] * np.sin(g.tc)[None, :]; Z = g.rc[:, None] * np.cos(g.tc)[None, :]
        self.rp_cells = np.sqrt(R ** 2 + (self.s * Z) ** 2); self.cosp_cells = self.s * Z / self.rp_cells
        # shells for the stretched charges: the grid's ln-r shells extended to s * r_out
        dln = math.log(g.re[1] / g.re[0]) / 4.0                                                  # stretched shells 4x finer than the grid
        nx = int(math.ceil(math.log(self.s * g.re[-1] / g.re[0]) / dln)) + 1
        self.re_s = g.re[0] * np.exp(dln * np.arange(nx + 1))
        self.rc_s = np.sqrt(self.re_s[1:] * self.re_s[:-1])
        self.ish = np.clip(np.searchsorted(self.re_s, self.rp_cells, side="right") - 1, 0, len(self.rc_s) - 1)
        self.Pl_s, _ = legendre_table(self.cosp_cells.ravel(), lmax)                            # (L+1, NR*NT) at stretched angles
        # evaluation geometry: cell centroids (for tests) and radial faces (for the forces: exact shell split), stretched
        self.Rc, self.Zc = R, Z
        self.rp_eval = self.rp_cells; self.thp_eval = np.arccos(np.clip(self.cosp_cells, -1, 1))
        Rf = g.re[:, None] * np.sin(g.tc)[None, :]; Zf = g.re[:, None] * np.cos(g.tc)[None, :]
        self.rp_face = np.sqrt(Rf ** 2 + (self.s * Zf) ** 2); self.thp_face = np.arccos(np.clip(self.s * Zf / self.rp_face, -1, 1))
        self._PLf = legendre_table(np.cos(self.thp_face.ravel()), lmax); self._PLc = legendre_table(np.cos(self.thp_eval.ravel()), lmax)

    # ---------------------------------------------------------------- gravity of the anomalous charge (G -> kq/4pi)
    def grav_at(self, dq, r_eval, theta_eval, core=None):
        m = dq * self.g.dV; mom = self.mp.moments(m)
        a_r, a_t = self.mp.accel(mom, self.g.rc, r_eval, theta_eval, extra_point=core)
        return a_r * self.kq / (4 * np.pi), a_t * self.kq / (4 * np.pi)

    def grav_cells(self, dq, faces=True):
        """charge gravity at the cell centroids (NR, NT): faces=True evaluated at the radial faces (exact shell split) and
        averaged; faces=False at the centroids (own shell counted exterior; tests)."""
        if not faces:
            return self.grav_at(dq, self.g.rc, self.g.tc)
        ar, at = self.grav_at(dq, self.g.re, self.g.tc)
        return 0.5 * (ar[1:] + ar[:-1]), 0.5 * (at[1:] + at[:-1])

    # ---------------------------------------------------------------- Legendre force grad chi at the cell centroids
    def chi_grad_cells(self, dq, faces=True):
        """grad chi at the cell centroids. faces=True: evaluated at the stretched radial faces (exact shell split) and averaged
        to the centroids (the hydro's force); faces=False: evaluated at the stretched centroids (tests)."""
        g = self.g; m = (dq * g.dV).ravel(); L = self.mp.L
        mom = np.zeros((L + 1, len(self.rc_s)))
        for l in range(L + 1):
            mom[l] = np.bincount(self.ish.ravel(), weights=m * self.Pl_s[l], minlength=len(self.rc_s))
        rp, thp, PL = (self.rp_face, self.thp_face, self._PLf) if faces else (self.rp_eval, self.thp_eval, self._PLc)
        a_rp, a_tp = self._accel_points(mom, self.rc_s, rp.ravel(), thp.ravel(), PL)
        a_rp = a_rp.reshape(rp.shape); a_tp = a_tp.reshape(rp.shape)
        aR = a_rp * np.sin(thp) + a_tp * np.cos(thp); aZ = a_rp * np.cos(thp) - a_tp * np.sin(thp)   # Cartesian in stretched space
        fR = -self.s ** 3 * aR * self.kq / (4 * np.pi); fZ = -self.s ** 4 * aZ * self.kq / (4 * np.pi)   # grad chi = -s^3 a'_R, -s^4 a'_zeta
        th = g.tc[None, :]
        f_r = fR * np.sin(th) + fZ * np.cos(th); f_t = fR * np.cos(th) - fZ * np.sin(th)
        if faces:
            f_r = 0.5 * (f_r[1:] + f_r[:-1]); f_t = 0.5 * (f_t[1:] + f_t[:-1])
        return f_r, f_t

    def _accel_points(self, mom, r_sh, r_pts, th_pts, PL=None):
        """as Multipole.accel but for paired (r, theta) points; PL = cached (Pl, dPl) at th_pts."""
        L = self.mp.L; ls = self.mp.ls
        Pl, dPl = legendre_table(np.cos(th_pts), L) if PL is None else PL
        rs = np.asarray(r_sh, float)
        inner_terms = mom * rs[None, :] ** ls; outer_terms = mom * rs[None, :] ** (-ls - 1.0)
        cin = np.concatenate([np.zeros((L + 1, 1)), np.cumsum(inner_terms, axis=1)], axis=1)
        cout = np.concatenate([np.cumsum(outer_terms[:, ::-1], axis=1)[:, ::-1], np.zeros((L + 1, 1))], axis=1)
        k = np.searchsorted(rs, r_pts, side="left")
        Il = cin[:, k]; El = cout[:, k]; rp = r_pts[None, :]
        Ar = (-(ls + 1) * rp ** (-ls - 2.0) * Il + ls * rp ** (ls - 1.0) * El)
        At = (rp ** (-ls - 1.0) * Il + rp ** ls * El) / rp
        return np.sum(Ar * Pl, axis=0), np.sum(At * dPl, axis=0)

    def frame_forces(self, dq, faces=True):
        """total extra force on the frame at the cell centroids: + grad chi (Legendre) - grav Phi_q (charge gravity)."""
        gr, gt = self.grav_cells(dq, faces); cr, ct = self.chi_grad_cells(dq, faces)
        return gr + cr, gt + ct, (gr, gt, cr, ct)

    # ---------------------------------------------------------------- static linear EFE solution (HEDGEHOG start of the galaxy cells)
    def _div_D_grad(self, grad_r_faces, grad_t_faces_r, grad_r_faces_t, grad_t_faces):
        """FV divergence of D grad phi from face gradients: radial faces (NR+1, NT): (d_r phi, (1/r) d_th phi);
        theta faces (NR, NT+1): (d_r phi, (1/r) d_th phi)."""
        g = self.g; Dpe, Dpa = 1 / (1 + self.xe), 1 / (1 + self.xe) ** 2
        tc = g.tc[None, :]; te = g.te[None, :]
        gz_r = grad_r_faces * np.cos(tc) - grad_t_faces_r * np.sin(tc)                           # d_z phi at radial faces
        Fr = Dpe * grad_r_faces + (Dpa - Dpe) * gz_r * np.cos(tc)
        gz_t = grad_r_faces_t * np.cos(te) - grad_t_faces * np.sin(te)
        Ft = Dpe * grad_t_faces + (Dpa - Dpe) * gz_t * (-np.sin(te))
        return (Fr[1:] * g.AR[1:] - Fr[:-1] * g.AR[:-1] + Ft[:, 1:] * g.AT[:, 1:] - Ft[:, :-1] * g.AT[:, :-1]) / (g.dV / (2 * np.pi))

    def static_start(self, gpar, mass_frac, tol=1e-8, maxiter=400):
        """dq_static (in rho_h units) of a body with Newtonian field gpar * mass_frac(r)/r^2 (code units), linear EFE response.
        Returns dq, info."""
        g = self.g
        def body_grad_faces():
            rr = g.re[:, None]; gr_r = gpar * mass_frac(rr) / rr ** 2 * np.ones((1, g.NT))
            rrc = g.rc[:, None]; gr_t = gpar * mass_frac(rrc) / rrc ** 2 * np.ones((1, g.NT + 1))
            return gr_r, np.zeros_like(gr_r), gr_t, np.zeros_like(gr_t)
        def charge_grad_faces(dq):
            ar_r, at_r = self.grav_at(dq, g.re, g.tc); ar_t, at_t = self.grav_at(dq, g.rc, g.te)
            return -ar_r, -at_r, -ar_t, -at_t                                                     # grad Phi_q = -a
        b = self._div_D_grad(*body_grad_faces()) / self.kq
        n = g.NR * g.NT
        def matvec(v):
            dq = v.reshape(g.NR, g.NT)
            return (dq - self._div_D_grad(*charge_grad_faces(dq)) / self.kq).ravel()
        A = LinearOperator((n, n), matvec=matvec, dtype=float)
        it = [0]
        def cb(_): it[0] += 1
        bn = float(np.linalg.norm(b.ravel()))
        with np.errstate(all="ignore"):
            x, flag = gmres(A, b.ravel() / bn, rtol=tol, maxiter=maxiter, restart=60, callback=cb, callback_type="pr_norm")
        x = x * bn; method = "gmres"
        if flag != 0 or not np.all(np.isfinite(x)):                                                # Picard fallback (contraction ~ D)
            x = b.ravel().copy(); method = "picard"
            for k in range(2000):
                xn = b.ravel() + (x - matvec(x)); ch = float(np.max(np.abs(xn - x))); x = xn; it[0] = k + 1
                if ch < tol * bn: break
        dq = x.reshape(g.NR, g.NT)
        res = np.linalg.norm(matvec(x) - b.ravel()) / max(bn, 1e-300)
        info = dict(method=method, gmres_flag=int(flag), iterations=it[0], rel_residual=float(res), dq_min_linear=float(dq.min()), dq_max_linear=float(dq.max()))
        info.update(dq_min=float(dq.min()), dq_max=float(dq.max()))
        return dq, info



def plummer_mass_frac(a_code):
    if a_code <= 0:
        return lambda r: np.ones_like(np.asarray(r, float))
    return lambda r: (np.asarray(r, float) / a_code) ** 3 / (1 + (np.asarray(r, float) / a_code) ** 2) ** 1.5


# ---------------------------------------------------------------------- self-tests (run as a script)
if __name__ == "__main__":
    import json, sys
    out = {}
    re = 0.05 * np.exp(0.05 * np.arange(139)); te = np.linspace(0, np.pi, 81)
    G_ = Grid(re, te)
    # T1 point-like charge in the innermost shell: gravity -Q/r^2, Legendre force = anisotropic Coulomb (Stage A A1h with D)
    for xe in (0.0, 0.9):
        F = Forces(G_, xe, kq=4 * np.pi)                                                           # kq/(4 pi) = 1: G = 1
        dq = np.zeros((G_.NR, G_.NT)); dq[0] = 1.0 / G_.dV[0].sum()                               # unit charge, spread over the first shell
        gr, gt = F.grav_cells(dq, faces=False); cr, ct = F.chi_grad_cells(dq, faces=False)
        s = math.sqrt(1 + xe); Dpe, Dpa = 1 / (1 + xe), 1 / (1 + xe) ** 2
        R = F.Rc; Z = F.Zc; den = np.sqrt(R ** 2 / Dpe + Z ** 2 / Dpa)
        # chi = -Q/(sqrt(Dpa) Dpe den)  ->  grad chi
        pref = 1 / (math.sqrt(Dpa) * Dpe)
        dchi_R = pref * (R / Dpe) / den ** 3; dchi_Z = pref * (Z / Dpa) / den ** 3
        th = G_.tc[None, :]
        ex_r = dchi_R * np.sin(th) + dchi_Z * np.cos(th); ex_t = dchi_R * np.cos(th) - dchi_Z * np.sin(th)
        sel = slice(int(np.searchsorted(G_.rc, 1.0)), None)                                    # r >= 1: 20 x the shell radius
        e_g = float(np.max(np.abs(gr[sel] * G_.rc[sel, None] ** 2 + 1))) ; e_gt = float(np.max(np.abs(gt[sel] * G_.rc[sel, None] ** 2)))
        e_c = float(np.max(np.abs(cr[sel] - ex_r[sel]) / np.abs(ex_r[sel]).max(axis=1, keepdims=True)))
        e_ct = float(np.max(np.abs(ct[sel] - ex_t[sel]) / np.abs(ex_r[sel]).max(axis=1, keepdims=True)))
        out[f"T1_xe{xe}"] = dict(grav_radial_rel=e_g, grav_theta=e_gt, chi_r_rel=e_c, chi_t_rel=e_ct)
        print(f"T1 x_e {xe}: point charge, r >= 1 (20 x the shell radius): gravity |a_r r^2 + 1| max {e_g:.2e}, |a_t r^2| {e_gt:.2e}; "
              f"Legendre grad chi vs anisotropic Coulomb: radial rel {e_c:.2e}, theta rel {e_ct:.2e}")
    # T2 static start of a Plummer body: the residual of the linear system and the sphere-averaged field vs Newton
    F = Forces(G_, 0.85, kq=1e-5)
    dq, info = F.static_start(1e-4, plummer_mass_frac(1.0))
    ar, at = F.grav_at(dq, np.array([1.0]), G_.tc)
    gN = 1e-4 * plummer_mass_frac(1.0)(1.0)
    gsph = gN + float(np.sum(-ar[0] * G_.w_sphere))
    out["T2"] = dict(info=info, g_static_over_gN_at_a=gsph / gN, q_min_total=float(1 + dq.min()))
    print(f"T2 Plummer x_e 0.85 gpar 1e-4 kq 1e-5: {info}; g_static/g_N at r = a (sphere) {gsph / gN:.4f}; min(1 + dq) {1 + dq.min():.3f}")
    json.dump(out, open(sys.argv[1], "w"), indent=1) if len(sys.argv) > 1 else None


# ---------------------------------------------------------------------- finite-volume anisotropic Poisson operator (the hydro's force kernel)
import scipy.sparse as _sp
import scipy.sparse.linalg as _spl


class FVPoisson:
    """div_FV[D grad u] = rhs on the (ln r, theta) grid, D = diag(Dperp, Dperp, Dpar) in Cartesian (axis z), cell-centred u.
    Faces: radial (D grad u).r^ = Dperp u_r + (Dpar - Dperp) cos(th) u_z,  u_z = cos(th) u_r - sin(th) u_th/r;
           theta  (D grad u).th^ = Dperp u_th/r + (Dpar - Dperp)(-sin(th)) u_z.
    u_r across a radial face by the two-point difference, u_th/r at a radial face by the mean of the two cells' central
    theta differences (reflected at the axes), and symmetrically at theta faces. Zero flux at r_in (inside the body / excised
    core), u = 0 at r_out (Dirichlet; the error at the readout is O((a/r_out)^3)), zero theta flux at the axes (sin = 0).
    Prefactorised (splu); solve(rhs) returns u. face_grad(u) returns the face gradient components used by the fluxes."""

    def __init__(self, grid, Dpar, Dperp):
        g = self.g = grid; NR, NT = g.NR, g.NT; n = NR * NT; self.Dpar, self.Dperp = Dpar, Dperp
        rc, re, tc, te = g.rc, g.re, g.tc, g.te; dth = tc[1] - tc[0]
        k = lambda i, j: i * NT + j
        rows, cols, vals = [], [], []
        vol = g.dV / (2 * np.pi)
        def add(i, j, i2, j2, v):
            rows.append(k(i, j)); cols.append(k(i2, j2)); vals.append(v)
        # radial faces m = 1..NR-1 between cells (m-1, j) and (m, j); m = 0 zero flux; m = NR Dirichlet 0 beyond
        for m in range(1, NR + 1):
            rf = re[m]
            for j in range(NT):
                th = tc[j]; cs, sn = math.cos(th), math.sin(th)
                area = g.AR[m, j]
                # coefficient structure: flux = A * u_r + B * (u_th / r) with
                A = Dperp + (Dpar - Dperp) * cs * cs; B = -(Dpar - Dperp) * cs * sn
                terms = {}                                        # (i, j) -> coefficient in the flux
                if m < NR:
                    dr = rc[m] - rc[m - 1]
                    terms[(m, j)] = terms.get((m, j), 0) + A / dr; terms[(m - 1, j)] = terms.get((m - 1, j), 0) - A / dr
                    for ii in (m - 1, m):                          # u_th/r at the face: mean of the two cells' central differences
                        jp, jm = min(j + 1, NT - 1), max(j - 1, 0)
                        c_ = B / (2 * dth * rf) * 0.5
                        terms[(ii, jp)] = terms.get((ii, jp), 0) + c_; terms[(ii, jm)] = terms.get((ii, jm), 0) - c_
                else:                                             # outer: ghost value 0 at the ghost centroid
                    dr = (re[NR] * math.exp(0.5 * math.log(re[NR] / re[NR - 1]))) - rc[NR - 1]
                    terms[(NR - 1, j)] = terms.get((NR - 1, j), 0) - A / dr
                    jp, jm = min(j + 1, NT - 1), max(j - 1, 0); c_ = B / (2 * dth * rf) * 0.5
                    terms[(NR - 1, jp)] = terms.get((NR - 1, jp), 0) + c_; terms[(NR - 1, jm)] = terms.get((NR - 1, jm), 0) - c_
                for (ii, jj), c_ in terms.items():
                    if m < NR:
                        add(m, j, ii, jj, -c_ * area / vol[m, j]); add(m - 1, j, ii, jj, c_ * area / vol[m - 1, j])
                    else:
                        add(NR - 1, j, ii, jj, c_ * area / vol[NR - 1, j])
        # theta faces p = 1..NT-1 between cells (i, p-1) and (i, p)
        for i in range(NR):
            r_ = rc[i]
            for p in range(1, NT):
                th = te[p]; cs, sn = math.cos(th), math.sin(th); area = g.AT[i, p]
                A = Dperp + (Dpar - Dperp) * sn * sn                 # flux = A * (u_th/r) + B * u_r
                B = -(Dpar - Dperp) * cs * sn
                terms = {}
                terms[(i, p)] = terms.get((i, p), 0) + A / (r_ * dth); terms[(i, p - 1)] = terms.get((i, p - 1), 0) - A / (r_ * dth)
                for jj in (p - 1, p):                               # u_r at the theta face: mean of the two cells' radial central differences
                    ip, im = min(i + 1, NR - 1), max(i - 1, 0)
                    if ip != im:
                        c_ = B / (rc[ip] - rc[im]) * 0.5
                        terms[(ip, jj)] = terms.get((ip, jj), 0) + c_; terms[(im, jj)] = terms.get((im, jj), 0) - c_
                for (ii, jj), c_ in terms.items():
                    add(i, p, ii, jj, -c_ * area / vol[i, p]); add(i, p - 1, ii, jj, c_ * area / vol[i, p - 1])
        self.A = _sp.csc_matrix((vals, (rows, cols)), shape=(n, n))
        self.lu = _spl.splu(self.A)

    def solve(self, rhs):
        return self.lu.solve(np.asarray(rhs, float).ravel()).reshape(self.g.NR, self.g.NT)

    def face_grad(self, u):
        """(u_r, u_th/r) at radial faces (NR+1, NT) and at theta faces (NR, NT+1), with the same differencing as the operator."""
        g = self.g; rc, re, tc, te = g.rc, g.re, g.tc, g.te; dth = tc[1] - tc[0]; NR, NT = g.NR, g.NT
        ur_r = np.zeros((NR + 1, NT)); ut_r = np.zeros((NR + 1, NT))
        ur_r[1:NR] = (u[1:] - u[:-1]) / (rc[1:] - rc[:-1])[:, None]
        rg = re[NR] * math.exp(0.5 * math.log(re[NR] / re[NR - 1])); ur_r[NR] = (0.0 - u[-1]) / (rg - rc[-1])
        uth = np.zeros_like(u); uth[:, 1:-1] = (u[:, 2:] - u[:, :-2]) / (2 * dth); uth[:, 0] = (u[:, 1] - u[:, 0]) / (2 * dth); uth[:, -1] = (u[:, -1] - u[:, -2]) / (2 * dth)
        ut_r[1:NR] = 0.5 * (uth[1:] + uth[:-1]) / re[1:NR, None]; ut_r[NR] = uth[-1] / re[NR]
        ur_t = np.zeros((NR, NT + 1)); ut_t = np.zeros((NR, NT + 1))
        ut_t[:, 1:NT] = (u[:, 1:] - u[:, :-1]) / (rc[:, None] * dth)
        urr = np.zeros_like(u); urr[1:-1] = (u[2:] - u[:-2]) / (rc[2:] - rc[:-2])[:, None]; urr[0] = (u[1] - u[0]) / (rc[1] - rc[0]); urr[-1] = (u[-1] - u[-2]) / (rc[-1] - rc[-2])
        ur_t[:, 1:NT] = 0.5 * (urr[:, 1:] + urr[:, :-1])
        return ur_r, ut_r, ur_t, ut_t

    def centroid_grad(self, u):
        """grad u at the centroids (r, theta components) as the mean of the bounding radial faces."""
        ur_r, ut_r, _, _ = self.face_grad(u)
        return 0.5 * (ur_r[1:] + ur_r[:-1]), 0.5 * (ut_r[1:] + ut_r[:-1])


class FVForces:
    """the hydro's force kernel: everything from one FV operator family on the grid (consistent to roundoff).
    kq = kappa_q; body rhs = kq * rho_b (code units) given as a cell array; forces at the centroids."""

    def __init__(self, grid, xe, kq):
        self.g, self.xe, self.kq = grid, xe, kq
        Dpa, Dpe = 1 / (1 + xe) ** 2, 1 / (1 + xe)
        self.LI = FVPoisson(grid, 1.0, 1.0); self.LD = FVPoisson(grid, Dpa, Dpe); self.LS = FVPoisson(grid, 1 - Dpa, 1 - Dpe)
        self.Dpa, self.Dpe = Dpa, Dpe

    def div_D_grad(self, u):
        g = self.g; ur_r, ut_r, ur_t, ut_t = self.LD.face_grad(u); Dpe, Dpa = self.Dpe, self.Dpa
        tc = g.tc[None, :]; te = g.te[None, :]
        Fr = Dpe * ur_r + (Dpa - Dpe) * (np.cos(tc) * ur_r - np.sin(tc) * ut_r) * np.cos(tc)
        Ft = Dpe * ut_t + (Dpa - Dpe) * (np.cos(te) * ur_t - np.sin(te) * ut_t) * (-np.sin(te))
        Fr[0] = 0.0; Ft[:, 0] = 0.0; Ft[:, -1] = 0.0
        return (Fr[1:] * g.AR[1:] - Fr[:-1] * g.AR[:-1] + Ft[:, 1:] * g.AT[:, 1:] - Ft[:, :-1] * g.AT[:, :-1]) / (g.dV / (2 * np.pi))

    def inner_source(self, f_in):
        """the flux f_in (= grad phi at r_in, the body's enclosed mass inside the excised r_in) as a source on the first cells:
        the operators carry zero flux at r_in, so L phi = rhs + f_in AR[0]/vol[0] reproduces (F1 AR1 - f_in AR0)/vol = rhs there."""
        g = self.g; src = np.zeros((g.NR, g.NT)); src[0] = f_in * g.AR[0] / (g.dV[0] / (2 * np.pi))
        return src

    def body(self, rho_b_code, f_in=0.0):
        """phi_body on the grid and its centroid gradient (gr, gt); rho_b_code in rho_h units; f_in the inner-face flux."""
        phi = self.LI.solve(self.kq * rho_b_code + self.inner_source(f_in)); gr, gt = self.LI.centroid_grad(phi)
        return phi, gr, gt

    def static_start(self, rho_b_code, f_in=0.0):
        """linear static EFE phantom (A1h): div[(I - D) grad phi_t] = kq rho_b (+ the same inner source), dq = div[D grad phi_t]/kq;
        an exact discrete fixed point of frame_forces + body."""
        phi_t = self.LS.solve(self.kq * rho_b_code + self.inner_source(f_in))
        return self.div_D_grad(phi_t) / self.kq, phi_t

    def frame_forces(self, dq):
        """+ grad chi (Legendre) - grad Phi_q (charge gravity) at the centroids."""
        chi = self.LD.solve(self.kq * dq); Phi = self.LI.solve(self.kq * dq)
        cr, ct = self.LD.centroid_grad(chi); pr, pt = self.LI.centroid_grad(Phi)
        return cr - pr, ct - pt, (-pr, -pt, cr, ct)


def d10_static_phantom(grid, y, xe, Lam, a0_SI, a_m, rho_h_SI, repo):
    """the record's nonlinear static EFE phantom (D10's Solver2D on X1/SE2's call) interpolated to the grid, in rho_h units.
    dq_phys = (a0/(K a)) div p, K = 4 pi G, lengths in a. Returns (s, info)."""
    import sys, os
    sys.path.insert(0, os.path.join(repo, "doors_push_2026_10_22", "D10_native_Lstar"))
    import d10_solver as S
    G2 = S.Grid2D(nper=24, Nt=16); sv = S.Solver2D(G2, y, 0.0 if xe <= 0 else xe, Lam, isolated=xe <= 0); U, res, it = sv.solve(tol=1e-10)
    D, _, _ = sv.divp(U[:G2.n]); D = np.asarray(D).reshape(G2.Nr, G2.Nt)
    G_SI = 6.67430e-11
    s_d10 = D * a0_SI / (4 * np.pi * G_SI * a_m * rho_h_SI)
    # bilinear interpolation in (ln r, theta) onto the grid centroids (constant beyond D10's range)
    lr_src = np.log(G2.rc); th_src = G2.tc
    lr = np.log(grid.rc); th = grid.tc
    ir = np.clip(np.searchsorted(lr_src, lr) - 1, 0, len(lr_src) - 2); jt = np.clip(np.searchsorted(th_src, th) - 1, 0, len(th_src) - 2)
    fr = np.clip((lr - lr_src[ir]) / (lr_src[ir + 1] - lr_src[ir]), 0, 1)[:, None]; ft = np.clip((th - th_src[jt]) / (th_src[jt + 1] - th_src[jt]), 0, 1)[None, :]
    s = ((1 - fr) * (1 - ft) * s_d10[np.ix_(ir, jt)] + fr * (1 - ft) * s_d10[np.ix_(ir + 1, jt)] + (1 - fr) * ft * s_d10[np.ix_(ir, jt + 1)] + fr * ft * s_d10[np.ix_(ir + 1, jt + 1)])
    return s, dict(d10_res=float(res), d10_it=int(it), s_min=float(s.min()), s_max=float(s.max()), d10_Nr=G2.Nr, d10_Nt=G2.Nt)
