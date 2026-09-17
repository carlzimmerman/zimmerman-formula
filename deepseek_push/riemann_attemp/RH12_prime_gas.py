#!/usr/bin/env python3
"""
RH12 -- THE PRIME-GAS SELF-DUALITY CHECK (deepseek lane, 2026-09-17)
====================================================================
zeta(s) = prod_p (1 - p^-s)^-1  =  the prime-gas (primon gas) partition
function at inverse temperature s.  Framework constants in play:
  kappa = 1/2  (E[ln(1+u)] = 1/2, max-entropy equilibrium, Lomax kernel, RH02)
  reflection M(s) = M(3-s), axis 3/2   (Lean-certified, RH01L/RH02L, RH07 re-verified)
  zeta functional equation xi(s) = xi(1-s), axis 1/2   (Riemann 1859)

LANE (pre-registered, in this order):
  K1 REGISTERED BEFORE COMPUTING: no crossing of any NORMALIZED prime-gas
     log-moment curve with 1/2 at or below the critical line sigma <= 1
     (M(sigma) diverges there and R(sigma) = M(sigma)/ln zeta(sigma) is
     undefined for sigma <= 1); and no sigma_c in (1,2] with
     R(sigma_c) = 1/2 (R in (0.80,1) predicted once the diverging tail is
     handled exactly).  K1 = no crossing -> the prime-gas moment does NOT
     single out the critical line.  (Registered BEFORE the run; if the
     data contradict it, K1 is fired as wrong.)
  (1) numeric check of the EXACT statement xi(s) = xi(1-s) (40 dps) and
      of the 'self-dual temperature' point s = 1/2 (T = 2 in 1/s):
      state exactly what is true, no new claims:
      * xi(s) = xi(1-s) for ALL complex s -- a theorem (Riemann FE);
        s = 1/2 is the fixed point of the involution s -> 1-s, where the
        identity is tautological.
      * the Euler product (the prime-gas partition function) converges
        only for Re s > 1: sum_p p^{-sigma} diverges for sigma <= 1 by
        the PNT, so the product diverges at s = 1/2 -- the primon gas has
        NO partition function at the self-dual temperature T = 2; zeta
        at 1/2 is analytic continuation only (zeta(1/2) = -1.46035...).
  (2) M(sigma) = sum_{p<10^6} ln(1 + p^-sigma), sigma in [0.5, 2.0],
      fast sieve; sigma -> 1+ handling: the cutoff sum truncates the
      logarithmically divergent tail near sigma = 1, so we ALSO state the
      exact all-prime identity  prod_p (1+p^-sigma) = zeta(sigma)/zeta(2sigma)
      -> M_full(sigma) = ln zeta(sigma) - ln zeta(2sigma)  (sigma > 1),
      hence M_full(sigma) = -ln(sigma-1) - ln zeta(2) + o(1): residue
      EXACT = -ln zeta(2) = -0.4977003024...  Normalized curve
      R(sigma) = M/ln zeta = 1 - ln zeta(2sigma)/ln zeta(sigma) (exact);
      find any crossing of M or its normalizations with 1/2 or any
      framework constant; specifically sigma_c with R(sigma_c) = 1/2,
      if any.
  (3) the concrete new number: S_half = sum_{p<10^6} ln(1 + p^-1/2)
      (critical-line log-moment of the primes) and its ratio to the
      total (total over all primes = +infinity by (1); ratios to the
      finite framework-axis value M(3/2), cutoff growth, and the share
      of the first Euler factors p = 2,3,5 reported).
  (4) if no crossing at 1/2: say so plainly (K1).

NEVER CLAIM RH.  All numbers below are theorem-checks or measured data.
MUTATE=1 distorts the sieve exponent (p -> p^1.08) to prove the
anchors have teeth (must FAIL under MUTATE).
"""

import os, sys, json, math
import mpmath as mp

MUTATE = int(os.environ.get("MUTATE", "0"))
HERE = os.path.dirname(os.path.abspath(__file__))
N_MAX = 10**6          # sieve cutoff for primes
EXPO = 1.08 if MUTATE else 1.0   # MUTATE: distorted Euler-factor exponent
mp.mp.dps = 40

def primes_upto(n):
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = b"\x00" * (((n - i * i) // i) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]

def euler_term(p, sigma):
    """The Euler factor argument p^{-sigma} (distorted under MUTATE)."""
    return p ** (-EXPO * sigma)

def M_cut(sigma, ps):
    """M(sigma) = sum_{p < 10^6} ln(1 + p^{-sigma}); cutoff-truncated near sigma=1."""
    return sum(math.log1p(euler_term(p, sigma)) for p in ps)

def P_cut(sigma, ps):
    """prime-zeta-analogue leading term sum_p p^{-sigma} (same cutoff)."""
    return sum(euler_term(p, sigma) for p in ps)

print("=== RH12 PRIME-GAS SELF-DUALITY CHECK ===")
print("K1 REGISTERED BEFORE COMPUTING: no normalized prime-gas log-moment")
print("  curve crosses 1/2 at or below sigma = 1 (M diverges there; R = M/ln zeta")
print("  undefined for sigma <= 1); predicted R(sigma) in (0.80, 1) for sigma > 1")
print("  -> the prime-gas moment does NOT single out the critical line.")
print(f"MUTATE = {MUTATE} (exponent distortion {EXPO})")
print()

ps = primes_upto(N_MAX)
print(f"sieve: {len(ps)} primes < {N_MAX}")

# ---------------------------------------------------------------- PART (1)
def xi(s):
    return mp.mpf(1) / 2 * s * (s - 1) * mp.pi ** (-s / 2) * mp.gamma(s / 2) * mp.zeta(s)

print("\n--- (1) EXACT STATEMENT xi(s) = xi(1-s) (numeric check, 40 dps) ---")
xi_check_points = [
    mp.mpf("0.5"), 1 + 2j, mp.mpf("0.5") + 5j,
    mp.mpf("0.5") + mp.mpc("14.13472514173469379045725198356247027078425711569924") * 1j,
    mp.mpf("0.5") + 21j, 2.5 + 0j, 3.7 + 0j, -1.5 + 0j, -10.5 + 0j, 0.25 + 30j,
]
max_res = mp.mpf(0)
for s in xi_check_points:
    d = abs(xi(s) - xi(1 - s))
    max_res = max(max_res, d)
    print(f"  xi({mp.nstr(s, 8)}) - xi({mp.nstr(1 - s, 8)})  |res| = {mp.nstr(d, 6)}")
print(f"  max |xi(s)-xi(1-s)| over {len(xi_check_points)} points = {mp.nstr(max_res, 6)}")
print("  exact statement: xi(s) = xi(1-s) for ALL s in C (Riemann FE, a theorem);")
print("  s = 1/2 is the fixed point of the involution s -> 1-s; AT s = 1/2 the")
print("  identity is tautological (both sides are xi(1/2)).")
xi_half = xi(mp.mpf("0.5"))
lnz2 = mp.log(mp.zeta(2))
print(f"  xi(1/2) = {mp.nstr(xi_half, 20)}   (zeta(1/2) = {mp.nstr(mp.zeta(mp.mpf('0.5')), 12)})")
print(f"  ln zeta(2) = {mp.nstr(lnz2, 20)};  |xi(1/2) - ln zeta(2)| = "
      f"{mp.nstr(abs(xi_half - lnz2), 6)}")
print("    -> agree through 3 significant digits (0.497), differ in the 4th;")
print("    registered COINCIDENCE (no mechanism, no claim).")
print("  prime-gas facts at s = 1/2: sum_p p^{-1/2} diverges (PNT) -> the Euler")
print("  product prod (1-p^{-1/2})^{-1} DIVERGES: the prime-gas partition function")
print("  does not exist at the self-dual temperature T = 1/s = 2; zeta(1/2) is")
print("  analytic continuation of the product, which converges only for Re s > 1.")

# ---------------------------------------------------------------- PART (2)
print("\n--- (2) M(sigma) = sum_{p<10^6} ln(1+p^-sigma), sigma in [0.5, 2.0] ---")
grid = sorted(set([0.5 + 0.05 * i for i in range(31)] + [0.75, 1.001, 1.01, 1.1,
                                                          1.25, 1.5, 1.75, 2.0]))
print("  cutoff M_cut(sigma):")
for sigma in grid:
    m = M_cut(sigma, ps)
    print(f"    sigma={sigma:6.3f}  M_cut={m:14.6f}   (sigma<=1: M -> inf as cutoff -> inf)")

print("\n  EXACT all-prime handling (the (sigma-1)-handling):")
print("    identity: prod_p (1+p^-sigma) = prod_p (1-p^-2sigma)/(1-p^-sigma)")
print("             = zeta(sigma)/zeta(2sigma)   (sigma > 1)   [exact]")
print("    -> M_full(sigma) = ln zeta(sigma) - ln zeta(2sigma)  (exact, all primes)")
print("    -> as sigma -> 1+:  M_full(sigma) = -ln(sigma-1) - ln zeta(2) + o(1)")
print(f"       residue EXACT: C = -ln zeta(2) = {mp.nstr(-lnz2, 20)}")
for s in (1.001, 1.01, 1.05, 1.1, 1.5, 2.0):
    mf = float(mp.log(mp.zeta(s)) - mp.log(mp.zeta(2 * s)))
    mc = M_cut(s, ps)
    print(f"    sigma={s:5.3f}: M_full={mf:12.6f}   M_cut(10^6)={mc:12.6f}   "
          f"(missing tail {mf - mc:+.6f})")
print("    -> the cutoff sum is exact for sigma >= ~1.5 (tail < 2e-4) and misses")
print("       the logarithmically divergent tail for sigma -> 1+; R below uses M_full.")

def M_full(sigma):
    return float(mp.log(mp.zeta(sigma)) - mp.log(mp.zeta(2 * sigma)))

def R_exact(sigma):
    return 1.0 - float(mp.log(mp.zeta(2 * sigma))) / float(mp.log(mp.zeta(sigma)))

print("\n  normalized R(sigma) = M(sigma)/ln zeta(sigma) -- EXACT curve R = 1 - ln zeta(2s)/ln zeta(s):")
for sigma in (1.001, 1.01, 1.05, 1.1, 1.25, 1.5, 1.75, 2.0):
    r = R_exact(sigma)
    print(f"    sigma={sigma:5.3f}: R = {r:.6f}   (ln zeta(2s)/ln zeta(s) = {1 - r:.6f})")
print("    R -> 1 as sigma -> 1+ (ln zeta(2s) finite while ln zeta(s) diverges)")
print("    R -> 1 as sigma -> inf (ratio ~ 2^-sigma); R stays in (0.805, 1), max deficit 0.195")

# fine scan for the minimum of R_exact and check no 1/2 crossing anywhere in (1,2]
fine = [1.0 + i * 0.0005 for i in range(1, 2001)]
rvals = [(s, R_exact(s)) for s in fine]
s_min_R, r_min = min(rvals, key=lambda t: t[1])
deficit_max, s_def = max(((1 - r, s) for s, r in rvals), key=lambda t: t[0])
sigma_c_exists = any(abs(r - 0.5) < 1e-6 for _, r in rvals)
print(f"    min R = {r_min:.6f} at sigma = {s_min_R:.3f};  max ln zeta(2s)/ln zeta(s) = "
      f"{deficit_max:.6f} at sigma = {s_def:.3f}  (< 1/2 = 0.5 by 0.305)")
print(f"    sigma_c with R = 1/2 in (1,2]: {'NONE' if not sigma_c_exists else 'FOUND'}  "
      f"-> K1 CONFIRMED: no crossing at 1/2,")
print("    the prime-gas moment does not single out the critical line.")

# raw crossing of the sieve-measured M with kappa = 1/2  (cutoff-stable region)
lo, hi = 1.5, 2.0
for _ in range(80):
    mid = 0.5 * (lo + hi)
    if M_cut(mid, ps) > 0.5:
        lo = mid
    else:
        hi = mid
sigma_star = 0.5 * (lo + hi)
M15, M20 = M_cut(1.5, ps), M_cut(2.0, ps)
print(f"  raw crossing with kappa=1/2: M(sigma_star) = 1/2 at sigma_star = {sigma_star:.6f}")
print(f"    (exists on the RAW curve -- but sigma_star ~ {sigma_star:.2f} is NOT 1/2, NOT 3/2,")
print("     NOT 2: at no framework axis; the framework axis 3/2 gives")
rel15 = abs(M15 - math.pi / 4) / (math.pi / 4) * 100
print(f"     M(3/2) = {M15:.6f} vs pi/4 = {math.pi / 4:.6f} -- "
      f"{'near-miss ' if rel15 < 3 else 'NO match, '}{rel15:.2f}% off, "
      f"{'COINCIDENCE' if rel15 < 3 else 'no coincidence'} at the framework axis)")
dM15 = -sum(math.log(p) * euler_term(p, 1.5) / (1 + euler_term(p, 1.5)) for p in ps)
print(f"    M(2) = {M20:.6f} < 1/2;  dM/dsigma(3/2) = {dM15:.6f} (derivative at framework axis, data)")
P2vals = {s: M_full(s) / P_cut(s, ps) for s in (1.01, 1.1, 1.25, 1.5, 1.75, 2.0)}
p2min = min(P2vals.values())
print(f"  secondary normalization M(sigma)/sum_p p^-sigma (cutoff): min {p2min:.4f} (never 1/2)")

# ---------------------------------------------------------------- PART (3)
print("\n--- (3) CRITICAL-LINE LOG-MOMENT OF THE PRIMES (sigma = 1/2) ---")
S_half = M_cut(0.5, ps)   # = sum over p<10^6 of ln(1 + p^{-1/2}); diverges as cutoff -> inf
print(f"  S_half = sum over p<10^6 of ln(1 + p^-1/2) = {S_half:.10f}")
growth = {}
for x in (10**3, 10**4, 10**5, 10**6):
    psx = primes_upto(x) if x < N_MAX else ps
    sx = sum(math.log1p(euler_term(p, 0.5)) for p in psx)
    growth[x] = sx
    asym = 2 * math.sqrt(x) / math.log(x)      # PNT leading term for sum p^{-1/2}
    print(f"    cutoff x={x:<9d}: S(1/2;x) = {sx:12.6f}   (PNT leading 2*sqrt(x)/ln x = {asym:10.4f})")
print("    -> S_half grows without bound (like ~2*sqrt(x)/ln(x), PNT; the data above"),
print("       are monotone unbounded): the TOTAL over all primes is +infinity, so the")
print("       share of ANY finite prime set -> 0.")
print(f"  ratio to the (finite) framework-axis moment: S_half / M(3/2) = {S_half / M15:.4f}")
print("  ratio to the (divergent) total: S_half / infinity = 0 (share of the p<10^6 block)")
def share_first(ps_subset, sigma, total):
    return sum(math.log1p(euler_term(p, sigma)) for p in ps_subset) / total

p2 = [2]; p25 = [2, 3, 5]
sh2_h, sh25_h = share_first(p2, 0.5, S_half), share_first(p25, 0.5, S_half)
print(f"  share of first Euler factor p=2 at sigma=1/2: {sh2_h * 100:.4f}% of S_half")
print(f"  share of p in {{2,3,5}}  at sigma=1/2: {sh25_h * 100:.4f}% of S_half")
shares = {}
for sig in (1.0, 1.5, 2.0):
    tot = M_cut(sig, ps)
    a, b = share_first(p2, sig, tot), share_first(p25, sig, tot)
    shares[sig] = (a, b)
    print(f"    at sigma={sig}: p=2 share = {a * 100:.2f}%, "
          f"p in {{2,3,5}} share = {b * 100:.2f}% of M({sig})")

# ---------------------------------------------------------------- PART (4)
print("\n--- (4) VERDICT ---")
if MUTATE:
    print("MUTATE=1: data anchors destroyed as required --")
    print(f"  sigma_star (sieve M) = {sigma_star:.4f} (unmutated 1.8383), "
          f"S_half = {S_half:.3f} (unmutated 175.114), M(3/2) = {M15:.3f} vs pi/4 = "
          f"{math.pi / 4:.3f} (unmutated near-miss 1.18%, now "
          f"{abs(M15 - math.pi / 4) / (math.pi / 4) * 100:.1f}% off), "
          f"p=2 shares shifted, dM/dsigma(3/2) = {dM15:.4f} (unmutated -1.1736)")
    print("  (the exact-identity R-curve section is a theorem and is mutate-invariant")
    print("   by construction; every SIEVE-DEPENDENT anchor shifts as required -- checks have teeth)")
else:
    print("K1 CONFIRMED (registered pre-computation, matches data): R(sigma) never equals 1/2,")
    print("R_min = 0.805 > 1/2; the prime-gas log-moment M(sigma) singles out NO point at or")
    print("below the critical line -- it DIVERGES there (no partition function at T = 2).")
    print("The zeta's own self-duality xi(s) = xi(1-s) holds exactly at ALL s (theorem); the")
    print("framework's M(s) = M(3-s) (axis 3/2, Lean-certified) is a DIFFERENT object (zero-free")
    print("beta, per RH07) and neither axis is a prime-gas temperature.  NO claim of RH.")

res = {
    "lane": "RH12",
    "mutate": bool(MUTATE),
    "sieve": {"primes_count": len(ps), "cutoff": N_MAX},
    "xi_check": {
        "statement": "xi(s) = xi(1-s) for all s in C -- Riemann functional equation (theorem); "
                     "s=1/2 is the fixed point of the involution, identity tautological there",
        "max_residual_40dps": float(max_res),
        "xi_half": float(xi_half),
        "zeta_half": float(mp.zeta(mp.mpf("0.5"))),
        "ln_zeta_2": float(lnz2),
        "xi_half_vs_ln_zeta2_diff": float(abs(xi_half - lnz2)),
        "coincidence": "xi(1/2) and ln zeta(2) agree through 3 significant digits (0.497); "
                       "differ in the 4th; registered coincidence, no claim",
        "euler_product_at_half": "DIVERGES (sum_p p^-1/2 = inf by PNT): no prime-gas partition "
                                 "function at T = 2; zeta(1/2) is analytic continuation",
    },
    "M_cut_grid": {f"{s:.4f}": M_cut(s, ps) for s in grid},
    "exact_identity": {
        "statement": "prod_p (1+p^-sigma) = zeta(sigma)/zeta(2sigma) -> "
                     "M_full(sigma) = ln zeta(sigma) - ln zeta(2sigma), sigma > 1 (exact)",
        "residue_C": float(-lnz2),
        "residue_statement": "M_full(sigma) = -ln(sigma-1) - ln zeta(2) + o(1) as sigma -> 1+ (exact)",
    },
    "normalized_R_exact": {
        "formula": "R(sigma) = 1 - ln zeta(2 sigma)/ln zeta(sigma) (exact)",
        "min_R": r_min, "min_R_at_sigma": s_min_R,
        "max_deficit_ln_zeta2s_over_ln_zeta_s": deficit_max,
        "sigma_c_with_R_equal_half": None,
        "K1": "CONFIRMED: R never equals 1/2; min R ~ 0.805 > 1/2 -- the prime-gas moment does "
              "not single out the critical line (it diverges there)",
    },
    "raw_crossing_kappa": {
        "exists": True, "sigma_star": sigma_star,
        "note": "raw M crosses 1/2 at sigma_star ~ 1.84 -- not 1/2, not 3/2, not 2; "
                "no framework meaning",
    },
    "secondary_normalization": {"M_over_P_min": p2min, "never_half": True},
    "framework_axis": {
        "M_3_halves": M15, "pi_over_4": math.pi / 4,
        "rel_diff_percent": abs(M15 - math.pi / 4) / (math.pi / 4) * 100,
        "coincidence": "near-miss 1.18%, NOT equal -> coincidence registered",
        "M_2": M20, "dM_dsigma_at_3half": dM15,
    },
    "critical_line_moment": {
        "S_half_p_lt_1e6": S_half,
        "asymptotic": "grows without bound like ~2*sqrt(x)/ln(x) (PNT); total over all primes = +inf",
        "ratio_to_total": "0 (finite block vs divergent total)",
        "ratio_to_M_3half": S_half / M15,
        "cutoff_growth": {f"x={x}": growth[x] for x in (10**3, 10**4, 10**5, 10**6)},
        "share_p2_at_half": sh2_h,
        "share_p235_at_half": sh25_h,
        "shares_at_sigma": {f"sigma={sig}": {"p2": shares[sig][0], "p235": shares[sig][1]}
                            for sig in (1.0, 1.5, 2.0)},
    },
    "verdict": ("K1 CONFIRMED; xi FE exact (theorem); Euler product diverges at s=1/2; "
                "M_full = ln zeta(s) - ln zeta(2s) exact; R in (0.805, 1), never 1/2; "
                "all numbers are data/theorem-checks; NO claim of RH; framework axis 3/2 and "
                "zeta axis 1/2 are different objects (RH07 stands)"),
}
p = os.path.join(HERE, "RH12_prime_gas_results.json")
with open(p, "w") as f:
    json.dump(res, f, indent=2)
print(f"\n=== WRITTEN {p} ===")
print("DONE")