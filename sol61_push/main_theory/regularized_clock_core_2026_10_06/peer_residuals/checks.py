"""Independent original-Euler residuals on saved states; no trajectory certificate."""
import ast,argparse,json,pathlib,types,hashlib,math
import mpmath as mp
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);pa.add_argument('--control',choices=['none','zero_shift_matter'],default='none');args=pa.parse_args();mp.mp.dps=50
ROOT=pathlib.Path(__file__).resolve().parents[4];PARENT=pathlib.Path(__file__).resolve().parents[1];CORE=PARENT/'core.py';DATA=PARENT/'runs/core_200k_b/results.json'
# Select only these three plain definitions. No source-module import or top-level solver execution.
source=ast.parse(CORE.read_text());names={'operator','material','rhsraw'};nodes=[n for n in source.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(nodes)==3 and not any(n.decorator_list for n in nodes)
class DecimalFloat(ast.NodeTransformer):
 def visit_Constant(self,node):
  if isinstance(node.value,float):return ast.copy_location(ast.Call(ast.Attribute(ast.Name('mp',ast.Load()),'mpf',ast.Load()),[ast.Constant(str(node.value))],[]),node)
  return node
module=ast.fix_missing_locations(DecimalFloat().visit(ast.Module(body=nodes,type_ignores=[])))
class Maths:
 def __getattr__(self,n):return getattr(mp,n)
 @staticmethod
 def copysign(a,b):return abs(a) if b>=0 else -abs(a)
 @staticmethod
 def hypot(a,b):return mp.sqrt(a*a+b*b)
ns={'mp':mp,'math':Maths(),'np':types.SimpleNamespace(array=lambda x:x),'float':mp.mpf,'eta':mp.mpf('.5'),'A':mp.mpf(1),'H':mp.mpf(1),'rho':mp.mpf('6000000'),'p0':mp.mpf(4),'eps':mp.mpf('.01'),'kap':mp.mpf('.99')}
exec(compile(module,str(CORE)+'[three-AST-definitions-only]','exec'),ns)
ns64={'math':math,'np':types.SimpleNamespace(array=lambda x:x),'eta':.5,'A':1.,'H':1.,'rho':6000000.,'p0':4.,'eps':.01,'kap':.99}
nodes64=[n for n in ast.parse(CORE.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
exec(compile(ast.Module(body=nodes64,type_ignores=[]),str(CORE)+'[binary64-three-AST-definitions-only]','exec'),ns64)
checks=[]
def ck(n,b,d=None):checks.append(dict(name=n,passed=bool(b),detail=d))
# Exact constitutive expressions reconstructed independently of core.operator.
def response(a):
 ga=abs(a);root=mp.sqrt(ga*ga+mp.mpf('.25'));s=root-mp.mpf('.5');W=(ga*root+mp.mpf('.25')*mp.asinh(2*ga)-ga)/2
 Q=mp.mpf('.99')*ga*ga-2*W;Qa=2*(mp.mpf('.99')*a-mp.sign(a)*s);Qaa=2*(mp.mpf('.99')-ga/root)
 return Q,Qa,Qaa

def evaluate(node,inside,binary64=False):
 r=mp.mpf(str(node['r']));y=[mp.mpf(str(q)) for q in node['y']];lnN,lnB,w,k=y;dt=[mp.mpf(str(q)) for q in ns64['rhsraw'](math.log(node['r']),node['y'],inside)] if binary64 else ns['rhsraw'](mp.log(r),y,inside);N=mp.exp(lnN);B=mp.exp(lnB);V=-w*r*N;Np=N*k/r;Bp=B*dt[1]/r;Vp=V*(1+k+dt[2]/w)/r;Npp=N*(dt[3]+k*k-k)/(r*r);a=Np/(N*B);ap=Npp/(N*B)-a*(Np/N+Bp/B);Q,Qa,Qaa=response(a);F=N*N-B*B*V*V
 if inside:
  rho=mp.mpf(6000000);p=mp.mpf('6000004')/mp.sqrt(F)-rho
 else:rho=mp.mpf(0);p=mp.mpf(0)
 S=rho+p;energy=S*N*N/F-p;radial=p+S*B*B*V*V/F;U=-3+3*lnN;eta=mp.mpf('.5')
 # Original variations, each term retained for backward relative normalization.
 EN=[B-1/B,2*r*Bp/B**2,((B+2*r*Bp)*V*V+2*r*B*V*Vp)/N**2,2*eta*(Bp*r*r*V+2*B*r*V+B*r*r*Vp)/N,B*r*r*(U+6*eta+Q-a*Qa),-2*r*Qa,-r*r*Qaa*ap,-B*r*r*energy]
 EB=[N*(1-1/B**2),-2*r*Np/B**2,(V*V+2*r*V*Vp)/N,-2*r*V*V*Np/N**2,-2*eta*r*r*V*Np/N,N*r*r*(U+Q-a*Qa),N*r*r*radial]
 shiftmatter=N*B**3*r*r*S*V/F
 EV=[-2*r*V*(Bp/N+B*Np/N**2),-2*eta*B*r*r*Np/N,0 if args.control=='zero_shift_matter' else shiftmatter]
 def norm(terms):return abs(mp.fsum(terms))/mp.fsum(abs(q) for q in terms) if any(terms) else mp.mpf(0)
 Fp=2*N*Np-2*B*Bp*V*V-2*B*B*V*Vp;gexact=Fp/(2*N*B*mp.sqrt(F));q2=B*B*r*r*w*w;gdict=(k*(1-q2)-q2*(dt[1]+1+dt[2]/w))/(r*B*mp.sqrt(1-q2));pprime=-S*Fp/(2*F)
 # Pressure derivative obtained independently by differentiating conservation closed form.
 pclosedprime=-mp.mpf('6000004')*Fp/(2*F**mp.mpf('1.5')) if inside else mp.mpf(0)
 return dict(r=str(r),inside=inside,EL_N_residual=str(mp.fsum(EN)),EL_B_residual=str(mp.fsum(EB)),EL_V_residual=str(mp.fsum(EV)),backward_relative=dict(N=str(norm(EN)),B=str(norm(EB)),V=str(norm(EV))),physical_exact=str(gexact),physical_dictionary=str(gdict),force_dictionary_error=str(abs(gexact-gdict)/(abs(gexact) or 1)),exterior_leading=str(a-V*Vp+r) if not inside else None,stored_exterior_leading_error=str(abs(a-V*Vp+r-mp.mpf(str(node['physical_leading_g'])))/(abs(a-V*Vp+r) or 1)) if not inside else None,background_restored_leading_vs_exact_error=str(abs(a-V*Vp-gexact)/(abs(gexact) or 1)) if not inside else None,leading_vs_exact_force_error=str(abs(a-V*Vp+r-gexact)/(abs(gexact) or 1)) if not inside else None,stored_force_error=str(abs(gexact-mp.mpf(str(node['physical_force'])))/(abs(gexact) or 1)) if inside else None,pressure=str(p),stored_pressure_error=str(abs(p-mp.mpf(str(node['p'])))) if inside else None,fluid_conservation_error=str(abs(pprime-pclosedprime)) if inside else None,shift_matter=str(shiftmatter),F=str(F),clock=str(a),Qaa=str(Qaa))
rows=[];data=json.loads(DATA.read_text());maxes={'N':mp.mpf(0),'B':mp.mpf(0),'V':mp.mpf(0)}
for run in data['runs']:
 interior=run['interior'];exterior=run['samples'];ck('declared_sample_counts_'+str(run['tol']),len(interior)==61 and len(exterior)==41)
 samples=[evaluate(pt,True) for pt in interior]+[evaluate(pt,False) for pt in exterior]
 for name in maxes:
  peak=max(mp.mpf(z['backward_relative'][name]) for z in samples);maxes[name]=max(maxes[name],peak);ck('original_EL_'+name+'_'+str(run['tol']),peak<mp.mpf('1e-18'),str(peak))
 ck('exact_metric_force_dictionary_'+str(run['tol']),max(mp.mpf(z['force_dictionary_error']) for z in samples)<mp.mpf('1e-40'))
 ck('stored_interior_force_rounding_'+str(run['tol']),max(mp.mpf(z['stored_force_error']) for z in samples if z['inside'])<mp.mpf('1e-8'))
 ck('stored_exterior_leading_dictionary_'+str(run['tol']),max(mp.mpf(z['stored_exterior_leading_error']) for z in samples if not z['inside'])<mp.mpf('1e-8'))
 ck('stored_properpressure_rounding_'+str(run['tol']),max(mp.mpf(z['stored_pressure_error']) for z in samples if z['inside'])<mp.mpf('1e-7'))
 ck('static_fluid_conservation_'+str(run['tol']),max(mp.mpf(z['fluid_conservation_error']) for z in samples if z['inside'])<mp.mpf('1e-30'))
 ck('sampled_patch_and_response_'+str(run['tol']),all(mp.mpf(z['F'])>0 and mp.mpf(z['Qaa'])>0 for z in samples))
 rows.append(dict(tol=run['tol'],samples=samples))
binaryrows=[];binarymax={k:mp.mpf(0) for k in maxes}
for run in data['runs']:
 points=[evaluate(pt,True,True) for pt in run['interior']]+[evaluate(pt,False,True) for pt in run['samples']]
 for name in binarymax:
  peak=max(mp.mpf(z['backward_relative'][name]) for z in points);binarymax[name]=max(binarymax[name],peak);ck('binary64_original_EL_'+name+'_'+str(run['tol']),peak<mp.mpf('1e-10'),str(peak))
 binaryrows.append(dict(tol=run['tol'],samples=points))
# Independent highprecision center root: pole-offset coordinates avoid subtractive root conditioning.
eta=mp.mpf('.5');epsilon=mp.mpf('.01');kap=1-epsilon;dens=mp.mpf('6000012');pole=-eta/(3*kap)
poly=lambda x:(3*kap*x+eta)*(dens+6*x*x-6*eta*x-6*(1+eta))-18*epsilon*eta*x*(x+1)
delta=mp.findroot(lambda d:poly(pole-d),(mp.mpf('5e-10'),mp.mpf('9e-10')),tol=mp.mpf('1e-45'));xhigh=pole-delta;n2high=(dens+6*xhigh*xhigh-6*eta*xhigh-6*(1+eta))/(12*epsilon)
xstored=mp.mpf(str(data['center']['x']));n2stored=mp.mpf(str(data['center']['n2']));left=(3*kap*xstored+eta)*n2stored;right=mp.mpf('1.5')*eta*xstored*(xstored+1);absres=abs(left-right);relres=absres/(abs(left)+abs(right))
centerreview=dict(highprecision_x=str(xhigh),highprecision_pole=str(pole),highprecision_pole_offset=str(delta),highprecision_n2=str(n2high),stored_x_minus_highprecision=str(xstored-xhigh),stored_pole_offset_relative_error=str(abs((pole-xstored)/delta-1)),stored_n2_relative_error=str(abs(n2stored/n2high-1)),trace_absolute_residual=str(absres),trace_terms_relative_residual=str(relres),trace_divided_by_1_plus_n2=str(absres/(1+abs(n2stored))),warning='Division by1+n2 is not relative cancellation accuracy. RHS residuals do not bound initial-series remainder.')
xbinary=mp.mpf(data['center']['x']);n2binary=mp.mpf(data['center']['n2']);lb=(3*kap*xbinary+eta)*n2binary;rb=mp.mpf('1.5')*eta*xbinary*(xbinary+1);nativeabs=abs((3*.99*data['center']['x']+.5)*data['center']['n2']-.75*data['center']['x']*(data['center']['x']+1))
centerreview.update(exact_binary64_x=str(xbinary),binary64_trace_absolute_residual_at_exact_physical_coefficients=str(abs(lb-rb)),binary64_trace_terms_relative_residual=str(abs(lb-rb)/(abs(lb)+abs(rb))),native_binary64_trace_absolute_residual=nativeabs,native_binary64_divided_by_1_plus_n2=nativeabs/(1+abs(data['center']['n2'])),recorded_center_metric=data['center']['trace_relative_residual'])
ck('highprecision_center_root',abs(poly(xhigh))<mp.mpf('1e-35'));ck('reported_center_normalization_is_not_relative_accuracy',relres>mp.mpf('1e-9') and absres/(1+abs(n2stored))<mp.mpf('1e-14'))
result=dict(passed=all(z['passed'] for z in checks),checks=checks,precision_decimal_digits=50,maximum_backward_relative={k:str(v) for k,v in maxes.items()},runs=rows,binary64_runs=binaryrows,maximum_binary64_backward_relative={k:str(v) for k,v in binarymax.items()},center_precision_review=centerreview,control=args.control,input_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [CORE,DATA]},non_claims=['RHS algebraic consistency, not derivative of recorded interpolant','No between-node ODE residual certificate','No proof of finite-start center remainder','No perturbative health or global cosmic match'])
out=pathlib.Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],checks=len(checks),maximum_backward_relative=result['maximum_backward_relative'],failed=[z['name'] for z in checks if not z['passed']])));raise SystemExit(0 if result['passed'] else 1)
