"""High-precision full-spectrum CW/pressure via analytic SU(5) representation blocks."""
import json,sys,resource
from pathlib import Path
import mpmath as mp
mp.mp.dps=50

def eig2(a,b,c):
    tr=a+c;disc=mp.sqrt((a-c)**2+4*b*b)
    return [(tr-disc)/2,(tr+disc)/2]

def masses(X,h,lam,g):
    a=mp.sqrt(2*h/(30*h*h+lam*lam));b=h*X/lam;c=lam*lam*h/(30*h*h+lam*lam)
    out=[]
    for name,r,mult in [('SU3',mp.mpf(2),8),('SU2',mp.mpf(-3),3),('broken',mp.mpf('-.5'),12)]:
        m=(1+r)*h*X;q=r*lam*a;split=(1+r)*c
        A=m*m+q*q+split;B=-m*q;C=q*q
        if name=='broken':
            A+=(5*g*a)**2;B-=(5*g)**2*a*b;C+=(5*g*b)**2
        es=eig2(A,B,C)+eig2(m*m+q*q-split,m*q,q*q)
        if name=='broken':
            mat=mp.matrix([[m,q,5*g*a],[q,0,5*g*b],[5*g*a,5*g*b,0]])
            ef=[v*v for v in mp.eigsy(mat,eigvals_only=True)]
            ev=[25*g*g*(a*a+b*b)]
        else:ef=eig2(m*m+q*q,m*q,q*q);ev=[]
        out.append((name,mult,es,ef,ev))
    # The remaining singlet and unbroken-gauge contributions cancel/vanish identically.
    return out

def cw(X,h,lam,g,details=False):
    out=masses(X,h,lam,g);parts={};s4=mp.mpf(0);s2=mp.mpf(0);minimum=mp.inf
    def ht(vals):
        total=mp.mpf(0)
        for v in vals:
            if v < -mp.mpf('1e-38'):raise ValueError('negative physical tree mass')
            if v>mp.mpf('1e-38'):total+=v*v*(mp.log(v)-mp.mpf('1.5'))
        return total
    for name,mult,es,ef,ev in out:
        parts[name]=mult*(ht(es)-2*ht(ef)+3*ht(ev))/(64*mp.pi**2)
        s4+=mult*(sum(v*v for v in es)-2*sum(v*v for v in ef)+3*sum(v*v for v in ev))
        s2+=mult*(sum(es)-2*sum(ef)+3*sum(ev))
        minimum=min(minimum,min(es))
    return (sum(parts.values()),parts,s4,s2,minimum) if details else sum(parts.values())

def deriv(X,h,lam,g,step):
    vs=[cw(X*mp.exp(j*step),h,lam,g) for j in (-2,-1,0,1,2)]
    d=(vs[0]-8*vs[1]+8*vs[3]-vs[4])/(12*step)
    dd=(-vs[0]+16*vs[1]-30*vs[2]+16*vs[3]-vs[4])/(12*step*step)
    return d,dd

def main(path):
    from block_spectrum import sectors,flattened,cw_value
    controls=[]
    for x in (mp.mpf('.1'),mp.mpf(1),mp.mpf(10)):
        h=lam=mp.mpf('.6');g=mp.sqrt(mp.mpf(29)/200)*lam
        ss=sectors(x,h,lam,g)
        fast=masses(x,h,lam,g)
        errors=[]
        for sk,key in [(2,'scalars'),(3,'Weyls'),(4,'vectors')]:
            a=sorted(v for block in fast for v in block[sk] for _ in range(block[1]))
            b=sorted(v for block in ss[:3] for v in block[key] for _ in range(block['multiplicity']))
            errors.append(max(abs(v-w) for v,w in zip(a,b)))
        controls.append({'X':str(x),'max_eigen_difference':str(max(errors)),
                         'CW_difference':str(abs(cw(x,h,lam,g)-cw_value(x,h,lam,g)))})
    assert max(mp.mpf(r['max_eigen_difference']) for r in controls)<mp.mpf('1e-35')
    rows=[];summaries=[];step=mp.mpf('.005');worst=mp.mpf(0)
    for h in map(mp.mpf,('.3','.6','1')):
        for lam in map(mp.mpf,('.3','.6','1')):
            g=mp.sqrt(mp.mpf(29)/200)*lam;local=[]
            for j in range(81):
                X=mp.power(10,mp.mpf(-2)+mp.mpf(j)/20)
                val,parts,s4,s2,minmass=cw(X,h,lam,g,True)
                d,dd=deriv(X,h,lam,g,step);d2,dd2=deriv(X,h,lam,g,step/2)
                err=max(abs(d-d2),abs(dd-dd2));worst=max(worst,err)
                U=lam*lam/(lam*lam+30*h*h)+val
                source=d2>0;radial=2*d2+dd2>0;comp=dd2-3*d2
                row={'h':float(h),'lambda':float(lam),'X':float(X),'U':float(U),'CW':float(val),
                     'U_s':float(d2),'U_ss':float(dd2),'U_ss_minus_3U_s':float(comp),
                     'positive_source':bool(source),'radial_stability':bool(radial),
                     'positive_compressibility':bool(comp>0),'derivative_abs_repeat_difference':float(err),
                     'STr_M2':float(s2),'STr_M4':float(s4),'tree_scalar_min':float(minmass)}
                if source and radial:
                    row['dP_dlnrho']=float(5*d2*comp/(9*(2*d2+dd2)))
                local.append(row);rows.append(row)
            mins=[];pressure=[]
            # Bracket finite-threshold minima and first stable-branch compressibility transitions.
            for left,right in zip(local,local[1:]):
                if left['U_s']<0<right['U_s']:
                    lo=mp.mpf(left['X']);hi=mp.mpf(right['X'])
                    for _ in range(36):
                        mid=mp.sqrt(lo*hi);dm=deriv(mid,h,lam,g,step/2)[0]
                        if dm>0:hi=mid
                        else:lo=mid
                    xx=mp.sqrt(lo*hi);d0,dd0=deriv(xx,h,lam,g,step/2)
                    vv=cw(xx,h,lam,g);u0=lam*lam/(lam*lam+30*h*h)+vv
                    mins.append({'X':float(xx),'U':float(u0),'U_s':float(d0),'U_ss':float(dd0),
                                 'Bcurv_over_U':float(dd0/(9*u0))})
                if left['positive_source'] and right['positive_source'] and left['U_ss_minus_3U_s']>0>right['U_ss_minus_3U_s']:
                    lo=mp.mpf(left['X']);hi=mp.mpf(right['X'])
                    for _ in range(36):
                        mid=mp.sqrt(lo*hi);dm,ddm=deriv(mid,h,lam,g,step/2)
                        if ddm-3*dm>0:lo=mid
                        else:hi=mid
                    xx=mp.sqrt(lo*hi);d0,dd0=deriv(xx,h,lam,g,step/2)
                    pressure.append({'X':float(xx),'U_s':float(d0),'U_ss':float(dd0),
                                     'Wss':float(2*d0+dd0),'X_over_minimum':float(xx)/mins[-1]['X'] if mins else None})
            summaries.append({'h':float(h),'lambda':float(lam),'minima':mins,'pressure_boundaries':pressure,
                              'positive_source_grid_count':sum(r['positive_source'] for r in local),
                              'stable_positive_source_compressible_grid_count':sum(r['positive_source'] and r['radial_stability'] and r['positive_compressibility'] for r in local),
                              'source_stable_negative_compressibility_grid_count':sum(r['positive_source'] and r['radial_stability'] and not r['positive_compressibility'] for r in local)})
    checks={'three_fast_block_controls':True,'729_cases':len(rows)==729,
            'supertrace2_50digit':max(abs(r['STr_M2']) for r in rows)<1e-35,
            'supertrace4_critical_50digit':max(abs(r['STr_M4']) for r in rows)<1e-32,
            'no_resolved_tree_tachyons':min(r['tree_scalar_min'] for r in rows)>-1e-35,
            'derivative_repeat_absolute_difference_below_1e-8':worst<mp.mpf('1e-8')}
    result={'claim_id':'TP01_THRESHOLD_PRESSURE','mp_dps':mp.mp.dps,'checks':checks,'controls':controls,
            'case_count':len(rows),'summaries':summaries,'cases':rows,
            'max_derivative_repeat_abs_difference':float(worst),'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'non_claims':['Fixed-coupling one-loop threshold potential only, not RG-resummed two-loop vacuum location',
                          'No derived particle portal or occupied-state kinetic matching','No full transverse quantum Hessian or IR confinement contribution',
                          'Finite grid signs plus numerical roots are not an all-coupling theorem']}
    Path(path).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['checks','summaries','max_derivative_repeat_abs_difference','peak_rss_bytes_macos']},indent=2))
    assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
