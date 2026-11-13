#!/usr/bin/env python3
import argparse,json,math
from pathlib import Path
from scipy.special import gamma,gammainc
G=6.674e-11;MSUN=1.989e30;MPC=3.0857e22;C_LIGHT=299792458.;A0=9.3603e-11
Mb=1e11;rM=math.sqrt(G*MSUN*Mb/A0)/MPC;a=A0/C_LIGHT**2*MPC;eps=a*rM
R=60.;d=2/(R*math.sqrt(1+4*R*R))/4;KPic=a*d/rM

def ref(x):
 s=math.sqrt(1+4*x*x);return math.asinh(2*x)-(1+s)/(2*x)-math.asinh(120.),(1+s)/(2*x*x),2/(x*s)
rows=[]
for mu in [198.25,25120.]:
 delta=(1/mu)**2
 f_inner,_,_=ref(1.)
 L2_global=(eps*f_inner)**2/(-math.log1p(-delta))
 for x in [1.,10.,60.]:
  f,y,Z=ref(x);qoffset=-eps*f;u=Z/d;S=math.exp(-u**3)
  L2_local=qoffset*qoffset/(math.log1p(-S)-math.log1p(-delta))
  integral=3*gamma(5/3)*gammainc(5/3,u**3)
  alpha_local=mu*mu*L2_local/(2*KPic)*integral
  alpha_global=mu*mu*L2_global/(2*KPic)*integral
  # K*Bstar=mu² L_Q²/2. Pressure candidate lower bound J>=1.54025 Bstar.
  KBstar=mu*mu*L2_global/2
  phi=eps*f;KPi=a*Z/rM
  rows.append({'mu_Mpc_inverse':mu,'r_over_rM':x,'r_Mpc':x*rM,'phi_geo':phi,'g_over_a0':y,'Pi_over_Pic':u,'KPi_Mpc_inverse2':KPi,'KPic_Mpc_inverse2':KPic,'dust_fraction_ceiling_delta':delta,'LQ_squared_min_from_local_suppression':L2_local,'LQ_squared_min_from_whole_annulus':L2_global,'Gamma_prime_min_local':alpha_local,'Gamma_prime_min_whole_annulus':alpha_global,'mu_effective_with_fixed_W_at_beta_min':1-(1+alpha_global)**2/(1+(1+alpha_global)*y),'K_Bstar_min_Mpc_inverse2':KBstar,'K_pressure_floor_1p54025_Bstar_Mpc_inverse2':1.54025*KBstar,'pressure_floor_over_Pi':1.54025*KBstar/KPi})
out={'Mb_Msun':Mb,'rM_Mpc':rM,'epsilon':eps,'d':d,'KPic_Mpc_inverse2':KPic,'I_gate_infinite':3*gamma(5/3),'assumptions':'Same canonical physical annulus as run04; u_R4; required gate-dust fraction<=1/mu² at every radius. Qindependent stabilizer Gamma prime0=0. Pressure column conditional on sibling analytic boundJ>=1.54025Bstar, not established by this script.','rows':rows}
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
