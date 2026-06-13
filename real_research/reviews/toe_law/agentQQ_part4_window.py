import sympy as sp
import numpy as np

print("="*78)
print("PART 4 — THE WINDOW: s6>0 that bounds the fold (no ghost) AND keeps inflection k*")
print("="*78)

c2v, s4v = 1.0, -0.5
thr = s4v**2/(4*c2v)
print(f"c2={c2v}, s4={s4v} => no-ghost threshold s6* = s4^2/(4c2) = {thr}\n")

def om2(u, s6):  # u=k^2
    return c2v*u + s4v*u**2 + s6*u**3
def om2_over_u(uu, s6):  # ghost test poly s6 u^2+s4 u+c2
    return s6*uu**2 + s4v*uu + c2v

print(f"{'s6':>8} | {'ghost?':>7} | {'inflection u*=k*^2 (om2>0)':>27} | {'k*':>7} | {'om2(k*)':>9}")
print("-"*72)
for s6 in [0.05, 0.06, 0.0625, 0.063, 0.07, 0.08, 0.10, 0.15, 0.25, 0.5, 1.0]:
    # ghost: min of s6 u^2+s4 u+c2 at u=-s4/(2 s6)
    ustar_g = -s4v/(2*s6)
    ghost = "YES" if om2_over_u(ustar_g, s6) < 0 else "no"
    # inflection cubic in u: 6 s6^2 u^3 + 9 s4 s6 u^2 + (10 c2 s6 + 2 s4^2) u + 3 c2 s4
    coeffs = [6*s6**2, 9*s4v*s6, 10*c2v*s6 + 2*s4v**2, 3*c2v*s4v]
    rts = np.roots(coeffs)
    found = "NONE"; kstar=""; om2k=""
    for r in sorted(rts, key=lambda z: z.real):
        if abs(r.imag) < 1e-9 and r.real > 0:
            uu = r.real
            o2 = om2(uu, s6)
            if o2 > 0:
                found = f"{uu:.4f}"; kstar=f"{uu**0.5:.4f}"; om2k=f"{o2:.4f}"
                break
    print(f"{s6:>8.4f} | {ghost:>7} | {found:>27} | {kstar:>7} | {om2k:>9}")

print()
print("=> Read the transition across the no-ghost threshold s6*=0.0625.")
