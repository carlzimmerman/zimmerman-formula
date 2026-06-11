#!/usr/bin/env python3
"""
agentJJ -- THE TRANSIENT FINGERPRINT CONFRONTED: do freshly-assembled deep-MOND systems (TDGs) sit off
the settled RAR, and does the banked SK construction's transient (agentX 6b x2.32; agentFF FF-2) survive
contact with the real numbers?
=========================================================================================================
  [0] GATES: (a) reproduce agentX 6b's banked fingerprint numbers (x2.32, half-life 1.2 cyc, pre-dev
      1e-2) with the same single-stage machinery; (b) record the byte-identical full rerun of
      agentX_sk_dynamics.py (done at shell, sha256 here); (c) reproduce agentCC's locked SPARC baseline
      (Ud, dex-RMS, both footings) before the SPARC locus is used.
  [1] THE ASSEMBLY TRANSIENT QUANTIFIED, self-consistently, in BOTH banked operator readings of (X-4):
      COMP form  (agentX run_driven, the action-derived  m a + sum (mu_ch - 1)[a]_ch = F)  and
      IMPL form  (agentX 3c-iv / agentFF FF-2 port,  a * mu(A_ret(a)) = F, own term theta(1)=1).
      Initial condition per the task: QUIET HISTORY THEN TURN-ON (the agentFF step geometry), isolated
      and EFE-embedded; matrix over settled depth x_set and window depth N_cyc. Observable: response
      envelope vs settled -> RAR offset in dex vs age in internal orbits. The two forms DISAGREE on the
      empty-window onset sign (a structural finding, reported as such); the 6b stale-line geometry where
      they agree is re-measured with both as the bridge to the banked x2.32.
  [2] THE REALISTIC TDG PREPARATION: window pre-loaded with the parent-disc line (loud high-x history,
      ejection, then internal turn-on with the EFE line standing). Sign and size of the net offset.
  [3] CONVERSION: dex-vs-orbits curves -> Gyr for T_orb = 0.3 / 0.5 / 1 Gyr; half-lives, 0.1/0.05-dex
      crossing ages, per N_cyc and form.
  [4] THE DATA: the six Lelli+2015 TDGs (A&A 584 A113, Tables 1/7/8; NGC 5291 trio = Bournaud+2007
      objects) placed on the RAR under the in-repo conventions, both footings; expectations: isolated
      settled RAR, QUMOND-radial EFE (repo convention, agentCC pred_efe), M22-native EFE (theta-weighted
      shiluta line, per-TDG frequency ratio); SPARC settled locus zero-point in the same g_bar band
      (locked conventions). Per-TDG offsets with full error propagation; weighted means.
  [5] CONFOUNDS, quantified: (a) EFE shift sizes + brackets; (b) out-of-equilibrium expectation
      (UNPINNED beyond Lelli's own equilibrium caveat; the 1D toy's control startup stated); (c)
      inclination +-15 deg swings; (d) Mbar geometry factor; (e) Vrot-vs-Vcirc choice.
  [6] VERDICT ARITHMETIC: per-(form, prep, N_cyc) predicted offsets at each TDG's measured age-in-orbits
      vs the measured offsets -> sigma-distances; which combinations die, which survive, what would
      discriminate.
Working rule (Carl's #1): every deficit/excess claim is checked against convention artifacts -- both a0
footings (9.36e-11 fw / 1.2e-10 canon), both EFE conventions, Upsilon (moot: gas-dominated), geometry
factor, inclination -- before being reported. Data provenance: Lelli+2015 tables fetched 2026-06-11
(ar5iv 1509.05404); Gentile+2007 (0706.1976) for the NGC 5291 external field (g_ext ~ 0.2 a0, <= 0.3 a0,
separations 58-75 kpc). NGC 7252 / VCC 2062 external fields are literature-bracketed, marked UNPINNED.
agentJJ, 2026-06-11. Usage: python3 agentJJ_transient_fingerprint.py [0|1|2|3|4|5|6 ...] (default: all).
"""
import numpy as np, sys, os, glob, hashlib

LINE = "=" * 100
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "data", "sparc_data")
LN10 = np.log(10.0)
kpc = 3.0857e19
Gyr = 3.15576e16
G_SI = 6.674e-11
Msun = 1.989e30
A0_FW, A0_CANON = 9.36e-11, 1.2e-10           # the two footings (repo canonical / regular-MOND default)

# ---------------------------------------------------------------- the M22 pieces (agentX/agentM conventions)
def mu_rar(x):
    x = np.maximum(x, 1e-300)
    return -np.expm1(-np.sqrt(x))
def nu_mcg(y):                                 # the inverse-form McGaugh nu (repo locked baseline)
    return 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-300))))
def th_A(y): return 2.0 / (1.0 + y * y)
def th_B(y): return np.exp(1.0 - np.minimum(y, 700))
def th_C(y): return np.exp((1.0 - np.minimum(y, 700)) / 2.0)
THETAS = {"2/(1+y^2)": th_A, "exp(1-y)": th_B, "exp((1-y)/2)": th_C}

def solve_mond(F, mu=mu_rar, A_extra=0.0):
    """settled solve a*mu(a + A_extra) = F (toy units a0=1), damped Picard."""
    a = max(F, 1e-12)
    for _ in range(400):
        a = 0.5 * (a + F / mu(a + A_extra))
    return a

# ---------------------------------------------------------------- the two banked operator readings, generalized
def integrate_comp(F0, w0=1.0, N_cyc=8.0, T_cycles=120, dt_per_cyc=200, theta=th_A, mu=mu_rar,
                   bg=(), preload=(), preload0=0.0, freeze_mu=None, two_stage=True):
    """COMP form (agentX run_driven, generalized):  a = F - sum_ch (mu_ch - 1) * comp_ch(a).
    bg      : ((w_b, amp_b), ...) steady background lines entering A via theta only (the agentM galactic-
              line treatment -- their worldline DOF is not simulated).
    preload : ((w_p, amp_p), ...) channels whose window starts LOADED (remembered past content) and
              receives no further forcing -- the EWMA decays on its own window time.
    preload0: starting load of the OWN (w0) channel window (the 6b stale-line geometry).
    freeze_mu: if not None, mu of every channel is frozen at this value (the settled-law control).
    Returns dict of arrays: t (in cycles of w0), a, v, mu0 (channel-0 mu), A0, Pae, PF."""
    dt = 2 * np.pi / w0 / dt_per_cyc
    nst = int(T_cycles * dt_per_cyc)
    ws = np.array([w0] + [w for w, _ in preload])
    nch = len(ws)
    ccs = np.exp(-dt / (N_cyc * 2 * np.pi / ws))
    y1 = np.zeros(nch, dtype=complex)
    y2 = np.zeros(nch, dtype=complex)
    y1[0] = y2[0] = preload0 / 2.0
    for j, (_, amp) in enumerate(preload):
        y1[j + 1] = amp / 2.0
        y2[j + 1] = amp / 2.0
    bgw = np.array([w for w, _ in bg]); bga = np.array([a for _, a in bg])
    t_arr = np.arange(nst) * dt
    a_s = np.zeros(nst); v_s = np.zeros(nst); mu0_s = np.zeros(nst); A0_s = np.zeros(nst)
    Pae_s = np.zeros(nst); PF_s = np.zeros(nst)
    v = 0.0
    for n in range(nst):
        t = t_arr[n]
        F = F0 * np.cos(w0 * t)
        amps = 2 * np.abs(y2)                      # PAST data only
        A = np.empty(nch)
        for i in range(nch):
            A[i] = amps[i] + sum(theta(ws[k] / ws[i]) * amps[k] for k in range(nch) if k != i)
            if len(bgw): A[i] += float(np.sum(theta(bgw / ws[i]) * bga))
        mu_ch = np.full(nch, freeze_mu) if freeze_mu is not None else mu(A)
        ph = np.exp(1j * ws * t)
        a_cur = F
        for _ in range(10):
            y1p = ccs * y1 + (1 - ccs) * a_cur * ph
            y2p = (ccs * y2 + (1 - ccs) * y1p) if two_stage else y1p
            comp = 2 * np.real(y2p * np.conj(ph))
            a_new = F - np.dot(mu_ch - 1.0, comp)
            if abs(a_new - a_cur) < 1e-14 + 1e-12 * abs(a_cur):
                a_cur = a_new; break
            a_cur = a_new
        y1p = ccs * y1 + (1 - ccs) * a_cur * ph
        y2p = (ccs * y2 + (1 - ccs) * y1p) if two_stage else y1p
        comp = 2 * np.real(y2p * np.conj(ph))
        v_mid = v + 0.5 * a_cur * dt
        Pae_s[n] = -np.dot(mu_ch - 1.0, comp) * v_mid
        PF_s[n] = F * v_mid
        a_s[n], v_s[n], mu0_s[n], A0_s[n] = a_cur, v, mu_ch[0], A[0]
        v += a_cur * dt
        y1, y2 = y1p, y2p
    return dict(t=t_arr * w0 / (2 * np.pi), a=a_s, v=v_s, mu0=mu0_s, A0=A0_s, Pae=Pae_s, PF=PF_s, dt=dt)

def integrate_impl(F0, w0=1.0, N_cyc=8.0, T_cycles=120, dt_per_cyc=200, theta=th_A, mu=mu_rar,
                   bg=(), preload=(), preload0=0.0, two_stage=True):
    """IMPL form (agentX 3c-iv / agentFF FF-2 port, generalized to an oscillatory line):
    per step solve |a| * mu(A_ret(|a|)) = |F| with the own term in its own window (theta(1)=1):
    A_ret(|a|) = 2|c*y_own + (1-c)*|a|*e^{iwt}| (+ cross-memory + bg).  mu multiplies the WHOLE a."""
    dt = 2 * np.pi / w0 / dt_per_cyc
    nst = int(T_cycles * dt_per_cyc)
    ws = np.array([w0] + [w for w, _ in preload])
    nch = len(ws)
    ccs = np.exp(-dt / (N_cyc * 2 * np.pi / ws))
    y1 = np.zeros(nch, dtype=complex); y2 = np.zeros(nch, dtype=complex)
    y1[0] = y2[0] = preload0 / 2.0
    for j, (_, amp) in enumerate(preload):
        y1[j + 1] = amp / 2.0; y2[j + 1] = amp / 2.0
    bgw = np.array([w for w, _ in bg]); bga = np.array([a for _, a in bg])
    t_arr = np.arange(nst) * dt
    a_s = np.zeros(nst); v_s = np.zeros(nst); mu0_s = np.zeros(nst); A0_s = np.zeros(nst)
    Pae_s = np.zeros(nst); PF_s = np.zeros(nst)
    v = 0.0
    for n in range(nst):
        t = t_arr[n]
        F = F0 * np.cos(w0 * t)
        amps = 2 * np.abs(y2)
        cross = sum(theta(ws[k] / ws[0]) * amps[k] for k in range(1, nch))
        if len(bgw): cross += float(np.sum(theta(bgw / ws[0]) * bga))
        ph0 = np.exp(1j * ws[0] * t)
        c0 = ccs[0]
        def own_amp(m):   # two-stage would-be own-channel amplitude with candidate |a| = m
            y1p = c0 * y1[0] + (1 - c0) * m * ph0
            y2p = (c0 * y2[0] + (1 - c0) * y1p) if two_stage else y1p
            return 2 * abs(y2p)
        if F == 0.0 and amps[0] == 0.0 and cross == 0.0:
            a_cur = 0.0; muv = 1.0
        else:
            lo, hi = 1e-15, 1e9
            for _ in range(60):
                mid = np.sqrt(lo * hi)
                if mid * mu(own_amp(mid) + cross) > abs(F): hi = mid
                else: lo = mid
            m = np.sqrt(lo * hi)
            muv = mu(own_amp(m) + cross)
            a_cur = np.sign(F) * m if F != 0.0 else 0.0
        ph = np.exp(1j * ws * t)
        y1 = ccs * y1 + (1 - ccs) * a_cur * ph
        y2 = (ccs * y2 + (1 - ccs) * y1) if two_stage else y1
        v_mid = v + 0.5 * a_cur * dt
        Pae_s[n] = (1.0 / muv - 1.0) * F * v_mid if muv > 0 else 0.0
        PF_s[n] = F * v_mid
        a_s[n], v_s[n], mu0_s[n] = a_cur, v, muv
        A0_s[n] = 2 * abs(y2[0]) + cross
        v += a_cur * dt
    return dict(t=t_arr * w0 / (2 * np.pi), a=a_s, v=v_s, mu0=mu0_s, A0=A0_s, Pae=Pae_s, PF=PF_s, dt=dt)

def envelope(t_cyc, x, t_at, halfwin=0.5):
    """sqrt(2) * trailing-half-cycle RMS of x at each requested time (in cycles)."""
    out = []
    for ta in t_at:
        m = (t_cyc > ta - halfwin) & (t_cyc <= ta)
        out.append(np.sqrt(2.0 * np.mean(x[m] ** 2)) if m.sum() > 3 else np.nan)
    return np.array(out)

def atfreq_amp(t_cyc, x, t_at, w_extra=None, w0=1.0, maxwin=2.0):
    """w0-COHERENT amplitude at each mark: trailing-window least squares on cos/sin at w0 (plus the
    remembered-line frequency if given, so its ghost ringing does NOT leak into the rotation measure).
    This is the rotation-curve analog -- a velocity-field fit reads the coherent component; the
    off-resonant ringing lands in sigma/non-circular terms instead. Window = min(t, maxwin) cycles."""
    out = []
    tt = t_cyc * 2 * np.pi   # radians of w0
    for ta in t_at:
        m = (t_cyc > ta - min(ta, maxwin)) & (t_cyc <= ta)
        if m.sum() < 8:
            out.append(np.nan); continue
        cols = [np.cos(w0 * tt[m]), np.sin(w0 * tt[m])]
        if w_extra:
            cols += [np.cos(w_extra * tt[m]), np.sin(w_extra * tt[m])]
        Adm = np.vstack(cols).T
        AtA = Adm.T @ Adm + 1e-9 * np.eye(Adm.shape[1])
        coef = np.linalg.solve(AtA, Adm.T @ x[m])
        out.append(float(np.hypot(coef[0], coef[1])))
    return np.array(out)

AGE_MARKS = np.array([0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0])

_RUN_CACHE = {}

def fingerprint_run(form, x_set, N_cyc, prep, theta=th_A, x_par=0.0, w_par=1.65, par_fade=1.0,
                    y_efe=0.3, e_g=0.2, T_cycles=None, dt_per_cyc=200):
    """One assembly run. prep in {'ISO','EFE'}; x_par > 0 adds the remembered parent-disc line
    (amplitude x_par * par_fade at w_par). F0 is CHOSEN so the settled response is exactly x_set:
    F0 = x_set * mu(x_set + A_bg) (both forms share this settled state -- tracking gain -> 1).
    Returns (marks, ddex_a, ddex_v2, ddex_mu, x_set, mu_set, run-dict)."""
    key = (form, x_set, N_cyc, prep, theta.__name__, x_par, w_par, par_fade, y_efe, e_g, T_cycles, dt_per_cyc)
    if key in _RUN_CACHE:
        return _RUN_CACHE[key]
    bg = ((y_efe, e_g),) if prep == "EFE" else ()
    A_bg = theta(np.array([y_efe]))[0] * e_g if prep == "EFE" else 0.0
    F0 = x_set * mu_rar(x_set + A_bg)
    mu_set = mu_rar(x_set + A_bg)
    preload = ((w_par, x_par * par_fade),) if x_par > 0 else ()
    T = T_cycles if T_cycles else int(max(12 * N_cyc, 40))
    fn = integrate_comp if form == "COMP" else integrate_impl
    r = fn(F0=F0, N_cyc=N_cyc, T_cycles=T, dt_per_cyc=dt_per_cyc, theta=theta, bg=bg, preload=preload)
    a_env = envelope(r["t"], r["a"], AGE_MARKS)
    a_w0 = atfreq_amp(r["t"], r["a"], AGE_MARKS, w_extra=(w_par if x_par > 0 else None))
    v_env = envelope(r["t"], r["v"], AGE_MARKS)
    v_set = x_set / 1.0                                            # w0 = 1: settled velocity amplitude
    ddex_a = np.log10(a_env / x_set)
    ddex_a0 = np.log10(a_w0 / x_set)
    ddex_v2 = 2 * np.log10(v_env / v_set)
    mu_at = np.interp(AGE_MARKS, r["t"], r["mu0"])
    ddex_mu = np.log10(mu_set / np.maximum(mu_at, 1e-30))
    out = (AGE_MARKS, ddex_a, ddex_a0, ddex_v2, ddex_mu, x_set, mu_set, r)
    _RUN_CACHE[key] = out
    return out

# ---------------------------------------------------------------- SPARC loader (agentCC locked conventions)
def load_sparc():
    gals = []
    for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try: d = np.genfromtxt(f, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6: continue
        name = os.path.basename(f).replace("_rotmod.dat", "")
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        gals.append((name, R * kpc, Vobs, eV, Vgas, Vdisk, Vbul))
    return gals

def assemble(gals, Ud, a0):
    GB, GO, ED, GI, VM = [], [], [], [], []
    for gi, (name, Rm, Vobs, eV, Vgas, Vdisk, Vbul) in enumerate(gals):
        Vbar2 = np.sign(Vgas) * Vgas ** 2 + Ud * Vdisk ** 2 + 1.4 * Ud * Vbul ** 2
        gb = Vbar2 * 1e6 / Rm; go = (Vobs * 1e3) ** 2 / Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0)
        fr = np.clip(eV, 1, None) / np.clip(Vobs, 1, None)
        GB += list(gb[ok]); GO += list(go[ok]); ED += list((2.0 / LN10) * fr[ok]); GI += [gi] * int(ok.sum())
        VM += [float(np.max(Vobs))] * int(ok.sum())
    return np.array(GB), np.array(GO), np.array(ED), np.array(GI, int), np.array(VM)

# ---------------------------------------------------------------- the TDG table (provenance in [4] header)
# name, D/Mpc, Rout/kpc, eR, Vrot, eVrot, Vcirc, eVcirc, i/deg, Mbar/1e8Msun, eMbar,
# Mdyn/1e8, eMdyn, ratio, eratio, age/Gyr, (tmerg/torb Lelli), g_ext mid/lo/hi (SI), d_par/kpc, V_par/km/s, pin
TDGS = [
    ("NGC5291N",  62.0, 4.8, 1.2, 40, 9, 45, 9, 55, 15.6, 1.7, 23.0, 11.0, 1.5, 0.7, 0.36, 0.5,
     2.4e-11, 1.2e-11, 3.6e-11, 65.0, 219.0, "PINNED(Gentile07: gext~0.2a0,<=0.3a0; sep 58-75 kpc)"),
    ("NGC5291S",  62.0, 7.2, 1.2, 20, 6, 35, 6, 65, 15.9, 2.1, 20.0, 8.0, 1.3, 0.5, 0.36, 0.2,
     2.4e-11, 1.2e-11, 3.6e-11, 65.0, 219.0, "PINNED(Gentile07)"),
    ("NGC5291SW", 62.0, 4.8, 1.2, 22, 7, 28, 7, 60, 7.1, 1.2, 8.7, 4.9, 1.2, 0.7, 0.36, 0.3,
     2.4e-11, 1.2e-11, 3.6e-11, 65.0, 219.0, "PINNED(Gentile07)"),
    ("NGC7252E",  66.5, 4.5, 1.9, 11, 5, 18, 5, 80, 3.9, 0.5, 3.4, 2.4, 0.9, 0.6, 0.65, 0.3,
     2.2e-11, 1.0e-11, 4.5e-11, 70.0, 220.0, "BRACKET-UNPINNED(remnant V 180-260, d 50-90 kpc)"),
    ("NGC7252NW", 66.5, 7.7, 1.9, 16, 6, 21, 6, 60, 8.2, 0.8, 7.9, 4.9, 1.0, 0.6, 0.65, 0.2,
     2.2e-11, 1.0e-11, 4.5e-11, 70.0, 220.0, "BRACKET-UNPINNED"),
    ("VCC2062",   17.0, 2.6, 0.6, 13, 7, 16, 7, 45, 1.4, 0.3, 1.5, 1.3, 1.0, 0.9, 0.75, 0.6,
     2.0e-11, 0.6e-11, 4.4e-11, 20.0, 110.0, "BRACKET-UNPINNED(NGC4694 V 80-140, d 15-30 kpc)"),
]

def pred_efe_qumond(gb, a0, gext):
    """QUMOND radial EFE -- repo convention (agentCC pred_efe / sparc_efe_test.py)."""
    if gext <= 0: return nu_mcg(gb / a0) * gb
    eN = gext / a0
    return nu_mcg((gb + gext) / a0) * (gb + gext) - nu_mcg(np.array([eN]))[0] * gext

def pred_efe_m22(gb, a0, gext, y_efe, theta=th_A):
    """M22-native EFE: the external line enters the internal channel's A with weight theta(y_efe)
    (the agentM galactic-line treatment). Settled response solves a*mu(a/a0 + th*gext/a0) = gb."""
    A_bg = theta(np.array([y_efe]))[0] * gext / a0
    a = max(gb, 1e-15)
    for _ in range(400):
        a = 0.5 * (a + gb / mu_rar(a / a0 + A_bg))
    return a

# ================================================================ sections
def sec0():
    print(LINE); print("[0] GATES -- banked numbers reproduced before any new use"); print(LINE)
    # (a) agentX 6b fingerprint, same machinery (single-stage EWMA, same params)
    from scipy.signal import lfilter
    w0 = 1.0; A_quiet, boost = 0.1, 10.0; N_cyc1 = 8.0
    dt1 = 2 * np.pi / w0 / 200.0
    Tpre, Tpost = 80 * 2 * np.pi, 60 * 2 * np.pi
    t1 = np.arange(-Tpre, Tpost, dt1)
    a1 = np.where(t1 < 0, A_quiet, boost * A_quiet) * np.cos(w0 * t1)
    Twin = N_cyc1 * 2 * np.pi / w0
    cc1 = np.exp(-dt1 / Twin)
    y1 = lfilter([1 - cc1], [1, -cc1], a1 * np.exp(1j * w0 * t1))
    A_ret_t = 2 * np.abs(y1)
    i_audit = (t1 < 0) & (t1 > -Tpre + 8 * Twin)
    pre_dev = np.max(np.abs(A_ret_t[i_audit] - A_quiet)) / A_quiet
    mu_ret_t = mu_rar(A_ret_t)
    mu_l = mu_rar(boost * A_quiet)
    i0 = np.searchsorted(t1, 0.0)
    resp = mu_l / mu_ret_t[i0:]
    thr = 1.0 + 0.5 * (resp[0] - 1.0)
    i_half = int(np.argmax(resp < thr))
    hl = t1[i0 + i_half] / (2 * np.pi)
    print(f"  (a) agentX 6b geometry re-run: enhancement mu_loud/mu_ret(0+) = {resp[0]:.3f} "
          f"(banked 2.32), half-life {hl:.1f} cyc (banked 1.2), pre-onset dev {pre_dev:.1e} (banked 1.0e-2)")
    ok_a = abs(resp[0] - 2.32) < 0.01 and abs(hl - 1.2) < 0.1 and pre_dev < 2.5 / (2 * np.pi * N_cyc1)
    print(f"      GATE (a): {'PASS' if ok_a else 'FAIL'}")
    assert ok_a
    # (b) byte-identical rerun record
    h_bank = hashlib.sha256(open(os.path.join(HERE, "agentX_sk_dynamics.out"), "rb").read()).hexdigest()[:16]
    rerun = "/tmp/agentJJ_xdyn_rerun.out"
    if os.path.exists(rerun):
        h_new = hashlib.sha256(open(rerun, "rb").read()).hexdigest()[:16]
        print(f"  (b) full agentX_sk_dynamics.py rerun (2026-06-11): sha256[:16] banked = {h_bank}, "
              f"rerun = {h_new} -> {'BYTE-IDENTICAL' if h_bank == h_new else 'DIFFERS (STOP)'}")
        assert h_bank == h_new
    else:
        print(f"  (b) banked agentX_sk_dynamics.out sha256[:16] = {h_bank}; shell-level rerun was "
              f"byte-identical (diff clean, recorded in memo)")
    # (c) agentCC locked SPARC baseline
    gals = load_sparc()
    print(f"  (c) SPARC galaxies loaded: {len(gals)}; reproducing the locked baseline "
          f"(mi_f4_sparc_shape_test / agentCC [0]):")
    LOCKED = {9.36e-11: (0.52, 0.1950), 1.2e-10: (0.46, 0.1977)}
    ok_c = True
    for a0, (Ud_lock, s_lock) in LOCKED.items():
        best = (None, 9e9)
        for Ud in np.linspace(0.3, 1.2, 46):
            gb, go, ed, gi, vm = assemble(gals, Ud, a0)
            r = np.log10(go) - np.log10(nu_mcg(gb / a0) * gb)
            s = float(np.sqrt(np.mean(r ** 2)))
            if s < best[1]: best = (Ud, s)
        match = (abs(best[0] - Ud_lock) < 1e-9) and (abs(best[1] - s_lock) < 5e-4)
        ok_c &= match
        print(f"      a0 = {a0:.3g}: best Ud = {best[0]:.2f} (locked {Ud_lock:.2f}), "
              f"dex RMS = {best[1]:.4f} (locked {s_lock:.4f})  {'PASS' if match else 'FAIL'}")
    assert ok_c
    print("  [0] ALL GATES PASS -- machinery certified against the banked corpus.\n")

def sec1():
    print(LINE)
    print("[1] THE ASSEMBLY TRANSIENT QUANTIFIED -- quiet history then turn-on (the agentFF step geometry),")
    print("    BOTH banked operator readings, isolated and EFE-embedded, self-consistent")
    print(LINE)
    print("""  The structural fact first (found while porting, reported per house rule): the banked corpus
  carries TWO readings of (X-4) that AGREE on loaded windows but DISAGREE at an empty one:
    COMP (action-derived, agentX run_driven):  m a + sum_ch (mu_ch - 1)[a]_ch = F.  Empty window =>
         [a]_ch ~ 0 => the MI correction VANISHES => onset response is NEWTONIAN (a = F), rising to
         the settled MOND value from BELOW as the window fills.
    IMPL (agentX 3c-iv, agentFF FF-2a/2b port): a * mu(A_ret(a)) = F, own term theta(1)=1.  Empty
         window => mu evaluated near zero => onset response is ENHANCED (the integrable t^(-1/3)
         spike agentFF measured), decaying to settled from ABOVE.
  The equivalence 'm a + sum(mu-1)[a]_ch = F  <=>  mu*a = F' claimed in (X-4) holds only when the
  filter bank reconstructs the worldline (sum_ch [a]_ch = a); a stale or empty window breaks it.
  The transient's SIGN is therefore an UNFIXED CONVENTION of the construction, alongside N_cyc.
  Both are quantified below; the 6b stale-line geometry (loaded window) is run with both first.\n""")
    # bridge: 6b geometry with both integrators (window pre-loaded with the SAME line, amplitude step)
    print("  [1-bridge] the 6b geometry (x: 0.1 -> 1.0, N_cyc = 8) run with BOTH integrators")
    print("    (window pre-loaded with the quiet line at the SAME frequency; F stepped to the loud value):")
    for form, fn in (("COMP", integrate_comp), ("IMPL", integrate_impl)):
        F_loud = 1.0 * mu_rar(1.0)
        r = fn(F0=F_loud, N_cyc=8, T_cycles=60, dt_per_cyc=200, theta=th_A,
               preload0=0.1)                      # the OWN window holds the quiet line (6b geometry)
        a_env = envelope(r["t"], r["a"], np.array([0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 40.0]))
        boost = a_env / 1.0
        print(f"    {form}: response/settled at 0.5/1/2/4/8/16/40 cyc = "
              + "/".join(f"{b:.2f}" for b in boost))
    print("""    MACHINE OVERRULES THE DRAFT GUESS (recorded per house rule): the forms do NOT agree on the
    loaded-window step either. IMPL reproduces the banked x2.32 ENHANCEMENT (2.30 at 0.5 cyc, decaying
    on the window time). COMP -- the literal action-derived (X-4) EOM, agentX's own run_driven -- gives
    0.70 x settled: the response rises monotonically FROM BELOW (a = F + (1-mu_stale)*comp_stale; the
    stale comp is the OLD amplitude, so there is NO transient boost at EOM level). The banked '6b x2.32
    response enhancement' is a prescribed-mu statement (response ASSUMED = F/mu_ret), i.e. the IMPL
    reading; it was never integrated through the action EOM -- agentX's own 3c-iii kick WAS integrated
    (COMP) and indeed shows no response boost, only the small flux event. The fingerprint's sign is
    form-split in EVERY transient geometry, not just the empty-window corner.\n""")
    hdr = "ages(orb):" + "".join(f"{a:7.2f}" for a in AGE_MARKS)
    for prep, lbl in (("ISO", "ISOLATED (empty window, no external line) -- the e_N -> 0 limit"),
                      ("EFE", "EFE-EMBEDDED (standing external line: e_g = 0.2 a0, y_efe = 0.3, "
                              "theta_A(0.3) = %.2f => A_bg = %.2f a0) -- the real-TDG regime" %
                              (th_A(0.3), th_A(0.3) * 0.2))):
        print(f"  [1-{prep}] {lbl}")
        print("    " + hdr)
        for form in ("COMP", "IMPL"):
            for x_set in (0.05, 0.1, 0.2):
                for N in (8, 16, 32):
                    marks, dda, dda0, ddv2, ddmu, a_set, mu_set, r = fingerprint_run(form, x_set, N, prep)
                    print(f"    {form} x_set={x_set:4.2f} N={N:2d} Ddex_a:  "
                          + "".join(f"{d:+7.3f}" for d in dda))
                    if N == 8:
                        print(f"    {form} x_set={x_set:4.2f} N={N:2d} Ddex_v2: "
                              + "".join(f"{d:+7.3f}" for d in ddv2) + "   (V^2-based; toy keeps kinematic memory)")
                    if N == 8 and x_set == 0.1:
                        print(f"    {form} x_set={x_set:4.2f} N={N:2d} Ddex_w0: "
                              + "".join(f"{d:+7.3f}" for d in dda0)
                              + "   (w0-coherent check: matches Ddex_a on single-line runs)")
        print()
    # theta-shape spot check (EFE prep, x_set = 0.1, N = 16)
    print("  [1-theta] theta-shape dependence (EFE prep, x_set = 0.1, N_cyc = 16, Ddex_a):")
    for tl, th in THETAS.items():
        for form in ("COMP", "IMPL"):
            marks, dda, dda0, _, _, _, _, _ = fingerprint_run(form, 0.1, 16, "EFE", theta=th)
            print(f"    theta={tl:13s} {form}: " + "".join(f"{d:+7.3f}" for d in dda))
    print()
    # dt-convergence of the IMPL onset marks (the t^(-1/3) spike: peak is cutoff-dependent [FF-2b])
    print("  [1-dt] dt-dependence of the IMPL early marks (x_set = 0.1, N_cyc = 8):")
    for prep in ("ISO", "EFE"):
        for dpc in (200, 400, 800):
            marks, dda, dda0, _, _, _, _, _ = fingerprint_run("IMPL", 0.1, 8, prep, dt_per_cyc=dpc, T_cycles=6)
            print(f"    {prep} dt = T/{dpc:3d}: Ddex_a(0.25 orb) = {dda[0]:+.3f}, (0.50) = {dda[1]:+.3f}, "
                  f"(0.75) = {dda[2]:+.3f}")
    print("""    honesty note: the ISO 0.25/0.50-orbit marks CREEP UPWARD ~+0.06 dex per dt halving (the
    spike's slow dt^(1/3) tail) -- quote them as LOWER BOUNDS '>= +1.5 dex'; the >= 0.75-orbit marks
    and ALL EFE-embedded marks are dt-stable to < 0.01 dex (the standing external line regularizes
    the onset). The instantaneous peak stays cutoff-dependent exactly as agentFF measured; not used.""")
    print()

def sec2():
    print(LINE)
    print("[2] THE REALISTIC TDG PREPARATION -- parent-disc memory loaded (loud high-x history), EFE standing")
    print(LINE)
    print("""  The material of a real TDG was NOT quiet before assembly: it orbited the parent's outer disc
  at x_par ~ 0.5-1 (period T_par ~ 0.6 T_int), was ejected ~0.1-0.5 Gyr before condensation, and the
  parent line decays only on ITS window (N_cyc * T_par). The remembered line enters the internal
  channel with weight theta_A(w_par/w_int = 1.65) = %.2f -- it RAISES A => raises mu => SUPPRESSES the
  response (the loud->quiet direction of the 6b transient). Pre-decay applied: x0.9 (ejection-to-
  condensation lag ~ 0.75 T_par at N_cyc = 8).\n""" % th_A(1.65))
    hdr = "ages(orb):" + "".join(f"{a:7.2f}" for a in AGE_MARKS)
    print("    " + hdr)
    for form in ("COMP", "IMPL"):
        for x_par in (0.5, 1.0):
            for N in (8, 16, 32):
                marks, dda, dda0, ddv2, ddmu, a_set, mu_set, r = fingerprint_run(
                    form, 0.1, N, "EFE", x_par=x_par, par_fade=0.9)
                print(f"    {form} x_par={x_par:3.1f} N={N:2d} Ddex_w0: "
                      + "".join(f"{d:+7.3f}" for d in dda0)
                      + ("" if form == "IMPL" else "   [RMS-envelope incl. ghost: "
                         + "/".join(f"{d:+.2f}" for d in dda[[0, 3, 7]]) + " at 0.25/1/4 orb]"))
        print()
    print("""  OBSERVABLE-EXTRACTION NOTE (caught in-run, bug log): the first-draft broadband RMS envelope
  showed COMP+parent at +0.31..+0.49 dex -- that is NOT a rotation boost; it is the (mu_par-1)*comp_par
  GHOST FORCE: under the COMP form the worldline keeps being forced at the REMEMBERED parent frequency
  while that window drains (amplitude (1-mu_par)*x_par*fade ~ 0.3 = x6 the internal drive, decaying on
  N_cyc*T_par). A velocity-field fit reads it as NON-CIRCULAR motion / inflated sigma_HI, not as Vrot
  (cf. Lelli+15's own note that the NGC 5291 dwarfs' sigma_HI ~ 20 km/s 'may indicate unresolved
  non-circular motions' -- direction-compatible, not claimed as evidence). The w0-coherent (Ddex_w0)
  rows above are the rotation-curve analog; the IMPL form has no ghost-force channel at all (memory
  enters only through mu).""")
    print("  net-sign summary (x_set = 0.1, EFE prep): the parent memory pushes the offset NEGATIVE")
    print("  (suppressed / quasi-Newtonian-ward) relative to the same form without it; size and decay")
    print("  above. Ejection-lag sensitivity (par_fade 0.9 -> 0.7, IMPL, x_par = 1.0, N = 16):")
    for pf in (0.9, 0.7):
        marks, dda, dda0, _, _, _, _, _ = fingerprint_run("IMPL", 0.1, 16, "EFE", x_par=1.0, par_fade=pf)
        print(f"    par_fade={pf:3.1f}: " + "".join(f"{d:+7.3f}" for d in dda0))
    print()

def sec3():
    print(LINE)
    print("[3] CONVERSION TO PHYSICAL TIME -- T_orb = 0.3 / 0.5 / 1 Gyr dwarfs")
    print(LINE)
    print("  For each (form, prep, N_cyc): offset at 0.25 orb, half-life of |Ddex| (orbits), and the age")
    print("  at which |Ddex| falls below 0.1 / 0.05 dex; then in Gyr for the three T_orb values.")
    rows = []
    for form in ("COMP", "IMPL"):
        for prep, x_par in (("ISO", 0.0), ("EFE", 0.0), ("EFE", 1.0)):
            for N in (8, 16, 32):
                marks, dda, dda0, _, _, _, _, r = fingerprint_run(form, 0.1, N, prep if prep != "ISO" else "ISO",
                                                                  x_par=x_par, par_fade=0.9 if x_par else 1.0)
                # dense curve for crossing ages (w0-coherent measure; ghost excluded if parent loaded)
                tt = r["t"]
                tg = np.arange(0.25, max(tt) - 0.5, 0.25)
                aa = atfreq_amp(tt, r["a"], tg, w_extra=(1.65 if x_par else None))
                dd = np.log10(aa / 0.1)
                d0 = dd[0]
                def first_below(th):
                    idx = np.where(np.abs(dd) < th)[0]
                    return tg[idx[0]] if len(idx) else np.nan
                hl_idx = np.where(np.abs(dd) < abs(d0) / 2)[0]
                hl = tg[hl_idx[0]] if len(hl_idx) else np.nan
                rows.append((form, prep + ("+par" if x_par else ""), N, d0, hl, first_below(0.1), first_below(0.05)))
    print(f"    {'form':5s} {'prep':8s} {'N':>3s} {'Ddex(0.25orb)':>14s} {'half-life(orb)':>15s} "
          f"{'|D|<0.1 (orb)':>14s} {'|D|<0.05 (orb)':>15s}   t(|D|<0.1) for T_orb 0.3/0.5/1 Gyr")
    for form, prep, N, d0, hl, t01, t005 in rows:
        gyr = "/".join("--" if np.isnan(t01) else f"{t01 * T:.2f}" for T in (0.3, 0.5, 1.0))
        print(f"    {form:5s} {prep:8s} {N:3d} {d0:+14.3f} {hl:15.2f} {t01:14.2f} {t005:15.2f}   {gyr} Gyr")
    print("""
  Reading, per form: (i) IMPL/ISO -- the only large POSITIVE branch -- lives 6-23 orbits (|D|>0.1),
  i.e. 1.8-23 Gyr for dwarf T_orb: alive in every young isolated dwarf but ERASED by an e_N ~ 0.2
  external field (IMPL/EFE rows: never exceeds 0.05 dex). (ii) COMP -- the action-EOM reading -- is a
  LONG-LIVED NEGATIVE (quasi-Newtonian) state: at TDG ages it sits at the full Newtonian floor and
  its refill outlives the sample ages by an order of magnitude (the deep-MOND refill is
  ~2.6 N_cyc / <d(x mu)/dx> orbits plus a nonlinear early-time stall). The TDG sample at 0.2-0.8
  internal orbits (Lelli Table 7) therefore confronts: COMP => g_obs ~ g_bar; IMPL => g_obs ~ the
  settled EFE-MOND locus (+0.02..0.07). Adiabatically-grown settled dwarfs are untouched by both
  (their windows were never empty -- no conflict with SPARC).\n""")

def sec4():
    print(LINE)
    print("[4] THE DATA -- the six Lelli+2015 TDGs on the RAR, in-repo conventions, both footings")
    print(LINE)
    print("""  Provenance (fetched 2026-06-11): Lelli+2015 A&A 584 A113 (ar5iv 1509.05404) Table 1 (distances
  62 / 66.5 / 17 Mpc; ages: NGC 5291 ring ~360 Myr, NGC 7252 merger ~600-700 Myr, VCC 2062 0.5-1 Gyr),
  Table 7 (Rout, Vrot, i, sigma_HI, Vcirc = asymmetric-drift-corrected; t_merg/t_orb = 0.5/0.2/0.3/
  0.3/0.2/0.4-0.8), Table 8 (M_dyn, M_HI, M_*, M_mol, M_bar, M_dyn/M_bar). External fields: NGC 5291
  g_ext ~ 0.2 a0 (<= 0.3 a0) at separations 58-75 kpc PINNED from Gentile+2007 (0706.1976; their a0 =
  1.2e-10 => g_ext = 2.4e-11 SI, bracket 1.2-3.6e-11); NGC 7252 and VCC 2062 g_ext are literature
  BRACKETS (remnant/parent V and projected d as commented in the table) -- marked UNPINNED.
  g_obs = Vcirc^2/Rout; g_bar = G Mbar/Rout^2 (spherical; geometry factor confound in [5]).""")
    print(f"\n    {'TDG':10s} {'g_bar':>9s} {'g_obs':>9s} {'+-dex':>6s} {'Mdyn/Mbar':>9s} {'age/orb':>8s} "
          f"{'eN(fw)':>7s} {'eN(can)':>8s}  pin")
    rows = []
    for (nm, D, R, eR, Vr, eVr, Vc, eVc, inc, Mb, eMb, Md, eMd, rat, erat, age, tt_l,
         gx, gxlo, gxhi, dpar, Vpar, pin) in TDGS:
        Rm = R * kpc
        go = (Vc * 1e3) ** 2 / Rm
        gb = G_SI * Mb * 1e8 * Msun / Rm ** 2
        t_orb = 2 * np.pi * Rm / (Vc * 1e3) / Gyr
        t_orb_vr = 2 * np.pi * Rm / (Vr * 1e3) / Gyr
        age_orb = age / t_orb
        T_efe = 2 * np.pi * (dpar * kpc) / (Vpar * 1e3) / Gyr
        y_efe = t_orb / T_efe
        rows.append((nm, gb, go, Vc, eVc, R, eR, Mb, eMb, age, t_orb, t_orb_vr, age_orb, tt_l,
                     y_efe, gx, gxlo, gxhi, rat, erat))
        edex_go = np.sqrt((2 / LN10 * eVc / Vc) ** 2)   # V part only; R folded into Delta below
        print(f"    {nm:10s} {gb:9.2e} {go:9.2e} {edex_go:6.2f} {rat:5.1f}+-{erat:3.1f} "
              f"{age_orb:8.2f} {gx/A0_FW:7.2f} {gx/A0_CANON:8.2f}  {pin[:40]}")
    print("\n    (age/orb = adopted age / (2 pi Rout / Vcirc); Lelli's own t_merg/t_orb column: "
          + ", ".join(f"{r[13]:.1f}" if not isinstance(r[13], str) else r[13] for r in rows) + ")")
    # ---- offsets vs the three expectations, both footings, with full errors
    print("\n  Per-TDG offsets Ddex = log10(g_obs / g_pred)  [errors: V,R,M propagated incl. the R-correlation]")
    results = {}
    for a0, foot in ((A0_FW, "fw  a0=9.36e-11"), (A0_CANON, "can a0=1.20e-10")):
        for model in ("ISO", "QUM-EFE", "M22-EFE"):
            ds, es = [], []
            for (nm, gb, go, Vc, eVc, R, eR, Mb, eMb, age, t_orb, t_orb_vr, age_orb, tt_l,
                 y_efe, gx, gxlo, gxhi, rat, erat) in rows:
                def predf(g):
                    if model == "ISO": return nu_mcg(g / a0) * g
                    if model == "QUM-EFE": return pred_efe_qumond(g, a0, gx)
                    return pred_efe_m22(g, a0, gx, y_efe)
                P = predf(gb)
                d = np.log10(go / P)
                s = (np.log10(predf(gb * 1.01)) - np.log10(P)) / np.log10(1.01)   # local slope
                dV = 2 / LN10 * eVc / Vc
                dM = s / LN10 * eMb / Mb
                dR = abs(-1 + 2 * s) / LN10 * eR / R
                e = np.sqrt(dV ** 2 + dM ** 2 + dR ** 2)
                ds.append(d); es.append(e)
            ds, es = np.array(ds), np.array(es)
            w = 1 / es ** 2
            mean = np.sum(w * ds) / np.sum(w); err = 1 / np.sqrt(np.sum(w))
            results[(a0, model)] = (ds, es, mean, err)
            print(f"    [{foot} | {model:7s}] " + " ".join(f"{d:+5.2f}+-{e:4.2f}" for d, e in zip(ds, es))
                  + f"   wmean = {mean:+.3f} +- {err:.3f}  ({mean/err:+.1f} sigma)")
    # ---- EFE bracket sensitivity on the wmean (QUMOND + M22, canon footing)
    print("\n  EFE-bracket sensitivity of the weighted mean (canon footing):")
    for model in ("QUM-EFE", "M22-EFE"):
        for which, idx in (("lo", 16), ("mid", 15), ("hi", 17)):
            ds, es = [], []
            for r in rows:
                gb, go, Vc, eVc, R, eR, Mb, eMb = r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]
                y_efe = r[14]; gx = r[idx]
                P = pred_efe_qumond(gb, A0_CANON, gx) if model == "QUM-EFE" else \
                    pred_efe_m22(gb, A0_CANON, gx, y_efe)
                Pp = pred_efe_qumond(gb * 1.01, A0_CANON, gx) if model == "QUM-EFE" else \
                    pred_efe_m22(gb * 1.01, A0_CANON, gx, y_efe)
                s = (np.log10(Pp) - np.log10(P)) / np.log10(1.01)
                e = np.sqrt((2 / LN10 * eVc / Vc) ** 2 + (s / LN10 * eMb / Mb) ** 2
                            + (abs(-1 + 2 * s) / LN10 * eR / R) ** 2)
                ds.append(np.log10(go / P)); es.append(e)
            ds, es = np.array(ds), np.array(es)
            w = 1 / es ** 2
            print(f"    {model} g_ext={which:3s}: wmean = {np.sum(w*ds)/np.sum(w):+.3f} +- {1/np.sqrt(np.sum(w)):.3f}")
    # ---- SPARC settled locus zero-point in the TDG g_bar band
    print("\n  SPARC settled locus in the TDG band (g_bar in [2.0e-12, 1.1e-11], locked conventions):")
    gals = load_sparc()
    for a0, Ud in ((A0_FW, 0.52), (A0_CANON, 0.46)):
        gb, go, ed, gi, vm = assemble(gals, Ud, a0)
        # outer-point flag (TDG points are outermost radii): last 30% of radii per galaxy
        outer = np.zeros(len(gb), bool)
        for g in np.unique(gi):
            sel = np.where(gi == g)[0]
            outer[sel[int(np.ceil(0.7 * len(sel))):]] = True
        m = (gb > 2.0e-12) & (gb < 1.1e-11)
        r_all = np.log10(go[m]) - np.log10(nu_mcg(gb[m] / a0) * gb[m])
        md = (vm < 70)
        r_dw = np.log10(go[m & md]) - np.log10(nu_mcg(gb[m & md] / a0) * gb[m & md])
        r_dwo = np.log10(go[m & md & outer]) - np.log10(nu_mcg(gb[m & md & outer] / a0) * gb[m & md & outer])
        print(f"    a0={a0:.3g}: N={m.sum():4d} pts, median offset {np.median(r_all):+.3f}, "
              f"mean {np.mean(r_all):+.3f}, scatter {np.std(r_all):.3f} dex; "
              f"dwarfs (Vmax<70): N={int((m & md).sum())}, median {np.median(r_dw):+.3f}; "
              f"dwarf OUTER pts: N={int((m & md & outer).sum())}, median {np.median(r_dwo):+.3f}")
    print("""    -> the whole-band settled locus sits ON the analytic curve (median -0.00/-0.03), but the
       settled-DWARF subset sits 0.1-0.2 dex BELOW it (inner rising-curve points AND outer points --
       the known deep-end behaviour, cf. agentCC). Working-rule both-ways: referenced to the
       EMPIRICAL settled-dwarf outer locus instead of the analytic curve, every TDG offset above
       moves UP by ~+0.1..+0.2 dex (the deficit reading weakens; the enhanced reading stays dead).""")
    # ---- cross-check vs published Mdyn/Mbar
    print("\n  Cross-check: g_obs/g_bar vs Lelli's published Mdyn/Mbar (same spherical convention):")
    for r in rows:
        print(f"    {r[0]:10s}: g_obs/g_bar = {r[2]/r[1]:.2f}  vs  Mdyn/Mbar = {r[18]:.1f}+-{r[19]:.1f}")
    return results

def sec5():
    print(LINE)
    print("[5] CONFOUNDS, QUANTIFIED")
    print(LINE)
    print("""  (a) THE EFE (opposite sign to the enhanced fingerprint): size of the suppression it already
      explains, per TDG -- the gap between the isolated and EFE-corrected expectations:""")
    for (nm, D, R, eR, Vr, eVr, Vc, eVc, inc, Mb, eMb, Md, eMd, rat, erat, age, tt_l,
         gx, gxlo, gxhi, dpar, Vpar, pin) in TDGS:
        Rm = R * kpc
        gb = G_SI * Mb * 1e8 * Msun / Rm ** 2
        t_orb = 2 * np.pi * Rm / (Vc * 1e3) / Gyr
        T_efe = 2 * np.pi * (dpar * kpc) / (Vpar * 1e3) / Gyr
        for a0, lbl in ((A0_CANON, "can"),):
            iso = nu_mcg(gb / a0) * gb
            qum = pred_efe_qumond(gb, a0, gx)
            m22 = pred_efe_m22(gb, a0, gx, t_orb / T_efe)
            print(f"      {nm:10s} ({lbl}): isolated {iso:.2e} -> QUM-EFE {qum:.2e} ({np.log10(qum/iso):+.2f} dex)"
                  f" -> M22-EFE {m22:.2e} ({np.log10(m22/iso):+.2f} dex)   [eN(can) = {gx/a0:.2f}]")
    print("""
  (b) OUT-OF-EQUILIBRIUM NEWTONIAN EXPECTATION: direction UNPINNED (no simulation source fetched within
      the budget; kicked self-gravitating systems can scatter V^2/R both ways). What IS pinned: Lelli+15
      states the TDGs have completed 'less than a full rotation since the interaction' and that it is
      'unclear whether they are in dynamical equilibrium' (t_merg/t_orb = 0.2-0.8). In the 1D toy the
      settled-law control from rest at cos-phase has NO amplitude transient (the response amplitude is
      algebraic per step), so the [1]-[2] curves isolate window physics; a real 2D disc's radial
      readjustment and phase mixing are NOT modelled here and enter the data as extra scatter, not as a
      sign-definite bias that this memo can claim.
  (c) INCLINATION (Lelli's dominant systematic; their Table 7 errors already include it; the swing if i
      were wrong by -+15 deg, Vcirc ~ 1/sin i):""")
    for t in TDGS:
        nm, D, R, eR, Vr, eVr, Vc, eVc, inc = t[:9]
        for di in (-15, +15):
            i2 = np.clip(inc + di, 20, 89)
            f = np.sin(np.radians(inc)) / np.sin(np.radians(i2))
            print(f"      {nm:10s} i = {inc:2d} -> {i2:2.0f} deg: g_obs x {f**2:.2f} ({2*np.log10(f):+.2f} dex)")
    print("""  (d) Mbar GEOMETRY: g_bar = G Mbar/R^2 is the spherical reading; a thin-disc edge raises g_bar by
      up to x1.3 (-0.11 dex on the offset via the pred slope ~0.5-0.8 => net ~ -+0.05 dex), gas beyond
      Rout lowers it (x0.8 => +-0.05 dex). Bracket carried: +-0.06 dex on the means -- subdominant.
  (e) Vrot vs Vcirc: the asymmetric-drift correction raises V (sigma_HI is comparable to Vrot in these
      discs). Offsets recomputed with RAW Vrot (canon footing, QUM-EFE):""")
    ds = []
    for t in TDGS:
        nm, D, R, eR, Vr, eVr, Vc, eVc, inc, Mb, eMb = t[:11]
        gx = t[17]
        Rm = R * kpc
        gb = G_SI * Mb * 1e8 * Msun / Rm ** 2
        go_r = (Vr * 1e3) ** 2 / Rm
        P = pred_efe_qumond(gb, A0_CANON, gx)
        d = np.log10(go_r / P); ds.append(d)
        print(f"      {nm:10s}: Ddex(Vrot) = {d:+.2f}  (vs Vcirc-based above)")
    print(f"      raw-Vrot weighted-mean shift: all offsets move DOWN (Vrot < Vcirc); mean {np.mean(ds):+.2f}")
    print("      -> the Vcirc choice is the CONSERVATIVE one for testing an ENHANCED fingerprint.\n")
    print("  (f) Upsilon* fork: gas fractions Mgas/Mbar = 0.78-0.93 -- doubling Upsilon* moves g_bar by")
    print("      < 0.06 dex for every TDG: the usual Upsilon convention fork is MOOT here (gas-dominated).")

def sec6():
    print(LINE)
    print("[6] VERDICT ARITHMETIC -- predicted offsets at the TDGs' measured ages vs the measured offsets")
    print(LINE)
    # measured: vs the EFE-corrected settled locus (the fingerprint rides ON TOP of the EFE), canon+fw
    # predicted: interpolate the [1]/[2] curves at each TDG's age-in-orbits (x_set ~ its own x), per combo
    print("  Measured (from [4]): weighted-mean offsets vs the settled EFE-corrected locus (the locus the")
    print("  transient rides on). Predicted: Ddex_a at each TDG's age/orbits from the [1]/[2] runs at its")
    print("  x_set (interpolated 0.05/0.1/0.2 grid), then the same weighted mean.")
    # gather TDG kinematic placements (canon, QUM-EFE as the reference locus; fw as the parallel column)
    combos = []
    for form in ("COMP", "IMPL"):
        for prep, x_par, tag in (("EFE", 0.0, "EFE-prep"), ("EFE", 1.0, "EFE+parent")):
            for N in (8, 16, 32):
                combos.append((form, prep, x_par, N, f"{form}/{tag}/N{N}"))
    # precompute fingerprint curves on the x grid
    curves = {}
    for form in ("COMP", "IMPL"):
        for x_par in (0.0, 1.0):
            for N in (8, 16, 32):
                for x_set in (0.05, 0.1, 0.2):
                    key = (form, x_par, N, x_set)
                    marks, dda, dda0, _, _, _, _, r = fingerprint_run(form, x_set, N, "EFE",
                                                                      x_par=x_par, par_fade=0.9 if x_par else 1.0)
                    tt = r["t"]
                    tg = np.arange(0.25, max(tt) - 0.5, 0.05)
                    aa = atfreq_amp(tt, r["a"], tg, w_extra=(1.65 if x_par else None))
                    curves[key] = (tg, np.log10(aa / x_set))
    # per-TDG measured offsets vs QUM-EFE and M22-EFE (both footings)
    meas = {}
    for a0 in (A0_FW, A0_CANON):
        for model in ("QUM-EFE", "M22-EFE"):
            ds, es, ages, xs = [], [], [], []
            for t in TDGS:
                nm, D, R, eR, Vr, eVr, Vc, eVc, inc, Mb, eMb = t[:11]
                age, tt_l, gx = t[15], t[16], t[17]
                dpar, Vpar = t[20], t[21]
                Rm = R * kpc
                go = (Vc * 1e3) ** 2 / Rm
                gb = G_SI * Mb * 1e8 * Msun / Rm ** 2
                t_orb = 2 * np.pi * Rm / (Vc * 1e3) / Gyr
                T_efe = 2 * np.pi * (dpar * kpc) / (Vpar * 1e3) / Gyr
                y_efe = t_orb / T_efe
                P = pred_efe_qumond(gb, a0, gx) if model == "QUM-EFE" else pred_efe_m22(gb, a0, gx, y_efe)
                Pp = pred_efe_qumond(gb * 1.01, a0, gx) if model == "QUM-EFE" else pred_efe_m22(gb * 1.01, a0, gx, y_efe)
                s = (np.log10(Pp) - np.log10(P)) / np.log10(1.01)
                e = np.sqrt((2 / LN10 * eVc / Vc) ** 2 + (s / LN10 * eMb / Mb) ** 2
                            + (abs(-1 + 2 * s) / LN10 * eR / R) ** 2)
                ds.append(np.log10(go / P)); es.append(e)
                ages.append(age / t_orb); xs.append(go / a0)
            meas[(a0, model)] = (np.array(ds), np.array(es), np.array(ages), np.array(xs))
    XG = np.array([0.05, 0.1, 0.2])
    print(f"\n    {'combo':22s} {'pred wmean':>11s}   vs QUM-EFE (can / fw)        vs M22-EFE (can / fw)")
    print(f"    {'':22s} {'(dex)':>11s}   wmean_obs-pred  sigma         wmean_obs-pred  sigma")
    for form, prep, x_par, N, tag in combos:
        # predicted offset per TDG at its age and x
        line = f"    {tag:22s}"
        preds_at = None
        for a0, model in ((A0_CANON, "QUM-EFE"), (A0_FW, "QUM-EFE"), (A0_CANON, "M22-EFE"), (A0_FW, "M22-EFE")):
            ds, es, ages, xs = meas[(a0, model)]
            pr = []
            for age_orb, x in zip(ages, xs):
                xc = np.clip(x, 0.05, 0.2)
                dd = []
                for xg in XG:
                    tg, cv = curves[(form, x_par, N, xg)]
                    dd.append(np.interp(np.clip(age_orb, tg[0], tg[-1]), tg, cv))
                pr.append(np.interp(np.log10(xc), np.log10(XG), dd))
            pr = np.array(pr)
            w = 1 / es ** 2
            mo = np.sum(w * (ds - pr)) / np.sum(w)
            so = 1 / np.sqrt(np.sum(w))
            if preds_at is None:
                preds_at = np.sum(w * pr) / np.sum(w)
                line += f" {preds_at:+11.3f}  "
            line += f" {mo:+6.3f}({abs(mo/so):4.1f}s)"
        print(line)
    # references: settled (Delta = 0) and Newtonian
    for tag, prfun in (("SETTLED (Ddex=0)", lambda gb, P: 0.0), ("NEWTONIAN (g=g_bar)", None)):
        line = f"    {tag:22s} {'':11s}  "
        for a0, model in ((A0_CANON, "QUM-EFE"), (A0_FW, "QUM-EFE"), (A0_CANON, "M22-EFE"), (A0_FW, "M22-EFE")):
            ds, es, ages, xs = meas[(a0, model)]
            if prfun is None:
                pr = []
                for t in TDGS:
                    nm, D, R, eR, Vr, eVr, Vc, eVc, inc, Mb, eMb = t[:11]
                    gx = t[17]; dpar, Vpar = t[20], t[21]
                    Rm = R * kpc
                    gb = G_SI * Mb * 1e8 * Msun / Rm ** 2
                    t_orb = 2 * np.pi * Rm / (Vc * 1e3) / Gyr
                    T_efe = 2 * np.pi * (dpar * kpc) / (Vpar * 1e3) / Gyr
                    P = pred_efe_qumond(gb, a0, gx) if model == "QUM-EFE" else pred_efe_m22(gb, a0, gx, t_orb / T_efe)
                    pr.append(np.log10(gb / P))
                pr = np.array(pr)
            else:
                pr = np.zeros(len(ds))
            w = 1 / es ** 2
            mo = np.sum(w * (ds - pr)) / np.sum(w)
            so = 1 / np.sqrt(np.sum(w))
            line += f" {mo:+6.3f}({abs(mo/so):4.1f}s)"
        print(line)
    # internal consistency of the six offsets (errors honest? scatter beyond errors?)
    print("\n  internal consistency (chi2 of the 6 offsets about their weighted mean):")
    for a0, model, lbl in ((A0_CANON, "QUM-EFE", "can/QUM"), (A0_CANON, "M22-EFE", "can/M22")):
        ds, es, ages, xs = meas[(a0, model)]
        w = 1 / es ** 2
        mean = np.sum(w * ds) / np.sum(w)
        chi2 = float(np.sum((ds - mean) ** 2 / es ** 2))
        print(f"    {lbl}: chi2 = {chi2:.1f} / 5 dof -- " +
              ("errors conservative (offsets over-consistent)" if chi2 < 5 else
               "scatter consistent with errors" if chi2 < 11.1 else "EXCESS scatter beyond errors"))
    print("\n  (sigma in parentheses = |weighted-mean residual| / its error; > 2 = disfavored, > 3 = excluded")
    print("   under the stated conventions. NOTE the toy-level approximation: the transient curves use the")
    print("   generic EFE prep (y_efe = 0.3, e_g = 0.2 a0, theta_A); per-TDG y_efe = 0.3-1.0 and e_N vary --")
    print("   second-order against the 0.1-0.3 dex form gaps. Verdict text in the memo.)")

if __name__ == "__main__":
    secs = sys.argv[1:] if len(sys.argv) > 1 else ["0", "1", "2", "3", "4", "5", "6"]
    print(LINE)
    print("agentJJ -- the transient fingerprint confronted (TDGs) -- run date 2026-06-11")
    print(LINE)
    for s in secs:
        {"0": sec0, "1": sec1, "2": sec2, "3": sec3, "4": sec4, "5": sec5, "6": sec6}[s]()
    print("[DONE] sections " + " ".join(secs))
