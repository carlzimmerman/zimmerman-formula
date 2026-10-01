#!/usr/bin/env python3
"""
AS228 — Derive independent galactic spatial and lapse potentials (slip = Psi - Phi)
Run:  AS228-slip-r1-20260928T1936Z-dsv4f-hermes
Worker: deepseek/deepseek-v4-flash-0731 via Hermes subagent (openrouter)

Seed: AS228_derive_independent_galactic_spatial_and_lapse_potentials.md
  sha256 f5f9f44da70be29782909dba84ceffac453b34e92304f0519ea2051416742f0e
Sources: FINAL_ACTION.md b8c04d4e... (CA4-GNC common action, CA5-GNC-R branch),
  FRIED_CHICKEN_SPEC.md 98d9149f... (amended reqs 1/3/7/12), REVIEW.md 26693935...

Task target (seed-displayed math):
    ds^2 = -(1+2Phi/c^2) c^2 dt^2 + (1-2Psi/c^2) dx^2 ;  slip = Psi - Phi.
Derive, from the SAME action, the linearized lapse equation and the trace-free
spatial metric equation INDEPENDENTLY (including gate, filter and projector
stress), express the sourced slip equation WITHOUT imposing Phi = Psi, and run
the negative control: assign Psi = Phi before varying the metric and require a
nonzero transition stress residual.

Conventions (pinned): c = 1 in the action; dimensionless potentials in the
weak-field static chart; torus T^3 mean-zero normalization ("nonzero-mode
normalization", FINAL_ACTION.md Sec. 5); operative branch = filtered MONO
(nu_mono through S = exp(b Delta_h), b = xi^2/2); kappa = 1/2 adopted;
G_N = 6.67430e-11 SI, G_bare = c_N G_N kept separate.

Controls (residuals are ACTUAL computed numbers, all capable of failing):
  C0  on-shell lapse-type residual (eq.13 linearized) at solved fields
  C1  trace-channel metric variation dL/deps at SOLVED fields -> ~0
  C2  traceless-channel metric variation at SOLVED fields -> ~0
  Cs  substitution of the derived slip equation: lap(slip) - 4 pi G rho_slip -> ~0
  NEG assign Psi = Phi, vary the metric: transition stress residual NONZERO;
      with the gate idle (small source, f = 0) it must -> ~0
  Cr  refinement N=64 -> N=96
Bounds: signal.alarm(120); 1 thread; /usr/bin/time -l.
"""
import gc, json, os, resource, signal, subprocess, sys, time
import numpy as np

signal.alarm(120)
for v in ("OPENBLAS", "OMP", "MKL", "NUMEXPR", "VECLIB"):
    os.environ.setdefault(v + "_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")

T0 = time.time()

G_SI = 6.67430e-11
G_N = G_SI   # measured Newton constant (default numerics convention)
C_SI = 299792458.0
M_SUN = 1.98847e30
PC_SI = 3.085677581491367e16
KAPPA = 0.5
A0_CAN = 9.3619e-11
A0_ALT = 1.1279e-10
XI = 0.5
B_HEAT = XI * XI / 2.0
DELTA_MONO = 0.05
ALPHA = 0.1
C_N = 1.0 - ALPHA / 2.0
ELL = 0.04
A0G = 1.0e-6                # grid-unit a0 scale (y = |p|/A0G through the MONO transition)
THETA_G = 4.0 * A0G * A0G * 0.35     # gate threshold: transition at y_theta via J(y) = 4 a0^2 int h
DELTA_GATE = 0.5 * THETA_G           # gate ramp width in Y units
G_BARE = C_N * G_SI
G_GRID = 1.0e-17            # grid-unit Newton constant (weak-field cell, G_GRID rho_b r^2 << 1)

FOOTINGS = {
    "canonical":   {"a0": A0_CAN, "rho_Lambda": 4.0 * A0_CAN ** 2 / (G_SI * C_SI ** 2)},
    "alternative": {"a0": A0_ALT, "rho_Lambda": 4.0 * A0_ALT ** 2 / (G_SI * C_SI ** 2)},
}
for _n, _f in FOOTINGS.items():
    _a = KAPPA * C_SI * np.sqrt(G_SI * _f["rho_Lambda"])
    _f["a0_roundtrip"] = _a
    _f["a0_relerr"] = abs(_a - _f["a0"]) / _f["a0"]

# ---------------------------------------------------------------------------
# 1. Criterion-B branches (all five distinct; MONO operative)
# ---------------------------------------------------------------------------

def nu_q(y):
    return np.sqrt(1.0 + 1.0 / y)

def nu_rar(y):
    y = np.asarray(y, dtype=float)
    s = np.sqrt(y)
    return 1.0 / (-np.expm1(-s))

def h_rar(y):
    y = np.asarray(y, dtype=float)
    s = np.sqrt(y)
    sm = s < 40.0
    out = np.empty_like(y)
    with np.errstate(divide="ignore", invalid="ignore"):
        em1 = np.expm1(s[sm])
        out[sm] = np.where(em1 > 0.0, y[sm] / em1, 0.0)
    out[~sm] = y[~sm] * np.exp(-s[~sm])
    return out

def dh_rar(y):
    y = np.asarray(y, dtype=float)
    s = np.sqrt(y)
    e = np.exp(s)
    sm = s < 40.0
    out = np.empty_like(y)
    es = e[sm]
    with np.errstate(divide="ignore", invalid="ignore"):
        em1 = np.expm1(s[sm])
        out[sm] = np.where(em1 > 0.0, 1.0 / em1 - y[sm] * es / (2.0 * s[sm] * em1 * em1), 0.0)
    out[~sm] = np.exp(-s[~sm]) * (1.0 - y[~sm] / (2.0 * s[~sm]))
    return out

def _root(f, lo, hi, n=400, tol=1e-14):
    flo, fhi = f(lo), f(hi)
    assert (flo <= 0.0 <= fhi) or (fhi <= 0.0 <= flo), (lo, hi, flo, fhi)
    for _ in range(n):
        m = 0.5 * (lo + hi)
        fm = f(m)
        if fm == 0.0:
            return m
        if fm * flo <= 0:
            hi, fhi = m, fm
        else:
            lo, flo = m, fm
        if hi - lo < tol * max(1.0, abs(hi)):
            break
    return 0.5 * (lo + hi)

_YP = _root(dh_rar, 2.0, 3.0)
_HP = float(h_rar(_YP))
_Y_STAR = _root(lambda y: dh_rar(y) - DELTA_MONO * _HP / (y + _YP), 2.0, 2.6)
_H_STAR = float(h_rar(_Y_STAR))

def h_mono(y):
    y = np.asarray(y, dtype=float)
    return np.where(y <= _Y_STAR, h_rar(y),
                    _H_STAR + DELTA_MONO * _HP * np.log((y + _YP) / (_Y_STAR + _YP)))

def nu_mono(y):
    return 1.0 + h_mono(y) / y

def dnu_mono(y):
    y = np.asarray(y, dtype=float)
    h = np.empty_like(y)
    d = np.empty_like(y)
    sm = y <= _Y_STAR
    h[sm] = h_rar(y[sm]);            d[sm] = dh_rar(y[sm])
    h[~sm] = _H_STAR + DELTA_MONO * _HP * np.log((y[~sm] + _YP) / (_Y_STAR + _YP))
    d[~sm] = DELTA_MONO * _HP / (y[~sm] + _YP)
    return d / y - h / (y * y)

def _implicit(fnu, y):
    y = np.asarray(y, dtype=float)
    out = np.empty_like(y)
    for i, yi in enumerate(y.ravel()):
        g = lambda t, yy=yi: t * fnu(yy * t) - 1.0
        hi = 1.0
        while g(hi) <= 0.0:
            hi *= 2.0
        out.flat[i] = _root(g, 1.0, hi, tol=1e-12)
    return out

nu_exp_imp = lambda y: _implicit(lambda x: 1.0 - np.exp(-x), y)
nu_mu2_imp = lambda y: _implicit(lambda x: 1.0 - (1.0 + x / 2.0) ** -2, y)

def _fd_dnu(nu_f, y, h=1e-5):
    y = np.asarray(y, dtype=float)
    return (nu_f(y + h) - nu_f(y - h)) / (2.0 * h)

BRANCHES = {
    "Q":    (nu_q, lambda y: -0.5 / (y * y * np.sqrt(1.0 + 1.0 / y))),
    "RAR":  (nu_rar, lambda y: -nu_rar(y) ** 2 * np.exp(-np.sqrt(y)) / (2.0 * np.sqrt(y))),
    "EXP":  (nu_exp_imp, lambda y: _fd_dnu(nu_exp_imp, y)),
    "MU2":  (nu_mu2_imp, lambda y: _fd_dnu(nu_mu2_imp, y)),
    "MONO": (nu_mono, dnu_mono),
}

# ---------------------------------------------------------------------------
# 2. Spectral torus T^3
# ---------------------------------------------------------------------------

class Torus3:
    def __init__(self, N, L):
        self.N, self.L = N, L
        self.ks = 2.0 * np.pi * np.fft.fftfreq(N, d=1.0)
        self.kx, self.ky, self.kz = np.meshgrid(self.ks, self.ks, self.ks, indexing="ij")
        self.k2 = self.kx ** 2 + self.ky ** 2 + self.kz ** 2
        nq = self.N // 2 + 1
        self.k2q = self.k2[..., :nq]
        self.kxq = self.kx[..., :nq]
        self.kyq = self.ky[..., :nq]
        self.kzq = self.kz[..., :nq]
        self.x = np.linspace(0.0, L, N, endpoint=False)
        self.X, self.Y, self.Z = np.meshgrid(self.x, self.x, self.x, indexing="ij")

    def D(self, i, f):
        # full-spectrum derivative: rfftn half-spectrum conjugation breaks axes 0/1
        kk = (self.kx, self.ky, self.kz)[i]
        return np.fft.ifftn(1j * kk * np.fft.fftn(f)).real

    def lap(self, f):
        return np.fft.irfftn(-self.k2q * np.fft.rfftn(f), s=(self.N,) * 3)

    def poisson(self, rhs):
        rhs = rhs - rhs.mean()
        f = np.fft.rfftn(rhs)
        out = np.zeros_like(f)
        safe = self.k2q > 1e-30
        out[safe] = (-1.0 / self.k2q[safe] * f[safe])
        return np.fft.irfftn(out, s=(self.N,) * 3)

    def filter_s(self, f):
        return np.fft.irfftn(np.exp(-B_HEAT * self.k2q) * np.fft.rfftn(f), s=(self.N,) * 3)

    def grad(self, f):
        return np.array([self.D(i, f) for i in range(3)])

    def div(self, v):
        return self.D(0, v[0]) + self.D(1, v[1]) + self.D(2, v[2])

# ---------------------------------------------------------------------------
# 3. Frozen convex gate ramp  (FINAL_ACTION Sec.1)
# ---------------------------------------------------------------------------

def gate_f(Y):
    Y = np.asarray(Y, dtype=float)
    f = np.zeros_like(Y)
    f[Y >= DELTA_GATE] = 1.0
    m = (Y > 0.0) & (Y < DELTA_GATE)
    rm = Y[m] / DELTA_GATE
    f[m] = 35.0 * rm ** 4 - 84.0 * rm ** 5 + 70.0 * rm ** 6 - 20.0 * rm ** 7
    return f

def gate_G(Y):
    Y = np.asarray(Y, dtype=float)
    G = np.zeros_like(Y)
    G[Y >= DELTA_GATE] = Y[Y >= DELTA_GATE] - DELTA_GATE / 2.0
    m = (Y > 0.0) & (Y < DELTA_GATE)
    rm = Y[m] / DELTA_GATE
    G[m] = DELTA_GATE * (7.0 * rm ** 5 - 14.0 * rm ** 6 + 10.0 * rm ** 7 - 2.5 * rm ** 8)
    return G

# ---------------------------------------------------------------------------
# 4. Metric strain: A^ij and exact first-order operator responses
# ---------------------------------------------------------------------------

class Strain:
    def __init__(self, T, kind, chi=None, eta=None):
        self.T = T
        self.kind = kind
        if kind == "trace":
            self.A = np.zeros((3, 3) + chi.shape)
            for i in range(3):
                self.A[i, i] = 2.0 * chi
        else:
            e = eta
            n2 = e[0] ** 2 + e[1] ** 2 + e[2] ** 2
            self.A = np.empty((3, 3) + e[0].shape)
            for i in range(3):
                for j in range(3):
                    self.A[i, j] = e[i] * e[j] - (1.0 / 3.0) * n2 * (1.0 if i == j else 0.0)
        self.trA = self.A[0, 0] + self.A[1, 1] + self.A[2, 2]

    def dLapl(self, f):
        """First variation of Delta_h under h -> h + eps A^ij (verified vs FD):
        dLapl f = A^ij f_,ij + (d_i A^ij) f_,j - (1/2)(d^i trA) f_,i."""
        T = self.T
        out = np.zeros_like(f)
        for i in range(3):
            for j in range(3):
                out += self.A[i, j] * T.D(j, T.D(i, f))
        for i in range(3):
            for j in range(3):
                out += T.D(i, self.A[i, j]) * T.D(j, f)
        for i in range(3):
            out -= 0.5 * T.D(i, self.trA) * T.D(i, f)
        return out

    def dFilterAct(self, u, m=4):
        """(d/deps) S_{h(eps)} u = int_0^b e^{(b-r)Delta} (dLapl) e^{r Delta} u dr
        (Duhamel; midpoint rule, spectral semigroup, exact to first order)."""
        T = self.T
        acc = np.zeros_like(u)
        dr = B_HEAT / m
        for k in range(m):
            r = (k + 0.5) * dr
            Fr = np.fft.irfftn(np.exp(-r * T.k2q) * np.fft.rfftn(u), s=(T.N,) * 3)
            dFr = self.dLapl(Fr)
            acc += np.fft.irfftn(np.exp(-(B_HEAT - r) * T.k2q) * np.fft.rfftn(dFr), s=(T.N,) * 3)
        return acc * dr

    def dMeasure(self):
        return -0.5 * self.trA

# ---------------------------------------------------------------------------
# 5. On-shell fields and the derived sourced slip equation
# ---------------------------------------------------------------------------

def kernel_J(p, a0g):
    """J(DW) = 2 a0^2 q(|DW|^2/a0^2), q'(y^2) = nu(y)-1
    Closed form: J = 4 a0g^2 * int_0^y h(s) ds  (h = monotone phantom).
    Deterministic CDF quadrature on a fixed s-grid."""
    n2 = p[0] ** 2 + p[1] ** 2 + p[2] ** 2
    y = np.sqrt(n2) / a0g
    smax = max(float(np.max(y)), 1e-3)
    grid = np.linspace(0.0, smax * 1.05, 120001)
    hh = h_mono(grid)
    hh[0] = 0.0   # integrand regular at s = 0: h(s) ~ s(nu-1) -> 0
    cdf = np.concatenate([[0.0], np.cumsum(hh[1:] * np.diff(grid))])
    return 4.0 * a0g * a0g * np.interp(y, grid, cdf)

def slip_source_analytic(F, T, ell):
    """Derived leading same-action slip source (derivation.md Sec.6):
       rho_slip = (1/4 pi G_N) * { c_N f [ 4(nu-1)|p|^2 + 2 ell Delta W ]
                                   + 2 c_N ell (D Phi . D W)
                                   - c_N [ G(Y_h) - ell Delta W ] }
       gate trace stress   +  compensator cross  -  lapse-channel gate weight."""
    p, nu, f, Yh = F["p"], F["nu"], F["f"], F["Yh"]
    n2 = p[0] ** 2 + p[1] ** 2 + p[2] ** 2
    dQ = T.grad(F["Phi"])
    dQdW = sum(dQ[i] * p[i] for i in range(3))
    g1 = C_N * f * (4.0 * (nu - 1.0) * n2 + 2.0 * ell * T.lap(F["W"]))
    g2 = 2.0 * C_N * ell * dQdW
    g4 = C_N * (gate_G(Yh) - ell * T.lap(F["W"]))
    return (g1 + g2 - g4) / (4.0 * np.pi * G_GRID), {"g1": g1, "g2": g2, "g4": g4}

def solve_fields(T, rho_b, a0g, ell=ELL):
    """On-shell linearized system (derivation.md Sec.6):
       u_b = -Delta^-1(4 pi G_N rho_b);  U = u_b / Q(k), Q = 1 - (1-<f>) ell S_k/4;
       W = S_h U; p = DW; y = |p|/a0g;  Y_h = J(DW) + ell Delta_h W - theta_g;
       f = G'(Y_h); nu = nu_mono(y).
       LAPSE:   Delta Phi = 4 pi G_N rho_b + S div[(nu-1) p]            (operative eq)
       SPATIAL: Delta Psi = 4 pi G_N rho_b + S div[(nu-1) p] + 4 pi G_N rho_slip
       slip = Psi - Phi."""
    u_b = T.poisson(4.0 * np.pi * G_GRID * rho_b)
    U = u_b.copy()
    for _ in range(3):
        W = T.filter_s(U)
        p = T.grad(W)
        y = np.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2) / a0g
        nu = nu_mono(y)
        Yh = kernel_J(p, a0g) + ell * T.lap(W) - THETA_G
        f = gate_f(Yh)
        Q = 1.0 - (1.0 - f.mean()) * ell * np.exp(-B_HEAT * T.k2q) / 4.0
        U = np.fft.irfftn(np.fft.rfftn(u_b) / Q, s=(T.N,) * 3)
    W = T.filter_s(U)
    p = T.grad(W)
    n2 = p[0] ** 2 + p[1] ** 2 + p[2] ** 2
    y = np.sqrt(n2) / a0g
    nu = nu_mono(y)
    Yh = kernel_J(p, a0g) + ell * T.lap(W) - THETA_G
    f = gate_f(Yh)
    j_ph = (nu - 1.0) * np.array(p)
    src = T.filter_s(T.div(j_ph))
    rho_ph = (1.0 / (4.0 * np.pi * G_GRID)) * src
    Phi = T.poisson(4.0 * np.pi * G_GRID * rho_b + src)
    F = {"u_b": u_b, "U": U, "W": W, "p": p, "y": y, "nu": nu, "Yh": Yh, "f": f,
         "j_ph": j_ph, "rho_ph": rho_ph, "Phi": Phi}
    rho_slip, slt = slip_source_analytic(F, T, ell)
    F["rho_slip"] = rho_slip
    F["slip_src"] = rho_slip * 4.0 * np.pi * G_GRID
    F["slip_terms"] = slt
    Psi = T.poisson(4.0 * np.pi * G_GRID * rho_b + src + 4.0 * np.pi * G_GRID * rho_slip)
    F["Psi"] = Psi
    F["slip"] = Psi - Phi
    F["a0g"] = a0g
    F["ell"] = ell
    return F

# ---------------------------------------------------------------------------
# 6. Exact 4-curvature of the static metric (full EH sector, no reduction)
# ---------------------------------------------------------------------------

def ricci_scalar4_static(T, Phi, Psi, LC=None):
    """Full R for ds^2 = -(1+2Phi) dt^2 + h_ij dx^i dx^j, static.
    Nonzero Christoffel: Gamma^i_00 (lapse) and Gamma^k_ij (spatial).
       R_00 = d_i Gamma^i_00 + Gamma^i_00 Gamma^k_ik
       R_ij = d_k Gamma^k_ij - d_j (Gamma^k_ik) + Gamma^a_ij Gamma^b_ab - Gamma^a_jb Gamma^b_ia
       R    = g^00 R_00 + h^ij R_ij
    Verified against the analytic reference: flat h, N=1+phi gives
    R = -(N Delta N + |DN|^2)/N^2 (exact)."""
    N2 = 1.0 + 2.0 * Phi
    if LC is None:
        LC = np.empty((3, 3) + Phi.shape)
        for i in range(3):
            for j in range(3):
                LC[i, j] = (1.0 - 2.0 * Psi) * (1.0 if i == j else 0.0)
    dPhi = T.grad(Phi)
    # inverse of the 3x3 spatial metric (analytic, pointwise)
    a = LC[0, 0]; b = LC[0, 1]; c = LC[0, 2]
    d = LC[1, 0]; e = LC[1, 1]; f = LC[1, 2]
    g = LC[2, 0]; h = LC[2, 1]; k = LC[2, 2]
    det = a * (e * k - f * h) - b * (d * k - f * g) + c * (d * h - e * g)
    hinv = np.empty((3, 3) + Phi.shape)
    hinv[0, 0] = (e * k - f * h) / det; hinv[0, 1] = (c * h - b * k) / det; hinv[0, 2] = (b * f - c * e) / det
    hinv[1, 0] = (f * g - d * k) / det; hinv[1, 1] = (a * k - c * g) / det; hinv[1, 2] = (c * d - a * f) / det
    hinv[2, 0] = (d * h - e * g) / det; hinv[2, 1] = (b * g - a * h) / det; hinv[2, 2] = (a * e - b * d) / det
    dH = np.empty((3, 3, 3) + Phi.shape)
    for i in range(3):
        for j in range(3):
            dH[i, j] = T.grad(LC[i, j])
    # Gamma^k_ij = (1/2) h^k sigma ( h_i sigma,j + h_j sigma,i - h_ij,sigma )
    Gam = np.empty((3, 3, 3) + Phi.shape)
    for kk in range(3):
        for i in range(3):
            for j in range(3):
                s = np.zeros_like(Phi)
                for l in range(3):
                    s += hinv[kk, l] * (dH[i, l][j] + dH[j, l][i] - dH[l, i][j])
                Gam[kk, i, j] = 0.5 * s
    N = np.sqrt(N2)
    Gam0 = np.array([N * sum(hinv[i, j] * dPhi[j] for j in range(3)) for i in range(3)])
    # traces
    trGam_i = np.array([sum(Gam[k, i, k] for k in range(3)) for i in range(3)])
    # R_00
    R00 = np.zeros_like(Phi)
    for i in range(3):
        R00 += T.D(i, Gam0[i])
        R00 += Gam0[i] * trGam_i[i]
    # R_ij
    Rij = np.empty((3, 3) + Phi.shape)
    for i in range(3):
        for j in range(3):
            acc = np.zeros_like(Phi)
            for kk in range(3):
                acc += T.D(kk, Gam[kk, i, j])
                acc -= T.D(j, Gam[kk, i, kk])
            for aa in range(3):
                for bb in range(3):
                    acc += Gam[aa, i, j] * Gam[bb, aa, bb]
                    acc -= Gam[aa, j, bb] * Gam[bb, i, aa]
            Rij[i, j] = acc
    R = np.zeros_like(Phi)
    R += -R00 / N2
    for i in range(3):
        for j in range(3):
            R += hinv[i, j] * Rij[i, j]
    return R

# ---------------------------------------------------------------------------
# 7. On-shell variation along a strain A^ij
# ---------------------------------------------------------------------------

def onshell_density(T, F, ell, a0g):
    """Quadratic on-shell density (units M_P^2/2):
       L = [2|DPsi|^2 - 4 DPhi.DPsi] + [-2 c_N |D(Phi-Z)|^2 - 4 c_N DZ.DU]
         + c_N [G(Y_h) + ell DPhi.DW],  Z = Phi - U on-shell."""
    dP = T.grad(F["Psi"]); dQ = T.grad(F["Phi"]); dW = T.grad(F["W"]); dU = T.grad(F["U"])
    EH = 2.0 * sum(dP[i] ** 2 for i in range(3)) - 4.0 * sum(dQ[i] * dP[i] for i in range(3))
    dZ = dQ - dU
    AUX = -2.0 * C_N * sum((dQ[i] - dZ[i]) ** 2 for i in range(3)) \
          - 4.0 * C_N * sum(dZ[i] * dU[i] for i in range(3))
    Yh = kernel_J(F["p"], a0g) + ell * T.lap(F["W"]) - THETA_G
    GATE = C_N * (gate_G(Yh) + ell * sum(dQ[i] * dW[i] for i in range(3)))
    return {"EH": EH, "AUX": AUX, "GATE": GATE}

def onshell_dLdeps(T, F, strain, ell, a0g, eps=1e-6):
    """d/deps of the on-shell reduced functional along A^ij:
       EH sector: exact central FD of the FULL sqrt(-g) R with h_ij(eps)
       AUX/GATE: analytic first order + exact on-shell responses
         (u_b -> du = -Delta^-1 dLapl u_b;  W -> dW = (dS)u + S du;  Y -> dY;  f -> df)
       Returns (dL, sectors)."""
    Phi, Psi, W = F["Phi"], F["Psi"], F["W"]
    def eh_density(eps):
        LC = np.empty((3, 3) + Phi.shape)
        for i in range(3):
            for j in range(3):
                LC[i, j] = (1.0 - 2.0 * Psi) * (1.0 if i == j else 0.0) - eps * strain.A[i, j]
        R = ricci_scalar4_static(T, Phi, Psi, LC=LC)
        N2 = 1.0 + 2.0 * Phi
        a = LC[0, 0]; b = LC[0, 1]; c = LC[0, 2]
        d = LC[1, 0]; e = LC[1, 1]; f = LC[1, 2]
        g = LC[2, 0]; h = LC[2, 1]; k = LC[2, 2]
        det = a * (e * k - f * h) - b * (d * k - f * g) + c * (d * h - e * g)
        return np.sqrt(N2 * det) * R
    dEH = (eh_density(eps) - eh_density(-eps)) / (2.0 * eps)

    # on-shell responses (exact first order)
    du = T.poisson(strain.dLapl(F["u_b"]))
    dW_t = strain.dFilterAct(F["u_b"]) + T.filter_s(du)
    dp = T.grad(dW_t)
    p = F["p"]
    dN2 = np.zeros_like(Phi)
    for i in range(3):
        for j in range(3):
            dN2 += strain.A[i, j] * p[i] * p[j]
    dN2 += 2.0 * sum(p[i] * dp[i] for i in range(3))
    dJ = 4.0 * (F["nu"] - 1.0) * dN2
    dLapW = strain.dLapl(W) + T.lap(dW_t)
    dY = dJ + ell * dLapW
    df = (gate_f(np.asarray(F["Yh"] + eps * dY, dtype=float)) -
          gate_f(np.asarray(F["Yh"] - eps * dY, dtype=float))) / (2.0 * eps)

    dQ = T.grad(Phi)
    dW0 = T.grad(W)
    dU0 = T.grad(F["U"])
    dZ0 = dQ - dU0
    # AUX: strain part + dU-response part + measure
    dAUX = np.zeros_like(Phi)
    for i in range(3):
        for j in range(3):
            dAUX += strain.A[i, j] * (-2.0 * C_N * (dQ[i] - dZ0[i]) * (dQ[j] - dZ0[j])
                                      - 4.0 * C_N * dZ0[i] * dU0[j])
    ddu = T.grad(du)
    dZres = -ddu
    dAUX += -2.0 * C_N * 2.0 * sum((dQ[i] - dZ0[i]) * dZres[i] for i in range(3))
    dAUX += -4.0 * C_N * (sum(dZ0[i] * ddu[i] for i in range(3)) + sum(dZres[i] * dU0[i] for i in range(3)))
    # GATE: chain + W-responses + measure
    dGdW = np.zeros_like(Phi)
    for i in range(3):
        for j in range(3):
            dGdW += strain.A[i, j] * dQ[i] * dW0[j]
    dGdW += sum(dQ[i] * dW_t[i] * 0.0 for i in range(3)) + sum(dQ[i] * dp[i] for i in range(3))
    dGATE = C_N * (df * dY + ell * dGdW)
    dm = strain.dMeasure()
    L0 = onshell_density(T, F, ell, a0g)
    dAUX = dAUX + L0["AUX"] * dm
    dGATE = dGATE + L0["GATE"] * dm
    return dEH + dAUX + dGATE, {"dEH": dEH, "dAUX": dAUX, "dGATE": dGATE}

# ---------------------------------------------------------------------------
# 8. Probes
# ---------------------------------------------------------------------------

N_MAIN, L_MAIN = 48, 16.0

def tune_source(T):
    """Unit-amplitude gaussian carrier, amplitude tuned to y_peak = 12."""
    rho0 = gaussian_bump(T, (L_MAIN / 2.0,) * 3, sigma=1.5)
    u1 = T.poisson(4.0 * np.pi * G_GRID * rho0)
    p1 = T.grad(T.filter_s(u1))
    y1 = np.sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2) / A0G
    amp = 12.0 / float(np.max(y1))
    return {"rho_b": rho0 * amp, "amp": amp}

def gaussian_bump(T, center, sigma=1.5):
    r2 = (T.X - center[0]) ** 2 + (T.Y - center[1]) ** 2 + (T.Z - center[2]) ** 2
    return np.exp(-r2 / (2.0 * sigma * sigma))

def eta_field(T, center, sigma=1.5):
    b = gaussian_bump(T, center, sigma)
    return np.array([T.D(i, b) for i in range(3)])

def rms(a):
    return float(np.sqrt(np.mean(np.asarray(a) ** 2)))

def mx(a):
    m = np.isfinite(a)
    return float(np.max(np.abs(a[m])))


# ---------------------------------------------------------------------------
# 8b. Probe subprocess workers (RSS partitioning): macOS allocator does not
#     return numpy churn to the OS, so each heavy probe runs in a short-lived
#     child (peak ~100-150 MB); the parent only accumulates tiny statistics.
# ---------------------------------------------------------------------------

def probe_worker_stdin():
    """Child entry: reads a JSON job line on stdin, prints RESULT_JSON=..."""
    signal.alarm(45)
    job = json.loads(sys.stdin.readline())
    npz, ctr, kind, ell = job["npz"], tuple(job["ctr"]), job["kind"], job["ell"]
    eps = job.get("eps", 1e-6)
    T = Torus3(job["N"], job["L"])
    F = {}
    with np.load(npz) as z:
        for k in z.files:
            F[k] = z[k]
    F["a0g"] = float(np.asarray(F["a0g"]))
    out = []
    dpath = None
    chi = gaussian_bump(T, ctr, sigma=1.5)
    chi = chi / np.sqrt(np.mean(chi ** 2))
    if kind == "trace":
        st = Strain(T, "trace", chi=chi)
        dL, sect = onshell_dLdeps(T, F, st, ell, F["a0g"], eps=eps)
        dpath = os.path.join(job["wdir"], "dL_%s.npy" % job["key"])
        np.save(dpath, dL)
        out.append({"kind": "trace", "rms": rms(dL), "max": mx(dL),
                    "sectors": {k: rms(v) for k, v in sect.items()}})
    else:
        et = eta_field(T, ctr, sigma=1.5)
        stT = Strain(T, "traceless", eta=et)
        dLt, _ = onshell_dLdeps(T, F, stT, ell, F["a0g"], eps=eps)
        dpath = os.path.join(job["wdir"], "dL_%s.npy" % job["key"])
        np.save(dpath, dLt)
        out.append({"kind": "traceless", "rms": rms(dLt), "max": mx(dLt)})
    print("RESULT_JSON=" + json.dumps({"probe": job["key"], "data": out, "path": dpath},
                                      sort_keys=True, default=float))
    sys.stdout.flush()
    return 0

def spawn_probe(job, parent_rss):
    env = dict(os.environ)
    for v in ("OPENBLAS", "OMP", "MKL", "NUMEXPR"):
        env.setdefault(v + "_NUM_THREADS", "1")
    env.setdefault("VECLIB_MAXIMUM_THREADS", "1")
    p = subprocess.run([sys.executable, "-B", "-c",
                        "import sys, as228_slip as A; sys.exit(A.probe_worker_stdin())"],
                       env=env,
                       input=json.dumps(job) + "\n", capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("probe worker failed: " + p.stderr[-2000:])
    line = [l for l in p.stdout.splitlines() if l.startswith("RESULT_JSON=")]
    if not line:
        raise RuntimeError("no RESULT_JSON: " + p.stdout[-2000:] + p.stderr[-2000:])
    r = json.loads(line[0][len("RESULT_JSON="):])
    if r.get("path"):
        r["field"] = np.load(r["path"])
    return r

def main():
    global _spawn_rss
    _spawn_rss = []
    res = {"kernels": {}, "branches": {}, "controls": {}, "probes": {}, "footings": {}, "bounds": {}}
    print("=" * 96)
    print("AS228 — independent galactic spatial and lapse potentials (slip = Psi - Phi)")
    print("=" * 96)

    res["kernels"]["landmarks"] = {"y_p": _YP, "h_p": _HP, "y_star": _Y_STAR,
                                   "splice_continuity": float(h_rar(_Y_STAR) - _H_STAR)}
    for nm, (nu, _) in BRANCHES.items():
        ys = np.array([0.05, 0.1, 0.5, 1.0, 2.0, _Y_STAR, 3.0, 10.0, 100.0])
        v = nu(ys)
        res["kernels"][nm] = {"nu_sample": [float(x) for x in v],
                              "all_nu_gt_1": bool(np.all(v > 1.0))}
    print("[0] landmarks: y_p=%.6g h_p=%.6g y_star=%.6g" % (_YP, _HP, _Y_STAR))

    N, L = 48, 16.0
    T = Torus3(N, L)
    rho0 = gaussian_bump(T, (L / 2.0, L / 2.0, L / 2.0), sigma=1.5)
    u1 = T.poisson(4.0 * np.pi * G_GRID * rho0)
    p1 = T.grad(T.filter_s(u1))
    y1 = np.sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2) / A0G
    AMP = 12.0 / float(np.max(y1))
    rho_b = rho0 * AMP
    res["source"] = {"amp": AMP, "y_peak": float(np.max(y1) * AMP)}
    print("[1] source tuned: amp=%.6e  (y_peak=%.2f)" % (AMP, np.max(y1) * AMP))

    for ell_cell in (0.04, 0.004, 0.0):
        print("\n[2] main cell ell = %g" % ell_cell)
        F = solve_fields(T, rho_b, A0G, ell=ell_cell)
        tag = "ell_%g" % ell_cell
        cell = {}
        cell["y_window"] = [float(np.min(F["y"])), float(np.max(F["y"]))]
        cell["frac_transition"] = float(np.mean((F["f"] > 1e-6) & (F["f"] < 1.0 - 1e-6)))
        cell["frac_active"] = float(np.mean(F["f"] > 1.0 - 1e-6))
        cell["nu_max"] = float(np.max(F["nu"]))
        cell["slip_rms"] = rms(F["slip"]); cell["slip_max"] = mx(F["slip"])
        cell["Phi_max"] = mx(F["Phi"]); cell["Psi_max"] = mx(F["Psi"])
        cell["rho_ph_max"] = mx(F["rho_ph"]); cell["rho_slip_max"] = mx(F["rho_slip"])
        cell["slip_over_Phi_max_ratio"] = mx(F["slip"]) / max(mx(F["Phi"]), 1e-30)
        ai = np.argmax(np.abs(F["slip"]))
        cell["y_at_max_slip"] = float(np.asarray(F["y"]).flat[ai])
        cell["f_at_max_slip"] = float(np.asarray(F["f"]).flat[ai])
        Rslip = T.lap(F["slip"]) - 4.0 * np.pi * G_GRID * F["rho_slip"]
        Rlap = T.lap(F["Phi"]) - 4.0 * np.pi * G_GRID * rho_b - T.filter_s(T.div(F["j_ph"]))
        cell["R_slip_max"] = mx(Rslip)
        cell["R_slip_rms"] = rms(Rslip)
        cell["R_lapse_max"] = mx(Rlap)
        gr = gate_G(F["Yh"]) - ell_cell * T.lap(F["W"])
        RN = C_N * (4.0 * T.lap(F["Psi"]) + 4.0 * C_N * T.lap(F["U"]) + C_N * gr) / (16.0 * np.pi * G_GRID * C_N)
        RN = RN - RN.mean()
        cell["R_lapse_onshell_max"] = mx(RN)
        cell["R_lapse_onshell_rms"] = rms(RN)
        Fsav = {k: v for k, v in F.items() if isinstance(v, np.ndarray) and v.dtype != object}
        Fsav["a0g"] = np.asarray(A0G)
        npz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields_ell%g.npz" % ell_cell)
        np.savez(npz, **Fsav)
        stat_t, stat_tl = [], []
        centers = [(L/2, L/2, L/2), (L/2+2.5, L/2, L/2), (L/2-3.5, L/2+1.5, L/2)]
        for ci, ctr in enumerate(centers):
            for kind in ("trace", "traceless"):
                job = {"npz": npz, "ctr": list(ctr), "kind": kind,
                       "ell": float(ell_cell), "N": N, "L": L,
                       "wdir": os.path.dirname(os.path.abspath(__file__)),
                       "key": "ell%g_c%d_%s" % (ell_cell, ci, kind)}
                r = spawn_probe(job, _spawn_rss)
                d = r["data"][0]
                if kind == "trace":
                    stat_t.append({"center": list(ctr), "rms": d["rms"], "max": d["max"],
                                   "sectors": d["sectors"]})
                else:
                    stat_tl.append({"center": list(ctr), "rms": d["rms"], "max": d["max"]})
        cell["stationarity_trace"] = stat_t
        cell["stationarity_traceless"] = stat_tl
        res["controls"][tag] = cell

    # ----- NEGATIVE CONTROL: assign Psi = Phi BEFORE varying the metric -----
    print("\n[NEG] no-slip branch tests")
    F = solve_fields(T, rho_b, A0G, ell=0.04)
    chi = gaussian_bump(T, (L/2, L/2, L/2), sigma=1.5)
    chi = chi / np.sqrt(np.mean(chi ** 2))
    npz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields_neg.npz")
    Fsav = {k: v for k, v in F.items() if isinstance(v, np.ndarray) and v.dtype != object}
    Fsav["a0g"] = np.asarray(A0G)
    np.savez(npz, **Fsav)
    Fn = dict(F); Fn["Psi"] = F["Phi"].copy()
    Fsavn = {k: v for k, v in Fn.items() if isinstance(v, np.ndarray) and v.dtype != object}
    Fsavn["a0g"] = np.asarray(A0G)
    np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields_noslip.npz"), **Fsavn)
    r1 = spawn_probe({"npz": npz, "ctr": [L/2, L/2, L/2], "kind": "trace", "ell": 0.04,
                      "N": N, "L": L, "wdir": os.path.dirname(os.path.abspath(__file__)),
                      "key": "neg_solved"}, _spawn_rss)
    r2 = spawn_probe({"npz": os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields_noslip.npz"),
                      "ctr": [L/2, L/2, L/2], "kind": "trace", "ell": 0.04,
                      "N": N, "L": L, "wdir": os.path.dirname(os.path.abspath(__file__)),
                      "key": "neg_noslip"}, _spawn_rss)
    dL_solv = r1["field"]; dL_nosi = r2["field"]
    tN = {"dEH": r2["data"][0]["sectors"]["dEH"], "dAUX": r2["data"][0]["sectors"]["dAUX"],
          "dGATE": r2["data"][0]["sectors"]["dGATE"]}
    dL_diff = dL_nosi - dL_solv
    res["controls"]["NEG"] = {
        "solved_rms": rms(dL_solv), "solved_max": mx(dL_solv),
        "no_slip_rms": rms(dL_nosi), "no_slip_max": mx(dL_nosi),
        "transition_stress_rms": rms(dL_diff), "transition_stress_max": mx(dL_diff),
        "sectors_no_slip": {k: rms(v) for k, v in tN.items()},
        "verdict": "FIRES" if mx(dL_diff) > 0.1 * mx(dL_nosi) else "CHECK",
    }
    rho_slip_ns, _ = slip_source_analytic(Fn, T, 0.04)
    res["controls"]["NEG"]["analytic_slip_src_rms"] = rms(rho_slip_ns)
    res["controls"]["NEG"]["analytic_slip_src_max"] = mx(rho_slip_ns)
    print("   no-slip residual rms=%.3e (solved rms=%.3e) -> %s"
          % (rms(dL_nosi), rms(dL_solv), res["controls"]["NEG"]["verdict"]))

    # ----- gate-idle limit: small source, f = 0 everywhere -> residual ~ 0 -----
    rho_s = rho0 * 0.7 * AMP * 0.01
    Fi = solve_fields(T, rho_s, A0G, ell=0.04)
    Fsav = {k: v for k, v in Fi.items() if isinstance(v, np.ndarray) and v.dtype != object}
    Fsav["a0g"] = np.asarray(A0G)
    np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields_idle.npz"), **Fsav)
    r3 = spawn_probe({"npz": os.path.join(os.path.dirname(os.path.abspath(__file__)), "fields_idle.npz"),
                      "ctr": [L/2, L/2, L/2], "kind": "trace", "ell": 0.04,
                      "N": N, "L": L, "wdir": os.path.dirname(os.path.abspath(__file__)),
                      "key": "idle"}, _spawn_rss)
    dL_idle = r3["field"]
    res["controls"]["gate_idle"] = {
        "y_max": float(np.max(Fi["y"])), "f_max": float(np.max(Fi["f"])),
        "no_slip_residual_rms": rms(dL_idle), "no_slip_residual_max": mx(dL_idle),
        "slip_rms": rms(Fi["slip"]),
        "verdict": "ZERO_LIMIT_OK" if rms(Fi["slip"]) < 0.05 * rms(F["slip"]) else "CHECK",
    }
    print("   idle-gate residual rms=%.3e (slip rms=%.3e, f_max=%.3g) -> %s"
          % (rms(dL_idle), rms(Fi["slip"]), float(np.max(Fi["f"])),
             res["controls"]["gate_idle"]["verdict"]))

    # ----- branch dictionary (comparison only) -----
    for nm in BRANCHES:
        u2 = T.poisson(4.0 * np.pi * G_GRID * rho_b)
        W2 = T.filter_s(u2)
        p2 = T.grad(W2)
        y2 = np.sqrt(p2[0] ** 2 + p2[1] ** 2 + p2[2] ** 2) / A0G
        nu2 = BRANCHES[nm][0](y2)
        j2 = (nu2 - 1.0) * np.array(p2)
        rp2 = (1.0 / (4.0 * np.pi * G_GRID)) * T.filter_s(T.div(j2))
        res["branches"][nm] = {"rho_ph_max": mx(rp2), "nu_max": float(np.max(nu2))}
    print("[3] branch phantom peaks (comparison; MONO operative): " +
          ", ".join("%s=%.3e" % (nm, res["branches"][nm]["rho_ph_max"]) for nm in res["branches"]))

    # ----- refinement N=96 -----
    T96 = Torus3(96, L)
    rho96 = gaussian_bump(T96, (L/2, L/2, L/2), sigma=1.5) * AMP
    F96 = solve_fields(T96, rho96, A0G, ell=0.04)
    R96s = T96.lap(F96["slip"]) - 4.0 * np.pi * G_GRID * F96["rho_slip"]
    res["controls"]["refinement_N96"] = {"R_slip_max": mx(R96s),
                                         "slip_rms": rms(F96["slip"]),
                                         "slip_max": mx(F96["slip"])}
    print("[4] refinement N96: R_slip_max=%.3e slip_rms=%.3e" % (mx(R96s), rms(F96["slip"])))

    # ----- projector stress probe (synthetic carrier density rho_d != 0) -----
    rho_d = 0.05 * rho_b * (1.0 + 0.3 * np.cos(2.0 * np.pi * T.X / L))
    zs = T.poisson((rho_d - rho_d.mean()) / (2.0 * C_N * 16.0 * np.pi * G_GRID))
    proj_trace = -3.0 * float(rho_d.mean()) * zs
    res["probes"]["projector_trace_stress"] = {
        "rho_d_mean": float(rho_d.mean()),
        "trace_rms": rms(proj_trace), "trace_max": mx(proj_trace),
        "note": "Delta T^ij_mean = -[<N rho_d>_h/N] z h^ij (FINAL_ACTION eq.9): "
                "vanishes identically for rho_d = 0; probe shows the operator active."}

    # ----- both footings -----
    MB = 1.0e10 * M_SUN
    for nm, ft in FOOTINGS.items():
        rM = np.sqrt(G_SI * MB / ft["a0"])
        res["footings"][nm] = {"a0": ft["a0"], "rho_Lambda": ft["rho_Lambda"],
                               "a0_roundtrip": ft["a0_roundtrip"], "a0_relerr": ft["a0_relerr"],
                               "rM_m": float(rM), "rM_pc": float(rM / PC_SI)}
    ch = resource.getrusage(resource.RUSAGE_CHILDREN)
    res["bounds"] = {"declared_wall_s": 120,
                     "enforced": "signal.alarm(120) in-script; probe probes run in "
                                 "short-lived subprocesses (signal.alarm(45) each) "
                                 "because macOS does not return numpy churn to the OS",
                     "threads": "OPENBLAS/OMP/MKL/NUMEXPR/VECLIB=1",
                     "recorded_wall_s": float(time.time() - T0),
                     "max_child_rss_mb": float(ch.ru_maxrss / 1024.0),
                     "n_child_probes": len(_spawn_rss)}
    print("\n[bounds] wall = %.2f s" % res["bounds"]["recorded_wall_s"])
    with open("raw_output.json", "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True, default=float)
    print("RESULT_JSON=" + json.dumps(res, sort_keys=True, default=float))
    return 0

if __name__ == "__main__":
    import as228_phase
    sys.exit(as228_phase.driver_main())