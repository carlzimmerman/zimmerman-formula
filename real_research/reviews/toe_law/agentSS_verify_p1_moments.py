"""
agentSS VERIFY part 1 — INDEPENDENT re-derivation of the load-bearing results.
All numeric (mpmath), but using a method that does NOT share the route's code path:
  - moments via the 0F1 generating function Z(t)=sum t^n/[n!(2D)_n] and its analytic
    theta=t d/dt derivatives evaluated by mp.diff (NOT the route's hand-summed central moments),
  - cross-checked by a fully independent direct Pochhammer summation.
  (A) R = 4 j3/j2^2 =? 8 Delta for a_n = 1/[n!(2Delta)_n].
  (B) modular/dilation scaling weight of 4 j3/j2^2 (claimed -1).
  (C) character-weight (2D)_n/n! divergence (claimed: not a line shape).
RUTHLESS: assume R=8D and weight=-1 overclaimed until reproduced independently.
"""
import mpmath as mp
mp.mp.dps = 40

def poch(a, k):
    r = mp.mpf(1)
    for i in range(int(k)):
        r *= (a + i)
    return r

# ---- METHOD 1: generating function + analytic theta-derivatives -------------
# Z(t) = 0F1(; 2D; t).  Raw POWER moments m_k = (theta^k Z)/Z |_{t=1}, theta=t d/dt.
# Use mp.hyp0f1 and numerical differentiation for theta powers.
def Z(D, t):
    return mp.hyp0f1(2*D, t)

def theta_moments(D, K=3):
    """raw power moments <n^k>, k=0..K, via theta operator on Z at t=1."""
    # build theta^k Z as function of t, evaluate at 1. theta f = t f'.
    # Implement by repeated symbolic-ish numeric: define g0=Z; g_{k+1}=t*g_k'.
    funcs = [lambda t, D=D: Z(D, t)]
    for k in range(K):
        prev = funcs[-1]
        def nxt(t, prev=prev):
            return t*mp.diff(prev, t)
        funcs.append(nxt)
    Z1 = Z(D, mp.mpf(1))
    return [funcs[k](mp.mpf(1))/Z1 for k in range(K+1)]

def central_from_raw(m):
    m1, m2, m3 = m[1], m[2], m[3]
    j2 = m2 - m1**2
    j3 = m3 - 3*m2*m1 + 2*m1**3
    return j2, j3

# ---- METHOD 2: independent direct Pochhammer summation (different from route's loop) ----
def direct_moments(D, N=4000):
    D = mp.mpf(D)
    a = [1/(mp.factorial(n)*poch(2*D, n)) for n in range(N)]
    Zs = mp.fsum(a)
    m1 = mp.fsum(a[n]*n for n in range(N))/Zs
    # central via shifted sums
    j2 = mp.fsum(a[n]*(n-m1)**2 for n in range(N))/Zs
    j3 = mp.fsum(a[n]*(n-m1)**3 for n in range(N))/Zs
    return j2, j3

print("="*72)
print("(A) R = 4 j3/j2^2 for a_n=1/[n!(2D)_n]: METHOD1 (genfn-theta) vs METHOD2 (direct)")
print("="*72)
print(f"{'Delta':>7} {'R_method1':>16} {'R_method2':>16} {'8*Delta':>12} {'R-8D(m1)':>14}")
for Dv in [mp.mpf('0.5'), mp.mpf(1), mp.mpf(2), mp.mpf(4), mp.mpf(8), mp.mpf(16)]:
    m = theta_moments(Dv, 3)
    j2a, j3a = central_from_raw(m)
    Ra = 4*j3a/j2a**2
    j2b, j3b = direct_moments(Dv)
    Rb = 4*j3b/j2b**2
    print(f"{mp.nstr(Dv,4):>7} {mp.nstr(Ra,10):>16} {mp.nstr(Rb,10):>16} {mp.nstr(8*Dv,8):>12} {mp.nstr(Ra-8*Dv,6):>14}")

print()
print("Small-Delta high-precision check of leading constant + subleading:")
for Dv in [mp.mpf('0.5'), mp.mpf(1), mp.mpf(2)]:
    m = theta_moments(Dv, 3)
    j2, j3 = central_from_raw(m)
    R = 4*j3/j2**2
    print(f"  Delta={mp.nstr(Dv,3)}: R={mp.nstr(R,12)}, 8D={mp.nstr(8*Dv,6)}, R-8D={mp.nstr(R-8*Dv,8)}")
print("  -> if R = 8D + c with c->0 as D grows, the ratio SLIDES with free Delta (PERMITS).")
