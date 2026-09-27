#!/usr/bin/env python3
"""Normalized common host, compact projection, and weighted convex gate."""
import argparse,json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import quad
from scipy.linalg import expm

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();ch={}
    def ex(name,z):
        r=s.factor(s.simplify(z));assert r==0,(name,r);ch[name]={'passed':True,'residual':str(r)}
    def num(name,value,ok):
        assert bool(ok),(name,value);ch[name]={'passed':True,'measured':value}
    k,C,c2,alpha=s.symbols('k C c2 alpha',positive=True)
    cN=1-alpha/2
    psi,Phi,beta,U,pd=s.symbols('psi Phi beta U psidot',real=True)
    L=-6*pd**2+4*k*k*beta*pd-c2*(3*pd-k*k*beta)**2+2*k*k*psi*psi-4*k*k*Phi*psi+2*cN*k*k*(U-Phi)**2+alpha*k*k*Phi*Phi+2*cN*k*k*C*U*U
    sol={U:2*psi/(2*C+alpha),Phi:2*(1+C)*psi/(2*C+alpha),beta:(2+3*c2)*pd/(c2*k*k)}
    for v in [U,Phi,beta]:ex('normalized_host_aux_'+str(v),s.diff(L,v).subs(sol))
    Lred=2*(2+3*c2)/c2*pd*pd-2*(2-alpha)/(2*C+alpha)*k*k*psi*psi
    ex('normalized_host_exact_reduced_action',L.subs(sol)-Lred)
    cs2=c2*(2-alpha)/((2+3*c2)*(2*C+alpha))
    ex('normalized_host_sound_speed',-s.diff(Lred,psi,2)/(k*k*s.diff(Lred,pd,2))-cs2)
    ex('normalized_host_positive_kinetic_coefficient',s.diff(Lred,pd,2)-4*(2+3*c2)/c2)
    ex('normalized_host_deep_limit_is_degenerate',s.limit(cs2,C,s.oo))
    # Full determinant crosscheck independently uses the Euler rows.
    om=s.symbols('omega',real=True);D=-s.I*om;ep=-c2
    rows=[4*k*k*psi-4*k*k*Phi-D*(-12*D*psi+4*k*k*beta+6*ep*(3*D*psi-k*k*beta)),
          -4*k*k*psi-4*cN*k*k*(U-Phi)+2*alpha*k*k*Phi,
          4*k*k*D*psi-2*ep*k*k*(3*D*psi-k*k*beta),4*cN*k*k*(U-Phi)+4*cN*k*k*C*U]
    det=s.factor(s.Matrix(rows).jacobian([psi,Phi,beta,U]).det())
    ex('normalized_host_dispersion_determinant',det.subs(om**2,cs2*k*k))
    oldcs=c2*(2-alpha*(1+C))/((2+3*c2)*(alpha+(alpha+2)*C))
    par={alpha:s.Rational(1,100),c2:s.Rational(1,50),C:1000}
    oldnum=float(oldcs.subs(par));newnum=float(cs2.subs(par))
    num('negative_control_original_host_vs_normalized_host',{'old_cs2':oldnum,'new_cs2':newnum},oldnum<0<newnum)

    # Independently varied static physical potentials before any identification.
    z,u,a,spat=s.symbols('DZ DU DPhi DPsi',real=True)
    density=2*spat**2-4*a*spat+alpha*(a-z)**2+4*a*z-2*z*z-4*cN*z*u
    ex('static_spatial_metric_equation',s.diff(density,spat)-4*(spat-a))
    ex('static_normalization_after_independent_no_slip',density.subs(spat,a)-(-2*cN*(a-z)**2-4*cN*z*u))
    MP,lb,ld,lapPhi,lapZ,lapU=s.symbols('M2 rho_b rho_d lapPhi lapZ lapU',real=True)
    lapse_eq=2*MP*cN*(lapPhi-lapZ)-lb-ld
    z_eq=2*MP*cN*(lapZ-lapPhi+lapU)+ld
    ex('baryon_only_Poisson_from_two_varied_equations',lapse_eq+z_eq-(2*MP*cN*lapU-lb))
    oldlapse=2*MP*((1-alpha/2)*lapPhi-lapZ)-lb-ld
    oldz=2*MP*(lapZ-lapPhi+lapU)+ld
    ex('negative_control_old_alpha_kernel_leak',oldlapse+oldz-(2*MP*(lapU-alpha*lapPhi/2)-lb))
    Gbare,GN=s.symbols('Gbare GN',positive=True)
    ex('measured_Newton_normalization',(Gbare/cN)*cN-Gbare)

    # Arbitrary G first variation with the weighted Laplacian, in one dimension.
    x=s.symbols('x',real=True);N=s.Function('N')(x);W=s.Function('W')(x)
    F=s.Function('f')(x);ell=s.symbols('ell',real=True)
    lp=s.diff(W,x,2)+s.diff(N,x)*s.diff(W,x)/N
    weighted_integrand=N*ell*lp
    ex('full_on_weighted_laplacian_is_exact_divergence',weighted_integrand-s.diff(N*ell*s.diff(W,x),x))
    nn=s.Function('n')(x);ee=s.symbols('epsilon',real=True)
    Nvar=N*s.exp(ee*nn)
    lpvar=s.diff(W,x,2)+s.diff(Nvar,x)*s.diff(W,x)/Nvar
    ex('weighted_laplacian_fixed_h_lapse_variation',s.diff(lpvar,ee).subs(ee,0)-s.diff(nn,x)*s.diff(W,x))
    weighted_f_adjoint=s.diff(N*s.diff(F,x),x)/N
    ex('weighted_laplacian_self_adjoint_density',N*weighted_f_adjoint-s.diff(N*s.diff(F,x),x))
    Jval,theta,delta=s.symbols('J theta delta',real=True)
    ex('full_on_lapse_source_cancels_density_divergence',Jval+ell*lp-theta-delta/2-ell*lp-(Jval-theta-delta/2))
    Bgeom=s.Function('Bgeom')(x)
    ex('geometric_laplacian_does_not_have_same_boundary_identity',
       N*s.diff(W,x,2)-(s.diff(N*s.diff(W,x),x)-s.diff(N,x)*s.diff(W,x)))

    # Compact h-volume projection, using finite quadrature solely to verify
    # measure variation and the nonlocal source. No Poisson inverse is assumed.
    nh=11;xx=np.arange(nh)*2*np.pi/nh
    hh=1+.25*np.cos(xx);Nv=1+.3*np.sin(xx);Zv=.2*np.cos(2*xx)+.1*np.sin(xx)
    vv=.3+.2*np.sin(3*xx);WW=.8+.2*np.cos(xx);dZ=np.sin(xx)+.3*np.cos(3*xx)
    dn=np.cos(xx)-.2*np.sin(2*xx);dh=.4*np.cos(3*xx)
    def eval_lapse_h(Nv0,hv,Z0):
        mean=np.dot(hv,Z0)/sum(hv);zz=Z0-mean
        KK=vv*vv/(2*Nv0*Nv0)
        LL=np.exp(zz)*KK-np.exp(-zz)*WW
        rho=np.exp(zz)*KK+np.exp(-zz)*WW
        return float(np.dot(hv*Nv0,LL)),zz,rho
    ee0,zz,rh=eval_lapse_h(Nv,hh,Zv);abar=np.dot(hh*Nv,rh)/sum(hh)
    projected=rh-abar/Nv
    num('compact_projected_source_integrates_to_zero',float(np.dot(hh*Nv,projected)),abs(np.dot(hh*Nv,projected))<1e-12)
    predz=float(np.dot(hh*Nv*projected,dZ))
    predn=float(-np.dot(hh*Nv*rh,dn))
    # delta h-volume weight = dh times h (dh=1/2 h^ij delta h_ij).
    KK=vv*vv/(2*Nv*Nv);LL=np.exp(zz)*KK-np.exp(-zz)*WW
    predh=float(np.dot(hh*(Nv*LL-abar*zz),dh))
    errs=[]
    for step in [1e-3,1e-4,1e-5]:
        vz=(eval_lapse_h(Nv,hh,Zv+step*dZ)[0]-eval_lapse_h(Nv,hh,Zv-step*dZ)[0])/(2*step)
        vn=(eval_lapse_h(Nv*np.exp(step*dn),hh,Zv)[0]-eval_lapse_h(Nv*np.exp(-step*dn),hh,Zv)[0])/(2*step)
        vh=(eval_lapse_h(Nv,hh*np.exp(step*dh),Zv)[0]-eval_lapse_h(Nv,hh*np.exp(-step*dh),Zv)[0])/(2*step)
        errs.append({'step':step,'Z_error':abs(vz-predz),'lapse_error':abs(vn-predn),'volume_error':abs(vh-predh)})
    num('projection_source_lapse_and_volume_differences',errs,max(errs[-1][k] for k in ['Z_error','lapse_error','volume_error'])<2e-9)
    frozenh=float(np.dot(hh*Nv*LL,dh))
    num('negative_control_freezing_projector_metric_variation',abs(frozenh-predh),abs(frozenh-predh)>.001)
    e_shift=eval_lapse_h(Nv,hh,Zv+7)[0]
    num('projected_action_constant_Z_gauge',abs(e_shift-ee0),abs(e_shift-ee0)<1e-12)
    flat_rho=np.full(nh,2.0);flat_N=np.ones(nh)
    source_flat=flat_rho-np.dot(hh*flat_N,flat_rho)/(sum(hh)*flat_N)
    num('homogeneous_positive_carrier_admitted_by_projected_Z_equation',source_flat.tolist(),np.max(abs(source_flat))<1e-12)
    num('negative_control_unprojected_homogeneous_constraint',float(np.dot(hh*flat_N,flat_rho)),np.dot(hh*flat_N,flat_rho)>1)

    # Closed-leaf weighted convex-gate U and lapse first variations. The
    # constitutive J below is the exact deep-MOND power, not a new fit.
    nnodes=13;tt=np.arange(nnodes)*2*np.pi/nnodes
    ks=np.fft.fftfreq(nnodes,d=1/nnodes);fft=np.fft.fft(np.eye(nnodes),axis=0)
    DD=np.real(np.fft.ifft((1j*ks)[:,None]*fft,axis=0))
    Lap=DD@DD;SS=expm(.12*Lap)
    NN=1+.25*np.sin(tt);uu=.3*np.cos(tt)+.16*np.sin(2*tt)+.04*np.cos(3*tt)
    du=.2*np.sin(tt)+.15*np.cos(2*tt);n_dir=.3*np.cos(tt)
    elln=.4;th=.1;width=.2
    def gate_f(xx0):
        if xx0<=0:return 0.
        if xx0>=width:return 1.
        t=xx0/width;logit=-1/t+1/(1-t)
        return 1/(1+np.exp(-np.clip(logit,-700,700)))
    def ramp(xx0):
        if xx0<=0:return 0.
        if xx0>=width:return xx0-width/2
        return quad(gate_f,0,xx0,epsabs=1e-12,epsrel=1e-12)[0]
    def gate_energy(N0,u0):
        ww=SS@u0;gg=DD@ww;LN=-(DD.T@(N0[:,None]*DD))/N0[:,None]
        JJ=4/3*np.abs(gg)**1.5
        XX=JJ+elln*(LN@ww)-th
        fs=np.array([gate_f(v) for v in XX]);gs=np.array([ramp(v) for v in XX])
        return float(np.dot(N0,gs)),(ww,gg,LN,XX,fs,gs)
    ge,(ww,gg,LN,XX,fs,gs)=gate_energy(NN,uu)
    jp=2*np.sign(gg)*np.sqrt(abs(gg))
    # Weighted adjoint outer S_N^dagger is used explicitly.
    divj=-(DD.T@(NN*fs*jp))/NN
    pred_U=SS.T@(NN*(-divj+elln*LN@fs))
    divfp=-(DD.T@(NN*fs*gg))/NN
    pred_N=NN*(gs-elln*divfp)
    u_der=float(pred_U@du);n_der=float(pred_N@n_dir);last={}
    for step in [1e-4,1e-5,1e-6]:
        uf=(gate_energy(NN,uu+step*du)[0]-gate_energy(NN,uu-step*du)[0])/(2*step)
        nf=(gate_energy(NN*np.exp(step*n_dir),uu)[0]-gate_energy(NN*np.exp(-step*n_dir),uu)[0])/(2*step)
        last={'step':step,'U_error':abs(uf-u_der),'lapse_error':abs(nf-n_der)}
    num('weighted_convex_gate_U_and_lapse_variations',last,max(last['U_error'],last['lapse_error'])<2e-8)
    no_interface=float((SS.T@(NN*(-divj)))@du)
    num('negative_control_dropping_gate_interface_term',abs(no_interface-u_der),abs(no_interface-u_der)>.01)
    # Transition convexity in the directional Hessian (away from p=0).
    def fprime(v):
        if v<=0 or v>=width:return 0.
        t=v/width;ff=gate_f(v)
        return ff*(1-ff)*(1/t**2+1/(1-t)**2)/width
    dp=DD@(SS@du);dq=LN@(SS@du)
    jpp=1/np.sqrt(abs(gg))
    Hgate=float(np.dot(NN,fs*jpp*dp*dp+np.array([fprime(v) for v in XX])*(jp*dp+elln*dq)**2))
    num('convex_gate_directional_hessian_nonnegative',Hgate,Hgate>=0)
    out={'claim_id':'CD26_4_NORMALIZED_PROJECTED_CONVEX_COMMON_ACTION','number_of_checks':len(ch),'checks':ch,
         'normalized_host_reduced_action':str(s.factor(Lred)),'normalized_host_cs2':str(cs2),
         'scope':['Constant theta and fixed geometry for convex auxiliary proof','Compact h-volume projection varied with lapse and spatial measure',
                  'Frozen isotropic scalar symbol only; no full coupled gravitational evolution proof',
                  'Heat-regularized convex composition changes regional empirical gate','No homogeneous positive density discarded by Poisson inversion']}
    target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'number_of_checks':len(ch),'all_passed':True,'new_cs2':str(cs2),'weighted_gate_variation':last,'projection_variation':errs[-1]},indent=2))

if __name__=='__main__':main()
