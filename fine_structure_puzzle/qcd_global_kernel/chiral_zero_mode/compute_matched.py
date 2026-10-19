#!/usr/bin/env python3
"""Bounded new matched-replacement / nonconstant-pion checks; no fit inputs."""
import hashlib
import json
from pathlib import Path
import sys
import time
import mpmath as mp
import sympy as sp

BASE = Path(__file__).resolve().parent
INPUTS = json.loads((BASE / 'INPUTS.json').read_text())
COUNTS = {}


def number(value):
    if isinstance(value, str) and '/' in value:
        a, b = value.split('/')
        return mp.mpf(a) / mp.mpf(b)
    return mp.mpf(value)


def check(name, got, expected, tolerance):
    err = abs(got - expected) / max(mp.mpf(1), abs(expected))
    if err > tolerance:
        raise AssertionError('%s: err=%s got=%s expected=%s' % (name, err, got, expected))
    COUNTS[name.split(':')[0]] = COUNTS.get(name.split(':')[0], 0) + 1
    return err


def exact_checks():
    a0, a1, a2, a3, p1, p2, p3, F, G = sp.symbols('a0 a1 a2 a3 p1 p2 p3 F G', real=True)
    aa = sp.Matrix([a1, a2, a3]); pp = sp.Matrix([p1, p2, p3])
    p2sum = (pp.dot(pp))
    a0new = a0 * (1-p2sum/(2*F**2)) - aa.dot(pp)/F
    anew = aa*(1-p2sum/(2*F**2)) + (a0*pp-aa.cross(pp))/F

    def contract(expr):
        out = 0
        for powers, coef in sp.Poly(sp.expand(expr), p1, p2, p3).terms():
            if sum(powers) == 0:
                out += coef
            elif sum(powers) == 2 and 2 in powers:
                out += G * coef
        return sp.expand(out)

    s = a1**2+a2**2; norm = a0**2+a1**2+a2**2+a3**2
    assert sp.simplify(contract(a0new)-a0*(1-3*G/(2*F**2))) == 0
    assert sp.simplify(contract(anew[0]**2+anew[1]**2)-s-G/F**2*(2*norm-4*s)) == 0
    tau = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.diag(1, -1)]
    U = a0*sp.eye(2)+sp.I*sum((a*t for a, t in zip([a1,a2,a3], tau)), sp.zeros(2))
    Q = sp.eye(2)/6+tau[2]/2
    trace = sp.expand(sp.trace(Q*U*Q*U.conjugate().T))
    assert sp.simplify(trace-(sp.Rational(5,9)*norm-s)) == 0
    comm = Q*U-U*Q
    assert sp.simplify(sp.trace(comm*comm.conjugate().T)-2*s) == 0
    # Spectral finite-part simplification, independent of numerical fit.
    A = sp.Rational(5,2)
    hzminus1 = -(A*A-A+sp.Rational(1,6))/2
    fp = hzminus1/3+sp.Rational(3,8)-(sp.harmonic(3)-2*sp.EulerGamma)/3
    assert sp.simplify(fp-(2*sp.EulerGamma/3-sp.Rational(8,9))) == 0
    a,b=sp.symbols('a b', positive=True)
    k=1/(2*(a+2*b))+1/(8*a)-a/(a+2*b)**2
    assert sp.simplify(k+3/(8*a)-b*(3*a+2*b)/(a*(a+2*b)**2)) == 0
    assert sp.simplify(sp.diff(k,b)-(3*a-2*b)/(a+2*b)**3) == 0
    return {'polynomial_contraction': 'exact', 'dashen_trace': 'exact',
            'photon_seagull_trace': 'exact', 'zeta_finitepart': str(fp),
            'saddle_coefficient_derivatives': 'exact'}


def gauss_rule(n):
    # Bounded Newton iteration; nodes are independently regenerated at each precision.
    rows=[]
    for i in range(1, (n+1)//2+1):
        z=mp.cos(mp.pi*(mp.mpf(i)-mp.mpf('0.25'))/(n+mp.mpf('0.5')))
        for _ in range(30):
            p0,p1=mp.mpf(1),z
            for j in range(2,n+1):
                p0,p1=p1,((2*j-1)*z*p1-(j-1)*p0)/j
            deriv=n*(z*p1-p0)/(z*z-1)
            dz=p1/deriv
            z-=dz
            if abs(dz)<mp.eps*8:
                break
        else:
            raise AssertionError('Gauss root did not converge')
        # Re-evaluate derivative at the final root.
        p0,p1=mp.mpf(1),z
        for j in range(2,n+1):
            p0,p1=p1,((2*j-1)*z*p1-(j-1)*p0)/j
        deriv=n*(z*p1-p0)/(z*z-1)
        weight=1/((1-z*z)*deriv*deriv)
        rows.append(((1-z)/2,weight))
        rows.append(((1+z)/2,weight))
    assert len(rows)==n
    rows.sort()
    check('quadrature_weight',sum(w for _,w in rows),1,mp.mpf('1e-32'))
    return rows


def make_integrator():
    rules={}; cache={}

    def moments(x,y,n=None):
        if n is None:
            n=64 if x+2*y<100 else (128 if x+2*y<700 else 256)
        key=(mp.nstr(x,mp.mp.dps),mp.nstr(y,mp.mp.dps),n)
        if key in cache:
            return cache[key]
        if n not in rules:
            rules[n]=gauss_rule(n)
        raw={(i,j):mp.mpf(0) for i in range(4) for j in range(4-i)}
        for s,w in rules[n]:
            r=mp.sqrt(1-s); t=x*r
            i0=mp.besseli(0,t); i1=mp.besseli(1,t)
            if t==0:
                angular=[mp.mpf(1),mp.mpf(0),(1-s)/2,mp.mpf(0)]
            else:
                i2=i0-2*i1/t; i3=i1-4*i2/t
                angular=[i0,r*i1,(1-s)*(i0+i2)/2,r**3*(3*i1+i3)/4]
            common=w*mp.exp(-y*s-x)
            for i in range(4):
                for j in range(4-i):
                    raw[(i,j)]+=common*angular[i]*s**j
        zscaled=raw[(0,0)]
        raw={key:val/zscaled for key,val in raw.items()}
        m=raw[(1,0)]; q=raw[(0,1)]
        va=raw[(2,0)]-m*m; vs=raw[(0,2)]-q*q; c=raw[(1,1)]-m*q
        kaas=raw[(2,1)]-q*raw[(2,0)]-2*m*raw[(1,1)]+2*m*m*q
        kass=raw[(1,2)]-m*raw[(0,2)]-2*q*raw[(1,1)]+2*m*q*q
        ksss=raw[(0,3)]-3*q*raw[(0,2)]+2*q**3
        B=mp.mpf('1.5')*x*(m-1)-4*y*q
        E=mp.mpf('1.5')*x*x*va-mp.mpf('5.5')*x*y*c+4*y*y*vs
        By=-4*q-mp.mpf('1.5')*x*c+4*y*vs
        DBy=-mp.mpf('5.5')*x*c+8*y*vs-mp.mpf('1.5')*x*x*kaas+mp.mpf('5.5')*x*y*kass-4*y*y*ksss
        logz=x+mp.log(zscaled)
        wrep=-(logz-x+mp.log(x)/2+mp.log(x+2*y)-mp.log(2/mp.pi)/2)
        out={'x':x,'y':y,'logZ':logz,'Wrep':wrep,'m':m,'q':q,'va':va,'vs':vs,'cov':c,
             'kaas':kaas,'kass':kass,'ksss':ksss,'P_rep':x*(1-m)+y*q-mp.mpf('1.5'),
             'charge_rho_over_C':q+x*c-y*vs,'B':B,'DB':B+E,'By':By,'DBy':DBy,
             'T':B+mp.mpf('1.5')*x+2*y,'nodes':n}
        if va < -mp.mpf('1e-30') or vs < -mp.mpf('1e-30') or va*vs-c*c < -mp.mpf('1e-30'):
            raise AssertionError('Moment covariance is not positive semidefinite')
        cache[key]=out
        return out
    return moments


def fd1(fun,z,h):
    return (fun(z-2*h)-8*fun(z-h)+8*fun(z+h)-fun(z+2*h))/(12*h)


def numerical_checks(dps):
    mp.mp.dps=dps
    moments=make_integrator(); rows=[]; errors=[]
    h=number(INPUTS['finite_difference_step']); tol=number(INPUTS['derivative_tolerance'])
    gpref=number(INPUTS['metric_test_gpref']); glog=number(INPUTS['metric_test_glog'])
    g=gpref*glog; gdot=-g/2+gpref/2
    for index,case in enumerate(INPUTS['finite_cases']):
        x,y=map(number,case); r=moments(x,y); rows.append(r)
        if index<3:
            p=fd1(lambda t:moments(x*mp.exp(t),y*mp.exp(t))['Wrep'],mp.mpf(0),h)
            errors.append(check('metric_Q:%d'%index,p,r['P_rep'],tol))
            dcharge=fd1(lambda b:moments(x,b)['P_rep'],y,h)
            errors.append(check('charge_covariance:%d'%index,dcharge,r['charge_rho_over_C'],tol))
            qcharge=fd1(lambda b:moments(x,b)['Wrep'],y,h)
            errors.append(check('charge_Q:%d'%index,qcharge,r['q']-2/(x+2*y),tol))
            db=fd1(lambda t:moments(x*mp.exp(t),y*mp.exp(t))['B'],mp.mpf(0),h)
            errors.append(check('DB:%d'%index,db,r['DB'],tol))
            by=fd1(lambda b:moments(x,b)['B'],y,h)
            errors.append(check('By:%d'%index,by,r['By'],tol))
            dby=fd1(lambda t:moments(x*mp.exp(t),y*mp.exp(t))['By'],mp.mpf(0),h)
            errors.append(check('DBy_third_cumulants:%d'%index,dby,r['DBy'],tol))
            def interaction(t):
                gt=gpref*mp.exp(-t/2)*(glog+t/2)
                return gt*moments(x*mp.exp(t),y*mp.exp(t))['B']
            di=fd1(interaction,mp.mpf(0),h)
            errors.append(check('extra_metric:%d'%index,di,gdot*r['B']+g*r['DB'],tol))
            def interaction_rho(b):
                v=moments(x,b)
                return gdot*v['B']+g*v['DB']
            dic=fd1(interaction_rho,y,h)
            errors.append(check('extra_charge_metric:%d'%index,dic,(gdot+g)*r['By']+g*r['DBy'],tol))
    # Independent tanh-sinh quadrature for the new replacement point, not an old Haar grid.
    x,y=map(number,INPUTS['independent_quadrature_case'])
    zts=mp.quad(lambda s:mp.exp(-y*s-x)*mp.besseli(0,x*mp.sqrt(1-s)),[0,mp.mpf('0.5'),1])
    ref=moments(x,y)
    errors.append(check('independent_tanh_sinh_Q',mp.log(zts)+x,ref['logZ'],number(INPUTS['quadrature_tolerance'])))
    for case in INPUTS['doubled_rule_cases']:
        x,y=map(number,case); r1=moments(x,y,128); r2=moments(x,y,256)
        for k in ['Wrep','P_rep','charge_rho_over_C','B','DB','By','DBy']:
            errors.append(check('doubled_quadrature:'+k,r1[k],r2[k],number(INPUTS['quadrature_tolerance'])))
    # Uniform-axis source check unique to the new interaction, exact x=0.
    ym=number(INPUTS['massless_interaction_y'])
    q0=1/ym-1/mp.expm1(ym)
    T0=2*ym-4*ym*q0; B0=-4*ym*q0
    errors.append(check('massless_T_no_linear_term',T0/ym**2,mp.mpf(1)/3,mp.mpf('1e-12')))
    errors.append(check('massless_aligned_subtraction',T0-B0,2*ym,mp.mpf('1e-30')))
    saddle=[]; previous=None
    for value in INPUTS['saddle_x']:
        V=number(value); a=mp.mpf(1); b=mp.mpf(2); x=a*V;y=b*V
        r=moments(x,y); k=1/(2*(a+2*b))+1/(8*a)-a/(a+2*b)**2
        scaled=r['P_rep']*V  # V^2 rho_rep
        charge_scaled=r['charge_rho_over_C']*V**2
        target=(3*a-2*b)/(a+2*b)**3
        err=abs(scaled-k)
        if previous is not None and not err<previous:
            raise AssertionError('Saddle remainder did not decrease')
        previous=err
        check('saddle_replacement',scaled,k,mp.mpf('0.01'))
        check('saddle_charge',charge_scaled,target,mp.mpf('0.001'))
        if not charge_scaled<0:
            raise AssertionError('Declared negative charge response missing')
        saddle.append({'x':x,'y':y,'V2_rho_rep':scaled,'k_target':k,
                       'V2_charge_rho_over_C':charge_scaled,'charge_target':target,
                       'scaled_error':err})
    return {'dps':dps,'finite':rows,'saddle':saddle,'max_control_error':max(errors)}


def spectral_checks():
    mp.mp.dps=number(INPUTS['precisions_decimal'][-1]).__int__()
    A=mp.mpf('2.5'); c=mp.mpf('2.25'); K=INPUTS['spectral_terms']; e=number(INPUTS['spectral_epsilon'])
    r=c/A**2
    tail=A*(1+A)*(1+1/(4*A*A))/3*r**K*((K+1)/(1-r)+r/(1-r)**2)
    def finite_at(delta):
        p=1+delta; total=mp.mpf(0); coef=mp.mpf(1)
        for k in range(K):
            if k:
                coef*=c*(p+k-1)/k
            total+=coef*(mp.zeta(2*p+2*k-3,A)-mp.zeta(2*p+2*k-1,A)/4)/3
        return total-1/(3*delta)
    fs=[finite_at(j*e) for j in [1,2,3,4]]
    extrap=4*fs[0]-6*fs[1]+4*fs[2]-fs[3]
    target=2*mp.euler/3-mp.mpf(8)/9
    err=check('S4_zeta_Laurent',extrap,target,number(INPUTS['spectral_tolerance']))
    if not tail<number(INPUTS['spectral_tolerance'])/100:
        raise AssertionError('Spectral tail too large')
    return {'terms':K,'epsilon':e,'finite_values':fs,'extrapolated_finitepart':extrap,
            'analytic_finitepart':target,'error':err,'per_value_analytic_tail_bound':tail,
            'pole_residue':'1/3','Gbar_pole_coefficient':'R/(96*pi^2)'}


def serialize(value):
    if isinstance(value,dict):
        return {str(k):serialize(v) for k,v in value.items()}
    if isinstance(value,list):
        return [serialize(v) for v in value]
    if isinstance(value,mp.mpf):
        return mp.nstr(value,38)
    return value


def main():
    started=time.monotonic(); exact=exact_checks()
    runs=[numerical_checks(dps) for dps in INPUTS['precisions_decimal']]
    diffs=[]
    for a,b in zip(runs[0]['finite'],runs[1]['finite']):
        for key in ['Wrep','P_rep','charge_rho_over_C','B','DB','By','DBy']:
            diffs.append(check('repeated_precision:'+key,a[key],b[key],number(INPUTS['precision_tolerance'])))
    spectral=spectral_checks()
    result={'claim_id':'FSP008_MATCHED_COMPACT_CHIRAL_CONTINUATION','status':'passed',
            'new_delta':'exact/Gaussian replacement and first nonconstant-pion source contraction with aligned Gaussian subtraction',
            'ancestry_overlap':'raw Haar/Dashen integral and old finite grid belong to FSP003; not new here',
            'exact':exact,'runs':runs,'spectral':spectral,'checks_by_family':COUNTS,
            'max_repeated_precision_error':max(diffs),'elapsed_seconds':time.monotonic()-started,
            'non_claims':INPUTS['non_claims']}
    output=Path(sys.argv[1]); output.write_text(json.dumps(serialize(result),indent=2)+'\n')
    print(json.dumps({'status':'passed','checks':sum(COUNTS.values()),'elapsed_seconds':time.monotonic()-started,
                      'max_repeated_precision_error':mp.nstr(max(diffs),8)}))


if __name__=='__main__':
    main()
