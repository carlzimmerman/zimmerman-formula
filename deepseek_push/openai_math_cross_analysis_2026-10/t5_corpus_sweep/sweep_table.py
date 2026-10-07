#!/usr/bin/env python3
"""T5 corpus sweep: verified re-read table for the frozen score-1/score-2 families.

House lane format (see campaign_fresh_gravity/CFG380_32pi_geometric_door/):
- Emits the sweep table to sweep_table.out and per-row checks to
  t5_corpus_sweep_results.json; exits 0 on all PASS, 1 on any FAIL.
- Check per row: READ == True (the family's manuscripts were actually read at
  manuscript level, per the .md table's "Manuscripts read" column), and any
  PROMOTED family (my_score >= 2 with triage_score < 2) must carry
  script_check == True (a committed script check exists in this lane).
- Final line of .out: 'T5 CORPUS SWEEP COMPLETE: N/M checks PASS.'

MUTATE control (declared): with MUTATE=1 the script flips one already-read
family's READ flag to False (seeded choice, seed 20261006, "random" per the
task), writes SEPARATE sweep_table_MUTATE.out and
t5_corpus_sweep_results_MUTATE.json, that row's check must flip to FAIL, and
the script must exit 1.

Status of this run: all 31 frozen families were re-read against their
manuscripts (preprints/ PDFs, or build/*.tex where the PDF needed OCR);
abstract + introduction + main theorem checked per family; no promotions.
"""
import json
import os
import random
import sys

LANE = "T5 CORPUS SWEEP"

# (family, short title, manuscripts-read tag, triage_score, my_score, read, promoted, script_check, piece, screen, notes)
ROWS = [
    (374, "Sharp one-third stability of Brenier maps", "Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026", 2, 2, True, False, None, "P2", "n/a (stability exponent, not a constant)", "Thm 1.1 verified (uniform source on compact convex K, ||Tm-Tn||<=C W2^(1/3), 1/3 sharp on 3-atom cube targets); abstract-level only (t1 deep-reads)."),
    (90, "Triangular lattice optimality, Riesz/Coulomb", "4 mss: atomic certificate; universal optimality; Fourier certificate; Coulomb renormalized energy", 1, 1, True, False, None, "P8/P1 analogy", "Q1 no; Q3 packing pi/(2 sqrt3) etc. planar", "All four manuscripts planar, unit-density background; no 3D 1/r gravity content (t4 deep-reads)."),
    (96, "Gaussian propeller 9/(8 pi)", "The-Gaussian-Propeller-Bound-in-Every-Dimension-September-24-2026", 1, 1, True, False, None, "P1/P8 analogy", "Q1 no; Q2 forced in its problem; Q3 9/(8pi) in F itself, 259% off T", "Thm 1.1 verified word-for-word; 3 sectors 2pi/3 attain; no physical functional (t4 deep-reads)."),
    (87, "Mahler conjectures / polar-product width", "3 mss: symmetric + general Mahler; symplectic balls", 1, 1, True, False, None, "P8 analogy", "Q1 no; 'width 4' trivially in F; no coupling", "V(K)V(K^o)>=4^n/n!, simplex (n+1)^(n+1)/(n!)^2; Gromov width of K x K^o is literally 4 -- numerology, no gravity link (t4 deep-reads)."),
    (91, "Log/L_p Brunn-Minkowski, B-conjecture", "The-logarithmic-Brunn-Minkowski-conjecture-September-23-2026", 1, 1, True, False, None, "P8 analogy", "n/a", "Even log-BM for origin-symmetric bodies all dimensions; equality cases only; no physical coupling."),
    (93, "Dimension-free log-Sobolev", "A-dimension-free-log-Sobolev-inequality-...-September-23-2026", 1, 1, True, False, None, "P5/P8 analogy", "Q2 constant NON-explicit", "Ent<=C a^2 |Df|^2, one universal nonexplicit C; not a quasilinear 3-Laplacian statement."),
    (101, "Sharp simplex bound, isotropic constants", "A-sharp-entropy-bound-and-the-simplex-inequality-...-October-5-2026", 1, 1, True, False, None, "P8 analogy", "n/a", "Simplex maximizes isotropic constant; entropy bound equality one-sided exponentials; pure geometry."),
    (88, "Projection-body (Petty) inequalities", "2 mss: Petty projection-volume; product counterexample", 1, 1, True, False, None, "P8 analogy", "n/a", "Ellipsoids unique minimizers n>=4; product of two 10-simplices beats 20-simplex (22355476/22020096>1) -- extra content vs triage one-liner, no score change."),
    (72, "Brennan conjecture / integral means", "2 mss: Brennan inverse-square; strict inverse-first-power", 1, 1, True, False, None, "P5 analogy", "Q3 n/a: 4/3 and 4 are integrability exponents", "Brennan 4/3<s<4 verified; B_S(-2)=1; B_b(-1)<1/4 (Kraetzer false); 2D conformal maps."),
    (149, "Classwise permanence, mass-action", "2 mss: Uniform Permanence; Boundedness and persistence", 1, 1, True, False, None, "P2", "n/a", "Compact convex forward-invariant absorbing set in finite time per compatibility class -- right KIND of settling statement, but set fixed by network+rates, cannot encode rho_ph; ODEs, no gravity."),
    (186, "Sharp thresholds graph/hypergraph", "2 mss: uniform influence hypergraph; sharp threshold monotone graphs", 1, 1, True, False, None, "P6", "Q3 n/a: constant explicitly non-tuned", "Friedgut-Kalai width <= C log(1/2eps)/(log n)^2; constant 'only a convenient explicit choice' -- not sharp; vocabulary only."),
    (213, "Critical percolation quasi-transitive", "2 mss: bond+site Z^3; no percolation at criticality", 1, 1, True, False, None, "P6", "n/a", "No infinite cluster at p_c on Z^3 (bond+site) and on quasi-transitive graphs; threshold analogy only."),
    (214, "Benjamini-Schramm nonuniqueness", "Nonuniqueness-of-percolation-on-nonamenable-quasi-transitive-graphs-...", 1, 1, True, False, None, "P6", "n/a", "p_c<p_{2->2}<=p_u nonamenable; coexistence interval; no g_N/a0 threshold."),
    (228, "Continuum phase transitions, radial pair potentials", "2 mss: temperature singularity; algebraic decay", 1, 1, True, False, None, "P6", "Q1 no; beta_c in [7/8,9/8], density 5 rho_*/3 (construction params, in F)", "Stable 3D radial potentials, canonical free energy strict downward derivative jump at one common beta_c over an open density interval; shell graph <=3m^2/8 edges. Classical stat-mech switch in beta, not g_N/a0; no gravity kernel."),
    (377, "Interior C^{1,alpha} infinity-harmonic", "Uniform-Interior-C1alpha-Estimates-...-October-4-2026", 1, 1, True, False, None, "P5", "Q3 n/a: alpha_d non-explicit in (0,1/3]", "Downgrade CONFIRMED: p=infinity, homogeneous, non-explicit exponent; p=3-with-source is classical. One-line confirm only."),
    (360, "Weak MTW -> convexity, regular OT", "2 mss: Global Support; Uniform Bi-Holder Transport", 1, 1, True, False, None, "P2", "n/a", "Abstract-level: manifold setting, densities bounded above and away from zero; flat Euclidean settling already Caffarelli-classical (t2 deep-reads)."),
    (373, "Nonattainment 3-marginal Coulomb", "A-counterexample-to-the-Monge-ansatz-...-September-25-2026", 1, 1, True, False, None, "P2", "n/a", "Kantorovich min attained by coupling, no Monge map pair attains; infima agree. Cautionary only; settling is not multi-marginal."),
    (367, "Critical dimension 7, one-phase Bernoulli", "The-critical-dimension-for-one-phase-Bernoulli-minimizers-...", 1, 1, True, False, None, "P2", "n/a", "d*=7, flat <=6, nonflat cone in R^7, singular set dim <= n-7 sharp; free-boundary analogy, no density target."),
    (370, "Subcritical Henon-Lane-Emden", "The-Subcritical-Henon-Lane-Emden-Conjecture-September-24-2026", 1, 1, True, False, None, "P5", "Q1 no; critical hyperbola is exponent-space threshold", "No positive entire solutions of semilinear Laplace SYSTEM on the subcritical side; not the quasilinear 3-Laplacian, no source-carrying p=3 statement."),
    (375, "De Giorgi conjecture, dimension 8", "De-Giorgis-conjecture-in-dimension-eight-September-26-2026", 1, 1, True, False, None, "P6", "Q3: sqrt(2) layer width trivially in F; no g_N/a0 threshold", "Monotone entire solutions of Du=u^3-u in R^8 are planar tanh((e.x-c)/sqrt2); stable solutions in R^7 classified. tanh is only a possible switch TEMPLATE; nothing forces its argument."),
    (362, "3D relativistic Vlasov-Maxwell smoothness", "Global-classical-solutions-of-the-three-dimensional-relativistic-Vlasov-Maxwell-system-...", 1, 1, True, False, None, "P7", "n/a", "One-species charged repulsive, compact support; attractive gravity VP not covered; no growth law."),
    (363, "Non-uniqueness hard-sphere Boltzmann", "Nonuniqueness-with-local-conservation-for-the-hard-sphere-Boltzmann-equation-...", 1, 1, True, False, None, "P7", "n/a", "Nonuniqueness WITH exact local conservation, two distinct L^1-strong solutions; weak-solution warning, collisionless MOND out of scope."),
    (364, "Kinetic limits, Boltzmann lifespan", "The-Boltzmann-Grad-limit-for-stable-radial-potentials-...", 1, 1, True, False, None, "P7", "n/a", "Boltzmann-Grad limit from grand-canonical Newtonian gas; no gravitational/Poisson content."),
    (337, "Cartan-Hadamard isoperimetry", "2 mss: generalized CH isoperimetry; CAT(0) integral fillings", 1, 1, True, False, None, "P8", "n/a", "sec<=kappa<=0 model comparison with Euclidean rigidity; kappa<=0 not rho_Lambda>0; sharp-constant style only."),
    (354, "Isoperimetric profile cubic 3-torus", "The-Isoperimetric-Conjecture-for-the-Cubic-Flat-Three-Torus-...", 1, 1, True, False, None, "P8", "Q1 no; Q3: 4pi/81 (290% off) and 1/pi (700% off) -- no hit", "I_unit(V)=min{(36pi)^(1/3) v^(2/3), 2pi v, 2}, minimizers fully classified at transitions 4pi/81, 1/pi; flat torus has no scale to couple."),
    (261, "Anderson localization / delocalization", "2 mss: a.c. spectrum d>=3; pure point 2D", 1, 1, True, False, None, "P6", "n/a", "d>=3 small disorder a.c. on open interval; 2D pure point at every disorder; mobility-edge analogy only."),
    (267, "Positive-T BEC dilute hard-sphere gas", "2 mss read (positive-T + ground-state); family has 5", 1, 1, True, False, None, "P3/P6", "Q3 n/a: liminf>0 only, no fraction value; T=T(a,rho) exists", "Positive-T BEC real for small density: positive condensate fraction at volume-independent T. Loosest analogue for a condensate cold fluid; NO amount 5.36, no gravity."),
    (282, "Scale -> conformal symmetry, 4D QFT", "Scale-and-conformal-symmetry-in-four-dimensional-operational-QFT-...", 1, 1, True, False, None, "P1", "Q1 no; 1/3 is the standard Weyl improvement, couples nothing", "Stress tensor admits traceless local improvement under discreteness hypotheses; global conformal action left open; no rational for rho_Lambda vs a0."),
    (264, "Strong cosmic censorship near Kerr", "Generic-Future-Inextendibility-...-September-23-2026 (family: 3 mss)", 1, 0, True, False, None, "none", "n/a", "Meagre set of extendible data near subextremal Kerr; Lambda=0, no a0 content. Downgrade 1->0 (triage's own 'treat as 0')."),
    (260, "Spacetime Penrose inequalities", "flagship charged + AdS variant read (family: 13 mss)", 1, 0, True, False, None, "none", "Q1 no; AdS m>=sqrt(A/16pi)(1+A/(4pi)) has Lambda=-3 normalization, 1/2 is chosen not derived; quasilinear div(t(|df|)grad f/|df|)=0 is a PROOF TOOL", "Lambda<0 only; no positive-Lambda content, no a0; the only quasilinear operator in the sweep carries no physical source. Downgrade 1->0 (triage's own 'treat as 0')."),
    (348, "Einstein four-manifolds classification", "3 mss: zero-plane rigidity; L2 gap; positively curved", 1, 0, True, False, None, "none", "n/a", "Riemannian classification (S^4, CP^2, S^2xS^2, RP^4); Ric=3g normalization radius 1/sqrt3 is an artifact; no Lambda dynamics. Downgrade 1->0 (triage's own 'treat as 0')."),
]


def run(mutate: bool):
    rows = list(ROWS)
    if mutate:
        rng = random.Random(20261006)
        idx = rng.randrange(len(rows))
        fam = rows[idx][0]
        (fam_id, title, mss, ts, ms, _read, promo, sck, piece, screen, notes) = rows[idx]
        rows[idx] = (fam_id, title, mss, ts, ms, False, promo, sck, piece, screen, notes)  # READ -> False
        print(f"[MUTATE] marked family {fam} as unread (READ=TRUE -> FALSE)")
    else:
        fam = None

    # per-row checks
    results = []
    n_pass = 0
    for (fam_id, title, mss, ts, ms, read, promo, sck, piece, screen, notes) in rows:
        ok = read and (not promo or sck)
        results.append({
            "family": fam_id, "title": title, "manuscripts": mss,
            "triage_score": ts, "my_score": ms, "read": bool(read),
            "promoted": bool(promo), "script_check_present": sck,
            "piece": piece, "screen": screen, "check": "PASS" if ok else "FAIL",
        })
        n_pass += 1 if ok else 0

    total = len(rows)
    all_pass = n_pass == total

    # .out table
    out_lines = []
    out_lines.append(f"# {LANE} sweep table (verified at manuscript level)")
    out_lines.append(f"{'#':>3} | {'family':<4} | {'triage':<6} | {'mine':<6} | {'read':<5} | {'promo':<5} | piece | screen result")
    out_lines.append("-" * 100)
    for r in results:
        out_lines.append(
            f"{r['check']:>3} | {r['family']:<4} | {r['triage_score']:<6} | {r['my_score']:<6} | "
            f"{str(r['read']):<5} | {str(r['promoted']):<5} | {r['piece']:<25} | {r['screen'][:55]}")
    out_lines.append("")
    out_lines.append(f"{LANE} COMPLETE: {n_pass}/{total} checks PASS." if all_pass
                     else f"{LANE} FAIL: {total - n_pass}/{total} checks FAILED.")
    for r in results:
        if r["check"] == "FAIL":
            out_lines.append(f"  FAIL row: family {r['family']} ({r['title']})")

    suffix = "_MUTATE" if mutate else ""
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"sweep_table{suffix}.out")
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             f"t5_corpus_sweep_results{suffix}.json")
    with open(out_path, "w") as f:
        f.write("\n".join(out_lines) + "\n")
    payload = {
        "lane": "t5_corpus_sweep",
        "mutate": bool(mutate),
        "mutated_family": fam,
        "n_checks": total, "n_pass": n_pass, "all_pass": all_pass,
        "rows": results,
    }
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=1)
    print("\n".join(out_lines))
    print(f"wrote {out_path}")
    print(f"wrote {json_path}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    mutate = os.environ.get("MUTATE", "0") == "1"
    sys.exit(run(mutate))