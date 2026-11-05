#!/usr/bin/env python3
"""Fixed signed Bullet source and physical cubic-Galileon normalization."""
import ast,math
import numpy as np
import audit_inputs as A
G=6.674e-11;MSUN=1.989e30;KPC=3.0857e19;C=299792458.
L0_KPC=1000.;RHO_REF=1e5
A0={'canonical':9.3603e-11,'alt':1.1312e-10}
SOURCE=A.ROOT/'rebuild_2026_10_22/FA1_fresh_action/fa1_zeta.py'

def components():
    selected={}
    for node in ast.parse(SOURCE.read_text()).body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ('GAS','GAL'):
            selected[node.targets[0].id]=ast.literal_eval(node.value)
    if set(selected)!={'GAS','GAL'}:raise ValueError('Missing source assignments')
    return np.array([list(row)+[0.] for name in ('GAS','GAL') for row in selected[name]],float)

def density(x,y,z,rows=None):
    rows=components() if rows is None else np.asarray(rows,float)
    out=np.zeros(np.broadcast_shapes(np.shape(x),np.shape(y),np.shape(z)))
    for mass,radius,cx,cy,cz in rows:
        r2=(np.asarray(x)-cx)**2+(np.asarray(y)-cy)**2+(np.asarray(z)-cz)**2
        out+=3*mass/(4*math.pi*radius**3)*(1+r2/radius**2)**-2.5
    return out

def centroid(rows=None):
    rows=components() if rows is None else np.asarray(rows,float)
    return np.sum(rows[:,0,None]*rows[:,2:],axis=0)/np.sum(rows[:,0])

def spherical_mass(r_kpc,rows=None):
    rows=components() if rows is None else np.asarray(rows,float)
    r=np.asarray(r_kpc,float)
    return sum(m*r**3/(r*r+a*a)**1.5 for m,a,*_ in rows)

def normalization(foot,rho_ref=RHO_REF):
    rho=rho_ref*MSUN/KPC**3;k=C*C/(3*A0[foot]**2)
    epsilon=1/math.sqrt(8*math.pi*G*rho*k)
    acceleration_gradient=math.sqrt(8*math.pi*G*rho/k)
    return dict(epsilon=epsilon,k_s2=k,rho_ref_msun_kpc3=rho_ref,rho_ref_SI=rho,
                pi_per_phi_SI=(L0_KPC*KPC)**2*acceleration_gradient)

def positive_root(r,Q,epsilon):
    r,Q=np.broadcast_arrays(np.asarray(r,float),np.asarray(Q,float))
    if np.any(r<0) or np.any(Q<0) or epsilon<0:raise ValueError('Positive branch requires nonnegative r,Q,epsilon')
    denominator=epsilon*r*r+np.sqrt(epsilon**2*r**4+8*r*Q)
    out=np.zeros_like(r);np.divide(2*Q,denominator,out=out,where=denominator>0)
    return out

def selector(H,mutate=False):
    H=np.asarray(H,float);n2=np.sum(H*H,axis=(-2,-1));det=np.linalg.det(H)
    out=np.zeros_like(n2);np.divide(3*math.sqrt(3)*det,n2**1.5,out=out,where=n2>0)
    return -out if mutate else out
