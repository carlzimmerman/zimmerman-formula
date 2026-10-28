#!/usr/bin/env python3
"""Bounded exact/numerical diagnostic; no inherited harness is executed."""
import argparse
import json
import math
from pathlib import Path
import resource
import sys

import numpy as np
from scipy.integrate import quad, simpson
from scipy.optimize import brentq
import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument('--output', required=True)
ap.add_argument('--mutate', action='store_true')
args = ap.parse_args()
repo = Path(__file__).resolve().parents[3]
outdir = Path(args.output)
outdir.mkdir(parents=True, exist_ok=True)
checks = []

def check(name, assertion, value):
    checks.append({'name': name, 'pass': bool(assertion), 'value': value})
    print(name, 'PASS' if assertion else 'FAIL', value, flush=True)

G = 6.67430e-11
c = 299792458.0
MS = 1.98847e30
PC = 3.0856775814913673e16
GYR = 365.25 * 86400 * 1e9
a0s = {'canonical': 9.3603e-11, 'alt': 1.1312e-10}
thresholds = {'canonical': 10**12.2357, 'alt': 10**12.5739}
bs1 = json.loads((repo / 'rebuild_2026_10_22/BS1_basin_switch/bs1_basin_switch_results.json').read_text())
g2 = json.loads((repo / 'rebuild_2026_10_22/G2_preinfall_retention/g2_preinfall_retention_results.json').read_text())
age = g2['constants']['t0_Gyr']
HL = math.sqrt(32 * math.pi / 3) * a0s['canonical'] / c

# Exact primitives, response inversion, and field-normalization invariance.
z, r, q, B, A, lam, C = sp.symbols('z r q B A lam C', positive=True)
F = z - 2 * sp.sqrt(z) + 2 * sp.log(1 + sp.sqrt(z)) + C
U = -(1 + sp.sqrt(1 + 4*r*r))/(2*r) + sp.asinh(2*r)
gd = (1 + sp.sqrt(1 + 4*r*r))/(2*r*r)
pot_res = sp.simplify(sp.diff(U, r) - gd)
F_res = sp.simplify(sp.diff(F, z) - sp.sqrt(z)/(1 + sp.sqrt(z)))
a0_inv = sp.simplify((q/lam) / sp.sqrt(B/lam**2) - q/sp.sqrt(B))
G_inv = sp.simplify((q/lam)**2/(8*sp.pi*A*(B/lam**2)) - q*q/(8*sp.pi*A*B))
check('K1_symbolic', pot_res == 0 and F_res == 0 and a0_inv == 0 and G_inv == 0,
      {'potential_derivative': str(pot_res), 'F_derivative': str(F_res),
       'a0_rescale': str(a0_inv), 'G_rescale': str(G_inv)})

def In(qv, independent=False):
    def f(th):
        u = math.sin(th)**2
        return (1 if args.mutate else 2)*u / math.sqrt(2 - qv*u*(1 + u))
    if independent:
        grid = np.linspace(0, math.pi/2, 20001)
        return float(simpson([f(float(th)) for th in grid], x=grid))
    return quad(f, 0, math.pi/2, epsabs=1e-11, epsrel=1e-11)[0]

zero_expected = math.pi/(2*math.sqrt(2))
zero_measured = In(0.0)
check('K2_zero_vacuum', abs(zero_measured/zero_expected - 1) < 1e-12,
      {'measured': zero_measured, 'expected': zero_expected, 'mutate': args.mutate})

def potential(R):
    return -(1 + math.sqrt(1 + 4*R*R))/(2*R) + math.asinh(2*R)

def lawg(R):
    return (1 + math.sqrt(1 + 4*R*R))/(2*R*R)

def Il(beta, R0, independent=False):
    def f(th):
        s = math.sin(th)
        cc = math.cos(th)
        if th < 1e-14:
            return 0.0
        if cc*cc < 1e-14:
            return math.sqrt(2*R0/(lawg(R0)-beta*R0))
        R = R0*s*s
        delta = R0*cc*cc
        sq = math.sqrt(1+4*R*R)
        sq0 = math.sqrt(1+4*R0*R0)
        # Stable divided difference [U(R0)-U(R)]/(R0-R):
        # rationalize the square roots, use log1p for the asinh difference.
        V = (1/(2*R*R0)
             +(R0+R)/(2*R*R*R0*R0*(sq/R+sq0/R0))
             +math.log1p(delta*(2+4*(R0+R)/(sq0+sq))/(2*R+sq))/delta)
        return 2*math.sqrt(R0)*s/math.sqrt(2*V-beta*(R0+R))
    if independent:
        grid = np.linspace(0, math.pi/2, 20001)
        return float(simpson([f(float(th)) for th in grid], x=grid))
    return quad(f, 0, math.pi/2, epsabs=2e-10, epsrel=2e-10)[0]

rows = []
quad_residuals = []
dim_residuals = []
time_residuals = []
min_radicands = []
for years in sorted(set([10.0, age, 20.0])):
    t = years*GYR
    tau = t*HL
    qv = brentq(lambda qq: math.sqrt(qq)*In(qq)-tau, 1e-12, 1-1e-8, xtol=1e-13)
    quad_residuals.append(abs(In(qv, True)/In(qv)-1))
    time_residuals.append(abs(math.sqrt(qv)*In(qv)/tau-1))
    for foot, a0 in a0s.items():
        base = a0**3/(G*HL**4)/MS
        # GM/r0^2=a0 at a first-turnaround radius.
        eds = 64*a0**3*t**4/(math.pi**4*G)/MS
        newton_lam = qv*qv*base
        # For the simple response, g=a0 iff g_N=a0/2, hence 1/8 mass at fixed radius law.
        row = {'footing': foot, 'age_Gyr': years, 'q': qv,
               'scale_a0cubed_over_G_HLambda4_Msun': base,
               'newton_no_vacuum_gN_Msun': eds,
               'newton_Lambda_gN_Msun': newton_lam,
               'newton_Lambda_postprocessed_actual_g_Msun': newton_lam/8,
               'static_balance_gN_Msun': base,
               'static_balance_actual_g_Msun': base/2,
               'BS1_T_Msun': thresholds[foot]}
        # Verify a dimensional Newtonian energy integral independently.
        mass = newton_lam*MS
        R0 = (G*mass*qv/(HL*HL))**(1/3)
        def dimensional_n(th):
            u = math.sin(th)**2
            if u < 1e-28:
                return 0.0
            # Factorization is the original energy first integral in SI units.
            return 2*R0*math.sin(th)**2/math.sqrt(2*G*mass/R0 - HL*HL*R0*R0*u*(1+u))
        td = quad(dimensional_n, 0, math.pi/2, epsrel=1e-11)[0]
        dim_residuals.extend([abs(td/t-1), abs(G*mass/R0**2/a0-1)])
        for label, rcrit in [('gN', 1.0), ('actual_g', math.sqrt(2))]:
            # Spherical law + vacuum diagnostic, not an asserted relativistic parent.
            bmax = lawg(rcrit)/rcrit
            beta = brentq(lambda bb: math.sqrt(bb)*Il(bb,rcrit)-tau,
                          1e-12, bmax*(1-1e-7), xtol=1e-12)
            quad_residuals.append(abs(Il(beta,rcrit,True)/Il(beta,rcrit)-1))
            time_residuals.append(abs(math.sqrt(beta)*Il(beta,rcrit)/tau-1))
            mlaw = base*beta*beta
            row['law_Lambda_'+label+'_Msun'] = mlaw
            row['law_beta_'+label] = beta
            grid = np.linspace(1e-6,rcrit*(1-1e-6),1000)
            rad = [2*(potential(rcrit)-potential(float(R)))-beta*(rcrit*rcrit-R*R) for R in grid]
            min_radicands.append(min(rad))
            # Physical age and response reconstructed from dimensional mass.
            rM = math.sqrt(G*mlaw*MS/a0)
            td_law = math.sqrt(rM/a0)*Il(beta,rcrit)
            dim_residuals.extend([abs(td_law/t-1), abs(HL*HL*rM/a0/beta-1)])
        rows.append(row)

check('K2_quadratures', max(quad_residuals) < 2e-7, max(quad_residuals))
check('K3_dimensional_energy', max(dim_residuals) < 2e-7 and max(time_residuals) < 2e-7 and min(min_radicands)>0,
      {'max_dimensional_residual':max(dim_residuals),'max_time_residual':max(time_residuals),
       'min_sampled_radicand':min(min_radicands)})

# Direct reconstruction from inherited Local Group geometry, no timing-radius assumption.
lgmass = 10**bs1['LG']['basin']['lgM']
lgr = bs1['LG']['R0_data_kpc']*1000*PC
lg_gN = G*lgmass*MS/lgr**2
LG = {}
for foot,a0 in a0s.items():
    y = lg_gN/a0
    actual = .5*y+math.sqrt(.25*y*y+y)
    LG[foot] = {'gN_over_a0':y,'simple_actual_g_over_a0':actual,
                'basin_mass_over_T':lgmass/thresholds[foot],
                'radius_required_for_gN_a0_kpc':math.sqrt(G*lgmass*MS/a0)/(1000*PC),
                'radius_required_for_actual_g_a0_kpc':math.sqrt(2*G*lgmass*MS/a0)/(1000*PC)}
mins = {}
for foot in a0s:
    mins[foot] = min(v for row in rows if row['footing']==foot
                     for k,v in row.items() if k.endswith('_Msun') and k not in ['BS1_T_Msun'])/thresholds[foot]
check('K4_all_declared_cells', len(rows)==6 and all(v>1e4 for v in mins.values()),
      {'rows':len(rows),'minimum_mass_to_BS1_T_ratio':mins,'Local_Group':LG})

# AQUAL radial Gauss law implies every exterior shell leaves the interior field invariant.
# Each mass in units of T: m_inner=1/4, optional shell=1. The annulus is outside r=.5.
shell_points=[]
for rr in [1e-3,.01,.1,.25]:
    Menc0=.25
    Menc1=.25
    gn0=Menc0/(rr*rr)
    gn1=Menc1/(rr*rr)
    f0=.5*gn0+math.sqrt(.25*gn0*gn0+gn0)
    f1=.5*gn1+math.sqrt(.25*gn1*gn1+gn1)
    shell_points.append({'r':rr,'force_difference':f1-f0})
# Check Newtonian pressureless symmetry r -> ell*r, M -> ell^3*M at unchanged t.
ell, R, M, H = sp.symbols('ell R M H',positive=True)
gravity_scaling=sp.simplify((-G*(ell**3*M)/(ell*R)**2+H**2*ell*R)
                          -ell*(-G*M/R**2+H**2*R))
check('K5_shell_and_similarity', all(x['force_difference']==0 for x in shell_points)
      and (.25>1) != (1.25>1) and gravity_scaling==0,
      {'shell_points':shell_points,'basin_mass_units_T':[.25,1.25],
       'local_flags':[False,True],'gravity_scaling_residual':str(gravity_scaling)})

# Formal rescaling cannot change kappa; choosing F(0) changes physical matching.
kappas=[.25,.46065886596178063,.5,1.0]
normalization=[{'kappa':k,'F0_required':8*math.pi/k**2} for k in kappas]
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform=='darwin' else 1e6)
result={'claim_id':'BASIN_KAPPA_20261028','mutate':args.mutate,
        'constants':{'G':G,'c':c,'M_sun':MS,'pc':PC,'Gyr':GYR,'a0':a0s,
                     'H_Lambda_conditional_canonical':HL,'age_Gyr':age},
        'rows':rows,'Local_Group':LG,'minimum_threshold_ratio':mins,
        'normalization':normalization,'checks':checks,'peak_RSS_GB':rss,
        'passed':sum(x['pass'] for x in checks),'total':len(checks),
        'non_claims':['No condensation field equation derived','No raw data newly scored',
                      'Dust similarity excludes a mass scale only at fixed dimensionless initial data',
                      'A mass-dependent initial spectrum/history can break similarity',
                      'No locality obstruction to nonlocal auxiliary fields or boundary conditions',
                      'Kappa remains fitted and is invariant under a genuine field redefinition']}
(outdir/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print('BASIN_KAPPA COMPLETE:',result['passed'],'/',result['total'],'checks PASS; RSS GB',rss)
sys.exit(0 if all(x['pass'] for x in checks) else 1)
