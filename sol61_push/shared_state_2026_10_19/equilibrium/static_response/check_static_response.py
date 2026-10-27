#!/usr/bin/env python3
"""Static l=1 source response of an existing full GP + gamma5/3 baryon state.

The COM constraint removes the uniform-gravity translation. This is a finite
floating-point BVP response, not certification of a background minimum or gap.
"""
import hashlib
import json
import math
import pathlib
import sys

import numpy as np
from scipy.integrate import quad, solve_bvp
from scipy.interpolate import CubicHermiteSpline, CubicSpline
from scipy.optimize import brentq
from scipy.special import spherical_jn

HERE = pathlib.Path(__file__).resolve().parent
P = json.loads((HERE/'parameters.json').read_text())
OUT = pathlib.Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
for kind in ['profiles', 'results']:
    path = pathlib.Path(P['background_'+kind])
    assert hashlib.sha256(path.read_bytes()).hexdigest() == P['expected_'+kind+'_sha256']
profile = json.loads(pathlib.Path(P['background_profiles']).read_text())[P['background_key']]
data = json.loads(pathlib.Path(P['background_results']).read_text())
row = next(v for v in data['GP'] if v['tau']==P['tau'] and v['L']==14. and v['tol']==2e-7)
r0 = np.array(profile['r'])
L = float(r0[-1])
tau, K, Kb = P['tau'], P['K'], P['Kb']
mu_d, mu_b = row['mu_d'], row['mu_b']
Rb = row['baryon_radius']
f_spline = CubicHermiteSpline(r0, profile['u'], profile['u_prime'])
U_spline = CubicSpline(r0, profile['U'], bc_type=((1,0.), (1,-profile['U'][-1]/L)))
Rb = brentq(lambda r: U_spline(r)-mu_b, Rb-.02, Rb+.02)


def background(r):
    f = f_spline(r)
    U = U_spline(r)
    # d rho_b/d enthalpy; reconstruct from the same declared EOS.
    enthalpy = np.maximum(mu_b-U, 0.)
    kap = 3./(5*Kb) * np.sqrt(enthalpy/(2.5*Kb))
    V = 6*K*f*f + U - mu_d
    return f, kap, V


def finite_k_reduced(r, k):
    # phi/r - 1. Removing its known affine part improves the small-k solve.
    z = k*np.asarray(r)
    small = np.abs(z) < 0.02
    z2 = z*z
    series = -z2/10 + z2*z2/280 - z2*z2*z2/15120 + z2**4/1330560
    safe = np.where(z==0, 1., z)
    direct = 3*spherical_jn(1,z)/safe - 1.
    return np.where(small, series, direct)


def solve_case(name, k, tol):
    affine_part = 0. if name=='cubic' else 1.
    def reduced(r):
        if name=='affine':
            return np.zeros_like(r)
        if name=='cubic':
            return np.asarray(r)**2
        return finite_k_reduced(r,k)
    def coords(t,inside):
        if inside:
            return Rb*t*(2-t),2*Rb*(1-t)
        return Rb+(L-Rb)*t*t,2*(L-Rb)*t
    def rhs(t,y,par):
        parts=[]
        for off,inside in [(0,True),(4,False)]:
            r,rp=coords(t,inside)
            f,kap,V=background(r)
            a,ap,b,bp=y[off:off+4]
            force=reduced(r)+par[0]
            # At the interior center rp/r=1/t-1/(2-t); the -4/t
            # part is handled by solve_bvp's exact singular S matrix.
            fric=4/(2-t) if inside else -4*rp/r
            parts.extend([rp*ap,rp*(V*a+f*b-f*force)/tau+fric*ap,
                          rp*bp,rp*P['four_pi_G']*(2*f*a+kap*(force-b))+fric*bp])
        return np.array(parts)
    def rhs_jac(t,y,par):
        n=len(t); a=np.zeros((8,8,n)); b=np.zeros((8,1,n))
        for off,inside in [(0,True),(4,False)]:
            r,rp=coords(t,inside)
            f,kap,V=background(r)
            fric=4/(2-t) if inside else -4*rp/r
            a[off,off+1]=rp; a[off+1,off]=rp*V/tau
            a[off+1,off+1]=fric; a[off+1,off+2]=rp*f/tau
            a[off+2,off+3]=rp
            a[off+3,off]=rp*P['four_pi_G']*2*f
            a[off+3,off+2]=-rp*P['four_pi_G']*kap
            a[off+3,off+3]=fric
            b[off+1,0]=-rp*f/tau
            b[off+3,0]=rp*P['four_pi_G']*kap
        return a,b
    def bc(y0,yL,par):
        return np.r_[y0[1],y0[3],yL[4],yL[6],yL[7],yL[:4]-y0[4:]]
    def bc_jac(y0,yL,par):
        a=np.zeros((9,8)); b=np.zeros((9,8)); c=np.zeros((9,1))
        a[0,1]=1.; a[1,3]=1.; b[2,4]=1.; b[3,6]=1.; b[4,7]=1.
        for j in range(4):
            b[5+j,j]=1.; a[5+j,4+j]=-1.
        return a,b,c
    # delta f=r*a and v=r*b make the regular l=1 center nonsingular.
    S = np.zeros((8,8)); S[1,1] = S[3,3] = -4.
    mesh=np.linspace(0,1,P['initial_mesh_points'])
    sol=solve_bvp(rhs,bc,mesh,np.zeros((8,len(mesh))),p=[0.],S=S,
                  fun_jac=rhs_jac,bc_jac=bc_jac,tol=tol,bc_tol=tol*.01,
                  max_nodes=P['max_bvp_nodes'])
    assert sol.success,(name,tol,sol.message,len(sol.x),
                        float(np.max(sol.rms_residuals)),
                        float(sol.x[np.argmax(sol.rms_residuals)]))
    ell=float(sol.p[0]); frame_lambda=ell-affine_part
    def vals(r):
        r=np.asarray(r)
        inside=r<=Rb
        t=np.where(inside,1-np.sqrt(np.maximum(1-r/Rb,0.)),
                   np.sqrt(np.maximum((r-Rb)/(L-Rb),0.)))
        y=sol.sol(t)
        a,ap,b,bp=np.where(inside,y[:4],y[4:])
        f,kap,V=background(r)
        phi_over_r=reduced(r)+affine_part
        s=r*a; sp=a+r*ap; v=r*b
        db=kap*r*(reduced(r)+ell-b)
        drho=2*f*s+db
        return a,ap,b,bp,f,kap,V,phi_over_r,s,sp,v,db,drho
    def integ(fn):
        parts=[quad(lambda t: float(fn(float(coords(t,inside)[0])))*float(coords(t,inside)[1]),
                    0.,1.,epsabs=P['quadrature_epsabs']*.5,
                    epsrel=P['quadrature_epsrel'],limit=300) for inside in [True,False]]
        return sum(p[0] for p in parts),sum(p[1] for p in parts)
    chi,chierr=integ(lambda r: r**3*vals(r)[7]*vals(r)[12])
    # Affine overlap vanishes by the COM constraint, so this is identical and
    # avoids subtractive cancellation in the finite-k susceptibility.
    chip,chiperr=integ(lambda r: r**3*float(reduced(r))*vals(r)[12])
    com,comerr=integ(lambda r: r**3*vals(r)[12])
    pref=4*math.pi/3
    chi*=pref; chip*=pref; com*=pref
    def work_integrand(r):
        a,ap,b,bp,f,kap,V,pr,s,sp,v,db,drho=vals(r)
        bary=kap*r*r*(float(reduced(r))+ell-b)**2
        return r*r*(2*tau*(sp*sp+2*a*a)+2*V*s*s+bary+drho*v)
    work,workerr=integ(work_integrand)
    work*=pref
    # Boundary-to-volume Poisson moment: M1=(L^3 v'-L^2 v)/(4piG).
    outer=sol.sol(1.)[4:]
    vL=L*outer[2]; vpL=outer[2]+L*outer[3]
    com_boundary=pref*(L**3*vpL-L**2*vL)/P['four_pi_G']
    bcres=float(np.max(np.abs(bc(sol.y[:,0],sol.y[:,-1],sol.p))))
    rr=np.linspace(0,L,P['profile_output_points'])
    vv=vals(rr)
    max_response=float(max(np.max(np.abs(vv[8])),np.max(np.abs(vv[10]))))
    result={'name':name,'q':None if k is None else k*Rb,'k':k,'tol':tol,
            'nodes':len(sol.x),'max_solver_rms_residual':float(np.max(sol.rms_residuals)),
            'boundary_residual':bcres,'frame_lambda':frame_lambda,'chi_direct':chi,
            'chi_COM_projected':chip,'chi_quad_abs_error':pref*chierr,
            'chi_projected_quad_abs_error':pref*chiperr,'COM_moment':com,
            'COM_quad_abs_error':pref*comerr,'COM_boundary_moment':float(com_boundary),
            'work_quadratic':work,'work_quad_abs_error':pref*workerr,
            'work_relative_discrepancy':abs(work-chip)/max(abs(chip),1e-14),
            'source_gauge_identity_error':abs(chi-chip-affine_part*com),
            'max_abs_delta_f_or_v':max_response}
    if name=='affine':
        assert abs(frame_lambda+1.)<1e-13
        assert max_response<1e-13 and abs(chi)<1e-13 and abs(com)<1e-13
    else:
        assert chip>0.
        assert abs(com)<2e-5*max(1.,max_response)
        assert result['work_relative_discrepancy']<3e-4
        assert abs(chi-chip)<2e-5*max(abs(chip),1e-8)
    assert bcres<1e-10
    record={'r':rr.tolist(),'delta_f':vv[8].tolist(),'v':vv[10].tolist(),
            'delta_rho_b':vv[11].tolist(),'delta_rho_total':vv[12].tolist()}
    return result,record


rows=[]; response_profiles={}
sources=[('affine',None),('cubic',None)]+[(f'q={q}',q/Rb) for q in P['q_values']]
for name,k in sources:
    start=len(rows)
    for tol in P['bvp_tolerances']:
        ans,pr=solve_case(name,k,tol)
        rows.append(ans); response_profiles[f'{name};tol={tol}']=pr
    c,fine=rows[start:]
    rel=abs(c['chi_COM_projected']-fine['chi_COM_projected'])/max(abs(fine['chi_COM_projected']),1e-14)
    fine['coarse_fine_chi_relative_change']=rel
    assert rel<2e-4,(name,rel)
fine_rows=[r for r in rows if r['tol']==P['bvp_tolerances'][-1]]
cubic=next(r for r in fine_rows if r['name']=='cubic')['chi_COM_projected']
for r in fine_rows:
    if r['k'] is not None:
        r['chi_over_k4']=r['chi_COM_projected']/r['k']**4
        r['leading_cubic_prediction']=r['k']**4*cubic/100
        r['ratio_to_leading_cubic']=r['chi_COM_projected']/r['leading_cubic_prediction']
result={'background_profiles_sha256':P['expected_profiles_sha256'],
        'background_results_sha256':P['expected_results_sha256'],
        'background_key':P['background_key'],'baryon_radius':Rb,
        'assertion_tested':'Five sources at two tolerances: zero affine response with lambda=-1, positive finite-k/cubic source-specific chi, zero COM moment, quadratic-work identity and tolerance comparison within explicit thresholds.',
        'non_claims':P['non_claims'],'rows':rows}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'response_profiles.json').write_text(json.dumps(response_profiles,separators=(',',':'))+'\n')
print(json.dumps({'cases':len(rows),'fine_response':[{k:r[k] for k in ['name','chi_COM_projected','frame_lambda','COM_moment','work_relative_discrepancy']} for r in fine_rows]}))
