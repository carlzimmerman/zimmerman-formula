#!/usr/bin/env python3
r"""mi_psi_search_r2Z_2026.py -- does ADMISSIBILITY bound the crossover ratio r? Solve the VARIATIONAL problem.

THE QUESTION. mi_crossover_master_formula_2026.py (14/14) reduced the whole dS-Unruh inertia class
I = f(T) - f(T_GH), T = sqrt(a^2+H^2)/2pi, to ONE number: q = a_0/(c H_Lambda) = 2/r, r = f'(T_GH)/c1p.
mi_r_admissibility_bound_2026.py (6/6) then asked whether admissibility bounds r, scanned SEVEN psi shapes x 220
scales, found max admissible r = 9.016763, and concluded (its checks B2 and C1) that r = 2Z = 11.577620
(kappa = 1/2) and r = 4 pi = 12.566371 (Milgrom 2020) are BOTH inadmissible -- while flagging, in its own words,
"SEVEN SHAPES IS NOT A PROOF ... A single admissible shape reaching 2Z overturns this."

THIS SCRIPT OVERTURNS IT, and then says what that is and is not worth.

  Set s = T - T_GH, x = s/T_GH, F(s) = f(T_GH+s) - f(T_GH), F'(s) = c1p[1 + lam psi(s)], lam = r - 1,
  psi(0) = 1, psi non-increasing, psi(inf) = 0, Int psi < inf, and Phi(x) = Int_0^x psi. With c1p = 1 (q is
  invariant under f -> alpha f + b) the two admissibility conditions of the previous script become, EXACTLY,
      (A1)  mu <= 1        <=>   lam Phi(inf) <= 1
      (A2)  mu monotone    <=>   lam J(x) <= 1 for all x > 0,   J(x) = (1 + 1/x) Phi(x) - (x+2) psi(x).
  So max admissible r = 1 + 1/ inf_psi sup_x J -- a clean minimax over a function space, not a menu.

  RESULT, in the direction the mathematics went and NOT the direction wanted:
   * (A1) is REDUNDANT: (A2) at x -> inf implies it (Lemma 2). Only (A2) ever binds.
   * J(x) >= -psi(x) >= -1 for EVERY admissible psi (Lemma 1), so every r in [0,1] is admissible for EVERY
     shape: a_0 >= 2 c H_Lambda is completely unconstrained.
   * The (A2) equality locus is F proportional to w = sqrt(s(s+2T_GH)), on which mu is EXACTLY CONSTANT. Splicing
     a compact segment of it onto a plateau psi = 1 gives, for EVERY r > 1, an admissible psi with a strict
     margin (Theorem, section E). sup r = +infinity. An LP over a discretised psi (section D) independently
     reaches r = 2.1e4 and grows as x_min^(-1/2) with no plateau.
   * The bound survives NOTHING: not smoothness, not complete monotonicity. Section F exhibits a closed-form,
     real-analytic, COMPLETELY MONOTONE psi = (1+s/delta)^(-1/2) (1+s/Delta)^(-1) admissible up to r = 20.2,
     i.e. r = 2Z with a 45% margin in lam, and its nu(y) is a sane MOND kernel on y in [1e-4, 1e4].
   * What admissibility actually says (section H): for the sharp family, r <= 1 + 2/(x1 + sqrt(x1(x1+2))) where
     x1 is the plateau length -- i.e. a_0 cannot be much BELOW the acceleration at which the kernel's shape
     starts to move. A statement about the SHAPE SCALE, not about the coefficient. Toothless on a_0.

  SO: the previous script's B2/C1 exclusion of r = 2Z is WITHDRAWN, and so is its exclusion of r = 4 pi. That
  removes a no-go against kappa = 1/2 -- and in the same stroke it removes the ONLY route by which this class
  could ever have DERIVED any coefficient, since the admissible set of r is now all of [0, inf). kappa = 1/2 is
  FITTED, NOT DERIVED, and this script leaves it more thoroughly fitted than before, not less.
  Also recorded because it cuts against the framework: the single-scale menu bound is exactly r = 9 (section H,
  closed form), and 9 < 2Z < 4pi, so BOTH live coefficients need a psi with a second scale tuned to a_0, while
  Milgrom 1999's r = 1 and his eq.10 r = 2 are admissible with every single-scale shape and no tuning at all.

CREDIT. nu = sqrt(1+1/y) and the dS-Unruh temperature balance are Milgrom 1999 PLA 253:273 eqs 6-9, who fixes
a_0_hat = 2 c H_Lambda (r = 1); his eqs 10-11 give a SECOND coefficient (r = 2); Milgrom 2008 arXiv:0801.3133
sec 7.3.1 says the coefficient mismatch "isn't necessarily meaningful ... would just point to a different
effective mu(x)" -- the r-freedom is HIS observation. Temperature sqrt(a^2+Lambda/3)/2pi is Narnhofer, Peter and
Thirring 1996 IJMPB 10:1507. Five-acceleration reading: Deser and Levin 1997 CQG 14:L163.
a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994 Ann.Phys. 229:384. Exponential kernel: McGaugh 2008 ApJ 683:137 11a.

Exit 0 = every check held. Every check below has an input that makes it print FAIL; section C carries an
explicit NEGATIVE CONTROL (a non-monotone psi) that violates Lemma 1, to show the lemma checks have teeth.
"""
from __future__ import annotations
import math, sys
import numpy as np
import sympy as sp
from mpmath import mp, mpf, sqrt as msqrt
from scipy.optimize import linprog
from scipy.integrate import quad
from scipy.special import erf

ok: list[tuple[bool, str]] = []
def check(c, m):
    c = bool(c); ok.append((c, m)); print(f"  [{'OK' if c else 'FAIL'}] {m}"); return c
def banner(t):
    print("\n" + "=" * 108); print(f"  {t}"); print("=" * 108)

Z = 2*math.sqrt(8*math.pi/3); TWOZ = 2*Z; FOURPI = 4*math.pi
TG = 1.0/(2*math.pi)                  # T_GH in units c = H_Lambda = 1
CHL = 5.4194e-10                      # c H_Lambda, m/s^2
MENU_MAX_COMMITTED = 9.016763         # the committed 7-shape number being audited
mp.dps = 50

# ---------------------------------------------------------------------------------------------------------
banner("A  THE REDUCTION -- (A1) and (A2) in the scale-free variable x = s/T_GH")

x, lamS, cS, CS, A_, B_ = sp.symbols("x lambda c C Phi_x psi_x", positive=True)
# margin of (A2):  F'(s) s(s+2T) - F(s)(s+T),  in units T_GH^2, with F/T = x + lam Phi, F' = 1 + lam psi
marg_raw = (1 + lamS*B_)*x*(x + 2) - (x + lamS*A_)*(x + 1)
J_sym    = (1 + 1/x)*A_ - (x + 2)*B_
print("  F'(s) s(s+2T_GH) - F(s)(s+T_GH)  =  T_GH^2 * x * (1 - lam J(x)),   J = (1+1/x)Phi - (x+2)psi")
check(sp.simplify(marg_raw - x*(1 - lamS*J_sym)) == 0,
      "A1 the (A2) margin factorises EXACTLY as x(1 - lam J(x)) with J = (1+1/x)Phi - (x+2)psi, so monotonicity "
      "of mu is the single linear-in-psi condition lam J(x) <= 1 for all x > 0. Linear in psi is what makes the "
      "variational problem an LP in section D rather than a shape scan")

mu_sym = (x + lamS*A_)/sp.sqrt(x*(x + 2))
dmu = sp.simplify(sp.diff(mu_sym.subs(A_, sp.Function("P")(x)), x).subs(
    {sp.Derivative(sp.Function("P")(x), x): B_, sp.Function("P")(x): A_}))
check(sp.simplify(dmu - x*(1 - lamS*J_sym)/(x*(x + 2))**sp.Rational(3, 2)) == 0,
      "A2 and d mu/dx = x(1 - lam J)/(x(x+2))^(3/2), so the SIGN of the margin is the sign of mu', exactly. The "
      "two conditions are therefore mu' >= 0 and mu(inf) = 1 from above, nothing else")

# ---------------------------------------------------------------------------------------------------------
banner("B  CONTROL -- r = 1 (Milgrom 1999, f = T) must pass, with the known exact margin s T_GH")

xs = np.logspace(-12, 12, 400001)
marg1 = xs*(1 - 0.0)                       # lam = 0
mu1 = xs/np.sqrt(xs*(xs + 2))
print(f"  r = 1:  min margin/x = {marg1.min()/xs.min():.6f} (exact value 1, i.e. margin = s T_GH)   "
      f"max mu = {mu1.max():.15f}")
check(abs(marg1.min()/xs.min() - 1.0) < 1e-12 and mu1.max() <= 1.0,
      f"B1 r = 1 passes with margin x T_GH^2 = s T_GH identically and max mu = {mu1.max():.12f} <= 1, "
      f"reproducing check A1 of mi_r_admissibility_bound_2026.py. The reduction is anchored on the one case "
      f"whose answer is known independently")

# ---------------------------------------------------------------------------------------------------------
banner("C  TWO LEMMAS -- and a NEGATIVE CONTROL, so the lemma checks can fail")

print("""  LEMMA 1.  psi non-increasing => Phi(x) >= x psi(x) => (1+1/x)Phi >= (x+1)psi, hence
              -J = (x+2)psi - (1+1/x)Phi <= psi(x) <= 1,  i.e.  J(x) >= -psi(x) >= -1.
            Consequence: for lam in [-1,0] (r in [0,1]) lam J = |lam|(-J) <= |lam| psi <= 1 for EVERY admissible
            psi. So every r in [0,1] is admissible with NO condition on the shape: a_0 >= 2 c H_Lambda is
            entirely unconstrained, and the admissible set of r contains [0,1] outright.
  LEMMA 2.  psi non-increasing and integrable => x psi(x) -> 0 (since (x/2)psi(x) <= Int_{x/2}^x psi -> 0), so
            J(x) -> Phi(inf) as x -> inf. Hence (A2) at large x IMPLIES (A1): lam Phi(inf) <= 1. (A1) is
            REDUNDANT and only (A2) can ever bind.""")

rng = np.random.default_rng(20260807)
xg = np.logspace(-8, 8, 20001)
worst_J, worst_lam1 = np.inf, -np.inf
for _ in range(1500):
    w = rng.dirichlet(np.full(len(xg) - 1, 0.06))          # random non-increasing psi: 1 -> 0
    ps = np.concatenate(([1.0], 1.0 - np.cumsum(w)))
    Ph = np.concatenate(([xg[0]*(1 + ps[0])/2],
                         xg[0]*(1 + ps[0])/2 + np.cumsum(0.5*(ps[1:] + ps[:-1])*np.diff(xg))))
    Jv = (1 + 1/xg)*Ph - (xg + 2)*ps
    worst_J = min(worst_J, (Jv + ps).min())                # Lemma 1: J + psi >= 0
    worst_lam1 = max(worst_lam1, (-Jv).max())              # lam = -1 feasibility: -J <= 1
print(f"  1500 random non-increasing psi:  min over all of (J + psi) = {worst_J:+.3e}   max over all of (-J) = "
      f"{worst_lam1:.9f}")
check(worst_J > -1e-9 and worst_lam1 <= 1.0 + 1e-9,
      f"C1 Lemma 1 verified on 1500 random non-increasing shapes: J + psi >= {worst_J:+.2e} (>= 0) and "
      f"max(-J) = {worst_lam1:.6f} <= 1, so lam = -1 (r = 0) is feasible for all of them. Every r in [0,1] is "
      f"admissible for every shape")

ps_bad = np.where(xg < 1.0, 1.0, np.where(xg < 3.0, 0.05, np.where(xg < 10.0, 0.9, 0.9*np.exp(-(xg - 10)))))
Ph_bad = np.concatenate(([xg[0]], xg[0] + np.cumsum(0.5*(ps_bad[1:] + ps_bad[:-1])*np.diff(xg))))
J_bad = (1 + 1/xg)*Ph_bad - (xg + 2)*ps_bad
print(f"  NEGATIVE CONTROL, a psi that DIPS then RISES (not admissible by hypothesis): min J = {J_bad.min():.6f}")
check(J_bad.min() < -1.0,
      f"C2 the negative control gives min J = {J_bad.min():.4f} < -1, violating Lemma 1. So C1 is not a check "
      f"that cannot fail: monotonicity of psi is exactly what the lemma uses, and dropping it breaks the bound")

exh_far = []                                                # filled in E/F, used for the Lemma-2 check

# ---------------------------------------------------------------------------------------------------------
banner("D  THE VARIATIONAL SOLVE -- minimise sup_x J over psi by LINEAR PROGRAMMING (not a menu)")

def lp_solve(xmin, xmax=1e3, N=400):
    """min c s.t. J_i <= c at every node, psi non-increasing, psi(0)=1, psi(x_max)=0. Phi by trapezoid."""
    xx = np.concatenate(([0.0], np.logspace(math.log10(xmin), math.log10(xmax), N)))
    n = len(xx) - 1
    dx = np.diff(xx)
    M = np.zeros((n, n)); b0 = np.zeros(n)
    prevM = np.zeros(n); prev = 0.0
    for i in range(n):
        curM = prevM.copy(); curb = prev
        if i == 0:
            curb += 0.5*dx[i]; curM[0] += 0.5*dx[i]
        else:
            curM[i-1] += 0.5*dx[i]; curM[i] += 0.5*dx[i]
        M[i, :] = curM; b0[i] = curb; prevM, prev = curM, curb
    xi = xx[1:]
    A = (1.0 + 1.0/xi)[:, None]*M
    A[np.arange(n), np.arange(n)] -= (xi + 2.0)
    Acon = np.ascontiguousarray(A)                 # contiguous copy: matmul on the hstacked VIEW raises
    A = np.hstack([A, -np.ones((n, 1))]); b = -(1.0 + 1.0/xi)*b0   # spurious FPE warnings in numpy
    Am = np.zeros((n, n + 1)); bm = np.zeros(n); Am[0, 0] = 1.0; bm[0] = 1.0
    for i in range(1, n):
        Am[i, i] = 1.0; Am[i, i-1] = -1.0
    obj = np.zeros(n + 1); obj[-1] = 1.0
    res = linprog(obj, A_ub=np.vstack([A, Am]), b_ub=np.concatenate([b, bm]),
                  bounds=[(0.0, 1.0)]*(n - 1) + [(0.0, 0.0)] + [(-2.0, 5.0)], method="highs")
    cst = res.x[-1]
    Jn = Acon @ np.ascontiguousarray(res.x[:-1]) - b     # J_i = A phi + (1+1/x)b0 ; b_ub = -(1+1/x)b0
    nact = int(np.sum(Jn > cst - 1e-6*max(abs(cst), 1e-12)))
    # if the optimum rides the (A2) equality locus, psi = C(x+1)/sqrt(x(x+2)) - c with C CONSTANT: measure it
    sup = res.x[:-1] > 1e-6
    Ci = (res.x[:-1][sup] + cst)*np.sqrt(xi[sup]*(xi[sup] + 2))/(xi[sup] + 1)
    return cst, 1.0 + 1.0/cst, nact, res.status, float(Ci.max()/Ci.min() - 1), int(sup.sum())

print(f"  {'x_min':>10}{'c* = sup J':>14}{'r_max (LP)':>14}{'x_min^(-1/2)':>14}{'#active/#nodes':>16}"
      f"{'arc-fit C spread':>18}")
print("  " + "-" * 88)
lp = {}; spread = {}
for xm in (1e-2, 1e-3, 1e-4, 1e-6, 1e-8):
    cst, rmx, nact, st, spr, nsup = lp_solve(xm)
    lp[xm] = rmx; spread[xm] = spr
    print(f"  {xm:>10.0e}{cst:>14.6e}{rmx:>14.4f}{math.sqrt(2/xm):>14.1f}{f'{nact}/400':>16}"
          f"{spr:>18.2e}   status={st}, support {nsup}")
check(lp[1e-8] > TWOZ and lp[1e-8] > FOURPI and lp[1e-2] > TWOZ,
      f"D1 *** the OPTIMISER reaches r_max = {lp[1e-8]:.1f} at x_min = 1e-8 and already r_max = {lp[1e-2]:.2f} at "
      f"x_min = 1e-2, both ABOVE 2Z = {TWOZ:.6f} and 4 pi = {FOURPI:.6f}. The committed 7-shape maximum "
      f"{MENU_MAX_COMMITTED:.6f} is a property of the MENU, not of admissibility. This check FAILS if the LP is "
      f"bounded near 9 ***")
grow = lp[1e-8]/lp[1e-4]
check(abs(grow/100.0 - 1.0) < 0.2 and lp[1e-8]/lp[1e-6] > 5,
      f"D2 and r_max grows like x_min^(-1/2): r_max(1e-8)/r_max(1e-4) = {grow:.1f} against the predicted 100 "
      f"(the resolution of the plateau is what limits the discretised problem, see section H). No plateau in r "
      f"anywhere -- a genuine bound would show one. This check FAILS if the growth stalls")
check(max(spread.values()) < 5e-3,
      f"D3 and the LP's own optimum IS the equality locus of section E, found independently: writing its psi as "
      f"C(x+1)/sqrt(x(x+2)) - c gives C constant to {max(spread.values()):.1e} relative across ~320 supported "
      f"nodes, with EVERY node's (A2) constraint active. The optimiser and the closed form agree on the answer "
      f"-- which is why the unboundedness is not a numerical accident. This check FAILS if the LP optimum has "
      f"any other shape")

# ---------------------------------------------------------------------------------------------------------
banner("E  THEOREM -- an EXPLICIT admissible psi for EVERY r > 1. sup r = +infinity")

print("""  The (A2) equality locus is the linear ODE  (1+1/x)Phi - (x+2)Phi' = c, whose solution is
      Phi(x) = C sqrt(x(x+2)) - c x,   psi(x) = Phi'(x) = C(x+1)/sqrt(x(x+2)) - c,
  i.e. F proportional to w = sqrt(s(s+2T_GH)) plus a linear piece -- and on it J == c IDENTICALLY.
  CONSTRUCTION (parameters r > 1, theta in (0,1) margin, beta in (0,1) plateau fraction):
      lam = r-1,  c = theta/lam,  x1 = beta * 2c^2/(1+2c),  C = (1+c) sqrt(x1/(x1+2)),  k = c/C > 1,
      x2 = k/sqrt(k^2-1) - 1 > x1,
      psi = 1 on [0,x1),  = C(x+1)/sqrt(x(x+2)) - c on [x1,x2],  = 0 on (x2,inf).
  psi(0) = 1, psi non-increasing (psi(x1+) = (x1+1-c)/(x1+2) < 1), psi(inf) = 0, compact support so Int psi < inf,
  Phi continuous at x1 (both readings give Phi(x1) = x1). Then J = -1 on [0,x1), == c on [x1,x2], and
  = (1+1/x)Phi(x2) < c beyond, so sup J = c and lam sup J = theta < 1 STRICTLY.""")

Phi_arc = CS*sp.sqrt(x*(x + 2)) - cS*x
psi_arc = sp.diff(Phi_arc, x)
J_arc = sp.simplify((1 + 1/x)*Phi_arc - (x + 2)*psi_arc)
print(f"\n  sympy:  psi_arc = {sp.simplify(psi_arc)}")
print(f"          J_arc   = {J_arc}")
check(sp.simplify(J_arc - cS) == 0,
      "E1 J == c IDENTICALLY on the arc, symbolically (the C-dependence cancels exactly). This is the whole "
      "theorem: an entire one-parameter family sits ON the (A2) boundary at level c, and c is FREE")
dpsi = sp.simplify(sp.diff((x + 1)/sp.sqrt(x*(x + 2)), x))
check(sp.simplify(dpsi + (x*(x + 2))**sp.Rational(-3, 2)) == 0,
      f"E2 and d/dx[(x+1)/sqrt(x(x+2))] = -(x(x+2))^(-3/2) < 0, so psi_arc is strictly decreasing: the family is "
      f"admissible in shape, not just in the two integral conditions")

def build(r, theta=0.98, beta=0.5):
    lam = r - 1.0; c = theta/lam
    x1 = beta*2.0*c*c/(1.0 + 2.0*c)
    C = (1.0 + c)*math.sqrt(x1/(x1 + 2.0))
    k = c/C
    if k <= 1.0:
        raise ValueError("k <= 1: psi would not reach 0")
    x2 = k/math.sqrt(k*k - 1.0) - 1.0
    return dict(r=r, lam=lam, c=c, theta=theta, x1=x1, x2=x2, C=C, k=k,
                Phi2=C*math.sqrt(x2*(x2 + 2.0)) - c*x2)

def arc_psi(xv, P):
    xv = np.asarray(xv, float); out = np.zeros_like(xv)
    out[xv < P["x1"]] = 1.0
    m = (xv >= P["x1"]) & (xv <= P["x2"]); q = xv[m]
    out[m] = P["C"]*(q + 1.0)/np.sqrt(q*(q + 2.0)) - P["c"]
    return out

def arc_Phi(xv, P):
    xv = np.asarray(xv, float); out = np.empty_like(xv)
    m1 = xv < P["x1"]; out[m1] = xv[m1]
    m2 = (xv >= P["x1"]) & (xv <= P["x2"]); q = xv[m2]
    out[m2] = P["C"]*np.sqrt(q*(q + 2.0)) - P["c"]*q
    out[xv > P["x2"]] = P["Phi2"]
    return out

def audit(psif, Phif, lam, xlo=-16, xhi=16, n=600001, extra=()):
    """min (A2) margin/x, lam*sup J, lam*Phi(inf), min(1-mu), monotonicity. 1-mu written to kill the
    sqrt(1+2/x)-1 cancellation (float64 hazard: the literal 1 - mu loses ALL digits for x > 1e8)."""
    g = np.logspace(xlo, xhi, n)
    for xk in extra:
        g = np.concatenate([g, xk*np.logspace(-6, 6, 4001), [xk]])
    g = np.unique(g)
    ps, Ph = psif(g), Phif(g)
    J = (1 + 1/g)*Ph - (g + 2)*ps
    one_m_mu = (2.0/(np.sqrt(1 + 2/g) + 1) - lam*Ph)/np.sqrt(g*(g + 2))
    return dict(minmarg=float(np.min(g*(1 - lam*J))/1.0), minmargx=float(np.min(1 - lam*J)),
                lamsupJ=float(lam*J.max()), xstar=float(g[np.argmax(J)]),
                lamPhiinf=float(lam*Ph[-1]), min1mmu=float(one_m_mu.min()),
                mono=bool(np.all(np.diff(ps) <= 1e-15)), Jfar=float(J[-1]), Phiinf=float(Ph[-1]))

print(f"\n  {'r':>12}{'lam':>11}{'c':>11}{'x1':>12}{'x2':>9}{'min(1-lam J)':>14}{'lam supJ':>10}"
      f"{'lam Phi_inf':>13}{'min(1-mu)':>12}{'psi dec':>9}")
print("  " + "-" * 113)
E_pass = True; a1_over_a0 = []
for rv in (TWOZ, FOURPI, 100.0, 1.0e4, 1.0e6):
    P = build(rv)
    a1_over_a0.append(math.sqrt(P["x1"]*(P["x1"] + 2))/(2.0/rv))
    A = audit(lambda t, P=P: arc_psi(t, P), lambda t, P=P: arc_Phi(t, P), P["lam"],
              extra=(P["x1"], P["x2"]))
    exh_far.append((f"arc r={rv:.4g}", A["Jfar"], A["Phiinf"]))
    good = (A["minmargx"] > 0 and A["lamsupJ"] < 1.0 and A["lamPhiinf"] < 1.0
            and A["min1mmu"] >= 0 and A["mono"])
    E_pass &= good
    print(f"  {rv:>12.5f}{P['lam']:>11.4f}{P['c']:>11.6f}{P['x1']:>12.4e}{P['x2']:>9.4f}"
          f"{A['minmargx']:>14.6f}{A['lamsupJ']:>10.6f}{A['lamPhiinf']:>13.6f}{A['min1mmu']:>12.3e}"
          f"{str(A['mono']):>9}")
check(E_pass,
      f"E3 *** EVERY r tested -- 2Z (kappa = 1/2), 4 pi (Milgrom 2020), 100, 1e4, 1e6 -- is ADMISSIBLE, with the "
      f"(A2) margin bounded below by (1-theta) x = 0.02 x > 0 and (A1) slack by a factor 3.5. There is NO upper "
      f"bound on r: sup r = +infinity, so mi_r_admissibility_bound_2026.py checks B2 and C1 are WITHDRAWN. "
      f"This check FAILS if any single r listed misses either condition ***")

print(f"  plateau end in acceleration units, a1/a_0 = {['%.4f' % v for v in a1_over_a0]}  (large-r limit "
      f"theta/sqrt(2) = {0.98/math.sqrt(2):.4f})")
check(max(abs(v/(0.98/math.sqrt(2)) - 1) for v in a1_over_a0) < 1.5e-2,
      f"E3b and the exhibit is not a deep-MOND cheat: its plateau (where psi == 1, so F' = r c1p and the master "
      f"formula's I = c2 a^2 with c2 = f'(T_GH)/4pi holds EXACTLY) always extends to a1 = "
      f"{a1_over_a0[0]:.4f} a_0, flat to 0.7% from r = 2Z to r = 1e6. The a^2 regime is a genuine deep-MOND one "
      f"at every r, so q = 2/r is the real crossover of the exhibited kernel and not an artefact of a plateau "
      f"shrinking away")

P2Z = build(TWOZ)
A_lo = audit(lambda t: arc_psi(t, P2Z), lambda t: arc_Phi(t, P2Z), P2Z["lam"], extra=(P2Z["x1"], P2Z["x2"]))
A_hi = audit(lambda t: arc_psi(t, P2Z), lambda t: arc_Phi(t, P2Z), P2Z["lam"], xlo=-18, xhi=18, n=2400001,
             extra=(P2Z["x1"], P2Z["x2"]))
print(f"\n  refinement at r = 2Z:  n = 6.0e5, x in [1e-16,1e16]:  min(1-lam J) = {A_lo['minmargx']:.9f}")
print(f"                         n = 2.4e6, x in [1e-18,1e18]:  min(1-lam J) = {A_hi['minmargx']:.9f}"
      f"   (shift {abs(A_hi['minmargx']-A_lo['minmargx']):.2e})")
check(abs(A_hi["minmargx"] - A_lo["minmargx"]) < 1e-6 and A_hi["minmargx"] > 0,
      f"E4 4x grid and 100x domain move the margin by {abs(A_hi['minmargx']-A_lo['minmargx']):.1e} -- the "
      f"admissibility of r = 2Z is resolved, not a discretisation artefact (hazard H5, which bit this corpus "
      f"twice). Note the exhibit needs NO quadrature at all: Phi is closed form")

# mpmath: at r = 1e6, J ~ 1e-6 is the difference of two O(1) terms -> float64 cancellation must be bounded
P6 = build(1.0e6)
def J_mp(xv, P):
    xv = mpf(xv); c = mpf(P["c"]); C = mpf(P["C"])
    w = msqrt(xv*(xv + 2))
    if xv < mpf(P["x1"]):
        Ph, ps = xv, mpf(1)
    elif xv <= mpf(P["x2"]):
        Ph, ps = C*w - c*xv, C*(xv + 1)/w - c
    else:
        Ph, ps = mpf(P["Phi2"]), mpf(0)
    return (1 + 1/xv)*Ph - (xv + 2)*ps
worst_rel = 0.0
for xv in (P6["x1"]*0.5, P6["x1"]*1.001, 1e-4, 0.05, P6["x2"]*0.999):
    f64 = float((1 + 1/xv)*arc_Phi(np.array([xv]), P6)[0] - (xv + 2)*arc_psi(np.array([xv]), P6)[0])
    ref = float(J_mp(xv, P6))
    worst_rel = max(worst_rel, abs(f64 - ref)/max(abs(ref), 1e-300))
    print(f"  mpmath(50 dps) vs float64 at x = {xv:.4e}:  J = {ref:+.12e}  vs  {f64:+.12e}")
check(worst_rel < 1e-8,
      f"E5 float64 J agrees with 50-digit mpmath to {worst_rel:.1e} relative even at r = 1e6, where J ~ 1e-6 is a "
      f"difference of two O(1) terms. The cancellation is bounded and the margins above are real, not rounding")

# ---------------------------------------------------------------------------------------------------------
banner("F  DOUBLE SCRUTINY -- a COMPLETELY MONOTONE, closed-form, real-analytic psi reaching r = 2Z")

print("""  The section-E exhibit has a jump in psi (a kink in f'), and the natural objection is that a physical
  spectral kernel should be smooth -- indeed completely monotone (a Laplace transform of a positive measure,
  Bernstein), which is what a positive spectral density would deliver. So take the strongest available class:
      psi(s) = (1 + s/delta)^(-1/2) (1 + s/Delta)^(-1),   delta = 1e-3 T_GH, Delta = 0.1 T_GH,
  a PRODUCT of two completely monotone factors, hence completely monotone, hence C^infinity, strictly positive,
  strictly decreasing, and integrable (tail s^(-3/2)). Its Phi is closed form:
      Phi(x) = 2 Delta' k [ arctan(k sqrt(1+x/delta')) - arctan(k) ],  k = sqrt(delta'/(Delta'-delta')),
  written as one arctan of a difference-free argument to avoid the small-x cancellation.""")

dlt, Dlt = 1e-3, 1e-1
KAP = math.sqrt(dlt/(Dlt - dlt))
def cm_psi(xv):
    xv = np.asarray(xv, float)
    return (1.0 + xv/dlt)**-0.5/(1.0 + xv/Dlt)
def cm_Phi(xv):
    xv = np.asarray(xv, float); q = np.sqrt(1.0 + xv/dlt)
    return 2*Dlt*KAP*np.arctan(KAP*(xv/dlt)/((q + 1.0)*(1.0 + KAP*KAP*q)))
for xv in (1e-6, 1e-2, 1.0, 1e3):
    print(f"  Phi closed form vs quad at x = {xv:.0e}: {cm_Phi(np.array([xv]))[0]:.12e} vs "
          f"{quad(lambda t: float(cm_psi(np.array([t]))[0]), 0, xv, limit=200)[0]:.12e}")
check(max(abs(cm_Phi(np.array([xv]))[0]/quad(lambda t: float(cm_psi(np.array([t]))[0]), 0, xv, limit=200)[0] - 1)
          for xv in (1e-6, 1e-2, 1.0, 1e3)) < 1e-8,
      "F1 the closed-form Phi matches adaptive quadrature to 1e-8 at four decades, so the completely monotone "
      "exhibit carries no quadrature error either")

Acm = audit(cm_psi, cm_Phi, TWOZ - 1.0)
Acm4 = audit(cm_psi, cm_Phi, TWOZ - 1.0, xlo=-18, xhi=18, n=2400001)
J_of_lam1 = Acm["lamsupJ"]/(TWOZ - 1.0)                      # = sup J
lam_max_cm = 1.0/J_of_lam1
print(f"\n  at r = 2Z (lam = {TWOZ-1:.6f}):  lam sup J = {Acm['lamsupJ']:.8f} <= 1   lam Phi_inf = "
      f"{Acm['lamPhiinf']:.6f} <= 1   min(1-mu) = {Acm['min1mmu']:.3e}   (A2) binds at x* = {Acm['xstar']:.4e}")
print(f"  4x refinement: lam sup J = {Acm4['lamsupJ']:.8f}  (shift {abs(Acm4['lamsupJ']-Acm['lamsupJ']):.1e})")
print(f"  this single shape is admissible up to lam_max = {lam_max_cm:.4f}, i.e. r_max = {1+lam_max_cm:.4f}")
exh_far.append(("CM exhibit", Acm4["Jfar"], Acm4["Phiinf"]))
check(Acm["lamsupJ"] < 1.0 and Acm["lamPhiinf"] < 1.0 and Acm["min1mmu"] >= 0 and Acm["mono"]
      and abs(Acm4["lamsupJ"] - Acm["lamsupJ"]) < 1e-6,
      f"F2 *** r = 2Z is admissible on a COMPLETELY MONOTONE, real-analytic, strictly positive psi with "
      f"lam sup J = {Acm['lamsupJ']:.4f} -- a {100*(1-Acm['lamsupJ']):.0f}% margin, refinement-stable to "
      f"{abs(Acm4['lamsupJ']-Acm['lamsupJ']):.0e}. Smoothness, positivity and complete monotonicity do NOT "
      f"restore the exclusion. This check FAILS if lam sup J or lam Phi_inf exceeds 1 ***")
check(1 + lam_max_cm > TWOZ and 1 + lam_max_cm > FOURPI,
      f"F3 that one shape's own ceiling is r_max = {1+lam_max_cm:.4f}, which clears BOTH 2Z = {TWOZ:.4f} (by a "
      f"factor {lam_max_cm/(TWOZ-1):.2f} in lam) and 4 pi = {FOURPI:.4f}. So the exclusion did not fail by a "
      f"hair on a contrived shape; it fails by a wide margin on a two-line one")

def cm_lp(tlo, thi, NT=160, xlo=1e-10, xhi=1e6, NX=900):
    t = np.logspace(math.log10(tlo), math.log10(thi), NT)
    xv = np.logspace(math.log10(xlo), math.log10(xhi), NX)
    TX = np.outer(xv, t)
    Jm = (1 + 1/xv)[:, None]*(-np.expm1(-TX))/t[None, :] - (xv + 2)[:, None]*np.exp(-TX)
    A = np.hstack([Jm, -np.ones((NX, 1))])
    Aeq = np.zeros((1, NT + 1)); Aeq[0, :NT] = 1.0
    obj = np.zeros(NT + 1); obj[-1] = 1.0
    res = linprog(obj, A_ub=A, b_ub=np.zeros(NX), A_eq=Aeq, b_eq=[1.0],
                  bounds=[(0, None)]*NT + [(-2, 5)], method="highs")
    return res.x[-1]
print(f"\n  LP over ALL completely monotone psi (mixtures of exponentials, psi = Int e^(-xt) drho(t)):")
print(f"  {'rate range':>22}{'c*':>14}{'r_max (CM)':>14}")
cmr = {}
for tlo, thi in ((1e-2, 1e2), (1e-2, 1e4), (1e-2, 1e6), (1e-2, 1e8)):
    cst = cm_lp(tlo, thi); cmr[thi] = 1 + 1/cst
    print(f"  [{tlo:.0e}, {thi:.0e}]{cst:>19.6e}{1+1/cst:>14.4f}")
check(min(cmr.values()) > TWOZ and cmr[1e8]/cmr[1e4] > 50,
      f"F4 and the LP over the WHOLE completely monotone class is unbounded too: r_max = {cmr[1e2]:.2f} -> "
      f"{cmr[1e8]:.0f} as the spectral range widens, growing like sqrt(t_max), every value above 2Z. So no "
      f"positivity/Herglotz-type postulate on the spectral measure rescues a bound either")

# ---------------------------------------------------------------------------------------------------------
banner("G  IS THE r = 2Z KERNEL SANE? nu(y) on y in [1e-4, 1e4], on the completely monotone exhibit")

lam2Z = TWOZ - 1.0
gx = np.logspace(-14, 10, 2000001)
a_of_x = np.sqrt(gx*(gx + 2))                         # a in units of c H_Lambda
mu = (gx + lam2Z*cm_Phi(gx))/a_of_x
a0_units = 2.0/TWOZ                                   # a_0/(c H_Lambda) = q = 2/r
yv = mu*a_of_x/a0_units                               # y = g_bar/a_0, g_bar = mu * g_obs
nuv = 1.0/mu
sel = (yv >= 1e-4) & (yv <= 1e4)
i_hi = int(np.argmin(abs(yv - 1e4))); i_lo = int(np.argmin(abs(yv - 1e-4)))
print(f"  mu on the window: [{mu[sel].min():.6f}, {mu[sel].max():.6f}]   strictly increasing: "
      f"{bool(np.all(np.diff(mu[sel]) > 0))}  (min increment {np.diff(mu[sel]).min():.2e})")
print(f"  y strictly increasing in a: {bool(np.all(np.diff(yv[sel]) > 0))}")
print(f"  Newtonian end : nu(y = {yv[i_hi]:.4e}) = {nuv[i_hi]:.8f}          -> 1")
print(f"  deep end      : nu * sqrt(y) at y = {yv[i_lo]:.4e} = {nuv[i_lo]*math.sqrt(yv[i_lo]):.8f}  -> 1")
check(np.all(np.diff(mu[sel]) > 0) and mu[sel].min() > 0 and mu[sel].max() <= 1.0
      and abs(nuv[i_hi] - 1.0) < 1e-3 and abs(nuv[i_lo]*math.sqrt(yv[i_lo]) - 1.0) < 1e-3
      and np.all(np.diff(yv[sel]) > 0),
      f"G1 the r = 2Z kernel is a sane MOND kernel across eight decades: mu strictly increasing inside (0,1], "
      f"y monotone in a, nu -> 1 at the Newtonian end ({nuv[i_hi]:.6f}) and nu -> y^(-1/2) at the deep end "
      f"(nu sqrt(y) = {nuv[i_lo]*math.sqrt(yv[i_lo]):.6f}). No wiggle, no multivaluedness, no super-Newtonian "
      f"region. This check FAILS on any of the five failure modes")

x_tr = (dlt, Dlt)
print(f"\n  and the shape's own transition sits where MOND's does: delta, Delta = {dlt:.0e}, {Dlt:.0e} in x "
      f"correspond to a/a_0 = {math.sqrt(dlt*(dlt+2))/a0_units:.3f} to {math.sqrt(Dlt*(Dlt+2))/a0_units:.3f}")
a0_can = CHL*2.0/TWOZ
OmL = 0.6847
a0_alt = CHL/math.sqrt(OmL)*2.0/TWOZ
print(f"  a_0 from r = 2Z, CANONICAL footing (rho_DE, c H_Lambda = {CHL:.4e}):  a_0 = {a0_can:.6e} m/s^2 "
      f"(= c H_Lambda/Z; brief 9.3614e-11)")
print(f"  a_0 from r = 2Z, ALT footing (rho_total, c H_0 = {CHL/math.sqrt(OmL):.4e}): a_0 = {a0_alt:.6e} m/s^2 "
      f"(brief 1.13e-10), ratio {1/math.sqrt(OmL):.4f}")
check(abs(a0_can/9.3614e-11 - 1) < 3e-4 and abs(a0_alt/1.13e-10 - 1) < 2e-3
      and abs((a0_alt/a0_can)/1.2082 - 1) < 3e-4,
      f"G2 r = 2Z delivers a_0 = {a0_can:.4e} on the canonical footing and {a0_alt:.4e} on the ALT footing, ratio "
      f"{a0_alt/a0_can:.4f} = 1/sqrt(Omega_Lambda). BOTH footings need the SAME r, because r = 2/q is a RATIO of "
      f"a_0 to the floor and both sides of the fork scale together -- so nothing in this script is "
      f"footing-dependent, and the fork cannot rescue or damage the conclusion")

check(all(abs(Jf/Pi - 1) < 1e-6 for _, Jf, Pi in exh_far),
      f"G3 Lemma 2 verified on all {len(exh_far)} exhibits: J(x -> inf)/Phi(inf) = 1 to better than 1e-6, so "
      f"(A1) really is the x -> inf limit of (A2) and adds nothing. Only (A2) ever binds -- which answers the "
      f"brief's 'which constraint binds' with: (A2), always")

# ---------------------------------------------------------------------------------------------------------
banner("H  WHAT ACTUALLY BINDS, AND THE EXACT MENU BOUND (which is 9, not 9.016763)")

print("""  WHY THE EQUALITY CASE DOES NOT HAND YOU r = infinity FOR FREE. The pure equality solution is F = C w,
  w = sqrt(s(s+2T_GH)): it has F'(0) = infinity, so r = infinity formally -- but c1p = lim F/s = C, so
  mu = F/(c1p w) == 1 IDENTICALLY and q = 2 c1p/F'(0) = 0. r = infinity IS the Newtonian endpoint a_0 = 0, not a
  MOND theory. Finite r comes from splicing a COMPACT segment of the equality locus onto the plateau psi = 1, and
  on that segment (at theta = 1) mu is exactly the constant lam C = 1/k < 1. What sets r is how EARLY you may
  enter the arc, and the answer is:  entering at plateau length x1 is admissible iff  c >= c_min(x1), i.e.
      r <= 1 + 2/(x1 + sqrt(x1(x1+2))),   sharp within the family,
  because for c < c_min one gets k < 1 and then psi(inf) = C - c > 0: psi never reaches zero and the theory has
  no Newtonian limit. THAT is the binding structure -- integrability of psi against the plateau length -- and
  since x1 -> 0 is allowed, nothing bounds r. Read as a statement about a_0 it says only
      a_0 >~ (the acceleration at which the inertia kernel leaves its floor value),
  a constraint on the SHAPE SCALE, not on the coefficient. Toothless on kappa.""")

sC, sc = sp.symbols("C c", positive=True)
Fw = sC*sp.sqrt(x*(x + 2))
c1p_w = sp.limit(Fw/x, x, sp.oo)
mu_w = sp.simplify(Fw/(c1p_w*sp.sqrt(x*(x + 2))))
Fp0 = sp.limit(sp.diff(Fw, x), x, 0, "+")
print(f"\n  F = C w:   c1p = {c1p_w}   F'(0+) = {Fp0}   mu = {mu_w}   =>  q = 2 c1p/F'(0) = 0")
check(c1p_w == sC and mu_w == 1 and Fp0 == sp.oo,
      "H1 sympy confirms the equality case has c1p = C, F'(0+) = infinity and mu == 1, hence q = 0: the r -> "
      "infinity limit of the family is Newtonian gravity with a_0 = 0, which is why an infinite slope at the "
      "floor is not by itself a large a_0-suppression")

x1s = sp.symbols("x1", positive=True)
c_min_expr = (x1s + sp.sqrt(x1s*(x1s + 2)))/2
sol = sp.solve(sp.Eq(2*cS**2/(1 + 2*cS), x1s), cS)
print(f"  c_min(x1) solving 2c^2/(1+2c) = x1:  {[sp.simplify(v) for v in sol if sp.simplify(v).is_real is not False]}")
check(any(sp.simplify(v - c_min_expr) == 0 for v in sol),
      f"H2 c_min(x1) = (x1 + sqrt(x1(x1+2)))/2 EXACTLY -- i.e. c_min = (x1 + a1)/2 where a1 = sqrt(x1(x1+2)) is "
      f"the acceleration at the end of the plateau, in units of c H_Lambda. So r_max(x1) = 1 + 2/(x1+a1) ~ "
      f"2/a1 for small a1, i.e. a_0 >~ a1 c H_Lambda: admissibility ties a_0 to the SHAPE scale and to nothing "
      f"else")
xt = 7.2418e-3
cm_ = float(c_min_expr.subs(x1s, xt))
def k_of(x1v, cv):                       # k = c/C decides whether psi ever reaches 0
    return cv/((1.0 + cv)*math.sqrt(x1v/(x1v + 2.0)))
k_above, k_below = k_of(xt, cm_*1.02), k_of(xt, cm_*0.9995)
print(f"  at x1 = {xt:.4e}: c_min = {cm_:.6f} -> r_max = {1+1/cm_:.4f};  k(c = 1.02 c_min) = {k_above:.6f} > 1 "
      f"(builds, psi -> 0),  k(c = 0.9995 c_min) = {k_below:.6f} <= 1 (psi(inf) = C - c = "
      f"{(1+cm_*0.9995)*math.sqrt(xt/(xt+2)) - cm_*0.9995:+.3e} > 0, no Newtonian limit)")
check(k_below <= 1.0 < k_above and abs(k_of(xt, cm_) - 1.0) < 1e-9 and 1 + 1/cm_ > TWOZ,
      f"H3 the sharp edge is real and k(c_min) = 1 exactly: 0.05% below c_min the construction cannot be built "
      f"(k <= 1, psi(inf) > 0, no Newtonian limit) while 2% above it builds. And even this SHARP family bound "
      f"at x1 = {xt:.2e} is "
      f"r <= {1+1/cm_:.3f} > 2Z, so 2Z is inside the sharp bound at that plateau length, not sneaking past a "
      f"soft one")

def sech(u):
    au = np.abs(u); return 2*np.exp(-au)/(1 + np.exp(-2*au))
def X4(u):
    s2 = math.sqrt(2.0)
    return (1/(4*s2))*(np.log((u*u + s2*u + 1)/(u*u - s2*u + 1))
                       + 2*(np.arctan(s2*u + 1) + np.arctan(s2*u - 1)))
SHAPES = {"exp(-s/d)":     (lambda u: np.exp(-u),      lambda u: -np.expm1(-u)),
          "exp(-(s/d)^2)": (lambda u: np.exp(-u*u),    lambda u: math.sqrt(math.pi)/2*erf(u)),
          "sech(s/d)":     (sech,                      lambda u: 2*np.arctan(np.tanh(u/2))),
          "1/(1+(s/d)^2)": (lambda u: 1/(1 + u*u),     lambda u: np.arctan(u)),
          "(1+s/d)^-2":    (lambda u: (1 + u)**-2.0,   lambda u: u/(1 + u)),
          "(1+s/d)^-3":    (lambda u: (1 + u)**-3.0,   lambda u: 0.5*(1 - (1 + u)**-2.0)),
          "1/(1+(s/d)^4)": (lambda u: 1/(1 + u**4),    X4)}
def menu_lam_max(nm, d, n=3000001):
    chi, Xf = SHAPES[nm]
    u = np.logspace(-9, 11, n); xv = d*u
    J = (1 + 1/xv)*(d*Xf(u)) - (xv + 2)*chi(u)
    return 1.0/J.max()
print(f"\n  EXACT ceiling of each committed menu shape (delta -> 0 limit, where each is largest):")
print(f"  {'psi shape':<18}{'lam_max(d=1e-5)':>18}{'lam_max(d=1e-7)':>18}{'r_max':>10}")
mx = 0.0
for nm in SHAPES:
    v5, v7 = menu_lam_max(nm, 1e-5), menu_lam_max(nm, 1e-7)
    mx = max(mx, v7)
    print(f"  {nm:<18}{v5:>18.6f}{v7:>18.6f}{1+v7:>10.6f}")
lam_pl = lambda d: 4*(2 - d)**2/(2 + 7*d - 4*d*d)
print(f"\n  closed form for the best menu shape (1+s/d)^-2, from K = x d (x^2+x-d)/(d+x)^2 minimised at "
      f"x* = 3d/(1-2d):   lam_max(d) = 4(2-d)^2/(2+7d-4d^2)")
for d in (1e-3, 1e-5, 1e-7):
    print(f"    d = {d:.0e}:  closed form {lam_pl(d):.9f}   direct numeric {menu_lam_max('(1+s/d)^-2', d):.9f}")
check(max(abs(lam_pl(d)/menu_lam_max("(1+s/d)^-2", d) - 1) for d in (1e-3, 1e-5, 1e-7)) < 1e-5
      and abs(lam_pl(1e-9) - 8.0) < 1e-7 and mx < 8.0 + 1e-4,
      f"H4 the exact ceiling of the committed 7-shape menu is r = 1 + 8 = 9 EXACTLY (closed form, delta -> 0, "
      f"attained only in the limit), and every other shape is strictly below: max lam over the menu = "
      f"{mx:.6f}. The committed value 9.016763 is {100*(MENU_MAX_COMMITTED/9-1):.3f}% HIGH -- a trapezoid/grid "
      f"bias, not a shape that beats the limit")
check(abs(MENU_MAX_COMMITTED/9.0 - 1) < 5e-3 and MENU_MAX_COMMITTED > 9.0,
      f"H5 and the size of that bias is {100*(MENU_MAX_COMMITTED/9-1):.3f}%, far too small to have changed that "
      f"script's own conclusion (9.017 vs 9 are both below 2Z). Its ARITHMETIC was fine; what was wrong was "
      f"the inference from seven single-scale shapes to a bound -- exactly the caveat it wrote down itself")

# ---------------------------------------------------------------------------------------------------------
banner("I  AGAINST INTEREST")
print(f"""  Recorded because it is where this leaves the programme, and it is not where the framework would want.
   - THIS DOES NOT DERIVE kappa = 1/2 AND MAKES IT HARDER TO. The admissible set of r is now [0, infinity):
     Lemma 1 gives all of [0,1] for free (a_0 >= 2 c H_Lambda unconstrained), section E gives every r > 1. A
     constraint that admits everything discriminates nothing, so the master-formula class provably CANNOT
     derive any coefficient by admissibility -- 2Z included. The one route that could have DERIVED a_0 in this
     class is closed by theorem, not by another failed search. a_0's value stays a fitted one-parameter input.
   - IT ALSO REPEALS A NO-GO AGAINST THE COMPETITION. r = 4 pi = {FOURPI:.6f} is admissible on exactly the same
     footing, and 4 pi has an obvious mechanism (a horizon-area/solid-angle normalisation) that 2Z does not.
     The previous exclusion was doing the framework a favour it was not entitled to.
   - THE PRICE OF REACHING 2Z IS A SECOND SCALE TUNED TO a_0. The single-scale menu ceiling is exactly r = 9
     (H4), and 9 < 2Z = {TWOZ:.4f} < 4 pi, so BOTH live coefficients require a psi with two scales, with the
     inner one at a ~ a_0 (section G: the exhibit's delta, Delta sit at a/a_0 = 0.26 to 2.65). H2 says why: the
     bound is r <~ 2/a1, so a large r REQUIRES a shape that leaves its floor below a_0. The coefficient is
     smuggled in through the shape scale -- which is the definition of fitting it.
   - MILGROM'S COEFFICIENTS REMAIN THE ONLY ONES THAT NEED NOTHING. r = 1 (f = T, his 1999 eqs 6-9) passes with
     the maximal margin and no shape freedom at all, and r = 2 (his eqs 10-11) passes on every one of the seven
     single-scale shapes. On any simplicity ordering, HIS value is still the one the class prefers -- which is
     the same verdict this corpus already records from the other side (the two natural constants in the a_0 box
     are both Z = 2 pi), and it is not changed by anything here.
   - SCOPE. Sections E/F prove admissibility (mu <= 1, mu monotone). They do NOT prove that the exhibited f is
     derivable from a microphysical response, that psi's two scales are natural, or that anything selects the
     exhibit over Milgrom's f = T. And the LP r_max values in section D are discretisation-limited upper
     estimates; the certified statements are the closed-form exhibits, which need no quadrature.""")
check(9.0 < TWOZ < FOURPI and abs(FOURPI/TWOZ - 1) < 0.09,
      f"I1 the ordering that carries the against-interest reading: single-scale ceiling 9 < 2Z = {TWOZ:.4f} < "
      f"4 pi = {FOURPI:.4f}, with 2Z and 4 pi only {100*(FOURPI/TWOZ-1):.2f}% apart. Even a real admissibility "
      f"bound could never have separated the two live coefficients at that spacing")

banner("RESULT")
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c: print(f"    - {m}")
    sys.exit(1)
print(f"  r_max from the OPTIMISER: unbounded (LP {lp[1e-8]:.0f} at x_min = 1e-8, growing as x_min^(-1/2)).")
print(f"  r_max from THEOREM: +infinity (explicit psi for every r > 1, strict margins, section E).")
print(f"  vs best menu shape 9 (exactly), 2Z = {TWOZ:.6f}, 4 pi = {FOURPI:.6f}: BOTH admissible.")
print(f"  Binding constraint: (A2) always, on an interval; (A1) is implied by (A2) at x -> inf and never binds.")
print(f"  mi_r_admissibility_bound_2026.py checks B2 and C1 are WITHDRAWN.")
print(f"  kappa = 1/2 remains FITTED, NOT DERIVED -- and by the theorem above, underivable from admissibility.")
