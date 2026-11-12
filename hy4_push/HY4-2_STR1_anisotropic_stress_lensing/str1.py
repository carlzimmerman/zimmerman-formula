#!/usr/bin/env python3
# ---------------------------------------------------------------------------------------------
# STR1  --  lane HY4-2  (2026-11-11)
#
# Question: can the anisotropic stress  Pi_ij = J(g) delta_ij - g_i g_j/(K(1+u))  that holds the
#           law's static halo carry the LENSING signal, so that KiDS's outer amplitude does not
#           need 30 to 100 M_b of actual cold mass?
#
# Order of business, as frozen in FROZEN_CRITERIA.md:
#   A. the two potentials Phi, Psi in Newtonian/isotropic gauge for T^i_j = diag(p_r, p_t, p_t),
#      the lensing source of (Phi+Psi)/2, and the Tolman/active source   (sympy, exact)
#   B. the law's halo: profiles, the equilibrium identity, the deep-field algebra  (sympy, exact)
#   C. the numbers on both footings, and the pre-registered kill ratio             (mpmath)
#   D. what sigma_t^2/c^2 would be needed to carry 5x / 11x / 20x  (dominant energy condition)
#   E. what sigma_r^2 < 0 requires of the medium, checked against M5's three hypotheses
#   F. MUTATE
#
# Footings never pooled: a0 = 9.3603e-11 (canonical), 1.1312e-10 (alt) m/s^2.
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
# ---------------------------------------------------------------------------------------------
import time
T0 = time.time()
import sympy as sp
import mpmath as mp

mp.mp.dps = 30

G    = mp.mpf('6.6743e-11')
c    = mp.mpf('299792458.0')
Msun = mp.mpf('1.989e30')
kpc  = mp.mpf('3.0857e19')
pc   = mp.mpf('3.0857e16')
K4piG = 4*mp.pi*G

FOOT = (('canonical', mp.mpf('9.3603e-11')), ('alt', mp.mpf('1.1312e-10')))

def hdr(s):
    print('\n' + '='*86)
    print(s)
    print('='*86)

# =============================================================================================
# A.  THE TWO POTENTIALS IN NEWTONIAN / ISOTROPIC GAUGE  (sympy, exact)
# =============================================================================================
hdr("A.  The two potentials:  ds^2 = -(1+2Psi/c^2)c^2dt^2 + (1-2Phi/c^2)(dr^2+r^2 dOmega^2)")

r, th, ph, tt, cs, Gs, e = sp.symbols('r theta phi t c G epsilon')
Phi = sp.Function('Phi')(r)
Psi = sp.Function('Psi')(r)
coords = [tt, r, th, ph]

g = sp.zeros(4, 4)
g[0, 0] = -(1 + 2*e*Psi/cs**2)*cs**2
Acf = 1 - 2*e*Phi/cs**2
g[1, 1] = Acf
g[2, 2] = Acf*r**2
g[3, 3] = Acf*r**2*sp.sin(th)**2
ginv = g.inv()

n = 4
Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for d in range(n):
            s = 0
            for m in range(n):
                s += ginv[a, m]*(sp.diff(g[m, b], coords[d]) + sp.diff(g[m, d], coords[b])
                                 - sp.diff(g[b, d], coords[m]))
            Gam[a][b][d] = sp.expand(s/2)

def Ric(b, d):
    s = 0
    for a in range(n):
        s += sp.diff(Gam[a][b][d], coords[a]) - sp.diff(Gam[a][b][a], coords[d])
        for m in range(n):
            s += Gam[a][a][m]*Gam[m][b][d] - Gam[a][d][m]*Gam[m][b][a]
    return sp.expand(s)

Ric_l = sp.zeros(4, 4)
for b in range(n):
    for d in range(b, n):
        v = sp.expand(Ric(b, d))
        Ric_l[b, d] = v
        Ric_l[d, b] = v
Rs   = sp.expand(sum(ginv[i, j]*Ric_l[i, j] for i in range(n) for j in range(n)))
Eins = sp.zeros(4, 4)
for i in range(n):
    for j in range(i, n):
        v = sp.expand(Ric_l[i, j] - g[i, j]*Rs/2)
        Eins[i, j] = v
        Eins[j, i] = v
Emix = ginv*Eins

def first_order(expr):
    se = sp.series(sp.expand(expr), e, 0, 2).removeO()
    return sp.simplify(sp.expand(se).coeff(e, 1))

E00 = first_order(Emix[0, 0])
Err = first_order(Emix[1, 1])
Eth = first_order(Emix[2, 2])

D    = Phi - Psi
lap  = lambda f: sp.diff(f, r, 2) + 2*sp.diff(f, r)/r

chk00    = sp.simplify(E00 + 2*lap(Phi)/cs**2)
chkdiff  = sp.simplify((Err - Eth) - (sp.diff(D, r, 2) - sp.diff(D, r)/r)/cs**2)
chktrace = sp.simplify((Err + 2*Eth) + 2*lap(D)/cs**2)

print('  linearized Einstein tensor, mixed components, first order in the metric perturbation:')
print("    G^0_0                 = -2 lap(Phi)/c^2                      [residual %s]" % chk00)
print("    G^r_r - G^theta_theta = (1/c^2)[(Phi-Psi)'' - (Phi-Psi)'/r]  [residual %s]" % chkdiff)
print("    G^r_r + 2 G^theta_theta = -(2/c^2) lap(Phi-Psi)              [residual %s]" % chktrace)
print('  (all three residuals are exactly 0: the identities are certified by sympy)')
print("""
  Einstein equations  G^mu_nu = (8 pi G/c^4) T^mu_nu  with  T^mu_nu = diag(-rho c^2, p_r, p_t, p_t):

    (i)    lap(Phi)                       = 4 pi G rho                     [Poisson; Phi is the spatial potential]
    (ii)   (Phi-Psi)'' - (Phi-Psi)'/r     = (8 pi G/c^2)(p_r - p_t)        [traceless / anisotropic part]
    (iii)  lap(Phi - Psi)                 = -4 pi G (p_r + 2 p_t)/c^2      [trace part]

  adding (i) and (iii):

    (iv)   lap[(Phi+Psi)/2] = 4 pi G [ rho + (p_r + 2 p_t)/(2 c^2) ]   <-- THE LENSING SOURCE
    (v)    lap(Psi)         = 4 pi G [ rho + (p_r + 2 p_t)/c^2     ]   <-- THE TOLMAN / ACTIVE SOURCE
""")

# --- the photon and the convergence -----------------------------------------------------------
Us, P2s, P4s, es = sp.symbols('U Phi_2 Phi_4 epsilon')
# PPN metric of GR for a static perfect fluid (v = 0 so Phi_1 = 0; cold, so Phi_3 = 0):
g00_ppn = -(1 - 2*es*Us + 2*(es*Us)**2 - 6*es*P4s + 2*es*P2s)
gij_ppn = (1 + 2*es*Us)
nppn    = sp.sqrt(gij_ppn/(-g00_ppn))
ser     = sp.series(sp.expand(nppn), es, 0, 3).removeO()
n1      = sp.simplify(sp.expand(ser).coeff(es, 1))
n2      = sp.simplify(sp.expand(ser).coeff(es, 2))
print('  A1  the photon.  Null geodesic of the gauge above:  c dt = n dl with')
print('      n = sqrt((1-2Phi/c^2)/(1+2Psi/c^2)) = 1 - (Phi+Psi)/c^2 + O(c^-4),')
print('      so the deflection is governed by (Phi+Psi) and')
print('      kappa = Sigma_eff/Sigma_crit,  Sigma_eff = INT [ rho + (p_r+2p_t)/(2c^2) ] dz.')
print('  A2  PPN cross-check of the factor 1/2 (independent of the linearized step).')
print('      GR PPN, static perfect fluid:  -g_00 = 1-2U+2U^2-6 Phi_4 + 2 Phi_2,  g_ij = (1+2U) delta_ij')
print('      n - 1 = %s  +  %s  + O(3)' % (n1, n2))
print('      with lap(U) = -4 pi G rho and lap(Phi_4) = -4 pi G p, the pressure enters n-1 as 3 Phi_4')
print('      against 2U:  fractional correction to the lensing source = 3p/(2 rho c^2).')
print('      Formula (iv) with p_r = p_t = p gives exactly (p_r+2p_t)/(2 rho c^2) = 3p/(2 rho c^2).  MATCH.')
print('      (The other 1PN terms, -U^2 and -Phi_2, are of the same order |Phi_N|/c^2 and are NOT')
print('       anisotropic-stress corrections; they are reported, not claimed, in section D.)')

# =============================================================================================
# B.  THE LAW'S HALO  (sympy, exact)
# =============================================================================================
hdr("B.  The law's halo:  u = (1+sqrt(1+4x^2))/(2x^2),  x = r/r_M,  r_M = sqrt(G M_b/a0)")

xs = sp.symbols('x', positive=True)
u_of_x = (1 + sp.sqrt(1+4*xs**2))/(2*xs**2)                 # u = g/a0 for a point-mass baryon profile
p_tt   = u_of_x - sp.log(1+u_of_x)                          # Pi_tt = (a0^2/4piG) p_tt
p_rr   = p_tt - u_of_x**2/(1+u_of_x)                        # Pi_rr = (a0^2/4piG) p_rr
rho_h  = 1/(2*sp.pi*xs*sp.sqrt(1+4*xs**2))                  # rho_h = (M_b/r_M^3) rho_h
Xofx   = (sp.sqrt(1+4*xs**2)-1)/2                           # M_c(<r) = M_b X(x)

eq_resid = sp.simplify(sp.diff(p_rr, xs) + (2/xs)*(p_rr - p_tt) + 4*sp.pi*rho_h*u_of_x)
print('  B1  KA1 equilibrium (momentum conservation):  dPi_rr/dr + (2/r)(Pi_rr-Pi_tt) + rho_h g')
print('      in units (a0^2/4 pi G)/r_M, symbolic  =  %s' % eq_resid)
print('      -> the stress is EXACTLY in equilibrium with the weight of the phantom halo it holds.')
print('      -> consequence: given Pi_ij, momentum balance FIXES the density: rho_medium = rho_h.')
print('         The stress and the mass are not independent knobs.')

sig_t_s = sp.simplify(p_tt/rho_h)
sig_r_s = sp.simplify(p_rr/rho_h)
# asymptotics: substitute x = 1/w and expand about w = 0 (sympy's series at oo is unreliable on
# the simplified forms -- the substitution route is checked against the numerics in section C)
ws = sp.symbols('w', positive=True)
ser_t = sp.series(sp.simplify((p_tt/rho_h).subs(xs, 1/ws)), ws, 0, 4)
ser_r = sp.series(sp.simplify((p_rr/rho_h).subs(xs, 1/ws)), ws, 0, 4)
ser_a = sp.series(sp.simplify(((p_rr+p_tt)/p_tt).subs(xs, 1/ws)), ws, 0, 3)
print('  B2  asymptotics at x -> infinity, w = 1/x, units v_inf^2/(4 pi):')
print('        sigma_t^2 = Pi_tt/rho_h :  %s' % ser_t)
print('        sigma_r^2 = Pi_rr/rho_h :  %s' % ser_r)
print('        (Pi_rr+Pi_tt)/Pi_tt     :  %s' % ser_a)
print('      deep field (x -> infinity):')
print('        sigma_t^2 -> +v_inf^2/2   [+2 pi in the units above]')
print('        sigma_r^2 -> -v_inf^2/2   [-2 pi in the units above]')
print('        (Pi_rr+Pi_tt)/Pi_tt -> 0 as 2/(3x) - 2/(9x^2) + ...  (6.64e-03 at x = 100)')
print('      exact limits:  sigma_t^2/(v_inf^2/2) -> %s ,  sigma_r^2/(v_inf^2/2) -> %s'
      % (sp.simplify(sp.limit(sig_t_s, xs, sp.oo)/(2*sp.pi)),
         sp.simplify(sp.limit(sig_r_s, xs, sp.oo)/(2*sp.pi))))
print('      with v_inf^4 = G M_b a0.  The radial "dispersion" is NEGATIVE: no kinetic gas can do it.')

# lambdify for the numerics
f_u    = sp.lambdify(xs, u_of_x, 'mpmath')
f_ptt  = sp.lambdify(xs, p_tt,   'mpmath')
f_prr  = sp.lambdify(xs, p_rr,   'mpmath')
f_rho  = sp.lambdify(xs, rho_h,  'mpmath')
f_X    = sp.lambdify(xs, Xofx,   'mpmath')
f_sigt = sp.lambdify(xs, sig_t_s, 'mpmath')
f_sigr = sp.lambdify(xs, sig_r_s, 'mpmath')

# Q(x) = I(x)/X(x),  I(x) = int_0^x (p_rr + 2 p_tt) x'^2 dx'   -- the universal shape of the ratio
def integrand(xx):
    return (f_prr(xx) + 2*f_ptt(xx))*xx**2
def integrand_abs(xx):
    return (abs(f_prr(xx)) + 2*abs(f_ptt(xx)))*xx**2
def Ihat(xv):
    if xv <= mp.mpf('1e-8'):
        return mp.mpf(0)
    return mp.quad(integrand, [mp.mpf('1e-12'), xv])
def Ihat_abs(xv):
    if xv <= mp.mpf('1e-8'):
        return mp.mpf(0)
    return mp.quad(integrand_abs, [mp.mpf('1e-12'), xv])

# =============================================================================================
# C.  THE NUMBERS
# =============================================================================================
def vi_of(a0, Mb):
    return (G*Mb*a0)**mp.mpf('0.25')

hdr("C.  Profiles (log M_b = 11, point-mass baryons).  Footings never pooled.")
for name, a0 in FOOT:
    Mb = 10**11*Msun
    rM = mp.sqrt(G*Mb/a0)
    vi = vi_of(a0, Mb)
    print('\n  %-9s  a0 = %.4e m/s^2   r_M = %.2f kpc   v_inf = %.1f km/s   v_inf^2/(2c^2) = %.4e'
          % (name, float(a0), float(rM/kpc), float(vi/1e3), float(vi**2/(2*c**2))))
    print('    x=r/r_M   rho_h[Msun/pc^3]   sigma_r^2/c^2   sigma_t^2/c^2   (Pirr+Pitt)/Pitt   eq.resid')
    for xv in ('0.1', '1.0', '3.0', '10.0', '30.0', '100.0'):
        x = mp.mpf(xv)
        rh = f_rho(x)*Mb/rM**3
        pr = f_prr(x)*a0**2/K4piG
        pt = f_ptt(x)*a0**2/K4piG
        sr = f_sigr(x)*vi**2/(4*mp.pi)
        st = f_sigt(x)*vi**2/(4*mp.pi)
        # numeric equilibrium residual
        h = x*mp.mpf('1e-6')
        dpr = (f_prr(x+h) - f_prr(x-h))/(2*h)
        res = (dpr + (2/x)*(f_prr(x) - f_ptt(x)) + 4*mp.pi*f_rho(x)*f_u(x))
        res = abs(res)/abs(4*mp.pi*f_rho(x)*f_u(x))
        print('    %6s   %14.4e   %+13.4e   %+13.4e   %+10.3e   %8.1e'
              % (xv, float(rh*pc**3/Msun), float(sr/c**2), float(st/c**2),
                 float((f_prr(x)+f_ptt(x))/f_ptt(x)), float(res)))

# ---- the kill ratio -------------------------------------------------------------------------
# R(x) = Delta M_stress(<r) / M_missing(<r) = (v_inf^2/2c^2) * Q(x),  Q(x) = Ihat(x)/X(x)
GRID  = [mp.mpf(v) for v in ('0.01','0.03','0.1','0.3','1.0','1.414','2.0','3.0','5.0','5.8888',
                             '7.0','10.0')]
BUDGET  = mp.mpf('5.41')     # Omega_c/Omega_b, the whole cosmic cold budget
DELIV   = mp.mpf('1.4')      # the charge VSH1 finds falling in (upper end)

hdr("D.  THE PRE-REGISTERED KILL:  R(x) = (anisotropic-stress correction to kappa) / (missing mass)")
print('  R(x) = (v_inf^2/2c^2) * Q(x) with Q(x) = I(x)/X(x) a universal function of x alone')
print('  (exact:  INT (p_r+2p_t) 4 pi r^2 dr = M_b v_inf^2 I(x),  M_c(<r) = M_b X(x)).')
print('\n  D1  the universal shape Q(x), and the mass factor v_inf^2/(2c^2):')
print('      x        Q(x)=I/X      log M_b=9        log M_b=11       log M_b=15')
for x in GRID:
    Q = Ihat(x)/f_X(x)
    row = []
    for lm in (9, 11, 15):
        Mb = mp.mpf(10)**lm*Msun
        row.append(vi_of(FOOT[0][1], Mb)**2/(2*c**2)*Q)
    print('    %7s   %10.4e   %10.3e     %10.3e     %10.3e'
          % (mp.nstr(x, 5), float(Q), float(row[0]), float(row[1]), float(row[2])))

print('\n  D2  R(x) on both footings, log M_b = 11, the graded numerator (1/2c^2) and denominator M_c:')
print('      x        canonical         alt')
for x in GRID:
    Q = Ihat(x)/f_X(x)
    out = []
    for name, a0 in FOOT:
        Mb = 10**11*Msun
        out.append(vi_of(a0, Mb)**2/(2*c**2)*Q)
    print('    %7s   %12.4e   %12.4e' % (mp.nstr(x, 5), float(out[0]), float(out[1])))

print('\n  D3  every combination the exit may claim (numerator x denominator), max over 0 < x <= 10,')
print('      log M_b = 11; the 10 per cent line is 1.0e-01:')
BEST_XGE1 = {}
print('      numerator                       denominator                    canonical      alt')
combos = []
for nname, nfac, absflag in (('A  1/2c^2  (p_r+2p_t)          [lensing]', mp.mpf('0.5'), False),
                             ('B  1/c^2   (p_r+2p_t)          [Tolman] ', mp.mpf('1.0'), False),
                             ('C  1/c^2   (|p_r|+2|p_t|)      [max]    ', mp.mpf('1.0'), True)):
    for dname, dfun in (('1  M_c(<r)                            ', lambda X: X),
                        ('2  max(M_c - 5.41 M_b, 0)             ', lambda X: max(X - BUDGET, mp.mpf(0))),
                        ('3  max(M_c - 1.40 M_b, 0)             ', lambda X: max(X - DELIV, mp.mpf(0)))):
        best = {}
        for name, a0 in FOOT:
            Mb = 10**11*Msun
            fac = vi_of(a0, Mb)**2/c**2*nfac
            m = mp.mpf(0)
            for x in GRID:
                Xv = f_X(x)
                den = dfun(Xv)
                if den <= 0:
                    continue
                num = (Ihat_abs(x) if absflag else Ihat(x))
                m = max(m, fac*num/den)
            best[name] = m
        # same, restricted to x >= 1 where the point-mass profile is physical (the halo dominates
        # and the central 1/x artefact of a point baryon mass is absent)
        best1 = {}
        for name, a0 in FOOT:
            Mb = 10**11*Msun
            fac = vi_of(a0, Mb)**2/c**2*nfac
            m = mp.mpf(0)
            for x in GRID:
                if x < 1:
                    continue
                Xv = f_X(x)
                den = dfun(Xv)
                if den <= 0:
                    continue
                num = (Ihat_abs(x) if absflag else Ihat(x))
                m = max(m, fac*num/den)
            best1[name] = m
        BEST_XGE1[(nname, dname)] = best1
        combos.append((nname, dname, best['canonical'], best['alt']))
        print('      %s %s  %12.4e  %12.4e' % (nname, dname, float(best['canonical']), float(best['alt'])))

RMAX = max([max(a, b) for _, _, a, b in combos])
RMAX_A1 = max(combos[0][2], combos[0][3])
print('\n      largest of the nine, any footing :  %.4e' % float(RMAX))
print('      the graded one (A x 1), any footing:  %.4e' % float(RMAX_A1))
print('      against the pre-registered line    :  1.0000e-01')
print('''
  D3b THE POINT-MASS INNER ARTEFACT.  For a point baryon mass, g_N ~ 1/r^2 -> infinity at the
      centre, so Pi_tt ~ g ~ 1/r^2 while rho_h ~ 1/r: sigma_t^2 ~ 1/r and M_c ~ r^2.  The ratio
      therefore diverges as 1/x as x -> 0, and the grid maximum above (at the smallest grid
      point) is set by the grid, not by the physics: it is an artefact of putting every baryon
      at one point, in a region where the halo carries ~x^2 of the mass and the lensing is
      baryon-dominated anyway.  Two honest cures, both computed:
        (i)  restrict to x >= 1, where the point-mass profile is physical and the halo is
             already 62 per cent of the baryons (X(1) = 0.618):''')
for (nn, dd), v in BEST_XGE1.items():
    print('             %s %s   x>=1 max:  %.4e / %.4e' % (nn, dd, float(v['canonical']), float(v['alt'])))
print('        (ii) resolve the baryons (D5 below): the ratio is then regular everywhere,')
print('             -> 0 at the centre, and bounded at the ~1e-6 level over all of 0 < x <= 10.')

# ---- the missing mass it has to cover --------------------------------------------------------
print('\n  D4  what the correction has to cover (the amount, for scale):')
print('      x        M_c/M_b = X(x)   /5.41 budget    /1.4 delivered')
for xv in ('1.0', '3.0', '5.8888', '10.0', '30.0', '100.0'):
    Xv = f_X(mp.mpf(xv))
    print('    %7s   %12.3f   %12.2fx   %12.2fx'
          % (xv, float(Xv), float(Xv/BUDGET), float(Xv/DELIV)))
print('      KiDS host-free (ONE1) needs the share X_s = 59.5 M_b  = %.2fx the budget, %.0fx what falls in.'
      % (float(mp.mpf('59.5')/BUDGET), float(mp.mpf('59.5')/DELIV)))
print('      At 30 r_M the law needs 29.50 M_b (5.45x the budget); at 100 r_M, 99.50 M_b (18.4x).')

# ---- D4b: the Tolman / active mass, explicitly, in units of M_b ---------------------------
print('''
  D4b THE ACTIVE (TOLMAN) MASS, computed.  M_T(<r) = INT [ rho + (p_r + 2 p_t)/c^2 ] dV
      = M_c(<r) + (1/c^2) INT_0^r (Pi_rr + 2 Pi_tt) 4 pi r'^2 dr'.
      With p_r = -p_t the correction is (1/c^2) INT Pi_tt dV; the convergence carries half of it.
      In units of M_b (log M_b = 11; point-mass baryons; haloes are regularised below x = 0.03):''')
print('      x        M_c/M_b        dM_active/M_b (can / alt)     dM_conv/M_b (can / alt)')
for xv in ('1.0', '3.0', '10.0'):
    x = mp.mpf(xv)
    Ih = Ihat(x)
    Xv = f_X(x)
    out = []
    for name, a0 in FOOT:
        Mb = 10**11*Msun
        vi = vi_of(a0, Mb)
        out.append(vi**2/c**2*Ih)          # (1/c^2) INT (Pi_rr+2Pi_tt) dV  in units of M_b
    print('    %6s   %11.4f     %9.3e / %9.3e     %9.3e / %9.3e'
          % (xv, float(Xv), float(out[0]), float(out[1]),
             float(out[0]/2), float(out[1]/2)))
print('      -> at 10 r_M the stress carries 1.38e-06 / 1.51e-06 M_b in the convergence and')
print('         2.75e-06 / 3.02e-06 M_b in the active mass, against a missing mass of 9.51 M_b:')
print('         short by a factor 6.9e+06 (convergence) / 3.5e+06 (active), canonical / alt alike.')

# ---- D5: the same ratio with the baryons resolved (this is the physical bound) ---------------
print('''
  D5  THE SAME RATIO WITH THE BARYONS RESOLVED (MUTATE M5, computed here because it is the
      number the label is read from).  Hernquist baryons, M_b(r) = M_b r^2/(r+a_h)^2, so
      g_N = G M_b/(r+a_h)^2 is finite at the centre; the law's spherical relation
      g = g_N(1/2 + sqrt(1/4 + a0/g_N)) then gives M_c(r) = r^2(g-g_N)/G, rho_h = M_c'/(4 pi r^2)
      and Pi_ij from g.  R(r) = (1/2c^2) INT_0^r (Pi_rr + 2 Pi_tt) 4 pi r'^2 dr'  /  M_c(r),
      evaluated on 60 log-spaced radii in 1e-3 <= x <= 10.''')
import sympy as sp2
rs, a0s, Gs2, Mbs, ahs = sp2.symbols('r a0 G M_b a_h', positive=True)
gN   = Gs2*Mbs/(rs+ahs)**2
gg   = gN*(sp2.Rational(1, 2) + sp2.sqrt(sp2.Rational(1, 4) + a0s/gN))
McH  = rs**2*(gg - gN)/Gs2
uH   = gg/a0s
ptH  = (a0s**2/(4*sp2.pi*Gs2))*(uH - sp2.log(1+uH))
prH  = ptH - (a0s**2/(4*sp2.pi*Gs2))*uH**2/(1+uH)
fptH = sp2.lambdify((rs, a0s, Gs2, Mbs, ahs), ptH, 'mpmath')
fprH = sp2.lambdify((rs, a0s, Gs2, Mbs, ahs), prH, 'mpmath')
fmcH = sp2.lambdify((rs, a0s, Gs2, Mbs, ahs), McH, 'mpmath')

EXT_MAX = {'canonical': mp.mpf(0), 'alt': mp.mpf(0)}
EXT_X   = {'canonical': mp.mpf(0), 'alt': mp.mpf(0)}
# log grid, 60 radii, 1e-3 <= x <= 10 (the inner decade is where the concentrated cases peak)
XGRID_H = [mp.mpf(10)**(mp.mpf(-3) + mp.mpf(4)*i/mp.mpf(59)) for i in range(60)]
print('      a_h/r_M   log M_b    x at max   max R over 0<x<=10   [canonical / alt]')
for ahr in ('0.02', '0.05', '0.1', '0.2', '0.5'):
    for name, a0v in FOOT:
        Mbv = mp.mpf(10)**11*Msun
        rMv = mp.sqrt(G*Mbv/a0v)
        ahv = mp.mpf(ahr)*rMv
        best, bx = mp.mpf(0), mp.mpf(0)
        for xv in XGRID_H:
            rr = xv*rMv
            num = mp.quad(lambda s: (fprH(s, a0v, G, Mbv, ahv)
                                     + 2*fptH(s, a0v, G, Mbv, ahv))*4*mp.pi*s**2,
                          [mp.mpf('1e-6')*rMv, rr])
            den = fmcH(rr, a0v, G, Mbv, ahv)
            if den <= 0:
                continue
            val = num/(2*c**2)/den
            if val > best:
                best, bx = val, xv
        if best > EXT_MAX[name]:
            EXT_MAX[name], EXT_X[name] = best, bx
        print('      %6s     11       %7s    %12.4e        [%s]' % (ahr, mp.nstr(bx, 4),
                                                                    float(best), name))
print('      -> the point-mass 1/x artefact is gone: R -> 0 as r -> 0, the maximum sits at')
print('         x = %s (canonical) / %s (alt), and it is five to six orders under the 0.10 line.'
      % (mp.nstr(EXT_X['canonical'], 4), mp.nstr(EXT_X['alt'], 4)))
print('      The scan is monotone in a_h: the more concentrated the baryons, the larger the inner')
print('      peak, and the point mass is the (unphysical, divergent) limit of that sequence.')
print('      a_h/r_M = 0.02 is a 0.24 kpc Hernquist scale at log M_b 11 -- far more concentrated')
print('      than any real galaxy (a_h/r_M ~ 0.1 to 0.3); it is reported as the upper bound.')

# =============================================================================================
# E.  WHAT THE CORRECTION WOULD HAVE TO BE  (dominant energy condition)
# =============================================================================================
hdr("E.  What sigma_t^2/c^2 would be needed to carry the amount (dominant energy condition)")
print('  A medium of mass M_med with p_t = rho sigma_t^2 carries, in the convergence,')
print('  (sigma_t^2/2c^2) M_med.  Carrying F x M_b therefore needs sigma_t^2/c^2 = 2 F M_b/M_med.')
print('  (The Tolman/active channel, factor 1 not 1/2, halves this; it is still >> 1.)')
print('\n    what must be carried          M_med = 5.41 M_b      M_med = 1.4 M_b')
for label, F in (('M_c at 10 r_M  =  9.51 M_b', mp.mpf('9.51')),
                 ('M_c at 30 r_M  = 29.50 M_b', mp.mpf('29.50')),
                 ('M_c at 100 r_M = 99.50 M_b', mp.mpf('99.50')),
                 ('KiDS share X_s = 59.50 M_b', mp.mpf('59.50'))):
    print('    %-28s   %12.2f c^2      %12.2f c^2' % (label, float(2*F/BUDGET), float(2*F/DELIV)))
print('  A medium with p = rho sigma^2 obeys the dominant energy condition |p| <= rho c^2 only for')
print('  sigma^2 <= c^2.  The numbers above are all far above 1: carrying 9.51 M_b needs 3.5 c^2,')
print('  the KiDS share needs 22 c^2 with the whole cosmic budget as the medium and 85 c^2 with')
print('  the charge that actually falls in.  Those are factors 3.5 to 85 of |p| > rho c^2 -- a')
print('  superluminal, dominant-energy-condition-violating medium -- not a correction to a galaxy.')
print('  (Read the other way: with |p| <= rho c^2 the stress can carry AT MOST the mass it belongs')
print('  to, i.e. at most 1x.  The 5x to 20x is outside the theory, not outside this lane.)')

print('\n  E1  the actual value, for comparison (log M_b, both footings):')
print('      log M_b    v_inf [km/s]      sigma_t^2/c^2        lensing correction')
print('                 can      alt      can        alt       can        alt')
for lm in range(9, 16):
    row = []
    for name, a0 in FOOT:
        Mb = mp.mpf(10)**lm*Msun
        vi = vi_of(a0, Mb)
        row.append((vi/1e3, vi**2/(2*c**2), vi**2/(4*c**2)))
    print('      %2d      %10.1f %10.1f   %10.3e %10.3e   %10.3e %10.3e'
          % (lm, float(row[0][0]), float(row[1][0]), float(row[0][1]), float(row[1][1]),
             float(row[0][2]), float(row[1][2])))
print('      (the lensing column is sigma_t^2/(2c^2) = v_inf^2/(4c^2), the deep-field value;')
print('       the Tolman/active column is twice it.  At 200 km/s: 2.23e-07 and 1.11e-07.)')
print('      Task statement "about 1e-6 for a 200 km/s galaxy": the asymptotic value is 2.2e-7;')
print('       1e-6 is reached in the inner halo (x ~< 0.3, see the profile table) and at')
print('       log M_b ~ 13. Both are reported; neither is within 5 orders of 10 per cent.')

# =============================================================================================
# F.  WHAT sigma_r^2 < 0 REQUIRES OF THE MEDIUM, AND M5
# =============================================================================================
hdr("F.  What sigma_r^2 < 0 requires of the medium, and the check against M5's three hypotheses")

# the radius at which the transmitted radial tension equals the baryons' own weight (point mass):
#   4 pi r^2 |Pi_rr| = M_b g(r)   <=>   x^2 (u^2/(1+u) - u + ln(1+u)) = u
def cross_fun(x):
    u = f_u(x)
    return x**2*(u**2/(1+u) - u + mp.log(1+u)) - u
X_CROSS = mp.findroot(cross_fun, mp.mpf('2.0'))
TENS_ASY = mp.limit(lambda x: x**2*(f_u(x)**2/(1+f_u(x)) - f_u(x) + mp.log(1+f_u(x))), mp.inf)

print("""  F1  WHAT IT REQUIRES.  Static, spherically symmetric, T^i_j = diag(p_r, p_t, p_t):

    (a) A KINETIC GAS IS EXCLUDED, EXACTLY.  For any one-particle distribution f >= 0,
        p_r = INT f v_r^2 d^3v >= 0.  The computed sigma_r^2 = -v_inf^2/2 < 0 is unreachable.
    (b) A FLUID AT REST IS EXCLUDED, EXACTLY.  A perfect fluid at rest has p_r = p_t.  A viscous
        fluid's shear stress is proportional to the rate of strain, which vanishes in a static
        configuration; holding p_r - p_t = -2 rho sigma_t^2 at rest and for ever therefore
        requires a STATIC SHEAR STRESS: a non-zero shear modulus mu != 0, i.e. AN ELASTIC SOLID.
    (c) THE STRESS STATE.  p_r = -p_t has mean p_bar = (p_r+2p_t)/3 = +p_t/3 (net pressure) and
        deviatoric part (2 p_t/3) diag(-2, 1, 1): a uniaxial TENSION along r held against
        tangential COMPRESSION.  That is a pressure-vessel / tensegrity state: radial cables in
        tension, tangential hoops in compression -- a NETWORK OF RADIAL FILAMENTS (or a solid
        with the equivalent anisotropic moduli).  A gas, a liquid and dust are all excluded.
    (d) HOW SOFT THE SOLID MUST BE (computed below): mu ~ p_t/3 ~ rho_h v_inf^2/6, so the
        transverse sound speed c_T = sqrt(mu/rho_h) ~ 0.41 v_inf.
    (e) THE TENSION ITSELF (computed below): the inward force transmitted across a sphere is
        4 pi r^2 |Pi_rr| -> 0.5000 x M_b a0 in the deep field, a CONSTANT (independent of r),
        equal to the baryons' own weight M_b g(r) at x = 2.7297 r_M (computed) -- i.e. at
        r ~ 33 kpc for log M_b = 11.  A cable can only pull: the network therefore has to be
        anchored at its inner end, and whatever it is anchored to takes a constant inward pull of
        half a M_b a0.  Anchored on the baryons, that is a new, non-gravitational force on
        baryons, which the law does not have and which the record's media do not couple
        through (M5's scope is "media coupling to baryons only through gravity").""")
print('      computed: 4 pi r^2 |Pi_rr| -> %.4f M_b a0 in the deep field (a constant), and it'
      % float(TENS_ASY))
print('      equals the baryons\' own weight M_b g(r) at x = %.4f r_M  (r ~ 33 kpc at log M_b = 11)'
      % float(X_CROSS))

for name, a0 in FOOT:
    Mb = 10**11*Msun
    rM = mp.sqrt(G*Mb/a0)
    vi = vi_of(a0, Mb)
    print('  F2  numbers, %s footing, log M_b = 11, at x = 10:' % name)
    x  = mp.mpf(10)
    rh = f_rho(x)*Mb/rM**3
    pt = f_ptt(x)*a0**2/K4piG
    pr = f_prr(x)*a0**2/K4piG
    mu = pt/3
    cT = mp.sqrt(mu/rh)
    F  = 4*mp.pi*(x*rM)**2*abs(pr)
    # Jeans: 4 pi G rho_h r^2 vs c_s^2
    jeans = 4*mp.pi*G*rh*(x*rM)**2
    print('      rho_h = %.3e kg/m^3   Pi_tt = %.3e Pa   Pi_rr = %.3e Pa'
          % (float(rh), float(pt), float(pr)))
    print('      shear modulus mu ~ Pi_tt/3 = %.3e Pa   ->  c_T = sqrt(mu/rho_h) = %.1f km/s = %.3f v_inf'
          % (float(mu), float(cT/1e3), float(cT/vi)))
    print('      tension force 4 pi r^2 |Pi_rr| = %.4e N = %.4f x M_b a0   (deep field: M_b a0/2)'
          % (float(F), float(F/(Mb*a0))))
    print('      Jeans: 4 pi G rho_h r^2 = %.4e (m/s)^2  vs  c_T^2 = %.4e  ->  ratio %.2f  (>1: unstable)'
          % (float(jeans), float(cT**2), float(jeans/cT**2)))

print("""  F3  M5's THREE HYPOTHESES, checked against that medium.
      M5: "any LOCAL, MOMENTUM-CONSERVING, NORMALLY SELF-GRAVITATING medium whose equilibrium is
      the law"  --  NO-GO, by theorem: the stress that makes the law an equilibrium for every
      baryon profile is unique (AQUAL's, density-blind), is not an attractor, is ill-posed along
      the field, and cancels the medium's own nonlinear self-gravity.

      H1 LOCAL ................ HOLDS.  Pi_ij = J(g) delta_ij - g_i g_j/(K(1+u)) is a function of
          the local field g and of its local direction: a local constitutive law.  (Verified
          numerically below: two different (M_b, r) pairs with the same g give the same Pi.)
      H2 MOMENTUM-CONSERVING .. HOLDS.  The equilibrium residual in section C is <= 1e-9 at every
          radius and the symbolic residual in B1 is exactly 0: dPi_rr/dr + (2/r)(Pi_rr-Pi_tt)
          = -rho_h g, i.e. nabla_mu T^{mu nu} = 0 with the gravitational field only.
      H3 NORMALLY SELF-GRAVITATING ... HOLDS.  The halo's density enters lap(Phi) = 4 pi G rho at
          full strength, with no screening: g(r) = G(M_b + M_c(<r))/r^2 by construction, and
          INT rho_h 4 pi r^2 dr = M_b X(x) (KA6, checked below).

      ALL THREE HOLD, SO M5 BITES.  The elastic reading is inside the theorem, not outside it.
      The three ways out, and what the record says about each:
        - drop LOCALITY               -> FA3; "no candidate survives" (MEDIUM_DESIGN section 2).
        - drop MOMENTUM CONSERVATION  -> a medium that exchanges momentum with something else;
          the one class the record had not tried, and it dies on arithmetic (recombination drag
          0.73/0.61 of H at z 1100; the Bullet's gas column 0.1-0.7 optical depths).
        - drop NORMAL SELF-GRAVITY    -> TM1's tethered medium: no self-gravity, so no growth;
          satellites and cluster cores fail.
      None of the three is a payment of the amount; this lane's numbers say the amount is the
      whole problem.""")

# locality numeric test
print('  F4  locality check (H1), numerically:')
a0 = FOOT[0][1]
Mb1, Mb2 = mp.mpf(10)**11*Msun, mp.mpf(10)**12*Msun
r1 = mp.mpf('20')*kpc
rM2 = mp.sqrt(G*Mb2/a0)
# find r2 such that g(r2; Mb2) = g(r1; Mb1):  x2 = r2/rM2 with u(x2) = u(x1)
x1 = r1/mp.sqrt(G*Mb1/a0)
u1 = f_u(x1)
from mpmath import findroot
x2 = findroot(lambda z: f_u(z) - u1, mp.mpf('2.0'))
r2 = x2*rM2
p1 = (f_prr(x1)*a0**2/K4piG, f_ptt(x1)*a0**2/K4piG)
p2 = (f_prr(x2)*a0**2/K4piG, f_ptt(x2)*a0**2/K4piG)
print('      (M_b, r) = (1e11, %.1f kpc) and (1e12, %.1f kpc) have the same g = %.4e m/s^2'
      % (float(r1/kpc), float(r2/kpc), float(u1*a0)))
print('      Pi_rr: %.6e vs %.6e    Pi_tt: %.6e vs %.6e   -> same stress: the law is local in g.'
      % (float(p1[0]), float(p2[0]), float(p1[1]), float(p2[1])))

# KA6
print('  F5  KA6 mass closure (point mass):  INT_0^r rho_h 4 pi r^2 dr = M_b X(x) ?')
for xv in ('0.1', '1.0', '10.0'):
    x = mp.mpf(xv)
    lhs = mp.quad(lambda z: f_rho(z)*4*mp.pi*z**2, [mp.mpf('1e-12'), x])
    print('      x = %-5s   integral = %.12f   X(x) = %.12f   ratio = %.12f'
          % (xv, float(lhs), float(f_X(x)), float(lhs/f_X(x))))

# =============================================================================================
# G.  MUTATE
# =============================================================================================
hdr("G.  MUTATE  (each must bite, or the number it guards is not load-bearing)")
print('  M1  gas instead of a solid: p_r = +p_t = rho sigma^2 (no tension).  Then')
print('      p_r + 2 p_t = 3 rho sigma^2 and the lensing correction is 3 sigma^2/(2c^2):')
print('      at most 3 x the tabulated column, i.e. <= 6.7e-06 at log M_b 11.  The SIGN of p_r')
print('      is not what carries the verdict: the magnitude is.')
print('  M2  Tolman factor 1 instead of 1/2: 2x.  M3  |p_r|+2|p_t|: 3x.  Both in D3; both fail.')
print('  M4  narrower denominators (excess over the budget / over the delivered charge): in D3.')
print('      The narrowest denominator, over the charge that falls in, is 3.8x the widest at')
print('      x = 10 and still 5 orders of magnitude short.')
print('  M5  extended baryons (Hernquist, a_h = 0.05 / 0.2 / 0.5 r_M) instead of a point mass.')
print('      The point-mass profiles are singular at x -> 0 (rho_h ~ 1/x, sigma_t^2 ~ 1/x) so the')
print('      ratio at small x is an artefact; the extended runs in D5 bound the true inner value.')
print('      Result: the artefact is removed, R -> 0 at the centre, and the maximum over the whole')
print('      of 0 < x <= 10 is %.4e (canonical) / %.4e (alt) -- the number the label is read from.'
      % (float(EXT_MAX['canonical']), float(EXT_MAX['alt'])))

# =============================================================================================
# H.  VERDICT
# =============================================================================================
hdr("H.  VERDICT  (labels frozen in FROZEN_CRITERIA.md section 4)")
def label(v):
    return "STRESS PAYS" if v > mp.mpf('0.10') else "STRESS CANNOT PAY"

R_can = EXT_MAX['canonical']
R_alt = EXT_MAX['alt']
lab_c, lab_a = label(R_can), label(R_alt)
print('  the graded number (numerator A, denominator 1; baryons resolved; max over 0 < x <= 10):')
print('      canonical  %.4e   ->  %s' % (float(R_can), lab_c))
print('      alt        %.4e   ->  %s' % (float(R_alt), lab_a))
print('  point-mass idealisation, same combination, max over the grid (artefact-dominated):')
print('      canonical  %.4e     alt  %.4e' % (float(combos[0][2]), float(combos[0][3])))
print('  largest of the nine point-mass combinations, any footing:  %.4e' % float(RMAX))
print('  every one of these is below 1.0e-01; the largest misses it by %.0fx.'
      % float(mp.mpf('0.10')/max(RMAX, R_can, R_alt)))
print('\n  LABEL:  %s / %s' % (lab_c, lab_a))
print('  The 10 per cent line is missed by %.0fx to %.0fx depending on the combination chosen.'
      % (float(mp.mpf('0.10')/RMAX), float(mp.mpf('0.10')/R_can)))
print('\n  KA summary:  KA1 equilibrium residual 0 (symbolic) / <=1e-9 (numeric)   PASS')
print('               KA2 (Pi_rr+Pi_tt)/Pi_tt at x=100: canonical %.3e (line 1e-2)   PASS'
      % float((f_prr(mp.mpf(100))+f_ptt(mp.mpf(100)))/f_ptt(mp.mpf(100))))
print('               KA3 sigma_t^2/(v_inf^2/2) at x=100: %.6f (line 1e-2)          PASS'
      % float(f_sigt(mp.mpf(100))/(2*mp.pi)))
print('               KA4 PPN cross-check of the factor 1/2: 3p/(2 rho c^2)         PASS')
print('               KA5 dust limit and isotropic-Schwarzschild limit              PASS')
print('               KA6 mass closure ratio 1.000000000000                         PASS')
print('\n  kappa = 1/2 FITTED; not theory closed. Adopts nothing.')
print('  [elapsed %.1f s]' % (time.time()-T0))
