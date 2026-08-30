#!/usr/bin/env python3
"""PRICE the un-localized nonlocal F+ door. F+(Z)=4[1-(1+sqrt(Z)/2)e^{-sqrt(Z)/2}], Z a differential
operator (Z ~ -D^2/scale). Question: does genuine (un-localized) nonlocality ESCAPE the pincer, and
at what cost? sympy where decidable."""
import sympy as sp

Z, u, k, c = sp.symbols('Z u k c', positive=True)
Fp = 4*(1 - (1 + sp.sqrt(Z)/2)*sp.exp(-sp.sqrt(Z)/2))

print("=== 1. Is F+ finitely localizable (=> reduces to the pincer / DC-012) or genuinely nonlocal? ===")
print(f"   F+(Z) = {Fp}")
print("   F+ contains e^(-sqrt(Z)/2): sqrt(Z)=sqrt(-D^2) is a PSEUDO-differential operator (branch cut),")
print("   and e^(-sqrt(Z)/2) is TRANSCENDENTAL. A rational f(box) localizes with finitely many auxiliary")
print("   fields (partial fractions) -> would be a LOCAL theory -> pincer/DC-012 applies. But F+ is")
print("   NON-rational (transcendental + branch cut) => NOT finitely localizable => GENUINELY nonlocal.")
print("   => UNLIKE the scale-split, the pincer's LOCAL under-lensing proof does NOT auto-transfer.")
print("      THIS is the one door that genuinely EXITS DC-001's scope. Now price it.")

print("\n=== 2. Small-k structure: MOND kernel + the banked extra mode ===")
series = sp.series(Fp, Z, 0, 3).removeO()
print(f"   F+(Z->0) = {sp.simplify(series)}   (leading ~ Z/2 => 1/k^2 MOND potential; 2F+'=e^-y gives mu)")
# the localization dispersion (banked): omega^2 = (1/2) c^2 k^2  -> non-tachyonic?
omega2 = sp.Rational(1,2)*c**2*k**2
print(f"   banked extra-mode dispersion: omega^2 = {omega2}  -> omega^2 > 0 for all k (NON-tachyonic,")
print("      NOT a gradient instability). Sub-luminal group speed c/sqrt(2). Ghost = RESIDUE sign (open).")

print("\n=== 3. THE PRICE (what genuine nonlocality costs) ===")
print("   (a) NONLOCAL initial-value problem: data on a time SLAB, not a slice (pseudo-diff sqrt(-D^2)).")
print("   (b) CAUSAL PRESCRIPTION mandatory: retarded box^-1 (causal, => the extra propagating mode) vs")
print("       Feynman (acausal). Retarded is the physical choice and IS the source of the omega^2 mode.")
print("   (c) EXTRA MODE health: omega^2=c^2k^2/2 is non-tachyonic (shown); its residue SIGN (ghost or")
print("       not) is the open computation -- the scale-split localization had A=I (healthy) as evidence")
print("       FOR ghost-freedom, but the transcendental un-localized residue must be checked directly.")
print("   (d) QUANTIZATION generically ill-defined for nonlocal actions => valid as a CLASSICAL effective")
print("       theory only (acceptable at this stage; a UV completion is a separate, later bill).")

print("\n=== 4. The lensing question must be RE-DERIVED (the pincer proof used LOCAL linear stress) ===")
print("   The DC-012 under-lensing proof: a frameless LOCAL scalar has O(pert^2) kinetic stress => no")
print("   linear Psi source. A NONLOCAL operator phi (D_i D_j / box) phi CAN give a LINEAR anisotropic")
print("   stress => could source Psi frame-free. So nonlocality is EXACTLY where the pincer's proof can")
print("   break. Whether F+ specifically yields a healthy (ghost-free) frame-free Psi source = THE open")
print("   calculation that decides this door. NOT yet computed; do not assume either way.")

print("\n=== PRICE SUMMARY ===")
print("The un-localized nonlocal F+ is the ONE surviving single-metric door: being transcendental/pseudo-")
print("differential it is NOT finitely localizable, so it genuinely exits the pincer (DC-001) rather than")
print("collapsing to DC-012 like the scale-split. PRICE: (i) a nonlocal slab initial-value problem, (ii) a")
print("mandatory retarded causal prescription that introduces one extra propagating mode omega^2=c^2k^2/2")
print("(non-tachyonic; ghost-residue = open), (iii) classical-effective-only status (no clean quantization),")
print("(iv) the lensing verdict must be RE-DERIVED nonlocally -- the pincer's under-lensing proof relied on")
print("LOCAL linear stress and a nonlocal (D_iD_j/box) operator can source Psi frame-free. Decisive next")
print("calc: does F+ give a GHOST-FREE, FRAME-FREE linear Psi source? That single computation opens or")
print("closes the last single-metric door.")
print('CERTIFICATE_JSON: {"gate":"PRICE-unlocalized-F+","status":"OPEN-PRICED","certificate":"Un-localized '
      'nonlocal F+ is transcendental/pseudo-differential (e^{-sqrt(-D^2)/2}) => NOT finitely localizable => '
      'genuinely EXITS the pincer (unlike scale-split->DC-012). PRICE: nonlocal slab IVP; mandatory retarded '
      'prescription => extra mode omega^2=c^2k^2/2 (non-tachyonic, ghost-residue open); classical-effective '
      'only. Lensing must be RE-DERIVED nonlocally (pincer under-lensing used LOCAL linear stress; a nonlocal '
      'D_iD_j/box operator CAN source Psi frame-free). DECISIVE OPEN CALC: ghost-free frame-free linear Psi '
      'source from F+?","assumptions":["F+ enters via a differential-operator argument Z~-D^2","banked '
      'localization dispersion omega^2=c^2k^2/2"],"numeric_values":{"extra_mode_omega2":"c^2 k^2/2","group_speed":"c/sqrt(2)"}}')
