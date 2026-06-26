import numpy as np

print("="*70)
print("MUSE-DARK III (Ciocan 2026) vs the three a0(z) hypotheses")
print("  measured: a0(z) = a0(0) + a1*z, a1=1.59e-10, a0(z~1)~2.38e-10")
print("  local a0(0) ~ 1.2e-10 (their RAR normalization)")
print("="*70)
a0_local = 1.2e-10
a1 = 1.59e-10
def muse(z): return a0_local + a1*z

# framework declining sqrt(rho_DE), DR2 DESY5
def rho_ratio(z,w0,wa): return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))
def fw(z): return a0_local*np.sqrt(rho_ratio(z,-0.752,-0.86))
# rising rival cH ∝ E(z)
Om,OL=0.31,0.69
def Ez(z): return np.sqrt(Om*(1+z)**3+OL)
def rival(z): return a0_local*Ez(z)/Ez(0)

print(f"\n{'z':>6}{'MUSE obs':>12}{'framework':>12}{'rising-rival':>14}{'const-MOND':>12}")
for z in [0.0,0.33,0.5,0.75,1.0,1.44]:
    print(f"{z:>6.2f}{muse(z):>12.2e}{fw(z):>12.2e}{rival(z):>14.2e}{a0_local:>12.2e}")

print("\nAt z~1: MUSE obs={:.2e}  framework={:.2e} ({:+.0f}%)  rival={:.2e} ({:+.0f}%)".format(
    muse(1), fw(1), 100*(fw(1)/muse(1)-1), rival(1), 100*(rival(1)/muse(1)-1)))
print("\nREAD:")
print(" - MUSE a0 ROUGHLY DOUBLES by z~1 (steep RISE). ")
print(" - Framework (declining sqrt rho_DE): ~FLAT to z~1 (+1%), then DECLINES. ")
print("   => framework UNDERSHOOTS MUSE by ~factor 2 at z~1. TENSION.")
print(" - Even the RISING rival (+78% at z=1) undershoots MUSE's ~+98%.")
print(" - BUT: Ciocan/MUSE is ROTATION-CURVE-INFERRED a0 at fixed baryons;")
print("   degenerate with M/L evolution, gas fractions, beam smearing, ")
print("   pressure support at high z (LCDM-degenerate per the memory).")
print("   It is NOT a clean a0 measurement -> CONTESTED/non-diagnostic, not a kill.")
