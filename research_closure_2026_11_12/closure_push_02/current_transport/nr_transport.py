#!/usr/bin/env python3
"""Closed leading NR gated clock equations, periodic compatibility background.

This is a finite smooth transport benchmark, not an expanding cosmology or a
halo fit. H=C x^2 exp(-Pi/Pic), x=Q-1, Pi=dP/dx, gamma=0, original QX17 W.
Poisson subtracts the mean source required on a periodic domain; that uniform
compatibility background is prescribed, not a cosmological closure.
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np

C=500.;K=.01;A0=.1;PIC=10.;L=2*np.pi


class Model:
    def __init__(self,N):
        self.N=N;self.x=np.arange(N)*L/N;self.k=np.fft.fftfreq(N,1/N)
        # Even-grid Nyquist derivative is zero for real collocation data.
        self.k[N//2]=0
        self.D=np.fft.ifft(1j*self.k[:,None]*np.fft.fft(np.eye(N),axis=0),axis=0).real
        self.P=np.zeros(N);self.max_residual=0.;self.max_newton=0
        self.max_gate_derivative=0.;self.max_x=0.;self.max_phi=0.;self.max_P=0.

    def constraint(self,n):
        P=self.P.copy()
        for iteration in range(20):
            Pi=self.D@P;h=n-Pi;exp=np.exp(Pi/PIC)
            clock=h*exp/(2*C)
            chemical=clock*(1-h/(2*PIC))
            chemical_Pi=exp/(2*C)*(-1+2*h/PIC-h*h/(2*PIC*PIC))
            denom=1-K*np.abs(P)/A0
            if np.min(denom)<=0:raise RuntimeError('W domain exceeded')
            WP=K*P/denom
            residual=self.D@chemical+WP
            if np.max(np.abs(residual))<2e-13:break
            jacobian=self.D@(chemical_Pi[:,None]*self.D)+np.diag(K/denom**2)
            step=np.linalg.solve(jacobian,-residual)
            scale=1.
            while np.max(np.abs(K*(P+scale*step)/A0))>=.9:scale*=.5
            P+=scale*step
        else:raise RuntimeError('Polarization Newton failed')
        self.P=P;self.max_residual=max(self.max_residual,float(np.max(np.abs(residual))))
        self.max_newton=max(self.max_newton,iteration)
        self.max_x=max(self.max_x,float(np.max(np.abs(clock))))
        self.max_gate_derivative=max(self.max_gate_derivative,float(np.max(np.abs(-clock*h/(2*PIC)))))
        self.max_P=max(self.max_P,float(np.max(np.abs(P))))
        return P,Pi,clock

    def potential(self,n):
        coeff=np.fft.fft(n);out=np.zeros_like(coeff);mask=self.k!=0
        out[mask]=-K*coeff[mask]/self.k[mask]**2
        phi=np.fft.ifft(out).real
        self.max_phi=max(self.max_phi,float(np.max(np.abs(phi))))
        return phi

    def value(self,f,z):
        # Inputs carry negligible Nyquist amplitude in this finite smooth test.
        coeff=np.fft.fft(f)/self.N
        return float(np.real(np.sum(coeff*np.exp(1j*self.k*z))))

    def interval(self,n,left,right):
        coeff=np.fft.fft(n)/self.N;mask=self.k!=0
        return float(np.real(coeff[0]*(right-left)+np.sum(coeff[mask]*(np.exp(1j*self.k[mask]*right)-np.exp(1j*self.k[mask]*left))/(1j*self.k[mask]))))

    def energy(self,n,v):
        P,Pi,clock=self.constraint(n);phi=self.potential(n)
        p=K*np.abs(P)/A0
        W=A0*A0/K*(-p-np.log1p(-p))
        internal=(n-Pi)**2*np.exp(Pi/PIC)/(4*C)
        return float(L*np.mean(.5*n*v*v+internal+W+.5*(n-n.mean())*phi))

    def rhs(self,t,state):
        n,v=np.split(state[:2*self.N],2)
        P,Pi,clock=self.constraint(n);phi=self.potential(n)
        dn=-self.D@(n*v)
        dv=-self.D@(.5*v*v+phi+clock)
        radius=1.2+.08*np.sin(t);speed=.08*np.cos(t)
        left,right=np.pi-radius,np.pi+radius
        # Reynolds transport: dM/dt = [n(v_boundary-v)]_right - same_left.
        flux=self.value(n,right)*speed-self.value(n*v,right)+self.value(n,left)*speed+self.value(n*v,left)
        # Adversarial omission of the boundary speed, integrated alongside.
        wrong=-self.value(n*v,right)+self.value(n*v,left)
        return np.concatenate((dn,dv,[flux,wrong]))


def run(N,dt,mean,output,linear=False):
    start=time.perf_counter();model=Model(N)
    n=mean+.1*np.cos(model.x)+.03*np.cos(2*model.x)
    v=.025*np.sin(model.x)+.01*np.sin(3*model.x)
    clock0=mean/(2*C);aq=2*C;bq=-mean/PIC;dq=C*clock0**2/PIC**2;cq=1+bq
    h_eff=(K-dq)/(aq*K+(cq*cq-aq*dq))-K
    growth=np.sqrt(-mean*h_eff)
    if linear:
        n=mean+1e-5*np.cos(model.x)
        v=-growth*1e-5/mean*np.sin(model.x)
    mass0=float(L*np.mean(n));interval0=model.interval(n,np.pi-1.2,np.pi+1.2)
    state=np.concatenate((n,v,[interval0,interval0]));initial_n=n.copy()
    energy0=model.energy(n,v);steps=round(1/dt);dt=1/steps
    times=[];density=[];velocity=[];mass=[];interval=[];ledger=[];wrong=[];energy=[]
    def record(t):
        nn,vv=np.split(state[:2*N],2);r=1.2+.08*np.sin(t)
        times.append(t);density.append(nn.copy());velocity.append(vv.copy());mass.append(L*nn.mean())
        interval.append(model.interval(nn,np.pi-r,np.pi+r));ledger.append(state[-2]);wrong.append(state[-1]);energy.append(model.energy(nn,vv))
    record(0.)
    for j in range(steps):
        t=j*dt;k1=model.rhs(t,state);k2=model.rhs(t+dt/2,state+dt*k1/2)
        k3=model.rhs(t+dt/2,state+dt*k2/2);k4=model.rhs(t+dt,state+dt*k3)
        state+=dt*(k1+2*k2+2*k3+k4)/6
        if (j+1)%max(1,steps//100)==0:record((j+1)*dt)
    nn,vv=np.split(state[:2*N],2)
    checks={'mass_abs_drift':float(np.max(np.abs(np.array(mass)-mass0))),
            'moving_boundary_reynolds_abs_error':float(np.max(np.abs(np.array(interval)-ledger))),
            'omit_boundary_speed_error':float(np.max(np.abs(np.array(interval)-wrong))),
            'energy_abs_drift':float(np.max(np.abs(np.array(energy)-energy0))),
            'polarization_constraint_max_abs':model.max_residual,
            'max_density_change':float(np.max(np.abs(nn-initial_n))),
            'minimum_density':float(np.min(density)),
            'max_clock_offset':model.max_x,'max_potential':model.max_phi,
            'max_H_Pi_abs':model.max_gate_derivative,'max_polarization_fraction_of_cap':K*model.max_P/A0,
            'max_newton_iterations':model.max_newton,
            'max_nyquist_density_amplitude':float(max(abs(np.fft.fft(z)[N//2])/N for z in density))}
    amplitude=float(2*np.mean((nn-mean)*np.cos(model.x)))
    if linear:
        checks['linear_growing_mode_relative_error']=float(abs(amplitude/(1e-5*np.exp(growth))-1))
    result={'N':N,'dt':dt,'time_final':1.,'mean_initial_charge':mean,'charge_total_initial':mass0,
            'charge_total_final':float(L*nn.mean()),'interval_initial':interval0,'interval_final':interval[-1],
            'constants':{'C':C,'K':K,'a0':A0,'Pi_c':PIC,'gamma':0,'S':'exp(-Pi/Pi_c)'},
            'linear_benchmark':linear,'linear_growth_rate':float(growth),'final_cosine_amplitude':amplitude,
            'checks':checks,'runtime_seconds':time.perf_counter()-start,
            'scope':'Finite periodic leading-NR transport with prescribed uniform Poisson compatibility background; not full cosmology, UV health or an EFE derivation'}
    p=Path(output);p.mkdir(parents=True,exist_ok=True)
    (p/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    np.savez_compressed(p/'trajectory.npz',t=times,x=model.x,n=density,v=velocity,charge=mass,interval=interval,ledger=ledger,wrong_ledger=wrong,energy=energy)
    print(json.dumps(result,indent=2))
    assert checks['mass_abs_drift']<1e-10
    assert checks['moving_boundary_reynolds_abs_error']<1e-8
    assert checks['omit_boundary_speed_error']>1e-3
    assert checks['polarization_constraint_max_abs']<2e-13
    assert checks['max_density_change']>(1e-7 if linear else 1e-3)
    if linear:assert checks['linear_growing_mode_relative_error']<1e-6
    assert checks['minimum_density']>0
    assert checks['max_nyquist_density_amplitude']<1e-9


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--N',type=int,default=32);p.add_argument('--dt',type=float,default=.005)
    p.add_argument('--mean',type=float,default=1.);p.add_argument('--output',required=True)
    p.add_argument('--linear',action='store_true')
    a=p.parse_args();run(a.N,a.dt,a.mean,a.output,a.linear)
