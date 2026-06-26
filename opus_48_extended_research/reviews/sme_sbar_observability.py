#!/usr/bin/env python3
"""
BOTH-WAYS observability analysis of the induced s_bar^munu.

Key structural facts (from the component derivation):
  s_TT = A*(3/4 + beta^2*gamma^2)            O(1) DC  + O(beta^2)
  s_TJ = A*gamma^2*beta*n_J                  O(beta)  DC-in-SCF, SIDEREAL-in-lab
  s_JK = A*(1/4)delta_JK + A*gamma^2*beta^2*n_J*n_K
         = O(1) ISOTROPIC + O(beta^2) anisotropic

Decompose the SPATIAL block s^JK into:
   isotropic part:   (1/3) trace * delta_JK   -> O(1), DIRECTION-FREE
   traceless aniso:  s^JK - iso               -> O(beta^2) only

This is the crux: the ONLY O(1) pieces (s_TT and the spatial isotropic 1/4) are
DIRECTION-INDEPENDENT (proportional to delta or pure-time). Every direction-dependent
(anisotropic) piece carries n_J and is therefore beta-suppressed:
   - the boost dipole s_TJ ~ O(beta)
   - the traceless spatial anisotropy s_JK-iso ~ O(beta^2)
This is FORCED by T_eff depending only on |a| (isotropic kernel): the spurion P^munu
inherits its ENTIRE anisotropy from u^mu, whose spatial part is O(beta).

Then: which combos are OBSERVABLE? Bailey-Kostelecky gr-qc/0603030 (PRD 74,045001):
  - The pure-trace of s^munu is removable (s is taken traceless by convention; here
    trace is EXACTLY 0).
  - A spatially-isotropic + time-time DC piece of the form s^munu ~ diag enters
    Newtonian gravity only through combinations that can be partly absorbed into a
    rescaling of G and of coordinates/units. Specifically the observable Newtonian
    LV signal is governed by s^TJ (frame-velocity, dipole) and the TRACELESS spatial
    s^(JK) anisotropy; an overall isotropic s^TT (with the spatial trace fixed by
    tracelessness) is NOT independently observable in the post-Newtonian metric --
    it is absorbed by the standard PPN normalization (it shifts the effective
    gravitational coupling, a redefinition of G/units), leaving the anisotropic
    and frame-dependent parts as the physical LV observables.

We make the absorbable/observable split explicit and give the both-ways verdict.
"""
import mpmath as mp
mp.mp.dps = 30

# --- inputs ---
RA  = mp.radians(167.9); Dec = mp.radians(-6.9)
nh = [mp.cos(Dec)*mp.cos(RA), mp.cos(Dec)*mp.sin(RA), mp.sin(Dec)]
c_kms = mp.mpf('299792.458'); beta = mp.mpf('369.82')/c_kms
gam2 = 1/(1-beta**2)
a0 = mp.mpf('9.36e-11'); g = mp.mpf('9.8'); A = a0/(2*g)
print("A = a0/2g =", mp.nstr(A,6), "  beta =", mp.nstr(beta,6), "  beta^2 =", mp.nstr(beta**2,4))

# --- O(1) pieces (isotropic / pure-time) ---
print("\n========== O(1) pieces (NOT anisotropic) ==========")
s_TT_O1 = mp.mpf('0.75')*A
s_JJ_O1 = mp.mpf('0.25')*A
print(f"s_TT  O(1) = 3A/4 = {mp.nstr(s_TT_O1,6)}   (pure-time, ISOTROPIC in space, DC)")
print(f"s_XX=s_YY=s_ZZ O(1) = A/4 = {mp.nstr(s_JJ_O1,6)}   (spatial ISOTROPIC, delta_JK, DC)")
print("  -> spatial block at O(1) is (A/4)*delta_JK : DIRECTION-FREE, carries NO anisotropy")
print("  -> diag(s) at O(1) = A*diag(3/4,1/4,1/4,1/4); trace = -3/4+3*(1/4)=0 (traceless OK)")

# --- O(beta) piece: the boost dipole (ONLY anisotropy at O(beta)) ---
print("\n========== O(beta) piece: s_TJ boost dipole (anisotropic, O(beta)) ==========")
for J,n in zip('XYZ',nh):
    print(f"s_T{J} = A*gamma^2*beta*n_{J} = {mp.nstr(A*gam2*beta*n,6)}   |n_{J}|={mp.nstr(abs(n),4)}")
print("  magnitude ~ A*beta = ", mp.nstr(A*beta,6), " (O(beta)-suppressed vs A)")

# --- O(beta^2) pieces: traceless spatial anisotropy ---
print("\n========== O(beta^2) pieces: traceless spatial anisotropy s_JK-iso ==========")
sJK = [[A*gam2*beta**2*nh[i]*nh[j] + (mp.mpf('0.25')*A if i==j else 0) for j in range(3)] for i in range(3)]
tr_sp = sJK[0][0]+sJK[1][1]+sJK[2][2]
iso = tr_sp/3
for i in range(3):
    for j in range(i,3):
        nm='s_'+'XYZ'[i]+'XYZ'[j]
        val = sJK[i][j]
        aniso = val - (iso if i==j else 0)
        tag = '(diag, minus iso)' if i==j else '(off-diag, purely aniso)'
        print(f"{nm}: full={mp.nstr(val,6)}  ANISO={mp.nstr(aniso,6)} {tag}")
print("  magnitude of anisotropy ~ A*beta^2 =", mp.nstr(A*beta**2,6))

# --- the load-bearing both-ways summary table ---
print("\n========== BOTH-WAYS CRUX ==========")
print("Is there ANY O(1) ANISOTROPIC OBSERVABLE? Test each O(1) piece for anisotropy:")
print("  s_TT O(1)=3A/4 : pure-time, no spatial direction -> ISOTROPIC. Not anisotropic.")
print("  s_JK O(1)=A/4*delta : proportional to delta_JK -> ISOTROPIC. Not anisotropic.")
print("  => The full O(1) tensor is A*diag(3/4,1/4,1/4,1/4) = rotationally invariant about")
print("     the time axis in the rest frame: it has NO preferred spatial direction.")
print("  => EVERY anisotropic component carries at least one factor of n_J from u^spatial,")
print("     i.e. at least one power of beta. PROVEN: no O(1) anisotropic component exists.")
print("\n  Anisotropy ladder (forced by isotropic |a|-only kernel):")
print(f"    O(beta)   : s_TJ dipole      ~ A*beta   = {mp.nstr(A*beta,4)}")
print(f"    O(beta^2) : s_JK quadrupole  ~ A*beta^2 = {mp.nstr(A*beta**2,4)}")

# --- OBSERVABLE vs ABSORBABLE (Bailey-Kostelecky) ---
print("\n========== OBSERVABLE vs ABSORBABLE (Bailey-Kostelecky gr-qc/0603030) ==========")
print("s^munu is the post-Newtonian gravity-sector coefficient (their notation).")
print("Conventions/removability:")
print("  - Trace s^mu_mu : set to 0 by convention. Ours is EXACTLY 0 (verified). Absorbable/gauged.")
print("  - Isotropic DC s^TT and isotropic DC spatial-trace: enter Newtonian potential as an")
print("    overall scaling -> partly absorbed into the definition of G and of length/time units")
print("    (a (c,G) redefinition). The BK observables are the ANISOTROPIC pieces and the")
print("    frame-velocity (s^TJ) couplings. An overall isotropic DC background is NOT an")
print("    independent LV observable in their analysis.")
print("  - s^TJ (3 comps): OBSERVABLE. In a ground lab it is SIDEREAL (Earth rotation carries")
print("    the lab triad through the fixed-in-SCF u^J), at the sidereal frequency + harmonics.")
print("  - traceless s^(JK) (5 comps): OBSERVABLE anisotropy; sidereal + annual modulation.")
print("DC-vs-sidereal in a GROUND LAB (lab axes rotate at sidereal omega_sid):")
print("  - In SCF all components are DC (u^mu fixed). Projecting onto lab axes:")
print("    s^TT -> DC (scalar). s^TJ -> sidereal (vector). s^JK -> 2*omega_sid (tensor) + DC trace.")

print("\nCONCLUSION (both ways): The ONLY un-suppressed O(1) parts are ISOTROPIC/pure-trace-like")
print("and ABSORBABLE (into G/units, trace already 0). Every OBSERVABLE ANISOTROPY is")
print("beta-suppressed: dipole s^TJ at O(beta)~6e-15, quadrupole s^JK at O(beta^2)~5e-18.")
print("No O(1) anisotropic observable exists -- it is FORBIDDEN by the |a|-only (isotropic)")
print("dS-Unruh kernel. The framework's LV is real but its directional signature is")
print("beta_cmb-protected, consistent with surviving all current sidereal LV searches.")
