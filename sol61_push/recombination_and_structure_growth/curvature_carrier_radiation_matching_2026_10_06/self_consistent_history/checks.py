import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['omit_trace_kinetic','use_canonical_rho']);args=ap.parse_args();rows=[]
def ck(n,b,e=''):rows.append({'name':n,'passed':bool(b),'detail':str(e)})
def eq(n,e):e=s.factor(s.cancel(e));ck(n,e==0,e)
M,xi,f,D,E,H,rd,rr,R=s.symbols('M xi f D E H rd rr R');F=M-2*xi*f;fd=-4*xi*D;B=F+12*xi**2*f
Rsol=(rd+(0 if args.mutation=='omit_trace_kinetic' else 2*(6*xi-1)*E))/B
Hd=R/6-2*H**2;dot={f:2*D,D:E-3*H*D-xi*R*f,E:-6*H*E-2*xi*R*D,H:Hd,rd:-3*H*rd,rr:-4*H*rr}
der=lambda v:sum(s.diff(v,k)*dv for k,dv in dot.items())
C=3*F*H**2+3*fd*H-rd-rr-E
closure=H*(B*R-rd-2*(6*xi-1)*E)-4*H*C
eq('raw_constraint_derivative_identity',der(C)-closure)
eq('on_shell_constraint_propagation',(der(C)+4*H*C).subs(R,Rsol))
eq('Fdot_from_field_invariant',der(F)-fd)
fdd=der(fd)
eq('Fddot_from_field_EL',fdd+4*xi*(E-3*H*D-xi*R*f))
eq('trace_denominator_real_normalization',B-M-2*xi*(6*xi-1)*f)
eq('Einstein_radial_kinetic_coefficient',M/F+3*M*(8*xi*xi*f)/(2*F*F)-M*B/F**2)
# Friedmann expandingroot; useindependentdiscriminantsymbol.
G=s.symbols('G',positive=True);tot=rd+rr+E
root=(-fd+G)/(2*F)
eq('positive_H_friedmann_root',(3*F*root**2+3*fd*root-tot)-(3*(G**2-fd**2)-4*F*tot)/(4*F))
eq('implicit_H_derivative_coefficient',s.diff(C,H)-3*(2*F*H+fd))
eq('root_derivative_nondegeneracy',2*F*root+fd-G)
rational=2*tot/(3*(G+fd));eq('rationalized_root',(root-rational)-(3*(G**2-fd**2)-4*F*tot)/(6*F*(G+fd)))
# Direct metricvariation scalarstress, notcanonicalenergy.
rho=E+6*xi*H**2*f+12*xi*H*D
pressure=E+2*xi*(-(2*Hd+3*H**2)*f-der(2*D)-2*H*(2*D))
rho_used=E if args.mutation=='use_canonical_rho' else rho
pcompact=(1-4*xi)*E+4*xi*H*D+2*xi*f*((2*xi-s.Rational(1,3))*R+H**2)
eq('full_pressure_raw_variation',pressure-pcompact)
eq('full_carrier_rho_metric_constraint',rho_used-(3*M*H**2-rd-rr)+C)
peq=-M*(2*Hd+3*H**2)-rr/3
eq('full_carrier_pressure_metric_constraint',(pressure-peq+C/3).subs(R,Rsol))
eq('carrier_conservation',der(rho)+3*H*(rho+pressure))
eq('total_density_conservation',der(rd+rr+rho)+3*H*(rd+rr+rho+rr/3+pressure))
# Complexcomponents independentcharge andinvariantclosure.
x,y,p,q,a=s.symbols('x y p q a');vel={x:p,y:q,p:-3*H*p-xi*R*x,q:-3*H*q-xi*R*y,a:a*H};dt=lambda ex:sum(s.diff(ex,j)*dj for j,dj in vel.items())
ff=x*x+y*y;DD=x*p+y*q;EE=p*p+q*q;L=x*q-y*p
eq('raw_f_dot',dt(ff)-2*DD)
eq('raw_D_dot',dt(DD)-(EE-3*H*DD-xi*R*ff))
eq('raw_E_dot',dt(EE)+6*H*EE+2*xi*R*DD)
eq('angular_momentum_identity',ff*EE-DD*DD-L*L)
eq('U1_charge_conservation',dt(a**3*L))
# Actualspecifiedlate data; radiationaltersH butnotRtraceatthisinstant.
fe,omega=s.symbols('fe omega');Es=4*xi*fe/3;Ds=-fe/2
initial={M:1,f:fe,D:Ds,E:Es,rd:s.Rational(4,3)}
eq('initial_trace_R_independent_radiation',Rsol.subs(initial)-s.Rational(4,3))
# fullscalartrace hasMR-rd onceconstraintzero; actualinitialR=rd/M⇒radiationtypecarrierpressure.
eq('initial_carrier_trace_on_constraint',(-rho+3*pressure).subs(R,Rsol).subs(initial))
args.out.mkdir(parents=True,exist_ok=True);out={'checks':rows,'passed':sum(z['passed'] for z in rows),'total':len(rows),'mutation':args.mutation,'scope':'actualhomogeneousFRW action, xi>3/16,F>0,positiveH branch; no perturbativehealth or32piselector'};(args.out/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[z['name'] for z in rows if not z['passed']]}));sys.exit(0 if out['passed']==out['total'] else 1)
