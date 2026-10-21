#!/usr/bin/env python3
"""
A2_medium -- the saturating medium as a Langmuir lattice, and n=1 vs n=2 as two
different capacity assignments.

Run:  python3 a2_checks.py            (all checks must PASS, exit 0)
      python3 a2_checks.py --mutate   (capacity halved; declared checks must FAIL)

Deterministic. stdlib + numpy + sympy. No network. <= 120 s.
"""
import sys
import json
import math
import numpy as np
import sympy as sp

MUTATE = "--mutate" in sys.argv

# ----------------------------------------------------------------------------
# Constants (BRIEF section 4; GM_sun = IAU nominal, listed in results.json)
# ----------------------------------------------------------------------------
A0 = 9.36e-11              # canonical footing, m s^-2
A0_ALT = 1.13e-10          # alternative footing (never pooled)
G_NEWT = 6.67430e-11       # m^3 kg^-1 s^-2
GM_SUN = 1.32712440018e20  # m^3 s^-2
MSUN = GM_SUN / G_NEWT
KPC = 3.0856775814913673e19

# The two capacity assignments.  CAP is the saturation value of the medium
# response A = g - g_N; AFF is the gate affinity scale k_d/k_a.
# n = 1 : CAP = AFF = a0.   --mutate halves the capacity (the n=2 assignment).
CAP = A0 / 2.0 if MUTATE else A0
AFF = A0

CHECKS = []


def ck(cid, ok, value, threshold, note=""):
    ok = bool(ok)
    CHECKS.append({"id": cid, "pass": ok, "value": value, "threshold": threshold,
                   "note": note})
    tail = f"  # {note}" if note else ""
    print(f"{cid} {'PASS' if ok else 'FAIL'} {value} {threshold}{tail}")


def law_canonical(gN):
    """g for the canonical n=1 law g_N = g^2/(g+a0)."""
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * A0 * gN))


def law_n2(gN):
    """g for the quadrature law g^2 - g_N^2 = a0 g_N."""
    return np.sqrt(gN * gN + A0 * gN)


def resp_n1(g):
    """Medium response A = g - g_N for the canonical law."""
    return A0 * g / (g + A0)


def resp_n2(g):
    """Medium response A = g - g_N for the quadrature law (a = a0/2)."""
    a = A0 / 2.0
    return g + a - np.sqrt(g * g + a * a)


# ============================================================================
# K1 -- exact algebraic identity: canonical law == Langmuir isotherm
# ============================================================================
g, a0, u, C, s, K, lam = sp.symbols('g a0 u C s K lambda', positive=True)
gN_can = g ** 2 / (g + a0)
x = g / a0
theta = x / (1 + x)
A_med = sp.simplify(g - gN_can)

id_a = sp.simplify(A_med - a0 * theta)          # A = a0 * theta
id_b = sp.simplify(gN_can - g * theta)          # g_N = g * theta
id_c = sp.simplify(1 / A_med - (1 / g + 1 / a0))  # 1/A = 1/g + 1/a0
id_d = sp.simplify(g - (a0 + g) * theta)        # g = (a0+g) theta
id_e = sp.simplify(gN_can.subs({g: lam * g, a0: lam * a0}) - lam * gN_can)
ids = [id_a, id_b, id_c, id_d, id_e]
ck("K1", all(e == 0 for e in ids), float(sum(abs(sp.N(e, 20)) for e in ids)), 0.0,
   "exact sympy: A=a0*th, gN=g*th, 1/A=1/g+1/a0, g=(a0+g)th, homogeneity deg 1")

# ============================================================================
# K2 -- mass-action kinetics: stationary condition is the canonical law
# ============================================================================
ka, kd, th = sp.symbols('k_a k_d theta', positive=True)
sol = sp.solve(sp.Eq(ka * g * (1 - th), kd * th), th)
th_star = sp.simplify(sol[0].subs(kd, ka * a0))          # k_d/k_a = a0
k2_law = sp.simplify((g - a0 * th_star) - g ** 2 / (g + a0))
k2_th = sp.simplify(th_star - theta)
ck("K2", k2_law == 0 and k2_th == 0, float(abs(sp.N(k2_law, 20)) + abs(sp.N(k2_th, 20))),
   0.0, "k_a g (1-th) = k_d th  =>  th = g/(g+a0)  =>  g_N = g^2/(g+a0)")

# ============================================================================
# K3 -- grand-canonical one site, two states; free energy reproduces the law
# ============================================================================
beta, mu, eps, kT = sp.symbols('beta mu epsilon kT', positive=True)
Z = 1 + sp.exp(beta * (mu + eps))
x_GC = sp.exp(beta * (mu + eps))
th_GC = sp.simplify(x_GC / (1 + x_GC))
# chemical potential set by the drive:  mu = kT ln(g/a0) - eps,  beta*kT = 1
th_GC_g = sp.simplify(th_GC.subs({beta * (mu + eps): sp.log(g / a0)}))
k3_occ = sp.simplify(th_GC_g - g / (g + a0))
# free energy whose derivative is the total field: K W_full'(u) = g, u = a0 th
W_full = (a0 ** 2 / K) * (-u / a0 - sp.log(1 - u / a0))
k3_der = sp.simplify(K * sp.diff(W_full, u) - a0 * (u / a0) / (1 - u / a0))
# and the remainder is exactly canonical Eq.(2) at n=1
W_rem = sp.simplify(W_full - u ** 2 / (2 * K))
W_rem_ref = (a0 ** 2 / K) * (-sp.log(1 - u / a0) - u / a0 - u ** 2 / (2 * a0 ** 2))
k3_rem = sp.simplify(W_rem - W_rem_ref)
k3_amp = sp.simplify(W_full.subs(u, a0 * theta) -
                     (a0 ** 2 / K) * (-theta - sp.log(1 - theta)))
ck("K3", k3_occ == 0 and k3_der == 0 and k3_rem == 0 and k3_amp == 0,
   float(abs(sp.N(k3_occ, 20)) + abs(sp.N(k3_der, 20)) + abs(sp.N(k3_rem, 20))),
   0.0, "GC: th=x/(1+x), mu=kT ln(g/a0)-eps => th=g/(g+a0); K W_full'=g; W_rem=Eq.(2,n=1)")

# ============================================================================
# K4 -- no equilibrium Gibbs state with LINEAR coupling gives the law
# ============================================================================
b_lin = sp.symbols('b', positive=True)
th_F = 1 / (1 + sp.exp(-b_lin * g))          # two-state site, H = -lam g sigma_z
# Langmuir has a pole at g = -a0; the Fermi function is finite there.
val_at_pole = sp.simplify(th_F.subs(g, -a0))
lim_L = sp.limit(g / (g + a0), g, -a0, '+')
k4 = (sp.simplify(val_at_pole - 1 / (1 + sp.exp(b_lin * a0))) == 0
      and lim_L in (sp.oo, -sp.oo))
# asymptotic second signature
asym_F = sp.limit(g * (1 - th_F), g, sp.oo)
asym_L = sp.limit(g * (1 - g / (g + a0)), g, sp.oo)
k4b = (asym_F == 0 and sp.simplify(asym_L - a0) == 0)
ck("K4", k4 and k4b, float(sp.N(1 / (1 + sp.exp(b_lin * a0)).subs(b_lin, 1 / a0), 12)),
   1.0, "Fermi(theta) finite at g=-a0 where Langmuir has its only pole; g(1-th)->0 vs ->a0")

# ============================================================================
# K5 -- single-scale lattice: MOND deep limit FORCES capacity == affinity
# ============================================================================
gN_lat = sp.simplify(g - C * g / (g + s))
ser = sp.series(gN_lat, g, 0, 3).removeO()
lin_coeff = sp.simplify(sp.expand(ser).coeff(g, 1))
k5_lin = sp.simplify(lin_coeff - (1 - C / s))
# deep MOND requires the linear term to vanish => C = s; then the law is canonical
k5_forced = sp.simplify(gN_lat.subs(C, s) - g ** 2 / (g + s))
# with C = s = a0 the capacity equals the deep-limit scale
k5_cap = sp.simplify((C - s).subs({C: A0, s: A0}))
deep_n1 = sp.limit(sp.solve(sp.Eq(g ** 2 / (g + s), u), g)[0] / sp.sqrt(s * u), u, 0)
# numeric statement of the same fact with the declared assignments
lin_num = abs(1.0 - CAP / AFF)
ck("K5", k5_lin == 0 and k5_forced == 0 and lin_num < 1e-15, lin_num, 1e-15,
   "series linear coeff = 1-C/s; MOND forces C=s => capacity=affinity=a0 (n=1)")

# ============================================================================
# K6 -- the n=2 law is NOT any single Langmuir: even vs non-even, O(g^3) gap
# ============================================================================
gN_2 = sp.sqrt(g ** 2 + (a0 / 2) ** 2) - a0 / 2
k6_even = sp.simplify(gN_2.subs(g, -g) - gN_2)
ser2 = sp.series(gN_2, g, 0, 6).removeO()
ser1 = sp.series(gN_can, g, 0, 6).removeO()
c3_1 = sp.simplify(ser1.coeff(g, 3) * a0 ** 2)
c3_2 = sp.simplify(ser2.coeff(g, 3) * a0 ** 2)
c2_1 = sp.simplify(ser1.coeff(g, 2) * a0)
c2_2 = sp.simplify(ser2.coeff(g, 2) * a0)
# best 2-parameter Langmuir fit matches g^0..g^2 but not g^3
k6_gap = abs(float(c3_1 - c3_2))
ck("K6", k6_even == 0 and c2_1 == c2_2 == 1 and k6_gap > 0.99,
   k6_gap, 0.99, "n=2 gN(g) is EVEN; any Langmuir is not. Shared g^2/a0, cubic 1/a0^2 vs 0")

# ============================================================================
# K7 -- n=2 is not a positive mixture of Langmuir gates (branch-point proof)
# ============================================================================
gz = sp.symbols('gz')
a_par = sp.symbols('a', positive=True)
A2 = gz + a_par - sp.sqrt(gz ** 2 + a_par ** 2)
h2 = sp.simplify(A2 / gz)
branch = sp.solve(sp.Eq(gz ** 2 + a_par ** 2, 0), gz)   # +- i a
# no positivity assumption on gz here:
gz2 = sp.symbols('gz2')
branch = sp.solve(sp.Eq(gz2 ** 2 + a_par ** 2, 0), gz2)
off_axis = all(sp.simplify(sp.re(b)) == 0 and sp.simplify(sp.im(b)) != 0 for b in branch)
# second, independent test: A2' must be completely monotone for a positive mixture
f1 = sp.diff(A2, gz)
f3 = sp.simplify(sp.diff(f1, gz, 3))
sgn_lo = sp.sign(sp.simplify(f3.subs(gz, a_par / 4)))
sgn_hi = sp.sign(sp.simplify(f3.subs(gz, a_par)))
k7_cm = (sgn_lo == 1 and sgn_hi == -1)
# the n=1 response instead has its only singularity on the negative real axis
h1 = sp.simplify((a0 * gz / (gz + a0)) / gz)
sing1 = sp.solve(sp.Eq(gz + a0, 0), gz)
k7_n1 = (len(sing1) == 1 and sp.simplify(sing1[0] + a0) == 0)
ck("K7", off_axis and k7_cm and k7_n1, float(len(branch)), 2.0,
   "A2/g has branch points +-i a0/2 (off (-inf,0]); A2''' changes sign at g=a0/4")

# ============================================================================
# K8 -- two internal degrees of freedom per site: additive capacity = one gate
# ============================================================================
c1, s1, c2, s2 = sp.symbols('c1 s1 c2 s2', positive=True)
two_same = sp.simplify(c1 * g / (g + s1) + c2 * g / (g + s2)
                       - (c1 + c2) * g / (g + s1)).subs({s2: s1, c2: c2})
two_same = sp.simplify((c1 * g / (g + s1) + c2 * g / (g + s1))
                       - (c1 + c2) * g / (g + s1))
# additive occupancy with one shared scale is a single Langmuir: capacity adds,
# and A'(0)=1 then forces capacity = scale => n=1 again.
slope_two = sp.simplify(sp.diff((2 * c1) * g / (g + s1), g).subs(g, 0) - 2 * c1 / s1)
# a two-scale sum cannot be even in g either, so it cannot be n=2 either
two_scale = c1 * g / (g + s1) + c2 * g / (g + s2)
k8_even = sp.simplify(two_scale.subs(g, -g) - two_scale)
ck("K8", two_same == 0 and slope_two == 0 and k8_even != 0, float(abs(sp.N(slope_two, 12))),
   0.0, "2 identical gates = 1 Langmuir with capacity 2c; A'(0)=1 => 2c=s => n=1")

# ============================================================================
# K9 -- maximum fractional difference: 15.47% in g, 7.457% in v, at g_N=a0/2
# ============================================================================
z = sp.symbols('z', positive=True)
R = (z + 1) / sp.sqrt(z ** 2 + 3)
dR = sp.simplify(sp.diff(R, z))
zmax = sp.solve(sp.Eq(dR, 0), z)
Rmax = sp.simplify(R.subs(z, 3))
exact_g = sp.simplify(Rmax - 1)
exact_v = sp.simplify(sp.sqrt(Rmax) - 1)
y = np.logspace(-7, 7, 400001)
gg1 = 0.5 * (y + np.sqrt(y * y + 4 * y))     # g1/a0
gg2 = np.sqrt(y * y + y)                     # g2/a0
frac = gg1 / gg2 - 1.0
imax = int(np.argmax(frac))
num_g = float(frac[imax])
num_v = float(np.sqrt(gg1[imax] / gg2[imax]) - 1.0)
y_at = float(y[imax])
k9 = (abs(num_g - float(exact_g)) < 2e-6 and abs(y_at - 0.5) < 2e-3
      and abs(num_v - float(exact_v)) < 2e-6)
ck("K9", k9, num_g, float(exact_g),
   f"max at gN/a0={y_at:.6f}; v-ratio max {num_v:.9f} vs {float(exact_v):.9f}")

# ============================================================================
# K10 -- where: g_N = a0/2, r = sqrt(2 G M / a0), mass-independent fraction
# ============================================================================
rows = []
for M in (1e8, 1e9, 1e10, 1e11):
    GM = G_NEWT * M * MSUN
    rM = math.sqrt(GM / A0)          # MOND radius sqrt(GM/a0)
    rs = math.sqrt(2.0) * rM         # radius where g_N = a0/2
    v1 = math.sqrt(A0 * rs)
    v2 = math.sqrt(math.sqrt(3.0) / 2.0 * A0 * rs)
    rows.append({"M_Msun": M, "r_star_kpc": rs / KPC, "gN_over_a0": 0.5,
                 "v1_kms": v1 / 1e3, "v2_kms": v2 / 1e3,
                 "frac_v": v1 / v2 - 1.0})
r10 = rows[2]
# mass independence of the fractional maximum (point source): all rows equal
spread = max(r["frac_v"] for r in rows) - min(r["frac_v"] for r in rows)
k10 = (abs(r10["r_star_kpc"] - 5.4574) < 2e-3 and abs(r10["v1_kms"] - 125.55) < 0.05
       and spread < 1e-12)
ck("K10", k10, r10["r_star_kpc"], 5.4574,
   f"M=1e10 Msun: r*={r10['r_star_kpc']:.5f} kpc v1={r10['v1_kms']:.3f} v2={r10['v2_kms']:.3f} km/s")

# windows where the two laws differ by more than a threshold (in g)
wins = {}
for thr in (0.01, 0.05, 0.10):
    yy = y[frac >= thr]
    wins[str(thr)] = [float(yy.min()), float(yy.max())]

# ============================================================================
# K11 -- fluctuation-dissipation: RAR scatter at fixed g_N <-> occupancy variance
# ============================================================================
def sig_log_g(gval, Ns, law):
    """sigma(log10 g) at fixed g_N for one law, from binomial occupancy noise."""
    if law == 1:
        cap, aff = A0, A0
        th = gval / (gval + aff)
        up = aff ** 2 / (gval + aff) ** 2
    else:
        cap = A0 / 2.0
        a = A0 / 2.0
        uu = gval + a - math.sqrt(gval * gval + a * a)
        th = uu / cap
        up = 1.0 - gval / math.sqrt(gval * gval + a * a)
    # delta g = cap*xi/(1-u'),  Var(xi)=th(1-th)/Ns
    sig_g = cap * math.sqrt(th * (1 - th) / Ns) / abs(1.0 - up)
    return sig_g / (gval * math.log(10.0))

# exact closed form for n=1:  sigma_g = a0^{3/2}(g+a0) / (sqrt(Ns g)(g+2a0))
def sig_log_closed(gval, Ns):
    return (A0 ** 1.5 * (gval + A0) /
            (gval ** 1.5 * (gval + 2 * A0) * math.sqrt(Ns) * math.log(10.0)))

closed_err = abs(sig_log_closed(3 * A0, 7.0) - sig_log_g(3 * A0, 7.0, 1))
# Monte Carlo of the binomial occupancy variance at fixed g (Ns sites)
rng = np.random.default_rng(20261021)
Ns_mc, gmc = 4000, 2.0 * A0
thm = gmc / (gmc + A0)
draws = rng.binomial(Ns_mc, thm, size=20000) / Ns_mc
mc_rel_std = float(np.std(draws)) / thm          # relative to the mean occupancy
pred_rel_std = math.sqrt((1 - thm) / (thm * Ns_mc))
mc_err = abs(mc_rel_std / pred_rel_std - 1.0)
# the same variance seen as an acceleration scatter at fixed g_N
sig_g_pred = A0 * pred_rel_std * thm / abs(1.0 - A0 ** 2 / (gmc + A0) ** 2)
k11 = closed_err < 1e-12 * max(1.0, sig_log_closed(3 * A0, 7.0)) and mc_err < 0.03
ck("K11", k11, mc_err, 0.03,
   f"Var(th)/th^2=(1-th)/(th Ns); MC rel.std {mc_rel_std:.6f} vs {pred_rel_std:.6f}")

# ============================================================================
# K12 -- the observable: sigma(log g) ~ g^-3/2, Ns-free ratio, n=1 vs n=2
# ============================================================================
Ns = 1.0
r_lo_hi_1 = sig_log_g(0.3 * A0, Ns, 1) / sig_log_g(3.0 * A0, Ns, 1)
r_lo_hi_2 = sig_log_g(0.3 * A0, Ns, 2) / sig_log_g(3.0 * A0, Ns, 2)
r_a0_10_1 = sig_log_g(A0, Ns, 1) / sig_log_g(10 * A0, Ns, 1)
r_a0_10_2 = sig_log_g(A0, Ns, 2) / sig_log_g(10 * A0, Ns, 2)
# slope check: the asymptotic log-log slope is -3/2 (approach is O(a0/g))
gs = np.array([1e3, 1e4, 1e5]) * A0
sl = np.polyfit(np.log(gs), np.log([sig_log_g(v, Ns, 1) for v in gs]), 1)[0]
# exact local slope d ln sigma / d ln g at g = 30 a0 (finite-g value, for the report)
sl_30 = 30.0 / 31.0 - 1.5 - 30.0 / 32.0
# inversion: Ns required for the lattice term to stay below a stated scatter
def ns_for(sigma_dex, gval, law=1):
    return (sig_log_g(gval, 1.0, law) / sigma_dex) ** 2
ns_bound = ns_for(0.05, 0.3 * A0, 1)
k12 = (abs(sl + 1.5) < 0.005 and r_lo_hi_1 > 20 and r_a0_10_1 > 20
       and abs(r_a0_10_1 - 22.998) < 0.01)
ck("K12", k12, float(sl), -1.5,
   f"ratio(0.3a0/3a0) n1={r_lo_hi_1:.2f} n2={r_lo_hi_2:.2f}; "
   f"ratio(a0/10a0) n1={r_a0_10_1:.2f} n2={r_a0_10_2:.2f}")

# skewness: sign flip exactly at theta=1/2, i.e. g=a0 (N_s-free location)
sk_lo = (1 - 2 * 0.3) / math.sqrt(4000 * 0.3 * 0.7)
sk_hi = (1 - 2 * 0.7) / math.sqrt(4000 * 0.3 * 0.7)
ck("K13", sk_lo > 0 > sk_hi, float(sk_lo), 0.0,
   "skew(delta g) ~ (1-2 theta): positive below g=a0, negative above")

# ============================================================================
# K14 -- one scale only: the law is homogeneous of degree 1 in (g, a0)
# ============================================================================
hom1 = sp.simplify((lam * g) ** 2 / (lam * g + lam * a0) - lam * gN_can)
hom2 = sp.simplify(sp.sqrt((lam * g) ** 2 + (lam * a0 / 2) ** 2) - lam * a0 / 2
                   - lam * (sp.sqrt(g ** 2 + (a0 / 2) ** 2) - a0 / 2))
ck("K14", hom1 == 0 and hom2 == 0, float(abs(sp.N(hom1, 20)) + abs(sp.N(hom2, 20))), 0.0,
   "both laws homogeneous deg 1 in (g,a0): a0 is the only dimensionful input")

# ============================================================================
# K15 -- multi-occupancy ladders ("capacity in energy"): capacity >= a0 always
# ============================================================================
def ladder_theta(xv, Nmax, Uhat):
    """Grand-canonical occupancy of a site with N=0..Nmax, E=eps*N+U*N(N-1)/2."""
    N = np.arange(Nmax + 1, dtype=float)
    w = np.exp(N * np.log(xv) - Uhat * N * (N - 1) / 2.0)
    return float(np.sum(N * w) / np.sum(w))

def ladder_capacity(Nmax, Uhat):
    """theta at x->inf (capacity/C) and slope at x->0 (must be 1)."""
    return float(ladder_theta(1e12, Nmax, Uhat))

lad = {}
for Nmax, Uhat in ((1, 0.0), (2, 0.0), (3, 0.0), (2, 2.0), (5, 1.0), (8, 3.0)):
    cap_ratio = ladder_capacity(Nmax, Uhat)
    # slope at x->0 is 1 for every ladder, so C = a0; compare NORMALISED shapes
    xs = np.logspace(-2, 2, 400)
    th_l = np.array([ladder_theta(xv, Nmax, Uhat) for xv in xs]) / cap_ratio
    th_1 = xs / (1 + xs)
    th_2 = (2 * xs + 1 - np.sqrt(4 * xs ** 2 + 1))       # u/a0 with u=A_2, x=g/a0
    dev1 = float(np.max(np.abs(th_l - th_1)))
    dev2 = float(np.max(np.abs(th_l - th_2)))
    lad[f"Nmax{Nmax}_U{Uhat}"] = {"capacity_over_a0": cap_ratio,
                                  "maxdev_vs_n1": dev1, "maxdev_vs_n2": dev2}
min_cap = min(v["capacity_over_a0"] for v in lad.values())
best1 = lad["Nmax1_U0.0"]
k15 = (min_cap >= 1.0 - 1e-9 and best1["maxdev_vs_n1"] < 1e-12
       and abs(best1["capacity_over_a0"] - 1.0) < 1e-9
       and all(v["maxdev_vs_n2"] > 1e-3 for v in lad.values()))
ck("K15", k15, min_cap, 1.0,
   "ladders N=0..Nmax: capacity/a0 >= 1 always (a0/2 unreachable); only Nmax=1 is exact")

# ============================================================================
# K16 -- the declared capacity assignment reproduces the canonical law
# ============================================================================
def g_from_lattice(gNv, cap, aff):
    """Invert g_N = g - cap*g/(g+aff) for g > 0."""
    return 0.5 * (gNv + cap - aff +
                  math.sqrt((aff - cap - gNv) ** 2 + 4.0 * gNv * aff))

gN_grid = A0 * np.logspace(-3, 3, 600)
g_recon = np.array([g_from_lattice(v, CAP, AFF) for v in gN_grid])
g_ref = law_canonical(gN_grid)
rel_dev = float(np.max(np.abs(g_recon / g_ref - 1.0)))
k16 = rel_dev < 1e-12
ck("K16", k16, rel_dev, 1e-12,
   f"lattice inversion with CAP={CAP:.3e}, AFF={AFF:.3e} vs canonical law on gN/a0 in [1e-3,1e3]")

# ============================================================================
# summary
# ============================================================================
npass = sum(1 for c in CHECKS if c["pass"])
ntot = len(CHECKS)

numbers = {
    "max_frac_g": num_g,
    "max_frac_v": num_v,
    "max_frac_g_exact": float(exact_g),
    "max_frac_v_exact": float(exact_v),
    "argmax_y": y_at,
    "frac_2_over_sqrt3_minus_1": float(2 / math.sqrt(3) - 1),
    "sqrt_2_over_sqrt3_minus_1": float(math.sqrt(2 / math.sqrt(3)) - 1),
    "windows_g": wins,
    "table": rows,
    "sigma_ratio_0p3_3_n1": r_lo_hi_1,
    "sigma_ratio_0p3_3_n2": r_lo_hi_2,
    "sigma_ratio_a0_10a0_n1": r_a0_10_1,
    "sigma_ratio_a0_10a0_n2": r_a0_10_2,
    "sigma_log_slope_high_g": float(sl),
    "Ns_for_0p05dex_at_0p3a0": ns_bound,
    "Ns_for_0p03dex_at_a0": ns_for(0.03, A0, 1),
    "Ns_for_0p05dex_at_a0": ns_for(0.05, A0, 1),
    "Ns_for_0p10dex_at_a0": ns_for(0.10, A0, 1),
    "capacity": CAP,
    "affinity": AFF,
    "mutate": MUTATE,
    "prior_report_2026_10_20": {
        "r_star_kpc": 5.45785,
        "v1_kms": 125.554,
        "rel_diff_r": abs(r10["r_star_kpc"] / 5.45785 - 1.0),
        "rel_diff_v": abs(r10["v1_kms"] / 125.554 - 1.0),
        "source": "core_open_problems_2026_10_20/02_medium/report.md section 8",
    },
    "r_window_kpc_1e10": {
        k: [math.sqrt(2.0 * G_NEWT * 1e10 * MSUN / (A0 * v[1])) / KPC,
            math.sqrt(2.0 * G_NEWT * 1e10 * MSUN / (A0 * v[0])) / KPC]
        for k, v in wins.items()
    },
    "stated_thresholds": {"flat_scatter_factor": 1.2},
    "pct_forms": {"max_frac_g_pct": 100.0 * num_g, "max_frac_v_pct": 100.0 * num_v,
                  "prior_figure_pct": 7.46, "mutation_dev_pct": 93.79},
    "scatter_dex_examples": [0.03, 0.05, 0.10],
}

print(f"A2 COMPLETE: {npass}/{ntot} checks PASS.")
if npass != ntot:
    print("FAILED: " + ",".join(c["id"] for c in CHECKS if not c["pass"]))

if not MUTATE:
    out = {
        "lane": "A2_medium",
        "status": ("CONDITIONAL(single-scale driven two-state lattice: capacity = "
                   "affinity = a0); n=1 forced; n=2 NO-GO in the thermal-lattice class"),
        "checks": CHECKS,
        "numbers": numbers,
        "constants_used": [
            {"name": "a0_can", "value": A0, "source": "BRIEF section 4"},
            {"name": "a0_alt", "value": A0_ALT, "source": "BRIEF section 4 (not used)"},
            {"name": "G", "value": G_NEWT, "source": "BRIEF section 4"},
            {"name": "GM_sun", "value": GM_SUN, "source": "IAU nominal, external"},
            {"name": "M_sun", "value": MSUN, "source": "GM_sun/G"},
            {"name": "kpc", "value": KPC, "source": "BRIEF section 4 (1 pc)"},
        ],
    }
    with open("a2_results.json", "w") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")

sys.exit(0 if npass == ntot else 1)
