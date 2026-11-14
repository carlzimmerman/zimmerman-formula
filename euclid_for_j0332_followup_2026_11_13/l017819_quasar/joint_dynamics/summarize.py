"""Read completed evidence and draw a conditional sensitivity comparison."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent


def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    spec=json.loads((HERE.parent/'dynamics_audit/run_02/primary_split.json').read_text())
    sens=json.loads((HERE/'a0_sensitivity_01/result.json').read_text())
    fine=json.loads((HERE/'fields_03/result.json').read_text())
    tab=np.array(spec['profile']);dc=tab[:,2]-spec['chi2']
    sensitivity=[]
    for row in sens['records'][:4]:
        sigma=row['aperture']['rms_kms'][0]
        sensitivity.append(dict(label=row['label'],predicted_sigma_kms=sigma,
                                primary_profile_delta_chi2_linear_interpolation=float(np.interp(sigma,tab[:,0],dc))))
    values=[v for r in fine['records'] for s in r['scenarios'] for v in s['rms_kms']]
    centered=[v for r in fine['records'] for s in r['scenarios'] for v in s['satoh_k1_centered_sigma_kms']]
    summary=dict(spectral_best_sigma_kms=spec['sigma'],
                 conditional_profile_intervals=spec['delta_chi2_intervals_linear_grid'],
                 SS6_Gaussian_host_mass_fixtures_rms_range_kms=[min(values),max(values)],
                 SS6_Gaussian_host_mass_fixtures_satoh_centered_range_kms=[min(centered),max(centered)],
                 fixed_mass_a0_sensitivity=sensitivity,
                 non_claims=['No joint posterior or calibrated pass/fail','No alternate-a0 mass refit',
                             'Gaussian-host masses remain dependent on signed-source and light assumptions',
                             'Jeans second moments do not certify a Gaussian LOSVD or distribution function'])
    (out/'result.json').write_text(json.dumps(summary,indent=2)+'\n')
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(1,2,figsize=(12,4.7))
    ax[0].plot(tab[:,0],dc,'o-',ms=3,color='#235f8c',label='DESI absorption profile')
    ax[0].axhline(1,color='grey',ls=':',lw=1);ax[0].axhline(4,color='grey',ls=':',lw=1)
    ax[0].axvspan(min(values),max(values),color='#16a085',alpha=.22,label='Fixed-a₀ Jeans scenarios¹')
    ax[0].set(xlim=(160,300),ylim=(0,10),xlabel='Velocity dispersion (km/s)',ylabel='Conditional Δχ²',title='The spectrum allows the predicted scale')
    ax[0].legend(frameon=False,fontsize=9)
    ys=[x['predicted_sigma_kms'] for x in sensitivity]
    lo,hi=spec['delta_chi2_intervals_linear_grid']['1.0']
    ax[1].axhspan(lo,hi,color='#235f8c',alpha=.15,label='DESI Δχ² ≤ 1 interval')
    ax[1].axhline(spec['sigma'],color='#235f8c',ls='--',lw=1)
    ax[1].plot([0,.5,1,2],ys,'o-',color='#16a085',lw=2,label='Same stellar mass and light shape')
    ax[1].scatter([1],[ys[2]],s=100,facecolors='none',edgecolors='black',zorder=4)
    ax[1].set(xticks=[0,.5,1,2],xticklabels=['Newton²','0.5','1 (theory)','2'],ylim=(185,255),
              xlabel='a₀ / predicted a₀',ylabel='Predicted fiber RMS (km/s)',title='A factor-four a₀ range changes RMS by 9 km/s')
    ax[1].legend(frameon=False,fontsize=9,loc='upper left')
    fig.suptitle('L017819: compatible kinematics, limited sensitivity to a₀',fontsize=14)
    fig.text(.06,.02,'¹ Two Gaussian-host light/mass fixtures; orbital and seeing scenarios.  ² Newtonian stars only, not a dark-matter fit.\nMass is held fixed in the right panel. No alternative-a₀ refit, complete spectral uncertainty, or full-theory verdict.',fontsize=9,color='#444444')
    fig.tight_layout(rect=[0,.10,1,.94]);fig.savefig(out/'a0_kinematics.png',dpi=170);plt.close(fig)
    print(json.dumps(summary),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
