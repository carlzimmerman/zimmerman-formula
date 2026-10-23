"""Exact (Galerkin) Fock-space evolution of normal-ordered polynomial Hamiltonians of the X1 action.

Generic sparse builder for the zero-momentum four-mode model Phi+ (0), Phi- (1), X+ (2), X- (3): normal-ordered
monomials applied exactly on a truncated occupation basis (states leaving the basis are dropped, exactly as in Codex's
quantum_fock_solver.Model). Units m_Phi = 1; cell volume V enters as V**(1 - n_fields/2) per vertex, as in Codex.
rwa=True keeps only monomials with Delta W = 0 (W = N_Phi + 2 N_X), the rotating-wave projection (AMENDMENT A1);
it is then evolved in the frame rotating with N_W and rotated back exactly.
"""
from collections import defaultdict
from itertools import product
import numpy as np
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import expm_multiply
from scipy.special import gammaln

G = .002168; LAM = .00881292; MX = 2*np.sqrt(1+.02**2)
WW = np.array([1, 1, 2, 2])


def w_basis(Wmax, nmax=None):
    """All (n0,n1,n2,n3) with n0+n1+2(n2+n3) <= Wmax (and n_i <= nmax_i if given)."""
    out = []
    for n2 in range(Wmax//2+1):
        for n3 in range((Wmax-2*n2)//2+1):
            r = Wmax-2*(n2+n3)
            n0, n1 = np.meshgrid(np.arange(r+1), np.arange(r+1), indexing='ij')
            m = (n0+n1) <= r
            blk = np.stack([n0[m], n1[m], np.full(m.sum(), n2), np.full(m.sum(), n3)], axis=1)
            out.append(blk)
    st = np.concatenate(out)
    if nmax is not None:
        st = st[np.all(st <= np.asarray(nmax), axis=1)]
    return st


class FockK0:
    def __init__(self, Wmax=None, nmax=None, volume=1., ecut=None, ncut=None, charge=None, g=G, lam=LAM, rwa=False,
                 states=None):
        self.E = np.array([1., 1., MX, MX]); self.Q = np.array([1, -1, 2, -2]); self.V = float(volume)
        self.g = g; self.lam = lam; self.rwa = rwa
        if states is None:
            if Wmax is None:
                nm = np.asarray(nmax)
                grids = np.meshgrid(*[np.arange(k+1) for k in nm], indexing='ij')
                st = np.stack([x.ravel() for x in grids], axis=1)
            else:
                st = w_basis(Wmax, nmax)
        else:
            st = np.asarray(states)
        keep = np.ones(len(st), bool)
        if ecut is not None: keep &= (st*self.E).sum(1) <= ecut+1e-9
        if ncut is not None: keep &= st.sum(1) <= ncut
        if charge is not None: keep &= st@self.Q == charge
        st = st[keep]
        self.nmax = st.max(axis=0)
        self.base = self.nmax+2
        self.mult = np.cumprod(np.r_[1, self.base[:-1]]).astype(np.int64)
        keys = st@self.mult; order = np.argsort(keys)
        self.states = st[order]; self.keys = keys[order]; self.dim = len(self.states)
        self.free = (self.states*self.E).sum(1); self.W = (self.states*WW).sum(1)
        sPhi = 1/np.sqrt(2*self.E[0]); sX = 1/np.sqrt(2*self.E[2])
        F = {'phi': [(0, False, sPhi), (1, True, sPhi)], 'phibar': [(0, True, sPhi), (1, False, sPhi)],
             'X': [(2, False, sX), (3, True, sX)], 'Xbar': [(2, True, sX), (3, False, sX)]}
        self.H0 = diags(self.free, format='csr')
        self.H3 = self.operator(self.vertex(F, [('Xbar', 'phi', 'phi'), ('X', 'phibar', 'phibar')]))
        self.H4 = self.operator(self.vertex(F, [('phibar', 'phibar', 'phi', 'phi')]))
        self.H = (self.H0+g*self.H3+lam*self.H4).tocsr()

    def vertex(self, F, words):
        terms = defaultdict(float)
        for word in words:
            for fac in product(*(F[w] for w in word)):
                cr = tuple(sorted(f[0] for f in fac if f[1])); an = tuple(sorted(f[0] for f in fac if not f[1]))
                if self.rwa and sum(WW[k] for k in cr) != sum(WW[k] for k in an):
                    continue
                terms[cr, an] += self.V**(1-len(word)/2)*np.prod([f[2] for f in fac])
        return terms

    def lookup(self, occ):
        ok = np.all((occ >= 0) & (occ <= self.nmax), axis=1)
        k = np.where(ok[:, None], occ, 0)@self.mult
        idx = np.clip(np.searchsorted(self.keys, k), 0, self.dim-1)
        ok &= self.keys[idx] == k
        return idx, ok

    def apply_monomial(self, cr, an, coef):
        occ = self.states.copy(); w = np.full(self.dim, coef, dtype=float)
        for k in an:
            w *= np.sqrt(np.maximum(occ[:, k], 0)); occ[:, k] -= 1
        for k in cr:
            w *= np.sqrt(np.maximum(occ[:, k]+1, 0)); occ[:, k] += 1
        idx, ok = self.lookup(occ); ok &= w != 0
        return idx[ok], np.nonzero(ok)[0], w[ok]

    def operator(self, terms):
        rows = [np.zeros(0, int)]; cols = [np.zeros(0, int)]; data = [np.zeros(0)]
        for (cr, an), c in terms.items():
            r, cl, w = self.apply_monomial(cr, an, c); rows.append(r); cols.append(cl); data.append(w)
        return coo_matrix((np.concatenate(data), (np.concatenate(rows), np.concatenate(cols))),
                          shape=(self.dim, self.dim)).tocsr()

    def annihilator(self, k):
        r, c, w = self.apply_monomial((), (k,), 1.)
        return coo_matrix((w, (r, c)), shape=(self.dim, self.dim)).tocsr()

    def coherent(self, gammas):
        gam = np.asarray(gammas, dtype=complex); logamp = np.zeros(self.dim, dtype=complex)
        for k in range(4):
            n = self.states[:, k]
            if gam[k] == 0:
                logamp += np.where(n == 0, 0., -np.inf)
            else:
                logamp += -abs(gam[k])**2/2+n*np.log(gam[k])-gammaln(n+1)/2
        psi = np.exp(logamp); norm = np.linalg.norm(psi)
        return psi/norm, float(1-norm**2)

    def evolve(self, psi0, T, num):
        """Generator over (t, psi_lab(t)) at num equally spaced times; never stores the history.
        Propagator: shifted Taylor series in sub-steps with |H - mu|_1 dt_sub <= 1, terms until < 1e-17
        (scipy's expm_multiply leaks ~80 MB per call in this environment)."""
        times = np.linspace(0, T, num); psi = psi0.astype(complex)
        Hr = (self.H-diags(self.W.astype(float))).tocsr() if self.rwa else self.H.tocsr()
        d = Hr.diagonal(); mu = 0.5*(d.max()+d.min())
        Hs = (Hr-diags(np.full(self.dim, mu))).tocsr()
        norm1 = abs(Hs).sum(axis=0).max()
        yield times[0], psi
        for k in range(1, num):
            dtk = times[k]-times[k-1]; nsub = max(1, int(np.ceil(norm1*dtk))); h = dtk/nsub
            for _ in range(nsub):
                term = psi.copy(); acc = psi.copy()
                for j in range(1, 60):
                    term = (-1j*h/j)*(Hs@term); acc += term
                    if np.linalg.norm(term) < 1e-17*np.linalg.norm(acc): break
                psi = acc*np.exp(-1j*mu*h)
            yield times[k], (psi*np.exp(-1j*self.W*times[k]) if self.rwa else psi)


def observables_exact(model, gen, driven):
    """gen yields (t, psi). Returns time series of the frozen observables."""
    S = model.states.astype(float); NX = S[:, 2]+S[:, 3]; NP = S[:, 0]+S[:, 1]
    dm = (2, 3) if driven == 'X' else (0, 1)
    A0, A1 = [model.annihilator(k) for k in dm]
    q = ((A0+A1.T+A0.T+A1)/np.sqrt(2)).tocsr()
    top = model.W >= model.W.max()-1
    rows = {k: [] for k in ('t', 'N', 'varX', 'varPhi', 'coh', 'skew', 'exkurt', 'edge_prob', 'norm', 'energy')}
    for t, h in gen:
        p = np.abs(h)**2; n = p@S
        rows['t'].append(t); rows['N'].append(n)
        rows['varX'].append(p@NX**2-(p@NX)**2); rows['varPhi'].append(p@NP**2-(p@NP)**2)
        m0 = np.vdot(h, A0@h); m1 = np.vdot(h, A1@h)
        rows['coh'].append((abs(m0)**2+abs(m1)**2)/max(n[dm[0]]+n[dm[1]], 1e-300))
        v1 = q@h; v2 = q@v1
        m1_, m2_, m3_, m4_ = np.vdot(h, v1).real, np.vdot(v1, v1).real, np.vdot(v1, v2).real, np.vdot(v2, v2).real
        k2 = m2_-m1_**2; k3 = m3_-3*m2_*m1_+2*m1_**3; k4 = m4_-4*m3_*m1_-3*m2_**2+12*m2_*m1_**2-6*m1_**4
        rows['skew'].append(k3/k2**1.5); rows['exkurt'].append(k4/k2**2)
        rows['edge_prob'].append(p[top].sum()); rows['norm'].append(p.sum()); rows['energy'].append(np.vdot(h, model.H@h).real)
    return {k: np.array(v) for k, v in rows.items()}
