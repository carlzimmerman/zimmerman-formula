"""
mc_gates.py -- the cheap numeric gates.

Order (cheapest first, short-circuit on failure):
    Gate-H        kinetic Hessian of the carrier multiplet -> {healthy, ghost, degenerate}
                  PRE-screen: kill only on a ROBUST ghost (negative kinetic eigenvalue at
                  EVERY reference background).  Conservative by construction.
    Gate-CARRIER  does the carrier turn ON and change the dynamics?  (the minimal AC-MOND
                  archetype died here: A_mu = 0 on the regular branch)
    Gate-MOND     quasistatic reduction -> div[mu grad Phi] = 4 pi G rho with
                  mu -> 1 (Newtonian, G3: no rescaling of G) and mu -> y (deep MOND)
    Gate-SLIP     Sigma_P = 0 (traceless carrier stress) AND lensing potential == dynamical
                  potential in the matter frame, at EVERY sampled y, by CANCELLATION
                  (individual contributions nonzero) rather than by everything vanishing
    Gate-H2       Hessian re-evaluated at the candidate's OWN solved background, with the
                  constraint-vs-strong-coupling classification
    Gate-PPN      preferred-frame: a boost-INVARIANT carrier vacuum proves alpha_1 =
                  alpha_2 = 0; a boost-breaking vacuum is reported as PARTIAL (the exact
                  1PN alpha_2 is a stage-2 object -- never fabricated here)

Units: c = 1, a0 = 1, 16 pi G = 1.  In these units pure GR gives, for a sheet of surface
density Sigma, Phi' = Psi' = Sigma/8 = 2 pi G Sigma  (verified in mc_validate.py).
"""
import numpy as np
import mc_reduce_static as RS
import mc_reduce_hessian as RH
from mc_basis import N_OPS, N_PARAM, OP_IDS

NEWTON_G_FACTOR = 1.0 / 8.0        # g_N = Sigma * NEWTON_G_FACTOR  (pure GR, verified)

# indices into the static unknown vector
IX = {n: i for i, n in enumerate(RS.UNKNOWNS)}

_R = None


def _rt():
    global _R
    if _R is None:
        _R = RS.load()
    return _R


# ----------------------------------------------------------------------------------
# static solve
# ----------------------------------------------------------------------------------

def residual_and_jac(cext, mpar, Sigma, X):
    X = np.asarray(X, dtype=float)
    """returns (R, J, per-equation scale, M-matrix).

    The per-equation scale is the largest single TERM entering that equation, so the
    convergence test is a genuine relative-cancellation test rather than an absolute one
    (the equations span many orders of magnitude across the Sigma scan).
    """
    r = _rt()
    Mv = np.asarray(r["Mfun"](*X), dtype=float).reshape(N_OPS + 1, RS.N_COL)
    terms = cext[:, None] * Mv[:, :RS.N_EQ]
    R = terms.sum(axis=0)
    src = np.asarray(r["Sfun"](*X, *mpar), dtype=float).ravel()
    ssrc = 0.5 * Sigma * src
    R[6:15] += ssrc

    Jv = np.asarray(r["Jfun"](*X), dtype=float).reshape(N_OPS + 1, RS.N_COL, RS.N_UNK)
    JR = np.einsum('i,ijk->jk', cext, Jv)[:RS.N_EQ].copy()
    SJ = np.asarray(r["SJfun"](*X, *mpar), dtype=float).reshape(9, RS.N_UNK)
    JR[6:15] += 0.5 * Sigma * SJ

    # Row scale = natural MAGNITUDE of each equation, |J|.|X| + |source|.  (Using the
    # per-operator term magnitudes instead fails: an equation fed by a single operator
    # -- e.g. the EH row -4 Phi' + 4 Psi' -- would have scale == residual and could never
    # converge.  Verified failure mode.)
    xtyp = max(1e-8, 0.01 * float(np.abs(X).max()) if X.size else 1e-8)
    mag = np.abs(JR) @ (np.abs(X) + xtyp)
    mag[6:15] += np.abs(ssrc)
    gs = float(mag.max()) if mag.size else 0.0
    sc = np.maximum(mag, max(1e-4 * gs, 1e-300))
    return R, JR, sc, Mv


def solve_static(cext, mpar, Sigma, X0, maxit=30, tol=1e-9):
    """damped Gauss-Newton with Tikhonov regularisation (handles inert directions)."""
    X = np.array(X0, dtype=float)
    lam = 1e-6
    best = None
    hist = []
    for _ in range(maxit):
        try:
            R, J, sc, Mv = residual_and_jac(cext, mpar, Sigma, X)
        except (FloatingPointError, ValueError, ZeroDivisionError):
            return None, False, {}
        if not np.all(np.isfinite(R)) or not np.all(np.isfinite(J)):
            return None, False, {}
        Rn_ = R / sc
        Jn_ = J / sc[:, None]
        err = float(np.max(np.abs(Rn_)))
        if best is None or err < best[0]:
            best = (err, X.copy(), Mv)
        if err < tol:
            return X, True, dict(err=err, Mv=Mv)
        hist.append(err)
        # early bail-out: a stalled trajectory will not converge and costs the screen
        if len(hist) >= 9 and err > 1e-6 and hist[-9] < err * 1.05:
            break
        A = Jn_.T @ Jn_
        tr = np.trace(A) / max(len(A), 1)
        A = A + (lam * max(tr, 1e-30) + 1e-14) * np.eye(len(A))
        try:
            dx = -np.linalg.solve(A, Jn_.T @ Rn_)
        except np.linalg.LinAlgError:
            return (best[1] if best else None), False, dict(err=err)
        nrm = np.linalg.norm(dx)
        if not np.isfinite(nrm):
            return (best[1] if best else None), False, dict(err=err)
        step = max(1.0, np.linalg.norm(X))
        if nrm > 2.0 * step:
            dx *= 2.0 * step / nrm
        # line search on a merit function evaluated with the CURRENT row scale
        # (re-normalising at the trial point makes the merit non-monotonic and stalls
        # the solver -- verified failure mode on the unit-timelike multiplier sector)
        merit0 = float(np.linalg.norm(Rn_))
        ok = False
        for _bt in range(12):
            Xn = X + dx
            try:
                Rq, _, _, _ = residual_and_jac(cext, mpar, Sigma, Xn)
            except Exception:
                dx *= 0.5
                continue
            if np.all(np.isfinite(Rq)) and float(np.linalg.norm(Rq / sc)) < merit0 * (1 - 1e-10):
                X = Xn
                ok = True
                lam = max(lam * 0.4, 1e-12)
                break
            dx *= 0.5
        if not ok:
            lam *= 10.0
            if lam > 1e8:
                break
    if best is not None and best[0] < max(tol * 100, 1e-8):
        return best[1], True, dict(err=best[0], Mv=best[2])
    return (best[1] if best else None), False, dict(err=(best[0] if best else np.inf))


# ----------------------------------------------------------------------------------
# observables in the matter frame
# ----------------------------------------------------------------------------------

def observables(X, mpar):
    """matter-frame potential gradients.

    g~_mn = e^{2(m1 phi + m2 chi)} [ g_mn + (m3+m5 phi) A_m A_n + (m4+m6 phi) S_mn
                                          + (m7+m8 phi) d_m phi d_n phi ]
    Phi~ from g~_00 ; Psi~ from the TRACE-AVERAGED spatial block (a stage-1 proxy: a
    disformal d_m phi d_n phi term makes the spatial metric anisotropic, and the exact
    light-bending integral along the line of sight is a stage-2 object).
    Test particles feel  a = -grad Phi~ ; lensing feels (Phi~ + Psi~)/2.
    """
    m1, m2, m3, m4, m5, m6, m7, m8 = mpar
    Phi1 = X[IX["Phi1"]]; Psi1 = X[IX["Psi1"]]; phi1 = X[IX["phi1"]]
    chi0 = X[IX["chi0"]]; chi1 = X[IX["chi1"]]
    A00 = X[IX["A00"]]; A01 = X[IX["A01"]]
    Az0 = X[IX["Az0"]]; Az1 = X[IX["Az1"]]
    S000 = X[IX["S000"]]; S001 = X[IX["S001"]]
    Szz0 = X[IX["Szz0"]]; Szz1 = X[IX["Szz1"]]

    conf0 = 1.0 + 2.0 * m2 * chi0
    confp = 2.0 * (m1 * phi1 + m2 * chi1)
    dA0, dAp = m3, m5 * phi1
    dS0, dSp = m4, m6 * phi1
    dP0, dPp = m7, m8 * phi1

    B00_0 = -1.0 + dA0 * A00 ** 2 + dS0 * S000
    B00_p = (-2.0 * Phi1 + dAp * A00 ** 2 + dA0 * 2.0 * A00 * A01
             + dSp * S000 + dS0 * S001)
    Phit1 = -0.5 * (confp * B00_0 + conf0 * B00_p)

    Sxx0 = 0.5 * (S000 - Szz0); Sxxp = 0.5 * (S001 - Szz1)
    Bxx_0 = 1.0 + dS0 * Sxx0
    Bxx_p = -2.0 * Psi1 + dSp * Sxx0 + dS0 * Sxxp
    Bzz_0 = 1.0 + dA0 * Az0 ** 2 + dS0 * Szz0 + dP0 * phi1 ** 2
    Bzz_p = (-2.0 * Psi1 + dAp * Az0 ** 2 + dA0 * 2.0 * Az0 * Az1
             + dSp * Szz0 + dS0 * Szz1 + dPp * phi1 ** 2)
    Bsp_0 = (2.0 * Bxx_0 + Bzz_0) / 3.0
    Bsp_p = (2.0 * Bxx_p + Bzz_p) / 3.0
    Psit1 = -0.5 * (confp * Bsp_0 + conf0 * Bsp_p)

    return dict(g_dyn=Phit1, g_lens=0.5 * (Phit1 + Psit1), Phit1=Phit1, Psit1=Psit1)


def carrier_norm(X):
    return max(abs(X[IX[k]]) for k in ["phi1", "chi0", "A00", "Az0", "S000", "Szz0"])


# ----------------------------------------------------------------------------------
# Gate-H
# ----------------------------------------------------------------------------------

REF_BG = [
    (1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
    (0.1, 0.3, 1.0, 0.2, 0.15, -0.05, 0.4),
    (3.0, -0.7, 0.5, -0.3, -0.2, 0.1, -0.6),
    (0.01, 2.0, 0.0, 0.0, 0.3, 0.2, 0.0),
]

_HT_CACHE = {}


def hess_tensors(bg):
    key = tuple(np.round(bg, 12))
    if key not in _HT_CACHE:
        _HT_CACHE[key] = RH.tensors(bg)
        if len(_HT_CACHE) > 4096:
            _HT_CACHE.clear()
    return _HT_CACHE[key]


def classify_hessian(cops, bg, tol_rel=1e-10):
    H, G, Mm, Cx = hess_tensors(bg)
    Hc = np.einsum('i,iab->ab', cops, H)
    Gc = np.einsum('i,iab->ab', cops, G)
    Mc = np.einsum('i,iab->ab', cops, Mm)
    Cc = np.einsum('i,iab->ab', cops, Cx)
    Hc = 0.5 * (Hc + Hc.T)
    if not np.all(np.isfinite(Hc)):
        return dict(status="NONFINITE", n_neg=-1, n_zero=-1)
    w, V = np.linalg.eigh(Hc)
    sc = max(float(np.abs(Hc).max()), 1e-300)
    tol = tol_rel * sc
    n_neg = int(np.sum(w < -tol))
    n_zero = int(np.sum(np.abs(w) <= tol))
    n_pos = int(np.sum(w > tol))
    info = dict(n_neg=n_neg, n_zero=n_zero, n_pos=n_pos,
                eig_min=float(w.min()), eig_max=float(w.max()), scale=sc)
    if n_neg > 0:
        info["status"] = "nondegenerate-ghost"
        return info
    if n_zero == 0:
        info["status"] = "nondegenerate-healthy"
        return info
    # degenerate: does each null direction carry a genuine constraint?
    null = V[:, np.abs(w) <= tol]
    gauge_like = 0
    constrained = 0
    qs = max(float(np.abs(Gc).max()), float(np.abs(Mc).max()), float(np.abs(Cc).max()), 1e-300)
    for k in range(null.shape[1]):
        n = null[:, k]
        r = (abs(n @ Mc @ n) + abs(n @ Gc @ n)
             + float(np.abs(Cc @ n).max()) + float(np.abs(n @ Cc).max()))
        if r > 1e-9 * qs:
            constrained += 1
        else:
            gauge_like += 1
    info["n_constrained_null"] = constrained
    info["n_gauge_or_strongcoupled_null"] = gauge_like
    info["status"] = "degenerate"
    return info


def gate_H_pre(cops):
    """robust-ghost pre-screen: kill only if ghostly at EVERY reference background."""
    stats = []
    for bg in REF_BG:
        st = classify_hessian(cops, bg)
        stats.append(st)
        if st.get("status") == "NONFINITE":
            return False, dict(reason="NONFINITE_HESSIAN", stats=stats)
    if all(s["status"] == "nondegenerate-ghost" for s in stats):
        return False, dict(reason="ROBUST_GHOST", stats=stats)
    return True, dict(stats=stats)


# ----------------------------------------------------------------------------------
# the full gate chain
# ----------------------------------------------------------------------------------

# Sigma grid: g_N = Sigma/8 spans 1e-6 .. 1e8, so y spans ~3e-3 (deep MOND) to ~1e8
# (solar-system).  COARSE grid first for a fast reject, FINE grid only for survivors.
SIGMA_FINE = 8.0 * np.logspace(-6.0, 8.0, 29)
SIGMA_COARSE = 8.0 * np.logspace(-6.0, 8.0, 9)

# system size in units c^2/a0 (the MOND length).  a galaxy: 10 kpc / 4 Gpc ~ 2.5e-6.
L_GAL = 2.5e-6

TOL = dict(newton=1e-9, mond_newt=0.02, mond_slope=0.15, mond_range=1.5,
           slip=1e-6, carrier=1e-8, carrier_effect=1e-3,
           y_newton=1e6, y_deep=0.05)


def initial_guesses(Sigma, Xprev, ratio, rng, n_rand=2):
    gs = []
    if Xprev is not None:
        for f in (np.sqrt(max(ratio, 1e-300)), ratio, 1.0):
            gs.append(Xprev * f)
    X0 = np.zeros(RS.N_UNK)
    X0[IX["Phi1"]] = X0[IX["Psi1"]] = Sigma / 8.0
    gs.append(X0)
    for sc in (np.sqrt(Sigma), Sigma ** (1.0 / 3.0)):
        Xg = X0.copy()
        Xg[IX["phi1"]] = sc
        Xg[IX["chi0"]] = sc
        Xg[IX["A00"]] = 1.0
        gs.append(Xg)
    for _ in range(n_rand):
        gs.append(X0 + rng.normal(scale=max(0.3, np.sqrt(Sigma)), size=RS.N_UNK))
    return gs


def _powerlaw_predict(S2_, X2_, S1_, X1_, Snew):
    """component-wise power-law continuation predictor.

    Different unknowns scale with DIFFERENT powers of Sigma (Phi' ~ Sigma, a MOND scalar
    gradient ~ sqrt(Sigma), a unit-timelike A_0 ~ const), so a uniform rescale of the
    previous solution is a bad predictor at large Sigma.  Fit an exponent per component.
    """
    out = np.zeros_like(X1_)
    lr = np.log(S1_ / S2_)
    ln = np.log(Snew / S1_)
    for k in range(len(X1_)):
        a, b = X2_[k], X1_[k]
        if a == 0.0 or b == 0.0 or a * b < 0:
            out[k] = b
            continue
        pk = np.log(abs(b / a)) / lr
        pk = float(np.clip(pk, -2.0, 2.0))
        out[k] = b * np.exp(pk * ln)
    return out


def _solve_seq(cext, mpar, grid, rng, X_start=None):
    """continuation along `grid`; returns list of (Sigma, X) or None on first failure."""
    out = []
    Xprev, Sprev, Xprev2, Sprev2 = X_start, None, None, None
    for Sg in grid:
        ratio = (Sg / Sprev) if Sprev else 1.0
        gs = []
        if Xprev2 is not None:
            gs.append(_powerlaw_predict(Sprev2, Xprev2, Sprev, Xprev, Sg))
        gs.extend(initial_guesses(Sg, Xprev, ratio, rng))
        got = None
        for X0 in gs:
            X, ok, d = solve_static(cext, mpar, Sg, X0, tol=TOL["newton"])
            if ok and np.all(np.isfinite(X)):
                got = X
                break
        if got is None:
            return None, Sg
        out.append((Sg, got))
        Xprev2, Sprev2 = Xprev, Sprev
        Xprev, Sprev = got, Sg
    return out, None


def _mu_curve(cext, mpar, seq):
    ys, mus = [], []
    for Sg, X in seq:
        ob = observables(X, mpar)
        gd = abs(ob["g_dyn"])
        if not np.isfinite(gd) or gd < 1e-300:
            return None, None
        ys.append(gd)
        mus.append(Sg * NEWTON_G_FACTOR / gd)
    return np.array(ys), np.array(mus)


def _mond_verdict(ys, mus):
    o = np.argsort(ys)
    ys, mus = ys[o], mus[o]
    hi = ys > TOL["y_newton"]
    if not hi.any():
        return "NO_NEWTONIAN_REACH", dict(y_range=[ys[0], ys[-1]])
    if abs(mus[hi][-1] - 1.0) > TOL["mond_newt"]:
        return f"G3_FAIL_mu_inf={mus[hi][-1]:.4g}", dict(y_range=[ys[0], ys[-1]])
    if mus.max() / max(mus.min(), 1e-300) < TOL["mond_range"]:
        return f"MU_CONSTANT_{mus.max()/max(mus.min(),1e-300):.3g}", {}
    lo = ys < TOL["y_deep"]
    if lo.sum() < 2:
        return "NO_DEEP_MOND_REACH", {}
    sl = float(np.polyfit(np.log(ys[lo]), np.log(np.maximum(mus[lo], 1e-300)), 1)[0])
    if abs(sl - 1.0) > TOL["mond_slope"]:
        return f"DEEP_SLOPE={sl:.3f}", dict(deep_slope=sl)
    return "PASS", dict(deep_slope=sl, y_range=[float(ys[0]), float(ys[-1])],
                        mu_range=[float(mus.min()), float(mus.max())])


def run_chain(cvec, rng=None, verbose=False):
    """returns (verdict, info).  verdict = the gate the candidate DIED at, or 'SURVIVOR'."""
    cops = np.asarray(cvec[:N_OPS], dtype=float)
    mpar = np.asarray(cvec[N_OPS:], dtype=float)
    cext = np.concatenate([cops, [1.0]])
    rng = rng if rng is not None else np.random.default_rng(0)
    info = {}

    # ---------------- Gate-H (pre): robust ghost only ----------------
    okH, hinfo = gate_H_pre(cops)
    info["H_pre"] = hinfo.get("reason", "PASS")
    if not okH:
        return "Gate-H", info

    # ---------------- Gate-CARRIER ----------------
    Sig_mid = 8.0
    got = None
    for X0 in initial_guesses(Sig_mid, None, 1.0, rng, n_rand=5):
        X, ok, d = solve_static(cext, mpar, Sig_mid, X0, tol=TOL["newton"])
        if ok:
            got = X
            break
    if got is None:
        info["carrier"] = "NO_SOLUTION"
        return "Gate-CARRIER", info
    if carrier_norm(got) < TOL["carrier"]:
        info["carrier"] = "CARRIER_OFF"
        return "Gate-CARRIER", info
    info["carrier"] = "ON"

    # ---------------- Gate-MOND (coarse then fine) ----------------
    seq, badS = _solve_seq(cext, mpar, SIGMA_COARSE, rng)
    if seq is None:
        info["mond"] = f"NO_SOLUTION_at_Sigma={badS:.3e}"
        return "Gate-MOND", info
    ys, mus = _mu_curve(cext, mpar, seq)
    if ys is None:
        info["mond"] = "DEGENERATE_g_dyn"
        return "Gate-MOND", info
    v, d = _mond_verdict(ys, mus)
    info.update(d)
    if v != "PASS":
        info["mond"] = "COARSE:" + v
        return "Gate-MOND", v == "PASS" and info or info

    seq, badS = _solve_seq(cext, mpar, SIGMA_FINE, rng)
    if seq is None:
        info["mond"] = f"NO_SOLUTION_fine_at_Sigma={badS:.3e}"
        return "Gate-MOND", info
    ys, mus = _mu_curve(cext, mpar, seq)
    if ys is None:
        info["mond"] = "DEGENERATE_g_dyn"
        return "Gate-MOND", info
    v, d = _mond_verdict(ys, mus)
    info.update(d)
    if v != "PASS":
        info["mond"] = v
        return "Gate-MOND", info
    info["mond"] = "PASS"

    # ---------------- Gate-SLIP ----------------
    # Two physically DIFFERENT ways a candidate can fail G2, tested separately:
    #
    # (a) FRAME slip.  Phi~' vs Psi~' in the metric matter and light actually couple to.
    #     This is O(1) and unambiguous.  A conformal-only coupling always fails it
    #     (Phi~ = Phi_E + c phi, Psi~ = Psi_E - c phi, so the lensing sum is UNCHANGED
    #     while dynamics is MOND-enhanced: "conformal scalars do not lens").  Bekenstein's
    #     phi-dependent disformal term is the known cure.  KILLS.
    #
    # (b) TRACELESS-STRESS slip, Part-I's Sigma_P.  Turning Sigma_P into an observable
    #     slip needs the carrier's own gravitating (phantom) density: the local equations
    #     are 2 (Phi-Psi)'' = -Sigma_P and 4 Psi'' = -rho_carrier, so the slip is
    #     2 Sigma_P / rho_carrier.  That ratio is O(1) precisely when the MOND enhancement
    #     is carried by the EINSTEIN-FRAME METRIC (the constraint / QUMOND class Part I
    #     covers).  When the enhancement is carried by the matter-frame map instead (the
    #     TeVeS fifth-force class) the carrier's energy density is ~a0^2/G ~ rho_Lambda
    #     and the slip is negligible.  So the Sigma_P cancellation test is applied as a
    #     KILL only for metric-carried MOND, and REPORTED otherwise.  Never assumed.
    worst_frame, worst_rel, parts_max, worst_metric_frac = 0.0, 0.0, 0.0, 0.0
    for Sg, X in seq:
        Mv = np.asarray(_rt()["Mfun"](*X), dtype=float).reshape(N_OPS + 1, RS.N_COL)
        parts = cext * Mv[:, RS.SIGP_COL]
        sc = float(np.abs(parts).max())
        parts_max = max(parts_max, sc)
        sigp = float(parts.sum())
        if sc > 1e-280:
            worst_rel = max(worst_rel, abs(sigp) / sc)
        ob = observables(X, mpar)
        gd = abs(ob["g_dyn"])
        if gd < 1e-300 or not np.isfinite(gd):
            info["slip"] = "DEGENERATE_g_dyn"
            return "Gate-SLIP", info
        worst_frame = max(worst_frame, abs(ob["Phit1"] - ob["Psit1"]) / gd)
        gN = Sg * NEWTON_G_FACTOR
        enh = abs(ob["g_dyn"]) - gN
        if abs(enh) > 1e-3 * gN:
            worst_metric_frac = max(worst_metric_frac,
                                    abs(X[IX["Phi1"]] - gN) / abs(enh))
    info["sigmaP_cancellation_rel"] = float(worst_rel)
    info["frame_slip_worst"] = float(worst_frame)
    info["sigmaP_parts_max"] = float(parts_max)
    info["metric_carried_frac"] = float(worst_metric_frac)
    if worst_frame > TOL["slip"]:
        info["slip"] = f"FRAME_SLIP={worst_frame:.3e} (lensing != dynamics)"
        return "Gate-SLIP", info
    if worst_metric_frac > 0.1 and worst_rel > TOL["slip"]:
        info["slip"] = (f"SIGMA_P_NONZERO={worst_rel:.3e} "
                        f"(metric-carried MOND, frac={worst_metric_frac:.2f})")
        return "Gate-SLIP", info
    info["slip"] = "PASS"
    info["slip_note"] = ("Sigma_P cancels structurally" if worst_rel < 1e-6 else
                         "frame-carried MOND: Sigma_P nonzero but does not gravitate at "
                         "MOND strength (reported, not assumed)")

    # ---------------- Gate-H2 (candidate's OWN background) ----------------
    bad, degen, gauge_sc = 0, 0, 0
    for Sg, X in seq:
        bg = (X[IX["phi1"]], X[IX["chi0"]], X[IX["A00"]], X[IX["Az0"]],
              X[IX["S000"]], X[IX["S000"]] / 6.0 - X[IX["Szz0"]] / 2.0, X[IX["lam0"]])
        st = classify_hessian(cops, bg)
        if st["status"] in ("nondegenerate-ghost", "NONFINITE"):
            bad += 1
        elif st["status"] == "degenerate":
            degen += 1
            gauge_sc = max(gauge_sc, st.get("n_gauge_or_strongcoupled_null", 0))
    info["H2_ghost_points"] = bad
    info["H2_degenerate_points"] = degen
    info["H2_gauge_or_strongcoupled_nulls"] = gauge_sc
    if bad:
        info["H2"] = "GHOST_AT_OWN_BACKGROUND"
        return "Gate-H2", info
    info["H2"] = "PASS"

    # ---------------- Gate-PPN ----------------
    # A boost-INVARIANT carrier vacuum PROVES alpha_1 = alpha_2 = 0: with no VEV that
    # singles out a time direction there is no preferred frame for the system velocity w
    # to be measured against.  A vacuum carrying A_0 != 0 or S_00 != 0 (a unit-timelike
    # aether, a timelike tensor VEV) is exactly the structure that produced
    # alpha_2 = 1/lam_s + 2/(K_B lam_s^2) in AeST.  The exact 1PN value is a stage-2
    # object and is NOT fabricated here: such candidates are reported, not scored.
    Xz = np.zeros(RS.N_UNK)
    Rz, _, scz, _ = residual_and_jac(cext, mpar, 0.0, Xz)
    if float(np.max(np.abs(Rz / scz))) < 1e-9:
        info["ppn"] = "PASS(trivial boost-invariant carrier vacuum => alpha_1 = alpha_2 = 0)"
        info["vacuum_boost_break"] = 0.0
        return "SURVIVOR", info
    Xv = None
    for X0 in initial_guesses(1e-10, None, 1.0, rng, n_rand=4):
        Xt, okv, dv = solve_static(cext, mpar, 0.0, X0, tol=TOL["newton"])
        if okv and Xt is not None and np.all(np.isfinite(Xt)):
            Xv = Xt
            break
    if Xv is None:
        info["ppn"] = "NO_VACUUM_SOLUTION"
        return "Gate-PPN", info
    boost_break = max(abs(Xv[IX["A00"]]), abs(Xv[IX["S000"]]))
    info["vacuum_boost_break"] = float(boost_break)
    if boost_break > 1e-8:
        info["ppn"] = "PREFERRED_FRAME_VACUUM(alpha_1,alpha_2 NOT established -- stage-2 1PN)"
        return "Gate-PPN", info
    info["ppn"] = "PASS(boost-invariant carrier vacuum => alpha_1 = alpha_2 = 0)"
    return "SURVIVOR", info
