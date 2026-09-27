#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR21_pm_core -- THE PARTICLE-MESH ENGINE FOR THE DERIVATION CHAIN'S CURRENT MODEL (a library; the XR21 stage scripts
import it and code-test every piece of it).  Importing it builds nothing heavy; running it prints this description.

UNITS (the record's PM, L176/L346/L362/L366, read-only): comoving positions in Mpc/h; time in 1/H0; canonical momentum
p = a^2 dx/dt with dp/dt = -grad phi and lap phi = (3/2) Omega_m delta / a, so phi is the PHYSICAL peculiar potential in
H0^2 (Mpc/h)^2 and the PHYSICAL peculiar acceleration is |grad phi| / a, in units of UNIT_ACC = H0^2 Mpc/h (m/s^2).  The
peculiar velocity is v = p / a in units of 100 km/s.  (Stage 1 records, as a flag for the owners, that L346/L347/L362/DE11/
DE11b evaluate the MOND kernel at |grad phi| / a^2, i.e. (1+z) x the physical field; L377/L388 use 1/a.  This engine uses
1/a; the stage-1 script XR21_s1_hy_operator.py checks it against FP6's linear field.)

THE MODEL (read from the chain's files; they are authoritative, not this summary)
  GRAVITY (FP7's AQUAL-type root + FP9's separator H_Y) in the QUMOND-TYPE APPROXIMATION the chain's lead accepted for a first
  pass (FP7 R7e: AQUAL and QUMOND agree to <= 0.035 dex in discs; in spherical symmetry they are identical).  Every result
  that uses it carries the label "QUMOND-type approximation":
      phi_ph = B u,     lap u = div W,     W = C^Q(y) G,     G = grad (B phi_N[src]),     y = |G| / (a a0),
      C^Q(y) y = X(y - y_th),   X(D) = sqrt(D^2 + D) - D for D > 0 and 0 below the yield (P2's field law, FP1 L4c; the yield
                 floor J_Y = J_P2 + 2 y_th sqrt(Y), FP9 Y1: the scalar is frozen where the band-passed field is below y_th a0),
      B = S_xi - S_L,  S_l = exp(-k^2 l^2 / 2): C-H's heat branch read at two diffusion times (FP6 G6a, FP9 R9a); xi <= 100 pc
          (FP5 K-xi; FP7 floor ~0.03 pc) is far below any mesh, so S_xi = 1 on the mesh;
      L(a) = L_Lambda Omega_L(a)^(n/2),   y_th(a) = y_Lambda Omega_L(a)^(-p'),   Omega_L = 3 Lambda / <K>_h^2 with <K>_h = 3H(a)
          (CV4: the khronon's leaves are CMC, so both are uniform on each time slice).
      Headline cell (FP9 H2): L(0.25) = 1.3 Mpc, n = 2, y_th(0.25) = 1e-6, p' = 4  =>  L_Lambda = 2.46 Mpc, y_Lambda = 7.8e-8.
      All four are PARAMETERS.  Kernel: P2 (the chain's FP9 law); nu_mono available.
      FP13's H_S (27faacc84) replaces the four constants by state functionals -- L from <(S_B delta_m)^2>_h = delta_c^2 and
      y_th = c_y <|g_bp|^2>_h^(1/2)/a0 x max(0, 2q) -- carried here FROZEN (FP13's committed tables, HSFrozen) or LIVE (read from
      the box's own matter field each step, HSLive, with pluggable readout rules).  XR18 finds H_S linearly ILL-POSED as written
      at z <= 0.635 (the state term's own force, absent from this quasi-static operator); H_Y is linearly healthy per XR18.
      H_S boxes are therefore code paths only until the chain lead's repair; H_Y is kept as the healthy option.
      The gradient of the band-passed potential and the divergence of W are the record's centred differences (the operator
      form XR5 verified for L361/L377); the band-pass and the Poisson solve are spectral (continuous k^2, as L362).
      The tracking weight (FP9's 1/(1 + (H/c_s k)^2)) is omitted: a quasi-static phantom (bounded in stage 1).
  WHO SOURCES AND WHO FEELS THE PHANTOM -- a declared switch, 'reading':
      'chain'  FP10 / L353 reciprocity (and L377/L388's PM): the kernel reads the BARYONS' Newtonian field and only the
               baryons feel the phantom; the dark fluid sources and feels Newtonian gravity only.
      'fp9'    FP9's linear yardstick (FP6/L341 growth): all matter sources the kernel and all matter feels the phantom.
  LENSING: psi = Phi (FP7 R7d, no slip), so light sees phi_N + phi_ph: the lensing density is delta_m + delta_ph.

  THE DARK FLUID (FK1; FP10's action): a classical coherent field, NOT a particle species -- the particles below are only a
  numerical device.  Heavy (cold, convertible, phi_H) and light (the daughters, phi_L) parts; both feel and source Newtonian
  gravity only.  The conversion phi_H phi_H -> phi_L phi_L is set off by the heavy part's OWN density above
      rho_t(z) / rho_bar_carrier = delta_t0 E(z)^4 / (1+z)^3   (FK1 N2; delta_t0 a parameter: FK1's bracket 5-25, the linear
      cell's 5.31, XR12's working band 7.5-13.5)
  and emits back-to-back daughters: a heavy particle of mass m becomes two light particles of mass m/2 with momenta
  p +- a (v_k / 100 km/s) n, n isotropic -- each daughter leaves at v_k relative to its parent.  Mass and momentum are conserved
  exactly; the kinetic energy gained per unit converted mass is v_k^2/2 (FK1 A1's latent heat; the rest-mass deficit
  v_k^2/2c^2 ~ 2e-6 is not tracked).  Daughters never convert back.  Re-accretion is automatic (they are followed).
      MESH trigger   the heavy density CIC'd on the mesh, read at each heavy particle; rate Gamma = Gamma_0 H(a);
                     'cap' (convert the excess above rho_t: FK1's stimulated instability stops at n_t, XR12 F2a) or
                     'cleared' (the whole cell, at the rate).
      SUB-GRID       the heavy fluid in UNRESOLVED clumps: the extended-Press-Schechter conditional collapsed fraction in halos
                     M_min < M < M_up(z) at the cell's linear overdensity (Mo & White 1996's spherical-collapse map, Lagrangian
                     cell mass rho_bar (1 + delta) V_cell), times each clump's above-threshold share (cap: 1 - delta_t/Delta_vir;
                     cleared: 1).  M_up(z) = delta_t(z) rho_bar_m V_cell: a clump heavier than that lifts a cell over the
                     threshold on its own, so the mesh trigger sees it.  Applied per particle by a fixed uniform number u
                     drawn at the start (a heavy particle converts once u < f_SG of its cell): irreversible, a running maximum.
                     XR12/XR16: FK1's gain length is ~pc at halo densities, so the 0.39 Mpc/h mesh cannot see the clumps it
                     converts; this prescription is REQUIRED and is compared with the mesh trigger where the mesh resolves
                     the clump (stage 1, test 5).

WHAT IS NOT HERE: hydrodynamics (the forest is the record's FGPA on the baryon particles, L347/L362), AQUAL's curl field, the
khronon's own dynamics, the tracking lag, any carrier cap or kick scale beyond FK1's.  kappa = 1/2 enters only through a0
(FITTED; Z = 5.7888); both a0 footings are carried: 9.3603e-11 (canonical) and 1.1312e-10 m/s^2 (alt), FP0.
"""
import os, sys, math, time, json, resource
import numpy as np
import scipy.fft as sfft
from scipy.special import erfc, erf
from scipy.integrate import solve_ivp, quad

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
G03 = os.path.join(REPO, "real_research", "g03_audit_2026")
DSEC = os.path.join(REPO, "real_research", "dark_sector_2026")
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")

C_KMS = 299792.458
MPC_M = 3.0856775814913673e22
GNEWT = 6.67430e-11
MSUN = 1.98847e30
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}         # FP0's footings (a0 = kappa c sqrt(G rho), kappa = 1/2 FITTED)
try:                                                          # FP0's committed values at full precision (FP9 reads the same)
    _n0 = json.load(open(os.path.join(CHAIN, "FP0_core_postulates_results.json")))["numbers"]
    A0_SI = {"canonical": float(_n0["a0_canonical"]), "alt": float(_n0["a0_rho_total"])}
except (OSError, KeyError, ValueError):
    pass
FOOTS = ("canonical", "alt")


def peak_rss_gb():
    """peak resident set size of this process (macOS reports bytes, Linux kB)."""
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e9 if sys.platform == "darwin" else r / 1e6


# ============================================================================================= cosmology
class Cosmo:
    """flat background: E(a)^2 = Or a^-4 + Om a^-3 + OL.  'l362' = the record's PM (no radiation, Om = 0.3138);
    'fp6' = the chain's growth yardstick (FP6: Om = (0.02237 + 0.1200)/h^2, radiation from T_CMB and N_eff)."""

    def __init__(self, kind="l362"):
        self.kind = kind
        self.h = 0.6736
        if kind == "l362":
            self.Om, self.Or = 0.3138, 0.0
        elif kind == "fp6":
            h = self.h; om_b, om_c = 0.02237, 0.1200; T_CMB = 2.7255; N_eff = 3.046
            H0 = 100 * h * 1e3 / 3.0856775814913673e22; rho_crit0 = 3 * H0 ** 2 / (8 * math.pi * 6.67430e-11)
            Og = (4 * 5.670374419e-8 * T_CMB ** 4 / 2.99792458e8 ** 3) / rho_crit0
            self.Or = Og * (1 + N_eff * (7 / 8) * (4 / 11) ** (4 / 3))
            self.Om = (om_b + om_c) / h ** 2
        else:
            raise ValueError(kind)
        self.OL = 1.0 - self.Om - self.Or
        self.fb = 0.02237 / (0.02237 + 0.1200)                 # baryon share of the matter (L366's WB)
        self.H0_SI = 100 * self.h * 1e3 / MPC_M
        self.UNIT_ACC = (MPC_M / self.h) * self.H0_SI ** 2       # m/s^2 per code unit of acceleration
        self._growth = None

    def E(self, a):
        return math.sqrt(self.Or / a ** 4 + self.Om / a ** 3 + self.OL)

    def Om_a(self, a):
        return (self.Om / a ** 3) / self.E(a) ** 2

    def OmL_a(self, a):
        return self.OL / self.E(a) ** 2

    def a0_code(self, foot):
        return A0_SI[foot] / self.UNIT_ACC

    # linear growth (LCDM, matter + Lambda + radiation) from an ODE started deep in matter domination: D ~ a
    def growth(self):
        if self._growth is None:
            N = np.linspace(math.log(1e-3), 0.0, 4001)
            def rhs(n, Y):
                a = math.exp(n); E2 = self.E(a) ** 2
                dlnH = 0.5 * (-4 * self.Or / a ** 4 - 3 * self.Om / a ** 3) / E2
                return [Y[1], 1.5 * self.Om_a(a) * Y[0] - (2 + dlnH) * Y[1]]
            s = solve_ivp(rhs, (N[0], 0.0), [1e-3, 1e-3], t_eval=N, method="LSODA", rtol=1e-10, atol=1e-16)
            D, Dp = s.y[0], s.y[1]
            self._growth = (N, D / D[-1], Dp / D)                # normalised D(a)/D(1) and f = dlnD/dlna
        return self._growth

    def D(self, a):
        N, D, _ = self.growth(); return float(np.interp(math.log(a), N, D))

    def f(self, a):
        N, _, f = self.growth(); return float(np.interp(math.log(a), N, f))


# ============================================================================================= H_Y constants
def fp9_headline(cosmo_fp6=None):
    """FP9's headline cell as FP9 defines it (L(0.25) = 1.3 Mpc, n = 2, y_th(0.25) = 1e-6, p' = 4) on FP6's background."""
    c6 = cosmo_fp6 or Cosmo("fp6")
    oml = c6.OmL_a(1 / 1.25)
    return dict(L_Lambda=1.3 / oml ** 1.0, n=2.0, y_Lambda=1e-6 * oml ** 4.0, p=4.0)


class HY:
    """H_Y's running constants on a background: L(a) [physical Mpc], its comoving value [Mpc/h], y_th(a)."""

    def __init__(self, cosmo, L_Lambda, n, y_Lambda, p, yield_on=True, bandpass_on=True, kernel="p2", label="H_Y"):
        self.c = cosmo; self.L_Lambda, self.n, self.y_Lambda, self.p = L_Lambda, n, y_Lambda, p
        self.yield_on, self.bandpass_on, self.kernel, self.label = yield_on, bandpass_on, kernel, label

    def L_phys(self, a):
        return self.L_Lambda * self.c.OmL_a(a) ** (self.n / 2.0)

    def L_com(self, a):                                          # comoving Mpc/h
        return self.L_phys(a) * self.c.h / a

    def y_th(self, a):
        return self.y_Lambda * self.c.OmL_a(a) ** (-self.p) if self.yield_on else 0.0

    def hk(self, a, K2):
        if not self.bandpass_on:
            return np.ones_like(K2)
        return -np.expm1(-0.5 * K2 * self.L_com(a) ** 2)

    def prepare(self, box, Fdm, a):                              # H_Y's constants are fixed functions of a
        return None


class HSFrozen(HY):
    """FP13's separator H_S with its COMMITTED readout frozen: L(a) and y_th(a) tabulated by FP13's own functions on its ln a
    grid (L log-interpolated, y_th linearly, as FP13's fun_of), one footing per instance.  The band-pass is closed (h = 0)
    where FP13's L is its floor xi (no root of the variance condition)."""

    def __init__(self, cosmo, lna, L_phys_tab, yth_tab, kernel="p2", label="H_S frozen"):
        self.c = cosmo; self.kernel = kernel; self.label = label
        self.lna = np.asarray(lna, float); self.lL = np.log(np.maximum(np.asarray(L_phys_tab, float), 1e-300))
        self.yt = np.asarray(yth_tab, float)
        self.yield_on, self.bandpass_on = True, True

    def L_phys(self, a):
        return float(np.exp(np.interp(math.log(a), self.lna, self.lL)))

    def y_th(self, a):
        return max(float(np.interp(math.log(a), self.lna, self.yt)), 0.0)


class HSLive(HY):
    """FP13's separator H_S read ON THE FLY from the box's own nonlinear MATTER field (FP13's matter readout; the box average
    stands in for the leaf average <.>_h).  The readout RULES are pluggable (the chain lead's repair of H_S is open: XR18 finds
    FP13's H_S linearly ill-posed at z <= 0.635 as written; candidate repairs fix B by dS/dB = 0, or read the state only through
    <K>_h-type quantities).  A rule receives the box's shell spectrum of delta_m (k^2 values, the variance per shell) and a.
    The defaults are FP13's headline:
        L_rule  'variance': <(S_B delta_m)^2>_box = delta_c^2, S_B = exp(-k^2 L^2/2), i.e. sum_k |delta_k|^2/N^2 exp(-k^2 L^2) =
                delta_c^2 (no root -> the band-pass is closed, FP13's L = xi);
        y_rule  'rms_ramp': c_y <|g_bp|^2>_box^(1/2) / a0 x switch(a), g_bp = (1 - S_L) grad phi_N[delta_m] (physical),
                switch 'ramp' = max(0, 2q) = max(0, 1 + Omega_r - 3 Omega_L) (FP13's headline), 'none' = 1 (FP13's MUTATE).
    WHAT THE BOX DOES NOT CONTAIN: the readout is applied as a prescribed functional; the state term's own variation (the O(1)
    force XR18 finds in the lapse and phi equations, R_B ~ 7-8 on FP13's headline state) is not in the quasi-static operator, so
    the box can neither show nor rule out XR18's ill-posedness.  The box's field is its mesh (CIC) field: modes beyond the mesh and
    below the fundamental are absent -- a resolution systematic of this readout (XR21_s1_hs_readout D3)."""

    def __init__(self, cosmo, a0c, delta_c=3.0 / 20.0 * (12.0 * math.pi) ** (2.0 / 3.0), c_y=1.0, switch="ramp", amp=1.0,
                 kernel="p2", label="H_S live", L_rule=None, y_rule=None):
        self.c = cosmo; self.a0c = a0c; self.delta_c = delta_c; self.c_y = c_y; self.switch = switch; self.amp = amp
        self.kernel = kernel; self.label = label; self.yield_on, self.bandpass_on = True, True
        self.L_rule = L_rule if L_rule is not None else self.L_variance
        self.y_rule = y_rule if y_rule is not None else self.y_rms_ramp
        self._L = 0.0; self._y = 0.0; self.hist = []

    def two_q(self, a):
        E2 = self.c.E(a) ** 2
        return 1.0 + (self.c.Or / a ** 4) / E2 - 3.0 * self.c.OL / E2

    def sw(self, a):
        if self.switch == "none":
            return 1.0
        if self.switch == "step":
            return 1.0 if self.two_q(a) > 0 else 0.0
        return max(0.0, self.two_q(a))

    def L_com(self, a):
        return self._L

    def L_phys(self, a):
        return self._L * a / self.c.h

    def y_th(self, a):
        return self._y

    def hk(self, a, K2):
        if self._L <= 0:
            return np.zeros_like(K2)
        return -np.expm1(-0.5 * K2 * self._L ** 2)

    # ---- the state, and FP13's headline rules
    def shells(self, mesh, Fdm):
        """(k^2 per populated shell, the variance of delta_m per shell, the total variance) from the rfft of delta_m."""
        N = float(mesh.NG) ** 3
        nmax = int(mesh.n2.max()) + 1
        S = np.bincount(mesh.n2.ravel(), weights=(mesh.wr * np.abs(Fdm) ** 2).ravel(), minlength=nmax) / N ** 2
        S[0] = 0.0
        S /= self.amp ** 2
        n2v = np.nonzero(S > 0)[0]
        return mesh.kf ** 2 * n2v, S[n2v], float(S.sum())

    def L_variance(self, k2v, Sv, a, mesh):
        dc2 = self.delta_c ** 2
        if float(Sv.sum()) <= dc2:
            return 0.0
        from scipy.optimize import brentq
        f = lambda R: float(np.sum(Sv * np.exp(-k2v * R * R))) - dc2
        return brentq(f, 1e-8, mesh.L, xtol=1e-12, rtol=1e-12) if f(mesh.L) < 0 else mesh.L

    def y_rms_ramp(self, k2v, Sv, L, a):
        hk2 = (-np.expm1(-0.5 * k2v * L * L)) ** 2
        g2 = float(np.sum(Sv * (1.5 * self.c.Om / (a ** 2)) ** 2 / k2v * hk2))
        return self.c_y * math.sqrt(g2) / self.a0c * self.sw(a)

    def readout(self, mesh, Fdm, a):
        """(L_com, y_th, sigma_unsmoothed) from the rfft of delta_m (box units)."""
        k2v, Sv, s0 = self.shells(mesh, Fdm)
        L = self.L_rule(k2v, Sv, a, mesh)
        y = self.y_rule(k2v, Sv, L, a) if L > 0 else 0.0
        return L, y, math.sqrt(s0)

    def prepare(self, box, Fdm, a):
        self._L, self._y, s0 = self.readout(box.mesh, Fdm, a)
        self.hist.append((a, self._L, self._y, s0))


class HK1(HY):
    """FP19's separator H_K1 (0c18c582f), every read a zero mode of the khronon (per 1/16 pi G, c = 1, alpha = a0/c^2):
        chi = (S_xi - S_B) phi,  B = L^2/2,  L = L_Lambda Omega_L(<K>_h)^(n/2),  Omega_L(<K>_h) = 3 Lambda/<K>_h^2,
        J_Y = J_P2(Y) + 2 y_th sqrt(Y),  y_th = max(0, 1 + Omega_r - 9 Lambda/<K>_h^2) (<K>_h^2/3 - Lambda) L/alpha
                                              = c_y max(0, 2q) 4 pi G rho_bar L/a0 with c_y = 2 (FP19's y_tied).
    FP19's headline: L_Lambda = 2.9 Mpc (physical), n = 2, c_y = 2, P2 kernel.  THE READOUT IN THE BOX: <K>_h is the leaf's mean
    extrinsic curvature; on the box it is 3 H(a) exactly (the box mean of the velocity divergence vanishes on a periodic mesh,
    and FP19 B4 finds the <K>_h channel (v/c)^2-suppressed), so L and y_th are the background functions below, read on the
    separator's own background `sep` (FP6's, with radiation, as FP19) -- they need not equal the box's dynamical background.
    yield_on=False removes the yield floor (y_th = 0 at every epoch; this lane's MUTATE)."""

    def __init__(self, sep, a0c, L_Lambda=2.9, n=2.0, c_y=2.0, yield_on=True, kernel="p2", label="H_K1"):
        self.c = sep; self.a0c = a0c; self.L_Lambda, self.n, self.c_y = L_Lambda, n, c_y
        self.yield_on, self.bandpass_on, self.kernel, self.label = yield_on, True, kernel, label

    def K2_over_9H02(self, a):                                  # <K>_h^2 / (9 H0^2) = E(a)^2 on FRW
        return self.c.E(a) ** 2

    def OmL_K(self, a):                                         # 3 Lambda/<K>_h^2 = Omega_L(a)
        return self.c.OL / self.K2_over_9H02(a)

    def two_q(self, a):                                         # 1 + Omega_r(a) - 9 Lambda/<K>_h^2 = 2q
        return 1.0 + (self.c.Or / a ** 4) / self.K2_over_9H02(a) - 3.0 * self.OmL_K(a)

    def L_phys(self, a):                                        # physical Mpc
        return self.L_Lambda * self.OmL_K(a) ** (self.n / 2.0)

    def y_th(self, a):
        if not self.yield_on:
            return 0.0
        fourpiGrho = 1.5 * (self.c.Om / a ** 3 + self.c.Or / a ** 4)            # 4 pi G rho_bar in H0^2 units
        return self.c_y * max(0.0, self.two_q(a)) * fourpiGrho * self.L_phys(a) * self.c.h / self.a0c


def X_p2(D):
    """P2's scalar field law with the yield: phantom field / a0 = sqrt(D^2 + D) - D for D > 0, else 0 (stable form)."""
    D = np.asarray(D, dtype=np.float64)
    out = np.zeros_like(D)
    m = D > 0
    Dm = D[m]
    out[m] = 1.0 / (1.0 + np.sqrt(1.0 + 1.0 / Dm))
    return out


_MONO = {}


def _mono_table():
    if not _MONO:
        from scipy.optimize import brentq
        def h_rar(y):
            y = np.asarray(y, float)
            with np.errstate(over="ignore"):
                return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
        def dh_rar(y, e=1e-6):
            return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
        YP = brentq(lambda y: float(dh_rar(y)), 1, 5); HP = float(h_rar(YP))
        LYG = np.linspace(-14, 14, 280001); YG = 10 ** LYG; DH = np.maximum(dh_rar(YG), 0.05 * HP / (YG + YP))
        HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])
        _MONO.update(LYG=LYG, HM=HM)
    return _MONO


def X_mono(D):
    """nu_mono's field law (FP6/L377 construction): phantom / a0 = D (nu_mono(D) - 1) = h_mono(D) for D > 0, else 0."""
    t = _mono_table(); D = np.asarray(D, dtype=np.float64)
    out = np.zeros_like(D); m = D > 0
    out[m] = np.interp(np.log10(np.maximum(D[m], 1e-14)), t["LYG"], t["HM"])
    return out


def X_law(D, kernel="p2"):
    return X_p2(D) if kernel == "p2" else X_mono(D)


# ============================================================================================= the mesh
class Mesh:
    """periodic mesh with the record's operations (L362's Sim: continuous-k^2 Poisson, centred-difference gradient, CIC)
    and fast primitives (bincount deposit, flat-index gather, real FFTs with `workers` threads)."""

    def __init__(self, L, NG, workers=1, threads=1):
        self.L, self.NG = float(L), int(NG); self.d = self.L / self.NG; self.kf = 2 * np.pi / self.L
        self.workers = int(workers); self.threads = int(threads)            # FFT threads; particle-chunk threads
        self.k1 = (np.fft.fftfreq(self.NG, d=self.d) * 2 * np.pi)              # full axis (L362's convention)
        self.kr = (np.fft.rfftfreq(self.NG, d=self.d) * 2 * np.pi)             # half axis
        K2 = self.k1[:, None, None] ** 2 + self.k1[None, :, None] ** 2 + self.kr[None, None, :] ** 2
        K2[0, 0, 0] = 1.0
        self.K2 = K2                                                           # rfft layout (L362: K2[0,0,0] = 1)
        self._n2 = None; self._wr = None
        self.kz1 = np.abs(np.fft.fftfreq(self.NG, d=self.d) * 2 * np.pi)

    @property
    def n2(self):                                                              # integer shell index n^2 (built on demand)
        if self._n2 is None:
            n1 = np.rint(np.fft.fftfreq(self.NG) * self.NG).astype(np.int64)
            nr = np.rint(np.fft.rfftfreq(self.NG) * self.NG).astype(np.int64)
            self._n2 = (n1[:, None, None] ** 2 + n1[None, :, None] ** 2 + nr[None, None, :] ** 2).astype(np.int64)
        return self._n2

    @property
    def wr(self):                                                              # Hermitian multiplicity of each rfft cell
        if self._wr is None:
            w = np.full(self.K2.shape, 2.0); w[:, :, 0] = 1.0
            if self.NG % 2 == 0:
                w[:, :, -1] = 1.0
            self._wr = w
        return self._wr

    # ---- FFTs
    def rfft(self, f):
        return sfft.rfftn(f, workers=self.workers)

    def irfft(self, F):
        return sfft.irfftn(F, s=(self.NG,) * 3, workers=self.workers)

    def poisson(self, src):
        F = self.rfft(src); F = -F / self.K2; F[0, 0, 0] = 0.0
        return self.irfft(F)

    def grad(self, f):
        return [self.grad_axis(f, i) for i in range(3)]

    def div(self, v):
        """L362's sum of centred differences (0 + t_x + t_y + t_z)."""
        out = self.grad_axis(v[0], 0)
        for i in (1, 2):
            out += self.grad_axis(v[i], i)
        return out

    def smooth(self, f, R):
        return self.irfft(self.rfft(f) * np.exp(-0.5 * self.K2 * R ** 2)) if R > 0 else f

    # ---- CIC (L362's _cic arithmetic), processed in particle chunks (no per-step cache: bounded transient memory)
    CHUNK = 1 << 20

    def _corners(self, x):
        NG = self.NG
        g = x / self.d; i0 = np.floor(g); f = g - i0; del g
        i0 = i0.astype(np.int64); i0 %= NG; i1 = i0 + 1; i1 %= NG
        for dx in (0, 1):
            wx = f[:, 0] if dx else 1 - f[:, 0]; ix = i1[:, 0] if dx else i0[:, 0]
            for dy in (0, 1):
                wy = f[:, 1] if dy else 1 - f[:, 1]; iy = i1[:, 1] if dy else i0[:, 1]
                for dz in (0, 1):
                    wz = f[:, 2] if dz else 1 - f[:, 2]; iz = i1[:, 2] if dz else i0[:, 2]
                    yield (ix * NG + iy) * NG + iz, wx, wy, wz

    def cic(self, x):                                            # kept for API compatibility: no cache is built
        return None

    def deposit(self, x, w, cic=None):
        """CIC deposit (L366's bincount form).  With self.threads > 1 the particle chunks run in a thread pool (numpy releases the
        GIL) and their meshes are summed in chunk order: deterministic, but not bit-identical to the one-thread sum."""
        NG = self.NG
        w = np.broadcast_to(np.asarray(w, dtype=np.float64), (len(x),))
        chunks = [(s0, min(s0 + self.CHUNK, len(x))) for s0 in range(0, len(x), self.CHUNK)]

        def one(c_):
            s0, s1 = c_; xs = x[s0:s1]; ws = w[s0:s1]; r = np.zeros(NG ** 3)
            for ii, wx, wy, wz in self._corners(xs):
                r += np.bincount(ii, weights=ws * wx * wy * wz, minlength=NG ** 3)
            return r
        if self.threads > 1 and len(chunks) > 1:
            from concurrent.futures import ThreadPoolExecutor
            rho = np.zeros(NG ** 3)
            with ThreadPoolExecutor(self.threads) as ex:
                for j in range(0, len(chunks), self.threads):              # bounded memory: one batch of meshes at a time
                    for r in ex.map(one, chunks[j:j + self.threads]):
                        rho += r
            return rho.reshape(NG, NG, NG)
        rho = np.zeros(NG ** 3)
        for s0 in range(0, len(x), self.CHUNK):
            xs = x[s0:s0 + self.CHUNK]; ws = w[s0:s0 + self.CHUNK]
            for ii, wx, wy, wz in self._corners(xs):
                rho += np.bincount(ii, weights=ws * wx * wy * wz, minlength=NG ** 3)
        return rho.reshape(NG, NG, NG)

    def interp(self, fields, x, cic=None):
        """gather one field or a list of fields at the particles (L362's arithmetic: field[...] * wx * wy * wz, summed);
        per-particle arithmetic is identical with threads (chunks are independent)."""
        single = not isinstance(fields, (list, tuple))
        flist = [fields] if single else list(fields)
        outs = [np.zeros(len(x)) for _ in flist]
        flat = [np.ascontiguousarray(f).reshape(-1) for f in flist]

        def one(s0):
            xs = x[s0:s0 + self.CHUNK]
            for ii, wx, wy, wz in self._corners(xs):
                for o, ff in zip(outs, flat):
                    o[s0:s0 + len(xs)] += ff[ii] * wx * wy * wz
        starts = list(range(0, len(x), self.CHUNK))
        if self.threads > 1 and len(starts) > 1:
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(self.threads) as ex:
                list(ex.map(one, starts))
        else:
            for s0 in starts:
                one(s0)
        return outs[0] if single else outs

    def grad_axis(self, f, i):
        """L362's (roll(f, -1, i) - roll(f, 1, i)) / (2 d), computed without the two rolled copies (same arithmetic)."""
        out = np.empty_like(f)
        def sl(s):
            return tuple(s if j == i else slice(None) for j in range(3))
        np.subtract(f[sl(slice(2, None))], f[sl(slice(None, -2))], out=out[sl(slice(1, -1))])
        np.subtract(f[sl(slice(1, 2))], f[sl(slice(-1, None))], out=out[sl(slice(0, 1))])
        np.subtract(f[sl(slice(0, 1))], f[sl(slice(-2, -1))], out=out[sl(slice(-1, None))])
        out /= (2 * self.d)
        return out

    def force_at(self, phi, x, cic=None):
        """-grad phi (centred differences, L362) gathered at the particles in one pass over the CIC corners."""
        base = cic if cic is not None else self.cic(x)
        g = [self.grad_axis(phi, i) for i in range(3)]
        out = self.interp(g, x, base)
        del g
        return -np.stack(out, 1)

    # ---- power spectra (the record's estimators, full-FFT normalisation)
    def power_shells(self, delta):
        """|delta_k|^2 L^3 / NG^6 averaged on exact shells n^2 (all modes; Hermitian weights); returns (k, P, Nmodes)."""
        F = self.rfft(delta); Pw = (np.abs(F) ** 2) * (self.L ** 3) / self.NG ** 6
        nmax = int(self.n2.max()) + 1
        num = np.bincount(self.n2.ravel(), weights=(Pw * self.wr).ravel(), minlength=nmax)
        den = np.bincount(self.n2.ravel(), weights=self.wr.ravel(), minlength=nmax)
        ok = den > 0; ok[0] = False
        n2v = np.nonzero(ok)[0]
        return self.kf * np.sqrt(n2v), num[ok] / den[ok], den[ok]

    def pk_bins(self, delta, KG):
        """L367's estimator exactly: mean |FFT(delta)_k|^2 (unnormalised, full FFT) in 0.8 q - 1.2 q (ratios are used)."""
        f = np.fft.fftn(delta); Pw = np.abs(f) ** 2
        k1 = self.k1
        kk = np.sqrt(k1[:, None, None] ** 2 + k1[None, :, None] ** 2 + k1[None, None, :] ** 2)
        return {q: float(Pw[(kk >= 0.8 * q) & (kk <= 1.2 * q)].mean()) for q in KG}

    def pk_log(self, delta, nb=14, kmin=0.15, kmax=4.0):
        """L346's estimator: log bins 0.15-4.0 h/Mpc, |delta_k|^2 L^3 / NG^6 (full FFT); rows (k_centre, P)."""
        f = np.fft.fftn(delta); Pw = np.abs(f) ** 2 * (self.L ** 3) / self.NG ** 6
        k1 = self.k1
        kk = np.sqrt(k1[:, None, None] ** 2 + k1[None, :, None] ** 2 + k1[None, None, :] ** 2); kk[0, 0, 0] = 0
        edges = np.geomspace(kmin, kmax, nb + 1); out = []
        for i in range(nb):
            m = (kk >= edges[i]) & (kk < edges[i + 1])
            out.append((float(np.sqrt(edges[i] * edges[i + 1])), float(Pw[m].mean()) if m.any() else float("nan")))
        return out

    def sigma8(self, delta):
        """L366's estimator (full FFT, top hat of 8 Mpc/h on the mesh power)."""
        f = np.fft.fftn(delta); Pw = np.abs(f) ** 2 / self.NG ** 6
        k1 = self.k1
        kk = np.sqrt(k1[:, None, None] ** 2 + k1[None, :, None] ** 2 + k1[None, None, :] ** 2); kk[0, 0, 0] = 0
        x = kk * 8.0
        with np.errstate(divide="ignore", invalid="ignore"):
            W = np.where(x > 0, 3 * (np.sin(x) - x * np.cos(x)) / np.maximum(x, 1e-12) ** 3, 1.0)
        W[0, 0, 0] = 0.0
        return float(np.sqrt(np.sum(Pw * W ** 2)))


# ============================================================================================= the forest (L347/L362 FGPA)
FLUX = dict(BETA=1.6, RJ=0.1, BTH=13.5)
TAU_EFF = {3.0: 0.751 * (4.0 / 4.5) ** 2.90 - 0.132, 2.0: 0.751 * (3.0 / 4.5) ** 2.90 - 0.132,
           2.5: 0.751 * (3.5 / 4.5) ** 2.90 - 0.132}


def flux_p1d(mesh, cosmo, x, p, a, z, w=None):
    """L362's Sim.flux_p1d (FGPA: gas = the given particles smoothed on R_J = 0.1 Mpc/h, tau ~ delta_gas^1.6, redshift-space
    mapping by the mass-weighted velocity, thermal broadening b = 13.5 km/s, A fixed by Becker+13 tau_eff), with bincount in
    place of np.add.at.  w = particle masses (None: equal, as the record)."""
    from scipy.optimize import brentq
    NG = mesh.NG; npart = len(x)
    ww = np.ones(npart) if w is None else np.asarray(w, float) * npart / np.sum(w)
    c = mesh.cic(x)
    rho = mesh.deposit(x, ww, c) * NG ** 3 / npart
    mom = mesh.deposit(x, ww * p[:, 2], c) * NG ** 3 / npart
    vz = np.where(rho > 0, mom / np.maximum(rho, 1e-12), 0.0) / a
    dgas = np.maximum(mesh.irfft(mesh.rfft(rho) * np.exp(-0.5 * mesh.K2 * FLUX["RJ"] ** 2)), 1e-6)
    tau_r = dgas ** FLUX["BETA"]
    shift = vz / (a * cosmo.E(a))
    zpos = (np.arange(NG) * mesh.d)[None, None, :] + shift
    g = (zpos % mesh.L) / mesh.d; j0 = np.floor(g).astype(np.int64); fr = g - j0; j0 %= NG; j1 = (j0 + 1) % NG
    I = np.arange(NG)[:, None, None]; J = np.arange(NG)[None, :, None]
    base = (I * NG + J) * NG
    tau_s = np.bincount((base + j0).ravel(), weights=(tau_r * (1 - fr)).ravel(), minlength=NG ** 3)
    tau_s += np.bincount((base + j1).ravel(), weights=(tau_r * fr).ravel(), minlength=NG ** 3)
    tau_s = tau_s.reshape(NG, NG, NG)
    sig = (FLUX["BTH"] / math.sqrt(2)) / (100.0 * cosmo.E(a) * a)
    tau_s = np.real(np.fft.ifft(np.fft.fft(tau_s, axis=2) * np.exp(-0.5 * (mesh.kz1 * sig) ** 2)[None, None, :], axis=2))
    tau_s = np.maximum(tau_s, 0.0)
    Fbar_t = math.exp(-TAU_EFF[z])
    A = brentq(lambda A_: float(np.mean(np.exp(-A_ * tau_s))) - Fbar_t, 1e-6, 1e3)
    F = np.exp(-A * tau_s); dF = F / F.mean() - 1
    Pk1 = np.mean(np.abs(np.fft.fft(dF, axis=2)) ** 2, axis=(0, 1)) * mesh.L / NG ** 2
    kpar = np.fft.fftfreq(NG, d=mesh.d)[:NG // 2] * 2 * np.pi
    return kpar[1:], Pk1[1:NG // 2]


# ============================================================================================= initial conditions
def lattice(NP, L):
    q = (np.arange(NP) + 0.5) * L / NP
    QX, QY, QZ = np.meshgrid(q, q, q, indexing="ij")
    return np.stack([QX.ravel(), QY.ravel(), QZ.ravel()], 1)


def za_ics(mesh, cosmo, NP, zi, Pfun, seed, kmax_clip=60.0, fixed_amp=False, amp=1.0, growth_rate="record"):
    """the record's Zel'dovich ICs (L362 run(): white noise from default_rng(seed), delta0 = ifft(white sqrt(P NG^3/L^3)),
    psi = -grad poisson(delta0) (centred differences), CIC onto the particle lattice, p = a^2 H f psi).
    Pfun(k) = P_lin(k, z_i) [(Mpc/h)^3]; evaluated once per exact shell n^2 (bit-identical to evaluating it cell by cell).
    fixed_amp: |white_k| set to its rms (phases kept) -- for the linear-regime tests.  amp scales delta (linear boxes).
    growth_rate: 'record' = Omega_m(a)^0.55 (L362), 'ode' = the background's exact f."""
    NG, L = mesh.NG, mesh.L
    rng = np.random.default_rng(seed)
    white = mesh.rfft(rng.normal(size=(NG, NG, NG)))
    if fixed_amp:
        white = white / np.maximum(np.abs(white), 1e-300) * math.sqrt(NG ** 3)
    n2u, inv = np.unique(mesh.n2, return_inverse=True)
    ku = np.clip(mesh.kf * np.sqrt(n2u.astype(float)), mesh.kf, kmax_clip)
    Pu = np.array([Pfun(float(q)) for q in ku]); Pu[n2u == 0] = 0.0
    Pk = Pu[inv].reshape(mesh.n2.shape)
    delta0 = mesh.irfft(white * np.sqrt(Pk * NG ** 3 / L ** 3)) * amp
    del white, Pk
    phi0 = mesh.poisson(delta0)
    Q = lattice(NP, L)
    base = mesh.cic(Q)
    disp = np.empty((len(Q), 3))
    for i in range(3):                                          # psi = -grad poisson(delta0), one component at a time
        psi_i = mesh.grad_axis(phi0, i); psi_i *= -1.0
        disp[:, i] = mesh.interp(psi_i, Q, base); del psi_i
    del base, phi0
    ai = 1.0 / (1.0 + zi)
    fg = cosmo.Om_a(ai) ** 0.55 if growth_rate == "record" else cosmo.f(ai)
    x = (Q + disp) % L
    p = ai ** 2 * cosmo.E(ai) * fg * disp
    return x, p, delta0


# ============================================================================================= EPS sub-grid machinery
class SubGrid:
    """extended Press-Schechter conditional collapsed fraction in M_min < M < M_up(z) for each mesh cell."""

    def __init__(self, cosmo, P0fun, cell_vol, delta_t0, picture="cap", kmin=1e-4, kmax=500.0, kclip=50.0):
        self.c, self.Vc, self.dt0, self.picture = cosmo, cell_vol, delta_t0, picture
        self.rho_m = 2.775e11 * cosmo.Om                           # h^2 Msun / Mpc^3  (Msun/h per (Mpc/h)^3)
        lk = np.linspace(math.log(kmin), math.log(kmax), 6000); kk = np.exp(lk)
        kcl = min(kmax, kclip)                                  # the linear-spectrum table's own limit (CLASS: 60 h/Mpc)
        kin = kk[kk <= kcl]; Pin = np.array([P0fun(float(k)) for k in kin])
        slope = (math.log(Pin[-1]) - math.log(Pin[-40])) / (math.log(kin[-1]) - math.log(kin[-40]))
        Pk = np.concatenate([Pin, Pin[-1] * (kk[kk > kcl] / kin[-1]) ** slope])   # power-law tail beyond the table (labelled)
        self.tail_slope = slope
        lM = np.linspace(math.log(1e4), math.log(1e17), 700); self.lM = lM
        R = (3 * np.exp(lM) / (4 * np.pi * self.rho_m)) ** (1 / 3)
        x = np.outer(R, kk)
        with np.errstate(divide="ignore", invalid="ignore"):
            W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
        self.S0 = np.trapz(kk ** 3 * Pk * W ** 2, lk, axis=1) / (2 * np.pi ** 2)     # sigma^2(M) at z = 0

    def S(self, M):
        return np.interp(np.log(M), self.lM, self.S0)

    def delta_t(self, a):
        z = 1 / a - 1
        return self.dt0 * self.c.E(a) ** 4 / (1 + z) ** 3

    def M_up(self, a):
        return self.delta_t(a) * self.rho_m * self.Vc

    def Delta_vir(self, a):                                     # Bryan & Norman 1998, in units of the mean matter density
        om = self.c.Om_a(a); xx = om - 1
        return (18 * math.pi ** 2 + 82 * xx - 39 * xx ** 2) / om

    def share(self, a):
        return max(0.0, 1.0 - self.delta_t(a) / self.Delta_vir(a)) if self.picture == "cap" else 1.0

    @staticmethod
    def delta_lin(dnl):
        """Mo & White 1996, eq. 18: the linear overdensity of a spherical region with nonlinear overdensity dnl."""
        y = 1.0 + np.maximum(dnl, -0.99)
        return 1.68647 - 1.35 * y ** (-2 / 3) - 1.12431 * y ** (-0.5) + 0.78785 * y ** (-0.58661)

    def f_sg(self, dnl, a, M_min, M_up=None):
        """the sub-grid converted share of a cell's heavy fluid (cap/cleared share included)."""
        Mup = self.M_up(a) if M_up is None else M_up
        D = self.c.D(a); dc = 1.686
        dl = self.delta_lin(dnl)
        MR = self.rho_m * (1 + np.maximum(dnl, -0.99)) * self.Vc
        SR = self.S(MR)
        def F(Mx):
            Sx = self.S(np.full_like(MR, Mx))
            var = np.maximum(Sx - SR, 1e-12) * D ** 2
            out = erfc(np.maximum(dc - dl, 0.0) / np.sqrt(2 * var))
            return np.where(MR > Mx, out, 0.0)
        if Mup <= M_min:
            return np.zeros_like(dnl)
        Fmin = np.where(dl >= dc, 1.0, F(M_min))
        Fup = np.where(dl >= dc, 1.0, F(Mup))
        return np.clip(Fmin - Fup, 0.0, 1.0) * self.share(a)

    # ---- the mesh's own detection function (the seamless hand-over between the sub-grid term and the mesh trigger)
    @staticmethod
    def c_dm14(M_h, z):
        """Dutton & Maccio 2014 (Planck) c_200(M, z), M in Msun/h, floored at 3 (XR16's floor for the fit's high-z tail)."""
        aa = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); bb = -0.101 + 0.026 * z
        return max(3.0, 10 ** (aa + bb * math.log10(M_h / 1e12)))

    def clump_share(self, M_h, a, c=None):
        """the exact above-threshold share of a truncated NFW clump on the mean background (cap: int (rho - rho_t)_+ dV / M;
        cleared: int_{rho > rho_t} rho dV / M, the background inside included)."""
        z = 1 / a - 1; c = self.c_dm14(M_h, z) if c is None else c
        dv = self.Delta_vir(a); rv = (3 * M_h / (4 * math.pi * dv * self.rho_m)) ** (1 / 3); rs = rv / c
        mf = lambda y: math.log1p(y) - y / (1 + y)
        rhos = M_h / (4 * math.pi * rs ** 3 * mf(c)) / self.rho_m
        rt = self.delta_t(a)
        prof = lambda r: rhos / ((r / rs) * (1 + r / rs) ** 2) + 1.0
        if self.picture == "cap":
            val = quad(lambda r: max(prof(r) - rt, 0.0) * 4 * math.pi * r * r, 0, rv, limit=400, points=[rs])[0]
        else:
            val = quad(lambda r: prof(r) * 4 * math.pi * r * r if prof(r) > rt else 0.0, 0, rv, limit=400, points=[rs])[0]
        return val / (M_h / self.rho_m), rv, c

    def detection(self, a, d, nM=40, noff=48, npts=6000, seed=3):
        """f_seen(M): the share of an isolated NFW clump (mass M, DM14 concentration) the MESH trigger converts in one shot at
        cell size d (comoving Mpc/h): the clump sampled with npts points at a random sub-cell offset on the mean background,
        CIC-deposited on a local patch, the density read back at each point by CIC (the box's own trigger arithmetic), cap:
        mean (1 - rho_t/rho)_+, cleared: mean 1(rho > rho_t).  Clumps with r_vir >= 4 d are resolved: f_seen = the exact share
        (T5a verifies both regimes against real particles in a box).  Returns (lnM grid, f_seen, share)."""
        rng = np.random.default_rng(seed)
        rt = self.delta_t(a); z = 1 / a - 1
        M1 = rt * self.rho_m * d ** 3                                    # the mass that lifts one cell to the threshold
        Ms = np.exp(np.linspace(math.log(0.2 * M1), math.log(max(3e3 * M1, 1e16)), nM))
        fs, sh, es = [], [], []
        mf = lambda y: np.log1p(y) - y / (1 + y)
        for M in Ms:
            share, rv, c = self.clump_share(M, a)
            sh.append(share)
            if rv >= 4 * d:
                fs.append(share); es.append(0.0); continue
            npat = int(2 * math.ceil(rv / d) + 6)
            xg = np.linspace(1e-6, c, 20001); cdf = mf(xg) / mf(c)
            nq = int(max(npts, 20 * M / M1))                            # points light enough not to trigger by themselves
            vals = []
            for _ in range(noff):
                u = rng.random(nq); r = np.interp(u, cdf, xg) * rv / c
                v = rng.normal(size=(nq, 3)); v /= np.linalg.norm(v, axis=1)[:, None]
                pos = r[:, None] * v + (npat // 2 + rng.random(3)) * d
                g = pos / d; i0 = np.floor(g).astype(np.int64); f = g - i0
                rho = np.zeros((npat,) * 3); wgt = (M / nq) / (self.rho_m * d ** 3)            # units of the mean
                for dx in (0, 1):
                    for dy in (0, 1):
                        for dz in (0, 1):
                            w = (f[:, 0] if dx else 1 - f[:, 0]) * (f[:, 1] if dy else 1 - f[:, 1]) * (f[:, 2] if dz else 1 - f[:, 2])
                            np.add.at(rho, ((i0[:, 0] + dx) % npat, (i0[:, 1] + dy) % npat, (i0[:, 2] + dz) % npat), wgt * w)
                rho += 1.0
                rp = np.zeros(nq)
                for dx in (0, 1):
                    for dy in (0, 1):
                        for dz in (0, 1):
                            w = (f[:, 0] if dx else 1 - f[:, 0]) * (f[:, 1] if dy else 1 - f[:, 1]) * (f[:, 2] if dz else 1 - f[:, 2])
                            rp += rho[(i0[:, 0] + dx) % npat, (i0[:, 1] + dy) % npat, (i0[:, 2] + dz) % npat] * w
                vals.append(float(np.mean(np.maximum(1 - rt / rp, 0.0))) if self.picture == "cap" else float(np.mean(rp > rt)))
            fs.append(min(float(np.mean(vals)), share)); es.append(float(np.std(vals) / math.sqrt(len(vals))))
        return np.log(Ms), np.array(fs), np.array(sh), np.array(es)

    def f_sg_seamless(self, dnl, a, M_min, det, nsub=48):
        """the sub-grid share with the seamless hand-over: int_{M_min}^{M_R} dF(>M | cell) [share(M) - f_seen(M)]_+ -- each clump
        contributes the part the mesh trigger does not already convert (f_seen from detection(); 0 below its grid, the exact
        share above: resolved clumps are the mesh's alone)."""
        lMg, fsg, shg = det[0], det[1], det[2]
        D = self.c.D(a); dc = 1.686
        dl = self.delta_lin(dnl)
        MR = self.rho_m * (1 + np.maximum(dnl, -0.99)) * self.Vc
        SR = self.S(MR)
        lMtop = lMg[-1]
        grid = np.linspace(math.log(M_min), max(lMtop, math.log(M_min) + 1e-6), nsub + 1)
        wmid = np.interp(0.5 * (grid[1:] + grid[:-1]), lMg, np.maximum(shg - fsg, 0.0), left=float(max(shg[0] - 0.0, 0.0)), right=0.0)

        def F(lMx):
            Mx = math.exp(lMx)
            var = np.maximum(self.S(np.full_like(MR, Mx)) - SR, 1e-12) * D ** 2
            return np.where(MR > Mx, erfc(np.maximum(dc - dl, 0.0) / np.sqrt(2 * var)), 0.0)
        out = np.zeros_like(dnl, dtype=float); Fprev = F(grid[0])
        for j in range(nsub):
            Fn = F(grid[j + 1]); out += (Fprev - Fn) * wmid[j]; Fprev = Fn
        out = np.where(dl >= dc, 0.0, out)                     # a cell collapsed as a whole is the mesh's (resolved)
        return np.clip(out, 0.0, 1.0)


# ============================================================================================= the H_Y operator
def hy_phantom(m, hy, cosmo, src_delta, a, a0_scale, want_dph=False):
    """THE H_Y PHANTOM on the mesh (QUMOND-type approximation of FP7's AQUAL root with FP9's separator):
        phi_ph = B u,  lap u = div_c[ C^Q(y) G ],  G = grad_c(B phi_N[src]),  y = |G| / (a a0),  C^Q y = X(y - y_th),
    B = 1 - exp(-k^2 L_c^2 / 2) (xi -> 0), grad_c/div_c the record's centred differences, Poisson spectral.
    src_delta: the source's density perturbation in units of the mean total matter density; a0_scale = a0 in code units
    (x the amplitude factor of a linear box).  Returns (phi_ph, delta_ph or None, diagnostics).  In-place arithmetic."""
    hk = hy.hk(a, m.K2)
    F = m.rfft(src_delta)
    F *= hk; F *= -(1.5 * cosmo.Om / a); F /= m.K2; F[0, 0, 0] = 0.0                       # B phi_N[src] in k-space
    phib = m.irfft(F); del F
    G = [m.grad_axis(phib, i) for i in range(3)]; del phib                                  # comoving gradient
    Gm2 = G[0] * G[0]; Gm2 += G[1] * G[1]; Gm2 += G[2] * G[2]
    Gm = np.sqrt(Gm2)
    scale = a * a0_scale
    yth = hy.y_th(a)
    D = Gm / scale; D -= yth                                                                 # y - y_th
    on_frac = float(np.mean(D > 0))
    fac = X_law(D, hy.kernel); del D                                                         # X(y - y_th) = C^Q y
    fac *= scale; np.maximum(Gm, 1e-300, out=Gm); fac /= Gm; del Gm                        # C^Q
    sum_g2 = float(Gm2.sum())
    diag = dict(y_rms=math.sqrt(sum_g2 / Gm2.size) / scale, y_th=float(yth), on_frac=on_frac,
                L_com=float(hy.L_com(a)), cbar=float(np.sum(fac * Gm2)) / max(sum_g2, 1e-300))
    del Gm2
    for g in G:
        g *= fac                                                                             # W = C^Q G
    del fac
    dW = m.div(G); del G
    FdW = m.rfft(dW); del dW
    FdW *= hk
    dph = m.irfft(FdW) * (a / (1.5 * cosmo.Om)) if want_dph else None
    FdW /= m.K2; FdW *= -1.0; FdW[0, 0, 0] = 0.0
    phi_ph = m.irfft(FdW); del FdW
    return phi_ph, dph, diag


# ============================================================================================= the box
class Box:
    """one particle-mesh box.  species: 'b' baryons (single particle mass), 'd' the dark fluid (masses, heavy/light state).
    mode: 'single' -- one species carries all the matter (the record's L346/L362 PM and FP9's one-fluid yardstick);
          'two'    -- baryons + dark fluid on the same Lagrangian lattice (L366).
    gravity: 'newton' | 'hy' (the real-space H_Y operator, QUMOND-type approximation) | 'hy_permode' (FP9's per-mode
             yardstick rule as a k-space multiplier on phi_N: a CONTROL operator, not the model) .
    reading: 'chain' | 'fp9' (see the module docstring)."""

    def __init__(self, L, NG, NP, cosmo, zi=49.0, seed=7, mode="two", gravity="newton", reading="chain", hy=None,
                 foot="canonical", Pfun=None, workers=1, fixed_amp=False, amp=1.0, growth_rate="record",
                 kmax_clip=60.0, conversion=None, subgrid=None, rng_seed=11, ic_NG=None, threads=1):
        self.mesh = Mesh(L, NG, workers, threads); self.c = cosmo; self.NP = NP; self.mode = mode
        self.gravity, self.reading, self.hy, self.foot = gravity, reading, hy, foot
        self.a0c = cosmo.a0_code(foot); self.amp = amp
        self.a = 1.0 / (1.0 + zi); self.zi = zi
        mesh_ic = self.mesh if (ic_NG is None or ic_NG == NG) else Mesh(L, ic_NG, workers)     # the realisation's own mesh
        x, p, _ = za_ics(mesh_ic, cosmo, NP, zi, Pfun, seed, kmax_clip, fixed_amp, amp, growth_rate)
        del mesh_ic
        n = len(x)
        if mode == "single":
            self.xb, self.pb = x, p; self.mb = 1.0 / n
            self.xd = np.zeros((0, 3)); self.pd = np.zeros((0, 3)); self.md = np.zeros(0); self.sd = np.zeros(0, np.int8)
        else:
            fb = cosmo.fb
            self.xb, self.pb = x, p; self.mb = fb / n
            self.xd, self.pd = x.copy(), p.copy(); self.md = np.full(n, (1 - fb) / n); self.sd = np.zeros(n, np.int8)
        self.rng = np.random.default_rng(rng_seed)
        self.ud = self.rng.random(len(self.xd))                  # the sub-grid threshold numbers (fixed per heavy particle)
        self.conv = conversion                                   # None or dict(delta_t0, Gamma0, picture, vk)
        self.sg = subgrid                                        # None or dict(obj=SubGrid, M_min)
        self.log = {"converted_mass": [], "events": 0}
        self.audit = None                                        # a dict turns on the conversion's exact bookkeeping audit
        self.diag = {}
        self.permode_state = None

    # ---------------------------------------------------------------- densities (units of the mean total matter density)
    def densities(self):
        NG = self.mesh.NG
        self.cb = self.mesh.cic(self.xb)
        rb = self.mesh.deposit(self.xb, self.mb, self.cb) * NG ** 3
        if len(self.xd):
            self.cd = self.mesh.cic(self.xd)
            rd = self.mesh.deposit(self.xd, self.md, self.cd) * NG ** 3
        else:
            self.cd = None; rd = np.zeros_like(rb)
        return rb, rd

    # ---------------------------------------------------------------- the H_Y phantom (real space, QUMOND-type approximation)
    def phantom(self, src_delta, a, want_dph=False):
        return hy_phantom(self.mesh, self.hy, self.c, src_delta, a, self.a0c * self.amp, want_dph)

    # ---------------------------------------------------------------- FP9's per-mode rule (CONTROL operator, k-space)
    def permode_multiplier(self, delta_tot, a):
        """FP9 growth_aq's per-mode rule on the box's own spectrum: C_eff(k) = C^Q(y_k) h_k^2 w_k, y_k = g_k h_k / a0 with
        g_k = (3/2) Om Delta(k) / (a^2 k) from the box's shell-averaged power (physical amplitude = box / amp), and FP9's
        tracking weight w = 1/(1 + (H/(c_s k))^2), c_s = c / sqrt(C^Q (2 + 3 c_2) h^2 / c_2), c_2 = 7.3e-3 (lambda = 0)."""
        m, hy, c = self.mesh, self.hy, self.c
        k, Pk, _ = m.power_shells(delta_tot)
        Delta = np.sqrt(k ** 3 * Pk / (2 * np.pi ** 2)) / self.amp
        hk_s = hy.hk(a, k ** 2)
        gk = 1.5 * c.Om * Delta / (a ** 2 * k)
        yk = gk * hk_s / self.a0c
        yth = hy.y_th(a)
        CQ = np.where(yk > 0, X_law(yk - yth, hy.kernel) / np.maximum(yk, 1e-300), 0.0)
        c2 = 7.3e-3
        lam_phi = (2 + 3 * c2) * hk_s ** 2 / c2
        cs = C_KMS / np.sqrt(np.maximum(CQ, 1e-300) * np.maximum(lam_phi, 1e-300))           # km/s
        kphys = k / a                                                                         # h/Mpc physical
        Hz = 100.0 * c.E(a)                                                                   # h km/s/Mpc
        wt = 1.0 / (1.0 + (Hz / (cs * kphys)) ** 2)
        Ce = np.maximum(CQ * hk_s ** 2 * wt, 0.0)
        n2v = np.rint((k / m.kf) ** 2).astype(np.int64)
        table = np.zeros(int(m.n2.max()) + 1); table[n2v] = Ce
        return table[m.n2], dict(k=k, Ce=Ce, yk=yk, wt=wt)

    # ---------------------------------------------------------------- forces
    def source(self, rb, rho):
        """the kernel's source perturbation (units of the mean total matter density) for this box's reading."""
        if self.reading == "chain" and self.mode == "two":
            return rb - self.c.fb
        return rho - 1.0

    def forces(self, a):
        m, c = self.mesh, self.c
        if self.gravity == "none":                               # a force-free box (ballistic control)
            return np.zeros_like(self.xb), np.zeros_like(self.xd)
        rb, rd = self.densities()
        rho = rb + rd; del rd
        Fd = m.rfft(rho - 1.0)
        if self.hy is not None and self.gravity in ("hy", "hy_permode"):
            self.hy.prepare(self, Fd, a)                          # H_S live reads the matter field here (a no-op otherwise)
        FphiN = Fd * (-(1.5 * c.Om / a) / m.K2); FphiN[0, 0, 0] = 0.0
        phiN = m.irfft(FphiN)
        self.fields = dict(rho=rho, rb=rb)
        if self.gravity == "hy":
            phi_ph, _, dg = self.phantom(self.source(rb, rho), a)
            self.diag = dg
            del Fd, FphiN
            phi_b = phiN + phi_ph
            if self.reading == "chain" and self.mode == "two":
                del phi_ph
                ab = m.force_at(phi_b, self.xb, self.cb); del phi_b
                ad = m.force_at(phiN, self.xd, self.cd) if len(self.xd) else np.zeros((0, 3))
            else:
                del phi_ph
                ab = m.force_at(phi_b, self.xb, self.cb)
                ad = m.force_at(phi_b, self.xd, self.cd) if len(self.xd) else np.zeros((0, 3))
                del phi_b
        elif self.gravity == "hy_permode":
            Ce, info = self.permode_multiplier(rho - 1.0, a)
            self.permode_state = info
            FphiN *= (1.0 + Ce); del Ce, Fd
            phi_all = m.irfft(FphiN); del FphiN
            ab = m.force_at(phi_all, self.xb, self.cb)
            ad = m.force_at(phi_all, self.xd, self.cd) if len(self.xd) else np.zeros((0, 3))
            del phi_all
        else:
            del Fd, FphiN
            ab = m.force_at(phiN, self.xb, self.cb)
            ad = m.force_at(phiN, self.xd, self.cd) if len(self.xd) else np.zeros((0, 3))
        del phiN
        self.cb = self.cd = None
        return ab, ad

    def lensing_delta(self, a):
        """the lensing density delta_m + delta_ph at the current positions (psi = Phi: light sees the phantom)."""
        rb, rd = self.densities(); self.cb = self.cd = None
        rho = rb + rd; del rd
        if self.gravity == "hy":
            _, dph, _ = self.phantom(self.source(rb, rho), a, want_dph=True)
        elif self.gravity == "hy_permode":
            Ce, _ = self.permode_multiplier(rho - 1.0, a)
            dph = self.mesh.irfft(self.mesh.rfft(rho - 1.0) * Ce)
        else:
            dph = np.zeros_like(rho)
        return rho - 1.0, dph

    # ---------------------------------------------------------------- the dark fluid's conversion
    def convert(self, a, dt):
        """FK1's conversion: mesh trigger (+ sub-grid).  Returns the mass converted in this call."""
        if self.conv is None or len(self.xd) == 0:
            return 0.0
        m, c = self.mesh, self.c; NG = m.NG
        heavy = self.sd == 0
        if not heavy.any():
            return 0.0
        cv = self.conv
        fc = 1.0 - c.fb if self.mode == "two" else 1.0
        z = 1 / a - 1
        rho_t = cv["delta_t0"] * c.E(a) ** 4 / (1 + z) ** 3                       # units of the carrier's cosmic mean
        idx = np.nonzero(heavy)[0]
        cH = m.cic(self.xd[idx])
        rhoH = m.deposit(self.xd[idx], self.md[idx], cH) * NG ** 3 / fc
        rH = m.interp(rhoH, self.xd[idx], cH)
        hit = np.zeros(len(idx), bool)
        if cv.get("mesh", True):
            prob = 1.0 - math.exp(-cv["Gamma0"] * c.E(a) * dt) if np.isfinite(cv["Gamma0"]) else 1.0
            over = rH > rho_t
            pc = np.where(over, (1.0 - rho_t / np.maximum(rH, 1e-300)) if cv["picture"] == "cap" else 1.0, 0.0) * prob
            hit |= self.rng.random(len(idx)) < pc
        if self.sg is not None:
            dnl = self.fields["rho"] - 1.0
            if self.sg.get("det") is not None:                   # the seamless hand-over (a detection table per epoch)
                det = self.sg["det"](a) if callable(self.sg["det"]) else self.sg["det"]
                fsg_mesh = self.sg["obj"].f_sg_seamless(dnl, a, self.sg["M_min"], det)
            else:
                fsg_mesh = self.sg["obj"].f_sg(dnl, a, self.sg["M_min"])
            fsg = m.interp(fsg_mesh, self.xd[idx], cH)
            hit |= self.ud[idx] < fsg
        if not hit.any():
            return 0.0
        par = idx[hit]
        nh = self.rng.normal(size=(len(par), 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
        dp = a * (cv["vk"] / 100.0) * nh
        mh = self.md[par] * 0.5
        if self.audit is not None:                               # exact bookkeeping, before
            M0 = self.total_mass(); P0 = self.total_momentum(); KE0 = float(np.sum(self.md * np.sum(self.pd ** 2, 1))) / 2
            Pabs = float(self.mb * np.abs(self.pb).sum() + np.sum(self.md[:, None] * np.abs(self.pd)))
            p_par = self.pd[par].copy()
        # the parent becomes daughter 1; daughter 2 is appended
        x2 = self.xd[par].copy(); p2 = self.pd[par] - dp
        self.pd[par] = self.pd[par] + dp
        self.md[par] = mh; self.sd[par] = 1
        self.xd = np.concatenate([self.xd, x2]); self.pd = np.concatenate([self.pd, p2])
        self.md = np.concatenate([self.md, mh]); self.sd = np.concatenate([self.sd, np.ones(len(par), np.int8)])
        self.ud = np.concatenate([self.ud, np.ones(len(par))])
        self.log["events"] += int(len(par))
        if self.audit is not None:                               # ... and after
            au = self.audit; n0 = len(self.xd) - len(par)
            d1 = self.pd[par] - p_par; d2 = self.pd[n0:] - p_par
            vrel = np.concatenate([np.linalg.norm(d1, axis=1), np.linalg.norm(d2, axis=1)]) / a * 100.0      # km/s
            KE1 = float(np.sum(self.md * np.sum(self.pd ** 2, 1))) / 2
            dKE_exp = float(np.sum(2 * mh * np.sum(dp ** 2, 1))) / 2
            au["mass"] = max(au.get("mass", 0.0), abs(self.total_mass() - M0) / M0)
            au["momentum"] = max(au.get("momentum", 0.0), float(np.max(np.abs(self.total_momentum() - P0))) / max(Pabs, 1e-300))
            au["vrel"] = max(au.get("vrel", 0.0), float(np.max(np.abs(vrel / cv["vk"] - 1))) if cv["vk"] > 0 else float(np.max(vrel)))
            au["vrel_abs_max"] = max(au.get("vrel_abs_max", 0.0), float(np.max(vrel)))
            au["back_to_back"] = max(au.get("back_to_back", 0.0), float(np.max(np.abs(d1 + d2))) / max(float(np.max(np.abs(d1))), 1e-300))
            au["latent_heat"] = max(au.get("latent_heat", 0.0), abs((KE1 - KE0) / dKE_exp - 1) if dKE_exp > 0 else abs(KE1 - KE0))
            au["nsum"] = au.get("nsum", np.zeros(3)) + nh.sum(0); au["n"] = au.get("n", 0) + len(par)
            au["mesh_mass"] = max(au.get("mesh_mass", 0.0), abs(float(self.mesh.deposit(self.xd, self.md).sum()) + self.mb * len(self.xb) - 1.0))
        return float(2 * mh.sum())

    # ---------------------------------------------------------------- the integrator (the record's KDK in ln a)
    def run(self, zouts, dlna=0.02, exact=False, on_output=None, on_step=None, a_start_forces=True):
        """L362's leapfrog: dt = da/(a E(a)) at the step's start; kick 1/2, drift with a_old^2, a += da, conversion (the
        record's position: after the drift, before the forces, as L366), forces, kick 1/2.  exact=True shortens a step to
        land on each output redshift (the record overshoots to the first step past it)."""
        c, L = self.c, self.mesh.L
        a = self.a
        ab, ad = self.forces(a)
        zs = sorted(zouts, reverse=True); out = {}
        self.nstep = 0; t0 = time.time()
        while zs:
            dl = dlna
            if exact:
                a_next = 1.0 / (1.0 + zs[0])
                if a * math.exp(dlna) > a_next * (1 + 1e-12):
                    dl = math.log(a_next / a)
            da = a * (np.exp(dl) - 1); dt = da / (a * c.E(a))
            self.pb += 0.5 * dt * ab
            if len(self.xd):
                self.pd += 0.5 * dt * ad
            self.xb = (self.xb + dt * self.pb / a ** 2) % L
            if len(self.xd):
                self.xd = (self.xd + dt * self.pd / a ** 2) % L
            a = a + da
            if exact and abs(a - 1.0 / (1.0 + zs[0])) < 1e-12:
                a = 1.0 / (1.0 + zs[0])
            self.a = a
            if self.conv is not None:
                rb, rd = self.densities(); self.fields = dict(rho=rb + rd, rb=rb); self.cb = self.cd = None; del rd
                cm = self.convert(a, dt)
                self.log["converted_mass"].append((a, cm))
            ab, ad = self.forces(a)                              # recomputed on the (possibly longer) particle list
            self.pb += 0.5 * dt * ab
            if len(self.xd):
                self.pd += 0.5 * dt * ad
            self.nstep += 1
            if on_step is not None:
                on_step(self, a)
            for z in list(zs):
                if 1.0 / a - 1.0 <= z + 1e-9:
                    out[str(z)] = on_output(self, a, z) if on_output is not None else {}
                    zs.remove(z)
        self.wall = time.time() - t0
        return out

    # ---------------------------------------------------------------- bookkeeping
    def total_mass(self):
        return float(self.mb * len(self.xb) + self.md.sum())

    def total_momentum(self):
        return self.mb * self.pb.sum(0) + (self.md[:, None] * self.pd).sum(0)


if __name__ == "__main__":
    print(__doc__)


# ============================================================================================= the web channel's instrument
def flow_strain(mesh, cosmo, x, p, m, a, R_s, hubble=True):
    """the carrier's flow read on the mesh, as XR19's web census needs it (stage 3's web conversion channel; XR19_web_runaway):
    mass, momentum and velocity-squared CIC-deposited and Gaussian-smoothed on R_s (comoving Mpc/h); v = <mv>/<m>; the 1D
    dispersion sigma^2 = (<m v^2>/<m> - |v|^2)/3 [(100 km/s)^2]; the strain tensor T_ij = H delta_ij + (1/a) d_(j v_i) (spectral
    derivative of the smoothed velocity, symmetrised), returned as its eigenvalues e_1 <= e_2 <= e_3 in units of H(a).  XR19's
    classes: TA = contracting along axis 1 (e_1 < 0) in single stream, EX = all axes expanding, MS = shell-crossed (stage 3
    reads it from the dispersion).  hubble=False drops the Hubble term (the MUTATE control).  Returns (e (N,3), rho, sigma)."""
    NG = mesh.NG
    v = p / a                                                                     # peculiar velocity, units of 100 km/s
    fields = [mesh.deposit(x, m)] + [mesh.deposit(x, m * v[:, i]) for i in range(3)] + [mesh.deposit(x, m * (v ** 2).sum(1))]
    S = np.exp(-0.5 * mesh.K2 * R_s ** 2); S[0, 0, 0] = 1.0                  # a normalised smoothing (K2[0,0,0] = 1 is L362's)
    sm = [mesh.irfft(mesh.rfft(f) * S) for f in fields]
    rho = np.maximum(sm[0], 1e-30)
    vel = [sm[1 + i] / rho for i in range(3)]
    sig2 = np.maximum(sm[4] / rho - (vel[0] ** 2 + vel[1] ** 2 + vel[2] ** 2), 0.0) / 3.0
    E = cosmo.E(a)
    kvec = (mesh.k1[:, None, None], mesh.k1[None, :, None], mesh.kr[None, None, :])
    Fv = [mesh.rfft(vi) for vi in vel]
    T = np.empty((NG, NG, NG, 3, 3))
    for i in range(3):
        for j in range(i, 3):
            dij = mesh.irfft(1j * kvec[j] * Fv[i]); dji = mesh.irfft(1j * kvec[i] * Fv[j]) if i != j else dij
            T[..., i, j] = T[..., j, i] = 0.5 * (dij + dji) / a / E            # peculiar strain in units of H
    if hubble:
        for i in range(3):
            T[..., i, i] += 1.0
    e = np.linalg.eigvalsh(T.reshape(-1, 3, 3))
    return e, rho.reshape(-1) * NG ** 3, np.sqrt(sig2).reshape(-1)


def zeldovich_ic_eigen(mesh, delta0, R_s):
    """the IC's Zel'dovich deformation eigenvalues lambda_1 >= lambda_2 >= lambda_3 (at z_i), read with flow_strain's own
    operators: the box's displacement psi = -grad_c poisson(delta0) (za_ics' centred differences), Gaussian-smoothed on R_s,
    its spectral Jacobian symmetrised, lambda = eig(-sym d psi/d q).  The ZA density is 1/prod(1 - D lambda_i) and the strain
    e_i = 1 - f d_i/(1 - d_i) (units of H, d_i = D lambda_i; XR19_common.zeldovich_strain)."""
    NG = mesh.NG
    phi0 = mesh.poisson(delta0)
    S = np.exp(-0.5 * mesh.K2 * R_s ** 2); S[0, 0, 0] = 1.0
    kvec = (mesh.k1[:, None, None], mesh.k1[None, :, None], mesh.kr[None, None, :])
    Fpsi = []
    for i in range(3):
        psi_i = mesh.grad_axis(phi0, i); psi_i *= -1.0
        Fpsi.append(mesh.rfft(psi_i) * S); del psi_i
    T = np.empty((NG, NG, NG, 3, 3))
    for i in range(3):
        for j in range(i, 3):
            dij = mesh.irfft(1j * kvec[j] * Fpsi[i]); dji = mesh.irfft(1j * kvec[i] * Fpsi[j]) if i != j else dij
            T[..., i, j] = T[..., j, i] = -0.5 * (dij + dji)
    return np.linalg.eigvalsh(T.reshape(-1, 3, 3))[:, ::-1]
