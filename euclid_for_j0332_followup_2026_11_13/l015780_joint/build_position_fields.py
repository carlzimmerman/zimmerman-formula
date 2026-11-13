"""Direct oblate AQUAL deflections for L015780's four supplied images.

Output is unreduced physical deflection in arcseconds: source-distance
geometry is a separate scalar beta. No source redshift is asserted.
"""
import argparse,json,sys,time
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'euclid_for_j0332_fit_2026_11_13'))
from aqual_lensing import make_field,projected_deflection,geometry
I=ROOT/'euclid_for_j0332_followup_2026_11_13/l015780_inputs'
ZL=.42827037396


def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 raw=json.loads((I/'results/coolest_sersic.json').read_text())
 p=raw['lensing_entities'][0]['light_model'][0]['parameters'];v=lambda k:p[k]['point_estimate']['value']
 re,n,q,cx,cy=v('theta_eff'),v('n'),v('q'),v('center_x'),v('center_y')
 phi=np.pi/2+np.deg2rad(v('phi'));co,si=np.cos(phi),np.sin(phi)
 xy=np.array(json.loads((I/'dataset/positions.json').read_text())['arguments']['values']['array'])
 X,N=xy[:,1],-xy[:,0];u=co*(X-cx)+si*(N-cy);vv=-si*(X-cx)+co*(N-cy)
 scale,ratio=geometry(ZL,3.);rem=re/np.sqrt(q)*scale
 masses=np.arange(11.7,12.550001,.025);incs=np.array([90.,60.,50.]);allmaps=[];records=[]
 def solve(m,inc,nr=320,nt=64,nlos=256,outer=500.):
  qi=np.sqrt((q*q-np.cos(np.deg2rad(inc))**2)/np.sin(np.deg2rad(inc))**2)
  f=make_field(10**m,rem,n,qi,nr=nr,nt=nt,rmax_re=outer)
  au,av=projected_deflection(f,u,vv,inclination=inc,zl=ZL,zs=3.,nlos=nlos)
  alpha=np.stack([co*au-si*av,si*au+co*av])/ratio
  rec=dict(logmass=float(m),inclination=float(inc),qi=float(qi),nr=nr,nt=nt,nlos=nlos,
           outer_Re=outer,residual=f['residual'],iterations=f['iterations'],
           deposited_mass_ratio=f['deposited_mass']/10**m)
  assert abs(rec['deposited_mass_ratio']-1)<.003
  return alpha,rec,f
 for inc in incs:
  maps=[]
  for m in masses:
   t=time.monotonic();alpha,rec,_=solve(m,inc);rec['seconds']=time.monotonic()-t
   maps.append(alpha);records.append(rec);print(json.dumps(rec),flush=True)
  allmaps.append(maps)
  np.savez_compressed(out/'progress.npz',logmass=masses,inclination=incs[:len(allmaps)],alpha_hat_sky=np.array(allmaps),theta_sky=np.stack([X,N]))
 # Separate mesh/LOS/outer-domain checks at both sides of the anticipated
 # capacity transition and at the thinnest tested deprojection.
 checks=[]
 for m,inc in [(11.95,90.),(12.2,90.),(12.2,50.)]:
  a,_,f=solve(m,inc)
  for label,nr,nt,nlos,outer in [('mesh',640,128,256,500.),('LOS',320,64,512,500.),('outer',340,64,256,1000.)]:
   if label=='LOS':
    au,av=projected_deflection(f,u,vv,inclination=inc,zl=ZL,zs=3.,nlos=nlos);aa=np.stack([co*au-si*av,si*au+co*av])/ratio
   else:aa,_,_=solve(m,inc,nr,nt,nlos,outer)
   err=float(np.max(np.linalg.norm(aa-a,axis=0)/np.linalg.norm(aa,axis=0)))
   checks.append(dict(logmass=m,inclination=inc,change=label,max_vector_relative_error=err))
   assert err<.005,(checks[-1])
 # A changed reference source redshift must disappear on dividing by beta.
 au,av=projected_deflection(f,u,vv,inclination=inc,zl=ZL,zs=1.5,nlos=256)
 alt=np.stack([co*au-si*av,si*au+co*av])/geometry(ZL,1.5)[1]
 invariance=float(np.max(abs(alt-a)));assert invariance<1e-12
 np.savez_compressed(out/'positions_deflections.npz',logmass=masses,inclination=incs,
                     alpha_hat_sky=np.array(allmaps),theta_sky=np.stack([X,N]),
                     zl=ZL,re_geom_arcsec=re,n=n,q_projected=q,center=np.array([cx,cy]),
                     phi_west_to_north=phi,a0_SI=9.3603e-11)
 result=dict(assertion_tested='Unreduced oblate AQUAL deflections at supplied L015780 image positions over finite mass/inclination grid',
             shape=dict(re_geom_arcsec=re,re_major_kpc=rem,n=n,q_projected=q,center_west_north=[cx,cy],phi_west_to_north=phi),
             zl=ZL,reference_zs=3.,reference_beta=ratio,reference_source_invariance_absolute=invariance,
             grid=dict(logmass=masses.tolist(),inclination=incs.tolist()),records=records,refinement_checks=checks,
             non_claims=['No image likelihood or stellar dynamics fit in this run','No source-redshift measurement','No aperture mass comparison until separate audit',
                        'Smooth isolated unscreened AQUAL, equal lensing/temporal potentials, fixed light shape and constant M/L',
                        'Finite refinement checks are not universal PDE error bounds','No environmental external field or full screened-action solve'])
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'refinement_checks':checks,'reference_source_invariance_absolute':invariance}),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
