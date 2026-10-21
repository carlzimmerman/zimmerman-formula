#!/usr/bin/env python3
"""Post hoc KiDS shape diagnostic: profile a common form of positive amplitude in both arms."""
import sys
sys.dont_write_bytecode=True
import os
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","VECLIB_MAXIMUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[v]="1"
os.environ["CFG596_MUTATE"]="0"
import hashlib, importlib.util, json, pathlib, resource, time, warnings
import numpy as np
import scipy
from scipy.optimize import minimize

ROOT=pathlib.Path(__file__).resolve().parents[3]
HERE=pathlib.Path(__file__).resolve().parent
OUT=pathlib.Path(sys.argv[1]).resolve()
EXT=ROOT.parent/"_external_data"
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1048576),b""):h.update(b)
    return h.hexdigest()
def loadmod(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

t0=time.time()
inventory=json.loads((HERE/"external_inputs.json").read_text())
before={p:sha(pathlib.Path(p)) for p in inventory["shear"]}
assert before==inventory["shear"]
mod=loadmod("review_cfg654",ROOT/"campaign_fresh_gravity/CFG654_independent_inputs/cfg654_native.py")
G=mod.load_lib("native_cmb")
F=json.loads(next((EXT/"cfg654_work/NC1x").glob("*_RES_*.json")).read_text())
S=json.loads(next((EXT/"cfg654_work/NCS0").glob("*_S0_*.json")).read_text())
run,_=mod.build(F,S,int(F["np"]),float(F["L"]),F["foot"],"review_NC1x")
Ps={"F":G["Pmat"](run,"F"),"S0":G["Pmat"](run,"S0")}
Sv=G["SURV"]["KiDS"];keep=Sv["pubkeep"]&(G["support_mask"](Sv,run,Ps["S0"])>=.9);D=G["subset"](Sv,keep)
ref=json.loads((ROOT/"campaign_fresh_gravity/CFG654_independent_inputs/cfg654_native_results_NC1x.json").read_text())["surveys"]["KiDS"]
assert D["N"]==ref["N_kept"]==108
x0,lo,hi,unpack,prior=G["nuis_spec"](Sv,1.0,True)
bounds=list(zip(lo,hi));Cinv=D["Cinv"];data=D["d"]

def evaluate(x,P,free):
    t=G["theory"](Sv,D,unpack(x),P,"PM")
    den=float(t@Cinv@t);a=max(0.0,float(t@Cinv@data)/den) if free else 1.0
    r=data-a*t;cd=float(r@Cinv@r)
    return cd+prior(x),a,cd,t

result={"status":"post_hoc_diagnostic_only","pair":"NC1x_vs_NCS0","foot":"canonical","N_kept":D["N"],"amplitude_definition":"t(A,x)=A*t_frozen(x), A>=0 unpenalized, profiles total GG+GI+II shear together; same nuisance priors and cuts in both arms","non_claims":["Not a self-consistent cosmology fit","No changed frozen rule or revised pass/fail class","No significance assigned to the fitted-model delta chi-square","A>=0 adds a parameter only to this diagnostic"],"arms":{}}
for arm in ("S0","F"):
    fixed=G["fit"](Sv,D,Ps[arm]);target=ref["chi2_"+arm]
    assert abs(fixed["chi2"]-target)<1e-6,(arm,fixed["chi2"],target)
    assert abs(evaluate(np.array(fixed["x"]),Ps[arm],False)[0]-target)<1e-6
    starts=[np.array(fixed["x"]),x0.copy(),np.r_[x0[:-1],-.5]]
    fits=[]
    for i,xs in enumerate(starts):
        rr=minimize(lambda x:evaluate(x,Ps[arm],True)[0],xs,method="L-BFGS-B",bounds=bounds,options=dict(maxiter=400,ftol=1e-12,gtol=1e-8))
        value,a,cd,t=evaluate(rr.x,Ps[arm],True)
        fits.append(dict(start=i,chi2=value,chi2_data=cd,amplitude=a,x=rr.x.tolist(),success=bool(rr.success),message=str(rr.message),nfev=int(rr.nfev),nit=int(rr.nit)))
    best=min(fits,key=lambda x:x["chi2"])
    assert best["chi2"]<=fixed["chi2"]+1e-7
    xx=np.array(best["x"]);f1=evaluate(xx,Ps[arm],True);f2=evaluate(xx,Ps[arm]*1.1,True)
    assert abs(f1[0]-f2[0])<1e-9 and abs(f1[1]/1.1-f2[1])<1e-10
    result["arms"][arm]={"fixed_chi2_reproduced":fixed["chi2"],"fixed_chi2_data":fixed["chi2_data"],"fixed_A_IA":fixed["A_IA"],"profiled":best,"starts":fits,"uniform_power_rescaling_invariance_abs_diff":abs(f1[0]-f2[0])}
    print(arm,"frozen chi2",fixed["chi2"],"profiled",best["chi2"],"A",best["amplitude"],"all starts",[(f["chi2"],f["success"]) for f in fits],flush=True)

result["dchi2_fixed"]=ref["dchi2"]
result["dchi2_profiled_amplitude"]=result["arms"]["F"]["profiled"]["chi2"]-result["arms"]["S0"]["profiled"]["chi2"]
result["removed_advantage_fraction"]=1-result["dchi2_profiled_amplitude"]/ref["dchi2"]
after={p:sha(pathlib.Path(p)) for p in inventory["shear"]};assert after==before
result.update(external_input_hashes_before=before,external_input_hashes_after=after,runtime_seconds=time.time()-t0,python=sys.version,numpy=np.__version__,scipy=scipy.__version__,maxrss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
assert result["maxrss_bytes"]<1_000_000_000
OUT.write_text(json.dumps(result,indent=2)+"\n")
print("post hoc amplitude-profiled dchi2",result["dchi2_profiled_amplitude"],"removed fraction",result["removed_advantage_fraction"],flush=True)
