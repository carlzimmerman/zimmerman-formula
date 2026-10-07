#!/usr/bin/env python3
"""SCAN 10-07: is the cold fluid's amount tied to kappa by y_H = ln(1 + Om_b/Om_c)?
y_H = g_N,baryons(R_H)/a0 = Om_b c H0 / (2 a0) (homogeneous baryon sphere at the Hubble radius); the supply-edge exponent is
s = ln(1 + Om_b/Om_c) (T10 / CFG423 edge).  Planck 2018 numbers; a0 = kappa c sqrt(G rho_L).  Checks the match, the kappa it implies,
what it reduces to, and whether it can hold at more than one epoch (Om_b/Om_c is fixed, y_H(z) is not)."""
import math
h, obh2, och2, OL = 0.6736, 0.02237, 0.1200, 0.6847
ob, oc = obh2 / h**2, och2 / h**2; om = 1 - OL
A0H = lambda k: k * math.sqrt(3 * OL / (8 * math.pi))          # a0/(c H0) on the rho_L footing
s = math.log(1 + ob / oc)
L = []
def P(x): print(x); L.append(x)
P(f"Om_b {ob:.5f}  Om_c {oc:.5f}  s = ln(1+Om_b/Om_c) = {s:.5f}")
for k in (0.5, 0.465, 0.53, 0.55):
    yH = ob / (2 * A0H(k)); P(f"  kappa {k:5.3f}: y_H = {yH:.5f}  (y_H/s = {yH/s:.4f})")
kneed = ob / (2 * math.sqrt(3 * OL / (8 * math.pi)) * s)
P(f"kappa implied by y_H = s: {kneed:.4f}  (record: 0.465 +- 0.076 / 0.55 +- 0.17; 1% match is far inside kappa's own error, so untestable)")
P(f"exact-kernel version (g_obs at edge = a0 s^2/f_b): kappa implied {0.5 * (ob / (2 * A0H(0.5))) / (s**2 * (ob + oc) / ob):.4f}  -> the 'match' moves 8% with the reading")
P(f"reduction: Om_b/(2 ln(1+Om_b/Om_c)) = {ob / (2 * s):.4f} ~ (Om_c + Om_b/2)/2 = {(oc + ob / 2) / 2:.4f}; a0/(cH0) at kappa=1/2 = {A0H(0.5):.4f}; 1/(2 pi) = {1 / (2 * math.pi):.4f}; Om_m/2 = {om / 2:.4f}")
P("  i.e. it is the old a0 ~ c H0/2pi coincidence written through Om_m ~ 1/pi, not a new relation.")
P("epoch test (Om_b/Om_c fixed; a0 flat): y_H(z)/y_H(0) = Om_b(z) H(z) / (Om_b H0) = (1+z)^3 H0/H(z)")
for z in (0.5, 1.0, 2.0):
    E = math.sqrt(om * (1 + z)**3 + OL); P(f"  z {z}: y_H ratio {(1 + z)**3 / E:.3f}")
P("VERDICT: NUMEROLOGY, TODAY-ONLY. The 1% match holds only at z = 0 (y_H doubles by z = 0.5) and is the a0 ~ cH0/2pi coincidence")
P("re-expressed; it does not tie the amount to kappa. Recorded so it is not re-chased.")
open("scan_cosmic_supply.out", "w").write("\n".join(L) + "\n")
