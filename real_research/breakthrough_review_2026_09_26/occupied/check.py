#!/usr/bin/env python3
"""On-shell occupied FRW scalar action: exact background jets and Schur."""
import argparse,json,sys
from pathlib import Path
import sympy as s

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();checks={}
 def exact(name,expr):
  z=s.factor(s.simplify(expr));assert z==0,(name,z);checks[name]=str(z)
 e=s.symbols('e')
 M,H,Hd,c2,x,alpha,r,V0=s.symbols('M H Hd c2 x alpha r V0',positive=True) # M denotes M_P²
 psi,pd,phi,B,C,Z,U,beta,chi,cd,v,vd,V,Vp,Vpp,f1,f2=s.symbols('psi pd phi B C Z U beta chi cd v vd V Vp Vpp f1 f2',real=True)
 T=v*v/2;rho=T+V+V0;Q=1-r;cN=1-alpha/2;K=2*(2+3*c2)/c2;ae=2-(2-alpha)*Q**2
 # Exact scalar ADM kinetic, then spatial/time IBP at nonconstant H.
 Tc=H-e*pd+e**2*C
 EH=M/2*s.exp(-e*(phi+3*psi))*(-6*Tc**2+4*Tc*e*B)
 EH2=s.diff(EH,e,2).subs(e,0)/2
 EHtarget=M/2*(-6*(pd+H*phi)**2-4*B*(pd+H*phi)+3*H*H*phi**2-18*H*H*phi*psi+(27*H*H+18*Hd)*psi**2)
 # Spatial integral C=-psi B; time boundary integrates -18 M H psi pd.
 EHibp=s.expand(EH2).subs(C,-psi*B)+18*M*H*psi*pd+9*M*(3*H*H+Hd)*psi**2
 exact('ADM_non_deSitter_background_IBP',EHibp-EHtarget)
 # Two-cell projected fields: every fluctuation has opposite signs between cells.
 weights=[s.exp(-3*e*psi),s.exp(3*e*psi)];zs=[e*Z,-e*Z]
 mean=sum(w*z for w,z in zip(weights,zs))/sum(weights)
 L=0
 for sig,ww,zz in zip([1,-1],weights,zs):
  z=zz-mean;n=s.exp(sig*e*phi)
  Vjet=V+sig*e*Vp*chi+e*e*Vpp*chi*chi/2
  Fjet=1+f1*z+f2*z*z/2
  L+=ww*((1+z)/n*(v+sig*e*cd)**2/2-n*Vjet/(1+z)-n*V0*Fjet)/2
 L2=s.diff(L,e,2).subs(e,0)/2
 expected=cd**2/2+v*cd*(Z-phi-3*psi)+(T-V-V0)*phi**2/2+3*rho*phi*psi+9*(T-V-V0)*psi**2/2+(V-T-V0*f1)*phi*Z-(V+V0*f2/2)*Z*Z+Vp*chi*(Z-phi+3*psi)-Vpp*chi*chi/2
 exact('projected_general_vacuum_matter_quadratic',L2-expected)
 # Friedmann and Raychaudhuri are background equations of the centered action.
 extra=3*M*H*H*phi**2/2-9*M*H*H*phi*psi+M*(27*H*H+18*Hd)*psi**2/2
 bg=(T-V-V0)*phi**2/2+3*rho*phi*psi+9*(T-V-V0)*psi**2/2
 exact('on_shell_background_cancellations',(extra+bg-T*phi**2).subs({H**2:rho/(3*M),Hd:-T/M}))
 # -3 a³ v psi chi_dot integrates to 3 v psi_dot chi plus -3 Vp psi chi.
 exact('matter_volume_time_IBP',(3*(vd+3*H*v)*psi*chi+3*Vp*psi*chi).subs(vd,-3*H*v-Vp))
 ss=pd+H*phi
 shiftblock=M/2*(-6*ss**2+4*x*beta*ss-c2*(3*ss-x*beta)**2)-x*beta*v*chi
 betastar=((3+2/c2)*ss-v*chi/(M*c2))/x
 shiftreduced=M*K*ss**2/2-(3+2/c2)*ss*v*chi+v*v*chi*chi/(2*M*c2)
 exact('occupied_shift_stationarity',s.diff(shiftblock,beta).subs(beta,betastar))
 exact('occupied_shift_reduction',shiftblock.subs(beta,betastar)-shiftreduced)
 aux=M*x/2*(alpha*(phi-Z)**2+4*phi*Z-2*Z*Z-4*cN*Z*U+4*cN*r*phi*U)
 exact('unchanged_U_constraint',s.diff(aux,U).subs(Z,r*phi))
 exact('spatial_alpha_reduction',aux.subs(Z,r*phi)-M*ae*x*phi*phi/2)
 rest=cd*cd/2+v*cd*(Z-phi)+3*v*pd*chi+T*phi*phi+(V-T-V0*f1)*phi*Z-(V+V0*f2/2)*Z*Z+Vp*chi*(Z-phi)-(x+Vpp)*chi*chi/2
 spatial=M*x*psi*psi-2*M*x*phi*psi
 full=shiftblock+aux+rest+spatial
 reduced=full.subs({beta:betastar,Z:r*phi})
 Delta=ae*x+2*(T+(V-T-V0*f1)*r-(V+V0*f2/2)*r*r)/M
 F=K*H*H+Delta
 Dkin=ae*x+2*r*(Q*(T+V)-V0*(f1+f2*r/2))/M
 source=M*K*H*pd-Q*v*cd-2*M*x*psi-H*(3+2/c2)*v*chi-Q*Vp*chi
 base=M*K*pd*pd/2+cd*cd/2-2*pd*v*chi/c2+v*v*chi*chi/(2*M*c2)-(x+Vpp)*chi*chi/2+M*x*psi*psi
 exact('full_occupied_reduced_before_lapse',reduced-(base+phi*source+M*F*phi*phi/2))
 exact('carrier_occupation_control_identity',Delta-Q*Q*v*v/M-Dkin)
 phistar=-source/(M*F)
 exact('occupied_lapse_stationarity',s.diff(base+phi*source+M*F*phi*phi/2,phi).subs(phi,phistar))
 final=base-source*source/(2*M*F)
 exact('full_occupied_reduced_action',(base+phi*source+M*F*phi*phi/2).subs(phi,phistar)-final)
 FG=s.symbols('FG',nonzero=True)
 uvec=s.Matrix([M*K*H,-Q*v])
 kinetic=s.diag(M*K,1)-uvec*uvec.T/(M*FG)
 exact('parallel_kinetic_determinant',kinetic.det()-M*K*(FG-K*H*H-Q*Q*v*v/M)/FG)
 exact('parallel_host_kinetic_entry',kinetic[0,0]-M*K*(FG-K*H*H)/FG)
 # Full four-variable constraint matrix, not a single fixed-velocity subblock.
 constraint=s.hessian(full,[beta,U,Z,phi])
 exact('full_constraint_determinant',constraint.det()-4*M**4*c2*cN**2*x**4*F)
 # Two independent carrier directions verify the rank-one determinant pattern.
 w=s.symbols('w',real=True);u3=s.Matrix([M*K*H,-Q*v,-Q*w])
 km3=s.diag(M*K,1,1)-u3*u3.T/(M*FG)
 exact('two_carrier_rank_one_determinant',km3.det()-M*K*(FG-K*H*H-Q*Q*(v*v+w*w)/M)/FG)
 transverse=s.Matrix([0,w,-v])
 for i,z in enumerate(km3*transverse-transverse):exact('transverse_canonical_'+str(i),z)
 r0,ssq,Eexc=s.symbols('r0 ssq Eexc',positive=True)
 Dpq=Dkin.subs({f1:-1,f2:2/r0})
 exact('PQ_positive_decomposition',Dpq-(ae*x+2*(r*Q*(T+V)+V0*r*(1-r/r0))/M))
 Dflat=Dkin.subs({f1:0,f2:0})
 exact('flat_vacuum_positive_decomposition',Dflat-(ae*x+2*r*Q*(T+V)/M))
 exact('occupied_IR_PQ',Dpq.subs({x:0,r:r0})-2*r0*(1-r0)*(T+V)/M)
 exact('occupied_IR_flat',Dflat.subs({x:0,r:r0})-2*r0*(1-r0)*(T+V)/M)
 # UV of actual FRW action, with fixed finite background jets. Heat terms vanish
 # faster than powers; scaling both time derivative perturbations by sqrt(x)
 # retains every second-order principal term.
 lam,pp,cc=s.symbols('lam pp cc',positive=True)
 uv=s.limit(final.subs({r:0,x:lam*lam,pd:lam*pp,cd:lam*cc})/lam**2,lam,s.oo)
 expectedUV=M*K*pp*pp/2+cc*cc/2-M*(2-alpha)*psi*psi/alpha-chi*chi/2
 exact('occupied_FRW_UV_action',uv-expectedUV)
 exact('occupied_FRW_UV_host_speed',2*(2-alpha)/(K*alpha)-c2*(2-alpha)/((2+3*c2)*alpha))
 out={'runtime':{'python':sys.version,'executable':sys.executable,'sympy':s.__version__},'checks':checks,'count':len(checks),
      'background':'homogeneous expanding flat compact FRW, centered trace, inactive gate, U=Z=0, canonical homogeneous carrier equations and Friedmann/Raychaudhuri; V0>0',
      'general_vacuum':'L=(1+z) K−V_exc/(1+z)−V0 F(1+z), F1=1, f1=Fprime1, f2=Fdoubleprime1',
      'definitions':{'M':'M_P²','K':str(K),'Delta':str(Delta),'Fden':str(F),'Dkin':str(Dkin),'full_reduced_action':str(final)},
      'conclusions':['PQ and flat-jet vacuum both give positive exact occupied-FRW velocity Hessian for every q>0','N−1 carrier directions transverse to background velocity retain unit velocity Hessian','Full lapse/shift/U/Z constraint determinant=4 M^4 c2 cN² q^8 Fden is nonzero on that domain','UV host speed²=c2(2−alpha)/[(2+3c2)alpha], carrier speeds²=1 at fixed finite background jets'],
      'nonclaims':['No finite-q occupied restoring-matrix or mode-growth theorem','No uniform q=0 kinetic lower bound or complete homogeneous Dirac count','No full nonlinear PDE or barrier-continuation theorem','Flat-barrier action is separate from PQ; only its two vacuum jets enter this linear kinetic block']}
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':True,'exact_checks':len(checks)}))

if __name__=='__main__':main()
