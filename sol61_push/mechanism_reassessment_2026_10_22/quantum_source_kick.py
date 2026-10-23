"""Exact non-Gaussian potential substep in the source-normal-ordered frame.
For field configurations on a fixed spatial mesh, multiply the wavefunctional
by exp(-i dt * integral residual_potential / lambda). No Fock cutoff is used.
This substep alone is NOT the full quantum field evolution.
"""
import numpy as np

def residual_potential(fields,mean_phi,Cphi,cubic):
 f,h,x,y=fields;Cf,Ch=Cphi
 phi3=mean_phi*(f**3-3*Cf*f+f*(h*h-Ch))
 phi4=.25*(f**4-6*Cf*f*f+3*Cf*Cf+h**4-6*Ch*h*h+3*Ch*Ch+2*(f*f-Cf)*(h*h-Ch))
 interaction=cubic*(x*(f*f-h*h-Cf+Ch)+2*y*f*h)
 return phi3+phi4+interaction

def residual_force(fields,mean_phi,Cphi,cubic):
 f,h,x,y=fields;Cf,Ch=Cphi
 return -np.array([mean_phi*(3*f*f-3*Cf+h*h-Ch)+f**3-3*Cf*f+f*(h*h-Ch)+2*cubic*(x*f+y*h),2*mean_phi*f*h+h**3-3*Ch*h+h*(f*f-Cf)+2*cubic*(-x*h+y*f),cubic*(f*f-h*h-Cf+Ch),2*cubic*f*h])

def phase_kick(fields,dt,cell_volume,mean_phi,Cphi,cubic,effective_hbar=.00881292):
 return np.exp(-1j*dt*cell_volume*np.sum(residual_potential(fields,mean_phi,Cphi,cubic))/effective_hbar)
