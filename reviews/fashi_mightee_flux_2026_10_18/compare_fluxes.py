#!/usr/bin/env python3
"""FASHI/MIGHTEE flux calibration check. Run through computation-audit runner.

Usage: python3 reviews/fashi_mightee_flux_2026_10_18/compare_fluxes.py --output DIR
Contract: contract.json beside this file, specified before COSMOS FASHI ratios.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/fashi_mightee_mpl")
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
C = 299792.458
NU0 = 1420.40575177e6
SEED = 20261018
CAT = "data_assembly/mightee_hi_catalogue_2026-10-02/MIGHTEE_HI_COSMOS_catalogue.csv"
CUBE = "campaign_fresh_gravity/CFG302_mightee_cube_raw_widths/cfg302_per_galaxy.csv"
OLD = "campaign_fresh_gravity/CFG304_mightee_flux_scale_alfalfa/cfg304_matched_pairs.csv"
SCIENCE = "campaign_fresh_gravity/CFG301_mightee_hi_catalogue_width_chain/cfg301_stageA_results.json"
FAST = "_external_data/fashi_dr2_2026_10_18/fashi_dr2.csv"
FA = "_external_data/fashi_dr2_2026_10_18/fashi_alfalfa.csv"
FLAGS = ["low_confidence_flag", "blended_flag", "confused_flag", "bad_ellipse_flag", "contaminated_source_flag"]


def sep(ra1, de1, ra2, de2):
    r1, d1, r2, d2 = map(np.radians, (ra1, de1, ra2, de2))
    h = np.sin((d1-d2)/2)**2 + np.cos(d1)*np.cos(d2)*np.sin((r1-r2)/2)**2
    return 3600*np.degrees(2*np.arcsin(np.sqrt(np.clip(h, 0, 1))))


def conv(flux, freq_mhz, mode):
    nu = np.asarray(freq_mhz)*1e6
    factor = {"OPT": C*NU0/nu**2, "REST": C/nu, "RADIO": C/NU0}[mode]
    return np.asarray(flux)*factor


def truth(x):
    return str(x).lower() in ("true", "1", "1.0")


def stats(x, seed=SEED):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if not len(x):
        return {"n": 0, "median_dex": None, "ratio": None, "ci68_dex": None, "ci95_dex": None, "scatter_dex": None}
    med = float(np.median(x))
    rng = np.random.default_rng(seed)
    boot = np.median(x[rng.integers(0, len(x), (10000, len(x)))], axis=1)
    qq = np.quantile(boot, [.16, .84, .025, .975])
    return {"n": len(x), "median_dex": med, "ratio": float(10**med), "ci68_dex": qq[:2].tolist(),
            "ci95_dex": qq[2:].tolist(), "scatter_dex": float(1.4826*np.median(np.abs(x-med)))}


def assess(s, minimum=8):
    if s["n"] < minimum:
        return "insufficient pairs"
    lo, hi = s["ci95_dex"]
    if hi < -.1:
        return "lower than reference beyond 0.10 dex band"
    if lo > .1:
        return "higher than reference beyond 0.10 dex band"
    if lo >= -.1 and hi <= .1:
        return "compatible within 0.10 dex band"
    return "unresolved at 95 percent"


def match(m, f, radius=60., ra=None, de=None):
    ra = m.RA_deg.to_numpy() if ra is None else ra
    de = m.Dec_deg.to_numpy() if de is None else de
    ss = sep(ra[:, None], de[:, None], f.ra.to_numpy()[None, :], f.dec.to_numpy()[None, :])
    vv = C*(NU0/(m.freq_MHz.to_numpy()*1e6)-1)
    dv = vv[:, None]-f.v_opt.to_numpy()[None, :]
    ii, jj = np.nonzero((ss <= radius) & (np.abs(dv) <= 300))
    cand = pd.DataFrame({"i": ii, "j": jj, "sep_arcsec": ss[ii, jj], "dv_kms": dv[ii, jj]})
    cand["n_m_candidates"] = cand.groupby("i").i.transform("size")
    cand["n_f_candidates"] = cand.groupby("j").j.transform("size")
    cand["abs_dv"] = np.abs(cand.dv_kms)
    cand = cand.sort_values(["sep_arcsec", "abs_dv", "i", "j"], kind="mergesort")
    used_m, used_f, keep = set(), set(), []
    for k, row in cand.iterrows():
        i, j = int(row.i), int(row.j)
        if i not in used_m and j not in used_f:
            keep.append(k); used_m.add(i); used_f.add(j)
    return cand.loc[keep].copy(), cand


def controls():
    checks = {}
    checks["sky_known_one_arcsec"] = abs(float(sep(0, 0, 1/3600, 0))-1) < 1e-10
    checks["sky_ra_wrap"] = abs(float(sep(359.999, 0, .001, 0))-7.2) < 1e-6
    q = np.array([1320., 1400.]); x = np.array([1000., 5000.])
    checks["conversion_opt_radio_identity"] = bool(np.allclose(conv(x,q,"OPT")/conv(x,q,"RADIO"), (NU0/(q*1e6))**2, rtol=1e-14))
    checks["known_flux_ratio_sign"] = abs(stats(np.log10(np.full(12, .5)))["median_dex"]-math.log10(.5)) < 1e-14
    checks["agreement_decision_identity"] = assess(stats(np.zeros(12))) == "compatible within 0.10 dex band"
    checks["deficit_decision_identity"] = assess(stats(np.full(12, -.3))).startswith("lower")
    checks["insufficient_sample_guard"] = assess(stats(np.zeros(3))) == "insufficient pairs"
    a = pd.DataFrame({"RA_deg": [150., 150.1], "Dec_deg": [2.,2.], "freq_MHz": [1400.,1400.]})
    b = pd.DataFrame({"ra": [150.1,150.], "dec": [2.,2.], "v_opt": C*(NU0/(np.array([1400.,1400.])*1e6)-1)})
    mm, _ = match(a,b)
    checks["shuffled_rows_known_matching"] = {(int(r.i),int(r.j)) for _,r in mm.iterrows()} == {(0,1),(1,0)}
    assert all(checks.values()), checks
    return checks


def make_rows(m, f, cube, old, fmap, science, radius=60):
    pairs, candidates = match(m, f, radius)
    mc = C*(NU0/(m.freq_MHz.to_numpy()*1e6)-1)
    cidx, aidx = cube.set_index("ID"), old.set_index("ID")
    famap = fmap.set_index("FASHI_ID")
    rows = []
    for _, p in pairs.iterrows():
        i,j = int(p.i),int(p.j); a,b = m.iloc[i],f.iloc[j]; ident = a.ID_catalogue
        neighbors_m = (sep(b.ra,b.dec,m.RA_deg.to_numpy(),m.Dec_deg.to_numpy()) <= 174)
        neighbors_m &= np.abs(mc-b.v_opt) <= .5*(m.W_50_km_s.to_numpy()+b.W_50)+200
        neighbors_m[i] = False
        neighbors_f = (sep(b.ra,b.dec,f.ra.to_numpy(),f.dec.to_numpy()) <= 174)
        neighbors_f &= np.abs(f.v_opt.to_numpy()-b.v_opt) <= .5*(f.W_50.to_numpy()+b.W_50)+200
        neighbors_f[j] = False
        r = {"ID": ident, "fashi_id": int(b.fashi_id), "sep_arcsec": float(p.sep_arcsec), "dv_kms": float(p.dv_kms),
             "n_m_candidates": int(p.n_m_candidates), "n_f_candidates": int(p.n_f_candidates), "science47": ident in science,
             "z_m_freq": mc[i]/C, "ra_m": a.RA_deg, "dec_m": a.Dec_deg, "ra_f": b.ra, "dec_f": b.dec,
             "z_f": b.z_opt, "f_snr": b.snr, "m_snr": a.SNR_3D,
             "golden_m": bool((a[FLAGS].to_numpy(dtype=float)==0).all()),
             "unique_match": p.n_m_candidates==1 and p.n_f_candidates==1,
             "f_busy": b.S_bf/1000, "f_sum": b.S_sum/1000, "f_err": b.S_err/1000,
             "W50_m": a.W_50_km_s, "W50_f": b.W_50,
             "log_width_m_f": np.log10(a.W_50_km_s/b.W_50) if a.W_50_km_s>0 and b.W_50>0 else np.nan,
             "conf_m": int(neighbors_m.sum()), "conf_f": int(neighbors_f.sum()),
             "neighbor_m_IDs": ";".join(m.loc[neighbors_m,"ID_catalogue"]),
             "cube_primary": False, "cube_detected": False, "alfalfa": np.nan, "agc": np.nan, "alf_code": np.nan,
             "cube_flagged": False, "agc_link_agrees": None}
        if ident in aidx.index:
            aa=aidx.loc[ident];r.update(alfalfa=aa.s21_jykms,agc=int(aa.agc),alf_code=int(aa.hi_code))
        if int(b.fashi_id) in famap.index:
            aa=famap.loc[int(b.fashi_id)]
            if isinstance(aa,pd.DataFrame):
                r["n_fashi_alfalfa_links"]=len(aa)
                same=aa[aa.AGCNr==r["agc"]]
                aa=same.iloc[0] if len(same) else aa.iloc[0]
            if np.isfinite(r["agc"]):r["agc_link_agrees"]=int(aa.AGCNr)==int(r["agc"])
            r["fashi_link_alfalfa"]=aa.ALFALFA_S/1000
        cc=cidx.loc[ident] if ident in cidx.index else None
        if cc is not None:
            r["cube_primary"]=truth(cc.primary);r["cube_detected"]=truth(cc.detected)
            r["cube_flagged"]=any(truth(cc[k]) for k in ["BEAMFLAG","STITCH","EDGE","NAN","TRUNC","NBFLAG"])
        for mode in ["OPT","REST","RADIO"]:
            r["m_"+mode]=float(conv(a.S_HI_Jy_Hz,a.freq_MHz,mode))
            r["m_err_"+mode]=float(conv(a.S_HI_Jy_Hz_err,a.freq_MHz,mode))
            r["cube_"+mode]=float(conv(cc.S_win_Jy_Hz,a.freq_MHz,mode)) if cc is not None else np.nan
            r["beam_sum_"+mode]=r["m_"+mode]+float(np.sum(conv(m.loc[neighbors_m,"S_HI_Jy_Hz"],m.loc[neighbors_m,"freq_MHz"],mode)))
            for fn in ["busy","sum"]:
                for label in ["m","cube","beam_sum"]:
                    val=r[label+"_"+mode];ref=r["f_"+fn]
                    r[f"R_{label}_{mode}_{fn}"]=np.log10(val/ref) if val>0 and ref>0 else np.nan
        r["R_alf_f_busy"]=np.log10(r["alfalfa"]/r["f_busy"]) if r["alfalfa"]>0 and r["f_busy"]>0 else np.nan
        r["R_alf_f_sum"]=np.log10(r["alfalfa"]/r["f_sum"]) if r["alfalfa"]>0 and r["f_sum"]>0 else np.nan
        r["R_m_alf_OPT"]=np.log10(r["m_OPT"]/r["alfalfa"]) if r["alfalfa"]>0 else np.nan
        r["R_busy_sum"]=np.log10(r["f_busy"]/r["f_sum"]) if r["f_busy"]>0 and r["f_sum"]>0 else np.nan
        r["reliable"]=bool(r["golden_m"] and r["unique_match"] and b.snr>=10 and r["f_busy"]>0 and r["m_OPT"]>0)
        r["clean"]=bool(r["reliable"] and not r["conf_m"] and not r["conf_f"])
        rows.append(r)
    return pd.DataFrame(rows), candidates


def summarize(d):
    masks={"all_matches":np.ones(len(d),bool),"reliable_parent":d.reliable.to_numpy(),"clean_parent":d.clean.to_numpy(),
           "science47_matched":d.science47.to_numpy(),"science47_reliable":(d.science47 & d.reliable).to_numpy(),
           "science47_clean":(d.science47 & d.clean).to_numpy(),
           "reliable_width_consistent":(d.reliable & (d.log_width_m_f.abs()<=.15)).to_numpy()}
    out={}
    for name,mask in masks.items():
        q=d.loc[mask]; st={"n":len(q),"cat":{},"cube":{},"beam_sum":{}}
        for mode in ["OPT","REST","RADIO"]:
            for fn in ["busy","sum"]:
                key=mode+"_"+fn
                for label in ["m","cube","beam_sum"]:
                    qq=q if label!="cube" else q[q.cube_primary & q.cube_detected]
                    ss=stats(qq[f"R_{label}_{mode}_{fn}"]);ss["assessment"]=assess(ss,5 if label=="cube" else 8)
                    st[{"m":"cat","cube":"cube","beam_sum":"beam_sum"}[label]][key]=ss
        st["width"]=stats(q.log_width_m_f)
        st["busy_vs_sum"]=stats(q.R_busy_sum)
        # These use the SAME objects in each ratio, rather than unrelated medians.
        tri=q[(q.alf_code==1) & q.alfalfa.notna() & q.R_alf_f_busy.notna()]
        st["triple_code1"]={"n":len(tri),"MIGHTEE_over_FAST":stats(tri.R_m_OPT_busy),
                              "ALFALFA_over_FAST":stats(tri.R_alf_f_busy),"MIGHTEE_over_ALFALFA":stats(tri.R_m_alf_OPT),
                              "ALFALFA_over_FAST_sum":stats(tri.R_alf_f_sum)}
        for ss in st["triple_code1"].values():
            if isinstance(ss,dict):ss["assessment"]=assess(ss)
        out[name]=st
    return out


def shifted(ra,de,angle):
    d=np.radians(10/60);lat=np.radians(de);lon=np.radians(ra)
    ll=np.arcsin(np.sin(lat)*np.cos(d)+np.cos(lat)*np.sin(d)*np.cos(angle))
    rr=lon+np.arctan2(np.sin(angle)*np.sin(d)*np.cos(lat),np.cos(d)-np.sin(lat)*np.sin(ll))
    return np.degrees(rr)%360,np.degrees(ll)


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--output",required=True);args=ap.parse_args()
    out=ROOT/args.output;out.mkdir(parents=True,exist_ok=True)
    check=controls()
    m=pd.read_csv(ROOT/CAT);full=pd.read_csv(ROOT/FAST);fa=pd.read_csv(ROOT/FA)
    cube=pd.read_csv(ROOT/CUBE);old=pd.read_csv(ROOT/OLD)
    science=set(json.loads((ROOT/SCIENCE).read_text())["numbers"]["survivor_ids"])
    assert len(m)==293 and m.ID_catalogue.is_unique and len(science)==47 and science<=set(m.ID_catalogue)
    assert len(full)==156411 and full.fashi_id.is_unique and len(fa)==28352
    box=full.ra.between(m.RA_deg.min()-1,m.RA_deg.max()+1)&full.dec.between(m.Dec_deg.min()-1,m.Dec_deg.max()+1)
    f=full.loc[box].reset_index(drop=True)
    d,candidates=make_rows(m,f,cube,old,fa,science)
    assert len(d)>0 and d.ID.is_unique and d.fashi_id.is_unique
    summaries=summarize(d)
    d.to_csv(out/"matched_sources.csv",index=False,float_format="%.12g")
    candidates["ID"]=m.iloc[candidates.i.to_numpy()].ID_catalogue.to_numpy()
    candidates["fashi_id"]=f.iloc[candidates.j.to_numpy()].fashi_id.to_numpy()
    candidates.to_csv(out/"all_candidates.csv",index=False,float_format="%.12g")
    coverage=m[["ID_catalogue","RA_deg","Dec_deg","freq_MHz","z_HI"]].copy()
    coverage["science47"]=coverage.ID_catalogue.isin(science)
    coverage["matched"]=coverage.ID_catalogue.isin(d.ID)
    coverage["beyond_fashi_z_limit"]=NU0/(coverage.freq_MHz*1e6)-1 > full.z_opt.max()
    coverage.to_csv(out/"coverage.csv",index=False)
    sens={}
    for radius in [30,90]:
        v,_=make_rows(m,f,cube,old,fa,science,radius)
        sens[str(radius)]=summarize(v)
        v.to_csv(out/f"matches_radius_{radius}.csv",index=False,float_format="%.12g")
    rng=np.random.default_rng(SEED);counts=[]
    for _ in range(200):
        ra,de=shifted(m.RA_deg.to_numpy(),m.Dec_deg.to_numpy(),rng.uniform(0,2*np.pi,len(m)))
        p,_=match(m,f,ra=ra,de=de);counts.append(len(p))
    # Independent Cartesian dot-product check of the matched separations.
    def xyz(ra,de):
        rr,dd=np.radians(ra),np.radians(de)
        return np.column_stack([np.cos(dd)*np.cos(rr),np.cos(dd)*np.sin(rr),np.sin(dd)])
    ss=np.degrees(np.arccos(np.clip(np.sum(xyz(d.ra_m,d.dec_m)*xyz(d.ra_f,d.dec_f),axis=1),-1,1)))*3600
    separation_max_difference=float(np.max(np.abs(ss-d.sep_arcsec)))
    check["independent_spherical_geometry"]=separation_max_difference<.001
    check["OPT_REST_per_object_identity"]=bool(np.allclose(d.m_OPT/d.m_REST,1+d.z_m_freq,rtol=1e-13))
    check["doubling_flux_shifts_logratio"]=bool(np.allclose(np.log10(2*d.m_OPT/d.f_busy)-d.R_m_OPT_busy,np.log10(2),atol=1e-13))
    tri=d[d.alfalfa.notna()]
    check["paired_three_survey_closure"]=bool(np.allclose(tri.R_m_OPT_busy-tri.R_m_alf_OPT,tri.R_alf_f_busy,atol=1e-13))
    oldlookup=old.set_index("ID")
    e=[abs(r.m_OPT-oldlookup.loc[r.ID,"S_cat_OPT"]) for _,r in tri.iterrows()]
    check["MIGHTEE_conversion_reproduces_old_lane"]=bool(max(e,default=0)<1e-8)
    agc=d.agc_link_agrees.dropna()
    diagnostic={"independent_sky_difference_arcsec":separation_max_difference,
                "FASHI_ALFALFA_ID_links_agree":int(agc.sum()),"FASHI_ALFALFA_ID_links_checked":len(agc),
                "shuffle_mean_pairs":float(np.mean(counts)),"shuffle_max_pairs":max(counts),"shuffle_counts":counts,
                "median_abs_dv_kms":float(d.dv_kms.abs().median()),"median_separation_arcsec":float(d.sep_arcsec.median()),
                "duplicate_candidate_pairs":int(((candidates.n_m_candidates>1)|(candidates.n_f_candidates>1)).sum())}
    trends={}
    q=d[d.reliable]
    for x in ["f_snr","z_m_freq","m_snr"]:
        if len(q)>=4:
            rho,p=spearmanr(q[x],q.R_m_OPT_busy);trends[x]={"rho":float(rho),"p_descriptive":float(p),"n":len(q)}
    results={"contract":"reviews/fashi_mightee_flux_2026_10_18/contract.json","checks":check,
             "counts":{"MIGHTEE_parent":len(m),"science_sample":47,"FASHI_total":len(full),"FASHI_local_box":len(f),
                       "candidate_pairs":len(candidates),"matched":len(d),"science_matched":int(d.science47.sum()),
                       "science_beyond_fashi_limit":int((coverage.science47 & coverage.beyond_fashi_z_limit).sum())},
             "summaries":summaries,"radius_sensitivities":sens,"diagnostics":diagnostic,"descriptive_trends":trends,
             "interval_scope":"Object bootstrap only; common calibration floors and selection/confusion uncertainty not included",
             "non_claims":["No a0 measurement or gravity-model comparison","No assumed correction for unmatched science objects"]}
    def clean(v):
        if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
        if isinstance(v,list):return [clean(x) for x in v]
        if isinstance(v,(float,np.floating)):return float(v) if np.isfinite(v) else None
        if isinstance(v,np.integer):return int(v)
        if isinstance(v,np.bool_):return bool(v)
        return v
    (out/"results.json").write_text(json.dumps(clean(results),indent=2,allow_nan=False))
    lines=["FASHI DR2 and MIGHTEE COSMOS flux comparison",json.dumps(results["counts"]),
           "Median log10(numerator/reference); intervals are object-bootstrap 95 percent, exclude common calibration errors."]
    for name,st in summaries.items():
        for group,key in [("cat","OPT_busy"),("cat","OPT_sum"),("cat","RADIO_busy"),("cube","OPT_busy")]:
            a=st[group][key];lines.append(f"{name}: {group}/{key}: {a}")
        lines.append(f"{name}: same-object ALFALFA code-1 triple: {st['triple_code1']}")
    lines.append("Checks: "+json.dumps(check));lines.append("Diagnostics: "+json.dumps({k:v for k,v in diagnostic.items() if k!="shuffle_counts"}))
    (out/"report.txt").write_text("\n".join(lines)+"\n")
    fig,axs=plt.subplots(2,2,figsize=(12,9),layout="constrained")
    a=axs[0,0];good=d[d.reliable]
    for flag,label,color in [(False,"Other parent sources","#64748b"),(True,"Original science sample","#d95f02")]:
        z=good[good.science47==flag];a.scatter(z.f_busy,z.m_OPT,label=f"{label} (N={len(z)})",c=color,s=34,alpha=.8)
    vals=np.concatenate([good.f_busy,good.m_OPT]);low=max(float(np.min(vals))*.6,.001);high=float(np.max(vals))*1.6
    xx=np.array([low,high]);a.plot(xx,xx,"k--",lw=1);a.plot(xx,.5*xx,color="#cbd5e1",ls=":")
    a.set(xscale="log",yscale="log",xlim=(low,high),ylim=(low,high),xlabel="FAST busy-function flux (Jy km/s)",ylabel="MIGHTEE catalogue flux (Jy km/s)",title="Reliable matches, nominal OPT convention");a.legend(fontsize=8)
    a=axs[0,1];tri=good[(good.alf_code==1)&good.alfalfa.notna()]
    for _,r in tri.iterrows():a.plot([0,1,2],[r.R_m_OPT_busy,0,r.R_alf_f_busy],c="#94a3b8",alpha=.45,lw=.8)
    if len(tri):
        yy=[np.median(tri.R_m_OPT_busy),0,np.median(tri.R_alf_f_busy)]
        a.plot([0,1,2],yy,"o-",c="#0f766e",lw=3,label="Median on identical galaxies")
    a.axhspan(-.1,.1,color="#d1fae5",alpha=.5);a.axhline(0,c="k",ls="--",lw=1)
    a.set(xticks=[0,1,2],xticklabels=["MIGHTEE","FAST","ALFALFA"],ylabel="log10(flux / FAST flux)",title=f"Same-object three-survey comparison (N={len(tri)})");a.legend(fontsize=8)
    a=axs[1,0]
    for flag,label,color in [(False,"Other parent sources","#64748b"),(True,"Science sample","#d95f02")]:
        z=good[good.science47==flag];a.scatter(z.f_snr,z.R_m_OPT_busy,c=color,s=34,label=label)
    a.axhspan(-.1,.1,color="#d1fae5",alpha=.5);a.axhline(0,c="k",ls="--",lw=1)
    a.set(xscale="log",xlabel="FAST signal-to-noise ratio",ylabel="log10(MIGHTEE / FAST flux)",title="Detection-threshold diagnostic");a.legend(fontsize=8)
    a=axs[1,1];names=["reliable_parent","clean_parent","science47_reliable","science47_clean"]
    for y,name in enumerate(names):
        for delta,group,key,col in [(-.12,"cat","OPT_busy","#0f766e"),(.12,"cat","OPT_sum","#b45309")]:
            s=summaries[name][group][key]
            if s["n"]:
                med=s["median_dex"];lo,hi=s["ci95_dex"];a.errorbar(med,y+delta,xerr=[[med-lo],[hi-med]],fmt="o",color=col,capsize=3)
    a.axvspan(-.1,.1,color="#d1fae5",alpha=.5);a.axvline(0,color="k",ls="--",lw=1)
    a.set(yticks=range(4),yticklabels=[f"{n.replace('_',' ')} (N={summaries[n]['n']})" for n in names],xlabel="Median log10(MIGHTEE / FAST), 95% bootstrap",title="Busy fit (green) versus direct sum (brown)");a.invert_yaxis()
    fig.suptitle("FASHI DR2 versus existing MIGHTEE COSMOS measurements",fontsize=15)
    fig.savefig(out/"flux_comparison.png",dpi=160);plt.close(fig)
    assert all(check.values()),check
    print(json.dumps(results["counts"],indent=2))
    for n in ["reliable_parent","clean_parent","science47_reliable","science47_clean"]:
        print(n,json.dumps(summaries[n]["cat"]["OPT_busy"]),"TRIPLE",json.dumps(summaries[n]["triple_code1"]))
    print("All implementation controls passed:",len(check))


if __name__=="__main__":
    main()
