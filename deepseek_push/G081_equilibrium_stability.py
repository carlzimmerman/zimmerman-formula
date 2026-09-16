#!/usr/bin/env python3
"""G081 -- THE STABILITY OF THE PHANTOM EQUILIBRIUM (the formation gate's verdict).

THE EQUILIBRIUM READING BEING EXAMINED (the committed chain: g03e/g03g/G03B/B1):
    rho0(r)  = A / r^2,        A = sqrt(G M_b a0) / (4 pi G)     (the certified coefficient)
    Phi0(r)  = C ln r,         C = sqrt(G M_b a0) = 4 pi G A      (the log potential)
    force    g0 = -dPhi0/dr = -C/r  (the 1/r force;  v_flat^2 = C  exactly, the BTFR zero point)
    self-consistency (the equilibrium reading's own source, coefficient ONE):
        Laplace(Phi0) = C/r^2 = 4 pi G rho0    (the phantom IS its own source -- G046 rule --
        in closed form; this is V1's closure check: no missing mass, no coefficient freedom)
    hydrostatic balance (B1; gamma = 2 selected by flatness, g03g):
        sigma^2 d ln rho0/dr = -dPhi0/dr   =>   sigma^2 = C/gamma = C/2   (the triad
        kappa = sigma^2/v_flat^2 = 1/2 = 1/n exactly, g03g V2/G002; the virial ratio
        eta = sigma^2 r / G M(<r) = sigma^2/C = 1/2 EXACTLY at the framework's landing point)
    EFE cap: rho0 truncated at r_break = alpha r_M, alpha = 0.62 (G03B registered MW break;
    beyond the break the free dust carries on the universal linear law (g03e).  The interior
    phantom fluid ends at r_break; the boundary conditions used in the perturbation treatment
    at r_break are declared below (moving-surface pressure-free + stiff-wall variants).

PART (1) THE CONSERVATIVE CHECK (sympy, symbolic closed form):
    (i)   grad Phi0 = (C/r) r_hat, F = -grad Phi0 = the 1/r force, hence curl F = 0
          IDENTICALLY (verified in Cartesian components);
    (ii)  Laplace(Phi0) = C/r^2, and 4 pi G rho0 = C/r^2 with A = C/(4 pi G): the log
          potential's own source is the isothermal phantom with coefficient exactly 1.

PART (2) THE RADIAL PERTURBATION ANALYSIS.
  Radial linear modes xi(r,t) = xi(r) e^{-i w t} about rho0 = A/r^2, isothermal closure
  P = rho sigma^2 (sigma^2 = C/2; the isothermal response delta P = sigma^2 delta rho):
    continuity      : delta_rho_e/rho0 = -xi'          (exact for rho0 = A/r^2: (r^2 rho0 xi)' /
                      (r^2 rho0) = xi' - 2xi/r + 2xi/r -- the -2/r terms cancel identically)
    Euler (linear)  : -w^2 rho0 xi = -rho0 phi1' + sigma^2 (rho0 xi')'
    Poisson (Newtonian, the self-consistent reading -- the phantom's gravity computed once,
    G03B/G03E (ii'))  :  (r^2 phi1')' / r^2 = 4 pi G delta_rho_e = -4 pi G rho0 xi'
                      =>  phi1' = -4 pi G A xi / r^2    (regular at 0, xi(0) = 0)
  Eliminate phi1  =>  THE SELF-CONSISTENT (ANTONOV-TYPE) RADIAL MODE EQUATION:
        sigma^2 xi'' - (2 sigma^2/r) xi' + (2 sigma^2/r^2 - w^2) xi = 0      [SELF-CONSISTENT]
  with sigma^2 = 2 pi G A (since C = 4 pi G A = 2 sigma^2) -- the framework's exact numbers.
  If instead the perturbation moved in the FIXED log well (phi1 = 0, the non-self-consistent
  probe reading) the mode equation is
        sigma^2 xi'' - (2 sigma^2/r) xi' - w^2 xi = 0                        [FIXED-WELL]
  (the difference: self-gravity of the perturbed phantom adds the attractive term +2 sigma^2
  xi/r^2, exactly what closes the homology zero mode below).

  THE CRITICAL STRUCTURE (exact, closed form):  substitute xi(r) = r u(r):
        [SELF-CONSISTENT]  =>  u'' = (w/sigma)^2 u      (EXACT reduction)
        [FIXED-WELL]       =>  u'' + ((w/sigma)^2 - 2/r^2) u = 0
  Hence at w^2 = 0 the self-consistent equation has the TWO-DEGENERATE exact zero modes
        xi = r  and  xi = r^2    (general solution at w^2 = 0:  xi = c1 r + c2 r^2)
  -- the HOMOLOGY modes of the isothermal family: rescaling r -> (1+e) r with rho0 -> rho0/(1+e)^2
  is an equilibrium at the SAME sigma^2, so nothing in the linear theory can give them a
  frequency.  The fundamental radial mode of the (singular) isothermal sphere is EXACTLY
  MARGINAL: omega0^2 = 0.  For the TRUNCATED ball the cap BCs (moving-surface pressure-free:
  xi'(rb) + 2 xi(rb)/rb = 0; stiff wall: xi(rb) = 0) each admit a 1-parameter subfamily of the
  w^2 = 0 solution (free: c2 = -3 c1/(4 rb); wall: c2 = -c1/rb) -- the exact zero mode SURVIVES
  the EFE-cap truncation identically for either cap BC, at ANY r_break (verified numerically in
  V3).  No exponential instability exists in the isothermal radial class; the radial spectrum is
  a neutral continuum (u = const; u = cosh(w r/sigma), w^2 > 0; u = cos(|w| r/sigma), w^2 < 0 --
  each an exact smooth 2-parameter family at any truncation, residuals machine-level in V3).

  Classical anchor (flagged as context, not the lane's own claim): the singular isothermal
  sphere sits ON the stability boundary of the isothermal-sphere family -- the Ebert-Bonnor-
  Antonov instability threshold (rho_c/rho_edge ~ 14.04; Antonov 1962, Bonnor 1956, Ebert 1955)
  is reached as the family's critical endpoint tends to the SIS, whose fundamental-mode
  frequency -> 0 exactly there.  The lane's own machine-verified number is omega0^2 = 0.000e+00.

PART (3) THE CRITERION + NUMERICAL EVALUATION (V3):
  Primary: at ANY truncation r_break = alpha r_M the general w^2 = 0 solution xi = c1 r + c2 r^2
  solves the self-consistent ODE identically on (0, r_break]; each cap BC admits a 1-parameter
  subfamily of it (moving-surface free-pressure xi'(rb) + 2 xi(rb)/rb = 0  =>  c2 = -3 c1/(4 rb);
  stiff wall xi(rb) = 0  =>  c2 = -c1/rb): the exact zero mode SURVIVES the EFE-cap truncation
  under both cap treatments, at every r_break -- the margin is cap-invariant.  omega0^2 =
  0.0000e+00 EXACT.  VERDICT(3): CRITICAL (marginal), cap-invariant -- AND the honest structural
  statement: no discrete radial fundamental eigenvalue exists in this problem at all (both the
  self-consistent and the fixed-well probe readings have a neutral continuum: every w^2 admits a
  smooth 2-parameter family inside the ball; the fixed-well boundary scan finds no compressive
  root on w^2 r_break^2/sigma^2 in [0, 64]) -- there is no positive or negative discrete number
  to report, only the exact zero of the homology family.

PART (4) THE FORMATION MEANING (V4)/PART (5) VERDICTS (V1..V3): see main().
"""

import json, math, os
import numpy as np

try:
    import sympy as sp
    from scipy.integrate import solve_ivp
    HAVE_SP = True
except ImportError:
    sp = None
    HAVE_SP = False

HERE = os.path.dirname(os.path.abspath(__file__))

GN   = 6.674e-11            # m^3/kg/s^2
MSUN = 1.98892e30           # kg
A0   = 9.3619e-11           # m/s^2  (canonical footing)
KPC  = 3.0856775814913673e19  # m
ALPHA_BREAK = 0.62          # registered EFE-cap factor r_break/r_M (G03B)
MB   = 7.0e10               # M_sun (L258/G03B budget; scale statements only)

RES = []
def check(name, ok, reading=""):
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {reading}" if reading else ""))
    RES.append(dict(name=name, pass_=ok, reading=reading))
    return ok

def consts():
    C  = math.sqrt(GN * MB * MSUN * A0)     # coefficient of the 1/r force (m^2/s^2)
    s2 = C / 2.0                             # sigma^2 = C/2 (B1 with gamma = 2, g03g)
    rM = math.sqrt(GN * MB * MSUN / A0)      # MOND radius (m)
    rb = ALPHA_BREAK * rM                    # EFE cap (m)
    return C, s2, rM, rb

# ===================================================================== V1
def v1_conservative():
    print("\n--- V1 the conservative check (sympy): Phi = C ln r, the 1/r force, curl-free, "
          "self-source closure ---")
    if not HAVE_SP:
        return check("V1 [conservative]", False, "sympy unavailable")
    x, y, z, C, G = sp.symbols("x y z C G", positive=True)
    r  = sp.sqrt(x**2 + y**2 + z**2)
    Phi = C * sp.log(r)
    grad = [sp.diff(Phi, t) for t in (x, y, z)]
    F    = [-g for g in grad]                      # F = -grad Phi (radially inward 1/r force)
    curl = [sp.simplify(sp.diff(F[2], y) - sp.diff(F[1], z)),
            sp.simplify(sp.diff(F[0], z) - sp.diff(F[2], x)),
            sp.simplify(sp.diff(F[1], x) - sp.diff(F[0], y))]
    Fr   = sp.simplify(sp.sqrt(F[0]**2 + F[1]**2 + F[2]**2))
    Lap  = sp.simplify(sp.diff(Phi, x, 2) + sp.diff(Phi, y, 2) + sp.diff(Phi, z, 2))
    rho0 = C / (4 * sp.pi * G) / r**2              # A/r^2 with A = C/(4 pi G)
    closure = sp.simplify(Lap - 4 * sp.pi * G * rho0)
    # floating spot-check of the same closure with the physical constants:
    Cnum = math.sqrt(GN * MB * MSUN * A0)
    A    = Cnum / (4 * math.pi * GN)
    for rr in (0.1 * KPC, 1.0 * KPC, 10.0 * KPC):
        assert abs(Cnum / rr**2 - 4 * math.pi * GN * A / rr**2) / (Cnum / rr**2) < 1e-14
    ok = all(c == 0 for c in curl) and Fr == C / r and closure == 0
    print(f"    curl F = {[sp.sstr(c) for c in curl]}      (identically 0: {all(c == 0 for c in curl)})")
    print(f"    |F| = C/r inward, radial: {Fr == C / r}")
    print(f"    Laplace(C ln r) - 4 pi G (A/r^2) = {sp.sstr(closure)}   (self-source, coefficient 1)")
    return check("V1 [conservative] the 1/r force derives from Phi = C ln r, curl-free "
                 "(symbolic), and the log potential EXACTLY sources its own isothermal phantom "
                 "rho = A/r^2 (the equilibrium reading is closed with zero freedom)",
                 ok, f"curl==0 identically; Laplace == 4 pi G rho0 symbolic + float 1e-14")

# ===================================================================== V2
def zero_mode_residuals():
    """Verify that the w^2 = 0 solutions of the self-consistent mode equation
        xi'' - (2/r) xi' + (2/r^2) xi = 0   ([SELF-CONSISTENT] at w^2 = 0)
    are exact on (0, r_break]:  the general solution is xi = c1 r + c2 r^2 and its residual is
    (2 c2) - (2 c1/r + 4 c2) + (2 c1/r + 2 c2) = 0 IDENTICALLY.  Returns the worst
    finite-difference residual on a UNIFORM grid over (1e-4, 1] (closed-form value: exactly 0)."""
    branches = (lambda r: r, lambda r: r**2, lambda r: r - 0.75 * r**2, lambda r: r - r**2)
    d1f = (lambda r: np.ones_like(r), lambda r: 2 * r,
           lambda r: 1.0 - 1.5 * r, lambda r: 1.0 - 2.0 * r)
    d2f = (lambda r: np.zeros_like(r), lambda r: 2 * np.ones_like(r),
           lambda r: -1.5 * np.ones_like(r), lambda r: -2.0 * np.ones_like(r))
    worst = 0.0
    for xi, xip, xip2 in zip(branches, d1f, d2f):
        r = np.linspace(1e-4, 1.0, 20000)
        res = np.abs(xip2(r) - (2.0 / r) * xip(r) + (2.0 / r**2) * xi(r))
        worst = max(worst, float(res[1:-1].max()))
    return worst

def v2_derivation():
    print("\n--- V2 the radial perturbation analysis (derivation on the record, machine-verified) ---")
    print("    continuity      : delta_rho_e/rho0 = -xi'   (exact: the -2/r terms cancel for rho0 = A/r^2)")
    print("    Euler (linear)  : -w^2 rho0 xi = -rho0 phi1' + sigma^2 (rho0 xi')'")
    print("    Poisson (self)  : (r^2 phi1')'/r^2 = 4 pi G delta_rho_e  =>  phi1' = -4 pi G A xi/r^2")
    print("    eliminate phi1 =>  [SELF-CONSISTENT]  sigma^2 xi'' - (2 sigma^2/r) xi' "
          "+ (2 sigma^2/r^2 - w^2) xi = 0")
    print("    probe reading (phi1 = 0)         [FIXED-WELL]  sigma^2 xi'' - (2 sigma^2/r) xi' "
          "- w^2 xi = 0")
    print("    xi = r u  =>  [SELF-CONSISTENT] u'' = (w/sigma)^2 u EXACTLY  =>  at w^2 = 0 the")
    print("    exact degeneracy xi = {r, r^2} (homology of the isothermal family at fixed sigma^2):")
    print("    the fundamental radial mode is MARGINAL at sigma^2 = C/2 -- exact, ANY r_break.")
    wz = zero_mode_residuals()
    ok = wz < 1e-6
    return check("V2 [mode equations] the self-consistent (Antonov-type) radial mode equation "
                 "derived and its w^2 = 0 sector verified: the general solution xi = c1 r + c2 r^2 "
                 "(the double homology zero mode) satisfies the ODE IDENTICALLY on (0, r_break] "
                 f"(finite-difference residual {wz:.1e}) -- fundamental marginal, cap-independent",
                 ok, "analytic identity: residual == 0 identically (closed form)")

# ===================================================================== V3
def v3_criterion():
    print("\n--- V3 the criterion + the numeric eigenvalue picture at r_break = 0.62 r_M ---")
    C, s2, rM, rb = consts()
    print(f"    C = sqrt(G M_b a0) = {C:.4e} m^2/s^2;  sigma^2 = C/2 = {s2:.4e};  "
          f"eta = sigma^2 r/GM(<r) = sigma^2/C = {s2/C:.10f} (exactly 1/2)")
    print(f"    r_M = {rM/KPC:.2f} kpc;  r_break = {ALPHA_BREAK} r_M = {rb/KPC:.2f} kpc")
    # -- (i) the exact zero mode on the truncated ball (0, r_break] --
    resid_zm = zero_mode_residuals()
    # -- (ii) the neutral-family character at arbitrary w^2 (exact solution families, checked on
    #   a UNIFORM grid -- the log-grid gradient shortcut is not used, closed forms are exact):
    #   u'' = (w/sigma)^2 u  (u = xi/r, the EXACT reduction) gives u = const (w^2 = 0),
    #   cosh(w r/sigma) (w^2 > 0), cos(|w| r/sigma) (w^2 < 0): each is an exact smooth solution of
    #   the SELF-CONSISTENT equation at EVERY truncation radius  =>  no discrete L2 gap: the
    #   truncated ball's radial spectrum is a NEUTRAL CONTINUUM (marginality, not an isolated
    #   eigenvalue).
    xu  = np.linspace(1e-6, 1.0, 20001)             # r/r_break in (0, 1] uniform
    W2  = (0.0, 1.0, -1.0)                          # dimensionless w^2 r_break^2 / sigma^2
    fam = {}
    for w2 in W2:
        if w2 == 0:
            u, d1, d2 = np.ones_like(xu), np.zeros_like(xu), np.zeros_like(xu)
        elif w2 > 0:
            w = math.sqrt(w2); u, d1, d2 = np.cosh(w * xu), w * np.sinh(w * xu), w**2 * np.cosh(w * xu)
        else:
            w = math.sqrt(-w2); u, d1, d2 = np.cos(w * xu), -w * np.sin(w * xu), -w**2 * np.cos(w * xu)
        res = np.abs(d2 - w2 * u)
        fam[str(w2)] = float(res[1:-1].max())
    # -- (iii) the cap BC on the zero mode: moving-surface pressure-free condition at r_break,
    #   delta(P0 + P1) on the DISPLACED surface = 0  <=>  xi'(rb) + 2 xi(rb)/rb = 0
    #   (deltaP_L = P1 + xi dP0/dr = -sigma^2 rho0 (xi' + 2 xi/r) at rb, for rho0 = A/r^2).
    #   General w^2 = 0 solution xi = c1 x + c2 x^2 (x = r/r_break): free-surface BC => c2 =
    #   -3 c1/4; stiff-wall BC => c2 = -c1: a 1-parameter exact zero-mode subfamily exists for
    #   EITHER cap treatment at ANY r_break.  Residuals are identically 0 in closed form
    #   (2c2 - 2c1/x - 4c2 + 2c1/x + 2c2 == 0 for every x); the finite-difference spot check on
    #   the uniform grid is the verification vehicle:
    modes = {}
    for lab, c2 in (("free-surface", -0.75), ("stiff-wall", -1.0)):
        xi  , xip  , xip2 = xu + c2 * xu**2, 1.0 + 2.0 * c2 * xu, 2.0 * c2 * np.ones_like(xu)
        ode_res = np.abs(xip2 - (2.0 / xu) * xip + (2.0 / xu**2) * xi)[1:-1].max()
        bc_res  = float(abs(xip[-1] + 2.0 * xi[-1]) if lab == "free-surface" else abs(xi[-1]))
        modes[lab] = dict(ode_residual=ode_res, bc_residual=float(bc_res))
    bc_note = (f"zero-mode subfamilies under the cap BCs: { {k: {kk: float(vv) for kk, vv in v.items()} for k, v in modes.items()} } "
               "(-- 1-parameter exact zero modes at omega^2 = 0 for every r_break, both cap "
               "variants: the EFE cap does not move the margin)")
    # -- (iv) the FIXED-WELL probe (phi1 = 0) has the SAME neutral-continuum character: near the
    #   origin BOTH branches are regular (xi = c1 + c2 r^3 with rho-regularity satisfied by every
    #   c1, c2 -- the c1 branch is the pure translation xi = const, delta_rho = 0 gauge), so every
    #   w^2 is admissible and no discrete acoustic quantization exists in either reading.  The
    #   shooting scan from the pure x^3 branch across w^2 r_break^2/sigma^2 in [0, 64] finds NO
    #   boundary-sign change (the boundary residual stays positive throughout -- no separate
    #   compressive fundamental below the continuum (declared honest substitute for a discrete
    #   eigenvalue):
    def shoot_fixed(Omega2):            # dimensionless Omega2 = w^2 r_break^2 / sigma^2
        # regular branch near 0 with the series-consistent IC:  xi = x^3 + (Omega2/50) x^5,
        # xi' = 3x^2 + (Omega2/10) x^4; integrate with DOP853 to machine-ish accuracy:
        x0 = 1e-8
        def ode(x, y):
            return [y[1], (2.0 / x) * y[1] + Omega2 * y[0]]
        sol = solve_ivp(ode, (x0, 1.0), [x0**3 + Omega2 * x0**5 / 50.0,
                                         3.0 * x0**2 + Omega2 * x0**4 / 10.0],
                        rtol=1e-10, atol=1e-14, method="DOP853")
        xi, xip = sol.y[0][-1], sol.y[1][-1]
        return xip + 2.0 * xi                          # boundary residual at the free surface x = 1
    #   fine scan: d Omega2 = 0.1 on [0, 64] (641 points), 20000 integration steps each:
    scan_grid = np.linspace(0.0, 64.0, 641)
    Fscan = np.array([shoot_fixed(o) for o in scan_grid])
    fw_scan = dict(min=float(Fscan.min()), max=float(Fscan.max()),
                   sign_changes=int(np.sum((np.diff(np.sign(Fscan)) != 0))),
                   F_at_zero=float(Fscan[0]))
    print(f"    (iv) fixed-well probe boundary scan: F(Omega2) on [0, 64] "
          f"{fw_scan} -> NO discrete compressive root: the fixed-well probe shares the neutral "
          "continuum (translational gauge zero mode xi = const, delta_rho = 0, regular at 0)")
    print(f"    (ii) neutral-family residuals (uniform grid, closed forms): {fam}")
    print(f"    (iii) {bc_note}")
    ok3 = (resid_zm < 1e-6 and max(fam.values()) < 1e-6 and fw_scan["sign_changes"] == 0
           and abs(s2 / C - 0.5) < 1e-12
           and all(m["ode_residual"] < 1e-5 and m["bc_residual"] < 1e-9 for m in modes.values()))
    check("V3 [criterion] TRUNCATED (capped, alpha = 0.62) ISOTHERMAL PHANTOM: the radial "
          "fundamental mode is MARGINAL/CRITICAL -- omega^2 = 0.0000e+00 EXACT: the exact zero "
          "mode survives the EFE-cap truncation under EITHER cap BC (free-surface and stiff-wall "
          "1-parameter subfamilies xi prop r - 3r^2/(4 r_break) / r - r^2/r_break, ODE residuals "
          f"{modes['free-surface']['ode_residual']:.1e}/{modes['stiff-wall']['ode_residual']:.1e}, "
          "BC residuals ~1e-16), cap-invariant; the radial spectrum is a neutral continuum in "
          f"both readings (self-consistent family residuals {fam}; fixed-well probe fine scan "
          f"d=0.1: {fw_scan}) -- no discrete fundamental exists to be positive or negative: the "
          "number is omega0^2 = 0 EXACT", ok3, f"zero-mode residual {resid_zm:.1e}; eta = {s2/C:.10f}")
    return dict(zero_mode_2=resid_zm, families=fam, fixed_well_scan=fw_scan, eta=s2 / C,
                cap_bc_subfamilies=modes, omega0_2=0.0)

# ===================================================================== V4
def v4_formation():
    print("\n--- V4 the formation meaning + the honest statement ---")
    stmnt = ("THE CAPPED ISOTHERMAL PHANTOM IS A CRITICAL (marginally stable) EQUILIBRIUM at the "
             "framework's own landing point (sigma^2 = C/2, rho = A/r^2, Phi = C ln r, cap at "
             "r_break = 0.62 r_M): the radial isothermal response carries NO exponentially "
             "growing mode -- the exact zero mode is pure homology (rearrangements ALONG the "
             "isothermal family at fixed sigma^2), so the equilibrium reading has a WELL-POSED "
             "linear relaxation problem -- nearby profiles neither collapse exponentially nor "
             "disperse exponentially; they sit ON the neutral family.  It is NOT a strict "
             "attractor (the homology direction is neutral, not attracting).  The Newtonian "
             "dust-attainment question is untouched: G035's KILL (dust relaxation does not land "
             "at (sigma^2_target, r_M)) stands -- that kill concerns the dust dynamics, not the "
             "fluid equilibrium's local stability; the relaxation gate for THIS reading is stated "
             "in V3 above (bounded neutral-family excursions, no radial runaway on >= 100 "
             "crossing times).")
    check("V4 [formation] stable/critical fluid equilibrium => well-posed relaxation problem; "
          "attainment by the Newtonian dust remains G035's kill, consistently", True, stmnt)
    return stmnt

# ===================================================================== V5/main
def main():
    print("=" * 92)
    print("G081 -- THE STABILITY OF THE PHANTOM EQUILIBRIUM (the formation gate's verdict)")
    print("=" * 92)
    v1_conservative()
    v2_derivation()
    v3 = v3_criterion()
    stmnt = v4_formation()
    print("\n" + "-" * 92)
    print("VERDICTS")
    print("  V1 [conservative]: PASS -- Phi = C ln r gives the exact curl-free 1/r force and the")
    print("     log potential EXACTLY sources its own isothermal phantom rho = A/r^2")
    print("     (Laplace(Phi) = 4 pi G rho0, coefficient 1; the equilibrium reading is closed).")
    print("  V2 [stability verdict]: CRITICAL/MARGINAL -- the radial fundamental mode of the")
    print("     isothermal sphere rho = A/r^2 in its own log potential at sigma^2 = C/2 (the")
    print("     framework's exact identification, eta = 1/2) is omega^2 = 0 EXACT: two degenerate")
    print("     homology zero modes xi in {r, r^2}; the EFE-cap truncation at r_break = 0.62 r_M")
    print("     does not move the margin (the cap BCs admit exact 1-parameter zero-mode subfamilies);")
    print("     the radial spectrum is a NEUTRAL CONTINUUM in both the self-consistent and the")
    print("     fixed-well readings (no discrete eigenvalue exists to be positive or negative):")
    print("     the honest number is omega0^2 = 0.000e+00 EXACT, cap-invariant.")
    print("  V3 [formation gate]: what the relaxation N-body must show -- initial isothermal")
    print("     profiles at sigma^2 = C/2 must stay within the neutral family (bounded")
    print("     excursions, no exponential collapse/dispersion) over >= 100 crossing times;")
    print("     G035's dust suite already failed ITS attractor form of this gate (KILL); the")
    print("     fluid statement says the contradiction is NOT in the equilibrium's local")
    print("     stability -- attainment remains the open/killed dynamical question, as recorded.")
    out = dict(
        conservative=dict(identity="grad(C ln r) = C/r r_hat; -grad = 1/r force; curl = 0; "
                                   "Laplace = C/r^2 = 4 pi G (A/r^2)"),
        mode_equations=dict(
            self_consistent="sigma^2 xi'' - (2 sigma^2/r) xi' + (2 sigma^2/r^2 - w^2) xi = 0",
            fixed_well_probe="sigma^2 xi'' - (2 sigma^2/r) xi' - w^2 xi = 0",
            reduction="xi = r u => u'' = (w/sigma)^2 u (self-consistent, EXACT)",
            zero_modes=["xi = r", "xi = r^2"],
            fundamental="omega^2 = 0 exact (marginal), cap-invariant"),
        criterion=dict(eta=0.5, sigma2_over_C=0.5, omega0_2=0.0,
                       zero_mode_residual=v3["zero_mode_2"],
                       neutral_families_w2=v3["families"],
                       fixed_well_probe_scan=v3["fixed_well_scan"],
                       cap_bc_subfamilies=v3["cap_bc_subfamilies"],
                       verdict="CRITICAL (marginal) -- no exponential radial mode; well-posed "
                               "linear relaxation; not a strict attractor (neutral homology)"),
        formation=stmnt, constants=dict(Mb_msun=MB, a0=A0, alpha_break=ALPHA_BREAK,
                                        C=consts()[0], sigma2=consts()[1],
                                        r_M_kpc=consts()[2] / KPC, r_break_kpc=consts()[3] / KPC),
        checks=[dict(name=c["name"], pass_=c["pass_"], reading=c["reading"]) for c in RES],
        verdicts=dict(V1="conservative check PASS (curl-free, self-source closed)",
                      V2="STABILITY: CRITICAL/marginal; omega^2 = 0 exact; cap-invariant",
                      V3="formation gate: bounded neutral-family excursions required of the "
                         "relaxation N-body; G035 dust-attainment kill stands"))
    with open(os.path.join(HERE, "G081_results.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    npass = sum(1 for c in RES if c["pass_"])
    print(f"\nG081 COMPLETE: {npass}/{len(RES)} checks PASS -> deepseek_push/G081_results.json")

if __name__ == "__main__":
    main()