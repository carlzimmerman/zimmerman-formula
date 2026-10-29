"""Exact group/flow checks and nine finite leading-log vacuum trajectories."""
import json,math,sys
from pathlib import Path
import numpy as np
import scipy
import sympy as sp
from scipy.integrate import solve_ivp

k=1/(16*math.pi**2)

def gammas(h,l,g):return np.array([12*h*h,h*h+2.1*l*l-10*g*g,1.05*l*l-10*g*g])*k
def rhs(t,z):
    h,l,g,logf=z;gx,ga,gb=gammas(h,l,g)
    return [h*(gx+2*ga),l*(gb+2*ga),-5*k*g**3,gx]
def logV(z):
    h,l,g,logf=z
    return 2*logf+2*math.log(l)-math.log(l*l+30*h*h)
def ratio(h,l):return 29/(12*(16*math.pi**2)**2)*h*h*l*l*(16*h*h+13*l*l)/(l*l+30*h*h)

def symbolic():
    h,l,g=sp.symbols('h l g',positive=True);kk=sp.symbols('k',positive=True)
    gx=12*h*h*kk;ga=(h*h+sp.Rational(21,10)*l*l-10*g*g)*kk;gb=(sp.Rational(21,20)*l*l-10*g*g)*kk
    beta=[h*(gx+2*ga),l*(gb+2*ga),-5*kk*g**3]
    ge=(l*l*gx+30*h*h*gb)/(l*l+30*h*h)
    closed=kk*h*h*(sp.Rational(87,2)*l*l-300*g*g)/(l*l+30*h*h)
    derivative=sum(sp.diff(ge,z)*b for z,b in zip([h,l,g],beta))
    crit={g:sp.sqrt(sp.Rational(29,200))*l}
    target=sp.Rational(29,12)*kk*kk*h*h*l*l*(16*h*h+13*l*l)/(l*l+30*h*h)
    logfeff=sp.log(l)-sp.log(l*l+30*h*h)/2
    effective_beta=gx+sum(sp.diff(logfeff,z)*b for z,b in zip([h,l,g],beta))
    return {key:bool(sp.simplify(value)==0) for key,value in {
      'weighted_anomalous_dimension':ge-closed,
      'effective_F_running':effective_beta-ge,
      'critical_coupling_surface':ge.subs(crit),
      'microscopic_stiffness_formula':(sp.Rational(2,9)*derivative).subs(crit)-target,
    }.items()}

def group_check():
    n=5;generators=[]
    for i in range(n):
        for j in range(i+1,n):
            a=np.zeros((n,n),complex);a[i,j]=a[j,i]=1/math.sqrt(2);generators.append(a)
            a=np.zeros((n,n),complex);a[i,j]=-1j/math.sqrt(2);a[j,i]=1j/math.sqrt(2);generators.append(a)
    for j in range(1,n):
        a=np.zeros((n,n),complex)
        for i in range(j):a[i,i]=1/math.sqrt(j*(j+1))
        a[j,j]=-j/math.sqrt(j*(j+1));generators.append(a)
    T=np.array(generators)
    gram=np.einsum('aij,bji->ab',T,T)
    sym=np.empty((24,24,24),complex);f=np.empty_like(sym)
    for a in range(24):
        for b in range(24):
            sym[a,b]=np.einsum('ij,cji->c',(T[a]@T[b]+T[b]@T[a])/2,T)
            f[a,b]=np.einsum('ij,cji->c',-1j*(T[a]@T[b]-T[b]@T[a])/math.sqrt(2),T)
    dgram=np.einsum('abc,abd->cd',sym,np.conj(sym))
    fgram=np.einsum('abc,abd->cd',f,np.conj(f))
    return {'generator_count':len(T),'orthonormality_error':float(np.max(abs(gram-np.eye(24)))),
            'symmetric_contraction_error':float(np.max(abs(dgram-2.1*np.eye(24)))),
            'adjoint_Casimir_error':float(np.max(abs(fgram-5*np.eye(24))))}

def main(path):
    checks=symbolic();group=group_check();rows=[]
    for h in [.3,.6,1.]:
        for l in [.3,.6,1.]:
            g=math.sqrt(29/200)*l;z0=[h,l,g,0.]
            forward=solve_ivp(rhs,[0,.5],z0,method='DOP853',rtol=2e-12,atol=2e-14,dense_output=True)
            backward=solve_ivp(rhs,[0,-.5],z0,method='DOP853',rtol=2e-12,atol=2e-14,dense_output=True)
            assert forward.success and backward.success
            def value(t):return math.exp(logV((forward if t>=0 else backward).sol(t)))
            step=.02;vals=[value(i*step) for i in [-2,-1,0,1,2]]
            curvature=(-vals[0]+16*vals[1]-30*vals[2]+16*vals[3]-vals[4])/(12*step*step*vals[2]*9)
            reference=ratio(h,l)
            rows.append({'h':h,'lambda':l,'g_critical':g,'V_model_over_f2':vals[2],
                         'B_curv_over_V_leading_log':reference,'ODE_finite_difference_ratio':curvature,
                         'ratio_relative_error':abs(curvature/reference-1),'V_minus_over_V0':value(-.5)/vals[2],
                         'V_plus_over_V0':value(.5)/vals[2],'max_abs_one_loop_gamma_at_vacuum':float(max(abs(gammas(h,l,g))))})
    checks.update({'24_generator_group_checks':group['generator_count']==24 and max(group[k] for k in ['orthonormality_error','symmetric_contraction_error','adjoint_Casimir_error'])<1e-12,
                   'all_nine_RG_curvatures':max(r['ratio_relative_error'] for r in rows)<2e-4,
                   'all_nine_local_RG_minima':all(r['V_minus_over_V0']>1 and r['V_plus_over_V0']>1 for r in rows),
                   'vacuum_anomalous_dimensions_below_point_one':max(r['max_abs_one_loop_gamma_at_vacuum'] for r in rows)<.1})
    result={'claim_id':'MV28_INVERTED','checks':checks,'group_checks':group,'cases':rows,'software':{'Python':sys.version.split()[0],'NumPy':np.__version__,'SciPy':scipy.__version__,'SymPy':sp.__version__},'non_claims':['No full gauged threshold/spectrum validation','No full supergravity vacuum matching','No microscopic coupling selection','No halo portal derivation or viable dense pressure proof']}
    Path(path).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
