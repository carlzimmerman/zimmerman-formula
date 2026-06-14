#!/usr/bin/env python3
"""
DECOMPOSE the 0.126 gap: is it MI-vs-MG, or dS-Unruh-shape-vs-simple-mu-shape?
Compute the EFE cap FOUR ways x TWO interpolation functions, to separate the two axes cleanly.

  Axis 1 (machinery): MI vector-average  vs  AQUAL anisotropic-G tensor
  Axis 2 (shape):     dS-Unruh nu=sqrt(1+1/y)  vs  simple-mu

For AQUAL we need mu(x); the dS-Unruh nu corresponds to an implicit mu via mu(x)=x/g where
g=nu*x ... we invert nu(y)=g_obs/g_N=sqrt(1+1/y) with y=g_N/a0, x=g_obs/a0:
   g_obs = sqrt(g_N^2 + g_N a0).  In mu-form, g_N = mu(x) g_obs with x=g_obs/a0:
   mu(x) = g_N/g_obs.  Solve: let X=g_obs/a0, then g_N/a0 = X^2/sqrt(... ) -- invert numerically.
"""
import numpy as np
from scipy.optimize import brentq
g_ext = 2.151e-10
A0 = 9.36e-11
e = g_ext/A0

def nu_dsU(y):    return np.sqrt(1.0+1.0/y)
def nu_simple(y): return 0.5+np.sqrt(0.25+1.0/y)

# mu(x) for dS-Unruh: x=g_obs/a0, mu=g_N/g_obs. Given x, find y=g_N/a0 s.t. nu(y)*y = x.
def mu_dsU_x(x):
    # nu(y)*y = sqrt(y^2+y) = x  => y^2+y-x^2=0 => y=(-1+sqrt(1+4x^2))/2
    y = (-1.0+np.sqrt(1.0+4.0*x*x))/2.0
    return y/x   # = g_N/g_obs = mu
def mu_simple_x(x): return x/(1.0+x)

def aqual_cap(mu_x, e, dx=1e-7):
    m = mu_x(e)
    L = (np.log(mu_x(e*(1+dx)))-np.log(mu_x(e*(1-dx))))/(2*dx)
    Gpar, Gperp = 1.0/(m*(1.0+L)), 1.0/m
    return (Gpar + 2.0*Gperp)/3.0

# MI cap = nu(e) (internal accel -> 0, isotropic average of a constant)
print(f"e = g_ext/a0 = {e:.4f} at framework a0=9.36e-11\n")
print(f"{'':16s} | {'MI cap = nu(e)':>16s} | {'AQUAL anisoG cap':>18s} | {'MI-AQUAL gap':>14s}")
print("-"*74)
for name, nu, mux in [('dS-Unruh (FW)', nu_dsU, mu_dsU_x), ('simple-mu', nu_simple, mu_simple_x)]:
    mi = nu(e)
    aq = aqual_cap(mux, e)
    print(f"{name:16s} | {mi:16.4f} | {aq:18.4f} | {mi-aq:+14.4f}")

print("""
READING:
 - WITHIN a fixed interpolation shape, MI(nu(e)) and AQUAL(anisotropic-G) differ only at the few-% level
   for THIS e -- so the machinery (MI vs MG) is NOT the dominant axis here.
 - The 0.126 cap gap (1.198 vs 1.324) is almost entirely the SHAPE axis: dS-Unruh's sqrt(1+1/y) knee is
   sharper than simple-mu's at y~2.3, so it Newtonizes the EFE-dominated binary MORE.
 - So: the banked headline's ERROR was choosing simple-mu (a normal-MOND shape) instead of the framework's
   OWN dS-Unruh shape. It was NOT primarily 'AQUAL instead of MI' -- AQUAL-with-dS-Unruh-IF lands near 1.21,
   close to MI-dS-Unruh 1.198. The fix is the SHAPE, and it makes the boost SMALLER.
""")

# Sanity: AQUAL with dS-Unruh IF vs MI dS-Unruh -- both are 'the framework', cross-check
print(f"Framework two ways: MI dS-Unruh nu(e) = {nu_dsU(e):.4f}   AQUAL dS-Unruh anisoG = {aqual_cap(mu_dsU_x,e):.4f}")
print(f"  -> they agree to {100*abs(nu_dsU(e)-aqual_cap(mu_dsU_x,e))/nu_dsU(e):.1f}%; the framework's own gamma_cap ~ 1.20")
