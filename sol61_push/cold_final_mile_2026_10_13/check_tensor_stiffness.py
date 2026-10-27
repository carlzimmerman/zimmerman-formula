"""CE-FM-012: covariant connection, shift reduction and actual mixed odd tensor branch."""
import json,sys,math
from pathlib import Path
import sympy as s

t,x,y,z=s.symbols('t x y z');coords=(t,x,y,z)
h=s.Function('h')(t,x);ny=s.Function('Ny')(t,x);p=s.Function('p')(t,x)
Ppar,Pper,I,gamma,M2=s.symbols('Ppar Pper I gamma Mpl2',positive=True)
pert=s.zeros(4);pert[0,2]=pert[2,0]=ny;pert[2,3]=pert[3,2]=h
eta=(-1,1,1,1)
def christ(i,a,b):
    return eta[i]*(s.diff(pert[b,i],coords[a])+s.diff(pert[a,i],coords[b])-s.diff(pert[a,b],coords[i]))/2
back=(0,Ppar,0,Pper)
time=[];space=[]
for i in range(1,4):
    time.append((s.diff(p,t) if i==2 else 0)+sum(christ(i,0,j)*back[j] for j in range(1,4)))
    for k in range(1,4):
        space.append((s.diff(p,coords[k]) if i==2 else 0)+sum(christ(i,k,j)*back[j] for j in range(1,4)))
hd,hx,Nx,pd,px,qd,qx=s.symbols('hd hx Nx pd px qd qx',real=True)
replacement={s.diff(h,t):hd,s.diff(h,x):hx,s.diff(ny,x):Nx,s.diff(p,t):pd,s.diff(p,x):px}
T=s.expand(sum(v*v for v in time)).subs(replacement).subs(pd,qd-Pper*hd/2)
D=s.expand(sum(v*v for v in space)).subs(replacement).subs(px,qx-Pper*hx/2)
checks=[]
def check(name,cond,detail):
    checks.append(dict(name=name,passed=bool(cond),detail=detail))
    if not cond:raise AssertionError(name)
check('time derivative from4D connection',s.simplify(T-(qd+Ppar*Nx/2)**2)==0,str(s.factor(T)))
expectedD=qx*qx+(Pper*Pper/4+Ppar*Ppar/2)*hx*hx
check('spatial derivative from3D connection',s.simplify(D-expectedD)==0,str(s.factor(D)))

kin=M2*hd*hd/4+M2*Nx*Nx/4+I*T/2
constraint=s.solve(s.diff(kin,Nx),Nx)[0]
reduced=s.simplify(kin.subs(Nx,constraint))
Ieff=s.factor(s.diff(reduced,qd,2));A=s.diff(reduced,hd,2)
check('shift-reduced field kinetic',s.simplify(Ieff-2*I*M2/(2*M2+I*Ppar*Ppar))==0,str(Ieff))
check('tensor field kinetic decouples',s.simplify(s.diff(reduced,qd,hd))==0,'h-q mixed kinetic zero afterq transform and shift')
spatial=M2*hx*hx/4+gamma*D/2
check('tensor field gradient decouples',s.simplify(s.diff(spatial,qx,hx))==0,'h-q mixed gradient zero')
cT=s.factor(s.diff(spatial,hx,2)/A)
check('mixed tensor principal speed',s.simplify(cT-1-gamma*(Pper*Pper+2*Ppar*Ppar)/(2*M2))==0,str(cT))

G,L,u,rr,mb,a0=s.symbols('G L u r Mb a0',positive=True);K=4*s.pi*G
beta=K*K/a0;B=s.sqrt(G*mb*a0)/K;rM=s.sqrt(G*mb/a0)
ell=gamma/(beta*B)
check('screening length coefficient',s.simplify(2*rM*ell-2*gamma/K)==0,'Lstar^2=2gamma/K')
costheta=s.symbols('costheta',real=True)
mapping={M2:1/(8*s.pi*G),gamma:K*L*L/2,Ppar:u*costheta/K,Pper:u*s.sqrt(1-costheta**2)/K}
delta=s.simplify((cT-1).subs(mapping,simultaneous=True))
check('physical acceleration length mapping',s.simplify(delta-L*L*u*u*(1+costheta**2)/2)==0,str(delta))

root=Path(__file__).resolve().parents[2]
foot=json.loads((root/'real_research/derivation_chain_2026/FP0_core_postulates_results.json').read_text())['numbers']
a0s={'canonical':float(foot['a0_canonical']),'alt':float(foot['a0_rho_total'])}
c=299792458.;pc=3.0856775814913673e16;rows=[]
for footing,acc in a0s.items():
    for Lpc in (5.75,100.,1000.):
        for cosine2 in (0.,.5,1.):
            d=(Lpc*pc*acc/(c*c))**2*(1+cosine2)/2
            relative=d/(math.sqrt(1+d)+1)
            check(f'positive finite branch shift {footing} L={Lpc} cos2={cosine2}',d>0 and0<relative<1e-12,relative)
            rows.append(dict(footing=footing,a0_SI=acc,Lstar_pc=Lpc,cosine_squared=cosine2,
                             upper_bound_delta_speed_squared=d,upper_bound_fractional_cross_speed=relative))
result=dict(checks=checks,shift_constraint=str(constraint),reduced_field_kinetic=str(Ieff),tensor_speed_squared=str(cT),
            normalized_length_shift=str(delta),saturation_speed_bound=rows,
            scope='Odd cross principal block of an explicit independent-P covariant comparison; not all modes or identified inertial-carrier completion.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
