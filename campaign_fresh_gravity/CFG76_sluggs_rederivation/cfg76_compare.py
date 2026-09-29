import json, numpy as np
mine=json.load(open('cfg76_results.json'))
ref=json.load(open('/Users/carlzimmerman/new_physics/zimmerman-formula/campaign_fresh_gravity/CFG55_sluggs_dynamical_masses_results.json'))['numbers']
names=[int(n[3:]) for n in ref['names']]
for f in ('canonical','alt'):
    for k in ('nu_mono','nu_rar'):
        pg=mine['per_galaxy_all'][f'{k}|{f}']
        for kind in ('law','rule'):
            a=np.array([pg[kind][str(n)] for n in names]); b=np.array(ref['RES'][f][kind]['per'])
            d=a-b
            print(f"{f:9s} {k:8s} {kind:4s}: mean mine {a.mean():.5f} ref {b.mean():.5f}; per-galaxy diff max|d| {np.abs(d).max():.5f}, rms {np.sqrt((d**2).mean()):.5f}; err ddof1 {a.std(ddof=1)/4:.5f} ddof0 {a.std()/4:.5f} ref err {ref['RES'][f][kind]['err']:.5f} (ref ddof1 {b.std(ddof=1)/4:.5f}, ddof0 {b.std()/4:.5f})")
        ml=np.array([np.log10(pg['Ms'][str(n)][0]) for n in names]); 
        print("   logM law diff max", np.abs(ml-np.array(ref['RES'][f]['logM_law'])).max(), " rule:", np.abs(np.array([np.log10(pg['Ms'][str(n)][1]) for n in names])-np.array(ref['RES'][f]['logM_rule'])).max())
        sg=np.array([mine['sluggs_per_galaxy'][f'{k}|{f}'][str(n)] for n in names])
        print("   SLUGGS-mass law mean", sg.mean(), "ref", ref['RES'][f]['law_sluggs']['mean'], "err ddof1", sg.std(ddof=1)/4, "ddof0", sg.std()/4, "ref err", ref['RES'][f]['law_sluggs']['err'])
