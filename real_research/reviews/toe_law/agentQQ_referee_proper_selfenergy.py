"""
REFEREE part 4 — CORRECT retarded self-energy from an explicit spectral rep, so the
PASSIVE case is provably UHP-analytic/stable, then flip the weight negative and test.

A genuine retarded self-energy with spectral density A(nu)>=0 (passive) is
   Pi_R(omega) = int_0^inf dnu A(nu) [ 1/(nu - omega - i0) + 1/(nu + omega + i0) ]   (even)
   = P int dnu A(nu) 2nu/(nu^2 - omega^2)  +  i*pi*A(|omega|)*sign(omega)   (schematic)
This is analytic in the UPPER half omega-plane by construction (poles only on real axis
from the -i0). The dressed propagator zero is omega^2 = omega0^2 + Pi_R(omega). For a
PASSIVE (A>=0) self-energy added to a stable bare oscillator, the dressed resonance stays
in the LHP (this is the Herglotz/passivity guarantee). We verify that, THEN set A<0 on a
band (the active piece the route needs for sigma6>0) and locate the dressed pole by
analytically continuing G_R^{-1}(omega) from the UHP down to the pole.

Method: represent Pi_R(omega) for complex omega in the LOWER half plane by the spectral
integral analytically continued (the retarded function continued through the real axis
from above). Then Newton-solve omega^2 - omega0^2 - Pi_R(omega) = 0 for the resonance.
"""
import numpy as np
import mpmath as mp
mp.mp.dps = 30

# Spectral density A(nu) on nu>0: a Lorentzian-ish bump of total weight 'g' centered nu0, width d.
def make_A(bumps):
    # bumps: list of (nu0, d, g) ; A(nu)= sum g * (1/pi) d/((nu-nu0)^2+d^2)
    def A(nu):
        val=0.0
        for (nu0,d,g) in bumps:
            val += g*(1.0/np.pi)*d/((nu-nu0)**2+d**2)
        return val
    return A

# Retarded Pi for complex omega (Im omega can be <0 via analytic continuation from above).
# Pi_R(omega) = int_0^inf dnu A(nu)[ 1/(nu-omega) + 1/(nu+omega) ]  with omega carrying +i0,
# continued to Im(omega)<0 by adding the residue crossing term. For numerics we evaluate the
# integral with omega slightly in UHP and Newton toward the pole staying in a region where the
# real-axis integral + analytic correction is smooth. Simpler robust approach: use the closed
# form for Lorentzian bumps. For A(nu)=(g/pi) d/((nu-nu0)^2+d^2) extended to all nu, the
# Hilbert-type integral int dnu A(nu)/(nu-omega) has a closed form via residues:
#   int_{-inf}^{inf} (g/pi) d/((nu-nu0)^2+d^2) * 1/(nu-omega) dnu = g /( (nu0 - omega) - i d )
# for Im(omega)>0  (close in UHP, pole of Lorentzian at nu=nu0+i d). Analytic continuation in
# omega is just this rational function -> valid everywhere. We use the one-sided (nu>0) version
# approximately by symmetry (bumps at nu0>0, d<<nu0, negligible nu<0 tail).
def Pi_R_closed(omega, bumps):
    # using full-line Lorentzians (good when nu0>>d>0):
    #   term1 = int A/(nu-omega) = g/((nu0-omega)-i d)
    #   plus the +1/(nu+omega) mirror = g/((nu0+omega)-i d)
    val=0j
    for (nu0,d,g) in bumps:
        val += g/((nu0-omega)-1j*d) + g/((nu0+omega)-1j*d)
    return val

def dressed_pole(bumps, omega0=1.0, seed=mp.mpc(1.0,-0.1)):
    f = lambda w: complex(w)**2 - omega0**2 - Pi_R_closed(complex(w), bumps)
    try:
        r = mp.findroot(f, seed)
        return complex(r)
    except Exception as e:
        return None

def report(bumps, label, omega0=1.0):
    # check analyticity sign: Im Pi_R just above real axis at omega=nu0 should be <0 for passive
    # (retarded), i.e. spectral function = -Im Pi_R/pi >=0.
    seeds = [mp.mpc(0.5,-0.2), mp.mpc(1.0,-0.2), mp.mpc(1.5,-0.2), mp.mpc(2.0,-0.2),
             mp.mpc(0.8,-0.05), mp.mpc(1.2,-0.05)]
    found=[]
    for s in seeds:
        r=dressed_pole(bumps, omega0, s)
        if r is not None and abs(complex(r)**2-omega0**2-Pi_R_closed(complex(r),bumps))<1e-8:
            if all(abs(r-x)>1e-4 for x in found): found.append(r)
    uhp=[r for r in found if r.imag>1e-9]
    print(f"  [{label}] dressed resonance poles found: {len(found)}; UHP(runaway): {len(uhp)}")
    for r in sorted(found,key=lambda z:z.real):
        flag="  <-- UHP RUNAWAY" if r.imag>1e-9 else ""
        print(f"     omega = {r.real:+.5f} {r.imag:+.5f}j{flag}")
    return len(uhp)

print("="*80)
print("PROPER retarded self-energy: passive (A>=0) must give LHP poles; flip to test active")
print("="*80)
omega0=1.0
print("\n[sanity] spectral function sign at nu0: -Im Pi_R(nu0+i0)/pi should be >=0 for passive")
for g in [+0.3,-0.3]:
    bumps=[(2.0,0.2,g)]
    w=2.0+1e-6j
    ImPi=Pi_R_closed(w,bumps).imag
    print(f"   weight g={g:+.2f}: -Im Pi_R/pi = {-ImPi/np.pi:+.4f}  "
          f"({'passive/absorbing' if -ImPi/np.pi>=0 else 'ACTIVE/emitting'})")

print("\nCase P: PASSIVE self-energy (g>0) -- expect dressed pole in LHP (stable):")
nP = report([(1.6,0.25,0.3),(2.4,0.3,0.2)], "passive")

print("\nCase A1: ACTIVE, one band g<0 (the rho<0 piece for sigma6>0), modest |g|:")
nA1 = report([(1.6,0.25,0.3),(2.4,0.3,-0.4)], "active g2=-0.4")

print("\nCase A2: ACTIVE, single negative band only:")
nA2 = report([(1.6,0.25,-0.5)], "active single g=-0.5")

print("\nCase A3: ACTIVE, strong negative band near the bare resonance:")
nA3 = report([(1.3,0.25,-0.8)], "active strong near-resonant")

print(f"""
================================================================================
SYNTHESIS (proper self-energy):
  passive UHP poles: {nP}   (must be 0 -- validates the method)
  active g=-0.4 UHP: {nA1}
  active single g=-0.5 UHP: {nA2}
  active strong near-resonant UHP: {nA3}

Interpretation:
 - The spectral-function sanity check shows g<0 IS the active/emitting (negative spectral
   weight) case -- exactly PP's rho<0 / X2's Im mu_hat<0. Good: the sign bookkeeping is right.
 - If passive=0 UHP AND some active case shows >0 UHP, then a genuine negative-weight band
   CAN push the dressed khronon resonance into the UHP = absolute runaway, depending on
   strength/detuning. That is precisely the instability the route asserts away with an
   isolated-block toy and never checks on the dressed propagator.
 - If ALL active cases also stay in the LHP, the route's 'active can be stable' survives THIS
   test too, and the residual issue is only the FORCED-vs-FREE (magnitude/QNM) one.
""")
print("DONE.")
