"""w2_lib -- shared machinery of lane W2 (declared in W2_PREREGISTRATION.md).  Not a script; imported by w2_*.py.
Imports lane B `rg_common` and lane N1 `n1_lib` READ-ONLY (path-relative).  No bytecode.
Contents: the QED-only toy running (one and two loop, thresholds), the U(1)_Y one-loop line, the N1 two-loop SM run with a pole event, lane D's bar call.
"""
import sys
sys.dont_write_bytecode = True
import os, math
import numpy as np
import mpmath as mp
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "B_rg_asymptotic_safety"))
sys.path.insert(0, os.path.join(HERE, "..", "N1_joint_couplings"))
sys.path.insert(0, os.path.join(HERE, "..", "D_calibration_bar"))
import rg_common as RGC     # noqa: E402  (lane B, read only)
import n1_lib as N1         # noqa: E402  (lane N1, read only)

PI = math.pi
ALPHA_INV0 = RGC.ALPHA_INV0                 # 137.035999177
MZ, MT = RGC.MZ, RGC.MT
XP = RGC.MPL                                # 1.220890e19
XR = RGC.MPL_RED                            # 2.435e18
XS = XR / math.sqrt(118)
XG = 2.0e16                                 # declared conventional GUT-scale number (not derived)
SCALES = {"X_G": XG, "X_S": XS, "M_red": XR, "M_P": XP}
B_Y = RGC.B_Y                               # 41/6
SET_A, SET_B = N1.SET_A, N1.SET_B
A_Y_MZ = {"A": RGC.ALPHA_INV_MZ * (1 - RGC.S2W), "B": SET_B["alpha_inv"] * (1 - SET_B["s2w"])}


# ---------------------------------------------------------------- QED-only toy (lane I convention)
def toy_table(setno):
    """rows (name, m GeV, N_c Q^2, N_c Q^4)  -- lane B fermion tables 1 (current) or 2 (constituent light quarks)."""
    rows = []
    for name, m, nq2 in RGC.fermions(setno):
        # N_c Q^4 from N_c Q^2 : leptons Q=1 (nq2=1 -> 1); up-type 3*4/9 -> 3*16/81; down-type 3*1/9 -> 3/81
        if abs(nq2 - 1.0) < 1e-12:
            nq4 = 1.0
        elif abs(nq2 - 12 / 9) < 1e-12:
            nq4 = 3 * 16 / 81
        else:
            nq4 = 3 / 81
        rows.append((name, m, nq2, nq4))
    return rows


def S_oneloop(rows, M, coef=2 / (3 * PI)):
    """S(M) = (2/3pi) sum_{m<M} N_c Q^2 ln(M/m):  1/alpha(M) = 1/alpha_0 - S(M)  (lane I convention)."""
    return coef * sum(nq2 * math.log(M / m) for _, m, nq2, _ in rows if M > m)


def pole_scale_oneloop(rows, u0=ALPHA_INV0, coef=2 / (3 * PI), w_b=0.0, m_w=80.379):
    """ln of the pole scale (GeV) when all fermions are active (and optionally a W with b_W = w_b above m_w).
    1/alpha(M) = u0 - coef*[ sum nq2 ln(M/m) ] - (w_b/2pi) ln(M/m_w) =0 solved for ln M (all thresholds below M)."""
    S1 = sum(r[2] for r in rows)
    c1 = coef * S1 + w_b / (2 * PI)
    rhs = u0 + coef * sum(r[2] * math.log(r[1]) for r in rows) + (w_b / (2 * PI)) * math.log(m_w)
    # u0 - coef*sum nq2 (lnM - ln m) - (w_b/2pi)(lnM - ln m_w) = 0
    return rhs / c1        # ln(M/GeV)


def pole_scale_twoloop(rows, u0=ALPHA_INV0):
    """Two-loop QED-only toy: d alpha/d ln mu = (2 S1/3pi) alpha^2 + (S2/2pi^2) alpha^3, thresholds at the fermion masses.
    Variable w = u^2 (u = 1/alpha):  dw/dt = -2 b1 sqrt(w) - 2 c.  Returns ln(M_pole/GeV)."""
    rows = sorted(rows, key=lambda r: r[1])
    t = math.log(rows[0][1])
    w = u0 ** 2
    edges = [math.log(r[1]) for r in rows] + [math.log(1e300)]
    for i in range(len(rows)):
        S1 = sum(r[2] for r in rows[: i + 1])
        S2 = sum(r[3] for r in rows[: i + 1])
        b1, c = 2 / (3 * PI) * S1, S2 / (2 * PI ** 2)
        f = lambda tt, y: [-2 * b1 * math.sqrt(max(y[0], 0.0)) - 2 * c]
        ev = lambda tt, y: y[0] - 1e-12
        ev.terminal = True
        ev.direction = -1
        sol = solve_ivp(f, [t, edges[i + 1]], [w], events=ev, rtol=1e-12, atol=1e-14, method="LSODA")
        if sol.t_events[0].size:
            return float(sol.t_events[0][0])
        t, w = edges[i + 1], float(sol.y[0, -1])
    return float("inf")


def twoloop_closed_single(S1, S2, alpha0, m):
    """Closed form for ONE active species set: ln(Lambda/m) = (1/b1)[1/alpha0 + r ln(r alpha0/(1+r alpha0))], r = c/b1, b1 = 2 S1/3pi, c = S2/2pi^2."""
    b1, c = 2 * S1 / (3 * PI), S2 / (2 * PI ** 2)
    r = c / b1
    return (1 / b1) * (1 / alpha0 + r * math.log(r * alpha0 / (1 + r * alpha0)))


# ---------------------------------------------------------------- U(1)_Y one loop and the N1 two-loop pole
def aY_oneloop(mu, inp="A", bY=B_Y, extra=()):
    """a_Y(mu) one loop from m_Z; extra = iterable of (N, db, m) unit multiplets switching on at m (db added to b_Y for mu>m)."""
    a = A_Y_MZ[inp] - bY / (2 * PI) * math.log(mu / MZ)
    for N, db, m in extra:
        if mu > m:
            a -= N * db / (2 * PI) * math.log(mu / m)
    return a


def pole_aY_oneloop(inp="A", extra=()):
    """ln(mu_pole/GeV) with a_Y(mu_pole)=0, one loop, SM desert plus extra multiplets (each (N, db, m))."""
    A0 = A_Y_MZ[inp]
    tot_b = B_Y + sum(N * db for N, db, m in extra)
    # a = A0 - B/2pi (L - LZ) - sum N db/2pi (L - ln m)
    num = A0 + B_Y / (2 * PI) * math.log(MZ) + sum(N * db / (2 * PI) * (-math.log(m)) * (-1) for N, db, m in extra) * 0
    # solve linearly
    lnMZ = math.log(MZ)
    const = A0 + (B_Y / (2 * PI)) * lnMZ + sum((N * db / (2 * PI)) * math.log(m) for N, db, m in extra)
    return const / (tot_b / (2 * PI))


def need_N_Y(X, inp="A", db=4 / 3, m=1000.0):
    """Number of unit-hypercharge Dirac singlets at m (Delta b_Y = 4/3 each) so that the one-loop a_Y(X)=0 with the MEASURED a_Y(m_Z)."""
    A0 = A_Y_MZ[inp]
    base = A0 - B_Y / (2 * PI) * math.log(X / MZ)          # a_Y(X) without extra content (negative if the SM pole is below X)
    return base / (db / (2 * PI) * math.log(X / m))


def sm_twoloop_run(inp="A", tmax=math.log(1e45)):
    """Central 2L-A/2L-B run (lane N1 Runner RHS), dense output, with an event a_Y = 0.  Returns (sol, ln_pole or None, runner)."""
    R = N1.Runner()
    inp_d = N1.SET_A if inp == "A" else N1.SET_B
    y0 = list(N1.boundaries(inp_d)) + [R.yt_at_mz(inp_d)]
    ev = lambda t, y: y[0] - 1e-3
    ev.terminal = True
    ev.direction = -1
    sol = solve_ivp(lambda t, y: R._rhs(t, y), [math.log(MZ), tmax], y0, rtol=1e-10, atol=1e-12, dense_output=True, events=ev, method="LSODA")
    lp = float(sol.t_events[0][0]) if sol.t_events[0].size else None
    return sol, lp, R


# ---------------------------------------------------------------- lane D's bar
def bar(delta, n_hits=20, predicted_precision=0.01):
    import alpha_bar_checker as ABC
    return ABC.assess(delta=abs(delta), log2size=math.log2(n_hits), n_targets=1, predicted_precision=predicted_precision, fitted_reals=0, scale_stated=True, verbose=False)


def finish(fails, mutate, name):
    """Exit-code convention: real run exit 0 iff no failures; MUTATE run exit 1 if some check failed (control bites), 3 if none failed (control broken)."""
    if mutate:
        code = 1 if fails else 3
        print(f"[{name} MUTATE] failed checks: {fails if fails else 'NONE (control broken)'} -> exit {code}")
    else:
        code = 1 if fails else 0
        print(f"[{name}] failed checks: {fails if fails else 'none'} -> exit {code}")
    sys.exit(code)
