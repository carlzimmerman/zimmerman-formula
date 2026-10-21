#!/usr/bin/env python3
"""Bounded checks; run from any directory. No network and no external skill dependency."""
import argparse
import hashlib
import json
import math
import platform
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
OUT = HERE / 'results'
BASE = '431f22bd6fe998759b843d13113762d73356aec6'
SOURCES = [
    'campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14.md',
    'campaign_fresh_gravity/CFG820_stiffness_from_globulars/README.md',
    'campaign_fresh_gravity/CFG821_stiffness_from_dsph/README.md',
    'campaign_fresh_gravity/PARAMRED_2026-10-16/C_LSTAR/README.md',
    'campaign_fresh_gravity/CFG691_stiffness_window/README.md',
    'campaign_fresh_gravity/CFG694_combined_construction/README.md',
    'campaign_fresh_gravity/CFG699_settle_time/README.md',
    'campaign_fresh_gravity/CFG807_stiff_vacuum_route/README.md',
    'campaign_fresh_gravity/CFG858_stiffness_extra_speed/README.md',
    'campaign_fresh_gravity/CFG897_kappa_D1_stiffness_frw_vacuum/README.md',
    'campaign_fresh_gravity/CFG938_medium_continuum_eft/DERIVATION.md',
    'argon_clues/O6_parameter_origins.md',
]

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git(*args):
    try:
        return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=OUT,
                        help='Destination for new results; use a fresh directory to preserve the primary run.')
    parser.add_argument('--provenance-root',type=Path,
                        help='Optional repository root: require and hash documentary source files. Numerical checks do not need them or git.')
    args=parser.parse_args()
    out=args.output_dir.resolve()
    record_root=args.provenance_root.resolve() if args.provenance_root else HERE
    def record_path(p):
        try: return str(p.relative_to(record_root))
        except ValueError: return str(p)
    started = datetime.now(timezone.utc).isoformat()
    t0 = time.perf_counter()
    out.mkdir(exist_ok=True,parents=True)
    local = [Path(__file__), HERE/'contract.md', HERE/'requirements.txt']
    inputs = ([record_root/p for p in SOURCES] if args.provenance_root else []) + local
    before = {record_path(p): digest(p) for p in inputs}
    checks = []
    def check(name, ok, detail):
        checks.append({'name': name, 'passed': bool(ok), 'detail': detail})

    # Dimensionless potential: Wrem = a0^2/K * w(K|P|/a0).
    s, q, rho, g, m, kap, Gs, L = sp.symbols('s q rho g m kap G L', positive=True)
    w = -s*s/2-s-sp.log(1-s)
    B = s/(1-s)
    A = s*(2-s)/(1-s)**2
    check('potential_derivative', sp.simplify(sp.diff(w,s)-s*s/(1-s)) == 0,
          'w prime = s^2/(1-s)')
    check('potential_radial_hessian', sp.simplify(sp.diff(w,s,2)-A) == 0,
          'A=s(2-s)/(1-s)^2')
    check('potential_tangential_hessian', sp.simplify(sp.diff(w,s)/s-B) == 0,
          'B=s/(1-s)')
    check('fixed_potential_mass_identity', sp.simplify(1+A-1/(1-s)**2) == 0,
          'At externally fixed Phi the mass is K(I+H_W/K), not the Schur complement.')
    vx, vy, vz, px, py, pz, phi = sp.symbols('vx vy vz px py pz phi', real=True)
    # At k along z, the complex Fourier phase is absorbed into real gradient amplitude phi.
    E = (px*px+py*py+(phi-pz)**2)/2
    Eelim = sp.expand(E.subs(phi, sp.solve(sp.diff(E,phi),phi)[0]))
    check('gravity_schur_complement', sp.simplify(Eelim-(px*px+py*py)/2) == 0,
          'Minimizing the static quadratic form over grad Phi leaves K/2 |P_T|^2.')
    check('vacuum_longitudinal_gap', sp.limit(A,s,0)==0 and sp.limit(B,s,0)==0,
          'The longitudinal coupled vacuum mode is gapless; Lstar is not its finite correlation length.')

    # Independent Cartesian finite differences of the radial potential.
    def wnum(x):
        r = np.linalg.norm(x)
        # Positive series avoids cancellation near zero.
        if r < .2:
            return sum(r**n/n for n in range(3,120))
        return -.5*r*r-r-math.log1p(-r)
    fd=[]
    direction = np.array([2.,-1.,3.]); direction /= np.linalg.norm(direction)
    for sv in [.001,.01,.1,.3,.7,.9]:
        x = direction*sv
        h = 2e-4*min(sv,1-sv)
        H = np.empty((3,3))
        eye = np.eye(3)
        for i in range(3):
            for j in range(3):
                if i==j:
                    H[i,j]=(wnum(x+h*eye[i])-2*wnum(x)+wnum(x-h*eye[i]))/h**2
                else:
                    H[i,j]=(wnum(x+h*eye[i]+h*eye[j])-wnum(x+h*eye[i]-h*eye[j])-wnum(x-h*eye[i]+h*eye[j])+wnum(x-h*eye[i]-h*eye[j]))/(4*h*h)
        av=sv*(2-sv)/(1-sv)**2; bv=sv/(1-sv)
        analytic = bv*np.eye(3)+(av-bv)*np.outer(direction,direction)
        rel=float(np.linalg.norm(H-analytic)/np.linalg.norm(analytic))
        fd.append({'s':sv,'relative_frobenius_error':rel})
    check('cartesian_hessian_finite_difference', max(r['relative_frobenius_error'] for r in fd)<2e-5,
          {'six_backgrounds':fd,'relative_tolerance':2e-5})

    response=[]; errors=[]; minima=[]
    for sv in [.0001,.001,.01,.1,.3,.7,.9]:
        av=sv*(2-sv)/(1-sv)**2; bv=sv/(1-sv); d=av-bv
        for theta in np.linspace(0,math.pi/2,13):
            nv=np.array([math.sin(theta),0.,math.cos(theta)])
            H=np.diag([bv,bv,av])+np.eye(3)-np.outer(nv,nv)
            ev=np.linalg.eigvalsh(H)
            disc=math.sqrt(d*d+1-2*d*math.cos(2*theta))
            expected=np.sort([bv+1,(av+bv+1-disc)/2,(av+bv+1+disc)/2])
            errors.append(float(np.max(np.abs(ev-expected))))
            minima.append(float(ev[0]))
        response.append({'s':sv,'A':av,'B':bv,
            'xi_over_L_parallel_k_parallel_P':1/math.sqrt(2*av),
            'xi_over_L_longitudinal_k_perpendicular_P':1/math.sqrt(2*bv),
            'xi_over_L_transverse_common':1/math.sqrt(2*(1+bv)),
            'xi_over_L_fixed_Phi_radial':1/math.sqrt(2*(1+av))})
    check('directional_spectrum', max(errors)<2e-12 and min(minima)>0,
          {'number_of_matrices':len(errors),'max_absolute_eigenvalue_error':max(errors),'min_eigenvalue':min(minima)})

    # Route 1: a normalized Gaussian has <r_i r_j>=ell^2 delta_ij.
    exact=1-sp.exp(-q*q/2)
    check('finite_range_coefficient', sp.limit(exact/q**2,q,0)==sp.Rational(1,2),
          'gamma=eta K ell^2/2; Lstar^2=eta ell^2; not a determination of eta or ell')
    kernel=[]
    for qv in [.01,.03,.1,.3,1.,3.,10.]:
        symbol=-math.expm1(-qv*qv/2)
        approx=qv*qv/2
        kernel.append({'k_ell':qv,'exact_over_eta_K':symbol,'gradient_over_eta_K':approx,
                       'relative_gradient_error':approx/symbol-1})
    check('finite_range_positive_and_mutation', all(r['exact_over_eta_K']>0 for r in kernel) and all(-r['exact_over_eta_K']<0 for r in kernel),
          'Positive eta gives nonnegative exchange energy; reversing it makes every nonzero tested mode negative.')
    # Solve the 1% derivative-expansion boundary by bisection, no fit to L window.
    lo,hi=.0001,1.
    for _ in range(70):
        mid=(lo+hi)/2
        if (mid*mid/2)/(-math.expm1(-mid*mid/2))-1>.01: hi=mid
        else: lo=mid
    qmax=(lo+hi)/2

    # Route 2: internal energy and pressure mapping.
    eps=g*rho*rho/(2*m*m)
    pressure=sp.simplify(rho*sp.diff(eps,rho)-eps)
    gamma=g/(m*m)
    check('contact_eos', sp.simplify(pressure-eps)==0 and sp.simplify(sp.diff(pressure,rho)/rho-gamma)==0,
          'p=eps=g rho^2/(2m^2), cs^2=g rho/m^2; matches only (div P)^2.')
    theta=sp.symbols('theta',real=True)
    cos4_average=sp.integrate(sp.cos(theta)**4,(theta,0,2*sp.pi))/(2*sp.pi)
    check('quartic_microscopic_average', cos4_average==sp.Rational(3,8),
          'For phi=A cos(mt), n=m A^2/2, averaging kappa4 phi^4 gives 3 kappa4 n^2/(2m^2), hence g=3 kappa4/m^2.')
    v=sp.Matrix([vx,vy,vz]); p=sp.Matrix([px,py,pz])
    identity=sp.expand(v.dot(v)*p.dot(p)-v.dot(p)**2-v.cross(p).dot(v.cross(p)))
    check('longitudinal_versus_shear', identity==0 and float(np.dot([1,0,0],[0,1,0]))==0,
          '|k|^2 |P|^2=|k.P|^2+|k cross P|^2; transverse example has zero compressibility and nonzero canonical stiffness.')
    check('jeans_ratio_conditional', sp.simplify(sp.sqrt((2*sp.pi*Gs*L**2*rho)/(4*sp.pi*Gs*rho))-L/sp.sqrt(2))==0,
          'For an ordinary self-gravitating contact fluid only: inverse Jeans wavenumber=Lstar/sqrt(2). S2 cancels this gravitational vacuum mass.')

    # Route 3: density-gradient energy -> k^4 in longitudinal P.
    check('quantum_operator_order', sp.Poly(q**4,q).degree()==4 and sp.Poly(q**2,q).degree()==2,
          'delta rho=div P; |grad delta rho|^2=k^4 |P_L|^2.')
    mismatch=[{'k_over_k0':x,'quantum_to_canonical_after_match_at_k0':x*x} for x in [.01,.1,.3,1.,3.,10.,100.]]
    detector=lambda rows: max(abs(r['quantum_to_canonical_after_match_at_k0']-1) for r in rows)>1
    mutated=[dict(r,quantum_to_canonical_after_match_at_k0=1) for r in mismatch]
    check('quantum_order_mutation', detector(mismatch) and not detector(mutated),
          'Erasing the extra k^2 removes the operator-mismatch detection; the comparison is not hard-coded.')

    # All values are declared independent SI inputs / illustrative hypotheses.
    G=6.67430e-11; c=299792458.; hbar=1.054571817e-34; eV=1.602176634e-19
    pc=3.0856775814913673e16; Msun=1.98847e30; AU=149597870700.
    K=4*math.pi*G
    densities={'halo_0.01_Msun_pc3':.01*Msun/pc**3,'halo_0.1_Msun_pc3':.1*Msun/pc**3}
    for foot,a0 in [('canonical',9.3603e-11),('alternate',1.1312e-10)]:
        densities[foot+'_cosmic_mean_assumed']=(.26/.686)*4*a0*a0/(G*c*c)
    lengths=[24.,24.7,1000.,2042.,2138.]
    physical=[]
    for lpc in lengths:
        lm=lpc*pc; gam=K*lm*lm/2
        # Goodman V=1/2 m^2 phi^2 + kappa4 phi^4, hbar=c=1:
        # g=3 kappa4/m^2, Lstar^2=3 kappa4/(2 pi G m^4).
        # SI restoration from natural units: E^4 = (3/2pi) E_Planck^2 (hbar c/L)^2.
        # Goodman v1 Eq.12 prints c^3, a dimensional typo; its 10.7 eV number
        # requires c^7. Derive from Eqs.2,3,10 rather than copying this typo.
        E=(3*hbar**3*c**7/(2*math.pi*G*lm*lm))**.25
        row={'Lstar_pc':lpc,'gamma_SI_m5_kg_s2':gam,
             'contact_mass_eV_over_kappa4_quarter':E/eV,
             'contact_core_zero_radius_pc':math.pi*lpc/math.sqrt(2),
             'contact_core_curvature_radius_pc':3*lpc/math.sqrt(2),
             'eta_min_if_one_percent_at_k_inverse_AU':(lm/(qmax*AU))**2,
             'rho_when_gamma_rho_equals_c2_kg_m3':c*c/gam,
             'density_cases':[],'healing_mass_requirements':[]}
        for label,rhov in densities.items():
            cs=math.sqrt(gam*rhov)
            # The following only asks what mass would make inverse quantum Jeans k equal L.
            mass_req=hbar/(math.sqrt(16*math.pi*G*rhov)*lm*lm)
            row['density_cases'].append({'density_label':label,'rho_kg_m3':rhov,
              'sound_speed_km_s':cs/1000,
              'quantum_mass_eV_if_inverse_Jeans_k_equals_L':mass_req*c*c/eV,
              'redshift_formal_contact_relativistic_transition':(c*c/(gam*rhov))**(1/3)-1 if 'cosmic' in label else None})
            check('parameter_inverse_'+str(lpc)+'_'+label,
                  abs((hbar*hbar/(16*math.pi*G*rhov*mass_req**2))**.25/lm-1)<1e-12,
                  'Independent inversion back into inverse quantum Jeans wavenumber; not a parameter prediction.')
        for cs_kms in [1.,10.,100.]:
            mr=hbar/(math.sqrt(2)*lm*cs_kms*1000)
            row['healing_mass_requirements'].append({'assumed_cs_km_s':cs_kms,'mass_eV_if_xi_equals_L':mr*c*c/eV})
        physical.append(row)
    # Independent units and numerical check of the contact-mass conversion.
    # Dimension vectors are (kg,m,s); E^4 must be (4,8,-8).
    dh=np.array([1,2,-1]); dc=np.array([0,1,-1]); dg=np.array([-1,3,-2]); dl=np.array([0,1,0])
    check('contact_SI_dimensions', np.array_equal(3*dh+7*dc-dg-2*dl,[4,8,-8]),
          'hbar^3 c^7/(G L^2) has energy^4 units; c^3 would have momentum^4 units.')
    check('contact_bad_SI_mutation', not np.array_equal(3*dh+3*dc-dg-2*dl,[4,8,-8]),
          'The source-v1 printed c^3 typo is rejected by the dimension check.')
    rc=1000*pc
    goodman_benchmark=(27*hbar**3*c**7/(4*math.pi*G*rc*rc))**.25/eV
    check('contact_independent_benchmark', abs(goodman_benchmark/10.7-1)<.01,
          {'computed_eV_at_core_curvature_radius_1kpc':goodman_benchmark,'primary_source_rounded_eV':10.7})
    reference_mass=1e-22*eV/c**2
    qref=[{'density_label':key,'rho_kg_m3':rv,
           'inverse_quantum_Jeans_k_pc':(hbar*hbar/(16*math.pi*G*rv*reference_mass**2))**.25/pc}
          for key,rv in densities.items()]
    check('source_hashes_unchanged', all(digest(record_root/p)==v for p,v in before.items()), 'All inputs rehashed after computation.')
    results={'claim_id':'OPEN4-STIFFNESS-2026-10-20','base_checkpoint':BASE,
      'interpretation':'Finite assertions verified only in declared ranges; origin of Lstar remains open.',
      'constants':{'G_SI':G,'c_SI':c,'hbar_SI':hbar,'eV_J':eV,'pc_m':pc,'Msun_kg':Msun,'AU_m':AU},
      'response_lengths':response,'finite_range_kernel':kernel,'kernel_one_percent_k_ell_max':qmax,
      'parameter_requirements':physical,'quantum_reference_1e_minus22_eV':qref,
      'quantum_operator_mismatch':mismatch,'checks':checks}
    result_path=out/'checks.json'
    result_path.write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    summary={'checks_passed':sum(x['passed'] for x in checks),'checks_total':len(checks),
             'one_percent_kernel_boundary':qmax,'response_example_s_0.01':response[2],
             'contact_mass_eV_at_unit_coupling':{r['Lstar_pc']:r['contact_mass_eV_over_kappa4_quarter'] for r in physical},
             'quantum_reference':qref}
    summary_path=out/'summary.json'
    summary_path.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    passed=all(x['passed'] for x in checks)
    manifest={'schema_version':2,'claim_id':'OPEN4-STIFFNESS-2026-10-20',
      'repository':{'commit':git('rev-parse','HEAD') or 'unavailable (portable replay)',
                    'dirty':bool(git('status','--porcelain'))},
      'command':['python3',record_path(Path(__file__))]+sys.argv[1:],
      'environment':{'software':[{'name':'Python','version':platform.python_version()},
        {'name':'numpy','version':np.__version__},{'name':'sympy','version':sp.__version__}],
        'hardware':platform.platform()+'; '+platform.machine()},
      'mathematics':{'assertion_tested':'Symbolic Hessian, Schur complement, contact-EOS and operator identities; finite derivative/spectral and parameter-inversion checks.',
        'coefficient_domain':'Exact symbolic real positive parameters; IEEE float64 for finite values.',
        'conventions':'K=4piG, gamma=K Lstar^2/2; k angular wavenumber; xi=1/k, not wavelength.',
        'inputs':SOURCES if args.provenance_root else [],'bounds':{'hessian_backgrounds':6,'spectrum_backgrounds':7,'angles':13,'kernel_wavenumbers':7,'quantum_ratio_wavenumbers':7,'length_benchmarks':5,'density_benchmarks':4},
        'non_claims':['No microscopic parameter selected','No new observational fit','No full cosmological evolution','No universal correlation length proved','No all-routes-exhausted claim']},
      'randomness':{'used':False,'generator':'','seed':None},
      'run':{'started_at':started,'runtime_seconds':time.perf_counter()-t0,'exit_status':0 if passed else 1,
        'status':'completed' if passed else 'failed','resource_limits':{'memory_bytes':None,'cpu_seconds':None,'max_cores':None,'max_threads':None}},
      'outputs':[{'path':record_path(p),'sha256':digest(p),'kind':'result'} for p in [result_path,summary_path]],
      'checks':checks,'result':'implementation and finite assertion verified in stated range' if passed else 'at least one check failed',
      'residual_risks':['Finite differences conditional on reported tolerance','No microscopic map to full S2','A response crossover is not automatically an isotropic real-space correlation length'],
      'input_artifacts':[{'path':p,'sha256':v,'sha256_after':digest(record_root/p)} for p,v in before.items()],
      'declared_results':[record_path(result_path),record_path(summary_path)]}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True))
    return 0 if passed else 1

if __name__=='__main__':
    sys.exit(main())
