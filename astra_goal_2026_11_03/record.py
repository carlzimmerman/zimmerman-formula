"""Small-run evidence recorder. No imports or writes outside the AZ tree."""
import hashlib,json,platform,subprocess,time
from pathlib import Path
import numpy as np
import scipy
DISCLAIMER='κ = ½ FITTED; not theory closed'
def record(script, calculate, extra_inputs=()):
    script=Path(script).resolve(); here=script.parent; root=Path(__file__).resolve().parent.parent
    output=here/'results.json'  # declared before calculate is invoked
    artifacts=[script,here/'CRITERIA.md',Path(__file__).resolve()]+[root/p for p in extra_inputs]
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    hashes={str(p.relative_to(root)):digest(p) for p in artifacts}
    revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    started=time.time();result=calculate();result['disclaimer']=DISCLAIMER
    output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    manifest={'schema_version':2,'claim_id':here.name.split('_')[0],'repository':{'commit':revision,'dirty':True},'command':['python3',str(script.relative_to(root))],'environment':{'software':[{'name':'Python','version':platform.python_version()},{'name':'numpy','version':np.__version__},{'name':'scipy','version':scipy.__version__}],'hardware':platform.machine()},'mathematics':{'assertion_tested':result['assertion_tested'],'coefficient_domain':'float64 unless exact algebra explicitly stated','conventions':'see CRITERIA.md','inputs':list(hashes),'bounds':result.get('bounds',{}),'non_claims':result.get('non_claims',['No uncomputed empirical row passes'])},'randomness':{'used':False,'generator':'','seed':None},'run':{'started_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(started)),'runtime_seconds':time.time()-started,'exit_status':0,'status':'completed','resource_limits':{'memory_bytes':None,'cpu_seconds':None,'max_cores':None,'max_threads':None}},'outputs':[{'path':str(output.relative_to(root)),'sha256':digest(output),'kind':'result'}],'checks':result.get('checks',[]),'result':result['label'],'residual_risks':result.get('residual_risks',[]),'input_artifacts':[{'path':p,'sha256':h,'sha256_after':digest(root/p)} for p,h in hashes.items()],'declared_results':[str(output.relative_to(root))]}
    (here/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(result,indent=2))
