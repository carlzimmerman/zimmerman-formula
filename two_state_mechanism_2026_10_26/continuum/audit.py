"""Classify actual continuum evidence; never turn numerical loss into chemistry."""
import argparse,json,re
from pathlib import Path
import numpy as np
from kmat import read_k
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
b=Path(__file__).resolve().parent
rows={}
for folder in sorted(b.glob('run_*')):
    if not (folder/'Kmat.txt').exists():continue
    settings=json.loads((folder/'results.json').read_text())['settings']
    log=(folder/'logs/scattering.scatci.out').read_text()
    poles=[float(x) for x in re.findall(r'^ EIGEN-ENERGIES\s*\n\s*([-0-9.]+)',log,re.M)]
    assert len(poles)==1,(folder,poles)
    data=read_k(folder/'Kmat.txt');S=np.array(data[0]['S_real'])+1j*np.array(data[0]['S_imag'])
    phase=np.loadtxt(folder/'eigenphases.txt')[:,1]
    phase_error=max(abs(np.angle(np.exp(2j*(r['eigenphase_sum']-v)))/2) for r,v in zip(data,phase))
    assert len(data)==len(phase)==5 and phase_error<1e-7
    rejected=settings['multipole']==8
    # Gross plausibility screen only, NOT an accuracy certificate or exact bound.
    assert (poles[0]<-2) if rejected else (-1.3<poles[0]<-1.0)
    rows[folder.name[4:]]=dict(settings={k:settings[k] for k in ['R','nb','lmax','multipole']},lowest_inner_pole=poles[0],first_energy=data[0]['energy_au'],S00=[S[0,0].real,S[0,0].imag],phase_sum=data[0]['eigenphase_sum'],max_unitarity_error=max(r['unitarity_error'] for r in data),phase_comparison_error_modulo_pi=phase_error,classification='REJECTED: spurious deep poles, insufficient integral multipoles' if rejected else 'limited corrected continuum evidence; not fully converged chemistry')

def s(label):return complex(*rows[label]['S00'])
comparisons={}
for label,left,right in [('integral_order','multipole15','corrected20'),('radial_basis','corrected20','physical_radial25'),('angular_basis','physical_radial25','physical_angular4')]:
    comparisons[label]=dict(left=left,right=right,absolute_S00_change=abs(s(left)-s(right)),phase_sum_change=rows[right]['phase_sum']-rows[left]['phase_sum'])
comparisons['fixed_kinetic_energy_derivative_S00']=[((s('corrected_plus')-s('corrected_minus'))/.02).real,((s('corrected_plus')-s('corrected_minus'))/.02).imag]
nuclear=json.loads((b/'run_nuclear/results.json').read_text());nrows=[]
for row in nuclear['rows']:
    coarse,fine=row['steps'];assert coarse['antisymmetry_error']>3*fine['antisymmetry_error'];assert abs(coarse['metric'][0]-fine['metric'][0])<5e-6
    assert min(fine['omitted_derivative_norm'])>0
    nrows.append(dict(R=row['R'],ground_metric=fine['metric'][0],omitted_ground_fraction=fine['omitted_derivative_norm'][0]/fine['metric'][0],radial_adiabatic_correction=fine['ground_DBOC'],antisymmetry_error=fine['antisymmetry_error']))
outer=json.loads((b/'run_outer_corrected/results.json').read_text())['rows'];outer_summary=[]
for row in outer:
    r=row['data'][0];outer_summary.append(dict(radius=row['radius'],phase_sum=r['eigenphase_sum'],S00=[r['S_real'][0][0],r['S_imag'][0][0]]))
scans={}
for name in ['scan_corrected','scan_physical']:
    for key,value in json.loads((b/('run_'+name)/'results.json').read_text()).items():
        if isinstance(value,dict):scans[key]=dict(candidate_peaks=value['candidate_peaks'],max_unitarity_error=value['max_unitarity_error'])
result=dict(points=rows,comparisons=comparisons,nuclear=nrows,outer=outer_summary,scans=scans,physical_DR_rates_derived=False,new_physical_galaxy_trajectories=0,photon_recycling_coupled_to_new_rates=False,scope='Numerical continuum and finite-basis radial couplings only. No flux into nuclear dissociation products computed. Unitarity is algebraic consistency, not convergence.')
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(comparisons=comparisons,nuclear=nrows,outer=outer_summary,scans=scans),indent=2))
