import math
from math import comb, factorial
import numpy as np
def gam(s):
    g0 = math.sqrt(sum(comb(s - 1, t - 1) / t ** 2 for t in range(1, s + 1)))
    gS2 = max((n + s) ** 2 * sum(comb(s, t) / (n + t) ** 2 for t in range(s + 1)) for n in range(1, 200))
    return g0, math.sqrt(gS2)
def beta(s):
    g0, gS = gam(s)
    return [g0] + [2 ** k * (g0 * s ** k + k * gS * s ** (k - 1)) for k in range(1, 2 * s + 1)]
for s in (2,3,4):
    b = beta(s)
    q = lambda mu: b[0] + sum(b[k] * mu ** k / factorial(k) for k in range(1, 2 * s + 1))
    qp = lambda mu: sum(b[k] * mu ** (k - 1) / factorial(k - 1) for k in range(1, 2 * s + 1))
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        (lo, hi) = (mid, hi) if q(mid) - 2 * mid * qp(mid) > 0 else (lo, mid)
    lam_c = lo / q(lo)
    for fac in (1-1e-9, 1.0+1e-3, 1.2):
        lam = lam_c*fac
        P = 3000
        a = np.zeros(P+1); a[1] = b[0]*lam
        for pp in range(2, P+1):
            ser = a[:pp].copy(); ser[0]=0
            pw = np.zeros(pp); pw[0]=1.0; tot=0.0
            for k in range(1, 2*s+1):
                pw = np.convolve(pw, ser)[:pp]
                tot += b[k]/factorial(k)*pw[pp-1]
            a[pp] = lam*tot
        S = a.sum()
        print(f"s={s} lam/lam_c={fac:.6f}: ||C||_1 majorant sum = {S:.6e} (mu_c={lo:.6e}); last terms {a[-1]:.2e}; 2 lam q'(sum) = {2*lam*qp(S):.6f}")
