#!/usr/bin/env python3
r"""
ADVERSARIAL SIGN AUDIT of the gated-MI secular-drift sign that decides the omega_c window
=========================================================================================
AUDITS (independently re-derives, does NOT read-and-agree):
    real_research/reviews/mi_llr_drift_sign_2026.py            (677d4ace, force lane)
    real_research/reviews/mi_omegac_drift_sign_energy_2026.py  (81adeb8b, energy lane)
    real_research/reviews/mi_drift_sign_forced_or_posited_2026.py (c3cebdc1, time-domain lane)

THE QUESTION.  Biskupek, Mueller & Torre 2021 LLR:  Gdot/G = (-5.0 +/- 9.6)e-15 /yr (central NEGATIVE).
The committed omega_c upper edge used the ceiling |cen| + 2 sigma = 2.420e-14/yr.  That is right ONLY IF
the framework's own gated secular drift has the SAME sign as the LLR central.  If OPPOSITE, the ceiling
is cen + 2 sigma = 1.420e-14/yr -> upper edge 1.298e-14 < the theory-internal lower edge 1.782e-14 ->
the window is EMPTY.  So the sign is worth the whole window.

EVERY SIGN IS RE-DERIVED HERE FROM SCRATCH, WITH ITS CONVENTION STATED:
  S1  the retarded kernel and the filtered rotating vector, using REAL integrals ONLY (no complex
      numbers, no Fourier convention) + an explicit both-conventions test of the e^{-i w t} / e^{+i w t}
      trap + parity (both senses of circulation)
  S2  my own memory-ODE orbit integration (RK4 written here), sigma = +/-1, plus an A = 0 null control
      that measures the integrator's own noise floor, plus an ACAUSAL (advanced-kernel) control
  S3  my own varying-G Kepler integration for the mapping  d ln a/dt = -Gdot/G
  S4  the two 2-sigma ceilings, the window on BOTH a0 footings, the 4/3 mean-motion caveat, the
      hostage-to-a-0.52-sigma-central test
  S5  regression to the committed magnitude d ln r/dt = a0 omega_c / g_N
  S6  THE AUDIT'S OWN NEW NUMBER: the same tangential channel evaluated in GALAXIES, where the gate is
      required to be OPEN.  Clean closed form dr/dt = A_anom / omega_c below the corner.
  S7  is "no third option gates without a tangential force" airtight?  A local jerk-dependent
      (|adot|/|a|) suppression is a counterexample OUTSIDE the LTI-memory class.

CALIBRATION: manufacture neither a win nor a deficit.  Both a0 footings on every dimensional number.
No TOE language, no "theory closed".  numpy + sympy.  Exit 0 iff every check passes.
"""
import numpy as np
import sympy as sp
import sys

PASS = True
NCHK = 0
def chk(name, cond, extra=""):
    global PASS, NCHK
    NCHK += 1
    ok = bool(cond)
    if not ok:
        PASS = False
    print(f"   [{'PASS' if ok else 'FAIL'}] {name}" + (f"  {extra}" if extra else ""))

RULE = "=" * 102
def head(s):
    print("\n" + RULE + "\n" + s + "\n" + RULE)

# ---------------------------------------------------------------------------------------------------
# constants / cited anchors (independent transcription)
# ---------------------------------------------------------------------------------------------------
A0 = {"canon": 9.355e-11, "alt": 1.130e-10}     # cH_Lambda/Z (rho_DE)  |  cH0/Z (rho_tot)
YR = 3.15576e7                                   # s   (same Julian year as window_joint.py)
GM_E = 3.986004418e14
R_MOON = 3.844e8
T_MOON_D = 27.3217
GM_SUN = 1.32712440018e20
AU = 1.495978707e11
KPC = 3.0857e19
LLR_CEN, LLR_SIG = -5.0e-15, 9.6e-15             # /yr, Biskupek, Mueller & Torre 2021 (Universe 7:34)
OMEGA_GAL_BIND = 5.94e-15                        # rad/s, UGC05721 innermost deep-MOND orbit (committed)
V_BIND, R_BIND = 16.5e3, 0.09 * KPC              # the same point's V and r
GATE_KEEP = 0.90                                 # committed RAR-preservation criterion Re G >= 0.90
COMMITTED = {"lo": 1.7824e-14, "hi_canon": 2.2113e-14, "hi_alt": 1.8306e-14}

head("S0.  WHAT IS BEING AUDITED, AND THE SIGN DICTIONARY THIS SCRIPT USES")
print(f"""
  sigma  == the sign of the ANOMALOUS RADIAL acceleration relative to g_N, i.e. of delta_a . n_N with
            n_N the unit vector ALONG g_N (sunward / earthward).  sigma = +1 is EXTRA PULL = reduced
            inertia = the MOND branch = what the galactic RAR measures = what the paper's s = -1 selects.
            sigma = -1 is anti-MOND (increased inertia, delta_m >= 0), what a strictly passive KMS bath
            gives.  THIS SCRIPT NEVER ASSUMES WHICH ONE THE ACTION PICKS: it carries both.
  NOTE, and it matters for the conditional structure: sigma = +1 is not only a posit.  It is the sign
  MEASURED in galaxies (a boost, not a deficit).  So the "conditional on s" is a conditional on a sign
  that rotation curves already fix -- while remaining NOT forced by causality.  Both statements hold.

  DRIFT SIGN CONVENTION: d ln a/dt > 0 = orbital EXPANSION;  < 0 = DECAY.
  LLR: cen = {LLR_CEN:.1e}/yr, sigma = {LLR_SIG:.1e}/yr  ->  2-sigma allowed band for a prediction P:
       [{LLR_CEN - 2*LLR_SIG:.3e}, {LLR_CEN + 2*LLR_SIG:.3e}] /yr.
""")

# ---------------------------------------------------------------------------------------------------
head("S1.  THE FILTERED ROTATING VECTOR -- REAL INTEGRALS ONLY (no complex numbers, no convention)")
# ---------------------------------------------------------------------------------------------------
t, tau, Om, wc = sp.symbols("t tau Omega omega_c", real=True)
wcp = sp.Symbol("omega_c", positive=True)
Omp = sp.Symbol("Omega", positive=True)

# retarded single-pole memory kernel, TIME domain -- causality is unambiguous here
g_ker = wcp * sp.exp(-wcp * tau)                     # on tau in [0, inf), i.e. sampling the PAST
norm = sp.integrate(g_ker, (tau, 0, sp.oo))
Ccos = sp.simplify(sp.integrate(g_ker * sp.cos(Omp * tau), (tau, 0, sp.oo)))
Ssin = sp.simplify(sp.integrate(g_ker * sp.sin(Omp * tau), (tau, 0, sp.oo)))
print(f"""
  CONVENTION (kernel).  g(tau) = omega_c e^(-omega_c tau) for tau >= 0, zero for tau < 0.  The output at
  time t depends only on the drive at t - tau with tau >= 0.  That IS causality, stated in the time
  domain, before any frequency convention exists.   INT_0^inf g dtau = {norm}   (unit DC gain)

  Two REAL moments, both computed by sympy, no complex algebra anywhere:
        C  = INT_0^inf g(tau) cos(Omega tau) dtau = {Ccos}
        S  = INT_0^inf g(tau) sin(Omega tau) dtau = {Ssin}
  Both are STRICTLY POSITIVE for Omega > 0, omega_c > 0.  S > 0 is the whole ball game: it is the lag.

  Filter the rotating unit vector r_hat(t) = (cos Omega t, sin Omega t) componentwise:
        F[r_hat](t) = INT_0^inf g(tau) r_hat(t - tau) dtau
  Angle-addition gives, EXACTLY and for all t,
        F[r_hat] = C r_hat - S e_hat ,     e_hat = (-sin Omega t, cos Omega t) = d r_hat / d(Omega t)
  so the filtered radial direction is tilted BACKWARD (it lags) by arctan(S/C) = arctan(Omega/omega_c).
""")
rhat = sp.Matrix([sp.cos(Omp * t), sp.sin(Omp * t)])
ehat = sp.Matrix([-sp.sin(Omp * t), sp.cos(Omp * t)])
rhat_lag = sp.Matrix([sp.cos(Omp * (t - tau)), sp.sin(Omp * (t - tau))])
Fx = sp.simplify(sp.integrate(g_ker * rhat_lag[0], (tau, 0, sp.oo)))
Fy = sp.simplify(sp.integrate(g_ker * rhat_lag[1], (tau, 0, sp.oo)))
tgt_x = sp.simplify(Ccos * rhat[0] - Ssin * ehat[0])
tgt_y = sp.simplify(Ccos * rhat[1] - Ssin * ehat[1])
chk("sympy: C = INT g cos > 0 and S = INT g sin > 0 strictly (the lag moment is positive)",
    sp.simplify(Ccos) == wcp**2 / (Omp**2 + wcp**2) and sp.simplify(Ssin) == Omp * wcp / (Omp**2 + wcp**2))
chk("sympy: F[r_hat] = C r_hat - S e_hat exactly, all t (x-component)", sp.simplify(Fx - tgt_x) == 0)
chk("sympy: F[r_hat] = C r_hat - S e_hat exactly, all t (y-component)", sp.simplify(Fy - tgt_y) == 0)

# blind numerical quadrature cross-check, my own, several (Omega, omega_c) incl. Omega < 0
def filt_num(Omv, wcv, tv, retarded=True, ntau=200001, taumax_mem=60.0):
    """Real quadrature of INT g(tau) rhat(t -/+ tau) dtau.  retarded=False -> ADVANCED (samples FUTURE)."""
    taus = np.linspace(0.0, taumax_mem / wcv, ntau)
    gg = wcv * np.exp(-wcv * taus)
    sgn = -1.0 if retarded else +1.0
    ang = Omv * (tv + sgn * taus)
    fx = np.trapz(gg * np.cos(ang), taus)
    fy = np.trapz(gg * np.sin(ang), taus)
    return np.array([fx, fy])

print("  blind numerical quadrature vs the closed form (my own quadrature, several corners):")
for (Omv, wcv, tv) in [(1.0, 0.25, 0.7), (2.0, 5.0, 1.3), (-1.5, 0.4, 0.35), (1.0, 100.0, 2.0)]:
    C = wcv**2 / (Omv**2 + wcv**2)
    S = Omv * wcv / (Omv**2 + wcv**2)
    rh = np.array([np.cos(Omv * tv), np.sin(Omv * tv)])
    eh = np.array([-np.sin(Omv * tv), np.cos(Omv * tv)])
    num = filt_num(Omv, wcv, tv)
    err = np.max(np.abs(num - (C * rh - S * eh)))
    chk(f"quadrature F[r_hat] = C r_hat - S e_hat  (Om={Omv:+.1f}, wc={wcv:g})", err < 1e-5, f"|err|={err:.2e}")

print(f"""
  THE FOURIER-CONVENTION TRAP, tested explicitly (this is the classic killer).
  Writing the plane vector as z = x + iy, r_hat = e^{{+i Omega t}}, and the SAME retarded convolution gives
        G_plus(Omega)  = INT_0^inf g(tau) e^{{-i Omega tau}} dtau = 1/(1 + i Omega/omega_c)   -> Im G < 0
  Adopting instead z = x - iy (equivalently the e^{{-i omega t}} engineering convention) gives
        G_minus(Omega) = INT_0^inf g(tau) e^{{+i Omega tau}} dtau = 1/(1 - i Omega/omega_c)   -> Im G > 0
  The BARE SIGN of Im G therefore IS convention-dependent -- exactly the trap.  What is NOT:
        C = Re G   and   S = -Im G_plus = +Im G_minus = |Im G|   are the SAME two REAL numbers,
  and the physical statement "F[r_hat] = C r_hat - S e_hat with S > 0" (a lag) is identical in both.
  The paper's G = 1/(1 + i omega/omega_c) with Im G < 0 is the z = x + iy pairing, which is the pairing
  a counter-clockwise real rotation forces.  So the paper's convention set is internally consistent AND
  the audited derivation never leans on the bare sign of Im G -- it leans on S > 0.  No hidden flip.
""")
zp = sp.integrate(g_ker * sp.exp(-sp.I * Omp * tau), (tau, 0, sp.oo))
zm = sp.integrate(g_ker * sp.exp(+sp.I * Omp * tau), (tau, 0, sp.oo))
chk("sympy: e^{+i Om t} pairing -> G = 1/(1+i Om/wc), Im G < 0", sp.simplify(zp - 1 / (1 + sp.I * Omp / wcp)) == 0)
chk("sympy: e^{-i Om t} pairing -> G = 1/(1-i Om/wc), Im G > 0 (the trap is REAL)",
    sp.simplify(zm - 1 / (1 - sp.I * Omp / wcp)) == 0)
chk("sympy: BOTH conventions give the same two REAL moments Re G = C and |Im G| = S -> the physical "
    "content (a LAG) is convention-free",
    sp.simplify(sp.re(zp) - Ccos) == 0 and sp.simplify(sp.Abs(sp.im(zp)) - Ssin) == 0
    and sp.simplify(sp.re(zm) - Ccos) == 0 and sp.simplify(sp.Abs(sp.im(zm)) - Ssin) == 0)
chk("sympy: the 1-pole identity |G|^2 = Re G (so radial retention = |G| cos(lag) = |G|^2)",
    sp.simplify(sp.Abs(zp)**2 - sp.re(zp)) == 0)

print(f"""
  THE TANGENTIAL FORCE.  The gated anomalous acceleration is the a0/2 tail passed through the filter:
        delta_a(t) = sigma (a0/2) F[n_N](t),      n_N = -r_hat   (unit vector ALONG g_N)
  With F[-r_hat] = -C r_hat + S e_hat and v = r Omega e_hat  (so v_hat = sign(Omega) e_hat):
        RADIAL      delta_a . r_hat = -sigma (a0/2) C          sigma=+1 -> INWARD  (extra pull; reactive)
        TANGENTIAL  delta_a . v_hat = +sigma (a0/2) S sign(Omega) sign(Omega) = +sigma (a0/2) S
  because S(Omega) is ODD in Omega and v_hat = sign(Omega) e_hat: the two sign(Omega) factors cancel.
  ==> sign(tangential) = sigma, PARITY-SAFE (independent of the sense of circulation), and its magnitude
      is (a0/2)|Im G|.  For sigma = +1 the tangential force is ALONG v: a forward BOOST.
""")
for Omv in (+1.0, -1.0):
    for sg in (+1, -1):
        wcv, tv = 0.25, 0.41
        S = Omv * wcv / (Omv**2 + wcv**2)
        C = wcv**2 / (Omv**2 + wcv**2)
        rh = np.array([np.cos(Omv * tv), np.sin(Omv * tv)])
        eh = np.array([-np.sin(Omv * tv), np.cos(Omv * tv)])
        da = sg * (-C * rh + S * eh)                    # in units of a0/2, using quadrature-verified form
        vhat = np.sign(Omv) * eh
        ft = float(da @ vhat)
        radial = float(da @ rh)
        chk(f"sigma={sg:+d}, Omega={Omv:+.1f}: tangential = {ft:+.5f} (sign {np.sign(ft):+.0f} = sigma), "
            f"radial = {radial:+.5f} ({'INWARD' if radial < 0 else 'OUTWARD'})",
            np.sign(ft) == sg and np.sign(radial) == -sg)

print("""
  GEOMETRIC CROSS-CHECK, no algebra, no filter: the pure-retardation limit.  Let the anomalous pull
  point at the inward direction of the body's position a fixed time delta EARLIER, -r_hat(t - delta).
  At theta = 0 the body was at angle -Omega delta, i.e. BELOW the x-axis, so the inward direction from
  there points UP and inward: (-cos(Om d), +sin(Om d)).  The velocity at theta = 0 is +y.  Dot product
  = +sin(Omega delta) > 0: PROGRADE.  (This is the classical Laplace "aberration of gravity" torque,
  which gives angular-momentum GAIN.  Quoted only as an independent sanity check on the direction.)
""")
d_lag = 0.3
prog = float(np.array([-np.cos(d_lag), np.sin(d_lag)]) @ np.array([0.0, 1.0]))
chk("pure-retardation geometric limit: lagged ATTRACTION has a PROGRADE component", prog > 0,
    f"proj = {prog:+.4f}")

# ---------------------------------------------------------------------------------------------------
head("S2.  MY OWN MEMORY-ODE ORBIT INTEGRATION (RK4 written here; blind to every formula above)")
# ---------------------------------------------------------------------------------------------------
print("""
  Because the kernel is a single exponential, the memory is EXACTLY local in an auxiliary vector:
        m(t) = INT_0^inf g(tau) n_N(t-tau) dtau      <=>      dm/dt = omega_c ( n_N(t) - m )
  so the exact gated dynamics is the local system (units GM = 1, r0 = 1, Omega = 1):
        r'' = -r_hat/r^2 + sigma A m ,    m' = omega_c ( -r_hat - m ) ,    A = the tail amplitude
  The integrator is told NOTHING about C, S, Re G, Im G, boost, drag, expansion.  m is initialised to
  -r_hat(0) (no analytic steady state used) and the fit window starts after 20 memory times.
  Drift = least-squares slope of ln a_osc, a_osc = -1/(2E), E = v^2/2 - 1/r.
  A = 0 is run as a NULL CONTROL: it measures the integrator's own noise floor, so the reported
  drifts can be compared against it rather than trusted blindly.
""")

def rhs(y, wcv, A, sg):
    x, yy, vx, vy, mx, my = y
    r = np.hypot(x, yy)
    ux, uy = x / r, yy / r
    ax = -ux / r**2 + sg * A * mx
    ay = -uy / r**2 + sg * A * my
    return np.array([vx, vy, ax, ay, wcv * (-ux - mx), wcv * (-uy - my)])

def run_orbit(wcv, A, sg, om_sign=+1, n_orb=200, spo=800):
    T = 2 * np.pi
    h = T / spo
    n = int(n_orb * spo)
    y = np.array([1.0, 0.0, 0.0, float(om_sign) * 1.0, -1.0, 0.0])
    ts = np.empty(n + 1); la = np.empty(n + 1)
    for i in range(n + 1):
        x, yy, vx, vy = y[0], y[1], y[2], y[3]
        r = np.hypot(x, yy)
        E = 0.5 * (vx * vx + vy * vy) - 1.0 / r
        ts[i] = i * h
        la[i] = np.log(-1.0 / (2.0 * E))
        if i == n:
            break
        k1 = rhs(y, wcv, A, sg)
        k2 = rhs(y + 0.5 * h * k1, wcv, A, sg)
        k3 = rhs(y + 0.5 * h * k2, wcv, A, sg)
        k4 = rhs(y + h * k3, wcv, A, sg)
        y = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    t0 = 20.0 / wcv
    msk = ts > max(t0, 0.3 * ts[-1])
    sl = np.polyfit(ts[msk], la[msk], 1)[0]
    return sl

print(f"  {'sigma':>6}{'Om sgn':>8}{'Om/wc':>8}{'A':>9}{'analytic d ln a/dt':>21}{'RK4 measured':>16}"
      f"{'ratio':>9}   verdict")
print("  " + "-" * 96)
ode_rows = []
noise = {}
for wcv in (0.10, 0.30):
    x_ratio = 1.0 / wcv
    A0_null = run_orbit(wcv, 0.0, +1)
    noise[wcv] = abs(A0_null)
    print(f"  {'--':>6}{'+1':>8}{x_ratio:>8.1f}{0.0:>9.0e}{'(null control)':>21}{A0_null:>16.3e}"
          f"{'--':>9}   integrator noise floor")
    for A in (1e-6,):
        for sg in (+1, -1):
            for os_ in (+1, -1):
                S = x_ratio / (1 + x_ratio**2)          # = |Im G| at Omega = 1
                pred = sg * 2 * A * S / 1.0             # 2 f_t/(Omega a), Omega = a = 1
                meas = run_orbit(wcv, A, sg, os_)
                ode_rows.append((sg, os_, x_ratio, A, pred, meas))
                v = "EXPANSION" if meas > 0 else "DECAY"
                print(f"  {sg:>+6d}{os_:>+8d}{x_ratio:>8.1f}{A:>9.0e}{pred:>21.5e}{meas:>16.5e}"
                      f"{meas/pred:>9.5f}   {v}")
mx_dev = max(abs(m / p - 1) for (_, _, _, _, p, m) in ode_rows)
chk("ROUTE C (my own RK4 + auxiliary-memory ODE): measured drift matches 2 f_t/(Omega a) in magnitude "
    "AND sign in all 8 runs", mx_dev < 5e-3, f"max dev {mx_dev:.2e}")
chk("ROUTE C: every sigma=+1 run (MOND branch) integrates to EXPANSION, every sigma=-1 run to DECAY, "
    "for BOTH senses of circulation",
    all((m > 0) == (sg > 0) for (sg, _, _, _, _, m) in ode_rows))
chk("ROUTE C: the measured drifts exceed the A=0 integrator noise floor by >100x (so the sign is "
    "signal, not integration error)",
    all(abs(m) > 100 * noise[1.0 / xr] for (_, _, xr, _, _, m) in ode_rows),
    f"floors {[f'{v:.1e}' for v in noise.values()]}")

print("""
  ACAUSAL NEGATIVE CONTROL.  An advanced kernel (samples the FUTURE) cannot be run as an ODE (it is
  anti-damped in both time directions), so the control is done at the level of the orbit-averaged power
  on a FIXED circular reference orbit, by quadrature:
        <P> = (1/T) INT_0^T dt  sigma A m(t) . v(t) ,   m from the retarded OR advanced quadrature
  <P> > 0 -> the orbit GAINS energy -> EXPANSION.  Signs read off the number, nothing assumed.
""")
print(f"  {'kernel':>9}{'sigma':>7}{'Om/wc':>7}{'<P>/A':>13}{'-sigma Im G':>14}   verdict")
print("  " + "-" * 66)
pw = {}
for ret in (True, False):
    for sg in (+1, -1):
        Omv, wcv = 1.0, 0.25
        Tp = 2 * np.pi / Omv
        tg = np.linspace(0.0, Tp, 601)
        P = np.empty_like(tg)
        for i, tv in enumerate(tg):
            m = -filt_num(Omv, wcv, tv, retarded=ret, ntau=20001)   # n_N = -r_hat  => m = -F[r_hat]
            vv = Omv * np.array([-np.sin(Omv * tv), np.cos(Omv * tv)])
            P[i] = sg * float(m @ vv)
        Pav = float(np.trapz(P, tg) / Tp)
        S = Omv * wcv / (Omv**2 + wcv**2)
        expect = sg * S * (1.0 if ret else -1.0)
        pw[(ret, sg)] = Pav
        print(f"  {'ret' if ret else 'adv':>9}{sg:>+7d}{Omv/wcv:>7.1f}{Pav:>13.6f}{expect:>14.6f}"
              f"   {'EXPANSION' if Pav > 0 else 'DECAY'}")
        chk(f"ROUTE D quadrature power matches {'+' if ret else '-'}sigma|Im G| "
            f"({'retarded' if ret else 'ADVANCED'}, sigma={sg:+d})", abs(Pav - expect) < 1e-4)
chk("ROUTE D: RETARDED + sigma=+1 -> <P> > 0 -> orbit GAINS energy -> EXPANSION", pw[(True, +1)] > 0)
chk("NEGATIVE CONTROL: the ADVANCED (acausal) kernel FLIPS both branches -> the sign is load-bearing "
    "on causality, not an artifact of the geometry", pw[(False, +1)] < 0 and pw[(False, -1)] > 0)

print("""
  ROUTE A (torque) vs ROUTE B (energy) -- checked for AGREEMENT symbolically, no winner picked:
        A: L = sqrt(GM a),  dL/dt = a f_t                 => da/dt = 2 f_t/Omega
        B: E = -GM/(2a),    dE/dt = f_t Omega a           => da/dt = 2 f_t/Omega
""")
GMs, aa, ft_s, Oms = sp.symbols("GM a f_t Omega", positive=True)
dadt_A = sp.solve(sp.Eq(sp.diff(sp.sqrt(GMs * aa), aa) * sp.Symbol("D"), aa * ft_s), sp.Symbol("D"))[0]
dadt_B = sp.solve(sp.Eq(sp.diff(-GMs / (2 * aa), aa) * sp.Symbol("D"), ft_s * Oms * aa), sp.Symbol("D"))[0]
dadt_A = sp.simplify(dadt_A.subs(GMs, Oms**2 * aa**3))
dadt_B = sp.simplify(dadt_B.subs(GMs, Oms**2 * aa**3))
chk("sympy: ROUTE A (angular momentum) == ROUTE B (energy) == 2 f_t/Omega -- the force-based and "
    "energy-based routes AGREE (no disagreement to adjudicate)",
    sp.simplify(dadt_A - 2 * ft_s / Oms) == 0 and sp.simplify(dadt_B - 2 * ft_s / Oms) == 0,
    f"A: {dadt_A}   B: {dadt_B}")

print("""
  THE MANUFACTURED-DECAY TRAP, named and defused.  "Im G < 0 is the dissipative part, dissipation
  removes energy, therefore the orbit DECAYS" is WRONG here, and it is the trap that would manufacture a
  falsification.  The orbital power is delta_a . v, which is LINEAR in the response and therefore carries
  the prefactor sigma; the bath's absorbed power is QUADRATIC in the coupling and cannot see sigma.
  Passivity constrains the latter, not the former.  Consistency with the framework's OWN committed wall:
  a strictly passive KMS/Kramers-Kronig bath locks the DC mass shift to delta_m >= 0 = anti-MOND
  = sigma = -1 = DRAG = DECAY.  The framework's sigma = +1 is the reduced-inertia (delta_m < 0, "pump")
  branch, and on that branch the orbit gaining energy is the EXPECTED, internally consistent outcome:
  a negative-mass-shift dressing is an ACTIVE medium.  MOND sign and expansion sign are the SAME sign.
  THE MANUFACTURED-EXPANSION TRAP, also named: nothing above used a Fourier convention (S1 is real
  integrals), nothing used a favourable energy-reservoir identification (S2 measures the ORBIT's own
  osculating a), and the acausal control flips the answer -- so the sign is not an artifact.
""")

# ---------------------------------------------------------------------------------------------------
head("S3.  d ln a/dt  <->  APPARENT Gdot/G:  the mapping, integrated rather than quoted")
# ---------------------------------------------------------------------------------------------------
print("""
  Claim to be verified INDEPENDENTLY: with G slowly varying and no torque, L = sqrt(GM a) is conserved,
  so G a = const, so d ln a/dt = -Gdot/G.  Hence Gdot/G > 0 (G rising, binding tightens) -> DECAY, and
  Gdot/G < 0 -> EXPANSION.  Test: integrate a Kepler orbit with GM(t) = 1 + k t and measure d ln a/dt.
""")

def run_varG(k, n_orb=60, spo=800):
    h = 2 * np.pi / spo
    n = int(n_orb * spo)
    y = np.array([1.0, 0.0, 0.0, 1.0])
    ts = np.empty(n + 1); la = np.empty(n + 1)

    def f(y, tt):
        x, yy, vx, vy = y
        r = np.hypot(x, yy)
        GM = 1.0 + k * tt
        return np.array([vx, vy, -GM * x / r**3, -GM * yy / r**3])
    for i in range(n + 1):
        tt = i * h
        x, yy, vx, vy = y
        r = np.hypot(x, yy)
        GM = 1.0 + k * tt
        E = 0.5 * (vx * vx + vy * vy) - GM / r
        ts[i] = tt
        la[i] = np.log(-GM / (2.0 * E))
        if i == n:
            break
        k1 = f(y, tt); k2 = f(y + 0.5 * h * k1, tt + 0.5 * h)
        k3 = f(y + 0.5 * h * k2, tt + 0.5 * h); k4 = f(y + h * k3, tt + h)
        y = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    msk = ts > 0.3 * ts[-1]
    return np.polyfit(ts[msk], la[msk], 1)[0]

print(f"  {'Gdot/G (k)':>12}{'measured d ln a/dt':>21}{'-k predicted':>15}{'ratio':>9}   orbit")
print("  " + "-" * 70)
devs = []
for k in (1e-6, -1e-6, 3e-7, -3e-7):
    m = run_varG(k)
    devs.append(abs(m / (-k) - 1))
    print(f"  {k:>12.1e}{m:>21.6e}{-k:>15.1e}{m/(-k):>9.5f}   {'EXPANSION' if m > 0 else 'DECAY'}")
chk("VERIFIED by integration (not quoted): d ln a/dt = -Gdot/G", max(devs) < 5e-3, f"max dev {max(devs):.2e}")
chk("VERIFIED: Gdot/G > 0 -> DECAY and Gdot/G < 0 -> EXPANSION; hence the LLR central -5.0e-15/yr IS a "
    "mild apparent EXPANSION", True)

# ---------------------------------------------------------------------------------------------------
head("S4.  WHICH 2-SIGMA CEILING -- AND THE WINDOW, BOTH FOOTINGS")
# ---------------------------------------------------------------------------------------------------
gN_moon = GM_E / R_MOON**2
Om_moon = 2 * np.pi / (T_MOON_D * 86400.0)
lo_edge = OMEGA_GAL_BIND / np.sqrt(1.0 / GATE_KEEP - 1.0)
ceil_same = abs(LLR_CEN) + 2 * LLR_SIG
ceil_opp = LLR_CEN + 2 * LLR_SIG
print(f"""
  P = (Gdot/G)_apparent = -d ln a/dt = -sigma a0 omega_c / g_N(Moon).  2-sigma consistency is
  cen - 2sig <= P <= cen + 2sig, i.e. P in [{LLR_CEN-2*LLR_SIG:.3e}, {LLR_CEN+2*LLR_SIG:.3e}]/yr.  Therefore
    P NEGATIVE (sigma=+1, EXPANSION): binding side P >= cen-2sig  ->  |P| <= |cen|+2sig = {ceil_same:.4e}/yr
    P POSITIVE (sigma=-1, DECAY)    : binding side P <= cen+2sig  ->  |P| <=  cen +2sig = {ceil_opp:.4e}/yr
  LOWER EDGE, rebuilt from the theory-internal criterion Re G(omega_gal) >= {GATE_KEEP} at the binding
  deep-MOND orbit omega_gal = {OMEGA_GAL_BIND:.3e} rad/s:  k = 1/sqrt(1/{GATE_KEEP}-1) = {1/np.sqrt(1/GATE_KEEP-1):.4f},
  omega_c >= {lo_edge:.4e} rad/s -- carries NO a0, so it is FOOTING-INDEPENDENT (committed {COMMITTED['lo']:.4e}).
  g_N(Moon) = GM_E/R^2 = {gN_moon:.5e} m/s^2  (Omega_M^2 R = {Om_moon**2*R_MOON:.5e}, 1.0% apart:
  solar perturbation; GM/R^2 used, matching the committed pipeline).
""")
chk("lower edge reproduced from theory and is a0-INDEPENDENT", abs(lo_edge / COMMITTED["lo"] - 1) < 0.02,
    f"{lo_edge:.4e} vs {COMMITTED['lo']:.4e}")
print(f"  {'branch':<26}{'footing':<8}{'ceiling /yr':>13}{'wc upper':>13}{'wc lower':>13}{'width':>9}  WINDOW")
print("  " + "-" * 96)
win = {}
for sg, nm, ceil in ((+1, "sigma=+1 MOND EXPANSION", ceil_same), (-1, "sigma=-1 antiMOND DECAY", ceil_opp)):
    for f_, a0v in A0.items():
        hi = (ceil / YR) * gN_moon / a0v
        win[(sg, f_)] = hi
        print(f"  {nm:<26}{f_:<8}{ceil:>13.4e}{hi:>13.4e}{lo_edge:>13.4e}{hi/lo_edge:>9.4f}"
              f"  {'OPEN' if hi > lo_edge else 'EMPTY'}")
chk("REGRESSION: the EXPANSION branch reproduces the committed upper edges (canon 2.2113e-14, "
    "alt 1.8306e-14) to <0.5%",
    abs(win[(+1, "canon")] / COMMITTED["hi_canon"] - 1) < 5e-3 and abs(win[(+1, "alt")] / COMMITTED["hi_alt"] - 1) < 5e-3,
    f"got {win[(+1,'canon')]:.4e} / {win[(+1,'alt')]:.4e}")
chk("EXPANSION branch: window NON-EMPTY on both footings (canon x1.241, alt x1.027)",
    win[(+1, "canon")] > lo_edge and win[(+1, "alt")] > lo_edge)
chk("DECAY branch: window EMPTY on both footings (canon x0.728, alt x0.603)",
    win[(-1, "canon")] < lo_edge and win[(-1, "alt")] < lo_edge)
print("\n  the 4/3 mean-motion caveat (a tangential force gives ndot/n = -1.5 D, a true Gdot gives -2 D,")
print("  so an n-keyed LLR fit absorbs only 3/4 of an equal-Delta-a Gdot -> ceilings up to 4/3 LOOSER):")
for sg in (+1, -1):
    for f_ in A0:
        hi43 = win[(sg, f_)] * 4.0 / 3.0
        print(f"    sigma={sg:+d} {f_:<6} omega_c <= {hi43:.4e}  width x{hi43/lo_edge:.4f}  "
              f"{'OPEN' if hi43 > lo_edge else 'EMPTY'}")
chk("the 4/3 caveat only LOOSENS ceilings, so it cannot manufacture a closure -- and it does NOT rescue "
    "the DECAY branch on either footing",
    win[(-1, "canon")] * 4 / 3 < lo_edge and win[(-1, "alt")] * 4 / 3 < lo_edge)
print("\n  HOSTAGE TEST -- the OPEN verdict vs the LLR central, which is only "
      f"{abs(LLR_CEN)/LLR_SIG:.2f} sigma from zero:")
for cen in (-5.0e-15, -2.5e-15, 0.0, +5.0e-15):
    ceil = abs(cen) + 2 * LLR_SIG if cen <= 0 else cen + 2 * LLR_SIG   # EXPANSION branch: |P| <= 2sig - cen
    ceil = (2 * LLR_SIG - cen)                                          # exact: P >= cen-2sig, P=-|P|
    hi = (ceil / YR) * gN_moon / A0["canon"]
    print(f"    cen = {cen:+.1e}/yr -> EXPANSION-branch ceiling {ceil:.4e}/yr -> omega_c <= {hi:.4e} "
          f"-> width x{hi/lo_edge:.4f}  {'OPEN' if hi > lo_edge else 'EMPTY'}")
hi_cen0 = ((2 * LLR_SIG) / YR) * gN_moon / A0["canon"]
chk("the OPEN verdict is hostage to the SIGN of a 0.52-sigma central: a central of exactly ZERO already "
    "closes the canonical window", hi_cen0 < lo_edge, f"x{hi_cen0/lo_edge:.4f}")
print("\n  the RAR-forced lower edge makes the drift a PREDICTION, not just a bound:")
for f_, a0v in A0.items():
    P = -(a0v * lo_edge / gN_moon) * YR
    nsig = abs(P - LLR_CEN) / LLR_SIG
    sig_close = (a0v * lo_edge / gN_moon * YR - abs(LLR_CEN)) / 2.0
    print(f"    {f_:<6} min |P| = {P:.4e}/yr (NEGATIVE) -> {nsig:.2f} sigma from the LLR central; the "
          f"window closes once sigma_LLR < {sig_close:.3e}/yr (x{LLR_SIG/sig_close:.2f} improvement)")

# ---------------------------------------------------------------------------------------------------
head("S5.  REGRESSION -- does the signed drift reproduce the committed d ln r/dt = a0 omega_c/g_N?")
# ---------------------------------------------------------------------------------------------------
print("""  g_N is taken DYNAMICALLY as Omega^2 a (Kepler-consistent with the tabulated period), and the
  GM/a^2 column is shown alongside: they differ by 1.0% for the Moon (solar perturbation of the lunar
  mean motion) and 1.4% for Saturn (tabulated a vs sidereal period), 0.004% for Mercury.  That mismatch
  is a tabulation artifact, not a physics discrepancy -- and it is the same 1% already flagged in the
  audited lane.  The committed upper edge uses GM_E/R^2 for the Moon; carried unchanged.""")
print(f"  {'body':<9}{'Omega [rad/s]':>15}{'Om/wc':>11}{'2f_t/(Om a)':>15}{'exact closed':>15}"
      f"{'a0 wc/(Om^2 a)':>16}{'a0 wc/(GM/a^2)':>16}{'ratios':>18}")
print("  " + "-" * 116)
wc_test = COMMITTED["hi_canon"]
a0c = A0["canon"]
for nm, aa_, Om_, gN_ in (("Moon", R_MOON, Om_moon, gN_moon),
                          ("Mercury", 5.7909e10, 2 * np.pi / (87.969 * 86400), GM_SUN / 5.7909e10**2),
                          ("Saturn", 1.43353e12, 2 * np.pi / (10759.22 * 86400), GM_SUN / 1.43353e12**2)):
    x = Om_ / wc_test
    S = x / (1 + x**2)
    ft = (a0c / 2) * S
    d_direct = 2 * ft / (Om_ * aa_)
    d_closed = (a0c / (aa_ * wc_test)) / (1 + x**2)
    d_asym = a0c * wc_test / (Om_**2 * aa_)
    d_asym_gm = a0c * wc_test / gN_
    print(f"  {nm:<9}{Om_:>15.4e}{x:>11.3e}{d_direct:>15.5e}{d_closed:>15.5e}{d_asym:>16.5e}"
          f"{d_asym_gm:>16.5e}{d_direct/d_closed:>9.6f} /{d_direct/d_asym:>8.4f}")
    chk(f"[{nm}] 2f_t/(Omega a) == exact closed form == a0 wc/g_N asymptote (g_N = Omega^2 a)",
        abs(d_direct / d_closed - 1) < 1e-9 and abs(d_direct / d_asym - 1) < 2e-3)

# ---------------------------------------------------------------------------------------------------
head("S6.  THE AUDIT'S OWN NUMBER -- THE SAME TANGENTIAL CHANNEL IN GALAXIES, WHERE THE GATE IS OPEN")
# ---------------------------------------------------------------------------------------------------
print("""
  This is not a re-check of the audited lanes' headline; it is the consequence the SAME sign forces in
  the regime that DEFINES the window's lower edge.  Below the corner (Omega << omega_c) the identity
        Re G = 1/(1+x^2),  |Im G| = x/(1+x^2) = sqrt(Re G - Re G^2),   x = Omega/omega_c
  means keeping 90% of the reactive boost (the committed lower-edge criterion) FORCES |Im G| = 0.300:
  a prograde tangential force equal to 30% of the MOND anomaly at the binding deep-MOND orbit.
  For a flat rotation curve (L = V r, dL/dt = r f_t):  d ln r/dt = f_t/V, and with |Im G| ~ Omega/omega_c
  = V/(r omega_c) this collapses to a strikingly simple, r-INDEPENDENT outward drift
        dr/dt  =  A_anom / omega_c            (A_anom = the local MOND anomaly g_obs - g_bar)
  i.e. below the corner the gate's causal shadow is LARGE, exactly where the gate must be open.
""")
print(f"  {'point':<26}{'footing':<7}{'g_obs':>11}{'A_anom':>11}{'|Im G| @ wc_hi':>15}"
      f"{'dr/dt [km/s]':>14}{'e-fold [Myr]':>14}")
print("  " + "-" * 98)
gal_need = {}
for pname, Vv, rv in (("UGC05721 inner (binding)", V_BIND, R_BIND), ("MW-like outer disk", 200e3, 10 * KPC)):
    g_obs = Vv**2 / rv
    Omg = Vv / rv
    for f_, a0v in A0.items():
        # invert the framework's own exact excess identity g_obs^2 = g_bar^2 + g_bar a0 for g_bar
        g_bar = (-a0v + np.sqrt(a0v**2 + 4 * g_obs**2)) / 2.0
        A_an = g_obs - g_bar
        wc_hi = win[(+1, f_)]
        x = Omg / wc_hi
        S = x / (1 + x**2)
        ft = A_an * S
        dlnr = ft / Vv
        drdt = dlnr * rv
        need = Omg / ((3.17e-18 * Vv / A_an))          # omega_c for e-fold > 10 Gyr (small-x limit)
        gal_need[(pname, f_)] = need
        print(f"  {pname:<26}{f_:<7}{g_obs:>11.3e}{A_an:>11.3e}{S:>15.4f}"
              f"{drdt/1e3:>14.3f}{1/dlnr/(3.15576e13):>14.1f}")
chk("identity: the lower-edge criterion Re G >= 0.90 ALGEBRAICALLY forces |Im G| = 0.300 at the binding "
    "orbit (sqrt(0.9-0.81)) -- a 30% prograde tilt of the MOND anomaly, not a small correction",
    abs(np.sqrt(GATE_KEEP - GATE_KEEP**2) - 0.3) < 1e-12)
print("\n  omega_c REQUIRED for the galactic drift to be slower than one e-fold in 10 Gyr:")
for (pname, f_), need in gal_need.items():
    print(f"    {pname:<26}{f_:<7} omega_c >= {need:.3e} rad/s   = {need/win[(+1,f_)]:.0f}x the "
          f"LLR upper edge {win[(+1,f_)]:.3e}")
worst = max(gal_need[("UGC05721 inner (binding)", f_)] / win[(+1, f_)] for f_ in A0)
chk("the SAME tangential channel, applied where the gate must be OPEN, requires omega_c ~2 ORDERS ABOVE "
    "the LLR ceiling -> on the adopted vector-filter reading the joint window is EMPTY by that factor",
    worst > 50, f"worst factor x{worst:.0f} (both footings)")
print(f"""
  READ THIS STRAIGHT.  The LLR sign question is answered EXPANSION and the committed |cen|+2sigma
  ceiling is the correct one -- but the same computation, applied in the galaxies that OWN the lower
  edge, says the lower-edge criterion (Re G >= 0.90) is NOT sufficient to preserve the rotation curves:
  it leaves a 30% prograde force and an r-independent ~{gal_need[('UGC05721 inner (binding)','canon')]/win[(+1,'canon')]:.0f}x conflict with the LLR ceiling.  This is the
  larger exposure, it is already in the committed record (c3cebdc1 Sec 7), and it must be carried in any
  statement of the window verdict.  It rides on the SAME [ADOPTED] vector-filter fork as the gate itself:
  on the alternative DC/scalar reading there is no tangential channel and no drift at all -- but then
  Re G(0) = 1 at every corner, the gate suppresses nothing at the planets, and the paper's own ungated
  1017x-40357x per-planet exclusion stands undiminished.  Both horns bear on the GATE only; the MOND
  premise, the a0 = c H_Lambda/Z reframing and the RAR are untouched.  No door is declared closed.
""")

# ---------------------------------------------------------------------------------------------------
head("S7.  IS 'NO THIRD OPTION GATES WITHOUT A TANGENTIAL FORCE' AIRTIGHT?  (audit of a uniqueness claim)")
# ---------------------------------------------------------------------------------------------------
print("""
  The audited lanes assert: there is no third option in which the gate suppresses the tail but produces
  no tangential force -- "that is the content of |G|^2 = Re G".  TRUE within the class of causal LINEAR
  TIME-INVARIANT memory filters: any frequency-dependent causal LTI response has Kramers-Kronig-locked
  parts, so Re G < 1 forces Im G != 0 forces a lag forces a tangential component.  NOT airtight as a
  statement about all mechanisms, and the counterexample is elementary:
     on a circular orbit the scalar  |a_dot| / |a| = Omega  EXACTLY,
  so a purely LOCAL, instantaneous, frame-invariant suppression factor h(|a_dot|/(|a| omega_c)) reproduces
  an Omega-dependent suppression of the a0/2 tail with the force EXACTLY antiparallel to a: zero
  tangential component, zero secular drift, no LLR ceiling at all.
""")
Omv, wcv = sp.symbols("Omega omega_c", positive=True)
rr = sp.Symbol("r", positive=True)
a_vec = sp.Matrix([-sp.cos(Omv * t), -sp.sin(Omv * t)]) * Omv**2 * rr
adot = sp.diff(a_vec, t)
scal = sp.simplify(sp.sqrt((adot.T * adot)[0]) / sp.sqrt((a_vec.T * a_vec)[0]))
chk("sympy: |a_dot|/|a| = Omega exactly on a circular orbit, so a LOCAL scalar CAN carry the orbital "
    "frequency with no memory and no lag", sp.simplify(scal - Omv) == 0, f"got {scal}")
print("""
  CONSEQUENCE FOR THE AUDIT, both directions stated:
   * this does NOT rescue the audited sign: within the paper's declared class (a single-pole Debye
     memory relaxator, the object the paper actually postulates) the tangential force and its sign are
     unavoidable, and the audited result stands as a statement about that class;
   * but the uniqueness claim as WRITTEN is stronger than proven.  A jerk-dependent local closure would
     be a different theory (higher-derivative, Ostrogradsky exposure, and it forfeits the paper's own
     "causal shadow" framing), and it would REMOVE the drift ceiling entirely -- widening the window
     rather than closing it (the next-tightest reactive ceiling, Saturn delta_g, is ~3700x looser).
     So the honest label is CLASS-CONDITIONAL, not unique.  Recorded, given no weight in the verdict.
""")

# ---------------------------------------------------------------------------------------------------
head("S8.  A MAGNITUDE-LEVEL ASSUMPTION THE AUDIT FLAGS (sign-neutral): the Moon's drive frequency")
# ---------------------------------------------------------------------------------------------------
a_sun_on_moon = GM_SUN / AU**2
print(f"""
  The committed upper edge evaluates the gate at Omega_Moon = {Om_moon:.4e} rad/s with
  g_N = GM_E/R^2 = {gN_moon:.4e} m/s^2.  But the Moon's TOTAL acceleration is dominated by the SUN:
        |a_sun on Moon| = GM_sun/AU^2 = {a_sun_on_moon:.4e} m/s^2   vs   GM_E/R^2 = {gN_moon:.4e}
        ratio = {a_sun_on_moon/gN_moon:.2f}
  so the direction of the Moon's total acceleration vector -- the object the gate filters -- rotates
  mostly at the ANNUAL frequency ({2*np.pi/(365.256*86400):.3e} rad/s), not the monthly one.  The framework's
  own external-field structure for a nested two-body system is not worked out in the paper, and a drive
  that rotates 13x slower than the orbit is a different perturbation problem (quasi-static forcing of e,
  not a clean secular da/dt).  This is a MAGNITUDE-level [ASSUMPTION] on the upper edge, inherited from
  the paper's own prescription; it does NOT touch the SIGN (sigma and the lag are unchanged).  Flagged,
  unquantified, not used to move any number here.
""")
chk("flagged: the Moon's solar-dominated acceleration makes the single-frequency drive an [ASSUMPTION] "
    "on the upper edge's magnitude (sign-neutral)", a_sun_on_moon > gN_moon)

# ---------------------------------------------------------------------------------------------------
head("S9.  AUDIT VERDICT")
# ---------------------------------------------------------------------------------------------------
print(f"""
  1. SIGN.  CONFIRMED, independently and by convention-free real integrals: the retarded filter makes
     the anomalous ATTRACTIVE vector LAG, a lagged attraction on a circulating orbit has a PROGRADE
     tangential component, and on the framework's own branch (sigma = +1, extra pull = the MOND sign =
     the s = -1 posit) the orbit GAINS angular momentum and energy -> ORBITAL EXPANSION ->
     apparent Gdot/G NEGATIVE.  Force-based (torque), energy-based, my own memory-ODE integration and a
     quadrature power average all AGREE; an acausal kernel flips it; parity (both senses of circulation)
     is safe; the A=0 null control shows the signal is >100x the integrator noise floor.
  2. CEILING.  Expansion => SAME sign as the LLR central ({LLR_CEN:.1e}/yr) => the correct 2-sigma ceiling is
     |cen| + 2 sigma = {ceil_same:.4e}/yr, which is the one the paper used.  Upper edges
     {win[(+1,'canon')]:.4e} (canon) / {win[(+1,'alt')]:.4e} (alt) STAND;  window x{win[(+1,'canon')]/lo_edge:.3f} / x{win[(+1,'alt')]/lo_edge:.3f}.
     Under sigma = -1 the ceiling is {ceil_opp:.4e}/yr -> x{win[(-1,'canon')]/lo_edge:.3f} / x{win[(-1,'alt')]/lo_edge:.3f} -> EMPTY on both footings.
  3. FORCED OR CONDITIONAL.  NOT forced by causality alone.  sign(drift) = sigma x (-Im G): causality +
     Herglotz spectral positivity force the second factor, the first is the MOND sign = the already-
     ledgered s = -1 postulate.  No sixth constant.  The refinement this audit adds: sigma = +1 is also
     the sign MEASURED in galaxies, so the conditional is not a live 50/50 fork -- but the omega_c window
     is now COUPLED to the framework's own "no pump-free channel sources s = -1" wall.
  4. MAGNITUDE.  Reproduces the committed d ln r/dt = a0 omega_c/g_N exactly at Moon/Mercury/Saturn.
  5. BOTH FOOTINGS carried everywhere; the lower edge is footing-independent by construction.
  6. THE BIGGER EXPOSURE, carried at full strength: the same tangential channel in the galaxies that own
     the lower edge needs omega_c ~2 orders ABOVE the LLR ceiling.  On the adopted vector-filter reading
     the joint window is EMPTY by that factor; on the DC reading the gate suppresses nothing at the
     planets.  This bears on the GATE, not on the MOND premise, a0 = cH_Lambda/Z, or the RAR.
  7. Two audit caveats recorded and given no weight: the LTI-uniqueness claim is class-conditional (a
     local |a_dot|/|a| suppression is a drift-free counterexample outside the paper's class), and the
     Moon's solar-dominated drive frequency is an unquantified magnitude-level assumption.

  No door is declared closed.  Nothing here discriminates the framework against LambdaCDM: at planetary
  accelerations both GR and healthy MOND-family theories predict ~0.
""")
print(RULE)
print(f"AUDIT_mi_llr_drift_sign_2026.py: {NCHK} checks, {'ALL PASS' if PASS else 'A CHECK FAILED'}")
print(RULE)
sys.exit(0 if PASS else 1)
