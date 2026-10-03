#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
AUDIT of L341's sigma_8 = 18-27 (e9f450b10) -- diagnostics only; nothing here re-scores or replaces L341.

Loads L341's own machinery from the byte-identical copy in this folder (L341_rerun_copy.py, sha256 checked against
real_research/g03_audit_2026/L341_chk_frw_gate.py), executes it only up to its F1 banner (definitions: cosmology,
EH98 spectrum normalised to sigma_8 = 0.811, nu_mono, growth()), then asks:

  D1  At L341's start (z_i = 1000) is the perturbation field Newtonian (y >> 1)?  If yes, the pre-z_i transfer
      (EH98 / LCDM) is framework-correct for the chassis with its cold component, and the A_s anchor is fair.
  D2  The history: rms field y(z) and nu(y) along the MOND run; when does the boost switch on; when does the
      sigma_8-window amplitude cross 1 (onset of nonlinearity)?  Is the excess made while delta << 1?
  D3  Ratio of MOND to LCDM growth vs redshift (what a CMB-lensing or z ~ 1-3 clustering probe would see).
  D4  Anchor sensitivity (fixed, declared, not a fit): initial amplitude x (1 +- 0.042) [~3 sigma of Planck A_s in
      amplitude] and x 0.1 / x 10 [an order-of-magnitude anchor error].  Does any rescue sigma_8?
  D5  Start-time sensitivity (fixed, declared): MOND boost switched on only from z = 200 / 50 / 10 instead of 1000.
  D6  Framework-neutral field scale today: the peculiar acceleration implied by the measured Local Group motion,
      v ~ 600 km/s with f ~ Omega_m^0.55, g ~ H0 f^-1 v ... reported in units of a0 (an order-of-magnitude check that
      the real large-scale field is sub-a0).

kappa = 1/2 fixed (both footings as L341).  No downloads.  Writes audit_sigma8_diagnostics_results.json here.
Run from this folder or the repo root:  python3 campaign_fresh_gravity/AUDIT_SIGMA8_2026-10-03/audit_sigma8_diagnostics.py
"""
import os, sys, json, math, hashlib, io, contextlib
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(HERE, "L341_rerun_copy.py"); ORIG = os.path.join(REPO, "real_research", "g03_audit_2026", "L341_chk_frw_gate.py")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
assert sha(SRC) == sha(ORIG), "copy differs from L341's committed script"
code = open(SRC).read(); cut = code.index('banner("F1')
ns = {"__file__": SRC, "__name__": "l341_defs"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:cut], SRC, "exec"), ns)
P = lambda *a: print(*a, flush=True)
OUT = {"sha256_L341": sha(SRC)}
c, G, H0, Om, Or, rho_crit0, h = (ns[k] for k in ("c", "G", "H0", "Om", "Or", "rho_crit0", "h"))
Mpc, KH, DREF, A0, nu_mono, sigma8_of = ns["Mpc"], ns["KH"], ns["DREF"], ns["A0"], ns["nu_mono"], ns["sigma8_of"]
OL = 1 - Om - Or
Ez = lambda a: math.sqrt(Or/a**4 + Om/a**3 + OL); dlnH = lambda a: 0.5*(-4*Or/a**4 - 3*Om/a**3)/Ez(a)**2
Wth = ns["Wth"]

def lcdm_D(a_i=1/1001.):
    s = solve_ivp(lambda N, Y: [Y[1], 1.5*(Om/math.exp(3*N)/Ez(math.exp(N))**2)*Y[0] - (2 + dlnH(math.exp(N)))*Y[1]],
                  (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-9, atol=1e-14, dense_output=True)
    return s

def run_rms(foot="canonical", amp=1.0, z_on=None, z_i=1000.0, dense=True):
    """L341's 'rms' growth (c_2 tracking factor ~1 in the window, as L341 F2 shows: c_2 0.0073 vs 0.067 identical to 1e-3);
    here the tracking factor is omitted (c_2 -> window, boost = nu).  amp scales the initial amplitude; z_on delays the boost."""
    a_i = 1/(1 + z_i); a0 = A0[foot]; sL = lcdm_D(a_i); r0 = sL.sol(0.0)[0]; Di = amp*DREF/r0
    def grms_of(a, D):
        rho = Om*rho_crit0/a**3; gk = 4*math.pi*G*rho*np.abs(Di*D)/(KH*h/(a*Mpc))
        return math.sqrt(np.trapz(gk**2/KH, KH)/np.trapz(1/KH, KH))
    def rhs(N, Y):
        a = math.exp(N); D, Dp = Y
        y = grms_of(a, D)/a0; nu = nu_mono(y) if (z_on is None or 1/a - 1 <= z_on) else 1.0
        return [Dp, 1.5*(Om/a**3/Ez(a)**2)*nu*D - (2 + dlnH(a))*Dp]
    s = solve_ivp(rhs, (math.log(a_i), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-7, atol=1e-12, dense_output=dense)
    return s, sL, Di, grms_of, a0

banner = lambda t: (P("\n" + "=" * 100), P(t), P("=" * 100))

banner("D0  CONTROL: this harness reproduces L341 F2 rms (c_2 window) sigma_8")
D0 = {}
for foot in ("canonical", "alt"):
    s, sL, Di, gof, a0 = run_rms(foot)
    D0[foot] = sigma8_of(Di*s.y[0][-1]); P(f"    {foot:9s}: sigma_8 = {D0[foot]:.3f}  (L341 committed: canonical 23.314 / alt 27.474)")
OUT["D0"] = D0
ok0 = abs(D0["canonical"]/23.314 - 1) < 0.01 and abs(D0["alt"]/27.474 - 1) < 0.01
P(f"  [{'PASS' if ok0 else 'FAIL'}] D0 within 1% of L341")

banner("D1/D2  THE FIELD AND THE BOOST ALONG THE HISTORY (canonical, rms)")
s, sL, Di, gof, a0 = run_rms("canonical")
rows = []
s8_0_lcdm = sigma8_of(DREF)
for z in (1000, 500, 200, 100, 50, 20, 10, 5, 3, 2, 1, 0.5, 0):
    a = 1/(1 + z); N = math.log(a); D = s.sol(N)[0]; DL = sL.sol(N)[0]/sL.sol(0.0)[0]
    y = gof(a, D)/a0; yL = gof(a, sL.sol(N)[0])/a0
    s8m = sigma8_of(Di*D); s8l = s8_0_lcdm*DL
    rows.append(dict(z=z, y_rms_mond=y, nu=nu_mono(y), y_rms_lcdm=yL, nu_at_lcdm_field=nu_mono(yL),
                     sigma8_window_mond=s8m, sigma8_window_lcdm=s8l, growth_ratio=s8m/s8l))
    P(f"    z {z:6g}: y_rms {y:9.3g} (LCDM-field {yL:9.3g})  nu {nu_mono(y):7.3g}   sigma8-window MOND {s8m:9.3g}  LCDM {s8l:7.3g}  ratio {s8m/s8l:7.3g}")
OUT["D2_history"] = rows
# onset: first z (scan fine) where sigma8-window MOND crosses 1, and the growth ratio there
zz = np.concatenate([np.geomspace(1000, 1, 400), np.linspace(1, 0, 101)[1:]])
cross = None
for z in zz:
    a = 1/(1 + z); D = s.sol(math.log(a))[0]
    if sigma8_of(Di*D) >= 1.0: cross = z; break
aC = 1/(1 + cross); ratio_at_cross = sigma8_of(Di*s.sol(math.log(aC))[0])/(s8_0_lcdm*sL.sol(math.log(aC))[0]/sL.sol(0.0)[0])
P(f"    the sigma_8-window amplitude of the MOND run crosses 1 (nonlinear on 8 Mpc/h) at z = {cross:.2f}; growth ratio there {ratio_at_cross:.3g}")
OUT["D2_nonlinear_onset"] = {"z_cross_sigma8_window_1": float(cross), "growth_ratio_at_cross": float(ratio_at_cross)}
ok1 = rows[0]["y_rms_mond"] > 10
P(f"  [{'PASS' if ok1 else 'FAIL'}] D1 at z_i = 1000 the field is Newtonian (y_rms > 10): y = {rows[0]['y_rms_mond']:.3g}, nu - 1 = {rows[0]['nu'] - 1:.2g}")

banner("D4  ANCHOR SENSITIVITY (declared amplitudes; not a fit)")
D4 = {}
for amp in (0.958, 1.042, 0.1, 10.0):
    sA, sLA, DiA, _, _ = run_rms("canonical", amp=amp, dense=False)
    D4[amp] = sigma8_of(DiA*sA.y[0][-1]); P(f"    initial amplitude x {amp:<6g}: sigma_8 = {D4[amp]:.3f}   (LCDM would give {0.811*amp:.3f})")
OUT["D4_anchor"] = {str(k): v for k, v in D4.items()}

banner("D5  START-TIME SENSITIVITY (boost on only below z_on; declared values)")
D5 = {}
for zon in (200, 50, 10, 3):
    sB, _, DiB, _, _ = run_rms("canonical", z_on=zon, dense=False)
    D5[zon] = sigma8_of(DiB*sB.y[0][-1]); P(f"    boost on for z <= {zon:<4g}: sigma_8 = {D5[zon]:.3f}")
OUT["D5_start"] = {str(k): v for k, v in D5.items()}

banner("D6  FRAMEWORK-NEUTRAL FIELD SCALE: the Local Group's peculiar acceleration")
v = 6.0e5; f = Om**0.55
g_lin = 1.5*Om*H0*v/f                                    # linear theory: v = 2 f g / (3 Omega_m H0)
P(f"    v = 600 km/s, f = Om^0.55 = {f:.3f}: g = 3 Om H0 v / (2 f) = {g_lin:.3g} m/s^2 = {g_lin/A0['canonical']:.3g} a0 (canonical) / {g_lin/A0['alt']:.3g} a0 (alt)")
P(f"    nu_mono at that y: {nu_mono(g_lin/A0['canonical']):.3g} (canonical) / {nu_mono(g_lin/A0['alt']):.3g} (alt)")
OUT["D6_LG_field"] = {"g_m_s2": g_lin, "y_canonical": g_lin/A0["canonical"], "y_alt": g_lin/A0["alt"],
                      "nu_canonical": nu_mono(g_lin/A0["canonical"]), "nu_alt": nu_mono(g_lin/A0["alt"])}

json.dump(OUT, open(os.path.join(HERE, "audit_sigma8_diagnostics_results.json"), "w"), indent=1, default=float)
P("\nwrote audit_sigma8_diagnostics_results.json")
sys.exit(0 if (ok0 and ok1) else 1)
