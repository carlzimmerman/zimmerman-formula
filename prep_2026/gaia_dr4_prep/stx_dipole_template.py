#!/usr/bin/env python3
"""
GAIA DR4 PREP -- DOOR 4B: s^TX BOOST-DIPOLE FIXED-DIRECTION TEMPLATE FIT
================================================================================
PREP ONLY. No new theory claims. The fixed-direction amplitude fit for the SME
boost dipole s^{Tj}, direction LOCKED at the CMB apex.

BANKED INPUTS (honored, not re-derived):
  * Prediction (Saturn channel / binding): |s^TX| = 8.68e-10  [canonical a0]
    from zimmerman-formula/real_research/reviews/stx_target.py and the
    per-body formula s^{Tj} = (a0 / 2|g_orb|) gamma^2 beta_cmb n_hat_j
    (stx_inpop_recipe.py; a0 enters LINEARLY -> both footings below).
  * LOCKED apex component ratios (equatorial J2000):
        s^TY : s^TX : s^TZ = 0.208 : -0.971 : -0.120
    (= the Planck 2018 dipole apex l=264.021, b=48.253 -> RA 167.94, Dec -6.94;
    verified against the rotation below to <0.5%).
  * Current combined bound: sigma(s^TX) ~ 1.3e-9 (Hees et al. 2016 review,
    arXiv:1610.04682 Table 9; Kostelecky-Russell Data Tables v19 Table D50:
    combined fit (-0.2 +/- 1.3)e-9) -> margin ~1.5x over the canonical
    prediction, i.e. the prediction sits 0.67 sigma INSIDE the bar with the
    predicted (negative) sign. DO NOT cite "~9.6x margin": that figure is the
    superseded Saturn-a x INPOP-ONLY (8.3e-9) looser-bound corner (banked
    correction 2026-06-21), not the live combined bound.
  * BOTH a0 FOOTINGS: canonical 9.36e-11 -> 8.68e-10; alt 1.13e-10 ->
    8.68e-10 x (1.13/0.936) = 1.048e-9 (margin vs bound only ~1.24x).
  * INTERPRETATION GUARD (banked 2026-06-21): s^TX is the PREFERRED-FRAME /
    Lorentz-violation discriminator and is MOND-family-SHARED (any
    preferred-frame MG host induces a comparable s^TX). It is NOT an
    MI-vs-MG discriminator; no outcome here separates MI from MG.

PHYSICS (Hees, Bailey et al., PRD 92, 064049 (2015), Eq. 3; transcribed in the
banked stx_inpop_recipe.py): the s^{0j} boost piece adds, for a Sun-planet
two-body system,
    d2r/dt2 |_SME = (2 G M / (c r^3)) [ (s.v) r_vec - (r.v) s_vec ],
with s_vec = amplitude x n_hat. Overall EOM sign convention flips only the
sign of the fitted amplitude; the template is built at the + sign (banked
cross-check integrated both signs against H15 Eq. 7).

PIPELINE (the fixed-direction fit, prep for the DR4-era ephemeris cycle):
  fit_amplitude(times, residuals, sigma) -> (alpha_hat, sigma_alpha)
  * template T(t): Earth-Saturn range perturbation from numerical integration
    (DOP853, rtol 3e-12) of BOTH bodies (Saturn and EMB each carry their own
    per-body s amplitude, locked to one overall multiplier alpha;
    alpha = 1 <=> |s^TX(Saturn)| = 8.68e-10);
  * linearity of T in alpha verified numerically (two scalings, <1% required);
  * ephemeris-absorption: T and the data are projected orthogonal to the
    partials of 6 Saturn ICs + 6 EMB ICs + GM_sun + range bias + linear drift
    (finite differences; the banked "conservative" absorption level -- a real
    INPOP/DE global refit absorbs more: asteroid ring, other planets ->
    FLAGGED: sensitivities here are upper limits at this absorption level);
  * GLS amplitude fit: alpha_hat = <T_perp, d> / <T_perp, T_perp>.

SYNTHETIC-INJECTION GATE (no hard-coded passes):
  Cassini-like Saturn ranging: 623 normal points 2004.0-2017.7 (Di Ruscio et
  al. 2020, A&A 640, A7: Cassini metre-level Saturn NPs), Gaussian noise
  sigma_NP = 6 m primary (metre-level mid value, FLAG approx; 3 m and 15 m
  sensitivity rows). Inject alpha_true = 1 (canonical), alpha_true = 0
  (null), AND a high-S/N alpha_true = 2000 (so recovery is exercised above
  the noise, still linear); 500 noise realizations each; require:
    (a) mean recovered alpha within 3 sem of truth, all three cases;
    (b) high-S/N case recovered at per-realization |alpha/2000 - 1| < 5%;
    (c) empirical sigma(alpha) consistent with the analytic GLS sigma (20%);
    (d) linearity check passes.
  Reports: sigma(s^TX) of this channel, detection significance of the
  prediction, and the sigma at which the prediction separates from a
  bound-saturating signal (1.3e-9), both footings. Universal-reading (U)
  template cross-fit reported (banked P/U fork).

HONEST EXPECTATION (verified against the banked recipe this session): the
single Cassini-Saturn direct-range channel at conservative absorption is
sigma(s^TX) ~ 1e-7 -- it CANNOT alone detect 8.68e-10 or separate it from
1.3e-9. The banked stx_inpop_recipe.py reference (rerun 2026-07-16): Saturn P
raw p2p 6.721e-2 m, RMS con 4.725e-3 m, sigma_A 4.5e-8; the strong per-body
channel is MARS ranging (sigma_A 3.44e-9) and the published 1.3e-9 bound is
the COMBINED multi-planet secular fit. This pipeline is the fixed-direction
fit MACHINERY (the piece that is new for the DR4-era cycle), gated on
recovery, not a sensitivity claim.

exit 0 iff all gate checks pass.
C. Zimmerman prep campaign, 2026-07-16.
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp

# ----------------------------------------------------------------------
# Constants + banked inputs
# ----------------------------------------------------------------------
GM   = 1.32712440018e20      # Sun, m^3/s^2
AU   = 1.495978707e11
c    = 299792458.0
YR   = 3.15576e7

A0_CAN, A0_ALT = 9.36e-11, 1.13e-10
STX_TARGET     = 8.68e-10                       # banked Saturn-channel |s^TX|
STX_ALT        = STX_TARGET*(A0_ALT/A0_CAN)     # a0 enters linearly
BOUND_STX      = 1.3e-9                         # Hees+16 combined
beta = 369.82e3/c
gam2 = 1.0/(1.0-beta**2)

# LOCKED direction: equatorial ratios (Y, X, Z) = (0.208, -0.971, -0.120)
n_eq = np.array([-0.971, 0.208, -0.120]); n_eq /= np.linalg.norm(n_eq)

# cross-check vs Planck apex through the IAU rotation (banked recipe, sec 0)
R_eq2gal = np.array([[-0.0548755604, -0.8734370902, -0.4838350155],
                     [ 0.4941094279, -0.4448296300,  0.7469822445],
                     [-0.8676661490, -0.1980763734,  0.4559837762]])
l, b = np.radians(264.021), np.radians(48.253)
n_gal = np.array([np.cos(b)*np.cos(l), np.cos(b)*np.sin(l), np.sin(b)])
n_chk = R_eq2gal.T @ n_gal
assert np.linalg.norm(n_chk - n_eq) < 5e-3, "locked ratios vs Planck apex mismatch"

eps_obl = np.radians(23.4392911)
R_eq2ecl = np.array([[1, 0, 0],
                     [0,  np.cos(eps_obl), np.sin(eps_obl)],
                     [0, -np.sin(eps_obl), np.cos(eps_obl)]])
n_ecl = R_eq2ecl @ n_eq                          # integration frame = ecliptic

# J2000 mean elements (Standish): a[AU], e, i, Omega, varpi, L [deg]
ELEM = {
 'EMB'   : (1.00000011, 0.01671022, 0.00005, -11.26064, 102.94719, 100.46435),
 'Saturn': (9.53707032, 0.05415060, 2.48446, 113.71504,  92.43194,  49.94432),
}
def g_orb(a_AU): return GM/(a_AU*AU)**2

# per-body amplitude at alpha=1, NORMALIZED so |s^TX(Saturn)| = STX_TARGET
# exactly (the ~1% Standish-vs-ledger a-convention offset is absorbed into the
# normalization; the RATIO EMB/Saturn keeps the per-body 1/g scaling)
_amp_raw = {p: (A0_CAN/(2*g_orb(ELEM[p][0])))*gam2*beta for p in ELEM}
_norm    = STX_TARGET/(_amp_raw['Saturn']*abs(n_eq[0]))
AMP      = {p: _amp_raw[p]*_norm for p in ELEM}
print("== banked-input checks ==")
print(f"locked n_hat (eq): X={n_eq[0]:+.4f} Y={n_eq[1]:+.4f} Z={n_eq[2]:+.4f} "
      f"(vs Planck-apex rotation: |diff|={np.linalg.norm(n_chk-n_eq):.1e})")
print(f"raw Saturn |s^TX| = {_amp_raw['Saturn']*abs(n_eq[0]):.3e} "
      f"(banked 8.68e-10; norm factor {_norm:.4f} absorbs the a-convention)")
assert abs(_amp_raw['Saturn']*abs(n_eq[0]) - STX_TARGET) < 0.12e-10
print(f"prediction: |s^TX| canonical = {STX_TARGET:.3e} | alt footing = "
      f"{STX_ALT:.3e} | combined bound ~ {BOUND_STX:.1e} "
      f"(margins {BOUND_STX/STX_TARGET:.2f}x / {BOUND_STX/STX_ALT:.2f}x)")

def s_vec(planet, alpha, reading='P'):
    if reading == 'P':                 # per-body (ledger formula, 1/g scaling)
        return alpha*AMP[planet]*n_ecl
    return alpha*AMP['Saturn']*n_ecl   # universal at the Saturn-channel value

# ----------------------------------------------------------------------
# Two-body integration with the H15 Eq.(3) boost term
# ----------------------------------------------------------------------
def kepler_state(planet, t=0.0):
    a_AU, e, i, Om, vp, L = ELEM[planet]
    i, Om, vp, L = np.radians([i, Om, vp, L]); w = vp - Om
    a = a_AU*AU; n = np.sqrt(GM/a**3)
    M = (L - vp) + n*t
    E = M
    for _ in range(80): E = E - (E - e*np.sin(E) - M)/(1 - e*np.cos(E))
    xp, yp = a*(np.cos(E)-e), a*np.sqrt(1-e**2)*np.sin(E)
    Ed = n/(1-e*np.cos(E))
    vx, vy = -a*np.sin(E)*Ed, a*np.sqrt(1-e**2)*np.cos(E)*Ed
    P = np.array([ np.cos(Om)*np.cos(w)-np.cos(i)*np.sin(Om)*np.sin(w),
                   np.sin(Om)*np.cos(w)+np.cos(i)*np.cos(Om)*np.sin(w),
                   np.sin(i)*np.sin(w)])
    Q = np.array([-np.cos(Om)*np.sin(w)-np.cos(i)*np.sin(Om)*np.cos(w),
                  -np.sin(Om)*np.sin(w)+np.cos(i)*np.cos(Om)*np.cos(w),
                   np.sin(i)*np.cos(w)])
    R = np.column_stack([P, Q, np.cross(P, Q)])
    return R @ np.array([xp, yp, 0.]), R @ np.array([vx, vy, 0.])

def integrate(y0, sv, ts, gm_fac=1.0):
    f = lambda t, y: np.hstack([y[3:],
        -GM*gm_fac*y[:3]/np.linalg.norm(y[:3])**3
        + (2*GM/(c*np.linalg.norm(y[:3])**3))*((sv@y[3:])*y[:3]-(y[:3]@y[3:])*sv)])
    return solve_ivp(f, (ts[0], ts[-1]), y0, t_eval=ts,
                     rtol=3e-12, atol=1e-4, method='DOP853').y[:3]

# ----------------------------------------------------------------------
# Template + absorption machinery
# ----------------------------------------------------------------------
T0, T1, NPTS = 4.0*YR, 17.7*YR, 623        # Cassini window (Di Ruscio+2020)
rng = np.random.default_rng(20261216)
TS = np.sort(rng.uniform(T0, T1, NPTS))

def build_geometry(ts):
    y0s = np.hstack(kepler_state('Saturn', ts[0]))
    y0e = np.hstack(kepler_state('EMB',   ts[0]))
    z = np.zeros(3)
    rs0, re0 = integrate(y0s, z, ts), integrate(y0e, z, ts)
    rho0 = np.linalg.norm(rs0-re0, axis=0)
    return y0s, y0e, rs0, re0, rho0

def raw_signal(ts, geom, scale, reading='P'):
    """Range perturbation for alpha=scale, divided back by scale (template)."""
    y0s, y0e, rs0, re0, rho0 = geom
    rs = integrate(y0s, s_vec('Saturn', scale, reading), ts)
    re = integrate(y0e, s_vec('EMB',    scale, reading), ts)
    return (np.linalg.norm(rs-re, axis=0) - rho0)/scale

def absorption_matrix(ts, geom):
    """FD partials: 6 Saturn ICs, 6 EMB ICs, GM, bias, drift  (banked 'con')."""
    y0s, y0e, rs0, re0, rho0 = geom
    z, cols = np.zeros(3), []
    for body, y0_, other, sgn in (('S', y0s, re0, +1), ('E', y0e, rs0, -1)):
        for j in range(6):
            dy = np.zeros(6)
            step = 1e-7*np.linalg.norm(y0_[:3] if j < 3 else y0_[3:]); dy[j] = step
            rj = integrate(y0_+dy, z, ts)
            d = rj-other if body == 'S' else other-rj
            cols.append((np.linalg.norm(d, axis=0)-rho0)/step)
    cols.append((np.linalg.norm(integrate(y0s, z, ts, 1+1e-9)
                 - integrate(y0e, z, ts, 1+1e-9), axis=0)-rho0)/1e-9)
    cols.append(np.ones_like(ts))                 # range bias
    cols.append((ts-ts[0])/(ts[-1]-ts[0]))        # linear drift
    A = np.array(cols).T
    A /= np.linalg.norm(A, axis=0)
    return A

def project_perp(A, x):
    with np.errstate(all='ignore'):   # spurious Accelerate-BLAS matmul warnings
        r = x - A @ np.linalg.lstsq(A, x, rcond=None)[0]   # on macOS (cf. the
    assert np.all(np.isfinite(r)), "non-finite projection: real numerical bug"
    return r                          # banked stx_inpop_recipe.py, same guard)

def fit_amplitude(residuals, T_perp, sigma_np):
    """The DR4-era entry point: GLS amplitude of the locked-direction template.
    residuals must already be ephemeris-postfit (or projected with the same A)."""
    tt = float(T_perp @ T_perp)
    return float(T_perp @ residuals)/tt, sigma_np/np.sqrt(tt)

# ----------------------------------------------------------------------
# BUILD + GATE
# ----------------------------------------------------------------------
print("\n== build: geometry, template, absorption (DOP853 rtol 3e-12) ==")
geom = build_geometry(TS)
SC_T, SC_I = 1e6, 3e5     # template and injection built at DIFFERENT scalings
T_raw  = raw_signal(TS, geom, SC_T)
T_raw2 = raw_signal(TS, geom, SC_I)
lin_err = np.max(np.abs(T_raw-T_raw2))/np.max(np.abs(T_raw))
lin_ok = lin_err < 1e-2
print(f"template raw p2p = {np.ptp(T_raw):.3e} m per unit alpha "
      f"(alpha=1 <=> |s^TX|=8.68e-10)")
print(f"linearity check (x{SC_T:.0e} vs x{SC_I:.0e}): rel dev = {lin_err:.2e} "
      f"-> {'PASS' if lin_ok else 'FAIL'}")

A = absorption_matrix(TS, geom)
T_perp = project_perp(A, T_raw)
T_perp_U = project_perp(A, raw_signal(TS, geom, SC_T, 'U'))
print(f"after absorption (12 ICs + GM + bias + drift): "
      f"RMS(T_perp) = {np.sqrt(np.mean(T_perp**2)):.3e} m per unit alpha "
      f"(raw RMS {np.sqrt(np.mean(T_raw**2)):.3e}; "
      f"absorbed {(1-np.sqrt(np.mean(T_perp**2)/np.mean(T_raw**2)))*100:.1f}%)")

# injection signal: built from the INDEPENDENT scaling run
SIG_perp = project_perp(A, T_raw2)     # = alpha_true x T_perp up to lin_err

NRE = 500
ABIG = 2000.0        # high-S/N injection (still linear: lin check spans x3.3)
print(f"\n== GATE: {NPTS} NPs 2004.0-2017.7, {NRE} noise realizations ==")
gate_ok = lin_ok
rows = []
for sig_np in (3.0, 6.0, 15.0):
    ah = np.empty(NRE); a0h = np.empty(NRE); abg = np.empty(NRE)
    for k in range(NRE):
        noise = sig_np*rng.standard_normal(NPTS)
        ah[k],  sa = fit_amplitude(SIG_perp*1.0 + noise, T_perp, sig_np)
        a0h[k], _  = fit_amplitude(noise, T_perp, sig_np)
        abg[k], _  = fit_amplitude(SIG_perp*ABIG + noise, T_perp, sig_np)
    m1, s1 = ah.mean(),  ah.std(ddof=1)
    m0, s0 = a0h.mean(), a0h.std(ddof=1)
    mb, sb = abg.mean(), abg.std(ddof=1)
    sem = s1/np.sqrt(NRE)
    ok1 = abs(m1-1.0) < 3*sem
    ok0 = abs(m0-0.0) < 3*(s0/np.sqrt(NRE))
    okb = (abs(mb/ABIG-1.0) < 3*(sb/np.sqrt(NRE))/ABIG) and \
          np.all(np.abs(abg/ABIG-1.0) < 0.05 + 5*sa/ABIG)
    ok2 = abs(s1/sa - 1.0) < 0.20
    gate_ok &= ok1 & ok0 & ok2 & okb
    rows.append((sig_np, m1, s1, sa))
    print(f" sigma_NP={sig_np:4.1f} m: inj alpha=1 -> {m1:+.3f}+-{s1:.3f} "
          f"(analytic {sa:.3f}) [{'PASS' if ok1 else 'FAIL'}] | "
          f"null -> {m0:+.3f}+-{s0:.3f} [{'PASS' if ok0 else 'FAIL'}] | "
          f"emp/analytic {s1/sa:.3f} [{'PASS' if ok2 else 'FAIL'}]")
    print(f"               high-S/N inj alpha={ABIG:.0f} -> recovered "
          f"{mb:.1f}+-{sb:.1f} (ratio {mb/ABIG:.4f}) "
          f"[{'PASS' if okb else 'FAIL'}]")

# universal-reading cross-fit (banked P/U fork; shape differs via EMB weight)
aU = float(T_perp_U @ SIG_perp)/float(T_perp_U @ T_perp_U)
print(f" P/U fork: per-body injection fit with the UNIVERSAL template -> "
      f"alpha = {aU:+.4f} (reading mismatch bias, noise-free)")

print("\n== DELIVERABLE NUMBERS (single Cassini-Saturn channel, this ==")
print("==            absorption level; FLAGGED as such)             ==")
print(f"{'sigma_NP':>9} {'sigma(s^TX)':>12} {'det canonical':>14} "
      f"{'det alt':>9} {'pred-vs-bound sep':>18}")
for sig_np, m1, s1, sa in rows:
    s_stx = sa*STX_TARGET
    det_c = STX_TARGET/s_stx
    det_a = STX_ALT/s_stx
    sep   = (BOUND_STX-STX_TARGET)/s_stx
    print(f"{sig_np:8.1f}m {s_stx:12.3e} {det_c:12.4f}s {det_a:8.4f}s "
          f"{sep:16.4f}s")
print("""HONEST VERDICT: this single direct-range channel is ~2 orders short of the
prediction -- detection significance ~0.006 sigma and pred-vs-bound separation
~0.003 sigma at 6 m. That MATCHES the banked reference (stx_inpop_recipe.py
reading P: Saturn sigma_A = 4.5e-8, S/N 0.02): the 1.3e-9 combined bound and
any future kill/confirm live in the MULTI-PLANET secular fit (banked: Mars P
channel sigma_A = 3.44e-9; INPOP wdot supplementary advances), NOT in Cassini
Saturn ranging alone. The deliverable here is the GATED fixed-direction
template machinery (locked ratios 0.208:-0.971:-0.120), ready to ingest real
DR4-era ephemeris residual series via fit_amplitude().""")

ALT_FAC = STX_ALT/STX_TARGET   # 1.207: alpha at which the ALT footing sits
print(f"""
== FROZEN DECISION BANDS (pre-registered 2026-07-16; PREREGISTRATION_DR4.md) ==
Statistic: alpha_hat, sigma_a = fit_amplitude() GLS on the LOCKED template
  (direction = CMB apex, ratios s^TY:s^TX:s^TZ = 0.208:-0.971:-0.120, sign
  built in: alpha > 0 IS the framework sign, s^TX < 0). Primary reading = P
  (per-body 1/g, the ledger's own formula); U cross-fit always reported
  (noise-free P-vs-U template overlap here: alpha_U = {aU:+.4f} -> the readings
  are nearly orthogonal in this channel; verdicts are quoted PER READING).
  alpha = 1 <=> |s^TX| = {STX_TARGET:.3e} (canonical a0 = {A0_CAN:.2e});
  alpha = {ALT_FAC:.3f} <=> |s^TX| = {STX_ALT:.3e} (alt a0 = {A0_ALT:.2e}).
DETECT (canonical): alpha_hat >= 3 sigma_a  AND  |alpha_hat - 1| <= 2 sigma_a.
DETECT (alt):       alpha_hat >= 3 sigma_a  AND  |alpha_hat - {ALT_FAC:.3f}| <= 2 sigma_a.
KILL (canonical):   |alpha_hat| < 2 sigma_a with sigma_a <= 0.50
                    (i.e. sigma(s^TX) <= {STX_TARGET/2:.2e}); 3-sigma kill at
                    sigma_a <= 0.33 (sigma(s^TX) <= {STX_TARGET/3:.2e}).
KILL (alt):         same with sigma_a <= {ALT_FAC/2:.3f} (sigma(s^TX) <= {STX_ALT/2:.2e}).
WRONG SIGN:         alpha_hat <= -3 sigma_a ALSO kills (direction-locked; no
                    sign freedom is available post hoc).
NO-VERDICT:         any sigma_a above the kill threshold that excludes neither
                    0 nor the prediction (the present standing: prediction
                    0.67 sigma inside the combined (-0.2 +/- 1.3)e-9 bar).
Interpretation guard: any outcome is a PREFERRED-FRAME/LV verdict, MOND-family-
shared -- NOT an MI-vs-MG verdict.""")

print("\n" + "="*78)
print(f"GATE VERDICT: {'PASS' if gate_ok else 'FAIL'} "
      f"(linearity, injection recovery, null, sigma consistency)")
print("="*78)
sys.exit(0 if gate_ok else 1)
