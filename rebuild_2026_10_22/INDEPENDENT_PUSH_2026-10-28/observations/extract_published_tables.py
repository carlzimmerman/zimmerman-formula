#!/usr/bin/env python3
"""Recreate small X-ray tables from pinned PDFs. Requires Poppler pdftotext.

This writes only the two derived CSV files. The Taibi JSON is a documented
manual extraction of section6.2 p17. Check the recovered tables visually.
"""
import csv, subprocess, re
from pathlib import Path
HERE=Path(__file__).resolve().parent
def pdftext(name):
    return subprocess.check_output(['pdftotext','-layout',str(HERE/'sources'/name),'-'],text=True)
text=pdftext('babyk2018_arxiv_v1.pdf')
lines=text.splitlines()
rows=[]
for n,label,loc in [(4486,'M87','Tables 1-3; pp4 7 10'),(4365,'NGC4365','Tables 1-3; pp3 6 9'),
                     (4374,'NGC4374','Tables 1-3; pp3 6 9'),(5846,'NGC5846','Tables 1-3; pp4 7 10')]:
    # Source table1 has NH range with slash, table2 first value is 5Re,
    # table3 first two values beta and rc; classify by token syntax.
    ls=[l.strip() for l in lines if re.match(r'^\s*NGC'+str(n)+r'\s',l)]
    t1=[l for l in ls if '/' in l and '±' not in l][0]
    da=t1.split()[-3].rstrip('*')
    numeric=re.compile(r'^NGC'+str(n)+r'\s+([\d.]+)±([\d.]+)\s+([\d.]+)±([\d.]+)')
    t2,t3=None,None
    for l in ls:
        m=numeric.match(l)
        if not m:continue
        if float(m[1])>2:t2=(l,m)
        else:t3=(l,m)
    assert t2 and t3,(n,ls)
    l,m=t2; ap,ae,t,te=m.groups(); stat=l.split()[-2]
    l,m=t3; beta,be,rc,re_=m.groups(); chi=l.split()[4]
    rows.append(dict(name=label,ngc=n,kT_keV=t,kT_error_keV=te,aperture_kpc=ap,aperture_error_kpc=ae,DA_Mpc=da,
        beta=beta,beta_error=be,rc_kpc=rc,rc_error_kpc=re_,spectral_stat_per_dof=stat,beta_chi2=chi,beta_dof=96,
        source='Babyk2018_arxiv1803.00020v1',locator=loc))
with (HERE/'sluggs_xray_inputs.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

text=pdftext('clogs2017_v2.pdf')
text=text[text.index('    H IGH -R ICHNESS SUBSAMPLE'):text.index('    L OW-R ICHNESS SUBSAMPLE')]
pat=re.compile(r'^\s*(\d+)\s+(NGC \d+|ESO 507-25)\s+(\d\d) (\d\d) ([\d.]+)\s+([+-]\d\d) (\d\d) (\d\d)\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+(\d+)',re.M)
# Table3 morphology and Table4 asymmetric temperature errors require inspecting
# linewrapped entries; these explicitly transcribed fields have source locators.
grp={9,18,31,42,72,103,117,158,278,338,363,393,402,473};gal={66,185,262}
Ts={9:(.88,.03,.02),18:(.98,.02,.02),31:(.79,.01,.01),42:(.89,.02,.02),58:(.41,.03,.04),66:(.49,.11,.15),
    72:(1.02,.01,.01),103:(.74,.03,.03),117:(.37,.06,.08),158:(1.25,.01,.01),185:(.44,.11,.27),262:(.56,.07,.04),
    276:(.71,.10,.08),278:(1.36,.02,.03),338:(1.28,.01,.01),363:(.72,.01,.01),393:(.95,.01,.01),402:(.59,.01,.01),
    421:(.29,.06,.08),473:(1.,.01,.01)}
rows=[]
for m in pat.finditer(text):
    g,name,h,mi,s,dd,dm,ds,z,d,scale,rich=m.groups();g=int(g)
    ra=15*(int(h)+int(mi)/60+float(s)/3600)
    de=(-1 if dd.startswith('-') else 1)*(abs(int(dd))+int(dm)/60+int(ds)/3600)
    tx,lo,hi=Ts.get(g,('','',''))
    rows.append(dict(LGG=g,BGE=name,ra_deg=ra,dec_deg=de,z=z,D_Mpc=d,richness=rich,
        gas_morphology='GRP' if g in grp else ('gal' if g in gal else 'pnt_or_no_extended'),
        kT_keV=tx,kT_lower_error_keV=lo,kT_upper_error_keV=hi,source='OSullivan2017_arxiv1708.03555v2_Tables1_3_4'))
assert len(rows)==26
with (HERE/'clogs_highrichness_inputs.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Extracted 4 SLUGGS temperatures + beta fits; 26 CLoGS positions, with source-pinned morphology/temperature transcription.')
