#!/usr/bin/env python3
"""Q1-3 -- what the dS_4 Dirac-fermion current says about alpha: conductivity function G_f(m/H), ties, the ln(m/H) term, G_f vs the scalar G, special values.

Pre-registered in Q1_PREREGISTRATION.md (with Amendments; written before this script was run).  Uses ONLY the closed form (3.12) of arXiv:1603.04165 in the amended
variant validated by the direct mode sum in q1_2_induced_current_ds4.py (see the amendment log), the weak-field formula (4.3), and the AH4 scalar closed form (Kobayashi-Afshordi 2.58).
Units H = 1.  J_HFY(L, M) = <J^3>_ren/(e a^3 H^3);  sigma_HFY(M) = lim J_HFY/L;  conductivity sigma_c = J/E:  sigma_c/H = e^2 sigma_HFY = alpha G_f(M),  G_f = 4 pi sigma_HFY  (AH4's G = f_1/pi).

Run:     python3 q1_3_physics_answers.py            (real run; exit 0 iff every check passes)
         python3 q1_3_physics_answers.py --mutate   (control: the SCALAR ln M coefficient 1/(12 pi^2) replaces the Dirac 1/(3 pi^2) in the running check; Q2 must FAIL;
                                                     exit 1 if the targeted check FAILS as required, exit 3 if it does NOT fail = the control has no power)
"""
import sys
sys.dont_write_bytecode = True
import math
import numpy as np
import mpmath as mp
import sympy as sp
from q1_lib import PI, hfy_closed, hfy_weak, scalar_closed_f

MUTATE = "--mutate" in sys.argv
CHECKS = {}
KAPPA = 0.5


def check(tag, ok, detail=""):
    CHECKS[tag.split()[0]] = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}", flush=True)


def sigma_min(M):
    return hfy_weak(M)


def sigma_max(M):
    """Hayashinaka-Xue maximal subtraction, their (15)/(16): sigma_max = -M (4 M^2 + 1)/(9 pi sinh(2 pi M))  (quoted, not re-derived)."""
    mp.mp.dps = 40
    M = mp.mpf(M)
    return float(-M * (4 * M ** 2 + 1) / (9 * mp.pi * mp.sinh(2 * mp.pi * M)))


def G_f(M, scheme="min"):
    return 4 * PI * (sigma_min(M) if scheme == "min" else sigma_max(M))


def G_s(M, lam=1e-4):
    return scalar_closed_f(lam, M) / lam / PI


if __name__ == "__main__":
    print("=" * 108)
    print("Q1-3 physics answers for the dS_4 Dirac fermion -- mode: " + ("MUTATE CONTROL (scalar ln coefficient used)" if MUTATE else "REAL RUN"))
    print("=" * 108, flush=True)

    # ------------------------------------------------------------------ Q2: the ln(m/H) term  (run first: the control targets it)
    print("\nQ2. the ln(m/H) term")
    tt, HH, EE = sp.symbols("tau H E", real=True)
    a = -1 / (HH * tt)
    div = sp.simplify(sp.diff(a ** 4 * (-EE / a ** 2), tt) / a ** 4)                      # nabla_nu F^{nu z}, F_{tau z} = E a^2
    divv = abs(float(div.subs({tt: -1, HH: 1, EE: 1})))
    print(f"     nabla_nu F^(nu z) = {div}   -> |.| at tau = -1, H = 1, E = 1: {divv:.6f}  (= 2 E H / a)")
    coef_dirac_closed = (1 / (4 * PI ** 2)) * (4.0 / 3.0)         # (3.12): (e L/(4 pi^2)) (4/3) ln M, in units of e^2 E H (e H^3 L = e^2 E H)
    coef_scalar_closed = (1 / (4 * PI ** 2)) * (1.0 / 3.0)        # AH4 / K&A (2.58): (e H^3/(4 pi^2)) (lambda/3) ln m
    coef_used = coef_scalar_closed if MUTATE else coef_dirac_closed
    running_dirac = (1 / (6 * PI ** 2)) * divv                    # d(1/e^2)/d ln mu = -1/(6 pi^2) (one Dirac fermion, recalled) x |nabla F|
    running_scalar = (1 / (24 * PI ** 2)) * divv                  # complex scalar
    print(f"     coefficient of e^2 E H ln M:  used {coef_used:.10e}   Dirac running x |nabla F| = {running_dirac:.10e}   scalar running x |nabla F| = {running_scalar:.10e}")
    ok_run = abs(abs(coef_used / running_dirac) - 1) < 1e-12
    ok_ratio = abs(coef_used / coef_scalar_closed - 4.0) < 1e-12
    check("Q2a the ln M coefficient of (3.12) equals the one-loop Dirac running (1/(6 pi^2)) times |nabla_nu F^(nu z)| = 2 E H (|ratio| = 1 to 1e-12)", ok_run, f"(ratio {coef_used / running_dirac:.12f})")
    check("Q2b the ratio Dirac/scalar coefficient equals 4 to 1e-12 (b = 4/3 vs 1/3 per unit charge)", ok_ratio, f"(ratio {coef_used / coef_scalar_closed:.12f})")
    if MUTATE:
        failed = not (CHECKS["Q2a"] and CHECKS["Q2b"])
        print("\nMUTATE CONTROL: the scalar ln M coefficient replaced the Dirac one in Q2a/Q2b.")
        print(f"  Q2a/Q2b {'FAILED as required -- the control works' if failed else 'DID NOT FAIL -- the check has no power'}")
        sys.exit(1 if failed else 3)

    # heavy-mass decoupling from the validated closed form at small L
    print("\n     heavy-mass decoupling (small-L closed form (3.12)):  sigma_HFY(M) = J/L at L = 1e-3")
    sig = {}
    for M in (2.0, 5.0, 10.0, 20.0, 40.0):
        sig[M] = hfy_closed(1e-3, M, dps=60, variant="amended") / 1e-3
        print(f"     M = {M:5.1f}   sigma_HFY = {sig[M]:+.6e}   (1/(3 pi^2)) ln M = {math.log(M) / (3 * PI ** 2):.5f}   weak-field (4.3): {sigma_min(M):+.6e}")
    slope = (math.log(abs(sig[40.0])) - math.log(abs(sig[10.0]))) / (math.log(40.0) - math.log(10.0))
    print(f"     log-log slope of |sigma_HFY| between M = 10 and 40: {slope:.4f}")
    check("Q2c heavy fermions decouple as a POWER (slope in [-2.3, -1.7]) and the ln M term is cancelled: |sigma_HFY(40)| < (1/3)(1/(3 pi^2)) ln 40", -2.3 <= slope <= -1.7 and abs(sig[40.0]) < math.log(40.0) / (3 * PI ** 2) / 3, f"(slope {slope:.3f})")

    # ------------------------------------------------------------------ Q3: G_f vs G_s
    print("\nQ3. conductivity functions: G_f(M) = 4 pi sigma_HFY (Dirac, minimal scheme) and G_s(M) (complex scalar, AH4/K&A), sigma_c/H = alpha G")
    MS = (0.01, 0.1, 0.3, 1.0, 2.0, 5.0, 10.0, 20.0, 40.0)
    Gf = {M: G_f(M) for M in MS}
    Gs = {}
    for M in MS:
        try:
            Gs[M] = G_s(M)
        except Exception as ex:                                          # closed form may fail numerically at very small M: reported, not silently dropped
            Gs[M] = None
            print(f"     scalar closed form failed at M = {M}: {ex}")
    print("      M        G_f(M)          G_s(M)         G_f M^2        G_s M^2      G_f/G_s")
    for M in MS:
        gs = Gs[M]
        print(f"     {M:6.2f}  {Gf[M]:+.6e}  " + (f"{gs:+.6e}" if gs is not None else "   n/a       ") + f"  {Gf[M] * M * M:+.6e}  " + (f"{gs * M * M:+.6e}" if gs is not None else "   n/a       ") + "  " + (f"{Gf[M] / gs:+.4f}" if gs is not None else "n/a"))
    grid = np.exp(np.linspace(math.log(1e-2), math.log(50.0), 400))
    negs = all(sigma_min(float(M)) < 0 for M in grid)
    check("Q3a sigma_HFY(M) < 0 (negative conductivity, anti-screening) at every M on a 400-point log grid in (0.01, 50) (HFY's claim, NOT assumed)", negs, "")
    cf, cs = 1 / (9 * PI), 7 / (18 * PI)
    okb = abs(abs(Gf[40.0]) * 40.0 ** 2 / cf - 1) < 0.02 and Gs[40.0] is not None and abs(Gs[40.0] * 40.0 ** 2 / cs - 1) < 0.02
    check("Q3b large M: |G_f| M^2 -> 1/(9 pi) = 0.03537 and G_s M^2 -> 7/(18 pi) = 0.1238, each within 2% at M = 40", okb,
          f"(G_f M^2 = {Gf[40.0] * 1600:+.5f}; G_s M^2 = {Gs[40.0] * 1600 if Gs[40.0] is not None else float('nan'):+.5f})")
    gam = float(mp.euler)
    pred = lambda M: (4 / (3 * PI)) * (math.log(M) + gam - 1 / 6)
    okc = abs((Gf[0.01] - Gf[0.1]) / ((4 / (3 * PI)) * math.log(0.1)) - 1) < 0.05 and abs(Gf[0.01] / pred(0.01) - 1) < 0.02 and abs(Gf[0.1] / pred(0.1) - 1) < 0.02
    okc_s = Gs[0.1] is not None and Gs[0.3] is not None and Gs[0.1] / Gs[0.3] > 5.0
    check("Q3c small M (Amendment 4 wording): the fermion follows the logarithm G_f = (4/(3 pi))(ln M + gamma_E - 1/6) within 2% at M = 0.01 and 0.1 (and (G_f(0.01) - G_f(0.1))/((4/(3 pi)) ln 0.1) is within 5% of 1) while the scalar grows as a power (G_s(0.1)/G_s(0.3) > 5)",
          okc and okc_s, f"(G_f(0.01)/pred = {Gf[0.01] / pred(0.01):.4f}, G_f(0.1)/pred = {Gf[0.1] / pred(0.1):.4f}; G_s(0.1)/G_s(0.3) = {Gs[0.1] / Gs[0.3] if okc_s or Gs[0.1] else float('nan'):.3f}; G_f(0.1)/G_f(0.3) = {Gf[0.1] / Gf[0.3]:.3f})")
    sl_f = (math.log(abs(Gf[40.0])) - math.log(abs(Gf[10.0]))) / math.log(4.0)
    sl_s = (math.log(abs(Gs[40.0])) - math.log(abs(Gs[10.0]))) / math.log(4.0)
    check("Q3d both fall as power laws at large M (no exponential threshold): log-log slopes between M = 10 and 40 in [-2.3, -1.7]", -2.3 <= sl_f <= -1.7 and -2.3 <= sl_s <= -1.7, f"(fermion {sl_f:.3f}, scalar {sl_s:.3f})")
    check("Q3e opposite sign and ratio: G_f/G_s -> -(1/9)/(7/18) = -2/7 = -0.2857 within 3% at M = 40", abs(Gf[40.0] / Gs[40.0] / (-2 / 7) - 1) < 0.03, f"(G_f/G_s = {Gf[40.0] / Gs[40.0]:+.4f})")
    print("     (scheme note, quoted from Hayashinaka-Xue 1802.03686, not re-derived)  maximal subtraction: G_f^max(M) = 4 pi sigma_max(M):")
    for M in (0.0001, 0.5, 1.0, 2.0, 5.0):
        print(f"       M = {M:g}:  G_f^max = {G_f(M, 'max'):+.6e}   (minimal: {G_f(M):+.6e})")
    print(f"       M -> 0: G_f^max(0) = -2/(9 pi) = {-2 / (9 * PI):+.6f};  large M: exponentially small e^(-2 pi M) (a different asymptotic class from the power law of the minimal scheme)")

    # ------------------------------------------------------------------ Q1: ties
    print("\nQ1. does sigma_c/H = alpha G_f(M) let a tie fix alpha?  required alpha = c/G_f(M) for ties sigma_c/H = c")
    MASSES = (0.5, 1.0, 2.0, 5.0)
    CS = {"kappa": KAPPA, "kappa/pi": KAPPA / PI, "1/(2 pi)": 1 / (2 * PI), "1/pi": 1 / PI, "1": 1.0, "2 kappa": 2 * KAPPA}
    any_det = False
    for scheme in ("min", "max"):
        print(f"   scheme {scheme}:  G_f = " + ", ".join(f"{G_f(M, scheme):+.4e}" for M in MASSES) + f"  at M = {MASSES}")
        for name, c in CS.items():
            vals = [c / G_f(M, scheme) for M in MASSES]
            pos = all(v > 0 for v in vals)
            mags = [abs(v) for v in vals]
            spread = max(mags) / min(mags)
            det = pos and spread < 2.0
            any_det = any_det or det
            print(f"     c = {name:9s} required alpha: " + "  ".join(f"{v:+.3e}" for v in vals) + f"   sign-consistent positive: {pos};  |spread| max/min = {spread:.2e};  determined: {det}")
    check("Q1a no tie among the six constants and four masses, in either scheme, is both positive and mass-independent within a factor 2 (alpha not determined)", not any_det, "")
    # structure: e enters only through e^2 (overall) and L: from q1_1 D2c; state numerically that sigma_c/H scales as e^2 at fixed M
    print("     structure: J = e H^3 F(L, M), F odd in L (q1_2), so sigma_c/H = e^2 F_1(M) = 4 pi alpha (G_f/(4 pi)) = alpha G_f(M) with G_f independent of e (q1_1 D2c: (e, E, m, H) enter only via L, M).")
    MU_E = 0.51099895e6 / (67.4e3 / 3.0856775814913673e22 * 6.582119569e-16)
    print(f"   electron-mass reading (EXTRAPOLATION of the large-M law G_f ~ -1/(9 pi M^2)): M_e = m_e/H_0 = {MU_E:.3e}; |G_f| ~ {1 / (9 * PI * MU_E ** 2):.2e};  a tie sigma_c/H = kappa would need |alpha| ~ {KAPPA * 9 * PI * MU_E ** 2:.2e} (and the sign is wrong)")

    # ------------------------------------------------------------------ Q4: special values
    print("\nQ4. special values of the coupling?")
    # (a) zeros of sigma_HFY(M): none (Q3a).  (b) zero of the current: L*(M)
    mp.mp.dps = 60

    def J_of(L, M):
        return hfy_closed(L, M, dps=60, variant="amended")
    print("     (b) the current's own zero L*(M) (HFY's stable point; a FIELD value eE/H^2, not a coupling):")
    Lstar = {}
    nzero = {}
    for M in MASSES:
        scan = [J_of(float(Lx), M) for Lx in np.exp(np.linspace(math.log(0.02), math.log(40.0), 41))]
        nzero[M] = sum(1 for u, v in zip(scan[:-1], scan[1:]) if u * v < 0)
        lo, hi = 0.02, 40.0
        jl, jh = J_of(lo, M), J_of(hi, M)
        if jl < 0 < jh:
            for _ in range(50):
                mid = math.sqrt(lo * hi)
                if J_of(mid, M) > 0:
                    hi = mid
                else:
                    lo = mid
            Lstar[M] = math.sqrt(lo * hi)
            print(f"       M = {M:3.1f}:  J(0.02) = {jl:+.3e} < 0,  J(40) = {jh:+.3e} > 0,  L* = {Lstar[M]:.5f}   (sign changes on a 41-point log scan of (0.02, 40): {nzero[M]}; E* = L* H^2/e: any e is compatible with any L*)")
        else:
            Lstar[M] = None
            print(f"       M = {M:3.1f}:  J(0.02) = {jl:+.3e}, J(40) = {jh:+.3e}: no sign change bracketed")
    check("Q4a sigma_HFY has no zero (Q3a) and the current has one sign change L*(M) at each of the four masses; L* is a field value, so it selects no coupling", negs and all(v is not None for v in Lstar.values()) and all(nzero[M] == 1 for M in MASSES),
          "(existence of L* is descriptive; the coupling e is unconstrained because E is free)")
    print("     (c) massless conformal limit: the minimal scheme has (4/(3 pi)) ln M -> -infinity (no finite value); the maximal scheme has G_f^max(0) = -2/(9 pi) < 0, which no positive tie can match;")
    print("         with m = 0 the only scale besides H is the renormalization scale mu, and ln(mu/H) is a free input.")
    n_list = 6 * 4 * 2 + 1 + 4
    print('     note: L*(M) is not monotonic in M (descriptive).')
    print(f"     closed candidate list scored: {n_list} (six ties x four masses x two schemes, the M -> 0 maximal value, and L* at four masses); none selects a value of alpha.")

    print("\n" + "=" * 108)
    passed = sum(CHECKS.values())
    print(f"CHECKS: {passed}/{len(CHECKS)} passed")
    print("Scope: one Dirac fermion, minimal coupling, dS_4 planar patch, in-vacuum, published order-2 adiabatic (minimal) subtraction; scheme comparison quoted, not re-derived.")
    print("alpha stays an INPUT (the ln(m/H) term is the running of e; flat-space renormalization condition).  kappa = 1/2 stays FITTED.  The SM-mass wall is unchanged.")
    sys.exit(0 if passed == len(CHECKS) else 1)
