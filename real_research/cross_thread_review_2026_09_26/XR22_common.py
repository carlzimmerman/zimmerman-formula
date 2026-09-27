#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR22_common -- shared machinery for review lane XR22 (the derivation chain's law for wide binaries, confronted with the frozen
Gaia DR4 pre-registration).  Imported by XR22_force_law.py and XR22_prereg_statistic.py; it writes nothing and runs nothing
on import.

THE LAW (the chain's z = 0 static limit, FP7 R7d with FP14's c_2 -> oo, lambda = 0 and FP13's separator reduced locally):
    g = g_N + S grad(phi),      div[ mu_s(|grad phi|/a0) grad phi ] = 4 pi G S rho,      mu_s(x) = x/(1 - 2x)   (J_P2 in AQUAL form)
    S = exp(xi^2 Laplacian/2): the heat filter (Fourier e^{-xi^2 k^2/2}, a Gaussian of std xi in real space), applied to the
    source AND to the output (FP7 A1b: the double filter is forced).  The Galaxy enters as the uniform background gradient
    x_e e_z of the scalar with mu_s(x_e) x_e = eta, eta = the Newtonian Galactic field in units of a0 (P2 inversion of the
    observed field).  Units in the solvers: G M_tot = a0 = 1, so lengths are in r_M = sqrt(G M_tot/a0).

PLUG-INS (the coordinator's request: a different screening term must drop in):
    Law     -- the scalar's constitutive law: mu(x), dmu(x), the energy density W(x) (W' = mu x) and the barrier x_max.  An
               optional position-dependent term c(r) G(x) (flux c(r) G'(x)/x p) can be attached through `extra`, which the
               3-D solver adds to the energy, the flux and the Hessian.  Shipped: LAW_P2 (the chain), LAW_DEEP (mu = x).
    Filter  -- a Fourier multiplier applied to the source and (optionally) to the output: HeatFilter(xi); IdentityFilter.
    Anything that is not a local constitutive law (e.g. BDEF's Riemann-coupled Galileon, whose term contains phi_{;mu nu} R)
    needs its own field equation first; XR22 scores it only in FP17's own spherical reduction (an ESTIMATE, labelled).

SOLVERS
    lin_kernel(...)  the exact free-space LINEAR response (EFE-dominated regime) with the double filter, by the Schwinger
                     representation 1/A = Int_0^oo dt e^{-tA}:  G(x) = -(4 pi)^{-1/2} Int dt a_T^{-1} a_L^{-1/2}
                     exp(-rho^2/4a_T - z^2/4a_L),  a_j = xi^2 + t mu_j  (mu_T = mu_s(x_e), mu_L = (x mu_s)'(x_e)).
    solve3d(...)     the full NONLINEAR problem on a periodic box: pseudo-spectral (exact derivatives, odd N), Newton on the
                     convex energy with a preconditioned-CG inner solve (preconditioner = the far-field operator, inverted by
                     FFT), a barrier-aware line search; periodic images are removed by the linear image correction
                     a = a_NL,periodic - a_L,periodic + a_L,free.
    solve2d(...)     an INDEPENDENT axisymmetric P1 finite-element Newton solver in free space (Dirichlet far field), for
                     the separation parallel to the Galactic field and for isolated (deep-MOND) two-body controls.

THE PRE-REGISTRATION'S MACHINERY (read-only; nothing in prep_2026/gaia_dr4_prep is written, moved or re-saved):
    load_pipeline()  exec's the frozen wide_binary_pipeline.py source into a private namespace (no bytecode is written).
    RegisteredEstimator  the theory-to-gamma_v path Amendments 11 and 12 register (g03y / L47 run_estimator, mirrored
                     line by line, including its clipping and its M_obs-based r3d), cached so the population and the model
                     medians are built once per a0; a control checks it is bit-identical to the direct call.
"""
import os, sys, io, json, math, time, contextlib
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CHAIN = os.path.join(REPO, "real_research", "derivation_chain_2026")
PREREG = os.path.join(REPO, "prep_2026", "gaia_dr4_prep")
CLOSURE = os.path.join(REPO, "qwen_claude_field_theory", "closure_2026")

# physical constants (the chain's own, FP7/FP17)
G_SI = 6.67430e-11
GM_SUN = 1.32712440018e20
AU_M = 1.495978707e11
KAU_M = 1e3 * AU_M
PC_M = 3.0856775814913673e16
C_SI = 299792458.0
KPC_M = 1e3 * PC_M


# ================================================================================================ the chain's committed inputs
def load_json(path):
    with open(path) as f:
        return json.load(f)


def chain_inputs():
    """every number XR22 takes from the chain, read from the committed result files (read-only)."""
    fp0 = load_json(os.path.join(CHAIN, "FP0_core_postulates_results.json"))["numbers"]
    fp7 = load_json(os.path.join(CHAIN, "FP7_aqual_type_repair_results.json"))["numbers"]["A4"]
    fp13 = load_json(os.path.join(CHAIN, "FP13_separator_from_state_results.json"))["numbers"]["H1"]
    fp14 = load_json(os.path.join(CHAIN, "FP14_zero_knob_core_results.json"))
    fp17 = load_json(os.path.join(CHAIN, "FP17_screening_without_xi_results.json"))["numbers"]
    a0 = {"canonical": fp0["a0_canonical"], "alt": fp0["a0_rho_total"]}
    floors = {f: fp7["AQUAL_floors"][f]["floor"] for f in a0}
    f14 = {r_["link"]: r_ for r_ in fp14["ledger"]}
    return dict(a0=a0, H_Lambda=fp0["H_Lambda"], xi_floor_pc=floors, xi_floor_binding={f: fp7["AQUAL_floors"][f]["binding"] for f in a0},
                xi_qumond_pc=fp7["QUMOND_floors"], L0_kpc=fp13["L_kpc"]["0.0"], yth0=fp13["yth"]["0.0"],
                F14p=f14.get("F14p", {}).get("what", ""), F14d=f14.get("F14d", {}).get("what", ""),
                V4=fp17["V4"], R2=fp17.get("R2"), B1=fp17.get("B1"))


# ================================================================================================ plug-in laws and filters
class Law:
    """the scalar's constitutive law in two-field AQUAL form: flux F = mu(x) p, energy density W(x), W'(x) = mu(x) x."""

    def __init__(self, name, mu, dmu, W, xmax, extra=None, closed_form_p2=False):
        self.name, self.mu, self.dmu, self.W, self.xmax, self.extra = name, mu, dmu, W, xmax, extra
        self.closed_form_p2 = closed_form_p2

    def mu_eff(self, x, c=0.0):
        """the local constitutive function with the plug-in term c G(x) folded in: mu + c G'(x)/x"""
        x = np.asarray(x, float)
        if self.extra is None or np.all(np.asarray(c) == 0):
            return self.mu(x)
        return self.mu(x) + c * self.extra["dG"](x) / np.maximum(x, 1e-300)

    def dmu_eff(self, x, c=0.0):
        x = np.asarray(x, float)
        if self.extra is None or np.all(np.asarray(c) == 0):
            return self.dmu(x)
        xs = np.maximum(x, 1e-300)
        return self.dmu(x) + c * (self.extra["d2G"](x) / xs - self.extra["dG"](x) / xs ** 2)

    def stiffness(self, eta):
        """background x_e (flux balance mu_eff(x_e) x_e = eta with the plug-in term at its far-field value c_inf) and the linear
        stiffnesses mu_T = mu_eff(x_e), mu_L = (x mu_eff)'(x_e)"""
        c = self.extra["c_inf"] if self.extra is not None else 0.0
        if self.extra is None and self.closed_form_p2:
            xe = math.sqrt(eta * eta + eta) - eta
        else:
            from scipy.optimize import brentq
            hi = min(self.xmax * (1 - 1e-12), 1e6)
            xe = brentq(lambda x: float(self.mu_eff(np.array(x), c)) * x - eta, 1e-300, hi, xtol=1e-16, rtol=1e-15)
        muT = float(self.mu_eff(np.array(xe), c))
        muL = muT + xe * float(self.dmu_eff(np.array(xe), c))
        return xe, muT, muL


LAW_P2 = Law("P2 two-field AQUAL (J_P2, mu_s = x/(1-2x))",
             lambda x: x / (1.0 - 2.0 * x), lambda x: 1.0 / (1.0 - 2.0 * x) ** 2,
             lambda x: -0.25 * x * x - 0.25 * x - 0.125 * np.log1p(-2.0 * x), 0.5, closed_form_p2=True)
LAW_DEEP = Law("deep MOND (mu = x)", lambda x: x, lambda x: np.ones_like(x), lambda x: x ** 3 / 3.0, np.inf)


class HeatFilter:
    """S = exp(xi^2 Laplacian/2): Fourier multiplier e^{-xi^2 k^2/2}; real space a normalised Gaussian of std xi."""

    def __init__(self, xi):
        self.xi = float(xi)

    def hat(self, K2):
        return np.exp(-0.5 * self.xi * self.xi * K2)

    def density(self, m, r2):
        s = self.xi
        return m * (2 * np.pi * s * s) ** -1.5 * np.exp(-0.5 * r2 / (s * s))


class IdentityFilter:
    """no filter (S = 1): only for the linear kernel's xi -> 0 limit; a grid solver needs a resolved source"""
    xi = 0.0

    def hat(self, K2):
        return np.ones_like(K2)


def with_extra(law, c_field, c_inf, G, dG, d2G, name=None, key_force=None):
    """a plug-in screening term: energy density + c(r) G(|grad phi|), flux + c(r) G'(x)/x grad phi.  c_field(box, bodies) returns
    a grid array (or a scalar); c_inf is its far-field value (it sets the background and the preconditioner).  If the key c
    reads the matter configuration, the matter feels -(1/4 pi) Int G(x) dc/dp_b as well: key_force(box, bodies, Gx) must
    return that force per body (momentum conservation, checked by the solver's diagnostic, fails without it)."""
    return Law(name or (law.name + " + plug-in"), law.mu, law.dmu, law.W, law.xmax,
               extra=dict(c_field=c_field, c_inf=c_inf, G=G, dG=dG, d2G=d2G, key_force=key_force))


def eta_of_gobs(g):
    """P2 inversion of the observed field g (units a0): g = sqrt(eta^2 + eta) -> the Newtonian field eta."""
    return 0.5 * (-1.0 + math.sqrt(1.0 + 4.0 * g * g))


# ================================================================================================ the exact linear kernel
def lin_kernel_grad(pts, xi, muT, muL, nq=3001, span=26.0):
    """gradient (outward positive) of the free-space Green function of div(A0 grad) for a UNIT mass, convolved with a Gaussian
    of variance 2 xi^2 per axis (the double heat filter), e along z.  pts: (n, 3) array.  Schwinger representation with a
    trapezoid in u = ln(t/t0) (spectrally accurate for this smooth, doubly-exponentially decaying integrand)."""
    pts = np.atleast_2d(np.asarray(pts, float))
    out = np.zeros_like(pts)
    for i, (x, y, z) in enumerate(pts):
        rho2 = x * x + y * y
        t0 = max((rho2 + z * z) / (4.0 * min(muT, muL)), xi * xi / max(muT, muL), 1e-300)
        u = np.linspace(-span, span, nq)
        t = t0 * np.exp(u)
        aT = xi * xi + t * muT
        aL = xi * xi + t * muL
        base = (4 * np.pi) ** -0.5 * t / (aT * np.sqrt(aL)) * np.exp(-rho2 / (4 * aT) - z * z / (4 * aL))
        out[i, 0] = np.trapz(base * x / (2 * aT), u)
        out[i, 1] = np.trapz(base * y / (2 * aT), u)
        out[i, 2] = np.trapz(base * z / (2 * aL), u)
    return out


def lin_boost(s, theta, xi, muT, muL, filt_var=2.0):
    """radial and tangential relative-force boosts of the linear kernel for separation s at angle theta to the field
    (units r_M, total mass 1).  filt_var = 2 (double filter, the chain) or 1 (source filter only, MUTATE)."""
    n = np.array([math.sin(theta), 0.0, math.cos(theta)])
    g = lin_kernel_grad(s * n[None, :], xi * math.sqrt(filt_var / 2.0), muT, muL)[0]
    rad = 1.0 + s * s * float(g @ n)
    tan = s * s * float(np.linalg.norm(g - (g @ n) * n))
    return rad, tan, g


def analytic_tensor(theta, muT, muL):
    """the unfiltered (xi -> 0) EFE-saturated radial boost of two-field AQUAL: 1 + [1/(mu_T sqrt mu_L)]/sqrt(sin^2/mu_T + cos^2/mu_L)"""
    return 1.0 + (1.0 / (muT * math.sqrt(muL))) / math.sqrt(math.sin(theta) ** 2 / muT + math.cos(theta) ** 2 / muL)


def orient_avg_exact(muT, muL):
    """sphere average of the unfiltered radial boost over u = cos(theta) in [0, 1] (closed form)"""
    a, b = 1.0 / muT, 1.0 / muT - 1.0 / muL
    return 1.0 + (1.0 / (muT * math.sqrt(muL))) * math.asin(math.sqrt(b / a)) / math.sqrt(b)


# ================================================================================================ 3-D periodic nonlinear solver
def smooth_odd(n):
    """smallest odd 3-5-7-smooth integer >= n (fast FFT sizes)"""
    m = int(math.ceil(n))
    if m % 2 == 0:
        m += 1
    while True:
        k = m
        for p_ in (3, 5, 7):
            while k % p_ == 0:
                k //= p_
        if k == 1:
            return m
        m += 2


class Box3D:
    def __init__(self, N, L, workers=1):
        import scipy.fft as sfft
        assert N % 2 == 1
        self.sfft, self.workers = sfft, workers
        self.N, self.L, self.h = N, L, L / N
        self.x = (np.arange(N) - (N - 1) // 2) * self.h
        self.x0 = self.x[0]
        k = 2 * np.pi * np.fft.fftfreq(N, d=self.h)
        kz = 2 * np.pi * np.fft.rfftfreq(N, d=self.h)
        self.KX, self.KY, self.KZ = k[:, None, None], k[None, :, None], kz[None, None, :]
        self.K2 = self.KX ** 2 + self.KY ** 2 + self.KZ ** 2
        self.shape = (N, N, N)

    def fwd(self, f):
        return self.sfft.rfftn(f, workers=self.workers)

    def inv(self, F):
        return self.sfft.irfftn(F, s=self.shape, workers=self.workers)

    def grad_hat(self, F):
        return [self.inv(1j * K * F) for K in (self.KX, self.KY, self.KZ)]

    def div(self, q):
        return self.inv(sum(1j * K * self.fwd(qj) for K, qj in zip((self.KX, self.KY, self.KZ), q)))

    def point_hat(self, m, p):
        """DFT coefficients (per grid convention) of a unit-normalised point source at p, times m (before filtering)"""
        ph = self.KX * (p[0] - self.x0) + self.KY * (p[1] - self.x0) + self.KZ * (p[2] - self.x0)
        return m * np.exp(-1j * ph) / self.h ** 3

    def eval_at(self, F, p):
        """exact trigonometric interpolation of the grid field with half-spectrum F at the point p"""
        ph = np.exp(1j * (self.KX * (p[0] - self.x0) + self.KY * (p[1] - self.x0) + self.KZ * (p[2] - self.x0)))
        w = np.full(F.shape[-1], 2.0)
        w[0] = 1.0
        if self.N % 2 == 0:
            w[-1] = 1.0
        return float(np.real(np.sum(F * ph * w[None, None, :]))) / self.N ** 3


def box_for(s, xi, hfac=2.5, margin=9.0, nmax=231):
    """production box: L = s + 2 max(margin, 6 xi) (units r_M), h = xi/hfac, N the next smooth odd size (capped)."""
    L = s + 2.0 * max(margin, 6.0 * xi)
    N = smooth_odd(L / (xi / hfac))
    if N > nmax:
        N = nmax if nmax % 2 == 1 else nmax - 1
    return N, L


def solve3d(law, filt, eta, bodies, N, L, tol=1e-10, workers=1, output_filter=True, cg_max=500, newton_max=40, verbose=False,
            linear_only=False):
    """the nonlinear two-field AQUAL problem for Gaussian-filtered bodies [(m, p)] (sum m = 1) in the uniform background x_e e_z.
    Returns the relative-acceleration boosts of bodies[1] relative to bodies[0] along n = (p1 - p0)/|p1 - p0|, image-corrected."""
    t0 = time.time()
    box = Box3D(N, L, workers)
    xe, muT0, muL0 = law.stiffness(eta)
    den = muT0 * (box.KX ** 2 + box.KY ** 2) + muL0 * box.KZ ** 2
    den[0, 0, 0] = 1.0
    Pinv = 1.0 / den
    Pinv[0, 0, 0] = 0.0
    Fh = filt.hat(box.K2)
    Pb = [box.point_hat(m, p) for m, p in bodies]
    Sb = [P_ * Fh for P_ in Pb]                                   # filtered bodies (source leg)
    Shat = sum(Sb)
    Shat[0, 0, 0] = 0.0
    src = box.inv(4 * np.pi * Shat)
    Ob = Sb if output_filter else Pb                              # output leg: filtered (the chain) or point bodies (MUTATE)
    ms = [m for m, _ in bodies]
    pos = [np.asarray(p, float) for _, p in bodies]

    def forces(phi_hat):
        g_hat = [1j * K * phi_hat for K in (box.KX, box.KY, box.KZ)]
        out = []
        for b in range(len(bodies)):
            if output_filter:
                rb = box.inv(Ob[b])
                out.append(np.array([-box.h ** 3 * np.sum(rb * box.inv(gh)) for gh in g_hat]))
            else:
                out.append(np.array([-ms[b] * box.eval_at(gh, pos[b]) for gh in g_hat]))
        return out

    phiL_hat = -4 * np.pi * Shat * Pinv
    FL = forces(phiL_hat)
    if linear_only:
        n = pos[1] - pos[0]
        s = float(np.linalg.norm(n))
        n = n / s
        a_lp = FL[1] / ms[1] - FL[0] / ms[0]
        return dict(B_lin_per=1.0 - s * s * float(a_lp @ n), N=N, L=L, h=box.h, time=time.time() - t0)
    phi = box.inv(phiL_hat)
    ex = law.extra
    cf = 0.0 if ex is None else ex["c_field"](box, bodies)

    def fields(ph):
        g = box.grad_hat(box.fwd(ph))
        p = [g[0], g[1], g[2] + xe]
        return p, np.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2)

    # feasible start: scale the linear guess until |grad phi| < x_max
    p, x = fields(phi)
    scale = 1.0
    while np.max(x) >= law.xmax * (1 - 1e-6) and scale > 1e-3:
        scale *= 0.7
        p, x = fields(phi * scale)
    phi = phi * scale

    Fe = float(law.mu(np.array(xe))) * xe
    We = float(law.W(np.array(xe)))
    srcn = math.sqrt(np.mean(src ** 2))

    def energy(ph):
        p, x = fields(ph)
        if np.max(x) >= law.xmax:
            return np.inf
        w = law.W(x) - We - Fe * (p[2] - xe)
        if ex is not None:
            w = w + cf * (ex["G"](x) - float(ex["G"](np.array(xe))))
        return box.h ** 3 * (np.sum(w) + np.sum(src * ph))

    def residual(ph):
        p, x = fields(ph)
        m = law.mu_eff(x, cf)
        R = box.div([m * p[0], m * p[1], m * p[2]]) - src
        return R, p, x

    hist, cgits, steps = [], [], []
    for it in range(newton_max):
        R, p, x = residual(phi)
        rn = math.sqrt(np.mean(R ** 2)) / srcn
        hist.append(rn)
        if verbose:
            print(f"      newton {it}: |R|/|src| = {rn:.2e}  x in [{x.min():.4f}, {x.max():.4f}]", flush=True)
        if rn < tol:
            break
        m = law.mu_eff(x, cf)
        c = law.dmu_eff(x, cf) / np.maximum(x, 1e-12)

        def Hv(v):
            g = box.grad_hat(box.fwd(v))
            pg = p[0] * g[0] + p[1] * g[1] + p[2] * g[2]
            return -box.div([m * g[j] + c * pg * p[j] for j in range(3)])

        def Pv(r):
            return box.inv(box.fwd(r) * Pinv)
        b = R - R.mean()
        d = np.zeros_like(b)
        r = b.copy()
        z = Pv(r)
        pp = z.copy()
        rz = float(np.sum(r * z))
        bn = math.sqrt(max(rz, 1e-300))
        eta_k = min(0.1, max(1e-4, math.sqrt(rn))) if rn > 1e-6 else 1e-5
        k_ = 0
        for k_ in range(cg_max):
            Ap = Hv(pp)
            alpha = rz / float(np.sum(pp * Ap))
            d += alpha * pp
            r -= alpha * Ap
            z = Pv(r)
            rz_new = float(np.sum(r * z))
            if math.sqrt(abs(rz_new)) < eta_k * bn:
                break
            pp = z + (rz_new / rz) * pp
            rz = rz_new
        cgits.append(k_ + 1)
        t = 1.0
        E0 = None
        while True:
            trial = phi + t * d
            Rt, pt, xt = residual(trial)
            if np.max(xt) < law.xmax:
                if math.sqrt(np.mean(Rt ** 2)) / srcn < (1 - 1e-4 * t) * rn:
                    break
                if E0 is None:
                    E0 = energy(phi)
                if energy(trial) < E0 - 1e-4 * t * float(np.sum(R * d)) * box.h ** 3:
                    break
            if t < 1e-9:
                break
            t *= 0.5
        steps.append(t)
        phi = trial
    F = forces(box.fwd(phi))
    if ex is not None and ex.get("key_force") is not None:
        p, x = fields(phi)
        KF = ex["key_force"](box, bodies, ex["G"](x))
        F = [F[b] + KF[b] for b in range(len(F))]
    n = pos[1] - pos[0]
    s = float(np.linalg.norm(n))
    n = n / s
    a_nl = F[1] / ms[1] - F[0] / ms[0]
    a_lp = FL[1] / ms[1] - FL[0] / ms[0]
    theta = math.acos(max(-1.0, min(1.0, float(n[2]))))
    xi_eff = filt.xi if output_filter else filt.xi / math.sqrt(2.0)
    g_free = lin_kernel_grad(s * n[None, :], xi_eff, muT0, muL0)[0]
    a_lf = -g_free
    a = a_nl - a_lp + a_lf
    B_rad = 1.0 - s * s * float(a @ n)
    B_tan = s * s * float(np.linalg.norm(a - (a @ n) * n))
    return dict(B=B_rad, B_tan=B_tan, B_lin_free=1.0 - s * s * float(a_lf @ n), B_lin_per=1.0 - s * s * float(a_lp @ n),
                B_nl_per=1.0 - s * s * float(a_nl @ n), newton=len(hist), res=hist[-1], cg=cgits, steps=steps,
                momentum=float(np.linalg.norm(F[0] + F[1]) / max(np.linalg.norm(F[1]), 1e-300)),
                xrange=(float(x.min()), float(x.max())), N=N, L=L, h=box.h, time=time.time() - t0, theta=theta, s=s)


def angular_interp(theta, B3, Blin3, Blin_theta):
    """the radial boost at any angle from three solved angles (0, 45, 90 deg): the exact linear kernel's angular shape times a
    nonlinear correction factor C = (B - 1)/(B_lin - 1), interpolated as a quadratic in cos^2(theta) through the three nodes.
    B3, Blin3: arrays (..., 3) at 0/45/90; Blin_theta: the linear boost at theta (same leading shape)."""
    c2 = np.cos(theta) ** 2
    C = (np.asarray(B3) - 1.0) / np.where(np.abs(np.asarray(Blin3) - 1.0) > 1e-14, np.asarray(Blin3) - 1.0, 1e-14)
    x0, x1, x2 = 1.0, 0.5, 0.0                                     # cos^2 at 0, 45, 90 deg
    L0 = (c2 - x1) * (c2 - x2) / ((x0 - x1) * (x0 - x2))
    L1 = (c2 - x0) * (c2 - x2) / ((x1 - x0) * (x1 - x2))
    L2 = (c2 - x0) * (c2 - x1) / ((x2 - x0) * (x2 - x1))
    Cth = C[..., 0] * L0 + C[..., 1] * L1 + C[..., 2] * L2
    return 1.0 + (np.asarray(Blin_theta) - 1.0) * Cth


def pair_bodies(s, theta, q=1.0):
    """two bodies of total mass 1, mass ratio q = m2/m1, barycentre at the origin, separation s at angle theta to e_z"""
    m1, m2 = 1.0 / (1.0 + q), q / (1.0 + q)
    n = np.array([math.sin(theta), 0.0, math.cos(theta)])
    return [(m1, -m2 * s * n), (m2, m1 * s * n)]


# ================================================================================================ 2-D axisymmetric FEM solver
def stretched_sym(a, b, h, R, grow):
    n = max(2, int(round((b - a) / h)))
    core = np.linspace(a, b, n + 1)
    right, left = [b], [a]
    d = h
    while right[-1] < R:
        d *= grow
        right.append(right[-1] + d)
    d = h
    while left[-1] > -R:
        d *= grow
        left.append(left[-1] - d)
    return np.concatenate([np.array(left[::-1][:-1]), core, np.array(right[1:])])


def stretched_pos(h, a, R, grow):
    n = max(1, int(round(a / h)))
    core = np.linspace(0.0, a, n + 1)
    out = [a]
    d = h
    while out[-1] < R:
        d *= grow
        out.append(out[-1] + d)
    return np.concatenate([core, np.array(out[1:])])


class Mesh2D:
    """structured (rho, z) mesh, each cell split into two P1 triangles (alternating diagonals); 7-point degree-5 quadrature"""

    def __init__(self, rn, zn):
        import scipy.sparse as sps
        nr, nz = len(rn), len(zn)
        R, Z = np.meshgrid(rn, zn, indexing="ij")
        self.R, self.Z = R.ravel(), Z.ravel()
        idx = np.arange(nr * nz).reshape(nr, nz)
        tris = []
        for i in range(nr - 1):
            a = idx[i, :-1]; b = idx[i + 1, :-1]; c = idx[i, 1:]; d = idx[i + 1, 1:]
            if i % 2 == 0:
                tris += [np.stack([a, b, d], 1), np.stack([a, d, c], 1)]
            else:
                tris += [np.stack([a, b, c], 1), np.stack([b, d, c], 1)]
        T = np.concatenate(tris)
        self.T = T
        xr, xz = self.R[T], self.Z[T]
        det = (xr[:, 1] - xr[:, 0]) * (xz[:, 2] - xz[:, 0]) - (xr[:, 2] - xr[:, 0]) * (xz[:, 1] - xz[:, 0])
        self.area = 0.5 * np.abs(det)
        br = np.stack([xz[:, 1] - xz[:, 2], xz[:, 2] - xz[:, 0], xz[:, 0] - xz[:, 1]], 1) / det[:, None]
        bz = np.stack([xr[:, 2] - xr[:, 1], xr[:, 0] - xr[:, 2], xr[:, 1] - xr[:, 0]], 1) / det[:, None]
        self.w = 2 * np.pi * xr.mean(1) * self.area
        nt = len(T)
        rows = np.repeat(np.arange(nt), 3)
        self.Gr = sps.csr_matrix((br.ravel(), (rows, T.ravel())), shape=(nt, nr * nz))
        self.Gz = sps.csr_matrix((bz.ravel(), (rows, T.ravel())), shape=(nt, nr * nz))
        bary = np.array([[1 / 3, 1 / 3, 1 / 3], [0.0597158717, 0.4701420641, 0.4701420641], [0.4701420641, 0.0597158717, 0.4701420641],
                         [0.4701420641, 0.4701420641, 0.0597158717], [0.7974269853, 0.1012865073, 0.1012865073],
                         [0.1012865073, 0.7974269853, 0.1012865073], [0.1012865073, 0.1012865073, 0.7974269853]])
        wq = np.array([0.225, 0.1323941527, 0.1323941527, 0.1323941527, 0.1259391805, 0.1259391805, 0.1259391805])
        self.qr, self.qz = bary @ xr.T, bary @ xz.T
        self.qw = wq[:, None] * self.area[None, :] * 2 * np.pi * self.qr
        self.bary = bary
        bnd = np.zeros((nr, nz), bool)
        bnd[-1, :] = True
        bnd[:, 0] = True
        bnd[:, -1] = True
        self.bnd = bnd.ravel()
        self.shape = (nr, nz)


def solve2d(law, filt, xe, bodies_z, mesh, phi_bc, tol=1e-9, newton_max=60, xreg=1e-7):
    """axisymmetric two-field AQUAL; bodies_z = [(m, z_b)] on the axis; xe = the uniform background gradient along z.
    Returns the z-forces F_b = -Int S rho_b d_z phi (the uniform part included) and diagnostics."""
    import scipy.sparse as sps
    import scipy.sparse.linalg as spl
    t0 = time.time()
    Sq = sum(filt.density(m, mesh.qr ** 2 + (mesh.qz - zb) ** 2) for m, zb in bodies_z)
    f = np.zeros(len(mesh.R))
    for k in range(3):
        np.add.at(f, mesh.T[:, k], 4 * np.pi * np.sum(Sq * mesh.qw * mesh.bary[:, k][:, None], 0))
    wb = [np.sum(filt.density(m, mesh.qr ** 2 + (mesh.qz - zb) ** 2) * mesh.qw, 0) for m, zb in bodies_z]
    free = ~mesh.bnd
    phi = phi_bc.copy()

    def grads(ph):
        gr = mesh.Gr @ ph
        gz = mesh.Gz @ ph + xe
        return gr, gz, np.sqrt(gr * gr + gz * gz)

    def energy(ph):
        gr, gz, x = grads(ph)
        if np.max(x) >= law.xmax:
            return np.inf
        return float(np.sum(mesh.w * law.W(x)) + f @ ph)

    def gradE(ph):
        gr, gz, x = grads(ph)
        m = law.mu(x)
        return mesh.Gr.T @ (mesh.w * m * gr) + mesh.Gz.T @ (mesh.w * m * gz) + f, gr, gz, x

    fn = np.linalg.norm(f[free])
    rn = np.inf
    it = 0
    for it in range(newton_max):
        g, gr, gz, x = gradE(phi)
        rn = np.linalg.norm(g[free]) / fn
        if rn < tol:
            break
        xs = np.maximum(x, xreg)
        m = law.mu(xs)
        c = law.dmu(xs) / xs
        Arr, Azz, Arz = m + c * gr * gr, m + c * gz * gz, c * gr * gz
        H = (mesh.Gr.T @ sps.diags(mesh.w * Arr) @ mesh.Gr + mesh.Gz.T @ sps.diags(mesh.w * Azz) @ mesh.Gz
             + mesh.Gr.T @ sps.diags(mesh.w * Arz) @ mesh.Gz + mesh.Gz.T @ sps.diags(mesh.w * Arz) @ mesh.Gr).tocsr()
        d = np.zeros_like(phi)
        d[free] = spl.spsolve(H[free][:, free].tocsc(), -g[free])
        E0 = energy(phi)
        t = 1.0
        while True:
            trial = phi + t * d
            Et = energy(trial)
            if np.isfinite(Et):
                rnt = np.linalg.norm(gradE(trial)[0][free]) / fn
                if rnt < (1 - 1e-4 * t) * rn or Et < E0 + 1e-4 * t * float(g[free] @ d[free]):
                    break
            t *= 0.5
            if t < 1e-10:
                break
        phi = trial
    gr, gz, x = grads(phi)
    F = [-float(np.sum(w * gz)) for w in wb]
    return dict(F=F, newton=it, res=rn, time=time.time() - t0, nodes=len(mesh.R), xmax=float(x.max()))


def solve2d_efe_pair(law, xi, eta, s, q=1.0, hfac=6.0, Rout=250.0, grow=1.03):
    """separation parallel to the Galactic field (theta = 0): the axisymmetric free-space solve with the linear anisotropic
    Coulomb far field of the total mass as the Dirichlet datum.  Returns the radial boost B."""
    xe, muT, muL = law.stiffness(eta)
    m1, m2 = 1.0 / (1.0 + q), q / (1.0 + q)
    z1, z2 = -m2 * s, m1 * s
    h = xi / hfac
    mesh = Mesh2D(stretched_pos(h, 4 * xi, Rout, grow), stretched_sym(z1 - 4 * xi, z2 + 4 * xi, h, Rout, grow))
    RR = np.sqrt(mesh.R ** 2 / muT + mesh.Z ** 2 / muL)
    phi_bc = np.where(mesh.bnd, -1.0 / (muT * math.sqrt(muL) * np.maximum(RR, 1e-12)), 0.0)
    out = solve2d(law, HeatFilter(xi), xe, [(m1, z1), (m2, z2)], mesh, phi_bc)
    F1, F2 = out["F"]
    a_rel = F2 / m2 - F1 / m1
    out["B"] = 1.0 - s * s * a_rel
    out["momentum"] = F1 + F2 + xe               # F_b includes -m_b x_e; the sum must equal -x_e
    return out


def solve2d_deep_pair(xi, s=1.0, q=1.0, hfac=4.0, Rout=300.0, grow=1.03):
    """isolated pure deep-MOND pair (mu = x) on the axis; returns the virial ratio against Milgrom's exact two-body force"""
    m1, m2 = 1.0 / (1.0 + q), q / (1.0 + q)
    z1, z2 = -m2 * s, m1 * s
    h = xi / hfac
    mesh = Mesh2D(stretched_pos(h, 4 * xi, Rout, grow), stretched_sym(z1 - 4 * xi, z2 + 4 * xi, h, Rout, grow))
    rr = np.sqrt(mesh.R ** 2 + mesh.Z ** 2)
    phi0 = np.log(rr + xi)
    phi0[mesh.bnd] = np.log(rr[mesh.bnd])
    out = solve2d(LAW_DEEP, HeatFilter(xi), 0.0, [(m1, z1), (m2, z2)], mesh, phi0)
    F1, F2 = out["F"]
    pred = (2.0 / 3.0) * (1.0 - m1 ** 1.5 - m2 ** 1.5)
    out["virial"] = -(z1 * F1 + z2 * F2)
    out["pred"] = pred
    out["ratio"] = out["virial"] / pred
    out["momentum"] = abs(F1 + F2) / abs(F2)
    return out


# ================================================================================================ pool worker (physical units in, boosts out)
def phys_task(task):
    """one configuration in physical units -> the nonlinear boosts.  task keys: a0, gext, xi_pc, M, s_kAU, theta_deg, q,
    hfac, margin, output_filter, kind ('3d' or '2d').  Units: r_M = sqrt(G M a0^-1); eta = P2 inversion of gext/a0."""
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    a0, M = task["a0"], task["M"]
    rM = math.sqrt(GM_SUN * M / a0)
    xi = task["xi_pc"] * PC_M / rM
    s = task["s_kAU"] * KAU_M / rM
    eta = eta_of_gobs(task["gext"] / a0)
    th = math.radians(task["theta_deg"])
    t0 = time.time()
    try:
        if task.get("kind", "3d") == "2d":
            out = solve2d_efe_pair(LAW_P2, xi, eta, s, q=task.get("q", 1.0), hfac=task.get("hfac2d", 6.0))
            res = dict(B=out["B"], newton=out["newton"], res=out["res"], nodes=out["nodes"], momentum=out["momentum"])
        else:
            N, L = box_for(s, xi, hfac=task.get("hfac", 2.5), margin=task.get("margin", 9.0), nmax=task.get("nmax", 231))
            out = solve3d(LAW_P2, HeatFilter(xi), eta, pair_bodies(s, th, task.get("q", 1.0)), N, L,
                          output_filter=task.get("output_filter", True))
            res = {k: out[k] for k in ("B", "B_tan", "B_lin_free", "B_lin_per", "B_nl_per", "newton", "res", "momentum", "N", "L", "h")}
            res["cg_total"] = int(sum(out["cg"]))
            res["xrange"] = out["xrange"]
        res["ok"] = bool(res["res"] < (1e-7 if task.get("kind", "3d") == "2d" else 1e-8))
        res["error"] = ""
    except Exception as exc:                                          # recorded, never hidden
        res = dict(B=float("nan"), ok=False, error=repr(exc))
    res["time"] = time.time() - t0
    res["xi_rM"], res["s_rM"], res["eta"] = xi, s, eta
    out = dict(task)
    out.update(res)
    return out


# ================================================================================================ the pre-registration's machinery
def load_pipeline():
    """the frozen DR4 pipeline, exec'd read-only from its source into a private namespace (main() is __main__-guarded; no
    bytecode is written anywhere)."""
    path = os.path.join(PREREG, "wide_binary_pipeline.py")
    with open(path) as fh:
        src = fh.read()
    ns = {"__file__": path, "__name__": "frozen_wide_binary_pipeline"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, path, "exec"), ns)
    return ns


def registered_table(T, Ms_order=(1.0, 2.0)):
    """g03y's / L47's load_json/load_table, mirrored: the orientation average -trapz([g0, g45, g90], [1, cos45, 0]); for a
    mass row without 45 deg the weight comes from the M = 1 row."""
    Ms = sorted({float(k.split("|")[0]) for k in T})
    S = sorted({s_ for s_ in {float(k.split("|")[1]) for k in T}
                if all(f"{M}|{s_}|{th}" in T for M in Ms for th in (("0.0", "45.0", "90.0") if M == 1.0 else ("0.0", "90.0")))})
    xs = np.array([1.0, math.cos(math.radians(45)), 0.0])
    tab = np.zeros((len(Ms), len(S)))
    for i, M in enumerate(Ms):
        for j, s in enumerate(S):
            g0, g90 = T[f"{M}|{s}|0.0"]["gamma"], T[f"{M}|{s}|90.0"]["gamma"]
            if f"{M}|{s}|45.0" in T:
                g45 = T[f"{M}|{s}|45.0"]["gamma"]
            else:
                r0, r45, r90 = (T[f"1.0|{s}|{th}"]["gamma"] - 1 for th in (0.0, 45.0, 90.0))
                w = r45 / (r0 + r90) if (r0 + r90) != 0 else 0.5
                g45 = 1 + w * ((g0 - 1) + (g90 - 1))
            tab[i, j] = -np.trapz(np.array([g0, g45, g90]), xs)
    return np.array(Ms), np.array(S), tab


class RegisteredEstimator:
    """g03y's / L47's run_estimator (Amendments 11-12's theory -> gamma_v path), mirrored line by line:
         rng = default_rng(20261216); pop = make_population(1_500_000, rng); r3d from M_obs and g_true; gamma per system =
         sqrt(orientation-averaged force boost), log-interpolated in s (clipped to the table), linear in M (clipped);
         model = model_medians(pop, a0, GRID, rng); bin_medians(boot = 300); fit_gamma.
    The population and the model medians do not depend on the injected law and the rng state after model_medians is the
    same for every law, so they are built once per a0 and the state is restored for every call: bit-identical results."""

    def __init__(self, P, a0):
        self.P, self.a0 = P, a0
        rng = np.random.default_rng(20261216)
        self.pop = P["make_population"](1_500_000, rng, dr4=True)
        self.logy = np.log10(self.pop["g_proj"] / a0)
        self.r3d = np.sqrt(P["G"] * self.pop["M_obs"] * P["MSUN"] / self.pop["g_true"])
        self.mod = P["model_medians"](self.pop, a0, P["GRID"], rng)
        self.state = rng.bit_generator.state

    def gamma_sys(self, Ms, S, tab):
        P = self.P
        sk = np.clip(self.r3d / P["KAU"], S[0], S[-1])
        m = np.clip(self.pop["M_obs"], Ms[0], Ms[-1])
        gl = np.interp(np.log(sk), np.log(S), tab[0])
        gh = np.interp(np.log(sk), np.log(S), tab[-1])
        return np.sqrt(np.maximum(gl + (gh - gl) * (m - Ms[0]) / (Ms[-1] - Ms[0]), 1e-6))

    def fit(self, gam, sel=None, mod=None):
        P, pop = self.P, self.pop
        rng = np.random.default_rng()
        rng.bit_generator.state = self.state
        vX = (gam * pop["pmx"] + pop["npmx"]) * 4.74e3 * (pop["d_obs"] / 1000.)
        vY = (gam * pop["pmy"] + pop["npmy"]) * 4.74e3 * (pop["d_obs"] / 1000.)
        vt = np.hypot(vX, vY) / pop["vc_obs"]
        logy = self.logy
        if sel is not None:
            vt, logy = vt[sel], logy[sel]
        med, sig, cnt = P["bin_medians"](logy, vt, boot=300, rng=rng)
        g, sg, chi2, nb, kap = P["fit_gamma"](med, sig, self.mod if mod is None else mod, P["GRID"])
        return dict(gamma=float(g), sigma=float(sg), chi2=float(chi2), nbins=int(nb), kappa=float(kap),
                    med=med.tolist(), sig=sig.tolist(), cnt=cnt.tolist())

    def run_table(self, Ms, S, tab):
        return self.fit(self.gamma_sys(Ms, S, tab))


def frozen_gate_inject1():
    """the frozen pipeline's own gate, first injection (gamma = 1.00), replayed with its frozen seed and draw order: the
    3,000,000-pair master, both model-median grids, the 81,000-pair data draw, the 30,000-pair keep, then run_fit's
    bin_medians(boot = 200) + fit_gamma for the canonical and the alt binning.  Returns {footing: (gamma, sigma, kappa)}.
    Meant to run in a short-lived child process (the master needs ~2-3 GB)."""
    P = load_pipeline()
    rng = np.random.default_rng(20261216)
    pop_m = P["make_population"](3_000_000, rng, dr4=True)
    mod_can = P["model_medians"](pop_m, P["A0_CAN"], P["GRID"], rng)
    mod_alt = P["model_medians"](pop_m, P["A0_ALT"], P["GRID"], rng)
    del pop_m
    pop_d = P["make_population"](int(30000 * 2.7), rng, dr4=True)
    keep = rng.permutation(len(pop_d["s_obs"]))[:30000]
    pop_d = {k_: v_[keep] for k_, v_ in pop_d.items()}
    vt_d = P["vtilde_of"](pop_d, 1.00, P["A0_CAN"])
    out = {}
    for f, a0p, mod in (("canonical", P["A0_CAN"], mod_can), ("alt", P["A0_ALT"], mod_alt)):
        med, sig, cnt = P["bin_medians"](np.log10(pop_d["g_proj"] / a0p), vt_d, boot=200, rng=rng)
        g, sg, chi2, nb, kap = P["fit_gamma"](med, sig, mod, P["GRID"])
        out[f] = (float(g), float(sg), float(kap))
    return out


def run_estimator_direct(P, Ms, S, tab, a0):
    """the registered run_estimator verbatim (for the bit-identity control of the cached version)"""
    rng = np.random.default_rng(20261216)

    def fn(r3d, Mt):
        sk = np.clip(r3d / P["KAU"], S[0], S[-1])
        m = np.clip(Mt, Ms[0], Ms[-1])
        gl = np.interp(np.log(sk), np.log(S), tab[0])
        gh = np.interp(np.log(sk), np.log(S), tab[-1])
        return np.sqrt(np.maximum(gl + (gh - gl) * (m - Ms[0]) / (Ms[-1] - Ms[0]), 1e-6))
    pop = P["make_population"](1_500_000, rng, dr4=True)
    logy = np.log10(pop["g_proj"] / a0)
    r3d = np.sqrt(P["G"] * pop["M_obs"] * P["MSUN"] / pop["g_true"])
    gam = fn(r3d, pop["M_obs"])
    vX = (gam * pop["pmx"] + pop["npmx"]) * 4.74e3 * (pop["d_obs"] / 1000.)
    vY = (gam * pop["pmy"] + pop["npmy"]) * 4.74e3 * (pop["d_obs"] / 1000.)
    vt = np.hypot(vX, vY) / pop["vc_obs"]
    mod = P["model_medians"](pop, a0, P["GRID"], rng)
    med, sig, cnt = P["bin_medians"](logy, vt, boot=300, rng=rng)
    return P["fit_gamma"](med, sig, mod, P["GRID"])


def make_population_full(P, N, rng, dr4=True, dmax_pc=250., smin_kAU=2., smax_kAU=30., Gcut=17., ecc="thermal", rng_orient=None):
    """the frozen make_population, mirrored statement by statement (same draws in the same order, so for the same seed the
    returned common fields are bit-identical -- a control checks it), additionally returning the 3-D separation vector, the
    component and TRUE total masses and, from a SEPARATE generator (so the frozen draw sequence is untouched), a random
    Galactic-field direction per system (isotropic, as Amendment 10 PART D treats it)."""
    G, MSUN, KAU = P["G"], P["MSUN"], P["KAU"]
    M1 = rng.uniform(0.45, 1.25, N)
    q = rng.uniform(0.30, 1.00, N)
    M2 = np.clip(q * M1, 0.15, None)
    Mt = M1 + M2
    d = (rng.uniform(25. ** 3, dmax_pc ** 3, N)) ** (1 / 3.)
    p = -0.6
    lo, hi = (smin_kAU * 0.5) ** p, (smax_kAU * 2.0) ** p
    a_sma = (rng.uniform(hi, lo, N)) ** (1 / p) * KAU
    if ecc == 'thermal':
        e = np.sqrt(rng.uniform(0, 1, N))
    else:
        e = rng.uniform(0, 1, N)
    Ma = rng.uniform(0, 2 * np.pi, N)
    E = Ma.copy()
    for _ in range(60):
        E -= (E - e * np.sin(E) - Ma) / (1 - e * np.cos(E))
    n = np.sqrt(G * Mt * MSUN / a_sma ** 3)
    b_ = a_sma * np.sqrt(1 - e ** 2)
    xo, yo = a_sma * (np.cos(E) - e), b_ * np.sin(E)
    Ed = n / (1 - e * np.cos(E))
    vxo, vyo = -a_sma * np.sin(E) * Ed, b_ * np.cos(E) * Ed
    Om, w = rng.uniform(0, 2 * np.pi, N), rng.uniform(0, 2 * np.pi, N)
    ci = rng.uniform(-1, 1, N)
    si = np.sqrt(1 - ci ** 2)
    cO, sO, cw, sw = np.cos(Om), np.sin(Om), np.cos(w), np.sin(w)
    Pv = np.stack([cO * cw - ci * sO * sw, sO * cw + ci * cO * sw, si * sw])
    Qv = np.stack([-cO * sw - ci * sO * cw, -sO * sw + ci * cO * cw, si * cw])
    r3 = xo * Pv + yo * Qv
    v3 = vxo * Pv + vyo * Qv
    r_ = np.linalg.norm(r3[:, :2000], axis=0)
    vv = np.sum(v3[:, :2000] ** 2, axis=0)
    assert np.allclose(vv, G * Mt[:2000] * MSUN * (2 / r_ - 1 / a_sma[:2000]), rtol=1e-8)
    r3d = np.linalg.norm(r3, axis=0)
    s_proj = np.hypot(r3[0], r3[1])
    g_true = G * Mt * MSUN / r3d ** 2
    G1 = P["MG_of_mass"](M1) + 5 * np.log10(d / 10.)
    G2 = P["MG_of_mass"](M2) + 5 * np.log10(d / 10.)
    spm = np.sqrt(P["sigma_pm"](G1, dr4) ** 2 + P["sigma_pm"](G2, dr4) ** 2)
    splx = 1 / np.sqrt(P["sigma_plx"](G1, dr4) ** -2 + P["sigma_plx"](G2, dr4) ** -2)
    plx = 1000. / d
    d_obs = 1000. / (plx + splx * rng.standard_normal(N))
    dkpc = d / 1000.
    pmx, pmy = v3[0] / (4.74e3 * dkpc), v3[1] / (4.74e3 * dkpc)
    npmx, npmy = spm * rng.standard_normal(N), spm * rng.standard_normal(N)
    s_obs = s_proj * (d_obs / d)
    M_obs = Mt * (1 + 0.05 * rng.standard_normal(N))
    sel = ((s_obs > smin_kAU * KAU) & (s_obs < smax_kAU * KAU) & (d < dmax_pc)
           & (np.maximum(G1, G2) < Gcut) & (d_obs > 0) & (M_obs > 0.2))
    ro = rng_orient if rng_orient is not None else np.random.default_rng(777)
    eh = ro.standard_normal((3, N))
    eh /= np.linalg.norm(eh, axis=0)
    psi = np.arccos(np.clip(np.sum(r3 * eh, axis=0) / r3d, -1, 1))
    sp_norm = np.hypot(r3[0], r3[1])
    ep_norm = np.hypot(eh[0], eh[1])
    cosphi_proj = np.abs(r3[0] * eh[0] + r3[1] * eh[1]) / np.maximum(sp_norm * ep_norm, 1e-30)
    return dict(pmx=pmx[sel], pmy=pmy[sel], npmx=npmx[sel], npmy=npmy[sel], d_obs=d_obs[sel], s_obs=s_obs[sel],
                M_obs=M_obs[sel], g_true=g_true[sel], g_proj=G * M_obs[sel] * MSUN / s_obs[sel] ** 2,
                vc_obs=np.sqrt(G * M_obs[sel] * MSUN / s_obs[sel]),
                r3d=r3d[sel], Mt=Mt[sel], M1=M1[sel], M2=M2[sel], psi=psi[sel], cosphi_proj=cosphi_proj[sel],
                s_proj=s_proj[sel])
