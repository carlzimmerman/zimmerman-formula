"""Gate objective for the coefficient-history search (hermes autoflow).

METHOD (the one that works for hard equations generally): parameterise the unknown object, define a residual that vanishes EXACTLY when
the target property holds, drive the residual down with a global optimiser, then certify the discovered object -- the numerics locate the
solution, the certificate establishes it. Here the unknown object is the coefficient history of the cuscuton-clock MOND action and the
residual is the total gate violation.

THE TARGET (set by fable_independent_2026/L192, gradient-driven criticality). The clock-scalar sound speed at zero field gradient is
c_s^2(0) = (1 - s0) m_rel/(2 - m_rel); it rises monotonically with the background gradient invariant Y and crosses zero at a unique Y*,
which is a two-sided attractor whose state is EXACT pressureless dust. Criticality therefore operates wherever the clock runs faster than
proper time, s0 > 1. A history that has s0 > 1 at every epoch of interest is driven to exact dust by its own MOND sector, with no tuning
of the logarithm margin. So the search is for such a history that is also a consistent dust-like dark sector of the right amount.

CLOSURE ALGEBRA (explicit; from the frozen action, with gamma -> 0):
  m  = U - 2 d q^2          the logarithm margin, must be positive         m_rel = m/U, must lie in (0, 2) for a healthy kinetic term
  P_X = U d/m,  P_XX = 2 U d^2/m^2,  B = 2 P_X + 4 X P_XX = (2Ud/m)(2U - m)/m
  rho_clock = 2 q^2 P_X + V = 2 q^2 U d/m + U            (P vanishes on its own reference point at gamma = 0)
  W(Y) = U + 2 d l (sqrt(1 + Y/l) - 1),  W_Y = d (1 + Y/l)^(-1/2),  m(Y) = m + 2 d Y,  X = q^2 - Y
  c_s^2(Y) = [2 P_X(Y) (1 - D) - 2 s0 W_Y(Y)]/[B(Y)(1 - D)],  D = 2 q^2 W_Y(Y)/W(Y)

PARAMETERISATION: each of U, d, l, q, s0 is a power law in the scale factor, X(a) = X0 a^p, ten parameters in all. Extend the family by
editing PARAM_NAMES and history(); do NOT tune a gate's threshold to make a candidate pass -- report the failure instead.

Every gate returns a NUMBER, never a boolean, so the optimiser can see the gradient and the reader can see how far off a candidate is."""
import numpy as np
PARAM_NAMES = ["logU0", "pU", "logd0", "pd", "logl0", "pl", "q0", "pq", "s0_0", "ps0"]
BOUNDS = [(-4, 4), (-6, 6), (-6, 2), (-6, 6), (-8, 2), (-6, 6), (0.05, 3.0), (-3, 3), (1.0, 4.0), (-3, 3)]
AGRID = np.geomspace(0.10, 1.0, 10)                     # a = 0.10 (z = 9) to today
OMEGA_C = 0.26                                           # required dark-sector share of the critical density today
def history(theta, a):
    lU, pU, ld, pd, ll, pl, q0, pq, s00, ps0 = theta
    return (10**lU*a**pU, 10**ld*a**pd, 10**ll*a**pl, q0*a**pq, s00*a**ps0)
def cs2(U, d, l, q, s0, Y):
    X = q*q - Y; m = U - 2*d*X
    if m <= 0 or 1 + Y/l <= 0: return np.nan
    PX = U*d/m; B = (2*U*d/m)*(2*U - m)/m
    W = U + 2*d*l*(np.sqrt(1 + Y/l) - 1); WY = d/np.sqrt(1 + Y/l); D = 2*q*q*WY/W
    if abs(B*(1 - D)) < 1e-300: return np.nan
    return (2*PX*(1 - D) - 2*s0*WY)/(B*(1 - D))
def critical_Y(U, d, l, q, s0):
    """The unique gradient at which the sound speed vanishes (L192); nan if the sector is already stable at Y = 0."""
    if cs2(U, d, l, q, s0, 0.0) >= 0: return np.nan
    lo, hi = 1e-14*l, None
    for Y in np.geomspace(1e-12*l, 0.5*(q*q + U/(2*d)), 300):
        v = cs2(U, d, l, q, s0, Y)
        if np.isfinite(v) and v > 0: hi = Y; break
    if hi is None: return np.inf
    for _ in range(80):
        mid = np.sqrt(lo*hi)
        if cs2(U, d, l, q, s0, mid) < 0: lo = mid
        else: hi = mid
    return np.sqrt(lo*hi)
def gates(theta):
    """Return (loss, breakdown). Every entry is a non-negative violation; zero means the gate is met exactly."""
    g = {k: 0.0 for k in ("domain", "kinetic", "criticality", "reachable", "dust", "amount", "monotone")}
    rho = []
    for a in AGRID:
        U, d, l, q, s0 = history(theta, a)
        if not all(np.isfinite([U, d, l, q, s0])) or min(U, d, l, q) <= 0: return 1e6, g
        m = U - 2*d*q*q
        g["domain"] += max(-m/U, 0.0) + max(1e-6 - m/U, 0.0)                     # margin must be positive
        mrel = m/U
        g["kinetic"] += max(mrel - 2.0, 0.0)                                       # 2U - m > 0, no ghost
        g["criticality"] += max(1.0 - s0, 0.0)                                     # s0 > 1 so the attractor exists (L192)
        Ys = critical_Y(U, d, l, q, s0)
        g["reachable"] += 0.0 if (np.isfinite(Ys) and 0 < Ys < 0.1*l) else 1.0     # the marginal gradient must be small and finite
        rho.append(2*q*q*U*d/m + U)
    rho = np.asarray(rho)
    if not np.all(np.isfinite(rho)) or np.any(rho <= 0): return 1e6, g
    sl = np.polyfit(np.log(AGRID), np.log(rho), 1)[0]
    g["dust"] = abs(sl + 3.0)                                                      # the sector must redshift as dust
    g["amount"] = abs(np.log(rho[-1]/(3*OMEGA_C)))                                 # right amount today (M^2 = 1, H0 = 1 units)
    g["monotone"] = float(np.any(np.diff(rho) > 0))                                # density must fall with time
    return float(sum(g.values())), g
def describe(theta):
    out = []
    for a in (0.10, 0.30, 1.0):
        U, d, l, q, s0 = history(theta, a); m = U - 2*d*q*q
        out.append(f"a={a:.2f}: m_rel={m/U:+.4f} s0={s0:.3f} c_s2(0)={cs2(U, d, l, q, s0, 0.0):+.3e} Y*/l={critical_Y(U, d, l, q, s0)/l:.4f}")
    return "; ".join(out)
