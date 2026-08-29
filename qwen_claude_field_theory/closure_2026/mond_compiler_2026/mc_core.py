"""
mc_core.py -- symbolic tensor core for the relativistic-MOND inverse-design compiler.

Explicit-component sympy tensor calculus (no abstract index engine): a 4x4 metric of
sympy expressions, its Christoffels, Ricci, and covariant derivatives of a vector and a
symmetric rank-2 tensor.  Everything downstream (the operator basis, the three
reductions) is built on the `Ctx` object produced here, so the SAME operator definition
is reused verbatim in the static / Hessian / PPN reductions.

Conventions
-----------
signature (-,+,+,+); coords (t,x,y,z)
R^a_{bmn} = d_m Gamma^a_{nb} - d_n Gamma^a_{mb} + ...
R_{mn} = d_a Gamma^a_{mn} - d_n Gamma^a_{ma} + Gamma^a_{ab} Gamma^b_{mn} - Gamma^a_{nb} Gamma^b_{ma}
(so that for FRW / Schwarzschild R > 0 for ordinary matter; validated in mc_selftest.py)
"""
import sympy as sp

# ----------------------------------------------------------------------------------
# basic differential geometry on explicit components
# ----------------------------------------------------------------------------------

def christoffel(g, ginv, coords):
    n = len(coords)
    Gam = [[[sp.S.Zero] * n for _ in range(n)] for _ in range(n)]
    dg = [[[sp.diff(g[i, j], coords[k]) for k in range(n)] for j in range(n)] for i in range(n)]
    for a in range(n):
        for m in range(n):
            for q in range(m, n):
                s = sp.S.Zero
                for b in range(n):
                    if ginv[a, b] == 0:
                        continue
                    s += ginv[a, b] * (dg[b][m][q] + dg[b][q][m] - dg[m][q][b])
                s = sp.expand(s / 2)
                Gam[a][m][q] = s
                Gam[a][q][m] = s
    return Gam


def ricci(Gam, coords):
    n = len(coords)
    R = sp.zeros(n, n)
    for m in range(n):
        for q in range(m, n):
            e = sp.S.Zero
            for a in range(n):
                e += sp.diff(Gam[a][m][q], coords[a]) - sp.diff(Gam[a][m][a], coords[q])
                for b in range(n):
                    e += Gam[a][a][b] * Gam[b][m][q] - Gam[a][q][b] * Gam[b][m][a]
            e = sp.expand(e)
            R[m, q] = e
            R[q, m] = e
    return R


def cov_d_vector(A, Gam, coords):
    """A given with LOWER index.  returns DA[m][n] = nabla_m A_n."""
    n = len(coords)
    DA = [[sp.S.Zero] * n for _ in range(n)]
    for m in range(n):
        for q in range(n):
            e = sp.diff(A[q], coords[m])
            for a in range(n):
                e -= Gam[a][m][q] * A[a]
            DA[m][q] = sp.expand(e)
    return DA


def cov_d_tensor2(S, Gam, coords):
    """S symmetric with LOWER indices.  returns DS[m][n][p] = nabla_m S_{np}."""
    n = len(coords)
    DS = [[[sp.S.Zero] * n for _ in range(n)] for _ in range(n)]
    for m in range(n):
        for q in range(n):
            for p in range(q, n):
                e = sp.diff(S[q, p], coords[m])
                for a in range(n):
                    e -= Gam[a][m][q] * S[a, p] + Gam[a][m][p] * S[q, a]
                e = sp.expand(e)
                DS[m][q][p] = e
                DS[m][p][q] = e
    return DS


# ----------------------------------------------------------------------------------
# the context object every operator sees
# ----------------------------------------------------------------------------------

class Ctx:
    """Carries the metric + carrier multiplet and every contraction the basis needs."""

    def __init__(self, coords, g, phi, chi, A, S, lam, rho=sp.S.Zero, build_curvature=True,
                 trunc=None):
        self.coords = coords
        self.n = len(coords)
        self.g = g
        gi = g.inv()
        self.ginv = sp.Matrix(self.n, self.n, lambda i, j: sp.cancel(gi[i, j]))
        self.detg = sp.cancel(g.det())
        self.sqrtg = sp.sqrt(-self.detg)
        if trunc is not None:
            # keep every downstream expression POLYNOMIAL in the small metric potentials
            self.ginv = sp.Matrix(self.n, self.n, lambda i, j: trunc(self.ginv[i, j]))
            self.sqrtg = trunc(self.sqrtg)
        self.phi = phi
        self.chi = chi
        self.A = A            # list, LOWER index
        self.S = S            # Matrix, LOWER indices, traceless (flat trace imposed)
        self.lam = lam
        self.rho = rho

        self.Gam = christoffel(g, self.ginv, coords)
        if build_curvature:
            self.Ric = ricci(self.Gam, coords)
            self.Rs = sum(self.ginv[i, j] * self.Ric[i, j] for i in range(self.n)
                          for j in range(self.n))
        else:
            self.Ric = sp.zeros(self.n, self.n)
            self.Rs = sp.S.Zero

        # raised objects
        self.Au = [sum(self.ginv[i, j] * A[j] for j in range(self.n)) for i in range(self.n)]
        self.Sud = sp.Matrix(self.n, self.n,
                             lambda i, j: sum(self.ginv[i, k] * S[k, j] for k in range(self.n)))
        self.Suu = sp.Matrix(self.n, self.n,
                             lambda i, j: sum(self.ginv[i, k] * self.ginv[j, l] * S[k, l]
                                              for k in range(self.n) for l in range(self.n)))
        # derivatives
        self.dphi = [sp.diff(phi, c) for c in coords]
        self.dchi = [sp.diff(chi, c) for c in coords]
        self.dphiu = [sum(self.ginv[i, j] * self.dphi[j] for j in range(self.n))
                      for i in range(self.n)]
        self.dchiu = [sum(self.ginv[i, j] * self.dchi[j] for j in range(self.n))
                      for i in range(self.n)]
        self.DA = cov_d_vector(A, self.Gam, coords)
        self.DS = cov_d_tensor2(S, self.Gam, coords)

        # common scalars
        self.X = sum(self.dphiu[i] * self.dphi[i] for i in range(self.n))      # (grad phi)^2
        self.A2 = sum(self.Au[i] * A[i] for i in range(self.n))                # A_mu A^mu
        self.S2 = sum(self.Suu[i, j] * S[i, j] for i in range(self.n) for j in range(self.n))
        self.divA = sum(self.ginv[i, j] * self.DA[i][j] for i in range(self.n)
                        for j in range(self.n))
        self.Adphi = sum(self.Au[i] * self.dphi[i] for i in range(self.n))     # A^mu d_mu phi
        self.Adchi = sum(self.Au[i] * self.dchi[i] for i in range(self.n))
        self.dchi2 = sum(self.dchiu[i] * self.dchi[i] for i in range(self.n))

    # ---- helper contractions used by several operators ----
    def F(self, m, q):
        return self.DA[m][q] - self.DA[q][m]

    def F2(self):
        tot = sp.S.Zero
        for m in range(self.n):
            for q in range(self.n):
                for a in range(self.n):
                    for b in range(self.n):
                        gg = self.ginv[m, a] * self.ginv[q, b]
                        if gg == 0:
                            continue
                        tot += gg * self.F(m, q) * self.F(a, b)
        return tot

    def DAsq(self):
        """nabla_m A_n nabla^m A^n"""
        tot = sp.S.Zero
        for m in range(self.n):
            for q in range(self.n):
                for a in range(self.n):
                    for b in range(self.n):
                        gg = self.ginv[m, a] * self.ginv[q, b]
                        if gg == 0:
                            continue
                        tot += gg * self.DA[m][q] * self.DA[a][b]
        return tot

    def SdA(self):
        """S^{mn} nabla_m A_n"""
        return sum(self.Suu[m, q] * self.DA[m][q] for m in range(self.n) for q in range(self.n))

    def divS(self, q):
        """nabla_m S^{m}_{ q}  (one lower index left)"""
        tot = sp.S.Zero
        for m in range(self.n):
            for a in range(self.n):
                if self.ginv[m, a] == 0:
                    continue
                tot += self.ginv[m, a] * self.DS[m][a][q]
        return tot

    def divSu(self, q):
        return sum(self.ginv[q, b] * self.divS(b) for b in range(self.n))

    def DSsq(self):
        tot = sp.S.Zero
        for m in range(self.n):
            for a in range(self.n):
                if self.ginv[m, a] == 0:
                    continue
                for i in range(self.n):
                    for j in range(self.n):
                        for k in range(self.n):
                            for l in range(self.n):
                                gg = self.ginv[i, k] * self.ginv[j, l]
                                if gg == 0:
                                    continue
                                tot += self.ginv[m, a] * gg * self.DS[m][i][j] * self.DS[a][k][l]
        return tot

    def AAR(self):
        return sum(self.Au[m] * self.Au[q] * self.Ric[m, q]
                   for m in range(self.n) for q in range(self.n))

    def SR(self):
        return sum(self.Suu[m, q] * self.Ric[m, q]
                   for m in range(self.n) for q in range(self.n))

    def dphidphiR(self):
        return sum(self.dphiu[m] * self.dphiu[q] * self.Ric[m, q]
                   for m in range(self.n) for q in range(self.n))

    def SAA(self):
        return sum(self.Suu[m, q] * self.A[m] * self.A[q]
                   for m in range(self.n) for q in range(self.n))

    def Sdphidphi(self):
        return sum(self.Suu[m, q] * self.dphi[m] * self.dphi[q]
                   for m in range(self.n) for q in range(self.n))

    def Sdchidchi(self):
        return sum(self.Suu[m, q] * self.dchi[m] * self.dchi[q]
                   for m in range(self.n) for q in range(self.n))

    def SAdphi(self):
        return sum(self.Suu[m, q] * self.A[m] * self.dphi[q]
                   for m in range(self.n) for q in range(self.n))

    def SAdchi(self):
        return sum(self.Suu[m, q] * self.A[m] * self.dchi[q]
                   for m in range(self.n) for q in range(self.n))

    def AdivS(self):
        return sum(self.Au[q] * self.divS(q) for q in range(self.n))

    def divSdchi(self):
        return sum(self.divSu(q) * self.dchi[q] for q in range(self.n))

    def divSdivS(self):
        return sum(self.divSu(q) * self.divS(q) for q in range(self.n))

    def S3(self):
        tot = sp.S.Zero
        for i in range(self.n):
            for j in range(self.n):
                for k in range(self.n):
                    tot += self.Sud[i, j] * self.Sud[j, k] * self.Sud[k, i]
        return tot

    def AAdphidphi(self):
        return self.Adphi ** 2

    def AAdchidchi(self):
        return self.Adchi ** 2


# ----------------------------------------------------------------------------------
# truncation helper
# ----------------------------------------------------------------------------------

EPS = sp.Symbol('__eps__')


def trunc_eps(expr, order, e=EPS):
    """Truncate `expr` at `order` in the bookkeeping parameter `e`.

    The perturbations MUST already carry explicit factors of `e` (built in at the
    ansatz), never substituted in afterwards: substituting into `Derivative` objects
    silently destroys terms (verified failure mode -- see git history).
    Polynomial fast path with a Taylor fallback for rational/sqrt dependence.
    """
    ex = expr
    try:
        exp = sp.expand(ex)
        pl = sp.Poly(exp, e)
        out = sp.S.Zero
        for (k,), c in pl.terms():
            if k <= order:
                out += c * e**k
        return sp.expand(out)
    except (sp.PolynomialError, sp.GeneratorsNeeded):
        pass
    out = sp.S.Zero
    term = ex.doit()
    fact = 1
    for k in range(order + 1):
        out += term.doit().subs(e, 0) * e**k / fact
        if k < order:
            term = sp.diff(term, e)
            fact *= (k + 1)
    return sp.expand(out)
