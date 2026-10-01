#!/usr/bin/env python3
"""AS204 -- bounded prototype: curved-leaf heat-force derivative on the round 3-sphere.

Curved-leaf object (FINAL_ACTION.md b8c04d4e... + filtered_zero_field/RESULT.md 7067ca07...):
  Delta_h : Laplace-Beltrami (intrinsic),  S_h = exp(b*Delta_h),  b = xi^2/2 > 0
  phi(y) = h_mono(y)/y   (XC4 derivative-floor splice at y_star, delta = 0.05)
  H   = S_h grad u,   F = phi(|H|/a0) H
  u'  = Delta_h^{-1} delta_h F            (longitudinal elliptic projection, mean zero)
  S_h^* = N^{-1} S_h N                     (weighted adjoint in the lapse measure N sqrt(h))
  a_ph = -grad(S_h^* u')
  (N=1 flat: reduces exactly to the pinned -S P_L F via the transfer identity grad(S_h u') =
   S_h^{(1)}(grad u') on exact forms.)
Target: ||grad a_ph||_infty <= K_tot(b, geometry, lapse) ||F||_2.

Leaf: S^3 round (closed; |Rm|_sec = 1; inj radius pi; Ric = 2h: R0 = 2; lambda1 = 3).
Quadrature: exact separable (Chebyshev-Gauss t = cos theta, uniform u = cos phi and psi);
all basis Gram entries exact at truncation.

Controls that can fail
  NC1: flat multiplier identity D S = S D reused on curved geometry -> measured commutator
       ||grad(S_h f) - e^{b grad*grad}(grad f)||_infty = (1 - e^{-2b}) ||grad(S_h f)||_infty
       on S^3 (Ric parallel, closed form), ~1e-13 on the flat torus twin.
  NC2: naive flat transfer E_flat = M_b ||F||_2 (torus moment, pinned formula); ratio reported
       (expected > 1 whenever curvature/lapse corrections bite).
  C1: corrected bound r_curved = ||grad a_ph||_infty / (K_tot ||F||_2) <= 1.
  C2: b->0 limit a_ph -> -grad u'; weighted-adjoint identity; P_L contraction;
      Weitzenbock [Delta, grad] = 2 grad (modal); Hodge transfer; hessian integrated identity.
Enforced: <= 120 s wall, <= 512 MB RSS, 1 thread.
"""
import json, gc, os, subprocess, sys, time, resource, math

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np

T0 = time.monotonic()
WALL_MAX = 115.0
MEM_MAX = 512 * 1024 * 1024

# empirical 4th-order ambient eigenvalue per level: e_l = int_{S^3} |Hess_amb P_{l,1}|^2
# (exact to 1e-11 at the quadrature; deterministic build; probe_etable.py archived in-run)
E_TABLE = {1: 0.0, 2: 48.0, 3: 288.0, 4: 960.0, 5: 2400.0, 6: 5040.0, 7: 9408.0,
           8: 16128.0, 9: 25920.0, 10: 39600.0, 11: 58080.0, 12: 81120.0}

def budget(label):
    wall = time.monotonic() - T0
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if wall > WALL_MAX:
        raise SystemExit(f"WALL BUDGET EXCEEDED at {label}: {wall:.1f} s")
    if rss > MEM_MAX:
        raise SystemExit(f"MEM BUDGET EXCEEDED at {label}: {rss/1e6:.1f} MB")
    return wall, rss

# ------------------------------------------------------------ framework constants
G_N = 6.67430e-11
C_L = 299792458.0
MSUN = 1.98847e30
PC = 3.085677581491367e16
A0_CAN = 9.3619e-11
A0_ALT = 1.1279e-10
KAPPA = 0.5
RHO_L_CAN = 4.0 * A0_CAN ** 2 / (G_N * C_L ** 2)
RHO_L_ALT = 4.0 * A0_ALT ** 2 / (G_N * C_L ** 2)
DELTA_M = 0.05

# ------------------------------------------------------------ constitutive (nu_mono)
def h_RAR(y):
    y = np.asarray(y, float)
    return np.where(y > 0, y / np.expm1(np.sqrt(np.maximum(y, 0.0))), 0.0)

def hRAR_deriv(y):
    y = np.asarray(y, float)
    s = np.sqrt(np.maximum(y, 1e-300))
    e = np.exp(s)
    d = e - 1.0
    return (d - 0.5 * s * e) / (d * d)

def _solve(f, lo, hi, it=200):
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

Y_P = _solve(lambda y: np.exp(-math.sqrt(y)) - (1.0 - 0.5 * math.sqrt(y)), 1.5, 4.0)
H_P = float(h_RAR(Y_P))
Y_STAR = _solve(lambda y: DELTA_M * H_P / (y + Y_P) - hRAR_deriv(y), 1.5, 3.0)

def h_mono(y):
    y = np.asarray(y, float)
    out = np.empty_like(y)
    m = y <= Y_STAR
    out[m] = h_RAR(y[m])
    out[~m] = h_RAR(Y_STAR) + DELTA_M * H_P * np.log((y[~m] + Y_P) / (Y_STAR + Y_P))
    return out

# ------------------------------------------------------------ S^3 spectral calculus
def sphere_grid(L):
    Nt, Nu, Np = L + 3, 2 * L + 5, 2 * L + 5
    # Chebyshev-Gauss of the second kind in t (weight sqrt(1-t^2) = the S^3 surface factor)
    k = np.arange(1, Nt + 1)
    tk = np.cos(np.pi * k / (Nt + 1))
    wt = (np.pi / (Nt + 1)) * np.sin(np.pi * k / (Nt + 1)) ** 2
    uj, wu = np.polynomial.legendre.leggauss(Nu)
    ps = 2.0 * np.pi * (np.arange(Np) + 0.5) / Np
    wp = np.full(Np, 2.0 * np.pi / Np)
    T, U, P = np.meshgrid(tk, uj, ps, indexing="ij")
    st, su = np.sqrt(1.0 - T * T), np.sqrt(1.0 - U * U)
    x = np.stack([T, st * U, st * su * np.cos(P), st * su * np.sin(P)], axis=-1).reshape(-1, 4)
    W = wt[:, None, None] * wu[None, :, None] * wp[None, None, :]
    w = (W.ravel() / (2.0 * np.pi ** 2)).copy()
    return x, w

class S3:
    """Round S^3 leaf: quadrature-exact harmonic basis + gradient/hessian recursion."""
    def __init__(self, L):
        self.L = L
        self.x, self.w = sphere_grid(L)
        self.G = self.x.shape[0]
        self.V = []
        self.Q = []          # Q[l]: (n_l, 4 n_{l-1}) orthonormalization coefficients
        self._build()
        self.n = sum(v.shape[0] for v in self.V)
        self.dims = [v.shape[0] for v in self.V]
        self.mode_level = np.concatenate([np.full(v.shape[0], l) for l, v in enumerate(self.V)])
        self.lam = self.mode_level * (self.mode_level + 2.0)
        Vtot = np.concatenate(self.V, axis=0)
        self.gram_residual = float(np.max(np.abs((Vtot * self.w[None, :]) @ Vtot.T - np.eye(self.n))))

    def _build(self):
        x, w, G = self.x, self.w, self.G
        self.V = [np.ones((1, G))]
        self.Q = [None]
        self.Gr = [np.zeros((4, 1, G))]          # cached ambient gradients per level
        for l in range(1, self.L + 1):
            vp = self.V[-1]
            nl = vp.shape[0]
            cand = np.stack([x[:, i, None] * vp.T for i in range(4)], axis=1).reshape(G, 4 * nl)
            # project out all previous levels (candidates span H_l plus lower-layer pullbacks)
            Vprev = np.concatenate(self.V, axis=0)               # (n_prev, G)
            proj = Vprev.T @ (Vprev @ (cand * w[:, None]))
            R = cand - proj
            del proj, cand
            Gram = R.T @ (R * w[:, None])
            vals, vecs = np.linalg.eigh(Gram)
            keep = vals > 1e-10 * vals[-1]
            nk = int(np.count_nonzero(keep))
            assert nk == (l + 1) ** 2, f"level {l}: kept {nk}, expected {(l + 1) ** 2}"
            Q = vecs[:, keep] / np.sqrt(vals[keep][None, :])
            self.V.append(Q.T @ R.T)
            self.Q.append(Q.T)
            del R, Gram, vals, vecs, Vprev
            # gradient of this level's basis from the previous level's cached gradient
            gp = self.Gr[l - 1]
            cg = np.zeros((4, 4 * nl, G))
            for i in range(4):
                seg = slice(i * nl, (i + 1) * nl)
                cg[:, seg, :] = np.where(np.arange(4)[:, None, None] == i, vp[None, :, :], 0.0)
                cg[:, seg, :] += x[:, i][None, None, :] * gp
            self.Gr.append(np.einsum("ab,jbg->jag", Q.T, cg))
            del cg, Q

    def save_cache(self, path):
        np.savez(path, x=self.x, w=self.w, gram_res=self.gram_residual,
                            **{f"v{i}": v for i, v in enumerate(self.V)},
                            **{f"g{i}": g for i, g in enumerate(self.Gr)},
                            **{f"q{i}": q for i, q in enumerate(self.Q) if q is not None})

    @classmethod
    def load_cache(cls, path):
        z = np.load(path, mmap_mode="r")
        L = max(int(k[1:]) for k in z.files if k[0] == "v")
        obj = cls.__new__(cls)
        obj.L = L
        obj.x = z["x"]
        obj.w = z["w"]
        obj.G = obj.x.shape[0]
        obj.V = [z[f"v{i}"] for i in range(L + 1)]
        obj.Gr = [z[f"g{i}"] for i in range(L + 1)]
        obj.Q = [None] + [z[f"q{i}"] for i in range(1, L + 1)]
        obj.n = sum(v.shape[0] for v in obj.V)
        obj.dims = [v.shape[0] for v in obj.V]
        obj.mode_level = np.concatenate(
            [np.full(v.shape[0], l) for l, v in enumerate(obj.V)])
        obj.lam = obj.mode_level * (obj.mode_level + 2.0)
        obj.gram_residual = float(z["gram_res"])
        return obj

    def _idx(self, l):
        a = sum(k * k for k in range(l + 1))
        return slice(a, a + (l + 1) ** 2)

    def grad_level(self, l):
        """AMBIENT derivatives of the level-l basis: (4, n_l, G). Cached in _build."""
        return self.Gr[l]

    def grad_level_o(self, l):
        """one-shot recursion used by grad_level; recomputes the chain per level."""
        if l == 0:
            return np.zeros((4, 1, self.G))
        return self.grad_level(l)

    def grad_ambient(self, c):
        """Ambient derivatives of the polynomial extension of field c (unprojected)."""
        g = np.zeros((4, self.G))
        for l in range(1, self.L + 1):
            ic = self._idx(l)
            cc = c[ic]
            if np.any(cc):
                g += np.einsum("a,jag->jg", cc, self.grad_level(l))
        return g

    def grad(self, c):
        """INTRINSIC gradient of field c (tangential projection of the ambient derivative)."""
        g = self.grad_ambient(c)
        gx = np.einsum("jg,jg->g", g, self.x.T)
        return g - gx[None, :] * self.x.T

    def hess_field(self, c, block=640):
        """Ambient Hessian of the polynomial extension of field c. Recursion per level:
        cand hessian of x_i Y_{l-1,gamma}:  d_k d_j = d_ik d_j Y + d_ij d_k Y + x_i d_k d_j Y.""" 
        H = np.zeros((4, 4, self.G))
        x = self.x
        for b0 in range(0, self.G, block):
            b1 = min(b0 + block, self.G)
            sl = slice(b0, b1)
            blk = b1 - b0
            Hprev = np.zeros((4, 4, 1, blk))
            for l in range(1, self.L + 1):
                ic = self._idx(l)
                cc = c[ic]
                nl1 = self.V[l - 1].shape[0]
                Gp = self.grad_level(l - 1)                      # (4, nl1, G)
                Gpb = Gp[:, :, sl]
                ch = np.zeros((4, 4, 4 * nl1, blk))
                for i in range(4):
                    seg = slice(i * nl1, (i + 1) * nl1)
                    for j in range(4):
                        # d_ik d_j Y : add G[j] to row j, col k=i
                        ch[j, :, seg, :] += (np.arange(4)[:, None, None] == i) * Gpb[j][None, :, :]
                    # d_ij d_k Y : rows j == i get G[k] added along the k axis
                    ch[:, :, seg, :] += (np.arange(4)[:, None, None, None] == i) * Gpb[None, :, :, :]
                    ch[:, :, seg, :] += x[sl, i][None, None, None, :] * Hprev
                Hl = np.einsum("ab,jkbg->jkag", self.Q[l], ch)   # (4,4,n_l,blk)
                Hprev = Hl
                if np.any(cc):
                    H[:, :, sl] += np.einsum("a,jkag->jkg", cc, Hl)
        return H

    def coeffs(self, f):
        return np.concatenate([(v * self.w[None, :]) @ f for v in self.V])

    def values(self, c):
        out = np.zeros(self.G)
        for l, v in enumerate(self.V):
            out += v.T @ c[self._idx(l)]
        return out

    def heat(self, c, b):
        return c * np.exp(-b * self.lam)

    def green(self, c):
        out = np.zeros_like(c)
        m = self.mode_level > 0
        out[m] = c[m] / self.lam[m]
        return out

def _build_leaf_cli(L, path):
    """Child-process leaf builder: peak RSS of the build never enters the parent."""
    leaf = S3(L)
    leaf.save_cache(path)
    print(f"leaf L={L} built: n={leaf.n} G={leaf.G} gram_res={leaf.gram_residual:.3e}")

# ------------------------------------------------------------ flat twin on the torus
def torus_pipeline(b, n=28, kmax=12, seed=7):
    import numpy.fft as FF
    ax = [np.linspace(0, 2 * np.pi, n, endpoint=False) for _ in range(3)]
    X = np.meshgrid(*ax, indexing="ij")
    Kf = [np.fft.fftfreq(n, d=2 * np.pi / n) for _ in range(3)]
    K = np.meshgrid(*Kf, indexing="ij")
    K2 = sum(ki ** 2 for ki in K)
    rng = np.random.default_rng(seed)
    u = np.zeros((n, n, n))
    for d in range(3):
        for kk in range(1, kmax + 1):
            u += np.cos(kk * X[d] + rng.uniform(0, 2 * np.pi)) / kk ** 2.5
    u -= u.mean()
    uk = FF.fftn(u)
    du = [FF.ifftn(1j * K[i] * uk).real for i in range(3)]
    sk = np.exp(-b * K2)
    H = [FF.ifftn(FF.fftn(du[i]) * sk).real for i in range(3)]
    Hm = np.sqrt(sum(hi ** 2 for hi in H))
    F = [(h_mono(Hm) / np.where(Hm > 0, Hm, 1.0)) * H[i] for i in range(3)]
    Fk = [FF.fftn(F[i]) for i in range(3)]
    denom = np.where(K2 > 0, K2, 1.0)
    daph = [None] * 3
    for i in range(3):
        W = sum(K[i] * K[j] * Fk[j] for j in range(3))
        W = np.where(K2 > 0, W / denom, 0.0)
        daph[i] = FF.ifftn(1j * K[i] * sk * W).real
    daphN = np.sqrt(sum(di ** 2 for di in daph))
    divF = sum(1j * K[i] * Fk[i] for i in range(3))
    up = np.where(K2 > 0, -divF / denom, 0.0)
    aph2 = [-FF.ifftn(1j * K[i] * (up * sk)).real for i in range(3)]
    aph1 = [-FF.ifftn(sk * (sum(K[j] * Fk[j] for j in range(3)) / denom)).real for i in range(3)]
    resid = max(float(np.max(np.abs(aph2[i] - aph1[i]))) for i in range(3))
    comm = 0.0
    for i in range(3):
        t = FF.ifftn(1j * K[i] * sk * FF.fftn(du[i])).real - FF.ifftn(sk * (1j * K[i] * uk)).real
        comm = max(comm, float(np.max(np.abs(t))))
    kk = np.arange(-30, 31)
    K3 = np.meshgrid(kk, kk, kk)
    K2s = sum(ki ** 2 for ki in K3)
    M2 = float(np.sum(K2s[K2s > 0] * np.exp(-2.0 * b * K2s[K2s > 0])))
    f2 = math.sqrt(sum(float(np.mean(fi ** 2)) for fi in F))
    return {"commutator_DS_SD_max": comm, "reduction_residual": resid,
            "r_flat": float(np.max(daphN)) / (math.sqrt(M2) * f2), "M2": M2,
            "daph_max": float(np.max(daphN)), "f2": f2}

# ------------------------------------------------------------ one S^3 run
def run_s3(L, b, lapse_eps, target_supH, tag, out, rngs, leaf=None):
    leaf = leaf if leaf is not None else S3(L)
    G = leaf.G
    lam = leaf.lam
    diml = (leaf.mode_level + 1) ** 2
    # kernel constants: spectral-sum form AND operator-sup measured on the grid
    mC0 = math.sqrt(float(np.sum(diml * np.exp(-2.0 * b * lam))))
    mCg = math.sqrt(float(np.sum(diml * lam * np.exp(-2.0 * b * lam))))
    mChh = math.sqrt(float(np.sum(diml * lam ** 2 * np.exp(-2.0 * b * lam))))
    mCG = math.sqrt(float(np.sum(diml[1:] / lam[1:] ** 2)))
    sC0 = 0.0
    sq = np.zeros(G)
    for l in range(leaf.L + 1):
        sq += np.sum((np.exp(-b * lam[leaf._idx(l)])[:, None] * leaf.V[l]) ** 2, axis=0)
    sC0 = float(np.sqrt(np.max(sq)))
    sq.fill(0.0)
    for l in range(1, leaf.L + 1):
        gv = np.einsum("a,jag->jg", np.exp(-b * lam[leaf._idx(l)]), leaf.grad_level(l))
        sq += np.sum(gv ** 2, axis=0)
    sCg = float(np.sqrt(np.max(sq)))
    C0, Cg, Chh, CG = mC0, mCg, mChh, mCG
    R0, lam1, B_ell = 2.0, 3.0, math.sqrt(3.0)

    # lapse
    Y1 = leaf.V[1]
    Nv = 1.0 + lapse_eps * Y1[0]
    cN = leaf.coeffs(Nv)
    glnN = leaf.grad(cN) / Nv[None, :]
    L_N = float(np.max(np.sqrt(np.sum(glnN ** 2, axis=0))))
    cmin, cmax = float(np.min(Nv)), float(np.max(Nv))

    # source (deterministic), normalized ||grad u||_2 = 1, amplitude-gated to target sup|H|
    csrc = np.zeros(leaf.n)
    for l in range(1, leaf.L + 1):
        csrc[leaf._idx(l)] = rngs.standard_normal(leaf.dims[l]) / (l + 1) ** 1.5
    gu = leaf.grad(csrc)
    csrc /= math.sqrt(float(np.sum(gu ** 2 * leaf.w[None, :])))
    H0 = leaf.grad(leaf.heat(csrc, b))
    supH = math.sqrt(float(np.max(np.sum(H0 ** 2, axis=0))))
    csrc *= target_supH / supH if supH > 0 else 1.0
    H0 = leaf.grad(leaf.heat(csrc, b))
    supH = float(np.sqrt(np.max(np.sum(H0 ** 2, axis=0))))
    Hm = np.sqrt(np.sum(H0 ** 2, axis=0))
    Fv = (h_mono(Hm) / np.where(Hm > 0, Hm, 1.0)) * H0

    # longitudinal elliptic projection
    dFc = np.zeros(leaf.n)
    for l in range(1, leaf.L + 1):
        gl = leaf.grad_level(l)
        dFc[leaf._idx(l)] = -np.einsum("jg,jag->a", Fv * leaf.w[None, :], gl)
    up = leaf.green(dFc)
    up[0] = 0.0
    P_F = leaf.grad(up)
    f2 = float(np.sqrt(np.sum(Fv * Fv * leaf.w)))
    dPL2 = float(np.sqrt(np.sum(P_F * P_F * leaf.w)))
    up_inf = float(np.sqrt(np.max(leaf.values(up) ** 2)))
    if os.environ.get("AS204_MEMTRACE"):
        print("MEM green: rss MB",
              round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 1))

    # weighted adjoint: S_h^* u' = N^{-1} S_h (N u')
    cSNu = leaf.heat(leaf.coeffs(Nv * leaf.values(up)), b)
    vstar = leaf.values(cSNu) / Nv
    cstar = leaf.coeffs(vstar)
    aph = -leaf.grad(cstar)
    aph_n2 = np.sum(aph ** 2, axis=0)

    # derivative of the physical force: ||grad a_ph||^2 = Tr(J^T J) - ||J x||^2 - ||J^T x||^2
    # + (x^T J x)^2 with J = ambient Jacobian of the field -grad_S v ITSELF (a polynomial
    # extension that equals the force on the sphere; J = -Hess(v) alone is the Jacobian of the
    # UNPROJECTED gradient and invalid).  J[i,j] = -Hess[i,j] + (Hess.x)[j] x[i] + g[j] x[i]
    # + (g.x) delta[i,j], g = grad_ambient(v).
    gA = leaf.grad_ambient(cstar)
    Hv = leaf.hess_field(cstar)
    gAx = np.einsum("jg,jg->g", gA, leaf.x.T)
    Hxx = np.einsum("ijg,jg->ig", Hv, leaf.x.T)
    J = -Hv.copy()
    if os.environ.get("AS204_MEMTRACE"):
        print("MEM daph: hess done, rss MB",
              round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 1))
    for i in range(4):
        J[:, i, :] += (Hxx[i][None, :] + gA[i][None, :]) * leaf.x.T
        J[i, i, :] += gAx
    tr = np.einsum("ijg,ijg->g", J, J)
    Jx = np.einsum("ijg,jg->ig", J, leaf.x.T)
    JTx = np.einsum("ijg,ig->jg", J, leaf.x.T)
    xJx = np.einsum("ijg,ig,jg->g", J, leaf.x.T, leaf.x.T)
    daph2 = tr - np.einsum("ig,ig->g", Jx, Jx) - np.einsum("jg,jg->g", JTx, JTx) + xJx
    daph2 = np.maximum(daph2, 0.0)
    daph_max = float(np.sqrt(np.max(daph2)))
    int_hess = float(np.sum(tr * leaf.w))
    int_form = float(np.sum(np.array([2.0 * l * l * (l * l + 2.0 * l + 2.0)
                                      for l in range(1, leaf.L + 1)])
                            * np.array([np.sum(cstar[leaf._idx(l)] ** 2)
                                        for l in range(1, leaf.L + 1)])))
    hess_int_rel = abs(int_hess - int_form) / (int_form + 1e-300)

    # controls
    cstar0 = leaf.coeffs(leaf.values(up))
    b0resid = float(np.max(np.abs(leaf.grad(cstar0) - P_F)))
    Wc = np.zeros(leaf.n)
    for l in range(1, leaf.L + 1):
        Wc[leaf._idx(l)] = rngs.standard_normal(leaf.dims[l]) / (l + 1)
    Wf = leaf.values(Wc)
    lhs = float(np.sum(leaf.w * Nv * vstar * Wf))
    rhs = float(np.sum(leaf.w * (Nv * leaf.values(up)) * leaf.values(leaf.heat(Wc, b))))
    adj_rel = abs(lhs - rhs) / (abs(lhs) + abs(rhs) + 1e-300)
    # DS = SD on curved geometry (NC1): e^{b grad*grad}(grad f) = e^{-2b} grad(S_h f) on S^3
    gSf = leaf.grad(leaf.heat(csrc, b))
    ratio = 1.0 - math.exp(-2.0 * b)
    ds_num = float(np.sum((gSf * (math.exp(-2.0 * b) - 1.0)) ** 2 * leaf.w[None, :]))
    ds_den = float(np.sum(gSf ** 2 * leaf.w[None, :]))
    # negative control NC2
    flat = torus_pipeline(b)
    E_flat = math.sqrt(flat["M2"]) * f2
    r_naive = daph_max / E_flat if E_flat > 0 else float("nan")
    # corrected bound
    K_tot = final_constant(C0, Cg, Chh, CG, R0, lam1, B_ell, L_N, cmin, cmax, b)
    r_curved = daph_max / (K_tot * f2) if f2 > 0 else float("nan")
    # Weitzenbock modal check on the first l=1 and l=2 modes
    wz = []
    for l in (2, 3):
        ic = leaf._idx(l)
        for mm in range(2):
            e = np.zeros(leaf.n)
            e[ic.start + mm] = 1.0
            He = leaf.hess_field(e)
            h2 = float(np.sum(np.einsum("ijg,ijg->g", He, He) * leaf.w))
            lam_e = float(lam[ic.start + mm])
            wz.append({"mode": int(ic.start + mm), "lam": lam_e,
                       "Hess2_integrated": h2,
                       "Hess2_empirical_e_l": E_TABLE[l],
                       "rel_resid": abs(h2 - E_TABLE[l]) / (E_TABLE[l] + 1e-300)})
    out[tag] = {
        "L": L, "grid": G, "n_modes": leaf.n, "b": b, "lapse_eps": lapse_eps,
        "target_supH": target_supH, "gram_residual": leaf.gram_residual,
        "supH": supH, "f2": f2, "P_L_contraction_ratio": dPL2 / f2, "up_inf": up_inf,
        "daph_max": daph_max,
        "beta_comm": C0 * R0 * math.sqrt(2.0 * b / math.e),
        "r_naive_flat_transfer": r_naive, "E_flat": E_flat,
        "K_tot": K_tot, "r_curved_corrected": r_curved,
        "constants": {"C0": C0, "Cg": Cg, "Chh": Chh, "CG": CG, "R0": R0, "lambda1": lam1,
                      "B_ell": B_ell, "C0_sup": sC0, "Cg_sup": sCg,
                      "C0_sup_over_formula": sC0 / C0, "Cg_sup_over_formula": sCg / Cg},
        "lapse": {"L_N": L_N, "c_min": cmin, "c_max": cmax},
        "controls": {
            "b0_limit_residual": b0resid,
            "adjoint_identity_relative_residual": adj_rel,
            "hessian_integrated_relative_residual": hess_int_rel,
            "weitzenbock_modes": wz,
            "DS_equals_SD_curved_sq_ratio": ds_num / (ds_den + 1e-300),
            "DS_equals_SD_curved_closed_form_sq": ratio ** 2,
            "DS_equals_SD_curved_closed_form_match": abs(ds_num / (ds_den + 1e-300) - ratio ** 2)
                                                     / (ratio ** 2 + 1e-300),
            "flat_twin": flat,
        },
    }
    return leaf

class _R:
    def __init__(self, n):
        pass

def final_constant(C0, Cg, Chh, CG, R0, lam1, B_ell, L_N, cmin, cmax, b):
    """K_tot = termwise chain (derivation.md eq. (B)); rho2 = ||grad Ric|| = 0 on S^3."""
    K = (1.0 / cmin) * (Chh * cmax / lam1)                     # N^-1 Hess(S_h N u')
    K += (L_N / cmin) * (Cg * cmax / lam1)                      # grad(N^-1) . grad(S_h N u')
    K += (L_N / cmin) * (C0 * cmax * L_N * CG)                  # grad(N^-1) S_h ((grad N) u')
    K += (1.0 / cmin) * (C0 * R0 * math.sqrt(2.0 * b / math.e)) * (cmax * L_N * CG)
    K += (1.0 / cmin) * Cg * (2.0 * L_N * cmax * CG / lam1)
    K += (L_N / cmin) * (C0 * cmax * B_ell)                     # grad(N^-1) S_h^* grad u'
    K += (1.0 / cmin) * Cg * cmax * B_ell                       # N^-1 grad S_h^* grad u'
    return K

def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--buildleaf":
        _build_leaf_cli(int(sys.argv[2]), sys.argv[3])
        return
    out: dict = {"seed": "AS204", "run_id": "run_20260928T1715"}
    eps = 1e-6
    dl = (h_RAR(Y_STAR) - h_RAR(Y_STAR - eps)) / eps
    dr = (h_mono(Y_STAR + eps) - h_mono(Y_STAR)) / eps
    out["constitutive"] = {"y_star": Y_STAR, "y_p": Y_P, "h_p": H_P,
                           "splice_condition_residual": float(
                               abs(hRAR_deriv(Y_STAR) - DELTA_M * H_P / (Y_STAR + Y_P))),
                           "C1_join_relative_residual": float(abs(dl - dr) / max(abs(dl), 1e-30)),
                           "h_RAR_deep_coeff": float(h_RAR(1e-8) / 1e-4)}
    runs = [(8, 0.05, 0.0, 2.3374), (8, 0.05, 0.3, 2.3374), (8, 0.2, 0.0, 2.3374),
            (8, 0.2, 0.3, 2.3374), (8, 0.2, 0.3, 1.2), (8, 0.2, 0.3, 4.0)]
    run_dir = os.path.dirname(os.path.abspath(__file__))
    leaf_files = {}
    for L in sorted({L for (L, *_r) in runs}):
        cache = os.path.join(run_dir, f"leaf_L{L}.npz")
        if not os.path.exists(cache):
            sub = subprocess.run([sys.executable, os.path.abspath(__file__),
                                  "--buildleaf", str(L), cache],
                                 capture_output=True, text=True)
            if sub.returncode != 0 or not os.path.exists(cache):
                raise RuntimeError(f"leaf build failed for L={L}: {sub.stderr[-2000:]}")
        leaf_files[L] = cache
    out["leaves"] = {}
    out["runs"] = {}
    rngs = np.random.default_rng(204)
    completed = []
    leaves = {}
    last_L = None
    for (L, b, e, t) in runs:
        tag = f"L{L}_b{str(b)}_e{str(e)}_t{str(t)}"
        if last_L is not None and L != last_L:
            del leaves[last_L]
            gc.collect()
        if L not in leaves:
            leaves[L] = S3.load_cache(leaf_files[L])
            budget("leaf load")
            out["leaves"][str(L)] = {"n": int(leaves[L].n), "G": int(leaves[L].G),
                                     "gram_residual": float(leaves[L].gram_residual)}
        last_L = L
        try:
            run_s3(L, b, e, t, tag, out["runs"], rngs, leaf=leaves[L])
            completed.append(tag)
            budget("run loop")
        except SystemExit as ex:
            out["wall_budget_truncation"] = str(ex)
            out["completed_runs"] = completed
            break
    out["completed_runs"] = completed
    out["footings"] = footing_table(out["runs"])
    out["enforcement"] = enforcement()
    with open("residuals.json", "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    print(json.dumps(out, indent=1, default=float))

def enforcement():
    wall = time.monotonic() - T0
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return {"declared_wall_s": 120, "declared_memory_MB": 512, "declared_threads": 1,
            "measured_wall_s": wall, "measured_maxrss_bytes": int(rss),
            "enforced": ("external 'ulimit -t 120'; OMP/OPENBLAS/MKL/VECLIB threads forced to 1 "
                         "before numpy import; internal wall > 115 s or RSS > 512 MB raises SystemExit")}

def footing_table(runs):
    tag0 = next(iter(runs))
    r = runs[tag0]
    volh = 2.0 * math.pi ** 2
    c1 = math.sqrt(Y_P)
    Fb_can = c1 * math.sqrt(volh * (r["supH"] / A0_CAN))
    Fb_alt = c1 * math.sqrt(volh * (r["supH"] / A0_ALT))
    return {
        "a0_canonical": A0_CAN, "a0_alternative": A0_ALT, "kappa_adopted": KAPPA,
        "rho_Lambda_canonical": RHO_L_CAN, "rho_Lambda_alternative": RHO_L_ALT,
        "rho_ratio_alt_over_can": RHO_L_ALT / RHO_L_CAN,
        "kappa_eff_if_rho_fixed": KAPPA * A0_ALT / A0_CAN,
        "note": ("All bound constants are a0-free: both footings apply with the identical K_tot at "
                 "kappa = 1/2 (kappa fixed -> densities differ by (a0_alt/a0_can)^2); "
                 "||F||_2 <= c sqrt(vol_h * ||H||_inf / a0) carries the 1/sqrt(a0) factor."),
        "F2_bound_canonical": Fb_can, "F2_bound_alternative": Fb_alt,
        "F2_bound_ratio_alt_over_can": math.sqrt(A0_CAN / A0_ALT),
        "K_tot_footing_independent": r["K_tot"],
    }

if __name__ == "__main__":
    main()