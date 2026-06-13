"""
REFEREE part 6 — the CLEAN, correct stability test, plus the structural verdict.

LESSON from parts 3-5: any propagator written as a function of omega^2 (e.g. omega^2 -
omega0^2 - Pi(omega^2)) is EVEN in omega, so its roots are forced into +-omega, +-omega*
quadruplets and CANNOT all sit in the LHP -- 'UHP pole' is then a kinematic artifact, not
a physical runaway. Retarded stability must be read off the FIRST-ORDER (in omega) damped
oscillator written with a linear-in-omega friction term, where the retarded/advanced split
is meaningful. We do that here, correctly, and reach the structural verdict.

Damped oscillator with self-energy, written correctly:
   chi(omega) = 1/(omega0^2 - omega^2 - i*omega*Gamma(omega)),  Gamma = friction kernel.
Retarded chi is analytic in UHP. Im chi(omega>0) = omega Gamma |chi|^2. Passive (dissipative)
<=> Gamma>0 => Im chi>0 for omega>0 => poles in LHP (omega = +-sqrt(omega0^2-Gamma^2/4)-iGamma/2).
ACTIVE (gain) <=> Gamma<0 on a band => Im chi<0 (the X2/PP active sign) => pole Im = -Gamma/2 >0
=> UHP => RUNAWAY. So for a SIMPLE oscillator, active (Im chi<0) <=> anti-damped <=> UHP <=> runaway.
The route's escape: 'negative RESIDUE with positive Gamma' -- chi = -A/(omega0^2-omega^2-iGamma omega).
But a NEGATIVE residue with positive Gamma has Im chi = -A*omega*Gamma|...|^2 < 0 (active) AND
poles at +-sqrt-iGamma/2 in the LHP. So in THIS toy active+stable coexist. The question that
decides the route: is the route's chosen sign (neg residue, pos Gamma) the one the X2 SUM RULE
and the FORWARD physical coupling actually deliver, or is it an unforced sign choice?
"""
import numpy as np
import mpmath as mp
mp.mp.dps=30

print("="*80)
print("(1) Simple oscillator: ACTIVE-via-anti-damping vs ACTIVE-via-negative-residue")
print("="*80)
A,w0=1.0,1.0
for (resid,gamma,name) in [(+1.0,+0.2,"passive (Im>0, LHP)"),
                            (+1.0,-0.2,"anti-damped (Gamma<0): active+UHP RUNAWAY"),
                            (-1.0,+0.2,"neg-residue, Gamma>0: route's claimed active+stable")]:
    # chi = resid/(w0^2-omega^2 - i gamma omega)
    poles=[ np.sqrt(complex(w0**2-(gamma/2)**2))-1j*gamma/2,
           -np.sqrt(complex(w0**2-(gamma/2)**2))-1j*gamma/2]
    om=np.linspace(0.01,3,4000)
    chi=resid/(w0**2-om**2-1j*gamma*om)
    print(f"  {name}")
    print(f"     pole Im parts: {[f'{p.imag:+.3f}' for p in poles]}  "
          f"=> {'UHP RUNAWAY' if any(p.imag>1e-9 for p in poles) else 'LHP stable'}")
    print(f"     Im chi(omega>0) min={chi.imag.min():+.3f}  "
          f"({'has active (Im<0) band' if chi.imag.min()<-1e-6 else 'passive (Im>=0)'})")
print("""
  => CONFIRMS the route's mathematical claim IS internally valid: a negative-residue,
     positive-Gamma block has an active band (Im chi<0) AND poles in the LHP. So 'active'
     (negative spectral weight) is NOT logically identical to 'anti-damped' (UHP). The route
     is right that these are distinct. POINT TO THE ROUTE.
""")

print("="*80)
print("(2) BUT: is a negative-residue block a legitimate STANDALONE physical response, or")
print("    only a piece that must be added to a passive background to keep Im(total)>=0?")
print("="*80)
print("""
A standalone passive response needs Im chi>=0 for ALL omega>0 (dissipation>=0). A pure
negative-residue Lorentzian has Im chi<0 for ALL omega>0 -- it is active at EVERY frequency,
not just a band. That is a NET energy SOURCE at all frequencies = a perfect amplifier with
no passive floor. Physically the khronon response = passive_background + active_correction,
and the X2 statement is only that there is a BAND with Im<0, with Im>=0 elsewhere (the sum
rule integral can still converge). Test: passive Lorentzian + smaller negative-residue
Lorentzian -- does the TOTAL have Im<0 only in a band (physical) and still poles in LHP?
""")
def total_chi(om, comps):
    val=0j*om
    for (r,w0_,g_) in comps:
        val=val+ r/(w0_**2-om**2-1j*g_*om)
    return val
om=np.linspace(0.01,4,8000)
comps=[(+1.0,1.0,0.3),(-0.5,2.0,0.3)]  # passive at w=1, active at w=2
ch=total_chi(om,comps)
neg_band = om[ch.imag<-1e-6]
print(f"  total = passive(w0=1) + neg-residue(w0=2): Im<0 on omega in "
      f"[{neg_band.min():.3f},{neg_band.max():.3f}] (a BAND, Im>=0 elsewhere: physical).")
# dressed poles of the SUM (this is now genuinely a sum of two simple oscillators, each LHP):
print("  each Lorentzian's own poles are in the LHP (Gamma>0 for both); the SUM is a passive+gain")
print("  network -> the response is bounded, poles in LHP. So a banded active response CAN be")
print("  causal+bounded. The route's existence claim survives.")

print("""
================================================================================
(3) THE STRUCTURAL VERDICT -- what the route ACTUALLY established vs CLAIMED
================================================================================
ESTABLISHED (survives independent recompute):
 * no-ghost window sigma6>sigma6*=sigma4^2/(4c2): CONFIRMED by independent algebra
   (min of s6 u^2+s4 u+c2 over u>0) and Sturm root counts. Threshold exact = 1/16. [Attack A]
 * PP no-fold / Cauchy-Schwarz for passive: re-confirmed by Hankel-PSD, 0/200000. [Attack D]
 * 'active (Im<0 band)' is distinct from 'anti-damped (UHP pole)': a negative-residue,
   positive-Gamma block has both an active band AND LHP poles. The route is RIGHT that
   activeness need not be a UHP runaway IN A SINGLE LINEAR BLOCK. [part 6 (1)]
 * a BANDED active response (passive + small negative-residue) is bounded/causal. [part6 (2)]

NOT ESTABLISHED (the gaps the recompute exposes):
 (i) TWO-OBJECT CONFLATION [Attack C]: the bounded-fold SPATIAL dispersion omega^2(k)=
     c2 k^2+s4 k^4+s6 k^6 (s4<0,s6>0) is a LOSSLESS roton dispersion (real, no Im off-shell)
     -- by itself NOT active at all (it's literally the He-4 roton form). The 'activeness'
     lives in a DIFFERENT object (the temporal self-energy generating s4<0,s6>0). The route
     proves STABILITY of object#1 and ACTIVENESS of object#2 and reports 'stable AND active'.
     They are the same response only if the self-energy that PRODUCES s4<0,s6>0 is the
     negative-residue/LHP one -- which the route ASSERTS, never derives. So 'stable active
     gain bounds the fold' is shown POSSIBLE for a toy, not shown to be what the dS pump does.
 (ii) THE INFLECTION-vs-ROTON GAP [Q1, part 4]: at the route's own showcase in-window value
     sigma6=0.10 there is NO roton minimum and NO soft point (group velocity > 0 everywhere,
     min vg=+0.25). A genuine soft edge (omega(k*)->0, vg=0) exists ONLY at the tuned triple
     point sigma6=sigma6*. So Part 7's claim 'vg=0 at the roton minimum = the soft edge' for
     the window {0.07,0.10,0.25} is FALSE except at the single point sigma6*. The 'edge'
     (NN's omega->0 soft sonic point) and the 'bounded healthy fold' (omega^2(k*)>0) are
     achieved at DIFFERENT sigma6: the edge needs sigma6=sigma6* exactly (marginal, the
     dispersion KISSES zero -> a soft mode, borderline-unstable), while a robust gap needs
     sigma6>sigma6* (no soft edge). The route's 'pin at the edge' = sit AT sigma6* = sit at
     the marginal-stability knife-edge, NOT comfortably inside a stable window.
 (iii) DRESSED-POLE STABILITY NOT COMPUTED: the route reads stability off omega^2(k)>0 (a
     LOSSLESS criterion) and an ISOLATED-block toy; it never computes the poles of the FULL
     retarded propagator with the active self-energy. Whether the actual dS-pump self-energy
     of magnitude reaching sigma6>=sigma6* keeps the dressed pole in the LHP is open (the
     even-in-omega^2 toys here cannot settle it; a proper retarded computation is needed --
     = the QNM calculation the route itself defers).

NET: the route correctly DEFENDS the LOGICAL POSSIBILITY of stable-active-bounded-fold and
correctly identifies its verdict as PARTIAL-NEEDS-MORE (forced in DIRECTION, free in
MAGNITUDE; pin needs the QNM). The recompute AGREES with that verdict. The corrections are:
(a) the 'pin at the edge' is specifically at the MARGINAL point sigma6* (soft/borderline),
not inside a comfortable stable window -- the route slightly oversells 'stable' by mixing
window-interior examples with an edge that only exists at the boundary; (b) 'active' and
'stable' are demonstrated on DIFFERENT objects; (c) the dressed-pole stability the PRIMARY
CHECK demands is asserted from a toy, not computed. None of these overturn PARTIAL-NEEDS-MORE;
they tighten it and confirm the fold is NOT delivered.
""")
print("DONE.")
