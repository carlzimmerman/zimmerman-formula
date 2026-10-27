import math, numpy as np
exec(open('stiffness_point_mass.py').read().split("G=6.6743e-11")[0])   # reuse solve(), alg_v()
G=6.6743e-11; Ms=1.98847e30; a0=9.36e-11; pc=3.0857e16; Ls=5.75*pc; Mc=2*a0*Ls**2/G/Ms
print('screening radius r_s = L*^2/r_M(M): the scale beyond which the algebraic law is recovered (r_M = sqrt(GM/a0))')
for M in (1,3e3,1e5,1e7,1e11): 
    rM=math.sqrt(G*M*Ms/a0)/pc; print('  M=%.0e Msun: r_M=%.3g pc, r_s = %.3g pc'%(M,rM,5.75**2/rM))
print('\nUFD-like point source: enclosed (baryon + phantom) mass inside r_half, stiffened vs algebraic, and the implied velocity-dispersion shift')
print('%8s %8s | M_tot/M stiff  alg   | d log10 sigma (stiff - alg)'%('M*','r_half'))
for M in (1e3,3e3,1e4):
    for r in (20,30,50):
        m=2*M/Mc; s,_=solve(m); x=r/5.75
        st=1+s.sol(x)[0]*x**2/m; al=1+alg_v(m,x)*x**2/m
        print('%8.0e %6d pc | %10.1f %8.1f | %+.3f'%(M,r,st,al,0.5*math.log10(st/al)))
