"""argon_clues: what a cold-energy -> baryon channel is allowed / would need. All inputs from the record (CFG779 FRB census, R0) plus unit conversions."""
import math
G=6.6743e-11; c=2.99792458e8; Msun=1.98847e30; yr=3.15576e7; Gyr=1e9*yr
mp=1.67262192e-27; eV=1.602176634e-19; keV=1e3*eV
R0=5.364; Bmid, Blo, Bhi = 1.064, 1.010, 1.122
print('R0 = Omega_c/Omega_b (CMB) = %.3f'%R0)
print('\n1. CENSUS BOUND (CFG779: FRBs see B = %.3f [%.3f, %.3f] of the Big-Bang baryon density today)'%(Bmid,Blo,Bhi))
for B in (Bmid,Bhi):
    dOb=B-1.0                      # created baryons, in units of Omega_b(BBN)
    frac_c=dOb/R0                  # fraction of the cold energy that was converted
    Rnew=(R0-dOb)/(1+dOb)
    print('   B = %.3f: created baryons = %.1f%% of Omega_b = %.2f%% of the cold energy; R today = %.3f (from %.3f)'%(B,100*dOb,100*frac_c,Rnew,R0))
frac=(Bhi-1)/R0; t_since=13.8*Gyr
print('   if the conversion ran at a constant rate Gamma since z~1 (7.7 Gyr): Gamma <= %.2e /Gyr  (tau >= %.1e yr); over a Hubble time: Gamma*t_H <= %.3f'%(frac/(7.7), 7.7e9/frac, frac))
print('\n2. WHAT EACH CONVERTED BARYON MUST CARRY (conservation)')
print('   baryon number: dB/dt = +Gamma rho_c/m_p per volume (the cold sector must be able to SUPPLY B, or the process violates B); charge: baryon = p (+1) needs an e- (-1); lepton number: an e- needs a nu_e-bar.')
print('   minimal neutron-decay-like channel: chi -> p + e- + nu_bar (m_chi >~ %.1f MeV per baryon unit; the neutron-proton mass difference is 1.29 MeV: free energy ~ 0.78 MeV shared by e- and nu)'%(939.57))
print('\n3. KINETIC FEEDBACK OF THE PRODUCED GAS (baryons are born at the carrier velocity; the gas is collisional, so they thermalise)')
for lab,sig in (('galaxy halo (200 km/s)',200e3),('group (400)',400e3),('cluster (1000)',1000e3)):
    kT=0.5*mp*sig**2/keV; print('   %-26s kinetic energy per proton = %.3f keV  (thermalises to ~ %.2f keV: the SAME order as the observed gas temperature)'%(lab,kT,kT*2/3))
Mc=1e14*Msun*R0*0.15
for conv in (0.022,0.1):
    L=conv*Mc*0.5*(1000e3)**2/(13.8*Gyr)
    print('   cluster, converting %.1f%% of its free cold pool (%.1e Msun) over t_H: heating %.1e erg/s vs L_X ~ 1e44-45 erg/s (not a constraint for 2%%; %.0f x L_X(1e45) for 10%%)'%(100*conv,Mc/Msun,L*1e7,L*1e7/1e45))
print('\n4. DYNAMICAL SIDE: conversion at rate Gamma removes cold mass that carries the tether/phantom: need Gamma*t_dyn << 1 (t_dyn ~ 0.1-1 Gyr) or the law is perturbed; Gamma*t_H <= %.3f gives Gamma*t_dyn <= %.4f (negligible).'%(frac,frac*0.5/13.8))
