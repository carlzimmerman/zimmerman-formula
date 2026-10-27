"""CE-FM-064: correlated residual audit and exact external-shell response bound."""
import sys,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import ellipk
D=Path('real_research/data/lensing_rar/brouwer2021_rar');raw=[np.loadtxt(D/f'Fig-3_Lensing-rotation-curves_Massbin-{j}.txt') for j in range(1,5)]
R=np.array([r[:,0] for r in raw]);Y=np.concatenate([r[:,1]/r[:,4] for r in raw]);c=np.loadtxt(D/'Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt');keys=sorted(set(c[:,0]));C=np.zeros((60,60))
for z in c:
 i=keys.index(z[0])*15+int(np.argmin(abs(R[0]-z[2])));j=keys.index(z[1])*15+int(np.argmin(abs(R[0]-z[3])));C[i,j]=z[4]/z[6]
checks=[]
def ck(name,x):
 checks.append({'name':name,'pass':bool(x)})
 if not x:raise AssertionError(name)
def esd(x):
 sig=ellipk(1/(1+4*x*x))/(math.pi*math.sqrt(1+4*x*x));m=(math.sqrt(1+4*x*x)-1)/2
 mc=m+quad(lambda r:2*r/math.sqrt(1+4*r*r)*(x/r)**2/(1+math.sqrt(max(0,1-(x/r)**2))),x,np.inf,epsabs=1e-11)[0]
 return (1+mc)/(math.pi*x*x)-sig
L=[10.36,10.83,11.01,11.18];pred=[]
for b,lm in enumerate(L):
 M=10**lm;rM=math.sqrt(4.30091e-3*M/(9.3603e-11*3.0857e16/1e6));pred.extend([M/rM**2*esd(rr*1e6/rM) for rr in R[b]])
r=Y-pred;full=float(r@np.linalg.solve(C,r));ck('new diagnostic total reproduced',abs(full-163.1)<.15)
blocks=[]
for b,expected in enumerate([17.9,43.2,45.9,60.6]):
 sel=np.arange(15*b,15*b+15);oth=np.setdiff1d(np.arange(60),sel);bb=C[np.ix_(sel,sel)];bo=C[np.ix_(sel,oth)];oo=C[np.ix_(oth,oth)]
 block=float(r[sel]@np.linalg.solve(bb,r[sel]));ck('marginal block diagnostic bin'+str(b+1),abs(block-expected)<.15)
 q=r[sel]-bo@np.linalg.solve(oo,r[oth]);S=bb-bo@np.linalg.solve(oo,bo.T);cond=float(q@np.linalg.solve(S,q));rest=float(r[oth]@np.linalg.solve(oo,r[oth]))
 ck('Schur conditional score identity bin'+str(b+1),abs(full-rest-cond)<1e-9)
 pulls=r[sel]/np.sqrt(bb.diagonal());blocks.append({'bin':b+1,'marginal_block_chi2':block,'conditional_increment_over_other_bins':cond,'rest_marginal_chi2':rest,'diagonal_pulls':pulls.tolist(),'inner_residual_Msun_pc2':float(r[15*b]),'inner_diagonal_sigma_Msun_pc2':float(np.sqrt(bb[0,0]))})
# Thin spherical shell of unit mass at a, surface projection including both hemispheres.
# For R<a, y=sqrt(1-(R/a)^2), K=-(1-y)^2/(2piR^2 y).
# Use stable 1-y=(R/a)^2/(1+y).
def K(R,a):
 if R>=a:return 1/(math.pi*R*R)
 y=math.sqrt(1-(R/a)**2);one=(R/a)**2/(1+y)
 return -one*one/(2*math.pi*R*R*y)
for q in [.001,.01,.1,.5,.9]:
 a=1.;rr=q;y=math.sqrt(1-q*q);sigma=1/(2*math.pi*a*a*y);cyl=q*q/(1+y)
 ck('shell projection algebra '+str(q),abs(K(rr,a)-(cyl/(math.pi*rr*rr)-sigma))<1e-12)
 ck('negative interior response '+str(q),K(rr,a)<0)
 ck('kernel weakens farther out '+str(q),abs(K(rr,1.1*a))<abs(K(rr,a)))
ck('shell exterior point mass',K(2,1)==1/(4*math.pi))
ck('small-R asymptotic',abs(K(.0001,1)/(-.0001**2/(8*math.pi))-1)<2e-8)
s=5.364;fb=1/(1+s);h=.6736
f=lambda q:.1+.45*np.clip(q-12.5,0,1)+.30*np.clip(q-13.5,0,7/6)
rows=[]
for b,lm in enumerate(L):
 q=brentq(lambda q:10**(q-lm)*fb*f(q+math.log10(h))-1,lm,lm+3);N=1/float(f(q+math.log10(h)));total=(1+s)*N*10**lm
 for amin in [.1,.164,.2,.3]:
  rr=R[b,0]*1e6;aa=amin*1e6;kernel=K(rr,aa);deficit=-r[15*b];need=deficit/(-kernel)
  rows.append({'bin':b+1,'fixed_logMb':lm,'inner_R_Mpc':float(R[b,0]),'minimum_outer_radius_Mpc':amin,'negative_ESD_per_unit_shell_mass_pc_minus2':kernel,'nominal_deficit_Msun_pc2':float(deficit),'minimum_added_mass_Msun':float(need),'translated_N':N,'entire_catchment_mass_Msun':total,'maximum_inner_reduction_if_entire_catchment_added_Msun_pc2':-kernel*total,'minimum_mass_over_entire_catchment':need/total})
  ck('positive deficit bound bin'+str(b+1)+'r'+str(amin),need>total)
# Deterministic shell mixtures obey envelope; no galaxy fit or morphology assignment.
rr=.035;amin=.2;radii=np.array([.2,.3,.5,.8]);masses=np.array([.2,.1,.3,.4]);response=sum(m*K(rr,a) for m,a in zip(masses,radii))
ck('nonnegative shell mixture envelope',response>=K(rr,amin)*sum(masses))
# A projected positive nonincreasing Sigma has DeltaSigma>=0, so cannot subtract
# a fixed baseline inner excess. A cavity/shell is allowed to go negative and
# is explicitly included above rather than assumed away.
result={'claim_id':'CE-FM-064','n_checks':len(checks),'all_pass':all(z['pass'] for z in checks),'checks':checks,'total_chi2_at_fixed_source_diagnostic_masses':full,'blocks':blocks,'shell_budget_diagnostics':rows,'scope':'Self-review. Spherical additive positive external mass, fixed original no-edge diagnostic baseline and masses, stated empirical catchment stock. Pointwise nominal residuals, not joint confidence bounds. No hot-gas live run, new galaxy fit, metric derivation or morphology identification.'}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':len(checks),'all_pass':result['all_pass'],'chi2':full,'Rmin0p2':[z for z in rows if z['minimum_outer_radius_Mpc']==.2]}))
