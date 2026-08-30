#!/usr/bin/env python3
"""TRUSTED GATE TEMPLATES — deterministic, pre-verified math for the common cases.
Policy: if a template applies to the candidate's declared structure, the TEMPLATE is the judge
(trusted tier, same rank as G0). Qwen-generated scripts are used ONLY when no template applies,
and those stay PENDING_AUDIT. Templates are frozen extracts of machinery verified this session
(closure_2026: FROZEN_PRIMITIVE, gauntlet, compiler) — edit only with a committed re-verification."""
import sympy as sp


def applies(gate, cand):
    mr = cand.get("mond_realization", "")
    if gate == "G1" and mr in ("aux_legendre_chi", "constraint_first_q", "nonlocal_f+", "nonlocal_F+"):
        return True
    if gate == "G2" and mr in ("aux_legendre_chi", "constraint_first_q", "nonlocal_f+", "nonlocal_F+"):
        return True
    if gate == "G3":
        return True   # structural TT analysis from declared couplings always possible
    return False


def _cert(gate, status, certificate, **kw):
    out = {"gate": gate, "status": status, "certificate": certificate[:300],
           "assumptions": kw.pop("assumptions", []), "domain": kw.pop("domain", "template"),
           "numeric_values": kw.pop("numeric_values", {}), "trusted_template": True}
    return out


# ------------------------------------------------------------------ G1: exact MOND reduction
def G1(cand):
    """Verify the DECLARED mu-realization reproduces mu(y)=1-e^-y exactly (symbolic identity,
    full domain — not point checks). This certifies the constitutive sector; whether the FULL
    action delivers this reduction still requires the candidate's own couplings to be MOND-neutral,
    which G0 order rules + later gates police."""
    y = sp.symbols('y', positive=True)
    mr = cand.get("mond_realization", "").lower()
    target = 1 - sp.exp(-y)
    if mr == "aux_legendre_chi":
        chi = sp.symbols('chi', positive=True)
        Vp = -sp.log(1 - chi) ** 2                      # frozen V'(chi)
        # constitutive relation: chi = mu(y) solves Vp(chi) = -y^2  (Legendre pairing)
        resid = sp.simplify(Vp.subs(chi, target) + y ** 2)
        ok = resid == 0
        return _cert("G1", "PASS" if ok else "KILL",
                     f"aux-Legendre: V'(mu(y))+y^2 = {resid} (must be 0)",
                     assumptions=["chi algebraic; couplings MOND-neutral per G0"])
    if mr in ("nonlocal_f+",):
        Z = sp.symbols('Z', positive=True)
        Fp = 4 * (1 - (1 + sp.sqrt(Z) / 2) * sp.exp(-sp.sqrt(Z) / 2))
        mu = sp.simplify(1 - 2 * sp.diff(Fp, Z).subs(Z, 4 * y ** 2) * 1)
        # note: 2F+'(Z) = e^{-sqrt(Z)/2}; with Z=4y^2 -> e^{-y}
        resid = sp.simplify((1 - 2 * sp.diff(Fp, Z)).subs(Z, 4 * y ** 2) - target)
        ok = resid == 0
        return _cert("G1", "PASS" if ok else "KILL",
                     f"F+: 1-2F+'(4y^2) - (1-e^-y) = {resid} (must be 0)",
                     assumptions=["quasistatic limit; localization health deferred to G4/G5"])
    if mr == "constraint_first_q":
        # constraint C_M = D_i[mu(y) D^i q] - src with the frozen mu: the reduction is definitional;
        # certify ellipticity across the domain instead (the real content).
        lam_perp = target
        lam_par = sp.simplify(target + y * sp.diff(target, y))
        p_ok = all(sp.limit(l, y, 0) >= 0 for l in (lam_perp, lam_par))
        mins = min(float(lam_par.subs(y, v)) for v in (0.1, 0.5, 1, 2, 5, 10))
        ok = p_ok and mins > 0 and sp.simplify(lam_par - (1 - sp.exp(-y) + y * sp.exp(-y))) == 0
        return _cert("G1", "PASS" if ok else "KILL",
                     f"constraint-first: lam_perp=mu>0, lam_par=1-e^-y+ye^-y>0 (min sampled {mins:.3f})",
                     numeric_values={"lam_par_min_sampled": mins},
                     assumptions=["generic branch; Dirac count deferred to G4"])
    return None


# ------------------------------------------------------------------ G2: Newton/GR limit
def G2(cand):
    """G_eff/G_N = 1 requires: no coupling rescales the Gauss law at y>>1. Deterministic check on
    the declared architecture + the frozen mu limit (exponentially small corrections)."""
    y = sp.symbols('y', positive=True)
    mu = 1 - sp.exp(-y)
    lim = sp.limit(mu, y, sp.oo)
    resc = [cp for cp in cand.get("couplings", [])
            if "g_rescale" in [str(s).lower() for s in cp.get("sources", [])]]
    if resc:
        return _cert("G2", "KILL", "declared G-rescaling coupling present (forbidden repair)")
    if lim != 1:
        return _cert("G2", "KILL", f"mu(inf)={lim}!=1")
    # corrections must be exponential: 1-mu = e^-y (exact for the frozen kernel)
    return _cert("G2", "PASS", "mu->1 with corrections exactly e^-y; no G-rescaling couplings declared",
                 assumptions=["full-solution GR recovery beyond constitutive sector deferred to G4-G8"])


# ------------------------------------------------------------------ G3: tensor sector
def G3(cand):
    """TT-sector structural theorem (verified in the gauntlet): on transverse-traceless h_ij,
    K=0, a_i=0, D_i(scalars)->0 at quadratic order, so ONLY the GR kinetic pair + R3 survive
    UNLESS a coupling touches TT structures directly. Deterministic scan of declared sources."""
    TT_TOUCHING = {"k_ij", "weyl_e", "graviton_mass", "tt_kernel", "riemann"}
    offenders = []
    for cp in cand.get("couplings", []):
        hits = TT_TOUCHING & {str(s).lower() for s in cp.get("sources", [])}
        if hits:
            offenders.append((cp.get("label"), sorted(hits)))
    for f in cand.get("fields", []):
        if f.get("type") == "stf_tensor" and f.get("kinetic") == "standard":
            offenders.append((f.get("name"), ["propagating STF tensor mixes with TT"]))
    if offenders:
        return _cert("G3", "OPEN",
                     f"couplings touch the TT sector {offenders}; c_T needs an explicit derivation",
                     assumptions=["template covers only the no-TT-coupling theorem"])
    return _cert("G3", "PASS",
                 "no declared coupling touches TT structures => quadratic TT action = GR pair + R3 "
                 "=> Q_T>0, c_T^2=1 exactly (gauntlet-verified theorem)",
                 assumptions=["declared architecture faithful (policed by later gates)"])


def _has_second_metric(cand):
    return sum(1 for f in cand.get("fields", []) if f.get("type") == "metric") >= 2

def _timelike_frame_fields(cand):
    return [f for f in cand.get("fields", [])
            if f.get("timelike_background") and f.get("type") in ("vector", "khronon")]


# ------------------------------------------------------------------ G6: lensing / slip-lock (DC-013)
def G6(cand):
    """SLIP-LOCK THEOREM (DC-013, this session, analytic): a FRAME-FREE single-metric theory cannot
    give correct MOND lensing. Diff-invariance locks any extra mode's (Phi,Psi) coupling to the exact
    delta-R direction R^(1)=-2 lap Phi+4 lap Psi (=(1,-2)); on that ray eta=(4L+m)/(8L+m)!=1 for any
    coupling, so enhancement always comes with an f(R)-type slip. Deterministic verdict from the field
    content: frame-free + single-metric => KILL; a genuine 2nd metric or a timelike frame escapes the
    theorem's scope (=> OPEN, escalate for the frame/bimetric analysis)."""
    if _has_second_metric(cand):
        return _cert("G6", "OPEN", "second dynamical metric present: exits slip-lock scope (bimetric) "
                     "-> needs the ghost-free-XOR-MOND price analysis", domain="theorem")
    if _timelike_frame_fields(cand):
        return _cert("G6", "OPEN", "timelike preferred-frame field present: slip-lock does not apply; "
                     "the frame's slip mode must be checked at G8 (P7 fork)", domain="theorem")
    # frame-free single metric: on the locked delta-R ray eta != 1 for any enhancing coupling
    L, mm = sp.symbols('L m', positive=True)
    eta = (4*L + mm) / (8*L + mm)
    locked = sp.solve(sp.Eq(eta, 1), L)   # -> [] (no positive L): eta=1 only in the trivial L=0 limit
    return _cert("G6", "KILL",
                 f"frame-free single-metric: diff-invariance locks coupling to delta-R (1,-2); "
                 f"eta=(4L+m)/(8L+m)=1 has no L>0 solution ({locked}) => f(R)-type slip, cannot lens (DC-013)",
                 numeric_values={"eta_L1": "5/9 (!=1)"},
                 assumptions=["diff-invariant coupling", "no 2nd metric", "no preferred frame"])


# ------------------------------------------------------------------ G8: strong coupling / P7 fork (DC-014)
def G8(cand):
    """P7 + stiff-vector fork (DC-010/DC-014, this session). A screened preferred-frame carrier that
    supplies the (necessary) lensing slip has its slip-carrying longitudinal mode normalized EITHER by
    the screened mass (K_long ~ e^-y -> strong coupling) OR by an independent stiffness (timelike temporal
    ghost). Deterministic: a timelike frame with an e^-y-screened preferred-frame coupling => KILL, unless
    a genuine 2nd metric carries the slip instead (=> OPEN, bimetric)."""
    if _has_second_metric(cand):
        return _cert("G8", "OPEN", "2nd metric may carry the slip without a screened frame mode "
                     "-> bimetric price analysis, not the P7 fork", domain="theorem")
    frames = _timelike_frame_fields(cand)
    screened_pf = [cp for cp in cand.get("couplings", [])
                   if cp.get("preferred_frame") and cp.get("screened_by") == "e^-y"]
    if frames and screened_pf:
        return _cert("G8", "KILL",
                     "screened timelike preferred-frame slip carrier: longitudinal mode normalized by "
                     "the screened mass (K_long~e^-y => P7 strong coupling, Lambda_sc~e^-y/2->0) OR by "
                     "independent stiffness (timelike temporal ghost). Fork kill (DC-014).",
                     assumptions=["timelike frame supplies the slip", "e^-y screening",
                                  "Maxwell blind to longitudinal (FM-000004)"])
    if frames and not screened_pf:
        return _cert("G8", "OPEN", "timelike frame with UNscreened coupling: P2/alpha_2 danger "
                     "(AeST-type) -> needs explicit alpha_1,alpha_2 (G7)", domain="theorem")
    return _cert("G8", "OPEN", "no timelike frame: P7 fork does not apply at template level "
                 "(strong coupling still needs the explicit Lambda_sc calc)", domain="theorem")


# ------------------------------------------------------------------ G4: bimetric structure / BD ghost
def G4(cand):
    """Bimetric-only structural gate (deterministic rules from established massive-gravity results).
    Kill conditions (no trading failures): (a) a claimed massive-graviton mechanism with NO declared
    g<->h interaction potential = the declared theory has no graviton mass (mechanism void) and, with
    matter sourcing the second metric, is doubly-coupled massless bigravity; (b) matter directly
    sourcing the 2nd metric without a declared composite/HR structure = doubly-coupled matter =>
    Boulware-Deser ghost; (c) declared non-HR interaction without an argued degeneracy => BD ghost."""
    if not _has_second_metric(cand):
        return None
    spec = cand.get("bimetric_spec", {}) or {}
    coups = cand.get("couplings", [])
    tokens = [str(s).lower() for cp in coups for s in cp.get("sources", [])]
    metric_names = [f.get("name", "").lower() for f in cand.get("fields", []) if f.get("type") == "metric"]
    has_interaction = (spec.get("interaction") in ("hassan_rosen", "composite")) or         any(sum(1 for mn in metric_names if mn and mn in {str(s).lower() for s in cp.get("sources", [])}) >= 2
            for cp in coups) or ("hr_potential" in tokens) or ("interaction_potential" in tokens)
    matter_on_second = ("rho" in tokens or "matter" in tokens) and spec.get("matter_metric") in (None, "both")         and any("rho" in {str(s).lower() for s in cp.get("sources", [])} or
                "matter" in {str(s).lower() for s in cp.get("sources", [])} for cp in coups)
    mech = (cand.get("claimed_mechanism", "") + " " + cand.get("predicted_weak_field", "")).lower()
    claims_massive = "massive" in mech and "graviton" in mech
    if claims_massive and not has_interaction:
        return _cert("G4", "KILL",
                     "claims a massive-graviton mechanism but declares NO g<->h interaction potential: "
                     "the declared theory has no graviton mass (mechanism void); with matter sourcing "
                     "the 2nd metric it is doubly-coupled massless bigravity => BD ghost. Declare "
                     "bimetric_spec{interaction: hassan_rosen|composite} + the potential coupling.",
                     assumptions=["declared architecture IS the theory"])
    if matter_on_second and spec.get("matter_metric") not in ("g", "f", "composite"):
        return _cert("G4", "KILL",
                     "matter directly sources the 2nd metric with no declared single/composite matter "
                     "metric: doubly-coupled matter => Boulware-Deser ghost (established massive-gravity "
                     "result). Declare bimetric_spec.matter_metric.",
                     assumptions=["no composite metric declared"])
    if spec.get("interaction") == "bimond_connection":
        return _cert("G4", "OPEN", "relative-connection (BIMOND) interaction: DERIVATIVE bimetric "
                     "coupling, generically ghosty but not provably so -- the decisive gate is the "
                     "Hamiltonian/BD constraint audit (A-P ladder D/E). Escalate; do NOT pass "
                     "structurally.", assumptions=["ghost status genuinely open for C-invariants"])
    if spec.get("interaction") == "other":
        return _cert("G4", "KILL", "non-Hassan-Rosen interaction with no argued degeneracy => BD ghost "
                     "(generic potential reintroduces the 6th mode).")
    if spec.get("interaction") in ("hassan_rosen", "composite"):
        return _cert("G4", "PASS", "HR/composite interaction declared: BD-ghost-free by construction "
                     "at the structural level (full ADM Hessian rank still audited on escalation).",
                     assumptions=["HR potential exactly of ghost-free form"])
    return _cert("G4", "OPEN", "bimetric structure incompletely declared: cannot certify; escalate "
                 "only after bimetric_spec is complete.")


# ------------------------------------------------------------------ G5: bimetric MOND-source fork
def G5(cand):
    """The ghost-free-XOR-MOND fork (priced in closure_2026/bimetric_door): a LINEAR massive graviton
    gives Yukawa (fixed length, enhance-short/cutoff-long) which can NEVER equal mu(y)=1-e^-y (an
    acceleration scale). Deterministic: mond_source=linear_massive_graviton => KILL. Nonlinear/composite
    claims go OPEN -> escalation (that is where the genuine unknown lives). Higuchi flagged."""
    if not _has_second_metric(cand):
        return None
    spec = cand.get("bimetric_spec", {}) or {}
    src = spec.get("mond_source")
    if src == "linear_massive_graviton":
        return _cert("G5", "KILL",
                     "MOND from the LINEAR massive-graviton sector: Yukawa force (fixed Compton length, "
                     "vDVZ 4/3 short-range + long-range cutoff) is structurally NOT mu(y)=1-e^-y (an "
                     "acceleration scale). Ghost-free-XOR-MOND fork (bimetric_door price).",
                     assumptions=["linear regime dominates galactic scales"])
    if src == "connection_invariants":
        return _cert("G5", "OPEN", "MOND from relative-connection C-invariants (BIMOND route): the "
                     "acceleration scale arises naturally from first-derivative differences (unlike the "
                     "HR Yukawa). NR limit + slip must be derived; escalate with the Hamiltonian audit "
                     "as the FIRST calculation.", assumptions=["Milgrom NR-limit construction"])
    if src in ("nonlinear_helicity0", "composite_matter", "f_sector"):
        return _cert("G5", "OPEN",
                     f"MOND from {src}: the genuine unknown (nonlinear sector). Escalate with the full "
                     "8-step bimetric audit (exact action, ADM Hessian, constraint rank, Higuchi at "
                     "m_FP~H0, spherical MOND reduction, lensing, c_T, PPN). No failure-trading.",
                     assumptions=["Higuchi m^2>=2H^2 marginal at m_FP~H0 (flag)"])
    return _cert("G5", "OPEN", "bimetric_spec.mond_source undeclared: cannot run the fork; candidate "
                 "must declare where the a0 acceleration scale comes from.")


TEMPLATES = {"G1": G1, "G2": G2, "G3": G3, "G4": G4, "G5": G5, "G6": G6, "G8": G8}


def run(gate, cand):
    fn = TEMPLATES.get(gate)
    if fn is None:
        return None
    if gate in ("G4", "G5", "G6", "G8"):  # theorem-gates apply to every candidate (self-scoping)
        try:
            return fn(cand)
        except Exception as e:
            return _cert(gate, "BLOCKED", f"template error: {e}")
    if not applies(gate, cand):
        return None
    try:
        return fn(cand)
    except Exception as e:
        return _cert(gate, "BLOCKED", f"template error: {e}")
