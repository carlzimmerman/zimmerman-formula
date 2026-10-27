"""forest3d: framework-native 3D Lyman-alpha forest mock (P1D4).

Native linear power (P1D1 background) -> fixed-amplitude Gaussian field in a periodic box -> pressure filter ->
lognormal baryons (+ optional M6 patches, compensated) -> FGPA tau in real space -> shift to redshift space by the
linear Kaiser displacement f*psi_z (same Gaussian modes) -> thermal Gaussian broadening along the line of sight ->
flux at fixed mean -> 1D flux power along z for a lattice of skewers.

kappa = 1/2 FITTED; cold dark energy = gravitating w ~ 0 field component, never a particle; not theory closed.
"""
import math
import numpy as np
import scipy.fft as sfft
from scipy.integrate import quad

trapz = getattr(np, "trapezoid", None) or np.trapz
W = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3


class Background:
    def __init__(self, OM=0.2976016, h=0.6856427, wb=0.0223081, ns=0.965, s8=0.827959):
        OB = wb / h ** 2
        self.OM, self.OB, self.h, self.ns, self.s8, self.OL = OM, OB, h, ns, s8, 1 - OM
        self.RRAT = (OM - OB) / OB
        Gam = OM * h * np.exp(-OB * (1.0 + np.sqrt(2 * h) / OM))
        self.Tk = lambda kk: (np.log(1 + 2.34 * kk / Gam) / (2.34 * kk / Gam) * (1 + 3.89 * kk / Gam + (16.1 * kk / Gam) ** 2
                              + (5.46 * kk / Gam) ** 3 + (6.71 * kk / Gam) ** 4) ** -0.25)
        kf = np.logspace(-4, 3, 4000)
        shape = kf ** (3 + ns) * self.Tk(kf) ** 2
        self.NORM = s8 ** 2 / trapz(shape * W(kf * 8.0) ** 2, np.log(kf))
        self.D0 = self._D(1.0)

    def P0(self, k):
        k = np.asarray(k, float)
        out = np.zeros_like(k)
        m = k > 0
        out[m] = 2 * math.pi ** 2 * self.NORM * k[m] ** (3 + self.ns) * self.Tk(k[m]) ** 2 / k[m] ** 3
        return out

    def Ez(self, z):
        return math.sqrt(self.OM * (1 + z) ** 3 + self.OL)

    def _D(self, a):
        Ea = lambda x: math.sqrt(self.OM * x ** -3 + self.OL)
        return 2.5 * self.OM * Ea(a) * quad(lambda x: 1.0 / (x * Ea(x)) ** 3, 0, a, epsabs=0, epsrel=1e-12, limit=400)[0]

    def Dz(self, z):
        return self._D(1 / (1 + z)) / self.D0

    def fz(self, z, eps=1e-4):
        a = 1 / (1 + z)
        return (math.log(self._D(a * (1 + eps))) - math.log(self._D(a * (1 - eps)))) / (math.log(1 + eps) - math.log(1 - eps))

    def cz(self, z):
        """km/s per comoving Mpc/h along the line of sight."""
        return 100.0 * self.Ez(z) / (1 + z)


class Box:
    """Periodic box; fixed-amplitude modes with seed-fixed phases; float32 throughout to stay < 1 GB."""

    def __init__(self, N=256, L=64.0, seed=0, skip=2):
        self.N, self.L, self.dx = N, L, L / N
        k1 = 2 * math.pi * np.fft.fftfreq(N, self.dx).astype(np.float32)
        kz = 2 * math.pi * np.fft.rfftfreq(N, self.dx).astype(np.float32)
        self.kx, self.ky, self.kz = k1[:, None, None], k1[None, :, None], kz[None, None, :]
        self.k2 = (self.kx ** 2 + self.ky ** 2 + self.kz ** 2).astype(np.float32)
        self.k2[0, 0, 0] = 1.0
        rng = np.random.default_rng(seed)
        ph = rng.random((N, N, N // 2 + 1), dtype=np.float32)
        self.phase = np.exp(2j * np.pi * ph).astype(np.complex64)
        del ph
        self.phase[0, 0, 0] = 0
        self.skip = skip
        self.kf = 2 * math.pi / L
        self.kpar = (2 * math.pi * np.fft.rfftfreq(N, self.dx)).astype(np.float64)

    def _powgrid(self, bg, z, RJ):
        """sqrt(P(k) D^2 / V) N^3 exp(-k^2 RJ^2 / 2) on the rfft grid, float32 (P interpolated in log k)."""
        kk = np.logspace(math.log10(self.kf * 0.5), math.log10(math.sqrt(3) * math.pi / self.dx * 1.01), 4000)
        lp = np.log(bg.P0(kk) * bg.Dz(z) ** 2 / self.L ** 3)
        k = np.sqrt(self.k2)
        out = np.exp(0.5 * np.interp(np.log(k), np.log(kk), lp).astype(np.float32)) * np.float32(self.N ** 3)
        out *= np.exp(np.float32(-0.5 * RJ ** 2) * self.k2)
        out[0, 0, 0] = 0
        return out

    def gaussian(self, bg, z, RJ):
        """Filtered Gaussian density and LOS displacement psi_z (comoving Mpc/h), on the skewer sub-lattice."""
        dk = self._powgrid(bg, z, RJ).astype(np.complex64)
        dk *= self.phase
        delta = sfft.irfftn(dk, s=(self.N,) * 3, workers=1)
        var = float(delta.var(dtype=np.float64))
        s = self.skip
        dsub = delta[::s, ::s, :].copy(); del delta
        dk *= (1j * self.kz / self.k2).astype(np.complex64)
        psi = sfft.irfftn(dk, s=(self.N,) * 3, workers=1)
        del dk
        psub = psi[::s, ::s, :].copy(); del psi
        return dsub, psub, var

    def patches(self, RL, fV, dbi, mu, RJ, seed=1, seed_extra=2):
        """Compensated M6 patches (stratified tags) smoothed by RJ; returns multiplicative baryon factor on the sub-lattice."""
        if mu <= 0:
            return None
        N = self.N
        Vp = 4 * math.pi * RL ** 3 / 3
        N1 = int(round(fV * self.L ** 3 / Vp))
        r1 = np.random.default_rng(seed)
        cen = r1.random((N1, 3)) * self.L
        tags = (r1.permutation(N1) + 0.5) / N1
        cen = cen[tags <= mu]
        if mu > 1:
            r2 = np.random.default_rng(seed_extra)
            cen = np.vstack([cen, r2.random((int(round((mu - 1) * N1)), 3)) * self.L])
        I = np.zeros((N, N, N), np.float32)
        rc = int(math.ceil(RL / self.dx)) + 1
        off = np.arange(-rc, rc + 1)
        OX, OY, OZ = np.meshgrid(off, off, off, indexing="ij")
        for c in cen:
            i0 = np.floor(c / self.dx).astype(int)
            gx, gy, gz = i0[0] + OX, i0[1] + OY, i0[2] + OZ
            d2 = ((gx + 0.5) * self.dx - c[0]) ** 2 + ((gy + 0.5) * self.dx - c[1]) ** 2 + ((gz + 0.5) * self.dx - c[2]) ** 2
            m = d2 <= RL ** 2
            I[gx[m] % N, gy[m] % N, gz[m] % N] = 1.0
        fv_eff = float(I.mean(dtype=np.float64))
        G = sfft.rfftn(I, workers=1); del I
        G *= np.exp(np.float32(-0.5 * RJ ** 2) * self.k2)
        Is = sfft.irfftn(G, s=(N,) * 3, workers=1); del G
        Is = np.clip(Is, 0, 1)
        s = self.skip
        Is = Is[::s, ::s, :]
        return (1 + dbi * Is - fv_eff * dbi * (1 - Is) / (1 - fv_eff)).astype(np.float32), fv_eff


def tau_redshift(Delta, psi, f, gam, dx):
    """FGPA tau_real = Delta^beta (unit amplitude), shifted to redshift space by f*psi (CIC along the last axis)."""
    beta = 2 - 0.7 * (gam - 1)
    t = np.power(np.clip(Delta, 0, None), beta, dtype=np.float32)
    nsk, N = t.shape[0] * t.shape[1], t.shape[2]
    pos = (np.arange(N, dtype=np.float32)[None, None, :] + f * psi / dx) % N
    i0 = np.floor(pos).astype(np.int64); w1 = (pos - i0).astype(np.float32); i1 = (i0 + 1) % N
    base = (np.arange(nsk, dtype=np.int64) * N).reshape(t.shape[0], t.shape[1], 1)
    out = np.bincount((base + i0).ravel(), weights=(t * (1 - w1)).ravel(), minlength=nsk * N)
    out += np.bincount((base + i1).ravel(), weights=(t * w1).ravel(), minlength=nsk * N)
    return out.reshape(t.shape).astype(np.float32)


def flux_p1d(tau_rs, b_kms, Fbar, cz, dx, L):
    """Thermal broadening (constant b at mean density), mean flux Fbar, 1D power in km/s at the box LOS modes."""
    N = tau_rs.shape[2]
    kpar = 2 * math.pi * np.fft.rfftfreq(N, dx)
    sx = (b_kms / math.sqrt(2)) / cz
    t = np.fft.irfft(np.fft.rfft(tau_rs, axis=2) * np.exp(-0.5 * kpar ** 2 * sx ** 2)[None, None, :].astype(np.float32), n=N, axis=2)
    t = np.clip(t, 0, None).astype(np.float32)
    lA = math.log(max(-math.log(Fbar) / max(float(t.mean()), 1e-30), 1e-30))
    for _ in range(50):
        A = math.exp(lA); e = np.exp(-A * t)
        fm = float(e.mean()) - Fbar; d = -float((A * t * e).mean())
        if d == 0 or abs(fm) < 1e-9: break
        lA -= max(min(fm / d, 2.0), -2.0)
    F = np.exp(-math.exp(lA) * t)
    dF = F / F.mean() - 1
    Pk = (np.abs(dx * np.fft.rfft(dF, axis=2)) ** 2 / L).mean(axis=(0, 1)) * cz
    return kpar / cz, Pk, float(F.mean()), math.exp(lA)


def p1d_analytic(bg, z, RJ, kpar):
    """1D projection of the filtered linear 3D power (P1D1's p1d), Mpc/h."""
    KG = np.logspace(-4, math.log10(200.0), 60001); LNK = np.log(KG)
    f = KG ** 2 * bg.P0(KG) * bg.Dz(z) ** 2 * np.exp(-KG ** 2 * RJ ** 2)
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(LNK))])
    return (cum[-1] - np.interp(np.log(np.maximum(kpar, 1e-6)), LNK, cum)) / (2 * math.pi)
