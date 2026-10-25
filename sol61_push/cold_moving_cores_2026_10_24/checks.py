import numpy as np,json
from tracking import Potential
from angular_half import Angular
rng=np.random.default_rng(1010);r=np.geomspace(.01,30,300);w=np.gradient(r);a=Angular(4,4,r,w);co=rng.normal(size=(len(r),len(a.density.lm)))+1j*rng.normal(size=(len(r),len(a.density.lm)))
# Use a physically real potential constructed from an actual field.
v=rng.normal(size=(len(r),len(a.field.lm)))+1j*rng.normal(size=(len(r),len(a.field.lm)));v*=np.exp(-r[:,None]);v/=np.linalg.norm(v);_,co,_=a.potential(v);p=Potential(r,co,a.density.lm);x=rng.normal(size=(100,3));h=1e-6;fd=np.column_stack([(p.evaluate(x+np.eye(3)[k]*h)-p.evaluate(x-np.eye(3)[k]*h))/(2*h) for k in range(3)]);grad=p.evaluate(x,True);err=np.max(abs(grad-fd));assert err<1e-7
out=p.evaluate(np.array([[40.,2.,3.]]),True);ex=p.mass*np.array([[40.,2.,3.]])/np.linalg.norm([40.,2.,3.])**3;assert np.max(abs(out-ex))<1e-15
print(json.dumps(dict(full_multipole_gradient_max_absolute_error=err,outer_point_mass_error=float(np.max(abs(out-ex)))),indent=2))
