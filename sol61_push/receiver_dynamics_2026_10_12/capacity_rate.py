from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
rows=[]
for H0 in [1.,2.,4.,8.,16.]:
    scan=[]
    for b in np.geomspace(.01,100,25):
        def f(t,z):
            q,x,p=z; y=1-q
            return [2*H0*b*p*p*y,p,-x-b*p*y]
        def stop(t,z): return z[0]-.9
        stop.terminal=True; stop.direction=1
        sol=solve_ivp(f,(0,max(5000.,100/b)),[0,1,0],method="Radau",rtol=1e-9,atol=1e-11,events=stop,dense_output=True)
        assert sol.success and len(sol.t_events[0])==1
        t=float(sol.t_events[0][0]); q,x,p=sol.sol(np.linspace(0,t,201))
        err=float(np.max(np.abs(q/H0+x*x+p*p-1)))
        assert err<=1e-7
        scan.append({"b":float(b),"omega_t90":t,"energy_error":err})
    best=min(scan,key=lambda r:r["omega_t90"])
    omega=5.78881*9.36e-11/299792458.
    rows.append({"capacity":H0,"best_sampled":best,"conditional_best_Gyr":best["omega_t90"]/omega/(365.25*86400)/1e9,"scan":scan})
result={"rows":rows,"scope":"Finite normalized receiver scan. No derived capacity, mobility or halo selector; minima are within sampled rates only."}
Path(__file__).with_name("capacity_rate_run").joinpath("results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps([{k:v for k,v in r.items() if k!="scan"} for r in rows],indent=2))
