#!/usr/bin/env python3
"""CFG624 G6 (FROZEN_CRITERIA.md 803cef306): CMB acoustic peaks with NO COLD ENERGY -- CONTEXT ONLY, NO VERDICT.
Framework-native verdict: UNTESTABLE (declared in the criteria: no derived law for linear perturbations in the pre-recombination plasma;
A5 is an input without an action).  Context: if A5 is read literally (law off where nothing is bound), z ~ 1100 physics is GR + baryons +
photons + neutrinos; CAMB (FLAGGED: inherited GR-linear Boltzmann machinery) gives the TT spectrum for omega_c = 0 in the NCE open
background (rho_DE held).  Raw Planck TT band powers are NOT on disk; the comparison values below are RECALLED Planck 2018 peak heights
(PROVISIONAL, not raw data).  M-G6: the peak finder on CAMB omega_c = 0.120 (flat) must find three peaks at l ~ 200-230, 520-560, 790-840
(machinery control only; no LCDM yardstick enters anything).
Run from the repository root:  nice -n 10 python3 campaign_fresh_gravity/CFG624_no_cold_energy/cfg624_cmb.py"""
import os, json
os.environ["OMP_NUM_THREADS"] = "2"
import numpy as np
import camb

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


h = 0.6736; OL = 1.0 - (0.02237 + 0.1200) / h ** 2


def tt(omch2, omk):
    p = camb.CAMBparams()
    p.set_cosmology(H0=100 * h, ombh2=0.02237, omch2=omch2, omk=omk, mnu=0.0, num_massive_neutrinos=0, tau=0.054)
    p.InitPower.set_params(ns=0.965, As=2.1e-9); p.set_for_lmax(2500, lens_potential_accuracy=0); p.WantTensors = False
    r = camb.get_results(p)
    cl = r.get_cmb_power_spectra(p, CMB_unit="muK", raw_cl=False)["unlensed_scalar"][:, 0]
    return np.arange(len(cl)), cl, r


def peaks(ell, D, lo=100, hi=2450):   # range widened after the first run (only one NCE peak below 1400); disclosed
    m = (ell >= lo) & (ell <= hi); e, d = ell[m], D[m]
    i = [k for k in range(3, len(d) - 3) if d[k] == d[k - 3:k + 4].max()]
    return [(int(e[k]), float(d[k])) for k in i]


P(__doc__.split("Run from")[0].strip())
ok_ = 1.0 - 0.02237 / h ** 2 - OL
e0, D0, r0 = tt(0.0, ok_)
e1, D1, r1 = tt(0.1200, 0.0)
pk0, pk1 = peaks(e0, D0), peaks(e1, D1)
P(f"\n  NCE (omega_c 0, Omega_k {ok_:+.4f}, Omega_DE {r0.omega_de:.5f}): TT peaks (l, D_l muK^2): {[(l, round(d)) for l, d in pk0[:5]]}")
P(f"  machinery control (omega_c 0.120, flat): TT peaks: {[(l, round(d)) for l, d in pk1[:5]]}")
ctl = len(pk1) >= 3 and 200 <= pk1[0][0] <= 230 and 520 <= pk1[1][0] <= 560 and 790 <= pk1[2][0] <= 840
P(f"  [{'PASS' if ctl else 'FAIL'}] M-G6 the peak finder finds the three control peaks in the declared windows")
REC = dict(l1=220, D1=5720.0, l3=815, D3=2520.0, note="RECALLED Planck 2018 TT peak heights, PROVISIONAL, not raw band powers")
r3 = pk0[2][1] / pk0[0][1] if len(pk0) >= 3 else float("nan")
P(f"  NCE 3rd/1st peak height ratio {r3:.3f} (peaks at l {[l for l, _ in pk0[:3]]}); recalled Planck ~{REC['D3'] / REC['D1']:.2f} "
  f"(PROVISIONAL) -> CONTEXT ONLY; G6 framework-native verdict UNTESTABLE")
res = dict(lane="CFG624", script="cfg624_cmb", verdict="UNTESTABLE (framework-native); context only", NCE_peaks=pk0[:6], control_peaks=pk1[:6],
           NCE_ratio_3_1=r3, control_ok=bool(ctl), recalled_planck=REC, NCE_Omega_k=ok_, NCE_Omega_DE=float(r0.omega_de),
           NCE_D_l_at=dict((str(l), float(D0[l])) for l in (220, 540, 815, 1100)))
json.dump(res, open(os.path.join(HERE, "cfg624_cmb_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg624_cmb.out"), "w").write("\n".join(LOG) + "\n")
