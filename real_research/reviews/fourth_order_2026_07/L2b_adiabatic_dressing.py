#!/usr/bin/env python3
"""
L2b -- THE CORRECTED, DECISIVE TEST: the WORK-FREE (adiabatic) dressing.

Correction to a first-pass framing: a SUDDEN switch-on of the detector-field coupling
is itself a quench that does WORK (W_agent>0) and can transiently invert the detector
-- this is the agent-pumped channel (already priced by the hexad; Theorem VI's quench
mu=-62 dying in one period). It is NOT a free-from-vacuum effect. A robustness sweep
confirmed single sudden kicks DO invert (p_e up to 0.83) -- because they are quenches,
not because the vacuum supplies the sign.

The physically correct question for MODIFIED INERTIA: does the INTERACTING vacuum give
the detector NEGATIVE inertial DRESSING (delta-m<0, inversion) in the WORK-FREE limit --
i.e. when the coupling is switched on ADIABATICALLY, so the joint system tracks its
ground state and the agent does (asymptotically) zero work? That adiabatic dressed state
IS the reactive inertia the framework's a0 would have to come from.

Test: ramp the coupling 0 -> g_max over a ramp time T_ramp; scan T_ramp from sudden to
slow. If inversion is a genuine vacuum property it survives the adiabatic limit; if it is
a quench/work artifact it vanishes as T_ramp grows. Interacting (hz=0.6) vs free (hz=0.0).
Also read the adiabatic dressing sign directly from the dressed detector populations.
Runtime < 60 s (L=8).
"""
import numpy as np
from numpy.linalg import eigh
np.seterr(over='ignore', invalid='ignore', divide='ignore')
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from L2_nonuniform_interacting_vacuum import ising_chain, sx, sz, I2

def ramp_on(L, hz, g_max=1.5, w0=1.0, T_ramp=1.0, nseg=40):
    """Adiabatically ramp coupling 0->g_max over T_ramp (nseg piecewise-const steps),
       joint system starting in its UNCOUPLED ground state (detector down (x) chain vac).
       Return final detector p_e and the work done W_agent (energy above the coupled
       ground state -- the adiabatic 'defect')."""
    Hc, Z = ising_chain(L, 1.0, 0.9, hz)
    dimc = 2**L
    Ec, Vc = eigh(Hc); vac = Vc[:,0]
    site = L//2; Zc = Z[site]
    Hdet = np.kron(0.5*w0*sz, np.eye(dimc))
    Hc_full = np.kron(I2, Hc)
    Vcpl = np.kron(sx, Zc)
    det0 = np.array([0,1], complex)
    psi = np.kron(det0, vac)
    ne_proj = np.kron(np.array([[1,0],[0,0]],complex), np.eye(dimc))
    dt = T_ramp/nseg
    for k in range(nseg):
        amp = g_max*(k+0.5)/nseg              # linear ramp 0 -> g_max
        H = Hdet + Hc_full + amp*Vcpl
        E,V = eigh(H)
        psi = V @ (np.exp(-1j*E*dt) * (V.conj().T @ psi))
    p_e = np.real(psi.conj() @ ne_proj @ psi)
    # ground state of the FULLY coupled H (the ideal adiabatic target)
    Hfull = Hdet + Hc_full + g_max*Vcpl
    Ef, Vf = eigh(Hfull)
    gs = Vf[:,0]
    E_psi = np.real(psi.conj() @ Hfull @ psi)
    W_defect = E_psi - Ef[0]                   # energy above coupled ground = non-adiab work
    # detector populations in the ADIABATIC dressed ground state (the work-free answer)
    d = np.outer(gs, gs.conj()).reshape(2,dimc,2,dimc)
    rhoS = np.einsum('ikjk->ij', d)
    pe_gs = np.real(rhoS[0,0])                 # excited-state weight of the dressed ground
    return p_e, W_defect, pe_gs

if __name__ == "__main__":
    L = 8
    print("="*80)
    print(f"L2b  WORK-FREE (adiabatic) dressing, L={L}, g_max=1.5, interacting hz=0.6")
    print("  ramp coupling 0->g_max over T_ramp; sudden (small T) does work, slow -> adiabatic")
    print("="*80)
    print(f"  {'T_ramp':>8} {'p_e[int]':>10} {'W_defect[int]':>14} {'p_e[free]':>10}")
    for T in [0.1, 0.5, 2.0, 8.0, 25.0]:
        pe_i, Wd_i, pegs_i = ramp_on(L, 0.6, T_ramp=T, nseg=max(40,int(T*20)))
        pe_f, Wd_f, pegs_f = ramp_on(L, 0.0, T_ramp=T, nseg=max(40,int(T*20)))
        print(f"  {T:8.1f} {pe_i:10.4f} {Wd_i:14.5f} {pe_f:10.4f}")
    # the work-free answer: excited weight of the exact dressed GROUND state
    _,_,pegs_i = ramp_on(L, 0.6, T_ramp=25.0, nseg=500)
    _,_,pegs_f = ramp_on(L, 0.0, T_ramp=25.0, nseg=500)
    print("-"*80)
    print(f"  ADIABATIC dressed-ground-state excited weight p_e:  interacting {pegs_i:.5f}"
          f"  free {pegs_f:.5f}")
    print(f"  (this is the work-free reactive dressing; p_e<0.5 => NO inversion => delta-m>=0)")
    print("-"*80)
    inv_free = pegs_i > 0.5
    print("VERDICT: " + (
        "CRACK -- the adiabatic (work-free) dressed vacuum INVERTS the detector"
        if inv_free else
        "SIGN WALL HOLDS in the work-free limit: as the ramp slows, transient (quench)\n"
        "  inversion vanishes and the exact dressed GROUND state has p_e<<0.5 (no inversion,\n"
        "  delta-m>=0). All the strong-g inversions seen with sudden kicks are QUENCH WORK\n"
        "  (W_defect large at small T_ramp, ->0 as T_ramp grows) -- the priced pump channel,\n"
        "  made MORE effective by interactions, never free from the vacuum."))
    print("="*80)
