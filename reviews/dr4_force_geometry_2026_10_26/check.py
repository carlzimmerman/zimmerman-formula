"""Bounded extraction from isolated v3 census caches; not a DR4 forecast."""
import hashlib
import json
import pathlib
import sys
import numpy as np
from scipy.interpolate import RegularGridInterpolator

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / 'rebuild_2026_10_22/S3_v3_mw_seals'
sys.path.insert(0, str(SRC))
import s3_mw as M

points = np.array([(r,z) for r in (8.122,12.,16.) for z in (.5,1.1,2.)])
results = {'scope':'isolated static v3, census baryons; no external field, no observation covariance', 'rows':[], 'controls':[]}
for tag, grid in [('main',M.GRID_MAIN),('fine',M.GRID_FINE)]:
    mw=M.MW(grid,tag=tag)
    g=mw.g
    def at(arr):
        return RegularGridInterpolator((g.Rc,g.zc),arr)(points)
    pn,pbn=mw.phiN(1.)
    nr,nz=g.cell_derivs(pn,pbn)
    # Analytic spherical and constant-flattening potentials sampled on the same grid.
    for q in (1.,.7):
        phi=10000.*np.log(g.RR**2+g.ZZ**2/q**2+1.)
        pb_control=dict(R=10000.*np.log(g.Re[-1]**2+g.zc**2/q**2+1.),
                        B=10000.*np.log(g.Rc**2+g.ze[0]**2/q**2+1.),
                        T=10000.*np.log(g.Rc**2+g.ze[-1]**2/q**2+1.))
        dr,dz=g.cell_derivs(phi,pb_control)
        got=points[:,1]*at(dr)/(points[:,0]*at(dz))
        err=float(np.max(abs(got-q*q)))
        assert err<.015, (tag,q,err)
        results['controls'].append(dict(grid=tag,q=q,max_q_squared_error=err))
    for foot in ('canonical','alt'):
        key=f'{tag}|{foot}|s1.000000|eN0.000000|'
        p=SRC/'_cache_final'/('mw_'+hashlib.sha1(key.encode()).hexdigest()[:16]+'.npz')
        assert p.exists(),p
        with np.load(p,allow_pickle=False) as a:
            phi=a['Phi']; info=json.loads(str(a['info']))
            pb={k:a['PB_'+k] for k in ('R','B','T')}
        assert np.isfinite(phi).all()
        dr,dz=g.cell_derivs(phi,pb)
        # Positive potential gradients; signed-acceleration D is minus this numerator.
        fr,fz=at(dr-nr),at(dz-nz)
        assert np.all(fr>0) and np.all(fz>0)
        q2=points[:,1]*fr/(points[:,0]*fz)
        delta=fz-points[:,1]/points[:,0]*fr
        for i,(r,z) in enumerate(points):
            results['rows'].append(dict(grid=tag,footing=foot,R_kpc=r,z_kpc=z,
                extra_FR=fr[i],extra_Fz=fz[i],q_eff=float(np.sqrt(q2[i])),
                vertical_excess_over_spherical=delta[i],
                total_Fz=at(dz)[i],
                source=str(p.relative_to(ROOT)),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                cached_solver_info=info))
for foot in ('canonical','alt'):
    a=[r for r in results['rows'] if r['grid']=='main' and r['footing']==foot]
    b=[r for r in results['rows'] if r['grid']=='fine' and r['footing']==foot]
    err=max(abs(x['q_eff']-y['q_eff']) for x,y in zip(a,b))
    assert err<.02,err
    results.setdefault('convergence',{})[foot]=err
out=ROOT/sys.argv[1]
out.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'controls':results['controls'],'convergence':results['convergence']}))
for r in results['rows']:
    if r['grid']=='fine':
        print(r['footing'],r['R_kpc'],r['z_kpc'],'qeff',round(r['q_eff'],4),
              'deltaFz',round(r['vertical_excess_over_spherical'],2))
