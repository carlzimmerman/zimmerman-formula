import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp,simpson
from scipy.special import gammainc
from scipy.linalg import eigh_tridiagonal

S=5.364;rmin=1e-5
checks=[]
def check(name,c,detail=''):
    checks.append(dict(name=name,passed=bool(c),detail=str(detail)))
    if not c:raise AssertionError(name+': '+str(detail))
def baryon(r):return np.minimum(r**3,1.)
def components(r,q):
    qq=np.clip(q,0.,S);src=baryon(r)+qq
    root=2*src*r*r/(np.sqrt(src*src+4*src*r*r)+src)
    m=np.minimum(qq+root,S);u=(m-qq)/(r*r)
    return m,u,u/(1-u)
def solve(beta,outerfactor,tolerance):
    ell=np.sqrt(beta);R=max(50.,outerfactor*ell)
    x=np.unique(np.r_[np.geomspace(rmin,R,800),1.])
    q=S*gammainc(3,x/ell);n=S*np.exp(-x/ell)/(2*ell**3)
    def rhs(x,y):return np.array([x*x*y[1],-components(x,y[0])[2]/beta])
    def boundary(y0,y1):return np.array([y0[0]-y0[1]*rmin**3/3,y1[1]-(S-y1[0])/(ell*R*(R+ell))])
    sol=solve_bvp(rhs,boundary,x,np.array([q,n]),tol=tolerance,max_nodes=30000)
    check('refined solver B%g outer%g'%(beta,outerfactor),sol.success,sol.message)
    return sol,R

def reduced_energy(nodes,q,beta):
    rr=(nodes[1:]+nodes[:-1])/2;dr=np.diff(nodes);qm=(q[1:]+q[:-1])/2
    m,u,_=components(rr,qm)
    # w_full with stable small-u evaluation, using power series for u<.001.
    ww=-u-np.log1p(-u)
    small=u<.001
    ww[small]=sum(u[small]**j/j for j in range(2,9))
    return float(sum(dr*(-(baryon(rr)*m+m*m/2)/(rr*rr)+rr*rr*ww+beta*((q[1:]-q[:-1])/dr)**2/(2*rr*rr))))

rows=[];hessianrows=[]
for beta in [1.,100.,1000.,10000.]:
    sol,R=solve(beta,15.,5e-7);refined,R2=solve(beta,30.,1e-7)
    probe=np.geomspace(rmin,min(R,R2),1000)
    q,n=sol.sol(probe);qr,nr=refined.sol(probe)
    change=max(abs(q-qr))/S
    check('outer/tolerance sensitivity B%g'%beta,change<2e-5,change)
    check('review reference domain B%g'%beta,min(qr)>-1e-7 and max(qr)<S+1e-7 and min(nr)>-1e-8,(min(qr),max(qr),min(nr)))
    forcecontrols=[]
    for rad in [1.,2.,4.]:
        qq=float(refined.sol(rad)[0]);m=float(components(np.array([rad]),np.array([qq]))[0][0]);gb=1/rad**2
        goal=(gb+np.sqrt(gb*gb+4*gb))/2
        forcecontrols.append(dict(r=rad,reference_mass=qq,carrier_mass=m,force_ratio=(1+m)/rad**2/goal))
    # Reference EOS energy integrable, but this is not the actual full mass/current energy.
    points=np.geomspace(rmin,R2,6000);qq,nn=refined.sol(points)
    reference_energy=float(simpson(beta*points**2*nn**2/2,x=points))
    rows.append(dict(B=beta,outer_radii=[R,R2],max_reference_profile_change_over_S=float(change),nodes=[len(sol.x),len(refined.x)],reference_EOS_energy=reference_energy,force_controls=forcecontrols))
    for count in [400,800]:
        end=max(12*np.sqrt(beta),10.);start=max(1e-4,.001*np.sqrt(beta))
        grid=np.geomspace(start,end,count+1);rr=(grid[1:]+grid[:-1])/2;dr=np.diff(grid)
        qgrid=refined.sol(grid)[0];qm=(qgrid[:-1]+qgrid[1:])/2
        m,u,g=components(rr,qm)
        active=m<S-1e-8
        C=np.where(active,-(g+1)**2/(rr**2*g*(g+2)),1/(rr**2*(1-u)**2))
        stiff=beta/(rr*rr*dr)
        mass=C*dr/4
        diag=stiff[:-1]+stiff[1:]+mass[:-1]+mass[1:]
        off=-stiff[1:-1]+mass[1:-1]
        scale=stiff[:-1]+stiff[1:]
        evals=eigh_tridiagonal(diag/scale,off/np.sqrt(scale[:-1]*scale[1:]),select='i',select_range=(0,2),eigvals_only=True)
        # This check is a finite radial energy block only; full dynamical stability is excluded.
        check('radial energy block B%g N%d'%(beta,count),min(evals)>0,evals)
        # Independent energy finite differences on a compact smooth test displacement.
        phase=np.log(grid/start)/np.log(end/start)
        direction=np.sin(np.pi*phase)**2
        direction[0]=direction[-1]=0
        dd=np.diff(direction)
        dq=np.diff(qgrid)
        amplitude=.002*float(min(dq[np.abs(dd)>1e-12]/np.abs(dd[np.abs(dd)>1e-12])))
        check('nonzero feasible variation B%g N%d'%(beta,count),amplitude>0,amplitude)
        direction*=amplitude
        fullform=float(sum(stiff*np.diff(direction)**2+mass*(direction[:-1]+direction[1:])**2))
        # Avoid catastrophic cancellation: evaluate only potential differences per cell
        # with long double, then add the quadratic derivative term exactly.
        def potential(qmid):
            rl=rr.astype(np.longdouble);ql=qmid.astype(np.longdouble)
            ml,ul,_=components(rl,ql)
            return -(baryon(rl)*ml+ml*ml/2)/(rl*rl)+rl*rl*(-ul-np.log1p(-ul))
        dm=(direction[:-1]+direction[1:])/2
        pot2=float(sum(dr.astype(np.longdouble)*(potential(qm+dm)+potential(qm-dm)-2*potential(qm))))
        finite=pot2+float(sum(stiff*np.diff(direction)**2))
        error=abs(finite-fullform)/max(fullform,1e-30)
        # Some tails make feasible amplitudes too tiny to resolve even in longdouble.
        resolved=fullform>1e-15
        if resolved:check('energy variation identity B%g N%d'%(beta,count),error<.03,error)
        hessianrows.append(dict(B=beta,grid_intervals=count,domain=[start,end],normalized_energy_eigenvalues=evals.tolist(),feasible_amplitude=amplitude,analytic_second_variation=fullform,finite_difference_second_variation=finite,relative_error=error,finite_difference_resolved=resolved))
out=dict(checks=checks,refined_cases=rows,radial_energy_checks=hessianrows,scope='Boundary/tolerance checks and positive finite radial energy Hessian on specified compact perturbation grids; not continuum spectrum or full clock/metric/current stability.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
