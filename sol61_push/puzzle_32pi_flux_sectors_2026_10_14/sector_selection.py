import sympy as s,json
z,V,M2,B,L1,Om1,delta,q1,q2,mu4=s.symbols('z V M2 B L1 Om1 delta q1 q2 mu4',positive=True)
checks=[]
def ck(name,e):
 assert s.simplify(e)==0,(name,e)
 checks.append(name)
# z=sqrt(Omega); B=sqrt(24 pi^2); same Euler sector in every comparison.
I=V*z**2-2*M2*B*z
ck('continuous_minimum_certificate',I-(V*(z-M2*B/V)**2-M2**2*B**2/V))
ck('continuous_stationary_point',s.diff(I,z).subs(z,M2*B/V))
ck('stationary_curvature', (B/z).subs(z,M2*B/V)-V/M2)
ck('stationary_bare_counterterm',M2*(V/M2)-V)
I1=-2*M2*L1*Om1+V*Om1
I2=-2*M2*(L1/2)*(4*Om1)+V*(4*Om1)
ck('two_sector_action_difference',I2-I1-Om1*(3*V-2*M2*L1))
ck('zero_offset_favors_larger_volume',(I2-I1).subs(V,0)+2*M2*L1*Om1)
ck('shifted_offset_favors_target',(I2-I1).subs(V,M2*L1)-M2*L1*Om1)
ck('ordering_threshold',(I2-I1).subs(V,2*M2*L1/3))
ck('relative_log_weight_shift',-delta*q1/mu4+delta*q2/mu4+delta*(q1-q2)/mu4)
print(json.dumps({'count':len(checks),'checks':checks,'scope':'Formal action comparison with fixed sector weights. Not a derived measure, contour, or prediction of universe nucleation.'},indent=2))
