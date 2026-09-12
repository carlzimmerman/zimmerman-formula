#!/usr/bin/env python3
"""TT principal control for homogeneous aligned FLRW, constant EH M2."""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as S


def main():
    z=S.symbols('z',real=True);a,M2=S.symbols('a M2',positive=True)
    f=S.Function('h')(z)
    # Exact plus-polarized, z-propagating, traceless exponential spatial metric.
    metric=S.diag(a*a*S.exp(f),a*a*S.exp(-f),a*a);inverse=metric.inv()
    def D(expr,i):return S.diff(expr,z) if i==2 else S.S.Zero
    connection=[[[S.simplify(sum(inverse[i,l]*(D(metric[l,k],j)+D(metric[l,j],k)-D(metric[j,k],l))/2 for l in range(3))) for k in range(3)] for j in range(3)] for i in range(3)]
    ricci=S.Matrix(3,3,lambda i,j:sum(D(connection[k][i][j],k)-D(connection[k][i][k],j)+sum(connection[k][i][j]*connection[l][k][l]-connection[l][i][k]*connection[k][j][l] for l in range(3)) for k in range(3)))
    curvature=S.simplify(S.trace(inverse*ricci))
    assert S.simplify(metric.det()-a**6)==0
    assert S.simplify(curvature+S.diff(f,z)**2/(2*a*a))==0
    H,hdot,q,gamma=S.symbols('H hdot q gamma',real=True)
    K=S.diag(H+hdot/2,H-hdot/2,H)
    assert S.trace(K)==3*H
    kinetic=S.expand(M2*a**3*(S.trace(K*K)-S.trace(K)**2)/2)
    assert S.diff(kinetic,hdot,2)==M2*a**3/2
    cubic=-S.Rational(2,3)*gamma*a**3*q**3*S.trace(K)
    assert S.diff(cubic,hdot)==0
    hz=S.symbols('h_z',real=True)
    tensor_L=S.expand(kinetic-kinetic.subs(hdot,0)+M2*a**3*curvature.subs(S.diff(f,z),hz)/2)
    tensor_kinetic=S.simplify(S.diff(tensor_L,hdot,2))
    tensor_gradient=S.simplify(-S.diff(tensor_L,hz,2))
    tensor_coordinate_speed_squared=S.simplify(tensor_gradient/tensor_kinetic)
    tensor_speed_squared=S.simplify(a*a*tensor_coordinate_speed_squared)

    # Minimal Maxwell action, one transverse A_x(t,z) polarization, A_0=0.
    # F is constructed explicitly; indices are raised by the FLRW metric.
    At,Az=S.symbols('A_t A_z',real=True)
    spacetime=S.diag(-1,a*a,a*a,a*a);spacetime_inverse=spacetime.inv()
    F=S.zeros(4);F[0,1]=At;F[1,0]=-At;F[3,1]=Az;F[1,3]=-Az
    Fup=spacetime_inverse*F*spacetime_inverse
    F_squared=S.simplify(sum(F[i,j]*Fup[i,j] for i in range(4) for j in range(4)))
    maxwell_L=S.simplify(-S.sqrt(-spacetime.det())*F_squared/4)
    maxwell_kinetic=S.simplify(S.diff(maxwell_L,At,2))
    maxwell_gradient=S.simplify(-S.diff(maxwell_L,Az,2))
    maxwell_coordinate_speed_squared=S.simplify(maxwell_gradient/maxwell_kinetic)
    maxwell_speed_squared=S.simplify(a*a*maxwell_coordinate_speed_squared)
    checks={
        'unimodular_TT_spatial_metric':S.simplify(metric.det()-a**6)==0,
        'direct_spatial_curvature':S.simplify(curvature+S.diff(f,z)**2/(2*a*a))==0,
        'exact_trace_K':S.simplify(S.trace(K)-3*H)==0,
        'Einstein_TT_kinetic':S.simplify(tensor_kinetic-M2*a**3/2)==0,
        'Einstein_TT_gradient':S.simplify(tensor_gradient-M2*a/2)==0,
        'cubic_no_TT_kinetic':S.diff(cubic,hdot)==0,
        'Maxwell_antisymmetric_F':F+F.T==S.zeros(4),
        'Maxwell_contraction':S.simplify(F_squared-2*(-At**2/a**2+Az**2/a**4))==0,
        'Maxwell_kinetic':S.simplify(maxwell_kinetic-a)==0,
        'Maxwell_gradient':S.simplify(maxwell_gradient-1/a)==0,
        'tensor_and_Maxwell_same_physical_cone':S.simplify(tensor_speed_squared-maxwell_speed_squared)==0,
        'tensor_physical_speed_from_ratio':S.simplify(tensor_speed_squared-1)==0,
        'Maxwell_physical_speed_from_ratio':S.simplify(maxwell_speed_squared-1)==0}
    assert all(checks.values()),checks
    return {'assumptions':['constant positive Einstein coefficient M2','homogeneous aligned chi and tau, Y=0','isotropic FLRW background','constant gamma; cubic is +gamma X Box chi','matter and photons minimally coupled to the same metric','TT principal order; background equations and lower derivative terms handled separately'], 'exact_plus_polarization_R3':str(curvature),'plus_principal_L2':str(tensor_L),'rotationally_completed_TT_principal_action':'M2/8 integral dt d3x a³ [dot h_ij dot h_ij - a^-2 partial_k h_ij partial_k h_ij]','tensor_kinetic_coefficient':str(tensor_kinetic),'tensor_coordinate_gradient_coefficient':str(tensor_gradient),'tensor_coordinate_speed_squared':str(tensor_coordinate_speed_squared),'tensor_speed_squared':str(tensor_speed_squared),'Maxwell_F_squared':str(F_squared),'Maxwell_transverse_L2':str(maxwell_L),'Maxwell_kinetic_coefficient':str(maxwell_kinetic),'Maxwell_coordinate_gradient_coefficient':str(maxwell_gradient),'Maxwell_coordinate_speed_squared':str(maxwell_coordinate_speed_squared),'minimally_coupled_Maxwell_speed_squared':str(maxwell_speed_squared),'speed_convention':'Physical speed squared = a² times coordinate-gradient coefficient / kinetic coefficient; coefficients are obtained by differentiating the derived Lagrangians.','checks':checks,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'non_claims':['No scalar sound-speed equality is implied.','An arrival-time difference also depends on emission-time difference and propagation path.','This calculation does not model gamma-ray emission, detector timing, strong-field wave generation, or non-FLRW propagation.']}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args()
    text=json.dumps(main(),indent=2)+'\n'
    if a.output:a.output.write_text(text)
    else:print(text,end='')
