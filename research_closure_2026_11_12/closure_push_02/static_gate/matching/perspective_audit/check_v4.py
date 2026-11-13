#!/usr/bin/env python3
"""Independent algebra and endpoint audit, not a complete GR spectrum calculation."""
import argparse,json,math
from pathlib import Path
import sympy as s
import mpmath as mp
mp.mp.dps=70
q,C,L,u,z=s.symbols('q C L u z',positive=True); x=q-1;t=x*x/(L*L*q)
F=C*x*x;B=C*L*L*q*(1-s.exp(-t));S=s.exp(-u**3)
Bp=s.diff(B,q);Bpp=s.diff(B,q,2)
target_Bpp=C*s.exp(-t)*(2-(q*q-1)**2/(L*L*q**3))
assert s.simplify(Bpp-target_Bpp)==0
assert s.simplify(q*Bp-B-C*(q*q-1)*s.exp(-t))==0
GG=s.Function('Gamma')(u);H=F-B+B*S-q*GG
rho=q*s.diff(H,q)-H
assert s.simplify(rho-C*(q*q-1)*(1-(1-S)*s.exp(-t)))==0
assert s.simplify(s.diff(H,q,2)-(2*C-(1-S)*target_Bpp))==0
Huu=s.diff(H,u,2).subs(s.diff(GG,u,2),9*C*L*L*u**4*S)
target_Huu=-q*C*L*L*S*(9*u**4*s.exp(-t)+6*u*(1-s.exp(-t)))
assert s.simplify(Huu-target_Huu)==0
# Moment lower bound antiderivative; u0³=2/3.
Sp=s.diff(S,u);Spp=s.diff(S,u,2)
assert s.simplify(s.diff(u*Sp-S,u)-u*Spp)==0
J=s.symbols('J',positive=True)
assert s.simplify(q*s.diff(q*J,q)-q*J)==0
# Static fixed-J ADM spatial stress: independent diagonal metric variation.
aa,bb,cc,NN,JJ,ZZ=s.symbols('aa bb cc NN JJ ZZ',real=True)
HH=s.Function('HH');WW=s.Function('WW');sigma=aa+bb+cc
Lmetric=NN*s.exp(sigma)*(HH(ZZ*s.exp(-sigma))-WW(JJ*s.exp(-aa-bb)))
base={aa:0,bb:0,cc:0,NN:1}
pclock=HH(ZZ)-ZZ*s.diff(HH(ZZ),ZZ)
ptrans=s.diff(Lmetric,aa).subs(base)
prad=s.diff(Lmetric,cc).subs(base)
assert s.simplify(ptrans-(pclock+JJ*s.diff(WW(JJ),JJ)-WW(JJ)))==0
assert s.simplify(prad-(pclock-WW(JJ)))==0
assert s.simplify((2*ptrans+prad)/3-(pclock+s.Rational(2,3)*JJ*s.diff(WW(JJ),JJ)-WW(JJ)))==0
pp=s.symbols('pp',positive=True);ww=-pp-s.log(1-pp)
assert s.simplify(s.diff(pp*s.diff(ww,pp)-2*ww,pp)-pp*pp/(1-pp)**2)==0
assert s.limit(pp*s.diff(ww,pp)-2*ww,pp,0,dir='+')==0
assert s.simplify(H-u*s.diff(H,u)-((F-B)+B*(S-u*s.diff(S,u))+q*(u*s.diff(GG,u)-GG)))==0
I0=3*mp.gamma(mp.mpf(5)/3);I1=mp.mpf(3)
u0=(mp.mpf(2)/3)**(mp.mpf(1)/3)
minimum_J=3*mp.exp(-mp.mpf(2)/3)
U=mp.mpf(4)
tail_slope=3*mp.gammainc(mp.mpf(5)/3,U**3,mp.inf)
tail_moment=3*mp.gammainc(2,U**3,mp.inf)
E=tail_moment-U*tail_slope
E_direct=mp.quad(lambda v:9*(v-U)*v**4*mp.exp(-v**3),[U,5,8,mp.inf])
assert abs(E/E_direct-1)<mp.mpf('1e-50')
finite_min=minimum_J-(3*U**3+1)*mp.exp(-U**3)
assert finite_min>0 and finite_min<minimum_J
# Deliberate excluded-domain witnesses for careless extension of the claim.
Q=mp.mpf(10);LL=mp.mpf(1);UU=mp.mpf(-3);tt=(Q-1)**2/(LL*LL*Q)
bpp=mp.exp(-tt)*(2-(Q*Q-1)**2/(LL*LL*Q**3))
hqq=2-(1-mp.exp(-UU**3))*bpp
assert hqq<0
Q2=mp.mpf(2);U2=mp.mpf('-.01');tt2=(Q2-1)**2/Q2
huu=-Q2*mp.exp(-U2**3)*(9*U2**4*mp.exp(-tt2)+6*U2*(1-mp.exp(-tt2)))
assert huu>0
inputs=json.loads(Path('research_closure_2026_11_12/closure_push_02/static_gate/matching/run01/results.json').read_text())
rows=[]
for mu in [198.25,25120.]:
 inner=next(r for r in inputs['rows'] if r['mu_Mpc_inverse']==mu and r['r_over_rM']==1.)
 offset=mp.mpf(str(-inner['phi_geo']));Q=1+offset;delta=mp.mpf(str(inner['dust_fraction_ceiling_delta']))
 # Finite gate at inner radius is smaller than exp(-10^12), so S=0 limit stated explicitly.
 L2=offset**2/(Q*(-mp.log1p(-delta)))
 KB=mp.mpf(str(mu))**2*L2/2
 for rr in [1.,10.,60.]:
  local=next(r for r in inputs['rows'] if r['mu_Mpc_inverse']==mu and r['r_over_rM']==rr)
  Qlocal=1+mp.mpf(str(-local['phi_geo']));UP=mp.mpf(str(local['Pi_over_Pic']))
  min_moment=minimum_J-(3*UP**3+1)*mp.exp(-UP**3)
  Kp_min=Qlocal*KB*min_moment
  rows.append({'mu_Mpc_inverse':mu,'r_over_rM':rr,'LQ2_min_perspective_energy':float(L2),'K_Bstar_min':float(KB),'K_J_asymptote_min':float(KB*minimum_J),'K_QJ_partial_moment_min':float(Kp_min),'partial_moment_pressure_over_reference_Pi':float(Kp_min/mp.mpf(str(local['KPi_Mpc_inverse2']))),'curvature_radius_Mpc':float(1/mp.sqrt(KB*minimum_J))})
ttest=s.symbols('ttest',positive=True)
assert s.simplify(s.diff((1-s.exp(-ttest))/ttest,ttest)-((ttest+1)*s.exp(-ttest)-1)/ttest**2)==0
integrated=[]
for mu in [198.25,25120.]:
 inner=next(r for r in inputs['rows'] if r['mu_Mpc_inverse']==mu and r['r_over_rM']==1.)
 outer=next(r for r in inputs['rows'] if r['mu_Mpc_inverse']==mu and r['r_over_rM']==60.)
 delta=mp.mpf(str(inner['dust_fraction_ceiling_delta']))
 offset=mp.mpf(str(-inner['phi_geo']));Qinner=1+offset;Qouter=1+mp.mpf(str(-outer['phi_geo']))
 L2=offset**2/(Qinner*(-mp.log1p(-delta)))
 KB=mp.mpf(str(mu))**2*L2/2
 minimum_moment_under_suppression=minimum_J-(1-3*mp.log(delta))*delta
 assert minimum_moment_under_suppression>0
 rinner=mp.mpf(str(inner['r_Mpc']));router=mp.mpf(str(outer['r_Mpc']))
 ageo=mp.mpf(str(inputs['epsilon']))/mp.mpf(str(inputs['rM_Mpc']))
 # N=1/Q with Q=1-phi for the explicitly stated weak-potential target.
 inner_Nprime=ageo*mp.mpf(str(inner['g_over_a0']))/Qinner**2
 outer_Nprime=ageo*mp.mpf(str(outer['g_over_a0']))/Qouter**2
 target_flux=router**2*outer_Nprime-rinner**2*inner_Nprime
 Kp_floor=KB*minimum_moment_under_suppression
 required_flux=Kp_floor/Qinner*(router**3-rinner**3)
 integrated.append({'mu_Mpc_inverse':mu,'necessary_u_min_from_energy_suppression':float((-mp.log(delta))**(mp.mpf(1)/3)),'minimum_moment_per_CL2_under_suppression':float(minimum_moment_under_suppression),'K_mean_pressure_floor':float(Kp_floor),'target_lapse_flux_per_4pi_Mpc':float(target_flux),'minimum_required_lapse_flux_per_4pi_Mpc':float(required_flux),'required_over_target_flux':float(required_flux/target_flux),'finite_Qband_K_Bband_lower':float(KB*delta),'finite_Qband_K_mean_pressure_floor':float(Kp_floor*delta),'finite_Qband_required_flux_per_4pi_Mpc':float(required_flux*delta),'finite_Qband_required_over_target_flux':float(required_flux*delta/target_flux),'assumptions':'Static on-P-shell;Q>=1,positivePi,suppression<=delta throughoutannulus;weak spatialmetric;N=1/Q; no additional negative-active stresscancelingfloor; cosmologicalLambda omitted relativetofloor.'})
result={'integrated_static_target_contradiction':integrated,'exact_symbolic_checks':{'B_second_derivative':True,'QBprime_minus_B':True,'normal_energy_suppression':True,'H_QQ_formula':True,'H_PiPi_formula':True,'moment_antiderivative':True,'QJ_zero_normal_energy':True,'fixed_J_ADM_transverse_and_radial_stress':True,'isotropic_mean_stress':True,'W_cannot_lower_mean_pressure':True,'finite_u_clock_pressure_moment':True,'finite_Qband_decreasing_ratio_derivative':True},'endpoint_constants':{'slope_per_CL2':str(I0),'intercept_per_CL2':str(I1),'minimum_intercept_per_CL2':str(minimum_J),'u0':str(u0),'u4_E_per_CL2':str(E),'u4_tail_moment_per_CL2':str(tail_moment),'u4_minimum_moment_subtraction_per_CL2':str(minimum_J-finite_min),'u4_direct_tail_quadrature_relative_error':str(abs(E/E_direct-1))},'excluded_negative_Pi_counterexamples':{'Q10_L1_u_minus3_HQQ_per_C':str(hqq),'Q2_L1_u_minus_point01_Huu_per_C':str(huu)},'physical_target_rows':rows,'scope':'Algebra Q>0,finitePi>=0; physical energy suppression Q>1; universal compensator bound assumes concavity all Q>=1 and Gamma(0)=Gamma_u(0)=0. On the static polarization shell, the fixed-J metric variation shows complete mean pressure is bounded below by the partial moment; bare covariant gradient terms cannot cancel it independently. No universal theory no-go.'}
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
