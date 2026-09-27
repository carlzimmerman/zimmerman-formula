#!/usr/bin/env python3
"""CD26-3: exact gate/clock inverses and bounded stored-output controls.

No historical simulation module is imported or executed. Source tables are
read as data, preserving each background and footing separately.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    checks = {}

    def exact(name, value):
        residual = s.factor(s.simplify(value))
        assert residual == 0, (name, residual)
        checks[name] = {'passed': True, 'exact_residual': str(residual)}

    def bounded(name, value, condition):
        assert bool(condition), (name, value)
        checks[name] = {'passed': True, 'measured': value}

    G, M, a0, H, re, B, D, vf, fv, xc, E, dv = s.symbols(
        'G M a0 H re B D vf fv xc E dv', positive=True)
    p = s.symbols('p', real=True)
    edge = vf/(H*s.sqrt(D+B))
    exact('edge_inverse_with_mean_density',
          (vf**2/(H**2*re**2)-B).subs(re, edge)-D)
    exact('gate_forward_inverse', (xc*fv**(-p))*fv**p-xc)
    exact('vacuum_fraction_is_density_ratio_over_H_squared',
          s.expand_log(s.log(dv/E**2), force=True)-s.log(dv)+2*s.log(E))
    exact('log_gate_density_history',
          s.expand_log(s.log(xc)-p*s.log(dv/E**2), force=True)
          -(s.log(xc)+2*p*s.log(E)-p*s.log(dv)))
    b, l1, l2, y1, y2, w1, w2 = s.symbols('b l1 l2 y1 y2 w1 w2', real=True)
    jj = s.Matrix([[1, -l1], [1, -l2]])
    exact('two_epoch_log_Jacobian', jj.det()-(l1-l2))
    exact('two_epoch_p_inverse', ((y2-y1)/(l1-l2)).subs(
        {y1:b-p*l1, y2:b-p*l2})-p)
    exact('two_epoch_Fisher_determinant',
          (jj.T*s.diag(w1,w2)*jj).det()-w1*w2*(l1-l2)**2)
    pp, ll = s.symbols('pprime log_fraction', nonzero=True, real=True)
    exact('unknown_history_exponent_degeneracy', p*ll-pp*(p*ll/pp))
    exact('reference_epoch_cannot_measure_exponent', s.diff(b-p*ll,p).subs(ll,0))
    exact('zero_exponent_cannot_measure_history', s.diff(b-p*ll,ll).subs(p,0))

    # Log-coordinate derivatives preserve the independence assumptions explicitly.
    lm, la, lh, lr, bb = s.symbols('logM loga0 logH logr B', real=True)
    SS = s.sqrt(G)*s.exp(lm/2+la/2-2*lh-2*lr)
    dd = SS-bb
    for var, coefficient in [(lm,s.Rational(1,2)), (la,s.Rational(1,2)),
                             (lh,-2), (lr,-2)]:
        exact('inverse_nuisance_'+str(var), s.diff(s.log(dd),var)-coefficient*SS/dd)
    exact('inverse_nuisance_mean_density', s.diff(s.log(dd),bb)+1/dd)
    logr = lm/4+la/4-lh-s.log(s.exp(b-p*ll)+bb)/2+s.log(G)/4
    for var, predicted in [(lm,s.Rational(1,4)),(la,s.Rational(1,4)),(lh,-1),
                           (b,-s.exp(b-p*ll)/(2*(s.exp(b-p*ll)+bb))),
                           (p,ll*s.exp(b-p*ll)/(2*(s.exp(b-p*ll)+bb))),
                           (ll,p*s.exp(b-p*ll)/(2*(s.exp(b-p*ll)+bb))),
                           (bb,-1/(2*(s.exp(b-p*ll)+bb)))]:
        exact('forward_nuisance_'+str(var),s.diff(logr,var)-predicted)
    exact('edge_mass_acceleration_product_degeneracy',s.diff(logr,lm)-s.diff(logr,la))
    exact('flagship_edge_argument',
          (G*M/(a0*re**2)).subs(re,(G*M*a0)**s.Rational(1,4)/(H*s.sqrt(D+B)))
          -H**2*s.sqrt(G*M)*(D+B)/a0**s.Rational(3,2))
    ys = s.symbols('ystar',positive=True)
    masscap = (ys*a0**s.Rational(3,2)/(H**2*(D+B)))**2/G
    exact('flagship_mass_cap',
          (H**2*s.sqrt(G*M)*(D+B)/a0**s.Rational(3,2)).subs(M,masscap)-ys)
    rr=s.symbols('radius',positive=True)
    exact('general_spherical_profile_recovers_deep_edge_variable',
          s.diff(rr**2*(vf**2/rr),rr)/(H**2*rr**2)-B-(vf**2/(H**2*rr**2)-B))

    # Vacuum shift is invisible to fixed-metric matter equations, not gravity.
    R, Om, Rd, C, m2, lam = s.symbols('R Omega Rdot C m2 lambda', real=True)
    Vdyn = m2*R**2/2+lam*R**4/4
    K=(Rd**2+R**2*Om**2)/2
    rho, pressure = K+Vdyn+C, K-Vdyn-C
    exact('constant_shift_radial_equation',s.diff(Vdyn+C,R)-s.diff(Vdyn,R))
    exact('constant_shift_radial_gap',s.diff(Vdyn+C,R,2)-s.diff(Vdyn,R,2))
    exact('constant_shift_density',s.diff(rho,C)-1)
    exact('constant_shift_pressure',s.diff(pressure,C)+1)
    exact('rho_plus_P_is_kinetic_twice',rho+pressure-2*K)
    exact('rho_minus_P_is_total_potential_twice',rho-pressure-2*(Vdyn+C))
    u,q,r=s.symbols('mu2 Omega2 R2',positive=True)
    gap=u+4*q; sound=u/gap; disp=16*q*q/gap**3
    ss,dd4,W,P=s.symbols('cs2 d4 enthalpy P',real=True)
    inverse_gap=(1-ss)**2/dd4
    inverse_q=(1-ss)**3/(4*dd4)
    inverse_u=ss*(1-ss)**2/dd4
    inverse_r=4*dd4*W/(1-ss)**3
    replace={ss:sound,dd4:disp,W:r*q}
    exact('dispersion_inverse_gap',inverse_gap.subs(replace)-gap)
    exact('dispersion_inverse_rotation_rate',inverse_q.subs(replace)-q)
    exact('dispersion_inverse_radial_stiffness',inverse_u.subs(replace)-u)
    exact('enthalpy_and_dispersion_inverse_amplitude',inverse_r.subs(replace)-r)
    exact('inverse_charge_magnitude_squared',
          (4*W**2*dd4/(1-ss)**3).subs(replace)-r*r*q)
    exact('dispersion_gap_consistency',disp*gap-(1-sound)**2)
    exact('dispersion_constant_shift_invisible',s.diff(sound,C)+s.diff(disp,C))
    # Quartic potential is an extra model assumption, essential to the C inverse.
    pressure_quartic=u*r/8-C
    inverse_m2=(1-ss)**2*(1-3*ss)/(4*dd4)
    inverse_lambda=ss*(1-ss)**5/(8*dd4**2*W)
    inverse_C=-P+ss*W/(2*(1-ss))
    exact('quartic_inverse_bare_mass_squared',inverse_m2.subs(replace)-(q-u/2))
    exact('quartic_inverse_lambda',inverse_lambda.subs(replace)-u/(2*r))
    exact('quartic_inverse_vacuum_constant',
          inverse_C.subs(replace).subs(P,pressure_quartic)-C)
    modelmap=s.Matrix([sound,disp,r*q,pressure_quartic])
    determinant=s.factor(modelmap.jacobian([u,q,r,C]).det())
    exact('quartic_inverse_full_rank_Jacobian',determinant-64*q**3/(u+4*q)**5)
    exact('massless_quartic_vacuum_stress_inverse',
          (-P+ss*W/(2*(1-ss))).subs(ss,s.Rational(1,3))-(W-4*P)/4)
    rx, amp = s.symbols('rx amp',real=True)
    tmax=-rx*amp+s.sqrt(rx**2*amp**2+s.Rational(6,5)-amp**2)
    exact('DE3_transfer_bound_positive_root',tmax**2+2*rx*tmax*amp+amp**2-s.Rational(6,5))

    # Arbitrary synthetic vacuum-density history: no LCDM background imposed.
    hist=np.array([1.,.72,.21,.08]); HH=np.array([1.,1.3,2.1,3.2])
    MM=np.array([1.,4.,.8,2.]); aa=np.array([1.,.7,1.4,1.1])
    BB=np.array([.4,.8,1.2,1.4]); xp=2.5; ppn=1.0
    DD=xp*hist**(-ppn); vv=(MM*aa)**.25
    radii=vv/(HH*np.sqrt(DD+BB))
    inferred=vv**2/(HH**2*radii**2)-BB
    recovered_p=math.log(inferred[3]/inferred[1])/math.log(hist[1]/hist[3])
    recovered_xc=inferred[1]*hist[1]**recovered_p
    bounded('synthetic_non_LCDM_edge_inverse',
            {'p':recovered_p,'xc':recovered_xc,'max_threshold_error':float(np.max(abs(inferred-DD)))},
            abs(recovered_p-ppn)<1e-12 and abs(recovered_xc-xp)<1e-12)
    inferred_density_ratio=HH**2*(xp/inferred)**(1/ppn)
    bounded('synthetic_vacuum_density_reconstruction',inferred_density_ratio.tolist(),
            np.max(abs(inferred_density_ratio-HH**2*hist))<1e-12)
    omitted=vv**2/(HH**2*radii**2)
    biased_p=math.log(omitted[3]/omitted[1])/math.log(hist[1]/hist[3])
    bounded('negative_control_omitted_mean_density_biases_p',biased_p,abs(biased_p-ppn)>.05)
    alternate_p=2.0; alternate_hist=hist**(ppn/alternate_p)
    bounded('negative_control_different_history_same_edges',alternate_hist.tolist(),
            np.max(abs(xp*alternate_hist**(-alternate_p)-DD))<1e-12 and np.max(abs(alternate_hist-hist))>.1)
    rank_same=int(np.linalg.matrix_rank(np.array([[1.,-.2],[1.,-.2]])))
    bounded('negative_control_same_fraction_epoch_rank_one',rank_same,rank_same==1)
    mass_rescale=7.; same_v=(MM*mass_rescale*aa/mass_rescale)**.25
    bounded('negative_control_mass_a0_rescale_same_edges',float(np.max(abs(same_v-vv))),np.max(abs(same_v-vv))<1e-12)

    root=Path(__file__).resolve().parents[3]
    de1=json.loads((root/'real_research/dark_energy_2026/DE1_vacuum_gate_flagship_results.json').read_text())['numbers']
    de2=json.loads((root/'real_research/dark_energy_2026/DE2_vacuum_gate_joint_window_results.json').read_text())['numbers']
    de3=json.loads((root/'real_research/dark_energy_2026/DE3_tmax_at_linear_gate_results.json').read_text())['numbers']
    cell=de3['cell']; prediction=cell['x_c0']*cell['E2_mock']**cell['p']
    bounded('DE3_current_cell_threshold',prediction,abs(prediction-cell['x_lens'])<1e-14)
    historical_background=.3138*1.5**3+.6862
    bounded('DE3_L359_threshold_separately',2.5*historical_background,
            abs(2.5*historical_background-cell['x_lens_L359_background'])<1e-14)
    background_difference=abs(historical_background/cell['E2_mock']-1)
    bounded('negative_control_mock_backgrounds_are_distinct',background_difference,background_difference>3e-5)
    current=next(v for v in de2['L359_cells'] if v['p']==1 and v['x0']==2.5)
    expected=[2.5*(.3138*1.25**3+.6862),prediction,2.5*(.3138*3.5**3+.6862)]
    bounded('DE2_current_cell_three_preserved_backgrounds',current,
            np.max(abs(np.array(current['x_eff'])-expected))<1e-12)

    # L352 constants are translated exactly; its H convention is not silently
    # replaced by DE1's OM47 gate background. These are stored-profile controls.
    gn=6.67430e-11; mpc=3.0856775814913673e22; h=.6736; cn=2.99792458e8
    hzero=100*h*1e3/mpc; ommatter=(.02237+.1200)/h**2
    rhoc=3*hzero*hzero/(8*math.pi*gn)
    og=(4*5.670374419e-8*2.7255**4/cn**3)/rhoc
    orad=og*(1+3.046*(7/8)*(4/11)**(4/3)); ol=1-ommatter-orad
    mass=1e11*1.98892e30; stored_rows=[]; maxima={}; pmax_rows=[]
    for footing,a0n in [('canonical',9.3619e-11),('alt',1.1279e-10)]:
        errors=[]
        for row in de1['E1']['1.0/2.5/'+footing+'/11.0']:
            z=row['z']; hz2=hzero*hzero*(ommatter*(1+z)**3+ol)
            back=1.5*ommatter*(1+z)**3*hzero*hzero/hz2
            desired=2.5*(.3138*(1+z)**3+.6862)
            found=math.sqrt(gn*mass*a0n)/(hz2*(row['re_kpc']*mpc/1e3)**2)-back
            relative=found/desired-1;errors.append(abs(relative))
            stored_rows.append({'footing':footing,'z':z,'stored_edge_kpc':row['re_kpc'],
                                'deep_inverse_threshold':found,'prescribed_threshold':desired,
                                'relative_deep_inverse_error':relative,'fractional_bias_if_background_omitted':back/desired})
        maxima[footing]=max(errors)
        z=2.5; hz2=hzero*hzero*(ommatter*(1+z)**3+ol)
        back=1.5*ommatter*(1+z)**3*hzero*hzero/hz2
        dmax=.1*a0n**1.5/(hz2*math.sqrt(gn*mass))-back
        pmax_rows.append({'footing':footing,'xc0':2.5,'corrected_deep_pmax':math.log(dmax/2.5)/math.log(.3138*3.5**3+.6862),
                          'no_background_pmax':math.log((dmax+back)/2.5)/math.log(.3138*3.5**3+.6862)})
    bounded('DE1_deep_inverse_matches_stored_finite_y_edges_within_one_percent',maxima,max(maxima.values())<.01)

    # Fixed canonical quartic model: changing C changes stress but no local modes.
    un,qn,rn=.8,1.6,2.25
    sn=un/(un+4*qn);dn=16*qn**2/(un+4*qn)**3;wn=rn*qn
    clock_examples=[]
    for cc in [0.,3.,10.]:
        pn=un*rn/8-cc; en=wn-pn
        recovered_c=-pn+sn*wn/(2*(1-sn))
        clock_examples.append({'C':cc,'rho':en,'P':pn,'rho_plus_P':wn,'cs2':sn,'d4':dn,'recovered_C_if_quartic_fixed':recovered_c})
        bounded('quartic_clock_vacuum_inverse_C_'+str(cc),recovered_c,abs(recovered_c-cc)<1e-12)
    bounded('negative_control_dispersion_cannot_identify_vacuum',clock_examples,
            clock_examples[0]['cs2']==clock_examples[-1]['cs2'] and clock_examples[0]['d4']==clock_examples[-1]['d4']
            and clock_examples[0]['rho']!=clock_examples[-1]['rho'])

    output={'claim_id':'CD26_3_GATE_CLOCK_INVERSES','number_of_checks':len(checks),'checks':checks,
            'clock_inverse_Jacobian':str(determinant),'DE1_stored_profile_controls':stored_rows,
            'DE1_background_corrected_flagship_bounds':pmax_rows,
            'synthetic_gate':{'fraction_history':hist.tolist(),'H_over_H0':HH.tolist(),
                              'vacuum_density_ratio':(HH**2*hist).tolist(),'edge_dimensionless':radii.tolist()},
            'scope':['Exact conditional algebra, not a derivation of the vacuum gate',
                     'Stored DE tables read only; no mock or N-body run and no new data fit',
                     'Deep spherical step-gate edges; finite-y stored-profile comparison is bounded',
                     'Clock inverse requires circular canonical polar action and separated clock stress',
                     'Quartic C inference assumes specified potential normalization; dispersion alone cannot infer C',
                     'No closure of common-action MOND, full coupled evolution, or cosmic abundance']}
    target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'number_of_checks':len(checks),'all_passed':True,'stored_edge_relative_errors':maxima,
                      'flagship_bounds':pmax_rows,'clock_inverse_Jacobian':str(determinant)},indent=2))


if __name__=='__main__':
    main()
