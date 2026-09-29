#!/usr/bin/env python3
"""CFG55's 'Salpeter population masses' row under its two readings (post hoc, reported only; CFG55's outputs are untouched).

CFG55's README gives the row (+0.049 / -0.033, canonical) without defining the masses; CFG76's independent code got +0.076 / +0.021.
Both use ATLAS3D's (M/L)_Salp x L_r, moved to the SLUGGS distance at fixed M/L (L ~ D^2).  They differ in how the mass is used:
  (a) CFG55: the Salpeter mass IS the stellar mass (a population mass; no kinematic calibration);
  (b) CFG76: the Salpeter mass is the calibration target in place of M_JAM (nu M_*/2 = M_Salp/2, and the rule's debris likewise).
This script executes CFG55's committed source read-only up to its results block and evaluates both with CFG55's own functions.
Run: python3 campaign_fresh_gravity/CFG55_salpeter_definition_check.py
"""
import os, sys, io, contextlib

os.environ["MUTATE"] = "0"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
p = os.path.join(HERE, "CFG55_sluggs_dynamical_masses.py")
src = open(p).read()
ns = {"__file__": p, "__name__": "cfg55"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("\nRES = {}\n")], p, "exec"), ns)
G16, sample, law_mass_g, rule_mass = ns["G16"], ns["sample"], ns["law_mass_g"], ns["rule_mass"]

lines = ["CFG55's Salpeter population row under its two readings (canonical footing; mean offset +- galaxy-to-galaxy error, dex)",
         f"  sample: CFG55's {len(G16)} galaxies"]
ms = [g["Msalp"] for g in G16]
a = {w: sample("canonical", ms, w)[1:] for w in ("law", "rule")}
lines.append(f"  (a) Salpeter mass used directly as M_* (CFG55's row): law {a['law'][0]:+.4f} +- {a['law'][1]:.4f}; "
             f"rule {a['rule'][0]:+.4f} +- {a['rule'][1]:.4f}")
G2 = [dict(g, Mjam=g["Msalp"]) for g in G16]
bl = sample("canonical", [law_mass_g(g, "canonical", 0.5) for g in G2], "law")[1:]
br = sample("canonical", [rule_mass(g, "canonical", 0.5) for g in G2], "rule")[1:]
lines.append(f"  (b) Salpeter mass as the calibration target in place of M_JAM (CFG76's reading): law {bl[0]:+.4f} +- {bl[1]:.4f}; "
             f"rule {br[0]:+.4f} +- {br[1]:.4f}")
ok = abs(a["law"][0] - 0.049) < 5e-4 and abs(a["rule"][0] + 0.033) < 5e-4 and abs(bl[0] - 0.076) < 5e-4 and abs(br[0] - 0.021) < 5e-4
lines.append(f"  (a) reproduces CFG55's committed +0.049 / -0.033 and (b) CFG76's +0.076 / +0.021 at the printed precision: {'YES' if ok else 'NO'}")
out = "\n".join(lines)
print(out)
with open(os.path.join(HERE, "CFG55_salpeter_definition_check.out"), "w") as f:
    f.write(out + "\n")
sys.exit(0 if ok else 1)
