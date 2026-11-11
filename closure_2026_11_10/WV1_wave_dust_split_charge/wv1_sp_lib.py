"""WV1 solver library: radial Schrodinger-Poisson for Psi (cold dark energy as a wave field) in comoving coordinates,
COL1's setup otherwise (Hubble start at z = 10, KD1 cosmology per footing, baryon point mass softened over 1 kpc and
ramped on over 1 Gyr with a smoothstep, uniform baryon background).

Equation (Widrow-Kaiser / Schive form), u = x psi, |psi|^2 = comoving mass density, nu = hbar/m:
    i nu d_t u = -(nu^2 / 2 a^2) d_xx u + V u,
    d_x V = G dM(<x) / (a x^2) + G M_b(t) x / (a (x^2 + (eps/a)^2)^1.5) [+ a * law extra, bracket only],
    dM(<x) = 4 pi Int_0^x (|u|^2 - x'^2 rhobar) dx'.
Split step (kick-drift-kick). Drift: exact, discrete sine transform (type I) on w = u - x sqrt(rhobar) (the uniform
background is a zero mode of d_xx), Dirichlet w = 0 at x = 0 and at the outer boundary.

Units kpc, km/s, Msun; time unit kpc/(km/s) = 0.977792 Gyr. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import math, os, sys, signal, time, json
import numpy as np
from scipy.fft import dst, next_fast_len

HERE = os.path.dirname(os.path.abspath(__file__))
COL1 = os.path.abspath(os.path.join(HERE, "..", "..", "fable52_push", "COL1_clock_collapse"))
sys.path.insert(0, COL1)
import col1_lib as L          # read-only import: Cosmo, smoothstep, law_g, a0_of, G, TU

G = L.G
TU = L.TU
PI = math.pi


def dst1(v):
    return dst(v.real, type=1, norm="ortho", workers=1) + 1j * dst(v.imag, type=1, norm="ortho", workers=1)


class Run:
    def __init__(self, nu, logMb, footing, kd1, x_max, dx, law_bracket=False, eps=1.0, zi=10.0, ramp_gyr=1.0,
                 mass_on=True):
        s = kd1["footings"][footing]["setting"]
        self.cos = L.Cosmo(s["h"], s["omega_d"], s["omega_b"])
        self.nu, self.Mb, self.eps = nu, (10 ** logMb if mass_on else 0.0), eps
        self.a0 = L.a0_of(footing)
        self.law = law_bracket
        n1 = int(math.ceil(x_max / dx))                    # N + 1 cells; DST-I runs an FFT of length 2 (N + 1),
        n2 = next_fast_len(2 * n1)                         # so take 2 (N + 1) 5-smooth (dx shrinks slightly)
        while n2 % 2:
            n2 = next_fast_len(n2 + 1)
        self.N = n2 // 2 - 1
        self.dx = x_max / (self.N + 1)
        self.x = self.dx * np.arange(1, self.N + 1)
        self.xmax = self.dx * (self.N + 1)
        self.kk = PI * np.arange(1, self.N + 1) / self.xmax
        self.rbar = self.cos.nbar0                         # comoving Psi background density (Msun/kpc^3)
        self.bg = self.x * math.sqrt(self.rbar)
        self.u = self.bg.astype(np.complex128).copy()
        self.ti = self.cos.t_of_a(1.0 / (1.0 + zi))
        self.t = self.ti
        self.ramp = ramp_gyr / TU
        self.steps = 0

    # ------------------------------------------------------------------ fields
    def a(self, t=None):
        return self.cos.a_of_t(self.t if t is None else t)

    def Mb_t(self, t):
        return self.Mb * float(L.smoothstep((t - self.ti) / self.ramp))

    def dM(self, u=None):
        u = self.u if u is None else u
        f = 4 * PI * (np.abs(u) ** 2 - self.x ** 2 * self.rbar)
        c = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * self.dx)])
        return c + 0.5 * f[0] * self.x[0]            # f -> 0 at x = 0 (u = 0 there)

    def dVdx(self, t, u=None):
        a = self.a(t)
        x = self.x
        d = G * self.dM(u) / (a * x ** 2)
        Mb = self.Mb_t(t)
        if Mb > 0:
            r = a * x
            gpm = G * Mb * r / (r * r + self.eps ** 2) ** 1.5           # physical inward accel of the point mass
            d = d + a * gpm
            if self.law:
                d = d + a * (L.law_g(gpm, self.a0) - gpm)
        return d

    def V(self, t, u=None):
        """Gauge V(x_max) = 0: a constant offset is a global phase, and with V = 0 at the boundary the background
        u = x sqrt(rhobar) stays in phase there, as the Dirichlet condition w(x_max) = 0 requires."""
        d = self.dVdx(t, u)
        c = np.concatenate([[0.0], np.cumsum(0.5 * (d[1:] + d[:-1]) * self.dx)])
        return -(c[-1] - c) - d[-1] * self.dx, d

    # ------------------------------------------------------------------ stepping
    def drift(self, dt):
        am = self.a(self.t + 0.5 * dt)
        w = self.u - self.bg
        W = dst1(w)
        W *= np.exp(-1j * self.nu * self.kk ** 2 * dt / (2 * am * am))
        self.u = dst1(W) + self.bg

    def kick(self, V, h):
        self.u *= np.exp(-1j * V * (h / self.nu))

    def choose_dt(self, d, dt_max, c_dyn=0.02, c_alias=0.1):
        a = self.a()
        g = np.abs(d) / a                                   # physical accel
        gmax = max(float(g.max()), 1e-30)
        dt1 = c_dyn * math.sqrt(self.eps / gmax)
        dt2 = c_alias * (PI / self.dx) * self.nu / max(float(np.abs(d).max()), 1e-30)
        return min(dt1, dt2, dt_max)

    def step(self, dt, V0):
        self.kick(V0, 0.5 * dt)
        self.drift(dt)
        self.t += dt
        V1, d1 = self.V(self.t)
        self.kick(V1, 0.5 * dt)
        self.steps += 1
        return V1, d1

    # ------------------------------------------------------------------ diagnostics (physical units)
    def diag(self, footing_a0=None):
        a = self.a()
        H = self.cos.H_of_a(a)
        u = self.u
        x, dx = self.x, self.dx
        au = np.abs(u)
        r = a * x
        rho = au ** 2 / x ** 2 / a ** 3                      # physical Psi density
        up = np.gradient(u, dx)
        with np.errstate(divide="ignore", invalid="ignore"):
            dth = np.imag(np.conj(u) * up) / np.maximum(au ** 2, 1e-300)
        vphys = H * r + (self.nu / a) * dth
        # total physical inward gravity: background (Psi + baryons) + point mass (+ law) + perturbation
        cos = self.cos
        Mbg = (4 * PI / 3) * (cos.nbar0 + cos.rhob0) * r ** 3 / a ** 3
        gin = G * (Mbg + self.dM()) / r ** 2 - cos.OL * cos.H0 ** 2 * r
        Mb = self.Mb_t(self.t)
        gpm = G * Mb * r / (r * r + self.eps ** 2) ** 1.5 if Mb > 0 else 0 * r
        gin = gin + gpm
        if self.law and Mb > 0:
            gin = gin + (L.law_g(gpm, self.a0) - gpm)
        # frame proper acceleration A = -d_r Q_qu, Q_qu = -(nu^2/2a^2) d_xx|u| / |u|
        with np.errstate(divide="ignore", invalid="ignore"):
            q = np.gradient(np.gradient(au, dx), dx) / np.maximum(au, 1e-300)
        Q = -(self.nu ** 2 / (2 * a * a)) * q
        A = -np.gradient(Q, dx) / a
        return dict(a=a, z=1 / a - 1, t=self.t, r=r, rho=rho, v=vphys, gin=gin, A=A, au=au)
