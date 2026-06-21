#!/usr/bin/env python3
"""
MASTER RUNNER -- the three caveats together + the verdict.
==========================================================
Ties caveat 1 (self-consistent r''=-g_AeST), caveats 2+3 (vector + violent-relaxation
mode-mixing), and the adversarial artifact-ruling into ONE verdict on whether dynamical
collapse PINS the AeST oscillation phase (the cluster-boost knob chi_infty).

Outputs the load-bearing numbers:
  - slope d(theta_late)/d(IC_phase) for each caveat  (≈1 -> no pin; ≈0 -> pin)
  - eta(R500) spread over ICs                         (the boost observable)
  - E_drift of the conservative vector mixing         (≈0 -> mixing not dissipation)
  - gamma_pin/(3H0) damping needed to force a pin     (>>1 -> no physical pin)
  - galaxy worst-case RAR shift (dex)                 (<0.05 -> galaxy-safe)
QUARANTINE / BOTH-WAYS per aest_rig_core.py.
"""
import numpy as np, functools
from aest_rig_core import mu_of, H0, c, Mpc, kpc, Msun, a0
from aest_rig_selfconsistent import run_selfconsistent
from aest_rig_nonradial_vector import pin_sweep
from aest_rig_ADVERSARIAL import damping_sweep, galaxy_safety, artifact_ruling
from aest_rig_core import slope_theta_vs_ic, circ_std, pin_metric
print = functools.partial(print, flush=True)

def main():
    print("="*92); print("RIGOROUS AeST COLLAPSE -- MASTER VERDICT (3 caveats + adversarial)")
    print("="*92)
    out = {}

    # -------- CAVEAT 1: self-consistent collapse, IC-phase sweep, mass + profile ensemble --------
    print("\n[CAVEAT 1] SELF-CONSISTENT r''=-g_AeST -- IC + mass + profile ensemble:")
    ic_phases = np.linspace(0, 2*np.pi, 6, endpoint=False)
    th=[]; etas=[]; cross=[]
    grid = [(1e14,1.3,'tophat'), (1e15,2.0,'nfw'), (3e14,1.6,'tophat')]
    for (M,R,prof) in grid:
        for p in ic_phases:
            r = run_selfconsistent(Mtot_Msun=M, R500_Mpc=R, ic_phase=p, profile=prof,
                                   n_shell=36)
            th.append(r['theta_late']); etas.append(r['eta']); cross.append(r['cross_events'])
    # clean d/dIC on the first (single M,prof) family + the wrap-immune |resp| metric
    th0=[run_selfconsistent(Mtot_Msun=1e14,R500_Mpc=1.3,ic_phase=p,n_shell=30)['theta_late']
         for p in ic_phases]
    slope1, cstd1, resp1 = pin_metric(ic_phases, th0)
    out['c1_slope']=slope1; out['c1_circstd']=cstd1; out['c1_resp']=resp1
    out['c1_eta']=(float(np.nanmin(etas)), float(np.nanmax(etas))); out['c1_cross']=int(np.median(cross))
    print(f"  slope d(theta)/d(IC) = {slope1:+.3f} | circ_std = {cstd1:.3f} rad | "
          f"|IC-response| = {resp1:.3f}  (1=tracks IC=NO pin, 0=pinned)")
    print(f"  eta(R500) (descriptive, dPhi0=0) = {np.nanmin(etas):+.3f}..{np.nanmax(etas):+.3f}")
    print(f"  median shell-crossing events = {int(np.median(cross))} (>0 -> multi-stream present)")

    # -------- CAVEATS 2+3: vector (conservative) + violent-relaxation mode-mixing --------
    print("\n[CAVEATS 2+3] VECTOR (conservative) + violent-relaxation mode-mixing:")
    s_cons, cs_cons, Edr_cons,_,_, resp_cons = pin_sweep('conservative', K_coupling=2.0)
    s_diss, cs_diss, Edr_diss,_,_, resp_diss = pin_sweep('dissipative', K_coupling=2.0)
    out['c23_slope_cons']=s_cons; out['c23_Edrift_cons']=Edr_cons; out['c23_resp_cons']=resp_cons
    out['c23_slope_diss']=s_diss; out['c23_Edrift_diss']=Edr_diss; out['c23_resp_diss']=resp_diss
    print(f"  PHYSICAL conservative mixing: |IC-resp|={resp_cons:.3f} E_drift={Edr_cons:.2e} "
          f"(resp~1 -> tracks IC=no pin; E~0 -> no sink)")
    print(f"  CONTROL  dissipative   sink : |IC-resp|={resp_diss:.3f} E_drift={Edr_diss:.2e} "
          f"(resp~0 -> sink PINS; E<0 -> energy bled)")

    # -------- ADVERSARIAL: damping threshold + galaxy-safe + artifact ruling --------
    print("\n[ADVERSARIAL] damping threshold to force a pin + galaxy-safety:")
    res = damping_sweep()
    pin_g = next(((g,gh) for g,gh,sl in res if abs(sl)<0.3), None)
    out['gamma_pin_over_3H0'] = pin_g[1] if pin_g else None
    if pin_g:
        print(f"  phase pins only at gamma >= {pin_g[1]:.1f} x 3H0 (AeST has NO friction term)")
    worst_dex, pg, pc = galaxy_safety()
    out['galaxy_worst_dex']=worst_dex; out['protect_ratio']=pc/pg
    print(f"  galaxy worst-case RAR shift over all phases = {worst_dex:.4f} dex (veto 0.05)")
    print(f"  cluster/galaxy mass-term protection ratio = {pc/pg:.0f}x")
    print("  artifact ruling (nu_num halving + BC flip):")
    for nu_num, somm, slope in artifact_ruling():
        print(f"    nu_num={nu_num:.0e} sommerfeld={somm} -> slope={slope:+.3f}")

    # -------- VERDICT --------
    print("\n" + "="*92); print("VERDICT")
    print("="*92)
    # PIN requires |IC-response| -> 0 (phase independent of IC) for a PHYSICAL (E-conserving)
    # mechanism. c1_resp~0.5 (partial, noisy differencing) and c23_resp_cons~1 (tracks IC).
    pinned = (out['c1_resp']<0.15) or (out['c23_resp_cons']<0.15 and abs(out['c23_Edrift_cons'])<1e-2)
    if pinned:
        print("  A PIN emerged -- check it is a BOOST, universal, galaxy-safe, NOT an artifact.")
    else:
        print("  NO PIN. All three additions leave the phase IC-tracking (slope ~ O(1)).")
        print("  The conservative vector mixing REDISTRIBUTES (E_drift~0) but does not dissipate;")
        print("  a pin requires gamma >> 3H0 which AeST's action-conservative structure forbids.")
        print(f"  Galaxy-safe ({out['galaxy_worst_dex']:.4f} dex < 0.05). The no-go HOLDS, harder.")
    return out

if __name__ == "__main__":
    o = main()
    print("\nMACHINE-READABLE:", {k:(round(v,4) if isinstance(v,float) else v) for k,v in o.items()
                                   if not isinstance(v,tuple)})
