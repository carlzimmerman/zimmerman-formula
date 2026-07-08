import numpy as np
c=2.99792458e8
# Canonical rho_DE footing
H_L=1.79e-18  # H_Lambda ~ sqrt(Lambda/3)*c, approx s^-1 for the dS horizon term
Z=np.sqrt(32*np.pi/3)
print("Z =",Z)
# canonical a0 = c H_Lambda / Z target = 9.36e-11
a0_canon=9.36e-11
a0_alt=1.13e-10
print("a0 canon =",a0_canon,"  a0 alt =",a0_alt)
print("ratio alt/canon =",a0_alt/a0_canon)
print("dex offset in deep-MOND amplitude (0.5*log10 ratio) =",0.5*np.log10(a0_alt/a0_canon))

# STX lane: fixed-CMB-apex fit on INPOP15a
A=-8.79e-11; sigA=6.35e-10
print("\nSTX A =",A,"+/-",sigA)
print("95% |A| <",1.96*sigA)
target_canon=8.6e-10
print("target canon |sTX| =",target_canon,"-> sigma =",abs(A- -target_canon)/sigA if False else target_canon/sigA,"(target/sigma)")
print("  (A sits at",abs(A)/sigA,"sigma from 0; target at",(target_canon-abs(A))/sigA,"sigma above current)")
print("kill floor sigma =",4.3e-10,"  current sigma",sigA,"-> ABOVE floor:",sigA>4.3e-10)

# EUCLID lane: MM24 anchor offsets
print("\nEUCLID cluster deep-MOND offset canon = -0.054 dex, alt = -0.013 dex; MM24 scatter ~0.10-0.15 dex")
print("a0(z) fork: canon FLAT; alt RISING +0.16 dex by z=1.5; ~0.05 dex/bin sep by z=1")
