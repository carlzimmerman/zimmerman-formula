#!/usr/bin/env python3
"""
L152 (part 1 of 2) -- THE DECIDING BOLTZMANN RUN FOR THE L139 SECTOR: does a dark fluid whose sound speed
        RUNS UP with time (c_s^2 = c0 (a/a_*)^3, the cosh/exp-K leaf-normal k-essence) reproduce the CMB?
=============================================================================================================
THE SECTOR (L139 route 2):  L_dark = K(Q) - c_Y |D chi|^2,  Q = n^mu grad_mu chi on the clock's foliation.
  background: dK/dQ = I_0/a^3  => exact a^-3 dust (cosh/exp K: no a^-6 stiff partner, L137).
  linear:     c_s^2 = 2 c_Y / K_QQ(a):  CONSTANT for quadratic K;  ~ a^+3 for cosh/exp K (L138).
  The L138 window on c_s^2(today):  floor ~1e-6 (galaxy smoothness)  ..  ceiling 3.21e-6 (arXiv:1601.05097).

HOW IT IS RUN (stated exactly):
  * CLASS 3.3.4.0 (classy), PATCHED so the fluid's rest-frame sound speed can run:
        cs2_fld(a) = min( cs2_fld_max , cs2_fld * (a/cs2_fld_astar)^cs2_fld_p )
    The patch is L152_class_running_cs2/running_cs2.patch (4 call sites + input reading); it is built into
    L152_class_running_cs2/site by build_patched_classy.sh and imported from there.  With cs2_fld_p = 0 the
    patched code is REQUIRED (check REG-*) to reproduce the stock classy bit-for-bit.  This is a real
    Boltzmann integration of a GDM fluid with w = 0, c_s^2(a) as above, c_vis^2 = 0 (CLASS's fld has no
    viscosity) -- no piecewise stand-in, no growth-ODE substitute.
  * the dark sector is CLASS's 'fld' with w0 = -1e-5 (CLASS refuses w >= 0; L129 used -1e-4 -- both are
    run, see part 4), Omega_fld = 0.1190/h^2, plus a residual omega_cdm = 0.001 so the code's CDM branch
    stays alive.  Total dark density = 0.1200, Planck-2018-like everything else.
  * recombination = recfast.  REASON (found here): CLASS's HyRec wrapper computes ITS OWN H(z) from
    Omega0_nfsm (baryons + cdm only, the fluid excluded), so a fluid-as-dust run recombines in the wrong
    Hubble rate (z_rec shifts by 0.5, theta_s by 6e-4).  recfast takes H from the background module and the
    fluid control then matches a real LambdaCDM run to 2e-4 (check CTRL-2).  The differential comparison is
    immune to this either way (part 4), but the ABSOLUTE control should be a faithful CDM stand-in.
  * every test run is compared with the c_s^2 = 0 CONTROL of the SAME fluid (same w): identical background
    by construction (100*theta_s agrees to <1e-5), so only the effect of the sound speed is measured.
  * the GDM mapping (w=0, rest-frame c_s^2 = the dispersion sound speed 2c_Y/K_QQ, no shear) is exact
    sub-horizon; near horizon crossing it is an O((aH/k)^2) effective description of the scalar.  Because
    c_s^2(a_rec) ~ 1e-15 in the running case, that regime is irrelevant here.

WHAT IS COMPUTED:
  0  build/regression: patched(p=0) == stock classy;  control reproduces the observed peak 1 (l~220,
     ~5750 uK^2) and a true LambdaCDM run.
  1  CONSTANT c_s^2 (quadratic K) scan over the window and beyond: peak heights/ratios, max fractional
     deviation of TT/EE/TE (unlensed AND lensed) over l = 30-2000, C_l^phiphi, and a Planck-like
     fixed-parameter Delta chi^2 (labelled: no marginalisation => an UPPER bound on detectability).
  2  RUNNING c_s^2 = c0 a^3 scan: the same, plus c_s^2(a_rec).
  3  the running ceiling: the c0 at which the lensed CMB first leaves the 1% band.
  4  the L129-identical configuration (hyrec, w0 = -1e-4) as a cross-check row.
Part 2 (L152_running_cs2_pk_lyman_alpha.py) does P(k), sigma_8, the k of 50% suppression, Lyman-alpha, and an
independent growth-solver validation of the patch's time dependence.

POLARITY: each check ASSERTS a statement; PASS = true; every pass condition is a computed inequality.
"""
import os, sys, json, time, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, 'L152_class_running_cs2', 'site')
STOCK_DUMP = os.path.join(HERE, 'L152_class_running_cs2', 'stock_dump.npz')

# ---------------------------------------------------------------------------------------------------------
# subprocess mode: dump spectra from the STOCK classy (the two packages share a name, so separate process)
# ---------------------------------------------------------------------------------------------------------
h = 0.6736
BASE = dict(output='tCl,pCl,lCl', lensing='yes', l_max_scalars=2500, omega_b=0.02237, h=h, A_s=2.1e-9,
            n_s=0.9649, tau_reio=0.0544, N_ur=3.046, YHe=0.2454, recombination='recfast')
FLD = dict(omega_cdm=0.001, Omega_fld=0.1190 / h ** 2, w0_fld=-1e-5, wa_fld=0.0, use_ppf='no')
LMAX = 2500

def run_spectra(Class, extra, base=BASE):
    c = Class(); p = dict(base); p.update(extra); c.set(p); c.compute()
    cl = c.raw_cl(LMAX); lcl = c.lensed_cl(LMAX)
    der = c.get_current_derived_parameters(['100*theta_s', 'z_rec', 'rs_rec'])
    out = dict(tt=cl['tt'], ee=cl['ee'], te=cl['te'], pp=cl['pp'], ltt=lcl['tt'], lee=lcl['ee'], lte=lcl['te'],
               theta=der['100*theta_s'], z_rec=der['z_rec'], rs_rec=der['rs_rec'])
    c.struct_cleanup(); c.empty()
    return out

if len(sys.argv) > 1 and sys.argv[1] == '--dump-stock':
    from classy import Class as StockClass          # NO sys.path insertion: the stock package
    d0 = run_spectra(StockClass, dict(FLD, cs2_fld=0.0))
    d1 = run_spectra(StockClass, dict(FLD, cs2_fld=1e-6))
    np.savez(sys.argv[2], **{f'c0_{k}': v for k, v in d0.items()}, **{f'c1_{k}': v for k, v in d1.items()})
    sys.exit(0)

# ---------------------------------------------------------------------------------------------------------
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)

print("=" * 112)
print("L152 (1/2) -- running-sound-speed dark fluid vs the CMB: a real Boltzmann run with a patched CLASS")
print("=" * 112, flush=True)

sec("PART 0 -- the patched CLASS: import, bit-for-bit regression against stock classy, control validation")
if not os.path.isdir(SITE):
    print("  patched classy not built: run L152_class_running_cs2/build_patched_classy.sh first"); sys.exit(2)
sys.path.insert(0, SITE)
from classy import Class
import classy as _classy_mod
check("BUILD-0  the classy imported by this script is the PATCHED build living under "
      "L152_class_running_cs2/site (not the system package)",
      os.path.abspath(os.path.dirname(_classy_mod.__file__)).startswith(os.path.abspath(SITE)),
      "import path is inside L152_class_running_cs2/site")

# regression against the stock package, run in a subprocess (sequential: one CLASS process at a time)
rc = subprocess.run([sys.executable, os.path.abspath(__file__), '--dump-stock', STOCK_DUMP],
                    capture_output=True, text=True)
if rc.returncode != 0 or not os.path.exists(STOCK_DUMP):
    check("REG-0  the stock classy could be run in a subprocess for the regression comparison", False,
          "stock classy unavailable: " + rc.stderr.strip().splitlines()[-1][:120] if rc.stderr.strip() else "no stderr")
else:
    st = np.load(STOCK_DUMP)
    p0 = run_spectra(Class, dict(FLD, cs2_fld=0.0))
    p1 = run_spectra(Class, dict(FLD, cs2_fld=1e-6))
    p1b = run_spectra(Class, dict(FLD, cs2_fld=1e-6, cs2_fld_p=0.0, cs2_fld_astar=1.0, cs2_fld_max=1.0))
    worst = 0.0
    for tag, pr in (('c0', p0), ('c1', p1)):
        for q in ('tt', 'ee', 'te', 'pp', 'ltt', 'lee', 'lte'):
            a, b = st[f'{tag}_{q}'][2:], pr[q][2:]
            m = np.abs(a) > 0
            worst = max(worst, float(np.max(np.abs(b[m] - a[m]) / np.abs(a[m]))))
    check("REG-0  with the running switched off (cs2_fld_p = 0, the default) the PATCHED classy reproduces the "
          "STOCK classy to machine precision on TT/EE/TE/phiphi, unlensed and lensed, for c_s^2 = 0 and 1e-6 "
          "(max relative difference < 1e-10): the patch changes nothing it should not",
          worst < 1e-10, f"max |rel diff| over all spectra = {worst:.1e}")
    worst2 = max(float(np.max(np.abs(p1b[q][2:] - p1[q][2:]) / np.abs(p1[q][2:])))
                 for q in ('tt', 'ee', 'ltt'))
    check("REG-1  passing the new parameters explicitly at their defaults (p=0, a_*=1, max=1) is a no-op "
          "(max rel diff < 1e-12), so the parameters are read and default exactly as documented",
          worst2 < 1e-12, f"max |rel diff| = {worst2:.1e}")
    os.remove(STOCK_DUMP)

# control validation: observed peak 1 and a true LambdaCDM run
def peaks(cl_dimless, nmax=3):
    l = np.arange(len(cl_dimless)); D = cl_dimless * l * (l + 1) / (2 * np.pi) * (2.7255e6) ** 2
    out = []
    for i in range(101, len(D) - 1):
        if D[i] > D[i - 1] and D[i] > D[i + 1]:
            out.append((int(l[i]), float(D[i])))
        if len(out) >= nmax: break
    return out
ctrl = run_spectra(Class, dict(FLD, cs2_fld=0.0))
lcdm = run_spectra(Class, dict(omega_cdm=0.1200))
pk_ctrl = peaks(ctrl['tt']); lpk_ctrl = peaks(ctrl['ltt'])
l = np.arange(LMAX + 1); BAND = (l >= 30) & (l <= 2000)
def maxdev(a, b, band=BAND): return float(np.max(np.abs(a[band] / b[band] - 1)))
def maxdev_te(a, b, tt, ee, band=BAND): return float(np.max(np.abs((a[band] - b[band]) / np.sqrt(tt[band] * ee[band]))))
print(f"    control (fluid, c_s^2=0):  100*theta_s={ctrl['theta']:.6f}  z_rec={ctrl['z_rec']:.3f}  "
      f"unlensed peaks={[(a, round(b, 1)) for a, b in pk_ctrl]}")
print(f"    true LambdaCDM (omega_cdm=0.12): 100*theta_s={lcdm['theta']:.6f}  z_rec={lcdm['z_rec']:.3f}  "
      f"unlensed peaks={[(a, round(b, 1)) for a, b in peaks(lcdm['tt'])]}")
check("CTRL-0  the c_s^2 = 0 control reproduces the measured first acoustic peak (l ~ 220, ~5750 uK^2), as "
      "L129's control does: the pipeline sees the real CMB",
      200 < pk_ctrl[0][0] < 245 and 5300 < pk_ctrl[0][1] < 6200,
      f"peak1: l={pk_ctrl[0][0]}, {pk_ctrl[0][1]:.0f} uK^2")
check("CTRL-1  and the control's peaks 2 and 3 sit where the data put them (l ~ 537, ~810) with the observed "
      "third/second ratio ~1.0 (Planck: 0.99 +- 0.01 at this binning)",
      500 < pk_ctrl[1][0] < 560 and 780 < pk_ctrl[2][0] < 840 and 0.95 < pk_ctrl[2][1] / pk_ctrl[1][1] < 1.03,
      f"peak2 l={pk_ctrl[1][0]}, peak3 l={pk_ctrl[2][0]}, peak3/peak2={pk_ctrl[2][1] / pk_ctrl[1][1]:.4f}")
dev_ctrl = dict(tt=maxdev(ctrl['tt'], lcdm['tt']), ltt=maxdev(ctrl['ltt'], lcdm['ltt']), ee=maxdev(ctrl['ee'], lcdm['ee']),
                pp=maxdev(ctrl['pp'], lcdm['pp']))
check("CTRL-2  the fluid-as-dust control IS a faithful CDM stand-in: against a true LambdaCDM run (real CDM, "
      "no fluid, same everything else) it agrees to < 5e-4 in TT (unlensed and lensed) and < 1e-3 in EE over "
      "l = 30-2000, and 100*theta_s agrees to < 1e-4 -- this is what recfast + w0 = -1e-5 buys (with hyrec, "
      "which computes its own H(z) without the fluid, the mismatch is 7e-3; see part 4)",
      dev_ctrl['tt'] < 5e-4 and dev_ctrl['ltt'] < 5e-4 and dev_ctrl['ee'] < 1e-3 and abs(ctrl['theta'] - lcdm['theta']) < 1e-4,
      f"TT {dev_ctrl['tt']:.1e}, lensed TT {dev_ctrl['ltt']:.1e}, EE {dev_ctrl['ee']:.1e}, phiphi {dev_ctrl['pp']:.1e}, "
      f"d(100theta_s) = {abs(ctrl['theta'] - lcdm['theta']):.1e}, dz_rec = {abs(ctrl['z_rec'] - lcdm['z_rec']):.3f}")

# Planck-like fixed-parameter Delta chi^2 (TT+EE+TE, lensed, l=30-2000, f_sky=0.7, 7' beam, 30/60 uK-arcmin)
T0uK = 2.7255e6
arcmin = np.pi / (180 * 60); theta_b = 7 * arcmin
NlT = (30 * arcmin) ** 2 * np.exp(l * (l + 1) * theta_b ** 2 / (8 * np.log(2))) / T0uK ** 2
NlP = (60 * arcmin) ** 2 * np.exp(l * (l + 1) * theta_b ** 2 / (8 * np.log(2))) / T0uK ** 2
def dchi2(r, ref, fsky=0.7):
    """TT+TE+EE (lensed) Gaussian Delta chi^2 at FIXED parameters, l = 30-2000."""
    tot = 0.0
    for i in np.where(BAND)[0]:
        C = np.array([[ref['ltt'][i] + NlT[i], ref['lte'][i]], [ref['lte'][i], ref['lee'][i] + NlP[i]]])
        D = np.array([[r['ltt'][i] - ref['ltt'][i], r['lte'][i] - ref['lte'][i]],
                      [r['lte'][i] - ref['lte'][i], r['lee'][i] - ref['lee'][i]]])
        M = np.linalg.solve(C, D)
        tot += fsky * (2 * i + 1) / 2 * np.trace(M @ M)
    return float(tot)
def dA_lens(r, ref, L1=40, L2=400):
    """(2L+1)-weighted mean fractional change of C_L^phiphi over Planck's most sensitive range."""
    L = np.arange(L1, L2 + 1); w = 2 * L + 1
    return float(np.sum(w * (r['pp'][L1:L2 + 1] / ref['pp'][L1:L2 + 1] - 1)) / np.sum(w))
SIG_ALENS = 0.025     # Planck 2018 lensing-amplitude precision (2.5%)
def dchi2_lens(r, ref): return (dA_lens(r, ref) / SIG_ALENS) ** 2

def metrics(r, ref):
    pk = peaks(r['tt']); lpk = peaks(r['ltt']); pkr = peaks(ref['tt']); lpkr = peaks(ref['ltt'])
    m = dict(theta=r['theta'], dtheta=abs(r['theta'] - ref['theta']),
             peaks_unl=pk, peaks_len=lpk,
             p1=pk[0][1] / pkr[0][1], p2=pk[1][1] / pkr[1][1], p3=pk[2][1] / pkr[2][1],
             r31=pk[2][1] / pk[0][1], r32=pk[2][1] / pk[1][1], r21=pk[1][1] / pk[0][1],
             r31_ref=pkr[2][1] / pkr[0][1], r32_ref=pkr[2][1] / pkr[1][1], r21_ref=pkr[1][1] / pkr[0][1],
             lp1=lpk[0][1] / lpkr[0][1], lp3=lpk[2][1] / lpkr[2][1],
             dev_tt=maxdev(r['tt'], ref['tt']), dev_ee=maxdev(r['ee'], ref['ee']),
             dev_te=maxdev_te(r['te'], ref['te'], ref['tt'], ref['ee']),
             dev_ltt=maxdev(r['ltt'], ref['ltt']), dev_lee=maxdev(r['lee'], ref['lee']),
             dev_lte=maxdev_te(r['lte'], ref['lte'], ref['ltt'], ref['lee']),
             dev_pp_max=maxdev(r['pp'], ref['pp']),
             dev_pp_L8_400=float(np.mean(r['pp'][8:401] / ref['pp'][8:401] - 1)),
             dev_pp_L400_2000=float(np.mean(r['pp'][400:2001] / ref['pp'][400:2001] - 1)),
             dev_low_l=float(np.max(np.abs(r['ltt'][2:30] / ref['ltt'][2:30] - 1))),
             dchi2_cl=dchi2(r, ref), dA_lens=dA_lens(r, ref), dchi2_lens=dchi2_lens(r, ref))
    m['dchi2'] = m['dchi2_cl'] + m['dchi2_lens']
    return m

def row(tag, m):
    print(f"  {tag:18s} dTheta {m['dtheta']:.0e} | pk1/2/3 {m['p1']:.4f}/{m['p2']:.4f}/{m['p3']:.4f} "
          f"r32 {m['r32']:.4f} (ctrl {m['r32_ref']:.4f}) | maxdev l=30-2000: TT {m['dev_tt']:.1e} EE {m['dev_ee']:.1e} "
          f"TE {m['dev_te']:.1e} | lensed TT {m['dev_ltt']:.1e} EE {m['dev_lee']:.1e} | phiphi mean L8-400 "
          f"{m['dev_pp_L8_400']:+.1e} max {m['dev_pp_max']:.1e} | l<30 {m['dev_low_l']:.1e} | dchi2 TTTEEE {m['dchi2_cl']:.2g} "
          f"+ lens(dA={m['dA_lens']:+.3f}) {m['dchi2_lens']:.2g} = {m['dchi2']:.2g}",
          flush=True)

RES = dict(setup=dict(w0_fld=-1e-5, recombination='recfast', omega_cdm_residual=0.001, Omega_fld_h2=0.1190,
                      cs2_form='min(1, c0*(a/a_star)^p), a_star=1', c_vis2=0.0, lmax=LMAX, band='l=30-2000'),
           control=dict(theta=ctrl['theta'], z_rec=ctrl['z_rec'], peaks_unl=pk_ctrl, peaks_len=lpk_ctrl,
                        vs_lcdm=dev_ctrl), constant={}, running={}, hyrec_config={})

sec("PART 1 -- CONSTANT c_s^2 (quadratic K): the window 1e-6 .. 3.21e-6, bracketed by 1e-7 and 1e-5")
C0_CONST = [1e-7, 1e-6, 1.8e-6, 3.21e-6, 1e-5]
for c0 in C0_CONST:
    r = run_spectra(Class, dict(FLD, cs2_fld=c0)); m = metrics(r, ctrl); RES['constant'][f'{c0:.3g}'] = m
    row(f"const {c0:.2e}", m)
mc = RES['constant']
check("CONST-0  every constant-c_s^2 run shares the control's background exactly (100*theta_s agrees to "
      "< 1e-5), so what follows is a pure sound-speed effect, not a re-tuned expansion history",
      all(m['dtheta'] < 1e-5 for m in mc.values()), f"max d(100theta_s) = {max(m['dtheta'] for m in mc.values()):.1e}")
check("CONST-1  at recombination a constant c_s^2 in the window is INVISIBLE in the primary (unlensed) CMB: "
      "max |dC_l/C_l| < 1e-3 for TT, EE and TE over l = 30-2000 at c_s^2 = 3.21e-6 -- consistent with L127's "
      "finding that the published 3.21e-6 bound is set by LATE-time clustering, not by recombination physics",
      mc['3.21e-06']['dev_tt'] < 1e-3 and mc['3.21e-06']['dev_ee'] < 1e-3 and mc['3.21e-06']['dev_te'] < 1e-3,
      f"unlensed at 3.21e-6: TT {mc['3.21e-06']['dev_tt']:.1e}, EE {mc['3.21e-06']['dev_ee']:.1e}, TE {mc['3.21e-06']['dev_te']:.1e}")
check("CONST-2  the late-time effect is where a constant c_s^2 shows: at 3.21e-6 the lensing potential is "
      "suppressed by tens of percent (Planck measures its amplitude to 2.5%), and the LENSED TT/EE deviate at "
      "the ~1% level -- so the window's ceiling is a CMB-lensing/late-ISW bound, reproduced here in kind",
      abs(mc['3.21e-06']['dev_pp_L8_400']) > 0.025 and mc['3.21e-06']['dev_ltt'] > 3e-3,
      f"at 3.21e-6: <dC^phiphi/C> L=8-400 = {mc['3.21e-06']['dev_pp_L8_400']:+.3f}, lensed TT maxdev {mc['3.21e-06']['dev_ltt']:.1e}, "
      f"lensed EE {mc['3.21e-06']['dev_lee']:.1e}")
m321 = mc['3.21e-06']
check("CONST-3  pipeline sensitivity is consistent with the literature bound, AND the bound is a LENSING bound: "
      "at the published 99.7% ceiling c_s^2 = 3.21e-6 (arXiv:1601.05097, Planck 2015 temperature, "
      "polarisation and lensing) the fixed-parameter Planck-like Delta chi^2 from TT+TE+EE ALONE is < 9 -- "
      "the lensed spectra by themselves would NOT exclude it -- while adding the lensing-potential amplitude "
      "(2.5% precision) lifts the total to >= 9.  (A first version of this check without the lensing term "
      "FAILED at 4.6; that failure is what identified the bound's origin.)  No marginalisation: upper bounds.",
      m321['dchi2_cl'] < 9.0 and m321['dchi2'] >= 9.0,
      f"Delta chi^2 at 3.21e-6: TT+TE+EE {m321['dchi2_cl']:.1f}; lensing amplitude dA = {m321['dA_lens']:+.3f} -> "
      f"{m321['dchi2_lens']:.1f}; total {m321['dchi2']:.1f}")
check("CONST-4  and it is monotone: the deviation grows with c_s^2 at every level (unlensed TT, lensed TT, "
      "phiphi), with no numerical noise floor masquerading as signal",
      all(bool(np.all(np.diff([mc[f'{c:.3g}'][q] for c in C0_CONST]) > 0)) for q in ('dev_tt', 'dev_ltt', 'dev_pp_max')),
      "all three deviation measures strictly increase along the scan")

sec("PART 2 -- RUNNING c_s^2 = c0 (a/1)^3 (cosh/exp K): the window, then up to 1e-3 to find the ceiling")
C0_RUN = [1e-6, 1.8e-6, 3.21e-6, 1e-5, 1e-4, 3e-4, 1e-3]
a_rec = 1.0 / (1.0 + ctrl['z_rec'])
for c0 in C0_RUN:
    r = run_spectra(Class, dict(FLD, cs2_fld=c0, cs2_fld_p=3.0, cs2_fld_astar=1.0, cs2_fld_max=1.0))
    m = metrics(r, ctrl); m['cs2_rec'] = c0 * a_rec ** 3; RES['running'][f'{c0:.3g}'] = m
    row(f"run c0={c0:.2e}", m)
mr = RES['running']
print(f"    c_s^2 at recombination (a_rec = {a_rec:.3e}): c0 * a_rec^3 = c0 * {a_rec ** 3:.2e}")
check("RUN-0  identical background across the running scan too (100*theta_s to < 1e-5)",
      all(m['dtheta'] < 1e-5 for m in mr.values()), f"max d(100theta_s) = {max(m['dtheta'] for m in mr.values()):.1e}")
win = [mr['1e-06'], mr['1.8e-06'], mr['3.21e-06']]
check("RUN-1  THE RESULT AT RECOMBINATION: for the whole L138 window (c0 = 1e-6 .. 3.21e-6) the running sector "
      "is INDISTINGUISHABLE from CDM in the primary CMB -- max |dC_l/C_l| < 1e-4 in TT, EE and TE over "
      "l = 30-2000 (a factor 100 inside the 1% band), because c_s^2(a_rec) = c0 a_rec^3 ~ 1e-15",
      all(m['dev_tt'] < 1e-4 and m['dev_ee'] < 1e-4 and m['dev_te'] < 1e-4 for m in win),
      f"unlensed maxdev at c0=3.21e-6: TT {win[2]['dev_tt']:.1e}, EE {win[2]['dev_ee']:.1e}, TE {win[2]['dev_te']:.1e}; "
      f"c_s^2(a_rec) = {win[2]['cs2_rec']:.1e}")
check("RUN-2  all three acoustic peak heights and both ratios (3/1, 3/2) agree with the control to < 1e-4 "
      "across the window (unlensed): the third peak is driven exactly as by CDM",
      all(abs(m['p1'] - 1) < 1e-4 and abs(m['p2'] - 1) < 1e-4 and abs(m['p3'] - 1) < 1e-4
          and abs(m['r32'] / m['r32_ref'] - 1) < 1e-4 and abs(m['r31'] / m['r31_ref'] - 1) < 1e-4 for m in win),
      f"at 3.21e-6: pk1/2/3 = {win[2]['p1']:.5f}/{win[2]['p2']:.5f}/{win[2]['p3']:.5f}, r32 = {win[2]['r32']:.5f} vs {win[2]['r32_ref']:.5f}")
check("RUN-3  the LENSED spectra -- what Planck actually measures -- also stay inside the 1% band by a wide "
      "margin over the window: lensed TT/EE max deviation < 1e-3, and the low-l (ISW) deviation < 1e-3",
      all(m['dev_ltt'] < 1e-3 and m['dev_lee'] < 1e-3 and m['dev_low_l'] < 1e-3 for m in win),
      f"at 3.21e-6: lensed TT {win[2]['dev_ltt']:.1e}, lensed EE {win[2]['dev_lee']:.1e}, l<30 {win[2]['dev_low_l']:.1e}")
check("RUN-4  CMB LENSING: the lensing-potential amplitude over Planck's L = 8-400 changes by less than the "
      "2.5% measurement precision across the window (the suppression lives at L > 400, where it reaches a "
      "few percent)",
      all(abs(m['dev_pp_L8_400']) < 0.025 for m in win),
      f"<dC^phiphi/C>(L=8-400) = {win[0]['dev_pp_L8_400']:+.1e} / {win[1]['dev_pp_L8_400']:+.1e} / {win[2]['dev_pp_L8_400']:+.1e}; "
      f"L=400-2000: {win[0]['dev_pp_L400_2000']:+.1e} / {win[2]['dev_pp_L400_2000']:+.1e}")
check("RUN-5  the fixed-parameter Planck-like Delta chi^2 (TT+TE+EE + lensing amplitude) over the window is "
      "< 1 (undetectable even with no marginalisation), versus >= 9 for the constant case at the same "
      "c_s^2(today) -- the running sector is at least an order of magnitude below the CMB's reach where "
      "quadratic K sits at its ceiling",
      all(m['dchi2'] < 1.0 for m in win) and mc['3.21e-06']['dchi2'] >= 9.0,
      f"running dchi2 = {win[0]['dchi2']:.2g} / {win[1]['dchi2']:.2g} / {win[2]['dchi2']:.2g}; constant at 3.21e-6: {mc['3.21e-06']['dchi2']:.1f}")

sec("PART 3 -- the running CEILING: where does the lensed CMB first leave the 1% band?")
xs = np.array(C0_RUN); ys = np.array([mr[f'{c:.3g}']['dev_ltt'] for c in C0_RUN])
ys_u = np.array([mr[f'{c:.3g}']['dev_tt'] for c in C0_RUN])
crosses = np.where((ys[:-1] < 0.01) & (ys[1:] >= 0.01))[0]
if len(crosses):
    i = crosses[0]; c_ceiling = float(np.exp(np.interp(np.log(0.01), np.log(ys[i:i + 2]), np.log(xs[i:i + 2]))))
else:
    c_ceiling = float('inf') if ys[-1] < 0.01 else float(xs[0])
RES['running_ceiling_lensedTT_1pct'] = c_ceiling
print(f"    lensed-TT max deviation along the scan: " + "  ".join(f"{c:.0e}:{y:.1e}" for c, y in zip(xs, ys)))
print(f"    unlensed-TT:                            " + "  ".join(f"{c:.0e}:{y:.1e}" for c, y in zip(xs, ys_u)))
print(f"    1%-band ceiling on c0 (running, lensed TT, log-interpolated): {c_ceiling:.2e}")
check("CEIL-0  the running ceiling sits ABOVE the window by more than two orders of magnitude: the lensed TT "
      "deviation only reaches 1% for c0 > 1e-4, i.e. > 30x the constant-case ceiling of 3.21e-6.  The CMB "
      "does not bound the running sector anywhere near the galaxy window -- the binding constraints are "
      "late-time (part 2 of L152)",
      c_ceiling > 30 * 3.21e-6, f"ceiling c0 = {c_ceiling:.1e} vs 3.21e-6 -> ratio {c_ceiling / 3.21e-6:.0f}")
check("CEIL-1  and it is the late-time (lensing) channel that binds, not recombination: at the ceiling the "
      "unlensed deviation is still below the lensed one, and only at c0 ~ 1e-3 (c_s^2(a_rec) ~ 1e-12) does "
      "anything reach the primary spectrum at the percent level",
      ys_u[np.searchsorted(xs, 1e-4)] < ys[np.searchsorted(xs, 1e-4)] and mr['0.001']['dev_tt'] > 1e-3,
      f"at c0=1e-4: unlensed {ys_u[np.searchsorted(xs, 1e-4)]:.1e} < lensed {ys[np.searchsorted(xs, 1e-4)]:.1e}; at 1e-3: unlensed {mr['0.001']['dev_tt']:.1e}")

sec("PART 4 -- cross-check in the L129-identical configuration (hyrec, w0 = -1e-4): the differential result "
    "does not depend on the recombination-code choice")
B2 = dict(BASE); B2.pop('recombination'); F2 = dict(FLD, w0_fld=-1e-4)
ctrl2 = run_spectra(Class, dict(F2, cs2_fld=0.0), base=B2)
lcdm2 = run_spectra(Class, dict(omega_cdm=0.1200), base=B2)
m2 = metrics(run_spectra(Class, dict(F2, cs2_fld=1e-6, cs2_fld_p=3.0), base=B2), ctrl2)
m2c = metrics(run_spectra(Class, dict(F2, cs2_fld=1e-6), base=B2), ctrl2)
RES['hyrec_config'] = dict(running_1e6=m2, constant_1e6=m2c, control_vs_lcdm_tt=maxdev(ctrl2['tt'], lcdm2['tt']),
                           control_z_rec=ctrl2['z_rec'], lcdm_z_rec=lcdm2['z_rec'])
row("hyrec run 1e-6", m2); row("hyrec const 1e-6", m2c)
print(f"    hyrec control vs true LambdaCDM: TT maxdev {RES['hyrec_config']['control_vs_lcdm_tt']:.1e}, "
      f"z_rec {ctrl2['z_rec']:.3f} vs {lcdm2['z_rec']:.3f} (the HyRec-wrapper H(z) issue)")
check("XCHK-0  in the L129-identical configuration the running-case deviations agree with the recfast "
      "configuration to within a factor 1.5 on every measure (unlensed TT, lensed TT, phiphi mean), so the "
      "verdict is not a recombination-code artefact",
      all(0.67 < m2[q] / mr['1e-06'][q] < 1.5 for q in ('dev_tt', 'dev_ltt')) and
      0.67 < m2['dev_pp_L8_400'] / mr['1e-06']['dev_pp_L8_400'] < 1.5,
      f"ratios hyrec/recfast: TT {m2['dev_tt'] / mr['1e-06']['dev_tt']:.2f}, lensed TT {m2['dev_ltt'] / mr['1e-06']['dev_ltt']:.2f}, "
      f"phiphi {m2['dev_pp_L8_400'] / mr['1e-06']['dev_pp_L8_400']:.2f}")
check("XCHK-1  but the ABSOLUTE control is worse with hyrec: its mismatch to true LambdaCDM exceeds 5e-3 in TT "
      "and z_rec is off by > 0.3 -- the reason the L152 runs use recfast (CTRL-2)",
      RES['hyrec_config']['control_vs_lcdm_tt'] > 5e-3 and abs(ctrl2['z_rec'] - lcdm2['z_rec']) > 0.3,
      f"hyrec control vs LCDM: TT {RES['hyrec_config']['control_vs_lcdm_tt']:.1e}, dz_rec = {abs(ctrl2['z_rec'] - lcdm2['z_rec']):.2f}")

sec("VERDICT (CMB) -- and honest scope")
print(f"""
  RUNNING c_s^2 = c0 a^3 over the L138 window (c0 = 1e-6 .. 3.21e-6) PASSES THE CMB:
     primary (unlensed) TT/EE/TE max deviation {win[0]['dev_tt']:.1e} .. {win[2]['dev_tt']:.1e} over l = 30-2000 (band 1e-2),
     lensed TT {win[0]['dev_ltt']:.1e} .. {win[2]['dev_ltt']:.1e}, lensing potential (L=8-400) {win[0]['dev_pp_L8_400']:+.1e} .. {win[2]['dev_pp_L8_400']:+.1e},
     peak heights 1/2/3 and ratios equal to the control to < 1e-4, fixed-parameter Planck-like
     Delta chi^2 {win[0]['dchi2']:.2g} .. {win[2]['dchi2']:.2g}.  c_s^2(a_rec) = {win[0]['cs2_rec']:.1e} .. {win[2]['cs2_rec']:.1e}.
     The CMB's own ceiling on the running sector is c0 ~ {c_ceiling:.0e} (lensed TT reaches 1%), ~{c_ceiling / 3.21e-6:.0f}x above the window.
  CONSTANT c_s^2 (quadratic K) at the same c_s^2(today): invisible at recombination (< 1e-3) but the lensing
     potential drops by {-mc['1e-06']['dev_pp_L8_400'] * 100:.0f}-{-mc['3.21e-06']['dev_pp_L8_400'] * 100:.0f}% (L=8-400) and the lensed spectra move at the {mc['1e-06']['dev_ltt'] * 100:.1f}-{mc['3.21e-06']['dev_ltt'] * 100:.1f}% level:
     the published 3.21e-6 ceiling is reproduced in kind (fixed-parameter Delta chi^2 = {mc['3.21e-06']['dchi2']:.0f} there, of
     which only {mc['3.21e-06']['dchi2_cl']:.1f} comes from TT+TE+EE: the published ceiling is a CMB-LENSING bound).

  SCOPE: (i) GDM mapping with w = -1e-5 (not exactly 0), rest-frame c_s^2 = the dispersion sound speed,
  c_vis^2 = 0 (CLASS's fld carries no shear); exact sub-horizon, an O((aH/k)^2) effective description at
  horizon crossing -- irrelevant here because c_s^2(a_rec) ~ 1e-15.  (ii) The cosh/exp K sound speed is
  c_s^2 ~ a^3 only while the shift charge is undiluted (Z >> 1); if the transition a_t falls before today
  the late-time c_s^2 saturates at a constant -- that case lies between the two scans run here.  (iii) The
  Delta chi^2 is a Planck-LIKE Gaussian estimate at FIXED cosmological parameters (an upper bound on
  detectability), not the Planck likelihood; no sigma is quoted from it.  (iv) Passing the CMB is necessary,
  not sufficient: sigma_8, P(k), and the Lyman-alpha forest are part 2.
""", flush=True)

with open(os.path.join(HERE, 'L152_cmb_results.json'), 'w') as f:
    json.dump(RES, f, indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
print("=" * 112)
if FAILS:
    print(f"L152 (1/2) INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L152 (1/2) COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time() - T0:.1f}s]")
print("=" * 112)
