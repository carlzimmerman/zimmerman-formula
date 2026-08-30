#!/usr/bin/env python3
"""THE DETERMINISTIC EVALUATOR — authoritative. Qwen proposes; this module (and the sympy scripts it
executes) judge. No status here can be overridden by model prose.

Two tiers:
  TIER 1 (fully deterministic, this file): dedup + dead-class matching + G0 structural/order rules +
    the prohibited-ingredient rules P1-P7 read from KNOWLEDGE_GRAPH.json. Cheap; kills most candidates.
  TIER 2 (script-certified): gates G1..G12 run as GENERATED sympy/numpy scripts under a strict
    certificate contract: the script must exit 0 and print one line `CERTIFICATE_JSON: {...}` with
    status in {PASS, OPEN, CONDITIONAL, KILL}. The referee agent then attacks the script+output.
    A gate is machine-PASS only if: script exit 0 + certificate PASS + referee does not refute.
    HONESTY: machine-PASS on Tier-2 gates is still "PASS(script)" — final SURVIVOR promotion requires
    the committed scripts to survive a human/Claude audit (see program.md). Qwen never grades itself."""
import json, os, re, subprocess, sys, hashlib, time

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state")
DB = os.path.join(HERE, "database")

GATES = ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12"]
CHEAP_GATES = ["G0"]           # fully deterministic here
SCRIPT_GATES = GATES[1:]       # require a generated, executed, refereed script


def _kg():
    return json.load(open(os.path.join(STATE, "KNOWLEDGE_GRAPH.json")))


# ------------------------------------------------------------------ dead-class signature matching
def matches_dead_class(canon, dead_class):
    """A dead class carries a machine signature: a set of required structural predicates.
    ALL must hold for the candidate to be excluded (conservative: single-candidate kills never
    auto-generalize; only human/Claude-promoted class rules get signatures)."""
    sig = dead_class.get("signature", {})
    if not sig:
        return False
    # scope guard: theorems derived for single-metric must NOT match bimetric candidates
    if sig.get("single_metric_only") and \
            sum(1 for f in canon["fields"] if f["type"] == "metric") >= 2:
        return False
    for k, v in sig.items():
        if k == "single_metric_only":
            continue
        if k == "family" and canon.get("family") != v:
            return False
        if k == "any_coupling":  # candidate must contain a coupling matching ALL listed props
            found = False
            for cp in canon["couplings"]:
                if all(cp.get(pk) == pv for pk, pv in v.items()):
                    found = True
            if not found:
                return False
        if k == "no_field_type" and any(f["type"] == v for f in canon["fields"]):
            return False
        if k == "has_field":
            if not any(all(f.get(pk) == pv for pk, pv in v.items()) for f in canon["fields"]):
                return False
    return True


# ------------------------------------------------------------------ TIER 1: G0 + P-rules
def gate_G0(cand, canon):
    """Structural/order consistency + prohibited ingredients. Returns certificate dict."""
    kills, notes = [], []
    coup = canon["couplings"]; fields = canon["fields"]

    # -- order counting (the T3/order-counting lesson): a coupling meant to CANCEL the O(eps^2)
    #    MOND anisotropic stress must itself be O(eps^2). Declared orders are checked for coherence.
    for cp in coup:
        o = cp.get("order_in_phi")
        if o is None:
            kills.append(f"coupling {cp['sources']} has no declared order_in_phi (G0 requires it)")
        elif cp.get("preferred_frame") is False and "lensing_canceller" in cp["sources"] and o != 2:
            kills.append(f"lensing-canceller at O(eps^{o}) != O(eps^2): cannot cancel Sigma_P (P1/T3)")

    # -- P1 quadratic-only carrier stress
    tf_carriers = [f for f in fields if f["type"] == "stf_tensor"]
    if tf_carriers:
        lin = [cp for cp in coup if cp.get("order_in_phi") == 2 and not cp.get("preferred_frame")]
        if not lin:
            notes.append("STF carrier present with no O(eps^2) non-PF coupling: P1 risk (flag)")

    # -- P2 unscreened constant preferred-frame coupling
    for cp in coup:
        if cp.get("preferred_frame") and cp.get("screened_by") not in ("e^-y",):
            kills.append("preferred-frame coupling with no e^-y screening (P2: AeST/disformal kill)")

    # -- P3 lapse-weighted MOND sector
    for cp in coup:
        if cp.get("lapse_weighted"):
            kills.append("MOND sector weights the lapse (P3: H_perp demotion -> extra DOF, proven twice)")

    # -- P6 temporal nonlocality
    for cp in coup:
        if cp.get("nonlocal") == "temporal":
            kills.append("temporal nonlocality on the primary branch (P6: needs separate causal branch)")

    # -- P7 screening kills kinetic normalization: if ANY field's kinetic term is declared to be
    #    controlled by the same screened coefficient, kill (the khronometric wound, now a rule).
    for f in fields:
        if f.get("kinetic") == "degenerate":
            scr = [cp for cp in coup if cp.get("screened_by") == "e^-y"]
            if scr and cand.get("kinetic_normalization_source") == "screened_coupling":
                kills.append("PPN-visible screened coupling ALSO controls kinetic normalization (P7)")

    # -- P4 heuristic: a 'nonlocal'/'auxiliary' field with standard kinetic term is propagating
    for f in fields:
        if f.get("kinetic") == "standard" and f["type"] in ("scalar", "vector") \
                and f.get("timelike_background"):
            notes.append("timelike-background propagating field: G7 preferred-frame danger (must compute)")

    # -- MECHANISM LINTER (claim-vs-action): a narrative claim with no declared structural basis
    #    is a contradiction, not a promissory note (the FM-000035 lesson, generalized).
    mech = (cand.get("claimed_mechanism", "") + " " + cand.get("predicted_weak_field", "")).lower()
    n_metrics = sum(1 for f in fields if f.get("type") == "metric")
    tokens = [str(s).lower() for cp in coup for s in cp.get("sources", [])]
    if ("massive" in mech and "graviton" in mech) and n_metrics >= 2:
        spec = cand.get("bimetric_spec", {}) or {}
        if spec.get("interaction") not in ("hassan_rosen", "composite", "bimond_connection"):
            kills.append("MECHANISM_CONTRADICTION: claims a massive graviton but declares no g<->h "
                         "interaction (no interaction => m_FP=0 => mechanism void)")
    if any(cp.get("nonlocal") == "spatial" for cp in coup) and not any(
            f.get("timelike_background") for f in fields) and n_metrics < 2:
        notes.append("COVARIANCE_CLAIM_UNVERIFIED: spatial elliptic operator declared with no frame "
                     "and one metric -- what defines the spatial slice? must be answered at audit")
    # -- DECLARATION COHERENCE (FM-000060 lessons): labels must be backed by structure.
    conn = (cand.get("connection") or "riemannian").lower()
    if conn == "riemannian" and any(t in ("torsion_t",) for t in tokens):
        kills.append("INCOHERENT: torsion_T source on a riemannian connection (torsion==0 identically; "
                     "the coupling is empty)")
    if conn != "nonmetricity" and "nonmetricity_q" in tokens and conn != "teleparallel":
        if conn == "riemannian":
            kills.append("INCOHERENT: nonmetricity_Q source on a riemannian connection (Q==0)")
    for f in fields:
        if f.get("kinetic") == "higher_derivative":
            if not any(k in mech for k in ("ostrogradsky", "degener", "constraint")):
                kills.append("higher_derivative kinetic with NO named Ostrogradsky evasion "
                             "(degeneracy/constraint) => ghost by default")
    n_metric_fields = sum(1 for f in fields if f.get("type") == "metric")
    for f in fields:
        if f.get("type") == "multiplier" and f.get("kinetic") not in ("none", None):
            kills.append("INCOHERENT: multiplier field with a kinetic term (a Lagrange multiplier is "
                         "non-dynamical by definition; kinetic must be 'none')")
        if f.get("type") == "metric" and f.get("kinetic") not in ("standard", None):
            kills.append(f"INCOHERENT: metric field with kinetic='{f.get('kinetic')}' (a metric carries "
                         "the Einstein-Hilbert kinetic; a non-propagating 'metric' is not a metric)")
    if any(t in ("c_invariant_1", "c_tensor") for t in tokens) and n_metric_fields < 2:
        kills.append("INCOHERENT: connection-difference C-invariant (Gamma(g)-Gamma(h)) source with <2 "
                     "metrics (C requires TWO metrics; meaningless with one)")
    sect = (cand.get("scalar_sector") or "propagating").lower()
    if sect in ("instantaneous", "constrained") and not (
            any(f.get("type") == "multiplier" for f in fields) or
            any(f.get("kinetic") == "degenerate" for f in fields)):
        kills.append(f"scalar_sector='{sect}' declared with NO backing structure (no multiplier, no "
                     "degenerate kinetic) -- unearned declaration")
    status = "KILL" if kills else "PASS"
    return {"gate": "G0", "status": status, "certificate": "; ".join(kills) or "structural checks clean",
            "notes": notes, "assumptions": ["declared architecture object is faithful"],
            "domain": "structural"}


# ------------------------------------------------------------------ TIER 2: script gates
CERT_RE = re.compile(r"CERTIFICATE_JSON:\s*(\{.*\})")


def run_gate_script(cid, gate, script_text, timeout=1800):
    """Execute a generated gate script deterministically; parse its certificate. The SCRIPT is the
    judge; its stdout certificate is recorded verbatim. Script is saved permanently (audit trail)."""
    sdir = os.path.join(HERE, "gate_scripts")
    spath = os.path.join(sdir, f"{cid}_{gate}.py")
    with open(spath, "w") as f:
        f.write(script_text)
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, spath], capture_output=True, text=True, timeout=timeout,
                           cwd=sdir)
    except subprocess.TimeoutExpired:
        return {"gate": gate, "status": "BLOCKED", "certificate": f"timeout {timeout}s",
                "script": spath, "runtime": time.time() - t0}
    out = (p.stdout or "") + "\n" + (p.stderr or "")
    with open(spath.replace(".py", ".out"), "w") as f:
        f.write(out)
    m = CERT_RE.search(p.stdout or "")
    if p.returncode != 0 or not m:
        return {"gate": gate, "status": "BLOCKED",
                "certificate": f"exit={p.returncode}, certificate_line={'found' if m else 'MISSING'}",
                "script": spath, "runtime": time.time() - t0}
    try:
        cert = json.loads(m.group(1))
    except Exception as e:
        return {"gate": gate, "status": "BLOCKED", "certificate": f"unparseable certificate: {e}",
                "script": spath, "runtime": time.time() - t0}
    cert.setdefault("gate", gate)
    if cert.get("status") not in ("PASS", "OPEN", "CONDITIONAL", "KILL"):
        cert["status"] = "BLOCKED"
    cert["script"] = spath
    cert["runtime"] = time.time() - t0
    cert["test_hash"] = hashlib.sha256(script_text.encode()).hexdigest()[:12]
    return cert


def prior_certificate(cid_arch_hash, gate, test_hash=None):
    """Never re-run certified work: same architecture + same gate (+ same script) => load prior."""
    best = None
    path = os.path.join(DB, "experiments.jsonl")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        for line in f:
            try: row = json.loads(line)
            except Exception: continue
            if row.get("arch_hash") == cid_arch_hash and row.get("gate") == gate:
                if test_hash is None or row.get("test_hash") == test_hash:
                    best = row
    return best


def explain_dead_match(canon, dead_class):
    """Human-readable decisive reason a candidate matched a dead-class signature (for architect feedback)."""
    sig = dead_class.get("signature", {})
    parts = []
    for k, v in sig.items():
        if k == "any_coupling":
            parts.append(f"contains a coupling with {v}")
        elif k == "no_field_type":
            parts.append(f"has NO field of type '{v}'")
        elif k == "has_field":
            parts.append(f"contains a field matching {v}")
        elif k == "family":
            parts.append(f"family == {v}")
    return f"{dead_class['class_id']} ({dead_class['name']}): " + "; ".join(parts) +            f" -- decisive: {dead_class.get('decisive','')[:200]}"
