#!/usr/bin/env python3
"""
L152 (part 2 of 2) -- THE SAME SECTOR AT LATE TIMES: sigma_8, P(k), the scale of 50% suppression, the
        Lyman-alpha forest, and an INDEPENDENT validation of the patched CLASS's time dependence.
=============================================================================================================
Part 1 (L152_running_cs2_cmb_boltzmann.py) showed the running-sound-speed fluid c_s^2 = c0 a^3 passes the CMB
across the L138 window (c0 = 1e-6 .. 3.21e-6).  Passing the CMB is necessary, not sufficient.  Here:

  0  VALIDATION OF THE PATCH'S TIME DEPENDENCE.  Part 1 verified the patched CLASS is bit-identical to stock
     with the running OFF; that says nothing about whether the running is implemented correctly.  So an
     independent sub-horizon two-fluid growth solver (pressureless baryons+cdm, dark fluid with an arbitrary
     c_s^2(a) Jeans term, written here from the equations, no CLASS input beyond the cosmological parameters)
     is compared with the patched CLASS's fluid and baryon transfer ratios at several k and z.
  1  TOTAL-MATTER P(k) (baryons + residual cdm + fluid, built from CLASS's transfer functions -- CLASS's own
     mPk/sigma8 contain only b+cdm, which here is 16% of the matter), sigma_8, and P/P_control at
     k = 0.1, 0.2, 0.3, 1, 3, 10 h/Mpc at z = 0 (and 0.1-0.3 h/Mpc at z = 0.5, the BOSS/DESI scales);
     the wavenumber k_50 at which the suppression reaches 50%.  Constant-c_s^2 alongside, for contrast.
  2  LYMAN-ALPHA (z = 2-4, k = 1-12 h/Mpc): the suppression of the TOTAL matter, of the FLUID, and of the
     BARYONS separately, against the suppression allowed by the thermal-WDM bound m > 5.3 keV (Irsic et al.
     2017) through the Viel et al. 2005 transfer function -- and a flat few-percent criterion.
     The two readings (total vs baryon) differ by more than an order of magnitude, and that fork is the
     honest state of the Lyman-alpha verdict (see LYA-*).

Setup exactly as part 1: patched classy from L152_class_running_cs2/site, fld with w0 = -1e-5, use_ppf = no,
recombination = recfast, Omega_fld h^2 = 0.1190 + omega_cdm = 0.001, Planck-2018-like otherwise, linear P(k).
POLARITY: each check ASSERTS a statement; PASS = true; every pass condition is a computed inequality.
"""
import os, sys, json, time
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, 'L152_class_running_cs2', 'site')
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)

print("=" * 112)
print("L152 (2/2) -- running-sound-speed dark fluid at late times: P(k), sigma_8, k_50, Lyman-alpha, validation")
print("=" * 112, flush=True)
if not os.path.isdir(SITE):
    print("  patched classy not built: run L152_class_running_cs2/build_patched_classy.sh first"); sys.exit(2)
sys.path.insert(0, SITE)
from classy import Class

h = 0.6736; om_b = 0.02237; om_c_res = 0.001; om_f = 0.1190
ZS = [0.0, 0.5, 2.0, 3.0, 4.0]
BASE = dict(output='mPk,mTk', omega_b=om_b, h=h, A_s=2.1e-9, n_s=0.9649, tau_reio=0.0544, N_ur=3.046, YHe=0.2454,
            recombination='recfast', non_linear='none', z_pk=','.join(str(z) for z in ZS), **{'P_k_max_h/Mpc': 30})
FLD = dict(omega_cdm=om_c_res, Omega_fld=om_f / h ** 2, w0_fld=-1e-5, wa_fld=0.0, use_ppf='no')
KGRID = np.logspace(-4, np.log10(29.0), 400)          # h/Mpc, for sigma_8 and the ratio tables

def run(extra, base=BASE):
    c = Class(); p = dict(base); p.update(extra); c.set(p); c.compute()
    bg = c.get_background(); zbg = bg['z']
    out = dict(sigma8_class=c.sigma8())
    for z in ZS:
        tr = c.get_transfer(z); kt = tr['k (h/Mpc)']
        i = np.argmin(np.abs(zbg - z))
        rb, rc = bg['(.)rho_b'][i], bg['(.)rho_cdm'][i]; rf = bg['(.)rho_fld'][i] if '(.)rho_fld' in bg else 0.0
        db, dc = tr['d_b'], tr['d_cdm']; df = tr['d_fld'] if 'd_fld' in tr else np.zeros_like(db)
        dm_mine = (rb * db + rc * dc) / (rb + rc)
        dtot = (rb * db + rc * dc + rf * df) / (rb + rc + rf)
        resid = np.abs(dm_mine / tr['d_m'] - 1)
        out[f'dm_check_{z}'] = float(np.max(resid[kt >= 1e-2]))
        out[f'dm_resid_{z}'] = [float(np.interp(np.log(kk), np.log(kt), resid)) for kk in (1e-3, 1e-2, 1e-1)]
        pk_class = np.array([c.pk(k * h, z) for k in KGRID])                     # (Mpc)^3, CLASS's b+cdm P(k)
        ratio_tot = np.interp(np.log(KGRID), np.log(kt), (dtot / tr['d_m']) ** 2)  # denominator: CLASS's own d_m
        out[f'k_{z}'] = kt; out[f'db_{z}'] = db; out[f'df_{z}'] = df; out[f'dtot_{z}'] = dtot; out[f'dm_{z}'] = dm_mine
        out[f'pk_b_{z}'] = pk_class; out[f'pk_tot_{z}'] = pk_class * ratio_tot
    c.struct_cleanup(); c.empty()
    return out

def sigma8(pk_tot):
    kk = KGRID * h; R = 8.0 / h; x = kk * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return float(np.sqrt(np.trapz(kk ** 2 * pk_tot * W ** 2 / (2 * np.pi ** 2), kk)))

def at(kgrid, arr, k): return float(np.interp(np.log(k), np.log(kgrid), arr))
def k_half(kgrid, ratio, level=0.5):
    """first k (increasing) where the ratio drops through 'level'; inf if never."""
    idx = np.where((ratio[:-1] >= level) & (ratio[1:] < level))[0]
    if len(idx) == 0: return float('inf')
    i = idx[0]
    return float(np.exp(np.interp(level, [ratio[i + 1], ratio[i]], [np.log(kgrid[i + 1]), np.log(kgrid[i])])))

sec("PART 0 -- runs: control, true LambdaCDM, the running window, and constant c_s^2 for contrast")
ctrl = run(dict(FLD, cs2_fld=0.0))
lcdm = run(dict(omega_cdm=0.1200))
rz = {z: ctrl[f'dm_resid_{z}'] for z in ZS}
decay_ok = all(rz[z][0] / rz[z][1] > 10 and rz[z][1] / rz[z][2] > 10 for z in ZS)
check("SETUP-0  the hand-built (rho_b d_b + rho_cdm d_cdm)/(rho_b+rho_cdm) reproduces CLASS's own d_m transfer "
      "to < 1e-5 for every k >= 0.01 h/Mpc at every z, and the residual below that is the expected large-scale "
      "GAUGE term (CLASS's d_m is the gauge-invariant comoving density, d_b/d_cdm are synchronous): it falls by "
      "> 10x per decade from k = 1e-3 to 1e-1 h/Mpc at every z.  So the density weights are the code's own; "
      "the total spectrum below uses CLASS's d_m as its denominator, and sigma_8/P(k) at k >= 0.01 carry no "
      "error from this",
      max(ctrl[f'dm_check_{z}'] for z in ZS) < 1e-5 and decay_ok,
      f"max |d_m(mine)/d_m(CLASS) - 1| (k >= 0.01) = {max(ctrl[f'dm_check_{z}'] for z in ZS):.1e}; residual at k = 1e-3/1e-2/1e-1 (z=0): "
      f"{rz[0.0][0]:.1e}/{rz[0.0][1]:.1e}/{rz[0.0][2]:.1e}; (z=3): {rz[3.0][0]:.1e}/{rz[3.0][1]:.1e}/{rz[3.0][2]:.1e}")
s8_ctrl = sigma8(ctrl['pk_tot_0.0']); s8_lcdm = sigma8(lcdm['pk_tot_0.0'])
check("SETUP-1  the TOTAL-matter sigma_8 of the c_s^2 = 0 fluid control equals that of a true LambdaCDM run "
      "(real CDM, no fluid) to < 0.5%, and my sigma_8 integral reproduces CLASS's own sigma8() for LambdaCDM "
      "to < 0.5%: the total-P(k) construction is validated at both ends",
      abs(s8_ctrl / s8_lcdm - 1) < 5e-3 and abs(s8_lcdm / lcdm['sigma8_class'] - 1) < 5e-3,
      f"sigma_8: control(total) {s8_ctrl:.4f}, LambdaCDM(total, mine) {s8_lcdm:.4f}, LambdaCDM (CLASS) {lcdm['sigma8_class']:.4f}; "
      f"CLASS's sigma8() of the control counts b+cdm only: {ctrl['sigma8_class']:.4f}")
dev_pk = float(np.max(np.abs(ctrl['pk_tot_0.0'] / lcdm['pk_tot_0.0'] - 1)[(KGRID > 0.01) & (KGRID < 10)]))
check("SETUP-2  and the control's total P(k, z=0) matches true LambdaCDM to < 1% for 0.01 < k < 10 h/Mpc",
      dev_pk < 1e-2, f"max |P_ctrl/P_LCDM - 1| = {dev_pk:.1e}")

C0_RUN = [1e-6, 1.8e-6, 3.21e-6]
RUN = {c0: run(dict(FLD, cs2_fld=c0, cs2_fld_p=3.0, cs2_fld_astar=1.0, cs2_fld_max=1.0)) for c0 in C0_RUN}
CONST = {c0: run(dict(FLD, cs2_fld=c0)) for c0 in (1e-6, 3.21e-6)}
print(f"    runs done [{time.time() - T0:.1f}s]")

sec("PART 1 -- INDEPENDENT VALIDATION of the running implementation: sub-horizon two-fluid growth solver vs CLASS")
CKMS = 299792.458; H0 = h / 2997.92458                     # Mpc^-1 (c = 1)
Om_b, Om_c, Om_f = om_b / h ** 2, om_c_res / h ** 2, om_f / h ** 2
Om_m = Om_b + Om_c + Om_f
Og = 2.4728e-5 / h ** 2 * (2.7255 / 2.7255) ** 4; Or = Og * (1 + 3.046 * 7. / 8. * (4. / 11.) ** (4. / 3.))
OL = 1 - Om_m - Or
f_f = Om_f / Om_m; f_p = (Om_b + Om_c) / Om_m
def E2(a): return Om_m / a ** 3 + Or / a ** 4 + OL
def dlnH_dlna(a): return 0.5 * (-3 * Om_m / a ** 3 - 4 * Or / a ** 4) / E2(a)
def Om_of_a(a): return Om_m / a ** 3 / E2(a)
def growth_ratio(k_hMpc, cs2_of_a, z_out, a_i=1e-2):
    """returns (delta_f/delta_f[cs2=0])^2 and (delta_p/delta_p[cs2=0])^2 at z_out, sub-horizon, linear."""
    k = k_hMpc * h
    def rhs(lna, y, cs2fun):
        a = np.exp(lna); df, dfp, dp, dpp = y
        fric = 2 + dlnH_dlna(a); src = 1.5 * Om_of_a(a) * (f_f * df + f_p * dp)
        J = cs2fun(a) * k ** 2 / (a * H0) ** 2 / E2(a)
        return [dfp, src - fric * dfp - J * df, dpp, src - fric * dpp]
    y0 = [1.0, 1.0, 1.0, 1.0]                                  # growing mode delta ~ a at a_i
    outs = []
    for fun in (cs2_of_a, lambda a: 0.0):
        sol = solve_ivp(rhs, [np.log(a_i), np.log(1.0 / (1 + z_out))], y0, args=(fun,), rtol=1e-8, atol=1e-12,
                        method='DOP853', dense_output=False)
        outs.append(sol.y[:, -1])
    return (outs[0][0] / outs[1][0]) ** 2, (outs[0][2] / outs[1][2]) ** 2
c0v = 1e-6; r1 = RUN[c0v]
print("  running c0 = 1e-6, c_s^2(a) = c0 a^3:   (P/P_ctrl) for the FLUID and for the BARYONS, solver vs CLASS")
print("      z     k[h/Mpc] |  fluid: solver   CLASS  |  baryon: solver   CLASS")
rows = []
for z in (0.0, 2.0, 3.0):
    for kk in (0.3, 0.5, 1.0, 2.0, 5.0, 10.0):
        sf, sb = growth_ratio(kk, lambda a: c0v * a ** 3, z)
        cf = at(r1[f'k_{z}'], (r1[f'df_{z}'] / ctrl[f'df_{z}']) ** 2, kk)
        cb = at(r1[f'k_{z}'], (r1[f'db_{z}'] / ctrl[f'db_{z}']) ** 2, kk)
        rows.append((z, kk, sf, cf, sb, cb))
        print(f"    {z:4.1f}   {kk:6.2f}   |   {sf:7.4f}   {cf:7.4f}  |    {sb:7.4f}   {cb:7.4f}")
band = [(sf, cf, sb, cb) for (_, _, sf, cf, sb, cb) in rows if cf > 0.3]
worst_f = max(abs(sf - cf) for sf, cf, _, _ in band); worst_b = max(abs(sb - cb) for _, _, sb, cb in band)
check("VAL-0  the independent solver reproduces the patched CLASS's FLUID suppression to within 0.05 (absolute, "
      "in P/P_ctrl) wherever the ratio exceeds 0.3, and the BARYON suppression to within 0.02: the running "
      "c_s^2 = c0 a^3 is implemented in CLASS with the right power of a and the right normalisation (a wrong "
      "exponent shifts these ratios by far more than this over z = 0-3)",
      worst_f < 0.05 and worst_b < 0.02, f"max |solver - CLASS|: fluid {worst_f:.3f}, baryon {worst_b:.3f} ({len(band)} cells with ratio > 0.3)")
# discriminating power of VAL-0: what would p = 2 or p = 4 have given at the same cells?
alt = {}
for p_alt in (2.0, 4.0):
    d = []
    for (z, kk, sf, cf, sb, cb) in rows:
        if cf > 0.3:
            sfa, _ = growth_ratio(kk, lambda a, p=p_alt: c0v * a ** p, z); d.append(abs(sfa - cf))
    alt[p_alt] = max(d)
check("VAL-1  the comparison is DISCRIMINATING: had CLASS implemented a^2 or a^4 instead of a^3, the solver "
      "(run with those exponents) would disagree with CLASS by > 0.1 in the same cells -- so VAL-0 is not a "
      "test that anything would pass",
      alt[2.0] > 0.1 and alt[4.0] > 0.1, f"max |solver(p=2) - CLASS(p=3)| = {alt[2.0]:.3f}; p=4: {alt[4.0]:.3f}")
# fluid vs baryon: the physics of the fork
print("  NOTE the fluid-vs-baryon asymmetry: once the fluid's Jeans term switches on, its own delta stops growing,\n"
      "  but the baryons keep falling into the (frozen, not erased) fluid potential and their linear delta\n"
      "  continues to grow almost as before -- so linear baryons are far less suppressed than the fluid.")

sec("PART 2 -- sigma_8, P(k)/P_control at z = 0 and 0.5, and the 50%-suppression scale")
def table(tag, r, z, ks):
    rt = r[f'pk_tot_{z}'] / ctrl[f'pk_tot_{z}']; rb = r[f'pk_b_{z}'] / ctrl[f'pk_b_{z}']
    rf = np.interp(np.log(KGRID), np.log(r[f'k_{z}']), (r[f'df_{z}'] / ctrl[f'df_{z}']) ** 2)
    print(f"  {tag:16s} z={z:3.1f}  total: " + " ".join(f"k{k:g}:{at(KGRID, rt, k):.4f}" for k in ks)
          + f" | k_50(total) {k_half(KGRID, rt):.3g}  k_50(fluid) {k_half(KGRID, rf):.3g}  k_50(baryon) {k_half(KGRID, rb):.3g} h/Mpc")
    return rt, rb, rf
RES = dict(sigma8=dict(control_total=s8_ctrl, lcdm_total=s8_lcdm, lcdm_class=lcdm['sigma8_class']), running={}, constant={}, lya={})
print(f"  sigma_8 (TOTAL matter, z=0): control {s8_ctrl:.4f}")
for c0, r in RUN.items():
    s8 = sigma8(r['pk_tot_0.0']); rt0, rb0, rf0 = table(f"run c0={c0:.2e}", r, 0.0, (0.1, 0.2, 0.3, 1, 3, 10))
    rt05, _, _ = table(f"run c0={c0:.2e}", r, 0.5, (0.1, 0.2, 0.3, 1))
    RES['running'][f'{c0:.3g}'] = dict(sigma8_total=s8, ds8=s8 / s8_ctrl - 1,
        z0_total={f'{k:g}': at(KGRID, rt0, k) for k in (0.1, 0.2, 0.3, 1, 3, 10)},
        z0_baryon={f'{k:g}': at(KGRID, rb0, k) for k in (0.1, 0.2, 0.3, 1, 3, 10)},
        z0_fluid={f'{k:g}': at(KGRID, rf0, k) for k in (0.1, 0.2, 0.3, 1, 3, 10)},
        z05_total={f'{k:g}': at(KGRID, rt05, k) for k in (0.1, 0.2, 0.3, 1)},
        k50_total_z0=k_half(KGRID, rt0), k50_fluid_z0=k_half(KGRID, rf0), k50_baryon_z0=k_half(KGRID, rb0))
    print(f"                    sigma_8(total) = {s8:.4f}  ({100 * (s8 / s8_ctrl - 1):+.1f}% vs control);  CLASS's b+cdm sigma8 = {r['sigma8_class']:.4f}")
for c0, r in CONST.items():
    s8 = sigma8(r['pk_tot_0.0']); rt0, rb0, rf0 = table(f"const c={c0:.2e}", r, 0.0, (0.1, 0.2, 0.3, 1, 3, 10))
    RES['constant'][f'{c0:.3g}'] = dict(sigma8_total=s8, ds8=s8 / s8_ctrl - 1,
        z0_total={f'{k:g}': at(KGRID, rt0, k) for k in (0.1, 0.2, 0.3, 1, 3, 10)}, k50_total_z0=k_half(KGRID, rt0))
    print(f"                    sigma_8(total) = {s8:.4f}  ({100 * (s8 / s8_ctrl - 1):+.1f}% vs control)")
R1, R2, R3 = (RES['running'][f'{c:.3g}'] for c in C0_RUN)
check("PK-0  THE INTENDED FEATURE IS THERE: at z = 0 the running fluid suppresses galaxy-scale total-matter "
      "power by half at k_50 = 0.4-0.8 h/Mpc across the window (P/P_ctrl < 0.35 at k = 1 h/Mpc, < 0.05 at "
      "10 h/Mpc), while the large scales survive: < 1.5% at k = 0.1 h/Mpc for c0 = 1e-6",
      all(0.3 < RES['running'][f'{c:.3g}']['k50_total_z0'] < 1.0 for c in C0_RUN) and R1['z0_total']['1'] < 0.35
      and R1['z0_total']['10'] < 0.05 and R1['z0_total']['0.1'] > 0.985,
      f"k_50 = {R1['k50_total_z0']:.2f}/{R2['k50_total_z0']:.2f}/{R3['k50_total_z0']:.2f} h/Mpc; c0=1e-6: P/P at k=0.1: {R1['z0_total']['0.1']:.4f}, "
      f"k=1: {R1['z0_total']['1']:.3f}, k=10: {R1['z0_total']['10']:.4f}")
check("PK-1  sigma_8 (total matter) moves DOWN by 2-8% across the window -- a shift current S8 measurements "
      "(weak lensing sits 3-8% below Planck) cannot exclude and might even welcome; it is NOT a kill and NOT "
      "a win, and the check only asserts the size: |dsigma_8/sigma_8| < 10% for every window value",
      all(abs(RES['running'][f'{c:.3g}']['ds8']) < 0.10 for c in C0_RUN),
      f"sigma_8 = {R1['sigma8_total']:.4f} ({100 * R1['ds8']:+.1f}%), {R2['sigma8_total']:.4f} ({100 * R2['ds8']:+.1f}%), "
      f"{R3['sigma8_total']:.4f} ({100 * R3['ds8']:+.1f}%) vs control {s8_ctrl:.4f}")
check("PK-2  the BOSS/DESI regime is touched at the few-percent level: at z = 0.5 the total P(k) is suppressed "
      "by < 2% at k = 0.1 h/Mpc and < 10% at k = 0.3 h/Mpc for c0 = 1e-6 (a shape distortion that full-shape "
      "analyses can probe but which this lane does not adjudicate)",
      R1['z05_total']['0.1'] > 0.98 and R1['z05_total']['0.3'] > 0.90,
      f"z=0.5, c0=1e-6: P/P at k=0.1: {R1['z05_total']['0.1']:.4f}, 0.2: {R1['z05_total']['0.2']:.4f}, 0.3: {R1['z05_total']['0.3']:.4f}")
Cc = RES['constant']['1e-06']
check("PK-3  CONTRAST -- the constant-c_s^2 (quadratic K) branch at the SAME c_s^2(today) = 1e-6 is dead on "
      "late-time structure alone: sigma_8 down by > 15% and P/P_ctrl < 0.05 at k = 1 h/Mpc (k_50 ~ 0.25 h/Mpc), "
      "confirming with a Boltzmann code what L129's growth solver found for p = 0",
      Cc['ds8'] < -0.15 and Cc['z0_total']['1'] < 0.05,
      f"const 1e-6: sigma_8 {Cc['sigma8_total']:.4f} ({100 * Cc['ds8']:+.1f}%), P/P(k=1) = {Cc['z0_total']['1']:.4f}, k_50 = {Cc['k50_total_z0']:.2f}")

sec("PART 3 -- LYMAN-ALPHA (z = 2-4, k = 1-12 h/Mpc): total vs fluid vs baryon suppression against the WDM allowance")
def T2_wdm(k_hMpc, m_keV, Om=Om_m, hh=h):
    """Viel et al. 2005 thermal-WDM transfer function squared (linear P suppression), nu = 1.12."""
    alpha = 0.049 * m_keV ** (-1.11) * (Om / 0.25) ** 0.11 * (hh / 0.7) ** 1.22      # Mpc/h
    nu = 1.12
    return (1 + (alpha * k_hMpc) ** (2 * nu)) ** (-10.0 / nu)
M_WDM = 5.3                                                         # keV, Irsic et al. 2017 (95%)
KL = [1.0, 2.0, 3.0, 5.0, 8.0, 10.0, 8.0 / h]
KCUT = [k for k in KL if k >= 8.0]                                  # where the forest constrains the cutoff
print(f"  allowance proxy: 1 - T^2_WDM(k) for m_WDM = {M_WDM} keV (the linear suppression the forest tolerates, z-independent):")
print("      k[h/Mpc]: " + "  ".join(f"{k:5.2f}" for k in KL))
print("      allowed : " + "  ".join(f"{1 - T2_wdm(k, M_WDM):5.3f}" for k in KL))
print("  the ratio 'suppression/allowed' is evaluated over k = 8-12 h/Mpc (0.07-0.1 s/km at z = 3-4), the range in\n"
      "  which the published bound is set by the cutoff shape.  At k <= 3 h/Mpc the WDM proxy 'allows' only\n"
      "  1e-4 .. 2e-3, far below any real forest sensitivity to a smooth suppression, so a max over all k would\n"
      "  be an artefact of the proxy, not of the data.  The full table is printed so both can be read.")
FLAT_TOL = 0.05
for c0, r in RUN.items():
    RES['lya'][f'{c0:.3g}'] = {}
    print(f"  running c0 = {c0:.2e}:  suppression 1 - P/P_ctrl")
    for z in (2.0, 3.0, 4.0):
        kt = r[f'k_{z}']
        sup_t = [1 - at(kt, (r[f'dtot_{z}'] / ctrl[f'dtot_{z}']) ** 2, k) for k in KL]
        sup_f = [1 - at(kt, (r[f'df_{z}'] / ctrl[f'df_{z}']) ** 2, k) for k in KL]
        sup_b = [1 - at(kt, (r[f'db_{z}'] / ctrl[f'db_{z}']) ** 2, k) for k in KL]
        allow = [1 - T2_wdm(k, M_WDM) for k in KL]
        Rt = max(s / a for s, a, k in zip(sup_t, allow, KL) if k in KCUT)
        Rb = max(s / a for s, a, k in zip(sup_b, allow, KL) if k in KCUT)
        RES['lya'][f'{c0:.3g}'][f'z{z:g}'] = dict(k=KL, total=sup_t, fluid=sup_f, baryon=sup_b, allowed=allow,
                                                  R_total=Rt, R_baryon=Rb,
                                                  max_total_k1_10=max(s for s, k in zip(sup_t, KL) if k <= 10),
                                                  max_baryon_k1_10=max(s for s, k in zip(sup_b, KL) if k <= 10))
        print(f"    z={z:g}  total : " + "  ".join(f"{s:5.3f}" for s in sup_t) + f"   (max/allowed over k=8-12 = {Rt:6.1f})")
        print(f"         fluid : " + "  ".join(f"{s:5.3f}" for s in sup_f))
        print(f"         baryon: " + "  ".join(f"{s:5.3f}" for s in sup_b) + f"   (max/allowed over k=8-12 = {Rb:6.2f})")
L1 = RES['lya']['1e-06']
check("LYA-0  TOTAL-MATTER READING (the quantity a WDM-style bound is placed on): at z = 3 and z = 4 the running "
      "fluid's total suppression at k = 5-10 h/Mpc exceeds the 5.3-keV WDM allowance by more than 5x for the "
      "SMALLEST window value c0 = 1e-6 -- and exceeds a flat 5% criterion at k = 10 h/Mpc.  In this reading "
      "the sector FAILS the forest decisively",
      L1['z3']['R_total'] > 5 and L1['z4']['R_total'] > 5 and L1['z3']['max_total_k1_10'] > FLAT_TOL,
      f"c0=1e-6: max(suppression/allowed) total: z=3 {L1['z3']['R_total']:.1f}x, z=4 {L1['z4']['R_total']:.1f}x; "
      f"total suppression at k=10, z=3: {L1['z3']['total'][KL.index(10.0)]:.2f}")
check("LYA-1  BARYON READING (linear gas, the quantity L129's growth-solver gate used): at z = 4 -- the "
      "redshifts that drive the published WDM bound -- the baryon suppression is INSIDE the allowance over the "
      "constraining range k = 8-12 h/Mpc for c0 = 1e-6 (suppression/allowed < 1)",
      L1['z4']['R_baryon'] < 1.0, f"c0=1e-6, z=4: max(suppression/allowed, k=8-12) baryon = {L1['z4']['R_baryon']:.2f}")
check("LYA-2  and at z = 3 the baryon reading is BORDERLINE: suppression/allowed between 0.5 and 2 at its worst "
      "k for c0 = 1e-6 (it exceeds 2 at z = 2, where the forest is less constraining)",
      0.5 < L1['z3']['R_baryon'] < 2.0 and L1['z2']['R_baryon'] > 2.0,
      f"c0=1e-6: z=3 {L1['z3']['R_baryon']:.2f}, z=2 {L1['z2']['R_baryon']:.2f}; baryon suppression at k=10 h/Mpc: "
      f"z=2 {L1['z2']['baryon'][KL.index(10.0)]:.3f}, z=3 {L1['z3']['baryon'][KL.index(10.0)]:.3f}, z=4 {L1['z4']['baryon'][KL.index(10.0)]:.3f}")
check("LYA-3  THE FORK IS REAL AND LARGE: at z = 3 the total-matter and baryon suppressions differ by more than "
      "5x at k = 10 h/Mpc.  Which one the forest flux traces on scales that are mildly non-linear at z = 3 "
      "(Delta^2 ~ 10-30) cannot be decided by linear theory: the gas needs the fluid's potential wells to reach "
      "the overdensities the forest sees, and a fluid that is pressure-supported below ~3 h/Mpc at z = 3 does "
      "not provide them.  => the Lyman-alpha verdict is UNDETERMINED between a decisive FAIL (total reading) "
      "and BORDERLINE (baryon reading), and the deciding computation is a hydrodynamical simulation with a "
      "separate pressure-supported dark fluid, which does not exist for this sector or for AeST",
      L1['z3']['total'][KL.index(10.0)] / L1['z3']['baryon'][KL.index(10.0)] > 5,
      f"z=3, k=10 h/Mpc: total {L1['z3']['total'][KL.index(10.0)]:.3f} vs baryon {L1['z3']['baryon'][KL.index(10.0)]:.3f} "
      f"(ratio {L1['z3']['total'][KL.index(10.0)] / L1['z3']['baryon'][KL.index(10.0)]:.1f}x)")
L3 = RES['lya']['3.21e-06']
check("LYA-4  the window's upper end is worse in both readings: at c0 = 3.21e-6 the baryon reading already "
      "exceeds the allowance at z = 3 (ratio > 1) and the total reading exceeds it by > 10x",
      L3['z3']['R_baryon'] > 1.0 and L3['z3']['R_total'] > 10,
      f"c0=3.21e-6, z=3: baryon {L3['z3']['R_baryon']:.2f}x, total {L3['z3']['R_total']:.1f}x allowed")

sec("VERDICT (late times) -- and honest scope")
print(f"""
  RUNNING c_s^2 = c0 a^3, c0 = 1e-6 (window floor):
     sigma_8(total) {R1['sigma8_total']:.4f} vs control {s8_ctrl:.4f} ({100 * R1['ds8']:+.1f}%);  z=0 P/P_ctrl: k=0.1 {R1['z0_total']['0.1']:.4f},
     k=1 {R1['z0_total']['1']:.3f}, k=10 {R1['z0_total']['10']:.4f} h/Mpc;  50% suppression at k_50 = {R1['k50_total_z0']:.2f} h/Mpc (fluid alone {R1['k50_fluid_z0']:.2f}).
     Galaxy-scale power IS suppressed, large scales survive, sigma_8 shifts modestly downward.
     Across the window (to 3.21e-6): sigma_8 {R3['sigma8_total']:.4f} ({100 * R3['ds8']:+.1f}%), k_50 = {R3['k50_total_z0']:.2f} h/Mpc.
  LYMAN-ALPHA (the named next falsifier), c0 = 1e-6, k = 1-10 h/Mpc, suppression 1 - P/P_ctrl:
     z=3 total  : {"  ".join(f"{s:.3f}" for s in L1['z3']['total'][:6])}   -> FAILS the 5.3-keV allowance by {L1['z3']['R_total']:.0f}x
     z=3 baryon : {"  ".join(f"{s:.3f}" for s in L1['z3']['baryon'][:6])}   -> {L1['z3']['R_baryon']:.2f}x the allowance (borderline)
     z=4 baryon : {"  ".join(f"{s:.3f}" for s in L1['z4']['baryon'][:6])}   -> {L1['z4']['R_baryon']:.2f}x (inside)
     z=2 baryon : {"  ".join(f"{s:.3f}" for s in L1['z2']['baryon'][:6])}   -> {L1['z2']['R_baryon']:.2f}x (outside, weaker data)
     VERDICT: UNDETERMINED between FAIL (total-matter reading) and BORDERLINE (linear-baryon reading); the
     generous reading sits AT the tolerance for the smallest allowed c0, so any non-linear starvation of the
     gas by the pressure-supported fluid pushes it over.  A two-species hydro simulation decides.

  SCOPE: (i) linear theory throughout; the forest at k ~ 5-10 h/Mpc, z = 3 is mildly non-linear.  (ii) The
  WDM allowance is a z-independent proxy (Viel+05 transfer, m = 5.3 keV) for a bound derived from a joint
  z = 3-5.4 fit; a z-dependent suppression is compared to it redshift by redshift, which is approximate in
  both directions.  (iii) The sound speed is c0 a^3 all the way to today (cosh/exp K with the shift charge
  still undiluted); a saturating c_s^2 lies between the running and constant scans.  (iv) The galaxy
  window's floor (c_s^2 ~ 1e-6, c_s ~ 300 km/s today) is L138's number; it is not re-derived here.
""", flush=True)
with open(os.path.join(HERE, 'L152_pk_results.json'), 'w') as f:
    json.dump(RES, f, indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
print("=" * 112)
if FAILS:
    print(f"L152 (2/2) INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L152 (2/2) COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time() - T0:.1f}s]")
print("=" * 112)
