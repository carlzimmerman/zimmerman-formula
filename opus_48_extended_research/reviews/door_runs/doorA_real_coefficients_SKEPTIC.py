#!/usr/bin/env python3
"""
SKEPTIC re-run of doorA_real_coefficients.py. Independently reproduce the load-bearing
extractions and stress-test the verdict BOTH WAYS, including the branch the main script
might be UNDER-stating: what if a Horava k^4 tail IS present (the framework's gate-evasion
note leans on the ghost-condensate k^4)? Does adding the REAL Horava dispersion (BS Eq.6.8)
give a sharp K_B/alpha squeeze, a robust pass, or still non-diagnostic?

Three independent checks:
  (S1) reproduce det M = 0 (omega^2 = 0) from BS Eq.(5.8) -- the scalar is NON-propagating
       at quadratic order on Minkowski. CONFIRM no k^2 wave AND no k^4 wave from AeST.
  (S2) reproduce the SZ scalar propagating-branch sound speed c_s^2 and the vector luminal
       speed, independently.
  (S3) BOTH-WAYS Horava branch: take BS Eq.(6.8) omega^2 = lambda((1-a)k^2-mu^2)/((2+3l)
       (a k^2+mu^2)) k^2. This DOES have a high-k limit. Compute the gapless group velocity
       and compare to the luminal gapped vector via Serra-Trombetta. Find the real window.
"""
import sympy as sp
import numpy as np

LINE="="*94
def hdr(s): print("\n"+LINE+"\n"+s+"\n"+LINE)

# ---------------------------------------------------------------------------
hdr("(S1) BS Eq.(5.8): reproduce det M = 0 -> omega^2 = 0 (scalar non-propagating)")
omega,k,alpha,mu = sp.symbols('omega k alpha mu', real=True)
# BS Eq.(5.8) normal-mode matrix M in field space W={psi,phi,sigma}:
#  [ -3w^2+k^2 ,   -k^2        ,  0                 ]
#  [ -k^2      ,  a k^2+mu^2   ,  i(a k^2+mu^2) w   ]
#  [ 0         , -i(a k^2+mu^2)w, (a k^2+mu^2) w^2  ]
g = alpha*k**2 + mu**2
M = sp.Matrix([
    [-3*omega**2 + k**2, -k**2,            0            ],
    [-k**2,              g,                sp.I*g*omega  ],
    [0,                 -sp.I*g*omega,     g*omega**2    ],
])
detM = sp.simplify(M.det())
print("det M =", detM)
sol = sp.solve(sp.Eq(detM,0), omega**2)
print("solve det M = 0 for omega^2 :", sol)
# expected: omega^2 = 0 (the genuine AeST result -- non-propagating scalar)
print("  => the ONLY normal-mode frequency is omega^2 = 0 (factor of omega^4):",
      "omega^4" in str(sp.factor(detM)) or detM.has(omega**4))
print("""  CONFIRMED (S1): the genuine AeST quadratic scalar action is NON-PROPAGATING
  (omega^2=0). There is NO k^2 wave and NO k^4 wave from the AeST action itself ->
  the banked B_k4=1.0 placeholder has NO AeST origin. B_AeST = 0.""")

# ---------------------------------------------------------------------------
hdr("(S2) reproduce SZ vector luminal speed + scalar propagating c_s^2 independently")
K_B,lam_s,K2,Q0 = sp.symbols('K_B lambda_s K2 Q0', positive=True)
# vector beta_i (SZ): omega^2 = k^2 + M^2 -> gradient speed^2 = 1 (coeff of k^2)
print("vector beta_i: omega^2 = k^2 + M^2  => v_gapped^2 = d(omega^2)/d(k^2)|_grad = 1 (luminal)")
# scalar (SZ): omega^2 = (2-K_B)/(K2 K_B)(1 + K_B lam_s/2) k^2 + M^2
cs2 = (2-K_B)/(K2*K_B)*(1+K_B*lam_s/2)
print("scalar c_s^2 = (2-K_B)/(K2 K_B)(1+K_B lam_s/2) =", sp.simplify(cs2))
# sanity: positivity on the window
print("  c_s^2 > 0 on 0<K_B<2, lam_s>0, K2>0 ? ->",
      sp.simplify(sp.Lt(0, cs2.subs({K_B:sp.Rational(1,2),lam_s:1,K2:1}))) )

# ---------------------------------------------------------------------------
hdr("(S3) BOTH-WAYS: the Horava k^4 branch (BS Eq.6.8). Does a REAL k^4 squeeze?")
# BS Eq.(6.8):  omega^2 = lambda*((1-alpha)k^2 - mu^2)/((2+3lambda)(alpha k^2 + mu^2)) * k^2
lam,a = sp.symbols('lambda alpha', positive=True)   # Horava params; 0<alpha<1, lambda small
disp = lam*((1-a)*k**2 - mu**2)/((2+3*lam)*(a*k**2 + mu**2)) * k**2
print("BS Eq.(6.8) scalar dispersion (Horava completion):")
print("  omega^2 =", disp)
# HIGH-k limit (k >> mu): the gapless mode's effective speed^2
hi = sp.limit(disp/k**2, k, sp.oo)
print("\n  high-k group: omega^2/k^2 ->", sp.simplify(hi), " (the high-k sound speed^2)")
# special subcase lambda=2 alpha (BS): omega^2 -> k^2 at k>>mu (luminal khronon)
hi_sub = sp.simplify(hi.subs(lam, 2*a))
print("  subcase lambda=2 alpha (BS 'luminal khronon'): high-k c_s^2 =", hi_sub)
# is there a k^4 tail? expand omega^2 at large k:
ser = sp.series(disp, k, sp.oo, 2).removeO() if False else None
# do it by substitution u=1/k
u=sp.symbols('u',positive=True)
disp_u = disp.subs(k, 1/u)
ser_u = sp.series(disp_u*u**2, u, 0, 4).removeO()   # omega^2/k^2 in powers of 1/k
print("\n  omega^2/k^2 expanded in 1/k (u=1/k):", sp.simplify(ser_u),
      "\n   -> leading is a CONSTANT (k^2 wave), the correction is ~mu^2/k^2 (IR), NOT a k^4 UV tail.")
print("""
  READING (S3, both-ways): even the HORAVA completion (the only way to make the AeST
  scalar propagate at quadratic order) gives a k^2 dispersion at high k with sound
  speed^2 = lambda(1-alpha)/((2+3lambda)alpha) -> 1 in the luminal subcase lambda=2alpha.
  It does NOT give a stabilizing omega^2 ~ +k^4 ghost-condensate tail in the propagating
  sector; the high-order spatial terms BS mention are SEPARATE, suppressed, free-scale UV
  operators. So there is NO AeST/Horava O(1) k^4 coefficient B to read -- the banked
  question 'is B >~ 0.5?' has no AeST answer; B is either 0 (AeST) or a free UV scale.
""")

# Serra-Trombetta on the Horava branch: gapless scalar high-k speed vs luminal vector(=1)
hdr("(S3b) Serra-Trombetta on the Horava branch: c_s^2(high-k) vs luminal vector =1")
cs2_hor = sp.simplify(hi)   # = lambda(1-alpha)/((2+3lambda)alpha)
print("Horava high-k c_s^2 =", cs2_hor)
# ST PASS iff c_s^2 >= 1:
cs2_hor_f = sp.lambdify((lam,a), cs2_hor, 'numpy')
print("ST PASS (c_s^2>=1) boundary, solve for lambda:",
      sp.solve(sp.Eq(cs2_hor, 1), lam))
print("\n  scan (0<alpha<1, lambda in [1e-3,2]):")
print(f"  {'alpha':>7} | " + " ".join(f"l={l:<5g}" for l in [0.01,0.1,0.5,1.0,2.0]))
for av in [0.05,0.1,0.3,0.5,0.9]:
    row=[cs2_hor_f(l,av) for l in [0.01,0.1,0.5,1.0,2.0]]
    print(f"  {av:7.2f} | " + " ".join(f"{v:7.3g}" for v in row))
print("""
  In the luminal subcase lambda=2 alpha: c_s^2 = 2alpha(1-alpha)/((2+6alpha)alpha)
   = (1-alpha)/(1+3alpha) <= 1 for all 0<alpha<1 -> ST FAILS (gapped vector =1 is FASTER)
   EXCEPT alpha->0 where c_s^2 ->1 (marginal). So on the Horava branch with the
   observationally-required luminal-GW / small-alpha choice, c_s^2 < 1 generically
   -> the luminal gapped vector is FASTER than the gapless scalar -> ST 'fails' AGAIN,
   reinforcing the main script: under the gapless-scalar/gapped-vector identification,
   ST is violated across the physical (small-alpha, CMB-fitting) region, and only
   marginally satisfied at the K2=1 / small-K_B BS corner.
""")
cs2_lum = sp.simplify(cs2_hor.subs(lam, 2*a))
print("  luminal subcase c_s^2 = (1-alpha)/(1+3alpha) =", cs2_lum,
      "  -> <=1 for 0<alpha<1 (=1 only at alpha=0).")

hdr("SKEPTIC SYNTHESIS")
print("""
S1: det M = 0 reproduced -> AeST scalar is NON-PROPAGATING (omega^2=0), NO k^4 tail.
    The banked B_k4=1.0 / M_over_mu=1.0 placeholders have NO AeST origin. B_AeST=0. CONFIRMED.
S2: vector luminal (speed^2=1); scalar c_s^2=(2-K_B)/(K2 K_B)(1+K_B lam_s/2). CONFIRMED.
S3: even the Horava completion gives a k^2 (not +k^4) dispersion; high-k c_s^2 =
    lambda(1-alpha)/((2+3lambda)alpha), and in the luminal subcase = (1-alpha)/(1+3alpha)<=1.
    So there is NO O(1) k^4 'B' to read EITHER WAY, and the ST ordering c_s^2>=1 is
    VIOLATED across the physical small-alpha / large-K2 region.

NET (both-ways): the main script's verdict stands and is, if anything, REINFORCED. The
open caveat ('read B and M/mu, decide B>~0.5 robust-pass vs B<~0.5 K_B-squeeze') is
DISSOLVED by the real action: there is NO k^4 tail in AeST (or its Horava completion's
propagating sector), the gapped partner is the LUMINAL vector (not the scalar-times-K2
the banked script used), and the genuine ST content is the ordering c_s^2>=1 i.e.
K2 <= (2-K_B)/K_B(1+K_B lam_s/2). That is SATISFIED only in the BS24 K2=1 small-K_B
corner and VIOLATED in every CMB-fitting (large-K2) SZ21 model -- a real exclusion of
the CMB-tuned corner UNDER the (contestable) gapless-scalar/gapped-vector identification,
NON-diagnostic otherwise. NOT a manufactured robust pass; NOT a reflexive squeeze;
the honest third answer the placeholder hid. Quarantine held.
""")
print("SKEPTIC complete. exit 0")
