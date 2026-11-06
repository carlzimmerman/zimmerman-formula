import sympy as s
import json
r,A,P,g,M,a,K,B,E,u,v=s.symbols('r A P gamma M a K B E u v',nonzero=True)
wp,wpp=s.symbols('Wp Wpp')
Ca,Cbeta,CA,CP,Cm,CH=s.symbols('Ca Cbeta CA CP Cm CH')
ax,Kx=s.symbols('ax Kx')
D=(A*r-1-g*r*r)/g
Dr=s.diff(D,r)
H=r*r/2+(A*r-1-g*r*r)**2/(2*g)
h=s.diff(H,r);R=s.diff(H,r,2);c2=h/(r*R)
J=h+P*wp/r
S=-(r*r*Dr*u+wp*v+2*B*J)/R
F=-r*c2*K+S
V=F/r
Eu=wpp*v/r-wp*F/r**3+wp*K/r**2
Ev=Dr*F/r+r*u/g-2*E*v+K*(D-2*P*E)/r+2*P*B*(a+E)/r
nE=-a*B-B*E
actual={r:r*(a+Ca),A:wp/r+CA,P:D-2*P*E+CP,B:(K-B)*E+Cm,
        u:Eu,v:Ev,wp:wpp*(D-2*P*E+CP),a:ax,K:Kx}
zero={Ca:0,Cbeta:0,CA:0,CP:0,Cm:0,CH:0}
def ex(z):return sum(s.diff(z,x)*y for x,y in actual.items())
def exstar(z):return ex(z).subs(zero)
na=exstar(V)-(V+K)*a
nCa=ex(V)-(V+K)*(a+Ca)-na
VP=s.diff(V,P)+wpp*s.diff(V,wp)
expectedCa=(r*s.diff(V,r)-V-K)*Ca+s.diff(V,A)*CA+VP*CP+s.diff(V,B)*Cm
nCA=ex(r*u)-(a+Ca)*r*u-K*(wp/r+CA)-wpp*v+wp*F/r**2
nCP=ex(r*v)-(a+Ca)*r*v-K*(D-2*P*E+CP)-Dr*F-s.diff(D,A)*r*u+2*r*v*E+2*P*nE
nCbeta=(K-B)*E+Cm-(a+Ca)*B-K*(E+Cbeta)-nE
checks={
 'Ca_compact_formula':s.cancel(nCa-expectedCa)==0,
 'CA_transport':s.cancel(nCA+K*CA)==0,
 'CP_transport':s.cancel(nCP+K*CP)==0,
 'Cbeta_transport':s.expand(nCbeta-(Cm-B*Ca-K*Cbeta))==0,
 'no_independent_source':s.cancel(nCa.subs(zero))==0,
 'no_spatial_residual_derivatives':not expectedCa.has(ax,Kx),
}
out={'checks':checks,'all_pass':all(checks.values()),'V':str(s.factor(V)),
 'Ca_coefficients':{
   'Ca':str(s.factor(r*s.diff(V,r)-V-K)),
   'CA':str(s.factor(s.diff(V,A))),
   'CP':str(s.factor(VP)),
   'Cmom':str(s.factor(s.diff(V,B)))},
 'n_CA':str(s.cancel(nCA)), 'n_CP':str(s.cancel(nCP)),
 'n_Cbeta':str(s.expand(nCbeta))}
print(json.dumps(out,indent=2))
