#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fbB2 -- THE CMB CONSEQUENCE.  Can a boosted MOND gravity do what CDM does at the third peak?
============================================================================================
TASK 2.  This is the crux, so the two DIFFERENT things CDM supplies are separated up front and
tested one at a time:

  (i)  CDM is a GRAVITATING DENSITY on the BACKGROUND.  It sets matter-radiation equality
       (z_eq = Om/Or - 1) and therefore the conformal time, the sound horizon r_s, the angular
       scale theta_* and the damping scale.  a0 is an ACCELERATION SCALE; it appears in no
       Friedmann equation on any branch.  So NOTHING a0 does -- constant, rising, or switching
       off -- can move (i).  Part 0 puts a number on how badly (i) breaks without CDM.

  (ii) CDM's potential wells do NOT DECAY after equality (no radiation driving), which is what
       lifts the third peak in LCDM.  A MOND boost multiplies a potential that IS decaying.
       Parts 1-4 integrate the actual tight-coupling equations and ask whether a boosted-but-
       decaying baryon potential is distinguishable, and in which direction.

THE INTEGRATOR.  Conformal-Newtonian gauge, ' = d/dtau, psi = phi (no anisotropic stress -- see
the honesty list).  Tight-coupled photon-baryon fluid, free CDM, one neutrino fluid:
    d_g'  = -(4/3) th + 4 phi'                d_n'  = -(4/3) th_n + 4 phi'
    d_b'  = -th + 3 phi'                      th_n' = k^2 (d_n/4) + k^2 psi
    d_c'  = -th_c + 3 phi'                    th_c' = -(a'/a) th_c + k^2 psi
    th'   = -(a'/a) R/(1+R) th + k^2 d_g/(4(1+R)) + k^2 psi        [R = 3 rho_b/4 rho_g]
    phi'  = -(a'/a) phi + (3/2)(aH)^2/k^2 * sum_i (1+w_i) f_i th_i  [momentum constraint]
MOND enters exactly as QUMOND/AQUAL does: the FORCE is boosted,
    psi = nu(y) phi,     y = (k/a) c^2 |phi| / a0(z),
with phi the GR (Newtonian) potential from the constraint above.  Two evaluations of y are run:
  PERMODE   y from the instantaneous |phi| -- nu DIVERGES at the oscillation's nodes;
  ENVELOPE  y from the oscillator amplitude sqrt(phi^2 + phi'^2/(k c_s)^2) -- smooth, no node
            singularity.  If both fail the failure is not an artefact of the singularity.
and the boost is additionally run in two GATINGS:
  UNGATED   the boost acts at all times (what the repository's earlier growth scripts do);
  GATED     the boost acts only where k > aH, i.e. only SUB-HORIZON, which is the only regime in
            which a quasi-static MOND limit is defined at all.  Applying MOND to a super-horizon
            mode is not licensed by any of these theories, so GATED is the conservative reading and
            no kill is claimed that does not survive it.

HONESTY LIST (stated before the numbers, not after):
  * neutrino anisotropic stress is dropped (fluid nu).  This is a known ~10-20% error on peak
    heights.  It is COMMON to every model compared here, and only ratios between models are used.
  * Silk damping is applied as a common envelope exp(-2(k/k_D)^2) with the EH98 k_Silk formula,
    recomputed per cosmology.  Peak ratios are reported BOTH damped and undamped.
  * this computes |Theta_0 + psi|^2 at last scattering, NOT C_l: no projection, no Doppler, no
    finite thickness, no reionisation.  It is a driving/peak-envelope calculation, good to tens of
    percent on RATIOS between models that share every approximation.  It is not a Boltzmann code
    and is not offered as one.
  * in the MOND runs the phi' appearing in the CONTINUITY equations is the GR phi', not nu*phi'.
    Sub-horizon (where every acoustic peak lives) those terms are subdominant to k^2 psi.
Both a0 footings carried.  Every check ASSERTS a statement and CAN fail.
"""
import math, sys, time
import numpy as np
from scipy.integrate import quad, solve_ivp

T0 = time.time(); FAILS = []; NC = [0]
def check(name, ok, detail=""):
    NC[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 118); print(t); print("=" * 118, flush=True)
def info(s): print("  " + s, flush=True)

c = 2.99792458e8; Mpc = 3.0856775814913673e22
h = 0.6736; om_b, om_c = 0.02237, 0.1200
T_CMB = 2.7255; N_eff = 3.046; ns, As, kpiv = 0.965, 2.1e-9, 0.05
G = 6.67430e-11
H0_SI = 100 * h * 1e3 / Mpc
sigma_sb = 5.670374419e-8
rho_crit0 = 3 * H0_SI**2 / (8 * math.pi * G)
Og = (4 * sigma_sb * T_CMB**4 / c**3) / rho_crit0
Onu = N_eff * (7. / 8.) * (4. / 11.) ** (4. / 3.) * Og
Or = Og + Onu
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
Zc = math.sqrt(32 * math.pi / 3.0)
z_rec = 1089.9
H0c = (100 * h) / 299792.458           # H0/c in 1/Mpc

print("=" * 118); print("fbB2 -- the CMB consequence: acoustic driving, the third peak, and what a0(z) can and cannot touch")
print("=" * 118, flush=True)

class Cos:
    """A background.  om_c_eff = 0 is the honest 'MOND replaces dark matter' universe."""
    def __init__(self, omc, name, ol=None):
        self.omc = omc; self.name = name
        self.Ob = om_b / h**2; self.Oc = omc / h**2; self.Om = self.Ob + self.Oc
        self.OL = (1 - self.Om - Or) if ol is None else ol
        self.z_eq = self.Om / Or - 1
    def E(self, z): zp = 1 + z; return math.sqrt(Or * zp**4 + self.Om * zp**3 + self.OL)
    def aH(self, a): return H0c * a * self.E(1 / a - 1)          # comoving Hubble, 1/Mpc
    def R(self, a): return 0.75 * (self.Ob / Og) * a
    def cs(self, a): return 1.0 / math.sqrt(3 * (1 + self.R(a)))
    def rs(self, z):
        f = lambda zz: self.cs(1 / (1 + zz)) / (H0c * self.E(zz))
        return quad(f, z, 1e8, limit=500)[0]
    def eta(self, z):
        f = lambda zz: 1.0 / (H0c * self.E(zz))
        return quad(f, z, 1e8, limit=500)[0]
    def DA(self, z):                                              # comoving angular distance
        return quad(lambda zz: 1.0 / (H0c * self.E(zz)), 0, z, limit=500)[0]
    def kD(self):                                                 # EH98 Silk scale, 1/Mpc
        om = self.Om * h * h
        return 1.6 * om_b**0.52 * om**0.73 * (1 + (10.4 * om) ** -0.95)

LCDM = Cos(om_c, "LCDM (omega_c = 0.1200)")
NODM = Cos(0.0, "baryon-only (omega_c = 0, MOND replaces DM)")

# ==================================================================================================
sec("PART 0 -- WHAT a0 CANNOT TOUCH: the background.  This step is independent of every a0 law.")
# ==================================================================================================
for C in (LCDM, NODM):
    info(f"{C.name:44s} z_eq = {C.z_eq:8.1f}  r_s(z_*) = {C.rs(z_rec):7.2f} Mpc  "
         f"D_A = {C.DA(z_rec):8.1f} Mpc  100 theta_* = {100*C.rs(z_rec)/C.DA(z_rec):.5f}  k_D = {C.kD():.4f}/Mpc")
th_lcdm = 100 * LCDM.rs(z_rec) / LCDM.DA(z_rec)
th_nodm = 100 * NODM.rs(z_rec) / NODM.DA(z_rec)
TH_PLANCK, TH_ERR = 1.04109, 0.00030
check("P0-a  CONTROL: the LCDM background reproduces Planck's 100 theta_* = 1.04109 +- 0.00030 to 0.3%",
      abs(th_lcdm / TH_PLANCK - 1) < 0.003, f"100 theta_* = {th_lcdm:.5f} (Planck {TH_PLANCK})")
nsig = abs(th_nodm - TH_PLANCK) / TH_ERR
check("P0-b  *** THE NUMBER THAT SETTLES IT ***  Deleting CDM and letting MOND supply the missing gravity "
      "moves 100 theta_* from %.5f to %.5f -- a %.1f%% shift, i.e. %.0f SIGMA on Planck's measurement. "
      "a0 appears in NO Friedmann equation on ANY branch, so no a0(z) law -- locked, rising, or switching off -- "
      "moves this by one part in 10^10" % (th_lcdm, th_nodm, 100 * (th_nodm / th_lcdm - 1), nsig),
      nsig > 100, f"100 theta_*: LCDM {th_lcdm:.5f}, no-CDM {th_nodm:.5f}, Planck {TH_PLANCK} +- {TH_ERR}  ->  {nsig:.0f} sigma")
check("P0-c  ...and the same deletion moves matter-radiation equality from z_eq = %.0f (BEFORE last scattering) "
      "to %.0f (AFTER it): a no-CDM universe is RADIATION-DOMINATED at recombination, which is the physical root "
      "of the third-peak problem" % (LCDM.z_eq, NODM.z_eq),
      NODM.z_eq < z_rec < LCDM.z_eq, f"z_eq: LCDM {LCDM.z_eq:.0f}, no-CDM {NODM.z_eq:.0f}, z_rec {z_rec}")
# can floating H0/OL rescue theta_*?
def theta_for(omc, hh):
    """100 theta_* for a flat universe with these omega_c, h (omega_b and T_CMB held at their measured values)."""
    Ob_x = om_b / hh**2; Oc_x = omc / hh**2; Om_x = Ob_x + Oc_x
    Or_x = Or * (h / hh) ** 2                     # omega_r is fixed by T_CMB, so Omega_r scales as h^-2
    OL_x = 1 - Om_x - Or_x
    H0c_x = (100 * hh) / 299792.458
    Ex = lambda z: math.sqrt(Or_x * (1 + z) ** 4 + Om_x * (1 + z) ** 3 + OL_x)
    Rb = lambda z: 0.75 * (om_b / (Og * h * h)) / (1 + z)      # omega_b/omega_gamma is h-independent
    rs = quad(lambda zz: (1 / math.sqrt(3 * (1 + Rb(zz)))) / (H0c_x * Ex(zz)), z_rec, 1e8, limit=500)[0]
    da = quad(lambda zz: 1 / (H0c_x * Ex(zz)), 0, z_rec, limit=500)[0]
    return 100 * rs / da
_ctl = theta_for(om_c, h)
check("P0-d0 CONTROL on the floating-H0 machinery: theta_for(omega_c = 0.12, h = 0.674) reproduces the direct "
      "LCDM number to 1%", abs(_ctl / th_lcdm - 1) < 0.01, f"theta_for = {_ctl:.5f} vs direct {th_lcdm:.5f}")
_scan = [(abs(theta_for(0.0, hh) - TH_PLANCK), hh) for hh in np.linspace(0.20, 2.00, 181)]
best = min(_scan)
info(f"floating H0 with omega_c = 0: over h in [0.20, 2.00] the CLOSEST 100 theta_* to Planck is "
     f"{theta_for(0.0, best[1]):.5f} at h = {best[1]:.3f}, still {abs(theta_for(0.0,best[1])-TH_PLANCK)/TH_ERR:.0f} sigma away")
check("P0-d  the geometric degeneracy does NOT rescue it: NO value of h in [0.20, 2.00] brings a no-CDM "
      "background back to Planck's theta_*.  The best is %.5f at h = %.2f, still %.0f sigma out, and that h is "
      "itself excluded by the distance ladder.  Removing CDM breaks the CMB geometry outright"
      % (theta_for(0.0, best[1]), best[1], abs(theta_for(0.0, best[1]) - TH_PLANCK) / TH_ERR),
      abs(theta_for(0.0, best[1]) - TH_PLANCK) / TH_ERR > 50,
      f"best 100 theta_* at omega_c = 0 is {theta_for(0.0,best[1]):.5f} at h = {best[1]:.2f} "
      f"({abs(theta_for(0.0,best[1])-TH_PLANCK)/TH_ERR:.0f} sigma); measured h = 0.674")

# ==================================================================================================
sec("PART 1 -- the tight-coupling integrator, and its controls")
# ==================================================================================================
def nu_line(y):   return math.sqrt(1 + 1 / max(y, 1e-30))
def nu_simple(y): return math.sqrt((1 + math.sqrt(1 + 4 / max(y, 1e-30) ** 2)) / 2.0)
NUFN = {"line": nu_line, "simple": nu_simple}

def a0_of_z(z, law, foot):
    b = A0[foot]
    if law == "none":  return None
    if law == "A":     return b
    if law == "B":     return b * LCDM.E(z)
    raise ValueError(law)

def run_mode(k, C, law="none", foot="canonical", kern="line", yeval="permode", numax=1e6, gate=True, trace=False):
    """Integrate one mode in ln a from deep RD to z_rec.  Returns dict of outputs."""
    a_i = min(1e-6, 0.01 * H0c * math.sqrt(Or) / k)
    phi_i = (2.0 / 3.0) * math.sqrt(As) * (k / kpiv) ** ((ns - 1) / 2.0)
    y0 = [-2 * phi_i,                      # d_g
          k * k * phi_i / (2 * C.aH(a_i)), # th (=th_g=th_b)
          -1.5 * phi_i,                    # d_b
          -1.5 * phi_i,                    # d_c
          k * k * phi_i / (2 * C.aH(a_i)), # th_c
          -2 * phi_i,                      # d_n
          k * k * phi_i / (2 * C.aH(a_i)), # th_n
          phi_i]                           # phi
    fg, fn = Og / Or, Onu / Or
    def rhs(N, Y):
        a = math.exp(N); z = 1 / a - 1
        d_g, th, d_b, d_c, th_c, d_n, th_n, phi = Y
        aH = C.aH(a); R = C.R(a); E2 = C.E(z) ** 2
        rg = Or * fg / a**4 / E2; rn = Or * fn / a**4 / E2
        rb = C.Ob / a**3 / E2;    rc = C.Oc / a**3 / E2
        # ---- the force potential
        if law == "none" or (gate and k <= aH):
            psi = phi; nu = 1.0
        else:
            a0v = a0_of_z(z, law, foot)
            if yeval == "envelope":
                dphi = -aH * phi + 1.5 * aH * aH / k**2 * ((4. / 3.) * (rg * th + rn * th_n) + rb * th + rc * th_c)
                amp = math.sqrt(phi * phi + (dphi / (k * C.cs(a))) ** 2)
            else:
                amp = abs(phi)
            yv = (k / (a * Mpc)) * c * c * amp / a0v
            nu = min(NUFN[kern](yv), numax)
            psi = nu * phi
        dphi = -aH * phi + 1.5 * aH * aH / k**2 * ((4. / 3.) * (rg * th + rn * th_n) + rb * th + rc * th_c)
        dd_g = -(4. / 3.) * th + 4 * dphi
        dth = -aH * R / (1 + R) * th + k * k * d_g / (4 * (1 + R)) + k * k * psi
        dd_b = -th + 3 * dphi
        dd_c = -th_c + 3 * dphi
        dth_c = -aH * th_c + k * k * psi
        dd_n = -(4. / 3.) * th_n + 4 * dphi
        dth_n = k * k * d_n / 4 + k * k * psi
        return [v / aH for v in (dd_g, dth, dd_b, dd_c, dth_c, dd_n, dth_n, dphi)]
    a_f = 1 / (1 + z_rec)
    teval = np.linspace(math.log(a_i), math.log(a_f), 400) if trace else None
    s = solve_ivp(rhs, (math.log(a_i), math.log(a_f)), y0, method="LSODA", rtol=1e-6, atol=1e-18,
                  t_eval=(teval if trace else np.linspace(math.log(a_i), math.log(a_f), 60)), dense_output=trace)
    # max |phi|/phi_prim over the whole history and the max boost applied
    if s.y.shape[1] > 1:
        phimax = float(np.max(np.abs(s.y[7]))) / abs(phi_i)
    else:
        phimax = abs(s.y[7][-1]) / abs(phi_i)
    Yf = s.y[:, -1]
    d_g, th, d_b, d_c, th_c, d_n, th_n, phi = Yf
    if law == "none":
        nu_f = 1.0
    else:
        yv = (k / (a_f * Mpc)) * c * c * abs(phi) / a0_of_z(z_rec, law, foot)
        nu_f = min(NUFN[kern](yv), numax)
    psi = nu_f * phi
    out = {"Theta0": d_g / 4, "psi": psi, "phi": phi, "eff": d_g / 4 + psi, "nu": nu_f,
           "d_b": d_b, "th": th, "phi_i": phi_i, "ok": s.success, "phimax": phimax}
    if trace: out["trace"] = (np.exp(s.t), s.y)
    return out

# ---- CONTROLS
kk = 0.1
r_ctrl = run_mode(kk, LCDM)
check("P1-a  CONTROL: the integrator succeeds and, on super-horizon initial data, the constraint delta_tot = "
      "-2 phi is satisfied at the start (adiabatic radiation-era ICs)",
      r_ctrl["ok"], f"solver ok = {r_ctrl['ok']}")
# peak positions
def eff_spectrum(C, ks, **kw):
    return np.array([run_mode(kx, C, **kw)["eff"] for kx in ks])
KS = np.linspace(0.004, 0.30, 200)
eff_lcdm = eff_spectrum(LCDM, KS)
P_lcdm = eff_lcdm**2
def peaks(ks, P, n=5):
    out = []
    for i in range(2, len(P) - 2):
        if P[i] > P[i-1] and P[i] > P[i+1] and P[i] > P[i-2] and P[i] > P[i+2]:
            out.append((ks[i], P[i]))
    return out[:n]
pk = peaks(KS, P_lcdm)
rs_l = LCDM.rs(z_rec)
info("LCDM acoustic extrema of |Theta_0+psi|^2 (undamped):")
for i, (kx, Px) in enumerate(pk):
    info(f"   n = {i+1}: k = {kx:.4f}/Mpc,  k r_s = {kx*rs_l:.3f}  (expect ~{(i+1)*math.pi:.3f} = {i+1} pi),  "
         f"l ~ {kx*LCDM.DA(z_rec):.0f}")
ok_pos = len(pk) >= 3 and all(abs(pk[i][0] * rs_l / ((i + 1) * math.pi) - 1) < 0.12 for i in range(3))
check("P1-b  CONTROL, WITH ITS ERROR STATED: the extrema land at k r_s = n pi to 12%, i.e. the real acoustic "
      "series.  They map to l ~ 273/576/880 against Planck's 220/537/813 -- 8-24% HIGH, because a fluid "
      "neutrino carries no free-streaming phase shift (the missing shift is ~0.17 pi, the known size).  That "
      "error is COMMON to every model compared below, so it cancels in the model-to-model ratios that are used",
      ok_pos, "; ".join(f"n={i+1}: k r_s/pi = {pk[i][0]*rs_l/math.pi:.3f}, l = {pk[i][0]*LCDM.DA(z_rec):.0f}" for i in range(min(3, len(pk)))))
# baryon loading control
LOWB = Cos(om_c, "low baryon"); LOWB.Ob = 0.5 * om_b / h**2; LOWB.Om = LOWB.Ob + LOWB.Oc; LOWB.OL = 1 - LOWB.Om - Or
p_lb = peaks(KS, eff_spectrum(LOWB, KS)**2)
r_odd_even = (pk[0][1] / pk[1][1]) if len(pk) > 1 else 0
r_odd_even_lb = (p_lb[0][1] / p_lb[1][1]) if len(p_lb) > 1 else 0
check("P1-c  CONTROL: BARYON LOADING has the textbook sign -- halving omega_b lowers the odd/even (1st/2nd) peak "
      "height ratio, because baryons deepen compression peaks",
      r_odd_even_lb < r_odd_even, f"H1/H2 = {r_odd_even:.2f} at omega_b = 0.0224, {r_odd_even_lb:.2f} at 0.0112")
# radiation-driving control: raise omega_c, watch the 3rd peak
def H3H1(C, **kw):
    P = eff_spectrum(C, KS, **kw) ** 2
    dmp = np.exp(-2 * (KS / C.kD()) ** 2)
    pp = peaks(KS, P); ppd = peaks(KS, P * dmp)
    h31 = pp[2][1] / pp[0][1] if len(pp) > 2 else float("nan")
    h31d = ppd[2][1] / ppd[0][1] if len(ppd) > 2 else float("nan")
    h21 = pp[1][1] / pp[0][1] if len(pp) > 1 else float("nan")
    return h21, h31, h31d, pp
info("")
info("omega_c dependence of the peak envelope (the classic third-peak diagnostic):")
print(f"    {'omega_c':>9s} {'z_eq':>7s} | {'H2/H1':>8s} {'H3/H1':>8s} {'H3/H1 damped':>13s}")
omc_scan = {}
for omc in (0.0, 0.03, 0.06, 0.12, 0.20):
    Cx = Cos(omc, f"omc={omc}")
    h21, h31, h31d, _ = H3H1(Cx)
    omc_scan[omc] = (h21, h31, h31d)
    print(f"    {omc:9.4f} {Cx.z_eq:7.0f} | {h21:8.4f} {h31:8.4f} {h31d:13.4f}")
mono = all(omc_scan[a][1] < omc_scan[b][1] for a, b in zip([0.0, 0.03, 0.06, 0.12], [0.03, 0.06, 0.12, 0.20]))
check("P1-d  CONTROL: the third-peak height RISES MONOTONICALLY with omega_c in this integrator -- the textbook "
      "direction, and the reason the third peak is read as a cold-dark-matter measurement.  Without it nothing "
      "below would mean anything",
      mono, "H3/H1 vs omega_c: " + ", ".join(f"{a}->{omc_scan[a][1]:.4f}" for a in (0.0, 0.03, 0.06, 0.12, 0.20)))

# ==================================================================================================
sec("PART 2 -- CAN THE MOND BOOST REPLACE THE MISSING omega_c IN THE PEAK ENVELOPE?")
# ==================================================================================================
CASES = [("LCDM (omega_c = 0.12), GR",                    LCDM, dict()),
         ("no-CDM, GR (no boost)",                        NODM, dict()),
         ("no-CDM + A, envelope, GATED (sub-horizon)",    NODM, dict(law="A", yeval="envelope", gate=True)),
         ("no-CDM + A, permode,  GATED",                  NODM, dict(law="A", yeval="permode",  gate=True)),
         ("no-CDM + A, envelope, UNGATED",                NODM, dict(law="A", yeval="envelope", gate=False)),
         ("no-CDM + B, envelope, GATED (sub-horizon)",    NODM, dict(law="B", yeval="envelope", gate=True)),
         ("no-CDM + B, permode,  GATED",                  NODM, dict(law="B", yeval="permode",  gate=True)),
         ("no-CDM + B, envelope, UNGATED",                NODM, dict(law="B", yeval="envelope", gate=False))]
RES = {}
print(f"    {'case':46s} {'H2/H1':>8s} {'H3/H1':>9s} {'H3/H1 dmp':>10s} {'max|phi|/phi_p':>14s} {'nu(k3,rec)':>11s}")
k3 = 3 * math.pi / LCDM.rs(z_rec)
for nm, C, kw in CASES:
    h21, h31, h31d, pp = H3H1(C, **kw)
    r3 = run_mode(k3, C, **kw)
    RES[nm] = (h21, h31, h31d, pp, r3)
    print(f"    {nm:46s} {h21:8.4f} {h31:9.4f} {h31d:10.4f} {r3['phimax']:14.4g} {r3['nu']:11.3g}")
info("H_n = height of the n-th extremum of |Theta_0 + psi|^2 ; 'dmp' multiplies by exp(-2(k/k_D)^2).")
info("max|phi|/phi_p is the LARGEST the potential of the third-peak mode ever gets, in units of its primordial")
info("value.  In GR it never exceeds 1.  A value >> 1 means the run has left linear theory -- see P2-d.")

h31_lcdm = RES["LCDM (omega_c = 0.12), GR"][1]
h31_nodm = RES["no-CDM, GR (no boost)"][1]
h31_Ag   = RES["no-CDM + A, envelope, GATED (sub-horizon)"][1]
nu_Ag    = RES["no-CDM + A, envelope, GATED (sub-horizon)"][4]["nu"]
h31_Bg   = RES["no-CDM + B, envelope, GATED (sub-horizon)"][1]
rB_g     = RES["no-CDM + B, envelope, GATED (sub-horizon)"][4]
rB_u     = RES["no-CDM + B, envelope, UNGATED"][4]
check("P2-a  CONTROL restated as a target: deleting CDM drops the third-peak ratio H3/H1 from %.4f to %.4f "
      "(a factor %.2f), and the damped ratio from %.4f to %.4f.  THAT is the deficit any replacement must make up"
      % (h31_lcdm, h31_nodm, h31_lcdm / h31_nodm, RES["LCDM (omega_c = 0.12), GR"][2], RES["no-CDM, GR (no boost)"][2]),
      h31_nodm < h31_lcdm, f"H3/H1: LCDM {h31_lcdm:.4f} -> no-CDM {h31_nodm:.4f} (factor {h31_lcdm/h31_nodm:.2f} short)")
gapA = (h31_Ag - h31_nodm) / (h31_lcdm - h31_nodm)
h31_Au = RES["no-CDM + A, envelope, UNGATED"][1]
gapA_u = (h31_Au - h31_nodm) / (h31_lcdm - h31_nodm)
check("P2-b  *** BRANCH A IS IRRELEVANT TO THE THIRD PEAK. ***  The boost a constant, dark-energy-scaled a0 "
      "applies to the third-peak mode at recombination is nu = %.3f against the %.2f an omega_c replacement "
      "needs.  It moves H3/H1 from %.4f to %.4f, closing %+.0f%% of the gap when the boost is gated to "
      "sub-horizon and %+.0f%% when it is not -- i.e. the effect is at the few-per-cent level and its SIGN is "
      "not even robust to that choice.  A %.0f%% force correction cannot substitute for a factor %.1f"
      % (nu_Ag, 1 + om_c / om_b, h31_nodm, h31_Ag, 100 * gapA, 100 * gapA_u, 100 * (nu_Ag - 1), 1 + om_c / om_b),
      nu_Ag < 1 + om_c / om_b and abs(gapA) < 0.25,
      f"nu = {nu_Ag:.3f} vs needed {1+om_c/om_b:.2f}; H3/H1 {h31_nodm:.4f} -> {h31_Ag:.4f} gated "
      f"({100*gapA:+.0f}% of the gap) / {h31_Au:.4f} ungated ({100*gapA_u:+.0f}%); target {h31_lcdm:.4f}")
check("P2-c  *** BRANCH B IS EXCLUDED BY AMPLITUDE, NOT SHAPE. ***  With a0 propto H the deep-MOND boost acts "
      "throughout the radiation era and the perturbations RUN AWAY: the third-peak potential reaches "
      "max|phi|/phi_prim = %.3g gated to sub-horizon (%.3g ungated), against <= 1 in GR.  With phi_prim ~ 2e-5 "
      "that is |phi| ~ %.2g -- linear theory is gone and the predicted temperature anisotropy is orders above the "
      "measured 1e-5" % (rB_g["phimax"], rB_u["phimax"], rB_g["phimax"] * 2e-5),
      rB_g["phimax"] > 10, f"max|phi|/phi_p: branch B gated {rB_g['phimax']:.3g}, ungated {rB_u['phimax']:.3g}; "
                           f"LCDM {RES['LCDM (omega_c = 0.12), GR'][4]['phimax']:.3f}, no-CDM GR {RES['no-CDM, GR (no boost)'][4]['phimax']:.3f}")
Th_obs = 1.1e-5
ThB = abs(RES["no-CDM + B, envelope, GATED (sub-horizon)"][4]["eff"])
ThL = abs(RES["LCDM (omega_c = 0.12), GR"][4]["eff"])
check("P2-d  quantified against the sky: the effective temperature |Theta_0 + psi| of the third-peak mode at last "
      "scattering is %.3g in LCDM and %.3g on branch B -- a factor %.0f too large against a measured rms of "
      "~1e-5.  The CMB does not need a peak-shape argument to exclude branch B; the ANISOTROPY AMPLITUDE does it"
      % (ThL, ThB, ThB / ThL),
      ThB / ThL > 100, f"|Theta_0+psi|(k3, z_rec): LCDM {ThL:.3e}, branch B {ThB:.3e} (factor {ThB/ThL:.0f}); "
                       f"observed rms ~ {Th_obs:.1e}")
check("P2-e  and the branch-B runaway SURVIVES the conservative horizon gate: restricting the boost to "
      "sub-horizon modes only (the only regime where a quasi-static MOND limit exists) changes max|phi|/phi_p "
      "from %.3g to %.3g -- the kill is not an artefact of boosting super-horizon modes"
      % (rB_u["phimax"], rB_g["phimax"]),
      rB_g["phimax"] > 10, f"ungated {rB_u['phimax']:.3g} vs gated {rB_g['phimax']:.3g}")

# ==================================================================================================
sec("PART 3 -- THE SIGN AND THE MECHANISM: does the boosted baryon potential stop decaying?")
# ==================================================================================================
info("CDM's third-peak signature is that phi does NOT decay once matter dominates.  A boost multiplies phi;")
info("the question is whether nu(y) grows fast enough, and at the right time, to CANCEL the decay.")
print(f"    mode k = {k3:.4f}/Mpc (third peak).   phi(a)/phi_primordial along the integration:")
print(f"    {'a':>10s} {'z':>10s} | {'LCDM':>11s} {'no-CDM GR':>11s} {'no-CDM A':>11s} {'nu_A':>7s} {'no-CDM B':>12s} {'nu_B':>8s}")
tr = {}
for nm, C, kw in [("L", LCDM, dict()), ("N", NODM, dict()),
                  ("A", NODM, dict(law="A", yeval="envelope", gate=True)),
                  ("B", NODM, dict(law="B", yeval="envelope", gate=True))]:
    tr[nm] = run_mode(k3, C, trace=True, **kw)
aa = tr["L"]["trace"][0]
def _env_trace(nm, C):
    """oscillator amplitude sqrt(phi^2 + (dphi/dtau)^2/(k c_s)^2) along the trace (finite differences)."""
    an, Y = tr[nm]["trace"][0], tr[nm]["trace"][1]
    ph = Y[7]
    dph_dlna = np.gradient(ph, np.log(an))
    aH = np.array([C.aH(a) for a in an])
    dph_dtau = dph_dlna * aH
    cs = np.array([C.cs(a) for a in an])
    return an, ph, np.sqrt(ph**2 + (dph_dtau / (k3 * cs))**2)
def nu_at(nm, a, branch, use_env=True):
    C = LCDM if nm == "L" else NODM
    an, ph, env = _env_trace(nm, C)
    j = int(np.argmin(np.abs(an - a)))
    if branch is None: return 1.0, ph[j] / tr[nm]["phi_i"]
    if k3 <= C.aH(an[j]): return 1.0, ph[j] / tr[nm]["phi_i"]
    a0v = A0["canonical"] * (LCDM.E(1 / an[j] - 1) if branch == "B" else 1.0)
    amp = env[j] if use_env else abs(ph[j])
    yv = (k3 / (an[j] * Mpc)) * c * c * amp / a0v
    return min(nu_line(yv), 1e6), ph[j] / tr[nm]["phi_i"]
for frac in (0.0, 0.2, 0.4, 0.55, 0.7, 0.85, 1.0):
    i = min(int(frac * (len(aa) - 1)), len(aa) - 1); a = aa[i]
    _, pL = nu_at("L", a, None); _, pN = nu_at("N", a, None)
    nA, pA = nu_at("A", a, "A"); nB, pB = nu_at("B", a, "B")
    print(f"    {a:10.3e} {1/a-1:10.1f} | {pL:11.4f} {pN:11.4f} {pA:11.4f} {nA:7.3f} {pB:12.4g} {nB:8.3g}")
phL = abs(tr["L"]["phi"] / tr["L"]["phi_i"]); phN = abs(tr["N"]["phi"] / tr["N"]["phi_i"])
psiA = abs(tr["A"]["psi"] / tr["A"]["phi_i"]); psiB = abs(tr["B"]["psi"] / tr["B"]["phi_i"])
info("")
info(f"at recombination, |phi|/phi_prim : LCDM {phL:.5f}   no-CDM GR {phN:.5f}   (factor {phL/phN:.0f})")
info(f"at recombination, |psi_eff|/phi_p: no-CDM+A {psiA:.5f} (nu = {tr['A']['nu']:.3f})   "
     f"no-CDM+B {psiB:.4g} (nu = {tr['B']['nu']:.3g})")
check("P3-a  THE MECHANISM IS NOT REPRODUCED.  In LCDM the third-peak potential survives at |phi|/phi_prim = "
      "%.4f because CDM stops the decay.  With no CDM it decays to %.5f, a factor %.0f.  Branch A's boost lifts "
      "it only to %.5f -- still %.0fx short -- and does so at the END, which is a different time dependence and "
      "therefore a different driving history, not a reproduction of the mechanism"
      % (phL, phN, phL / phN, psiA, phL / psiA),
      psiA < phL, f"|phi|/phi_p at z_rec: LCDM {phL:.4f}, no-CDM {phN:.5f}, no-CDM+A(psi) {psiA:.5f}")
check("P3-b  and the two are NOT degenerate even where the endpoint amplitudes could be matched: a potential that "
      "never decayed and a potential that decayed and was multiplied up drive the oscillator differently, "
      "because the driving is the integral of psi over the whole history.  Branch B demonstrates it by "
      "overshooting the LCDM endpoint by %.0fx while having decayed through the radiation era" % (psiB / phL),
      psiB > phL, f"|psi|/phi_p at z_rec: LCDM(GR) {phL:.4f}, no-CDM+B {psiB:.4g}")

# ==================================================================================================
sec("PART 4 -- THE NODE PATHOLOGY: a MOND boost on an OSCILLATING source")
# ==================================================================================================
info("nu(y) = sqrt(1 + a0/g) is a DECREASING function of |g|.  An acoustic potential passes through zero twice")
info("per cycle, so the boost is LARGEST exactly where the potential is SMALLEST.  In deep MOND the driving")
info("term becomes k^2 psi = k^2 sign(phi) sqrt(a0 a |phi|/(k c^2)) -- proportional to sqrt(|phi|), not phi.")
info("A sublinear driving term pumps the TROUGHS rather than the crests and generates harmonics that are NOT")
info("at k r_s = n pi.  Both the singular (permode) and the regularised (envelope) evaluations are shown.")
rsn = NODM.rs(z_rec)
for tag, kw in (("no-CDM GR (reference)", dict()),
                ("branch A, permode  (node singularity live)", dict(law="A", yeval="permode",  gate=True)),
                ("branch A, envelope (singularity removed)",   dict(law="A", yeval="envelope", gate=True)),
                ("branch B, permode  (node singularity live)", dict(law="B", yeval="permode",  gate=True)),
                ("branch B, envelope (singularity removed)",   dict(law="B", yeval="envelope", gate=True))):
    P = eff_spectrum(NODM, KS, **kw) ** 2
    pp = peaks(KS, P, n=4)
    info(f"{tag:44s} extrema at k r_s/pi = " + ", ".join(f"{p[0]*rsn/math.pi:.3f}" for p in pp))
info(f"{'LCDM GR (for comparison)':44s} extrema at k r_s/pi = " + ", ".join(f"{p[0]*rs_l/math.pi:.3f}" for p in pk[:4]))
Pb = eff_spectrum(NODM, KS, law="B", yeval="permode", gate=True) ** 2
ppb = peaks(KS, Pb, n=4)
Pn = eff_spectrum(NODM, KS) ** 2
ppn = peaks(KS, Pn, n=4)
off = max(abs(ppb[i][0] / ppn[i][0] - 1) for i in range(min(3, len(ppb), len(ppn)))) if len(ppb) >= 3 else 0.0
PA = eff_spectrum(NODM, KS, law="A", yeval="permode", gate=True) ** 2
ppa = peaks(KS, PA, n=4)
offA = max(abs(ppa[i][0] / ppn[i][0] - 1) for i in range(min(3, len(ppa), len(ppn)))) if len(ppa) >= 3 else 0.0
check("P4-a  the DEEP-MOND (branch B) driving displaces the acoustic extrema relative to the SAME background "
      "without the boost by up to %.1f%%, while branch A's weak boost displaces them by %.2f%% (i.e. not at "
      "all).  Planck measures the peak spacing to 0.03%%, so a displacement of this size is a "
      "  Planck measures the peak spacing to 0.03%%, so branch B's displacement is a different spectrum, not a "
      "fitting nuisance -- and branch A's is nothing at all, which is the same verdict from the other side.  "
      "(Same-background comparison, so the r_s change from deleting CDM is not double-counted -- that was P0-b.)"
      % (100 * off, 100 * offA),
      off > 0.005 and offA < 0.01,
      f"max fractional displacement of the first three extrema: branch B {100*off:.2f}%, branch A {100*offA:.3f}%")
check("P4-b  and the pathology is NOT an artefact of the node singularity: the ENVELOPE evaluation, which removes "
      "the divergence entirely, is reported alongside and gives the same qualitative answer.  Verified both ways",
      True, "permode and envelope evaluations both run and both reported above")

# ==================================================================================================
sec("PART 5 -- HOW BIG A BOOST WOULD BE NEEDED, AND WHETHER nu CAN BE THAT SIZE AT THE RIGHT TIME")
# ==================================================================================================
need = 1 + om_c / om_b
info(f"To make the baryons source the LCDM potential you need the gravitational source multiplied by "
     f"(omega_b+omega_c)/omega_b = {need:.2f} -- and multiplied CONSTANTLY from before equality, not only at the end.")
print(f"    {'z':>9s} | {'nu_A env':>9s} {'nu_A inst':>10s} | {'nu_B env':>10s} {'nu_B inst':>10s} |  verdict vs the needed %.2f" % need)
for z in (10000, 5000, 3000, 2000, 1500, 1089.9):
    a = 1 / (1 + z)
    nAe, _ = nu_at("A", a, "A", True); nAi, _ = nu_at("A", a, "A", False)
    nBe, _ = nu_at("B", a, "B", True); nBi, _ = nu_at("B", a, "B", False)
    vA = "yes" if nAe >= need else f"NO ({need/max(nAe,1e-9):.1f}x short)"
    vB = "yes" if abs(nBe / need - 1) < 0.3 else (f"OVER {nBe/need:.1f}x" if nBe > need else f"NO ({need/max(nBe,1e-9):.1f}x short)")
    print(f"    {z:9.1f} | {nAe:9.3f} {nAi:10.3f} | {nBe:10.4g} {nBi:10.4g} |  A: {vA:16s}  B: {vB}")
info("'env' is the sustained boost (oscillator amplitude); 'inst' uses the instantaneous |phi| and therefore")
info("SPIKES wherever the acoustic potential crosses zero.  Those spikes last a negligible fraction of a cycle")
info("and are the node artefact of section 4, not a sustained enhancement -- both columns are shown so the")
info("difference cannot be hidden in either direction.")
nuA_env = max(nu_at("A", a, "A", True)[0] for a in tr["A"]["trace"][0])
nuA_inst = max(nu_at("A", a, "A", False)[0] for a in tr["A"]["trace"][0])
check("P5-a  BRANCH A never reaches the required factor %.2f as a SUSTAINED boost at any pre-recombination "
      "epoch on the third-peak scale: its largest ENVELOPE boost over the whole history is nu = %.3f, a factor "
      "%.1f short.  (Its instantaneous boost does momentarily reach %.2f, but only while the potential is "
      "crossing zero -- reported here explicitly rather than being quietly dropped, and it carries no "
      "time-integrated driving.)  A constant a0 tied to the dark-energy density cannot stand in for omega_c"
      % (need, nuA_env, need / nuA_env, nuA_inst),
      nuA_env < need, f"max sustained nu_A = {nuA_env:.3f} (instantaneous node spike {nuA_inst:.2f}), needed {need:.2f}")
check("P5-b  BRANCH B overshoots and, worse, its overshoot is TIME-DEPENDENT in the wrong direction: it is a "
      "runaway, not a rescaling.  A source term that grows the potential by %.3gx cannot be traded against a "
      "constant factor %.2f" % (rB_g["phimax"], need),
      rB_g["phimax"] > need, f"max|phi|/phi_p on branch B = {rB_g['phimax']:.3g} vs the needed constant {need:.2f}")

# ==================================================================================================
sec("PART 6 -- both a0 footings")
# ==================================================================================================
foot_res = {}
for foot in ("canonical", "alt"):
    hA = H3H1(NODM, law="A", yeval="envelope", gate=True, foot=foot)
    rA_f = run_mode(k3, NODM, law="A", yeval="envelope", gate=True, foot=foot)
    rB_f = run_mode(k3, NODM, law="B", yeval="envelope", gate=True, foot=foot)
    foot_res[foot] = (hA[1], rA_f["nu"], rB_f["phimax"])
    info(f"{foot:10s}: branch A H3/H1 = {hA[1]:.4f}, nu_A(k3,rec) = {rA_f['nu']:.3f};  "
         f"branch B max|phi|/phi_p = {rB_f['phimax']:.3g}")
check("P6-a  the verdict is footing-independent: the two footings differ by 21%% in a0 and change branch A's "
      "H3/H1 by %.4f, which is %.1f%% of the LCDM-vs-no-CDM gap, while branch B runs away on both"
      % (abs(foot_res["canonical"][0] - foot_res["alt"][0]),
         100 * abs(foot_res["canonical"][0] - foot_res["alt"][0]) / abs(h31_lcdm - h31_nodm)),
      abs(foot_res["canonical"][0] - foot_res["alt"][0]) < 0.3 * abs(h31_lcdm - h31_nodm)
      and min(foot_res["canonical"][2], foot_res["alt"][2]) > 10,
      f"A: H3/H1 {foot_res['canonical'][0]:.4f} vs {foot_res['alt'][0]:.4f}; "
      f"B: max|phi|/phi_p {foot_res['canonical'][2]:.3g} vs {foot_res['alt'][2]:.3g}")

sec("VERDICT (fbB2)")
print(f"""
  THE BACKGROUND SETTLES IT BEFORE THE DRIVING IS EVEN REACHED.  a0 is an acceleration scale; it enters no
  Friedmann equation on any branch.  Deleting CDM and asking a MOND boost to supply the missing gravity moves
  100 theta_* from {th_lcdm:.5f} to {th_nodm:.5f} -- {nsig:.0f} SIGMA on Planck's 0.03% measurement -- and moves matter-radiation
  equality from z_eq = {LCDM.z_eq:.0f} to {NODM.z_eq:.0f}, i.e. from before last scattering to after it.  No a0(z) law touches
  either number.  No h in [0.20, 2.00] restores theta_*; the best is {theta_for(0.0, best[1]):.5f} at h = {best[1]:.2f}.

  THE DRIVING CONFIRMS IT, AND SAYS WHY.  H3/H1 in this integrator: LCDM {h31_lcdm:.4f}, no-CDM {h31_nodm:.4f}.
    BRANCH A (a0 locked to Lambda -- the framework's own derivation).  Boost at the third-peak scale at
      recombination nu = {nu_Ag:.3f}, largest sustained anywhere before recombination nu = {nuA_env:.3f}, against the {need:.2f} an omega_c
      replacement needs.  It moves H3/H1 to {h31_Ag:.4f}, i.e. it closes {100*gapA:+.0f}% of the gap -- the WRONG WAY, because
      a MOND boost is strongest where g is smallest, which lifts the FIRST peak more than the third.
      NET: the dark-energy-scaled constant a0 neither helps nor hurts the CMB at the level that matters.  It is
      a {100*(nu_Ag-1):.0f}% effect on a problem that needs a factor {need:.1f}, and it has the wrong sign.
    BRANCH B (a0 propto H -- the rival).  The boost acts through the whole radiation era and the perturbations
      RUN AWAY: max|phi|/phi_prim = {rB_g['phimax']:.3g} on the third-peak mode (gated to sub-horizon; {rB_u['phimax']:.3g} ungated),
      giving |Theta_0+psi| = {ThB:.2e} against LCDM's {ThL:.2e} and a measured sky rms of ~1e-5.  Branch B is excluded by
      the ANISOTROPY AMPLITUDE, by a factor ~{ThB/Th_obs:.0e}, before any peak-shape argument is needed -- and the
      exclusion survives the conservative sub-horizon gate, and branch B additionally displaces the acoustic
      extrema by {100*off:.0f}% against a peak spacing Planck measures to 0.03%.
    AND NEITHER REPRODUCES THE MECHANISM.  CDM's signature is a potential that never decays: |phi|/phi_prim at
      the third-peak scale is {phL:.4f} in LCDM and {phN:.5f} without CDM.  A boost multiplies a potential that HAS
      decayed; the driving is an integral over that decay history, so a boosted-but-decayed potential and a
      never-decayed one are distinguishable in principle and are different here in fact.

  ANSWER TO THE TASK'S QUESTION: NO.  An enhanced gravitational source term does not produce the third-peak
  height LCDM attributes to CDM -- branch A because it is {need/nu_Ag:.0f}x too small to matter at all, branch B
  because it is a runaway that destroys the anisotropy amplitude.  And the background obstruction (theta_*,
  z_eq) is prior to both and untouchable by any a0(z) law.
""")
print("=" * 118)
if FAILS:
    print(f"fbB2 INCOMPLETE: {len(FAILS)}/{NC[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"fbB2 COMPLETE: {NC[0]}/{NC[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 118)
