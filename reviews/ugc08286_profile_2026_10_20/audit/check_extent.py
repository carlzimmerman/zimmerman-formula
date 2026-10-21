"""Independent finite support/dual checks; existing audit artifacts untouched."""
import argparse,json
from fractions import Fraction as F
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import linprog

ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
out=Path(args.output_dir);p=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(p))
from kernel.disk_kernel import build_annular_kernel
d=np.loadtxt(p/'data/UGC08286_rotmod.dat');r,v,ev,vg,vd=d[:,:5].T
source=json.loads((p/'extent_run/results.json').read_text())
foot=json.loads((p.parents[1]/'real_research/derivation_chain_2026/FP0_core_postulates_results.json').read_text())['numbers']
a0s={'canonical':foot['a0_canonical'],'alt':foot['a0_rho_total']}
gas=vg*np.abs(vg);b0=gas+.5*vd**2
beam=6500*np.deg2rad(30/3600);h=.196*1.05**.633
cache={};matrix_cache={};checks=[]

def frac(x):return F.from_float(float(x))
def exact_certificate(M,b,u):
    # The exact coefficient domain here is the binary64 finite matrix.
    # Original Newtonian/photometric kernels remain approximate inputs.
    Mf=[[frac(t) for t in row] for row in M]
    bf=[frac(t) for t in b];uf=[frac(t) for t in u]
    raww=[sum((Mf[i][j]*uf[i] for i in range(len(uf))),F(0)) for j in range(M.shape[1])]
    rawneg=sum((a*z for a,z in zip(bf,uf)),F(0))
    row={'raw_exact_signs_pass':min(uf)>=0 and min(raww)>=0,
        'raw_exact_negative_margin_pass':rawneg<0,
        'raw_negative_margin_v2':float(rawneg),
        'raw_min_column_margin':float(min(raww)),
        'raw_min_u':float(min(uf)), 'raw_normalization':float(sum(uf))}
    # The outermost target radius is outside or on all source radii. Its
    # upper-inequality coefficients are strictly positive. Adding a small
    # positive weight there repairs roundoff sign defects without assuming
    # any upper bound on source mass. All following tests are exact rational.
    uf=[max(t,F(0)) for t in uf]
    w=[sum((Mf[i][j]*uf[i] for i in range(len(uf))),F(0)) for j in range(M.shape[1])]
    outer=Mf[len(r)-1]
    if min(outer)<=0:
        row['repair_error']='outer row not strictly positive';return row
    t=max([F(0)]+[-z/a for z,a in zip(w,outer)])
    if t>0:t*=F(1000001,1000000)
    uf[len(r)-1]+=t
    repaired=[z+t*a for z,a in zip(w,outer)]
    neg=sum((a*z for a,z in zip(bf,uf)),F(0))
    signs=min(uf)>=0 and min(repaired)>=0
    row.update(repaired_exact_valid=bool(signs and neg<0),
        correction_outer_upper_weight=str(t),correction_weight_float=float(t),
        repaired_exact_negative_margin=str(neg),repaired_negative_margin_v2=float(neg),
        repaired_min_column_margin=float(min(repaired)),
        repaired_normalization=float(sum(uf)),
        u_original=np.asarray(u).tolist())
    return row

for q in source['cases']:
    cut=q['cut_kpc'];hf=q['height_factor'];div=q['beam_divisor'];key=f'cut{cut:.2f}_h{hf}_div{div}'
    if key not in cache:
        n=int(np.ceil(cut/(beam/div)));edges=np.linspace(0,cut,n+1)
        A=build_annular_kernel(r,edges,h*hf,order=192)*1e9
        cache[key]=A;matrix_cache[key]=A;matrix_cache[key+'_edges']=edges
    A=cache[key];a0=a0s[q['footing']]
    base=(b0+np.sqrt(b0*b0+4*a0*r*3.0857e19/1e6*b0))/2
    n=q['nsigma'];lo=np.maximum(v-n*ev,0)**2-base;hi=(v+n*ev)**2-base
    M=np.r_[A,-A];rhs=np.r_[hi,-lo]
    row={k:q[k] for k in ['cut_kpc','height_factor','beam_divisor','annuli','footing','nsigma','status','success']}
    row['matrix_key']=key;assert q['annuli']==A.shape[1]
    if q['success']:
        z=linprog(np.ones(A.shape[1]),A_ub=M,b_ub=rhs,bounds=(0,None),method='highs-ds')
        row['independent_primal_status']=int(z.status)
        if z.success:
            row.update(independent_mass_msun=float(z.fun*1e9),
                saved_minimum_relative_difference=float(abs(z.fun*1e9-q['minimum_mass_msun'])/max(q['minimum_mass_msun'],1)),
                independent_primal_violation=float(max(0,np.max(M@z.x-rhs),-np.min(z.x))),
                independent_masses_billion_msun=z.x.tolist())
    elif q['status']==2:
        row['certificate']=exact_certificate(M,rhs,np.array(q['certificate']['u']))
    else:
        # Preserve the author's primal status4. A separate exact negative
        # certificate, if found, can still establish finite-matrix exclusion.
        z=linprog(rhs,A_ub=-M.T,b_ub=np.zeros(A.shape[1]),
            A_eq=np.ones((1,len(rhs))),b_eq=[1.],bounds=(0,None),method='highs-ds')
        row['independent_dual_status']=int(z.status)
        if z.success:
            row['independent_dual_objective']=float(rhs@z.x)
            row['certificate']=exact_certificate(M,rhs,z.x)
    checks.append(row)

summary={}
for footing in a0s:
    for nsig in (1,2):
        controls=[]
        for hf in (.5,1,2):
            for div in (4,8):
                qs=[q for q in checks if q['footing']==footing and q['nsigma']==nsig and q['height_factor']==hf and q['beam_divisor']==div]
                feasible=[q for q in qs if q.get('independent_primal_status')==0]
                first=min((q['cut_kpc'] for q in feasible),default=None)
                below=[q for q in qs if first is not None and q['cut_kpc']<first]
                controls.append(dict(height_factor=hf,beam_divisor=div,
                    first_independently_feasible_cut_kpc=first,
                    all_smaller_tested_cuts_exactly_excluded=all(q.get('certificate',{}).get('repaired_exact_valid',False) for q in below),
                    smaller_tested_cut_count=len(below),
                    unresolved_smaller_cuts=[q['cut_kpc'] for q in below if not q.get('certificate',{}).get('repaired_exact_valid',False)]))
        summary[f'{footing}_{nsig}']=controls

certs=[q for q in checks if 'certificate' in q]
res={'assertion_tested':'Rebuild all408 finite extent matrices/constraints, independently solve190 saved feasible LPs, check198 saved negative certificates in exact rational arithmetic for binary64 matrices after documented outer-row correction, and attempt separate negative certificates for20 primal-status4 cases.',
    'case_count':len(checks),'summary':summary,'checks':checks,
    'certificate_summary':dict(total=len(certs),raw_exact_signs_pass=sum(q['certificate']['raw_exact_signs_pass'] for q in certs),
        repaired_exact_valid=sum(q['certificate'].get('repaired_exact_valid',False) for q in certs),
        original_status4=len([q for q in checks if q['status']==4]),
        status4_resolved_by_separate_certificate=sum(q['status']==4 and q['certificate'].get('repaired_exact_valid',False) for q in certs),
        minimum_absolute_repaired_negative_margin=min(abs(q['certificate']['repaired_negative_margin_v2']) for q in certs if q['certificate'].get('repaired_exact_valid')),
        maximum_outer_row_correction=max(q['certificate'].get('correction_weight_float',0) for q in certs)),
    'non_claims':['Certificates apply exactly to reconstructed and saved binary64 finite matrices only, not exact continuous Newtonian kernels',
        'No source between tested support cuts or outside these geometry/basis controls is excluded',
        'No physical stellar-gradient restriction, density uniqueness, statistical confidence or lifetime']}
np.savez_compressed(out/'matrices.npz',**matrix_cache)
(out/'checks.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'certificate_summary':res['certificate_summary'],'summary':summary},indent=2))
