import argparse,json,subprocess,sys,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);base=Path(__file__).resolve().parent
result={}
for label in ['multipole15','corrected20']:
    temp=Path(tempfile.mkdtemp(prefix='continuum-scan-',dir='/private/tmp'))/'work'
    dest=out.parent/label/'results.json'
    subprocess.run([sys.executable,str(base/'scan_energies.py'),'--input',str(base/('run_'+label)),'--work',str(temp),'--bin','/private/tmp/ukrmol-build/build/bin','--output',str(dest)],check=True)
    result[label]=json.loads(dest.read_text())
result['physical_DR_rates_derived']=False
out.write_text(json.dumps(result,indent=2)+'\n')
