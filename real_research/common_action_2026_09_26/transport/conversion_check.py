#!/usr/bin/env python3
"""Exact linear classical mode-conversion pump/Floquet audit."""
import argparse,json,math
from pathlib import Path
import sympy as S
import numpy as np
from scipy.integrate import solve_ivp
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();checks={}
def eq(n,e):
 e=S.factor(e);assert e==0,(n,e);checks[n]='exact zero'
def yes(n,p):assert bool(p),n;checks[n]=True
l,a,b,M,h=S.symbols('l a b M h',real=True)
mat=S.Matrix([[l*l+a,2*M*l,h],[-2*M*l,l*l+a,0],[2*h,0,l*l+b]])
poly=((l*l+a)**2+4*M*M*l*l)*(l*l+b)-2*h*h*(l*l+a)
eq('exact rotating determinant',mat.det()-poly)
M2,m2,u2=S.symbols('M2 m2 u2',positive=True)
k2=((M2-m2-u2)**2-4*m2*u2)/(4*M2)
eq('resonance chi frequency',k2+m2-(M2+m2-u2)**2/(4*M2))
eq('resonance real frequency',k2+u2-(M2-m2+u2)**2/(4*M2))
# First-order slow amplitude matrix: product determines growth, not damping.
sig,delta,wc,ws=S.symbols('sig delta wc ws',real=True)
rwa=S.Matrix([[sig+S.I*delta/2,S.I*h/(2*wc)],[-S.I*h/(2*ws),sig-S.I*delta/2]])
eq('RWA growth determinant',rwa.det()-(sig*sig+delta*delta/4-h*h/(4*wc*ws)))
# Charge exchange is antisymmetric even with the positive-square interaction.
pr,pi,cr,ci,ss,g,mm=S.symbols('pr pi cr ci ss g mm',real=True)
z=pr+S.I*pi;c=cr+S.I*ci
V=M2*(pr*pr+pi*pi)+mm*((cr+g*ss*pr)**2+(ci+g*ss*pi)**2)+u2*ss*ss/2
# Cartesian-normalization charge derivative: forces -V_(real)/2 for complex components.
qp=2*(pr*(-S.diff(V,pi)/2)-pi*(-S.diff(V,pr)/2))
qc=2*(cr*(-S.diff(V,ci)/2)-ci*(-S.diff(V,cr)/2))
eq('diagonal charge conservation',qp+qc)
eq('complex charge transfer source',qp+2*g*mm*ss*(pr*ci-pi*cr))
# current divergence source = minus local charge derivative for homogeneous raised-index convention as explicitly audited in report.

def matrix(M,m,mu,h,k):
 A=np.zeros((6,6));A[:3,3:]=np.eye(3)
 aa=k*k+m*m-M*M;bb=k*k+mu*mu+2*h*h/(m*m)
 A[3,[0,2,4]]=[-aa,-h,-2*M];A[4,[1,3]]=[-aa,2*M];A[5,[0,2]]=[-2*h,-bb]
 return A

def resonance(M,m,mu,h):
 ue2=mu*mu+2*h*h/(m*m);ue=math.sqrt(ue2)
 if M<=m+ue:return None
 k=math.sqrt(((M*M-m*m-ue2)**2-4*m*m*ue2)/(4*M*M))
 wc=math.sqrt(m*m+k*k);ws=math.sqrt(ue2+k*k)
 eig=np.linalg.eigvals(matrix(M,m,mu,h,k));growth=max(eig.real)
 return dict(M=M,m=m,mu=mu,h=h,mu_eff=ue,k=k,omega_chi=wc,omega_s=ws,group_velocity_chi=k/wc,group_velocity_s=k/ws,exact_growth=float(growth),rwa_growth=h/(2*math.sqrt(wc*ws)),eigenvalues=[[float(x.real),float(x.imag)]for x in eig])
rows=[]
for hh in [.1,.03,.01,.003]:
 r=resonance(3,1,.5,hh);rows.append(r);yes('sum resonance exact h'+str(hh),abs(r['omega_chi']+r['omega_s']-3)<1e-12);yes('positive exact Floquet growth h'+str(hh),r['exact_growth']>0)
yes('RWA converges as coupling weakens',abs(rows[-1]['exact_growth']/rows[-1]['rwa_growth']-1)<abs(rows[0]['exact_growth']/rows[0]['rwa_growth']-1))
slow=resonance(1,.998,0,1e-6)
yes('conditional slow converted wave speed',.0019<slow['group_velocity_chi']<.0021)
yes('pump-induced mass closes resonance',resonance(1,.998,0,.01)is None)
# Independent integration in original periodically forced coordinates over one exact pump period.
M,m,mu,hh=3.,1.,.5,.1;r=resonance(M,m,mu,hh);kk=r['k'];T=2*math.pi/M
# chi=x+iy: real RHS -h cosMt s, imag RHS +h sinMt s; s force -2h(cosMt x-sinMt y).
def periodic(t,Y):
 A=np.zeros((6,6));A[:3,3:]=np.eye(3);c=math.cos(M*t);s=math.sin(M*t)
 A[3,[0,2]]=[-(kk*kk+m*m),-hh*c];A[4,[1,2]]=[-(kk*kk+m*m),hh*s];A[5,[0,1,2]]=[-2*hh*c,2*hh*s,-(kk*kk+mu*mu+2*hh*hh/(m*m))]
 return (A@Y.reshape(6,6)).ravel()
sol=solve_ivp(periodic,[0,T],np.eye(6).ravel(),method='DOP853',rtol=1e-12,atol=1e-13)
actual=np.linalg.eigvals(sol.y[:,-1].reshape(6,6));expected=np.exp(np.linalg.eigvals(matrix(M,m,mu,hh,kk))*T)
err=max(min(abs(x-y)for y in actual)for x in expected)
yes('periodic monodromy matches rotating polynomial',sol.success and err<1e-9)
# The complete exact polynomial, not a assumed resonance rate, determines finite band.
ks=np.linspace(.9,1.7,321);gs=[float(max(np.linalg.eigvals(matrix(3,1,.5,.1,k)).real))for k in ks]
active=[float(k)for k,growth in zip(ks,gs)if growth>1e-7]
yes('finite sampled resonance band',len(active)>0 and min(active)>.9 and max(active)<1.7)
out={'result':'classical coherent conversion linear Floquet audit accepted','checks':checks,'check_count':len(checks),'resonance_rows':rows,'slow_wave_witness':slow,'periodic_monodromy_error':float(err),'sampled_k_band':{'range':[.9,1.7],'count':321,'threshold':1e-7,'first':min(active),'last':max(active)},'non_claims':['Prescribed exact pump linearization, not undepleted full dynamics forever','Classical zero seed remains zero','No particle production or stochastic rate inferred','No selfgravity or empirical fit','Weak-pump RWA is approximate and checked against exact Floquet']}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
