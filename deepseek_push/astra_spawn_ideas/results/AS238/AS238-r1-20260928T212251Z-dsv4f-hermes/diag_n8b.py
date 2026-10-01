#!/usr/bin/env python3
"""Resolve N8 discrepancy: discrete window means of the probe kinematics vs continuum."""
import numpy as np

Twin = 0.3
Ns3 = 41
dtv = Twin/(Ns3-1)
ts_ = (np.arange(Ns3) - Ns3//2)*dtv
q0_ = 0.01
u = (ts_ + Twin/2)/Twin
q = q0_*np.sin(np.pi*u)**2
qd = q0_*(np.pi/Twin)*np.sin(2*np.pi*u)
qdd = -2*q0_*(np.pi/Twin)**2*np.cos(2*np.pi*u)
sub = slice(4, -4)
n = Ns3-8
a_sub = n*dtv/2
print("discrete <qd^2>:", np.mean(qd[sub]**2), " continuum 16.063996*q0^2/1e-4/1e-2^2*... ")
print("discrete <q^2> :", np.mean(q[sub]**2))
print("discrete <qdd q>:", np.mean(qdd[sub]*q[sub]))
print("continuum <qd^2>: 16.063996e-4, <q^2>: 0.454312e-4, <qddq>: 67.513732e-4 (per q0^2=1e-4)")
# NOTE: qd here is the ANALYTIC derivative sampled; the numeric stencil values:
def d4_central(f):
    o = np.zeros_like(f)
    o[2:-2] = (f[4:] - 8*f[3:-1] + 8*f[1:-3] - f[:-4])/(12*dtv)
    return o
qd_num = d4_central(q)
qdd_num = d4_central(qd_num)
print("stencil  <qd^2>:", np.mean(qd_num[sub]**2))
print("stencil  <q^2> :", np.mean(q[sub]**2))
print("stencil  <qdd q>:", np.mean(qdd_num[sub]*q[sub]))
# raw-density mean from pointwise-verified formula:
Mv, a0v, kz = 1.0, 1.3, 1.0
P_d = -3*0.11**2
L2raw_mean = (Mv/2)*a0v**3*(-0.75*np.mean(qd_num[sub]**2) - np.mean(qdd_num[sub]*q[sub])
                           - 0.25*kz**2*np.mean(q[sub]**2)/a0v**2) \
             - 0.25*a0v**3*P_d*np.mean(q[sub]**2)
print("reconstructed L2raw mean:", L2raw_mean)
print("measured from numeric (q0=0.01):", -0.0776398065+0.0797511000)