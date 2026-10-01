#!/usr/bin/env python3
# AS206 -- supplementary grid scan: fit-intercept residual of the metric-variation identity
# for the 3D curved-leaf general-k case at N = 32, 48, 64 (same field construction, seed
# 20260928). Documents the spectral reconstruction error of the non-band-limited
# intermediates (hinv = h^-1, sqrt(det h)): the identity itself is exact; the residual is
# a grid artifact that shrinks with N. Separate process so its 64^3 peak stays bounded.
import numpy as np
import sys

rng = np.random.default_rng(20260928)

def trig_field(rng, shape, modes=(1, 2), amp=1.0):
    g = np.zeros(shape, dtype=float)
    for _ in range(6):
        m = rng.integers(modes[0], modes[1] + 1, size=len(shape))
        ph = rng.uniform(0, 2 * np.pi)
        fr = rng.uniform(0.3, 1.0) * amp
        cs = rng.choice([-1, 1], size=1)[0]
        x = np.meshgrid(*[np.arange(n) * 2 * np.pi / n for n in shape], indexing='ij')
        arg = sum(m[k] * x[k] for k in range(len(shape))) + ph
        g += cs * fr * np.cos(arg)
    return g

def grad_spectral(f):
    sh = f.shape; nd = len(sh)
    F = np.fft.rfftn(f)
    out = []
    for d in range(nd):
        k = np.fft.fftfreq(sh[d]) * sh[d]
        K = np.zeros(F.shape)
        sl = [slice(None)] * nd
        sl[d] = slice(0, F.shape[d])
        K[tuple(sl)] = k[:F.shape[d]].reshape([1 if i != d else -1 for i in range(nd)])
        out.append(np.fft.irfftn(1j * K * F, s=sh))
    return out

def hinv_of(h):
    return np.moveaxis(np.linalg.inv(np.moveaxis(h, (0, 1), (-2, -1))), (-2, -1), (0, 1))

def det_of(h):
    return np.linalg.det(np.moveaxis(h, (0, 1), (-2, -1)))

def lap_spec(h, u, deriv):
    nd = u.ndim
    sdet = np.sqrt(det_of(h))
    Hi = hinv_of(h)
    Gu = [deriv(u, d) for d in range(nd)]
    W = [np.zeros_like(u) for _ in range(nd)]
    for i in range(nd):
        for j in range(nd):
            W[i] += sdet * Hi[i, j] * Gu[j]
    S = np.zeros_like(u)
    for i in range(nd):
        S += deriv(W[i], i)
    return S / sdet

def christoffel_num(h, deriv, nd):
    Gam = {}
    hinv = hinv_of(h)
    dh = [[[deriv(h[a, bb], d) for d in range(nd)] for bb in range(nd)] for a in range(nd)]
    for i in range(nd):
        for j in range(nd):
            for l in range(nd):
                s = np.zeros_like(h[0, 0])
                for m in range(nd):
                    s += hinv[l, m] * (dh[m][j][i] + dh[i][m][j] - dh[i][j][m])
                Gam[(i, j, l)] = 0.5 * s
    return Gam

def lap_curved_formula(h, k, u, deriv):
    nd = u.ndim
    hinv = hinv_of(h)
    khat = np.einsum('ia...,ab...,bj...->ij...', hinv, k, hinv)
    T = np.einsum('ij...,ij...->...', hinv, k)
    Gam = christoffel_num(h, deriv, nd)
    Gu = [deriv(u, d) for d in range(nd)]
    GGu = np.zeros((nd, nd) + u.shape)
    for i in range(nd):
        for j in range(nd):
            GGu[i, j] = deriv(Gu[i], j)
            for l in range(nd):
                GGu[i, j] -= Gam[(i, j, l)] * Gu[l]
    term1 = np.zeros_like(u)
    for i in range(nd):
        for j in range(nd):
            term1 += khat[i, j] * GGu[i, j]
    out = -term1
    for j in range(nd):
        DKj = np.zeros_like(u)
        for i in range(nd):
            DKj += deriv(khat[i, j], i)
            for l in range(nd):
                DKj += Gam[(i, l, j)] * khat[i, l]
                DKj += Gam[(i, l, i)] * khat[l, j]
        DTj = np.zeros_like(u)
        for m in range(nd):
            DTj += hinv[j, m] * deriv(T, m)
        out -= (DKj - 0.5 * DTj) * Gu[j]
    return out

eps_vals = np.array([1e-4, 1e-5, 1e-6])
def intercept(R):
    R = np.array(R)
    Rt = R.reshape(3, -1)
    X = np.column_stack([np.ones_like(eps_vals), eps_vals])
    c, *_ = np.linalg.lstsq(X, Rt, rcond=None)
    return c[0].reshape(R.shape[1:])

def run(NN):
    nn = (NN, NN, NN)
    r2 = np.random.default_rng(20260928)
    tf = lambda shape: trig_field(r2, shape)
    uu = tf(nn)
    hh = np.zeros((3, 3) + nn)
    for i in range(3):
        hh[i, i] = 1.0 + 0.1 * tf(nn)
    hh[0, 1] = hh[1, 0] = 0.08 * tf(nn); hh[0, 2] = hh[2, 0] = 0.08 * tf(nn); hh[1, 2] = hh[2, 1] = 0.08 * tf(nn)
    kk = np.zeros((3, 3) + nn)
    for i in range(3):
        kk[i, i] = 0.3 * tf(nn)
    kk[0, 1] = kk[1, 0] = 0.3 * tf(nn); kk[0, 2] = kk[2, 0] = 0.3 * tf(nn); kk[1, 2] = kk[2, 1] = 0.3 * tf(nn)
    dv = lambda f, d: grad_spectral(f)[d]
    d0 = lap_spec(hh, uu, dv)
    rr = lap_curved_formula(hh, kk, uu, dv)
    R = [(lap_spec(hh + ep * kk, uu, dv) - d0) / ep for ep in eps_vals]
    a = intercept(R)
    rel = np.max(np.abs(a - rr)) / max(np.max(np.abs(rr)), 1e-30)
    print(f'N={NN}: fit-intercept relative residual = {rel:.3e}')
    return rel

if __name__ == '__main__':
    for N in (32, 48, 64):
        run(N)
        import gc
        gc.collect()
    print('SCAN DONE')
    sys.exit(0)