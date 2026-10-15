"""CFG792 -- the hypothetical cold-energy ramjet, stress-tested.  Criteria: FROZEN_CRITERIA.md (7e9bf8cf4).
Run: python3 cfg792.py   (CFG792_MUTATE=1: rho_c -> 0).  Seconds.  External inputs quoted from memory (provisional).
kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG792_MUTATE") == "1"
OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


c, G, MSUN, PC, YR = 2.99792458e8, 6.674e-11, 1.989e30, 3.0857e16, 3.156e7
RHO = 0.0 if MUT else 0.01 * MSUN / PC ** 3
U0 = RHO * c ** 2
V0 = 2.3e5
SIG = 1e-3                                   # kg/m^2
SB = 5.670e-8
mp, me = 1.6726e-27, 9.109e-31
R = {"lane": "CFG792", "mutate": MUT, "rho": RHO}
P("CFG792  hypothetical cold-energy ramjet: stress test" + ("  [MUTATE rho_c=0]" if MUT else ""))
P(f"  rho_c {RHO:.3e} kg/m^3, rho c^2 {U0:.3e} J/m^3, ambient flux rho c^2 v0 {U0 * V0:.2f} W/m^2")

# K1
tau0 = SIG / (RHO * c) / 86400 if RHO else float("inf")
k1 = MUT or abs(tau0 - 57.0) < 1.0
P(f"  K1 tau0 = {tau0:.1f} d (CFG791 57 d): {'PASS' if k1 else 'FAIL'}")

# F fuel identity
uF = (2e-10) ** 2 / (8 * math.pi * G)
ratio = U0 / uF if RHO else 0.0
P(f"\nF  rest-mass reading {U0:.2e} J/m^3 vs field-energy reading g^2/8piG {uF:.2e} J/m^3 -> ratio {ratio:.2e}")
P(f"   alpha Cen (1 g/m^2, eta 1): rest-mass 2.1 yr ship (CFG791); field reading: e-fold {tau0 * ratio / 365.25:.2e} yr -> no trip")
R["F"] = dict(u_rest=U0, u_field=uF, ratio=ratio)

# N natural matter
flux = U0 * V0
glob = flux / 4                                 # sphere-averaged
down = glob / 2                                 # isotropic emission: half reaches the ground
lux = down * 93.0
ex_sky = lux / 1e-3
earth = flux * math.pi * 6.371e6 ** 2
ex_heat = earth / 47e12
clsN = "MATERIAL PORTAL EXCLUDED" if max(ex_sky, ex_heat) > 10 else "ALLOWED"
P(f"\nN  material portal: Earth intercepts {earth:.2e} W (heat flow x{ex_heat:.0f}); ground light {down:.2f} W/m^2 = {lux:.0f} lux"
  f" vs night sky 1e-3 lux -> x{ex_sky:.1e}  => {clsN}; natural-matter suppression needed >= {ex_sky:.0e}")
P(f"   (a 1 g/m^2 sheet of the design material facing the apex would glow at {flux:.0f} W/m^2 ~ {flux * 93:.0f} lux)")
R["N"] = dict(earth_W=earth, x_heat=ex_heat, lux=lux, x_sky=ex_sky, cls=clsN)

# S stimulation
d = SIG / 2000.0
tdev = d / V0
S = 4.4e15 * YR / tdev
P(f"\nS  device thickness {d * 1e6:.2f} um, crossing {tdev:.1e} s, tau_dev (eta 1) {tdev:.1e} s; stimulation over CFG789 bound S = {S:.1e}")
R["S"] = dict(tdev=tdev, S=S)

# T thermal
P("\nT  sail temperature (both faces, eps 1)")
R["T"] = {}
worst = 0.0
for b in (0.1, 0.5, 0.9, 0.998):
    g2 = 1 / (1 - b * b)
    q = g2 * U0 * b * c
    row = {}
    for w in (0.01, 0.1, 1.0):
        T = (w * q / (2 * SB)) ** 0.25
        row[str(w)] = T
    worst = max(worst, row["0.1"])
    R["T"][str(b)] = dict(q=q, **row)
    P(f"   beta {b}: intake {q:.2e} W/m^2; T(w .01/.1/1) = {row['0.01']:.0f} / {row['0.1']:.0f} / {row['1.0']:.0f} K")
P(f"   class (w=0.1): {'OK' if worst < 2000 else 'LIMIT'}  (w=1 at the end: LIMIT); Lambertian emission = 2/3 of collimated thrust")


# I interstellar gas
def bethe(b):  # MeV cm^2/g, carbon (Z/A 0.5, I 78 eV)
    g = 1 / math.sqrt(1 - b * b)
    return 0.307 * 0.5 / b ** 2 * (math.log(2 * 0.511e6 * b * b * g * g / 78.0) - b * b)


bk2 = math.sqrt(1 - (1 / (1 + 100 / 938.272)) ** 2)
k2 = abs(bethe(bk2) - 6.4) / 6.4 < 0.2
P(f"\n  K2 Bethe 100 MeV p in C: {bethe(bk2):.2f} MeV cm^2/g vs 6.4: {'PASS' if k2 else 'FAIL'}")
n, rI = 1e6, 1e6 * mp
P("I  ISM (1 proton/cm^3); sail 0.1 mg/cm^2")
R["I"] = {}
okI = True
for b in (0.001, 0.01, 0.02, 0.1, 0.5, 0.9, 0.998):
    g = 1 / math.sqrt(1 - b * b)
    KE = (g - 1) * 938.272                                       # MeV
    if b < 0.02:
        drag = rI * g * g * (b * c) ** 2; heatI = n * b * c * KE * 1.602e-13; mode = "stops"
    else:
        dE = min(bethe(b) * 1e-4, KE); drag = n * b * c * dE * 1.602e-13 / c * 1; heatI = n * b * c * dE * 1.602e-13; mode = "passes"
    thrust = U0 * g * g * b / (1 + b) if RHO else 0.0   # eta 1 force per area (CFG791 form, rho A gamma^2 v (c - v) ~)
    thrust = RHO * g * g * b * c * (c - b * c)
    heatC = 0.01 * g * g * U0 * b * c
    rd = drag / thrust if thrust else float("inf"); rh = heatI / heatC if heatC else float("inf")
    okI &= (rd < 1 and rh < 1) or MUT
    R["I"][str(b)] = dict(mode=mode, drag_over_thrust=rd, heat_over_cold=rh)
    P(f"   beta {b:<6}: protons {mode:6s}; drag/thrust {rd:.1e}; heat_ISM/heat_cold(w .01) {rh:.1e}")
P(f"   class: {'OK' if okI else 'LIMIT'}")
P("\nD  dark energy (w=-1) is the same in every frame: no ram, no drag; converter = photon rocket with ambient fuel, thrust P/c,"
  f" power set by device volume. rho_DE c^2 = 4 a0^2/G = {4 * (1.13e-10) ** 2 / G:.1e} J/m^3 (alt footing).")
R.update(K1=bool(k1), K2=bool(k2), clsI="OK" if okI else "LIMIT")
if MUT:
    P(f"  MUTATE: N excess {ex_sky:.1e}, cold heat 0 -> {'bites' if ex_sky == 0 else 'DID NOT BITE'}")
sfx = "_MUTATE" if MUT else ""
json.dump(R, open(os.path.join(HERE, f"cfg792_results{sfx}.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg792{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
