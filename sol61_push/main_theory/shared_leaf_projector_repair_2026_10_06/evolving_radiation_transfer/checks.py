#!/usr/bin/env python3
import argparse,json
from pathlib import Path
import numpy as np
import sympy as s
from transfer import integrate,coefficients,auxiliary,rhs,chart_det,raw_geometry,observables
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['none','operator','hat'],default='none');ar=ap.parse_args();rows=[];results=[]
def eq(n,v):
 z=s.factor(v);rows.append(dict(name=n,passed=z==0,residual=str(z)))
def ck(n,v,d):rows.append(dict(name=n,passed=bool(v),detail=d))
# Common-coordinate gauge transformations and physical source combinations.
H,H2,l,L,T,Td,Tdd,Hd,H2d,B,Bd,nu,z,zd,rhod=s.symbols('H H2 ell L T Tdot Tddot Hdot H2dot B Bdot nu z zdot rhodot')
eq('visible_curvature_gauge',-(z-H*T)-H*(B+T)-(-z-H*B))
eq('visible_lapse_gauge',(nu-Td)+(Bd+Td)-(nu+Bd))
hat_delta=L*L*T if ar.control=='hat' else T
hat_dd=L*L*Td+2*l*L*L*T if ar.control=='hat' else Td
eq('hatted_curvature_gauge',-(z-H2*T)-H2*(B+hat_delta)-(-z-H2*B))
eq('hatted_lapse_gauge',(nu-Td-l*T)+(Bd+hat_dd)+l*(B+hat_delta)-(nu+Bd+l*B))
eq('Newton_density_gauge',-rhod*T+rhod*T)
# Solve actual system at two declared tolerances, not a survey.
for k in [400.,800.]:
 for op in ['arithmetic','lambda1']:
  actual='arithmetic' if ar.control=='operator' and op=='lambda1' else op
  sol,ys,obs,r=integrate(k,actual,2e-9);fine,yy,oo,rr=integrate(k,actual,2e-10)
  r['declared_operator']=op;r['tight_RHS_calls']=rr['RHS_calls'];results.append(r)
  scale=1+np.max(np.abs(yy),axis=0);err=float(np.max(np.abs(ys-yy)/scale))
  oerr=float(np.max(np.abs(obs-oo)/(1+np.max(np.abs(oo),axis=0))))
  ck('success_'+str(k)+op,r['success'] and rr['success'],[r['RHS_calls'],rr['RHS_calls']]);ck('tolerance_phase_'+str(k)+op,err<2e-7,err);ck('tolerance_physical_'+str(k)+op,oerr<2e-7,oerr)
  ck('canonical_constraint_'+str(k)+op,r['constraint_relative_residual']<2e-8,r['constraint_relative_residual'])
  ck('linear_amplitude_example_'+str(k)+op,r['I_peak_a0_one_amplitude_1e_minus8']<1e-6 and 1e-8*r['max_unit_lapse']<1e-5,dict(I_peak=r['I_peak_a0_one_amplitude_1e_minus8'],lapse=1e-8*r['max_unit_lapse']))
  # Independently check radiation Newton conservation using time differences of
  # the actual dense evolving solution, not a frozen background estimate.
  residual=[];dt=2e-5
  for t in np.linspace(sol.t[0]+3*dt,sol.t[-1]-3*dt,31):
   y=sol.sol(t);a,b,H,L,H2,ell,e,Pg,Ph,A,Bc,D,g,j,G=coefficients(y,k,actual)
   def values(ti):
    v=sol.sol(ti);o=observables(v,k,actual);return np.array([o[6]/(3*v[0]**-4),o[0]])
   der=(values(t-2*dt)-8*values(t-dt)+8*values(t+dt)-values(t+2*dt))/(12*dt)
   raw=raw_geometry(y,k,actual);vn=raw[2]+raw[3]
   resid=der[0]+4*Pg*vn/3-4*der[1]
   residual.append(abs(resid)/(1+abs(der[0])+abs(4*Pg*vn/3)+abs(4*der[1])))
  ck('radiation_energy_'+str(k)+op,max(residual)<2e-5,max(residual))
  if op=='lambda1':ck('repaired_relative_bounded_'+str(k),r['chi_max']<1.1,r['chi_max'])
  else:ck('arithmetic_relative_growth_'+str(k),r['chi_end']>4 if k==400 else r['chi_end']>40,r['chi_end'])
# Separate repaired low-k trajectory across the velocity chart root.
sol,ys,obs,r=integrate(6.,'lambda1',2e-10);results.append(r)
ck('actual_chart_crossing',r['chart_det_range'][0]<0<r['chart_det_range'][1],r['chart_det_range'])
ck('crossing_finite_phase',np.isfinite(ys).all() and np.isfinite(obs).all(),dict(phase_max=float(np.max(np.abs(ys))),Weyl_max=r['Weyl_max']))
ck('crossing_constraint',r['constraint_relative_residual']<1e-10,r['constraint_relative_residual'])
rad,ry,ro,rd=integrate(6.,'lambda1',2e-10,method='Radau');results.append(rd)
ck('crossing_Radau_success',rd['success'],rd['RHS_calls'])
ck('crossing_Radau_phase_agreement',np.max(np.abs(ys-ry)/(1+np.max(np.abs(ys),axis=0)))<2e-8,float(np.max(np.abs(ys-ry)/(1+np.max(np.abs(ys),axis=0)))))
ck('crossing_Radau_physical_agreement',np.max(np.abs(obs-ro)/(1+np.max(np.abs(obs),axis=0)))<2e-8,float(np.max(np.abs(obs-ro)/(1+np.max(np.abs(obs),axis=0)))))
# Positive, unequal exact background and correct full radiation inertia.
for idx,y in enumerate([ys[0],ys[-1]]):
 a,b,H,L,H2,ell,e,Pg,Ph,A,Bc,D,g,j,G=coefficients(y,6.,'lambda1')
 ck('admitted_background_'+str(idx),min(a,b,H,L,H2,A,Bc,D,G)>0 and b>a and abs(H*H-(1+a**-4))<1e-12,dict(a=a,b=b,L=L,H=H,H2=H2))
r=dict(passed=sum(x['passed'] for x in rows),total=len(rows),checks=rows,cases=results,control=ar.control,scope='actual time-dependent quadratic Q1 radiation background; bounded linear unit seed transfer columns, no full nonlinear admission or physical amplitude/likelihood/abundance')
p=Path(ar.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['passed','total']}));raise SystemExit(r['passed']!=r['total'])
