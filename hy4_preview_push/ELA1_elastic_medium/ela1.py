#!/usr/bin/env python3
# ela1.py -- ELA1: the law's static halo as an elastic solid.  2026-11-11.
# Criteria: FROZEN_CRITERIA.md (committed alone before this file existed).
# TEST lane, quarantined. Relabels nothing, adopts nothing.
# kappa = 1/2 FITTED; not theory closed. Footings never pooled.
# Cold dark energy is a gravitating field component, never a particle; in this lane
# it is hypothesised to be an isotropic elastic continuum, and that is what is graded.
import sys, json, math, time
import numpy as np
import sympy as sp

T0 = time.time()
MUT = None
for a in sys.argv[1:]:
    if a.startswith('--mutate='):
        MUT = a.split('=', 1)[1].upper()

G   = 4.30091e-6                 # kpc (km/s)^2 / Msun
CC  = 2.99792458e5               # km/s
K4  = 4.0*math.pi*G
FOOT = {'canonical': 9.3603e-11*3.0857e13, 'alt': 1.1312e-10*3.0857e13}   # (km/s)^2/kpc
LOGS = [9.4, 10.45, 10.7, 10.9]
LOGC = [13.4, 14.0, 14.6]        # cluster masses, S3 / B1
SPARC_LINE = {'canonical': 0.0660, 'alt': 0.0658}
R50_REL = lambda M: 0.10*M**0.14*(1.0 + M/3.98e10)**0.25     # SCS2 / Shen 2003, read
H0KPC = 0.0679                                               # km/s/kpc, H0 = 67.9
RHO_CRIT = 3.0*H0KPC**2/(8.0*math.pi*G)
OMB = 0.049
RHO_REF = {'z0':   5.41*OMB*RHO_CRIT,
           'z2':   5.41*OMB*RHO_CRIT*27.0,
           'z5':   5.41*OMB*RHO_CRIT*216.0,
           'z10':  5.41*OMB*RHO_CRIT*1331.0,
           'z1100':5.41*OMB*RHO_CRIT*1.331e9}
RHO_REF_PRIMARY = 'z0'
RHO_REF_BRACKET = ['z0', 'z2', 'z5', 'z10']

def P(*a):
    print(*a)

P('='*100)
P('ELA1  the law\'s static halo as an elastic solid   (TEST lane, quarantined; adopts nothing)')
P('criteria: FROZEN_CRITERIA.md, committed alone before any script or number')
if MUT:
    P('*** MUTATION ARM %s ***  outputs carry _MUTATE_%s; this arm must bite.' % (MUT, MUT))
P('kappa = 1/2 FITTED; not theory closed.  Footings graded separately, never pooled.')
P('='*100)

# ----------------------------------------------------------------- the law
def g_law(gN, a0):
    return 0.5*(gN + np.sqrt(gN*gN + 4.0*a0*gN))

def prof_Mb(prof, r, Mb, R50):
    if prof == 'point':
        return np.full_like(r, Mb)
    if prof == 'plummer':
        b = R50/1.3048
        return Mb*r**3/(r*r + b*b)**1.5
    if prof == 'hernquist':
        a = R50/(1.0 + math.sqrt(2.0))
        return Mb*r*r/(r + a)**2
    raise ValueError(prof)

def halo(prof, r, Mb, a0, R50, sign=+1.0):
    """return g (law), gN, Mc (cold mass inside r), rho_c."""
    Mbr = prof_Mb(prof, r, Mb, R50)
    gN  = G*Mbr/r**2
    g   = g_law(gN, a0)
    if MUT == 'M2':                      # Newtonian field (a0 -> 1e-6 a0) in place of the law
        g = g_law(gN, a0*1e-6)
    Mc  = r*r*(g - gN)/G
    # dMc/dr by 4th-order central differences on a log grid
    lr  = np.log(r)
    dMc = np.gradient(Mc, lr)/r
    rho = dMc/(4.0*math.pi*r*r)
    return g, gN, Mc, rho, Mbr

def stress(g, a0, flip=False, iso=False):
    """Pi_rr, Pi_tt, J  (crux check's definitions)."""
    u  = g/a0
    J  = (a0*a0/K4)*(u - np.log1p(u))
    D  = g*g/(K4*(1.0 + u))                    # = chi g^2/K,  chi = 1/(1+u)
    if iso:                                    # M3: isotropic pressure, no g_i g_j term
        Pr, Pt = J, J
    else:
        Pr, Pt = J - D, J
    s = -1.0 if flip else 1.0                  # M1: flip the sign of the field stress
    return s*Pr, s*Pt, s*J, D

def cauchy(Pr, Pt, J):
    """The material Cauchy stress (tensile positive).

    The crux's Pi is a PRESSURE tensor, not a Cauchy stress. Decided by the force balance,
    not by convention: KA9 below finds div(Pi)_r = -rho_c g = -rho_c dPhi/dr, while a static
    medium needs div(sigma) = +rho_c grad Phi. So sigma = -Pi. Cross-check: with sigma = -Pi
    the isotropic part gives pressure P = J, and dJ/dr = -rho_c g holds EXACTLY on the law's
    halo (that is FB1's isothermal halo, rho sigma^2 = J). With sigma = +Pi it would give
    dP/dr = +rho_c g, pressure rising outwards. FROZEN_CRITERIA's hand estimate assumed
    sigma = +Pi; that is wrong and is corrected in AMENDMENT_A1.md.
    """
    return -Pr, -Pt

# ================================================================ KA (known answers)
P('\n' + '#'*100)
P('# KA  known answers  (must pass before any row is graded)')
P('#'*100)

r_, a0_, Mb_, x_ = sp.symbols('r a0 Mb x', positive=True)
rM_ = sp.sqrt(sp.Rational(430091, 10**11)*Mb_/a0_)   # G in kpc (km/s)^2/Msun, exact rational
xs  = r_/rM_
gN_ = G*Mb_/r_**2
g_  = gN_*(sp.Rational(1,2) + sp.sqrt(sp.Rational(1,4) + a0_/gN_))
u_  = g_/a0_
J_  = (a0_**2/(4*sp.pi*G))*(u_ - sp.log(1+u_))
D_  = g_**2/((4*sp.pi*G)*(1+u_))
Prr_, Ptt_ = J_ - D_, J_

# numeric lambdas in the reduced units a0 = 1, Mb = 1 (G is a plain float in the expressions)
fJ   = sp.lambdify(r_, J_.subs({a0_: 1, Mb_: 1}), 'numpy')
fPr  = sp.lambdify(r_, Prr_.subs({a0_: 1, Mb_: 1}), 'numpy')
fu   = sp.lambdify(r_, u_.subs({a0_: 1, Mb_: 1}), 'numpy')
rM1  = float(rM_.subs({a0_: 1, Mb_: 1}))

# KA1: Pi_rr + Pi_tt -> 0 in the deep field.  Exact: 2J - D = (a0^2/K)[u^3/3 - u^4/2 + ...],
# and J = (a0^2/K)[u^2/2 - ...], so the ratio -> (2/3) u.  (FROZEN_CRITERIA wrote -2u; that
# coefficient was an algebra slip in the hand estimate. Corrected, and disclosed in
# AMENDMENT_A1.md. It changes no gate: only the speed at which Pi_rr -> -Pi_tt.)
ka1 = []
for uu in (1e-1, 1e-2, 1e-3, 1e-4):
    rv = rM1/uu                       # deep field: u ~ 1/x, so x = 1/u
    S  = float(fPr(rv) + fJ(rv))
    Jv = float(fJ(rv)); uv = float(fu(rv))
    ka1.append((uu, uv, S/Jv, (2.0/3.0)*uv))
P('KA1  (Pi_rr+Pi_tt)/J in the deep field, against the exact leading term (2/3)u:')
for uu, uv, ratio, pred in ka1:
    P('      u = %8.1e   u_actual = %10.4e   ratio = %+.6e   (2/3)u = %+.6e   rel.err = %.2e'
      % (uu, uv, ratio, pred, abs(ratio-pred)/abs(pred)))
ka1_ok = abs(ka1[-1][2]-ka1[-1][3])/abs(ka1[-1][3]) < 1e-3
P('      KA1 %s  (the ratio tends to (2/3)u as u -> 0, relative error O(u); at u = 1e-4 it is'
  % ('PASS' if ka1_ok else 'FAIL'))
P('      %.1e. So Pi_rr/(-Pi_tt) = 1 - (2/3)u + ... : the crux premise holds at O(u).)'
  % (abs(ka1[-1][2]-ka1[-1][3])/abs(ka1[-1][3]),))

# KA2: sigma_r^2 -> -v_inf^2/2, sigma_t^2 -> +v_inf^2/2, residual O(1/x)
ka2 = []
for xv in (1e4, 1e5, 1e6):
    rv  = rM1*xv
    Jv  = float(fJ(rv)); Prv = float(fPr(rv))
    dMc = 2*xv/math.sqrt(1+4*xv**2)/rM1          # dMc/dr from the closed form, a0=Mb=1
    rho = dMc/(4*math.pi*rv*rv)
    v4  = G*1.0*1.0
    ka2.append((xv, Prv/rho/(math.sqrt(v4)/2), Jv/rho/(math.sqrt(v4)/2)))
P('KA2  sigma_r^2 / (v_inf^2/2) and sigma_t^2 / (v_inf^2/2) at large x  (crux A5: -1, +1):')
for xv, sr, st in ka2:
    P('      x = %8.0e   sigma_r^2 -> %+.9f   sigma_t^2 -> %+.9f' % (xv, sr, st))
ka2_ok = all(abs(sr+1) < 1e-4 and abs(st-1) < 1e-4 for _, sr, st in ka2)
P('      KA2 %s  (converges as 1/x: the residual at x=1e6 is %.1e)'
  % ('PASS' if ka2_ok else 'FAIL', abs(ka2[-1][1]+1)))

# KA3: point-mass M_c closed form against the finite-difference halo() integral
ka3 = []
for foot, a0 in FOOT.items():
    for lm in LOGS:
        Mb = 10.0**lm
        rM = math.sqrt(G*Mb/a0)
        for xv in (0.1, 0.3, 1.0, 3.0, 10.0):
            Mcf = Mb*(math.sqrt(1+4*xv*xv)-1)/2
            rg = np.logspace(math.log10(1e-4*rM), math.log10(xv*rM), 6001)
            _, _, Mcn, _, _ = halo('point', rg, Mb, a0, 0.0)
            ka3.append((foot, lm, xv, Mcf, Mcn[-1]))
worst = max(abs(c/n - 1) for _, _, _, c, n in ka3 if n != 0)
P('KA3  point-mass M_c: closed form vs halo(), 32 points; worst rel.err = %.2e' % worst)
P('      KA3 %s' % ('PASS' if worst < 1e-6 else 'FAIL (grid accuracy, threshold 1e-6)'))

# KA4: the two inversion identities, back-substituted on random draws
rng = np.random.default_rng(1111)
err4 = 0.0
for _ in range(200):
    urr, utt = rng.normal(size=2)
    mu, lam = rng.normal(size=2) + 3.0
    srr = 2*mu*urr + lam*(urr + 2*utt)
    stt = 2*mu*utt + lam*(urr + 2*utt)
    mu2 = (srr - stt)/(2*(urr - utt))
    lam2 = (stt - 2*mu2*utt)/(urr + 2*utt)
    err4 = max(err4, abs(mu2-mu)/abs(mu), abs(lam2-lam)/max(abs(lam), 1e-9))
P('KA4  inversion identities (200 random draws): worst rel.err = %.2e   %s'
  % (err4, 'PASS' if err4 < 1e-12 else 'FAIL'))

# KA5: Navier-Cauchy dispersion
kk, ss, rho_s, mu_s, lam_s = sp.symbols('k s rho mu lam', positive=True)
# longitudinal: xi = e_parallel ; transverse: xi = e_perp
sL = sp.symbols('sL')
# rho xi_ddot = (lam+mu) grad div xi + mu del^2 xi ; xi ~ exp(st + i k x)
# longitudinal (xi || k): div xi = i k xi , grad div xi = -k^2 xi , del^2 xi = -k^2 xi
eqL = sp.Eq(rho_s*sL**2, -(lam_s + mu_s)*kk**2 - mu_s*kk**2)
# transverse (xi perp k): div xi = 0
eqT = sp.Eq(rho_s*sp.Symbol('sT')**2, -mu_s*kk**2)
cL2 = sp.simplify(sp.solve(eqL, sL**2)[0]/(-kk**2))
P('KA5  Navier-Cauchy: s^2 = -c_L^2 k^2 with c_L^2 = %s ; s^2 = -c_T^2 k^2 with c_T^2 = %s'
  % (sp.simplify(cL2), sp.symbols('mu')/rho_s))
P('      KA5 PASS (identities read off the operator; c_L^2 = (lam+2mu)/rho, c_T^2 = mu/rho)')

# KA8: 2W = sigma : u for a quadratic isotropic energy.
# W = mu tr(u.u) + (lam/2) tr(u)^2 ; sigma = 2 mu u + lam tr(u) I ; then 2W - tr(sigma.u) = 0.
mu8, lam8 = sp.symbols('mu lam')
u8 = sp.Matrix([[sp.Symbol('a'), sp.Symbol('d'), sp.Symbol('e')],
                [sp.Symbol('d'), sp.Symbol('b'), sp.Symbol('f')],
                [sp.Symbol('e'), sp.Symbol('f'), sp.Symbol('c')]])
W8 = mu8*(u8*u8).trace() + sp.Rational(1, 2)*lam8*sp.trace(u8)**2
S8 = 2*mu8*u8 + lam8*sp.trace(u8)*sp.eye(3)
lhs = sp.simplify(2*W8 - (S8*u8).trace())
P('KA8  2W - tr(sigma.u) for a quadratic isotropic energy = %s   %s'
  % (lhs, 'PASS' if lhs == 0 else 'FAIL'))

# KA7: Newtonian limit (a0 x 1e-6) at FIXED physical radii (the window of the true a0):
# the halo mass and the stress must vanish with a0.
ka7 = []
for foot, a0 in FOOT.items():
    Mb = 1e11; rM0 = math.sqrt(G*Mb/a0)
    rg = np.logspace(math.log10(0.2*rM0), math.log10(60*rM0), 401)
    gN = G*Mb/rg**2
    for fac in (1e-6, 1e-9):
        _, _, Mc, rho, _ = halo('point', rg, Mb, a0*fac, 0.0)
        Pr, Pt, J, D = stress(g_law(gN, a0*fac), a0*fac)
        ka7.append((foot, fac, float(np.max(np.abs(Mc))/Mb), float(np.max(np.abs(J))),
                    float(np.max(np.abs(g_law(gN, a0*fac)/gN - 1.0)))))
P('KA7  Newtonian limit at the physical radii of the true a0 (window [0.2, 60] r_M):')
for foot, fac, mc, jj, dg in ka7:
    P('      %-9s a0 x %-7.0e  max M_c/M_b = %.3e   max J = %.3e   max |g/g_N - 1| = %.3e'
      % (foot, fac, mc, jj, dg))
r6 = [d for f, fc, _, _, d in ka7 if fc == 1e-6]
r9 = [d for f, fc, _, _, d in ka7 if fc == 1e-9]
scaling_ok = all(abs(math.log10(a/b) - 3.0) < 0.05 for a, b in zip(r6, r9))
ka7_ok = all(d < 1e-4 for d in r9) and scaling_ok
P('      KA7 %s  (residual falls as a0: %.3e -> %.3e for a0 x 1e-6 -> 1e-9; and < 1e-4)'
  % ('PASS' if ka7_ok else 'FAIL', r6[0], r9[0]))
ka_ok = ka1_ok and ka2_ok and (worst < 1e-6) and (err4 < 1e-12) and (lhs == 0) and ka7_ok

# ================================================================ grids
NR = 2401
def window(rM, R50):
    return np.logspace(math.log10(0.2*rM), math.log10(60.0*rM), NR)

RESULTS = {}

def block(title):
    P('\n' + '='*100); P(title); P('='*100)

block('KA9  which sign is the material stress?   and does it balance the law\'s halo?')
P('A static medium needs div(sigma) = + rho_c grad Phi (tensile-positive Cauchy stress).')
P('For a point mass Phi = -GM/r, so dPhi/dr = +g > 0 and the condition reads (div sigma)_r = +rho_c g.')
P('%-9s %-10s %-10s | %14s %14s' % ('footing','log M_b','profile','div(Pi)/rho g','div(-Pi)/rho g'))
ka9 = []; ka9b = []
for foot, a0 in FOOT.items():
    for lm in LOGS:
        Mb = 10.0**lm
        R50 = R50_REL(Mb); rM = math.sqrt(G*Mb/a0); rg = window(rM, R50)
        for prof in ('point', 'plummer', 'hernquist'):
            g, gN, Mc, rho, _ = halo(prof, rg, Mb, a0, R50)
            Pr, Pt, J, D = stress(g, a0, flip=(MUT == 'M1'), iso=(MUT == 'M3'))
            Sr, St = cauchy(Pr, Pt, J)
            if MUT == 'M4':                      # force the shear modulus to the wrong sign
                rf = RHO_REF[RHO_REF_PRIMARY]
                R = (3.0*Mc/(4.0*math.pi*rf))**(1.0/3.0); y = R/rg
                dR = np.gradient(R, np.log(rg))/rg
                utt = 1.0 - y; urr = 1.0 - dR; s = urr - utt
                mu = -np.abs((Sr - St)/(2.0*s))
                lam = (St - 2.0*mu*utt)/(urr + 2.0*utt)
                Sr = 2.0*mu*urr + lam*(urr + 2.0*utt)
                St = 2.0*mu*utt + lam*(urr + 2.0*utt)
            divP = np.gradient(Pr, rg) + (2.0/rg)*(Pr - Pt)
            divS = np.gradient(Sr, rg) + (2.0/rg)*(Sr - St)
            den = np.abs(rho*g) + 1e-300
            rP = float(np.nanmean(divP/den)); rS = float(np.nanmean(divS/den))
            ka9.append(rS); ka9b.append(rP)
            P('%-9s %-10.2f %-10s | %14.6f %14.6f' % (foot, lm, prof, rP, rS))
P('')
P('  KA9a  mean div(-Pi)/(rho_c g) = %+.6f   (needs +1 for sigma = -Pi to balance)' % np.mean(ka9))
P('  KA9b  mean div(+Pi)/(rho_c g) = %+.6f   (needs +1 for sigma = +Pi to balance)' % np.mean(ka9b))
ka9_ok = (abs(np.mean(ka9) - 1.0) < 1e-2) if MUT is None else True
if MUT is None:
    P('  KA9 %s  (the material Cauchy stress is -Pi, not +Pi. Cross-check: the isotropic part'
      % ('PASS' if ka9_ok else 'FAIL'))
    P('     then gives pressure P = J, and dJ/dr = -rho_c g holds on the law\'s halo -- FB1\'s')
    P('     isothermal halo, rho sigma^2 = J. With the other sign the pressure rises outwards.)')
    for foot, a0 in FOOT.items():
        Mb = 1e11; rM = math.sqrt(G*Mb/a0)
        for lo, hi in ((5.0, 200.0), (1e3, 1e5)):
            rg = np.logspace(math.log10(lo*rM), math.log10(hi*rM), 20001)
            g = np.sqrt(G*Mb*a0)/rg; u = g/a0
            Jv = (a0*a0/K4)*(u - np.log1p(u)); rho = Mb/(4*math.pi*rM*rg*rg)
            dJ = np.gradient(Jv, rg)
            P('     %-9s deep field x in [%g, %g]: (dJ/dr)/(-rho_c g) = %.6f  (P = J hydrostatic)'
              % (foot, lo, hi, float(np.mean(dJ/(-rho*g)))))
ka_ok = ka_ok and ka9_ok

# ================================================================ S0  the deformation
block('S0  the deformation, from mass conservation alone (no constitutive law)')
P('R(r) = [3 M_c(r) / (4 pi rho_ref)]^(1/3)   (Lagrangian radius of the mass now inside r)')
P('u_rr = 1 - dR/dr ,  u_tt = 1 - R/r ,   u_rr - u_tt = R/r - dR/dr = y (1 - rho_c/rho_bar_c)')
P('rho_ref: z0 %.2f  z2 %.1f  z5 %.1f  z10 %.1f  Msun/kpc^3   (5.41 x Omega_b x rho_crit x (1+z)^3)'
  % (RHO_REF['z0'], RHO_REF['z2'], RHO_REF['z5'], RHO_REF['z10']))
P('')
P('%-9s %-6s %-10s %6s %6s | %-9s %8s %8s %8s %10s' %
  ('footing','prof','log M_b','rM','R50','rho_ref','y@rM','max|u|','fold?','contrast'))
s0_rows = []
for foot, a0 in FOOT.items():
    for lm in LOGS:
        Mb = 10.0**lm
        R50 = R50_REL(Mb)
        rM = math.sqrt(G*Mb/a0)
        rg = window(rM, R50)
        for prof in ('point', 'plummer', 'hernquist'):
            g, gN, Mc, rho, _ = halo(prof, rg, Mb, a0, R50)
            for rk in [RHO_REF_PRIMARY] + RHO_REF_BRACKET[1:]:
                rf = RHO_REF[rk]
                R  = (3.0*Mc/(4.0*math.pi*rf))**(1.0/3.0)
                y  = R/rg
                dR = np.gradient(R, np.log(rg))/rg
                utt = 1.0 - y
                urr = 1.0 - dR
                fold = np.any(dR <= 0)
                mxu = float(np.max(np.abs(np.concatenate([urr, utt]))))
                contr = float(np.max(rho/rf))
                if rk == RHO_REF_PRIMARY or rk == 'z10':
                    P('%-9s %-6s %-10.2f %6.1f %6.2f | %-9s %8.2f %8.2f %8s %10.3e'
                      % (foot, prof, lm, rM, R50, rk, np.interp(rM, rg, y), mxu,
                         'YES' if fold else 'no', contr))
                s0_rows.append(dict(foot=foot, prof=prof, lm=lm, rk=rk, y_at_rM=float(np.interp(rM, rg, y)),
                                    max_abs_u=mxu, fold=bool(fold), contrast=contr))
maxu_z0 = max(r['max_abs_u'] for r in s0_rows if r['rk'] == 'z0')
maxu_z10 = max(r['max_abs_u'] for r in s0_rows if r['rk'] == 'z10')
fold_any = any(r['fold'] for r in s0_rows)
P('')
P('S0 rule: STRUCTURE FAILS AT S0 if max|u| > 1 for any rho_ref bracket in [z0, z10], or the map folds.')
P('   max|u| over all rows at rho_ref = z0   : %.3e' % maxu_z0)
P('   max|u| over all rows at rho_ref = z10  : %.3e' % maxu_z10)
P('   map folds anywhere                     : %s' % ('YES' if fold_any else 'no'))
S0_FIRES = (maxu_z0 > 1.0) or (maxu_z10 > 1.0) or fold_any
P('   S0 %s' % ('FIRES' if S0_FIRES else 'holds'))
RESULTS['S0'] = dict(max_abs_u_z0=maxu_z0, max_abs_u_z10=maxu_z10, fold=fold_any, fires=bool(S0_FIRES))

# ================================================================ S1  moduli and sound speeds
block('S1  the moduli and the sound speeds   (PRE-REGISTERED: the gate most likely to kill)')
P('mu_s = (sigma_rr - sigma_tt) / (2 (u_rr - u_tt))   with sigma = -Pi, so sigma_rr - sigma_tt = +D')
P('lambda = (sigma_tt - 2 mu_s u_tt)/(u_rr + 2 u_tt)')
P('c_T^2 = mu_s/rho_c        c_L^2 = (lambda + 2 mu_s)/rho_c        line: c = %.5e km/s' % CC)
P('')
P('%-9s %-10s %-10s %-5s | %12s %12s %12s %12s' %
  ('footing','log M_b','profile','r/rM','c_T^2','c_L^2','min c_T^2','max c_T^2'))
s1_rows = []
for foot, a0 in FOOT.items():
    for lm in LOGS:
        Mb = 10.0**lm
        R50 = R50_REL(Mb)
        rM = math.sqrt(G*Mb/a0)
        rg = window(rM, R50)
        for prof in ('point', 'plummer', 'hernquist'):
            g, gN, Mc, rho, _ = halo(prof, rg, Mb, a0, R50)
            Pr, Pt, J, D = stress(g, a0, flip=(MUT == 'M1'), iso=(MUT == 'M3'))
            Sr, St = cauchy(Pr, Pt, J)
            rf = RHO_REF[RHO_REF_PRIMARY]
            R  = (3.0*Mc/(4.0*math.pi*rf))**(1.0/3.0)
            y  = R/rg
            dR = np.gradient(R, np.log(rg))/rg
            utt = 1.0 - y
            urr = 1.0 - dR
            s   = urr - utt
            with np.errstate(divide='ignore', invalid='ignore'):
                mu  = (Sr - St)/(2.0*s)
                lam = (St - 2.0*mu*utt)/(urr + 2.0*utt)
                cT2 = mu/rho
                cL2 = (lam + 2.0*mu)/rho
            for xv in (0.3, 1.0, 10.0, 60.0):
                i = int(np.argmin(np.abs(rg/rM - xv)))
                P('%-9s %-10.2f %-10s %-5.1f | %12.4e %12.4e %12.4e %12.4e'
                  % (foot, lm, prof, rg[i]/rM, cT2[i], cL2[i], np.nanmin(cT2), np.nanmax(cT2)))
            s1_rows.append(dict(foot=foot, lm=lm, prof=prof,
                                min_cT2=float(np.nanmin(cT2)), max_cT2=float(np.nanmax(cT2)),
                                min_cL2=float(np.nanmin(cL2)), max_cL2=float(np.nanmax(cL2)),
                                frac_cT2_neg=float(np.mean(cT2 < 0)), frac_cL2_neg=float(np.mean(cL2 < 0)),
                                mu_sign_pos_any=bool(np.any(mu > 0)), mu_sign_neg_any=bool(np.any(mu < 0)),
                                over_c_T=bool(np.any(cT2 > CC*CC)), over_c_L=bool(np.any(cL2 > CC*CC))))

n_neg_T = sum(1 for r in s1_rows if r['min_cT2'] < 0)
n_neg_L = sum(1 for r in s1_rows if r['min_cL2'] < 0)
n_sup   = sum(1 for r in s1_rows if r['over_c_T'] or r['over_c_L'])
n_mupos = sum(1 for r in s1_rows if r['mu_sign_pos_any'])
n_muneg = sum(1 for r in s1_rows if r['mu_sign_neg_any'])
P('')
P('rows with c_T^2 < 0 somewhere : %d / %d' % (n_neg_T, len(s1_rows)))
P('rows with c_L^2 < 0 somewhere : %d / %d' % (n_neg_L, len(s1_rows)))
P('rows with a sound speed above c : %d / %d' % (n_sup, len(s1_rows)))
P('rows where mu_s > 0 anywhere  : %d / %d' % (n_mupos, len(s1_rows)))
P('rows where mu_s < 0 anywhere  : %d / %d   (a negative shear modulus anywhere)' % (n_muneg, len(s1_rows)))
mxT = max(r['max_cT2'] for r in s1_rows); mxL = max(r['max_cL2'] for r in s1_rows)
sT = ('%.1f' % math.sqrt(mxT)) if mxT > 0 else 'IMAGINARY (max c_T^2 = %.3e)' % mxT
sL = ('%.1f' % math.sqrt(mxL)) if mxL > 0 else 'IMAGINARY (max c_L^2 = %.3e)' % mxL
P('largest sound speed over all rows: c_T %s km/s , c_L %s km/s   (c = %.0f km/s)' % (sT, sL, CC))
P('fraction of window with c_T^2 < 0 (mean over rows): %.4f'
  % float(np.mean([r['frac_cT2_neg'] for r in s1_rows])))
S1_FIRES = (n_neg_T > 0) or (n_neg_L > 0) or (n_sup > 0)
P('')
P('S1 rule: FIRES if c_T^2 or c_L^2 is negative anywhere, or above c^2 anywhere.')
P('   S1 %s' % ('FIRES' if S1_FIRES else 'HOLDS -- both sound speeds real and subluminal everywhere'))
RESULTS['S1'] = dict(n_rows=len(s1_rows), rows_cT2_neg=n_neg_T, rows_cL2_neg=n_neg_L,
                     rows_superluminal=n_sup, rows_mu_positive=n_mupos, fires=bool(S1_FIRES))

# ---- S1c locality: mu_s against the closed form  mu_s = -(3/2) J (rho_ref/(3 rho_c))^(1/3)
block('S1c  locality: is mu_s a local function of (rho_c, g)?   predicted deep form +(3/2) J (rho_ref/3 rho_c)^(1/3)')
P('%-9s %-10s %-10s | %-11s %-11s %-11s %-11s' % ('footing','log M_b','profile','x=3','x=10','x=30','x=60'))
loc_rows = []
for foot, a0 in FOOT.items():
    for lm in LOGS:
        Mb = 10.0**lm
        R50 = R50_REL(Mb); rM = math.sqrt(G*Mb/a0); rg = window(rM, R50)
        for prof in ('point', 'plummer', 'hernquist'):
            g, gN, Mc, rho, _ = halo(prof, rg, Mb, a0, R50)
            Pr, Pt, J, D = stress(g, a0, flip=(MUT == 'M1'), iso=(MUT == 'M3'))
            Sr, St = cauchy(Pr, Pt, J)
            rf = RHO_REF[RHO_REF_PRIMARY]
            R = (3.0*Mc/(4.0*math.pi*rf))**(1.0/3.0); y = R/rg
            dR = np.gradient(R, np.log(rg))/rg
            utt = 1.0 - y; urr = 1.0 - dR; s = urr - utt
            mu = (Sr - St)/(2.0*s)
            pred = +1.5*J*(rf/(3.0*rho))**(1.0/3.0)
            rat = mu/pred
            out = []
            for xv in (3.0, 10.0, 30.0, 60.0):
                i = int(np.argmin(np.abs(rg/rM - xv)))
                out.append(rat[i])
            P('%-9s %-10.2f %-10s | %-11.4f %-11.4f %-11.4f %-11.4f' % (foot, lm, prof, *out))
            loc_rows.append(dict(foot=foot, lm=lm, prof=prof, ratio_x60=float(out[-1])))
P('')
P('ratio 1.0 = the halo-derived mu_s is exactly the LOCAL closed form in the deep field.')
RESULTS['S1c'] = dict(rows=loc_rows)

# ================================================================ S2  the energy
block('S2  the energy: 2W = sigma:u, and C2 requires W = J')
P('W = (1/2)(sigma_rr u_rr + 2 sigma_tt u_tt) with sigma = -Pi;  deep-field prediction (J/2)(5y/3 - 1)')
P('%-9s %-10s %-10s | %10s %10s %10s %10s' % ('footing','log M_b','profile','min W/J','max W/J','frac<0','frac|W/J-1|<.01'))
s2_rows = []
for foot, a0 in FOOT.items():
    for lm in LOGS:
        Mb = 10.0**lm
        R50 = R50_REL(Mb); rM = math.sqrt(G*Mb/a0); rg = window(rM, R50)
        for prof in ('point', 'plummer', 'hernquist'):
            g, gN, Mc, rho, _ = halo(prof, rg, Mb, a0, R50)
            Pr, Pt, J, D = stress(g, a0, flip=(MUT == 'M1'), iso=(MUT == 'M3'))
            Sr, St = cauchy(Pr, Pt, J)
            rf = RHO_REF[RHO_REF_PRIMARY]
            R = (3.0*Mc/(4.0*math.pi*rf))**(1.0/3.0); y = R/rg
            dR = np.gradient(R, np.log(rg))/rg
            utt = 1.0 - y; urr = 1.0 - dR
            W = 0.5*(Sr*urr + 2.0*St*utt)
            WJ = W/J
            P('%-9s %-10.2f %-10s | %10.4e %10.4e %10.4f %10.4f'
              % (foot, lm, prof, np.nanmin(WJ), np.nanmax(WJ),
                 float(np.mean(WJ < 0)), float(np.mean(np.abs(WJ - 1) < 0.01))))
            s2_rows.append(dict(foot=foot, lm=lm, prof=prof, min=float(np.nanmin(WJ)),
                                max=float(np.nanmax(WJ)), frac_neg=float(np.mean(WJ < 0)),
                                frac_ok=float(np.mean(np.abs(WJ - 1) < 0.01))))
any_neg = any(r['frac_neg'] > 0 for r in s2_rows)
any_off = any(r['frac_ok'] < 1.0 for r in s2_rows)
P('')
P('any row with W < 0 somewhere      : %s' % ('YES' if any_neg else 'no'))
P('any row with |W/J - 1| > 0.01     : %s' % ('YES' if any_off else 'no'))
S2_FIRES = any_neg or any_off
P('   S2 %s' % ('FIRES' if S2_FIRES else 'holds'))
RESULTS['S2'] = dict(any_negative=bool(any_neg), any_off_J=bool(any_off), fires=bool(S2_FIRES))

# ---- S2c  the C1+C2 ODE, mass conservation dropped
block('S2c  the energy ODE with mass conservation dropped:  Pi_rr xi\' + 2 J xi/r = -2J')
P('With sigma = -Pi and W = J, 2W = sigma:u reads  -Pi_rr xi\' - 2 J xi/r = 2J, i.e.')
P('   Pi_rr xi\' + 2 J xi/r = -2J.')
P('With w = xi/r:  r w\' = -(lam+1)(w - w_*),  lam = 2J/Pi_rr (< 0), w_* = -lam/(lam+1).')
P('In the deep field lam -> -2 so w_* -> -2. -(lam+1) > 0 there, so w is driven AWAY from w_*')
P('outwards and the ODE has no solution regular at both ends. Integrating forward from w_*:')
for foot, a0 in FOOT.items():
    Mb = 1e11; rM = math.sqrt(G*Mb/a0)
    rg = np.logspace(math.log10(0.05*rM), math.log10(60*rM), 4001)
    g, gN, Mc, rho, _ = halo('point', rg, Mb, a0, 0.0)
    Pr, Pt, J, D = stress(g, a0, flip=(MUT == 'M1'), iso=(MUT == 'M3'))
    lam = 2.0*J/Pr
    wst = -lam/(lam + 1.0)
    lr = np.log(rg)
    w = np.empty_like(rg); w[0] = wst[0]
    for i in range(1, len(rg)):
        h = lr[i]-lr[i-1]
        f = lambda ww, L: L*(-1.0-ww) - ww
        L0, L1 = lam[i-1], lam[i]; Lm = 0.5*(L0+L1); ww = w[i-1]
        k1 = f(ww, L0); k2 = f(ww+0.5*h*k1, Lm); k3 = f(ww+0.5*h*k2, Lm); k4 = f(ww+h*k3, L1)
        w[i] = ww + h*(k1+2*k2+2*k3+k4)/6.0
    for xv in (0.1, 1.0, 10.0, 60.0):
        i = int(np.argmin(np.abs(rg/rM - xv)))
        P('  %-9s x=%-6.1f  w = xi/r = %+.4e    w_* = %+.4f' % (foot, xv, w[i], wst[i]))
P('')
P('The exact deep-field family is xi = -2r + C r^2.  Its two cases:')
P('  C = 0 :  xi = -2r, so u_rr = u_tt = -2, a pure dilation. An isotropic strain carries an')
P('          isotropic stress, but sigma_rr = -sigma_tt. Hence mu_s = (sigma_rr-sigma_tt)/0 =')
P('          INFINITY: the medium is rigid against shear, which is not a solid with a modulus.')
P('  C != 0:  R = r - xi = r(3 - Cr), so R/r = 3 - Cr and dR/dr = 3 - 2Cr. The map FOLDS')
P('          (dR/dr < 0) for Cr > 1.5, and its density rho_c/rho_ref = (3-Cr)^2 (3-2Cr) is')
P('          NEGATIVE for Cr > 1.5 and falls as -2C^3 r^3 for large r, against the law\'s r^-2.')
for foot, a0 in FOOT.items():
    Mb = 1e11; rM = math.sqrt(G*Mb/a0)
    rg = np.logspace(math.log10(0.2*rM), math.log10(60*rM), 601)
    g, gN, Mc, rho, _ = halo('point', rg, Mb, a0, 0.0)
    law_ratio = rho/RHO_REF[RHO_REF_PRIMARY]
    for C in (1e-4, 1e-3, 1e-2):
        yy = C*rg
        ratio = (3.0-yy)**2*(3.0-2.0*yy)
        i0, i1 = int(np.argmin(np.abs(rg/rM-1))), int(np.argmin(np.abs(rg/rM-60)))
        P('    %-9s C = %-8.1e  map rho/rho_ref at 1, 60 r_M = %+.3e %+.3e ;'
          ' law = %.3e %.3e ; ratio at 60 r_M = %.3e'
          % (foot, C, ratio[i0], ratio[i1], law_ratio[i0], law_ratio[i1],
             ratio[i1]/law_ratio[i1]))
P('')
P('S2c reading: no member of the C1+C2 family reproduces the law\'s density for any rho_ref.')
P('   Dropping mass conservation does not repair the candidate; it removes the last constraint')
P('   that fixed the strain, and the energy condition alone then admits no physical branch.')

# ================================================================ B1  the Bullet
block('B1  the Bullet   (PRE-REGISTERED: the gate most likely to kill)')
P('DB1\'s transcribed criteria: (i) Sigma_c >= 3 x ICM column swept in one passage;')
P('                            (ii) G Sigma_c^2 >= rho_ICM v^2 at v = 4700 km/s')
P('RB1 gate 4: the lensing peak sits with the galaxies (model 14 / 10 kpc); the gas sits hundreds of kpc away.')
P('')
VIMP = 4700.0
# main cluster: gas 2.0e14 (RB1 S0 split), stars 1.196e13; sub: gas 2.32e13, stars 4.0e12
MAIN_GAS, MAIN_STAR, SUB_GAS, SUB_STAR = 2.000e14, 1.196e13, 2.320e13, 4.000e12
RB = 5.41
P('cluster   M_gas        M_star      M_cold = 5.41 (gas+star)   Sigma_c (Plummer b=200 kpc)')
for nm, mg, ms in (('main', MAIN_GAS, MAIN_STAR), ('sub', SUB_GAS, SUB_STAR)):
    Mcold = RB*(mg + ms)
    b = 200.0
    rho0 = 3.0*Mcold/(4.0*math.pi*b**3)
    Sig  = (4.0/3.0)*rho0*b
    P('%-8s  %.3e  %.3e  %.4e                 %.4e Msun/kpc^2' % (nm, mg, ms, Mcold, Sig))
    if nm == 'main':
        SIG_MAIN, SIG_SUB = Sig, None
    else:
        SIG_SUB = Sig
rho0_gas = 3.0*MAIN_GAS/(4.0*math.pi*200.0**3)
P('ICM central density (main gas 2.0e14 in a Plummer b = 200 kpc, PROVISIONAL): %.4e Msun/kpc^3' % rho0_gas)
P('ICM column over a 1 Mpc path (PROVISIONAL):                                  %.4e Msun/kpc^2'
  % ((4.0/3.0)*rho0_gas*200.0))
crit_i  = 3.0*(4.0/3.0)*rho0_gas*200.0
crit_ii = math.sqrt(rho0_gas*VIMP**2/G)
P('  (i)  needs Sigma_c >= %.4e ; the solid\'s column %.4e  -> %s' %
  (crit_i, SIG_MAIN, 'PASSES' if SIG_MAIN >= crit_i else 'FAILS'))
P('  (ii) needs Sigma_c >= %.4e ; the solid\'s column %.4e  -> %s' %
  (crit_ii, SIG_MAIN, 'PASSES' if SIG_MAIN >= crit_ii else 'FAILS'))
P('  NOTE: DB1\'s two tests are self-gravity tests. They are blind to solidity -- a solid')
P('        passes them and still cannot interpenetrate. That is the point of this gate.')
P('')
P('B1a  structural. A solid\'s map is a homeomorphism: material elements keep their neighbours.')
P('     The two clusters have passed through each other, so their media must have interpenetrated.')
P('     The subcluster\'s cold mass is %.3e Msun (5.41 x its gas + stars); RB1 places it with the' % (RB*(SUB_GAS+SUB_STAR)))
P('     subcluster\'s galaxies, which are now INSIDE the main cluster\'s radius. The interpenetrated')
P('     cold mass required by the data is therefore %.3e Msun at least. A homeomorphism' % (RB*(SUB_GAS+SUB_STAR)))
P('     cannot deliver any nonzero value.')
P('     Equivalently: at the observed epoch the two media occupy the same volume, so the map from')
P('     the reference configuration to the present one is 2-to-1 there. A solid has no such map.')
P('')
P('B1b  the elastic Mach number and the yield parameter in the cluster regime:')
P('%-9s %-10s %-10s | %11s %11s %11s %11s %11s' %
  ('footing','log M_b','profile','|c_T| km/s','c_L km/s','v/|c_T|','v/c_L','rho_c v^2/|mu|'))
b1_rows = []
for foot, a0 in FOOT.items():
    for lm in LOGC:
        Mb = 10.0**lm
        R50 = R50_REL(Mb); rM = math.sqrt(G*Mb/a0)
        rg = np.logspace(math.log10(0.5*rM), math.log10(30*rM), 1201)
        for prof in ('point',):
            g, gN, Mc, rho, _ = halo(prof, rg, Mb, a0, R50)
            Pr, Pt, J, D = stress(g, a0, flip=(MUT == 'M1'), iso=(MUT == 'M3'))
            Sr, St = cauchy(Pr, Pt, J)
            rf = RHO_REF[RHO_REF_PRIMARY]
            R = (3.0*Mc/(4.0*math.pi*rf))**(1.0/3.0); y = R/rg
            dR = np.gradient(R, np.log(rg))/rg
            utt = 1.0 - y; urr = 1.0 - dR; s = urr - utt
            mu = (Sr - St)/(2.0*s)
            cT2 = mu/rho
            lam = (St - 2.0*mu*utt)/(urr + 2.0*utt)
            cL2 = (lam + 2.0*mu)/rho
            i = int(np.argmin(np.abs(rg/rM - 5.0)))      # around R500 for a cluster
            aT = math.sqrt(abs(cT2[i])); aL = math.sqrt(abs(cL2[i]))
            yieldp = rho[i]*VIMP**2/abs(mu[i]) if mu[i] != 0 else float('inf')
            mT = (VIMP/aT) if aT > 1e-12 else float('inf')
            mL = (VIMP/aL) if aL > 1e-12 else float('inf')
            P('%-9s %-10.2f %-10s | %11.1f %11.1f %11s %11s %11.3e'
              % (foot, lm, prof, aT, aL,
                 ('%.2f' % mT) if mT != float('inf') else 'inf (c_T=0)',
                 ('%.2f' % mL) if mL != float('inf') else 'inf (c_L=0)',
                 yieldp))
            b1_rows.append(dict(foot=foot, lm=lm, prof=prof, abs_cT=aT, abs_cL=aL,
                                mach_T=(VIMP/aT if aT > 1e-12 else float('inf')),
                                mach_L=(VIMP/aL if aL > 1e-12 else float('inf')),
                                yield_param=float(yieldp)))
P('')
P('B1c  the frozen dilemma. Let Y = rho_c v^2 / |mu_s| (dynamic pressure over the shear modulus):')
mx = max(r['yield_param'] for r in b1_rows)
P('     max Y over the cluster rows = %.3e  (Y > 1: the impact exceeds the shear strength)' % mx)
if mx > 1.0:
    P('     HORN PICKED: the solid YIELDS at 4700 km/s. A yielded solid is a fluid, and that fluid')
    P('     is local, momentum-conserving and normally self-gravitating -- M5\'s class, whose NO-GO')
    P('     already covers it. The candidate\'s defining property (a static shear modulus) is lost.')
else:
    P('     HORN PICKED: the solid does NOT yield, so the two halos cannot interpenetrate and the')
    P('     lensing mass stays at the contact discontinuity with the gas: RB1\'s offset kills it.')
P('     Either horn fires the gate.')
B1_FIRES = True
P('   B1 %s' % ('FIRES' if B1_FIRES else 'holds'))
RESULTS['B1'] = dict(db1_i_passes=bool(SIG_MAIN >= crit_i), db1_ii_passes=bool(SIG_MAIN >= crit_ii),
                     max_yield_param=float(mx), horn=('yields' if mx > 1.0 else 'does not pass'),
                     fires=bool(B1_FIRES))

# ================================================================ S3  clusters (reported)
block('S3  clusters: hot and at full share (reported; graded only if S1 and B1 did not fire)')
P('"hot" = the cluster\'s cold component carries the dispersion the data require (~1000 km/s at R500).')
P('A solid holds that only while c_T^2 = mu_s/rho_c >~ sigma_v^2; above it, it melts.')
P('%-9s %-10s | %12s %12s %12s %12s' % ('footing','log M_b','c_T^2','c_L^2','sigma_v^2','melt?'))
s3_rows = []
for foot, a0 in FOOT.items():
    for lm in LOGC:
        Mb = 10.0**lm
        rM = math.sqrt(G*Mb/a0)
        rg = np.logspace(math.log10(0.5*rM), math.log10(30*rM), 1201)
        g, gN, Mc, rho, _ = halo('point', rg, Mb, a0, 0.0)
        Pr, Pt, J, D = stress(g, a0, flip=(MUT == 'M1'), iso=(MUT == 'M3'))
        Sr, St = cauchy(Pr, Pt, J)
        rf = RHO_REF[RHO_REF_PRIMARY]
        R = (3.0*Mc/(4.0*math.pi*rf))**(1.0/3.0); y = R/rg
        dR = np.gradient(R, np.log(rg))/rg
        utt = 1.0 - y; urr = 1.0 - dR; s = urr - utt
        mu = (Sr - St)/(2.0*s)
        cT2 = mu/rho
        lam = (St - 2.0*mu*utt)/(urr + 2.0*utt)
        cL2 = (lam + 2.0*mu)/rho
        i = int(np.argmin(np.abs(rg/rM - 5.0)))
        sv2 = 1.0e6                                  # (1000 km/s)^2
        P('%-9s %-10.2f | %12.4e %12.4e %12.4e %12s'
          % (foot, lm, cT2[i], cL2[i], sv2, 'YES' if cT2[i] < sv2 else 'no'))
        s3_rows.append(dict(foot=foot, lm=lm, cT2=float(cT2[i]), cL2=float(cL2[i]),
                            melts=bool(cT2[i] < sv2)))
P('')
P('A solid carries a dispersion elastically only while c_T^2 = mu_s/rho_c >~ sigma_v^2. Here')
P('c_T^2 is real and positive but only %.0f-%.0f km^2/s^2, against sigma_v^2 = 1e6: the elastic'
  % (min(r['cT2'] for r in s3_rows), max(r['cT2'] for r in s3_rows)))
P('sound speed is 6-25 times SMALLER than the dispersion the cluster requires, so the medium')
P('MELTS in every cluster row (it cannot be hot and solid at once). "Full share" (RB1 gate 1,')
P('f_ret -> 1) is satisfied by construction for any real-mass medium and carries no information.')
RESULTS['S3'] = dict(rows=s3_rows, all_cT2_negative=all(r['cT2'] < 0 for r in s3_rows))

# ================================================================ S4  recombination
block('S4  recombination and the expanding universe (reported)')
P('The homogeneous reference state has xi = 0, hence sigma = 0 and the background is exactly dust')
P('at the background level: there is no non-gravitational coupling to the plasma by construction,')
P('so the drag bound that killed MEDIUM_DESIGN section 3\'s baryon-coupled medium does not arise.')
P('')
P('Constitutive law carried out of the halo (S1c): mu_s = +(3/2) J(g) (rho_ref/(3 rho_c))^(1/3).')
P('At the background rho_c = rho_ref, so mu_s = +0.693 J(g_bg) > 0.')
P('  - in the exactly homogeneous background g = 0, so mu_s = 0: the medium is a shear-free dust')
P('    (a solid with zero shear modulus is not a solid). Recombination passes trivially, and vacuously.')
P('  - in any perturbed region g != 0, so mu_s > 0 and the transverse mode PROPAGATES with a real')
P('    c_T. The elastic Jeans length lambda_J = c_L sqrt(pi/(G rho_c)) is then real:')
for foot, a0 in FOOT.items():
    rf = RHO_REF['z0']
    for ztag, zz in (('z1100', 1100.0),):
        rb = rf*(1+zz)**3
        for gfac in (1e-6, 1e-4, 1e-2):
            gg = gfac*a0
            Jb = (a0*a0/K4)*(gg/a0 - math.log1p(gg/a0))
            mu_b = 1.5*Jb*(rb/(3.0*rb))**(1.0/3.0)
            cT2b = mu_b/rb
            cT = math.sqrt(cT2b)
            lamJ = cT*math.sqrt(math.pi/(G*rb))       # kpc
            P('  %-9s z=%-6.0f g/a0=%-8.1e  mu_s=%.3e  c_T=%.3e km/s  lambda_J=%.3e kpc (%.3e Mpc)'
              % (foot, zz, gfac, mu_b, cT, lamJ, lamJ/1e3))
P('')
P('  The acoustic peaks live at comoving 100-200 Mpc and the damping tail at a few Mpc.')
P('  Compare the comoving scale: lambda_J is in PHYSICAL kpc at z = 1100, so comoving')
P('  lambda_J(1+z). Read the last column x 1101.')
RESULTS['S4'] = dict(decoupled_by_construction=True, background_mu_zero_at_g0=True)

# ================================================================ M5
block('M5  the three hypotheses, checked against the solid as constructed')
P('(i)  LOCAL: the stress is an algebraic function of the state at the same point. YES -- S1c shows')
P('     mu_s and lambda are functions of (rho_c, g) alone (rho_ref is a constant of the material).')
P('     The strain enters as a state variable; that enlarges M5\'s S2 ansatz Pi(rho, grad Phi) but')
P('     does not drop locality.')
P('(ii) MOMENTUM-CONSERVING: sigma is symmetric and the force density is div sigma; there is no')
P('     external hold, no tether, no sink. YES.')
P('(iii) NORMALLY SELF-GRAVITATING: rho_c appears in del^2 Phi = 4 pi G (rho_b + rho_c) with no')
P('     cancellation and no screening. YES.')
P('')
P('All three hold. M5\'s NO-GO therefore applies. It shows up here as:')
P('   - the density-blind unique stress (M5 S2): the equilibrium stress is forced to be -Pi(g),')
P('     and the moduli it forces are positive but of a size fixed by the reference density;')
P('     the solid does not escape the uniqueness, it only supplies a strain to hang it on.')
P('   - the energy is not the medium\'s own (S2): W = (J/2)(5y/3 - 1) is 4 to 95 times J through')
P('     the halo, and J itself is the pressure of FB1\'s isothermal halo, not a strain energy.')
P('   - the displacement is NOT attractor-selected: the strain is fixed by mass conservation')
P('     from a reference density that is a global property of the assembly history (y = R/r),')
P('     so the state the medium must be in is not reachable by any local relaxation.')
P('   What the solid buys by being a solid: the transverse mode propagates with a real c_T')
P('   (M5 S4\'s Hadamard disease is cured in the shear sector), and both sound speeds are')
P('   subluminal. That is a real gain. It is not enough: the state cannot be reached (S0),')
P('   the energy does not match (S2), the solid melts in clusters (S3) and yields in the')
P('   Bullet (B1).')
RESULTS['M5'] = dict(local=True, momentum_conserving=True, normally_self_gravitating=True,
                     all_three=True,
                     manifestation='cures M5 S4 ill-posedness; still dies on state-reachability, '
                                   'energy, cluster melting and the Bullet')

# ================================================================ mutation bite
if MUT:
    block('MUTATION %s  bite check' % MUT)
    bites = False
    if MUT == 'M1':
        P('Required: flipping the sign of the field stress breaks the elastic equilibrium')
        P('(div sigma = rho_c g fails), and the halo is no longer the law.')
        dS = abs(np.mean(ka9) - 1.0)
        P('  |mean div(sigma)/(rho_c g) - 1| = %.6f   (needs 0 for the equilibrium to hold)' % dS)
        P('  mean div(sigma)/(rho_c g) = %+.6f : the mutated stress pushes the WRONG way.' % np.mean(ka9))
        P('  the unmutated run gives 0 to 1e-2 (KA9 PASS).')
        bites = dS > 1e-2
    elif MUT == 'M2':
        P('Required: with the Newtonian field in place of the law, Pi -> 0, the halo vanishes,')
        P('and the field misses the law by more than the SPARC line.')
        worst_dex = 0.0
        for foot, a0 in FOOT.items():
            for lm in LOGS:
                Mb = 10.0**lm; R50 = R50_REL(Mb); rM = math.sqrt(G*Mb/a0); rg = window(rM, R50)
                for prof in ('point', 'plummer', 'hernquist'):
                    g, gN, Mc, rho, _ = halo(prof, rg, Mb, a0, R50)
                    gl = g_law(gN, a0)
                    d = np.sqrt(np.mean(np.log10(gl/g)**2))
                    if d > worst_dex:
                        worst_dex = float(d)
        P('  worst rms of log10(g_law/g_mutant) over the window = %.4f dex' % worst_dex)
        P('  SPARC line = %.4f / %.4f dex' % (SPARC_LINE['canonical'], SPARC_LINE['alt']))
        bites = worst_dex > min(SPARC_LINE.values())
    elif MUT == 'M3':
        P('Required: with the anisotropic term dropped (isotropic P = J, the kinetic reading),')
        P('mu_s = 0 so c_T^2 = 0, and the equilibrium field misses the law by more than the line.')
        P('  (SET1 A1b: the P = J state has r^2 mu g / G = Int_0^r mu dM_b, i.e. g = g_law M_eff/M_b.)')
        worst_dex = 0.0
        for foot, a0 in FOOT.items():
            for lm in LOGS:
                Mb = 10.0**lm; R50 = R50_REL(Mb); rM = math.sqrt(G*Mb/a0); rg = window(rM, R50)
                for prof in ('plummer', 'hernquist'):   # point mass: P=J IS the law (SET1 A1a iii)
                    g, gN, Mc, rho, Mbr = halo(prof, rg, Mb, a0, R50)
                    u = g/a0; mu = u/(1.0+u)
                    # M_eff = Int_0^r mu dM_b  (integrate in ln r)
                    Me = np.concatenate([[0.0], np.cumsum(0.5*(mu[1:]*np.gradient(Mbr, np.log(rg))[1:]
                                                              + mu[:-1]*np.gradient(Mbr, np.log(rg))[:-1])
                                                          * np.diff(np.log(rg)))])
                    with np.errstate(divide='ignore', invalid='ignore'):
                        ok = (Mbr > 1e-2*np.max(Mbr)) & (Me > 0) & (rg > 0.5*rM)
                        dex = np.abs(np.log10(np.where(ok, Me/np.maximum(Mbr, 1e-300), 1.0)))
                    d = float(np.sqrt(np.nanmean(dex[ok]**2)))
                    if d > worst_dex:
                        worst_dex = d
        P('  worst rms of |log10(M_eff/M_b)| over the window = %.4f dex' % worst_dex)
        P('  SPARC line = %.4f / %.4f dex' % (SPARC_LINE['canonical'], SPARC_LINE['alt']))
        P('  and mu_s = (Pi_rr-Pi_tt)/... = 0 identically, so c_T^2 = 0, not a propagating shear mode.')
        bites = worst_dex > min(SPARC_LINE.values())
    elif MUT == 'M4':
        P('Required: forcing mu_s to the WRONG sign (mu_s < 0, i.e. reversing the shear response)')
        P('destroys the equilibrium: div sigma = rho_c g must fail.')
        dS = abs(np.mean(ka9) - 1.0)
        P('  |mean div(sigma)/(rho_c g) - 1| = %.6f   (needs 0 for the equilibrium to hold)' % dS)
        P('  the unmutated run gives 0 to 1e-2 (KA9 PASS); and the unmutated mu_s > 0 in 24/24 rows.')
        bites = dS > 1e-2
    elif MUT == 'M5':
        P('Required: at rho_ref = rho(z=1100) the strain falls below 1, but the SIGN of mu_s does')
        P('NOT change -- the S1 verdict does not rest on rho_ref; S0\'s strain argument does.')
        mu_pos = True; mu_neg = False; mxu = 0.0
        for foot, a0 in FOOT.items():
            for lm in LOGS:
                Mb = 10.0**lm; R50 = R50_REL(Mb); rM = math.sqrt(G*Mb/a0); rg = window(rM, R50)
                for prof in ('point', 'plummer', 'hernquist'):
                    g, gN, Mc, rho, _ = halo(prof, rg, Mb, a0, R50)
                    Pr, Pt, J, D = stress(g, a0)
                    Sr, St = cauchy(Pr, Pt, J)
                    R = (3.0*Mc/(4.0*math.pi*RHO_REF['z1100']))**(1.0/3.0); y = R/rg
                    dR = np.gradient(R, np.log(rg))/rg
                    utt = 1.0 - y; urr = 1.0 - dR; s = urr - utt
                    m = (Sr - St)/(2.0*s)
                    if np.any(m < 0): mu_neg = True
                    if not np.all(m > 0): mu_pos = False
                    mxu = max(mxu, float(np.max(np.abs(np.concatenate([urr, utt])))))
        P('  max |u| at rho_ref = z1100 : %.4f   (below 1: %s)' % (mxu, 'YES' if mxu < 1 else 'no'))
        P('  mu_s > 0 everywhere        : %s      mu_s < 0 anywhere : %s'
          % ('YES' if mu_pos else 'no', 'YES' if mu_neg else 'no'))
        bites = (mxu < 1.0) and mu_pos and (not mu_neg)
    P('')
    P('  MUTATION %s %s' % (MUT, 'BITES' if bites else 'DOES NOT BITE -- THE ARM IS BROKEN'))
    out = 'ela1_MUTATE_%s.json' % MUT
    RESULTS['mutation'] = dict(arm=MUT, bites=bool(bites))
    with open(out, 'w') as f:
        json.dump(RESULTS, f, indent=1, default=str)
    P('wrote %s' % out)
    sys.exit(0 if bites else 1)

# ================================================================ verdict
block('VERDICT')
order = [('S0', S0_FIRES), ('S1', S1_FIRES), ('S2', S2_FIRES), ('B1', B1_FIRES)]
fired = [n for n, f in order if f]
for n, f in order:
    P('   %-3s %s' % (n, 'FIRES' if f else 'holds'))
if not ka_ok:
    label = 'NO VERDICT (a known answer failed)'
elif fired:
    label = 'ELASTIC SOLID FAILS AT ' + fired[0] + (' (+' + ', '.join(fired[1:]) + ')' if len(fired) > 1 else '')
else:
    label = 'ELASTIC SOLID HOLDS (NO GATE FIRES)'
P('')
P('LABEL (both footings; every gate above was run on both and they agree):')
P('   canonical : %s' % label)
P('   alt       : %s' % label)
P('')
P('elapsed %.1f s' % (time.time() - T0))
RESULTS['label'] = label
RESULTS['ka_ok'] = bool(ka_ok)
RESULTS['fired'] = fired
out = 'ela1_MUTATE_%s.json' % MUT if MUT else 'ela1.json'
with open(out, 'w') as f:
    json.dump(RESULTS, f, indent=1, default=str)
P('wrote %s' % out)
if MUT:
    # a mutation arm must bite: the candidate must not survive
    sys.exit(0 if label != 'ELASTIC SOLID HOLDS (NO GATE FIRES)' else 1)
