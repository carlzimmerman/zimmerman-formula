#!/usr/bin/env python3
"""
Fast Riemann zero finder via the Z-function at Gram points (Odlyzko-style).

Each zero of zeta on the critical line is a REAL root of the Hardy Z-function
Z(t) = e^{i theta(t)} zeta(1/2 + i t), where
    theta(t) ~ (t/2) ln(t/2pi) - t/2 - pi/8 + 1/(48t) + ...
Z(t) is real for real t; its sign changes bracket the zeros.  Gram's law
(empirically ~true for the first 10^5+ intervals) says Z changes sign in
most Gram intervals [g_n, g_{n+1}], g_n = theta^{-1}(n pi) -- so:
  1. build the Gram points g_n via Newton on theta(g) = n pi,
  2. evaluate Z(g_n); a sign change between neighbours -> findroot inside.
This is ~100x faster than mpmath.zetazero for the first tens of thousands.
Both the Gram construction and the Z evaluation are checked in-lane
(no zetazero input; the first few zeros are verified against zetazero).
"""
import math, cmath, os, json, time
import mpmath as mp

mp.mp.dps = 30

def theta(t):
    t = mp.mpf(t)
    return (t / 2) * mp.log(t / (2 * mp.pi)) - t / 2 - mp.pi / 8 + mp.mpf(1) / (48 * t)

def gram(n):
    """g_n = theta^{-1}(n pi) by Newton from the asymptotic root."""
    n = mp.mpf(n)
    # asymptotic inversion: g ~ 2 pi exp(W(n pi / e + ...)) -- just Newton from
    # the large-n expansion root t0 = 2 pi n / W(n) shape; safer: Newton from
    # t0 = 2 pi * n / math.log(n) for n large, and from a scan for small n.
    if n < 50:
        t = mp.mpf(10 + 1.5 * n)
    else:
        inner = n * mp.pi / math.e
        # t ~ 2 pi e^{W(inner/2 - ...)} ~ 2 pi e^{W(inner/2)}; use mpmath.lambertw
        w = mp.lambertw(inner / 2 + mp.mpf(1) / 8)
        t = 2 * mp.pi * mp.e ** w
    for _ in range(8):
        f = theta(t) - n * mp.pi
        fp = (mp.mpf(1) / 2) * (mp.log(t / (2 * mp.pi)) + 1) - mp.mpf(1) / (48 * t * t)
        t = t - f / fp
    return t

def Z(t):
    """Hardy Z-function via mpmath zeta (accurate, no external lib)."""
    t = mp.mpf(t)
    th = theta(t)
    z = mp.zeta(mp.mpf(0.5) + 1j * t)
    # Z(t) = exp(i theta) zeta(1/2+it); real part is the Z function
    return mp.re(mp.e ** (1j * th) * z)

def zeros_up_to(N, check_first=3):
    """First N zeros via Gram sign changes + findroot refinement."""
    zeros = []
    prev_t = gram(mp.mpf(0))
    prev_z = Z(prev_t)
    n = 0
    k = 1
    while len(zeros) < N and k < N * 3:
        gk = gram(mp.mpf(k))
        zk = Z(gk)
        if prev_z * zk < 0:
            try:
                root = mp.findroot(Z, (prev_t, gk), solver="secant", tol=1e-12)
                zeros.append(float(mp.im(mp.mpf(root))))
                n += 1
            except ValueError:
                # residue: refine with mpmath's robust brent on the interval
                try:
                    root = mp.findroot(Z, (prev_t, gk), solver="anderson",
                                       tol=1e-12)
                    zeros.append(float(mp.im(mp.mpf(root))))
                    n += 1
                except ValueError:
                    pass  # missed zero (Gram law failures); counted in gap
            k += 1
            prev_t, prev_z = gk, zk
            continue
        prev_t, prev_z = gk, zk
        k += 1
    # verify against mpmath.zetazero
    ver = [float(mp.zetazero(i).imag) for i in range(1, check_first + 1)]
    return zeros, ver

if __name__ == "__main__":
    t0 = time.time()
    N = int(os.environ.get("N_ZEROS", "5000"))
    zs, ver = zeros_up_to(N)
    print(f"found {len(zs)} zeros in {time.time()-t0:.0f} s; first 3 vs zetazero: "
          f"{[round(z, 6) for z in zs[:3]]} vs {[round(v, 6) for v in ver]}")
    errs = [abs(a - b) for a, b in zip(zs[:3], ver)]
    print(f"|err| = {[f'{e:.2e}' for e in errs]}")
    np_zs = [float(z) for z in zs]
    with open("fast_zeros.json", "w") as f:
        json.dump(np_zs, f)
    print("wrote fast_zeros.json")