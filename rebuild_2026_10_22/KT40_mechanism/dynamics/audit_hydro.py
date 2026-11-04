"""Independent algebra and tensor-derivative audit of stored MW gas probes."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import checks_v3 as C


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args()
    src=Path(__file__).resolve().parents[1]/'mw/hydro_002/results.json'
    d=json.loads(src.read_text());assert d['complete'] and d['all_checks_pass']
    G=4.30091e-6;rows=[];n=np.array([0.,1.,0.]);nn=np.outer(n,n)
    for case in d['cases']:
        for j in case['jets']:
            h=j['hydrostatic_barotropic_two_gas'];g=np.array(j['g_over_a0']);H=np.array(j['H_over_a0_per_kpc'])
            q=C.coefficients(g,H,n,1.125,ell=3.)
            assert math.isclose(q['N'],h['N_vertical_kpc2'],rel_tol=1e-12,abs_tol=1e-12)
            step=1e-4*np.linalg.norm(H)
            bp=C.L.tensor_terms(g,H+step*nn,3.,p=1.125)['B']
            bm=C.L.tensor_terms(g,H-step*nn,3.,p=1.125)['B']
            fd=float(np.sum(nn*(bp-bm)))/(2*step)
            nerr=abs(fd-q['N'])/max(abs(q['N']),abs(q['D']),1e-12)
            assert nerr<2e-6
            ev=np.linalg.eigvalsh(H);hh=float(np.sum(H*H))
            qmin=0. if ev[0]<=0<=ev[-1] else float(np.min(ev*ev))/hh
            qmax=float(np.max(ev*ev))/hh
            extrema=sorted(q['D']*(1+2*q['J']*u) for u in [qmin,qmax])
            assert np.allclose(extrema,[j['N_min_kpc2'],j['N_max_kpc2']],rtol=1e-12,atol=1e-12)
            gz=h['physical_gz_km2_s2_per_kpc'];Z=j['Z_kpc']
            cs2=np.array([a*gz/math.tanh(Z/(2*a)) for a in [.085,.045]])
            assert np.allclose(cs2,[h['required_cs_squared_HI_km2_s2'],h['required_cs_squared_H2_km2_s2']],rtol=1e-13)
            rho=1e9*np.array([h['rho_HI_Msun_pc3'],h['rho_H2_Msun_pc3']])
            v=np.sqrt(rho);matrix=4*math.pi*G*q['N']*np.outer(v,v)-np.diag(cs2)
            eig=np.linalg.eigvalsh(matrix)
            assert np.allclose(matrix,h['growth_matrix_km2_s2'],rtol=1e-12,atol=1e-10)
            assert np.allclose(eig,h['growth_matrix_eigenvalues_km2_s2'],rtol=1e-12,atol=1e-10)
            positive=bool(np.all(cs2>0));assert positive==h['positive_compressibility_hydrostatic_closure']
            worst=None;worst_eig=None
            if positive:
                parameter=4*math.pi*G*q['N']*float(np.sum(rho/cs2))
                assert math.isclose(parameter,h['rank_one_instability_parameter'],rel_tol=1e-12,abs_tol=1e-12)
                assert (eig[-1]>0)==(parameter>1)
                worst=4*math.pi*G*extrema[1]*float(np.sum(rho/cs2))
                worst_eig=float(np.linalg.eigvalsh(4*math.pi*G*extrema[1]*np.outer(v,v)-np.diag(cs2))[-1])
                assert (worst_eig>0)==(worst>1)
                assert worst<1
            else:
                assert gz<0 and np.all(cs2<0)
                assert h['rank_one_instability_parameter'] is None
                assert h['high_k_growth_under_positive_compressibility'] is None
            rows.append(dict(footing=case['footing'],refine=case['refine'],R=j['R_kpc'],Z=Z,
                             N_vertical_fd_normalized_error=nerr,gz=gz,
                             positive_compressibility_closure=positive,
                             worst_direction_parameter=worst,worst_direction_growth_matrix_max_eigenvalue=worst_eig))
    summary={}
    for foot in ['canonical','alt']:
        rr=[r for r in rows if r['footing']==foot and r['refine']==5]
        good=[r for r in rr if r['positive_compressibility_closure']]
        bad=[r for r in rr if not r['positive_compressibility_closure']]
        assert len(good)==14 and len(bad)==1 and (bad[0]['R'],bad[0]['Z'])==(12.,.3)
        summary[foot]=dict(positive_compressibility_points=14,
            maximum_all_angle_instability_parameter=max(r['worst_direction_parameter'] for r in good),
            outward_force_point=bad[0])
    out=dict(all_checks_pass=True,rows=rows,summary=summary,source=str(src),
             qualification='Algebra and independent tensor derivative audit of stored fields; no new Poisson solve. For the specified isotropic barotropic two-gas closure, all14 restoring-force sample points have stable leading high-k symbol in all directions. The remaining point has no positive-compressibility hydrostatic closure. This is not a global or collisionless stability theorem.')
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(all_checks_pass=True,rows=len(rows),summary=summary),indent=2))


if __name__=='__main__':main()
