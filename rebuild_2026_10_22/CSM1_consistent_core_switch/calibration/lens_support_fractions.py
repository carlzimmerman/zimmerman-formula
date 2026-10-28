"""Count actual positive-weight lens interpolation support using captured physical flags, avoiding repeated kernel-call counts."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import pathlib,json,math,io,contextlib,argparse,hashlib,resource,sys
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--runs',nargs='+',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();D=pathlib.Path(__file__).resolve().parent;ROOT=D.parents[2];REB=ROOT/'rebuild_2026_10_22';H={}
def rd(p):p=pathlib.Path(p).resolve();H[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
f2=REB/'F2_outer_lensing/f2_outer_lensing.py';t=f2.read_text();H[str(f2)]=hashlib.sha256(f2.read_bytes()).hexdigest();s=t[:t.index('# ============================================================================ 2. K0')]+t[t.index('# ============================================================================ 4. lens inventory'):t.index('# ============================================================================ 5. Track A')];n={'__file__':str(f2),'__name__':'csm1_fraction_inventory'}
with contextlib.redirect_stdout(io.StringIO()):exec(compile(s,str(f2),'exec'),n)
for p in [ROOT/'real_research/data/lensing_rar/lr_lenses.npz',ROOT/'real_research/data/lensing_rar/cfg110_perlens.npz',ROOT/'campaign_fresh_gravity/CFG885_kids_rar_native_distances/cfg885_results.json']:
 H[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
e=rd(REB/'EM1_emergent_dust_law/em1_emergent_results.json')['rows']['A_c2b_refit']['R1'];bg_a,bg_b=e['a'],e['b'];g=n['LMG'];h=.679
mass=[]
for lm in g:
 lm70=lm-2*np.log10(.70/h);mc=10**(lm+(-.69*lm70+6.63));mass.append(10**(bg_a+bg_b*(math.log10(10**lm+mc)-10)))
res={}
for rp in a.runs:
 r=rd(rp);cells={}
 for L,cell in r['levels'].items():
  feet={}
  for f in ('canonical','alt'):
   rows=[q for q in cell['lens']['core_columns'] if q['footing']==f];flags=[]
   for m in mass:
    near=min(rows,key=lambda q:abs(math.log(q['mass']/m)));assert abs(near['mass']/m-1)<1e-12;flags.append(near['expected'])
   flags=np.asarray(flags,dtype=bool);bins={};union=set();weighted_halo=0.;weights=0.;total_lenses=0;total_node_decisions=0;halo_node_decisions=0
   for b in range(4):
    inv=n['INV'][b];keep=inv['w']>0;w=inv['w'][keep];lm=inv['logMs70'][keep]+2*np.log10(.70/h)+2*np.log10(inv['qDA'][keep]);lo=np.searchsorted(g,lm,side='right')-1;lo=np.clip(lo,0,len(g)-2);hi=lo+1;alpha=np.clip((lm-g[lo])/(g[hi]-g[lo]),0,1)
    lc=1-alpha;hc=alpha;validlo=lc>0;validhi=hc>0;support=set(lo[validlo].tolist()+hi[validhi].tolist());union.update(support);hcount=sum(bool(flags[i]) for i in support);fd=flags[lo]*lc+flags[hi]*hc
    nd=int(validlo.sum()+validhi.sum());hd=int((validlo&flags[lo]).sum()+(validhi&flags[hi]).sum());fully=fd==1;law=fd==0;partial=(fd>0)&(fd<1)
    bins[str(b+1)]=dict(positive_weight_lenses=int(len(w)),support_grid_nodes=len(support),halo_support_grid_nodes=hcount,halo_support_fraction=hcount/len(support),support_min_logMstar=float(g[min(support)]),support_max_logMstar=float(g[max(support)]),positive_interpolation_node_decisions=nd,halo_interpolation_node_decisions=hd,halo_node_decision_fraction=hd/nd,weighted_halo_interpolation_fraction=float(w@fd/w.sum()),fully_halo_lenses=int(fully.sum()),partial_halo_lenses=int(partial.sum()),fully_law_lenses=int(law.sum()))
    weighted_halo+=float(w@fd);weights+=float(w.sum());total_lenses+=len(w);total_node_decisions+=nd;halo_node_decisions+=hd
   feet[f]=dict(bins=bins,unique_support_grid_nodes=len(union),unique_halo_support_grid_nodes=sum(bool(flags[i]) for i in union),unique_halo_support_fraction=sum(bool(flags[i]) for i in union)/len(union),per_bin_support_node_decisions=sum(x['support_grid_nodes'] for x in bins.values()),per_bin_halo_support_node_decisions=sum(x['halo_support_grid_nodes'] for x in bins.values()),positive_weight_lenses=int(total_lenses),positive_interpolation_node_decisions=total_node_decisions,halo_interpolation_node_decisions=halo_node_decisions,halo_node_decision_fraction=halo_node_decisions/total_node_decisions,weighted_halo_interpolation_fraction=weighted_halo/weights,exact_X43_roots={tag:d['roots'] for tag,d in cell['own']['result'][0]['_exact_diagnostics'].items()},coarse_X53_roots=cell['lens']['result']['_table_diagnostics']['roots'])
  cells[L]=feet
 res[str(pathlib.Path(rp).resolve())]=cells
out=pathlib.Path(a.output);out.write_text(json.dumps(dict(assertion_tested='Actual positive-weight interpolation support of the executed X53 estimator, classified from captured physicalhalo_setup flags; node decisions count positive interpolation coefficients, not repeated kernel invocations.',actualRSS_GB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform=='darwin' else 1e6),results=res,input_hashes={p:dict(before=v,after=hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()) for p,v in H.items()}),indent=2)+'\n');print(out)
