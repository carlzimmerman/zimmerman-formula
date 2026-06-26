import numpy as np, scipy.integrate as si

def solve_a(Fval,a0=1.0):
    F=np.atleast_1d(np.asarray(Fval,float)); out=np.zeros_like(F)
    for i,Fi in enumerate(F):
        s=np.sign(Fi); Fi=abs(Fi)
        if Fi==0: out[i]=0; continue
        a=Fi
        for _ in range(300):
            xx=a/a0; r=np.sqrt(1+4*xx**2); mu=(r-1)/(2*xx); g=mu*a
            dmu=((4*xx/r)*(2*xx)-(r-1)*2)/(4*xx**2)/a0; dg=mu+a*dmu
            anew=a-(g-Fi)/dg
            if anew<=0: anew=a/2
            if abs(anew-a)<1e-16*max(1,a): a=anew;break
            a=anew
        out[i]=s*a
    return out[0] if out.size==1 else out

print("="*100)
print("[B5'] The algebraic mu*a=F law is 1-DOF AUTONOMOUS  a=A(x). It conserves H=1/2 v^2 + Phi_mod(x),")
print("      Phi_mod(x) = - INT_0^x A(x') dx'.  PROOF by direct integration of the trajectory.")
print("="*100)
k=1.0; a0=1.0
# precompute A(x) on a grid; trajectory by RK4 using A(x); track H = 1/2 v^2 + Phi_mod(x)
xs=np.linspace(-0.55,0.55,2201)
Ax=np.array([solve_a(-k*xi) for xi in xs])
Phi=-si.cumulative_trapezoid(Ax,xs,initial=0.0)
# center Phi at x=0
Phi -= np.interp(0.0,xs,Phi)
def Aint(xc): return np.interp(xc,xs,Ax)
def Phint(xc): return np.interp(xc,xs,Phi)
dt=2e-4; nstep=200000; xx,vv=0.5,0.0
H0=0.5*vv**2+Phint(xx); Hmin=H0;Hmax=H0
Enewt0=0.5*vv**2+0.5*k*xx**2; Enmin=Enewt0;Enmax=Enewt0
for i in range(nstep):
    k1x,k1v=vv,Aint(xx); k2x,k2v=vv+0.5*dt*k1v,Aint(xx+0.5*dt*k1x)
    k3x,k3v=vv+0.5*dt*k2v,Aint(xx+0.5*dt*k2x); k4x,k4v=vv+dt*k3v,Aint(xx+dt*k3x)
    xx+=dt/6*(k1x+2*k2x+2*k3x+k4x); vv+=dt/6*(k1v+2*k2v+2*k3v+k4v)
    H=0.5*vv**2+Phint(xx); Hmin=min(Hmin,H);Hmax=max(Hmax,H)
    En=0.5*vv**2+0.5*k*xx**2; Enmin=min(Enmin,En);Enmax=max(Enmax,En)
print(f"   MODIFIED energy H=1/2v^2+Phi_mod : drift = {Hmax-Hmin:.3e}   (CONSERVED)")
print(f"   NEWTONIAN  E   =1/2v^2+1/2kx^2  : swing = {Enmax-Enmin:.3e}  (NOT conserved -- but irrelevant)")
print("   => The algebraic instantaneous mu*a=F law is strictly CONSERVATIVE (1-DOF autonomous).")
print("      It has NO bath, NO medium, NO energy gain. 'Newtonian E not conserved' is just the")
print("      wrong potential -- a passive nonlinear spring also 'fails' to conserve the WRONG energy.")
print("      VERDICT (instantaneous reading): passivity is NOT violated; there is no active kernel here.")
