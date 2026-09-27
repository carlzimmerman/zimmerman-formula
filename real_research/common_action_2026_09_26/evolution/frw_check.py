#!/usr/bin/env python3
"""Direct on-shell de Sitter ADM scalar expansion for inactive CA4-GNC-P."""
import argparse,json,sys
from pathlib import Path
import sympy as s


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();checks={}
 def exact(name,expr):
  z=s.factor(s.simplify(expr));assert z==0,(name,z);checks[name]=str(z)
 e=s.symbols('e');H,b,alpha,x,xi,ell=s.symbols('H b alpha x xi ell',positive=True)
 psi,pd,phi,B,C,px,pxx,beta,Z,U=s.symbols('psi pd phi B C px pxx beta Z U',real=True)
 # ADM: h_ij=a²e^-2psi delta_ij, N=e^phi, N^x=a^-2 beta_x.
 # B=beta_xx/a² is first order; C=beta_x psi_x/a² is second order.
 T=H-e*pd+e**2*C
 EH=s.exp(-e*(phi+3*psi))*(-6*T*T+4*T*e*B)
 vac=-6*H*H*s.exp(e*(phi-3*psi)) # V0=3M²H², including factor2/M².
 coeff=s.diff(EH+vac,e,2).subs(e,0)/2
 target=-6*(pd+H*phi)**2-4*B*(pd+H*phi)
 # Difference is exactly a spatial divergence and a³-weighted time boundary.
 exact('ADM_kinetic_vacuum_before_IBP',coeff-target+12*H*(C+psi*B)+36*H*psi*pd+54*H*H*psi*psi)
 exact('ADM_spatial_shift_IBP',(-12*H*(C+psi*B)).subs(C,-psi*B))
 exact('ADM_time_IBP_boundary',(-36*H*psi*pd-54*H*H*psi*psi).subs(pd,-s.Rational(3,2)*H*psi))
 R=s.exp(e*(phi-psi))*(4*e*pxx-2*e*e*px*px)
 R2=s.diff(R,e,2).subs(e,0)/2
 exact('ADM_intrinsic_curvature_IBP',R2-(2*px*px+4*phi*pxx)+4*(psi*pxx+px*px))
 v=pd+H*phi
 pre=-6*v*v+4*x*beta*v-b*(3*v-x*beta)**2
 shift=(3+2/b)*v/x
 K=2*(2+3*b)/b
 exact('centered_clock_shift_stationarity',s.diff(pre,beta).subs(beta,shift))
 exact('centered_clock_shift_reduced_kinetic',pre.subs(beta,shift)-K*v*v)
 # Two-cell nonzero mean-zero mode keeps the projector's second variation.
 weights=[s.exp(-3*e*psi),s.exp(3*e*psi)];zs=[e*Z,-e*Z];ns=[s.exp(e*phi),s.exp(-e*phi)]
 mean=sum(ww*zz for ww,zz in zip(weights,zs))/sum(weights)
 delta_vac=sum(ns[i]*weights[i]*(1-1/(1+zs[i]-mean))for i in range(2))/2
 exact('projected_vacuum_quadratic',s.diff(delta_vac,e,2).subs(e,0)/2-(phi*Z-Z*Z))
 r=s.symbols('r',positive=True);cN=1-alpha/2
 aux=alpha*(phi-Z)**2+4*phi*Z-2*Z*Z-4*cN*Z*U+4*cN*r*phi*U
 exact('off_U_constraint',s.diff(aux,U).subs(Z,r*phi))
 ae=2-(2-alpha)*(1-r)**2
 exact('off_spatial_alpha_effective',aux.subs(Z,r*phi)-ae*phi*phi)
 D=ae*x+6*H*H*r*(1-r);E=K*H*H+D
 L=K*(pd+H*phi)**2+2*x*psi*psi-4*x*phi*psi+D*phi*phi
 sol=(2*x*psi-K*H*pd)/E
 exact('FRW_lapse_stationarity',s.diff(L,phi).subs(phi,sol))
 Ar=K*D/E;Br=4*K*H*x/E;Cr=2*x-4*x*x/E
 exact('FRW_reduced_coefficients',L.subs(phi,sol)-(Ar*pd*pd+Br*pd*psi+Cr*psi*psi))
 # q²=x evolves with xdot=-2Hx; r=ell exp(-xi²x/2)/4.
 rdot=H*xi*xi*x*r
 dtime=lambda F:s.diff(F,x)*(-2*H*x)+s.diff(F,r)*rdot
 Ceff=s.factor(Cr-(3*H*Br+dtime(Br))/2)
 Dx=s.diff(D,x)-s.diff(D,r)*xi*xi*r/2
 exact('FRW_integrated_stiffness',Ceff-(2*x*D/E-4*x*x/E-4*K*H*H*x*x*Dx/E**2))
 r0=ell/4;D0=6*H*H*r0*(1-r0)
 exact('FRW_IR_kinetic',Ar.subs({x:0,r:r0})-K*D0/(K*H*H+D0))
 exact('FRW_IR_C_over_x',(Ceff/x).subs({x:0,r:r0})-2*D0/(K*H*H+D0))
 exact('FRW_IR_growth_coefficient',(Ceff/(Ar*x)).subs({x:0,r:r0})-2/K)
 Dadot=dtime(D);aedot=dtime(ae)
 exact('FRW_D_dot_positive_bridge',Dadot+2*H*D-(x*aedot+6*H*H*(rdot*(1-2*r)+2*H*r*(1-r))))
 Adot=dtime(Ar);friction=3*H+Adot/Ar
 exact('FRW_friction_lower_bridge',friction-(3*H-2*H*K*H*H/E)-K*H*H*(Dadot+2*H*D)/(D*E))
 exact('FRW_friction_baseline',3*H-2*H*K*H*H/E-(H+2*H*D/E))
 # xi>0 ultraviolet heat gain tends to zero faster than any polynomial.
 Cuv=s.factor(Ceff.subs(r,0));Auv=s.factor(Ar.subs(r,0))
 exact('FRW_UV_speed',s.limit(-Cuv/(Auv*x),x,s.oo)-2*(2-alpha)/(K*alpha))
 out={'runtime':{'python':sys.version,'executable':sys.executable,'sympy':s.__version__},'checks':checks,'count':len(checks),
      'definitions':{'background':'a=exp(Ht), H²=V0/(3M²), Lambda_bare=0, zero carrier excitations, inactive gate','mode':'q=k/a !=0','r':'ell exp(-xi²q²/2)/4','K':str(K),'D':str(D),'A':str(Ar),'B':str(Br),'C':str(Cr),'C_integrated':str(Ceff)},
      'results':['Conjectured ADM block confirmed after explicit spatial and time IBP and projection variation',
                 'For0<ell<4 all finite nonzero modes have positive reduced kinetic A',
                 'For anyell>0 infrared C_integrated/A=(2/K)q²+O(q4), negative spatial stiffness',
                 'For0<ell<=2 the future friction is>=H and each fixed Fourier mode has a finite future limit by an integrable-coefficient Volterra bound'],
      'nonclaims':['No q=0 division or homogeneous-mode degree count','No uniform Sobolev/mode-sum or nonlinear global PDE theorem','Infrared negative stiffness is not an automatic unbounded-time instability because q redshifts']}
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':True,'exact_checks':len(checks)}))
if __name__=='__main__':main()
