"""Posthoc frame/fragment audit, exact angular cap integrals of finite density."""
import pathlib,json,hashlib,importlib.util,sys,numpy as np
from scipy.special import sph_harm,eval_legendre
from scipy.optimize import minimize
from angular_half import Angular
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];sf=ROOT/'sol61_push/cold_survey_capture_2026_10_24/survey.py';refs=sf.parent/'survey_results.json';prevfile=ROOT/'sol61_push/cold_data_constraints_2026_10_24/results.json';tags=['draco_escape','draco_escape_long','sextans_escape','sextans_escape_long'];files=[pathlib.Path(__file__),P/'angular_half.py',sf,refs,prevfile,sf.parent/'data/members.tsv',ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv']
for tag in tags:files.extend([P/'runs'/f'{tag}.json',P/'runs'/f'{tag}_fields.npz'])
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
before=hashes();sp=importlib.util.spec_from_file_location('survey',sf);s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s);data=s.load();previous=json.loads(prevfile.read_text())['galaxies'];ref=min(z['nll'] for z in json.loads(refs.read_text())['continuous_best'] if z['footing']=='canonical' and z['beta']==0 and z['tracer_taper_pc'] is None);rows=[]
for tag in tags:
 q=json.loads((P/'runs'/f'{tag}.json').read_text());par=q['parameters'];u=q['physical'];f=np.load(P/'runs'/f'{tag}_fields.npz');r=f['r'];w=f['w'];v=f['final'];ang=Angular(par['lmax'],par['mmax'],r,w);fa=ang.field.forward(v);pa,co,W=ang.potential(v);rho=abs(fa)**2/(w*r*r)[:,None,None];cr=ang.density.back(rho);shellcoeff=cr*(w*r*r)[:,None];ell=np.array([l for l,m in ang.density.lm]);ms=np.array([m for l,m in ang.density.lm]);mass=float(np.sum(abs(v)**2));R=u['Runit_pc'];M=u['Munit_Msun'];V=u['Vunit_kms']
 zcom=float(np.sum(r*ang.field.integral(abs(fa)**2*ang.field.mu[None,:,None]))/mass)
 i,j,k=np.unravel_index(np.argmin(pa),pa.shape);mu=ang.field.mu[j];phi=np.pi*k/ang.field.nphi;c0=r[i]*np.array([np.sqrt(1-mu*mu)*np.cos(phi),np.sqrt(1-mu*mu)*np.sin(phi),mu])
 def potential(c):
  d=np.linalg.norm(c)
  if d<r[0]:return float(co[0,0].real/np.sqrt(4*np.pi))
  ii=np.searchsorted(r,d)-1
  if ii>=len(r)-1:return -mass/d
  tt=(d-r[ii])/(r[ii+1]-r[ii]);coeff=(1-tt)*co[ii]+tt*co[ii+1];theta=np.arccos(np.clip(c[2]/d,-1,1));ph=np.arctan2(c[1],c[0]);Y=sph_harm(ms,ell,ph,theta);return float(np.real(coeff@Y))
 opt=minimize(potential,c0,method='Nelder-Mead',options={'maxiter':1000,'xatol':1e-7,'fatol':1e-12});c=opt.x;d=float(np.linalg.norm(c));theta=np.arccos(np.clip(c[2]/d,-1,1));phi=np.arctan2(c[1],c[0]);Yc=sph_harm(ms,ell,phi,theta)
 angular_l=np.array([np.real(np.sum(shellcoeff[:,ell==l]*Yc[ell==l],axis=1)) for l in range(2*par['lmax']+1)]).T
 def cap(a):
  if d<1e-8:return float(sum(np.sum(abs(v)**2,axis=1)[r<a]))
  z=np.clip((r*r+d*d-a*a)/(2*r*d),-1,1);ans=angular_l[:,0]*(1-z)
  for l in range(1,angular_l.shape[1]):ans+=angular_l[:,l]*(eval_legendre(l-1,z)-eval_legendre(l+1,z))/(2*l+1)
  return float(2*np.pi*sum(ans))
 aps=np.array([.5,1,2,3,5]);enc=np.array([cap(a) for a in aps])*M
 assert np.min(enc)>-1e-8*M and np.max(enc)<mass*M*(1+1e-10)
 # Independent spherical-shell limit of the angular cap formula.
 z=.3;fraction=2*np.pi*(1/np.sqrt(4*np.pi))*(1/np.sqrt(4*np.pi))*(1-z);assert abs(fraction-(1-z)/2)<1e-15
 # Smooth curve for a MONOPOLE diagnostic around the newly chosen well.
 ar=np.geomspace(1e-4,1.1*(par['rmax']+d),320);cm=np.maximum.accumulate(np.maximum([cap(a) for a in ar],0));assert cm[-1]<=mass*(1+1e-9)
 def gc(rad):return s.G*M*np.interp(rad/R,ar,cm,left=0,right=mass)/rad**2
 name=par['galaxy'];row={'tag':tag,'scope':'posthoc instantaneous cold-potential-well centre; not a moving-centre DF solution or new pass of original fixed-origin gates','COM_pc':[0,0,zcom*R],'potential_minimum_offset_pc':d*R,'potential_minimum_xyz_pc':(c*R).tolist(),'potential_minimizer_success':bool(opt.success),'potential_depth_below_original_origin_kms2':(potential(np.zeros(3))-potential(c))*V*V,'pi_symmetric_partner_xyz_pc':(-c[0]*R,-c[1]*R,c[2]*R),'apertures_pc':(aps*R).tolist(),'cold_mass_within_well_centred_apertures_Msun':enc.tolist(),'potential_minimum_code':potential(c)}
 if name=='Draco':
  xx,ww=np.polynomial.legendre.leggauss(128);tt=(xx+1)*np.pi/4;ww*=np.pi/4;rad=R*np.tan(tt);base=previous[name]['moments']['canonical'][0]['sigma_baryon']**2;row['well_centred_global_sigma_diagnostic_kms']=float(np.sqrt(base+R*np.sum(ww*np.sin(tt)**3*gc(rad))))
 else:
  def g(rad):
   gn=sum(s.G*250000*rad/(rad*rad+a*a)**1.5 for a in data['aa']);return .5*(gn+np.sqrt(gn*gn+4*s.A0['canonical']*gn))+gc(rad)
  var=np.array([s.projection(data['R'],a,g) for a in data['aa']]).T;fit=s.fit(data,var,np.zeros_like(var),fixed_mass=0.);row['well_centred_survey_twice_NLL_above_reference']=2*(fit['nll']-ref)
 rows.append(row);print(row,flush=True)
after=hashes();assert before==after;(P/'centering.json').write_text(json.dumps({'scope':'frame/fragment audit with exact finite spherical-harmonic angular-cap integrals and radial shell quadrature; original centre criteria preserved; no actual star heating claimed','inputs_before':before,'inputs_after':after,'results':rows},indent=2)+'\n')
