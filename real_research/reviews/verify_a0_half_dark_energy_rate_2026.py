import math
C=2.99792458e8; G=6.67430e-11; MPC=3.0856775814913673e22
H0=67.66e3/MPC; OL=0.6889
rho_c=3*H0**2/(8*math.pi*G); rho_L=OL*rho_c
HL=math.sqrt(8*math.pi*G*rho_L/3)
Z=math.sqrt(32*math.pi/3)
a_half=0.5*C*math.sqrt(G*rho_L)
a_ZHL=C*HL/Z
print(f"rho_L      = {rho_L:.4e} kg/m^3")
print(f"H_Lambda   = {HL:.4e} 1/s")
print(f"Z          = {Z:.5f}")
print(f"(c/2)sqrt(G rho_L) = {a_half:.4e}")
print(f"c H_L / Z          = {a_ZHL:.4e}")
print(f"identity rel diff  = {abs(a_half-a_ZHL)/a_half:.2e}   (must be ~0)")
print(f"vs fitted 9.36e-11 : {(a_half/9.36e-11-1)*100:+.2f}%")
print(f"Milgrom99 2cH_L    = {2*C*HL:.4e}  = {2*C*HL/a_half:.3f}x  (expect 2Z={2*Z:.3f})")
print(f"Milgrom20 cH_L/2pi = {C*HL/(2*math.pi):.4e}")
d=abs(math.log10(Z/(2*math.pi)))
print(f"Z vs 2pi           : {abs(Z/(2*math.pi)-1)*100:.1f}% = {d:.4f} dex in a0, {d/2:.4f} dex in g_obs")
print(f"                     vs RAR scatter 0.1116 dex -> {d/2/0.1116:.3f} of the scatter")
assert abs(a_half-a_ZHL)/a_half < 1e-12, "identity FAILED"
assert abs(2*C*HL/a_half - 2*Z) < 1e-9, "Milgrom ratio FAILED"
print("\nALL CHECKS PASS")
