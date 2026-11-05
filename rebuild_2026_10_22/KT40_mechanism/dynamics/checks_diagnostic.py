"""Independent derivatives and plane-wave energy checks for local KT39 dynamics."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
path = ROOT/'rebuild_2026_10_22/KT39_power_curvature/analytic/law.py'
spec = importlib.util.spec_from_file_location('kt40_frozen_law',path)
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)


def coefficients(g,H,n,p,ell=1.,a0=1.):
    x = float(g@g)/a0**2
    h2 = float(np.sum(H*H))
    s = ell**2*h2/a0**2
    z = x+s**p
    d = float(L.zRprime(z))
    f = x/z
    u = z**.25
    alpha = 2-(-.5/(u*math.sqrt(u*u+4)))/d
    D = p*ell**2*s**(p-1)*f*d
    J = p-1-p*alpha*(1-f)
    N = D*(1+2*J*float(n@H@n)**2/h2) if h2 else 0.
    K = float(L.R(z))+f*d+2*float(n@g)**2/(a0*a0*z)*d*(2-alpha*f)
    return dict(x=x,s=s,z=z,f=f,alpha=alpha,D=D,J=J,K=K,N=N)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args()
    directions=[np.array([1.,0.,0.]),np.array([0.,1.,0.]),
                np.array([1/math.sqrt(3),math.sqrt(2/3),0.])]
    rows=[]
    for p in [1.,1.125,1.25,1.5,1.75,2.]:
        for gscale in [.1,1.,10.]:
            for q in [.01,.1,1.,10.]:
                for delta in [0.,.01]:
                    g=gscale*np.array([1.,.3,-.2]);H=q*np.diag([-2+delta,1+delta,1+delta])
                    for n in directions:
                        nn=np.outer(n,n);analytic=coefficients(g,H,n,p)
                        errors=[]
                        for step in [1e-3,1e-4,1e-5]:
                            hg=step*np.linalg.norm(g);hh=step*np.linalg.norm(H)
                            gp=L.tensor_terms(g+hg*n,H,1.,p=p)
                            gm=L.tensor_terms(g-hg*n,H,1.,p=p)
                            hp=L.tensor_terms(g,H+hh*nn,1.,p=p)
                            hm=L.tensor_terms(g,H-hh*nn,1.,p=p)
                            K=float(n@(gp['A']-gm['A']))/(2*hg)+1
                            N=float(np.sum(nn*(hp['B']-hm['B'])))/(2*hh)
                            mixed_g=float(np.sum(nn*(gp['B']-gm['B'])))/(2*hg)
                            mixed_H=float(n@(hp['A']-hm['A']))/(2*hh)
                            errors.append(dict(step=step,
                                K_relative=abs(K-analytic['K'])/max(abs(analytic['K']),1e-14),
                                N_relative=abs(N-analytic['N'])/max(abs(analytic['N']),1e-14),
                                mixed_relative=abs(mixed_g-mixed_H)/max(abs(mixed_g),abs(mixed_H),1e-10)))
                        assert min(v['K_relative'] for v in errors)<2e-6
                        assert min(v['N_relative'] for v in errors)<2e-6
                        
                        if min(v['mixed_relative'] for v in errors)>=2e-5:
                            print('FAILED MIXED',p,gscale,q,delta,n.tolist(),float(n@H@n),errors,flush=True)
                            raise AssertionError('mixed conditioning diagnostic')
                        assert 1.25<analytic['alpha']<1.5
                        rows.append(dict(p=p,gscale=gscale,q=q,delta=delta,direction=n.tolist(),analytic=analytic,errors=errors))
    g=np.array([1.,0.,0.]);H=np.diag([-1.99,1.01,1.01]);p=1.125
    explicit=[coefficients(g,H,n,p) for n in directions[:2]]
    assert explicit[0]['N']>0>explicit[1]['N']
    plane=[];angles=np.arange(128)*2*np.pi/128
    E0=float(L.tensor_terms(g,H,1.,p=p)['energy'])
    for n in directions[:2]:
        nn=np.outer(n,n);c=coefficients(g,H,n,p)
        for k in [1.,3.]:
            target=c['K']*k*k+c['N']*k**4
            errs=[]
            for amp in [1e-3,1e-4]:
                energies=[]
                for sign in [1,-1]:
                    dg=-sign*amp*k*np.sin(angles)[:,None]*n
                    dH=-sign*amp*k*k*np.cos(angles)[:,None,None]*nn
                    energies.append(np.mean(L.tensor_terms(g+dg,H+dH,1.,p=p)['energy']))
                actual=float((sum(energies)-2*E0)/(amp*amp))
                errs.append(dict(amplitude=amp,second_variation=actual,relative=abs(actual-target)/max(abs(target),1e-12)))
            assert min(v['relative'] for v in errs)<2e-5
            plane.append(dict(n=n.tolist(),k=k,target=target,errors=errs))
    G=6.6743e-11;KPC=3.0856775814913673e19;MSUN=1.98892e30
    physical={}
    for foot,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
        ell=3*KPC;rho=.03*a0/(4*math.pi*G*ell)
        N=explicit[0]['N']*ell*ell
        cs=math.sqrt(4*math.pi*G*rho*N)
        physical[foot]=dict(a0=a0,ell_m=ell,rho_kg_m3=rho,
            rho_Msun_pc3=rho*(KPC/1000)**3/MSUN,
            radial_N_m2=N,critical_sound_speed_m_s=cs,
            dust_high_k_efold_years_at_wavelength_1pc=(KPC/1000)/(2*math.pi*cs)/(365.25*86400),
            external_point_mass_Msun=a0*ell**2/G/MSUN,
            external_point_distance_kpc=3.)
    out=dict(all_checks_pass=True,jet_count=len(rows),jets=rows,explicit_positive_density_jet=dict(g=g.tolist(),H=H.tolist(),power=p,radial=explicit[0],tangential=explicit[1]),
             plane_wave_energy=plane,physical_scaling=physical,
             qualification='Frozen coefficient barotropic matter closure; the explicit jet is not a fitted MW location. Pressureless high-k growth is not a collisionless or relativistic no-go.')
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(all_checks_pass=True,jet_count=len(rows),explicit=explicit,physical=physical),indent=2))


if __name__=='__main__':main()
