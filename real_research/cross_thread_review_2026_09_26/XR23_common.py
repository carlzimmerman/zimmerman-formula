#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR23 common machinery: the derivation chain's force law at high redshift, reused READ-ONLY from the committed lanes.

  * FP13 (real_research/derivation_chain_2026/FP13_separator_from_state.py) is exec'd up to its K CONTROLS banner inside
    main() and main's locals are returned (FP13's own state machinery: FP9 -> FP6 inside, halofit, L_table, yth_state,
    gbp_rms_phys, growth_aq, the phantom with FP9's yield hook).  Nothing is edited; FP13's prints are captured.
  * The spherical-collapse force law is the chain's static law as FP6/FP9 implement it (FP6 phantom(): band-passed
    Newtonian field g_bp = (1 - S_L) g, raw phantom a0 x_P2(|g_bp|/a0 - y_th) along g_bp, the variation's output filter
    (1 - S_L) on the phantom), applied to the PECULIAR field of a spherical perturbation (the FRW leaf carries no field).
  * Two readings of which matter the MOND sector sees (never pooled):
      T  the linear yardstick's convention (FP6/FP9/FP13 growth): the kernel reads the total matter's band-passed field and
         the phantom acts on all matter -- the maximal-MOND bracket;
      B  the action's content (FP10: 'L353's constrained pair: the MOND kernel reads the baryons only; Psi feels Newtonian
         gravity'; FL1 F2 / FL2 V1): the kernel reads the baryons' band-passed field, the phantom acts on baryons only, the
         dark field collapses under Newtonian gravity.
No absolute paths; run from the repository root.
"""
import os, io, math, contextlib
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.special import erf, ndtr
from scipy.interpolate import PchipInterpolator

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
FP13_PATH = os.path.join(CHAIN, "FP13_separator_from_state.py")
FP13_MARK = "    # ============================================================================================= K  CONTROLS"
SQ2PI = math.sqrt(2.0 * math.pi)
A_EARLY = 1e-6                     # collapse ICs: Meszaros growing mode (matter + smooth radiation) set here
M_DARK = (1.9e-19, 5.2e-19)        # FP4 L10f / FP10: the dark field's mass floor [eV] (declared in the chain, not new here)

_CACHE = {}


def fp13():
    """(module namespace, main's locals) of FP13 exec'd read-only up to its K CONTROLS banner."""
    if "g" not in _CACHE:
        src = open(FP13_PATH).read()
        ns = {"__file__": FP13_PATH, "__name__": "fp13_machinery_xr23"}
        old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile(src[:src.index(FP13_MARK)] + "    return locals()\n", FP13_PATH, "exec"), ns)
                g = ns["main"]()
        finally:
            if old is None:
                os.environ.pop("MUTATE", None)
            else:
                os.environ["MUTATE"] = old
        _CACHE["ns"], _CACHE["g"] = ns, g
    return _CACHE["ns"], _CACHE["g"]


# ============================================================================================================ spectra
def T_eh98_textbook(k_mpc, h, Om, Ob, om_b, Tcmb):
    """Eisenstein & Hu 1998 no-wiggle transfer function, eqs. (26), (28)-(31): k in 1/Mpc, q = (k/h) Theta^2/Gamma_eff,
    Gamma_eff = Om h (alpha + (1 - alpha)/(1 + (0.43 k s)^4))."""
    th = Tcmb / 2.7; s = 44.5 * math.log(9.83 / (Om * h * h)) / math.sqrt(1 + 10 * om_b ** 0.75)
    ag = 1 - 0.328 * math.log(431 * Om * h * h) * (Ob / Om) + 0.38 * math.log(22.3 * Om * h * h) * (Ob / Om) ** 2
    k_mpc = np.asarray(k_mpc, float)
    ge = Om * h * (ag + (1 - ag) / (1 + (0.43 * k_mpc * s) ** 4)); q = (k_mpc / h) * th * th / ge
    L_ = np.log(2 * math.e + 1.8 * q); Cc = 14.2 + 731.0 / (1 + 62.5 * q)
    return L_ / (L_ + Cc * q * q)


def T_fdm(k_hmpc, m_eV, h):
    """Hu, Barkana & Gruzinov 2000 (PRL 85, 1158) transfer of a free scalar of mass m relative to CDM:
    T = cos(x^3)/(1 + x^8), x = 1.61 m22^(1/18) k/k_Jeq, k_Jeq = 9 m22^(1/2) Mpc^-1 (FL1 F5: the dark order parameter is a
    free field on linear scales, c_s^2 = q^2/(1 + q^2), q = k/2ma)."""
    m22 = m_eV / 1e-22; kJ = 9.0 * math.sqrt(m22)
    x = 1.61 * m22 ** (1.0 / 18.0) * (np.asarray(k_hmpc, float) * h) / kJ
    return np.cos(x ** 3) / (1 + x ** 8)


def spectra():
    """Delta^2_lin(k, z = 0) on FP13's k grid (h/Mpc) for: 'committed' (FP6's EH98 as the chain's machinery has it),
    'corrected' (the textbook EH98 form), each normalised to sigma_8 = 0.811 with the 8 Mpc/h top hat; and the wave cut-offs."""
    if "spec" in _CACHE:
        return _CACHE["spec"]
    ns, g = fp13(); M6 = g["M6"]; KKF, LKF, h, Om = g["KKF"], g["LKF"], g["h"], g["Om"]
    W8 = np.array([3 * (math.sin(8 * k) - 8 * k * math.cos(8 * k)) / (8 * k) ** 3 for k in KKF]) ** 2
    D2u = KKF ** 3 * (KKF * h) ** M6["ns"] * T_eh98_textbook(KKF * h, h, Om, M6["Ob"], M6["om_b"], M6["T_CMB"]) ** 2
    out = {"committed": np.array(g["D2L0"]), "corrected": D2u * M6["SIG8"] ** 2 / np.trapz(D2u * W8, LKF)}
    for m in M_DARK:
        tf2 = T_fdm(KKF, m, h) ** 2
        out[f"corrected_m{m:.1e}"] = out["corrected"] * tf2
        out[f"committed_m{m:.1e}"] = out["committed"] * tf2
    _CACHE["spec"] = out
    _CACHE["W8"] = W8
    return out


def register_state(tag, D2z0):
    """Add a state reading to FP13's STATE dict: linear tables D2z0 D(a)^2 and the nonlinear (halofit, FP13's rule: applied
    where the grid's smallest-scale variance exceeds 1) on FP13's LNA grid."""
    ns, g = fp13()
    if tag in g["STATE"]:
        return
    lin = [D2z0 * g["Dl"](a) ** 2 for a in g["AGR"]]
    g["STATE"][tag + "_lin"] = lin
    g["STATE"][tag] = [(g["halofit"](lin[i], g["AGR"][i])[0] if g["sig2"](g["RMIN"], lin[i]) > 1.0 else lin[i])
                       for i in range(len(g["AGR"]))]


class State:
    """The chain's separator state on FP13's LNA grid: L(a) [m, physical] and y_th(a) [a0 units] per footing."""
    def __init__(self, reading, s, switch="ramp", cy=1.0, Lmult=1.0, yth_scale=1.0):
        ns, g = fp13()
        self.Ltab = np.asarray(g["L_table"](s, reading), float)          # Mpc, physical
        ys = g["yth_state"](self.Ltab, reading, switch, cy)[1]
        self.ytab = {f: np.asarray(v, float) * yth_scale for f, v in ys.items()}
        self.lna = np.asarray(g["LNA"], float); self.a_min = float(g["AGR"][0])
        self.xi_m = ns["XI_FLOOR_MPC"] * g["Mpc"]; self.Mpc = g["Mpc"]
        self.lL = np.log(np.maximum(self.Ltab * g["Mpc"] * Lmult, 1e-300)); self.Lmult = Lmult
        self.reading, self.s = reading, s
        self.L_override = None                                            # MUTATE: a fixed L [m] at every epoch (no band-pass)

    def L(self, a):
        if self.L_override is not None:
            return self.L_override
        if a < self.a_min:
            return self.xi_m * self.Lmult
        return float(np.exp(np.interp(math.log(a), self.lna, self.lL)))

    def closed(self, a):
        """the band-pass is closed (B = b: L at the filter floor xi) -> chi = 0, no MOND"""
        if self.L_override is not None:
            return False
        return self.Lmult == 1.0 and self.L(a) <= 1.01 * self.xi_m

    def y(self, a, foot):
        if a < self.a_min:
            return 0.0
        return max(float(np.interp(math.log(a), self.lna, self.ytab[foot])), 0.0)


# ============================================================================================================ geometry
def phi_n(x):
    return np.exp(-0.5 * x * x) / SQ2PI


def F_TH(u, lam):
    """fraction of a unit-radius uniform ball, Gaussian-smoothed with sigma = lam per axis, inside radius u (closed form,
    derived from FP6's shell_frac integrated over the ball; lam > 10 uses the point-mass limit gfrac(u/lam))."""
    ns, g = fp13(); gfrac = g["M6"]["gfrac_smooth"]
    u = np.asarray(u, float); l = np.asarray(lam, float) * np.ones_like(u)
    big = l > 10.0
    ls = np.where(big, 1.0, np.maximum(l, 1e-300))
    x0 = 1.0 / ls; x1 = (1.0 + u) / ls; y1 = (1.0 - u) / ls
    A_ = lambda y: ndtr(y) * (1 + 3 * ls * ls) + phi_n(y) * (3 * ls - 3 * ls * ls * y + ls ** 3 * (y * y + 2))
    B_ = lambda x: -phi_n(x) * (ls ** 3 * (x * x + 2) - 3 * ls * ls * x + 3 * ls) - ndtr(x) * (3 * ls * ls + 1)
    I1 = u ** 3 / 3 * (ndtr(y1) + ndtr(x1) - 1.0) + ((A_(x0) - A_(y1)) - (B_(x1) - B_(x0))) / 3.0
    T2 = ls * ls * ((-ls * phi_n(x1) - ndtr(x1)) + (ndtr(y1) + ls * phi_n(y1)))
    v = 3.0 * (I1 + T2)
    return np.where(big, gfrac(u / np.where(big, l, 1.0)), v)


def shell_frac(r, rp, L):
    """FP6's shell_frac (a unit shell at rp, Gaussian-smoothed with sigma = L, fraction inside r), vectorised."""
    s = math.sqrt(2) * L; rp = np.maximum(np.asarray(rp, float), 1e-300)
    return 0.5 * (erf((r + rp) / s) + erf((r - rp) / s)) - (L / (rp * SQ2PI)) * (
        np.exp(-(r - rp) ** 2 / (2 * L * L)) - np.exp(-(r + rp) ** 2 / (2 * L * L)))


_XIG = np.linspace(-8, 8, 161)


def _ugrid(lam):
    top = 1.0 + 8.0 * lam
    loc = 1.0 + lam * _XIG
    return np.unique(np.concatenate([np.geomspace(1e-4, top, 500), loc[loc > 1e-4], [1.0]]))


def m_phantom_single(Y, yt, lam, prof, outf=True):
    """the chain's MOND acceleration (units a0, inward positive) on a spherical shell at u = 1 around a mass excess with edge
    field Y = G dM/(R^2 a0), lam = L/R: 'point' = the excess concentrated at the centre (FP6 phantom()'s geometry), 'tophat' =
    a uniform sphere with a sharp edge (its band-passed field has an edge layer ~L thick)."""
    ns, g = fp13(); gfrac = g["M6"]["gfrac_smooth"]; x_P2 = g["x_P2"]
    if Y <= 0 or lam < 1e-7:
        return 0.0
    u = _ugrid(lam)
    beta = (1.0 - gfrac(u / lam)) if prof == "point" else (np.minimum(1.0, u ** 3) - F_TH(u, lam))
    yb = Y * beta / u ** 2
    Mr = np.sign(yb) * x_P2(np.abs(yb) - yt) * u ** 2
    i1 = int(np.searchsorted(u, 1.0))
    if not outf:
        return float(Mr[i1])
    dM = np.diff(Mr); um = np.sqrt(u[1:] * u[:-1])
    Ms = float(shell_frac(1.0, um, lam) @ dM) + Mr[0] * float(gfrac(1.0 / lam))
    return float(Mr[i1] - Ms)


# ============================================================================================================ collapse
class Cosmo:
    """the chain's background (FP6's: h, Omega_m, Omega_L, Omega_r) and footings (FP0's a0 via FP9); radiation=False drops
    Omega_r (Omega_L unchanged) -- used only by the LCDM control against the textbook matter + Lambda threshold."""
    def __init__(self, radiation=True):
        ns, g = fp13()
        self.G, self.Mpc, self.MSUN, self.h = g["G"], g["Mpc"], g["MSUN"], g["h"]
        self.Om, self.OL, self.H0, self.rho_c0 = g["Om"], g["OL"], g["H0"], g["rho_crit0"]
        self.Or = g["Or"] if radiation else 0.0
        self.A0 = dict(g["A0"])
        if radiation:
            self.Ez, self.dlnH = g["Ez"], g["dlnH"]
        else:
            Om, OL = self.Om, self.OL
            self.Ez = lambda a: math.sqrt(Om / a ** 3 + OL)
            self.dlnH = lambda a: -1.5 * Om / a ** 3 / (Om / a ** 3 + OL)
        self.a_eq = max(self.Or, 1e-30) / self.Om
        self.fb = g["M6"]["Ob"] / self.Om
        sD = solve_ivp(lambda N, Y: [Y[1], -(2 + self.dlnH(math.exp(N))) * Y[1] + 1.5 * self.Om / math.exp(3 * N) / self.Ez(math.exp(N)) ** 2 * Y[0]],
                       (math.log(A_EARLY), math.log(4.0)), [1 + 1.5 * A_EARLY / self.a_eq, 1.5 * A_EARLY / self.a_eq],
                       method="LSODA", rtol=1e-12, atol=1e-15, dense_output=True)
        self._sD = sD

    def Du(self, N):
        """linear growth of the Meszaros growing mode normalised to 1 as a -> 0 (radiation smooth), same ODE as FP13's Dl"""
        return float(self._sD.sol(N)[0])

    def RL(self, Mmsun):
        return (3 * Mmsun * self.MSUN / (4 * math.pi * self.Om * self.rho_c0)) ** (1.0 / 3.0)   # comoving [m]


def _rhs_single(N, Y, cp, M, RL, a0, foot, st, prof, mond, outf):
    s, sp = Y; a = math.exp(N); H = cp.H0 * cp.Ez(a); d = math.expm1(s)
    extra = 0.0
    if mond and st is not None and d > 0 and a >= st.a_min and not st.closed(a):
        r = a * RL * math.exp(-s / 3.0); dM = M * d / (1 + d)
        Yv = cp.G * dM / (r * r * a0)
        extra = 3.0 * a0 * m_phantom_single(Yv, st.y(a, foot), st.L(a) / r, prof, outf) / (r * H * H)
    return [sp, -(2 + cp.dlnH(a)) * sp + sp * sp / 3.0 + 1.5 * cp.Om / a ** 3 / cp.Ez(a) ** 2 * d + extra]


def collapse_single(cp, Mmsun, A, foot, st, prof, mond=True, outf=True, rtol=1e-8):
    """one spherical shell (single-shell bracket models): returns (N at r = r_max/2 [formation], N at r -> 0 [collapse])."""
    M = Mmsun * cp.MSUN; RL = cp.RL(Mmsun); a0 = cp.A0[foot]
    yi = A_EARLY / cp.a_eq; d_i = A * (1 + 1.5 * yi); dp_i = A * 1.5 * yi
    ev = lambda N, Y, *args: Y[0] - math.log(1e9)
    ev.terminal = True; ev.direction = 1
    sol = solve_ivp(_rhs_single, (math.log(A_EARLY), math.log(4.0)), [math.log1p(d_i), dp_i / (1 + d_i)], method="LSODA",
                    rtol=rtol, atol=1e-12, events=ev, dense_output=True, args=(cp, M, RL, a0, foot, st, prof, mond, outf))
    if sol.status != 1:
        return float("nan"), float("nan")
    Nc = float(sol.t_events[0][0]); s_c = float(sol.y_events[0][0][0])
    a = math.exp(Nc); r = a * RL * math.exp(-s_c / 3.0)
    Ncol = Nc + cp.H0 * cp.Ez(a) * (2.0 / 3.0) * r ** 1.5 / math.sqrt(2 * cp.G * M)
    # formation: r = r_max/2 after turnaround, from the dense solution
    Ng = np.linspace(math.log(A_EARLY), Nc, 6000)
    rg = np.exp(Ng) * RL * np.exp(-sol.sol(Ng)[0] / 3.0)
    j = int(np.argmax(rg)); half = 0.5 * rg[j]
    k = j + int(np.argmax(rg[j:] <= half))
    if rg[k] > half:
        return float("nan"), Ncol
    from scipy.optimize import brentq
    f = lambda N: math.exp(N) * RL * math.exp(-float(sol.sol(N)[0]) / 3.0) - half
    Nf = brentq(f, Ng[k - 1], Ng[k], xtol=1e-12)
    return Nf, Ncol


def mean_profile(RL_hmpc, x, D2z0, KKF, LKF):
    """P(x) = C(x R, R)/C(R, R), C(q, R) = Int Delta^2 W(kq) W(kR) dln k: the conditional mean enclosed overdensity around a
    point whose top-hat-smoothed contrast at R is fixed (linear, Gaussian field)."""
    def W(y):
        y = np.maximum(y, 1e-8)
        return np.where(y < 1e-3, 1.0 - y * y / 10.0, 3 * (np.sin(y) - y * np.cos(y)) / y ** 3)
    WR = W(KKF * RL_hmpc)
    cRR = np.trapz(D2z0 * WR * WR, LKF)
    return np.array([np.trapz(D2z0 * W(KKF * xx * RL_hmpc) * WR, LKF) for xx in x]) / cRR


class MultiShell:
    """Lagrangian multi-shell spherical collapse in the chain's force law with a smooth initial profile.

    reading 'T': one species (all matter) feels the phantom sourced by the total band-passed peculiar field.
    reading 'B': dark shells (Newtonian only) + baryon shells (Newtonian + phantom sourced by the baryons' band-passed field).
    Each species' matter is piecewise uniform between its (sorted) shell radii; the band-pass (1 - S_L) is applied to that
    distribution exactly (F_TH closed form), the exterior beyond the last shell is uniform background; the phantom's output
    filter (1 - S_L) is applied the same way.  A shell is frozen (virialised) when it falls to half its maximum radius.
    The tracked shell is the one at the target mass's Lagrangian radius (the DARK one in reading B)."""

    def __init__(self, cp, Mmsun, foot, st, reading="T", D2z0=None, N_in=24, N_out=24, xmax=2.5, stepf=0.02,
                 mond=True, track_collapse=False, yth_b_scale=1.0):
        ns, g = fp13()
        self.cp, self.foot, self.st, self.reading, self.mond = cp, foot, st, reading, mond
        self.stepf, self.track_collapse, self.yth_b_scale = stepf, track_collapse, yth_b_scale
        self.x_P2 = g["x_P2"]
        self.M = Mmsun * cp.MSUN; self.RLc = cp.RL(Mmsun)
        x = np.concatenate([np.linspace(1.0 / N_in, 1.0, N_in), np.linspace(1.0, xmax, N_out + 1)[1:]])
        self.x = x; self.jR = int(np.argmin(abs(x - 1.0)))
        D2 = spectra()["corrected"] if D2z0 is None else D2z0
        self.P = mean_profile(self.RLc / cp.Mpc * cp.h, x, D2, g["KKF"], g["LKF"])
        self.q = x * self.RLc
        Menc = (4 * math.pi / 3) * cp.Om * cp.rho_c0 * self.q ** 3      # enclosed (Lagrangian) mass, all matter
        self.cell = np.diff(np.concatenate([[0.0], Menc]))
        self.Menc = Menc
        self.info = {"act": 0, "max_ratio": 0.0, "min_ratio": 0.0}

    # --- piecewise-uniform smoothing matrix: S[j, c] = fraction of cell c (between rs[c-1] and rs[c]) inside radius rq[j]
    @staticmethod
    def _Smat(rq, rs, L):
        F = F_TH(rq[:, None] / rs[None, :], L / rs[None, :])
        V = rs ** 3
        Vin = np.concatenate([[0.0], V[:-1]])
        Fin = np.concatenate([np.zeros((len(rq), 1)), F[:, :-1]], axis=1)
        return (V[None, :] * F - Vin[None, :] * Fin) / (V - Vin)[None, :], F[:, -1]

    def _phantom(self, rq_src, cellmass, rho_bg, L, yt, a0):
        """chain's phantom (inward positive, m/s^2) at the source species' own shell radii (sorted input)."""
        cp = self.cp
        S, Fext = self._Smat(rq_src, rq_src, L)
        rN = rq_src[-1]
        Mins = np.cumsum(cellmass)
        ext = 4 * math.pi / 3 * rho_bg * (rq_src ** 3 - rN ** 3 * Fext)
        bp = Mins - S @ cellmass - ext
        ybp = cp.G * bp / rq_src ** 2 / a0
        Mraw = np.sign(ybp) * self.x_P2(np.abs(ybp) - yt) * a0 * rq_src ** 2 / cp.G
        mu = np.diff(np.concatenate([[0.0], Mraw]))
        Mph = Mraw - S @ mu
        return cp.G * Mph / rq_src ** 2

    def run(self, A):
        cp = self.cp; st = self.st; a0 = cp.A0[self.foot]
        nsh = len(self.x); fb = cp.fb
        # ICs: each shell integrated alone (MOND off: a < FP13's first epoch) from A_EARLY to a_start
        a_start = st.a_min if st is not None else 1e-3
        N1 = math.log(a_start); yi = A_EARLY / cp.a_eq
        d_i = A * self.P * (1 + 1.5 * yi); dp_i = A * self.P * 1.5 * yi

        def pre(N, Y):
            s_, sp_ = Y[:nsh], Y[nsh:]
            return np.concatenate([sp_, -(2 + cp.dlnH(math.exp(N))) * sp_ + sp_ ** 2 / 3
                                   + 1.5 * cp.Om / math.exp(3 * N) / cp.Ez(math.exp(N)) ** 2 * np.expm1(s_)])
        sol = solve_ivp(pre, (math.log(A_EARLY), N1), np.concatenate([np.log1p(d_i), dp_i / (1 + d_i)]), method="LSODA",
                        rtol=1e-10, atol=1e-13)
        S0, S1 = sol.y[:nsh, -1].copy(), sol.y[nsh:, -1].copy()
        two = self.reading == "B"
        ns_ = 2 * nsh if two else nsh
        q = np.concatenate([self.q, self.q]) if two else self.q.copy()
        mass = np.concatenate([(1 - fb) * self.cell, fb * self.cell]) if two else self.cell.copy()
        isb = np.concatenate([np.zeros(nsh, bool), np.ones(nsh, bool)]) if two else np.zeros(nsh, bool)
        s = np.concatenate([S0, S0]) if two else S0.copy()
        sp = np.concatenate([S1, S1]) if two else S1.copy()
        jT = self.jR                                          # tracked shell (dark in B)
        frozen = np.zeros(ns_, bool); tfreeze = np.full(ns_, np.nan)
        Mfix = self.Menc[self.jR]
        radii = lambda N, s_: math.exp(N) * q * np.exp(-s_ / 3.0)
        rmax = radii(N1, s).copy()
        Nn = N1; Nend = math.log(4.0); self.bary_in = None

        def enclosed(r):
            """total enclosed mass at each shell radius: each species piecewise uniform (in r^3) between its sorted radii;
            a shell's own cell lies inside it (cell convention)."""
            out = np.zeros_like(r)
            for sel in ((~isb), isb):
                rs_ = np.sort(r[sel]); ms_ = mass[sel][np.argsort(r[sel])]
                cum = np.concatenate([[0.0], np.cumsum(ms_)]); rlo = np.concatenate([[0.0], rs_])
                idx = np.searchsorted(rs_, r, side="right")               # cells fully inside: 0 .. idx-1
                full = cum[idx]
                part = np.where(idx < len(rs_), ms_[np.minimum(idx, len(rs_) - 1)]
                                * np.clip((r ** 3 - rlo[idx] ** 3) / (rs_[np.minimum(idx, len(rs_) - 1)] ** 3 - rlo[idx] ** 3), 0.0, 1.0), 0.0)
                out += full + part
            return out

        def deriv(N, s_, sp_):
            a = math.exp(N); H = cp.H0 * cp.Ez(a)
            d = np.expm1(s_); r = radii(N, s_)
            # Newtonian: enclosed mass from the current positions (Lagrangian value when nothing has crossed)
            Me = enclosed(r) if two else self.Menc_sorted(r)
            if self.track_collapse and not two:
                Me[jT] = Mfix
            rho_bar = cp.Om * cp.rho_c0 / a ** 3
            gN_pec = cp.G * (Me - 4 * math.pi / 3 * rho_bar * r ** 3) / r ** 2
            acc_extra = np.zeros(ns_)
            if self.mond and st is not None and a >= st.a_min and not st.closed(a):
                L = st.L(a); yt = st.y(a, self.foot) * (self.yth_b_scale if two else 1.0)
                src = isb if two else np.ones(ns_, bool)
                ypec_max = np.max(np.abs(gN_pec[src])) / a0 * (fb if two else 1.0)
                if not (yt > 0 and 2.0 * ypec_max < yt):
                    rsrc = r[src]; o = np.argsort(rsrc)
                    gm_sorted = self._phantom(rsrc[o], mass[src][o], (fb if two else 1.0) * rho_bar, L, yt, a0)
                    gm = np.empty(src.sum()); gm[o] = gm_sorted
                    acc_extra[src] = gm
                    self.info["act"] += 1
                    if two:
                        rb_ = r[isb]; Mb_in = self.Menc * fb
                        ratB = gm / np.maximum(cp.G * Me[isb] / rb_ ** 2, 1e-300)
                        self.info["max_ratio"] = max(self.info["max_ratio"], float(np.max(ratB)))
                        self.info["min_ratio"] = min(self.info["min_ratio"], float(np.min(ratB)))
                        self.info["max_ybp_b"] = max(self.info.get("max_ybp_b", 0.0), float(np.max(np.abs(gm))) / a0)
                    if not two:
                        rat = gm[jT] / (cp.G * Me[jT] / r[jT] ** 2)
                        self.info["max_ratio"] = max(self.info["max_ratio"], rat)
                        self.info["min_ratio"] = min(self.info["min_ratio"], rat)
            # the s-equation with the enclosed mass possibly differing from the Lagrangian one
            MeL = np.concatenate([self.Menc, self.Menc]) if two else self.Menc
            corr = (Me / MeL - 1.0)                              # extra Newtonian pull from crossed mass, as a fraction
            acc = (-(2 + cp.dlnH(a)) * sp_ + sp_ ** 2 / 3 + 1.5 * cp.Om / a ** 3 / cp.Ez(a) ** 2 * (d + corr * (1 + d))
                   + 3 * acc_extra / (r * H * H))
            acc = np.where(frozen, 0.0, acc)
            spp = np.where(frozen, 3.0, sp_)
            return spp, acc

        nstep = 0
        while Nn < Nend:
            r = radii(Nn, s); act = ~frozen
            rdot = 1.0 - sp / 3.0
            tdyn = np.min(np.abs(1.0 / np.where(act, rdot, 1e-30)))
            dN = min(self.stepf, self.stepf * tdyn, Nend - Nn)
            k1 = deriv(Nn, s, sp)
            k2 = deriv(Nn + dN / 2, s + dN / 2 * k1[0], sp + dN / 2 * k1[1])
            k3 = deriv(Nn + dN / 2, s + dN / 2 * k2[0], sp + dN / 2 * k2[1])
            k4 = deriv(Nn + dN, s + dN * k3[0], sp + dN * k3[1])
            s_new = s + dN / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            sp_new = sp + dN / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            r_new = radii(Nn + dN, s_new)
            rmax = np.maximum(rmax, r_new)
            hit = (~frozen) & (r_new <= 0.5 * rmax)
            if self.track_collapse and not two:
                hit[jT] = False
            for j in np.where(hit)[0]:
                f0 = r[j] - 0.5 * rmax[j]; f1 = r_new[j] - 0.5 * rmax[j]
                frac = f0 / (f0 - f1) if f0 != f1 else 1.0
                tfreeze[j] = Nn + frac * dN; frozen[j] = True
                s_new[j] = 3 * (Nn + dN) - 3 * math.log(0.5 * rmax[j] / q[j])
                sp_new[j] = 3.0
            s, sp, Nn = s_new, sp_new, Nn + dN; nstep += 1
            if two and frozen[jT] and self.bary_in is None:
                rr_ = radii(Nn, s); rT = rr_[jT]
                rb_ = np.sort(rr_[isb]); mb_ = mass[isb][np.argsort(rr_[isb])]
                cumb = np.concatenate([[0.0], np.cumsum(mb_)]); rlo_ = np.concatenate([[0.0], rb_])
                k_ = int(np.searchsorted(rb_, rT, side="right"))
                part = mb_[k_] * (rT ** 3 - rlo_[k_] ** 3) / (rb_[k_] ** 3 - rlo_[k_] ** 3) if k_ < len(rb_) else 0.0
                self.bary_in = float((cumb[k_] + part) / (fb * self.Menc[self.jR]))      # piecewise-uniform baryon cells
            if self.track_collapse and not two:
                rT = radii(Nn, s)[jT]
                if rT < 1e-3 * rmax[jT]:
                    a = math.exp(Nn)
                    return {"N_form": float("nan"), "N_coll": Nn + cp.H0 * cp.Ez(a) * (2.0 / 3.0) * rT ** 1.5 / math.sqrt(2 * cp.G * Mfix), "steps": nstep}
            if (not self.track_collapse or two) and frozen[jT]:
                break
        return {"N_form": float(tfreeze[jT]), "N_coll": float("nan"), "steps": nstep, "bary_in": self.bary_in}

    def Menc_sorted(self, r):
        """single species: enclosed mass at each shell from the current order (Lagrangian value if nothing crossed)."""
        order = np.argsort(r); cum = np.cumsum(self.cell[order])
        out = np.empty_like(r); out[order] = cum
        return out


def dc_from_grid(cp, run_fn, zs, A_lo, A_hi, nA):
    """run_fn(A) -> N_event; returns {z: delta_eff = A(z) D_u(N(z))} by monotone interpolation of ln A against N_event."""
    As = np.geomspace(A_lo, A_hi, nA)
    Ns = np.array([run_fn(A) for A in As])
    ok = np.isfinite(Ns)
    lnA, Nn = np.log(As[ok]), Ns[ok]
    mono = bool(np.all(np.diff(Nn) < 0))
    out = {}
    if ok.sum() < 4:
        return {z: float("nan") for z in zs}, mono, (As, Ns)
    o = np.argsort(Nn)
    f = PchipInterpolator(Nn[o], lnA[o])
    for z in zs:
        Nt = math.log(1.0 / (1.0 + z))
        out[z] = float(math.exp(f(Nt)) * cp.Du(Nt)) if Nn.min() <= Nt <= Nn.max() else float("nan")
    return out, mono, (As, Ns)
