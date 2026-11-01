import sys
sys.dont_write_bytecode=True
import json,time,resource
from pathlib import Path
import mpmath as mp
from native_states import setup,gas_point,eigen,bisect
mp.mp.dps=50

def main(path):
    start=time.monotonic();out=[]
    for ee in ('.03','.1'):
        e,c,g,U,d,x0=setup(ee)
        comp=bisect(lambda r:gas_point(x0*r,e,U,d,x0)[4],mp.mpf('1.01'),mp.mpf('1.05'),60)
        radial=bisect(lambda r:mp.mpf(gas_point(x0*r,e,U,d,x0)[0]['D']),mp.mpf('1.5'),mp.mpf('1.8'),60)
        b=gas_point(x0*comp,e,U,d,x0);r=mp.mpf('1.01');base=gas_point(x0*r,e,U,d,x0);delta=mp.mpf('1e-5');plus=gas_point(x0*r*mp.exp(delta),e,U,d,x0);minus=gas_point(x0*r*mp.exp(-delta),e,U,d,x0);direct=(plus[2]-minus[2])/(2*delta)
        m,ms,*_=eigen(x0*r,e);p=base[1];EF=mp.sqrt(p*p+m*m);expected=-mp.mpf(base[0]['D'])*EF/(m*ms)
        out.append(dict(e=ee,compressibility_boundary_ratio=str(comp),radial_end_ratio=str(radial),compressibility_boundary=b[0],boundary_scaled_n=str(b[2]/c**mp.mpf('1.5')),boundary_scaled_pF=str(b[1]/mp.sqrt(c)),dn_ds_direct=str(direct),dn_ds_identity=str(expected),dn_ds_relative_error=str(abs(direct/expected-1))))
        print(json.dumps(out[-1],indent=2),flush=True)
    checks={'two_boundary_cases':len(out)==2,'density_identity_error_below_1e-6':max(mp.mpf(o['dn_ds_relative_error']) for o in out)<mp.mpf('1e-6'),'scaled_density_match_below_1e-30':abs(mp.mpf(out[0]['boundary_scaled_n'])/mp.mpf(out[1]['boundary_scaled_n'])-1)<mp.mpf('1e-30'),'same_boundary_ratio':out[0]['compressibility_boundary_ratio']==out[1]['compressibility_boundary_ratio']}
    result=dict(claim_id='TP02_EIGENMODE_GAS_BOUNDARIES',checks=checks,cases=out,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,non_claims=['No exact number/current or stable adjoint particle abundance','No gauge-singlet/IR matching or lifetime','No RG-improved occupied mass spectrum, halo or gravity model'])
    Path(path).write_text(json.dumps(result,indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
