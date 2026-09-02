import sympy as sp, pickle, glob
KB,C4,JY=sp.symbols('K_B c4 J_Y',real=True)
# candidate closed form discovered from the numeric grid:  alpha_1 = -4 c14 - 4(2-K_B)/(J_Y+1), c14=K_B+c4
alpha1_form = -4*(KB+C4) - 4*(2-KB)/(JY+1)
print("candidate: alpha_1 =", sp.simplify(alpha1_form), " = -4*c14 - 4*(2-K_B)/(J_Y+1)")
# check against the 4 numeric (K_B, J_Y=1) rows from the backstop:
rows = {sp.Rational(1,20): -4*sp.Symbol('c4')-sp.Rational(41,10),
        sp.Rational(1,10): -4*sp.Symbol('c4')-sp.Rational(21,5),
        sp.Rational(1,5):  -4*sp.Symbol('c4')-sp.Rational(22,5),
        sp.Rational(1,4):  -4*sp.Symbol('c4')-sp.Rational(9,2)}
c4=sp.Symbol('c4')
allok=True
for kb,expr in rows.items():
    got = sp.simplify(alpha1_form.subs({KB:kb, JY:1, C4:c4}) - expr)
    print(f"  K_B={kb}, J_Y=1:  form - numeric = {got}  {'OK' if got==0 else 'MISMATCH'}")
    allok &= (got==0)
# solve alpha_1=0 for c14 and show it's negative on 0<K_B<=0.25, all J_Y>=1
c14=sp.Symbol('c14',real=True)
form_c14 = -4*c14 - 4*(2-KB)/(JY+1)
c14star = sp.solve(sp.Eq(form_c14,0), c14)[0]
print("\n  alpha_1=0  =>  c14* =", sp.simplify(c14star), " = -(2-K_B)/(J_Y+1)")
print("  at J_Y=1:  c14* =", sp.simplify(c14star.subs(JY,1)), "= (K_B-2)/2")
print("  sign over 0<K_B<=0.25, J_Y>=1:  numerator (2-K_B)>0, denom (J_Y+1)>0  => c14* < 0 ALWAYS")
for kb in [sp.Rational(1,20),sp.Rational(1,10),sp.Rational(1,5),sp.Rational(1,4)]:
    for jy in [1,2,5]:
        v=sp.simplify(c14star.subs({KB:kb,JY:jy})); print(f"    K_B={kb}, J_Y={jy}: c14*={v}={float(v):.3f}  (<0 => spin-1 GHOST)")
# the drag piece is the (2-K_B) coupling itself -- the MOND-generating term
print("\n  MECHANISM: alpha_1 = -4*c14 [pure-EA] - 4*(2-K_B)/(J_Y+1) [scalar drag].")
print("  The drag coefficient (2-K_B) is EXACTLY the AeST scalar-aether coupling 2(2-K_B)J.grad(phi)")
print("  that GENERATES MOND. It is negative-definite in alpha_1 and c14-independent, so no aether")
print("  kinetic tuning removes it; alpha_1=0 costs c14<0 = spin-1 ghost. c2 is transverse-blind.")
print("\nALL CLOSED-FORM CHECKS", "PASS" if allok else "FAIL")
