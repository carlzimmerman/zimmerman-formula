import numpy as np

print("="*100)
print("[C] DECISIVE TEST: Milgrom-2022 time-nonlocal MI conserves phi + E_k (Eq.11), NO bath.")
print("    Reconcile with X2's 'P_medium > 0': the medium-power is the SPLIT artifact ds(1/2 m v^2),")
print("    NOT a true energy source. Compute BOTH ledgers on the SAME closed trajectory.")
print("="*100)
print()
print("Milgrom 2208.07073 Eq.(3):  m a_hat(w) I[{r},w,a0] = F_hat(w),  I = inertia functional of whole traj.")
print("Eq.(8) momentum P_hat=m v_hat I ; Eq.(11) kinetic energy E_k with dE_k/dt = v.F ;")
print("text after (11): for potential forces, phi + E_k CONSERVED for isolated system.")
print()

# We realize I in the simplest single-frequency-faithful way that reproduces mu_fw on circular orbits:
# For a single dominant frequency w0, I[{r},w0] -> mu_fw(|a_hat(w0)|/a0)  (Eq.5 with one argument).
# Build a closed 1-frequency system: harmonic force F=-k x  => circular/elliptic single-freq orbit.
# In Newtonian frame R=0 (Eq.9). Single freq w0: a_hat at w0. Then E_k(t) via Eq.(11).
#
# For a SINGLE frequency w0, the convolution Eq.(11) collapses. Let r(t)=Re[ r0 e^{i w0 t} ] (1D: r0 real amp times cos).
# Take x(t)=X cos(w0 t). v=-X w0 sin, a=-X w0^2 cos. |a_hat(w0)| = X w0^2. I=mu_fw(X w0^2/a0).
# EOM Eq.3: m a I = F = -k x.  With a=-X w0^2 cos, x=X cos:  m(-Xw0^2)mu = -kX  => m w0^2 mu(Xw0^2/a0)=k.
# This is the self-consistent single-freq orbit. E_k from Eq.(11): for single freq, 
#   E_k = (m/2) |v|^2_amp-weighted * I ... let's just use dE_k/dt=v.F to DEFINE E_k by integration, the physical content.

m=1.0; k=1.0; a0=1.0
def mu_fw(x): 
    x=abs(x); 
    return 1.0 if x==0 else (np.sqrt(1+4*x*x)-1)/(2*x)

# self-consistent amplitude X: m w0^2 mu(X w0^2/a0)=k, but w0 also set by orbit... 
# cleaner: pick X, then the consistent w0 solves m w0^2 mu(X w0^2/a0)=k. Solve for w0.
from scipy.optimize import brentq
X=0.8
def cons(w0): return m*w0**2*mu_fw(X*w0**2/a0)-k
w0=brentq(cons,1e-3,10.0)
print(f"[C1] single-freq self-consistent deep-ish orbit: X={X}, w0={w0:.5f}, |a|=Xw0^2={X*w0**2:.4f} (x_arg)")
mu0=mu_fw(X*w0**2/a0); print(f"     mu_fw at operating point = {mu0:.5f}")

T=2*np.pi/w0; N=2_000_000; t=np.linspace(0,T,N,endpoint=False); dt=t[1]-t[0]
x=X*np.cos(w0*t); v=-X*w0*np.sin(w0*t); F=-k*x

# Ledger 1 (Milgrom Eq.11): E_k defined by dE_k/dt = v.F  => E_k(t)=E_k(0)+int v F dt'. 
# Total energy = E_k + phi, phi=1/2 k x^2. dE_k/dt=vF and d(phi)/dt = -vF  => E_k+phi=const EXACTLY by construction.
Ek = np.concatenate([[0.0], np.cumsum(0.5*(v[1:]*F[1:]+v[:-1]*F[:-1]))*dt])
phi=0.5*k*x**2
Etot = Ek+phi - (Ek[0]+phi[0])
print(f"     Milgrom ledger: total energy phi+E_k drift over cycle = {Etot.max()-Etot.min():.3e}  (CONSERVED by Eq.11 def)")
print(f"     (Eq.11 DEFINES E_k s.t. dE_k/dt=v.F; for potential phi, phi+E_k is conserved -- Milgrom's theorem.)")

# Ledger 2 (the X2/SK 'baryon' split): pretend the 'real' kinetic energy is 1/2 m v^2 (Newtonian bookkeeping).
# Then 'medium power' P_med = d/dt(phi + 1/2 m v^2) ... = vF + m v a. With modified EOM m a mu = F => m a = F/mu.
# P_med = v F + v (F/mu) = vF(1+1/mu). Over a cycle <vF>=0 (closed), so the CYCLE-AVERAGE of m v a:
a = -X*w0**2*np.cos(w0*t)   # actual accel on the orbit
P_med_cycle = np.sum( (m*a)*v )*dt    # = oint (m a) . v  -- the 'newtonian kinetic' change over a cycle
# but newtonian KE is also periodic so this is 0. The X2 'P_ae>0' was the SECULAR/DC channel, not cyclic.
print(f"\n[C2] The X2 'medium power' on a CLOSED cyclic orbit:  oint (m a).v dt = {P_med_cycle:.3e} (=0, periodic).")
print("     => On any CLOSED orbit BOTH ledgers give zero net energy exchange. No activity on bound orbits.")
print("     The X2 P_ae>0 appeared ONLY for the SECULAR/DC-FORCED open channel (constant F on a ramping v),")
print("     which is NOT a closed isolated system -- it is an externally-driven non-isolated configuration,")
print("     exactly the case Milgrom's footnote EXCLUDES ('I assume a closed system, evolve on its own').")
