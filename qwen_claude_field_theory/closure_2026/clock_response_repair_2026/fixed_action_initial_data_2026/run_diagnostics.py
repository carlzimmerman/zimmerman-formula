import subprocess
import sys
from run_bounded import ROOT,HERE,SKILL,INPUTS,relative
source=HERE/'early_002/result.json'
output=HERE/'diagnostics_001'
command=[sys.executable,str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),
         '--contract',relative(HERE/'diagnostics_contract.json'),'--output',relative(output),
         '--timeout','180','--max-output-bytes','1048576','--max-threads','1']
for path in INPUTS+[HERE/'diagnostics.py',HERE/'run_diagnostics.py',HERE/'diagnostics_contract.json',
                   source,HERE.parent/'cosmological_bridge_2026/radiation_002/result.json']:
    command+=['--input',relative(path)]
command+=['--result',relative(output/'result.json'),'--',sys.executable,'-B',relative(HERE/'diagnostics.py'),
          '--source',relative(source),'--result-file',relative(output/'result.json')]
print('EXECUTION ARGV:',repr(command),flush=True)
result=subprocess.run(command,cwd=ROOT)
print('EXPERIMENT EXIT:',result.returncode,flush=True)
if result.returncode:
    raise SystemExit(result.returncode)
result=subprocess.run([sys.executable,str(SKILL/'scripts/validate_manifest.py'),
                       str(output/'manifest.json'),'--root',str(ROOT)],cwd=ROOT)
print('MANIFEST VALIDATION EXIT:',result.returncode,flush=True)
raise SystemExit(result.returncode)
