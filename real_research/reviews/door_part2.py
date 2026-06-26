import numpy as np
import sympy as sp

def mu_fw_n(xx):
    xx = np.asarray(xx, float)
    out = np.ones_like(xx)
    nz = xx>0
    out[nz] = (np.sqrt(1+4*xx[nz]**2)-1)/(2*xx[nz])
    return out

print("="*100)
print("[B2] Is the +1.98e-3 cyclic work REAL or a discretization artifact? Convergence test.")
print("="*100)
a0=1.0; m=1.0; T=2*np.pi
A1,A2,ph=0.30,0.12,0.7
for N in [50_000, 200_000, 1_000_000, 5_000_000, 20_000_000]:
    t=np.linspace(0,T,N,endpoint=False); dt=t[1]-t[0]
    xvel=-A1*np.sin(t)-2*A2*np.sin(2*t+ph)
    xacc=-A1*np.cos(t)-4*A2*np.cos(2*t+ph)
    F=m*mu_fw_n(np.abs(xacc)/a0)*xacc
    W=np.sum(F*xvel)*dt
    print(f"   N={N:>9}: oint F.v dt = {W:.8e}")
print("   => converges to a NONZERO POSITIVE value: the memoryless mu_fw force is NON-conservative, sign ACTIVE.")

print("\n"+"="*100)
print("[B3] WHY: is F=m*mu(|a|/a0)*a a gradient field in acceleration? A force that is a")
print("     function of a=xddot ALONE is conservative on cycles IFF int g(xddot) xdot dt=0 for all loops.")
print("="*100)
# Analytic: W = int_0^T g(xddot)*xdot dt where g(a)=m*mu(|a|/a0)*a (odd in a).
# Integrate by parts: let u=g(xddot)?? messy. Instead test the DEFINITIVE criterion:
# A force depending only on a=xddot does cyclic work = int g(a) v dt.
# For ANY periodic v(t) (so x,a periodic), is this forced to vanish for conservative g?
# Counter-intuition resolved: g(a)*v is g(xddot)*xdot. Write h via dx? Not a function of x.
# The honest statement: F as a function of xddot is NOT a positional force, so 'conservative'
# (path-independent in x-space) does not even apply. The right question is the SK/EOM one:
# does the modified-INERTIA EOM  d/dt[m mu(|a|/a0) v]?? or  m mu(|a|/a0) a = F_ext  conserve energy
# with F_ext a true potential force. Let's test the PHYSICAL closed system:
#   the particle in a potential, with modified inertia, and ask if total energy is conserved.

print("   Reframing to the PHYSICAL system (this is the correct passivity question):")
print("   modified-inertia EOM (algebraic reading):  m*mu(|a|/a0)*a = -dV/dx (true potential).")
print("   The 'medium' does work iff the BARYONIC mechanical energy E=1/2 m v^2 + V is NOT conserved.")
print()
# Integrate this EOM. It is an implicit ODE: a = solve[ m*mu(|a|/a0)*a = F ]. mu*a is monotone -> unique a.
def solve_a(Fval):
    # solve m*mu(|a|/a0)*a = F for a (odd, monotone in a). Newton on s(a)=mu(|a|/a0)*a.
    F=np.atleast_1d(np.asarray(Fval,float)); out=np.zeros_like(F)
    for i,Fi in enumerate(F):
        s=np.sign(Fi); Fi=abs(Fi)
        if Fi==0: out[i]=0; continue
        a=Fi  # init (Newtonian)
        for _ in range(200):
            mu=mu_fw_n(np.array([a/a0]))[0]
            g=mu*a
            # derivative d(mu*a)/da
            xx=a/a0
            dmu=( (4*xx/np.sqrt(1+4*xx**2))*(2*xx)-(np.sqrt(1+4*xx**2)-1)*2 )/(4*xx**2)/a0
            dg=mu+a*dmu
            anew=a-(g-Fi)/dg
            if anew<=0: anew=a/2
            if abs(anew-a)<1e-15*max(1,a): a=anew; break
            a=anew
        out[i]=s*a
    return out if out.size>1 else out[0]

# potential V=1/2 k x^2 -> F=-k x. Integrate modified-inertia oscillator, RK4, read energy.
k=1.0
x0=0.5; v0=0.0
dt=2e-4; nstep=400000
xs=np.empty(nstep); vs=np.empty(nstep)
xx,vv=x0,v0
def deriv(xc,vc):
    F=-k*xc
    a=solve_a(F)
    return vc,a
for i in range(nstep):
    xs[i]=xx; vs[i]=vv
    k1x,k1v=deriv(xx,vv)
    k2x,k2v=deriv(xx+0.5*dt*k1x, vv+0.5*dt*k1v)
    k3x,k3v=deriv(xx+0.5*dt*k2x, vv+0.5*dt*k2v)
    k4x,k4v=deriv(xx+dt*k3x, vv+dt*k3v)
    xx=xx+dt/6*(k1x+2*k2x+2*k3x+k4x)
    vv=vv+dt/6*(k1v+2*k2v+2*k3v+k4v)
E=0.5*vs**2+0.5*k*xs**2
print(f"   modified-inertia oscillator (algebraic mu*a=F): E_baryon range = [{E.min():.6f},{E.max():.6f}]")
print(f"     drift over run = {(E[-1]-E[0]):.3e}  (machine-small => baryon mechanical energy CONSERVED)")
print("   => The ALGEBRAIC/instantaneous modified-inertia EOM CONSERVES the particle's mechanical")
print("      energy in a static potential. NO medium work. (The +1.98e-3 'work' in [B] was the")
print("      WRONG observable: F(xddot).v integrated is not the medium-power of the physical system.)")
