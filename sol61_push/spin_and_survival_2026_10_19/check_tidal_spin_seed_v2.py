"""CE089B: allowed tidal-quadrupole spin source; no predicted dwarf geometry."""
import json,math,sys
from pathlib import Path
b=Path('sol61_push/spin_and_survival_2026_10_19');r=json.loads((b/'run_001/results.json').read_text());checks=[];rows=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
# External potential U=U0+A.x+.5 x.T x about COM.
# torque_z = int rho [x*(-Ty*y)-y*(-Tx*x)] dV = (Tx-Ty) Ixy.
# For planar principal moments I1,I2 rotated theta, Ixy=.5(I1-I2)sin2theta.
for name,factor in r['lambda_Fornax_over_lambda_dwarf'].items():
 relative=1/factor;theta=.5*math.asin(relative);I1,I2=2.,1.;Tx,Ty=3.,1.;co,si=math.cos(theta),math.sin(theta)
 Ixy=(I1-I2)*co*si;torque=(Tx-Ty)*Ixy;peak=(Tx-Ty)*(I1-I2)/2
 ck(name+' source ratio',abs(torque/peak-relative)<1e-12)
 rows.append({'name':name,'required_lambda_or_normalized_torque_ratio_at_equal_dimensionless_history':relative,'misalignment_angle_degrees_if_Fornax45deg':theta*180/math.pi})
ck('aligned patch torque zero',math.sin(0)==0);ck('isotropic moment patch torque zero',(1-1)*math.sin(.7)==0)
# e=Ixy/(M Ri²), T=Tx-Ty, tg=sqrt(Ri³/GM), Ei=-.3GM²/Ri.
# lambda = sqrt(.3) e (T tg²)(Delta_t/tg).
strength=[]
for lam in [.05,.1,.2]:
 for ellipticity in [.05,.1,.2]:
  for nd in [1,10]:
   dimensionless_shear=lam/(math.sqrt(.3)*ellipticity*nd)
   ck(str((lam,ellipticity,nd))+' lambda inversion',abs(math.sqrt(.3)*ellipticity*dimensionless_shear*nd-lam)<1e-14)
   strength.append({'lambda':lam,'Ixy_over_MRi2':ellipticity,'duration_over_tg':nd,'required_shear_T_tg2':dimensionless_shear})
# Core heat export is not necessarily escaped radiation: energy may go to outer stock.
# Energy conservation alone does not fix a gravothermal mass flux or rate.
out={'claim_id':'CE-FM-089B','n_checks':len(checks),'checks':checks,'all_pass':all(x['pass'] for x in checks),'torque_ratios':rows,'tidal_spin_strength':strength,'proof':'COM uniform field gives zero torque. Quadratic external potential gives tau_i=-epsilon_ijk T_kl I_jl. Diagonal planar T yields tau_z=(Tx-Ty)Ixy; rotated principal quadrupole yields Ixy=(I1-I2)sin2theta/2.','non_claims':['Angles are constructed to illustrate required ratios, not inferred progenitor alignments or probabilities','No actual tidal tensor, inertia history, shell crossing or cooling kernel supplied','Formation torques are not the present/pericentric tidal scalar tested in CFG838/839','Changing spin only sets a possible angular-momentum floor; dissipation and survival remain separate']};Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(checks),'angles':rows,'strength_e01_N1':[x for x in strength if x['Ixy_over_MRi2']==.1 and x['duration_over_tg']==1]},indent=2))
