"""High-precision analytic response and independent boundary-value solve."""
import argparse,json
from pathlib import Path
import mpmath as mp
mp.mp.dps=70

def response(A,y):
    A=mp.mpf(A);y=mp.mpf(y);x=mp.sqrt(A)*y
    # R=I=1. Closed form and an independently solved matching system.
    b=3*mp.exp(-1j*y)*(x*mp.cos(x)-mp.sin(x))/(x*x*(x*mp.cos(x)-1j*y*mp.sin(x)))
    a=3/(x*x)*(1j*y-1)/(x*mp.cos(x)-1j*y*mp.sin(x))
    G=3/(x*x)+3*a*(mp.sin(x)-x*mp.cos(x))/(x*x)
    aa,bb=mp.lu_solve(mp.matrix([[mp.sin(x),-mp.exp(1j*y)],
                                [x*mp.cos(x),-1j*y*mp.exp(1j*y)]]),
                       mp.matrix([-3/x**2,-3/x**2]))
    # Direct quadrature of the interior field, not its integrated formula.
    quad=mp.quad(lambda r:3*(3*r*r/x**2+aa*r*mp.sin(x*r)),[0,1])
    return b,G,max(abs(a-aa),abs(b-bb)),abs(G-quad)

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
rows=[];passivity=mp.mpf(0);match=mp.mpf(0);quad=mp.mpf(0);form=mp.mpf(0)
for A in [1,2,10,100,1000]:
 for x0 in ['0.001','0.01','0.1','0.5','1','1.57079632679489661923','2','3','4','5','8']:
    y=mp.mpf(x0)/mp.sqrt(A);b,G,er,eq=response(A,y)
    ep=abs(-G.imag-y*abs(b)**2)/max(mp.mpf(1),y*abs(b)**2)
    passivity=max(passivity,ep);match=max(match,er);quad=max(quad,eq)
    if A==1:
        target=-3*(mp.sin(y)-y*mp.cos(y))/y**3
        form=max(form,abs(b-target))
    rows.append({'A':A,'omega_R':float(y),'internal_phase':float(mp.mpf(x0)),
                 'outgoing_amplitude_squared':float(abs(b)**2),'susceptibility_real':float(G.real),
                 'susceptibility_imag':float(G.imag)})
assert max(passivity,match,quad,form)<mp.mpf('1e-45')
limits=[]
for A in [1,10,1000]:
    b,G,_,_=response(A,mp.mpf('1e-8'))
    assert abs(b+1)<mp.mpf('1e-12') and abs(G+mp.mpf(6)/5)<mp.mpf('2e-8')
    limits.append({'A':A,'monopole_error':float(abs(b+1)),'static_susceptibility_error':float(abs(G+mp.mpf(6)/5))})
out={'cases':len(rows),'precision_digits':70,'max_passivity_error':str(passivity),
     'max_boundary_solve_error':str(match),'max_quadrature_error':str(quad),'max_A1_form_factor_error':str(form),
     'low_frequency_limits':limits,'rows':rows,
     'non_claim':'Fixed uniform spherical inertia and prescribed harmonic source; no nonlinear formation rate or parameter prediction.'}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
