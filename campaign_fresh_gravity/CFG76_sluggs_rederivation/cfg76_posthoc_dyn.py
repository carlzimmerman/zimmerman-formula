"""POST-HOC (declared as such, after the pre-declared run): distance mode 'dyn' (M_JAM ~ D; the spec's INTERPRETATION 3 alternative) x both kernels,
compared per galaxy with CFG55's committed per-galaxy offsets/masses, plus CFG55's reported variant rows."""
import json, math, numpy as np, os, io, contextlib
src=open('cfg76_sluggs_jam.py').read(); src=src[:src.index('ALL = {}')]
os.environ['MUTATE']='0'
g={'__file__':os.path.abspath('cfg76_sluggs_jam.py'),'__name__':'x'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src,'cfg76','exec'),g)
ref=json.load(open('/Users/carlzimmerman/new_physics/zimmerman-formula/campaign_fresh_gravity/CFG55_sluggs_dynamical_masses_results.json'))['numbers']
names=[int(n[3:]) for n in ref['names']]
BINS=g['make_bins'](g['load_gcs'](True)[0]); run=g['run']; summ=g['summ']; fmt=g['fmt']
def P(*a): print(*a)
for kn in ('nu_mono','nu_rar'):
    for f in ('canonical','alt'):
        r=run(names,kn,f,dist_mode='dyn')
        for kind in ('law','rule'):
            a=np.array([r[kind][n] for n in names]); b=np.array(ref['RES'][f][kind]['per'])
            P(f"{kn:8s} {f:9s} {kind:4s}: mean {a.mean():.6f} ref {b.mean():.6f} (d {a.mean()-b.mean():+.1e}); per-gal max|d| {np.abs(a-b).max():.1e}; err ddof1 {a.std(ddof=1)/4:.5f} ref {ref['RES'][f][kind]['err']:.5f}; sigma {a.mean()/(a.std(ddof=1)/4):.3f} vs {b.mean()/ref['RES'][f][kind]['err']:.3f}")
P("\nreported variants (canonical), kernel nu_rar vs nu_mono, dyn distance:")
for kn in ('nu_rar','nu_mono'):
    s=summ(run(names,kn,'canonical',dist_mode='dyn',fmode='hern')); P(kn,'Hernquist fraction:',fmt(s),' | CFG55:',ref['R4_hernquist'])
    s=summ(run(names,kn,'canonical',dist_mode='dyn',salp=True)); P(kn,'Salpeter pop:',fmt(s),' | CFG55:',ref['R3_population']['Salpeter'])
    r=run(names,kn,'canonical',dist_mode='dyn'); s=summ(r,[n for n in names if n!=7457]); P(kn,'w/o 7457:',fmt(s),' | CFG55 post hoc:',ref['R5_posthoc_inrange']['canonical'])
    r=run(names,kn,'canonical',dist_mode='dyn',sluggs_mass=True); P(kn,'SLUGGS masses:',fmt(summ(r)))
    g['JAMF']=0.5; r=run(names,kn,'canonical',dist_mode='dyn'); g['JAMF']=1.0; P(kn,'JAM x0.5:',fmt(summ(r)), 'excluded',r['excl'])
