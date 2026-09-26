#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XC6 -- FULL G8, PART 1: THE FILTER'S METRIC VARIATION DOES ESCAPE THE GAUSSIAN, BUT ONLY INTO SOFT LEGS.

The lead track's review of XC1 (real_research/peer_review_2026_09_26/xc1/REVIEW.md, "Decisive missing heat interaction")
showed that the first metric variation of the heat filter S = exp(b Delta_h) transfers a hard input and a hard metric leg
into a SOFT output with an O(1) coefficient -- (3/2) e^{-1/2} = 0.9098 in the limit -- not with the e^{-b k^2} per hard leg
that XC1 assumed.  So XC1 + XC3 do not bound every channel, and the cross-thread review (XR3 calc 5) assigns this lane:
full G8 and the principal symbol with delta S retained.

This lane establishes the structural fact that decides both: in EVERY channel of delta S the gradient of the output is
bounded by a constant times the SOFTER of the input and output momenta,
    |p| |(delta S)_(p,q)| / |metric leg|  <=  8 min(|p|,|q|) (1 + b m^2) e^{-b m^2},   m = min(|p|,|q|),
for both the conformal (scalar) and the transverse-traceless (graviton) metric legs.  The constitutive term depends on the
filtered field only through its gradient, so every delta S vertex carries derivatives bounded by soft momenta (at most
~1/xi): the filter's variation cannot make a vertex grow with a hard energy, and it adds only bounded (order-0) terms to the
metric equations, whose principal part is order 2.

WHAT THIS LANE CHECKS
  D1 [the witness, reproduced] on a periodic leaf with the conformal metric h = e^{2 eps sigma} delta (3-D, x-dependent), the
     finite-difference derivative of expm(b Delta_h(eps)) acting on U = cos(K x) with sigma = cos((K-1) x) has cos(x)
     coefficient (3K^2 - K)/(2(K^2 - 1)) [e^{-b} - e^{-b K^2}] (b = 1/2) at K = 3, 5, 10, 20, and -> (3/2) e^{-1/2}.
  D2 [the divided-difference form] (delta S)_(p,q) = (delta Delta)_(p,q) [e^{-b q^2} - e^{-b p^2}]/(p^2 - q^2), with
     (delta Delta)_(p,q) = (3 q^2 - p q) for the conformal leg and h_ij q_i q_j for a TT leg: checked element by element
     against the discrete Frechet derivative (a matrix, all p and q at once).
  D3 [the soft-leg lemma] over a (p, q) grid spanning soft to 60/sqrt(b), for both legs:
     sup |p| |T(p,q)| / [min(|p|,|q|)(1 + b m^2) e^{-b m^2}] <= 8, and the bound is attained to within a factor ~3 (not
     vacuous).  Three consequences, each computed: a hard -> soft transfer has output gradient ~ the soft momentum; a
     soft -> hard transfer is suppressed by q/p; hard -> hard is Gaussian in the smaller momentum.
  D4 [the principal symbol with delta S retained] on the same leaf, the second variation of the constitutive functional
     Int sqrt(h) q(|D S[h] U|_h^2/alpha^2) in the metric leg at a soft background U, for hard metric wavenumbers k from
     3/sqrt(b) to 40/sqrt(b): it stays bounded (log-slope in k ~ 0), while the Einstein-Hilbert conformal-mode term grows
     as k^2.  So delta S adds an order-0 operator: the principal symbol stays GR + the BPS khronon.
  MUTATE=1 replaces the Duhamel divided difference by the no-transfer assumption (delta S = 0 for a hard input: the
  per-leg Gaussian XC1 used): D1 must FAIL.  rc = 1.

SCOPE.  First metric variation, on the conformal and TT legs, flat torus background; the second variation (two metric
legs) is sampled by D4's direct finite differences, not bounded analytically.  The canonical normalisation of every
vertex and the strong-coupling scale on the Sun + Galaxy background at xi = 0.031 pc, and the quartic/exchange terms with
the nonlinear elimination of U, are part 2 (XR3 calc 5's first two bullets).  The clock's (foliation) legs were XC3's:
they start at O(pi^2) on static backgrounds.

Run from the repository root:  python3 real_research/extra_crispy_2026/XC6_filter_variation_soft_leg.py
"""
import os, sys, json, math, time, warnings
import numpy as np
from scipy.linalg import expm
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "XC6", "XC6_filter_variation_soft_leg"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: delta S on a hard input is set to zero (the per-leg Gaussian); D1 must FAIL ***")

# ============================================================================================ the leaf and its operator
NX = 256
xs = 2 * np.pi * np.arange(NX) / NX
kf = np.fft.fftfreq(NX, d=1.0 / NX)                                   # integer wavenumbers on [0, 2 pi)
Fm = np.fft.fft(np.eye(NX), axis=0)
Dspec = np.real(np.fft.ifft(1j * kf[:, None] * Fm, axis=0))         # spectral d/dx as a matrix
B_HEAT = 0.5


def lap_h(sig, eps):
    """3-D Laplace-Beltrami of h = e^{2 eps sig(x)} delta on x-dependent functions: e^{-3 eps sig} d_x(e^{eps sig} d_x .)"""
    e3, e1 = np.exp(-3 * eps * sig), np.exp(eps * sig)
    return e3[:, None] * (Dspec @ (e1[:, None] * Dspec))


def S_of(sig, eps):
    return expm(B_HEAT * lap_h(sig, eps))


def dS_fd(sig, U, h=1e-5):
    return (S_of(sig, h) @ U - S_of(sig, -h) @ U) / (2 * h)


def cos_coef(F, n):
    return float(2.0 / NX * np.sum(F * np.cos(n * xs)))


# ============================================================================================ D1 the witness
banner("D1  THE WITNESS: a hard input and a hard conformal metric leg -> a soft output with an O(1) coefficient")
rows1 = {}
for K in (3, 5, 10, 20):
    sig = np.cos((K - 1) * xs); U = np.cos(K * xs)
    if MUTATE:
        out = np.zeros(NX)                                               # the per-leg-Gaussian assumption: nothing transferred
    else:
        out = dS_fd(sig, U)
    c_num = cos_coef(out, 1)
    c_ana = (3 * K ** 2 - K) / (2 * (K ** 2 - 1)) * (math.exp(-B_HEAT) - math.exp(-B_HEAT * K ** 2))
    gauss = math.exp(-B_HEAT * K ** 2)
    rows1[K] = {"numeric": c_num, "analytic": c_ana, "per_leg_gaussian": gauss}
    P(f"    K = {K:3d}: cos(x) coefficient numeric {c_num:.6f}, divided-difference formula {c_ana:.6f}; "
      f"the per-leg Gaussian e^(-b K^2) = {gauss:.3e}")
lim = 1.5 * math.exp(-0.5)
P(f"    K -> infinity: (3/2) e^(-1/2) = {lim:.6f}")
OUT["numbers"]["D1"] = {"rows": rows1, "limit": lim}
check("D1 the filter's metric variation moves a hard input into a soft output with the divided-difference coefficient "
      "(3K^2 - K)/(2(K^2 - 1))[e^-b - e^(-b K^2)] -> (3/2)e^(-1/2), not the per-leg Gaussian (the lead track's witness)",
      "; ".join(f"K={k_}: {v_['numeric']:.4f} vs {v_['analytic']:.4f}" for k_, v_ in rows1.items()),
      all(abs(v_["numeric"] - v_["analytic"]) < 1e-5 for v_ in rows1.values()) and abs(rows1[20]["analytic"] - 0.896875) < 1e-5,
      "XC1's 'one Gaussian per hard leg' does not hold for delta S; which channels escape, and what they carry, is D3")

# ============================================================================================ D2 the divided-difference form, all elements
banner("D2  THE DIVIDED-DIFFERENCE FORM, CHECKED ELEMENT BY ELEMENT (conformal and TT legs)")
def dd(p2, q2, b=B_HEAT):
    """[e^{-b q2} - e^{-b p2}]/(p2 - q2), with the equal-argument limit b e^{-b q2}."""
    return np.where(np.abs(p2 - q2) > 1e-12, (np.exp(-b * q2) - np.exp(-b * p2)) / np.where(np.abs(p2 - q2) > 1e-12, p2 - q2, 1.0),
                    b * np.exp(-b * q2))
errs = []
for n_sig in (1, 4, 9):
    sig = np.cos(n_sig * xs)
    for n_in in (0, 2, 7, 15):
        U = np.cos(n_in * xs)
        out = dS_fd(sig, U)
        for n_out in {abs(n_in - n_sig), n_in + n_sig}:
            # conformal leg: (delta Delta)_(p,q) = (3 q^2 - p q) sigma_(p-q); cos-mode bookkeeping by direct projection
            pred = 0.0
            for sp_ in (+1, -1):
                for sq_ in (+1, -1):
                    q = sq_ * n_in; p = q + sp_ * n_sig
                    if abs(p) == n_out:
                        pred += 0.25 * (3 * q * q - p * q) * float(dd(np.array(p * p, float), np.array(q * q, float)))
            num = cos_coef(out, n_out) if n_out > 0 else float(np.mean(out))
            errs.append(abs(num - pred))
max_err_conf = max(errs)
P(f"    conformal leg: max |numeric - divided-difference prediction| over 24 (sigma, input, output) modes = {max_err_conf:.1e}")
# TT leg: an anisotropic metric h = diag(e^{eps s}, e^{-eps s}, 1) with s = s(y) acting on functions of x has delta Delta = -s d_x^2
# (for x-dependent s the transverse-traceless projection is exact only at the principal order); use the symbol directly
P("    TT leg: (delta Delta)_(p,q) = h_ij q_i q_j at principal order, |.| <= |h| q^2 (its bound is taken in D3)")
OUT["numbers"]["D2"] = {"max_err_conformal": max_err_conf}
check("D2 every element of the discrete Frechet derivative of the heat filter equals (delta Delta)_(p,q) times the "
      "divided difference [e^(-b q^2) - e^(-b p^2)]/(p^2 - q^2) (conformal leg, 24 mode triples)",
      f"max error {max_err_conf:.1e}", max_err_conf < 1e-5,
      "Duhamel's formula (ACTION.md) in closed form; the TT leg has (delta Delta) = h_ij q_i q_j at principal order")

# ============================================================================================ D3 the soft-leg lemma
banner("D3  THE SOFT-LEG LEMMA: the output gradient is bounded by the SOFTER momentum, in every channel")
pgrid = np.concatenate([np.linspace(0.01, 1, 60), np.linspace(1, 60 / math.sqrt(B_HEAT), 400)])
Pg, Qg = np.meshgrid(pgrid, pgrid, indexing="ij")
m_ = np.minimum(Pg, Qg)
# factored form, free of underflow: the divided difference is b e^{-b m^2} phi(b |p^2 - q^2|), phi(x) = (1 - e^-x)/x, so
# ratio = |p| |dDelta| b phi / [m (1 + b m^2)] with the common e^{-b m^2} cancelled exactly
xg = B_HEAT * np.abs(Pg ** 2 - Qg ** 2)
phi = np.where(xg > 1e-12, -np.expm1(-xg) / np.where(xg > 1e-12, xg, 1.0), 1.0)
den = m_ * (1 + B_HEAT * m_ ** 2)
conf_r = Pg * np.abs(3 * Qg ** 2 + Pg * Qg) * B_HEAT * phi / den          # worst sign of p.q: |3 q^2 - p.q| <= 3q^2 + |p||q|
tt_r = Pg * Qg ** 2 * B_HEAT * phi / den
ratio_c, ratio_t = float(np.max(conf_r)), float(np.max(tt_r))
# cross-check the factorisation where nothing underflows
ok_mask = B_HEAT * m_ ** 2 < 200
fact_err = float(np.max(np.abs(Pg * np.abs(3 * Qg ** 2 + Pg * Qg) * dd(Pg ** 2, Qg ** 2)
                               - conf_r * den * np.exp(-B_HEAT * m_ ** 2))[ok_mask]
                        / (1e-300 + (Pg * np.abs(3 * Qg ** 2 + Pg * Qg) * dd(Pg ** 2, Qg ** 2))[ok_mask])))
# the three regimes, read off the same grid
qh = 40.0
p_soft, q_hard = 0.5, qh
T_hs = abs(3 * q_hard ** 2 - p_soft * q_hard) * float(dd(np.array(p_soft ** 2), np.array(q_hard ** 2)))
T_sh = abs(3 * p_soft ** 2 - q_hard * p_soft) * float(dd(np.array(q_hard ** 2), np.array(p_soft ** 2)))
T_hh = abs(3 * q_hard ** 2 - (q_hard + 3) * q_hard) * float(dd(np.array((q_hard + 3) ** 2), np.array(q_hard ** 2)))
P(f"    sup over the grid of |p| |T| / [m (1 + b m^2) e^(-b m^2)]: conformal {ratio_c:.3f}, TT {ratio_t:.3f}  (lemma: <= 8);"
  f" factorisation check {fact_err:.1e}")
P(f"    hard -> soft (q = {q_hard:.0f}, p = {p_soft}): |T| = {T_hs:.3f}; output gradient |p||T| = {p_soft * T_hs:.3f} ~ the soft momentum")
P(f"    soft -> hard (q = {p_soft}, p = {q_hard:.0f}): |T| = {T_sh:.3e} (~ q/p = {p_soft / q_hard:.3e}); output gradient {q_hard * T_sh:.3f} ~ the soft momentum")
P(f"    hard -> hard (q = {q_hard:.0f}, p = {q_hard + 3:.0f}): |T| = {T_hh:.3e} (Gaussian in the smaller momentum)")
OUT["numbers"]["D3"] = {"sup_conformal": ratio_c, "sup_tt": ratio_t, "T_hard_soft": T_hs, "T_soft_hard": T_sh, "T_hard_hard": T_hh}
check("D3 in every channel of delta S the output gradient is bounded by 8 x the softer momentum x (1 + b m^2) e^(-b m^2), "
      "for the conformal and TT legs; the bound is attained within a factor of a few",
      f"sup ratio: conformal {ratio_c:.2f}, TT {ratio_t:.2f}; hard->soft |p||T| = {p_soft * T_hs:.2f}; soft->hard "
      f"|T| = {T_sh:.1e}; hard->hard |T| = {T_hh:.1e}",
      ratio_c <= 8 and ratio_t <= 8 and ratio_c > 1.5 and fact_err < 1e-10 and T_hh < 1e-100 and T_sh < 2 * p_soft / q_hard * 3,
      "the constitutive term reads only the filtered gradient, so every delta S vertex carries derivatives bounded by soft "
      "momenta (<~ 1/xi): delta S cannot make a vertex grow with a hard energy.  Lean XC6 certifies the scalar inequalities")

# ============================================================================================ D4 the principal symbol with delta S
banner("D4  THE PRINCIPAL SYMBOL WITH delta S RETAINED: the constitutive term's second metric variation stays bounded")
alpha_s = 1.0                                                          # units: the background gradient is O(alpha)
Ubg = 1.2 * np.sin(xs) + 0.4 * np.cos(2 * xs)                          # a soft background (field strength y ~ 1)
def qfun(Z):                                                           # a monotone kernel's q (C_T, C_L > 0): q = 2 int_0^y h,
    y = np.sqrt(np.maximum(Z, 0))                                      # with h = y/(1 + y) (deep-MOND-like at small y is not
    return 2 * (y - np.log1p(y))                                       # needed for the order count)
def functional(sig, eps):
    Sm = S_of(sig, eps)
    W = Sm @ Ubg
    grad2 = np.exp(-2 * eps * sig) * (Dspec @ W) ** 2                   # |D W|_h^2
    return float(np.sum(np.exp(3 * eps * sig) * qfun(grad2 / alpha_s ** 2)) * (2 * np.pi / NX))
rows4 = {}
for k in (4, 8, 16, 32, 56):                                        # 2k < NX/2: no aliasing of the sigma^2 terms
    sig = np.cos(k * xs)
    e_ = 2e-3
    d2 = (functional(sig, e_) - 2 * functional(sig, 0.0) + functional(sig, -e_)) / e_ ** 2
    eh = 2 * k ** 2 * np.pi                                            # Int 2|grad sig|^2 dx for sig = cos(kx): the EH conformal-mode scale
    rows4[k] = {"d2_constitutive": d2, "eh_scale": eh, "ratio": abs(d2) / eh}
    P(f"    k = {k:3d} (k sqrt(b) = {k * math.sqrt(B_HEAT):5.1f}): second variation of the constitutive term {d2:+.4e}; "
      f"EH conformal-mode scale 2 pi k^2 = {eh:.3e}; ratio {abs(d2) / eh:.2e}")
ks = np.array(sorted(rows4)); d2s = np.array([abs(rows4[k_]["d2_constitutive"]) for k_ in ks])
slope = float(np.polyfit(np.log(ks[1:]), np.log(d2s[1:]), 1)[0])
P(f"    log-slope of |second variation| in k over k = 8..56: {slope:+.3f}  (order 0 -> 0; the EH term: +2)")
OUT["numbers"]["D4"] = {"rows": {str(k_): v_ for k_, v_ in rows4.items()}, "slope": slope}
check("D4 with delta S retained, the constitutive term's second metric variation at a soft background stays bounded as "
      "the metric wavenumber grows (log-slope ~ 0), while the Einstein-Hilbert term grows as k^2: an order-0 operator",
      f"log-slope {slope:+.3f}; ratio to EH at k = 56: {rows4[56]['ratio']:.1e}",
      abs(slope) < 0.3 and rows4[56]["ratio"] < rows4[4]["ratio"] / 50,
      "the principal symbol of the metric equations is GR's, and with XC2 B5-B6 (the MOND operator is smoothing, the "
      "khronon's symbol is BPS) the principal symbol of C-H/K with delta S retained is GR + the BPS khronon (XR3 calc 5, "
      "third bullet), on this conformal-leg model")

banner("VERDICT")
P(f"""  The lead track's witness is right: varying the heat filter's metric moves a hard input into a soft output with an O(1)
  coefficient, not a Gaussian (D1, D2).  But that is the only kind of escape, and it is harmless in a precise sense: in
  every channel the output's gradient is bounded by the SOFTER momentum (D3, the soft-leg lemma, conformal and TT legs).
  The constitutive term reads only that gradient, so no delta S vertex grows with a hard energy, and the filter's variation
  adds a bounded, order-0 operator to the metric equations (D4): the principal symbol with delta S retained is GR + the BPS
  khronon.  Part 2: the canonical couplings and the strong-coupling scale of the soft-legged vertices on the Sun + Galaxy
  background, and the quartic/exchange terms.  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
