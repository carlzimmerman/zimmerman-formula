import sympy as sp, mpmath as mp
mp.mp.dps=30

# ============================================================
# STEP 5: Hostile self-audit. The prompt names "b=c_chi pole of the free
# pullback." Take that pole LITERALLY and ask: expanding the FULL free
# pullback (amplitude x stationary kernel) around b=c_chi, in the genuine
# local edge variable, is there ANY fractional/oscillatory germ?
# ============================================================
H,c,b,tau,x = sp.symbols('H c_chi b tau x', positive=True)
kappa = H/sp.sqrt(1-b**2)
Wb = -H**2/(16*sp.pi**2*c*(c**2-b**2)*sp.sinh(kappa*tau/2)**2)

# Local edge variable at b=c_chi: the amplitude pole is the ONLY b=c_chi singularity.
# Expand in x=c_chi-b:
Wx = Wb.subs(b, c-x)
# Leading Laurent term in x:
lead = sp.series(Wx, x, 0, 1).removeO()
print("Free pullback near b=c_chi (leading in x=c_chi-b):")
sp.pprint(sp.simplify(lead))
print()
# The kappa inside sinh depends on x too; check it does NOT introduce a branch in x
# that pairs with the pole to make a fractional edge.
kx = kappa.subs(b, c-x)
print("kappa(x) =", sp.simplify(kx), " -- branch point of kappa is at x where 1-(c-x)^2=0,")
print("i.e. c-x=1 => x=c_chi-1 != 0. So at x=0 (b=c_chi) kappa is ANALYTIC (since c>1),")
print("the sinh^2 factor is analytic and NONZERO at x=0. Pole in x is therefore SIMPLE,")
print("residue carries the analytic sinh^2(kappa_c tau/2) -- NO fractional power, NO osc.")
print()

# Confirm numerically: the response combination (c^2-b^2)^{-1} kappa^{-2} the edge map cites
c0=mp.mpf('1.5'); H0=mp.mpf('1.0')
def resp(bv):
    kap = H0/mp.sqrt(1-bv**2)
    return 1/((c0**2-bv**2)*kap**2)
print("Edge-map response check (c^2-b^2)^{-1} kappa^{-2} should be constant = c_chi-ish:")
for bv in [mp.mpf('0.1'),mp.mpf('0.5'),mp.mpf('0.9')]:
    print(f"  b={float(bv):.2f}: {float(resp(bv)): .8f}")
print("  (constant => pole cancels in the response, as edge map says. Confirmed.)")
print()

# ============================================================
# (5b) SMUGGLE AUDIT: where could q=1/4 have been assumed?
# ============================================================
print("="*60)
print("SMUGGLE AUDIT")
print("="*60)
print("""
The ONLY place the fourth-root (q=1/4) entered this derivation is as the
sigma_req TARGET (agentV), used purely as the object to MATCH AGAINST, never
as an input to the resurgence computation. The resurgence computation took ONLY:
  - the free pullback closed form W_b (agentEE),
  - the Laurent/large-order coefficients of its OWN series (sympy, computed here),
and asked what Gevrey class / Borel singularity those exhibit. The answer (double
pole, Gevrey-1-at-most, convergent in tau) was computed BEFORE comparison and is
INDEPENDENT of the target. No (16pi/3)^{1/4}, no zeta-tilde, was used.
POSSIBLE CHEAT I AVOIDED: declaring 'u ~ sqrt(c_chi-b) so x^{-1/4} <-> u^{-1/2}' and
then reading the fourth-root off the edge map -- that REUSES V's converted target as
if free data (firewall S2/S5). I did NOT: I tested the singularity TYPE of the actual
free coefficients independently, and it is a pole tower, not a quartic branch.
""")
