#!/usr/bin/env python3
"""Stock CLASS positive control. No clock-sector modification is inserted.

Use the existing Python 3.13 environment, not system Python 3.9. The result
tests engine availability and records reference spectra summaries; it is not
validation of a clock-to-Boltzmann mapping or a fit to observations.
"""
import argparse
import json
from pathlib import Path
import platform
import numpy as np
import classy
from classy import Class


def compute():
    params=dict(h=.6736,omega_b=.02237,omega_cdm=.1200,A_s=2.1e-9,
                n_s=.9649,tau_reio=.0544,N_ur=3.046,N_ncdm=0,YHe=.2454,
                output='tCl,pCl,lCl,mPk',lensing='yes',l_max_scalars=1500,
                **{'P_k_max_1/Mpc':1.})
    engine=Class();engine.set(params)
    try:
        engine.compute();cl=engine.raw_cl(1500);ell=cl['ell'][2:]
        dl=ell*(ell+1)*cl['tt'][2:]/(2*np.pi)
        smooth=np.convolve(dl,np.ones(9)/9,mode='same');peaks=[]
        for i in range(60,len(smooth)-60):
            if 120<ell[i]<1300 and smooth[i]>=max(smooth[i-60:i+61]):
                peaks.append(dict(ell=int(ell[i]),Dl=float(smooth[i])))
        assert len(peaks)>=3,'GR reference does not resolve three peaks'
        assert all(np.all(np.isfinite(cl[key])) for key in ('tt','ee','te','pp'))
        assert np.all(cl['tt'][2:]>0) and np.all(cl['ee'][2:]>0)
        result=dict(parameters=params,peaks=peaks[:3],sigma8=engine.sigma8(),
                    derived=engine.get_current_derived_parameters(['z_rec','100*theta_s','rs_rec']),
                    spectrum_peak_ratios=[peaks[1]['Dl']/peaks[0]['Dl'],peaks[2]['Dl']/peaks[1]['Dl']],
                    python=platform.python_version(),classy_version=classy.__version__,
                    classy_path=classy.__file__,full_theory_status='OPEN',
                    scope='EH+Lambda+baryons+CDM+radiation comparator only; CDM is not silently added to the clock candidate')
        return result
    finally:
        engine.struct_cleanup();engine.empty()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args();result=compute()
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
