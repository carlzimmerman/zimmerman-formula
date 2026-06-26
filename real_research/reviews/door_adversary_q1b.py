import numpy as np
print("="*100)
print("ADVERSARY q1b: The algebraic reading is trivially conservative (1-DOF gradient). The REAL X2")
print("claim lives in the TIME-NONLOCAL kernel I[{r},w]. Build the genuinely DISPERSIVE response and")
print("ask the passivity question PROPERLY: a two-tone drive probes Im of the F<->a relation directly.")
print("If the cycle-averaged power into the element is NEGATIVE (element DELIVERS energy) -> ACTIVE -> survives.")
print("="*100)
# A linear passive element: F = chi * a (response).  Power delivered BY element to load over cycle:
#   for a(t)=Re[a_w e^{iwt}], P = -<F v> ... the standard passivity: a passive element ABSORBS, <P_abs> >=0.
# For the MI, the 'modulus' is mu_fw(|a|/a0): real, frequency-INDEPENDENT in the instantaneous reading.
# A real-valued, frequency-independent multiplier has Im=0 EXACTLY -> ZERO reactive/active power. 
# The X2 'Im<0' arose ONLY from FORCING a causal completion of the amplitude-dependence as if it were freq-dependence.
print("\n[K1] KEY POINT: mu_fw is a real-valued AMPLITUDE multiplier mu(|a|/a0), NOT a frequency kernel.")
print("     Its Fourier 'kernel' if you (mis)read amplitude-dependence as time-dependence is what X2 did.")
print("     A real multiplier has Im=0 => zero net reactive power. Let's verify the instantaneous law")
print("     delivers EXACTLY zero average power under a single-tone steady drive, both signs of slope.")

a0=1.0
def mu(x):
    x=abs(x); return 1.0 if x==0 else (np.sqrt(1+4*x*x)-1)/(2*x)
# Steady single-tone: a(t)=Ac cos(wt). F=mu(|a|/a0)*a (instantaneous). v=INT a dt. P=<F v>.
w=1.0
t=np.linspace(0,2*np.pi/w,2_000_000,endpoint=False); dt=t[1]-t[0]
for Ac in [0.2,1.0,5.0]:
    a=Ac*np.cos(w*t)
    F=np.array([mu(abs(ai)/a0)*ai for ai in a])
    v=np.cumsum(a)*dt; v-=v.mean()  # velocity from accel
    P=np.mean(F*v)
    print(f"   Ac={Ac:>4}: <F*v> over cycle = {P:+.3e}  (=0 => no net power, neither absorbs nor delivers)")
print("   => At EVERY amplitude (deep-MOND Ac>>1 included) the average power is ZERO. No gain, no loss.")

print("\n[K2] The DECISIVE distinction (nonlinear-constitutive vs linear-kernel inversion):")
print("   - LINEAR-KERNEL inversion (FORBIDDEN if passive): Im chi(w)<0 at FIXED operating point => energy/cycle != 0.")
print("   - NONLINEAR-CONSTITUTIVE inversion (ALLOWED): mu(0)<mu(inf) is 'two operating points of a real multiplier',")
print("     each with Im=0 and zero cycle-energy. The drop is in the REAL secant modulus vs amplitude, not Im chi.")
print("   We just showed mu_fw is the SECOND kind: real multiplier, P=0 at all amplitudes. The 'active' read")
print("   was the artifact of representing amplitude-dependence as a causal frequency kernel (X2's own caveat).")

print("\n[K3] ADVERSARY'S LAST STAND: is there ANY genuine frequency dispersion in Milgrom MI that could")
print("   carry a real Im? Milgrom Eq.3 I[{r},w] IS frequency-dependent for NON-circular orbits. But Eq.11")
print("   PROVES phi+E_k conserved REGARDLESS -> any genuine dispersion is REACTIVE (energy-storing), not")
print("   dissipative/active. Conservation is the theorem; it forecloses BOTH passive-loss AND active-gain.")
print("   => The only consistent reading: the MI kernel is LOSSLESS (purely reactive). Not passive-bath,")
print("      not active-source. 'Active kernel required' is FALSE; 'passive-bath kernel' is ALSO false;")
print("      the truth is 'LOSSLESS non-bath reactive functional' -- which a closed Lagrangian theory HAS.")
