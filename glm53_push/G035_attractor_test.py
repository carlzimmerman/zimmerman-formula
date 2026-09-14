#!/usr/bin/env python3
"""
G035 -- THE ATTRACTOR TEST: is the Zimmerman temperature sigma^2 = G M_b/(2 r_M)
a real ATTRACTOR of dust relaxation under the certified physics, or postulated?

Pre-registration: glm53_push/G035_preregistration.md (committed BEFORE the suite ran;
the engine's static validations V1-V4 and the constants block are the only code
executed between that commit and the suite launch).

THE KEY PHYSICS DECISION (registered): the dust feels ONLY Newtonian baryon
attraction + its own Newtonian self-gravity.  The phantom is the EQUILIBRIUM
description, not an extra force.  Real physical units throughout (length unit =
r_M, time unit = t_cross(r_M) = r_M/sigma_target, mass unit = M_b  =>  G_code = 2
exactly); the a0 footing enters the DIMENSIONLESS dynamics through the real
SPARC baryon profile sampled at r/r_M -- the two footings are genuinely
different dynamical problems.

Galaxy: NGC3198.  Baryon field from the REAL SPARC curve in the G033 bundle
(website/src/data/fluid_real_data.json, sparc[52]: 43 points, D = 13.8 Mpc,
M_b = 6.2501e10 M_sun = max enclosed baryons, the G033 pipeline value).
M_enc(r) = v_b(r)^2 r / G, exact closed form, NO softening on the baryons
(M_enc ~ r^3 at small r, so g_b is smooth at the origin).

Engine: direct-summation O(N^2) KDK leapfrog, numpy-vectorised per step,
multiprocessing over cells (16 workers).  Plummer softening eps = 0.08 r_M on
the dust-dust force ONLY (canonical 772 pc, alt 703 pc -- smaller than r_M/10).
External baryon field: exact spherical g_b(r) from the real curve, direction-
averaged (the suite's registered spherical reading).
"""
import os
os.environ.setdefault("NUMBA_THREADING_LAYER", "workqueue")  # before numba import
import sys, json, math, time
import numpy as np
from multiprocessing import Pool

# numba fast path (K001's engine pattern); numpy fallback kept for validation
try:
    import numba
    numba.config.THREADING_LAYER = "workqueue"   # always available, no external deps
    from numba import njit, prange
    HAVE_NUMBA = True

    @njit(parallel=True, fastmath=True)
    def _accel_self_nb(pos, acc, mp, eps2, gcode):
        n = pos.shape[0]
        for i in prange(n):
            xi = pos[i, 0]; yi = pos[i, 1]; zi = pos[i, 2]
            ax = 0.0; ay = 0.0; az = 0.0
            for j in range(n):
                if j == i:
                    continue
                dx = xi - pos[j, 0]; dy = yi - pos[j, 1]; dz = zi - pos[j, 2]
                r2 = dx * dx + dy * dy + dz * dz + eps2
                inv = gcode * mp / (r2 * np.sqrt(r2))
                ax -= inv * dx; ay -= inv * dy; az -= inv * dz
            acc[i, 0] = ax; acc[i, 1] = ay; acc[i, 2] = az
except ImportError:
    HAVE_NUMBA = False

    def _accel_self_nb(pos, acc, mp, eps2, gcode):
        dx = pos[:, None, 0] - pos[None, :, 0]
        dy = pos[:, None, 1] - pos[None, :, 1]
        dz = pos[:, None, 2] - pos[None, :, 2]
        r2 = dx * dx + dy * dy + dz * dz + eps2
        inv_r3 = r2 ** -1.5
        np.fill_diagonal(inv_r3, 0.0)
        acc[:, 0] = -gcode * mp * (dx * inv_r3).sum(1)
        acc[:, 1] = -gcode * mp * (dy * inv_r3).sum(1)
        acc[:, 2] = -gcode * mp * (dz * inv_r3).sum(1)

HERE   = os.path.dirname(os.path.abspath(__file__))
BUNDLE = "/Users/carlzimmerman/new_physics/zimmerman-formula 2/website/src/data/fluid_real_data.json"
OUT    = os.path.join(HERE, "G035_results.json")
OUTX   = os.path.join(HERE, "G035_transfer_function.json")

# ------------------------------------------------------------------ constants
G_SI   = 6.674e-11                 # m^3/kg/s^2
MSUN   = 1.98892e30                # kg
KPC_M  = 3.0857e19                 # m
KMS    = 1.0e3                     # m/s
MYR    = 3.15576e13                # s
A0_CAN = 9.3619e-11                # m/s^2   (canonical footing)
A0_ALT = 1.1279e-10                # m/s^2   (alt footing)
# code units: length = r_M, mass = M_b, velocity = sigma_target  =>
# time unit = t_cross(r_M) = r_M/sigma_target and Newton's identity
# G M_b = 2 sigma_t^2 r_M forces G_code = 2 EXACTLY (asserted at startup).
GCODE  = 2.0

GAL   = "NGC3198"
MB_MSUN = 6.2501e10                # M_sun, from the bundle (G033 pipeline)

# suite (frozen by the pre-registration)
N_PART   = 2000
EPS_RM   = 0.08                    # dust softening in r_M
SIG_GRID = (0.3, 0.5, 0.7, 1.0, 1.5)
R0_GRID  = (0.5, 1.0, 2.0)
MU_GRID  = (0.1, 0.3, 1.0)
MU_PRIMARY = 0.3
STEPS    = 12000
NSTEP_HALF = 24000                 # dt-convergence run
NSTRIDE  = 300                     # light-curve cadence
DTFAC    = 1.0 / STEPS
XMAX     = 60.0                    # potential-reference radius in r_M (registered)
ETA      = 0.05                    # adaptive step: dt = eta sqrt(eps/|a|max)  (K001's eta)
DT_MAX   = 0.02                    # hard step cap in t_cross(r_M) units

def zimmerman(Mb_msun, a0):
    """r_M, sigma_target, t_cross(r_M) in SI (m, m/s, s) for baryon mass Mb_msun."""
    Mb  = Mb_msun * MSUN
    rM  = math.sqrt(G_SI * Mb / a0)
    st  = math.sqrt(G_SI * Mb / (2.0 * rM))
    return rM, st, rM / st

# ------------------------------------------------- real SPARC baryon profile
def load_baryon_profile(a0):
    """Spherical enclosed-baryon mass profile of NGC3198 from the REAL curve,
    on the r/r_M grid of the dynamics.  Returns (xs, ys, sxl, sxr, rM, sig_t, gal):
    piecewise power-law interpolation in log-log (exact inside the curve);
    REGISTERED extrapolation: solid-body below the first point (M ~ x^3),
    flat-v_b beyond the last point (M ~ x).  M/Mb normalised by the curve's
    MAX enclosed baryon (the G033 pipeline M_b definition; the last curve point
    sits 0.2% below the max -- measurement noise, registered)."""
    d = json.load(open(BUNDLE))
    gal = next(g for g in d["sparc"] if g["name"] == GAL)
    pts = gal["curve"]                       # r kpc, v km/s (baryonic speeds)
    rM, sig_t, _ = zimmerman(MB_MSUN, a0)
    rr = np.array([p["r"] for p in pts]) * KPC_M / rM       # r in r_M
    vb = np.array([p["vb"] for p in pts]) * KMS             # m/s
    # enclosed baryon mass in units of M_b:  M(r)/M_b = (v_b r)^2 / (G M_b)
    # with r_M^2 = G M_b / a0 and sigma_t^2 = G M_b/(2 rM):
    #   M(r)/M_b = (vb/ (sqrt(2) sig_t))^2 * (r / rM)   [dimensional identity]
    mm = (vb / (math.sqrt(2.0) * sig_t)) ** 2 * rr
    mm = mm / mm.max()                        # Mb = MAX enclosed (bundle value)
    xs = np.log(rr); ys = np.log(mm)
    assert rr[0] > 0 and mm[0] > 0 and np.all(np.diff(rr) > 0)
    sxl = 3.0                                 # registered solid-body head
    sxr = 1.0                                 # registered flat-v_b tail
    return xs, ys, sxl, sxr, rM, sig_t, gal

def menc_over_mb(x, xs, ys, sxl, sxr):
    """log M_enc(r)/M_b at r = exp(x) r_M: piecewise power-law inside the curve,
    solid body (slope 3) below, flat-v_b (slope 1) above (registered)."""
    x = np.asarray(x, dtype=float)
    y = np.interp(x, xs, ys)
    y = np.where(x < xs[0], ys[0] + 3.0 * (x - xs[0]), y)
    y = np.where(x > xs[-1], ys[-1] + 1.0 * (x - xs[-1]), y)
    return y

def gb_code(x, xs, ys, sxl, sxr):
    """Baryon acceleration g_b in code units (sigma_t^2 / r_M) at r = x r_M.
    g_b = G M_enc / r^2;  in code units: g_b/ (sig_t^2/rM) = 2 * (M/Mb) / x^2."""
    x = np.asarray(x, dtype=float)
    return 2.0 * np.exp(menc_over_mb(np.log(x), xs, ys, sxl, sxr)) / x**2

# ------------------------------------------------------------------ ICs
def ic_uniform(N, R0, sig_start, mu, seed):
    """Cold-start IC: uniform sphere radius R0 (r_M), isotropic Gaussian
    velocities with per-component dispersion sig_start (sigma_target units),
    zero net momentum.  Returns pos (N,3), vel (N,3) in code units."""
    rng = np.random.default_rng(seed)
    u = rng.uniform(0.0, 1.0, N)             # radius CDF (must be in [0,1])
    c = rng.uniform(-1.0, 1.0, N)            # cos theta
    phi = rng.uniform(0.0, 2.0 * np.pi, N)
    rr = R0 * u ** (1.0 / 3.0)
    pos = np.empty((N, 3))
    st = np.sqrt(np.maximum(1.0 - c * c, 0.0))
    pos[:, 0] = rr * st * np.cos(phi)
    pos[:, 1] = rr * st * np.sin(phi)
    pos[:, 2] = rr * c
    vel = rng.normal(0.0, sig_start, (N, 3))
    vel -= vel.mean(0)                       # zero net momentum
    return pos, vel

def ic_isothermal(N, R0, mu, seed):
    """C2 control IC: rho ~ r^-2 dust on [0.25, 2.5] r_M (r uniform in volume),
    velocities Gaussian at exactly sigma_target (1.0 in code units)."""
    rng = np.random.default_rng(seed)
    rmin, rmax = 0.25, 2.5
    rr = (rmin**3 + (rmax**3 - rmin**3) * rng.uniform(0, 1, N)) ** (1.0 / 3.0)
    u = rng.uniform(0.0, 1.0, N)             # radius CDF already drawn above
    c = rng.uniform(-1.0, 1.0, N)            # cos theta
    phi = rng.uniform(0.0, 2.0 * np.pi, N)
    pos = np.empty((N, 3))
    st = np.sqrt(np.maximum(1.0 - c * c, 0.0))
    pos[:, 0] = rr * st * np.cos(phi)
    pos[:, 1] = rr * st * np.sin(phi)
    pos[:, 2] = rr * c
    vel = rng.normal(0.0, 1.0, (N, 3))
    vel -= vel.mean(0)
    return pos, vel

# ------------------------------------------------------------------ kernel
def accelerations(pos, mp, eps2, gb_args):
    """Total ATTRACTION: self-gravity (Plummer-softened O(N^2): numba-parallel
    if available, numpy fallback otherwise) + external baryon field g_b(r)
    from the real SPARC curve (no softening).
    a_i = -G mp sum_j (x_i - x_j)/(|x_i-x_j|^2+eps^2)^{3/2} - g_b(r_i) r_hat_i."""
    acc = np.empty_like(pos)
    _accel_self_nb(pos, acc, mp, eps2, GCODE)
    r = np.sqrt(pos[:, 0] ** 2 + pos[:, 1] ** 2 + pos[:, 2] ** 2)
    gb = gb_code(np.maximum(r, 1e-6), *gb_args)
    acc[:, 0] -= gb * pos[:, 0] / r
    acc[:, 1] -= gb * pos[:, 1] / r
    acc[:, 2] -= gb * pos[:, 2] / r
    return acc

def accelerations_selfonly(pos, mp, eps2):
    dx = pos[:, None, 0] - pos[None, :, 0]
    dy = pos[:, None, 1] - pos[None, :, 1]
    dz = pos[:, None, 2] - pos[None, :, 2]
    r2 = dx * dx + dy * dy + dz * dz + eps2
    inv_r3 = r2 ** -1.5
    np.fill_diagonal(inv_r3, 0.0)
    return -GCODE * mp * np.stack([(dx * inv_r3).sum(1), (dy * inv_r3).sum(1),
                                   (dz * inv_r3).sum(1)], 1)

def energy(pos, vel, mp, eps, gb_args):
    """Total energy in code units: self PE (softened pair sum, G_code = 2)
    + baryon PE from the exact closed-form potential of the piecewise power-law
    M_enc(r), + KE.  Diagnostic only (verdict-gating quantities are kinematic).
    Potential reference registered: phi(XMAX) = 0 with XMAX = 60 r_M
    (the flat-vb tail diverges logarithmically; only differences matter)."""
    eps2 = eps * eps
    dx = pos[:, None, 0] - pos[None, :, 0]
    dy = pos[:, None, 1] - pos[None, :, 1]
    dz = pos[:, None, 2] - pos[None, :, 2]
    r2 = dx * dx + dy * dy + dz * dz + eps2
    inv = 1.0 / np.sqrt(r2)
    np.fill_diagonal(inv, 0.0)
    pe_self = -0.5 * GCODE * mp * mp * inv.sum()
    r = np.sqrt((pos * pos).sum(1))
    # exact closed-form log tail for ALL radii (no clamp): the flat-v_b tail
    # potential keeps growing as ln(r); clamping it at XMAX mis-bookkept the
    # potential energy of escapers (the run-1 INSTRUMENT-FAIL -- dE ~ -0.4 in
    # the C2 control traced exactly to this).  Reference phi(XMAX=60) = 0 kept.
    phi = phi_baryon(np.clip(r, 1e-3, 1e9), gb_args)
    pe_b = mp * phi.sum()
    ke = 0.5 * mp * (vel * vel).sum()
    return ke + pe_self + pe_b

def phi_baryon(x, gb_args):
    """Baryon potential phi_b(r)/sigma_t^2 = -int_x^XMAX g_b ds < 0
    (exactly -[g_b integral] so that -grad phi = +g_b r_hat, the inward field;
    exact closed form per piecewise power-law segment).  Segment i:
    M ~ (x/xi)^p locally  =>  g = 2 e^{y_i} xi^-p x^(p-2)  =>
        int_x^xi g ds = 2 e^{y_i}/((p-1) xi) (1 - (x/xi)^(p-1))   (p != 1)
                      = 2 e^{y_i}/xi ln(xi/x)                    (p = 1).
    Flat-vb tail (x > x_1): g = 2 e^{y_last}/(x1 x)  =>  |phi| = 2 e^{yl}/x1 ln(XMAX/x).
    Solid-body interior (x < x_0): g = 2 e^{y_0} x / x0^3  =>  int = g0 (x0^2-x^2)/2."""
    xs, ys, sxl, sxr = gb_args
    x = np.atleast_1d(np.asarray(x, dtype=float))
    yl = ys[-1]; x1 = math.exp(xs[-1])
    # start: |phi| at the curve's outer edge (tail integral from x1 to XMAX)
    acc = np.full_like(x, (2.0 * math.exp(yl) / x1) * math.log(XMAX / x1))
    # interior segments, outside-in
    for i in range(len(xs) - 1, 0, -1):
        p  = (ys[i] - ys[i-1]) / (xs[i] - xs[i-1])
        xi = math.exp(xs[i]); yi = ys[i]
        xc = np.clip(x, math.exp(xs[i-1]), None)      # below the segment use its full integral
        if abs(p - 1.0) > 1e-9:
            int_x_xi = 2.0 * math.exp(yi) / ((p - 1.0) * xi) * (1.0 - (xc / xi) ** (p - 1))
        else:
            int_x_xi = 2.0 * math.exp(yi) / xi * np.log(xi / xc)
        acc = acc + np.where(x < xi, int_x_xi, 0.0)
    # below the first curve point: solid body (M ~ x^3)
    x0 = math.exp(xs[0]); y0 = ys[0]
    g0 = 2.0 * math.exp(y0) / x0**3
    acc = acc + np.where(x < x0, 0.5 * g0 * (x0**2 - np.clip(x, 1e-9, None)**2), 0.0)
    # beyond the curve: the pure log tail
    out = np.where(x > x1, (2.0 * math.exp(yl) / x1) * np.log(XMAX / np.clip(x, 1e-9, None)), acc)
    return -out          # phi < 0 everywhere: -dphi/dr = +g_b (inward)

# ------------------------------------------------------------------ runner
def run_cell(args):
    (mu, sig_start, R0, footing, t_end, seed, tag, eta) = args
    t0 = time.time()
    a0 = A0_CAN if footing == "canonical" else A0_ALT
    xs, ys, sxl, sxr, rM, sig_t, gal = load_baryon_profile(a0)
    gb_args = (xs, ys, sxl, sxr)
    eps  = EPS_RM
    eps2 = eps * eps
    mp   = mu / N_PART
    if tag.startswith("C2"):
        pos, vel = ic_isothermal(N_PART, R0, mu, seed)
    else:
        pos, vel = ic_uniform(N_PART, R0, sig_start, mu, seed)
    # adaptive KDK leapfrog: dt = eta * sqrt(eps / |a|_max), capped at DT_MAX,
    # integrated to t_end (in t_cross(r_M) units).  Resolves the dense settled
    # phase (dt ~ 0.008 t_cross) and takes large steps in the cold dilute
    # pre-collapse phase -- uniform accuracy at uniform wall cost.
    acc = accelerations(pos, mp, eps2, gb_args)
    light_times = [t_end * k / 60.0 for k in range(1, 61)]
    hist, nsteps_used = [], 0
    E0 = energy(pos, vel, mp, eps, gb_args)
    t = 0.0
    li = 0
    # K001's validated shared adaptive step: a fraction eta of the local
    # free-fall time in the softened field, min over particles, capped.
    # (The |a|max criterion sawtooths with the deepest pair and under-resolves
    # the collapsing core; the free-fall form is smooth and was validated to
    # dE/E ~ 1e-5 in K001's production collapse.)
    def choose_dt(p, v=None):
        r2p = (p * p).sum(1) + eps2
        menb = np.exp(menc_over_mb(np.log(np.maximum(np.sqrt((p * p).sum(1)), 1e-6)), *gb_args))
        tau = np.sqrt(r2p ** 1.5 / (menb + mu))
        if v is not None:
            v2 = (v * v).sum(1)
            enc = eps / np.maximum(np.sqrt(v2), 1e-12)     # encounter time at eps
            return min(DT_MAX, ETA * np.minimum(tau, enc).min())
        return min(DT_MAX, ETA * tau.min())
    dt = choose_dt(pos, vel)
    while t < t_end - 1e-12:
        dt = min(dt, t_end - t)
        vel += 0.5 * dt * acc
        pos += dt * vel
        acc = accelerations(pos, mp, eps2, gb_args)
        vel += 0.5 * dt * acc
        t += dt
        nsteps_used += 1
        dt = choose_dt(pos, vel)
        while li < len(light_times) and t >= light_times[li] - 1e-12:
            r = np.sqrt((pos * pos).sum(1))
            vc = vel.mean(0)
            vsub = vel - vc
            s2 = float((vsub ** 2).sum() / (3.0 * N_PART))   # 1D variance
            hist.append(dict(t=light_times[li], r50=float(np.median(r)),
                             r90=float(np.quantile(r, 0.9)), sig2_1d=s2,
                             f_esc=float((r > 10.0).mean())))
            li += 1
    E1 = energy(pos, vel, mp, eps, gb_args)
    r = np.sqrt((pos * pos).sum(1))
    vc = vel.mean(0)
    vsub = vel - vc
    sig2_1d = float((vsub ** 2).sum() / (3.0 * N_PART))
    sigprof = dispersion_profile(pos, vsub)
    md_rm = float((r < 1.0).mean() * mu)          # dust mass inside r_M / M_b (S2)
    edges = np.logspace(-1.3, 1.3, 40)
    rc = np.sqrt(edges[1:] * edges[:-1])
    cnt, _ = np.histogram(r, edges)
    vol = 4.0 / 3.0 * np.pi * (edges[1:] ** 3 - edges[:-1] ** 3)
    rho = mp * cnt / vol
    ok = (cnt > 15) & (rc > 0.3) & (rc < 3.0)
    slope = float(np.polyfit(np.log(rc[ok]), np.log(rho[ok]), 1)[0]) if ok.sum() > 4 else float("nan")
    # relaxed flag: light curve at 85% vs 100% of t_end
    h0, h1 = hist[-1], hist[int(len(hist) * 0.85)]
    relaxed = (abs(h1["r50"] - h0["r50"]) / max(h0["r50"], 1e-9) < 0.15 and
               abs(h1["sig2_1d"] - h0["sig2_1d"]) / max(h0["sig2_1d"], 1e-9) < 0.20)
    return dict(tag=tag, mu=mu, sig_start=sig_start, R0=R0, footing=footing,
                t_end=t_end, eta=eta, nsteps=nsteps_used, seed=seed,
                wall=time.time() - t0,
                dE=float((E1 - E0) / abs(E0)),
                sig2_inf=sig2_1d, r50=float(np.median(r)),
                r90=float(np.quantile(r, 0.9)),
                md_rm=md_rm,
                f_esc=float((r > 10.0).mean()),
                slope=slope, sig_profile=sigprof,
                sig2_hist=[h["sig2_1d"] for h in hist],
                r50_hist=[h["r50"] for h in hist],
                relaxed=bool(relaxed))

def dispersion_profile(pos, vsub):
    r = np.sqrt((pos * pos).sum(1))
    out = []
    for lo, hi in ((0.3, 0.6), (0.6, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 3.0)):
        m = (r > lo) & (r < hi)
        out.append(float(np.sqrt((vsub[m] ** 2).sum() / (3.0 * m.sum()))) if m.sum() > 20 else None)
    return out

# ------------------------------------------------------------------ suite
def build_suite():
    cells, seeds = [], {}
    def T(mu, ss, R0, footing, t_end, seed, tag, eta=ETA):
        cells.append((mu, ss, R0, footing, t_end, seed, tag, eta))
    # --- C1 attractor suite, canonical (45) -----------------------------
    for mi, mu in enumerate(MU_GRID):
        for si, ss in enumerate(SIG_GRID):
            for ri, R0 in enumerate(R0_GRID):
                seed = 10000 + 100 * mi + 10 * si + ri
                t_end = 50.0 * max(R0, 0.2) / max(ss, 0.05)
                T(mu, ss, R0, "canonical", t_end, seed, "C1")
                seeds[f"{mu}/{ss}/{R0}"] = seed
    # --- C2 equilibrium-existence controls (3) --------------------------
    for mi, mu in enumerate(MU_GRID):
        seed = 10000 + 100 * mi + 33
        T(mu, 1.0, 0.0, "canonical", 100.0, seed, "C2")
        seeds[f"C2/{mu}"] = seed
    # --- alt-footing confirmation subset (9) ----------------------------
    alt = [(0.3, ss, 1.0) for ss in SIG_GRID] + \
          [(0.3, 1.0, 0.5), (0.3, 1.0, 2.0), (0.1, 1.0, 1.0), (1.0, 1.0, 1.0)]
    for (mu, ss, R0) in alt:
        seed = 20000 + int(mu * 100) + int(ss * 10) + int(R0 * 10)
        t_end = 50.0 * max(R0, 0.2) / max(ss, 0.05)
        T(mu, ss, R0, "alt", t_end, seed, "C1")
    # --- dt-convergence run (1) -----------------------------------------
    T(0.3, 0.5, 1.0, "canonical", 100.0, 10011, "C1dt", eta=ETA / 2.0)
    return cells, seeds

# ------------------------------------------------------------------ verdicts
def make_verdict(results, seeds):
    c1 = {k: v for k, v in results.items() if v["tag"] == "C1" and v["footing"] == "canonical"}
    c2 = {k: v for k, v in results.items() if v["tag"] == "C2"}
    dtr = next((v for v in results.values() if v["tag"] == "C1dt"), None)
    dtt = next((v for v in results.values() if v["tag"] == "C1" and
                v["mu"] == 0.3 and v["sig_start"] == 0.5 and v["R0"] == 1.0), None)
    # ---- P1/P2 on the primary suite (mu = 0.3) --------------------------
    prim = {k: v for k, v in c1.items() if v["mu"] == MU_PRIMARY}
    P1 = all(0.8 <= v["sig2_inf"] <= 1.25 for v in prim.values())
    P2 = all(0.5 <= v["r50"] <= 2.0 for v in prim.values())
    # ---- P3: control + diagonal stability --------------------------------
    c2m = next((v for v in c2.values() if v["mu"] == 1.0), None)
    diag = [v for v in prim.values() if v["sig_start"] == 1.0]
    P3 = (c2m is not None and 0.8 <= c2m["sig2_inf"] <= 1.25 and
          0.5 <= c2m["r50"] <= 2.0 and
          all(s is not None for s in c2m["sig_profile"]) and
          all(abs(s - 1.0) <= 0.25 for s in c2m["sig_profile"]) and
          all(v["relaxed"] for v in diag))
    # ---- instrument gates -------------------------------------------------
    allcells = [v for v in results.values() if v["tag"] in ("C1", "C2")]
    energy_ok = all(abs(v["dE"]) < 5e-2 for v in allcells)
    dtconv = (dtr is not None and dtt is not None and
              abs(dtr["sig2_inf"] - dtt["sig2_inf"]) / dtt["sig2_inf"] < 0.05 and
              abs(dtr["r50"] - dtt["r50"]) / dtt["r50"] < 0.05)
    relax_frac = sum(1 for v in allcells if v["relaxed"]) / max(len(allcells), 1)
    instrument_ok = energy_ok and dtconv and (relax_frac > 2.0 / 3.0)
    # ---- registered kill patterns -----------------------------------------
    kill_T = False
    for R0 in R0_GRID:
        cell = [v for v in prim.values() if v["R0"] == R0]
        if len(cell) == 5:
            s03 = next(v["sig2_inf"] for v in cell if v["sig_start"] == 0.3)
            s15 = next(v["sig2_inf"] for v in cell if v["sig_start"] == 1.5)
            if s15 > 1.25 * s03:
                kill_T = True
    r50_span = []
    for ss in SIG_GRID:
        rr = [v["r50"] for v in prim.values() if v["sig_start"] == ss]
        if len(rr) == 3:
            r50_span.append(max(rr) / min(rr))
    kill_R = any(s > 1.5 for s in r50_span)
    kill = (not P3) or kill_T or kill_R
    if not instrument_ok:
        verdict = "INSTRUMENT-FAIL"
    elif P1 and P2 and P3:
        verdict = "PASS"
    elif kill:
        verdict = "KILL"
    else:
        verdict = "NEUTRAL"
    return dict(P1=P1, P2=P2, P3=P3, kill_T=kill_T, kill_R=kill_R, kill=kill,
                instrument_ok=instrument_ok, energy_ok=energy_ok, dtconv=dtconv,
                relax_frac=relax_frac, verdict=verdict,
                r50_span={f"{ss}": s for ss, s in zip(SIG_GRID, r50_span)})

def transfer_matrices(results):
    """The registered deliverable: sigma_inf^2 and r50 as functions of
    (sigma_start, R0) for each mu (canonical footing, C1 runs)."""
    out = {}
    for mu in MU_GRID:
        for name, fn in (("sig2", lambda v: v["sig2_inf"]),
                         ("r50", lambda v: v["r50"])):
            M = {}
            for ss in SIG_GRID:
                row = {}
                for R0 in R0_GRID:
                    v = next((r for r in results.values()
                              if r["tag"] == "C1" and r["footing"] == "canonical"
                              and r["mu"] == mu and r["sig_start"] == ss and r["R0"] == R0), None)
                    row[str(R0)] = None if v is None else fn(v)
                M[str(ss)] = row
            out[f"{name}/mu={mu}"] = M
    return out

# ------------------------------------------------------------------ checks
RES = []
def check(name, measured, ok, reading=""):
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading:
        print(f"         reading : {reading}")
    RES.append(dict(name=name, measured=str(measured), **{"pass": ok}, reading=reading))

def gb_tuple(prof):
    return (prof[0], prof[1], prof[2], prof[3])

def static_validations():
    """V1-V5: the engine's correctness case, run before the suite."""
    print("\n--- STATIC VALIDATIONS ---")
    # V1: unit-system identity G M_b = 2 sigma_t^2 r_M on both footings
    for footing, a0 in (("canonical", A0_CAN), ("alt", A0_ALT)):
        rM, st, tc = zimmerman(MB_MSUN, a0)
        lhs = G_SI * MB_MSUN * MSUN
        rhs = 2.0 * st * st * rM
        check(f"V1 [{footing}] unit identity G M_b = 2 sigma_t^2 r_M",
              f"|lhs/rhs - 1| = {abs(lhs / rhs - 1):.2e}",
              abs(lhs / rhs - 1) < 1e-9,
              "the code-unit system is the physical one; G_code = 2 exact")
    # V2: the real baryon curve reproduces the bundle M_b (closed loop)
    prof = load_baryon_profile(A0_CAN)
    xs, ys, sxl, sxr, rM, st, gal = prof
    Mb_max = float(np.exp(ys).max())
    Mb_last = float(np.exp(ys[-1]))
    check("V2 bundle M_b closed loop (max enclosed baryons of the real curve)",
          f"max M/M_b = {Mb_max:.6f} (expect 1.0 by construction), "
          f"M(x_last)/M_b = {Mb_last:.4f} (last curve point, 0.2% noise, registered), "
          f"x_last = {math.exp(xs[-1]):.2f} r_M",
          abs(Mb_max - 1.0) < 1e-9 and Mb_last > 0.99,
          "the baryon field is the bundle's own curve, normalised to its own M_b "
          "(the G033 pipeline M_b definition: MAX enclosed baryons)")
    # V3: baryon field structure: solid-body head BELOW the curve's first point
    # (x_first = 0.033 r_M), flat-vb tail beyond the last point (both pure regimes)
    x0 = math.exp(xs[0])
    ga, gb_ = (float(gb_code(np.array([x]), *gb_tuple(prof))[0]) for x in (0.01, 0.02))
    g1 = float(gb_code(np.array([1.0]), *gb_tuple(prof))[0])
    x1 = math.exp(xs[-1])
    gx1 = float(gb_code(np.array([x1]), *gb_tuple(prof))[0])
    g2x1 = float(gb_code(np.array([2 * x1]), *gb_tuple(prof))[0])
    check("V3 baryon field structure",
          f"g(0.01)/g(0.02) = {ga / gb_:.3f} (solid body: 0.500); "
          f"g(2 x_last)/g(x_last) = {g2x1 / gx1:.3f} (flat-vb: 0.500); g(r_M) = {g1:.3f}",
          abs(ga / gb_ - 0.5) < 0.02 and abs(g2x1 / gx1 - 0.5) < 0.05,
          "interior solid-body below x_first, tail flat-v_b (g ~ 1/x); no softening")
    # V4: closed-form potential differentiates back to the field
    xg = np.logspace(-1.3, 1.6, 2000)
    ph = phi_baryon(xg, gb_tuple(prof))
    dph = np.gradient(ph, np.log(xg))            # dphi/dlnx = x g_b (phi < 0)
    xgd = gb_code(xg, *gb_tuple(prof)) * xg
    m = xgd > 0
    worst = float(np.abs(dph[m] / xgd[m] - 1).max())
    check("V4 closed-form potential vs field: -dphi/dln r = r g_b",
          f"max rel dev = {worst:.2e} (finite-difference, 2000 pts)",
          worst < 5e-2,
          "the exact segment integrals reproduce g_b; the PE bookkeeping is correct")
    # V5: tracer-orbit conservation in the real baryon field
    mp = 1e-9
    x0 = 1.5
    g15 = float(gb_code(np.array([x0]), *gb_tuple(prof))[0])
    pos = np.array([[x0, 0.0, 0.0]])
    vel = np.array([[0.0, math.sqrt(g15 * x0 * 0.8), 0.0]])
    gb_args = gb_tuple(prof)
    eps2 = EPS_RM ** 2
    acc = accelerations(pos, mp, eps2, gb_args)
    E0 = energy(pos, vel, mp, EPS_RM, gb_args)
    L0 = mp * float(pos[0, 0] * vel[0, 1] - pos[0, 1] * vel[0, 0])
    t = 0.0
    while t < 20.0:
        # the suite's validated free-fall step (tracer: mu ~ 0 in the denominator)
        r2p = float(pos[0, 0] ** 2 + pos[0, 1] ** 2 + pos[0, 2] ** 2) + eps2
        menb = float(np.exp(menc_over_mb(np.log(max(math.sqrt(r2p - eps2), 1e-6)), *gb_args)))
        tau = math.sqrt(r2p ** 1.5 / (menb + mp))
        dt = min(ETA * tau, 0.02, 20.0 - t)
        vel += 0.5 * dt * acc
        pos += dt * vel
        acc = accelerations(pos, mp, eps2, gb_args)
        vel += 0.5 * dt * acc
        t += dt
    E1 = energy(pos, vel, mp, EPS_RM, gb_args)
    L1 = mp * float(pos[0, 0] * vel[0, 1] - pos[0, 1] * vel[0, 0])
    check("V5 tracer-orbit conservation in the real baryon field",
          f"dE/E = {(E1 - E0) / abs(E0):+.2e}, dL/L = {abs((L1 - L0) / L0):.2e} over 20 t_cross",
          abs((E1 - E0) / abs(E0)) < 1e-3 and abs((L1 - L0) / L0) < 1e-3,
          "leapfrog conserves E and L in the exact external field (mp ~ 0)")
    # V6: THE FORCE IS ATTRACTIVE -- baryon term points INWARD (-r_hat)
    for xr in (0.05, 0.3, 1.0, 3.0):
        p1 = np.array([[xr, 0.0, 0.0]])
        a1 = accelerations(p1, 1e-12, EPS_RM ** 2, gb_tuple(prof))   # baryons only
        radial = float(a1[0, 0] * p1[0, 0] / (np.linalg.norm(a1[0]) * xr + 1e-30))
        check(f"V6a baryon force direction at r = {xr} r_M",
              f"a.r_hat = {radial:+.6f} (attractive: -1)",
              radial < -0.999,
              "the field pulls toward the origin (a sign error here invalidates everything)")
    # V6b: self-gravity attractive -- two particles fall together
    p2 = np.array([[-0.5, 0.0, 0.0], [0.5, 0.0, 0.0]])
    a2 = accelerations_selfonly(p2, 1.0, EPS_RM ** 2)
    closing = bool(a2[0, 0] > 0 and a2[1, 0] < 0)
    check("V6b self-gravity direction (two particles close, do not repel)",
          f"a(left) x = {a2[0, 0]:+.4f} > 0, a(right) x = {a2[1, 0]:+.4f} < 0",
          closing,
          "particles accelerate toward each other")
    # V7: inverse-square orbit stays BOUND (an outward force would unbind it)
    prof_pt = (np.array([math.log(0.1), math.log(10.0)]), np.array([0.0, 0.0]), 3.0, 1.0)
    mp_t = 1e-12
    pos_t = np.array([[1.0, 0.0, 0.0]])
    vel_t = np.array([[0.0, math.sqrt(2.0 * 1.0 * 0.95), 0.0]])   # slightly sub-circular
    acc_t = accelerations(pos_t, mp_t, 1e-8, prof_pt)
    E0t = energy(pos_t, vel_t, mp_t, 1e-4, prof_pt)
    r0t = 1.0
    t = 0.0
    rmin_t, rmax_t = 1.0, 1.0
    while t < 12.0:                       # ~2 orbital periods
        r2p = float(pos_t[0, 0] ** 2 + pos_t[0, 1] ** 2) + 1e-8
        tau = math.sqrt(r2p ** 1.5 / (1.0 + mp_t))
        dt = min(ETA * tau, 0.02, 12.0 - t)
        vel_t += 0.5 * dt * acc_t
        pos_t += dt * vel_t
        acc_t = accelerations(pos_t, mp_t, 1e-8, prof_pt)
        vel_t += 0.5 * dt * acc_t
        t += dt
        rr = math.hypot(pos_t[0, 0], pos_t[0, 1])
        rmin_t = min(rmin_t, rr); rmax_t = max(rmax_t, rr)
    E1t = energy(pos_t, vel_t, mp_t, 1e-4, prof_pt)
    check("V7 inverse-square orbit bound",
          f"r in [{rmin_t:.3f}, {rmax_t:.3f}] (start 1.0, sub-circular v), dE/E = {(E1t - E0t) / abs(E0t):+.2e}",
          rmin_t < 0.98 and rmax_t < 1.1 and abs((E1t - E0t) / abs(E0t)) < 1e-3,
          "a 1/r^2 attractive field keeps the orbit bound and oscillating")
    # V8: numba kernel == numpy kernel (machine agreement)
    posk, _ = ic_uniform(500, 1.0, 0.7, 0.3, 424242)
    mpk = 0.3 / 500
    acc_k = np.empty_like(posk)
    _accel_self_nb(posk, acc_k, mpk, EPS_RM ** 2, GCODE)
    dxk = posk[:, None, 0] - posk[None, :, 0]
    dyk = posk[:, None, 1] - posk[None, :, 1]
    dzk = posk[:, None, 2] - posk[None, :, 2]
    r2k = dxk * dxk + dyk * dyk + dzk * dzk + EPS_RM ** 2
    inv3 = r2k ** -1.5
    np.fill_diagonal(inv3, 0.0)
    acc_ref = np.stack([-GCODE * mpk * (dxk * inv3).sum(1),
                        -GCODE * mpk * (dyk * inv3).sum(1),
                        -GCODE * mpk * (dzk * inv3).sum(1)], 1)
    dev = float(np.abs((acc_k - acc_ref) / (np.abs(acc_ref).max() + 1e-30)).max())
    check("V8 numba kernel vs numpy kernel",
          f"max abs dev = {dev:.2e} (500 particles), numba = {HAVE_NUMBA}",
          dev < 1e-10,
          "the production kernel is the validated kernel (fallback identity)")

# ------------------------------------------------------------------ main
def main():
    t00 = time.time()
    print("=" * 78)
    print("G035 -- THE ATTRACTOR TEST (pre-registered verdicts in")
    print("        G035_preregistration.md; frozen BEFORE this suite ran)")
    print("=" * 78)
    for footing, a0 in (("canonical", A0_CAN), ("alt", A0_ALT)):
        rM, st, tc = zimmerman(MB_MSUN, a0)
        print(f"  [{footing:9s}] a0 = {a0:.4e}  r_M = {rM/KPC_M:6.3f} kpc  "
              f"sigma_target = {st/KMS:7.2f} km/s  t_cross(r_M) = {tc/MYR:6.2f} Myr")
    static_validations()
    if any(not c["pass"] for c in RES):
        print("STATIC VALIDATION FAILED -- suite not launched.")
        json.dump(dict(checks=RES), open(OUT, "w"), indent=1)
        return
    cells, seeds = build_suite()
    print(f"\n--- SUITE: {len(cells)} runs x {N_PART} particles, "
          f"eps = {EPS_RM} r_M, adaptive dt (eta = {ETA}, cap {DT_MAX}) ---")
    results = {}
    with Pool(10) as pool:
        for res in pool.imap_unordered(run_cell, cells):
            key = f"{res['tag']}/{res['footing']}/{res['mu']}/{res['sig_start']}/{res['R0']}"
            results[key] = res
            print(f"  [{key}]  sig2/sig2t = {res['sig2_inf']:.3f}  "
                  f"r50 = {res['r50']:.3f} r_M  slope = {res['slope']:+.2f}  "
                  f"f_esc = {res['f_esc']:.2f}  dE/E = {res['dE']:+.1e}  "
                  f"relaxed = {res['relaxed']}  ({res['wall']:.0f}s)", flush=True)
    json.dump(results, open(OUTX, "w"), indent=1)
    print(f"\n  all runs done in {time.time()-t00:.0f}s -> {OUTX}")

    # ---- verdicts ----------------------------------------------------
    v = make_verdict(results, seeds)
    tm = transfer_matrices(results)
    print("\n" + "=" * 78)
    print("TRANSFER FUNCTION sigma_inf^2/sigma_target^2 (rows sigma_start, cols R0):")
    for mu in MU_GRID:
        M = tm[f"sig2/mu={mu}"]
        print(f"  mu = {mu}:")
        for ss in SIG_GRID:
            row = M[str(ss)]
            print(f"    sigma_start = {ss}: " +
                  "  ".join(f"R0={r}: {row[str(r)]:.3f}" for r in R0_GRID))
    print("TRANSFER FUNCTION r50/r_M:")
    for mu in MU_GRID:
        M = tm[f"r50/mu={mu}"]
        print(f"  mu = {mu}:")
        for ss in SIG_GRID:
            row = M[str(ss)]
            print(f"    sigma_start = {ss}: " +
                  "  ".join(f"R0={r}: {row[str(r)]:.3f}" for r in R0_GRID))
    print("-" * 78)
    print(f"P1 (temperature in [0.8, 1.25] everywhere, mu = {MU_PRIMARY}): {v['P1']}")
    print(f"P2 (r50 in [0.5, 2.0] r_M everywhere):                          {v['P2']}")
    print(f"P3 (control holds + diagonal stable):                           {v['P3']}")
    print(f"instrument: energy_ok = {v['energy_ok']}, dt-convergence = {v['dtconv']}, "
          f"relaxed {100 * v['relax_frac']:.0f}% of cells")
    print(f"VERDICT: {v['verdict']}")
    json.dump(dict(checks=RES, verdict=v, transfer=tm,
                   constants=dict(Mb_msun=MB_MSUN, N=N_PART, eps_rm=EPS_RM,
                                  eta=ETA, dt_max=DT_MAX, xmax=XMAX)),
              open(OUT, "w"), indent=1)
    print(f"\nResults written to {OUT}")
    print(f"G035 COMPLETE: verdict = {v['verdict']} ({time.time()-t00:.0f}s total).")

if __name__ == "__main__":
    main()
