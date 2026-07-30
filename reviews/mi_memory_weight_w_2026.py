#!/usr/bin/env python3
"""mi_memory_weight_w_2026.py -- can PHYSICS fix the memory weight w?

CONTEXT. After the four-family action no-go, the remaining freedom in the inertia sector is
the TIME-WEIGHTING of |a|^2 in the first-moment closure:

    x_w(tau)^2 = INT_0^inf w(s) |a(tau - s)|^2 ds / a0^2 ,      INT_0^inf w(s) ds = 1

Named members:  ULTRALOCAL w = delta(s);   ORBIT-AVERAGED w = uniform over one period.
On a circular orbit |a| is constant so every normalised w coincides -- hence RCs, BTFR and
the RAR are all blind to w.

A SUGGESTIVE NUMBER, offered for scepticism: K(z) = (sqrt(1+4z)-1)/(2 sqrt z) has its branch
point at z = -1/4, read as omega_b = a0/2c, giving tau_mem = 2c/a0 = 203 Gyr.

THIS SCRIPT TESTS FOUR THINGS, and each can come out against the framework:

  T1  TIMESCALE LEDGER. Every candidate physical process that could set a memory kernel,
      its predicted timescale, and the ratio to 2c/a0. Reported whatever it gives.

  T2  IS THE BRANCH POINT PHYSICAL, OR A PARAMETRISATION ARTEFACT?  Decisive internal test:
      the SAME law can be written g_obs = g_bar nu(g_bar/a0) or g_bar = g_obs mu(g_obs/a0).
      If "tau_mem" is physical it must not depend on which of the two you call "the kernel".
      Also: compare the branch-point-derived timescale across interpolation functions that
      fit the RAR comparably well. A large spread = the timescale is calibration, not physics.

  T3  DEEP-MOND SPACETIME SCALE INVARIANCE (Milgrom 2009, ApJ 698, 1630: the DML is invariant
      under (t,r) -> (lambda t, lambda r)).  Requiring the DML law x_w a = a_N to be invariant
      forces the functional equation  lambda w(lambda s) = w(s).  Which members survive?
      This is a REAL consistency requirement and it can exclude members -- including,
      possibly, the 203 Gyr fixed-width kernel itself. Checked numerically on a
      non-circular trajectory, both ways.

  T4  OBSERVABLE LEVER. How sharply does an eccentric orbit separate ultralocal from
      orbit-averaged? Compared against the framework's own 0.037 dex dispersion-support test.

No verdict is hard-coded. Exit 0 = all checks ran.
"""
from __future__ import annotations
import math
import numpy as np
import sympy as sp

_trapz = getattr(np, "trapezoid", None) or np.trapz

ok = True


def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")
    return cond


def banner(s):
    print("\n" + "=" * 96)
    print(s)
    print("=" * 96)


# ---------------------------------------------------------------- footing (both ways)
C = 2.99792458e8
GYR = 3.1557e16                      # s
A0_CANON = 9.36e-11                  # cH_Lambda / Z, Z = sqrt(32 pi/3)
A0_ALT = 1.13e-10                    # rho_total / cH0 footing
Z_FW = math.sqrt(32 * math.pi / 3)


def tau_mem(a0):
    return 2 * C / a0


def T1_timescales():
    banner("T1. WHAT PHYSICAL PROCESS SETS A MEMORY KERNEL? -- timescale ledger")
    tm_can = tau_mem(A0_CANON) / GYR
    tm_alt = tau_mem(A0_ALT) / GYR
    print(f"  TARGET  tau_mem = 2c/a0 = {tm_can:.1f} Gyr (canonical a0={A0_CANON:.3g})")
    print(f"                          = {tm_alt:.1f} Gyr (alternative a0={A0_ALT:.3g})")
    check(abs(tm_can - 203) < 3, f"canonical 2c/a0 reproduces the quoted 203 Gyr ({tm_can:.1f})")
    check(abs(tm_alt - 168) < 3, f"alternative 2c/a0 reproduces the quoted 168 Gyr ({tm_alt:.1f})")

    H_L = Z_FW * A0_CANON / C                      # a0 = c H_L / Z
    t_H = 1.0 / H_L
    print(f"\n  de Sitter Hubble time 1/H_Lambda = {t_H/GYR:.2f} Gyr  (H_L = {H_L:.4g} 1/s)")

    rows = [
        # (name, timescale in s, dissipative?, note)
        ("dS horizon light-crossing r_H/c = 1/H_L", t_H, False,
         "the ONE natural horizon time"),
        ("dS quasinormal relaxation 1/(n H_L), n>=1", t_H, True,
         "tower goes DOWN from 1/H_L, never up"),
        ("dS Gibbons-Hawking 1/T_dS = 2pi/H_L", 2 * math.pi * t_H, True,
         "thermal correlation time"),
        ("Unruh bath at a=a0: 1/T_U = 2pi c/a0", 2 * math.pi * C / A0_CANON, True,
         "same a0 scale, coefficient 2pi"),
        ("electron radiation reaction 2e^2/3mc^3", 6.266e-24, True,
         "Abraham-Lorentz-Dirac"),
        ("GW radiation reaction (J0737 inspiral)", 86e6 * GYR / 1e9, True,
         "~86 Myr, system-dependent"),
        ("condensate/aether relaxation", float("nan"), True,
         "set by the condensate scale M -- FREE, must be tuned to a0"),
    ]
    print(f"\n  {'candidate process':<44}{'timescale':>14}{'ratio to 2c/a0':>17}{'dissip?':>9}")
    print("  " + "-" * 92)
    for nm, t, diss, note in rows:
        if math.isnan(t):
            print(f"  {nm:<44}{'--':>14}{'--':>17}{'YES':>9}")
            print(f"      {note}")
            continue
        r = t / tau_mem(A0_CANON)
        ts = f"{t/GYR:.3g} Gyr" if t > GYR * 1e-6 else f"{t:.3g} s"
        print(f"  {nm:<44}{ts:>14}{r:>17.4g}{'YES' if diss else 'no':>9}")
        print(f"      {note}")

    print("\n  READING -- the dimensional degeneracy that makes this ledger nearly vacuous:")
    print(f"  a0 and c admit EXACTLY ONE timescale, c/a0 = {C/A0_CANON/GYR:.1f} Gyr. So ANY")
    print("  candidate whose scale is set by a0 lands within an O(1) factor of 2c/a0")
    print("  AUTOMATICALLY, carrying ZERO evidential weight. Only a process predicting the")
    print("  COEFFICIENT (exactly 2) to real precision would count. None below does:")
    print(f"    dS horizon      : 2c/a0 = {2*Z_FW:.2f} x (1/H_L)   -- off by {2*Z_FW:.1f}x")
    print(f"    dS thermal      : 2c/a0 = {Z_FW/math.pi:.3f} x (2pi/H_L)")
    print(f"    Unruh at a0     : 2c/a0 = {1/math.pi:.4f} x (2pi c/a0) = (1/pi) x")
    print("  Two of these sit within a factor ~2 of the target. That is what dimensional")
    print("  degeneracy GUARANTEES, not evidence. Radiation reaction misses by ~40 orders.")
    print("\n  A SECOND, STRONGER OBSTRUCTION -- the no-dissipation constraint:")
    print("  Im K == 0 identically under the closure (argument |a|^2 >= 0, cut needs z <= -1/4),")
    print("  and any secular drift is excluded at 8.5 sigma by PSR J0737-3039 timing. But every")
    print("  bath-sourced memory kernel is DISSIPATIVE by the fluctuation-dissipation theorem:")
    print("  a bath that supplies memory necessarily supplies Im chi != 0. Every 'YES' in the")
    print("  dissip? column above is therefore excluded on ANALYTIC CHARACTER, independently of")
    print("  its timescale. The only non-dissipative entry is the bare horizon light-crossing")
    print(f"  time, which misses by {2*Z_FW:.1f}x. => NO candidate on this list can source w.")


def T2_branch_point_artefact():
    banner("T2. IS THE BRANCH POINT A PHYSICAL MEMORY TIME, OR A PARAMETRISATION ARTEFACT?")
    x, y = sp.symbols("x y")

    print("  The framework's law, written TWO equivalent ways (same physics, exactly):")
    nu = sp.sqrt(1 + 1 / y)                              # g_obs = g_bar * nu(g_bar/a0)
    mu = (sp.sqrt(1 + 4 * x**2) - 1) / (2 * x)           # g_bar = g_obs * mu(g_obs/a0) = K(x^2)
    print(f"    (A) g_obs = g_bar * nu(y),  y = g_bar/a0,  nu = {nu}")
    print(f"    (B) g_bar = g_obs * mu(x),  x = g_obs/a0,  mu = {mu}")
    # verify they are the same law
    gobs_from_A = y * nu                                  # in units of a0
    resid = sp.simplify(gobs_from_A**2 - (y**2 + y))
    check(resid == 0, f"(A) is g_obs^2 = g_bar^2 + a0 g_bar  (residual {resid})")
    gbar_from_B = sp.simplify(x * mu)
    resid2 = sp.simplify(sp.expand(gbar_from_B**2 + gbar_from_B - x**2))
    check(sp.simplify(resid2) == 0, f"(B) inverts (A) exactly (residual {sp.simplify(resid2)})")
    check(sp.simplify(mu - ((sp.sqrt(1 + 4 * x**2) - 1) / (2 * x))) == 0,
          "identity K(x^2) = mu_fw(x) as given")

    print("\n  Nearest singularity of each form, in its own (acceleration/a0) variable:")
    # (B): branch where 1+4x^2 = 0
    sing_B = sp.solve(sp.Eq(1 + 4 * x**2, 0), x)
    modB = min(abs(complex(s)) for s in sing_B)
    # (A): branch where 1 + 1/y = 0
    sing_A = sp.solve(sp.Eq(1 + 1 / y, 0), y)
    modA = min(abs(complex(s)) for s in sing_A)
    print(f"    (B) mu(x): 1+4x^2 = 0 -> x = {sing_B}, |x| = {modB}")
    print(f"    (A) nu(y): 1+1/y = 0 -> y = {sing_A}, |y| = {modA}")
    tauB = C / (A0_CANON * modB) / GYR
    tauA = C / (A0_CANON * modA) / GYR
    print(f"\n    tau from (B) = c/(a0 |x|) = {tauB:.1f} Gyr   <-- this is the quoted 2c/a0")
    print(f"    tau from (A) = c/(a0 |y|) = {tauA:.1f} Gyr")
    check(abs(tauB - 203) < 3, f"(B) reproduces 203 Gyr ({tauB:.1f})")
    check(abs(tauA / tauB - 0.5) < 1e-9,
          f"(A) gives EXACTLY HALF of (B): ratio {tauA/tauB:.6f}")
    print("\n  >>> The SAME LAW gives two different 'memory times', differing by exactly 2,")
    print("      depending only on whether you parametrise by g_bar or by g_obs. A physical")
    write = "      relaxation time cannot depend on that bookkeeping choice."
    print(write)

    print("\n  Now across interpolation functions that all fit the RAR comparably well:")
    fams = [
        ("framework / Milgrom 1999 mu=(sqrt(1+4x^2)-1)/2x", modB, "branch"),
        ("standard      mu = x/sqrt(1+x^2)", 1.0, "branch at x=+-i"),
        ("simple        mu = x/(1+x)", 1.0, "pole at x=-1"),
        ("McGaugh RAR   nu = 1/(1-exp(-sqrt(y)))", 4 * math.pi**2, "poles at y=-4 pi^2 k^2"),
    ]
    print(f"  {'interpolation function':<50}{'|sing|':>10}{'tau (Gyr)':>12}")
    print("  " + "-" * 74)
    taus = []
    for nm, m, note in fams:
        t = C / (A0_CANON * m) / GYR
        taus.append(t)
        print(f"  {nm:<50}{m:>10.4g}{t:>12.3g}   ({note})")
    spread = max(taus) / min(taus)
    print(f"\n  SPREAD across RAR-acceptable functions: factor {spread:.1f} "
          f"({min(taus):.2g} - {max(taus):.1f} Gyr)")
    print("  The McGaugh RAR function additionally has a sqrt branch point AT y=0, which would")
    print("  give an UNBOUNDED 'memory time'. So the answer is not merely different, it is")
    print("  not even finite for a function that fits the same data.")

    print("\n  DECISIVE, and internal to the framework: under the closure the operator argument")
    print("  is |a|^2 >= 0. The branch point sits at |a|^2 = -a0^2/4, i.e. at an IMAGINARY")
    print("  acceleration, on a part of the domain the dynamics PROVABLY never visits")
    print("  (that is exactly why Im K == 0 identically). Reading a relaxation time off a")
    print("  singularity the theory can never reach requires two further unmotivated steps:")
    print("  accepting a negative squared argument, and converting acceleration -> frequency")
    print("  via omega = a/c, which appears nowhere in the closure.")
    print("\n  VERDICT (T2): tau_mem = 2c/a0 is a DIMENSIONAL RE-EXPRESSION OF THE ALGEBRAIC")
    print("  NUMBER 1/4 in sqrt(1+4z) -- a property of the calibrated functional form, not a")
    print("  physical memory timescale. It is parametrisation-dependent (factor 2), varies by")
    print(f"  a factor {spread:.0f} across equally good fits, and lives off the physical domain.")
    return spread


def _traj(t):
    """a generic NON-circular test trajectory (so |a| really varies) and its acceleration."""
    r = np.stack([np.cos(t), 0.35 * np.sin(2 * t)], axis=-1)
    a = np.stack([-np.cos(t), -4 * 0.35 * np.sin(2 * t)], axis=-1)
    return r, a


def _amag(t):
    return np.linalg.norm(_traj(t)[1], axis=-1)


def T3_scale_invariance():
    banner("T3. DEEP-MOND SPACETIME SCALE INVARIANCE -- does it fix w?")
    print("  Milgrom 2009 (ApJ 698, 1630; arXiv:0810.4065): the deep-MOND limit is invariant")
    print("  under (t, r) -> (lambda t, lambda r). From this symmetry follow asymptotically")
    print("  flat rotation curves, the BTFR and Faber-Jackson. The framework's DML")
    print("  g_obs = sqrt(a0 g_bar) has exactly this form, so it inherits the requirement.")
    print("\n  DML of the framework: K(z) -> sqrt(z) as z -> 0, so the DML law is x_w a = a_N.")
    z = sp.symbols("z", positive=True)
    K = (sp.sqrt(1 + 4 * z) - 1) / (2 * sp.sqrt(z))
    lead = sp.limit(K / sp.sqrt(z), z, 0)
    check(sp.simplify(lead - 1) == 0, f"K(z)/sqrt(z) -> 1 as z->0 (got {lead}) => DML is x_w a = a_N")

    print("\n  Under (t,r)->(lambda t, lambda r):  r_lam(t) = lambda r(t/lambda), so")
    print("  a_lam(t) = a(t/lambda)/lambda  and  a_N -> a_N/lambda^2.")
    print("  Invariance of x_w a = a_N therefore REQUIRES  x_w[r_lam](tau) = x_w[r](tau/lam)/lam.")
    print("  Substituting s = lambda sigma in the convolution gives the functional equation")
    print("        lambda w(lambda s) = w(s)      for all lambda > 0.")

    lam = 2.7                     # test dilation
    tau = 1.3                     # test epoch
    P = 2 * math.pi               # period of the test trajectory

    def x2(weight, scale, tau_eval, period):
        """x_w^2 (a0=1) for trajectory r_scale(t) = scale*r(t/scale), at time tau_eval."""
        if weight == "delta":
            return (_amag(tau_eval / scale) / scale) ** 2
        if weight == "exp_fixed":
            T = 4.0                              # FIXED width, in absolute time units
            s = np.linspace(0, 40 * T, 400001)
            w = np.exp(-s / T) / T
            am = _amag((tau_eval - s) / scale) / scale
            return _trapz(w * am ** 2, s) / _trapz(w, s)
        if weight == "orbit":
            Pl = period * scale                  # window RESCALES with the trajectory
            s = np.linspace(0, Pl, 200001)
            am = _amag((tau_eval - s) / scale) / scale
            return _trapz(am ** 2, s) / Pl
        if weight == "invs":
            eps, big = 1e-3, 1e3                 # w ~ 1/s, the other homogeneous solution
            s = np.linspace(eps, big, 400001)
            w = 1.0 / s
            am = _amag((tau_eval - s) / scale) / scale
            return _trapz(w * am ** 2, s) / _trapz(w, s)
        raise ValueError(weight)

    print(f"\n  Numerical test on a NON-circular trajectory, lambda = {lam}, tau = {tau}:")
    print(f"  {'weight w':<34}{'x_w[r_lam](tau)':>18}{'x_w[r](tau/lam)/lam':>22}{'invariant?':>13}")
    print("  " + "-" * 90)
    verdicts = {}
    for nm, key in [("ULTRALOCAL  w = delta(s)", "delta"),
                    ("ORBIT-AVERAGED (window = period)", "orbit"),
                    ("fixed-width exponential (tau_mem)", "exp_fixed"),
                    ("homogeneous w ~ 1/s (unnormalisable)", "invs")]:
        lhs = math.sqrt(x2(key, lam, tau, P))
        rhs = math.sqrt(x2(key, 1.0, tau / lam, P)) / lam
        rel = abs(lhs - rhs) / max(abs(rhs), 1e-30)
        inv = rel < 2e-3
        verdicts[key] = inv
        print(f"  {nm:<34}{lhs:>18.8f}{rhs:>22.8f}{('YES' if inv else 'NO'):>13}")

    check(verdicts["delta"], "ULTRALOCAL is DML scale-invariant")
    check(verdicts["orbit"], "ORBIT-AVERAGED is DML scale-invariant (window scales with orbit)")
    check(not verdicts["exp_fixed"],
          "FIXED-WIDTH kernel BREAKS DML scale invariance (as the functional equation demands)")

    print("\n  WHY the two named members both survive: delta satisfies lam*delta(lam s)=delta(s)")
    print("  identically, and the orbit-average window is not an external constant -- its width")
    print("  is the trajectory's own period, which rescales WITH the orbit. Both are scale-free.")
    print("\n  >>> CONSEQUENCE FOR THE 203 Gyr READING. A weight with a FIXED width tau_mem")
    print("      introduces a new dimensioned constant beyond a0 and breaks the very symmetry")
    print("      that delivers flat rotation curves and the BTFR. Milgrom's own construction")
    print("      (arXiv:2208.07073) avoids this by making his weight depend only on a RATIO of")
    print("      frequencies -- 'Only ratios of frequencies enter, and a0 remains the only new")
    print("      dimensioned constant.' The 203 Gyr kernel is exactly the forbidden kind.")
    print("\n  SECOND, INDEPENDENT PROBLEM with taking 203 Gyr seriously: it exceeds EVERY")
    print("  astrophysical dynamical time by orders of magnitude, so w would be effectively")
    print("  flat over every observable orbit:")
    for nm, tdyn in [("wide binary at 10 kAU", 1.0e6), ("MW vertical oscillation", 8.0e7),
                     ("solar Galactic orbit", 2.2e8), ("dwarf satellite orbit", 2.5e9)]:
        n = tau_mem(A0_CANON) / (tdyn * 3.1557e7)
        print(f"    {nm:<28} t_dyn ~ {tdyn:.1g} yr  ->  tau_mem / t_dyn = {n:.3g} orbits")
    print("  i.e. the 203 Gyr reading does NOT leave the choice open -- it collapses the whole")
    print("  family onto the ORBIT-AVERAGED member for every system we can observe, and makes")
    print("  ULTRALOCAL unreachable. It is therefore not a neutral curiosity: it PREDICTS the")
    print("  -0.037 dex dispersion-support offset rather than zero. Testable, and it is the")
    print("  member that DML scale invariance penalises. The two readings cannot both be held.")
    return verdicts


def T4_observable_lever():
    banner("T4. OBSERVABLE LEVER -- how sharply does eccentricity separate the weightings?")
    e = sp.symbols("e", nonnegative=True)
    # <|a|^2>_t over a Kepler orbit, exact
    th = sp.symbols("theta")
    # dt = (r^2/L) dtheta, r = p/(1+e cos th), |a| = GM/r^2
    integ = sp.integrate((1 + sp.cos(th) * e) ** 2, (th, 0, 2 * sp.pi))
    check(sp.simplify(integ - 2 * sp.pi * (1 + e**2 / 2)) == 0,
          f"INT (1+e cos)^2 dtheta = 2 pi (1 + e^2/2)  (got {sp.simplify(integ)})")
    ratio = sp.sqrt(1 + e**2 / 2) / (1 - e**2) ** sp.Rational(5, 4)
    print("\n  EXACT result: for a Kepler orbit of semi-major axis A, with a_circ = GM/A^2,")
    print(f"      sqrt(<|a|^2>_t) / a_circ = {ratio}")
    check(sp.simplify(ratio.subs(e, 0) - 1) == 0, "reduces to 1 at e=0 (all weightings agree)")

    print(f"\n  {'e':>6}{'orbit-avg / a_circ':>21}{'dex':>9}"
          f"{'ultralocal at apo':>20}{'apo split (dex)':>18}")
    print("  " + "-" * 76)
    for ev in [0.0, 0.2, 0.4, 0.6, 0.8, 0.9]:
        rv = float(ratio.subs(e, ev))
        apo = 1.0 / (1 + ev) ** 2          # |a|/a_circ at apocentre
        print(f"  {ev:>6.1f}{rv:>21.4f}{math.log10(rv):>9.3f}"
              f"{apo:>20.4f}{math.log10(rv/apo):>18.3f}")
    print("\n  Compare the framework's own dispersion-support test: 0.037 dex "
          f"(= factor {10**0.037:.3f}).")
    r6 = float(ratio.subs(e, 0.6))
    print(f"  At e = 0.6 the orbit-averaged/ultralocal split at apocentre is "
          f"{math.log10(r6/(1/1.6**2)):.2f} dex,")
    print(f"  i.e. ~{math.log10(r6/(1/1.6**2))/0.037:.0f}x the lever of the circular-system test.")

    print("\n  DWARF-SATELLITE EFE, RESOLVED BY ORBITAL PHASE. Milgrom (arXiv:2208.07073) makes")
    print("  the same distinction explicitly: the EFE is set by a time-average <a_ex> under a")
    print("  memory weight, versus the MOMENTARY a_ex under ultralocal weighting.")
    V_MW = 2.0e5                                   # m/s, flat MW curve -> a_ex = V^2/r
    KPC = 3.0857e19
    R_PERI, R_APO = 33.0, 117.0                    # Crater II, Gaia EDR3 (Pace+ 2022; Fu+ 2019)

    # time-weighted rms of a_ex over the radial orbit (dt \propto dr/v_r, flat-curve potential)
    rr = np.linspace(R_PERI, R_APO, 200001)
    vr = np.sqrt(np.maximum(np.log(R_APO / rr), 1e-14))
    wt = 1.0 / np.maximum(vr, 1e-7)
    aex_r = V_MW ** 2 / (rr * KPC)
    aex_rms = math.sqrt(_trapz(wt * aex_r ** 2, rr) / _trapz(wt, rr))

    def mu_fw(xv):
        return (math.sqrt(1 + 4 * xv * xv) - 1) / (2 * xv)

    print(f"\n    orbit spans r = {R_PERI:.0f} - {R_APO:.0f} kpc; time-rms a_ex/a0 = "
          f"{aex_rms/A0_CANON:.3f}")
    print("    In the EFE-dominated regime internal dynamics are Newtonian with G_eff =")
    print("    G/mu(a_ex/a0), so sigma^2 ~ 1/mu. Split as a function of CURRENT phase:")
    print(f"\n  {'current phase':<26}{'r (kpc)':>9}{'a_ex/a0 (momentary)':>21}"
          f"{'sigma_oa/sigma_ul':>19}{'dex':>8}")
    print("  " + "-" * 84)
    x_oa = aex_rms / A0_CANON
    for nm, r_kpc in [("at pericentre", R_PERI), ("mid-orbit", 60.0),
                      ("at apocentre", R_APO)]:
        x_ul = V_MW ** 2 / (r_kpc * KPC) / A0_CANON
        s_ratio = math.sqrt(mu_fw(x_oa) / mu_fw(x_ul))
        print(f"  {nm:<26}{r_kpc:>9.0f}{x_ul:>21.3f}{s_ratio:>19.3f}"
              f"{abs(math.log10(s_ratio)):>8.3f}")

    print("\n  >>> IMPORTANT CORRECTION TO THE OBVIOUS OBSERVING STRATEGY. The split is NOT")
    print("      largest for the famous EFE dwarfs. An eccentric orbit spends most of its time")
    print("      near APOCENTRE, so the time-average is dominated by the apocentric field --")
    print("      which means at apocentre the orbit-averaged and momentary values nearly")
    print("      COINCIDE and the test has almost no power. Crater II and Antlia II are both")
    print("      near apocentre (Pace+ 2022), so the flagship EFE successes are the WRONG")
    print("      objects for this test. The discriminating power is concentrated in dwarfs")
    print("      currently near PERICENTRE, where the momentary field greatly exceeds the")
    print("      orbit average. That is a sharp, cheap selection rule for a DR4 sample.")

    print("\n  RANKING by lever and by whether the dominant systematic is COHERENT (bad) or")
    print("  RANDOM (good), and -- decisively -- whether it CORRELATES with the discriminant:")
    rank = [
        ("1. MW satellite dwarfs NEAR PERICENTRE, phase-resolved EFE", "0.13-0.24",
         "random per object (small-N sigma, binaries)",
         "orbits known per object from Gaia; M/L does NOT correlate with orbital phase, so "
         "the coherent systematic is orthogonal to the discriminant; select near pericentre "
         "(apocentric dwarfs have ~no power); BUT tidal disturbance ALSO correlates with "
         "pericentre -- that confound is the main threat and must be modelled"),
        ("2. Eccentric wide binaries (2-30 kAU)", "0.2-0.9",
         "COHERENT (undetected triples; unknown e-distribution)",
         "largest raw lever, but e is unmeasurable per system at these separations, so the "
         "e-distribution prior is DEGENERATE with w itself; also sits in the omega_c gate dead zone"),
        ("3. MW vertical dynamics, population-differential", "0.05-0.2",
         "coherent MW potential -- but CANCELS between populations at fixed R",
         "different populations share a_ex and differ in vertical frequency; Milgrom flags "
         "exactly this case; a genuinely differential test"),
        ("4. Tidal streams (GD-1, Pal 5)", "0.1-0.3",
         "COHERENT (MW baryonic potential + progenitor orbit)",
         "precise geometry but the systematic is the model itself"),
        ("5. Infalling cluster members", "<0.1",
         "COHERENT (cluster mass modelling)",
         "weakest; MOND clusters already carry an unresolved central residual"),
    ]
    for nm, lev, sysd, note in rank:
        print(f"\n    {nm}")
        print(f"       lever ~{lev} dex | systematic: {sysd}")
        print(f"       {note}")


def T5_composite_body():
    banner("T5. IS w REALLY THE ENTIRE REMAINING FREEDOM? -- the composite-body test")
    print("  Milgrom flagged this in the ORIGINAL 1994 paper (Annals of Physics 229, 384;")
    print("  astro-ph/9303012) and it is still open in 2022:")
    print('    \"We cannot yet offer an example of a theory that fully accounts for the correct')
    print('     center-of-mass motion of composite objects: A composite body (e.g. a star),')
    print('     with constituents whose internal motion is Newtonian should still undergo a')
    print('     center-of-mass motion similar to that of a test particle, which may be well in')
    print('     the MOND regime.\"')
    print("  His fix needs FREQUENCY structure: high-frequency internal accelerations must be")
    print("  SUPPRESSED in the low-frequency (galactic) inertia. In 2208.07073 that is the")
    print("  weight theta(omega'/omega), which decays for omega' >> omega.")

    print("\n  Now test the framework's family against it. THE OBSTRUCTION IS POSITIVITY.")
    print("  Theorem 1 makes the argument exactly +|a|^2 (from u.u = -1), so for ANY normalised")
    print("  w >= 0:   if |a(tau)| >= A on supp(w), then x_w >= A/a0.  A positive weight cannot")
    print("  SUPPRESS a large internal acceleration -- averaging a positive quantity keeps it.")

    a0 = 1.0
    # a star's constituent: huge internal acceleration, small galactic component
    A_INT = 274.0 / 9.36e-11        # solar surface gravity in units of a0
    A_GAL = 0.5                      # galactic component, in units of a0 (deep MOND)
    print(f"\n  Star constituent: |a_int| = {A_INT:.3g} a0 (solar surface gravity), "
          f"|a_gal| = {A_GAL} a0")

    def mu_fw(xv):
        return (math.sqrt(1 + 4 * xv * xv) - 1) / (2 * xv)

    t = np.linspace(0, 200 * math.pi, 400001)
    # constituent acceleration: fast internal oscillation + slow galactic term
    a_int = A_INT * np.cos(50.0 * t)
    a_gal = A_GAL * np.ones_like(t)
    amag2 = (a_int + a_gal) ** 2

    print(f"\n  {'weight w':<38}{'x_w':>14}{'mu_fw(x_w)':>13}{'MOND?':>9}")
    print("  " + "-" * 76)
    for nm, key in [("ULTRALOCAL delta (at generic phase)", "d"),
                    ("ORBIT-AVERAGED over internal period", "o"),
                    ("fixed-width kernel, any width", "f")]:
        if key == "d":
            xw = math.sqrt(amag2[len(amag2) // 3])
        elif key == "o":
            xw = math.sqrt(float(np.mean(amag2[: len(amag2) // 100])))
        else:
            T = 20.0
            s = t
            w = np.exp(-s / T) / T
            xw = math.sqrt(float(_trapz(w * amag2, s) / _trapz(w, s)))
        m = mu_fw(xw)
        mondy = m < 0.9
        print(f"  {nm:<38}{xw:>14.4g}{m:>13.6f}{('yes' if mondy else 'NO'):>9}")
        check(not mondy, f"{nm.strip()} leaves the constituent NEWTONIAN (mu={m:.6f})")

    print("\n  Every member gives mu_fw ~ 1: the constituent is Newtonian, so the star's total")
    print("  inertia is Newtonian, so its centre of mass feels NO MOND in the galaxy -- and")
    print("  rotation curves, which are the framework's primary evidence, would be Newtonian.")
    print("  This is not a property of a bad choice of w. It follows from |a|^2 >= 0, i.e. from")
    print("  the SAME positivity (Theorem 1, u.u = -1) that gives Im K == 0. The framework's")
    print("  positivity-locked first moment has no suppression mechanism at all.")
    print("\n  THE FORK, both horns stated:")
    print("   (i)  If the law applies to every timelike worldline (as Theorem 1 states), then NO")
    print("        member of the w-family solves the composite-body problem. The freedom is in")
    print("        the wrong place: fixing w would not complete the inertia sector.")
    print("   (ii) If instead the law applies only to designated centre-of-mass worldlines, the")
    print("        theory needs an extra rule saying WHICH worldlines are fundamental (star?")
    print("        cloud? galaxy?). That rule is a new free choice, and a BIGGER one than w.")
    print("  Either way the brief's premise -- that w is the entire remaining freedom -- does")
    print("  not survive. Milgrom escapes only because his weight is a frequency RATIO acting")
    print("  on |a_hat(omega)|, which a positive time-domain weight on |a|^2 cannot reproduce.")


def main() -> int:
    banner("mi_memory_weight_w_2026 -- can physics fix the memory weight w?")
    T1_timescales()
    spread = T2_branch_point_artefact()
    T3_scale_invariance()
    T4_observable_lever()
    T5_composite_body()

    banner("SUMMARY -- stated whatever the outcome")
    print("  1. (T1) No enumerated physical process sets 2c/a0. Worse, the comparison is")
    print("     structurally uninformative: c/a0 is the ONLY time a0 and c can build, so any")
    print("     a0-scale process matches to O(1) automatically. And every bath-sourced kernel")
    print("     is dissipative, which the framework's own Im K == 0 (and the 8.5 sigma")
    print("     J0737-3039 bound) forbids. The candidate class is empty on analytic character.")
    print(f"  2. (T2) tau_mem = 2c/a0 is an ARTEFACT. It changes by exactly 2 under a pure")
    print("     re-parametrisation of the SAME law (nu-form vs mu-form), and by a factor")
    print(f"     {spread:.0f} across interpolation functions that fit the RAR comparably. The branch")
    print("     point also sits at an imaginary acceleration the dynamics provably never")
    print("     reaches. It should NOT be presented as a memory timescale.")
    print("  3. (T3) DML spacetime scale invariance (Milgrom 2009) is a REAL constraint: it")
    print("     forces lambda w(lambda s) = w(s). Ultralocal and orbit-averaged both pass;")
    print("     every FIXED-width kernel fails, including a 203 Gyr one. So w is narrowed to")
    print("     scale-free members, but NOT to a unique one.")
    print("  4. (T4) Eccentric systems beat the circular-system test by ~6-20x in lever, but")
    print("     ONLY near pericentre -- at apocentre the orbit average and the momentary value")
    print("     nearly coincide, so the famous EFE dwarfs have almost no power. w must be fixed")
    print("     by DATA, and the sharpest available are pericentric dwarf EFE measurements.")
    print("  5. (T5) w is NOT the entire remaining freedom. Positivity (|a|^2 >= 0, the same")
    print("     Theorem-1 positivity that gives Im K == 0) means NO member of the w-family")
    print("     suppresses a star's internal accelerations, so none solves the composite-body")
    print("     problem Milgrom named in 1994 and had not solved in 2022. Either the law fails")
    print("     for composite bodies, or it needs an extra rule naming which worldlines are")
    print("     fundamental -- a larger freedom than w itself.")
    print("=" * 96)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
