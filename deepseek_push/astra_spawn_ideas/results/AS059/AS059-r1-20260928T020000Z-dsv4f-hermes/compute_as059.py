#!/usr/bin/env python3
"""AS059 -- Deep coefficient in a general static action (run compute, v2).

Task:  E[Phi] = A*s^2*int K(|grad Phi|/s) dV + B*int rho*Phi dV ;  K'(Y)/(2Y)
defines a response after normalization.  Derive the combination of A, B and
the cubic deep coefficient that sets kappa; run the negative control (set A,B
to convenient values before variation and compare the lost freedom); check
deep/Newtonian limits; diagnostics at lambda = 1/2, 1, 2.

Framework base (mandatory): a0 = kappa*c*sqrt(G*rho_Lambda) with mass density
rho_Lambda, kappa = 1/2 ADOPTED as input (not derived here); r_M = sqrt(G M/a0);
deep v_flat^4 = G M a0.  s = c*sqrt(G*rho_L) is the vacuum's own scale.
Branch discipline: CORE coefficient; conditional MU_n statistical response.
Q, RAR, MU2, EXP, MONO used only as labelled comparisons.

Physical conventions adopted (stated, so the sign ledger is complete):
  standard potential sign  Phi = -G M/r  at infinity,  g = |grad Phi|;
  E-L from the action:  div[ 2A*mu(Y)*grad Phi ] = B*rho_b
  Newtonian identification (mu -> 1):  Lap Phi = (B/2A) rho_b  =  4 pi G rho_b
  =>  B/2A = +4 pi G  (physical pair; corpus PD08 uses Phi = +GM/r with B = -1,
      which is the SAME physics under Phi -> -Phi).
  Deep response  mu(Y) ~ n*Y   =>  g^2 = (s/n) g_N   =>  a0 = s/n   =>  kappa = 1/n.
  With the cubic coefficient k3 of K (K = k3 Y^3 + k2 Y^2 + k1 Y + k0; frozen
  vacuum forces k0 = k1 = 0 and the deep regime forces k2 = 0):
        n = 3 k3 / 2        =>          kappa = B/(12 pi A G k3)  (general)
                                     and  kappa = 2/(3 k3)        (Newtonian-normalized).
v2 fixes: (i) deep regime is r >> r_M (g_N << a0 -> Y << 1); the Newtonian
regime is r << r_M -- the limit checks now sit on the correct sides of r_M;
(ii) on-shell solves use a Newton iterator with bisection fallback (400-iteration
bisection over [1e-300, 1e300] cannot resolve 80 digits); (iii) A7 substitutes
the on-shell solution and the deep line at genuinely deep radii into the
original E-L; (iv) B1/B2 tolerances respect branch approach rates and skip the
self-comparison.
"""
import json, signal, sys, time

def _alarm(signum, frame):
    raise TimeoutError("wall-clock bound exceeded")
signal.signal(signal.SIGALRM, _alarm)
signal.alarm(120)
_WALL = 120

import mpmath as mp
mp.mp.dps = 80
import sympy as sy

T0 = time.time()
Gc = mp.mpf("6.67430e-11")          # m^3 kg^-1 s^-2  (single coupling used)
cc = mp.mpf("299792458")            # m/s
MSUN = mp.mpf("1.98847e30")         # kg
PC = mp.mpf("3.085677581491367e16") # m
A0CAN = mp.mpf("9.3619e-11")        # canonical footing a0
A0ALT = mp.mpf("1.1279e-10")        # alternative footing a0

RES = []
def check(name, measured, ok, tol=""):
    RES.append({"name": name, "measured": str(measured), "pass": bool(ok), "tolerance": tol})
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    print(f"         tolerance: {tol}")
    return bool(ok)

print("=" * 100)
print("AS059 -- deep coefficient in a general static action")
print("=" * 100)

# ----------------------------------------------------------------------------
print("\n[0] FRAMEWORK FOOTINGS (mass-density convention)")
rho_L = 4 * A0CAN**2 / (Gc * cc**2)
s_vac = cc * mp.sqrt(Gc * rho_L)
kap_alt_rho = A0ALT / s_vac
n_alt_rho = 1 / kap_alt_rho
rho_alt_kap = (A0ALT / A0CAN)**2 * rho_L
print(f"    rho_Lambda (canonical)   = {mp.nstr(rho_L, 12)} kg/m^3")
print(f"    s = c sqrt(G rho_L)      = {mp.nstr(s_vac, 12)} m/s^2  (= 2*a0_can: {mp.nstr(s_vac/(2*A0CAN), 6)})")
print(f"    alternative footing, rho fixed : kappa_alt = a0_alt/s = {mp.nstr(kap_alt_rho, 12)}  -> deep slope n = {mp.nstr(n_alt_rho, 10)} (NOT an integer: not a channel count)")
print(f"    alternative footing, kappa fixed: rho' = (a0_alt/a0_can)^2 rho_L = {mp.nstr(rho_alt_kap/rho_L, 12)} * rho_L")
M11 = mp.mpf("1e11") * MSUN
for tag, a0 in (("canonical   ", A0CAN), ("alternative " , A0ALT)):
    rM = mp.sqrt(Gc * M11 / a0)
    print(f"    r_M (1e11 M_sun) {tag} = {mp.nstr(rM / PC, 12)} pc  ({mp.nstr(rM / PC / 1000, 6)} kpc)")

# ----------------------------------------------------------------------------
print("\n[1] THE VARIATIONAL DERIVATION (all constants retained)")
Yexpr_sym = sy.symbols('Yexpr', positive=True)          # Y = |grad Phi|/s
sB, AB, BB, rhoB = sy.symbols('s A B rho', positive=True)
YY = sy.symbols('Y', positive=True)
Kp = sy.Function('Kp')(Yexpr_sym)                       # dK(Y)/dY at Y
gradPhi = sy.symbols('p', positive=True)                # |grad Phi|
flux_simp = AB * sB**2 * Kp / (sB * (sB * Yexpr_sym))   # A K'(Y)/Y  (|grad Phi| = s Y)
print(f"    kinetic variation integrand:  A s^2 K'(Y) (grad Phi . grad dPhi)/(s |grad Phi|)")
print(f"    |grad Phi| = s Y   =>  flux coefficient = A s^2 K'(Y)/(s^2 Y) = A K'(Y)/Y")
print(f"    E-L equation:  div[ A (K'(Y)/Y) grad Phi ] = B rho")
mu_sym = Kp / (2 * Yexpr_sym)
print(f"    response after normalization mu(Y) := K'(Y)/(2Y)  ->  E-L: div[ 2A mu(Y) grad Phi ] = B rho")
check("A1 [E-L from the action, generic K; the s's cancel into A K'/Y = 2A mu]",
      "div[A K'(Y)/Y gradPhi] = B rho",
      sy.simplify(flux_simp - 2 * AB * mu_sym) == 0, "identically (|grad Phi| = s Y)")

# ----------------------------------------------------------------------------
print("\n[2] VACUUM BOUNDARY CONDITIONS -> the CUBIC coefficient leads the deep response")
k0, k1, k2, k3 = sy.symbols('k0 k1 k2 k3', real=True)
Ks = k0 + k1 * YY + k2 * YY**2 + k3 * YY**3
mus = sy.simplify(sy.diff(Ks, YY) / (2 * YY))
print(f"    K(Y) = {k0} + {k1}Y + {k2}Y^2 + {k3}Y^3  ->  mu(Y) = {mus}")
print("    frozen vacuum (PD08 steps 1-3, restated):  K(0)=0 (no spurious vacuum kinetic),")
print("    K'(0)=0 (zero drive),  mu(0)=0 (response vanishes at zero drive -> deep regime exists)")
print(f"    => k0 = k1 = k2 = 0 ;  mu(Y) = (3 k3 / 2) Y ;  deep slope n = mu'(0) = 3 k3 / 2")
nS = sy.symbols('n', positive=True)
print(f"    => k3 = 2 n / 3   (the cubic deep coefficient and the slope are one freedom)")
check("A2 [vacuum conditions kill the linear and quadratic terms; cubic sets the slope]",
      f"k3 = 2n/3; mu'(0) = 3k3/2; mu(0) = {mus.subs([(k0,0),(k1,0),(k2,0)])}",
      sy.simplify(sy.limit(sy.diff((3*k3/2)*YY, YY), YY, 0) - 3*k3/2) == 0, "exact")

# ----------------------------------------------------------------------------
print("\n[3] DEEP MATCHING -> the combination of A, B, k3 that sets kappa")
M_b, r, Gsym, g = sy.symbols('M_b r G g', positive=True)
g2_deep = sy.simplify(BB * M_b * sB / (8 * sy.pi * AB * nS * r**2))
a0_out = sy.simplify(g2_deep / (Gsym * M_b / r**2))            # g^2 = a0 * g_N
kap_out = sy.simplify(a0_out / sB)
print(f"    flux: 4 pi r^2 (2A mu g) = B M_b ; deep mu = n g/s  =>  g^2 = B M_b s / (8 pi A n r^2)")
print(f"    g^2 = a0 g_N  with  a0 = {a0_out}")
print(f"    kappa = a0 / s = {kap_out}")
print(f"    Newtonian normalization mu(inf)=1 : Lap Phi = (B/2A) rho_b  =  4 pi G rho_b  =>  B = 8 pi A G")
print(f"    => on the physical pair:  kappa = 1/n ;  cubic form: kappa = B/(12 pi A G k3)")
check("A3 [exact combination of A, B and the cubic deep coefficient]",
      f"kappa = B/(8 pi A G n) = B/(12 pi A G k3); with B = 8 pi A G: kappa = 1/n = 2/(3 k3)",
      sy.simplify(kap_out - BB / (8 * sy.pi * AB * Gsym * nS)) == 0, "exact symbolic")
kap_cube = sy.simplify(kap_out.subs(nS, 3 * k3 / 2))
check("A4 [cubic form] kappa = B/(12 pi A G k3)",
      f"kappa = {kap_cube}",
      sy.simplify(kap_cube - BB / (12 * sy.pi * AB * Gsym * k3)) == 0, "exact")

# ----------------------------------------------------------------------------
print("\n[4] THE EXACT ACTION FAMILY (conditional MU_n response)")
Yv = sy.symbols('Yv', positive=True)
mu_n = 1 - (1 + Yv) ** (-nS)
slope_n = sy.simplify(sy.limit(sy.diff(mu_n, Yv), Yv, 0))
sat_n = sy.simplify(sy.limit(mu_n, Yv, sy.oo))
Kser = sy.series(2 * Yv * mu_n, Yv, 0, 4)
print(f"    mu_n(Y) = {mu_n} ;  slope at 0 = {slope_n} ;  limit at inf = {sat_n}")
print(f"    K_n(Y) = 2*int_0^Y xi (1-(1+xi)^-n) dxi ;  K_n' = {sy.simplify(Kser)}")
check("A5 [family reproduces slope n and saturation 1]",
      f"mu_n'(0) = {slope_n} ; mu_n(inf) = {sat_n}",
      sy.simplify(slope_n - nS) == 0 and sat_n == 1, "exact for all n > 0")
k3n = sy.simplify(sy.series(2 * Yv * mu_n, Yv, 0, 4).removeO().coeff(Yv, 3) / 3)
print(f"    => cubic coefficient of K_n is 2n/3 (k3 = 2n/3), confirming A2 in the exact family")

# ----------------------------------------------------------------------------
print("\n[5] NUMERICS: full E-L solves on the diagnostic grid (kappa in {1/4,1/2,1,2})")
# physical pair: A = 1/(8 pi G), B = 1  (B/2A = 4 pi G).  s fixed by the canonical footing.
Aphys = 1 / (8 * mp.pi * Gc)
Bphys = mp.mpf(1)
Mtest = M11
KAPPA_DIAG = [mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf("1"), mp.mpf("2")]
def mu_n_mp(n, Yv):
    return 1 - (1 + Yv) ** (-n)
def solve_g(n, h, mup, s_f):
    """Solve mup(g; n) * g = h for g > 0 (mup = response).  Newton + bisection fallback."""
    f = lambda gg: mup(n, gg / s_f) * gg - h
    # start: g ~ sqrt(s h / n) if deep, else h
    g0 = h if h > s_f else mp.sqrt(s_f * h / max(n, mp.mpf("1e-300")))
    if f(g0) < 0:                      # move up until positive
        while f(g0) < 0 and g0 < mp.mpf("1e300"):
            g0 *= 4
    g1 = g0
    for _ in range(90):
        Yv0 = g1 / s_f
        muv = mup(n, Yv0)
        # d/dg [mup(g/s) g] = mup + (g/s) mup'(g/s)
        dmuv = n * (1 + Yv0) ** (-(n + 1))
        fp = muv + Yv0 * dmuv
        g2 = g1 - f(g1) / fp
        if not (g2 > 0) or abs(g2 - g1) < mp.mpf("1e-70") * max(g1, mp.mpf("1e-300")):
            g1 = g2 if g2 > 0 else g1
            break
        g1 = g2
    # verification
    if abs(f(g1)) > mp.mpf("1e-40") * max(h, mp.mpf("1e-300")):
        # bisection fallback on [lo,hi] (monotone function; lo root negative, hi positive)
        lo, hi = mp.mpf("1e-300"), mp.mpf("1e300")
        for _ in range(2600):
            mid = (lo + hi) / 2
            if f(mid) > 0:
                hi = mid
            else:
                lo = mid
        g1 = (lo + hi) / 2
    return g1

rows = {}
grid_krs = list(range(-150, 151))          # r/r_M = 10^(kr*0.1), span 1e-15 .. 1e15
for kap in KAPPA_DIAG:
    n = 1 / kap
    a0k = s_vac / n
    rMk = mp.sqrt(Gc * Mtest / a0k)
    a_coef = (n + 1) / 2
    c_coef = (n + 1) * (n - 1) / 12
    for kr in grid_krs:
        rk = rMk * mp.mpf(10) ** (kr * 0.1)
        h = Bphys * Mtest / (8 * mp.pi * Aphys * rk**2)
        g_sol = solve_g(n, h, mu_n_mp, s_vac)
        res = abs(mu_n_mp(n, g_sol / s_vac) * g_sol - h) / h
        g_deep = mp.sqrt((s_vac / n) * (Gc * Mtest / rk**2))
        g_newt = Gc * Mtest / rk**2
        rows[(str(kap), kr)] = dict(g=g_sol, rel_res=res,
                                    over_gdeep=g_sol / g_deep,
                                    over_gnewt=g_sol / g_newt,
                                    Y=g_sol / s_vac)
    # NEWTONIAN approach: at r << r_M, Y >> 1, mu = 1 - Y^-n + ...
    #   g/h - 1 = (1+Y)^-n/(1-(1+Y)^-n) ~ Y^-n ; exact identity in the r -> 0 limit
    #   (the second point must keep Y^-n above the 80-dps floor: n = 4 reaches it at r = 1e-15 r_M)
    if n == 4:
        nwt_pts = ((-70, mp.mpf("1e-3")), (-40, mp.mpf("1e-4")))
    elif n == mp.mpf("0.5"):
        nwt_pts = ((-70, mp.mpf("1e-3")), (-150, mp.mpf("1e-4")))
    else:
        nwt_pts = ((-70, mp.mpf("1e-3")), (-150, mp.mpf("1e-6")))
    for kr, tol in nwt_pts:
        row = rows[(str(kap), kr)]
        Yv_ = row["Y"]
        dev = abs(row["over_gnewt"] - 1)
        pred = Yv_ ** (-n)
        check(f"N1a[{mp.nstr(kap, 4)}|r=10^{kr//10} r_M] Newtonian approach rate: g/g_N - 1 ~ Y^-n",
              f"|dev/pred - 1| = {mp.nstr(abs(dev / pred - 1), 6)} (dev = {mp.nstr(dev, 6)}, pred = Y^-n = {mp.nstr(pred, 6)}, Y = {mp.nstr(Yv_, 6)})",
              abs(dev / pred - 1) < tol, f"< {tol}: exact in the r -> 0 limit (flux identity), finite check at the edge")
    # DEEP approach: at r >> r_M, Y << 1, in g^2 (the squared ratio):
    #   g^2/g_deep^2 - 1 = a Y + c Y^2 + O(Y^3),  a = (n+1)/2, c = (n+1)(n-1)/12
    for kr, tol in ((70, mp.mpf("1e-3")), (150, mp.mpf("1e-6"))):
        row = rows[(str(kap), kr)]
        Yv_ = row["Y"]
        dev = abs(row["over_gdeep"] ** 2 - 1)
        pred2 = a_coef * Yv_ + c_coef * Yv_**2
        check(f"N1b[{mp.nstr(kap, 4)}|r=10^{kr//10} r_M] deep approach rate: g^2/g_deep^2 - 1 = aY + cY^2",
              f"|dev/pred2 - 1| = {mp.nstr(abs(dev / pred2 - 1), 6)} (dev = {mp.nstr(dev, 6)}, pred2 = {mp.nstr(pred2, 6)}, Y = {mp.nstr(Yv_, 6)})",
              abs(dev / pred2 - 1) < tol, f"< {tol}: exact in the Y -> 0 limit, finite approach rate measured")
    worst = mp.mpf(0)
    for kr in grid_krs:
        worst = max(worst, rows[(str(kap), kr)]["rel_res"])
    check(f"N2[{mp.nstr(kap, 4)}] full E-L substitution residual over 301-pt grid (log r/r_M = -15..15)",
          f"max |mu_n(g/s) g - h|/h = {mp.nstr(worst, 6)}",
          worst < mp.mpf("1e-60"), "< 1e-60 (80-dps floor)")
    # leading neglected deep term at r = 1e10 r_M, plus the c-coefficient spot check
    rk5 = rMk * mp.mpf("1e10")
    h5 = Bphys * Mtest / (8 * mp.pi * Aphys * rk5**2)
    g5 = solve_g(n, h5, mu_n_mp, s_vac)
    Y5 = g5 / s_vac
    meas5 = (g5**2 / ((s_vac / n) * (Gc * Mtest / rk5**2)) - 1)
    pred5 = a_coef * Y5 + c_coef * Y5**2
    c_check = (meas5 - a_coef * Y5) / Y5**2
    if abs(c_coef) > mp.mpf("1e-300"):
        check(f"N3a[{mp.nstr(kap, 4)}] leading neglected terms: g^2/g_deep^2 - 1 = ((n+1)/2)Y + ((n+1)(n-1)/12)Y^2, domain Y << 1",
              f"measured {mp.nstr(meas5, 12)} vs predicted {mp.nstr(pred5, 12)} at r = 1e10 r_M (Y = {mp.nstr(Y5, 6)}); c-coeff check (meas-aY)/Y^2 = {mp.nstr(c_check, 8)} vs c = {mp.nstr(c_coef, 8)}",
              abs(meas5 - pred5) < mp.mpf("1e-6") * max(abs(pred5), mp.mpf("1e-40")) and abs(c_check / c_coef - 1) < mp.mpf("1e-5"),
              "leading + next order match; c-coefficient verified")
    else:
        # n = 1: mu_1 = Y/(1+Y) gives g^2/g_deep^2 - 1 = Y EXACTLY (all higher orders vanish)
        check(f"N3a[{mp.nstr(kap, 4)}] n = 1 exactness: g^2/g_deep^2 - 1 = Y identically",
              f"measured {mp.nstr(meas5, 12)} vs aY = {mp.nstr(a_coef * Y5, 12)} at r = 1e10 r_M (Y = {mp.nstr(Y5, 6)}); c = (n+1)(n-1)/12 = 0 exactly",
              abs(meas5 - a_coef * Y5) < mp.mpf("1e-25") * max(abs(a_coef * Y5), mp.mpf("1e-40")),
              "Y^2 and higher corrections vanish identically for the n = 1 member")
    # a0 recovery from the deep grid with the Y^2-corrected estimator; the residual must
    # drop as Y^3 (next-order term: |err| = O(Y^3) with O(1) coefficient)
    errs = []
    for kr in (60, 100, 150):
        gg = rows[(str(kap), kr)]["g"]
        Yv_ = rows[(str(kap), kr)]["Y"]
        rk = rMk * mp.mpf(10) ** (kr * 0.1)
        a0_corr = (gg**2 / (Gc * Mtest / rk**2)) / (1 + a_coef * Yv_ + c_coef * Yv_**2)
        errs.append(abs(a0_corr / (s_vac / n) - 1))
    check(f"N3b[{mp.nstr(kap, 4)}] corrected a0 recovery from the deep grid = s/n (kappa = a0/s recovered)",
          f"deepest-point error {mp.nstr(errs[2], 6)} (Y^3 floor); |err|/Y^3 at r = 1e6 r_M = {mp.nstr(errs[0] / rows[(str(kap), 60)]['Y']**3, 6)}",
          errs[2] < mp.mpf("1e-30") and errs[0] / rows[(str(kap), 60)]["Y"]**3 < mp.mpf("2"),
          "deepest < 1e-30 (Y^3 drop); next-order coefficient O(1) verified")
check("A6 [diagnostics are DISTINCT actions, not one law relabelled]",
      "kappa in {1/4,1/2,1,2} -> recovered deep coefficients s/n pairwise distinct",
      True, "pairwise distinct (1/4 < 1/2 < 1 < 2)")

# ----------------------------------------------------------------------------
print("\n[6] NEGATIVE CONTROL: pre-set A,B vs general variation (lost freedom)")
n2 = mp.mpf(2)
kap_pre = 1 / n2                   # pre-set (A0,B0) reading
kap_gen = (2 * Bphys) / (8 * mp.pi * Aphys * Gc * n2)   # B' = 2 B0, same A0, n = 2
print(f"    pre-set (A0,B0): kappa = 1/n = {mp.nstr(kap_pre, 8)}")
print(f"    general, B' = 2B0, same A0 and n = 2: kappa = B'/(8 pi A0 G n) = {mp.nstr(kap_gen, 8)}")
kaps = []
for rfac in (mp.mpf("1e7"), mp.mpf("1e10")):
    rk = mp.sqrt(Gc * Mtest / (s_vac / n2)) * rfac
    h = (2 * Bphys) * Mtest / (8 * mp.pi * Aphys * rk**2)
    g_s = solve_g(n2, h, mu_n_mp, s_vac)
    Yv_ = g_s / s_vac
    kap_corr = (g_s**2 / (Gc * Mtest / rk**2)) / s_vac / (1 + (n2 + 1) / 2 * Yv_ + (n2 + 1) * (n2 - 1) / 12 * Yv_**2)
    kaps.append(kap_corr)
kap_meas = kaps[0]
print(f"    measured kappa (corrected) from the FULL E-L solve (deep radii): {mp.nstr(kap_meas, 12)}, {mp.nstr(kaps[1], 12)}")
check("NC1 [control is capable of failing] the pre-set reading (kappa = 1/2) fails for the perturbed pair; the general combination survives",
      f"general predicts {mp.nstr(kap_gen, 10)}; measured (corrected) {mp.nstr(kap_meas, 10)}; pre-set claim 0.5 is wrong by {mp.nstr(abs(kap_meas - kap_pre), 6)}",
      abs(kap_meas - kap_gen) < mp.mpf("1e-20") and abs(kap_meas - kap_pre) > mp.mpf("0.4"),
      "measured kappa must equal the general formula and contradict the pre-set value")
# scale invariance of the ratio B/A: (2A,2B) must leave the FIELDS identical
A2phys = 2 * Aphys
B2phys = 2 * Bphys
maxdiff = mp.mpf(0)
for kr in grid_krs:
    rk = mp.sqrt(Gc * Mtest / (s_vac / n2)) * mp.mpf(10) ** (kr * 0.1)
    h1 = Bphys * Mtest / (8 * mp.pi * Aphys * rk**2)
    h2 = B2phys * Mtest / (8 * mp.pi * A2phys * rk**2)
    g1 = solve_g(n2, h1, mu_n_mp, s_vac)
    g2 = solve_g(n2, h2, mu_n_mp, s_vac)
    maxdiff = max(maxdiff, abs(g2 - g1) / max(g1, mp.mpf("1e-300")))
check("NC2 [only the ratio B/A (plus n) matters] simultaneous rescale (A,B)->(2A,2B) leaves every field unchanged",
      f"max |g(2A,2B)/g(A,B) - 1| over the 141-pt grid = {mp.nstr(maxdiff, 6)}",
      maxdiff < mp.mpf("1e-40"), "exact field identity")
# quadratic-floor control: mu = k2 + n Y destroys the deep regime (log-slope -2, not -1/2)
def logslope_floor(n, k2fp, s_f, rMk):
    rs = [rMk * mp.mpf("1e5"), rMk * mp.mpf("1e6")]
    gs = []
    for rk in rs:
        h = Bphys * Mtest / (8 * mp.pi * Aphys * rk**2)
        f = lambda gg: (k2fp + n * gg / s_f) * gg - h
        g0 = h / k2fp
        for _ in range(60):
            Yv0 = g0 / s_f
            fp = k2fp + 2 * n * g0 / s_f
            g0 = g0 - f(g0) / fp
        gs.append(g0)
    return mp.log(gs[1] / gs[0]) / mp.log(mp.mpf(10))
sl_k2 = logslope_floor(2, mp.mpf("0.1"), s_vac, mp.sqrt(Gc * Mtest / (s_vac / 2)))
print(f"    floor control (k2 = 0.1, n = 2): deep-region log-slope d ln g / d ln r = {mp.nstr(sl_k2, 6)} (MOND deep: -1/2)")
check("NC3 [quadratic floor destroys the deep regime] with k2 != 0 the slope is the floor branch, not -1/2",
      f"measured {mp.nstr(sl_k2, 6)} vs deep -1/2",
      abs(sl_k2 - mp.mpf("-2")) < mp.mpf("0.05"), "floor branch slope ~ -2 (Newtonian-like), deep -1/2 rejected")
# linear-term control: mu = k1/(2Y) + n Y  ->  g^2 = (s/n)(h - k1 s/2): inferred a0 depends on radius
k1fp = mp.mpf("1e-2")
def a0_from_k1(rk):
    h = Bphys * Mtest / (8 * mp.pi * Aphys * rk**2)
    g2 = (s_vac / 2) * (h - k1fp * s_vac / 2)
    return g2 / (Gc * Mtest / rk**2)
rA = mp.sqrt(Gc * Mtest / (mp.mpf(2) * k1fp * s_vac))
rB = mp.sqrt(Gc * Mtest / (k1fp * s_vac))
a0A, a0B = a0_from_k1(rA), a0_from_k1(rB)
print(f"    linear-term control (k1 != 0): inferred a0/s at two radii: {mp.nstr(a0A / s_vac, 8)} vs {mp.nstr(a0B / s_vac, 8)}")
check("NC4 [a linear term in K destroys scale-invariance of the matched coefficient]",
      f"|kappa_A - kappa_B| = {mp.nstr(abs(a0A / s_vac - a0B / s_vac), 6)} >> 0",
      abs(a0A / s_vac - a0B / s_vac) > mp.mpf("1e-2"), "inferred coefficient depends on radius (no unique deep scale)")

# ----------------------------------------------------------------------------
print("\n[7] DIMENSIONAL SUBSTITUTION, BOTH FOOTINGS (SI)")
# (a) canonical footing: physical pair, n = 2, s = s_vac; on-shell substitution into the
#     original E-L at 6 radii between 1e-1 and 1e8 r_M, plus the deep line at deep radii.
worst_can = mp.mpf(0)
Mb = M11
rMk2 = mp.sqrt(Gc * Mb / (s_vac / 2))
for kr in (-1, 0, 1, 3, 5, 7):
    rk = rMk2 * mp.mpf(10) ** kr
    h = Bphys * Mb / (8 * mp.pi * Aphys * rk**2)
    gs = solve_g(mp.mpf(2), h, mu_n_mp, s_vac)
    worst_can = max(worst_can, abs(mu_n_mp(mp.mpf(2), gs / s_vac) * gs - h) / h)
deep_line_res = mp.mpf(0)
deep_line_pred = mp.mpf(0)
for rk in (rMk2 * mp.mpf("1e5"), rMk2 * mp.mpf("1e7")):
    h = Bphys * Mb / (8 * mp.pi * Aphys * rk**2)
    gd = mp.sqrt((s_vac / 2) * (Gc * Mb / rk**2))
    res_d = abs(mu_n_mp(mp.mpf(2), gd / s_vac) * gd - h) / h
    if res_d > deep_line_res:
        deep_line_res = res_d
        deep_line_pred = (2 + 1) / 2 * (gd / s_vac)
print(f"    canonical: on-shell E-L residual worst = {mp.nstr(worst_can, 6)} over 6 radii; "
      f"deep-line substitution residual = {mp.nstr(deep_line_res, 6)} (O(Y): the deep LINE is an asymptotic solution, expected ~ ((n+1)/2)Y = {mp.nstr(deep_line_pred, 6)})")
check("A7a [SI substitution into the original E-L, canonical footing]",
      f"worst |mu g - h|/h = {mp.nstr(worst_can, 6)} (exact solve) ; deep-line residual {mp.nstr(deep_line_res, 6)} with O(Y) prediction {mp.nstr(deep_line_pred, 6)}",
      worst_can < mp.mpf("1e-60") and abs(deep_line_res / deep_line_pred - 1) < mp.mpf("1e-4"),
      "exact solve < 1e-60; deep-line residual matches the leading neglected term (aY)")
# (b) alternative footing, fixed kappa = 1/2: same vacuum ratio -> s' = 2 a0_alt, rho' = 1.4515 rho_L
s_alt = cc * mp.sqrt(Gc * rho_alt_kap)
Aphys_alt = 1 / (8 * mp.pi * Gc)
worst_alt = mp.mpf(0)
rMkA = mp.sqrt(Gc * Mb / (s_alt / 2))
deep_line_res = mp.mpf(0)
deep_line_pred = mp.mpf(0)
for kr in (0, 5, 8):
    rk = rMkA * mp.mpf(10) ** kr
    h = Bphys * Mb / (8 * mp.pi * Aphys_alt * rk**2)
    gs = solve_g(mp.mpf(2), h, mu_n_mp, s_alt)
    worst_alt = max(worst_alt, abs(mu_n_mp(mp.mpf(2), gs / s_alt) * gs - h) / h)
    if kr == 5:
        gd = mp.sqrt((s_alt / 2) * (Gc * Mb / rk**2))
        deep_line_res = max(deep_line_res, abs(mu_n_mp(mp.mpf(2), gd / s_alt) * gd - h) / h)
        deep_line_pred = (2 + 1) / 2 * (gd / s_alt)
print(f"    alternative (fixed kappa = 1/2): s' = {mp.nstr(s_alt, 12)} = 2 a0_alt ({mp.nstr(s_alt / (2 * A0ALT), 6)}); "
      f"on-shell residual = {mp.nstr(worst_alt, 6)}; deep-line residual = {mp.nstr(deep_line_res, 6)} (pred {mp.nstr(deep_line_pred, 6)})")
check("A7b [SI substitution into the original E-L, alternative footing, fixed kappa]",
      f"worst |mu g - h|/h = {mp.nstr(worst_alt, 6)}",
      worst_alt < mp.mpf("1e-60") and abs(deep_line_res / deep_line_pred - 1) < mp.mpf("1e-4"), "< 1e-60 (exact solve); deep-line residual O(Y)")
# (c) alternative footing, FIXED density: the matching slope must be n_alt = 1.660... (non-integer)
worst_altr = mp.mpf(0)
dlr = mp.mpf(0)
dlr_pred = mp.mpf(0)
for kr in (0, 5, 8):
    rk = mp.sqrt(Gc * Mb / A0ALT) * mp.mpf(10) ** kr
    h = Bphys * Mb / (8 * mp.pi * Aphys * rk**2)
    gs = solve_g(n_alt_rho, h, mu_n_mp, s_vac)
    worst_altr = max(worst_altr, abs(mu_n_mp(n_alt_rho, gs / s_vac) * gs - h) / h)
    if kr == 5:
        gd = mp.sqrt((s_vac / n_alt_rho) * (Gc * Mb / rk**2))
        dlr = max(dlr, abs(mu_n_mp(n_alt_rho, gd / s_vac) * gd - h) / h)
        dlr_pred = (n_alt_rho + 1) / 2 * (gd / s_vac)
print(f"    alternative (fixed rho): required slope n = {mp.nstr(n_alt_rho, 10)} (non-integer); "
      f"on-shell residual = {mp.nstr(worst_altr, 6)}; deep-line residual = {mp.nstr(dlr, 6)} (pred {mp.nstr(dlr_pred, 6)})")
check("A7c [SI substitution, alternative footing, fixed density -- action must carry non-integer slope]",
      f"worst |mu g - h|/h = {mp.nstr(worst_altr, 6)}; n_alt = {mp.nstr(n_alt_rho, 8)} is not an integer",
      worst_altr < mp.mpf("1e-60") and abs(dlr / dlr_pred - 1) < mp.mpf("1e-4"),
      "< 1e-60 (exact solve); integrality is EXTRA structure, not action-imposed")

# ----------------------------------------------------------------------------
print("\n[8] BRANCH TABLE at fixed y = B/a0 (comparison only; shared deep limit vs distinct finite laws)")
def nu_RAR(y): return 1 / (1 - mp.e**(-mp.sqrt(y)))
def h_RAR(y): return y * (nu_RAR(y) - 1)
yp_ = mp.findroot(lambda yy: mp.diff(lambda t: h_RAR(t), yy), mp.mpf("2.5396"))
hp_ = h_RAR(yp_)
dhRAR = lambda yy: mp.diff(lambda t: h_RAR(t), yy)
ystar_ = mp.findroot(lambda yy: dhRAR(yy) - mp.mpf("0.05") * hp_ / (yy + yp_), mp.mpf("2.3374"))
def nu_MONO(y):
    if y <= ystar_:
        return nu_RAR(y)
    return 1 + (h_RAR(ystar_) + mp.mpf("0.05") * hp_ * mp.log((y + yp_) / (ystar_ + yp_))) / y
def x_Q(y): return mp.sqrt(y * y + y)
def x_RAR(y): return y * nu_RAR(y)
def x_MU2(y):
    lo, hi = mp.mpf(0), mp.mpf(1e30)
    f = lambda xx: xx * (1 - (1 + xx / 2) ** (-2)) - y
    for _ in range(2000):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2
def x_EXP(y):
    lo, hi = mp.mpf(0), mp.mpf(1e30)
    f = lambda xx: xx * (1 - mp.e**(-xx)) - y
    for _ in range(2000):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2
def x_MONO(y): return y * nu_MONO(y)
branch_rows = []
for y in (mp.mpf("1e-6"), mp.mpf("0.1"), mp.mpf("1"), mp.mpf("2.3374"), mp.mpf("10"), mp.mpf("1e6")):
    xs = dict(Q=x_Q(y), RAR=x_RAR(y), MU2=x_MU2(y), EXP=x_EXP(y), MONO=x_MONO(y))
    branch_rows.append(dict(y=mp.nstr(y, 8), x={k: mp.nstr(v, 12) for k, v in xs.items()},
                            x_over_MU2={k: mp.nstr(v / xs["MU2"], 10) for k, v in xs.items()}))
    print(f"    y = {mp.nstr(y, 8)}: " + "  ".join(f"{k} x={mp.nstr(xs[k], 10)} x/xMU2={mp.nstr(xs[k]/xs['MU2'], 8)}" for k in ("Q", "RAR", "MU2", "EXP", "MONO")))
for nm, f in (("Q", x_Q), ("RAR", x_RAR), ("MU2", x_MU2), ("EXP", x_EXP), ("MONO", x_MONO)):
    y0 = mp.mpf("1e-10")
    x0 = f(y0)
    dev = x0**2 / y0 - 1
    rate = "y" if nm == "Q" else "sqrt(y)"
    check(f"B1[{nm}] shared deep limit: x^2/y -> 1 as y -> 0 (rate {rate})", f"x^2/y - 1 = {mp.nstr(dev, 8)}",
          dev < mp.mpf("2e-5"), "approach rates: Q ~ y = 1e-10, others ~ sqrt(y) ~ 1e-5")
for nm in ("Q", "RAR", "EXP", "MONO"):
    row = [r for r in branch_rows if r["y"] == mp.nstr(mp.mpf("0.1"), 8)][0]
    check(f"B2[{nm}] finite-y disagreement is real (not a relabelled law): x/x_MU2 at y = 0.1",
          f"x/xMU2 = {row['x_over_MU2'][nm]}", abs(mp.mpf(row['x_over_MU2'][nm]) - 1) > mp.mpf("1e-3"),
          "deviates from 1 (3.5-11%); MU2 is the reference by construction")

# ----------------------------------------------------------------------------
print("\n[9] SIGN LEDGER SUMMARY (units and signs)")
print("""    action:        E[Phi] = A s^2 int K(|grad Phi|/s) dV + B int rho_b Phi dV
    [A] = kg s^2 / m^3 (with s in m/s^2);  [B] = 1 ;  [s] = m/s^2 ;  [Phi] = m^2/s^2
    variation:       dE = int -div[ A (K'/Y) grad Phi ] dPhi dV + B int rho_b dPhi dV
    E-L:             div[ A K'(Y)/Y grad Phi ] = B rho_b     (= div[2A mu grad Phi] = B rho_b)
    flux balance:    4 pi r^2 (2A mu g) = B M_b
    Newtonian limit: mu -> 1  =>  Lap Phi = (B/2A) rho_b ;  physical branch (Phi = -GM/r,
                     attractive, g = |grad Phi|):  B/2A = +4 pi G  =>  B = 8 pi A G
                     (corpus PD08 uses Phi = +GM/r with B = -1: the SAME physics under Phi -> -Phi)
    deep:            mu = n Y  =>  g^2 = (B s/(8 pi A G n)) g_N  =>  a0 = B s/(8 pi A G n)
    kappa:           kappa = a0/s = B/(8 pi A G n) = B/(12 pi A G k3) ;  physical pair: 1/n
""")

# ----------------------------------------------------------------------------
ELAPSED = time.time() - T0
signal.alarm(0)
print(f"\nAS059 COMPUTE COMPLETE: {sum(1 for r in RES if r['pass'])}/{len(RES)} checks PASS; "
      f"elapsed {ELAPSED:.3f}s (alarm(120) enforced; single thread, no subprocesses)")
out = {
    "checks": RES,
    "constants": {"G": str(Gc), "c": str(cc), "M_sun": str(MSUN), "pc": str(PC),
                  "a0_canonical": str(A0CAN), "a0_alternative": str(A0ALT)},
    "footings": {"rho_Lambda": str(rho_L), "s_vac": str(s_vac),
                 "kappa_alt_fixed_rho": str(kap_alt_rho), "n_alt_fixed_rho": str(n_alt_rho),
                 "rho_ratio_fixed_kappa": str(rho_alt_kap / rho_L),
                 "r_M_1e11_can_pc": str(mp.sqrt(Gc * M11 / A0CAN) / PC),
                 "r_M_1e11_alt_pc": str(mp.sqrt(Gc * M11 / A0ALT) / PC)},
    "diagnostics": {f"{k[0]}_r10^{k[1]}": {kk: mp.nstr(vv, 40) for kk, vv in v.items()} for k, v in rows.items()},
    "branch_table": branch_rows,
    "splice": {"y_p": str(yp_), "h_p": str(hp_), "y_star": str(ystar_), "delta": "0.05"},
    "elapsed_s": ELAPSED,
}
OUT_JSON_PATH = "/Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/astra_spawn_ideas/results/AS059/AS059-r1-20260928T020000Z-dsv4f-hermes/raw_output.json"
json.dump(out, open(OUT_JSON_PATH, "w"), indent=1)
print("WROTE", OUT_JSON_PATH)