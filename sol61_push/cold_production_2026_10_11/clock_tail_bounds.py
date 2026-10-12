"""Evaluate deliberately loose conditional analytical IR and UV bounds."""
import math,json
from pathlib import Path
p=Path(__file__).parent
background=json.loads((p/'autonomous_clock_run/results.json').read_text())['rows'][0]['tight']
energy=json.loads((p/'clock_energy_run/results.json').read_text())
J=10.;delta=.01;T=2.;K=10000.;k0=.001
# Exact energy H=6 implies these pointwise background bounds.
y=math.sqrt(12);yp=y;ypp=4*y;v=math.sqrt(12/J)
w0=1.;w1=1.875/delta;w2=6/delta**2;w3=60/delta**3;w4=360/delta**4
acc=1.5*w1*y*y/J
# Sum of absolute bounds for diagonal entries plus twice the off-diagonal.
u0=3*w0+2*3*y*w1/math.sqrt(J)+1.5*y*y*w2/J
u1=3*w1*v+2*3*(yp*w1+y*w2*v)/math.sqrt(J)+1.5*(2*y*yp*w2+y*y*w3*v)/J
u2=3*(w2*v*v+w1*acc)+2*3*(ypp*w1+2*yp*w2*v+y*(w3*v*v+w2*acc))/math.sqrt(J)+1.5*(2*(yp*yp+y*ypp)*w2+4*y*yp*w3*v+y*y*(w4*v*v+w3*acc))/J
jump=1.5*y*y*w3*v/J
I0=T*u0;I1=T*u1;I2=T*u2+4*jump
U2=T*u0*u0;UU1=T*u0*u1;U3=T*u0**3
C=math.exp(I0/(2*K))*((I2+U2)/8+(I1/4+7*UU1/16)/K+(I0/8+7*U2/16+3*U3/16)/K**2)
uv=C*C*math.sqrt(1+1/K**2)/(2*math.pi**2*K*K)
# IR bound additionally assumes a monotone clock with speed >=.8 on the edges.
min_speed=.8;edge_time=2*delta/min_speed
nu=math.sqrt(1+u0+k0*k0)
Sbound=nu*(1+nu*T)*math.exp(nu*edge_time)
ir=(1+k0*k0)*Sbound*Sbound*k0*k0/(4*math.pi**2)
factor=energy['physical']['M_eV']**4/energy['physical']['source_density_eV4']
checks=[dict(name='numerical background duration supports T<=2',passed=background['duration']<T),dict(name='sampled numerical clock speed supports conditional IR assumption',passed=background['clock_speed_min']>min_speed),dict(name='conditional tail fractions below cold budget',passed=(uv+ir)*factor<1e-7)]
# Audit derivative polynomial constants over a finite grid; inequalities are separately justified in text.
for i in range(1001):
 z=i/1000
 assert abs(30*z*z*(1-z)**2)<=1.875+1e-12
 assert abs(60*z*(1-z)*(1-2*z))<=6
 assert abs(60-360*z+360*z*z)<=60+1e-12
 assert abs(-360+720*z)<=360+1e-12
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,background_bounds=dict(u0=u0,u1=u1,u2=u2,I0=I0,I1=I1,I2=I2,derivative_jump_bound=jump),uv=dict(beta_operator_coefficient=C,dimensionless_energy_bound=uv,fraction_of_source_bound=uv*factor),ir=dict(transfer_operator_bound=Sbound,dimensionless_energy_bound=ir,fraction_of_source_bound=ir*factor),combined_conditional_tail_fraction=(uv+ir)*factor,non_claims=['Tail bounds conditional on stated duration and edge crossing assumptions','Background assumptions numerically supported, not interval certified','No nonlinear or primordial fluctuation bound'])
(p/'clock_tail_bounds_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
