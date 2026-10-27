"""Small exact/finite original-action hard-channel calculation, not kinetics."""
import json
import math
import sys
from pathlib import Path

import sympy as s

out = Path(sys.argv[1])
assert out.is_dir()
checks = []


def check(name, value):
    value = bool(value)
    checks.append({"name": name, "passed": value})
    assert value, name


M, m, g, p, z = s.symbols("M m g p z", positive=True)
X, Xstar, phi, phistar = s.symbols("X Xstar phi phistar")
Lint = -g*(Xstar*phi**2+X*phistar**2)
check("cubic X Phi-star Phi-star vertex coefficient", s.diff(Lint, X, phistar, phistar) == -2*g)
check("charge-forbidden X Phi-star Phi vertex absent", s.diff(Lint, X, phistar, phi) == 0)
E2 = M*M+p*p
k2 = E2-m*m
t_minus_m2 = M*M-2*E2+2*p*s.sqrt(k2)*z
check("threshold virtual daughter denominator", s.simplify(t_minus_m2.subs(p, 0)+M*M) == 0)
amplitude = -4*g*g/t_minus_m2
check("threshold amplitude positive sign", s.simplify(amplitude.subs(p, 0)-4*g*g/M**2) == 0)
A = M*M+2*p*p
B2 = 4*p*p*k2
check("angular denominator positive exact invariant", s.expand(A*A-B2-M**4-4*m*m*p*p) == 0)

# Integral of 1/(A-Bz)^2: evaluate its elementary antiderivative at +-1.
aa, bb = s.symbols("A B", positive=True)
anti = 1/(bb*(aa-bb*z))
check("angular elementary antiderivative", s.simplify(s.diff(anti, z)-1/(aa-bb*z)**2) == 0)
angle_integral = s.simplify(anti.subs(z, 1)-anti.subs(z, -1))
check("angular integral exact endpoints", s.simplify(angle_integral-2/(aa*aa-bb*bb)) == 0)

E, k = s.symbols("E k", positive=True)
# d sigma/dOmega = |M|^2 k/(64 pi^2 s p); v_rel=2p/E.
sigma_v_general = s.simplify((k/(64*s.pi**2*(4*E*E)*p))*(2*p/E)
    *(2*s.pi)*(16*g**4)*(2/(A*A-B2)))
check("CM flux and angular normalization", s.simplify(
    sigma_v_general-g**4*k/(2*s.pi*E**3*(M**4+4*m*m*p*p))) == 0)
beta_f = s.sqrt(1-m*m/(M*M))
sv0 = beta_f*g**4/(2*s.pi*M**6)
check("threshold sigma-v coefficient", s.simplify(
    sigma_v_general.subs({p: 0, E: M, k: M*beta_f})-sv0) == 0)

beta_dec = s.symbols("beta_dec", positive=True)
# Decay amplitude squared 4g^2; integrated two-body phase beta/(8pi),
# one initial 1/(2M), one identical-final 1/2!.
Gamma = s.simplify((4*g*g)*beta_dec/(8*s.pi)/(2*M)/2)
check("decay identical-final normalization", Gamma == g*g*beta_dec/(8*s.pi*M))
nopp = s.symbols("nopp", positive=True)
check("annihilation per-source to decay ratio", s.simplify(
    nopp*sv0/Gamma-4*nopp*g*g*beta_f/(M**5*beta_dec)) == 0)
u = s.symbols("u", positive=True)
MofU = 2*m*s.sqrt(1+u*u)
check("exact decay velocity in u-star", s.simplify(
    s.sqrt(1-4*m*m/MofU**2)-u/s.sqrt(1+u*u)) == 0)
check("hard daughter momentum vs mass", s.simplify(
    (MofU**2-m*m)/m**2-(3+4*u*u)) == 0)

nu = (-1, -1, 1, 1)  # X+, X-, Phi+, Phi-
check("signed exact charge event moment", sum(a*b for a,b in zip(nu,(2,-2,1,-1))) == 0)
check("weighted positive all-mode event moment", sum(a*b for a,b in zip(nu,(2,2,1,1))) == -2)
check("weighted soft-only event moment", sum(a*b for a,b in zip(nu,(2,2,0,0))) == -4)
check("ordinary quasiparticle count is two-to-two", sum(nu) == 0)
check("full relativistic event energy", s.simplify(-2*M+2*s.sqrt(m*m+M*M-m*m)) == 0)
check("source-decay weighted positive moment", sum(a*b for a,b in zip((-1,0,2,0),(2,2,1,1))) == 0)

alpha = s.symbols("alpha", positive=True)
ann_fraction = 1-s.log(1+alpha)/alpha
check("decaying-bath integrated annihilation leading fraction", s.limit(ann_fraction/alpha, alpha, 0, dir="+") == s.Rational(1,2))

# Reconstruct the declared benchmark, without importing its runnable old script.
hbarc_GeV_cm = 1.973269804e-14
GeV_in_g = 1.7826619216279e-24
c_cm_s = 2.99792458e10
hbar_GeV_s = hbarc_GeV_cm/c_cm_s
mass = .001
ustar = .02
rlambda = 2.
sigma_mass_cm2_g = .3
sigma_mass_natural = sigma_mass_cm2_g*GeV_in_g/hbarc_GeV_cm**2
lambda_rep = math.sqrt(8*math.pi*mass**3*sigma_mass_natural)
source_mass = 2*mass*math.sqrt(1+ustar**2)
gap = 4*mass**2*ustar**2
coupling = math.sqrt(lambda_rep*gap/rlambda)
bd = ustar/math.sqrt(1+ustar**2)
bf = math.sqrt(1-mass**2/source_mass**2)
width = coupling**2*bd/(8*math.pi*source_mass)
sv = bf*coupling**4/(2*math.pi*source_mass**6)
sv_cm3_s = sv*hbarc_GeV_cm**2*c_cm_s
gamma_s = width/hbar_GeV_s
ratio_per_n_over_M3 = 4*(coupling/source_mass)**2*bf/bd
ncrit_GeV3 = width/sv
ncrit_cm3 = ncrit_GeV3/hbarc_GeV_cm**3
check("benchmark source is a narrow unstable quasiparticle", width/source_mass < 1e-8)
check("benchmark hard daughters leave cold production band", math.sqrt(source_mass**2-mass**2)/(mass*ustar) > 80)
check("benchmark cm and natural density ratios agree", abs(
    (sv_cm3_s/gamma_s)*(source_mass/hbarc_GeV_cm)**3/ratio_per_n_over_M3-1) < 2e-15)
check("benchmark critical-density forms agree", abs(
    ncrit_GeV3/source_mass**3*ratio_per_n_over_M3-1) < 2e-15)

# Independent direct angular quadrature approaches threshold and matches exact
# finite-p CM formula; four fixed NR source momenta only.
angle_rows = []
for p_over_M in (.0001, .001, .01, .1):
    pin = source_mass*p_over_M
    energy = math.sqrt(source_mass**2+pin**2)
    kout = math.sqrt(energy**2-mass**2)
    a = source_mass**2+2*pin**2
    b = 2*pin*kout
    panels = 2000
    step = 2/panels
    total = 0.
    for j in range(panels+1):
        zz = -1+j*step
        weight = 1 if j in (0,panels) else (4 if j%2 else 2)
        total += weight/(a-b*zz)**2
    quad = total*step/3
    numerical_sv = kout/(128*math.pi**2*energy**3)*(2*math.pi)*(16*coupling**4)*quad
    closed_sv = coupling**4*(kout/energy)/(2*math.pi*energy**2*(source_mass**4+4*mass**2*pin**2))
    error = abs(numerical_sv/closed_sv-1)
    check("direct angular quadrature p/M="+str(p_over_M), error < 2e-12)
    angle_rows.append({"p_over_M":p_over_M,"sigma_v_over_threshold":closed_sv/sv,
                       "direct_angular_relative_error":error})

density_rows=[]
for density_ratio in (1e-12,1e-6,1e-3,1.):
    rate_ratio = ratio_per_n_over_M3*density_ratio
    # Stable evaluation of 1-log(1+a)/a at very small a.
    fraction = sum(((-1)**(j+1))*rate_ratio**j/(j+1) for j in range(1,6)) if rate_ratio < .001 else 1-math.log1p(rate_ratio)/rate_ratio
    check("positive integrated weighted defect density ratio="+str(density_ratio), 0 < fraction < rate_ratio/2)
    density_rows.append({"n_opposite_over_M_cubed":density_ratio,
                         "instant_annihilation_over_decay":rate_ratio,
                         "soft_weighted_defect_fraction_in_decay_only_bath":fraction,
                         "all_mode_weighted_defect_fraction_in_decay_only_bath":fraction/2})

result={"assertion_tested":"Exact cubic vertex/CM denominator/flux/stoichiometry/decay-ratio identities, declared benchmark reconstruction, four independent angular integrals and density-dependent hierarchy table.",
        "checks_count":len(checks),"checks":checks,
        "benchmark":{"m_GeV":mass,"u_star":ustar,"r_lambda":rlambda,
          "sigma0_over_m_cm2_per_g":sigma_mass_cm2_g,"M_GeV":source_mass,
          "lambda_rep":lambda_rep,"g_GeV":coupling,"g_over_M":coupling/source_mass,
          "beta_decay":bd,"beta_hard_final":bf,"hard_p_over_m":math.sqrt(source_mass**2-mass**2)/mass,
          "Gamma_decay_GeV":width,"Gamma_decay_per_s":gamma_s,"decay_lifetime_s":1/gamma_s,
          "sigma_v_GeV_minus2":sv,"sigma_v_cm3_per_s":sv_cm3_s,
          "ratio_coefficient_per_n_opposite_over_M3":ratio_per_n_over_M3,
          "density_for_equal_per_source_annihilation_and_decay_GeV3":ncrit_GeV3,
          "density_for_equal_per_source_annihilation_and_decay_cm_minus3":ncrit_cm3,
          "density_for_equal_rates_over_M3":ncrit_GeV3/source_mass**3,
          "density_for_equal_rates_over_m3":ncrit_GeV3/mass**3},
        "angular_comparisons":angle_rows,"density_rows":density_rows,
        "scope":"Leading vacuum tree channel with prepared narrow X quasiparticles, dilute factorized occupations and no final stimulation; no kinetic evolution simulation.",
        "non_claims":["No exhaustive all-channel number-loss audit, finite-density Bose/inverse corrections or cosmological/halo current theorem.","Weighted positive source/daughter number is not an exact relativistic charge; ordinary particle count happens to be 2-to-2 in this channel.","Integrated defect table assumes a neutral equal-sign source stock with decay and this annihilation alone, and ignores inverse/hard-population backreaction."]}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({"checks":len(checks),"benchmark":result['benchmark'],"density_rows":density_rows},indent=2))
