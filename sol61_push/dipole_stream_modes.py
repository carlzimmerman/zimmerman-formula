#!/usr/bin/env python3
"""Longitudinal multistream extension with dipole+gauge+gravity feedback.

Use linear forms of arXiv:2502.14686v2 Eqs 3.15,3.18,3.19. Equal eta=sqrt(3),
three colors and two equal-density opposite streams per color. Omega^2=1.
Finite uniform stream velocity is a declared extension of the near-rest
background. No full covariant kinetic action or nonlinear closure is asserted.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import sympy as s


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    args=ap.parse_args(); checks=[]; rows=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    # (d_t +/- v d_x)^2 xi_as = Omega^2[(sum_bt xi_bt)/6
    #                                              -(sum_t xi_at)/2].
    C=s.ones(6)/6-s.kronecker_product(s.eye(3),s.ones(2)/2)
    color=s.Matrix.hstack(s.Matrix([1,1,1])/s.sqrt(3),s.Matrix([1,-1,0])/s.sqrt(2),s.Matrix([1,1,-2])/s.sqrt(6))
    T=s.kronecker_product(color,s.eye(2))
    expected=s.diag(s.zeros(2),-s.ones(2)/2,-s.ones(2)/2)
    check('orthonormal_color_basis',s.simplify(color.T*color)==s.eye(3),'uniform color direction and two color-orthogonal directions')
    check('gravity_feedback_color_decomposition',s.simplify(T.T*C*T)==expected,'uniform-color longitudinal branch is marginal; two orthogonal branches retain collective plasma forces')
    k,lam=s.symbols('k lambda',real=True)
    velocities=s.diag(1,-1)
    def block(coupling):
        return s.zeros(2).row_join(s.eye(2)).col_join((k*k*s.eye(2)+coupling).row_join(-2*s.I*k*velocities))
    cp0=block(s.zeros(2)).charpoly(lam); lam0=cp0.gen
    cp1=block(-s.ones(2)/2).charpoly(lam); lam1=cp1.gen
    quartic=lam1**4+(2*k*k+1)*lam1**2+k**4-k*k
    check('marginal_gravity_branch',s.expand(cp0.as_expr()-(lam0**2+k*k)**2)==0,'only advective double roots; not an exponential instability or selected equilibrium')
    check('internal_streaming_quartic',s.expand(cp1.as_expr()-quartic)==0,str(quartic))
    check('zero_flow_internal_frequency',s.factor(quartic.subs(k,0))==lam1**2*(lam1**2+1),'relative stream displacement zero mode plus plasma oscillation; gravity channel is distinct')
    CN=np.array(C,dtype=float)
    stream=np.array([1,-1]*3,dtype=float)
    for kk in (.2,math.sqrt(3/8),.9,1.2):
        M=np.block([[np.zeros((6,6)),np.eye(6)],
                    [kk*kk*np.eye(6)+CN,-2j*kk*np.diag(stream)]])
        vals,vecs=np.linalg.eig(M)
        low=kk*kk+.5-.5*math.sqrt(1+8*kk*kk)
        predicted=math.sqrt(-low) if low<0 else 0.
        growth=float(np.max(vals.real))
        # Marginal Jordan roots acquire O(sqrt(machine epsilon)) numerical
        # real parts. Test genuine growth against a 1e-6 discriminator.
        check(f'full_twelve_dimensional_growth_k={kk}',abs(growth-predicted)<1e-6,f'growth={growth:.12g}, scalar prediction={predicted:.12g}')
        unstable=np.flatnonzero(vals.real>1e-6)
        gravity_projections=[float(abs(vecs[:6,j].sum())/np.linalg.norm(vecs[:6,j])) for j in unstable]
        if predicted:
            check(f'unstable_mode_gravity_cancels_k={kk}',len(unstable)==2 and max(gravity_projections)<1e-10,f'two growing color modes; normalized total polarization={gravity_projections}')
        else:
            check('stable_wavelength_in_full_model',len(unstable)==0,'no exponential instability above kv/Omega=1 in the scoped longitudinal extension')
        rows.append(dict(k_v_over_Omega=kk,growth=growth,analytic_growth=predicted,growing_modes=int(len(unstable)),gravity_projection=gravity_projections))
    # All first-order longitudinal fields are gradients. Quadratic cross
    # forcing has exactly zero divergence in a homogeneous medium.
    x,y,z=s.symbols('x y z',real=True)
    coords=(x,y,z)
    phi=s.Function('phi')(x,y,z); psi=s.Function('psi')(x,y,z)
    grad=lambda f:s.Matrix([s.diff(f,u) for u in coords])
    cross=grad(phi).cross(grad(psi))
    divergence=s.simplify(sum(s.diff(cross[i],coords[i]) for i in range(3)))
    check('quadratic_longitudinal_cross_is_divergence_free',divergence==0,'div(grad phi cross grad psi)=0 for smooth scalar fields')
    third=s.Function('third')(x,y,z)
    jacobian=grad(third).dot(cross)
    boundary=s.simplify(sum(s.diff(third*cross[i],coords[i]) for i in range(3)))
    check('static_electric_cubic_is_boundary_term',s.simplify(jacobian-boundary)==0,'grad(third) dot (grad(phi) cross grad(psi)) is a divergence; constant-coefficient purely electrostatic cubic cannot select a bulk state by itself')
    k1=s.Matrix(s.symbols('k1x k1y k1z',real=True)); k2=s.Matrix(s.symbols('k2x k2y k2z',real=True))
    check('independent_fourier_projection',(k1+k2).dot(k1.cross(k2)).expand()==0,'combined wavevector is perpendicular to the quadratic cross source, even for noncollinear waves')
    velocities=s.Matrix(s.symbols('vx vy vz',real=True))
    field=s.Function('f')(x,y,z)
    conv=lambda f:sum(velocities[i]*s.diff(f,coords[i]) for i in range(3))
    check('uniform_transport_commutes_with_gradient',all(s.simplify(conv(s.diff(field,u))-s.diff(conv(field),u))==0 for u in coords),'constant density/frequency/velocity operators preserve the longitudinal/transverse split')
    A=s.Function('A')(x,y,z)
    weighted=s.simplify(sum(s.diff(A*cross[i],coords[i]) for i in range(3)))
    check('inhomogeneity_changes_the_obstruction',s.simplify(weighted-grad(A).dot(cross))==0,'varying density or coupling permits grad(A) dot (grad phi cross grad psi); no claim that it selects the desired state')
    # Constructive counterexample to a GLOBAL no-go: angularly weighted
    # smooth gradients can have nonzero monopole flux. This vector field is
    # not asserted to satisfy the dipole/gauge equations.
    radius,core=s.symbols('r core',positive=True); epsilon,mu=s.symbols('epsilon mu',real=True)
    regularizer=s.sqrt(x*x+y*y+z*z+core*core)
    phi0=x/regularizer; psi0=y/regularizer
    cross0=grad(phi0).cross(grad(psi0))
    dotR=s.simplify(cross0.dot(s.Matrix([x,y,z])))
    check('smooth_angular_witness_radial_component',s.simplify(dotR-z/regularizer**2)==0,'all fields are smooth at the origin for core>0; no monopole singularity in the scalar potentials')
    radial=mu/(radius*radius+core*core)+epsilon*radius*mu**2/(radius*radius+core*core)**s.Rational(3,2)
    average=s.simplify(s.integrate(radial,(mu,-1,1))/2)
    expected_average=epsilon*radius/(3*(radius*radius+core*core)**s.Rational(3,2))
    check('angular_weight_produces_monopole_flux',s.simplify(average-expected_average)==0,'A=1+epsilon*z/sqrt(r^2+core^2), phi=x/sqrt(...), psi=y/sqrt(...)')
    flux=s.simplify(4*s.pi*radius**2*average)
    averaged_divergence=s.simplify(s.diff(radius**2*average,radius)/radius**2)
    check('witness_source_is_Plummer_shaped',s.simplify(averaged_divergence-epsilon*core**2/(radius**2+core**2)**s.Rational(5,2))==0,'angular average of divergence is positive for epsilon>0, though the full source need not be everywhere positive')
    check('radial_weight_alone_has_no_monopole',average.subs(epsilon,0)==0,'a radial coefficient alone cannot give spherical flux to a cross of globally smooth gradients')
    # A weighted gradient generally has curl, so using it as physical
    # polarization exits the PURELY longitudinal/electrostatic sector.
    weight=1+epsilon*z/regularizer
    curl=lambda v:s.Matrix([s.diff(v[2],y)-s.diff(v[1],z),s.diff(v[0],z)-s.diff(v[2],x),s.diff(v[1],x)-s.diff(v[0],y)])
    witness_curl=s.simplify(curl(weight*grad(phi0)).subs({x:0,y:0,z:0}))
    check('witness_exits_electrostatic_sector',witness_curl==s.Matrix([0,epsilon/core**2,0]),f'curl(A grad(phi)) at origin={witness_curl.T}; magnetic/time-dependent completion is required for a physical field dictionary')
    data=dict(checks=checks,rows=rows,linear_coupling_matrix=str(C),
              internal_quartic=str(quartic),marginal_characteristic=str(cp0.as_expr()),witness_flux=str(flux),witness_averaged_divergence=str(averaged_divergence),
              verdict='The longitudinal multistream extension supports a real internal instability, but its growing modes are gravity-neutral at first order; homogeneous quadratic products of longitudinal waves have no gravitational divergence. Conversion into a gravity-active state remains necessary.',
              non_claims=['No full covariant multistream action','No nonlinear saturation calculated for the dipole medium','No transverse/magnetic/inhomogeneous mode analysis','Marginal gravity channel is not a health certificate','No MOND amplitude selection, BTFR normalization or 32pi derivation','Purely longitudinal, equal-charge, constant-density background'])
    Path(args.output).write_text(json.dumps(data,indent=2)+'\n')
    failed=sum(not x['passed'] for x in checks)
    print(f'{len(checks)-failed}/{len(checks)} checks pass; theory and 32pi OPEN.')
    return int(failed>0)


if __name__=='__main__': raise SystemExit(main())
