"""Audit finite-rate/photon interface; manufactured rates are NOT physics data."""
import argparse,json,sys,unittest,io
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'recycling'))
from photons import Radiation,PROFILES,environment
from coupling import thermal_loss,collision_source,couple

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    suite=unittest.defaultTestLoader.discover(str(HERE),pattern='test_*.py')
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream).run(suite)
    print(stream.getvalue());assert result.wasSuccessful()
    rad=Radiation(order=3);mu=201/202
    # Artificial maximal loss in ONE incoming block, used solely as a fixture.
    # It is not a computed S matrix or a total physical cross section.
    fixture=lambda T:np.full(rad.nb,np.sqrt(2*np.pi)/mu**1.5/np.sqrt(T))
    fun,env=couple(rad,.2,1e7,*PROFILES[2],fixture,closed=True)
    base,_=rad.system(.2,1e7,*PROFILES[2],closed=True)
    zero,_=couple(rad,.2,1e7,*PROFILES[2],lambda T:np.zeros(rad.nb),closed=True)
    y=np.zeros(rad.nm+rad.nq+1);y[0]=.2;y[1:rad.nb+1]=.1/rad.nb
    y[rad.nm-1]=1.5*(1+.6)*.02
    assert np.array_equal(zero(y),base(y))
    direction=np.sin(np.arange(len(y))+1);direction[rad.nm-1]*=.01
    # Scale photon perturbation to avoid derivative cancellation of huge occupations.
    direction[rad.nm:]*=1e-8
    h=1e-7;fd=(fun(y+h*direction)-fun(y-h*direction))/(2*h)
    analytic=fun(y,True)@direction
    jac_error=np.linalg.norm(fd-analytic)/np.linalg.norm(fd)
    assert jac_error<2e-6,jac_error
    tmax=1e-9
    sol=solve_ivp(lambda t,y:fun(y),(0,tmax),y,method='BDF',jac=lambda t,y:fun(y,True),rtol=2e-9,atol=1e-14)
    assert sol.success,sol.message
    aa=sol.y[0];tt=sol.y[1:rad.nb+1];x=1-aa-2*tt.sum(axis=0);c=1-aa-tt.sum(axis=0)
    energy=sol.y[rad.nm-1]-.5*aa-(.5+rad.D)@tt+rad.omega@sol.y[rad.nm:rad.nm+rad.nq]+sol.y[-1]
    charge=x+tt.sum(axis=0)-c
    energy_error=float(max(abs(energy-energy[0])));charge_error=float(max(abs(charge)))
    assert energy_error<1e-10 and charge_error<1e-12
    assert min(np.min(aa),np.min(tt),np.min(x),np.min(c))>-1e-10
    validity=[]
    for Mb,b in PROFILES:
        n,T,L,age=environment(.2,1e7,Mb,b)
        # E=3T/2 is just a representative thermal energy, not a distribution bound.
        eta=np.sqrt(mu/(3*T));sommerfeld=2*np.pi*eta/(-np.expm1(-2*np.pi*eta))
        validity.append(dict(Mb=Mb,b=b,initial_T=T,representative_eta=float(eta),coulomb_origin_enhancement=float(sommerfeld),one_block_unit_loss_optical_depth=float(age*n*np.sqrt(2*np.pi)/mu**1.5/np.sqrt(T))))
    out=dict(unit_tests=result.testsRun,jacobian_relative_error=float(jac_error),manufactured_photon_collision_test=dict(physical_rate=False,energy_error=energy_error,charge_error=charge_error,nfev=sol.nfev,end_age_fraction=tmax,initial_molecular_fraction=float(201/101*.1),final_molecular_fraction=float(201/101*sum(tt[:,-1]))),born_validity_at_shared_point=validity,physical_finite_rate_halo_runs=0)
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
