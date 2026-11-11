"""EFN1 core (criteria 98364c8d20): backgrounds on SCS3's AX grids, the finite-volume operators, the nonlinear right-hand
side of the clock / gravity system, and the leading linear mode.

Equations (section 1 of the criteria; perturbation variables, exact):
    d_t pi = phi - s + |grad pi|^2/2,   lap phi = K n,   div[P(grad Phi0 + grad s)] - div[P(grad Phi0)] = n,
    d_t n  = div[(N0 + n) grad pi]        on the dynamic cells r >= r_in = 0.4 r_e (pi = n = 0 inside).
Discrete P flux: SCS2's phantom() face flux K P_f.n_f = (1/(1+u_f)) dS/dn, u_f from the normal difference and the averaged
tangential cell gradients (scs2_aqual.face_mu, re-expressed here as sparse operators and checked against it).

scs2_aqual.py is copied unedited from fable52_push/SCS3_external_field_stability/ (itself SCS2's file).  make_grid_res is
SCS3's scs3_maps.make_grid_res (AX branch), re-typed here.  Units kpc, km/s, Msun; time unit kpc/(km/s).
"""
import os, sys, math, json, tempfile
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scs2_aqual as S

G = S.G
K = 4 * np.pi * G
GYR_S = 3.15576e16                      # s per Gyr (SCS3's conversion)
TU_S = 3.0857e16                        # s per kpc/(km/s)
TU_GYR = TU_S / GYR_S
AX_BASE = [(48, 24), (72, 36), (108, 54), (162, 81), (243, 121), (364, 182), (546, 273)]   # SCS3 scs3_maps.py
CACHE = os.path.join(tempfile.gettempdir(), "efn1_cache")
SCS3_LABELS = os.path.join(HERE, "..", "..", "fable52_push", "SCS3_external_field_stability", "scs3_labels.json")
RE_LIST = [0.5, 0.75, 1.0, 1.5, 2.0, 4.0]
R_IN_FAC = 0.4

GRADED = {"canonical": [("expo", "9.4"), ("expo", "10.45"), ("expo", "10.7"), ("kuzmin", "9.4"), ("kuzmin", "10.7"), ("kuzmin", "10.9")],
          "alt": [("expo", "9.4"), ("expo", "10.45"), ("expo", "10.7"), ("expo", "10.9"), ("kuzmin", "9.4"), ("kuzmin", "10.9")]}
MUT_SET = [("canonical", "expo", "9.4"), ("canonical", "kuzmin", "10.9"), ("alt", "expo", "9.4"), ("alt", "kuzmin", "10.9")]


def scs3_rate(foot, kind, logm, ge):
    """SCS3 A4 converged route-L Gamma (per Gyr and per time unit) and its label, read from scs3_labels.json."""
    d = json.load(open(SCS3_LABELS))["A4"][f"AX_{foot}"]["backgrounds"]
    key = f"AX_{foot}_{kind}_{logm.replace('.', 'p')}_{str(ge).replace('.', 'p')}_z"
    v = d[key]
    q = v["GammaL2"]["Qinf"]
    gam_s = math.sqrt(q)
    return dict(key=key, label=v["label"], efold_gyr=1 / (gam_s * GYR_S), gamma_tu=gam_s * TU_S, where=v["where"][-1],
                efold_by_res=v["efold_gyr"])


def make_grid_res(M, Rd, a0, ge, res):
    re = (math.sqrt(G * M * a0) / (ge * a0)) if ge > 0 else 0.0
    r_max = max(1e3 * Rd, 10 * re)
    r_min = 1e-4 * Rd
    scale = math.log(r_max / r_min) / math.log(r_max / (0.02 * Rd))
    nr, nt = AX_BASE[res]
    return S.Grid(r_min, r_max, int(round(nr * scale)), 2 * nt, 1, "full")


def background(foot, kind, logm, ge, res, isolated=False):
    """SCS2's background() on SCS3's full-theta AX grid R_res.  isolated=True: the same grid (that of the ge twin) with the
    isolated (constant) far field, for KA-c.  Cached in the system temp directory."""
    os.makedirs(CACHE, exist_ok=True)
    tag = f"{foot}_{kind}_{logm}_{ge}_{res}_{'iso' if isolated else 'ef'}"
    path = os.path.join(CACHE, tag + ".npz")
    M = 10 ** float(logm); a0 = S.a0k(foot); Rd = S.R_d_shen(M)
    g = make_grid_res(M, Rd, a0, ge, res)
    re = math.sqrt(G * M * a0) / (ge * a0)
    if os.path.exists(path):
        z = np.load(path)
        return dict(g=g, Phi=z["Phi"], Phib=z["Phib"], Mc=z["Mc"], Min=float(z["Min"]), M=M, Rd=Rd, a0=a0, ge=ge, re=re,
                    residual=float(z["residual"]), foot=foot, kind=kind, logm=logm, res=res, isolated=isolated)
    Mc, Min = S.deposit(g, kind, M, Rd)
    Rmin = g.rf[0]
    Md_in = M * ((1 - Rd / math.sqrt(Rmin ** 2 + Rd ** 2)) if kind == "kuzmin" else (1 - (1 + Rmin / Rd) * math.exp(-Rmin / Rd)))
    c1, c2 = np.cos(g.tf[:-1]), np.cos(g.tf[1:])
    I = np.abs(np.abs(c1) * c1 - np.abs(c2) * c2) / 2
    Mc = Mc.copy(); Mc[0] += Md_in * (I[:, None] * np.diff(g.pf)[None, :] / (2 * np.pi))
    Min = Min - Md_in
    Phib = S.far_field(g, M, a0, 0.0 if isolated else ge, "z")
    Phi, res_, nit = S.solve(g, Mc, Min, Phib, a0)
    np.savez(path, Phi=Phi, Phib=Phib, Mc=Mc, Min=Min, residual=res_)
    return dict(g=g, Phi=Phi, Phib=Phib, Mc=Mc, Min=Min, M=M, Rd=Rd, a0=a0, ge=ge, re=re, residual=res_, foot=foot,
                kind=kind, logm=logm, res=res, isolated=isolated)


class Ops:
    """sparse finite-volume operators on one background."""

    def __init__(self, bg, r_in_fac=R_IN_FAC, sheet_static=True):
        g = bg["g"]; self.g = g; self.bg = bg
        n = g.n; nr, nt = g.nr, g.nt
        self.n = n; self.a0 = bg["a0"]
        F = S.faces(g)
        k1r, k2r, Ar, dr = F["r"]; k1t, k2t, At, dt = F["t"]
        self.k1 = np.concatenate([k1r, k1t])
        self.k2 = np.concatenate([k2r, k2t])
        self.A = np.concatenate([Ar, At]); self.d = np.concatenate([dr, dt])
        self.isr = np.concatenate([np.ones(len(k1r), bool), np.zeros(len(k1t), bool)])
        nf = len(self.k1); self.nf = nf
        kO, AO, dO = F["out"]; self.kO, self.AO, self.dO = kO, AO, dO
        f = np.arange(nf)
        self.Dn = sps.csr_matrix((np.concatenate([-1 / self.d, 1 / self.d]), (np.concatenate([f, f]), np.concatenate([self.k1, self.k2]))), shape=(nf, n))
        nO = len(kO); fo = np.arange(nO)
        self.DnO = sps.csr_matrix((-1 / dO, (fo, kO)), shape=(nO, n))
        self.bO = bg["Phib"].ravel() / dO                     # outer normal difference's Dirichlet part (for S = Phi0 + s)
        # cell gradients (scs2_aqual.cell_gradient, as sparse maps; Dirichlet ghost at r_max = 2 Phib - P)
        idx = np.arange(n).reshape(nr, nt)
        rc = g.rc; rce = np.concatenate([[rc[0] * math.exp(-g.dx)], rc, [rc[-1] * math.exp(g.dx)]])
        rows, cols, vals = [], [], []
        br = np.zeros((nr, nt))
        for i in range(nr):
            den = rce[i + 2] - rce[i]
            up = idx[i + 1] if i + 1 < nr else None
            dn = idx[i - 1] if i > 0 else idx[0]
            if up is not None:
                rows.append(idx[i]); cols.append(up); vals.append(np.full(nt, 1 / den))
            else:
                rows.append(idx[i]); cols.append(idx[i]); vals.append(np.full(nt, -1 / den))
                br[i] = 2 * bg["Phib"][:, 0] / den
            rows.append(idx[i]); cols.append(dn); vals.append(np.full(nt, -1 / den))
        self.Gr = sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))
        self.br = br.ravel()
        tce = np.concatenate([[-g.tc[0]], g.tc, [2 * np.pi - g.tc[-1]]])
        rows, cols, vals = [], [], []
        for j in range(nt):
            den = (tce[j + 2] - tce[j]) * rc
            up = idx[:, j + 1] if j + 1 < nt else idx[:, nt - 1]
            dn = idx[:, j - 1] if j > 0 else idx[:, 0]
            rows += [idx[:, j], idx[:, j]]; cols += [up, dn]; vals += [1 / den, -1 / den]
        self.Gt = sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))
        # face tangential component: r faces <- mean gt; t faces <- mean gr; outer <- gt of the cell
        Avg = sps.csr_matrix((np.full(2 * nf, 0.5), (np.concatenate([f, f]), np.concatenate([self.k1, self.k2]))), shape=(nf, n))
        selr = sps.diags(self.isr.astype(float)); selt = sps.diags((~self.isr).astype(float))
        self.Tm = selr @ Avg @ self.Gt + selt @ Avg @ self.Gr
        self.bT = selt @ (Avg @ self.br)
        self.TmO = sps.csr_matrix(self.Gt[kO])
        self.Div = sps.csr_matrix((np.concatenate([self.A, -self.A]), (np.concatenate([self.k1, self.k2]), np.concatenate([f, f]))), shape=(n, nf))
        self.DivO = sps.csr_matrix((AO, (kO, fo)), shape=(n, nO))
        self.V = g.V.ravel()
        # background face quantities
        P0 = bg["Phi"].ravel(); self.P0 = P0
        self.gn0 = self.Dn @ P0; self.T0 = self.Tm @ P0 + self.bT
        self.gnO0 = self.DnO @ P0 + self.bO; self.TO0 = self.TmO @ P0
        self.flux0 = self.flux_full(P0)
        self.N0 = self.flux0 / (K * self.V)
        # Poisson operator (coefficient 1, Dirichlet 0 at r_max): Lp phi = K V n
        self.Lp = (self.Div @ self.Dn + self.DivO @ self.DnO).tocsc()
        self.Lp_lu = spla.splu(self.Lp)
        self.J0 = self.jacobian(self.gn0, self.T0, self.gnO0, self.TO0).tocsc()
        self.J0_lu = spla.splu(self.J0)
        # dynamic region
        re = bg["re"]; self.re = re
        R2 = (g.rc[:, None] * np.ones((1, nt))).ravel(); self.rcell = R2
        self.thcell = (np.ones((nr, 1)) * g.tc[None, :]).ravel()
        self.Dm = R2 >= r_in_fac * re
        if sheet_static:                       # amendment A1 (c3e466efbf): the razor-thin sheet's two plane rows held static
            jm = nt // 2
            pl = np.zeros((nr, nt), bool); pl[:, jm - 1] = True; pl[:, jm] = True
            self.Dm &= ~pl.ravel()
        self.sheet_static = sheet_static
        self.Didx = np.where(self.Dm)[0]
        self.open = self.Dm[self.k1] & self.Dm[self.k2]
        gr0 = self.Gr @ P0 + self.br; gt0 = self.Gt @ P0
        self.gmag0 = np.sqrt(gr0 ** 2 + gt0 ** 2); self.gr0 = gr0
        u = self.gmag0 / self.a0
        self.loc2 = -4 * np.pi * G * self.N0 * u * (2 + u)              # local route-L rate^2 (tu^-2), >0 where unstable
        dmask = self.Dm.copy()
        self.istar = int(np.argmax(np.where(dmask, self.loc2, -np.inf)))
        self.omega_max = math.sqrt(np.max(np.abs(self.loc2[dmask])))
        self.N0min = float(np.min(self.N0[dmask]))
        rf = g.rf; tf = g.tf
        hr = (rf[1:] - rf[:-1])[:, None] * np.ones((1, nt)); ht = g.rc[:, None] * (tf[1:] - tf[:-1])[None, :]
        self.h = np.minimum(hr, ht).ravel()
        self.N0f = 0.5 * (self.N0[self.k1] + self.N0[self.k2])
        # face-count arrays for |grad pi|^2 from open faces
        of = self.open
        cnt_r = np.zeros(n); cnt_t = np.zeros(n)
        np.add.at(cnt_r, self.k1[of & self.isr], 1); np.add.at(cnt_r, self.k2[of & self.isr], 1)
        np.add.at(cnt_t, self.k1[of & ~self.isr], 1); np.add.at(cnt_t, self.k2[of & ~self.isr], 1)
        self.cnt_r = np.maximum(cnt_r, 1); self.cnt_t = np.maximum(cnt_t, 1)
        # shells for dg
        self.shell = {x: int(np.argmin(np.abs(g.rc - x * re))) for x in RE_LIST}

    # ------------------------------------------------------------------ P flux
    def _cg(self, gn, T):
        Am = np.sqrt(gn ** 2 + T ** 2); u = Am / self.a0
        return 1 / (1 + u), Am, u

    def flux_full(self, Psi):
        gn = self.Dn @ Psi; T = self.Tm @ Psi + self.bT
        gnO = self.DnO @ Psi + self.bO; TO = self.TmO @ Psi
        c, _, _ = self._cg(gn, T); cO, _, _ = self._cg(gnO, TO)
        return self.Div @ (c * gn) + self.DivO @ (cO * gnO)

    def dflux(self, s):
        """flux(Phi0 + s) - flux(Phi0) without cancellation."""
        out = np.zeros(self.n)
        for (Dn, Tm, gn0, T0, Div) in ((self.Dn, self.Tm, self.gn0, self.T0, self.Div), (self.DnO, self.TmO, self.gnO0, self.TO0, self.DivO)):
            dg = Dn @ s; dT = Tm @ s
            gn1 = gn0 + dg; T1 = T0 + dT
            A0 = np.sqrt(gn0 ** 2 + T0 ** 2); A1 = np.sqrt(gn1 ** 2 + T1 ** 2)
            dA2 = dg * (2 * gn0 + dg) + dT * (2 * T0 + dT)
            du = dA2 / (self.a0 * np.maximum(A1 + A0, 1e-300))
            u0 = A0 / self.a0; u1 = A1 / self.a0
            c0 = 1 / (1 + u0)
            dc = -du / ((1 + u1) * (1 + u0))
            out += Div @ (c0 * dg + gn1 * dc)
        return out

    def jacobian(self, gn, T, gnO, TO):
        mats = []
        for (Dn, Tm, gn_, T_, Div) in ((self.Dn, self.Tm, gn, T, self.Div), (self.DnO, self.TmO, gnO, TO, self.DivO)):
            c, Am, u = self._cg(gn_, T_)
            Am = np.maximum(Am, 1e-300)
            alpha = c - gn_ ** 2 / (self.a0 * Am * (1 + u) ** 2)
            beta = -gn_ * T_ / (self.a0 * Am * (1 + u) ** 2)
            mats.append(Div @ (sps.diags(alpha) @ Dn + sps.diags(beta) @ Tm))
        return mats[0] + mats[1]

    def solve_s(self, b, s0=None, tol=1e-10, maxit=30, maxit2=60):
        """quasi-Newton for dflux(s) = b (b = K V n); returns s, iterations, ok."""
        s = np.zeros(self.n) if s0 is None else s0.copy()
        nb = max(np.linalg.norm(b), 1e-300)
        lu = self.J0_lu; it_tot = 0
        for stage in (0, 1):
            for it in range(maxit if stage == 0 else maxit2):
                r = b - self.dflux(s)
                if np.linalg.norm(r) <= tol * nb:
                    return s, it_tot, True
                s = s + lu.solve(r); it_tot += 1
                if not np.all(np.isfinite(s)):
                    return s, it_tot, False
            if stage == 0:
                Ps = self.P0 + s
                Jc = self.jacobian(self.Dn @ Ps, self.Tm @ Ps + self.bT, self.DnO @ Ps + self.bO, self.TmO @ Ps).tocsc()
                lu = spla.splu(Jc)
        r = b - self.dflux(s)
        return s, it_tot, bool(np.linalg.norm(r) <= tol * nb)

    # ------------------------------------------------------------------ clock
    def grad2_pi(self, pi):
        of = self.open
        dpi = (pi[self.k2] - pi[self.k1]) / self.d
        q = np.where(of, dpi ** 2, 0.0)
        gr2 = np.zeros(self.n); gt2 = np.zeros(self.n)
        m = of & self.isr
        np.add.at(gr2, self.k1[m], q[m]); np.add.at(gr2, self.k2[m], q[m])
        m = of & ~self.isr
        np.add.at(gt2, self.k1[m], q[m]); np.add.at(gt2, self.k2[m], q[m])
        return gr2 / self.cnt_r + gt2 / self.cnt_t

    def ndot_V(self, pi, n, sig, central=False):
        """sum over open faces of (N0_f + sig * n_upwind) (pi_k2 - pi_k1)/d A, into cells (V n_t)."""
        dpi = pi[self.k2] - pi[self.k1]
        Nf = self.N0f.copy()
        if sig != 0:
            nup = 0.5 * (n[self.k1] + n[self.k2]) if central else np.where(dpi < 0, n[self.k1], n[self.k2])   # A3: central for route W
            Nf = Nf + sig * nup
        Fl = np.where(self.open, Nf * dpi / self.d * self.A, 0.0)
        out = np.zeros(self.n)
        np.add.at(out, self.k1, Fl); np.add.at(out, self.k2, -Fl)
        return out

    def rhs(self, pi, n, sig=1, s_prev=None, phi_extra=None, tol=1e-10, sig_s=None, sig_g=None, sig_f=None, central=False):
        """returns (pi_t, n_t, info).  sig = 1 the equations; 0 linear (M3); -1 every nonlinear term's sign flipped (M2).
        sig_s, sig_g, sig_f override the sign of the s-map's nonlinear part, of |grad pi|^2/2 and of the upwind n flux."""
        ss = sig if sig_s is None else sig_s; sg = sig if sig_g is None else sig_g; sf = sig if sig_f is None else sig_f
        b = K * self.V * n
        phi = self.Lp_lu.solve(b)
        if phi_extra is not None:
            phi = phi + phi_extra
        s_lin = self.J0_lu.solve(b)
        info = dict(it=0, ok=True, s=None)
        if ss == 0:
            s_eff = s_lin
        else:
            s, it, ok = self.solve_s(b, s_prev, tol=tol)
            info.update(it=it, ok=ok, s=s)
            s_eff = s_lin + ss * (s - s_lin)
        pit = phi - s_eff
        if sg != 0:
            pit = pit + sg * 0.5 * self.grad2_pi(pi)
        pit = np.where(self.Dm, pit, 0.0)
        nt = np.where(self.Dm, self.ndot_V(pi, n, sf, central) / self.V, 0.0)
        info["phi"] = phi
        return pit, nt, info

    def seed_n(self, eps, sign=1.0, w_r=0.2, w_t=0.2):
        """n = -div(N0 xi), xi = eps r_e exp(...) rhat centred on the route-L maximum; faces open only."""
        r_s = self.rcell[self.istar]; t_s = self.thcell[self.istar]; re = self.re
        g = self.g
        m = self.open & self.isr
        rface = g.rf[1:-1][self.k1[m] // g.nt]                 # r face between shells i and i+1 sits at rf[i+1]
        th = self.thcell[self.k1[m]]
        xi = sign * eps * re * np.exp(-(rface - r_s) ** 2 / (2 * (w_r * re) ** 2) - (th - t_s) ** 2 / (2 * w_t ** 2))
        Fl = self.N0f[m] * xi * self.A[m]
        nV = np.zeros(self.n)
        np.add.at(nV, self.k1[m], -Fl); np.add.at(nV, self.k2[m], Fl)
        return nV / self.V

    def amplitude(self, n):
        a = np.abs(n[self.Didx]); i = int(np.argmax(a))
        k = self.Didx[i]
        return float(a[i] / abs(self.N0min)), int(k)

    def resP(self):
        """the background's Picard residual in SCS2's mu form, A_mu Phi0 - (b - cout Phib), per cell (for KA-d)."""
        g = self.g; bg = self.bg
        F = S.faces(g)
        gr, gt, gp = S.cell_gradient(g, bg["Phi"], bg["Phib"])
        mu = S.face_mu(g, F, bg["Phi"], bg["Phib"], bg["a0"], False, gr, gt, gp)
        A, cout, kout = S.operator(g, F, mu)
        b = (4 * np.pi * G * (bg["Mc"] + bg["Min"] * g.solid[0][None, :, :] / (4 * np.pi) * (np.arange(g.nr) == 0)[:, None, None])).ravel()
        rhs = b.copy(); np.add.at(rhs, kout, -cout * bg["Phib"].ravel())
        return A @ bg["Phi"].ravel() - rhs

    def dg(self, phi):
        g = self.g
        gr = (self.Gr @ phi).reshape(g.nr, g.nt)              # Dirichlet 0 at r_max: br not added for the perturbation
        out = {}
        for x, i in self.shell.items():
            rel = np.abs(gr[i]) / self.gmag0.reshape(g.nr, g.nt)[i]
            out[str(x)] = [float(rel.max()), float(rel.mean())]
        return out

    def vmax_dt(self, pi):
        v = np.sqrt(self.grad2_pi(pi))
        vv = v[self.Didx]
        return float(vv.max()), float(np.min(self.h[self.Didx] / np.maximum(vv, 1e-300)))

    # ------------------------------------------------------------------ linear mode (route W / KA-b / KA-c)
    def Cmat(self):
        """K V n_t = Cmat pi_D (linear part), Cmat: n x nD."""
        nD = len(self.Didx)
        cols = np.full(self.n, -1); cols[self.Didx] = np.arange(nD)
        m = self.open
        k1, k2 = self.k1[m], self.k2[m]
        w = K * self.N0f[m] / self.d[m] * self.A[m]
        rows = np.concatenate([k1, k1, k2, k2]); cc = np.concatenate([cols[k2], cols[k1], cols[k1], cols[k2]])
        vals = np.concatenate([w, -w, w, -w])
        return sps.csr_matrix((vals, (rows, cc)), shape=(self.n, nD))

    def block_lu(self, sigma):
        n = self.n; nD = len(self.Didx)
        C = self.Cmat()
        ED = sps.csr_matrix((np.ones(nD), (np.arange(nD), self.Didx)), shape=(nD, n))
        Z = None
        Blk = sps.bmat([[self.Lp, Z, -C], [Z, self.J0, -C], [ED, -ED, -sigma * sps.identity(nD)]], format="csc")
        return spla.splu(Blk), n, nD

    def leading_mode(self, sigma, k=4, left=False, tol=1e-10):
        lu, n, nD = self.block_lu(sigma)
        def mv(x, trans="N"):
            z = np.zeros(2 * n + nD); z[2 * n:] = x
            return lu.solve(z, trans=trans)[2 * n:]
        op = spla.LinearOperator((nD, nD), matvec=lambda x: mv(x), dtype=float)
        vals, vecs = spla.eigs(op, k=k, which="LM", tol=tol, maxiter=5000)
        lam = sigma + 1 / vals
        i = int(np.argmax(lam.real))
        out = dict(lam=complex(lam[i]), all=[complex(v_) for v_ in lam], vec=np.real(vecs[:, i]))
        if left:
            opT = spla.LinearOperator((nD, nD), matvec=lambda x: mv(x, "T"), dtype=float)
            vT, wT = spla.eigs(opT, k=k, which="LM", tol=tol, maxiter=5000)
            lamT = sigma + 1 / vT
            jT = int(np.argmin(np.abs(lamT - lam[i])))
            out["lam_left"] = complex(lamT[jT]); out["vec_left"] = np.real(wT[:, jT])
        del lu
        return out

    def apply_M(self, n_full):
        b = K * self.V * n_full
        return (self.Lp_lu.solve(b) - self.J0_lu.solve(b))

    def apply_MT(self, f_full):
        """transpose of M (cell space): (Lp^-T - J0^-T) f, times K V."""
        return K * self.V * (self.Lp_lu.solve(f_full, trans="T") - self.J0_lu.solve(f_full, trans="T"))
