#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR10 -- THE ANSWER VALIDATOR: is every row the answer calls an M* result actually run on M*?

WHY.  The final answer (ANSWER_AS_IT_STANDS.md) is assembled from lanes run by parallel sessions.  On 2026-09-26 alone
results were silently mixed across settings five times: switch cells (L381), switch branches (L388 vs DE2), cap forms
(L395's local form vs MS5's kappa form), force operators (PM vs action vs merger) and epochs (retention at z = 0 used at
z = 0.4 or 0.5).  Docstrings and README rows drifted from the code each time.  This gate reads the CODE.

WHAT IT DOES.  XR10_answer_rows.json holds one row per result that bears on the target model M*.  Every axis of every
row carries a trace: a file, a regular expression that finds the defining line, and a derivation (a signature table
classifies the line, or numbers are parsed from it).  The validator re-derives each axis from the source -- the
committed version (git show HEAD:) for committed lanes, the working tree for uncommitted ones -- and compares:
  (D) the registry against the source: a registered value the code no longer supports is DRIFT;
  (M) the derived value against M* (the parameter block MSTAR below): MATCH, COMPAT (a committed lane has shown the
      difference is controlled for this row's gates, the rule is enabled, and the row's scope states it), MISMATCH,
      or N/A (the axis does not enter the row);
and prints a per-row table.  Nothing is imported from or executed in the lanes; results are read only from committed
JSON / .out files.

RC = 1 IF ANY OF:
  D   drift on a committed row (the code no longer says what the registry says, or a trace is lost);
  M   a row claimed as an M* result ('claim': 'M*') has a MISMATCH on any axis, is not committed, or has a defining axis
      (switch, cap, carrier, p, x_c0, footings) that is asserted rather than derived from the code;
  E   an enabled approximation rule's evidence does not hold in the committed files;
  C1  CONTROL: L395's cell (c) is not flagged from its source (the withdrawn local cap form in the particle-mesh dynamics
      while its shear is scored with the hard 1.75 Mpc radius: a CAP-SPLIT mismatch);
  C2  NEGATIVE CONTROL: a row the rules must pass is flagged (MS5's kappa-form shear on cap form; MS3's hard radius
      on halo-model shear; L396's kappa cap in the dynamics with the hard radius in its shear score);
  C3  CONTROL (the gate can pass): MS5's kappa-form shear row, with the epoch tolerance widened in memory, must pass an
      M* claim -- the claim check is not vacuous.
REPORTED (never rc): drift on pending rows (their sources are live), candidate rules that are not enabled, the rows the
  current scorecard cites that are off M*, the per-lane status table.

MODES.  XR10_SNAPSHOT=1 records what the code says now (commit, verdict, status, each axis's file:line) into the
  registry's 'recorded' fields; later runs report traces that moved (never rc).  MUTATE=1 corrupts one registry axis in memory -- DE10's registered cap form is set to kappa_MS5, hiding its
  withdrawn local form -- and check D must fail (rc = 1).  XR10_SCORECARD=1 treats every row the current scorecard
  cites as claimed M* (the gate as the answer page is written today).  M* overrides, for XR9's scan:
  XR10_P, XR10_XC0, XR10_WMAX, XR10_EPOCH_TOL (or edit MSTAR below).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR10_answer_validator.py
(read-only everywhere; single-threaded; a few seconds)
"""
import json, os, re, subprocess, sys, time, math

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SCORECARD = os.environ.get("XR10_SCORECARD", "0") == "1"
SNAPSHOT = os.environ.get("XR10_SNAPSHOT", "0") == "1"             # write what the code says now into the registry's 'recorded'

P = lambda *a: print(*a, flush=True)

# ======================================================================================================================
# M*: THE TARGET MODEL.  Edit here, or override by environment (XR10_P, XR10_XC0, XR10_WMAX, XR10_EPOCH_TOL).
# ======================================================================================================================
MSTAR = dict(
    switch_reading="mond_sector_constrained",        # CV3's C[lap(u - v) + div((nu - 1) grad S w)]
    switch_equivalent=("mond_sector_phiX",),         # MS1's C lap(Phi - v): same gate value (CV3); recorded, data gates only
    cap_form="kappa_MS5",                            # U_cap = C m(lap Phi_X, v_cap^2 kappa_X^2): regions end at v_cap/(H sqrt x_c)
    p=1.0, x_c0=2.5, w_max=0.25,                     # the vacuum gate x_c,eff(z) = x_c0 E(z)^(2p); smooth width 0 < w <= w_max
    kernel="nu_mono",
    sigma=1.0,                                       # L361's web self-term, as V0 takes it
    operator="A",                                    # the action's region operator (L361, screened)
    carrier="L388_density_trigger", kick_kms=(575.0, 650.0),
    footings=("canonical", "alt"),                   # both, wherever a0 enters
    epoch_dz_tol=0.1,                                # retention must be measured within this of the scoring epoch
)
for _k, _e in (("p", "XR10_P"), ("x_c0", "XR10_XC0"), ("w_max", "XR10_WMAX"), ("epoch_dz_tol", "XR10_EPOCH_TOL")):
    if os.environ.get(_e):
        MSTAR[_k] = float(os.environ[_e])

EFE_GATES = {"efe_cluster_infall", "efe_lv_dwarfs", "coma_udg", "lg_zero_velocity"}
AXES = ("switch_reading", "cap_form", "p", "x_c0", "w", "kernel", "sigma", "operator", "carrier", "kick", "footings", "epoch")
ABBR = {"switch_reading": "switch", "cap_form": "cap", "p": "p", "x_c0": "x_c0", "w": "w", "kernel": "kern", "sigma": "sig",
        "operator": "op", "carrier": "carr", "kick": "kick", "footings": "foot", "epoch": "epoch"}

# ======================================================================================================================
# SIGNATURE TABLES: how a traced code line is classified (the registry's value is never used to classify)
# ======================================================================================================================
SIG = {
    "switch_reading": [
        ("mond_sector_constrained", [r"UgAp = Cg \* \(\(d_\(u, 2\) - d_\(v, 2\)\) \+ phant\)", r"U = C\[lap\(u - v\) \+ div\(\(nu - 1\) grad S w\)\]"]),
        ("mond_sector_phiX", [r"d_\(Phi, 2\) - d_\(v, 2\)", r"PX = Phi - v", r"rho - FB \* rho_bar\) / H_L",
                              r"rho - FB \* D8\[\"rho_bar\"\]", r"sub = 1\.0 if reading == \"curvature\" else FB",
                              r"FB \* delta \+ state\[\"dph\"\]", r"FB if door == \"mond\" else 1\.0", r"xce = 2\.5 \* E2\(z\)",
                              r"the MOND-sector reading x = 4 pi G \(rho_b \+ rho_ph - f_b rho_bar_m\)", r"rho - FB \* rhob\) / H \*\* 2"]),
        ("mond_sector_abs", [r"\(rb \+ dpos\)", r"rb \+ np\.maximum\(dph_all, 0\.0\)", r"FB \* rho_h \+ np\.maximum\(rho_ph, 0\)",
                             r"ON where x >= x_c,eff\(z\) max\(1, v_loc", r"R_of\(XLIN, A0\[f_\], rc_, \"door\"",
                             r"'ms_abs'  r_e = v_f/\(H sqrt\(x_c,eff - 1\.5 Om\(z\) f_b\)\)", r"rho_b \+ max\(rho_ph,all, 0\)\)/rho_bar_m \(absolute"]),
        ("curvature_clipped", [r"\(rho - 1\.0 \+ dpos\)"]),
        ("curvature_signed", [r"\"a_curvature\": C \* d_\(Phi, 2\)", r"build_regions\"\]\(mk, rhoB, XLIN", r"rho_dyn - Om \* rho_crit0", r"rho_dyn = np\.gradient\(M, rr\)", r"rho - 1\.0 \+ delta_ph,all",
                              r"np\.gradient\(Mdyn, rr\) / \(4 \* math\.pi \* rr \*\* 2\) \+ rho_car", r"XE_LIN = round\(XE59",
                              r"XE_COMMON = round\(N60\[\"XE59\"\]", r"fit_comb\(A052\[f_\], XE_LIN", r"R = R\^\(3\) \+ sigma_ij",
                              r"f = F\(R\^\(3\) \+ sigma_ij", r"growing the regions with the phantom|build_regions\(mk, rhoB, XLIN",
                              r"CURVATURE  the gate reads the dynamical", r"f = Theta\(1\.5 Omega_m\(a\) \(rho/rho_bar - 1 \+ delta_ph,all\)"]),
        ("matter_only", [r"\"b_matter\": C \* \(rb \+ rd\)", r"Om_a\(a\) \* \(rho - 1\.0\) \* gate > X_C0", r"1\.5 \* self\.rho / self\.rhoc\) >= x_ceff", r"1\.5 \* rreal / \(RHOC0 \* Ez2\(z\)\)",
                         r"return rm$", r"rho_bar_m\(z\) \* \(\(1 \+ x\) if reading == \"contrast\" else x\)",
                         r"MATTER     the gate reads the matter density", r"def lower_mask\(xc\)"]),
        ("khronon_K", [r"varying tau in -c_2 Int sqrt\(-g\) \(K - <K>\)\^2"]),
        ("none", [r"from L377_full_construction_pm import nu_vec as nu_mono", r"def trig_acc|Gamma = Gamma_0 Theta\(y_b - y_v\)",
                  r"No switch|no switch"]),
    ],
    "cap_form": [
        ("kappa_MS5", [r"VCAP(_CODE)?2 \* kap \*\* 2", r"np\.minimum\(x, \(V_CAP / \(rr \* H\)\) \*\* 2\)", r"lcap = lambda xc: 1\.75 \* math\.sqrt\(XLIN / xc\)",
                       r"THE CAP\.  MS5's kappa form", r"\"kappa\": lambda M, Mb, a0: RCAP", r"U = C \* F\(d_\(PX\), d_\(PX, 2\)\)",
                       r"xkap = \(V_CAP \*\* 2 / r \*\* 2\) / H \*\* 2", r"x_cap = v_cap\^2 kappa_X\^2/H\(a\)\^2"]),
        ("withdrawn_vloc", [r"thr = X_C0 \* np\.maximum\(1\.0, vloc2 / VCAP_CODE2\)", r"scale = np\.maximum\(1\.0, vloc2 / V_CAP \*\* 2\)",
                            r"\"L395/nfw_ext\": lambda M, Mb, a0: edge_L395", r"ON where x >= x_c,eff\(z\) max\(1, v_loc",
                            r"F2 = \(d_\(sAB, 2\).*/ \(1 \+ d_\(sAB\) \*\* 2", r"MS3's local cap \(v_cap = 325 km/s\)",
                            r"the capped switch itself \(L395's form"]),
        ("hard_radius_MS3", [r"re = min\(re, rcap\)", r"f = np\.where\(r <= rcap, f, 0\.0\)", r"\"msc\": \(\"door\", 1\.75\)",
                             r"R_of\(XLIN, A0M\[f_\], 1\.75, \"door\", ret\)", r"R_of\(XLIN, A0\[f_\], rc_, \"door\""]),
        ("none", [r"\"curv\": \(\"upper\", math\.inf\)", r"\"matter\": \(\"upper\", math\.inf\)", r"the cap is not applied", r"RMAX = |no cap"]),
    ],
    "kernel": [
        ("nu_mono", [r"nu_mono", r"L352's nu_mono table"]),
        ("nu_RAR", [r"L20\[\"nu\"\]", r"nu_RAR", r"D4\[\"nu\"\]", r"1\.0 / \(1\.0 - math\.exp\(-math\.sqrt\(y\)\)\)"]),
        ("generic", [r"q = c1 s\^\(3/2\) \+ d1 log\(1 \+ s\)", r"F = sp\.Function\(\"F\"\)"]),
    ],
    "carrier": [
        ("L388_density_trigger", [r"L77\.XC_TRIG", r"L388R\[\"retention_by_mass\"\]", r"ret_L388", r"retention_by_mass\"\]\[\"v",
                                  r"L388 = jl\(DS, \"L388_linear_gate_pooled_results\.json\"\)",
                                  r"retention by host mass from L388", r"L388_linear_gate_pooled_results\.json"]),
        ("L375_resolved_shell", [r"from L375_triggered_carrier_galaxy_retention import halo", r"import L376_triggered_carrier_inner_galaxies",
                                 r"XR9_carrier_halos_results\.json"]),
        ("L372_two_mode", [r"mode U|f_U\(0\)|L372's U \+ G|L372's carrier|two-mode", r"\(0\.25, 750\.0\), \(0\.25, 900\.0\), \(0\.25, 1050\.0\)"]),
        ("AT_acceleration_trigger", [r"y_v0|trig_acc|a_retention\(|YVS = |YV0S = |Gamma = Gamma_0 Theta\(y_b - y_v\)",
                                     r"the acceleration trigger's decay budget"]),
        ("L366_newtonian_transfers", [r"TRANS = \{int\(k_\[1:\]\)"]),
        ("L360_template", [r"L360's post-decay template|carrier: L360's post-decay"]),
        ("intact", [r"single-fluid|every particle feels the\s+phantom|kernel reads all matter"]),
        ("none", [r"shift\(10 \*\* l, f, 2\.5, 1\.0, 2\.5, 0\.0, fc, \"contrast\", \"mond\"\)", r"switch only|switch-only|no carrier",
                  r"rho_car is deliberately NOT added"]),
    ],
    "operator": [
        ("A", [r"def solve_region\(Mb, a0, f, m_inv, sigma", r"\(lap - M\^2\) P = div\[f \(nu_mono", r"operator A \(L361",
               r"extra = solve_region\(Mb, a0, f, 100 \* KPC_, 1\.0\)", r"L361_bound_region_kernel\.py:16-32"]),
        ("B", [r"import L377_full_construction_pm as L77", r"import L379_clearing_by_environment as L79", r"import L395_two_switch_branches as L95",
               r"operator B \(the PM track"]),
        ("B_all_matter", [r"import L347_switch_forest_flux_power as L7"]),
        ("C", [r"def phantom_felt\(grid, rb, rreal", r"from L389_harvey_same_cell_linear_gate import harvey_cell",
               r"P71 = os\.path\.join\(REPO, \"real_research\", \"merger_infall_2026\", \"L371", r"HNS\[\"SW_DEF\"\] = SW_COMMON"]),
        ("halo_model", [r"def transform\(M, Mb, xc, a0, rcap, conv\)", r"def transform_smooth\(", r"def R_capfun\(",
                        r"R_of, SCEN, ret_L388, XLIN, A0, E2m = MS\["]),
        ("analytic_radial", [r"def rho_phantom_on\(Mb, a0, r\)", r"Mdyn = Mb \* nu_vec\(G \* Mb / rr \*\* 2 / a0\)",
                             r"return Mb \* MS \* nu_mono_vec\(yN\)", r"M = Mb \* MS \* nu_mono_vec"]),
    ],
}


def classify(axis, line):
    """the code part (before any '#') first; the whole line only if the code part matches nothing.  Exactly one
    category must match, or the trace is ambiguous."""
    for part in (line.split("#")[0], line):
        hits = list(dict.fromkeys(cat for cat, pats in SIG[axis] if any(re.search(p_, part) for p_ in pats)))
        if hits:
            break
    if len(hits) != 1:
        raise TraceError(f"{axis}: line classifies as {hits or 'nothing'}: {line.strip()[:120]!r}")
    return hits[0]


class TraceError(Exception):
    pass


# ======================================================================================================================
# FILE ACCESS (read-only): committed version for committed files, the working tree for untracked ones
# ======================================================================================================================
_ST, _TXT, _COMMIT = {}, {}, {}


def git(*a):
    return subprocess.run(["git", *a], cwd=REPO, capture_output=True, text=True)


_PORC = None


_TRACKED = None


def git_state(path):
    """committed | modified | untracked | ignored | deleted-in-tree | absent, from two git calls for the whole tree."""
    global _PORC, _TRACKED
    if _PORC is None:
        _PORC = {ln[3:].strip().strip('"'): ln[:2] for ln in git("status", "--porcelain", "--untracked-files=all").stdout.splitlines()}
        _TRACKED = set(git("ls-files", "real_research").stdout.splitlines())
    if path not in _ST:
        exists = os.path.exists(os.path.join(REPO, path))
        if path in _PORC:
            _ST[path] = "untracked" if _PORC[path] == "??" else ("modified" if exists else "deleted-in-tree")
        elif path in _TRACKED:
            _ST[path] = "committed" if exists else "deleted-in-tree"
        else:
            _ST[path] = "ignored" if exists else "absent"
    return _ST[path]


def text_of(path):
    """(text, origin): HEAD's blob for committed/modified files (the source the committed results came from), the working
    tree for untracked files."""
    if path not in _TXT:
        st = git_state(path)
        if st in ("committed", "modified", "deleted-in-tree"):
            r = git("show", f"HEAD:{path}")
            _TXT[path] = (r.stdout if r.returncode == 0 else None, "HEAD" + ("*" if st != "committed" else ""))
        elif st in ("untracked", "ignored"):
            _TXT[path] = (open(os.path.join(REPO, path), encoding="utf-8", errors="replace").read(), "WT" if st == "untracked" else "WT, gitignored")
        else:
            _TXT[path] = (None, "absent")
    return _TXT[path]


def commit_of(path):
    """last commit touching the file (one batched git log for every registered script, on first use)."""
    if not _COMMIT:
        paths = sorted({r_["script"] for r_ in REG["rows"]})
        cur = None
        for ln in git("log", "--format=%x01%h", "--name-only", "--", *paths).stdout.splitlines():
            if ln.startswith("\x01"):
                cur = ln[1:]
            elif ln.strip() and ln.strip() not in _COMMIT:
                _COMMIT[ln.strip()] = cur
        _COMMIT["__done__"] = True
    if git_state(path) in ("untracked", "ignored", "absent"):
        return "uncommitted"
    return _COMMIT.get(path) or git("log", "-1", "--format=%h", "--", path).stdout.strip() or "?"


def find_lines(path, pattern):
    txt, origin = text_of(path)
    if txt is None:
        raise TraceError(f"{path}: {origin}")
    return [(i, ln) for i, ln in enumerate(txt.splitlines(), 1) if re.search(pattern, ln)], origin


_JS = {}


def jload(path):
    """committed JSON only (None if the file is not at HEAD)."""
    if path not in _JS:
        if git_state(path) not in ("committed", "modified"):
            _JS[path] = None
        else:
            r = git("show", f"HEAD:{path}")
            _JS[path] = json.loads(r.stdout) if r.returncode == 0 else None
    return _JS[path]


def short(path):
    return path.replace("real_research/", "")


# ======================================================================================================================
# DERIVATIONS
# ======================================================================================================================
FOOT_TOK = [(r"A0C\b|\bcanonical\b", "canonical"), (r"A0A\b|\"alt\"|A0\[\"alt\"\]", "alt")]


def derive(axis, e):
    """returns (value, evidence) from the source; raises TraceError when the trace is lost."""
    kind = e.get("derive", "classify")
    if kind == "na" and "src" not in e:
        return "n/a", e.get("reason", "")
    for v in e.get("via", []):                                   # the import / call chain must still be there
        hits, origin = find_lines(v["src"], v["pattern"])
        if not hits:
            raise TraceError(f"via link lost: {short(v['src'])} /{v['pattern']}/")
    hits, origin = find_lines(e["src"], e["pattern"])
    if not hits:
        raise TraceError(f"pattern not found in {short(e['src'])} [{origin}]: /{e['pattern']}/")
    ln, txt = hits[0]
    ev = f"{short(e['src'])}:{ln}" + ("" if origin == "HEAD" else f" [{origin}]")
    if e.get("via"):
        ev += " via " + ", ".join(f"{short(v['src'])}:{find_lines(v['src'], v['pattern'])[0][0][0]}" for v in e["via"])
    if kind == "na":                                              # n/a, with the line that shows why
        return "n/a", ev
    if kind == "classify":
        if e.get("classify_on"):                                  # classify one part of the line (e.g. one dict entry)
            m = re.search(e["classify_on"], txt)
            if not m:
                raise TraceError(f"classify_on /{e['classify_on']}/ not on {ev}")
            return classify(axis, m.group(0)), ev
        return classify(axis, txt), ev
    if kind == "float":
        m = re.search(e["pattern"], txt)
        return float(m.group(e.get("group", 1))), ev
    if kind == "power":                                           # the gate exponent p read off x_c0 * E(z)^(2p): no '** p' means p = 1
        m = re.search(e["pattern"], txt)
        return (float(m.group(1)) if m.group(1) else 1.0), ev
    if kind == "pairs":                                           # a list of (p, x_c0) cells, read as pairs
        m = re.search(e["pattern"], txt)
        xs = [float(x) for x in re.findall(r"[\d.]+(?:e[+-]?\d+)?", m.group(e.get("group", 1)))]
        if len(xs) % 2:
            raise TraceError(f"odd number of values for (p, x_c0) pairs on {ev}")
        return [[xs[i], xs[i + 1]] for i in range(0, len(xs), 2)], ev
    if kind == "floats":
        m = re.search(e["pattern"], txt)
        return [float(x) for x in re.findall(r"[\d.]+(?:e[+-]?\d+)?", m.group(e.get("group", 1)))], ev
    if kind == "footings":                                        # every matching line, 'canonical'/'alt' tokens
        got = set()
        for _, t in hits:
            for rx, name in FOOT_TOK:
                if re.search(rx, t):
                    got.add(name)
        if not got:
            raise TraceError(f"no footing token on the lines matching /{e['pattern']}/ in {short(e['src'])}")
        ev = f"{short(e['src'])}:" + ",".join(str(i) for i, _ in hits[:6]) + ("" if origin == "HEAD" else f" [{origin}]")
        return [f_ for f_ in ("canonical", "alt") if f_ in got], ev
    if kind == "present":
        return e["value"], ev
    if kind == "absent":                                          # value holds iff NO line of the listed files matches
        for f_ in e.get("files", [e["src"]]):
            h_, _ = find_lines(f_, e["absent"])
            if h_:
                raise TraceError(f"'{e['value']}' asserted by absence, but {short(f_)}:{h_[0][0]} matches /{e['absent']}/")
        return e["value"], ev + f" (and no /{e['absent']}/ in {', '.join(short(f_) for f_ in e.get('files', [e['src']]))})"
    raise TraceError(f"unknown derivation {kind}")


# ======================================================================================================================
# THE REGISTRY
# ======================================================================================================================
REG = json.load(open(os.path.join(HERE, "XR10_answer_rows.json")))
ATOMS, RULES, ROWS = REG["atoms"], REG["rules"], REG["rows"]
if MUTATE:
    for r_ in ROWS:
        if r_["id"] == "DE10.kids":
            r_["axes"]["cap_form"] = [dict(ATOMS[x["atom"]], **{k: v for k, v in x.items() if k != "atom"}) if "atom" in x else x
                                      for x in r_["axes"]["cap_form"]]
            r_["axes"]["cap_form"][0]["value"] = "kappa_MS5"


ROWMAP = {r_["id"]: r_ for r_ in ROWS}


def entries(row, axis, depth=0):
    out = []
    for x in row["axes"].get(axis, []):
        if "same_as" in x:                                        # the axis is inherited from another row (its traces)
            if depth > 3 or x["same_as"] not in ROWMAP:
                raise KeyError(f"{row['id']}.{axis}: same_as {x.get('same_as')!r}")
            out.extend(dict(y, inherited=x["same_as"]) for y in entries(ROWMAP[x["same_as"]], axis, depth + 1))
        elif "atom" in x:
            y = dict(ATOMS[x["atom"]]); y.update({k: v for k, v in x.items() if k != "atom"}); y["atom"] = x["atom"]
            out.append(y)
        else:
            out.append(dict(x))
    return out


# ======================================================================================================================
# RULES: approximations a committed lane has shown to be controlled (enabled) and candidates (reported only)
# ======================================================================================================================
def check_evidence(ev):
    k = ev["kind"]
    if k == "text":
        txt, origin = text_of(ev["file"])
        ok = txt is not None and origin.startswith("HEAD") and ev["contains"] in txt
        return ok, f"{short(ev['file'])} [{origin}] contains {ev['contains'][:60]!r}: {ok}"
    if k == "json_check":
        d = jload(ev["file"])
        if d is None:
            return False, f"{short(ev['file'])} not committed"
        key = next((c for c in d["checks"] if c.split()[0] == ev["check"]), None)
        c = d["checks"].get(key, {}) if key else {}
        ok = bool(c.get("ok", c.get("pass"))) and ev.get("contains", "") in c.get("measured", "")
        return ok, f"{short(ev['file'])} check {ev['check']}: ok={c.get('ok', c.get('pass'))} ({c.get('measured', '')[:70]})"
    if k == "json_le":
        d = jload(ev["file"])
        v = d
        for p_ in ev["path"]:
            v = v[p_]
        return v <= ev["max"], f"{short(ev['file'])} {'/'.join(ev['path'])} = {v:.4g} <= {ev['max']}"
    if k == "json_close":
        a, b = jload(ev["file"]), jload(ev["file2"])
        for p_ in ev["path"]:
            a = a[p_]
        for p_ in ev["path2"]:
            b = b[p_]
        return abs(a - b) <= ev["tol"], f"{'/'.join(ev['path'])} {a:.6f} vs {short(ev['file2'])} {'/'.join(ev['path2'])} {b:.6f}"
    if k == "window_contains":                                    # DE9's MOND-sector window at M*'s p contains M*'s x_c0
        d = jload(ev["file"])
        key = f"{ev['reading']}/{MSTAR['p']:g}" if f"{ev['reading']}/{MSTAR['p']:g}" in d["numbers"]["window"] else f"{ev['reading']}/{MSTAR['p']:.1f}"
        win = d["numbers"]["window"].get(key, {})
        rng = [win.get(w_) for w_ in ev["widths"]]
        ok = all(r_ is not None and r_[0] <= MSTAR["x_c0"] <= r_[1] for r_ in rng)
        return ok, f"DE9 window {key} at w = {ev['widths']}: {rng} contains x_c0 = {MSTAR['x_c0']}: {ok}"
    if k == "mstar_is":
        ok = abs(MSTAR[ev["key"]] - ev["value"]) < 1e-9
        return ok, f"evidence computed at {ev['key']} = {ev['value']} (M*: {MSTAR[ev['key']]})"
    if k == "computed_lcap":                                     # l_cap(z) = v_cap/(H sqrt(x_c,eff)) against a radius
        E2 = 0.3138 * (1 + ev["z"]) ** 3 + 0.6862
        H = 67.36 * math.sqrt(E2)
        lcap = ev["v_cap"] / (H * math.sqrt(MSTAR["x_c0"] * E2 ** MSTAR["p"]))
        return lcap * 1e3 > ev["r_kpc"], f"l_cap(z = {ev['z']}) = {lcap * 1e3:.0f} kpc (M*'s cell) vs {ev['r_kpc']} kpc"
    raise ValueError(k)


MSTAR_DEPENDENT = ("window_contains", "mstar_is", "computed_lcap")    # evidence that depends on M*'s own parameters
RULE_OK, RULE_AT_MSTAR = {}, {}
for rid, ru in RULES.items():
    res = [(check_evidence(ev), ev["kind"] in MSTAR_DEPENDENT) for ev in ru["evidence"]]
    RULE_OK[rid] = (all(r_[0][0] for r_ in res), [m for (_, m), _ in res])
    RULE_AT_MSTAR[rid] = all(r_[0][0] for r_ in res if not r_[1])       # the committed evidence itself holds


def in_from(value, frm):
    vals = value if isinstance(value, list) else [value]
    return bool(vals) and all(v in frm for v in vals)


def rule_applies(rid, row, axis, e, value):
    ru = RULES[rid]
    if ru["axis"] != axis or not in_from(value, ru["from"]):
        return False, ""
    if row["kind"] not in ru.get("kinds", ["data", "action"]):
        return False, f"{rid}: not for {row['kind']}-level rows"
    gates = set(row["gates"])
    if "gates_only" in ru and not gates <= set(ru["gates_only"]):
        return False, f"{rid}: covers only {ru['gates_only']}, row scores {sorted(gates - set(ru['gates_only']))}"
    if ru.get("exclude_efe") and gates & EFE_GATES:
        return False, f"{rid}: not controlled for the EFE ({sorted(gates & EFE_GATES)})"
    if "uses" in ru and e.get("use") not in ru["uses"]:
        return False, f"{rid}: only for use {ru['uses']}, entry is {e.get('use')!r}"
    if not RULE_OK[rid][0]:
        return False, f"{rid}: evidence does not hold ({'; '.join(RULE_OK[rid][1])[:120]})"
    if f"[{rid}]" not in row.get("scope", ""):
        return False, f"{rid} would apply, but the row's scope does not state [{rid}]"
    return True, rid


# ======================================================================================================================
# EVALUATION AGAINST M*
# ======================================================================================================================
def compare(row, axis, e, value):
    """base comparison: ('MATCH'|'MISMATCH'|'N/A', note)."""
    if value == "n/a" or (isinstance(value, str) and value.startswith("n/a")):
        return "N/A", e.get("reason", "")
    if axis == "switch_reading":
        if value == MSTAR["switch_reading"]:
            return "MATCH", ""
        if value in MSTAR["switch_equivalent"]:
            if row["kind"] == "data":
                return "MATCH", "phiX: the same gate value as CV3's constrained form (recorded)"
            return "MISMATCH", "action-level: CV3 G3/G3b -- lap(Phi - v) reads the multiplier Phi; only CV3's constrained form keeps the lapse constraint regular"
        return "MISMATCH", ""
    if axis == "cap_form":
        return ("MATCH", "") if value == MSTAR["cap_form"] else ("MISMATCH", "")
    if axis in ("p", "x_c0") and isinstance(value, list) and value and isinstance(value[0], list):     # (p, x_c0) cells
        on = [MSTAR["p"], MSTAR["x_c0"]] in [[float(a_), float(b_)] for a_, b_ in value]
        return ("MATCH", "M*'s (p, x_c0) is one cell of the scan") if on else ("MISMATCH", f"M*'s cell ({MSTAR['p']:g}, {MSTAR['x_c0']:g}) is not scanned")
    if axis in ("p", "x_c0"):
        vals = value if isinstance(value, list) else [value]
        return ("MATCH", "" if len(vals) == 1 else "M*'s value is one cell of the scan") if any(abs(v - MSTAR[axis]) < 1e-9 for v in vals) \
            else ("MISMATCH", f"M* {axis} = {MSTAR[axis]:g}")
    if axis == "w":
        vals = value if isinstance(value, list) else [value]
        good = [v for v in vals if 0 < v <= MSTAR["w_max"] + 1e-12]
        if good and len(good) == len(vals):
            return "MATCH", ""
        if good:
            return "MATCH", f"widths above w_max also scored: {[v for v in vals if v not in good]}"
        return "MISMATCH", "hard switch (w = 0)" if all(v == 0 for v in vals) else f"w > {MSTAR['w_max']}"
    if axis == "kernel":
        return ("MATCH", "") if value == MSTAR["kernel"] else ("N/A", "generic kernel (a symbolic identity)") if value == "generic" else ("MISMATCH", "")
    if axis == "sigma":
        vals = value if isinstance(value, list) else [value]
        if any(abs(float(v) - MSTAR["sigma"]) < 1e-9 for v in vals):
            return "MATCH", ("" if len(vals) == 1 else "both sigma scored")
        return "MISMATCH", ""
    if axis == "operator":
        if value == MSTAR["operator"]:
            return "MATCH", ""
        if value in ("halo_model", "analytic_radial"):
            return "N/A", "no field operator: the exact spherical phantom of an isolated system"
        return "MISMATCH", ""
    if axis == "carrier":
        return ("MATCH", "") if value == MSTAR["carrier"] else ("MISMATCH", "")
    if axis == "kick":
        vals = value if isinstance(value, list) else [value]
        lo, hi = MSTAR["kick_kms"]
        inside = [v for v in vals if lo - 1e-9 <= v <= hi + 1e-9]
        if inside and len(inside) == len(vals):
            return "MATCH", ""
        return "MISMATCH", f"kicks outside {lo:g}-{hi:g}: {[v for v in vals if v not in inside]}"
    if axis == "footings":
        return ("MATCH", "") if set(value) >= set(MSTAR["footings"]) else ("MISMATCH", f"{'/'.join(value)} only")
    raise ValueError(axis)


def evaluate(row):
    """per axis: list of (entry, value, evidence, status, note, drift) and row flags."""
    res, flags = {}, []
    for axis in AXES:
        if axis == "epoch":
            continue
        out = []
        for e in entries(row, axis):
            drift = None
            try:
                val, ev = derive(axis, e)
            except TraceError as ex:
                val, ev, drift = e.get("value"), "TRACE LOST", str(ex)
            reg = e.get("value")
            if drift is None and e.get("derive", "classify") not in ("present", "na"):
                same = (val == reg) if isinstance(val, list) and val and isinstance(val[0], list) else \
                    (sorted(map(float, val)) == sorted(map(float, reg))) if isinstance(val, list) and all(isinstance(x, (int, float)) for x in val) \
                    else (sorted(val) == sorted(reg)) if isinstance(val, list) else (abs(val - reg) < 1e-9 if isinstance(val, float) else val == reg)
                if not same:
                    drift = f"registry says {reg!r}, source gives {val!r}"
            st, note = compare(row, axis, e, val)
            if st == "MISMATCH":
                cands = []
                for rid, ru in RULES.items():
                    ok, why = rule_applies(rid, row, axis, e, val) if ru.get("enabled") else (False, "")
                    if ok:
                        st, note = "COMPAT", f"[{rid}]"
                        break
                    if why and ru.get("enabled") and ru["axis"] == axis and in_from(val, ru["from"]):
                        note = (note + "; " if note else "") + why
                    if not ru.get("enabled") and ru["axis"] == axis and in_from(val, ru["from"]):
                        ok_c, why_c = rule_applies(rid, row, axis, e, val)
                        if ok_c or ("scope does not state" in why_c and RULE_OK[rid][0]):
                            cands.append(rid)
                if st == "MISMATCH" and cands:
                    note = (note + "; " if note else "") + f"candidate rule(s), not enabled: {cands}"
            out.append(dict(e=e, val=val, ev=ev, st=st, note=note, drift=drift))
        res[axis] = out
    # epoch: retention epochs against the scoring epoch, per use
    ep = []
    for e in entries(row, "epoch"):
        drift = None
        try:
            val, ev = derive("epoch", e)
        except TraceError as ex:
            val, ev, drift = e.get("value"), "TRACE LOST", str(ex)
        if drift is None and e.get("derive") not in ("na", "present") and abs(float(val) - float(e["value"])) > 1e-9:
            drift = f"registry says {e['value']}, source gives {val}"
        ep.append(dict(e=e, val=val, ev=ev, drift=drift))
    out = []
    uses = sorted({x["e"].get("use", "") for x in ep})
    for u in uses:
        sc = [x for x in ep if x["e"].get("use", "") == u and x["e"].get("role") == "score"]
        rt = [x for x in ep if x["e"].get("use", "") == u and x["e"].get("role") == "retention"]
        na = [x for x in ep if x["e"].get("use", "") == u and x["e"].get("role") == "n/a"]
        if na and not sc:
            out.append(dict(e=na[0]["e"], val="n/a", ev=na[0]["ev"], st="N/A", note=na[0]["e"].get("reason", ""), drift=na[0]["drift"]))
            continue
        zs = sc[0]["val"] if sc else None
        bad = [x for x in rt if zs is not None and x["val"] != "n/a" and abs(float(x["val"]) - float(zs)) > MSTAR["epoch_dz_tol"] + 1e-12]
        val = f"retention z = {sorted({float(x['val']) for x in rt})} for scoring z = {zs}" if rt else f"scoring z = {zs}"
        st = "MISMATCH" if bad else ("MATCH" if rt else "N/A")
        note = ("EPOCH-MIXED: " + "; ".join(f"{x['e'].get('what', '')} at z = {x['val']:g}" for x in bad)) if bad else ""
        drift = "; ".join(x["drift"] for x in sc + rt if x["drift"]) or None
        out.append(dict(e=dict(use=u), val=val, ev="; ".join(f"{x['e'].get('what', x['e'].get('role'))} {x['ev']}" for x in sc + rt), st=st, note=note, drift=drift))
    res["epoch"] = out
    # row flags
    # a split is between STAGES of one result; separately reported branches (use 'branch_...') are not stages
    caps = [x for x in res["cap_form"] if x["st"] != "N/A" and not str(x["e"].get("use", "")).startswith("branch_")]
    if len({x["val"] for x in caps}) > 1 and any(x["st"] == "MISMATCH" for x in caps):
        flags.append("CAP-SPLIT: " + ", ".join(f"{x['e'].get('use')}={x['val']}" for x in caps))
    sws = [x for x in res["switch_reading"] if x["st"] != "N/A" and not str(x["e"].get("use", "")).startswith("branch_")]
    if len({x["val"] for x in sws}) > 1 and any(x["st"] == "MISMATCH" for x in sws):
        flags.append("SWITCH-SPLIT: " + ", ".join(f"{x['e'].get('use')}={x['val']}" for x in sws))
    if any(x["st"] == "MISMATCH" for x in res["footings"]):
        flags.append("FOOTING-PARTIAL")
    if any(x["st"] == "MISMATCH" for x in res["epoch"]):
        flags.append("EPOCH-MIXED")
    return res, flags


CORE = ("switch_reading", "cap_form", "x_c0", "carrier")


def row_status(row, res):
    """OFF-M*: a mismatch on any axis.  n/a: no core axis (switch, cap, x_c0, carrier) enters -- the row does not
    instantiate the model.  PARTIAL: a data row with a core axis not traced.  ON-M*~: on M* with stated approximations."""
    sts = [x["st"] for a in AXES for x in res[a]]
    if "MISMATCH" in sts:
        return "OFF-M*"
    core = [x["st"] for a in CORE for x in res[a]]
    if all(c == "N/A" for c in core):
        return "n/a"
    if row["kind"] == "data" and "N/A" in core:
        return "PARTIAL"
    return "ON-M*~" if "COMPAT" in sts else "ON-M*"


def axis_cell(xs):
    if not xs:
        return "."
    sts = {x["st"] for x in xs}
    if "MISMATCH" in sts:
        return "X"
    if "COMPAT" in sts:
        return "~"
    if sts == {"N/A"}:
        return "-"
    return "ok"


# ======================================================================================================================
# VERDICTS from committed results
# ======================================================================================================================
def verdict(row):
    rj = row.get("results")
    d = jload(rj) if rj else None
    if d is None:
        o = row.get("out")
        if o and git_state(o) in ("committed", "modified"):
            txt, _ = text_of(o)
            m = [ln for ln in txt.splitlines() if "checks pass" in ln]
            if m:
                return m[-1].strip()[:110], True
        on_disk = rj and git_state(rj) in ("untracked", "ignored")
        return "pending: no committed results" + (" (an uncommitted results JSON is on disk, not read)" if on_disk else ""), False
    ch = d.get("checks", {})
    okv = lambda v: v.get("ok", v.get("pass")) if isinstance(v, dict) else v
    n, npass = len(ch), sum(1 for v in ch.values() if okv(v) is True)
    lbf = [k.split()[0] for k, v in ch.items() if okv(v) is not True and (not isinstance(v, dict) or v.get("load_bearing", True))]
    s = f"{npass}/{n}" + (f", load-bearing FAIL {lbf}" if lbf else "")
    hc = row.get("headline_check")
    if hc:
        key = next((k for k in ch if k.split()[0] == hc), None)
        if key:
            s += f"; {hc}: {str(ch[key].get('measured', ''))[:150]}"
    return s, True


# ======================================================================================================================
# RUN
# ======================================================================================================================
P(__doc__.split("RC = 1 IF")[0].strip())
head = git("rev-parse", "--short", "HEAD").stdout.strip()
P(f"\n  registry: {len(ROWS)} rows, {len(ATOMS)} shared traces, {len(RULES)} rules; inspected {REG['inspected_at']} at "
  f"{REG['git_head'][:9]}; now HEAD {head}")
P("  M* = " + ", ".join(f"{k} {v}" for k, v in MSTAR.items()))
if MUTATE:
    P("\n  *** MUTATE=1: DE10's registered cap form is corrupted to 'kappa_MS5' in memory (hides its withdrawn local form); "
      "check D must fail and rc must be 1 ***")
if SCORECARD:
    P("\n  *** XR10_SCORECARD=1: every row the current scorecard cites is treated as claimed M* ***")
FAIL = []


def fail(tag, msg):
    FAIL.append((tag, msg)); P(f"  ** {tag}: {msg}")


P("\n" + "=" * 120 + "\nE  THE APPROXIMATION RULES: each one's evidence, re-checked in the committed files\n" + "=" * 120)
for rid, ru in RULES.items():
    ok, msgs = RULE_OK[rid]
    tag = "enabled " if ru.get("enabled") else "CANDIDATE (not enabled)"
    P(f"  [{'PASS' if ok else 'FAIL'}] {rid:26s} {tag}: {ru['axis']} {ru['from']} -> {ru['to']}  | {ru['scope_text']}")
    for m in msgs:
        P(f"           {m}")
    if ru.get("enabled") and not ok:
        if RULE_AT_MSTAR[rid]:
            P(f"           -> not applicable at this M* (its evidence was computed at other parameters); rows relying on it are mismatches")
        else:
            fail("E", f"enabled rule {rid}: its committed evidence does not hold")

RES = {}
for row in ROWS:
    RES[row["id"]] = evaluate(row)

P("\n" + "=" * 120 + "\nD  REGISTRY vs SOURCE (drift on a committed row is a failure; on a pending row it is reported)\n" + "=" * 120)
nd = 0
for row in ROWS:
    res, _ = RES[row["id"]]
    pending = row["claim"] == "pending" or commit_of(row["script"]) == "uncommitted"
    for a in AXES:
        for x in res[a]:
            if x["drift"]:
                nd += 1
                msg = f"{row['id']}.{a}{'[' + x['e'].get('use', '') + ']' if x['e'].get('use') else ''}: {x['drift']}"
                if pending:
                    P(f"  (pending row, reported) {msg}")
                else:
                    fail("D", msg)
P(f"  {nd} drift item(s); {sum(len(RES[r['id']][0][a]) for r in ROWS for a in AXES)} traced axis entries")


def evidence_now(row):
    res, _ = RES[row["id"]]
    return {a: [f"{x['e'].get('use', '')}: {x['val']} <- {x['ev']}" for x in res[a]] for a in AXES}


moved, recommitted = [], []
for row in ROWS:
    rec = row.get("recorded")
    if not rec:
        continue
    now = evidence_now(row)
    moved += [f"{row['id']}.{a}" for a in AXES if rec["evidence"].get(a) != now[a]]
    if rec.get("commit") != commit_of(row["script"]):
        recommitted.append(f"{row['id']} ({rec.get('commit')} -> {commit_of(row['script'])})")
P(f"  (reported) since the registry's snapshot: {len(moved)} axis trace(s) moved or changed line"
  + (f" [{', '.join(moved[:8])}{' ...' if len(moved) > 8 else ''}]" if moved else "")
  + f"; scripts re-committed: {recommitted or 'none'}")

P("\n" + "=" * 120 + "\nTHE TABLE: per row, each axis against M*  (ok = match, ~ = compatible approximation, X = mismatch, - = n/a)\n" + "=" * 120)
hdr = f"  {'row':24s} {'commit':10s} {'claim':10s} " + " ".join(f"{ABBR[a]:>6s}" for a in AXES) + "  status    verdict (committed)"
P(hdr)
STAT = {}
for row in ROWS:
    res, flags = RES[row["id"]]
    st = row_status(row, res)
    STAT[row["id"]] = st
    cm = commit_of(row["script"])
    v, _ = verdict(row)
    P(f"  {row['id']:24s} {cm:10s} {row['claim']:10s} " + " ".join(f"{axis_cell(res[a]):>6s}" for a in AXES)
      + f"  {st:8s}  {v[:70]}")

P("\n" + "=" * 120 + "\nDETAIL: every axis entry with its value, file:line and status (mismatches and approximations first)\n" + "=" * 120)
for row in ROWS:
    res, flags = RES[row["id"]]
    cm = commit_of(row["script"])
    v, _ = verdict(row)
    P(f"\n  {row['id']}  [{row['lane']}, {cm}, claim {row['claim']}, {row['kind']}-level]  gates {row['gates']}  -> {STAT[row['id']]}"
      + (f"   FLAGS: {' | '.join(flags)}" if flags else ""))
    P(f"    verdict: {v}")
    if row.get("owner_claim"):
        P(f"    owner says: {row['owner_claim']}")
    for a in AXES:
        for x in sorted(res[a], key=lambda x: {"MISMATCH": 0, "COMPAT": 1, "MATCH": 2, "N/A": 3}[x["st"]]):
            u = x["e"].get("use")
            vv = x["val"] if not isinstance(x["val"], list) else "/".join(f"{y:g}" if isinstance(y, float) else str(y) for y in x["val"])
            P(f"    {x['st']:8s} {ABBR[a]:6s}{('[' + u + ']') if u else '':20s} {str(vv)[:60]:60s} {x['ev'][:120]}"
              + (f"\n             {x['note'][:190]}" if x["note"] and x["note"] != x["ev"] else ""))

# ------------------------------------------------------------------------------------------------ claims (check M)
def claim_check(row, res, status):
    """(ok, reason) for a row claimed as an M* result."""
    cm = commit_of(row["script"])
    _, committed = verdict(row)
    mis = [f"{ABBR[a]}{'[' + x['e'].get('use') + ']' if x['e'].get('use') else ''}={x['val']}" for a in AXES for x in res[a] if x["st"] == "MISMATCH"]
    # an M* claim needs its defining axes DERIVED from code: classified (switch, cap, carrier), parsed (p, x_c0), tokenised (footings)
    need = {"switch_reading": ("classify",), "cap_form": ("classify",), "carrier": ("classify",), "p": ("float", "floats", "power", "pairs"),
            "x_c0": ("float", "floats", "pairs"), "footings": ("footings",)}
    weak = [f"{ABBR[a]} ({x['e'].get('derive', 'classify')})" for a, kinds in need.items() for x in res[a]
            if x["e"].get("derive", "classify") not in kinds]
    mis += [f"weakly traced: {', '.join(weak)}"] if weak else []
    ok = not mis and cm != "uncommitted" and committed and status in ("ON-M*", "ON-M*~")
    why = "on M*" if ok else (("; ".join(mis) or f"status {status}") + ("" if cm != "uncommitted" and committed else " [not committed]"))
    return ok, why


P("\n" + "=" * 120 + "\nM  CLAIMS: rows claimed as M* results must be committed, derived from code and match M* on every axis\n" + "=" * 120)
claimed = [r for r in ROWS if r["claim"] == "M*" or (SCORECARD and r.get("scorecard"))]
for row in claimed:
    ok, why = claim_check(row, RES[row["id"]][0], STAT[row["id"]])
    P(f"  [{'PASS' if ok else 'FAIL'}] {row['id']:24s} {commit_of(row['script']):10s} {why[:175]}")
    if not ok:
        fail("M", f"{row['id']} claimed M*: {why[:150]}")
P(f"  {len(claimed)} row(s) claimed as M* results" + (" (scorecard mode)" if SCORECARD else ""))

# ------------------------------------------------------------------------------------------------ controls
P("\n" + "=" * 120 + "\nCONTROLS\n" + "=" * 120)
r95 = next(r for r in ROWS if r["id"] == "L395.c_msc")
res95, fl95 = RES["L395.c_msc"]
caps95 = {x["e"].get("use"): (x["val"], x["st"], x["ev"]) for x in res95["cap_form"]}
ok1 = (caps95.get("pm_dynamics", (None, None))[:2] == ("withdrawn_vloc", "MISMATCH")
       and caps95.get("halo_model_shear", (None, None))[0] == "hard_radius_MS3"
       and any(f_.startswith("CAP-SPLIT") for f_ in fl95) and STAT["L395.c_msc"] == "OFF-M*"
       and all(x["ev"] != "TRACE LOST" for x in res95["cap_form"]))
P(f"  [{'PASS' if ok1 else 'FAIL'}] C1 CONTROL: L395's cell (c) is flagged from its source -- dynamics "
  f"{caps95.get('pm_dynamics', ('?', '?'))[0]} ({caps95.get('pm_dynamics', ('', '', ''))[2]}), shear "
  f"{caps95.get('halo_model_shear', ('?', '?'))[0]} ({caps95.get('halo_model_shear', ('', '', ''))[2]}); flags {fl95}")
if not ok1:
    fail("C1", "L395 (c) not flagged")
neg = []
m5 = {x["e"].get("use"): x["st"] for x in RES["MS5.S1_kappa"][0]["cap_form"]}
neg.append(("MS5.S1_kappa cap form MATCH", m5.get("halo_model_shear") == "MATCH"))
if RULE_OK["HARDCAP_FOR_KAPPA_SHEAR"][0]:                         # these two rest on MS5 S1, computed at x_c0 = 2.5
    m3 = {x["e"].get("use"): (x["st"], x["note"]) for x in RES["MS3.K1"][0]["cap_form"]}
    neg.append(("MS3.K1 hard radius on halo-model shear COMPAT [HARDCAP_FOR_KAPPA_SHEAR]", m3.get("halo_model_shear", ("", ""))[0] == "COMPAT"))
    c96 = {x["e"].get("use"): x["st"] for x in RES["L396.msck"][0]["cap_form"]}
    neg.append(("L396 kappa cap in the dynamics MATCH, hard radius in its shear COMPAT, no CAP-SPLIT",
                c96.get("pm_dynamics") == "MATCH" and c96.get("halo_model_shear") == "COMPAT"
                and not any(f_.startswith("CAP-SPLIT") for f_ in RES["L396.msck"][1])))
else:
    P("  (C2's hard-radius checks skipped: HARDCAP_FOR_KAPPA_SHEAR's evidence is at x_c0 = 2.5, not at this M*)")
for name, ok in neg:
    P(f"  [{'PASS' if ok else 'FAIL'}] C2 NEGATIVE CONTROL: {name}")
    if not ok:
        fail("C2", name)
# C3: the gate can PASS.  MS5's kappa-form shear row, re-evaluated in memory with the epoch tolerance widened to 2 (so its
# z = 0 / z = 2 retention counts as its scoring epoch's), is on M* with stated approximations and a claim on it passes.
_tol = MSTAR["epoch_dz_tol"]; MSTAR["epoch_dz_tol"] = 2.0
_r = ROWMAP["MS5.S1_kappa"]; _res, _ = evaluate(_r); _st = row_status(_r, _res)
MSTAR["epoch_dz_tol"] = _tol
ok3, why3 = claim_check(_r, _res, _st)
if RULE_OK["HARDCAP_FOR_KAPPA_SHEAR"][0] and RULE_OK["HARDW_FOR_SMOOTH"][0]:
    P(f"  [{'PASS' if ok3 else 'FAIL'}] C3 CONTROL (the gate can pass): MS5.S1_kappa with the epoch tolerance widened to 2 is {_st}; "
      f"an M* claim on it: {why3[:110]}")
    if not ok3:
        fail("C3", "the claim gate rejects a row that is on M*")
else:
    P("  (C3 skipped: its row relies on rules whose evidence is at x_c0 = 2.5)")
if MUTATE:
    P("         (MUTATE) trusting the corrupted registry alone, DE10's cap would read kappa_MS5 and its cap mismatch would be "
      "hidden; check D is what catches it")

# ------------------------------------------------------------------------------------------------ the scorecard audit
P("\n" + "=" * 120 + "\nSCORECARD AUDIT (reported): rows the current answer page cites as M* evidence, and what keeps each off M*\n" + "=" * 120)
for row in ROWS:
    if not row.get("scorecard"):
        continue
    res, flags = RES[row["id"]]
    mis = [f"{ABBR[a]}{'[' + x['e'].get('use') + ']' if x['e'].get('use') else ''}={x['val'] if not isinstance(x['val'], list) else '/'.join(map(str, x['val']))}"
           for a in AXES for x in res[a] if x["st"] == "MISMATCH"]
    P(f"  {row['id']:24s} {commit_of(row['script']):10s} {STAT[row['id']]:7s} " + ("; ".join(mis) if mis else "on M* (with the approximations stated)")[:190])

# ------------------------------------------------------------------------------------------------ per lane summary
P("\n" + "=" * 120 + "\nPER LANE\n" + "=" * 120)
lanes = {}
for row in ROWS:
    lanes.setdefault(row["lane"], []).append(row)
for lane, rows in lanes.items():
    sts = sorted({STAT[r["id"]] for r in rows})
    cls = sorted({r["claim"] for r in rows})
    P(f"  {lane:8s} {', '.join(r['id'].split('.', 1)[-1] for r in rows)[:44]:44s} claim {'/'.join(cls):22s} {'/'.join(sts)}")

if SNAPSHOT and not MUTATE and not SCORECARD:
    raw = json.load(open(os.path.join(HERE, "XR10_answer_rows.json")))
    for r_ in raw["rows"]:
        v_, _ = verdict(r_)
        r_["recorded"] = dict(commit=commit_of(r_["script"]), verdict=v_, status=STAT[r_["id"]], evidence=evidence_now(r_))
    raw["inspected_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z"); raw["git_head"] = git("rev-parse", "HEAD").stdout.strip()
    json.dump(raw, open(os.path.join(HERE, "XR10_answer_rows.json"), "w"), indent=1, ensure_ascii=False)
    P(f"\n  XR10_SNAPSHOT=1: recorded commit, verdict, status and every axis's file:line into XR10_answer_rows.json")

P("\n" + "=" * 120 + "\nVERDICT\n" + "=" * 120)
ns = {s: sum(1 for v in STAT.values() if v == s) for s in ("ON-M*", "ON-M*~", "OFF-M*")}
P(f"  {len(ROWS)} rows: {ns['ON-M*']} on M*, {ns['ON-M*~']} on M* with stated approximations, {ns['OFF-M*']} off M*; "
  f"{len(claimed)} claimed as M* results")
P(f"  checks D/M/E/C1/C2/C3: {'all pass' if not FAIL else str(len(FAIL)) + ' failure(s): ' + ', '.join(sorted({t for t, _ in FAIL}))}"
  f"   [{time.time() - T0:.1f}s]")
rc = 1 if FAIL else 0
P(f"rc={rc}")
sys.exit(rc)
