#!/usr/bin/env python3
"""targets_zimmerman.py -- the framework's own numbers, as generators AND as targets.

'grade' is the tautology guard (T061's classifier, applied up front):
  MEASURED    -- has an error bar; a match against it is potentially contentful
  DERIVED     -- computed from the framework; matches often restate the derivation
  CONVENTION  -- definitional (Z = sqrt(32 pi/3)/... etc.); matches are TAUTOLOGIES
Searches must never count a CONVENTION-target match as a hit; the engine tags them.
"""
ZIMMERMAN = {
    "kappa_meas":  dict(v=0.551,      s=0.043,  grade="MEASURED",   note="distance-free kappa"),
    "kappa_adopt": dict(v=0.5,        s=None,   grade="CONVENTION", note="adopted 1/2"),
    "Z_const":     dict(v=5.788805,   s=None,   grade="CONVENTION", note="sqrt(32 pi / 3)"),
    "a0_can":      dict(v=9.3619e-11, s=None,   grade="DERIVED",    note="canonical footing, m/s^2"),
    "a0_alt":      dict(v=1.1279e-10, s=None,   grade="DERIVED",    note="alt footing, m/s^2"),
    "nu0_lo":      dict(v=2.14e-5,    s=None,   grade="DERIVED",    note="charge window floor (stage17)"),
    "nu0_hi":      dict(v=1.77e-4,    s=None,   grade="DERIVED",    note="charge window ceiling"),
    "Q0_lo":       dict(v=0.0024,     s=None,   grade="DERIVED",    note="pinned band low edge, Mpc^-1"),
    "Q0_hi":       dict(v=0.0146,     s=None,   grade="DERIVED",    note="pinned band high edge"),
    "R_dm":        dict(v=0.387,      s=0.006,  grade="MEASURED",   note="Omega_dm/Omega_Lambda"),
    "L0_tensor":   dict(v=0.3674,     s=None,   grade="DERIVED",    note="EFE response anisotropy (kernel tautology risk)"),
    "nu0_kernel":  dict(v=1.4732,     s=None,   grade="DERIVED",    note="nu(y_ext) at solar circle (same risk)"),
    "sqrt_pi":     dict(v=1.7724539,  s=None,   grade="CONVENTION", note="the transcendental Z carries"),
}
# generator packs for the engine (--pack):
PACKS = {
    "base":  [("1", 1.0), ("2", 2.0), ("3", 3.0), ("5", 5.0), ("pi", 3.141592653589793),
              ("e", 2.718281828459045)],
    "zimm":  [("1", 1.0), ("2", 2.0), ("3", 3.0), ("pi", 3.141592653589793),
              ("kappa", 0.5), ("Z", 5.788805), ("sqrtpi", 1.7724539), ("Rdm", 0.387)],
    "angle": [("1", 1.0), ("2", 2.0), ("3", 3.0), ("5", 5.0), ("pi", 3.141592653589793),
              ("phi", 1.618033988749895)],
}
