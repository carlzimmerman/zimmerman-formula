"""SCS2 backgrounds: the law's static equation div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho_b, mu(x) = x/(1+x), solved by
finite volume on (x = ln r, theta, phi) with Picard iteration and sparse direct solves (the scheme of the record's
closure_2026_11_06/QX4_udg/aqual.py, generalised: full theta range when the plane symmetry is broken, phi cells for an
in-plane external field, a far-field Dirichlet boundary for an external field).  Criteria FROZEN_CRITERIA.md (158c4cf770),
amendment A1 (847f24db0b).  Units: kpc, km/s, Msun; G = 4.30091e-6 kpc (km/s)^2/Msun.

As a module it provides the solver, the backgrounds and the D.P (phantom) maps.  Run as a script it solves every frozen
background, runs the known answers KA1 (point mass), KA2 (Kuzmin closed form), KA4 (residual, two resolutions), KA5
(phantom mass), writes scs2_maps.json / .out and caches the solutions (npz) in $SCS2_CACHE for the two routes.
"""
import os, sys, json, math, time, resource
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla

HERE = os.path.dirname(os.path.abspath(__file__))
G = 4.30091e-6
CONV = 1e6 / 3.0857e19                     # (km/s)^2/kpc -> m/s^2
C_KMS = 2.99792458e5
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LOGM = ["9.4", "10.45", "10.7", "10.9"]


def a0k(foot): return A0[foot] / CONV


def R_d_shen(M):
    """Shen et al. 2003, late types, eq. 18 (quoted from memory): R_50 = 0.10 kpc M^0.14 (1 + M/3.98e10)^0.25; R_d = R_50/1.678."""
    return 0.10 * M ** 0.14 * (1 + M / 3.98e10) ** 0.25 / 1.678


def h_z_bershady(Rd): return 0.196 * Rd ** 0.633


class Grid:
    """cells in ln r (nr), theta (nt), phi (np_).  tmode 'half': theta in [0, pi/2] (plane mirror); 'full': [0, pi].
    np_ = 1: axisymmetric (full turn); np_ > 1: phi in [0, pi] (y mirror)."""
    def __init__(self, r_min, r_max, nr, nt, np_=1, tmode="half", p=2.0):
        self.xf = np.linspace(math.log(r_min), math.log(r_max), nr + 1)
        self.xc = 0.5 * (self.xf[1:] + self.xf[:-1]); self.dx = self.xf[1] - self.xf[0]
        self.rf = np.exp(self.xf); self.rc = np.exp(self.xc)
        if tmode == "half":
            s = np.linspace(0, 1, nt + 1); self.tf = 0.5 * np.pi * (1 - (1 - s) ** p)
        else:
            s = np.linspace(-1, 1, nt + 1); self.tf = 0.5 * np.pi + 0.5 * np.pi * np.sign(s) * np.abs(s) ** p
            self.tf[0], self.tf[-1] = 0.0, np.pi
        self.tc = 0.5 * (self.tf[1:] + self.tf[:-1])
        self.pf = np.array([0.0, 2 * np.pi]) if np_ == 1 else np.linspace(0, np.pi, np_ + 1)
        self.pc = 0.5 * (self.pf[1:] + self.pf[:-1])
        self.nr, self.nt, self.np_, self.tmode = nr, nt, np_, tmode
        self.shape = (nr, nt, np_); self.n = nr * nt * np_
        dcos = np.cos(self.tf[:-1]) - np.cos(self.tf[1:]); dph = np.diff(self.pf)
        self.V = ((self.rf[1:] ** 3 - self.rf[:-1] ** 3) / 3)[:, None, None] * dcos[None, :, None] * dph[None, None, :]
        self.mult = (2.0 if tmode == "half" else 1.0) * (2.0 if np_ > 1 else 1.0)     # mirror copies
        self.R = self.rc[:, None, None] * np.sin(self.tc)[None, :, None] * np.ones(self.shape)
        self.Z = self.rc[:, None, None] * np.cos(self.tc)[None, :, None] * np.ones(self.shape)
        self.X = self.R * np.cos(self.pc)[None, None, :]; self.Y = self.R * np.sin(self.pc)[None, None, :]
        self.solid = dcos[None, :, None] * dph[None, None, :] * np.ones((1, nt, np_))


def faces(g):
    """face lists: (k1, k2, area, dist, kind, ...) for interior faces, Dirichlet outer faces, and inner faces."""
    nr, nt, np_ = g.shape
    idx = np.arange(g.n).reshape(g.shape)
    dcos = np.cos(g.tf[:-1]) - np.cos(g.tf[1:]); dph = np.diff(g.pf); dth = np.diff(g.tf)
    F = {}
    # r faces between i and i+1
    A = (g.rf[1:-1] ** 2)[:, None, None] * dcos[None, :, None] * dph[None, None, :]
    d = (g.rc[1:] - g.rc[:-1])[:, None, None] * np.ones((1, nt, np_))
    F["r"] = (idx[:-1].ravel(), idx[1:].ravel(), A.ravel(), d.ravel())
    # outer Dirichlet faces at r_max
    Ao = (g.rf[-1] ** 2) * dcos[:, None] * dph[None, :]
    F["out"] = (idx[-1].ravel(), Ao.ravel(), np.full(nt * np_, g.rf[-1] - g.rc[-1]))
    # theta faces between j and j+1
    if nt > 1:
        At = ((g.rf[1:] ** 2 - g.rf[:-1] ** 2) / 2)[:, None, None] * np.sin(g.tf[1:-1])[None, :, None] * dph[None, None, :]
        dt = g.rc[:, None, None] * (g.tc[1:] - g.tc[:-1])[None, :, None] * np.ones((1, 1, np_))
        F["t"] = (idx[:, :-1].ravel(), idx[:, 1:].ravel(), At.ravel(), dt.ravel())
    if np_ > 1:
        Ap = ((g.rf[1:] ** 2 - g.rf[:-1] ** 2) / 2)[:, None, None] * dth[None, :, None] * np.ones((1, 1, np_ - 1))
        dp = (g.rc[:, None, None] * np.sin(g.tc)[None, :, None]) * (g.pc[1:] - g.pc[:-1])[None, None, :]
        F["p"] = (idx[:, :, :-1].ravel(), idx[:, :, 1:].ravel(), Ap.ravel(), dp.ravel())
    return F


def cell_gradient(g, Phi, Phib):
    """cell-centred gradient (g_r, g_t, g_p) with ghost cells: mirror at the inner sphere, axis, symmetry planes and phi
    ends; Dirichlet ghost at r_max."""
    P = Phi
    Pr = np.concatenate([P[:1], P, (2 * Phib - P[-1:])], axis=0)
    rc = np.concatenate([[g.rc[0] * math.exp(-g.dx)], g.rc, [g.rc[-1] * math.exp(g.dx)]])
    gr = (Pr[2:] - Pr[:-2]) / (rc[2:] - rc[:-2])[:, None, None]
    Pt = np.concatenate([P[:, :1], P, P[:, -1:]], axis=1)
    tc = np.concatenate([[-g.tc[0]], g.tc, [(np.pi if g.tmode == "half" else 2 * np.pi) - g.tc[-1]]])
    gt = (Pt[:, 2:] - Pt[:, :-2]) / (tc[2:] - tc[:-2])[None, :, None] / g.rc[:, None, None]
    if g.np_ > 1:
        Pp = np.concatenate([P[:, :, :1], P, P[:, :, -1:]], axis=2)
        pc = np.concatenate([[-g.pc[0]], g.pc, [2 * np.pi - g.pc[-1]]])
        gp = (Pp[:, :, 2:] - Pp[:, :, :-2]) / (pc[2:] - pc[:-2])[None, None, :] / (g.rc[:, None, None] * np.sin(g.tc)[None, :, None])
    else:
        gp = np.zeros_like(P)
    return gr, gt, gp


def face_mu(g, F, Phi, Phib, a0, mu_one, gr, gt, gp):
    """mu at every face from the normal difference and the averaged tangential components."""
    out = {}
    Pf = Phi.ravel(); comps = [gr.ravel(), gt.ravel(), gp.ravel()]
    for key, normal in (("r", 0), ("t", 1), ("p", 2)):
        if key not in F: continue
        k1, k2, A, d = F[key]
        gn = (Pf[k2] - Pf[k1]) / d
        tan2 = sum((0.5 * (comps[c][k1] + comps[c][k2])) ** 2 for c in range(3) if c != normal)
        x = np.sqrt(gn ** 2 + tan2) / a0
        out[key] = np.ones_like(x) if mu_one else x / (1 + x)
    k1, A, d = F["out"]
    gn = (Phib.ravel() - Pf[k1]) / d
    tan2 = comps[1][k1] ** 2 + comps[2][k1] ** 2
    x = np.sqrt(gn ** 2 + tan2) / a0
    out["out"] = np.ones_like(x) if mu_one else x / (1 + x)
    return out


def operator(g, F, coef):
    """flux operator: (A Phi)_k = sum_faces coef_f (Phi_k' - Phi_k) [interior] - coef_out Phi_k [Dirichlet part]."""
    rows, cols, vals = [], [], []
    diag = np.zeros(g.n)
    for key in ("r", "t", "p"):
        if key not in F: continue
        k1, k2, A, d = F[key]
        c = coef[key] * A / d
        rows += [k1, k2, k1, k2]; cols += [k2, k1, k1, k2]; vals += [c, c, -c, -c]
    k1, A, d = F["out"]
    cout = coef["out"] * A / d
    np.add.at(diag, k1, -cout)
    M = sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(g.n, g.n))
    return M + sps.diags(diag), cout, k1


def solve(g, Mcell, Min, Phib, a0, mu_one=False, tol=1e-8, maxit=600, omega=0.7, verbose=False):
    """Picard iteration; Mcell: mass per cell (domain fraction), Min: total mass inside r_min (spherical share)."""
    F = faces(g)
    b = 4 * np.pi * G * (Mcell + Min * g.solid[0][None, :, :] / (4 * np.pi) * (np.arange(g.nr) == 0)[:, None, None])
    b = b.ravel()
    Phi = np.zeros(g.shape) + Phib.mean()
    hist = []
    for it in range(maxit):
        gr, gt, gp = cell_gradient(g, Phi, Phib)
        mu = face_mu(g, F, Phi, Phib, a0, mu_one if it > 0 else True, gr, gt, gp)
        if it == 0: mu = {k_: np.ones_like(v) for k_, v in mu.items()}
        A, cout, kout = operator(g, F, mu)
        rhs = b.copy(); np.add.at(rhs, kout, -cout * Phib.ravel())
        res = np.linalg.norm(A @ Phi.ravel() - rhs) / np.linalg.norm(rhs)
        hist.append(res)
        if it > 0 and res < tol: break
        new = spla.spsolve(A.tocsc(), rhs).reshape(g.shape)
        Phi = new if it == 0 else Phi + omega * (new - Phi)
        if mu_one and it == 0:
            Phi = new
    return Phi, hist[-1], len(hist)


def phantom(g, Phi, Phib, Mcell, a0):
    """K D.P per cell from the finite-volume divergence of grad Phi/(1+u) = lap Phi - mu-flux; returns D.P density
    (Msun/kpc^3) and the cell gradient.  The innermost shell is masked (its inner face carries the enclosed-mass flux)."""
    F = faces(g)
    gr, gt, gp = cell_gradient(g, Phi, Phib)
    mu = face_mu(g, F, Phi, Phib, a0, False, gr, gt, gp)
    coef = {k_: 1 - v for k_, v in mu.items()}                       # 1/(1+u) = 1 - mu
    A, cout, kout = operator(g, F, coef)
    rhs = np.zeros(g.n); np.add.at(rhs, kout, -cout * Phib.ravel())
    flux = (A @ Phi.ravel() - rhs).reshape(g.shape)                  # sum_faces (1/(1+u)) grad Phi . n A
    dp = flux / (4 * np.pi * G * g.V)
    dp[:20] = np.nan                                              # amendments A2/A3: first 20 shells masked
    return dp, (gr, gt, gp)


def gauss_phantom(bg, r_target):
    """phantom mass inside the sphere through the r-face nearest r_target: flux of grad Phi/(1+u) over 4 pi G, minus nothing
    (the baryons enter through mu-flux); equals lap-flux/(4 pi G) - M_b(<r)."""
    g = bg["g"]; Phi = bg["Phi"]; Phib = bg["Phib"]
    F = faces(g)
    gr, gt, gp = bg["grads"]
    mu = face_mu(g, F, Phi, Phib, bg["a0"], False, gr, gt, gp)
    i = int(np.argmin(np.abs(g.rf[1:-1] - r_target)))          # face between cells i and i+1
    k1, k2, A, d = F["r"]
    sel = np.zeros(len(k1), bool)
    per = g.nt * g.np_
    sel[i * per:(i + 1) * per] = True
    Pf = Phi.ravel()
    flux = np.sum(((1 - mu["r"]) * A / d * (Pf[k2] - Pf[k1]))[sel])
    return float(flux / (4 * np.pi * G) * g.mult), float(g.rf[i + 1])


# ------------------------------------------------------------------ backgrounds
def far_field(g, M, a0, ge, axis):
    """Dirichlet values at r_max.  Isolated: constant.  External field ge (units of a0) along 'z' or 'x' (in plane)."""
    r = g.rf[-1]
    T = g.tc[:, None] * np.ones((1, g.np_)); Pp = g.pc[None, :] * np.ones((g.nt, 1))
    if ge == 0:
        return np.full((g.nt, g.np_), -math.sqrt(G * M * a0) * math.log(r))
    gek = ge * a0; xe = ge
    mue = xe / (1 + xe); Le = 1 / (1 + xe)
    par = r * np.cos(T) if axis == "z" else r * np.sin(T) * np.cos(Pp)
    perp2 = r ** 2 - par ** 2
    return gek * par - G * M / (mue * math.sqrt(1 + Le)) / np.sqrt(perp2 + par ** 2 / (1 + Le))


def deposit(g, kind, M, Rd):
    """mass per cell (the domain's share) and the mass inside r_min."""
    nr, nt, np_ = g.shape
    frac_phi = np.diff(g.pf) / (2 * np.pi)
    Mc = np.zeros(g.shape)
    rmin = g.rf[0]
    if kind in ("expo", "kuzmin", "expo+bulge"):
        if kind == "kuzmin":
            a = Rd; Menc = lambda R: M * (1 - a / np.sqrt(R ** 2 + a ** 2))
        else:
            Menc = lambda R: M * (1 - (1 + R / Rd) * np.exp(-R / Rd))
        Md = M * (0.8 if kind == "expo+bulge" else 1.0)
        shell = (Menc(g.rf[1:]) - Menc(g.rf[:-1])) * (Md / M)
        if g.tmode == "half":
            Mc[:, -1, :] += 0.5 * shell[:, None] * frac_phi[None, :]
        else:
            jm = g.nt // 2
            Mc[:, jm - 1, :] += 0.5 * shell[:, None] * frac_phi[None, :]
            Mc[:, jm, :] += 0.5 * shell[:, None] * frac_phi[None, :]
        Min = Menc(rmin) * (Md / M)
        if kind == "expo+bulge":
            ab = 0.2 * Rd; Mb_ = 0.2 * M
            Mh = lambda r: Mb_ * r ** 2 / (r + ab) ** 2
            sh = Mh(g.rf[1:]) - Mh(g.rf[:-1])
            Mc += sh[:, None, None] * g.solid / (4 * np.pi)
            Min += Mh(rmin)
        return Mc, Min
    if kind == "thick":
        hz = h_z_bershady(Rd); rho0 = M / (4 * np.pi * Rd ** 2 * hz)
        nsub = 5; u = (np.arange(nsub) + 0.5) / nsub
        for i in range(nr):
            r = np.exp(g.xf[i] + u * g.dx)
            for j in range(nt):
                t = g.tf[j] + u * (g.tf[j + 1] - g.tf[j])
                R = r[:, None] * np.sin(t)[None, :]; z = r[:, None] * np.cos(t)[None, :]
                w = (r ** 3)[:, None] * np.sin(t)[None, :] * (g.dx / nsub) * ((g.tf[j + 1] - g.tf[j]) / nsub)
                Mc[i, j, :] = np.sum(rho0 * np.exp(-R / Rd - np.abs(z) / hz) * w) * np.diff(g.pf)
        # mass inside r_min: small; take the thin-disc estimate
        Min = M * (1 - (1 + rmin / Rd) * math.exp(-rmin / Rd))
        return Mc, Min
    if kind == "point":
        return Mc, M
    raise ValueError(kind)


def make_grid(kind, M, Rd, a0, ge, axis, res):
    """res: 0 coarse (48 x 24), 1 fine (72 x 36); 3D in-plane: nr 48, ntheta 16, nphi 16."""
    rM = math.sqrt(G * M / a0)
    re = (math.sqrt(G * M * a0) / (ge * a0)) if ge > 0 else 0.0
    r_max = max(1e3 * Rd, 10 * re)
    r_min = 1e-4 * Rd                                            # amendment A2 (was 0.02 R_d); spacing kept
    scale = math.log(r_max / r_min) / math.log(r_max / (0.02 * Rd))
    if ge > 0 and axis == "x":
        return Grid(r_min, r_max, int(round(48 * scale)), 16, 16, "half")
    nr, nt = ((48, 24), (72, 36))[res]
    nr = int(round(nr * scale))
    if ge > 0 and axis == "z":
        return Grid(r_min, r_max, nr, 2 * nt, 1, "full")
    return Grid(r_min, r_max, nr, nt, 1, "half")


def background(foot, kind, logm, ge=0.0, axis="z", res=1, Rd_fac=1.0):
    M = 10 ** float(logm); a0 = a0k(foot)
    Rd = R_d_shen(M) * Rd_fac
    dkind = kind if kind != "point" else "point"
    g = make_grid(kind, M, Rd, a0, ge, axis, res)
    Mc, Min = deposit(g, dkind, M, Rd)
    if kind in ("expo", "kuzmin", "expo+bulge"):
        # amendment A3: the disc's mass inside r_min enters as the sheet's flux, proportional to |cos theta|
        Rmin = g.rf[0]
        Md_in = (M * 0.8 if kind == "expo+bulge" else M) * (
            (1 - Rd / math.sqrt(Rmin ** 2 + Rd ** 2)) if kind == "kuzmin" else (1 - (1 + Rmin / Rd) * math.exp(-Rmin / Rd)))
        c1, c2 = np.cos(g.tf[:-1]), np.cos(g.tf[1:])
        I = np.abs(np.abs(c1) * c1 - np.abs(c2) * c2) / 2
        Mc = Mc.copy(); Mc[0] += Md_in * (I[:, None] * np.diff(g.pf)[None, :] / (2 * np.pi))
        Min = Min - Md_in
    Phib = far_field(g, M, a0, ge, axis)
    t0 = time.time()
    Phi, res_, nit = solve(g, Mc, Min, Phib, a0)
    dp, grads = phantom(g, Phi, Phib, Mc, a0)
    return dict(g=g, Phi=Phi, Phib=Phib, Mc=Mc, Min=Min, dp=dp, grads=grads, M=M, Rd=Rd, a0=a0, ge=ge, axis=axis,
                residual=res_, iterations=nit, seconds=time.time() - t0, foot=foot, kind=kind, logm=logm)


def nu(y): return 0.5 + np.sqrt(0.25 + 1 / y)


def summarize_map(bg, crop=None):
    """sign map statistics of D.P (off the innermost shell; plane cells reported separately for thin discs)."""
    g = bg["g"]; dp = bg["dp"]; V = g.V * g.mult
    ok = np.isfinite(dp)
    rmax_map = crop if crop else g.rf[-1]
    inside = ok & (g.rc[:, None, None] * np.ones(g.shape) <= rmax_map)
    thin = bg["kind"] in ("expo", "kuzmin", "expo+bulge")
    plane = np.zeros(g.shape, bool)
    if thin:
        if g.tmode == "half": plane[:, -1, :] = True
        else: plane[:, g.nt // 2 - 1, :] = True; plane[:, g.nt // 2, :] = True
    scale = np.nanmax(np.abs(dp[inside & ~plane])) if np.any(inside & ~plane) else 1.0
    neg = inside & ~plane & (dp < -1e-6 * scale)
    Q = dp * V
    Qpos = float(np.nansum(Q[inside & (dp > 0)])); Qneg = float(np.nansum(Q[inside & (dp < 0)]))
    Qneg_off = float(np.nansum(Q[neg]))
    out = dict(n_cells=int(inside.sum()), n_negative_offplane=int(neg.sum()),
               volume_negative_kpc3=float(np.sum(V[neg])), volume_inside_kpc3=float(np.sum(V[inside])),
               Q_pos=Qpos, Q_neg=Qneg, Q_neg_offplane=Qneg_off,
               frac_neg_over_pos=float(-Qneg_off / Qpos) if Qpos > 0 else None,
               frac_neg_over_net=float(-Qneg_off / (Qpos + Qneg)) if (Qpos + Qneg) != 0 else None,
               plane_min=float(np.nanmin(dp[plane & inside])) if np.any(plane & inside) else None,
               plane_negative_cells=int(np.sum(plane & inside & (dp < 0))),
               min_dp_offplane=float(np.nanmin(dp[inside & ~plane])))
    if neg.any():
        R = g.R[neg]; Z = g.Z[neg]; r = np.sqrt(R ** 2 + Z ** 2)
        out["where"] = dict(r_kpc=[float(r.min()), float(r.max())], r_over_Rd=[float(r.min() / bg["Rd"]), float(r.max() / bg["Rd"])],
                            theta_deg=[float(np.degrees(np.arctan2(R, Z)).min()), float(np.degrees(np.arctan2(R, Z)).max())],
                            z_sign=sorted(set(np.sign(Z).astype(int).tolist())),
                            on_axis=bool(np.any(np.degrees(np.arctan2(R, np.abs(Z))) < 10)))
    return out


def kuzmin_closed(bg):
    """KA2: |grad Phi| against the law applied to the point mass at z = -a (above the plane), cells >= 3 off the plane."""
    g = bg["g"]; a = bg["Rd"]; M = bg["M"]; a0 = bg["a0"]
    gr, gt, gp = bg["grads"]
    gmag = np.sqrt(gr ** 2 + gt ** 2 + gp ** 2)
    R = g.R; Z = g.Z
    d = np.sqrt(R ** 2 + (np.abs(Z) + a) ** 2)
    gN = G * M / d ** 2
    gl = gN * nu(gN / a0)
    sel = np.zeros(g.shape, bool)
    sel[:, : g.nt - 3, :] = True if g.tmode == "half" else False
    sel &= (np.sqrt(R ** 2 + Z ** 2) <= 100 * a) & np.isfinite(bg["dp"])     # A2: inner layer excluded
    rel = np.abs(gmag[sel] / gl[sel] - 1)
    return float(rel.max()), int(sel.sum())


def phantom_mass_inside(bg, r):
    g = bg["g"]; sel = (g.rc[:, None, None] * np.ones(g.shape) <= r) & np.isfinite(bg["dp"])
    # add the innermost shell's phantom from the enclosed-mass flux through its outer face: use the field there
    return float(np.nansum((bg["dp"] * g.V * g.mult)[sel]))


def save_cache(bg, path):
    g = bg["g"]
    np.savez_compressed(path, Phi=bg["Phi"], Phib=bg["Phib"], Mc=bg["Mc"], dp=bg["dp"], gr=bg["grads"][0], gt=bg["grads"][1],
                        gp=bg["grads"][2], xf=g.xf, tf=g.tf, pf=g.pf, tmode=g.tmode, M=bg["M"], Rd=bg["Rd"], a0=bg["a0"],
                        ge=bg["ge"], axis=bg["axis"], Min=bg["Min"])


def load_cache(path):
    z = np.load(path, allow_pickle=True)
    nr = len(z["xf"]) - 1; nt = len(z["tf"]) - 1; np_ = len(z["pf"]) - 1 if len(z["pf"]) > 2 else 1
    g = Grid.__new__(Grid)
    Grid.__init__(g, math.exp(z["xf"][0]), math.exp(z["xf"][-1]), nr, nt, np_, str(z["tmode"]))
    return dict(g=g, Phi=z["Phi"], Phib=z["Phib"], Mc=z["Mc"], dp=z["dp"], grads=(z["gr"], z["gt"], z["gp"]),
                M=float(z["M"]), Rd=float(z["Rd"]), a0=float(z["a0"]), ge=float(z["ge"]), axis=str(z["axis"]), Min=float(z["Min"]))


# ------------------------------------------------------------------ the frozen list of backgrounds
def frozen_list():
    L = []
    for foot in ("canonical", "alt"):
        for lm in LOGM:
            for kind in ("expo", "kuzmin"):
                L.append(dict(group="primary", foot=foot, kind=kind, logm=lm))
            L.append(dict(group="bracket_thick", foot=foot, kind="thick", logm=lm))
            L.append(dict(group="bracket_bulge", foot=foot, kind="expo+bulge", logm=lm))
            for kind in ("expo", "kuzmin"):
                for ge in (0.01, 0.1):
                    L.append(dict(group="bracket_EF_axis", foot=foot, kind=kind, logm=lm, ge=ge, axis="z"))
                    if lm in ("9.4", "10.9"):
                        L.append(dict(group="bracket_EF_plane", foot=foot, kind=kind, logm=lm, ge=ge, axis="x"))
        for kind in ("expo", "kuzmin"):
            for fac in (0.5, 2.0):
                L.append(dict(group="bracket_Rd", foot=foot, kind=kind, logm="10.45", Rd_fac=fac))
    return L


def tag_of(d):
    return "_".join(str(d.get(k_, "")) for k_ in ("group", "foot", "kind", "logm", "ge", "axis", "Rd_fac")).replace(".", "p")


if __name__ == "__main__":
    OUTL = []
    def P_(s=""):
        print(s, flush=True); OUTL.append(str(s))
    t0 = time.time()
    CACHE = os.environ.get("SCS2_CACHE", os.path.join(HERE, "_cache"))
    os.makedirs(CACHE, exist_ok=True)
    RES = {"lane": "SCS2", "script": "scs2_aqual", "criteria": "158c4cf770", "amendments": ["847f24db0b", "cb6ac0fe9a", "ac13205c89"],
           "known_answers": {}, "maps": {}}
    # ---------------- KA1: point mass through the axisymmetric machinery; KA5 phantom mass for the point mass
    ka1 = {}
    for foot in ("canonical", "alt"):
        bg = background(foot, "point", "10.45")
        g = bg["g"]; dp = bg["dp"]; ok = np.isfinite(dp)
        rM = math.sqrt(G * bg["M"] / bg["a0"])
        pm_i, rr = gauss_phantom(bg, 10 * rM)
        y = G * bg["M"] / (rr ** 2 * bg["a0"])
        exact = bg["M"] * (nu(y) - 1)
        ka1[foot] = dict(min_dp=float(np.nanmin(dp[ok])), positive_everywhere=bool(np.all(dp[ok] > 0)), residual=bg["residual"],
                         iterations=bg["iterations"], phantom_inside=pm_i, exact=float(exact), rel=float(abs(pm_i / exact - 1)))
        save_cache(bg, os.path.join(CACHE, f"KA1_point_{foot}.npz"))
        P_(f"KA1/KA5 point mass ({foot}): D.P > 0 in every cell: {ka1[foot]['positive_everywhere']}; residual {bg['residual']:.1e} "
           f"({bg['iterations']} it); phantom inside {rr:.1f} kpc {pm_i:.6e} vs M (nu - 1) {exact:.6e}, rel {ka1[foot]['rel']:.2e}")
    RES["known_answers"]["KA1_point_mass_map"] = ka1
    RES["known_answers"]["KA5_point_mass"] = dict(pass_=bool(all(v["rel"] <= 1e-3 for v in ka1.values())),
                                                  rel={k_: v["rel"] for k_, v in ka1.items()})
    # ---------------- all frozen backgrounds (fine grid; primary also coarse for KA4)
    for d in frozen_list():
        tg = tag_of(d)
        kw = dict(ge=d.get("ge", 0.0), axis=d.get("axis", "z"), Rd_fac=d.get("Rd_fac", 1.0))
        bg = background(d["foot"], d["kind"], d["logm"], res=1, **kw)
        crop = None
        if kw["ge"] > 0:
            re = math.sqrt(G * bg["M"] * bg["a0"]) / (kw["ge"] * bg["a0"]); crop = max(30 * bg["Rd"], 3 * re)
        smap = summarize_map(bg)
        entry = dict(spec=d, Rd_kpc=bg["Rd"], residual=bg["residual"], iterations=bg["iterations"], seconds=round(bg["seconds"], 1),
                     map=smap, crop_route2_kpc=crop if crop else 30 * bg["Rd"])
        if d["kind"] == "kuzmin" and kw["ge"] == 0:
            ka2, nsel = kuzmin_closed(bg); entry["KA2_rel"] = ka2; entry["KA2_cells"] = nsel
        if d["group"] in ("primary",):
            # KA5 for discs: phantom inside 30 R_d against M (nu(y) - 1) at the shell's outer face
            pm, rr = gauss_phantom(bg, 30 * bg["Rd"])
            y = G * bg["M"] / (rr ** 2 * bg["a0"])
            entry["KA5"] = dict(phantom_inside=pm, exact=float(bg["M"] * (nu(y) - 1)), rel=float(abs(pm / (bg["M"] * (nu(y) - 1)) - 1)),
                                r_kpc=float(rr))
            # KA4: coarse grid
            bgc = background(d["foot"], d["kind"], d["logm"], res=0, **kw)
            smc = summarize_map(bgc)
            entry["KA4"] = dict(residual_coarse=bgc["residual"], residual_fine=bg["residual"],
                                frac_coarse=smc["frac_neg_over_pos"], frac_fine=smap["frac_neg_over_pos"],
                                min_dp_coarse=smc["min_dp_offplane"], min_dp_fine=smap["min_dp_offplane"])
            save_cache(bgc, os.path.join(CACHE, tg + "_coarse.npz"))
        save_cache(bg, os.path.join(CACHE, tg + ".npz"))
        if d["group"] != "primary" and not (kw["ge"] > 0 and kw["axis"] == "x"):
            # coarse twin for route 2's second resolution (brackets); its map is not graded
            bgc = background(d["foot"], d["kind"], d["logm"], res=0, **kw)
            save_cache(bgc, os.path.join(CACHE, tg + "_coarse.npz"))
        RES["maps"][tg] = entry
        P_(f"[{tg}] res {bg['residual']:.1e} ({bg['iterations']} it, {bg['seconds']:.0f}s); negative off-plane cells "
           f"{smap['n_negative_offplane']}; Q_neg/Q_pos {smap['frac_neg_over_pos']}; min D.P {smap['min_dp_offplane']:.3e}; "
           f"plane min {smap['plane_min']}" + (f"; KA2 {entry['KA2_rel']:.2e}" if 'KA2_rel' in entry else "")
           + (f"; KA5 {entry['KA5']['rel']:.2e}" if 'KA5' in entry else "") + (f"; where {smap['where']}" if 'where' in smap else ""))
    # ---------------- known-answer verdicts
    prim = [e for e in RES["maps"].values() if e["spec"]["group"] == "primary"]
    allres = [e["residual"] for e in RES["maps"].values()] + [e["KA4"]["residual_coarse"] for e in prim]
    ka2 = [e["KA2_rel"] for e in RES["maps"].values() if "KA2_rel" in e]
    def agree(a_, b_):
        if (a_ in (None, 0) or a_ == 0.0) and (b_ in (None, 0) or b_ == 0.0): return True
        if a_ is None or b_ is None: return False
        return abs(a_ - b_) <= 0.2 * max(abs(a_), abs(b_))
    ka4_ok = max(allres) <= 1e-8 and all(agree(e["KA4"]["frac_coarse"], e["KA4"]["frac_fine"]) and
                                          agree(e["KA4"]["min_dp_coarse"], e["KA4"]["min_dp_fine"]) for e in prim)
    RES["known_answers"]["KA2_kuzmin"] = dict(max_rel=max(ka2), pass_=bool(max(ka2) <= 1e-2))
    RES["known_answers"]["KA4_residual_convergence"] = dict(max_residual=max(allres), pass_=bool(ka4_ok))
    RES["known_answers"]["KA5_discs"] = dict(max_rel=max(e["KA5"]["rel"] for e in prim),
                                             pass_=bool(max(e["KA5"]["rel"] for e in prim) <= 0.02))
    for k_, v in RES["known_answers"].items():
        if "pass_" in v: P_(f"{k_}: {'PASS' if v['pass_'] else 'FAIL'} " + json.dumps({kk: vv for kk, vv in v.items() if kk != 'pass_'})[:300])
    RES["seconds"] = round(time.time() - t0, 1)
    RES["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
    RES["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
    with open(os.path.join(HERE, "scs2_maps.json"), "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    P_(f"runtime {RES['seconds']} s, peak RSS {RES['peak_rss_GB']} GB")
    P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
    with open(os.path.join(HERE, "scs2_maps.out"), "w") as fh:
        fh.write("\n".join(OUTL) + "\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
