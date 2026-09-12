import argparse
import subprocess
import sys
from run_bounded import ROOT,HERE,SKILL,INPUTS,relative

parser=argparse.ArgumentParser()
parser.add_argument('--name',required=True)
parser.add_argument('--step',type=float,default=.025)
args=parser.parse_args()
output=HERE/args.name
source=HERE/'scan_001/result.json'
command=[sys.executable,str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),
         '--contract',relative(HERE/'early_contract.json'),'--output',relative(output),
         '--timeout','420','--max-output-bytes','1048576','--max-threads','1']
for path in INPUTS+[HERE/'early_extension.py',HERE/'early_contract.json',HERE/'run_early.py',source]:
    command+=['--input',relative(path)]
command+=['--result',relative(output/'result.json'),'--',sys.executable,'-B',
          relative(HERE/'early_extension.py'),'--source',relative(source),
          '--result-file',relative(output/'result.json'),'--step',str(args.step)]
print('EXECUTION ARGV:',repr(command),flush=True)
result=subprocess.run(command,cwd=ROOT)
print('EXPERIMENT EXIT:',result.returncode,flush=True)
if result.returncode:
    raise SystemExit(result.returncode)
result=subprocess.run([sys.executable,str(SKILL/'scripts/validate_manifest.py'),
                       str(output/'manifest.json'),'--root',str(ROOT)],cwd=ROOT)
print('MANIFEST VALIDATION EXIT:',result.returncode,flush=True)
raise SystemExit(result.returncode)
