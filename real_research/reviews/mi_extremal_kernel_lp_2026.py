#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LANE X -- THE EXTREMAL KERNEL PRINCIPLE, settled by linear programming.
mi_extremal_kernel_lp_2026.py

CONTEXT. Master formula (mi_crossover_master_formula_2026.py): I = f(T)-f(T_GH),
T = sqrt(a^2+H^2)/2pi, q = a_0/(cH_Lambda) = 2/r, r = f'(T_GH)/c1p.
Admissibility class (mi_r_admissibility_bound_2026.py), T_GH-units, s = T-T_GH:
F'(s) = c1p [1 + (r-1) psi(s)], psi(0)=1, psi decreasing to 0, Int psi finite:
  (A1) mu <= 1       <=>  (r-1) Int_0^inf psi <= T_GH
  (A2) mu monotone   <=>  F'(s) s (s+2T_GH) >= F(s) (s+T_GH)   for all s > 0
The 7-shape x 220-scale scan gave "max admissible r = 9.016763" (not a proof).

STRUCTURAL FACT exploited here: for FIXED r both (A1),(A2) are LINEAR in psi,
so feasibility at fixed r is an LP; and with the exact substitution
phi = (r-1) psi the whole problem is ONE LP:  maximize lam = phi(0)  s.t.
phi decreasing >= 0,  s + phi(s) s(s+2T) - Phi(s)(s+T) >= 0,  Phi(inf) <= T,
with Phi = Int_0^s phi and sup r = 1 + lam*.  (Feasible psi at r* stays
feasible for every r <= r*: the constraint only binds where the psi-bracket is
negative, and shrinking r-1 relaxes exactly those rows.)

RESULT (this script): THE SUPREMUM IS +INFINITY. The admissibility class as
stated does NOT bound r at all. Two independent demonstrations:
  (1) LP: sup r on a grid grows as smin^(-1/2) with no ceiling
      (212 -> 2120 -> 21202 -> 212088 as smin = 1e-4 -> 1e-10);
  (2) an EXPLICIT hand-built family (no LP): continuous piecewise-linear
      "cascade" kernels with n nested levels h^k at scales alpha^k
      (h=0.55, alpha=12) reach r_max ~ 18.5, 106, 634 for n = 6, 9, 12 --
      each certified by direct evaluation of (A1),(A2) on a dense grid.
Mechanism: a decreasing psi may step DOWN by a factor ~1/2 essentially for
free (the Newtonian +s term pays for each drop), and n nested near-halvings
relabel r -> r/2^n; the integral (A1)/tail cost only fixes scale ratios.
The seven-shape scan bound was a SINGLE-SCALE SHAPE ARTEFACT.

CONSEQUENCES, both halves, no softening:
  (i)  kappa = 1/2 canonical (r = 2Z = 11.578) is REACHABLE: admissibility
       does NOT exclude it. The "28% above the bound" pressure is VOID.
  (ii) the tantalising 0.17% match of 2 cH_L/9.0167 with McGaugh's 1.20e-10
       is ALSO VOID as a derivation: admissibility alone selects NO r, hence
       derives NO a_0 -- on either footing. (Chance baseline in this project:
       10/19 targets hit by chance. This one no longer even has a principle
       attached.) Any revival requires an EXTRA assumption (e.g. single-scale
       /unimodal psi), which is currently unjustified.
kappa = 1/2 remains FITTED, NOT DERIVED.

CREDIT: nu = sqrt(1+1/y) and the dS-Unruh balance are Milgrom 1999 PLA 253:273
eqs 6-9 (his eqs 10-11 a second coefficient; Milgrom 2008 arXiv:0801.3133 sec
7.3.1: the mismatch "isn't necessarily meaningful"). a_lambda = c^2
sqrt(Lambda/3): Milgrom 1994 Ann.Phys. 229:384. T = sqrt(a^2+Lambda/3)/2pi:
Narnhofer-Peter-Thirring 1996 IJMPB 10:1507. Exponential kernel: McGaugh 2008
ApJ 683:137 eq 11a. RAR kernel: Lelli-McGaugh-Schombert. Empirical a_0 =
1.2e-10: McGaugh / SPARC.
"""
import sys
import numpy as np
from scipy.optimize import linprog

np.seterr(all="ignore")   # Accelerate BLAS raises spurious FP flags in matmul;
                          # finiteness is asserted explicitly where it matters.

CHL      = 5.4194e-10        # c H_Lambda [m/s^2]
A0_CANON = 9.3614e-11        # kappa=1/2 canonical (rho_DE + cH_Lambda)
A0_ALT   = 1.13e-10          # ALT footing (x1.2082)
A0_EMP   = 1.20e-10          # McGaugh empirical
R_SHAPE  = 9.016763
R_2Z     = 11.5776100732     # 2Z, kappa=1/2 canonical
R_TARGETS = [
    ("7-shape scan bound",         9.016763),
    ("McGaugh empirical 1.20e-10", 2*CHL/A0_EMP),
    ("ALT footing 1.13e-10",       2*CHL/A0_ALT),
    ("SPARC 1.15x refit",          10.0676),
    ("2Z  (kappa=1/2 canonical)",  R_2Z),
    ("4pi (2pi a0 ~ cH_L)",        4*np.pi),
]

checks = []
def check(name, ok, detail=""):
    checks.append(bool(ok))
    print(("[OK]   " if ok else "[FAIL] ") + name + (("  " + detail) if detail else ""))

# ------------------------------------------------------------------ LP pieces
def make_grid(smin, smax, N):
    return np.geomspace(smin, smax, N)

def trap_matrix(s):
    """Psi_i = Int_0^{s_i} psi (trapezoid with a node at s=0).
    Psi = W @ psi + w0 * psi(0). Exact for piecewise-linear psi."""
    N = len(s)
    ds = np.diff(np.concatenate(([0.0], s)))
    W  = np.zeros((N, N)); w0 = np.zeros(N)
    w0 += 0.5*ds[0]; W[:, 0] += 0.5*ds[0]
    for j in range(1, N):
        W[j:, j-1] += 0.5*ds[j]; W[j:, j] += 0.5*ds[j]
    return W, w0

def a2_rows(s, W, w0, T):
    """A2 at nodes, vars x=[lam, phi]: Phi(s+T) - phi s(s+2T) <= s, row-scaled."""
    N = len(s)
    A = np.zeros((N, N+1))
    A[:, 0]  = w0*(s+T)
    A[:, 1:] = W*(s+T)[:, None]
    A[np.arange(N), 1+np.arange(N)] -= s*(s+2*T)
    sc = 1.0/(s*(s+2*T))
    return A*sc[:, None], s*T*sc      # Newtonian term of A2 is s*T, not s

def midpoint_a2_rows(s, W, w0, T):
    """A2 at log-midpoints (psi piecewise-linear in s; still linear in vars)."""
    N = len(s)
    sm = np.sqrt(s[:-1]*s[1:])
    t  = (sm - s[:-1])/(s[1:] - s[:-1])
    A = np.zeros((N-1, N+1))
    for k in range(N-1):
        h = sm[k] - s[k]
        row = np.zeros(N+1)
        row[0] = w0[k]; row[1:] = W[k]
        row[1+k]   += 0.5*h*(2.0 - t[k])       # Phi(sm)=Phi_k+0.5(phi_k+phi_m)h
        row[1+k+1] += 0.5*h*t[k]
        A[k]  = row*(sm[k]+T)
        A[k, 1+k]   -= (1.0-t[k])*sm[k]*(sm[k]+2*T)
        A[k, 1+k+1] -= t[k]      *sm[k]*(sm[k]+2*T)
    sc = 1.0/(sm*(sm+2*T))
    return A*sc[:, None], sm*T*sc

def build_lp(s, T):
    N = len(s)
    W, w0 = trap_matrix(s)
    # monotone: phi_1 <= lam; phi_{i+1} <= phi_i
    M = np.zeros((N, N+1))
    M[0, 0], M[0, 1] = -1.0, 1.0
    for i in range(1, N):
        M[i, i], M[i, i+1] = -1.0, 1.0
    A1r, b1r = a2_rows(s, W, w0, T)
    A2r, b2r = midpoint_a2_rows(s, W, w0, T)
    # tail (psi == 0 beyond s_N): Phi_N <= T (A1) and Phi_N <= s_N T/(s_N+T)
    tail = np.zeros((2, N+1))
    tail[0, 0], tail[0, 1:] = w0[-1], W[-1]
    tail[1] = tail[0]
    A_ub = np.vstack([M, A1r, A2r, tail])
    b_ub = np.concatenate([np.zeros(N), b1r, b2r,
                           [T, s[-1]*T/(s[-1]+T)]])
    c = np.zeros(N+1); c[0] = -1.0
    return c, A_ub, b_ub, W, w0

def solve_direct(s, T, B=1e7):
    c, A, b, W, w0 = build_lp(s, T)
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(0.0, B)]*(len(s)+1), method="highs")
    if res.status != 0:
        raise RuntimeError("direct LP status %d: %s" % (res.status, res.message))
    lam = res.x[0]
    return 1.0 + lam, res.x[1:]/max(lam, 1e-300)

def feasible_at_r(s, T, r, tol=1e-7):
    """Bisection route: fixed r, vars phi only (lam = r-1 constant).
    Robust phase-1 form: minimise the worst A2/tail violation t; feasible iff
    t* <= tol. phi <= r-1 exactly (monotone from phi(0) = lam)."""
    N = len(s)
    c, A, b, W, w0 = build_lp(s, T)
    lam = r - 1.0
    A_phi = A[:, 1:]; b_phi = b - A[:, 0]*lam
    tcol = np.zeros((A_phi.shape[0], 1)); tcol[N:, 0] = -1.0  # slack A2+tail only
    res = linprog(np.concatenate([np.zeros(N), [1.0]]),
                  A_ub=np.hstack([A_phi, tcol]), b_ub=b_phi,
                  bounds=[(0.0, lam)]*N + [(0.0, None)], method="highs")
    if res.status != 0:
        raise RuntimeError("phase-1 LP status %d at r=%.4f" % (res.status, r))
    return res.x[-1] <= tol

def bisect_sup(s, T, lo, hi, rtol=1e-4):
    if not feasible_at_r(s, T, lo): raise RuntimeError("lo infeasible")
    if feasible_at_r(s, T, hi):     raise RuntimeError("hi feasible")
    while (hi - lo)/lo > rtol:
        mid = 0.5*(lo + hi)
        if feasible_at_r(s, T, mid): lo = mid
        else:                        hi = mid
    return lo, hi

def maximin_at_r(s, T, r):
    """At fixed r, maximise the minimum row-scaled A2/tail slack -> robust psi."""
    N = len(s)
    c, A, b, W, w0 = build_lp(s, T)
    lam = r - 1.0
    A_phi = A[:, 1:]; b_phi = b - A[:, 0]*lam
    tcol = np.zeros((A_phi.shape[0], 1)); tcol[N:, 0] = 1.0   # slack on A2+tail
    Ax = np.hstack([A_phi, tcol])
    cobj = np.zeros(N+1); cobj[-1] = -1.0
    res = linprog(cobj, A_ub=Ax, b_ub=b_phi,
                  bounds=[(0.0, lam)]*N + [(0.0, 10.0)], method="highs")
    if res.status != 0:
        raise RuntimeError("maximin LP status %d" % res.status)
    return res.x[:N]/lam, res.x[-1]

# ------------------------------------------ direct evaluation (no LP) pieces
def eval_G(bp, pv, r, T=1.0, M=400000):
    """min over a dense grid of G = s + (r-1)[psi s(s+2T) - Psi(s+T)] for the
    piecewise-linear psi given by knots (bp, pv), psi=0 beyond bp[-1].
    Trapezoid on a grid containing every knot is EXACT for pw-linear psi.
    Returns (min scaled G, Psi_inf, A1 slack, tail slack)."""
    sg = np.geomspace(max(bp[1]*1e-3, 1e-30), bp[-1], M)
    sg = np.unique(np.concatenate((sg, bp[1:])))
    psi = np.interp(sg, bp, pv)
    ds  = np.diff(np.concatenate(([0.0], sg)))
    pm  = 0.5*(np.concatenate(([pv[0]], psi[:-1])) + psi)
    Psi = np.cumsum(pm*ds)
    G = sg*T + (r-1.0)*(psi*sg*(sg+2*T) - Psi*(sg+T))
    Gs = G/(sg*(sg+2*T))
    a1 = T - (r-1.0)*Psi[-1]
    tl = sg[-1]*T/(sg[-1]+T) - (r-1.0)*Psi[-1]
    assert np.all(np.isfinite(Gs)) and np.isfinite(a1)
    return Gs.min(), Psi[-1], a1, min(a1, tl)

def r_max_of(bp, pv, T=1.0, M=400000):
    """Largest admissible r for a FIXED pw-linear psi (closed form: the
    constraint is affine in r-1)."""
    sg = np.geomspace(max(bp[1]*1e-3, 1e-30), bp[-1], M)
    sg = np.unique(np.concatenate((sg, bp[1:])))
    psi = np.interp(sg, bp, pv)
    ds  = np.diff(np.concatenate(([0.0], sg)))
    pm  = 0.5*(np.concatenate(([pv[0]], psi[:-1])) + psi)
    Psi = np.cumsum(pm*ds)
    Brk = psi*sg*(sg+2*T) - Psi*(sg+T)
    neg = Brk < 0
    bound = np.min(sg[neg]*T/(-Brk[neg])) if neg.any() else np.inf
    return 1.0 + min(bound, T/Psi[-1])

def cascade_psi(n, h=0.55, alpha=12.0, eps=1e-3, send=0.05):
    """Continuous piecewise-linear cascade: plateau levels h^k on geometric
    scales alpha^k, steep linear ramps of relative width eps, support [0,send].
    psi(0)=1, decreasing to 0, Int psi finite: IN THE ADMISSIBILITY CLASS."""
    w = send*alpha**(-float(n))
    bp = [0.0]; pv = [1.0]
    for k in range(1, n+1):
        b = w*alpha**k
        bp += [b, b*(1.0+eps)]
        pv += [h**(k-1), (h**k if k < n else 0.0)]
    return np.array(bp), np.array(pv)

# ------------------------------------------------------------------ kernels
def mu_from_psi(s, psi, r, T=1.0):
    W, w0 = trap_matrix(s)
    Psi = W@psi + w0*1.0
    F   = s + (r-1.0)*Psi
    mu  = F/np.sqrt(s*(s+2*T))
    x   = 0.5*r*np.sqrt(s*(s+2*T))/T          # x = a/a0 with a0 = 2 cH_L/r
    return x, mu

def nu_milgrom99(y): return np.sqrt(1.0 + 1.0/y)
def nu_simple(y):    return 0.5 + np.sqrt(0.25 + 1.0/y)
def nu_rar(y):       return 1.0/(-np.expm1(-np.sqrt(y)))
def nu_mcgaugh_exp(y_grid):
    x = np.geomspace(1e-6, 1e6, 200000)
    mu = -np.expm1(-x)                        # mu = 1 - e^-x (stable)
    return np.exp(np.interp(np.log(y_grid), np.log(x*mu), np.log(1.0/mu)))

# ================================================================== RUN
print("="*78)
print("LANE X: extremal kernel principle -- LP supremum of r  (T_GH = 1 WLOG)")
print("="*78)
T = 1.0

# --- 1. LP sup vs grid floor: the refinement that DOES NOT stabilise --------
print("\n[1] direct LP sup r vs grid floor smin (span to 1e4, ~60 pts/decade):")
SCAN = [(1e-4, 480), (1e-6, 600), (1e-8, 720), (1e-10, 840)]
sups = []
for smin, N in SCAN:
    s = make_grid(smin, 1e4, N)
    supr, _ = solve_direct(s, T)
    sups.append(supr)
    print("    smin = %.0e  N = %4d   sup r = %12.3f" % (smin, N, supr))
sups = np.array(sups)
smins = np.array([g[0] for g in SCAN])
slope = np.polyfit(np.log10(smins), np.log10(sups - 1.0), 1)[0]
print("    log-log slope d log(sup r - 1)/d log(smin) = %.4f  (cascade theory: -1/2)"
      % slope)
print("    2x-density/10x-span refinement DOES NOT stabilise -- honestly: it")
print("    CANNOT, the class supremum is +infinity (demonstrated below).")

# --- 2. base grid of the task spec: certificate + bisection ------------------
print("\n[2] base grid [1e-7, 1e4], N = 480 (task spec):")
s_b = make_grid(1e-7, 1e4, 480)
sup_b, psi_b = solve_direct(s_b, T)
print("    direct LP sup r = %.3f" % sup_b)
lo, hi = bisect_sup(s_b, T, 2.0, 1.2*sup_b, rtol=1e-4)
sup_bis = 0.5*(lo + hi)
print("    bisection-on-r with LP feasibility: sup r in [%.3f, %.3f]" % (lo, hi))
# certificate: psi_b evaluated on an 8x-denser INDEPENDENT trapezoid grid
# (0.99 scale: between-node quadratic dips of the pw-linear kernel eat the
#  enforced-node margin at 0.999; scaling r-1 down relaxes exactly the
#  binding rows, so 0.99 sup is still 5.7e2 x every table target)
bp_b = np.concatenate(([0.0], s_b)); pvb = np.concatenate(([1.0], psi_b))
r_cert = 1.0 + 0.99*(sup_b - 1.0)
Gmin_b, PsiI_b, a1_b, tail_b = eval_G(bp_b, pvb, r_cert, T, M=8*480*10)
print("    certificate at r = 0.99-scaled sup (%.3f): min scaled A2 = %.3e,"
      % (r_cert, Gmin_b))
print("    A1 slack = %.3e, tail slack = %.3e" % (a1_b, tail_b))
infeas_above = not feasible_at_r(s_b, T, 1.05*sup_b)

# the SAME certified psi* is feasible at every r below (bracket-sign lemma);
# verify per-target directly, no lemma assumed:
targ_ok = {}
for name, rv in R_TARGETS:
    gmin, _, _, tl = eval_G(bp_b, pvb, rv, T, M=20000)
    targ_ok[name] = (gmin > -1e-12) and (tl > -1e-12)

# cascade structure of the near-extremal LP solution
lev = psi_b[psi_b > 1e-9]
drops = lev[:-1]/np.maximum(lev[1:], 1e-300)
big = drops[drops > 1.05]
print("    structure of psi*: support [%.1e, %.1e], %d significant down-steps,"
      % (s_b[0], s_b[np.sum(psi_b > 1e-9)-1], len(big)))
print("    median step ratio %.3f (cascade mechanism: near-halvings at nested scales)"
      % (np.median(big) if len(big) else np.nan))

# --- 3. explicit cascade family: unboundedness WITHOUT the LP ---------------
print("\n[3] explicit continuous cascade family (h=0.55, alpha=12, NO LP):")
r_cas = {}
for n in (6, 9, 12):
    bp, pv = cascade_psi(n)
    r_cas[n] = r_max_of(bp, pv, T)
    gmin_lo, _, _, tl_lo = eval_G(bp, pv, 0.99*r_cas[n], T)
    gmin_hi, _, _, _     = eval_G(bp, pv, 1.01*r_cas[n], T)
    print("    n = %2d:  r_max = %8.2f   (0.99 r: min G = %+.2e OK; 1.01 r: %+.2e violates)"
          % (n, r_cas[n], gmin_lo, gmin_hi))
    r_cas[(n, "lo")] = (gmin_lo > -1e-12) and (tl_lo > -1e-12)
    r_cas[(n, "hi")] = gmin_hi < 0

# --- 4. scale WLOG control ---------------------------------------------------
sT2 = make_grid(2e-7, 2e4, 480)
sup_T2, _ = solve_direct(sT2, 2.0)

# --- 5. comparison table -----------------------------------------------------
print("\n[4] COMPARISON TABLE -- sup r = +infinity (no finite supremum exists):")
print("    %-32s %10s   %s" % ("target", "r", "verdict"))
for name, rv in R_TARGETS:
    print("    %-32s %10.4f   REACHABLE (certified: min G >= 0 at this r)"
          % (name, rv))
print("    -> admissibility EXCLUDES NOTHING and DERIVES NOTHING:")
print("       a0 = 2 cH_L / r is unconstrained on BOTH footings")
print("       (canonical cH_L = %.4e; ALT scale x1.2082)." % CHL)

print("\n[5] HEADLINE (a): sup r >= %.0f certified on the base grid alone" % sup_b)
print("    (and grows without bound, slope %.2f in smin) -- kappa = 1/2" % slope)
print("    (r = 11.578) IS reachable after all; the seven-shape bound 9.0168")
print("    was a SHAPE ARTEFACT (single-scale kernels only).")
print("    BOTH halves of the unpriced observation die together:")
print("    - no exclusion of kappa = 1/2 canonical (the 28%-over-bound is void);")
print("    - NO derivation of the empirical a0 = 1.20e-10 either: with no finite")
print("      supremum, '2 cH_L / 9.0167 = 1.2021e-10 (0.17% from McGaugh)' has")
print("      no principle attached. It was a property of 7 hand-picked shapes.")
print("    Any revival needs an EXTRA, currently unjustified, single-scale or")
print("    unimodality axiom -- and would then need pricing against chance")
print("    (this project's own baseline: chance hit 10/19 targets).")

# --- 6. the framework-relevant admissible kernel at r = 2Z -------------------
print("\n[6] admissible kernel AT the framework's r = 2Z = 11.5776 (maximin slack):")
psi_2Z, t_marg = maximin_at_r(s_b, T, R_2Z)
bp2 = np.concatenate(([0.0], s_b)); pv2 = np.concatenate(([1.0], psi_2Z))
gmin_2Z, _, _, tail_2Z = eval_G(bp2, pv2, R_2Z, T, M=40000)
x_k, mu_k = mu_from_psi(s_b, psi_2Z, R_2Z, T)
y_k, nu_k = x_k*mu_k, 1.0/mu_k
m = (y_k > 1e-2) & (y_k < 1e2)
dex = {
  "Milgrom99 sqrt(1+1/y)": np.max(np.abs(np.log10(nu_k[m]) - np.log10(nu_milgrom99(y_k[m])))),
  "simple mu=x/(1+x)":     np.max(np.abs(np.log10(nu_k[m]) - np.log10(nu_simple(y_k[m])))),
  "McGaugh08 exponential": np.max(np.abs(np.log10(nu_k[m]) - np.log10(nu_mcgaugh_exp(y_k[m])))),
  "RAR 1/(1-e^-sqrt(y))":  np.max(np.abs(np.log10(nu_k[m]) - np.log10(nu_rar(y_k[m])))),
}
print("    certificate at r = 2Z: min scaled G = %.3e, tail slack = %.3e, margin t = %.2e"
      % (gmin_2Z, tail_2Z, t_marg))
print("    STRUCTURE (honest): this kernel drops psi 1 -> %.2f BELOW the grid"
      % psi_2Z[0])
print("    floor s = 1e-7, then holds mu ~ %.1e FLAT through the resolved range"
      % mu_k[0])
print("    (a boosted-Newton shelf); true deep-MOND mu ~ x only below x ~ %.0e."
      % x_k[0])
print("    nu(y) vs known kernels, max |dex| over y in [1e-2, 1e2]:")
for k, v in sorted(dex.items(), key=lambda kv: kv[1]):
    print("      %-24s %8.4f dex" % (k, v))
best = min(dex, key=dex.get)
print("    nearest: %s at %.4f dex -> %s" % (best, dex[best],
      "COINCIDES" if dex[best] < 0.01 else
      "close but NOT a known kernel" if dex[best] < 0.05 else
      "DISTINCT from every known kernel (a contrived multi-scale object)"))
# deep-MOND slope of nu(y): d log nu/d log y -> -1/2. The maximin solution
# parks its 1 -> 0.27 drop below the grid floor, so the floor region is the
# flat shelf; the CONTINUOUS kernel (psi(0)=1, linear on [0, s_1]) recovers
# mu ~ x below it. Evaluate there analytically (exact for pw-linear psi):
s_e  = np.geomspace(1e-12, 1e-10, 40)
psi_e = 1.0 + (psi_2Z[0] - 1.0)*s_e/s_b[0]
Psi_e = s_e - (1.0 - psi_2Z[0])*s_e**2/(2.0*s_b[0])
F_e   = s_e + (R_2Z - 1.0)*Psi_e
mu_e  = F_e/np.sqrt(s_e*(s_e + 2*T))
x_e   = 0.5*R_2Z*np.sqrt(s_e*(s_e + 2*T))/T
dslope = np.polyfit(np.log10(x_e*mu_e), np.log10(1.0/mu_e), 1)[0]
mu_over_x_deep = mu_e[0]/x_e[0]

# --- 7. attainment -----------------------------------------------------------
print("\n[7] ATTAINMENT: the supremum is +infinity and is NOT attained by any")
print("    admissible psi. Correct limit statement: for every R there exists a")
print("    CONTINUOUS admissible psi (e.g. the n-level cascade, n ~ log R /")
print("    log(1/h)) with r_max(psi) > R; r_max(cascade): %.1f -> %.1f -> %.1f"
      % (r_cas[6], r_cas[9], r_cas[12]))
print("    for n = 6 -> 9 -> 12. No extremal psi* exists; the 'principle'")
print("    reduces to a limit statement and therefore selects nothing.")

# ================================================================== CHECKS
print("\n" + "="*78)
check("LP machinery: r = 2 (Milgrom 1999 eq 10) feasible on base grid",
      feasible_at_r(s_b, T, 2.0))
check("LP sup grows >= 2x per 100x smin (a true finite bound would cap it)",
      (sups[1] > 2*sups[0]) and (sups[2] > 2*sups[1]) and (sups[3] > 2*sups[2]),
      "sups: " + ", ".join("%.0f" % v for v in sups))
check("scaling law: log-log slope in [-0.65, -0.35] (cascade theory -1/2)",
      -0.65 < slope < -0.35, "slope = %.4f" % slope)
check("base grid: sup r exceeds ALL six targets incl. 2Z and 4pi",
      sup_b > max(rv for _, rv in R_TARGETS), "sup = %.1f" % sup_b)
check("bisection agrees with direct LP on base grid to < 1%",
      abs(sup_bis - sup_b)/sup_b < 0.01,
      "bisect %.3f vs direct %.3f" % (sup_bis, sup_b))
check("certificate: LP psi* passes A1+A2 on independent 8x-dense grid (0.99 r)",
      (Gmin_b > -1e-8) and (tail_b > -1e-12),
      "min scaled G = %.2e" % Gmin_b)
check("base-grid LP infeasible at 1.05 x its own sup (bisection route)",
      infeas_above)
check("the certified psi* is feasible at EVERY table target r",
      all(targ_ok.values()),
      "; ".join("%s:%s" % (k.split()[0], "ok" if v else "VIOLATED")
                for k, v in targ_ok.items()))
check("cascade growth: r_max(9) > 4 r_max(6) and r_max(12) > 4 r_max(9)",
      (r_cas[9] > 4*r_cas[6]) and (r_cas[12] > 4*r_cas[9]),
      "%.1f, %.1f, %.1f" % (r_cas[6], r_cas[9], r_cas[12]))
check("hand-built n=6 cascade alone already beats BOTH 2Z and 4pi (no LP)",
      r_cas[6] > 4*np.pi, "r_max = %.2f" % r_cas[6])
check("cascade r_max cross-validated: feasible at 0.99 r_max, violated at 1.01",
      all(r_cas[(n, "lo")] and r_cas[(n, "hi")] for n in (6, 9, 12)))
check("scale WLOG: T_GH = 2 run reproduces T_GH = 1 sup to < 1% (same N)",
      abs(sup_T2 - sup_b)/sup_b < 0.01, "%.3f vs %.3f" % (sup_T2, sup_b))
check("psi(2Z) admissible shape: psi <= 1, monotone decreasing, >= 0",
      (psi_2Z[0] <= 1 + 1e-9) and np.all(np.diff(psi_2Z) <= 1e-9)
      and np.all(psi_2Z >= -1e-12))
check("mu from psi(2Z) is a sane MOND kernel: mu <= 1 and monotone",
      (mu_k.max() <= 1 + 1e-6) and np.all(np.diff(mu_k) >= -1e-7),
      "max mu = %.6f" % mu_k.max())
check("deep-MOND limit of psi(2Z) kernel below the shelf: slope -1/2, mu/x -> 1",
      (abs(dslope + 0.5) < 0.02) and (abs(mu_over_x_deep - 1.0) < 0.05),
      "slope = %.4f, mu/x = %.4f at x = %.1e" % (dslope, mu_over_x_deep, x_e[0]))
u = 1e-8
s_small = u*u/(np.sqrt(1.0 + u*u) + 1.0)
check("float hazard: stable s(a) map satisfies s(s+2) = u^2 at u = 1e-8",
      abs(s_small*(s_small + 2.0)/u**2 - 1.0) < 1e-10)
check("table arithmetic: 2 cH_L / 1.20e-10 reproduces 9.0323 to 4 sf",
      abs(2*CHL/A0_EMP - 9.0323) < 5e-4, "%.4f" % (2*CHL/A0_EMP))

n_ok = sum(checks)
print("\n%d/%d checks held." % (n_ok, len(checks)))
if n_ok != len(checks):
    sys.exit(1)
print("VERDICT: sup r = +INFINITY over the stated class -- the seven-shape 9.0168")
print("was a single-scale shape artefact. kappa = 1/2 NOT excluded; empirical a0")
print("NOT derived. kappa = 1/2 remains fitted, on both footings.")
