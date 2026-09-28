#!/usr/bin/env python3
"""One-time bootstrap: execution dirs, durable campaign ledger, wave-0 claim reservations.
Read-only wrt task files; creates claims/ results/ reviews/ branches/ and CAMPAIGN_LEDGER.json.
"""
import json, hashlib, os, sys, datetime

CAT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(CAT, "manifest.json")
LEDGER = os.path.join(CAT, "CAMPAIGN_LEDGER.json")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

m = json.load(open(MANIFEST))
tasks = m["tasks"]
assert len(tasks) == 2000, len(tasks)

# 1. execution dirs
for d in ("claims", "results", "reviews", "branches"):
    os.makedirs(os.path.join(CAT, d), exist_ok=True)

# 2. ledger: one row per seed
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
if os.path.exists(LEDGER):
    ledger = json.load(open(LEDGER))
else:
    ledger = {"schema_version": 1, "created_utc": now, "updated_utc": now,
              "wave": 0, "rows": {}}
rows = ledger["rows"]
for t in tasks:
    tid = t["id"]
    fname = next((f for f in os.listdir(CAT) if f.startswith(tid + "_")), None)
    rows.setdefault(tid, {
        "id": tid, "group": t["group"], "title": t["title"],
        "priority": t.get("priority", ""),
        "deps": t.get("prerequisites", []),
        "file": fname,
        "file_sha256": sha256(os.path.join(CAT, fname)) if fname else None,
        "state": "pending",          # pending|claimed|running|completed|failed|blocked|reused
        "owner": None, "worker": None, "claim": None,
        "result_dir": None, "run_id": None,
        "outcome": None, "review_status": "unreviewed",
        "evidence": [], "next_action": "wave0 queue",
    })
json.dump(ledger, open(LEDGER, "w"), indent=1, sort_keys=True)

# 3. claims for wave 0 sub-wave A: AS001..AS020 (P0 unit/scale audits, all independent)
claimed = []
for i in range(1, 21):
    tid = f"AS{i:03d}"
    r = rows[tid]
    claim_path = os.path.join(CAT, "claims", f"{tid}.json")
    if os.path.exists(claim_path):
        continue
    claim = {
        "task_id": tid, "task_sha256": r["file_sha256"],
        "owner": "hermes-orchestrator", "worker": None,
        "reserved_utc": now, "state": "reserved",
        "result_base": f"results/{tid}/", "run_id": None,
    }
    with open(claim_path, "x") as f:   # exclusive creation
        json.dump(claim, f, indent=1)
    r["state"] = "claimed"; r["owner"] = "hermes-orchestrator"; r["claim"] = claim_path
    claimed.append(tid)

ledger["updated_utc"] = now
json.dump(ledger, open(LEDGER, "w"), indent=1, sort_keys=True)
print(f"ledger rows: {len(rows)}; claimed wave0-A: {claimed}")