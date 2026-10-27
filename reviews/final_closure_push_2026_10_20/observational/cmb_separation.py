#!/usr/bin/env python3
"""Post hoc power diagnostic on frozen CFG917 vectors; never changes a class."""
import sys
sys.dont_write_bytecode = True
import hashlib, json, math, os, pathlib, resource, statistics, time

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(sys.argv[1]).resolve()
EXT = ROOT.parent / "_external_data"
PR4 = EXT / "cmb_lensing_raw/planck_PR4_lensing/planckpr4lensing/data_pr4"
STEM = "pp_consext8_npipe_smicaed_TiPi_jTP_pre30T_kfilt_rdn0cov_PS1"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def table(p):
    return [[float(x) for x in line.split()] for line in p.read_text().splitlines() if line.strip() and not line.lstrip().startswith("#")]
def dot(a, b): return math.fsum(x*y for x,y in zip(a,b))
def sub(a, b): return [x-y for x,y in zip(a,b)]
def chol(C):
    n = len(C); L = [[0.0]*n for _ in C]
    for i in range(n):
        for j in range(i+1):
            v=C[i][j]-math.fsum(L[i][k]*L[j][k] for k in range(j))
            L[i][j] = math.sqrt(v) if i==j else v/L[j][j]
    return L
def whiten(L, a):
    y=[]
    for i in range(len(a)): y.append((a[i]-math.fsum(L[i][j]*y[j] for j in range(i)))/L[i][i])
    return y
def solve(C, b):
    """Independent partial-pivot Gaussian elimination, for a q-form cross-check."""
    a=[list(r)+[x] for r,x in zip(C,b)]; n=len(b)
    for j in range(n):
        k=max(range(j,n),key=lambda k:abs(a[k][j]));a[j],a[k]=a[k],a[j]
        for i in range(j+1,n):
            f=a[i][j]/a[j][j]
            for k in range(j,n+1):a[i][k]-=f*a[j][k]
    x=[0.0]*n
    for j in range(n-1,-1,-1):x[j]=(a[j][-1]-dot(a[j][j+1:n],x[j+1:n]))/a[j][j]
    return x

t0=time.time()
paths=[PR4/(STEM+"_CMBmarged_cov.dat"),PR4/(STEM+"_CMBmarged_lensing_fiducial_correction.dat"),PR4/(STEM+"_bandpowers.dat")]
paths += [ROOT/f"campaign_fresh_gravity/CFG917_cmb_lensing_gate/cfg917_{p}.json" for p in ("NC1x","T1x","T2x")]
before={str(p):sha(p) for p in paths}
C=table(paths[0]); offset=[r[1] for r in table(paths[1])]; data=[r[4] for r in table(paths[2])]
assert len(C)==len(offset)==len(data)==9
assert max(abs(C[i][j]-C[j][i]) for i in range(9) for j in range(9)) < 1e-20
L=chol(C); wd=whiten(L,[x+y for x,y in zip(data,offset)])
R={"status":"post_hoc_diagnostic_only", "pairs":{}, "derivation":"delta=F-S; q=delta^T C^-1 delta. Under d~N(S,C), D=chi2(F)-chi2(S)~N(q,4q); under F mean=-q. Shape separation projects delta orthogonally to the uncorrected S template u_S=B_S+F_fid in the C^-1 metric. Free amplitude B(A)=A*u-F_fid.", "non_claims":["No new frozen class or theorem-level closure","Fixed Gaussian covariance and fixed stored templates only","Primary-only threshold probabilities are upper bounds for the full robust exclusion rule","No extrapolation beyond stored box-supported models"]}
normal=statistics.NormalDist()
for pair,p in zip(("NC1x","T1x","T2x"),paths[3:]):
    raw=json.loads(p.read_text()); r=raw["primary"]; F=r["B_F"]; S=r["B_S0"]
    assert max(abs(x-y) for x,y in zip(data,r["d"]))==0
    delta=sub(F,S); wdelta=whiten(L,delta); q=dot(wdelta,wdelta)
    q_ind=dot(delta,solve(C,delta));assert abs(q-q_ind)<1e-13
    fit={}
    for name,v in (("F",F),("S0",S)):
        resid=whiten(L,sub(v,data));ch=dot(resid,resid)
        assert abs(ch-r["chi2_"+name])<1e-9
        u=whiten(L,[x+y for x,y in zip(v,offset)]);aa=dot(u,wd)/dot(u,u)
        rr=sub(wd,[aa*x for x in u]);chfree=dot(rr,rr)
        assert abs(aa-r["A_"+name][0])<1e-10
        fit[name]={"chi2_reproduced":ch,"amplitude":aa,"amplitude_sigma":1/math.sqrt(dot(u,u)),"chi2_free_amplitude":chfree}
    us=whiten(L,[x+y for x,y in zip(S,offset)])
    projection=dot(wdelta,us)/dot(us,us);orth=sub(wdelta,[projection*x for x in us]);qp=dot(orth,orth)
    assert 0<=qp<=q*(1+1e-10)
    tail=lambda x:0.5*math.erfc(x/math.sqrt(2))
    R["pairs"][pair]={"inputs":raw["inputs"],"foot":raw["foot"],"class_frozen":raw["class"],"q_full":q,"sqrt_q":math.sqrt(q),"q_after_profiled_amplitude":qp,"sqrt_q_shape":math.sqrt(qp),"fraction_q_parallel_to_amplitude":1-qp/q,"amplitude_projection_delta":projection,"prob_primary_D_ge_4_if_S0_true":tail((4-q)/(2*math.sqrt(q))),"prob_primary_D_ge_9_if_S0_true":tail((9-q)/(2*math.sqrt(q))),"power_one_sided_3sigma_optimal_simple_test":tail(3-math.sqrt(q)),"fits":fit,"observed_free_amplitude_dchi2":fit["F"]["chi2_free_amplitude"]-fit["S0"]["chi2_free_amplitude"],"observed_original_dchi2":r["dchi2"],"coverage":raw["coverage"]}
after={str(p):sha(p) for p in paths};assert after==before
R.update(input_hashes_before=before,input_hashes_after=after,runtime_seconds=time.time()-t0,python=sys.version,maxrss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
assert R["maxrss_bytes"]<1_000_000_000
OUT.write_text(json.dumps(R,indent=2)+"\n")
for k,v in R["pairs"].items():print(k,"sqrt(q)",v["sqrt_q"],"shape",v["sqrt_q_shape"],"amplitude q fraction",v["fraction_q_parallel_to_amplitude"],"free-A observed dchi2",v["observed_free_amplitude_dchi2"])
