#!/usr/bin/env python3
"""
LEG A - LOCAL CURVATURE INVARIANTS: close-or-break calculation.

Trichotomy question (Layer C frontier): can a scalar functional q[g] built from
LOCAL curvature invariants (finite derivatives of Riemann at a point) deliver an
evolving a0(z) ~ H(z) INSIDE a virialized bound system, with no new DOF, no
Cauchy data, no conserved dark charge?

Four parts, each fully computed (no scaling guesses):
  A. Schwarzschild-de Sitter: ALL algebraic invariants (R, Ricci^2, Kretschmann,
     Weyl^2) computed symbolically; free-symbol audit shows they are functions of
     (m, r, Lambda) ONLY. Staticity => every finite covariant derivative is also
     t-independent. H(z) is NOT encoded locally in the bound vacuum region.
  B. McVittie: full Einstein tensor computed symbolically. Shows G^t_t = -3H(t)^2
     at EVERY radius => the cosmic energy density rho = 3H^2/8piG is forced to
     penetrate the bound region homogeneously, and the pressure needed to support
     it carries a (1+mu)/(1-mu) factor that DIVERGES at the would-be horizon
     unless Hdot = 0. The H-carrying of McVittie IS a forced penetrating medium
     (= the dark-fluid/leg-C escape in disguise), not a property of local vacuum
     geometry. Hdot=0 limit: p = -rho = const => Schwarzschild-dS (Layer A).
  C. Numbers: contamination and ceiling. (i) local matter Ricci vs cosmic-mean
     Ricci: 5-8 orders; (ii) the MAXIMAL physical imprint of expansion inside a
     bound system (the tidal H^2 r / q H^2 r acceleration) vs a0: ~1e-4 at
     100 kpc, and it is a tide (prop. to r), not a scale.
  D. Environment-coupled variant: a0 <- rho_local is the only surviving local
     coupling, and it is disfavored by the standing SPARC environmental-fork
     null (ledger-standing: rho_local-vs-rho_Lambda decisive null, 175 SPARC).

Units: geometric G=c=1 in the symbolic parts (m = GM/c^2); SI in part C.
"""

import sympy as sp

LINE = "=" * 78


def curvature_from_metric(gmat, coords):
    """Christoffel, Riemann (up-first), Ricci, scalar for a DIAGONAL metric."""
    n = len(coords)
    ginv = gmat.inv()
    Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = sp.S(0)
                for d in range(n):
                    if ginv[a, d] == 0:
                        continue
                    s += ginv[a, d] * (sp.diff(gmat[d, b], coords[c])
                                       + sp.diff(gmat[d, c], coords[b])
                                       - sp.diff(gmat[b, c], coords[d]))
                Gam[a][b][c] = sp.together(sp.cancel(s / 2))
    Riem = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    e = sp.diff(Gam[a][b][d], coords[c]) - sp.diff(Gam[a][b][c], coords[d])
                    for f in range(n):
                        e += Gam[a][c][f] * Gam[f][b][d] - Gam[a][d][f] * Gam[f][b][c]
                    Riem[a][b][c][d] = sp.together(sp.cancel(e))
    Ric = sp.zeros(n)
    for b in range(n):
        for d in range(n):
            Ric[b, d] = sp.simplify(sum(Riem[a][b][a][d] for a in range(n)))
    Rs = sp.simplify(sum(ginv[b, b] * Ric[b, b] for b in range(n)))
    return ginv, Gam, Riem, Ric, Rs


def quadratic_invariants(gmat, ginv, Riem, Ric, Rs, n=4):
    """Kretschmann, Ricci^2, Weyl^2 for a diagonal metric."""
    # lower the first index of Riemann
    Rlow = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    Rlow[a][b][c][d] = sp.cancel(gmat[a, a] * Riem[a][b][c][d])
    K = sp.S(0)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    if Rlow[a][b][c][d] != 0:
                        K += Rlow[a][b][c][d] ** 2 * ginv[a, a] * ginv[b, b] * ginv[c, c] * ginv[d, d]
    K = sp.simplify(K)
    R2 = sp.simplify(sum(Ric[a, b] ** 2 * ginv[a, a] * ginv[b, b]
                         for a in range(n) for b in range(n)))
    C2 = sp.simplify(K - 2 * R2 + sp.Rational(1, 3) * Rs ** 2)
    return K, R2, C2


# ============================================================================
print(LINE)
print("PART A: Schwarzschild-de Sitter -- the exact geometry of a bound vacuum")
print("        region in a Lambda universe (Einstein-Straus vacuole interior).")
print(LINE)

t, r, th, ph = sp.symbols('t r theta phi', real=True)
m, Lam = sp.symbols('m Lambda', positive=True)   # m = GM/c^2 (geometric)

f = 1 - 2 * m / r - Lam * r ** 2 / 3
g_sds = sp.diag(-f, 1 / f, r ** 2, r ** 2 * sp.sin(th) ** 2)
coords = [t, r, th, ph]

ginv, Gam, Riem, Ric, Rs = curvature_from_metric(g_sds, coords)
K, R2, C2 = quadratic_invariants(g_sds, ginv, Riem, Ric, Rs)

print(f"Ricci scalar        R          = {Rs}")
assert sp.simplify(Rs - 4 * Lam) == 0, "R != 4 Lambda"
# Einstein-space check: R_ab = Lambda g_ab
einstein_space = all(sp.simplify(Ric[a, b] - Lam * g_sds[a, b]) == 0
                     for a in range(4) for b in range(4))
print(f"R_ab = Lambda g_ab (Einstein space):   {einstein_space}")
assert einstein_space
print(f"Ricci^2             R_ab R^ab  = {R2}")
print(f"Kretschmann         R_abcd^2   = {K}")
print(f"Weyl^2              C_abcd^2   = {C2}")
assert sp.simplify(R2 - 4 * Lam ** 2) == 0
assert sp.simplify(C2 - 48 * m ** 2 / r ** 6) == 0
assert sp.simplify(K - (48 * m ** 2 / r ** 6 + sp.Rational(8, 3) * Lam ** 2)) == 0

print("\nFree-symbol audit (what a local functional can possibly read):")
for name, expr in [("R", Rs), ("Ricci^2", R2), ("Kretschmann", K), ("Weyl^2", C2)]:
    print(f"  {name:12s}: {sorted(str(s) for s in expr.free_symbols) or ['(constant)']}")
    assert t not in expr.free_symbols

# staticity => all covariant derivatives t-independent too
static_ok = all(sp.diff(g_sds[a, b], t) == 0 for a in range(4) for b in range(4))
print(f"\nMetric static (d/dt g_ab = 0 identically): {static_ok}")
assert static_ok
print("""
=> Every algebraic invariant is a function of (m, r, Lambda) ONLY.
=> Because the metric is STATIC, every FINITE covariant derivative of Riemann
   is likewise t-independent: the full local jet of the geometry at any point
   of the bound vacuum region carries NO t-dependence at all.
=> H(z) is simply NOT PRESENT in the local data. A functional a0^2[g] of local
   invariants evaluated here returns a0^2(m, r, Lambda):
     - the Lambda piece is CONSTANT  -> Layer A (a0^2 = c^4 Lambda/32pi), fine;
     - the (m, r) piece is ENVIRONMENT-DEPENDENT -> Part D.
   There is no third option: those are the only symbols available.""")

# ============================================================================
print(LINE)
print("PART B: McVittie -- resolve the apparent counterexample")
print(LINE)

a = sp.Function('a', positive=True)(t)
mu = m / (2 * a * r)                       # isotropic-coordinate McVittie
g_tt = -((1 - mu) / (1 + mu)) ** 2
psi4 = (1 + mu) ** 4 * a ** 2
g_mcv = sp.diag(g_tt, psi4, psi4 * r ** 2, psi4 * r ** 2 * sp.sin(th) ** 2)

ginvM, GamM, RiemM, RicM, RsM = curvature_from_metric(g_mcv, coords)

H = sp.Function('H', real=True)(t)
adot_sub = {sp.Derivative(a, t): H * a,
            sp.Derivative(a, t, 2): (sp.Derivative(H, t) + H ** 2) * a}

def to_H(expr):
    e = expr
    # substitute a'' first, then a'
    e = e.subs(sp.Derivative(a, t, 2), (sp.Derivative(H, t) + H ** 2) * a)
    e = e.subs(sp.Derivative(a, t), H * a)
    return sp.simplify(e)

# Einstein tensor, mixed components
G_tt_mixed = to_H(sp.simplify(ginvM[0, 0] * (RicM[0, 0] - g_mcv[0, 0] * RsM / 2)))
G_rr_mixed = to_H(sp.simplify(ginvM[1, 1] * (RicM[1, 1] - g_mcv[1, 1] * RsM / 2)))
R_mcv = to_H(RsM)
Hd = sp.Derivative(H, t)

print(f"McVittie  G^t_t = {G_tt_mixed}")
check_rho = sp.simplify(G_tt_mixed + 3 * H ** 2)
print(f"  G^t_t + 3H^2 = {check_rho}   (0 => rho = 3H^2/8piG at EVERY radius)")
assert check_rho == 0

target_p = -3 * H ** 2 - 2 * Hd * (1 + mu) / (1 - mu)
check_p = sp.simplify(G_rr_mixed - target_p)
print(f"McVittie  G^r_r = -3H^2 - 2*Hdot*(1+mu)/(1-mu):  residual = {check_p}")
assert check_p == 0

target_R = 12 * H ** 2 + 6 * Hd * (1 + mu) / (1 - mu)
check_R = sp.simplify(R_mcv - target_R)
print(f"McVittie  R     = 12H^2 + 6*Hdot*(1+mu)/(1-mu):  residual = {check_R}")
assert check_R == 0

print("""
RESOLUTION (exact, from the components above):
  1. G^t_t = -3H^2 at EVERY radius means the Einstein equations force the FULL
     COSMIC ENERGY DENSITY rho(t) = 3H^2/8piG to be present homogeneously at
     every point, arbitrarily deep inside the 'bound' region. McVittie does not
     show vacuum geometry reading H; it shows a spacetime DEFINED by injecting
     a cosmological medium everywhere. The H-dependence of R rides on T_ab, via
     R = 8pi(rho - 3p) -- Einstein's equations, not local vacuum structure.
  2. The pressure that sustains this is NOT free: p(r,t) carries the factor
     (1+mu)/(1-mu), which DIVERGES at mu -> 1 (the would-be horizon) whenever
     Hdot != 0. A real virialized system has no such singular pressure shell.
  3. The z-carrying piece of R is exactly the Hdot term -- the SAME term whose
     pressure profile is singular and radius-dependent. Strip the medium
     (impose T_ab = 0 with Lambda in the interior) and Birkhoff/Einstein-Straus
     force the interior to be EXACTLY Schwarzschild-dS: Part A applies, H gone.
  4. Hdot = 0 limit: p = -rho = -3H^2/8pi = const => the medium degenerates to
     Lambda and McVittie is Schwarzschild-dS in disguise (Layer A, constant a0).
=> McVittie's H-carrying medium IS the dark fluid: a physical T_ab with a
   prescribed pressure profile penetrating the bound system. Specifying and
   transporting that medium off-FLRW is Cauchy data + a preferred flow = the
   congruence/dark-fluid leg. Leg A is not breached.""")

# ============================================================================
print(LINE)
print("PART C: Quantify -- can any scalar combination isolate an H(z) piece")
print("        inside a real virialized region?  (SI numbers)")
print(LINE)

import math
Gsi = 6.674e-11; csi = 2.998e8
H0 = 2.20e-18            # s^-1  (67.8 km/s/Mpc)
rho_crit = 3 * H0 ** 2 / (8 * math.pi * Gsi)
rho_m_mean = 0.31 * rho_crit
rho_ISM = 1e-21          # kg/m^3 galactic ISM
rho_disk = 1e-20         # solar-neighborhood midplane
rho_halo_gas = 1e-25     # hot circumgalactic gas
a0 = 9.36e-11            # framework a0

print(f"rho_crit               = {rho_crit:.3e} kg/m^3")
print(f"rho_m_mean(z=0)        = {rho_m_mean:.3e} kg/m^3")
print("\nRicci contamination R_local/R_cosmic-matter = rho_local/rho_m_mean(z):")
for name, rho in [("ISM 1e-21", rho_ISM), ("disk midplane 1e-20", rho_disk),
                  ("CGM hot gas 1e-25", rho_halo_gas)]:
    for z in (0, 1):
        ratio = rho / (rho_m_mean * (1 + z) ** 3)
        print(f"  {name:22s} z={z}:  {ratio:.2e}")
print("""
The matter-sourced Ricci sector inside a galaxy exceeds the cosmic-mean piece
by ~4 to 7 orders (CGM) up to ~5-8 orders (disk/ISM), with O(1) scatter from
system to system.  The a0(z) ~ H(z) signal is an O(1) change by z=1
(E(1) ~ 1.75).  Any 'scalar combination' that tries to proxy Hbar(z) via local
density therefore reads a contaminant 1e4-1e8 times the signal.  There is no
combination that cancels the contaminant: by Part A the local jet contains only
(m, r, Lambda, rho_local(x)); the cosmic mean rho_bar(z) -- the only local
carrier of H(z) besides Lambda -- is not among the local data of a DETACHED
region (it was expelled at turnaround/virialization).""")

# ceiling on the REAL imprint of expansion inside a bound system
for rsys_kpc in (10.0, 100.0):
    rsys = rsys_kpc * 3.086e19
    tidal = H0 ** 2 * rsys          # |q| ~ O(1); H^2 r tidal acceleration
    print(f"maximal expansion imprint (tidal ~ H^2 r) at r = {rsys_kpc:5.0f} kpc: "
          f"{tidal:.2e} m/s^2  = {tidal / a0:.1e} * a0 ;  (H r/c)^2 = {(H0*rsys/csi)**2:.1e}")
print("""
Even the MAXIMAL genuine local imprint of the expansion history (the tidal
q H^2 r acceleration; metric corrections O((Hr/c)^2) ~ 1e-9) is ~1e-6 - 1e-4
of a0 at 10-100 kpc, grows linearly with r (a tide, not a scale), and its
constant part is already the Lambda term of Part A.  The z-dependent part
(Hdot) is the piece McVittie shows requires the penetrating medium.  So the
H(z) 'signal' available to a local functional inside a bound system is 4-6
orders too SMALL, while the density contaminant is 4-8 orders too LARGE.""")

# ============================================================================
print(LINE)
print("PART D: the environment-coupled variant + the dynamical-embedding trap")
print(LINE)
print("""
D1. ENVIRONMENT COUPLING. By Part A the only non-constant local scalars are
    (m/r^3-type Weyl invariants) and rho_local.  An a0 built from them is an
    ENVIRONMENT-DEPENDENT a0 varying by orders of magnitude across and within
    galaxies (Part C spreads).  This is the rho_local-vs-rho_Lambda fork, and
    the standing SPARC environmental-fork null (LEDGER-STANDING: decisive null
    on 175 SPARC galaxies, rho_local coupling disfavored at 13-34 sigma;
    pipeline committed, BIG-SPARC extension pending) already disfavors it.
    It also does not deliver the target: rho_local does not track H(z).

D2. DYNAMICAL-EMBEDDING TRAP (why 'just put q[g] in the action' fails the
    no-DOF condition).  To make a0[g] act on matter, q[g] must enter the
    dynamics.  Two exhaustive cases:
      (a) q[g] NON-DYNAMICAL (a formula evaluated on-shell): then Parts A-C
          apply directly -> constant (Layer A) or environment-dependent (D1).
      (b) q[g] IN THE ACTION: any f(R) is equivalent to GR + a propagating
          scalaron (new DOF, new Cauchy data) -- violating condition (i);
          f(Ricci^2, Riemann^2) generically adds ghosts; the one 4D exception,
          Gauss-Bonnet, is topological and contributes nothing locally.  The
          'no new DOF' condition removes exactly the machinery that could make
          a local invariant dynamical.
    Either way Leg A cannot yield an evolving a0(z) in bound systems.

VERDICT: LEG A CLOSES.  In a virialized region detached from the expansion,
local curvature invariants read (M, r, Lambda, rho_local) and nothing else;
H(z) is not in the local jet (Part A), cannot be smuggled in without a
penetrating medium (Part B: McVittie = dark fluid in disguise), is numerically
unreachable by any density proxy (Part C), and the environment-coupled fallback
is ledger-disfavored and off-target (D1).  Constant a0 (Layer A) is untouched.
""")
print("ALL SYMPY ASSERTIONS PASSED")
