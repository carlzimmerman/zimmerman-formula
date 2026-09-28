#!/usr/bin/env python3
"""
AS138.C01 -- compute b exactly from the pinned k04 four-form flux coefficient and the
ratio Z/beta^2 = 8 - 2b; high-precision numerics (mpmath, 60 dps).

Premise AS651 (landed): P(q) = (Z/2 + b beta^2) q^2, b = (2 - K_B) I/(16 pi),
I = jsat = 2 (s_sat Delta_sat - int_0^{s_sat} Delta(s) ds),  Delta(s) = s/(e^{sqrt s} - 1)
(RAR kernel, truncated at its peak),  kappa^2 = 2 beta^2/(Z + 2 b beta^2),
kappa = 1/2  <=>  Z/beta^2 = 8 - 2b.
"""
import math, json
import mpmath as mp

mp.mp.dps = 60

G = mp.mpf("6.67430e-11")
c = mp.mpf(299792458)
A0 = {"canonical": mp.mpf("9.3619e-11"), "alt": mp.mpf("1.1279e-10")}

def Delta(s):
    return mp.mpf(0) if s <= 0 else s / (mp.e**mp.sqrt(s) - 1)

# -- saturation point: max of Delta on (0, inf) --
f = lambda s: -Delta(s)
peak = mp.findroot(lambda s: mp.diff(Delta, s), mp.mpf("2.53963828"), tol=mp.mp.mpf("1e-40"))
s_sat = peak
D_sat = Delta(s_sat)
I_integral = mp.quad(Delta, [0, s_sat])          # int_0^{s_sat} Delta
jsat = 2 * (s_sat * D_sat - I_integral)
I_rar = jsat

b0   = (2 - mp.mpf(0))    * I_rar / (16 * mp.pi)   # K_B = 0
b25  = (2 - mp.mpf("0.25")) * I_rar / (16 * mp.pi) # K_B = 1/4
r0   = 8 - 2 * b0
r25  = 8 - 2 * b25

print("=" * 100)
print("AS138.C01 -- b from the pinned k04 flux coefficient; ratio Z/beta^2 = 8 - 2b")
print("=" * 100)
print(f"kernel Delta(s) = s/(e^sqrt(s) - 1), truncated at its peak (k04)")
print(f"  s_sat                 = {mp.nstr(s_sat, 20)}")
print(f"  Delta_sat             = {mp.nstr(D_sat, 20)}")
print(f"  int_0^{{s_sat}} Delta ds = {mp.nstr(I_integral, 20)}")
print(f"  jsat = I_rar = 2(s*D - int) = {mp.nstr(I_rar, 20)}")
print(f"  (AS651 landed value: 0.45252490; jsat - landed = {mp.nstr(I_rar - mp.mpf('0.45252490'), 5)})")
print()
print("b = (2 - K_B) I/(16 pi)  [K_B in {0, 1/4}]")
print(f"  K_B = 0   : b  = {mp.nstr(b0, 20)}")
print(f"             8 - 2b = {mp.nstr(r0, 20)}")
print(f"  K_B = 1/4 : b  = {mp.nstr(b25, 20)}")
print(f"             8 - 2b = {mp.nstr(r25, 20)}")
print(f"  (AS651 landed r* = 7.96398921 at K_B=0: residual {mp.nstr(r0 - mp.mpf('7.96398921'), 6)})")
print()

# consistency: b read back from the ratio
b_check0 = (8 - r0) / 2
b_check25 = (8 - r25) / 2
print(f"consistency  b = (8 - (8-2b))/2  :  K_B=0: {mp.nstr(b_check0, 20)} -> b - b_check = {mp.nstr(b0 - b_check0, 3)}")
print(f"                                        K_B=1/4: {mp.nstr(b_check25, 20)} -> b - b_check = {mp.nstr(b25 - b_check25, 3)}")
print()

# -- kappa projection as a function of r = Z/beta^2 (AS651 B-iv continuum, re-evaluated exactly)
def kappa2(r, b):  return mp.mpf(2) / (r + 2 * b)
def kappa(r, b):   return mp.sqrt(kappa2(r, b))

print("kappa(r) = sqrt(2/(r + 2b)); on-shell total-Ward conservation holds for EVERY r (assembly theorem).")
print("  r values in the witness family (K_B = 0, b = {}):".format(mp.nstr(b0, 10)))
for r in [1, 2, 4, r0, 8, 16, 64]:
    k = kappa(r, b0)
    lab = "  <-- r* = 8-2b (tuned: kappa = 1/2)" if abs(r - r0) < mp.mpf("1e-12") else ""
    print(f"    r = {mp.nstr(r, 14):>16}  kappa = {mp.nstr(k, 12)}{lab}")
k_half_check = kappa(r0, b0)
print(f"  kappa(r*) - 1/2 = {mp.nstr(k_half_check - mp.mpf('0.5'), 4)}  (exact 0 at 60 dps)")
print()

# -- footings (both registered) --
print("Footings (kappa = 1/2 adopted; distinct densities, never both fixed):")
for name, a0 in A0.items():
    rho_L = 4 * a0**2 / (G * c**2)
    eps_L = rho_L * c**2
    Lam   = 32 * mp.pi * a0**2 / c**4
    q_star = a0 / mp.sqrt(G)                    # beta = 1
    back = a0 / (c * mp.sqrt(G * rho_L))        # = kappa, must be exactly 1/2
    print(f"  {name:9s} a0 = {mp.nstr(a0, 6)} m/s^2 | rho_L = {mp.nstr(rho_L, 10)} kg/m^3 | eps_L = {mp.nstr(eps_L, 10)} J/m^3 | "
          f"Lambda = {mp.nstr(Lam, 6)} m^-2 | q_* = {mp.nstr(q_star, 8)} (beta=1) | kappa back-check = {mp.nstr(back, 10)}")
print()

# -- r = 8 witness --
k8 = kappa(mp.mpf(8), b0)
print(f"counterexample family member: r = 8  -> kappa(8) = {mp.nstr(k8, 12)} != 1/2 "
      f"(diff = {mp.nstr(k8 - mp.mpf('0.5'), 4)}); conservation holds identically at r = 8 (assembly theorem).")

out = {
    "s_sat": mp.nstr(s_sat, 20), "Delta_sat": mp.nstr(D_sat, 20),
    "jsat": mp.nstr(I_rar, 20), "b_K0": mp.nstr(b0, 20), "rstar_K0": mp.nstr(r0, 20),
    "b_K025": mp.nstr(b25, 20), "rstar_K025": mp.nstr(r25, 20),
    "kappa_at_rstar": mp.nstr(k_half_check, 12),
    "kappa_at_8": mp.nstr(k8, 12),
}
print()
print("JSON:", json.dumps(out))