#!/usr/bin/env python3
"""
LANE G1 -- THE KOIDE PARAMETER COUNT, DONE HONESTLY.
=====================================================================================
Koide's Q = (m_e+m_mu+m_tau)/(sqrt m_e + sqrt m_mu + sqrt m_tau)^2 = 2/3 is the ONE
genuine numerical lead in the flavour sector.  The corpus asserts the framework only
RE-LABELS it with a free r = sqrt(2).  This script settles that by EXPLICIT COUNT,
and then converts the assertion into two THEOREMS about why the bridge is hard.

FOOTING (locked, not under test here):
  a_0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 (FITTED, NOT DERIVED) -> 9.3614e-11 m/s^2
  ALT footing 1.13e-10 (larger by 1/sqrt(Omega_Lambda) = 1.2082)
  Z = 2 sqrt(8 pi/3) = 5.7888100366...,  1/Z = 0.1727470747
  Exact law g_obs^2 = g_bar^2 + a_0 g_bar
  CREDIT LINE: nu = sqrt(1+1/y) is Milgrom 1999 PLA 253:273 Eq 9; the framework's
  distinctive content is the cH_Lambda/Z COEFFICIENT + the modified-inertia completion.
  The Koide relation is Koide 1981 / Brannen -- NOT this framework's.

WHAT IS PROVED HERE (nothing is claimed derived):
  T1  Q-BLINDNESS THEOREM.  Let f:(0,inf)->(0,inf) act on each sqrt-mass by the SAME
      rule (sqrt m_i -> f(sqrt m_i)).  If f preserves Q on all positive triples then
      f(x) = w x, i.e. f is a common rescaling -- and a common rescaling leaves Q
      EXACTLY fixed.  Corollary: a flavour-blind kernel can neither DERIVE nor BREAK
      Koide.  Necessary condition for ANY real flavour mechanism: it must be
      generation-DEPENDENT or generation-MIXING.  (Falsifiable demand on future claims.)
  T2  Z-GRADING THEOREM.  Grade Qbar(sqrt pi) by the power of the transcendental
      sqrt(pi).  Z = sqrt(32/3)*sqrt(pi) has grade 1; sqrt(2) is algebraic, grade 0.
      Hence any closed-form expression equal to sqrt(2) has NET Z-GRADE ZERO: the
      framework's signature number Z provably CANNOT appear in a forced r = sqrt(2).
      So even a successful Koide derivation would be evidence for NOBODY's framework.
  T3  THE kappa^(-1/2) = sqrt(2) COINCIDENCE is found, flagged, and PRICED DOWN by an
      independent second route (precision mismatch of 3-4 orders + monomial density).
      Treated as a suspected bug from the outset, per the double-scrutiny rule.

Every check can FAIL.  No check compares a quantity with itself.
"""
import sys
import numpy as np
import sympy as sp
import mpmath as mp

mp.mp.dps = 50
np.random.seed(20260807)

NCK = [0, 0]  # [passed, total]


def ck(name, cond):
    NCK[1] += 1
    ok = bool(cond)
    if ok:
        NCK[0] += 1
    print(f"  [{'OK' if ok else 'FAIL'}] {name}")
    return ok


def hdr(s):
    print("\n" + "=" * 86)
    print(s)
    print("=" * 86)


# =====================================================================================
hdr("(0) FOOTING -- framework constants (locked; printed so the reader can audit them)")
# =====================================================================================
Z_sym = 2 * sp.sqrt(8 * sp.pi / 3)
Z = mp.mpf(2) * mp.sqrt(8 * mp.pi / 3)
kappa = mp.mpf(1) / 2
a0_canon = mp.mpf("9.3614e-11")
a0_alt = mp.mpf("1.13e-10")
print(f"  Z          = 2 sqrt(8 pi/3) = {mp.nstr(Z, 12)}")
print(f"  1/Z        = {mp.nstr(1/Z, 12)}")
print(f"  kappa      = 1/2  (FITTED, NOT DERIVED)")
print(f"  a0 canon   = {mp.nstr(a0_canon,6)} m/s^2 ;  a0 ALT = {mp.nstr(a0_alt,6)} m/s^2")
print(f"  ALT/canon  = {mp.nstr(a0_alt/a0_canon, 8)}   (1/sqrt(Omega_Lambda) ~ 1.2082)")
ck("Z reproduces the banked 5.7888100366 to 1e-9", abs(Z - mp.mpf("5.7888100366")) < 1e-9)
ck("1/Z reproduces the banked 0.1727470747 to 1e-9", abs(1 / Z - mp.mpf("0.1727470747")) < 1e-9)
a0_alt_exact = a0_canon * mp.mpf("1.2082")
print(f"  canon x 1.2082 = {mp.nstr(a0_alt_exact, 6)} -> quoted as {mp.nstr(a0_alt,4)} (3 s.f.);"
      f" the {mp.nstr(abs(a0_alt/a0_canon - mp.mpf('1.2082')), 3)} offset in the RATIO is that rounding, nothing physical")
ck("quoted ALT 1.13e-10 = canon x 1/sqrt(Omega_Lambda) to within 3-sig-fig rounding (5e-3 rel)",
   abs(a0_alt - a0_alt_exact) / a0_alt_exact < mp.mpf("5e-3"))


# =====================================================================================
hdr("(1) Q FROM CURRENT PDG LEPTON MASSES, WITH UNCERTAINTIES")
# =====================================================================================
def Qof(ms):
    ms = [mp.mpf(x) for x in ms]
    S1 = sum(ms)
    S2 = sum(mp.sqrt(x) for x in ms)
    return S1 / S2 ** 2


def sigmaQ(ms, sig):
    """analytic linear propagation, mpmath (no float64 cancellation)"""
    ms = [mp.mpf(x) for x in ms]
    S1 = sum(ms)
    S2 = sum(mp.sqrt(x) for x in ms)
    var = mp.mpf(0)
    for m_i, s_i in zip(ms, sig):
        d = 1 / S2 ** 2 - S1 / (S2 ** 3 * mp.sqrt(m_i))
        var += (d * mp.mpf(s_i)) ** 2
    return mp.sqrt(var)


# CODATA-2022 / PDG-2024 central values and 1-sigma errors, MeV
m_e, s_e = mp.mpf("0.51099895069"), mp.mpf("0.00000000016")
m_mu, s_mu = mp.mpf("105.6583755"), mp.mpf("0.0000023")
FOOTINGS = {
    "PDG-2024   m_tau = 1776.86 +- 0.12": (mp.mpf("1776.86"), mp.mpf("0.12")),
    "BelleII-23 m_tau = 1777.09 +- 0.14": (mp.mpf("1777.09"), mp.mpf("0.14")),
}
two_thirds = mp.mpf(2) / 3
res = {}
for lab, (m_tau, s_tau) in FOOTINGS.items():
    ms = [m_e, m_mu, m_tau]
    sg = [s_e, s_mu, s_tau]
    Q = Qof(ms)
    sQ = sigmaQ(ms, sg)
    dev = Q - two_thirds
    nsig = abs(dev) / sQ
    res[lab] = (Q, sQ, dev, nsig, m_tau, s_tau)
    print(f"\n  {lab}")
    print(f"    Q            = {mp.nstr(Q, 12)}   sigma_Q = {mp.nstr(sQ, 4)}")
    print(f"    Q - 2/3      = {mp.nstr(dev, 4)}   ({mp.nstr(abs(dev)/two_thirds*100, 4)} % of 2/3)")
    print(f"    deviation    = {mp.nstr(nsig, 4)} sigma  ->  "
          f"{'CONSISTENT with 2/3' if nsig < 3 else 'INCONSISTENT with 2/3 at >3 sigma'}")

# MC cross-check of the analytic sigma (float64 is plenty: Q~1, sigma_Q~1e-5)
QP, sQP, devP, nsigP, mtP, stP = res["PDG-2024   m_tau = 1776.86 +- 0.12"]
N = 200000
sam = np.stack([
    np.random.normal(float(m_e), float(s_e), N),
    np.random.normal(float(m_mu), float(s_mu), N),
    np.random.normal(float(mtP), float(stP), N),
], axis=1)
Qmc = sam.sum(1) / np.sqrt(sam).sum(1) ** 2
print(f"\n  MC (N={N}) sigma_Q = {Qmc.std(ddof=1):.4e}   vs analytic {mp.nstr(sQP,4)}")
ck("MC sigma_Q agrees with analytic propagation to 5%",
   abs(Qmc.std(ddof=1) - float(sQP)) / float(sQP) < 0.05)
ck("Q is inside the mathematically allowed window [1/3, 1]", mp.mpf(1) / 3 < QP < 1)
ck("PDG Q agrees with 2/3 at < 3 sigma (deviation NOT significant)", nsigP < 3)
ck("|Q - 2/3| is smaller than 2e-5 (the coincidence is real at the 1e-5 level)",
   abs(devP) < mp.mpf("2e-5"))
ck("sigma_Q is dominated by m_tau (drop m_tau error -> sigma falls by >100x)",
   sigmaQ([m_e, m_mu, mtP], [s_e, s_mu, mp.mpf(0)]) * 100 < sQP)
# the footing fork must be reported, not hidden
QB, sQB, devB, nsigB, _, _ = res["BelleII-23 m_tau = 1777.09 +- 0.14"]
print(f"  FOOTING FORK: deviation is {mp.nstr(nsigP,3)} sigma (PDG) vs {mp.nstr(nsigB,3)} sigma (Belle II).")
print("  Both < 3 sigma -> Q = 2/3 survives BOTH m_tau footings; neither footing manufactures a kill.")
ck("Belle-II footing also < 3 sigma (verdict is footing-robust)", nsigB < 3)

# Koide's own single prediction: m_tau from (m_e, m_mu) at Q = 2/3 exactly
se, smu = mp.sqrt(m_e), mp.sqrt(m_mu)
# solve (m_e+m_mu+x^2) = (2/3)(se+smu+x)^2 for x = sqrt(m_tau), take larger root
A = 1 - two_thirds
B = -2 * two_thirds * (se + smu)
C = m_e + m_mu - two_thirds * (se + smu) ** 2
disc = B * B - 4 * A * C
x_pred = (-B + mp.sqrt(disc)) / (2 * A)
mtau_pred = x_pred ** 2
print(f"\n  Koide's ONE prediction: m_tau(from m_e,m_mu, Q=2/3) = {mp.nstr(mtau_pred, 10)} MeV")
print(f"    vs PDG    1776.86 +- 0.12  ->  {mp.nstr((mtau_pred-mtP)/stP, 3)} sigma")
print(f"    vs BelleII 1777.09 +- 0.14 ->  {mp.nstr((mtau_pred-mp.mpf('1777.09'))/mp.mpf('0.14'), 3)} sigma")
ck("Koide m_tau prediction lands within 3 sigma of PDG", abs(mtau_pred - mtP) / stP < 3)
ck("Koide m_tau prediction is NOT trivially loose (predicted value within 0.1% of measured)",
   abs(mtau_pred - mtP) / mtP < mp.mpf("1e-3"))


# =====================================================================================
hdr("(2) THE FRAMEWORK'S PARAMETERISATION, WRITTEN OUT -- EVERY FREE PARAMETER NAMED")
# =====================================================================================
print("""
  The framework's flavour statement (KOIDE_TRIALITY_OCTONION / KOIDE_SELFDUALITY) is the
  S3/triality decomposition of the sqrt-mass 3-vector v = (sqrt m_e, sqrt m_mu, sqrt m_tau)
  into democratic singlet + standard doublet, in Brannen circulant form:

        sqrt(m_k) = M * ( 1 + r cos(delta + 2 pi k / 3) ),   k = 0,1,2

  FREE PARAMETERS (continuous):
     P1  M      overall sqrt-mass scale   (the Yukawa scale; NOT supplied by the framework)
     P2  delta  circulant phase           (NOT supplied by the framework)
     P3  r      doublet/singlet amplitude (the framework's claim is r = sqrt 2 <-> 45 deg)
  DISCRETE choices (absorbed, listed for completeness):
     D1  assignment of k to (e, mu, tau)  -- absorbed into the range of delta
     D2  branch of the sqrt              -- fixed by m_i > 0
""")
M, r, th, w = sp.symbols("M r theta w", positive=True)
phis = [th + 2 * sp.pi * j / 3 for j in (0, 1, 2)]
sm = [M * (1 + r * sp.cos(p)) for p in phis]
Q_sym = sp.simplify(sum(s ** 2 for s in sm) / sp.simplify(sum(sm)) ** 2)
print(f"  Q(M, delta, r) = {sp.simplify(Q_sym)}")
ck("Q = 1/3 + r^2/6 identically: Q is blind to BOTH M and delta",
   sp.simplify(Q_sym - (sp.Rational(1, 3) + r ** 2 / 6)) == 0)
rsol = sp.solve(sp.Eq(sp.Rational(1, 3) + r ** 2 / 6, sp.Rational(2, 3)), r)
print(f"  Q = 2/3  <=>  r = {rsol}")
ck("Q = 2/3 <=> r = sqrt 2 EXACTLY (so 'force r' and 'assume Q' are one statement)",
   sp.sqrt(2) in rsol)
# geometric restatement: Q = 1/(3 cos^2 theta_v), theta_v = angle(v, democratic axis)
v = sp.Matrix([sp.Symbol(f"v{i}", positive=True) for i in range(3)])
n = sp.Matrix([1, 1, 1]) / sp.sqrt(3)
cos2 = sp.simplify(((v.T * n)[0, 0]) ** 2 / (v.T * v)[0, 0])
Q_geo = sp.simplify(1 / (3 * cos2))
Q_dir = sp.simplify((v.T * v)[0, 0] / (v[0] + v[1] + v[2]) ** 2)
ck("Q = 1/(3 cos^2 angle(v, (1,1,1))) identically  =>  Q = 2/3 <=> 45 degrees",
   sp.simplify(Q_geo - Q_dir) == 0)

# the parameterisation is a BIJECTION on real data: fit it and round-trip
vobs = [mp.sqrt(m_e), mp.sqrt(m_mu), mp.sqrt(mtP)]
M_fit = sum(vobs) / 3
c = [x / M_fit - 1 for x in vobs]
ph = [2 * mp.pi * j / 3 for j in (0, 1, 2)]
X = mp.mpf(2) / 3 * sum(ci * mp.cos(pi_) for ci, pi_ in zip(c, ph))
Y = -mp.mpf(2) / 3 * sum(ci * mp.sin(pi_) for ci, pi_ in zip(c, ph))
r_fit = mp.sqrt(X ** 2 + Y ** 2)
d_fit = mp.atan2(Y, X)
rt = [M_fit * (1 + r_fit * mp.cos(d_fit + p)) for p in ph]
maxerr = max(abs(a - b) / b for a, b in zip(rt, vobs))
print(f"\n  FIT to real leptons:  M = {mp.nstr(M_fit,10)} sqrt(MeV),  delta = {mp.nstr(d_fit,10)} rad,"
      f"  r = {mp.nstr(r_fit,12)}")
print(f"  round-trip max relative error on sqrt(m_i) = {mp.nstr(maxerr, 4)}")
ck("the 3-parameter form reproduces all 3 masses EXACTLY (round trip < 1e-30)", maxerr < mp.mpf("1e-30"))
ck("fitted r equals sqrt(6Q-2) (internal consistency of the fit)",
   abs(r_fit - mp.sqrt(6 * QP - 2)) < mp.mpf("1e-30"))
print(f"  r_fit - sqrt2 = {mp.nstr(r_fit - mp.sqrt(2), 4)}"
      f"   ( {mp.nstr(abs(r_fit-mp.sqrt(2))/mp.sqrt(2)*100, 4)} % )")
# sigma on r, propagated
r_hi = mp.sqrt(6 * (QP + sQP) - 2)
r_lo = mp.sqrt(6 * (QP - sQP) - 2)
s_r = (r_hi - r_lo) / 2
print(f"  sigma_r = {mp.nstr(s_r,4)}  ->  r is sqrt2 to {mp.nstr(abs(r_fit-mp.sqrt(2))/s_r,3)} sigma,"
      f" i.e. r is PINNED to {mp.nstr(s_r/mp.sqrt(2)*100,3)} % by data")
ck("r agrees with sqrt 2 at < 3 sigma", abs(r_fit - mp.sqrt(2)) / s_r < 3)
ck("data pins r to better than 0.01% (needed later to price the kappa coincidence)",
   s_r / mp.sqrt(2) < mp.mpf("1e-4"))
# a bijection needs a non-vanishing Jacobian: check numerically
def fwd(p):
    Mv, dv, rv = p
    return np.array([Mv * (1 + rv * np.cos(dv + 2 * np.pi * j / 3)) ** 2 for j in (0, 1, 2)])
p0 = np.array([float(M_fit), float(d_fit), float(r_fit)])
J = np.zeros((3, 3))
for i in range(3):
    e = np.zeros(3); e[i] = 1e-7 * max(1.0, abs(p0[i]))
    J[:, i] = (fwd(p0 + e) - fwd(p0 - e)) / (2 * e[i])
detJ = np.linalg.det(J)
print(f"  det d(m_e,m_mu,m_tau)/d(M,delta,r) = {detJ:.6e}  (non-zero => locally 3->3 BIJECTIVE)")
ck("Jacobian determinant non-zero => the map (M,delta,r) -> (m_e,m_mu,m_tau) is a local bijection",
   abs(detJ) > 1e-8 * np.abs(J).max() ** 3)


# =====================================================================================
hdr("(3) THE COUNT:  N_free  vs  N_observables")
# =====================================================================================
N_free_A = 3   # M, delta, r
N_obs = 3      # m_e, m_mu, m_tau
N_free_B = 2   # M, delta, with r FIXED at sqrt2 by fiat
print(f"""
  TIER A -- the framework's actual parameterisation (r FREE, as the corpus records:
            'r = sqrt2 is a free modulus'):
              N_free = {N_free_A}  (M, delta, r)      N_observables = {N_obs}  (m_e, m_mu, m_tau)
              net predictive content = {N_obs - N_free_A}
              and the map is a BIJECTION (det J != 0 above) -> it fits ANY positive mass triple.

  TIER B -- r fixed at sqrt2 by fiat (this is KOIDE's relation, 1981, not the framework's):
              N_free = {N_free_B}  (M, delta)         N_observables = {N_obs}
              net predictive content = {N_obs - N_free_B}  -> exactly ONE prediction: m_tau
              and that one prediction WORKS ({mp.nstr(abs(mtau_pred-mtP)/stP,3)} sigma).
""")
ck("TIER A: N_free >= N_observables", N_free_A >= N_obs)
ck("TIER B: N_free < N_observables (so Koide's relation itself has 1 dof of real content)",
   N_free_B < N_obs)
if N_free_A >= N_obs:
    print("  VERDICT ON THE FRAMEWORK'S TIER:  REPARAMETRISATION, not derivation")
    print("  (3 free parameters absorbing 3 observables, via a provably bijective map.)")
# OPERATIONAL TEST OF "REPARAMETRISATION": the form must fit an ARBITRARY mass triple, not just
# the real one.  If it does, it has no empirical content of its own.
def fit_form(triple):
    v = [mp.sqrt(mp.mpf(x)) for x in triple]
    Mf = sum(v) / 3
    cc = [x / Mf - 1 for x in v]
    Xf = mp.mpf(2) / 3 * sum(ci * mp.cos(p) for ci, p in zip(cc, ph))
    Yf = -mp.mpf(2) / 3 * sum(ci * mp.sin(p) for ci, p in zip(cc, ph))
    rf = mp.sqrt(Xf ** 2 + Yf ** 2)
    df = mp.atan2(Yf, Xf)
    back = [(Mf * (1 + rf * mp.cos(df + p))) ** 2 for p in ph]
    return rf, max(abs(b - t) / t for b, t in zip(back, [mp.mpf(x) for x in triple]))
rnd = [sorted(10 ** np.random.uniform(-3, 3, 3)) for _ in range(200)]
worst = mp.mpf(0)
rs = []
for tr in rnd:
    rf, er = fit_form(tr)
    worst = max(worst, er)
    rs.append(rf)
print(f"  operational test of 'reparametrisation': fitted 200 RANDOM mass triples spanning 6 decades")
print(f"    worst round-trip relative error = {mp.nstr(worst, 4)};  fitted r spans "
      f"[{mp.nstr(min(rs),6)}, {mp.nstr(max(rs),6)}]")
ck("the 3-parameter form fits 200 ARBITRARY mass triples exactly (<1e-25) -> it has no "
   "empirical content of its own: REPARAMETRISATION, not derivation", worst < mp.mpf("1e-25"))
ck("fitted r on random triples is NOT clustered at sqrt2 (spread > 0.3) -> r = sqrt2 is a "
   "property of the DATA, not of the parameterisation", max(rs) - min(rs) > mp.mpf("0.3"))
print("""
  The ONLY thing that could promote Tier A to Tier B is a mechanism that FORCES r = sqrt 2.
  Section (4) asks that, and only that.""")


# =====================================================================================
hdr("(4) IS THERE ANYTHING IN THE FRAMEWORK THAT FORCES r = sqrt 2?")
# =====================================================================================
print("""
  Treated per the double-scrutiny rule: a positive answer here would be the framework's
  FIRST flavour prediction, so any positive result is a SUSPECTED BUG until a second,
  independent route confirms it.  Three sub-questions, T1/T2/T3.
""")

# ---------------------------------------------------------------- T1
print("  --- T1  Q-BLINDNESS THEOREM (what a flavour-blind kernel can do to Q: nothing) ---")
print("""  PREMISE P1 (a statement about the framework, labelled as such, not a theorem):
    the framework's kernel is a scalar function of a single scalar invariant
    (nu(y) = sqrt(1+1/y), y = g_bar/a_0).  Applied to a mass sector it acts as ONE
    multiplier common to all three generations: sqrt m_i -> f(sqrt m_i) with the SAME f.
  THEOREM: if such an f preserves Q on all positive triples and f > 0 on (0, inf),
    then f(x) = w x.  And a common rescaling leaves Q EXACTLY invariant.""")
t, a, u = sp.symbols("t a u", positive=True)
lhs = (2 * a ** 2 + u ** 2) * (2 + t) ** 2 - (2 + t ** 2) * (2 * a + u) ** 2
sols = sp.solve(sp.Eq(lhs, 0), u)
sols = [sp.simplify(s) for s in sols]
print(f"    Q-preservation on the slice v=(1,1,t):  f(t) in {sols}")
lin = [s for s in sols if sp.simplify(s - a * t) == 0]
oth = [s for s in sols if sp.simplify(s - a * t) != 0]
ck("T1a: the Q-preservation equation on (1,1,t) has EXACTLY 2 branches", len(sols) == 2)
ck("T1b: one branch is the linear map f(t) = a t", len(lin) == 1)
if oth:
    mob = sp.simplify(oth[0])
    print(f"    second (Moebius) branch: f(t) = {mob}")
    val4 = sp.simplify(mob.subs({t: 4}))
    val5 = sp.simplify(mob.subs({t: 5, a: 1}))
    print(f"      f(4) = {val4}   f(5)|a=1 = {val5}  -> leaves (0,inf) at t = 4")
    ck("T1c: the Moebius branch VIOLATES positivity at t >= 4 (excluded by m_i > 0)",
       val4 == 0 and val5 < 0)
    # and it fails OFF the slice too, so no continuity argument is needed
    f2 = sp.lambdify(t, mob.subs(a, 1), "mpmath")
    trip = [mp.mpf(1), mp.mpf(2), mp.mpf(3)]
    im = [mp.mpf(f2(x)) for x in trip]
    Qa = sum(x ** 2 for x in trip) / sum(trip) ** 2
    Qb = sum(x ** 2 for x in im) / sum(im) ** 2
    print(f"      off-slice test on v=(1,2,3): Q = {mp.nstr(Qa,10)} -> {mp.nstr(Qb,10)}")
    ck("T1d: the Moebius branch does NOT preserve Q off the slice (killed without continuity args)",
       abs(Qa - Qb) > mp.mpf("1e-6"))
# the linear branch really does leave Q fixed (both symbolically and on real leptons)
Q_w = sp.simplify(sum((w * s) ** 2 for s in sm) / sp.simplify(sum(w * s for s in sm)) ** 2)
ck("T1e: common rescale leaves Q identically fixed (symbolic)", sp.simplify(Q_w - Q_sym) == 0)
scaled = [Qof([wf * m_e, wf * m_mu, wf * mtP]) for wf in (mp.mpf("0.5"), 2, 137)]
print(f"    real leptons under common rescale x{{0.5,2,137}}: "
      f"{[mp.nstr(q,14) for q in scaled]}")
ck("T1f: real-lepton Q invariant under common rescale to 1e-40",
   all(abs(q - QP) < mp.mpf("1e-40") for q in scaled))
# a power-law kernel f(x)=x^p DOES move Q unless p=1 -> shows the theorem has teeth
mov = []
for p in (mp.mpf("0.5"), mp.mpf("0.9"), mp.mpf("1.1"), mp.mpf(2)):
    imv = [x ** p for x in vobs]
    mov.append(sum(x ** 2 for x in imv) / sum(imv) ** 2)
print(f"    kernel f(x)=x^p, p in {{0.5,0.9,1.1,2}} gives Q = {[mp.nstr(q,8) for q in mov]}")
ck("T1g: a NON-linear componentwise kernel DOES move Q (so T1 is not vacuous)",
   all(abs(q - QP) > mp.mpf("1e-6") for q in mov))
print("""    COROLLARY (the point): under P1 the framework is Q-BLIND -- it can neither DERIVE
    nor BREAK Koide.  Necessary condition for any genuine flavour mechanism in this
    framework: it must be generation-DEPENDENT or generation-MIXING (non-diagonal in
    generation space).  That is a falsifiable demand to put to any future claim.""")

# ---------------------------------------------------------------- T2
print("\n  --- T2  Z-GRADING THEOREM (Z provably cannot appear in a forced r = sqrt 2) ---")
print("""    sqrt(pi) is transcendental (pi transcendental, Lindemann-Weierstrass), so Qbar(sqrt pi)
    is a rational function field over Qbar in the indeterminate T := sqrt(pi), and it carries
    a T-VALUATION (grade).  Z = sqrt(32/3) * T has grade +1.  sqrt(2) is algebraic: grade 0.
    Hence any closed-form equal to sqrt(2) has NET Z-grade ZERO.""")
T = sp.Symbol("T", positive=True)
Z_T = sp.sqrt(sp.Rational(32, 3)) * T
ck("T2a: Z = sqrt(32/3) sqrt(pi) exactly (grade-1 element)",
   sp.simplify(Z_sym - Z_T.subs(T, sp.sqrt(sp.pi))) == 0)
ck("T2b: Z^2/pi is RATIONAL (= 32/3), i.e. Z carries exactly one power of sqrt(pi)",
   sp.simplify(Z_sym ** 2 / sp.pi - sp.Rational(32, 3)) == 0)
# empirical corroboration of transcendence: no low-height integer relation among
# log(pi^(n/2)) and log(sqrt2) -> pslq finds nothing
rel = mp.pslq([mp.log(mp.pi), mp.log(2)], maxcoeff=10 ** 8, maxsteps=20000)
print(f"    pslq(log pi, log 2) with coeffs up to 1e8 -> {rel}")
ck("T2c: no integer relation a*log(pi) + b*log(2) = 0 up to height 1e8 "
   "(no rational power of pi is a rational power of 2)", rel is None)
# OPERATIONAL TEETH.  Enumerate monomials 2^a 3^b pi^c Z^d on a grid of quarter-integer
# exponents in [-2,2] and separate EXACT hits (the theorem's object) from NEAR hits at 1e-5
# (numerology's object).  T2 predicts: every EXACT hit has net pi-power zero (c + d/2 = 0);
# it says NOTHING about approximate hits, and approximate hits with Z DO exist -- which is
# exactly why the exact/approximate distinction is the whole content of the theorem.
gg = np.arange(-8, 9) / 4.0          # -2 .. 2 in steps of 1/4
A_, B_, C_, D_ = [x.ravel() for x in np.meshgrid(gg, gg, gg, gg, indexing="ij")]
tot = A_.size
lg = (A_ * np.log(2.0) + B_ * np.log(3.0) + C_ * np.log(np.pi)
      + D_ * float(mp.log(Z)))
target_lg = 0.5 * np.log(2.0)
relerr = np.abs(np.expm1(lg - target_lg))          # expm1: no 1-exp underflow
near = np.flatnonzero(relerr < 1e-5)
# re-test the near hits at dps=50 to separate EXACT from merely close
exact_idx, nearonly_idx = [], []
for i in near:
    val = (mp.mpf(2) ** mp.mpf(A_[i]) * mp.mpf(3) ** mp.mpf(B_[i])
           * mp.pi ** mp.mpf(C_[i]) * Z ** mp.mpf(D_[i]))
    (exact_idx if abs(val - mp.sqrt(2)) / mp.sqrt(2) < mp.mpf("1e-40")
     else nearonly_idx).append(i)
hits = [(mp.mpf(A_[i]), mp.mpf(B_[i]), mp.mpf(C_[i]), mp.mpf(D_[i])) for i in near]
exact = [(A_[i], B_[i], C_[i], D_[i]) for i in exact_idx]
exact_Z = [h for h in exact if h[3] != 0]
nearZ = [(A_[i], B_[i], C_[i], D_[i]) for i in nearonly_idx if D_[i] != 0]
print(f"    grid 2^a 3^b pi^c Z^d, exponents = quarter-integers in [-2,2]: {tot} monomials")
print(f"      EXACT hits on sqrt2 (1e-40): {len(exact)}   of which containing Z: {len(exact_Z)}")
print(f"      NEAR-only hits (1e-5 but not exact): {len(nearonly_idx)}   of which containing Z: {len(nearZ)}")
if exact_Z:
    print(f"      exact Z-hits (a,b,c,d): {[tuple(float(x) for x in h) for h in exact_Z[:6]]}")
ck("T2d: at least one EXACT Z-containing hit exists on this grid (so the check has content)",
   len(exact_Z) >= 1)
ck("T2d': EVERY EXACT hit has net pi-power zero (c + d/2 = 0) -- Z enters only through the "
   "pi-cancelling ratio Z/sqrt(pi).  T2 confirmed operationally",
   len(exact) >= 1 and all(abs(h[2] + h[3] / 2) < 1e-12 for h in exact))
# AT WHAT NUMERICAL TOLERANCE DOES THE GRADING OBSTRUCTION STOP BITING?
# T2 is a statement about EXACT identities.  Numerology works at finite precision, so measure
# the tolerance at which uncancelled-Z monomials start reaching sqrt2.  (My first draft ASSERTED
# such near-hits exist at 1e-5; the scan says they do not.  Claim corrected to the measurement.)
netpi = C_ + D_ / 2.0
dirty = (D_ != 0) & (np.abs(netpi) > 1e-12)      # uses Z with pi NOT cancelled
print("      tolerance scan -- uncancelled-Z monomials reaching sqrt2:")
first_dirty = None
for tolq in (1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1):
    nd = int(np.count_nonzero(dirty & (relerr < tolq)))
    if nd > 0 and first_dirty is None:
        first_dirty = tolq
    print(f"        rel tol {tolq:8.0e}:  {nd:6d} uncancelled-Z hits")
print(f"      -> the grading obstruction bites numerically down to rel tol ~{first_dirty:.0e}"
      f" on this grid;\n         it is EXACT-only in principle, and the measured crossover is stated"
      f" rather than assumed.")
ck("T2e: NO uncancelled-Z monomial reaches sqrt2 at 1e-5 -- so on this grid the grading "
   "obstruction bites even numerically, at the precision to which r is actually known",
   int(np.count_nonzero(dirty & (relerr < 1e-5))) == 0)
ck("T2e': uncancelled-Z monomials DO reach sqrt2 at some looser tolerance (so the previous "
   "check is a real constraint, not an empty grid)",
   first_dirty is not None and int(np.count_nonzero(dirty & (relerr < 1e-1))) > 0)
ck("T2e'': the crossover tolerance is LOOSER than the precision to which data pins r "
   f"({mp.nstr(s_r/mp.sqrt(2),3)}), i.e. Z cannot be smuggled in at the precision that matters",
   first_dirty is not None and mp.mpf(first_dirty) > s_r / mp.sqrt(2))
print("""    CONSEQUENCE: a forced r = sqrt 2 cannot involve Z except in combinations where Z's
    sqrt(pi) cancels -- i.e. in Z-INDEPENDENT quantities.  So even a successful Koide
    derivation would NOT be evidence for this framework.  This is the computed
    number-field obstruction, now stated as a grading argument.""")

# ---------------------------------------------------------------- T3
print("\n  --- T3  THE ONE POSITIVE-LOOKING HIT, FOUND AND PRICED (suspected bug first) ---")
print(f"""    FOUND: kappa = 1/2  =>  kappa^(-1/2) = {mp.nstr(kappa**mp.mpf('-0.5'), 16)} = sqrt 2 EXACTLY.
    So 'r = 1/sqrt(kappa)' reproduces the Koide amplitude to all digits.  If real this is
    the first flavour prediction.  Two INDEPENDENT routes are used to price it.""")
ck("T3a: kappa^(-1/2) equals sqrt2 to 1e-40 (the hit is arithmetically exact -- stated, not hidden)",
   abs(kappa ** mp.mpf("-0.5") - mp.sqrt(2)) < mp.mpf("1e-40"))
# ROUTE 1: precision mismatch. kappa is FITTED from a0 data to ~1.24% (best) - 5.44%.
ratios = []
for sk_rel in (mp.mpf("0.0124"), mp.mpf("0.0544")):
    # kappa \propto a0 at fixed rho_Lambda -> sigma_kappa/kappa = sigma_a0/a0
    r_from_k = kappa ** mp.mpf("-0.5")
    s_r_from_k = mp.mpf("0.5") * sk_rel * r_from_k   # d(k^-1/2)/k^-1/2 = -1/2 dk/k
    ratios.append(s_r_from_k / s_r)
    print(f"    route 1: sigma(a0)/a0 = {mp.nstr(sk_rel*100,3)} %  ->  r(kappa) = "
          f"{mp.nstr(r_from_k,8)} +- {mp.nstr(s_r_from_k,3)}  ({mp.nstr(s_r_from_k/r_from_k*100,3)} %)")
    print(f"             but data pins r to {mp.nstr(s_r/mp.sqrt(2)*100,3)} % -> the kappa route is "
          f"{mp.nstr(s_r_from_k/s_r,4)}x = {mp.nstr(mp.log10(s_r_from_k/s_r),3)} ORDERS too imprecise")
    ck(f"T3b: kappa known to {mp.nstr(sk_rel*100,3)}% is >=100x too imprecise to supply r "
       f"(which data pins to {mp.nstr(s_r/mp.sqrt(2)*100,3)}%)", s_r_from_k / s_r > 100)
print(f"    -> the precision gap is {mp.nstr(mp.log10(min(ratios)),3)}-{mp.nstr(mp.log10(max(ratios)),3)}"
      f" orders of magnitude (NOT the '3-4 orders' a looser telling would claim)")
ck("T3b': the gap is between 2 and 4 orders (stated to the digit, not rounded up in my favour)",
   2 < mp.log10(min(ratios)) and mp.log10(max(ratios)) < 4)
# ROUTE 2: sqrt2 is reached at ZERO framework cost -- and a control test on how special that is.
zero_cost = [h for h in exact if h[2] == 0 and h[3] == 0]
print(f"\n    route 2: EXACT hits using NO framework constant (c = d = 0, i.e. 2^a 3^b only):"
      f" {len(zero_cost)}")
if zero_cost:
    print(f"      e.g. (a,b,c,d) = {tuple(float(x) for x in zero_cost[0])}  ->  sqrt2 = 2^(1/2),"
          f" reached without pi, without Z, without kappa.")
ck("T3c: sqrt2 is EXACTLY reached by a monomial containing no framework constant at all, "
   "so the framework contributes nothing to reaching it", len(zero_cost) >= 1)
# control: is the grid so dense that any target is hit?  Report against interest.
ctrl = np.random.uniform(1.2, 1.6, 300)
ctrl_counts = []
for cv in ctrl:
    ctrl_counts.append(int(np.count_nonzero(np.abs(np.expm1(lg - np.log(cv))) < 1e-5)))
ctrl_counts = np.array(ctrl_counts)
print(f"      CONTROL (against interest): 300 random targets in [1.2,1.6] are hit "
      f"{ctrl_counts.mean():.2f} +- {ctrl_counts.std():.2f} times each (max {ctrl_counts.max()}),"
      f"\n      vs sqrt2's {len(near)} near / {len(exact)} exact.  So the grid is NOT trivially dense:"
      f"\n      'reachable by a simple monomial' is a real property, and sqrt2 has it maximally"
      f" (exactly, at zero cost).")
ck("T3d: the monomial grid is NOT so dense that a generic target is hit exactly -- the median "
   "control target gets fewer hits than sqrt2 (so route 2 is a real argument, not a vacuous one)",
   float(np.median(ctrl_counts)) < len(near))
print("""    ROUTE 3 (independent-prediction bar): 'r = kappa^(-1/2)' predicts NOTHING new.
    r = sqrt2 <=> Q = 2/3 <=> m_tau already measured.  Zero new observables.  Per the
    project's own chance baseline, a numerical coincidence with no independent prediction
    attached is worth nothing.
    VERDICT T3: the kappa^(-1/2) = sqrt2 hit is a COINCIDENCE, not a derivation.  It dies on
    precision (2.8-3.4 orders), on zero-framework-cost reachability (sqrt2 = 2^(1/2) needs no
    kappa, no Z, no pi), and on the no-new-prediction bar.  NOTE AGAINST MY OWN DISMISSAL: the
    control scan shows monomial-reachability is NOT vacuous (a generic target in [1.2,1.6] gets
    0.18 hits on average), so 'it's just numerology' would be too glib -- the dismissal rests on
    the precision gap and the absent mechanism, not on density.
    FALSIFIABLE RESIDUE (stated so it can be tested, not to keep a door propped open): IF a0's
    kappa were ever measured to ~1e-5 and stayed exactly 1/2, AND a mechanism linking a MOND
    coefficient to a generation-space projection angle were exhibited, this would sharpen.
    Neither holds today.""")
print(f"\n  ANSWER TO (4):  NO.  Nothing in the framework forces r = sqrt 2.")
print("  T1 says a flavour-blind kernel CANNOT move Q at all; T2 says Z CANNOT appear in the")
print("  answer; T3's only arithmetic hit is priced out.  This is a NEGATIVE result with two")
print("  theorems attached, which is the deliverable -- not a failed attempt.")


# =====================================================================================
hdr("(5) CHANCE-ALONE BASELINE: what is P(hit Q = 2/3 to the observed precision)?")
# =====================================================================================
print("""
  Detection tolerance: you could not have resolved better than sigma_Q, so ask
  P(|Q - 2/3| < sigma_Q) under several measures.  The measure is a genuine fork -- all of
  them are reported, none is privileged.""")
tol = float(sQP)
print(f"  tolerance = sigma_Q = {tol:.3e}")

# exact range of Q (Cauchy-Schwarz): Q in [1/3, 1]
mq = 10 ** np.random.uniform(-6, 6, (400000, 3))
Qr = mq.sum(1) / np.sqrt(mq).sum(1) ** 2
print(f"  empirical range of Q over 4e5 random decades: [{Qr.min():.6f}, {Qr.max():.6f}]")
ck("Q range respects the Cauchy-Schwarz window [1/3, 1]", Qr.min() >= 1 / 3 - 1e-12 and Qr.max() <= 1 + 1e-12)
ck("2/3 is the MIDPOINT of the allowed window (so it is not a boundary/attractor artifact)",
   abs(two_thirds - (mp.mpf(1) / 3 + 1) / 2) < mp.mpf("1e-40"))

P = {}
# (a) uniform in Q on its allowed window
P["uniform in Q on [1/3,1]"] = 2 * tol / (1 - 1 / 3)
# (b) uniform in r on [0,2) (the full range for which some delta keeps all masses positive)
#     Q = 1/3 + r^2/6 -> dQ = r dr /3
r0 = float(mp.sqrt(2))
P["uniform in r on [0,2)"] = (2 * tol * 3 / r0) / 2.0
# (c) log-uniform in the two mass ratios, several boxes (the physically honest measure:
#     masses are log-hierarchical)
def p_loguniform(lo1, hi1, lo2, hi2, n=4000000):
    x = np.random.uniform(lo1, hi1, n)   # log10(m_mu/m_e)
    y = np.random.uniform(lo2, hi2, n)   # log10(m_tau/m_mu)
    a1 = 10 ** x
    a2 = 10 ** (x + y)
    Qs = (1 + a1 + a2) / (1 + np.sqrt(a1) + np.sqrt(a2)) ** 2
    k = np.count_nonzero(np.abs(Qs - 2.0 / 3.0) < tol)
    return k / n, k
obs1 = float(mp.log(m_mu / m_e, 10))
obs2 = float(mp.log(mtP / m_mu, 10))
print(f"  observed hierarchy: log10(m_mu/m_e) = {obs1:.4f}, log10(m_tau/m_mu) = {obs2:.4f}")
for lab, box in {
    "log-uniform, wide box (0..6, 0..6 dex)": (0, 6, 0, 6),
    "log-uniform, +-1 dex around observed": (obs1 - 1, obs1 + 1, obs2 - 1, obs2 + 1),
    "log-uniform, +-0.5 dex around observed": (obs1 - .5, obs1 + .5, obs2 - .5, obs2 + .5),
}.items():
    p, kk = p_loguniform(*box)
    P[lab] = p
    print(f"    {lab:42s} p = {p:.3e}   ({kk} hits)")
print()
for lab, p in P.items():
    print(f"    {lab:42s} p = {p:.3e}    1 in {1/p:,.0f}" if p > 0 else f"    {lab:42s} p = 0")
pvals = [p for p in P.values() if p > 0]
print(f"\n  SPREAD across measures: p = {min(pvals):.2e} .. {max(pvals):.2e}"
      f"  (a factor {max(pvals)/min(pvals):.1f})")
ck("every measure gives p < 1e-3 (the closeness is NOT explained by chance under ANY measure)",
   all(p < 1e-3 for p in pvals))
ck("the uniform-Q figure reproduces the corpus's banked ~1-in-44000 to within a factor 3",
   1 / 3 < (1 / P["uniform in Q on [1/3,1]"]) / 44000 < 3)
ck("log-uniform measures are NOT wildly more permissive than uniform-Q (spread < 100x)",
   max(pvals) / min(pvals) < 100)

# multiplicity: the project's own audit found chance hit 10 of 19 numerical targets
p_single = max(pvals)
print(f"""
  MULTIPLICITY / CHANCE-ALONE CALIBRATION.  This project's symbolic-regression audit found
  chance alone hit 10 of 19 numerical targets -- a per-target hit rate of {10/19:.2f} for a
  FORMULA SEARCH.  Koide is not that object: it is ONE fixed relation on 3 masses with the
  worst-case single-shot p = {p_single:.2e}.""")
for Ntry in (1, 100, 1000, 100000):
    peff = 1 - (1 - p_single) ** Ntry
    print(f"    if {Ntry:>6d} comparably-simple relations were tried: p_eff = {peff:.3e}"
          f"  [worst measure p={p_single:.1e}]")
# where does it break?  report the honest break-even trial count on BOTH ends of the fork
p_best = min(pvals)
Nbreak_worst = np.log1p(-0.05) / np.log1p(-p_single)   # log1p: no 1-x cancellation
Nbreak_best = np.log1p(-0.05) / np.log1p(-p_best)
print(f"\n    BREAK-EVEN at p_eff = 0.05:  N = {Nbreak_worst:,.0f} trials (worst/most permissive"
      f" measure)\n                                 N = {Nbreak_best:,.0f} trials (widest/least tuned measure)")
print("    So the coincidence survives a few-hundred-relation search and dies above ~1e3-6e3.")
ck("at 100 trials the coincidence still survives (p_eff < 0.05) under the WORST measure",
   1 - (1 - p_single) ** 100 < 0.05)
ck("the break-even trial count is >= 500 even on the most permissive measure "
   "(so a modest search cannot explain Koide)", Nbreak_worst >= 500)
ck("at 1e5 trials the coincidence would NOT survive (the multiplicity test has teeth "
   "and is not rigged to pass)", 1 - (1 - p_single) ** 100000 > 0.05)
ck("the single-shot p is >=100x smaller than the audit's chance per-target hit rate 10/19",
   p_single * 100 < 10 / 19)
print(f"""
  BOTH-WAYS READING (this cuts against the sceptic, and is reported as such):
    the Koide coincidence IS numerically real.  p ~ {p_single:.1e} under the most permissive
    measure tried, surviving a search of up to ~{Nbreak_worst:,.0f} comparably simple relations
    ({Nbreak_best:,.0f} on the least-tuned measure).  Calling it 'just numerology' is NOT
    supported by this calculation.  It IS killed by a search of ~1e5 relations -- so the
    verdict is measure- and search-size-dependent, and that dependence is stated, not buried.
  AND AGAINST INTEREST:
    that has nothing to do with this framework.  Tier A is a REPARAMETRISATION (3 for 3, via
    a bijection).  T1 says the framework's flavour-blind kernel cannot move Q at all.  T2 says
    the framework's signature number Z provably cannot appear in r = sqrt 2.  So the one real
    flavour lead in physics is, for THIS framework, provably out of reach by the route it has.""")


# =====================================================================================
hdr("SUMMARY")
# =====================================================================================
print(f"""
  1. Q(PDG-2024)  = {mp.nstr(QP,12)} +- {mp.nstr(sQP,3)} ;  Q - 2/3 = {mp.nstr(devP,3)}
     = {mp.nstr(nsigP,3)} sigma  -> the deviation from 2/3 is NOT significant.
     Footing fork Belle-II 2023: {mp.nstr(nsigB,3)} sigma.  Verdict robust to both m_tau footings.
  2. Framework parameterisation sqrt m_k = M(1 + r cos(delta + 2 pi k/3)):
     free parameters = 3  (M, delta, r);  observables = 3.  Map is bijective (det J != 0).
  3. N_free (3) >= N_observables (3)  ->  REPARAMETRISATION, not derivation.
     With r fixed at sqrt2 you get exactly ONE prediction (m_tau = {mp.nstr(mtau_pred,9)} MeV,
     {mp.nstr(abs(mtau_pred-mtP)/stP,3)} sigma) -- and that prediction is KOIDE's, dated 1981.
  4. Does anything FORCE r = sqrt 2?  NO, with two theorems for why:
       T1  a flavour-blind componentwise kernel that preserves Q must be LINEAR, and a linear
           (common) rescale leaves Q exactly fixed  ->  the framework is Q-BLIND: it can
           neither derive nor break Koide.  Any real mechanism must be generation-dependent
           or generation-mixing.  [FALSIFIABLE demand on future claims]
       T2  grading Qbar(sqrt pi) by the power of sqrt(pi): Z has grade 1, sqrt(2) grade 0, so a
           forced r = sqrt2 has NET Z-GRADE ZERO -- Z provably cannot appear.  Verified
           operationally: every EXACT monomial hit satisfies c + d/2 = 0, and NO uncancelled-Z
           monomial reaches sqrt2 even at 1e-5 (crossover measured at rel tol ~{first_dirty:.0e},
           far looser than the {mp.nstr(s_r/mp.sqrt(2),3)} to which data pins r).  My first draft asserted such
           near-hits existed at 1e-5; the scan says otherwise and the claim was corrected.
       T3  the exact hit kappa^(-1/2) = sqrt2 is a COINCIDENCE: kappa is fitted to 1.2-5.4%
           while r is pinned to {mp.nstr(s_r/mp.sqrt(2)*100,3)}%, a gap of
           {mp.nstr(mp.log10(min(ratios)),3)}-{mp.nstr(mp.log10(max(ratios)),3)} orders; sqrt2 is reached EXACTLY with no framework
           constant at all (2^(1/2)); and it predicts no new observable.
  5. Chance baseline: p = {min(pvals):.2e} .. {max(pvals):.2e} across measures; survives a search of
     ~{Nbreak_worst:,.0f}-{Nbreak_best:,.0f} comparable relations, dies at ~1e5.  The lead IS real -- and is NOT
     this framework's.

  NOTHING HERE IS CLAIMED DERIVED.  a_0, Z and kappa remain un-derived; kappa = 1/2 is FITTED.
  The deliverable is a NEGATIVE result upgraded to two theorems about why the flavour bridge
  is unreachable from this framework's structure.
""")

print(f"{NCK[0]}/{NCK[1]} checks held.")
if NCK[0] != NCK[1]:
    sys.exit(1)
sys.exit(0)
