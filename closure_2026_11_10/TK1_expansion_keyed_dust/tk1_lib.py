"""TK1 library: M_2(theta), the clock's energy density at fixed charge, the flat background and the closed top-hat patch.
Units: c = 1, H0 = 1 (lengths in c/H0). Densities as x = (8 pi G/3) rho / H0^2, so K n = 1.5 Omega_n.
Criteria 98f2ab2b6e. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import math
import mpmath as mp

mp.mp.dps = 30
C_KMS = 299792.458
H0_KMS = 67.4
H0_PER_MPC = H0_KMS / C_KMS                     # 2.2482e-4 per Mpc
GYR_PER_HUBBLE = 977.792221 / H0_KMS            # 1/H0 in Gyr
import json, os
_KD1 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "../../closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json")))["footings"]
FOOT = {}
for _f in ("canonical", "alt"):
    _s = _KD1[_f]["setting"]
    _I0 = _s["I0_Mpc-2"]
    _Od = _I0 / (3 * H0_PER_MPC**2)
    _Ob = _s["omega_b"] / 0.674**2
    _Or = _KD1[_f]["B1"]["Omega_r"]
    FOOT[_f] = dict(I0=_I0, Od=_Od, Ob=_Ob, Or=_Or, OL=1 - _Od - _Ob - _Or,
                    mu_B1a=_KD1[_f]["B1"]["mu_B1a"], mu_J=_KD1[_f]["G9a_jeans"]["mu_J"])
I0 = FOOT["canonical"]["I0"]
OMEGA_D = FOOT["canonical"]["Od"]
OMEGA_B = FOOT["canonical"]["Ob"]
OMEGA_R = FOOT["canonical"]["Or"]
OMEGA_L = FOOT["canonical"]["OL"]
MU_J = 2.512e4                                   # per Mpc, KD1 G9a

PRIMARY = dict(mu0=3e4, th0=0.1, p=2, Mf=1e-3)   # mu0, Mf per Mpc; th0 in H0
BRACKETS = {"theta0_9H0": dict(mu0=3e4, th0=9.0, p=2, Mf=1e-3),
            "p4": dict(mu0=3e4, th0=0.1, p=4, Mf=1e-3),
            "floor_off": dict(mu0=3e4, th0=0.1, p=2, Mf=0.0),
            "MU2_key_off": dict(mu0=3e4, th0=0.1, p=0, Mf=0.0)}   # p = 0: M_2 = mu0^2 constant


class Key:
    """M_2(theta) = mu0^2 s^p + Mf^2, s = theta^2/(theta^2 + th0^2), in H0 units."""
    def __init__(self, mu0, th0, p, Mf, drop_thFth=False):
        self.m0 = mp.mpf(mu0) / H0_PER_MPC
        self.mf = mp.mpf(Mf) / H0_PER_MPC
        self.th0 = mp.mpf(th0)
        self.p = p
        self.drop = drop_thFth

    def M2(self, th):
        th = mp.mpf(th)
        if self.p == 0:
            return self.m0**2 + self.mf**2
        s = th**2 / (th**2 + self.th0**2)
        return self.m0**2 * s**self.p + self.mf**2

    def dM2(self, th, n=1):
        return mp.diff(self.M2, th, n)

    def thM2p_over_M2(self, th):
        """theta M_2'/M_2, analytic: mu0^2 p s^p * 2 th0^2/(th^2+th0^2) / M_2."""
        if self.p == 0:
            return mp.mpf(0)
        th = mp.mpf(th)
        s = th**2 / (th**2 + self.th0**2)
        return self.m0**2 * self.p * s**self.p * 2 * self.th0**2 / (th**2 + self.th0**2) / self.M2(th)

    def M2pp(self, th):
        """analytic second derivative of mu0^2 s^p."""
        if self.p == 0:
            return mp.mpf(0)
        th = mp.mpf(th); t0 = self.th0; p = self.p
        s = th**2 / (th**2 + t0**2)
        ds = 2 * th * t0**2 / (th**2 + t0**2)**2
        dds = 2 * t0**2 * (t0**2 - 3 * th**2) / (th**2 + t0**2)**3
        return self.m0**2 * (p * (p - 1) * s**(p - 2) * ds**2 + p * s**(p - 1) * dds) if p >= 2 else self.m0**2 * dds

    def xK(self, th, Om_n):
        """(8 pi G/3) rho_K / H0^2 at fixed charge: Om_n + 0.75 Om_n^2 / M_2 (1 + theta M_2'/M_2)."""
        M2 = self.M2(th)
        fac = 1 if self.drop else 1 + self.thM2p_over_M2(th)
        return Om_n + mp.mpf(0.75) * Om_n**2 / M2 * fac

    def Qm1(self, th, Om_n):
        return mp.mpf(1.5) * Om_n / self.M2(th)

    def lam_eff(self, th, Om_n):
        return -self.M2pp(th) * self.Qm1(th, Om_n)**2


def H_root(key, rest, Om_n, Hhi=None):
    """LARGEST positive root of G(H) = H^2 - rest - xK(3H, Om_n) (the expanding branch, continuous from early times).
    G need not be monotone (floor on: the stiff part peaks near theta ~ theta_0 sqrt(M_f/mu_0)); scan down from Hhi in
    steps of 10^(1/16), then bisect in log H. Returns None if G > 0 down to H = 1e-30 (no expanding root)."""
    def G(H):
        return H**2 - rest - key.xK(3 * H, Om_n)
    hi = mp.mpf(Hhi or 1e8)
    hi = max(hi, 10 * mp.sqrt(abs(rest) + 3 * abs(Om_n) + 1))
    if G(hi) < 0:
        raise ValueError("no root below Hhi")
    step = mp.mpf(10)**(mp.mpf(1) / 16)
    lo = hi / step
    while G(lo) > 0:
        hi = lo
        lo = lo / step
        if lo < mp.mpf("1e-30"):
            return None
    for _ in range(200):
        mid = mp.sqrt(lo * hi)
        if G(mid) > 0:
            hi = mid
        else:
            lo = mid
        if hi / lo - 1 < mp.mpf("1e-32"):
            break
    return mp.sqrt(lo * hi)


def G_H(key, rest, Om_n, H):
    """dG/dH at the root (fold where it vanishes)."""
    f = lambda h: h**2 - rest - key.xK(3 * h, Om_n)
    return mp.diff(f, H)


def minisuper_D(key, a, H, Om_n, kc, Kc=mp.mpf(1.5)):
    """Clock-time minisuperspace principal determinant D = L_vv L_NN - L_vN^2 (v = adot), units H0 = 1, (2/3)K = 1.
    L = (3/(2K))(-a v^2/N + kc N a) + N a^3 M_2(theta) (1/N - 1)^2/(2K) + (terms linear in N, no v)."""
    Q = 1 + mp.mpf(1.5) * Om_n / key.M2(3 * H)
    N0 = 1 / Q
    v0 = N0 * a * H
    def Lf(N, v):
        th = 3 * v / (N * a)
        return 3 / (2 * Kc) * (-a * v**2 / N) + N * a**3 * key.M2(th) * (1 / N - 1)**2 / (2 * Kc)
    Lvv = mp.diff(Lf, (N0, v0), (0, 2))
    LNN = mp.diff(Lf, (N0, v0), (2, 0))
    LvN = mp.diff(Lf, (N0, v0), (1, 1))
    return Lvv * LNN - LvN**2, Lvv, LNN, LvN


def background_H(key, a, foot="canonical"):
    F = FOOT[foot]
    a = mp.mpf(a)
    Om_n = F["Od"] / a**3
    rest = F["Or"] / a**4 + F["Ob"] / a**3 + F["OL"]
    return H_root(key, rest, Om_n), Om_n
