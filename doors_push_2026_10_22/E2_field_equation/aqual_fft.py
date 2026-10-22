"""Route B: 3-D nonlinear AQUAL (and QUMOND) for point masses in a uniform external field, FFT longitudinal
projection on D2's grid (lane E2_field_equation).

Physical accelerations. AQUAL: div[mu(|g|) g] = div g_N, g curl-free, g -> x_e e at infinity.
Write g = x_e e + g_int + delta,  delta = P_L[ (1 - mu(|g|)) g - (1 - mu_e) x_e e ]   (fixed point; P_L = curl-free part).
QUMOND (D2):  delta = P_L[ (nu(|g_N|) - 1) g_N - (nu_e - 1) y_e e ],  g_N = y_e e + g_int   (one projection).
Units a0 = 1, separation s = 1 (binary) as in D2 `qumond_fft.py`; the grid/star placement is D2's.
"""
import numpy as np
import scipy.fft as sfft


def omm(x):                     # 1 - mu for the canonical law (simple mu)
    return 1.0 / (1.0 + x)


def nu(y):
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / y))


def grid(N, m):
    dx = 1.0 / (2 * m + 1)
    xs = (np.arange(N) - N // 2 + 0.5) * dx
    zs = (np.arange(N) - N // 2) * dx
    return dx, xs, zs


class FFT3:
    def __init__(self, N, dx):
        self.N = N
        k = (2 * np.pi * sfft.fftfreq(N, dx)).astype(np.float32)
        kz = (2 * np.pi * sfft.rfftfreq(N, dx)).astype(np.float32)
        self.k = (k[:, None, None], k[None, :, None], kz[None, None, :])
        k2 = self.k[0] ** 2 + self.k[1] ** 2 + self.k[2] ** 2
        k2[0, 0, 0] = 1.0
        self.ik2 = (1.0 / k2).astype(np.float32)

    def project(self, S, out):
        """out[c] = longitudinal part of S (3 comps), zero mean."""
        D = sfft.rfftn(S[0], workers=1) * self.k[0]
        D += sfft.rfftn(S[1], workers=1) * self.k[1]
        D += sfft.rfftn(S[2], workers=1) * self.k[2]
        D *= self.ik2
        D[0, 0, 0] = 0.0
        for c in range(3):
            out[c] = sfft.irfftn(D * self.k[c], s=(self.N,) * 3, workers=1)

    def linear_aqual(self, S, mu_e, L0, e, out):
        """solve div[mu_e (I + L0 e e) delta] = div S_N  ->  delta_hat = k (k.S)/(mu_e (k^2 + L0 (k.e)^2))."""
        Sh = [sfft.rfftn(S[c], workers=1) for c in range(3)]
        kS = Sh[0] * self.k[0] + Sh[1] * self.k[1] + Sh[2] * self.k[2]
        ke = self.k[0] * e[0] + self.k[1] * e[1] + self.k[2] * e[2]
        k2 = self.k[0] ** 2 + self.k[1] ** 2 + self.k[2] ** 2
        den = mu_e * (k2 + L0 * ke ** 2)
        den[0, 0, 0] = 1.0
        D = kS / den
        D[0, 0, 0] = 0.0
        for c in range(3):
            out[c] = sfft.irfftn(D * self.k[c], s=(self.N,) * 3, workers=1)


def internal_field(N, m, masses):
    """masses: list of (GM, (x0,y0,z0)); returns float32 (3,N,N,N) Newtonian internal field."""
    dx, xs, zs = grid(N, m)
    G = np.zeros((3, N, N, N), dtype=np.float32)
    X = xs[:, None]
    Y = xs[None, :]
    for kk in range(N):
        z = zs[kk]
        gx = np.zeros((N, N)); gy = np.zeros((N, N)); gz = np.zeros((N, N))
        for GM, (x0, y0, z0) in masses:
            ddx = X - x0; ddy = Y - y0; ddz = z - z0
            r2 = ddx * ddx + ddy * ddy + ddz * ddz
            r3 = r2 * np.sqrt(r2)
            gx += -GM * ddx / r3; gy += -GM * ddy / r3; gz += -GM * ddz / r3
        G[0, :, :, kk] = gx; G[1, :, :, kk] = gy; G[2, :, :, kk] = gz
    return G


def solve(N, m, masses, x_e, e, mode="AQUAL", maxit=200, tol=1e-7, probe=None, omega=1.0, verbose=False):
    """Return (delta (3,N,N,N) float32, info). probe(delta) -> scalar monitored for convergence."""
    dx, xs, zs = grid(N, m)
    ft = FFT3(N, dx)
    Gi = internal_field(N, m, masses)
    e = np.asarray(e, float)
    delta = np.zeros_like(Gi)
    S = np.empty_like(Gi)
    y_e = x_e * x_e / (1.0 + x_e)
    if mode == "QUMOND":
        nue = nu(y_e)
        for kk in range(N):
            tx = Gi[0, :, :, kk] + y_e * e[0]; ty = Gi[1, :, :, kk] + y_e * e[1]; tz = Gi[2, :, :, kk] + y_e * e[2]
            mag = np.sqrt(tx * tx + ty * ty + tz * tz)
            f = nu(mag) - 1.0
            S[0, :, :, kk] = f * tx - (nue - 1) * y_e * e[0]
            S[1, :, :, kk] = f * ty - (nue - 1) * y_e * e[1]
            S[2, :, :, kk] = f * tz - (nue - 1) * y_e * e[2]
        ft.project(S, delta)
        return delta, dict(iters=1, rel=0.0, hist=[probe(delta)] if probe else [])
    ome = omm(x_e)
    hist = []
    prev = None
    for it in range(maxit):
        for kk in range(N):
            tx = Gi[0, :, :, kk] + x_e * e[0] + delta[0, :, :, kk]
            ty = Gi[1, :, :, kk] + x_e * e[1] + delta[1, :, :, kk]
            tz = Gi[2, :, :, kk] + x_e * e[2] + delta[2, :, :, kk]
            mag = np.sqrt(tx * tx + ty * ty + tz * tz)
            f = omm(mag)
            S[0, :, :, kk] = f * tx - ome * x_e * e[0]
            S[1, :, :, kk] = f * ty - ome * x_e * e[1]
            S[2, :, :, kk] = f * tz - ome * x_e * e[2]
        ft.project(S, S)                         # projection reads S fully before writing (saves one array)
        if omega == 1.0:
            delta, S = S, delta
        else:
            delta += omega * (S - delta)
        val = probe(delta) if probe else float(np.max(np.abs(delta)))
        hist.append(val)
        if verbose:
            print(it, val)
        if prev is not None and abs(val - prev) <= tol * max(abs(val), 1e-30):
            break
        prev = val
    rel = abs(hist[-1] - hist[-2]) / max(abs(hist[-1]), 1e-30) if len(hist) > 1 else np.nan
    return delta, dict(iters=it + 1, rel=rel, hist=hist)


def binary_probe(N, m, y_tot):
    ix = [N // 2 - 1, N // 2]
    kup = [N // 2 + m, N // 2 + m + 1]
    kdn = [N // 2 - m - 1, N // 2 - m]

    def probe(delta):
        up = np.mean(delta[2][np.ix_(ix, ix, kup)])
        dn = np.mean(delta[2][np.ix_(ix, ix, kdn)])
        return float(1.0 + (dn - up) / y_tot)          # a_rel / a_N along the separation
    return probe


def binary_arel(y_tot, x_e, theta, N=192, m=8, mode="AQUAL", **kw):
    masses = [(0.5 * y_tot, (0.0, 0.0, -0.5)), (0.5 * y_tot, (0.0, 0.0, 0.5))]
    e = (np.sin(theta), 0.0, np.cos(theta))
    probe = binary_probe(N, m, y_tot)
    delta, info = solve(N, m, masses, x_e, e, mode=mode, probe=probe, **kw)
    return info["hist"][-1], info


GL3_MU = np.array([0.1127016653792583, 0.5, 0.8872983346207417])
GL3_W = np.array([5.0, 8.0, 5.0]) / 18.0


def gamma_v_avg(y_tot, x_e, N=192, m=8, mode="AQUAL", **kw):
    vals, infos = [], []
    for mu in GL3_MU:
        a, info = binary_arel(y_tot, x_e, float(np.arccos(mu)), N=N, m=m, mode=mode, **kw)
        vals.append(a); infos.append(info)
    a = float(np.sum(GL3_W * np.array(vals)))
    return float(np.sqrt(a)), vals, infos


# ----------------------------------------------------------------------------- isolated-process tasks
# Each heavy 3-D job runs in a fresh single-threaded child process so that the peak RSS of the run stays
# below the lane's 2 GB budget (the parent's freed Route A memory is not returned to the OS on macOS).
def _rss_mb():
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6


def task(kind, kw):
    if kind == "k6":
        x18 = kw["x"]
        N, m = kw["N"], kw["m"]
        dx, _, _ = grid(N, m)
        ft = FFT3(N, dx)
        Gi = internal_field(N, m, [(0.5, (0.0, 0.0, -0.5)), (0.5, (0.0, 0.0, 0.5))])
        mu_e = x18 / (1 + x18)
        L0 = 1.0 / (1 + x18)
        probe = binary_probe(N, m, 1.0)
        outP = np.empty_like(Gi)
        ft.project(Gi, outP)
        outL = np.empty_like(Gi)
        res = []
        for th in (0.0, np.pi / 2):
            e = (np.sin(th), 0.0, np.cos(th))
            ft.linear_aqual(Gi, mu_e, L0, e, outL)
            res.append(probe(outL - outP))
        return dict(B=res, mu_e=mu_e, L0=L0, rss=_rss_mb())
    if kind == "k7":
        from scipy.interpolate import RegularGridInterpolator
        N, m = kw["N"], kw["m"]
        delta, info = solve(N, m, [(1.0, (0.0, 0.0, 0.5))], kw["x_e"], (0.0, 0.0, -1.0), mode=kw["mode"],
                            maxit=300, tol=1e-9)
        dx, xs, zs = grid(N, m)
        out = []
        for P in kw["points"]:
            out.append([float(RegularGridInterpolator((xs, xs, zs), delta[c].astype(float))([P])[0]) for c in range(3)])
        return dict(vals=out, iters=info["iters"], rss=_rss_mb())
    if kind == "arel":
        a, info = binary_arel(kw["y_tot"], kw["x_e"], kw["theta"], N=kw["N"], m=kw["m"], mode=kw["mode"],
                              **kw.get("extra", {}))
        return dict(a=a, iters=info["iters"], rel=info["rel"], rss=_rss_mb())
    raise ValueError(kind)


def run_isolated(kind, kw):
    import json
    import os
    import subprocess
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    code = ("import sys, json; sys.path.insert(0, %r); import aqual_fft as B; "
            "print('@@' + json.dumps(B.task(sys.argv[1], json.loads(sys.argv[2]))))" % here)
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    out = subprocess.run([sys.executable, "-c", code, kind, json.dumps(kw)], capture_output=True, text=True, env=env,
                         check=True).stdout
    return json.loads([ln for ln in out.splitlines() if ln.startswith("@@")][-1][2:])


def gamma_v_avg_isolated(y_tot, x_e, N, m, mode, extra=None):
    vals, infos = [], []
    for mu in GL3_MU:
        r = run_isolated("arel", dict(y_tot=y_tot, x_e=x_e, theta=float(np.arccos(mu)), N=N, m=m, mode=mode,
                                      extra=extra or {}))
        vals.append(r["a"]); infos.append(r)
    return float(np.sqrt(np.sum(GL3_W * np.array(vals)))), vals, infos
