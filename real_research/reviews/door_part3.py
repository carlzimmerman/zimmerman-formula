import numpy as np

def mu_fw_n(xx):
    xx=np.asarray(xx,float); out=np.ones_like(xx); nz=xx>0
    out[nz]=(np.sqrt(1+4*xx[nz]**2)-1)/(2*xx[nz]); return out

a0=1.0
def solve_a(Fval):
    F=np.atleast_1d(np.asarray(Fval,float)); out=np.zeros_like(F)
    for i,Fi in enumerate(F):
        s=np.sign(Fi); Fi=abs(Fi)
        if Fi==0: out[i]=0; continue
        a=Fi
        for _ in range(300):
            xx=a/a0; r=np.sqrt(1+4*xx**2); mu=(r-1)/(2*xx); g=mu*a
            dmu=( (4*xx/r)*(2*xx)-(r-1)*2 )/(4*xx**2)/a0; dg=mu+a*dmu
            anew=a-(g-Fi)/dg
            if anew<=0: anew=a/2
            if abs(anew-a)<1e-16*max(1,a): a=anew; break
            a=anew
        out[i]=s*a
    return out[0] if out.size==1 else out

print("="*100)
print("[B4] Is the 4.9e-2 energy drift of the ALGEBRAIC mu*a=F oscillator REAL or integration error?")
print("     Convergence in dt, and is the drift SECULAR (real) or BOUNDED (artifact)?")
print("="*100)
k=1.0
for dt in [4e-4,1e-4,2.5e-5]:
    nstep=int(round(40.0/dt))  # fixed physical time T_end=40
    xx,vv=0.5,0.0; E0=0.5*vv**2+0.5*k*xx**2; Emax=E0;Emin=E0; Eend=E0
    def deriv(xc,vc):
        return vc, solve_a(-k*xc)
    for i in range(nstep):
        k1x,k1v=deriv(xx,vv); k2x,k2v=deriv(xx+0.5*dt*k1x,vv+0.5*dt*k1v)
        k3x,k3v=deriv(xx+0.5*dt*k2x,vv+0.5*dt*k2v); k4x,k4v=deriv(xx+dt*k3x,vv+dt*k4v if False else vv+dt*k3v)
        xx=xx+dt/6*(k1x+2*k2x+2*k3x+k4x); vv=vv+dt/6*(k1v+2*k2v+2*k3v+k4v)
        E=0.5*vv**2+0.5*k*xx**2; Emax=max(Emax,E);Emin=min(Emin,E);Eend=E
    print(f"   dt={dt:.1e}: E0={E0:.6f} Eend={Eend:.6f}  swing=[{Emin:.4f},{Emax:.4f}]  |Eend-E0|={abs(Eend-E0):.3e}")
print("   READ: if |Eend-E0| shrinks ~ dt^4 -> it's RK4 integration error (E truly conserved).")
print("         if it stays O(0.01) independent of dt -> the algebraic law genuinely fails energy conservation.")

print("\n"+"="*100)
print("[B5] DECISIVE: is there a CONSERVED energy for the algebraic law mu(|a|/a0)*a = -V'(x)?")
print("     A 1-D autonomous 2nd-order ODE a=f(x) (here a=solve_a(-V'(x)), a function of x ALONE)")
print("     ALWAYS has a conserved 'energy' E=1/2 v^2 - INT f(x) dx. Check what it is.")
print("="*100)
# a = A(x) where A(x)=solve_a(-k x). Then v dv/dx = A(x) -> 1/2 v^2 = INT A(x) dx + C.
# Conserved quantity: H = 1/2 v^2 - INT_0^x A(x') dx'.  Always exists for a=A(x)! So the
# algebraic law IS conservative (autonomous, 1 DOF). The 'energy' is just NOT 1/2v^2+V.
import scipy.integrate as si
xs=np.linspace(-0.6,0.6,4001)
Ax=np.array([solve_a(-k*xi) for xi in xs])
# potential of the MODIFIED dynamics: Phi(x) = -INT A dx
Phi=-si.cumulative_trapezoid(Ax,xs,initial=0)
# verify H=1/2 v^2 + Phi conserved on the trajectory
dt=1e-4; nstep=int(400000); xx,vv=0.5,0.0
def Aofx(xc): return solve_a(-k*xc)
Hs=[]
for i in range(nstep):
    k1x,k1v=vv,Aofx(xx); k2x,k2v=vv+0.5*dt*k1v,Aofx(xx+0.5*dt*k1x)
    k3x,k3v=vv+0.5*dt*k2v,Aofx(xx+0.5*dt*k2x); k4x,k4v=vv+dt*k3v,Aofx(xx+dt*k3x)
    xx=xx+dt/6*(k1x+2*k2x+2*k3x+k4x); vv=vv+dt/6*(k1v+2*k2v+2*k3v+k4v)
    if i%20000==0:
        Phi_x=-np.interp(xx,xs,Ax)*0  # placeholder
        Phi_here=-np.trapz(np.array([solve_a(-k*xi) for xi in np.linspace(0,xx,400)]),np.linspace(0,xx,400))
        Hs.append(0.5*vv**2+Phi_here)
Hs=np.array(Hs)
print(f"   modified 'energy' H=1/2 v^2 + Phi_mod(x):  range over run = [{Hs.min():.6f},{Hs.max():.6f}]")
print(f"     drift = {Hs.max()-Hs.min():.3e}  (small => H IS the conserved quantity)")
print("   => CONCLUSION: the algebraic mu*a=F law is a 1-DOF autonomous system; it conserves a")
print("      MODIFIED energy H=1/2v^2+Phi_mod, NOT the Newtonian 1/2v^2+V. So '1/2v^2+V not conserved'")
print("      is NOT medium-work; it's just the wrong bookkeeping. The algebraic law has NO bath at all.")
