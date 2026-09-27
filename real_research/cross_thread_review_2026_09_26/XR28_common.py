#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR28 shared machinery (imported by XR28_controls.py, XR28_outskirts_L.py and XR28_hot_phase.py; runs nothing heavy on
import).  Units: Mpc, km/s, Msun; time in Mpc/(km/s).  Every formula is the chain's own (FP6/FP9's band-passed phantom and
yield, FP0's footings, FK1/FP10's kick and budget, XR19's web conversion) or a published LCDM ingredient (EH98 transfer,
Correa et al. 2015a MAH, the DK14 profile the observers fit), each stated where it is used.  No constant is added.

  * THE CHAIN'S COSMOLOGY (FP6/FP9): h = 0.6736, omega_b = 0.02237, omega_c = 0.1200, T_CMB = 2.7255, N_eff = 3.046,
    n_s = 0.965, sigma_8 = 0.811 (FP6's EH98 no-wiggle shape), flat, radiation included.
  * THE BAND-PASSED PHANTOM (FP6's phantom(), FP9's yield hook), generalised from a point mass to any spherical baryon
    excess: g_bp = G [dM_b(<r) - S_L dM_b(<r)]/r^2 (Gaussian-smoothed excess subtracted, sigma = L per axis); the MOND field
    a0 x(y - y_th) along g_bp (x = (nu_P2 - 1) y, or (nu_mono - 1) y); M_raw = sign(g_bp) a0 x r^2/G; the variation's output
    filter M_ph = M_raw - S_L M_raw (FP6 G6e: Gauss compensation).  Baryons and light feel -G M_ph/r^2 (psi = Phi, FP7);
    the dark state is kernel-invisible and feels Newtonian gravity only (L353, FP4, FP10).
  * THE SEPARATOR'S LENGTH: L(a) = L0 [Omega_L(a)/Omega_L(1)]^(n/2), n = 2 (FP9's H_Y running; H_S's n_eff = 2.06, FP13);
    H_Y's yield y_th(a) = y_Lambda Omega_L(a)^(-4), y_Lambda = 1e-6 Omega_L(z = 0.25)^4 (FP9's headline).
  * THE SHELL MODEL: spherical Lagrangian shells, comoving x and p = a^2 dx/dt, KDK leapfrog in ln a,
        dp/dt = a [ -G M(<r) r/(r^2 + eps^2)^(3/2) + (4 pi/3) G rho_m(a) r + j^2/r^3 + g_ph (baryons only) ],
    Zel'dovich growing-mode ICs; the Lagrangian profile is Correa et al. (2015a) inside the cluster's Lagrangian radius and the
    constrained mean (+ t x its conditional scatter) outside (the form FP16 uses, re-implemented here on EH98); each shell gets
    j = j_f r v_c at its own turnaround (j_f uniform in 0.15-0.35, FP16's choice).
  * THE DARK SECTOR'S PHASES (FK1/FP10/XR19): each shell's dark mass is split into sub-particles that co-move with it until
    their conversion event, then get an isotropic kick of speed v (Gauss-Legendre nodes in mu = cos theta): escaped from
    sub-haloes (FP10's bias-weighted budget F_b(z), v_inf = v_k), converted in the web (XR19's nominal f_web(z)), converted at
    the host's front (0.95 r200c, FP10 A6) or at turnaround (XR19 I1), or kept cold (bound in sub-haloes; unconverted).
  * THE OBSERVERS' INFERENCE: the stacked model profile is projected (uniform-shell kernel, as FP18; checked against Wright &
    Brainerd's NFW) and fitted with the DK14 form and the priors of Shin et al. (2021) / Chang et al. (2018); r_sp and
    gamma(r_sp) are read off the fitted 3D profile exactly as the observers do.
"""
import os, math, json, hashlib, time
import numpy as np
from scipy.special import erf
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

# ------------------------------------------------------------------------------------------------ units and footings
GMPC = 4.30091727e-9                        # G [Mpc (km/s)^2 / Msun]
MPC_M = 3.0856775814913673e22
SI_ACC = 1e6 / MPC_M                        # (km/s)^2/Mpc -> m/s^2
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}                    # FP0's footings
A0 = {k_: v_ / SI_ACC for k_, v_ in A0_SI.items()}                     # [(km/s)^2/Mpc]
FOOTS = ("canonical", "alt")

# ------------------------------------------------------------------------------------------------ the chain's cosmology (FP6)
h = 0.6736; om_b = 0.02237; om_c = 0.1200; T_CMB = 2.7255; N_eff = 3.046; ns = 0.965; SIG8 = 0.811
_c = 2.99792458e8; _G = 6.67430e-11
_H0si = 100 * h * 1e3 / MPC_M; _rhoc_si = 3 * _H0si ** 2 / (8 * math.pi * _G)
Og = (4 * 5.670374419e-8 * T_CMB ** 4 / _c ** 3) / _rhoc_si
Or = Og * (1 + N_eff * (7 / 8) * (4 / 11) ** (4 / 3))
Ob, Oc = om_b / h ** 2, om_c / h ** 2
Om = Ob + Oc
OL = 1 - Om - Or
FB = Ob / Om
H0 = 100 * h
RHOC0 = 3 * H0 ** 2 / (8 * math.pi * GMPC)
RHOM0 = Om * RHOC0                          # comoving mean matter density [Msun/Mpc^3]


def E(a):
    return np.sqrt(Or / a ** 4 + Om / a ** 3 + OL)


def Hof(a):
    return H0 * E(a)


def OmL_a(a):
    return OL / E(a) ** 2


def Omm_a(a):
    return Om / a ** 3 / E(a) ** 2


def rhoc_a(a):
    return RHOC0 * E(a) ** 2


def rhom_a(a):
    return RHOM0 / a ** 3


def _growth_table():
    dlnH = lambda a: 0.5 * (-4 * Or / a ** 4 - 3 * Om / a ** 3) / E(a) ** 2
    rhs = lambda N_, Y: [Y[1], 1.5 * Omm_a(math.exp(N_)) * Y[0] - (2 + dlnH(math.exp(N_))) * Y[1]]
    lna = np.linspace(math.log(1 / 1001.0), math.log(2.0), 4001)
    s = solve_ivp(rhs, (lna[0], lna[-1]), [1.0, 1.0], method="LSODA", rtol=1e-10, atol=1e-14, t_eval=lna)
    D = s.y[0]; D1 = float(np.interp(0.0, lna, D))
    return lna, D / D1, s.y[1] / s.y[0]


_LNA_G, _D_G, _F_G = _growth_table()


def Dof(a):
    return np.interp(np.log(a), _LNA_G, _D_G)


def fof(a):
    return np.interp(np.log(a), _LNA_G, _F_G)


def T_EH98(k):                              # FP6's EH98 no-wiggle transfer; k in 1/Mpc
    th = T_CMB / 2.7; s = 44.5 * math.log(9.83 / (Om * h * h)) / math.sqrt(1 + 10 * om_b ** 0.75)
    ag = 1 - 0.328 * math.log(431 * Om * h * h) * (Ob / Om) + 0.38 * math.log(22.3 * Om * h * h) * (Ob / Om) ** 2
    k = np.asarray(k, float)
    ge = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s / h) ** 4)); q = k * th * th / ge
    L = np.log(2 * math.e + 1.8 * q); Cc = 14.2 + 731.0 / (1 + 62.5 * q)
    return L / (L + Cc * q * q)


def Wth(x):
    x = np.asarray(x, float)
    return np.where(x > 1e-4, 3 * (np.sin(x) - x * np.cos(x)) / np.maximum(x, 1e-4) ** 3, 1.0 - x * x / 10.0)


_LK = np.linspace(math.log(1e-5), math.log(2e3), 6000); _KK = np.exp(_LK)
_P0 = _KK ** ns * T_EH98(_KK) ** 2
_NORM = SIG8 ** 2 / float(np.trapz(_KK ** 3 * _P0 * Wth(_KK * 8.0 / h) ** 2 / (2 * math.pi ** 2), _LK))
_D2 = _NORM * _KK ** 3 * _P0 / (2 * math.pi ** 2)


def sig2_cross(q, R):
    """<delta(<q) delta(<R)> at z = 0 (top hats, comoving Mpc)."""
    q = np.atleast_1d(np.asarray(q, float))
    return np.trapz(_D2[None, :] * Wth(np.outer(q, _KK)) * Wth(_KK * R)[None, :], _LK, axis=1)


def R_of_M(M):
    return (3 * np.asarray(M, float) / (4 * math.pi * RHOM0)) ** (1 / 3)


def S_of_M(M):
    R = np.atleast_1d(R_of_M(M))
    return np.array([float(sig2_cross([r_], r_)[0]) for r_ in R])


def correa_mah(M0):
    """Correa et al. (2015a, MNRAS 450, 1514; App. B): M(z) = M0 (1+z)^(a f) e^(-f z), a = 1.686 (2/pi)^(1/2) dD/dz|0 + 1,
    f = [S(M0/q) - S(M0)]^(-1/2), q = 4.137 zf^-0.9476, zf = -0.0064 (log M0)^2 + 0.0237 log M0 + 1.8837 (M0 in Msun)."""
    lm = math.log10(M0)
    zf = -0.0064 * lm ** 2 + 0.0237 * lm + 1.8837
    qq = 4.137 * zf ** (-0.9476)
    fM = 1.0 / math.sqrt(max(float(S_of_M(M0 / qq)[0] - S_of_M(M0)[0]), 1e-8))
    dDdz = -float(fof(1.0))
    al = (1.686 * math.sqrt(2 / math.pi) * dDdz + 1) * fM
    return (lambda z: M0 * (1 + np.asarray(z, float)) ** al * np.exp(-fM * np.asarray(z, float))), dict(alpha=al, f=fM)


# ------------------------------------------------------------------------------------------------ kernels (FP6's forms)
def x_P2(D):
    """P2's scalar field (units a0): (nu_P2 - 1) D in FP9's stable form."""
    D = np.maximum(np.asarray(D, float), 0.0)
    return np.where(D > 0, 1.0 / (1.0 + np.sqrt(1.0 + 1.0 / np.maximum(D, 1e-300))), 0.0)


def _h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def _dh_rar(y, e=1e-6):
    return (_h_rar(y * (1 + e)) - _h_rar(y * (1 - e))) / (2 * y * e)


_YP = brentq(lambda y: float(_dh_rar(y)), 1, 5); _HP = float(_h_rar(_YP))
_LYG = np.linspace(-14, 14, 280001); _YG = 10 ** _LYG
_DH = np.maximum(_dh_rar(_YG), 0.05 * _HP / (_YG + _YP))
_HM = float(_h_rar(_YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (_DH[1:] + _DH[:-1]) * np.diff(_YG))])


def nu_mono(y):                              # FP6's nu_mono (nu_RAR spliced to a monotone phantom above y* = 2.3374)
    y = np.maximum(np.asarray(y, float), 1e-14)
    return 1.0 + np.interp(np.log10(y), _LYG, _HM) / y


def x_kernel(y, kernel="p2", yth=0.0):
    if kernel == "p2":
        return x_P2(np.asarray(y, float) - (yth or 0.0))
    yy = np.maximum(np.asarray(y, float) - (yth or 0.0), 0.0)
    return np.where(yy > 0, (nu_mono(np.maximum(yy, 1e-14)) - 1.0) * yy, 0.0)


# ------------------------------------------------------------------------------------------------ the separator's L(a) and yield
L_LAMBDA_HY = 2.46                           # FP9's headline L_Lambda [Mpc], n = 2
Y_LAMBDA_HY = 1e-6 * float(OmL_a(1 / 1.25)) ** 4
L0_HY = L_LAMBDA_HY * float(OmL_a(1.0))      # H_Y's L(z = 0) = 1.688 Mpc
# H_S (FP13; linearly ill-posed as written, XR18; FP19 repairing): L(0) from FP13's committed state readouts --
# 2.879 Mpc (headline NL, delta_c), 3.248 Mpc (self-consistent matter feedback, H3), and with FP10's clearing thinning the
# one-halo term (A7: L(0.25) = 1.24-1.53 Mpc) times FP13's own L(0)/L(0.25) = 2.879/1.914.
L0_HS_BAND = (1.240 * 2.879 / 1.914, 3.248)


def L_of_a(a, L0, n=2.0):
    """the band-pass length on the leaf [physical Mpc]; L0 = inf or None -> no band-pass."""
    if L0 is None or not np.isfinite(L0):
        return None
    return L0 * (float(OmL_a(a)) / float(OmL_a(1.0))) ** (n / 2.0)


def yth_of_a(a, mode="HY"):
    return Y_LAMBDA_HY * float(OmL_a(a)) ** (-4.0) if mode == "HY" else 0.0


# ------------------------------------------------------------------------------------------------ Gaussian smoothing of spherical profiles
def gfrac(x):
    x = np.asarray(x, float)
    return erf(x / math.sqrt(2)) - math.sqrt(2 / math.pi) * x * np.exp(-x * x / 2)


def shell_frac(r, rp, L):
    """FP6's closed form: a unit shell at rp, Gaussian-smoothed (sigma = L per axis), enclosed inside r."""
    s = math.sqrt(2) * L; rp = np.maximum(rp, 1e-300)
    return 0.5 * (erf((r + rp) / s) + erf((r - rp) / s)) - (L / (rp * math.sqrt(2 * math.pi))) * (
        np.exp(-(r - rp) ** 2 / (2 * L * L)) - np.exp(-(r + rp) ** 2 / (2 * L * L)))


class Smoother:
    """S_L on a fixed log grid: (S_L M)(r_i) = sum_j F_ij dM_j + M_0 gfrac(r_i/L)."""

    def __init__(self, rg):
        self.rg = rg; self.rgm = np.sqrt(rg[1:] * rg[:-1]); self.L = None

    def set_L(self, L):
        if self.L is not None and abs(L / self.L - 1) < 2e-3:
            return
        self.L = L
        with np.errstate(all="ignore"):
            self.F = shell_frac(self.rg[:, None], self.rgm[None, :], L)
        self.g0 = gfrac(self.rg / L)

    def __call__(self, M):
        with np.errstate(all="ignore"):
            return self.F @ np.diff(M) + M[0] * self.g0


def phantom_enclosed(rg, dMb, a0, L, kernel="p2", yth=0.0, sm=None, out_filter=True):
    """the chain's band-passed phantom (enclosed mass on the grid rg) for a spherical baryon excess dMb(<rg)."""
    if L is None:
        gbp = GMPC * dMb / rg ** 2
    else:
        sm = sm if sm is not None else Smoother(rg)
        sm.set_L(L)
        gbp = GMPC * (dMb - sm(dMb)) / rg ** 2
    Mraw = np.sign(gbp) * a0 * x_kernel(np.abs(gbp) / a0, kernel, yth) * rg ** 2 / GMPC
    if L is None or not out_filter:
        return Mraw
    return Mraw - sm(Mraw)


# ------------------------------------------------------------------------------------------------ initial Lagrangian profile
DELTA_C = 1.686
GH3 = ((-math.sqrt(3.0), 1 / 6), (0.0, 2 / 3), (math.sqrt(3.0), 1 / 6))   # 3-node Gauss-Hermite (environment ensemble)


def initial_profile(Mf, zf, Nq, t_env=0.0, qmin_frac=0.05):
    """shells around a cluster of collapsed mass Mf at zf (Correa inside R_f; constrained mean + t_env x conditional scatter
    outside); delta extrapolated linearly to z = 0; a running minimum keeps delta(<q) non-increasing outward."""
    Rf = float(R_of_M(Mf))
    qmax = max(3.0 * Rf, Rf + 40.0)
    qe = np.geomspace(qmin_frac * Rf, qmax, Nq + 1)
    qm = ((qe[1:] ** 3 + qe[:-1] ** 3) / 2) ** (1 / 3)
    m = 4 * math.pi / 3 * RHOM0 * (qe[1:] ** 3 - qe[:-1] ** 3)
    Mq = 4 * math.pi / 3 * RHOM0 * qm ** 3
    M0 = math.exp(brentq(lambda l: math.log(correa_mah(math.exp(l))[0](zf)) - math.log(Mf), math.log(Mf) - 0.5, math.log(Mf) + 6.0))
    mah = correa_mah(M0)[0]
    dL = np.zeros(Nq)
    inner = qm <= Rf
    zz = np.linspace(zf, 40.0, 8000); Mz = mah(zz)
    zc = np.interp(np.log(Mq[inner]), np.log(Mz[::-1]), zz[::-1], left=40.0, right=zf)
    dL[inner] = DELTA_C / Dof(1 / (1 + zc))
    s_ff = float(sig2_cross([Rf], Rf)[0])
    out = ~inner
    s_cross = sig2_cross(qm[out], Rf)
    dL[out] = DELTA_C / float(Dof(1 / (1 + zf))) * s_cross / s_ff
    if t_env != 0.0:
        s_qq = np.array([float(sig2_cross([q_], q_)[0]) for q_ in qm[out]])
        dL[out] = dL[out] + t_env * np.sqrt(np.maximum(s_qq - s_cross ** 2 / s_ff, 0.0))
    dL = np.minimum.accumulate(dL)
    return dict(qe=qe, qm=qm, m=m, dL=dL, Rf=Rf, qmax=qmax, Mf=Mf, zf=zf, t_env=t_env, M0=M0)


# ------------------------------------------------------------------------------------------------ the dark sector's histories (committed inputs)
ZG_FP10 = np.array([0, 0.1, 0.25, 0.4, 0.6, 0.8, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4, 5, 6, 8, 10, 12, 15, 20, 30.0])
FP10_JSON = os.path.join(REPO, "real_research", "derivation_chain_2026", "FP10_internal_splitting_dark_sector_results.json")
XR19_WEB_JSON = os.path.join(HERE, "XR19_web_runaway_results.json")
XR19_FRONT_JSON = os.path.join(HERE, "XR19_front_physics_results.json")


def fp10_budget(vk=600.0, K="185"):
    """FP10's committed halo-collapse budget (A6): F(z) converted, F_b(z) bias-weighted escaped, on L357's ZG."""
    b = json.load(open(FP10_JSON))["numbers"]["A6"]["budget"][f"{vk:.0f}|{K}"]
    return np.array(b["F"]), np.array(b["Fb"])


def xr19_ftot(key="nominal"):
    """XR19's web-runaway F_tot(z) (converted fraction of the whole fluid)."""
    d = json.load(open(XR19_WEB_JSON))["numbers"]["F_tot"][key]
    zz = np.array(sorted(float(k_) for k_ in d)); ff = np.array([d[f"{z_:.1f}"] if f"{z_:.1f}" in d else d[str(z_)] for z_ in zz])
    return zz, ff


def fweb_history(fp10, key="nominal"):
    zw, Ft = xr19_ftot(key)
    Fh = np.interp(zw, ZG_FP10, fp10[0])
    return zw, np.clip((Ft - Fh) / np.maximum(1 - Fh, 1e-9), 0, 1)


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


# ------------------------------------------------------------------------------------------------ particles
EV_NONE, EV_EPOCH, EV_TURN, EV_FRONT = 0, 1, 2, 3
TAG = {"baryon": 0, "cold": 1, "bound": 2, "escape": 3, "web": 4, "front": 5, "turn": 6}


def build_particles(ic, dark="lcdm", vk=600.0, nmu=4, fp10=None, fweb=None, zobs=0.4, vinf_frac=1.0):
    """split every Lagrangian shell into a baryon particle and dark sub-particles.  dark: 'lcdm'/'cold' (all cold);
    'nominal' (FP10 escape + XR19 web epochs + the remainder at the host's front); 'turnaround' (escape + the smooth carrier
    converts at max(turnaround, z = 1.5), or at the front if it gets there first); 'front' (escape + the smooth carrier at the
    front); 'halo' (escape only; the rest stays cold -- the largest cold phase the chain's histories allow)."""
    N = len(ic["m"]); idx = np.arange(N)
    cols = {k_: [] for k_ in ("idx", "sp", "m", "ev", "ev_s", "ev_v", "ev_mu", "tag")}

    def add(m_, sp=1, ev=EV_NONE, ev_s=np.inf, ev_v=0.0, ev_mu=0.0, tag=1):
        cols["idx"].append(idx); cols["sp"].append(np.full(N, sp)); cols["m"].append(np.asarray(m_, float))
        cols["ev"].append(np.full(N, ev)); cols["ev_s"].append(np.full(N, ev_s)); cols["ev_v"].append(np.full(N, ev_v))
        cols["ev_mu"].append(np.full(N, ev_mu)); cols["tag"].append(np.full(N, tag))

    add(FB * ic["m"], sp=0, tag=TAG["baryon"])
    md = (1 - FB) * ic["m"]
    meta = {}
    if dark in ("lcdm", "cold"):
        add(md, tag=TAG["cold"])
    else:
        F, Fb = fp10
        mu, wmu = np.polynomial.legendre.leggauss(nmu); wmu = wmu / 2.0
        Fz = float(np.interp(zobs, ZG_FP10, F)); Fbz = float(np.interp(zobs, ZG_FP10, Fb))
        f_bound = max(Fz - Fbz, 0.0)
        zfine = np.linspace(zobs, 30.0, 6000); Fbf = np.interp(zfine, ZG_FP10, Fb)
        esc_z = [float(np.interp(q_ * Fbz, Fbf[::-1], zfine[::-1])) for q_ in (5 / 6, 1 / 2, 1 / 6)]
        f_smooth = 1.0 - Fz
        zw, fw = fweb
        fwz = float(np.interp(zobs, zw, fw))
        web_z = [float(np.interp(q_ * fwz, fw[::-1], zw[::-1])) for q_ in (3 / 4, 1 / 4)] if dark == "nominal" else []
        f_web = f_smooth * fwz if dark == "nominal" else 0.0
        f_unconv = f_smooth - f_web
        add(md * f_bound, tag=TAG["bound"])
        for ze in esc_z:
            for k_ in range(nmu):
                add(md * Fbz / 3.0 * wmu[k_], ev=EV_EPOCH, ev_s=-math.log(1 + ze), ev_v=vinf_frac * vk, ev_mu=mu[k_], tag=TAG["escape"])
        for zwk in web_z:
            for k_ in range(nmu):
                add(md * f_web / len(web_z) * wmu[k_], ev=EV_EPOCH, ev_s=-math.log(1 + zwk), ev_v=vk, ev_mu=mu[k_], tag=TAG["web"])
        if dark == "halo":
            add(md * f_unconv, tag=TAG["cold"])
        elif dark == "turnaround":
            for k_ in range(nmu):
                add(md * f_unconv * wmu[k_], ev=EV_TURN, ev_s=-math.log(1 + 1.5), ev_v=vk, ev_mu=mu[k_], tag=TAG["turn"])
        else:
            for k_ in range(nmu):
                add(md * f_unconv * wmu[k_], ev=EV_FRONT, ev_v=vk, ev_mu=mu[k_], tag=TAG["front"])
        meta = dict(esc_z=esc_z, web_z=web_z, f_bound=f_bound, f_esc=Fbz, f_web=f_web, f_unconv=f_unconv)
    out = {k_: np.concatenate(v_) for k_, v_ in cols.items()}
    out["meta"] = meta
    return out


# ------------------------------------------------------------------------------------------------ the shell integrator
SNAPS = (-0.12, -0.08, -0.04, 0.0, 0.04, 0.08, 0.12)        # Delta ln a around z_obs (FP16's window; the samples' z spread)


def run_shells(ic, parts, a0=None, L0=None, kernel="p2", ymode="HY", z_obs=0.4, snaps=SNAPS, z_i=150.0, ds_early=0.005,
               ds_late=0.00075, z_switch=6.0, eps_frac=0.004, jf_range=(0.15, 0.35), seed=28, ngrid=260, front_frac=0.95):
    N = len(parts["m"]); qm = ic["qm"]; dL = ic["dL"]; idx = parts["idx"]
    a_i = 1 / (1 + z_i); Di = float(Dof(a_i)); fi = float(fof(a_i)); Hi = float(Hof(a_i))
    x = qm[idx] * (1 - Di * dL[idx] / 3.0)
    p = -a_i ** 2 * qm[idx] * dL[idx] * Di * fi * Hi / 3.0
    m = parts["m"].astype(float); sp = parts["sp"]; isb = sp == 0
    j2 = np.zeros(N); turned = np.zeros(N, bool)
    jf = np.random.default_rng(seed).uniform(jf_range[0], jf_range[1], len(qm))[idx]
    ev = parts["ev"]; ev_s = parts["ev_s"]; ev_v = parts["ev_v"]; ev_mu = parts["ev_mu"]
    done = ev == EV_NONE
    kicked_at = np.full(N, np.nan)
    s_obs = -math.log(1 + z_obs)
    snap_s = sorted(s_obs + np.asarray(snaps, float))
    s_end = snap_s[-1]
    s_sw = -math.log(1 + z_switch)
    grid = list(np.arange(math.log(a_i), s_sw, ds_early)) + list(np.arange(s_sw, s_end, ds_late)) + list(snap_s)
    grid = np.array(sorted(set(np.round(grid, 12)))); grid = grid[grid <= s_end + 1e-12]
    rg = np.geomspace(1e-3, 80.0, ngrid); sm = Smoother(rg)
    use_ph = a0 is not None
    eps0 = eps_frac * 0.171 * ic["Rf"] / (1 + z_obs)
    snapsout = []; si = 0

    def phantom_force(a, xs):
        rb = a * xs[isb]; mb = m[isb]
        o = np.argsort(rb); cb = np.cumsum(mb[o])
        Mb = np.interp(rg, rb[o], cb, left=0.0)
        rmax = 0.9 * a * xs.max()
        dMb = Mb - 4 * math.pi / 3 * FB * rhom_a(a) * rg ** 3
        inside = rg <= rmax
        dMb = np.where(inside, dMb, dMb[inside][-1])
        Mph = phantom_enclosed(rg, dMb, a0, L_of_a(a, L0), kernel, yth_of_a(a, ymode), sm)
        g = np.zeros(N)
        g[isb] = -GMPC * np.interp(rb, rg, Mph) / np.maximum(rb, 1e-6) ** 2
        return g, Mph

    def accel(a, xs):
        r = a * xs
        o = np.argsort(xs)
        cm = np.cumsum(m[o]) - 0.5 * m[o]
        Menc = np.empty(N); Menc[o] = cm
        g = -GMPC * Menc * r / (r * r + eps0 * eps0) ** 1.5 + 4 * math.pi / 3 * GMPC * rhom_a(a) * r + j2 / np.maximum(r, 1e-6) ** 3
        Mph = None
        if use_ph:
            gph, Mph = phantom_force(a, xs)
            g = g + gph
        return g, Mph, o, cm

    a = math.exp(grid[0])
    g, Mph, o, cm = accel(a, x)
    vr_prev = Hof(a) * a * x + p / a
    for n_ in range(len(grid) - 1):
        s0, s1 = grid[n_], grid[n_ + 1]; ds = s1 - s0
        a0_, a1_ = math.exp(s0), math.exp(s1); am = math.exp(0.5 * (s0 + s1))
        p = p + 0.5 * ds * a0_ * g / Hof(a0_)
        x = x + ds * p / (am ** 2 * Hof(am))
        neg = x < 0
        if np.any(neg):
            x[neg] = -x[neg]; p[neg] = -p[neg]
        g, Mph, o, cm = accel(a1_, x)
        p = p + 0.5 * ds * a1_ * g / Hof(a1_)
        r = a1_ * x
        vr = Hof(a1_) * r + p / a1_
        newt = (~turned) & (vr <= 0.0) & (vr_prev > 0.0)
        if np.any(newt):
            gN = g[newt] - j2[newt] / np.maximum(r[newt], 1e-6) ** 3 - 4 * math.pi / 3 * GMPC * rhom_a(a1_) * r[newt]
            j2[newt] = (jf[newt] * r[newt]) ** 2 * r[newt] * np.abs(np.minimum(gN, 0.0))
            turned |= newt
        todo = ~done
        if np.any(todo):
            fire = todo & (ev == EV_EPOCH) & (ev_s <= s1 + 1e-12)
            pend = todo & ((ev == EV_FRONT) | (ev == EV_TURN))
            if np.any(pend):
                rs = a1_ * x[o]
                dens = cm / (4 * math.pi / 3 * np.maximum(rs, 1e-6) ** 3)
                ok = np.where(dens >= 200 * rhoc_a(a1_))[0]
                r200c = rs[ok[-1]] if len(ok) else 0.0
                fire |= pend & (r < front_frac * r200c)
                fire |= todo & (ev == EV_TURN) & (vr <= 0.0) & (s1 >= ev_s)
            if np.any(fire):
                vv = ev_v[fire]; mu = ev_mu[fire]; rr = r[fire]
                p[fire] = p[fire] + a1_ * vv * mu
                j2[fire] = j2[fire] + rr ** 2 * vv ** 2 * (1 - mu ** 2)
                done |= fire; kicked_at[fire] = s1
        vr_prev = Hof(a1_) * a1_ * x + p / a1_
        while si < len(snap_s) and abs(s1 - snap_s[si]) < 1e-9:
            snapsout.append(dict(s=s1, a=a1_, x=x.copy(), m=m.copy(), Mph=None if Mph is None else Mph.copy()))
            si += 1
    return dict(snaps=snapsout, rg=rg, sp=sp, tag=parts["tag"], kicked_at=kicked_at, nsteps=len(grid) - 1)


# ------------------------------------------------------------------------------------------------ profiles and splashback
XB = np.geomspace(0.03, 40.0, 121)          # comoving bin edges [Mpc]
XBM = np.sqrt(XB[1:] * XB[:-1])
XVOL = 4 * math.pi / 3 * (XB[1:] ** 3 - XB[:-1] ** 3)


def _r_delta(rs, cum, rho_ref, Delta=200.0):
    dens = cum / (4 * math.pi / 3 * np.maximum(rs, 1e-9) ** 3)
    ok = np.where(dens >= Delta * rho_ref)[0]
    if not len(ok):
        return float("nan")
    i = ok[-1]
    if i + 1 >= len(rs):
        return float(rs[i])
    d0, d1 = dens[i], dens[i + 1]; r0, r1 = rs[i], rs[i + 1]
    t = (math.log(d0) - math.log(Delta * rho_ref)) / max(math.log(d0) - math.log(max(d1, 1e-300)), 1e-12)
    return float(math.exp(math.log(r0) + t * (math.log(r1) - math.log(r0))))


def snapshot_profiles(res, sel):
    """per snapshot: comoving-bin density contrasts rho/rho_m for each selection (and the phantom, the lensing total), the
    mass inside the innermost bin, and r200m (lensing: Newtonian + phantom) and r200c (Newtonian), comoving."""
    out = []
    for sn in res["snaps"]:
        a = sn["a"]; x = sn["x"]; m = sn["m"]
        prof = {}
        for k_, msk in sel.items():
            h_, _ = np.histogram(x[msk], bins=XB, weights=m[msk])
            prof[k_] = h_ / XVOL / RHOM0
        inner = {k_: float(np.sum(m[msk & (x < XB[0])])) for k_, msk in sel.items()}
        o = np.argsort(x); rs = a * x[o]; cum = np.cumsum(m[o])
        if sn["Mph"] is not None:
            Mph_e = np.interp(a * XB, res["rg"], sn["Mph"])
            prof["phantom"] = np.diff(Mph_e) / XVOL / RHOM0
            inner["phantom"] = float(Mph_e[0])
            Mph_at = np.interp(rs, res["rg"], sn["Mph"])
        else:
            prof["phantom"] = np.zeros(len(XBM)); inner["phantom"] = 0.0; Mph_at = 0.0
        prof["lens"] = prof["all"] + prof["phantom"]; inner["lens"] = inner["all"] + inner["phantom"]
        r200m_l = _r_delta(rs, cum + Mph_at, rhom_a(a)); r200m_n = _r_delta(rs, cum, rhom_a(a)); r200c_n = _r_delta(rs, cum, rhoc_a(a))
        out.append(dict(a=a, prof=prof, inner=inner, r200m_lens=r200m_l / a, r200m_newt=r200m_n / a, r200c_newt=r200c_n / a,
                        M200m_lens=200 * rhom_a(a) * 4 * math.pi / 3 * r200m_l ** 3, M200m_newt=200 * rhom_a(a) * 4 * math.pi / 3 * r200m_n ** 3))
    return out


def stack(items):
    """items: list of (weight, snapshot-profile dict); returns the weighted stack."""
    w = np.array([w_ for w_, _ in items], float); w = w / w.sum()
    sps = [s_ for _, s_ in items]
    keys = sps[0]["prof"].keys()
    prof = {k_: sum(w_ * s_["prof"][k_] for w_, s_ in zip(w, sps)) for k_ in keys}
    inner = {k_: sum(w_ * s_["inner"][k_] for w_, s_ in zip(w, sps)) for k_ in sps[0]["inner"]}
    lg = lambda key: float(np.exp(sum(w_ * math.log(s_[key]) for w_, s_ in zip(w, sps))))
    return dict(prof=prof, inner=inner, r200m_lens=lg("r200m_lens"), r200m_newt=lg("r200m_newt"), r200c_newt=lg("r200c_newt"),
                M200m_lens=float(sum(w_ * s_["M200m_lens"] for w_, s_ in zip(w, sps))),
                M200m_newt=float(sum(w_ * s_["M200m_newt"] for w_, s_ in zip(w, sps))))


SIG_LN = 0.08                                # declared smoothing of the 3D log-slope (Gaussian in ln r)
SIG_TRIAX = 0.12                             # declared apocentre scatter (lognormal in r) of the matter a spherical model lacks


def smooth_matter(st, sig=SIG_TRIAX):
    """spread every particle-based profile (not the phantom, smooth on scale L) by a lognormal of width sig in r: the
    triaxiality/substructure scatter of apocentres that widens a caustic without moving it (Adhikari et al. 2014, Fig. 3)."""
    if sig <= 0:
        return st
    lx = np.log(XBM); dl = lx[1] - lx[0]; n = int(math.ceil(4 * sig / dl))
    ker = np.exp(-0.5 * (np.arange(-n, n + 1) * dl / sig) ** 2); ker /= ker.sum()
    out = dict(st); out["prof"] = dict(st["prof"])
    for k_ in st["prof"]:
        if k_ in ("phantom", "lens"):
            continue
        mass = st["prof"][k_] * XVOL
        out["prof"][k_] = np.convolve(np.pad(mass, (n, n), mode="edge"), ker, mode="valid") / XVOL
    out["prof"]["lens"] = out["prof"]["all"] + out["prof"]["phantom"]
    return out


def log_slope(rho, xm=XBM, sig_ln=SIG_LN):
    lx = np.log(xm); good = rho > 0
    lr = np.where(good, np.log(np.where(good, rho, 1.0)), 0.0)
    dl = lx[1] - lx[0]; n = int(math.ceil(4 * sig_ln / dl))
    ker = np.exp(-0.5 * (np.arange(-n, n + 1) * dl / sig_ln) ** 2)
    num = np.convolve(lr * good, ker, mode="same"); den = np.convolve(good.astype(float), ker, mode="same")
    lrs = np.where(den > 0.5 * ker.sum(), num / np.maximum(den, 1e-300), np.nan)
    return np.gradient(lrs, lx), good


def splashback3d(rho, r200, lo=0.4, hi=3.0):
    """r_sp = minimum of the smoothed 3D log-slope in [lo, hi] r200m; every local minimum; any non-positive density there."""
    sl, good = log_slope(rho)
    win = (XBM >= lo * r200) & (XBM <= hi * r200)
    negw = win & ~good
    res = dict(neg=bool(np.any(negw)), neg_range=([float(XBM[negw].min() / r200), float(XBM[negw].max() / r200)] if np.any(negw) else None))
    ok = win & np.isfinite(sl)
    if not np.any(ok):
        res.update(r_sp=float("nan"), gamma=float("nan"), minima=[]); return res
    i = int(np.where(ok)[0][np.argmin(sl[ok])])
    mins = [(round(float(XBM[k_] / r200), 3), round(float(sl[k_]), 2)) for k_ in np.where(ok)[0] if 0 < k_ < len(sl) - 1
            and np.isfinite(sl[k_ - 1]) and np.isfinite(sl[k_ + 1]) and sl[k_] < sl[k_ - 1] and sl[k_] <= sl[k_ + 1]]
    res.update(r_sp=float(XBM[i]), x_sp=float(XBM[i] / r200), gamma=float(sl[i]), minima=mins)
    return res


# ------------------------------------------------------------------------------------------------ projection and the observers' DK14 fit
HD = 0.7                                     # the data's h (DES/ACT/CCCP analyses)
R_WL = np.geomspace(0.2, 20.0, 14)           # Shin et al. (2021): 14 WL bins over 0.2-20 h^-1 cMpc
R_GAL = np.geomspace(0.2, 20.0, 20)          # 20 galaxy-density bins over the same range
ERR_WL, ERR_GAL = 43.0, 62.0                 # Shin et al. (2021) total S/N -> per-bin fractional errors 1/(S/N/sqrt(N))


def shell_esd_kernel(R, e):
    """Delta Sigma and Sigma at projected radii R per unit mass in each uniform-density shell (e[k], e[k+1])."""
    r1, r2 = e[:-1], e[1:]
    R = np.atleast_1d(R)[:, None]; rho = 1.0 / ((4 * np.pi / 3) * (r2 ** 3 - r1 ** 3))
    pc = lambda z: np.clip(z, 0.0, None)
    Sig = 2 * rho * (np.sqrt(pc(r2 ** 2 - R ** 2)) - np.sqrt(pc(r1 ** 2 - R ** 2)))
    Mcyl = 1.0 - (4 * np.pi / 3) * rho * (pc(r2 ** 2 - R ** 2) ** 1.5 - pc(r1 ** 2 - R ** 2) ** 1.5)
    return Mcyl / (np.pi * R ** 2) - Sig, Sig


def nfw_esd_wb(R, M200, c, rho_ref, Delta=200.0):
    """Wright & Brainerd (2000) NFW Delta Sigma; M200 w.r.t. Delta rho_ref."""
    r200 = (3 * M200 / (4 * np.pi * Delta * rho_ref)) ** (1 / 3); rs = r200 / c
    dc = (Delta / 3.) * c ** 3 / (math.log(1 + c) - c / (1 + c)); x = np.asarray(R, float) / rs; g = np.empty_like(x)
    for i, xi in enumerate(x):
        if xi < 1 - 1e-6:
            at = np.arctanh(math.sqrt((1 - xi) / (1 + xi)))
            g[i] = 8 * at / (xi ** 2 * math.sqrt(1 - xi ** 2)) + 4 / xi ** 2 * math.log(xi / 2) - 2 / (xi ** 2 - 1) + 4 * at / ((xi ** 2 - 1) * math.sqrt(1 - xi ** 2))
        elif xi < 1 + 1e-6:
            g[i] = 10 / 3. + 4 * math.log(0.5)
        else:
            at = np.arctan(math.sqrt((xi - 1) / (1 + xi)))
            g[i] = 8 * at / (xi ** 2 * math.sqrt(xi ** 2 - 1)) + 4 / xi ** 2 * math.log(xi / 2) - 2 / (xi ** 2 - 1) + 4 * at / ((xi ** 2 - 1) ** 1.5)
    return rs * dc * rho_ref * g


_KWL = shell_esd_kernel(R_WL / HD, XB)       # model bins are comoving Mpc; data radii h^-1 cMpc
_KGAL = shell_esd_kernel(R_GAL / HD, XB)


def model_esd(st, key="lens", mean=1.0):
    """Delta Sigma [Msun/Mpc^2, comoving] of the stacked excess (contrast - mean) at R_WL, with the inner mass as a point."""
    dM = (st["prof"][key] - mean) * XVOL * RHOM0
    return _KWL[0] @ dM + st["inner"][key] / (math.pi * (R_WL / HD) ** 2)


def model_sigma(st, key="bar", mean=FB):
    dM = (st["prof"][key] - mean) * XVOL * RHOM0
    return _KGAL[1] @ dM


DK_FINE = np.geomspace(1e-3, 60.0, 700)      # DK14 model shells [h^-1 cMpc]
DK_MID = np.sqrt(DK_FINE[1:] * DK_FINE[:-1])
DK_VOL = 4 * np.pi / 3 * (DK_FINE[1:] ** 3 - DK_FINE[:-1] ** 3)
_DKWL = shell_esd_kernel(R_WL, DK_FINE)
_DKGAL = shell_esd_kernel(R_GAL, DK_FINE)


def dk14_rho(r, p):
    """DK14 as fitted by Shin et al. (2021, eqs. 2-6): tau_max = 20, r_0 = 1.5 h^-1 cMpc."""
    lrs, la, lrs_, lrt, lb, lg, lr0, se = p[:8]
    rs, al, rt, be, ga = 10 ** lrs_, 10 ** la, 10 ** lrt, 10 ** lb, 10 ** lg
    inner = 10 ** lrs * np.exp(-2.0 / al * ((r / rs) ** al - 1.0)) * (1.0 + (r / rt) ** be) ** (-ga / be)
    return inner + 10 ** lr0 / (1.0 / 20.0 + (r / 1.5) ** se)


def dk14_slope(r, p, eps=1e-4):
    return (np.log(dk14_rho(r * (1 + eps), p)) - np.log(dk14_rho(r * (1 - eps), p))) / (2 * eps)


def dk14_fit(y, kind="esd", nstart=12, seed=7, r200h=None, win=(0.5, 3.0)):
    """MAP fit of DK14 (+ an inner point mass for WL) to a model profile with the declared fractional errors and the
    Shin et al. (2021) priors: log alpha ~ N(log 0.22, 0.6), log beta ~ N(log 6, 0.2), log gamma ~ N(log 4, 0.2), r_s in
    [0.1, 5], r_t in [0.5, 5] h^-1 cMpc, s_e in [0.1, 10].  r_sp = steepest slope of the fitted 3D profile in [0.5, 3] r200m
    (the outskirts window; a spherical model's inner caustics must not be read as splashback)."""
    from scipy.optimize import least_squares
    if kind == "esd":
        K = _DKWL[0]; frac = math.sqrt(len(R_WL)) / ERR_WL; R = R_WL
    else:
        K = _DKGAL[1]; frac = math.sqrt(len(R_GAL)) / ERR_GAL; R = R_GAL
    sig = frac * np.abs(y)
    pri = np.array([math.log10(0.22), math.log10(6.0), math.log10(4.0)]); psd = np.array([0.6, 0.2, 0.2])

    def model(p):
        out = K @ (dk14_rho(DK_MID, p) * DK_VOL)
        if kind == "esd":
            out = out + 10 ** p[8] / (math.pi * R ** 2)
        return out

    def resid(p):
        return np.concatenate([(model(p) - y) / sig, (np.array([p[1], p[4], p[5]]) - pri) / psd])

    lo = [-10, -3, math.log10(0.1), math.log10(0.5), -2, -2, -10, 0.1]
    hi = [30, 1, math.log10(5.0), math.log10(5.0), 2, 2, 30, 10.0]
    if kind == "esd":
        lo.append(0.0); hi.append(20.0)
    rng = np.random.default_rng(seed); best = None
    ylev = float(np.median(np.abs(y))) + 1e-300
    for _ in range(nstart):
        p0 = [math.log10(ylev) + 0.3 + rng.normal(0, 0.5), pri[0] + rng.normal(0, 0.2), rng.uniform(math.log10(0.15), math.log10(0.8)),
              rng.uniform(math.log10(0.6), math.log10(3.0)), pri[1] + rng.normal(0, 0.1), pri[2] + rng.normal(0, 0.1),
              math.log10(ylev) - 1.0 + rng.normal(0, 0.5), rng.uniform(0.8, 2.0)]
        if kind == "esd":
            p0.append(math.log10(ylev) + 12.0 + rng.normal(0, 0.5))
        p0 = np.clip(p0, np.array(lo) + 1e-6, np.array(hi) - 1e-6)
        try:
            r_ = least_squares(resid, p0, bounds=(lo, hi), x_scale="jac", max_nfev=3000)
        except Exception:
            continue
        if best is None or r_.cost < best.cost:
            best = r_
    p = best.x
    rr = np.geomspace(0.3, 8.0, 900) if r200h is None else np.geomspace(win[0] * r200h, win[1] * r200h, 900)
    sl = dk14_slope(rr, p)
    i = int(np.argmin(sl))                   # r_sp: the steepest slope (inside [0.5, 3] r200m when r200h is given)
    chi2 = float(np.sum(((model(p) - y) / sig) ** 2))
    return dict(p=[float(v) for v in p], r_sp=float(rr[i]), gamma=float(sl[i]), chi2=chi2, n=len(y))


# ------------------------------------------------------------------------------------------------ the published measurements (h = 0.7; comoving)
# r_sp/r200m and gamma(r_sp) as quoted; M200m in 1e14 h^-1 Msun.  Compilation: Shin et al. (2021, MNRAS 507, 5758) Table 3,
# checked against the originals: Chang et al. (2018, ApJ 864, 83) sec. 5; Shin et al. (2021) sec. 4; Contigiani, Hoekstra &
# Bahe (2019, MNRAS 485, 408) abstract; Shin et al. (2019, MNRAS 487, 2900); Zurcher & More (2019, ApJ 874, 184).
DATA = {
    "DES-Y1 redMaPPer (Chang+2018)": dict(M200m=1.8, z=0.41, sel="optical",
                                          wl=dict(x=0.97, lo=0.15, hi=0.15, g=-3.5, glo=0.4, ghi=0.4),
                                          gal=dict(x=0.82, lo=0.05, hi=0.05, g=-3.6, glo=0.3, ghi=0.3)),
    "ACT-DR5 x DES-Y3 (Shin+2021)": dict(M200m=4.8, z=0.46, sel="SZ", sim_x=1.07,
                                         wl=dict(x=1.16, lo=0.29, hi=0.21, g=-3.42, glo=0.40, ghi=0.54),
                                         gal=dict(x=1.10, lo=0.14, hi=0.06, g=-3.40, glo=0.17, ghi=0.32)),
    "CCCP X-ray (Contigiani+2019)": dict(M200m=14.0, z=0.28, sel="X-ray",
                                         wl=dict(x=1.34, lo=0.26, hi=0.45, g=-4.3, glo=1.5, ghi=1.0), gal=None),
    "Planck SZ (Zurcher & More 2019)": dict(M200m=6.2, z=0.18, sel="SZ", wl=None,
                                            gal=dict(x=0.92, lo=0.15, hi=0.13, g=None, glo=None, ghi=None)),
}


def pull(val, d, key="x"):
    """signed pull of a model value against an asymmetric measurement (the error on the model's side)."""
    obs = d[key]; lo = d["lo" if key == "x" else "glo"]; hi = d["hi" if key == "x" else "ghi"]
    if obs is None or val is None or not np.isfinite(val):
        return float("nan")
    return (val - obs) / (hi if val > obs else lo)


# ------------------------------------------------------------------------------------------------ reporting helpers
class Report:
    def __init__(self, lane, slug, mutate):
        self.lane, self.slug, self.mutate = lane, slug + ("_MUTATE" if mutate else ""), mutate
        self.lines = []; self.checks = []; self.numbers = {}; self.t0 = time.time()

    def P(self, *a):
        s = " ".join(str(v) for v in a); print(s, flush=True); self.lines.append(s)

    def banner(self, t):
        self.P("\n" + "=" * 116 + "\n" + t + "\n" + "=" * 116)

    def check(self, name, measured, ok, load_bearing=True, reading=None):
        ok = bool(ok); self.checks.append(dict(name=name, ok=ok, measured=str(measured), load_bearing=load_bearing))
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
        if reading:
            self.P(f"         reading:  {reading}")
        return ok

    def el(self):
        return f"[{time.time() - self.t0:.0f} s]"

    def finish(self):
        nlb = sum(1 for c in self.checks if c["load_bearing"] and not c["ok"])
        npass = sum(1 for c in self.checks if c["ok"])
        verdict = f"{npass}/{len(self.checks)} checks pass; load-bearing failures: {nlb}"
        self.P("\n" + verdict + f"   {self.el()}")
        out = dict(lane=self.lane, mutate=self.mutate, checks=self.checks, numbers=self.numbers, verdict=verdict,
                   n_fail_load_bearing=nlb)
        base = self.slug[:-len("_MUTATE")] if self.mutate else self.slug
        with open(os.path.join(HERE, f"{base}_results{'_MUTATE' if self.mutate else ''}.json"), "w") as f:
            json.dump(out, f, indent=1, default=lambda o: o.tolist() if isinstance(o, np.ndarray) else str(o))
        with open(os.path.join(HERE, f"{self.slug}.out"), "w") as f:
            f.write("\n".join(self.lines) + "\n")
        return 1 if nlb else 0
