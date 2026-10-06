import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['none','omit_shift','opposite_time','integrated_only'],default='none');args=ap.parse_args();rows=[]
def eq(n,x):x=s.factor(s.simplify(x));rows.append(dict(name=n,passed=x==0,residual=str(x)))
def ck(n,x):rows.append(dict(name=n,passed=bool(x)))
N,gx,gy,gz=s.symbols('N gx gy gz',positive=True);S,eps=s.symbols('S eps',real=True);pt,px,py,pz=s.symbols('pt px py pz',real=True)
inv=s.Matrix([[-1/N**2,S/N**2,0,0],[S/N**2,1/gx-S*S/N**2,0,0],[0,0,1/gy,0],[0,0,0,1/gz]])
th=s.Matrix([1+eps*pt,eps*px,eps*py,eps*pz]);X=-(th.T*inv*th)[0];Nc=1/s.sqrt(X)
uc=-Nc*th;uv=inv*uc
basec=uc.subs(eps,0);basev=uv.subs(eps,0);dc=s.diff(uc,eps).subs(eps,0);dv=s.diff(uv,eps).subs(eps,0)
eq('exact_normalization',(basec.T*basev)[0]+1)
eq('normalized_lapse_clockvariation',s.diff(s.log(Nc),eps).subs(eps,0)+pt-S*px)
for i,candidate in enumerate([0,-N*px/gx,-N*py/gy,-N*pz/gz]):eq('contravariant_normal_variation_'+str(i),dv[i]-candidate)
Pm=s.eye(4)+basec*basev.T;dPm=dc*basev.T+basec*dv.T;Pup=inv+basev*basev.T;dPup=dv*basev.T+basev*dv.T
for i,pp in [(1,px),(2,py),(3,pz)]:
 eq('mixed_projector_time_'+str(i),dPm[i,0]+pp)
 eq('mixed_projector_shift_'+str(i),dPm[i,1]-S*pp)
for j in range(4):eq('actual_unitary_projector_time_'+str(j),Pup[0,j])
for i in range(1,4):
 for j in range(i,4):eq('coincident_spatial_projector_variation_'+str(i)+str(j),dPup[i,j].subs(S,0))
lt,lx,ly,lz,pxt,Sx,pxx=s.symbols('lt lx ly lz pxt Sx pxx',real=True)
dax=sum(dPm[1,j]*n for j,n in enumerate([lt,lx,ly,lz]))-pxt+Sx*px+S*pxx
eq('exact_spatial_acceleration_clockvariation',dax-(-pxt+Sx*px+S*pxx-(lt-S*lx)*px))
# Pure relativeamplitude expansion aboutbackgroundN1,S0.
nu,nd,rrshift,rrshift_x=s.symbols('nu nd rrshift rrshift_x',real=True)
pureg=dax.subs({lt:eps*nd/2,lx:0,ly:0,lz:0,S:eps*rrshift/2,Sx:eps*rrshift_x/2})
pureh=dax.subs({lt:-eps*nd/2,lx:0,ly:0,lz:0,S:-eps*rrshift/2,Sx:-eps*rrshift_x/2})
relative=s.diff(pureg-pureh,eps).subs(eps,0)
eq('relative_acceleration_order1',relative-rrshift_x*px-rrshift*pxx+nd*px)
nux=s.symbols('nux',real=True)
eq('pure_relative_temporal_acceleration_difference',(eps*rrshift/2)*(eps*nux/2)-(-eps*rrshift/2)*(-eps*nux/2))

# Clockvariationfromcovariantm0=.5; temporal/projectortermsverifiedabove.
K,a,k,H,t,amp=s.symbols('K a k H t amp',positive=True);x=s.symbols('x',real=True);beta=s.symbols('beta',real=True);P=k*k/a**2
nuf=nu*s.cos(k*x);shift=-k*beta*s.sin(k*x)/a**2;ndf=nd*s.cos(k*x)
flux=s.diff(nuf,x,2)*shift+ndf*s.diff(nuf,x)
E=2*K*a*s.diff(flux,x)
expected=2*K*a*k*k*nu*(P*beta-nd)*s.cos(2*k*x)
eq('raw_clock_Euler_second_harmonic',s.expand_trig(E-expected))
mode={beta:2*H*nu/P,nd:-H*nu}
actual=s.simplify(expected.subs(mode))
eq('actual_decay_clock_residual',actual-6*K*a*H*k*k*nu*nu*s.cos(2*k*x))
ck('nonzero_local_clock_residual',actual.subs({x:0,nu:amp})>0)
eq('integrated_clock_row_zero',s.integrate(actual,(x,0,2*s.pi/k)))
eq('late_mode_residual_a_minus1',actual.subs({a:s.exp(H*t),nu:-amp*s.exp(-H*t)})-6*K*H*k*k*amp*amp*s.exp(-H*t)*s.cos(2*k*x))
# Independent two-direction same-eigenvalue witness of compact eigenshell theorem.
ycoord=s.symbols('ycoord',real=True);field=nu*(s.cos(k*x)+s.cos(k*ycoord));coords=[x,ycoord]
lap=lambda f:sum(s.diff(f,j,2) for j in coords)
vec=[lap(field)*(2*H*s.diff(field,j)/k**2)-H*field*s.diff(field,j) for j in coords]
Eg=2*K*a*sum(s.diff(v,j) for v,j in zip(vec,coords))
eq('same_eigenshell_clock_identity',Eg+3*K*a*H*lap(field*field))
ck('same_eigenshell_superposition_not_a_cure',s.simplify(Eg.subs({x:0,ycoord:0,nu:amp}))>0)
# Frozenmodeandinstanttunedmixture are distinct fromadmissiononopen timeinterval.
eq('frozen_mode_has_no_this_residual',expected.subs({nu:0,nd:0}))
Z0,B=s.symbols('Z0 B',real=True);general=expected.subs({beta:2*H*nu/P-P*Z0/(H*P),nd:-H*nu})
# β=2Hν/P−Z0/H; afterconstantνcoeff division cannot vanish identicallyin a forBnonzero.
poly=s.expand((general.subs(nu,-B/a)/(2*K*a*k*k*s.cos(2*k*x)))*a**3*H)
eq('general_mode_two_distinct_time_powers',poly-(3*H*H*B*B*a+k*k*B*Z0))
# True operatorcontrols omit/flip pieces or discardall nonzero Fourierclockrows.
candidate=expected
if args.control=='omit_shift':candidate=2*K*a*k*k*nu*(-nd)*s.cos(2*k*x)
if args.control=='opposite_time':candidate=2*K*a*k*k*nu*(P*beta+nd)*s.cos(2*k*x)
if args.control=='integrated_only':candidate=s.integrate(expected,(x,0,2*s.pi/k))*k/(2*s.pi)
eq('candidate_retains_full_local_clock_row',candidate-expected)
out={'passed':sum(r['passed'] for r in rows),'total':len(rows),'checks':rows,'control':args.control,'scope':'n3coincidentdeS,purerelativeplane finitek, exactclocknormalization plussecondorderlocalEuler; noallmodeclaim'}
p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2));print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[r for r in rows if not r['passed']]}));sys.exit(out['passed']!=out['total'])
