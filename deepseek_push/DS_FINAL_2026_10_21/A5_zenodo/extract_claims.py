#!/usr/bin/env python3
"""Sentence-level claim extraction from the cached Zenodo records.

Produces _zenodo/extract.json: for every record, the sentences of its abstract
that contain (i) a number and (ii) a keyword from one of the five lanes
(a) kappa/a0 origin, (b) medium/saturation/n, (c) lensing/GW/PPN/stability,
(d) 24 pc .. 1 kpc length scales, (e) predictions/kill conditions.

Sentence splitting is deliberately dumb (period/; boundaries) so that quotes
stay verbatim: we never rewrite the abstract, we only select substrings.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_zenodo")

NUM = re.compile(
    r"(?<![\w.])[-+]?(?:\d+(?:\.\d+)?(?:[eE][-+]?\d+)?|\.\d+)"
    r"(?:\s*(?:×|x)\s*10\^?\{?[-+]?\d+\}?)?"
)

CATS = {
    "a_kappa_a0": [
        "kappa", "κ", "a0", "a_0", "acceleration scale", "cH", "c H",
        "dark-energy density", "rho_Lambda", "ρ_Λ", "Lambda/32", "Λ/32",
        "coefficient", "normalisation", "normalization", "one-half", "1/2",
        "Z =", "Z=", "5.788", "0.1727", "9.36", "1.13e-10", "1.2e-10",
        "vacuum energy", "de Sitter", "Unruh",
    ],
    "b_medium_saturation": [
        "medium", "saturat", "n = 1", "n=1", "n = 2", "n=2", "capacity",
        "dielectric", "polariz", "polaris", "cold energy", "cold-energy",
        "condensate", "superfluid", "elastic", "solid", "tethered", "displacement",
        "two-level", "Born-Infeld", "stiffness", "bulk modulus", "sound speed",
        "equation of state", "interpolation", "quadrature", "kernel", "memory",
        "nonlocal", "non-local", "retarded",
    ],
    "c_lensing_gw_ppn": [
        "lensing", "GW", "gravitational wave", "speed of light", "c_T", "ct",
        "PPN", "gamma", "γ", "Cassini", "Shapiro", "stability", "ghost",
        "gradient instability", "tachyon", "Laplacian", "Jeans", "sound horizon",
        "screening", "Vainshtein", "disformal", "conformal", "no-slip",
        "frame", "Lorentz", "preferred frame", "ephemeris", "perihelion",
    ],
    "d_length_scale": [
        "pc", "kpc", "Mpc", "parsec", "24 pc", "kiloparsec", "length scale",
        "radius", "core radius", "scale radius", "wavelength", " mm", "cm",
        "eV", "Hz", "GHz", "THz", "micron", "μm", "nm", "AU", "solar radius",
        "R =", "R=", "r_c", "r0", "km",
    ],
    "e_prediction_kill": [
        "predict", "falsif", "kill", "test", "pre-registered", "preregistered",
        "forecast", "no-go", "no go", "excluded", "excludes", "rules out",
        "detect", "signature", "discrimin", "confirm", "refute", "bound",
        "upper limit", "sigma", "σ", "χ2", "chi2", "Δχ", "tension", "ppm",
        "false", "fails", "survive", "passes",
    ],
}

SENT_SPLIT = re.compile(r"(?<=[.;])\s+(?=[A-Z(])")


def sentences(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    parts = SENT_SPLIT.split(text)
    out = []
    for p in parts:
        p = p.strip()
        if p:
            out.append(p)
    return out


def cats_for(s):
    low = s.lower()
    return [c for c, kws in CATS.items() if any(k.lower() in low for k in kws)]


def main():
    recs = json.load(open(os.path.join(CACHE, "all_records.json")))
    out = []
    for r in recs:
        sents = sentences(r["description"])
        picked = []
        for s in sents:
            c = cats_for(s)
            if not c:
                continue
            has_num = bool(NUM.search(s))
            picked.append({"text": s, "cats": c, "has_number": has_num})
        nums = sorted(set(m.group(0) for m in NUM.finditer(
            re.sub(r"<[^>]+>", " ", r["description"]))))
        out.append({
            "id": r["id"], "doi": r["doi"], "date": r["date"],
            "title": r["title"], "n_sent": len(sents),
            "n_picked": len(picked), "sentences": picked,
            "numbers": nums,
            "desc_chars": len(r["description"]),
        })
    with open(os.path.join(CACHE, "extract.json"), "w") as f:
        json.dump(out, f, indent=1)
    tot = sum(o["n_picked"] for o in out)
    print(f"records={len(out)} picked_sentences={tot}")
    for o in out[:3]:
        print(o["id"], o["n_picked"], len(o["numbers"]))


if __name__ == "__main__":
    main()
