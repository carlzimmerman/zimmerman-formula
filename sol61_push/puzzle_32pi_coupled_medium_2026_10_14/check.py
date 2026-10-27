import sympy as s, numpy as np,json
A,b,rho,v=s.symbols('A b rho v',positive=True)
B=b/v
K=s.Matrix([[A-B,A*v],[A*v,rho+A*v*v]])
det=(A-B)*rho-A*B*v*v
assert s.simplify(K.det()-det)==0
assert s.simplify(-v*det/(A*b)-(v*v-rho*v/b+rho/A))==0
disc=(rho/b)**2-4*rho/A
roots=[rho/(2*b)-s.sqrt(disc)/2,rho/(2*b)+s.sqrt(disc)/2]
for root in roots:
    assert s.simplify((v*v-rho*v/b+rho/A).subs(v,root))==0
assert s.simplify(s.limit(v*det,v,0)+b*rho)==0
assert s.simplify(s.limit(det/v,v,s.oo)+A*b)==0
td,ud,px,py,pz,m,cN=s.symbols('td ud px py pz m cN',real=True)
nn=b*v/m
L2=-B*(td-v*px/m)**2/2-nn*(px*px+py*py+pz*pz)/(2*m)+A*(td+v*ud)**2/2+rho*ud*ud/2
assert s.simplify(s.hessian(L2,(td,ud))-K)==s.zeros(2)
assert s.simplify(-s.diff(L2,px,2)-2*b*v/m**2)==0
assert s.simplify(-s.diff(L2,py,2)-b*v/m**2)==0
assert s.simplify(s.diff(L2,td,px)-b/m)==0
rows=[]
for vv in [.02,.1,.5,1.,2.,10.]:
    kk=np.array([[100-1/vv,100*vv],[100*vv,100+100*vv*vv]])
    mineig=float(np.linalg.eigvalsh(kk).min());assert mineig>0
    maxspeed=0.;maximag=0.
    for c in np.linspace(-1,1,101):
        gg=np.diag([vv*(1+c*c),1.]) # b=m=1; rho=100; c_normal=.1
        cc=np.diag([c,0.])
        pencil=np.block([[np.zeros((2,2)),np.eye(2)],[np.linalg.solve(kk,gg),2*np.linalg.solve(kk,cc)]])
        eig=np.linalg.eigvals(pencil)
        maximag=max(maximag,float(abs(eig.imag).max()))
        maxspeed=max(maxspeed,float(abs(eig.real).max()))
    assert maximag<1e-9
    rows.append({'gradient':vv,'minimum_kinetic_eigenvalue':mineig,'max_phase_speed_over_sampled_angles':maxspeed,'max_imaginary_part':maximag})
bad=[]
for vv in [.005,200.]:
    kk=np.array([[100-1/vv,100*vv],[100*vv,100+100*vv*vv]])
    val=float(np.linalg.eigvalsh(kk).min());assert val<0
    bad.append({'gradient':vv,'minimum_kinetic_eigenvalue':val})
print(json.dumps({'exact_checks':10,'parameters':{'A':100,'rho':100,'b':1,'mass':1,'normal_speed':.1},
 'stable_gradient_interval':[float(x.subs({A:100,rho:100,b:1})) for x in roots],
 'angle_count':101,'stable_samples':rows,'ghost_controls':bad,
 'scope':'Explicit nonrelativistic coupled scalar-elastic-medium toy action, constant-gradient backgrounds; phase speeds are not group/front velocities; no microscopic matching'},indent=2))
