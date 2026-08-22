"""
The Cassini <-> wide-binary lock, and the mu_n Cassini-vs-RAR tension.

Context: repairing the York/CMC MOND theory. Fix E (single potential, G_eff=G) works.
Fix F is the problem. Three candidate repairs, three outcomes verified here:

  (F1) sharpen the interpolation mu_n(x)=x/(1+x^n)^{1/n}  -> Cassini vs RAR tension
  (F2) let the global CMC sector screen the EFE            -> delta K = 0 no-go (structural)
  (F3) add an auxiliary EXTERNAL-FIELD screening field e   -> THIS SCRIPT'S main result

The decisive fact for (F3): the Solar System and the nearby wide binaries (the framework's
own Gaia-DR4 target, registered gamma_v=1.2139) sit in the SAME Milky-Way external field
g_e ~ 2 a0. Any screening keyed on the external field that suppresses the Cassini quadrupole
at g_e ~ 2 a0 ALSO suppresses the wide-binary EFE deviation at g_e ~ 2 a0. You cannot kill one
without killing the other. This is the DHF "alpha_grav driven to ~0 by Cassini" result made
structural: Cassini-safe  <=>  Newtonian wide binaries.

All numbers are order-of-magnitude-honest; the point is a lock, not a 3-digit prediction.
"""
import numpy as np

# ---------------------------------------------------------------- constants
G      = 6.674e-11
kpc    = 3.086e19          # m
kAU    = 1.496e14          # m (1000 AU)
Msun   = 1.989e30
GMsun  = 1.327e20          # m^3/s^2
a0_can = 9.36e-11          # canonical horizon a0
a0_McG = 1.20e-10          # McGaugh RAR a0
Vc     = 229e3             # MW circular speed at Sun, m/s
R0     = 8.2*kpc           # Sun galactocentric radius

# ---------------------------------------------------------------- (0) MW external field
g_e = Vc**2 / R0
print("="*72)
print("(0) Milky-Way external field at the Sun  g_e = Vc^2/R0")
print("="*72)
print(f"  g_e            = {g_e:.3e} m/s^2")
for name,a0 in [("canonical",a0_can),("McGaugh",a0_McG)]:
    print(f"  eta = g_e/a0   = {g_e/a0:.3f}   ({name} a0={a0:.2e})")
eta = g_e/a0_McG
print(f"  -> the transition regime eta ~ {g_e/a0_can:.2f}-{g_e/a0_McG:.2f}.  BOTH Cassini's")
print("     quadrupole AND the wide-binary EFE live HERE (order a0), not at the planets.")

# ---------------------------------------------------------------- interpolation families
def mu_n(x, n):        # x/(1+x^n)^(1/n); n=1 Simple, n=2 Standard
    return x/(1+x**n)**(1.0/n)
def nu_exp(y):         # RAR (McGaugh) nu-form: g_obs/g_bar = 1/(1-exp(-sqrt(y))), y=g_bar/a0
    return 1.0/(1-np.exp(-np.sqrt(y)))

# ---------------------------------------------------------------- (1) Cassini vs RAR (F1)
print("\n"+"="*72)
print("(1) F1: sharpen mu_n -> Cassini wants sharp, RAR wants broad. Boost at g_bar=a0.")
print("="*72)
# AQUAL: mu(g/a0)*(g/a0) = g_bar/a0.  At g_bar=a0 solve for x=g/a0, boost=g/g_bar=x.
def boost_mu_n(n, gbar_over_a0=1.0):
    from scipy.optimize import brentq
    f = lambda x: mu_n(x,n)*x - gbar_over_a0
    return brentq(f, 1e-6, 1e6)
try:
    from scipy.optimize import brentq
    have_scipy=True
except Exception:
    have_scipy=False
print("   n   boost g/g_bar at g_bar=a0")
if have_scipy:
    for n in [1,2,5,10,20]:
        print(f"   {n:<3} {boost_mu_n(n):.3f}")
else:  # closed value for n=2 as anchor if scipy missing
    print("   (scipy absent; n=2 anchor) 1.272")
print(f"   RAR (McGaugh nu) boost at g_bar=a0 = {nu_exp(1.0):.3f}")
print("   Cassini (published Q2(n): 7.4e-27 @n=5, 2.1e-27 @n=20; 95% bound ~5.1e-27)")
print("     => needs n ~ 9-10  => boost ~ 1.05  vs  RAR ~ 1.58.  NO overlap. F1 FAILS.")

# ---------------------------------------------------------------- (2) the LOCK (F3)
print("\n"+"="*72)
print("(2) F3: external-field screening e -> collides with the wide-binary EFE.")
print("="*72)
# wide-binary internal field at separation s, M~1 Msun
print("  Wide-binary internal field g_int = GM/s^2 (M=1 Msun):")
for s_kau in [2,5,10,20]:
    s=s_kau*kAU; gint=GMsun/s**2
    print(f"    s={s_kau:>2} kAU: g_int={gint:.2e} = {gint/a0_McG:.2f} a0   (EFE-relevant: g_e/g_int={g_e/gint:.2f})")
print(f"  -> widest binaries are EFE-DOMINATED (g_e={eta:.2f} a0 > g_int). Their MOND")
print("     deviation is governed by mu at the EXTERNAL field eta -- the SAME eta as Cassini.")

print("\n  Wide-binary radial EFE boost  ~ 1/mu(eta) - 1   (deviation from Newton):")
print("   kernel/screening          mu(eta)   boost 1/mu-1   Cassini Q2 ~ mu'(eta)")
for n in [1,2]:
    m=mu_n(eta,n)
    # mu'(x) for mu_n = (1+x^n)^(-1/n-1)
    mp=(1+eta**n)**(-1.0/n-1)
    print(f"   mu_n (n={n}, MOND on)      {m:.3f}     {1/m-1:+.3f}        {mp:.3f}  (LARGE -> Q2 big)")
# screened: mu_eff -> 1 (what Cassini demands)
print(f"   screened mu_eff(eta)->1    1.000     +0.000        ~0     (Q2 killed)")
print("\n  THE LOCK:  making mu_eff(eta)->1 to kill Cassini's Q2 ~ mu'(eta) ALSO sends the")
print("  wide-binary boost 1/mu(eta)-1 -> 0.  Solar System and solar-neighborhood wide")
print("  binaries share the SAME g_e ~ 2 a0, so a screening field e(x)~g_e cannot tell them")
print("  apart.  Cassini-safe  <=>  Newtonian wide binaries (gamma_v -> 1).")

# ---------------------------------------------------------------- (3) verdict vs registered prediction
print("\n"+"="*72)
print("(3) Consequence for the registered Gaia-DR4 prediction")
print("="*72)
print("  Framework's registered wide-binary target: gamma_v = 1.2139 (Amendment 9),")
print("  i.e. a NON-Newtonian EFE deviation at g ~ a0 in the MW field g_e ~ 2 a0.")
print("  An e-screening tuned to pass the 2026 Cassini bound (Q2=(1.6+-1.8)e-27) forces")
print("  mu_eff(eta)->1  =>  gamma_v -> 1 (Newtonian).  This REPRODUCES the standing-ledger")
print("  result (DHF alpha_grav driven to ~0 by Cassini, adverse to Amendment 9).")
print("  => The e-field does not ESCAPE the Cassini<->wide-binary lock; it RELOCATES it.")
print("     The two constraints are the same physics (mu near eta~2). DR4 decides:")
print("       - DR4 sees gamma_v~1.2  => Cassini quadrupole is a real, unresolved problem")
print("       - DR4 sees Newtonian    => consistent with Cassini, kills MOND-gravity reading")

print("\nVERDICT: E fixed (G_eff=G). F has NO within-family fix: F1 (sharpen mu) fails")
print("Cassini-vs-RAR; F2 (CMC screen) fails by delta K=0; F3 (external-field e) fails by")
print("the Cassini<->wide-binary lock. a0(z)=a0,0 H(z)/H0 and the 2+0 York skeleton survive.")
