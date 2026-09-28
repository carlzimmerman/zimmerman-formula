"""Conforming P1 variational modes of the inhomogeneous Q/R hydrostatic slab."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_ivp, quad
from scipy.linalg import eigh, cholesky

SOURCE=Path('campaign_fresh_gravity_astra/stage_04/matter_stability/run_003/results.json')


def constitutive(branch,u):
    u=np.asarray(u)
    if branch=='Q':
        return np.sqrt(u*(u+1)),2*np.sqrt(u*(u+1))/(2*u+1)
    t=np.sqrt(u);d=-np.expm1(-t)
    return u/d,d*d/(d-.5*t*np.exp(-t))


def background(branch):
    def ode(x,y):
        g,_=constitutive(branch,y[0])
        return [y[1],-y[1]*float(g)]
    sol=solve_ivp(ode,[0,1],[.01,.1],method='DOP853',dense_output=True,
                  rtol=1e-12,atol=1e-14,max_step=.005)
    assert sol.success
    def evaluate(x):
        u,r=sol.sol(x);g,A=constitutive(branch,u)
        return u,r,g,A
    return evaluate


def assemble(evaluate,n,eta,order=8,factorized=True,cross=True):
    full=n+2;nodes=np.linspace(0,1,full);h=nodes[1]-nodes[0]
    z,w=leggauss(order);z=(z+1)/2;w=w*h/2
    N=np.column_stack((1-z,z));D=np.array([-1/h,1/h])
    points=nodes[:-1,None]+h*z[None,:]
    u,r,g,A=evaluate(points.ravel())
    r=r.reshape(-1,order);g=g.reshape(-1,order);A=A.reshape(-1,order)
    H=np.zeros((2*full,2*full));M=np.zeros_like(H)
    for e in range(full-1):
        ix=np.array([e,e+1]);ip=ix+full
        xx=np.zeros((2,2));xp=np.zeros((2,2));pp=np.zeros((2,2))
        mx=np.zeros((2,2));mp=np.zeros((2,2))
        for j in range(order):
            Nq=N[j];rq=r[e,j];Aq=A[e,j];gq=g[e,j]
            if factorized:
                xx+=w[j]*(rq*np.outer(D,D)+rq*rq/Aq*np.outer(Nq,Nq))
                xp+=w[j]*rq*np.outer(Nq,D)
            else:
                delta=-rq*D+rq*gq*Nq
                xx+=w[j]*np.outer(delta,delta)/rq
                xp+=w[j]*np.outer(delta,Nq)
            pp+=w[j]*Aq*np.outer(D,D)
            mx+=w[j]*rq*np.outer(Nq,Nq)
            mp+=w[j]*eta*np.outer(Nq,Nq)
        H[np.ix_(ix,ix)]+=xx;H[np.ix_(ip,ip)]+=pp
        if cross:
            H[np.ix_(ix,ip)]+=xp;H[np.ix_(ip,ix)]+=xp.T
        M[np.ix_(ix,ix)]+=mx;M[np.ix_(ip,ip)]+=mp
    keep=np.r_[np.arange(1,full-1),full+np.arange(1,full-1)]
    return H[np.ix_(keep,keep)],M[np.ix_(keep,keep)],nodes


def direct_rayleigh(evaluate,n,eta,vector,order=12):
    full=n+2;nodes=np.linspace(0,1,full);h=1/(n+1)
    X=np.r_[0,vector[:n],0];P=np.r_[0,vector[n:],0]
    z,w=leggauss(order);z=(z+1)/2;w=w*h/2
    points=nodes[:-1,None]+h*z[None,:]
    u,r,g,A=evaluate(points.ravel());r=r.reshape(-1,order);g=g.reshape(-1,order);A=A.reshape(-1,order)
    xx=X[:-1,None]*(1-z)+X[1:,None]*z
    pp=P[:-1,None]*(1-z)+P[1:,None]*z
    dx=(X[1:]-X[:-1])[:,None]/h;dp=(P[1:]-P[:-1])[:,None]/h
    delta=-r*dx+r*g*xx
    original=np.sum((delta*delta/r+A*dp*dp+2*delta*pp)*w)
    squared=np.sum((r*dx*dx+A*(dp+r*xx/A)**2)*w)
    mass=np.sum((r*xx*xx+eta*pp*pp)*w)
    return float(original/mass),float(squared/mass),float(mass)


def periodic_control(eta,k):
    z,w=leggauss(80);x=(z+1)*math.pi;w=w*math.pi
    X=np.sin(k*x);P=np.cos(k*x);dX=k*np.cos(k*x);dP=-k*np.sin(k*x)
    A=.5;delta=-dX
    H=np.array([[np.sum(w*delta*delta),np.sum(w*delta*P)],
                [np.sum(w*delta*P),np.sum(w*A*dP*dP)]])
    M=np.diag([np.sum(w*X*X),np.sum(w*eta*P*P)])
    got=eigh(H,M,eigvals_only=True)
    trace=(1+A/eta)*k*k;large=.5*(trace+math.hypot((A/eta-1)*k*k,2*k/math.sqrt(eta)))
    small=(k*k/eta*(A*k*k-1))/large
    target=np.array([small,large]);err=float(max(abs(got-target)/np.maximum(1,abs(target))))
    assert err<1e-11
    wrong=np.array([[np.sum(w*(dX*dX+X*X/A)),np.sum(w*X*dP)],
                    [np.sum(w*X*dP),np.sum(w*A*dP*dP)]])
    wronglow=float(eigh(wrong,M,eigvals_only=True)[0])
    if k==1:assert got[0]<0 and wronglow>0
    else:assert got[0]>0
    return dict(eta=eta,k=k,omega2=got.tolist(),analytic=target.tolist(),relative_error=err,
                wrongly_applying_hydrostatic_factorization_lowest=wronglow,
                scope='Separate periodic supported/subtracted constant background; it is not hydrostatic.')


def main(out):
    rows=[];bg_reports=[];boundary_controls=[];convergence=[]
    source=json.loads(SOURCE.read_text())
    for branch in ['Q','R']:
        evaluate=background(branch)
        ref=next(x for x in source['balanced_slabs'] if x['kernel']==branch and x['initial_u']==.01)
        u,r,g,A=evaluate(np.array(ref['chi']))
        bg_error=max(float(max(abs(u-np.array(ref['u'])))),float(max(abs(r-np.array(ref['r'])))))
        assert bg_error<2e-12 and min(r)>0 and min(A)>0
        integral=quad(lambda q:float(constitutive(branch,q)[0]),.01,float(u[-1]),epsabs=1e-13,epsrel=1e-13)[0]
        first_error=abs(float(r[-1])+integral-.1);assert first_error<1e-12
        sample=np.linspace(0,1,101);su,sr,sg,sA=evaluate(sample)
        bg_reports.append(dict(branch=branch,initial_u=.01,initial_r=.1,interval=[0,1],
            source_sample_max_error=bg_error,first_integral_error=first_error,
            chi=sample.tolist(),u=su.tolist(),r=sr.tolist(),g_over_a=sg.tolist(),A=sA.tolist(),
            rho_min=float(min(sr)),A_min=float(min(sA))))
        # Deliberately violate xi=0 at both ends. Keep the exact boundary term.
        original=quad(lambda x:float(evaluate(x)[1]*evaluate(x)[2]**2),0,1,epsabs=1e-13)[0]
        square=quad(lambda x:float(evaluate(x)[1]**2/evaluate(x)[3]),0,1,epsabs=1e-13)[0]
        boundary=float(-evaluate(1)[1]*evaluate(1)[2]+evaluate(0)[1]*evaluate(0)[2])
        residual=original-square-boundary
        assert abs(residual)<2e-12 and abs(boundary)>1e-4
        boundary_controls.append(dict(branch=branch,trial='xi=1, psi=0; outside Dirichlet trial space',
            original_2V=original,squares_only_2V=square,boundary_term=boundary,
            corrected_identity_residual=residual,wrongly_omitted_boundary_residual=original-square))
        stiffness_hash={}
        for eta in [.01,.04]:
            for n in [64,128,256]:
                H,M,nodes=assemble(evaluate,n,eta,8,True)
                Hd,Md,_=assemble(evaluate,n,eta,12,False)
                factor_error=float(np.linalg.norm(H-Hd,np.inf)/np.linalg.norm(H,np.inf))
                mass_quad_error=float(np.linalg.norm(M-Md,np.inf)/np.linalg.norm(M,np.inf))
                assert factor_error<2e-11 and mass_quad_error<2e-12
                hm=hashlib.sha256(H.tobytes()).hexdigest()
                if n in stiffness_hash:assert stiffness_hash[n]==hm
                else:stiffness_hash[n]=hm
                Lm=cholesky(M,lower=True);Lh=cholesky(H,lower=True)
                mass_min=float(eigh(M,subset_by_index=[0,0],eigvals_only=True)[0])
                values,vectors=eigh(H,M,subset_by_index=[0,9],driver='gvx')
                assert min(values)>0 and mass_min>0
                ortho=float(np.max(abs(vectors.T@M@vectors-np.eye(10))))
                assert ortho<1e-9
                rayleigh=[];residual=[];modes=[]
                xout=np.linspace(0,1,33)
                for j,value in enumerate(values):
                    v=vectors[:,j]
                    if v[np.argmax(abs(v[:n]))]<0:v=-v
                    Hmv=H@v;Mmv=M@v
                    err=float(np.linalg.norm(Hmv-value*Mmv)/(np.linalg.norm(Hmv)+abs(value)*np.linalg.norm(Mmv)))
                    rr,sq,mass=direct_rayleigh(evaluate,n,eta,v)
                    re=max(abs(rr/value-1),abs(sq/value-1))
                    assert err<2e-8 and re<2e-8 and abs(mass-1)<2e-10
                    rayleigh.append(dict(original=rr,squared=sq,eigenvalue=float(value),mass=mass,relative_error=re))
                    residual.append(err)
                    X=np.r_[0,v[:n],0];P=np.r_[0,v[n:],0]
                    slopes=np.array([P[1]/(nodes[1]-nodes[0]),-P[-2]/(nodes[-1]-nodes[-2])])
                    flux=slopes*np.array([evaluate(0)[3],evaluate(1)[3]])
                    modes.append(dict(mode=j+1,xi=np.interp(xout,nodes,X).tolist(),
                        psi=np.interp(xout,nodes,P).tolist(),boundary_potential=[0.,0.],
                        boundary_psi_derivative=slopes.tolist(),boundary_scalar_flux=flux.tolist()))
                assert max(abs(np.array(modes[0]['boundary_scalar_flux'])))>1e-8
                Hunc,_,_=assemble(evaluate,n,eta,12,False,False)
                unc=float(eigh(Hunc,M,subset_by_index=[0,0],eigvals_only=True)[0])
                assert unc>0 and values[0]<=unc*(1+1e-9)
                rows.append(dict(branch=branch,eta=eta,K=eta/.005,cs_over_c=math.sqrt(.005),
                    interior_nodes=n,elements=n+1,omega2=values.tolist(),
                    smallest_mass_eigenvalue=mass_min,min_mass_cholesky_diagonal=float(min(np.diag(Lm))),
                    min_stiffness_cholesky_diagonal=float(min(np.diag(Lh))),
                    original_factorized_matrix_relative_error=factor_error,mass_quadrature_error=mass_quad_error,
                    mass_orthogonality_error=ortho,max_eigen_residual=max(residual),
                    max_independent_rayleigh_relative_error=max(x['relative_error'] for x in rayleigh),
                    rayleigh_checks=rayleigh,uncoupled_lowest_omega2=unc,stiffness_sha256=hm,
                    sample_chi=xout.tolist(),modes=modes))
            rr=[x for x in rows if x['branch']==branch and x['eta']==eta]
            a,b,c=[np.array(x['omega2']) for x in rr]
            coarse=abs(a-b)/b;fine=abs(b-c)/c
            rates=fine/coarse
            assert max(fine)<.004 and max(rates)<.5
            convergence.append(dict(branch=branch,eta=eta,coarse_relative_change=coarse.tolist(),
                fine_relative_change=fine.tolist(),fine_over_coarse_change=rates.tolist(),
                observed_decreasing=bool(np.all(a>b) and np.all(b>c)),
                caution='65,129,257 elements are not nested; observed monotonicity is not used as a theorem.'))
        for n in [64,128,256]:
            a,b=[x for x in rows if x['branch']==branch and x['interior_nodes']==n]
            assert np.all(np.array(b['omega2'])<=np.array(a['omega2'])*(1+1e-10))
    controls=[periodic_control(eta,k) for eta in [.01,.04] for k in [1,3]]
    c=299792458.;cs=c*math.sqrt(.005);restoration=[]
    for name,a in [('canonical',9.3619e-11),('alternative',1.1279e-10)]:
        for row in [x for x in rows if x['interior_nodes']==256]:
            restoration.append(dict(normalization=name,a_reference_m_s2=a,branch=row['branch'],K=row['K'],
                sound_speed_m_s=cs,slab_length_m=cs*cs/a,
                omega_per_second=(a/cs*np.sqrt(row['omega2'])).tolist(),
                note='Same dimensionless family, with B and rho also rescaled; not a fit of one physical slab.'))
    result=dict(primary_cells=len(rows),backgrounds=bg_reports,rows=rows,convergence=convergence,
        boundary_controls=boundary_controls,periodic_controls=controls,dimensional_restoration=restoration,
        checks_summary=dict(all_generalized_eigenvalues_positive=True,
          smallest_returned_omega2=min(x['omega2'][0] for x in rows),
          largest_original_factor_matrix_error=max(x['original_factorized_matrix_relative_error'] for x in rows),
          largest_eigen_residual=max(x['max_eigen_residual'] for x in rows),
          largest_rayleigh_error=max(x['max_independent_rayleigh_relative_error'] for x in rows),
          largest_fine_grid_change=max(max(x['fine_relative_change']) for x in convergence),
          largest_refinement_gap_ratio=max(max(x['fine_over_coarse_change']) for x in convergence),
          stiffness_independent_of_eta=True),
        scope='Finite positive-spectrum verification of the actual Q/R isothermal slab with xi=psi=0 walls; not filtered-MONO, 3D, free-boundary or nonlinear stability.')
    (out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(primary_cells=len(rows),**result['checks_summary']),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    main(p.parse_args().out)
