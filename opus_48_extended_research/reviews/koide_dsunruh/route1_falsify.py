import sympy as sp
mp_dps=40

print("=== TEST A: is the d=s (r=sqrt2) extremum a MINIMUM of a real renormalizable V? ===")
# A polynomial potential V(phi) is a sum of e1,q,c,t monomials. Its STATIONARY points are
# the residual-subgroup alignments (r in {0,1,2,4,inf}) generically. The f2-ratio is NOT a
# polynomial potential -- it's a homogeneous degree-0 RATIO. A renormalizable flavon V
# CANNOT have d=s as an isolated minimum unless tuned, because:
a,b=sp.symbols('a b',real=True)
# On the (a,a,b) branch, the gradient of ANY quartic S3 potential vanishes at rho=b/a in a
# finite set; r=sqrt2 needs rho=4-3sqrt2 (irrational). A polynomial gradient=0 gives algebraic
# rho; to FORCE rho=4-3sqrt2 the couplings must satisfy a tuned algebraic relation.
rho=sp.symbols('rho',real=True)
# general quartic V on branch, gradient wrt rho (after fixing radial), zeros:
m2,L,h,k=sp.symbols('m2 L h k',real=True)
# V(1,1,rho) up to overall a-scale; treat radial separately. The ANGULAR eq fixing rho:
e1=2+rho; q=2+rho**2; c=2+rho**3; t=rho
V=-m2*q+L*q**2+h*c+k*t
# angular stationarity: d/drho of V at fixed |phi| is messy; instead require the FULL (a,b) grad=0
# and ask: for the minimum to have rho=4-3sqrt2, what coupling relation?
rho_star=4-3*sp.sqrt(2)
# Use (a,b) gradient; set a=1 wlog scale, solve grad_b=0 and grad_a=0 jointly for the ratio.
av,bv=sp.symbols('av bv',real=True)
e1v=2*av+bv; qv=2*av**2+bv**2; cv=2*av**3+bv**3; tv=av**2*bv
Vab=-m2*qv+L*qv**2+h*cv+k*tv
ga=sp.diff(Vab,av); gb=sp.diff(Vab,bv)
# impose bv=rho_star*av, av=1, then need ga=gb=0 -> 2 eqs in (m2,L,h,k): codim-2 surface
g1=ga.subs({av:1,bv:rho_star}); g2=gb.subs({av:1,bv:rho_star})
print("  Requiring the VEV ratio b/a = 4-3sqrt2 (=> r=sqrt2) imposes TWO eqs on couplings:")
print("   ", sp.simplify(g1),"= 0")
print("   ", sp.simplify(g2),"= 0")
print("  -> a codimension-2 tuned surface in (m2,L,h,k). r=sqrt2 is NOT generic; it is TUNED.")
print()

print("=== TEST B: FALSIFICATION -- AM-GM 'equal split' is FLAVOR-BLIND ===")
# If the principle is 'maximize d^2 s^2/q^2' (AM-GM equal split), it forces d=s => r=sqrt2
# => Q=2/3 for EVERY fermion sector identically. But measured:
import mpmath as mp
mp.mp.dps=30
# PDG-ish masses
me,mmu,mtau=mp.mpf('0.51099895e-3'),mp.mpf('105.6583755e-3'),mp.mpf('1776.86e-3')  # GeV
mu_,mc,mt=mp.mpf('2.16e-3'),mp.mpf('1.27'),mp.mpf('172.69')
md,ms,mb=mp.mpf('4.67e-3'),mp.mpf('93.4e-3'),mp.mpf('4.18')
def Q(ms_):
    x=[mp.sqrt(m) for m in ms_]
    return sum(m for m in ms_)/sum(x)**2
def r_of_Q(Qv): return mp.sqrt(6*(Qv-mp.mpf(1)/3))
for name,trip in [("leptons",(me,mmu,mtau)),("up",(mu_,mc,mt)),("down",(md,ms,mb))]:
    Qv=Q(trip); print(f"  {name:8s} Q={mp.nstr(Qv,8)}  r={mp.nstr(r_of_Q(Qv),8)}  (d=s would force r=sqrt2={mp.nstr(mp.sqrt(2),8)}, Q=2/3)")
print()
print("  Leptons sit at r=sqrt2 (Q=2/3) but UP r=", mp.nstr(r_of_Q(Q((mu_,mc,mt))),6),
      "(Q=",mp.nstr(Q((mu_,mc,mt)),5),"!=2/3), DOWN r=",mp.nstr(r_of_Q(Q((md,ms,mb))),6))
print("  => a flavor-blind 'equal-split/AM-GM' principle is FALSIFIED by quarks.")
print("     For f2 to apply ONLY to leptons needs a lepton-specific reason it is")
print("     extremized -- which the AM-GM invariant does NOT supply (no sector label).")
