#!/usr/bin/env python3
"""Regrade completed CSM1 primitives without fitting or rerunning a scorer."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FEET = ("canonical", "alt")
BACKGROUNDS = ("A_c2b_refit", "B_cfg886_bg")
CLASSES = ("MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    return json.loads(p.read_text())


def close(x, y):
    return math.isclose(x, y, rel_tol=2e-12, abs_tol=2e-12)


def run(args):
    paths = [Path(p).resolve() for p in args.calibration + args.heldout]
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    checks = {}
    sources = {}
    calibration = {}
    heldout = {}
    for kind, names, dest in (("calibration", args.calibration, calibration),
                              ("heldout", args.heldout, heldout)):
        for name in names:
            p = Path(name).resolve()
            data = load(p)
            manifest = load(p.parent / "manifest.json")
            key = str(p.relative_to(ROOT))
            checks[key + "|completed"] = manifest["run"]["status"] == "completed"
            checks[key + "|controls"] = all(c.get("pass_", c.get("passed", False)) for c in manifest["checks"])
            checks[key + "|own_checks"] = all(data["checks"].values())
            sources[key] = {"sha256": sha(p), "manifest_sha256": sha(p.parent / "manifest.json")}
            for text_level, cell in data["levels"].items():
                level = float(text_level)
                if level in dest:
                    # The heldout challenge deliberately replays the primary levels.
                    if cell != dest[level]:
                        raise ValueError("Disagreeing duplicate level in authoritative " + kind)
                    checks[key + "|identical_replay|" + repr(level)] = True
                    continue
                dest[level] = cell
    checks["same_levels"] = set(calibration) == set(heldout)
    checks["four_levels"] = len(calibration) == 4
    rows = []
    details = {}
    for level in sorted(calibration):
        c = calibration[level]
        h = heldout[level]
        detail = {}
        for foot in FEET:
            # Use underlying source results rather than the coordinator's grade booleans.
            own = c["own"]["result"][0]["footings"][foot]
            basin = c["basin"]["result"][0]["footings"][foot]
            lens = c["lens"]["result"][foot]["all"]
            pure = c["pure"]["result"][foot]["all"]
            dl = lens["H2H"]["chi2"] - lens["L2H"]["chi2"]
            dh = lens["H2H"]["chi2"] - pure["H2H"]["chi2"]
            lens_pass = dl <= 9 and dh < 0
            ref = c["grade"][foot]
            checks[f"{level!r}|{foot}|lens_arithmetic"] = (
                close(dl, ref["lensing"]["delta_law"]) and close(dh, ref["lensing"]["delta_halo"])
                and lens_pass == ref["lensing"]["pass_"])
            scopes = {}
            for label, src in (("own", own), ("basin", basin)):
                sp = src["sparc"]
                checks[f"{level!r}|{foot}|{label}|two_backgrounds"] = set(sp) == set(BACKGROUNDS)
                sparc = {b: sp[b]["rms"] <= .110 and .50 <= sp[b]["U_median"] <= .80
                         for b in BACKGROUNDS}
                group = src["groups"]
                group_pass = group["tot"] <= .045 and abs(group["Z"]) < 2
                checks[f"{level!r}|{foot}|{label}|group_arithmetic"] = (
                    close(group["Z"], group["mean"] / group["tot"])
                    and group_pass == (group["verdict"] == "CONSISTENT") and group["N"] == 63)
                cells = src["clusters"]["cells"]
                checks[f"{level!r}|{foot}|{label}|cluster_coverage"] = (
                    set(cells) == {"h0672", "h0686"} and all(len(v) == 15 for v in cells.values())
                    and set(cells["h0672"]) == set(cells["h0686"]))
                cluster_z = [z["Z"] for hs in cells.values() for z in hs.values()]
                cluster_pass = all(abs(z) <= 2 for z in cluster_z)
                scopes[label] = dict(sparc=sparc, sparc_pass=all(sparc.values()),
                    sparc_rms={b: sp[b]["rms"] for b in BACKGROUNDS},
                    sparc_U={b: sp[b]["U_median"] for b in BACKGROUNDS},
                    groups_pass=group_pass, group_Z=group["Z"], group_tot=group["tot"],
                    clusters_pass=cluster_pass, cluster_maxabsZ=max(map(abs, cluster_z)),
                    calibration_pass=all(sparc.values()) and group_pass and cluster_pass and lens_pass)
                checks[f"{level!r}|{foot}|{label}|source_grade"] = (
                    all(sparc[b] == bool(sp[b]["line"]) for b in BACKGROUNDS)
                    and group_pass == group["PASS"] and cluster_pass == (not src["clusters"]["fails"])
                    and scopes[label]["calibration_pass"] == (not ref[label]["fails"]))
            dwarf = h["dwarfs"]["footings"][foot]
            classes = dwarf["classes"]
            checks[f"{level!r}|{foot}|five_classes"] = set(classes) == set(CLASSES)
            dwarf_pass = {name: abs(classes[name]["Z"]) < 2 for name in CLASSES}
            checks[f"{level!r}|{foot}|dwarf_arithmetic"] = all(
                close(v["Z"], v["median"] / v["sd"]) and dwarf_pass[k] == bool(v["reproduced"])
                for k, v in classes.items())
            mw = {}
            for bg in BACKGROUNDS:
                box = h["mw"]["box"][foot + "|" + bg]
                cells = [cell["rows"][foot + "|" + bg] for cell in h["mw"]["cells"]]
                count_vk = box["counts"]["L1&L2a&L2b"]
                mc = h["mw"]["mcmillan"]["rows"][foot + "|" + bg]
                mw[bg] = dict(VK_count=count_vk, VK_pass=count_vk > 0, classification=box["cls"],
                    all_four_count=box["counts"]["all"], McMillan_Vc=mc["vc_R0"],
                    McMillan_K=mc["K_R0"], McMillan_lines={k: mc[k] for k in ("L1", "L2a", "L2b", "L3")})
                checks[f"{level!r}|{foot}|{bg}|mw_cells"] = len(cells) == 175
                nvk = sum(all(row[k] for k in ("L1", "L2a", "L2b")) for row in cells)
                nall = sum(all(row[k] for k in ("L1", "L2a", "L2b", "L3")) for row in cells)
                checks[f"{level!r}|{foot}|{bg}|mw_arithmetic"] = nvk == count_vk and nall == box["counts"]["all"]
            detail[foot] = dict(scopes=scopes, lens=dict(delta_law=dl, delta_pure=dh, pass_=lens_pass,
                law_chi2=lens["L2H"]["chi2"], corrected_chi2=lens["H2H"]["chi2"], pure_chi2=pure["H2H"]["chi2"]),
                dwarfs=dict(class_pass=dwarf_pass, class_Z={k: v["Z"] for k, v in classes.items()},
                    isolated=dwarf["isolated"], satellites=dwarf["satellites"], IC1613=dwarf["flags"]["IC 1613"]),
                mw=mw)
            s = scopes["basin"]
            rows.append(dict(L=level, footing=foot, SPARC=s["sparc_pass"], groups=s["groups_pass"],
                group_Z=s["group_Z"], clusters=s["clusters_pass"], lensing=lens_pass,
                lens_delta_law=dl, lens_delta_pure=dh, calibration=s["calibration_pass"],
                dwarf_classes=all(dwarf_pass.values()), MW_A_VK=mw[BACKGROUNDS[0]]["VK_count"],
                MW_A_all_four=mw[BACKGROUNDS[0]]["all_four_count"], field_S3=dwarf["isolated"]["ok"]["S3"]))
        details[repr(level)] = detail
    checks["inputs_stable"] = all(sha(ROOT / p) == h for p, h in hashes.items())
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    result = dict(scope="Finite four-level regrade; no universal exclusion of canonical L", checks=checks,
                  sources=sources, rows=rows, details=details)
    (out / "results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (out / "checks.json").write_text(json.dumps([dict(name=k, pass_=v) for k, v in checks.items()], indent=2) + "\n")
    with (out / "scores.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(dict(checks=len(checks), failed=[k for k, v in checks.items() if not v], rows=rows), indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--calibration", action="append", required=True)
    p.add_argument("--heldout", action="append", required=True)
    p.add_argument("--output", required=True)
    raise SystemExit(run(p.parse_args()))
