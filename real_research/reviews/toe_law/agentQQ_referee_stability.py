"""
REFEREE part 2 — the decisive stability hunt. Two precise questions:

(Q1) Does the bounded-fold dispersion actually have a ROTON MINIMUM (vg=0, a band of
     negative group velocity / backward modes)? If yes, that band + any active gain is
     the absolute-instability hazard. If NO (just an inflection, vg>0 everywhere), the
     'fold' is only an inflection, not a roton dip -- which is its OWN problem for the
     Airy/edge story (NN needs omega''(k*)=0 AND a genuine soft edge omega(k*)->0).

(Q2) THE COUPLED-SYSTEM test the route skips: build the ACTUAL retarded khronon inverse
     propagator with a self-energy whose spectral density rho has the rho<0 band needed
     to produce s4<0, s6>0, and ask: where are the poles omega(k) of the FULL G_R^{-1}=
     omega^2 - c2 k^2 - Pi_R(omega,k)? A genuinely active (rho<0 band) self-energy is
     NOT guaranteed to keep poles in the LHP -- test it directly, do not assume.
"""
import numpy as np
import mpmath as mp
mp.mp.dps = 30

print("="*80)
print("Q1 — is it an INFLECTION or a true ROTON MINIMUM? scan s4=-0.5 fixed, vary s6")
print("="*80)
c2,s4 = 1.0,-0.5
def om2(u,s6): return c2*u+s4*u**2+s6*u**3
print(f"{'s6':>8} | {'min om2/u? (ghost)':>18} | {'has vg=0 (roton dip)?':>22} | {'min vg':>8}")
print("-"*72)
for s6 in [0.0625, 0.07, 0.08, 0.10, 0.125, 0.15, 0.25, 0.5]:
    us=np.linspace(1e-5,8,400000); o2=om2(us,s6)
    ghost = o2.min() < -1e-9
    ok=o2>0; k=np.sqrt(us[ok]); om=np.sqrt(o2[ok]); vg=np.gradient(om,k)
    has_dip = vg.min() < -1e-6
    print(f"{s6:>8.4f} | {str(ghost):>18} | {str(has_dip):>22} | {vg.min():>+8.4f}")
print("""
  READING: a true roton MINIMUM (vg<0 band, backward modes) only appears for s6 small
  enough that omega(k) dips. At/above the no-ghost threshold the 'fold' is generically a
  mere INFLECTION (vg>0 everywhere) -- NOT a roton dip with omega(k*)->soft. The route's
  claim that 'vg=0 at the roton minimum = the soft edge' only holds AT s6=s6* (the triple
  root, where omega(k*)->0 exactly). Just inside the window (s6>s6*) the dispersion has an
  inflection but NO soft point and NO vg=0 -- check whether the NN edge (omega->0 soft) is
  then actually realized, or only at the single tuned point s6=s6*.
""")

print("="*80)
print("Q2 — THE COUPLED TEST: poles of the FULL retarded propagator with an active (rho<0")
print("     band) self-energy. Do they stay in the LHP, or does activeness push them UP?")
print("="*80)
print("""
Build Pi_R(omega) (at representative fixed k, absorb k into couplings) from a spectral
density rho(s) with a NEGATIVE band (the active piece needed for s6>0). Retarded:
   Pi_R(omega) = (1/pi) int rho(s) / (s - omega - i0) ds   [one-sided, retarded]
Full inverse propagator at this k-channel:
   D(omega) = omega^2 - omega0^2 - Pi_R(omega)
Find complex zeros omega_pole of D. POLE IN UHP (Im>0) => exponential RUNAWAY (absolute
instability). This is the test the route replaced with an ISOLATED-Lorentzian assertion.
""")
# representative passive background pole + an active (negative-weight) Lorentzian band.
# rho(s) = passive Lorentzian at s_p>0 (weight>0) PLUS active Lorentzian at s_a>0 (weight<0).
def Pi_R(omega, comps):
    # comps: list of (s0, width, weight). Pi_R(omega)=sum weight * 1/(s0^2 - omega^2 - i width omega)...
    # use simple-pole resonant form Pi = sum weight*s0^2/(s0^2-omega^2 - i*width*omega)
    val=0j
    for (s0,width,wt) in comps:
        val += wt*s0**2/(s0**2 - omega**2 - 1j*width*omega)
    return val
omega0 = 1.0
def D(omega, comps): return omega**2 - omega0**2 - Pi_R(omega, comps)

def find_poles(comps, label):
    roots=[]
    # scan a grid of complex seeds, polish with mpmath
    for re0 in np.linspace(-3,3,25):
        for im0 in np.linspace(-1.5,1.5,21):
            try:
                r = mp.findroot(lambda w: D(complex(w), comps), mp.mpc(re0,im0))
                r=complex(r)
                if all(abs(r-rr)>1e-4 for rr in roots) and abs(D(r,comps))<1e-6:
                    roots.append(r)
            except Exception:
                pass
    uhp=[r for r in roots if r.imag>1e-6]
    print(f"  [{label}] distinct poles found: {len(roots)}; UHP (runaway) poles: {len(uhp)}")
    for r in sorted(roots,key=lambda z:(round(z.real,3),z.imag)):
        flag = "  <-- UHP RUNAWAY" if r.imag>1e-6 else ""
        print(f"     omega = {r.real:+.4f} {r.imag:+.4f}j{flag}")
    return uhp

# Case 1: PURELY PASSIVE self-energy (all weights>0, width>0) -- expect all LHP.
print("\n  Case 1: passive self-energy (all weights>0):")
find_poles([(1.3,0.2,0.3),(2.2,0.3,0.2)], "passive")

# Case 2: ACTIVE -- one NEGATIVE-weight band (the rho<0 piece needed for s6>0),
#         keeping width>0 (positive damping = route's 'negative residue, positive gamma').
print("\n  Case 2: active self-energy (one NEGATIVE weight, width>0 = route's claimed case):")
uhp2 = find_poles([(1.3,0.2,0.3),(2.2,0.3,-0.5)], "active neg-weight")

# Case 3: stronger active band (what you might need to actually reach s6>s6*):
print("\n  Case 3: STRONGER negative band (larger |neg weight|):")
uhp3 = find_poles([(1.3,0.2,0.3),(1.8,0.3,-1.2)], "strong active")

print("""
READING Q2: this is the real test of 'active but stable'. If even Case 2/3 (a genuine
rho<0 band with positive width) keeps ALL poles in the LHP, the route's central claim
survives an independent coupled-system check. If a UHP pole appears as the active band is
strengthened toward the magnitude needed to reach s6>=s6*, then 'bounding the fold' DOES
buy an instability and the route's 'stable' is an artifact of the isolated-Lorentzian toy.
""")
print("DONE.")
