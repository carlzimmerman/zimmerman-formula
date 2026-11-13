#!/usr/bin/env python3
"""Independent read-only boundary/unit/convolution checks for gas_corrections."""
import hashlib,importlib.util,json,math,sys
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy.integrate import quad

lane=Path(__file__).resolve().parent
target=lane.parent/'gas_corrections/corrected_signal.py'
before=hashlib.sha256(target.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('gas_under_audit',target)
gas=importlib.util.module_from_spec(spec);spec.loader.exec_module(gas)
checks=[]
def check(name,ok,value):
    checks.append(dict(name=name,passed=bool(ok),measurement=value))
    print(('PASS' if ok else 'FAIL')+' '+name+': '+str(value),flush=True)

# Independent dimensionless shell integrations include both radial boundaries.
shell=[]
for a0 in gas.A0.values():
    R=2.6*gas.MPC; ri=gas.budget_radius(a0); sigma=gas.Sigma(a0)
    for b in [0.,.999*ri,ri,1.001*ri,.3*gas.MPC,.999*R,R,1.01*R]:
        if b>=R: col=em=0.
        else:
            zhi=math.sqrt(R*R-b*b); zlo=math.sqrt(max(0,ri*ri-b*b))
            # Physical columns integrated in scaled z to retain accuracy in SI.
            col=2*quad(lambda t:(sigma/(2*math.sqrt(b*b+(t*R)**2)))*R,
                       zlo/R,zhi/R,epsabs=1e-12,epsrel=1e-10)[0]
            em=2*quad(lambda t:gas.XH/gas.MUE*(sigma/(2*gas.MP))**2
                      /(b*b+(t*R)**2)*R*1e-10,zlo/R,zhi/R,epsabs=1e3,epsrel=1e-10)[0]
        expected_col=gas.N_e_m(b,a0,R)*gas.MUE*gas.MP
        expected_em=gas.EM(b,a0,R)
        errc=abs(expected_col-col)/max(abs(col),1e-100)
        erre=abs(expected_em-em)/max(abs(em),1e-100)
        shell.append(max(errc,erre))
    # At and inside Rin the compact mass is counted once and gas mass is zero.
    check('shell zero gas interior '+str(a0),gas.M_req(.5*ri,a0)==0 and
          abs(gas.M_req(ri,a0))<1e-14*gas.MBST*gas.MSUN,
          dict(M_inside=gas.M_req(.5*ri,a0),M_at_inner=gas.M_req(ri,a0)))
    for s in [1.001,2.,R/ri]:
        outer=s*ri
        mass=quad(lambda t:4*math.pi*(ri*t)**2*float(gas.rho_A(ri*t,a0))*ri,
                  1.,s,epsabs=0,epsrel=1e-10)[0]
        check('shell volume mass '+str(a0)+' '+str(s),abs(mass/gas.M_req(outer,a0)-1)<1e-10,
              abs(mass/gas.M_req(outer,a0)-1))
check('LOS and EM at inner and outer edges',max(shell)<1e-9,max(shell))

# Independent 2D angular integral for a smooth compact radial source.
# The kernel is reconstructed from Euclidean distance, not i0/i0e.
sigma=.7
def source(b): return (1-b*b/4)**2 if 0<=b<2 else 0.
grid=np.linspace(0,8,4001); inp=np.array([source(b) for b in grid])
conv=gas.smear(grid,inp,sigma*math.sqrt(8*math.log(2)))
beam_errors=[]
for R in [0.,.5,1.,2.,3.]:
    def radial(b):
        angular=quad(lambda phi:math.exp(-(R*R+b*b-2*R*b*math.cos(phi))/(2*sigma*sigma)),
                     0.,2*math.pi,epsabs=1e-11,epsrel=1e-11)[0]
        return b*source(b)*angular/(2*math.pi*sigma*sigma)
    independent=quad(radial,0.,2.,epsabs=1e-11,epsrel=1e-11)[0]
    got=float(np.interp(R,grid,conv))
    beam_errors.append(abs(got-independent))
flux_in=2*math.pi*quad(lambda r:r*source(r),0,2,epsabs=1e-12)[0]
flux_out=float(2*math.pi*np.trapz(grid*conv,grid))
check('beam versus direct 2D angular convolution',max(beam_errors)<1e-6,max(beam_errors))
check('beam conserves full-plane compact-source flux on large domain',abs(flux_out/flux_in-1)<2e-6,flux_out/flux_in-1)
check('SI to cgs flux scales as inverse distance squared',
      gas.xray_flux_cgs(1.,2.)==gas.xray_flux_cgs(1.,1.)/4,
      gas.xray_flux_cgs(1.,1.))
z=1e-6
ratio=gas.D_A(z)/(299792.458/67.4*gas.MPC*z)
check('angular diameter distance has correct small-redshift units',abs(ratio-1)<2e-6,ratio)
after=hashlib.sha256(target.read_bytes()).hexdigest()
check('audited source unchanged during checks',before==after,after)
result=dict(source=str(target.relative_to(lane.parent)),source_sha256=before,
            checks=checks,all_pass=all(x['passed'] for x in checks),
            scope='Shell realization, projection/EM, convolution, units; no observational significance or unique gas-profile inference')
(lane/'gas_independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
if not result['all_pass']:raise SystemExit(1)
