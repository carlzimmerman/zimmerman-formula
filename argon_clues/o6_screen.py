"""argon_clues O6: parameter-origin screen. (1) dimensional analysis of the open constants; (2) the rescaling/zero-mode test every coefficient-selection route must pass;
(3) sensitivity of the downstream numbers to each input. Inputs from committed results only."""
import json, math, sympy as sp
# 1. Buckingham: variables a0, c, G, rho_DE in (L, T, M)
dims = {'a0':(1,-2,0),'c':(1,-1,0),'G':(3,-2,-1),'rho':(-3,0,1)}
M = sp.Matrix([dims[k] for k in dims]).T            # columns = variables
ns = M.nullspace()
print('1. dimensionless groups of (a0, c, G, rho_DE): %d  -> exponents %s  (order: a0,c,G,rho)'%(len(ns),[list(v.T) for v in ns]))
print('   => a0/(c sqrt(G rho_DE)) = kappa is the ONLY dimensionless number. A derivation of a0 is a derivation of one pure number; dimensional analysis alone cannot supply it.')
# add L*, R0: L* carries length, a0 L*/c^2... variables (a0,c,G,rho,L*)
dims2=dict(dims); dims2['Lstar']=(1,0,0)
M2=sp.Matrix([dims2[k] for k in dims2]).T; print('   with L* added: %d groups; second group: L* * a0/c^2 or L*/(c/sqrt(G rho))  (the stiffness length in Hubble-ish units: %.2e)'%(len(M2.nullspace()),5.75*3.0857e16*9.36e-11/(2.998e8)**2))
# 2. rescaling / zero-mode screen
print('\n2. SCREEN every proposed selection route R(kappa) against: (a) static scale covariance (Lean: scale_gN/scale_tether/scale_nu); (b) a continuous vacuum-offset family (sol61 open_items item 4).')
print('   A route passes only if its output is NOT invariant under (g,a0)->(lam g, lam a0) AND it contains rho_DE or Lambda and c in its inputs. Static-class routes fail (a) by construction: they contain neither.')
routes = {'hemisphere average (1/2)': 'typed pairing (a0 = <cos> c sqrt(K/4pi rho))','Komar/Gauss 1/2':'ratio of two normalisations','Galileo drift (lambda=1)':'cross-term coefficient inserted','S2 orientation':'projection x solid angle chosen','Deser-Levin / horizon routes':'give cH x rational (floor a0/2 => 2Z off)','Friedmann conversion':'identity, moves the gate scale choice (sqrt(G rho) vs H)'}
for r,why in routes.items(): print('   %-30s fails the screen: %s'%(r,why))
# 3. inventory with committed numbers
c493=None
print('\n3. INVENTORY (status labels: DERIVED / MEASURED / BOUNDED / SELECTED)')
rows=[('kappa (a0/c sqrt(G rho_DE))','MEASURED (and posited = 1/2)','CFG493 GLS: 0.417 +- 0.095 (canonical), 0.345 +- 0.078 (alt); 1/2 at 0.80 / 1.63 sigma; floor 9.3% from shared systematics; kernel choice moves it +0.06-0.09 dex','no derivation survives: Lean no-go (static class), sol61 continuous offset family, 10+ audited routes'),
      ('Omega_c/Omega_b = R0','MEASURED','5.364 (CMB; native 5.376); census: no net conversion > 2.3% of cold energy (CFG779, cold_to_baryon.py)','dust equations preserve any initial ratio (sol61 item 5): needs an independently normalised production history'),
      ('L* (stiffness length)','BOUNDED','>= 5.75 pc (Saturn bound, CFG691); SPARC fine to >= 1 kpc; GC X2 minimum ~25 pc (4 clusters); UFD median cost +0.03 / +0.08 / +0.16 / +0.30 dex at 5.75 / 10 / 15 / 25 pc; Gaia DR4: boost (1/2)(s/L*)^2','joint window ~10-15 pc if globulars and UFDs are both taken at face value; no derivation'),
      ('gamma','tied to L*','gamma = K L*^2/2 (canonical theory)','inherits L*'),
      ('a0 footing (Lambda vs rho_crit)','SELECTED (declared)','9.36e-11 vs 1.13e-10 m/s^2, both reported','footing is a convention for kappa = 1/2; never pooled'),
      ('basin / no-EFE rule','SELECTED (data-forced)','satellite lensing: no-EFE chi2 0.7 vs EFE 99.5 (PAPER44)','no local action derives it (Stueckelberg, transport, scalar potential all fail)'),
      ('free fraction (2/3 of R0 f_hot)','SELECTED','level matches X-COP median (0.05-0.08 dex), rank test fails (rho 0.46-0.48, p 0.12-0.13)','mechanism for the partition not derived')]
for r in rows: print('   - %-32s %-30s\n       evidence: %s\n       derivation status: %s'%r)
# 4. sensitivities
print('\n4. SENSITIVITY of downstream numbers')
print('   k = (2/3) R0 f_hot: dk/k = dR0/R0 (1:1); R0 5.364 -> 4.80 moves the X-COP level by 0.048 dex.')
print('   a0 ~ kappa: GLS 1-sigma 25 percent in kappa = 0.099 dex; the sealed ALMA gas predictions shift ~ (0.5-1) x that in log M_gas (CFG571 note: stellar-mass branch moves them 0.6 dex).')
print('   L* in [5.75, 25] pc: UFD median +0.03 -> +0.30 dex; GC X2 8.5 -> 3.1; Solar System excludes < 5.75.')
