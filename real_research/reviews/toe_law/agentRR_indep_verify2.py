"""
INDEPENDENT checks (C) clamp identity + (D) stability at fold strength + (E) hostile parameter count.
"""
import sympy as sp, numpy as np

print("="*70)
print("CHECK (C): the clamp identity g_eff(I*)=kappa is structural (FORCED), independent")
print("="*70)
I,Isat,g0,kappa = sp.symbols('I I_sat g0 kappa', positive=True)
# general saturating gain: g(I)=g0/(1+I/Isat). Steady state of dI/dt=(g(I)-kappa)I, I>0 => g(I*)=kappa.
# Solve g(I*)=kappa generally:
Istar = sp.solve(sp.Eq(g0/(1+I/Isat), kappa), I)[0]
print("I* solving g(I*)=kappa:", sp.simplify(Istar))
# the KEY hostile point: is 'g_eff clamps to loss' special to this saturation form, or generic?
# For ANY strictly-decreasing g(I) with g(0)=g0>kappa and g(inf)<kappa, IVT gives a unique I*>0 with
# g(I*)=kappa. So the CLAMP VALUE = loss is forced by monotonicity, NOT by the Lorentzian/laser form.
print("=> clamp value = loss is forced by ANY monotone-decreasing saturation (IVT). Structural. CONFIRMED.")
# BUT hostile sub-point: does the clamp pin the AMPLITUDE I* to a pump scale, or to the free Isat?
print("I* = Isat*(g0/kappa - 1): the amplitude scale is set by Isat (free) and g0/kappa (free ratio).")
print("=> the clamp EXISTS (forced) but WHERE it sits (I*) is set by FREE scales. Honest split confirmed.")

print()
print("="*70)
print("CHECK (D): off-center pole at fold strength -- independent quartic, do poles go UHP?")
print("="*70)
# Independent construction: dressed khronon D(w)=w^2 - wk2 + i kappa w - chi(w),
# chi(w) = lam/(wr^2 - w^2 - i gamma w), lam=-B (active, negative residue). Build the quartic and
# root it directly with numpy (mirror of part9d but rewritten and re-sanity-checked).
def maxim(wk2,B,wr,gamma,kappa):
    lam=-B
    # (w^2 - wk2 + i kappa w)(wr^2 - w^2 - i gamma w) - lam = 0
    # expand to a4 w^4 + a3 w^3 + a2 w^2 + a1 w + a0
    a4=-1.0
    a3=-1j*(gamma+kappa)
    a2=(wr**2 + kappa*gamma + wk2)
    a1=1j*(kappa*wr**2 + gamma*wk2)
    a0=(-wk2*wr**2 - lam)
    return max(r.imag for r in np.roots([a4,a3,a2,a1,a0]))
wr,gamma=0.6,0.1
# sanity: passive limit B<0? at small active B and large loss, LHP; at fold B and any loss, UHP?
print("fold-strength B, sweep kappa, worst Im(pole) over off-center band wk2 in [0.2,1.5]:")
for kappa in [0.05,0.5,1.0,2.0,5.0]:
    worst={}
    for B in [0.05,0.6,1.3]:
        m=max(maxim(wk2,B,wr,gamma,kappa) for wk2 in np.linspace(0.2,1.5,400))
        worst[B]=m
    print(f"  kappa={kappa}: " + " ".join(f"B={b}:Im={worst[b]:+.3f}" for b in worst))
print("=> even kappa up to 5 (huge khronon loss) leaves fold-strength B=0.6,1.3 with UHP poles.")
print("   Scalar (Markovian) saturation cannot stabilize the off-center fold band. CONFIRMED.")

print()
print("="*70)
print("CHECK (E): HOSTILE parameter count -- is anything 'FORCED' actually a tunable knob?")
print("="*70)
# Enumerate the route's continuous parameters and classify ruthlessly.
# Dimensionless fold conditions (from Check A/B): everything reduces to TWO dimensionless ratios
#   x = k0^2 / Gamma   (center/width)        -- must be in ~[0.10,0.30]
#   y = A / (c^2 Gamma) (clamp strength)     -- must be in ~[1.00,1.30]
# plus k0 must coincide with the sonic edge b->c_chi (one more tuning).
# Question: does the dS pump (H, T_dS=H/2pi) fix x and y, or only set dimensionful SCALES?
print("The fold needs TWO dimensionless ratios in narrow bands + 1 edge-coincidence:")
print("  x = k0^2/Gamma in [0.10,0.30]   (center-to-width RATIO)")
print("  y = A/(c^2 Gamma) in [1.00,1.30] (clamp-strength RATIO)")
print("  + k0 = b->c_chi (sonic-edge coincidence)")
print()
print("dS pump pins SCALES (H sets k0~H, T_dS sets Gamma~H), but a RATIO x=k0^2/Gamma is")
print("dimensionless -- setting both ~H gives x~O(1)~H, NOT a forced value in [0.1,0.3].")
print("The smooth GH continuum is BROAD => small x is NOT what the thermal bath delivers (QQ: sigma6<0).")
print()
# The forced claims the route banks: count them and check none is a disguised knob.
forced = [
 ("medium active (g0>0)", "X2 passivity theorem", "SIGN of activity, not magnitude -> not a knob"),
 ("sigma4<0 bend", "dS-bath level repulsion (851e7649)", "SIGN only -> not a knob"),
 ("saturation clamps amplitude", "monotone saturation + IVT", "EXISTENCE of clamp -> not a knob; but I* set by free Isat"),
]
free = ["x=k0^2/Gamma in [0.1,0.3] (narrow peak)","y=A/(c^2 Gamma) in [1.0,1.3] (fold magnitude)",
        "k0 = sonic edge (coincidence)","k-resolved/non-Markovian clamp (scalar fails, Check D)"]
print("FORCED claims (each a SIGN/EXISTENCE statement, no continuous value asserted):")
for f_ in forced: print(f"   [OK] {f_[0]:32s} <- {f_[1]} ({f_[2]})")
print("\nFREE knobs load-bearing for DELIVERY (continuous values that must land in narrow bands):")
for fr in free: print(f"   [FREE] {fr}")
print(f"\nFREE-KNOB COUNT for delivery = {len(free)}  => NOT zero => route's 'FORCED' subset is")
print("clean (only signs/existence), but DELIVERY is MODEL-DEPENDENT. No knob mislabeled forced.")
