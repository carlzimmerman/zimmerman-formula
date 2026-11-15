#!/usr/bin/env python3
"""DP8 launcher for the seed-mean NSS-off sweep on the release-day path (criteria FROZEN_CRITERIA.md, 4caa8bc91f). NEW CODE.

Owner decision 2026-11-15b Q1 / Q2 (prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-15b_DR4_OPEN_GAPS.md): the filed seed-mean
entry of OWNER_DECISION_2026-11-05c (filed 2026-11-08) is computed on release day by DP7's sweep, K = 50, cones-literal, with
the rung's uncovered pairs on the extract fallback. DP7's `dp7_seed_mean.py` (imported here READ-ONLY, unchanged) installs a
socket guard at import and its main() refuses --allow-network, so its DR4 command cannot run as written. This launcher:
  * DR3 (no --allow-network): passes every argument through to dp7_seed_mean.main() unchanged; outputs go to --out-dir.
  * DR4: only with --release dr4 --allow-network and --owner-go-recorded "GO G11S ..." (the approval-file line); then it
    removes DP7's refusal (the --allow-network flag is consumed here, DP7's driver init and DP1's rung_build are called with
    allow_network = True) and restores the socket functions saved before any import. Anything else on DR4 exits 2.
  * Outputs: DP7's module globals HERE / PARTS / WORK are pointed at --out-dir, so <out>.json, <out>.out, parts/ and work/
    land there (never in DP7's folder). A sidecar <out>.dp8.json records the launcher's own facts.
Run on release day under dp6_with_a17.py (A17 cut 12, runbook O8), as the wrapper's step G11S does:
  dp6_with_a17.py --a17-manifest M -- dp8_seed_mean_release.py --release dr4 --manifest M --neighbours-manifest NM
      --cut13 cones-literal --fit-path pipeline --K 50 --rung-missing-cones extract-fallback --allow-network --out dp7_dr4
      --out-dir <OUT>/G11S_seed_mean --owner-go-recorded "<GO G11S line>"
The DR4 network path is untested (no network, no DR4 byte before release). DR3 numbers are code-path tests, never results.
kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.
"""
import socket
_SOCK = {n: getattr(socket.socket, n) for n in ("connect", "connect_ex")}
_SOCKMOD = {n: getattr(socket, n) for n in ("create_connection", "getaddrinfo")}
import sys
sys.dont_write_bytecode = True
import json, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DP7 = REPO / "dr4_push_2026_11_05" / "DP7_seed_mean_check"


def refuse(msg):
    print("DP8 launcher REFUSED: " + msg, flush=True)
    sys.exit(2)


def split_args(argv):
    """own options (--out-dir, --owner-go-recorded) and the rest, which is DP7's argument list; --allow-network is consumed here."""
    own, rest, i = {"out_dir": None, "go": None}, [], 0
    allow = False
    while i < len(argv):
        x = argv[i]
        if x in ("--out-dir", "--owner-go-recorded"):
            if i + 1 >= len(argv):
                refuse(f"{x} needs a value")
            own["out_dir" if x == "--out-dir" else "go"] = argv[i + 1]; i += 2; continue
        if x.startswith("--out-dir="):
            own["out_dir"] = x.split("=", 1)[1]; i += 1; continue
        if x.startswith("--owner-go-recorded="):
            own["go"] = x.split("=", 1)[1]; i += 1; continue
        if x == "--allow-network":
            allow = True; i += 1; continue
        rest.append(x); i += 1
    rel = "dr3"
    for j, x in enumerate(rest):
        if x == "--release" and j + 1 < len(rest):
            rel = rest[j + 1]
        elif x.startswith("--release="):
            rel = x.split("=", 1)[1]
    return own, rest, allow, rel


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    own, rest, allow, rel = split_args(argv)
    if not own["out_dir"]:
        refuse("--out-dir is required (DP7's own folder is never written)")
    go = (own["go"] or "").strip()
    if allow and rel != "dr4":
        refuse("--allow-network is for --release dr4 only (DR3 runs offline)")
    if rel == "dr4" and not allow:
        refuse("--release dr4 needs --allow-network (the sweep's stage-G delta correlation fetches; DP7 RESULT section 7)")
    if rel == "dr4" and not go.startswith("GO G11S"):
        refuse("--release dr4 needs --owner-go-recorded with the approval file's 'GO G11S' line (owner's yes in chat)")
    net = bool(allow and rel == "dr4" and go.startswith("GO G11S"))
    out = Path(own["out_dir"]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(DP7))
    import dp7_seed_mean as S7                                   # READ-ONLY import (installs DP7's socket guard)
    S7.HERE, S7.PARTS, S7.WORK = out, out / "parts", out / "work"
    if net:
        for n, f in _SOCK.items():
            setattr(socket.socket, n, f)
        for n, f in _SOCKMOD.items():
            setattr(socket, n, f)
        _init, _rb = S7.D.init, S7.NR.rung_build

        def init_net(allow_network=False):
            return _init(True)

        def rung_build_net(*a, **k):
            a = list(a)
            if len(a) >= 7:
                a[6] = True
            else:
                k["allow_network"] = True
            return _rb(*a, **k)
        S7.D.init, S7.NR.rung_build = init_net, rung_build_net
    side = dict(launcher="dr4_push_2026_11_05/DP8_release_path_wiring/dp8_seed_mean_release.py", criteria="DP8 FROZEN_CRITERIA.md (4caa8bc91f)",
                decision="OWNER_DECISION_2026-11-05c (filed 2026-11-08); OWNER_DECISION_2026-11-15b Q1, Q2", release=rel, network=("allowed (DR4, GO recorded)" if net else "blocked"),
                owner_go_recorded=(go or None), dp7_argv=rest, out_dir=out.name,
                note="kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.")
    sys.argv = [str(DP7 / "dp7_seed_mean.py")] + rest
    code = 0
    try:
        code = S7.main() or 0
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
        if e.code not in (None, 0) and not isinstance(e.code, int):
            print(str(e.code), flush=True)
    oname = None
    for j, x in enumerate(rest):
        if x == "--out" and j + 1 < len(rest):
            oname = rest[j + 1]
        elif x.startswith("--out="):
            oname = x.split("=", 1)[1]
    side["exit_code"] = code
    if oname:
        (out / f"{oname}.dp8.json").write_text(json.dumps(side, indent=1) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
