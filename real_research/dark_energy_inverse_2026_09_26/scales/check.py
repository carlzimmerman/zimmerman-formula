#!/usr/bin/env python3
"""CD26-3 scale inverses. No likelihood or new observational fit.

Positive-domain symbolic identities and exact log-rank calculation; numerical
rows reuse archived project footings and retain their rounded SI constants.
"""
import argparse
import json
import math
from pathlib import Path
import sympy as s


def identities():
    a,k,c,G,rho,g,H,Om,hbar,kB,lam=s.symbols('a kappa c GN rho g Htotal Omega hbar kB lambda',positive=True)
    P=s.pi; checks={}
    def exact(name,expr):
        v=s.simplify(s.powdenest(expr,force=False))
        assert v==0,(name,v)
        checks[name]=str(v)
    eps=rho*c*c; pv=-eps
    aa=k*c*s.sqrt(G*rho)
    ri=a*a/(k*k*c*c*G)
    Hv=s.sqrt(8*P*g*G*rho/3)
    Lgeom=8*P*g*G*rho/(c*c)
    LN=8*P*G*rho/(c*c)
    Z=s.sqrt(8*P*g/3)/k
    lacc=c*c/aa; Rstar=c/s.sqrt(G*rho); RdS=c/Hv
    TdS=hbar*Hv/(2*P*kB); TU=hbar*aa/(2*P*c*kB)
    exact('density_forward_inverse',aa.subs(rho,ri)-a)
    exact('density_inverse_forward',ri.subs(a,aa)-rho)
    exact('energy_form',aa-k*s.sqrt(G*eps))
    exact('energy_inverse',aa*aa/(k*k*G)-eps)
    exact('vacuum_pressure_inverse',-aa*aa/(k*k*G)-pv)
    exact('geometric_Lambda_form',aa-k*c*c*s.sqrt(Lgeom/(8*P*g)))
    exact('geometric_Lambda_inverse',8*P*g*aa*aa/(k*k*c**4)-Lgeom)
    exact('newton_density_Lambda_distinction',Lgeom-g*LN)
    exact('vacuum_Friedmann',Hv*Hv-8*P*g*G*rho/3)
    exact('Z_ratio',c*Hv/aa-Z)
    exact('kappa_from_Z',s.sqrt(8*P*g/3)/Z-k)
    exact('g_from_Z',3*k*k*Z*Z/(8*P)-g)
    exact('Hvac_from_a',Z*aa/c-Hv)
    exact('Htotal_requires_Omega',((c*H*s.sqrt(Om))/Z).subs(Om,Hv*Hv/(H*H))-aa)
    exact('total_vacuum_scale_bias',((c*H/Z)/(c*H*s.sqrt(Om)/Z))-1/s.sqrt(Om))
    exact('deSitter_radius',RdS-s.sqrt(3/Lgeom))
    exact('acceleration_radius_ratio',lacc/RdS-Z)
    exact('density_radius_ratio',Rstar/RdS-s.sqrt(8*P*g/3))
    exact('density_radius_inverse',k*c*c/Rstar-aa)
    exact('deSitter_temperature_inverse',hbar*c/(2*P*kB*TdS)-RdS)
    exact('temperature_ratio',TdS/TU-Z)
    exact('temperature_equality_acceleration',(hbar*a/(2*P*c*kB)-TdS).subs(a,c*Hv))
    ktwo=s.sqrt(8*P*g/3)/(2*P)
    exact('two_pi_proposal', (k*c*s.sqrt(G*rho)).subs(k,ktwo)-c*Hv/(2*P))
    # A nonzero factor remains: the proposal does NOT equate the two temperatures.
    exact('two_pi_proposal_temperature_ratio',(TU/TdS).subs(k,ktwo)-1/(2*P))
    kap_hat=a/(c*s.sqrt(G*rho))
    exact('calibration_round_trip_is_tautology',a*a/(kap_hat**2*G*c*c)-rho)
    exact('unidentified_scaling_a',aa.subs({k:lam*k,rho:rho/lam**2},simultaneous=True)-aa)
    exact('unidentified_scaling_H',Hv.subs({g:lam**2*g,rho:rho/lam**2},simultaneous=True)-Hv)
    exact('apparent_kappa_under_assumed_g_one',aa*s.sqrt(8*P/3)/(c*Hv)-k/s.sqrt(g))
    C,B,Gbare,Lbare=s.symbols('C B Gbare Lambda_bare',positive=True)
    GN=Gbare/C; Gcos=Gbare/(1+3*B/2); rb=Lbare*c*c/(8*P*Gbare)
    exact('same_action_coupling_ratio',Gcos/GN-C/(1+3*B/2))
    exact('same_action_geometric_Lambda',8*P*Gcos*rb/(c*c)-Lbare/(1+3*B/2))
    exact('same_action_Newton_density_Lambda',8*P*GN*rb/(c*c)-Lbare/C)
    # Positive inverse selects the nonnegative acceleration branch.
    exact('signed_acceleration_control',aa.subs(rho,ri.subs(a,-a))-a)
    # A detector temperature law is a stated input, not a derived mechanism.
    adot,Teff=s.symbols('a_detector T_effective',nonnegative=True)
    th=hbar/(2*P*c*kB); aH=c*Hv
    acceltemp=s.sqrt(adot*adot+aH*aH)
    exact('effective_temperature_inverse_squared',acceltemp**2-aH*aH-adot*adot)
    ae=s.symbols('temperature_excess_acceleration',nonnegative=True)
    AH=s.symbols('positive_horizon_acceleration',positive=True)
    rootarg=s.factor(ae*ae+2*AH*ae+AH*AH)
    exact('temperature_excess_inverse',s.sqrt(rootarg)-AH-ae)
    # Logs (kappa,rho,g), c and measured GN fixed. All scale restatements add
    # no rank beyond (a,Hvac). Epsilon would add rank only if independently known.
    J=s.Matrix([[1,s.Rational(1,2),0],[0,s.Rational(1,2),s.Rational(1,2)],
                [0,1,1],[0,-s.Rational(1,2),-s.Rational(1,2)],
                [0,s.Rational(1,2),s.Rational(1,2)],[-1,0,s.Rational(1,2)]])
    assert J.rank()==2 and J.nullspace()==[s.Matrix([s.Rational(1,2),-1,1])]
    assert (J.col_join(s.Matrix([[0,1,0]]))).rank()==3
    # Dimensional matrix for a=kappa c^x GN^y rho^z, axes M,L,T.
    dimensions=s.Matrix([[0,-1,1],[1,3,-3],[-1,-2,0]])
    assert dimensions.det()==-2 and dimensions.inv()*s.Matrix([0,1,-2])==s.Matrix([1,s.Rational(1,2),s.Rational(1,2)])
    return checks,{'inputs':['ln kappa','ln rho','ln g'],'outputs':['ln a','ln Hvac','ln Lambda_geom','ln RdS','ln TdS','ln Z'],
                   'matrix':[[str(v)for v in row]for row in J.tolist()],'rank':J.rank(),
                   'null_direction':[1,-2,2],'rank_with_independent_density_measurement':3,
                   'dimensional_exponent_matrix':[[int(v)for v in row]for row in dimensions.tolist()],
                   'dimensional_determinant':int(dimensions.det())}


def numerical():
    # Archived k01 footings; rounded constants are intentionally retained.
    c=2.998e8; G=6.674e-11; a0=9.3619e-11; kap=.5
    rho=a0*a0/(kap*kap*c*c*G)
    # SI-defined h and k_B; no fitted observational data are introduced.
    hbar=6.62607015e-34/(2*math.pi); kB=1.380649e-23
    rows=[]
    for g in [1,.5/(1+3*.1/2)]:
        hv=math.sqrt(8*math.pi*g*G*rho/3); Z=c*hv/a0
        row={'g':g,'a0':a0,'kappa':kap,'rho_kg_m3':rho,'epsilon_J_m3':rho*c*c,
             'vacuum_pressure_Pa':-rho*c*c,'Hvac_s_inverse':hv,'Lambda_geom_m_inverse2':3*hv*hv/(c*c),
             'Lambda_N_m_inverse2':8*math.pi*G*rho/(c*c),'Zvac':Z,'RdS_m':c/hv,
             'Rstar_m':c/math.sqrt(G*rho),'Racc_m':c*c/a0,
             'TdS_K':hbar*hv/(2*math.pi*kB),'TU_a0_K':hbar*a0/(2*math.pi*c*kB),
             'kappa_if_g_one_assumed':kap/math.sqrt(g)}
        assert abs((row['TdS_K']/row['TU_a0_K'])/Z-1)<1e-14
        rows.append(row)
    # This records existing κ summaries; it does not refit or pool them.
    summaries=[('BTFR_archived',.465,.076),('distance_free_old',.551,.043),('distance_free_later_summary',.55,.17)]
    circular=[]
    for name,kh,sigma in summaries:
        aimplied=kh*c*math.sqrt(G*rho)
        rback=aimplied**2/(kh**2*G*c*c)
        assert abs(rback/rho-1)<1e-14
        circular.append({'name':name,'kappa_summary':kh,'quoted_sigma':sigma,
                         'a_implied_by_definition_not_new_measurement':aimplied,
                         'recovered_rho_is_input':rback})
    Om=.685
    control={'Omega_archive':Om,'Htotal_substitution_acceleration_bias':1/math.sqrt(Om),
             'density_bias_if_total_used_as_vacuum':1/Om,
             'kappa_half':.5,'kappa_2pi_at_g1':math.sqrt(8*math.pi/3)/(2*math.pi),
             'rounding_note':'Canonical a0=9.3619e-11 from k01; k03 H0=67.4 reconstruction yields9.3625e-11. These are archived rounded inputs, not a discrepancy fit.',
             'g_control_scope':'g=10/23 comes from the CD26-2 C=.5,B=.1 action example, which failed its PPN check. It is not an observed cosmological coupling.'}
    return rows,circular,control


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    checks,rank=identities();rows,circular,control=numerical()
    import sys
    out={'runtime':{'python':sys.version,'executable':sys.executable,'sympy':s.__version__},
         'scope':'Conditional scale inverses and identifiability, not a physical origin or new likelihood',
         'exact_checks':checks,'log_jacobian':rank,'numerical_footing_controls':rows,
         'circular_calibration_controls':circular,'controls':control,
         'domains':['c,GN,kappa,g,rho>0 for all reciprocal/log formulas; rho=0 only for the forward law',
                    'Vacuum pressure p=-rho*c^2 requires w=-1; negative vacuum density has no real positive scale in this square-root branch',
                    'Hvac>0 is the expanding branch; squared Friedmann alone also admits contraction',
                    'Teff>=TdS for real nonnegative detector-acceleration inverse'],
         'non_claims':['No derivation of kappa or vacuum zero, no evidence from algebraic round trips',
                       'No Htotal inference without independent vacuum fraction/model',
                       'No numerical likelihood or reanalysis of galaxy data',
                       'No identification of action Lambda with geometric Lambda without coupling normalization']}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'exact_checks':len(checks),'log_rank':rank['rank'],'controls':len(rows),'passed':True}))


if __name__=='__main__':main()
