"""V3X lower-memory Route N solver: C6's Newton loop with the linear solve swapped.

C6's code (covariant_push_2026_10_22/C6_literal_cassini/c6_solver.py) and D7d's (doors_push_2026_10_22/D7d_screened_q2/
d7d_solver.py) are imported READ-ONLY (no bytecode written). Only the linear solve inside each Newton step changes:
  method "A": block-tridiagonal direct LU on two-shell super-blocks (shell-interleaved order; the grad-div operator couples
              shells i +- 2, so pairs of shells make the matrix block-tridiagonal). Dense LAPACK LU per super-block; the
              eliminated upper blocks X_j = D_j^-1 C_j are streamed to a scratch file outside the repo and read back in
              reverse, so RSS holds O(1) blocks.
  method "B": SuperLU with a fill-reducing column ordering (permc_spec) on the same scaled Jacobian (cross-check).
  method "C6": C6's own splu(NATURAL) on the interleaved matrix (reference, as V3W ran it).
The Jacobian, residual, row scaling and line search are C6's solve_v, line by line.
kappa = 1/2 FITTED; footings never pooled; adopts nothing; not theory closed.
"""
import os, sys, tempfile
sys.dont_write_bytecode = True
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl
import scipy.linalg as sla
import scipy.linalg.lapack as lapack
import scipy.linalg.blas as blas

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "covariant_push_2026_10_22", "C6_literal_cassini"))
import c6_solver as C          # read-only
S = C.S                        # D7d's solver module, read-only
SCRATCH = os.environ.get("V3X_SCRATCH", tempfile.gettempdir())


class BlockTridiagLU:
    """Gaussian elimination with partial pivoting on a block-tridiagonal Jp (CSR, interleaved order), super-block size bs
    (last block may be shorter). At step j the pivot is searched over block rows j and j + 1 (the only rows with entries
    in block column j), as banded LU does; U gains one block of fill (j + 2). The factors (tall L panel with its row
    permutation, U12) are streamed to a scratch file outside the repo and read back per solve. All dense work uses
    preallocated buffers and BLAS/LAPACK in place, so RSS holds O(1) panels (no allocator growth over blocks)."""

    def __init__(self, Jp, bs):
        N = Jp.shape[0]
        self.Jp = Jp = Jp.tocsr(); self.N = N
        self.e = e = list(range(0, N, bs)) + [N]
        self.nb = nb = len(e) - 1
        for i in range(nb):                               # structure: block row i touches block columns i-1..i+1 only
            ind = Jp.indices[Jp.indptr[e[i]]:Jp.indptr[e[i + 1]]]
            if ind.size and (ind.min() < e[max(i - 1, 0)] or ind.max() >= e[min(i + 2, nb)]):
                raise RuntimeError("matrix is not block-tridiagonal at this block size")
        self.sz = sz = [e[i + 1] - e[i] for i in range(nb)]
        fd, self.path = tempfile.mkstemp(prefix="v3x_blk_", suffix=".bin", dir=SCRATCH)
        os.close(fd)
        self.off = []
        b = max(sz)
        Pf = np.zeros((2 * b, 3 * b), order="F")          # panel [carry; next block row] x block columns j..j+2
        Rt = np.zeros((b, 2 * b), order="F"); Rb = np.zeros((b, 2 * b), order="F")
        Lb = np.zeros((b, b), order="F"); L2 = np.zeros((b, b), order="F")
        def cols(c0, c1):
            return e[c0], e[min(c1, nb)]
        with open(self.path, "wb") as fh:
            a0, a1 = cols(0, 3)
            Pf[:sz[0], :a1 - a0] = Jp[e[0]:e[1]][:, a0:a1].toarray()
            for j in range(nb):
                bj = sz[j]
                bj1 = sz[j + 1] if j + 1 < nb else 0
                c0, c1 = cols(j, j + 3)
                ncol = c1 - c0                            # block columns j..j+2 present
                m = bj + bj1
                if bj1:
                    Pf[bj:m, :ncol] = Jp[e[j + 1]:e[j + 2]][:, c0:c1].toarray()
                if bj == b and m == 2 * b:
                    lu, piv, info = lapack.dgetrf(Pf[:, :b], overwrite_a=1)
                else:
                    lu, piv, info = lapack.dgetrf(np.asfortranarray(Pf[:m, :bj]))
                if info < 0:
                    raise RuntimeError(f"dgetrf info {info}")
                perm = np.arange(m)
                for i in range(bj):
                    p_ = piv[i]
                    if p_ != i:
                        perm[i], perm[p_] = perm[p_], perm[i]
                o = [fh.tell()]
                fh.write(np.asfortranarray(lu).T.data)
                fh.write(perm.astype(np.int64).tobytes())
                nr = ncol - bj                            # columns right of block j
                if nr:
                    right = Pf[:m, bj:ncol]
                    top = Rt[:bj, :nr] if (bj == b and nr == 2 * b) else np.zeros((bj, nr), order="F")
                    np.take(right, perm[:bj], axis=0, out=top, mode="clip")
                    Lb[:bj, :bj] = lu[:bj, :bj]
                    Lv = Lb if bj == b else np.asfortranarray(Lb[:bj, :bj])
                    top = blas.dtrsm(1.0, Lv, top, lower=1, diag=1, overwrite_b=1)
                    o.append(fh.tell()); fh.write(np.asfortranarray(top).T.data)
                    if bj1:
                        bot = Rb if (bj1 == b and nr == 2 * b) else np.zeros((bj1, nr), order="F")
                        np.take(right, perm[bj:], axis=0, out=bot, mode="clip")
                        L2[:bj1, :bj] = lu[bj:m, :bj]
                        L2v = L2 if (bj1 == b and bj == b) else np.asfortranarray(L2[:bj1, :bj])
                        bot = blas.dgemm(-1.0, L2v, top, beta=1.0, c=bot, overwrite_c=1)
                        # next panel: carry = bot on block columns j+1..j+3 (j+3 part zero)
                        Pf[:bj1, :nr] = bot
                        Pf[:bj1, nr:] = 0.0
                o.append(nr)
                self.off.append(o)
                del lu

    def solve(self, rhs):
        e, nb, sz = self.e, self.nb, self.sz
        b = max(sz)
        ys = []
        buf = np.empty(2 * b * 2 * b)
        def rd(fh, off, shape, dtype=np.float64):
            fh.seek(off)
            n = int(np.prod(shape))
            if dtype is np.float64:
                v = buf[:n]
                fh.readinto(memoryview(v).cast("B"))
                return v.reshape(shape, order="F")
            return np.frombuffer(fh.read(n * 8), dtype=dtype)
        with open(self.path, "rb") as fh:
            c = rhs[e[0]:e[1]].copy()
            for j in range(nb):
                bj = sz[j]
                w = np.concatenate([c, rhs[e[j + 1]:e[j + 2]]]) if j + 1 < nb else c
                m = w.size
                perm = rd(fh, self.off[j][0] + m * bj * 8, (m,), np.int64)
                lu = rd(fh, self.off[j][0], (m, bj))
                w = w[perm]
                y = sla.solve_triangular(lu[:bj], w[:bj], lower=True, unit_diagonal=True, check_finite=False)
                if j + 1 < nb:
                    c = w[bj:] - lu[bj:] @ y
                ys.append(y)
            x = np.empty(self.N)
            for j in range(nb - 1, -1, -1):
                bj = sz[j]; m = bj + (sz[j + 1] if j + 1 < nb else 0)
                r = ys[j]
                nr = self.off[j][-1]
                if nr:
                    U12 = rd(fh, self.off[j][1], (bj, nr))
                    r = r - U12 @ x[e[j + 1]:e[j + 1] + nr]
                lu = rd(fh, self.off[j][0], (m, bj))
                x[e[j]:e[j + 1]] = sla.solve_triangular(lu[:bj], r, lower=False, check_finite=False)
        return x

    def close(self):
        if os.path.exists(self.path):
            os.unlink(self.path)


def block_tridiag_solve(Jp, rhs, bs, refine=1):
    """Solve Jp x = rhs with BlockTridiagLU plus `refine` steps of iterative refinement (same factors)."""
    F = BlockTridiagLU(Jp, bs)
    try:
        x = F.solve(rhs)
        for _ in range(refine):
            x = x + F.solve(rhs - F.Jp @ x)
    finally:
        F.close()
    return x


def solve_v(g, Lam, xe, rF=0.0, maxit=60, U0=None, mutate=False, tol=1e-9, method="A", permc="MMD_AT_PLUS_A", mu=0.0, polish=0):
    """C6's solve_v (Route N in the Galactic field) with the linear solve swapped; returns U (3,Nr,Nt), residual, iterations.
    mu > 0: the Newton step solves (Js + mu I_q) dU = -sc F, a diagonal shift on the w rows of the row-scaled Jacobian
    (bounds the step in float64-null directions); the residual, scaling, line search and the convergence test are C6's.
    polish > 0: after the residual first drops below tol, up to `polish` further Newton steps are taken while the line
    search still lowers the residual (the converged state still satisfies C6's test; this only removes the shift's bias)."""
    A, rhs, nl = C.build(g, Lam, rF, mutate)
    Nr, Nt = g.Nr, g.Nt; n = Nr * Nt
    CT = np.broadcast_to(g.ct, (Nr, Nt)); ST = np.broadcast_to(g.st, (Nr, Nt))
    A = A.tocsc(); Apsi = A[:, :n]; Aq = A[:, n:]
    del A
    nlr = np.repeat(nl, Nt).astype(float)
    Dw = sp.diags(np.concatenate([nlr * np.repeat(g.r ** 2, Nt)] * 2))
    Z = sp.csc_matrix((n, 2 * n))
    perm = C.interleave(g)
    U = np.zeros(g.N) if U0 is None else U0.copy()

    def resid(U):
        wr = U[n:2 * n].reshape(Nr, Nt); wt = U[2 * n:].reshape(Nr, Nt)
        pr, pt, J = S.dP(xe, CT, ST, wr, wt)
        F = Apsi @ U[:n] + Aq @ np.concatenate([pr.ravel(), pt.ravel()]) + np.concatenate([np.zeros(n), Dw @ U[n:]]) - rhs
        return F, J
    fin = np.inf; it = 0; extra = 0
    for it in range(maxit + 1):
        F, J = resid(U)
        if not np.all(np.isfinite(F)): fin = np.inf; break
        Jb = sp.bmat([[sp.diags(J[0].ravel()), sp.diags(J[1].ravel())], [sp.diags(J[2].ravel()), sp.diags(J[3].ravel())]])
        Jac = sp.hstack([Apsi, Aq @ Jb + sp.vstack([Z, Dw])]).tocsr()
        del Jb
        sc = 1 / np.maximum(abs(Jac).max(axis=1).toarray().ravel(), 1e-300)
        fin = np.linalg.norm(sc * F)
        if it == maxit: break
        if fin < tol:
            if extra >= polish: break
            extra += 1
        Js = (sp.diags(sc) @ Jac).tocsr(); del Jac
        if mu:
            Js = (Js + sp.diags(np.concatenate([np.zeros(n), np.full(2 * n, mu)]))).tocsr()
        if method == "A":
            Jp = Js[perm][:, perm].tocsr(); del Js
            dU = np.empty(g.N); dU[perm] = -block_tridiag_solve(Jp, (sc * F)[perm], 6 * Nt); del Jp
        elif method == "B":
            dU = -spl.splu(Js.tocsc(), permc_spec=permc).solve(sc * F); del Js
        elif method == "C6":
            Jp = Js[perm][:, perm].tocsc(); del Js
            dU = np.empty(g.N); dU[perm] = -spl.splu(Jp, permc_spec="NATURAL").solve((sc * F)[perm]); del Jp
        else:
            raise ValueError(method)
        alpha = 1.0
        for _ in range(40):
            Fn, _ = resid(U + alpha * dU)
            if np.all(np.isfinite(Fn)) and np.linalg.norm(sc * Fn) < (1 - 1e-4 * alpha) * fin: break
            alpha *= 0.5
        if alpha < 1e-9: break
        U = U + alpha * dU
    return U.reshape(3, Nr, Nt), fin, it


def grid(Lam, gres):
    """C6/V3W grid rule."""
    return S.Grid(1e-4, (1e3 if Lam <= 30 else 300.0) * max(1.0, Lam), gres[0], gres[1])
