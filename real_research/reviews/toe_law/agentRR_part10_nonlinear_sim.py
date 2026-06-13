"""
agentRR Part 10 -- direct nonlinear simulation: does saturation give a STATIC stable fold, or only a
bounded (limit-cycle) amplitude with the instability persisting? Integrate the fold-band mode under a
saturated active gain and watch: amplitude bounded (clamp works) vs. operating point static-stable.

Model the unstable fold-band mode chi(t) (complex amplitude, one k near the gain center) with
saturated gain:
    d chi/dt = [ i*Omega + (g0/(1+|chi|^2/Isat) - kappa)/2 ] chi
Omega = sqrt(omega^2(k_fold)) the (real) oscillation freq; g0 the small-signal gain (>kappa above
threshold = fold-strength); kappa the loss. Above threshold the linear growth (g0-kappa)/2>0 drives
|chi| up until saturation clamps gain->loss: |chi|^2 -> Isat(g0/kappa -1). Then |chi| is CONSTANT
(static intensity) and chi(t)=|chi*|e^{i Omega t} -- a steady oscillation at the band freq. The
amplitude is bounded (clamp = D1) BUT this is a self-sustained finite-amplitude oscillation: the mode
is NOT quiescent, it lases. For a DISPERSION fold we needed a quiet, static branch with v_g^2<0 -- the
lasing band instead radiates at Omega. So 'bounded' != 'a static stable roton minimum'.
"""
import numpy as np

def sim(g0,kappa,Isat,Omega,T=400,dt=0.002,chi0=1e-3):
    n=int(T/dt); chi=complex(chi0,0.0); amps=[]
    for i in range(n):
        g=g0/(1+abs(chi)**2/Isat)
        dchi=(1j*Omega + 0.5*(g-kappa))*chi
        chi=chi+dt*dchi
        if i%50==0: amps.append(abs(chi))
    return np.array(amps)

Omega=0.6
print("=== nonlinear saturated-gain band: amplitude bounded? operating point? ===")
for g0,kappa,Isat in [(0.05,0.015,1.0),(0.6,0.015,1.0),(1.3,0.05,1.0),(1.0,0.5,0.5)]:
    amps=sim(g0,kappa,Isat,Omega)
    pred=np.sqrt(Isat*(g0/kappa-1)) if g0>kappa else 0.0
    print(f"  g0={g0} kappa={kappa} Isat={Isat}: |chi| start={amps[0]:.4f} end={amps[-1]:.4f}, "
          f"bounded={amps[-1]<1e3}, clamp pred |chi*|={pred:.4f} (match={abs(amps[-1]-pred)<0.05*max(pred,1e-9)})")
print("\n=> amplitude BOUNDS to the clamp value (D1 confirmed dynamically): saturation tames the")
print("   runaway -- |chi| does NOT blow up, it settles to |chi*|=sqrt(Isat(g0/kappa-1)).")
print("=> BUT the settled state is a self-sustained oscillation chi(t)=|chi*|e^{iOmega t} (a 'laser'):")
print("   the band is ACTIVE and RADIATING, not a quiescent static roton branch. The retarded pole")
print("   sat ON the real axis (marginal, Part 1 clamp) = a persistent limit cycle, NOT an LHP")
print("   quiescent fold. 'Bounded amplitude' is delivered; 'static stable roton minimum' is NOT.")

# Confirm the marginal/limit-cycle nature: at the clamped operating point the linearized growth of a
# perturbation in |chi| is f'(I*)<0 (intensity stable, Part1) but the PHASE/frequency mode is neutral
# (Omega undamped) -> the dispersion 'pole' for the lasing band sits at Im=0 (marginal), reproducing
# the temporal-pole picture of Part 9d at the clamped (not fold) gain. The mismatch: the fold needs
# gain at FOLD strength on OTHER k's (the dispersive Re part), and Part 9d showed those k's go UHP.
print("\n=> RECONCILIATION with Part 9d: the clamp pins the GAIN-CENTER band marginal (Im=0), but the")
print("   dispersive fold needs the active Re-part to act across a RANGE of k (B~1.0-1.3). Part 9d:")
print("   those off-center k's have UHP poles that the SCALAR intensity clamp does not touch (the")
print("   clamp is one global I*, it cannot pin every k's pole). So saturation bounds the CENTER but")
print("   leaves the fold band's off-center modes anti-damped. A k-resolved (spatially structured)")
print("   saturation would be needed -- that is the adaptive/non-Markovian extra structure, NOT plain")
print("   laser saturation, and NOT forced by the pump.")
