"""Scope test for eliminating the mediator in a coherent neutral carrier medium."""
import json,math,sys
from pathlib import Path
import sympy as s
m=1.;M=2.;delta=2e-9;mu=.002;lam=1e-6;hc=1.973269804e-7;hb=6.582119569e-16
h=mu/(2*m*math.sqrt(2*M));gself=lam/(2*m*m)-mu*mu/(4*m*m*M*M)
gcross_contact=(lam-mu*mu/(4*M*M))/(m*m);gcross=gcross_contact-h*h/delta
# Eliminate r from delta |r|^2+h(r* a b+h.c.) by completing a square.
d,H,A,B,R=s.symbols('delta h a b r',real=True)
assert s.expand(d*(R+H*A*B/d)**2-H**2*A**2*B**2/d-(d*R**2+2*H*R*A*B))==0
# At equal densities n/2, interaction Hessian eigenvectors are density and charge.
gs,gc=s.symbols('gs gc',real=True);K=s.Matrix([[gs,gc],[gc,gs]])
assert K*s.Matrix([1,1])==(gs+gc)*s.Matrix([1,1])
assert K*s.Matrix([1,-1])==(gs-gc)*s.Matrix([1,-1])
critical_n=delta*delta/(h*h)/hc**3
rows=[]
volume=4*math.pi*.02**3/3
for label,nSI in [('two_particles_in_2cm_sphere',2/volume),('one_hundred_pairs_in_2cm_sphere',200/volume),('assigned_0.3GeV_per_cm3_at_1eV',.3e9*1e6)]:
    n=nSI*hc**3;ratio=h*math.sqrt(n)/delta;Aenergy=-n*(gself+gcross)
    row=dict(label=label,total_number_density_per_m3=nSI,coherent_mixing_parameter=ratio,second_order_shift_over_detuning=ratio**2,elimination_small_parameter=ratio<.1)
    if ratio<.1:
        row.update(eliminated_density_mode_coefficient_eV=-Aenergy,formal_continuum_max_growth_per_s=Aenergy/(2*hb),formal_continuum_fastest_wavelength_m=2*math.pi*hc/math.sqrt(m*Aenergy),warning='Continuum coherent instability formula only; finite trap and small particle number may invalidate that state model')
    else:row['warning']='Do not use eliminated Bogoliubov spectrum here; keep the mediator explicitly'
    rows.append(row)
result=dict(scope='Coherent equal particle/antiparticle medium diagnostic; not an empirical halo density or a proof about arbitrary multimode states',pair_mediator_coupling_eV_minus_half=h,same_sign_NR_coupling_eV_minus2=gself,opposite_nonresonant_NR_coupling_eV_minus2=gcross_contact,opposite_eliminated_NR_coupling_eV_minus2=gcross,density_channel_Hessian_eigenvalue_eV_minus2=gself+gcross,charge_channel_Hessian_eigenvalue_eV_minus2=gself-gcross,mixing_order_one_density_per_m3=critical_n,mixing_below_point1_density_per_m3=.01*critical_n,rows=rows,symbolic_assertions_passed=3)
assert gself>0 and gself+gcross<0
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
