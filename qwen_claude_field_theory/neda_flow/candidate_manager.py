#!/usr/bin/env python3
"""Candidate schema, canonicalization, permanent IDs, deduplication, genealogy.
Every candidate is a machine-readable architecture object (never prose-only)."""
import json, hashlib, os, time

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "database")
STATE = os.path.join(HERE, "state")

# ---- the architecture schema (see architecture_grammar.md). Free-text fields are allowed but the
# ---- structural fields below are what canonicalization + deterministic gates read.
REQUIRED_FIELDS = ["name", "family", "fields", "couplings", "mond_realization", "claimed_mechanism"]
# fields:   list of {name, type: scalar|vector|stf_tensor|metric|khronon|multiplier,
#                    kinetic: none|standard|degenerate, timelike_background: bool}
# couplings: list of {label, sources: [<ingredient tokens>], order_in_phi: int|null,
#                     preferred_frame: bool, screened_by: "e^-y"|null, lapse_weighted: bool,
#                     nonlocal: none|spatial|temporal}
# mond_realization: "aux_legendre_chi" | "constraint_first_q" | "nonlocal_F+" | <new, described>


def canonicalize(cand):
    """Order-independent canonical form: sort fields/couplings, drop free-text, normalize names.
    Field renames collapse (fields keyed by (type,kinetic,timelike) signature, not by name)."""
    c = {"family": cand.get("family", "").strip().lower(),
         "mond_realization": cand.get("mond_realization", "").strip().lower(),
         "fields": sorted(
             [{"type": f.get("type"), "kinetic": f.get("kinetic", "none"),
               "timelike_background": bool(f.get("timelike_background", False))}
              for f in cand.get("fields", [])],
             key=lambda f: json.dumps(f, sort_keys=True)),
         "couplings": sorted(
             [{"sources": sorted([str(s).lower() for s in cp.get("sources", [])]),
               "order_in_phi": cp.get("order_in_phi"),
               "preferred_frame": bool(cp.get("preferred_frame", False)),
               "screened_by": cp.get("screened_by"),
               "lapse_weighted": bool(cp.get("lapse_weighted", False)),
               "nonlocal": cp.get("nonlocal", "none")}
              for cp in cand.get("couplings", [])],
             key=lambda cp: json.dumps(cp, sort_keys=True))}
    return c


def arch_hash(cand):
    return hashlib.sha256(json.dumps(canonicalize(cand), sort_keys=True).encode()).hexdigest()[:16]


def _load_jsonl(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try: out.append(json.loads(line))
                except Exception: pass
    return out


def append_jsonl(path, obj):
    with open(path, "a") as f:
        f.write(json.dumps(obj, sort_keys=True) + "\n")


def next_id():
    cands = _load_jsonl(os.path.join(DB, "candidates.jsonl"))
    return f"FM-{len(cands) + 1:06d}"


def dedup_check(cand):
    """Returns (status, ref) where status in {NEW, DUPLICATE_OF_KILLED, DUPLICATE_OF_SURVIVOR,
    DUPLICATE_PENDING}. Never run a killed architecture again; resume survivors from new gates."""
    h = arch_hash(cand)
    for row in _load_jsonl(os.path.join(DB, "candidates.jsonl")):
        if row.get("arch_hash") == h:
            st = row.get("status", "")
            if st in ("KILL", "DUPLICATE_OF_KILLED"):
                return "DUPLICATE_OF_KILLED", row["candidate_id"]
            if st == "SURVIVOR":
                return "DUPLICATE_OF_SURVIVOR", row["candidate_id"]
            return "DUPLICATE_PENDING", row["candidate_id"]
    # class-level exclusions (DEAD_CLASSES carry machine-checkable signatures)
    dead = json.load(open(os.path.join(STATE, "DEAD_CLASSES.json")))
    from evaluator import matches_dead_class
    for dc in dead.get("classes", []):
        if matches_dead_class(canonicalize(cand), dc):
            return "DUPLICATE_OF_KILLED", dc["class_id"]
    return "NEW", None


def register(cand, parent=None, mutation=None, reason=None, failed_gate=None):
    """Permanent registration. IDs never reused; candidates never overwritten."""
    cid = next_id()
    row = {"candidate_id": cid, "arch_hash": arch_hash(cand), "ts": time.time(),
           "status": "REGISTERED", "family": cand.get("family"), "name": cand.get("name"),
           "mech_fp": mechanism_fingerprint(cand)[0]}
    append_jsonl(os.path.join(DB, "candidates.jsonl"), row)
    with open(os.path.join(HERE, "candidates", f"{cid}.json"), "w") as f:
        json.dump(cand, f, indent=1, sort_keys=True)
    if parent:
        append_jsonl(os.path.join(DB, "transitions.jsonl"),
                     {"parent_candidate": parent, "child_candidate": cid, "mutation_type": mutation,
                      "reason_for_mutation": reason, "failed_gate_being_addressed": failed_gate,
                      "ts": time.time()})
    return cid


def set_status(cid, status, extra=None):
    row = {"candidate_id": cid, "status": status, "ts": time.time()}
    if extra: row.update(extra)
    append_jsonl(os.path.join(DB, "candidates.jsonl"), row)   # append-only; latest row wins on read


def latest_status(cid):
    st = None
    for row in _load_jsonl(os.path.join(DB, "candidates.jsonl")):
        if row.get("candidate_id") == cid and "status" in row:
            st = row["status"]
    return st


# ---------------- mechanism fingerprint: dedup by MECHANISM, not by architecture decoration.
def mechanism_fingerprint(cand):
    """Coarse canonical mechanism key: kills synonym loops (same idea, different names/decoration).
    Axes: geometry / locality / frame / MOND carrier / lensing carrier / kinetic structure."""
    fields = cand.get("fields", [])
    coups  = cand.get("couplings", [])
    n_metric = sum(1 for f in fields if f.get("type") == "metric")
    geometry = "bimetric" if n_metric >= 2 else "single_metric"
    locality = ("spatial_nonlocal" if any(cp.get("nonlocal") == "spatial" for cp in coups)
                else ("spacetime_nonlocal" if any(cp.get("nonlocal") == "temporal" for cp in coups)
                      else "local"))
    tl = [f for f in fields if f.get("timelike_background") and f.get("type") in ("vector", "khronon")]
    frame = ("none" if not tl else
             ("propagating" if any(f.get("kinetic") == "standard" for f in tl) else "non_propagating"))
    pf = [cp for cp in coups if cp.get("preferred_frame")]
    screening = ("e^-y" if any(cp.get("screened_by") == "e^-y" for cp in pf)
                 else ("unscreened" if pf else "no_pf"))
    lensing = ("second_metric" if geometry == "bimetric"
               else ("screened_frame_slip" if pf else
                     ("nonlocal_stress" if locality != "local" else "none_declared")))
    kin = tuple(sorted({f.get("kinetic", "none") for f in fields}))
    mond = cand.get("mond_realization", "").strip().lower()
    fp = {"geometry": geometry, "locality": locality, "frame": frame, "screening": screening,
          "lensing_carrier": lensing, "kinetic_structure": kin, "mond_carrier": mond}
    if geometry == "bimetric":     # {metric count, interaction, MOND source, matter metric} axes
        bs = cand.get("bimetric_spec", {}) or {}
        fp.update({"bi_interaction": bs.get("interaction"), "bi_mond_source": bs.get("mond_source"),
                   "bi_matter_metric": bs.get("matter_metric")})
    key = hashlib.sha256(json.dumps(fp, sort_keys=True).encode()).hexdigest()[:12]
    return key, fp


def mechanism_dedup(cand, max_per_fp=2):
    """(status, ref): MECHANISM_OF_KILLED if this fingerprint was killed at a theorem/audit gate;
    MECHANISM_SATURATED if >= max_per_fp candidates with this fingerprint were already registered."""
    key, fp = mechanism_fingerprint(cand)
    kills, count = [], 0
    status_by_cid = {}
    for row in _load_jsonl(os.path.join(DB, "candidates.jsonl")):
        cid = row.get("candidate_id")
        if row.get("mech_fp") == key:
            count += 1
        if cid:
            status_by_cid.setdefault(cid, {}).update(row)
    for cid, row in status_by_cid.items():
        if row.get("mech_fp") == key and row.get("status") in ("KILL",):
            kills.append(cid)
    if kills:
        return "MECHANISM_OF_KILLED", kills[0]
    if count >= max_per_fp:
        return "MECHANISM_SATURATED", key
    return "NEW", key


def battery_guard(new_dead_class_predicate):
    """Guard the eval: a NEW dead-class rule is only admissible if it does NOT exclude any known-viable
    point in the falsification battery. new_dead_class_predicate(point_tags)->bool returns True if the
    rule would kill that point. Returns (ok, offending) -- ok=False means the rule is over-broad."""
    bat = json.load(open(os.path.join(STATE, "FALSIFICATION_BATTERY.json")))
    for kv in bat.get("known_viable_points", []):
        if new_dead_class_predicate(set(kv.get("fits", []))):
            return False, kv.get("what")
    return True, None
