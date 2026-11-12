# hy4_preview_push / hy4_crux_check.py  (2026-11-11)
# Three computations, no lane, no label, nothing graded. Adopts nothing.
#   A. The law's static halo: the stress, and the sign of the radial one.
#   B. Can the anisotropic stress carry the lensing?  (active / Tolman mass)
#   C. The amount budget: required cold mass vs the cosmic 5.41 and the delivered ~1.
# Footings never pooled: a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt) m/s^2.
import math

G    = 6.6743e-11
K    = 4*math.pi*G
c    = 299792458.0
Msun = 1.989e30
kpc  = 3.0857e19
pc   = 3.0857e16

FOOT = (('canonical', 9.3603e-11), ('alt', 1.1312e-10))

def g_law(a0, Mb, r):
    gN = G*Mb/r**2
    return gN*(0.5 + math.sqrt(0.25 + a0/gN))

def Mc(a0, Mb, r):
    return r**2*(g_law(a0, Mb, r) - G*Mb/r**2)/G

def halo(a0, Mb, r):
    g  = g_law(a0, Mb, r)
    u  = g/a0
    J  = (a0**2/K)*(u - math.log(1+u))       # the law's Legendre partner
    Pi_tt = J
    Pi_rr = J - g**2/(K*(1+u))               # the radial piece
    h  = r*1e-6
    rho = (Mc(a0, Mb, r+h) - Mc(a0, Mb, r-h))/(2*h)/(4*math.pi*r**2)
    return g, u, rho, Pi_rr, Pi_tt

print('='*78)
print("A.  The law's static halo: the stress and the sign of its radial piece")
print('='*78)
for name, a0 in FOOT:
    Mb = 1e11*Msun
    rM = math.sqrt(G*Mb/a0)
    vi = (G*Mb*a0)**0.25
    print('\n  %-9s a0 = %.4e m/s^2, log M_b = 11, r_M = %.2f kpc, v_inf = %.1f km/s'
          % (name, a0, rM/kpc, vi/1e3))
    print('    r/r_M     rho_c [Msun/pc^3]   sigma_r^2/c^2   sigma_t^2/c^2   (Pi_rr+Pi_tt)/Pi_tt')
    for xf in (0.1, 1.0, 3.0, 10.0, 30.0, 100.0):
        r = rM*xf
        g, u, rho, Prr, Ptt = halo(a0, Mb, r)
        print('    %6.1f   %14.4e   %+13.4e   %+13.4e   %+10.2e'
              % (xf, rho*pc**3/Msun, Prr/rho/c**2, Ptt/rho/c**2, (Prr+Ptt)/Ptt))
print('\n  A1  sigma_r^2 = -sigma_t^2 in the deep field: the radial "dispersion" is NEGATIVE.')
print('      A kinetic gas cannot have it. A medium with a shear modulus (a solid) can.')
print('      Large-r closed form: sigma_t^2 = (1/2) sqrt(G M_b a0) = v_inf^2/2  (PD1 P7).')

print('\n'+'='*78)
print('B.  Can that anisotropic stress carry the lensing?')
print('='*78)
print('  Active (Tolman) source of a static spherical configuration: rho + (p_r + 2 p_t)/c^2.')
print('  Here p_r = Pi_rr, p_t = Pi_tt, and Pi_rr + Pi_tt = 0, so p_r + 2 p_t = Pi_tt.')
print('  Fractional correction to the lensing source = (Pi_tt/c^2)/rho = sigma_t^2/c^2.')
print('  Large-r closed form: sqrt(G M_b a0)/(2 c^2).')
print('\n    log M_b    canonical          alt                what it must cover')
for lm in range(9, 16):
    vals = []
    for name, a0 in FOOT:
        Mb = 10.0**lm*Msun
        vals.append(math.sqrt(G*Mb*a0)/(2*c**2))
    print('      %2d     %-17.4e %-17.4e  a factor 6 to 20 of halo mass' % (lm, vals[0], vals[1]))
print('\n  B1  VERDICT: the anisotropic stress contributes ~1e-6 of the lensing source, against a')
print('      shortfall of a factor 6 to 20. The stress tells you what the medium is; it does not')
print('      pay the amount. The lensing signal is mass.')

print('\n'+'='*78)
print('C.  The amount budget')
print('='*78)
Xs = 5.41                                   # Omega_c / Omega_b, the whole cosmic budget
print('  Budget: M_c <= 5.41 M_b (all the cold charge comoving with the galaxy\'s baryons).')
print('  Law:    M_c(<r) = M_b X(x),  X(x) = (sqrt(1+4x^2)-1)/2,  x = r/r_M.')
xbreak = math.sqrt(Xs*(Xs+1.0))
print('  X(x) = 5.41 at x = %.4f r_M. Beyond that the law\'s halo exceeds the entire' % xbreak)
print('  cosmic cold budget, and X grows as x thereafter.')
print('\n    log M_b    r_M [kpc]    budget gone at      at 30 r_M needs     ratio')
for name, a0 in FOOT:
    print('  %s:' % name)
    for lm in (9, 10, 11, 12):
        Mb = 10.0**lm*Msun
        rM = math.sqrt(G*Mb/a0)/kpc
        X30 = (math.sqrt(1+4*900)-1)/2
        print('      %2d       %8.2f     %8.1f kpc         %6.2f M_b       %5.2fx'
              % (lm, rM, xbreak*rM, X30, X30/Xs))
print('\n  C1  Required to pass KiDS host-free (ONE1): share X_s = 59.5 M_b.')
print('      vs the 5.41 budget          : %.2fx over.' % (59.5/5.41))
print('      vs the charge that falls in : %.0fx to %.0fx over (VSH1: 0.9-1.4 M_b).'
      % (59.5/1.4, 59.5/0.9))
print('  C2  T4 (exact: net polarization charge in any free-fall-bounded ball is 0 at all times,')
print('      for any momentum equation) and LFS1 (exact: static polarization is frozen, the')
print("      halo's charge changes only by O(|Phi|/c^2) ~ 1e-6) say the halo's charge EQUALS the")
print('      dust charge carried in. So the cap is a conservation law, not a mechanism failure.')
print('  C3  The one reconciliation: g_bar at KiDS radii is missing hot gas. The law would be')
print('      evaluated with g_bar raised %.1fx there. The record\'s own note: "with B21\'s own'
      % (59.5/5.41))
print('      hot-gas estimate in g_bar, its published outer points drop from 1.50 to 0.47 of the')
print('      law. Nothing on disk measures that gas."')

print('\n'+'='*78)
print('D.  What the deep field gives, for the mechanism')
print('='*78)
for name, a0 in FOOT:
    col = a0/(2*math.pi*G)/Msun*pc**2
    pre = a0**2/(8*math.pi*G)
    print('  %-9s column a0/(2 pi G) = %.1f Msun/pc^2  (the same for every galaxy)'
          % (name, col))
    print('  %-9s pressure scale a0^2/(8 pi G) = %.4e Pa = rho_Lambda c^2/(32 pi) at kappa = 1/2'
          % ('', pre))
print('\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.')
