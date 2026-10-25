import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from experiment import matrix
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
# Independent field-equation linearization in a Fourier representation.
N=48;x=np.arange(N)*2*np.pi/N;k=np.fft.fftfreq(N,1/N);k2=k*k
inv=np.zeros(N);inv[1:]=1/k2[1:]
m=np.array([1.,.1]);q=np.array([1.,-1.]);Q=.7
errors=[]
for amp in [1e-3,1e-4,1e-5]:
    dn=amp*np.array([1.,-.3]);psi=np.sqrt(1+dn[:,None]*np.cos(x))
    density=psi**2
    vc=np.fft.ifft(np.fft.fft(q@density)*inv).real
    vm=np.fft.ifft(np.fft.fft(m@density)*inv).real
    V=(q[:,None]*vc-m[:,None]*vm)/(2*Q)
    def op(a):return np.fft.ifft(np.fft.fft(a,axis=1)*k2,axis=1)*Q/m[:,None]+V*a
    pdot=-1j*op(psi);pddot=-op(op(psi))
    densityddot=2*abs(pdot)**2+2*np.real(psi*pddot)
    measured=2*np.mean(densityddot*np.cos(x),axis=1)
    D,_=matrix(Q,.1)
    predicted=-(D@(np.sqrt(m)*dn))/np.sqrt(m)
    errors.append(dict(amplitude=amp,relative_error=float(np.linalg.norm(measured-predicted)/np.linalg.norm(predicted))))
assert errors[-1]['relative_error']<1e-7
base=Path(__file__).resolve().parent
d=json.loads((base/'run_response/results.json').read_text())
rows=[r for r in d['spectra'] if r['epsilon']==.1 and r['gravity']]
Qvalues=np.array([r['Q'] for r in rows]);w=np.array([r['w2'] for r in rows]);res=np.array([r['dipole_residues'] for r in rows])
fig,ax=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
for j,label in enumerate(['Lower branch','Upper branch']):
 ax[0].plot(Qvalues,w[:,j],label=label)
ax[0].axhline(0,color='black',lw=.6);ax[0].set_xscale('log');ax[0].set_yscale('symlog',linthresh=1)
ax[0].set(xlabel=r'$Q=\hbar k^2/(2m\omega_0)$',ylabel=r'$\omega^2/\omega_0^2$',title='Self-gravitating quantum modes')
ax[0].legend();ax[0].text(.03,.05,'Negative = instability, not a vacuum mode',transform=ax[0].transAxes,fontsize=9)
thresholds=[r['critical_mass_eV'] for r in d['threshold_examples']]
labels=['3e5 solar masses / 0.3 kpc','1e8 / 1 kpc','6e10 / 3 kpc','1e14 / 300 kpc']
ax[1].scatter(thresholds,range(4),s=70,color='#416b8e')
ax[1].set_xscale('log');ax[1].set_yticks(range(4),labels);ax[1].invert_yaxis()
ax[1].set(xlabel=r'Critical positive-particle mass [eV/$c^2$]',title='Same microphysics, different physical scales')
ax[1].grid(axis='x',alpha=.2)
fig.suptitle('Charged Bose mean-field candidate: epsilon = 0.1',fontsize=14)
out=Path(args.output);fig.savefig(out.parent/'quantum_scale.png',dpi=160)
out.write_text(json.dumps(dict(independent_field_linearization=errors,figure='quantum_scale.png'),indent=2))
print(json.dumps(errors))
