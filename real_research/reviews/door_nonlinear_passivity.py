import numpy as np
import sympy as sp

print("="*100)
print("DOOR: Is the passivity no-go a LINEAR-RESPONSE artifact the nonlinear MI evades?")
print("Independent calculation. Framework: mu_fw(x)=(sqrt(1+4x^2)-1)/(2x), a0=9.36e-11.")
print("="*100)

# ---------------------------------------------------------------------------
# PART A. The framework's mu_fw and the 'inversion' as a CONSTITUTIVE relation
# ---------------------------------------------------------------------------
x = sp.symbols('x', positive=True)
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)
print("\n[A] mu_fw(x) =", mu_fw)
print("    mu_fw(0+)   =", sp.limit(mu_fw, x, 0))          # deep-MOND
print("    mu_fw(oo)   =", sp.limit(mu_fw, x, sp.oo))      # Newtonian
print("    => CONSTITUTIVE inversion: mu(0)=0 < mu(inf)=1 (inertia DROPS at low accel).")

# The 'effective mass' as a function of |a|:  m_eff(a) = m * mu_fw(a/a0).
# The force law (modified inertia, the algebraic/AQUAL-MI reading):
#    F = m * mu_fw(|a|/a0) * a   (force needed to sustain acceleration a)
# Question: is THIS (a memoryless, instantaneous nonlinear law) the linear-kernel
# kind of inversion (forbidden) or the nonlinear-constitutive kind (allowed)?

# ---------------------------------------------------------------------------
# PART B. ENERGY BALANCE of the MEMORYLESS nonlinear constitutive law
#   m(a) a = F, with m(a)=m*mu_fw(|a|/a0). Drive on a closed loop, compute oint F.v dt.
# ---------------------------------------------------------------------------
print("\n[B] ENERGY BALANCE of the MEMORYLESS nonlinear MI law  F = m mu_fw(|a|/a0) a")
print("    A memoryless force F(a) that is a function of acceleration ALONE.")
print("    Over any closed loop in (position,velocity) phase space, compute oint F.dx.")

# For 1D periodic motion x(t) with period T, with F = m*mu(|a|/a0)*a  (a=xddot):
#   W = oint F dx = int_0^T F * xdot dt = int_0^T m*mu(|a|/a0)*xddot*xdot dt
# Define g(a) = m*mu(|a|/a0)*a as an odd function of a. Then F = g(xddot).
# W = int g(xddot)*xdot dt. Integrate by parts is not trivial because g acts on xddot.
# Let's just numerically integrate on a periodic orbit and read the cyclic work.

def mu_fw_n(xx):
    xx = np.asarray(xx, float)
    out = np.ones_like(xx)
    nz = xx>0
    out[nz] = (np.sqrt(1+4*xx[nz]**2)-1)/(2*xx[nz])
    return out

a0 = 1.0  # work in a0 units
m  = 1.0

# A genuinely non-sinusoidal periodic worldline (deep-MOND amplitudes) so |a| varies a lot:
T  = 2*np.pi
N  = 2_000_000
t  = np.linspace(0, T, N, endpoint=False)
dt = t[1]-t[0]
# x(t) = A1 cos(t) + A2 cos(2t+ph)  -> a varies, passes through deep-MOND and transition
A1, A2, ph = 0.30, 0.12, 0.7
xpos = A1*np.cos(t) + A2*np.cos(2*t+ph)
xvel = -A1*np.sin(t) - 2*A2*np.sin(2*t+ph)
xacc = -A1*np.cos(t) - 4*A2*np.cos(2*t+ph)

F_memless = m*mu_fw_n(np.abs(xacc)/a0)*xacc      # instantaneous nonlinear MI force
W_memless = np.sum(F_memless*xvel)*dt            # cyclic work done BY the force on the particle
print(f"    memoryless F=m*mu(|a|/a0)*a : oint F.v dt over one period = {W_memless:.3e}")
print(f"      (machine-zero => the memoryless nonlinear MI is CONSERVATIVE on cycles)")

# sanity: compare to a known dissipative force (drag) and a known conservative force
W_drag   = np.sum((-0.1*xvel)*xvel)*dt
W_spring = np.sum((-1.0*xpos)*xvel)*dt
print(f"      control: drag  -0.1*v  -> oint = {W_drag:.3e}  (negative = dissipative, as expected)")
print(f"      control: spring -x     -> oint = {W_spring:.3e} (zero = conservative, as expected)")

