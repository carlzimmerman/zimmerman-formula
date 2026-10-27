"""Exact checks of one proposed coefficient change; no new physical solver."""
from fractions import Fraction as F
from pathlib import Path
import json,sys,math,resource
checks=[];rows=[]
def ck(n,v):
 assert v,n
 checks.append({'name':n,'pass':True})
for eta in [F(1,1000),F(1,100),F(1,10),F(1,2),F(1)]:
 q=eta/(1+eta);f=lambda u:u*u/(1-u)
 ck('zero-source nonzero root '+str(eta),f(q)-eta*q==0)
 slope=(2*q-q*q)/(1-q)**2-eta
 ck('new-branch slope '+str(eta),slope==eta*(1+eta))
 ck('restoring quadratic retune cancels '+str(eta),(1-eta)/2+eta/2==F(1,2))
 rows.append({'eta':str(eta),'u0_over_a0':str(q),'restoring_slope_zero':str(-eta),'restoring_slope_new_root':str(slope)})
# Nonrelativistic local elastic collision illustration, rational orthogonal rotation.
v1=(F(1),F(2),F(3));v2=(F(-3),F(4),F(-1));V=tuple((a+b)/2 for a,b in zip(v1,v2));w=tuple(a-b for a,b in zip(v1,v2));rw=(-w[1],w[0],w[2]);p1=tuple(a+b/2 for a,b in zip(V,rw));p2=tuple(a-b/2 for a,b in zip(V,rw))
ck('local elastic pair conserves momentum',tuple(a+b for a,b in zip(v1,v2))==tuple(a+b for a,b in zip(p1,p2)))
ck('local elastic pair conserves kinetic energy',sum(x*x for x in v1+v2)==sum(x*x for x in p1+p2))
# Clock is a scattering-event estimate, not a measured transport/collapse rate.
MSUN=1.989e33;PC=3.0857e18;GYR=365.25*86400*1e9;rho=.1*MSUN/PC**3;v=1e6;S=1.;time=1/(rho*S*v)/GYR
ck('fiducial collision clock Gyr range',4<time<5)
result={'format':'v2 result payload for exact coefficient checks and illustrative kinetics','checks':checks,'n_checks':len(checks),'coefficient_rows':rows,'scattering_event_clock_Gyr_at_rho_0p1_Msun_pc3_v10kms_S1cm2g':time,'scope':'Coefficient-only modification of fixed rational restoring law; homogeneous zero-source algebra not finite-object stability. Elastic pair conservation is not capture, condensation or E/J transport. Scattering cross section is assumed, not derived; no galaxy fit.','peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':len(checks),'illustrative_event_clock_Gyr':time}))
