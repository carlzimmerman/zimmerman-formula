#!/usr/bin/env python3
"""u2_2 -- does a unit winding of the capped condensate have a Coulomb far field?  (U2 definition D1: e_far^2 = lim d U(d).)
Pre-registered in U2_PREREGISTRATION.md (written before this ran).

U(d)/F^2 = pi * oint oint dl1.dl2 / |r1 - r2|   (Neumann energy of two unit-winding filaments; rho Gamma^2 = 4 pi^2 F^2; classical result recalled, not derived here).
Units: F^2 = 1, ring radius a = 1.

Run:      PYTHONDONTWRITEBYTECODE=1 python3 u2_2_vortex_far_field.py            (exit 0 iff all checks pass)
Control:  PYTHONDONTWRITEBYTECODE=1 python3 u2_2_vortex_far_field.py --mutate   (swaps the closed ring for an open segment in B1/B2; the monopole-is-zero checks must FAIL; exit 1)
"""
import sys
sys.dont_write_bytecode = True
import mpmath as mp
import sympy as sp

MUT = "--mutate" in sys.argv
mp.mp.dps = 30
CH = []


def chk(tag, ok, detail=""):
    CH.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


# ------------------------------------------------------------------ B1 closure (sympy)
phi, ell, a_ = sp.symbols("phi ell a", positive=True)
if not MUT:
    dl = sp.Matrix([-a_ * sp.sin(phi), a_ * sp.cos(phi), 0])          # ring, d r/d phi
    total = sp.simplify(sp.Matrix([sp.integrate(dl[i], (phi, 0, 2 * sp.pi)) for i in range(3)]))
    shape = "closed ring"
else:
    total = sp.Matrix([0, 0, ell])                                       # an open straight segment of length ell along z
    shape = "OPEN SEGMENT (mutated)"
print(f"U2 / u2_2: far field of a unit winding. shape used for B1/B2: {shape}")
chk("B1 oint dl = 0 (so the Coulomb 1/d coefficient (oint dl1).(oint dl2) vanishes)", total == sp.zeros(3, 1), f"(oint dl = {list(total)})")


# ------------------------------------------------------------------ B2 coaxial rings (or segments) Neumann energy
def U_rings(d):
    """U/F^2 for two coaxial rings, a = 1, separation d: 2 pi^2 int_0^{2pi} cos(psi)/sqrt(2(1-cos psi)+d^2) dpsi."""
    return 2 * mp.pi ** 2 * mp.quad(lambda p: mp.cos(p) / mp.sqrt(2 * (1 - mp.cos(p)) + d * d), [0, mp.pi, 2 * mp.pi])


def U_segments(d, l=1):
    """U/F^2 for two parallel open segments of length l at perpendicular separation d, aligned: pi int int ds ds'/sqrt((s-s')^2 + d^2)."""
    return mp.pi * mp.quad(lambda s, t: 1 / mp.sqrt((s - t) ** 2 + d * d), [0, l], [0, l])


U = U_segments if MUT else U_rings
ds = [mp.mpf(v) for v in (10, 30, 100, 300, 1000)]
vals = [U(d) for d in ds]
print("\nB2 Neumann energy U(d)/F^2 (a = 1):")
for d, v in zip(ds, vals):
    print(f"    d/a = {mp.nstr(d, 5):>6s}   U = {mp.nstr(v, 10):>16s}   d*U = {mp.nstr(d * v, 10):>16s}   U d^3/(2 pi^3) = {mp.nstr(v * d ** 3 / (2 * mp.pi ** 3), 10)}")
# local exponent at the two largest d
n_loc = (mp.log(vals[-1]) - mp.log(vals[-2])) / (mp.log(ds[-1]) - mp.log(ds[-2]))
print(f"    local exponent d ln U / d ln d between d = 300 and 1000: {mp.nstr(n_loc, 8)}")
chk("B2a local exponent is -3.000 +- 0.02 (dipole-dipole)", abs(n_loc + 3) < 0.02, f"(exponent = {mp.nstr(n_loc, 6)})")
coef = vals[-1] * ds[-1] ** 3 / (2 * mp.pi ** 3)
chk("B2b U d^3 / (2 pi^3 F^2 a^4) -> 1 to 1e-3 at d/a = 1000", abs(coef - 1) < 1e-3, f"(= {mp.nstr(coef, 8)})")
e_far2 = ds[-1] * vals[-1]
chk("B2c d*U falls as d^-2 (>= 50x smaller at d = 1000 than at d = 100, expected 100x), so D1 e_far^2 = lim d U = 0", (ds[-1] * vals[-1]) < (ds[2] * vals[2]) / 50,
    f"(d U at 100: {mp.nstr(ds[2] * vals[2], 6)}, at 1000: {mp.nstr(e_far2, 6)})")

# ------------------------------------------------------------------ B3 independent Stokes flux check (uses the Biot-Savart velocity, not the double line integral)
mp.mp.dps = 15


def vz(rho, z, a=1.0):
    return (1 / (4 * mp.pi)) * mp.quad(lambda p: (a * a - a * rho * mp.cos(p)) / (rho * rho + a * a - 2 * a * rho * mp.cos(p) + z * z) ** 1.5, [0, mp.pi, 2 * mp.pi])


print("\nB3 Stokes flux check (Gamma = 1; U/F^2 = 4 pi^2 Phi/Gamma):")
okB3 = True
if not MUT:
    for dd in (3, 10):
        flux = mp.quad(lambda r: 2 * mp.pi * r * vz(r, dd), [0, 1])
        u_flux = 4 * mp.pi ** 2 * flux
        mp.mp.dps = 30
        u_dbl = U_rings(mp.mpf(dd))
        mp.mp.dps = 15
        rel = abs(u_flux / u_dbl - 1)
        okB3 &= rel < 1e-6
        print(f"    d = {dd}: 4 pi^2 Phi = {mp.nstr(u_flux, 12)}   Neumann double integral = {mp.nstr(u_dbl, 12)}   rel diff = {mp.nstr(rel, 3)}")
    chk("B3 flux of ring 2's velocity through ring 1's disk reproduces the Neumann energy to 1e-6", okB3)
else:
    print("    (skipped in the mutated control)")
    chk("B3 (skipped under --mutate; counted as pass)", True)

# ------------------------------------------------------------------ B4 on-axis velocity of a ring: dipole far field
print("\nB4 on-axis velocity of a ring (Gamma = 1, a = 1): closed form Gamma a^2 / (2 (a^2 + z^2)^(3/2))")
okB4 = True
zs = [mp.mpf(v) for v in (10, 100, 1000)]
vs = []
for z in zs:
    num = vz(mp.mpf(0), z)
    cf = 1 / (2 * (1 + z * z) ** mp.mpf(1.5))
    okB4 &= abs(num / cf - 1) < 1e-10
    vs.append(num)
    print(f"    z = {mp.nstr(z, 5):>6s}: numeric = {mp.nstr(num, 12)}, closed form = {mp.nstr(cf, 12)}")
n_axis = (mp.log(vs[-1]) - mp.log(vs[-2])) / (mp.log(zs[-1]) - mp.log(zs[-2]))
chk("B4 numeric Biot-Savart equals the closed form (1e-10) and the far-field exponent is -3.000 +- 0.01 (a dipole field, not the 1/r^2 of a monopole)", okB4 and abs(n_axis + 3) < 0.01, f"(exponent = {mp.nstr(n_axis, 6)})")

# ------------------------------------------------------------------ B5 what a Coulomb charge would need (the bypass D2 assumes)
mp.mp.dps = 20
d5 = mp.mpf(1000)
u5 = U_segments(d5)
n5 = (mp.log(U_segments(mp.mpf(1000))) - mp.log(U_segments(mp.mpf(300)))) / (mp.log(mp.mpf(1000)) - mp.log(mp.mpf(300)))
print(f"\nB5 open parallel segments (l = 1): U d /(pi F^2 l^2) at d = 1000 = {mp.nstr(u5 * d5 / mp.pi, 10)},  local exponent {mp.nstr(n5, 6)}")
chk("B5 open segments DO give a Coulomb law U -> pi F^2 l^2/d (exponent -1.000 +- 0.005, coefficient 1 to 1e-6): that is the D2 bypass, and it needs div(omega) != 0 (a line ending in the fluid), which a phase-winding cannot have",
    abs(n5 + 1) < 0.005 and abs(u5 * d5 / mp.pi - 1) < 1e-6, f"(exponent {mp.nstr(n5, 6)})")

n_fail = CH.count(False)
print(f"\nchecks: {len(CH) - n_fail}/{len(CH)} pass")
print("\nVERDICT (against the pre-registered criteria):")
print("  D1: the interaction energy of two unit-winding rings is dipole-dipole, U ~ 2 pi^3 F^2 a^4/d^3; the 1/d coefficient is (oint dl1).(oint dl2) = 0 exactly (Helmholtz: vorticity has no sources).")
print("  So e_far = 0: a closed unit winding of a phase field has NO Coulomb charge. The winding-charge model has no charge quantum at large distance and dies at step (iii).")
print("  A Coulomb 1/d needs open segments (B5), i.e. a monopole source of vorticity, which the U(1) phase does not have; that is the bypass behind D2, not part of the model.")
if MUT:
    print("\nMUTATE CONTROL: an open segment replaces the ring; the closure and dipole checks (B1, B2a, B2b, B2c) must FAIL.")
    ok = (not CH[0]) and (not CH[1]) and (not CH[2]) and (not CH[3])
    print("  " + ("FAILED as required -- the control works (exit 1)" if ok else "DID NOT FAIL -- the control is broken"))
    sys.exit(1 if ok else 0)
sys.exit(0 if n_fail == 0 else 1)
