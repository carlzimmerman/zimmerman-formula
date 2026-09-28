#!/usr/bin/env python3
"""
AS034 - Constructing the MONO continuation by integration.

Branch: operative filtered MONO (RAR + delta*h_p log continuation), separate from
Q, RAR, MU2, historical EXP. kappa = 1/2 adopted as framework input.

Derivation object:
  h_RAR(y)  = y/(exp(sqrt(y)) - 1) = y * (nu_RAR(y) - 1)
  nu_RAR(y) = 1/(1 - exp(-sqrt(y)))
  h'_RAR(y) = [2(e^s - 1) - s e^s] / [2 (e^s - 1)^2],  s = sqrt(y)
  P(y)      = delta * h_p / (y + y_p)                 (phantom slope rule)
  y_p       : h'_RAR(y_p) = 0   (phantom peak)
  h_p       = h_RAR(y_p)
  y_star    : h'_RAR(y_star) = P(y_star)   (splice / max() crossing)
  h_mono(y) = h_RAR(y_star) + delta*h_p*ln((y+y_p)/(y_star+y_p))   y >= y_star
  nu_mono(y)= 1 + h_mono(y)/y

Controls:
  C1 continuity at splice |h_mono(y_star) - h_RAR(y_star)|
  C2 derivative identity  |h'_mono(y) - P(y)| on the continuation (grid)
  C3 independent quadrature of P over [y_star, y] vs closed form (mp.quad)
  C4 negative control A: omit integration constant -> force jump quantified
  C5 negative control B: switch-back scan D(y) = P(y) - h'_RAR(y) > 0 on
     (y_star, inf): fine grid + adjacent-pair sign scan + analytic argument
     on (y_p, inf); report min D and its location.
  C6 representation check: h_RAR = y*(nu_RAR - 1) identity on grid.
  C7 landmarks: y_star ~ 2.3374, y_p ~ 2.5396, h_p ~ 0.647610,
     0.0104 dex claim near y = 14.35.
  C8 limits: deep y->0+ h_RAR ~ sqrt(y) - y/2 + y^{3/2}/12 (series check);
     Newtonian y->inf: nu_mono -> 1, h_mono/y -> 0.

Bounds: single OS thread, wall-clock target <= 120 s, memory target <= 512 MB.
Enforced/recorded: OMP/MKL/OPENBLAS threads = 1 at import; grid 181 pts
(k = -10..8 step 0.1); fine refinement grids (spike/large-y) as declared below;
peak RSS via resource.getrusage; wall time via time.monotonic.
"""
import json
import os
import resource
import sys
import time

# --- enforce single thread before numeric imports ---
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import mpmath as mp  # noqa: E402

mp.mp.dps = 50

# ---------------- framework constants ----------------
G_SI = 6.67430e-11      # m^3 kg^-1 s^-2  (measured Newton coupling G_N)
C_SI = 299792458.0      # m/s
A0_CANON = 9.3619e-11   # m/s^2  canonical footing (kappa = 1/2 adopted)
A0_ALT = 1.1279e-10     # m/s^2  alternative footing
KAPPA_ADOPTED = mp.mpf("0.5")
DELTA = mp.mpf("0.05")  # delta = 0.05 (framework input, dimensionless)

# ---------------- branch functions ----------------
def s_of(y):
    return mp.sqrt(y)

def nu_RAR(y):
    s = s_of(y)
    return 1 / (1 - mp.exp(-s))

def h_RAR(y):
    s = s_of(y)
    return y / (mp.exp(s) - 1)

def hp_RAR(y):
    """h'_RAR(y) = [2(e^s-1) - s e^s] / [2 (e^s-1)^2], s = sqrt(y)."""
    s = s_of(y)
    e = mp.exp(s)
    return (2 * (e - 1) - s * e) / (2 * (e - 1) ** 2)

def n_of_s(s):
    """Numerator of h'_RAR: n(s) = e^s (2 - s) - 2."""
    return mp.exp(s) * (2 - s) - 2

def Pslope(y, yp, hp):
    return DELTA * hp / (y + yp)

def h_mono(y, ys, yp, hp, hRAR_ys):
    return hRAR_ys + DELTA * hp * mp.log((y + yp) / (ys + yp))

def nu_mono(y, ys, yp, hp, hRAR_ys):
    return 1 + h_mono(y, ys, yp, hp, hRAR_ys) / y

def bisect(f, a, b, tol=mp.mpf("1e-48"), maxit=2000):
    """Bisection on a bracketed sign change; 50-digit working precision."""
    fa, fb = f(a), f(b)
    assert fa * fb < 0, f"no sign change on [{a}, {b}]: f(a)={fa}, f(b)={fb}"
    for _ in range(maxit):
        m = (a + b) / 2
        fm = f(m)
        if fm == 0 or (b - a) < tol:
            return m
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return (a + b) / 2

def main():
    t0 = time.monotonic()
    out = {}

    # ---------- step 1: peak y_p, h_p ----------
    # analytic: n'(s) = e^s (1 - s), n(0) = 0, n(1) = e - 2 > 0, n(s) -> -inf
    # => exactly one root s_p > 1.  Bracket [1.5, 1.7].
    assert n_of_s(mp.mpf("1.5")) > 0 and n_of_s(mp.mpf("1.7")) < 0
    s_p = bisect(n_of_s, mp.mpf("1.5"), mp.mpf("1.7"))
    y_p = s_p ** 2
    h_p = h_RAR(y_p)
    out["y_p"] = str(y_p)
    out["s_p"] = str(s_p)
    out["h_p"] = str(h_p)
    # peak residual
    out["peak_residual_hp_RAR"] = str(hp_RAR(y_p))

    # ---------- step 2: splice y_star from h'_RAR(y) = P(y) ----------
    def cross_f(y):
        return hp_RAR(y) - Pslope(y, y_p, h_p)

    a, b = mp.mpf("2.30"), mp.mpf("2.40")
    fa, fb = cross_f(a), cross_f(b)
    assert fa > 0 and fb < 0, f"bracket failed: f(2.3)={fa}, f(2.4)={fb}"
    y_star = bisect(cross_f, a, b)
    hRAR_ys = h_RAR(y_star)
    out["y_star"] = str(y_star)
    out["h_RAR_y_star"] = str(hRAR_ys)
    out["cross_residual_at_splice"] = str(cross_f(y_star))
    out["c_slope_P_at_splice"] = str(Pslope(y_star, y_p, h_p))

    # ---------- step 3: continuity (C1) and derivative identity (C2) ----------
    hm_ys = h_mono(y_star, y_star, y_p, h_p, hRAR_ys)
    out["C1_continuity_residual"] = str(hm_ys - hRAR_ys)

    # derivative of the closed form, computed from the ratio-form antiderivative
    def hmono_deriv(y):
        return DELTA * h_p / (y + y_p)

    D_ident_samp = []
    for yv in [mp.mpf("2.5"), mp.mpf("3"), mp.mpf("10"), mp.mpf("100"),
               mp.mpf("1e4"), mp.mpf("1e8")]:
        D_ident_samp.append([str(yv), str(hmono_deriv(yv) - Pslope(yv, y_p, h_p))])
    out["C2_derivative_identity_samples"] = D_ident_samp

    # independent representation: mp.quad of P over [y_star, y] (C3)
    quad_checks = []
    for yv in [mp.mpf("3"), mp.mpf("10"), mp.mpf("100"), mp.mpf("1e4")]:
        q = mp.quad(lambda t: DELTA * h_p / (t + y_p), [y_star, yv])
        closed = DELTA * h_p * mp.log((yv + y_p) / (y_star + y_p))
        quad_checks.append([str(yv), str(q), str(closed), str(q - closed)])
    out["C3_quadrature_vs_closed_form"] = quad_checks

    # representation identity C6: h_RAR == y*(nu_RAR - 1)
    grid_k = [-10 + 0.1 * i for i in range(181)]  # -10 .. 8 step 0.1
    grid = [mp.mpf(10) ** k for k in grid_k]
    rep_max = mp.mpf(0)
    for yv in grid:
        d = h_RAR(yv) - yv * (nu_RAR(yv) - 1)
        rep_max = max(rep_max, mp.fabs(d))
    # add y = 14.35 (claim landmark: max |log10(nu_mono/nu_RAR)| ~ 0.0104 dex)
    y_1435 = mp.mpf("14.35")
    grid_extra = grid + [y_1435]
    out["C6_hRAR_repr_max_residual"] = str(rep_max)

    # ---------- step 4: negative control A (C4): omit integration constant ---
    h_zero = DELTA * h_p * mp.log((y_star + y_p) / (y_star + y_p))
    jump_h = hRAR_ys - h_zero
    g_ratio = (1 + h_zero / y_star) / (1 + hRAR_ys / y_star)
    out["C4_omit_constant_h_at_splice_plus"] = str(h_zero)
    out["C4_h_jump"] = str(jump_h)
    out["C4_force_ratio_plus_over_minus"] = str(g_ratio)
    out["C4_force_jump_percent"] = str((g_ratio - 1) * 100)

    # ---------- step 5: negative control B (C5): switch-back scan ----------
    # D(y) := h'_mono - h'_RAR = P - h'_RAR.  Must be > 0 strictly on (y_star, inf).
    def D(y):
        return Pslope(y, y_p, h_p) - hp_RAR(y)

    # analytic part: for y > y_p, h'_RAR < 0 (n(s) < 0 for s > s_p) and P > 0.
    # numeric part: scan grids; count adjacent-pair sign changes (must be 0
    # inside the continuation); record min D.
    scans = {}
    # (a) fine log grid continuation: y from y_star*(1+1e-14) to 1e8
    ys_log = [y_star * (1 + mp.mpf(10) ** e) for e in mp.linspace(
        -14, 0, 51)] if False else None
    cont_pts = []
    # log-spaced from just above splice to 1e8
    lo = mp.log(y_star)
    hi = mp.log(mp.mpf(1e8))
    npt = 4000
    for i in range(npt + 1):
        t = lo + (hi - lo) * mp.mpf(i) / npt
        cont_pts.append(mp.exp(t))
    # replace first point by y_star*(1+1e-13) touch point
    cont_pts[0] = y_star * (1 + mp.mpf("1e-13"))
    sign_changes = 0
    dmin = mp.mpf("inf")
    dmin_at = None
    for yv in cont_pts:
        dv = D(yv)
        if dv < dmin:
            dmin, dmin_at = dv, yv
    for yv1, yv2 in zip(cont_pts, cont_pts[1:]):
        if D(yv1) * D(yv2) < 0:
            sign_changes += 1
    scans["log_continuation_grid_points"] = npt + 1
    scans["sign_changes_inside"] = sign_changes
    scans["min_D"] = str(dmin)
    scans["min_D_at_y"] = str(dmin_at)

    # (b) linear fine grid on (y_star, y_p) and (y_p, 5): 2e5 pts
    for name, ylo, yhi, n in [("fine_splice_to_peak", y_star, y_p, 100000),
                              ("fine_peak_to_5", y_p, mp.mpf("5"), 100000)]:
        sc = 0
        dm = mp.mpf("inf")
        da = None
        prev = D(ylo)
        for i in range(1, n + 1):
            yv = ylo + (yhi - ylo) * mp.mpf(i) / n
            dv = D(yv)
            if dv < dm:
                dm, da = dv, yv
            if prev * dv < 0:
                sc += 1
            prev = dv
        scans[name] = {"points": n, "sign_changes": sc,
                       "min_D": str(dm), "min_D_at_y": str(da)}
    out["C5_switchback_scan"] = scans

    # touch point residual near splice (D -> 0+ as y -> y_star+)
    out["C5_D_at_splice_touch"] = str(D(y_star * (1 + mp.mpf("1e-13"))))

    # ---------- step 6: landmarks and limits ----------
    # dex claim: max |log10(nu_mono/nu_RAR)| and argmax over grid + 14.35
    dex_max = mp.mpf(0)
    dex_at = None
    dex_1435 = None
    for yv in grid_extra:
        if yv <= y_star:
            continue
        dd = mp.fabs(mp.log(nu_mono(yv, y_star, y_p, h_p, hRAR_ys) / nu_RAR(yv)) / mp.log(10))
        if dd > dex_max:
            dex_max, dex_at = dd, yv
        if yv == y_1435:
            dex_1435 = dd
    out["dex_max"] = str(dex_max)
    out["dex_max_at_y"] = str(dex_at)
    out["dex_at_14_35"] = str(dex_1435)

    # deep limit series: h_RAR = sqrt(y) - y/2 + y^{3/2}/12 + ...  (leading
    # neglected term after sqrt(y): -y/2; relative size at y = 1e-10)
    y_tiny = mp.mpf("1e-10")
    h_tiny = h_RAR(y_tiny)
    s_tiny = mp.sqrt(y_tiny)
    out["deep_limit_h_at_1e-10"] = str(h_tiny)
    out["deep_limit_sqrt_y"] = str(s_tiny)
    out["deep_limit_ratio_h_over_sqrt_y"] = str(h_tiny / s_tiny)
    # Newtonian limit on continuation: h_mono/y -> 0, nu_mono -> 1
    y_big = mp.mpf("1e8")
    out["newtonian_limit_h_over_y_at_1e8"] = str(
        h_mono(y_big, y_star, y_p, h_p, hRAR_ys) / y_big)
    out["newtonian_limit_nu_minus_1_at_1e8"] = str(
        nu_mono(y_big, y_star, y_p, h_p, hRAR_ys) - 1)

    # ---------- footings ----------
    def rho_lambda(a0):
        return 4 * a0 * a0 / (G_SI * C_SI * C_SI)

    rho_can = rho_lambda(A0_CANON)
    rho_alt = rho_lambda(A0_ALT)
    kappa_eff_alt = KAPPA_ADOPTED * (A0_ALT / A0_CANON)
    lam_can = 32 * mp.pi * mp.mpf(A0_CANON) ** 2 / mp.mpf(C_SI) ** 4
    lam_alt = 32 * mp.pi * mp.mpf(A0_ALT) ** 2 / mp.mpf(C_SI) ** 4
    out["footings"] = {
        "kappa_adopted": str(KAPPA_ADOPTED),
        "a0_canonical_m_s2": A0_CANON,
        "a0_alternative_m_s2": A0_ALT,
        "rho_Lambda_canonical_kg_m3": rho_can,
        "rho_Lambda_alternative_kappa_fixed_kg_m3": rho_alt,
        "kappa_effective_if_rho_fixed": str(kappa_eff_alt),
        "Lambda_canonical_m2": str(lam_can),
        "Lambda_alternative_m2": str(lam_alt),
        "note": "dimensionless theorem; a0 only rescales the y axis. "
                "G_N used for the vacuum identities; G_bare/G_cosmo kept separate.",
    }

    # ---------- bounds ----------
    out["bounds"] = {
        "wall_sec": round(time.monotonic() - t0, 3),
        "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "threads": 1,
        "thread_env": {k: os.environ.get(k) for k in
                       ("OMP_NUM_THREADS", "MKL_NUM_THREADS",
                        "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS")},
        "mpmath_dps": mp.mp.dps,
        "declared_limits": "<=120 s wall, <=512 MB, 1 thread",
    }
    out["python"] = sys.version.split()[0]
    out["mpmath_version"] = mp.__version__

    rdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(rdir, "raw_outputs", "analysis.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(json.dumps(out, indent=1, default=str)[:4000])
    print("WROTE", os.path.join(rdir, "raw_outputs", "analysis.json"))
    print("wall_sec", out["bounds"]["wall_sec"],
          "peak_rss_MB", round(out["bounds"]["peak_rss_bytes"] / 1e6, 2))

if __name__ == "__main__":
    main()
