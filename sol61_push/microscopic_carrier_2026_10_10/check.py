"""Contact-interaction identity audit; illustrative inputs, not observational bounds."""
import json, math, pathlib, sys
HBAR=1.054571817e-34
C=299792458.
EV=1.602176634e-19
S=.1  # 1 cm^2/g, inherited benchmark, NOT a newly verified limit
rows=[]
checks=[]
for label,rho,v in [('inherited_cluster',1.30665e-24,1e6),('illustrative_galaxy',1e-21,2e5)]:
    for mev in [.62,.81,1.04]:
        m=mev*EV/C**2
        a=math.sqrt(S*m/(8*math.pi))
        g=4*math.pi*HBAR**2*a/m
        for chi in [1,2]:
            pressure=chi*g*rho**2/(2*m*m)
            cint2=chi*g*rho/(m*m)
            recovered=m**5*cint2**2/(2*math.pi*chi**2*HBAR**4*rho**2)
            # Orthogonal route: infer scattering length directly from pressure.
            a_pressure=pressure*m**3/(2*math.pi*chi*HBAR**2*rho**2)
            recovered2=8*math.pi*a_pressure**2/m
            checks.append({'check':'two independent coupling eliminations','pass':math.isclose(recovered,S,rel_tol=2e-14) and math.isclose(recovered2,S,rel_tol=2e-14)})
            # Pressure derivative checked independently, chi fixed.
            h=rho*1e-3
            derivative=(chi*g*(rho+h)**2/(2*m*m)-chi*g*(rho-h)**2/(2*m*m))/(2*h)
            checks.append({'check':'fixed-chi pressure derivative','pass':math.isclose(derivative,cint2,rel_tol=1e-11)})
            # Deliberately confuse coherent and Gaussian pair factors.
            wrong=recovered*chi**2
            if chi==2:
                checks.append({'check':'pair-factor mutation detected','pass':not math.isclose(wrong,S,rel_tol=.01)})
            m_required=(2*math.pi*chi**2*HBAR**4*rho**2*S/v**4)**.2
            rows.append(dict(case=label,rho_kg_m3=rho,v_m_s=v,mass_eV=mev,chi=chi,
                             scattering_length_m=a,contact_speed_m_s=math.sqrt(cint2),
                             contact_speed_squared_over_v_squared=cint2/v**2,
                             pressure_over_rho_v_squared=pressure/(rho*v*v),
                             de_broglie_wavelength_m=2*math.pi*HBAR/(m*v),
                             diluteness=rho/m*a**3,k_a_using_k_mv_over_hbar=m*v*a/HBAR,
                             mass_for_contact_speed_equal_v_eV=m_required*C*C/EV))
out={'checks':checks,'passed':sum(x['pass'] for x in checks),'count':len(checks),'rows':rows,
     'scope':'Finite floating-point audit, no kinetic evolution and no empirical species identification.'}
pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed':out['passed'],'count':out['count'],'example':rows[1]}))
sys.exit(0 if out['passed']==out['count'] else 1)
