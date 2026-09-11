#!/usr/bin/env python3
"""A separately labelled matter extension, leaving the gravitational action fixed.

L_b = lambda*(sqrt(Z)-m_b)^(5/2), Z=-grad(theta)^2, sqrt(Z)>m_b>0.
This is an irrotational baryon fluid proxy, not a collisionless stellar disk,
not a dark-particle component, and not yet a coupled clock-gravity solution.
Its static pressure gradient can support a nonzero lapse gradient, unlike dust.
"""
import json
import sympy as s


def derive():
    Z,mb,lam,N,omega,Nr=s.symbols('Z m_b lambda N omega Nr',positive=True)
    power=s.Rational(5,2)
    P=lam*(s.sqrt(Z)-mb)**power
    PX=s.diff(P,Z);rho=2*Z*PX-P;kinetic=PX+2*Z*s.diff(PX,Z)
    speed=s.simplify(PX/kinetic)
    # In static theta=omega*t, Z=omega²/N². This derivative is the matter
    # Ward identity itself, not an imposed hydrostatic prescription.
    pprime=s.diff(P.subs(Z,omega**2/N**2),N)*Nr
    hydro=s.simplify(pprime+(rho+P).subs(Z,omega**2/N**2)*Nr/N)
    enthalpy=s.symbols('h',positive=True)
    branch={Z:(mb+enthalpy)**2}
    p_h=s.simplify(P.subs(branch));rho_h=s.simplify(rho.subs(branch))
    px_h=s.simplify(PX.subs(branch));kin_h=s.simplify(kinetic.subs(branch))
    cs_h=s.simplify(speed.subs(branch))
    checks={
        'hydrostatic_identity_from_action':hydro==0,
        'density':s.simplify(rho_h-lam*enthalpy**s.Rational(3,2)*(s.Rational(3,2)*enthalpy+power*mb))==0,
        'positive_spatial_kinetic':px_h.is_positive is True,
        'positive_temporal_kinetic':kin_h.is_positive is True,
        'sound_speed':s.simplify(cs_h-2*enthalpy/(3*(enthalpy+mb)))==0,
        'subluminal':s.simplify(1-cs_h).is_positive is True,
        'nonrelativistic_density_limit':s.simplify(s.limit(rho_h/enthalpy**s.Rational(3,2),enthalpy,0)-power*lam*mb)==0,
        'nonzero_static_pressure_support':pprime!=0,
    }
    if not all(checks.values()):raise AssertionError(checks)
    return {'checks':checks,'pressure':str(p_h),'density':str(rho_h),
            'temporal_kinetic':str(kin_h),'spatial_kinetic':str(px_h),'sound_speed_squared':str(cs_h),
            'hydrostatic_equation':'p_r = -(rho+p) N_r/N',
            'scope':'local matter action, positive enthalpy; coupled gravitational boundary problem not solved',
            'non_claims':['not a MOND construction','not derived microphysics or fitted baryon data',
                          'vacuum h=0 is degenerate and requires a separate free-boundary treatment',
                          'does not retroactively change any dust evolution result']}

if __name__=='__main__':print(json.dumps(derive(),indent=2))
