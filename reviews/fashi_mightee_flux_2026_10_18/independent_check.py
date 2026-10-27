#!/usr/bin/env python3
"""Independent stdlib-only catalogue matching and flux-median verification.
Run: python3 reviews/fashi_mightee_flux_2026_10_18/independent_check.py
Does not import the analysis implementation, pandas, scipy, or numpy.
"""
import csv
import json
import math
from collections import Counter
from pathlib import Path
from statistics import median

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent


def read(p):
    with open(ROOT/p) as f:return list(csv.DictReader(f))


def yes(x):return str(x).lower() in ("true","1","1.0")


def vector(ra,dec):
    r,d=math.radians(ra),math.radians(dec)
    return math.cos(d)*math.cos(r),math.cos(d)*math.sin(r),math.sin(d)


def angle(u,v):
    cross=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
    return math.degrees(math.atan2(math.sqrt(sum(x*x for x in cross)),sum(x*y for x,y in zip(u,v))))*3600


def main():
    m=read('data_assembly/mightee_hi_catalogue_2026-10-02/MIGHTEE_HI_COSMOS_catalogue.csv')
    f=read('_external_data/fashi_dr2_2026_10_18/fashi_dr2.csv')
    candidates=[]
    for i,a in enumerate(m):
        ra,dec=float(a['RA_deg']),float(a['Dec_deg'])
        v=299792.458*(1420.40575177/float(a['freq_MHz'])-1)
        av=vector(ra,dec)
        for b in f:
            if abs(float(b['ra'])-ra)>.1 or abs(float(b['dec'])-dec)>.1:continue
            dv=v-float(b['v_opt'])
            if abs(dv)>300:continue
            s=angle(av,vector(float(b['ra']),float(b['dec'])))
            if s<=60:candidates.append((s,abs(dv),i,int(b['fashi_id']),b))
    cm=Counter(x[2] for x in candidates);cf=Counter(x[3] for x in candidates)
    mm,ff=set(),set();pairs=[]
    for s,dv,i,k,b in sorted(candidates,key=lambda x:x[:4]):
        if i in mm or k in ff:continue
        mm.add(i);ff.add(k);pairs.append((i,k,b,s))
    observed=read('reviews/fashi_mightee_flux_2026_10_18/run_02/matched_sources.csv')
    expected={(a['ID'],int(a['fashi_id'])) for a in observed}
    actual={(m[i]['ID_catalogue'],k) for i,k,b,s in pairs}
    assert actual==expected,(actual^expected)
    out=json.loads((HERE/'run_02/results.json').read_text())
    assert len(candidates)==out['counts']['candidate_pairs']
    science=set(json.loads((ROOT/'campaign_fresh_gravity/CFG301_mightee_hi_catalogue_width_chain/cfg301_stageA_results.json').read_text())['numbers']['survivor_ids'])
    flags=['low_confidence_flag','blended_flag','confused_flag','bad_ellipse_flag','contaminated_source_flag']
    primary=[];science_primary=[]
    maxsep=0
    od={r['ID']:r for r in observed}
    for i,k,b,s in pairs:
        a=m[i];nu=float(a['freq_MHz'])*1000000
        flux=float(a['S_HI_Jy_Hz'])*299792.458/nu*(1420.40575177e6/nu)
        val=math.log10(flux/(float(b['S_bf'])*.001))
        r=od[a['ID_catalogue']]
        assert abs(val-float(r['R_m_OPT_busy']))<1e-10
        maxsep=max(maxsep,abs(s-float(r['sep_arcsec'])))
        reliable=cm[i]==1 and cf[k]==1 and float(b['snr'])>=10 and all(float(a[t])==0 for t in flags)
        assert reliable==yes(r['reliable'])
        if reliable:
            primary.append(val)
            if a['ID_catalogue'] in science:science_primary.append(val)
    for name,values in [('reliable_parent',primary),('science47_reliable',science_primary)]:
        ss=out['summaries'][name]['cat']['OPT_busy']
        assert len(values)==ss['n']
        assert abs(median(values)-ss['median_dex'])<1e-12
    result={'status':'passed','implementation':'stdlib csv, Cartesian cross/dot angular separation, statistics.median; no imported analysis code',
            'candidate_pairs':len(candidates),'matched':len(pairs),'reliable_parent':len(primary),'science47_reliable':len(science_primary),
            'median_parent_dex':median(primary),'median_science_dex':median(science_primary),'maximum_separation_difference_arcsec':maxsep,
            'scope':'Independently verifies candidate pairs, one-to-one matching, reliable-sample membership, per-source flux conversion and median ratios. Does not independently validate bootstraps or confusion filtering.'}
    (HERE/'independent_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
