"""p40: (S) the 'capacity' self-consistency principle and (N) a look-elsewhere test of 'nice' turn-off numbers. Kernel nu_fix (k = 2), vacuum L(y_t) = Lambda c^4/a0^2 (p35).
(S) Principle: the MOND field's extra energy density u = (g^2 - g_N^2)/(8 pi G) = a0 g_N/(8 pi G) saturates when it reaches the vacuum energy density rho_Lambda c^2,
    i.e. y_t = s * L with s a shape factor of order 1. Combined with the vacuum condition L = L(y_t) ~ (pi/4) y_t: does this fix L, or only s?
(N) If y_t is a 'nice' pure number N, the model predicts L = L(N) and a0 = 9.3603e-11 sqrt(32 pi / L(N)). Menu of 20 simple numbers in [30, 400] (declared here);
    which land within 1 sigma of the measured a0 (lane V ensemble 1.097e-10 +- 12%)? A menu where many hit means no single hit is evidence.
Run: python3 p40_selfconsistency_and_nice_numbers.py  |  MUTATE=1: the ensemble error set to 1% (check N must fail: few hits)
"""
import os, sys, math
from scipy.integrate import quad
from scipy.optimize import brentq
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
pi = math.pi
def L(yt):
    segs = [(1e-9, 1e-3), (1e-3, 1), (1, 10), (10, 1e2), (1e2, 1e3), (1e3, 1e5), (1e5, 1e7)]
    f = lambda y: 2 * y * math.expm1(0.5 * math.log1p(1 / y)) / (1 + (y / yt)**2)
    return 0.5 * sum(quad(f, s, e, limit=4000, epsabs=1e-10, epsrel=1e-10)[0] for s, e in segs)
# (S): for each s, solve L(y_t) = y_t / s  (y_t = s L)
print("   (S) capacity principle y_t = s L combined with the vacuum condition:")
sols = {}
for s in (1.0, 1.2, 4 / pi, 1.4, 2.0):
    g = lambda yt: L(yt) - yt / s
    try:
        r = brentq(g, 1.0, 1e5); sols[s] = (r, L(r))
        print(f"     s = {s:.4f}: y_t = {r:9.2f}, L = {L(r):9.2f}")
    except ValueError:
        sols[s] = None; print(f"     s = {s:.4f}: no positive solution in [1, 1e5]")
vals = [v[1] for v in sols.values() if v]
check("S the capacity principle does not fix L: the solution moves by orders of magnitude with the O(1) shape factor s (or does not exist)", (len(vals) < 2) or (max(vals) / min(vals) > 3))
# (N)
menu = {"10pi": 10 * pi, "32": 32, "12pi": 12 * pi, "4pi^2": 4 * pi**2, "16pi": 16 * pi, "50": 50, "64": 64, "20pi": 20 * pi, "8pi^2": 8 * pi**2, "25pi": 25 * pi,
        "100": 100, "32pi": 32 * pi, "36pi": 36 * pi, "128": 128, "(4pi)^2": (4 * pi)**2, "50pi": 50 * pi, "16pi^2": 16 * pi**2, "64pi": 64 * pi, "256": 256, "100pi": 100 * pi}
amean, aerr = 1.097e-10, (0.01 if MUTATE else 0.122)
hits = []
print("   (N) y_t = N  ->  L(N), predicted a0, pull vs the measured ensemble:")
for k, N in menu.items():
    LN = L(N); a = 9.3603e-11 * math.sqrt(32 * pi / LN); pull = math.log(a / amean) / aerr
    if abs(pull) < 1: hits.append(k)
    print(f"     {k:8s} N = {N:7.2f}  L = {LN:7.2f}  a0 = {a:.3e}  pull {pull:+.2f}")
print(f"   within 1 sigma: {len(hits)} of {len(menu)}: {hits}")
check(f"N many 'nice' numbers fit equally well ({len(hits)}/20 within 1 sigma): a turn-off at 32 pi (or any single value) is not evidence", len(hits) >= 4)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
