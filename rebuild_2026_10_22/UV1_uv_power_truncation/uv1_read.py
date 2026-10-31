#!/usr/bin/env python3
"""UV1 read-out (FROZEN_CRITERIA.md): same-seed pairs, kick and cut against X48's and ZN1's runs. kappa = 1/2 FITTED; not theory closed."""
import importlib.util, json, math, os, sys
import numpy as np
from scipy.optimize import minimize_scalar as ms
HERE=os.path.dirname(os.path.abspath(__file__)); RB=os.path.dirname(HERE); ZD=os.path.join(RB,"ZN1_zooms_to_z0"); s=importlib.util.spec_from_file_location("zm",os.path.join(ZD,"zn1_measure.py")); Z=importlib.util.module_from_spec(s); sys.argv=["x"]; s.loader.exec_module(Z); XG=Z.XG; OUT=[]; mu=lambda y:np.log1p(y)-y/(1+y); XS=[0.05,0.1,0.2,0.5,1,1.5,2]
def P(t): print(t,flush=True); OUT.append(t)
def zf(f):
    S=np.load(f,allow_pickle=False); me=json.loads(str(S["meta"])); x,m=S["x"],float(S["m"]); rho=me["Mf"]/(4/3*math.pi*me["qM"]**3)*(1+me["zf"])**3; o,r=Z.FIT(x,m,rho,me["eps"]); return dict(cf=o.get("c_f") or o.get("cf"),cn=o.get("c_nfw_fit"),eta=r["S"]["eta"] if r else None)
def z0(f,zs):
    S=np.load(f,allow_pickle=False); me=json.loads(str(S["meta"])); o=Z.measure(S["x"],float(S["m"]),zs,me["eps"]); l=np.array(o["lnm"]); k=(XG>=.05)&(XG<=1); c=ms(lambda c_:float(np.sum((np.log(mu(c_*XG[k])/mu(c_))-l[k])**2)),bounds=(1,40),method="bounded").x; return dict(c=c,lgM=math.log10(o["M200"]),m=[float(np.interp(math.log(x),np.log(XG),l)) for x in XS])
R={}
for v in ("kick","cut"):
    a=[];b=[];c=[]
    for sd in range(1,10):
        A=os.path.join(HERE,"runs_zf",f"{v}_s{sd}","snap_zf.npz"); A0=os.path.join(RB,"X48_native_cf_zoom","runs",f"M1e14_s{sd}_ng64","snap_zf.npz"); B=os.path.join(HERE,"runs",f"{v}_s{sd}","snap_z0.00.npz"); B0=os.path.join(ZD,"runs",f"M1e14_s{sd}_ng64","snap_z0.00.npz")
        if not (os.path.exists(A) and os.path.exists(B)): continue
        p,q=zf(A),zf(A0); a.append((p,q)); b.append((z0(B,0.0),z0(B0,0.0)))
    n=len(a); med=lambda f:float(np.median([f(x) for x in a])); dcn=med(lambda t:math.log(t[0]["cn"]/t[1]["cn"])); de=med(lambda t:math.log(t[0]["eta"]/t[1]["eta"])); adcn=med(lambda t:abs(math.log(t[0]["cn"]/t[1]["cn"]))); ade=med(lambda t:abs(math.log(t[0]["eta"]/t[1]["eta"]))); cf=[t[0]["cf"] for t in a if t[0]["cf"]]; cf0=[t[1]["cf"] for t in a if t[1]["cf"]]; dm=[float(np.median([x[0]["m"][i]-x[1]["m"][i] for x in b])) for i in range(len(XS))]; adm=[float(np.median([abs(x[0]["m"][i]-x[1]["m"][i]) for x in b])) for i in range(len(XS))]; dc=float(np.median([math.log(x[0]["c"]/x[1]["c"]) for x in b])); dM=float(np.median([x[0]["lgM"]-x[1]["lgM"] for x in b]))
    P(f"{v}: {n} pairs. z_f: r_-2 c_f {np.median(cf) if cf else 'n/a'} vs {np.median(cf0) if cf0 else 'n/a'}; NFW c median d ln {dcn:+.3f}, |d ln| {adcn:.3f}; eta_S d ln {de:+.3f}, |d ln| {ade:.3f}. z = 0: c200 d ln {dc:+.3f}, lg M200 {dM:+.3f}; d ln m at x {XS}: "+", ".join(f"{d:+.3f}" for d in dm)+"; median |d ln m|: "+", ".join(f"{d:.3f}" for d in adm))
    R[v]=dict(n=n,cf=float(np.median(cf)) if cf else None,dcn=dcn,adcn=adcn,de=de,ade=ade,dc=dc,dM=dM,dm=dm,adm=adm)
K=R["kick"]; vk="ARGON'S SPIKE CONFIRMED" if K["cf"] and 4.5<=K["cf"]<=5.5 else "NO EFFECT" if K["adcn"]<=.05 and K["ade"]<=.05 else "PARTIAL"; C=R["cut"]; vc="UV-SENSITIVE" if max(C["adm"][1],C["adm"][2])>.10 else "UV-INSENSITIVE"; P(f"VERDICT kick: {vk}. cut: {vc}.")
json.dump(R,open(os.path.join(HERE,"uv1_results.json"),"w"),indent=1); open(os.path.join(HERE,"uv1.out"),"w").write("\n".join(OUT)+"\n")
