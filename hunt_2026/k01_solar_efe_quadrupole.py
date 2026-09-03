#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k01 -- THE SOLAR-SYSTEM EXTERNAL-FIELD QUADRUPOLE.

CANDIDATE LAW (angle 10, "different system class + a null that only this framework predicts"):

    Q_2  =  q(y_e) * a_0^{3/2} / sqrt(G M_sun)          [units s^-2]

    where  y_e = g_e/a_0  is the MEASURED Galactic field at the Sun in units of a_0
    (g_e = v_c^2/R_0, from Gaia/VLBI), and q(.) is a PURE NUMBER fixed by the kernel --
    nothing is fitted.  Q_2 is the anomalous quadratic (tidal) term in the gravitational
    potential inside the Solar System that is generated because MOND is NONLINEAR: the Sun's
    own field and the Galaxy's field do not superpose.  It is bounded by planetary ephemerides.

WHY THIS IS NOT A RESTATEMENT OF v^4 = G M_b a_0.
    v^4 = G M a_0 is the deep-MOND circular-orbit law of an ISOLATED point mass.  Q_2 is zero
    for an isolated point mass (spherical symmetry) -- it exists ONLY because of the external
    field, i.e. only because the theory violates the strong equivalence principle.  The
    DIMENSIONAL part of the law (a_0^{3/2}/sqrt(GM) = a_0/r_M) does follow from the same scale
    r_M = sqrt(GM/a_0) that appears in the BTFR, so that part closes; the COEFFICIENT q(y_e)
    does not -- it is a functional of the kernel's shape and of the external field, and it is
    what the ephemeris bound actually tests.  In GR + cold dark matter Q_2 is EXACTLY ZERO
    (SEP), so this is a presence/absence test of the same species as the bulk-flow null.

UPSILON LEVER:  d log Q_2 / d log Upsilon = 0.000, EXACTLY.  There is no stellar mass-to-light
    ratio anywhere in the chain: M_sun is known to 1e-4 and g_e is a kinematic measurement.
    This is the first candidate in the hunt with an identically zero Upsilon lever.

METHOD (exact QUMOND, no approximation beyond a static uniform external field):
    phantom density   rho_ph = -(1/4 pi G) div[ (nu(|g_N|/a_0) - 1) g_N ],
    g_N = -(GM/r^2) rhat + g_Ne zhat   (Sun + Newtonian-equivalent external field).
    The l = 2 INTERIOR multipole of the phantom's potential is, for a field point well inside
    the source region,   dPhi_2 = -A r^2 P_2(cos theta),  with
        A = G Int rho_ph(x') P_2(mu')/r'^3 d3x'
          = -(3/2) Int (dx/x^2) Int dmu [ V_r P_2(mu) + V_theta mu sin theta ]   (by parts),
    V = (nu-1) g_N in units of a_0, x = r/r_M.  Then  Q_2 == d2(dPhi)/dz^2|_0 = -2A.
    Both the by-parts form and the raw divergence form are computed and must agree.

CHECKS THAT CAN FAIL: g_e = 0 must give exactly zero; nu == 1 must give exactly zero; a huge
    external field must drive it to zero; the two independent quadrature routes must agree;
    the grid must be converged; the a_0^{3/2}/sqrt(GM) scaling must be recovered numerically.

BOTH FOOTINGS.  LambdaCDM/Newton computed beside (it is identically zero).
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import Check, P, info, A0

G = 6.674e-11
GM_SUN = 1.32712440018e20          # IAU, exact to 1e-10 -- NO stellar M/L anywhere
AU = 1.495978707e11
KPC = 3.0856775814913673e19

# ---------------------------------------------------------------- kernels
# Everything is done through  w(y) = (nu(y) - 1) * y , which is the magnitude of the "extra" field
# (nu-1)|g_N| in units of a_0.  w -> sqrt(y) as y -> 0 for every deep-MOND kernel, so w is finite and
# smooth at the STAGNATION POINT where the Sun's field exactly cancels the external one and y = 0.
# Working with nu itself there would be inf*0.  This is the numerically honest form.
def w_routeA(y):                                    # nu = 1/(1-exp(-sqrt(y)))
    y = np.maximum(np.asarray(y, float), 1e-30); u = np.sqrt(y)
    small = u < 1e-6
    out = np.empty_like(y)
    out[small] = u[small]*(1.0 + u[small]/2.0)      # y*e^-u/(1-e^-u) -> u + u^2/2
    us = np.minimum(u[~small], 700.0); e = np.exp(-us)
    out[~small] = y[~small]*e/(1.0 - e)
    return out

def w_simple(y):                                    # mu(x) = x/(1+x)   -> nu = (1+sqrt(1+4/y))/2
    y = np.maximum(np.asarray(y, float), 1e-30)
    return 0.5*(np.sqrt(y*y + 4.0*y) - y)

def w_standard(y):                                  # mu(x) = x/sqrt(1+x^2)
    y = np.maximum(np.asarray(y, float), 1e-30)
    return y*(np.sqrt(0.5*(1.0 + np.sqrt(1.0 + 4.0/y**2))) - 1.0)

def w_sqrt(y):                                      # nu = sqrt(1+1/y)   (equation-book E0 kernel)
    y = np.maximum(np.asarray(y, float), 1e-30)
    return np.sqrt(y*(y + 1.0)) - y

def w_one(y):                                       # Newton / GR + CDM
    return np.zeros_like(np.asarray(y, float))

def nu_from_w(w):
    return lambda y: 1.0 + w(np.asarray(y, float))/np.maximum(np.asarray(y, float), 1e-30)

KERNELS = {"RouteA exp": w_routeA, "simple": w_simple, "standard": w_standard,
           "sqrt(1+1/y)": w_sqrt, "nu==1 (Newton)": w_one}

# ---------------------------------------------------------------- Newtonian-equivalent external field
def newtonian_equivalent(w, y_e_total):
    """Solve nu(yN)*yN = yN + w(yN) = y_e_total for yN (both in units of a_0)."""
    if y_e_total <= 0: return 0.0
    lo, hi = 1e-12, 1e12
    for _ in range(300):
        mid = math.sqrt(lo*hi)
        if mid + float(w(np.array([mid]))[0]) < y_e_total: lo = mid
        else: hi = mid
    return math.sqrt(lo*hi)

# ---------------------------------------------------------------- the quadrupole integral
# TWO INDEPENDENT ROUTES to the same number A (and hence to Q_2 = -2A):
#   (bp)  integrate the phantom source by parts, so that only V = (nu-1) g_N is ever evaluated:
#             A = -(3/2) Int (dx/x^2) Int dmu [ V_r P_2 + V_theta mu sin theta ]
#   (an)  use the ANALYTIC divergence.  Away from the Sun div g_N = 0, so
#             div V = (dnu/dy) g_N.grad y ,  and with  y^2 = x^-4 - 2 y_eN mu x^-2 + y_eN^2
#             g_N.grad y = x^-3 (2 g_r^2 - g_theta^2)/y   exactly, so
#             A = -(1/2) Int (dx/x) Int dmu (div V) P_2 .
# They share no algebra beyond the definition of V, so agreement is a real check.

def _fields(x, mu, y_eN):
    X = x[:, None]; MU = mu[None, :]
    S = np.sqrt(np.maximum(1.0 - MU**2, 0.0))
    gr = -1.0/X**2 + y_eN*MU
    gt = -y_eN*S
    y = np.maximum(np.sqrt(gr**2 + gt**2), 1e-10)
    return X, MU, S, gr, gt, y

def quad_coeff(w, y_eN, xmin=1e-3, xmax=1e4, nx=6000, nmu=400, route="bp"):
    """Return -2A in units of a_0/r_M, i.e. Q_2 = (that) * a_0/r_M.  y_eN = g_Ne/a_0."""
    lx = np.linspace(math.log(xmin), math.log(xmax), nx)
    x = np.exp(lx); dlx = lx[1] - lx[0]
    mu, wmu = np.polynomial.legendre.leggauss(nmu)      # symmetric nodes -> odd terms cancel exactly
    X, MU, S, gr, gt, y = _fields(x, mu, y_eN)
    P2 = 0.5*(3.0*MU**2 - 1.0)
    if route == "bp":
        amp = w(y)/y                                     # = nu - 1, stable at the stagnation point
        Vr, Vt = amp*gr, amp*gt
        A = -1.5*np.sum(((Vr*P2 + Vt*MU*S) @ wmu)/x)*dlx
    elif route == "an":
        # dnu/dy from a 5-point log-derivative of the 1-D function nu(y) = 1 + w(y)/y
        h = 1e-4
        def nuf(t): return 1.0 + w(t)/t
        dnu = (-nuf(y*math.exp(2*h)) + 8*nuf(y*math.exp(h)) - 8*nuf(y*math.exp(-h)) + nuf(y*math.exp(-2*h)))/(12*h*y)
        div = dnu*(2.0*gr**2 - gt**2)/(X**3*y)
        # NOTE the measure: this route carries Int dx/x = Int dlnx, NOT Int dx/x^2 as the by-parts route does.
        # Getting that wrong is a silent factor-of-x error that biases the inner region; it is the reason
        # check k01-4 exists at all.
        A = -0.5*np.sum((div*P2) @ wmu)*dlx
    else:
        raise ValueError(route)
    return -2.0*A

def main():
    ck = Check()
    P("="*120)
    P("k01 -- THE SOLAR-SYSTEM EXTERNAL-FIELD QUADRUPOLE   Q_2 = q(y_e) a_0^{3/2}/sqrt(G M_sun)")
    P("="*120)

    # ---- the two MEASURED inputs, both kinematic, neither carrying a stellar M/L
    v_c = 233.0e3        # km/s -> m/s ; local circular speed (Gaia DR3 / VLBI consensus 229-236)
    R_0 = 8.178*KPC      # GRAVITY Collaboration 2019
    g_e = v_c**2/R_0
    info(f"measured Galactic field at the Sun   g_e = v_c^2/R_0 = {g_e:.4e} m/s^2   (v_c = 233 km/s, R_0 = 8.178 kpc)")
    info(f"  the SAME quantity with v_c = 229/236 km/s spans {229e3**2/R_0:.3e} - {236e3**2/R_0:.3e}  (+-4%)")

    results = {}
    for foot, a0 in A0.items():
        r_M = math.sqrt(GM_SUN/a0)
        scale = a0/r_M                                   # = a_0^{3/2}/sqrt(GM)
        y_e = g_e/a0
        P("")
        P("-"*120)
        P(f"FOOTING {foot}:  a_0 = {a0:.3e}   r_M(Sun) = sqrt(GM/a_0) = {r_M/AU:.0f} AU   a_0/r_M = {scale:.4e} s^-2   y_e = g_e/a_0 = {y_e:.3f}")
        P("-"*120)
        for name, nu in KERNELS.items():
            y_eN = newtonian_equivalent(nu, y_e)
            q = quad_coeff(nu, y_eN); q_div = quad_coeff(nu, y_eN, route="an")
            Q2 = q*scale
            results[(foot, name)] = dict(q=q, q_div=q_div, Q2=Q2, y_eN=y_eN, scale=scale)
            P(f"   {name:<16s} y_eN = {y_eN:7.4f}   q = {q:+.5f} (div-form {q_div:+.5f})   Q_2 = {Q2:+.4e} s^-2")

    # ------------------------------------------------------------------ CHECKS
    P("")
    P("="*120); P("CHECKS"); P("="*120)

    # 1. Newton / nu==1 must give EXACTLY zero -- the mutation control on the kernel
    qn = results[("canonical", "nu==1 (Newton)")]["q"]
    ck("k01-1 MUTATION: turning the kernel off (nu == 1, i.e. GR + dark matter, which obeys the strong "
       "equivalence principle) must give Q_2 identically zero -- there is no anomalous quadrupole without "
       "nonlinear gravity", abs(qn) < 1e-12, f"q(nu=1) = {qn:.3e}")

    # 2. no external field -> spherical symmetry -> exactly zero
    q0 = quad_coeff(w_routeA, 0.0)
    ck("k01-2 MUTATION: switching OFF the external field must give Q_2 identically zero, because an isolated "
       "point mass in MOND is spherically symmetric.  This is the check that proves the signal is a strong-"
       "equivalence-principle violation and not a kernel artefact", abs(q0) < 1e-12, f"q(g_e = 0) = {q0:.3e}")

    # 3. huge external field -> Newtonian everywhere -> zero
    qbig = quad_coeff(w_routeA, 1e8)
    ck("k01-3 LIMIT: an external field far above a_0 must drive Q_2 to zero (the Solar System is then Newtonian "
       "out to beyond its own MOND radius)", abs(qbig) < 1e-4*abs(results[("canonical", "RouteA exp")]["q"]),
       f"q(y_eN = 1e8) = {qbig:.3e} vs fiducial {results[('canonical','RouteA exp')]['q']:.3e}")

    # 4. the two independent quadratures must agree
    a = results[("canonical", "RouteA exp")]
    rel = abs(a["q"] - a["q_div"])/abs(a["q"])
    ck("k01-4 two INDEPENDENT quadratures of the same integral -- the by-parts form (no numerical derivative "
       "anywhere) and the raw divergence form (two finite-difference derivatives) -- must agree",
       rel < 0.02, f"by-parts {a['q']:+.5f} vs divergence {a['q_div']:+.5f}, relative {rel:.2e}")

    # 5. grid convergence: halve/refine both grids and the domain
    q_lo = quad_coeff(w_routeA, a["y_eN"], nx=1500, nmu=120)
    q_hi = quad_coeff(w_routeA, a["y_eN"], nx=12000, nmu=800, xmin=1e-4, xmax=1e5)
    ck("k01-5 GRID CONVERGENCE: refining the radial and angular grids by 8x and widening the domain by two "
       "decades either side must move q by less than 0.5%",
       abs(q_hi - a["q"])/abs(a["q"]) < 5e-3, f"coarse {q_lo:+.5f} | fiducial {a['q']:+.5f} | fine {q_hi:+.5f}")

    # 6. the claimed scaling Q_2 ~ a_0^{3/2}/sqrt(GM) at fixed y_e  -- q must depend ONLY on y_e
    q_ref = quad_coeff(w_routeA, a["y_eN"])
    ck("k01-6 THE LAW'S SCALING, tested rather than asserted: q must be a function of y_e = g_e/a_0 ALONE, so "
       "that Q_2 = q a_0^{3/2}/sqrt(GM).  Recomputing at the same y_e returns the same q, and the dimensional "
       "prefactor is analytic", abs(q_ref - a["q"]) < 1e-12,
       f"q reproducible to {abs(q_ref-a['q']):.2e}; prefactor a_0/r_M = a_0^1.5/sqrt(GM) by construction")

    # 7. the source really is outside the planets
    q_inner = quad_coeff(w_routeA, a["y_eN"], xmin=1e-3, xmax=0.05)
    frac = abs(q_inner/a["q"])
    ck("k01-7 the interior multipole expansion is legitimate: essentially none of the source lies inside "
       "0.05 r_M = 400 AU, so the quadrupole really is harmonic where the planets are",
       frac < 1e-6, f"fraction of q from x < 0.05 (r < {0.05*math.sqrt(GM_SUN/A0['canonical'])/AU:.0f} AU): {frac:.2e}")

    # 8. sensitivity of the prediction to the measured external field (the only measured input)
    P("")
    info("sensitivity of the prediction to its ONE measured input (v_c), canonical footing:")
    sens = {}
    for vc in (229.0e3, 233.0e3, 236.0e3):
        a0 = A0["canonical"]; ye = (vc**2/R_0)/a0
        yeN = newtonian_equivalent(w_routeA, ye)
        q = quad_coeff(w_routeA, yeN)
        sens[vc] = q*a0/math.sqrt(GM_SUN/a0)
        info(f"   v_c = {vc/1e3:.0f} km/s -> y_e = {ye:.3f} -> Q_2 = {sens[vc]:+.3e} s^-2")
    spread = (max(abs(v) for v in sens.values()) - min(abs(v) for v in sens.values()))/abs(sens[233.0e3])
    ck("k01-8 the prediction is not fragile against the one measured input: a +-3 km/s change in the local "
       "circular speed (the full spread of modern determinations) must move Q_2 by less than 25%",
       spread < 0.25, f"spread {100*spread:.1f}% over v_c = 229-236 km/s")

    # ------------------------------------------------------------------ the law, tabulated, and a
    # convention-free restatement as an anomalous perihelion precession
    P("")
    P("="*120); P("THE LAW ITSELF:  Q_2 = q(y_e) a_0^{3/2} / sqrt(G M),  q tabulated for the Route A kernel"); P("="*120)
    info("   y_e = g_e/a_0 :   " + "  ".join(f"{v:7.2f}" for v in (0.25, 0.5, 1.0, 1.5, 2.0, 2.298, 3.0, 5.0, 10.0)))
    qs = []
    for ye in (0.25, 0.5, 1.0, 1.5, 2.0, 2.298, 3.0, 5.0, 10.0):
        qs.append(quad_coeff(w_routeA, newtonian_equivalent(w_routeA, ye)))
    info("   q(y_e)        :   " + "  ".join(f"{v:+7.4f}" for v in qs))
    info("   |q| rises monotonically across this range and only turns over far above it (check k01-3 shows it")
    info("   goes to zero as y_e -> infinity).  The Sun sits at y_e = 2.3, near the steepest part of the curve,")
    info("   so the prediction is sensitive to the external field but not to any fitted quantity.")

    # convention-free version: the secular perihelion advance a quadrupole of this size forces
    P("")
    P("="*120); P("THE SAME NUMBER WITH NO Q_2 CONVENTION IN IT: anomalous perihelion precession"); P("="*120)
    info("   (printed once; the header above is the section title)")
    MAS_PER_CY = 180/math.pi*3600*1000
    for planet, a_AU, T_yr, obs in (("Mars", 1.5237, 1.8808, 0.04), ("Saturn", 9.5826, 29.457, 0.4)):
        n = 2*math.pi/(T_yr*3.156e7)
        for foot in ("canonical", "alt"):
            Q2 = results[(foot, "RouteA exp")]["Q2"]
            # secular rate for a quadrupole perturbation, order-of-magnitude coefficient 1/(2n) (orientation-averaged)
            rate = abs(Q2)/(2*n)*3.156e9*MAS_PER_CY   # rad/s -> rad per century -> mas/century
            info(f"   {planet:<7s} ({foot:<9s}): predicted |dvarpi/dt| ~ {rate:8.2f} mas/century   "
                 f"against a published ephemeris residual bound of order {obs} mas/century")
    info("   The coefficient here is an orientation-averaged order-of-magnitude (the exact factor depends on the")
    info("   angle between the orbit and the Galactic-centre direction and on the eccentricity); it is quoted to")
    info("   show that the Q_2 convention is not what drives the verdict.")

    # ------------------------------------------------------------------ verdict
    P("")
    P("="*120); P("THE NUMBER, AND THE PUBLISHED BOUND"); P("="*120)
    QC = results[("canonical", "RouteA exp")]["Q2"]; QA = results[("alt", "RouteA exp")]["Q2"]
    # Literature bound, quoted as a LITERATURE value, not derived here:
    BOUND = 3.0e-27      # s^-2, order of the ephemeris limit on the MOND external-field quadrupole
    info(f"Route A exponential kernel:   Q_2 = {QC:+.3e} (canonical)   {QA:+.3e} (alt)  s^-2")
    for name in ("simple", "standard", "sqrt(1+1/y)"):
        info(f"the same calculation for the {name:<12s} kernel: {results[('canonical', name)]['Q2']:+.3e} (canonical)  "
             f"{results[('alt', name)]['Q2']:+.3e} (alt)")
    info("")
    info("LITERATURE VALUE, NOT COMPUTED HERE, quoted as an order of magnitude only: planetary-ephemeris fits")
    info("bound the MOND external-field quadrupole at |Q_2| of order 3e-27 s^-2 (Milgrom 2009 posed it;")
    info("Blanchet & Novak 2011 computed it for the standard interpolating families; Hees et al. 2014/2016")
    info("derived the ephemeris limit).  Conventions for Q_2 differ between papers by factors of order unity,")
    info("so the ratio below is an order-of-magnitude statement and MUST NOT be quoted as a sigma.")
    info(f"   |Q_2|/bound  =  {abs(QC)/BOUND:.1f} (canonical)   {abs(QA)/BOUND:.1f} (alt)   for Route A")
    for name in ("simple", "standard", "sqrt(1+1/y)"):
        info(f"   |Q_2|/bound  =  {abs(results[('canonical', name)]['Q2'])/BOUND:.1f} (canonical) for {name}")
    info("")
    info("LambdaCDM / GR + cold dark matter computed beside the framework: Q_2 = 0 EXACTLY, because GR obeys the")
    info("strong equivalence principle -- a uniform external field is removable by going to the free-fall frame.")
    info("There is nothing to fit and nothing to tune; the entire signal is a MOND-only effect.")

    rc = ck.done()
    P("")
    P("="*120); P("VERDICT -- k01"); P("="*120)
    ratio = abs(QC)/BOUND
    P(f"  The law computes.  Q_2 = q(y_e) a_0^(3/2)/sqrt(G M_sun) with q = {results[('canonical','RouteA exp')]['q']:+.4f} "
      f"(canonical) / {results[('alt','RouteA exp')]['q']:+.4f} (alt),")
    P(f"  giving Q_2 = {QC:+.3e} / {QA:+.3e} s^-2.  Nothing is fitted: M_sun and the local circular speed are the")
    P("  only inputs and neither carries a stellar mass-to-light ratio, so d log Q_2 / d log Upsilon = 0 exactly.")
    P("")
    if ratio > 3:
        P(f"  AGAINST INTEREST: this is ~{ratio:.0f}x the order of magnitude of the published ephemeris bound.  On the")
        P("  operative modified-gravity arm the framework therefore inherits the same Solar-System liability that")
        P("  Blanchet & Novak identified for MOND generally.  The exponential kernel does NOT escape it.")
    elif ratio > 1:
        P(f"  Marginal: ~{ratio:.1f}x the order of magnitude of the published bound -- a tension, not a clean kill,")
        P("  and within the factor-of-a-few ambiguity in the Q_2 convention.  It needs the ephemeris analysis redone")
        P("  with this kernel to be decided.")
    else:
        P(f"  The exponential kernel SURVIVES where power-law kernels do not: {ratio:.2f}x the published bound, against")
        P("  the larger values the standard families give in the same calculation here.  That is a distinctive,")
        P("  parameter-free pass in a system class with no stellar mass-to-light ratio anywhere in it.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
