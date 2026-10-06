import ast,math,numpy as np,pathlib,json,argparse,hashlib
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',action='store_true');args=p.parse_args();base=pathlib.Path(__file__).resolve().parent;source=base/'reference_integrate.py';ns={'math':math,'K':1.,'H':1.};tree=ast.parse(source.read_text());exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ['response','equations']],type_ignores=[]),str(source),'exec'),ns)
rows=[];checks=[]
for factor in [10.,30.]:
 m=1e-12;A=1.;eta=.5;L=math.sqrt(m*A);r=factor*math.sqrt(m/A);s=m/r**2;a=math.sqrt(s*(s+A));k=r*a;w=eta*(1+s/A);y=np.array([0.,math.log1p(k),w,k]);f=lambda x:np.array(ns['equations'](r,x,eta,A)[0]);mus=a/math.hypot(a,A/2);principal2=eta*k*mus/(r*r*w**3*(1-mus));freq=[]
 for refinement in [.5,1.,2.]:
  steps=np.array([L*1e-3,L*1e-3,1e-4,L*1e-3])*refinement;J=np.column_stack([(f(y+np.eye(4)[i]*steps[i])-f(y-np.eye(4)[i]*steps[i]))/(2*steps[i]) for i in range(4)]);ev=np.linalg.eigvals(J);fast=max(ev,key=lambda z:abs(z.imag));freq.append(abs(fast.imag));rows.append({'factor':factor,'r':r,'refinement':refinement,'J':J.tolist(),'eigenvalues':[[float(z.real),float(z.imag)] for z in ev],'RHS_at_trial':f(y).tolist(),'principal_omega2':principal2,'fast_frequency':abs(fast.imag),'fast_realpart':fast.real})
  checks.append({'name':'oscillatory_damped_frozen_pair_'+str((factor,refinement)),'passed':bool(fast.imag!=0 and fast.real<0)})
 checks.append({'name':'finite_difference_frequency_convergence_'+str(factor),'passed':bool(max(freq)-min(freq)<.003*max(freq))})
 checks.append({'name':'leading_frequency_not_zero_'+str(factor),'passed':principal2>0})
# Exact leading fast matrix eigen-square=-omega², not positive real growth.
mu_control=-mus if args.control else mus
upper=1/(r*r*w);lower=-eta*k*mu_control/(w*w*(1-mu_control))
checks.append({'name':'principal_pair_imaginary','passed':bool(upper*lower<0)})
result={'checks':checks,'rows':rows,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'non_claims':['Frozen Jac evaluated at formal trial, not true solution stability','No integrated global branch','Slow eigenvalues sensitive and not classified','No universal damping theorem']};pathlib.Path(args.output).write_text(json.dumps(result,indent=2)+'\n');passed=all(x['passed'] for x in checks);print(json.dumps({'passed':passed,'checks':len(checks),'frequencies':[x['fast_frequency'] for x in rows]}));raise SystemExit(0 if passed else 1)
