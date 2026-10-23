"""Exact witness and conditional response scales; see CONTRACT.md."""
import json, math, sys
from pathlib import Path
import sympy as s

x=s.symbols('x', real=True)
K, eta, beta, J, Lam=s.symbols('K eta beta J Lambda', positive=True)
q2=(2+3*beta)/(12*K)*(J**2/(2*eta)+Lam/(2*K))
H=s.simplify(-12*K*q2/(2+3*beta)+J**2/(2*eta)+Lam/(2*K))
N,M=s.sin(x),s.cos(x)
clock=0 if '--mutate' in sys.argv else 1
bracket=s.integrate(clock*J/eta*(N*s.diff(M,x)-M*s.diff(N,x)),(x,0,2*s.pi))
checks={
 'constraint_surface': H==0,
 'lapse_bracket_nonzero': s.simplify(bracket+2*s.pi*J/eta)==0,
 'clock_deletion_removes_witness': s.simplify(bracket.subs(J,0))==0,
}
# Independent canonical finite-difference gradient, periodic grid, J=eta=1.
# H[N] = dx sum N_j [pi_j^2/2 + (P_{j+1}-P_{j-1})/(2dx)].
# Canonical bracket {P_j,pi_l}=delta_jl/dx.
grids=[]
for n in [32,64,128,256]:
 dx=2*math.pi/n
 nv=[math.sin(j*dx) for j in range(n)]
 mv=[math.cos(j*dx) for j in range(n)]
 dHPn=[clock*(nv[(j-1)%n]-nv[(j+1)%n])/2 for j in range(n)]
 dHPm=[clock*(mv[(j-1)%n]-mv[(j+1)%n])/2 for j in range(n)]
 b=sum((dHPn[j]*(dx*mv[j])-(dx*nv[j])*dHPm[j])/dx for j in range(n))
 exact_grid=-clock*n*math.sin(dx)
 grids.append({'n':n,'bracket':b,'analytic_grid':exact_grid,'continuum_error':abs(b+2*math.pi)})
 checks['grid_'+str(n)]=abs(b-exact_grid)<1e-12
checks['grid_convergence']=grids[-1]['continuum_error']<grids[0]['continuum_error']/50
# SI restoration: angular frequency = c sqrt[(L^2/2) k^4 / ((2+3b)/b+(L^2/2) k^2)].
c=299792458.; pc=3.085677581491367e16; Gyr=365.25*86400*1e9
b=.02798
rows=[]
for Lpc in [24.,30.,90.]:
 L=Lpc*pc
 D=c*L*math.sqrt(b/(2*(2+3*b)))
 for Rkpc in [1.,10.,30.,100.,1000.]:
  R=Rkpc*1000*pc; k=1/R
  omega=c*math.sqrt((L*L/2)*k**4/((2+3*b)/b+(L*L/2)*k*k))
  t=1/omega/Gyr
  tmin=R*R/D/Gyr
  expected_ratio=math.sqrt(1+(L*L/2)*k*k*b/(2+3*b))
  checks['time_bound_'+str((Lpc,Rkpc))]=t>=tmin and abs(t/tmin-expected_ratio)<1e-12
  rows.append({'L_pc':Lpc,'R_kpc':Rkpc,'inverse_omega_Gyr':t,'eta_zero_infimum_Gyr':tmin})
 checks['r_scaling_'+str(Lpc)]=abs(rows[-1]['eta_zero_infimum_Gyr']/rows[-2]['eta_zero_infimum_Gyr']-100)<1e-10
# Even velocity distribution: normalised inward and outward fractions exactly equal.
v=s.symbols('v', real=True)
fin=s.integrate(s.exp(-v*v)/s.sqrt(s.pi),(v,-s.oo,0))
checks['inward_even_fraction']=fin==s.Rational(1,2)
result={'checks':checks,'all_pass':all(checks.values()),'constraint_residual':str(H),
 'q_squared':str(q2),'continuum_bracket':str(bracket),'grids':grids,
 'response_assumptions':{'beta':b,'eta_over_gamma':1,'k_definition':'1/R; R is inverse wavenumber, not wavelength','footings':'a0 cancels at fixed L and beta; identical on both footings'},
 'response':rows,'R_at_10Gyr_kpc':{str(Lpc):math.sqrt(c*Lpc*pc*math.sqrt(b/(2*(2+3*b)))*10*Gyr)/(1000*pc) for Lpc in [24.,30.,90.]},
 'inward_fraction':str(fin),'mutated':bool('--mutate' in sys.argv)}
out=Path(sys.argv[1]); out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
for k,val in checks.items(): print(k, 'PASS' if val else 'FAIL')
print('bracket =',bracket,'; response radii:',result['R_at_10Gyr_kpc'])
print('COMPLETE:',sum(checks.values()),'/',len(checks))
sys.exit(0 if result['all_pass'] else 1)
