"""Truncated Wigner (TW) for Codex's reduced Hamiltonians: classical evolution of the sampled Wigner function with the
exact Weyl symbol of each quantum Hamiltonian.

 TW4Full : zero-momentum four-mode model, full normal-ordered H (Weyl counterterm -4 c|phi|^2, c = 1/2) or the
           un-normal-ordered one-cell wavefunction potential (c = 0). Strang splitting, exact harmonic part, kick.
 TW4RWA  : the W-conserving projection (AMENDMENT A1), RK4 in the frame rotating with N_W.
 TW12    : Codex's 12-oscillator model (momenta -1,0,1 of Phi+-, X+-), Galerkin field on an 8-point dealiased grid.
Units m_Phi = 1. Mode amplitudes alpha: <|alpha|^2>_W = n + 1/2. mutate=True drops the -1/2 (the MUTATE of the criteria).
"""
import numpy as np

G = .002168; LAM = .00881292; MX = 2*np.sqrt(1+.02**2)


def sample_modes(gammas, N, rng, signed=()):
    """alpha_i = gamma_i + vacuum Wigner noise (variance 1/4 per quadrature). signed: modes in Fock |1> (weights 4|a|^2-1)."""
    gam = np.asarray(gammas, dtype=complex)
    a = gam[None, :]+(rng.standard_normal((N, len(gam)))+1j*rng.standard_normal((N, len(gam))))/2
    w = np.ones(N)
    for k in signed:
        w *= 4*np.abs(a[:, k]-gam[k])**2-1
    return a, w


def occ(alpha, mutate=False):
    return np.abs(alpha)**2-(0. if mutate else .5)


def tw_observables(alphas, w, driven, mutate=False):
    """alphas: (T, N, 4). Weighted TW estimates of the same observables as x1_fock.observables_exact."""
    W = w/np.sum(w)
    def E(x): return np.tensordot(x, W, axes=([1], [0]))
    nn = occ(alphas, mutate)
    N = np.stack([E(nn[:, :, k]) for k in range(4)], axis=1)
    def var(i, j):
        A = alphas[:, :, i]; B = alphas[:, :, j]
        s2 = (np.abs(A)**4-np.abs(A)**2)+(np.abs(B)**4-np.abs(B)**2)+2*(np.abs(A)**2-.5)*(np.abs(B)**2-.5)
        tot = nn[:, :, i]+nn[:, :, j]
        return E(s2)-E(tot)**2
    out = dict(N=N, varPhi=var(0, 1), varX=var(2, 3))
    dm = (2, 3) if driven == 'X' else (0, 1)
    m0 = E(alphas[:, :, dm[0]]); m1 = E(alphas[:, :, dm[1]])
    out['coh'] = (np.abs(m0)**2+np.abs(m1)**2)/np.maximum(N[:, dm[0]]+N[:, dm[1]], 1e-300)
    q = np.sqrt(2)*np.real(alphas[:, :, dm[0]]+np.conj(alphas[:, :, dm[1]]))
    mm = [E(q**k) for k in (1, 2, 3, 4)]
    m1_, m2_, m3_, m4_ = mm
    k2 = m2_-m1_**2; k3 = m3_-3*m2_*m1_+2*m1_**3; k4 = m4_-4*m3_*m1_-3*m2_**2+12*m2_*m1_**2-6*m1_**4
    out['skew'] = k3/k2**1.5; out['exkurt'] = k4/k2**2
    return out


class TW4Full:
    """Field variables: phi=(a+b*)/sqrt(2w), P=pi*= -i sqrt(w/2)(a-b*); same for X with w=M."""
    def __init__(self, volume=1., c=.5, g=G, lam=LAM):
        self.V = volume; self.c = c; self.g = g; self.lam = lam; self.w = np.array([1., MX])

    def to_fields(self, a):
        out = []
        for s, (i, j) in enumerate(((0, 1), (2, 3))):
            w = self.w[s]
            out += [(a[:, i]+np.conj(a[:, j]))/np.sqrt(2*w), -1j*np.sqrt(w/2)*(a[:, i]-np.conj(a[:, j]))]
        return out

    def to_modes(self, f):
        phi, P, x, Px = f; res = []
        for (q, p), w in (((phi, P), self.w[0]), ((x, Px), self.w[1])):
            res += [(w*q+1j*p)/np.sqrt(2*w), np.conj((w*q-1j*p)/np.sqrt(2*w))]
        return np.stack(res, axis=1)

    def force(self, phi, x):
        gV = self.g/np.sqrt(self.V); lV = self.lam/self.V
        Fphi = 2*gV*x*np.conj(phi)+lV*(2*np.abs(phi)**2*phi-4*self.c*phi)
        Fx = gV*phi*phi
        return Fphi, Fx

    def energy(self, f):
        phi, P, x, Px = f; gV = self.g/np.sqrt(self.V); lV = self.lam/self.V
        return (np.abs(P)**2+np.abs(phi)**2+np.abs(Px)**2+MX**2*np.abs(x)**2+2*gV*np.real(np.conj(x)*phi*phi)
                + lV*(np.abs(phi)**4-4*self.c*np.abs(phi)**2))

    def run(self, a0, T, num, dt):
        phi, P, x, Px = self.to_fields(a0)
        out_t = np.linspace(0, T, num); every = round((T/(num-1))/dt); assert abs(every*dt-T/(num-1)) < 1e-9
        cw = [np.cos(w*dt/2) for w in self.w]; sw = [np.sin(w*dt/2) for w in self.w]
        def rot(q, p, s):
            w = self.w[s]; return q*cw[s]+p/w*sw[s], p*cw[s]-w*q*sw[s]
        hist = [self.to_modes((phi, P, x, Px))]; E0 = self.energy((phi, P, x, Px))
        for k in range(1, num):
            for _ in range(every):
                phi, P = rot(phi, P, 0); x, Px = rot(x, Px, 1)
                Fp, Fx = self.force(phi, x); P = P-dt*Fp; Px = Px-dt*Fx
                phi, P = rot(phi, P, 0); x, Px = rot(x, Px, 1)
            hist.append(self.to_modes((phi, P, x, Px)))
        drift = float(np.max(np.abs(self.energy((phi, P, x, Px))-E0)/np.maximum(np.abs(E0), 1)))
        return out_t, np.array(hist), drift


class TW4RWA:
    def __init__(self, volume=1., g=G, lam=LAM):
        self.V = volume; self.g = g; self.lam = lam
        self.kc = g/np.sqrt(volume)*(1/np.sqrt(2*MX))*.5; self.kq = lam/volume*.25
        self.det = np.array([0., 0., MX-2, MX-2])

    def rhs(self, a):
        A = np.abs(a[:, 0])**2; B = np.abs(a[:, 1])**2
        d = np.empty_like(a)
        d[:, 0] = self.det[0]*a[:, 0]+self.kc*2*np.conj(a[:, 0])*a[:, 2]+self.kq*(2*(A+B)+2*B-4)*a[:, 0]
        d[:, 1] = self.det[1]*a[:, 1]+self.kc*2*np.conj(a[:, 1])*a[:, 3]+self.kq*(2*(A+B)+2*A-4)*a[:, 1]
        d[:, 2] = self.det[2]*a[:, 2]+self.kc*a[:, 0]**2
        d[:, 3] = self.det[3]*a[:, 3]+self.kc*a[:, 1]**2
        return -1j*d

    def run(self, a0, T, num, dt):
        a = a0.copy(); every = round((T/(num-1))/dt); out_t = np.linspace(0, T, num)
        ww = np.array([1, 1, 2, 2]); hist = [a.copy()]
        for k in range(1, num):
            for _ in range(every):
                k1 = self.rhs(a); k2 = self.rhs(a+dt/2*k1); k3 = self.rhs(a+dt/2*k2); k4 = self.rhs(a+dt*k3)
                a = a+dt/6*(k1+2*k2+2*k3+k4)
            hist.append(a*np.exp(-1j*ww*out_t[k])[None, :])
        return out_t, np.array(hist), 0.


class TWCell:
    """Codex's one-cell wavefunction model: H = sum p^2/2 + U(f,h,x,y), volume 1, NOT normal ordered (c = 0)."""
    def __init__(self, g=G, lam=LAM):
        self.g = g; self.lam = lam; self.w = np.array([1., 1., MX, MX])

    def force(self, q):
        f, h, x, y = q; r = f*f+h*h; c = self.g/np.sqrt(2)
        return np.array([self.lam*r*f+c*(2*x*f+2*y*h), self.lam*r*h+c*(-2*x*h+2*y*f), c*(f*f-h*h), c*2*f*h])

    def run(self, q, p, T, num, dt):
        out_t = np.linspace(0, T, num); every = round((T/(num-1))/dt); w = self.w[:, None]
        c = np.cos(w*dt/2); s = np.sin(w*dt/2)
        hq = [q.copy()]; hp = [p.copy()]
        for k in range(1, num):
            for _ in range(every):
                q, p = q*c+p/w*s, p*c-w*q*s
                p = p-dt*self.force(q)
                q, p = q*c+p/w*s, p*c-w*q*s
            hq.append(q.copy()); hp.append(p.copy())
        return out_t, np.array(hq), np.array(hp)


class TW12:
    """Codex's 12-mode Galerkin model. Mode order as Codex: Phi+ k=-1,0,1 (0-2), Phi- (3-5), X+ (6-8), X- (9-11)."""
    def __init__(self, volume=100., p=None, g=G, lam=LAM, ng=8):
        self.V = volume; self.g = g; self.lam = lam; self.ng = ng
        self.p = np.sqrt(((MX+2)/2)**2-1) if p is None else p
        self.k = np.array([-1, 0, 1])
        self.Ep = np.sqrt(1+(self.p*self.k)**2); self.EX = np.sqrt(MX**2+(self.p*self.k)**2)
        self.c = np.sum(1/(2*self.Ep))           # Weyl contraction of normal ordering, all three Phi momenta
        self.idx = self.k % ng

    def to_fields(self, a):
        """phi_k = (a_k + b*_{-k})/sqrt(2E_k), P_k = -i sqrt(E_k/2)(a_k - b*_{-k}); same for X."""
        out = []
        for (o1, o2), E in (((0, 3), self.Ep), ((6, 9), self.EX)):
            A = a[:, o1:o1+3]; Bm = np.conj(a[:, o2:o2+3][:, ::-1])
            out += [(A+Bm)/np.sqrt(2*E), -1j*np.sqrt(E/2)*(A-Bm)]
        return out

    def to_modes(self, f):
        phi, P, x, Px = f; res = np.empty((phi.shape[0], 12), dtype=complex)
        for (q, p), E, (o1, o2) in (((phi, P), self.Ep, (0, 3)), ((x, Px), self.EX, (6, 9))):
            A = (E*q+1j*p)/np.sqrt(2*E); Bm = (E*q-1j*p)/np.sqrt(2*E)
            res[:, o1:o1+3] = A; res[:, o2:o2+3] = np.conj(Bm)[:, ::-1]
        return res

    def grid(self, m):
        full = np.zeros((m.shape[0], self.ng), dtype=complex); full[:, self.idx] = m
        return np.fft.ifft(full, axis=1)*self.ng

    def proj(self, y):
        return np.fft.fft(y, axis=1)[:, self.idx]/self.ng

    def force(self, phi, x):
        Pg = self.grid(phi); Xg = self.grid(x); gV = self.g/np.sqrt(self.V); lV = self.lam/self.V
        Fp = 2*gV*Xg*np.conj(Pg)+lV*(2*np.abs(Pg)**2*Pg-4*self.c*Pg)
        Fx = gV*Pg*Pg
        return self.proj(Fp), self.proj(Fx)

    def run(self, a0, T, num, dt):
        phi, P, x, Px = self.to_fields(a0)
        out_t = np.linspace(0, T, num); every = round((T/(num-1))/dt)
        cP, sP = np.cos(self.Ep*dt/2), np.sin(self.Ep*dt/2); cX, sX = np.cos(self.EX*dt/2), np.sin(self.EX*dt/2)
        def rot(q, p, E, c, s): return q*c+p/E*s, p*c-E*q*s
        hist = [self.to_modes((phi, P, x, Px))]
        for k in range(1, num):
            for _ in range(every):
                phi, P = rot(phi, P, self.Ep, cP, sP); x, Px = rot(x, Px, self.EX, cX, sX)
                Fp, Fx = self.force(phi, x); P = P-dt*Fp; Px = Px-dt*Fx
                phi, P = rot(phi, P, self.Ep, cP, sP); x, Px = rot(x, Px, self.EX, cX, sX)
            hist.append(self.to_modes((phi, P, x, Px)))
        return out_t, np.array(hist)
