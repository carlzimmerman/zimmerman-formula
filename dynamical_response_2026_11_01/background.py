"""Frozen FR01 BVP reconstruction; imports are passive."""
import sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'inputs/fr01'))
import endpoint_reconstruction as fr01

class Background:
    def __init__(self,name):
        family='weak_diffuse' if name=='diffuse' else 'strong_compact'
        result=fr01.reconstruct_endpoint(.2,family,0. if name=='baseline' else 1.)
        self.name=name;self.sol=result['solution'];self.record=result['record']
        self.base=result['baseline_record'];self.R=self.record['radius'];self.eps=.01
        self.mass=self.record['target_dark_mass']
        self.core_radius=self.record['material_core']['radius_containing_original_core_mass']
        self.original_radius=self.base['radius']
        self.original_psi=.2
        self.outer=float(self.sol.x[-1])
        self.omega_dyn=float(np.sqrt(-self.sol.sol(self.R)[1]/self.R))
        self.reconstruction_errors=result['reconstruction_relative_differences']
    def values(self,r):
        p,dp,s,ds=self.sol.sol(r)
        return dict(psi=p,dpsi=dp,s=s,ds=ds,n=np.maximum(p,0.)**1.5*np.exp(3*s))

