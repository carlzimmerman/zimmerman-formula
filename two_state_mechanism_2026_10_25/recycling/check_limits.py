import argparse,json
from pathlib import Path
import numpy as np
from photons import Radiation,environment,PREV
from fast import FastChemistry
from kinetics_v3 import Rates,parcel
BASE=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
 rad=Radiation(6)
 # Same physical optically thin environment, independent previous parcel solver.
 rates=Rates(PREV/'run_refine/results.json')
 previous=parcel(rates,.2,1e9,6e10,3,tol=2e-10)
 now=rad.run(.2,1e9,6e10,3,rtol=2e-9)
 diff=now['molecular_mass_fraction']/previous['molecular_mass_fraction']-1
 assert abs(diff)<.01
 # Independent fast-limit frequency/time refinement at its largest sampled disk value.
 n,*_=environment(.15,1e6,6e10,3)
 fast=FastChemistry(rad,n).run(.15,1e6,6e10,3,rtol=1e-10)
 old=json.loads((BASE/'run_fast/results.json').read_text())['rows'][0]['states'][2]
 fdiff=fast['molecular_mass_fraction']/old['molecular_mass_fraction']-1
 # Stoichiometric check including a photon-mediated DR cycle.
 # Columns X,C,A,T,photon. Rows each forward event.
 sto=np.array([[-1,-1,1,0,1],[-1,0,-1,1,1],[1,1,-1,0,0],[1,0,1,-1,0],[0,-1,2,-1,0]])
 conserved=np.array([[1,0,1,2,0],[0,1,1,1,0],[1,-1,0,1,0]])
 assert not np.any(sto@conserved.T)
 assert np.array_equal(sto[0]-sto[1],sto[4])
 # Energy release of the cycle independent of incoming relative energy.
 cycle_defects=.5-rad.D
 out=dict(thin_previous=previous,thin_dynamic=now,thin_relative_fraction_difference=float(diff),fast_refined=fast,fast_relative_fraction_difference=float(fdiff),stoichiometry=sto.tolist(),conserved_vectors=conserved.tolist(),photon_mediated_DR_heat=cycle_defects.tolist())
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print('thin difference',diff,'fast difference',fdiff,'fast energy',fast['energy_error'])
if __name__=='__main__':main()
