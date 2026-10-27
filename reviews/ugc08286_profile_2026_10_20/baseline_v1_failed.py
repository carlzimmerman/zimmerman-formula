"""Read-only legacy reproduction and conditional spherical residual control."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
data = np.loadtxt(root/'real_research/data/sparc_data/UGC08286_rotmod.dat')
r,v,ev,vg,vd,vb = data[:,:6].T
assert len(r)==17 and np.all(np.diff(r)>0) and np.all(vb==0)
foot = json.loads((root/'real_research/derivation_chain_2026/FP0_core_postulates_results.json').read_text())['numbers']
a0s={'canonical':foot['a0_canonical'], 'alt':foot['a0_rho_total']}
kpc_legacy=3.0857e19
nu=lambda y:(1+np.sqrt(1+4/y))/2
gas=np.sign(vg)*vg**2
star=vd**2
lu0=np.log10(0.5)
sv=2/np.log(10)*np.maximum(ev,1)/np.maximum(v,1)
w=1/(sv**2+0.05**2)
luw=lu0+np.linspace(-1.5,1.5,1201)

def legacy_chi(lu):
    b=gas[:,None]+star[:,None]*10**np.atleast_1d(lu)[None,:]
    model=nu(b*1e6/(r[:,None]*kpc_legacy)/a0s['canonical'])*b
    residual=np.log10(v**2)[:,None]-np.log10(model)
    c=np.sum(w[:,None]*residual,axis=0)/w.sum()
    return np.sum(w[:,None]*(residual-c)**2,axis=0),c

ch,c=legacy_chi(luw)
best=int(np.argmin(ch))
ch0,c0=legacy_chi([lu0])
legacy=dict(delta_chi2=float(ch0[0]-ch[best]),c_req=float(c0[0]),
            U_ML=float(10**luw[best]))
old=json.loads((root/'argon_push/AG4h_pull_systematics/ag4h_results.json').read_text())
oldrow=next(x for x in old['rows'] if x['name']=='UGC08286')
checks={key:abs(legacy[key]-oldrow[key])<1e-9 for key in legacy}
assert all(checks.values()), (legacy,oldrow)

G=4.300917270036279e-6  # kpc (km/s)^2 / Msun, from inherited SI constants
rows={}
for footing,a0 in a0s.items():
    b=gas+0.5*star
    law=nu(b*1e6/(r*kpc_legacy)/a0)*b
    d=v**2-law
    curves=[]
    for nsig in (0,1,2):
        lo=np.maximum(v-nsig*ev,0)**2-law
        hi=(v+nsig*ev)**2-law
        # One spherical shell per observed radial interval, including a
        # central shell. Interior enclosed mass is monotone by construction.
        A=G/r[:,None]*np.tri(len(r))
        # Variables are masses in 1e9 Msun for numerical conditioning.
        A=A*1e9
        ans=linprog(np.ones(len(r)), A_ub=np.r_[A,-A],
                    b_ub=np.r_[hi,-lo], bounds=(0,None),method='highs')
        curves.append(dict(nsigma=nsig,feasible=bool(ans.success),
                    mass_msun=float(ans.fun*1e9) if ans.success else None,
                    solver_status=int(ans.status),message=ans.message,
                    max_constraint_violation=float(max(np.max(A@ans.x-hi),np.max(lo-A@ans.x),0)) if ans.success else None))
    rows[footing]=dict(a0_si=float(a0),r_kpc=r.tolist(),v_obs=v.tolist(),
        v_error=ev.tolist(),gas_v2_signed=gas.tolist(),
        stellar_unit_v2=star.tolist(),baseline_v2=law.tolist(),
        residual_v2=d.tolist(),spherical_required_enclosed_mass_msun=(r*d/G).tolist(),
        spherical_monotonic_central_values=bool(np.all(d>=0) and np.all(np.diff(r*d)>=0)),
        spherical_interval_controls=curves)
result=dict(assertion_tested='Reproduce preexisting AG4h UGC08286 data-only fit and compute fixed-source additive spherical surplus controls at 0,1,2 quoted velocity-error boxes.',
    legacy=legacy,legacy_checks=checks,footings=rows,point_count=17,
    spherical_only=True,actual_disk_inversion=False,
    errors='Quoted velocity errors treated as independent intervals, not a joint-confidence statement; legacy reproduction alone retains its old 0.05dex floor.',
    new_fitted_physical_parameters=0)
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(legacy=legacy,checks=checks,spherical={k:x['spherical_interval_controls'] for k,x in rows.items()}),indent=2))
