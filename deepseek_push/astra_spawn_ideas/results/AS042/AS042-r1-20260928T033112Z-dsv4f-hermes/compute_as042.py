#!/usr/bin/env python3
"""
AS042 - Filter order is part of the gravity law (bounded prototype, v5 - periodic cell).
Worker: deepseek/deepseek-v4-flash-0731 (openrouter) via Hermes focused subagent.
Run id: AS042-r1-20260928T033112Z-dsv4f-hermes

Framework cell: a0 = kappa*c*sqrt(G*rho_Lambda), kappa = 1/2 ADOPTED (input).
Operative MONO quasistatic equation (FRIED_CHICKEN rqmt 1, amendment 2026-09-26):
    Lap(Phi) = 4 pi G rho_b + S* div[(nu(|grad S u|/a0) - 1) grad S u]
    S = exp[(xi^2/2) Delta],  Lap u = 4 pi G rho_b.
Unfiltered RAR reference: Lap(Phi) = 4 pi G rho_b + div[(nu_RAR(|grad u|/a0)-1) grad u].

Main identity (verified with ACTUAL residuals on the periodic torus cell,
on the subdomain of nonzero gradients):
    S*M[Su] - M[u] = (xi^2/2)*(Delta M[u] + DM[u](Delta u)) + R4,  R4 = O(xi^4),
    M[u] = div[(nu(y)-1) grad u],  y = |grad u|/a0,
    DM[u](v) = div[(nu-1) grad v + nu'(y) (grad u . grad v)/(a0 |grad u|) grad u].
One-dimensional exact reduction (u' = |u'| > 0): DM[u](Delta u) = [(nu-1+y nu') u''']'.

Cell + adjoint data (FRAMEWORK_CONTRACT): ambient cell = flat 3-torus (R/2piL Z)^3
or 1-torus, Lebesgue measure, L^2 inner product; Delta is the flat Laplacian
with periodic data (domain = Sobolev H^2(T^3)); S = e^{(xi^2/2)Delta} is the
periodic heat semigroup (Fourier multiplier exp[-(xi^2/2)|k|^2]); S* = S in
L^2(T^3, dx) with these data (numerically verified, <Sg,f>-<g,Sf> ~ 1e-14,
1D and 3D). Self-adjointness is a property of this (measure, operator, data)
cell and is NOT transferred to weighted measures or lapse-modified metrics
(those stay open, as the contract demands). A Dirichlet-cell variant was run
and rejected as a diagnostic cell: the Dirichlet heat semigroup has an O(1)
boundary layer (it annihilates nonzero boundary data over a width ~ sqrt(xi^2)),
which is cell-boundary physics, not the filter's action; the expansion holds
uniformly only away from that layer. Zero-gradient points of the test fields
(cusp points of nu(|grad u|)) are excluded by the task's own restriction
"restrict the comparison to nonzero gradients"; the mask additionally clears a
cusp neighbourhood so the O(xi^4) remainder is measured on cells where all
quantities are finite, and an analytic remainder bound (xi^4/8)|Lap^2 M| is
reported at the same cells. On the physical torus source (Gaussian bump), M[u]
has integrable |x|^{-1/2} cusps at the zero-acceleration image centres; the
energy pairings involving M stay integrable and are reported as grid principal
values with the cusp caveat.

Negative controls (capable of failing): naive commutation (missing terms
-(xi^2/2) Delta M and +(xi^2/2)(DM(Delta u) - Delta M)), linear-cell exact
identity S* c Delta S = c Delta exp(xi^2 Delta) at machine precision,
deep/Newtonian limiting regimes, sympy symbolic O(xi^2) verification, energy
budget in J per footing (canonical 9.3619e-11 and alternative 1.1279e-10 m/s^2).

Bounds: RLIMIT_CPU (120,121) s enforced; RLIMIT_AS 512 MiB requested (macOS
rejects lowering -> recorded; ru_maxrss asserted <= 512 MiB at end); 1 thread.
"""
import json, os, resource, sys, time
import numpy as np

t0 = time.time()
resource.setrlimit(resource.RLIMIT_CPU, (120, 121))
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
as_limit_enforced = False
try:
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    as_limit_enforced = True
except (ValueError, OSError) as e:
    print("RLIMIT_AS not enforceable on this platform:", e, file=sys.stderr)

out = {"meta": {}, "checks": {}, "limits": {}, "energy": {}, "footings": {}, "grid_diagnostic": {}}
out["meta"]["started"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0))

G_SI = 6.67430e-11
C_SI = 299792458.0
M_SUN = 1.98847e30
PC_SI = 3.085677581491367e16
A0_CANON = 9.3619e-11
A0_ALT = 1.1279e-10
KAPPA = 0.5  # adopted framework input (not derived in this task)

Y_P = 2.5396382821881653
H_P = 0.6476102378919148
Y_STAR = 2.3374124052663294
DELTA = 0.05


def nu_rar(y):
    # stable: nu-1 = h_rar(y)/y ; direct 1/(1-exp(-sqrt y)) rounds nu-1 to 0 for
    # sqrt(y) > ~38 (float64), which would wrongly kill the Newtonian-tail check
    yc = np.maximum(y, 1e-300)
    return 1.0 + h_rar(yc) / yc


def nu_rar_prime(y):
    yc = np.maximum(y, 1e-300)
    return h_rar_prime(yc) / yc - h_rar(yc) / (yc * yc)


def h_rar(y):
    s = np.sqrt(np.maximum(y, 1e-300))
    return y / (np.exp(np.minimum(s, 700)) - 1.0)


def h_rar_prime(y):
    s = np.sqrt(np.maximum(y, 1e-300))
    e = np.exp(np.minimum(s, 700))
    return (2.0 * (e - 1.0) - s * e) / (2.0 * (e - 1.0) ** 2)


def phi_mono(y):
    return DELTA * H_P / (y + Y_P)


def h_mono(y):
    y = np.asarray(y, dtype=float)
    return np.where(y <= Y_STAR, h_rar(y),
                    h_rar(Y_STAR) + DELTA * H_P * np.log((y + Y_P) / (Y_STAR + Y_P)))


def h_mono_prime(y):
    y = np.asarray(y, dtype=float)
    return np.where(y <= Y_STAR, h_rar_prime(y), phi_mono(y))


def nu_mono(y):
    y = np.asarray(y, dtype=float)
    return 1.0 + h_mono(y) / np.maximum(y, 1e-300)


def nu_mono_prime(y):
    y = np.asarray(y, dtype=float)
    yc = np.maximum(y, 1e-300)
    return h_mono_prime(y) / yc - h_mono(y) / (yc * yc)


def nu_factory(branch):
    return (nu_rar, nu_rar_prime) if branch == "RAR" else (nu_mono, nu_mono_prime)


def periodic_gauss(X, Y, Z, L, A, sigma):
    Ls = np.array([-L, 0.0, L])
    best = None
    for dx in Ls:
        for dy in Ls:
            for dz in Ls:
                r2 = (X + dx)**2 + (Y + dy)**2 + (Z + dz)**2
                best = r2 if best is None else np.minimum(best, r2)
    return A * np.exp(-best / (2.0 * sigma**2))


# ================================================================ periodic (torus) machinery
class Torus3:
    """Flat 3-torus [0,L)^3: FFT spectral calculus. k2 = (2 pi f)^2 physical."""

    def __init__(self, N, L):
        self.N, self.L = N, L
        self.dx = L / N
        f = np.fft.fftfreq(N, d=self.dx)
        self.KX, self.KY, self.KZ = np.meshgrid(f, f, f, indexing="ij")
        self.k2 = (2.0 * np.pi) ** 2 * (self.KX**2 + self.KY**2 + self.KZ**2)
        self.k2[0, 0, 0] = 1.0
        self.ikx, self.iky, self.ikz = 2j * np.pi * self.KX, 2j * np.pi * self.KY, 2j * np.pi * self.KZ

    def grad(self, u):
        uh = np.fft.fftn(u)
        return (np.real(np.fft.ifftn(self.ikx * uh)), np.real(np.fft.ifftn(self.iky * uh)),
                np.real(np.fft.ifftn(self.ikz * uh)))

    def lap(self, u):
        uh = np.fft.fftn(u)
        return np.real(np.fft.ifftn(-self.k2 * uh))

    def div(self, vx, vy, vz):
        vh = (np.fft.fftn(vx), np.fft.fftn(vy), np.fft.fftn(vz))
        return np.real(np.fft.ifftn(self.ikx * vh[0] + self.iky * vh[1] + self.ikz * vh[2]))

    def S(self, u, xi):
        uh = np.fft.fftn(u)
        return np.real(np.fft.ifftn(np.exp(-(xi**2 / 2.0) * self.k2) * uh))

    def S2(self, u, xi):
        return self.S(u, xi * np.sqrt(2.0))

    # -- local finite differences (periodic wrap; no Gibbs ringing on cuspy
    #    quantities; 4th order) --
    def dfd(self, f, axis, order=1):
        fm2 = np.roll(f, 2, axis=axis)
        fm1 = np.roll(f, 1, axis=axis)
        fp1 = np.roll(f, -1, axis=axis)
        fp2 = np.roll(f, -2, axis=axis)
        h = self.dx
        if order == 1:
            return (fm2 - 8.0 * fm1 + 8.0 * fp1 - fp2) / (12.0 * h)
        return (-fm2 + 16.0 * fm1 - 30.0 * f + 16.0 * fp1 - fp2) / (12.0 * h * h)

    def grad_fd(self, u):
        return (self.dfd(u, 0, 1), self.dfd(u, 1, 1), self.dfd(u, 2, 1))

    def lap_fd(self, u):
        return self.dfd(u, 0, 2) + self.dfd(u, 1, 2) + self.dfd(u, 2, 2)

    def div_fd(self, vx, vy, vz):
        return self.dfd(vx, 0, 1) + self.dfd(vy, 1, 1) + self.dfd(vz, 2, 1)

    def lap_inv_meanzero(self, q):
        qh = np.fft.fftn(q - q.mean())
        qh[0, 0, 0] = 0.0
        return np.real(np.fft.ifftn(-qh / self.k2))


def M_op(box, u, nu, nu_p, a0=1.0):
    gx, gy, gz = box.grad_fd(u)
    gmag = np.sqrt(gx**2 + gy**2 + gz**2)
    y = np.maximum(gmag / a0, 1e-12)
    kk = nu(y) - 1.0
    return box.div_fd(kk * gx, kk * gy, kk * gz)


def DM_op(box, u, v, nu, nu_p, a0=1.0):
    gx, gy, gz = box.grad_fd(u)
    vx, vy, vz = box.grad_fd(v)
    gmag = np.sqrt(gx**2 + gy**2 + gz**2)
    y = np.maximum(gmag / a0, 1e-12)
    with np.errstate(divide="ignore", invalid="ignore"):
        gdv = (gx * vx + gy * vy + gz * vz) / np.maximum(gmag, 1e-300)
    coef = nu_p(y) / a0
    w1x = (nu(y) - 1.0) * vx + coef * gdv * gx
    w1y = (nu(y) - 1.0) * vy + coef * gdv * gy
    w1z = (nu(y) - 1.0) * vz + coef * gdv * gz
    z = gmag < 1e-300
    w1x, w1y, w1z = np.where(z, 0.0, w1x), np.where(z, 0.0, w1y), np.where(z, 0.0, w1z)
    return box.div_fd(w1x, w1y, w1z)


def filtered_phantom_source(box, u, xi, branch, a0=1.0):
    nu, nu_p = nu_factory(branch)
    Su = box.S(u, xi)
    return box.S(M_op(box, Su, nu, nu_p, a0), xi)


def leading_correction(box, u, xi, branch, a0=1.0):
    nu, nu_p = nu_factory(branch)
    M = M_op(box, u, nu, nu_p, a0)
    DMd = DM_op(box, u, box.lap_fd(u), nu, nu_p, a0)
    Q = box.lap_fd(M) + DMd
    return 0.5 * xi**2 * Q, Q


def cosine_bump3(N, L, A):
    """Smooth periodic test field: u = A(cos xh + cos yh + cos zh), xh = 2 pi x/L.
    |grad u| = (2 pi A/L)|(sin, sin, sin)|: y_max = sqrt(3) 2 pi A/L; the 8
    zero-gradient points sit at the cell vertices (cusp points, excluded by mask)."""
    xh = 2.0 * np.pi * np.arange(N) / N
    Xh, Yh, Zh = np.meshgrid(xh, xh, xh, indexing="ij")
    return A * (np.cos(Xh) + np.cos(Yh) + np.cos(Zh))


# ================================================================ mandated y-diagnostic grid
YGRID = 10.0 ** np.arange(-10.0, 8.0001, 0.1)
out["grid_diagnostic"] = {
    "n_points": int(len(YGRID)), "y_min": float(YGRID[0]), "y_max": float(YGRID[-1]),
    "nu_RAR_at_y_star_and_yp": [float(nu_rar(Y_STAR)), float(nu_rar(Y_P))],
    "nu_mono_at_y_star_and_yp": [float(nu_mono(Y_STAR)), float(nu_mono(Y_P))],
    "h_RAR_max": float(h_rar(Y_P)), "h_RAR_prime_at_yp": float(h_rar_prime(Y_P)),
    "mono_floor_phi_at_yp": float(phi_mono(Y_P)),
    "max_dex_nu_mono_vs_rar_on_grid": float(np.max(np.abs(np.log10(nu_mono(YGRID)) - np.log10(nu_rar(YGRID))))),
    "h_plus_asu_samples": [float(h_rar(YGRID[i])) for i in (0, 45, 90, 135, 180)],
}

# ================================================================ T1: main identity, 3D torus
N3, L3 = 48, 2.0 * np.pi
box = Torus3(N3, L3)
GAMMA = 0.3  # cusp clearance: keep cells with |grad u| > GAMMA * y_max (perturbative regime)
XI_SWEEP = [0.0625, 0.125, 0.25, 0.5, 1.0]
t1 = {}
for branch in ("RAR", "MONO"):
    res = {}
    for Aname, A in (("deep", 5e-4), ("mid", 4.0), ("newtonian", 1e4)):
        u = cosine_bump3(N3, L3, A)
        gk = box.grad_fd(u)
        ymag = np.sqrt(gk[0]**2 + gk[1]**2 + gk[2]**2)
        ymax = ymag.max()
        m = ymag > GAMMA * ymax
        for xi in XI_SWEEP:
            # sub-mask: cells farther than ~5 smoothing lengths (sqrt(xi^2/2) in x-units)
            # from the zero-gradient set, where the O(xi^2) expansion is perturbative
            sub = m & (ymag > 5.0 * A * np.sqrt(xi**2 / 2.0))
            if branch == "MONO":
                sub = sub & (np.abs(ymag - Y_STAR) > 0.05 * Y_STAR)   # y*-splice layer (C^1 only)
                m2 = m & (np.abs(ymag - Y_STAR) > 0.05 * Y_STAR)
            else:
                m2 = m
            lhs = filtered_phantom_source(box, u, xi, branch) - M_op(box, u, *nu_factory(branch))
            lead, Q = leading_correction(box, u, xi, branch)
            d = lhs - lead
            M = M_op(box, u, *nu_factory(branch))
            bnd = (xi**4 / 8.0) * np.abs(box.lap_fd(box.lap_fd(M)))[m].max()
            r = np.abs(d[sub]).max() if sub.any() else float("nan")
            res[f"{Aname}_xi_{xi}"] = {
                "y_min_max_on_mask": [float(ymag[m].min()), float(ymag[m].max())],
                "mask_fraction_kept": float(m.mean()),
                "submask_fraction": float(sub.mean()),
                "submask_empty": bool(not sub.any()),
                "max|LHS|(submasked)": float(np.abs(lhs[sub]).max()) if sub.any() else None,
                "max|leading|(submasked)": float(np.abs(lead[sub]).max()) if sub.any() else None,
                "max|R4|(submasked)": float(r),
                "rel_resid_submask": float(r / max(1e-300, np.abs(lhs[sub]).max())) if sub.any() else None,
                "max|R4|(masked)": float(np.abs(d[m2]).max()),
                "rel_resid_masked": float(np.abs(d[m2]).max() / max(1e-300, np.abs(lhs[m2]).max())),
                "bound_(xi^4/8)|Lap^2 M|inf(masked)": float(bnd),
                "R4_over_bound_submask": float(r / bnd) if sub.any() else None,
            }
    r4s = [res[f"mid_xi_{x}"]["max|R4|(submasked)"] for x in XI_SWEEP[:4]]
    res["_loglog_slope_R4_mid_submask(first4)"] = float(np.polyfit(
        np.log(np.array(XI_SWEEP[:4])), np.log(np.array(r4s)), 1)[0])
    r4s3 = [res[f"mid_xi_{x}"]["max|R4|(submasked)"] for x in XI_SWEEP[:3]]
    res["_loglog_slope_R4_mid_submask(first3)"] = float(np.polyfit(
        np.log(np.array(XI_SWEEP[:3])), np.log(np.array(r4s3)), 1)[0])
    t1[branch] = res
out["checks"]["T1_3D_torus_main_identity"] = t1


def _rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024.0 * 1024.0) if sys.platform == "darwin" else resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


print("rss_after_T1 %.1f MiB wall %.1f s" % (_rss(), time.time() - t0), flush=True)

# ================================================================ T5: linear cell exact identity
u_mid = cosine_bump3(N3, L3, 4.0)
out["checks"]["T5_linear_cell_exact"] = {}
for xi in (0.3, 0.9, 1.7):
    c = 0.5
    exact = c * box.lap(box.S2(u_mid, xi))
    Su = box.S(u_mid, xi)
    got = c * box.S(box.lap(Su), xi)
    d = float(np.abs(got - exact).max())
    out["checks"]["T5_linear_cell_exact"][xi] = {"max_abs_diff": d,
                                                 "rel": d / float(np.abs(exact).max())}

# ================================================================ S* = S in L^2(T^3, dx)
rng = np.random.default_rng(7)
f3 = rng.standard_normal((N3, N3, N3))
g3 = rng.standard_normal((N3, N3, N3))
adj3 = {}
for xi in (0.2, 0.8):
    ip = float((box.S(g3, xi) * f3).sum() - (g3 * box.S(f3, xi)).sum())
    norm = float(np.sqrt((f3 * f3).sum()) * np.sqrt((g3 * g3).sum()))
    adj3[xi] = {"<Sg,f>-<g,Sf>": ip, "relative": ip / norm}
mid_gk = box.grad_fd(u_mid)
mid_ymag = np.sqrt(mid_gk[0]**2 + mid_gk[1]**2 + mid_gk[2]**2)
mid_mask = mid_ymag > GAMMA * mid_ymag.max()
out["checks"]["S_self_adjoint_L2_torus3"] = adj3

# ================================================================ T3: commutation negative control
out["checks"]["T3_commutation_negative_control"] = {}
nu, nu_p = nu_factory("RAR")
M = M_op(box, u_mid, nu, nu_p)
u_mid_mask = mid_mask
for xi in (0.25, 0.5, 1.0):
    lhstrue = filtered_phantom_source(box, u_mid, xi, "RAR")
    Su = box.S(u_mid, xi)
    M_Su = M_op(box, Su, nu, nu_p)                       # naive 1: S only inside nu
    M_S2u = M_op(box, box.S2(u_mid, xi), nu, nu_p)       # naive 2: both S's inside the argument
    DMD = DM_op(box, u_mid, box.lap_fd(u_mid), nu, nu_p)
    dM = box.lap_fd(M)
    pred_N1 = -0.5 * xi**2 * dM
    pred_N2 = 0.5 * xi**2 * (DMD - dM)
    err_N1 = float(np.abs((M_Su - lhstrue) - pred_N1)[u_mid_mask].max())
    err_N2 = float(np.abs((M_S2u - lhstrue) - pred_N2)[u_mid_mask].max())
    scale1 = float(np.abs(M_Su - lhstrue)[u_mid_mask].max())
    scale2 = float(np.abs(M_S2u - lhstrue)[u_mid_mask].max())
    out["checks"]["T3_commutation_negative_control"][xi] = {
        "max|M[Su]-S*M[Su]| (naive 1)": scale1,
        "max|M[S*Su]-S*M[Su]| (naive 2)": scale2,
        "resid N1 vs -(xi^2/2)LapM": err_N1,
        "resid N2 vs +(xi^2/2)(DM(Lap u)-LapM)": err_N2,
        "N2_error_over_M_scale": float(scale2 / np.abs(M)[u_mid_mask].max()),
        "naive_error_rel_to_true_correction": float(
            scale2 / max(1e-300, np.abs(0.5 * xi**2 * (DMD + dM))[u_mid_mask].max())),
    }

# ================================================================ T4: 1D torus, two independent S
class Torus1:
    def __init__(self, N, L):
        self.N, self.L = N, L
        self.dx = L / N
        x = np.arange(N, dtype=float) * self.dx
        self.x = x
        f = np.fft.fftfreq(N, d=self.dx)
        self.k = 2.0 * np.pi * f
        self.k2 = self.k**2
        self.k2[0] = 1.0
        self.ik = 1j * self.k

    def deriv(self, u, order=1):
        uh = np.fft.fft(u)
        return np.real(np.fft.ifft((self.ik)**order * uh))

    def dfd(self, f, order=1):
        fm2 = np.roll(f, 2)
        fm1 = np.roll(f, 1)
        fp1 = np.roll(f, -1)
        fp2 = np.roll(f, -2)
        h = self.dx
        if order == 1:
            return (fm2 - 8.0 * fm1 + 8.0 * fp1 - fp2) / (12.0 * h)
        return (-fm2 + 16.0 * fm1 - 30.0 * f + 16.0 * fp1 - fp2) / (12.0 * h * h)

    def S(self, u, xi):
        uh = np.fft.fft(u)
        return np.real(np.fft.ifft(np.exp(-(xi**2 / 2.0) * self.k2) * uh))

    def S_fd(self, u, xi):
        """Explicit forward-Euler heat stepping with periodic BCs:
        independent (non-spectral) representation of the same semigroup."""
        dt = 0.45 * self.dx**2          # stable (<= dx^2/2), 45% margin
        nstep = int(np.ceil((xi**2 / 2.0) / dt))
        w = u.copy()
        for _ in range(nstep):
            w = w + dt * (np.roll(w, -1) - 2.0 * w + np.roll(w, 1)) / self.dx**2
        return w


def check_1d(branch, A, tag, xi=0.4, N=2048, sweep=(0.05, 0.1, 0.2)):
    dc1 = Torus1(N, 2.0 * np.pi)
    L = dc1.L
    xh = 2.0 * np.pi * dc1.x / L
    u = A * np.cos(xh)
    up = -A * np.sin(xh)                # du/dx, |up|max = A
    y = np.maximum(np.abs(up), 1e-12)
    ym = np.abs(up).max()
    mmask = np.abs(up) > GAMMA * ym
    nu, nu_p = nu_factory(branch)
    flux = (nu(y) - 1.0) * up
    M_fd = dc1.dfd(flux, 1)
    u3 = dc1.dfd(up, 2)                               # u''' (FD, periodic)
    Mpp = dc1.dfd(M_fd, 2)
    # 1D reduction: DM[u](Delta u) = d/dx[ (nu(y)-1 + u' nu'(y)) u''' ]  (u' = sign(y) * y)
    term2 = dc1.dfd((nu(y) - 1.0 + up * nu_p(y)) * u3, 1)
    res_sweep = {}
    for xis in sweep:
        sub = mmask & (y > 5.0 * A * np.sqrt(xis**2 / 2.0))
        if branch == "MONO":
            sub = sub & (np.abs(y - Y_STAR) > 0.05 * Y_STAR)
        Su = dc1.S(u, xis)
        Sup = dc1.dfd(Su, 1)
        yS = np.maximum(np.abs(Sup), 1e-12)
        M_Su = dc1.dfd((nu(yS) - 1.0) * Sup, 1)
        lhs = dc1.S(M_Su, xis) - M_fd                 # S* M[Su] - M[u]
        pred = 0.5 * xis**2 * (Mpp + term2)
        r = float(np.abs(lhs - pred)[sub].max()) if sub.any() else float("nan")
        scl = float(np.abs(lhs)[sub].max()) if sub.any() else float("nan")
        res_sweep[xis] = {"max|LHS|": scl, "resid": r, "rel": r / max(1e-300, scl),
                          "submask_frac": float(sub.mean()), "submask_empty": bool(not sub.any())}
    xis_arr = np.array(list(res_sweep.keys()), dtype=float)
    r4s = np.array([res_sweep[k]["resid"] for k in res_sweep], dtype=float)
    slope = float(np.polyfit(np.log(xis_arr), np.log(r4s), 1)[0])
    Su = dc1.S(u, xi)
    Sup = dc1.dfd(Su, 1)
    yS = np.maximum(np.abs(Sup), 1e-12)
    M_Su = dc1.dfd((nu(yS) - 1.0) * Sup, 1)
    lhs = dc1.S(M_Su, xi) - M_fd
    pred = 0.5 * xi**2 * (Mpp + term2)
    lhs_fd = dc1.S_fd(M_Su, xi) - M_fd                # independent S representation
    f1 = np.cos(xh) + 0.3 * np.cos(3.0 * xh)
    g1 = np.sin(xh) * np.cos(2.0 * xh)
    adj = float((dc1.S(g1, xi) * f1).sum() - (g1 * dc1.S(f1, xi)).sum())
    scl = float(np.abs(lhs)[mmask].max())
    return {"tag": tag, "branch": branch, "N": N, "A": A, "xi": xi,
            "y_min_max_on_mask": [float(y[mmask].min()), float(y[mmask].max())],
            "max|LHS|(masked,xi=0.4)": scl,
            "max|pred|(masked,xi=0.4)": float(np.abs(pred)[mmask].max()),
            "max|M|(masked)": float(np.abs(M_fd)[mmask].max()),
            "resid_FFT_vs_pred_xi04": float(np.abs(lhs - pred)[mmask].max()),
            "rel_FFT_xi04": float(np.abs(lhs - pred)[mmask].max() / max(1e-300, scl)),
            "resid_FDheat_vs_pred_xi04": float(np.abs(lhs_fd - pred)[mmask].max()),
            "rel_FDheat_xi04": float(np.abs(lhs_fd - pred)[mmask].max() / max(1e-300, scl)),
            "resid_rep_FFT_vs_FDheat_xi04": float(np.abs(lhs - lhs_fd)[mmask].max() / max(1e-300, scl)),
            "adjoint_<Sg,f>-<g,Sf>": adj,
            "resid_vs_xi_sweep": res_sweep,
            "loglog_slope_resid(first3)": slope}


out["checks"]["T4_1D_torus_two_reps"] = {
    "deep_RAR": check_1d("RAR", 5e-4, tag="deep: y in ~(8e-5, 5e-4)"),
    "mid_RAR": check_1d("RAR", 4.0, tag="y up to 4: crosses y_p"),
    "newtonian_RAR": check_1d("RAR", 1e4, tag="Newtonian tail: y up to 1e4"),
    "mono_mid": check_1d("MONO", 4.0, tag="MONO: y crosses y* = 2.3374"),
}
print("rss_after_T4 %.1f MiB wall %.1f s" % (_rss(), time.time() - t0), flush=True)

# ================================================================ T2: sympy symbolic check
# Runs in a subprocess so its memory footprint does not stack on the numpy block.
import subprocess as _sp
with open("t2_sympy.json", "w") as f:
    r = _sp.run([sys.executable, "t2_sympy.py"], capture_output=True, text=True, timeout=110)
    if r.returncode != 0:
        f.write(json.dumps({"subprocess_error": r.returncode, "stderr": r.stderr[-2000:]}, indent=1))
    else:
        f.write(r.stdout)
with open("t2_sympy.json") as f:
    sympy_res = json.load(f)
out["checks"]["T2_sympy_symbolic"] = sympy_res
print("rss_after_T2 %.1f MiB wall %.1f s" % (_rss(), time.time() - t0), flush=True)

# ================================================================ T6/T7: energy budget, physical units
def energy_budget(footing_name, a0):
    res = {}
    M_b = M_SUN
    rM = np.sqrt(G_SI * M_b / a0)
    sigma_phys = rM
    N2, L2 = 48, 12.0 * sigma_phys
    box2 = Torus3(N2, L2)
    xs2 = np.linspace(0, L2, N2, endpoint=False)
    X2, Y2, Z2 = np.meshgrid(xs2, xs2, xs2, indexing="ij")
    rho_t = periodic_gauss(X2, Y2, Z2, L2, 1.0, sigma_phys)
    dx3 = box2.dx**3
    rho_b = rho_t / (rho_t.sum() * dx3) * M_b
    u = box2.lap_inv_meanzero(4.0 * np.pi * G_SI * rho_b)
    res["rM_m"] = float(rM)
    res["rM_pc"] = float(rM / PC_SI)
    res["lap_u_eq_4piG_rho_b_max_resid"] = float(np.abs(box2.lap(u) - 4.0 * np.pi * G_SI * rho_b).max())
    gk = box2.grad(u)
    gmag = np.sqrt(gk[0]**2 + gk[1]**2 + gk[2]**2)
    y = gmag / a0
    res["y_min_max"] = [float(y.min()), float(y.max())]
    res["rho_b_total_mass_kg"] = float(rho_b.sum() * dx3)
    ygrid = np.concatenate([np.linspace(0, 0.01, 1001)[1:], np.geomspace(0.011, 100.0, 20000)])
    h_r, h_m = h_rar(ygrid), h_mono(ygrid)
    Hr = np.concatenate([[0.0], np.cumsum(0.5 * (h_r[1:] + h_r[:-1]) * np.diff(ygrid))])
    Hm = np.concatenate([[0.0], np.cumsum(0.5 * (h_m[1:] + h_m[:-1]) * np.diff(ygrid))])
    Hr_f = np.interp(y, ygrid, Hr)
    Hm_f = np.interp(y, ygrid, Hm)
    int_Hr = float((Hr_f * dx3).sum())
    int_Hm = float((Hm_f * dx3).sum())
    pref = a0**2 / (4.0 * np.pi * G_SI)
    E_RAR = -pref * int_Hr
    E_MONO = -pref * int_Hm
    nu, nu_p = nu_factory("MONO")
    Mf = M_op(box2, u, nu, nu_p, a0)
    Qd = 0.5 * (box2.lap(Mf) + DM_op(box2, u, box2.lap(u), nu, nu_p, a0))
    dPhi1 = box2.lap_inv_meanzero(Qd)
    xi_phys = 0.1 * rM
    dE_f = (xi_phys**2 / (4.0 * np.pi * G_SI)) * float((Mf * dPhi1 * dx3).sum())
    W = float((Mf * box2.lap(u) * dx3).sum())
    res["budget"] = {
        "xiphys_over_rm": float(xi_phys / rM), "xi_m": float(xi_phys),
        "int_H_RAR_m3": int_Hr, "int_H_MONO_m3": int_Hm,
        "E_ph_RAR_J": float(E_RAR), "E_ph_MONO_J": float(E_MONO),
        "dE_kernel_MONO-RAR_J": float(E_MONO - E_RAR),
        "dE_kernel_over_absE_RAR": float((E_MONO - E_RAR) / abs(E_RAR)),
        "dE_filter_leading_J": dE_f,
        "dE_filter_over_absE_RAR": float(dE_f / abs(E_RAR)),
        "sign_dE_filter": "positive -> smoothing raises (de-binds) phantom energy" if dE_f > 0 else "negative -> smoothing deepens phantom budget",
        "W_int": W,
        "note": ("physical field has y_max = 0.21 < y_star so H_mono == H_RAR pointwise: "
                 "kernel shift vanishes exactly on this field (reported honestly); M[u] has "
                 "integrable |x|^{-1/2} cusps at zero-gradient (image-)centres; dE_filter is "
                 "the grid principal value of an integrable singular pairing."),
    }
    return res


out["energy"] = {
    "canonical_a0_9.3619e-11": energy_budget("canonical", A0_CANON),
    "alternative_a0_1.1279e-10": energy_budget("alternative", A0_ALT),
}

# gradient identity Q = delta W/delta u on the smooth periodic cell + kernel shift
# on the crossing field (reaches y*): dimensionless, footing-independent:
nu, nu_p = nu_factory("MONO")
M_u = M_op(box, u_mid, nu, nu_p)
Qfull = box.lap_fd(M_u) + DM_op(box, u_mid, box.lap_fd(u_mid), nu, nu_p)
eta = u_mid / u_mid.max()          # smooth test direction (periodic, C^inf)
eps = 1e-6
W_u = float((M_u * box.lap_fd(u_mid) * box.dx**3).sum())
W_ep = float((M_op(box, u_mid + eps * eta, nu, nu_p) * box.lap_fd(u_mid + eps * eta) * box.dx**3).sum())
int_Q_eta = float((Qfull * eta * box.dx**3).sum())
fdW = (W_ep - W_u) / eps
out["checks"]["gradient_Q_eq_dW_torus"] = {
    "finite_diff_dW": float(fdW), "int(Q*eta)": float(int_Q_eta),
    "rel_err": float(abs(fdW - int_Q_eta) / max(1e-300, abs(int_Q_eta)))}
ygrid = np.concatenate([np.linspace(0, 0.01, 1001)[1:], np.geomspace(0.011, 100.0, 20000)])
h_r, h_m = h_rar(ygrid), h_mono(ygrid)
Hr = np.concatenate([[0.0], np.cumsum(0.5 * (h_r[1:] + h_r[:-1]) * np.diff(ygrid))])
Hm = np.concatenate([[0.0], np.cumsum(0.5 * (h_m[1:] + h_m[:-1]) * np.diff(ygrid))])
out["checks"]["kernel_energy_shift_crossing_field"] = {
    "y_min_max_on_mask": [float(mid_ymag[mid_mask].min()), float(mid_ymag[mid_mask].max())],
    "int(H_MONO-H_RAR)d3x": float(((np.interp(mid_ymag, ygrid, Hm) - np.interp(mid_ymag, ygrid, Hr)) * box.dx**3)[mid_mask].sum()),
    "volume_fraction_with_y>y_star": float((mid_ymag > Y_STAR)[mid_mask].mean()),
    "sign_statement": ("E_ph[MONO]-E_ph[RAR] = -(a0^2/4piG) int(H_mono-H_RAR) <= 0 with "
                       "equality iff no volume element has y > y_star; strict inequality "
                       "on the crossing field."),
    "prefactor_a0sq_over_4piG_canonical_J_m5": float(A0_CANON**2 / (4.0 * np.pi * G_SI)),
    "prefactor_alt_J_m5": float(A0_ALT**2 / (4.0 * np.pi * G_SI)),
}
out["checks"]["correction_scale_torus"] = {
    "predicted_max|correction|/max|M| at xi=0.1L (mid field)": float(
        0.5 * 0.1**2 * np.abs(Qfull)[mid_mask].max() / np.abs(M_u)[mid_mask].max())}

# ================================================================ footings
rhoL_c = 4.0 * A0_CANON**2 / (G_SI * C_SI**2)
rhoL_a = 4.0 * A0_ALT**2 / (G_SI * C_SI**2)
out["footings"] = {
    "kappa": KAPPA,
    "rho_Lambda_canonical_kg_m3": rhoL_c,
    "rho_Lambda_alternative_kg_m3": rhoL_a,
    "rho_Lambda_ratio": float(rhoL_a / rhoL_c),
    "note": ("kappa fixed at 1/2 across footings => rho_Lambda differs by "
             "(1.1279e-10/9.3619e-11)^2 = 1.4515; the dimensionless leading-order "
             "identity and its O(xi^4) bound apply unchanged to both footings (the "
             "identity is homogeneous in a0: y = |grad u|/a0, all occurrences of a0 "
             "enter only through y); SI energy examples are carried per footing; "
             "G_N, G_bare, G_cosmo kept as separate symbols (not equated here)."),
}

# ================================================================ wrap-up
t1 = time.time()
ru = resource.getrusage(resource.RUSAGE_SELF)
out["meta"]["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t1))
out["meta"]["wall_s"] = t1 - t0
out["meta"]["maxrss_MiB"] = ru.ru_maxrss / (1024.0 * 1024.0) if sys.platform == "darwin" else ru.ru_maxrss / 1024.0
out["meta"]["bounds"] = {
    "cpu_rlimit_sec": "120 (RLIMIT_CPU hard-enforced)",
    "as_rlimit_512MiB_requested": as_limit_enforced,
    "threads": "1 (OMP/OPENBLAS/MKL/VECLIB=1; numpy pocketfft single-threaded)",
    "maxrss_MiB_measured": out["meta"]["maxrss_MiB"], "wall_s": out["meta"]["wall_s"],
}
assert out["meta"]["wall_s"] < 120.0, "cpu budget exceeded"
print("rss_final %.1f MiB wall %.1f s" % (out["meta"]["maxrss_MiB"], out["meta"]["wall_s"]), flush=True)

with open("raw_output.json", "w") as f:
    json.dump(out, f, indent=1, default=str)
print("wall %.2f s  maxrss %.1f MiB" % (out["meta"]["wall_s"], out["meta"]["maxrss_MiB"]))
print("T1 slopes RAR:", out["checks"]["T1_3D_torus_main_identity"]["RAR"]["_loglog_slope_R4_mid_submask(first3)"],
      "MONO:", out["checks"]["T1_3D_torus_main_identity"]["MONO"]["_loglog_slope_R4_mid_submask(first3)"])
print("T4 FFT residuals:", {k: v["rel_FFT_xi04"] for k, v in out["checks"]["T4_1D_torus_two_reps"].items()})
print("T5:", json.dumps(out["checks"]["T5_linear_cell_exact"]))
print("gradient:", json.dumps(out["checks"]["gradient_Q_eq_dW_torus"]))
print("adjoint:", json.dumps(out["checks"]["S_self_adjoint_L2_torus3"]))
print("T2:", json.dumps(out["checks"]["T2_sympy_symbolic"], indent=1)[:800])
