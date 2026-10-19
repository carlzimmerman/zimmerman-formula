"""Full polar-areal constrained ADM Hessian in explicit radial Galerkin spaces.

Finite-basis positivity is evidence only on the tested space, not a continuum
mode-completeness or nonlinear stability certificate.
"""
import argparse,json,math,time
from pathlib import Path
import numpy as np
import scipy.linalg as la
from scipy.interpolate import CubicSpline
import torch
torch.set_num_threads(1);torch.set_default_dtype(torch.float64)
p=argparse.ArgumentParser();p.add_argument('--profile',required=True);p.add_argument('--R',type=float,default=300)
p.add_argument('--dx',type=float,default=.1);p.add_argument('--basis',type=int,default=40)
p.add_argument('--result',required=True);args=p.parse_args();start=time.monotonic()
data=np.load(args.profile);oldr=data['r'];G=float(data['G']);m=float(data['m']);M=float(data['M'])
lam=float(data['lambda_total']);g=float(data['g']);omega=float(data['omega'])
scale=math.sqrt(4*math.pi*G);cc=g/scale;LL=lam/(4*math.pi*G)
N=round(args.R/args.dx);dx=args.R/N;rr=(np.arange(N)+.5)*dx
def interp(y):return CubicSpline(oldr,y,bc_type=((1,0.),'natural'))(rr)
F0=scale*interp(data['f']);X0=-scale*interp(data['h'])
a0=interp(data['a']);alpha0=interp(data['alpha'])
P0=-omega*a0/alpha0*F0;P1=-2*omega*a0/alpha0*X0
r=torch.tensor(rr);r2=r*r
base=torch.tensor(np.array([F0,X0,P0,P1]))
B=args.basis
phi_np=np.sqrt(2/args.R)*np.sin(np.pi*np.arange(1,B+1)[:,None]*rr[None,:]/args.R)/rr[None,:]
basis=torch.tensor(phi_np)

def deriv(y):
    return torch.cat(((y[...,1:2]-y[...,:1])/(2*dx),
      (y[...,2:]-y[...,:-2])/(2*dx),(-y[...,-1:]-y[...,-2:-1])/(2*dx)),dim=-1)
def trap(y,initial):
    return torch.cat((initial.reshape(1),initial+torch.cumsum((y[1:]+y[:-1])*(.5*dx),dim=0)))

def functional(coeff,parity,which='grand'):
    d=(coeff.reshape(4,B)@basis)
    if parity=='even':
        Fr=base[0]+d[0];Xr=base[1]+d[1];PiFi=base[2]+d[2];PiXi=base[3]+d[3]
        Fi=torch.zeros_like(Fr);Xi=Fi;PiFr=Fi;PiXr=Fi
    else:
        Fr=base[0];Xr=base[1];PiFi=base[2];PiXi=base[3]
        Fi=d[0];Xi=d[1];PiFr=d[2];PiXr=d[3]
    fields=torch.stack((Fr,Fi,Xr,Xi));grads=deriv(fields)
    S=PiFr**2+PiFi**2+PiXr**2+PiXi**2+torch.sum(grads**2,dim=0)
    FF=Fr*Fr+Fi*Fi;XX=Xr*Xr+Xi*Xi
    U=m*m*FF+M*M*XX+2*cc*(Xr*(Fr*Fr-Fi*Fi)+2*Xi*Fr*Fi)+LL*FF*FF
    I=trap(2*r*S,S[0]*r[0]**2)
    J=trap(r2*(S+U)*torch.exp(I),(S[0]+U[0])*r[0]**3/3)
    mass=torch.exp(-I[-1])*J[-1]
    charge=-2*dx*torch.sum(r2*(Fr*PiFi-Fi*PiFr+2*(Xr*PiXi-Xi*PiXr)))
    if which=='mass':return mass
    if which=='charge':return charge
    return mass-omega*charge

zero=torch.zeros(4*B,requires_grad=True)
raw=[]
for parity in ['even','odd']:
    fun=lambda x:functional(x,parity)
    hess=torch.autograd.functional.hessian(fun,zero,vectorize=True).detach().numpy()
    symmetry=float(np.max(abs(hess-hess.T)));hess=.5*(hess+hess.T)
    grad=torch.autograd.functional.jacobian(fun,zero).detach().numpy()
    gm=torch.autograd.functional.jacobian(lambda x:functional(x,parity,'mass'),zero).detach().numpy()
    gq=torch.autograd.functional.jacobian(lambda x:functional(x,parity,'charge'),zero).detach().numpy()
    if parity=='even':
        excluded=gq;label='linear deltaQ=0 tangent'
    else:
        projection=lambda v:dx*np.sum(phi_np*(rr*rr*v)[None,:],axis=1)
        excluded=np.concatenate((projection(F0),2*projection(X0),-projection(P0),-2*projection(P1)))
        label='common U1 phase generator projected out'
    null=la.null_space(excluded[None,:])
    constrained=null.T@hess@null
    vals,vecs=la.eigh(constrained,subset_by_index=(0,4),driver='evr')
    allvals=la.eigh(hess,eigvals_only=True,driver='evr')
    witness=null@vecs[:,0]
    e0=float(fun(zero).detach());finites=[]
    for eps in [1e-4,5e-5,2.5e-5]:
        direction=torch.tensor(eps*witness)
        fd=(float(fun(direction).detach())+float(fun(-direction).detach())-2*e0)/eps**2
        finites.append({'epsilon':eps,'finite_second_variation':fd,'autograd_rayleigh':float(vals[0])})
    raw.append({'parity':parity,'dimension':4*B,'restriction':label,
       'lowest_projected_eigenvalues':[float(x)for x in vals],
       'lowest_unprojected_eigenvalues':[float(x)for x in allvals[:5]],
       'excluded_direction_rayleigh':float(excluded@hess@excluded/(excluded@excluded)),
       'stationarity_gradient_norm':float(la.norm(grad)),
       'stationarity_relative_gradient':float(la.norm(grad)/max(la.norm(gm)+omega*la.norm(gq),1e-100)),
       'hessian_symmetry_error':symmetry,'finite_directional_controls':finites,
       'linear_charge_tangent_error':float(gq@witness)})
    print(json.dumps({'parity':parity,'lowest_projected':float(vals[0]),'grad_norm':float(la.norm(grad))}),flush=True)

report={'status':'completed','profile':args.profile,'G':G,'m':m,'M':M,'g':g,'lambda_total':lam,
 'lambda_rep':lam-g*g/(M*M-4*m*m),'omega':omega,'grid':{'R':args.R,'dx':dx,'N':N},
 'basis':{'type':'spherical sine/r modes j=1..B with regular center and Dirichlet outer endpoint; L2(r2dr) normalized','B_per_component':B,'dimension_per_parity':4*B,'maximum_radial_wavenumber':math.pi*B/args.R},
 'background_ADM_mass_G':float(functional(zero,'even','mass').detach()),
 'background_Q_times_G':float(functional(zero,'even','charge').detach()),
 'background_grand_mass_G':float(functional(zero,'even').detach()),'blocks':raw,
 'runtime_seconds':time.monotonic()-start,'non_claims':['Positive finite-dimensional Galerkin Hessian excludes negative-energy directions only in the stated subspace','No omitted-mode/coercivity proof','Not a nonlinear/nonradial/asymptotic stability theorem','No fluid/EOS or NR evolution used']}
out=Path(args.result);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'completed','runtime_seconds':report['runtime_seconds']}),flush=True)
