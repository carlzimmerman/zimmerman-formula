"""CFG796 -- where can a cold-energy converter live?  Criteria: FROZEN_CRITERIA.md.  Theory only, seconds.
Run: python3 cfg796.py   (CFG796_MUTATE=1: L* = 0).  kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG796_MUTATE") == "1"
OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


c, G, hbar, PC, AU, YR, MSUN = 2.99792458e8, 6.674e-11, 1.054571817e-34, 3.0857e16, 1.496e11, 3.156e7, 1.989e30
LS = 0.0 if MUT else 5.75 * PC
rho = 0.01 * MSUN / PC ** 3
v = 2.3e5
P("CFG796  where can a cold-energy converter live?" + ("  [MUTATE L*=0]" if MUT else ""))
PH = lambda M: hbar * c ** 6 / (15360 * math.pi * G ** 2 * M ** 2)
k1 = abs(PH(1e9) / 3.56e14 - 1) < 0.01
k2 = MUT or abs(LS / AU / 1.19e6 - 1) < 0.01
P(f"  K1 Hawking P(1e9 kg) = {PH(1e9):.3e} W: {'PASS' if k1 else 'FAIL'};  K2 L*/AU = {LS / AU:.3e}: {'PASS' if k2 else 'FAIL'}")

uF = (2e-10) ** 2 / (8 * math.pi * G)
P(f"\n1 polarization identity: field energy {uF:.2e} J/m^3 = 1/{rho * c ** 2 / uF:.2e} of rest mass")
pen = {}
for lab, l in (("1 m", 1.0), ("1 km", 1e3), ("1 AU", AU)):
    pen[lab] = (LS / l) ** 2
    P(f"   depolarize over {lab:5s}: stiffness penalty (L*/l)^2 = {pen[lab]:.1e}")
c1 = "DEVICE-REACHABLE" if pen["1 AU"] < 1 else "FORBIDDEN BY STIFFNESS"
P(f"   -> {c1}")
P("\n2 new local sink in ordinary matter: no term in the record; must be >=2e5 off in natural matter (CFG792) and stimulated ~1e34"
  " with no known means (CFG794) -> UNMOTIVATED")
P("\n3 horizon sink (record: black holes convert cold mass to dark energy, PAPER50):")
H = {}
for M in (1e8, 1e9, 1e10):
    p = PH(M); life = 5120 * math.pi * G ** 2 * M ** 3 / (hbar * c ** 4) / YR
    rs = 2 * G * M / c ** 2
    intake = 16 * math.pi * G ** 2 * M ** 2 * rho / (c ** 2 * v)
    frac = intake / (p / c ** 2)
    H[str(M)] = dict(P=p, life_yr=life, rs=rs, E_form=M * c ** 2, intake=intake, cold_frac=frac)
    P(f"   M {M:.0e} kg: Hawking {p:.1e} W, life {life:.1e} yr, r_s {rs:.1e} m, formation {M * c ** 2:.1e} J;"
      f" cold intake {intake:.1e} kg/s vs loss {p / c ** 2:.1e} kg/s -> cold fraction {frac:.0e}")
P("   -> CONVERTER EXISTS IN PRINCIPLE (a horizon), but its power comes from its own mass; cold energy supplies a negligible fraction")
R = dict(lane="CFG796", mutate=MUT, K1=bool(k1), K2=bool(k2), uF=uF, penalty=pen, branch1=c1, horizon=H)
if MUT:
    P(f"  MUTATE: branch 1 {c1} -> {'bites' if c1 == 'DEVICE-REACHABLE' else 'DID NOT BITE'}")
sfx = "_MUTATE" if MUT else ""
json.dump(R, open(os.path.join(HERE, f"cfg796_results{sfx}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg796{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
