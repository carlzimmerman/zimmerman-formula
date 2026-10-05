"""p22: minimal BIMOND (f = 1) with a tail-sharpened kernel: which tail gives Lambda = 32 pi a0^2 (I_nu = 64 pi)?
Family F1 (contains the framework at alpha = 1, deep-MOND limit kept for every alpha): nu_a(y) = (1 + y^-a)^(1/(2a)); tail nu - 1 ~ y^-a/(2a).
Family F2 (Milgrom's nu_n; n = 1 is 'simple'): nu_n(y) = [(1 + sqrt(1 + 4 y^-n))/2]^(1/n); tail nu - 1 ~ y^-n/n.
I_nu = int_0^inf 2y (nu - 1) dy is finite iff the tail exponent > 2 (planets need >~ 1.5, Sereno & Jetzer 2006; SPARC cannot tell the tails apart,
mi_alpha1_solar_system_2026: <= 0.0084 dex). Lambda/a0^2 = I_nu/2 (p21, Milgrom 2009 eq 24 with f = 1).
Run: python3 p22_bimond_tail_alpha.py  |  MUTATE=1: F1's analytic tail coefficient doubled (check T must fail). (A first control that only changed the target could not fail; replaced.)
"""
import os, sys, math
from scipy.integrate import quad
from scipy.optimize import brentq
MUTATE = os.environ.get("MUTATE") == "1"
T = 64 * math.pi
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
F1 = lambda a: (lambda y: (1 + y**(-a))**(1 / (2 * a)))
F2 = lambda n: (lambda y: ((1 + math.sqrt(1 + 4 * y**(-n))) / 2)**(1 / n))
# nu - 1 without cancellation (1 + 1e-18 rounds to 1 in floating point; the first brute-force check lost the 1e6-1e7 decade to it)
N1 = lambda a: (lambda y: math.expm1(math.log1p(y**(-a)) / (2 * a)))
N2 = lambda n: (lambda y: math.expm1(math.log1p(2 * y**(-n) / (1 + math.sqrt(1 + 4 * y**(-n)))) / n))
Y = 1e4
def I(nm1, p, A):
    """numeric to Y, then the exact leading tail: nu - 1 = A y^-p + O(y^-2p)  ->  int_Y^inf 2y A y^-p dy = 2A Y^(2-p)/(p-2); next order ~ Y^(2-2p) < 1e-7"""
    g = lambda y: 2 * y * nm1(y)
    segs = ((0, 1), (1, 10), (10, 1e2), (1e2, 1e3), (1e3, Y))
    return sum(quad(g, a, b, limit=2000, epsabs=1e-13, epsrel=1e-12)[0] for a, b in segs) + 2 * A * Y**(2 - p) / (p - 2)
I1 = lambda p: I(N1(p), p, (1 / p) if MUTATE else 1 / (2 * p))      # F1 tail coefficient 1/(2a) (MUTATE: doubled)
I2 = lambda p: I(N2(p), p, 1 / p)            # F2 tail coefficient 1/n
check("0 F1 at alpha = 1 is exactly the framework kernel sqrt(1 + 1/y); the cancellation-free nu - 1 forms agree with the direct ones",
      all(abs(F1(1)(y) - math.sqrt(1 + 1 / y)) < 1e-12 for y in (0.01, 1, 77)) and all(abs(N1(a)(y) - (F1(a)(y) - 1)) < 1e-12 and abs(N2(a)(y) - (F2(a)(y) - 1)) < 1e-12 for a in (1, 2.5) for y in (0.1, 3, 50)))
print(f"   {'p':>5s} {'I_nu F1':>10s} {'I_nu F2':>10s}   (Lambda/a0^2 = I/2; target I = {T/math.pi:.0f} pi = {T:.2f})")
for p in (2.001, 2.003, 2.01, 2.05, 2.1, 2.5, 3, 6):
    print(f"   {p:7.4f} {I1(p):10.3f} {I2(p):10.3f}")
a1 = brentq(lambda p: I1(p) - T, 2.00001, 10); a2 = brentq(lambda p: I2(p) - T, 2.00001, 10)
print(f"   tail exponent that gives Lambda = {T/2/math.pi:.0f} pi a0^2: F1 alpha* = {a1:.4f}, F2 n* = {a2:.4f}")
check("T the analytic tail matches brute force at p = 3 (numeric to 1e7 + tail vs to Y + tail, within 1e-6)",
      abs(I1(3) - (sum(quad(lambda y: 2*y*N1(3)(y), a, b, limit=2000, epsabs=1e-13, epsrel=1e-12)[0] for a, b in ((0,1),(1,10),(10,1e2),(1e2,1e3),(1e3,1e4),(1e4,1e5),(1e5,1e6),(1e6,1e7))) + 2*(1/6)*1e7**(-1)/1)) < 1e-6)
check("A both families diverge as the tail exponent -> 2 and fall below the target for steep tails, so a solution exists in each", I1(2.00001) > T > I1(6) and I2(2.00001) > T > I2(6))
check(f"B the solution sits within 1% of the finiteness edge (alpha* - 2 = {a1-2:.2e}, n* - 2 = {a2-2:.2e}): the coefficient needs a tail tuned to the divergence", 2 < a1 < 2.02 and 2 < a2 < 2.02)
check("C the two families need different exponents for the same coefficient (|alpha* - n*| > 0.005): the coefficient tracks an unmeasured shape, so this is a fit, not a derivation",
      abs(a1 - a2) / max(a1 - 2, a2 - 2) > 0.2)
print(f"   F1 check of the pole: (alpha* - 2) x 64 pi x alpha* = {(a1-2)*T*a1:.3f}  (leading-order estimate 1 for I ~ 1/(alpha(alpha-2)))")
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
