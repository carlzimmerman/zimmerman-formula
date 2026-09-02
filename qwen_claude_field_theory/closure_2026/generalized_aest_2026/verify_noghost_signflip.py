import sympy as sp
KB,C4,JY,Q0,kx=sp.symbols('K_B c4 J_Y Q_0 k_x',real=True)
# spin-1 kinetic coefficient (coeff of omega^2), from gen_aest_dispersion_health.out, factored:
kin = 2*(KB+C4)*(2*JY*KB*Q0**2 - 4*JY*Q0**2 + 2*KB*Q0**2 - 4*Q0**2 - kx**2)
bracket = sp.factor(kin/(2*(KB+C4)))
print("spin-1 kinetic coeff = 2*(K_B+c4) * B,   B =", bracket)
print("  B = 2*Q0^2*(J_Y+1)*(K_B-2) - k_x^2   =>", sp.simplify(bracket - (2*Q0**2*(JY+1)*(KB-2)-kx**2))==0)
print("  For 0<K_B<2, J_Y>=1, Q0,k_x real: B < 0 ALWAYS (both terms negative). So sign(kin) = -sign(K_B+c4)=-sign(c14).")
print()
# The published v9 no-ghost theorem establishes AeST (c4=0, c14=K_B>0) is ghost-free => its sign(kin) is the HEALTHY sign.
# Evaluate sign at (a) AeST healthy point and (b) alpha_1=0 locus c14=-(2-K_B)/(J_Y+1)<0, at a physical point.
subs0 = {KB:sp.Rational(1,5), JY:1, Q0:sp.Rational(1,10), kx:1}
kin_aest = kin.subs({**subs0, C4:0})                          # c14 = K_B = 1/5 > 0  (healthy AeST)
c4star = -(2-sp.Rational(1,5))/(1+1) - sp.Rational(1,5)       # c4 s.t. c14 = -(2-K_B)/(J_Y+1)
c14star = sp.Rational(1,5)+c4star
kin_locus = kin.subs({**subs0, C4:c4star})                    # alpha_1=0 locus (c14<0)
print(f"AeST point   c14={sp.Rational(1,5)} (>0, healthy):  kinetic sign = {sp.sign(kin_aest)}   (value {float(kin_aest):.5f})")
print(f"alpha_1=0    c14={sp.nsimplify(c14star)} (<0):        kinetic sign = {sp.sign(kin_locus)}   (value {float(kin_locus):.5f})")
print(f"OPPOSITE SIGN => the alpha_1=0 locus has the spin-1 kinetic term flipped vs the ghost-free AeST point => GHOST: "
      f"{sp.sign(kin_aest) != sp.sign(kin_locus)}")
print()
print("No-ghost <=> stay on AeST's side <=> c14 = K_B+c4 > 0.  alpha_1=0 => c14=-(2-K_B)/(J_Y+1) < 0 => GHOST. QED.")
