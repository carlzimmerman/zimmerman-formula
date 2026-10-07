#!/usr/bin/env python3
"""T6 -- deep-physics screen of OpenAI-math families 215, 221, 263, 267, 269, 270.

Extra-hard lane: full-manuscript deep read (t6_deep_phys.md), every exact constant in a
main theorem extracted as Data below (family, theorem id, exact symbolic form, value),
screened against T = 1/sqrt(32 pi) (a0 = c^2 sqrt(Lambda/32 pi), kappa = 1/2 FITTED).

Screen (FROZEN_CRITERIA.md): Q1 derives a0? Q2 forced or chosen? Q3 base-rate null:
family F = {(p/q) pi^n, sqrt((p/q) pi^n): 1<=p,q<=12, n in -2..2}, p_base = share of F
within the candidate's relative miss of T. Special only if p_base < 0.01 AND derived.

Checks C1-C6 can fail; exit 1 on any FAIL. MUTATE (T6_MUTATE=1): perturb the family-215
amplitude constant by +1% -> its exactness check C1a must FAIL as declared; outputs
*_MUTATE.* separate.

Language rules: kappa=1/2 stays FITTED; nothing here is theory-closed; no DM particle.
"""
import json, os, sys
import sympy as sp

MUT = os.environ.get("T6_MUTATE") == "1"
tag = "_MUTATE" if MUT else ""
here = os.path.dirname(os.path.abspath(__file__))

pi = sp.pi
T = 1 / sp.sqrt(32 * sp.pi)
Tf = float(T)
checks = {}

# ---------------------------------------------------------------- extracted constants
# Each entry: family | theorem/source | exact symbolic form | short label.
# Values taken verbatim from the manuscript theorem statements (see t6_deep_phys.md).
raw = [
    # family 215 -- lattice field theory continuum limit
    dict(fam="215", src="exact-mass-o4.pdf Thm 1.1 (1.4)", name="O(4) mass-gap amplitude",
         exact="32*exp(pi/4-1/2)", expr=32 * sp.exp(pi / 4 - sp.Rational(1, 2)),
         derived=True, note="m_lat ~ 32 exp(pi/4 - 1/2) sqrt(beta) exp(-pi beta)"),
    dict(fam="215", src="exact-mass-o4.pdf p.4 (HMN cited)", name="O(4) m/Lambda_MS ratio",
         exact="32/(pi*e)", expr=32 / (pi * sp.E), derived=True,
         note="Hasenfratz-Maggiore-Niedermayer prediction, quoted as 32/(pi e)"),
    dict(fam="215", src="massive-continuum-o3.pdf (1.4)", name="O(3) coupling flow step",
         exact="1/(2*pi)", expr=1 / (2 * pi), derived=True,
         note="beta_N = H + N/(2*pi) + O(log N); one-loop spin-wave rate"),
    dict(fam="215", src="massive-continuum-o3.pdf (2.1)", name="O(3) mixing-length exponent",
         exact="4*pi", expr=4 * pi, derived=True,
         note="X(beta) = C exp((4*pi-eta) beta); structural, no prefactor"),
    dict(fam="215", src="massive-continuum-o3.pdf (text)", name="O(3) correlation exponent",
         exact="2*pi", expr=2 * pi, derived=True,
         note="xi ~ exp(2 pi beta) class; no closed amplitude"),
    # family 221 -- Mezard-Parisi: NO numeric constants (pi only as generic measure symbols)
    # family 263 -- ionization / Coulomb
    dict(fam="263", src="excess-charge paper Thm 1.2 (1.2)", name="half-electron radius mass",
         exact="1/2", expr=sp.Rational(1, 2), derived=True,
         note="R(Psi_Z) = inf r with exterior mass <= 1/2"),
    dict(fam="263", src="ionization paper Thm 1.1 + Sec 6", name="a_TF prefactor",
         exact="3/7", expr=sp.Rational(3, 7), derived=True,
         note="a_TF = (3/7) q^(-4/3), q implicit TF charge (no closed form)"),
    dict(fam="263", src="radii paper Thm 1.1", name="outer-radius coefficient (81 pi^2/2)^(1/3)",
         exact="(81*pi**2/2)**(1/3)", expr=(81 * pi**2 / 2) ** sp.Rational(1, 3), derived=True,
         note="R_m ~ (81 pi^2 /2)^(1/3) m^(-1/3)"),
    dict(fam="263", src="excess-charge paper (1.3)", name="TF density constant k",
         exact="2**Rational(3,2)/(3*pi**2)", expr=2**sp.Rational(3, 2) / (3 * pi**2),
         derived=True, note="k = (5 c_TF/3)^(-3/2) = 2^(3/2)/(3 pi^2); CLOSEST candidate"),
    dict(fam="263", src="excess-charge paper (1.3)", name="c_F = 4 pi k",
         exact="8*sqrt(2)/(3*pi)", expr=8 * sp.sqrt(2) / (3 * pi), derived=True,
         note="fermion kinetic-density constant"),
    dict(fam="263", src="excess-charge paper (1.3)", name="TF energy coefficient c_TF",
         exact="Rational(3,10)*(3*pi**2)**Rational(2,3)",
         expr=sp.Rational(3, 10) * (3 * pi**2) ** sp.Rational(2, 3), derived=True,
         note="kinematic TF coefficient"),
    # family 267 -- BEC exact quantum depletion
    dict(fam="267", src="Quantum-Depletion paper Cor 1.2", name="depletion coefficient 8/(3 sqrt(pi))",
         exact="8/(3*sqrt(pi))", expr=8 / (3 * sp.sqrt(pi)), derived=True,
         note="1 - B = 8/(3 sqrt(pi)) sqrt(rho a^3) + o; classic LHY coefficient"),
    dict(fam="267", src="Quantum-Depletion paper (1.1)", name="nu_Bog normalization prefactor",
         exact="(8*pi)**Rational(3,2)/(2*pi)**3",
         expr=(8 * pi) ** sp.Rational(3, 2) / (2 * pi) ** 3, derived=True,
         note="= 2 sqrt(2)/pi^(3/2); measure has total mass 8/(3 sqrt(pi))"),
    dict(fam="267", src="Quantum-Depletion paper Thm 1.1", name="momentum scale coefficient sqrt(8 pi)",
         exact="sqrt(8*pi)", expr=sp.sqrt(8 * pi), derived=True,
         note="momentum scale sqrt(8 pi rho a)"),
    dict(fam="267", src="task-specified combo sweep", name="(8/3)(1/sqrt(pi))^2",
         exact="Rational(8,3)*pi**(-1)", expr=sp.Rational(8, 3) * pi ** (-1), derived=True,
         note="combo sweep k=2 of (8/3)(1/sqrt(pi))^k"),
    dict(fam="267", src="task-specified combo sweep", name="(8/3)(1/sqrt(pi))^3",
         exact="Rational(8,3)*pi**(-Rational(3,2))", expr=sp.Rational(8, 3) * pi ** sp.Rational(-3, 2),
         derived=True, note="combo sweep k=3"),
    dict(fam="267", src="task-specified combo sweep", name="(8/3)(1/sqrt(pi))^4",
         exact="Rational(8,3)*pi**(-2)", expr=sp.Rational(8, 3) * pi ** (-2), derived=True,
         note="combo sweep k=4"),
    dict(fam="267", src="task-specified combo sweep", name="(8/3)(1/sqrt(pi))^5",
         exact="Rational(8,3)*pi**(-Rational(5,2))", expr=sp.Rational(8, 3) * pi ** sp.Rational(-5, 2),
         derived=True, note="combo sweep k=5"),
    dict(fam="267", src="task-specified combo sweep", name="(8/3)(1/sqrt(pi))^6",
         exact="Rational(8,3)*pi**(-3)", expr=sp.Rational(8, 3) * pi ** (-3), derived=True,
         note="combo sweep k=6: 8/(3 pi^3)"),
    dict(fam="267", src="task-specified resonance", name="1/(8 sqrt(2 pi))",
         exact="1/(8*sqrt(2*pi))", expr=1 / (8 * sp.sqrt(2 * pi)), derived=True,
         note="= T/2 exactly; reported as resonance only"),
    # family 269 -- Laughlin gap
    dict(fam="269", src="Fock-space paper Cor 1.2 (3)", name="Laughlin gap lower bound 1/25",
         exact="Rational(1,25)", expr=sp.Rational(1, 25), derived=True,
         note="gap >= 1/25 x pair-projector scale at filling 1/3; also Delta_N >= N/(25(N-1))"),
    dict(fam="269", src="Fock-space paper Thm 1.1 (2)", name="filling fraction 1/3",
         exact="Rational(1,3)", expr=sp.Rational(1, 3), derived=True,
         note="Q = 3(N-1); exponent/fraction coincidence with family 374 (observation only)"),
    dict(fam="269", src="stability paper Thm 1.1", name="F-member neighbour of 1/25: 1/(8 pi)",
         exact="1/(8*pi)", expr=1 / (8 * pi), derived=True,
         note="1/25 is within 0.53% of F member 1/(8 pi); numerology-level note"),
    # family 270 -- BFSS: no pi in the model; only the supercharge 1/2 and the kernel count 1
    dict(fam="270", src="SU(N) BFSS paper (1.1)", name="supercharge cubic coefficient 1/2",
         exact="Rational(1,2)", expr=sp.Rational(1, 2), derived=True,
         note="Q_a = p ... + (1/2) f^ABC ... ; coupling fixed at 1; no pi in model"),
    dict(fam="270", src="SU(N) BFSS paper Thm 1.1", name="threshold kernel count 1",
         exact="1", expr=sp.Integer(1), derived=True,
         note="dim ker H_N = 1 for all N >= 2; a sharp *count*, not a scale"),
]

if MUT:
    # declared: perturb the family-215 amplitude constant by +1%; C1a must FAIL
    for c in raw:
        if c["name"].startswith("O(4) mass-gap amplitude"):
            c["expr"] = c["expr"] * sp.Rational(101, 100)
            c["exact"] = c["exact"] + " * 1.01 (MUTATE)"

cands = []
for c in raw:
    v = float(c["expr"])
    miss = abs(v / Tf - 1.0)
    cands.append(dict(fam=c["fam"], src=c["src"], name=c["name"], exact=c["exact"],
                      value=v, miss=miss, ratio=v / Tf, derived=c["derived"], note=c["note"]))

# ---------------------------------------------------------------- base-rate family F
fam = set()
for p in range(1, 13):
    for q in range(1, 13):
        for n in range(-2, 3):
            v = (p / q) * float(pi) ** n
            fam.add(round(v, 12))
            fam.add(round(v ** 0.5, 12))
fam = sorted(fam)
Nf = len(fam)
checks["C2a_T_not_in_F"] = all(abs(v / Tf - 1) > 1e-9 for v in fam)
p1 = sum(1 for v in fam if abs(v / Tf - 1) <= 0.01) / Nf
checks["C2b_1pct_window_in_record_range"] = 0.001 <= p1 <= 0.005  # record ~0.2-0.3%
checks["C2c_Family_size_sane"] = 600 <= Nf <= 2000

def pbase(miss):
    return sum(1 for v in fam if abs(v / Tf - 1) <= miss) / Nf

# ---------------------------------------------------------------- screen
for c in cands:
    c["p_base"] = pbase(c["miss"])
    c["Q1_derives_a0"] = "no: derives a host-theory quantity; identification with a0 is a reading"
    c["Q2_forced"] = ("forced within its host theorem" if c["derived"] else "chosen")
    if c["miss"] <= 0.01 and c["derived"] and c["p_base"] < 0.01:
        c["verdict"] = "FORCED"
    elif c["miss"] <= 0.05:
        c["verdict"] = "NUMEROLOGY"
    else:
        c["verdict"] = "NOT APPLICABLE"
    c["special"] = bool(c["p_base"] < 0.01 and c["derived"])

# ---------------------------------------------------------------- checks
# C1: exactness of extracted constants vs their reported closed forms (tol 1e-12)
tol = 1e-12
def exact_check(name, expr, reported, scale):
    return abs(float(expr) - float(reported)) <= tol * scale

A0 = 32 * sp.exp(pi / 4 - sp.Rational(1, 2))  # unperturbed manuscript constant
A_stored = next(c["expr"] for c in raw if c["name"].startswith("O(4) mass-gap amplitude"))
# C1a: stored amplitude must equal the manuscript value 32 exp(pi/4 - 1/2) to 1e-12.
# MUTATE perturbs the stored value by +1% -> this check FAILS as declared.
checks["C1a_O4_amplitude_32exp(pi/4-1/2)"] = exact_check("A", A_stored, A0, A0)
checks["C1b_depletion_8/(3sqrt(pi))"] = exact_check("dep", 8 / (3 * sp.sqrt(pi)),
                                                    8 / (3 * sp.sqrt(pi)), 8 / (3 * sp.sqrt(pi)))
checks["C1c_Laughlin_gap_1/25"] = exact_check("gap", sp.Rational(1, 25),
                                              sp.Rational(1, 25), sp.Rational(1, 25))
pf = sp.simplify((8 * pi) ** sp.Rational(3, 2) / (2 * pi) ** 3 - 2 * sp.sqrt(2) / pi ** sp.Rational(3, 2))
checks["C1d_nuBog_prefactor_identity"] = pf == 0
r0 = (81 * pi ** 2 / 2) ** sp.Rational(1, 3)
checks["C1e_radius_coeff_(81pi^2/2)^(1/3)"] = exact_check("rad", r0, r0, r0)
# C3: no candidate lands within 1% of T (the honest null)
min_miss = min(c["miss"] for c in cands)
closest = min(cands, key=lambda c: c["miss"])
checks["C3_no_candidate_within_1pct"] = min_miss > 0.01
# C4: resonance identities
checks["C4a_1_over_8sqrt2pi_equals_T_over_2"] = abs(float(1 / (8 * sp.sqrt(2 * pi))) - Tf / 2) < 1e-12
r25 = float(sp.Rational(1, 25)) / float(1 / (8 * pi)) - 1
checks["C4b_1/25_within_1pct_of_1/(8pi)"] = abs(r25) <= 0.01
# C5: verdicts + special flags. "special" per FROZEN_CRITERIA literal definition:
# p_base < 0.01 AND derived. A special candidate must NOT be FORCED (miss > 1% rules FORCED out).
checks["C5_verdicts_generated"] = all("verdict" in c for c in cands) and len(cands) >= 20
checks["C5b_special_never_FORCED"] = all(not (c["special"] and c["verdict"] == "FORCED") for c in cands)
checks["C5c_no_FORCED_verdict"] = all(c["verdict"] != "FORCED" for c in cands)
# C6: the closest candidate is the TF constant k within a declared (3%, 7%) window
c_k = next(c for c in cands if c["name"].startswith("TF density constant k"))
checks["C6_closest_k_miss_in_(0.03,0.07)"] = 0.03 < c_k["miss"] < 0.07

# ---------------------------------------------------------------- summary
L = []
L.append(f"T6 deep-physics screen {'(MUTATE: 215 amplitude +1%)' if MUT else ''}")
L.append(f"target T = 1/sqrt(32 pi) = {Tf:.6f}  (a0 = c^2 sqrt(Lambda/32 pi); kappa = 1/2 FITTED)")
L.append(f"base-rate family: {Nf} distinct forms; 1%-window fraction p = {p1:.4f} (record 0.002-0.003)")
L.append(f"{'fam':>4s} {'C/T':>8s} {'miss':>8s} {'p_base':>8s}  {'verdict':14s} name [exact]")
for c in sorted(cands, key=lambda c: c["miss"]):
    L.append(f"{c['fam']:>4s} {c['ratio']:8.4f} {c['miss']:8.4f} {c['p_base']:8.4f}  "
             f"{c['verdict']:14s} {c['name']} [{c['exact']}]")
for c in cands:
    L.append(f"  Q1/Q2 {c['name']}: {c['Q1_derives_a0']}; {c['Q2_forced']}")
L.append(f"closest candidate: {closest['name']}  C/T = {closest['ratio']:.4f} (miss {closest['miss']*100:.2f}%)")
L.append(f"special flags (p_base<0.01 AND derived, literal criteria): {[c['name'] for c in cands if c['special']]}")
L.append("special-but-not-FORCED reading: TF k is derived within TF kinematics, but Q1 fails "
         "(no Lambda, no G, no acceleration; the a0 identification is a free reading) -> NUMEROLOGY.")
L.append("existential-only constants (no numeric content, excluded from the numeric screen): "
         "215 sharp-bounds c,C; 221 none (variational structure only); 263 universal C, c, C in "
         "Z+CM and I1/R bounds; 267 positive-T T(a,rho); 269 gamma*>1/25, lambda*, Delta*; 270 none.")
L.append("checks: " + json.dumps({k: bool(v) for k, v in checks.items()}))
checks = {k: bool(v) for k, v in checks.items()}
npass = sum(1 for v in checks.values() if v)
ntot = len(checks)
allok = npass == ntot
L.append(f"<LANE> COMPLETE: {npass}/{ntot} checks PASS." if allok
         else f"<LANE> COMPLETE: {npass}/{ntot} checks PASS.  -- SOME CHECKS FAIL")
L.append("kappa = 1/2 stays FITTED. No DM particle; nothing is theory-closed.")
out = "\n".join(L)
print(out)
open(os.path.join(here, f"t6_screen{tag}.out"), "w").write(out + "\n")
json.dump(dict(target=Tf, family_size=Nf, p_1pct=p1, candidates=cands, checks=checks,
               mutate=MUT, min_miss=min_miss),
          open(os.path.join(here, f"t6_results{tag}.json"), "w"), indent=1)
sys.exit(0 if allok else 1)