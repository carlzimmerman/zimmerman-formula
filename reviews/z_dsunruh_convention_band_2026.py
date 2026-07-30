"""Is Z = sqrt(32pi/3) even DISTINGUISHABLE from 2pi, given a0's real uncertainty?
And where does kappa=1/2 sit inside the dS-Unruh convention band?"""
import math
PI=math.pi; Z=math.sqrt(32*PI/3)
c=2.99792458e8; Mpc=3.0856775814913673e22
H0=67.4e3/Mpc; HL=H0*math.sqrt(0.6847); cHL=c*HL; cH0=c*H0

print("dS-UNRUH CONVENTION BAND for the coefficient q in a0 = q * cH_Lambda")
band=[("Milgrom deep-MOND Taylor match (forced)", 2.0),
      ("Milgrom abstract, in-root identification", 1.0),
      ("framework  1/Z  (kappa=1/2)", 1/Z),
      ("folklore   1/2pi  (a0 ~ cH/2pi)", 1/(2*PI))]
for nm,q in band:
    print(f"   q={q:8.5f}   a0={q*cHL:.4e}   {nm}")
print(f"   band spans a factor {2.0/(1/(2*PI)):.2f} = 4pi = {4*PI:.2f}  (pure convention)")
print(f"   framework sits at q=1/Z={1/Z:.5f}; the 2pi point is q={1/(2*PI):.5f}")
print(f"   -> framework/2pi-point = {(1/Z)/(1/(2*PI)):.4f}, i.e. {abs(100*((2*PI)/Z-1)):.1f}% apart\n")

print("DISTINGUISHABILITY: a0 empirical width vs the Z-to-2pi gap")
gap=abs((2*PI)/Z-1)
for label,w in [("SPARC RAR M/L systematic (Upsilon 0.5-0.7)",0.16),
                ("a0-line gas-dominated slope box 0.84-1.36e-10",0.24),
                ("optimistic future",0.05)]:
    print(f"   sigma_rel={w*100:5.1f}%  ({label})")
    print(f"      Z-vs-2pi separation = {gap*100:.1f}% = {gap/w:.2f} sigma  -> "
          f"{'INDISTINGUISHABLE' if gap/w < 2 else 'distinguishable'}")
print()
print("So no measurement supports sqrt(32pi/3) OVER 2pi. The claim that the")
print("coefficient is specifically sqrt(32pi/3) is a choice of algebra, not a datum.")
print()
print("Sanity: cH0/7 =",f"{cH0/7:.4e}", " vs framework", f"{cHL/Z:.4e}",
      f"({100*((cH0/7)/(cHL/Z)-1):+.2f}%)  <- an INTEGER beats Z. Illustrative only.")
