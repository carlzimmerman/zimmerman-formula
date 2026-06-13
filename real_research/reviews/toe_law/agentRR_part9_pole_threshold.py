"""
agentRR Part 9 -- rigorous retarded-pole stability of the active line, with sign convention pinned
against a PASSIVE reference, then the actual UHP threshold R_inst and whether the saturation clamp
sits below it.

Retarded self-energy of a single damped oscillator line (causal, analytic in UHP):
    Sigma_R(w) = R * w_r^2 / (w_r^2 - w^2 - i*gamma*w),   gamma>0.
PASSIVE: R>0 (positive residue, absorptive Im Sigma>0 for w>0). ACTIVE: R<0 (negative residue,
the QQ Route-2 active sign). Retarded propagator D(w) = w^2 - wk^2 - Sigma_R(w). Stability = all
roots of D(w)=0 have Im(w)<=0 (poles of G_R=1/D in LHP).

Step 1: pin convention -- a PASSIVE line (R>0) MUST give all poles in LHP for any R (no instability
ever). Verify. Step 2: ACTIVE line (R<0): find R_inst where a pole crosses into UHP. Step 3: relate
R to the clamp: saturation holds the in-band gain at g_eff=kappa (Part1). Is |R_clamp| < |R_inst|?
"""
import numpy as np

def poles(wk2, R, wr, gamma):
    # D(w)*(wr^2 - w^2 - i gamma w) = 0 :
    # (w^2 - wk2)(wr^2 - w^2 - i gamma w) - R wr^2 = 0  -> quartic in w
    # expand: (w^2-wk2)(-w^2 - i gamma w + wr^2) - R wr^2
    # = -w^4 - i gamma w^3 + wr^2 w^2 + wk2 w^2 + i gamma wk2 w - wk2 wr^2 - R wr^2
    a4=-1.0
    a3=-1j*gamma
    a2=(wr**2+wk2)
    a1=(1j*gamma*wk2)
    a0=(-wk2*wr**2 - R*wr**2)
    return np.roots([a4,a3,a2,a1,a0])

wr, gamma = 0.6, 0.1

# Step 1: passive reference R>0 -- expect all LHP
print("=== Step 1: PASSIVE line R>0 (must be all-LHP for any R, any wk2) ===")
worst_passive=-1e9
for R in [0.001,0.01,0.1,0.5,1.0,5.0]:
    for wk2 in np.linspace(0,1.5,200):
        worst_passive=max(worst_passive,max(p.imag for p in poles(wk2,R,wr,gamma)))
print(f"  max Im(pole) over passive R up to 5: {worst_passive:+.6f}  (expect <=0 => convention OK)")

# Step 2: ACTIVE line R<0 -- find UHP threshold
print("\n=== Step 2: ACTIVE line R<0 -- UHP threshold ===")
for R in [-0.001,-0.005,-0.01,-0.015,-0.02,-0.03,-0.05,-0.1]:
    worst=-1e9; wk_at=None
    for wk2 in np.linspace(0,1.5,400):
        m=max(p.imag for p in poles(wk2,R,wr,gamma))
        if m>worst: worst=m; wk_at=wk2
    flag="UHP-UNSTABLE" if worst>1e-9 else "stable(LHP)"
    print(f"  R={R:+.4f}: max Im(pole)={worst:+.6f} at wk^2={wk_at:.3f}  -> {flag}")

# Step 3: pinpoint R_inst (active threshold)
print("\n=== Step 3: active UHP threshold R_inst (bisection) ===")
def maxim(R):
    w=-1e9
    for wk2 in np.linspace(0,1.5,400):
        w=max(w,max(p.imag for p in poles(wk2,R,wr,gamma)))
    return w
lo,hi=-0.001,-0.1  # maxim(lo)<0, maxim(hi)>0 expected
# ensure bracket
if maxim(lo)>0:
    print("  even tiny active gain is UHP at this wr,gamma -- active line unstable from R->0-")
    Rinst=0.0
else:
    for _ in range(60):
        mid=(lo+hi)/2
        if maxim(mid)>0: hi=mid
        else: lo=mid
    Rinst=(lo+hi)/2
    print(f"  R_inst (active) ~ {Rinst:.5f}  (|R|>|R_inst| => UHP runaway)")

print("\n=== relation to the saturation clamp ===")
print("Part 1: above-threshold steady state clamps the *in-band* gain to the loss, g_eff(I*)=kappa.")
print("The clamp fixes the OPERATING in-band gain, NOT the negative-residue strength R that the")
print("dispersive (sigma4/sigma6) fold needs. The fold required |R|~y~1.0-1.3 (Part 7,8): FAR above")
print(f"|R_inst|~|{Rinst:.4f}|. So the fold-strength active response is DEEP in the UHP-unstable regime")
print("of the bare retarded propagator -- the clamp tames the AMPLITUDE (limit cycle) but does NOT")
print("move the LINEAR retarded pole back to the LHP. This is the crux: saturation bounds |chi| but a")
print("LINEAR perturbation about the operating point still sees the same UHP pole => convective/")
print("absolute instability of the fold band unless the clamp is ALSO frequency-structured (non-Markov).")
