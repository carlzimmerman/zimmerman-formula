"""Scalar-only one-loop diagnostics for the charge-even bridge.

MSbar input comparison at mu=m, sigma tadpole fixed separately. Pole-mass
inputs would instead require finite matching; this does not exclude them.
No full fermion/Higgs/two-loop calculation or measured vacuum prediction.
"""
import json
import math
import sys
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import quad
from scipy.special import roots_legendre

out=Path(sys.argv[1]);assert out.is_dir();base=Path(__file__).parent
old=json.loads((base/'neutral_scalar_bridge_run_001/results.json').read_text())
p=old['parameters'];m,M,g,lr=p['m'],p['M'],p['g'],p['rep']
checks=[]
def check(name,b):
    checks.append(dict(name=name,passed=bool(b)));assert b,name

sig,aa,mm,scale=s.symbols('sigma a m2 scale',positive=True)
cw=(mm+aa*sig)**2*(s.log((mm+aa*sig)/scale**2)-s.Rational(3,2))/(32*s.pi**2)
expected=[aa*mm*(s.log(mm/scale**2)-1)/(16*s.pi**2),
          aa**2*s.log(mm/scale**2)/(16*s.pi**2),
          aa**3/(16*s.pi**2*mm),-aa**4/(16*s.pi**2*mm**2)]
for n,want in enumerate(expected,1):check('CW derivative order'+str(n),s.simplify(s.diff(cw,sig,n).subs(sig,0)-want)==0)
betaV=(mm*mm+2*mm*aa*sig+aa*aa*sig*sig)/(16*s.pi**2)
check('axis one-loop RG cancellation',s.simplify(scale*s.diff(cw,scale)+betaV)==0)

# Real-field Hessian divergence: this also isolates the sigma-dependent
# operator basis, rather than assuming it from the sigma axis alone.
f1,f2,x1,x2,ss=s.symbols('f1 f2 x1 x2 ss',real=True)
m2,M2,ms2,gc,ac,L,Lx=s.symbols('m2 M2 ms2 g a L Lx',real=True)
II=(f1*f1+f2*f2)/2;JJ=(x1*x1+x2*x2)/2
V=m2*II+M2*JJ+gc*(x1*(f1*f1-f2*f2)+2*x2*f1*f2)/s.sqrt(2)+L*II**2+Lx*JJ**2+ms2*ss*ss/2+ac*ss*II
H=s.hessian(V,(f1,f2,x1,x2,ss));trace=s.expand(s.trace(H*H))
dependent=s.expand(trace-trace.subs(ss,0))
check('full real-field sigma divergence basis',s.simplify(dependent-(2*ac*ac*ss*ss+4*ac*m2*ss+16*ac*L*ss*II))==0)
check('mediator contribution to carrier mass beta',s.simplify(s.expand(trace).coeff(ac,2).subs(ss,0)-4*II)==0)

nodes,weights=roots_legendre(512);xx=(nodes+1)/2;ww=weights/2
rho_ref=(2.25e-12)**4 # chosen 2.25meV energy-scale reference, not a new fit
rows=[]
branches=[dict(row,name='original_compensated_family') for row in old['rows']]
selected=next(row for row in old['rows'] if row['mediator_mass_over_m']==10)
weak=dict(selected);weak.update(a_GeV=.0001,name='weaker_selected_comparison')
branches.append(weak)
for b in branches:
    ms,a=b['mediator_mass_GeV'],b['a_GeV'];bb=b['b'];r=ms/m
    integral=quad(lambda x:math.log(r*r*x+(1-x)**2),0,1,epsabs=1e-13,epsrel=1e-12)[0]
    gauss=float(ww@np.log(r*r*xx+(1-xx)**2))
    check('carrier pole integral independent quadrature '+str((r,a)),abs(integral/gauss-1)<1e-10)
    mass_shift=a*a*integral/(16*math.pi**2)
    fractional=mass_shift/(m*m)
    # sigma tadpole is set to zero by a separate renormalization condition.
    # New-a contribution to X pole mass begins beyond this retained loop.
    gap_shift=-4*mass_shift
    gap=p['gap']+gap_shift
    for ratio_scale in (1.,3.,10.):
        # Retained new-a contribution: running MS inputs cancel the
        # explicit log. Holding MS inputs fixed at a new scale would be
        # a different physical matching prescription.
        run_gap=p['gap']-a*a*math.log(ratio_scale)/(2*math.pi**2)
        explicit=a*a*(integral-2*math.log(ratio_scale))/(16*math.pi**2)
        check('retained RG gap invariance '+str((r,a,ratio_scale)),
              abs((run_gap-4*explicit)-gap)<1e-11*max(p['gap'],abs(gap)))
    width=a*a*math.sqrt(1-4*m*m/(ms*ms))/(16*math.pi*ms)
    # Independent optical-theorem check from sigma bubble's logarithmic cut.
    root=math.sqrt(1-4*m*m/(ms*ms));left,right=(1-root)/2,(1+root)/2
    absorptive=-a*a*(right-left)/(16*math.pi)
    check('sigma bubble cut reproduces decay width '+str((r,a)),abs(-absorptive/ms/width-1)<1e-13)
    # Real part of vacuum sigma kernel, with threshold edges split explicitly.
    cuts=[0.,left,right,1.]
    real=0.
    for lo,hi in zip(cuts[:-1],cuts[1:]):
        real+=quad(lambda x:math.log(abs(1-r*r*x*(1-x))),lo,hi,epsabs=1e-11,epsrel=1e-11)[0]
    tadpole=-a*m*m/(16*math.pi**2)
    sigma_shift=-tadpole/(ms*ms)
    zi=-a*bb/(ms*ms);uR=zi*zi/lr
    vacuum_phi=-3*m**4/(64*math.pi**2)
    vacuum_X=M**4*(math.log(M*M/(m*m))-1.5)/(32*math.pi**2)
    vacuum_sigma=ms**4*(math.log(ms*ms/(m*m))-1.5)/(64*math.pi**2)
    row=dict(name=b['name'],mediator_mass_GeV=ms,a_GeV=a,
        carrier_loop_mass_squared_shift_GeV2=mass_shift,carrier_loop_fractional_mass_squared_shift=fractional,
        original_gap_GeV2=p['gap'],gap_shift_GeV2=gap_shift,gap_after_unretuned_one_loop_GeV2=gap,
        mass_shift_loop_gate_below_0p1=fractional<.1,
        source_decay_open_in_unretuned_MS_comparison=gap>0,
        threshold_relative_shift=gap_shift/p['gap'],
        a_upper_for_gap_shift_below_gap_GeV=math.sqrt(4*math.pi**2*p['gap']/integral),
        sigma_bubble_real_on_shell_GeV2=a*a*real/(16*math.pi**2),
        sigma_bubble_Im_on_shell_GeV2=absorptive,sigma_tree_width_GeV=width,
        sigma_tadpole_at_scale_m_GeV3=tadpole,
        sigma_shift_if_no_finite_tadpole_matching_GeV=sigma_shift,
        additional_fractional_carrier_shift_from_this_tadpole=a*sigma_shift/(m*m),
        beta_carrier_mass_squared_from_a_GeV2=a*a/(8*math.pi**2),
        beta_gap_from_a_GeV2=-a*a/(2*math.pi**2),
        positive_sigma_induced_low_frequency_Z=a*a/(96*math.pi**2*m*m),
        compensated_extra_quartic=a*a/(2*ms*ms),zeta_NR_GeVminus2=zi/(2*m),
        u_R_GeVminus2=uR,u0_GeVminus2=bb*bb/(ms*ms)+uR,
        partial_scalar_CW_at_mu_m_GeV4=dict(Phi=vacuum_phi,X=vacuum_X,sigma=vacuum_sigma),
        partial_scalar_CW_sum_over_reference=(vacuum_phi+vacuum_X+vacuum_sigma)/rho_ref)
    rows.append(row)
check('weaker selected comparison retains open threshold',rows[-1]['source_decay_open_in_unretuned_MS_comparison'])
result=dict(parameters=p,scheme='MSbar mass-parameter diagnostic at mu=m; sigma tadpole separately renormalized to0 for pole comparison; only new a^2 loop retained; no finite on-shell mass matching',
    CW_potential='(m^2+a sigma)^2/(32 pi^2) [ln((m^2+a sigma)/mu^2)-3/2]',
    sigma_dependent_Tr_Hessian_squared=str(dependent),reference_vacuum_GeV4=rho_ref,
    rows=rows,checks=checks,non_claims=['MS gap diagnostic is not a physical exclusion when pole masses are separately fixed','No complete beta functions, multiloop, Higgs/fermion/frame or finite-density quantum matching','Partial scheme-dependent CW constants are not a measured cosmological constant prediction','No neutral abundance/coldness, galaxy, metric or novelty closure'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(controls=len(checks),rows=rows),indent=2))
