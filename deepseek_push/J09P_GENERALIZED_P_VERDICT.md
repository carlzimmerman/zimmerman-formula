# J09P — GENERALIZED-P WINDOW LAW: VERDICT PASS (21/21)

**2026-09-23 · K01 F3 fix executed · `J09p_general_p.py` · exit 0, ALL_PASSED**

## The law

For the profile family κ(r) = τ₀(1 + q r^p), central source:

    −ln A / E[D]  =  (1 + q/(p+1)) / (1/2 + q/(p+2))      (J09P-I)

with the q→∞ limit (p+2)/(p+1).  The J09 window [4/3, 2] is the p=2 special
case.  K01 F3's audit finding — "4/3 is NOT universal across profile shapes;
e.g. p=4 gives limit 6/5 = 1.2 < 4/3" — is now numerically confirmed as a
*law*, not just a correction: the τ₀-free ratio window exists for EVERY power
profile, and its deep-opacity endpoint is (p+2)/(p+1) ∈ (1, 2].

## Verified (n = 4×10⁵, seeds fresh, independent perpendicular sampler)

| cloud | ratio measured | exact | limit | PASS |
|---|---|---|---|---|
| p=1, q=0   | 1.9925 | 2.0000 | 1.5000 | ✓ |
| p=1, q=5   | 1.6167 | 1.6154 | 1.5000 | ✓ |
| p=2, q=0   | 2.0021 | 2.0000 | 1.3333 | ✓ (J09 window) |
| p=2, q=5   | 1.5227 | 1.5238 | 1.3333 | ✓ |
| p=4, q=0   | 1.9929 | 2.0000 | 1.2000 | ✓ |
| p=4, q=5   | 1.4940 | 1.5000 | 1.2000 | ✓ |
| p=4, q=20  | 1.3005 | 1.3043 | 1.2000 | ✓ |

(fresh independent perpendicular sampler; deep-opacity tail cloud p=4,q=20:
A = 0.00685 vs pred 0.00674 — 1.6% off, within tolerance)

All 21 checks (atom law, E[D] = τ₀(½+q/(p+2)) Bernoulli-exact, ratio law)
PASS.  The sampler is independent of J02's: exact analytic rate integrals
(p=1 closed-form asinh; p=2,4 polynomial), optical-depth inversion per
segment, acceptance-sampled Thomson kernel.

## Consequence (feeds J10/J11)

The window is τ₀-free for central sources at ANY profile power — that is
exactly why the volume-source τ₀-dependence found in J11 is a *geometry*
signature, not an opacity artifact: central is flat in τ₀, volume crosses
[4/3, 2].  The pair (flat vs τ₀-curved window) is the geometry discriminator.

## Files

`J09p_general_p.py`, `J09p_general_p.out` (exit 0), this verdict.
No git commit.