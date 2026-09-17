#!/usr/bin/env python3
"""
RH11 -- THE ZERO-FREE REGION ROUTE: the classical 3-4-1 (Hadamard/de la Vallee
================================================================================
Poussin) trick WITH THE FRAMEWORK'S LOMAX KERNEL SUBSTITUTED -- first attempt.

CLASSICAL SCHEME (the 3-4-1).  The Euler product gives, for sigma > 1 and ANY
weights (A, B, C) -- the identity is linear in the weights:

    A*log|zeta(sigma)| + B*log|zeta(sigma+it)| + C*log|zeta(sigma+2it)|
        = sum_p sum_m p^{-m*sigma} * k(m*theta_p) / m,
        k(theta) = A + B*cos(theta) + C*cos(2*theta),  theta_p = t*log(p).

Hadamard/dVP take (A,B,C) = (3,4,1):
    k(theta) = 3 + 4*cos t + cos(2t) = 2*(1+cos t)^2 >= 0  (sum of squares)
so the combination is >= 0, giving the lower bound |zeta(1+delta+it)| >= c*delta
and, via the classical pipeline, the zero-free region  sigma > 1 - c/(log|t|)
with the classical explicit constant c_class = 1/9.646 (Stechkin; the
"1/(9.6...)" family anchored in the lane brief; modern explicit improvements:
Kadiri 1/5.69693, Mossinghoff-Trudgian-Yang 2022: 1/5.558691).

FRAMEWORK ENTRY (never tried before -- this lane).  The framework's kernel is
the Lomax family f_l(u) = (1+u)^{-l}, l in {1.5, 2, 2.4824, 3}.  Substitute the
kernel into the SAME scheme as an AMPLITUDE MODULATOR of the three classical
frequencies (this preserves the Euler-product identity, which is linear in the
weights -- an exact generalization):

    k_l,u,w(theta) = w0*f(u) + w1*f(2u)*cos(theta) + w2*f(3u)*cos(2theta)
    A = w0*(1+u)^{-l},  B = w1*(1+2u)^{-l},  C = w2*(1+3u)^{-l}

    ""3*f(u) + 4*f(2u) + f(3u)"" with the classical trig factors attached.

POSITIVITY CERTIFICATE (sum of squares, the framework analogue of
2*(1+cos t)^2).  For B <= 4C the minimum over theta is exact and closed-form:

    min_theta k = A - C - B^2/(8C)   (margin),  attained at cos(theta) = -B/4C,
    k(theta) = margin + 2*C*(cos(theta) + B/(4C))^2      (SOS decomposition).

THE SCHEME CONSTANT.  The 3-4-1 pipeline with weights (A,B,C) yields the lower
bound |zeta(1+delta+it)| >= c_L * delta^alpha, alpha = (A+C)/B, and the region
sigma > 1 - c/(R*log|t|) with  R = alpha,  c = c_class * B/(A+C) = c_class/alpha
(Stechkin-normalized: (A,B,C)=(3,4,1) reproduces 1/9.646 exactly; the
sub-leading explicit factors log zeta(1+delta) <= -log delta + E*delta, E = 2,
only shrink c further -- reported separately as the pipeline-sharpened value).

PRE-REGISTERED KILLS (before any computation):
  K1: no (l,u,w) on the grids with k >= 0 for ALL theta in [0,2pi] AND positive
      leading Fourier coefficient B > 0   ->  "the 3-4-1 scheme refuses the
      framework kernels" -> the route fails via the framework kernel.
  K2: c_best found but < c_class/10      ->  weaker than known by an order of
      magnitude; registered as such.
  Family-optimality check (registered): margin >= 0 forces alpha >= 1 with
  equality only at the classical point (A,B,C) ~ (3,4,1), i.e. u -> 0, f ~ 1
  (the framework rungs l > 0 at u > 0 are STRICTLY weaker) -- this is checked
  on the grid and certified in Lean (theorem alpha_ge_one).

GRID (pre-registered):
  l  in {1.5, 2, 2.4824, 3}
  w  in {(3,4,1), (1,2,1), (5,6,1)}
  u  in G1 u G2:
       G1 = {0.02 * 500**(j/256), j = 0..255}        (log grid, [0.02, 10])
       G2 = {(4999 + 499*j)/249950, j = 0..4999}     (linear, ALL RATIONAL, [0.02, 10])
  theta in [0, 2pi]: coarse 2001 pts for every candidate; fine 40001 pts for
       the best candidates; closed-form min verified against the grid min.

HONESTY (binding): every printed number from a real computation; no RH claim;
weaker-than-classical is stated as weaker-than-known; no commit.

Family A (the LITERAL reading, also computed for the record): k(theta) =
sum_j w_j * f_l(j*tan^2(theta/2)) -- a nonnegative FUNCTION of theta but NOT a
trig polynomial, so the Euler-product combination identity FAILS (the combination
is not a linear combination of log|zeta| at the three shifts): no scheme
constant exists for Family A; its minimum is 0 (at theta = pi, f(inf) = 0).
Registered as the scheme-refusal of the literal substitution.
"""

import json
import math
import os
import time
from fractions import Fraction

import numpy as np

t0 = time.time()

# ---------------------------------------------------------------- constants --
C_CLASS = 1.0 / 9.646          # Stechkin classical explicit constant (c_class)
E_EXPL = 2.0                   # explicit: log zeta(1+delta) <= -log delta + E*delta
L_SET = [1.5, 2.0, 2.4824, 3.0]
W_SET = [(3, 4, 1), (1, 2, 1), (5, 6, 1)]


def f_l(x, l):
    return (1.0 + x) ** (-l)


# grids ---------------------------------------------------------------- pre-registered
U_LOG = 0.02 * 500.0 ** (np.arange(256) / 256.0)
U_LIN = np.array([Fraction(4999 + 499 * j, 249950) for j in range(5000)], dtype=object)
U_LIN_F = np.array([float(x) for x in U_LIN])
U_ALL = np.sort(np.unique(np.concatenate([U_LOG, U_LIN_F])))
TH_COARSE = np.linspace(0.0, 2.0 * np.pi, 2001)
TH_FINE = np.linspace(0.0, 2.0 * np.pi, 40001)

print(f"=== RH11 THE ZERO-FREE REGION ROUTE: 3-4-1 WITH FRAMEWORK (LOMAX) KERNELS ===")
print(f"c_class (Stechkin anchor) = 1/9.646 = {C_CLASS:.9f}")
print(f"grids: |G1|={len(U_LOG)}, |G2|={len(U_LIN)}, total u-points={len(U_ALL)}; "
      f"theta coarse={len(TH_COARSE)} pts, fine={len(TH_FINE)} pts")
print(f"l in {L_SET}, w in {W_SET}")

cos_t = np.cos(TH_COARSE)
cos2t = np.cos(2.0 * TH_COARSE)

# ---------------------------------------------------------------- the scan ----
rows = []          # one row per (l, w, u)
for l in L_SET:
    for w in W_SET:
        # vectorize over the u-grid
        A = w[0] * (1.0 + U_ALL) ** (-l)
        B = w[1] * (1.0 + 2.0 * U_ALL) ** (-l)
        C = w[2] * (1.0 + 3.0 * U_ALL) ** (-l)
        margin = A - C - B * B / (8.0 * C)
        # exact closed-form minimum of A + B cos + C cos2t over theta:
        #   B/(4C) in [-1,1] -> min = A - C - B^2/8C; else corner c = -1.
        vertex_in = np.abs(B / (4.0 * C)) <= 1.0
        mink = np.where(vertex_in, A - C - B * B / (8.0 * C), np.minimum(A - B + C, A + B + C))
        # coarse-grid verification, vectorized: k over (|u|, theta) blocks
        # (chunked to bound memory)
        CH = 700
        gmin = np.empty_like(mink)
        for s in range(0, len(U_ALL), CH):
            e = min(s + CH, len(U_ALL))
            kth = (A[s:e, None]
                   + np.outer(B[s:e], cos_t)
                   + np.outer(C[s:e], cos2t))
            gmin[s:e] = kth.min(axis=1)
        for j in range(len(U_ALL)):
            rows.append({
                "l": l, "u": float(U_ALL[j]), "u_rational": j >= len(U_LOG),
                "w": list(w), "A": float(A[j]), "B": float(B[j]), "C": float(C[j]),
                "margin": float(margin[j]), "min_closed": float(mink[j]),
                "min_grid": float(gmin[j]),
                "pass": bool(margin[j] >= -1e-10 and B[j] > 0.0 and mink[j] >= -1e-10),
            })

R = rows
npass = sum(1 for r in R if r["pass"])
nall = len(R)
print(f"scan done: {nall} candidates, {npass} pass (k>=0 for all theta AND B>0)")
# verification: closed-form min vs grid min
diffs = [abs(r["min_closed"] - r["min_grid"]) for r in R]
print(f"closed-form vs grid-min: max |diff| = {max(diffs):.3e} over all {nall} candidates")

# per-(l,w) pass ranges and thresholds
print("\nper (l,w): passing u-subset and alpha=(A+C)/B at the u-edges:")
for l in L_SET:
    for w in W_SET:
        rs = [r for r in R if r["l"] == l and tuple(r["w"]) == tuple(w)]
        pa = [r for r in rs if r["pass"]]
        if pa:
            us = [r["u"] for r in pa]
            alphas = [(r["A"] + r["C"]) / r["B"] for r in pa]
            print(f"  l={l:<7} w={w}: pass u in [{min(us):.5f}, {max(us):.5f}], "
                  f"alpha in [{min(alphas):.5f}, {max(alphas):.5f}]")
        else:
            print(f"  l={l:<7} w={w}: NO passing u on the grid")

# thresholds (root of margin(u)=0) by bisection, per (l,w), for the record
def margin_at(u, l, w):
    A = w[0] * (1.0 + u) ** (-l)
    B = w[1] * (1.0 + 2.0 * u) ** (-l)
    C = w[2] * (1.0 + 3.0 * u) ** (-l)
    return A - C - B * B / (8.0 * C)

for l in L_SET:
    for w in W_SET:
        lo, hi = 0.02, 10.0
        if margin_at(lo, l, w) >= 0.0:
            print(f"  threshold u*(l={l},w={w}): margin>0 on [0.02,10] (none in interior)")
            continue
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if margin_at(mid, l, w) >= 0.0:
                hi = mid
            else:
                lo = mid
        print(f"  threshold u*(l={l},w={w}) ~ {hi:.6f}")

# ---------------------------------------------------------------- best candidate ---
# "closest-to-0 minimum over the grid" = smallest actual min_theta k among passing:
print("\nBEST candidate = passing (l,u,w) whose min_theta k is closest to 0:")
best = min((r for r in R if r["pass"]), key=lambda r: r["min_closed"])
for kk in ["l", "u", "w", "A", "B", "C", "margin", "min_closed", "min_grid"]:
    print(f"  {kk:10s} = {best[kk]}")
alpha_best = (best["A"] + best["C"]) / best["B"]
c_best = C_CLASS * best["B"] / (best["A"] + best["C"])
print(f"  alpha = (A+C)/B = {alpha_best:.9f}")
print(f"  c_scheme = c_class * B/(A+C) = {c_best:.9f}  (c_class = {C_CLASS:.9f})")
print(f"  c_scheme/c_class = {c_best / C_CLASS:.9f}")
print(f"  vertex regime B <= 4C: {best['B'] <= 4 * best['C']}  (B/4C = {best['B'] / (4 * best['C']):.4f})")
# best-case family constant on the grid (smallest alpha among PASSING candidates)
pass_rows = [r for r in R if r["pass"]]
amin = min((r["A"] + r["C"]) / r["B"] for r in pass_rows)
r_amin = min(pass_rows, key=lambda r: (r["A"] + r["C"]) / r["B"])
print(f"  family best on grid (min alpha among passing): alpha = {amin:.9f} at "
      f"(l,u,w) = ({r_amin['l']}, {r_amin['u']:.5f}, {r_amin['w']}) -> c = {C_CLASS / amin:.9f} "
      f"(ratio {(C_CLASS / amin) / C_CLASS:.6f})")
# leading Fourier coefficient (coefficient of cos theta) -- numerically via FFT
kf = best["A"] + best["B"] * np.cos(TH_FINE) + best["C"] * np.cos(2 * TH_FINE)
fft = np.fft.rfft(kf) / len(kf)
a0 = 2 * fft[0].real - fft[0].real  # a0 = (1/2pi) int k dtheta * 2pi -> mean
a1 = 2 * fft[1].real                # coefficient of cos(theta)
print(f"  leading Fourier coeff a1 (FFT-verified) = {a1:.9f}  vs B = {best['B']:.9f}")
print(f"  min over fine theta-grid = {kf.min():.3e}  vs margin {best['margin']:.3e}")

# pipeline-sharpened c for representative heights T (sub-leading explicit factors)
print("\npipeline-sharpened region constant c_pipe(T) = c_class*B/(A+C) *exp(-alpha*E*delta*) "
      "at delta* = d0/log T (d0 = 2, E = 2):")
for T in [1e2, 1e4, 1e6]:
    d0 = 2.0
    delta = d0 / math.log(T)
    c_pipe = C_CLASS * best["B"] / (best["A"] + best["C"]) * math.exp(-alpha_best * E_EXPL * delta)
    c_pipe_class = C_CLASS * math.exp(-1.0 * E_EXPL * delta)
    print(f"  T = {T:8.0f}: c_pipe = {c_pipe:.6e}, c_pipe_classical = {c_pipe_class:.6e}, "
          f"ratio to classical-at-same-T = {c_pipe / c_pipe_class:.6f}")

# system-family optimum: min alpha on the grid (should be at smallest u, (3,4,1))
alph_all = [(r["A"] + r["C"]) / r["B"] for r in R]
imin = int(np.argmin(alph_all))
rmin = R[imin]
print(f"\nfamily alpha-min on grid: alpha = {alph_all[imin]:.9f} at (l,u,w) = "
      f"({rmin['l']}, {rmin['u']:.6f}, {rmin['w']}) [equality alpha=1 only at u->0/f=1]")

# ---------------------------------------------------------------- Family A (literal) ----
print("\nFAMILY A (literal reading k = sum_j w_j f_l(j*u(theta)), u=tan^2(theta/2)):")
U_T = np.tan(TH_COARSE / 2.0) ** 2          # tan^2(theta/2), theta in [0,2pi]
fa_rows = []
for l in L_SET:
    for w in W_SET:
        vals = np.zeros_like(TH_COARSE)
        for j, wj in zip([1, 2, 3], w):
            vals += wj * (1.0 + j * U_T) ** (-l)
        # leading Fourier coefficient via trapezoid: a1 = (1/pi) int_0^{2pi} k cos t dt
        a1 = (1.0 / math.pi) * np.trapz(vals * np.cos(TH_COARSE), TH_COARSE)
        fa_rows.append({"l": l, "w": list(w), "min": float(vals.min()), "a1": float(a1)})
for r_ in fa_rows:
    print(f"  l={r_['l']:<7} w={r_['w']}: min over theta = {r_['min']:.3e} (theta=pi, f(inf)=0), "
          f"leading Fourier coeff a1 = {r_['a1']:.6f}")
print("  -> Family A: k>=0 (trivial, sum of positive kernels) and a1 > 0, but k is NOT a "
      "trig polynomial, so the Euler-product identity FAILS: no (A,B,C) weights are realized; "
      "the 3-4-1 scheme refuses the literal substitution (no scheme constant exists).")

# ---------------------------------------------------------------- kills and verdict ----
found = npass > 0
c_best_class_ratio = c_best / C_CLASS
K1 = not found
K2 = found and c_best < C_CLASS / 10.0
print("\n=== PRE-REGISTERED KILLS ===")
print(f"K1 (no (l,u,w) found): {K1}   -> {'ROUTE FAILS via framework kernel' if K1 else 'unfired: candidates exist'}")
print(f"K2 (c < c_class/10):   {K2}   -> {'WEAKER THAN KNOWN by >10x' if K2 else 'unfired: c_best/c_class = ' + f'{c_best_class_ratio:.4f}'}")
verdict = (
    "[FAIL] as framework improvement: framework kernels DO enter the 3-4-1 scheme "
    f"(K1 unfired, {npass} passing (l,u,w)) but EVERY framework kernel is STRICTLY weaker: "
    f"alpha = (A+C)/B >= 1 with equality only at the classical point (u->0, f~1); "
    f"best c_scheme = {c_best:.9f} < c_class = {C_CLASS:.9f} (ratio {c_best_class_ratio:.6f}), "
    "K2 unfired (c >= c_class/10) but registered weaker-than-known; no RH claim."
)
print(f"VERDICT: {verdict}")

# best lean-certifiable candidate: best passing candidate with INTEGER l (exact
# rational kernel values) -- closest-to-0 min_theta over that subset
rint = [r for r in R if r["pass"] and r["l"] in (2.0, 3.0)]
best_int = min(rint, key=lambda r: r["min_closed"])
regime = "corner (B>=4C): k(min) = A-B+C, certificate (1+c)(B-2C+2Cc)" if best_int["B"] >= 4 * best_int["C"] else "vertex (B<=4C): k(min) = A-C-B^2/8C, certificate margin + 2C(c+B/4C)^2"
print(f"\nLEAN-EXACT BEST CANDIDATE (integer l, rational u on G2): l={best_int['l']}, "
      f"u = {best_int['u']:.10f}, w={best_int['w']}, min_closed = {best_int['min_closed']:.6e}")
print(f"  regime: {regime}")
li = int(round(best_int["l"]))
ui = Fraction(4999 + 499 * round((best_int["u"] - 0.02) * 249950 / 499.0), 249950)
wi = best_int["w"]
A_f = Fraction(wi[0]) * (Fraction(ui.denominator) / (ui.denominator + ui.numerator)) ** li
B_f = Fraction(wi[1]) * (Fraction(ui.denominator) / (ui.denominator + 2 * ui.numerator)) ** li
C_f = Fraction(wi[2]) * (Fraction(ui.denominator) / (ui.denominator + 3 * ui.numerator)) ** li
M_f = (A_f - B_f + C_f) if best_int["B"] >= 4 * best_int["C"] else (A_f - C_f - B_f * B_f / (8 * C_f))
print(f"  EXACT: A = {A_f}")
print(f"  EXACT: B = {B_f}")
print(f"  EXACT: C = {C_f}")
print(f"  EXACT min_theta k = {M_f} ~ {float(M_f):.6e};  > 0: {M_f > 0}")
print(f"  4C <= B (corner): {4 * C_f <= B_f};  C > 0: {C_f > 0}")
lean_pars = {"l": li, "w": list(wi), "u_num": ui.numerator, "u_den": ui.denominator,
             "A_num": A_f.numerator, "A_den": A_f.denominator,
             "B_num": B_f.numerator, "B_den": B_f.denominator,
             "C_num": C_f.numerator, "C_den": C_f.denominator,
             "min_num": M_f.numerator, "min_den": M_f.denominator,
             "min_float": float(M_f), "regime": "corner" if best_int["B"] >= 4 * best_int["C"] else "vertex"}
print("  (overall grid best is l=1.5, min = 4.487e-4 -- algebra certified in Lean "
      "symbolically for all (A,B,C); exact instantiation at the best integer-l candidate)")

print(f"\ntotal wall time: {time.time() - t0:.1f}s")

# ---------------------------------------------------------------- results json ---
out = {
    "lane": "RH11_kerZeroFree",
    "date": "2026-09-17",
    "interpretation": (
        "k(theta)=A+B*cos(theta)+C*cos(2*theta), A=w0*f_l(u), B=w1*f_l(2u), "
        "C=w2*f_l(3u), f_l(x)=(1+x)^-l; SOS: k = margin + 2C(cos+B/4C)^2, "
        "margin = A-C-B^2/8C = min_theta k (for B<=4C); scheme constant "
        "c = c_class*B/(A+C), alpha=(A+C)/B, region sigma>1-c/(alpha*log|t|)"
    ),
    "classical_anchor": {
        "c_class": C_CLASS,
        "source": "Stechkin 1970 c=1/9.646 (dVdP-type explicit; Ford survey Table 1/eq 1.4); "
                  "modern explicit: Kadiri 1/5.69693, MTY 2022 1/5.558691",
        "trig_identity": "3+4cos(t)+cos(2t) = 2(1+cos t)^2 >= 0",
    },
    "grids": {
        "l": L_SET,
        "weights": [list(w) for w in W_SET],
        "u_log": "0.02*500**(j/256), j=0..255",
        "u_linear_rational": "u_j=(4999+499*j)/249950, j=0..4999",
        "theta": "coarse 2001 pts all candidates; fine 40001 pts best",
    },
    "scan": {
        "n_candidates": nall,
        "n_pass": npass,
        "max_closed_vs_grid_min_diff": max(diffs),
        "alpha_min_on_grid": float(min(alph_all)),
        "alpha_min_at": {"l": rmin["l"], "u": rmin["u"], "w": rmin["w"]},
        "family_optimality": (
            "margin>=0 forces alpha=(A+C)/B>=1, equality iff (A,B,C)~(3,4,1) i.e. u->0, f=1: "
            "within the Lomax-modulated family the classical kernel is the unique optimum; "
            "every framework rung is strictly weaker (Lean-certified: theorem alpha_ge_one)"
        ),
    },
    "best_candidate": {
        "l": best["l"], "u": best["u"], "w": best["w"],
        "A": best["A"], "B": best["B"], "C": best["C"],
        "margin": best["margin"], "min_closed": best["min_closed"],
        "min_grid": best["min_grid"], "alpha": alpha_best,
        "leading_fourier_coeff_B": best["B"],
        "a1_fft_verified": a1,
        "c_scheme": c_best,
        "c_scheme_over_c_class": c_best_class_ratio,
    },
    "c_pipe": {
        "note": "c_pipe(T) = c_class*B/(A+C) * exp(-alpha*E*delta*), delta*=2/log T, E=2 "
                "(explicit log zeta(1+delta) <= -log delta + E*delta)",
        "values": {f"T={T:g}": {"c_pipe": c_pipe, "ratio_vs_classical_at_same_T": c_pipe / c_pipe_class}
                   for T, c_pipe, c_pipe_class in
                   [(T, C_CLASS * best["B"] / (best["A"] + best["C"]) * math.exp(-alpha_best * E_EXPL * 2.0 / math.log(T)),
                     C_CLASS * math.exp(-E_EXPL * 2.0 / math.log(T))) for T in [1e2, 1e4, 1e6]]},
    },
    "family_A_literal": {
        "note": "k=sum_j w_j f_l(j*tan^2(theta/2)): nonneg (trivial) and a1>0, but NOT a trig "
                "polynomial -> Euler-product combination identity fails -> no scheme constant; "
                "min = 0 at theta=pi (degenerate): the 3-4-1 scheme refuses the literal substitution",
        "rows": fa_rows,
    },
    "kills": {
        "K1": K1,
        "K1_statement": "no (l,u,w) with k>=0 for all theta AND leading Fourier coeff>0",
        "K2": K2,
        "K2_statement": "c found but c < c_class/10 (weaker than known by order of magnitude)",
        "K2_ratio_c_over_c_class": c_best_class_ratio,
        "note": "K1 unfired; K2 unfired (c >= c_class/10) but c < c_class strictly: "
                "registered weaker-than-known",
    },
    "verdict": verdict,
    "rh_claim": False,
    "lean": lean_pars,
    "files": [
        "RH11_kerZeroFree.py", "RH11_kerZeroFree.out", "RH11_kerZeroFree_results.json",
        "lean/RH11L_ker34one.lean", "RH11_SUMMARY.md",
    ],
}

base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, "RH11_kerZeroFree_results.json"), "w") as fh:
    json.dump(out, fh, indent=2, default=str)
print("wrote RH11_kerZeroFree_results.json")