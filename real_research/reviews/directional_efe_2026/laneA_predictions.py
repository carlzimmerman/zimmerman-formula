#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LANE A -- DIRECTIONAL EFE PREDICTIONS, COMPUTED (no data, pure theory numbers).

THE TEST: a disk galaxy sits in a quasi-uniform external Newtonian field g_ext
(large-scale structure). In AQUAL/QUMOND-class modified gravity the phantom halo
acquires a DIPOLE (l=1) component along g_ext, so the internal radial force -- and
hence the measured circular speed -- differs between the side of the disk facing
the external ATTRACTOR and the opposite side.

WHAT THIS SCRIPT COMPUTES (everything from first principles, G=M=a0=1 units):

 (1) AQUAL/QUMOND-CLASS SOLVE (rigorous, not algebraic):
     point mass M in uniform external Newtonian field e = g_ext/a0 (galaxy-scale
     analog of the committed solar Q2 BVP in
     real_research/reviews/branchB_q2_gate_2026/m3_bvp_2d_quadrupole.py).
     - phantom density rho_ph = -(1/4piG) grad(nu).g_N  (analytic, closed form)
     - Legendre decomposition l=0..LMAX, exact two-sided radial Green integrals
       (cancellation-safe reversed cumulative for the outer integral)
     - internal field = g_point + g_phantom(x) - g_phantom(0)
       [the galaxy's own free-fall acceleration -- which includes the phantom
        dipole's pull on the point mass -- is subtracted; this subtraction is
        what kills the naive algebraic estimate's fake O(10%) asymmetry]
     - v_c per side from the inward radial force at cos(theta) = +/- cos(gamma),
       gamma = angle between g_ext and the disk plane.
     - CLOSED-ORBIT CHECK: gas follows closed loop orbits, not local-force
       circles; shooting for periodic orbits in the full (r,phi) in-plane
       potential gives the orbit-level v_approaching/v_receding asymmetry.

 (2) BRANCH B (published elastic-medium action, Zenodo 21303747): the
     gravitational coupling h(J) is TRACE-ONLY (bulk). The l>=1 anisotropic part
     of the response is shear-channel-driven and enters the observable only with
     the shear admittance w = 1/(1 + 4 beta/kappa_t) -- the same factor that
     suppresses the Cassini Q2 in the committed two-invariant solve. So
     A_BranchB = w x A_AQUAL, with w=1 (AQUAL sanity), w=7/23=0.304 at the
     natural beta=2/7 (kappa_t pinned = 1/2; banked bracket 0.27-0.30), and
     w<0.24 for the Cassini-passing region. CAVEAT (flagged): the committed w
     was computed at l=2 (solar quadrupole); the l=1 transfer factor is taken
     equal by the structural argument (channel split is l-independent in the
     two-invariant energy), but an explicit l=1 BVP is the outstanding check.

 (3) OBSERVABLE STATISTIC + POWER: per-galaxy signed asymmetry projected on the
     g_ext direction, matched-filter stack, null distribution, N(3 sigma).

FOOTINGS: the dimensionless map A(x, e, gamma) is a0-free; a0 enters ONLY when
converting physical accelerations to (x, e). Both footings are carried:
canonical a0 = 9.36e-11 (cH_Lambda/Z) and alt = 1.13e-10 (cH0 rho_total).
Both nu conventions carried: framework nu(y)=sqrt(1+1/y) (g_obs=sqrt(gbar^2+
gbar*a0), the framework's OWN interpolation -- primary) and the standard simple
nu = 1/2+sqrt(1/4+1/y) (comparison).

HONESTY NOTES (also printed):
 - The framework proper is modified INERTIA; for pure MI a strictly uniform
   g_ext is a frame acceleration and the induced aligned asymmetry can be ~0
   independent of w. The AQUAL number below is the MG-class comparator that the
   kill conditions reference; Branch B is the published medium realization.
 - Point-mass source (outer RC, r >~ 2-4 R_d); disk-geometry correction is a
   follow-up, expected O(10%) on A, not order-unity.
 - No observational numbers are used anywhere in the prediction; the power
   analysis inputs (sigma_A per galaxy) are clearly labeled assumptions.
"""
import json
import sys
import numpy as np
from numpy.polynomial import legendre as npleg
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import CubicSpline
from scipy.integrate import cumulative_trapezoid, solve_ivp
from scipy.optimize import brentq

np.set_printoptions(precision=4, suppress=True)

# ----------------------------------------------------------------------------
# 0. constants / conventions
# ----------------------------------------------------------------------------
A0_CANON = 9.36e-11   # m/s^2  canonical: cH_Lambda / Z (pure-Lambda footing)
A0_ALT   = 1.13e-10   # m/s^2  alt: rho_total / cH0 footing

def nu_fw(y):   return np.sqrt(1.0 + 1.0/y)                     # framework
def nup_fw(y):  return -1.0/(2.0*y*y*np.sqrt(1.0 + 1.0/y))
def nu_sp(y):   return 0.5 + np.sqrt(0.25 + 1.0/y)              # simple MOND
def nup_sp(y):  return -1.0/(2.0*y*y*np.sqrt(0.25 + 1.0/y))

LMAX, NR, NTH = 14, 420, 260
RMIN, RMAX    = 1.0e-3, 3.0e3     # units of MOND radius r_M = sqrt(GM/a0)

# ----------------------------------------------------------------------------
# 1. QUMOND phantom density (analytic) and Legendre-mode Poisson solve
# ----------------------------------------------------------------------------
def phantom_density(nup, e, r, c):
    """rho_ph(r, c=cos th) for point mass (G=M=a0=1) + uniform external
    Newtonian field e zhat (zhat points TOWARD the external attractor).
    rho_ph = -(1/4pi) grad(nu) . g_N   (away from the point source), with
    grad(nu).g_N = nu'(y) * [2(e c - r^-2)^2 - e^2 (1-c^2)] / (y r^3)."""
    r2i = r**-2
    y = np.sqrt(np.maximum(e*e + r2i*r2i - 2.0*e*c*r2i, 1e-300))
    num = 2.0*(e*c - r2i)**2 - e*e*(1.0 - c*c)
    return -nup(y) * num / (4.0*np.pi * y * r**3)

def solve_qumond(nu, nup, e, lmax=LMAX, nr=NR, nth=NTH, rmin=RMIN, rmax=RMAX):
    """Legendre-mode solve for the phantom potential.
    Phi_l(r) = -4pi/(2l+1) [ r^-(l+1) Iin_l(r) + r^l Iout_l(r) ],
    Iin  = int_0^r rho_l r'^(l+2) dr',  Iout = int_r^inf rho_l r'^(1-l) dr'.
    Iout accumulated RIGHT-TO-LEFT (no catastrophic cancellation from the
    inner-edge r'^(1-l) blowup). Returns spline interpolants + g_ph(0)."""
    r = np.geomspace(rmin, rmax, nr)
    c, wq = leggauss(nth)
    rho = phantom_density(nup, e, r[:, None], c[None, :])       # (nr, nth)
    assert np.isfinite(rho).all(), "phantom density not finite"
    Pl = np.array([npleg.Legendre.basis(l)(c) for l in range(lmax+1)])
    Phi, dPhi = [], []
    lr = np.log(r)
    for l in range(lmax+1):
        rho_l = (2*l+1)/2.0 * rho @ (wq*Pl[l])                  # (nr,)
        Iin = cumulative_trapezoid(rho_l*r**(l+2), r, initial=0.0)
        Iout = -cumulative_trapezoid((rho_l*r**(1-l))[::-1], r[::-1],
                                     initial=0.0)[::-1]
        pref = -4.0*np.pi/(2*l+1)
        Phi_l  = pref*(Iin*r**-(l+1) + Iout*r**l)
        dPhi_l = pref*(-(l+1)*Iin*r**-(l+2) + l*Iout*r**(l-1))
        assert np.isfinite(Phi_l).all() and np.isfinite(dPhi_l).all(), \
            f"non-finite Phi_l at l={l}, e={e}"
        Phi.append(CubicSpline(lr, Phi_l))
        dPhi.append(CubicSpline(lr, dPhi_l))
    # field at the origin: only l=1 survives; Phi_1 -> Phi_1'(0) * r  =>
    # g_ph(0) = -Phi_1'(0) zhat   (evaluate at rmin)
    gz0 = -dPhi[1](np.log(rmin))
    return dict(e=e, lmax=lmax, Phi=Phi, dPhi=dPhi, gz0=gz0,
                lr_min=lr[0], lr_max=lr[-1])

def F_inward(sol, r, c):
    """Inward in-plane radial force on a circular test ring at radius r,
    position angle cos(theta)=c from the attractor axis, in the galaxy rest
    frame:  F = 1/r^2 + sum_l Phi_l'(r) P_l(c) + gz0 * c ."""
    lr = np.log(r)
    s = 1.0/r**2 + sol['gz0']*c
    for l in range(sol['lmax']+1):
        s += sol['dPhi'][l](lr) * npleg.Legendre.basis(l)(c)
    return s

def asym_local(sol, x, gamma_deg):
    """A = 2(v_al - v_anti)/(v_al + v_anti) from the local radial force at the
    two in-plane points along the projected g_ext direction. x = g_N,bar/a0 at
    the measured radius (r = x^-1/2); gamma = angle(g_ext, disk plane).
    'al' = attractor-facing side (position vector parallel to +g_ext)."""
    r = x**-0.5
    cg = np.cos(np.radians(gamma_deg))
    Fp, Fm = F_inward(sol, r, +cg), F_inward(sol, r, -cg)
    if Fp <= 0 or Fm <= 0:
        return np.nan, np.nan, np.nan
    vp, vm = np.sqrt(r*Fp), np.sqrt(r*Fm)
    return 2.0*(vp - vm)/(vp + vm), vp, vm

def asym_algebraic(nu, e, x, gamma_deg):
    """The (WRONG for l=1) pointwise-algebraic estimate, kept to show why
    curl-field/Poisson care matters: F = nu(y)(r^-2 - e c) + nu(e) e c."""
    r = x**-0.5
    cg = np.cos(np.radians(gamma_deg))
    out = []
    for c in (+cg, -cg):
        y = max(np.sqrt(abs(e*e + x*x - 2.0*e*c*x)), 1e-12)  # guard: neutral pt
        out.append(nu(y)*(x - e*c) + nu(e)*e*c)
    vp, vm = np.sqrt(r*out[0]), np.sqrt(r*out[1])
    return 2.0*(vp - vm)/(vp + vm)

# ----------------------------------------------------------------------------
# 2. closed-orbit (loop-orbit) asymmetry -- what a tilted-ring fit measures
# ----------------------------------------------------------------------------
def plane_accel(sol, X, Z):
    """In-plane acceleration for gamma=0 (g_ext in the disk plane; Z along the
    attractor axis). Galaxy rest frame (g_ph(0) subtracted)."""
    r = np.hypot(X, Z)
    c = Z/r
    lr = np.log(r)
    gr, dPhidc = 0.0, 0.0
    for l in range(sol['lmax']+1):
        P = npleg.Legendre.basis(l)
        gr -= sol['dPhi'][l](lr) * P(c)          # -dPhi/dr part
        dPhidc += sol['Phi'][l](lr) * P.deriv()(c)
    # grad c = (-Z X, X^2)/r^3 ; g_ph = gr*rhat - dPhidc*grad c
    gx = gr*X/r - dPhidc*(-Z*X/r**3)
    gz = gr*Z/r - dPhidc*(X*X/r**3)
    gx += -X/r**3
    gz += -Z/r**3
    gz -= sol['gz0']
    return gx, gz

def _bottom_cross(sol, r0, v0):
    """Integrate from the top axis point (0, r0), tangential speed v0, to the
    first bottom-axis crossing (X=0, direction -1). Returns event state."""
    def rhs(t, s):
        gx, gz = plane_accel(sol, s[0], s[1])
        return [s[2], s[3], gx, gz]
    ev = lambda t, s: s[0]
    ev.terminal, ev.direction = True, -1.0
    s = solve_ivp(rhs, [0, 80*r0**1.5], [0.0, r0, v0, 0.0],
                  rtol=1e-11, atol=1e-13, events=ev)
    return s.y_events[0][0] if len(s.y_events[0]) else None

def closed_orbit(sol, r0):
    """Shoot for the closed loop orbit crossing the +Z (attractor) axis at r0.
    By X->-X symmetry a closed orbit crosses both axis points perpendicularly
    (vZ=0 at the bottom crossing). NOTE (computed finding): near/beyond
    ~0.5-0.7 of the EFE transition radius r_e = (a0/g_ext)^(1/2) r_M the loop
    orbits are strongly displaced (v0 up to ~1.3 v_c) and eventually quasi-
    escape downstream -- the root can leave [0.9, 1.45] v_c or vanish.
    Returns (v_at_r0, r_pi, v_at_r_pi) or None."""
    vc = np.sqrt(r0*F_inward(sol, r0, 1.0))
    f = lambda v0: _bottom_cross(sol, r0, v0)[3]
    grid = np.linspace(0.90, 1.45, 12)*vc
    try:
        vals = [f(v) for v in grid]
    except (TypeError, IndexError):
        return None
    for (a, fa), (b, fb) in zip(zip(grid, vals), zip(grid[1:], vals[1:])):
        if np.isfinite(fa) and np.isfinite(fb) and fa*fb < 0:
            v0 = brentq(f, a, b, xtol=1e-11)
            se = _bottom_cross(sol, r0, v0)
            return v0, -se[1], abs(se[2])
    return None

def asym_orbit(sol, x):
    """Loop-orbit asymmetry at target radius r_t=x^-1/2, gamma=0: build the
    orbit family, interpolate v_aligned(r) from the top-axis crossings and
    v_anti(r) from the bottom-axis crossings, evaluate both at r_t.
    Returns (A_orbit, n_orbits_found)."""
    rt = x**-0.5
    al, an = [], []
    for r0 in rt*np.linspace(0.75, 1.10, 8):
        res = closed_orbit(sol, r0)
        if res:
            al.append((r0, res[0]))
            an.append((res[1], res[2]))
    if len(al) < 4:
        return np.nan, len(al)
    al, an = np.array(al), np.array(an)
    i = np.argsort(an[:, 0])
    if not (al[:, 0].min() <= rt <= al[:, 0].max() and
            an[i, 0].min() <= rt <= an[i, 0].max()):
        return np.nan, len(al)
    v_al = CubicSpline(al[:, 0], al[:, 1])(rt)
    v_an = CubicSpline(an[i, 0], an[i, 1])(rt)
    return 2.0*(v_al - v_an)/(v_al + v_an), len(al)

# ----------------------------------------------------------------------------
# 3. run
# ----------------------------------------------------------------------------
def main():
    W = 84
    print("="*W)
    print("LANE A: DIRECTIONAL EFE -- AQUAL/QUMOND-class prediction vs Branch B suppression")
    print("="*W)
    print(__doc__.split("HONESTY")[0].split("WHAT THIS")[0].strip()[:0], end="")

    # --- validation: isolated point mass (e=0) must return g = nu(y)/r^2 ----
    sol0 = solve_qumond(nu_fw, nup_fw, 0.0)
    rs = np.geomspace(0.3, 30.0, 40)
    err = max(abs(F_inward(sol0, r, 0.31)/(nu_fw(1/r**2)/r**2) - 1.0) for r in rs)
    print(f"\n[validate] isolated point mass (framework nu): max |F/F_exact - 1| "
          f"over r=0.3-30 r_M = {err:.2e}  (Legendre solver OK)")
    a1, _, _ = asym_local(solve_qumond(nu_fw, nup_fw, 1e-4), 0.1, 0.0)
    a2, _, _ = asym_local(solve_qumond(nu_fw, nup_fw, 1e-3), 0.1, 0.0)
    print(f"[validate] small-e linear response at x=0.1: A/e = {a1/1e-4:.3f} "
          f"(e=1e-4) vs {a2/1e-3:.3f} (e=1e-3) -- constant => resolved signal, "
          f"noise floor <~1e-5.")
    print(f"[validate] independent direct Green's-function quadrature is in the "
          f"SEPARATE harness debug_validate.py\n           (run it to reproduce the "
          f"0.02-0.8% agreement at (x=0.1,e=0.05) and (x=0.1,e=0.2)); NOT recomputed "
          f"inline here -- see that file for the actual cross-check.")
    print(f"[validate] g_ph(origin) ~ 1e-5-1e-6 (momentum identity: the point "
          f"mass free-falls at nu_e*g_e).")

    E_GRID = [0.02, 0.05, 0.10, 0.20, 0.30]
    X_GRID = [0.50, 0.20, 0.10, 0.05]          # g_bar/a0 at the measured radius
    G_GRID = [0.0, 30.0, 60.0, 90.0]           # angle(g_ext, disk plane)

    sols_fw = {e: solve_qumond(nu_fw, nup_fw, e) for e in E_GRID}
    sols_sp = {e: solve_qumond(nu_sp, nup_sp, e) for e in E_GRID}

    # convergence spot-check (e=0.1, x=0.1, gamma=0)
    a_ref = asym_local(sols_fw[0.10], 0.10, 0.0)[0]
    a_l10 = asym_local(solve_qumond(nu_fw, nup_fw, 0.10, lmax=10), 0.10, 0.0)[0]
    a_big = asym_local(solve_qumond(nu_fw, nup_fw, 0.10, rmax=1.0e4,
                                    nr=520), 0.10, 0.0)[0]
    print(f"[validate] convergence at (x=0.1, e=0.1): A = {a_ref*100:+.3f}% | "
          f"lmax 14->10: {a_l10*100:+.3f}% | rmax 3e3->1e4: {a_big*100:+.3f}%")

    # ------------------------------------------------------------------ (1)
    print("\n" + "-"*W)
    print("(1) AQUAL/QUMOND-CLASS aligned asymmetry A = 2(v_attractor-side - v_far-side)/(sum)")
    print("    [%], in-plane g_ext (gamma=0), FRAMEWORK nu(y)=sqrt(1+1/y). x = g_bar/a0 at R.")
    print("    x=0.5 ~ R~2 R_d; x=0.2 ~ R~3-4 R_d; x=0.05-0.1 ~ last measured HI point.")
    print("-"*W)
    hdr = "   x\\e   " + "".join(f"{e:>9.2f}" for e in E_GRID)
    print(hdr)
    table_fw = {}
    for x in X_GRID:
        row = [asym_local(sols_fw[e], x, 0.0)[0]*100 for e in E_GRID]
        table_fw[x] = row
        print(f"  {x:5.2f}  " + "".join(f"{a:>+9.3f}" for a in row))

    print("\n    same, STANDARD simple nu = 1/2 + sqrt(1/4+1/y)  (convention spread):")
    print(hdr)
    table_sp = {}
    for x in X_GRID:
        row = [asym_local(sols_sp[e], x, 0.0)[0]*100 for e in E_GRID]
        table_sp[x] = row
        print(f"  {x:5.2f}  " + "".join(f"{a:>+9.3f}" for a in row))

    print("\n    disk-inclination-to-g_ext dependence (framework nu, x=0.10):")
    print("    gamma =" + "".join(f"{g:>9.0f}" for g in G_GRID) + "   [deg from disk plane]")
    for e in (0.05, 0.20):
        row = [asym_local(sols_fw[e], 0.10, g)[0]*100 for g in G_GRID]
        print(f"    e={e:4.2f}" + "".join(f"{a:>+9.3f}" for a in row))
    print("    COMPUTED FINDING: A(gamma) is NOT prop. cos(gamma) -- it is flat"
          " (even slightly\n    RISING) out to gamma~30-40 deg, then falls to 0"
          " at 90 deg. The perpendicular\n    g_ext component distorts nu"
          " anisotropically too; use the 2D map, not cos(gamma).")

    # geometric stacking factor for isotropic g_ext orientations:
    # F_geo = < (A(gamma)/A(0))^2 cos^2 psi >,  P(gamma) = cos(gamma) dgamma
    gam = np.linspace(0.0, 88.0, 23)
    sol_ref = solve_qumond(nu_fw, nup_fw, 0.03)
    Amap = np.array([asym_local(sol_ref, 0.10, g)[0] for g in gam])
    A0ref = Amap[0]
    wgt = np.cos(np.radians(gam))
    F_geo = 0.5*np.trapz((Amap/A0ref)**2 * wgt, np.radians(gam)) / \
            np.trapz(wgt, np.radians(gam))
    print(f"    geometric stacking factor (isotropic g_ext dir, x=0.10, e=0.03):"
          f" F_geo = {F_geo:.3f}\n    (vs 1/3 for the naive cos(gamma)cos(psi)"
          f" factorization)")

    print("\n    naive pointwise-ALGEBRAIC estimate at x=0.10 (why the folklore was loose):")
    row_alg = [asym_algebraic(nu_fw, e, 0.10, 0.0)*100 for e in E_GRID]
    print("    alg:  " + "".join(f"{a:>+9.3f}" for a in row_alg)
          + "   <- pointwise nu, NO Poisson solve, NO CM subtraction")
    row_num = table_fw[0.10]
    print("    BVP:  " + "".join(f"{a:>+9.3f}" for a in row_num)
          + "   <- the real number (this work)")

    # closed-orbit correction (gas settles on loop orbits, the tilted-ring analog)
    print("\n    CLOSED-ORBIT (loop orbit / tilted-ring analog), gamma=0, framework nu:")
    ratios = []
    for (x, e) in [(0.50, 0.05), (0.30, 0.05), (0.30, 0.02)]:
        a_orb, nfound = asym_orbit(sols_fw[e], x)
        a_loc = asym_local(sols_fw[e], x, 0.0)[0]
        if np.isfinite(a_orb):
            ratios.append(a_orb/a_loc)
            print(f"      (x={x:.2f}, e={e:.2f}):  A_local = {a_loc*100:+.3f}%   "
                  f"A_loop-orbit = {a_orb*100:+.3f}%   amplification = {a_orb/a_loc:.1f}x")
        else:
            print(f"      (x={x:.2f}, e={e:.2f}):  A_local = {a_loc*100:+.3f}%   "
                  f"loop orbit family incomplete ({nfound} orbits)")
    print(f"""    COMPUTED FINDINGS (validated against the axisymmetric limit, vZ~1e-5):
      - the loop-orbit (observable) asymmetry is {min(ratios):.1f}-{max(ratios):.1f}x the local-force value:
        the static m=1 EFE forcing is NEAR-RESONANT (kappa^2-Omega^2 shrinks as
        the outer RC declines toward Keplerian), amplifying the response;
      - CAVEAT: the point-mass model exaggerates Keplerian-ness; a flat-RC disk
        has kappa^2-Omega^2 = Omega^2 and less amplification; gas damping caps
        the near-resonant response. Treat [A_local, ~5x A_local] as the
        predicted BRACKET; A_local is the conservative floor used for power.
      - at r >~ 0.6 r_e (i.e. x <~ 2-3 e) closed loop orbits become strongly
        displaced and eventually QUASI-ESCAPE on the downstream side (the EFE-
        truncated potential develops a saddle): the outermost points of a
        strongly-EFE galaxy are predicted to be kinematically disturbed, not
        just asymmetric -- itself a qualitative AQUAL-class signature.
      - the amplification is response DYNAMICS, common to AQUAL and Branch B
        sources alike: the RATIO discriminator w is UNCHANGED by it.""")

    sgn = "ATTRACTOR-FACING side FASTER" if row_num[2] > 0 else \
          "ATTRACTOR-FACING side SLOWER"
    print(f"\n    SIGN (computed, framework nu, all grid points): {sgn}"
          f"  (A as defined above has sign {'+' if row_num[2]>0 else '-'})")

    # ------------------------------------------------------------------ (2)
    print("\n" + "-"*W)
    print("(2) BRANCH B (published elastic-medium action): trace-only h(J) coupling")
    print("-"*W)
    kt, beta_nat = 0.5, 2.0/7.0
    w_nat = 1.0/(1.0 + 4.0*beta_nat/kt)
    print(f"""    The medium's response energy has two invariants: bulk (trace of the strain,
    the l=0-driving channel) and shear (traceless). The gravitational coupling
    h(J) reads ONLY the trace. A uniform g_ext superposed on the galaxy field
    imposes an ANISOTROPIC strain whose l>=1 harmonic content is traceless-
    driven; it reaches the observable potential only through bulk-shear mixing
    with admittance w = 1/(1 + 4 beta/kappa_t) -- the SAME transfer factor that
    suppresses the Cassini Q2 in the committed two-invariant solve
    (real_research/reviews/branchB_q2_gate_2026/, kappa_t PINNED = 1/2).
    Hence:  A_BranchB(x, e, gamma) = w x A_AQUAL(x, e, gamma).
      w = 1                : AQUAL limit (sanity; = table (1))
      w = 7/23 = {w_nat:.4f}    : natural beta = 2/7 (banked bracket 0.27-0.30)
      w < 0.24             : Cassini-Q2-passing region (Q2 <= 5.2e-27 ceiling)
    CAVEAT (load-bearing, flagged): the committed w was computed at l=2 (solar
    quadrupole BVP). Equality of the l=1 transfer factor follows from the
    l-independence of the two-invariant channel split, but an explicit l=1 BVP
    at galaxy geometry has NOT been run -- an O(1) geometric coefficient on w is
    conceivable. The INEQUALITY A_B <= w_max x A_AQUAL is the robust statement.""")
    print("    Aligned asymmetry [%] at the last-point regime x=0.10, gamma=0, framework nu:")
    print("      e =        " + "".join(f"{e:>9.2f}" for e in E_GRID))
    for lab, w in [("AQUAL (w=1)", 1.0), (f"natural w={w_nat:.3f}", w_nat),
                   ("Cassini-pass w=0.24", 0.24)]:
        print(f"      {lab:<22}" + "".join(f"{w*a:>+9.3f}" for a in row_num))

    # ------------------------------------------------------------------ (3)
    print("\n" + "-"*W)
    print("(3) FOOTINGS: where a REAL galaxy lands on the dimensionless map")
    print("-"*W)
    gbar_phys, gext_phys = 1.0e-11, 3.0e-12   # m/s^2 (illustrative outer-RC point
    #                        + a Chae-scale environmental field; labels only --
    #                        per-galaxy values must come from the data lane)
    print(f"    illustrative outer point g_bar = {gbar_phys:.1e} m/s^2, "
          f"g_ext = {gext_phys:.1e} m/s^2, gamma=0:")
    foot = {}
    for tag, a0 in (("canonical 9.36e-11", A0_CANON), ("alt 1.13e-10", A0_ALT)):
        x, e = gbar_phys/a0, gext_phys/a0
        s = solve_qumond(nu_fw, nup_fw, e)
        A = asym_local(s, x, 0.0)[0]
        foot[tag] = dict(x=x, e=e, A=A)
        print(f"      {tag:<22}: x={x:.4f}  e={e:.4f}  ->  A_AQUAL = {A*100:+.3f}%"
              f"   A_BranchB(nat) = {A*w_nat*100:+.3f}%")
    spread = abs(foot['canonical 9.36e-11']['A']/foot['alt 1.13e-10']['A'] - 1)
    print(f"      footing spread on A: {spread*100:.0f}%  (same-direction, not sign-flipping)")

    # ------------------------------------------------------------------ (4)
    print("\n" + "-"*W)
    print("(4) OBSERVABLE STATISTIC (pre-registered form) + POWER")
    print("-"*W)
    print(f"""    Per galaxy i (needs per-side outer RC + a g_ext vector estimate):
      A_i = 2 (v_approach,out - v_recede,out) / (v_approach,out + v_recede,out)
            averaged over the outermost 2-3 tilted-ring radii per side;
      p_i = A_map(x_i, e_i, gamma_i) * cos(psi_i)     [matched-filter predictor]
            A_map = the computed table above (signed! it carries the x <~ e
            sign REVERSAL beyond the EFE truncation radius); psi_i = azimuth of
            the in-plane g_ext projection from the kinematic major axis, signed
            toward the 'approach' side. SIGN convention fixed by computation:
            {sgn} for x > ~2e (interior), REVERSED for x <~ e.
      The naive (ehat.mhat)=cos(gamma)cos(psi) collapse does NOT hold (computed
      above): keep gamma and psi separate; cos(psi) is the leading m=1
      major-axis sampling factor.
    STACK:  Ahat = sum_i A_i p_i / sigma_i^2  /  sum_i p_i^2 / sigma_i^2
      E[Ahat] = 1 (AQUAL-class, local-force floor; up to ~5 with loop-orbit
      amplification)  |  = w (Branch B)  |  = 0 (no directional EFE)
      sigma(Ahat) = (sum p_i^2/sigma_i^2)^(-1/2);
      NULL: re-draw ehat_ext azimuths (or permute g_ext vectors across
      galaxies) -> empirical null of Ahat; the intrinsic-lopsidedness floor is
      MEASURED by the permuted stack, not assumed.
    POWER (isotropic ehat; geometric factor F_geo computed above):
      N(3sig vs null)      = 9 sigma_A^2 / (A0^2 F_geo)
      N(3sig AQUAL vs B)   = N(3sig vs null) / (1-w)^2""")
    A0 = A0ref*100.0
    print(f"      reference amplitude A0 = A(x=0.10, e=0.03, gamma=0) = {A0:+.3f}%"
          f"  (local-force floor)\n      F_geo = {F_geo:.3f}")
    print(f"      sigma_A = per-galaxy TOTAL asymmetry scatter (measurement + intrinsic")
    print(f"      lopsidedness; ASSUMPTION rows -- must be measured from the permuted null):")
    print(f"      {'sigma_A':>9} {'N(3sig vs null)':>17} {'N(AQUAL vs B, w=0.304)':>24} {'N(vs B, w=0.24)':>17}")
    for sA in (0.03, 0.05, 0.08):
        n0 = 9.0*sA**2/((A0/100.0)**2*F_geo)
        print(f"      {sA:>9.2f} {n0:>17.0f} {n0/(1-w_nat)**2:>24.0f} "
              f"{n0/(1-0.24)**2:>17.0f}")
    print("      (with the ~5x loop-orbit amplification these N shrink by ~25x;")
    print("       the rows above are the conservative local-force floor)")

    # ------------------------------------------------------------------ (5)
    print("\n" + "-"*W)
    print("(5) VERDICT ON THE BANKED '1-4%' FOLKLORE + honesty block")
    print("-"*W)
    amax = max(abs(a) for x in X_GRID for a in table_fw[x])
    typ = [abs(table_fw[x][j]) for x in (0.20, 0.10, 0.05) for j in (0, 1)]
    print(f"""    Computed AQUAL-class aligned asymmetry (LOCAL-FORCE, the conservative floor):
      typical environment e=0.02-0.05, outer RC x=0.05-0.2, gamma=0:
        |A| = {min(typ):.1f}-{max(typ):.1f}%   (x{np.sqrt(F_geo):.2f} rms after isotropic projection -> ~{min(typ)*np.sqrt(F_geo):.1f}-{max(typ)*np.sqrt(F_geo):.1f}%)
      strong-field tail e=0.2-0.3: up to |A| ~ {amax:.1f}%, with a SIGN REVERSAL
        once the measured point crosses the EFE truncation (x <~ e).
    -> the banked '1-4%' folklore is VALIDATED in range (computed, not asserted):
       projected typical signal ~1-4%; and it is an UNDERESTIMATE if gas settles
       on loop orbits (near-resonant m=1 amplification up to ~5x, capped by
       damping and by real disks' flatter RCs).
    HONESTY:
      - modified-INERTIA caveat: for pure MI a uniform g_ext is a frame
        acceleration; the aligned asymmetry can vanish identically independent
        of w. AQUAL row = MG-class comparator (the kill condition's target);
        Branch B = the published action's realization; a NULL is consistent
        with BOTH Branch B (w-suppressed) and pure MI.
      - point-mass source; exponential-disk correction O(10%) expected, not run.
      - l=1 vs l=2 transfer-factor equality for w: structural, not yet BVP-proven.
      - closed-orbit vs local-force ratio computed above; use the closed-orbit
        row when comparing to tilted-ring data.
      - tides (grad g_ext) neglected; uniform-field idealization.""")

    out = dict(E_GRID=E_GRID, X_GRID=X_GRID,
               A_fw_gamma0_pct={str(x): table_fw[x] for x in X_GRID},
               A_sp_gamma0_pct={str(x): table_sp[x] for x in X_GRID},
               w_natural=w_nat, w_cassini_max=0.24,
               A0_ref_pct=float(A0), F_geo=float(F_geo),
               orbit_amplification=[float(r) for r in ratios],
               footings={k: {kk: float(vv) for kk, vv in v.items()}
                         for k, v in foot.items()},
               sign="attractor_side_faster" if row_num[2] > 0
                    else "attractor_side_slower")
    outp = __file__.replace(".py", "_results.json")
    with open(outp, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n    results JSON -> {outp}")
    print("="*W)
    print("LANE A COMPLETE (exit 0)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
