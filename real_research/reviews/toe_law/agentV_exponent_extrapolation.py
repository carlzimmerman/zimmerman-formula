#!/usr/bin/env python3
"""
agentV addendum — (1) deep-t Richardson extrapolation of the forward exponent
(exact-target member p=-9/8, phi=-pi/8): local slopes converge to sqrt(2)*zeta
with t^(1/4) subleading corrections — extrapolate and report digits.
(2) the TWO-CONDITION sharpening of the legality theorem:
x(x-2) - 2(x-2) = (x-2)^2 exactly => flatness conditions k=0 AND k=1 alone force
int (x-2)^2 d rho = 0 => rho = delta at the conformal point. LP echo with
epsilon-relaxed conditions: cost ~ 1/epsilon.
Output: agentV_exponent_extrapolation.out (incremental)
"""
import sympy as sp
import mpmath as mp
import numpy as np
import os, time

OUTPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agentV_exponent_extrapolation.out")
_f = open(OUTPATH, "w")
T0 = time.time()
def P(s=""):
    _f.write(str(s) + "\n"); _f.flush()
    print(s, flush=True)

P("agentV addendum: exponent extrapolation + two-condition sharpening")
P("=" * 70)

# ---------- (1) deep-t forward transform, exact-target member, dps=80
mp.mp.dps = 80
z = mp.mpf(1)
p = mp.mpf('-1.125')   # -9/8
phi = -mp.pi/8
pw = -4*p - 3          # = 3/2
def Ffwd(t):
    return 4*mp.quad(lambda w: w**pw*mp.e**(-z*w)*mp.cos(z*w + phi)/mp.sqrt(1 + t*w**4),
                     [0, 3, 12, 40, 120, 400, mp.inf])
ks = list(range(2, 17))                      # t = 10^(-1) .. 10^(-8)
ts = [mp.mpf(10)**(-mp.mpf(k)/2) for k in ks]
P("[X1] computing F(t) for t = 1e-1 .. 1e-8 at dps=80 (exact-target member, zeta=1):")
Fs = []
for t in ts:
    Fs.append(Ffwd(t))
P("[X1] F(1e-8) = %s ; sign set = %s" %
  (mp.nstr(Fs[-1], 8), sorted(set(int(mp.sign(F)) for F in Fs))))
# local slopes and their midpoint t
locs, tmids = [], []
for i in range(len(ts)-1):
    num = mp.log(abs(Fs[i+1])) - mp.log(abs(Fs[i]))
    den = -(ts[i+1]**(mp.mpf(-1)/4) - ts[i]**(mp.mpf(-1)/4))
    locs.append(float(num/den))
    tmids.append(float(mp.sqrt(ts[i]*ts[i+1])))
P("[X1] local exponent sequence: %s" % ", ".join("%.6f" % v for v in locs))
# Richardson: fit s_i = c_inf - A * tmid^(1/4) on the last n points, n = 6..10
for n in [6, 8, 10]:
    A = np.array([[1.0, -tm**0.25] for tm in tmids[-n:]])
    yv = np.array(locs[-n:])
    coef, _, _, _ = np.linalg.lstsq(A, yv, rcond=None)
    P("[X1] t^(1/4)-extrapolation over last %2d slopes: c_inf = %.6f  (sqrt(2) = %.6f; ratio %.6f)" %
      (n, coef[0], float(mp.sqrt(2)), coef[0]/float(mp.sqrt(2))))
# global 4-param fit: ln|F| = lnA + q ln t - c t^(-1/4) + b t^(1/4)  (subleading term included)
Amat = np.array([[1.0, float(mp.log(t)), -float(t**(mp.mpf(-1)/4)), float(t**(mp.mpf(1)/4))] for t in ts])
yv = np.array([float(mp.log(abs(F))) for F in Fs])
coef, _, _, _ = np.linalg.lstsq(Amat, yv, rcond=None)
resid = float(np.max(np.abs(Amat@coef - yv)))
P("[X1] 4-param fit (with t^1/4 subleading): c = %.6f (sqrt2: ratio %.6f), q = %.4f (target -0.5000), max resid %.1e"
  % (coef[2], coef[2]/float(mp.sqrt(2)), coef[1], resid))
P("[X1] done (%.0fs)" % (time.time()-T0))

# ---------- (2) two-condition sharpening
P("\n[X2] TWO-CONDITION SHARPENING (sympy + LP echo)")
x = sp.symbols('x', positive=True)
P("[X2] identity: x*(x-2) - 2*(x-2) = (x-2)^2: %s" % (sp.expand(x*(x-2) - 2*(x-2) - (x-2)**2) == 0))
P("[X2] => flatness conditions k=0 (int (x-2)drho = 0) and k=1 (int x(x-2)drho = 0) alone imply")
P("    int (x-2)^2 drho = 0 => rho = delta at x=2 (conformal point, ZERO tail).")
P("    The legality kill needs only the FIRST TWO vanishing power corrections at high a, not the full tower.")
try:
    from scipy.optimize import linprog
    xs = np.linspace(0.05, 40.0, 500)
    nf = xs - 2.0
    r0 = nf/np.max(np.abs(nf))
    r1 = nf*xs/np.max(np.abs(nf*xs))
    norm_row = np.where(xs > 2.0, nf, 0.0)
    P("[X2] epsilon-relaxed LP (|condition_k| <= eps, k=0,1; unit positive part; min total mass):")
    for eps in [1e-1, 1e-2, 1e-3, 1e-4]:
        A_ub = np.vstack([r0, -r0, r1, -r1])
        b_ub = np.array([eps]*4)
        res = linprog(c=np.ones_like(xs), A_ub=A_ub, b_ub=b_ub,
                      A_eq=norm_row.reshape(1, -1), b_eq=[1.0],
                      bounds=[(0, None)]*len(xs), method='highs')
        P("[X2] eps=%.0e: min total mass = %s" %
          (eps, ("%.4e" % res.fun) if res.status == 0 else "INFEASIBLE"))
    P("[X2] (mass diverging as eps -> 0: approximate flatness is unboundedly costly for positive measures)")
except Exception as ex:
    P("[X2] scipy LP unavailable (%s); the identity above carries the result." % ex)

P("\nDONE in %.0fs." % (time.time()-T0))
_f.close()
