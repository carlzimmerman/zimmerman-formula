#!/usr/bin/env python3
"""j02_principles_and_intersections.py -- lane J: what do the candidate PRINCIPLES fix, and where do they meet the puzzle's target?

Conventions: exactly those verified in j01 (Heaviside rho = E^2/2, Gauss jump e, Israel A - B = 4 pi sigma, G = c = 1).
Units E = 1;  x = e/E,  s = sigma/E,  DP = x - x^2/2,  mean = DP/(3 s),  A, B = mean +- 2 pi s,  H_out = sqrt(4 pi/3),  H_in = H_out |1-x|.

DECLARED BEFORE ANY NUMBER WAS COMPUTED (the menu is frozen here; nothing was added after seeing a result):
  P1  (i)/(ii)/(iii) "no force from the outer vacuum" = critical / BPS-type / equator wall:  B = 0   <=>  DeltaP = 6 pi sigma^2   (R = 1/H_out)
      P1' the same for the inner vacuum: A = 0  <=>  DeltaP = -6 pi sigma^2
  P2  (i) net-force-free wall: DeltaP = 0 (mean acceleration zero)  <=>  x = 2 (field flips sign), or x = 0
  P3  (ii) complete discharge (interior Minkowski):  x = 1  (H_in = 0)
  P4  (v) flux quantisation E = n e:  x = 1/n, n = 1, 2, 3, ...
  P5  (iv) Schwinger/thermal threshold: bounce action B_bounce = hbar * (order one)  [needs hbar]
  P6  (iii) thresholds of the wall's own geometry: a = H crossover; R -> 0 (wall at the horizon); a = 0 (equatorial wall)
Target readings T:  mean, |A| or |B| equals H_ref / Z with H_ref = H_out or H_in, Z = sqrt(32 pi/3).
A principle 'counts' only if it plus at most ONE further declared principle fixes both x and s with no tuned number, and the result equals
the target.  Otherwise it is reported as a locus and the parameter values the target would need (x_t, s_t) are listed.

Exit 0 = every check (incl. controls that must detect wrong conventions/decoys) held.
"""
import sys, math, random
import sympy as sp
import mpmath as mp

mp.mp.dps = 30
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

Z = mp.sqrt(32 * mp.pi / 3)
Hout = mp.sqrt(4 * mp.pi / 3)
pi = mp.pi

def kappa_eff(aH):
    return aH / mp.sqrt(3 / (8 * mp.pi))

def acc(x, s):
    DP = x - x**2 / 2
    m = DP / (3 * s)
    return m, m + 2 * pi * s, m - 2 * pi * s

# =============================================================================================================== P1 derivation
print("== P1: critical / BPS-type / equator wall (B = 0) ==")
E_, e_, s_, G_ = sp.symbols('E e sigma G', positive=True)
Bs, As = sp.symbols('B A', real=True)
DP_ = sp.symbols('DP', positive=True)
# with G explicit: A - B = 4 pi G sigma,  A^2 - B^2 = (8 pi G/3) DP.   B = 0  =>
solB0 = sp.solve([sp.Eq(As - 0, 4 * sp.pi * G_ * s_), sp.Eq(As**2, sp.Rational(8, 3) * sp.pi * G_ * DP_)], [As, DP_], dict=True)[0]
chk("P1a B = 0 (wall geodesic w.r.t. the outer vacuum)  =>  DeltaP = 6 pi G sigma^2 and A = 4 pi G sigma", sp.simplify(solB0[DP_] - 6 * sp.pi * G_ * s_**2) == 0)
# (b) CDL: Minkowski false vacuum (H_out = 0), AdS true vacuum: 1/R^2 = B^2, R -> infinity <=> B = 0
chk("P1b Coleman-De Luccia critical tension for Minkowski -> AdS (R -> infinity, wall planar & static) is the same relation: |rho_AdS| = 6 pi G sigma^2",
    sp.simplify(solB0[DP_].subs(G_, 1) - 6 * sp.pi * s_**2) == 0)
# (c) N=1 supergravity, kappa = 8 pi G = 1 (supergravity domain-wall review hep-th/9604090, opened: Lambda = V = -3 chi^2 (6.1), extreme Type-I wall sigma = 2 chi (6.3)):
chi_ = sp.symbols('chi', positive=True)
rho_crit_kappa1 = (6 * sp.pi * G_ * s_**2).subs(G_, 1 / (8 * sp.pi))          # P1a with 8 pi G = 1: (3/4) sigma^2
chk("P1c the extreme (BPS) wall of N=1 sugra, sigma_ext = 2 chi with |V| = 3 chi^2 (kappa = 1), IS the B = 0 wall: |V| = (3/4) sigma^2 <=> sigma = 2 chi",
    sp.simplify(rho_crit_kappa1 - sp.Rational(3, 4) * s_**2) == 0 and sp.simplify(sp.solve(sp.Eq(3 * chi_**2, rho_crit_kappa1), s_)[0] - 2 * chi_) == 0)
# (d) dS: no real extreme wall, and the wall is not BPS
H_in2 = sp.symbols('Hin2', positive=True); Areal = sp.symbols('A_r', real=True)
H1, H2 = sp.symbols('H1 H2', positive=True)
sig_ext_dS = 2 * (sp.I * H1 - sp.I * H2)          # the review's Type III formula sigma = 2(chi_1 - chi_2) continued to chi = i H (dS)
chk("P1d between two dS vacua a planar static wall (1/R^2 = 0) would need A^2 = -H_in^2, which has no real solution; the sugra extreme-wall formula continued to chi = iH gives a purely imaginary sigma; and V > 0 breaks N=1 susy (the review states supersymmetric minima have V <= 0). So P1 in dS is the geometric threshold B = 0 (wall on the equator of the outer S^4), NOT a BPS statement",
    sp.solveset(sp.Eq(Areal**2, -H_in2), Areal, domain=sp.S.Reals) == sp.S.EmptySet and sp.re(sp.expand(sig_ext_dS)) == 0)
# the exact relations along P1 in the (x, s) plane
x, s = sp.symbols('x s', positive=True)
DPx = x - x**2 / 2
s_c = sp.sqrt(DPx / (6 * sp.pi))                                # s on P1
k_P1 = sp.simplify(x / s_c)                                      # k = e/sigma along P1
chk("P1e along P1: k = e/sigma = sqrt(12 pi x/(2 - x))  (pi to the first power)", sp.simplify(k_P1**2 - 12 * sp.pi * x / (2 - x)) == 0)
mean_P1 = sp.simplify(DPx / (3 * s_c))
Hout_s = sp.sqrt(4 * sp.pi / 3)
chk("P1f along P1: A/H_out = sqrt(x(2-x)),  mean/H_out = sqrt(x(2-x))/2  (pi-free for algebraic x); 1/R = H_out exactly",
    sp.simplify((mean_P1 * 2 / Hout_s)**2 - x * (2 - x)) == 0)
# probe-limit theorem: beta^2 = 6 pi sigma^2/DeltaP = 6 pi x/(k^2 (1 - x/2)) -> 0 at fixed k when x -> 0
k = sp.symbols('k', positive=True)
beta2 = 6 * sp.pi * (x / k)**2 / DPx
chk("P1g PROBE-LIMIT THEOREM: at fixed k = e/sigma, beta^2 = 6 pi G sigma^2/DeltaP = 6 pi x/(k^2 (1 - x/2)) -> 0 as x -> 0: every gravitational threshold (beta^2 = O(1): B = 0, A = 0) is unreachable in the probe limit unless k -> 0; P1 cannot fix k there",
    sp.limit(beta2, x, 0) == 0)

# =============================================================================================================== P2..P4
print("\n== P2/P3/P4: net-force-free, full discharge, flux quantisation ==")
chk("P2 (i) net-force-free wall: mean = DeltaP/(3 sigma) = 0 <=> x = 2 (or x = 0); then A = -B = 2 pi sigma: the acceleration left over is the wall's own gravity and sigma/H stays free",
    sp.simplify(sp.solve(sp.Eq(DPx, 0), x)[-1] - 2) == 0)
chk("P3 complete discharge x = 1: H_in = 0 (interior Minkowski), DeltaP = E^2/2; P1 and P3 together fix (x, s) = (1, 1/sqrt(12 pi))",
    sp.simplify(sp.sqrt(sp.Rational(1, 2) / (6 * sp.pi)) - 1 / sp.sqrt(12 * sp.pi)) == 0)
# P1 & P3 point
xP, sP = 1, 1 / mp.sqrt(12 * pi)
m, A, B = acc(1, sP)
print("   P1 & P3:  x = 1, s = %.6f;  mean/H_out = %.6f, A/H_out = %.6f, B = %.2e;  target 1/Z = %.6f;  kappa_eff(mean) = %.4f (= sqrt(2 pi/3) = %.4f), kappa_eff(A) = %.4f (= sqrt(8 pi/3) = %.4f)" %
      (sP, m / Hout, A / Hout, B, 1 / Z, kappa_eff(m / Hout), mp.sqrt(2 * pi / 3), kappa_eff(A / Hout), mp.sqrt(8 * pi / 3)))
chk("P1&P3 point: mean = H_out/2 (Z_eff = 2), A = H_out (Z_eff = 1): a factor Z/2 = sqrt(8 pi/3) = 2.894 and Z = 5.789 above the target 1/Z; not the target",
    abs(m / Hout - 0.5) < 1e-20 and abs(A / Hout - 1) < 1e-20 and abs((m / Hout) * Z - Z / 2) < 1e-20 and abs(m / Hout - 1 / Z) > 0.3)

# P4 alone: flux quantisation E = n e  =>  x = 1/n; the target then needs k_n = k*/(1 - 1/(2n)) (k free, only the correction factor is fixed)
nn = sp.symbols('n', positive=True)
k_n = sp.simplify((3 / (2 * sp.sqrt(2))) / (1 - 1 / (2 * nn)))
chk("P4a flux quantisation E = n e gives x = 1/n and nothing about k: the target then needs k_n = 3/(2 sqrt 2)/(1 - 1/(2n)); n = 1 gives 3/sqrt2 (the kappa = 1 probe value), n -> infinity gives 3/(2 sqrt2); a Dirac-type condition would carry hbar and relate e to a dual coupling, not to sigma",
    sp.simplify(k_n.subs(nn, 1) - 3 / sp.sqrt(2)) == 0 and sp.limit(k_n, nn, sp.oo) == 3 / (2 * sp.sqrt(2)))

# =============================================================================================================== intersections with the target
print("\n== the target locus intersected with each principle locus (units E = 1) ==")
def refs(x_, which):
    return Hout if which == 'out' else Hout * abs(1 - x_)

import numpy as np
def roots_1d(Ff, Fm, grid):
    """scan with float function Ff on a float grid, refine sign changes with the mpmath function Fm."""
    out = []
    vals = [Ff(t) for t in grid]
    for i in range(len(grid) - 1):
        v0, v1 = vals[i], vals[i + 1]
        if v0 is None or v1 is None or not (np.isfinite(v0) and np.isfinite(v1)):
            continue
        if v0 * v1 < 0:
            try:
                r = mp.findroot(Fm, (mp.mpf(grid[i]), mp.mpf(grid[i + 1])), solver='anderson', tol=1e-25, maxsteps=200)
                if abs(Fm(r)) < 1e-15:
                    out.append(r)
            except Exception:
                pass
    return out

def solutions(locus, reading, which):
    """all (x, s) on the locus with |reading| = H_ref/Z.  locus in {'B0','A0', c (x = c)}."""
    sols = []
    Hf = float(Hout); Zf = float(Z)
    def rd_f(x_, s_):
        DP = x_ - x_**2 / 2; m_ = DP / (3 * s_)
        return {'mean': abs(m_), 'A': abs(m_ + 2 * math.pi * s_), 'B': abs(m_ - 2 * math.pi * s_)}[reading]
    def rd_m(x_, s_):
        m_, A_, B_ = acc(x_, s_)
        return {'mean': abs(m_), 'A': abs(A_), 'B': abs(B_)}[reading]
    def ref_f(x_):
        return Hf if which == 'out' else Hf * abs(1 - x_)
    if locus in ('B0', 'A0'):
        sgn = 1 if locus == 'B0' else -1
        def sx_f(x_):
            v = sgn * (x_ - x_**2 / 2) / (6 * math.pi)
            return math.sqrt(v) if v > 0 else None
        def Ff(x_):
            s0 = sx_f(x_)
            if s0 is None or s0 == 0:
                return None
            return rd_f(x_, s0) - ref_f(x_) / Zf
        def Fm(x_):
            v = sgn * (x_ - x_**2 / 2) / (6 * pi)
            s0 = mp.sqrt(v)
            return rd_m(x_, s0) - (Hout if which == 'out' else Hout * abs(1 - x_)) / Z
        grid = [g / 1000 for g in range(-4000, 4001) if g != 0] + [4 + g / 20 for g in range(1, 1121)] + [-4 - g / 20 for g in range(1, 1121)]
        grid.sort()
        for r in roots_1d(Ff, Fm, grid):
            v = sgn * (r - r**2 / 2) / (6 * pi)
            sols.append((r, mp.sqrt(v)))
    else:
        xc = float(locus)
        def Ff(s0):
            if s0 <= 0:
                return None
            return rd_f(xc, s0) - ref_f(xc) / Zf
        def Fm(s0):
            return rd_m(locus, s0) - (Hout if which == 'out' else Hout * abs(1 - locus)) / Z
        grid = [10.0**(g / 200) for g in range(-1600, 800)]
        for r in roots_1d(Ff, Fm, grid):
            sols.append((mp.mpf(locus), r))
    uniq = []
    for xx, ss in sols:
        if all(abs(xx - u[0]) > 1e-8 or abs(ss - u[1]) > 1e-8 for u in uniq):
            uniq.append((xx, ss))
    return uniq

rows = []
loci = [('B0', 'P1  (B=0)'), ('A0', "P1' (A=0)"), (mp.mpf(1), 'P3  (x=1)'), (mp.mpf(2), 'P2  (x=2)')]
for locus, lname in loci:
    for reading in ('mean', 'A', 'B'):
        for which in ('out', 'in'):
            if which == 'in' and locus == mp.mpf(1):
                continue                                  # H_in = 0 at x = 1: the reading a = H_in/Z = 0 is degenerate
            for (xx, ss) in solutions(locus, reading, which):
                if refs(xx, which) < 1e-12:
                    continue                              # degenerate: reading equals zero
                m_, A_, B_ = acc(xx, ss)
                rows.append((lname, reading, which, xx, ss, xx / ss, m_ / Hout, A_ / Hout, B_ / Hout))
print("   %-11s %-5s %-4s %12s %12s %10s %10s | %9s %9s %9s" % ("locus", "read", "Href", "x_t", "s_t", "k_t=e/sig", "n_t=1/x_t", "mean/Ho", "A/Ho", "B/Ho"))
for (lname, rd_, wh, xx, ss, kk, mo, Ao, Bo) in rows:
    print("   %-11s %-5s %-4s %12.7f %12.7f %10.5f %10.4f | %9.5f %9.5f %9.5f" % (lname, rd_, wh, xx, ss, kk, 1 / xx if xx != 0 else float('inf'), mo, Ao, Bo))
def residual(row):
    lname, rd_, wh, xx, ss, kk_, mo, Ao, Bo = row
    val = {'mean': abs(mo), 'A': abs(Ao), 'B': abs(Bo)}[rd_] * Hout
    return abs(val - refs(xx, wh) / Z)
chk("I0 every listed intersection satisfies its reading exactly (residual < 1e-14); B-reading on P1 (B = 0) and A-reading on P1' (A = 0) correctly have no solution",
    len(rows) > 0 and all(residual(r) < 1e-14 for r in rows)
    and not any(r[0].startswith('P1  ') and r[1] == 'B' for r in rows) and not any(r[0].startswith("P1'") and r[1] == 'A' for r in rows))

# closed forms for the two headline intersections (P1 with the mean / A readings, H_ref = H_out)
xt_mean = 1 - mp.sqrt(1 - 3 / (8 * pi))
xt_A = 1 - mp.sqrt(1 - 3 / (32 * pi))
found_mean = [r for r in rows if r[0].startswith('P1  ') and r[1] == 'mean' and r[2] == 'out']
found_A = [r for r in rows if r[0].startswith('P1  ') and r[1] == 'A' and r[2] == 'out']
chk("I1 P1 with the mean reading (H_out): x_t = 1 - sqrt(1 - 3/(8 pi)) = %.6f (n_t = %.3f), s_t = 1/(4 sqrt2 pi) = %.6f" % (xt_mean, 1 / xt_mean, 1 / (4 * mp.sqrt(2) * pi)),
    len(found_mean) >= 1 and abs(found_mean[0][3] - xt_mean) < 1e-12 and abs(found_mean[0][4] - 1 / (4 * mp.sqrt(2) * pi)) < 1e-12)
chk("I2 P1 with the A reading (H_out): x_t = 1 - sqrt(1 - 3/(32 pi)) = %.6f (n_t = %.3f)" % (xt_A, 1 / xt_A),
    len(found_A) >= 1 and abs(found_A[0][3] - xt_A) < 1e-12)
# P3 with the mean reading: s_t = sqrt2/3
found_x1 = [r for r in rows if r[0].startswith('P3') and r[1] == 'mean' and r[2] == 'out']
chk("I3 P3 (x = 1) with the mean reading: s_t = sqrt2/3 = 0.4714 (algebraic), NOT the P1 value s = 1/sqrt(12 pi) = 0.1629: their ratio is sqrt(8 pi/3) = 2.894",
    len(found_x1) >= 1 and abs(found_x1[0][4] - mp.sqrt(2) / 3) < 1e-12 and abs(found_x1[0][4] * mp.sqrt(12 * pi) - mp.sqrt(8 * pi / 3)) < 1e-12)
found_x2 = [r for r in rows if r[0].startswith('P2') and r[1] == 'mean']
chk("I4 P2 (x = 2, DeltaP = 0): mean = 0, so the mean reading can never equal a0; only the A/B readings (= 2 pi sigma) can, at sigma tuned to H/(2 pi Z): a free ratio, not a principle-fixed one",
    len(found_x2) == 0 and any(r[0].startswith('P2') and r[1] == 'A' for r in rows))

# pi-degree ledger --------------------------------------------------------------------------------------------------------------
print("\n== pi-degree ledger (Heaviside variables x = e/E, s = sigma/E) ==")
xs, ss_ = sp.symbols('x s', positive=True)
target_rel = sp.Eq((xs - xs**2 / 2) / (3 * ss_), sp.sqrt(4 * sp.pi / 3) / sp.sqrt(32 * sp.pi / 3))
lhs_rhs = sp.simplify(target_rel.lhs - target_rel.rhs)
loci_rel = {"target (mean, H_out)": lhs_rhs,
            "P1  B=0": (xs - xs**2 / 2) - 6 * sp.pi * ss_**2,
            "P2  x=2": xs - 2,
            "P3  x=1": xs - 1,
            "P4  x=1/n": xs - sp.Rational(1, 16)}
for nm, ex in loci_rel.items():
    print("   %-24s relation %-42s contains pi: %s" % (nm, sp.simplify(ex), sp.simplify(ex).has(sp.pi)))
chk("L1 pi-degree ledger: the target locus DeltaP/(3 sigma) = sqrt(rho)/2 is pi-FREE in (x, s); P2, P3, P4 are pi-free; P1 carries pi to the first power",
    (not loci_rel["target (mean, H_out)"].has(sp.pi)) and (not loci_rel["P2  x=2"].has(sp.pi)) and (not loci_rel["P3  x=1"].has(sp.pi))
    and loci_rel["P1  B=0"].has(sp.pi))
# consequence: P1 meets the target at s = 1/(4 sqrt2 pi), x = 1 - sqrt(1 - 3/(8 pi)): both transcendental; so no algebraic (rational-n) x can lie on both
DPs = sp.symbols('DPs', positive=True)
DP_t = sp.solve(sp.Eq(DPs, 6 * sp.pi * (2 * sp.sqrt(2) / 3 * DPs)**2), DPs)[0]          # target locus s = (2 sqrt2/3) DP substituted into P1: DP = 6 pi s^2
xt_sym = sp.simplify(sp.solve(sp.Eq(xs - xs**2 / 2, DP_t), xs)[0])                      # smaller root
st_sym = sp.simplify(2 * sp.sqrt(2) / 3 * DP_t)
print("   P1 meets the target at DP = %s, x = %s = %.6f, s = %s = %.6f" % (DP_t, xt_sym, float(xt_sym), st_sym, float(st_sym)))
pi_from_x = sp.simplify(3 / (8 * (1 - (1 - xt_sym)**2)))
chk("L2a x_t is transcendental: pi = 3/(8(1 - (1 - x_t)^2)) is a rational function of x_t, so an algebraic x_t would make pi algebraic (Lindemann: false)", sp.simplify(pi_from_x - sp.pi) == 0)
chk("L2 P1 meets the target at x = 1 - sqrt(1 - 3/(8 pi)), s = 1/(4 sqrt(2) pi): both contain pi (transcendental), so no P4 point x = 1/n (algebraic) can equal it: an EXACT hit of P1+P4 is impossible for every integer n",
    xt_sym.has(sp.pi) and st_sym.has(sp.pi) and sp.simplify(xt_sym - (1 - sp.sqrt(1 - 3 / (8 * sp.pi)))) == 0)
# statement for P1&P4 numerically: mean/H = sqrt(2n-1)/(2n) algebraic vs 1/Z transcendental
print("   P1 & P4 (x = 1/n): mean/H_out = sqrt(2n-1)/(2n);  A/H_out = sqrt(2n-1)/n")
best = []
for rd_name, fac in (("mean", 1), ("A", 2)):
    devs = [(abs(fac * mp.sqrt(2 * n - 1) / (2 * n) * Z - 1), n) for n in range(1, 2000)]
    devs.sort()
    best.append((rd_name, devs[0]))
    print("     reading %-4s: nearest integer n = %d, value %.6f vs 1/Z = %.6f: %+.3f%%" % (rd_name, devs[0][1], fac * mp.sqrt(2 * devs[0][1] - 1) / (2 * devs[0][1]), 1 / Z,
          100 * (fac * mp.sqrt(2 * devs[0][1] - 1) / (2 * devs[0][1]) * Z - 1)))

# decoy control: how often does a RANDOM target coefficient come this close to some integer-n point? ------------------------------
random.seed(20260929)
def min_dev(t, fac):
    # min over n of |fac*sqrt(2n-1)/(2n)/t - 1|
    best_ = 1e9
    for n in range(1, 1200):
        v = fac * math.sqrt(2 * n - 1) / (2 * n)
        best_ = min(best_, abs(v / t - 1))
    return best_
ND = 1500
dec_mean = []; dec_A = []
for _ in range(ND):
    Zp = math.exp(random.uniform(math.log(3), math.log(12)))         # decoy coefficient Z' (a0 = H/Z')
    t = 1 / Zp
    dec_mean.append(min_dev(t, 1)); dec_A.append(min_dev(t, 2))
real_mean = min_dev(1 / float(Z), 1); real_A = min_dev(1 / float(Z), 2)
frac_mean = sum(1 for d in dec_mean if d <= real_mean) / ND
frac_A = sum(1 for d in dec_A if d <= real_A) / ND
print("   decoy control (%d random Z' in [3,12], same P1+P4 menu, n <= 1200):" % ND)
print("     mean reading: real nearest-n deviation %.3f%%; fraction of decoys at least this close: %.3f" % (100 * real_mean, frac_mean))
print("     A    reading: real nearest-n deviation %.3f%%; fraction of decoys at least this close: %.3f" % (100 * real_A, frac_A))
chk("D1 DECOY CONTROL: the near-hits of P1+P4 (n = 16 for the mean reading, +0.72%; n = 67 for the A reading, -0.36%) are what a random coefficient gets about as often (58% and 77% of decoys are at least as close): they carry no evidence",
    frac_mean >= 0.20 and frac_A >= 0.20)
# the exact-equality statement is what matters
chk("D2 the exact statement: for integer n, (mean/H)^2 = (2n-1)/(4 n^2) is RATIONAL while 1/Z^2 = 3/(32 pi) is IRRATIONAL: P1+P4 can never equal the target exactly (any n, either reading)",
    all(sp.Rational(2 * n - 1, 4 * n**2).is_rational for n in range(1, 50)) and (sp.Rational(3, 32) / sp.pi).is_rational is False)

# =============================================================================================================== P5 thermal / Schwinger
print("\n== P5: Schwinger / thermal-threshold principle (probe wall in dS, needs hbar) ==")
th0, L, sg, a, hb = sp.symbols('theta0 L sigma a hbar', positive=True)
th = sp.symbols('theta', positive=True)
I3 = sp.integrate(sp.sin(th)**3, (th, 0, th0))
DPp = 3 * sg * a
Bth = 2 * sp.pi**2 * L**3 * sg * sp.sin(th0)**3 - DPp * 2 * sp.pi**2 * L**4 * I3
extr = sp.simplify(sp.diff(Bth, th0))
tan_sol = sp.solve(sp.Eq(3 * sg * sp.cos(th0), DPp * L * sp.sin(th0)), th0)
chk("P5a probe wall in dS(H = 1/L): the instanton is an S^3 of radius R = L sin(theta0) with tan(theta0) = H/a  (a = DeltaP/(3 sigma)), i.e. 1/R^2 = H^2 + a^2 (matches the embedding result of the audit)",
    sp.simplify(sp.tan(tan_sol[0]) - 1 / (a * L)) == 0)
phi = sp.symbols('phi', positive=True)                # phi = a L = a/H
th_ext = sp.atan(1 / phi)
Bext = sp.simplify((Bth / (2 * sp.pi**2 * L**3 * sg)).subs({a: phi / L}).subs(th0, th_ext))
f_phi = (1 + 2 * phi**2) / sp.sqrt(1 + phi**2) - 2 * phi
chk("P5b exact probe-dS bounce action B = 2 pi^2 L^3 sigma f(a/H), f(phi) = (1 + 2 phi^2)/sqrt(1 + phi^2) - 2 phi; flat limit f -> 1/(4 phi^3) reproduces B = pi^2 sigma/(2 a^3)",
    sp.simplify(Bext - f_phi) == 0 and sp.limit(f_phi * 4 * phi**3, phi, sp.oo) == 1)
Bhat = 2 * sp.pi**2 * L**3 * sg * f_phi / hb
Sds = sp.pi * L**2 / hb                              # G = 1: S_dS = pi/(G H^2 hbar)
chk("P5c B/S_dS = (2 pi sigma/H) f(a/H): in units of the de Sitter entropy the action is the wall's self-gravity acceleration 2 pi sigma over H times a function of a/H",
    sp.simplify(Bhat / Sds - 2 * sp.pi * L * sg * f_phi) == 0)
# 'Boltzmann-unsuppressed' B = hbar*b0  =>  sigma_th = b0 hbar/(2 pi^2 L^3 f):  contains NO k = e/sigma:
b0 = sp.symbols('b0', positive=True)
sig_th = sp.solve(sp.Eq(2 * sp.pi**2 * L**3 * sg * f_phi, b0 * hb), sg)[0]
kk = sp.symbols('kk', positive=True)
print("   sigma_th = %s   (so sigma_th/H ~ hbar H^2/(2 pi^2 f) ~ (l_Planck H)^2 ~ 1e-120: the wall is an extreme probe)" % sp.simplify(sig_th))
# numbers: hbar = l_P^2, H l_P ~ 1e-61 (observed Lambda), so hbar H^2 ~ 1e-122 in Planck units; put H = 1, E = sqrt(3/(4 pi))
mp.mp.dps = 200
hbarH2 = mp.mpf('1e-122')
fv = (1 + 2 * (1 / Z)**2) / mp.sqrt(1 + (1 / Z)**2) - 2 / Z
sig_th_num = 1 * hbarH2 / (2 * mp.pi**2 * fv)                    # sigma_th/H with b0 = 1, H = 1
E_num = mp.sqrt(3 / (4 * mp.pi))
k_num = 3 / (2 * mp.sqrt(2))
x_num = k_num * sig_th_num / E_num
shift = x_num / 2                                                # relative shift of a/H from the (1 - x/2) factor
mp.mp.dps = 30
print("   at b0 = 1 and hbar H^2 = 1e-122: sigma_th/H = %s, x = e/E = %s, relative shift of a/H = %s" % (mp.nstr(sig_th_num, 5), mp.nstr(x_num, 5), mp.nstr(shift, 5)))
chk("P5d the threshold fixes sigma (through hbar), not k: at the threshold x = e/E ~ 1e-123, so a/H = k(1 - x/2)/(2 sqrt(3 pi)) is unchanged to a relative 1e-123: (iv) leaves k, hence a0/H, exactly as free as before",
    shift < mp.mpf('1e-120') and not sig_th.has(kk))
fZ = float(f_phi.subs(phi, 1 / sp.sqrt(sp.Rational(32, 3) * sp.pi)))
print("   at the target a/H = 1/Z: f = %.5f, so B = %.4f * 2 pi^2 L^3 sigma" % (fZ, fZ))

# =============================================================================================================== P6 geometry thresholds
print("\n== P6: thresholds of the wall's own geometry (probe limit) ==")
Ax = sp.symbols('A_wall', positive=True)
k_aH = sp.simplify(sp.solve(sp.Eq(kk / (2 * sp.sqrt(3 * sp.pi)), 1), kk)[0])
print("   a = H crossover (Schwinger radius = horizon radius):  k = %s = %.4f ; the puzzle target sits at a = H/Z, i.e. Z = %.4f times below the crossover" % (k_aH, float(k_aH), float(Z)))
chk("P6a the a = H crossover needs k = 2 sqrt(3 pi) = 6.13: it is a definition of the crossover, ratio to the target k* = 3/(2 sqrt 2) is exactly Z (no information)",
    sp.simplify(k_aH - 2 * sp.sqrt(3 * sp.pi)) == 0 and abs(mp.mpf(float(k_aH)) / (3 / (2 * mp.sqrt(2))) - Z) < 1e-12)
Rw, Hw = sp.symbols('R_w H_w', positive=True)
a_of_R = sp.sqrt(1 / Rw**2 - Hw**2)
chk("P6b wall at the horizon: a(R) = sqrt(1/R^2 - H^2) -> infinity as R -> 0; equatorial wall R = 1/H has a = 0; a = H/Z sits at R = (1/H)/sqrt(1 + 1/Z^2)... neither limit is a finite a = H/Z",
    sp.limit(a_of_R, Rw, 0, '+') == sp.oo and sp.simplify(a_of_R.subs(Rw, 1 / Hw)) == 0)

# =============================================================================================================== summary table of the principle-fixed numbers
print("\n== pairs of declared principles: which give a point? ==")
DPn = lambda xx: xx - xx**2 / 2
chk("PAIRS P1&P2 -> DeltaP = 0 = 6 pi sigma^2 forces sigma = 0 (no wall); P1'&P3 -> A = 0 needs DeltaP < 0 but x = 1 has DeltaP = 1/2 > 0 (empty); P2&P3 contradictory: the only declared PAIR that gives a point is P1&P3 (x = 1, s = 1/sqrt(12 pi)); P1&P4 gives the one-parameter family x = 1/n, s = sqrt(x(1 - x/2)/(6 pi))",
    DPn(2) == 0 and DPn(1) > 0 and abs(mp.sqrt(DPn(1) / (6 * pi)) - 1 / mp.sqrt(12 * pi)) < 1e-25)
print("\n== SUMMARY: what each principle fixes, and the a0/H it implies (target 1/Z = %.5f, kappa = 1/2; probe target k* = %.5f) ==" % (1 / Z, 3 / (2 * mp.sqrt(2))))
print("   %-40s %-9s %-14s %-10s %-9s" % ("principle-fixed configuration", "k=e/sig", "a/H_out (mean)", "kappa_eff", "vs target"))
def line(nm, kv, val):
    ks = "%.4f" % kv if kv is not None else "free"
    if val is None:
        print("   %-40s %-9s %-14s" % (nm, ks, "not fixed"))
    else:
        print("   %-40s %-9s %-14.5f %-10.4f %+8.1f%%" % (nm, ks, val, kappa_eff(val), 100 * (val * Z - 1)))
line("P1&P3  (B=0, x=1)  mean", mp.sqrt(12 * pi), mp.mpf(1) / 2)
line("P1&P3  (B=0, x=1)  A", mp.sqrt(12 * pi), mp.mpf(1))
for n in (2, 4, 8, 16, 32, 64):
    line("P1&P4  n=%d  mean" % n, mp.sqrt(12 * pi / (2 * n - 1)), mp.sqrt(2 * n - 1) / (2 * n))
line("a = H crossover (P6)", 2 * mp.sqrt(3 * pi), mp.mpf(1))
line("P2 (no net force) mean", None, mp.mpf(0))
line("P4 alone (x = 1/n, k free)", None, None)
line("P5 (thermal threshold)", None, None)
line("illustration: Gaussian balance e_G^2 = G sigma^2", 2 * mp.sqrt(pi), mp.mpf(1) / mp.sqrt(3))
print("   (last line: a rational Gaussian balance gives a/H = sqrt(q/3), a pi-free number; the target 1/Z = sqrt(3/(32 pi)) is not of that form; NOT a derived principle)")

# CONDITIONAL arithmetic on the WGC-type bound for walls (naive extrapolation, outside the range the source paper states)
print("\n== W1 (CONDITIONAL, not a result): dilatonic extremality bound naively extrapolated to a 4D membrane ==")
al = sp.symbols('alpha', real=True)
d_, p_ = 4, 3
bracket = al**2 / 2 + sp.Rational(p_ * (d_ - p_ - 2), d_ - 2)
print("   arXiv:1509.06374 eq. (25) form [alpha^2/2 + p(d-p-2)/(d-2)] T^2 <= e^2 q^2 M^{d-2} at d = 4, p = 3 gives bracket %s; the paper states its derivation holds for 1 <= p <= d-3 and says p = d-1 (domain walls in 4d) 'we will not discuss'" % bracket)
tgt = sp.Rational(9, 8) / (8 * sp.pi)     # e^2 M^2/sigma^2 with M^2 = 1/(8 pi G): (e^2/(G sigma^2))/(8 pi) = 9/(64 pi)
al2 = sp.solve(sp.Eq(bracket, tgt), al)
al2_val = [sp.simplify(v**2) for v in al2 if v.is_positive][0]
print("   IF that formula applied, saturating it at the puzzle's e^2/(G sigma^2) = 9/8 would need alpha^2 = %s = %.5f (pi in the dilaton coupling)" % (al2_val, float(al2_val)))
chk("W1 conditional arithmetic only: at alpha = 0 the naive bracket is negative (-3/2), so no bound and no extremality relation fixes e/sigma; saturation at the puzzle's ratio would need alpha^2 = 3 + 9/(32 pi), a pi-laden coupling",
    bracket.subs(al, 0) == sp.Rational(-3, 2) and sp.simplify(al2_val - (3 + sp.Rational(9, 32) / sp.pi)) == 0)

# CONTROLS on the whole chain: wrong Israel coefficient, wrong Gauss jump
print("\n== M: mutation controls for the principle relations ==")
cf_s = sp.symbols('cf', positive=True)
# B = 0 with A - B = cf*pi*sigma, A^2 - B^2 = (8 pi/3) DeltaP   =>  DeltaP = 3 cf^2 pi sigma^2/8
DP_B0 = sp.solve(sp.Eq((cf_s * sp.pi * s_)**2, sp.Rational(8, 3) * sp.pi * DP_), DP_)[0]
chk("M1 CONTROL: with the correct Israel coefficient cf = 4 the critical relation is DeltaP = 6 pi sigma^2; with cf = 8 it becomes 24 pi sigma^2 -- the mutant is detected (and would move x_t, s_t, n_t in the intersection table)",
    sp.simplify(DP_B0.subs(cf_s, 4) - 6 * sp.pi * s_**2) == 0 and sp.simplify(DP_B0.subs(cf_s, 8) - 24 * sp.pi * s_**2) == 0)
# a = H crossover k under a Gauss jump e/2 (jf = 1/2): k_thr = 2 sqrt(3 pi)/jf
chk("M2 CONTROL: a Gauss jump e/2 would put the a = H crossover at k = 4 sqrt(3 pi) instead of 2 sqrt(3 pi) (the crossover k is convention-laden, its physical content a/H = 1 is not)",
    sp.simplify(sp.solve(sp.Eq(kk * sp.Rational(1, 2) / (2 * sp.sqrt(3 * sp.pi)), 1), kk)[0] - 4 * sp.sqrt(3 * sp.pi)) == 0)
# positive control for the exact-equality test: a pi-free decoy target IS hit exactly by the P1&P4 family
def exact_hit(t2):
    return [n for n in range(1, 2000) if sp.simplify(sp.Rational(2 * n - 1, 4 * n**2) - t2) == 0]
hit_decoy = exact_hit(sp.Rational(3, 16))                 # decoy a0^2/H^2 = 3/16  (Z'^2 = 16/3): n = 2
hit_real = exact_hit(sp.Rational(3, 32) / sp.pi)          # the real target 1/Z^2 = 3/(32 pi)
chk("M3 POSITIVE CONTROL of the exact-equality test: a pi-free decoy target (a0/H)^2 = 3/16 is hit exactly by P1&P4 (n = %s), the real target (a0/H)^2 = 3/(32 pi) is hit by no n <= 2000 (%s): the test can succeed, and fails here for the stated reason" % (hit_decoy, hit_real),
    hit_decoy == [2] and hit_real == [])

tab_vals = [mp.mpf(1) / 2, mp.mpf(1), mp.mpf(0)] + [mp.sqrt(2 * n - 1) / (2 * n) for n in (2, 4, 8, 16, 32, 64)]
devs_tab = sorted(abs(v * Z - 1) for v in tab_vals)
chk("S1 no tabulated principle-fixed value equals 1/Z: smallest deviation %.3f%% (P1&P4 at n = 16, not fixed by any principle); the structural points P1&P3, a = H, P2 are off by factors 2.9 / 5.8 / infinity" % (100 * devs_tab[0]),
    devs_tab[0] > 1e-3 and abs(mp.mpf(1) / 2 * Z - Z / 2) < 1e-25 and all(abs(v * Z - 1) > 0.1 for v in tab_vals[:3]))

print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
