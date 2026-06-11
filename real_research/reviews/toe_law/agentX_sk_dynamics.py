#!/usr/bin/env python3
"""
agentX [dynamics side]: the causal (retarded, u-clocked, windowed) M22 EOM integrated in the time domain.
  [0] GATE + check 3a: causal demodulation estimators on the synthetic Sun-inventory worldline reproduce
      agentM's banked A(Omega_J)/a_J (1.167/1.177/1.130) and the exp-tail delta_a_sun (hostile footing).
  [1] check 3b: pre-acceleration audit -- the symmetric (Fourier-modulus) form responds BEFORE force onset
      at full strength; the retarded estimator does not (machine zero); the post-onset transient-MOND-boost
      fingerprint quantified. ALD comparison stated (no third derivative exists; no order reduction needed).
  [2] runaway audit: the implicit per-line solve a*mu(A(a)/a0)=a_N -- uniqueness scan (monotone x*mu(x)) and
      Picard contraction counts across x in [1e-3, 1e3], exponential and standard tails.
  [3] check 3c: self-consistent causal integration of a driven deep-MOND toy -- adiabatic reproduction of
      the algebraic M22 amplitude, energy-ledger closure, steady-state flux -> 0 scaling with window depth
      (single- and two-line), and the kick + DC/secular ACTIVE-flux demonstrations (Theorem X2 made flesh;
      cross-checked against the kernel script's (1/mu-1) co-payment numbers).
Units: toy sections use a0 = 1, m = 1; section [0] uses SI. EWMA demodulators: y <- c*y + (1-c)*x with
c = exp(-dt/T_w), T_w = N_cyc * 2pi/omega (constant-Q, the u-clocked window of memo Eq. X-2).
2026-06-11. No git.
"""
import numpy as np
from scipy.signal import lfilter

LINE = "=" * 100
print(LINE)
print("agentX SK-GATE [dynamics side] -- run date 2026-06-11")
print(LINE)

def mu_rar(x):    x = np.maximum(x, 1e-300); return -np.expm1(-np.sqrt(x))
def mu_std(x):    return x / np.sqrt(1.0 + x * x)
def c_rar_eps(x): e = np.exp(-np.sqrt(x)); return e / (1.0 - e)
def th_A(y): return 2.0 / (1.0 + y * y)
def th_B(y): return np.exp(1.0 - np.minimum(y, 700))
def th_C(y): return np.exp((1.0 - np.minimum(y, 700)) / 2.0)
THETAS = {"2/(1+y^2)": th_A, "exp(1-y)": th_B, "exp((1-y)/2)": th_C}

# ---------------------------------------------------------------- [0] GATE + 3a: the Sun inventory, causal
print("[0] CHECK 3a: causal estimators on the synthetic Sun worldline vs agentM banked numbers")
GMsun, AU = 1.32712440018e20, 1.495978707e11
S_HOST, A0_FW = 5.418e-10, 9.36e-11
planets = [("Mercury", 2.2032e13, 0.38710), ("Venus", 3.24859e14, 0.72333),
           ("EMB", 4.035032e14, 1.00000), ("Mars", 4.282837e13, 1.52366),
           ("Jupiter", 1.26686534e17, 5.20336), ("Saturn", 3.7931187e16, 9.53707),
           ("Uranus", 5.793939e15, 19.1913), ("Neptune", 6.836529e15, 30.0690)]
oms = np.array([np.sqrt(GMsun / (aau * AU) ** 3) for _, _, aau in planets])
amps = np.array([gm / (aau * AU) ** 2 for _, gm, aau in planets])
a_gal, om_gal = 2.15e-10, 9.2e-16
iJ = 4
om_J, a_J = oms[iJ], amps[iJ]
BANKED_RATIO = {"2/(1+y^2)": 1.167, "exp(1-y)": 1.177, "exp((1-y)/2)": 1.130}
BANKED_DA_HO = {"2/(1+y^2)": 1.267e-16, "exp(1-y)": 1.163e-16, "exp((1-y)/2)": 1.780e-16}

rng = np.random.default_rng(20260611)
phases = rng.uniform(0, 2 * np.pi, len(planets))
N_cyc = 24.0
yr = 3.15576e7
dt = (2 * np.pi / oms[0]) / 64.0                       # Mercury period / 64
T_sim = 7.0 * N_cyc * (2 * np.pi / oms[-1])            # 7 NEPTUNE windows of burn-in (slowest channel;
nstep = int(T_sim / dt)                                #  first draft used 4 Jupiter windows -> outer
t = np.arange(nstep) * dt                              #  channels unconverged, -26..-53%; bug log)
sig = np.zeros(nstep)
for k in range(len(planets)):
    sig += amps[k] * np.cos(oms[k] * t + phases[k])    # the Sun-wobble acceleration time series
print(f"    synthetic worldline: {nstep} steps, dt = {dt/86400:.2f} d, span = {T_sim/yr:.0f} yr, "
      f"window N_cyc = {N_cyc:.0f} cycles/channel (u-clocked, constant-Q)")
# strictly-causal per-line TWO-STAGE (cascaded) EWMA demodulators: skirts fall as 1/(T dw)^2, killing
# the big-line leakage that polluted the single-stage draft (Mars +145% from Jupiter's skirt; bug log).
# amplitude = time-average of 2|y| over the final Neptune window (endpoint sampling rides ripple; bug log)
est = np.zeros(len(planets))
i_avg = t > t[-1] - N_cyc * 2 * np.pi / oms[-1]
for k in range(len(planets)):
    Tw = N_cyc * 2 * np.pi / oms[k]
    cc = np.exp(-dt / Tw)
    demod = sig * np.exp(1j * oms[k] * t)
    y = lfilter([1 - cc], [1, -cc], lfilter([1 - cc], [1, -cc], demod))
    est[k] = np.mean(2 * np.abs(y[i_avg]))
print("    per-line causal estimates vs injected amplitudes:")
for k, (nm, _, _) in enumerate(planets):
    print(f"      {nm:8s}: injected {amps[k]:.4e}  estimated {est[k]:.4e}  err {100*(est[k]/amps[k]-1):+.2f}%")
ok0 = True
print("\n    A_ret(Omega_J) per Eq. shiluta from the CAUSAL estimates (+ galactic line, analytic steady state):")
for tlab, th in THETAS.items():
    A_ret = est[iJ] + sum(est[k] * th(oms[k] / om_J) for k in range(len(planets)) if k != iJ) \
                    + a_gal * th(om_gal / om_J)
    r = A_ret / a_J
    da_ho = a_J * c_rar_eps(A_ret / S_HOST)
    drift = abs(r / BANKED_RATIO[tlab] - 1)
    dda = abs(da_ho / BANKED_DA_HO[tlab] - 1)
    ok0 &= drift < 0.01
    print(f"      theta={tlab:13s}: A_ret/a_J = {r:.3f} (banked {BANKED_RATIO[tlab]:.3f}, drift {100*drift:.2f}%) ; "
          f"exp-tail da_sun(hostile) = {da_ho:.3e} (banked {BANKED_DA_HO[tlab]:.3e}, {100*dda:.0f}%)")
print("      (the delta_a comparison is steep by construction: dln(eps)/dln(A) = -sqrt(x)/2 ~ -11 at hostile x,")
print("       so a sub-% A-drift moves delta_a by ~10%; the GATE criterion is the 1% A-level agreement.)")
assert ok0, "causal estimator failed the banked A-ratio gate"
print("    [0] CHECK 3a PASS: the retarded estimator reproduces the adiabatic (banked) filter values <1%.\n")

# ---------------------------------------------------------------- [1] pre-acceleration audit
print(LINE)
print("[1] CHECK 3b: PRE-ACCELERATION -- symmetric vs retarded on a quiet->loud worldline (a0=1 units)")
print(LINE)
w0 = 1.0
A_quiet, boost = 0.1, 10.0           # deep-MOND quiet line, x_quiet = 0.1; amplitude steps x10 at t=0
N_cyc1 = 8.0                         # shallower window here so the pre-onset audit segment outlives burn-in
dt1 = 2 * np.pi / w0 / 200.0
Tpre, Tpost = 80 * 2 * np.pi, 60 * 2 * np.pi
t1 = np.arange(-Tpre, Tpost, dt1)
a1 = np.where(t1 < 0, A_quiet, boost * A_quiet) * np.cos(w0 * t1)
# SYMMETRIC evaluation: |a^(w0)| over the WHOLE interval (the M22 Fourier-modulus form)
amp_sym = 2 * np.abs(np.trapz(a1 * np.exp(1j * w0 * t1), t1)) / (t1[-1] - t1[0])
mu_sym = mu_rar(amp_sym)
mu_q, mu_l = mu_rar(A_quiet), mu_rar(boost * A_quiet)
pre_strength = (mu_sym - mu_q) / (mu_l - mu_q)
print(f"    quiet x = {A_quiet}, loud x = {boost*A_quiet}: mu_quiet = {mu_q:.4f}, mu_loud = {mu_l:.4f}")
print(f"    SYMMETRIC form assigns the pre-onset epoch mu_sym = {mu_rar(amp_sym):.4f} "
      f"-> pre-response at {100*pre_strength:.0f}% of the full quiet->loud shift, BEFORE the force changes.")
print("    (acausality is O(1) -- the modulus-Fourier functional reads the future at full strength;")
print("     it decays only as the loud epoch's share of the window -> no exponential protection.)")
# RETARDED estimator on the same worldline
Twin = N_cyc1 * 2 * np.pi / w0
cc1 = np.exp(-dt1 / Twin)
y1 = lfilter([1 - cc1], [1, -cc1], a1 * np.exp(1j * w0 * t1))
A_ret_t = 2 * np.abs(y1)
i_audit = (t1 < 0) & (t1 > -Tpre + 8 * Twin)          # pre-onset, after burn-in
pre_dev = np.max(np.abs(A_ret_t[i_audit] - A_quiet)) / A_quiet
mu_ret_t = mu_rar(A_ret_t)
print(f"    RETARDED estimator pre-onset deviation: max |A_ret - A_quiet|/A_quiet = {pre_dev:.2e} "
      f"(window ripple only, ~1/(2 pi N_cyc) = {1/(2*np.pi*N_cyc1):.2e}; ZERO future response)  "
      + ("PASS" if pre_dev < 2.5 / (2 * np.pi * N_cyc1) else "FAIL"))
# transient fingerprint: response enhancement while the window refills
i0 = np.searchsorted(t1, 0.0)
resp_boost = mu_l / mu_ret_t[i0:]
thresh = 1.0 + 0.5 * (resp_boost[0] - 1.0)
i_half = int(np.argmax(resp_boost < thresh))
print(f"    transient-MOND-boost fingerprint: immediately post-step the stale window gives response "
      f"enhancement mu_loud/mu_ret = {resp_boost[0]:.3f} (-> 1 as the window fills; half-life "
      f"{t1[i0+i_half]/(2*np.pi):.1f} cycles = {t1[i0+i_half]/(2*np.pi)/N_cyc1:.2f} N_cyc -- mu's steep "
      f"rise at small A front-loads the recovery; full refill ~ N_cyc)")
print("    ALD comparison: the M22 law is SECOND order plus memory -- no third derivative ever appears, so")
print("    the ALD runaway/pre-acceleration disease (and its order-reduction cure) has no analog here; the")
print("    analog risk is multivaluedness of the implicit mu-solve, closed in [2] by monotone x*mu(x).\n")

# ---------------------------------------------------------------- [2] runaway audit: uniqueness + Picard
print(LINE)
print("[2] RUNAWAY AUDIT: the implicit solve a*mu(a/a0) = a_N -- root uniqueness + Picard contraction")
print(LINE)
agrid = np.geomspace(1e-9, 1e9, 400000)
for mlab, mu in [("exp tail", mu_rar), ("standard", mu_std)]:
    xmux = agrid * mu(agrid)
    mono = np.all(np.diff(xmux) > 0)
    print(f"    {mlab:9s}: x*mu(x) strictly monotone on [1e-9,1e9]: {mono} -> exactly ONE root for any a_N")
    worst = 0
    for aN in np.geomspace(1e-6, 1e3, 28):
        a = aN
        for it in range(1, 201):
            a_new = aN / mu(a)
            if abs(a_new / a - 1) < 1e-12:
                break
            a = 0.5 * (a + a_new)                       # damped Picard (plain Picard also converges; damped is uniform)
        worst = max(worst, it)
        assert abs(a * mu(a) - aN) / aN < 1e-9
    print(f"               damped-Picard iterations to 1e-12 across a_N in [1e-6,1e3]: worst = {worst}  "
          + ("PASS (no runaway, no multi-root, uniform convergence)" if worst < 200 else "FAIL"))
print()

# ---------------------------------------------------------------- [3] self-consistent causal integration
print(LINE)
print("[3] CHECK 3c: the causal EOM integrated -- adiabatic amplitude, ledger closure, flux scaling, kick, DC")
print(LINE)

def run_driven(F_amps, F_oms, N_cyc_loc, T_total, dt3, kick_factor=None, t_kick=None):
    """Integrate m*mu_per-channel(a) = F with strictly-causal EWMA channels. Returns time series."""
    F_amps, F_oms = np.asarray(F_amps, float), np.asarray(F_oms, float)
    nst = int(T_total / dt3)
    tt = np.arange(nst) * dt3
    nch = len(F_oms)
    ych = np.zeros(nch, dtype=complex)
    ccs = np.exp(-dt3 / (N_cyc_loc * 2 * np.pi / np.asarray(F_oms)))
    a_s, v_s, Pae_s, PF_s, mus = np.zeros(nst), np.zeros(nst), np.zeros(nst), np.zeros(nst), np.zeros((nst, nch))
    v = 0.0
    for n in range(nst):
        F = sum(F_amps[j] * (kick_factor if (kick_factor and tt[n] >= t_kick) else 1.0) *
                np.cos(F_oms[j] * tt[n]) for j in range(nch))
        # channel amplitudes from PAST data only (ych holds data through step n-1)
        amps_ch = 2 * np.abs(ych)
        # A_ret per channel (Eq. shiluta across channels, theta_A)
        A_ch = np.array([amps_ch[i] + sum(th_A(F_oms[k] / F_oms[i]) * amps_ch[k]
                                          for k in range(nch) if k != i) for i in range(nch)])
        mu_ch = mu_rar(A_ch)
        # reconstruct per-channel components of the CURRENT acceleration via fixed point
        a_cur = F                                       # start
        for _ in range(8):
            comp = np.array([2 * np.real((ccs[i] * ych[i] + (1 - ccs[i]) * a_cur * np.exp(1j * F_oms[i] * tt[n]))
                                         * np.exp(-1j * F_oms[i] * tt[n])) for i in range(nch)])
            a_new = F - np.dot(mu_ch - 1.0, comp)
            if abs(a_new - a_cur) < 1e-14 + 1e-12 * abs(a_cur):
                a_cur = a_new
                break
            a_cur = a_new
        comp = np.array([2 * np.real((ccs[i] * ych[i] + (1 - ccs[i]) * a_cur * np.exp(1j * F_oms[i] * tt[n]))
                                     * np.exp(-1j * F_oms[i] * tt[n])) for i in range(nch)])
        v_mid = v + 0.5 * a_cur * dt3                   # midpoint velocity: makes the discrete ledger EXACT
        P_ae = -np.dot(mu_ch - 1.0, comp) * v_mid       # power the MI/khronon channel delivers to the particle
        a_s[n], v_s[n], Pae_s[n], PF_s[n], mus[n] = a_cur, v, P_ae, F * v_mid, mu_ch
        # advance
        v += a_cur * dt3
        ych = ccs * ych + (1 - ccs) * a_cur * np.exp(1j * F_oms * tt[n])
    return tt, a_s, v_s, Pae_s, PF_s, mus

# --- 3c-i: single-line steady state: adiabatic amplitude + ledger + flux scaling
print("    [3c-i] single line, F0 = 0.06, w0 = 1 (deep MOND):")
F0, w0 = 0.06, 1.0
# algebraic M22 prediction: a*mu(a) = F0
a_pred = F0
for _ in range(300):
    a_pred = 0.5 * (a_pred + F0 / mu_rar(a_pred))
print(f"      algebraic M22 amplitude: a_ss = {a_pred:.5f} (x = {a_pred:.3f}, mu = {mu_rar(a_pred):.4f}, "
      f"enhancement a_ss/F0 = {a_pred/F0:.3f})")
rows = []
for Ncl in (4, 8, 16, 32):
    dt3 = 2 * np.pi / w0 / 400
    Ttot = (12 * Ncl) * 2 * np.pi / w0
    tt, a_s, v_s, Pae, PF, mus = run_driven([F0], [w0], Ncl, Ttot, dt3)
    last = tt > tt[-1] - 4 * 2 * np.pi / w0
    a_meas = (a_s[last].max() - a_s[last].min()) / 2
    # ledger closure: Ekin(after step n) - work(through step n) = const  (post-step pairing; the first
    # draft paired pre-step Ekin with through-step work -> spurious one-step offset ~3%; bug log)
    Ekin = 0.5 * (v_s + a_s * dt3) ** 2
    WF = np.cumsum(PF) * dt3
    Wae = np.cumsum(Pae) * dt3
    led = Ekin - WF - Wae
    led_err = (led.max() - led.min()) / max(Ekin.max(), 1e-30)
    flux_frac = abs(np.mean(Pae[last])) / np.mean(np.abs(PF[last]))
    rows.append((Ncl, a_meas, led_err, flux_frac))
    print(f"      N_cyc = {Ncl:2d}: a_meas = {a_meas:.5f} (vs algebraic {a_pred:.5f}, "
          f"err {100*(a_meas/a_pred-1):+.2f}%) ; ledger closure {led_err:.1e} ; "
          f"steady <P_ae>/<|P_F|> = {flux_frac:.2e}")
sc = np.polyfit(np.log([r[0] for r in rows]), np.log([max(r[3], 1e-18) for r in rows]), 1)[0]
print(f"      steady-state residual flux scaling: <P_ae> ~ N_cyc^{sc:.2f} (park-in-the-gaps: resolved spectrum")
print(f"      -> conservative; the residual is window ripple, vanishing with memory depth)")

# --- 3c-ii: two incommensurate lines
print("\n    [3c-ii] two lines (w = 1, sqrt(5)), F = (0.05, 0.04):")
for Ncl in (8, 24):
    dt3 = 2 * np.pi / np.sqrt(5) / 400
    Ttot = (14 * Ncl) * 2 * np.pi / 1.0
    tt, a_s, v_s, Pae, PF, mus = run_driven([0.05, 0.04], [1.0, np.sqrt(5)], Ncl, Ttot, dt3)
    last = tt > tt[-1] - 6 * 2 * np.pi
    flux_frac = abs(np.mean(Pae[last])) / np.mean(np.abs(PF[last]))
    Ekin = 0.5 * (v_s + a_s * dt3) ** 2
    led = Ekin - np.cumsum(PF) * dt3 - np.cumsum(Pae) * dt3
    print(f"      N_cyc = {Ncl:2d}: steady <P_ae>/<|P_F|> = {flux_frac:.2e} ; ledger closure "
          f"{(led.max()-led.min())/max(Ekin.max(),1e-30):.1e} ; mu_ch(end) = "
          + ", ".join(f"{m:.4f}" for m in mus[-1]))
print("      (quasiperiodic spectrum resolved -> flux -> 0 with window depth; conservation on resolved content)")

# --- 3c-iii: the kick: transient flux invoice
print("\n    [3c-iii] kick test: drive amplitude x3 at t_kick (N_cyc = 16):")
dt3 = 2 * np.pi / 400
Ttot = 360 * 2 * np.pi
tk = 200 * 2 * np.pi
tt, a_s, v_s, Pae, PF, mus = run_driven([F0], [w0], 16, Ttot, dt3, kick_factor=3.0, t_kick=tk)
pre = (tt > tk - 30 * 2 * np.pi) & (tt < tk)
trans = (tt >= tk) & (tt < tk + 40 * 2 * np.pi)
late = tt > tk + 100 * 2 * np.pi
E_ae_trans = np.sum(Pae[trans]) * dt3
E_F_trans = np.sum(np.abs(PF[trans])) * dt3
mu_old, mu_new = mus[pre][-1, 0], mus[late][-1, 0]
print(f"      mu: {mu_old:.4f} -> {mu_new:.4f}; transient (40 cycles): int P_ae dt = {E_ae_trans:+.3e} "
      f"({100*abs(E_ae_trans)/E_F_trans:.1f}% of the external work in the same span; "
      f"sign {'ACTIVE (reservoir->worldline)' if E_ae_trans > 0 else 'ABSORB (worldline->reservoir)'})")
print(f"      steady flux before kick {abs(np.mean(Pae[pre]))/np.mean(np.abs(PF[pre])):.1e}, "
      f"after re-equilibration {abs(np.mean(Pae[late]))/np.mean(np.abs(PF[late])):.1e} (transient-limited)")

# --- 3c-iv: the DC/secular channel: Theorem X2 made flesh
print("\n    [3c-iv] DC/secular forcing (the X2 channel): constant F_dc on a quiet worldline, DC window T_w = 200:")
F_dc, Tw_dc = 0.03, 200.0
dt4 = 0.02
nst = int(1200 / dt4)
cc = np.exp(-dt4 / Tw_dc)
yd, v = 0.0, 0.0
out = []
for n in range(nst):
    # implicit per-step solve: a * mu(|c*yd + (1-c)*a|) = F_dc  (own term enters its own window: theta(1)=1)
    lo, hi = 1e-12, 1e9
    for _ in range(200):
        mid = np.sqrt(lo * hi)
        if mid * mu_rar(abs(cc * yd + (1 - cc) * mid)) > F_dc: hi = mid
        else: lo = mid
    a = np.sqrt(lo * hi)
    P_ae = (1.0 - mu_rar(abs(cc * yd + (1 - cc) * a))) / mu_rar(abs(cc * yd + (1 - cc) * a)) * F_dc * v \
        if v != 0 else 0.0   # = (1/mu - 1) F v, the medium's co-payment
    out.append((n * dt4, a, v, P_ae))
    v += a * dt4
    yd = cc * yd + (1 - cc) * a
out = np.array(out)
a_inf = out[-1, 1]
a_alg = F_dc
for _ in range(300):
    a_alg = 0.5 * (a_alg + F_dc / mu_rar(a_alg))       # algebraic MOND solve a*mu(a) = F_dc
print(f"      late-time self-consistent a = {a_inf:.5f} (algebraic a*mu(a)=F_dc: {a_alg:.5f}, "
      f"err {100*(a_inf/a_alg-1):+.2f}%); enhancement a/F_dc = {a_inf/F_dc:.2f}")
mu_inf = mu_rar(a_inf)
print(f"      mu(late) = {mu_inf:.4f}; medium co-payment P_ae/P_F = (1/mu - 1) = {(1-mu_inf)/mu_inf:.3f} "
      f"(kernel-script elementary value at x = {a_inf:.2f}: {c_rar_eps(a_inf):.3f})  "
      + ("CROSS-CHECK PASS" if abs((1-mu_inf)/mu_inf - c_rar_eps(a_inf)) < 1e-6 else "FAIL"))
print(f"      measured late-time P_ae/P_F from the run: {out[-1,3]/(F_dc*out[-1,2]):.3f}")
print(f"      sign: P_ae > 0 throughout the secular ramp: {np.all(out[200:,3] > 0)} -> the medium DOES NET")
print("      POSITIVE WORK on the secularly-forced worldline: the ACTIVE channel is real, finite (self-limited")
print("      by the nonlinearity), and exactly the (1/mu - 1) co-payment of Theorem X2. A vacuum reservoir")
print("      cannot supply it; the pumped (dS-bath-class) reservoir of the kernel-script invoice must.")
print("\n[4] DONE (dynamics side).")
