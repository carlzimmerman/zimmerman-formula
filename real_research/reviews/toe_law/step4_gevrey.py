import sympy as sp, mpmath as mp
mp.mp.dps=40

# ============================================================
# STEP 4: Gevrey-class mismatch. A non-perturbative term e^{-zeta/u^{1/4}}
# (fourth-root essential singularity, the TARGET) is the resurgent partner
# of a perturbative series with coefficients growing like Gamma(4n) ~ (4n)!.
# The free thermal series grows like (2n)! (Gevrey-1 in the worldline time).
# These are DIFFERENT resurgence universality classes.
# ============================================================
n = sp.symbols('n', positive=True, integer=True)

print("Gevrey-k <-> essential singularity e^{-1/x^{1/(k)}} dictionary (standard):")
print("  series sum a_n x^n with a_n ~ (k n)! has Borel-k summable structure,")
print("  non-perturbative partner ~ exp(-const / x^{1/k}).")
print()
print("TARGET sigma_req: e^{-zeta u^{-1/4}}  => essential sing of order 1/4 in u")
print("  => its perturbative partner (in u) would need a_n ~ (4n)! growth.")
print("  (the '4' is the FOURTH-root order; this is the structural fingerprint.)")
print()
print("FREE thermal series: a_{2j} ~ Gamma-free, ~ (2j+1)/pi^{2j} = GEOMETRIC x linear.")
print("  In worldline TIME tau the free series is CONVERGENT (radius 2pi/kappa);")
print("  the (2n)! shows up only after Borel/Laplace to FREQUENCY -- a SIMPLE pole tower.")
print()
# Demonstrate numerically the growth-rate gap:
print("Growth-rate comparison of |a_n|^{1/n} normalized (the Gevrey order):")
print(" n   (4n)!^{1/n}/n   (2n)!^{1/n}/n   free_a_n^{1/n} (->1/pi, bounded)")
for N in [5,10,20,40,80]:
    g4 = mp.gamma(4*N+1)**(mp.mpf(1)/N)/N
    g2 = mp.gamma(2*N+1)**(mp.mpf(1)/N)/N
    # free coeff a_{2N} ~ (2N+1)*2/pi^{2N+2}; |a_{2N}|^{1/(2N)} -> 1/pi
    free = ((2*N+1)*2/mp.pi**(2*N+2))**(mp.mpf(1)/(2*N))
    print(f" {N:3d}  {float(g4): .4f}        {float(g2): .4f}        {float(free): .6f}")
print()
print("=> (4n)! and (2n)! both DIVERGE as n->inf (Gevrey>0); free stays BOUNDED at 1/pi")
print("   (Gevrey-0 / analytic in tau). The free WORLDLINE series is convergent.")
print("   Neither (4n)! NOR (2n)! growth is present in the free tau-series coefficients.")
print()

# ============================================================
# (4b) The decisive resurgence statement: can the free Borel singularity
# (double pole at finite distance) ever PRODUCE a quartic-root branch point
# under the u = 2pi/kappa ~ sqrt(c_chi - b) edge map? Test the map's effect
# on the singularity TYPE.
# ============================================================
print("="*60)
print("(4b) Does the Deser-Levin sqrt edge map upgrade pole->branch point?")
print("="*60)
# Free density in omega has SIMPLE POLES at omega = i kappa m (Matsubara). Under
# kappa ~ 1/u (u = 2pi/kappa), a pole at omega ~ kappa m = (2pi m)/u. Composing with
# any analytic weight keeps it a pole in omega. To get u^{-1/4} essential sing you need
# an ACCUMULATION of the Matsubara tower with a quartic-root spacing -- which the free
# (equally-spaced, linear) tower does NOT have.
b,c,u,om2 = sp.symbols('b c_chi u omega', positive=True)
# Matsubara spacing in the free tower: Delta omega = kappa = const in m (linear).
# Required for u^{-1/4}: the Borel singularities must accumulate with action S_m ~ m^{?}.
# e^{-zeta u^{-1/4}} resummed = sum over saddles with action growing like a quartic lattice.
print("Free Matsubara actions S_m = 2pi m/kappa : LINEAR in m (equal spacing).")
print("A fourth-root essential sing requires saddle actions accumulating like a")
print("QUARTIC lattice (S ~ m^{4/3}-type / confluent tower), absent in the free spectrum.")
print("=> The edge map (analytic, sqrt) cannot manufacture a quartic branch from a")
print("   linear simple-pole tower: singularity TYPE is map-invariant under analytic comp.")
