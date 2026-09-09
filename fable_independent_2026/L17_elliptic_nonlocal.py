#!/usr/bin/env python3
"""
L17 -- the A5 lane: can a SPATIALLY NONLOCAL ELLIPTIC operator build MOND?
==========================================================================
`CRISPY_FRIED_CHICKEN_RECIPE.md` section 3 lists five "acceptable proteins".  Four have been used to
build candidates.  A5 has not:

    A5 -- Spatially nonlocal elliptic operators: (-D^2)^{-1}, f(-D^2/a0^2) -- elliptic, no temporal
    mode, controlled GR limit.  NOTE: changes momentum scaling, NEVER perturbative amplitude order.

and warning P6 says temporal nonlocality is closed while "spatial elliptic nonlocality is admissible
research".  So A5 is the one untried protein, and its attraction is real: an elliptic operator adds no
temporal mode by construction, which is the only obvious way to get MOND phenomenology without buying
the scalar that every local single-metric route buys (I3a wants exactly two tensor polarisations).

This lane builds the construction A5 licenses, runs it against the frozen ingredients I1-I5 and the four
gates (DOF, MOND limit, Newtonian limit, Solar-System screening), and then tests A5's own caveat -- the
amplitude clause -- which is the most likely way the class dies.

THE CONSTRUCTION.  The programme already has a filtered action of exactly this type, PAPER4's

    I = int dt d3x { L_m - rho Phi - [ 2 grad(Phi).grad(u) - |grad u|^2 - a0^2 q(|grad(S u)|^2/a0^2) ]/(8 pi G) }

with S = exp(xi^2 Delta/2) a Gaussian (or Helmholtz (1 - xi^2 Delta)^{-1}) filter, q'(s^2) = nu(s) - 1,
nu the exact inverse partner of mu(y) = 1 - e^{-y}.  Its field equations are

    Delta u = 4 pi G rho,        Delta Phi = 4 pi G rho + S grad.[ (nu - 1) grad(S u) ],

elliptic in space, second order in time (in fact zeroth), no new temporal mode.  PAPER4 sets the filter
length xi from the SOLAR SYSTEM (xi >= 0.02-0.03 pc).  A5 licenses a different thing: the filter scale
set by a0, f(-D^2/a0^2).  That version has never been built.  It is what this lane builds, in the two
placements a filter can occupy:

  (A5-L)  the filter acts ALONE, i.e. the MOND function is dropped and the whole modification is the
          nonlocal elliptic kinetic operator:   div[ F grad Phi ] = -4 pi G rho,  F = f(-l^2 Delta).
          This is the only placement in which the elliptic operator is what PRODUCES the modification;
          it is A5 used as a protein.
  (A5-F)  the filter sits INSIDE the nonlinear MOND function, PAPER4's placement, with xi -> l0 = c^2/a0.
          Here the nonlinearity produces MOND and the filter only modifies it; A5 used as a seasoning.

THE GATES, each a check that can fail:
  L  the length gate      -- what length does A5 actually have, and is it the length MOND needs?
  M  the MOND gate        -- does the static weak field give mu(y) = 1 - e^{-y} with a0 (I1, G1)?
  N  the Newtonian gate   -- measured G at y >> 1 with exponentially small corrections (I5, G2)
  F  the filtered gate    -- A5-F: does an a0-scaled filter leave MOND intact?
  D  the DOF gate         -- Hamiltonian count, no canonical data beyond the two tensors (I3a, G4, P4)
  S  the screening gate   -- controlled by a LOCAL acceleration, not a scale or a label (I4)
  O  A5's own caveat      -- "changes momentum scaling, NEVER perturbative amplitude order" (G0)

CONTROLS, C0-C6.  Seven checks guard my own algebra before any of it is used against A5: the kernel
inversion against its own deep-MOND series; a dimensional solver that must reproduce the Planck length;
the oscillatory integral behind the log potential against its exact closed form; the mass-scaling
estimator run on the exact exponential-kernel AQUAL point mass, where it must return 1/2 and 1; the
Gaussian filter at PAPER4's own xi, where it must be inert on galactic scales, and its interior limit;
and (C6) six textbook Dirac counts at once -- free scalar 1, scalar-plus-multiplier 0, Maxwell 2,
Proca 3, linearised GR 2, massive Fierz-Pauli 5.  A CONTROL failure invalidates the run and exits 3;
a GATE failure is the finding.

Both footings a0 = 9.3619e-11 (canonical) and 1.1279e-10 m s^-2 (alternate) throughout.
"""
import numpy as np, math, sys
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import quad

FAILS, CFAILS = [], []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)
        if name.startswith("C"): CFAILS.append(name)

# ---------------------------------------------------------------- constants, both footings
G    = 6.674e-11
c    = 2.99792458e8
MSUN = 1.989e30
pc   = 3.0857e16
kpc  = 3.0857e19
Mpc  = 3.0857e22
Gpc  = 3.0857e25
AU   = 1.495978707e11
HBAR = 1.054571817e-34
A0   = {"canonical": 9.3619e-11, "alternate": 1.1279e-10}

print("=" * 118)
print("L17 -- the A5 lane: can a spatially nonlocal ELLIPTIC operator build MOND?")
print("=" * 118, flush=True)

# ================================================================ 0. the frozen kernel
def mu_exp(y):      return -np.expm1(-np.asarray(y, float))  # 1 - e^-y, accurate for tiny y
def s_of_y(y):      return y*mu_exp(y)                       # s = y mu(y) = |grad u|/a0
def y_of_s(s):
    """invert s = y(1 - e^{-y});  y = g/a0 given the Newtonian s = g_N/a0."""
    s = float(s)
    if s <= 0: return 0.0
    if s < 1e-3:                                   # tight bracket: the deep branch is y ~ sqrt(s)
        lo, hi = 0.5*math.sqrt(s), 2.0*math.sqrt(s) + 4.0*s
    else:
        lo, hi = 1e-30, max(4.0, 2.0*s + 4.0)
    while s_of_y(hi) < s: hi *= 2.0
    return brentq(lambda y: s_of_y(y) - s, lo, hi, xtol=1e-300, rtol=1e-15, maxiter=400)

print("\n0. THE FROZEN KERNEL (I1), used unchanged everywhere below")
print(f"    mu(y) = 1 - e^-y ;  s = y mu(y) ;  nu(s) = y/s ;  deep limit y = sqrt(s)(1 + sqrt(s)/4 + ...)")
_dev = []
for _s in (1e-12, 1e-16, 1e-20):
    _y = y_of_s(_s)
    _dev.append(abs(_y/math.sqrt(_s) - 1 - math.sqrt(_s)/4))
    print(f"    s = {_s:.0e}:  y/sqrt(s) - 1 = {_y/math.sqrt(_s) - 1:+.4e}   (series: sqrt(s)/4 = {math.sqrt(_s)/4:+.4e})")
check("C0 [control] the kernel inversion follows its own deep-MOND series y = sqrt(s)(1 + sqrt(s)/4) to 1e-7",
      max(_dev) < 1e-7, f"worst departure from the series {max(_dev):.2e}")

# ================================================================ 1. the construction, written out
print("\n1. THE CONSTRUCTION A5 LICENSES")
print("""    Two placements of one filter F = f(-l^2 Delta), l the filter length:

      (A5-L)  div[ F grad Phi ] = -4 pi G rho          <=>   sigma(k) Phi_k = -4 pi G rho_k,  sigma = k^2 f(l k)
              from  I = int { L_m - rho Phi - (1/8 pi G) grad(Phi).F grad(Phi) }.
              Best case, chosen to be as MOND-like as a linear operator can be:
                  f(x) = x/(1+x)   =>   sigma(k) = l k^3/(1 + l k),
              which is  k^2 (Newton) at l k >> 1 and l k^3 (a logarithmic potential, flat rotation
              curve) at l k << 1.  sigma > 0 for every k > 0: uniformly elliptic away from k = 0.

      (A5-F)  PAPER4's filtered action with xi -> l:
              Delta u = 4 pi G rho,   Delta Phi = 4 pi G rho + S grad.[(nu - 1) grad(S u)],  S = e^{l^2 Delta/2}.

    A5's own dimensional instruction, f(-D^2/a0^2), fixes l: the argument must be dimensionless, so the
    operator's length is the unique length built from a0 and c.  Section 2 solves for it.""")

# ================================================================ 2. L -- the length gate
print("\n2. L -- THE LENGTH GATE: what length does A5 have, and is it the length MOND needs?")

def dim_solve(target, basis):
    """exponents alpha with prod(basis_i^alpha_i) having dimensions `target`; dims are (L,M,T) triples."""
    Aa = np.array([[b[j] for b in basis] for j in range(3)], float)
    tt = np.array(target, float)
    sol, res, rank, sv = np.linalg.lstsq(Aa, tt, rcond=None)
    ok = np.allclose(Aa@sol, tt, atol=1e-9)
    ns = Aa.shape[1] - rank                    # dimension of the null space = family size
    return sol, ok, ns

DIM = {"a0": (1, 0, -2), "c": (1, 0, -1), "G": (3, -1, -2), "hbar": (2, 1, -1)}
LEN = (1, 0, 0)
sol_p, ok_p, ns_p = dim_solve(LEN, [DIM["G"], DIM["hbar"], DIM["c"]])
l_planck = G**sol_p[0] * HBAR**sol_p[1] * c**sol_p[2]
check("C1 [control] the dimensional solver returns the Planck length from {G, hbar, c} to 1e-9",
      ok_p and abs(l_planck/1.616255e-35 - 1) < 1e-3,
      f"exponents ({sol_p[0]:+.3f},{sol_p[1]:+.3f},{sol_p[2]:+.3f}) -> {l_planck:.4e} m")

sol_a, ok_a, ns_a = dim_solve(LEN, [DIM["a0"], DIM["c"], DIM["G"]])
print(f"    a0^alpha c^beta G^gamma = a length  =>  (alpha,beta,gamma) = "
      f"({sol_a[0]:+.4f},{sol_a[1]:+.4f},{sol_a[2]:+.4f}); null space dimension {ns_a}")
check("L1 the length A5's operator must use is UNIQUE (no free family), i.e. f(-D^2/a0^2) has one scale",
      ok_a and ns_a == 0 and abs(sol_a[0] + 1) < 1e-9 and abs(sol_a[1] - 2) < 1e-9 and abs(sol_a[2]) < 1e-9,
      "it is l0 = c^2/a0; G cannot enter without a mass, so no other length exists")

L0 = {f: c*c/A0[f] for f in A0}
for f in A0:
    print(f"    {f:>9}: a0 = {A0[f]:.4e} m/s^2  ->  l0 = c^2/a0 = {L0[f]:.4e} m = {L0[f]/Gpc:.2f} Gpc"
          f"  (Hubble radius c/H0 = {c/(67.4e3/Mpc)/Gpc:.2f} Gpc)")

print("\n    the length MOND actually needs around a mass M is the MOND radius r_M = sqrt(GM/a0):")
MASSES = [1e8, 1e9, 1e10, 1e11, 1e12]
rat = {}
for f in A0:
    row = []
    for Mg in MASSES:
        M = Mg*MSUN
        rM = math.sqrt(G*M/A0[f]); vf = (G*M*A0[f])**0.25
        row.append((Mg, rM, vf, L0[f]/rM, (c/vf)**2))
    rat[f] = row
    print(f"    {f}:")
    for Mg, rM, vf, q, cv in row:
        print(f"        M = {Mg:.0e} Msun:  r_M = {rM/kpc:8.2f} kpc,  v_flat = {vf/1e3:6.1f} km/s,"
              f"  l0/r_M = {q:.3e}   [(c/v_flat)^2 = {cv:.3e}]")
qmin = min(min(r[3] for r in rat[f]) for f in rat)
check("L2 A5's length is the length MOND needs (within a factor 10 of r_M for any real galaxy)",
      qmin < 10, f"smallest l0/r_M over 1e8-1e12 Msun and both footings is {qmin:.3e}; "
                 f"l0/r_M = c^2/sqrt(GMa0) = (c/v_flat)^2 exactly, so the mismatch IS the ratio of the "
                 f"speed of light to a rotation speed, squared")
spread = max(math.sqrt(MASSES[-1]/MASSES[0]) for f in rat)
check("L3 a SINGLE fixed filter length can serve the observed galaxy mass range",
      spread < 3, f"the length a linear filter must have to match mass M is proportional to r_M ~ M^1/2, "
                  f"so over 1e8-1e12 Msun the required length spans a factor {spread:.0f}; one operator "
                  f"cannot have {spread:.0f} lengths")

print("\n    A filter could instead take its length from a LOCAL quantity, which is what I4 asks of a")
print("    screening trigger.  Every local length available, at the solar circle (r = 8.2 kpc,")
print("    g = 2.15e-10 m/s^2, |Phi| ~ v^2 = 5.4e10 m^2/s^2, M_b = 6e10 Msun).  A length is only useful")
print("    if it (a) is I4-legal, (b) CARRIES a0 -- otherwise it sets no transition -- and (c) equals r_M:")
r_sun = 8.2*kpc; g_sun = 2.15e-10; Phi_sun = (233e3)**2; Mb_MW = 6e10*MSUN
CAND = []
for f in A0:
    rM_MW = math.sqrt(G*Mb_MW/A0[f])
    lengths = [("c^2/a0     the A5 operator itself", L0[f],          False, True),
               ("c^2/g      Rindler, acceleration", c*c/g_sun,       True,  False),
               ("g/|grad g| scale-free derivative", r_sun,           True,  False),
               ("|Phi|/a0   the potential        ", Phi_sun/A0[f],   False, True)]
    print(f"      {f}: r_M(MW) = {rM_MW/kpc:.2f} kpc")
    for nm, LL, legal, hasa0 in lengths:
        print(f"        {nm} = {LL/kpc:12.4g} kpc = {LL/rM_MW:10.3e} r_M   "
              f"I4-legal: {'yes' if legal else 'NO ':<3}   carries a0: {'yes' if hasa0 else 'NO'}")
        CAND.append((nm, legal, hasa0, LL/rM_MW))
good = [x for x in CAND if x[1] and x[2] and 0.5 < x[3] < 2.0]
check("L4 some length that is I4-legal AND carries a0 AND equals r_M exists",
      len(good) > 0,
      "no candidate satisfies all three. c^2/a0 carries a0 but is not local and overshoots by (c/v)^2; "
      "c^2/g is local and legal but a0-free, so it sets no transition, and it overshoots by the same "
      "(c/v)^2; g/|grad g| is legal but is just the local radius, a0-free and therefore scale-free; "
      "|Phi|/a0 hits r_M EXACTLY (v^2 = GM/r_M makes |Phi|/a0 = r_M identically) and is the only one "
      "that does -- and it is the potential, which I4 forbids by name and which is not a local invariant")

# ================================================================ 3. M -- the MOND gate on A5-L
print("\n3. M -- THE MOND GATE on A5-L (the elliptic operator used as the protein)")
print("""    sigma(k) = l k^3/(1 + l k) splits exactly: Phi_k = -4 pi G M [ 1/k^2 + 1/(l k^3) ], so the
    point-mass solution is EXACT and elementary,
        Phi(r) = -GM/r + (2GM/(pi l)) ln r + const,      g(r) = GM/r^2 + 2GM/(pi l r).
    The 1/r piece is what A5 buys: the momentum scaling IS changed, exactly as the recipe says.""")

def g_A5L(r, M, l):  return G*M/r**2 + 2*G*M/(math.pi*l*r)

# control: the oscillatory integral behind the log term, int_0^inf [cos u/u - sin u/u^2] du = -1
def _osc(u):
    if u < 1e-3: return -u/3.0 + u**3/30.0            # series, avoids 0/0
    return math.cos(u)/u - math.sin(u)/u**2
U_CUT = 400.0
I_osc = quad(_osc, 0.0, U_CUT, limit=4000)[0] - math.sin(U_CUT)/U_CUT   # tail = [sin u/u] from U to inf
check("C2 [control] the inverse transform behind the log term integrates to its closed form (-1)",
      abs(I_osc + 1) < 1e-8,
      f"quadrature to u = {U_CUT:.0f} plus the analytic tail gives {I_osc:.12f} vs exact -1; this integral "
      f"is the entire content of g_asym = 2GM/(pi l r)")

# control: the mass-scaling estimator on the exact exponential-kernel AQUAL point mass
def g_MOND(r, M, a0): return a0*y_of_s(G*M/r**2/a0)
def slope_M(gfun, r, a0, m1=1e10, m2=1e11):
    g1 = gfun(r, m1*MSUN, a0); g2 = gfun(r, m2*MSUN, a0)
    return math.log(g2/g1)/math.log(m2/m1)
for f in A0:
    p_mond_deep = slope_M(g_MOND, 300*kpc, A0[f])
    p_mond_newt = slope_M(g_MOND, 0.01*kpc, A0[f])
    print(f"    {f}: exponential-kernel AQUAL point mass, d ln g/d ln M = {p_mond_deep:.4f} at 300 kpc "
          f"(deep MOND) and {p_mond_newt:.4f} at 10 pc (Newtonian)")
p_ok = all(abs(slope_M(g_MOND, 300*kpc, A0[f]) - 0.5) < 0.02 and
           abs(slope_M(g_MOND, 0.01*kpc, A0[f]) - 1.0) < 1e-6 for f in A0)
check("C3 [control] the mass-scaling estimator returns 1/2 on the frozen kernel's own deep-MOND limit",
      p_ok, "0.5 asymptotically, 1.0 in the Newtonian regime, both footings")

print("\n    A5-L's own mass scaling and amplitude (both footings, at r = 20 kpc and asymptotically):")
p_lin = {}
for f in A0:
    l = L0[f]
    p = math.log(g_A5L(300*kpc, 1e11*MSUN, l)/g_A5L(300*kpc, 1e10*MSUN, l))/math.log(10.0)
    p_lin[f] = p
    M = 1e11*MSUN; r = 20*kpc
    gl = 2*G*M/(math.pi*l*r); gm = math.sqrt(G*M*A0[f])/r
    vf = (G*M*A0[f])**0.25
    print(f"    {f}: d ln g/d ln M = {p:.6f}  (MOND needs 0.5);  asymptotic g_A5L/g_MOND = "
          f"{gl/gm:.4e}  [predicted (2/pi)(v_f/c)^2 = {(2/math.pi)*(vf/c)**2:.4e}]")
check("M1 A5-L reproduces the MOND mass scaling g ~ M^(1/2) (equivalently the BTFR)",
      all(abs(p_lin[f] - 0.5) < 0.05 for f in p_lin),
      f"it returns exactly {p_lin['canonical']:.4f}. A filter is a LINEAR operator, so the field equation "
      f"obeys superposition and g is exactly proportional to M for every f, every l and every symbol. "
      f"This is independent of the length and kills the linear placement of A5 outright")

amp = {}
for f in A0:
    M = 1e11*MSUN; r = 20*kpc; l = L0[f]
    amp[f] = (2*G*M/(math.pi*l*r))/(math.sqrt(G*M*A0[f])/r)
check("M2 A5-L's asymptotic amplitude matches sqrt(GMa0)/r within a factor 2",
      all(0.5 < amp[f] < 2.0 for f in amp),
      f"it is short by {1/amp['canonical']:.3e} (canonical) and {1/amp['alternate']:.3e} (alternate); the "
      f"deficit is exactly (2/pi)(v_flat/c)^2 and is r-INDEPENDENT, so no radius rescues it")

for f in A0:
    l = L0[f]; M = 1e11*MSUN
    r_t = math.pi*l/2                                    # GM/r^2 = 2GM/(pi l r)
    rM = math.sqrt(G*M/A0[f])
    print(f"    {f}: A5-L transition radius (where the two terms balance) = {r_t/Gpc:.2f} Gpc; "
          f"r_M = {rM/kpc:.2f} kpc; ratio {r_t/rM:.3e}")
check("M3 A5-L's transition happens at the MOND radius (within a factor 10)",
      all((math.pi*L0[f]/2)/math.sqrt(G*1e11*MSUN/A0[f]) < 10 for f in A0),
      "it happens at pi l0/2 ~ 49 Gpc, past the observable universe; the model is Newtonian everywhere "
      "a measurement exists")

print("\n    I1 test -- is the effective mu a function of the ACCELERATION?")
for f in A0:
    l = L0[f]; r = 20*kpc
    print(f"    {f}: at r = 20 kpc,")
    for Mg in (1e9, 1e11):
        M = Mg*MSUN
        gN = G*M/r**2
        mu_eff = gN/g_A5L(r, M, l)
        y_req = y_of_s(gN/A0[f]); mu_req = mu_exp(y_req)
        print(f"        M = {Mg:.0e} Msun: y = g/a0 = {y_req:8.4f};  I1 requires mu = {mu_req:.6f};"
              f"  A5-L gives mu_eff = {mu_eff:.9f}")
mu_lo = {f: (G*1e9*MSUN/(20*kpc)**2)/g_A5L(20*kpc, 1e9*MSUN, L0[f]) for f in A0}
mu_hi = {f: (G*1e11*MSUN/(20*kpc)**2)/g_A5L(20*kpc, 1e11*MSUN, L0[f]) for f in A0}
mreq_lo = {f: mu_exp(y_of_s(G*1e9*MSUN/(20*kpc)**2/A0[f])) for f in A0}
mreq_hi = {f: mu_exp(y_of_s(G*1e11*MSUN/(20*kpc)**2/A0[f])) for f in A0}
check("M4 [I1] A5-L's effective mu is a function of y = g/a0, as the frozen kernel requires",
      all(abs(mu_lo[f]/mu_hi[f] - mreq_lo[f]/mreq_hi[f]) < 0.1 for f in A0),
      f"mu_eff = 1/(1 + 2r/(pi l)) depends on r ALONE and is identical ({mu_lo['canonical']:.12f} vs "
      f"{mu_hi['canonical']:.12f}) for two masses whose required mu differ by "
      f"{mreq_hi['canonical']/mreq_lo['canonical']:.1f}x. A linear operator cannot see an amplitude, so "
      f"no f produces any mu(y), let alone 1 - e^-y")

print("\n    generality over the SYMBOL, not just this f.  For any pure power sigma(k) = l^(a-2) k^a the")
print("    point-mass solution is Phi ~ r^(a-3) (log at a = 3), so g ~ r^(a-4):")
for a in (1, 2, 3, 4):
    tag = {1: "(-D^2)^-1-type insertion", 2: "Newton", 3: "flat rotation curve",
           4: "constant force -- the alpha=1 sunward anomaly"}[a]
    print(f"        a = {a}:  g ~ r^{a-4:+d}   d ln g/d ln M = 1   {tag}")
rng = np.random.default_rng(20260908)
Ngr = 200
Lap = np.diag(2.0*np.ones(Ngr)) + np.diag(-np.ones(Ngr-1), 1) + np.diag(-np.ones(Ngr-1), -1)
Ker = rng.normal(size=(Ngr, Ngr)); Ker = 0.5*(Ker + Ker.T)                 # arbitrary NONLOCAL kernel
src = rng.normal(size=Ngr)
with np.errstate(all="ignore"):        # stale LAPACK IEEE flags again; results are checked below
    Op = Lap + Ker @ Ker.T / Ngr
    x1 = np.linalg.solve(Op, src); x2 = np.linalg.solve(Op, 100.0*src)
assert np.isfinite(x1).all() and np.isfinite(x2).all()
lin_err = float(np.max(np.abs(x2/x1 - 100.0)))
print(f"    numerical test of the same statement on an ARBITRARY nonlocal positive-definite operator "
      f"(200x200,\n    dense kernel, not a differential operator): source x100 gives field x"
      f"{100.0 + lin_err:.10f}, error {lin_err:.2e}")
check("M5 some elliptic symbol gives BOTH the flat-rotation force law AND a mass scaling other than 1",
      lin_err > 1e-6,
      f"a = 3 is the unique exponent with g ~ 1/r (verified exactly by C2 at a = 3 and by Newton at a = 2), "
      f"and EVERY nonlocal positive-definite operator has d ln g/d ln M = 1 to {lin_err:.0e} because the "
      f"equation is linear in rho. The symbol has one free function and it buys the radial slope only; "
      f"the mass slope is not for sale at any price")

# ================================================================ 4. N -- the Newtonian gate
print("\n4. N -- THE NEWTONIAN GATE (I5, G2): recovery with the MEASURED G")
for f in A0:
    l = L0[f]
    for rr, nm in ((AU, "1 AU"), (30e3*AU, "30 kAU"), (kpc, "1 kpc")):
        dev = 2*rr/(math.pi*l)
        print(f"    {f}: at {nm:>7}, g_A5L/g_Newton - 1 = {dev:.3e}")
dev_worst = max(2*kpc/(math.pi*L0[f]) for f in A0)
check("N1 [I5] A5-L recovers Newton with the measured G at high acceleration",
      dev_worst < 1e-6, f"largest fractional deviation inside 1 kpc is {dev_worst:.2e}; the bare coupling "
                        f"IS the measured G because the correction is additive and vanishes as r -> 0")
_M = 1e11*MSUN
_r = math.sqrt(G*_M/(20.0*A0['canonical']))            # radius where y = g_N/a0 = 20, deep in Newton
_dev = lambda rr: 2*rr/(math.pi*L0['canonical'])
idx_A5 = math.log(_dev(2*_r)/_dev(_r))/math.log(2.0)
d1 = g_MOND(_r, _M, A0['canonical'])/(G*_M/_r**2) - 1.0
d2 = g_MOND(2*_r, _M, A0['canonical'])/(G*_M/(2*_r)**2) - 1.0
idx_kernel = math.log(d2/d1)/math.log(2.0)
print(f"    at r = {_r/kpc:.2f} kpc (y = 20) and 2r, fractional correction:  A5-L {_dev(_r):.3e} -> "
      f"{_dev(2*_r):.3e},  frozen kernel {d1:.3e} -> {d2:.3e}")
print(f"    local index d ln(g/g_N - 1)/d ln r:  A5-L {idx_A5:+.4f} (pure power law),  "
      f"frozen kernel {idx_kernel:+.2f} (exponential: e^-y with y ~ r^-2)")
check("N2 [I5] the correction is exponentially small in the Newtonian regime, with no singular 1/y",
      idx_A5 > 5.0,
      f"the A5-L correction is a POWER law, g_extra/g_N = 2r/(pi l0), index exactly {idx_A5:+.1f}, while "
      f"the frozen kernel's index at the same radius is {idx_kernel:+.0f} and grows. Harmless at 1e-16, "
      f"but the wrong shape: I5's 'exponentially small' is a property of the kernel, and a linear filter "
      f"has no exponentials to give")

# ================================================================ 5. F -- the filtered gate (A5-F)
print("\n5. F -- THE FILTERED GATE: A5-F, PAPER4's placement with xi -> l0 = c^2/a0")
print("""    Gaussian filter S = e^{xi^2 Delta/2}: for a point mass S u = -GM erf(r/(sqrt2 xi))/r, so
        |grad(S u)|(r) = GM | erf(x)/r^2 - sqrt(2/pi) e^{-x^2}/(xi r) |,  x = r/(sqrt2 xi),
    which tends to GM/r^2 for x >> 1 and to 0.2660 GM r/xi^3 for x << 1 (the smoothed cloud's interior).""")

def grad_Su(r, M, xi):
    x = r/(math.sqrt(2.0)*xi)
    return abs(G*M*(math.erf(x)/r**2 - math.sqrt(2.0/math.pi)*math.exp(-x*x)/(xi*r)))

def grad_Su_helm(r, M, xi):
    """the other filter PAPER4 names, S = (1 - xi^2 Delta)^-1: S u = -GM(1 - e^{-r/xi})/r,
       verified by (1 - xi^2 Delta)[(1-e^{-r/xi})/r] = 1/r; interior limit GM/(2 xi^2)."""
    e = math.exp(-r/xi) if r/xi < 700 else 0.0
    return abs(G*M*(e/(xi*r) - (1.0 - e)/r**2))

# control: PAPER4's own xi must be inert on galactic scales
r_test = 20*kpc; M_test = 1e11*MSUN
inert = grad_Su(r_test, M_test, 0.03*pc)/(G*M_test/r_test**2)
check("C4 [control] at PAPER4's own filter length xi = 0.03 pc the filter is inert at 20 kpc",
      abs(inert - 1) < 1e-6, f"|grad(S u)|/|grad u| = {inert:.12f}")
# control: the small-x interior coefficient
xi_big = 1e6*r_test
coef = grad_Su(r_test, M_test, xi_big)/(G*M_test*r_test/xi_big**3)
coef_h = grad_Su_helm(r_test, M_test, xi_big)/(G*M_test/(2*xi_big**2))
inert_h = grad_Su_helm(r_test, M_test, 0.03*pc)/(G*M_test/r_test**2)
check("C5 [control] both filter shapes reproduce their analytic interior limits and are inert at "
      "PAPER4's xi",
      abs(coef - math.sqrt(2)/(3*math.sqrt(math.pi))) < 1e-3 and abs(coef_h - 1) < 1e-3
      and abs(inert_h - 1) < 1e-6,
      f"Gaussian interior sqrt(2)/(3 sqrt(pi)): {coef:.5f} vs 0.26596; Helmholtz interior GM/(2 xi^2): "
      f"ratio {coef_h:.6f}; Helmholtz at xi = 0.03 pc: {inert_h:.12f}")

print("\n    A5-F with xi = l0, evaluated on a 1e11 Msun galaxy at 20 kpc:")
for f in A0:
    a0 = A0[f]; xi = L0[f]
    s_un = G*M_test/r_test**2/a0
    s_fl = grad_Su(r_test, M_test, xi)/a0
    y_un = y_of_s(s_un); y_fl = y_of_s(s_fl)
    ph_un = (1/mu_exp(y_un) - 1)*s_un*a0          # (nu-1)|grad u|, the phantom amplitude
    ph_fl = (1/mu_exp(y_fl) - 1)*s_fl*a0
    print(f"    {f}: unfiltered s = g_N/a0 = {s_un:.4f} -> y = {y_un:.4f}, phantom = {ph_un:.3e} m/s^2")
    print(f"    {'':>{len(f)}}  filtered   s = {s_fl:.3e} -> y = {y_fl:.3e}, phantom = {ph_fl:.3e} m/s^2"
          f"   (argument suppressed {s_un/s_fl:.2e}x, phantom {ph_un/ph_fl:.2e}x)")
sup, sup_h = {}, {}
for f in A0:
    sup[f] = (G*M_test/r_test**2)/grad_Su(r_test, M_test, L0[f])
    sup_h[f] = (G*M_test/r_test**2)/grad_Su_helm(r_test, M_test, L0[f])
    print(f"    {f}: suppression of |grad(S u)| at 20 kpc -- Gaussian {sup[f]:.2e}x, "
          f"Helmholtz {sup_h[f]:.2e}x (both filter shapes PAPER4 names)")
check("F1 A5-F keeps the MOND argument within a factor 2 of its unfiltered value on galactic scales",
      all(sup[f] < 2 and sup_h[f] < 2 for f in sup),
      f"the a0-scaled filter suppresses |grad(S u)| by {sup['canonical']:.2e} (Gaussian) and "
      f"{sup_h['canonical']:.2e} (Helmholtz) at 20 kpc -- it smooths the galaxy over "
      f"{L0['canonical']/Gpc:.0f} Gpc -- and the deep-MOND phantom by the square root of that. The two "
      f"shapes differ by orders of magnitude and neither is remotely survivable: the MOND effect is not "
      f"modified, it is annihilated")

print("\n    the opposite sign: a SHARPENING elliptic filter S^-1 = 1 - xi^2 Delta.  For an exponential"
      "\n    disc (M_b = 6e10 Msun, R_d = 3 kpc, z_0 = 300 pc) S^-1 u = u - 4 pi G xi^2 rho, so")
Rd = 3*kpc; z0 = 300*pc
rho_disc = (Mb_MW/(4*math.pi*Rd**2*z0))*math.exp(-8.2/3.0)
grad_rho = rho_disc/z0
for f in A0:
    xi = L0[f]
    extra = 4*math.pi*G*xi**2*grad_rho
    print(f"    {f}: rho(R=8.2 kpc) = {rho_disc:.2e} kg/m^3, |grad rho| = {grad_rho:.2e};"
          f"  4 pi G xi^2 |grad rho| = {extra:.3e} m/s^2  =>  y = {extra/A0[f]:.3e}")
check("F2 the sharpening filter at the a0 scale leaves y in the MOND range somewhere in a real disc",
      all(4*math.pi*G*L0[f]**2*grad_rho/A0[f] < 1e3 for f in A0),
      f"y = {4*math.pi*G*L0['canonical']**2*grad_rho/A0['canonical']:.2e} inside the disc, so mu = 1 to "
      f"machine precision and the theory is exactly Newtonian")

print("\n    the pincer: the window of filter lengths that are merely HARMLESS on a galaxy")
xi_hi = 0.5*r_test                       # smoothing must not erase the galaxy
xi_lo = math.sqrt(A0['canonical']/(4*math.pi*G*grad_rho))   # sharpening must not swamp a0
print(f"    smoothing branch needs xi << r_gal ~ {r_test/kpc:.0f} kpc = {xi_hi/pc:.2e} pc")
print(f"    sharpening branch needs xi << sqrt(a0/(4 pi G |grad rho|)) = {xi_lo/pc:.2e} pc")
print(f"    PAPER4's Solar-System-fixed xi = 0.02-0.05 pc sits inside that window; "
      f"l0 = {L0['canonical']/pc:.2e} pc is outside it by {L0['canonical']/min(xi_hi, xi_lo):.2e}")
check("F3 [pincer] SOME monotone filter at the a0 scale has its transition inside 1 Mpc",
      L0["canonical"] < Mpc,
      f"both branches require xi below ~{min(xi_hi, xi_lo)/pc:.1e} pc; l0 exceeds that by "
      f"{L0['canonical']/min(xi_hi, xi_lo):.1e}. Smoothing gives Newton by killing the argument, "
      f"sharpening gives Newton by saturating it; there is no third sign")

# ================================================================ 6. D -- the DOF gate
print("\n6. D -- THE DOF GATE (I3a, G4, P4): an actual Hamiltonian count, controls first")

def dirac_count(M, C, K, tol=1e-9, maxit=60):
    # LAPACK/BLAS leave stale IEEE flags that numpy then attributes to later matmuls; every array is
    # asserted finite inside, so the suppression cannot hide a real division by zero.
    with np.errstate(all="ignore"):
        return _dirac_count(M, C, K, tol=tol, maxit=maxit)

def _dirac_count(M, C, K, tol=1e-9, maxit=60):
    """Dirac constraint analysis for L = 1/2 qdot^T M qdot + qdot^T C q + 1/2 q^T K q.
       Returns the physical DOF (2n - 2*first_class - second_class)/2.
       Primary constraints from ker(M); the chain propagates only those combinations whose bracket with
       the PRIMARY set vanishes (the others fix multipliers instead of generating constraints)."""
    M = np.asarray(M, float); C = np.asarray(C, float); K = np.asarray(K, float)
    n = M.shape[0]; M = 0.5*(M + M.T); K = 0.5*(K + K.T)
    w, V = np.linalg.eigh(M)
    sc = max(1.0, np.max(np.abs(w))); keep = np.abs(w) > tol*sc
    Mp = (V[:, keep]*(1.0/w[keep])) @ V[:, keep].T if keep.any() else np.zeros((n, n))
    NL = V[:, ~keep]
    A = np.block([[C.T@Mp@C - K, -C.T@Mp], [-Mp@C, Mp]]); A = 0.5*(A + A.T)
    assert np.isfinite(Mp).all() and np.isfinite(A).all(), "singular pseudo-inverse in dirac_count"
    J = np.block([[np.zeros((n, n)), np.eye(n)], [-np.eye(n), np.zeros((n, n))]])
    B = np.zeros((2*n, 0))
    def add(vec):
        nonlocal B
        nv = np.linalg.norm(vec)
        if nv < 1e-12: return False
        v = vec/nv
        if B.shape[1]: v = v - B@(B.T@v)
        r = np.linalg.norm(v)
        if r < 1e-7: return False
        B = np.hstack([B, (v/r).reshape(-1, 1)]); return True
    for j in range(NL.shape[1]):
        v = NL[:, j]; add(np.concatenate([-C.T@v, v]))          # primary: v.(p - Cq) = 0
    P0 = B.copy(); n_prim = P0.shape[1]
    for _ in range(maxit):
        if B.shape[1] == 0: break
        Bs = B.copy()
        if n_prim:
            Pm = Bs.T@J@P0                                      # {phi_alpha, primary_a}
            u, sv, vt = np.linalg.svd(Pm, full_matrices=True)
            rank = int((sv > 1e-8*max(sv.max() if sv.size else 0.0, 1.0)).sum())
            nullv = u[:, rank:].T          # combinations whose consistency cannot fix a multiplier
        else:
            nullv = np.eye(Bs.shape[1])
        added = False
        for r_ in range(nullv.shape[0]):
            if add(-A@J@(Bs@nullv[r_])): added = True
        if not added: break
    m = B.shape[1]
    if m:
        sv = np.linalg.svd(B.T@J@B, compute_uv=False)
        SC = int((sv > 1e-8*max(sv.max(), 1.0)).sum())
    else:
        SC = 0
    FC = m - SC
    return dict(n=n, primary=n_prim, constraints=m, first_class=FC, second_class=SC,
                dof=(2*n - 2*FC - SC)/2.0)

def fierz_pauli(mass2=0.0, kval=1.0):
    """quadratic Fierz-Pauli at one real Fourier mode along z; parity = (-1)^(number of z indices)."""
    t, z, k = sp.symbols('t z k', real=True, positive=True)
    Cc, Ss = sp.symbols('Cc Ss')
    pairs = [(a, b) for a in range(4) for b in range(a, 4)]
    amp = {p: sp.Function('a_%d%d' % p)(t) for p in pairs}
    def par(a, b): return ((a == 3) + (b == 3)) % 2
    def h(a, b):
        p = (min(a, b), max(a, b)); return amp[p]*(Ss if par(*p) else Cc)
    eta = [-1, 1, 1, 1]
    def d(mu, e):
        if mu == 0: return sp.diff(e, t)
        if mu == 3: return k*(-e.diff(Cc)*Ss + e.diff(Ss)*Cc)
        return sp.Integer(0)
    hh = [[h(a, b) for b in range(4)] for a in range(4)]
    tr = sum(eta[a]*hh[a][a] for a in range(4))
    L = 0
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                L += -sp.Rational(1, 2)*eta[lam]*eta[mu]*eta[nu]*d(lam, hh[mu][nu])**2
                L += eta[mu]*eta[nu]*eta[lam]*d(mu, hh[nu][lam])*d(nu, hh[mu][lam])
    for nu in range(4):
        L += -sum(eta[mu]*eta[nu]*d(mu, hh[mu][nu]) for mu in range(4))*d(nu, tr)
    for lam in range(4):
        L += sp.Rational(1, 2)*eta[lam]*d(lam, tr)**2
    if mass2:
        h2 = sum(eta[a]*eta[b]*hh[a][b]**2 for a in range(4) for b in range(4))
        L += -sp.Rational(1, 2)*sp.nsimplify(mass2)*(h2 - tr**2)
    P = sp.Poly(sp.expand(L), Cc, Ss)
    Lav = 0
    for (i, j), co in zip(P.monoms(), P.coeffs()):
        if (i, j) == (2, 0) or (i, j) == (0, 2): Lav += co*sp.Rational(1, 2)
        elif (i, j) == (0, 0): Lav += co
    Lav = sp.expand(Lav)
    q = [amp[p] for p in pairs]; qd = [sp.diff(x, t) for x in q]; nq = len(q)
    Mm, Cm, Km = sp.zeros(nq, nq), sp.zeros(nq, nq), sp.zeros(nq, nq)
    for i in range(nq):
        for j in range(nq):
            Mm[i, j] = sp.diff(Lav, qd[i], qd[j]); Cm[i, j] = sp.diff(Lav, qd[i], q[j])
            Km[i, j] = sp.diff(Lav, q[i], q[j])
    ev = lambda X: np.array(sp.Matrix(X).subs({k: kval}).evalf(), float)
    return ev(Mm), ev(Cm), ev(Km)

def maxwell(kk=1.0, mm=0.0):
    n = 4; M = np.zeros((n, n)); C = np.zeros((n, n)); K = np.zeros((n, n))
    for i in (1, 2, 3): M[i, i] = 0.5
    C[3, 0] = 0.5*kk; K[0, 0] = 0.5*kk**2; K[1, 1] = -0.5*kk**2; K[2, 2] = -0.5*kk**2
    if mm:
        K[0, 0] += 0.5*mm**2
        for i in (1, 2, 3): K[i, i] -= 0.5*mm**2
    return M, C, K

print("    controls (textbook counts my machinery must reproduce before it is used on the candidate):")
ctl = []
r_ = dirac_count([[1.0]], [[0.0]], [[-1.0]]);                             ctl.append(("free scalar", r_, 1))
r_ = dirac_count(np.diag([1.0, 0.0]), np.zeros((2, 2)), np.array([[0.0, 1.0], [1.0, 0.0]]))
ctl.append(("scalar + Lagrange multiplier", r_, 0))
r_ = dirac_count(*maxwell(1.0, 0.0));                                     ctl.append(("Maxwell", r_, 2))
r_ = dirac_count(*maxwell(1.0, 1.0));                                     ctl.append(("Proca", r_, 3))
FPm = fierz_pauli(0.0); r_ = dirac_count(*FPm);                           ctl.append(("ADM/Fierz-Pauli GR", r_, 2))
FPM = fierz_pauli(1.0); r_ = dirac_count(*FPM);                           ctl.append(("massive Fierz-Pauli", r_, 5))
for nm, rr, want in ctl:
    print(f"      {nm:<30} n={rr['n']:2d}  primary={rr['primary']:2d}  constraints={rr['constraints']:2d}"
          f"  (1st {rr['first_class']:2d} / 2nd {rr['second_class']:2d})  ->  DOF = {rr['dof']:.1f}   [want {want}]")
check("C6 [control] the Dirac counter returns the textbook DOF on six known systems, including 2 for GR",
      all(abs(rr['dof'] - want) < 1e-9 for _, rr, want in ctl),
      "free scalar 1, scalar+multiplier 0, Maxwell 2, Proca 3, linearised GR 2, massive Fierz-Pauli 5")

print("\n    the candidate's own sector.  The filter is localised the only way it can be localised in an"
      "\n    action, with an auxiliary w and a multiplier lam:  L_f = lam[(1 - l^2 Delta) w - u].")
kk = 1.0; l2 = 2.0; sig = 1.0 + l2*kk**2
r_ell = dirac_count(np.zeros((2, 2)), np.zeros((2, 2)), np.array([[0.0, sig], [sig, 0.0]]))
r_tem = dirac_count(np.array([[0.0, -l2], [-l2, 0.0]]), np.zeros((2, 2)), np.array([[0.0, sig], [sig, 0.0]]))
kin_t = np.linalg.eigvalsh(np.array([[0.0, -l2], [-l2, 0.0]]))
r_deg = dirac_count(np.zeros((2, 2)), np.zeros((2, 2)), np.array([[0.0, 1e-14], [1e-14, 0.0]]))
print(f"      spatial/elliptic   (1 - l^2 Delta): constraints={r_ell['constraints']} "
      f"(1st {r_ell['first_class']} / 2nd {r_ell['second_class']})  ->  DOF = {r_ell['dof']:.1f}")
print(f"      temporal           (1 - l^2 Box)  : constraints={r_tem['constraints']} "
      f"(1st {r_tem['first_class']} / 2nd {r_tem['second_class']})  ->  DOF = {r_tem['dof']:.1f}, "
      f"kinetic eigenvalues {kin_t[0]:+.1f}, {kin_t[1]:+.1f} (one ghost)")
print(f"      elliptic at a ZERO of the symbol   : constraints={r_deg['constraints']} "
      f"(1st {r_deg['first_class']} / 2nd {r_deg['second_class']}) -- the four second-class constraints "
      f"degenerate; the auxiliary stops being determined by u")
check("D1 [A5's central claim] the spatial elliptic localisation adds NO canonical initial data",
      r_ell['dof'] == 0.0,
      "four second-class constraints (pi_w, pi_lam, (1-l^2 Delta)w - u, (1-l^2 Delta)lam) remove the pair "
      "exactly; this is the one part of A5 that is simply true, and it is true for any positive symbol")
check("D2 [P6 contrast] the SAME localisation with a temporal operator does add propagating modes, which "
      "is what makes P6 closed and A5 open",
      r_tem['dof'] >= 1.0 and kin_t[0] < 0 < kin_t[1],
      f"it adds {r_tem['dof']:.0f} with kinetic eigenvalues {kin_t[0]:+.0f}/{kin_t[1]:+.0f} -- a ghost "
      f"pair. P6's warning reproduced quantitatively from the same machinery that gives D1")
check("D3 [contrast] ellipticity is load-bearing in D1, i.e. the count changes at a zero of the symbol",
      r_deg['second_class'] < 4,
      f"at a zero of the symbol the second-class quartet collapses to {r_deg['first_class']} first-class "
      f"constraints: the auxiliary stops being determined by u and its evolution becomes undetermined. "
      f"Positivity of the symbol, not the word 'auxiliary', is what makes D1 true (P4)")

print("\n    the price A5 does not pay in D1: the filter needs a FOLIATION.  There is no covariant elliptic")
print("    operator on a Lorentzian manifold -- D^2 built from g alone is Box, which is hyperbolic -- so")
print("    'spatial' requires a unit timelike n_mu, i.e. a khronon tau with n_mu = -d_mu tau/|d tau|.")
print("    Two toy Lagrangians settle whether the A5 term itself can pay for that khronon.  In unitary")
print("    gauge the Stuckelberg field enters through the lapse, ln N ~ pi_dot:")
c14 = 0.3
K_A5   = np.array([[0.0]])                     # L = V N sqrt(gamma) Q(gamma): pi_dot enters LINEARLY
K_host = np.array([[2*c14*kk**2]])             # L = c14 (d_i ln N)^2 -> c14 (d_i pi_dot)^2
r_A5pi   = dirac_count(K_A5,   np.array([[0.0]]), np.array([[0.0]]))
r_hostpi = dirac_count(K_host, np.array([[0.0]]), np.array([[0.0]]))
print(f"      A5 term, N only in the measure  L = N sqrt(gamma) Q(gamma): pi_dot enters LINEARLY,"
      f" kinetic matrix = {K_A5[0,0]:.2f}  ->  khronon DOF = {r_A5pi['dof']:.1f}")
print(f"      host's acceleration term        L = c14 (d_i ln N)^2      : kinetic matrix = 2 c14 k^2 ="
      f" {K_host[0,0]:.2f}  ->  khronon DOF = {r_hostpi['dof']:.1f}")
check("D4 the A5 term supplies the kinetic normalisation of the foliation mode it requires",
      K_A5[0, 0] > 0.0,
      "the filter is built from gamma_ij alone and N appears only in the measure, so its khronon kinetic "
      "matrix is exactly ZERO. Either the host supplies c14 != 0 -- and then N_grav = 3, failing I3a -- "
      "or nothing does and the foliation scalar is infinitely strongly coupled, which is P7 verbatim. "
      "A5 is kinetically inert, and inertness is not the same as being free")
N_grav = ctl[4][1]['dof'] + r_ell['dof'] + r_hostpi['dof']
print(f"      => N_grav = {ctl[4][1]['dof']:.0f} (tensor, control) + {r_ell['dof']:.0f} (filter pair, D1)"
      f" + {r_hostpi['dof']:.0f} (the foliation the filter needs) = {N_grav:.0f}")
check("D5 [I3a] the A5 construction delivers exactly two gravitational modes",
      N_grav == 2.0,
      f"{N_grav:.0f}. The count is 2 only if the foliation is a NON-DYNAMICAL background structure, which "
      f"is not a diffeomorphism-invariant theory; with a dynamical khronon it is 3, the same count the "
      f"lead's parallel construction has (L4_VERIFICATION.md). A5's 'no temporal mode' is true of the "
      f"filter and false of the theory the filter has to live in")

# ================================================================ 7. S -- the screening gate
print("\n7. S -- THE SCREENING GATE (I4): is the trigger a local ACCELERATION?")
print("    two systems of the SAME size and 100x different acceleration; I4 demands they be screened")
print("    differently, since one is deep-MOND and the other is not:")
r_pair = 20*kpc
for f in A0:
    l = L0[f]
    for Mg in (1e9, 1e11):
        M = Mg*MSUN; gN = G*M/r_pair**2
        boost_A5 = g_A5L(r_pair, M, l)/gN
        boost_MOND = g_MOND(r_pair, M, A0[f])/gN
        print(f"    {f}: M = {Mg:.0e} Msun, g_N/a0 = {gN/A0[f]:7.4f}:  MOND boost = {boost_MOND:6.3f},"
              f"   A5-L boost = {boost_A5:.12f}")
b1 = {f: g_A5L(r_pair, 1e9*MSUN, L0[f])/(G*1e9*MSUN/r_pair**2) for f in A0}
b2 = {f: g_A5L(r_pair, 1e11*MSUN, L0[f])/(G*1e11*MSUN/r_pair**2) for f in A0}
check("S1 [I4] the A5 modification is controlled by a local acceleration",
      all(abs(b1[f]/b2[f] - 1) > 0.01 for f in A0),
      f"the two boosts are identical to {abs(b1['canonical']/b2['canonical'] - 1):.1e}: a filter is "
      f"triggered by a LENGTH (a wavenumber), never by an amplitude. This is I4's exact prohibition -- "
      f"the trigger is a scale label, not a dynamical acceleration")
SUNGATE = 3.66e-14      # repository's alpha=1 sunward gate: (a0/2)/1278, m s^-2
for f in A0:
    l = L0[f]; rS = 9.58*AU
    extra = 2*G*MSUN/(math.pi*l*rS)
    print(f"    {f}: A5-L anomalous sunward acceleration at Saturn = {extra:.3e} m/s^2 "
          f"(repository gate {SUNGATE:.2e}) -> {extra/SUNGATE:.1e} of the bound")
check("S2 [Solar System] A5-L passes the Solar-System gate",
      all(2*G*MSUN/(math.pi*L0[f]*9.58*AU) < SUNGATE for f in A0),
      "it passes by six orders of magnitude, but VACUOUSLY: it passes for the same reason it fails "
      "the MOND gate -- the modification is ~1e-16 of Newton everywhere inside 1 Mpc. A gate that a "
      "theory passes by doing nothing is not evidence of screening")

# ================================================================ 8. O -- A5's own caveat
print("\n8. O -- A5's OWN CAVEAT (G0): 'changes momentum scaling, NEVER perturbative amplitude order'")
print("    momentum scaling: the point-mass force law")
for f in A0:
    l = L0[f]; M = 1e11*MSUN
    for rr, un in ((1*kpc, "1 kpc   "), (1*Gpc, "1 Gpc   "), (100*Gpc, "100 Gpc "), (1e6*Gpc, "1e6 Gpc ")):
        gg = g_A5L(rr, M, l); gg2 = g_A5L(2*rr, M, l)
        print(f"    {f}: at r = {un}, local slope d ln g/d ln r = "
              f"{math.log(gg2/gg)/math.log(2.0):+.4f}")
R_FAR = 1e6*Gpc
sl_far = math.log(g_A5L(2*R_FAR, 1e11*MSUN, L0['canonical'])/g_A5L(R_FAR, 1e11*MSUN, L0['canonical']))/math.log(2)
check("O1 the elliptic operator CAN change the momentum scaling (1/r^2 -> 1/r)",
      abs(sl_far + 1) < 0.05, f"asymptotic slope {sl_far:+.4f}, i.e. exactly the flat-rotation-curve force "
                              f"law -- the first half of A5's note is correct")
print("\n    amplitude order: G0's rescaling rho -> eps rho (equivalently Phi -> eps Phi)")
eps = np.array([1.0, 1e-2, 1e-4, 1e-6])
for f in A0:
    l = L0[f]; a0 = A0[f]; M0 = 1e11*MSUN; rr = 300*kpc
    gl = np.array([g_A5L(rr, e*M0, l) - G*e*M0/rr**2 for e in eps])
    gm = np.array([g_MOND(rr, e*M0, a0) - G*e*M0/rr**2 for e in eps])
    p_l = np.polyfit(np.log(eps), np.log(gl), 1)[0]
    p_m = np.polyfit(np.log(eps), np.log(gm), 1)[0]
    print(f"    {f}: order of the EXTRA (non-Newtonian) force in eps:  A5-L {p_l:.6f},  "
          f"frozen kernel {p_m:.6f}")
pl = np.polyfit(np.log(eps), np.log([g_A5L(300*kpc, e*1e11*MSUN, L0['canonical']) - G*e*1e11*MSUN/(300*kpc)**2 for e in eps]), 1)[0]
pm = np.polyfit(np.log(eps), np.log([g_MOND(300*kpc, e*1e11*MSUN, A0['canonical']) - G*e*1e11*MSUN/(300*kpc)**2 for e in eps]), 1)[0]
check("O2 [A5's caveat, the decisive one] the elliptic operator can supply the MOND amplitude order",
      abs(pl - pm) < 0.05,
      f"A5-L's extra force is O(eps^{pl:.3f}) -- exactly first order, as any linear operator must be -- "
      f"while the frozen kernel's is O(eps^{pm:.3f}). MOND's phantom is NON-ANALYTIC in the source and "
      f"DOMINATES at small eps; a linear map cannot lower the order of anything. A5's note is not a "
      f"caveat about precision, it is a theorem about the class")

# ================================================================ 9. verdict
print("\n9. VERDICT")
_failed = set(FAILS)
def failed(pref): return any(x.startswith(pref) for x in _failed)
protein_ok = not (failed("M1") or failed("M2") or failed("M4") or failed("F1") or failed("O2"))
season_ok  = (not failed("D1")) and (not failed("C4"))
check("V1 A5 can be used as a PROTEIN -- a spatially nonlocal elliptic operator that produces MOND",
      protein_ok,
      "both placements close. Linear (A5-L): superposition forces g ~ M^1 where MOND needs M^1/2, for "
      "every symbol and every length (M1, O2) -- GENERIC to the class, not specific to this realisation. "
      "Filtered (A5-F): the length A5 licenses is c^2/a0 = 31 Gpc, 2.6e6 times the MOND radius, and it "
      "annihilates MOND from either side (F1-F3) -- generic to the a0-SCALED version, not to PAPER4's xi")
check("V2 A5 survives as a SEASONING -- a filter inside an already-MOND nonlinear term, with a length "
      "imported from somewhere other than a0",
      season_ok,
      "PAPER4's construction is exactly that and it works: its filter length 0.02-0.05 pc is fixed by the "
      "Solar System, not by a0 (C4 shows it is inert where it must be), and the nonlinear q -- not the "
      "filter -- carries the MOND kernel. A5's DOF claim (D1) is also simply true, and the "
      "elliptic/temporal contrast (D1 vs D2) is a clean quantitative statement of why P6 is closed")

print("\n  WHY, in one line: a nonlocal operator is triggered by a LENGTH; MOND is triggered by an")
print("  ACCELERATION; the dictionary between them is r_M = |Phi|/a0, i.e. the POTENTIAL -- which I4")
print("  forbids by name, which is not a local invariant, and which is mass-dependent and therefore not")
print("  an operator at all.  With only a0 and c the dictionary gives c^2/a0 instead, too long by")
print("  (c/v_flat)^2 ~ 2.6e6.  That is A5's amplitude clause, derived rather than quoted.")
print("\n  WHAT IS NOT CLOSED here, stated rather than hidden: (i) a filter whose length is a FIELD, "
      "\n  l = l[u], is not an operator and is not what A5 licenses, but it is also not tested here -- the "
      "\n  one such length that works is |Phi|/a0, which I4 forbids, and any other would have to be "
      "\n  exhibited; (ii) a nonlocal operator acting on something OTHER than the potential (on the metric "
      "\n  determinant, on a matter current) is outside this construction; (iii) the DOF statement D5 "
      "\n  assumes the foliation is carried by a khronon -- a non-dynamical preferred frame gives 2, at "
      "\n  the price of general covariance, and that trade is not evaluated here.")

ncf = len(CFAILS)
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") +
      f"\n        {ncf} of them CONTROL failures" + ("" if ncf == 0 else " -- THE RUN IS INVALID"))
print("        With the controls clean, the gate failures ARE the finding: A5 is not a protein.")
sys.exit(3 if ncf else 0)
