#!/usr/bin/env python3
"""LMC1 lead's check, written 2026-11-12 AFTER the result was read. Not graded; changes no label.
Usage: python3 -I -B lmc1_lead_check.py     (reads lmc1_results.json beside it; runs no simulation)

L1  How far the model's noise leaves each frozen word from the central estimate: E1 with the error
    propagated from the three bins' bootstrap err_q, against the frozen boundaries 0.8 E0, 1.2 E0 and the
    value of E1 at which z1 = 1.
L2  The two-sigma bound on what the LMC does to the 30-40 kpc dispersion, in km/s.
L3  Does the model's dipole grow with the LMC's mass? Amplitudes and vectors at the four masses.
L4  The model's apex (minus the dipole vector) against the published reflex apex (l, b) = (56, -34), a
    PROVISIONAL look-up quoted in RESULT.md; angle between them for the central case and for the borrowed
    1.5e11 case (context only).
"""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "lmc1_results.json")))
OUT = open(os.path.join(HERE, "lmc1_lead_check.out"), "w")
def say(s=""):
    print(s); OUT.write(s + "\n")

say("LMC1 LEAD'S CHECK (after the result; not graded; changes no label)")
sig = [d["sigma"] for d in R["sample"]["disp"]]; E0 = R["sample"]["E0"]
say(f"observed dispersions {', '.join(f'{s:.2f}' for s in sig)}; E0 = {E0:.3f} km/s")
say("")
say("L1 / L2  central M_eff 2.5e10")
for ft in ("canonical", "alt"):
    F = R["footings"][ft]; Q = F["q"]["central"]; lab = F["label"]
    q = [x["q"] for x in Q]; e = [x["err"] for x in Q]
    E1 = sig[1] / q[1] - 0.5 * (sig[0] / q[0] + sig[2] / q[2])
    dE = math.sqrt((sig[1] * e[1] / q[1] ** 2) ** 2 + ((sig[0] * e[0] / q[0] ** 2) ** 2 + (sig[2] * e[2] / q[2] ** 2) ** 2) / 4)
    Ez1 = lab["E1"] / lab["z1"]
    say(f"  {ft}: E1 = {E1:.2f} (file {lab['E1']:.2f}) +/- {dE:.2f} from the model's noise alone")
    say(f"     LMC EXPLAINS THE BIN needs E1 < {Ez1:.2f} (z1 < 1): {(E1 - Ez1) / dE:.1f} model-noise sigma away")
    say(f"     LMC PART OF IT needs E1 <= {0.8 * E0:.2f}: {(E1 - 0.8 * E0) / dE:.1f} sigma away")
    say(f"     LMC MAKES IT WORSE needs E1 >= {1.2 * E0:.2f}: {(1.2 * E0 - E1) / dE:.1f} sigma away")
    lo, hi = sig[1] / (q[1] + 2 * e[1]) - sig[1], sig[1] / (q[1] - 2 * e[1]) - sig[1]
    say(f"     30-40 bin: q = {q[1]:.4f} +/- {e[1]:.4f}; corrected minus observed dispersion "
        f"{sig[1] / q[1] - sig[1]:+.2f} km/s, two-sigma range {lo:+.2f} to {hi:+.2f} km/s (the excess is {E0:.1f})")
say("")
say("L3  full-sky 50-80 kpc model dipole against the LMC's mass")
def unit(v):
    a = math.sqrt(sum(x * x for x in v)); return [x / a for x in v], a
pub = [math.cos(math.radians(-34)) * math.cos(math.radians(56)), math.cos(math.radians(-34)) * math.sin(math.radians(56)), math.sin(math.radians(-34))]
MASS = {"low": 1.6e10, "central": 2.5e10, "high": 4.0e10}
for ft in ("canonical", "alt"):
    rows = [(MASS[k], R["footings"][ft]["dip50"][k]) for k in ("low", "central", "high")] + [(1.5e11, R["mutations"][f"M1/{ft}"]["dip50"])]
    c = rows[1][1]["amp"]
    for M, d in rows:
        u, a = unit(d["vec"]); ang = math.degrees(math.acos(max(-1, min(1, -sum(x * y for x, y in zip(u, pub))))))
        say(f"  {ft} M = {M:.1e}: |d| = {a:5.2f} km/s, vector ({d['vec'][0]:+.2f}, {d['vec'][1]:+.2f}, {d['vec'][2]:+.2f}); "
            f"ratio to central {a / c:.2f} for a mass ratio {M / 2.5e10:.2f}; apex {ang:.0f} deg from the published one")
say("")
say("L4  reading: the dipole's vertical component has the published sign (northern stars receding) at every")
say("    mass, but the model's apex lies about 100 degrees from the published apex and the amplitude grows far")
say("    more slowly than the mass. The rigid model is therefore NOT validated against the measured reflex.")
say("")
say("L5  model-free ceiling: a pure dipole of amplitude A adds A^2 / 3 to a bin's variance. Removing a dipole of")
say("    the full published reflex amplitude (PROVISIONAL, measured beyond 40 kpc) from each bin:")
for A in (32.0, 36.0):
    c = [math.sqrt(s * s - A * A / 3) for s in sig[:3]]
    say(f"    A = {A:.0f} km/s: dispersions {c[0]:.2f}, {c[1]:.2f}, {c[2]:.2f} (changes {c[0] - sig[0]:+.2f}, {c[1] - sig[1]:+.2f}, {c[2] - sig[2]:+.2f}); "
        f"excess {c[1] - 0.5 * (c[0] + c[2]):.2f} against {E0:.2f}")
Aneed = math.sqrt(3 * (sig[1] ** 2 - (0.5 * (sig[0] + sig[2])) ** 2))
say(f"    a dipole in the 30-40 bin alone would need A = {Aneed:.0f} km/s to carry the whole excess.")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()
