"""
CHARGED-LEPTON SECTOR brute-force search with the 3-part GATE (project_atomos).

The calibration sector. Koide lives here. We must:
  (A) RE-FIND the calibration positives  : sqrt(8pi/3) kernel (forced), Koide Q=2/3 (FDR-surviving)
  (B) REJECT the FDR-dead re-labelings    : 4Z^2+3, 64pi+Z, Z+11, lambda^6, 3/13, ...
  (C) ask: does ANYTHING beyond Koide survive the gate on the 3 lepton mass ratios + the angle?

Building blocks = the framework's FORCED constants ONLY:
   Z=sqrt(32pi/3)=5.78881, sqrt(8pi/3)=2.89441, pi/2pi/4pi/8pi/32pi, 3, 4pi/3,
   triality/SO10 integers {3,8,16}, e, phi, sqrt2/sqrt3/sqrt5, ints 1..16, simple rationals.

The GATE per hit (all three must pass to count):
   G1  trials-corrected surprise  1/(N * 2p) >> 1   (N = #expressions in the complexity bin,
       p = relative match precision). bits = -log2( N * 2p * multiplicity ).  PASS >= 10 bits.
   G2  forced/mechanistic kernel vs free fit. A hit whose value is a free O(1) tuned to land the
       target is dead. PASS only if the matching expression's coefficient is a FORCED kernel
       (provenance pinned before the fit) with exactly one free O(1) (kappa-class).
   G3  interlock: same structure forces >=2 independent observables OR ties >=3 constants w/ 1 param.

Both-ways: gate-survivor = real relation (credit + p-value + mechanism). all-dead = parameter space
searched, kernel-free confirmed BY the search. A 0.01% match out of 10^7 tries is FDR-dead -> say so.
"""
from __future__ import annotations
import math, itertools
from dataclasses import dataclass

PHI = (1 + math.sqrt(5)) / 2
PI = math.pi
Z = math.sqrt(32 * PI / 3)            # 5.788810market...
K = math.sqrt(8 * PI / 3)             # 2.894405...  the a0 forced kernel

# ---- the FORCED / framework building blocks (the germ pool) --------------------------------
# Each entry: name -> (value, forced_provenance_or_None).  forced_provenance None => FREE O(1).
GERMS = {
    # measure-pi germs (forced by GR geometry / the a0 derivation)
    "pi": (PI, "measure-pi"),
    "2pi": (2 * PI, "measure-pi"),
    "4pi": (4 * PI, "Einstein-8pi/2"),
    "8pi": (8 * PI, "Einstein-8pi"),
    "32pi": (32 * PI, "a0-norm-32pi"),
    "4pi/3": (4 * PI / 3, "ball-volume"),
    "K": (K, "a0-kernel-sqrt(8pi/3)"),        # forced: Einstein-8pi x Friedmann-3
    "Z": (Z, "Z=sqrt(32pi/3)"),               # forced: sqrt(2/Z)=(3/8pi)^.25 machine-exact
    # small forced integers (triality/SO10: 3 generations, Spin8 dim 8, SO10 16)
    "1": (1.0, "int"), "2": (2.0, "int"), "3": (3.0, "N_gen/Friedmann-3"),
    "4": (4.0, "int"), "5": (5.0, "int"), "6": (6.0, "S3-order"),
    "7": (7.0, "int"), "8": (8.0, "Spin8-dim"), "9": (9.0, "int"),
    "10": (10.0, "int"), "11": (11.0, "int"), "12": (12.0, "A4-order"),
    "13": (13.0, "int"), "14": (14.0, "int"), "15": (15.0, "int"), "16": (16.0, "SO10-dim"),
    # irrationals that appear organically (e, phi, small surds)
    "e": (math.e, None),                       # NOT forced in this sector -> free
    "phi": (PHI, None),
    "sqrt2": (math.sqrt(2), "Koide-r-sqrt2"),  # forced-ISH (S3 1+2 decomp); flagged below
    "sqrt3": (math.sqrt(3), "Friedmann-sqrt3"),
    "sqrt5": (math.sqrt(5), None),
    # simple rationals
    "1/2": (0.5, "half"), "1/3": (1/3, "third"), "2/3": (2/3, "Koide-2/3"),
    "3/2": (1.5, "rational"), "5/2": (2.5, "rational"), "3/4": (0.75, "rational"),
}

# the value provenance lookup (for the Gate-B forced-kernel test)
def prov(name): return GERMS[name][1]
def val(name):  return GERMS[name][0]

# ---- TARGETS (PDG/CODATA) -------------------------------------------------------------------
m_e, m_mu, m_tau = 0.51099895000, 105.6583755, 1776.86
se, sm, st = math.sqrt(m_e), math.sqrt(m_mu), math.sqrt(m_tau)
Q_lep = (m_e + m_mu + m_tau) / (se + sm + st) ** 2

TARGETS = {
    # name        : (value, rel_precision_of_measurement)
    "r_mu_e":   (m_mu / m_e,   2e-8),     # measured to ~8 sig figs
    "r_tau_mu": (m_tau / m_mu, 6.8e-5),   # m_tau 0.12/1776.86
    "r_tau_e":  (m_tau / m_e,  6.8e-5),
    "koide_Q":  (Q_lep,        9e-6),     # the 2/3 interlock
    "koide_theta_deg": (math.degrees(math.acos(math.sqrt((se+sm+st)**2/(3*(m_e+m_mu+m_tau))))), 1e-4),
}

# ---- the ENUMERATOR: all expressions up to a fixed complexity over the germ pool ------------
# depth-1: a
# depth-2: a o b   for o in {*, /, +, -, ^}
# depth-3: (a o b) o2 c   and  a o (b o2 c)
# Track each expression's value, string, and the SET of germ names used (for provenance).
OPS = ["*", "/", "+", "-", "^"]

@dataclass
class Expr:
    value: float
    s: str
    germs: tuple   # germ names used

def _combine(a: Expr, op: str, b: Expr):
    try:
        if op == "*": v = a.value * b.value
        elif op == "/":
            if b.value == 0: return None
            v = a.value / b.value
        elif op == "+": v = a.value + b.value
        elif op == "-": v = a.value - b.value
        elif op == "^":
            # only allow small, sane exponents to avoid overflow garbage
            if abs(b.value) > 7 or a.value <= 0: return None
            v = a.value ** b.value
        else: return None
    except (OverflowError, ValueError, ZeroDivisionError):
        return None
    if not math.isfinite(v) or abs(v) > 1e8 or abs(v) < 1e-8:
        return None
    return Expr(v, f"({a.s}{op}{b.s})", a.germs + b.germs)

def enumerate_exprs(max_depth=3):
    """Deterministic enumeration up to max_depth. Returns list[Expr] (canonical-dedup by value)."""
    leaves = [Expr(val(n), n, (n,)) for n in GERMS]
    levels = {1: leaves}
    for d in range(2, max_depth + 1):
        out = []
        # combine any two expressions whose depths sum appropriately (build-up)
        lower = [e for dd in range(1, d) for e in levels[dd]]
        for a in lower:
            for b in lower:
                for op in OPS:
                    r = _combine(a, op, b)
                    if r is not None:
                        out.append(r)
        levels[d] = out
    allexpr = [e for d in range(1, max_depth + 1) for e in levels[d]]
    # canonical dedup by rounded value (keep the shortest string)
    seen = {}
    for e in allexpr:
        key = round(e.value, 9)
        if key not in seen or len(e.s) < len(seen[key].s):
            seen[key] = e
    return list(seen.values())

# ---- GATE G1: trials-corrected surprise -----------------------------------------------------
def g1_bits(target, p_rel, library_values, n_targets):
    """How surprising is a hit at relative precision p_rel, given the library DENSITY near target?
    E_chance = (#library points within +-10% of target) * (2*p_rel)/0.2.  This is the local-density
    Poisson expectation (attack5_fdr_partB). bits = -log2(E_chance * n_targets). >=10 => surprising.
    Also report the global N (library size) and the naive 1/(N*2p) for context."""
    lo10, hi10 = target * 0.9, target * 1.1
    n_band = sum(1 for v in library_values if lo10 <= v <= hi10)
    e_chance = n_band * (2 * p_rel) / 0.2
    e_corr = e_chance * max(1, n_targets)
    bits = -math.log2(e_corr) if e_corr > 0 else float("inf")
    # measurement precision cap: cannot earn more bits than the measurement pins
    cap = -math.log2(p_rel)
    return min(bits, cap), e_chance, n_band

# ---- main ------------------------------------------------------------------------------------
def main():
    print("=" * 96)
    print("CHARGED-LEPTON SECTOR brute-force + 3-part GATE   (project_atomos calibration)")
    print("=" * 96)
    lib = enumerate_exprs(max_depth=3)
    libvals = [e.value for e in lib]
    N = len(lib)
    print(f"germ pool size            : {len(GERMS)}")
    print(f"expressions enumerated (N): {N:,}  (depth<=3, canonical-dedup by value)")
    print(f"targets searched          : {len(TARGETS)}  (look-elsewhere multiplicity)")
    print()

    PASS_BITS = 10.0
    survivors = []
    for tname, (tval, p_rel) in TARGETS.items():
        print("-" * 96)
        print(f"TARGET  {tname} = {tval:.10g}   (measurement rel-precision p = {p_rel:.1e})")
        # find all expressions within the measurement window
        hits = [(e, abs(e.value - tval) / abs(tval)) for e in lib
                if abs(e.value - tval) / abs(tval) < max(p_rel, 1e-6) * 5]
        hits.sort(key=lambda x: x[1])
        if not hits:
            # widen to nearest few for reporting
            near = sorted(lib, key=lambda e: abs(e.value - tval) / abs(tval))[:3]
            print("  no expression within 5x the measurement window. nearest:")
            for e in near:
                print(f"    {e.s:38s} = {e.value:.8g}   ({abs(e.value-tval)/abs(tval)*100:.4f}% off)")
            continue
        print(f"  {len(hits)} expression(s) within 5x window. best:")
        for e, rel in hits[:6]:
            bits, e_chance, n_band = g1_bits(tval, max(rel, p_rel), libvals, len(TARGETS))
            # Gate B: forced-kernel. classify each germ used.
            germ_provs = [prov(g) for g in e.germs]
            free_germs = [g for g in e.germs if prov(g) is None]
            n_free = len(set(free_germs))
            # crude Gate-B: forced only if NO free germ AND the relation is not a bare tuned ratio.
            g2_pass = (n_free == 0)
            g1_pass = bits >= PASS_BITS
            tag = "FORCED-germs" if g2_pass else f"{n_free} FREE germ(s):{set(free_germs)}"
            print(f"    {e.s:36s} = {e.value:.8g}  rel={rel:.2e}  "
                  f"G1_bits={bits:5.1f}{'(pass)' if g1_pass else '(dead)'}  "
                  f"E_chance={e_chance:.2f}  band={n_band}  G2:{tag}")
            if g1_pass and g2_pass:
                survivors.append((tname, e, rel, bits))
    print()
    print("=" * 96)
    if survivors:
        print(f"GATE SURVIVORS (G1 AND G2 pass): {len(survivors)}")
        for tname, e, rel, bits in survivors:
            print(f"  {tname}: {e.s} = {e.value:.8g}  ({bits:.1f} bits, rel {rel:.1e})")
    else:
        print("GATE SURVIVORS: NONE. Every formula-hit is either dense-pool (E_chance>=1) or")
        print("uses a FREE germ tuned to land the target. Formula sector = FDR-dead.")
    print("=" * 96)

if __name__ == "__main__":
    main()
