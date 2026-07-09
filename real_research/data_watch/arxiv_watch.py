#!/usr/bin/env python3
"""
arxiv_watch.py — daily arXiv scan for results bearing on the Zimmerman Theory of Gravity.

Stdlib only (urllib + xml.etree). No ai_slop dependency. This script ONLY fetches and
dedupes candidate papers; the VALIDATE/INVALIDATE assessment is done by Claude following
real_research/data_watch/ROUTINE.md.

It queries astro-ph.GA / astro-ph.CO / gr-qc for the framework's watch terms, keeps papers
submitted in the last N days, removes any already in seen.json, prints the new candidates
(Markdown by default, --json for machine output), and marks them seen.

Usage:
  python arxiv_watch.py                # last 2 days, mark seen, Markdown
  python arxiv_watch.py --days 7       # wider window (use once at setup to seed seen.json)
  python arxiv_watch.py --json         # JSON for programmatic use
  python arxiv_watch.py --no-mark      # dry run: do not update seen.json
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SEEN = os.path.join(HERE, "seen.json")
API = "https://export.arxiv.org/api/query"  # https: arXiv 301-redirects http now
CATS = ["astro-ph.GA", "astro-ph.CO", "gr-qc"]
# arXiv rejects an over-complex query (all terms OR'd at once) with HTTP 503, so
# fetch() splits the term list into chunks of this size and merges the results.
CHUNK = 5

# Watch terms — phrases bearing on the framework's pre-registered predictions (ROUTINE.md).
TERMS = [
    "radial acceleration relation", "baryonic Tully-Fisher", "Tully-Fisher relation",
    "MOND", "modified Newtonian dynamics", "modified inertia", "deep-MOND",
    "MOND acceleration scale", "external field effect", "emergent gravity",
    "wide binaries", "wide binary test", "MUSE-DARK", "dark energy equation of state",
    "w0waCDM", "evolving dark energy", "high-redshift rotation curves",
    # WATCHLIST entries 5-6: relativistic-MOND theory + the high-z / a0(z) telescopes
    "aether scalar tensor", "AeST", "Skordis", "relativistic MOND", "TeVeS",
    "weak lensing radial acceleration", "DESI DR3", "ELT HARMONI",
    "JWST rotation curve", "ALMA high-redshift kinematics", "galaxy cluster MOND residual",
]

# ── Attribution / priority scan (ROUTINE.md step 2c) ────────────────────────────
# FINGERPRINT_TERMS widen the arXiv full-text query with Carl's OWN distinctive
# coinages, so a paper reproducing his reframing surfaces even if it avoids the
# generic MOND vocabulary above. FINGERPRINTS then scans each fetched title+abstract
# for high-precision Carl-unique strings (exact coefficients / exact symbolic combos /
# his coined phrases) and FLAGs any hit for a human to check against his DOIs.
# Precision over recall by design: generic physics terms are deliberately excluded so
# ordinary MOND papers don't trip the flag. Provenance: enumerate-novel-reframings
# workflow over real_research/ (papers, NOVELTY.md, MASTER_PREDICTIONS.md, memory).
FINGERPRINT_TERMS = [
    "de Sitter-Unruh modified inertia", "Deser-Levin temperature inertia",
    "cosmic free-fall density surface gravity", "horizon acceleration scale square root Lambda",
    "inverted black hole duality", "non-monotonic acceleration scale",
    "acceleration scale dark energy density", "boost dipole CMB apex",
    "Machian relational inertia", "sigma hysteresis dwarf galaxy",
    "first-infall sign flip", "orbital history dispersion",
    "passive bath anti-MOND", "population-inverted bath",
    "Ostrogradsky ghost modified inertia", "flat-curve exceptional point",
    "Big Wheel rotation curve", "CKN bound cosmic seesaw",
    "trichotomy covariant modified inertia", "dark-energy free-fall frequency",
    "thawing dark energy event horizon", "modified inertia trilemma",
]

# Each fingerprint = (label, [patterns]). A pattern is either a string (substring match,
# case-insensitive, on title+abstract) or a list of strings (an AND-group: all must be
# present). A hit on ANY pattern flags the paper. Patterns are exact numeric coefficients,
# exact symbolic combinations, or Carl-coined phrases — NOT generic terms. AND-groups let a
# generic word (e.g. "swampland", "ostrogradsky", "growing neutrino") fingerprint Carl only
# when it co-occurs with his acceleration-scale context, so ordinary papers don't trip.
FINGERPRINTS = [
    ("a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 (horizon coefficient)",
     ["9.36e-11", "9.36 × 10⁻¹¹", "9.355e-11", "c^2 sqrt(lambda/32", "c²√(λ/32π)",
      "c^2√(λ/32", "sqrt(lambda/32pi)", "lambda/32pi", "λ/32π"]),
    ("a0 = cH_Lambda/Z, Z = sqrt(32pi/3) = 5.789 (Z-normalization)",
     ["ch_lambda/z", "ch_λ/z", "z = sqrt(32pi/3)", "√(32π/3)", "sqrt(32*pi/3)",
      "z^2 = 32pi/3", "z² = 32π/3", "z = 5.789", "5.7888", "5.78881",
      "2 sqrt(8pi/3)", "2√(8π/3)"]),
    ("dS-Unruh interpolation g_obs = sqrt(g_bar^2 + g_bar*a0)",
     ["g_bar^2 + g_bar", "g_bar² + g_bar", "sqrt(g_bar^2 + g_bar", "√(g_bar² + g_bar",
      "de sitter-unruh interpolation", "ds-unruh interpolation"]),
    ("Deser-Levin dS-Unruh floor T0 = 2.20e-30 K (excess-above-floor inertia)",
     ["deser-levin", "deser–levin", "2.20e-30", "2.20 × 10⁻³⁰", "2.2e-30 k",
      "excess above the floor", "half-machian", "a^2 + (ch_lambda)^2", "a² + (ch_λ)²",
      "sqrt(a^2 + (ch"]),
    ("mu_fw interpolation, tanh-asinh identity, 1/phi at a0",
     ["mu_fw", "μ_fw", "(sqrt(1+4x^2)-1)/2x", "(√(1+4x²)−1)/2x", "mu/(1-mu^2) = a/a0",
      "μ/(1−μ²) = a/a₀", "tanh(½ asinh(2x))", "tanh(0.5 asinh(2x))", "μ_fw(1) = 1/φ"]),
    ("non-monotonic a0(z) bump at phantom-crossing z~0.4",
     ["non-monotonic a₀(z)", "non-monotonic a0(z)", "bump in a₀",
      ["bump", "a₀(z)"], ["bump", "a0(z)"], ["phantom cross", "a0(z)"],
      ["phantom cross", "acceleration scale"]]),
    ("a0(z) proportional sqrt(rho_DE) declining; rho_DE-vs-rho_total fork",
     ["a₀(z) = a₀·√(ρ_de", "a0(z) = a0 sqrt(rho_de", "a₀ ∝ √ρ_de",
      "a0 proportional sqrt(rho_de)", "sqrt(rho_de(z)/rho_de(0))", "√(ρ_de(z)/ρ_de(0))",
      "√ρ_de vs √ρ_total", "sqrt(rho_de) vs sqrt(rho_total)", "a₀(z=3) ≈ 0.74",
      "0.74 a0(0)", "0.737 at z=3", "limbach–psaltis–özel", "lpo relation"]),
    ("H_RISE / H_CONST / H_DECL three-branch a0(z) labels",
     ["h_rise", "h_const", "h_decl", "a0_loc · e(z)", "declining branch √ρ_de"]),
    ("Big Wheel z=3.25 clean deep-MOND high-z a0(z) probe",
     ["big wheel", "a0_eff", "a₀_eff"]),
    ("inverted black hole duality: a0_BH = c^4/(4GMZ), r_cross = 2.406 r_s",
     ["inverted black hole", "a0_bh = c^4/(4gmz)", "a₀_bh = c⁴/(4gmz)", "c⁴/(4gmz)",
      "c^4/(4gmz)", "c^4/(4*g*m*z)", "r_cross = √z", "r_cross = sqrt(z)", "2.406 r_s",
      "x_isco = z/9", "z/9 = 0.643"]),
    ("exactly-GR null for BH strong-field (MI vs metric-shifting rivals)",
     ["exactly-gr null", "exactly gr null", "no a0_bh correction", "no a₀_bh correction"]),
    ("s^TX boost dipole locked to CMB apex, |A| ~ 8.7e-10",
     ["s^tx", "s̄^tx", "s̄^{tx}", "s^{tx}", "264.02", "48.25", "167.94",
      "8.7×10⁻¹⁰", "8.7e-10", "8.68e-10", "s̄^{ty}/s̄^{tx}"]),
    ("universal-vs-per-body reading fork in SME ephemeris test",
     ["universal vs per-body", "s_bar proportional a0/2g", "s̄ ∝ a₀/2g",
      "(a0/2|a|)*beta_cmb", "30–1000× below", "30-1000x below"]),
    ("CKN UV-IR cosmic seesaw welding a0 & Lambda; 2.24 meV vacuum",
     ["2.24 mev", "e_λ = √((2/z)", "geometric mean of planck and hubble",
      ["cosmic seesaw", "acceleration scale"], ["cosmic seesaw", "a0"],
      ["ckn", "acceleration scale"], ["uv-ir", "a0"], ["uv-ir", "acceleration scale"]]),
    ("kappa = 1/2 as the one free number (kappa-closure)",
     ["κ = ½", "kappa = 1/2", "κ = 1/2", "one free number", "κ-closure", "kappa-closure"]),
    ("memory kernel theta0 = sqrt(2), Lorentzian, tau = 0.45 Gyr",
     ["θ(0) = √2", "theta0 = sqrt(2)", "θ₀ = √2", "τ = 0.45 gyr", "0.45 gyr",
      "θ(y) = θ₀/(1 + (θ₀−1)y²)", "amplitude-branch selection", "θ₀ ∈ [√2, 2]"]),
    ("relational/Machian MOND-sign selection (excess above floor)",
     ["half-machian", "relational/machian", "dynamical inertia = excess",
      "r(u) = (√(1+u²)−1)/u", "conditional on the machian premise"]),
    ("passivity/state-clause sign theorem; population-inversion flip",
     ["passivity forces anti-mond", "no pump-free mond-sign channel", "thermostat theorem",
      "population-inverted", "population inversion flips", "state clause", "δm ≥ 0",
      "δm = 2∫ρ", "spectral emptiness"]),
    ("Ostrogradsky-ghost closure of local covariant MI",
     ["local mi gate", "milgrom 1994 wall", "d²l/d(ẍ)² ≠ 0",
      ["ostrogradsky", "modified inertia"], ["ostrogradsky", "milgrom"]]),
    ("PT frequency law mu_eff = 1 - (Omega/w_eff)^2",
     ["μ_eff = 1 − (ω/w_eff)²", "mu_eff = 1 - (omega/w_eff)^2", "the frequency law",
      "pt-quantized", "w_eff² = w²/k'", "selected by frequency, never by acceleration"]),
    ("gas-clamp / inverted-line closure (Theorem V)",
     ["gas clamp", "gas-clamp", "super-threshold amplifier", "inverted spectral line",
      "laser-like amplification", "ν₂ ∈ [1.1×10⁶", "1.1e6 h0", "9.9e7 h0",
      "γ = 3h₀", "gamma = 3h0"]),
    ("flat-curve exceptional-point band (0.7579886, 0.8947874), fold law",
     ["0.7579886", "0.8947874", "flat-curve band", "pt-broken band",
      "μ_fold = 1 − 1/(2p)", "mu_fold = 1 - 1/(2p)", "fold law", "664μ⁴−3036μ³"]),
    ("convex ghost-free Landau potential for mu_fw",
     ["φ(μ; x) = μ²/2", "phi(mu; x) = mu^2/2", "x·μ³/3", "x*mu^3/3",
      "convex, ghost-free potential", "convex ghost-free"]),
    ("first-infall sign flip / dwarf sigma hysteresis (MG-impossible)",
     ["first-infall sign flip", "first infall sign flip", "pre-pericentre deficit",
      "post-pericentre excess", "deficit-then-excess", "sigma hysteresis", "σ hysteresis",
      "double-valued sigma", "orbital-history dispersion", "modified-gravity-impossible dwarf"]),
    ("cluster anisotropy eta sliding with beta (MG-impossible)",
     ["η slides", "eta slides with", "d ln η/dβ", "d ln eta/d beta",
      "g m a0 = eta sigma^4", "gma₀ = ησ⁴", "pericentre-dominated milgrom"]),
    ("trichotomy of covariant MI completion routes",
     ["sharpened trichotomy", "three horns blocked", "route-e", "slip⇔φ bianchi",
      "bianchi lock", "trichotomy of covariant"]),
    ("number-field obstruction: Z in Q(sqrt(pi))",
     ["number-field obstruction", "number field obstruction", "q(√π)", "q(sqrt(pi))",
      "z ∈ q(√π)", "z carries √π"]),
    ("Z dimensional encoding Z_d = 8 sqrt(pi/[d(d-1)]) (holographic 3-ball)",
     ["z_d = 8√(π", "z_d = 8 sqrt(pi", "8√(π/[d(d−1)])", "8 sqrt(pi/[d(d-1)])",
      "d(d−1) = 64π", "z² = 32π/3 = 8", "unit 3-ball volume", "reads back d ≈ 3"]),
    ("swampland-compatible evolving DE vs static-Lambda dS violation",
     ["evolving a0(z)", "|∇v|/v ≥ c/m_p", "w < −1 for z > 0.4",
      ["swampland", "a0(z)"], ["swampland", "acceleration scale"],
      ["static λ violates", "swampland"]]),
    ("growing neutrino mass locked to a0(z)",
     ["locked to a0(z)", ["growing neutrino", "a0(z)"], ["growing neutrino", "acceleration scale"],
      ["m_ν(z)", "acceleration scale"], ["m_nu(z)", "a0(z)"]]),
    ("high-z BTFR offset sign (coeff 1/8, negative) + evolving EFE",
     ["high-z btfr", "dlogv = 1/8", "−7.3% in v", "discs below the z=0 relation",
      "η ∝ 1/e(z)", "e_n(z) = g_ext/a0(z)", "redshift-weakening external field"]),
    ("dark-energy free-fall frequency (three-reading uniqueness fork)",
     ["dark-energy free-fall frequency", "free-fall frequency of the dark",
      "three-reading", "reading #1"]),
    ("thawing DE -> no future event horizon under DESI CPL",
     ["no future event horizon", "thawing dark energy", "thaws away", "rho_de thaws"]),
    ("matter-chord kernel diagonal transport (not conversion)",
     ["matter-chord operator", "matter-chord kernel", "diagonal chord",
      "diagonal-dominant kernel", "transports the source"]),
    ("modified-inertia trilemma (Cassini-safe + a0(z)-natural + CMB-safe)",
     ["modified inertia trilemma", "trilemma of covariant",
      ["cassini-safe", "cmb-safe"]]),
    ("spectral center-vs-near-edge (Narovlansky-Verlinde / Okuyama fork)",
     ["center-vs-edge identification", "spectral center vs near-edge",
      ["narovlansky", "mond"], ["narovlansky", "a0"], ["okuyama", "mond"]]),
]

# Substrings that indicate a paper likely CREDITS Carl (annotation only — never auto-clears).
ZIMMERMAN_MARKERS = ["zimmerman", "zenodo.20576485", "10.5281/zenodo.2057",
                     "10.5281/zenodo.209", "10.5281/zenodo.211"]

ATOM = "{http://www.w3.org/2005/Atom}"


def _pattern_hit(pat, low):
    """A pattern hits if it's a substring present in `low`, or an AND-group
    (list/tuple) whose every substring is present."""
    if isinstance(pat, (list, tuple)):
        return all(s.lower() in low for s in pat)
    return pat.lower() in low


def scan_fingerprints(text):
    """Return the labels of every Carl-distinctive fingerprint present in text."""
    low = text.lower()
    return [label for label, pats in FINGERPRINTS if any(_pattern_hit(p, low) for p in pats)]


def build_query(terms):
    cat = " OR ".join(f"cat:{c}" for c in CATS)
    term_q = " OR ".join(f'all:"{t}"' for t in terms)
    return f"({cat}) AND ({term_q})"


def fetch_chunk(terms, max_results, retries=3):
    params = {"search_query": build_query(terms), "sortBy": "submittedDate",
              "sortOrder": "descending", "start": 0, "max_results": max_results}
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "zimmerman-data-watch/1.0"})
    last = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as ex:
            last = ex
            time.sleep(4 * (attempt + 1))
    raise last


def fetch(max_results):
    """Fetch all watch terms in chunks (arXiv 503s on the full query) and merge,
    deduping by arXiv id. Returns parsed entries (newest first)."""
    by_id = {}
    all_terms = TERMS + FINGERPRINT_TERMS
    chunks = [all_terms[i:i + CHUNK] for i in range(0, len(all_terms), CHUNK)]
    # Cap per-chunk results so the sum stays comparable to the old single-query budget.
    per_chunk = min(max_results, 60)
    for i, ch in enumerate(chunks):
        for e in parse(fetch_chunk(ch, per_chunk)):
            by_id[e["id"]] = e
        if i + 1 < len(chunks):
            time.sleep(3)  # be polite to the arXiv API between requests
    entries = sorted(by_id.values(), key=lambda e: e["published"], reverse=True)
    return entries


def parse(xml_bytes):
    root = ET.fromstring(xml_bytes)
    out = []
    for e in root.findall(ATOM + "entry"):
        idurl = (e.findtext(ATOM + "id", "") or "").strip()
        arxid = idurl.rsplit("/abs/", 1)[-1] if "/abs/" in idurl else idurl.rsplit("/", 1)[-1]
        out.append({
            "id": arxid,
            "title": " ".join((e.findtext(ATOM + "title", "") or "").split()),
            "authors": [a.findtext(ATOM + "name", "") for a in e.findall(ATOM + "author")],
            "abstract": " ".join((e.findtext(ATOM + "summary", "") or "").split()),
            "published": (e.findtext(ATOM + "published", "") or "")[:10],
            "link": idurl,
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=2)
    ap.add_argument("--max", type=int, default=200)
    ap.add_argument("--no-mark", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    seen = set()
    if os.path.exists(SEEN):
        try:
            seen = set(json.load(open(SEEN)))
        except Exception:
            seen = set()

    try:
        entries = fetch(args.max)
    except Exception as ex:
        print(f"ERROR fetching/parsing arXiv: {ex}", file=sys.stderr)
        sys.exit(2)

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    new = []
    for e in entries:
        if e["id"] in seen:
            continue
        try:
            pub = datetime.fromisoformat(e["published"] + "T00:00:00+00:00")
        except Exception:
            pub = None
        if pub is not None and pub < cutoff:
            continue
        new.append(e)

    # Attribution / priority scan: tag each candidate with Carl-distinctive fingerprints.
    for e in new:
        e["fingerprint_hits"] = scan_fingerprints(e["title"] + " " + e["abstract"])
        low = (e["title"] + " " + e["abstract"]).lower()
        e["mentions_zimmerman"] = any(m in low for m in ZIMMERMAN_MARKERS)

    if not args.no_mark and new:
        seen |= {e["id"] for e in new}
        json.dump(sorted(seen), open(SEEN, "w"), indent=0)

    if args.json:
        print(json.dumps(new, indent=2))
        return

    today = datetime.now(timezone.utc).date()
    print(f"# arXiv data-watch — {len(new)} new candidate(s), last {args.days}d ({today})\n")
    if not new:
        print("_No new candidate papers._")
        return

    flagged = [e for e in new if e["fingerprint_hits"]]
    if flagged:
        print(f"## ⚑ ATTRIBUTION FLAGS — {len(flagged)} candidate(s) reproduce a Carl-distinctive fingerprint\n")
        print("_Title+abstract match on a Carl-unique string; NOT proof of a scoop. "
              "Verify whether each cites his Zenodo DOIs (10.5281/zenodo.20576485 et al.)._\n")
        for e in flagged:
            cite = ("mentions 'Zimmerman' — likely cites, verify" if e["mentions_zimmerman"]
                    else "no 'Zimmerman' in abstract — verify citation in the PDF")
            print(f"- **{e['id']}** · {e['title']}")
            print(f"  - fingerprint: {'; '.join(e['fingerprint_hits'])}")
            print(f"  - {cite} · {e['link']}\n")
        print("---\n")

    for e in new:
        au = ", ".join(e["authors"][:4]) + (" et al." if len(e["authors"]) > 4 else "")
        print(f"## {e['title']}")
        print(f"- **{e['id']}** · {au} · {e['published']} · {e['link']}\n")
        print(f"{e['abstract'][:900]}\n")


if __name__ == "__main__":
    main()
