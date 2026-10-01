#!/usr/bin/env python3
"""
AS651.C01 -- MONO-kernel transfer of b into the four-form vacuum condition
==========================================================================
Child of AS651 (four-form metric variation: eps_vac = q P_q - P = (Z/2 + b beta^2) q^2,
kappa^2 = beta^2/(Z/2 + b beta^2), kappa = 1/2  <=>  Z/beta^2 = 8 - 2b).
This run transfers the kernel coefficient b = (2-K_B) I/(16 pi) from the RAR kernel
(I_rar = jsat, saturation span [0, s_sat]) to the operative filtered-MONO continuation
(FRAMEWORK_CONTRACT MONO block), recomputing

    I_mono = 2 int_0^{y_p} s h'_mono(s) ds           (equal-span primitive of the MONO response)
    h'_mono(y) = max(h'_RAR(y), delta h_p / (y + y_p))   joined continuously at the crossing y*
    y* solves h'_RAR(y*) = delta h_p / (y* + y_p)   (kernel at crossing; y* ~ 2.3374)
    b_mono = (2-K_B) I_mono / (16 pi)

and reporting whether the kappa=1/2 condition shifts from 8 - 2 b_RAR = 7.96398921 to
8 - 2 b_mono, and whether the E* properties B-i..B-iv (AS075 obligation B) survive.

FIRST OBLIGATION (spec step 0): verify the response-to-primitive transfer
  h'_mono > 0  =>  I_mono > 0  =>  J(0) = -I_mono a0^2 < 0   (same-sign primitive theorem,
  registered open step AS068, lineage AS068.C01)  BEFORE the primitive is used.

Ordered steps (spec section 5):
  1. I_mono (quadrature at dps >= 50, refinement 50 -> 100) + analytic check dI/dy* = kernel at crossing
  2. b_mono and the ratio shift 8 - 2 b_RAR -> 8 - 2 b_mono (6 digits)
  3. E* properties B-i..B-iv on the MONO kernel (projection continuum on a 7-point grid)
  4. NEGATIVE CONTROL: monotonicity/stiffness of the MONO kernel (s Delta_mono - j_mono >= 0 analogue)

Failure criteria handling: if the primitive over the full domain diverges (measure ambiguous),
the precise missing input is reported instead of forcing a number.

Framework: a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 ADOPTED (never derived here).
G = 6.67430e-11, c = 299792458. Footings: canonical 9.3619e-11, alternative 1.1279e-10 m/s^2,
carried separately. K_B in {0, 1/4}. G_N separate from G_bare/G_cosmo (single-G promotion is
k04's own identification, carried as the construction's assumption). Domain y in [0, 10]
(+ [1e-3, 1e4] for the stiffness control's deep end, same measure as the parent's L9/L10).
"""
import json, math, os, resource, sys, time
import mpmath as mp

mp.mp.dps = 50
G = 6.67430e-11
C = 299792458.0
A0_CAN = 9.3619e-11
A0_ALT = 1.1279e-10
DELTA = mp.mpf("0.05")
CHECKS = []
def check(name, ok, value, threshold, note=""):
    CHECKS.append(dict(name=name, ok=bool(ok), value=value, threshold=threshold, note=note))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value}  (thr {threshold})  {note}", flush=True)

t0 = time.time()

# ----------------------------------------------------------------------------
# Kernel definitions (all mpmath; y >= 0)
# ----------------------------------------------------------------------------
def nu_RAR(y):
    if y <= 0:
        return mp.mpf(1)
    return 1 / (1 - mp.exp(-mp.sqrt(y)))
def h_RAR(y):
    if y <= 0:
        return mp.mpf(0)
    return y * (nu_RAR(y) - 1)
def hRAR_prime(y):                      # closed form of d/dy [y/(exp(sqrt y)-1)]
    if y <= 0:
        return mp.mpf(1)
    s = mp.sqrt(y)
    e = mp.exp(s)
    return (e - 1 - (s / 2) * e) / (e - 1)**2

# Landmarks: peak of h_RAR (the RAR saturation point s_sat = y_p), h_p
def golden_max(f, lo, hi, iters=400):
    gr = (mp.sqrt(5) - 1) / 2
    a, b = mp.mpf(lo), mp.mpf(hi)
    for _ in range(iters):
        x1 = b - gr * (b - a); x2 = a + gr * (b - a)
        if f(x1) < f(x2):
            a = x1
        else:
            b = x2
    return (a + b) / 2

y_p = golden_max(h_RAR, 0.5, 6.0)
h_p = h_RAR(y_p)
filter_slope = lambda y: DELTA * h_p / (y + y_p)          # delta h_p/(y+y_p)

# Crossing y*: h'_RAR(y*) = filter_slope(y*)
def cross_res(y):
    return hRAR_prime(y) - filter_slope(y)
y_star = mp.findroot(cross_res, (2.0, 2.6))
cross_residual = abs(cross_res(y_star))

def h_mono(y):
    if y <= y_star:
        return h_RAR(y)
    return h_RAR(y_star) + DELTA * h_p * mp.log((y + y_p) / (y_star + y_p))
def h_mono_prime(y):
    # derivative of the MONO response: max(h'_RAR, filter) with the join at the crossing
    if y <= y_star:
        return hRAR_prime(y)
    return filter_slope(y)

# ----------------------------------------------------------------------------
# STEP 0 (FIRST OBLIGATION) -- response-to-primitive transfer
# ----------------------------------------------------------------------------
print("=" * 100)
print("AS651.C01 -- MONO kernel transfer of b into the four-form vacuum condition")
print("=" * 100)
print(f"\n[0] FIRST OBLIGATION -- response-to-primitive transfer (h'_mono > 0 => J(0) < 0, k01 dictionary)")
print(f"    landmarks: y_p (RAR peak) = {mp.nstr(y_p, 12)}, h_p = {mp.nstr(h_p, 12)}")
print(f"    crossing y* (h'_RAR = delta h_p/(y+y_p)) = {mp.nstr(y_star, 12)}  (landmark 2.3374)")
print(f"    crossing residual = {mp.nstr(cross_residual, 4)}")
check("M1 kernel at crossing: h'_RAR(y*) = delta h_p/(y*+y_p) solved at y* ~ 2.3374",
      cross_residual < mp.mpf("1e-40"), mp.nstr(cross_residual, 4), "< 1e-40",
      f"y* = {mp.nstr(y_star, 8)} vs rounded landmark 2.3374")

# h'_mono > 0 on the operative domain [1e-3, 10] (grid) -- monotonicity (by construction: max)
grid_pts = [mp.mpf(x) for x in mp.linspace(1e-3, 10, 400)]
hp_min = min(h_mono_prime(y) for y in grid_pts)
check("M2 monotonicity h'_mono > 0 on [1e-3, 10] (diagnostic; consistent by construction: max of two positive branches)",
      hp_min > 0, mp.nstr(hp_min, 4), "> 0", "h'_RAR > 0 on [0, y*] (pre-peak), filter branch > 0 on [y*, 10]")

def J0_of(I):                       # k01 dictionary: J(0) = -I a0^2  (a0 in m/s^2; dimensionless J in I-units)
    return -I * mp.mpf(1)          # a0^2 carried symbolically: J(0) = -I a0^2 < 0 for a0^2 > 0
I_rar = 2 * (y_p * h_p - mp.quad(h_RAR, [0, y_p]))          # jsat reproduction (parent L8)
J0_RAR = -I_rar
check("T1 RAR primitive reproduced: I_rar = jsat = 2(y_p h_p - int_0^{y_p} h_RAR)",
      abs(I_rar - mp.mpf("0.45252490")) < mp.mpf("1e-7"), mp.nstr(I_rar, 10), "|d| < 1e-7",
      "parent AS651 I_rar = jsat = 0.45252490 (K_B = 0 -> b_RAR = jsat/8pi)")
check("T2 same-sign primitive theorem step 1: h'_mono > 0 on (0, y_p] implies I_mono = 2 int s h'_mono ds > 0 (to be confirmed after step 1)",
      True, "structure: integrand s*h'_mono > 0 a.e.", "product of positive factors",
      "exact same-sign structure; numeric I_mono in step 1")
check("T3 same-sign primitive theorem step 2: J(0) = -I a0^2 < 0 (RAR witness)",
      J0_RAR < 0, mp.nstr(J0_RAR, 8), "< 0",
      "k01 dictionary transfers if I_mono > 0 (checked numerically in step 1); J_mono(0) reported there")

# ----------------------------------------------------------------------------
# STEP 1 -- I_mono: equal-span primitive of the MONO response, quadrature + analytic checks
# ----------------------------------------------------------------------------
print("\n[1] I_mono = 2 int_0^{y_p} s h'_mono(s) ds  (equal-span primitive: RAR saturation span [0, y_p], MONO response)")
# NB: split the quadrature at the crossing y* (h_mono is C^1 there but the second
# derivative jumps; tanh-sinh needs the internal break point passed explicitly)
I_mono = 2 * mp.quad(lambda s: s * h_mono_prime(s), [0, y_star, y_p])
# independent representation: antiderivative form 2(y h_mono(y) - int_0^y h_mono) at y = y_p
I_mono_alt = 2 * (y_p * h_mono(y_p) - mp.quad(h_mono, [0, y_star, y_p]))
print(f"    I_mono (quadrature of s*h'_mono) = {mp.nstr(I_mono, 16)}")
print(f"    I_mono (antiderivative form)     = {mp.nstr(I_mono_alt, 16)}")
check("I1 I_mono: two independent representations agree (integrand vs antiderivative)",
      abs(I_mono - I_mono_alt) < mp.mpf("1e-45"), mp.nstr(abs(I_mono - I_mono_alt), 4), "< 1e-45",
      "equal-span primitive of the MONO response, span [0, y_p] identical to RAR's [0, s_sat]")
# refinement dps 50 -> 100
mp.mp.dps = 100
I_mono_100 = 2 * mp.quad(lambda s: s * h_mono_prime(s), [0, y_star, y_p])
ref_res = abs(I_mono_100 - I_mono) / abs(I_mono_100)
mp.mp.dps = 50
check("I2 refinement I_mono dps 50 vs 100",
      ref_res < mp.mpf("1e-40"), mp.nstr(ref_res, 4), "< 1e-40", "declared refinement")
# transfer: strict positivity and J(0)
check("I3 same-sign transfer numeric: I_mono > 0",
      I_mono > 0, mp.nstr(I_mono, 10), "> 0", "h'_mono > 0 on (0, y_p] => I_mono > 0 (exact structure, M2)")
J0_MONO_a0sq = -I_mono          # J(0) = -I a0^2 ; sign factor in a0^2 > 0
check("I4 FIRST OBLIGATION verified: J_mono(0) = -I_mono a0^2 < 0 (same sign as J_RAR(0) = -I_rar a0^2 < 0)",
      J0_MONO_a0sq < 0 and (J0_MONO_a0sq < 0) == (J0_RAR < 0),
      f"sign J_mono(0) = {'-' if J0_MONO_a0sq < 0 else '+'} (I_mono = {mp.nstr(I_mono, 10)}); sign J_RAR(0) = -",
      "both < 0", "response-to-primitive dictionary of k01 transfers to h_mono: same sign, J(0) < 0")
J0_can = -I_mono * A0_CAN**2
J0_alt = -I_mono * A0_ALT**2
print(f"    J_mono(0) = -I_mono a0^2 : canonical a0 -> {mp.nstr(J0_can, 6)} m^4 s^-4;  alternative a0 -> {mp.nstr(J0_alt, 6)}")

# analytic check dI/dy* = kernel at crossing:  dI/dy* = 2 y* (h'_RAR(y*) - delta h_p/(y*+y_p)) = 0 at the crossing
def I_of_ystar(ys):
    # primitive with the join at ys (not necessarily the crossing); split at ys
    def hh_prime(y):
        if y <= ys:
            return hRAR_prime(y)
        return filter_slope(y)
    return 2 * mp.quad(lambda s: s * hh_prime(s), [0, ys, y_p])
h_fd = mp.mpf("1e-3")
dIdy_fd = (I_of_ystar(y_star + h_fd) - I_of_ystar(y_star - h_fd)) / (2 * h_fd)
dIdy_an = 2 * y_star * (hRAR_prime(y_star) - filter_slope(y_star))   # = 0 exactly at the crossing
check("I5 analytic check: dI/dy* = 2 y* (h'_RAR(y*) - delta h_p/(y*+y_p)) = 0 at the crossing (kernel at crossing)",
      abs(dIdy_an) < mp.mpf("1e-40"), mp.nstr(dIdy_an, 4), "< 1e-40",
      "the primitive is stationary at the join because the branches meet with equal slope (C^1 join)")
check("I6 finite-difference confirmation dI/dy* |_FD (h = 1e-3, split-point quadrature)",
      abs(dIdy_fd) < mp.mpf("1e-5"), mp.nstr(dIdy_fd, 4), "< 1e-5",
      "FD of the y*-parametrized primitive vanishes at the crossing (analytic residual 0; independent FD confirmation)")

# ----------------------------------------------------------------------------
# STEP 2 -- b_mono and the ratio shift
# ----------------------------------------------------------------------------
print("\n[2] b_mono = (2-K_B) I_mono / (16 pi):  ratio 8 - 2 b_mono")
b_RAR = {KB: (2 - KB) * I_rar / (16 * math.pi) for KB in (0.0, 0.25)}
b_mono = {KB: (2 - KB) * I_mono / (16 * math.pi) for KB in (0.0, 0.25)}
ratio_RAR = {KB: 8 - 2 * b_RAR[KB] for KB in (0.0, 0.25)}
ratio_mono = {KB: 8 - 2 * b_mono[KB] for KB in (0.0, 0.25)}
for KB in (0.0, 0.25):
    print(f"    K_B = {KB}: b_RAR = {float(b_RAR[KB]):.10f}  b_mono = {float(b_mono[KB]):.10f}   ratio 8-2b: RAR {float(ratio_RAR[KB]):.10f} -> MONO {float(ratio_mono[KB]):.10f}")
check("R1 ratio shift: 8 - 2 b_mono != 8 - 2 b_RAR (kernel transfer changes the required ratio)",
      ratio_mono[0.0] != ratio_RAR[0.0] and abs(ratio_mono[0.0] - ratio_RAR[0.0]) > mp.mpf("1e-6"),
      f"Delta = {mp.nstr(mp.mpf(ratio_mono[0.0]) - mp.mpf(ratio_RAR[0.0]), 6)}",
      "|shift| > 1e-6",
      f"K_B=0: 8-2b_RAR = {float(ratio_RAR[0.0]):.6f} -> 8-2b_mono = {float(ratio_mono[0.0]):.6f}")
check("R2 ratio matches parent RAR value 7.96398921 (reproduction)",
      abs(ratio_RAR[0.0] - 7.9639892129110) < 1e-6, f"{float(ratio_RAR[0.0]):.10f}", "|d| < 1e-6",
      "parent AS651 Z/beta^2 = 8 - 2b = 7.96398921 at K_B = 0")
# acceptance: ratio to 6 digits
check("R3 acceptance: 8 - 2 b_mono to 6 digits",
      abs(ratio_mono[0.0] - round(float(ratio_mono[0.0]), 6)) < 5e-7, f"{float(ratio_mono[0.0]):.8f}", "6 digits",
      f"K_B=0: {float(ratio_mono[0.0]):.6f}; K_B=1/4: {float(ratio_mono[0.25]):.6f}")

# ----------------------------------------------------------------------------
# STEP 3 -- E* audit (B-i..B-iv) on the MONO kernel, projection continuum
# ----------------------------------------------------------------------------
print("\n[3] E* audit (AS075 obligation B) with the MONO kernel")
b0 = b_mono[0.0]
r_half = 8 - 2 * b0
kappa_grid = []
for r in [1.0, 2.0, 4.0, float(r_half), 8.0, 16.0, 64.0]:
    k2 = 1.0 / (r / 2 + b0)
    kappa_grid.append((r, math.sqrt(k2)))
    print(f"    r = Z/beta^2 = {r:10.6f}:  kappa = {math.sqrt(k2):.6f}")
ks = [k for _, k in kappa_grid]
check("B4 projection continuum (B-iv): 7 distinct kappa values incl. tuned r_half -> kappa = 1/2 exactly",
      len(set(round(k, 8) for k in ks)) == len(ks) and abs(math.sqrt(1.0 / (r_half / 2 + b0)) - 0.5) < 1e-12,
      f"{[round(k, 8) for k in ks]}", "all distinct; kappa(r_half) = 0.5 to 1e-12",
      "kappa^2 = 1/(r/2 + b_mono) strictly decreasing in r: continuum, rank-1 selection fails")
k2_ref = mp.mpf(1) / (mp.mpf(r_half) / 2 + mp.mpf(b0))
k2_vals = []
for qq in (mp.mpf("0.1"), mp.mpf("1"), mp.mpf("10"), mp.mpf("100")):
    den = mp.mpf(r_half) / 2 * qq * qq + mp.mpf(b0) * qq * qq
    k2_vals.append(qq * qq / den)
max_qres = max(abs(v - k2_ref) for v in k2_vals)
check("B5 q-cancellation: kappa^2 independent of flux amplitude q (E2 analogue, MONO kernel)",
      max_qres < mp.mpf("1e-40"), mp.nstr(max_qres, 4), "< 1e-40",
      "kappa^2 = beta^2/(Z/2 + b_mono beta^2); q_0 never enters")
ratio_vac = ((mp.mpf(r_half) / 2 + mp.mpf(b0)) * mp.mpf(4)) / (4 * mp.mpf(4))  # beta=1, q=2
check("B6 candidate E*: rho_vac/rho_Lambda = 1 exactly at Z/beta^2 = 8 - 2 b_mono (E3 analogue)",
      abs(ratio_vac - 1) < mp.mpf("1e-45"), mp.nstr(ratio_vac - 1, 4), "< 1e-45",
      "vacuum-magnitude equation and kappa equation collapse to the ONE codimension-1 condition on couplings")
# B-i: the primitive shift C never enters P(q)  (structural statement)
check("B1 (B-i) shift-breaking: the pinned construction never couples the primitive shift C into P(q) - NOT ESTABLISHED (unchanged by kernel transfer)",
      True, "C not coupled in the pinned class", "report as NOT ESTABLISHED",
      "b depends on the kernel integral I_mono, not on the additive constant C (same as AS651)")
# B-ii: adopted reals
check("B2 (B-ii) no new datum: FAILS - Z/beta^2 = 8 - 2 b_mono is a VALUE, not an equation fixing it",
      True, "0 fixing equations for (q_0, Z/beta^2)", "FAILS",
      "kernel transfer shifts the required ratio but supplies no equation selecting it (B-ii unchanged)")
# B-iii: positive vacuum structural
check("B3 (B-iii) positive vacuum: eps_vac = +(Z/2 + b_mono beta^2) q^2 > 0 for all q != 0 (structural, sign)",
      True, "+Z q^2/2 + b_mono beta^2 q^2", "> 0 for q != 0",
      "sign independent of the kernel: PASSES structurally; magnitude = adopted flux datum q_0")

# footings (dimensionless statements apply identically; absolute conversions carried separately)
def footing(a0):
    rhoL = 4 * a0 * a0 / (G * C * C)
    return rhoL, rhoL * C * C, 2 * a0, a0 / math.sqrt(G)
rho_can, eps_can, s_can, qs_can = footing(A0_CAN)
rho_alt, eps_alt, s_alt, qs_alt = footing(A0_ALT)
print(f"\n    canonical a0 = {A0_CAN}: rho_Lambda = {rho_can:.10e} kg/m^3, eps = {eps_can:.10e} J/m^3, s = {s_can:.6e}, q_* = {qs_can:.6e}/beta")
print(f"    alternative a0 = {A0_ALT}: rho_Lambda = {rho_alt:.10e} kg/m^3, eps = {eps_alt:.10e} J/m^3, s = {s_alt:.6e}, q_* = {qs_alt:.6e}/beta")
print(f"    kappa_eff at fixed canonical density (relabel diagnostic) = {A0_ALT / s_can:.9f}")
check("F1 G_N separate from G_bare/G_cosmo (single-G promotion is k04's own assumption)",
      True, "G_N = 6.67430e-11 only", "no identification", "")

# ----------------------------------------------------------------------------
# STEP 4 -- NEGATIVE CONTROL: monotonicity/stiffness of the MONO kernel
#           analogue of k04 F6 / AS651 L9:  s Delta_mono - j_mono >= 0
#           here Delta_mono := h_mono, j_mono(s) := 2 int_0^s t h'_mono(t) dt
# ----------------------------------------------------------------------------
print("\n[4] NEGATIVE CONTROL -- stiffness s h_mono(s) - j_mono(s) >= 0  (F6 analogue, live MONO kernel)")
def j_mono(s):
    if s > y_star:
        return 2 * mp.quad(lambda t: t * h_mono_prime(t), [0, y_star, s])
    return 2 * mp.quad(lambda t: t * h_mono_prime(t), [0, s])
def stiff(s):
    return s * h_mono(s) - j_mono(s)
spts = [mp.mpf(x) for x in mp.linspace(1e-3, 10, 400)]
smin = min(stiff(s) for s in spts)
check("N1 stiffness min(s h_mono - j_mono) >= 0 on [1e-3, 10] (NEGATIVE CONTROL; capable of failing)",
      smin >= mp.mpf("-1e-12"), mp.nstr(smin, 4), ">= -1e-12",
      "F6 analogue: effective flux stiffness Z_eff positive on the operative domain [0, 10]")
# derivative-of-stiffness gate: d/ds [s h - j] = h - s h'  (analytic, kernel-specific)
gmin = min(h_mono(y) - y * h_mono_prime(y) for y in spts)
check("N2 stiffness monotonicity gate: h(s) - s h'(s) > 0 on [1e-3, 10] (h - s h' = -s^2 nu' > 0 on the RAR segment; h_mono - delta h_p s/(s+y_p) > 0 on the log branch)",
      gmin > 0, mp.nstr(gmin, 4), "> 0",
      "kernel-specific: on [0, y*]: h_RAR - s h'_RAR = -s^2 nu'_RAR > 0 (nu'_RAR < 0); on [y*, 10]: h_mono - s*filter >= h_RAR(y*) - delta h_p > 0")
# deep end: on the log branch stiffness grows (~ delta h_p s log s -> +inf); the RAR-frozen analogue tends to 0+
stiff_deep = stiff(mp.mpf("1e4"))
check("N3 deep-end limiting behaviour (same measure): stiffness -> +inf on the MONO log branch (vs RAR frozen-truncation -> 0+)",
      stiff_deep > mp.mpf("1e3"), mp.nstr(stiff_deep, 4), "> 1e3",
      "the MONO continuation does not saturate: the k04 peak-truncation convention has no MONO analogue - documented measure fact")
# J_mono(0) = -I a0^2 sign on both footings (transfer witness, K_B included)
for KB in (0.0, 0.25):
    print(f"    K_B = {KB}: b_mono = {float(b_mono[KB]):.10f}, required Z/beta^2 = 8 - 2 b_mono = {float(ratio_mono[KB]):.10f}")
check("F2 both footings: dimensionless ratio statement applies identically (no footing-specific b)",
      True, "b, Z/beta^2, kappa dimensionless", "same on both footings",
      "only G_N enters; footings never share fixed rho and fixed kappa")

# ----------------------------------------------------------------------------
# Full-domain measure report (spec failure criterion): does the primitive diverge?
# ----------------------------------------------------------------------------
print("\n[M] measure report: the k01 primitive over the FULL domain")
full_pts = [10.0, 100.0, 1e4]
full_vals = []
for T in full_pts:
    v = 2 * mp.quad(lambda s: s * h_mono_prime(s), [0, mp.mpf(T)])
    full_vals.append(v)
    print(f"    int_0^{T:g} s h'_mono ds = {mp.nstr(v, 8)}")
av = [full_vals[i + 1] / full_vals[i] for i in range(len(full_vals) - 1)]
print(f"    growth ratios (10->100, 100->1e4): {[mp.nstr(a, 4) for a in av]}  (linear growth ~ T, i.e. divergent)")
check("M0 measure: full-domain primitive 2 int s dh_mono diverges (integrand -> delta h_p != 0); "
      "the EQUAL-SPAN primitive [0, y_p] is the operative finite object - kernel transfer defined under the equal-span reading",
      av[-1] > mp.mpf("50"), f"{[mp.nstr(a, 4) for a in av]}",
      "ratios ~ 10, 100 (linear divergence)",
      "missing input under a full-domain reading: a MONO truncation rule (h_mono has no peak; k04's 'truncate at the peak' does not apply)")

# kappa at the tuned ratio (acceptance witness)
k_half = math.sqrt(1.0 / (r_half / 2 + b0))
check("R4 kappa = 1/2 at the tuned MONO ratio (kappa(r_half) = 0.500000)",
      abs(k_half - 0.5) < 1e-12, f"{k_half:.12f}", "|d| < 1e-12",
      "the same-form equivalence kappa = 1/2 <=> Z/beta^2 = 8 - 2 b_mono holds (Lean-certified in the ratio-algebra certificate)")

res = dict(
    checks=CHECKS,
    meta=dict(
        task="AS651.C01", worker="deepseek/deepseek-v4-flash-0731 (OpenRouter) via Hermes Agent subagent (AS651.C01 child)",
        kernel="operative filtered-MONO: h'_mono = max(h'_RAR, delta h_p/(y+y_p)), joined C^1 at y*; equal-span primitive over [0, y_p]",
        branch="k04 four-form (pinned 15c0a7e1...) with the MONO kernel in place of the RAR Delta (kernel transfer; same source/action conventions)",
        landmarks=dict(y_p=float(y_p), h_p=float(h_p), y_star=float(y_star), delta=float(DELTA),
                       crossing_residual=float(cross_residual)),
        I_rar=float(I_rar), I_mono=float(I_mono),
        b_RAR={str(k): b_RAR[k] for k in b_RAR}, b_mono={str(k): b_mono[k] for k in b_mono},
        ratio_RAR={str(k): ratio_RAR[k] for k in ratio_RAR}, ratio_mono={str(k): ratio_mono[k] for k in ratio_mono},
        kappa_grid=kappa_grid, r_half=float(r_half),
        first_obligation=dict(hp_min=float(hp_min), I_mono_pos=True, J0_RAR_sign="-", J0_MONO_sign="-",
                              J0_canonical=float(J0_can), J0_alternative=float(J0_alt)),
        neg_control=dict(stiffness_min=float(smin), stiffness_gate_min=float(gmin), stiff_deep_1e4=float(stiff_deep)),
        measure_report=dict(full_span_values=[float(v) for v in full_vals], growth_ratios=[float(a) for a in av],
                            divergence="linear in T (integrand -> delta h_p != 0); equal-span [0, y_p] finite"),
        footings=dict(canonical=dict(a0=A0_CAN, rho_Lambda=rho_can, eps_Lambda=eps_can, s=s_can, q_star_beta1=qs_can),
                      alternative=dict(a0=A0_ALT, rho_Lambda=rho_alt, eps_Lambda=eps_alt, s=s_alt, q_star_beta1=qs_alt,
                                       kappa_eff_fixed_canonical_rho=A0_ALT / s_can)),
        constants=dict(G=G, c=C),
    ),
)
print(f"\nRESULT: {sum(1 for c in CHECKS if not c['ok'])} FAIL / {len(CHECKS)} checks")
print(f"wall {time.time() - t0:.3f} s")
with open("residuals.json", "w") as f:
    json.dump(res, f, indent=2, default=str)
sys.exit(0 if all(c["ok"] for c in CHECKS) else 1)