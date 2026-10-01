from pathlib import Path
import json,time,subprocess,sys
here=Path(__file__).resolve().parent
watch=here/'runs/XR36_web_lensing_MUTATE/provenance.json'
start=time.time()
while time.time()-start<1800:
 if watch.exists() and json.loads(watch.read_text()).get('status') not in ('running',None):
  raise SystemExit(subprocess.call([sys.executable,str(here/'run_one.py'),'XR36_web_lensing','main','verified']))
 time.sleep(2)
raise SystemExit('original web mutation did not finish within queue bound')
