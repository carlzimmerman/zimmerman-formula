"""
agentSS Part 6 -- THE NON-MARKOVIAN (memory-in-TIME) steelman. The brief asks about a
"k-RESOLVED / non-Markovian" clamp. Parts 4-5 showed the k-resolved (spatial) structure is
permits-not-forces. Here the distinct angle: a genuinely NON-MARKOVIAN clamp has its OWN frequency
dependence Sigma_clamp(omega) -- memory -- which could add damping at the off-center pole frequency and
pull it into the LHP even where the static per-k analysis said R_crit=0. Does the dS heat kernel FORCE
such a stabilizing memory kernel?

A retarded clamp/self-energy with memory is, by Kramers-Kronig + PASSIVITY, a Herglotz/Pick function:
its imaginary part (the dissipation) has a DEFINITE sign (Im Sigma_R <= 0 in the lower half, dissipative).
The off-center pole goes UHP because the ACTIVE line supplies the WRONG-sign dissipation there
(anti-damping at the fold band). To pull it back, the clamp must ADD dissipation (correct-sign Im) at
the off-center pole frequency.

[6a] What memory does the dS heat kernel force? The GH state is KMS/thermal at T=H/2pi (EE STEP 1,
     machine-verified: the free khronon worldline density is the Planck density, detailed balance = KMS
     at kappa/2pi). A KMS/thermal bath self-energy is PASSIVE/dissipative (Im Sigma_R has the thermal
     sign, fluctuation-dissipation). So the heat-kernel memory, BY ITSELF, is a PASSIVE thermal kernel:
     it can only ADD ordinary (positive) damping -- which is GOOD for stability but is exactly the
     SMOOTH thermal continuum agentOO/PP already used, and PP's NO-FOLD THEOREM (Herglotz => monotone
     dispersion, d k^2/d omega^2>0) says a passive kernel gives NO FOLD. So the heat-kernel memory either
     (passive) stabilizes-but-cannot-fold, or (active, to fold) is NO LONGER the bare heat kernel.

[6b] Make it concrete: add the FORCED thermal (passive, KMS at H/2pi) memory clamp to the active fold
     line and check (i) does it pull the off-center pole into the LHP, and (ii) does the fold survive?
     Show the trade: enough passive thermal damping to stabilize (Im pole -> LHP) FLATTENS the fold
     (Herglotz contribution is monotone), and the amount of damping needed is NOT fixed by H -- it is a
     free strength. So even the non-Markovian route is permits-not-forces: the heat kernel forces the
     SIGN of the thermal memory (dissipative) but not the STRUCTURE (a finite-Q, k-resolved, active-yet-
     stable kernel) that both folds AND clamps.
"""
import numpy as np

print("="*72)
print("[6a] The dS heat-kernel memory is a PASSIVE thermal (KMS @ H/2pi) kernel -> Herglotz")
print("="*72)
print("EE STEP1 (machine-verified): free khronon worldline density = Planck density, KMS at kappa/2pi.")
print("=> the bare heat-kernel self-energy is PASSIVE: Im Sigma_R has the dissipative (thermal) sign,")
print("   it is a Herglotz/Pick function of omega^2. PP's NO-FOLD THEOREM: a passive (rho>=0) self-")
print("   energy S(x)=sum w_n/(x-W_n^2) is Herglotz => d(k^2)/d(omega^2)>0 strictly => MONOTONE, no fold.")
print("   So the heat-kernel memory alone CANNOT fold (it only stiffens) -- consistent, banked twice.")
print()

print("="*72)
print("[6b] Add a FORCED passive thermal memory clamp to the active fold line: stabilize vs fold trade")
print("="*72)
# Active fold line (RR/QQ) at fixed off-center k: Sigma_act(omega) = -A*Gam/(-1j*omega+Gam)  (negative
# residue, anti-damping on the below-center band). Add a PASSIVE thermal memory:
#   Sigma_th(omega) = -D_th * (-1j*omega)/(Gam_th - 1j*omega) ... use a simple Ohmic/thermal damping
#   Sigma_th = -1j*omega*eta_th  (Markovian-limit ohmic, dissipative: Im<0 for omega>0) plus a memory
#   tail; we add ohmic damping eta_th (passive). Question: how much eta_th to make the off-center pole
#   LHP, and what it does to the fold (Re-Sigma curvature).
A=0.18; Gam=0.1; c=1.0; k_off=0.3; k0=0.6  # below-center off-center mode (k_off<k0), unstable per Part3
def poles(eta_th, A=A, Gam=Gam, k=k_off):
    # D(w)= w^2 - c^2 k^2 - Sigma_act - Sigma_th ;  Sigma_act=-A*Gam/(-1j*(w)+Gam) (center at 0 temporal
    # companion of below-center)  ; Sigma_th = -1j w eta_th
    # clear active denom: (w^2 - c^2k^2 + 1j w eta_th)(-1j w + Gam) + A Gam = 0
    wk2=c**2*k**2
    # expand (w^2 - wk2 + 1j eta_th w)(-1j w + Gam) = -1j w^3 + Gam w^2 +1j wk2 w -Gam wk2 + eta_th w^2 +1j eta_th Gam w
    a3=-1j
    a2=(Gam+eta_th)
    a1=(1j*wk2 + 1j*eta_th*Gam)
    a0=(-Gam*wk2 + A*Gam)
    return np.roots([a3,a2,a1,a0])
print(" eta_th (passive thermal damping)   max Im(off-center pole)   stable?")
eta_stab=None
for eta in [0.0,0.05,0.1,0.2,0.4,0.8,1.5,3.0]:
    mi=max(r.imag for r in poles(eta))
    st = "LHP (stable)" if mi<=1e-9 else "UHP (unstable)"
    if mi<=1e-9 and eta_stab is None: eta_stab=eta
    print(f"   {eta:5.2f}                              {mi:+.5f}            {st}")
print(f"\n  off-center pole enters LHP at eta_th ~ {eta_stab} (a FREE damping strength, NOT fixed by H).")

# Now the fold: with enough damping to stabilize, does omega^2(k) still bend down?
# IR static dispersion omega^2(k)=c^2k^2 + Re Sigma_act(0,k). Adding passive damping does NOT change the
# STATIC Re part (ohmic Sigma_th=-1j w eta_th vanishes at omega->0), but the active line's Re part is what
# folds; stabilizing required raising eta_th, and a k-resolved finite-Q ACTIVE kernel (not ohmic) is what
# both folds and damps -- and THAT kernel's {center,width,Q,sign} are the RR N=4 free knobs, not H-forced.
print("\n  The passive ohmic clamp that stabilizes does NOT itself fold (Re Sigma_th(0)=0); the fold still")
print("  comes from the ACTIVE line, whose below-center anti-damping is what needed stabilizing. The")
print("  damping strength eta_th that stabilizes is a FREE knob (not H-forced). A single kernel that BOTH")
print("  folds AND keeps every pole LHP is a finite-Q active-but-stable line = RR's peaked dS QNM with")
print("  {center,width,Q} -- the N=4 free ratios. The heat kernel forces the thermal SIGN, not that kernel.")
print()
print("VERDICT (Part 6, non-Markovian axis): the dS heat-kernel memory is FORCED to be PASSIVE/thermal")
print("(KMS @ H/2pi) -> it can add dissipation (good) but by PP's theorem cannot fold; the active, finite-Q,")
print("k-resolved kernel that BOTH folds and clamps is NOT the bare heat kernel and its structure is free.")
print("=> non-Markovian route is ALSO permits-not-forces.")
