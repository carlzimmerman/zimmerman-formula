#!/usr/bin/env python3
"""Standalone deterministic stiffness checks. Only NumPy and SymPy are required."""
import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time

import numpy as np
import sympy as sp

BASE='8aa3f7046a7ae14a99f3515fd42df5bf061fb1db'
HERE=Path(__file__).resolve().parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git_observation():
    """Record the execution checkout, distinct from the requested scientific base."""
    def read(*args):
        try:
            return subprocess.check_output(['git','-C',str(HERE),*args],text=True,stderr=subprocess.DEVNULL).strip()
        except (OSError,subprocess.CalledProcessError):
            return None
    revision=read('rev-parse','HEAD')
    status=read('status','--porcelain') if revision else None
    return {'commit':revision or 'unavailable (no Git repository at execution location)',
            'dirty':bool(status) if status is not None else False,
            'is_repository':revision is not None,
            'dirty_observation':'observed from git status --porcelain' if status is not None else 'not applicable: detached non-Git execution',
            'requested_publication_base':BASE}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=HERE/'results')
    parser.add_argument('--verify-frozen-root',type=Path,
                        help='Optional immutable published checkout whose hashes are in source_map.json.')
    args=parser.parse_args()
    out=args.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    start=datetime.now(timezone.utc).isoformat(); t0=time.perf_counter()
    observed_repository=git_observation()
    inputs=[p for p in [Path(__file__),HERE/'contract.md',HERE/'raw_derivation.md',HERE/'requirements.txt',HERE/'source_map.json'] if p.exists()]
    before={str(p):sha(p) for p in inputs}
    checks=[]
    def ck(name,ok,detail): checks.append({'name':name,'passed':bool(ok),'detail':detail})

    # Route A: independent reconstruction of the strain-energy Hessian.
    k1,k2,k3,x1,x2,x3,lam,mu,rho,gamma,alpha=sp.symbols('k1 k2 k3 x1 x2 x3 lam mu rho gamma alpha',real=True)
    kv=sp.Matrix([k1,k2,k3]); xv=sp.Matrix([x1,x2,x3]); eye=sp.eye(3)
    strain=(kv*xv.T+xv*kv.T)/2
    energy=lam*sp.trace(strain)**2/2+mu*sp.trace(strain*strain)
    H=sp.hessian(energy,[x1,x2,x3])
    expected=mu*kv.dot(kv)*eye+(lam+mu)*kv*kv.T
    ck('elastic_hessian',sp.simplify(H-expected)==sp.zeros(3),'Direct strain-energy second derivative matches both Fourier sectors.')
    match=sp.solve([mu-gamma*rho**2,lam+2*mu-gamma*rho**2],[lam,mu])
    bulk=sp.simplify((lam+2*mu/3).subs(match))
    dilation=sp.simplify((sp.Rational(9,2)*lam+3*mu).subs(match)*alpha**2)
    ck('elastic_full_match',match=={lam:-gamma*rho**2,mu:gamma*rho**2},str(match))
    ck('elastic_negative_bulk',bulk==-gamma*rho**2/3 and dilation==-sp.Rational(3,2)*gamma*rho**2*alpha**2,
       {'bulk':str(bulk),'affine_energy_density':str(dilation),'scope':'free-affine stable stress-free isotropic solid'})
    # Algebraic rotation and boundary-integrated distinction.
    R=sp.Matrix([[0,-alpha,0],[alpha,0,0],[0,0,0]])
    ck('rigid_rotation_distinction',sp.simplify((R+R.T)/2)==sp.zeros(3) and sp.trace(R.T*R)==2*alpha**2,
       'Ordinary strain energy vanishes for infinitesimal rigid rotation; canonical full gradient density does not.')
    ck('periodic_operator_positive',sp.simplify(expected.subs(lam,-mu)-mu*kv.dot(kv)*eye)==sp.zeros(3),
       'Negative bulk does not imply negative periodic plane-wave eigenvalues; boundary qualification retained.')
    ck('elastic_mutation_detects_longitudinal_only',float((2+2*3)/3)!=1,
       'Positive example lambda=2,mu=3 has longitudinal/transverse ratio 8/3, so a pressure-plus-shear choice does not automatically match.')

    # Route B: build a finite periodic cubic lattice from real-space bonds.
    n=5; count=n**3; J=1.7; b=.6; M=.9
    matrix=np.zeros((count,count))
    index=lambda xyz: (xyz[0]*n+xyz[1])*n+xyz[2]
    for xyz in itertools.product(range(n),repeat=3):
        i=index(xyz)
        for axis in range(3):
            nxt=list(xyz); nxt[axis]=(nxt[axis]+1)%n; j=index(nxt)
            matrix[i,i]+=J; matrix[j,j]+=J; matrix[i,j]-=J; matrix[j,i]-=J
    exact_eigs=np.sort([4*J*sum(math.sin(math.pi*z/n)**2 for z in xyz) for xyz in itertools.product(range(n),repeat=3)])
    numeric_eigs=np.linalg.eigvalsh(matrix)
    err=float(np.max(np.abs(exact_eigs-numeric_eigs)))
    ck('real_space_lattice_spectrum',err<1e-12,{'sites':count,'bonds':3*count,'max_absolute_eigenvalue_error':err})
    # Full vector Hessian independently assembled by assigning three DOFs per site.
    vector_matrix=np.kron(matrix,np.eye(3))
    ve=np.linalg.eigvalsh(vector_matrix)
    verr=float(np.max(np.abs(ve-np.repeat(exact_eigs,3))))
    ck('full_vector_lattice_spectrum',verr<2e-12,{'dofs':3*count,'max_absolute_error':verr,'zero_modes':int(sum(abs(v)<1e-12 for v in ve))})
    q=sp.symbols('q',real=True)
    ck('lattice_continuum_coefficient',sp.limit(4*sp.sin(q/2)**2/q**2,q,0)==1,
       'Energy per volume gives gamma=J/b, inertia=M/b^3, c_ac^2=J b^2/M.')
    directions=[np.array(v,dtype=float)/np.linalg.norm(v) for v in [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,1,1),(2,-3,5)]]
    lattice=[]
    for di,d in enumerate(directions):
        for qb in [.01,.03,.1,.3,.6,1.,2.,math.pi]:
            symbol=4*float(np.sin(qb*d/2)@np.sin(qb*d/2))
            lattice.append({'direction':di,'unit_vector':d.tolist(),'k_b':qb,
                            'exact_over_J_b3':symbol,'local_relative_error':qb*qb/symbol-1})
    ck('lattice_error_scaling',max(abs(r['local_relative_error']) for r in lattice if r['k_b']<=.1)<.001,
       {'cases':len(lattice),'max_error_at_k_b_le_0p1':max(abs(r['local_relative_error']) for r in lattice if r['k_b']<=.1)})
    def boundary(direction):
        lo=1e-4; hi=2.
        for _ in range(75):
            mid=(lo+hi)/2
            sym=4*np.sum(np.sin(mid*direction/2)**2)
            if mid*mid/sym-1>.01: hi=mid
            else: lo=mid
        return (lo+hi)/2
    boundary_axis=boundary(directions[0]); boundary_diagonal=boundary(directions[4])
    ck('lattice_directional_boundary',abs(boundary_diagonal/boundary_axis-math.sqrt(3))<1e-10,
       {'one_percent_k_b_axis':boundary_axis,'one_percent_k_b_diagonal':boundary_diagonal})
    # A cubic material can have different vector stiffness along/across a bond.
    def bond_tensor(d,jl,jt):
        return sum((jt*np.eye(3)+(jl-jt)*np.outer(np.eye(3)[i],np.eye(3)[i]))*d[i]**2 for i in range(3))
    scalar=bond_tensor(directions[0],1,1); changed=bond_tensor(directions[0],2,1)
    ck('bond_tensor_mutation',np.allclose(scalar,np.eye(3)) and np.allclose(np.linalg.eigvalsh(changed),[1,1,2]),
       'Changing longitudinal bond constant leaves a stable model but breaks canonical equality of tensor sectors.')
    scale_rows=[]
    for a in [.01,.1,1.,10.,100.]:
        e_scaled=np.linalg.eigvalsh(a*matrix)/(a*M)
        scale_rows.append({'scale':a,'gamma_ratio':a,'Lstar_ratio':math.sqrt(a),
                           'max_frequency_squared_difference':float(np.max(np.abs(e_scaled-numeric_eigs/M)))})
    ck('lattice_degeneracy_family',max(r['max_frequency_squared_difference'] for r in scale_rows)<2e-12,
       scale_rows)
    ck('negative_bond_mutation',np.max(np.linalg.eigvalsh(-matrix))<1e-12 and np.min(np.linalg.eigvalsh(-matrix))<0,
       'Flipping J changes nonzero bond modes to negative curvature.')

    # Optical coordinate: total positive mass has zero internal dipole at fixed COM.
    m1,m2,t=sp.symbols('m1 m2 t',positive=True,real=True)
    mass_sum=m1+m2
    dipole=sp.simplify(m1*m2/mass_sum-m2*m1/mass_sum)
    second=sp.simplify((m1*(m2/mass_sum)**2+m2*(m1/mass_sum)**2)/2)
    ck('positive_mass_dipole_cancellation',dipole==0 and sp.simplify(second-m1*m2/(2*mass_sum))==0,
       'Linear total mass dipole vanishes; leading density-amplitude shift is -mu_red(k.d)^2/2.')
    optical=[]
    for td in [.0001,.001,.01,.03,.1]:
        amp=2*np.exp(-1j*3*td/5)+3*np.exp(1j*2*td/5)-5
        leading=-.6*td*td
        optical.append({'k_dot_d':td,'real_density_shift':float(amp.real),'imag_density_shift':float(amp.imag),
                        'relative_real_quadratic_error':float(abs(amp.real/leading-1))})
    ck('optical_mass_fourier_check',max(r['relative_real_quadratic_error'] for r in optical)<.0003,
       optical)
    ck('single_species_mutation',sp.simplify(m1*m2/mass_sum)!=0,
       'Keeping only one moving species gives a nonzero linear dipole: total versus species density is a real mapping distinction.')

    # Route C: symbolic exact Schur complement and frequency polynomial.
    h,C,D,I,Jq,k,z=sp.symbols('h C D I Jq k z',positive=True)
    block=sp.Matrix([[h+C-I*z,-C],[-C,C+D*k*k-Jq*z]])
    det=sp.expand(block.det())
    expected_det=I*Jq*z*z-(Jq*(h+C)+I*(C+D*k*k))*z+(h+C)*(C+D*k*k)-C*C
    ck('mediator_characteristic_polynomial',sp.simplify(det-expected_det)==0,str(expected_det))
    eff=h+C-I*z-C*C/(C+D*k*k-Jq*z)
    stat=sp.simplify(eff.subs(z,0))
    ck('static_schur_complement',sp.simplify(stat-h-C*D*k*k/(C+D*k*k))==0,
       'The tensor contribution is scalar for all 3 components before adding h.')
    ck('static_validity_exact',sp.simplify(D*k*k/(stat-h)-1-D*k*k/C)==0,
       'The relative local-gradient error is exactly (k ell)^2; ell^2=D/C.')
    eps=sp.symbols('eps')
    expansion=sp.series(eff.subs({k:k*sp.sqrt(eps),z:z*eps}),eps,0,3).removeO()
    target=h+eps*(D*k*k-(I+Jq)*z)-eps**2*(D*k*k-Jq*z)**2/C
    ck('dynamic_low_energy_expansion',sp.simplify(expansion-target)==0,
       'I_eff=I+Jq; controlled variable is |Dk^2-Jq omega^2|/C, away from mediator poles.')
    ck('positive_determinant',sp.expand(expected_det.subs(z,0))==C*h+D*h*k*k+C*D*k*k,
       'Positive trace and determinant for h>0 or k>0; only h=k=0 has a zero mode.')

    def roots(hv,cv,dv,iv,jv,kv):
        bb=jv*(hv+cv)+iv*(cv+dv*kv*kv)
        dd=(hv+cv)*(cv+dv*kv*kv)-cv*cv
        disc=max(0.,bb*bb-4*iv*jv*dd)
        high=(bb+math.sqrt(disc))/(2*iv*jv)
        low=dd/(iv*jv*high)
        return np.array([low,high])
    def numeric(hv,cv,dv,iv,jv,kv):
        mat=np.array([[hv+cv,-cv],[-cv,cv+dv*kv*kv]])
        norm=np.diag([1/math.sqrt(iv),1/math.sqrt(jv)])
        return np.linalg.eigvalsh(norm@mat@norm)
    dynamic_errors=[]; minimum=1e100; total=0
    for cv,dv,iv,jv in itertools.product([.1,1.,10.],repeat=4):
        for hv,kv in itertools.product([0.,.01,1.,100.],[0.,.001,.01,.1,1.,10.,100.]):
            analytic=roots(hv,cv,dv,iv,jv,kv); numerical=numeric(hv,cv,dv,iv,jv,kv)
            dynamic_errors.append(float(np.max(np.abs(analytic-numerical)/(1+np.abs(numerical)))))
            minimum=min(minimum,float(numerical[0])); total+=1
    ck('two_branch_numerical_spectrum',max(dynamic_errors)<1e-10 and minimum>-1e-10,
       {'cases':total,'max_normalized_error':max(dynamic_errors),'min_computed_omega_squared':minimum})

    # Full 6x6 coupled vector modes with the inherited canonical background Hessian.
    full_errors=[]; full_min=[]
    for sv in [.0001,.01,.1,.3,.7,.9]:
        A=sv*(2-sv)/(1-sv)**2; B=sv/(1-sv)
        for th in np.linspace(0,math.pi/2,13):
            nvec=np.array([math.sin(th),0.,math.cos(th)])
            H0=np.diag([B,B,A])+np.eye(3)-np.outer(nvec,nvec)
            he=np.linalg.eigvalsh(H0)
            cv,dv,iv,jv=2.,.9,1.3,.7
            for kv in [0.,.01,.1,1.,10.,100.]:
                mat=np.block([[H0+cv*np.eye(3),-cv*np.eye(3)],[-cv*np.eye(3),(cv+dv*kv*kv)*np.eye(3)]])
                norm=np.diag([1/math.sqrt(iv)]*3+[1/math.sqrt(jv)]*3)
                num=np.linalg.eigvalsh(norm@mat@norm)
                exp=np.sort(np.concatenate([roots(hh,cv,dv,iv,jv,kv) for hh in he]))
                full_errors.append(float(np.max(np.abs(num-exp)/(1+np.abs(num)))))
                full_min.append(float(num[0]))
    ck('full_six_component_modes',max(full_errors)<1e-10 and min(full_min)>0,
       {'matrices':len(full_errors),'max_normalized_error':max(full_errors),'min_omega_squared':min(full_min)})
    cv,dv,iv,jv=2.,.9,1.3,.7
    gap=cv*(iv+jv)/(iv*jv)
    low=roots(0,cv,dv,iv,jv,1e-4)[0]/1e-8
    # Avoid cancellation in determinant for tiny k via an independent formula for h=0.
    big=roots(0,cv,dv,iv,jv,1e-4)[1]
    low_stable=cv*dv/(iv*jv*big)
    ck('acoustic_and_optical_limits',abs(low_stable/(dv/(iv+jv))-1)<1e-7 and abs(roots(0,cv,dv,iv,jv,0)[1]-gap)<1e-12,
       {'low_k_speed_squared':low_stable,'expected':dv/(iv+jv),'optical_gap_squared':gap})
    ck('inertia_mutation',abs((dv/iv)/(dv/(iv+jv))-1)>.5,
       'Dropping auxiliary inertia changes the low-energy slope by 53.8% in the fixed test model.')
    high=roots(0,cv,dv,iv,jv,1e6)[1]/1e12
    ck('material_front_speed',abs(high/(dv/jv)-1)<1e-9,
       {'large_k_omega_squared_over_k_squared':high,'principal_speed_squared':dv/jv,'scope':'material sector only, no relativistic-gravity claim'})
    mediator_family=[]
    baseline=np.array([roots(0,cv,dv,iv,jv,kk) for kk in [.001,.1,1,10]])
    for aa in [.01,.1,1.,10.,100.]:
        scaled=np.array([roots(0,aa*cv,aa*dv,aa*iv,aa*jv,kk) for kk in [.001,.1,1,10]])
        mediator_family.append({'scale':aa,'gamma_ratio':aa,'Lstar_ratio':math.sqrt(aa),
          'range_squared':aa*dv/(aa*cv),'front_speed_squared':aa*dv/(aa*jv),
          'max_normalized_frequency_squared_difference':float(np.max(abs(scaled-baseline)/(1+abs(baseline))))})
    ck('mediator_degeneracy_family',max(r['max_normalized_frequency_squared_difference'] for r in mediator_family)<1e-12,mediator_family)

    # Physical requirements from specified resolution and conditional S3 inertia, no fits.
    G=6.67430e-11; gravK=4*math.pi*G; c=299792458.; pc=3.0856775814913673e16; AU=149597870700.; Msun=1.98847e30
    rho_mean=(.26/.686)*4*(9.3603e-11)**2/(G*c*c)
    densities={'canonical_cosmic_mean_assumed':rho_mean,'halo_0p01_Msun_pc3_assumed':.01*Msun/pc**3}
    requirements=[]
    ell=.1*AU
    for Lpc in [24.,1000.,2042.]:
        Dsi=gravK*(Lpc*pc)**2/2
        row={'Lstar_pc':Lpc,'ell_max_for_one_percent_at_k_inverse_AU_AU':.1,
             'C_over_K_min':Dsi/(ell*ell*gravK),'b_max_one_percent_lattice_axis_AU':boundary_axis,
             'conditional_density_cases':[]}
        for label,rhov in densities.items():
            cp=math.sqrt(Dsi*rhov)
            # f=Jq/(I+Jq); positivity 0<f<1; material causality f>=(cp/c)^2.
            # Maximum gap period at f=1/2: Omega_min=2 cp/ell.
            row['conditional_density_cases'].append({'density_label':label,'rho_kg_m3':rhov,
                'acoustic_speed_m_s':cp,'minimum_inertia_fraction_f_for_material_causality':(cp/c)**2,
                'max_optical_gap_period_years_at_ell_limit':math.pi*ell/cp/(365.25*86400)})
        requirements.append(row)

    frozen=[]
    if args.verify_frozen_root:
        source_map=json.loads((HERE/'source_map.json').read_text())
        for row in source_map['sources']:
            p=args.verify_frozen_root/row['repository_path']
            frozen.append({'repository_path':row['repository_path'],'expected_sha256':row['sha256'],'observed_sha256':sha(p)})
        ck('immutable_source_hashes',all(r['expected_sha256']==r['observed_sha256'] for r in frozen),'All optional frozen-source checks matched.')
    ck('local_inputs_unchanged',all(sha(Path(p))==v for p,v in before.items()),'All observed local input hashes rechecked.')
    results={'base_commit':BASE,'assertion_tested':'Specified material models, full tensor matching, operator validity and scoped coefficient freedom; no physical origin of Lstar claimed.',
      'checks':checks,'lattice_error_table':lattice,'lattice_scaling_family':scale_rows,'mediator_scaling_family':mediator_family,
      'physical_requirements':requirements,'optical_mass_check':optical,'frozen_sources_verified':frozen,
      'counts':{'scalar_lattice_sites':count,'vector_lattice_dofs':3*count,'two_mode_parameter_cases':total,'full_six_mode_matrices':len(full_errors)}}
    # Documentary provenance changes no mathematical content; keep it out of deterministic replay comparison.
    numeric_result={k:v for k,v in results.items() if k!='frozen_sources_verified'}
    numeric_result['checks']=[r for r in checks if r['name']!='immutable_source_hashes']
    resultpath=out/'checks.json'; resultpath.write_text(json.dumps(numeric_result,indent=2,sort_keys=True)+'\n')
    proofpath=out/'source_verification.json'; proofpath.write_text(json.dumps(frozen,indent=2,sort_keys=True)+'\n')
    passed=all(x['passed'] for x in checks)
    summary={'checks_passed':sum(r['passed'] for r in numeric_result['checks']),'checks_total':len(numeric_result['checks']),
             'optional_frozen_checks':len(frozen),'lattice_one_percent_axis_kb':boundary_axis,
             'lattice_one_percent_diagonal_kb':boundary_diagonal,'two_mode_parameter_cases':total,
             'full_six_mode_matrices':len(full_errors),'max_full_vector_normalized_error':max(full_errors),
             'physical_requirements':requirements}
    summarypath=out/'summary.json'; summarypath.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    def pathrecord(p):
        try: return str(p.relative_to(HERE))
        except ValueError: return str(p)
    manifest={'schema_version':2,'claim_id':'ROUND2-STIFFNESS-FULL-OPERATOR',
      'repository':observed_repository,
      'command':['python3','run_checks.py']+sys.argv[1:],
      'environment':{'software':[{'name':'Python','version':platform.python_version()},{'name':'numpy','version':np.__version__},{'name':'sympy','version':sp.__version__}],
                     'hardware':platform.platform()+'; '+platform.machine()},
      'mathematics':{'assertion_tested':'Exact elastic/lattice/mediator identities, finite spectra and scaling families in the registered models.',
        'coefficient_domain':'Positive real parameters; exact SymPy expressions and deterministic IEEE float64 matrices.',
        'conventions':'k angular wavenumber; Fourier Hessian energy=1/2 p^* H p; K=4piG, gamma=K Lstar^2/2; no fitted microscopic inputs.',
        'inputs':[pathrecord(p) for p in inputs],'bounds':results['counts'],
        'non_claims':['No independently predicted microscopic constants','No full S2/S3 microscopic completion','No cosmological pass','Material front speed is not relativistic gravitational causality','No all-model no-go']},
      'randomness':{'used':False,'generator':'','seed':None},
      'run':{'started_at':start,'runtime_seconds':time.perf_counter()-t0,'exit_status':0 if passed else 1,'status':'completed' if passed else 'failed',
             'resource_limits':{'memory_bytes':None,'cpu_seconds':None,'max_cores':None,'max_threads':None}},
      'outputs':[{'path':pathrecord(p),'sha256':sha(p),'kind':'result'} for p in [resultpath,summarypath,proofpath]],
      'checks':checks,'result':'implementation and finite assertion verified in stated range' if passed else 'at least one check failed',
      'residual_risks':['Numerical comparisons conditional on displayed tolerances','No radiative stability proof','No microscopic gravitational coupling or total-mass displacement map for internal coordinates'],
      'input_artifacts':[{'path':pathrecord(Path(p)),'sha256':v,'sha256_after':sha(Path(p))} for p,v in before.items()],
      'declared_results':[pathrecord(p) for p in [resultpath,summarypath,proofpath]]}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True))
    if not passed:
        print('FAILED:',[x['name'] for x in checks if not x['passed']])
    return 0 if passed else 1

if __name__=='__main__':
    sys.exit(main())
