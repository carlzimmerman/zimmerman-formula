#!/usr/bin/env python3
"""idea_seed.py -- the random seeding function.  Throws framework objects, SM constants,
and mathematical motifs into a short scrambled paragraph.  A later INTERPRETER session
(fresh context) reads ONE seed and turns it into a concrete falsifiable hypothesis; a
later REFEREE session (fresh context, sees ONLY the interpretation) grades it blind.
Deterministic per seed id.  Usage: python idea_seed.py [--n 2]
"""
import argparse, glob, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMEWORK = ["the shift charge Q0*n", "the DBI wall", "the nu0 window", "the drain flow",
             "the EFE response tensor (1.4732/0.3674)", "kappa = 0.551 +/- 0.043",
             "the a0-line g^2 - gb^2 = a0*gb", "the pinned Q0 band", "the aether tilt",
             "the pressure promotion A(Q) = kappa^2 G(-K)", "the binding-epoch wall z=10.8",
             "the y-gate", "R_dm = 0.387", "the off-switch at recombination",
             "Z = sqrt(32 pi/3) = 5.7888", "the golden-ratio point of the a0-line (g/gN = phi at y=1)",
             "w = -1 exact (the vacuum never rolls)", "the transition z_t = nu0^(-1/3) - 1 in [17,35]",
             "the X-pin (X = sqrt(y) c/v ~ 106-453)", "the fixed-point argument (drain vs pin)",
             "the conditional nu0-meter (DR4 as a charge gauge)", "kappa is pi-free (proven)",
             "the dust-mass-IS-the-charge theorem (rho/n = Q0)", "the Q/Y sector split (one field, two jobs)",
             "the two-footing fork (9.3619e-11 vs 1.1279e-10)", "the 0.108-dex RAR at Ups = 0.70",
             "the frozen wide-binary band 1.1614-1.1814", "the a0-bump cluster response (peaked at a0)",
             "M_lens/M_dyn = 29 at the f = 1/3 fixed point", "the 690-Gyr transport time"]
SM = ["the Cabibbo angle (0.2250)", "the Koide relation (2/3)", "sin^2 theta_W (0.2312)",
      "alpha^-1 = 137.036", "m_p/m_e = 1836.15", "the CKM CP phase (~1.14 rad)",
      "the PMNS solar angle (0.307)", "m_mu/m_e = 206.77", "the top Yukawa (~0.70)",
      "n_s = 0.9649", "m_W/m_Z (0.8814)"]
MOTIF = ["a fixed point of", "an averaging over structure of", "a boundary term ratio of",
         "the pi-free part of", "a footing-invariant combination of", "the drained remnant of",
         "a holonomy angle of", "the golden-ratio point of", "a polyhedral solid angle of",
         "spontaneous breaking of", "a duality exchanging", "the torsion of",
         "an entropy partition of", "the resonance condition between", "a projection of",
         "the continued fraction of", "a saturation bound on", "the beat frequency between"]
VERB = ["might set", "could renormalize into", "may be the shadow of", "might quantize",
        "could interpolate to", "may bound", "might select", "could be measured by"]


def make(seed_id):
    rng = random.Random(seed_id * 7919)
    f1, f2 = rng.sample(FRAMEWORK, 2)
    s1, s2 = rng.sample(SM, 2)
    m1, m2 = rng.sample(MOTIF, 2)
    v1, v2 = rng.sample(VERB, 2)
    lines = [
        f"SEED {seed_id:04d} (random collision -- interpret charitably, then test brutally)",
        f"* {m1} {f1} {v1} {s1}.",
        f"* {m2} {s2} {v2} {f2}.",
        f"* wildcard: what single dimensionless number would BOTH bullets share if true?",
    ]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2)
    a = ap.parse_args()
    pend = os.path.join(HERE, "seeds", "pending")
    os.makedirs(pend, exist_ok=True)
    existing = glob.glob(os.path.join(HERE, "seeds", "*", "seed_*.txt")) + \
        glob.glob(os.path.join(HERE, "seeds", "*", "interp_*.md"))
    nxt = 1 + max([int(os.path.basename(p).split("_")[1][:4]) for p in existing] or [0])
    for i in range(a.n):
        sid = nxt + i
        p = os.path.join(pend, f"seed_{sid:04d}.txt")
        open(p, "w").write(make(sid))
        print(f"[seed] wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
