#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg120_common -- shared machinery for CFG120 (DOOR 1: Mashhoon-type nonlocal gravity), written to the FROZEN criteria in
CFG120_FROZEN_CRITERIA.md (committed e8b9fbcdf).  Nothing here changes a criterion.

Units: kpc, km/s, Msun (as CFG44's Bcommon).  a0 canonical 9.3603e-11 m/s^2 and second footing 1.1312e-10 m/s^2; kappa = 1/2 is FITTED.
Repo root: ZF_REPO, else the nearest parent of this file that holds campaign_fresh_gravity/CFG44_fluid_target/Bcommon.py, else the
recorded location (disclosed on the banner).  CFG44's Bcommon is imported READ-ONLY (its Report class is NOT used: it writes into the
repo; this lane writes only next to these scripts).
"""
import os, sys, math, json, time, importlib.util
import numpy as np
from scipy import special
from scipy.integrate import quad
from scipy.optimize import minimize, differential_evolution

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_REPO = os.path.normpath(os.path.join(HERE, "..", ".."))  # fallback: this lane sits at <repo>/campaign_fresh_gravity/CFG120_door1_nonlocal_kernel


def find_repo():
    env = os.environ.get("ZF_REPO")
    if env and os.path.isfile(os.path.join(env, "campaign_fresh_gravity", "CFG44_fluid_target", "Bcommon.py")):
        return env, "ZF_REPO"
    p = HERE
    for _ in range(8):
        if os.path.isfile(os.path.join(p, "campaign_fresh_gravity", "CFG44_fluid_target", "Bcommon.py")):
            return p, "parent of __file__"
        p = os.path.dirname(p)
    return _DEFAULT_REPO, "recorded default (ZF_REPO not set, not inside the repo)"


REPO, REPO_HOW = find_repo()
_bpath = os.path.join(REPO, "campaign_fresh_gravity", "CFG44_fluid_target", "Bcommon.py")
_spec = importlib.util.spec_from_file_location("Bcommon", _bpath)
Bc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(Bc)                       # read-only import; Bcommon sets dont_write_bytecode

G = Bc.G                                           # kpc (km/s)^2 / Msun
KPC_M = Bc.KPC_M
A0_CAN_SI, A0_2ND_SI = 9.3603e-11, 1.1312e-10
FOOTINGS = {"canonical": A0_CAN_SI * KPC_M / 1e6, "second": A0_2ND_SI * KPC_M / 1e6}   # (km/s)^2/kpc
A0 = FOOTINGS["canonical"]
OMEGA_C_OVER_B = Bc.OMEGA_C_OVER_B                 # 0.1200/0.02237
C_KMS = 299792.458
MSUN = 1.98847e30
MASSES = 10 ** (9.0 + 0.25 * np.arange(13))         # 13-point log grid, 1e9 ... 1e12 (frozen)
XGRID = np.geomspace(0.1, 30.0, 200)                # frozen
TOL = 0.10
BAND = (0.90, 1.10)
MUTATE = os.environ.get("MUTATE", "").strip().lower()
if MUTATE in ("0", "none"):
    MUTATE = ""
assert MUTATE in ("", "a", "b", "c", "d"), "MUTATE must be one of a, b, c, d"


def rM(M, a0=A0):
    return math.sqrt(G * M / a0)


# ------------------------------------------------------------------------------------------------ reporting
class Report:
    def __init__(self, slug):
        self.slug = slug + ("_MUTATE_" + MUTATE if MUTATE else "")
        self.lines, self.checks, self.numbers, self.gates, self.t0 = [], [], {}, [], time.time()

    def P(self, s=""):
        print(s, flush=True)
        self.lines.append(s)

    def banner(self, s):
        self.P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)

    def head(self, doc):
        self.P(doc.strip())
        self.P(f"\n  repo root: {REPO}  ({REPO_HOW});  a0 footings (km/s)^2/kpc: canonical {FOOTINGS['canonical']:.2f}, second {FOOTINGS['second']:.2f}")
        self.P(f"  MUTATE mode: {MUTATE or 'none (main run)'}")

    def check(self, name, detail, ok, load_bearing=True):
        """a CHECK asserts a pre-declared expectation (usually 'the obstruction holds'); FAIL = expectation false (kept, exit 1)."""
        self.checks.append(dict(name=name, detail=detail, ok=bool(ok), load_bearing=load_bearing))
        self.P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         {detail}")

    def gate(self, gate, verdict, detail):
        """a GATE row is the door's verdict on a frozen gate (PASS / FAIL / UNDECIDED); it does not set the exit code."""
        self.gates.append(dict(gate=gate, verdict=verdict, detail=detail))
        self.P(f"  << GATE {gate}: {verdict} >> {detail}")

    def num(self, k, v):
        self.numbers[k] = v

    def write(self):
        lb = [c for c in self.checks if c["load_bearing"]]
        nf = sum(not c["ok"] for c in lb)
        self.P(f"\n  {sum(c['ok'] for c in self.checks)}/{len(self.checks)} checks pass; load-bearing failures: {nf}   ({time.time() - self.t0:.0f} s)")

        def clean(o):
            if isinstance(o, dict):
                return {str(k): clean(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [clean(v) for v in o]
            if isinstance(o, np.ndarray):
                return [clean(v) for v in o.tolist()]
            if isinstance(o, (np.floating, float)):
                return float(o) if np.isfinite(o) else str(o)
            if isinstance(o, np.integer):
                return int(o)
            if isinstance(o, (np.bool_, bool)):
                return bool(o)
            return o if isinstance(o, (int, str)) or o is None else str(o)

        json.dump(clean(dict(slug=self.slug, mutate=MUTATE, load_bearing_failures=nf, checks=self.checks, gates=self.gates,
                             numbers=self.numbers)), open(os.path.join(HERE, self.slug + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")
        return nf


# ------------------------------------------------------------------------------------------------ kernels (K in kpc^-3)
class KM:
    """the REQUIRED point-mass kernel  K_M(s) = 1/(4 pi rM s sqrt(s^2+rM^2))   (rM in kpc)"""
    name = "K_M"

    def __init__(self, rM_):
        self.rM = rM_

    def K(self, s):
        s = np.asarray(s, float)
        return 1.0 / (4 * math.pi * self.rM * s * np.sqrt(s * s + self.rM ** 2))

    def m(self, r):                                   # 4 pi Int_0^r K s^2 ds = sqrt(1+x^2) - 1
        r = np.asarray(r, float)
        return np.sqrt(1.0 + (r / self.rM) ** 2) - 1.0

    def Q(self, s):                                   # Int s' K ds' = asinh(s/rM)/(4 pi rM)
        return np.arcsinh(np.asarray(s, float) / self.rM) / (4 * math.pi * self.rM)

    def Khat(self, k):
        z = np.asarray(k, float) * self.rM
        return F_struve(z)


def F_fourier_quad(zi):
    """F(z) = (1/z) Int_0^inf sin(z u)/sqrt(1+u^2) du  (the defining Fourier integral, QAWF oscillatory quadrature)."""
    return quad(lambda u: 1.0 / math.sqrt(1.0 + u * u), 0.0, np.inf, weight="sin", wvar=zi, limlst=200)[0] / zi


def F_struve(z):
    """F(z) = (pi/2z) [I0(z) - L0(z)]  (FT of K_M with rM = 1).  Direct Struve/Bessel for z < 5 (cancellation-free there);
       for z >= 5 the defining sine integral by oscillatory quadrature (I0 - L0 loses all digits at large z)."""
    z = np.atleast_1d(np.asarray(z, float))
    out = np.empty_like(z)
    for i, zi in enumerate(z):
        out[i] = (math.pi / (2 * zi)) * (special.iv(0, zi) - special.modstruve(0, zi)) if zi < 5.0 else F_fourier_quad(zi)
    return out if out.size > 1 else out[0]


class RM:
    """Rahvar-Mashhoon-type kernel (AS RECALLED):  K = A (1 + mu s) exp(-mu s) / (4 pi lam s^2),  lam in kpc, mu in 1/kpc."""
    name = "RM"

    def __init__(self, A, lam, mu):
        self.A, self.lam, self.mu = float(A), float(lam), float(mu)

    def K(self, s):
        s = np.asarray(s, float)
        return self.A * (1 + self.mu * s) * np.exp(-self.mu * s) / (4 * math.pi * self.lam * s * s)

    def m(self, r):
        r = np.asarray(r, float)
        if self.mu == 0.0:
            return self.A * r / self.lam
        mu = self.mu
        return (self.A / self.lam) * (2.0 / mu - (2.0 / mu + r) * np.exp(-mu * r))

    def Q(self, s):                                   # Int s' K ds' up to an additive constant (only differences are used)
        s = np.asarray(s, float)
        if self.mu == 0.0:
            return self.A * np.log(s) / (4 * math.pi * self.lam)
        return self.A / (4 * math.pi * self.lam) * (special.expi(-self.mu * s) - np.exp(-self.mu * s))

    def total(self):
        return 2.0 * self.A / (self.lam * self.mu) if self.mu > 0 else float("inf")

    def Khat(self, k):
        k = np.asarray(k, float)
        if self.mu == 0.0:
            return self.A * (math.pi / 2) / (self.lam * k)
        return (self.A / (self.lam * k)) * (np.arctan(k / self.mu) + self.mu * k / (self.mu ** 2 + k ** 2))


class Tab:
    """tabulated spherical kernel from its dimensionless B(r) = r K (1+m) (point-mass R = 4 pi rM^2 B)."""
    name = "K*"

    def __init__(self, r, K):
        self.r = np.asarray(r, float)
        self.Kv = np.asarray(K, float)
        s2K = self.r * self.Kv
        lr = np.log(self.r)
        # Q(s) = Int s' K ds' (cumulative trapezoid in ln s), and m(r) = 4 pi Int s^2 K ds
        self.Qv = np.concatenate([[0.0], np.cumsum(0.5 * (s2K[1:] * self.r[1:] + s2K[:-1] * self.r[:-1]) * np.diff(lr))])
        s3K = self.r ** 2 * self.Kv * self.r
        self.mv = 4 * math.pi * np.concatenate([[0.0], np.cumsum(0.5 * (s3K[1:] + s3K[:-1]) * np.diff(lr))])
        self.lr = lr

    def K(self, s):
        return np.interp(np.log(np.maximum(s, self.r[0])), self.lr, self.Kv)

    def m(self, r):
        return np.interp(np.log(np.maximum(r, self.r[0])), self.lr, self.mv)

    def Q(self, s):
        return np.interp(np.log(np.maximum(s, self.r[0])), self.lr, self.Qv)


# ------------------------------------------------------------------------------------------------ point-mass G1 machinery
def x_range_mask(r, M, a0):
    x = r / rM(M, a0)
    return (x >= 0.1 - 1e-12) & (x <= 30.0 + 1e-12)


def R_point(kern, r, M, a0):
    """C_model/C_target for a point mass under an LTI kernel:  4 pi (G M/a0) r K(r) (1 + m(r))."""
    r = np.asarray(r, float)
    return 4 * math.pi * (G * M / a0) * r * kern.K(r) * (1.0 + kern.m(r))


def minimax_universal(rgrid, masses, a0, target_scale=None):
    """pointwise minimax over a universal B(r): R_i(r) = c_i(r) B(r) with c_i = 4 pi rM_i^2 / target_scale_i (R' = R / target_scale);
       returns (residual factor per r [nan where no mass constrains r], ln B*, mass-count per r, M_lo, M_hi)."""
    n = len(rgrid)
    fac, lnB, cnt = np.full(n, np.nan), np.full(n, np.nan), np.zeros(n, int)
    mlo, mhi = np.full(n, np.nan), np.full(n, np.nan)
    for j, r in enumerate(rgrid):
        cs, ms = [], []
        for M in masses:
            if x_range_mask(np.array([r]), M, a0)[0]:
                sc = 1.0 if target_scale is None else target_scale(M)
                cs.append(4 * math.pi * rM(M, a0) ** 2 / sc)
                ms.append(M)
        cnt[j] = len(cs)
        if cs:
            cs = np.array(cs)
            fac[j] = math.sqrt(cs.max() / cs.min())
            lnB[j] = -0.5 * (math.log(cs.max()) + math.log(cs.min()))
            mlo[j], mhi[j] = min(ms), max(ms)
    return fac, lnB, cnt, mlo, mhi


def build_Kstar(a0, masses=MASSES, target_scale=None, n=6000):
    """the best universal positive kernel (centred minimax B*(r)), B flat inward of the first constrained r and outward of the last.
       (1+m)^2 = 1 + 8 pi Int_0^r r' B dr'  =>  K = B / (r (1+m))."""
    r = np.geomspace(1e-5, 1e4, n)
    fac, lnB, cnt, _, _ = minimax_universal(r, masses, a0, target_scale)
    ok = np.isfinite(lnB)
    B = np.exp(np.interp(np.log(r), np.log(r[ok]), lnB[ok]))         # flat extension at both ends (np.interp clamps)
    lr = np.log(r)
    # Int_0^r r' B dr' = B[0] r0^2/2 + cumulative trapezoid of r'^2 B dln r
    integ = B[0] * r[0] ** 2 / 2 + np.concatenate([[0.0], np.cumsum(0.5 * (r[1:] ** 2 * B[1:] + r[:-1] ** 2 * B[:-1]) * np.diff(lr))])
    one_m = np.sqrt(1.0 + 8 * math.pi * integ)
    K = B / (r * one_m)
    return Tab(r, K), B, r


# ------------------------------------------------------------------------------------------------ RM best-case fit (T1g)
def rm_residual(params, masses, a0, fixedA=None, target_scale=None, nx=200):
    """max |ln R| over the whole frozen G1 domain for RM(A, lam, mu); params are logs."""
    if fixedA is None:
        A, lam, mu = np.exp(params)
    else:
        A = fixedA
        lam, mu = np.exp(params)
    kern = RM(A, lam, mu)
    worst = 0.0
    for M in masses:
        r = rM(M, a0) * np.geomspace(0.1, 30.0, nx)
        Rv = R_point(kern, r, M, a0)
        if target_scale is not None:
            Rv = Rv / target_scale(M)
        if not np.all(np.isfinite(Rv)) or np.any(Rv <= 0):
            return 1e3
        worst = max(worst, float(np.max(np.abs(np.log(Rv)))))
    return worst


def fit_rm(a0, masses=MASSES, fixedA=None, target_scale=None, seed=1):
    """best case over the RM family (a characterisation, not a scan for a pass: the pass line is unchanged).
       global differential evolution then Nelder-Mead polish; deterministic (seeded)."""
    if fixedA is None:
        bounds = [(math.log(1e-4), math.log(1e4)), (math.log(0.05), math.log(1e3)), (math.log(1e-5), math.log(10.0))]
    else:
        bounds = [(math.log(0.05), math.log(1e3)), (math.log(1e-5), math.log(10.0))]
    f = lambda p: rm_residual(p, masses, a0, fixedA, target_scale, nx=60)
    de = differential_evolution(f, bounds, seed=seed, maxiter=300, popsize=25, tol=1e-10, polish=False)
    res = minimize(lambda p: rm_residual(p, masses, a0, fixedA, target_scale, nx=200), de.x, method="Nelder-Mead",
                   options=dict(xatol=1e-10, fatol=1e-12, maxiter=4000))
    p = res.x
    if fixedA is None:
        A, lam, mu = np.exp(p)
    else:
        A = fixedA
        lam, mu = np.exp(p)
    return dict(A=float(A), lam=float(lam), mu=float(mu), max_abs_lnR=float(res.fun))


# ------------------------------------------------------------------------------------------------ extended baryons: spherical convolution
def exp_rho(M, h):
    return lambda r: M / (8 * math.pi * h ** 3) * np.exp(-np.asarray(r, float) / h)


def sphere_grid(r0, n_in=120, n_dom=200, xmax=30.0, rMv=None):
    """radial grid: log grid from 1e-3 min(h,rM) to 0.1 rM, then the frozen 200-point domain [0.1, 30] rM."""
    lo = 1e-3 * min(r0, rMv)
    a = np.geomspace(lo, 0.1 * rMv, n_in, endpoint=False)
    b = rMv * np.geomspace(0.1, xmax, n_dom)
    return np.concatenate([a, b])


def rhoD_sphere(kern, rho_b_fn, rgrid, rmax_b):
    """rho_D(r) = (2 pi / r) Int r' rho_b(r') [Q(r+r') - Q(|r-r'|)] dr'   (exact for spherical rho_b and radial K)."""
    out = np.empty(len(rgrid))
    for j, r in enumerate(rgrid):
        f = lambda rp: rp * rho_b_fn(rp) * (kern.Q(r + rp) - kern.Q(abs(r - rp)))
        v1 = quad(f, 0.0, r, epsabs=0.0, epsrel=1e-10, limit=200)[0]
        v2 = quad(f, r, r + rmax_b, epsabs=0.0, epsrel=1e-10, limit=200)[0]
        out[j] = 2 * math.pi / r * (v1 + v2)
    return out


def cum_mass(rgrid, rho):
    """4 pi Int rho r^2 dr from 0: trapezoid in ln r plus a constant-density core below rgrid[0]."""
    lr = np.log(rgrid)
    integ = rgrid ** 3 * rho
    cum = 4 * math.pi * np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(lr))])
    return cum + 4 * math.pi / 3 * rho[0] * rgrid[0] ** 3


def Mb_exp(M, h, r):
    s = np.asarray(r, float) / h
    return M * (1.0 - (1.0 + s + 0.5 * s * s) * np.exp(-s))


def C_ratio_sphere(kern, M, h, a0, rgrid=None, extra=None):
    """R(r) = C_model/C_target for an exponential sphere (mass M, scale h) with kernel kern.
       C_target = (a0/4pi) M_b(<r) exactly; C_model = rho_D r^3 g_tot with its own g_tot = G(M_b + M_D)/r^2.
       extra: optional (callable rho_b_extra, rmax_extra_fn) is not used; shells handled by the caller through add-on arrays."""
    rMv = rM(M, a0)
    if rgrid is None:
        rgrid = sphere_grid(h, rMv=rMv)
    rho_b = exp_rho(M, h)
    rhoD = rhoD_sphere(kern, rho_b, rgrid, 60.0 * h)
    MD = cum_mass(rgrid, rhoD)
    Mb = Mb_exp(M, h, rgrid)
    Cmod = 4 * math.pi * G * rgrid * rhoD * (Mb + MD)               # 4 pi * rho_D r^3 g_tot  (units of 4pi to compare with a0 Mb)
    R = Cmod / (a0 * Mb)
    return rgrid, R, rhoD, MD, Mb


# ------------------------------------------------------------------------------------------------ CFG44 reference target for extended baryons (own ODE)
def target_MD_ode(Mfun, a0, r0, r1, n=4001):
    """dM_D/dr = (a0/G) r M_b(<r) / (M_b(<r) + M_D(<r)), started on the slow manifold (as CFG44's cold_mass); returns r, M_D."""
    from scipy.integrate import solve_ivp
    rg = np.geomspace(r0, r1, n)

    def rhs(s, y):
        r = math.exp(s)
        Mb = float(Mfun(r))
        return [r * (a0 / G) * r * Mb / max(Mb + y[0], 1e-300)]

    Mb0 = float(Mfun(r0))
    u0 = G * Mb0
    MD0 = u0 * (math.sqrt(1.0 + a0 * r0 * r0 / u0) - 1.0) / G       # CFG44's slow-manifold start
    sol = solve_ivp(rhs, (math.log(r0), math.log(r1)), [MD0], t_eval=np.log(rg), rtol=1e-11, atol=1e-8, method="Radau")
    return rg, sol.y[0]


def fmt(x, p=4):
    return f"{x:.{p}g}"
