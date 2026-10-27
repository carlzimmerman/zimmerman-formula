import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import minimize_scalar


def surfaces(R):
    S=np.exp(-R)*(1+R+R*R/3)
    J=-1/R+np.exp(-2*R)*(1+1/R)
    K=-np.exp(-R)*(1+R)
    Haa=-.5+J;Hab=-.5*S+K
    return (Haa+Hab)/(1+S)+1/R,(Haa-Hab)/(1-S)+1/R,S

def radial(M=100.,dr=.04,L=40.,J=0,surface=0):
    R=np.arange(dr,L,dr);mu=M/2
    U=surfaces(R)[surface]+.5+J*(J+1)/(2*mu*R*R)
    diag=1/(mu*dr*dr)+U;off=np.full(len(R)-1,-1/(2*mu*dr*dr))
    return R,U,diag,off

def spectrum(M=100.,dr=.04,L=40.):
    rows=[];stop=None
    for J in range(101):
        R,U,d,e=radial(M,dr,L,J)
        if min(U)>=0:stop=J;break
        vals=eigh_tridiagonal(d,e,select='v',select_range=(-1,-1e-9),eigvals_only=True,check_finite=False)
        for v,E in enumerate(vals):rows.append(dict(J=J,v=v,binding=float(-E),weight=2*J+1))
    assert stop is not None
    return dict(mass_ratio=M,dr=dr,L=L,levels=rows,first_nonnegative_effective_potential_J=stop)

def photo(dr,L):
    R,U,diag,off=radial(dr=dr,L=L)
    E,v=eigh_tridiagonal(diag,off,select='i',select_range=(0,0),check_finite=False)
    binding=-E[0];bound=v[:,0]
    R,U,diag,off=radial(dr=dr,L=L,J=1,surface=1)
    en,vec=eigh_tridiagonal(diag,off,select='v',select_range=(0,.25),check_finite=False)
    S=surfaces(R)[2];dipole=R/(2*np.sqrt(1-S*S))
    strength=abs((bound*dipole)@vec)**2/np.gradient(en)
    energies=[.003,.01,.03,.1]
    rows=[]
    for ep in energies:
        ds=float(np.interp(ep,en,strength))
        rows.append(dict(continuum_energy=ep,photon_energy=float(ep+binding),
                         dipole_strength_per_energy=ds,
                         cross_section_over_alpha_aD2=float(4*np.pi*np.pi/3*(ep+binding)*ds)))
    return dict(dr=dr,L=L,binding=float(binding),continuum_levels=len(en),samples=rows)

def continuum():
    R,U,d,e=radial(dr=.06,L=60.)
    ew,v=eigh_tridiagonal(d,e,check_finite=False)
    w=np.exp(-(R-15)**2/(2*1.5**2))*np.exp(-3j*R)
    c=v.T@w;c[ew<0]=0;c/=np.linalg.norm(c)
    times=np.linspace(0,400,81)
    states=v@(c[:,None]*np.exp(-1j*ew[:,None]*times))
    Hstates=d[:,None]*states
    Hstates[1:]+=e[:,None]*states[:-1];Hstates[:-1]+=e[:,None]*states[1:]
    E=np.real(np.sum(states.conj()*Hstates,axis=0))
    bound=abs(v[:,ew<0].T@states)**2
    core=np.sum(abs(states[R<6])**2,axis=0)
    return dict(dr=.06,L=60.,times=times.tolist(),core_probability=core.tolist(),
                maximum_core_probability=float(max(core)),maximum_bound_probability=float(max(bound.sum(axis=0))),
                max_energy_error=float(max(abs(E-E[0]))),norm_error=float(max(abs(np.sum(abs(states)**2,axis=0)-1))))

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    opt=minimize_scalar(lambda r:surfaces(r)[0],bounds=(.2,8),method='bounded',options={'xatol':1e-13})
    specs=[spectrum(dr=h) for h in [.04,.02]]
    # Selected masses are separate spectra, not galaxy-specific choices.
    specs.extend(spectrum(M=m) for m in [50,1000])
    photos=[photo(.04,60),photo(.02,60),photo(.04,120)]
    cont=continuum()
    assert abs(opt.x-2.493)<.002
    assert len(specs[0]['levels'])>0
    assert cont['max_energy_error']<1e-10
    assert cont['maximum_bound_probability']<1e-20
    assert cont['norm_error']<1e-10
    result=dict(lcao_minimum_R=float(opt.x),well_depth=float(-.5-opt.fun),spectra=specs,photoionization=photos,continuum=cont)
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print('minimum',opt.x,'well',-.5-opt.fun)
    print('spectra',[(s['mass_ratio'],s['dr'],len(s['levels']),s['levels'][0]['binding']) for s in specs])
    print('continuum', {k:v for k,v in cont.items() if k not in ['times','core_probability']})
    print('photo',photos)
if __name__=='__main__':main()
