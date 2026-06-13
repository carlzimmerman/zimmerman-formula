"""
agentRR Part 9c -- get the PASSIVE/ACTIVE sign RIGHT from Im Sigma, then redo the pole test.
A self-energy Sigma_R(w) is PASSIVE (dissipative) iff Im Sigma_R(w) > 0 for w>0 (with our retarded
metric where the damped oscillator chi_R=1/(wr^2-w^2-i gamma w) has Im chi_R>0 for w>0). Check the
sign of Im Sigma for Sigma = s*wr^2*chi_R and find which sign s is passive. Then a PASSIVE Sigma must
give LHP khronon poles -- verify -- and the ACTIVE sign (the other s) is the one QQ needs.

Crucially also test: maybe the previous 'UHP for passive' was real and the khronon propagator
w^2 - wk^2 - Sigma is just not the right object -- the physical retarded GF for a field is
G_R = 1/(w^2 - wk^2 - Sigma) ONLY if the sign of Sigma is fixed so that Sigma reduces the restoring.
Let's just directly map: dressed dispersion w^2 = wk^2 + Sigma_R(w). Poles where this holds. Compute.
"""
import numpy as np

wr,gamma=0.6,0.1
w=np.linspace(0.01,2.0,9)
chiR = 1.0/(wr**2 - w**2 - 1j*gamma*w)
print("Im chi_R(w) for w>0 (sign of dissipation):", np.round(chiR.imag,4))
print("  Im chi_R > 0 for w<wr, <0 for w>wr -- it CHANGES sign at resonance. So 'Im Sigma>0=passive'")
print("  is band-dependent. Passivity is global: Sigma must be a positive-definite spectral measure.")
print()

# The clean test: build Sigma from a POSITIVE spectral density (passive) and from a NEGATIVE one
# (active), via Kramers-Kronig, and check pole location. Passive: rho(W)>=0.
# Sigma_R(w) = (1/pi) \int rho(W) / (W - w - i0) dW  (retarded). Single line rho(W)=pi R [delta(W-wr)-delta(W+wr)]/(2wr)*...
# Simpler & rigorous: the damped HO with POSITIVE coupling lambda^2>0 to the khronon is passive:
#   Sigma_R(w) = lambda^2 / (wr^2 - w^2 - i gamma w).   (lambda^2>0 = passive coupling)
# Dressed: w^2 - wk^2 - Sigma_R = 0. This is the standard two-coupled-oscillator (passive) problem;
# its poles MUST be LHP. Let's verify with lambda^2>0.
def poles(wk2,lam2,wr,gamma):
    # (w^2-wk2)(wr^2-w^2-i gamma w) - lam2 = 0
    a4=-1.0
    a3=-1j*gamma
    a2=(wr**2+wk2)
    a1=(1j*gamma*wk2)
    a0=(-wk2*wr**2 - lam2)
    return np.roots([a4,a3,a2,a1,a0])

print("=== PASSIVE coupling lambda^2>0 (two coupled oscillators, must be LHP) ===")
worst=-1e9; argw=None
for lam2 in [0.001,0.01,0.05,0.1,0.2]:
    for wk2 in np.linspace(0.0,1.5,400):
        ps=poles(wk2,lam2,wr,gamma)
        m=max(p.imag for p in ps)
        if m>worst: worst=m; argw=(lam2,wk2,ps)
print(f"  max Im(pole) over lambda^2>0: {worst:+.6f}")
if worst>1e-6:
    lam2,wk2,ps=argw
    print(f"  WORST at lam2={lam2}, wk2={wk2}: poles={[f'{p:.4f}' for p in ps]}")
    print("  If this is >0, my quartic is still wrong. Let me check a SINGLE point by hand.")
    # hand check: wk2=0.5, lam2=0.1, wr=0.6, gamma=0.1
    import numpy as _np
    wk2h,lam2h=0.5,0.1
    # define D(w) and find roots by dense scan of |D| in complex plane
    def D(wc): return wc**2 - wk2h - lam2h/(wr**2 - wc**2 - 1j*gamma*wc)
    # Newton from several seeds
    from numpy.polynomial import polynomial as PP
    # direct: multiply out -- use the SAME quartic
    ps2=poles(wk2h,lam2h,wr,gamma)
    print(f"  hand point quartic roots: {[f'{p:.5f}' for p in ps2]}")
    print(f"  residual |D(root)|: {[f'{abs(D(p)):.2e}' for p in ps2]}")
