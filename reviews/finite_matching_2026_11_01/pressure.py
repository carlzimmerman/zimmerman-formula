"""Fixed-order finite vacuum+current matched native-phase pressure.

Omega=V-F omega²-J omega⁴/2. V includes complete two-loop vacuum
graphs and heavy displacement once. F includes full one-loop component
current matching and the heavy shift. J is the leading tree heavy response.
The field-independent classical vacuum is subtracted in every case.
"""
import sys
sys.dont_write_bytecode=True
import argparse,json,math,time,resource
from pathlib import Path
import mpmath as mp
import numpy as np
from numpy.polynomial import Chebyshev
from scipy.optimize import brentq
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'gauge_diagrams'))
sys.path.insert(0,str(BASE/'current_matching'))
from full import calculate as vacuum
from current import calculate as current
from pressure_scan import cw


def main(out):
    start=time.monotonic();mp.mp.dps=55;cache={};cases=[];fit_controls=[]
    zmin=7.367143721278508
    e0=.03;range_s=[-.05,math.log(1.4)];active_fit=None
    def exact_coefficients(s,e):
        x=zmin/math.sqrt(31*e)*math.exp(s);xmin=zmin/math.sqrt(31*e);Q2=e/31+(e*xmin)**2;g=math.sqrt(29/200)*e
        v=vacuum(x,e,e,g,1.,Q2,True);k=current(x,e,e,g,1.,Q2)
        return {'U2':v['V2_reduced'],'dFh':v['deltaF_heavy'],'dFk':k['total'],'J':v['J_heavy'],
                'vacuum':v,'current':k}
    def fit_coefficients(n):
        nodes=np.cos(np.pi*(np.arange(n)+.5)/n)
        ss=(range_s[0]+range_s[1])/2+nodes*(range_s[1]-range_s[0])/2
        exact=[exact_coefficients(float(s),e0) for s in ss]
        return {k:Chebyshev.fit(ss,[d[k] for d in exact],n-1,domain=range_s) for k in ['U2','dFh','dFk','J']}
    def coefficients(lx,e):
        key=(float(lx).hex(),float(e).hex(),active_fit['n'])
        if key not in cache:
            x=math.exp(lx);xmin=zmin/math.sqrt(31*e);s=lx-math.log(xmin);scale=e/e0
            c=[mp.mpf(e),mp.mpf(e),mp.sqrt(mp.mpf(29)/200)*mp.mpf(e)]
            fit=active_fit['fit']
            cache[key]={'U1':cw(mp.mpf(x),*c),'U2':mp.mpf(float(fit['U2'](s)))*scale**4,
                        'F0':31*mp.mpf(x)**2,'dFh':mp.mpf(float(fit['dFh'](s)))*scale,
                        'dFk':mp.mpf(float(fit['dFk'](s)))*scale,'J':mp.mpf(float(fit['J'](s)))/scale**2}
        return cache[key]
    def values(lx,e,scheme):
        c=coefficients(lx,e)
        if scheme=='one_loop_tree_current':return dict(V=c['U1'],F=c['F0'],J=mp.mpf(0))
        if scheme=='finite_vacuum_heavy':return dict(V=c['U1']+c['U2'],F=c['F0']+c['dFh'],J=c['J'])
        if scheme=='finite_current_only':return dict(V=c['U1'],F=c['F0']+c['dFk'],J=mp.mpf(0))
        if scheme=='finite_matched':return dict(V=c['U1']+c['U2'],F=c['F0']+c['dFh']+c['dFk'],J=c['J'])
        raise ValueError(scheme)
    def stencil(lx,e,scheme,h):
        pts=[values(lx+j*h,e,scheme) for j in (-2,-1,0,1,2)];o=dict(pts[2])
        for k in ['V','F','J']:
            z=[q[k] for q in pts]
            o[k+'s']=(z[0]-8*z[1]+8*z[3]-z[4])/(12*h)
            o[k+'ss']=(-z[0]+16*z[1]-30*z[2]+16*z[3]-z[4])/(12*h*h)
        return o
    def point(lx,e,scheme,h,vac):
        d=stencil(lx,e,scheme,h);Vs,Fs,Js=d['Vs'],d['Fs'],d['Js'];F,J=d['F'],d['J']
        disc=Fs*Fs+2*Js*Vs
        if disc<=0 or Vs<=0 or Fs<=0:raise ValueError('inadmissible phase source')
        q=2*Vs/(Fs+mp.sqrt(disc));om=mp.sqrt(q)
        N=d['Vss']-d['Fss']*q-d['Jss']*q*q/2
        C=2*F+6*J*q;M=-2*om*(Fs+Js*q);D=N+M*M/C;n=2*om*(F+J*q)
        P=F*q+J*q*q/2-d['V']+vac;E=F*q+3*J*q*q/2+d['V']-vac
        cs=n*N/(om*C*D)
        return dict(Omega_ss=N,fixed_charge_D=D,partial_susceptibility=C,n=n,omega2=q,P_ex=P,epsilon_ex=E,w_ex=P/E,cs2_IR=cs)
    def clean(d):return {k:float(v) for k,v in d.items()}
    for node_count in [21,29]:
      active_fit={'n':node_count,'fit':fit_coefficients(node_count)}
      # Off-node checks directly evaluate independent diagrams, also checking
      # exact coupling scaling rather than assuming it numerically.
      for s in [-.017,math.log(1.12),math.log(1.3)]:
        for echeck in [.01,.03]:
          ex=exact_coefficients(s,echeck);e_ratio=echeck/e0
          errors={k:abs(float(active_fit['fit'][k](s))*e_ratio**power-ex[k])/max(abs(ex[k]),1e-100)
                  for k,power in [('U2',4),('dFh',1),('dFk',1),('J',-2)]}
          fit_controls.append(dict(nodes=node_count,e=echeck,s=s,relative_errors=errors))
      for e in [.01,.03]:
        xmin=zmin/math.sqrt(31*e);lxref=math.log(xmin)
        for scheme in ['one_loop_tree_current','finite_vacuum_heavy','finite_current_only','finite_matched']:
            # All three stencils are actual independent root solves.
            for hh in [.01,.005,.0025]:
                h=mp.mpf(hh)
                lx0=brentq(lambda x:float(stencil(x,e,scheme,h)['Vs']),lxref-.03,lxref+.03,xtol=2e-12)
                vac=values(lx0,e,scheme)['V']
                root=brentq(lambda r:float(point(lx0+math.log(r),e,scheme,h,vac)['Omega_ss']),1.15,1.28,xtol=2e-10)
                samples=[dict(X_over_min=r,**clean(point(lx0+math.log(r),e,scheme,h,vac))) for r in [1.01,1.05,1.2,1.3]]
                boundary=clean(point(lx0+math.log(root),e,scheme,h,vac))
                c=coefficients(lx0+math.log(root),e)
                ck=exact_coefficients(lx0+math.log(root)-lxref,e)['current']
                # Thermodynamic identity at a stable interior point, independent
                # of the analytic elimination used to calculate cs².
                ds=1e-4;ps=point(lx0+math.log(1.05)+ds,e,scheme,h,vac);ms=point(lx0+math.log(1.05)-ds,e,scheme,h,vac)
                direct=(ps['P_ex']-ms['P_ex'])/(mp.log(ps['n'])-mp.log(ms['n']))
                ref=point(lx0+math.log(1.05),e,scheme,h,vac)
                therm=ref['cs2_IR']*ref['n']*mp.sqrt(ref['omega2'])
                row=dict(e=e,scheme=scheme,stencil_h=hh,interpolation_nodes=node_count,X_min=math.exp(lx0),X_min_over_one_loop=math.exp(lx0)/xmin,
                         boundary_ratio=root,boundary=boundary,samples=samples,direct_pressure_relative_error=float(abs(direct/therm-1)),
                         finite_current_fraction=float(c['dFk']/c['F0']),heavy_current_fraction=float(c['dFh']/c['F0']),
                         omega2_over_heavy_mass2=float(boundary['omega2']/(2*e)),
                         current_parts=ck)
                cases.append(row)
                print(json.dumps({k:row[k] for k in ['e','scheme','stencil_h','X_min_over_one_loop','boundary_ratio','finite_current_fraction','direct_pressure_relative_error']}),flush=True)
    checks={'case_count_48':len(cases)==48,'all_positive_D_C':all(r['boundary']['fixed_charge_D']>0 and r['boundary']['partial_susceptibility']>0 and all(s['fixed_charge_D']>0 and s['partial_susceptibility']>0 for s in r['samples']) for r in cases),
            'positive_cs_at_1p2':all(r['samples'][2]['cs2_IR']>0 for r in cases),
            'negative_cs_at_1p3':all(r['samples'][3]['cs2_IR']<0 for r in cases),
            'pressure_rich_endpoint':all(r['boundary']['w_ex']>.5 for r in cases),
            'direct_thermodynamic_error_below_2e-4':max(r['direct_pressure_relative_error'] for r in cases)<2e-4,
            'off_node_and_scaling_relative_errors_below_2e-5':max(v for r in fit_controls for v in r['relative_errors'].values())<2e-5}
    convergence=[]
    for e in [.01,.03]:
        for scheme in ['one_loop_tree_current','finite_vacuum_heavy','finite_current_only','finite_matched']:
            rr=[r for r in cases if r['e']==e and r['scheme']==scheme and r['interpolation_nodes']==29]
            other=[r for r in cases if r['e']==e and r['scheme']==scheme and r['interpolation_nodes']==21][-1]
            delta=abs(rr[-1]['boundary_ratio']-rr[-2]['boundary_ratio']);interp=abs(rr[-1]['boundary_ratio']-other['boundary_ratio'])
            convergence.append(dict(e=e,scheme=scheme,last_two_root_difference=delta,interpolation_root_difference=interp))
    checks['root_repeats_below_2e-5']=max(c['last_two_root_difference'] for c in convergence)<2e-5
    checks['interpolation_root_repeats_below_2e-5']=max(c['interpolation_root_difference'] for c in convergence)<2e-5
    result=dict(claim_id='TP03_FINITE_MATCHED_PHASE',checks=checks,all_checks_pass=all(checks.values()),cases=cases,convergence=convergence,fit_controls=fit_controls,
                coefficient_evaluations=len(cache),runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                perturbative_scope='Complete finite two-loop vacuum plus one-loop two-derivative phase current and same-order classical heavy occupied response, at fixed weak couplings and Q. Algebraic truncated action is solved exactly; terms beyond its stated order are not controlled.',
                non_claims=['No all-orders finite remainder bound','No selected cosmological charge, protected lifetime, quantum confinement or gravity completion','No complete higher-derivative/nonlocal massless-current action','This native phase has exponent2, not the old waterbag comparator'])
    Path(out).write_text(json.dumps(result,indent=2)+'\n');assert result['all_checks_pass'],checks

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);main(p.parse_args().out)
