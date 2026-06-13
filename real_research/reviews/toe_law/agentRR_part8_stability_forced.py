"""
agentRR Part 8 -- the two decisive questions:
 (A) is the true-fold region STABLE (retarded pole in LHP, not a UHP runaway)?  The clamp (Part 1)
     pins the band-center mode marginal, but we must check the FULL active retarded propagator
     D(omega,k)=omega^2 - c^2 k^2 - Sigma(omega,k) has NO UHP pole at the operating point across k.
 (B) the forced-vs-free split: deep in the fold the IR sound speed c_eff^2 collapses (Part 7:
     c_eff^2=0.0008 at the deepest fold). Map fold-depth vs c_eff^2 and vs the gain y. Then state
     which of {y (gain), x=k0^2/Gam (center/width), Gam (width)} is FORCED by the dS pump
     (H, T_dS=H/2pi) and which is FREE.

For (A): the saturated/clamped self-energy at the operating point is, in the temporal channel, an
active Lorentzian with NEGATIVE residue but POSITIVE damping (QQ Route2: active != anti-damped).
Its retarded pole location: D(omega,k)=0 with Sigma(omega)= -A_t * gamma /( -i(omega-omega0) + gamma )
(causal, retarded, pole in LHP). We check Im(omega_pole) <= 0 for the operating-point parameters
mapped from the spatial fold. We do this numerically via the temporal companion (a single clamped
gain line, negative residue, gamma>0) and confirm LHP across the fold band.
"""
import numpy as np

def coeffs(A, Gam, k0, c=1.0):
    den4 = (Gam**2 + k0**4)
    c_eff2 = (-A*Gam**3 + A*Gam*k0**4 + Gam**4*c**2 + 2*Gam**2*c**2*k0**4 + c**2*k0**8)/(den4**2)
    sigma4 = A*Gam*k0**2*(-3*Gam**2 + k0**4)/(den4**3)
    sigma6 = A*Gam*(Gam**4 - 6*Gam**2*k0**4 + k0**8)/(den4**4)
    return c_eff2, sigma4, sigma6

def full_branch(A, Gam, k0, c=1.0):
    ug = np.linspace(1e-5, 1.5, 200000)
    om2 = c**2*ug - A*Gam*(ug - k0**2)/((ug - k0**2)**2 + Gam**2)
    vg2 = np.gradient(om2, ug)
    return ug, om2, vg2

Gam, c = 1.0, 1.0
# ---- (B) map fold-depth vs c_eff^2 over the true-fold region
print("=== (B) fold depth vs IR sound speed c_eff^2 (the soft-edge tradeoff) ===")
rows=[]
for x in np.linspace(0.10,0.30,41):
    k0=np.sqrt(x*Gam)
    for y in np.linspace(1.005,1.35,200):
        A=y*c**2*Gam
        ceff2,s4,s6=coeffs(A,Gam,k0,c)
        if ceff2<=0: continue
        ug,om2,vg2=full_branch(A,Gam,k0,c)
        if om2.min()>0 and vg2.min()<0:
            rows.append((x,y,ceff2,vg2.min(),om2.min()))
rows.sort(key=lambda r:r[3])  # deepest fold first
print("deepest folds (most negative v_g^2) and their c_eff^2:")
for r in rows[:6]:
    print(f"  x={r[0]:.3f} y={r[1]:.4f} c_eff^2={r[2]:.5f} v_g^2_min={r[3]:.4f} om^2_min={r[4]:.4f}")
print("shallowest folds (barely folding) and their c_eff^2:")
for r in rows[-6:]:
    print(f"  x={r[0]:.3f} y={r[1]:.4f} c_eff^2={r[2]:.5f} v_g^2_min={r[3]:.4f} om^2_min={r[4]:.4f}")
# correlation: deep fold <=> small c_eff^2 (near sonic-edge softening)
import numpy as _np
cef=_np.array([r[2] for r in rows]); dep=_np.array([r[3] for r in rows])
print(f"\ncorrelation(c_eff^2, v_g^2_min) over fold region = {_np.corrcoef(cef,dep)[0,1]:.3f}")
print("  (positive => deeper fold goes with SMALLER c_eff^2: the fold is bought by softening the")
print("   IR sound speed toward the b->c_chi edge -- exactly the sonic-edge coincidence QQ wanted.)")

# ---- (A) stability: temporal retarded pole of the clamped active line, across the fold band
print("\n=== (A) retarded-pole stability of the clamped active response ===")
# spatial fold maps to a temporal active Lorentzian: negative residue, gamma>0 (QQ Route2).
# D(w)=w^2 - w_k^2 - Sigma(w), Sigma(w) = -R * 2 g0_eff w0 / (w0^2 - w^2 - i*gamma*w)  (causal)
# clamp (Part 1) sets g0_eff -> kappa (loss); residue negative => Sigma has the active sign but the
# pole of Sigma is in LHP (gamma>0). Find roots of D(w)=0; require all Im(w)<=0.
def max_im_pole(wk2, R, w0, gamma):
    # build characteristic polynomial in w from D(w)*(w0^2-w^2-i gamma w)=0
    # (w^2 - wk2)(w0^2 - w^2 - i gamma w) + R*2*w0*... -> just root-find numerically on retarded D
    import numpy.polynomial.polynomial as P
    # D(w) = w^2 - wk2 + R*gamma/( -1j*(w-w0)+gamma )  (single clamped line, neg residue active)
    f = lambda w: w**2 - wk2 + R*gamma/(-1j*(w-w0)+gamma)
    # scan complex plane coarse then refine for roots; use a contour winding count for UHP poles
    # simpler: companion via clearing denom: (w^2-wk2)(-1j(w-w0)+gamma) + R*gamma = 0  -> cubic in w
    # coeffs of -1j w^3 + (gamma + 1j w0) w^2 + (1j wk2) w + (-gamma wk2 - 1j w0 wk2 + R gamma)
    a3=-1j; a2=(gamma+1j*w0); a1=(1j*wk2); a0=(-gamma*wk2 -1j*w0*wk2 + R*gamma)
    roots=np.roots([a3,a2,a1,a0])
    return roots
# sweep wk2 across the band, clamped active line (R = clamped gain ~ kappa-level, gamma>0, w0 ~ band)
gamma=0.1; w0=0.6
worst=-1e9
for wk2 in np.linspace(0.0,1.5,300):
    for R in [0.001,0.005,0.015,0.05]:   # clamped gain levels up to/around e_inst
        rts=max_im_pole(wk2,R,w0,gamma)
        worst=max(worst, max(r.imag for r in rts))
print(f"max Im(omega_pole) over band & clamped gain levels R<=0.05: {worst:+.5f}")
print("  (<=0 => all retarded poles in LHP = STABLE; the clamp keeps the active line non-runaway)")
print("  NOTE: this is the CLAMPED active line. Part 1 proved the clamp pulls g_eff->kappa so the")
print("  effective in-band gain that would open a UHP pole is self-limited; QQ's e_inst~0.015 LTI")
print("  runaway is the UNCLAMPED case. Saturation is exactly what holds R at/below clamp.")
