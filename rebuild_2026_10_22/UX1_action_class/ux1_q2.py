"""UX1: axisymmetric dual solver. Units a0 = 1, r_M = sqrt(GM/a0) = 1.
Equation: div H = div F_N, curl[k(|H|) H/|H|] = 0, where grad psi = k(|H|) H/|H|.
H is carried by a flux function, so div H = source holds exactly:
   H_r = 1/r^2 + y_e cos(th) + u_th / (r^2 sin th),  H_th = -y_e sin(th) - u_xi / (r^2 sin th),  xi = ln r,
   with u the deviation from the exact point mass + uniform y_e flux, u = 0 at r_out and on the axis, natural condition at r_in
   (psi constant on the inner sphere).
The curl condition is the stationarity of E[v] = Int Wstar(|H|) dV, Wstar' = k, convex. No cap appears in the dual.
Forms:
  'aqual'  : psi = total potential,     mu(x) x = H, k = (H + sqrt(H^2+4H))/2   (record's AQUAL; known answer: E2)
  'bimond' : psi = anomalous potential, x^2/(1-x) = H, k = 2H/(H + sqrt(H^2+4H)) (K1's static equation, ux1_gates.py)
  'qumond' : k = (nu-1) H as a linear-source check is not needed: v = 0 in QUMOND, so it is the first iterate for 'aqual'.
Q2 follows E2's sign: q = -3 c2/r^2, c2 the P2 coefficient of psi.
"""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla


def k_(kind, H):
    r = np.sqrt(H ** 2 + 4 * H)
    return (H + r) / 2 if kind == "aqual" else 2 * H / (H + r)


def dk_(kind, H):
    r = np.sqrt(H ** 2 + 4 * H)
    dr = (H + 2) / r
    if kind == "aqual":
        return (1 + dr) / 2
    return 2 * (H + r - H * (1 + dr)) / (H + r) ** 2


def Wstar(kind, H):
    r = np.sqrt(H ** 2 + 4 * H)
    # int (H+r)/2 dH and int (r-H)/2 dH; int r dH = (H+2) r/2 - 2 ln(H + 2 + r)
    I = (H + 2) * r / 2 - 2 * np.log((H + 2 + r) / 2)
    return (H ** 2 / 2 + I) / 2 if kind == "aqual" else (I - H ** 2 / 2) / 2


class Solver:
    def __init__(self, kind, y_e, r_in=1e-5, r_out=1e4, per_dec=40, Nt=64):
        self.kind, self.y_e = kind, float(y_e)
        Nr = int(round(per_dec * np.log10(r_out / r_in))) + 1
        xi = np.linspace(np.log(r_in), np.log(r_out), Nr)
        th = np.linspace(0, np.pi, Nt)
        self.xi, self.th, self.r, self.Nr, self.Nt = xi, th, np.exp(xi), Nr, Nt
        idx = np.arange(Nr * Nt).reshape(Nr, Nt)
        a, b, c, d = idx[:-1, :-1].ravel(), idx[1:, :-1].ravel(), idx[1:, 1:].ravel(), idx[:-1, 1:].ravel()
        tris = np.vstack([np.c_[a, b, c], np.c_[a, c, d], np.c_[a, b, d], np.c_[b, c, d]])
        X, T = xi[tris // Nt], th[tris % Nt]
        x1, x2, x3 = X.T
        t1, t2, t3 = T.T
        det = (x2 - x1) * (t3 - t1) - (x3 - x1) * (t2 - t1)
        gx = np.c_[t2 - t3, t3 - t1, t1 - t2] / det[:, None]
        gt = np.c_[x3 - x2, x1 - x3, x2 - x1] / det[:, None]
        rc = np.exp(0.5 * (X.max(1) + X.min(1)))
        tc = T.mean(1)
        m = tris.shape[0]
        rows = np.repeat(np.arange(m), 3)
        cols = tris.ravel()
        s, co = np.sin(tc), np.cos(tc)
        self.Br = sp.csr_matrix(((gt / (rc[:, None] ** 2 * s[:, None])).ravel(), (rows, cols)), shape=(m, Nr * Nt))
        self.Bt = sp.csr_matrix(((-gx / (rc[:, None] ** 2 * s[:, None])).ravel(), (rows, cols)), shape=(m, Nr * Nt))
        self.H0r = 1 / rc ** 2 + self.y_e * co      # exact point mass + exact external flux; v carries the rest
        self.H0t = -self.y_e * s
        self.vol = 2 * np.pi * rc ** 3 * s * 0.5 * np.abs(det) * 0.5
        self.rc, self.tc, self.s, self.co = rc, tc, s, co
        self.area = 0.5 * np.abs(det) * 0.5
        self.band = np.round((X.min(1) - xi[0]) / (xi[1] - xi[0])).astype(int)
        self.fixed = np.unique(np.concatenate([idx[-1, :], idx[:, 0], idx[:, -1]]))
        self.free = np.setdiff1d(np.arange(Nr * Nt), self.fixed)
        self.u = np.zeros(Nr * Nt)
        self.BrF, self.BtF = self.Br[:, self.free].tocsc(), self.Bt[:, self.free].tocsc()

    def field(self, u):
        Hr, Ht = self.H0r + self.Br @ u, self.H0t + self.Bt @ u
        return Hr, Ht, np.maximum(np.hypot(Hr, Ht), 1e-300)

    def energy(self, u):
        return float(np.sum(self.vol * Wstar(self.kind, self.field(u)[2])))

    def solve(self, maxit=400, tol=1e-10):
        for it in range(maxit):
            Hr, Ht, H = self.field(self.u)
            k, dk = k_(self.kind, H), dk_(self.kind, H)
            nr, nt = Hr / H, Ht / H
            gr = self.BrF.T @ (self.vol * k * nr) + self.BtF.T @ (self.vol * k * nt)
            s = k / H
            Arr, Art, Att = s + (dk - s) * nr * nr, (dk - s) * nr * nt, s + (dk - s) * nt * nt
            V = sp.diags(self.vol)
            A = (self.BrF.T @ V @ sp.diags(Arr) @ self.BrF + self.BtF.T @ V @ sp.diags(Att) @ self.BtF
                 + self.BrF.T @ V @ sp.diags(Art) @ self.BtF + self.BtF.T @ V @ sp.diags(Art) @ self.BrF)
            D = sp.diags(1 / np.sqrt(A.diagonal()))
            lu = spla.splu((D @ A @ D).tocsc())
            d = -(D @ lu.solve(D @ gr))
            dec = -float(gr @ d)
            H0v = H
            W0 = Wstar(self.kind, H0v)
            t = 1.0
            dd = np.zeros_like(self.u)
            dd[self.free] = d
            while t > 1e-8:
                dE = float(np.sum(self.vol * (Wstar(self.kind, self.field(self.u + t * dd)[2]) - W0)))
                if dE <= -1e-4 * t * dec + 1e-13 * float(np.sum(self.vol * np.abs(W0))) * 1e-3:
                    break
                t *= 0.5
            self.u = self.u + t * dd
            self.iters = it + 1
            step = np.max(np.abs(dd)) * t / max(np.max(np.abs(self.u[self.free])), 1e-30)
            if t == 1.0 and step < tol:
                break
        self.step = float(step)
        self.converged = bool(step < 1e-8)
        return self

    def c2(self):
        """P2 coefficient of psi per band: c2 = -(5/2) Int (d psi/d theta) (1/2) cos sin^2 dtheta, d psi/d theta = r k H_th/H."""
        Hr, Ht, H = self.field(self.u)
        dpsi = self.rc * k_(self.kind, H) * Ht / H
        w = self.area * self.s ** 2 * self.co / 2
        num = np.bincount(self.band, -2.5 * dpsi * w)
        den = np.bincount(self.band, self.area) / np.pi        # band's triangles cover d xi x pi
        rb = np.exp(0.5 * (self.xi[1:] + self.xi[:-1]))
        return rb, num / den

    def q_of_r(self):
        rb, c = self.c2()
        return rb, -3 * c / rb ** 2

    def q0(self, rfit=(1e-3, 3e-2)):
        rb, c = self.c2()
        sel = (rb >= rfit[0]) & (rb <= rfit[1])
        A = np.stack([np.ones(sel.sum()), rb[sel], rb[sel] ** 2], axis=1)
        co, *_ = np.linalg.lstsq(A, c[sel] / rb[sel] ** 2, rcond=None)
        return -3 * co[0]
