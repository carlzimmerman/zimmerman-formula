import argparse,json
from pathlib import Path
import numpy as np
from scipy.special import logsumexp
from molecule import surfaces
from chemistry import Chemistry

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    root=Path(__file__).parent;r=json.loads((root/'run_spectrum/results.json').read_text())
    R=r['lcao_minimum_R'];curves=[]
    for h in [.01,.005,.001]:
        K=(surfaces(R+h)[0]-2*surfaces(R)[0]+surfaces(R-h)[0])/h**2
        gap=surfaces(R)[1]-surfaces(R)[0]
        curves.append(dict(step=h,K=float(K),vibrational_frequency=float(np.sqrt(K/50)),electronic_gap=float(gap),ratio=float(gap/np.sqrt(K/50))))
    ch=Chemistry(r['spectra'][1]);checks=[];masses=np.array([100,1,101,201])
    for density in [1e-8,1e-4,.1]:
        for T in [.01,.03,.1]:
            s=ch.state(density,T);f=np.array([s['x'],s['c'],s['a'],s['t']])
            def thermo(temp):
                logq=np.array([0,0,.5/temp,.5/temp+logsumexp(ch.logw+ch.B/temp)])
                mu=temp*(np.log(density*f)+1.5*np.log(2*np.pi/(masses*temp))-logq)
                F=float(np.sum(f*(mu-temp)))
                return F,mu
            F,mu=thermo(T);h=T*1e-5
            un=-T*T*(thermo(T+h)[0]/(T+h)-thermo(T-h)[0]/(T-h))/(2*h)
            checks.append(dict(density=density,T=T,chemical_potential_error=float(max(abs(mu[0]+mu[1]-mu[2]),abs(mu[2]+mu[0]-mu[3]))),energy_derivative_error=abs(un-s['energy'])))
    assert max(x['chemical_potential_error'] for x in checks)<1e-9
    assert max(x['energy_derivative_error'] for x in checks)<1e-8
    result=dict(curvatures=curves,thermodynamic_checks=checks)
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
