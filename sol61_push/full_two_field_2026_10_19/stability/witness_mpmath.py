"""Independent high-precision directional derivative of the discrete ADM constraint.

The float64 saved background and witness direction are fixed input data.  All
stencils, potential coefficients, quadrature, exponential integrating factors,
and analytic derivatives below are evaluated with mpmath, without autodiff or
subtraction of nearby ADM masses.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
import mpmath as mp

p=argparse.ArgumentParser();p.add_argument('--witness',required=True)
p.add_argument('--report',required=True);p.add_argument('--digits',type=int,default=50)
p.add_argument('--result',required=True);a=p.parse_args();start=time.monotonic()
mp.mp.dps=a.digits
d=np.load(a.witness);report=json.loads(Path(a.report).read_text())
r=[mp.mpf(float(x)) for x in d['r']];dx=mp.mpf(report['grid']['dx']);n=len(r)
base=[[mp.mpf(float(x)) for x in row]for row in d['base']]
# Fixed contraction defines the direction, then every functional operation is MP.
direction=d['even_witness'].reshape(4,-1)@d['basis']
delta=[[mp.mpf(float(x))for x in row]for row in direction]
f,x,pf,px=base;df,xx,dpf,dpx=delta
def deriv(y):
    return [(y[1]-y[0])/(2*dx)]+[(y[j+1]-y[j-1])/(2*dx)for j in range(1,n-1)]+[(-y[-1]-y[-2])/(2*dx)]
fr,xr,dfr,dxr=map(deriv,(f,x,df,xx))
m=mp.mpf(report['m']);M=mp.mpf(report['M']);om=mp.mpf(report['omega'])
G=mp.mpf(report['G']);g=mp.mpf(report['g']);lam=mp.mpf(report['lambda_total'])
# Match the executed code's fixed float coefficient values, not a changed pi.
cc=mp.mpf(float(report['g']/np.sqrt(4*np.pi*report['G'])))
LL=mp.mpf(float(report['lambda_total']/(4*np.pi*report['G'])))
S0=[];S1=[];S2=[];A0=[];A1=[];A2=[]
for j in range(n):
    s0=pf[j]**2+px[j]**2+fr[j]**2+xr[j]**2
    s1=2*(pf[j]*dpf[j]+px[j]*dpx[j]+fr[j]*dfr[j]+xr[j]*dxr[j])
    s2=dpf[j]**2+dpx[j]**2+dfr[j]**2+dxr[j]**2
    u0=m*m*f[j]**2+M*M*x[j]**2+2*cc*x[j]*f[j]**2+LL*f[j]**4
    u1=2*m*m*f[j]*df[j]+2*M*M*x[j]*xx[j]+2*cc*(xx[j]*f[j]**2+2*x[j]*f[j]*df[j])+4*LL*f[j]**3*df[j]
    u2=m*m*df[j]**2+M*M*xx[j]**2+2*cc*(x[j]*df[j]**2+2*xx[j]*f[j]*df[j])+6*LL*f[j]**2*df[j]**2
    S0.append(s0);S1.append(s1);S2.append(s2)
    A0.append(s0+u0);A1.append(s1+u1);A2.append(s2+u2)
def cumulative(y,initial):
    out=[initial]
    for j in range(1,n):out.append(out[-1]+dx*(y[j-1]+y[j])/2)
    return out
I0=cumulative([2*r[j]*S0[j]for j in range(n)],S0[0]*r[0]**2)
I1=cumulative([2*r[j]*S1[j]for j in range(n)],S1[0]*r[0]**2)
I2=cumulative([2*r[j]*S2[j]for j in range(n)],S2[0]*r[0]**2)
v0=[];v1=[];v2=[]
for j in range(n):
    w=r[j]**2*mp.exp(I0[j])
    v0.append(w*A0[j]);v1.append(w*(A1[j]+A0[j]*I1[j]))
    v2.append(w*(2*A2[j]+2*A1[j]*I1[j]+A0[j]*(2*I2[j]+I1[j]**2)))
def finaltrap(y,initial):return initial+dx*mp.fsum((y[j-1]+y[j])/2 for j in range(1,n))
J0=finaltrap(v0,A0[0]*r[0]**3/3)
J1=finaltrap(v1,A1[0]*r[0]**3/3)
J2=finaltrap(v2,2*A2[0]*r[0]**3/3)
pref=mp.exp(-I0[-1]);mass=pref*J0
mass1=pref*(J1-I1[-1]*J0)
mass2=pref*(J2-2*I1[-1]*J1+(I1[-1]**2-2*I2[-1])*J0)
charge1=-2*dx*mp.fsum(r[j]**2*(df[j]*pf[j]+f[j]*dpf[j]+2*(xx[j]*px[j]+x[j]*dpx[j]))for j in range(n))
charge2=-4*dx*mp.fsum(r[j]**2*(df[j]*dpf[j]+2*xx[j]*dpx[j])for j in range(n))
grand2=mass2-om*charge2
expected=float(d['even_witness']@d['even_hessian']@d['even_witness'])
out={'status':'completed','digits':a.digits,'N':n,'fixed_input_convention':'saved float64 background and float64 basis-witness contraction; all subsequent analytic directional operations at stated mpmath precision',
 'ADM_mass_G':str(mass),'first_charge_derivative':str(charge1),'first_grand_derivative':str(mass1-om*charge1),
 'second_ADM_derivative':str(mass2),'second_charge_derivative':str(charge2),'second_grand_derivative':str(grand2),
 'saved_autograd_rayleigh':expected,'absolute_curvature_difference':str(abs(grand2-mp.mpf(expected))),
 'relative_curvature_difference':str(abs(grand2-mp.mpf(expected))/abs(grand2)),
 'runtime_seconds':time.monotonic()-start,'non_claims':['Checks the stated discrete directional curvature, not continuum spectral convergence','Does not rely on longdouble precision or nearby-mass cancellation']}
Path(a.result).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
