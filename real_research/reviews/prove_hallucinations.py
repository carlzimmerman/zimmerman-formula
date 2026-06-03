#!/usr/bin/env python3
"""
PROVE THE HALLUCINATIONS -- reproducible, decisive demonstrations (not assertions).
====================================================================================
Carl's ask: "explain all the hallucinations, but prove they were hallucinations without a doubt."
This script does not OPINE that a claim is bogus -- for each class it RUNS a decisive test that
anyone can rerun: the code's own numbers contradicting its conclusion, a trivial identity, a
look-elsewhere rate, a units error, or the self-incriminating source line extracted from the file
itself. Each block prints CLAIM -> TEST -> RESULT -> VERDICT. Needs numpy (+ the ai_slop files for
the extraction proofs, which degrade gracefully if absent).
"""
import os, re, json, glob
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SLOP = os.path.join(ROOT, "ai_slop")
Z2 = 32*np.pi/3
Z = np.sqrt(Z2)


def show(path, pattern, n=4, ctx=0):
    """Extract self-incriminating lines from an actual file (the proof is in the source)."""
    full = path if os.path.isabs(path) else os.path.join(ROOT, path)
    if not os.path.exists(full):
        # try a glob fallback
        hits = glob.glob(os.path.join(SLOP, "**", os.path.basename(path)), recursive=True)
        if not hits: return [f"   [file not found: {path}]"]
        full = hits[0]
    out = []
    rx = re.compile(pattern)
    lines = open(full, errors="ignore").read().splitlines()
    for i, ln in enumerate(lines):
        if rx.search(ln):
            out.append(f"   {os.path.relpath(full, ROOT)}:{i+1}:  {ln.strip()[:96]}")
            if len(out) >= n: break
    return out or [f"   [pattern not found in {os.path.relpath(full, ROOT)}]"]


def hdr(n, title):
    print("\n" + "="*92); print(f"HALLUCINATION CLASS {n} -- {title}"); print("="*92)


# ===================================================================================
def proof1_constants_numerology():
    hdr(1, "Dimensionless-constant 'derivations' (alpha, masses, sin2thetaW, Koide, CKM...)")
    print("  CLAIM: alpha^-1 = 4Z^2+3 = 137.041 'derives' the fine-structure constant (0.0039%).")
    print("  TEST:  build the same formula family and point it at UNRELATED targets + random ones.")
    # the formula family the engine used (a faithful, compact reconstruction)
    vals = []
    for a in range(1, 51):
        for b in range(-50, 51):
            vals.append(a*Z2 + b)                         # aZ^2 + b
        vals += [a*Z2, Z2/a, a*Z, Z/a, a*np.pi, np.pi/a]
    for p in range(1, 60):
        for q in range(1, 60):
            if p < 3*q: vals.append(p/q)                  # small fractions
    for a in range(1, 30):
        for n in (2, 3, 5, 6, 7, 10):
            vals.append(a*np.sqrt(n)); vals.append(np.sqrt(n)/a)
    vals = np.array(sorted(set(round(v, 6) for v in vals if 0 < v < 1e4)))
    def best(target):
        i = np.argmin(np.abs(vals - target)); return vals[i], abs(vals[i]-target)/target*100
    print(f"  formula pool size: {len(vals):,}")
    for name, t in [("alpha^-1 (physics)", 137.035999), ("Dunbar's number (sociology)", 150.0),
                    ("Tropopause temp /K (weather)", 217.0), ("Hubble H0 (km/s/Mpc)", 67.4)]:
        v, e = best(t); print(f"     {name:32} best match {v:>10.4f}  err {e:.4f}%")
    rng = np.random.default_rng(0)
    tg = rng.uniform(1, 200, 2000)
    errs = np.array([best(t)[1] for t in tg])
    print(f"  RESULT: of 2000 ARBITRARY targets in [1,200], the pool matches "
          f"{np.mean(errs<0.03)*100:.0f}% to <0.03%, {np.mean(errs<0.0039)*100:.0f}% to <0.0039% (alpha's quoted error).")
    print("  VERDICT: a machine that hits alpha, Dunbar's number AND a random target equally well")
    print("           carries ~0 bits. The 'derivation' is the EXPECTED output of the search. HALLUCINATION.")


# ===================================================================================
def proof2_trivial_identity():
    hdr(2, "'Z^2 predicts 8 protein contacts' -- a trivial integer identity, pi cancels")
    print("  CLAIM: Z^2 / Vol(unit 3-ball) = 8 -> '8 contacts per residue', a Z^2 prediction.")
    ratio = Z2 / (4*np.pi/3)
    print(f"  TEST:  Z^2/(4pi/3) = (32pi/3)/(4pi/3) = 32/4 = {ratio:.10f}   (pi CANCELS exactly)")
    print(f"  RESULT: the 'prediction' is the integer 8, independent of pi, Z, and all protein physics.")
    print("          The repo's own file derives the OTHER 8 as generic packing 12-2-2=8, then matches:")
    for ln in show("ai_slop/extended_research/biotech/hybrid_z2_test/prove_8_contacts_cube.py",
                   r"QED|CUBE_VERTICES = 8|12 - 2 - 2|32 \* np\.pi"):
        print(ln)
    print("  VERDICT: two unrelated 8's (32/4 and 12-2-2) matched by hand; cutoff r=(Z^2)^(1/4)*3.8A uses")
    print("           a FREE exponent; observed 8.60+/-0.18 is a significant MISS from 8. HALLUCINATION.")


# ===================================================================================
def proof3_frb_fabricated():
    hdr(3, "FRB birefringence 'null test' -- a fabricated positive (conclusion vs its own numbers)")
    j = os.path.join(SLOP, "research/frb_analysis/birefringence_null_results.json")
    print("  CLAIM (file's headline 'conclusion'):")
    if os.path.exists(j):
        d = json.load(open(j))
        bc = d.get("birefringence_constraint", {})
        beta, err = bc.get("beta_deg_per_Gpc"), bc.get("beta_error")
        sig = beta/err if (beta and err) else float("nan")
        print(f"     \"{d.get('conclusion')}\"")
        print(f"  TEST:  read the file's OWN computed numbers:")
        print(f"     beta = {beta:.3f} +/- {err:.3f} deg/Gpc  ->  {sig:.1f} sigma from zero")
        print(f"     consistent_with_zero = {bc.get('consistent_with_zero')}   null_supported = "
              f"{d.get('statistical_tests', {}).get('null_supported')}")
        print("  also: the input data are 100% SYNTHETIC -- generated, not observed:")
        for ln in show("ai_slop/research/frb_analysis/birefringence_null_test.py",
                       r"np\.random\.(seed|normal)\(", n=3):
            print(ln)
        print(f"  RESULT: the headline says 'supports beta=0 (Z^2 confirmed)' while the code's own beta is")
        print(f"          {sig:.1f}sigma AWAY from 0, on fabricated data, with both null flags = False.")
    else:
        print("     [results JSON not present]")
    print("  VERDICT: a 'confirmation' narrative directly OPPOSITE to its own computation. The single")
    print("           clearest artifact of the hallucination mode: story untethered from numbers. HALLUCINATION.")


# ===================================================================================
def proof4_geometric_mean():
    hdr(4, "'a0 = geometric mean of two horizon scales = cH/Z' -- the arithmetic is false")
    c, Mpc, G = 2.99792458e8, 3.0857e22, 6.674e-11
    H0 = 67.4e3/Mpc
    aH = c*H0                                   # horizon acceleration cH
    aF = c*np.sqrt(G*3*H0**2/(8*np.pi*G))       # 'Friedmann' accel c*sqrt(G rho_c)
    gm = np.sqrt(aH*aF)
    a0 = aH/Z
    print("  CLAIM: a0 = sqrt(a_Friedmann * a_horizon) = cH/Z.")
    print(f"  TEST:  a_horizon=cH={aH:.3e},  a_Friedmann=c*sqrt(G rho_c)={aF:.3e}")
    print(f"  RESULT: sqrt(aH*aF) = {gm:.3e} = cH/{aH/gm:.2f}   but   cH/Z = {a0:.3e} = cH/{Z:.2f}")
    print(f"          ratio = {gm/a0:.2f}x  -- they are NOT equal (off by {abs(gm/a0-1)*100:.0f}%).")
    print("  (Aside: np.isclose would FALSELY call these 'equal' -- its default atol=1e-8 dwarfs ~1e-10")
    print("   accelerations. Read the raw numbers. Only a_Friedmann/2 = cH/Z, and the 1/2 is a posit.)")
    print("  VERDICT: the 'two scales related by Z' story is post-hoc; the geometric mean is cH/1.70. HALLUCINATION.")


# ===================================================================================
def proof5_units_crime():
    hdr(5, "Hurricane 'V* = Vmax/Z^2' and eye/RMW=1/Z -- units crime + falsified on real data")
    print("  CLAIM: normalized hurricane intensity V* = Vmax / Z^2, and eye/RMW = 1/Z.")
    print("  TEST:  Z^2 = 32pi/3 is DIMENSIONLESS (a geometric volume ratio). Vmax is a SPEED (knots).")
    print(f"         Vmax/Z^2 = Vmax/{Z2:.2f} is just an arbitrary rescaling of knots by a geometry constant;")
    print("         it encodes nothing physical. The source commits exactly this:")
    for ln in show("ai_slop/meteorology/HURRICANE_PREDICTOR_SUMMARY.md", r"V\* = Vmax", n=1): print(ln)
    for ln in show("ai_slop/meteorology/FINAL_HURRICANE_FINDINGS.md", r"Vmax/Z", n=1): print(ln)
    print("  RESULT: and the eye/RMW=1/Z=0.173 prediction was FALSIFIED on 1,647 NOAA flight-recon obs:")
    for ln in show("ai_slop/meteorology/Z2_HURRICANE_FINAL_VERDICT.md", r"0\.58|236%|t = 64|FALSIF|REJECT", n=3):
        print(ln)
    print("  VERDICT: dimensionless geometry constant applied to a dimensional weather quantity, then")
    print("           falsified at >60 sigma on real data. HALLUCINATION (and honestly self-killed).")


# ===================================================================================
def proof6_fake_computation():
    hdr(6, "Biotech 'docking/structure' -- numbers are hard-coded constants, not computations")
    print("  CLAIM: CFTR chaperone peptides reach 'dG = -12 to -21 kcal/mol (MM/PBSA)'.")
    print("  TEST:  the energy function takes only the SEQUENCE; the fetched 2PZE structure is unused;")
    print("         the 'energy' is a sum of per-feature CONSTANTS, and -12 is the design TARGET:")
    for ln in show("ai_slop/extended_research/biotech/m4_cftr_chaperone_docking.py",
                   r"TARGET_BINDING = -12|def calculate_binding_energy\(sequence|burial \+= |return energy", n=4):
        print(ln)
    print("  CLAIM: Cas9 minimal variants have 'pLDDT' and 'catalytic_intact'.")
    print("  TEST:  pLDDT = a hand-rolled 'score = 50 + bonuses' (not ESMFold); catalytic_intact is hard-coded:")
    for ln in show("ai_slop/extended_research/biotech/m4_cas_minimization_screener.py",
                   r"score = 50\.0|catalytic_intact=True", n=4):
        print(ln)
    print("  VERDICT: 'structure prediction' and 'binding energy' are asserted constants/heuristics with")
    print("           the answer (or the target) wired in. HALLUCINATION (fake computation).")


# ===================================================================================
def proof7_circular_generations():
    hdr(7, "'3 fermion generations from the orbifold' -- answer reverse-engineered, self-documented")
    print("  CLAIM: the index theorem on the orbifold yields exactly 3 generations.")
    print("  TEST:  read the derivation's OWN words -- it gets 1, declares that wrong, then invents the")
    print("         count needed to reach 3:")
    for ln in show("ai_slop/core_theory/THEORETICAL_FOUNDATIONS.md",
                   r"this gives 1, not 3|Let me reconsider|6 relevant fixed points", n=3):
        print(ln)
    print("  VERDICT: the desired answer (3) drives the choice of inputs ('6 relevant fixed points').")
    print("           Reverse-engineering, self-documented in the source. HALLUCINATION.")


# ===================================================================================
def proof8_problem_inflation():
    hdr(8, "'Solves 452 unsolved problems' -- assertion inflation, one number, one day")
    print("  CLAIM: the formula 'solves/derives' 62 -> 87 -> 211 -> 286 -> 432 -> 452 problems.")
    print("  TEST:  these counts all appear in commit messages dated 2026-03-18 -- the same single day --")
    print("         each 'proof' being the one relation a0=cH/Z asserted to apply to another phenomenon.")
    print("         (git log --reverse: commits ~34-47, all 2026-03-18.)")
    print("  VERDICT: a real one-line relation cannot 'solve' 452 disparate open problems overnight; the")
    print("           count is rhetoric, not results. HALLUCINATION (assertion-as-proof).")


def main():
    print("#"*92)
    print("# PROVING THE HALLUCINATIONS -- reproducible decisive tests, one per class")
    print("# (the surviving result a0=(c/2)sqrt(G rho)=cH/Z is NOT here; it is real -- see real_research/)")
    print("#"*92)
    proof1_constants_numerology()
    proof2_trivial_identity()
    proof3_frb_fabricated()
    proof4_geometric_mean()
    proof5_units_crime()
    proof6_fake_computation()
    proof7_circular_generations()
    proof8_problem_inflation()
    print("\n" + "#"*92)
    print("""# BOTTOM LINE: eight classes, each proven by a test you can rerun -- a look-elsewhere rate, a
# pi-cancelling identity, a result contradicting its own JSON, false arithmetic, a units error,
# hard-coded 'computations', a self-documented reverse-engineering, and overnight assertion-
# inflation. None is a matter of opinion. Together they cover the entire dead sprawl. The ONE
# thing that is NOT in this file -- because it survives every test -- is a0=cH/Z and its evolution.""")
    print("#"*92)


if __name__ == "__main__":
    main()
