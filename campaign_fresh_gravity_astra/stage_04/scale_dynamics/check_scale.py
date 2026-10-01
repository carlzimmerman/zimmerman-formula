#!/usr/bin/env python3
"""SD1: deterministic, bounded checks of the explicitly assumed two-field model."""
import json
import math
import sys
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad, solve_bvp
from scipy.optimize import brentq

OUT = Path(sys.argv[1])
CHECKS = []
NODES, WEIGHTS = leggauss(64)
NODES, WEIGHTS = (NODES+1)/2, WEIGHTS/2


def check(name, passed, detail):
    CHECKS.append({"name": name, "passed": bool(passed), "detail": detail})
    if not passed:
        raise AssertionError(name+": "+str(detail))


def f_lam(branch, B, a):
    B,a=np.broadcast_arrays(np.asarray(B,dtype=float),np.asarray(a,dtype=float))
    u=B/a
    if branch=="Q":
        g=a*np.sqrt(u*(u+1))
        lam=2*np.sqrt(u*(u+1))/(2*u+1)
    else:
        t=np.sqrt(u)
        d=-np.expm1(-t)
        g=np.divide(B,d,out=np.zeros_like(B),where=B>0)
        lam=np.divide(d*d,d-0.5*t*np.exp(-t),out=np.zeros_like(B),where=B>0)
    return g,lam


def constitutive(branch,B,a):
    B,a=np.broadcast_arrays(np.asarray(B,dtype=float),np.asarray(a,dtype=float))
    g,lam=f_lam(branch,B,a)
    # Independent-variable substitution s=B z² removes the square-root endpoint.
    integrand=f_lam(branch,B[...,None]*NODES**2,a[...,None])[0]*NODES
    I=2*B*np.sum(integrand*WEIGHTS,axis=-1)
    W=g*B-I
    T=2*I-g*B
    q=g*lam-B
    mu=np.divide(B,g,out=np.zeros_like(B),where=g>0)
    return g,lam,mu,W,T,q


def at_fixed_g(branch,g,a):
    if branch=="Q":
        B=2*g*g/(math.sqrt(a*a+4*g*g)+a)
    else:
        B=brentq(lambda x:float(f_lam(branch,x,a)[0])-g,0,g,xtol=1e-14)
    return constitutive(branch,B,a)


def potential(chi,S):
    return S*(np.cosh(2*chi)-1)/4,S*np.sinh(2*chi)/2,S*np.cosh(2*chi)


def equilibrium(branch,B,S):
    root=brentq(lambda chi:float(potential(chi,S)[1]-constitutive(branch,B,math.exp(chi))[4]),0,12,xtol=1e-13)
    g,lam,mu,W,T,q=[float(x) for x in constitutive(branch,B,math.exp(root))]
    _,up,upp=potential(root,S)
    m=float(upp-2*T+g*q)
    M=m-q*q/lam
    M_identity=S*math.exp(-2*root)+B*q/lam
    return {"chi":root,"a_over_reference":math.exp(root),"g":g,"lambda":lam,"mu":mu,
            "W":W,"T":T,"q":q,"m":m,"M":M,"M_identity":M_identity}


def periodic_response(branch,k,eps):
    B0,S,J=1.,5.,1.
    eq=equilibrium(branch,B0,S)
    length=2*math.pi
    x=np.linspace(0,length,129)
    def ode(x,y):
        B=B0+eps*np.cos(k*x)
        T=constitutive(branch,B,np.exp(y[0]))[4]
        return np.vstack((y[1],(potential(y[0],S)[1]-T)/J))
    def bc(left,right):
        return np.array([left[1],right[1]])
    sol=solve_bvp(ode,bc,x,np.vstack((np.full_like(x,eq['chi']),np.zeros_like(x))),tol=2e-9,max_nodes=4096)
    sample=np.linspace(0,length,4097)
    chi=sol.sol(sample)[0]
    B=B0+eps*np.cos(k*sample)
    g=f_lam(branch,B,np.exp(chi))[0]
    amp_chi=np.trapz((chi-eq['chi'])*np.cos(k*sample),sample)/math.pi/eps
    amp_g=np.trapz((g-eq['g'])*np.cos(k*sample),sample)/math.pi/eps
    predicted_chi=eq['q']/(eq['lambda']*(eq['M']+J*k*k))
    predicted_g=(1+eq['q']**2/(eq['lambda']*(eq['M']+J*k*k)))/eq['lambda']
    return {"k":k,"epsilon":eps,"success":bool(sol.success),"nodes":int(sol.x.size),
            "max_rms_ode_residual":float(np.max(sol.rms_residuals)),
            "chi_response":float(amp_chi),"predicted_chi_response":predicted_chi,
            "g_response":float(amp_g),"predicted_g_response":predicted_g,
            "relative_chi_error":float(abs(amp_chi/predicted_chi-1)),
            "relative_g_error":float(abs(amp_g/predicted_g-1)),
            "fractional_susceptibility_excess":predicted_g*eq['lambda']-1,
            "response_length":math.sqrt(J/eq['M'])}


def spherical(branch,S,ell,initial_nodes):
    J=S*ell*ell
    r=np.linspace(0,8,initial_nodes)
    B=lambda r:3*r/(1+r*r)**1.5
    def ode(r,y):
        T=constitutive(branch,B(r),np.exp(y[0]))[4]
        return np.vstack((y[1],(potential(y[0],S)[1]-T)/J))
    def bc(left,right):
        return np.array([left[1],right[0]])
    sol=solve_bvp(ode,bc,r,np.zeros((2,r.size)),S=np.array([[0.,0.],[0.,-2.]]),tol=2e-8,max_nodes=4096)
    rs=np.linspace(0,8,1025)
    chi=sol.sol(rs)[0]
    source=B(rs)
    g=f_lam(branch,source,np.exp(chi))[0]
    old=f_lam(branch,source,1.)[0]
    excess=np.divide(g,old,out=np.ones_like(g),where=old>0)-1
    # Leading weak-backreaction check against independently solved linear BVP.
    def linear_ode(r,y):
        return np.vstack((y[1],(S*y[0]-constitutive(branch,B(r),1.)[4])/J))
    lin=solve_bvp(linear_ode,bc,r,np.zeros((2,r.size)),S=np.array([[0.,0.],[0.,-2.]]),tol=2e-8,max_nodes=4096)
    cl=lin.sol(rs)[0]
    rel=float(np.max(np.abs(chi-cl))/max(np.max(np.abs(chi)),1e-30))
    return {"S_over_a_ref2":S,"response_length_input":ell,"initial_nodes":initial_nodes,
            "success":bool(sol.success and lin.success),"final_nodes":int(sol.x.size),
            "max_rms_ode_residual":float(np.max(sol.rms_residuals)),
            "min_chi":float(chi.min()),"max_chi":float(chi.max()),
            "max_a_factor":float(np.exp(chi).max()),"max_force_fractional_excess":float(excess.max()),
            "max_fractional_linear_chi_error":rel,"chi_profile":chi.tolist(),"r":rs.tolist(),
            "SI_profiles":[{"a_reference":a,"a_at_max_chi":a*float(np.exp(chi).max()),
                            "maximum_g_m_s2":float(a*g.max())} for a in [9.3619e-11,1.1279e-10]]}


def scale_energy(branch,t,x):
    S,J,v=5.,0.5,1.
    chi=.2+.03*math.cos(x)*math.cos(.7*t)
    ct=-.021*math.cos(x)*math.sin(.7*t)
    cx=-.03*math.sin(x)*math.cos(.7*t)
    ctt=-.0147*math.cos(x)*math.cos(.7*t)
    cxx=-.03*math.cos(x)*math.cos(.7*t)
    U,up,_=potential(chi,S)
    desired_drive=J*ctt/v**2-J*cxx+up
    a=math.exp(chi)
    B=brentq(lambda B:float(constitutive(branch,B,a)[4])-desired_drive,0,100,xtol=1e-13)
    T=float(constitutive(branch,B,a)[4])
    return {"e":J*(ct*ct/v**2+cx*cx)/2+U,"flux":-J*ct*cx,
            "exchange":T*ct,"T":T,"chi_t":ct,"B":B}


def main():
    results={}
    for branch in ['Q','R']:
        derivative_rows=[]
        for B in [1e-3,.03,.3,1.,10.,100.]:
            g,lam,mu,W,T,q=[float(x) for x in constitutive(branch,B,1.)]
            iq=quad(lambda z:2*B*z*float(f_lam(branch,B*z*z,1.)[0]),0,1,epsabs=1e-12,epsrel=1e-12)[0]
            relI=abs(iq-(g*B-W))/max(iq,1e-30)
            h=2e-5
            tg=(float(at_fixed_g(branch,g*(1+h),1.)[4])-float(at_fixed_g(branch,g*(1-h),1.)[4]))/(2*h*g)
            tc=(float(at_fixed_g(branch,g,math.exp(h))[4])-float(at_fixed_g(branch,g,math.exp(-h))[4]))/(2*h)
            scale=max(abs(q),abs(2*T-g*q),1e-8)
            err=max(abs(tg-q),abs(tc-(2*T-g*q)))/scale
            derivative_rows.append({'B':B,'T':T,'q':q,'quadrature_relative_error':relI,'derivative_scaled_error':err})
        check(branch+' independent quadrature and scale derivatives',max(r['quadrature_relative_error'] for r in derivative_rows)<2e-11 and max(r['derivative_scaled_error'] for r in derivative_rows)<3e-7,derivative_rows)
        check(branch+' unequal fields forbid uniform scale',derivative_rows[2]['T']<derivative_rows[3]['T'],{'T_at_B_0p3':derivative_rows[2]['T'],'T_at_B_1':derivative_rows[3]['T']})
        equilibria=[]
        min_eigen=math.inf
        max_schur_error=0.
        for B in [1e-3,.1,1.,10.,100.]:
            for S in [1.,5.,20.]:
                eq=equilibrium(branch,B,S)
                equilibria.append({'B':B,'S':S,**eq})
                max_schur_error=max(max_schur_error,abs(eq['M']/eq['M_identity']-1))
                for k in np.geomspace(1e-4,1e3,71):
                    for angle in [0,math.pi/4,math.pi/2]:
                        La=eq['mu']*math.sin(angle)**2+eq['lambda']*math.cos(angle)**2
                        # J=1,K=2,v_chi=c=1, mass-normalized Hessian.
                        matrix=np.array([[La*k*k/2,eq['q']*k*math.cos(angle)/math.sqrt(2)],
                                         [eq['q']*k*math.cos(angle)/math.sqrt(2),k*k+eq['m']]])
                        min_eigen=min(min_eigen,float(np.linalg.eigvalsh(matrix)[0]))
        check(branch+' coupled field Schur and mode positivity',min_eigen>0 and max_schur_error<2e-10,{'minimum_omega_squared':min_eigen,'max_Schur_identity_relative_error':max_schur_error,'equilibrium_count':len(equilibria),'k_points':71,'angle_count':3})
        responses=[periodic_response(branch,k,eps) for k in [1,3] for eps in [.03,.01,.003]]
        for k in [1,3]:
            rr=[r for r in responses if r['k']==k]
            check(branch+' finite-scale susceptibility k='+str(k),all(r['success'] for r in rr) and rr[-1]['relative_g_error']<3e-6 and rr[-1]['relative_chi_error']<4e-5 and rr[-1]['relative_g_error']<rr[0]['relative_g_error']/30,rr)
        spheres=[spherical(branch,S,ell,n) for S in [5.,20.] for ell in [.2,1.] for n in [129,257]]
        for S in [5.,20.]:
            for ell in [.2,1.]:
                ss=[r for r in spheres if r['S_over_a_ref2']==S and r['response_length_input']==ell]
                diff=float(np.max(np.abs(np.array(ss[0]['chi_profile'])-np.array(ss[1]['chi_profile']))))
                check(branch+' spherical boundary solve S='+str(S)+' ell='+str(ell),all(r['success'] and r['min_chi']>-1e-10 and r['max_force_fractional_excess']>0 for r in ss) and diff<2e-7,{'max_refinement_chi_difference':diff,'max_force_fractional_excess':ss[-1]['max_force_fractional_excess'],'max_chi':ss[-1]['max_chi'],'linear_relative_error':ss[-1]['max_fractional_linear_chi_error']})
        energy=[]
        for h in [.002,.001,.0005]:
            t,x=.6,.4
            ed=(scale_energy(branch,t+h,x)['e']-scale_energy(branch,t-h,x)['e'])/(2*h)
            fd=(scale_energy(branch,t,x+h)['flux']-scale_energy(branch,t,x-h)['flux'])/(2*h)
            mid=scale_energy(branch,t,x)
            energy.append({'step':h,'residual':ed+fd-mid['exchange'],'exchange':mid['exchange'],'B':mid['B']})
        check(branch+' dynamic reservoir energy exchange',abs(energy[-1]['residual'])<1e-8 and abs(energy[-1]['residual'])<abs(energy[0]['residual'])/10,energy)
        results[branch]={'derivatives':derivative_rows,'equilibria':equilibria,'susceptibility':responses,'spheres':spheres,'scale_energy':energy}
    redshift=[]
    for z in [0,.5,1,2,3]:
        E2=.315*(1+z)**3+.685; E=math.sqrt(E2); om=.315*(1+z)**3/E2
        chi=math.log(E); acc=4.5*E2*om*(1-om/2)
        redshift.append({'z':z,'E':E,'chi_H':chi,'chi_H_tt_over_H0_squared':acc,
                         'U_prime_over_S':math.sinh(2*chi)/2,
                         'vacuum_reference_scales':[9.3619e-11,1.1279e-10],
                         'H_comparison_scales':[9.3619e-11*E,1.1279e-10*E]})
    check('H history needs positive homogeneous drive',all(r['chi_H_tt_over_H0_squared']>0 and r['U_prime_over_S']>=0 for r in redshift),redshift)
    answer={'claim_id':'SD1','status':'all finite checks passed','checks':CHECKS,'branches':results,
            'separate_redshift_branches':redshift,'non_claims':['No physical parameter fit','No metric/lensing completion','No global evolution theorem','No matter stability theorem','No universal constant scale retained','No identification of the extra scale field as vacuum energy']}
    OUT.write_text(json.dumps(answer,indent=2)+'\n')
    print(json.dumps({'passed_checks':len(CHECKS),'sphere_summary':{key:[{k:r[k] for k in ['S_over_a_ref2','response_length_input','max_chi','max_force_fractional_excess','max_fractional_linear_chi_error']} for r in results[key]['spheres'] if r['initial_nodes']==257] for key in results},'susceptibility':{key:results[key]['susceptibility'][-1] for key in results}},indent=2))


if __name__=='__main__': main()
