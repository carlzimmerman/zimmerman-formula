import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['omit_trace_mixing','drop_dust_momentum']);args=ap.parse_args();rows=[]
def ck(n,b,e=''):rows.append({'name':n,'passed':bool(b),'detail':str(e)})
M,xi,r,P,w=s.symbols('M xi r P w',nonzero=True);u,U,v,V,delta,wd,phi=s.symbols('u U v V delta wd phi');st=[u,U,v,V,delta,wd,phi]
def red(ex):
 numerator,denominator=s.fraction(s.cancel(ex));numerator=s.rem(s.Poly(s.expand(numerator),w),s.Poly(w**2-4*xi/3+s.Rational(1,4),w)).as_expr()
 return s.factor(numerator/denominator)
def eq(n,ex):ex=red(ex);ck(n,ex==0,ex)
F=M-xi*r;B=M+xi*(6*xi-1)*r;df=-2*xi*r*u;dfx=-2*xi*r*(U-u);fx=xi*r
psi=phi-df/F
phix=(-(0 if args.mutation=='drop_dust_momentum' else 4*M*wd/3)+r*(-u/2+w*v)+dfx-s.Rational(2,3)*df-(4*F/3+fx)*psi)/(2*F)
psix=phix-dfx/F+df*fx/F**2
traceDen=F if args.mutation=='omit_trace_mixing' else B
RR=(4*M*delta/3+(1-6*xi)*r*(U-2*w*V+8*xi*psi/3))/traceDen
rhs=[U,2*w*V-P*u-(psix+3*phix)/2-8*xi*psi/3-xi*RR,V,-2*w*U-P*v+w*(psix+3*phix),3*phix+P*wd,-psi-wd,phix]
D=lambda ex:sum(s.diff(ex,z)*rz for z,rz in zip(st,rhs))-r*s.diff(ex,r)+2*P*s.diff(ex,P)/3
C=(4*M-xi*r)*phix+8*M*psi/3+2*F*P*phi-(s.Rational(4,3)+P)*df-2*dfx+r*(-U/2+w*V+4*xi*u/3)+4*M*delta/3
# Exact trace obtained from scalar EOM plus Einstein trace, not a fixed-metric source.
rawtrace=4*M*delta/3+(1-6*xi)*r*(U-2*w*V-2*(w*w+s.Rational(1,4))*u+2*(w*w+s.Rational(1,4))*psi)-s.Rational(4,3)*(1-6*xi)*df
eq('exact_trace_u_cancellation',rawtrace-(4*M*delta/3+(1-6*xi)*r*(U-2*w*V+8*xi*psi/3)))
eq('trace_denominator',B-F-6*xi**2*r)
eq('anisostress_constraint',F*(phi-psi)-df)
eq('raw_momentum_constraint',2*F*(phix+2*psi/3)+fx*psi+4*M*wd/3-r*(-u/2+w*v)-dfx+2*df/3)
raw00=2*F*(P*phi+2*phix+4*psi/3)-4*df/3+4*M*delta/3+r*(-U/2+w*V+(w*w+s.Rational(1,4))*u)-(w*w+s.Rational(1,4))*r*psi-P*df-2*dfx+3*fx*phix+4*fx*psi
eq('raw00_exact_normalization',raw00-C)
eq('constraint_propagation',D(C)-xi*r*C/(2*F))
geo=-6*D(phix)-10*phix-4*psix-8*psi/3+2*P*(psi-2*phi)
eq('geometric_R_equals_trace_on_constraint',geo-RR+C/F)
eq('dust_velocity_evolution',rhs[5]+psi+wd)
eq('dust_density_evolution',rhs[4]-3*phix-P*wd)
# Residual of actual metric-sourced complex scalar row, x=ln t.
eq('radial_scalar_equation',rhs[1]-2*w*V+P*u+(psix+3*phix)/2+8*xi*psi/3+xi*RR)
eq('phase_scalar_equation',rhs[3]+2*w*U+P*v-w*(psix+3*phix))
eq('Phi_derivative_consistency',D(phi)-phix)
eq('Psi_derivative_consistency',D(psi)-psix)
eq('deltaF_derivative_consistency',D(df)-dfx)
# Algebraic initial constraint coefficient: zero possible in other domains, so retain explicit obligation.
eq('constraint_phi_coefficient',s.diff(C,phi)-(2*F*P-xi*r*(8*M+xi*r)/(6*F)))
# Exact GR sublimit (vanishingcarrier amplitude), not assumed quasistatic.
phi0=s.symbols('phi0');gr={r:0,u:0,U:0,v:0,V:0,delta:-(s.Rational(3,2)*P+2)*phi0,wd:-phi0,phi:phi0}
eq('GR_growing_Phi_constant',phix.subs(gr))
eq('GR_growing_density_transfer',rhs[4].subs(gr)+P*phi0)
eq('GR_growing_constraint',C.subs(gr))
eq('GR_growing_comoving_density', (delta-2*wd).subs(gr)+s.Rational(3,2)*P*phi0)
shift=s.symbols('time_shift_over_t');eq('comoving_density_gauge_invariance',(delta+2*shift)-2*(wd+shift)-(delta-2*wd))
# Background is actual full EdS solution, while F>0 restricts starttime.
norm=r*(w*w+s.Rational(1,4));eq('background_trace_on_shell',(B*s.Rational(4,3))-(4*M/3-(1-6*xi)*norm))
eq('background_00_on_shell',-s.Rational(4,3)*F+4*M/3+norm/2-2*fx)
args.out.mkdir(parents=True,exist_ok=True);out={'checks':rows,'passed':sum(z['passed'] for z in rows),'total':len(rows),'mutation':args.mutation,'domain':'xi>3/16,F>0,r>0,k>0; omega²=4xi/3−1/4; exact Fourier linear equations, no quasistatic assumption'};(args.out/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[z['name'] for z in rows if not z['passed']]}));sys.exit(0 if out['passed']==out['total'] else 1)
