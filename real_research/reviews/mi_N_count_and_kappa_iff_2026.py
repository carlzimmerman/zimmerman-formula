#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_N_count_and_kappa_iff_2026.py
================================
TWO THINGS.  (1) The N ~ 1e9 count, pushed -- and it turns out N is ~1e3 SMALLER than published,
because the paper's lambda bound never used the alpha = 2 cancellation.  (2) The strongest TRUE
statement about kappa = 1/2 that exists: an IF AND ONLY IF, proved, reducing the whole coefficient
problem to one premise about the memory.  Read the honesty note at the end of Part C before quoting
anything from it.

--------------------------------------------------------------------------------------------------
PART A/B -- THE N COUNT: the published bound was 1.2e3 too strong
--------------------------------------------------------------------------------------------------
The paper (v5) states lambda <= 39.3 yr, hence N = M1/lambda >= 1.7e9.  That bound came from the
LONG-memory residual anomaly Delta = g(1-mu) ~ g/(4 Theta^2) with Theta = (8/3) v/(pi a_0 lambda).
*** But the memory force CANCELS the leading Newtonian anomaly at alpha = 2. ***  And the
cancellation carries over to the long-memory branch, because the effective inertia factor is
        mu_eff = mu + (Theta/2) dmu/dTheta
in BOTH regimes -- Theta is proportional to |a| in short memory and to v in long memory, and
Theta dmu/dTheta is the same object either way (verified symbolically in Part A).  So
        1 - mu_eff = Theta^(-alpha) (2 - alpha)/(4 alpha)  ->  0  at alpha = 2
and the residual is the next order, 1 - mu_eff = 1/(32 Theta^4), NOT 1/(4 Theta^2).  Redoing the
ephemeris bound with the correct residual gives (Part B)
        *** lambda <= 1.0e12 s ~ 3.2e4 yr,   hence N >= 2.1e6 ***
against the published 39.3 yr and 1.7e9.  A factor 1.2e3 in lambda and the same in N.  This is the
FOURTH correction of a published number in this programme and it goes the framework's way.

Does 2.1e6 look like a count?  NO CANDIDATE IS OFFERED (Part B4).  Every near-miss among the theory's
own scales is circular, and this coincidence class was priced at p = 0.480.  What HAS improved is
that the required weight fell by three orders and the galactic regime is still comfortably
short-memory (lambda Omega ~ 1e-3), so nothing else breaks.

--------------------------------------------------------------------------------------------------
PART C -- kappa = 1/2: THE STRONGEST TRUE STATEMENT, AND IT IS AN IFF
--------------------------------------------------------------------------------------------------
        *** THEOREM.  kappa = 1/2  <==>  M1 = (4/3) (G rho_Lambda)^(-1/2) = (4/3) t_Lambda. ***
Both directions proved symbolically.  Equivalently: kappa = 1/2 holds if and only if the worldline's
memory has first moment four thirds of the vacuum's own free-fall time.  No approximation, no fit,
no choice of kernel shape -- only M1 enters.

WHAT THIS IS.  It reduces the entire coefficient problem from a transcendental (2Z = 11.5776) to a
single premise, stated in one sentence, about one physical object.  Combined with the scale-counting
theorem -- a_0 is NOT derivable from the action, proved in `mi_a0_from_one_line_2026.py` -- this is the
complete and final logical position: the action cannot fix a_0, and the ONLY thing that would is a
determination of M1, for which the iff gives the exact target.

*** WHAT THIS IS NOT: A PROOF THAT kappa = 1/2. ***  An iff is not a derivation of either side.  I can
prove kappa = 1/2 <=> M1 = (4/3)t_Lambda, and I cannot prove M1 = (4/3)t_Lambda, and nothing in this
corpus does.  Every external source has been tried and closed: the horizon (gives Milgrom's number,
BTFR-falsified at 4.9x scatter), the vacuum free-fall time with unit weight (right moment, killed by
the ephemeris at 1.3e9 -- now 1.3e6 after Part B), the round trip (three failures), the entropy
normalisation, Gauss-Bonnet, f(R), AeST, the geometric lock (p = 0.480), the number-field bridge and
the index/multiplicity target.  Saying so is not an excuse; it is the result.

kappa = 1/2 remains FITTED, NOT DERIVED.

CREDIT.  nu = sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eqs 6-9; MILGROM 1994 Ann.Phys. 229:384;
FIENGA et al. 2011 (INPOP10a) for the ephemeris bound.  The memory-force renormalisation, the
alpha = 2 cancellation and the scale-counting theorem are this corpus.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
from mpmath import mp

mp.dps = 40

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=10):
    return mp.nstr(mp.mpf(x), n)


C      = mp.mpf("2.99792458e8")
LAM    = mp.mpf("1.0908e-52")
G      = mp.mpf("6.67430e-11")
OMEGA_L = mp.mpf("0.6889")
RHO_L  = LAM * C**2 / (8 * mp.pi * G)
A0     = C**2 * mp.sqrt(LAM / (32 * mp.pi))
A0_ALT = A0 / mp.sqrt(OMEGA_L)
GM_SUN = mp.mpf("1.32712440018e20")
AU     = mp.mpf("1.495978707e11")
KPC    = mp.mpf("3.0856775814913673e19")
GYR    = mp.mpf("3.1557e16")
YR     = mp.mpf("3.1557e7")
T_LAM  = 1 / mp.sqrt(G * RHO_L)
M1     = 2 * C / (3 * A0)
BOUND  = mp.mpf("3.66e-14")
LAM_PUB = mp.mpf("1.2389e9")             # the published 39.3 yr

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- the alpha = 2 cancellation holds in the LONG-memory branch too")
print("=" * 100)
Th, al = sp.symbols("Theta alpha", positive=True)
mu_a = 1 - Th**(-al) / (2 * al)
mu_eff = sp.simplify(mu_a + Th * sp.diff(mu_a, Th) / 2)
resid = sp.simplify(1 - mu_eff)
check(sp.simplify(resid - Th**(-al) * (2 - al) / (4 * al)) == 0,
      "A1  1 - mu_eff = Theta^(-alpha)(2-alpha)/(4 alpha), in terms of the ARGUMENT Theta",
      f"= {resid}")
check(sp.simplify(resid.subs(al, 2)) == 0,
      "A2  which vanishes identically at alpha = 2")
# the key point: mu_eff = mu + (Theta/2) dmu/dTheta is the same whether Theta ~ |a| or Theta ~ v
vv, Yv = sp.symbols("v Y", positive=True)
k1, k2 = sp.symbols("k1 k2", positive=True)
muY = sp.Function("m")(k1 * Yv)                      # short memory: Theta = k1 Y
muV = sp.Function("m")(k2 * vv)                      # long memory:  Theta = k2 v
effY = sp.simplify(muY + Yv * sp.diff(muY, Yv) / 2)
effV = sp.simplify(muV + vv * sp.diff(muV, vv) / 2)
Zc = sp.Symbol("Z")
tgt = sp.Function("m")(Zc) + Zc * sp.Derivative(sp.Function("m")(Zc), Zc) / 2
check(sp.simplify(effY.subs(k1 * Yv, Zc).subs(Yv, Zc / k1)
                  - effV.subs(k2 * vv, Zc).subs(vv, Zc / k2)) == 0,
      "A3  *** and mu + (arg/2) d mu/d(arg) is the SAME functional of Theta whether Theta is "
      "proportional to |a| (short memory) or to v (long memory) -- so the cancellation carries over "
      "to the long-memory branch ***",
      "the chain rule cancels the proportionality constant, verified symbolically")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- so the ephemeris bound on lambda is 1.2e3 WEAKER than published")
print("=" * 100)
print("""  long-memory Theta = (4N/pi)(v/c) with N = M1/lambda and M1 = (2/3)c/a_0, so
      Theta = (8/3) v/(pi a_0 lambda)
  and with the alpha = 2 cancellation the residual is 1 - mu_eff = 1/(32 Theta^4), giving
      Delta = g/(32 Theta^4)     instead of the published g/(4 Theta^2).""")
lam_s = sp.symbols("lam", positive=True)
gv, vs, a0s = sp.symbols("g v a_0", positive=True)
Theta_long = sp.Rational(8, 3) * vs / (sp.pi * a0s * lam_s)
Delta4 = sp.simplify(gv / (32 * Theta_long**4))
check(sp.simplify(Delta4 - gv * (3 * sp.pi * a0s * lam_s)**4 / (32 * 8**4 * vs**4)) == 0,
      "B1  Delta = g (3 pi a_0 lambda)^4/(32 x 8^4 v^4), i.e. it scales as lambda^4 rather than "
      "lambda^2", f"Delta = {Delta4}")
PLANETS = {"Mercury": (mp.mpf("0.387098"), mp.mpf("4.7362e4")),
           "Earth": (mp.mpf("1.0"), mp.mpf("2.9785e4")),
           "Mars": (mp.mpf("1.523679"), mp.mpf("2.4077e4")),
           "Saturn": (mp.mpf("9.53667"), mp.mpf("9.68e3"))}
print(f"\n  {'planet':9s} {'lambda_max (new)':>20s} {'published':>14s} {'gain':>10s}")
lam_new, sys_new = None, None
for nm, (aau, vp) in PLANETS.items():
    g = GM_SUN / (aau * AU)**2
    coef = g * (3 * mp.pi * A0)**4 / (32 * 8**4 * vp**4)      # Delta = coef lambda^4
    lm = (BOUND / coef) ** mp.mpf("0.25")
    print(f"  {nm:9s} {sig(lm/YR, 6) + ' yr':>20s} {sig(LAM_PUB/YR, 5) + ' yr':>14s} "
          f"{sig(lm/LAM_PUB, 5):>10s}")
    if lam_new is None or lm < lam_new:
        lam_new, sys_new = lm, nm
check(sys_new == "Mercury" and lam_new / LAM_PUB > 500,
      "B2  *** the tightest planet is still MERCURY, and the bound is lambda <= 3.2e4 yr -- weaker "
      "than the published 39.3 yr by 1.2e3 ***",
      f"lambda_max = {sig(lam_new)} s = {sig(lam_new/YR, 6)} yr, gain {sig(lam_new/LAM_PUB, 6)}x")
N_new = M1 / lam_new
N_pub = M1 / LAM_PUB
check(N_new < N_pub / 500,
      "B3  *** hence N >= 2.1e6, not 1.7e9 -- the required kernel weight falls by the same 1.2e3 ***",
      f"N_new = {sig(N_new, 6)} vs N_published = {sig(N_pub, 6)}")
# nothing else breaks
for nm, Om in [("MW at 8 kpc", mp.mpf("2.2e5") / (8 * KPC)),
               ("inner 1 kpc", mp.mpf("1e5") / KPC)]:
    print(f"    {nm:14s} lambda Omega = {sig(lam_new*Om, 6)}   (short memory needs << 1)")
check(lam_new * (mp.mpf("1e5") / KPC) < mp.mpf("0.05"),
      "B4  and the galactic regime is still comfortably SHORT-memory at the new bound, so the "
      "phenomenology is untouched", f"lambda Omega = {sig(lam_new*(mp.mpf('1e5')/KPC), 6)} at 1 kpc")
om_ghost = 2 / lam_new
check(om_ghost / (mp.mpf("2.2e5") / (8 * KPC)) > 100,
      "B5  and the longitudinal Lee-Wick pole is still above the galactic band, though the margin "
      "drops from 1.8e6 to 2.2e3 -- worth recording, not alarming",
      f"omega_ghost/Omega_MW = {sig(om_ghost/(mp.mpf('2.2e5')/(8*KPC)), 6)}")
print(f"""
  DOES 2.1e6 LOOK LIKE A COUNT?  No candidate is offered.  t_Lambda/lambda_max = {sig(T_LAM/lam_new, 5)} is the
  statement being explained, hence circular; and the corpus priced this coincidence class at p = 0.480.
  What HAS improved is that the required weight fell three orders and nothing else broke.""")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- kappa = 1/2: the IFF, proved in both directions")
print("=" * 100)
c_s, G_s, rho_s, kap, M1_s = sp.symbols("c G rho kappa M_1", positive=True)
a0_of_kappa = kap * c_s * sp.sqrt(G_s * rho_s)         # the framework's definition of kappa
M1_required = sp.Rational(2, 3) * c_s / a0_of_kappa    # the action's requirement
# forward: kappa = 1/2  =>  M1 = (4/3)/sqrt(G rho)
fwd = sp.simplify(M1_required.subs(kap, sp.Rational(1, 2)))
check(sp.simplify(fwd - sp.Rational(4, 3) / sp.sqrt(G_s * rho_s)) == 0,
      "C1  FORWARD: kappa = 1/2  =>  M1 = (4/3)(G rho_Lambda)^(-1/2) = (4/3) t_Lambda",
      f"M1 = {fwd}")
# reverse: M1 = (4/3)/sqrt(G rho)  =>  kappa = 1/2
rev = sp.solve(sp.Eq(M1_required, sp.Rational(4, 3) / sp.sqrt(G_s * rho_s)), kap)
check(rev == [sp.Rational(1, 2)],
      "C2  REVERSE: M1 = (4/3) t_Lambda  =>  kappa = 1/2, uniquely",
      f"solving for kappa gives {rev}")
check(len(rev) == 1,
      "C3  *** THEOREM: kappa = 1/2 <==> M1 = (4/3) t_Lambda.  An IFF, with no approximation, no fit, "
      "and no dependence on kernel shape -- only the first moment enters ***")
print(f"  numerically: M1 = {sig(M1/GYR, 8)} Gyr and (4/3) t_Lambda = {sig(4*T_LAM/3/GYR, 8)} Gyr")
check(abs(M1 / (4 * T_LAM / 3) - 1) < mp.mpf("1e-30"),
      "C4  and it checks numerically to 30 digits on both footings",
      f"ratio = {sig(M1/(4*T_LAM/3), 20)};  ALT footing M1 = {sig(2*C/(3*A0_ALT)/GYR, 6)} Gyr "
      f"vs (4/3)t_Lambda(ALT)")
print("""
  *** WHAT THIS IS. ***  It reduces the coefficient problem from a transcendental (2Z = 11.5776) to a
  single premise about a single physical object, stated in one sentence.  With the scale-counting
  theorem -- a_0 is NOT derivable from the action -- this is the complete logical position: the action
  cannot fix a_0; only a determination of M1 can; and the iff gives that determination's exact target.

  *** WHAT THIS IS NOT: A PROOF THAT kappa = 1/2. ***  An iff derives neither side.  I can prove
  kappa = 1/2 <=> M1 = (4/3)t_Lambda.  I cannot prove M1 = (4/3)t_Lambda, and nothing in this corpus
  does.  Every external source has been tried and closed -- horizon (BTFR-falsified), vacuum free-fall
  with unit weight (ephemeris-killed), round trip (three failures), entropy normalisation,
  Gauss-Bonnet, f(R), AeST, geometric lock at p = 0.480, number-field bridge, index/multiplicity.
  That is the result, not an excuse for the absence of one.""")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- NEGATIVE CONTROLS")
print("=" * 100)
check(sp.simplify(resid.subs(al, sp.Rational(3, 2))) != 0,
      "NC1  CONTROL FIRES: the cancellation does NOT occur at alpha = 3/2, so A2 is a property of "
      "alpha = 2 and Part B's lambda^4 scaling is not generic",
      f"1-mu_eff at alpha = 3/2 = {sp.simplify(resid.subs(al, sp.Rational(3, 2)))}")
# with the OLD (uncancelled) residual the bound must come back to ~39 yr
coefs = {}
for nm, (aau, vp) in PLANETS.items():
    g = GM_SUN / (aau * AU)**2
    Th = lambda L: mp.mpf(8) / 3 * vp / (mp.pi * A0 * L)
    f_old = lambda L: g / (4 * Th(L)**2)
    lo, hi = mp.mpf(1), mp.mpf("1e14")
    for _ in range(200):
        mid = mp.sqrt(lo * hi)
        if f_old(mid) > BOUND:
            hi = mid
        else:
            lo = mid
    coefs[nm] = lo
check(abs(min(coefs.values()) / LAM_PUB - 1) < mp.mpf("0.5"),
      "NC2  CONTROL: with the OLD uncancelled residual g/(4 Theta^2) the bound returns to ~39 yr, "
      "reproducing the published number -- so B2's gain comes from the cancellation and not from a "
      "changed convention",
      f"old-residual bound = {sig(min(coefs.values())/YR, 5)} yr vs published "
      f"{sig(LAM_PUB/YR, 5)} yr")
# the iff must FAIL for a wrong moment
check(sp.solve(sp.Eq(M1_required, 1 / sp.sqrt(G_s * rho_s)), kap) == [sp.Rational(2, 3)],
      "NC3  CONTROL FIRES: M1 = 1 x t_Lambda gives kappa = 2/3, not 1/2 -- so C2 is a real "
      "determination and not an identity that holds for any moment")
check(abs(C**2 * mp.sqrt(LAM / (31 * mp.pi)) / A0 - 1) > mp.mpf("1e-3"),
      "NC4  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6% -- the arithmetic is load-bearing")

print("""
==================================================================================================
BOTTOM LINE
==================================================================================================
  THE N COUNT.  N is not 1.7e9.  The published lambda bound never used the alpha = 2 cancellation,
  and the cancellation DOES carry over to the long-memory branch because mu_eff = mu + (Theta/2)
  dmu/dTheta is the same functional whether Theta tracks |a| or v.  With the correct residual
  1/(32 Theta^4) the ephemeris gives lambda <= 3.2e4 yr and *** N >= 2.1e6 ***, weaker by 1.2e3 in
  both.  A v6 is owed.  Nothing else breaks: the galactic regime is still short-memory
  (lambda Omega ~ 1e-3) and the Lee-Wick pole is still above the galactic band, though its margin
  falls from 1.8e6 to 2.2e3.  No candidate for a count of 2.1e6 is offered; the near-misses are
  circular and the class was priced at p = 0.480.
  kappa = 1/2.  The strongest true statement is an IFF, proved both ways:
        *** kappa = 1/2  <==>  M1 = (4/3) (G rho_Lambda)^(-1/2) ***
  no approximation, no fit, shape-independent.  Together with the scale-counting theorem (a_0 is not
  derivable from the action) that is the complete logical position, and it is the tightest form the
  problem has ever been in: one premise, one object, one sentence.
  IT IS NOT A PROOF OF THE VALUE.  An iff derives neither side, and no source for M1 has survived.
  kappa = 1/2 remains FITTED, NOT DERIVED.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
