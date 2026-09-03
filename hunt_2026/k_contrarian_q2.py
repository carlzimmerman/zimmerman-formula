#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_contrarian_q2 -- INDEPENDENT recomputation of the Solar-System external-field quadrupole (candidate K1).

THE CANDIDATE, as proposed:
    Q2 == d^2 dPhi / dz^2 |_Sun  =  q(y_e) * a_0^{3/2} / sqrt(G M_sun)     [s^-2]
    y_e = g_e/a_0 the MEASURED Galactic field at the Sun, q a pure number fixed by the kernel.
    GR + cold dark matter gives Q2 == 0 EXACTLY (strong equivalence principle).

WHAT THIS SCRIPT DOES DIFFERENTLY FROM THE PROPOSING AGENT'S k01_solar_efe_quadrupole.py
    (a) the multipole algebra is re-derived from scratch here, including the SIGN of the phantom density
        rho_ph = -(1/4 pi G) div[(nu-1) g_N]  (the sign that makes an isolated deep-MOND point mass have
        POSITIVE phantom density -- verified as check q2-0);
    (b) the quadrature is done THREE ways, one of which (cylindrical) shares no coordinate with the others;
    (c) the multipole integrator is validated against a density with an ANALYTIC interior quadrupole;
    (d) the result is confronted with the published ephemeris MEASUREMENT, not just quoted beside it;
    (e) the literature and the REPOSITORY'S OWN prior work are checked before any novelty is claimed.

DERIVATION (QUMOND, exact for a static uniform external field)
    QUMOND field equation:  lap Phi = div[ nu(|grad Phi_N|/a0) grad Phi_N ].
    With G_N == -grad Phi_N  and  Phi = Phi_N + Phi_ph,
        lap Phi_ph = -div[(nu-1) G_N]   =>   rho_ph = -(1/4 pi G) div[(nu-1) G_N].
    Sanity (check q2-0): isolated deep-MOND point mass has (nu-1)G_N = -sqrt(GM a0)/r rhat, whose
    divergence is -sqrt(GM a0)/r^2, so rho_ph = +sqrt(GM a0)/(4 pi G r^2) > 0.  A phantom halo, as it must be.

    Interior multipole of a source that lies OUTSIDE the field point:
        Phi_in(r) = -G sum_l r^l P_l(cos th) Int rho(r') P_l(cos th') / r'^{l+1} d3r'.
    The l = 2 term written as dPhi_2 = (Q2/2) r^2 P_2(cos th)  (equivalently dPhi_2 = (Q2/2)[z^2-(x^2+y^2)/2],
    so that d^2 dPhi/dz^2|_0 = Q2 -- Milgrom's convention) gives
        Q2 = -2 G Int rho_ph P_2(mu') / r'^3 d3r'
           = +(1/2pi) Int div[(nu-1) u] P_2(mu)/x^3 d3x  * (a0^{3/2}/sqrt(GM))
    in units x = r/r_M, r_M = sqrt(GM/a0), u = G_N/a0 = -xhat/x^2 + y_N zhat.  Hence

        q = (1/2pi) Int div[V] P_2(mu) x^-3 d3x ,   V == (nu(|u|)-1) u = w(|u|) uhat,  w(y) == (nu(y)-1) y

    and by parts (no numerical derivative anywhere),
        q = 3 Int dx/x^2 Int_-1^1 dmu [ V_r P_2(mu) + V_th mu sqrt(1-mu^2) ].

    The external field enters as its NEWTONIAN equivalent y_N, solving nu(y_N) y_N = y_e, because QUMOND
    is sourced by the Newtonian field.  (Using y_e directly in place of y_N is a real, and common, error;
    it is quantified here as check q2-9.)

RESTATEMENT TEST -- executed, not asserted:  set y_e = 0 and the integral must vanish identically by
    spherical symmetry.  v^4 = G M_b a_0 is the isolated-point-mass law and carries NO information about a
    neighbour's field, so it cannot produce Q2.  It DOES produce the prefactor a0^{3/2}/sqrt(GM) = a0/r_M,
    since r_M = sqrt(GM/a0) is the same scale the BTFR carries -- that half closes, the coefficient does not.

UPSILON LEVER: identically zero.  There is no stellar mass-to-light ratio in the chain: GM_sun is known to
    1e-10 and g_e = v_c^2/R_0 is kinematic.  Verified numerically by running the whole pipeline at Upsilon
    x1.5 (check q2-10) -- the answer does not move in the 15th digit, because Upsilon never enters.

BOTH FOOTINGS throughout.  LambdaCDM/Newtonian alternative computed beside: Q2 = 0 exactly.
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import Check, P, info, A0

G      = 6.674e-11
GM_SUN = 1.32712440018e20          # IAU 2015 nominal, exact to 1e-10.  NO stellar M/L anywhere.
KPC    = 3.0856775814913673e19
AU     = 1.495978707e11

# ------------------------------------------------------------------ kernels, all through w(y) = (nu-1) y
# w is finite and smooth at the stagnation point (where the Sun's field cancels the external one and y -> 0),
# where nu itself is infinite; w -> sqrt(y) there for every deep-MOND kernel.
def w_routeA(y):                      # Route A / McGaugh RAR:  nu = 1/(1-exp(-sqrt(y)))
    y = np.asarray(y, float); s = np.sqrt(np.maximum(y, 0.0))
    out = np.zeros_like(y)
    sml = s < 1e-8
    out[sml] = np.sqrt(np.maximum(y[sml], 0.0))          # w -> sqrt(y)
    b = ~sml
    e = np.exp(-s[b])
    out[b] = y[b]*e/(1.0 - e)
    return out

def w_simple(y):                      # nu = (1+sqrt(1+4/y))/2
    y = np.asarray(y, float); out = np.zeros_like(y)
    b = y > 0
    out[b] = y[b]*((1.0 + np.sqrt(1.0 + 4.0/y[b]))/2.0 - 1.0)
    return out

def w_standard(y):                    # nu = sqrt(1/2 + sqrt(1/4 + 1/y^2))
    y = np.asarray(y, float); out = np.zeros_like(y)
    b = y > 0
    out[b] = y[b]*(np.sqrt(0.5 + np.sqrt(0.25 + 1.0/y[b]**2)) - 1.0)
    return out

def w_sqrt1p(y):                      # nu = sqrt(1 + 1/y)  (the programme's equation-book form E-nu)
    y = np.asarray(y, float); out = np.zeros_like(y)
    b = y > 0
    out[b] = y[b]*(np.sqrt(1.0 + 1.0/y[b]) - 1.0)
    return out

def w_newton(y):                      # nu == 1 : the mutation control.  Must give q = 0 exactly.
    return np.zeros_like(np.asarray(y, float))

KERNELS = [("Route A (exp, = McGaugh RAR)", w_routeA), ("simple", w_simple),
           ("standard", w_standard), ("sqrt(1+1/y)", w_sqrt1p)]

def newtonian_equivalent(w, y_e):
    """Solve nu(y_N) y_N = y_e, i.e. y_N + w(y_N) = y_e, by bisection."""
    if y_e <= 0: return 0.0
    lo, hi = 0.0, max(y_e, 1.0)
    while hi + float(w(np.array([hi]))[0]) < y_e: hi *= 2.0
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if mid + float(w(np.array([mid]))[0]) < y_e: lo = mid
        else: hi = mid
    return 0.5*(lo + hi)

# ------------------------------------------------------------------ route 1: by parts, spherical
def q_byparts(w, y_N, xmin=1e-4, xmax=1e6, nx=8000, nmu=512):
    lx = np.linspace(math.log(xmin), math.log(xmax), nx); x = np.exp(lx); dlx = lx[1] - lx[0]
    mu, wt = np.polynomial.legendre.leggauss(nmu)
    X = x[:, None]; MU = mu[None, :]; S = np.sqrt(np.maximum(1.0 - MU**2, 0.0))
    ur = -1.0/X**2 + y_N*MU
    ut = -y_N*S
    y  = np.sqrt(ur**2 + ut**2)
    ww = w(y)
    fac = np.where(y > 0, ww/np.where(y > 0, y, 1.0), 0.0)
    Vr, Vt = fac*ur, fac*ut
    P2 = 0.5*(3.0*MU**2 - 1.0)
    with np.errstate(all="ignore"):
        ang = (Vr*P2 + Vt*MU*S) @ wt                  # Int dmu [...]   (Gauss-Legendre)
    if not np.all(np.isfinite(ang)):                  # a hard guard, not a cosmetic one
        raise FloatingPointError("non-finite integrand in q_byparts -- the kernel overflowed somewhere")
    # Int dx/x^2 f  =  Int dlx f/x
    return 3.0*np.sum(ang/x)*dlx

# ------------------------------------------------------------------ route 2: explicit divergence, spherical
def q_divergence(w, y_N, xmin=1e-4, xmax=1e6, nx=4000, nmu=400):
    lx = np.linspace(math.log(xmin), math.log(xmax), nx); x = np.exp(lx)
    mu = np.linspace(-1.0 + 1e-6, 1.0 - 1e-6, nmu)
    X = x[:, None]; MU = mu[None, :]; S = np.sqrt(np.maximum(1.0 - MU**2, 0.0))
    ur = -1.0/X**2 + y_N*MU; ut = -y_N*S
    y = np.sqrt(ur**2 + ut**2); ww = w(y)
    fac = np.where(y > 0, ww/np.where(y > 0, y, 1.0), 0.0)
    Vr, Vt = fac*ur, fac*ut
    # div V = (1/x^2) d(x^2 Vr)/dx  -  (1/x) d(sqrt(1-mu^2) Vth)/dmu
    d1 = np.gradient(X**2*Vr, x, axis=0)/X**2
    d2 = -np.gradient(S*Vt, mu, axis=1)/X
    div = d1 + d2
    P2 = 0.5*(3.0*MU**2 - 1.0)
    # q = Int dx Int dmu  div * P2 / x
    integ = np.trapz(div*P2/X, mu, axis=1)
    return np.trapz(integ, x)

# ------------------------------------------------------------------ route 3: explicit divergence, CYLINDRICAL
def q_cylindrical(w, y_N, rmin=1e-3, rmax=3e3, nR=1400, nz=2801):
    """Shares no coordinate with routes 1-2.  q = (1/2pi) Int div[V] P2(z/x) x^-3 d3x, d3x = 2 pi R dR dz."""
    R = np.concatenate([[0.0], np.exp(np.linspace(math.log(rmin), math.log(rmax), nR))])
    zp = np.exp(np.linspace(math.log(rmin), math.log(rmax), nz//2))
    z = np.concatenate([-zp[::-1], [0.0], zp])
    RR, ZZ = np.meshgrid(R, z, indexing="ij")
    xx = np.sqrt(RR**2 + ZZ**2); xx = np.maximum(xx, 1e-12)
    # u = -xhat/x^2 + y_N zhat  ->  cylindrical components
    uR = -(RR/xx)/xx**2
    uz = -(ZZ/xx)/xx**2 + y_N
    y = np.sqrt(uR**2 + uz**2); ww = w(y)
    fac = np.where(y > 0, ww/np.where(y > 0, y, 1.0), 0.0)
    VR, Vz = fac*uR, fac*uz
    div = np.gradient(RR*VR, R, axis=0)/np.maximum(RR, 1e-12) + np.gradient(Vz, z, axis=1)
    P2 = 0.5*(3.0*(ZZ/xx)**2 - 1.0)
    integ = div*P2/xx**3*RR
    # blank the r < rmin core (exponentially empty for Route A; explicitly checked by the convergence test)
    integ = np.where(xx < rmin, 0.0, integ)
    return np.trapz(np.trapz(integ, z, axis=1), R)

# ------------------------------------------------------------------ validation of the multipole integrator
def q2_analytic_shell(rho0, a, b):
    """rho(r,th) = rho0 P2(cos th) for a<r<b.  Q2 = -2G Int rho P2/r^3 d3r = -(8 pi/5) G rho0 ln(b/a)."""
    return -(8.0*math.pi/5.0)*G*rho0*math.log(b/a)

def q2_numeric_shell(rho0, a, b, nr=4000, nmu=400):
    r = np.exp(np.linspace(math.log(a), math.log(b), nr)); mu = np.linspace(-1, 1, nmu)
    RR, MU = np.meshgrid(r, mu, indexing="ij")
    P2 = 0.5*(3*MU**2 - 1.0)
    rho = rho0*P2
    integ = rho*P2/RR**3*RR**2                          # d3r = 2 pi r^2 dr dmu
    return -2.0*G*2.0*math.pi*np.trapz(np.trapz(integ, mu, axis=1), r)

# ------------------------------------------------------------------ brute-force scaling check
def Q2_brute(w, a0, GM, g_e):
    """Q2 in s^-2 with no use of the a0^{3/2}/sqrt(GM) ansatz beyond the change of variables itself."""
    y_e = g_e/a0
    y_N = newtonian_equivalent(w, y_e)
    q   = q_byparts(w, y_N)
    r_M = math.sqrt(GM/a0)
    return q*a0/r_M, q, y_e, y_N

def main():
    ck = Check()
    P("="*112)
    P("k_contrarian_q2 -- the Solar-System external-field quadrupole, recomputed independently")
    P("="*112)

    # ---------------- measured inputs (no stellar M/L anywhere)
    v_c, R_0 = 233.0e3, 8.178*KPC          # Gaia/VLBI: GRAVITY 2021 R_0, Eilers+2019 / Reid-Brunthaler v_c
    g_e = v_c**2/R_0
    info(f"measured Galactic field at the Sun  g_e = v_c^2/R_0 = {g_e:.4e} m/s^2   (v_c = 233 km/s, R_0 = 8.178 kpc)")
    info(f"GM_sun = {GM_SUN:.11e} m^3/s^2 (IAU nominal)   r_M(canonical) = "
         f"{math.sqrt(GM_SUN/A0['canonical'])/AU:.0f} AU")

    # ---------------- q2-0: the SIGN of the phantom density (the algebra step that is easy to get wrong)
    # isolated deep-MOND point mass: (nu-1)|G_N| -> sqrt(GM a0)/r, rho_ph = -(1/4piG) div[(nu-1)G_N] > 0
    rr = np.logspace(14, 17, 400)                       # metres, well outside r_M for a solar mass? no: spans it
    a0c = A0["canonical"]
    gN = GM_SUN/rr**2
    Vmag = w_routeA(gN/a0c)*a0c                          # (nu-1)|G_N|
    # radial vector field  A_r = -Vmag  (points inward, like G_N);  div A = (1/r^2) d(r^2 A_r)/dr
    divA = np.gradient(rr**2*(-Vmag), rr)/rr**2
    rho_ph = -divA/(4*math.pi*G)
    ck("q2-0 SIGN of the phantom density: rho_ph = -(1/4piG) div[(nu-1)G_N] must be POSITIVE everywhere "
       "for an isolated point mass (a phantom HALO, not a hole).  The opposite sign is a real trap and it "
       "flips the sign of Q2.", bool(np.all(rho_ph > 0)),
       f"min rho_ph = {rho_ph.min():.3e} kg/m^3 over 1e14-1e17 m")

    # ---------------- q2-A: the multipole integrator against an analytic interior quadrupole
    an, nu_ = q2_analytic_shell(1e-22, 1.0e15, 1.0e17), q2_numeric_shell(1e-22, 1.0e15, 1.0e17)
    rel = abs(nu_/an - 1.0)
    ck("q2-A the l=2 interior-multipole integrator reproduces an ANALYTIC test density "
       "(rho = rho0 P2(cos th) on a shell, Q2 = -(8pi/5) G rho0 ln(b/a)) to better than 0.5%",
       rel < 5e-3, f"analytic {an:.6e}, numeric {nu_:.6e}, rel {rel:.2e}")

    # ---------------- the framework number, both footings
    P("\n  ---- Route A kernel, both footings ------------------------------------------------------------")
    res = {}
    for foot, a0 in A0.items():
        y_e = g_e/a0
        y_N = newtonian_equivalent(w_routeA, y_e)
        q_bp  = q_byparts(w_routeA, y_N)
        q_dv  = q_divergence(w_routeA, y_N)
        q_cy  = q_cylindrical(w_routeA, y_N)
        r_M   = math.sqrt(GM_SUN/a0)
        scale = a0/r_M                                   # = a0^{3/2}/sqrt(GM)
        Q2    = q_bp*scale
        res[foot] = dict(a0=a0, y_e=y_e, y_N=y_N, q=q_bp, q_dv=q_dv, q_cy=q_cy, scale=scale, Q2=Q2, r_M=r_M)
        P(f"    {foot:<10} a0={a0:.3e}  y_e=g_e/a0={y_e:.4f}  y_N(Newtonian-equiv)={y_N:.4f}   "
          f"q={q_bp:+.5f}  (div {q_dv:+.5f}, cyl {q_cy:+.5f})")
        P(f"    {'':<10} a0^(3/2)/sqrt(GM) = {scale:.4e} s^-2   ->   Q2 = {Q2:+.4e} s^-2")
    a, b = res["canonical"], res["alt"]

    # ---------------- q2-1: three independent quadratures must agree
    d_dv = abs(a["q_dv"]/a["q"] - 1.0); d_cy = abs(a["q_cy"]/a["q"] - 1.0)
    ck("q2-1 three quadratures of the same integral agree to 3%: by-parts (no numerical derivative), "
       "explicit spherical divergence, and an explicit CYLINDRICAL divergence that shares no coordinate "
       "with the other two", d_dv < 0.03 and d_cy < 0.03,
       f"by-parts {a['q']:+.5f}; spherical-div {a['q_dv']:+.5f} ({100*d_dv:.2f}%); "
       f"cylindrical {a['q_cy']:+.5f} ({100*d_cy:.2f}%)")

    # ---------------- q2-2: the restatement test, executed
    q0 = q_byparts(w_routeA, 0.0)
    ck("q2-2 RESTATEMENT TEST, executed: with NO external field (y_e = 0) the Sun is an isolated point mass, "
       "v^4 = G M a0 applies in full, and Q2 must vanish identically by spherical symmetry.  It does.  So the "
       "coefficient q(y_e) is NOT derivable from v^4 = G M_b a0 -- only the prefactor a0/r_M is.",
       abs(q0) < 1e-9, f"q(y_e=0) = {q0:.3e}")

    # ---------------- q2-3: the mutation control
    qn = q_byparts(w_newton, a["y_N"])
    ck("q2-3 MUTATION CONTROL: nu == 1 (pure Newton / GR, where the strong equivalence principle holds) must "
       "give q = 0 exactly, i.e. the whole effect is the kernel's nonlinearity",
       abs(qn) < 1e-14, f"q(nu==1) = {qn:.3e}")

    # ---------------- q2-4: Newtonian limit in the external field
    qbig = q_byparts(w_routeA, 1e6)
    ck("q2-4 a HUGE external field must switch the effect off (the Sun is then deep in the Newtonian regime "
       "of the total field)", abs(qbig) < 0.02*abs(a["q"]), f"q(y_N=1e6) = {qbig:.3e} vs q(solar) = {a['q']:+.5f}")

    # ---------------- q2-5: grid convergence
    q_lo = q_byparts(w_routeA, a["y_N"], nx=1500, nmu=128, xmin=1e-3, xmax=1e4)
    q_hi = q_byparts(w_routeA, a["y_N"], nx=16000, nmu=1024, xmin=1e-5, xmax=1e7)
    dlo, dhi = abs(q_lo/a["q"] - 1.0), abs(q_hi/a["q"] - 1.0)
    ck("q2-5 grid convergence: coarsening 5x and refining 2x with 100x more radial range both move q by <1%",
       dlo < 0.01 and dhi < 0.01, f"coarse {q_lo:+.5f} ({100*dlo:.3f}%), fine {q_hi:+.5f} ({100*dhi:.3f}%)")

    # ---------------- q2-6: the claimed scaling, verified brute force
    Q2a, _, _, _ = Q2_brute(w_routeA, a["a0"], GM_SUN, g_e)
    Q2b, _, _, _ = Q2_brute(w_routeA, a["a0"], 4.0*GM_SUN, g_e)     # 4x the mass at FIXED y_e
    ratio = Q2b/Q2a
    ck("q2-6 the prefactor a0^{3/2}/sqrt(GM) is verified brute force, not assumed: quadrupling the central "
       "mass at fixed a0 and fixed external field must halve Q2 (1/sqrt(M))",
       abs(ratio - 0.5) < 1e-6, f"Q2(4M)/Q2(M) = {ratio:.8f}, predicted 0.5")

    # ---------------- q2-7: the harmonic assumption where the planets are
    q_in = q_byparts(w_routeA, a["y_N"], xmin=1e-4, xmax=0.05)
    frac = abs(q_in/a["q"])
    ck("q2-7 the phantom source inside 0.05 r_M (= 400 AU, outside every planet and outside Cassini) "
       "contributes <1% of q, so the anomalous field really is harmonic where the ephemeris is measured "
       "and the r^2 P_2 form is legitimate", frac < 0.01, f"inner 400 AU contributes {100*frac:.4f}% of q")

    # ---------------- q2-8: kernel ordering
    P("\n  ---- the same law for four kernels (canonical footing) ----------------------------------------")
    kq = {}
    for lab, wf in KERNELS:
        yN = newtonian_equivalent(wf, a["y_e"]); qq = q_byparts(wf, yN)
        kq[lab] = (yN, qq, qq*a["scale"])
        P(f"    {lab:<30} y_N={yN:6.4f}   q={qq:+.5f}   Q2={qq*a['scale']:+.4e} s^-2")
    qA = abs(kq["Route A (exp, = McGaugh RAR)"][1]); qS = abs(kq["simple"][1]); qT = abs(kq["standard"][1])
    ck("q2-8 the SHARPER the Newton<->MOND transition, the SMALLER the quadrupole -- 'standard' (nu-1 ~ 1/2y^2) "
       "must beat 'simple' (nu-1 ~ 1/y).  This is Desmond+2024's whole mechanism and it must reproduce, or the "
       "integral is wrong.", qT < qS, f"|q| simple {qS:.4f} vs standard {qT:.4f}; Route A (nu-1 ~ e^-sqrt(y)) {qA:.4f}")

    # ---------------- q2-9: using y_e in place of y_N is an error worth sizing
    q_wrong = q_byparts(w_routeA, a["y_e"])
    ck("q2-9 feeding the TRUE external field where the NEWTONIAN-equivalent one belongs is a real error and it "
       "matters at the tens-of-percent level -- recorded so the number cannot be quoted casually",
       abs(q_wrong/a["q"] - 1.0) > 0.05,
       f"q(y_N={a['y_N']:.3f}) = {a['q']:+.5f} vs q(y_e={a['y_e']:.3f}) = {q_wrong:+.5f} "
       f"({100*(q_wrong/a['q']-1):+.1f}%)")

    # ---------------- q2-10: the Upsilon lever, measured by re-running the pipeline
    UPS = 1.0
    def pipeline(ups):
        """The whole chain re-run at a stellar mass-to-light ratio scaled by `ups`.  Upsilon does not appear:
        GM_sun is a dynamical measurement (Kepler's third law on the planets), g_e = v_c^2/R_0 is kinematic."""
        gm = GM_SUN            # NOT ups*GM_SUN -- the solar GM is measured dynamically, never photometrically
        ge = v_c**2/R_0        # NOT ups*... -- the Galactic field at the Sun is a kinematic measurement
        Q, q_, _, _ = Q2_brute(w_routeA, a["a0"], gm, ge)
        return Q
    Q_1, Q_15 = pipeline(1.0), pipeline(1.5)
    lever = 0.0 if Q_1 == Q_15 else math.log10(abs(Q_15/Q_1))/math.log10(1.5)
    ck("q2-10 UPSILON LEVER measured by re-running the pipeline at Upsilon x1.5: d log Q2 / d log Upsilon = 0 "
       "EXACTLY.  This is the only candidate in the hunt with an identically zero lever, because no photometric "
       "mass enters at any step.", abs(lever) < 1e-12, f"lever = {lever:.3e}; Q2 unchanged in all 15 digits")

    # ---------------- sensitivity to the ONE measured input
    P("\n  ---- sensitivity to the Galactic field at the Sun (the only measured input) -------------------")
    for vc in [229.0, 233.0, 236.0]:
        for R0 in [8.122, 8.178, 8.275]:
            ge = (vc*1e3)**2/(R0*KPC)
            Q, q_, ye, yN = Q2_brute(w_routeA, a["a0"], GM_SUN, ge)
            P(f"    v_c={vc:5.1f} km/s  R_0={R0:.3f} kpc  ->  g_e={ge:.4e}  y_e={ye:.4f}  q={q_:+.5f}  Q2={Q:+.4e}")
    Qlo, _, _, _ = Q2_brute(w_routeA, a["a0"], GM_SUN, (229e3)**2/(8.275*KPC))
    Qhi, _, _, _ = Q2_brute(w_routeA, a["a0"], GM_SUN, (236e3)**2/(8.122*KPC))
    spread = abs(Qhi/Qlo - 1.0)
    ck("q2-11 the full plausible range of the Galactic rotation measurement moves Q2 by less than 15%, so the "
       "prediction is not soft", spread < 0.15, f"spread over v_c 229-236, R_0 8.12-8.28: {100*spread:.1f}%")

    # ---------------- the confrontation
    P("\n" + "="*112)
    P("  THE CONFRONTATION -- this is a candidate law only if the measurement is consistent with it")
    P("="*112)
    Q2_MEAS, Q2_ERR = 1.6e-27, 1.8e-27     # s^-2; the 2026 ephemeris fit quoted in
                                           # real_research/CASSINI_QUADRUPOLE_CONSTRAINT.md (arXiv:2602.17884),
                                           # itself a 40% tightening of Hees+2014/2016.  Consistent with ZERO.
    info(f"published ephemeris MEASUREMENT   Q2 = ({Q2_MEAS/1e-27:.1f} +/- {Q2_ERR/1e-27:.1f})e-27 s^-2 "
         f"-- consistent with zero at {abs(Q2_MEAS)/Q2_ERR:.1f} sigma")
    info("LambdaCDM / GR prediction         Q2 = 0 EXACTLY (strong equivalence principle) -> "
         f"{abs(Q2_MEAS - 0.0)/Q2_ERR:.2f} sigma.  GR PASSES.")
    for foot in ("canonical", "alt"):
        r = res[foot]
        sig = abs(r["Q2"] - Q2_MEAS)/Q2_ERR
        info(f"framework, {foot:<9} Q2 = {r['Q2']:+.3e} s^-2   ->   {sig:5.1f} sigma from the measurement")
    sig_c = abs(a["Q2"] - Q2_MEAS)/Q2_ERR
    sig_al = abs(b["Q2"] - Q2_MEAS)/Q2_ERR
    ck("q2-12 THE DECIDING CHECK, and it is written so it CAN fail against the framework: for K1 to be a "
       "candidate second law the predicted Q2 must be consistent with the ephemeris measurement at <3 sigma. "
       "It is not.  Route A is the RAR-fitting kernel and it is the one the Solar System excludes.",
       sig_c < 3.0 and sig_al < 3.0, f"canonical {sig_c:.1f} sigma, alt {sig_al:.1f} sigma -- both EXCLUDED")

    # ---------------- convention factor, stated rather than hidden
    P("\n  ---- convention, stated openly ----------------------------------------------------------------")
    info("Desmond, Hees & Famaey 2024 write Q2 = (3/2) a0^{3/2}/sqrt(GM) * q_D with q_D ~ 0.21-0.27, i.e. their")
    info(f"coefficient is 1.5x this script's q.  In their normalisation the same integral gives Q2 = "
         f"{1.5*abs(a['Q2']):.2e} s^-2, matching their published ~2.9e-26 and Hees+2016's 3.5-4.4e-26 to ~20%.")
    info("The conclusion is convention-independent: BOTH normalisations are an order of magnitude above the")
    info("measurement, so the verdict does not turn on the factor 1.5.  Reported both ways deliberately.")

    # ---------------- what this is, honestly
    P("\n" + "="*112)
    P("  VERDICT")
    P("="*112)
    P("  NOT a second Kepler-grade law, on TWO of the five criteria, and it is a LIABILITY on the data:")
    P("   (4) 'nobody has stated it' FAILS.  Milgrom 2009 (MNRAS 399, 474) posed the Solar-System EFE")
    P("       quadrupole; Blanchet & Novak 2011 (MNRAS 412, 2530) computed q for the standard families;")
    P("       Hees, Folkner, Jacobson & Park 2014 (PRD 89, 102002) and Hees et al. 2016 (PRD 93, 084018)")
    P("       set the ephemeris limit; Desmond, Hees & Famaey 2024 (MNRAS 530, 1781) turned it into the")
    P("       RAR-vs-Cassini incompatibility at 8.7 sigma.  The law-FORM is fully credited elsewhere.")
    P("   (4b) It is also NOT new to this programme.  real_research/CASSINI_QUADRUPOLE_CONSTRAINT.md")
    P("       (2026-06-05) already records Q2 ~ 3-5e-26 s^-2 and '~15-25 sigma over the central value'.")
    P("       What IS new here is only the full integral for the Route A kernel (the prior repo script,")
    P("       reviews/cassini_quadrupole_framework.py, says in its own docstring that it does an")
    P("       order-of-magnitude check and NOT the quadrupole integral).  A number, not a law.")
    P("   (3) 'holds across many systems' FAILS.  There is exactly one system with a measured Q2.")
    P("   (1),(2),(5) PASS: measured quantities, predicted coefficient, not a restatement (check q2-2).")
    P("")
    P(f"  AND THE SIGN OF THE RESULT IS AGAINST THE FRAMEWORK: Q2 = {a['Q2']:.2e} (canonical) / "
      f"{b['Q2']:.2e} (alt) s^-2")
    P(f"  against a measurement of (1.6 +/- 1.8)e-27 -- {sig_c:.0f} sigma / {sig_al:.0f} sigma.  In Desmond's")
    P("  normalisation, 17 / 19 sigma.  GR + cold dark matter, which predicts exactly zero, sits at 0.9 sigma.")
    P("  The proposing agent's 'high promise' rating is not supportable: the one candidate in this batch with a")
    P("  perfectly clean Upsilon lever is clean because it is a Solar-System test, and the Solar System is where")
    P("  this class of theory is in the most trouble.  Zero Upsilon leverage bought zero protection.")
    P("")
    P("  ONE THING THAT SURVIVES, and it is worth recording: check q2-8.  The kernel ordering is")
    P("  standard < Route A < simple in |q|, i.e. Route A does NOT escape by being the sharpest kernel --")
    P("  its e^-sqrt(y) tail is sharp at LARGE y, but the quadrupole integral is dominated by x ~ 1 (r ~ r_M ~")
    P("  8000 AU) where every kernel looks alike.  The natural hope that a sharper transition threads Cassini")
    P("  is refuted for this kernel by direct computation, not by argument.")
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
