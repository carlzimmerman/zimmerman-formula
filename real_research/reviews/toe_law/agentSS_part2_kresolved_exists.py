"""
agentSS Part 2 -- DOES a k-RESOLVED clamp exist that holds ALL poles (center + off-center) in the LHP?
And WHAT k-profile does it need?

A spatially NON-LOCAL saturation gates the gain not by the local intensity |chi(x)|^2 but by a smeared
intensity  Ibar(x) = int d^3x' K(x-x') |chi(x')|^2.  In Fourier space the gain seen by mode k becomes
   Sigma_eff(omega,k) = -R0(k) * gamma/(-i(omega-omega0)+gamma),   R0(k) = s(k)*G(k),
where the clamp factor s(k) is now k-DEPENDENT because the smearing kernel K weights different modes'
contribution to the saturating field differently (per-k gain depletion). The QUESTION of existence:
is there ANY positive profile s(k) in [0,1] that pulls every mode's retarded pole into the closed LHP
WHILE keeping the band-center gain at fold strength (so the fold survives)?

Strategy: at each k, find the MAXIMUM R(k) for which Im(omega_pole)<=0 (the marginal-stability gain
ceiling R_crit(k)). A k-resolved clamp that keeps the pole in the LHP exists iff we can set
R(k) <= R_crit(k) for all k. Then check: does that ceiling still permit a *visible fold* (band-center
gain strong enough)?  We also record the SHAPE of R_crit(k) -- that is the k-profile any deliverer
must match. Finally, separate: EXISTENCE of a stabilizing s(k) (a free-construction question) from
whether the dS heat kernel FORCES that particular shape (Parts 3-5).
"""
import numpy as np

def poles_of_D(wk2, R, omega0, gamma):
    a3 = -1j
    a2 = (1j*omega0 + gamma)
    a1 = (1j*wk2)
    a0 = -(1j*omega0 + gamma)*wk2 + R*gamma
    return np.roots([a3, a2, a1, a0])

def max_im(wk2, R, omega0, gamma):
    return max(r.imag for r in poles_of_D(wk2, R, omega0, gamma))

c=1.0; gamma=0.1; omega0=0.6
wk0sq=omega0**2

# R_crit(k): largest R with max_im<=0 (bisection). For R=0 the pole is the bare LHP (stable, Im<0
# from gamma>0 only if there's loss; here bare D has real roots => Im=0). We seek the gain ceiling.
def Rcrit(wk2, Rlo=0.0, Rhi=2.0, tol=1e-6):
    # at Rlo stable (or marginal), at Rhi unstable presumably; if not unstable at Rhi, return Rhi
    if max_im(wk2,Rhi,omega0,gamma) <= 0:
        return Rhi
    lo,hi=Rlo,Rhi
    for _ in range(60):
        mid=0.5*(lo+hi)
        if max_im(wk2,mid,omega0,gamma) <= 0:
            lo=mid
        else:
            hi=mid
    return 0.5*(lo+hi)

print("=== R_crit(k): marginal-stability gain ceiling vs k ===")
print(" k       wk2     R_crit(k)   (max gain that keeps the retarded pole in the closed LHP)")
ks=np.linspace(0.0,1.4,29)
rc=[]
for k in ks:
    wk2=k**2
    r=Rcrit(wk2)
    rc.append(r)
    print(f" {k:5.3f}  {wk2:6.3f}   {r:8.4f}")
rc=np.array(rc)

# Is there room for a VISIBLE fold? The fold needs a strong, peaked gain near the band center.
# A k-resolved clamp can set R(k)=R_crit(k) (ride the ceiling). The dispersive (Re-Sigma) fold from
# R(k)=R_crit(k): does it still bend? Compute omega^2(k) = c^2 k^2 + Re Sigma at the stable ceiling.
# Re Sigma at omega->0 (static, IR fold) for the active line: Re Sigma(0,k) = -R(k)*gamma^2/(omega0^2+gamma^2)
print("\n=== Ride-the-ceiling dispersion: does the LHP-stable profile still fold? ===")
def reSig_static(R):
    # Re of -R*gamma/(-i(0-omega0)+gamma) = -R*gamma*(gamma)/ (omega0^2+gamma^2)  [real part]
    # -R*gamma/(i omega0 + gamma) = -R*gamma*(gamma - i omega0)/(gamma^2+omega0^2)
    return -R*gamma*gamma/(gamma**2+omega0**2)
om2_ceiling=[]
for k,r in zip(ks,rc):
    om2 = c**2*k**2 + reSig_static(r)
    om2_ceiling.append(om2)
om2_ceiling=np.array(om2_ceiling)
vg2=np.gradient(om2_ceiling, ks**2)   # d omega^2/d(k^2) ~ group-velocity^2 proxy
print(" k      omega^2(ride ceiling)    d(om2)/d(k2)")
for i,k in enumerate(ks):
    print(f" {k:5.3f}   {om2_ceiling[i]:+10.5f}        {vg2[i]:+8.4f}")
print(f"\nmin d(om2)/d(k2) along the stable ceiling = {vg2.min():+.4f}")
print("  (<0 => a fold survives even while every pole stays in the LHP -- a k-resolved clamp CAN")
print("   stabilize AND fold. >=0 => riding the stability ceiling kills the fold.)")
print("\nNOTE: this only shows a stabilizing s(k) EXISTS (free construction). Whether the dS heat")
print("kernel FORCES the shape s(k)=R_crit(k)/G(k) is the separate, load-bearing question (Parts 3-5).")
