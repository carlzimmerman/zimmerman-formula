"""POST-HOC diagnostic (declared as such): which distance treatment reproduces CFG55's committed per-galaxy JAM masses for the 6 galaxies where the pre-declared literal reading differs?"""
import json, math, numpy as np, os, sys
src=open('cfg76_sluggs_jam.py').read(); src=src[:src.index('# ================================================================ C1')]
os.environ['MUTATE']='0'
g={'__file__':os.path.abspath('cfg76_sluggs_jam.py'),'__name__':'x'}
import io,contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src,'cfg76','exec'),g)
ref=json.load(open('/Users/carlzimmerman/new_physics/zimmerman-formula/campaign_fresh_gravity/CFG55_sluggs_dynamical_masses_results.json'))['numbers']
names=[int(n[3:]) for n in ref['names']]
AT=g['AT']; kern=g['nu_rar']; calibrate=g['calibrate']
BINS=g['make_bins'](g['load_gcs'](True)[0])
print("NGC  D_S  D_A  ratio | refLogM | literal(L~D2,r@S) | M~D | L~D2 r@A | L~D2,M/L~1/D...")
def variants(n):
    a=AT[f"NGC{n:04d}"]; D=BINS[n]['D']; DA=a['Dist_Mpc']; L=10**a['logL']; ml=10**a['logML_JAM']
    r_S=10**a['logr12']/g['ARCSEC']*D*1e3; r_A=10**a['logr12']/g['ARCSEC']*DA*1e3
    return {'literal':(ml*L*(D/DA)**2, r_S),'M~D':(ml*L*(D/DA), r_S),'L~D2,r@A':(ml*L*(D/DA)**2, r_A),'noscale':(ml*L, r_A),'M~D,r@A':(ml*L*(D/DA),r_A), 'ML~D/DA,L~D2 (M~D^3)':(ml*(D/DA)*L*(D/DA)**2,r_S)}
res={}
for i,n in enumerate(names):
    b=BINS[n]; a=AT[f"NGC{n:04d}"]
    row=[]
    for k,(MJ,r12) in variants(n).items():
        M,_=calibrate(MJ,r12,b['Re'],'canonical',kern,False); row.append(f"{k}:{math.log10(M):.4f}")
    print(n, f"{b['D']:.1f} {a['Dist_Mpc']:.1f} {b['D']/a['Dist_Mpc']:.3f} | ref {ref['RES']['canonical']['logM_law'][i]:.4f} |", " ".join(row))
