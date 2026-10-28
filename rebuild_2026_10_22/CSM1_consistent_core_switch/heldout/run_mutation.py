#!/usr/bin/env python3
"""CSM1 actual-input BS1 MW/dwarf rerun; no historical lane writes."""
import argparse, ast, builtins, contextlib, hashlib, io, json, math, os, platform, resource, subprocess, sys, time
from pathlib import Path
for k in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","VECLIB_MAXIMUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"): os.environ[k]="1"
for k in list(os.environ):
    if k.endswith("_MUTATE"): os.environ.pop(k)
import numpy as np
import scipy
from scipy import stats
from scipy.optimize import brentq
HERE=Path(__file__).resolve().parent; REB=HERE.parents[1]; ROOT=REB.parent
AP=argparse.ArgumentParser(); AP.add_argument("--output",type=Path,required=True); AP.add_argument("--mutate",action="store_true"); args=AP.parse_args()
args.output=args.output.resolve(); args.output.mkdir(parents=True,exist_ok=True)
DECLARED_NAMES=("results.json","baseline.json","sigma_table.json","firstcell.json","cell_3.9.json","cell_4.0.json","resources.json","executed_ho2_source.py","executed_x51_source.py")
START=time.time(); READS={}; real_open=builtins.open
sys.dont_write_bytecode=True

def sha(p):
    with real_open(p,"rb") as fh: return hashlib.sha256(fh.read()).hexdigest()
def watched_open(file, mode="r",*a,**kw):
    if isinstance(file,(str,bytes,os.PathLike)):
        p=Path(file).resolve()
        if any(c in mode for c in "wax+"):
            if not p.is_relative_to(HERE): raise RuntimeError("Historical/out-of-scope write refused: "+str(p))
        elif p.is_relative_to(ROOT) and p.is_file(): READS.setdefault(str(p.relative_to(ROOT)),sha(p))
    return real_open(file,mode,*a,**kw)
builtins.open=watched_open
AUDIT_BUSY=False
def audit_io(event,event_args):
    global AUDIT_BUSY
    if event!="open" or AUDIT_BUSY or not isinstance(event_args[0],(str,bytes,os.PathLike)): return
    p=Path(os.fsdecode(event_args[0])).resolve(); mode=event_args[1]; flags=event_args[2]
    writing=(isinstance(mode,str) and any(c in mode for c in "wax+")) or (isinstance(flags,int) and bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)))
    if writing:
        if p.is_relative_to(ROOT) and not p.is_relative_to(HERE): raise RuntimeError("Audit refused historical write: "+str(p))
        return
    if p.is_relative_to(ROOT) and not p.is_relative_to(args.output) and p.is_file():
        AUDIT_BUSY=True
        try:
            READS.setdefault(str(p.relative_to(ROOT)),sha(p))
            if p.suffix==".pyc" and p.parent.name=="__pycache__":
                source=p.parent.parent/(p.name.split(".")[0]+".py")
                if source.is_file(): READS.setdefault(str(source.relative_to(ROOT)),sha(source))
        finally: AUDIT_BUSY=False
sys.addaudithook(audit_io)
READS[str(Path(__file__).resolve().relative_to(ROOT))]=sha(__file__)
# pathlib reads do not call builtins.open: scientific sources use this helper.
def read(p):
    with open(p) as fh: return fh.read()
def load(p):
    with open(p) as fh: return json.load(fh)
def save(p,obj):
    with open(p,"w") as fh: json.dump(obj,fh,indent=2,sort_keys=True,allow_nan=False,default=lambda x:x.item() if isinstance(x,np.generic) else x.tolist() if isinstance(x,np.ndarray) else str(x)); fh.write("\n")
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform=="darwin" else 1e6)
def emit(s): print(s,flush=True)
def patch(src,old,new):
    assert src.count(old)==1,(old[:90],src.count(old)); return src.replace(old,new)
def call_readonly(src_path,edits=(),cut=None,extra=None):
    src=read(src_path)
    if cut: src=src[:src.index(cut)]
    for old,new in edits: src=patch(src,old,new)
    ns={"__file__":str(src_path),"__name__":"csm1_readonly"}; ns.update(extra or {})
    argv=sys.argv; sys.argv=[str(src_path)]
    try:
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            try: exec(compile(src,str(src_path),"exec"),ns)
            except SystemExit: pass
    finally: sys.argv=argv
    return ns
# Original BS1 prefix only: exact data/geometry/membership, no SPARC or scoring.
BS=read(REB/"BS1_basin_switch/bs1_basin_switch.py")
LGsrc=BS[:BS.index("# ================================================================== (b) SPARC")]
LGsrc=patch(LGsrc,'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)',f'HERE={str(HERE)!r}; REB={str(REB)!r}; REPO={str(ROOT)!r}')
LG={"__file__":str(HERE/"geometry_readonly.py"),"__name__":"csm1_geometry"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(LGsrc,"bs1_geometry_prefix","exec"),LG)
REF=load(REB/"BS1_basin_switch/bs1_basin_switch_results.json")
assert LG["LGP"]==REF["LG"]["basin"],"Primary LG basin reconstruction mismatch"
assert abs(LG["R0D"]-REF["LG"]["R0_data_kpc"])<1e-10
assert {n:LG["field_R"](n) for n in LG["FIELD"]}==REF["LG"]["field_R_kpc"]
emit("BASE GEOMETRY exact LG primary logM="+repr(LG["LGP"]["lgM"]))
FEET=("canonical","alt"); TAGS=("A_c2b_refit","B_cfg886_bg")
# HO2 head supplies original native table and MW solver. Its child_mw is compiled
# with read-only output suppression and a bounded observable cache between L cells.
HS=read(REB/"HO2_sluggs_milkyway_heldout/ho2_heldout.py")
HS=HS[:HS.index("# ================================================================== orchestration")]
HS=patch(HS,'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)',f'HERE={str(HERE)!r}; REB={str(REB)!r}; REPO={str(ROOT)!r}')
HS=patch(HS,'bg = BGR[tag]; lM = bg["a"] + bg["b"] * (math.log10(Mb) - 10); flag = lM > TSW','bg = BGR[tag]; lM = bg["a"] + bg["b"] * (math.log10(Mb) - 10); flag = CSM_FLAG(foot, tag, SIG_A0_PC)')
# Expensive original GD2/GD1 controls run once per fresh process.
a=HS.index('    GD2SRC = ',HS.index('def child_mw():')); b=HS.index('    # ---- CL2 picture on the GD2 path',a)
setup=HS[a:b]
newsetup='    global CACHED_SETUP\n    if CACHED_SETUP is None:\n'+''.join('    '+line+'\n' for line in setup.splitlines())+'        CACHED_SETUP=(N2,dict(out))\n    else:\n        N2, oldout=CACHED_SETUP; out.update(oldout)\n    FIELD_CURSOR[0]=0\n'
HS=HS[:a]+newsetup+HS[b:]
HS=patch(HS,'    def field(rhof):','    def field_uncached(rhof):')
HS=patch(HS,'    def obs(g, dR, dz, extraR=None):','    def obs_uncached(g, dR, dz, extraR=None):')
wrappers="""    def field(rhof):
        idx=FIELD_CURSOR[0]; FIELD_CURSOR[0]+=1
        if idx in FIELD_MASSES: return ("cached",idx),None,None,FIELD_MASSES[idx]
        v=field_uncached(rhof); FIELD_IDS[id(v[0])]=idx; FIELD_MASSES[idx]=v[3]; return v
    def idx_of(g): return g[1] if isinstance(g,tuple) else FIELD_IDS[id(g)]
    def okey(g,extraR): return (idx_of(g),None if extraR is None else tuple(float(v) for v in extraR))
    def obs(g,dR,dz,extraR=None):
        key=okey(g,extraR)
        if key not in OBS_CACHE: OBS_CACHE[key]=obs_uncached(g,dR,dz,extraR)
        return OBS_CACHE[key]
    def law_obs(g,dR,dz,foot,extraR=None):
        key=(okey(g,extraR),foot)
        if key not in LAW_CACHE:
            fac=nu(np.hypot(dR,dz)*A0C/A0SI[foot]); LAW_CACHE[key]=obs_uncached(g,fac*dR,fac*dz,extraR)
        return LAW_CACHE[key]
"""
HS=patch(HS,'    def lines(vc, K, K0, vo):',wrappers+'    def lines(vc, K, K0, vo):')
HS=patch(HS,'        if branch(flag):\n            Sig = sigma_cl2_pc', '        b = obs(g, dR, dz, extraR); law_b = law_obs(g, dR, dz, foot, extraR)\n        if branch(flag):\n            Sig = sigma_cl2_pc')
HS=patch(HS,'            fac = nu(np.hypot(dR, dz) * A0C / A0SI[foot])\n            o = obs(g, fac * dR, fac * dz, extraR)','            o = law_b')
HO={"__file__":str(HERE/"ho2_readonly.py"),"__name__":"csm1_ho2", "CACHED_SETUP":None,"FIELD_CURSOR":[0],"FIELD_MASSES":{},"FIELD_IDS":{},"OBS_CACHE":{},"LAW_CACHE":{}}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(HS,"ho2_head_with_baryon_cache","exec"),HO)
# Source edits archive is reviewable, but never a historical-lane file.
with open(args.output/"executed_ho2_source.py","w") as fh: fh.write(HS)
C0=HO["child_sigma"](); HO["TAB"].update(lg=np.array(C0["lg"]),lsc={t:np.array(v) for t,v in C0["lsc"].items()})
save(args.output/"sigma_table.json",C0)
S9=HO["S9"]; B1=HO["B1"]; LOG=[]; STATE={"mode":"baseline","L":4.0}
def parent_column(foot,tag,M): return HO["eta"](M)*HO["sig_coll_pc"](tag,M)
def CSM_FLAG(foot,tag,floors):
    M=10**LG["LGP"]["lgM"]
    expected=LG["LGP"]["lgM"]>12.3 if STATE["mode"]=="baseline" else parent_column(foot,tag,M)>floors[foot]
    actual=(not expected) if args.mutate and STATE["mode"]!="baseline" else bool(expected)
    LOG.append(dict(footing=foot,background=tag,selected_mass_Msun=M,own_core_L=STATE["L"],column=parent_column(foot,tag,M),floor=floors[foot],expected=bool(expected),actual=bool(actual),mode=STATE["mode"]))
    return actual
HO["CSM_FLAG"]=CSM_FLAG
# X51 is sliced before old top-level score loops and evaluated with its original
# cooling-floor profile. Only gp's branch choice changes, through one callback.
XS=read(REB/"X51_dwarf_cooling_floor/x51_dwarfs.py")
XS=XS[:XS.index('RES = dict(frozen=')]
XS=patch(XS,'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)',f'HERE={str(HERE)!r}; REB={str(REB)!r}; REPO={str(ROOT)!r}')
XS=patch(XS,'        gp = gN + G * Mh / r12 ** 2','        above=CSM_DFLAG(r["name"],f)\n        gp = gN + G * Mh / r12 ** 2 if above else float(gN*(0.5+np.sqrt(0.25+A0[f]/gN)))')
XS=patch(XS,'out.append(dict(name=r["name"], cls=r["cls"],','out.append(dict(host=r["host"], branch="route E halo" if above else "law", gp=gp, gN=gN, gh=G*Mh/r12**2, gobs=gobs, name=r["name"], cls=r["cls"],')
DX={"__file__":str(HERE/"x51_readonly.py"),"__name__":"csm1_x51"}
DLOG=[]
def CSM_DFLAG(name,foot):
    d=LG["DWARFS"][name]; R=LG["field_R"](name) if d["host"] not in ("MW","M31") else None
    inLG=d["host"] in ("MW","M31") or (R is not None and R<LG["R0D"])
    M=10**LG["LGP"]["lgM"] if inLG else 10**LG["lgM200"](math.log10(LG["mb_of_mstar"](10**d["lm"])))
    floor=DX["SIGPC"][foot]; col=parent_column(foot,"A_c2b_refit",M)
    expected=math.log10(M)>12.3 if STATE["mode"]=="baseline" else col>floor
    actual=(not expected) if args.mutate and STATE["mode"]!="baseline" else bool(expected)
    DLOG.append(dict(name=name,footing=foot,background="A_c2b_refit",selected_mass_Msun=M,in_LG=inLG,column=col,floor=floor,expected=bool(expected),actual=bool(actual),mode=STATE["mode"]))
    return actual
DX["CSM_DFLAG"]=CSM_DFLAG
saved_argv=sys.argv; sys.argv=[str(HERE/"x51_readonly.py")]
try:
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(XS,"x51_profile_prefix","exec"),DX)
finally: sys.argv=saved_argv
with open(args.output/"executed_x51_source.py","w") as fh: fh.write(XS)
# HO3 frozen field rules copied as function definitions from BS1.
rt=ast.parse(BS); names={"thr","rules"}
rns={"np":np,"stats":stats,"math":math,"SEED":20261027,"S2T":{},"P0":.0455,"PMIN":.01}
exec(compile(ast.Module(body=[n for n in rt.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),"bs1_rules","exec"),rns)
ALLCLS=tuple(dict.fromkeys(r["cls"] for r in LG["X1"]))
def dwarfs():
    out={}; raw={}
    for f in FEET:
        R=DX["rows"](f,ALLCLS); raw[f]=R; rng=np.random.default_rng(20261026); classes={}
        for c in DX["CLS"]:
            q=[x for x in R if x["cls"]==c]; m,sd=DX["boot"](np.array([x["E"] for x in q]),np.array([x["s"] for x in q]),rng)
            classes[c]=dict(N=len(q),median=m,sd=sd,Z=m/sd,reproduced=abs(m/sd)<2,r0_kpc=float(np.median([x["r0_kpc"] for x in q])),M200=float(np.median([x["M200"] for x in q])))
        fld=sorted([x for x in R if x["host"] not in ("MW","M31")],key=lambda x:x["name"]); sat=[x for x in R if x["host"] in ("MW","M31")]
        per={x["name"]:dict(E=x["E"],s=x["s"],Z=x["E"]/x["s"],branch=x["branch"]) for x in fld}
        flags={n:dict(per[n],flag="ABOVE PICTURE" if per[n]["Z"]>=2 else "BELOW PICTURE" if per[n]["Z"]<=-2 else "CONSISTENT") for n in ("Leo T","Phoenix","IC 1613")}
        out[f]=dict(classes=classes,isolated=rns["rules"]([x["E"]/x["s"] for x in fld]),satellites=rns["rules"]([x["E"]/x["s"] for x in sat]),per_field=per,flags=flags)
    return dict(footings=out,rows=raw)
def setlevel(L,mode):
    STATE.update(L=L,mode=mode); HO["CF_TAB"][:]=[L*v/S9[2] for v in S9]
def mw():
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()): return HO["child_mw"]()
def leafdiff(a,b,tol=1e-6,path=""):
    bad=[]
    if isinstance(b,dict):
        for k,v in b.items():
            if k not in a: bad.append(path+"/"+k+" missing")
            else: bad+=leafdiff(a[k],v,tol,path+"/"+k)
    elif isinstance(b,list):
        if len(a)!=len(b): bad.append(path+" length")
        else:
            for i,(x,y) in enumerate(zip(a,b)): bad+=leafdiff(x,y,tol,path+"/"+str(i))
    elif isinstance(b,(bool,str)) or b is None:
        if a!=b: bad.append(path)
    elif abs(a-b)>tol*max(1.,abs(b)): bad.append(path)
    return bad
# Baseline must pass before corrected grades.
setlevel(4.,"baseline"); BD=dwarfs(); BM=mw()
bad=[]
for f in FEET:
    bad+=leafdiff(BD["footings"][f]["classes"],REF["primary"]["grade"][f]["dwarfs"],path="classes/"+f)
    for k in ("isolated","satellites","per_field","flags"): bad+=leafdiff(BD["footings"][f][k],REF["primary"]["dwarfs"][f][k],path=k+"/"+f)
    ref=REF["primary"]["mw"][f]; bx=BM["box"][f+"|A_c2b_refit"]
    bad+=leafdiff(bx,{k:ref[k] for k in ("cls","counts","branches","best","passing")},path="mwbox/"+f)
    mc=BM["mcmillan"]["rows"][f+"|A_c2b_refit"]
    cmp=dict(branch=mc["branch"],vc_R0=mc["vc_R0"],z_vc=mc["z_vc_Eilers"],K_R0=mc["K_R0"],z_Kz=mc["z_Kz_BR"],**{k:mc[k] for k in ("L1","L2a","L2b","L3")})
    bad+=leafdiff(cmp,ref["mcmillan"],path="mcmillan/"+f)
assert not bad,"Baseline failed: "+repr(bad[:20])
assert BM["S0_GD2"]["ok"] and BM["S0_GD1"]["ok"] and BM["K3"]<1e-9
emit("BASELINE BS1 primary reproduced: geometry, five classes, 13 field rows/rules, MW box/McMillan both footings")
BASE=dict(dwarfs=BD,mw=BM)
save(args.output/"baseline.json",BASE)
RES=dict(checkpoint="CSM1_heldout",mutate=args.mutate,LG=REF["LG"],baseline_reproduction=dict(pass_=True,leaf_tolerance=1e-6,geometry_exact=True),levels={},scope_limitations=["Only MW, X51 dwarf calibration classes, and HO3 field/satellite diagnostics rerun here; calibration owner supplies SPARC/groups/clusters/lensing.","X51 retains distinct cooling-floor profile; giant-parent switch used only for branch.","HO1 hot-gas and HO2 SLUGGS known failures are unaltered, not regraded here.","Heldout data were known before this correction; no blind-validation claim."])
for L in (3.75,3.9,4.):
    setlevel(L,"corrected"); LOG.clear(); DLOG.clear(); DD=dwarfs(); MM=mw()
    # Replay identical L4 baseline when all LG branches are unchanged in normal run.
    violations=0; maxerr=0.
    for z in LOG+DLOG:
        lm=math.log10(z["selected_mass_Msun"])
        cf=L*float(np.interp(lm,[12.,13.,14.],S9))/S9[2]
        coll=10**float(np.interp(lm,C0["lg"],C0["lsc"][z["background"]]))
        col=4/(3*(3*math.log(2)-math.pi/2))*cf**1.25*coll
        maxerr=max(maxerr,abs(col/z["column"]-1))
        violations+=int(bool(col>z["floor"])!=z["actual"])
    independent=dict(n=len(LOG)+len(DLOG),violations=violations,column_max_relative_error=maxerr)
    selector_ok=violations==0 and maxerr<1e-12
    roots={}
    for f in FEET:
        for tag in TAGS:
            floor=next(z["floor"] for z in LOG if z["footing"]==f and z["background"]==tag)
            roots[f+"|"+tag]=brentq(lambda lm: parent_column(f,tag,10**lm)-floor,9.,16.)
    level=dict(L=L,cf_table=list(HO["CF_TAB"]),dwarfs=DD,mw=MM,selector_log=dict(MW=list(LOG),dwarfs=list(DLOG)),selector_agreement=selector_ok,selector_independent_audit=independent,diagnostic_roots_native_table=roots)
    RES["levels"][str(L)]=level
    save(args.output/"firstcell.json" if L==3.75 else args.output/("cell_"+str(L)+".json"),level)
    emit("CORRECTED L="+str(L)+" selector_agreement="+str(selector_ok)+" "+json.dumps({f:dict(mw=MM["box"][f+"|A_c2b_refit"]["cls"],n_VK=MM["box"][f+"|A_c2b_refit"]["counts"]["L1&L2a&L2b"],field=DD["footings"][f]["isolated"]["ok"],dwarf_classes={c:dict(median=v["median"],Z=v["Z"]) for c,v in DD["footings"][f]["classes"].items()}) for f in FEET},sort_keys=True))
checks={"K0_baseline":not bad,"K1_all_corrected_selectors":all(v["selector_agreement"] for v in RES["levels"].values()),"K2_geometry_exact":LG["LGP"]==REF["LG"]["basin"],"K3_MW_baryon_cache_order":len(HO["FIELD_MASSES"])==HO["FIELD_CURSOR"][0],"K4_RSS_under_1GB":rss()<1.}
# Compare replay L4 baseline using full stable scientific outputs (switch counts
# are cumulative instrumentation and intentionally excluded).
if not args.mutate:
    M4=RES["levels"]["4.0"]["mw"]
    checks["K5_L4_baryonic_replay_matches_baseline"]=not leafdiff(M4["box"],BM["box"]) and not leafdiff(M4["mcmillan"],BM["mcmillan"])
RES["checks"]=checks; RES["cache"]={"field_count":len(HO["FIELD_MASSES"]),"observable_entries":len(HO["OBS_CACHE"]),"law_entries":len(HO["LAW_CACHE"])}
# Remove runtime/RSS/cumulative-switch counters from deterministic science file;
# exact measurements are retained in resources.json.
def stable(x):
    if isinstance(x,dict): return {k:stable(v) for k,v in x.items() if k not in ("rss","switch")}
    if isinstance(x,list): return [stable(v) for v in x]
    return x
RES=stable(RES)
save(args.output/"results.json",RES)
save(args.output/"resources.json",dict(runtime_seconds=time.time()-START,peak_RSS_GB=rss(),threads={k:os.environ[k] for k in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","VECLIB_MAXIMUM_THREADS","MKL_NUM_THREADS")},memory_limit="observed only; macOS RLIMIT_AS unsupported"))
# Manifest scientific sources observed through watched open, including dynamic
# solver read dependencies. Hash after computation; runtime metadata is separate.
for p in (HERE/"FROZEN_CRITERIA.md",HERE.parent/"FROZEN_CRITERIA.md"): READS[str(p.relative_to(ROOT))]=sha(p)
stable_inputs=all(sha(ROOT/p)==h for p,h in READS.items()); checks["K6_inputs_stable"]=stable_inputs
# Results checks now include provenance stability before its final hash.
RES["checks"]["K6_inputs_stable"]=stable_inputs; save(args.output/"results.json",RES)
outputs=[p for p in args.output.iterdir() if p.is_file() and p.name!="manifest.json"]
code=0 if all(checks.values()) else 1
manifest=dict(schema_version=2,claim_id="CSM1_MW_DWARF_FINITE",repository=dict(commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),dirty=True),command=[sys.executable,"-I",str(Path(__file__).resolve()),"--output",str(args.output)]+(["--mutate"] if args.mutate else []),environment=dict(software=[dict(name="Python",version=platform.python_version()),dict(name="numpy",version=np.__version__),dict(name="scipy",version=scipy.__version__),dict(name="classy",version=getattr(sys.modules["classy"],"__version__","unavailable"))],hardware=platform.platform()),mathematics=dict(assertion_tested="Reproduce BS1 primary and regrade fixed L3.75/3.9/4 with mass-dependent parent selector equal to core column on actual basin mass.",coefficient_domain="IEEE float64",conventions="S9 linear interpolation in logM with clamp; HO2 log-column 0.0005 dex native table; X51 dwarf cooling-floor profile",inputs=["BS1 original local data and frozen scorer inputs"],bounds=dict(L=[3.75,3.9,4.],footings=list(FEET),MW_cells=len(BM["cells"]),field_dwarfs=13),non_claims=RES["scope_limitations"]),randomness=dict(used=True,generator="numpy PCG64",seed=[20261027,20261026]),run=dict(started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(START)),runtime_seconds=time.time()-START,exit_status=code,status="completed" if code==0 else "failed",resource_limits=dict(memory_bytes=None,cpu_seconds=None,max_cores=None,max_threads=1)),outputs=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p),kind="result") for p in sorted(outputs)],checks=[dict(name=k,pass_=bool(v)) for k,v in checks.items()],result="Finite controls pass" if code==0 else "Expected source-flag mutation detected" if args.mutate and not checks["K1_all_corrected_selectors"] else "Control failure",residual_risks=RES["scope_limitations"],input_artifacts=[dict(path=p,sha256=h,sha256_after=sha(ROOT/p)) for p,h in sorted(READS.items())],declared_results=[str((args.output/n).relative_to(ROOT)) for n in DECLARED_NAMES])
save(args.output/"manifest.json",manifest)
emit("RESOURCE "+json.dumps(load(args.output/"resources.json"))); emit("CHECKS "+json.dumps(checks,sort_keys=True)); sys.exit(code)
