"""Fixed KT39 witness plus conditional hydrostatic two-gas-fluid WKB check."""
import argparse
import json
import math
from pathlib import Path
import sys
sys.dont_write_bytecode=True
RB=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(RB/'KT39_power_curvature/mw'))
import power_model as J
from refine import grid
M,E,L,np=J.M,J.E,J.L,J.np
P=1.125
ELL=3.


def observables(g,phi,a0):
    gr,gt=g.grad_cells(phi)
    dR=np.sin(g.t2d)*gr+np.cos(g.t2d)*gt
    dz=np.cos(g.t2d)*gr-np.sin(g.t2d)*gt
    rr=np.array([4.,6.,8.122,10.,12.,16.,22.])
    v2=g.interp_cells(dR,rr,np.zeros_like(rr))*a0*rr*M.C.PS.KPC/1e6
    # Use the identical SI conversion to the established MW diagnostic.
    conv=a0/(2*np.pi*M.C.PS.G_SI)/M.C.ns['SIGU']
    kz=g.interp_cells(dz,rr,np.full_like(rr,1.1))*conv
    return dict(R_kpc=rr.tolist(),v_squared_km2_s2=v2.tolist(),Kz_Msun_pc2=kz.tolist())


def jet_stats(gg,H,rho,rhogas):
    x=float(gg@gg);h2=float(np.sum(H*H));s=ELL**2*h2;z=x+s**P
    d=float(L.zRprime(z));f=x/z;t=s**P/z;u=z**.25
    alpha=2-(-1/(2*u*math.sqrt(u*u+4)))/d
    D=P*ELL**2*s**(P-1)*f*d
    ev=np.linalg.eigvalsh(H)
    qmin=0. if ev[0]<=0<=ev[-1] else float(np.min(ev*ev)/h2)
    qmax=float(np.max(ev*ev)/h2)
    vals=[D*(1+2*((P-1)-P*alpha*t)*q) for q in [qmin,qmax]]
    lo,hi=min(vals),max(vals)
    # G has units kpc (km/s)^2 / Msun, rho Msun/kpc^3, N kpc^2.
    speed=lambda density:math.sqrt(max(0,4*math.pi*M.C.G*density*hi))
    return dict(g_over_a0=gg.tolist(),H_over_a0_per_kpc=H.tolist(),
                H_eigenvalues=ev.tolist(),x=x,s=s,z=z,chi=s**P/x,
                curvature_fraction=t,alpha=alpha,D_kpc2=D,
                N_min_kpc2=lo,N_max_kpc2=hi,rho_Msun_pc3=rho/1e9,
                gas_rho_Msun_pc3=rhogas/1e9,
                cold_total_critical_speed_km_s=speed(rho),
                cold_gas_only_critical_speed_km_s=speed(rhogas))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args();J.set_power(P)
    prior=json.loads((RB/'KT39_power_curvature/mw/refine_001/results.json').read_text())
    cells=E.population();out=dict(power=P,ell_kpc=ELL,cases=[],checks={},complete=False)
    def save():args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    for foot,index in [('canonical',1368),('alt',1287)]:
        for ref in [3,4,5]:
            g,mu=grid(foot,ref,.005,1.)
            a0=M.C.A0[foot];sol=M.Solver(g,mu,a0);model=J.Generalized(sol)
            rf,_=M.rho_cell(cells[index]);rho=g.rho_axisym(lambda R,z:rf(R,z)/mu,nq=4)
            psi=sol.LU.newton(rho);gg,hh=model.fields(psi)
            A,B,_,_=model.coefficients(gg,hh,ELL)
            source,stats=model.source(psi,ELL,fields=(gg,hh))
            sa=-(g.Crr.T@(g.vol*A[0])+g.Cth.T@(g.vol*A[1]))/g.vol
            pa=sol.LU.lu.solve(sa);pb=sol.LU.lu.solve(source-sa);ph=sol.LU.lu.solve(source)
            linear=float(np.max(abs(ph-pa-pb))/np.max(abs(ph)))
            assert linear<1e-8
            score=sol.evaluate(psi+ph)
            old=next(r['score'] for r in prior['rows'] if r['footing']==foot and r['power']==P and r['refine']==ref and r['rmin']==.005 and r['outer']==1)
            assert max(abs(score[k]-old[k])/max(abs(old[k]),1) for k in ['vc','K0','cK','cO'])<1e-8
            parts={name:observables(g,pot,a0) for name,pot in [('Newton',psi),('A',pa),('B',pb),('total',psi+ph)]}
            for key in ['v_squared_km2_s2','Kz_Msun_pc2']:
                total=np.asarray(parts['total'][key]);summed=sum(np.asarray(parts[k][key]) for k in ['Newton','A','B'])
                assert np.max(abs(total-summed))/np.max(abs(total))<1e-8
            si,co=np.sin(g.t2d),np.cos(g.t2d)
            gc=[si*gg[0]+co*gg[1],co*gg[0]-si*gg[1],np.zeros(g.n)]
            hc=[si*si*hh[0]+2*si*co*hh[1]+co*co*hh[2],
                co*co*hh[0]-2*si*co*hh[1]+si*si*hh[2],
                si*co*(hh[0]-hh[2])+(co*co-si*si)*hh[1],hh[3]]
            fg,ft=g.grad_cells(psi+ph)
            physical_z=(np.cos(g.t2d)*fg-np.sin(g.t2d)*ft)*a0*M.C.PS.KPC/1e6
            jets=[]
            for R in [4.,6.,8.122,10.,12.]:
                for Z in [.1,.3,1.1]:
                    at=lambda field:float(g.interp_cells(field,np.array([R]),np.array([Z]))[0])
                    gv=np.array([at(v) for v in gc]);hv=[at(v) for v in hc]
                    H=np.array([[hv[0],hv[2],0],[hv[2],hv[1],0],[0,0,hv[3]]])
                    localrho=float(rf(np.array(R),np.array(Z)));gas=float(M.gas_density(np.array(R),np.array(Z)))
                    row=jet_stats(gv,H,localrho,gas)
                    row.update(R_kpc=R,Z_kpc=Z,
                               trace_relative_error=abs(float(np.trace(H))-4*np.pi*localrho/mu)/(4*np.pi*localrho/mu))
                    gz=at(physical_z)
                    hI,hII=.085,.045
                    rhoI=float(M.C.ns['S0_HI']*np.exp(-4/R-R/7)/(4*hI)/np.cosh(Z/(2*hI))**2)
                    rhoII=float(M.C.ns['S0_H2']*np.exp(-12/R-R/1.5)/(4*hII)/np.cosh(Z/(2*hII))**2)
                    assert abs(rhoI+rhoII-gas)/gas<1e-13
                    cs2=np.array([hI*gz/np.tanh(Z/(2*hI)),hII*gz/np.tanh(Z/(2*hII))])
                    h2=float(np.sum(H*H))
                    Nz=row['D_kpc2']*(1+2*((P-1)-P*row['alpha']*row['curvature_fraction'])*H[1,1]**2/h2)
                    densities=np.array([rhoI,rhoII]);rootrho=np.sqrt(densities)
                    matrix=4*np.pi*M.C.G*Nz*np.outer(rootrho,rootrho)-np.diag(cs2)
                    ev=np.linalg.eigvalsh(matrix);growth_speed=math.sqrt(max(0,float(ev[-1])))
                    positive_compressibility=bool(np.all(cs2>0))
                    parameter=4*np.pi*M.C.G*Nz*float(np.sum(densities/cs2)) if positive_compressibility else None
                    if positive_compressibility: assert (ev[-1]>0)==(parameter>1)
                    row['hydrostatic_barotropic_two_gas']=dict(
                        assumptions='Isotropic barotropic gas, stationary vertical hydrostatic balance in fixed full-model potential; stars held fixed under perturbation; local high-k vertical waves. Not general collisionless/MHD dynamics.',
                        physical_gz_km2_s2_per_kpc=gz,rho_HI_Msun_pc3=rhoI/1e9,rho_H2_Msun_pc3=rhoII/1e9,
                        positive_compressibility_hydrostatic_closure=positive_compressibility,
                        required_cs_squared_HI_km2_s2=float(cs2[0]),required_cs_squared_H2_km2_s2=float(cs2[1]),
                        required_cs_HI_km_s=math.sqrt(cs2[0]) if positive_compressibility else None,
                        required_cs_H2_km_s=math.sqrt(cs2[1]) if positive_compressibility else None,
                        N_vertical_kpc2=Nz,rank_one_instability_parameter=parameter,
                        growth_matrix_km2_s2=matrix.tolist(),growth_matrix_eigenvalues_km2_s2=ev.tolist(),
                        high_k_growth_under_positive_compressibility=bool(ev[-1]>0) if positive_compressibility else None,
                        formal_matrix_growth_speed_km_s=growth_speed,
                        asymptotic_e_fold_Myr_at_10pc=None if growth_speed==0 else .01*(M.C.PS.KPC/1000)/(2*np.pi*growth_speed)/(365.25*86400*1e6))
                    jets.append(row)
            out['cases'].append(dict(footing=foot,index=index,refine=ref,cell=cells[index],a0=a0,
                                     potential_linearity_relative=linear,score=score,parts=parts,jets=jets))
            save();print(foot,ref,'maxN',max(j['N_max_kpc2'] for j in jets),'maxtrace',max(j['trace_relative_error'] for j in jets),flush=True)
    for foot in ['canonical','alt']:
        c4=next(c for c in out['cases'] if c['footing']==foot and c['refine']==4)
        c5=next(c for c in out['cases'] if c['footing']==foot and c['refine']==5)
        assert max(j['trace_relative_error'] for j in c5['jets'])<.05
        delta=max(abs(a['N_max_kpc2']-b['N_max_kpc2'])/max(abs(a['N_max_kpc2']),abs(a['N_min_kpc2']),1e-12) for a,b in zip(c5['jets'],c4['jets']))
        assert delta<.05
        out['checks'][foot]=dict(max_N4_to5_normalized_change=delta,positive_Nmax_count=sum(j['N_max_kpc2']>0 for j in c5['jets']),sampled_points=15)
    out['complete']=True;out['all_checks_pass']=True;save()


if __name__=='__main__':main()
