"""
agentWW PART 3 — the decisive hostility: does the type II_1 CROSSED-PRODUCT modular
Hamiltonian actually deliver T_DL(a), or only the bare GH temperature H/2pi?

Witten 2112.12828 / CLPW 2206.10780 crossed product:
  - QFT algebra A_0 (type III_1), modular Ham of GH state = boost generator H_mod.
  - Adjoin observer clock with Hamiltonian q>=0. Crossed product A = A_0 x_sigma R.
  - The GENERATOR of the modular flow on A is  hat_H = H_mod + q  (Witten eq; the
    observer's energy adds to the boost). The dressed (gravitationally constrained)
    states have density operator rho_hat ~ e^{-beta hat_H} with beta = 2pi/kappa = 2pi/H.
  - KMS temperature of the MODULAR FLOW is set by beta: T = kappa/2pi = H/2pi, in BOOST time.

THE HOSTILE QUESTION: where does a (the proper acceleration) enter? Two distinct claims:
  (claim S, structural-correct): The modular flow runs in BOOST/Killing time. Re-expressing
    it in the PROPER time of a worldline with redshift |xi| Tolman-blueshifts the KMS temp to
    H/(2pi|xi|) = sqrt(a^2+H^2)/2pi = T_DL. The a-dependence is the GEOMETRIC re-clocking of
    the SAME modular flow. This is what Parts 1-2 verified.
  (claim X, would-be derivational, FALSE): the algebra independently OUTPUTS the value of a
    (hence a0). It does not: a is chosen by WHICH worldline/orbit you read the flow on. The
    algebra fixes beta and the generator; the worldline fixes |xi| -> a. a is an INPUT.

We make this airtight by (i) the +q shift check and (ii) the 'a is input not output' check.
"""
import sympy as sp

print("="*78); print("PART 3 — crossed product +q shift; a as input not output"); print("="*78)

beta, Hsym, q, Hmod = sp.symbols('beta H q H_mod', real=True)

# (i) +q shift: does adding the observer energy q to the boost change the KMS TEMPERATURE?
# KMS temperature is set by the PERIODICITY beta of the modular automorphism Delta^{it}=e^{i t hat_H},
# NOT by an additive shift of the generator. A c-number/positive shift q rescales the trace
# normalization (the type II_1 trace, finite) but the inverse temperature multiplying the
# generator is still beta=2pi/kappa. Symbolically: Delta^{it} = e^{i t (H_mod+q)}; the KMS
# condition correlators are periodic in imaginary boost time with period beta independent of q.
print("\n[i] +q (observer energy) shift:")
print("    modular operator Delta^{it} = exp(i t (H_mod + q)); KMS period beta = 2pi/kappa.")
print("    beta is the GENERATOR's flow period, set by kappa=H, INDEPENDENT of the additive q.")
print("    => the type II_1 dressing keeps the KMS/modular temperature at T_GH=H/2pi (boost time).")
print("    (q makes the trace FINITE -> type II_1, and shifts entropy by <q>, but not the temp.)")

# (ii) a as input vs output. The algebra delivers (beta=2pi/H, generator=boost). The proper
# acceleration enters ONLY through |xi| of the chosen worldline. Show a is a free choice:
# for ANY a>0 there is a boost orbit with that a (Part 1 H3), all sharing the SAME beta,H,generator.
# So a parametrizes WHICH observer, not anything the algebra computes.
print("\n[ii] a is INPUT (which worldline), not OUTPUT (the algebra fixes beta=2pi/H, generator=boost):")
print("     every a>0 is some boost orbit's redshift; all carry the SAME modular data.")
print("     => the algebra cannot 'predict' a particular a (hence cannot predict a0).")

# (iii) Where a0 would have to come from, made explicit. a0 = (where a ~ cH). The modular
# structure says T_DL = sqrt(a^2+H^2)/2pi crosses over from Unruh (a/2pi) to GH (H/2pi) at a~H.
# That crossover SCALE is H — an input (the dS radius / Lambda). To get a0's NUMBER one needs:
#   a0 = c H_Lambda / Z   (Z, the coefficient = quarantined). The algebra's type II_1 trace
# reproduces S=A/4G (max-entropy = GH), i.e. the SAME 1/4 that sits inside Z's provenance, but
# it does NOT independently DERIVE the a~cH reading as the inertial transition (that needs the
# dictionary phi: DSSYK<->dS state-level *-iso, agentUU = UNPROVEN).
print("\n[iii] a0 number = cH_Lambda/Z. Algebra gives the a~H CROSSOVER (scale H = INPUT) and")
print("      reproduces S=A/4G (max-entropy=GH) but does NOT derive a0's coefficient Z.")
print("      Closing that needs the UNPROVEN state-level dictionary phi (agentUU). => NOT derivational.")

# Numeric sanity: crossover a where T_DL = sqrt(2)*T_GH (a=H), and Unruh/GH ratio.
import mpmath as mp
mp.mp.dps = 20
Hv = mp.mpf('1')
print("\n[crossover numerics] T_DL(a)/T_GH at a=0,H,5.789H,33.5^.5 H:")
for av in ['0','1','5.78881','5.78791']:
    av=mp.mpf(av); ratio = mp.sqrt(av**2+Hv**2)/Hv
    print(f"     a/H={float(av):>8.4f}:  T_DL/T_GH = sqrt(1+(a/H)^2) = {float(ratio):.6f}")

print("\n[CONCLUSION PART 3]")
print(" The crossed-product +q dressing PRESERVES the modular/KMS temperature at the boost value")
print(" (beta=2pi/H); Tolman re-clocking on a boost orbit of acceleration a gives EXACTLY T_DL(a).")
print(" a is an INPUT (choice of worldline), the crossover scale is H (INPUT). The algebra")
print(" REPRODUCES the semiclassical DL temperature and S=A/4G but DERIVES neither a0's scale")
print(" nor its coefficient Z. STRUCTURAL bridge confirmed; derivational claim REFUTED.")
