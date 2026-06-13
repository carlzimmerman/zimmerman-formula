"""
agentSS Part 1 -- PIN THE FAILURE. Reproduce RR's result that a SCALAR (k-independent) intensity
clamp leaves the off-center fold-band retarded pole in the UHP, and isolate the MECHANISM: the clamp
multiplies the gain by the SAME factor s = 1/(1+I_tot/I_sat) for every k, so it cannot reshape the
k-profile of the gain -- it only rescales it. The off-center modes (k != gain center k0) keep the
active (negative-residue) self-energy that, at fold strength, sits a retarded pole in the UHP.

Model (RR Route 1 / QQ): retarded inverse propagator
   D(omega,k) = omega^2 - c^2 k^2 - Sigma(omega,k),
with the in-medium gain a peaked active line. In the TEMPORAL channel at fixed k the clamped active
line is
   Sigma(omega) = -R(k) * gamma / ( -i(omega - omega0) + gamma )   (causal/retarded; pole of Sigma in LHP)
R(k) = s * G(k), s = scalar clamp factor (same for all k), G(k) = bare gain profile peaked at k0.
We find roots of D(omega,k)=0 (a cubic after clearing the denominator) and read max Im(omega_pole).

Scalar clamp: s is a single number set by gain=loss at the OPERATING (band-center) mode. We then ask:
does that same s keep Im(omega_pole) <= 0 at OFF-CENTER k (where the propagator's real part c^2 k^2 is
detuned from the gain center)?  RR's answer: NO. We reproduce and, crucially, DIAGNOSE why.
"""
import numpy as np

def poles_of_D(wk2, R, omega0, gamma):
    # D(w) = w^2 - wk2 - Sigma(w),  Sigma(w) = -R*gamma/(-1j*(w-omega0)+gamma)
    # clear denom: (w^2 - wk2)*(-1j*(w-omega0)+gamma) + R*gamma = 0  -> cubic in w
    # -1j w^3 + (gamma + 1j omega0) w^2 + (1j wk2) w + (-(gamma + 1j omega0) wk2 + R gamma) ... expand:
    # (w^2-wk2)*(-1j w + (1j omega0 + gamma)) + R gamma
    #  = -1j w^3 + (1j omega0 + gamma) w^2 + 1j wk2 w - (1j omega0+gamma) wk2 + R gamma
    a3 = -1j
    a2 = (1j*omega0 + gamma)
    a1 = (1j*wk2)
    a0 = -(1j*omega0 + gamma)*wk2 + R*gamma
    return np.roots([a3, a2, a1, a0])

# --- gain profile peaked at omega0 (band center). Off-center modes have detuned wk2 = c^2 k^2. ---
c = 1.0
gamma = 0.1
omega0 = 0.6           # gain center (temporal companion of the spatial fold band)
# bare gain profile G(k): peaked Lorentzian in wk2 around wk0^2 = omega0^2
wk0sq = omega0**2
Gwidth = 0.15
def Gbare(wk2):
    return 1.0/(1.0 + ((wk2 - wk0sq)/Gwidth)**2)   # normalized peak =1 at band center

# FOLD STRENGTH: RR finds a *visible* fold needs gain >> instability onset e_inst~0.015.
# Take the band-center small-signal gain g0 strong enough to fold; clamp pulls the band-center
# EFFECTIVE gain to loss kappa (scalar clamp). The scalar clamp factor s makes R(center)=kappa.
g0_center = 0.9        # strong small-signal gain at band center (fold strength)
kappa = 0.05           # cold khronon loss
# scalar clamp: s chosen so s*g0_center*Gbare(center)=kappa  (gain=loss at band center)
s_scalar = kappa/(g0_center*Gbare(wk0sq))
print(f"scalar clamp factor s = {s_scalar:.5f}  (pulls band-center effective gain to loss kappa={kappa})")
print(f"check: R(center)= s*g0*G(center) = {s_scalar*g0_center*Gbare(wk0sq):.5f}  (should equal kappa)")

# Now sweep k (via wk2) across the fold band. R(k) = s_scalar * g0_center * Gbare(wk2).
print("\n=== SCALAR clamp: max Im(omega_pole) across the band (off-center included) ===")
worst = -1e9; worst_k = None
ks = np.linspace(0.0, 1.4, 281)
for wk2 in ks:
    R = s_scalar * g0_center * Gbare(wk2)
    rts = poles_of_D(wk2, R, omega0, gamma)
    mi = max(r.imag for r in rts)
    if mi > worst:
        worst, worst_k = mi, np.sqrt(max(wk2,0))
print(f"max Im(omega_pole) over band (SCALAR clamp) = {worst:+.5f} at k={worst_k:.3f}")
print("  (>0 => a retarded pole in the UHP = UNSTABLE: the scalar clamp fails off-center, per RR)")

# DIAGNOSE: the scalar clamp rescales ALL k by the same s. The off-center modes still carry the
# active negative-residue line at reduced but nonzero gain. Show Im(omega_pole) vs k.
print("\nIm(omega_pole) vs k (scalar clamp) -- the off-center band is where it goes UHP:")
for wk2 in [0.0,0.1,0.2,0.3,0.36,0.5,0.7,1.0]:
    R = s_scalar*g0_center*Gbare(wk2)
    rts = poles_of_D(wk2,R,omega0,gamma)
    mi = max(r.imag for r in rts)
    flag = "  <-- UHP" if mi>1e-9 else ""
    print(f"  k={np.sqrt(wk2):.3f}  R(k)={R:.4f}  max Im(pole)={mi:+.5f}{flag}")
