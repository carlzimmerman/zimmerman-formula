import csv, math, numpy as np
Ob, ODE = 0.0493, 0.6847; Rp, R0 = 5.364, 4.80
rows = list(csv.DictReader(open('../sonnet55_push/puzzle_32pi/p13c_desi_dr2_chains_a0z.csv')))
zg = np.linspace(0, 6, 6001)
def psi_shape(mode):
    if mode == 'M1': p = np.where(zg > 3, 1.0, 0.0)
    else: p = (1+zg)**2.6/(1+((1+zg)/2.6)**6.2)
    return p/np.trapz(p, zg)
def model(mode):
    psi = psi_shape(mode); dR = (Rp-R0)*psi                      # dR/dz > 0 (R falls toward today)
    Rz = R0 + np.concatenate([[0], np.cumsum(0.5*(dR[1:]+dR[:-1])*np.diff(zg))])  # R(z)
    w = (1+zg)**3 if mode != 'M2' else np.ones_like(zg)           # M2: no (1+z)^3 weighting
    inj = np.concatenate([[0], np.cumsum(0.5*((w*dR)[1:]+(w*dR)[:-1])*np.diff(zg))])  # rho_b0-units, injected by z..0
    rhoDE = ODE - Ob*inj                                          # true rho_DE(z)/rho_crit0 (conserved after injection)
    out = {}
    for anch, Rref in (('A today', R0), ('B early', Rp)):
        eff = rhoDE + Ob*(1+zg)**3*(Rz - Rref)                    # standard analysis: E^2 - Om_ref (1+z)^3
        out[anch] = eff
    return rhoDE, out
def band(fit, z, qs):
    r = [x for x in rows if x['fit'] == fit and abs(float(x['z'])-z) < 1e-6][0]
    return [float(r[q]) for q in qs]
for mode in ('base', 'M1', 'M2'):
    rhoDE, eff = model(mode)
    print('--- %s: true a0(z=2)/a0(0) = %.3f' % (mode, math.sqrt(rhoDE[int(2/6*6000)]/rhoDE[0])))
    for anch, e in eff.items():
        ratio = {z: math.sqrt(max(e[int(z/6*6000)]/e[0],0.0)) for z in (0.5, 1.0, 2.0)}
        s = '  %-8s model a0_eff ratios z=.5/1/2: %.3f %.3f %.3f' % (anch, ratio[0.5], ratio[1.0], ratio[2.0])
        ok_any = []
        for fit in sorted(set(r['fit'] for r in rows)):
            ok = all(band(fit, z, ('q025', 'q975'))[0] <= ratio[z] <= band(fit, z, ('q025', 'q975'))[1] for z in ratio)
            ok_any.append(ok)
        print(s, '| inside 95% for all three z in fits (CMB,DESY5,Pant+,Union3):', ok_any)
print('DESI bands (68%: q16-q84) a0/a0(0) at z=0.5,1,2:')
for fit in sorted(set(r['fit'] for r in rows)):
    print('  %-20s' % fit, [tuple(round(v, 3) for v in band(fit, z, ('q16', 'q84'))) for z in (0.5, 1.0, 2.0)])
