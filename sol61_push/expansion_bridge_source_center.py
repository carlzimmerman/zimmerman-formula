"""Conserved fluid stress and regular-center identities, not a source BVP."""
import argparse,json
from pathlib import Path
import sympy as s
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
r,N,sg,V,omega,psip,X=s.symbols('r N sigma V omega psip X',real=True)
E=s.exp(sg);F=N**2-E**2*V**2
Xm=((omega-V*psip)**2/N**2-psip**2/E**2)/2
psi0=-omega*E**2*V/F;X0=omega**2/(2*F)
pressure=s.Function('p');pp=pressure(X0);h=2*X0*s.diff(pressure(X),X).subs(X,X0)
Lm=r**2*N*E*pp
checks={
 'zero_radial_flux':s.diff(Xm,psip).subs(psip,psi0),
 'phase_X':Xm.subs(psip,psi0)-X0,
 'source_lapse':s.diff(Lm,N)/(r**2*E)-(pp-h*N**2/F),
 'source_shift':s.diff(Lm,V)/(r**2*N*E)-h*E**2*V/F,
 'source_radial_combination':(s.diff(Lm,sg)-V*s.diff(Lm,V))/(r**2*N*E)-pp,
}
R=s.symbols('R',positive=True)
M2,H,hc,lam,beta,xi,Nc,n1,s2,p1,v3,rho,pc,U=s.symbols('M2 H hc lambda beta xi Nc n1 s2 p1 v3 rho pc U',real=True)
S=3*lam-1
Nr=Nc*(1+n1*R**2/2);sig=s2*R**2;Vr=-Nc*hc*R+v3*R**3;Pr=p1*R
Fkin=s.diff(Vr,R)+Vr*s.diff(sig,R);W=Vr/R;trace=Fkin+2*W;theta=-trace/Nr
Q=Fkin**2+2*W**2-lam*trace**2
curv=2*(1-s.exp(-2*sig))/R**2+4*s.exp(-2*sig)*s.diff(sig,R)/R
metricF=Nr**2-s.exp(2*sig)*Vr**2
rad=-Q/(2*Nr**2)+(1-s.exp(-2*sig))/R**2-2*s.exp(-2*sig)*s.diff(Nr,R)/(Nr*R)-xi*Pr**2-U/M2-2*beta*Pr**3/theta+pc/M2
lapse=-Q/(2*Nr**2)+curv/2-2*s.exp(-sig)*(s.diff(Pr,R)+2*Pr/R)-xi*Pr**2-U/M2-2*beta*Pr**3/theta+(pc-(rho+pc)*Nr**2/metricF)/M2
pol=s.exp(-sig)*s.diff(Nr,R)/Nr-xi*Pr-3*beta*Pr**2/(2*theta)
rad0=s.Rational(3,2)*S*hc**2+2*s2-2*n1-U/M2+pc/M2
lap0=s.Rational(3,2)*S*hc**2+6*s2-6*p1-U/M2-rho/M2
checks.update({
 'center_radial_equation':s.limit(rad,R,0)-rad0,
 'center_lapse_equation':s.limit(lapse,R,0)-lap0,
 'center_polarization':s.limit(pol/R,R,0)-(n1-xi*p1),
})
center_s2=(3-xi)*p1/2+(rho+pc)/(4*M2)
center_relation=s.Rational(3,2)*M2*S*hc**2+3*M2*(1-xi)*p1+(rho+3*pc)/2-U
checks.update({
 'center_relation_from_radial':M2*rad0.subs({n1:xi*p1,s2:center_s2},simultaneous=True)-center_relation,
 'center_relation_from_lapse':M2*lap0.subs({n1:xi*p1,s2:center_s2},simultaneous=True)-center_relation,
 'critical_center_bound':center_relation.subs(xi,1)-(s.Rational(3,2)*M2*S*hc**2+(rho+3*pc)/2-U),
 'critical_vacuum_dictionary':s.solve(center_relation.subs({xi:1,U:s.Rational(3,2)*M2*S*H**2}),hc**2)[0]-(H**2-(rho+3*pc)/(3*M2*S)),
})
g,b,P,C=s.symbols('g b P C',real=True)
Lweak=-M2*g**2+2*M2*P*g-xi*M2*P**2-C*P**3
checks.update({
 'detuned_polarization':s.diff(Lweak,P)-2*M2*(g-xi*P-3*C*P**2/(2*M2)),
 'detuned_flux':s.diff(Lweak,g)+2*M2*(g-P),
 'infrared_Newton_ratio':s.limit((xi*P+3*C*P**2/(2*M2))/((xi-1)*P+3*C*P**2/(2*M2)),P,0)-xi/(xi-1),
})
results={key:s.simplify(value)==0 for key,value in checks.items()};assert all(results.values()),results
out={'passed':len(results),'checks':results,
 'scope':'Exact local fluid-envelope, center-limit and detuned reduced-action identities. Center theorem assumes M2>0, lambda>1, finite nonzero central Theta and regular finite-curvature metric. No source BVP, observed-density calibration, full health or 32pi selection.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
