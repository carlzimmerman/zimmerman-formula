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
    fine=json.loads((HERE/'fields_04/result.json').read_text())
    tab=np.array(spec['profile']);dc=tab[:,2]-spec['chi2']
    sensitivity=[]
    for row in sens['records'][:4]:
        sigma=row['aperture']['rms_kms'][0]
        sensitivity.append(dict(label=row['label'],predicted_sigma_kms=sigma,
                                primary_profile_delta_chi2_linear_interpolation=float(np.interp(sigma,tab[:,0],dc))))
    values=[v for r in fine['records'] for s in r['scenarios'] for v in s['rms_kms']]
    centered=[v for r in fine['records'] for s in r['scenarios'] for v in s['satoh_k1_centered_sigma_kms']]
    newton=json.loads((HERE/'fields_05/result.json').read_text())
    nvalues=[v for r in newton['records'] for a in r['scenarios'] for v in a['rms_kms']]
    comparisons=[]
    for fixture in ['run_04','run_03']:
        control=json.loads((HERE.parent/'aqual_host/newton_control/run_01'/fixture/'result.json').read_text())
        arow=next(r for r in fine['records'] if r['specification']['fixture']==fixture)
        nrow=next(r for r in newton['records'] if r['specification']['fixture']==fixture)
        ap=next(x for x in arow['scenarios'] if x['seeing_fwhm_arcsec']==1.2)['rms_kms'][1]
        npred=next(x for x in nrow['scenarios'] if x['seeing_fwhm_arcsec']==1.2)['rms_kms'][1]
        comparisons.append(dict(fixture=fixture,AQUAL_mass_msun=10**control['aqual_logmass_total'],Newton_mass_msun=control['mass_msun'],AQUAL_image_chi2=control['aqual']['chi2'],Newton_image_chi2=control['newton']['chi2'],AQUAL_fiber_rms_b1_seeing1p2=ap,Newton_fiber_rms_b1_seeing1p2=npred,AQUAL_spectrum_profile_penalty=float(np.interp(ap,tab[:,0],dc)),Newton_spectrum_profile_penalty=float(np.interp(npred,tab[:,0],dc))))
    summary=dict(mass_refitted_control=comparisons,Newton_refitted_rms_range_kms=[min(nvalues),max(nvalues)],spectral_best_sigma_kms=spec['sigma'],
                 conditional_profile_intervals=spec['delta_chi2_intervals_linear_grid'],
                 nonnegative_host_mass_fixtures_rms_range_kms=[min(values),max(values)],
                 nonnegative_host_mass_fixtures_satoh_centered_range_kms=[min(centered),max(centered)],
                 fixed_mass_a0_sensitivity=sensitivity,
                 non_claims=['No joint posterior or calibrated pass/fail','No alternate-a0 mass refit',
                             'Nonnegative-host masses remain dependent on imperfect foreground and source assumptions',
                             'Jeans second moments do not certify a Gaussian LOSVD or distribution function'])
    (out/'result.json').write_text(json.dumps(summary,indent=2)+'\n')
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(1,2,figsize=(12,4.7))
    ax[0].plot(tab[:,0],dc,'o-',ms=3,color='#235f8c',label='DESI absorption profile')
    ax[0].axhline(1,color='grey',ls=':',lw=1);ax[0].axhline(4,color='grey',ls=':',lw=1)
    ax[0].axvspan(min(values),max(values),color='#16a085',alpha=.22,label='Fixed-a₀ Jeans scenarios¹')
    ax[0].axvspan(min(nvalues),max(nvalues),color='#df8b24',alpha=.22,label='Newtonian stars, mass refitted¹')
    ax[0].set(xlim=(160,300),ylim=(0,10),xlabel='Velocity dispersion (km/s)',ylabel='Conditional Δχ²',title='Both mass-refitted models fit the kinematic scale')
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
    fig.suptitle('L017819: the present test does not isolate a₀',fontsize=14)
    fig.text(.06,.015,'¹ Left: masses refitted in each law; two light profiles and orbital/seeing scenarios.\n² Newtonian stars only; no dark-matter halo. Right: original stellar mass held fixed.\nNo complete spectral/systematic uncertainty or full-theory verdict.',fontsize=9,color='#444444')
    fig.tight_layout(rect=[0,.10,1,.94]);fig.savefig(out/'a0_kinematics.png',dpi=170);plt.close(fig)
    print(json.dumps(summary),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
