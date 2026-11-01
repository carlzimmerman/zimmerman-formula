#!/usr/bin/env python3
"""CRG1 spec stage: populate inputs/ and MANIFEST.txt from the repo. Not given to the implementer. Writes no candidate result.
Run from anywhere: OMP_NUM_THREADS=1 nice -n 15 python3 extract_inputs.py [--no-efe]. kappa = 1/2 FITTED; not theory closed."""
import csv, glob, hashlib, json, math, os, re, shutil, sys
for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","VECLIB_MAXIMUM_THREADS","MKL_NUM_THREADS"): os.environ[v]="1"
import numpy as np
from astropy.io import fits
H=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RB=os.path.dirname(H); REPO=os.path.dirname(RB); EXT=os.path.join(os.path.dirname(REPO),"_external_data"); IN=os.path.join(H,"inputs"); DATA=os.path.join(REPO,"real_research","data")
SRC={}
def out(p): q=os.path.join(IN,p); os.makedirs(os.path.dirname(q),exist_ok=True); return q
def cp(src,dst,tag): shutil.copyfile(src,out(dst)); SRC[dst]=tag
def J(*p): return json.load(open(os.path.join(RB,*p)))
def dump(o,dst,tag): json.dump(o,open(out(dst),"w"),indent=1); SRC[dst]=tag
# SPARC
for f in sorted(os.listdir(os.path.join(DATA,"sparc_data"))):
    if f.endswith("_rotmod.dat"): cp(os.path.join(DATA,"sparc_data",f),f"sparc/rotmod/{f}",f"real_research/data/sparc_data/{f}")
cp(os.path.join(DATA,"SPARC_Lelli2016c.mrt"),"sparc/SPARC_Lelli2016c.mrt","real_research/data/SPARC_Lelli2016c.mrt")
# LITTLE THINGS, Oh+2015 Table 2 cells parsed to a clean table
tex=open(os.path.join(REPO,"_external_data","little_things_oh2015","src","ms.tex")).read().split("\n"); i0=next(i for i,l in enumerate(tex) if "label{MD_results_LT}" in l); i1=next(i for i in range(i0,len(tex)) if "end{tabular}" in tex[i])
NAMES=["CVnIdwA","DDO 43","DDO 46","DDO 47","DDO 50","DDO 52","DDO 53","DDO 70","DDO 87","DDO 101","DDO 126","DDO 133","DDO 154","DDO 168","DDO 210","DDO 216","F564-V3","IC 10","IC 1613","NGC 1569","NGC 2366","NGC 3738","UGC 8508","WLM","Haro 29","Haro 36"]
rows={}; buf="";start=None
for k in range(i0,i1):
    l=tex[k].split("%")[0]
    if start is None:
        nm=l.split("&")[0].strip()
        if nm in NAMES: start=k+1; buf=""
        else: continue
    buf+=" "+l
    if "\\\\" in l:
        c=[x.strip() for x in buf.replace("\\\\","").split("&")]; rows[c[0]]=c; start=None
def val(c):
    c=c.replace("$","").replace("\\pm"," pm ").replace("{"," ").replace("}"," "); nums=re.findall(r"-?\d+\.?\d*(?:[eE][-+]?\d+)?",c)
    if not nums or "..." in c.split("pm")[0]: return None,None
    return float(nums[0]),(float(nums[1]) if ("pm" in c and len(nums)>1) else None)
with open(out("little_things/oh2015_table2.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["name","Rmax_kpc","V_kms","eV_kms","Mgas_1e7Msun","MSED_1e7Msun"])
    for n in NAMES:
        c=rows[n]; R=val(c[1])[0]; V,eV=val(c[3]); mg=val(c[13])[0]; ms=val(c[15])[0]; w.writerow([n,R,V,eV,mg,ms])
SRC["little_things/oh2015_table2.csv"]="zimmerman-formula/_external_data/little_things_oh2015/src/ms.tex (Table 2 cells, columns 1,3,13,15)"
# groups
cp(os.path.join(EXT,"vizier2026","J_A_A_710_L39.tsv"),"groups/J_A_A_710_L39.tsv","_external_data/vizier2026/J_A_A_710_L39.tsv")
# X-COP
for name in sorted(os.listdir(os.path.join(DATA,"xcop"))):
    p=os.path.join(DATA,"xcop",name)
    if os.path.isdir(p) and os.path.exists(os.path.join(p,f"{name}_mstar.fits")):
        for t in ("hydro_mass","fgas_profile","mstar"): cp(os.path.join(p,f"{name}_{t}.fits"),f"xcop/{name}/{name}_{t}.fits",f"real_research/data/xcop/{name}/{name}_{t}.fits")
# cluster shear stacks and catalogue columns
cp(os.path.join(RB,"X7_cluster_core_significance","x7_measure_percluster.npz"),"clusters/x7_measure_percluster.npz","rebuild_2026_10_22/X7_cluster_core_significance/x7_measure_percluster.npz")
X=np.load(os.path.join(RB,"X2_cluster_outskirts","x2_replay_percluster.npz"))
MY=np.load(os.path.join(RB,"X7_cluster_core_significance","x7_measure_percluster.npz"))
np.savez_compressed(out("clusters/x2_catalogue_columns.npz"),**{k:X[k] for k in ("name","ra","dec","z","Mgas500","R500","off_deg")}); SRC["clusters/x2_catalogue_columns.npz"]="rebuild_2026_10_22/X2_cluster_outskirts/x2_replay_percluster.npz (catalogue columns)"
E_=fits.open(os.path.join(DATA,"erass1cl_primary_v3.2.fits"))[1].data; idx={str(s).strip():k for k,s in enumerate(E_["NAME"])}; KT=np.asarray(E_["KT"],float)
with open(out("clusters/erass1_kt.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["name","KT_keV"]); [w.writerow([str(n),repr(float(KT[idx[str(n).strip()]]))]) for n in MY["name"]]
SRC["clusters/erass1_kt.csv"]="real_research/data/erass1cl_primary_v3.2.fits (KT, by NAME)"
LN=os.path.join(REPO,"campaign_fresh_gravity"); P687=np.load(os.path.join(LN,"CFG687_erass1_shear_stack","cfg687_percluster.npz")); CEN=json.load(open(os.path.join(LN,"CFG922_cluster_core_baryon_recheck","cfg922_census_A1.json")))["eRASS1"]
with open(out("clusters/bcg_per_cluster.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["name","bcg_Msun_or_nan"])
    for i in range(len(MY["name"])):
        dd=np.hypot((P687["ra"]-MY["ra"][i])*np.cos(np.radians(MY["dec"][i])),P687["dec"]-MY["dec"][i])*3600; j=int(np.argmin(dd)); v=float("nan")
        if dd[j]<5 and abs(P687["z"][j]-MY["z"][i])<1e-3 and not CEN[j].get("not_measured",False):
            b=float(CEN[j]["bcg_med"]); v=b if b>0 else float("nan")
        w.writerow([str(MY["name"][i]),repr(v)])
SRC["clusters/bcg_per_cluster.csv"]="campaign_fresh_gravity/CFG922_cluster_core_baryon_recheck/cfg922_census_A1.json matched through CFG687_erass1_shear_stack/cfg687_percluster.npz [INPUT AS GIVEN]"
X7J=J("X7_cluster_core_significance","x7_analysis_results.json"); tc={}
for f in ("canonical","alt"):
    for h in ("h0672","h0686"):
        cl=f"{f}|{h}"; a=X7J["all"][f"C*|boost|{cl}"]["OUTER"]; r=X7J["bins"][f"terciles|{cl}"]
        tc[cl]={"Mall":dict(A_CAL=a["A_CAL"],s_CAL=a["s_CAL"]),**{f"M{t+1}":dict(A_CAL=r[t]["OUTER"]["A_CAL"],s_CAL=r[t]["OUTER"]["s_CAL"]) for t in range(3)}}
dump(tc,"clusters/x7_outer_mgas_cal.json","rebuild_2026_10_22/X7_cluster_core_significance/x7_analysis_results.json (A_CAL, s_CAL, OUTER; measurement side) [INPUT AS GIVEN]")
cp(os.path.join(REPO,"real_research","reviews","directional_efe_2026","laneB_data","chae21_env.csv"),"clusters/chae21_env.csv","real_research/reviews/directional_efe_2026/laneB_data/chae21_env.csv")
# dwarfs
keep=["footing","name","host","cls","logMstar","M_V","rh_pc","sigma","sdMC[Newton]"]
with open(out("dwarfs/x1_per_system_inputs.csv"),"w",newline="") as fh:
    w=csv.DictWriter(fh,keep); w.writeheader()
    for r in csv.DictReader(open(os.path.join(RB,"X1_hosted_recount","x1_per_system.csv"))): w.writerow({k:r[k] for k in keep})
SRC["dwarfs/x1_per_system_inputs.csv"]="rebuild_2026_10_22/X1_hosted_recount/x1_per_system.csv (data columns only)"
cp(os.path.join(LN,"CFG257_ufd_kinematics_scoping","arroyo_polonio2026_tableA1.csv"),"dwarfs/arroyo_polonio2026_tableA1.csv","campaign_fresh_gravity/CFG257_ufd_kinematics_scoping/arroyo_polonio2026_tableA1.csv")
# lensing
B21=os.path.join(DATA,"lensing_rar","brouwer2021_rar")
for f in [f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt" for b in range(1,5)]+["Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"]: cp(os.path.join(B21,f),f"lensing/{f}",f"real_research/data/lensing_rar/brouwer2021_rar/{f}")
L=np.load(os.path.join(DATA,"lensing_rar","lr_lenses.npz")); PL=np.load(os.path.join(DATA,"lensing_rar","cfg110_perlens.npz"))
np.savez_compressed(out("lensing/lens_inventory.npz"),logM=L["logM"],z=L["z"],WLENS=PL["WW"].sum(axis=1)); SRC["lensing/lens_inventory.npz"]="real_research/data/lensing_rar/lr_lenses.npz (logM, z), cfg110_perlens.npz (WW summed over axis 1)"
T=json.load(open(os.path.join(EXT,"cfg650_work","T1x","cfg650_m1m2m3_RES_canonical_N1024_L100_ns1024_lean.json")))["snap"]["x0.2562"]
dump(dict(z=T["z"],k_h_Mpc=T["k"],P_grav=T["P_grav"],sigma8_grav=T["sigma8_grav"]),"lensing/t1x_pgrav_x0.2562.json","_external_data/cfg650_work/T1x/cfg650_m1m2m3_RES_canonical_N1024_L100_ns1024_lean.json (snap x0.2562) [INPUT AS GIVEN]")
# scalars
F3=J("F3_growth_audit","f3_growth_audit_results.json")["K2"]; EM=J("EM1_emergent_dust_law","em1_emergent_results.json")["rows"]
NR2=J("NR2_low_mass_ng80","nr2_results.json"); CEA4=J("CE1_converged_eta_grade","ce1_a4_results.json")["eta"]; X80=J("X80_low_mass_floor_emergence","x80_converged.json"); S77=J("X77_direct_core_surface_density","x77_results.json")["summary"]
dump(dict(
 backgrounds={t:dict(params=F3[t]["params"],sigma8=F3[t]["sigma8"],em1_map_a=EM[t]["R1"]["a"],em1_map_b=EM[t]["R1"]["b"]) for t in ("A_c2b_refit","B_cfg886_bg")},
 nr2=dict(cf_table=J("NR2_low_mass_ng80","NR2_MEDIAN_cf_table.json")["cf_by_mass"],rho10=NR2["r10"],rho11=NR2["r11"],eta12_anchor=21.53,per_seed_eta={k:v for k,v in NR2["eta"].items() if k.endswith("ng80")}),
 ce1_a3_cf={fs:J("CE1_converged_eta_grade",f"CE1_med_fs{fs}_cf_table.json")["cf_by_mass"] for fs in ("0.034","0.0615")},
 ce1_a4_eta_med={k:CEA4[k]["med"] for k in ("12","13","14")},
 ce1_a3_eta_med={k:J("CE1_converged_eta_grade","ce1_results.json")["eta"][k]["med"] for k in ("12","13","14")},
 x80=dict(r10=X80["r10"],r11=X80["r11"]),
 x48_A2_cf=J("X48_native_cf_zoom","x48_analyze_results_ng48_A2.json")["cf_by_mass"],
 x77_eta_med=dict(e12=S77["1e+12_ng64"]["eta_med"],e13=S77["1e+13_ng48"]["eta_med"],e14=S77["1e+14_ng48"]["eta_med"]),
 gs1_s_meas=J("GS1_measured_gas_outskirts","gs1_gas_slope_results.json")["slope"]["s_meas"],
 fstar=dict(primary=0.034,reported=0.0615,harness=0.20),gas_dex=dict(gs4=0.005,xcop=0.111),
 native=dict(Om=0.2976016,h=0.6856427,wb=0.0223081)),"scalars.json","rebuild_2026_10_22: F3, EM1, NR2, CE1, X80, X48 A2, X77, GS1, ZN4, X73 (inputs only) [INPUT AS GIVEN]")
# CLASS tables
from classy import Class
for t in ("A_c2b_refit","B_cfg886_bg"):
    p=F3[t]["params"]; c=Class(); c.set({"omega_b":p["omega_b"],"omega_cdm":p["omega_cdm"],"h":p["h"],"ln10^{10}A_s":p["lnAs"],"n_s":p["n_s"],"tau_reio":p["tau"],"N_ur":3.044,"output":"mPk","P_k_max_h/Mpc":200.0,"z_max_pk":10.0}); c.compute(); h=p["h"]
    k=np.logspace(-4,math.log10(150.0),3000); Pk=np.array([c.pk_lin(kk*h,0.0) for kk in k])*h**3
    zg=np.linspace(0,30,3001); Dg=np.array([c.scale_independent_growth_factor(z) for z in zg]); Dg/=Dg[0]
    Hz=np.array([c.Hubble(z) for z in np.linspace(0,3,301)])
    np.savez_compressed(out(f"background/class_{t}.npz"),k_h_Mpc=k,Pk_Mpc3_h3=Pk,zg=zg,Dg=Dg,Omega_m_class=float(c.Omega_m()),Omega_nu=float(c.Omega_nu),h=h)
    SRC[f"background/class_{t}.npz"]=f"CLASS run at F3's {t} params, settings as EM1 [INPUT AS GIVEN]"
# zoom snapshots: x as float32, m, meta subset
def zoom(src,dst):
    Z=np.load(src,allow_pickle=False); meta=json.loads(str(Z["meta"])); keep={k:meta[k] for k in ("M","Mf","qM","zf","eps","N","rf_phys") if k in meta}
    np.savez_compressed(out(dst),x=Z["x"].astype(np.float32),m=float(Z["m"]),meta=json.dumps(keep)); SRC[dst]=os.path.relpath(src,os.path.dirname(REPO))+" (x as float32, m, meta subset)"
for M,root in (("1e10",os.path.join(RB,"NR2_low_mass_ng80","runs")),("1e11",os.path.join(RB,"NR2_low_mass_ng80","runs")),("1e12",os.path.join(RB,"X48_native_cf_zoom","runs"))):
    for s in range(1,10):
        f=os.path.join(root,f"M{M}_s{s}_ng80","snap_zf.npz")
        if os.path.exists(f): zoom(f,f"zooms/eta/M{M}_s{s}_ng80_zf.npz")
for s in range(1,10):
    for zs in ("0.00","0.25","0.50"):
        f=os.path.join(RB,"ZN1_zooms_to_z0","runs",f"M1e13_s{s}_ng64",f"snap_z{zs}.npz")
        if os.path.exists(f): zoom(f,f"zooms/shape/M1e13_s{s}_ng64_z{zs}.npz")
for M in ("1e14","1e15"):
    for s in range(1,7):
        for zs in ("0.00","0.25","0.50"):
            f=os.path.join(RB,"ZN4_cluster_resolution","runs",f"M{M}_s{s}_ng80",f"snap_z{zs}.npz")
            if os.path.exists(f): zoom(f,f"zooms/shape/M{M}_s{s}_ng80_z{zs}.npz")
            elif zs=="0.50": zoom(os.path.join(RB,"ZN4_cluster_resolution","runs_zf",f"M{M}_s{s}_ng80","snap_zf.npz"),f"zooms/shape/M{M}_s{s}_ng80_zf_as_z0.50.npz")
# EFE tables (cross-check and fallback)
if "--no-efe" not in sys.argv:
    sys.path.insert(0,os.path.join(RB,"F2_outer_lensing")); import f2_aqual as AQ
    CH=list(csv.DictReader(open(out("clusters/chae21_env.csv")))); med=float(np.median([float(r["log_eN_noclu"]) for r in CH]))
    for f,a0 in (("canonical",9.3603e-11),("alt",1.1312e-10)):
        s=AQ.solve_efe(10**med*1.2e-10/a0,maxit=3000); np.savez_compressed(out(f"clusters/efe_table_{f}.npz"),s=np.asarray(s["r"]),M=np.asarray(s["M"]),x_e=s["x_e"],y_e=s["y_e"],iters=s["iters"],resid=s["resid"]); SRC[f"clusters/efe_table_{f}.npz"]="F2 AQUAL solver output at y_e of chae21 noclu [INPUT AS GIVEN, cross-check and fallback]"
# manifest
def nrows(p):
    q=os.path.join(IN,p)
    if p.endswith((".csv",".tsv",".dat",".txt",".mrt")): return sum(1 for _ in open(q,errors="replace"))
    if p.endswith(".npz"): Z=np.load(q,allow_pickle=False); return ";".join(f"{k}:{'x'.join(map(str,Z[k].shape))}" for k in Z.files)[:120]
    if p.endswith(".json"): return "json"
    if p.endswith(".fits"):
        with fits.open(q) as h: return ";".join(str(len(x.data)) for x in h[1:] if x.data is not None)
    return ""
with open(os.path.join(IN,"MANIFEST.txt"),"w") as fh:
    fh.write("# path\tsource path (repo-relative, _external_data = sibling of the repo)\tsha256\trows or shapes\n")
    for p in sorted(SRC): fh.write(f"{p}\t{SRC[p]}\t{hashlib.sha256(open(os.path.join(IN,p),'rb').read()).hexdigest()}\t{nrows(p)}\n")
print("done",len(SRC),flush=True)
