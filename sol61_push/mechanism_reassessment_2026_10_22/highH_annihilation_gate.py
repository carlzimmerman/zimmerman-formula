"""Controlled vacuum scattering test of a counterfactual surviving high-H X reservoir."""
import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
s=json.loads((P/'screening_exit_bound_v2_run/results.json').read_text());a0=s['probe']['a'];A0=s['probe']['X_envelope_GeV']
m=.001;M=2*m*np.sqrt(1+.02**2);g=2.168e-6;lam=.00881292;Hinf=1.3445177278709404e10
sv=np.sqrt(1-m*m/M**2)*g**4/(2*np.pi*M**6)
angular=[]
for v in [1e-5,.001,.01,.1,.5]:
    scom=4*M*M/(1-v*v); pi=M*v/np.sqrt(1-v*v);pf=np.sqrt(scom/4-m*m);aa=M*M-scom/2;bb=2*pi*pf;beta=2*pf/np.sqrt(scom)
    numerical=beta/(16*np.pi*scom)*quad(lambda x:(4*g*g/(aa+bb*x))**2,-1,1,epsabs=1e-25,epsrel=1e-12)[0]
    exact=2*beta*g**4/(np.pi*scom*(aa*aa-bb*bb))
    angular.append({'v':v,'sigma_v':numerical,'relative_error':abs(numerical/exact-1),'ratio_to_threshold':numerical/sv})
rows=[]
for A in [.01,.003,.001,.0003]:
    a=a0*(A0/A)**(2/3);H=Hinf/a**2;rho=M*M*A*A;ntot=rho/M;R=ntot*sv/(2*H)
    row=dict(A_GeV=A,a=a,H_GeV=H,gA_over_m2=g*A/(m*m),nX_total_GeV3=ntot,rhoX_GeV4=rho,Gamma_ann_over_H=R,forward_only_X_survival_fraction=1/(1+R),daughter_p_GeV=np.sqrt(M*M-m*m),daughter_initial_v=np.sqrt(1-m*m/M**2),entropy_mappings=[])
    for gst in [106.75,10.75]:
        T=(90/(np.pi**2*gst))**.25*np.sqrt(2.435e18*H);entropy=2*np.pi**2/45*gst*T**3;Yi=ntot/entropy
        row['entropy_mappings'].append(dict(gstar_constant=gst,T_GeV=T,YX_initial=Yi,Yphi_forward_only=Yi*R/(1+R),p_over_m_at_0p8eV_if_instant_release_and_no_scattering=np.sqrt(M*M/m**2-1)*(.8e-9/T)*(3.91/gst)**(1/3)))
    rows.append(row)
checks={'angular_integral_matches_exact':all(x['relative_error']<1e-10 for x in angular),'threshold_limit':abs(angular[0]['ratio_to_threshold']-1)<1e-8,'weak_pump_anchor':rows[2]['gA_over_m2']<.003,'weak_pump_annihilation_faster_than_H':rows[2]['Gamma_ann_over_H']>1e3}
out={'checks':{k:bool(v) for k,v in checks.items()},'all_pass':bool(all(checks.values())),'sigma_v_threshold_GeV_minus2':sv,'angular_checks':angular,'counterfactual_reservoir_anchors':rows,'scope':'Vacuum Born X+antiX -> Phi+antiPhi, nonrelativistic balanced X. Test of extrapolated no-transfer reservoir, not an actual late state. Forward-only depletion omits inverse, stimulated factors, Phi self-energy, coherent correlations, 4-to-2 and expansion-dependent gstar. NOT a surviving yield calculation.'};(O/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
