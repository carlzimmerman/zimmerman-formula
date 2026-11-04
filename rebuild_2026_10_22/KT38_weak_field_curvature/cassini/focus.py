"""New explicitly authorized lengths; unchanged full Cassini implementation."""
import argparse,json,math,time
from pathlib import Path
import calculate as C


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    started=time.monotonic();previous=C.HERE/'run_001/results.json'
    controls=json.loads(previous.read_text());assert controls['all_checks_pass']
    api=C.api_checks();assert api['passed']
    result=dict(law=controls['law'],physical_lengths_kpc=[1.5,1.75,2.,2.25,2.5],
        unchanged_controls_from=str(previous.relative_to(C.RB.parent)),
        api_check=api,footings={},checks={})
    for foot,a0 in C.old.A0.items():
        eta=C.old.GEXT/a0;rm=math.sqrt(C.old.GM/a0);rows={};result['footings'][foot]=rows
        for length in result['physical_lengths_kpc']:
            ell=length*C.KPC/rm
            base=C.prior.physical(C.quadrupole(eta,ell),a0)
            fine=C.prior.physical(C.quadrupole(eta,ell,nr=16000,nm=320,rmin=1e-10,rmax=1e7),a0)
            rows[str(length)]=dict(base=base,fine=fine)
            scale=max(abs(fine['q_signed']),1e-12)
            result['checks'][foot+f'|{length}|refinement']=abs(base['q_signed']-fine['q_signed'])/scale<2e-4
            result['checks'][foot+f'|{length}|density']=abs(fine['flux_density_difference'])/scale<2e-4
            print(foot,length,'qA',fine['q_A_flux'],'qB',fine['q_B_flux'],'q',fine['q_signed'],'ratio',fine['x_ceiling'],'densitydiff',fine['flux_density_difference'],flush=True)
    result['all_checks_pass']=all(result['checks'].values())
    result['runtime_seconds']=time.monotonic()-started
    result['outcome']='new finite physical lengths; shared full variation and previously validated origin controls, no continuous-length theorem'
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n')
    if not result['all_checks_pass']:raise SystemExit(1)


if __name__=='__main__':main()
