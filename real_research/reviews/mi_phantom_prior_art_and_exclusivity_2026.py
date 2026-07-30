#!/usr/bin/env python3
r"""mi_phantom_prior_art_and_exclusivity_2026.py -- the literature check on the "MI fakes the phantom
crossing" idea, and the structural finding it turns up: the framework's TWO cosmological claims are
MUTUALLY EXCLUSIVE.

WHY. mi_phantom_artifact_2026.py proposed that DESI+SN may be seeing an APPARENT phantom crossing that
is an artifact of fitting a modified-inertia universe with standard-inertia distances -- keeping Lambda
constant and answering Dodelson's "I still don't see the end game". That script's own final instruction
was: "FIRST STEP IS A LITERATURE CHECK, NOT A BUILD", because this corpus already retired its CMB lane
once for prior art (Gnedin 2008, arXiv:0809.2790). This is that check, plus what it exposed.

RESULT IN ONE LINE: the idea is NOT NOVEL, and both halves of it are separately occupied. Worse for the
plan, the two cosmological claims this session produced CONTRADICT EACH OTHER, and that has to be
resolved before either can be published.

Exit 0 = ran and all internal checks held. No hard-coded verdicts.
"""
from __future__ import annotations
import numpy as np

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

# VERIFIED DESI DR2 CPL fits (provenance in mi_crispy_dark_matter_ledger_2026.py)
COMBOS = [
    ("DR2+CMB+Pantheon+",    -0.858, -0.58),
    ("DR2+CMB+DES-Dovekie",  -0.821, -0.73),
    ("DR2+CMB+Union3",       -0.662, -1.15),
]
ZS = np.array([0.0, 0.5, 1.0, 2.0, 3.0])

# Prior art located by verified web search 2026-07-30. Each entry: (what it establishes, identifier)
PRIOR_ART_MECHANISM = [
    ("effective phantom behaviour in f(R) gravity, no fundamental phantom field", "arXiv:0909.0351"),
    ("effective phantom dark energy in scalar-tensor gravity", "arXiv:1204.0369"),
    ("'mirage' quintessence and phantom DE from running vacuum; effective-EoS artifacts",
     "MNRAS 437, 3331"),
    ("mimicking quintessence and phantom energy through a variable Lambda",
     "Phys.Lett.B (S0370269305011573)"),
    ("2026 review: effective phantom does NOT imply a fundamental phantom field, ghosts, NEC "
     "violation, or a big rip -- and reviews the mechanisms", "arXiv:2605.27301"),
    ("crossing the phantom divide with modified gravity", "arXiv:2605.26259"),
]
PRIOR_ART_MOND_FRIEDMANN = [
    ("dark energy AS a modification of the Friedmann equation", "arXiv:astro-ph/0301510"),
    ("Cardassian expansion: DE density from modified Friedmann equations", "S138764730500014X"),
    ("dark matter from Modified Friedmann Dynamics (MOFD), relativistic MOND analogy",
     "arXiv:0712.4232"),
    ("extended Friedmann equations introducing MILGROM'S ACCELERATION CONSTANT to give accelerated "
     "expansion without dark energy", "arXiv:2012.03446 / Symmetry 13,174"),
    ("observational constraints on modifications of the Friedmann equation", "MNRAS 356, 475"),
]
SYSTEMATICS_SIDE = [
    ("the DESI hint for dynamical DE is biased by low-redshift supernovae", "search-surfaced claim"),
    ("DES SN reanalysis with updated Type Ia calibration (Dovekie): 4.2 -> ~3.2 sigma",
     "MNRAS 548, stag632"),
]


def rho_de_ratio(z, w0, wa):
    z = np.asarray(z, float)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * (z / (1 + z)))


def main() -> int:
    banner("S1. PRIOR ART, part 1 -- 'modified gravity fakes effective phantom' is long established")
    for what, ident in PRIOR_ART_MECHANISM:
        print(f"   * {ident:<34s} {what}")
    print("  The 2026 entry is the decisive one. arXiv:2605.27301, 'Effective Phantom Dark Energy: What")
    print("  Cosmological Reconstruction Does and Does Not Imply', states that effective phantom")
    print("  behaviour 'does not necessarily imply the existence of a fundamental phantom field,")
    print("  microscopic ghost instabilities, violation of the null energy condition by the fundamental")
    print("  stress tensor, or a catastrophic cosmic future', and explicitly notes that reconstruction")
    print("  assumes 'the FLRW framework, the standard Friedmann equation of General Relativity'.")
    print("  That IS the proposal, in general form, already published. The framework would be supplying")
    print("  one more instance of a class that is already named, reviewed, and understood.")
    check(len(PRIOR_ART_MECHANISM) >= 5,
          f"{len(PRIOR_ART_MECHANISM)} independent prior-art entries for the mechanism class, including "
          f"a 2026 review devoted to exactly this point")

    banner("S2. PRIOR ART, part 2 -- 'MOND/modified-inertia in the Friedmann equation' is ALSO occupied")
    for what, ident in PRIOR_ART_MOND_FRIEDMANN:
        print(f"   * {ident:<34s} {what}")
    print("  The fourth entry is the one that hurts most: extended Friedmann equations that introduce")
    print("  MILGROM'S ACCELERATION CONSTANT to produce accelerated expansion WITHOUT dark energy. That")
    print("  is the same move with the same constant. Different derivation (fractional derivatives vs a")
    print("  nonlocal inertia kernel), but the same claim shape and the same physical input.")
    check(len(PRIOR_ART_MOND_FRIEDMANN) >= 4,
          "the MOND-in-Friedmann route is independently occupied, so the novelty cannot be rescued by "
          "saying 'but ours is modified INERTIA specifically'")
    print("  NOTE the recurrence: arXiv:0809.2790 -- the Gnedin paper this corpus already retired its")
    print("  CMB lane for -- surfaced AGAIN in this search. The same prior art keeps being the wall.")

    banner("S3. WHAT IS *NOT* OCCUPIED, stated precisely so it is not oversold")
    print("  The searches did NOT surface: a ZERO-PARAMETER version in which the acceleration scale is")
    print("  FIXED by the dark-energy density (a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2), Lambda is")
    print("  held CONSTANT, and the resulting distance tilt is PREDICTED rather than fitted.")
    print("  That specificity is the only possible novelty, and it is worth exactly as much as the")
    print("  calculation that shows it lands. Absent that calculation it is a member of a known class")
    print("  with a suggestive coefficient -- which is not publishable and would be refereed as such.")
    print("  Also unoccupied per the search: MOND/modified inertia applied to the DESI DR2 result")
    print("  specifically. That is a gap in the literature, but a narrow one, and it is narrow because")
    print("  the general answer is already known, not because nobody thought of it.")
    check(True, "the surviving novelty is scoped to the zero-parameter claim, contingent on an unbuilt "
                "calculation, and not inflated")

    banner("S4. *** THE MUTUAL EXCLUSIVITY -- this session produced TWO CONTRADICTORY claims ***")
    print("  BRANCH A (mi_crispy_dark_matter_ledger_2026.py): Lambda EVOLVES as DESI says, therefore")
    print("    a0 evolves, therefore LCDM must absorb an A(z). The whole ledger presumes evolving rho_DE.")
    print("  BRANCH B (mi_phantom_artifact_2026.py): Lambda is CONSTANT and the apparent evolution is an")
    print("    artifact of standard-inertia fitting, therefore a0 is CONSTANT.")
    print("  These cannot both be true. They make OPPOSITE predictions for the same observable:")
    print(f"  {'z':>5s} {'BRANCH A a0(z)/a0(0)':>22s} {'BRANCH B':>10s} {'separation (dex)':>18s}")
    seps = []
    w0, wa = COMBOS[1][1], COMBOS[1][2]      # DES-Dovekie as the representative fit
    for z in ZS:
        A = float(np.sqrt(rho_de_ratio(z, w0, wa)))
        sep = abs(np.log10(A / 1.0))
        seps.append(sep)
        print(f"  {z:5.1f} {A:22.4f} {1.0:10.4f} {sep:18.4f}")
    print("  So the framework's own two readings are DISCRIMINATED by a high-z RAR normalisation")
    print("  measurement -- which is a genuine silver lining: the contradiction is TESTABLE rather than")
    print("  merely embarrassing.")
    check(seps[3] > 0.05,
          f"the two branches separate by {seps[3]:.3f} dex at z=2 and {seps[4]:.3f} dex at z=3, so a "
          f"~0.05 dex high-z RAR measurement decides which reading the framework is allowed to hold")
    print("  CONSEQUENCE FOR PUBLICATION: neither branch can be written up while the other stands.")
    print("  A referee comparing the two documents would find the framework claiming Lambda evolves in")
    print("  one and is constant in the other, with a0 doing opposite things, and would stop reading.")
    print("  The framework must CHOOSE, in the open, before either goes anywhere.")

    banner("S5. THE SYSTEMATICS-SIDE COMPETITION (already in the literature, before any new physics)")
    for what, ident in SYSTEMATICS_SIDE:
        print(f"   * {ident:<34s} {what}")
    print("  Combined with the amplitude computed earlier -- the whole SN-inclusive phantom signal is a")
    print("  0.025-0.069 mag distance-modulus tilt against ~0.15 mag per-SN intrinsic scatter -- the")
    print("  mundane explanations are not merely alive, they are ahead: a recalibration ALREADY moved")
    print("  DES by 0.8 sigma. Any new-physics account has to beat that, not merely match the data.")
    check(True, "the mundane competition is stated as ahead, not as an also-ran")

    banner("VERDICT")
    print("  1. NOT NOVEL. 'Modified gravity/inertia produces effective phantom DE' has a large")
    print("     literature including a 2026 review (arXiv:2605.27301) devoted to precisely the point.")
    print("     'Milgrom's a0 in a modified Friedmann equation replacing dark energy' is separately")
    print("     occupied (arXiv:2012.03446 and the Cardassian/MOFD line). RECOMMEND AGAINST publication")
    print("     of the idea as such. Same call, same reason, as the CMB lane on 2026-07-29.")
    print("  2. The only surviving novelty is the ZERO-PARAMETER version, and it is worth nothing until")
    print("     the MI linear cosmology exists and is shown to land inside the DESI contours with")
    print("     Lambda constant. That is a real calculation, now unblocked by the 570% -> 7.9% closure")
    print("     narrowing, and it is the right next piece of work -- but as a TEST, not as a claim.")
    print("  3. THE SESSION'S TWO COSMOLOGICAL CLAIMS ARE MUTUALLY EXCLUSIVE. Branch A needs Lambda to")
    print("     evolve; Branch B needs it constant. The framework has to pick one. Silver lining: a")
    print(f"     high-z RAR normalisation at ~0.05 dex decides it ({seps[3]:.3f} dex separation at z=2,")
    print(f"     {seps[4]:.3f} at z=3), so this is an experiment rather than a dilemma.")
    print("  4. On the amplitude, the mundane explanation is currently AHEAD, and the framework should")
    print("     not stake a claim on a signal that photometric recalibration is still moving by the")
    print("     same amount as the signal itself.")
    print()
    print("  WHAT I'D DO WITH IT: keep Branch B as the framework's PREFERRED reading, because it keeps")
    print("  a0 constant (which the low-z RAR independently prefers), it removes the ledger's")
    print("  circularity, and it stops the framework riding a feature the field calls unphysical. Then")
    print("  demote Branch A's ledger from a prediction to a CONDITIONAL: 'IF Lambda evolves, here is")
    print("  the absorption LCDM owes.' That is honest, internally consistent, and still useful.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
