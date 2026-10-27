import sys,json,pathlib,itertools,math
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'rebuild_2026_10_22/X5_mw_joint_baryons'))
import x5_lib as X
ns=X.load_p4();S=ns['S'];fam=X.Family(ns)
points=np.array([(r,z) for r in (7.,9.,11.,13.,15.,17.,8.,10.,12.,14.,16.) for z in (.5,1.1,2.)])
profiles=np.array([(8.122,z) for z in (.3,.5,1.1,2.,3.)])
def density(sig,rd,mb):
 # Local stellar + gas column is sig, using the old gas radial profiles but new vertical profile.
 old,_=fam.rho(sig,mb,rd)
 def f(R,z):
  zz=np.abs(z);Rs=np.maximum(R,1e-6)
  # Subtract exactly the old gas, replace its vertical profile and normalize its local column to 11.
  og=(ns['S0_HI']*np.exp(-4/Rs-Rs/7)/(4*.085))/np.cosh(np.minimum(zz/(2*.085),300))**2+(ns['S0_H2']*np.exp(-12/Rs-Rs/1.5)/(4*.045))/np.cosh(np.minimum(zz/(2*.045),300))**2
  surf=ns['S0_HI']*np.exp(-4/Rs-Rs/7)+ns['S0_H2']*np.exp(-12/Rs-Rs/1.5)
  # Family's stellar normalization must be shifted to keep desired star column sig-11.
  stars,_=fam.rho(sig+(fam.sig_gas_R0/1e6-11),mb,rd)
  return stars(R,z)-og+surf*(11/(fam.sig_gas_R0/1e6))*np.exp(-zz/.2)/.4
 return f

def solve(rhof,foot,fine=False):
 a0=X.A0_SI[foot];mu=S.mass_unit(a0)
 g=ns['mw_grid'](6.6e10/mu) if not fine else S.Grid(S.log_edges(.005,18000,45),S.theta_edges(72,full=False,stretch_min=.002))
 rho=g.rho_axisym(lambda R,z:rhof(R,z)/mu,nq=4);mt=2*float(np.sum(rho*g.vol));pr=S.Problem(g,rho,mt,0.,Lam=0.)
 phi,res,it=pr.solve_aqual();assert res<1e-9
 obs=ns['mw_obs'](g,phi,a0)
 def forces(p,pts):
  dr,dt=g.grad_cells(p);fr=np.sin(g.t2d)*dr+np.cos(g.t2d)*dt;fz=np.cos(g.t2d)*dr-np.sin(g.t2d)*dt
  return np.column_stack([g.interp_cells(v,pts[:,0],pts[:,1]) for v in (fr,fz)])*a0*S.KPC/1e6
 total=forces(phi,points);bar=forces(pr.solve_newton(),points)
 K=forces(phi,profiles)[:,1]*1e6/S.KPC/(2*np.pi*S.G_SI)/ns['SIGU']
 return dict(obs=obs,points_kpc=points.tolist(),total_forces=total.tolist(),baryon_forces=bar.tolist(),Kz_profile=K.tolist(),rho_b0=float(rhof(8.122,0)/1e9),baryon_columns=X.columns(rhof,8.122),mass=mt*mu,residual=res)
results={'scope':'24 illustrative baryon solves; fixed stars/gas heights; no data likelihood refit, EFE or broken exponential','models':[]}
# Baseline reproduction against existing X5 unscreened model.
rhof,_=fam.rho(40.3,1.64e10,1.9333333333333336)
base=solve(rhof,'canonical')
ref=json.loads((ROOT/'rebuild_2026_10_22/X5_mw_joint_baryons/x5_grid_canonical.json').read_text())
ref=next(c['L0'] for c in ref['cells'] if c['sig_b']==40.3 and c['M_bb']==1.64e10 and abs(c['R_d']-1.9333333333333336)<1e-8)
assert abs(base['obs']['K_R0']-ref['K_R0'])<1e-6
results['baseline_check']={'computed':base['obs'],'stored':ref}
for foot in ('canonical','alt'):
 for sig,rd,mb in itertools.product((40.,44.,47.),(2.24,2.37),(1.64e10,2.12e10)):
  row=solve(density(sig,rd,mb),foot);row.update(footing=foot,sigma_b=sig,Rd=rd,Mbulge=mb)
  results['models'].append(row)
  print(foot,sig,rd,mb,'K',round(row['obs']['K_R0'],2),'V',round(row['obs']['vc_R0'],2),'RCchi',round(row['obs']['chi2_rc'],1),flush=True)
# Selection is explicit post hoc: illustrative local K~72 and V~229, not a fitted likelihood.
for foot in ('canonical','alt'):
 cand=[r for r in results['models'] if r['footing']==foot]
 best=min(cand,key=lambda r:((r['obs']['K_R0']-72)/7.5)**2+((r['obs']['vc_R0']-229.05)/4.645)**2)
 fine=solve(density(best['sigma_b'],best['Rd'],best['Mbulge']),foot,True)
 err=float(np.max(abs(np.array(fine['total_forces'])/best['total_forces']-1)))
 results.setdefault('selected',[]).append(dict(footing=foot,sigma_b=best['sigma_b'],Rd=best['Rd'],Mbulge=best['Mbulge'],fine=fine,main_fine_max_fraction=err))
print('selected',[(r['footing'],r['sigma_b'],r['Rd'],r['Mbulge'],r['main_fine_max_fraction']) for r in results['selected']],flush=True)
(ROOT/sys.argv[1]).write_text(json.dumps(results,indent=2)+'\n')
