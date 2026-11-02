import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
import an1_v3 as v,json
for N in (300,1200): print(N,json.dumps(v.K12(N=N)),flush=True)
