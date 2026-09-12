#!/usr/bin/env python3
"""Local clock-normal kinematics for lapse N(t,x) and isotropic scale a(t)."""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as S


def main():
    t,x,y,z=S.symbols('t x y z',real=True);coordinates=(t,x,y,z)
    N=S.Function('N',positive=True)(t,x);a=S.Function('a',positive=True)(t)
    g=S.diag(-N*N,a*a,a*a,a*a);gi=g.inv()
    n=S.Matrix([1/N,0,0,0]);nl=g*n
    connection=[[[S.simplify(sum(gi[i,l]*(S.diff(g[l,k],coordinates[j])+S.diff(g[l,j],coordinates[k])-S.diff(g[j,k],coordinates[l]))/2 for l in range(4))) for k in range(4)] for j in range(4)] for i in range(4)]
    theta=S.simplify(sum(S.diff(n[i],coordinates[i])+sum(connection[i][i][j]*n[j] for j in range(4)) for i in range(4)))
    acceleration=S.Matrix([S.simplify(sum(n[j]*(S.diff(nl[i],coordinates[j])-sum(connection[k][j][i]*nl[k] for k in range(4))) for j in range(4))) for i in range(4)])
    volume=N*a**3
    theta_divergence=S.simplify(sum(S.diff(volume*n[i],coordinates[i]) for i in range(4))/volume)
    H=S.diff(a,t)/a
    checks={
        'normal_is_unit_timelike':S.simplify((n.T*g*n)[0]+1)==0,
        'clock_rate_tau_equals_coordinate_t':S.simplify(n[0]-1/N)==0,
        'connection_expansion_equals_volume_divergence':S.simplify(theta-theta_divergence)==0,
        'expansion_equals_3H_over_N':S.simplify(theta-3*H/N)==0,
        'covariant_acceleration_t_zero':acceleration[0]==0,
        'covariant_acceleration_x_log_lapse':S.simplify(acceleration[1]-S.diff(S.log(N),x))==0,
        'covariant_acceleration_y_zero':acceleration[2]==0,
        'covariant_acceleration_z_zero':acceleration[3]==0}
    assert all(checks.values()),checks
    return {'scope':'Exact kinematics of the assumed metric diag(-N(t,x)^2,a(t)^2,a(t)^2,a(t)^2), tau=t, N>0,a>0. No Einstein or scalar field equations imposed.','normal_contravariant':str(n),'clock_rate_s':'1/N','theta':str(theta),'H_definition':str(H),'acceleration_covariant':str(acceleration),'checks':checks,'interpretation':'Along the normal d proper_time=N dt and d tau/d proper_time=1/N. Spatial lapse gradients give acceleration; normalized clock congruences need not be geodesic. Coordinate H=a_t/a differs from proper expansion theta/3 when N!=1.','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args()
    text=json.dumps(main(),indent=2)+'\n'
    if a.output:a.output.write_text(text)
    else:print(text,end='')
