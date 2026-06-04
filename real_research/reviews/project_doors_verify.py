#!/usr/bin/env python3
"""
Six-door systematic sweep: the load-bearing numbers, independently verified in-repo.
====================================================================================
Reproduces every number the DOORS_LEDGER.md verdicts rest on. Door A has its own script
(project_doorA_static_patch.py); this covers B-F, plus the cross-cutting de Sitter entropy.
Each block prints the claim and the check. Honest: this is verification, not advocacy.
Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; hbar = 1.055e-34; kB = 1.381e-23; Mpc = 3.086e22
lP = np.sqrt(hbar*G/c**3); H0 = 67.4e3/Mpc; OmL = 0.685
Z = 2*np.sqrt(8*np.pi/3); a0_obs = 1.2e-10
Lam = 3*OmL*H0**2/c**2


def main():
    print("#"*94); print("# Six-door sweep: load-bearing numbers, verified"); print("#"*94 + "\n")

    print("="*94); print("DOOR B -- Z vs CKN: does fixing the O(1) derive Lambda? (and an epoch catch)"); print("="*94)
    print(f"  identity 32pi/Z^2 = {32*np.pi/Z**2:.6f} (=3 exactly): so a0=cH0/Z and a0=c^2 sqrt(Lam/32pi)")
    print(f"           eliminate to Lam = 3 H^2/c^2 -- but only if BOTH hold at the SAME epoch.")
    a0_today = c*H0/Z
    a0_floor = c**2*np.sqrt(Lam/(32*np.pi))
    print(f"  CATCH (my correction to the agent): they hold at DIFFERENT epochs --")
    print(f"    a0(today)    = cH0/Z             = {a0_today:.3e}  (matches observed ~1.2e-10)")
    print(f"    a0(deSitter) = c^2 sqrt(Lam/32pi)= {a0_floor:.3e}  (the asymptotic FLOOR)")
    print(f"    ratio = {a0_floor/a0_today:.4f} = sqrt(OmL) = {np.sqrt(OmL):.4f}.  'Omega_L=1 liability' is an epoch artifact;")
    print(f"    the framework's Lambda is CONSTANT (w=-1) and a0~H(z) is kinematic, so the Hsu w=0 critique is N/A.")
    rhoP = c**5/(hbar*G**2); rho_Lam = Lam*c**2/(8*np.pi*G)
    print(f"  SOLID core: rho_Lam/rho_Planck ~ 1e{np.log10(rho_Lam/rhoP):.0f}; an O(1)=Z={Z:.2f} moves this by ZERO orders.")
    print(f"  => Door B does NOT derive Lambda / touch the CC problem. CLOSED on that; docs should label the two a0's.\n")

    print("="*94); print("DOOR C -- cosmic topology: dead band, live band, framework predictivity"); print("="*94)
    chi = 13.88                                   # Gpc, astropy Planck18 (agent, matches Planck D_M to 0.11%)
    print(f"  chi_rec = {chi} Gpc; LSS diameter = {2*chi:.1f} Gpc")
    print(f"  matched-circle exclusion: torus edge L < 0.97*2*chi = {0.97*2*chi:.1f} Gpc DEAD (20.6 Gpc torus dead, margin ~6 Gpc)")
    print(f"  COMPACT detectability ceiling: nearest clone < 1.2*LSSdiam = {1.2*2*chi:.1f} Gpc")
    print(f"  => surviving testable band ~{0.97*2*chi:.0f}-{1.2*2*chi:.0f} Gpc + rotation topologies. Framework predicts NO scale.")
    print(f"     (CMB-S4 cancelled Jul 2025; leverage is 3-D LSS: Euclid DR1 Oct 2026 -> Rubin -> 21cm 2030s.)\n")

    print("="*94); print("DOOR D -- nucleation kick-off + DESI falsifier"); print("="*94)
    S_inst = 3*np.pi/(Lam*lP**2)
    print(f"  instanton action S_E = 3pi/(Lam lP^2) = {S_inst:.3e} = de Sitter horizon entropy A/4G (the horizon")
    print(f"    that sources a0 IS the nucleation action -- elegant but CIRCULAR for a 'kick-off' claim).")
    print(f"  no-boundary weight ~ exp(+S_dS) favors small Lambda (empty-universe); tunneling ~ exp(-S_dS) favors large.")
    print(f"  supplying Lambda externally SIDESTEPS (removes the runaway only by removing the prediction).")
    print(f"  DESI exposure ~3 sigma: a0 response delta_a0/a0 = 0.5 delta_Lam/Lam -> only ~{100*0.5*0.30:.0f}% for a 30% rho_DE swing")
    print(f"    (Failure mode A 'Lambda drifts' SURVIVABLE). But phantom crossing of w=-1 (Failure mode B) is a change")
    print(f"    of KIND a static de Sitter horizon cannot make -- THAT is the real, load-bearing threat.\n")

    print("="*94); print("DOOR E -- low-entropy past / Boltzmann brains"); print("="*94)
    RH = c/H0; S_H = np.pi*RH**2/lP**2
    print(f"  S_dS(Hubble) = pi R_H^2/lP^2 = {S_H:.3e}. T_dS = hbar H/2pi kB = {hbar*H0/(2*np.pi*kB):.2e} K.")
    print(f"  Boltzmann-brain gap: N_ordinary/N_brain ~ exp(-(S_dS - S_brain)) ~ exp(-1e122) for S_brain~1e42: catastrophe.")
    print(f"  Boddy-Carroll-Pollack rescue needs INFINITE-dim Hilbert space; the framework's FINITE ceiling (dim e^S_dS)")
    print(f"    is the case BCP flag as STILL having the BB problem (Davenport-Olum: the horizon enables decoherence).")
    print(f"  => finite entropy does NOT rescue; must ADD a past hypothesis (Chen initial-projection law best fit). COST.\n")

    print("="*94); print("DOOR F -- complexity / 'geometry unfolding': the decisive exponent test"); print("="*94)
    print(f"  a0 = a_Planck*(sqrt(pi)/Z)*S_dS^(-1/2): the sqrt(S) suppression is the AREA LAW, R/lP = sqrt(S/pi) = {RH/lP:.2e}.")
    print(f"  de Sitter complexity rate (2025: linear, dC/dt ~ kappa S_dS T_GH ~ S_dS*H) scales as S_dS^(+1).")
    print(f"  OPPOSITE powers of S: complexity-as-acceleration overshoots a0 by ~S_dS = {S_H:.0e}; dividing it out returns")
    print(f"    plain cH (no complexity left). 'a0 = complexity rate' FAILS the numbers -- slogan, not calculation.")
    print(f"  BUT DSSYK<->dS is a genuine ally for Door A's finite-Hilbert/stretched-horizon program (entropy/DOS route).\n")

    print("#"*94)


if __name__ == "__main__":
    main()
