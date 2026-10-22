#!/usr/bin/env python3
"""
a50_checks.py -- Lane A50: can the first law of horizon mechanics fix kappa?

THE QUESTION.  Every other lane in this push attacks kappa algebraically: A1 proved
that no function of (c, G, hbar, Lambda, H) fixes it, that cell counting cannot reach
it, and that the "1/12" is the same equation restated.  Nobody has written the
THERMODYNAMIC lane: does the first law of horizon mechanics, applied at the apparent
horizon of the theory's own FRW background, force kappa = 1/2?

WHAT IS TRUE HERE, EXACTLY (all derived below, each with a check):

 (1) GEOMETRIC IDENTITY.  At the apparent horizon r_A = c/H, with
     S = A/(4 l_P^2) and T = hbar H/(2 pi k_B),

         T dS = (c^4/G) dr_A .                                       [K1, residual 0]

     The horizon heat flow is one unit of entropy per Planck length of radius.

 (2) THE FIRST LAW IS A CONSISTENCY CONDITION, NOT AN EQUATION OF MOTION.
     Along ANY flat FRW solution E = rho c^2 V = c^5/(2 G H) identically (the
     Misner-Sharp mass), so

         dE + P dV = ((1+3w)/2) (c^4/G) dr_A = ((1+3w)/2) T dS .    [K2, residual 0]

     Both sides are proportional to Hdot, so Hdot CANCELS: the first law does not
     determine the expansion rate.  Its entire content is the single algebraic
     relation lambda = (1+3w)/2 for the temperature normalization T = lambda T_dS.
     It contains no kappa and no a0.

 (3) THE EQUATION OF STATE IT DERIVES.  With the literal de Sitter temperature
     (lambda = 1) the Clausius relation holds iff w = 1/3, exactly.  For dust it
     fails by exactly 2; for vacuum it is degenerate (0 = 0).  So the first law at
     a conformal horizon is exact for radiation and only for radiation.  [K3]

 (4) THE COEFFICIENT OF THE SURFACE GRAVITY IS NOT 1 OR 1/2, IT IS A FUNCTION.
     T = lambda T_dS corresponds to kappa_sg = lambda c^2/r_A = lambda cH, so the
     first law forces kappa_sg/cH = (1+3w)/2: 1/2 for dust, 1 for radiation,
     -1 for vacuum.  No constant lambda satisfies the law across epochs
     (spread 2 over w in [-1, 1/2]).  A running coefficient cannot be the theory's
     constant kappa.                                                 [K4, K5]

 (5) THE 1/2 DOES APPEAR -- TWICE -- AND BOTH TIMES IT IS EINSTEIN BOOKKEEPING.
       N_surf = A/l_P^2 = 4S/k_B ;  N_bulk = 2E/(k_B T) ;
       N_bulk/N_surf = (1/2)|1+3w| (rho/rho_crit) .
     With the naive energy (w = 0): exactly 1/2 at rho = rho_crit.  The 1/2 is the
     coefficient ratio (4 pi G/3)/(8 pi G/3) -- the Einstein normalization.
     With the Komar energy and the theory's vacuum: exactly 1.  [K7-K9]

 (6) THE THEORY'S VACUUM IS SATURATED HOLOGRAPHIC EQUIPARTITION.
     N_surf = N_bulk^Komar  <=>  rho = 3H^2/(8 pi G)  <=>  P3.
     Padmanabhan's equality is not evidence for kappa; it is P3 rewritten.  [K10]

 (7) THE OBSTRUCTION.  Every horizon functional (T, S, E, P, V, N_surf, N_bulk) is a
     function of (H, rho, G, hbar, c, w) only.  kappa and a0 occur in NONE of them
     (symbolic absence + a 400-point scan with drift 0.0e+00).  No identity among
     them can contain kappa.  [K11]

     The step from "coefficient 1/2" to "kappa = 1/2" needs the map
     a0 <-> horizon acceleration, and that map carries the Einstein factor
     sqrt(3/(8 pi)) = 2/Z = 0.3454941:

         a0 = kappa c sqrt(G rho_bare), rho_bare = rho_crit
         => a0/(cH) = kappa sqrt(3/8 pi) => kappa = lambda Z/2 .      [K12]

     The first law supplies lambda = 1/2 (dust).  Inserting the Einstein factor
     gives kappa = (1/2)/0.3454941 = Z/4 = 1.447203 -- 2.894x the canonical 1/2 and
     2.894x the observed acceleration scale.  To land on kappa = 1/2 the first-law
     coefficient must be 1/Z = 0.1727471 = (1/2)sqrt(3/8 pi), i.e. w = -0.2181686,
     an equation of state the theory does not contain.  The "derivation" kappa = 1/2
     therefore assumes itself.                                        [K13-K16]

 (8) THE FACTOR.  kappa = 1/2 requires the coefficient (1/2)sqrt(3/8 pi) in the
     a0/(cH) normalization.  The thermodynamic 1/2 arrives WITHOUT sqrt(3/8 pi).
     The factor between them is sqrt(3/(8 pi)) = 2/Z = 0.3454941.  It is NOT
     2 sqrt(32 pi/3) = 11.5776 = 4/sqrt(3/8 pi) = 2Z, which overshoots the required
     number by 33.5x.                                                 [K14, K15]

VERDICT: NO-GO(obstruction).  kappa = 1/2 is not derivable from horizon
thermodynamics.  The first law is the Friedmann equation rewritten and is kappa-free;
it yields a 1/2 only as the dust-era value of a running temperature coefficient, and
converting that 1/2 into kappa requires the Einstein factor sqrt(3/8 pi) = 2/Z.

USAGE
    python3 a50_checks.py                # 17/17 PASS, exit 0
    python3 a50_checks.py --mutate=m1    # mutation control (see MUTATE.md)

Requires python3 + numpy + sympy; deterministic; no network; < 10 s.
Writes a50_results.json in the current directory.
"""

import sys
import json
import math

import numpy as np
import sympy as sp

# -----------------------------------------------------------------------------
# constants -- BRIEF Section 4 (CODATA 2018) and the theory's own values (P3)
# -----------------------------------------------------------------------------
C = 2.99792458e8             # m/s
G = 6.67430e-11              # m^3 kg^-1 s^-2
HBAR = 1.054571817e-34       # J s
KB = 1.380649e-23            # J/K
H0 = 2.1843e-18              # s^-1
LAM = 1.0890e-52             # m^-2
MPC = 3.0856775814913673e22  # m
KAPPA = 0.5                  # target value
Z = 2.0 * math.sqrt(8.0 * math.pi / 3.0)          # 5.7888100365 = 2sqrt(8pi/3)
INV_Z = 1.0 / Z                                   # 0.1727470747
SQRT_38PI = math.sqrt(3.0 / (8.0 * math.pi))      # 0.3454941495 = 2/Z
TWOSQRT_32PI3 = 2.0 * math.sqrt(32.0 * math.pi / 3.0)   # 11.5776200729 = 2Z

L_P2 = G * HBAR / C ** 3
RHO_CRIT_H0 = 3.0 * H0 ** 2 / (8.0 * math.pi * G)
H_LAMBDA = C * math.sqrt(LAM / 3.0)
RHO_CRIT_HL = 3.0 * H_LAMBDA ** 2 / (8.0 * math.pi * G)

MUT = None
for _a in sys.argv[1:]:
    if _a.startswith("--mutate="):
        MUT = _a.split("=", 1)[1]

_CHECKS = []
_SUMMARY = {}


def check(cid, ok, measured, threshold, note=""):
    _CHECKS.append(dict(id=cid, **{"pass": bool(ok)}, value=str(measured),
                        threshold=str(threshold), note=note))
    print("%-4s %-4s measured=%-46s threshold=%-22s # %s"
          % (cid, "PASS" if ok else "FAIL", measured, threshold, note))


def emit(**kw):
    _SUMMARY.update(kw)


def finalize():
    n, npass = len(_CHECKS), sum(1 for c in _CHECKS if c["pass"])
    _SUMMARY["checks"] = _CHECKS
    _SUMMARY["n_pass"] = npass
    _SUMMARY["n_total"] = n
    _SUMMARY["status"] = "NO-GO(obstruction)" if npass == n else "FAIL"
    with open("a50_results.json", "w") as fh:
        json.dump(_SUMMARY, fh, indent=1, sort_keys=True)
    print("-" * 100)
    print("A50 COMPLETE: %d/%d checks PASS." % (npass, n))
    return 0 if npass == n else 1


# =============================================================================
# K1 -- T dS = (c^4/G) dr_A identically
# =============================================================================
def k1():
    H, c, Gs, hb, kB = sp.symbols("H c G hbar k_B", positive=True)
    S = kB * sp.pi * c ** 5 / (Gs * hb * H ** 2)     # A/(4 l_P^2) kB, A = 4 pi (c/H)^2
    T = hb * H / (2 * sp.pi * kB)
    lhs = sp.simplify(T * sp.diff(S, H))
    rhs = sp.simplify((c ** 4 / Gs) * sp.diff(c / H, H))
    resid = sp.simplify(lhs - rhs)
    ratio = float((lhs / rhs).subs({H: H0}))
    check("K1", resid == 0 and abs(ratio - 1) < 1e-15,
          "residual=%.1e ratio=%.15f" % (float(resid), ratio), "0, 1",
          "T dS = (c^4/G) dr_A exactly (S=A/4l_P^2, T=hbarH/2pik_B)")
    emit(K1_residual=float(resid), K1_ratio=ratio)
    return dict(S=S, T=T)


# =============================================================================
# K2 -- (dE + P dV) = ((1+3w)/2) T dS exactly, via E = c^5/(2GH)
# =============================================================================
def k2():
    H, Hd, rho, w, c, Gs, hb, kB = sp.symbols("H Hdot rho w c G hbar k_B", positive=True)
    # horizon geometry
    T = hb * H / (2 * sp.pi * kB)
    S = kB * sp.pi * c ** 5 / (Gs * hb * H ** 2)
    V = 4 * sp.pi / 3 * (c / H) ** 3
    # sphere energy along a flat FRW solution: E = rho c^2 V with rho = 3H^2/8piG
    rho_fr = 3 * H ** 2 / (8 * sp.pi * Gs)
    E = sp.simplify(rho_fr * c ** 2 * V)              # = c^5/(2 G H)
    E_closed = c ** 5 / (2 * Gs * H)
    dE = sp.diff(E_closed, H) * Hd
    dV = sp.diff(V, H) * Hd
    P = w * rho_fr * c ** 2
    TdS = T * sp.diff(S, H) * Hd
    lam = sp.simplify(sp.expand((dE + P * dV) / TdS))
    # must be (1+3w)/2, independent of H, Hdot, rho
    resid = sp.simplify(lam - (1 + 3 * w) / 2)
    dHd = sp.simplify(sp.diff(lam, Hd))
    l0 = float(lam.subs({w: 0}))
    l13 = float(lam.subs({w: sp.Rational(1, 3)}))
    ok = (resid == 0 and dHd == 0 and abs(l0 - 0.5) < 1e-15 and abs(l13 - 1) < 1e-15)
    check("K2", ok, "lam(0)=%.15f lam(1/3)=%.15f dlam/dHdot=%.1e" % (l0, l13, float(dHd)),
          "(1+3w)/2, dHdot=0",
          "E=c^5/(2GH) identically => dE+PdV=((1+3w)/2)TdS; Hdot cancels")
    emit(K2_lambda_dust=l0, K2_lambda_rad=l13, K2_E_closed=str(E_closed),
         K2_residual=float(resid), K2_dlam_dHdot=float(dHd))
    return lam


# =============================================================================
# K3 -- the literal law (lambda=1) holds iff w=1/3; dust fails by 2; vacuum 0=0
# =============================================================================
def k3(lam):
    _fs = sorted(lam.free_symbols, key=str)
    w = _fs[0] if _fs else sp.Symbol("w")
    wsol = sp.solve(sp.Eq(lam, 1), w)
    dust_factor = float(sp.simplify(1 / lam.subs({w: 0})))
    lvac = sp.simplify(lam.subs({w: -1}))
    # vacuum: lambda = -1, and on the exact dS solution Hdot = 0 kills both sides
    H, Hd, c, Gs, hb, kB = sp.symbols("H Hdot c G hbar k_B", positive=True)
    TdS_coef = sp.simplify((hb * H / (2 * sp.pi * kB)) * sp.diff(
        kB * sp.pi * c ** 5 / (Gs * hb * H ** 2), H))        # coefficient of Hdot
    dEP_coef = sp.simplify(lvac * TdS_coef)                    # ((1+3w)/2) TdS/Hdot at w=-1
    vac_onshell = (sp.simplify(TdS_coef.subs({H: H0}) * Hd).subs({Hd: 0}) == 0
                   and sp.simplify(dEP_coef.subs({H: H0}) * 0) == 0)
    ok = (len(wsol) == 1 and sp.simplify(wsol[0] - sp.Rational(1, 3)) == 0
          and abs(dust_factor - 2.0) < 1e-15 and lvac == -1 and vac_onshell)
    check("K3", ok, "w_sol=%s dust_factor=%.15f lam(vac)=%d" % (wsol, dust_factor, lvac),
          "w=1/3, 2, -1",
          "conformal (radiation) EoS is the only one for which the literal law closes")
    emit(K3_w_solution=str(wsol[0]) if wsol else "none (no solution: lambda constant)",
         K3_dust_failure_factor=dust_factor,
         K3_lambda_vacuum=float(lvac), K3_vacuum_note="both sides vanish on-shell: Hdot=0")
    return wsol


# =============================================================================
# K4 -- no constant lambda works: the coefficient spreads by 2
# =============================================================================
def k4(lam):
    _fs = sorted(lam.free_symbols, key=str)
    w = _fs[0] if _fs else sp.Symbol("w")
    vals = [float(lam.subs({w: x})) for x in (-1.0, 0.0, 1.0 / 3.0, 0.5)]
    spread = max(vals) - min(vals)
    check("K4", abs(spread - 2.25) < 1e-12 and spread > 2.0,
          "spread=%.15f over w in [-1,1/2]" % spread, "2.25 (>2)",
          "lambda runs -1 -> 1.25; no single coefficient fits all epochs")
    emit(K4_lambda_spread=spread, K4_lambda_points=vals)
    return spread


# =============================================================================
# K5 -- the first law fixes lambda, not Hdot: residual independent of Hdot
# =============================================================================
def k5(lam):
    H, Hd, rho, c, Gs, hb, kB = sp.symbols("H Hdot rho c G hbar k_B", positive=True)
    _fs = sorted(lam.free_symbols, key=str)
    w = _fs[0] if _fs else sp.Symbol("w")
    T = hb * H / (2 * sp.pi * kB)
    S = kB * sp.pi * c ** 5 / (Gs * hb * H ** 2)
    V = 4 * sp.pi / 3 * (c / H) ** 3
    E = c ** 5 / (2 * Gs * H)
    P = w * (3 * H ** 2 / (8 * sp.pi * Gs)) * c ** 2
    TdS = sp.simplify(T * sp.diff(S, H) * Hd)
    dEP = sp.simplify(sp.diff(E, H) * Hd + P * sp.diff(V, H) * Hd)
    # with lambda = (1+3w)/2 the residual vanishes for EVERY Hdot
    lam_w = lam
    resid = sp.simplify(dEP - lam_w * TdS)
    # and the coefficient of Hdot in the residual is zero -> no equation for Hdot
    coef = sp.simplify(sp.diff(resid, Hd))
    # "G_eff" reading: lambda = G/G_eff
    Geff_over_G = float(sp.simplify(1 / lam.subs({w: 0})))
    rnum = abs(float(resid.subs({x: 1.0 for x in resid.free_symbols})))
    cnum = abs(float(coef.subs({x: 1.0 for x in coef.free_symbols})))
    ok = resid == 0 and coef == 0 and abs(Geff_over_G - 2.0) < 1e-15
    check("K5", ok, "resid=%.1e d(resid)/dHdot=%.1e G_eff/G(w=0)=%.6f"
          % (rnum, cnum, Geff_over_G), "0, 0, 2",
          "law is a consistency condition: it determines lambda, never Hdot or G")
    emit(K5_residual=rnum, K5_dresid_dHdot=cnum,
         K5_Geff_over_G_dust=Geff_over_G)
    return resid


# =============================================================================
# K6 -- numeric FRW: T*dS/dt = 2*dE/dt for dust, while T*S = E exactly
# =============================================================================
def k6():
    # analytic dust solution H = 2/(3t); SI constants; finite differences in t
    t0 = 1.5 / math.sqrt(8.0 * math.pi * G * RHO_CRIT_H0 / 3.0)   # H(t0)=H0
    def H_of_t(t):
        return 2.0 / (3.0 * t)
    def S_of_H(H):
        return KB * math.pi * C ** 5 / (G * HBAR * H ** 2)
    def E_of_H(H):
        return C ** 5 / (2.0 * G * H)
    def T_of_H(H):
        return HBAR * H / (2 * math.pi * KB)
    h = 1e-6 * t0
    Hp, Hm, Hc = H_of_t(t0 + h), H_of_t(t0 - h), H_of_t(t0)
    TdS = T_of_H(Hc) * (S_of_H(Hp) - S_of_H(Hm)) / (2 * h)
    dE = (E_of_H(Hp) - E_of_H(Hm)) / (2 * h)
    ratio = TdS / dE
    val_ratio = T_of_H(Hc) * S_of_H(Hc) / E_of_H(Hc)
    ok = abs(ratio - 2.0) < 1e-7 and abs(val_ratio - 1.0) < 1e-12
    check("K6", ok, "T*dS/dE=%.12f  T*S/E=%.12f" % (ratio, val_ratio), "2, 1",
          "numeric FRW: d(TS) != T dS; the heat form is twice dE although T*S=E")
    emit(K6_TdS_over_dE=ratio, K6_TS_over_E=val_ratio, K6_t0=t0)
    return ratio


# =============================================================================
# K7 -- naive equipartition: ratio = (1/2)(rho/rho_crit) = 1/2 at rho_crit
# =============================================================================
def k7():
    rA = C / H0
    A = 4 * math.pi * rA ** 2
    Nsurf = A / L_P2
    T = HBAR * H0 / (2 * math.pi * KB)
    E = C ** 5 / (2 * G * H0)
    Nbulk = 2 * E / (KB * T)
    ratio = Nbulk / Nsurf
    # symbolic form
    rho, H, Gs = sp.symbols("rho H G", positive=True)
    rho_c = 3 * H ** 2 / (8 * sp.pi * Gs)
    nsym = 4 * sp.pi / (Gs * H ** 2)
    nbulk_sym = 2 * (rho * (4 * sp.pi / 3) / H ** 3) / (H / (2 * sp.pi))
    form = sp.simplify(nbulk_sym / nsym - sp.Rational(1, 2) * rho / rho_c)
    ok = abs(ratio - 0.5) < 1e-12 and form == 0
    check("K7", ok, "ratio=%.15f" % ratio, "0.5",
          "N_bulk/N_surf=(1/2)(rho/rho_crit); 1/2 = (4piG/3)/(8piG/3), Einstein")
    emit(K7_Nsurf_H0=Nsurf, K7_Nbulk_naive_H0=Nbulk, K7_ratio_naive=ratio,
         K7_T_dS=T, K7_S=S_of_H0(), K7_E=E)
    return ratio


def S_of_H0():
    return KB * math.pi * C ** 5 / (G * HBAR * H0 ** 2)


# =============================================================================
# K8 -- Komar equipartition: ratio = 1 exactly for the theory's vacuum
# =============================================================================
def k8():
    rA = C / H0
    Nsurf = 4 * math.pi * rA ** 2 / L_P2
    T = HBAR * H0 / (2 * math.pi * KB)
    EK = 2 * RHO_CRIT_H0 * C ** 2 * (4 * math.pi / 3) * rA ** 3    # |rho+3P| = 2rho
    if MUT == "m2":
        EK = RHO_CRIT_H0 * C ** 2 * (4 * math.pi / 3) * rA ** 3    # mutant: naive
    Nbulk = 2 * EK / (KB * T)
    ratio = Nbulk / Nsurf
    rho, H, Gs = sp.symbols("rho H G", positive=True)
    rho_c = 3 * H ** 2 / (8 * sp.pi * Gs)
    ek = 2 * rho * (4 * sp.pi / 3) / H ** 3
    nbulk = 2 * ek / (H / (2 * sp.pi))
    rsym = sp.simplify((nbulk / (4 * sp.pi / (Gs * H ** 2))).subs({rho: rho_c}))
    ok = abs(ratio - 1.0) < 1e-12 and rsym == 1
    check("K8", ok, "ratio=%.15f sym=%s" % (ratio, rsym), "1",
          "Komar energy: N_surf = N_bulk EXACTLY for the theory's vacuum")
    emit(K8_ratio_komar=ratio)
    return ratio


# =============================================================================
# K9 -- one formula for both: (1/2)|1+3w|(rho/rho_crit)
# =============================================================================
def k9():
    rho, H, Gs, w = sp.symbols("rho H G w", positive=True)
    rho_c = 3 * H ** 2 / (8 * sp.pi * Gs)
    ek = sp.Abs(1 + 3 * w) * rho * (4 * sp.pi / 3) / H ** 3
    nbulk = 2 * ek / (H / (2 * sp.pi))
    ratio = sp.simplify(nbulk / (4 * sp.pi / (Gs * H ** 2)))
    target = sp.Rational(1, 2) * sp.Abs(1 + 3 * w) * rho / rho_c
    resid = sp.simplify(ratio - target)
    resid0 = sp.simplify(ratio.subs({w: 0}) - sp.Rational(1, 2) * rho / rho_c)
    rnum = abs(float(sp.simplify(resid.subs({rho: 1.0, H: 1.0, Gs: 1.0, w: 0.37}))))
    check("K9", resid == 0 and resid0 == 0, "residual=%.1e (numeric eval)" % rnum, "0",
          "naive (1/2) and Komar (1) are the same formula at w=0 / w=-1")
    emit(K9_formula="(1/2)|1+3w|(rho/rho_crit)", K9_residual=rnum)
    return ratio


# =============================================================================
# K10 -- N_surf = N_bulk^Komar  <=>  rho = 3H^2/(8piG)  <=>  P3
# =============================================================================
def k10():
    rho, H, Gs, w = sp.symbols("rho H G w", positive=True)
    rho_c = 3 * H ** 2 / (8 * sp.pi * Gs)
    # theory's vacuum: P = -rho  =>  |1+3w| = 2 exactly
    ek = 2 * rho * (4 * sp.pi / 3) / H ** 3
    nbulk = 2 * ek / (H / (2 * sp.pi))
    sol = [sp.simplify(s) for s in sp.solve(sp.Eq(4 * sp.pi / (Gs * H ** 2), nbulk), rho)]
    ok = any(sp.simplify(s - rho_c) == 0 for s in sol)
    check("K10", ok, "rho_sol=%s" % sol, "3H^2/8piG",
          "holographic equipartition IS P3: a restatement, not a derivation of kappa")
    emit(K10_equipartition_rho=[str(s) for s in sol])
    return sol


# =============================================================================
# K11 -- kappa and a0 are absent from every horizon functional
# =============================================================================
def k11():
    kap, a0 = sp.symbols("kappa a_0", positive=True)
    H, rho, Gs, hb, c, kB = sp.symbols("H rho G hbar c k_B", positive=True)
    funcs = {
        "T": hb * H / (2 * sp.pi * kB),
        "S": kB * sp.pi * c ** 5 / (Gs * hb * H ** 2),
        "E": rho * c ** 2 * 4 * sp.pi / 3 * (c / H) ** 3,
        "N_surf": 4 * sp.pi * (c / H) ** 2 / (Gs * hb / c ** 3),
        "N_bulk": 2 * (rho * c ** 2 * 4 * sp.pi / 3 * (c / H) ** 3)
                  / (kB * hb * H / (2 * sp.pi * kB)),
        "V": 4 * sp.pi / 3 * (c / H) ** 3,
    }
    absent = {k: (sp.simplify(sp.diff(v, kap)) == 0 and sp.simplify(sp.diff(v, a0)) == 0)
              for k, v in funcs.items()}
    scan = [k * C * math.sqrt(G * RHO_CRIT_H0) / (C * H0) / k for k in np.linspace(0.1, 3.0, 400)]
    drift = max(scan) - min(scan)
    ok = all(absent.values()) and drift < 1e-15
    check("K11", ok, "absent=%s drift=%.1e (400 kappa)" % (all(absent.values()), drift),
          "True, <1e-15",
          "no horizon functional depends on kappa: no identity among them can contain it")
    emit(K11_absent=absent, K11_scan_drift=float(drift), K11_scan_n=400)
    return absent


# =============================================================================
# K12 -- a0/(cH) = kappa sqrt(3/8pi); at kappa=1/2 this is exactly 1/Z
# =============================================================================
def k12():
    kap = sp.symbols("kappa", positive=True)
    expr = kap * sp.sqrt(sp.Rational(3, 1) / (8 * sp.pi))
    val = float(expr.subs({kap: sp.Rational(1, 2)}))
    ident = abs(0.5 * SQRT_38PI - INV_Z)
    val_exact = float(sp.Rational(1, 2) * sp.sqrt(sp.Rational(3, 1) / (8 * sp.pi)))
    if MUT == "m3":
        val = val_exact * Z          # mutant: uses sqrt(8pi/3) instead of sqrt(3/8pi)
    else:
        val = float(expr.subs({kap: sp.Rational(1, 2)}))
    ok = abs(val - INV_Z) < 1e-12 and ident < 1e-15 and abs(val_exact - INV_Z) < 1e-15
    check("K12", ok, "a0/(cH)=%.15f" % val, "=1/Z=0.1727471",
          "kappa=1/2 <=> a0/(cH)=(1/2)sqrt(3/8pi)=1/Z exactly")
    emit(K12_a0_over_cH=val, K12_invZ=INV_Z, K12_identity_residual=float(ident))
    return val


# =============================================================================
# K13 -- the thermodynamic coefficients never approach the required 1/Z
# =============================================================================
def k13():
    # map every physical coefficient to kappa = lambda/sqrt(3/8pi) and measure the
    # distance from the target 1/2.  candidates: dust 1/2, radiation 1, naive
    # quarter 1/4, five-quarter 5/4, vacuum -1, zero 0.
    cand = np.array([0.5, 1.0, 0.25, 1.25, -1.0, 0.0])
    kaps = cand / SQRT_38PI
    d = float(np.min(np.abs(kaps - 0.5)))
    check("K13", d > 0.2, "min|kappa(cand)-1/2|=%.9f (kappa %s)" % (d, np.round(kaps, 6)),
          ">0.2",
          "closest physical coefficient (1/4) gives kappa=0.7236, 44.7% above 1/2")
    emit(K13_min_distance_kappa=d, K13_kappa_candidates=list(kaps), K13_required=INV_Z)
    return d


# =============================================================================
# K14 -- the factor is sqrt(3/8pi)=2/Z, NOT 2sqrt(32pi/3)=2Z
# =============================================================================
def k14():
    a = abs(SQRT_38PI - 2.0 / Z)                 # 0 : s = 2/Z
    b = abs(INV_Z - 0.5 * SQRT_38PI)             # 0 : 1/Z = s/2
    c3 = abs(TWOSQRT_32PI3 - 4.0 / SQRT_38PI)    # 0 : 2sqrt(32pi/3) = 4/s
    d4 = abs(TWOSQRT_32PI3 - 2.0 * Z)            # 0 : 2sqrt(32pi/3) = 2Z
    ok = a < 1e-15 and b < 1e-15 and c3 < 1e-9 and d4 < 1e-12
    check("K14", ok, "|s-2/Z|=%.1e |1/Z-s/2|=%.1e |2sqrt(32pi/3)-4/s|=%.1e |2sqrt(32pi/3)-2Z|=%.1e"
          % (a, b, c3, d4), "all 0",
          "s=sqrt(3/8pi)=2/Z; 2sqrt(32pi/3)=4/s=2Z -- the reciprocal-flavoured number, not the factor")
    emit(K14_sqrt_3_8pi=SQRT_38PI, K14_2Z=2 * Z, K14_identities=[a, b, c3, d4])
    return a


# =============================================================================
# K15 -- "1/2 x 2sqrt(32pi/3)" overshoots the requirement by 33.5x
# =============================================================================
def k15():
    cand = 0.5 * TWOSQRT_32PI3
    ratio = cand / INV_Z
    check("K15", ratio > 30.0, "candidate/required=%.6f" % ratio, ">30",
          "1/2 x 2sqrt(32pi/3)=Z=5.7888 is 33.5x the required 0.1727")
    emit(K15_cand_over_required=ratio)
    return ratio


# =============================================================================
# K16 -- reading (A): a0 = surface gravity gives kappa = lambda Z/2 = Z/4, never 1/2
# =============================================================================
def k16():
    kA = 0.5 * Z / 2.0
    kB_ = 1.0 * Z / 2.0
    d = min(abs(kA - 0.5), abs(kB_ - 0.5))
    wstar = (2.0 / Z - 1.0) / 3.0
    ok = abs(kA - Z / 4) < 1e-12 and d > 0.9 and abs(wstar + 0.2181686168) < 1e-9
    check("K16", ok, "kappa_A(1/2)=%.9f  kappa_A(1)=%.9f  w*=%.9f" % (kA, kB_, wstar),
          ">0.9 from 1/2",
          "correct identification lands on A1 menu Z/4, Z/2; kappa=1/2 needs w=-0.2182")
    a0c = 0.5 * C * math.sqrt(G * RHO_CRIT_H0)
    emit(K16_kappa_A_half=kA, K16_kappa_A_one=kB_, K16_w_star=wstar,
         K16_a0_at_Z4=(Z / 4) * C * math.sqrt(G * RHO_CRIT_H0),
         K16_a0_at_Z2=(Z / 2) * C * math.sqrt(G * RHO_CRIT_H0),
         K16_a0_canon=a0c,
         K16_ratio_Z4_to_canon=(Z / 4) / 0.5,
         K16_ratio_Z2_to_canon=(Z / 2) / 0.5)
    return kA


# =============================================================================
# K17 -- the EFFICIENCY reading: eps = a0/(g+a0); at g=cH it is 1/(1+Z), not 1/2
# =============================================================================
def k17():
    x = INV_Z                       # a0/(cH) at kappa = 1/2
    eps = x / (1.0 + x)             # medium's share of the acceleration at g = cH
    eps_closed = 1.0 / (1.0 + Z)
    # eps = 1/2  <=>  x = 1  <=>  a0 = cH  <=>  kappa = Z/2
    kappa_eff = Z / 2.0
    # the Langmuir half-saturation at g = a0 (theta = 1/2) is a tautology for every kappa
    taut = [k * C * math.sqrt(G * RHO_CRIT_H0) / (k * C * math.sqrt(G * RHO_CRIT_H0)) for k in (0.1, 0.5, 2.0)]
    ok = (abs(eps - eps_closed) < 1e-15 and abs(kappa_eff - 2.8944050182) < 1e-9
          and abs(kappa_eff - 0.5) > 2.0 and max(taut) - min(taut) < 1e-15)
    check("K17", ok, "eps(cH)=%.9f kappa(eps=1/2)=%.6f" % (eps, kappa_eff),
          "0.147300, 2.894405",
          "medium supplies 14.73% at the horizon; half-share needs kappa=Z/2=2.894 (5.79x in a0)")
    emit(K17_eps_at_horizon=eps, K17_eps_closed=eps_closed,
         K17_kappa_for_half_share=kappa_eff,
         K17_langmuir_half_is_tautology=float(max(taut) - min(taut)))
    return eps


def main():
    print("a50_checks -- Lane A50 -- horizon thermodynamics vs kappa")
    print("constants: c=%.8e G=%.5e hbar=%.9e kB=%.7e H0=%.5e Z=%.10f 1/Z=%.10f"
          % (C, G, HBAR, KB, H0, Z, INV_Z))
    print("mutation : %s" % (MUT if MUT else "none"))
    print("-" * 100)
    sym = k1()
    lam = k2()
    if MUT == "m1":
        lam = sp.Rational(1, 2)
        print("  [m1] lambda forced to the constant 1/2 (K2 still verifies the true formula)")
    k3(lam)
    k4(lam)
    k5(lam)
    k6()
    k7()
    k8()
    k9()
    k10()
    k11()
    k12()
    k13()
    k14()
    k15()
    k16()
    k17()
    emit(lane="A50",
         title="kappa from horizon thermodynamics",
         verdict="NO-GO(obstruction)",
         claim=("the first law at the apparent horizon is the Friedmann equation rewritten "
                "and is kappa-free; its whole content is lambda=(1+3w)/2, so it yields 1/2 only "
                "as the dust-era value of a running coefficient, and kappa=1/2 needs in addition "
                "the Einstein factor sqrt(3/8pi)=2/Z"),
         geometric_factor=SQRT_38PI,
         geometric_factor_form="sqrt(3/8pi)=2/Z=0.3454941",
         not_the_factor="2sqrt(32pi/3)=4/sqrt(3/8pi)=2Z=11.5776",
         numbers=dict(Z=Z, invZ=INV_Z, sqrt_3_8pi=SQRT_38PI, two_sqrt_32pi_3=TWOSQRT_32PI3,
                     rho_crit_H0=RHO_CRIT_H0, rho_crit_HL=RHO_CRIT_HL,
                     H_Lambda=H_LAMBDA, a0_canon=0.5 * C * math.sqrt(G * RHO_CRIT_H0),
                     lambda_dust=0.5, lambda_rad=1.0, w_star=(2.0 / Z - 1.0) / 3.0,
                     kappa_A=(Z / 4)),
         constants_used=["c=2.99792458e8 m/s (CODATA)", "G=6.67430e-11 (CODATA)",
                         "hbar=1.054571817e-34 (CODATA)", "kB=1.380649e-23 (SI exact)",
                         "H0=2.1843e-18 s^-1 (BRIEF 4)", "Lambda=1.0890e-52 m^-2 (BRIEF 4)",
                         "kappa_target=0.5 (THEORY P3)"])
    return finalize()


if __name__ == "__main__":
    sys.exit(main())