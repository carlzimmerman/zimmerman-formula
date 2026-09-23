"""Exact regular canonical-density variables for the exponential well.

w = delta(pi_phi)/(a^3*(-F_Q)) = (Pdot-Q*lapse)/epsilon - 3*Phi.
Uses the conserved canonical scalar charge. No adiabatic mode deletion.
"""
from pathlib import Path
import json
import sympy as s

here=Path(__file__).resolve().parent
old=here.parents[1]/'frw_repair/run_verified/general_reduced.json'
d=json.loads(old.read_text())
M,R=[s.sympify(d[x]) for x in ('mass','rest')]
a,h,q,j,ep,xi,k,alpha,alphad=[s.sympify(x) for x in d['vars']]
b=next(x for x in M.free_symbols if str(x)=='clock_c2')
gc=1+3*b/2;hd=q*j/(4*gc)
def Dt(z):
    return a*h*s.diff(z,a)+hd*s.diff(z,h)-3*ep*h*s.diff(z,q)-3*h*j*s.diff(z,j)+alphad*s.diff(z,alpha)
f,fd,u,ud=s.symbols('f fd u ud');oldstate=s.Matrix([f,fd,u,ud])
lapse=s.sympify(d['lapse']);shift=s.sympify(d['shift'])
acc=(-M.inv()*R).applyfunc(s.factor)
A=s.Matrix([[0,1,0,0],list(acc[0,:]),[0,0,0,1],list(acc[1,:])])
charge=(ud-q*lapse)/ep-3*f
T=s.Matrix([f,fd,u,charge]).jacobian(oldstate)
Ti=T.inv().applyfunc(s.factor)
B=((T.applyfunc(Dt)+T*A)*Ti).applyfunc(s.factor)
scale=s.diag(1,h,1,1)
Bn=(scale.inv()*B*scale/h-scale.inv()*scale.applyfunc(Dt)/h).applyfunc(s.factor)
assert all(s.factor(z)==0 for z in B*T-T.applyfunc(Dt)-T*A)
assert all(s.factor(z)==0 for z in T*Ti-s.eye(4))
print('Exact invertible canonical density transformation verified.',flush=True)
print('new matrix operation count',sum(s.count_ops(z) for z in Bn),flush=True)
print('charge evolution coefficients',list(Bn[3,:]),flush=True)

def field_Dt(z):
    return Dt(z)+s.diff(z,f)*fd+s.diff(z,fd)*(acc*oldstate)[0]+s.diff(z,u)*ud+s.diff(z,ud)*(acc*oldstate)[1]
observables=s.Matrix([f,u,lapse,charge,f-h*a*shift,lapse+field_Dt(a*shift),
 q/(q-ep)*((ud-q*lapse)/ep-3*h*a*shift),(-3*(fd+h*lapse)+k*k*shift/a)/h,k*lapse/(a*h)])
obs=(observables.jacobian(oldstate)*Ti*scale).applyfunc(s.factor)
assert all(s.factor(z)==0 for z in obs[4,:]-obs[5,:])
record={'variables':[s.srepr(z) for z in (a,h,q,j,ep,xi,k,alpha,alphad,b)],
        'state':['Phi','dPhi/dlog(a)','P','canonical_charge_contrast'],
        'matrix_N':s.srepr(Bn),'old_cosmic_to_new_cosmic':s.srepr(T),
        'observables':s.srepr(obs),
        'observable_names':['Phi_clock','P_clock','lapse_clock','charge_contrast','Phi_Newtonian','Psi_Newtonian','density_Newtonian','clock_expansion_over_H','clock_acceleration_over_H'],
        'eps_zero_matrix_N':s.srepr(Bn.applyfunc(lambda z:s.factor(s.limit(z,ep,0,dir='+'))))}
(here/'canonical.json').write_text(json.dumps(record,indent=1)+'\n')
print('Regular dust-limit equations written. No stability conclusion from transformation alone.',flush=True)
